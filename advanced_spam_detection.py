#!/usr/bin/env python3
"""
Gelişmiş Spam Tespit Sistemi
- Email adreslerindeki kelimeleri spam olarak işaretlemez
- Sadece company adı ve gerçek spam içerikleri kontrol eder
- Eklediğiniz örnekleri de yakalar (bitcoin, yandex form linkleri)
"""

import pandas as pd
import re

def advanced_spam_detection():
    df = pd.read_excel('public/aluplan-list.xlsx')
    
    print('=== GELİŞMİŞ SPAM TESPİT SİSTEMİ ===')
    print(f'Toplam kayıt: {len(df)}')
    
    # Gerçek spam pattern'ları
    spam_patterns = [
        # Bitcoin/Kripto (sadece company/name alanında)
        r'bitcoin|btc(?!\w)|crypto|ethereum|dogecoin|binance|blockchain|nft|token(?!\w)|mining',
        
        # Emlak spam
        r'satılık\s+(villa|daire|ev|arsa)|emlak\s+konut|mortgage|ev\s+kredisi',
        
        # Yandex form linkleri (sizin örnekleriniz)
        r'forms\.yandex\.com',
        
        # Para/kazanç spam
        r'para\s+kazan|hızlı\s+para|kolay\s+para|dollars?\s+(get|operation)|(\d+)\s+dollars?',
        
        # Genel scam
        r'operation\s+\d+|prince\s+of|inheritance|lottery\s+winner|million\s+dollar',
        
        # Adult content
        r'viagra|cialis|escort|adult\s+content',
        
        # Şüpheli characters (Cyrillic karakterler spam'da)
        r'[а-я]{3,}',  # Cyrillic karakterler
        
        # Şüpheli linkler
        r'https?://[^\s]*(?:forms|temp|bit\.ly|tinyurl)',
    ]
    
    spam_records = []
    
    for index, row in df.iterrows():
        # Sadece company ve name alanlarını kontrol et (email adreslerini değil!)
        company = str(row.get('company', '')).lower()
        name = str(row.get('name', '')).lower()
        
        # Email'den sadece suspicious linkleri kontrol et
        email = str(row.get('email', ''))
        
        # Text to check (email adresini pattern matching'den hariç tut)
        text_to_check = f"{name} {company}"
        
        found_patterns = []
        spam_score = 0
        
        for pattern in spam_patterns:
            # Email'de sadece link pattern'larını ara
            if 'forms.yandex.com' in pattern or 'https?://' in pattern:
                if re.search(pattern, email, re.IGNORECASE):
                    found_patterns.append(f"Email'de şüpheli link: {pattern}")
                    spam_score += 10
            
            # Company ve name'de diğer pattern'ları ara
            if re.search(pattern, text_to_check, re.IGNORECASE):
                found_patterns.append(f"İçerik: {pattern}")
                spam_score += 5
        
        # Özel kontroller
        # 1. Bitcoin miktarı içeren metinler
        if re.search(r'\d+\.\d+\s*bitс?о?in', f"{name} {company} {email}", re.IGNORECASE):
            found_patterns.append("Bitcoin miktarı tespit edildi")
            spam_score += 15
            
        # 2. Yandex form linkleri
        if 'forms.yandex.com' in email.lower():
            found_patterns.append("Yandex form linki tespit edildi")
            spam_score += 20
            
        # 3. Company adında şüpheli karakterler
        if re.search(r'[а-я]', company):  # Cyrillic
            found_patterns.append("Cyrillic karakterler")
            spam_score += 10
            
        # 4. Rastgele string company isimleri
        if len(company) <= 6 and re.match(r'^[a-z0-9]+$', company) and company != 'nan':
            found_patterns.append("Rastgele string company adı")
            spam_score += 8
        
        if found_patterns and spam_score >= 5:
            spam_records.append({
                'index': index,
                'name': row.get('name', ''),
                'email': row.get('email', ''),
                'company': row.get('company', ''),
                'segment': row.get('segment', ''),
                'spam_patterns': found_patterns,
                'spam_score': spam_score
            })
    
    # Spam score'a göre sırala
    spam_records.sort(key=lambda x: x['spam_score'], reverse=True)
    
    print(f'🚨 Gerçek spam tespit edilen kayıt: {len(spam_records)}')
    
    if spam_records:
        print('\nTespit edilen spam kayıtlar (spam score\'a göre sıralı):')
        for i, record in enumerate(spam_records[:25]):
            print(f'{i+1}. [{record["spam_score"]} puan] {record["email"]}')
            print(f'   Company: {record["company"]}')
            print(f'   Name: {record["name"]}')
            print(f'   Spam nedenleri: {record["spam_patterns"]}')
            print(f'   Segment: {record["segment"]}')
            print()
    
    # Yüksek risk spam'ları ayır (score >= 15)
    high_risk_spam = [r for r in spam_records if r['spam_score'] >= 15]
    print(f'\\n🔥 Yüksek risk spam (≥15 puan): {len(high_risk_spam)}')
    
    return spam_records

if __name__ == "__main__":
    spam_list = advanced_spam_detection()
