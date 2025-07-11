# 🚨 Plesk Server Error 500 - Troubleshooting Guide

## ❌ Current Problem
**Server Error 500 - Internal Server Error**
Plesk'te Next.js uygulaması başlatılamıyor.

## 🔍 Debugging Steps

### 1. **Plesk Error Logs Kontrol**
```bash
# Plesk Panel → Websites & Domains → Domain → Logs
# Error Logs → Apache/Nginx Error Log
# Node.js Logs → Application Logs

# Terminal üzerinden:
tail -f /var/log/plesk/error.log
tail -f ~/logs/error.log
```

### 2. **Node.js Application Status**
```bash
# Plesk Panel → Node.js
# Status: Check if app is running
# If stopped → Start Application
```

### 3. **Dependencies Check**
```bash
# Plesk Terminal:
cd /var/www/vhosts/yourdomain.com/httpdocs
npm install --production
npm run build
```

### 4. **Environment Variables**
```bash
# Plesk Panel → Node.js → Environment Variables
# Ensure all variables are set:
NODE_ENV=production
PORT=3000
NEXT_TELEMETRY_DISABLED=1
```

### 5. **File Permissions**
```bash
# Plesk Terminal:
chmod +x app.js
chmod -R 755 .next
chmod -R 755 node_modules
```

## 🔧 Common Fixes

### Fix 1: Node.js Version
```bash
# Problem: Node.js version incompatible
# Solution: Plesk Panel → Node.js → Select 18.x or 20.x
```

### Fix 2: Build Missing
```bash
# Problem: .next directory missing or corrupt
# Solution:
rm -rf .next
npm run build
```

### Fix 3: Dependencies Issues
```bash
# Problem: node_modules missing or corrupt
# Solution:
rm -rf node_modules
npm install
```

### Fix 4: Startup File Issues
```bash
# Problem: app.js not working
# Solution: Test locally first
node app.js
# Should show: "Aluplan Marketing List starting on port 3000"
```

### Fix 5: Memory Issues
```bash
# Problem: Not enough memory
# Solution: Increase Node.js memory limit
# Plesk Panel → Node.js → Additional options
NODE_OPTIONS=--max-old-space-size=1024
```

## 📋 Step-by-Step Solution

### Step 1: Check Current Status
```bash
# Plesk Terminal:
cd /var/www/vhosts/yourdomain.com/httpdocs
ls -la
# Should see: app.js, package.json, .next/, node_modules/
```

### Step 2: Verify Build
```bash
# Check if build exists
ls -la .next/
# Should see: server/, static/, etc.
```

### Step 3: Test Locally
```bash
# Test startup script
node app.js
# Expected: No errors, app starts
```

### Step 4: Check Logs
```bash
# Check application logs
tail -f ~/logs/error.log
# Look for specific error messages
```

### Step 5: Restart Application
```bash
# Plesk Panel → Node.js → Restart App
# Wait for restart to complete
```

## 🎯 Most Likely Causes

1. **Build Missing**: `npm run build` not executed
2. **Dependencies Missing**: `npm install` not executed  
3. **Node.js Version**: Wrong version selected
4. **Permissions**: Files not executable
5. **Memory**: Insufficient memory allocation

## 🚀 Quick Fix Commands

```bash
# Run these in Plesk Terminal:
cd /var/www/vhosts/yourdomain.com/httpdocs
rm -rf .next node_modules
npm install
npm run build
chmod +x app.js
# Then restart Node.js app in Plesk Panel
```

---

**Next: Share the specific error message from Plesk logs for targeted solution!**
