import pandas as pd
import os
from pathlib import Path

# Veri kaynakları klasörü
veri_klasoru = "veri_kaynaklari"

# Dosya listesi
dosyalar = [
    "All Contacts-Dynamics-365.xlsx",
    "Allplan Müşteriler_Final_2025-03-19-R28 - V2022 ve eski.xlsx", 
    "Allplan Müşteriler_Final_2025-03-19-R28.xlsx",
    "Allplan-V2023-ve ustu.xlsx",
    "DNC.xlsx",
    "mautic-tum-liste.xlsx"
]

print("=== EXCEL DOSYALARI ANALİZİ ===\n")

for dosya in dosyalar:
    dosya_yolu = os.path.join(veri_klasoru, dosya)
    if os.path.exists(dosya_yolu):
        print(f"📄 {dosya}")
        try:
            # Excel dosyasını oku
            df = pd.read_excel(dosya_yolu)
            
            print(f"   📊 Satır sayısı: {len(df)}")
            print(f"   📋 Sütun sayısı: {len(df.columns)}")
            print(f"   🏷️  Sütun isimleri: {list(df.columns)}")
            
            # Email sütunu kontrol et
            email_sutunlari = [col for col in df.columns if 'email' in col.lower() or 'e-mail' in col.lower() or 'mail' in col.lower()]
            if email_sutunlari:
                print(f"   📧 Email sütunları: {email_sutunlari}")
                # İlk email sütunundaki boş olmayan kayıtlar
                email_col = email_sutunlari[0]
                email_count = df[email_col].notna().sum()
                print(f"   ✅ Geçerli email sayısı: {email_count}")
            
            # İsim sütunu kontrol et
            isim_sutunlari = [col for col in df.columns if 'name' in col.lower() or 'isim' in col.lower() or 'ad' in col.lower()]
            if isim_sutunlari:
                print(f"   👤 İsim sütunları: {isim_sutunlari}")
            
            # Şirket sütunu kontrol et
            sirket_sutunlari = [col for col in df.columns if 'company' in col.lower() or 'şirket' in col.lower() or 'firma' in col.lower()]
            if sirket_sutunlari:
                print(f"   🏢 Şirket sütunları: {sirket_sutunlari}")
            
            # Telefon sütunu kontrol et
            telefon_sutunlari = [col for col in df.columns if 'phone' in col.lower() or 'tel' in col.lower() or 'gsm' in col.lower()]
            if telefon_sutunlari:
                print(f"   📞 Telefon sütunları: {telefon_sutunlari}")
            
            # İlk 3 satırı göster
            print(f"   📋 İlk 3 satır örneği:")
            print(df.head(3).to_string(index=False))
            
        except Exception as e:
            print(f"   ❌ Hata: {e}")
        
        print("-" * 80)
    else:
        print(f"❌ {dosya} bulunamadı")
        print("-" * 80)
