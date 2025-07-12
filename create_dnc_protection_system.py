#!/usr/bin/env python3
"""
DNC (Do Not Contact) Koruma ve Alarm Sistemi
- DNC kayıtlarını sistemden kaldırır
- DNC listesini güvenlik için saklar
- Tekrar eklenme durumunda alarm verir
"""

import pandas as pd
import json
from datetime import datetime
import os

def create_dnc_protection_system():
    print("🔒 DNC Koruma Sistemi Oluşturuluyor...")
    
    # Ana dosyayı oku
    df = pd.read_excel('public/aluplan-list.xlsx')
    print(f"📁 Toplam kayıt yüklendi: {len(df)}")
    
    # DNC kayıtlarını ayır
    dnc_records = df[df['segment'].str.contains('DNC', case=False, na=False)]
    clean_records = df[~df['segment'].str.contains('DNC', case=False, na=False)]
    
    print(f"⚠️  DNC kayıt sayısı: {len(dnc_records)}")
    print(f"✅ Temiz kayıt sayısı: {len(clean_records)}")
    
    # DNC koruma listesi oluştur
    dnc_protection_list = {
        'created_date': datetime.now().isoformat(),
        'total_dnc_records': len(dnc_records),
        'dnc_emails': dnc_records['email'].str.lower().tolist(),
        'dnc_details': dnc_records[['name', 'email', 'company', 'segment']].to_dict('records')
    }
    
    # Koruma listesini kaydet
    os.makedirs('security', exist_ok=True)
    
    with open('security/dnc-protection-list.json', 'w', encoding='utf-8') as f:
        json.dump(dnc_protection_list, f, ensure_ascii=False, indent=2)
    
    # DNC kayıtlarını ayrı Excel dosyasında da sakla
    dnc_records.to_excel('security/dnc-removed-contacts.xlsx', index=False)
    
    # Temiz veriyi ana dosya olarak kaydet
    clean_records.to_excel('public/aluplan-list-clean.xlsx', index=False)
    
    print(f"""
🔒 DNC Koruma Sistemi Oluşturuldu!

📊 İstatistikler:
- Kaldırılan DNC kayıt: {len(dnc_records)}
- Temiz kalan kayıt: {len(clean_records)}
- Koruma dosyası: security/dnc-protection-list.json
- DNC yedek: security/dnc-removed-contacts.xlsx
- Temiz veri: public/aluplan-list-clean.xlsx

🚨 Güvenlik: DNC emailler artık alarm sistemiyle korunuyor
    """)
    
    return dnc_protection_list, clean_records

def check_dnc_violations(new_data_df):
    """Yeni veri yüklendiğinde DNC ihlallerini kontrol et"""
    
    if not os.path.exists('security/dnc-protection-list.json'):
        return []
    
    with open('security/dnc-protection-list.json', 'r', encoding='utf-8') as f:
        dnc_list = json.load(f)
    
    protected_emails = set(dnc_list['dnc_emails'])
    new_emails = set(new_data_df['email'].str.lower())
    
    violations = protected_emails.intersection(new_emails)
    
    if violations:
        print(f"🚨 DNC İHLALİ TESPİT EDİLDİ! {len(violations)} yasaklı email!")
        for email in violations:
            print(f"   ❌ {email}")
    
    return list(violations)

if __name__ == "__main__":
    dnc_list, clean_data = create_dnc_protection_system()
    
    # Test: DNC ihlal kontrolü
    print("\n🧪 Test: DNC ihlal kontrolü...")
    test_violations = check_dnc_violations(clean_data)
    print(f"Test sonucu: {len(test_violations)} ihlal tespit edildi (0 olmalı)")
