# Plesk Hosting Kurulum Talimatları

## 📋 Ön Hazırlık

### 1. GitHub Repository'den İndirme
```bash
git clone https://github.com/hazarvolga/aluplan-marketing-list.git
cd aluplan-marketing-list
```

### 2. Lokal Test
```bash
npm install
npm run build
npm start
```

## 🚀 Plesk Hosting Kurulumu

### Adım 1: Plesk Panel Ayarları
1. **Plesk Panel**'e giriş yapın
2. **"Websiteleri & Domainler"** bölümüne gidin
3. Domain'inizi seçin
4. **"Node.js"** sekmesine tıklayın

### Adım 2: Node.js Uygulaması Oluşturma
- **Node.js Version**: `18.x` veya üzeri seçin
- **Application Mode**: `Production` seçin
- **Application Root**: `httpdocs` (default)
- **Application Startup File**: `app.js`
- **Application URL**: Domain adresiniz

### Adım 3: Dosya Yükleme
1. **"Dosya Yöneticisi"** açın
2. **"httpdocs"** klasörüne gidin
3. Tüm proje dosyalarını yükleyin:
   ```
   - src/
   - public/
   - package.json
   - app.js
   - next.config.js
   - tailwind.config.js
   - tsconfig.json
   - .env.example
   ```

### Adım 4: Bağımlılıkları Yükleme
- Plesk otomatik olarak `npm install` çalıştıracak
- Manuel olarak çalıştırmak için:
  ```bash
  npm ci --production
  ```

### Adım 5: Environment Variables
1. **Node.js** ayarlarından **"Environment Variables"** bölümüne gidin
2. Şu değişkenleri ekleyin:
   ```
   NODE_ENV=production
   PORT=3000
   NEXT_PUBLIC_APP_NAME="Aluplan Marketing Data Filter"
   ```

### Adım 6: Uygulamayı Başlatma
1. **"Enable Node.js"** seçeneğini aktif edin
2. **"NPM Install"** butonuna tıklayın (eğer otomatik çalışmadıysa)
3. **"Restart App"** butonuna tıklayın

## 🔧 Troubleshooting

### Hata 1: Port Problemi
```bash
# Plesk'te port 3000 yerine farklı port kullanılıyor
# Environment variables'da PORT değerini kontrol edin
```

### Hata 2: Build Hatası
```bash
# Build işlemi için:
npm run build

# Eğer memory hatası alırsanız:
NODE_OPTIONS="--max-old-space-size=4096" npm run build
```

### Hata 3: Static Files
```bash
# Eğer CSS/JS dosyaları yüklenmiyorsa:
# next.config.js dosyasındaki trailingSlash: true ayarını kontrol edin
```

## 📊 Performans Optimizasyonu

### 1. Gzip Compression
Plesk Panel > Apache & nginx Settings > Additional nginx directives:
```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

### 2. Caching
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## 🔒 Güvenlik

### 1. SSL Certificate
- Plesk'te ücretsiz Let's Encrypt SSL aktif edin
- **"Force HTTPS"** seçeneğini etkinleştirin

### 2. File Permissions
```bash
chmod -R 755 .next
chmod -R 755 public
chmod +x app.js
```

## 🎯 Test Etme

1. **Browser'da açın**: `https://yourdomain.com`
2. **Excel dosyası yükleyin**
3. **Filtreleme özelliklerini test edin**
4. **Mobil uyumluluğu kontrol edin**

## 📞 Destek

Sorun yaşarsanız:
1. **Plesk Error Logs**'u kontrol edin
2. **Node.js Application** logs'una bakın
3. **Browser Console**'u inceleyin
4. **GitHub Issues** açın

---

✅ **Kurulum tamamlandıktan sonra uygulamanız canlı olacak!**
