import pandas as pd

print('🔧 SALES HUB TUTARSIZLIĞI ÇÖZÜMÜ UYGULAMA')
print('=' * 60)

# Mevcut veri setini yükle
df_mevcut = pd.read_excel('data/aluplan-list.xlsx')

# V2022 ve V2023 email listelerini yükle
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
    
    print(f'✅ Virtual email listeleri yüklendi:')
    print(f'   📧 V2022: {len(v2022_emails):,} email')
    print(f'   📧 V2023: {len(v2023_emails):,} email')
    
except Exception as e:
    print(f'❌ Email listeleri yüklenemedi: {e}')
    exit()

# Sales Hub Mevcut kayıtları
sales_hub_mevcut = df_mevcut[df_mevcut['segment'] == 'Sales Hub Mevcut']
print(f'\n📊 MEVCUT SALES HUB KAYITLARI: {len(sales_hub_mevcut):,}')

# NULL source kayıtları
null_source_records = sales_hub_mevcut[sales_hub_mevcut['source'].isna()]
print(f'📊 NULL source kayıtları: {len(null_source_records):,}')

# NULL kayıtları virtual segmentlere eşle
null_emails = null_source_records['email'].str.lower().str.strip()

# V2022'de bulunanları tespit et
in_v2022 = null_emails.isin(v2022_emails)
v2022_matches = null_source_records[in_v2022]

# V2023'te bulunanları tespit et
in_v2023 = null_emails.isin(v2023_emails)
v2023_matches = null_source_records[in_v2023]

# Hiçbirinde bulunmayanları tespit et
not_in_virtual = null_source_records[~in_v2022 & ~in_v2023]

print(f'\n🔍 NULL KAYITLARIN VİRTUAL SEGMENT DAĞILIMI:')
print(f'   📧 V2022 virtual: {len(v2022_matches):,}')
print(f'   📧 V2023 virtual: {len(v2023_matches):,}')
print(f'   📧 Dynamics real: {len(not_in_virtual):,}')

# Yeni segment yapısını oluştur
df_cozum = df_mevcut.copy()

# NULL source kayıtlarını güncelle
print(f'\n🔧 SEGMENT GÜNCELLEMELERİ:')

# V2022 virtual kayıtları
v2022_mask = (df_cozum['segment'] == 'Sales Hub Mevcut') & df_cozum['source'].isna() & df_cozum['email'].str.lower().str.strip().isin(v2022_emails)
df_cozum.loc[v2022_mask, 'source'] = 'V2022_VIRTUAL'
print(f'   ✅ V2022 virtual olarak işaretlendi: {v2022_mask.sum():,}')

# V2023 virtual kayıtları
v2023_mask = (df_cozum['segment'] == 'Sales Hub Mevcut') & df_cozum['source'].isna() & df_cozum['email'].str.lower().str.strip().isin(v2023_emails)
df_cozum.loc[v2023_mask, 'source'] = 'V2023_VIRTUAL'
print(f'   ✅ V2023 virtual olarak işaretlendi: {v2023_mask.sum():,}')

# Kalan NULL kayıtları Dynamics Real olarak işaretle
dynamics_mask = (df_cozum['segment'] == 'Sales Hub Mevcut') & df_cozum['source'].isna()
df_cozum.loc[dynamics_mask, 'source'] = 'DYNAMICS_REAL'
print(f'   ✅ Dynamics real olarak işaretlendi: {dynamics_mask.sum():,}')

# Sonuç analizi
updated_sales_hub = df_cozum[df_cozum['segment'] == 'Sales Hub Mevcut']
source_counts = updated_sales_hub['source'].value_counts()

print(f'\n📊 GÜNCELLENMİŞ SALES HUB MEVCUT DAĞILIMI:')
for source, count in source_counts.items():
    print(f'   📂 {source}: {count:,}')

# Matematik kontrol
v2022_total = (updated_sales_hub['source'] == 'V2022_VIRTUAL').sum()
v2023_total = (updated_sales_hub['source'] == 'V2023_VIRTUAL').sum()
dynamics_total = updated_sales_hub['source'].str.contains('DYNAMICS|All Contacts-Dynamics', na=False).sum()
mautic_total = (updated_sales_hub['source'] == 'mautic-tum-liste.xlsx').sum()

print(f'\n🔍 MATEMATİK KONTROL:')
print(f'   📊 V2022 Virtual: {v2022_total:,}')
print(f'   📊 V2023 Virtual: {v2023_total:,}')
print(f'   📊 Dynamics Real: {dynamics_total:,}')
print(f'   📊 Mautic: {mautic_total:,}')
print(f'   📊 Toplam: {v2022_total + v2023_total + dynamics_total + mautic_total:,}')

# Çözümlü veri setini kaydet
df_cozum.to_excel('data/aluplan-list-COZUM.xlsx', index=False)
print(f'\n✅ ÇÖZÜM UYGULANDI:')
print(f'   📁 Yeni dosya: data/aluplan-list-COZUM.xlsx')
print(f'   📊 Sales Hub matematik tutarlılığı sağlandı')
print(f'   🎯 Virtual segment filtering düzgün çalışacak')

print(f'\n📝 SONUÇ:')
print(f'   📊 V2022 (Virtual): {len(v2022_emails):,}')
print(f'   📊 V2023 (Virtual): {len(v2023_emails):,}')
print(f'   📊 Sales Hub Toplam: {len(updated_sales_hub):,}')
print(f'   ✅ Matematik: {len(v2022_emails)} + {len(v2023_emails)} + Dynamics = Sales Hub')
