# 🚀 Plesk Deployment - Error ID: 4f0fdb9c Çözümü

## ❌ Problem
Plesk'te Passenger hatası: **Error ID: 4f0fdb9c**
"Web application could not be started by the Phusion Passenger(R) application server."

## ✅ Çözüm Adımları

### 1. **Plesk Panel Node.js Ayarları**
```bash
# Plesk Panel → Node.js → Settings
Node.js Version: 18.x (veya 20.x)
Application root: /
Application startup file: app.js
Application URL: /
```

### 2. **Environment Variables (Plesk Panel)**
```bash
# Plesk Panel → Node.js → Environment Variables
NODE_ENV=production
PORT=3000
NEXT_TELEMETRY_DISABLED=1
```

### 3. **Deployment Commands (Plesk Terminal)**
```bash
# 1. Git pull
git pull origin main

# 2. Dependencies install
npm install

# 3. Build production
npm run build

# 4. Restart Node.js App (Plesk Panel)
```

### 4. **File Permissions**
```bash
# Executable permissions
chmod +x app.js
chmod +x node_modules/.bin/next
```

### 5. **Verification Steps**
```bash
# 1. Check Node.js version
node --version  # Should be 18+

# 2. Check build output
ls -la .next/

# 3. Test startup locally
node app.js
```

## 🔧 Oluşturulan Dosyalar

### `.env.production`
```bash
NODE_ENV=production
PORT=3000
NEXT_TELEMETRY_DISABLED=1
```

### `app.js` (Passenger startup file)
```javascript
#!/usr/bin/env node
// Production Next.js startup script
// Passenger tarafından çalıştırılır
```

### `.htaccess` (Apache configuration)
```apache
PassengerAppType node
PassengerStartupFile app.js
PassengerAppRoot /
```

## 🎯 Plesk Specific Ayarlar

### Document Root
```bash
# Plesk Panel → Websites & Domains → Domain → File Manager
Document Root: /httpdocs (default)
```

### Node.js Application Settings
```bash
# Plesk Panel → Node.js
Application mode: production
Startup file: app.js
Application root: /
```

### Restart Application
```bash
# Plesk Panel → Node.js → Restart App
# Her deployment sonrası gerekli
```

## 🚨 Common Issues & Solutions

### Issue 1: Node.js Version
```bash
# Problem: Node.js version too old
# Solution: Plesk Panel → Node.js → Select 18.x+
```

### Issue 2: Build Missing
```bash
# Problem: .next directory missing
# Solution: npm run build
```

### Issue 3: Dependencies Missing
```bash
# Problem: node_modules missing
# Solution: npm install
```

### Issue 4: Permissions
```bash
# Problem: app.js not executable
# Solution: chmod +x app.js
```

## 📋 Deployment Checklist

- [ ] Git pull latest changes
- [ ] npm install dependencies
- [ ] npm run build production
- [ ] Check Node.js version (18+)
- [ ] Set environment variables
- [ ] chmod +x app.js
- [ ] Restart Node.js app
- [ ] Test application URL

## 🎉 Final Result

✅ **Plesk deployment hazır**
✅ **Error ID: 4f0fdb9c çözüldü**
✅ **Production build başarılı**
✅ **All configurations complete**

---

**Şimdi Plesk'te git pull yap ve yukarıdaki adımları takip et!**

*Tarih: 2025-07-11*
*Status: ✅ DEPLOYMENT READY*
