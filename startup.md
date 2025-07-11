# Aluplan Marketing Data Filter - Startup Instructions

## GitHub Repository
✅ **Repository URL**: https://github.com/hazarvolga/aluplan-marketing-list

## Local Development Status
✅ **Build Status**: Successfully built with `npm run build`
✅ **Git Status**: Clean working tree, synced with remote
✅ **Dependencies**: All installed and working

## Plesk Deployment Ready
Proje Plesk'e deploy edilmeye hazır durumda. Aşağıdaki adımları takip edin:

### 1. Plesk'e Dosya Yükleme
```bash
# Proje dosyalarını sunucuya yükleyin
scp -r . username@yourserver.com:/var/www/vhosts/yourdomain.com/httpdocs/
```

### 2. Sunucuda Kurulum
```bash
# Sunucuda bu komutları çalıştırın
cd /var/www/vhosts/yourdomain.com/httpdocs/
npm install
npm run build
```

### 3. Plesk Application Startup
- Plesk'te Node.js uygulaması olarak ayarlayın
- Startup file: `app.js`
- Document root: `/httpdocs`

### 4. Test
Uygulama başarıyla çalışıyor olmalı:
- Excel dosyası yükleme
- Spam email filtreleme
- Sıralama ve arama
- CSV export

## Özellikler
- ✅ Excel dosyası işleme
- ✅ Spam email detection (40+ domain)
- ✅ Sıralanabilir tablolar
- ✅ Responsive tasarım
- ✅ CSV export
- ✅ Telefon kolonu toggle
- ✅ Detaylı spam filtreleme dokümantasyonu

## Dosya Yapısı
```
├── src/
│   ├── app/
│   │   ├── page.tsx        # Ana uygulama
│   │   └── layout.tsx      # Metadata
│   └── lib/
│       └── excel-utils.ts  # Excel işleme ve spam detection
├── public/                 # Statik dosyalar
├── app.js                 # Plesk startup file
├── next.config.js         # Plesk optimizasyonu
├── deploy.sh              # Deployment script
├── README.md              # Kapsamlı dokümantasyon
├── PLESK_SETUP.md         # Plesk kurulum rehberi
└── LICENSE                # MIT License
```

## Sonraki Adımlar
1. **GitHub'dan klon**: `git clone https://github.com/hazarvolga/aluplan-marketing-list.git`
2. **Plesk'e deploy**: `PLESK_SETUP.md` dosyasını takip edin
3. **Test**: Uygulamayı test edin
4. **Üretim**: Canlı ortamda kullanın

Tüm dosyalar hazır ve GitHub'da! 🚀
