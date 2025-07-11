# 🚀 Plesk Terminal ile Deployment - Root Access

## 🔧 Terminal Erişimi Var - Root User

### 1. **Domain Path Bulma**
```bash
# Domain path'ini bul
plesk bin domain --list
# veya
ls -la /var/www/vhosts/
```

### 2. **Domain Directory'ye Git**
```bash
# Domain klasörüne git (yourdomain.com yerine gerçek domain adını koy)
cd /var/www/vhosts/yourdomain.com/httpdocs
```

### 3. **Git Clone/Pull**
```bash
# Eğer ilk kez clone yapıyorsan:
git clone https://github.com/hazarvolga/aluplan-marketing-list.git .

# Eğer zaten var ise:
git pull origin main
```

### 4. **Node.js Version Control**
```bash
# Node.js version kontrol
node --version
# 18+ olmalı

# Eğer eski version varsa:
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs
```

### 5. **Dependencies & Build**
```bash
# Clean install
rm -rf node_modules .next
npm install
npm run build
```

### 6. **File Permissions**
```bash
# Executable permissions
chmod +x app.js
chmod -R 755 .next
chmod -R 755 node_modules
chown -R apache:apache .
```

### 7. **Environment Variables**
```bash
# .env.production dosyasını kontrol et
cat .env.production

# Eğer eksikse oluştur:
cat > .env.production << 'EOF'
NODE_ENV=production
PORT=3000
NEXT_TELEMETRY_DISABLED=1
NODE_OPTIONS=--max-old-space-size=1024
HOSTNAME=0.0.0.0
NEXT_PRIVATE_DEBUG_CACHE=false
NEXT_PRIVATE_STANDALONE=true
EOF
```

### 8. **Test Application**
```bash
# Local test
PORT=3001 node app.js
# Başka terminal'de test:
# curl http://localhost:3001
```

### 9. **Plesk Node.js Configuration**
```bash
# Plesk ile Node.js app'i restart et
plesk bin site --update-nodejs-app domain.com -startup-file app.js
```

## 📋 Tam Deployment Script

```bash
#!/bin/bash
# Plesk Next.js Deployment Script

# Domain adını değiştir
DOMAIN="yourdomain.com"
REPO="https://github.com/hazarvolga/aluplan-marketing-list.git"

echo "🚀 Starting Plesk deployment for $DOMAIN"

# Domain directory'ye git
cd /var/www/vhosts/$DOMAIN/httpdocs

# Git pull
echo "📥 Pulling latest changes..."
git pull origin main

# Dependencies
echo "📦 Installing dependencies..."
rm -rf node_modules .next
npm install

# Build
echo "🔨 Building application..."
npm run build

# Permissions
echo "🔒 Setting permissions..."
chmod +x app.js
chmod -R 755 .next
chmod -R 755 node_modules
chown -R apache:apache .

# Test
echo "🧪 Testing application..."
PORT=3001 timeout 5 node app.js &
sleep 3
if curl -f http://localhost:3001 > /dev/null 2>&1; then
    echo "✅ Application test successful"
else
    echo "❌ Application test failed"
fi

# Restart Plesk Node.js app
echo "🔄 Restarting Plesk Node.js application..."
plesk bin site --update-nodejs-app $DOMAIN -startup-file app.js

echo "🎉 Deployment completed!"
```

## 🔍 Debugging Commands

```bash
# Plesk logs
tail -f /var/log/plesk/error.log

# Node.js app logs
tail -f /var/www/vhosts/yourdomain.com/logs/error.log

# Process kontrolü
ps aux | grep node

# Port kontrolü
netstat -tlnp | grep :3000
```

## 🚨 Common Issues & Solutions

### Issue 1: Permission Denied
```bash
sudo chown -R apache:apache /var/www/vhosts/yourdomain.com/httpdocs
sudo chmod -R 755 /var/www/vhosts/yourdomain.com/httpdocs
```

### Issue 2: Node.js Version
```bash
# Node.js 18+ install
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs
```

### Issue 3: Build Failure
```bash
# Clean build
rm -rf node_modules .next package-lock.json
npm install
npm run build
```

---

**Root terminal erişimi ile full deployment guide!** 🚀
