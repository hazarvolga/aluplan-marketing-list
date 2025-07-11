import pandas as pd
import numpy as np

print("🔍 MEVCUT MÜŞTERİLER TUTARSIZLIK ANALİZİ")
print("=" * 60)

# Mevcut veri setini yükle
df_mevcut = pd.read_excel('data/aluplan-list.xlsx')
print(f"📊 MEVCUT VERİ SETİ:")
print(f"   📝 Toplam kayıt: {len(df_mevcut):,}")

# Segment dağılımı
segment_dagilimi = df_mevcut['segment'].value_counts()
print(f"\n🎯 MEVCUT SEGMENT DAĞILIMI:")
for segment, count in segment_dagilimi.items():
    print(f"   📋 {segment}: {count:,} kayıt")

# Dynamics 365 verilerini yükle
df_dynamics = pd.read_excel('veri_kaynaklari/All Contacts-Dynamics-365.xlsx')
df_dynamics_temiz = df_dynamics.dropna(subset=['Email'])
df_dynamics_temiz = df_dynamics_temiz[df_dynamics_temiz['Email'].str.contains('@', na=False)]
dynamics_emails = set(df_dynamics_temiz['Email'].str.lower().str.strip())

print(f"\n📦 DYNAMICS 365 VERİLERİ:")
print(f"   📧 Dynamics geçerli email: {len(dynamics_emails):,}")

# Mevcut Müşteriler segmentindeki kayıtları analiz et
mevcut_musteriler = df_mevcut[df_mevcut['segment'] == 'Mevcut Müşteriler']
print(f"\n🔍 MEVCUT MÜŞTERİLER ANALİZİ:")
print(f"   📝 Toplam Mevcut Müşteriler: {len(mevcut_musteriler):,}")

# Mevcut Müşteriler'den hangilerinin Dynamics'te olduğunu kontrol et
mevcut_musteriler['email_lower'] = mevcut_musteriler['email'].str.lower().str.strip()
mevcut_musteriler['dynamics_var'] = mevcut_musteriler['email_lower'].isin(dynamics_emails)

dynamics_te_olan = mevcut_musteriler[mevcut_musteriler['dynamics_var'] == True]
dynamics_te_olmayan = mevcut_musteriler[mevcut_musteriler['dynamics_var'] == False]

print(f"\n📊 MEVCUT MÜŞTERİLER DYNAMICS DURUMU:")
print(f"   ✅ Dynamics'te olan: {len(dynamics_te_olan):,} kayıt")
print(f"   ❌ Dynamics'te olmayan: {len(dynamics_te_olmayan):,} kayıt")

# Sales Hub Mevcut segmentindeki kayıtları analiz et
sales_hub_mevcut = df_mevcut[df_mevcut['segment'] == 'Sales Hub Mevcut']
sales_hub_mevcut['email_lower'] = sales_hub_mevcut['email'].str.lower().str.strip()
sales_hub_mevcut['dynamics_var'] = sales_hub_mevcut['email_lower'].isin(dynamics_emails)

sales_hub_dynamics = sales_hub_mevcut[sales_hub_mevcut['dynamics_var'] == True]
sales_hub_dynamics_degil = sales_hub_mevcut[sales_hub_mevcut['dynamics_var'] == False]

print(f"\n📊 SALES HUB MEVCUT DYNAMICS DURUMU:")
print(f"   ✅ Dynamics'te olan: {len(sales_hub_dynamics):,} kayıt")
print(f"   ❌ Dynamics'te olmayan: {len(sales_hub_dynamics_degil):,} kayıt")

# Kaynak dosya analizi
print(f"\n📁 KAYNAK DOSYA ANALİZİ:")
print(f"   Dynamics'te olmayan Mevcut Müşteriler kaynağı:")
kaynak_dagilimi = dynamics_te_olmayan['source'].value_counts()
for kaynak, count in kaynak_dagilimi.items():
    print(f"     📋 {kaynak}: {count:,} kayıt")

print(f"\n💡 SORUN TESPİTİ:")
print(f"   🔍 Dynamics'te olan {len(dynamics_te_olan):,} Mevcut Müşteri")
print(f"   🔍 Sales Hub'a taşınmamış durumdalar")
print(f"   🔍 Bu kayıtlar Sales Hub Mevcut'a taşınmalı")

# Çözüm önerisi
print(f"\n🎯 ÇÖZÜM ÖNERİSİ:")
print(f"   1. Dynamics'te olan {len(dynamics_te_olan):,} Mevcut Müşteri → Sales Hub Mevcut")
print(f"   2. Dynamics'te olmayan {len(dynamics_te_olmayan):,} kayıt → Mevcut Müşteriler'de kalsın")
print(f"   3. Sonuç: Sales Hub Mevcut ~{len(sales_hub_mevcut) + len(dynamics_te_olan):,} kayıt")
print(f"   4. Sonuç: Mevcut Müşteriler ~{len(dynamics_te_olmayan):,} kayıt")

# Örnek veriler
if len(dynamics_te_olan) > 0:
    print(f"\n📋 DYNAMICS'TE OLAN MEVCUT MÜŞTERİLER ÖRNEKLERI:")
    print(dynamics_te_olan[['name', 'email', 'company', 'source']].head(10).to_string(index=False))

if len(dynamics_te_olmayan) > 0:
    print(f"\n📋 DYNAMICS'TE OLMAYAN MEVCUT MÜŞTERİLER ÖRNEKLERI:")
    print(dynamics_te_olmayan[['name', 'email', 'company', 'source']].head(10).to_string(index=False))

print(f"\n" + "=" * 60)
print("🔍 TUTARSIZLIK ANALİZİ TAMAMLANDI")
print("=" * 60)
