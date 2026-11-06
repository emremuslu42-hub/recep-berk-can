# BSM Mekanik — Kurumsal Web Sitesi

BSM Mekanik Mühendislik İnşaat San. ve Tic. Ltd. Şti. için iki dilli (TR/EN) statik kurumsal site.
Cloudflare Workers (statik asset) üzerinde yayınlanır; derleme sunucusu gerektirmez.

- Türkçe: `https://www.bsmmekanik.com/` (kök) — canonical
- İngilizce: `https://www.bsmmechanical.com/en/` — canonical
- Çıplak alan adları (`bsmmekanik.com`, `bsmmechanical.com`) `www` adresine yönlenir.
- İki alan adı da sitenin tamamını açar; dil seçimi sağ üstteki TR/EN düğmesiyle yapılır.

## Klasör yapısı

```
src/content.py   Tüm içerik: firma bilgileri, hizmetler, 31 referans proje (TR/EN)
src/build.py     Sayfa şablonları; public/ altındaki HTML dosyalarını üretir
src/icons.py     SVG ikonlar ve vektör logo
src/generate-images.js  Paylaşım görselleri (og-tr/en.jpg) ve PNG ikonları üretir (Playwright)
public/          Yayınlanan site (Cloudflare bu klasörü sunar)
  index.html, kurumsal.html, hizmetler.html, referanslar.html, iletisim.html
  en/            İngilizce sayfalar
  assets/        CSS, JS, görseller, videolar
wrangler.jsonc   Cloudflare Workers yapılandırması
```

## İçerik güncelleme

1. `src/content.py` (veya şablon için `src/build.py`) dosyasını düzenleyin.
2. Sayfaları yeniden üretin:

```bash
python3 src/build.py
```

3. Commit + push; Cloudflare otomatik yayınlar.

`public/*.html` dosyalarını elle düzenlemeyin, bir sonraki üretimde üzerine yazılır.

Yerelde önizleme (uzantısız adresler için `.html` eklemeniz gerekebilir):

```bash
python3 -m http.server 8000 -d public
```

## Sayfalar

| TR | EN |
|---|---|
| `/` | `/en/` |
| `/kurumsal` | `/en/about` |
| `/hizmetler` + 7 hizmet sayfası (`/hizmetler/yangin-sondurme-sistemleri` …) | `/en/services` + 7 hizmet sayfası |
| `/referanslar` (hizmete göre filtre, `#yangin` gibi bağlantılar) | `/en/projects` |
| `/iletisim` (+ KVKK metni `#kvkk`) | `/en/contact` |

## SEO altyapısı

- Her sayfada benzersiz `title` / `description`, `canonical`, `hreflang` (tr, en, x-default), Open Graph + Twitter kartı
- Yapısal veri (JSON-LD): HVACBusiness (firma), WebSite, BreadcrumbList, Service + OfferCatalog, FAQPage, CollectionPage, ContactPage
- `sitemap.xml` (hreflang dahil), `robots.txt`, `site.webmanifest`, 404 sayfası (noindex), `_redirects`
- Görsellerde `width/height`, `srcset`, lazy-load; fontlar yerel (Google'a istek yok); temiz URL'ler
- Başlıklar nokta ile bitmez (build sırasında otomatik temizlenir)

Alan adları bağlandıktan sonra yapılacaklar:
1. Google Search Console'a iki alan adını da ekleyin (doğrulama TXT kaydı Cloudflare DNS'e), `https://www.bsmmekanik.com/sitemap.xml` gönderin.
2. Google İşletme Profili (Google Maps kaydı) açın; adres/telefon sitedekiyle birebir aynı olsun, web sitesi olarak www.bsmmekanik.com yazın.
3. Cloudflare panelinden Web Analytics'i açın (çerezsiz ziyaretçi istatistiği).

## Görseller

- **Referans görselleri** (`public/assets/img/ref/`): Firmanın referans listesindeki (Excel) görseller.
- **Temsili görseller**: Aşağıdaki 6 projenin listede görseli olmadığı için yapı türüne uygun Unsplash
  görselleri kullanıldı. Gerçek proje fotoğrafları geldiğinde aynı dosya adıyla değiştirilmeli:
  `besiktas-carsisi`, `nil-kuyumculuk`, `ozbarak-otel`, `arcelik-ersan`, `airties-ofis`, `cokertme-evi` (.webp)
- **Referans listesi**: 2020–2021 ve sonrası projeler (firma revizyonu); Robert Koleji onay sürecinde olduğu için listede yok.
- **Wikimedia Commons** (CC BY-SA 4.0, künyesi referanslar sayfasında):
  `ozyegin.webp` — Özyeğin University Campus, Bo yaser
- **Hizmet görselleri**: [Unsplash](https://unsplash.com/license)
- **Kurumsal fotoğraf** (`hizmet/ekip.webp`): [Pixabay](https://pixabay.com/service/license-summary/) #3979490 (kırpılmış)
- **Videolar**: [Pexels](https://www.pexels.com/license/) — `hero.mp4` (#34775814), `tesisat.mp4` (#30243437)
- **Logo**: Firmanın logo dosyasından vektöre çevrildi (`src/icons.py`, `assets/img/logo-mark.svg`).

## Teklif formu

Form, `/api/teklif` adresine gönderilir; Caddy bunu sunucudaki form alıcıya (`deploy/form-server/server.js`,
127.0.0.1:8787, bağımlılıksız Node.js) yönlendirir. Alıcı mesajı Google Workspace SMTP ile (gönderen:
Nesak Yazılım hesabı) `mert@bsmmechanical.com` adresine e-posta olarak iletir; e-postayı yanıtlamak doğrudan
formu dolduran kişiye gider. Koruma: gizli tuzak alanı, yalnızca kendi alan adlarından gelen istekler,
IP başına 10 dakikada 5 gönderim, alan uzunluk sınırları, e-posta başlığına satır sonu enjeksiyonu engeli.

Form alıcıya ulaşılamazsa (kurulmamış/kapalı) site, ziyaretçinin e-posta uygulamasını doldurulmuş olarak açar;
mesaj kaybolmaz.

Kurulum (Windows sunucu, Yönetici PowerShell; uygulama şifresi sorulur, deneme e-postası gönderilir):

```powershell
powershell -ExecutionPolicy Bypass -File C:\bsmmekanik\deploy\setup-form.ps1
```

Ayarlar `C:\bsmmekanik-key\form.json` (yalnızca Yönetici/SYSTEM), kayıtlar `C:\bsmmekanik-key\form.log`.
WhatsApp düğmesi Mert'in cep numarasına bağlıdır (`content.py` → `whatsapp`).

## Yasal (KVKK, TTK 1524)

- `/kvkk` ve `/en/privacy`: KVKK Aydınlatma Metni (veri sorumlusu, veri kategorileri, amaçlar, hukuki sebepler,
  yurt içi/yurt dışı aktarım — e-posta altyapısı Google Workspace ve GoDaddy, saklama süreleri, çerezler, md. 11 hakları, başvuru).
  Metin `src/build.py` → `privacy_sections()`; güncelleme tarihi `PRIVACY_UPDATED`.
- Form onay kutusu: "Aydınlatma Metni’ni okudum" (açık rıza ile birleştirilmez).
- Site çerez kullanmaz; iletişim sayfasındaki Google Haritası yalnızca "Haritayı göster" ile yüklenir.
- Form alıcının kayıtlarında (`form.log`) e-posta ve IP adresleri maskelenir.
- **Bilgi Toplumu Hizmetleri (TTK md. 1524):** `src/content.py` → `trade_registry`, `mersis`, `tax_office`, `tax_no`.
  Doldurulunca footer'da ve KVKK sayfasında otomatik görünür. Sicil, MERSİS ve vergi no girildi; vergi dairesi adı bekleniyor.
- Öneri: metinlerin bir avukat tarafından gözden geçirilmesi; firma ile barındırma sağlayıcısı arasında veri işleme sözleşmesi.

## Kendi sunucunda (VDS) yayın

`deploy/` klasörü:
- `setup-server.sh` — Ubuntu/Debian için tek komutla kurulum (Caddy varsa ona eklenir, yoksa nginx + Let's Encrypt), siteyi GitHub'dan çekme ve 5 dakikada bir otomatik güncelleme.
- `setup-windows.ps1` — Windows sunucuda çalışan Caddy için aynı kurulum (Git, deploy key, Caddyfile import, Görev Zamanlayıcı ile güncelleme).
- `bsmmekanik.caddy` / `bsmmekanik-windows.caddy` — Caddy site ayarı (Linux / Windows yolları).
- `nginx.conf` — temiz URL'ler, 404, www yönlendirmesi, önbellek, demo adresinde `noindex`.
- `.htaccess` — Apache kullanılan sunucular için aynı kurallar.

Windows (Yönetici PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File .\setup-windows.ps1              # demo
powershell -ExecutionPolicy Bypass -File .\setup-windows.ps1 -Mode domains # alan adları yönlendikten sonra
```

```bash
curl -fsSL https://raw.githubusercontent.com/emremuslu42-hub/recep-berk-can/claude/bold-edison-kwvvmm/deploy/setup-server.sh -o setup-server.sh
bash setup-server.sh demo      # bsmmekanik.nesakyazilim.com
bash setup-server.sh domains   # alan adları sunucuyu gösterdikten sonra
```

Alan adları için GoDaddy'de girilecek kayıtlar (her iki domainde; MX/TXT kayıtlarına dokunulmaz):

| Tür | Ad | Değer |
|---|---|---|
| A | `@` | VDS IP adresi |
| A | `www` | VDS IP adresi |
