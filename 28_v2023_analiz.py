import pandas as pd

print('🔍 V2023 SEGMENT ANALİZİ')
print('=' * 50)

# Ana veri dosyasını yükle
df = pd.read_excel('data/aluplan-list.xlsx')

# V2023 kayıtlarını analiz et
print('📊 ANA VERİ DOSYASI ANALİZİ:')
print(f'   📝 Toplam kayıt: {len(df):,}')

# Segment sütununda V2023 geçen kayıtları bul
v2023_segment = df[df['segment'].astype(str).str.contains('V2023', case=False, na=False)]
print(f'   📈 Segment\'te V2023 geçen: {len(v2023_segment):,}')

# V2023_EMAILS listesini yükle
v2023_emails = set()
with open('src/data/v2023-emails.ts', 'r') as f:
    content = f.read()
    # Email adreslerini çıkar
    import re
    emails = re.findall(r'"([^"]+@[^"]+)"', content)
    v2023_emails = set(email.lower().strip() for email in emails)

print(f'   📧 V2023_EMAILS listesi: {len(v2023_emails):,}')

# Ana veri dosyasında V2023_EMAILS listesindeki emailler
df_emails = df['email'].astype(str).str.lower().str.strip()
matching_emails = df[df_emails.isin(v2023_emails)]
print(f'   🎯 V2023_EMAILS ile eşleşen: {len(matching_emails):,}')

# Kesişim analizi
segment_emails = set(v2023_segment['email'].astype(str).str.lower().str.strip())
print(f'   📊 Segment V2023 unique email: {len(segment_emails):,}')

# Kesişim ve birleşim
intersection = segment_emails & v2023_emails
union = segment_emails | v2023_emails
print(f'   🔄 Kesişim (her ikisinde de): {len(intersection):,}')
print(f'   ➕ Birleşim (toplam unique): {len(union):,}')

# Sadece segment'te olanlar
only_segment = segment_emails - v2023_emails
print(f'   📋 Sadece segment\'te: {len(only_segment):,}')

# Sadece V2023_EMAILS'te olanlar
only_emails = v2023_emails - segment_emails
print(f'   📧 Sadece V2023_EMAILS\'te: {len(only_emails):,}')

print('\n📊 TOPLAM HESAPLAMA:')
print(f'   Segment V2023: {len(segment_emails):,}')
print(f'   + V2023_EMAILS: {len(v2023_emails):,}')
print(f'   - Kesişim: {len(intersection):,}')
print(f'   = Toplam: {len(union):,}')

# Segment detayları
print('\n🔍 SEGMENT DETAYLARI:')
segment_types = v2023_segment['segment'].value_counts()
for segment, count in segment_types.items():
    print(f'   📋 {segment}: {count:,}')

# İlk 10 örnek email
print('\n📧 SADECE SEGMENT\'TEKİ İLK 10 EMAIL:')
for email in sorted(only_segment)[:10]:
    print(f'   📧 {email}')

print('\n📧 SADECE V2023_EMAILS\'TEKİ İLK 10 EMAIL:')
for email in sorted(only_emails)[:10]:
    print(f'   📧 {email}')
