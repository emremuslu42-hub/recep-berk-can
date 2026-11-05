// BSM Mekanik — teklif formu alıcısı
//
// Bağımlılık yok (yalnızca Node.js 18+). Caddy, /api/teklif isteklerini buraya yönlendirir.
// Gelen mesajı SMTP (Google Workspace, port 465/TLS) ile alıcıya e-posta olarak gönderir.
//
// Ayar dosyası (depo dışında): BSM_FORM_CONFIG ortam değişkeni ya da C:\bsmmekanik-key\form.json
//   { "smtpHost": "smtp.gmail.com", "smtpPort": 465, "smtpUser": "bildirim@nesakyazilim.com",
//     "smtpPass": "<uygulama şifresi>", "from": "bildirim@nesakyazilim.com", "fromName": "BSM Mekanik Web Sitesi",
//     "to": "mert@bsmmechanical.com", "port": 8787 }
//
// Kullanım:
//   node server.js          → sunucuyu başlatır (127.0.0.1:8787)
//   node server.js --test   → ayarları kullanarak alıcıya bir deneme e-postası gönderir

"use strict";

const http = require("http");
const tls = require("tls");
const fs = require("fs");
const os = require("os");
const crypto = require("crypto");

const CONFIG_PATH = process.env.BSM_FORM_CONFIG
  || (process.platform === "win32" ? "C:\\bsmmekanik-key\\form.json" : "/etc/bsmmekanik/form.json");

const ALLOWED_ORIGINS = [
  "https://www.bsmmekanik.com", "https://bsmmekanik.com",
  "https://www.bsmmechanical.com", "https://bsmmechanical.com",
  "https://bsmmekanik.nesakyazilim.com",
];

function loadConfig() {
  const c = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf8"));
  for (const k of ["smtpUser", "smtpPass", "to"]) {
    if (!c[k]) throw new Error(`Ayar eksik: ${k} (${CONFIG_PATH})`);
  }
  return {
    smtpHost: "smtp.gmail.com", smtpPort: 465, from: c.smtpUser, fromName: "BSM Mekanik Web Sitesi",
    port: 8787, extraOrigins: [], rejectUnauthorized: true, ...c,
  };
}

function log(...a) { console.log(new Date().toISOString(), ...a); }

// ------------------------------------------------------------------ SMTP (TLS, AUTH LOGIN)
function smtpSend(cfg, { replyTo, subject, text }) {
  return new Promise((resolve, reject) => {
    const sock = tls.connect({
      host: cfg.smtpHost, port: cfg.smtpPort,
      ...(require("net").isIP(cfg.smtpHost) ? {} : { servername: cfg.smtpHost }),
      rejectUnauthorized: cfg.rejectUnauthorized !== false,
    });
    sock.setTimeout(30000, () => { sock.destroy(); reject(new Error("SMTP zaman aşımı")); });
    sock.on("error", reject);

    let buf = "";
    const waiters = [];
    sock.on("data", (d) => {
      buf += d.toString("utf8");
      // Çok satırlı yanıtlar "250-..." ile sürer, "250 ..." ile biter; yalnızca tamamlanmış satırlar işlenir
      let nl;
      while ((nl = buf.indexOf("\n")) !== -1) {
        const line = buf.slice(0, nl).replace(/\r$/, "");
        buf = buf.slice(nl + 1);
        const m = line.match(/^(\d{3})([ -])?/);
        if (m && m[2] !== "-" && waiters.length) waiters.shift()({ code: Number(m[1]), line });
      }
    });
    const expect = (ok) => new Promise((res, rej) => waiters.push((r) =>
      (ok.includes(r.code) ? res(r) : rej(new Error(`SMTP beklenmeyen yanıt: ${r.line}`)))));
    const cmd = (line, ok) => { sock.write(line + "\r\n"); return expect(ok); };

    const b64 = (s) => Buffer.from(s, "utf8").toString("base64");
    const encWord = (s) => `=?UTF-8?B?${b64(s)}?=`;
    const domain = cfg.from.split("@")[1] || "localhost";
    const headers = [
      `From: ${encWord(cfg.fromName)} <${cfg.from}>`,
      `To: <${cfg.to}>`,
      replyTo ? `Reply-To: <${replyTo}>` : null,
      `Subject: ${encWord(subject)}`,
      `Date: ${new Date().toUTCString().replace("GMT", "+0000")}`,
      `Message-ID: <${crypto.randomUUID()}@${domain}>`,
      "MIME-Version: 1.0",
      "Content-Type: text/plain; charset=UTF-8",
      "Content-Transfer-Encoding: base64",
    ].filter(Boolean);
    const body = b64(text).replace(/.{1,76}/g, "$&\r\n");
    const data = headers.join("\r\n") + "\r\n\r\n" + body;

    (async () => {
      await expect([220]);
      await cmd(`EHLO ${os.hostname().replace(/[^A-Za-z0-9.-]/g, "") || "localhost"}`, [250]);
      await cmd("AUTH LOGIN", [334]);
      await cmd(b64(cfg.smtpUser), [334]);
      await cmd(b64(cfg.smtpPass), [235]);
      await cmd(`MAIL FROM:<${cfg.from}>`, [250]);
      await cmd(`RCPT TO:<${cfg.to}>`, [250, 251]);
      await cmd("DATA", [354]);
      // Nokta ile başlayan satırlar SMTP'de iki noktaya çevrilir (base64'te oluşmaz ama güvenli olsun)
      await cmd(data.replace(/\r\n\./g, "\r\n..") + "\r\n.", [250]);
      await cmd("QUIT", [221]).catch(() => {});
      sock.end();
      resolve();
    })().catch((e) => { sock.destroy(); reject(e); });
  });
}

// ------------------------------------------------------------------ doğrulama
const LIMITS = { ad: 120, firma: 160, eposta: 160, telefon: 40, konu: 120, mesaj: 5000 };
const clean = (v, max) => String(v == null ? "" : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "").trim().slice(0, max);
const oneLine = (v) => v.replace(/[\r\n]+/g, " ");
const EMAIL_RE = /^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[A-Za-z]{2,}$/;

function validate(raw) {
  const f = {};
  for (const [k, max] of Object.entries(LIMITS)) f[k] = clean(raw[k], max);
  for (const k of ["ad", "firma", "eposta", "telefon", "konu"]) f[k] = oneLine(f[k]);
  const errors = [];
  if (!f.ad) errors.push("ad");
  if (!EMAIL_RE.test(f.eposta)) errors.push("eposta");
  if (f.mesaj.length < 5) errors.push("mesaj");
  if (!raw.kvkk || raw.kvkk === "false") errors.push("kvkk");
  return { f, errors, lang: raw.lang === "en" ? "en" : "tr", page: oneLine(clean(raw.sayfa, 300)) };
}

// ------------------------------------------------------------------ hız sınırı (IP başına)
const hits = new Map();
function rateLimited(ip) {
  const now = Date.now(), win = 10 * 60 * 1000, max = 5;
  const list = (hits.get(ip) || []).filter((t) => now - t < win);
  list.push(now);
  hits.set(ip, list);
  if (hits.size > 5000) for (const [k, v] of hits) if (!v.some((t) => now - t < win)) hits.delete(k);
  return list.length > max;
}

function mailText(v, ip) {
  const { f } = v;
  return [
    "Web sitesindeki teklif formundan yeni bir mesaj geldi.",
    "",
    `Ad Soyad : ${f.ad}`,
    `Firma    : ${f.firma || "-"}`,
    `E-posta  : ${f.eposta}`,
    `Telefon  : ${f.telefon || "-"}`,
    `Hizmet   : ${f.konu || "-"}`,
    `Dil      : ${v.lang === "en" ? "İngilizce" : "Türkçe"}`,
    "",
    "Mesaj:",
    f.mesaj,
    "",
    "—",
    `Gönderim : ${new Date().toLocaleString("tr-TR", { timeZone: "Europe/Istanbul" })}`,
    `Sayfa    : ${v.page || "-"}`,
    `IP       : ${ip}`,
    "Bu e-postayı yanıtladığınızda yanıtınız doğrudan formu dolduran kişiye gider.",
  ].join("\n");
}

// ------------------------------------------------------------------ HTTP
function readBody(req, limit) {
  return new Promise((resolve, reject) => {
    let size = 0, tooBig = false; const chunks = [];
    req.on("data", (c) => {
      size += c.length;
      if (size > limit) tooBig = true; else chunks.push(c);   // fazlası okunup atılır, bağlantı açık kalır
    });
    req.on("end", () => (tooBig ? reject(Object.assign(new Error("büyük"), { status: 413 }))
      : resolve(Buffer.concat(chunks).toString("utf8"))));
    req.on("error", reject);
  });
}

function send(res, status, obj) {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" });
  res.end(JSON.stringify(obj));
}

function start(cfg) {
  const origins = new Set([...ALLOWED_ORIGINS, ...(cfg.extraOrigins || [])]);
  const server = http.createServer(async (req, res) => {
    const url = (req.url || "").split("?")[0];
    if (req.method === "GET" && url === "/api/teklif/saglik") return send(res, 200, { ok: true });
    if (url !== "/api/teklif") return send(res, 404, { ok: false });
    if (req.method !== "POST") return send(res, 405, { ok: false });

    const origin = req.headers.origin || "";
    if (origin && !origins.has(origin)) return send(res, 403, { ok: false, error: "origin" });

    const ip = String(req.headers["x-forwarded-for"] || req.socket.remoteAddress || "").split(",")[0].trim();
    let raw;
    try {
      const body = await readBody(req, 32 * 1024);
      raw = (req.headers["content-type"] || "").includes("application/json")
        ? JSON.parse(body) : Object.fromEntries(new URLSearchParams(body));
    } catch (e) { return send(res, e.status || 400, { ok: false, error: e.status ? "size" : "body" }); }

    // Bot tuzağı: görünmeyen alan doluysa sessizce başarılı say
    if (raw.website) { log("tuzak alanı dolu, atlandı", ip); return send(res, 200, { ok: true }); }
    if (rateLimited(ip)) { log("hız sınırı", ip); return send(res, 429, { ok: false, error: "rate" }); }

    const v = validate(raw);
    if (v.errors.length) return send(res, 422, { ok: false, error: "fields", fields: v.errors });

    const subject = `Web sitesi teklif talebi — ${v.f.konu || "Genel"} — ${v.f.ad}`;
    try {
      await smtpSend(cfg, { replyTo: v.f.eposta, subject, text: mailText(v, ip) });
      log("gönderildi", ip, v.f.eposta);
      send(res, 200, { ok: true });
    } catch (e) {
      log("SMTP HATASI", e.message);
      send(res, 502, { ok: false, error: "mail" });
    }
  });
  server.listen(cfg.port, "127.0.0.1", () => log(`form alıcı hazır: http://127.0.0.1:${cfg.port}/api/teklif → ${cfg.to}`));
  return server;
}

// ------------------------------------------------------------------ giriş
const cfg = loadConfig();
if (process.argv.includes("--test")) {
  smtpSend(cfg, {
    replyTo: cfg.from,
    subject: "BSM Mekanik web sitesi — form deneme e-postası",
    text: "Bu bir deneme e-postasıdır. Web sitesindeki teklif formu bu adrese e-posta gönderebiliyor.\n\nBSM Mekanik Web Sitesi",
  }).then(() => { log(`deneme e-postası gönderildi → ${cfg.to}`); process.exit(0); })
    .catch((e) => { log("deneme BAŞARISIZ:", e.message); process.exit(1); });
} else {
  start(cfg);
  // Dosya güncellenince (GitHub'dan yeni sürüm gelince) çık; çalıştırıcı yeni sürümle yeniden başlatır
  fs.watchFile(__filename, { interval: 30000 }, () => { log("server.js güncellendi, yeniden başlatılıyor"); process.exit(0); });
}
