#!/bin/bash

# Aluplan Marketing List Deployment Script
# For Plesk hosting

echo "🚀 Aluplan Marketing List Deployment Started"
echo "=========================================="

# 1. Install dependencies
echo "📦 Installing dependencies..."
npm ci --production

# 2. Build the application
echo "🔨 Building application..."
npm run build

# 3. Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p uploads
mkdir -p temp

# 4. Set permissions (if needed)
echo "🔐 Setting permissions..."
chmod -R 755 .next
chmod -R 755 public
chmod +x app.js

# 5. Create log file
echo "📄 Creating log file..."
touch logs/app.log

# 6. Display success message
echo "✅ Deployment completed successfully!"
echo "=========================================="
echo "🌐 Application ready for Plesk hosting"
echo "📋 Startup file: app.js"
echo "🔧 Node.js version: $(node --version)"
echo "📦 NPM version: $(npm --version)"
echo "=========================================="

# 7. Show next steps
echo "Next steps for Plesk:"
echo "1. Upload files to httpdocs folder"
echo "2. Set Node.js application"
echo "3. Set startup file to: app.js"
echo "4. Set environment to: production"
echo "5. Install dependencies (automatic)"
echo "6. Start the application"
echo "=========================================="
