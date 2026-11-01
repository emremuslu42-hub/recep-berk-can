# BSM Mekanik — Kurumsal Web Sitesi

BSM Mekanik Mühendislik İnşaat San. ve Tic. Ltd. Şti. için iki dilli (TR/EN) statik kurumsal site.
Cloudflare Workers (statik asset) üzerinde yayınlanır; derleme sunucusu gerektirmez.

- Türkçe: `https://bsmmekanik.com/` (kök)
- İngilizce: `https://bsmmechanical.com/en/`
- İki alan adı da sitenin tamamını açar; dil seçimi sağ üstteki TR/EN düğmesiyle yapılır.

## Klasör yapısı

```
src/content.py   Tüm içerik: firma bilgileri, hizmetler, 31 referans proje (TR/EN)
src/build.py     Sayfa şablonları; public/ altındaki HTML dosyalarını üretir
src/icons.py     SVG ikonlar ve vektör logo
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

## Görseller

- **Referans görselleri** (`public/assets/img/ref/`): Firmanın referans listesindeki (Excel) görseller.
- **Temsili görseller**: Aşağıdaki 6 projenin listede görseli olmadığı için yapı türüne uygun Unsplash
  görselleri kullanıldı. Gerçek proje fotoğrafları geldiğinde aynı dosya adıyla değiştirilmeli:
  `besiktas-carsisi`, `nil-kuyumculuk`, `ozbarak-otel`, `arcelik-ersan`, `airties-ofis`, `cokertme-evi` (.webp)
- **Wikimedia Commons** (CC BY-SA 4.0, künyesi referanslar sayfasında):
  `robert-koleji.webp` — Mitchell Hall, Yaguzi · `ozyegin.webp` — Özyeğin University Campus, Bo yaser
- **Hizmet görselleri**: [Unsplash](https://unsplash.com/license)
- **Videolar**: [Pexels](https://www.pexels.com/license/) — `hero.mp4` (#34775814), `tesisat.mp4` (#30243437)
- **Logo**: Firmanın logo dosyasından vektöre çevrildi (`src/icons.py`, `assets/img/logo-mark.svg`).

## Formlar

İletişim formu ziyaretçinin e-posta uygulamasını mert@ ve berk@ adreslerine doldurulmuş olarak açar.
İleride doğrudan gönderim istenirse (Formspree, Cloudflare Worker + e-posta vb.) bağlanabilir.
WhatsApp düğmesi Mert'in cep numarasına bağlıdır (`content.py` → `whatsapp`).
