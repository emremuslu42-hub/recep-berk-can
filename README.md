# RBC Mühendislik — Kurumsal Web Sitesi

Karayolu dışı endüstriyel taşıma sistemleri (transfer arabaları, AGV, SPMT, hava yastıklı taşıyıcılar, pota arabaları) üreten bir mühendislik firması için statik kurumsal site.

Derleme adımı yoktur: saf HTML + CSS + JS. Herhangi bir statik hostinge (cPanel, Netlify, Vercel, GitHub Pages) klasör olduğu gibi yüklenebilir.

```
index.html       Ana sayfa (video hero, ürünler, sektörler, süreç, projeler)
kurumsal.html    Hakkımızda, misyon/vizyon, tarihçe, Ar-Ge, sertifikalar
urunler.html     6 ürün grubu, teknik özellik tabloları
sektorler.html   7 sektör
projeler.html    Referans projeler
iletisim.html    İletişim bilgileri, teklif formu, harita
assets/css/style.css   Tasarım sistemi (renkler :root içinde)
assets/js/main.js      Menü, animasyonlar, sayaçlar, form
assets/img, assets/video
```

Yerelde görmek için:

```bash
python3 -m http.server 8000 -d public
```

## Müşteriden alınıp güncellenmesi gerekenler

Aşağıdaki içerikler **yer tutucudur**, gerçek bilgilerle değiştirilmelidir (tüm sayfalarda geçer, toplu bul-değiştir yeterli):

- Firma adı ve logo: `RBC Mühendislik`, logo SVG'si header/footer'da ve `assets/img/favicon.svg`
- Telefon `+90 (262) 000 00 00`, e-posta `info@rbcmuhendislik.com.tr`, adres
- İstatistikler (350+ sistem, 20+ ülke vb.), tarihçe yılları, proje örnekleri
- Sertifikalar (ISO 9001/14001/45001, CE) — yalnızca firmada gerçekten olanlar kalmalı
- Sosyal medya linkleri ve KVKK / Çerez metinleri (`href="#"`)
- Harita konumu (`iletisim.html` içindeki OpenStreetMap iframe `bbox` değeri)
- İletişim formu şu an ziyaretçinin e-posta uygulamasını açar; sunucu tarafı form (PHP mail, Formspree vb.) bağlanabilir

Firmanın kendi ürün/saha fotoğrafları geldiğinde `assets/img` içindeki aynı isimli dosyalar değiştirilerek kolayca güncellenebilir.

## Görsel ve video kaynakları

Tüm medya ücretsiz ticari kullanıma izin veren lisanslarla alınmıştır:

- Fotoğraflar: [Unsplash](https://unsplash.com/license) (Unsplash License)
- Videolar: [Pexels](https://www.pexels.com/license/) (Pexels License) — `hero.mp4` (çelikhane, video #6997690), `kivilcim.mp4` (fırın kıvılcımları, video #6997856)
