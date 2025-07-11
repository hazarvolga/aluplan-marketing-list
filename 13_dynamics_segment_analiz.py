import pandas as pd
import numpy as np

print("🔍 DYNAMICS 365 KAYITLARININ SEGMENT ANALİZİ")
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
df_dynamics_temiz['email_lower'] = df_dynamics_temiz['Email'].str.lower().str.strip()
dynamics_emails = set(df_dynamics_temiz['email_lower'])

print(f"   📧 Dynamics geçerli email: {len(dynamics_emails):,}")

# Mevcut veri setindeki her kaydın Dynamics'te olup olmadığını kontrol et
df_mevcut['email_lower'] = df_mevcut['email'].str.lower().str.strip()
df_mevcut['dynamics_kayit'] = df_mevcut['email_lower'].isin(dynamics_emails)

print(f"\n🎯 DYNAMICS 365 KAYITLARININ SEGMENT DAĞILIMI:")
print(f"   (Sistemimizde bulunan Dynamics 365 kayıtları)")

# Dynamics'te olan kayıtları segment bazında analiz et
dynamics_sistemdeki = df_mevcut[df_mevcut['dynamics_kayit'] == True]
segment_dagilimi = dynamics_sistemdeki['segment'].value_counts()

toplam_dynamics_sistemde = len(dynamics_sistemdeki)
print(f"\n📊 DYNAMICS 365 KAYITLARININ SEGMENT DAĞILIMI:")
print(f"   📝 Toplam Dynamics kayıt (sistemde): {toplam_dynamics_sistemde:,}")
print()

for segment, count in segment_dagilimi.items():
    oran = (count / toplam_dynamics_sistemde) * 100
    print(f"   📋 {segment}: {count:,} kayıt ({oran:.1f}%)")

print(f"\n🔍 DETAYLI ANALİZ:")
print(f"   📧 Dynamics'te toplam geçerli email: {len(dynamics_emails):,}")
print(f"   📧 Sistemde bulunan Dynamics email: {toplam_dynamics_sistemde:,}")
print(f"   ❌ Sistemde olmayan Dynamics email: {len(dynamics_emails) - toplam_dynamics_sistemde:,}")

# Sistemde olmayan Dynamics kayıtları
sistemde_olmayan = dynamics_emails - set(df_mevcut['email_lower'])
if sistemde_olmayan:
    print(f"\n⚠️ SİSTEMDE OLMAYAN DYNAMICS KAYITLARI:")
    print(f"   📧 Eksik kayıt sayısı: {len(sistemde_olmayan):,}")
    print(f"   📧 İlk 5 örnek:")
    for i, email in enumerate(list(sistemde_olmayan)[:5]):
        print(f"      {i+1}. {email}")

print(f"\n🎯 ÖZEL FİLTRE BİLGİSİ:")
print(f"   📋 Sales Hub Mevcut: {segment_dagilimi.get('Sales Hub Mevcut', 0):,} kayıt")
print(f"   📋 Mevcut Müşteriler: {segment_dagilimi.get('Mevcut Müşteriler', 0):,} kayıt")
print(f"   📋 Potansiyel Müşteriler: {segment_dagilimi.get('Potansiyel Müşteriler', 0):,} kayıt")
print(f"   📋 Toplam Dynamics kayıt: {toplam_dynamics_sistemde:,} kayıt")

# UI'da gösterilecek filtre önerisi
print(f"\n💡 UI FİLTRE ÖNERİSİ:")
print(f"   🎯 'Dynamics 365 Kayıtları' isimli özel filtre eklenebilir")
print(f"   📊 Bu filtre {toplam_dynamics_sistemde:,} kayıt gösterecek")
print(f"   📋 İçeriği: Tüm segmentlerden Dynamics 365'te olan kayıtlar")

print(f"\n" + "=" * 60)
print("🔍 DYNAMICS 365 SEGMENT ANALİZİ TAMAMLANDI")
print("=" * 60)
