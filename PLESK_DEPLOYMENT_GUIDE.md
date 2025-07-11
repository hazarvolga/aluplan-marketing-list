# Plesk Deployment Rehberi - Aluplan Marketing List

## 🚀 Plesk'e Deployment Adımları

### 1. Plesk Panel Ayarları
```bash
# Node.js ayarları
Node.js Version: 18.x veya 20.x
Application root: /
Application startup file: app.js
```

### 2. Gerekli Ortam Değişkenleri
```bash
NODE_ENV=production
PORT=3000
NEXT_TELEMETRY_DISABLED=1
```

### 3. Build ve Deployment
```bash
# 1. Dependencies kurulumu
npm install

# 2. Next.js build
npm run build

# 3. Restart Application
```

### 4. File Permissions
```bash
# Executable yapın
chmod +x app.js
chmod +x node_modules/.bin/next

# Passenger için gerekli
chmod 755 .
```

### 5. Troubleshooting

#### Passenger Hatası (Error ID: 4f0fdb9c)
```bash
# 1. Node.js version kontrolü
node --version

# 2. Build kontrolü
npm run build

# 3. Dependencies kontrolü
npm install --production

# 4. Startup file kontrolü
node app.js
```

#### Log Dosyaları
```bash
# Passenger log
/var/log/passenger/

# Application log
~/logs/
```

#### Yaygın Hatalar
1. **Node.js version uyumsuzluğu**: Node.js 18+ gerekli
2. **Build eksik**: `npm run build` çalıştırılmamış
3. **Dependencies eksik**: `npm install` çalıştırılmamış
4. **Port conflict**: PORT environment variable ayarı

### 6. Plesk Specific Ayarları

#### Domain Ayarları
```bash
# Document Root: /httpdocs
# Application Root: /
# Startup File: app.js
```

#### Environment Variables (Plesk Panel)
```bash
NODE_ENV=production
PORT=3000
NEXT_TELEMETRY_DISABLED=1
```

#### Passenger Configuration
```bash
# passenger_app_type: node
# passenger_startup_file: app.js
# passenger_app_root: /
```

### 7. Deployment Komutları

```bash
# Plesk terminal üzerinden
cd /var/www/vhosts/yourdomain.com/httpdocs
npm install
npm run build
# Restart Node.js App (Plesk Panel)
```

### 8. Verification
```bash
# Build check
ls -la .next/

# Dependencies check
ls -la node_modules/

# Startup file check
node app.js
```

## 🔧 Hata Giderme

### Error ID: 4f0fdb9c
Bu hata genellikle şu nedenlerle oluşur:

1. **Node.js version problem**
2. **Build edilmemiş proje**
3. **Dependencies eksik**
4. **app.js başlatma hatası**

### Çözüm Adımları
```bash
# 1. Node.js version kontrol
node --version # 18+ olmalı

# 2. Clean build
rm -rf .next node_modules
npm install
npm run build

# 3. Test local
node app.js

# 4. Plesk restart
```

## 📝 Notlar

- Next.js 15 kullanılıyor
- Production build gerekli
- Passenger Node.js modu
- Port 3000 default
- Environment variables önemli

---
*Plesk deployment için optimized*
