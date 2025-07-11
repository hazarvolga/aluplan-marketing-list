import pandas as pd

print('🎯 SALES HUB VE VIRTUAL SEGMENT TUTARSIZLIĞI ÇÖZÜMÜ')
print('=' * 60)

# Mevcut veri setini yükle
df_mevcut = pd.read_excel('data/aluplan-list.xlsx')

print('📊 MEVCUT DURUM ANALİZİ:')
print('=' * 40)

# Segment sayıları
segment_counts = df_mevcut['segment'].value_counts()
for segment, count in segment_counts.items():
    print(f'   📋 {segment}: {count:,}')

# Sales Hub Mevcut analizi
sales_hub_mevcut = df_mevcut[df_mevcut['segment'] == 'Sales Hub Mevcut']
print(f'\n📊 SALES HUB MEVCUT DETAYI:')
print(f'   📧 Toplam: {len(sales_hub_mevcut):,}')

# Source dağılımı
source_counts = sales_hub_mevcut['source'].value_counts()
null_sources = sales_hub_mevcut['source'].isna().sum()
print(f'   📂 Source dağılımı:')
for source, count in source_counts.items():
    print(f'      📁 {source}: {count:,}')
print(f'      📁 NULL/Missing: {null_sources:,}')

print(f'\n🔍 SORUN TESPİTİ:')
print('=' * 40)
print(f'   ❌ 973 kayıtın source bilgisi kayıp')
print(f'   ❌ Virtual segment tanımları eksik')
print(f'   ❌ Segment geçiş işlemlerinde data kaybı')

print(f'\n💡 ÇÖZÜM STRATEJİSİ:')
print('=' * 40)
print(f'   1️⃣ NULL source kayıtlarının gerçek kaynağını tespit et')
print(f'   2️⃣ Virtual segment tanımlarını net hale getir')
print(f'   3️⃣ Sales Hub Mevcut segmentini yeniden yapılandır')
print(f'   4️⃣ Data consistency kontrolü ekle')

# NULL source kayıtlarını analiz et
null_source_records = sales_hub_mevcut[sales_hub_mevcut['source'].isna()]
print(f'\n🔍 NULL SOURCE KAYITLARI ANALİZİ:')
print(f'   📧 Sayı: {len(null_source_records):,}')

# Email pattern analizi
print(f'   📧 İlk 10 örnek:')
for i, row in null_source_records[['email', 'name', 'company']].head(10).iterrows():
    print(f'      📧 {row["email"]} - {row["name"]} - {row["company"]}')

# Bu kayıtlar V2022/V2023 listelerinde var mı?
try:
    # V2022 emails
    with open('src/lib/v2022-emails.ts', 'r') as f:
        v2022_content = f.read()
        import re
        v2022_emails = set(re.findall(r'"([^"]+@[^"]+)"', v2022_content))
        v2022_emails = set(email.lower() for email in v2022_emails)
    
    # V2023 emails
    with open('src/data/v2023-emails.ts', 'r') as f:
        v2023_content = f.read()
        v2023_emails = set(re.findall(r'"([^"]+@[^"]+)"', v2023_content))
        v2023_emails = set(email.lower() for email in v2023_emails)
    
    # NULL source kayıtlarının email analizi
    null_emails = set(null_source_records['email'].str.lower().str.strip())
    
    # Çakışma analizi
    null_in_v2022 = null_emails.intersection(v2022_emails)
    null_in_v2023 = null_emails.intersection(v2023_emails)
    null_not_in_virtual = null_emails - v2022_emails - v2023_emails
    
    print(f'\n📊 NULL SOURCE KAYITLARININ VİRTUAL SEGMENT ANALİZİ:')
    print(f'   📧 NULL kayıtlar: {len(null_emails):,}')
    print(f'   📧 V2022\'de bulunan: {len(null_in_v2022):,}')
    print(f'   📧 V2023\'te bulunan: {len(null_in_v2023):,}')
    print(f'   📧 Hiçbirinde bulunmayan: {len(null_not_in_virtual):,}')
    
except Exception as e:
    print(f'   ❌ Virtual email listesi okunamadı: {e}')

print(f'\n🎯 ÇÖZÜM ADIMLARI:')
print('=' * 40)
print(f'   1. NULL source kayıtlarını virtual segmentlere eşle')
print(f'   2. Eşleşmeyen kayıtları "Sales Hub Dynamics" segmentine taşı')
print(f'   3. Virtual segment counts\'ı yeniden hesapla')
print(f'   4. Data consistency test et')

print(f'\n📝 UYGULAMA ÖNERİSİ:')
print('=' * 40)
print(f'   📊 Sales Hub Mevcut = V2022 Virtual + V2023 Virtual + Dynamics Real')
print(f'   📊 Bu şekilde matematik tutarlı olacak')
print(f'   📊 Filtering mantığı da doğru çalışacak')
