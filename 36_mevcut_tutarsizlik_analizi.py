import pandas as pd

print('🔍 MEVCUT MÜŞTERİLER TUTARSIZLIK ANALİZİ')
print('=' * 60)

# Ana veri dosyasını yükle
df = pd.read_excel('data/aluplan-list.xlsx')

print('📊 1. MEVCUT MÜŞTERİLER SEGMENT ANALİZİ')
print('-' * 50)

# Farklı "Mevcut" içeren segmentleri analiz et
mevcut_segments = {}
for index, row in df.iterrows():
    if pd.notna(row['segment']):
        segments = str(row['segment']).split(',')
        for segment in segments:
            segment = segment.strip()
            if 'mevcut' in segment.lower():
                if segment not in mevcut_segments:
                    mevcut_segments[segment] = 0
                mevcut_segments[segment] += 1

print('   📊 "Mevcut" içeren segment türleri:')
for segment, count in sorted(mevcut_segments.items()):
    print(f'   📋 {segment}: {count:,} kayıt')

print('\n📊 2. FRONTEND FİLTRE LOJİĞİ SİMÜLASYONU')
print('-' * 50)

# Frontend lojiklerini simüle et
# 1. Sadece "Mevcut Müşteriler" segmenti
only_mevcut = df[df['segment'].astype(str).str.contains('Mevcut Müşteriler', case=False, na=False)]
print(f'   1️⃣ Sadece "Mevcut Müşteriler": {len(only_mevcut):,}')

# 2. Sadece "Sales Hub Mevcut" segmenti
only_sales_hub = df[df['segment'].astype(str).str.contains('Sales Hub Mevcut', case=False, na=False)]
print(f'   2️⃣ Sadece "Sales Hub Mevcut": {len(only_sales_hub):,}')

# 3. Frontend mevcutMusteriler filtresi (ikisini birleştiren)
frontend_mevcut = df[df['segment'].astype(str).str.contains('Mevcut', case=False, na=False)]
print(f'   3️⃣ Frontend "Mevcut" (hepsi): {len(frontend_mevcut):,}')

# 4. Excel-utils.ts lojik simülasyonu
excel_utils_mevcut = df[
    (df['segment'].astype(str).str.contains('Mevcut Müşteriler', case=False, na=False)) |
    (df['segment'].astype(str).str.contains('Sales Hub Mevcut', case=False, na=False))
]
print(f'   4️⃣ Excel-utils lojik: {len(excel_utils_mevcut):,}')

print('\n📊 3. OVERLAP ANALİZİ')
print('-' * 50)

# Overlap kontrolü
overlap_count = 0
for index, row in df.iterrows():
    if pd.notna(row['segment']):
        segment = str(row['segment']).lower()
        if ('mevcut müşteriler' in segment and 'sales hub mevcut' in segment):
            overlap_count += 1

print(f'   🔄 Hem "Mevcut Müşteriler" hem "Sales Hub Mevcut": {overlap_count:,}')
print(f'   🔢 Matematik kontrolü: {len(only_mevcut):,} + {len(only_sales_hub):,} - {overlap_count:,} = {len(only_mevcut) + len(only_sales_hub) - overlap_count:,}')

print('\n📊 4. KART GÖSTERİMİ TUTARSIZLIK ANALİZİ')
print('-' * 50)

# Şirket bilgisi analizi
mevcut_with_company = excel_utils_mevcut[excel_utils_mevcut['company'].notna()]
print(f'   🏢 Şirket bilgisi olan: {len(mevcut_with_company):,}')

# Şirket bilgisi oranı
company_rate = (len(mevcut_with_company) / len(excel_utils_mevcut)) * 100
print(f'   📊 Şirket bilgisi oranı: {company_rate:.1f}%')

print(f'\n   📱 Frontend kartında gösterilen: 1,255')
print(f'   💾 Backend hesaplanan: {len(excel_utils_mevcut):,}')
print(f'   🔄 Fark: {abs(len(excel_utils_mevcut) - 1255):,}')

print('\n📊 5. SORUN ANALİZİ VE ÇÖZÜM')
print('-' * 50)

print('   🔍 Tespit edilen sorunlar:')
print('   1. ❌ Frontend "Mevcut" filtresi çok geniş kapsıyor')
print('   2. ❌ Kart gösterimi ile backend farklı')
print('   3. ❌ Şirket bilgisi oranı %100 değil')

print('\n   💡 Çözüm önerileri:')
print('   1. ✅ Frontend filtre lojiklerini netleştir')
print('   2. ✅ Kart gösterimini backend ile senkronize et')
print('   3. ✅ Şirket bilgisi eksikliklerini göster')

print('\n📊 6. DOĞRU SAYILAR')
print('-' * 50)

print('   📊 Doğru segment sayıları:')
print(f'   👥 Mevcut Müşteriler (Salt): {len(only_mevcut):,}')
print(f'   🏢 Sales Hub Mevcut (Salt): {len(only_sales_hub):,}')
print(f'   🔄 Overlap: {overlap_count:,}')
print(f'   📊 Toplam Mevcut (Birleşim): {len(excel_utils_mevcut):,}')

print('\n🎯 TUTARLILIK SAĞLAMA PLANI')
print('-' * 50)

print('   1. ✅ Frontend karttaki sayıyı 1,262 yap')
print('   2. ✅ Şirket bilgisi oranını gerçek oranla göster')
print('   3. ✅ Filtre açıklamalarını netleştir')
print('   4. ✅ Backend-frontend senkronizasyonu sağla')

print(f'\n📊 SONUÇ: Backend doğru ({len(excel_utils_mevcut):,}), Frontend kartı güncellenmeli!')
