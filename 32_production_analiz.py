import pandas as pd
import os
import json
from pathlib import Path

print('🔍 PROJE KAPSAMLI VERİ TUTARLILIĞI VE PRODUCTION HAZIRLIĞI ANALİZİ')
print('=' * 80)

# 1. VERİ TUTARLILIĞI ANALİZİ
print('📊 1. VERİ TUTARLILIĞI ANALİZİ')
print('-' * 50)

# Ana veri dosyasını yükle
df = pd.read_excel('data/aluplan-list.xlsx')
print(f'   📝 Ana veri dosyası: {len(df):,} kayıt')

# Segment dağılımı
segments = df['segment'].value_counts()
print(f'   📊 Segment dağılımı:')
for segment, count in segments.head(10).items():
    print(f'      📋 {segment}: {count:,}')

# Email listelerini kontrol et
v2023_emails = set()
v2022_emails = set()

# V2023 emails
try:
    with open('src/data/v2023-emails.ts', 'r') as f:
        content = f.read()
        import re
        emails = re.findall(r'"([^"]+@[^"]+)"', content)
        v2023_emails = set(email.lower().strip() for email in emails)
    print(f'   📧 V2023 email listesi: {len(v2023_emails):,} email')
except Exception as e:
    print(f'   ❌ V2023 email listesi hatası: {e}')

# V2022 emails
try:
    with open('src/data/v2022-emails.ts', 'r') as f:
        content = f.read()
        import re
        emails = re.findall(r'"([^"]+@[^"]+)"', content)
        v2022_emails = set(email.lower().strip() for email in emails)
    print(f'   📧 V2022 email listesi: {len(v2022_emails):,} email')
except Exception as e:
    print(f'   ❌ V2022 email listesi hatası: {e}')

# Segment hesaplamaları
sales_hub_count = df[df['segment'].astype(str).str.contains('Sales Hub Mevcut', case=False, na=False)].shape[0]
potansiyel_count = df[df['segment'].astype(str).str.contains('Potansiyel', case=False, na=False)].shape[0]
mevcut_count = df[df['segment'].astype(str).str.contains('Mevcut', case=False, na=False)].shape[0]

print(f'\n   🧮 SEGMENT HESAPLAMALARI:')
print(f'      📊 Sales Hub Mevcut: {sales_hub_count:,}')
print(f'      📊 Potansiyel Müşteriler: {potansiyel_count:,}')
print(f'      📊 Mevcut Müşteriler: {mevcut_count:,}')
print(f'      📊 V2023 Virtual: {len(v2023_emails):,}')
print(f'      📊 V2022 Virtual: {len(v2022_emails):,}')

# 2. PROJE YAPISI ANALİZİ
print(f'\n📁 2. PROJE YAPISI ANALİZİ')
print('-' * 50)

# Önemli dosyalar
important_files = [
    'package.json',
    'next.config.js',
    'tailwind.config.js',
    'tsconfig.json',
    '.env.local',
    '.env.example',
    'README.md',
    'src/app/page.tsx',
    'src/lib/excel-utils.ts',
    'src/data/v2023-emails.ts',
    'src/data/v2022-emails.ts',
    'data/aluplan-list.xlsx'
]

print('   📋 ÖNEMLI DOSYALAR:')
for file in important_files:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f'      ✅ {file} ({size:,} bytes)')
    else:
        print(f'      ❌ {file} - BULUNAMADI')

# 3. PACKAGE.JSON ANALİZİ
print(f'\n📦 3. PACKAGE.JSON ANALİZİ')
print('-' * 50)

try:
    with open('package.json', 'r') as f:
        package_data = json.load(f)
    
    print(f'   📝 Proje adı: {package_data.get("name", "N/A")}')
    print(f'   📝 Versiyon: {package_data.get("version", "N/A")}')
    print(f'   📝 Açıklama: {package_data.get("description", "N/A")}')
    
    print(f'   📦 Dependencies:')
    deps = package_data.get('dependencies', {})
    for dep, version in deps.items():
        print(f'      📋 {dep}: {version}')
    
    print(f'   🔧 Scripts:')
    scripts = package_data.get('scripts', {})
    for script, command in scripts.items():
        print(f'      📋 {script}: {command}')
        
except Exception as e:
    print(f'   ❌ package.json okuma hatası: {e}')

# 4. NEXT.JS KONFIGÜRASYONU
print(f'\n⚡ 4. NEXT.JS KONFIGÜRASYONU')
print('-' * 50)

if os.path.exists('next.config.js'):
    print('   ✅ next.config.js mevcut')
    with open('next.config.js', 'r') as f:
        config_content = f.read()
        print(f'   📝 Konfigürasyon: {len(config_content)} karakter')
else:
    print('   ⚠️ next.config.js bulunamadı')

# 5. ENVIRONMENT VARIABLES
print(f'\n🌍 5. ENVIRONMENT VARIABLES')
print('-' * 50)

env_files = ['.env.local', '.env', '.env.example']
for env_file in env_files:
    if os.path.exists(env_file):
        print(f'   ✅ {env_file} mevcut')
    else:
        print(f'   ⚠️ {env_file} bulunamadı')

# 6. BUILD READİNESS
print(f'\n🔨 6. BUILD READİNESS')
print('-' * 50)

build_files = [
    '.next',
    'node_modules',
    'dist',
    'build'
]

for build_file in build_files:
    if os.path.exists(build_file):
        print(f'   📁 {build_file} mevcut')
    else:
        print(f'   ⚠️ {build_file} bulunamadı')

# 7. GIT DURUMU
print(f'\n📚 7. GIT DURUMU')
print('-' * 50)

if os.path.exists('.git'):
    print('   ✅ Git repository mevcut')
    # Git status kontrolü
    try:
        import subprocess
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print('   ⚠️ Uncommitted changes var')
            print(f'   📝 Değişiklikler: {len(result.stdout.splitlines())} dosya')
        else:
            print('   ✅ Working directory temiz')
    except:
        print('   ⚠️ Git status kontrolü yapılamadı')
else:
    print('   ❌ Git repository bulunamadı')

# 8. PRODUCTION READİNESS SCORE
print(f'\n🎯 8. PRODUCTION READİNESS SCORE')
print('-' * 50)

score = 0
max_score = 10

# Scoring criteria
if os.path.exists('package.json'): score += 1
if os.path.exists('next.config.js'): score += 1
if os.path.exists('src/app/page.tsx'): score += 1
if os.path.exists('src/lib/excel-utils.ts'): score += 1
if os.path.exists('data/aluplan-list.xlsx'): score += 1
if len(v2023_emails) > 0: score += 1
if len(v2022_emails) > 0: score += 1
if sales_hub_count > 0: score += 1
if os.path.exists('.git'): score += 1
if os.path.exists('README.md'): score += 1

percentage = (score / max_score) * 100
print(f'   📊 Production Readiness: {score}/{max_score} ({percentage:.1f}%)')

if percentage >= 90:
    print('   ✅ EXCELLENTRead! Production\'a hazır!')
elif percentage >= 70:
    print('   ⚠️ İYİ - Küçük düzeltmeler gerekli')
elif percentage >= 50:
    print('   ⚠️ ORTA - Önemli düzeltmeler gerekli')
else:
    print('   ❌ KÖTÜ - Major düzeltmeler gerekli')

print(f'\n' + '='*80)
print('🎯 SONUÇ VE ÖNERİLER')
print('=' * 80)
print('1. ✅ Veri tutarlılığı analiz edildi')
print('2. ✅ Proje yapısı kontrol edildi')
print('3. ✅ Production readiness değerlendirildi')
print('4. 🔄 GitHub stable release hazırlanacak')
print('5. 🌍 Plesk deployment yapılandırılacak')
print('6. 🔧 Development workflow optimize edilecek')
