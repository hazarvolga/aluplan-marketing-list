#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
from datetime import datetime

print('=== VERİ KAYNAKLARI ANALİZİ ===\n')

dosyalar = [
    'All Contacts-Dynamics-365.xlsx',
    'Allplan Müşteriler_Final_2025-03-19-R28 - V2022 ve eski.xlsx', 
    'Allplan Müşteriler_Final_2025-03-19-R28.xlsx',
    'Allplan-V2023-ve ustu.xlsx',
    'DNC.xlsx',
    'mautic-tum-liste.xlsx'
]

toplam_kayit = 0
dosya_detaylari = []
tum_veriler = []

for dosya in dosyalar:
    try:
        if os.path.exists(dosya):
            print(f'📋 {dosya}')
            df = pd.read_excel(dosya)
            satir_sayisi = len(df)
            kolon_sayisi = len(df.columns)
            toplam_kayit += satir_sayisi
            
            print(f'   Satır: {satir_sayisi:,}')
            print(f'   Kolon: {kolon_sayisi}')
            print(f'   Kolonlar: {list(df.columns)}')
            
            # Email analizi
            email_kolonlari = [col for col in df.columns if 'email' in col.lower() or 'mail' in col.lower()]
            if email_kolonlari:
                email_col = email_kolonlari[0]
                email_sayisi = df[email_col].notna().sum()
                bos_email = df[email_col].isna().sum()
                print(f'   📧 Email: {email_sayisi:,} dolu, {bos_email:,} boş')
            
            # İsim analizi
            isim_kolonlari = [col for col in df.columns if any(x in col.lower() for x in ['name', 'isim', 'ad', 'first', 'last'])]
            if isim_kolonlari:
                print(f'   👤 İsim kolonları: {isim_kolonlari}')
            
            # Şirket analizi
            sirket_kolonlari = [col for col in df.columns if any(x in col.lower() for x in ['company', 'şirket', 'firma', 'organization'])]
            if sirket_kolonlari:
                print(f'   🏢 Şirket kolonları: {sirket_kolonlari}')
            
            # Segment analizi
            segment_kolonlari = [col for col in df.columns if 'segment' in col.lower()]
            if segment_kolonlari:
                print(f'   🎯 Segment kolonları: {segment_kolonlari}')
            
            print()
            
            dosya_detaylari.append({
                'dosya': dosya,
                'satir': satir_sayisi,
                'kolon': kolon_sayisi,
                'kolonlar': list(df.columns),
                'df': df
            })
            
    except Exception as e:
        print(f'❌ {dosya}: Hata - {str(e)}')

print(f'📊 TOPLAM KAYIT: {toplam_kayit:,}')
print(f'📁 DOSYA SAYISI: {len([d for d in dosya_detaylari if d["satir"] > 0])}')

# Detaylı analiz
print('\n=== DETAYLI ANALİZ ===')
for detay in dosya_detaylari:
    print(f'\n📁 {detay["dosya"]}:')
    df = detay['df']
    
    # İlk 3 satırı göster
    print('   İlk 3 satır:')
    print(df.head(3).to_string(index=False))
    print()
