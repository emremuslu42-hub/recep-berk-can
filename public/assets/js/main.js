(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.remove("no-js");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Header: kaydırınca beyaz zemine geç
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (header) header.classList.toggle("is-solid", window.scrollY > 40);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Mobil menü
  var toggle = document.querySelector(".menu-toggle");
  function closeMenu() {
    root.classList.remove("menu-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = root.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".mobile-nav a").forEach(function (a) {
      a.addEventListener("click", closeMenu);
    });
    window.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && root.classList.contains("menu-open")) {
        closeMenu();
        toggle.focus();
      }
    });
  }

  // Görünür olunca beliren öğeler
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }

  // Sayaçlar
  var locale = root.lang === "en" ? "en-US" : "tr-TR";
  function runCounter(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (reduceMotion || !target) { el.textContent = target.toLocaleString(locale); return; }
    var start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / 1600, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))).toLocaleString(locale);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { runCounter(entry.target); co.unobserve(entry.target); }
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { co.observe(el); });
  }

  // Yatay proje kaydırıcısı
  document.querySelectorAll("[data-slider]").forEach(function (wrap) {
    var track = wrap.querySelector(".slider");
    var prev = wrap.querySelector("[data-prev]");
    var next = wrap.querySelector("[data-next]");
    function by(dir) {
      var card = track.firstElementChild;
      var w = card ? card.getBoundingClientRect().width + 20 : 300;
      track.scrollBy({ left: dir * w, behavior: reduceMotion ? "auto" : "smooth" });
    }
    if (prev) prev.addEventListener("click", function () { by(-1); });
    if (next) next.addEventListener("click", function () { by(1); });
  });

  // Açılış referans galerisi
  var hero = document.querySelector("[data-hero]");
  if (hero) {
    var slides = hero.querySelectorAll(".rh-slide");
    var infos = hero.querySelectorAll(".rh-info");
    var thumbs = hero.querySelectorAll(".rh-thumb");
    var cur = hero.querySelector("[data-cur]");
    var bar = hero.querySelector(".rh-progress");
    var DUR = 6000;
    var idx = 0, timer = null, paused = false;
    hero.style.setProperty("--rh-dur", DUR + "ms");

    function show(n) {
      idx = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) { s.classList.toggle("is-active", i === idx); });
      infos.forEach(function (s, i) { s.classList.toggle("is-active", i === idx); s.hidden = i !== idx; });
      thumbs.forEach(function (t, i) {
        t.classList.toggle("is-active", i === idx);
        if (i === idx) {
          t.setAttribute("aria-current", "true");
          var strip = t.parentNode;
          if (strip.scrollWidth > strip.clientWidth) strip.scrollTo({ left: t.offsetLeft - strip.offsetLeft - 8, behavior: reduceMotion ? "auto" : "smooth" });
        } else t.removeAttribute("aria-current");
      });
      if (cur) cur.textContent = (idx + 1 < 10 ? "0" : "") + (idx + 1);
      var nextImg = slides[(idx + 1) % slides.length].querySelector("img");
      if (nextImg) nextImg.loading = "eager";
      restart();
    }
    function restart() {
      clearTimeout(timer);
      if (bar) { bar.classList.remove("is-running"); void bar.offsetWidth; }
      if (paused || reduceMotion) return;
      if (bar) bar.classList.add("is-running");
      timer = setTimeout(function () { show(idx + 1); }, DUR);
    }
    hero.querySelector("[data-prev]").addEventListener("click", function () { show(idx - 1); });
    hero.querySelector("[data-next]").addEventListener("click", function () { show(idx + 1); });
    thumbs.forEach(function (t) {
      t.addEventListener("click", function () { show(parseInt(t.getAttribute("data-go"), 10)); });
    });
    var visual = hero.querySelector(".ref-hero-visual");
    visual.addEventListener("mouseenter", function () { paused = true; restart(); });
    visual.addEventListener("mouseleave", function () { paused = false; restart(); });
    hero.addEventListener("focusin", function () { paused = true; restart(); });
    hero.addEventListener("focusout", function () { paused = false; restart(); });
    document.addEventListener("visibilitychange", function () { paused = document.hidden; restart(); });
    var sx = null;
    visual.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    visual.addEventListener("touchend", function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 40) show(idx + (dx < 0 ? 1 : -1));
      sx = null;
    });
    restart();
  }

  // Hizmetler sayfası: alt menüde aktif bölüm
  var navLinks = document.querySelectorAll(".service-nav a");
  if (navLinks.length && "IntersectionObserver" in window) {
    var map = {};
    navLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (a) { a.classList.remove("is-active"); });
        var link = map[entry.target.id];
        if (link) {
          link.classList.add("is-active");
          var bar = link.closest("ul");
          bar.scrollTo({ left: link.offsetLeft - bar.clientWidth / 2 + link.clientWidth / 2, behavior: reduceMotion ? "auto" : "smooth" });
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(map).forEach(function (id) {
      var sec = document.getElementById(id);
      if (sec) so.observe(sec);
    });
  }

  // Referans filtresi
  var filterBar = document.querySelector("[data-filter]");
  if (filterBar) {
    var cards = document.querySelectorAll(".ref-card");
    var empty = document.querySelector(".ref-empty");
    function apply(tag) {
      var shown = 0;
      cards.forEach(function (c) {
        var ok = tag === "all" || (" " + c.getAttribute("data-tags") + " ").indexOf(" " + tag + " ") > -1;
        c.hidden = !ok;
        if (ok) shown++;
      });
      if (empty) empty.hidden = shown > 0;
      filterBar.querySelectorAll("button").forEach(function (b) {
        b.setAttribute("aria-pressed", b.getAttribute("data-tag") === tag ? "true" : "false");
      });
    }
    filterBar.addEventListener("click", function (e) {
      var btn = e.target.closest("button");
      if (!btn) return;
      var tag = btn.getAttribute("data-tag");
      apply(tag);
      history.replaceState(null, "", tag === "all" ? location.pathname : "#" + tag);
    });
    var initial = location.hash.slice(1);
    if (initial && filterBar.querySelector('[data-tag="' + initial + '"]')) apply(initial);
  }

  // Hareket azaltma tercihinde videoları durdur
  if (reduceMotion) {
    document.querySelectorAll("video[autoplay]").forEach(function (v) { v.removeAttribute("autoplay"); v.pause(); });
  }

  // İletişim formu: /api/teklif'e gönderir (sunucudaki form alıcı e-postayla iletir)
  var form = document.querySelector("[data-contact-form]");
  if (form) {
    var L = form.dataset;
    var status = form.querySelector(".form-status");
    var button = form.querySelector("button[type=submit]");
    var buttonHtml = button ? button.innerHTML : "";
    function setStatus(html, ok) {
      if (!status) return;
      status.innerHTML = html;
      status.classList.toggle("is-error", !ok);
    }
    function mailtoFallback(d) {
      var subject = L.subject + " — " + (d.get("konu") || "-");
      var body = [
        L.lName + ": " + d.get("ad"),
        L.lCompany + ": " + (d.get("firma") || "-"),
        L.lEmail + ": " + d.get("eposta"),
        L.lPhone + ": " + (d.get("telefon") || "-"),
        L.lTopic + ": " + (d.get("konu") || "-"),
        "",
        d.get("mesaj")
      ].join("\n");
      return "mailto:" + L.mailto + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    }
    // Form alıcıya ulaşılamazsa mesaj kaybolmasın: e-posta uygulamasını doldurulmuş olarak aç
    function fallback(d) {
      setStatus(L.error, false);
      window.location.href = mailtoFallback(d);
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) { setStatus(L.invalid, false); return; }
      var d = new FormData(form);
      var payload = {
        ad: d.get("ad"), firma: d.get("firma"), eposta: d.get("eposta"), telefon: d.get("telefon"),
        konu: d.get("konu"), mesaj: d.get("mesaj"), kvkk: d.get("kvkk") ? "on" : "",
        website: d.get("website"), lang: L.lang, sayfa: location.pathname
      };
      if (button) { button.disabled = true; button.textContent = L.sending; }
      setStatus("", true);
      fetch(form.getAttribute("action"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }).then(function (r) {
        return r.json().catch(function () { return { ok: false }; }).then(function (j) { return { status: r.status, body: j }; });
      }).then(function (res) {
        if (res.body && res.body.ok) {
          form.reset();
          setStatus(L.success, true);
        } else if (res.status === 429) {
          setStatus(L.rate, false);
        } else if (res.status === 422) {
          setStatus(L.invalid, false);
        } else {
          fallback(d);
        }
      }).catch(function () {
        fallback(d);
      }).then(function () {
        if (button) { button.disabled = false; button.innerHTML = buttonHtml; }
      });
    });
    var pre = new URLSearchParams(location.search).get("hizmet");
    var sel = form.querySelector("select[name=konu]");
    if (pre && sel) {
      Array.prototype.forEach.call(sel.options, function (o) { if (o.dataset.key === pre) sel.value = o.value; });
    }
  }

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
