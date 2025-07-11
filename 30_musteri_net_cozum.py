import pandas as pd

print('🎯 MÜŞTERİ İÇİN NET ÇÖZÜM ÖNERİSİ')
print('=' * 60)

# Ana veri dosyasını yükle
df = pd.read_excel('data/aluplan-list.xlsx')

print('📊 MEVCUT DURUM (SORUNLU):')
print('   V2023 ve üzeri: 128-129 (karışık)')
print('   V2022 ve eski: 800')
print('   Sales Hub Mevcut: 1,032')
print('   ❌ SORUN: Sayılar tutmuyor!')

print('\n' + '='*60)

print('🎯 ÖNERİLEN NET ÇÖZÜM:')
print('\n1️⃣ V2023+ SADECE Allplan Müşteriler Final\'dan:')
print('   📊 V2023 ve üzeri: 97 kayıt')
print('   📋 V2023: 23 + V2024: 29 + V2025: 60 = 112 kayıt → 97 unique email')
print('   ✅ Kaynak: Doğrudan Allplan müşteri veritabanı')
print('   ✅ Net: Hiç karışıklık yok')

print('\n2️⃣ V2022 ve eski AYNI KAL:')
print('   📊 V2022 ve eski: 800 kayıt')
print('   ✅ Kaynak: Email bazlı matching')

print('\n3️⃣ Sales Hub Mevcut AYNI KAL:')
print('   📊 Sales Hub Mevcut: 1,032 kayıt')
print('   ✅ Kaynak: Ana veri dosyası')

print('\n' + '='*60)

print('🧮 YENİ MATEMATİK:')
print('   V2023 ve üzeri: 97')
print('   V2022 ve eski: 800')
print('   Virtual Toplam: 97 + 800 = 897')
print('   Sales Hub Mevcut: 1,032')
print('   Fark: 1,032 - 897 = 135 (diğer kayıtlar)')
print('   ✅ MANTIKLI: Sales Hub > Virtual Toplam')

print('\n' + '='*60)

print('🎯 MÜŞTERİ SUNUM TABLOSU:')
print('┌─────────────────────────┬─────────┬─────────────────────────┐')
print('│ Segment                 │ Sayı    │ Kaynak                  │')
print('├─────────────────────────┼─────────┼─────────────────────────┤')
print('│ V2023 ve üzeri          │ 97      │ Allplan Müşteri DB      │')
print('│ V2022 ve eski           │ 800     │ Email Matching          │')
print('│ Sales Hub Mevcut        │ 1,032   │ Ana Veri Dosyası        │')
print('│ Mautic                  │ ???     │ Ana Veri Dosyası        │')
print('│ Potansiyel Müşteriler   │ ???     │ Ana Veri Dosyası        │')
print('└─────────────────────────┴─────────┴─────────────────────────┘')

print('\n' + '='*60)

print('🔧 UYGULAMA DEĞİŞİKLİĞİ:')
print('   ✅ V2023 filtresini değiştir')
print('   ✅ Sadece V2023_EMAILS listesini kullan')
print('   ✅ Segment V2023 kayıtlarını görmezden gel')
print('   ✅ Kod değişikliği: excel-utils.ts dosyasında')

print('\n❓ BU ÇÖZÜMÜ KABUL EDİYOR MUSUNUZ?')
print('   ✅ Evet → Kodu değiştirip V2023 = 97 yapacağım')
print('   ❌ Hayır → Başka bir yaklaşım önerebilirim')

# Diğer segment sayılarını da kontrol et
print('\n' + '='*60)
print('📊 DİĞER SEGMENT SAYILARI:')

# Mautic sayısı
mautic_count = df[df['segment'].astype(str).str.contains('Mautic', case=False, na=False)].shape[0]
print(f'   📊 Mautic: {mautic_count:,}')

# Potansiyel müşteriler
potansiyel_count = df[df['segment'].astype(str).str.contains('Potansiyel', case=False, na=False)].shape[0]
print(f'   📊 Potansiyel Müşteriler: {potansiyel_count:,}')

# Mevcut müşteriler
mevcut_count = df[df['segment'].astype(str).str.contains('Mevcut', case=False, na=False)].shape[0]
print(f'   📊 Mevcut Müşteriler: {mevcut_count:,}')

# Toplam
print(f'   📊 TOPLAM: {df.shape[0]:,}')

print('\n✅ GÜNCEL SUNUM TABLOSU:')
print('┌─────────────────────────┬─────────┐')
print('│ Segment                 │ Sayı    │')
print('├─────────────────────────┼─────────┤')
print(f'│ V2023 ve üzeri          │ 97      │')
print(f'│ V2022 ve eski           │ 800     │')
print(f'│ Sales Hub Mevcut        │ 1,032   │')
print(f'│ Mautic                  │ {mautic_count:,}     │')
print(f'│ Potansiyel Müşteriler   │ {potansiyel_count:,}     │')
print(f'│ Mevcut Müşteriler       │ {mevcut_count:,}   │')
print(f'│ TOPLAM                  │ {df.shape[0]:,}   │')
print('└─────────────────────────┴─────────┘')
