#!/usr/bin/env python3
"""BSM Mekanik sitesini üretir: public/ altına TR (kök) ve EN (/en/) sayfaları yazar.

Kullanım:  python3 src/build.py      (Python 3.8+, Pillow)
İçerik metinleri src/content.py içindedir.
"""
import datetime
import json
import re
import pathlib
import sys
from html import escape
from urllib.parse import quote

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import (CATEGORIES, CLIENT_STRIP, COMPANY, FEATURED, HOME_REFS,  # noqa: E402
                     REFERENCES, SERVICES, WORK)
from icons import I, LOGO_PATH, LOGO_VIEWBOX  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
C = COMPANY
TODAY = datetime.date.today().isoformat()
LANGS = ("tr", "en")
ORG_ID = C["domain_tr"] + "/#organizasyon"

CUR_PAGE = ' aria-current="page"'
CUR_TRUE = ' aria-current="true"'

TOTAL_AREA = sum(r[7] for r in REFERENCES)
AREA_ROUNDED = TOTAL_AREA // 10000 * 10000

# ---------------------------------------------------------------- adresler
SLUG = {
    "home": {"tr": "/", "en": "/en/"},
    "about": {"tr": "/kurumsal", "en": "/en/about"},
    "services": {"tr": "/hizmetler", "en": "/en/services"},
    "refs": {"tr": "/referanslar", "en": "/en/projects"},
    "contact": {"tr": "/iletisim", "en": "/en/contact"},
}
NAV = ["home", "about", "services", "refs", "contact"]


def path(page, lang, svc=None):
    if svc:
        return SLUG["services"][lang] + "/" + svc["slug"][lang]
    return SLUG[page][lang]


def absolute(p, lang):
    return (C["domain_tr"] if lang == "tr" else C["domain_en"]) + p


def out_file(p):
    if p.endswith("/"):
        return PUBLIC / p.lstrip("/") / "index.html"
    return PUBLIC / (p.lstrip("/") + ".html")


# ---------------------------------------------------------------- görseller
_dims = {}


def img(src, alt="", cls="", lazy=True, sizes="100vw", priority=False):
    """width/height ve gerekiyorsa küçük sürüm (srcset) ile <img> üretir."""
    f = PUBLIC / src.lstrip("/")
    if src not in _dims:
        with Image.open(f) as im:
            _dims[src] = im.size
    w, h = _dims[src]
    srcset = ""
    if w >= 1000 and f.suffix == ".webp":
        small = f.with_name(f.stem + "-640" + f.suffix)
        if not small.exists() or small.stat().st_mtime < f.stat().st_mtime:
            with Image.open(f) as im:
                im.thumbnail((640, 640 * h // w))
                im.save(small, "WEBP", quality=74)
        ssrc = src.rsplit("/", 1)[0] + "/" + small.name
        srcset = f' srcset="{ssrc} 640w, {src} {w}w" sizes="{sizes}"'
    attrs = f' class="{cls}"' if cls else ""
    attrs += ' loading="lazy" decoding="async"' if lazy else ""
    attrs += ' fetchpriority="high"' if priority else ""
    return f'<img src="{src}"{srcset} width="{w}" height="{h}" alt="{escape(alt)}"{attrs}>'


def thumb(src, width=240):
    """Küçük önizleme görseli (ör. galeri küçük resimleri)."""
    f = PUBLIC / src.lstrip("/")
    t = f.with_name(f.stem + "-t" + f.suffix)
    if not t.exists() or t.stat().st_mtime < f.stat().st_mtime:
        with Image.open(f) as im:
            im.thumbnail((width, width))
            im.save(t, "WEBP", quality=72)
    with Image.open(t) as im:
        w, h = im.size
    return f'<img src="{src.rsplit("/", 1)[0]}/{t.name}" width="{w}" height="{h}" alt="" decoding="async">'


# ---------------------------------------------------------------- arayüz metinleri
UI = {
    "tr": {
        "nav": {"home": "Ana Sayfa", "about": "Kurumsal", "services": "Hizmetler", "refs": "Referanslar", "contact": "İletişim"},
        "main_menu": "Ana menü", "skip": "İçeriğe geç", "quote": "Teklif Alın", "menu": "Menüyü aç / kapat",
        "tagline": "Mekanik Mühendislik",
        "footer_about": "Mekanik tesisat, yangın söndürme, HVAC ve havalandırma alanlarında projelendirmeden anahtar teslime mühendislik ve taahhüt hizmetleri.",
        "footer_services": "Hizmetler", "footer_company": "Kurumsal", "footer_contact": "İletişim",
        "rights": "Tüm hakları saklıdır.", "kvkk": "KVKK Aydınlatma Metni",
        "detail": "Detaylı bilgi", "breadcrumb": "Sayfa konumu",
        "cta_title": "Projeniz için doğru mekanik çözümü birlikte belirleyelim.",
        "cta_text": "Projenizin ölçeğini ve ihtiyaçlarını paylaşın; teknik değerlendirme ve teklifimizi en kısa sürede iletelim.",
        "cta_btn": "Teklif İsteyin", "cta_call": "Bizi Arayın",
        "wa": "WhatsApp ile yazın", "wa_text": "Merhaba, web siteniz üzerinden ulaşıyorum.",
        "m2": "m²", "area": "Alan", "year": "Yıl", "location": "Konum", "client": "İşveren",
        "lang_label": "Dil seçimi", "prev": "Önceki proje", "next": "Sonraki proje", "goto": "Projeye git",
        "og_alt": "BSM Mekanik — Mekanik tesisat, yangın, HVAC ve havalandırma",
    },
    "en": {
        "nav": {"home": "Home", "about": "About", "services": "Services", "refs": "Projects", "contact": "Contact"},
        "main_menu": "Main menu", "skip": "Skip to content", "quote": "Get a Quote", "menu": "Toggle menu",
        "tagline": "Mechanical Engineering",
        "footer_about": "Engineering and contracting for mechanical installations, fire protection, HVAC and ventilation, from design through to turnkey delivery.",
        "footer_services": "Services", "footer_company": "Company", "footer_contact": "Contact",
        "rights": "All rights reserved.", "kvkk": "Privacy Notice",
        "detail": "Learn more", "breadcrumb": "Breadcrumb",
        "cta_title": "Let's find the right mechanical solution for your project",
        "cta_text": "Tell us about the scope and requirements of your project, and we'll come back to you promptly with a technical assessment and proposal.",
        "cta_btn": "Request a Quote", "cta_call": "Call Us",
        "wa": "Message us on WhatsApp", "wa_text": "Hello, I am contacting you via your website.",
        "m2": "m²", "area": "Area", "year": "Year", "location": "Location", "client": "Client",
        "lang_label": "Language", "prev": "Previous project", "next": "Next project", "goto": "Go to project",
        "og_alt": "BSM Mechanical — mechanical, fire protection, HVAC and ventilation contractor",
    },
}


def fmt_num(n, lang):
    s = f"{n:,}"
    return s.replace(",", ".") if lang == "tr" else s


# ---------------------------------------------------------------- referans verisi
def ref_dict(r):
    keys = ["img", "imgtype", "cat", "client", "name_tr", "name_en", "works", "area", "loc", "year_tr", "year_en"]
    d = dict(zip(keys, r))
    tags = []
    for w in d["works"]:
        for t in WORK[w][2]:
            if t not in tags:
                tags.append(t)
    d["tags"] = tags
    d["src"] = f"/assets/img/ref/{d['img']}.webp"
    return d


REFS = [ref_dict(r) for r in REFERENCES]
REF_BY = {r["img"]: r for r in REFS}


def rname(r, lang):
    return r["name_tr"] if lang == "tr" else r["name_en"]


def ryear(r, lang):
    return r["year_tr"] if lang == "tr" else r["year_en"]


def rcat(r, lang):
    return CATEGORIES[r["cat"]][0 if lang == "tr" else 1]


def work(w, lang):
    return WORK[w][0 if lang == "tr" else 1]


# ---------------------------------------------------------------- yapısal veri
def org_schema():
    return {
        "@type": "HVACBusiness",
        "@id": ORG_ID,
        "name": C["legal"],
        "alternateName": [C["short"], "BSM Mechanical"],
        "url": C["domain_tr"] + "/",
        "logo": C["domain_tr"] + "/assets/img/logo-512.png",
        "image": C["domain_tr"] + "/assets/img/og-tr.jpg",
        "description": "Mekanik tesisat, yangın söndürme sistemleri, HVAC, havalandırma, mühendislik ve anahtar teslim taahhüt hizmetleri.",
        "foundingDate": str(C["founded"]),
        "telephone": C["office_tel"],
        "email": C["people"][0]["email"],
        "address": {"@type": "PostalAddress", "streetAddress": C["address"], "addressLocality": "Maltepe",
                    "addressRegion": "İstanbul", "addressCountry": "TR"},
        "areaServed": {"@type": "Country", "name": "Türkiye"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": p["tel"], "email": p["email"], "contactType": "sales",
                          "name": p["name"], "availableLanguage": ["Turkish", "English"]} for p in C["people"]],
        "knowsAbout": [s["tr"]["name"] for s in SERVICES],
        "sameAs": [C["domain_en"] + "/"],
    }


def breadcrumb_schema(items, lang):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": absolute(p, lang)} for i, (n, p) in enumerate(items)]}


def ld(*objs):
    graph = {"@context": "https://schema.org", "@graph": list(objs)}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>\n'


# ---------------------------------------------------------------- ortak parçalar
def logo(lang):
    return (f'<a href="{path("home", lang)}" class="logo" aria-label="{C["short"]} — {UI[lang]["nav"]["home"]}">'
            f'<svg class="logo-mark" viewBox="{LOGO_VIEWBOX}" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{LOGO_PATH}"/></svg>'
            f'<span class="logo-text"><strong>BSM</strong><span>{UI[lang]["tagline"]}</span></span></a>')


def head(lang, title, desc, paths, schema="", preload=""):
    """paths: {"tr": "/...", "en": "/en/..."} — canonical ve hreflang için."""
    can = absolute(paths[lang], lang)
    og_img = absolute(f"/assets/img/og-{lang}.jpg", lang)
    other = "en" if lang == "tr" else "tr"
    return f'''<!doctype html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{can}">
<link rel="alternate" hreflang="tr" href="{absolute(paths["tr"], "tr")}">
<link rel="alternate" hreflang="en" href="{absolute(paths["en"], "en")}">
<link rel="alternate" hreflang="x-default" href="{absolute(paths["tr"], "tr")}">
<meta name="theme-color" content="#0a1630">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{C["short"]}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{can}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{UI[lang]["og_alt"]}">
<meta property="og:locale" content="{"tr_TR" if lang == "tr" else "en_US"}">
<meta property="og:locale:alternate" content="{"en_US" if lang == "tr" else "tr_TR"}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/plus-jakarta-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/plus-jakarta-sans-latin-ext-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="/assets/css/style.css">
{schema}</head>
<body>
<a class="skip-link" href="#icerik">{UI[lang]["skip"]}</a>
'''


def header(lang, page, paths):
    u = UI[lang]
    nav = "\n".join(
        f'        <li><a href="{path(p, lang)}"{CUR_PAGE if p == page else ""}>{u["nav"][p]}</a></li>' for p in NAV)
    mob = "\n".join(
        f'      <li><a class="mobile-link" href="{path(p, lang)}"{CUR_PAGE if p == page else ""}>{u["nav"][p]}<span>0{i + 1}</span></a></li>'
        for i, p in enumerate(NAV))
    sw = (f'<div class="lang-switch" role="group" aria-label="{u["lang_label"]}">'
          f'<a href="{paths["tr"]}" hreflang="tr" lang="tr"{CUR_TRUE if lang == "tr" else ""}>TR</a>'
          f'<a href="{paths["en"]}" hreflang="en" lang="en"{CUR_TRUE if lang == "en" else ""}>EN</a></div>')
    return f'''<header class="site-header">
  <div class="container header-inner">
    {logo(lang)}
    <nav class="main-nav" aria-label="{u["main_menu"]}">
      <ul>
{nav}
      </ul>
    </nav>
    <div class="header-actions">
      {sw}
      <a class="btn btn--primary" href="{path("contact", lang)}">{u["quote"]}</a>
      <button class="menu-toggle" type="button" aria-label="{u["menu"]}" aria-expanded="false" aria-controls="mobil-menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-nav" id="mobil-menu">
  <nav aria-label="{u["main_menu"]}">
    <ul>
{mob}
    </ul>
  </nav>
  <a class="btn btn--primary" href="{path("contact", lang)}">{u["quote"]} {I["arrow"]}</a>
  <div class="mobile-nav-contact"><a href="tel:{C["office_tel"]}">{C["office_phone"]}</a><br><a href="mailto:{C["people"][0]["email"]}">{C["people"][0]["email"]}</a></div>
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
        <a class="btn btn--white" href="{path("contact", lang)}">{u["cta_btn"]} {I["arrow"]}</a>
        <a class="btn btn--ghost" href="tel:{C["office_tel"]}">{u["cta_call"]}</a>
      </div>
    </div>
  </div>
</section>
'''


def footer(lang):
    u = UI[lang]
    services = "\n".join(f'          <li><a href="{path(None, lang, s)}">{s[lang]["name"]}</a></li>' for s in SERVICES)
    company = "\n".join(f'          <li><a href="{path(p, lang)}">{u["nav"][p]}</a></li>' for p in ("about", "services", "refs", "contact"))
    people = "\n".join(f'          <li>{I["mail"]}<a href="mailto:{p["email"]}">{p["email"]}</a></li>' for p in C["people"])
    wa_url = f'https://wa.me/{C["whatsapp"]}?text={quote(u["wa_text"])}'
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        {logo(lang)}
        <p>{u["footer_about"]}</p>
      </div>
      <nav class="footer-col" aria-label="{u["footer_services"]}">
        <h2 class="footer-title">{u["footer_services"]}</h2>
        <ul>
{services}
        </ul>
      </nav>
      <nav class="footer-col" aria-label="{u["footer_company"]}">
        <h2 class="footer-title">{u["footer_company"]}</h2>
        <ul>
{company}
        </ul>
      </nav>
      <div class="footer-col footer-contact">
        <h2 class="footer-title">{u["footer_contact"]}</h2>
        <address>
        <ul>
          <li>{I["pin"]}<span>{C["address"]}<br>{C["city"]}</span></li>
          <li>{I["phone"]}<a href="tel:{C["office_tel"]}">{C["office_phone"]}</a></li>
{people}
        </ul>
        </address>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>{datetime.date.today().year}</span> {C["legal"]}. {u["rights"]}</span>
      <a href="{path("contact", lang)}#kvkk">{u["kvkk"]}</a>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa_url}" target="_blank" rel="noopener" aria-label="{u["wa"]}">{I["whatsapp"]}</a>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''


def page_hero(lang, title, lead, src, crumbs):
    """crumbs: [(ad, yol), ...] — son öğe mevcut sayfa."""
    trail = ""
    for i, (n, p) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            trail += f'<span aria-current="page">{n}</span>'
        else:
            trail += f'<a href="{p}">{n}</a><span aria-hidden="true">/</span>'
    return f'''<section class="page-hero">
  <div class="page-hero-bg">{img(src, "", lazy=False, priority=True)}</div>
  <div class="container">
    <nav class="breadcrumb" aria-label="{UI[lang]["breadcrumb"]}">{trail}</nav>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
'''


def ref_card(r, lang, delay=0, heading="h3"):
    u = UI[lang]
    d = f" reveal-delay-{delay}" if delay else ""
    cls = "ref-card-img ref-card-img--logo" if r["imgtype"] == "logo" else "ref-card-img"
    works = "".join(f"<li>{work(w, lang)}</li>" for w in r["works"])
    label = escape(r["client"]) if r["client"] else rcat(r, lang)
    return f'''      <article class="ref-card reveal{d}" data-tags="{" ".join(r["tags"])}">
        <div class="{cls}">{img(r["src"], rname(r, lang), sizes="(min-width: 1080px) 380px, (min-width: 680px) 50vw, 100vw")}<span class="ref-card-year">{ryear(r, lang)}</span></div>
        <div class="ref-card-body">
          <span class="ref-card-client">{label}</span>
          <{heading}>{escape(rname(r, lang))}</{heading}>
          <div class="ref-card-meta"><span>{I["pin_sm"]}{r["loc"]}</span><span>{I["area_sm"]}{fmt_num(r["area"], lang)} {u["m2"]}</span></div>
          <ul class="work">{works}</ul>
        </div>
      </article>
'''


def service_card(s, lang, i):
    x = s[lang]
    d = f" reveal-delay-{i % 3}" if i % 3 else ""
    return f'''      <a class="service-card reveal{d}" href="{path(None, lang, s)}">
        <div class="service-card-img">{img("/assets/img/hizmet/" + s["img"] + ".webp", "", sizes="(min-width: 1080px) 400px, (min-width: 680px) 50vw, 100vw")}</div>
        <div class="service-card-body">
          <span class="service-icon">{I[s["icon"]]}</span>
          <span class="service-card-num">0{i + 1}</span>
          <h3>{x["name"]}</h3>
          <p>{x["short"]}</p>
          <span class="link-arrow">{UI[lang]["detail"]} {I["arrow"]}</span>
        </div>
      </a>
'''


PROCESS = {
    "tr": [
        ("search", "Keşif & Analiz", "Saha incelemesi, ihtiyaç ve kapasite analizi ile doğru sistem seçiminin temelini atıyoruz."),
        ("blueprint", "Projelendirme", "Mekanik projeleri hazırlıyor, disiplinler arası koordinasyonu sağlıyoruz."),
        ("box", "Tedarik", "Projeye ve standartlara uygun, kalitesi kanıtlanmış malzeme ve ekipman temin ediyoruz."),
        ("wrench", "Montaj & Uygulama", "Deneyimli saha ekiplerimizle iş güvenliği kurallarına uygun uygulama yapıyoruz."),
        ("check", "Test & Teslim", "Testler, devreye alma ve dokümantasyon ile sistemi eksiksiz teslim ediyoruz."),
    ],
    "en": [
        ("search", "Survey & Analysis", "A site survey and load and capacity analysis lay the groundwork for the right system selection."),
        ("blueprint", "Design", "We produce the mechanical design and coordinate it with every other discipline."),
        ("box", "Procurement", "We source proven materials and equipment that meet the specification and relevant standards."),
        ("wrench", "Installation", "Experienced site teams carry out the works in full compliance with health and safety requirements."),
        ("check", "Testing & Handover", "Testing, commissioning and full O&M documentation for a clean handover."),
    ],
}
PROCESS_HEAD = {
    "tr": ("Çalışma Yöntemimiz", "Şeffaf, planlı ve ölçülebilir bir süreç.", "Her projeyi teknik gereklilikler ve güncel mühendislik yaklaşımlarıyla, net bir iş planı üzerinden yürütüyoruz."),
    "en": ("How We Work", "A transparent, well-planned and measurable process", "Every project runs to a clear programme, guided by technical requirements and current engineering practice."),
}


def process_section(lang):
    e, h, l = PROCESS_HEAD[lang]
    steps = "".join(
        f'<div class="process-step reveal{" reveal-delay-" + str(i % 4) if i % 4 else ""}"><span class="process-step-num">0{i + 1}</span>{I[ic]}<h3>{t}</h3><p>{p}</p></div>'
        for i, (ic, t, p) in enumerate(PROCESS[lang]))
    return f'''<section class="section section--dark" style="background:var(--navy-2)">
  <div class="container">
    <div class="section-head section-head--split">
      <div><span class="eyebrow">{e}</span><h2 class="h-lg">{h}</h2></div>
      <p class="lead">{l}</p>
    </div>
    <div class="process">{steps}</div>
  </div>
</section>
'''


# ================================================================ ANA SAYFA
HOME = {
    "tr": {
        "title": "BSM Mekanik | İstanbul Mekanik Tesisat, Yangın, HVAC ve Havalandırma",
        "desc": "Robert Koleji, Şişecam, Arçelik ve Özyeğin Üniversitesi referanslı BSM Mekanik; İstanbul’da mekanik tesisat, yangın söndürme, HVAC ve havalandırma.",
        "eyebrow": "Referanslarımız",
        "h1": "Güçlü referanslar, güvenilir mekanik mühendislik.",
        "lead": "Mekanik tesisat, yangın söndürme, HVAC ve havalandırmada projelendirmeden anahtar teslime çözümler.",
        "all_refs": "Tüm referanslar", "quote": "Teklif alın",
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
        "list_eyebrow": "Referans Listemizden",
        "list_h": "Eğitimden endüstriye, her ölçekte projeler.",
        "list_lead": f"2012’den bugüne {len(REFERENCES)} projede {fmt_num(TOTAL_AREA, 'tr')} m² alanda mekanik tesisat uygulaması.",
        "areas_eyebrow": "Uygulama Alanları",
        "areas_h": "Her ölçekte ve her yapı türünde.",
        "areas_lead": "Villalardan 50.000 m² üzeri fabrikalara kadar farklı ölçek ve gereksinimlerdeki projelerde deneyim.",
        "video_eyebrow": "Anahtar Teslim",
        "video_h": "Tek muhatap, eksiksiz mekanik altyapı.",
        "video_lead": "Projelendirme, malzeme temini ve montaj süreçlerini tek elden yöneterek zaman ve maliyet kaybını en aza indiriyoruz.",
        "video_btn": "Taahhüt hizmetlerimiz",
    },
    "en": {
        "title": "BSM Mechanical | Mechanical & Fire Protection Contractor, Istanbul",
        "desc": "Trusted by Robert College, Şişecam, Arçelik and Özyeğin University: an Istanbul-based contractor for mechanical, fire protection, HVAC and ventilation works.",
        "eyebrow": "Selected Projects",
        "h1": "A proven track record in mechanical engineering",
        "lead": "Mechanical, fire protection, HVAC and ventilation services, from design through to turnkey delivery.",
        "all_refs": "View all projects", "quote": "Get a quote",
        "facts": [(str(len(REFERENCES)), "Reference projects"), (fmt_num(AREA_ROUNDED, "en") + "+", "m² delivered"), ("7", "Areas of expertise"), ("Since 2012", "Delivering projects")],
        "marquee": "Selected clients",
        "about_eyebrow": "About Us",
        "about_h": "Engineering-led mechanical solutions, from design to handover",
        "about_lead": "Established in 2021, BSM Mechanical is an engineering firm specialising in mechanical installations, design and contracting.",
        "about_p": "We serve residential, commercial and industrial projects of every size, with quality, reliability and client satisfaction at the heart of every contract and turnkey delivery.",
        "about_list": ["Design, procurement, installation and commissioning under one roof", "Delivered to national and international standards", "A firm focus on site safety and on-time delivery", "Durable, sustainable system design"],
        "badge": "Founded",
        "services_eyebrow": "Our Services",
        "services_h": "Every mechanical system, one engineering team",
        "services_lead": "From fire safety to indoor air quality, plumbing to controls, we design and install your building's complete mechanical infrastructure.",
        "list_eyebrow": "From Our Portfolio",
        "list_h": "From education to industry, projects of every scale",
        "list_lead": f"{len(REFERENCES)} projects and {fmt_num(TOTAL_AREA, 'en')} m² of mechanical works delivered since 2012.",
        "areas_eyebrow": "Sectors",
        "areas_h": "Every scale, every building type",
        "areas_lead": "Experience on projects of every size, from private villas to manufacturing plants of over 50,000 m².",
        "video_eyebrow": "Turnkey Delivery",
        "video_h": "A single point of contact for your entire mechanical package",
        "video_lead": "With design, procurement and installation managed in-house, we keep programmes on track and costs under control.",
        "video_btn": "Mechanical contracting",
    },
}


def hero_slider(lang):
    t = HOME[lang]
    u = UI[lang]
    slides, infos, thumbs = "", "", ""
    n = len(FEATURED)
    for i, key in enumerate(FEATURED):
        r = REF_BY[key]
        active = " is-active" if i == 0 else ""
        hidden = "" if i == 0 else " hidden"
        name = escape(rname(r, lang))
        slides += (f'<figure class="rh-slide{active}" data-i="{i}" aria-roledescription="slide" aria-label="{i + 1} / {n}">'
                   f'{img(r["src"], rname(r, lang), lazy=i > 0, priority=i == 0, sizes="(min-width: 1000px) 720px, 100vw")}</figure>')
        chips = "".join(f"<li>{work(w, lang)}</li>" for w in r["works"][:4])
        client = f'<span class="rh-client">{escape(r["client"])}</span>' if r["client"] else ""
        infos += f'''<div class="rh-info{active}" data-i="{i}"{hidden}>
          <span class="rh-tag">{rcat(r, lang)}</span>
          <p class="rh-title">{name}</p>
          {client}
          <dl class="rh-meta"><div><dt>{u["area"]}</dt><dd>{fmt_num(r["area"], lang)} {u["m2"]}</dd></div><div><dt>{u["year"]}</dt><dd>{ryear(r, lang)}</dd></div><div><dt>{u["location"]}</dt><dd>{r["loc"]}</dd></div></dl>
          <ul class="rh-works">{chips}</ul>
        </div>
'''
        thumbs += (f'<button type="button" class="rh-thumb{active}" data-go="{i}" aria-label="{u["goto"]}: {name}"'
                   f'{CUR_TRUE if i == 0 else ""}>{thumb(r["src"])}</button>')
    facts = "".join(f"<div><strong>{v}</strong><span>{k}</span></div>" for v, k in t["facts"])
    return f'''<section class="ref-hero" data-hero aria-roledescription="carousel" aria-label="{t["eyebrow"]}">
  <div class="container ref-hero-grid">
    <div class="ref-hero-text on-dark">
      <span class="eyebrow">{t["eyebrow"]}</span>
      <h1>{t["h1"]}</h1>
      <p class="ref-hero-lead">{t["lead"]}</p>
      <div class="rh-infos" aria-live="polite">
        {infos}
      </div>
      <div class="rh-controls">
        <span class="rh-count"><b data-cur>01</b> / {n:02d}</span>
        <div class="rh-progress"><span></span></div>
        <div class="slider-nav"><button type="button" data-prev aria-label="{u["prev"]}">{I["arrow"]}</button><button type="button" data-next aria-label="{u["next"]}">{I["arrow"]}</button></div>
      </div>
      <div class="hero-actions">
        <a class="btn btn--white" href="{path("refs", lang)}">{t["all_refs"]} {I["arrow"]}</a>
        <a class="btn btn--ghost" href="{path("contact", lang)}">{t["quote"]}</a>
      </div>
    </div>
    <div class="ref-hero-visual">
      <div class="rh-stage">{slides}</div>
      <div class="rh-thumbs">{thumbs}</div>
    </div>
  </div>
  <div class="container"><div class="hero-facts">{facts}</div></div>
</section>
'''


def home(lang):
    t = HOME[lang]
    u = UI[lang]
    paths = {l: path("home", l) for l in LANGS}
    strip = "".join(f"<span>{n}</span>" for n in CLIENT_STRIP)
    strip2 = strip.replace("<span>", '<span aria-hidden="true">')
    cards = "".join(service_card(s, lang, i) for i, s in enumerate(SERVICES))
    refs = "".join(ref_card(REF_BY[k], lang, i % 3) for i, k in enumerate(HOME_REFS))
    areas = ""
    for k in ["konut", "ticari", "endustri", "egitim", "saglik", "otel"]:
        names = [rname(r, lang) for r in REFS if r["cat"] == k][:2]
        areas += f'<div class="area reveal">{I[CATEGORIES[k][2]]}<h3>{CATEGORIES[k][0 if lang == "tr" else 1]}</h3><p>{escape(", ".join(names))}</p></div>'
    about_list = "".join(f"<li>{I['check_circle']}{x}</li>" for x in t["about_list"])
    website = {"@type": "WebSite", "@id": C["domain_tr"] + "/#website", "url": absolute(paths[lang], lang),
               "name": C["short"], "inLanguage": lang, "publisher": {"@id": ORG_ID}}
    first = REF_BY[FEATURED[0]]["src"]
    preload = f'<link rel="preload" as="image" href="{first}" fetchpriority="high">\n'
    return head(lang, t["title"], t["desc"], paths, ld(org_schema(), website), preload) + header(lang, "home", paths) + f'''<main id="icerik">
{hero_slider(lang)}
<section class="marquee" aria-label="{t["marquee"]}">
  <p class="marquee-label">{t["marquee"]}</p>
  <div class="marquee-track">{strip}{strip2}</div>
</section>

<section class="section">
  <div class="container split">
    <div class="media-stack reveal">
      {img("/assets/img/hizmet/ekip.webp", "", sizes="(min-width: 960px) 560px, 100vw")}
      <div class="media-badge"><strong>{C["founded"]}</strong><span>{t["badge"]}</span></div>
    </div>
    <div class="reveal reveal-delay-1">
      <span class="eyebrow">{t["about_eyebrow"]}</span>
      <h2 class="h-lg">{t["about_h"]}</h2>
      <p class="lead">{t["about_lead"]}</p>
      <p style="margin-top:16px">{t["about_p"]}</p>
      <ul class="check-list">{about_list}</ul>
      <a class="btn btn--outline" href="{path("about", lang)}">{u["nav"]["about"]} {I["arrow"]}</a>
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

<section class="section">
  <div class="container">
    <div class="section-head section-head--split">
      <div><span class="eyebrow">{t["list_eyebrow"]}</span><h2 class="h-lg">{t["list_h"]}</h2></div>
      <div><p class="lead">{t["list_lead"]}</p><p style="margin-top:18px"><a class="link-arrow" href="{path("refs", lang)}">{t["all_refs"]} {I["arrow"]}</a></p></div>
    </div>
    <div class="ref-grid">
{refs}    </div>
  </div>
</section>

<section class="video-band">
  <video autoplay muted loop playsinline preload="none" poster="/assets/img/hero-poster.jpg" aria-hidden="true">
    <source src="/assets/video/hero.mp4" type="video/mp4">
  </video>
  <div class="container on-dark">
    <span class="eyebrow">{t["video_eyebrow"]}</span>
    <h2 class="h-lg">{t["video_h"]}</h2>
    <p class="lead">{t["video_lead"]}</p>
    <a class="btn btn--white" href="{path(None, lang, SERVICES[5])}">{t["video_btn"]} {I["arrow"]}</a>
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
{process_section(lang)}<div class="section--tight"></div>
</main>
''' + cta(lang) + footer(lang)


# ================================================================ KURUMSAL
ABOUT = {
    "tr": {
        "title": "Kurumsal | BSM Mekanik Mühendislik — Hakkımızda, Vizyon ve Misyon",
        "desc": "2021’de kurulan BSM Mekanik; mekanik tesisat, projelendirme ve taahhüt alanlarında faaliyet gösteren İstanbul merkezli bir mühendislik firmasıdır.",
        "h1": "Kalite, güvenilirlik ve teknik uzmanlıkla büyüyen bir mühendislik firması.",
        "lead": "Mekanik tesisat, mühendislik, projelendirme ve taahhüt alanlarında sürdürülebilir ve uzun ömürlü çözümler üretiyoruz.",
        "intro_eyebrow": "Biz Kimiz", "intro_h": "BSM Mekanik Mühendislik",
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
        "values_eyebrow": "Değerlerimiz", "values_h": "Her projede değişmeyen ilkelerimiz.",
        "values": [
            ("shield", "İş Güvenliği", "Sahadaki her çalışanın ve yapının güvenliği önceliğimizdir."),
            ("award", "Kalite", "Ulusal ve uluslararası standartlara uygun malzeme ve uygulama."),
            ("clock", "Zamanında Teslim", "Planlı iş programı ve şeffaf süreç takibi."),
            ("leaf", "Sürdürülebilirlik", "Enerji verimli, uzun ömürlü ve bakımı kolay sistemler."),
            ("handshake", "Müşteri Memnuniyeti", "Teslimden sonra da süren, uzun vadeli iş ortaklığı."),
        ],
        "numbers_eyebrow": "Rakamlarla", "numbers_h": "Referanslarımızla büyüyen deneyim.",
        "numbers": [(len(REFERENCES), "", "Referans proje"), (AREA_ROUNDED // 1000, "bin", "m² uygulama alanı"), (7, "", "Uzmanlık alanı"), (len({r["loc"].split(" - ")[0] for r in REFS}), "", "Farklı il")],
    },
    "en": {
        "title": "About Us | BSM Mechanical Engineering — Profile, Vision & Mission",
        "desc": "Established in 2021, BSM Mechanical is an Istanbul-based engineering firm specialising in mechanical installations, design and contracting.",
        "h1": "An engineering firm built on quality, reliability and technical expertise",
        "lead": "Sustainable, long-lasting solutions in mechanical installations, engineering, design and contracting.",
        "intro_eyebrow": "Who We Are", "intro_h": "BSM Mechanical Engineering",
        "paras": [
            f"Established in 2021, {C['legal']} (BSM Mechanical) is an engineering firm working across mechanical installations, engineering, design and contracting.",
            "Our services cover fire protection, HVAC and air conditioning, ventilation, heating, cooling and plumbing.",
            "Drawing on our technical know-how and project track record, we engineer solutions for residential, commercial and industrial projects of every scale, and put quality, reliability and client satisfaction first on every contract and turnkey delivery.",
            "From design to handover, every decision we make is grounded in technical requirements and current engineering practice, with the aim of delivering systems that are sustainable and built to last.",
        ],
        "quote": "From design to handover, every decision is grounded in <em>technical requirements</em> and <em>current engineering practice</em>.",
        "vision": ("Our Vision", [
            "To be one of Türkiye's leading mechanical engineering firms, the partner of choice nationwide for quality, reliability and technical expertise, creating lasting value for the industry.",
            "By embracing new technologies and innovative engineering, we aim to keep growing our capabilities, deliver sustainable projects and build long-term partnerships.",
        ]),
        "mission": ("Our Mission", [
            "To give our clients reliable, high-quality and sustainable mechanical solutions, backed by sound engineering knowledge and technical expertise.",
            "On every project, we put health and safety, quality, on-time delivery and client satisfaction first, developing efficient solutions tailored to each client's needs.",
        ]),
        "values_eyebrow": "Our Values", "values_h": "The principles behind every project",
        "values": [
            ("shield", "Health & Safety", "The safety of everyone on site, and of every building we work on, comes first."),
            ("award", "Quality", "Materials and workmanship that meet national and international standards."),
            ("clock", "On-time Delivery", "A realistic programme and transparent progress reporting."),
            ("leaf", "Sustainability", "Energy-efficient, durable systems that are easy to maintain."),
            ("handshake", "Client Focus", "A long-term partnership that continues well beyond handover."),
        ],
        "numbers_eyebrow": "In Numbers", "numbers_h": "Experience built on our track record",
        "numbers": [(len(REFERENCES), "", "Reference projects"), (AREA_ROUNDED // 1000, "k", "m² delivered"), (7, "", "Areas of expertise"), (len({r["loc"].split(" - ")[0] for r in REFS}), "", "Provinces")],
    },
}


def about(lang):
    t = ABOUT[lang]
    u = UI[lang]
    paths = {l: path("about", l) for l in LANGS}
    crumbs = [(u["nav"]["home"], path("home", lang)), (u["nav"]["about"], paths[lang])]
    paras = "".join(f"<p>{p}</p>" for p in t["paras"][1:])
    vis = "".join(f"<p>{p}</p>" for p in t["vision"][1])
    mis = "".join(f"<p>{p}</p>" for p in t["mission"][1])
    values = "".join(
        f'<div class="value reveal{" reveal-delay-" + str(i % 4) if i % 4 else ""}">{I[ic]}<h3>{h}</h3><p>{p}</p></div>'
        for i, (ic, h, p) in enumerate(t["values"]))
    nums = "".join(
        f'<div class="stat reveal"><strong><span data-count="{n}">{n}</span>{"<sup>" + s + "</sup>" if s else ""}</strong><span>{lbl}</span></div>'
        for n, s, lbl in t["numbers"])
    page = {"@type": "AboutPage", "url": absolute(paths[lang], lang), "name": t["title"], "inLanguage": lang, "about": {"@id": ORG_ID}}
    return head(lang, t["title"], t["desc"], paths, ld(page, breadcrumb_schema(crumbs, lang))) + header(lang, "about", paths) \
        + page_hero(lang, t["h1"], t["lead"], "/assets/img/hizmet/saha.webp", crumbs) + f'''<main id="icerik">
<section class="section">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">{t["intro_eyebrow"]}</span>
      <h2 class="h-lg">{t["intro_h"]}</h2>
      <p class="lead">{t["paras"][0]}</p>
      <div style="margin-top:18px">{paras}</div>
    </div>
    <div class="media-stack reveal reveal-delay-1">
      {img("/assets/img/hizmet/projelendirme.webp", "", sizes="(min-width: 960px) 560px, 100vw")}
      <div class="media-badge"><strong>{C["founded"]}</strong><span>{HOME[lang]["badge"]}</span></div>
    </div>
  </div>
</section>

<section class="section section--bg">
  <div class="container">
    <p class="big-quote reveal" style="margin-bottom:clamp(40px,6vw,64px)">{t["quote"]}</p>
    <div class="mv-grid">
      <div class="mv-card mv-card--brand reveal">{I["eye"]}<h2 class="h-md">{t["vision"][0]}</h2>{vis}</div>
      <div class="mv-card reveal reveal-delay-1">{I["target"]}<h2 class="h-md">{t["mission"][0]}</h2>{mis}</div>
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
    <div class="section-head section-head--split">
      <div><span class="eyebrow">{t["numbers_eyebrow"]}</span><h2 class="h-lg">{t["numbers_h"]}</h2></div>
      <p><a class="link-arrow" href="{path("refs", lang)}">{u["nav"]["refs"]} {I["arrow"]}</a></p>
    </div>
    <div class="stats">{nums}</div>
  </div>
</section>
</main>
''' + cta(lang) + footer(lang)


# ================================================================ HİZMETLER (genel)
SERV = {
    "tr": {"title": "Hizmetlerimiz | Mekanik Tesisat, Yangın, HVAC — BSM Mekanik",
           "desc": "Mekanik tesisat, yangın söndürme, HVAC, havalandırma, projelendirme, anahtar teslim taahhüt ile elektrik ve otomasyon hizmetleri.",
           "h1": "Mekanik tesisatın her alanında uçtan uca hizmet.",
           "lead": "Yedi uzmanlık alanında; projelendirme, tedarik, montaj ve devreye alma süreçlerini tek elden yönetiyoruz.",
           "eyebrow": "Uzmanlık Alanlarımız", "h2": "Yapınızın tüm mekanik altyapısı için tek çözüm ortağı.",
           "intro": "Her hizmetimizi; yapının kullanım amacı, ölçeği ve yönetmelik gereklilikleri doğrultusunda planlıyor, projelendirmeden devreye almaya kadar aynı mühendislik disipliniyle yürütüyoruz."},
    "en": {"title": "Services | Mechanical, Fire Protection & HVAC — BSM Mechanical",
           "desc": "Mechanical installation, fire protection systems, HVAC and air-conditioning, ventilation, engineering and design, turnkey contracting, electrical and automation services.",
           "h1": "End-to-end expertise across every mechanical discipline",
           "lead": "Seven areas of expertise, with design, procurement, installation and commissioning managed under one roof.",
           "eyebrow": "Areas of Expertise", "h2": "One partner for your building's entire mechanical package",
           "intro": "Every service is planned around the building's use, scale and regulatory requirements, and delivered with the same engineering discipline from design through to commissioning."},
}


def services(lang):
    t = SERV[lang]
    u = UI[lang]
    paths = {l: path("services", l) for l in LANGS}
    crumbs = [(u["nav"]["home"], path("home", lang)), (u["nav"]["services"], paths[lang])]
    cards = "".join(service_card(s, lang, i) for i, s in enumerate(SERVICES))
    item_list = {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": s[lang]["name"], "url": absolute(path(None, lang, s), lang)} for i, s in enumerate(SERVICES)]}
    return head(lang, t["title"], t["desc"], paths, ld(item_list, breadcrumb_schema(crumbs, lang))) + header(lang, "services", paths) \
        + page_hero(lang, t["h1"], t["lead"], "/assets/img/hizmet/sprinkler-tavan.webp", crumbs) + f'''<main id="icerik">
<section class="section section--bg">
  <div class="container">
    <div class="section-head section-head--split">
      <div><span class="eyebrow">{t["eyebrow"]}</span><h2 class="h-lg">{t["h2"]}</h2></div>
      <p class="lead">{t["intro"]}</p>
    </div>
    <div class="service-grid">
{cards}    </div>
  </div>
</section>
{process_section(lang)}<div class="section--tight"></div>
</main>
''' + cta(lang) + footer(lang)


# ================================================================ HİZMET DETAY
SVC_UI = {
    "tr": {"title": "{name} | İstanbul — BSM Mekanik", "scope": "Hizmet kapsamı", "approach": "Yaklaşımımız",
           "refs": "Bu alandaki referanslarımız", "faq": "Sık sorulan sorular", "others": "Diğer hizmetlerimiz",
           "contact_h": "Projeniz için teklif alın", "contact_p": "Keşif ve teknik değerlendirme için bize ulaşın.",
           "form": "Teklif formu", "all_refs": "Tüm referanslar",
           "faqs": [
               ("{name} hizmetini hangi yapı türlerinde veriyorsunuz?",
                "Konut ve villalardan otel, ofis, eğitim ve sağlık yapılarına, fabrika ve depolara kadar farklı ölçeklerdeki projelerde hizmet veriyoruz. Bu alandaki referanslarımız arasında {examples} yer alıyor."),
               ("Projelendirme ve uygulamayı birlikte üstleniyor musunuz?",
                "Evet. Keşif ve projelendirmeden malzeme temini, montaj, test ve devreye almaya kadar tüm süreci tek muhatap olarak yönetebiliyor; ihtiyaca göre yalnızca projelendirme, kontrollük veya uygulama aşamasında da hizmet verebiliyoruz."),
               ("Hangi bölgelerde hizmet veriyorsunuz?",
                "İstanbul Maltepe merkezli olarak başta İstanbul ve Kocaeli olmak üzere Türkiye genelinde çalışıyoruz; Kırklareli, Çorum, Nevşehir ve Muğla’da da tamamlanmış projelerimiz bulunuyor."),
               ("Teklif almak için hangi bilgiler gerekiyor?",
                "Projenin türünü, yaklaşık alanını (m²), konumunu ve talep ettiğiniz hizmetleri iletişim formu, telefon veya e-posta ile iletmeniz yeterli. Gerekirse keşif planlayarak teknik değerlendirme ve teklifimizi hazırlıyoruz."),
           ]},
    "en": {"title": "{name} in Istanbul | BSM Mechanical", "scope": "Scope of service", "approach": "Our approach",
           "refs": "Our projects in this field", "faq": "Frequently asked questions", "others": "Other services",
           "contact_h": "Get a quote for your project", "contact_p": "Contact us for a site survey and technical assessment.",
           "form": "Request a quote", "all_refs": "All projects",
           "faqs": [
               ("What types of building do you work on?",
                "We work on projects of every scale, from homes and villas to hotels, offices, schools, healthcare buildings, factories and warehouses. Recent projects in this field include {examples}."),
               ("Do you handle both design and installation?",
                "Yes. We can act as your single point of contact for the whole process, from survey and design through procurement, installation, testing and commissioning, or support you at the design, site supervision or installation stage only."),
               ("Which regions do you cover?",
                "We are based in Maltepe, Istanbul, and work across Türkiye, mainly in Istanbul and Kocaeli, with completed projects in Kırklareli, Çorum, Nevşehir and Muğla."),
               ("What information do you need for a quote?",
                "Just send us the project type, approximate floor area (m²), location and the services you need, via the contact form, phone or email. Where needed, we will arrange a site survey before preparing our technical assessment and quotation."),
           ]},
}


def service_page(s, lang):
    x = s[lang]
    t = SVC_UI[lang]
    u = UI[lang]
    paths = {l: path(None, l, s) for l in LANGS}
    crumbs = [(u["nav"]["home"], path("home", lang)), (u["nav"]["services"], path("services", lang)), (x["name"], paths[lang])]
    rel = sorted((r for r in REFS if s["key"] in r["tags"]), key=lambda r: r["imgtype"] == "stock")
    examples = ", ".join(rname(r, lang) for r in rel[:3])
    faqs = [(q.format(name=x["name"], name_l=x["name"].lower()), a.format(examples=examples)) for q, a in t["faqs"]]
    items = "".join(f"<li>{I['check_sm']}{it}</li>" for it in x["items"])
    mini = "".join(
        f'<div class="mini-ref">{thumb(r["src"]).replace(' alt=""', ' alt="' + escape(rname(r, lang)) + '" loading="lazy"')}<div><strong>{escape(rname(r, lang))}</strong>'
        f'<span>{r["loc"]} · {fmt_num(r["area"], lang)} {u["m2"]} · {ryear(r, lang)}</span></div></div>'
        for r in rel[:6])
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    others = "".join(
        f'<li><a href="{path(None, lang, o)}"{CUR_PAGE if o is s else ""}>{o[lang]["name"]}{I["arrow"]}</a></li>' for o in SERVICES)
    service_ld = {
        "@type": "Service", "name": x["name"], "serviceType": x["name"], "description": x["intro"],
        "provider": {"@id": ORG_ID}, "areaServed": {"@type": "Country", "name": "Türkiye"},
        "url": absolute(paths[lang], lang), "inLanguage": lang,
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": x["name"],
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": it}} for it in x["items"]]},
    }
    faq_ld = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    title = t["title"].format(name=x["name"])
    desc = (x["intro"][:150].rsplit(" ", 1)[0] + "…") if len(x["intro"]) > 158 else x["intro"]
    return head(lang, title, desc, paths, ld(service_ld, faq_ld, breadcrumb_schema(crumbs, lang))) + header(lang, "services", paths) \
        + page_hero(lang, x["name"], x["short"], "/assets/img/hizmet/" + s["img"] + ".webp", crumbs) + f'''<main id="icerik">
<section class="section">
  <div class="container svc-layout">
    <article class="svc-main">
      <p class="lead">{x["intro"]}</p>
      <h2>{t["scope"]}</h2>
      <ul class="bullet-grid">{items}</ul>
      <h2>{t["approach"]}</h2>
      <p>{s["detail"][lang]}</p>
      <h2>{t["refs"]}</h2>
      <div class="mini-refs">{mini}</div>
      <p style="margin-top:20px"><a class="link-arrow" href="{path("refs", lang)}#{s["key"]}">{t["all_refs"]} ({len(rel)}) {I["arrow"]}</a></p>
      <h2>{t["faq"]}</h2>
      <div class="faq">{faq_html}</div>
    </article>
    <aside class="svc-aside">
      <div class="aside-box">
        <h2 class="footer-title" style="color:var(--ink)">{t["others"]}</h2>
        <ul class="aside-nav">{others}</ul>
      </div>
      <div class="aside-box aside-box--brand">
        <h2 class="h-md" style="font-size:20px;color:#fff;margin-bottom:10px">{t["contact_h"]}</h2>
        <p>{t["contact_p"]}</p>
        <a class="tel" href="tel:{C["office_tel"]}">{C["office_phone"]}</a>
        <a href="mailto:{C["people"][0]["email"]}" style="color:#fff">{C["people"][0]["email"]}</a>
        <a class="btn btn--white" href="{path("contact", lang)}?hizmet={s["key"]}">{t["form"]} {I["arrow"]}</a>
      </div>
    </aside>
  </div>
</section>
</main>
''' + cta(lang) + footer(lang)


# ================================================================ REFERANSLAR
REFP = {
    "tr": {"title": "Referanslar | 31 Proje — BSM Mekanik Mühendislik",
           "desc": "Robert Koleji, Şişecam, Arçelik, Özyeğin Üniversitesi, Hanwha Aerospace ve daha fazlası: BSM Mekanik’in 2012’den bugüne mekanik tesisat referans projeleri.",
           "h1": "Güvenle tamamlanan projeler.", "lead": f"2012’den bugüne {len(REFERENCES)} proje ve {fmt_num(TOTAL_AREA, 'tr')} m² uygulama alanı.",
           "all": "Tümü", "filter": "Hizmete göre filtrele", "empty": "Bu kategoride proje bulunamadı.",
           "credit": "Robert Koleji fotoğrafı: Yaguzi; Özyeğin Üniversitesi fotoğrafı: Bo yaser — Wikimedia Commons, CC BY-SA 4.0."},
    "en": {"title": "Projects | Selected Work Since 2012 — BSM Mechanical",
           "desc": "Robert College, Şişecam, Arçelik, Özyeğin University, Hanwha Aerospace and more: mechanical, fire protection and HVAC projects delivered by BSM Mechanical since 2012.",
           "h1": "Projects delivered with confidence.", "lead": f"{len(REFERENCES)} projects and {fmt_num(TOTAL_AREA, 'en')} m² of mechanical works delivered since 2012.",
           "all": "All", "filter": "Filter by service", "empty": "No projects found in this category.",
           "credit": "Robert College photo: Yaguzi; Özyeğin University photo: Bo yaser — Wikimedia Commons, CC BY-SA 4.0."},
}


def refs(lang):
    t = REFP[lang]
    u = UI[lang]
    paths = {l: path("refs", l) for l in LANGS}
    crumbs = [(u["nav"]["home"], path("home", lang)), (u["nav"]["refs"], paths[lang])]
    btns = f'<button type="button" data-tag="all" aria-pressed="true">{t["all"]}<span>{len(REFS)}</span></button>'
    for s in SERVICES:
        n = sum(1 for r in REFS if s["key"] in r["tags"])
        if n:
            btns += f'<button type="button" data-tag="{s["key"]}" aria-pressed="false">{s[lang]["name"]}<span>{n}</span></button>'
    cards = "".join(ref_card(r, lang, i % 3, heading="h2") for i, r in enumerate(REFS))
    coll = {"@type": "CollectionPage", "url": absolute(paths[lang], lang), "name": t["title"], "inLanguage": lang,
            "about": {"@id": ORG_ID},
            "mainEntity": {"@type": "ItemList", "numberOfItems": len(REFS), "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": rname(r, lang)} for i, r in enumerate(REFS)]}}
    return head(lang, t["title"], t["desc"], paths, ld(coll, breadcrumb_schema(crumbs, lang))) + header(lang, "refs", paths) \
        + page_hero(lang, t["h1"], t["lead"], "/assets/img/ref/sisecam-bilim.webp", crumbs) + f'''<main id="icerik">
<section class="section">
  <div class="container">
    <div class="filter-bar" data-filter role="group" aria-label="{t["filter"]}">{btns}</div>
    <div class="ref-grid">
{cards}    </div>
    <p class="ref-empty" hidden>{t["empty"]}</p>
    <p class="text-muted" style="margin-top:48px;font-size:12.5px">{t["credit"]}</p>
  </div>
</section>
</main>
''' + cta(lang) + footer(lang)


# ================================================================ İLETİŞİM
CONT = {
    "tr": {"title": "İletişim | BSM Mekanik — Maltepe, İstanbul",
           "desc": "BSM Mekanik iletişim: Altıntepe Mah. İstasyon Yolu Sok. No:3/1 Maltepe/İstanbul · +90 (216) 706 14 01. Teklif ve keşif talepleriniz için bize ulaşın.",
           "h1": "Projenizi konuşalım.", "lead": "Teklif, keşif veya teknik danışmanlık talepleriniz için bize ulaşın; en kısa sürede dönüş yapalım.",
           "office": "Merkez Ofis", "phone": "Telefon", "email": "E-posta", "mobile": "Cep",
           "form_eyebrow": "Teklif Formu", "form_h": "Bize yazın",
           "f": {"name": "Ad Soyad", "company": "Firma", "email": "E-posta", "phone": "Telefon", "topic": "Hizmet", "msg": "Mesajınız",
                 "msg_ph": "Proje türü, alan (m²), konum ve talep ettiğiniz hizmetleri yazmanız değerlendirmemizi hızlandırır.",
                 "choose": "Seçiniz", "other": "Diğer",
                 "consent": "Kişisel verilerimin talebime dönüş yapılması amacıyla işlenmesini kabul ediyorum (<a href=\"#kvkk\">KVKK Aydınlatma Metni</a>).",
                 "send": "Gönder", "subject": "Web sitesi talebi", "success": "Teşekkürler! E-posta uygulamanız açılıyor; mesajınızı göndermeniz yeterli."},
           "map": "BSM Mekanik ofis konumu", "directions": "Yol tarifi al",
           "kvkk_h": "KVKK Aydınlatma Metni",
           "kvkk": [
               f"Veri sorumlusu {C['legal']} (“BSM Mekanik”) olarak, iletişim formu, e-posta, telefon veya WhatsApp üzerinden ilettiğiniz ad-soyad, firma, e-posta, telefon ve mesaj içeriği bilgilerinizi; yalnızca talebinize dönüş yapmak, teklif hazırlamak ve sizinle iletişim kurmak amacıyla, 6698 sayılı Kişisel Verilerin Korunması Kanunu’nun 5. maddesi kapsamında açık rızanıza ve bir sözleşmenin kurulmasıyla doğrudan ilgili olmasına dayanarak işliyoruz.",
               "Kişisel verileriniz, yasal yükümlülükler dışında üçüncü kişilerle paylaşılmaz ve işleme amacının gerektirdiği süre boyunca saklanır. Web sitemiz reklam veya takip amaçlı çerez kullanmaz; iletişim sayfasındaki harita Google Maps tarafından sağlanır ve Google’ın gizlilik politikasına tabidir.",
               f"KVKK’nın 11. maddesi uyarınca verilerinizin işlenip işlenmediğini öğrenme, düzeltilmesini veya silinmesini isteme gibi haklarınızı kullanmak için {C['people'][0]['email']} adresine yazabilirsiniz.",
           ]},
    "en": {"title": "Contact | BSM Mechanical — Maltepe, Istanbul",
           "desc": "Contact BSM Mechanical in Maltepe, Istanbul: +90 (216) 706 14 01, mert@bsmmechanical.com. Get in touch for quotations and site surveys.",
           "h1": "Let's talk about your project", "lead": "Get in touch for quotations, site surveys or technical advice, and we'll respond as soon as possible.",
           "office": "Head Office", "phone": "Phone", "email": "Email", "mobile": "Mobile",
           "form_eyebrow": "Quote Form", "form_h": "Write to us",
           "f": {"name": "Full name", "company": "Company", "email": "Email", "phone": "Phone", "topic": "Service", "msg": "Message",
                 "msg_ph": "Tell us the project type, floor area (m²), location and services required so we can respond faster.",
                 "choose": "Select", "other": "Other",
                 "consent": "I consent to my personal data being processed in order to respond to my request (<a href=\"#kvkk\">Privacy Notice</a>).",
                 "send": "Send", "subject": "Website enquiry", "success": "Thank you! Your email app is opening; just press send."},
           "map": "BSM Mechanical office location", "directions": "Get directions",
           "kvkk_h": "Privacy Notice",
           "kvkk": [
               f"As data controller, {C['legal']} (“BSM Mechanical”) processes the name, company, email, phone and message details you send via the contact form, email, phone or WhatsApp solely to respond to your request, prepare proposals and communicate with you, under Article 5 of Turkish Personal Data Protection Law No. 6698, based on your explicit consent and as directly related to establishing a contract.",
               "Your personal data is not shared with third parties except where required by law, and is kept only as long as the purpose requires. Our website does not use advertising or tracking cookies; the map on the contact page is provided by Google Maps and subject to Google’s privacy policy.",
               f"To exercise your rights under Article 11 of the Law, such as learning whether your data is processed or requesting its correction or deletion, please write to {C['people'][0]['email']}.",
           ]},
}


def contact(lang):
    t = CONT[lang]
    f = t["f"]
    u = UI[lang]
    paths = {l: path("contact", l) for l in LANGS}
    crumbs = [(u["nav"]["home"], path("home", lang)), (u["nav"]["contact"], paths[lang])]
    mailto = ",".join(p["email"] for p in C["people"])
    opts = "".join(f'<option data-key="{s["key"]}" value="{s[lang]["name"]}">{s[lang]["name"]}</option>' for s in SERVICES)
    mq = quote(C["map_query"])
    phones = "".join(f'<span class="label">{p["name"]} · {t["mobile"]}</span><a href="tel:{p["tel"]}">{p["phone"]}</a>' for p in C["people"])
    mails = "".join(f'<span class="label">{p["name"]}</span><a href="mailto:{p["email"]}">{p["email"]}</a>' for p in C["people"])
    kvkk = "".join(f'<p class="text-muted" style="max-width:90ch;margin-top:12px">{p}</p>' for p in t["kvkk"])
    page = {"@type": "ContactPage", "url": absolute(paths[lang], lang), "name": t["title"], "inLanguage": lang, "about": {"@id": ORG_ID}}
    return head(lang, t["title"], t["desc"], paths, ld(page, org_schema(), breadcrumb_schema(crumbs, lang))) + header(lang, "contact", paths) \
        + page_hero(lang, t["h1"], t["lead"], "/assets/img/hizmet/vrf-yangin.webp", crumbs) + f'''<main id="icerik">
<section class="section">
  <div class="container">
    <div class="contact-cards">
      <div class="contact-card reveal">{I["building"]}<h2 class="h-md" style="font-size:18px">{t["office"]}</h2><address style="font-style:normal">{C["address"]}<br>{C["city"]}</address><a class="link-arrow" style="margin-top:10px" href="https://www.google.com/maps/search/?api=1&amp;query={mq}" target="_blank" rel="noopener">{t["directions"]} {I["arrow"]}</a></div>
      <div class="contact-card reveal reveal-delay-1">{I["phone_lg"]}<h2 class="h-md" style="font-size:18px">{t["phone"]}</h2><span class="label">{t["office"]}</span><a href="tel:{C["office_tel"]}">{C["office_phone"]}</a>{phones}</div>
      <div class="contact-card reveal reveal-delay-2">{I["mail_lg"]}<h2 class="h-md" style="font-size:18px">{t["email"]}</h2>{mails}</div>
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
    <h2 class="h-md" style="margin-bottom:6px">{t["kvkk_h"]}</h2>
    {kvkk}
  </div>
</section>
</main>
''' + footer(lang)


# ================================================================ 404 / sitemap / manifest
def notfound():
    return f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sayfa bulunamadı | BSM Mekanik</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
<main class="notfound">
  <div>
    <svg viewBox="{LOGO_VIEWBOX}" style="width:64px;margin:0 auto 28px;color:#a9c0ea" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{LOGO_PATH}"/></svg>
    <strong>404</strong>
    <h1>Aradığınız sayfa bulunamadı.</h1>
    <p>The page you are looking for could not be found.</p>
    <p style="margin-top:28px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
      <a class="btn btn--white" href="/">Ana Sayfa {I["arrow"]}</a>
      <a class="btn btn--ghost" href="/en/">Home</a>
    </p>
  </div>
</main>
</body>
</html>
'''


def sitemap(all_paths):
    rows = []
    for paths in all_paths:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{absolute(paths[l], l)}"/>' for l in LANGS)
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{absolute(paths["tr"], "tr")}"/>'
        for l in LANGS:
            rows.append(f"  <url><loc>{absolute(paths[l], l)}</loc><lastmod>{TODAY}</lastmod>{alts}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def manifest():
    return json.dumps({
        "name": C["short"], "short_name": "BSM", "lang": "tr", "start_url": "/", "display": "browser",
        "background_color": "#0a1630", "theme_color": "#0a1630",
        "icons": [{"src": "/assets/img/logo-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/logo-512.png", "sizes": "512x512", "type": "image/png"}],
    }, ensure_ascii=False, indent=2) + "\n"


def write(p, html):
    # Başlıklar nokta ile bitmez
    html = re.sub(r"\.(\s*</h[1-3]>)", r"\1", html)
    f = out_file(p)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html, encoding="utf-8")
    print("yazıldı:", f.relative_to(ROOT))


def main():
    all_paths = []
    for page, fn in (("home", home), ("about", about), ("services", services), ("refs", refs), ("contact", contact)):
        paths = {l: path(page, l) for l in LANGS}
        all_paths.append(paths)
        for l in LANGS:
            write(paths[l], fn(l))
    for s in SERVICES:
        paths = {l: path(None, l, s) for l in LANGS}
        all_paths.append(paths)
        for l in LANGS:
            write(paths[l], service_page(s, l))
    (PUBLIC / "404.html").write_text(notfound(), encoding="utf-8")
    (PUBLIC / "sitemap.xml").write_text(sitemap(all_paths), encoding="utf-8")
    (PUBLIC / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {C['domain_tr']}/sitemap.xml\n", encoding="utf-8")
    (PUBLIC / "site.webmanifest").write_text(manifest(), encoding="utf-8")
    print(f"Toplam referans alanı: {TOTAL_AREA} m²")


if __name__ == "__main__":
    main()
