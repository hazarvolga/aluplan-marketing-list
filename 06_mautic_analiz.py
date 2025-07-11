import pandas as pd
import numpy as np

print("🔍 MAUTIC VERİSİ ANALİZİ")
print("=" * 50)

# Mautic dosyasını analiz et
mautic_file = "veri_kaynaklari/mautic-tum-liste.xlsx"
df_mautic = pd.read_excel(mautic_file)

print(f"📊 MAUTIC VERİSİ:")
print(f"   📁 Dosya: {mautic_file}")
print(f"   📝 Toplam kayıt: {len(df_mautic):,}")
print(f"   📋 Sütun sayısı: {len(df_mautic.columns)}")
print(f"   🏷️  Sütun isimleri: {list(df_mautic.columns)}")

# İlk 5 kayıt
print(f"\n📋 İLK 5 KAYIT:")
print(df_mautic.head().to_string(index=False))

# Hangi sütunları kullanabileceğimizi kontrol et
print(f"\n🎯 KULLANILACAK VERİ SÜTUNLARI:")
possible_name_cols = [col for col in df_mautic.columns if any(x in col.lower() for x in ['name', 'ad', 'isim', 'first', 'last', 'fname', 'lname'])]
possible_email_cols = [col for col in df_mautic.columns if any(x in col.lower() for x in ['email', 'mail', 'eposta'])]
possible_company_cols = [col for col in df_mautic.columns if any(x in col.lower() for x in ['company', 'firma', 'şirket', 'kurum'])]

print(f"   📝 İsim sütunları: {possible_name_cols}")
print(f"   📧 Email sütunları: {possible_email_cols}")
print(f"   🏢 Şirket sütunları: {possible_company_cols}")

# Veri kalitesi kontrolü
print(f"\n🔍 VERİ KALİTESİ KONTROLÜ:")
for col in df_mautic.columns:
    null_count = df_mautic[col].isnull().sum()
    total_count = len(df_mautic)
    if null_count > 0:
        print(f"   ❌ {col}: {null_count:,}/{total_count:,} boş kayıt ({null_count/total_count*100:.1f}%)")
    else:
        print(f"   ✅ {col}: Tam dolu")

# Email formatı kontrolü
if possible_email_cols:
    email_col = possible_email_cols[0]
    if email_col in df_mautic.columns:
        valid_emails = df_mautic[email_col].dropna().str.contains('@', na=False).sum()
        total_emails = len(df_mautic[email_col].dropna())
        print(f"   📧 Email formatı: {valid_emails:,}/{total_emails:,} geçerli")

print(f"\n" + "=" * 50)
print("🆚 ALLPLAN VE MAUTIC KARŞILAŞTIRMASI")
print("=" * 50)

# Allplan müşterilerini oku
allplan_file = "veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28.xlsx"
df_allplan = pd.read_excel(allplan_file, header=1)

print(f"📊 ALLPLAN MÜŞTERİLERİ:")
print(f"   📝 Toplam kayıt: {len(df_allplan):,}")
print(f"   📧 Email sütunu: Main E-Mail")

# Allplan'daki email adreslerini al
allplan_emails = set(df_allplan['Main E-Mail'].dropna().str.lower().str.strip())
print(f"   📧 Geçerli email sayısı: {len(allplan_emails):,}")

# Mautic'teki email adreslerini al
if possible_email_cols:
    mautic_email_col = possible_email_cols[0]
    mautic_emails = set(df_mautic[mautic_email_col].dropna().str.lower().str.strip())
    print(f"\n📧 MAUTIC EMAIL SAYILARI:")
    print(f"   📧 Mautic toplam email: {len(mautic_emails):,}")
    
    # Kesişimi bul
    ortak_emails = allplan_emails & mautic_emails
    sadece_mautic = mautic_emails - allplan_emails
    sadece_allplan = allplan_emails - mautic_emails
    
    print(f"\n🔍 EMAIL KARŞILAŞTIRMASI:")
    print(f"   🔄 Ortak email adresleri: {len(ortak_emails):,}")
    print(f"   🆕 Sadece Mautic'te olan: {len(sadece_mautic):,}")
    print(f"   🏢 Sadece Allplan'da olan: {len(sadece_allplan):,}")
    
    print(f"\n🎯 POTANSİYEL MÜŞTERİ ADAYLARI:")
    print(f"   📧 Mautic'te olup Allplan'da olmayan: {len(sadece_mautic):,} kayıt")
    print(f"   📝 Bu kayıtlar 'Potansiyel Müşteriler' olarak eklenecek")

print(f"\n" + "=" * 50)
print("❓ ONAY BEKLENİYOR")
print("=" * 50)
print(f"✅ Mautic'ten {len(sadece_mautic):,} potansiyel müşteri eklensin mi?")
print(f"✅ Segment: 'Potansiyel Müşteriler'")
print(f"✅ Kaynak: mautic-tum-liste.xlsx")
