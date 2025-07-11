import pandas as pd

print('🎯 V2023 VE ÜZERİ NET BİLGİ ANALİZİ')
print('=' * 60)

# Ana veri dosyasını yükle
df = pd.read_excel('data/aluplan-list.xlsx')

# Segment'te V2023 geçen kayıtları detaylı analiz et
v2023_segment = df[df['segment'].astype(str).str.contains('V2023', case=False, na=False)]

print('📊 ANA VERİ DOSYASI - SEGMENT V2023:')
print(f'   📝 Toplam kayıt: {len(v2023_segment):,}')
print(f'   📧 Unique email: {v2023_segment["email"].nunique():,}')
print(f'   🏢 Unique şirket: {v2023_segment["company"].nunique():,}')

# Segment detayları
print('\n🔍 SEGMENT DETAYLARI:')
segment_types = v2023_segment['segment'].value_counts()
for segment, count in segment_types.items():
    print(f'   📋 {segment}: {count:,}')

# İlk 10 kayıt
print('\n📋 İLK 10 KAYIT:')
for i, row in v2023_segment.head(10).iterrows():
    print(f'   📧 {row["email"]} | {row["company"]} | {row["name"]}')

print('\n' + '='*60)

# Allplan Müşteriler Final dosyasını yükle
print('📊 ALLPLAN MÜŞTERİLER FINAL - V2023+:')
df_final = pd.read_excel('veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28.xlsx', sheet_name='Müşteri Allplan')

version_sutunu = 'Unnamed: 5'  # Kalıcı/SUB/SSA sütunu
email_sutunu = 'Unnamed: 10'   # Main E-Mail sütunu

v2023_plus = df_final[df_final[version_sutunu].astype(str).str.contains('V202[345]', case=False, na=False)]
print(f'   📝 Toplam kayıt: {len(v2023_plus):,}')
print(f'   📧 Unique email: {v2023_plus[email_sutunu].nunique():,}')

# Version dağılımı
version_dagilimi = v2023_plus[version_sutunu].value_counts()
print(f'\n📊 VERSION DAĞILIMI:')
for version, count in version_dagilimi.items():
    print(f'   📋 {version}: {count:,}')

print('\n' + '='*60)

print('🤔 KARŞILAŞTIRMA VE ÖNERI:')
print('\n📊 KAYNAK 1: Ana Veri Dosyası')
print(f'   ✅ Segment "V2023 ve üzeri": {len(v2023_segment):,} kayıt')
print(f'   ✅ Diğer verilerle entegre: Evet')
print(f'   ❓ Kaynak belirsizliği: Var')

print('\n📊 KAYNAK 2: Allplan Müşteriler Final')
print(f'   ✅ V2023+ müşteriler: {len(v2023_plus):,} kayıt')
print(f'   ✅ Doğrudan Allplan\'dan: Evet')
print(f'   ✅ Version bilgisi net: Evet')

print('\n🎯 NET BİLGİ İÇİN ÖNERİLER:')
print('   1️⃣ SADECE Allplan Müşteriler Final kullan (97 kayıt)')
print('   2️⃣ SADECE Ana veri dosyası segment kullan (31 kayıt)')
print('   3️⃣ İKİSİNİ BİRLEŞTİR ama net açıklama yap (128 kayıt)')

print('\n❓ HANGİ YAKLAŞIM TERCİH EDİLİYOR?')
print('   A) Sadece Allplan Müşteriler Final → V2023+ = 97')
print('   B) Sadece Ana veri segment → V2023+ = 31')
print('   C) Birleşim → V2023+ = 128')

# Kesişim kontrol et
segment_emails = set(v2023_segment['email'].astype(str).str.lower().str.strip())
allplan_emails = set(v2023_plus[email_sutunu].astype(str).str.lower().str.strip())
intersection = segment_emails & allplan_emails

print(f'\n🔄 KESİŞİM ANALİZİ:')
print(f'   📧 Ortak email: {len(intersection):,}')
print(f'   📋 Sadece segment\'te: {len(segment_emails - allplan_emails):,}')
print(f'   📋 Sadece Allplan\'da: {len(allplan_emails - segment_emails):,}')

if len(intersection) > 0:
    print(f'\n📧 ORTAK EMAİLLER:')
    for email in sorted(intersection)[:5]:
        print(f'   📧 {email}')
