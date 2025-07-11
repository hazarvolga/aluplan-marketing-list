import pandas as pd

print('🔍 DUPLICATE EMAIL ANALİZİ')
print('=' * 50)

# Ana veri dosyasını yükle
df = pd.read_excel('data/aluplan-list.xlsx')

print(f'📊 TOPLAM KAYIT: {len(df):,}')
print(f'📧 TOPLAM EMAIL: {df["email"].count():,}')
print(f'📧 UNIQUE EMAIL: {df["email"].nunique():,}')
print(f'🔄 DUPLICATE EMAIL: {df["email"].count() - df["email"].nunique():,}')

# Duplicate emailleri bul
duplicates = df[df.duplicated(subset=['email'], keep=False)]
print(f'\n📋 DUPLICATE EMAIL KAYITLARI:')
print(f'   📧 Duplicate içeren kayıt: {len(duplicates):,}')
print(f'   📧 Unique duplicate email: {duplicates["email"].nunique():,}')

# İlk 10 duplicate email örneği
print(f'\n📧 İLK 10 DUPLICATE EMAIL:')
duplicate_emails = df[df.duplicated(subset=['email'], keep=False)]['email'].value_counts().head(10)
for email, count in duplicate_emails.items():
    print(f'   📧 {email}: {count} kez')

# Duplicate email kayıtlarının segment dağılımı
print(f'\n📊 DUPLICATE EMAIL SEGMENT DAĞILIMI:')
duplicate_segments = duplicates['segment'].value_counts()
for segment, count in duplicate_segments.head(10).items():
    print(f'   📋 {segment}: {count:,}')

# Duplicate email kayıtlarının source dağılımı
print(f'\n📊 DUPLICATE EMAIL SOURCE DAĞILIMI:')
duplicate_sources = duplicates['source'].value_counts()
for source, count in duplicate_sources.head(10).items():
    print(f'   📋 {source}: {count:,}')

print(f'\n🔍 DUPLICATE EMAIL DETAY ANALİZİ:')
# En çok duplicate olan emaili detaylandır
if len(duplicate_emails) > 0:
    most_duplicate_email = duplicate_emails.index[0]
    email_records = df[df['email'] == most_duplicate_email]
    print(f'   📧 Email: {most_duplicate_email}')
    print(f'   📝 Kayıt sayısı: {len(email_records)}')
    print(f'   📊 Segmentler: {list(email_records["segment"].unique())}')
    print(f'   📊 Kaynaklar: {list(email_records["source"].unique())}')
    print(f'   📊 Şirketler: {list(email_records["company"].unique())}')

print(f'\n🔧 ÇÖZÜM ÖNERİLERİ:')
print('1. ✅ Duplicate email filtreleme fonksiyonunu düzelt')
print('2. ✅ Frontend UI\'da duplicate gösterimini düzelt')
print('3. ✅ Data quality stats hesaplamasını kontrol et')
print('4. ⚠️ Duplicate kayıtları birleştirme seçeneği sun')
print('5. ⚠️ Duplicate kayıtları silme seçeneği sun')

print(f'\n📋 FRONTEND DUPLICATE FILTER DURUMU:')
print('   🔍 Duplicate email filtresi aktif edildiğinde kayıt gösterilmiyor')
print('   ❌ Bu durum duplicate kayıtların filtrelemede sorun olduğunu gösterir')
print('   ✅ excel-utils.ts dosyasındaki filterData fonksiyonu kontrol edilmeli')
