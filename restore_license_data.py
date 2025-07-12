#!/usr/bin/env python3
"""
Lisans verilerini email eşleştirmesiyle geri yükleme scripti
- Kaynak: veri_kaynaklari/birlestirilmis-liste.xlsx - "Kalıcı/SUB/SSA" sütunu
- Hedef: data/aluplan-list.xlsx - yeni "license" sütunu eklenecek
- Email eşleştirmesi ile güvenli merge
"""

import pandas as pd
import numpy as np
from datetime import datetime

def restore_license_data():
    print("=== Lisans Verilerini Geri Yükleme İşlemi ===")
    print(f"İşlem zamanı: {datetime.now()}")
    
    # 1. Kaynak dosyayı oku
    print("\n1. Kaynak dosya yükleniyor...")
    source_file = 'veri_kaynaklari/birlestirilmis-liste.xlsx'
    try:
        source_df = pd.read_excel(source_file)
        print(f"✅ Kaynak dosya yüklendi: {len(source_df)} satır")
        
        # Kolonları göster
        print("\nKaynak dosya kolonları:")
        for i, col in enumerate(source_df.columns):
            print(f"  {i}: {col}")
            
    except Exception as e:
        print(f"❌ Kaynak dosya okunamadı: {e}")
        return False
    
    # 2. Hedef dosyayı oku
    print("\n2. Hedef dosya yükleniyor...")
    target_file = 'data/aluplan-list.xlsx'
    try:
        target_df = pd.read_excel(target_file)
        print(f"✅ Hedef dosya yüklendi: {len(target_df)} satır")
        
        # Kolonları göster
        print("\nHedef dosya kolonları:")
        for i, col in enumerate(target_df.columns):
            print(f"  {i}: {col}")
            
    except Exception as e:
        print(f"❌ Hedef dosya okunamadı: {e}")
        return False
    
    # 3. Email ve lisans kolonlarını bul
    print("\n3. Email ve lisans kolonları kontrol ediliyor...")
    
    # Email kolonu bulma
    email_col = None
    for col in source_df.columns:
        if 'email' in str(col).lower() or 'e-mail' in str(col).lower():
            email_col = col
            break
    
    if email_col is None:
        print("❌ Kaynak dosyada email kolonu bulunamadı!")
        return False
    
    # Lisans kolonu bulma
    license_col = None
    for col in source_df.columns:
        if 'kalıcı' in str(col).lower() or 'sub' in str(col).lower() or 'ssa' in str(col).lower():
            license_col = col
            break
    
    if license_col is None:
        print("❌ Kaynak dosyada 'Kalıcı/SUB/SSA' kolonu bulunamadı!")
        print("Mevcut kolonlar:")
        for col in source_df.columns:
            print(f"  - {col}")
        return False
    
    print(f"✅ Email kolonu bulundu: {email_col}")
    print(f"✅ Lisans kolonu bulundu: {license_col}")
    
    # 4. Veri temizleme ve hazırlama
    print("\n4. Veri temizleme yapılıyor...")
    
    # Email adreslerini normalize et
    source_df[email_col] = source_df[email_col].astype(str).str.lower().str.strip()
    target_df['email'] = target_df['email'].astype(str).str.lower().str.strip()
    
    # Boş email'leri filtrele
    source_clean = source_df[
        (source_df[email_col].notna()) & 
        (source_df[email_col] != 'nan') & 
        (source_df[email_col] != '') &
        (source_df[email_col].str.contains('@', na=False))
    ].copy()
    
    print(f"✅ Kaynak dosyada geçerli email: {len(source_clean)}")
    
    # 5. Lisans bilgilerini analiz et
    print("\n5. Lisans bilgileri analiz ediliyor...")
    license_stats = source_clean[license_col].value_counts(dropna=False)
    print("Lisans türleri ve sayıları:")
    for license_type, count in license_stats.head(20).items():
        print(f"  {license_type}: {count}")
    
    if len(license_stats) > 20:
        print(f"  ... ve {len(license_stats) - 20} tane daha")
    
    # 6. Email eşleştirmesi yap
    print("\n6. Email eşleştirmesi yapılıyor...")
    
    # License mapping dictionary oluştur
    license_mapping = {}
    for _, row in source_clean.iterrows():
        email = row[email_col]
        license = row[license_col]
        if pd.notna(license) and str(license).strip() != '':
            license_mapping[email] = str(license).strip()
    
    print(f"✅ {len(license_mapping)} email-lisans eşleştirmesi oluşturuldu")
    
    # 7. Hedef dosyaya lisans bilgilerini ekle
    print("\n7. Lisans bilgileri hedef dosyaya ekleniyor...")
    
    # License kolonu ekle
    target_df['license'] = target_df['email'].map(license_mapping)
    
    # İstatistikler
    total_records = len(target_df)
    with_license = target_df['license'].notna().sum()
    without_license = total_records - with_license
    
    print(f"✅ Toplam kayıt: {total_records}")
    print(f"✅ Lisans bilgisi eklenen: {with_license}")
    print(f"⚠️  Lisans bilgisi olmayan: {without_license}")
    
    # 8. Sonuçları kaydet
    print("\n8. Güncellenmiş dosya kaydediliyor...")
    
    # Backup oluştur
    backup_file = f'data/aluplan-list-backup-{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    target_df_original = pd.read_excel(target_file)
    target_df_original.to_excel(backup_file, index=False)
    print(f"✅ Backup oluşturuldu: {backup_file}")
    
    # Güncellenmiş dosyayı kaydet
    target_df.to_excel(target_file, index=False)
    print(f"✅ Güncellenmiş dosya kaydedildi: {target_file}")
    
    # 9. Doğrulama
    print("\n9. Doğrulama yapılıyor...")
    verification_df = pd.read_excel(target_file)
    
    if 'license' in verification_df.columns:
        license_count = verification_df['license'].notna().sum()
        print(f"✅ Doğrulama başarılı: {license_count} lisans bilgisi mevcut")
        
        # Lisans türleri özeti
        final_license_stats = verification_df['license'].value_counts(dropna=False)
        print("\nEklenen lisans türleri:")
        for license_type, count in final_license_stats.head(10).items():
            print(f"  {license_type}: {count}")
    else:
        print("❌ Doğrulama başarısız: License kolonu bulunamadı!")
        return False
    
    print("\n=== İşlem Tamamlandı ===")
    return True

if __name__ == "__main__":
    success = restore_license_data()
    if success:
        print("🎉 Lisans verileri başarıyla geri yüklendi!")
    else:
        print("💥 İşlem başarısız oldu!")
