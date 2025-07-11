# Aluplan Marketing Data Filter

🚀 **Modern ve güçlü bir marketing veri analiz aracı** - Excel dosyalarınızı kolayca filtreleyin, analiz edin ve spam email'leri tespit edin.

## ✨ Özellikler

### 📊 Veri Yönetimi
- **Excel Dosya Desteği**: `.xlsx` ve `.xls` formatlarında dosya yükleme
- **Büyük Veri Seti Desteği**: 10,000+ kayıt ile sorunsuz çalışma
- **Gerçek Zamanlı Filtreleme**: Anında sonuçlar
- **CSV Export**: Filtrelenmiş verileri CSV formatında indirme

### 🔍 Akıllı Filtreleme
- **Segment Filtreleri**: Mautic, Sales Hub, V2022, V2023 kategorileri
- **Metin Arama**: İsim, email ve şirket adında arama
- **Kalite Filtreleri**: Geçersiz email, tekrar kayıt, eksik bilgi tespiti
- **Spam Tespit**: 40+ spam domain ve akıllı algoritma

### 🛡️ Spam Email Tespiti
- **Gelişmiş Algoritma**: 0-100 spam risk puanı
- **Görsel Göstergeler**: Renkli risk seviyeleri
- **Detaylı Analiz**: Spam sebep açıklamaları
- **Bilinen Spam Servisleri**: 10minutemail, tempmail, guerrillamail vb.

### 🎯 Kullanıcı Deneyimi
- **Sıralanabilir Tablo**: Tüm sütunlar için A-Z/Z-A sıralama
- **Duyarlı Tasarım**: Mobil ve masaüstü uyumlu
- **Dinamik Yükleme**: 100'er kayıt ile performans optimizasyonu
- **Görsel Geri Bildirim**: Aktif filtreler ve durum göstergeleri

## 🚀 Kurulum

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/hazarvolga/aluplan-marketing-list.git
cd aluplan-marketing-list
```

### 2. Bağımlılıkları Yükleyin
```bash
npm install
```

### 3. Geliştirme Sunucusunu Başlatın
```bash
npm run dev
```

### 4. Tarayıcıda Açın
```
http://localhost:3000
```

## 🏗️ Plesk Hosting Kurulumu

### 1. Proje Hazırlığı
```bash
# Projeyi build edin
npm run build

# Static export (isteğe bağlı)
npm run export
```

### 2. Plesk Upload
- **Dosya Yöneticisi** > **httpdocs** klasörüne yükleyin
- **Node.js** uygulaması olarak ayarlayın
- **Startup file**: `server.js` veya `next start`

### 3. Plesk Ayarları
- **Node.js Version**: 18.x veya üzeri
- **NPM Install**: Otomatik
- **Environment**: `production`

## 📁 Proje Yapısı

```
aluplan-marketing-list/
├── src/
│   ├── app/
│   │   ├── page.tsx           # Ana sayfa
│   │   ├── layout.tsx         # Layout
│   │   └── api/
│   │       └── load-data/     # API endpoint
│   ├── lib/
│   │   ├── excel-utils.ts     # Excel işlemleri
│   │   └── utils.ts          # Utility fonksiyonlar
│   └── components/           # React bileşenleri
├── public/                   # Statik dosyalar
├── package.json
├── next.config.js
├── tailwind.config.js
└── README.md
```

## �️ Teknolojiler

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **Icons**: Lucide React
- **Excel Processing**: XLSX
- **Deployment**: Plesk/Vercel uyumlu

## 📈 Veri Formatı

Excel dosyalarınız aşağıdaki sütunları içermelidir:

| Sütun | Açıklama |
|-------|----------|
| `name` | Kişi adı |
| `email` | E-mail adresi |
| `company` | Şirket adı |
| `phone` | Telefon numarası |
| `segment` | Segment bilgisi (virgülle ayrılmış) |

## 🎨 Spam Tespit Algoritması

### Risk Seviyeleri
- **0-19**: 🟢 Güvenli
- **20-39**: � Düşük Risk
- **40-59**: 🟡 Orta Risk
- **60-79**: 🟠 Yüksek Risk
- **80-100**: 🔴 Çok Yüksek Risk

### Tespit Yöntemleri
- Bilinen spam domain'ler
- Geçici email servisleri
- Şüpheli karakter patternleri
- Typo domain'ler
- Çok rakam içeren email'ler

## 🚦 Performans

- **Yükleme Süresi**: < 2 saniye
- **Filtreleme**: Gerçek zamanlı
- **Desteklenen Kayıt**: 50,000+
- **Tarayıcı Desteği**: Chrome, Firefox, Safari, Edge

## 📱 Mobil Uyumluluk

- Responsive tasarım
- Touch-friendly interface
- Optimize edilmiş tablo görünümü
- Mobil menüler

## 🔧 Geliştirici Notları

### Build Komutu
```bash
npm run build
```

### Lint Kontrolü
```bash
npm run lint
```

### Type Check
```bash
npx tsc --noEmit
```

## 📝 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasını inceleyebilirsiniz.

## 👨‍💻 Geliştirici

**Hazar Volga**
- GitHub: [@hazarvolga](https://github.com/hazarvolga)

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📞 Destek

Herhangi bir sorunuz veya öneriniz için:
- GitHub Issues açın
- Email ile iletişime geçin
- Dokumentasyonu kontrol edin

---

⭐ **Beğendiyseniz yıldızlamayı unutmayın!**

## Kurulum

1. Proje klasörüne gidin:
```bash
cd aluplan-mailing-data
```

2. Bağımlılıkları yükleyin:
```bash
npm install
```

3. Geliştirme sunucusunu başlatın:
```bash
npm run dev
```

4. Tarayıcınızda [http://localhost:3000](http://localhost:3000) adresine gidin.

## Kullanım

1. **Dosya Yükleme**: Ana sayfada "Excel Dosyası Yükle" butonuna tıklayarak .xlsx dosyanızı yükleyin
2. **Filtreleme**: Sol taraftaki filtre panelinden istediğiniz segmentleri seçin
3. **Arama**: Üst kısımdaki arama kutusunu kullanarak belirli kayıtları bulun
4. **İhracat**: Filtrelenmiş veriyi CSV olarak indirmek için "CSV İndir" butonunu kullanın

## Veri Yapısı

Uygulama aşağıdaki Excel kolonlarını destekler:
- **Name**: Kişi adı
- **Email**: E-posta adresi (geçerlilik kontrolü ile)
- **Company**: Şirket adı
- **Phone**: Telefon numarası
- **Segment**: Pazarlama segmenti (virgülle ayrılmış değerler)

### Segment Türleri
- **Mautic**: Marketing automation platformu verileri
- **Sales Hub Mevcut**: Mevcut müşteri verileri
- **V2022 ve eski**: 2022 ve öncesi versiyon kullanıcıları
- **V2023 ve üzeri**: 2023 sonrası versiyon kullanıcıları

### Veri Temizleme
- Duplicate e-mail kontrolü
- Geçersiz e-mail formatlarının tespiti
- DNC listesi ile karşılaştırma
- Eksik alan kontrolleri

## Geliştirme

### Proje Yapısı

```
src/
├── app/
│   ├── api/load-data/    # API routes
│   └── page.tsx          # Ana sayfa komponenti
├── lib/
│   ├── excel-utils.ts    # Excel işleme utilities
│   └── utils.ts          # Genel utility fonksiyonlar
└── data/                 # Excel dosyaları
```

### API Endpoints

- `GET /api/load-data`: Varsayılan Excel dosyasını yükler

## Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
