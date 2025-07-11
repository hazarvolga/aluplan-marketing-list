import pandas as pd
import numpy as np
import re

print("🔍 DYNAMICS 365 KONTAK FARK ANALİZİ")
print("=" * 60)

# Dynamics 365 orijinal verilerini yükle
df_dynamics = pd.read_excel('veri_kaynaklari/All Contacts-Dynamics-365.xlsx')
print(f"📊 DYNAMICS 365 ORİJİNAL VERİLER:")
print(f"   📝 Toplam satır sayısı: {len(df_dynamics):,}")
print(f"   📧 Email sütunu: 'Email'")

# Email kontrolü
df_dynamics_email = df_dynamics.copy()
print(f"\n📧 EMAIL ANALİZİ:")

# Boş email'ler
bos_email = df_dynamics_email['Email'].isna().sum()
print(f"   ❌ Boş email: {bos_email:,}")

# Email içermeyen kayıtlar
email_yoksa = df_dynamics_email[df_dynamics_email['Email'].notna()]
gecersiz_email = email_yoksa[~email_yoksa['Email'].astype(str).str.contains('@', na=False)]
print(f"   ❌ '@' işareti olmayan: {len(gecersiz_email):,}")

# Geçerli email formatı kontrolü
def is_valid_email(email):
    if pd.isna(email):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, str(email)))

# Geçersiz email formatları
df_dynamics_email['valid_email'] = df_dynamics_email['Email'].apply(is_valid_email)
gecersiz_format = df_dynamics_email[~df_dynamics_email['valid_email']]
print(f"   ❌ Geçersiz email formatı: {len(gecersiz_format):,}")

# Geçerli email'ler
gecerli_email = df_dynamics_email[df_dynamics_email['valid_email']]
print(f"   ✅ Geçerli email: {len(gecerli_email):,}")

# Tekrar email'ler
email_counts = gecerli_email['Email'].value_counts()
tekrar_emails = email_counts[email_counts > 1]
print(f"   🔄 Tekrar eden email: {len(tekrar_emails):,}")
print(f"   📊 Tekrar eden toplam kayıt: {tekrar_emails.sum():,}")

# Bizim sistemdeki Sales Hub verilerini yükle
df_sistem = pd.read_excel('data/aluplan-list.xlsx')
sales_hub_sistem = df_sistem[df_sistem['segment'] == 'Sales Hub Mevcut']
print(f"\n📊 BİZİM SİSTEMDEKİ SALES HUB:")
print(f"   📝 Toplam kayıt: {len(sales_hub_sistem):,}")

# Fark analizi
print(f"\n🔍 FARK ANALİZİ:")
print(f"   📊 Dynamics 365'te görünen kontak: 1,202")
print(f"   📊 Bizim sistemdeki Sales Hub: {len(sales_hub_sistem):,}")
print(f"   📊 Fark: {1202 - len(sales_hub_sistem):,}")

print(f"\n📋 FARK NEDENLERİ:")
print(f"   ❌ Boş email adresi: {bos_email:,}")
print(f"   ❌ Geçersiz email formatı: {len(gecersiz_format):,}")
print(f"   ❌ '@' işareti olmayan: {len(gecersiz_email):,}")
print(f"   🔄 Tekrar eden email'ler: {tekrar_emails.sum() - len(tekrar_emails):,}")

# Toplam filtrelenen
toplam_filtrelenen = bos_email + len(gecersiz_format) + len(gecersiz_email) + (tekrar_emails.sum() - len(tekrar_emails))
print(f"   📊 Toplam filtrelenen: {toplam_filtrelenen:,}")

# Geçersiz email örnekleri
print(f"\n❌ GEÇERSİZ EMAIL ÖRNEKLERİ:")
if len(gecersiz_format) > 0:
    ornekler = gecersiz_format['Email'].head(10).tolist()
    for i, ornek in enumerate(ornekler, 1):
        print(f"   {i}. {ornek}")

# Tekrar email örnekleri
print(f"\n🔄 TEKRAR EMAIL ÖRNEKLERİ:")
if len(tekrar_emails) > 0:
    for email, count in tekrar_emails.head(5).items():
        print(f"   📧 {email}: {count} kez")

# Özet
print(f"\n💡 ÖZET:")
print(f"   • Dynamics 365'te görünen 1,202 kontak var")
print(f"   • {toplam_filtrelenen:,} kayıt email problemi nedeniyle filtrelendi")
print(f"   • {len(sales_hub_sistem):,} geçerli kontak sisteme alındı")
print(f"   • Veri kalitesi: %{(len(sales_hub_sistem) / 1202 * 100):.1f}")

print(f"\n✅ ANALİZ TAMAMLANDI")
print("=" * 60)
