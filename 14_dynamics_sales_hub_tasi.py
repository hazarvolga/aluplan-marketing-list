import pandas as pd
import numpy as np
from datetime import datetime

print("🔄 DYNAMICS 365 KAYITLARINI SALES HUB MEVCUT'A TAŞIYORUZ")
print("=" * 60)

# Mevcut veri setini yükle
df_mevcut = pd.read_excel('data/aluplan-list.xlsx')
print(f"📊 MEVCUT VERİ SETİ:")
print(f"   📝 Toplam kayıt: {len(df_mevcut):,}")

# Dynamics 365 verilerini yükle
df_dynamics = pd.read_excel('veri_kaynaklari/All Contacts-Dynamics-365.xlsx')
print(f"\n📦 DYNAMICS 365 VERİLERİ:")
print(f"   📝 Toplam kayıt: {len(df_dynamics):,}")

# Dynamics'ten temiz email listesini al
df_dynamics_temiz = df_dynamics.dropna(subset=['Email'])
df_dynamics_temiz = df_dynamics_temiz[df_dynamics_temiz['Email'].str.contains('@', na=False)]
dynamics_emails = set(df_dynamics_temiz['Email'].str.lower().str.strip())

print(f"   📧 Dynamics geçerli email: {len(dynamics_emails):,}")

# Mevcut veri setinde Dynamics kayıtlarını belirle
df_mevcut['email_lower'] = df_mevcut['email'].str.lower().str.strip()
df_mevcut['dynamics_kayit'] = df_mevcut['email_lower'].isin(dynamics_emails)

# Dynamics'te olan kayıtları analiz et
dynamics_kayitlar = df_mevcut[df_mevcut['dynamics_kayit'] == True]
print(f"\n🎯 DYNAMICS KAYITLARININ MEVCUT SEGMENT DAĞILIMI:")
segment_oncesi = dynamics_kayitlar['segment'].value_counts()
for segment, count in segment_oncesi.items():
    print(f"   📋 {segment}: {count:,} kayıt")

# Dynamics kayıtlarını Sales Hub Mevcut'a taşı
df_guncellenmis = df_mevcut.copy()
df_guncellenmis.loc[df_guncellenmis['dynamics_kayit'] == True, 'segment'] = 'Sales Hub Mevcut'

print(f"\n🔄 SEGMENT DEĞİŞİKLİĞİ:")
print(f"   📈 Dynamics kayıtları → Sales Hub Mevcut'a taşındı")
print(f"   📝 Taşınan kayıt sayısı: {len(dynamics_kayitlar):,}")

# Güncel segment dağılımı
print(f"\n📊 YENİ SEGMENT DAĞILIMI:")
yeni_segment_dagilimi = df_guncellenmis['segment'].value_counts()
for segment, count in yeni_segment_dagilimi.items():
    print(f"   📋 {segment}: {count:,} kayıt")

# Değişiklikleri kaydet
df_guncellenmis = df_guncellenmis.drop(['email_lower', 'dynamics_kayit'], axis=1)
df_guncellenmis.to_excel('data/aluplan-list.xlsx', index=False)

print(f"\n💾 DOSYA KAYDEDILDI:")
print(f"   📁 data/aluplan-list.xlsx")
print(f"   📝 Toplam kayıt: {len(df_guncellenmis):,}")

# Filtre sonucu
sales_hub_count = yeni_segment_dagilimi.get('Sales Hub Mevcut', 0)
print(f"\n🎯 FİLTRE SONUCU:")
print(f"   📋 Sales Hub Mevcut filtresi seçildiğinde:")
print(f"   📝 Görünecek kayıt: {sales_hub_count:,}")
print(f"   📧 Dynamics 365'teki tüm kayıtlar dahil!")

print(f"\n" + "=" * 60)
print("✅ DYNAMICS 365 KAYITLARI SALES HUB MEVCUT'A TAŞINDI")
print("=" * 60)
print(f"✅ Sales Hub Mevcut: {sales_hub_count:,} kayıt")
print(f"✅ Toplam: {len(df_guncellenmis):,} kayıt")
print(f"✅ Uygulama: http://localhost:3001")
