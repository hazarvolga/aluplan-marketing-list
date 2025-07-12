#!/usr/bin/env python3
"""
Spam Kontrol Güvenlik Açıkları Test Scripti
"""

import pandas as pd
import json
import re

def test_spam_security_vulnerabilities():
    """Spam kontrol mekanizmasındaki güvenlik açıklarını test et"""
    
    print("🛡️ SPAM KONTROL GÜVENLİK AÇIKLARI TESİTİ")
    print("=" * 50)
    
    # Test email'leri - Potansiyel güvenlik açıkları
    test_emails = [
        # Bypass attempts
        "test@gmai.com",  # Typo domain - 50 puan
        "test@gmail.com",  # Legitimate - 0 puan
        "test@temp-mail.com",  # Suspicious pattern - 30 puan
        "test@10minutemail.com",  # High-risk - 95 puan
        "test@example.com",  # Legitimate but suspicious - 0 puan (BUG!)
        "test@test.com",  # Legitimate but suspicious - 0 puan (BUG!)
        
        # Format vulnerabilities
        "test@",  # Invalid format - 100 puan
        "@domain.com",  # Invalid format - 100 puan
        "test..test@domain.com",  # Double dot - 0 puan (BUG!)
        "test@domain.",  # Incomplete domain - 0 puan (BUG!)
        "test@domain..com",  # Double dot in domain - 0 puan (BUG!)
        
        # Injection attempts
        "test@domain.com<script>alert('xss')</script>",  # XSS - 0 puan (BUG!)
        "test@domain.com'; DROP TABLE users; --",  # SQL injection - 0 puan (BUG!)
        "test@domain.com\x00null",  # Null byte - 0 puan (BUG!)
        
        # Character encoding
        "test@dömaİn.com",  # Unicode - 0 puan (BUG!)
        "test@domain.com\r\n",  # CRLF - 0 puan (BUG!)
        "test@domain.com\t",  # Tab - 0 puan (BUG!)
        
        # Long domain/email
        "test@" + "a" * 100 + ".com",  # Long domain - 0 puan (BUG!)
        "a" * 100 + "@domain.com",  # Long local part - 25 puan (random pattern)
        
        # Subdomain bypass
        "test@subdomain.10minutemail.com",  # Subdomain bypass - 0 puan (BUG!)
        "test@10minutemail.com.legitimate.com",  # Domain spoofing - 0 puan (BUG!)
        
        # Case sensitivity
        "test@GMAI.COM",  # Case variation - 50 puan (works)
        "test@Gmail.Com",  # Mixed case - 0 puan (works)
        
        # Number patterns
        "123456789@domain.com",  # Many numbers - 20 puan
        "a1b2c3d4e5@domain.com",  # Mixed numbers - 0 puan
        "111111111111@domain.com",  # All numbers - 20 puan
        
        # Short emails
        "a@domain.com",  # Very short - 15 puan
        "ab@domain.com",  # Short - 15 puan
        "abc@domain.com",  # Normal - 0 puan
        
        # IP addresses
        "test@192.168.1.1",  # IP address - 0 puan (BUG!)
        "test@[192.168.1.1]",  # IP address with brackets - 0 puan (BUG!)
        
        # Legitimate but suspicious
        "admin@company.com",  # Legitimate - 0 puan
        "noreply@company.com",  # Legitimate - 0 puan
        "support@company.com",  # Legitimate - 0 puan
        
        # Real problematic patterns
        "randomstring12345@domain.com",  # Random pattern - 25 puan
        "asdasdasd@domain.com",  # Random pattern - 25 puan
        "qwerty123@domain.com",  # Common pattern - 0 puan
    ]
    
    def check_spam_email(email):
        """Python versiyonu spam kontrol - TypeScript'ten çeviri"""
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
    
    # Test email'leri analiz et
    print("\n🔍 GÜVENLİK AÇIKLARI TESİTİ:")
    print("-" * 50)
    
    vulnerabilities = []
    
    for email in test_emails:
        result = check_spam_email(email)
        
        # Güvenlik açıkları tespit et
        vulnerability = None
        
        if 'example.com' in email or 'test.com' in email:
            if result['score'] < 30:
                vulnerability = "Test/example domain'ler spam olarak işaretlenmeli"
        
        if '..' in email and result['score'] < 50:
            vulnerability = "Double dot formatı spam olarak işaretlenmeli"
        
        if email.endswith('.') and result['score'] < 50:
            vulnerability = "Eksik domain formatı spam olarak işaretlenmeli"
        
        if '<script>' in email or 'DROP TABLE' in email or '\x00' in email:
            if result['score'] < 80:
                vulnerability = "Injection attempt spam olarak işaretlenmeli"
        
        if '192.168.' in email or '[' in email:
            if result['score'] < 30:
                vulnerability = "IP address formatı şüpheli olarak işaretlenmeli"
        
        if 'subdomain.10minutemail.com' in email:
            if result['score'] < 80:
                vulnerability = "Subdomain bypass korunmalı"
        
        if len(email.split('@')[0]) > 50 and result['score'] < 40:
            vulnerability = "Çok uzun local part spam olarak işaretlenmeli"
        
        if len(email.split('@')[1]) > 50 and result['score'] < 40:
            vulnerability = "Çok uzun domain spam olarak işaretlenmeli"
        
        # Sonuçları yazdır
        status = "🚨 VULNERABLE" if vulnerability else "✅ SAFE"
        print(f"{status} | {email[:40]:<40} | Score: {result['score']:3d} | {result['reason']}")
        
        if vulnerability:
            vulnerabilities.append({
                'email': email,
                'vulnerability': vulnerability,
                'score': result['score'],
                'reason': result['reason']
            })
    
    # Güvenlik açığı özeti
    print(f"\n🛡️ GÜVENLİK AÇIĞI ÖZETİ:")
    print("-" * 50)
    
    if vulnerabilities:
        print(f"⚠️ {len(vulnerabilities)} güvenlik açığı tespit edildi!")
        
        for i, vuln in enumerate(vulnerabilities, 1):
            print(f"{i}. {vuln['vulnerability']}")
            print(f"   Email: {vuln['email']}")
            print(f"   Score: {vuln['score']} (düşük!)")
            print()
    else:
        print("✅ Güvenlik açığı bulunamadı!")
    
    # Öneriler
    print(f"\n💡 GÜVENLİK İYİLEŞTİRME ÖNERİLERİ:")
    print("-" * 50)
    
    recommendations = [
        "1. Test/example domain'leri spam listesine ekle",
        "2. IP address formatlarını kontrol et",
        "3. Double dot ve eksik domain kontrolü ekle",
        "4. Injection attempt kontrolü ekle",
        "5. Subdomain bypass koruması ekle",
        "6. Çok uzun email kontrolü ekle",
        "7. Unicode karakter kontrolü ekle",
        "8. CRLF/Tab karakteri kontrolü ekle",
        "9. Null byte kontrolü ekle",
        "10. Minimum spam score'u 30'a çıkar"
    ]
    
    for rec in recommendations:
        print(f"  {rec}")
    
    # Sonuçları kaydet
    report = {
        'test_date': pd.Timestamp.now().isoformat(),
        'total_tests': len(test_emails),
        'vulnerabilities_found': len(vulnerabilities),
        'vulnerabilities': vulnerabilities,
        'recommendations': recommendations
    }
    
    with open('spam_security_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Güvenlik raporu kaydedildi: spam_security_report.json")
    print(f"\n{'🚨 SPAM KONTROL MEKANİZMASI GÜVENLİK AÇIKLARI VAR!' if vulnerabilities else '✅ SPAM KONTROL MEKANİZMASI GÜVENLİ!'}")

if __name__ == "__main__":
    test_spam_security_vulnerabilities()
