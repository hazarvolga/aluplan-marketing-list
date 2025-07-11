import pandas as pd
import numpy as np
from datetime import datetime

print("✅ ACTIVE ACCOUNT PRODUCTS ANALİZİ")
print("=" * 60)

# Dosyayı yükle
file_path = 'veri_kaynaklari/Active Account Products 11_07_2025 21-28-06.xlsx'
try:
    df = pd.read_excel(file_path)
    print(f"📊 DOSYA YÜKLENDİ:")
    print(f"   📁 {file_path}")
    print(f"   📝 Toplam kayıt: {len(df):,}")
    print(f"   📄 Toplam sütun: {len(df.columns)}")
    
    print(f"\n🗂️ SÜTUN BİLGİLERİ:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    print(f"\n📋 İLK 5 KAYIT ÖRNEĞİ:")
    print(df.head().to_string(index=False))
    
    # Email sütunu ara
    email_columns = [col for col in df.columns if 'email' in col.lower() or 'e-mail' in col.lower() or 'mail' in col.lower()]
    if email_columns:
        print(f"\n📧 EMAIL SÜTUNLARI:")
        for col in email_columns:
            non_null_count = df[col].notna().sum()
            print(f"   📧 {col}: {non_null_count:,} dolu kayıt")
    
    # İsim sütunları ara
    name_columns = [col for col in df.columns if 'name' in col.lower() or 'isim' in col.lower() or 'ad' in col.lower()]
    if name_columns:
        print(f"\n👤 İSİM SÜTUNLARI:")
        for col in name_columns:
            non_null_count = df[col].notna().sum()
            print(f"   👤 {col}: {non_null_count:,} dolu kayıt")
    
    # Company/Account sütunları ara
    company_columns = [col for col in df.columns if 'company' in col.lower() or 'account' in col.lower() or 'şirket' in col.lower()]
    if company_columns:
        print(f"\n🏢 ŞİRKET/HESAP SÜTUNLARI:")
        for col in company_columns:
            non_null_count = df[col].notna().sum()
            print(f"   🏢 {col}: {non_null_count:,} dolu kayıt")
    
    # Telefon sütunları ara
    phone_columns = [col for col in df.columns if 'phone' in col.lower() or 'telefon' in col.lower() or 'tel' in col.lower()]
    if phone_columns:
        print(f"\n📞 TELEFON SÜTUNLARI:")
        for col in phone_columns:
            non_null_count = df[col].notna().sum()
            print(f"   📞 {col}: {non_null_count:,} dolu kayıt")
    
    # Veri kalite analizi
    print(f"\n📊 VERİ KALİTE ANALİZİ:")
    total_rows = len(df)
    total_cols = len(df.columns)
    total_cells = total_rows * total_cols
    null_cells = df.isnull().sum().sum()
    filled_cells = total_cells - null_cells
    
    print(f"   📝 Toplam hücre: {total_cells:,}")
    print(f"   ✅ Dolu hücre: {filled_cells:,} ({filled_cells/total_cells*100:.1f}%)")
    print(f"   ❌ Boş hücre: {null_cells:,} ({null_cells/total_cells*100:.1f}%)")
    
    # Sütun başına null analizi
    print(f"\n📋 SÜTUN BAŞINA BOŞ DEĞER ANALİZİ:")
    null_analysis = df.isnull().sum().sort_values(ascending=False)
    for col, null_count in null_analysis.items():
        filled_count = len(df) - null_count
        fill_rate = filled_count / len(df) * 100
        print(f"   📊 {col}: {filled_count:,} dolu ({fill_rate:.1f}%), {null_count:,} boş")
    
    # Benzersiz değer analizi
    print(f"\n🔍 BENZERSİZ DEĞER ANALİZİ:")
    for col in df.columns:
        unique_count = df[col].nunique()
        total_count = df[col].notna().sum()
        if total_count > 0:
            uniqueness_rate = unique_count / total_count * 100
            print(f"   📊 {col}: {unique_count:,} benzersiz ({uniqueness_rate:.1f}%)")
    
    # Mevcut sistem ile karşılaştırma hazırlığı
    print(f"\n🔄 MEVCUT SİSTEM İLE KARŞILAŞTIRMA HAZIRLIĞI:")
    
    # Mevcut veri setini yükle
    df_mevcut = pd.read_excel('data/aluplan-list.xlsx')
    mevcut_emails = set(df_mevcut['email'].str.lower().str.strip())
    print(f"   📧 Mevcut sistemde {len(mevcut_emails):,} email")
    
    # Email eşleşmesi kontrolü
    if email_columns:
        for email_col in email_columns:
            if df[email_col].notna().sum() > 0:
                df_temp = df[df[email_col].notna()].copy()
                df_temp['email_lower'] = df_temp[email_col].str.lower().str.strip()
                new_emails = set(df_temp['email_lower']) - mevcut_emails
                existing_emails = set(df_temp['email_lower']) & mevcut_emails
                
                print(f"   📧 {email_col} sütunu:")
                print(f"      🆕 Yeni email: {len(new_emails):,}")
                print(f"      🔄 Mevcut email: {len(existing_emails):,}")
                print(f"      📊 Toplam geçerli email: {len(df_temp):,}")
    
    print(f"\n" + "=" * 60)
    print("✅ ACTIVE ACCOUNT PRODUCTS ANALİZİ TAMAMLANDI")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ HATA: {str(e)}")
    print(f"   Dosya yolu: {file_path}")
    print(f"   Lütfen dosya yolunu ve formatını kontrol edin.")
