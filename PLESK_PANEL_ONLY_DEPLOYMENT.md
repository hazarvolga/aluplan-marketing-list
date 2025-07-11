# 🚀 Plesk Panel - Terminal ERİŞİMİ OLMADAN Deployment

## ⚠️ Problem: Terminal Erişimi Yok
Plesk'te terminal erişimi olmadan Next.js deployment yapacağız.

## 📋 Sadece Plesk Panel ile Çözüm

### 1. **Git Repository Sync**
```bash
# Plesk Panel → Git
Repository: https://github.com/hazarvolga/aluplan-marketing-list
Branch: main
Deploy Path: /
Actions: Pull/Deploy
```

### 2. **File Manager ile Kontrol**
```bash
# Plesk Panel → File Manager
# Kontrol edilecek dosyalar:
- package.json ✅
- app.js ✅
- .env.production ✅
- .next/ folder (build sonrası)
- node_modules/ folder
```

### 3. **Node.js Panel Ayarları**
```bash
# Plesk Panel → Node.js
Node.js Version: 18.17.0 (veya mevcut en son)
Application Mode: Production
Application Root: /
Application Startup File: app.js
```

### 4. **Environment Variables**
```bash
# Plesk Panel → Node.js → Environment Variables
NODE_ENV=production
PORT=3000
NEXT_TELEMETRY_DISABLED=1
NODE_OPTIONS=--max-old-space-size=1024
HOSTNAME=0.0.0.0
NEXT_PRIVATE_DEBUG_CACHE=false
NEXT_PRIVATE_STANDALONE=true
```

### 5. **NPM Scripts (Panel)**
```bash
# Plesk Panel → Node.js → NPM Scripts
# Run in order:
1. npm install
2. npm run build
3. Restart Application
```

## 🎯 Adım Adım Plesk Panel Rehberi

### Step 1: Git Repository
1. Plesk Panel → Git
2. Repository URL: `https://github.com/hazarvolga/aluplan-marketing-list`
3. Branch: `main`
4. Deploy Path: `/`
5. **Pull** butonuna tıkla

### Step 2: Node.js Settings
1. Plesk Panel → Node.js
2. Node.js Version: **18.17.0** (veya mevcut son)
3. Application Mode: **Production**
4. Application Root: `/`
5. Application Startup File: `app.js`
6. **Apply** butonuna tıkla

### Step 3: Environment Variables
1. Plesk Panel → Node.js → Environment Variables
2. Aşağıdaki değişkenleri ekle:
```
NODE_ENV=production
PORT=3000
NEXT_TELEMETRY_DISABLED=1
NODE_OPTIONS=--max-old-space-size=1024
HOSTNAME=0.0.0.0
NEXT_PRIVATE_DEBUG_CACHE=false
NEXT_PRIVATE_STANDALONE=true
```

### Step 4: NPM Install & Build
1. Plesk Panel → Node.js → NPM
2. **Install Dependencies** butonuna tıkla
3. Bekleme (birkaç dakika sürebilir)
4. **Run Script** → `build` seç
5. **Run** butonuna tıkla

### Step 5: Application Restart
1. Plesk Panel → Node.js
2. **Restart App** butonuna tıkla
3. Status: **Running** olana kadar bekle

## 🔍 Debugging (Panel Only)

### Check Application Status
```bash
# Plesk Panel → Node.js
Status: Running ✅ / Stopped ❌
```

### Check Error Logs
```bash
# Plesk Panel → Logs → Error Logs
# Son error mesajlarını kontrol et
```

### File Manager Control
```bash
# Plesk Panel → File Manager
# Kontrol et:
- .next/ folder exists ✅
- node_modules/ folder exists ✅
- app.js executable ✅
```

## 🚨 Common Issues & Panel Solutions

### Issue 1: Build Failed
```bash
# Solution: Plesk Panel → Node.js → NPM
# Clear Cache → Install Dependencies → Run Build
```

### Issue 2: App Won't Start
```bash
# Solution: Plesk Panel → Node.js
# Check Node.js Version (18+)
# Check Startup File: app.js
# Restart Application
```

### Issue 3: Memory Issues
```bash
# Solution: Environment Variables
# Add: NODE_OPTIONS=--max-old-space-size=1024
```

### Issue 4: Port Conflicts
```bash
# Solution: Environment Variables
# Set: PORT=3000
# Set: HOSTNAME=0.0.0.0
```

## 📝 Checklist (Panel Only)

- [ ] Git Pull from main branch
- [ ] Node.js Version 18+ selected
- [ ] Environment Variables added
- [ ] NPM Dependencies installed
- [ ] Build script executed
- [ ] Application restarted
- [ ] Status shows "Running"
- [ ] Test website URL

## 🎉 Final Steps

1. **Wait for Build**: Build process birkaç dakika sürebilir
2. **Check Status**: Application status "Running" olmalı
3. **Test URL**: Website URL'inizi test edin
4. **Check Logs**: Error varsa logs'u kontrol edin

---

**Terminal erişimi olmadan tamamen Plesk Panel ile deployment!** 🚀

*Her adımı sırasıyla takip et ve her step sonrası status kontrol et.*
