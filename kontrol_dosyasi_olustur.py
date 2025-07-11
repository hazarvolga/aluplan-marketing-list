import pandas as pd
import numpy as np
import re
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Spam domain listesi (bizim uygulamadaki gibi)
SPAM_DOMAINS = [
    '10minutemail.com', 'tempmail.org', 'guerrillamail.com', 'mailinator.com',
    'yopmail.com', 'temp-mail.org', 'throwaway.email', 'maildrop.cc',
    'sharklasers.com', 'grr.la', 'guerrillamail.info', 'guerrillamail.net',
    'guerrillamail.org', 'guerrillamail.biz', 'spam4.me', 'mvrht.com',
    'nwldx.com', 'trashmail.com', 'emailondeck.com', 'spamgourmet.com',
    'tempail.com', 'temp-mail.io', 'mohmal.com', 'disposablemail.com',
    'fakemailgenerator.com', 'tempmailer.com', 'dispostable.com',
    'tempinbox.com', 'tempmailaddress.com', 'disposable.email',
    'fake-mail.ml', 'throwaway-mail.com', 'burner-mail.com',
    'temporary-mail.net', 'tempmail.net', 'temporary-email.com',
    'fake-email.net', 'throwaway.ml', 'spam-mail.org', 'trashmail.org',
    'disposable-email.net', 'fake-box.com'
]

def check_spam_email(email):
    """Bizim uygulamadaki spam kontrolü"""
    if not email or '@' not in email:
        return {'isSpam': False, 'score': 0, 'reason': ''}
    
    domain = email.split('@')[1].lower()
    score = 0
    reasons = []
    
    # Bilinen spam domain'leri kontrol et
    if domain in SPAM_DOMAINS:
        score += 90
        reasons.append('Spam domain')
    
    # Şüpheli pattern'leri kontrol et
    if 'temp' in domain or 'disposable' in domain or 'fake' in domain:
        score += 70
        reasons.append('Şüpheli pattern')
    
    # Typo domain'leri kontrol et
    typo_domains = ['gmial.com', 'yahooo.com', 'hotmial.com', 'outlok.com']
    if domain in typo_domains:
        score += 80
        reasons.append('Typo domain')
    
    # Çok sayıda rakam içeren domain'ler
    if len(re.findall(r'\d', domain)) > 3:
        score += 50
        reasons.append('Çok rakam')
    
    return {
        'isSpam': score > 30,
        'score': min(score, 100),
        'reason': ', '.join(reasons) if reasons else ''
    }

def normalize_name(name):
    """İsim normalizasyonu"""
    if pd.isna(name):
        return ''
    name = str(name).strip()
    # Başlıktaki fazla boşlukları temizle
    name = re.sub(r'\s+', ' ', name)
    return name

def normalize_email(email):
    """Email normalizasyonu"""
    if pd.isna(email):
        return ''
    email = str(email).strip().lower()
    # Geçersiz karakterleri temizle
    email = re.sub(r'[^\w@.-]', '', email)
    return email

def normalize_company(company):
    """Şirket adı normalizasyonu"""
    if pd.isna(company):
        return ''
    company = str(company).strip()
    # Şirket adı temizleme
    company = re.sub(r'\s+', ' ', company)
    return company

def normalize_phone(phone):
    """Telefon normalizasyonu"""
    if pd.isna(phone):
        return ''
    phone = str(phone).strip()
    # Sadece rakam ve + karakteri bırak
    phone = re.sub(r'[^\d+\s\-()]', '', phone)
    return phone

def process_excel_file(file_path, source_name):
    """Excel dosyasını işle"""
    print(f"\n🔄 İşleniyor: {source_name}")
    
    try:
        # Excel dosyasını oku
        df = pd.read_excel(file_path)
        print(f"   📊 Ham veri: {len(df)} satır, {len(df.columns)} sütun")
        
        # Sütun isimlerini normalize et
        df.columns = df.columns.str.strip()
        
        # Kayıtları işle
        processed_records = []
        
        for index, row in df.iterrows():
            # Sütun eşlemeleri (her dosya için farklı)
            name = ''
            email = ''
            company = ''
            phone = ''
            
            # Sütun isimlerini kontrol et ve veri çek
            for col in df.columns:
                col_lower = col.lower()
                
                # İsim sütunları
                if any(x in col_lower for x in ['full name', 'name', 'firstname', 'lastname', 'yetkili']):
                    if 'full name' in col_lower or 'name' in col_lower:
                        name = normalize_name(row[col])
                    elif 'firstname' in col_lower:
                        firstname = normalize_name(row[col])
                        if name == '':
                            name = firstname
                    elif 'lastname' in col_lower:
                        lastname = normalize_name(row[col])
                        if name and lastname:
                            name = f"{name} {lastname}"
                
                # Email sütunları
                elif any(x in col_lower for x in ['email', 'e-mail', 'mail']):
                    email = normalize_email(row[col])
                
                # Şirket sütunları
                elif any(x in col_lower for x in ['company', 'şirket', 'firma', 'acount name']):
                    company = normalize_company(row[col])
                
                # Telefon sütunları
                elif any(x in col_lower for x in ['phone', 'tel', 'gsm', 'cep']):
                    phone = normalize_phone(row[col])
            
            # Firstname + Lastname birleştirme (Mautic için)
            if source_name == 'Mautic' and name == '':
                firstname = normalize_name(row.get('firstname', ''))
                lastname = normalize_name(row.get('lastname', ''))
                if firstname or lastname:
                    name = f"{firstname} {lastname}".strip()
            
            # Boş kayıtları atla
            if email == '' and name == '':
                continue
                
            # Spam kontrolü
            spam_check = check_spam_email(email)
            
            # Kayıt oluştur
            record = {
                'name': name,
                'email': email,
                'company': company,
                'phone': phone,
                'segment': source_name,
                'spamScore': spam_check['score'],
                'spamReason': spam_check['reason']
            }
            
            processed_records.append(record)
        
        print(f"   ✅ İşlenen kayıt: {len(processed_records)}")
        return processed_records
        
    except Exception as e:
        print(f"   ❌ Hata: {e}")
        return []

def merge_and_deduplicate(all_records):
    """Kayıtları birleştir ve çakışmaları çözümle"""
    print(f"\n🔄 Birleştirme ve çakışma çözümü başlıyor...")
    
    # Email'e göre gruplama
    email_groups = {}
    
    for record in all_records:
        email = record['email']
        if email == '':
            continue
            
        if email not in email_groups:
            email_groups[email] = []
        email_groups[email].append(record)
    
    # Çakışmaları çözümle
    merged_records = []
    
    for email, records in email_groups.items():
        if len(records) == 1:
            # Tek kayıt, direkt ekle
            merged_records.append(records[0])
        else:
            # Çakışma var, birleştir
            merged_record = {
                'name': '',
                'email': email,
                'company': '',
                'phone': '',
                'segment': '',
                'spamScore': 0,
                'spamReason': ''
            }
            
            # En iyi veriyi seç
            segments = []
            for record in records:
                # En uzun ismi al
                if len(record['name']) > len(merged_record['name']):
                    merged_record['name'] = record['name']
                
                # En uzun şirket adını al
                if len(record['company']) > len(merged_record['company']):
                    merged_record['company'] = record['company']
                
                # En uzun telefonu al
                if len(record['phone']) > len(merged_record['phone']):
                    merged_record['phone'] = record['phone']
                
                # Segment'i ekle
                if record['segment'] not in segments:
                    segments.append(record['segment'])
                
                # En yüksek spam skoru
                if record['spamScore'] > merged_record['spamScore']:
                    merged_record['spamScore'] = record['spamScore']
                    merged_record['spamReason'] = record['spamReason']
            
            # Segment'leri birleştir
            merged_record['segment'] = ', '.join(segments)
            merged_records.append(merged_record)
    
    print(f"   ✅ Birleştirme tamamlandı: {len(merged_records)} benzersiz kayıt")
    return merged_records

def main():
    print("🚀 ALUPLAN MARKETİNG VERİ BİRLEŞTİRME BAŞLIYOR...")
    print("=" * 60)
    
    # Dosya yolları
    veri_klasoru = Path("veri_kaynaklari")
    
    dosya_listesi = [
        ("All Contacts-Dynamics-365.xlsx", "Sales Hub Mevcut"),
        ("Allplan Müşteriler_Final_2025-03-19-R28 - V2022 ve eski.xlsx", "V2022 ve eski"),
        ("Allplan-V2023-ve ustu.xlsx", "V2023 ve üzeri"),
        ("mautic-tum-liste.xlsx", "Mautic"),
        ("DNC.xlsx", "DNC")
    ]
    
    # Tüm kayıtları topla
    all_records = []
    
    for dosya_adi, segment_adi in dosya_listesi:
        dosya_yolu = veri_klasoru / dosya_adi
        if dosya_yolu.exists():
            records = process_excel_file(dosya_yolu, segment_adi)
            all_records.extend(records)
        else:
            print(f"❌ {dosya_adi} bulunamadı")
    
    print(f"\n📊 TOPLAM HAM KAYIT: {len(all_records)}")
    
    # Birleştirme ve çakışma çözümü
    merged_records = merge_and_deduplicate(all_records)
    
    # DataFrame'e dönüştür
    if len(merged_records) > 0:
        df = pd.DataFrame(merged_records)
        
        # Segment kolonlarını oluştur (uygulama formatı)
        df['isMautic'] = df['segment'].str.contains('Mautic', na=False)
        df['isSalesHubMevcut'] = df['segment'].str.contains('Sales Hub Mevcut', na=False)
        df['isV2022'] = df['segment'].str.contains('V2022 ve eski', na=False)
        df['isV2023'] = df['segment'].str.contains('V2023 ve üzeri', na=False)
        df['isDNC'] = df['segment'].str.contains('DNC', na=False)
    else:
        print("❌ Hiç kayıt bulunamadı!")
        return
    
    # İstatistikler
    print(f"\n📈 SONUÇ İSTATİSTİKLERİ:")
    print(f"   📊 Toplam benzersiz kayıt: {len(df)}")
    print(f"   📧 Geçerli email: {df['email'].notna().sum()}")
    print(f"   👤 Geçerli isim: {df['name'].notna().sum()}")
    print(f"   🏢 Geçerli şirket: {df['company'].notna().sum()}")
    print(f"   📞 Geçerli telefon: {df['phone'].notna().sum()}")
    print(f"   🔴 Spam email: {(df['spamScore'] > 30).sum()}")
    print(f"   ⚠️  DNC kayıtları: {df['isDNC'].sum()}")
    
    print(f"\n🎯 SEGMENT DAĞILIMI:")
    print(f"   🟢 Mautic: {df['isMautic'].sum()}")
    print(f"   🟡 Sales Hub Mevcut: {df['isSalesHubMevcut'].sum()}")
    print(f"   🟠 V2022 ve eski: {df['isV2022'].sum()}")
    print(f"   🟣 V2023 ve üzeri: {df['isV2023'].sum()}")
    
    # Kontrol dosyasını kaydet
    output_file = "kontrol_dosyasi.xlsx"
    df.to_excel(output_file, index=False)
    print(f"\n💾 Kontrol dosyası kaydedildi: {output_file}")
    
    # Örnek kayıtları göster
    print(f"\n📋 İLK 5 KAYIT ÖRNEĞİ:")
    for i, row in df.head().iterrows():
        print(f"   {i+1}. {row['name']} - {row['email']} - {row['company']} - Spam: {row['spamScore']}")
    
    print(f"\n🎉 İŞLEM TAMAMLANDI!")
    print("=" * 60)

if __name__ == "__main__":
    main()
