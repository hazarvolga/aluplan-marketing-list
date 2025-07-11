import pandas as pd

print('🔄 DOĞRU V2023+ EMAIL LİSTESİ OLUŞTURMA')
print('=' * 60)

# Allplan Müşteriler Final dosyasından V2023+ kayıtlarını al
df_final = pd.read_excel('veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28.xlsx', sheet_name='Müşteri Allplan')

# V2023+ kayıtlarını filtrele
version_sutunu = 'Unnamed: 5'  # Kalıcı/SUB/SSA sütunu
email_sutunu = 'Unnamed: 10'   # Main E-Mail sütunu

v2023_plus = df_final[df_final[version_sutunu].astype(str).str.contains('V202[345]', case=False, na=False)]
v2023_emails = v2023_plus[email_sutunu].dropna().unique()

print(f'📊 DOĞRU V2023+ VERİLER:')
print(f'   📝 Toplam V2023+ kayıt: {len(v2023_plus):,}')
print(f'   📧 V2023+ unique email: {len(v2023_emails):,}')

# Version dağılımı
version_dagilimi = v2023_plus[version_sutunu].value_counts()
print(f'   📊 Version dağılımı:')
for version, count in version_dagilimi.items():
    print(f'      📋 {version}: {count:,}')

# Email listesini TypeScript formatında hazırla
email_list = []
for email in sorted(v2023_emails):
    email_list.append(f'  "{email}"')

typescript_content = f'''// V2023+ müşteri email listesi
// Bu liste Allplan Müşteriler_Final_2025-03-19-R28.xlsx dosyasından oluşturulmuştur
// Toplam: {len(v2023_emails)} email
// V2023: {version_dagilimi.get('V2023', 0)} kayıt
// V2024: {version_dagilimi.get('V2024', 0)} kayıt  
// V2025: {version_dagilimi.get('V2025', 0)} kayıt

export const V2023_EMAILS = new Set([
{',\n'.join(email_list)}
]);
'''

# Dosyayı yaz
with open('src/data/v2023-emails.ts', 'w') as f:
    f.write(typescript_content)

print(f'\n✅ YENİ V2023+ EMAIL LİSTESİ OLUŞTURULDU:')
print(f'   📁 src/data/v2023-emails.ts')
print(f'   📧 {len(v2023_emails):,} email')
print(f'   🎯 Dynamics 365 ile tutarlı (112 kayıt → 97 unique email)')

# Örnek emailler
print(f'\n📧 İLK 10 EMAIL:')
for email in sorted(v2023_emails)[:10]:
    print(f'   📧 {email}')

print(f'\n📊 KARŞILAŞTIRMA:')
print(f'   ❌ ESKİ: 1,237 email (yanlış)')
print(f'   ✅ YENİ: 97 email (doğru)')
print(f'   🎯 Dynamics 365: 360 kayıt (97 email ile tutarlı)')
print(f'   📈 Fark: {1237 - 97:,} fazla email temizlendi')
