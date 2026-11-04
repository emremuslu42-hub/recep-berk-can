"""Site içeriği (TR/EN). Metinleri buradan düzenleyip `python3 src/build.py` çalıştırın."""

COMPANY = {
    "short": "BSM Mekanik",
    "legal": "BSM Mekanik Mühendislik İnşaat Sanayi ve Ticaret Limited Şirketi",
    "founded": 2021,
    "address": "Altıntepe Mah. İstasyon Yolu Sok. No:3/1",
    "city": "Maltepe / İstanbul",
    "office_phone": "+90 (216) 706 14 01",
    "office_tel": "+902167061401",
    "people": [
        {"name": "Mert BALCI", "email": "mert@bsmmechanical.com", "phone": "+90 546 825 80 35", "tel": "+905468258035"},
    ],
    "whatsapp": "905468258035",
    "domain_tr": "https://www.bsmmekanik.com",
    "domain_en": "https://www.bsmmechanical.com",
    "map_query": "Altıntepe Mah. İstasyon Yolu Sok. No:3 Maltepe İstanbul",
}

# ---------------------------------------------------------------- Hizmetler
SERVICES = [
    {
        "key": "mekanik", "slug": {"tr": "mekanik-tesisat", "en": "mechanical-installation"}, "detail": {"tr": "Sıhhi tesisattan teknolojik su hatlarına kadar tüm boru tesisatlarını; malzeme seçimi, hidrolik hesaplar ve yapının kullanım senaryosu doğrultusunda planlıyoruz. Mevcut binalarda ise işletmeyi aksatmadan revizyon ve iyileştirme çalışmaları yürütüyoruz.", "en": "Every pipework system we deliver, from plumbing to process water, is planned around material selection, hydraulic calculations and how the building will actually be used. In occupied buildings, we carry out retrofits and upgrades with minimal disruption to day-to-day operations."}, "icon": "pipe", "img": "mekanik-tesisat",
        "tr": {
            "name": "Mekanik Tesisat",
            "short": "Sıhhi tesisat, temiz ve pis su, teknolojik su sistemleri ile montaj ve revizyon işleri.",
            "intro": "Konut, ticari yapılar ve endüstriyel tesislerin ihtiyaçlarına yönelik mekanik tesisat sistemlerinin projelendirme, tedarik, montaj ve uygulama hizmetlerini sunuyoruz.",
            "items": ["Genel mekanik tesisat uygulamaları", "Sıhhi tesisat sistemleri", "Temiz su ve pis su tesisatları", "Teknolojik su tesisatları", "Mekanik tesisat montaj ve revizyon işleri"],
        },
        "en": {
            "name": "Mechanical Installations",
            "short": "Plumbing, domestic water and drainage, process water systems, new installations and retrofits.",
            "intro": "We design, procure, install and commission mechanical systems for residential, commercial and industrial buildings.",
            "items": ["General mechanical installations", "Plumbing systems", "Domestic water and drainage", "Process water systems", "Mechanical installation and retrofit works"],
        },
    },
    {
        "key": "yangin", "slug": {"tr": "yangin-sondurme-sistemleri", "en": "fire-protection-systems"}, "detail": {"tr": "Sprinkler ve hidrant hatlarından yangın pompa dairelerine, algılama ve anons sistemlerine kadar tüm yangın güvenliği altyapısını yapının risk sınıfına ve yönetmeliklere uygun şekilde projelendirip uyguluyoruz. Fabrika, depo, otel, okul ve ofis gibi farklı yapı türlerinde sulu, kuru tip ve sprinkler sistemlerinde deneyime sahibiz.", "en": "We design and install complete fire safety systems, from sprinkler and hydrant mains to fire pump rooms, detection and voice alarm, matched to each building's hazard classification and current regulations. Our experience covers wet, dry and sprinkler systems in factories, warehouses, hotels, schools and offices."}, "icon": "flame", "img": "yangin",
        "tr": {
            "name": "Yangın Söndürme Sistemleri",
            "short": "Sprinkler, sulu ve kuru tip söndürme, yangın pompaları, algılama ve anons sistemleri.",
            "intro": "Yapıların ve endüstriyel tesislerin yangın güvenliğini sağlamak amacıyla ulusal ve uluslararası standartlara uygun yangın söndürme, algılama ve ihbar sistemleri çözümleri geliştiriyoruz.",
            "items": ["Yangın söndürme tesisatı", "Sulu ve kuru tip yangın sistemleri", "Sprinkler söndürme sistemleri", "Yangın pompa sistemleri", "Yangın algılama sistemleri", "Sesli yangın ihbar ve anons sistemleri"],
        },
        "en": {
            "name": "Fire Protection Systems",
            "short": "Automatic sprinklers, wet and dry suppression, fire pump sets, fire detection and voice alarm.",
            "intro": "We engineer fire suppression, detection and alarm systems to national and international standards, protecting people and assets in buildings and industrial facilities.",
            "items": ["Fire suppression pipework", "Wet and dry fire suppression systems", "Automatic sprinkler systems", "Fire pump sets", "Fire detection systems", "Voice alarm and evacuation systems"],
        },
    },
    {
        "key": "hvac", "slug": {"tr": "hvac-iklimlendirme", "en": "hvac-air-conditioning"}, "detail": {"tr": "Isı kaybı-kazancı hesaplarından cihaz seçimine, VRF/VRV sistemlerinden kazan dairelerine ve yerden ısıtmaya kadar iklimlendirme sistemlerini enerji verimliliğini ön planda tutarak tasarlıyor ve devreye alıyoruz. Konut, otel, ofis, eğitim ve endüstriyel yapılarda konforu ve işletme maliyetini birlikte gözetiyoruz.", "en": "From heat load calculations and plant selection to VRF/VRV systems, boiler plant rooms and underfloor heating, we design and commission HVAC systems with energy efficiency built in. Across homes, hotels, offices, schools and industrial buildings, we strike the right balance between comfort and running costs."}, "icon": "climate", "img": "hvac",
        "tr": {
            "name": "HVAC ve İklimlendirme",
            "short": "Isıtma, soğutma, VRF/VRV klima sistemleri, kazan daireleri ve yerden ısıtma.",
            "intro": "Yaşam ve çalışma alanlarında ideal iç ortam koşullarını sağlamak amacıyla ısıtma, soğutma ve iklimlendirme sistemlerinin projelendirme ve uygulama süreçlerini gerçekleştiriyoruz.",
            "items": ["Isıtma sistemleri", "Soğutma sistemleri", "VRF/VRV klima sistemleri", "Klima tesisatı ve uygulamaları", "Kazan dairesi sistemleri", "Yerden ısıtma sistemleri"],
        },
        "en": {
            "name": "HVAC & Air Conditioning",
            "short": "Heating, cooling, VRF/VRV air conditioning, boiler plant rooms and underfloor heating.",
            "intro": "We design and deliver heating, cooling and air conditioning systems that keep living and working spaces comfortable all year round.",
            "items": ["Heating systems", "Cooling systems", "VRF/VRV air conditioning", "Air conditioning installation", "Boiler plant rooms", "Underfloor heating"],
        },
    },
    {
        "key": "havalandirma", "slug": {"tr": "havalandirma-sistemleri", "en": "ventilation-systems"}, "detail": {"tr": "Taze hava ihtiyacını, egzoz ve duman tahliye gereksinimlerini yapının kullanımına göre hesaplıyor; kanal tesisatını sessiz, verimli ve bakımı kolay olacak şekilde uyguluyoruz. Restoran mutfaklarından üretim tesislerine ve otoparklara kadar farklı alanlarda havalandırma çözümleri sunuyoruz.", "en": "We size fresh air, extract and smoke control requirements to suit each building's use, and install ductwork that is quiet, efficient and easy to maintain. Our ventilation work spans everything from commercial kitchens to production facilities and car parks."}, "icon": "fan", "img": "havalandirma",
        "tr": {
            "name": "Havalandırma Sistemleri",
            "short": "Mekanik havalandırma, kanal tesisatı, taze hava, egzoz ve duman tahliye sistemleri.",
            "intro": "Kapalı alanlarda sağlıklı hava kalitesini ve konfor koşullarını sağlamak için mekanik havalandırma, taze hava, egzoz ve duman tahliye sistemleri tasarlıyor ve uyguluyoruz.",
            "items": ["Mekanik havalandırma sistemleri", "Havalandırma kanal tesisatı", "Taze hava sistemleri", "Egzoz ve duman tahliye sistemleri"],
        },
        "en": {
            "name": "Ventilation Systems",
            "short": "Mechanical ventilation, ductwork, fresh air supply, extract and smoke control systems.",
            "intro": "We design and install mechanical ventilation, fresh air, extract and smoke control systems that deliver healthy indoor air and occupant comfort.",
            "items": ["Mechanical ventilation systems", "Ductwork installation", "Fresh air supply systems", "Extract and smoke control systems"],
        },
    },
    {
        "key": "proje", "slug": {"tr": "muhendislik-projelendirme", "en": "engineering-design"}, "detail": {"tr": "Mekanik projeleri, mimari ve diğer disiplinlerle koordineli şekilde hazırlıyor; kapasite ve ihtiyaç analizleriyle doğru sistem seçimini yapıyoruz. Kontrollük ve teknik danışmanlık hizmetlerimizle, uygulamanın projeye ve standartlara uygun ilerlemesini güvence altına alıyoruz.", "en": "We develop mechanical designs in close coordination with the architect and other disciplines, using load and capacity analysis to select the right systems. Through site supervision and technical consultancy, we make sure the installation follows the design and complies with the relevant standards."}, "icon": "blueprint", "img": "projelendirme",
        "tr": {
            "name": "Mühendislik ve Projelendirme",
            "short": "Mekanik projelendirme, revizyonlar, kapasite analizleri ve teknik danışmanlık.",
            "intro": "Proje ihtiyaçlarını teknik açıdan değerlendirerek mekanik tesisat projelerinin hazırlanması, geliştirilmesi ve uygulama süreçlerinin mühendislik esaslarına uygun şekilde yürütülmesini sağlıyoruz.",
            "items": ["Mekanik tesisat projelendirme", "Mekanik proje revizyonları", "Mühendislik ve teknik danışmanlık", "Sistem kapasite ve ihtiyaç analizleri", "Proje koordinasyonu ve teknik yönetim"],
        },
        "en": {
            "name": "Engineering & Design",
            "short": "Mechanical services design, design revisions, load calculations and technical consultancy.",
            "intro": "We assess each project's technical requirements and take the mechanical design from concept through to construction, grounded in sound engineering principles.",
            "items": ["Mechanical services design", "Design revisions", "Engineering and technical consultancy", "Load and capacity calculations", "Project coordination and technical management"],
        },
    },
    {
        "key": "taahhut", "slug": {"tr": "mekanik-taahhut-anahtar-teslim", "en": "contracting-turnkey"}, "detail": {"tr": "Anahtar teslim projelerde projelendirme, malzeme temini, montaj, test ve devreye alma süreçlerinin tamamını tek sözleşme ve tek muhatapla yönetiyoruz. Bu yaklaşım; koordinasyon kayıplarını azaltır, iş programına uyumu ve maliyet kontrolünü kolaylaştırır.", "en": "On turnkey projects, we deliver design, procurement, installation, testing and commissioning under a single contract and a single point of contact. Fewer interfaces mean fewer coordination gaps, and a project that stays on programme and on budget."}, "icon": "key", "img": "taahhut",
        "tr": {
            "name": "Mekanik Taahhüt ve Anahtar Teslim",
            "short": "Projelendirmeden malzeme temini ve montaja kadar anahtar teslim proje yönetimi.",
            "intro": "Küçük ve büyük ölçekli projelerde mekanik tesisat işlerini projelendirmeden uygulamaya kadar yönetiyor; mekanik taahhüt ve anahtar teslim proje çözümleri sunuyoruz.",
            "items": ["Mekanik tesisat taahhüt işleri", "Anahtar teslim mekanik tesisat projeleri", "Endüstriyel tesis uygulamaları", "Ticari ve konut projeleri", "Projelendirme, malzeme temini ve montaj süreçlerinin yönetimi"],
        },
        "en": {
            "name": "Mechanical Contracting & Turnkey",
            "short": "Complete mechanical packages, from design and procurement through to installation.",
            "intro": "On projects large and small, we take mechanical works from design through to completion, either as mechanical contractor or on a fully turnkey basis.",
            "items": ["Mechanical contracting", "Turnkey mechanical packages", "Industrial installations", "Commercial and residential projects", "Design, procurement and installation management"],
        },
    },
    {
        "key": "elektrik", "slug": {"tr": "elektrik-otomasyon", "en": "electrical-automation"}, "detail": {"tr": "Mekanik sistemlerin verimli ve güvenli çalışması için gerekli elektrik tesisatı ve otomasyon altyapısını, alanında uzman çözüm ortaklarımızla birlikte projelendiriyor ve uyguluyoruz. Böylece mekanik ve elektrik işleri tek koordinasyon altında, uyumlu biçimde ilerler.", "en": "Together with our specialist partners, we design and install the power and controls infrastructure that mechanical systems need to run safely and efficiently, keeping mechanical and electrical works aligned under one coordinated programme."}, "icon": "bolt", "img": "elektrik",
        "tr": {
            "name": "Elektrik ve Otomasyon",
            "short": "Mekanik sistemlerle entegre elektrik tesisatı ve otomasyon çözümleri.",
            "intro": "Mekanik sistemlerle entegre çalışan elektrik ve otomasyon ihtiyaçlarına, alanında uzman çözüm ortaklarımız aracılığıyla kapsamlı çözümler sağlıyoruz.",
            "items": ["Elektrik tesisatı uygulamaları", "Elektrik proje ve uygulama koordinasyonu", "Mekanik sistem otomasyonu", "Çözüm ortaklarımız aracılığıyla elektrik ve otomasyon işleri"],
        },
        "en": {
            "name": "Electrical & Controls",
            "short": "Electrical installation and building controls, fully integrated with mechanical systems.",
            "intro": "Working with specialist partners, we deliver the electrical and controls packages that mechanical systems depend on.",
            "items": ["Electrical installation", "Electrical design and site coordination", "Controls and automation for mechanical systems", "Electrical and controls works through specialist partners"],
        },
    },
]

# ---------------------------------------------------------------- İş kalemleri (referanslar)
# anahtar: (TR, EN, hizmet etiketleri)
WORK = {
    "isitma_sogutma": ("Isıtma-soğutma sistemi kurulumu", "Heating and cooling system installation", ["hvac"]),
    "isitma_sogutma_tes": ("Isıtma-soğutma tesisatı", "Heating and cooling installation", ["hvac"]),
    "yangin": ("Yangın tesisatı işleri", "Fire suppression installation", ["yangin"]),
    "sulu_yangin": ("Siyah boru ile sulu yangın tesisatı", "Wet fire suppression pipework (black steel)", ["yangin"]),
    "sulu_yangin2": ("Sulu yangın tesisatı işleri", "Wet fire suppression installation", ["yangin"]),
    "kuru_yangin": ("Kuru tip yangın tesisatı", "Dry fire suppression system", ["yangin"]),
    "sprinkler": ("Sprinkler tesisatı işleri", "Sprinkler system installation", ["yangin"]),
    "algilama": ("Yangın algılama ve sesli anons tesisatı", "Fire detection and voice alarm system", ["yangin", "elektrik"]),
    "havalandirma": ("Havalandırma tesisatı işleri", "Ventilation and ductwork", ["havalandirma"]),
    "vrf": ("VRF tesisatı işleri", "VRF system installation", ["hvac"]),
    "teknolojik_su": ("Teknolojik su sistemleri", "Process water systems", ["mekanik"]),
    "sihhi": ("Sıhhi tesisat işleri", "Plumbing works", ["mekanik"]),
    "sihhi_pprc": ("PPRC ve PVC boru ile sıhhi tesisat", "Plumbing in PP-R and PVC pipework", ["mekanik"]),
    "dogalgaz": ("Doğalgaz tesisatı işleri", "Natural gas installation", ["mekanik"]),
    "mekanik_proje": ("Mekanik proje hizmeti", "Mechanical design services", ["proje"]),
    "em_proje": ("Elektrik-mekanik proje hizmeti", "Electrical and mechanical design services", ["proje", "elektrik"]),
    "elektrik": ("Elektrik işleri", "Electrical works", ["elektrik"]),
    "anahtar_klinik": ("Anahtar teslim diş kliniği yapımı", "Turnkey dental clinic construction", ["taahhut"]),
    "anahtar_tesis": ("Anahtar teslim tesis yapımı", "Turnkey facility construction", ["taahhut"]),
    "kontrolluk": ("Mekanik tesisat kontrollük ve danışmanlık hizmeti", "Mechanical site supervision and consultancy", ["proje"]),
    "ges_fizibilite": ("Kapasite tayini, fizibilite raporları ve çağrı mektubu süreci", "Capacity sizing, feasibility studies and grid connection application", ["proje"]),
    "ges_ihale": ("İhale ve proje yönetim süreçlerinin planlanması", "Tender and project management planning", ["proje"]),
    "sosyal_tesis": ("Sosyal tesis mekanik tesisat işleri", "Mechanical works for the clubhouse and amenities", ["mekanik", "taahhut"]),
    "mek_revizyon": ("Mekanik tesisat revizyon işleri", "Mechanical system retrofit", ["mekanik"]),
    "elk_revizyon": ("Elektrik tesisatı revizyon işleri", "Electrical system retrofit", ["elektrik"]),
    "insai": ("İnşai işler", "Construction works", ["taahhut"]),
    "kazan": ("Kazan dairesi kurulumu", "Boiler plant room installation", ["hvac"]),
    "lng": ("LNG tank soğutma sistemleri", "LNG tank cooling systems", ["mekanik"]),
    "klima_yerden": ("Klima, yerden ısıtma, soğutma ve havalandırma tesisatları", "Air conditioning, underfloor heating, cooling and ventilation", ["hvac", "havalandirma"]),
    "klima_isitma": ("Klima, ısıtma, soğutma ve havalandırma tesisatları", "Air conditioning, heating, cooling and ventilation", ["hvac", "havalandirma"]),
    "yangin_sprinkler": ("Yangın ve sprinkler tesisatları", "Fire protection and sprinkler systems", ["yangin"]),
    "pis_temiz": ("Pis su ve temiz su tesisatları", "Domestic water and drainage", ["mekanik"]),
    "otomasyon": ("Otomasyon işleri", "Controls and automation", ["elektrik"]),
}

# ---------------------------------------------------------------- Referanslar (Excel listesi; 2020–2021 ve sonrası)
# (görsel, görsel türü, kategori, müşteri, proje TR, proje EN, iş kalemleri, alan m², yer, yıl TR, yıl EN)
# görsel türü: "photo" = projenin kendi görseli, "logo" = firma logosu,
#              "stock" = temsili görsel (proje görseli geldiğinde değiştirilmeli), "wiki" = Wikimedia Commons
REFERENCES = [
    ("besiktas-carsisi", "stock", "ticari", "", "Büyük Beşiktaş Çarşısı", "Grand Beşiktaş Bazaar", ["mekanik_proje", "yangin"], 3000, "İstanbul - Beşiktaş", "2026", "2026"),
    ("nil-kuyumculuk", "stock", "endustri", "", "Nil Kuyumculuk Atölyesi", "Nil Jewellery Workshop", ["isitma_sogutma", "yangin", "havalandirma", "vrf", "teknolojik_su"], 900, "İstanbul - Yenibosna", "2026", "2026"),
    ("ozbarak-otel", "stock", "otel", "", "Özbarak 50 Odalı Otel", "Özbarak 50-Room Hotel", ["isitma_sogutma", "yangin", "havalandirma", "vrf"], 3500, "İstanbul - Samandıra", "2026", "2026"),
    ("arcelik-ersan", "stock", "endustri", "", "Arçelik Ersan Deposu", "Arçelik Ersan Warehouse", ["yangin"], 20000, "Kocaeli - Gebze", "2026", "2026"),
    ("ozyegin", "wiki", "egitim", "", "Özyeğin Üniversitesi", "Özyeğin University", ["yangin", "havalandirma", "vrf"], 300, "İstanbul - Çekmeköy", "2026", "2026"),
    ("airties-ofis", "stock", "ofis", "Bilişim Vadisi", "Airties Ofisi", "Airties Office", ["isitma_sogutma", "yangin", "havalandirma", "vrf", "sihhi"], 1000, "İstanbul - Sarıyer", "2026", "2026"),
    ("cokertme-evi", "stock", "konut", "", "Çökertme S.D. Evi", "Çökertme S.D. Residence", ["isitma_sogutma", "havalandirma", "vrf", "sihhi"], 600, "Muğla - Bodrum / Milas", "2026", "2026"),
    ("teknik-conta-silivri", "photo", "endustri", "Teknik Conta Kauçuk", "Teknik Conta Silivri Fabrikası", "Teknik Conta Silivri Factory", ["em_proje", "sulu_yangin", "havalandirma", "vrf", "elektrik"], 5000, "İstanbul - Silivri", "Devam ediyor", "Ongoing"),
    ("corum-gures", "photo", "egitim", "", "Çorum Güreş Eğitim Merkezi", "Çorum Wrestling Training Centre", ["havalandirma", "vrf"], 8000, "Çorum", "2025", "2025"),
    ("lua-dent", "photo", "saglik", "", "Kurtköy LUA Dent Diş Kliniği", "LUA Dent Dental Clinic, Kurtköy", ["anahtar_klinik"], 420, "İstanbul - Kurtköy", "2025", "2025"),
    ("kizilkayalar", "logo", "ticari", "Kızılkayalar", "Kızılkayalar Caddebostan Şubesi", "Kızılkayalar Caddebostan Branch", ["sihhi_pprc", "havalandirma", "vrf", "dogalgaz"], 600, "İstanbul - Kadıköy", "2025", "2025"),
    ("model-kuyumculuk", "photo", "endustri", "", "Model Kuyumculuk Atölyesi", "Model Jewellery Workshop", ["em_proje", "sulu_yangin", "havalandirma", "vrf", "elektrik"], 500, "İstanbul - Başakşehir", "2025", "2025"),
    ("nevsehir-ges", "photo", "enerji", "", "Nevşehir Arazi Tipi GES Projesi (1,4 MW)", "Nevşehir Ground-Mounted Solar Plant (1.4 MW)", ["ges_fizibilite", "ges_ihale"], 21000, "Nevşehir - Ürgüp", "2022–2023", "2022–2023"),
    ("hanwha", "logo", "ofis", "Hanwha Aerospace", "Hanwha Tuzla Showroom ve İdari Binası", "Hanwha Tuzla Showroom and Administrative Building", ["em_proje", "sulu_yangin", "havalandirma", "vrf", "elektrik"], 1200, "İstanbul - Tuzla", "2022–2023", "2022–2023"),
    ("lenza", "photo", "ticari", "TUBA Mimarlık", "Lenza Balık Restoranı", "Lenza Fish Restaurant", ["sihhi_pprc", "sulu_yangin", "havalandirma", "vrf", "dogalgaz"], 600, "İstanbul - Tuzla", "2021–2022", "2021–2022"),
    ("mene-biopark", "photo", "endustri", "Mene Health Group A.Ş.", "Çayırova Biopark Tesisi", "Çayırova Biopark Facility", ["anahtar_tesis"], 8000, "Kocaeli - Çayırova", "2020–2021", "2020–2021"),
]

FEATURED = ["teknik-conta-silivri", "mene-biopark", "ozyegin", "lua-dent", "model-kuyumculuk", "lenza"]

# Ana sayfadaki "referans listemizden" bölümü
HOME_REFS = ["arcelik-ersan", "hanwha", "airties-ofis", "ozbarak-otel", "kizilkayalar", "corum-gures"]

CATEGORIES = {
    "konut": ("Konut & Villa", "Residential & Villas", "home"),
    "ticari": ("Ticari & Restoran", "Retail & Restaurants", "store"),
    "endustri": ("Endüstriyel Tesis", "Industrial Facilities", "factory"),
    "egitim": ("Eğitim & Spor", "Education & Sports", "school"),
    "saglik": ("Sağlık", "Healthcare", "health"),
    "otel": ("Otel & Turizm", "Hotels & Hospitality", "hotel"),
    "ofis": ("Ofis & İdari Bina", "Offices & Administrative", "office"),
    "enerji": ("Enerji", "Energy", "sun"),
    "dini": ("Kamu & Dini Yapı", "Public & Religious Buildings", "dome"),
}

CLIENT_STRIP = ["Özyeğin Üniversitesi", "Arçelik", "Hanwha Aerospace", "Airties", "Mene Health", "Teknik Conta", "Kızılkayalar", "Büyük Beşiktaş Çarşısı", "TUBA Mimarlık", "Bilişim Vadisi"]
