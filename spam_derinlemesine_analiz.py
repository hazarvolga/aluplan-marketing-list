#!/usr/bin/env python3
"""
Spam Kontrol Mekanizması Derinlemesine Analiz
Bu script spam detection sistemini test eder
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import re

def analyze_spam_detection():
    """Spam detection mekanizmasını analiz et"""
    print("🔍 SPAM KONTROL MEKANİZMASI DERİNLEMESİNE ANALİZ")
    print("=" * 60)
    
    # Production dosyasını oku
    df = pd.read_excel('public/aluplan-list.xlsx')
    
    print(f"📊 Toplam kayıt: {len(df)}")
    
    # Email listesini al
    emails = df['email'].dropna().tolist()
    
    # Spam kontrol algoritması (TypeScript'ten Python'a çeviri)
    def check_spam_email(email):
        """Python versiyonu spam kontrol"""
        email_lower = email.lower()
        domain_parts = email_lower.split('@')
        
        if len(domain_parts) != 2:
            return {'isSpam': True, 'reason': 'Geçersiz email formatı', 'score': 100}
        
        domain = domain_parts[1]
        local_part = domain_parts[0]
        
        score = 0
        reasons = []
        
        # High-risk spam domains (90-100 puan)
        high_risk_domains = [
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com', 'mailinator.com',
            'yopmail.com', 'temp-mail.org', 'dispostable.com', 'throwaway.email'
        ]
        
        if domain in high_risk_domains:
            score = 95
            reasons.append('Geçici email servisi')
        
        # Medium-risk domains (60-80 puan)
        medium_risk_domains = [
            'getnada.com', 'maildrop.cc', 'sharklasers.com', 'grr.la'
        ]
        
        if domain in medium_risk_domains:
            score = 70
            reasons.append('Şüpheli email servisi')
        
        # Common typo domains (40-60 puan)
        typo_domains = [
            'gmial.com', 'gmai.com', 'yahooo.com', 'hotmial.com',
            'outlok.com', 'gmailcom', 'yahoo.co', 'hotmail.co'
        ]
        
        if domain in typo_domains:
            score = 50
            reasons.append('Typo domain')
        
        # Suspicious patterns (10-30 puan)
        if 'temp' in domain or 'disposable' in domain or 'fake' in domain:
            score = max(score, 30)
            reasons.append('Şüpheli domain')
        
        # Too many numbers in local part (10-20 puan)
        number_count = len(re.findall(r'\d', local_part))
        if number_count > len(local_part) * 0.7:
            score = max(score, 20)
            reasons.append('Şüpheli karakter')
        
        # Very short local part (5-15 puan)
        if len(local_part) < 3:
            score = max(score, 15)
            reasons.append('Kısa email')
        
        # Random character patterns (5-25 puan)
        if re.match(r'^[a-z0-9]{10,}$', local_part) and len(local_part) > 8:
            score = max(score, 25)
            reasons.append('Rastgele karakter')
        
        reason = ', '.join(reasons) if reasons else 'Geçerli email'
        is_spam = score >= 40  # 40 puan üzeri spam
        
        return {
            'isSpam': is_spam,
            'reason': reason,
            'score': score,
            'email': email
        }
    
    # Tüm email'leri analiz et
    spam_results = []
    for email in emails:
        result = check_spam_email(email)
        spam_results.append(result)
    
    # Spam istatistikleri
    spam_emails = [r for r in spam_results if r['isSpam']]
    clean_emails = [r for r in spam_results if not r['isSpam']]
    
    print(f"\n📊 SPAM ANALİZ SONUÇLARI:")
    print(f"  Toplam email: {len(emails)}")
    print(f"  Spam email: {len(spam_emails)}")
    print(f"  Temiz email: {len(clean_emails)}")
    print(f"  Spam oranı: {len(spam_emails) / len(emails) * 100:.2f}%")
    
    # Spam sebepleri dağılımı
    print(f"\n🚨 SPAM SEBEPLERİ:")
    spam_reasons = {}
    for spam in spam_emails:
        reason = spam['reason']
        spam_reasons[reason] = spam_reasons.get(reason, 0) + 1
    
    for reason, count in sorted(spam_reasons.items(), key=lambda x: x[1], reverse=True):
        print(f"  {reason}: {count} email")
    
    # Spam score dağılımı
    print(f"\n📈 SPAM SCORE DAĞILIMI:")
    score_ranges = {
        '0-10': 0,
        '11-20': 0,
        '21-30': 0,
        '31-40': 0,
        '41-50': 0,
        '51-60': 0,
        '61-70': 0,
        '71-80': 0,
        '81-90': 0,
        '91-100': 0
    }
    
    for result in spam_results:
        score = result['score']
        if score <= 10:
            score_ranges['0-10'] += 1
        elif score <= 20:
            score_ranges['11-20'] += 1
        elif score <= 30:
            score_ranges['21-30'] += 1
        elif score <= 40:
            score_ranges['31-40'] += 1
        elif score <= 50:
            score_ranges['41-50'] += 1
        elif score <= 60:
            score_ranges['51-60'] += 1
        elif score <= 70:
            score_ranges['61-70'] += 1
        elif score <= 80:
            score_ranges['71-80'] += 1
        elif score <= 90:
            score_ranges['81-90'] += 1
        else:
            score_ranges['91-100'] += 1
    
    for range_name, count in score_ranges.items():
        if count > 0:
            print(f"  {range_name}: {count} email")
    
    # En yüksek spam skorlu email'ler
    print(f"\n🎯 EN YÜKSEK SPAM SKORLU EMAIL'LER:")
    high_spam = sorted(spam_emails, key=lambda x: x['score'], reverse=True)[:10]
    for spam in high_spam:
        print(f"  {spam['email']} (Score: {spam['score']}) - {spam['reason']}")
    
    # Domain analizi
    print(f"\n🌐 DOMAIN ANALİZİ:")
    domains = {}
    for email in emails:
        domain = email.split('@')[1] if '@' in email else 'geçersiz'
        domains[domain] = domains.get(domain, 0) + 1
    
    # En çok kullanılan domain'ler
    top_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:15]
    print(f"  En çok kullanılan domain'ler:")
    for domain, count in top_domains:
        print(f"    {domain}: {count} email")
    
    # Şüpheli domain'leri kontrol et
    print(f"\n🔍 ŞÜPHELİ DOMAIN KONTROLÜ:")
    suspicious_domains = []
    for domain, count in domains.items():
        if ('temp' in domain or 'fake' in domain or 'disposable' in domain or 
            'mail' in domain and len(domain) > 15):
            suspicious_domains.append((domain, count))
    
    if suspicious_domains:
        for domain, count in suspicious_domains:
            print(f"  ⚠️ {domain}: {count} email")
    else:
        print("  ✅ Şüpheli domain bulunamadı")
    
    # Email format kontrolü
    print(f"\n📧 EMAIL FORMAT KONTROLÜ:")
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    invalid_emails = []
    for email in emails:
        if not email_pattern.match(email):
            invalid_emails.append(email)
    
    print(f"  Geçerli email formatı: {len(emails) - len(invalid_emails)}")
    print(f"  Geçersiz email formatı: {len(invalid_emails)}")
    
    if invalid_emails:
        print(f"  Geçersiz email'ler:")
        for email in invalid_emails[:10]:  # İlk 10 tanesi
            print(f"    {email}")
    
    # Duplicate email kontrolü
    print(f"\n🔄 DUPLICATE EMAIL KONTROLÜ:")
    unique_emails = set(emails)
    duplicate_count = len(emails) - len(unique_emails)
    
    print(f"  Toplam email: {len(emails)}")
    print(f"  Unique email: {len(unique_emails)}")
    print(f"  Duplicate email: {duplicate_count}")
    
    if duplicate_count > 0:
        # Duplicate email'leri bul
        email_counts = {}
        for email in emails:
            email_counts[email] = email_counts.get(email, 0) + 1
        
        duplicates = {email: count for email, count in email_counts.items() if count > 1}
        print(f"  Duplicate email listesi:")
        for email, count in sorted(duplicates.items(), key=lambda x: x[1], reverse=True):
            print(f"    {email}: {count} kez")
    
    # Güvenlik önerileri
    print(f"\n🛡️ GÜVENLİK ÖNERİLERİ:")
    
    spam_ratio = len(spam_emails) / len(emails) * 100
    if spam_ratio > 5:
        print(f"  ⚠️ Spam oranı yüksek ({spam_ratio:.1f}%) - Ek filtreleme gerekli")
    elif spam_ratio > 1:
        print(f"  ⚠️ Spam oranı orta ({spam_ratio:.1f}%) - Dikkat")
    else:
        print(f"  ✅ Spam oranı düşük ({spam_ratio:.1f}%) - İyi")
    
    if duplicate_count > 0:
        print(f"  ⚠️ {duplicate_count} duplicate email temizlenmeli")
    else:
        print(f"  ✅ Duplicate email yok")
    
    if invalid_emails:
        print(f"  ⚠️ {len(invalid_emails)} geçersiz email formatı düzeltilmeli")
    else:
        print(f"  ✅ Tüm email formatları geçerli")
    
    # Sonuçları kaydet
    output_data = {
        'analysis_date': datetime.now().isoformat(),
        'total_emails': len(emails),
        'spam_count': len(spam_emails),
        'clean_count': len(clean_emails),
        'spam_percentage': spam_ratio,
        'duplicate_count': duplicate_count,
        'invalid_count': len(invalid_emails),
        'spam_reasons': spam_reasons,
        'top_domains': dict(top_domains),
        'suspicious_domains': dict(suspicious_domains),
        'spam_emails': [s['email'] for s in spam_emails],
        'invalid_emails': invalid_emails
    }
    
    with open('spam_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detaylı rapor kaydedildi: spam_analysis_report.json")
    print(f"\n✅ Spam kontrol mekanizması analizi tamamlandı!")

if __name__ == "__main__":
    analyze_spam_detection()
