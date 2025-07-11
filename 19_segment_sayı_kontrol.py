import pandas as pd

print("🔍 SEGMENT SAYILARINI ANALİZ EDİYORUM")
print("=" * 60)

# Mevcut veri setini yükle
df = pd.read_excel('data/aluplan-list.xlsx')
print(f"📊 MEVCUT VERİ SETİ:")
print(f"   📝 Toplam kayıt: {len(df):,}")

# Segment analizi
segment_counts = df['segment'].value_counts()
print(f"\n🎯 SEGMENT DAĞILIMI:")
for segment, count in segment_counts.items():
    print(f"   📋 {segment}: {count:,} kayıt")

# V2022 ve V2023 kontrolü
v2022_count = df[df['segment'] == 'V2022 ve eski'].shape[0]
v2023_count = df[df['segment'] == 'V2023 ve üzeri'].shape[0]

print(f"\n🔍 V2022 VE V2023 DURUM:")
print(f"   📊 V2022 ve eski: {v2022_count:,} kayıt")
print(f"   📊 V2023 ve üzeri: {v2023_count:,} kayıt")

# Mevcut kayıtlarda V2022/V2023 segment'i var mı?
v2022_kayitlar = df[df['segment'] == 'V2022 ve eski']
v2023_kayitlar = df[df['segment'] == 'V2023 ve üzeri']

if len(v2022_kayitlar) > 0:
    print(f"\n📋 V2022 KAYITLARI:")
    print(v2022_kayitlar[['id', 'name', 'email', 'company', 'source']].head().to_string(index=False))
else:
    print(f"\n❌ V2022 segmentinde kayıt yok")

if len(v2023_kayitlar) > 0:
    print(f"\n📋 V2023 KAYITLARI:")
    print(v2023_kayitlar[['id', 'name', 'email', 'company', 'source']].head().to_string(index=False))
else:
    print(f"\n❌ V2023 segmentinde kayıt yok")

print(f"\n✅ ANALİZ TAMAMLANDI")
print("=" * 60)
