import pandas as pd
import numpy as np
from datetime import datetime

print("🔍 TÜM DOSYA ANALİZİ VE ÇAKIŞMA ÇÖZÜMÜ")
print("=" * 60)

# Tüm dosyaları tanımla
dosyalar = {
    'dynamics_365': 'veri_kaynaklari/All Contacts-Dynamics-365.xlsx',
    'allplan_v2022': 'veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28 - V2022 ve eski.xlsx',
    'allplan_v2023': 'veri_kaynaklari/Allplan-V2023-ve ustu.xlsx',
    'mevcut_allplan': 'veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28.xlsx'
}

# Mevcut veri setini yükle
df_mevcut = pd.read_excel('data/aluplan-list.xlsx')
print(f"📊 MEVCUT VERİ SETİ:")
print(f"   📝 Toplam kayıt: {len(df_mevcut):,}")
print(f"   📝 Mevcut Müşteriler: {len(df_mevcut[df_mevcut['segment'] == 'Mevcut Müşteriler']):,}")
print(f"   📝 Potansiyel Müşteriler: {len(df_mevcut[df_mevcut['segment'] == 'Potansiyel Müşteriler']):,}")

# Mevcut email listesini al
mevcut_emails = set(df_mevcut['email'].str.lower().str.strip())
print(f"   📧 Mevcut email sayısı: {len(mevcut_emails):,}")

print(f"\n" + "=" * 60)
print("📋 DOSYA ANALİZLERİ")
print("=" * 60)

# Her dosyayı analiz et
dosya_analizleri = {}

for dosya_key, dosya_yolu in dosyalar.items():
    print(f"\n🔍 {dosya_key.upper()} ANALİZİ:")
    print(f"   📁 Dosya: {dosya_yolu}")
    
    try:
        # Dosya yapısını kontrol et
        if 'v2022' in dosya_key or 'v2023' in dosya_key:
            df = pd.read_excel(dosya_yolu, header=1)  # V2022/V2023 dosyaları için header=1
        else:
            df = pd.read_excel(dosya_yolu)  # Dynamics 365 için header=0
        
        print(f"   📝 Toplam kayıt: {len(df):,}")
        print(f"   📋 Sütun sayısı: {len(df.columns)}")
        print(f"   🏷️  Sütun isimleri: {list(df.columns)[:10]}...")  # İlk 10 sütun
        
        # Email sütununu bul
        email_columns = [col for col in df.columns if any(x in col.lower() for x in ['email', 'mail', 'eposta'])]
        name_columns = [col for col in df.columns if any(x in col.lower() for x in ['name', 'ad', 'isim', 'first', 'last'])]
        company_columns = [col for col in df.columns if any(x in col.lower() for x in ['company', 'firma', 'şirket', 'account'])]
        
        print(f"   📧 Email sütunları: {email_columns}")
        print(f"   📝 İsim sütunları: {name_columns}")
        print(f"   🏢 Şirket sütunları: {company_columns}")
        
        # Veri kalitesi analizi
        if email_columns:
            email_col = email_columns[0]
            gecerli_emails = df[email_col].dropna().str.contains('@', na=False).sum()
            toplam_emails = len(df[email_col].dropna())
            print(f"   📧 Geçerli email: {gecerli_emails:,}/{toplam_emails:,}")
            
            # Mevcut sistemle çakışma kontrolü
            if toplam_emails > 0:
                dosya_emails = set(df[email_col].dropna().str.lower().str.strip())
                cakisan_emails = mevcut_emails & dosya_emails
                yeni_emails = dosya_emails - mevcut_emails
                
                print(f"   🔄 Çakışan email: {len(cakisan_emails):,}")
                print(f"   🆕 Yeni email: {len(yeni_emails):,}")
                
                dosya_analizleri[dosya_key] = {
                    'df': df,
                    'email_col': email_col,
                    'name_cols': name_columns,
                    'company_cols': company_columns,
                    'toplam_kayit': len(df),
                    'gecerli_emails': gecerli_emails,
                    'cakisan_emails': cakisan_emails,
                    'yeni_emails': yeni_emails
                }
        
        # İlk 3 kayıt örneği
        print(f"   📋 İlk 3 kayıt:")
        print(df.head(3).to_string(index=False)[:500] + "...")
        
    except Exception as e:
        print(f"   ❌ Hata: {e}")
        dosya_analizleri[dosya_key] = {'hata': str(e)}

print(f"\n" + "=" * 60)
print("🎯 ÇAKIŞMA ANALİZİ ÖZET")
print("=" * 60)

# Çakışma özeti
for dosya_key, analiz in dosya_analizleri.items():
    if 'hata' not in analiz:
        print(f"📋 {dosya_key.upper()}:")
        print(f"   📝 Toplam kayıt: {analiz['toplam_kayit']:,}")
        print(f"   📧 Geçerli email: {analiz['gecerli_emails']:,}")
        print(f"   🔄 Çakışan email: {len(analiz['cakisan_emails']):,}")
        print(f"   🆕 Yeni email: {len(analiz['yeni_emails']):,}")

print(f"\n" + "=" * 60)
print("💡 ÖNERİLEN ÇAKIŞMA ÇÖZÜM STRATEJİSİ")
print("=" * 60)

print(f"🎯 SEGMENT ÖNCELİK SIRASI:")
print(f"   1. Mevcut Müşteriler (Allplan Final) - EN YÜKSEK ÖNCELİK")
print(f"   2. Sales Hub Mevcut (Dynamics 365) - YÜKSEK ÖNCELİK")
print(f"   3. V2023 ve üzeri - ORTA ÖNCELİK")
print(f"   4. V2022 ve eski - ORTA ÖNCELİK")
print(f"   5. Potansiyel Müşteriler (Mautic) - EN DÜŞÜK ÖNCELİK")

print(f"\n🔄 ÇAKIŞMA ÇÖZÜM KURALLARI:")
print(f"   - Aynı email birden fazla segmentte varsa:")
print(f"   - En yüksek öncelikli segment ana segment olur")
print(f"   - Diğer segmentler ikincil etiket olarak eklenir")
print(f"   - İletişim bilgileri en eksiksiz olandan alınır")

print(f"\n❓ ONAY BEKLENİYOR:")
print(f"   Bu çakışma çözüm stratejisine göre devam edelim mi?")
print(f"   Hangi dosyaları önce işleyelim?")
