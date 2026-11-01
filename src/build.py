#!/usr/bin/env python3
"""BSM Mekanik sitesini üretir: public/ altına TR (kök) ve EN (/en/) sayfaları yazar.

Kullanım:  python3 src/build.py
İçerik metinleri src/content.py içindedir.
"""
import json
import pathlib
import sys
from html import escape
from urllib.parse import quote

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import (CATEGORIES, CLIENT_STRIP, COMPANY, FEATURED, REFERENCES,  # noqa: E402
                     SERVICES, WORK)
from icons import I, LOGO_PATH, LOGO_VIEWBOX  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
C = COMPANY

TOTAL_AREA = sum(r[7] for r in REFERENCES)
AREA_ROUNDED = TOTAL_AREA // 10000 * 10000

# ---------------------------------------------------------------- sayfa adresleri
PAGES = {
    "home": {"tr": "", "en": ""},
    "about": {"tr": "kurumsal", "en": "about"},
    "services": {"tr": "hizmetler", "en": "services"},
    "refs": {"tr": "referanslar", "en": "references"},
    "contact": {"tr": "iletisim", "en": "contact"},
}
FILES = {
    "home": {"tr": "index.html", "en": "en/index.html"},
    "about": {"tr": "kurumsal.html", "en": "en/about.html"},
    "services": {"tr": "hizmetler.html", "en": "en/services.html"},
    "refs": {"tr": "referanslar.html", "en": "en/references.html"},
    "contact": {"tr": "iletisim.html", "en": "en/contact.html"},
}


def url(page, lang, frm):
    """Sayfalar arası göreli bağlantı (uzantısız, Cloudflare temiz URL)."""
    slug = PAGES[page][lang]
    if lang == frm:
        return slug or "./"
    if lang == "en":
        return "en/" + slug if slug else "en/"
    return "../" + slug if slug else "../"


def canonical(page, lang):
    base = C["domain_tr"] if lang == "tr" else C["domain_en"] + "/en"
    slug = PAGES[page][lang]
    return base + "/" + slug if slug else base + "/"


def A(lang):
    return "" if lang == "tr" else "../"


# ---------------------------------------------------------------- arayüz metinleri
UI = {
    "tr": {
        "nav": {"home": "Ana Sayfa", "about": "Kurumsal", "services": "Hizmetler", "refs": "Referanslar", "contact": "İletişim"},
        "skip": "İçeriğe geç",
        "quote": "Teklif Alın",
        "menu": "Menüyü aç",
        "tagline": "Mekanik Mühendislik",
        "footer_about": "Mekanik tesisat, yangın söndürme, HVAC ve havalandırma alanlarında projelendirmeden anahtar teslime mühendislik ve taahhüt hizmetleri.",
        "footer_services": "Hizmetler",
        "footer_company": "Kurumsal",
        "footer_contact": "İletişim",
        "rights": "Tüm hakları saklıdır.",
        "kvkk": "KVKK Aydınlatma Metni",
        "cookies": "Çerez Politikası",
        "detail": "Detaylı bilgi",
        "home_crumb": "Ana Sayfa",
        "cta_title": "Projeniz için doğru mekanik çözümü birlikte belirleyelim.",
        "cta_text": "Projenizin ölçeğini ve ihtiyaçlarını paylaşın; teknik değerlendirme ve teklifimizi en kısa sürede iletelim.",
        "cta_btn": "Teklif İsteyin",
        "cta_call": "Bizi Arayın",
        "wa": "WhatsApp ile yazın",
        "wa_text": "Merhaba, web siteniz üzerinden ulaşıyorum.",
        "m2": "m²",
        "area": "Alan",
        "year": "Yıl",
        "location": "Konum",
        "lang_label": "Dil seçimi",
    },
    "en": {
        "nav": {"home": "Home", "about": "About", "services": "Services", "refs": "References", "contact": "Contact"},
        "skip": "Skip to content",
        "quote": "Get a Quote",
        "menu": "Open menu",
        "tagline": "Mechanical Engineering",
        "footer_about": "Engineering and contracting services from design to turnkey delivery in mechanical installation, fire protection, HVAC and ventilation.",
        "footer_services": "Services",
        "footer_company": "Company",
        "footer_contact": "Contact",
        "rights": "All rights reserved.",
        "kvkk": "Privacy Notice",
        "cookies": "Cookie Policy",
        "detail": "Learn more",
        "home_crumb": "Home",
        "cta_title": "Let's define the right mechanical solution for your project.",
        "cta_text": "Share the scope and needs of your project, and we will send our technical assessment and proposal shortly.",
        "cta_btn": "Request a Quote",
        "cta_call": "Call Us",
        "wa": "Message us on WhatsApp",
        "wa_text": "Hello, I am contacting you via your website.",
        "m2": "m²",
        "area": "Area",
        "year": "Year",
        "location": "Location",
        "lang_label": "Language",
    },
}


def fmt_num(n, lang):
    s = f"{n:,}"
    return s.replace(",", ".") if lang == "tr" else s


def svc(s, lang):
    return s[lang]


# ---------------------------------------------------------------- ortak parçalar
def logo(href, extra=""):
    return (f'<a href="{href}" class="logo{extra}" aria-label="{C["short"]}">'
            f'<svg class="logo-mark" viewBox="{LOGO_VIEWBOX}" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{LOGO_PATH}"/></svg>'
            f'<span class="logo-text"><strong>BSM</strong><span>{{tagline}}</span></span></a>')


def head(lang, page, title, desc, image="assets/img/hero-poster.jpg"):
    a = A(lang)
    alt_tr = canonical(page, "tr")
    alt_en = canonical(page, "en")
    can = canonical(page, lang)
    og_img = C["domain_tr"] + "/" + image
    return f'''<!doctype html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{can}">
<link rel="alternate" hreflang="tr" href="{alt_tr}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{alt_tr}">
<meta name="theme-color" content="#0a1630">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{C["short"]}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{can}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="{"tr_TR" if lang == "tr" else "en_US"}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{a}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{a}assets/css/style.css">
</head>
<body>
<a class="skip-link" href="#icerik">{UI[lang]["skip"]}</a>
'''


def header(lang, page):
    u = UI[lang]
    other = "en" if lang == "tr" else "tr"
    nav = "\n".join(
        f'        <li><a href="{url(p, lang, lang)}"{" aria-current=\"page\"" if p == page else ""}>{u["nav"][p]}</a></li>'
        for p in PAGES)
    mob = "\n".join(
        f'      <li><a class="mobile-link" href="{url(p, lang, lang)}">{u["nav"][p]}<span>0{i + 1}</span></a></li>'
        for i, p in enumerate(PAGES))
    tr_href = url(page, "tr", lang)
    en_href = url(page, "en", lang)
    sw = (f'<div class="lang-switch" role="group" aria-label="{u["lang_label"]}">'
          f'<a href="{tr_href}" hreflang="tr" lang="tr"{" aria-current=\"true\"" if lang == "tr" else ""}>TR</a>'
          f'<a href="{en_href}" hreflang="en" lang="en"{" aria-current=\"true\"" if lang == "en" else ""}>EN</a></div>')
    p0 = C["people"][0]
    return f'''<header class="site-header">
  <div class="container header-inner">
    {logo(url("home", lang, lang)).replace("{tagline}", u["tagline"])}
    <nav class="main-nav" aria-label="{u["nav"]["home"]}">
      <ul>
{nav}
      </ul>
    </nav>
    <div class="header-actions">
      {sw}
      <a class="btn btn--primary" href="{url("contact", lang, lang)}">{u["quote"]}</a>
      <button class="menu-toggle" type="button" aria-label="{u["menu"]}" aria-expanded="false" aria-controls="mobil-menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-nav" id="mobil-menu">
  <nav aria-label="{u["nav"]["home"]}">
    <ul>
{mob}
    </ul>
  </nav>
  <a class="btn btn--primary" href="{url("contact", lang, lang)}">{u["quote"]} {I["arrow"]}</a>
  <div class="mobile-nav-contact">{C["office_phone"]}<br>{p0["email"]}</div>
</div>
'''


def cta(lang):
    u = UI[lang]
    return f'''<section class="cta">
  <div class="container">
    <div class="cta-box reveal">
      <div>
        <h2>{u["cta_title"]}</h2>
        <p>{u["cta_text"]}</p>
      </div>
      <div class="cta-actions">
        <a class="btn btn--white" href="{url("contact", lang, lang)}">{u["cta_btn"]} {I["arrow"]}</a>
        <a class="btn btn--ghost" href="tel:{C["office_tel"]}">{u["cta_call"]}</a>
      </div>
    </div>
  </div>
</section>
'''


def footer(lang):
    u = UI[lang]
    a = A(lang)
    services = "\n".join(
        f'          <li><a href="{url("services", lang, lang)}#{s["key"]}">{s[lang]["name"]}</a></li>' for s in SERVICES)
    company = "\n".join(
        f'          <li><a href="{url(p, lang, lang)}">{u["nav"][p]}</a></li>' for p in ("about", "refs", "contact"))
    people = "\n".join(
        f'          <li>{I["mail"]}<a href="mailto:{p["email"]}">{p["email"]}</a></li>' for p in C["people"])
    wa_url = f'https://wa.me/{C["whatsapp"]}?text={quote(u["wa_text"])}'
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        {logo(url("home", lang, lang)).replace("{tagline}", u["tagline"])}
        <p>{u["footer_about"]}</p>
      </div>
      <div class="footer-col">
        <h4>{u["footer_services"]}</h4>
        <ul>
{services}
        </ul>
      </div>
      <div class="footer-col">
        <h4>{u["footer_company"]}</h4>
        <ul>
{company}
        </ul>
      </div>
      <div class="footer-col footer-contact">
        <h4>{u["footer_contact"]}</h4>
        <ul>
          <li>{I["pin"]}<span>{C["address"]}<br>{C["city"]}</span></li>
          <li>{I["phone"]}<a href="tel:{C["office_tel"]}">{C["office_phone"]}</a></li>
{people}
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> {C["legal"]}. {u["rights"]}</span>
      <nav aria-label="{u["kvkk"]}">
        <a href="{url("contact", lang, lang)}#kvkk">{u["kvkk"]}</a>
      </nav>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa_url}" target="_blank" rel="noopener" aria-label="{u["wa"]}">{I["whatsapp"]}</a>
<script src="{a}assets/js/main.js"></script>
</body>
</html>
'''


def page_hero(lang, title, lead, img, crumb):
    u = UI[lang]
    return f'''<section class="page-hero">
  <div class="page-hero-bg"><img src="{A(lang)}assets/img/{img}" alt="" fetchpriority="high"></div>
  <div class="container">
    <nav class="breadcrumb" aria-label="breadcrumb"><a href="{url("home", lang, lang)}">{u["home_crumb"]}</a><span>/</span><span aria-current="page">{crumb}</span></nav>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
'''


# ---------------------------------------------------------------- referans yardımcıları
def ref_dict(r):
    keys = ["img", "imgtype", "cat", "client", "name_tr", "name_en", "works", "area", "loc", "year_tr", "year_en"]
    d = dict(zip(keys, r))
    tags = []
    for w in d["works"]:
        for t in WORK[w][2]:
            if t not in tags:
                tags.append(t)
    d["tags"] = tags
    return d


REFS = [ref_dict(r) for r in REFERENCES]
REF_BY_IMG = {r["img"]: r for r in REFS}


def ref_name(r, lang):
    return r["name_tr"] if lang == "tr" else r["name_en"]


def ref_card(r, lang, delay):
    u = UI[lang]
    a = A(lang)
    d = f" reveal-delay-{delay}" if delay else ""
    name = ref_name(r, lang)
    year = r["year_tr"] if lang == "tr" else r["year_en"]
    cls = "ref-card-img"
    if r["imgtype"] == "logo":
        cls += " ref-card-img--logo"
    img = f'<img src="{a}assets/img/ref/{r["img"]}.webp" alt="{escape(name)}" loading="lazy">'
    works = "".join(f"<li>{WORK[w][0 if lang == 'tr' else 1]}</li>" for w in r["works"])
    client = f'<span class="ref-card-client">{escape(r["client"])}</span>' if r["client"] else f'<span class="ref-card-client">{CATEGORIES[r["cat"]][0 if lang == "tr" else 1]}</span>'
    return f'''      <article class="ref-card reveal{d}" data-tags="{" ".join(r["tags"])}">
        <div class="{cls}">{img}<span class="ref-card-year">{year}</span></div>
        <div class="ref-card-body">
          {client}
          <h3>{escape(name)}</h3>
          <div class="ref-card-meta"><span>{I["pin_sm"]}{r["loc"]}</span><span>{I["area_sm"]}{fmt_num(r["area"], lang)} {u["m2"]}</span></div>
          <ul class="work">{works}</ul>
        </div>
      </article>
'''


# ---------------------------------------------------------------- ANA SAYFA
HOME = {
    "tr": {
        "title": "BSM Mekanik | Mekanik Tesisat, Yangın, HVAC ve Havalandırma",
        "desc": "BSM Mekanik; mekanik tesisat, yangın söndürme, HVAC, havalandırma, projelendirme ve anahtar teslim taahhüt hizmetleri sunan İstanbul merkezli mühendislik firmasıdır.",
        "eyebrow": "Mekanik Mühendislik · Taahhüt",
        "h1": "Yapıların görünmeyen gücü: <em>mekanik mühendislik.</em>",
        "lead": "Mekanik tesisat, yangın söndürme, HVAC ve havalandırma sistemlerinde projelendirmeden anahtar teslime kadar güvenilir, sürdürülebilir ve uzun ömürlü çözümler.",
        "btn1": "Hizmetlerimiz", "btn2": "Referanslar",
        "facts": [(str(len(REFERENCES)), "Referans proje"), (fmt_num(AREA_ROUNDED, "tr") + "+", "m² uygulama alanı"), ("7", "Uzmanlık alanı"), ("2012’den", "Bugüne proje deneyimi")],
        "marquee": "Proje deneyimimizden",
        "about_eyebrow": "Hakkımızda",
        "about_h": "Projelendirmeden uygulamaya, mühendislik esaslı mekanik çözümler.",
        "about_lead": f"2021 yılında kurulan {C['short']}; mekanik tesisat, mühendislik, projelendirme ve taahhüt alanlarında faaliyet gösteren bir mühendislik firmasıdır.",
        "about_p": "Konut, ticari yapılar, endüstriyel tesisler ve farklı ölçeklerdeki projelere mühendislik çözümleri sunuyor; mekanik taahhüt ve anahtar teslim uygulamalarda kalite, güvenilirlik ve müşteri memnuniyetini ön planda tutuyoruz.",
        "about_list": ["Projelendirme, tedarik, montaj ve devreye alma tek elden", "Ulusal ve uluslararası standartlara uygun uygulama", "İş güvenliği ve zamanında teslim önceliği", "Uzun ömürlü ve sürdürülebilir sistem tasarımı"],
        "badge": "Kuruluş yılı",
        "services_eyebrow": "Hizmetlerimiz",
        "services_h": "Mekanik sistemlerin tamamı, tek mühendislik ekibi.",
        "services_lead": "Yangın güvenliğinden iç hava kalitesine, sıhhi tesisattan otomasyona kadar yapınızın tüm mekanik altyapısını tasarlıyor ve uyguluyoruz.",
        "featured_eyebrow": "Öne Çıkan Projeler",
        "featured_h": "İmza attığımız projelerden seçkiler.",
        "all_refs": "Tüm referanslar",
        "areas_eyebrow": "Uygulama Alanları",
        "areas_h": "Her ölçekte ve her yapı türünde.",
        "areas_lead": "Villalardan 50.000 m² üzeri fabrikalara kadar farklı ölçek ve gereksinimlerdeki projelerde deneyim.",
        "process_eyebrow": "Çalışma Yöntemimiz",
        "process_h": "Şeffaf, planlı ve ölçülebilir bir süreç.",
        "process_lead": "Her projeyi teknik gereklilikler ve güncel mühendislik yaklaşımlarıyla, net bir iş planı üzerinden yürütüyoruz.",
        "process": [
            ("search", "Keşif & Analiz", "Saha incelemesi, ihtiyaç ve kapasite analizi ile doğru sistem seçiminin temelini atıyoruz."),
            ("blueprint", "Projelendirme", "Mekanik projeleri hazırlıyor, disiplinler arası koordinasyonu sağlıyoruz."),
            ("box", "Tedarik", "Projeye ve standartlara uygun, kalitesi kanıtlanmış malzeme ve ekipman temin ediyoruz."),
            ("wrench", "Montaj & Uygulama", "Deneyimli saha ekiplerimizle iş güvenliği kurallarına uygun uygulama yapıyoruz."),
            ("check", "Test & Teslim", "Testler, devreye alma ve dokümantasyon ile sistemi eksiksiz teslim ediyoruz."),
        ],
        "video_eyebrow": "Anahtar Teslim",
        "video_h": "Tek muhatap, eksiksiz mekanik altyapı.",
        "video_lead": "Projelendirme, malzeme temini ve montaj süreçlerini tek elden yöneterek zaman ve maliyet kaybını en aza indiriyoruz.",
        "video_btn": "Taahhüt hizmetlerimiz",
    },
    "en": {
        "title": "BSM Mechanical | Mechanical, Fire Protection, HVAC & Ventilation",
        "desc": "BSM Mechanical is an Istanbul-based engineering firm providing mechanical installation, fire protection, HVAC, ventilation, design and turnkey contracting services.",
        "eyebrow": "Mechanical Engineering · Contracting",
        "h1": "The invisible strength of buildings: <em>mechanical engineering.</em>",
        "lead": "Reliable, sustainable and long-lasting solutions in mechanical installation, fire protection, HVAC and ventilation, from design to turnkey delivery.",
        "btn1": "Our Services", "btn2": "References",
        "facts": [(str(len(REFERENCES)), "Reference projects"), (fmt_num(AREA_ROUNDED, "en") + "+", "m² of applied area"), ("7", "Areas of expertise"), ("Since 2012", "Project experience")],
        "marquee": "From our project experience",
        "about_eyebrow": "About Us",
        "about_h": "Engineering-driven mechanical solutions, from design to delivery.",
        "about_lead": f"Founded in 2021, {C['short']} is an engineering company active in mechanical installation, engineering, design and contracting.",
        "about_p": "We deliver engineering solutions for residential, commercial and industrial projects of every scale, putting quality, reliability and client satisfaction first in contracting and turnkey works.",
        "about_list": ["Design, procurement, installation and commissioning under one roof", "Execution in line with national and international standards", "Priority on occupational safety and on-time delivery", "Durable and sustainable system design"],
        "badge": "Founded",
        "services_eyebrow": "Our Services",
        "services_h": "Every mechanical system, one engineering team.",
        "services_lead": "From fire safety to indoor air quality, from plumbing to automation, we design and build the entire mechanical infrastructure of your building.",
        "featured_eyebrow": "Featured Projects",
        "featured_h": "A selection of projects we have delivered.",
        "all_refs": "All references",
        "areas_eyebrow": "Sectors",
        "areas_h": "At every scale, for every building type.",
        "areas_lead": "Experience across projects of every size, from private villas to factories of over 50,000 m².",
        "process_eyebrow": "How We Work",
        "process_h": "A transparent, planned and measurable process.",
        "process_lead": "We run every project on a clear work plan, guided by technical requirements and current engineering practice.",
        "process": [
            ("search", "Survey & Analysis", "Site survey, demand and capacity analyses lay the foundation for the right system choice."),
            ("blueprint", "Design", "We prepare mechanical designs and coordinate across all disciplines."),
            ("box", "Procurement", "We source proven materials and equipment that meet project specifications and standards."),
            ("wrench", "Installation", "Our experienced site teams carry out the works in full compliance with safety rules."),
            ("check", "Testing & Handover", "Testing, commissioning and documentation for a complete handover."),
        ],
        "video_eyebrow": "Turnkey Delivery",
        "video_h": "One point of contact, complete mechanical infrastructure.",
        "video_lead": "By managing design, procurement and installation in-house, we minimise loss of time and cost.",
        "video_btn": "Our contracting services",
    },
}


def home(lang):
    t = HOME[lang]
    u = UI[lang]
    a = A(lang)
    facts = "".join(f"<div><strong>{v}</strong><span>{k}</span></div>" for v, k in t["facts"])
    strip = "".join(f"<span>{n}</span>" for n in CLIENT_STRIP)
    cards = ""
    for i, s in enumerate(SERVICES):
        x = s[lang]
        cards += f'''      <a class="service-card reveal{" reveal-delay-" + str(i % 3) if i % 3 else ""}" href="{url("services", lang, lang)}#{s["key"]}">
        <div class="service-card-img"><img src="{a}assets/img/hizmet/{s["img"]}.webp" alt="" loading="lazy"></div>
        <div class="service-card-body">
          <span class="service-icon">{I[s["icon"]]}</span>
          <span class="service-card-num">0{i + 1}</span>
          <h3>{x["name"]}</h3>
          <p>{x["short"]}</p>
          <span class="link-arrow">{u["detail"]} {I["arrow"]}</span>
        </div>
      </a>
'''
    feats = ""
    for key in FEATURED:
        r = REF_BY_IMG[key]
        year = r["year_tr"] if lang == "tr" else r["year_en"]
        cat = CATEGORIES[r["cat"]][0 if lang == "tr" else 1]
        sub = r["client"] or r["loc"]
        feats += f'''      <article class="feature-card">
        <img src="{a}assets/img/ref/{r["img"]}.webp" alt="{escape(ref_name(r, lang))}" loading="lazy">
        <span class="feature-card-tag">{cat}</span>
        <div>
          <h3>{escape(ref_name(r, lang))}</h3>
          <p>{escape(sub)}</p>
          <dl><div><dt>{u["area"]}</dt><dd>{fmt_num(r["area"], lang)} {u["m2"]}</dd></div><div><dt>{u["year"]}</dt><dd>{year}</dd></div><div><dt>{u["location"]}</dt><dd>{r["loc"].split(" - ")[0]}</dd></div></dl>
        </div>
      </article>
'''
    area_keys = ["konut", "ticari", "endustri", "egitim", "saglik", "otel"]
    areas = ""
    for k in area_keys:
        n = sum(1 for r in REFS if r["cat"] == k)
        names = [ref_name(r, lang) for r in REFS if r["cat"] == k][:2]
        areas += f'<div class="area reveal">{I[CATEGORIES[k][2]]}<h3>{CATEGORIES[k][0 if lang == "tr" else 1]}</h3><p>{escape(", ".join(names))}</p></div>'
    steps = "".join(
        f'<div class="process-step reveal{" reveal-delay-" + str(i % 4) if i % 4 else ""}"><span class="process-step-num">0{i + 1}</span>{I[ic]}<h3>{h}</h3><p>{p}</p></div>'
        for i, (ic, h, p) in enumerate(t["process"]))
    about_list = "".join(f"<li>{I['check_circle']}{x}</li>" for x in t["about_list"])
    ld = {
        "@context": "https://schema.org",
        "@type": "HVACBusiness",
        "name": C["legal"],
        "alternateName": [C["short"], "BSM Mechanical"],
        "url": C["domain_tr"] + "/",
        "logo": C["domain_tr"] + "/assets/img/logo-mark.svg",
        "image": C["domain_tr"] + "/assets/img/hero-poster.jpg",
        "foundingDate": str(C["founded"]),
        "telephone": C["office_phone"],
        "email": C["people"][0]["email"],
        "address": {"@type": "PostalAddress", "streetAddress": C["address"], "addressLocality": "Maltepe", "addressRegion": "İstanbul", "addressCountry": "TR"},
        "areaServed": "TR",
        "sameAs": [C["domain_en"] + "/"],
    }
    return head(lang, "home", t["title"], t["desc"]) + header(lang, "home") + f'''<main id="icerik">
<section class="hero">
  <div class="hero-media">
    <video autoplay muted loop playsinline preload="auto" poster="{a}assets/img/hero-poster.jpg" aria-hidden="true">
      <source src="{a}assets/video/hero.mp4" type="video/mp4">
    </video>
  </div>
  <div class="container hero-content on-dark">
    <span class="eyebrow">{t["eyebrow"]}</span>
    <h1 class="h-xl">{t["h1"]}</h1>
    <p class="lead">{t["lead"]}</p>
    <div class="hero-actions">
      <a class="btn btn--primary" href="{url("services", lang, lang)}">{t["btn1"]} {I["arrow"]}</a>
      <a class="btn btn--ghost" href="{url("refs", lang, lang)}">{t["btn2"]}</a>
    </div>
    <div class="hero-facts">{facts}</div>
  </div>
</section>

<section class="marquee" aria-label="{t["marquee"]}">
  <p class="marquee-label">{t["marquee"]}</p>
  <div class="marquee-track" aria-hidden="false">{strip}{strip.replace("<span>", '<span aria-hidden="true">')}</div>
</section>

<section class="section">
  <div class="container split">
    <div class="media-stack reveal">
      <img src="{a}assets/img/hizmet/ekip.webp" alt="" loading="lazy">
      <div class="media-badge"><strong>{C["founded"]}</strong><span>{t["badge"]}</span></div>
    </div>
    <div class="reveal reveal-delay-1">
      <span class="eyebrow">{t["about_eyebrow"]}</span>
      <h2 class="h-lg">{t["about_h"]}</h2>
      <p class="lead">{t["about_lead"]}</p>
      <p style="margin-top:16px">{t["about_p"]}</p>
      <ul class="check-list">{about_list}</ul>
      <a class="btn btn--outline" href="{url("about", lang, lang)}">{u["nav"]["about"]} {I["arrow"]}</a>
    </div>
  </div>
</section>

<section class="section section--bg">
  <div class="container">
    <div class="section-head section-head--split">
      <div><span class="eyebrow">{t["services_eyebrow"]}</span><h2 class="h-lg">{t["services_h"]}</h2></div>
      <p class="lead">{t["services_lead"]}</p>
    </div>
    <div class="service-grid">
{cards}    </div>
  </div>
</section>

<section class="section section--dark" data-slider>
  <div class="container">
    <div class="slider-head">
      <div><span class="eyebrow">{t["featured_eyebrow"]}</span><h2 class="h-lg">{t["featured_h"]}</h2></div>
      <div style="display:flex;gap:20px;align-items:center;flex-wrap:wrap">
        <a class="btn btn--ghost" href="{url("refs", lang, lang)}">{t["all_refs"]} {I["arrow"]}</a>
        <div class="slider-nav"><button type="button" data-prev aria-label="‹">{I["arrow"]}</button><button type="button" data-next aria-label="›">{I["arrow"]}</button></div>
      </div>
    </div>
    <div class="slider">
{feats}    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head section-head--split">
      <div><span class="eyebrow">{t["areas_eyebrow"]}</span><h2 class="h-lg">{t["areas_h"]}</h2></div>
      <p class="lead">{t["areas_lead"]}</p>
    </div>
    <div class="area-grid">{areas}</div>
  </div>
</section>

<section class="video-band">
  <video autoplay muted loop playsinline preload="none" poster="{a}assets/img/tesisat-poster.jpg" aria-hidden="true">
    <source src="{a}assets/video/tesisat.mp4" type="video/mp4">
  </video>
  <div class="container on-dark">
    <span class="eyebrow">{t["video_eyebrow"]}</span>
    <h2 class="h-lg">{t["video_h"]}</h2>
    <p class="lead">{t["video_lead"]}</p>
    <a class="btn btn--white" href="{url("services", lang, lang)}#taahhut">{t["video_btn"]} {I["arrow"]}</a>
  </div>
</section>

<section class="section section--dark" style="background:var(--navy-2)">
  <div class="container">
    <div class="section-head section-head--split">
      <div><span class="eyebrow">{t["process_eyebrow"]}</span><h2 class="h-lg">{t["process_h"]}</h2></div>
      <p class="lead">{t["process_lead"]}</p>
    </div>
    <div class="process">{steps}</div>
  </div>
</section>
<div class="section--tight"></div>
</main>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
''' + cta(lang) + footer(lang)


# ---------------------------------------------------------------- KURUMSAL
ABOUT = {
    "tr": {
        "title": "Kurumsal | BSM Mekanik",
        "desc": "BSM Mekanik Mühendislik İnşaat San. ve Tic. Ltd. Şti. hakkında: firma tanıtımı, vizyon, misyon ve değerlerimiz.",
        "h1": "Kalite, güvenilirlik ve teknik uzmanlıkla büyüyen bir mühendislik firması.",
        "lead": "Mekanik tesisat, mühendislik, projelendirme ve taahhüt alanlarında sürdürülebilir ve uzun ömürlü çözümler üretiyoruz.",
        "intro_eyebrow": "Biz Kimiz",
        "intro_h": "BSM Mekanik Mühendislik",
        "paras": [
            f"2021 yılında kurulan {C['legal']}, mekanik tesisat, mühendislik, projelendirme ve taahhüt alanlarında faaliyet gösteren bir mühendislik firmasıdır.",
            "Yangın söndürme sistemleri, HVAC ve iklimlendirme sistemleri, havalandırma, ısıtma, soğutma ve sıhhi tesisat uygulamaları başta olmak üzere geniş bir hizmet yelpazesi sunmaktadır.",
            "Uzmanlık alanlarında edindiği bilgi birikimi ve proje deneyimiyle; konut, ticari yapılar, endüstriyel tesisler ve farklı ölçeklerdeki projelere mühendislik çözümleri sunan BSM Mekanik, mekanik taahhüt ve anahtar teslim proje uygulamalarında kalite, güvenilirlik ve müşteri memnuniyetini ön planda tutmaktadır.",
            "Projelendirmeden uygulamaya kadar tüm süreçlerde teknik gereklilikleri ve güncel mühendislik yaklaşımlarını esas alarak, sürdürülebilir ve uzun ömürlü çözümler üretmeyi hedeflemektedir.",
        ],
        "quote": "Projelendirmeden uygulamaya kadar her aşamada <em>teknik gereklilikleri</em> ve <em>güncel mühendislik yaklaşımlarını</em> esas alıyoruz.",
        "vision": ("Vizyonumuz", [
            "Mekanik tesisat ve mühendislik sektöründe kalite, güvenilirlik ve teknik uzmanlığıyla öne çıkan, ulusal ölçekte tercih edilen ve sektörde kalıcı değer yaratan öncü mühendislik firmalarından biri olmak.",
            "Gelişen teknolojileri ve yenilikçi mühendislik yaklaşımlarını takip ederek hizmet kapasitemizi sürekli geliştirmek, sürdürülebilir projelere imza atmak ve uzun vadeli iş ortaklıkları kurmak hedefimizdir.",
        ]),
        "mission": ("Misyonumuz", [
            "Mühendislik bilgi birikimimizi ve teknik uzmanlığımızı kullanarak müşterilerimize güvenilir, kaliteli ve sürdürülebilir mekanik tesisat çözümleri sunmak.",
            "Üstlendiğimiz her projede iş güvenliği, kalite standartları, zamanında teslimat ve müşteri memnuniyetini ön planda tutarak, ihtiyaçlara uygun ve verimli çözümler geliştirmek temel çalışma prensibimizdir.",
        ]),
        "values_eyebrow": "Değerlerimiz",
        "values_h": "Her projede değişmeyen ilkelerimiz.",
        "values": [
            ("shield", "İş Güvenliği", "Sahadaki her çalışanın ve yapının güvenliği önceliğimizdir."),
            ("award", "Kalite", "Ulusal ve uluslararası standartlara uygun malzeme ve uygulama."),
            ("clock", "Zamanında Teslim", "Planlı iş programı ve şeffaf süreç takibi."),
            ("leaf", "Sürdürülebilirlik", "Enerji verimli, uzun ömürlü ve bakımı kolay sistemler."),
            ("handshake", "Müşteri Memnuniyeti", "Teslimden sonra da süren, uzun vadeli iş ortaklığı."),
        ],
        "numbers_eyebrow": "Rakamlarla",
        "numbers": [(len(REFERENCES), "", "Referans proje"), (AREA_ROUNDED // 1000, "bin", "m² uygulama alanı"), (7, "", "Uzmanlık alanı"), (len({r["loc"].split(" - ")[0] for r in REFS}), "", "Farklı il")],
    },
    "en": {
        "title": "About Us | BSM Mechanical",
        "desc": "About BSM Mekanik Mühendislik İnşaat San. ve Tic. Ltd. Şti.: company profile, vision, mission and values.",
        "h1": "An engineering company growing through quality, reliability and technical expertise.",
        "lead": "We create sustainable, long-lasting solutions in mechanical installation, engineering, design and contracting.",
        "intro_eyebrow": "Who We Are",
        "intro_h": "BSM Mechanical Engineering",
        "paras": [
            f"Founded in 2021, {C['legal']} is an engineering company operating in mechanical installation, engineering, design and contracting.",
            "We offer a broad range of services led by fire protection systems, HVAC and air-conditioning, ventilation, heating, cooling and plumbing.",
            "With the know-how and project experience gained in our fields of expertise, we provide engineering solutions to residential, commercial and industrial projects of various scales, and put quality, reliability and client satisfaction first in contracting and turnkey works.",
            "From design to execution, we base every step on technical requirements and current engineering practice, aiming for sustainable and long-lasting solutions.",
        ],
        "quote": "At every stage from design to execution, we build on <em>technical requirements</em> and <em>current engineering practice</em>.",
        "vision": ("Our Vision", [
            "To be one of the leading engineering companies in mechanical installation, recognised nationwide for quality, reliability and technical expertise, and creating lasting value in the industry.",
            "By following new technologies and innovative engineering approaches, we aim to continuously grow our capacity, deliver sustainable projects and build long-term partnerships.",
        ]),
        "mission": ("Our Mission", [
            "To provide our clients with reliable, high-quality and sustainable mechanical solutions using our engineering knowledge and technical expertise.",
            "Our core principle is to develop efficient solutions tailored to each need, prioritising occupational safety, quality standards, on-time delivery and client satisfaction on every project.",
        ]),
        "values_eyebrow": "Our Values",
        "values_h": "Principles that never change, project after project.",
        "values": [
            ("shield", "Safety", "The safety of every person on site and of every building comes first."),
            ("award", "Quality", "Materials and workmanship in line with national and international standards."),
            ("clock", "On-time Delivery", "A planned work schedule and transparent progress tracking."),
            ("leaf", "Sustainability", "Energy-efficient, durable and easy-to-maintain systems."),
            ("handshake", "Client Satisfaction", "A long-term partnership that continues after handover."),
        ],
        "numbers_eyebrow": "In Numbers",
        "numbers": [(len(REFERENCES), "", "Reference projects"), (AREA_ROUNDED // 1000, "k", "m² of applied area"), (7, "", "Areas of expertise"), (len({r["loc"].split(" - ")[0] for r in REFS}), "", "Provinces")],
    },
}


def about(lang):
    t = ABOUT[lang]
    a = A(lang)
    paras = "".join(f"<p>{p}</p>" for p in t["paras"][1:])
    vis = "".join(f"<p>{p}</p>" for p in t["vision"][1])
    mis = "".join(f"<p>{p}</p>" for p in t["mission"][1])
    values = "".join(
        f'<div class="value reveal{" reveal-delay-" + str(i % 4) if i % 4 else ""}">{I[ic]}<h3>{h}</h3><p>{p}</p></div>'
        for i, (ic, h, p) in enumerate(t["values"]))
    nums = "".join(
        f'<div class="stat reveal"><strong><span data-count="{n}">{n}</span>{f"<sup>{s}</sup>" if s else ""}</strong><span>{lbl}</span></div>'
        for n, s, lbl in t["numbers"])
    return head(lang, "about", t["title"], t["desc"]) + header(lang, "about") + page_hero(lang, t["h1"], t["lead"], "hizmet/saha.webp", UI[lang]["nav"]["about"]) + f'''<main id="icerik">
<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">{t["intro_eyebrow"]}</span>
      <h2 class="h-lg">{t["intro_h"]}</h2>
      <p class="lead">{t["paras"][0]}</p>
      <div style="margin-top:18px">{paras}</div>
    </div>
    <div class="media-stack reveal reveal-delay-1">
      <img src="{a}assets/img/hizmet/projelendirme.webp" alt="" loading="lazy">
      <div class="media-badge"><strong>{C["founded"]}</strong><span>{HOME[lang]["badge"]}</span></div>
    </div>
  </div>
</section>

<section class="section section--bg">
  <div class="container">
    <p class="big-quote reveal" style="margin-bottom:clamp(40px,6vw,64px)">{t["quote"]}</p>
    <div class="mv-grid">
      <div class="mv-card mv-card--brand reveal">{I["eye"]}<h3>{t["vision"][0]}</h3>{vis}</div>
      <div class="mv-card reveal reveal-delay-1">{I["target"]}<h3>{t["mission"][0]}</h3>{mis}</div>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{t["values_eyebrow"]}</span><h2 class="h-lg">{t["values_h"]}</h2></div>
    <div class="values">{values}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{t["numbers_eyebrow"]}</span></div>
    <div class="stats">{nums}</div>
  </div>
</section>
</main>
''' + cta(lang) + footer(lang)


# ---------------------------------------------------------------- HİZMETLER
SERV = {
    "tr": {"title": "Hizmetler | BSM Mekanik", "desc": "Mekanik tesisat, yangın söndürme, HVAC, havalandırma, projelendirme, anahtar teslim taahhüt ile elektrik ve otomasyon hizmetleri.",
           "h1": "Mekanik tesisatın her alanında uçtan uca hizmet.", "lead": "Yedi uzmanlık alanında; projelendirme, tedarik, montaj ve devreye alma süreçlerini tek elden yönetiyoruz.",
           "related": "Bu alandaki projelerimizden", "quote": "Bu hizmet için teklif alın"},
    "en": {"title": "Services | BSM Mechanical", "desc": "Mechanical installation, fire protection, HVAC, ventilation, engineering & design, turnkey contracting, electrical and automation services.",
           "h1": "End-to-end services across every area of mechanical installation.", "lead": "Across seven areas of expertise, we manage design, procurement, installation and commissioning under one roof.",
           "related": "Selected projects in this field", "quote": "Request a quote for this service"},
}


def services(lang):
    t = SERV[lang]
    a = A(lang)
    nav = "\n".join(f'      <li><a href="#{s["key"]}">{s[lang]["name"]}</a></li>' for s in SERVICES)
    blocks = ""
    for i, s in enumerate(SERVICES):
        x = s[lang]
        items = "".join(f"<li>{I['check_sm']}{it}</li>" for it in x["items"])
        rel = [ref_name(r, lang) for r in REFS if s["key"] in r["tags"]][:6]
        rel_html = f'<div class="related"><strong>{t["related"]}</strong><ul class="chip-list">{"".join(f"<li>{escape(n)}</li>" for n in rel)}</ul></div>' if rel else ""
        blocks += f'''  <article class="service-detail" id="{s["key"]}">
    <div class="service-detail-media reveal"><img src="{a}assets/img/hizmet/{s["img"]}.webp" alt="{x["name"]}" loading="lazy"><span class="service-icon">{I[s["icon"]]}</span></div>
    <div class="reveal reveal-delay-1">
      <span class="service-detail-num">0{i + 1} / 0{len(SERVICES)}</span>
      <h2>{x["name"]}</h2>
      <p class="lead">{x["intro"]}</p>
      <ul class="bullet-grid">{items}</ul>
      {rel_html}
      <p style="margin-top:28px"><a class="btn btn--primary" href="{url("contact", lang, lang)}?hizmet={s["key"]}">{t["quote"]} {I["arrow"]}</a></p>
    </div>
  </article>
'''
    return head(lang, "services", t["title"], t["desc"]) + header(lang, "services") + page_hero(lang, t["h1"], t["lead"], "hizmet/sprinkler-tavan.webp", UI[lang]["nav"]["services"]) + f'''<main id="icerik">
<nav class="service-nav" aria-label="{UI[lang]["nav"]["services"]}">
  <div class="container">
    <ul>
{nav}
    </ul>
  </div>
</nav>
<div class="container">
{blocks}</div>
</main>
''' + cta(lang) + footer(lang)


# ---------------------------------------------------------------- REFERANSLAR
REFP = {
    "tr": {"title": "Referanslar | BSM Mekanik", "desc": "2012'den bugüne BSM Mekanik referans projeleri: eğitim, endüstri, konut, otel, ofis ve ticari yapılarda mekanik tesisat uygulamaları.",
           "h1": "Güvenle tamamlanan projeler.", "lead": f"2012’den bugüne {len(REFERENCES)} proje ve {fmt_num(TOTAL_AREA, 'tr')} m² uygulama alanı.",
           "all": "Tümü", "empty": "Bu kategoride proje bulunamadı.",
           "credit": "Robert Koleji fotoğrafı: Yaguzi; Özyeğin Üniversitesi fotoğrafı: Bo yaser — Wikimedia Commons, CC BY-SA 4.0."},
    "en": {"title": "References | BSM Mechanical", "desc": "BSM Mechanical reference projects since 2012: mechanical installations in education, industrial, residential, hotel, office and retail buildings.",
           "h1": "Projects delivered with confidence.", "lead": f"{len(REFERENCES)} projects and {fmt_num(TOTAL_AREA, 'en')} m² of applied area since 2012.",
           "all": "All", "empty": "No projects found in this category.",
           "credit": "Robert College photo: Yaguzi; Özyeğin University photo: Bo yaser — Wikimedia Commons, CC BY-SA 4.0."},
}


def refs(lang):
    t = REFP[lang]
    btns = f'<button type="button" data-tag="all" aria-pressed="true">{t["all"]}<span>{len(REFS)}</span></button>'
    for s in SERVICES:
        n = sum(1 for r in REFS if s["key"] in r["tags"])
        if n:
            btns += f'<button type="button" data-tag="{s["key"]}" aria-pressed="false">{s[lang]["name"]}<span>{n}</span></button>'
    cards = "".join(ref_card(r, lang, i % 3) for i, r in enumerate(REFS))
    return head(lang, "refs", t["title"], t["desc"]) + header(lang, "refs") + page_hero(lang, t["h1"], t["lead"], "ref/sisecam-bilim.webp", UI[lang]["nav"]["refs"]) + f'''<main id="icerik">
<section class="section">
  <div class="container">
    <div class="filter-bar" data-filter role="group">{btns}</div>
    <div class="ref-grid">
{cards}    </div>
    <p class="ref-empty" hidden>{t["empty"]}</p>
    <p class="text-muted" style="margin-top:48px;font-size:12.5px">{t["credit"]}</p>
  </div>
</section>
</main>
''' + cta(lang) + footer(lang)


# ---------------------------------------------------------------- İLETİŞİM
CONT = {
    "tr": {"title": "İletişim | BSM Mekanik", "desc": "BSM Mekanik iletişim bilgileri: Altıntepe Mah. İstasyon Yolu Sok. No:3/1 Maltepe/İstanbul · +90 (216) 706 14 01",
           "h1": "Projenizi konuşalım.", "lead": "Teklif, keşif veya teknik danışmanlık talepleriniz için bize ulaşın; en kısa sürede dönüş yapalım.",
           "office": "Merkez Ofis", "phone": "Telefon", "email": "E-posta", "mobile": "Cep",
           "form_eyebrow": "Teklif Formu", "form_h": "Bize yazın",
           "f": {"name": "Ad Soyad", "company": "Firma", "email": "E-posta", "phone": "Telefon", "topic": "Hizmet", "msg": "Mesajınız",
                 "msg_ph": "Proje türü, alan (m²), konum ve talep ettiğiniz hizmetleri yazmanız değerlendirmemizi hızlandırır.",
                 "choose": "Seçiniz", "other": "Diğer", "consent": "Kişisel verilerimin talebime dönüş yapılması amacıyla işlenmesini kabul ediyorum.",
                 "send": "Gönder", "subject": "Web sitesi talebi", "success": "Teşekkürler! E-posta uygulamanız açılıyor; mesajınızı göndermeniz yeterli."},
           "map": "Konum", "directions": "Yol tarifi al",
           "kvkk_h": "KVKK Aydınlatma Metni",
           "kvkk": f"İletişim formu ve e-posta yoluyla ilettiğiniz ad, firma, e-posta, telefon ve mesaj bilgileriniz; yalnızca talebinize dönüş yapmak amacıyla veri sorumlusu {C['legal']} tarafından 6698 sayılı KVKK kapsamında işlenir ve üçüncü kişilerle paylaşılmaz. KVKK’nın 11. maddesindeki haklarınız için {C['people'][0]['email']} adresine başvurabilirsiniz."},
    "en": {"title": "Contact | BSM Mechanical", "desc": "Contact BSM Mechanical: Altıntepe Mah. İstasyon Yolu Sok. No:3/1 Maltepe, Istanbul · +90 (216) 706 14 01",
           "h1": "Let's talk about your project.", "lead": "Reach out for quotes, site surveys or technical consultancy, and we will get back to you shortly.",
           "office": "Head Office", "phone": "Phone", "email": "Email", "mobile": "Mobile",
           "form_eyebrow": "Quote Form", "form_h": "Write to us",
           "f": {"name": "Full name", "company": "Company", "email": "Email", "phone": "Phone", "topic": "Service", "msg": "Message",
                 "msg_ph": "Project type, area (m²), location and the services you need help us respond faster.",
                 "choose": "Select", "other": "Other", "consent": "I consent to my personal data being processed in order to respond to my request.",
                 "send": "Send", "subject": "Website enquiry", "success": "Thank you! Your email app is opening; just press send."},
           "map": "Location", "directions": "Get directions",
           "kvkk_h": "Privacy Notice",
           "kvkk": f"The name, company, email, phone and message details you send via the contact form or email are processed by the data controller {C['legal']} solely to respond to your request, under Turkish Personal Data Protection Law No. 6698, and are not shared with third parties. To exercise your rights, contact {C['people'][0]['email']}."},
}


def contact(lang):
    t = CONT[lang]
    f = t["f"]
    mailto = ",".join(p["email"] for p in C["people"])
    opts = "".join(f'<option data-key="{s["key"]}" value="{s[lang]["name"]}">{s[lang]["name"]}</option>' for s in SERVICES)
    people = "".join(
        f'<span class="label">{p["name"]}</span><a href="tel:{p["tel"]}">{p["phone"]}</a><a href="mailto:{p["email"]}">{p["email"]}</a>'
        for p in C["people"])
    mq = quote(C["map_query"])
    return head(lang, "contact", t["title"], t["desc"]) + header(lang, "contact") + page_hero(lang, t["h1"], t["lead"], "hizmet/vrf-yangin.webp", UI[lang]["nav"]["contact"]) + f'''<main id="icerik">
<section class="section">
  <div class="container">
    <div class="contact-cards">
      <div class="contact-card reveal">{I["building"]}<h3>{t["office"]}</h3><p>{C["address"]}<br>{C["city"]}</p><a class="link-arrow" style="margin-top:10px" href="https://www.google.com/maps/search/?api=1&query={mq}" target="_blank" rel="noopener">{t["directions"]} {I["arrow"]}</a></div>
      <div class="contact-card reveal reveal-delay-1">{I["phone_lg"]}<h3>{t["phone"]}</h3><span class="label">{t["office"]}</span><a href="tel:{C["office_tel"]}">{C["office_phone"]}</a>{"".join(f'<span class="label">{p["name"]} · {t["mobile"]}</span><a href="tel:{p["tel"]}">{p["phone"]}</a>' for p in C["people"])}</div>
      <div class="contact-card reveal reveal-delay-2">{I["mail_lg"]}<h3>{t["email"]}</h3>{"".join(f'<span class="label">{p["name"]}</span><a href="mailto:{p["email"]}">{p["email"]}</a>' for p in C["people"])}</div>
    </div>
    <div class="contact-grid">
      <form class="form reveal" data-contact-form novalidate data-mailto="{mailto}" data-subject="{f["subject"]}" data-success="{f["success"]}"
            data-l-name="{f["name"]}" data-l-company="{f["company"]}" data-l-email="{f["email"]}" data-l-phone="{f["phone"]}" data-l-topic="{f["topic"]}">
        <div><span class="eyebrow">{t["form_eyebrow"]}</span><h2 class="h-md">{t["form_h"]}</h2></div>
        <div class="form-row">
          <div class="field"><label for="ad">{f["name"]} *</label><input id="ad" name="ad" type="text" autocomplete="name" required></div>
          <div class="field"><label for="firma">{f["company"]}</label><input id="firma" name="firma" type="text" autocomplete="organization"></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="eposta">{f["email"]} *</label><input id="eposta" name="eposta" type="email" autocomplete="email" required></div>
          <div class="field"><label for="telefon">{f["phone"]}</label><input id="telefon" name="telefon" type="tel" autocomplete="tel"></div>
        </div>
        <div class="field"><label for="konu">{f["topic"]}</label><select id="konu" name="konu"><option value="">{f["choose"]}</option>{opts}<option value="{f["other"]}">{f["other"]}</option></select></div>
        <div class="field"><label for="mesaj">{f["msg"]} *</label><textarea id="mesaj" name="mesaj" placeholder="{f["msg_ph"]}" required></textarea></div>
        <label class="form-consent"><input type="checkbox" name="kvkk" required><span>{f["consent"]} *</span></label>
        <div><button class="btn btn--primary" type="submit">{f["send"]} {I["arrow"]}</button></div>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
      <div class="map-box reveal reveal-delay-1">
        <iframe title="{t["map"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={mq}&amp;z=16&amp;hl={lang}&amp;output=embed"></iframe>
      </div>
    </div>
  </div>
</section>
<section class="section--tight section--bg" id="kvkk">
  <div class="container">
    <h2 class="h-md" style="margin-bottom:14px">{t["kvkk_h"]}</h2>
    <p class="text-muted" style="max-width:90ch">{t["kvkk"]}</p>
  </div>
</section>
</main>
''' + footer(lang)


# ---------------------------------------------------------------- 404
def notfound():
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sayfa bulunamadı | BSM Mekanik</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
<main class="notfound">
  <div>
    <svg viewBox="{LOGO_VIEWBOX}" style="width:64px;margin:0 auto 28px;color:#a9c0ea" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{LOGO_PATH}"/></svg>
    <strong>404</strong>
    <h1>Aradığınız sayfa bulunamadı.</h1>
    <p>The page you are looking for could not be found.</p>
    <a class="btn btn--white" href="/">Ana Sayfa / Home {I["arrow"]}</a>
  </div>
</main>
</body>
</html>
'''


# ---------------------------------------------------------------- sitemap / robots
def sitemap():
    rows = []
    for p in PAGES:
        for lang in ("tr", "en"):
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{canonical(p, l)}"/>' for l in ("tr", "en"))
            rows.append(f"  <url><loc>{canonical(p, lang)}</loc>{alts}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def main():
    builders = {"home": home, "about": about, "services": services, "refs": refs, "contact": contact}
    (PUBLIC / "en").mkdir(parents=True, exist_ok=True)
    for page, fn in builders.items():
        for lang in ("tr", "en"):
            out = PUBLIC / FILES[page][lang]
            out.write_text(fn(lang), encoding="utf-8")
            print("yazıldı:", out.relative_to(ROOT))
    (PUBLIC / "404.html").write_text(notfound(), encoding="utf-8")
    (PUBLIC / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (PUBLIC / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {C['domain_tr']}/sitemap.xml\n", encoding="utf-8")
    print(f"Toplam referans alanı: {TOTAL_AREA} m²")


if __name__ == "__main__":
    main()
