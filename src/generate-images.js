// Paylaşım görselleri (og-*.jpg) ve uygulama ikonlarını üretir.
// Kullanım: node src/generate-images.js   (Playwright gerektirir)
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const img = (p) => path.join(root, "public/assets/img", p);
const src = fs.readFileSync(path.join(__dirname, "icons.py"), "utf8");
const viewBox = src.match(/LOGO_VIEWBOX = "([^"]+)"/)[1];
const d = src.match(/LOGO_PATH = "([^"]+)"/)[1];
const mark = (color) => `<svg viewBox="${viewBox}" style="width:100%;height:100%"><path fill="${color}" fill-rule="evenodd" d="${d}"/></svg>`;
const font = (f) => "data:font/woff2;base64," + fs.readFileSync(path.join(root, "public/assets/fonts", f)).toString("base64");
const fontCss = `
@font-face{font-family:J;src:url(${font("plus-jakarta-sans-latin-wght-normal.woff2")});font-weight:200 800;unicode-range:U+0000-00FF,U+0131,U+2000-206F}
@font-face{font-family:J;src:url(${font("plus-jakarta-sans-latin-ext-wght-normal.woff2")});font-weight:200 800;unicode-range:U+0100-02BA,U+0130,U+015E-015F,U+011E-011F}
*{margin:0;box-sizing:border-box}body{font-family:J,sans-serif}`;
const bg = "data:image/webp;base64," + fs.readFileSync(img("ref/sisecam-bilim.webp")).toString("base64");

const og = (lang) => {
  const t = lang === "tr"
    ? { h: "Mekanik Tesisat · Yangın · HVAC · Havalandırma", s: "Projelendirmeden anahtar teslime mühendislik ve taahhüt", d: "bsmmekanik.com" }
    : { h: "Mechanical · Fire Protection · HVAC · Ventilation", s: "Engineering and contracting, from design to turnkey delivery", d: "bsmmechanical.com" };
  return `<html><head><style>${fontCss}
  body{width:1200px;height:630px;position:relative;overflow:hidden;background:#0a1630;color:#fff}
  .bg{position:absolute;inset:0;background:url(${bg}) center/cover;opacity:.35}
  .ov{position:absolute;inset:0;background:linear-gradient(90deg,#0a1630 30%,rgba(10,22,48,.55) 100%)}
  .in{position:absolute;inset:0;padding:72px 80px;display:flex;flex-direction:column;justify-content:space-between}
  .logo{display:flex;align-items:center;gap:22px}.logo i{width:84px;height:92px;display:block}
  .logo b{font-size:56px;font-weight:800;letter-spacing:.04em;line-height:1}.logo span{display:block;font-size:17px;letter-spacing:.24em;opacity:.7;margin-top:8px;text-transform:uppercase}
  h1{font-size:52px;font-weight:800;letter-spacing:-.03em;line-height:1.12;max-width:900px}
  p{font-size:26px;opacity:.78;margin-top:18px}
  .f{display:flex;justify-content:space-between;align-items:center;font-size:22px;opacity:.85}
  .bar{position:absolute;left:0;bottom:0;height:10px;width:100%;background:#2a55a6}
  </style></head><body><div class="bg"></div><div class="ov"></div><div class="in">
  <div class="logo"><i>${mark("#ffffff")}</i><div><b>BSM</b><span>${lang === "tr" ? "Mekanik Mühendislik" : "Mechanical Engineering"}</span></div></div>
  <div><h1>${t.h}</h1><p>${t.s}</p></div>
  <div class="f"><span>${t.d}</span><span>+90 (216) 706 14 01</span></div></div><div class="bar"></div></body></html>`;
};
const icon = (size, pad, bgc, fg) => `<html><head><style>*{margin:0}body{width:${size}px;height:${size}px;display:grid;place-items:center;background:${bgc}}
  i{display:block;width:${size - pad * 2}px;height:${size - pad * 2}px}</style></head><body><i>${mark(fg)}</i></body></html>`;

(async () => {
  const b = await chromium.launch();
  const shot = async (html, w, h, out, type) => {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(html, { waitUntil: "networkidle" });
    await p.screenshot({ path: out, type, quality: type === "jpeg" ? 86 : undefined, omitBackground: false });
    await p.close();
    console.log("yazıldı:", path.relative(root, out));
  };
  await shot(og("tr"), 1200, 630, img("og-tr.jpg"), "jpeg");
  await shot(og("en"), 1200, 630, img("og-en.jpg"), "jpeg");
  await shot(icon(180, 30, "#ffffff", "#2a55a6"), 180, 180, img("apple-touch-icon.png"), "png");
  await shot(icon(192, 28, "#ffffff", "#2a55a6"), 192, 192, img("logo-192.png"), "png");
  await shot(icon(512, 70, "#ffffff", "#2a55a6"), 512, 512, img("logo-512.png"), "png");
  await shot(icon(32, 2, "#ffffff", "#2a55a6"), 32, 32, img("favicon-32.png"), "png");
  await b.close();
})();
