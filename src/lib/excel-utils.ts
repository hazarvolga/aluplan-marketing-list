import * as XLSX from 'xlsx';

export interface MarketingData {
  name: string;
  email: string;
  company: string;
  phone: string;
  segment: string;
  license: string;
  processingStatus: 'Sales Hub İşlenmiş' | 'Sales Hub İşlenmemiş' | 'Potansiyel' | 'Diğer';
  isMevcutMusteriler: boolean;
  isPotansiyelMusteriler: boolean;
  isSalesHubMevcut: boolean;
  spamScore: number;
  spamReason: string;
}

export interface FilterOptions {
  segments: {
    mevcutMusteriler: boolean;
    potansiyelMusteriler: boolean;
    salesHubMevcut: boolean;
  };
  searchTerm: string;
  licenses: string[]; // Seçili lisans türleri
}

export function processExcelData(buffer: ArrayBuffer): MarketingData[] {
  const workbook = XLSX.read(buffer, { type: 'array' });
  const sheetName = workbook.SheetNames[0];
  const worksheet = workbook.Sheets[sheetName];
  const rawData = XLSX.utils.sheet_to_json(worksheet);

  return rawData.map((row: any) => { // eslint-disable-line @typescript-eslint/no-explicit-any
    const segment = String(row.segment || '').toLowerCase();
    const email = String(row.email || '');
    const spamCheck = checkSpamEmail(email);
    
    // İşlenme durumunu belirle
    let processingStatus: 'Sales Hub İşlenmiş' | 'Sales Hub İşlenmemiş' | 'Potansiyel' | 'Diğer';
    const segmentLower = segment.toLowerCase();
    if (segmentLower.includes('sales hub mevcut')) {
      processingStatus = 'Sales Hub İşlenmiş';
    } else if (segmentLower.includes('mevcut müşteriler')) {
      processingStatus = 'Sales Hub İşlenmemiş';
    } else if (segmentLower.includes('potansiyel müşteriler') || segmentLower.includes('mautic')) {
      processingStatus = 'Potansiyel';
    } else {
      processingStatus = 'Diğer';
    }
    
    return {
      name: String(row.name || ''),
      email: email,
      company: String(row.company || ''),
      phone: String(row.phone || ''),
      segment: String(row.segment || ''),
      license: String(row.license || ''),
      processingStatus: processingStatus,
      isMevcutMusteriler: segmentLower.includes('mevcut müşteriler') || segmentLower === 'mevcut müşteriler' || segmentLower.includes('sales hub mevcut'),
      isPotansiyelMusteriler: segmentLower.includes('mautic') || segmentLower === 'mautic' || segmentLower.includes('potansiyel müşteriler'),
      isSalesHubMevcut: segmentLower.includes('sales hub'),
      spamScore: spamCheck.score,
      spamReason: spamCheck.reason,
    };
  });
}

export function filterData(data: MarketingData[], filters: FilterOptions): MarketingData[] {
  return data.filter(item => {
    // Search filter
    if (filters.searchTerm) {
      const searchLower = filters.searchTerm.toLowerCase();
      const matchesSearch = 
        item.name.toLowerCase().includes(searchLower) ||
        item.email.toLowerCase().includes(searchLower) ||
        item.company.toLowerCase().includes(searchLower);
      
      if (!matchesSearch) return false;
    }

    // Segment filters
    const { segments } = filters;
    const hasActiveFilters = Object.values(segments).some(Boolean);
    
    if (!hasActiveFilters) return true;

    const segmentMatch = (
      (segments.mevcutMusteriler && item.isMevcutMusteriler) ||
      (segments.potansiyelMusteriler && item.isPotansiyelMusteriler) ||
      (segments.salesHubMevcut && item.isSalesHubMevcut)
    );

    // License filter
    if (filters.licenses && filters.licenses.length > 0) {
      const licenseMatch = item.license && filters.licenses.includes(item.license);
      return segmentMatch && licenseMatch;
    }

    return segmentMatch;
  });
}

export function getSegmentCounts(data: MarketingData[]) {
  return {
    total: data.length,
    mevcutMusteriler: data.filter(item => item.isMevcutMusteriler).length,
    potansiyelMusteriler: data.filter(item => item.isPotansiyelMusteriler).length,
    salesHubMevcut: data.filter(item => item.isSalesHubMevcut).length,
  };
}

export function getUniqueLicenses(data: MarketingData[]): string[] {
  const licenses = data
    .map(item => item.license)
    .filter(license => license && license.trim() !== '')
    .filter((license, index, array) => array.indexOf(license) === index)
    .sort();
  return licenses;
}

export function exportToCSV(data: MarketingData[]): string {
  const headers = ['Name', 'Email', 'Company', 'Phone', 'Segment', 'Processing Status'];
  const rows = data.map(item => [
    item.name,
    item.email,
    item.company,
    item.phone,
    item.segment,
    item.processingStatus
  ]);
  
  const csvContent = [headers, ...rows]
    .map(row => row.map(cell => `"${cell}"`).join(','))
    .join('\n');
  
  return csvContent;
}

export interface DataQualityStats {
  totalRecords: number;
  duplicateEmails: number;
  invalidEmails: number;
  emptyNames: number;
  emptyCompanies: number;
  validRecords: number;
  spamEmails: number;
}

export function getDataQualityStats(data: MarketingData[]): DataQualityStats {
  // Email duplicate count - count records where email appears more than once
  const emailCounts = data.reduce((acc, item) => {
    if (item.email) {
      acc[item.email] = (acc[item.email] || 0) + 1;
    }
    return acc;
  }, {} as Record<string, number>);
  
  // Email format validation - use same regex as frontend
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
  // Categorize each record (mutually exclusive with priority order)
  let duplicateEmails = 0;
  let invalidEmails = 0;
  let emptyNames = 0;
  let spamEmails = 0;
  let validRecords = 0;
  
  data.forEach(item => {
    const emailCount = emailCounts[item.email] || 0;
    const isDuplicate = emailCount > 1;
    const isInvalidEmail = !item.email || !emailRegex.test(item.email);
    const isEmptyName = !item.name || item.name.trim() === '';
    const spamResult = checkSpamEmail(item.email);
    const isSpam = spamResult.isSpam;
    
    // Priority order: duplicate > invalid > empty name > spam > valid
    if (isDuplicate) {
      duplicateEmails++;
    } else if (isInvalidEmail) {
      invalidEmails++;
    } else if (isEmptyName) {
      emptyNames++;
    } else if (isSpam) {
      spamEmails++;
    } else {
      validRecords++;
    }
  });
  
  // Empty companies (separate metric, not mutually exclusive)
  const emptyCompanies = data.filter(item => !item.company || item.company.trim() === '').length;
  
  return {
    totalRecords: data.length,
    duplicateEmails,
    invalidEmails,
    emptyNames,
    emptyCompanies,
    validRecords,
    spamEmails,
  };
}

// Common spam/disposable email domains
/* const SPAM_DOMAINS = [
  // Disposable email services
  '10minutemail.com', 'tempmail.org', 'guerrillamail.com', 'mailinator.com',
  'yopmail.com', 'temp-mail.org', 'dispostable.com', 'throwaway.email',
  'getnada.com', 'maildrop.cc', 'sharklasers.com', 'grr.la',
  // Known spam domains
  'example.com', 'test.com', 'sample.com', 'demo.com',
  // Common typos
  'gmial.com', 'gmai.com', 'yahooo.com', 'hotmial.com',
  'outlok.com', 'gmailcom', 'yahoo.co', 'hotmail.co'
]; */

export interface SpamCheckResult {
  isSpam: boolean;
  reason: string;
  email: string;
  score: number; // 0-100 spam puanı
}

export function checkSpamEmail(email: string): SpamCheckResult {
  const emailLower = email.toLowerCase();
  const domain = emailLower.split('@')[1];
  let score = 0;
  const reasons: string[] = [];
  
  if (!domain) {
    return { isSpam: true, reason: 'Geçersiz email formatı', email, score: 100 };
  }
  
  // Email format validation
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailRegex.test(email)) {
    return { isSpam: true, reason: 'Geçersiz email formatı', email, score: 100 };
  }
  
  // Check for dangerous characters (XSS, SQL injection, etc.)
  if (email.includes('<') || email.includes('>') || email.includes('\'') || 
      email.includes('"') || email.includes('\\') || email.includes('\x00') ||
      email.includes('\r') || email.includes('\n') || email.includes('\t')) {
    return { isSpam: true, reason: 'Güvenlik tehdidi karakterler', email, score: 100 };
  }
  
  // Check for double dots or invalid domain formats
  if (email.includes('..') || domain.endsWith('.') || domain.includes('..')) {
    return { isSpam: true, reason: 'Geçersiz domain formatı', email, score: 100 };
  }
  
  // Check for IP addresses (suspicious but not always spam)
  if (/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(domain) || 
      /^\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\]$/.test(domain)) {
    score = Math.max(score, 60);
    reasons.push('IP address domain');
  }
  
  // Check for very long emails (potential DOS attack)
  if (email.length > 254 || domain.length > 253) {
    return { isSpam: true, reason: 'Çok uzun email', email, score: 100 };
  }
  
  // High-risk spam domains (90-100 puan)
  const highRiskDomains = [
    '10minutemail.com', 'tempmail.org', 'guerrillamail.com', 'mailinator.com',
    'yopmail.com', 'temp-mail.org', 'dispostable.com', 'throwaway.email'
  ];
  
  // Check for subdomain bypass
  const isDomainOrSubdomain = (targetDomain: string) => {
    return domain === targetDomain || domain.endsWith('.' + targetDomain);
  };
  
  if (highRiskDomains.some(isDomainOrSubdomain)) {
    score = 95;
    reasons.push('Geçici email servisi');
  }
  
  // Medium-risk domains (60-80 puan)
  const mediumRiskDomains = [
    'getnada.com', 'maildrop.cc', 'sharklasers.com', 'grr.la'
  ];
  
  if (mediumRiskDomains.some(isDomainOrSubdomain)) {
    score = 70;
    reasons.push('Şüpheli email servisi');
  }
  
  // Common typo domains (40-60 puan)
  const typoDomains = [
    'gmial.com', 'gmai.com', 'yahooo.com', 'hotmial.com',
    'outlok.com', 'gmailcom', 'yahoo.co', 'hotmail.co'
  ];
  
  if (typoDomains.includes(domain)) {
    score = 50;
    reasons.push('Typo domain');
  }
  
  // Test/example domains (should be flagged as spam)
  const testDomains = [
    'example.com', 'test.com', 'sample.com', 'demo.com',
    'localhost', '127.0.0.1'
  ];
  
  if (testDomains.includes(domain)) {
    score = 80;
    reasons.push('Test/example domain');
  }
  
  // Suspicious patterns (10-30 puan)
  if (domain.includes('temp') || domain.includes('disposable') || domain.includes('fake')) {
    score = Math.max(score, 30);
    reasons.push('Şüpheli domain');
  }
  
  // Too many numbers in local part (10-20 puan)
  const localPart = emailLower.split('@')[0];
  const numberCount = (localPart.match(/\d/g) || []).length;
  if (numberCount > localPart.length * 0.7) {
    score = Math.max(score, 20);
    reasons.push('Şüpheli karakter');
  }
  
  // Very short local part (5-15 puan)
  if (localPart.length < 3) {
    score = Math.max(score, 15);
    reasons.push('Kısa email');
  }
  
  // Random character patterns (5-25 puan)
  const hasRandomPattern = /^[a-z0-9]{10,}$/.test(localPart) && localPart.length > 8;
  if (hasRandomPattern) {
    score = Math.max(score, 25);
    reasons.push('Rastgele karakter');
  }
  
  const reason = reasons.length > 0 ? reasons.join(', ') : 'Geçerli email';
  const isSpam = score >= 30; // Lowered threshold for better security
  
  return { isSpam, reason, email, score };
}

export function getSpamStats(data: MarketingData[]) {
  const emails = data.map(item => item.email).filter(email => email);
  const spamResults = emails.map(email => checkSpamEmail(email));
  const spamEmails = spamResults.filter(result => result.isSpam);
  
  return {
    totalEmails: emails.length,
    spamCount: spamEmails.length,
    cleanCount: emails.length - spamEmails.length,
    spamPercentage: emails.length > 0 ? Math.round((spamEmails.length / emails.length) * 100) : 0,
    spamEmails: spamEmails,
  };
}

export function getCompanyStats(data: MarketingData[]) {
  const mevcutMusteriler = data.filter(item => item.isMevcutMusteriler || item.isSalesHubMevcut);
  const withCompany = mevcutMusteriler.filter(item => item.company.trim());
  
  return {
    totalMevcut: mevcutMusteriler.length,
    withCompany: withCompany.length,
    withoutCompany: mevcutMusteriler.length - withCompany.length,
    companyPercentage: mevcutMusteriler.length > 0 ? Math.round((withCompany.length / mevcutMusteriler.length) * 100) : 0,
  };
}

// Force reload
export function removeDuplicateEmails(data: MarketingData[]): MarketingData[] {
  const seen = new Set<string>();
  const result: MarketingData[] = [];
  const duplicateInfo: { email: string; count: number }[] = [];
  
  // İlk geçiş: duplicate'ları tespit et
  const emailCounts = data.reduce((acc, item) => {
    acc[item.email] = (acc[item.email] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  // Duplicate email'leri kaydet
  Object.entries(emailCounts).forEach(([email, count]) => {
    if (count > 1) {
      duplicateInfo.push({ email, count });
    }
  });
  
  // İkinci geçiş: her email'den sadece ilkini al
  data.forEach(item => {
    if (!seen.has(item.email)) {
      seen.add(item.email);
      result.push(item);
    }
  });
  
  return result;
}

export function getDuplicateEmailInfo(data: MarketingData[]): { 
  duplicateEmails: string[]; 
  duplicateCount: number; 
  cleanedCount: number;
  removedCount: number;
} {
  const emailCounts = data.reduce((acc, item) => {
    acc[item.email] = (acc[item.email] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  const duplicateEmails = Object.entries(emailCounts)
    .filter(([, count]) => count > 1)
    .map(([email]) => email);
  
  const duplicateCount = Object.values(emailCounts)
    .filter(count => count > 1)
    .reduce((sum, count) => sum + count, 0);
  
  const cleanedCount = data.length - duplicateEmails.length;
  const removedCount = duplicateCount - duplicateEmails.length;
  
  return {
    duplicateEmails,
    duplicateCount,
    cleanedCount,
    removedCount
  };
}

export function getLicenseCounts(data: MarketingData[]): Record<string, number> {
  const counts: Record<string, number> = {};
  
  data.forEach(item => {
    if (item.license && item.license.trim() !== '') {
      counts[item.license] = (counts[item.license] || 0) + 1;
    }
  });
  
  return counts;
}
