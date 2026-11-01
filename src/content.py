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
        {"name": "Mert", "email": "mert@bsmmechanical.com", "phone": "+90 546 825 80 35", "tel": "+905468258035"},
        {"name": "Berk", "email": "berk@bsmmechanical.com", "phone": "+90 553 930 67 89", "tel": "+905539306789"},
    ],
    "whatsapp": "905468258035",
    "domain_tr": "https://bsmmekanik.com",
    "domain_en": "https://bsmmechanical.com",
    "map_query": "Altıntepe Mah. İstasyon Yolu Sok. No:3 Maltepe İstanbul",
}

# ---------------------------------------------------------------- Hizmetler
SERVICES = [
    {
        "key": "mekanik", "icon": "pipe", "img": "mekanik-tesisat",
        "tr": {
            "name": "Mekanik Tesisat",
            "short": "Sıhhi tesisat, temiz ve pis su, teknolojik su sistemleri ile montaj ve revizyon işleri.",
            "intro": "Konut, ticari yapılar ve endüstriyel tesislerin ihtiyaçlarına yönelik mekanik tesisat sistemlerinin projelendirme, tedarik, montaj ve uygulama hizmetlerini sunuyoruz.",
            "items": ["Genel mekanik tesisat uygulamaları", "Sıhhi tesisat sistemleri", "Temiz su ve pis su tesisatları", "Teknolojik su tesisatları", "Mekanik tesisat montaj ve revizyon işleri"],
        },
        "en": {
            "name": "Mechanical Installation",
            "short": "Plumbing, clean and waste water, process water systems, installation and retrofit works.",
            "intro": "We provide design, procurement, installation and commissioning of mechanical systems for residential, commercial and industrial facilities.",
            "items": ["General mechanical installations", "Plumbing systems", "Clean and waste water systems", "Process water systems", "Mechanical installation and retrofit works"],
        },
    },
    {
        "key": "yangin", "icon": "flame", "img": "yangin",
        "tr": {
            "name": "Yangın Söndürme Sistemleri",
            "short": "Sprinkler, sulu ve kuru tip söndürme, yangın pompaları, algılama ve anons sistemleri.",
            "intro": "Yapıların ve endüstriyel tesislerin yangın güvenliğini sağlamak amacıyla ulusal ve uluslararası standartlara uygun yangın söndürme, algılama ve ihbar sistemleri çözümleri geliştiriyoruz.",
            "items": ["Yangın söndürme tesisatı", "Sulu ve kuru tip yangın sistemleri", "Sprinkler söndürme sistemleri", "Yangın pompa sistemleri", "Yangın algılama sistemleri", "Sesli yangın ihbar ve anons sistemleri"],
        },
        "en": {
            "name": "Fire Protection Systems",
            "short": "Sprinklers, wet and dry systems, fire pumps, detection and voice alarm systems.",
            "intro": "We deliver fire suppression, detection and alarm solutions in line with national and international standards to keep buildings and industrial facilities safe.",
            "items": ["Fire suppression piping", "Wet and dry type fire systems", "Sprinkler systems", "Fire pump systems", "Fire detection systems", "Voice alarm and evacuation systems"],
        },
    },
    {
        "key": "hvac", "icon": "climate", "img": "hvac",
        "tr": {
            "name": "HVAC ve İklimlendirme",
            "short": "Isıtma, soğutma, VRF/VRV klima sistemleri, kazan daireleri ve yerden ısıtma.",
            "intro": "Yaşam ve çalışma alanlarında ideal iç ortam koşullarını sağlamak amacıyla ısıtma, soğutma ve iklimlendirme sistemlerinin projelendirme ve uygulama süreçlerini gerçekleştiriyoruz.",
            "items": ["Isıtma sistemleri", "Soğutma sistemleri", "VRF/VRV klima sistemleri", "Klima tesisatı ve uygulamaları", "Kazan dairesi sistemleri", "Yerden ısıtma sistemleri"],
        },
        "en": {
            "name": "HVAC & Air Conditioning",
            "short": "Heating, cooling, VRF/VRV systems, boiler rooms and underfloor heating.",
            "intro": "We design and install heating, cooling and air-conditioning systems that create ideal indoor conditions in living and working spaces.",
            "items": ["Heating systems", "Cooling systems", "VRF/VRV air-conditioning", "Air-conditioning installations", "Boiler room systems", "Underfloor heating"],
        },
    },
    {
        "key": "havalandirma", "icon": "fan", "img": "havalandirma",
        "tr": {
            "name": "Havalandırma Sistemleri",
            "short": "Mekanik havalandırma, kanal tesisatı, taze hava, egzoz ve duman tahliye sistemleri.",
            "intro": "Kapalı alanlarda sağlıklı hava kalitesini ve konfor koşullarını sağlamak için mekanik havalandırma, taze hava, egzoz ve duman tahliye sistemleri tasarlıyor ve uyguluyoruz.",
            "items": ["Mekanik havalandırma sistemleri", "Havalandırma kanal tesisatı", "Taze hava sistemleri", "Egzoz ve duman tahliye sistemleri"],
        },
        "en": {
            "name": "Ventilation Systems",
            "short": "Mechanical ventilation, ductwork, fresh air, exhaust and smoke extraction systems.",
            "intro": "We design and install mechanical ventilation, fresh air, exhaust and smoke extraction systems for healthy air quality and comfort in enclosed spaces.",
            "items": ["Mechanical ventilation systems", "Ventilation ductwork", "Fresh air systems", "Exhaust and smoke extraction systems"],
        },
    },
    {
        "key": "proje", "icon": "blueprint", "img": "projelendirme",
        "tr": {
            "name": "Mühendislik ve Projelendirme",
            "short": "Mekanik projelendirme, revizyonlar, kapasite analizleri ve teknik danışmanlık.",
            "intro": "Proje ihtiyaçlarını teknik açıdan değerlendirerek mekanik tesisat projelerinin hazırlanması, geliştirilmesi ve uygulama süreçlerinin mühendislik esaslarına uygun şekilde yürütülmesini sağlıyoruz.",
            "items": ["Mekanik tesisat projelendirme", "Mekanik proje revizyonları", "Mühendislik ve teknik danışmanlık", "Sistem kapasite ve ihtiyaç analizleri", "Proje koordinasyonu ve teknik yönetim"],
        },
        "en": {
            "name": "Engineering & Design",
            "short": "Mechanical design, revisions, capacity analyses and technical consultancy.",
            "intro": "We assess each project's technical needs and prepare, develop and manage mechanical designs in accordance with sound engineering principles.",
            "items": ["Mechanical system design", "Mechanical design revisions", "Engineering and technical consultancy", "System capacity and demand analyses", "Project coordination and technical management"],
        },
    },
    {
        "key": "taahhut", "icon": "key", "img": "taahhut",
        "tr": {
            "name": "Mekanik Taahhüt ve Anahtar Teslim",
            "short": "Projelendirmeden malzeme temini ve montaja kadar anahtar teslim proje yönetimi.",
            "intro": "Küçük ve büyük ölçekli projelerde mekanik tesisat işlerini projelendirmeden uygulamaya kadar yönetiyor; mekanik taahhüt ve anahtar teslim proje çözümleri sunuyoruz.",
            "items": ["Mekanik tesisat taahhüt işleri", "Anahtar teslim mekanik tesisat projeleri", "Endüstriyel tesis uygulamaları", "Ticari ve konut projeleri", "Projelendirme, malzeme temini ve montaj süreçlerinin yönetimi"],
        },
        "en": {
            "name": "Contracting & Turnkey Projects",
            "short": "Turnkey project management from design through procurement and installation.",
            "intro": "From small to large-scale projects, we manage mechanical works from design to completion and deliver contracting and turnkey solutions.",
            "items": ["Mechanical contracting works", "Turnkey mechanical installation projects", "Industrial facility applications", "Commercial and residential projects", "Management of design, procurement and installation"],
        },
    },
    {
        "key": "elektrik", "icon": "bolt", "img": "elektrik",
        "tr": {
            "name": "Elektrik ve Otomasyon",
            "short": "Mekanik sistemlerle entegre elektrik tesisatı ve otomasyon çözümleri.",
            "intro": "Mekanik sistemlerle entegre çalışan elektrik ve otomasyon ihtiyaçlarına, alanında uzman çözüm ortaklarımız aracılığıyla kapsamlı çözümler sağlıyoruz.",
            "items": ["Elektrik tesisatı uygulamaları", "Elektrik proje ve uygulama koordinasyonu", "Mekanik sistem otomasyonu", "Çözüm ortaklarımız aracılığıyla elektrik ve otomasyon işleri"],
        },
        "en": {
            "name": "Electrical & Automation",
            "short": "Electrical installation and automation integrated with mechanical systems.",
            "intro": "Through our expert solution partners, we provide comprehensive electrical and automation solutions that work hand in hand with mechanical systems.",
            "items": ["Electrical installation works", "Electrical design and site coordination", "Mechanical system automation", "Electrical and automation works via solution partners"],
        },
    },
]

# ---------------------------------------------------------------- İş kalemleri (referanslar)
# anahtar: (TR, EN, hizmet etiketleri)
WORK = {
    "isitma_sogutma": ("Isıtma soğutma sistemi kurulumu", "Heating and cooling system installation", ["hvac"]),
    "isitma_sogutma_tes": ("Isıtma soğutma tesisatı", "Heating and cooling installation", ["hvac"]),
    "yangin": ("Yangın tesisatı işleri", "Fire protection installation", ["yangin"]),
    "sulu_yangin": ("Siyah boru ile sulu yangın tesisatı", "Wet fire protection piping (black steel)", ["yangin"]),
    "sulu_yangin2": ("Sulu yangın tesisatı işleri", "Wet fire protection installation", ["yangin"]),
    "kuru_yangin": ("Kuru tip yangın tesisatı", "Dry-type fire protection system", ["yangin"]),
    "sprinkler": ("Sprinkler tesisatı işleri", "Sprinkler system installation", ["yangin"]),
    "algilama": ("Yangın algılama ve sesli anons tesisatı", "Fire detection and voice alarm system", ["yangin", "elektrik"]),
    "havalandirma": ("Havalandırma tesisatı işleri", "Ventilation installation", ["havalandirma"]),
    "vrf": ("VRF tesisatı işleri", "VRF system installation", ["hvac"]),
    "teknolojik_su": ("Teknolojik su sistemleri", "Process water systems", ["mekanik"]),
    "sihhi": ("Sıhhi tesisat işleri", "Plumbing works", ["mekanik"]),
    "sihhi_pprc": ("PPRC ve PVC boru ile sıhhi tesisat", "Plumbing with PP-R and PVC piping", ["mekanik"]),
    "dogalgaz": ("Doğalgaz tesisatı işleri", "Natural gas installation", ["mekanik"]),
    "mekanik_proje": ("Mekanik proje hizmeti", "Mechanical design services", ["proje"]),
    "em_proje": ("Elektrik-mekanik proje hizmeti", "Electrical and mechanical design services", ["proje", "elektrik"]),
    "elektrik": ("Elektrik işleri", "Electrical works", ["elektrik"]),
    "anahtar_klinik": ("Anahtar teslim diş kliniği yapımı", "Turnkey dental clinic construction", ["taahhut"]),
    "anahtar_tesis": ("Anahtar teslim tesis yapımı", "Turnkey facility construction", ["taahhut"]),
    "kontrolluk": ("Mekanik tesisat kontrollük ve danışmanlık hizmeti", "Mechanical works supervision and consultancy", ["proje"]),
    "ges_fizibilite": ("Kapasite tayini, fizibilite raporları ve çağrı mektubu süreci", "Capacity sizing, feasibility reports and grid application", ["proje"]),
    "ges_ihale": ("İhale ve proje yönetim süreçlerinin planlanması", "Tender and project management planning", ["proje"]),
    "sosyal_tesis": ("Sosyal tesis mekanik tesisat işleri", "Mechanical works for the social facility", ["mekanik", "taahhut"]),
    "mek_revizyon": ("Mekanik tesisat revizyon işleri", "Mechanical system retrofit", ["mekanik"]),
    "elk_revizyon": ("Elektrik tesisatı revizyon işleri", "Electrical system retrofit", ["elektrik"]),
    "insai": ("İnşai işler", "Construction works", ["taahhut"]),
    "kazan": ("Kazan dairesi kurulumu", "Boiler room installation", ["hvac"]),
    "lng": ("LNG tank soğutma sistemleri", "LNG tank cooling systems", ["mekanik"]),
    "klima_yerden": ("Klima, yerden ısıtma, soğutma ve havalandırma tesisatları", "Air-conditioning, underfloor heating, cooling and ventilation", ["hvac", "havalandirma"]),
    "klima_isitma": ("Klima, ısıtma, soğutma ve havalandırma tesisatları", "Air-conditioning, heating, cooling and ventilation", ["hvac", "havalandirma"]),
    "yangin_sprinkler": ("Yangın ve sprinkler tesisatları", "Fire protection and sprinkler systems", ["yangin"]),
    "pis_temiz": ("Pis su ve temiz su tesisatları", "Waste and clean water systems", ["mekanik"]),
    "otomasyon": ("Otomasyon işleri", "Automation works", ["elektrik"]),
}

# ---------------------------------------------------------------- Referanslar (Excel listesi, 2012–2026)
# (görsel, görsel türü, kategori, müşteri, proje TR, proje EN, iş kalemleri, alan m², yer, yıl TR, yıl EN)
# görsel türü: "photo" = projenin kendi görseli, "logo" = firma logosu,
#              "stock" = temsili görsel (proje görseli geldiğinde değiştirilmeli), "wiki" = Wikimedia Commons
REFERENCES = [
    ("robert-koleji", "wiki", "egitim", "", "Robert Koleji", "Robert College", ["isitma_sogutma", "yangin", "havalandirma", "vrf", "teknolojik_su"], 2400, "İstanbul - Beşiktaş", "2026", "2026"),
    ("besiktas-carsisi", "stock", "ticari", "", "Büyük Beşiktaş Çarşısı", "Grand Beşiktaş Bazaar", ["mekanik_proje", "yangin"], 3000, "İstanbul - Beşiktaş", "2026", "2026"),
    ("nil-kuyumculuk", "stock", "endustri", "", "Nil Kuyumculuk Atölye", "Nil Jewellery Workshop", ["isitma_sogutma", "yangin", "havalandirma", "vrf", "teknolojik_su"], 900, "İstanbul - Yenibosna", "2026", "2026"),
    ("ozbarak-otel", "stock", "otel", "", "Özbarak 50 Odalı Otel", "Özbarak 50-Room Hotel", ["isitma_sogutma", "yangin", "havalandirma", "vrf"], 3500, "İstanbul - Samandıra", "2026", "2026"),
    ("arcelik-ersan", "stock", "endustri", "", "Arçelik Ersan Depo", "Arçelik Ersan Warehouse", ["yangin"], 20000, "Kocaeli - Gebze", "2026", "2026"),
    ("ozyegin", "wiki", "egitim", "", "Özyeğin Üniversitesi", "Özyeğin University", ["yangin", "havalandirma", "vrf"], 300, "İstanbul - Çekmeköy", "2026", "2026"),
    ("airties-ofis", "stock", "ofis", "Bilişim Vadisi", "Airties Ofis", "Airties Office", ["isitma_sogutma", "yangin", "havalandirma", "vrf", "sihhi"], 1000, "İstanbul - Sarıyer", "2026", "2026"),
    ("cokertme-evi", "stock", "konut", "", "Çökertme S.D. Evi", "Çökertme S.D. Residence", ["isitma_sogutma", "havalandirma", "vrf", "sihhi"], 600, "Muğla - Bodrum / Milas", "2026", "2026"),
    ("teknik-conta-silivri", "photo", "endustri", "Teknik Conta Kauçuk", "Silivri Fabrika", "Silivri Factory", ["em_proje", "sulu_yangin", "havalandirma", "vrf", "elektrik"], 5000, "İstanbul - Silivri", "Devam ediyor", "Ongoing"),
    ("corum-gures", "photo", "egitim", "", "Çorum Güreş Eğitim Merkezi", "Çorum Wrestling Training Centre", ["havalandirma", "vrf"], 8000, "Çorum", "2025", "2025"),
    ("lua-dent", "photo", "saglik", "", "Kurtköy LUA Dent Diş Kliniği", "LUA Dent Dental Clinic, Kurtköy", ["anahtar_klinik"], 420, "İstanbul - Kurtköy", "2025", "2025"),
    ("kizilkayalar", "logo", "ticari", "Kızılkayalar", "Caddebostan Şubesi", "Caddebostan Branch", ["sihhi_pprc", "havalandirma", "vrf", "dogalgaz"], 600, "İstanbul - Kadıköy", "2025", "2025"),
    ("model-kuyumculuk", "photo", "endustri", "", "Model Kuyumculuk Atölye", "Model Jewellery Workshop", ["em_proje", "sulu_yangin", "havalandirma", "vrf", "elektrik"], 500, "İstanbul - Başakşehir", "2025", "2025"),
    ("nevsehir-ges", "photo", "enerji", "", "Nevşehir Arazi Tipi GES Projesi (1,4 MW)", "Nevşehir Ground-Mounted Solar Plant (1.4 MW)", ["ges_fizibilite", "ges_ihale"], 21000, "Nevşehir - Ürgüp", "2022–2023", "2022–2023"),
    ("hanwha", "logo", "ofis", "Hanwha Aerospace", "Tuzla Showroom ve İdari Bina", "Tuzla Showroom and Administrative Building", ["em_proje", "sulu_yangin", "havalandirma", "vrf", "elektrik"], 1200, "İstanbul - Tuzla", "2022–2023", "2022–2023"),
    ("lenza", "photo", "ticari", "TUBA Mimarlık", "Lenza Balık Restoranı", "Lenza Fish Restaurant", ["sihhi_pprc", "sulu_yangin", "havalandirma", "vrf", "dogalgaz"], 600, "İstanbul - Tuzla", "2021–2022", "2021–2022"),
    ("mene-biopark", "photo", "endustri", "Mene Health Group A.Ş.", "Çayırova Biopark Tesisi", "Çayırova Biopark Facility", ["anahtar_tesis"], 8000, "Kocaeli - Çayırova", "2020–2021", "2020–2021"),
    ("biltur", "photo", "endustri", "Biltur Catering", "Dudullu Yemek Üretim Tesisi", "Dudullu Food Production Facility", ["kontrolluk"], 4200, "İstanbul - Ümraniye", "2019", "2019"),
    ("bilfen", "photo", "egitim", "Bilfen Eğitim Kurumları A.Ş.", "Bilfen Maslak Kampüsü", "Bilfen Maslak Campus", ["kontrolluk"], 800, "İstanbul - Maslak", "2019", "2019"),
    ("zekeriyakoy-villa", "photo", "konut", "Habif Mimarlık", "Zekeriyaköy Villa Projesi", "Zekeriyaköy Villa Project", ["sihhi", "havalandirma", "isitma_sogutma_tes"], 1200, "İstanbul - Sarıyer", "2018", "2018"),
    ("kule-4", "photo", "konut", "Eser İnşaat", "Kule-4 Konut Projesi", "Kule-4 Residential Project", ["sihhi", "yangin", "havalandirma", "isitma_sogutma_tes"], 6000, "İstanbul - Kurtköy", "2017", "2017"),
    ("astorya-ngn", "photo", "ofis", "Yapı Stüdyo Mimarlık", "Astorya NGN Office", "Astorya NGN Office", ["sihhi", "havalandirma", "isitma_sogutma_tes"], 500, "İstanbul - Şişli", "2017", "2017"),
    ("atiye-residence", "photo", "konut", "HAS-DBN Yatırım Ortaklığı", "Atiye Residence", "Atiye Residence", ["sihhi", "yangin", "havalandirma", "isitma_sogutma_tes"], 14000, "İstanbul - Kağıthane", "2017", "2017"),
    ("kiler-referans", "photo", "konut", "Kiler GYO", "Referans Kartal", "Referans Kartal", ["sosyal_tesis"], 2000, "İstanbul - Kartal", "2016", "2016"),
    ("yapi-merkezi", "photo", "ofis", "Yapı Merkezi A.Ş.", "Yapı Merkezi Genel Merkez Binası", "Yapı Merkezi Headquarters", ["mek_revizyon", "elk_revizyon"], 7500, "İstanbul - Aksaray", "2016", "2016"),
    ("licus-otel", "photo", "otel", "Licus Otelcilik", "Licus Otel", "Licus Hotel", ["insai", "sihhi", "sulu_yangin2", "havalandirma", "isitma_sogutma_tes", "kazan"], 1500, "İstanbul - Aksaray", "2015", "2015"),
    ("sisecam-pasabahce", "photo", "endustri", "Şişecam A.Ş.", "Paşabahçe Büyükkarıştıran Fabrikası", "Paşabahçe Büyükkarıştıran Plant", ["kuru_yangin", "sprinkler", "algilama", "lng"], 50000, "Kırklareli", "2015", "2015"),
    ("skalion-otel", "photo", "otel", "Merşa Tekstil", "Skalion Otel", "Skalion Hotel", ["sihhi", "havalandirma", "isitma_sogutma_tes"], 200, "İstanbul - Kumkapı", "2014", "2014"),
    ("alsit-villa", "photo", "konut", "Yapı Stüdyo Mimarlık", "Alsit Villa", "Alsit Villa", ["sihhi", "havalandirma", "isitma_sogutma_tes"], 300, "İstanbul - Sarıyer", "2014", "2014"),
    ("gosb-camii", "photo", "dini", "GOSB", "GOSB Camii", "GOSB Mosque", ["klima_yerden", "yangin", "pis_temiz", "otomasyon"], 6000, "Kocaeli - Gebze", "2013", "2013"),
    ("sisecam-bilim", "photo", "ofis", "Şişecam A.Ş.", "Bilim ve Teknoloji Merkezi", "Science and Technology Centre", ["klima_isitma", "yangin_sprinkler", "pis_temiz", "otomasyon"], 30000, "Kocaeli - Gebze", "2012–2013", "2012–2013"),
]

FEATURED = ["sisecam-bilim", "sisecam-pasabahce", "atiye-residence", "teknik-conta-silivri", "zekeriyakoy-villa", "kiler-referans", "mene-biopark", "licus-otel"]

CATEGORIES = {
    "konut": ("Konut & Villa", "Residential & Villas", "home"),
    "ticari": ("Ticari & Restoran", "Retail & Restaurants", "store"),
    "endustri": ("Endüstriyel Tesis", "Industrial Facilities", "factory"),
    "egitim": ("Eğitim & Spor", "Education & Sports", "school"),
    "saglik": ("Sağlık", "Healthcare", "health"),
    "otel": ("Otel & Turizm", "Hotels & Hospitality", "hotel"),
    "ofis": ("Ofis & İdari Bina", "Offices & Admin", "office"),
    "enerji": ("Enerji", "Energy", "sun"),
    "dini": ("Kamu & Dini Yapı", "Public & Religious", "dome"),
}

CLIENT_STRIP = ["Robert Koleji", "Özyeğin Üniversitesi", "Şişecam", "Arçelik", "Hanwha Aerospace", "Airties", "Yapı Merkezi", "Bilfen", "Kiler GYO", "Mene Health", "Biltur", "GOSB", "Eser İnşaat", "Habif Mimarlık"]
