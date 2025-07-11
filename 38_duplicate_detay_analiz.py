import pandas as pd

print('🔍 DUPLICATE EMAIL DETAY ANALİZİ')
print('=' * 60)

# Ana veri dosyasını yükle
df = pd.read_excel('data/aluplan-list.xlsx')

print('📊 1. DUPLICATE EMAIL SAYIMI')
print('-' * 50)

# Email sayımı
emails = df['email'].dropna().tolist()
email_counts = {}
for email in emails:
    email_counts[email] = email_counts.get(email, 0) + 1

# Duplicate emailler
duplicate_emails = {email: count for email, count in email_counts.items() if count > 1}

print(f'   📧 Toplam email: {len(emails):,}')
print(f'   🔄 Unique email: {len(email_counts):,}')
print(f'   🚫 Duplicate email türü: {len(duplicate_emails):,}')

# Duplicate sayım yöntemleri
method1 = len(duplicate_emails)  # Unique duplicate email sayısı
method2 = sum(count for count in email_counts.values() if count > 1)  # Duplicate kayıt sayısı
method3 = len(emails) - len(set(emails))  # Fazla kayıt sayısı

print(f'\n📊 FARKLI SAYIM YÖNTEMLERİ:')
print(f'   1️⃣ Unique duplicate email sayısı: {method1}')
print(f'   2️⃣ Duplicate kayıt sayısı: {method2}')
print(f'   3️⃣ Fazla kayıt sayısı: {method3}')

print(f'\n📋 DUPLICATE EMAIL DETAYLARI:')
for email, count in duplicate_emails.items():
    print(f'   📧 {email}: {count} kez tekrar ediyor')

print(f'\n📊 2. DUPLICATE KAYITLARIN DETAY ANALİZİ')
print('-' * 50)

# Her duplicate email için detay
for email, count in duplicate_emails.items():
    print(f'\n   🔍 {email} ({count} kayıt):')
    duplicate_rows = df[df['email'] == email]
    
    for i, (index, row) in enumerate(duplicate_rows.iterrows(), 1):
        print(f'      {i}. {row["name"]} - {row["company"]} - {row["segment"]}')

print(f'\n📊 3. DUPLICATE SORUN ANALİZİ')
print('-' * 50)

print('   🔍 Duplicate emailler neden sorun?')
print('   1. 🚫 Müşteriye aynı email birden fazla gönderilir')
print('   2. 📊 Pazarlama istatistikleri yanıltıcı olur')
print('   3. 💰 Email maliyeti artar')
print('   4. 📧 Spam olarak işaretlenme riski')
print('   5. 🎯 Hedef kitle analizi bozulur')

print(f'\n📊 4. ÇÖZÜM ÖNERİLERİ')
print('-' * 50)

print('   💡 Çözüm seçenekleri:')
print('   1. ✅ MANUEL KONTROL: Her duplicate manuel incelenir')
print('   2. ✅ OTOMATIK TEMİZLİK: İlk kaydı tut, diğerlerini sil')
print('   3. ✅ MERGE STRATEGI: Bilgileri birleştir')
print('   4. ✅ SEGMENT ÖNCELIK: En değerli segmenti tut')

print(f'\n📊 5. MANUEL KONTROL DETAYI')
print('-' * 50)

for email, count in duplicate_emails.items():
    print(f'\n   🔍 {email}:')
    duplicate_rows = df[df['email'] == email]
    
    # Segment analizi
    segments = duplicate_rows['segment'].unique()
    companies = duplicate_rows['company'].dropna().unique()
    names = duplicate_rows['name'].dropna().unique()
    
    print(f'      📊 Farklı segment: {len(segments)} ({", ".join(str(s) for s in segments)})')
    print(f'      🏢 Farklı company: {len(companies)} ({", ".join(str(c) for c in companies)})')
    print(f'      👤 Farklı name: {len(names)} ({", ".join(str(n) for n in names)})')
    
    # Öneri
    if len(segments) > 1:
        print(f'      💡 ÖNERİ: Segment çakışması var - Manuel kontrol gerekli')
    elif len(companies) > 1:
        print(f'      💡 ÖNERİ: Şirket değişimi var - Manuel kontrol gerekli')
    elif len(names) > 1:
        print(f'      💡 ÖNERİ: İsim farklılığı var - Manuel kontrol gerekli')
    else:
        print(f'      💡 ÖNERİ: Tamamen aynı - Otomatik silinebilir')

print(f'\n📊 6. FRONTEND ETKİSİ')
print('-' * 50)

print('   🎯 Frontend\'te duplicate sayısı gösteriliyor:')
print(f'   📊 Gösterilen: {method2} kayıt')
print(f'   📧 Gerçek duplicate email: {method1} adet')
print(f'   🔄 Fazla kayıt: {method3} adet')

print(f'\n   📋 Müşteriye açıklama:')
print(f'   "Sistemde {method1} email adresi tekrar ediyor."')
print(f'   "Toplamda {method2} duplicate kayıt var."')
print(f'   "Bu kayıtlar manuel kontrol edilmeli."')

print(f'\n🎯 SONUÇ VE ÖNERİ')
print('=' * 60)

if method1 <= 10:
    print('✅ DÜŞÜK RİSK: Duplicate sayısı düşük')
    print('💡 ÖNERİ: Manuel kontrol yapılabilir')
    print('🔧 EYLEM: Her duplicate email tek tek incelenir')
else:
    print('⚠️ YÜKSEK RİSK: Duplicate sayısı yüksek')
    print('💡 ÖNERİ: Otomatik temizlik stratejisi')
    print('🔧 EYLEM: Toplu temizlik algoritması')

print(f'\n📊 DUPLICATE ETKİSİ:')
print(f'   📧 Temiz email sayısı: {len(set(emails)):,}')
print(f'   🚫 Duplicate kayıt sayısı: {method2}')
print(f'   📊 Veri kalitesi etkisi: %{(method2/len(emails)*100):.2f}')

print(f'\n🚀 EYLEM PLANI:')
print(f'   1. ✅ Duplicate kayıtları listele')
print(f'   2. 🔍 Manuel kontrol yap')
print(f'   3. 💡 Temizlik stratejisi belirle')
print(f'   4. 🔧 Temizlik işlemini uygula')
print(f'   5. ✅ Sonuçları doğrula')
