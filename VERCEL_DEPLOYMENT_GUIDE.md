# 🚀 Vercel Deployment Guide - Aluplan Marketing List

## ✅ Vercel Deployment Adımları

### 1. **Vercel Dashboard'a Git**
```
https://vercel.com/dashboard
```

### 2. **New Project**
- "New Project" butonuna tıkla
- "Import Git Repository" seç

### 3. **GitHub Repository Import**
```
Repository: https://github.com/hazarvolga/aluplan-marketing-list
Branch: main
```

### 4. **Build Settings (Otomatik Algılanır)**
```
Framework Preset: Next.js
Build Command: npm run build
Output Directory: .next (otomatik)
Install Command: npm install
```

### 5. **Environment Variables**
```
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
```

### 6. **Deploy**
- "Deploy" butonuna tıkla
- 2-3 dakika bekle
- Canlı URL alacaksın!

## 🎯 Vercel'de Deployment Süreci

### Step 1: Vercel Dashboard
1. vercel.com/dashboard'a git
2. "New Project" tıkla
3. GitHub account'unu connect et (zaten varsa)

### Step 2: Repository Selection
1. "Import Git Repository" seç
2. "hazarvolga/aluplan-marketing-list" repository'sini bul
3. "Import" butonuna tıkla

### Step 3: Configure Project
```
Project Name: aluplan-marketing-list
Framework: Next.js (otomatik algılanır)
Root Directory: ./ (default)
Build Settings: Default (değiştirme)
```

### Step 4: Environment Variables (Opsiyonel)
```
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
```

### Step 5: Deploy
- "Deploy" butonuna tıkla
- Build logs'u izle
- Başarılı olursa canlı URL alacaksın

## 🔧 Vercel'de Özel Ayarlar

### Custom Domain (Eğer istersen)
```
Project Settings → Domains → Add Domain
allplan.com.tr veya istediğin domain
```

### Environment Variables
```
Project Settings → Environment Variables
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1
```

### Build & Development Settings
```
Build Command: npm run build (default)
Output Directory: .next (default)
Install Command: npm install (default)
```

## 🎉 Deployment Sonrası

### Otomatik Features
- ✅ HTTPS (SSL) otomatik
- ✅ CDN (Global edge network)
- ✅ Automatic builds (Git push'ta)
- ✅ Preview deployments (PR'larda)
- ✅ Custom domains support

### Performance
- ✅ Next.js optimization
- ✅ Image optimization
- ✅ Static file serving
- ✅ Server-side rendering

### Monitoring
- ✅ Build logs
- ✅ Function logs
- ✅ Analytics
- ✅ Performance insights

## 📝 Deployment Checklist

- [ ] Vercel dashboard'a git
- [ ] New Project tıkla
- [ ] GitHub repository import et
- [ ] Framework: Next.js seç
- [ ] Build settings default bırak
- [ ] Environment variables ekle (opsiyonel)
- [ ] Deploy butonuna tıkla
- [ ] Build logs'u izle
- [ ] Canlı URL'i test et

## 🔄 Sonraki Güncellemeler

GitHub'a push yaptığında otomatik deploy olacak:
```bash
git add .
git commit -m "Update"
git push origin main
```

Vercel otomatik olarak yeni versiyonu deploy edecek!

## 🌐 Canlı URL

Deploy sonrası şöyle bir URL alacaksın:
```
https://aluplan-marketing-list-hazarvolga.vercel.app
```

Custom domain de ekleyebilirsin.

---

**Şimdi vercel.com/dashboard'a git ve "New Project" ile başla!** 🚀

*GitHub repository'n hazır, sadece import et ve deploy et!*
