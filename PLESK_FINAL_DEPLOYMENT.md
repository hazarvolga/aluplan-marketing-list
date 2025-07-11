# 🚀 Plesk Deployment - Server Error 500 Solution

## ✅ GitHub Repository Updated
**Repository:** `https://github.com/hazarvolga/aluplan-marketing-list`  
**Branch:** `main`  
**Status:** ✅ Ready for deployment

## 🔧 Plesk'te Yapılacak Adımlar

### 1. **Git Pull (Plesk Terminal)**
```bash
cd /var/www/vhosts/yourdomain.com/httpdocs
git pull origin main
```

### 2. **Dependencies & Build**
```bash
# Clean install
rm -rf node_modules .next
npm install
npm run build
```

### 3. **File Permissions**
```bash
chmod +x app.js
chmod -R 755 .next
chmod -R 755 node_modules
```

### 4. **Plesk Panel Ayarları**
```bash
# Plesk Panel → Node.js
Node.js Version: 18.x (veya 20.x)
Application startup file: app.js
Application root: /
Application URL: /
```

### 5. **Environment Variables (Plesk Panel)**
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

### 6. **Restart Application**
```bash
# Plesk Panel → Node.js → Restart App
# Wait for restart completion
```

## 🔍 Debug Steps (Eğer Hala Hata Alırsan)

### Check Logs
```bash
# Plesk Panel → Logs → Error Logs
# Look for specific error messages
```

### Test Locally
```bash
# Plesk Terminal
cd /var/www/vhosts/yourdomain.com/httpdocs
node app.js
# Should show: "Aluplan Marketing List starting on port 3000"
```

### Verify Build
```bash
ls -la .next/
# Should see: server/, static/, standalone/
```

## 🎯 Enhanced .env.production

Yeni .env.production dosyası şu ayarları içeriyor:
```bash
NODE_ENV=production
PORT=3000
NEXT_TELEMETRY_DISABLED=1
NODE_OPTIONS=--max-old-space-size=1024
HOSTNAME=0.0.0.0
NEXT_PRIVATE_DEBUG_CACHE=false
NEXT_PRIVATE_STANDALONE=true
```

## 🚨 Common Issues & Solutions

### Issue 1: Memory Error
```bash
# Added: NODE_OPTIONS=--max-old-space-size=1024
```

### Issue 2: Hostname Binding
```bash
# Added: HOSTNAME=0.0.0.0
```

### Issue 3: Next.js Cache Issues
```bash
# Added: NEXT_PRIVATE_DEBUG_CACHE=false
```

### Issue 4: Standalone Mode
```bash
# Added: NEXT_PRIVATE_STANDALONE=true
```

## 📋 Deployment Checklist

- [ ] `git pull origin main` ✅
- [ ] `rm -rf node_modules .next`
- [ ] `npm install`
- [ ] `npm run build`
- [ ] `chmod +x app.js`
- [ ] Set Environment Variables in Plesk Panel
- [ ] Restart Node.js App
- [ ] Test application URL

## 🎉 Final Test

After deployment, test:
- Application loads without 500 error
- Data filtering works
- Export functionality works
- All filters functional

---

**Repository:** `https://github.com/hazarvolga/aluplan-marketing-list`  
**Branch:** `main`  
**Status:** ✅ Server Error 500 solution deployed

*Now run the steps above in Plesk!*
