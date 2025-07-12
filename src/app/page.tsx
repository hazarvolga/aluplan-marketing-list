'use client';

import React, { useState, useEffect } from 'react';
import { Upload, Search, Download, Filter, BarChart3, ChevronUp, ChevronDown, LogOut } from 'lucide-react';
import { MarketingData, FilterOptions, processExcelData, filterData, getSegmentCounts, exportToCSV, getDataQualityStats, checkSpamEmail, removeDuplicateEmails, getDuplicateEmailInfo, getUniqueLicenses } from '@/lib/excel-utils';
import LoginForm from '@/components/LoginForm';

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [data, setData] = useState<MarketingData[]>([]);
  const [filteredData, setFilteredData] = useState<MarketingData[]>([]);
  const [loading, setLoading] = useState(false);
  const [qualityFilter, setQualityFilter] = useState<string | null>(null);
  const [displayCount, setDisplayCount] = useState(100);
  // const [showPhone, setShowPhone] = useState(false); // Telefon sütunu geçici olarak gizlendi
  const [showSpamModal, setShowSpamModal] = useState(false);
  const [sortConfig, setSortConfig] = useState<{
    key: keyof MarketingData | null;
    direction: 'asc' | 'desc';
  }>({
    key: null,
    direction: 'asc',
  });
  const [filters, setFilters] = useState<FilterOptions>({
    segments: {
      mevcutMusteriler: false,
      potansiyelMusteriler: false,
      salesHubMevcut: false,
    },
    searchTerm: '',
    licenses: [],
  });
  const [licenseSearch, setLicenseSearch] = useState('');
  const [showLicenseDropdown, setShowLicenseDropdown] = useState(false);

  // Check authentication on component mount
  useEffect(() => {
    const checkAuth = () => {
      const isAuth = localStorage.getItem('aluplan_authenticated') === 'true';
      const loginTime = localStorage.getItem('aluplan_login_time');
      
      // Check if session expired (24 hours)
      if (isAuth && loginTime) {
        const now = Date.now();
        const loginTimestamp = parseInt(loginTime);
        const sessionDuration = 24 * 60 * 60 * 1000; // 24 hours
        
        if (now - loginTimestamp > sessionDuration) {
          // Session expired
          handleLogout();
          return;
        }
      }
      
      setIsAuthenticated(isAuth);
      setIsCheckingAuth(false);
    };
    
    checkAuth();
  }, []);

  // Load default data on component mount
  useEffect(() => {
    if (isAuthenticated) {
      loadDefaultData();
    }
  }, [isAuthenticated]);

  // Filter data when filters change
  useEffect(() => {
    let filtered = filterData(data, filters);
    
    // Apply quality filter if selected
    if (qualityFilter) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      switch (qualityFilter) {
        case 'duplicateEmails':
          const emails = data.map(item => item.email).filter(email => email);
          const emailCounts = emails.reduce((acc, email) => {
            acc[email] = (acc[email] || 0) + 1;
            return acc;
          }, {} as Record<string, number>);
          // Show ALL records that have duplicate emails (not just unique emails)
          filtered = filtered.filter(item => emailCounts[item.email] > 1);
          break;
        case 'invalidEmails':
          // Filter with priority order: only records that are in "invalid emails" category
          filtered = filtered.filter(item => {
            const emails = data.map(d => d.email).filter(email => email);
            const emailCounts = emails.reduce((acc, email) => {
              acc[email] = (acc[email] || 0) + 1;
              return acc;
            }, {} as Record<string, number>);
            
            const isDuplicate = emailCounts[item.email] > 1;
            const isInvalidEmail = !item.email || !emailRegex.test(item.email);
            
            // Priority: duplicate > invalid
            return !isDuplicate && isInvalidEmail;
          });
          break;
        case 'emptyNames':
          // Filter with priority order: only records that are in "empty names" category
          filtered = filtered.filter(item => {
            const emails = data.map(d => d.email).filter(email => email);
            const emailCounts = emails.reduce((acc, email) => {
              acc[email] = (acc[email] || 0) + 1;
              return acc;
            }, {} as Record<string, number>);
            
            const isDuplicate = emailCounts[item.email] > 1;
            const isInvalidEmail = !item.email || !emailRegex.test(item.email);
            const isEmptyName = !item.name.trim();
            
            // Priority: duplicate > invalid > empty name
            return !isDuplicate && !isInvalidEmail && isEmptyName;
          });
          break;
        case 'emptyCompanies':
          filtered = filtered.filter(item => !item.company.trim());
          break;
        case 'validRecords':
          filtered = filtered.filter(item => 
            item.email.trim() && 
            item.name.trim() && 
            emailRegex.test(item.email)
          );
          break;
        case 'spamEmails':
          // Filter with priority order: only records that are in "spam emails" category
          filtered = filtered.filter(item => {
            const emails = data.map(d => d.email).filter(email => email);
            const emailCounts = emails.reduce((acc, email) => {
              acc[email] = (acc[email] || 0) + 1;
              return acc;
            }, {} as Record<string, number>);
            
            const isDuplicate = emailCounts[item.email] > 1;
            const isInvalidEmail = !item.email || !emailRegex.test(item.email);
            const isEmptyName = !item.name.trim();
            const spamCheck = checkSpamEmail(item.email);
            const isSpam = spamCheck.isSpam;
            
            // Priority: duplicate > invalid > empty name > spam
            return !isDuplicate && !isInvalidEmail && !isEmptyName && isSpam;
          });
          break;
      }
    }
    
    setFilteredData(filtered);
    setDisplayCount(100); // Reset display count when filters change
  }, [data, filters, qualityFilter]);

  // Authentication functions
  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('aluplan_authenticated');
    localStorage.removeItem('aluplan_user');
    localStorage.removeItem('aluplan_login_time');
    setIsAuthenticated(false);
    setData([]);
    setFilteredData([]);
  };

  const loadDefaultData = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/load-data/');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const text = await response.text();
      console.log('API Response:', text);
      
      const result = JSON.parse(text);
      if (result.success) {
        setData(result.data);
      }
    } catch (error) {
      console.error('Failed to load default data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    try {
      const buffer = await file.arrayBuffer();
      const processedData = processExcelData(buffer);
      setData(processedData);
    } catch (error) {
      console.error('Error processing file:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSegmentFilterChange = (segment: keyof FilterOptions['segments']) => {
    setFilters(prev => ({
      ...prev,
      segments: {
        ...prev.segments,
        [segment]: !prev.segments[segment],
      },
    }));
  };

  const handleSearchChange = (value: string) => {
    setFilters(prev => ({
      ...prev,
      searchTerm: value,
    }));
  };

  const handleExport = () => {
    // Remove duplicate emails before export
    const cleanedData = removeDuplicateEmails(filteredData);
    const csv = exportToCSV(cleanedData);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'filtered-marketing-data.csv';
    link.click();
  };

  const resetFilters = () => {
    setFilters({
      segments: {
        mevcutMusteriler: false,
        potansiyelMusteriler: false,
        salesHubMevcut: false,
      },
      searchTerm: '',
      licenses: [],
    });
    setQualityFilter(null);
    setDisplayCount(100);
  };

  const loadMore = () => {
    setDisplayCount(prev => prev + 100);
  };

  const handleSort = (key: keyof MarketingData) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedData = React.useMemo(() => {
    const sortableData = [...filteredData];
    if (sortConfig.key) {
      sortableData.sort((a, b) => {
        const aValue = a[sortConfig.key!];
        const bValue = b[sortConfig.key!];
        
        if (aValue < bValue) {
          return sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (aValue > bValue) {
          return sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableData;
  }, [filteredData, sortConfig]);

  const segmentCounts = getSegmentCounts(data);
  const qualityStats = getDataQualityStats(data);

  // Show loading while checking authentication
  if (isCheckingAuth) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Sistem kontrol ediliyor...</p>
        </div>
      </div>
    );
  }

  // Show login form if not authenticated
  if (!isAuthenticated) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Aluplan Marketing Data Filter
              </h1>
              <p className="text-gray-600">
                Marketing verilerinizi filtreleyin ve analiz edin
              </p>
            </div>
            <button
              onClick={handleLogout}
              className="inline-flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              <LogOut className="w-4 h-4" />
              Çıkış Yap
            </button>
          </div>
        </div>

        {/* Data Quality Info */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-sm p-6 mb-6 border border-blue-100">
          <div className="flex items-center gap-4 mb-4">
            <BarChart3 className="w-5 h-5 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              Veri Kalitesi ve Temizleme
            </h2>
          </div>
          
          {/* Data Quality Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
            <div 
              className={`bg-white rounded-lg p-4 border border-blue-200 cursor-pointer transition-all hover:shadow-md ${
                qualityFilter === 'duplicateEmails' ? 'ring-2 ring-red-500 bg-red-50' : ''
              }`}
              onClick={() => setQualityFilter(qualityFilter === 'duplicateEmails' ? null : 'duplicateEmails')}
            >
              <h3 className="text-sm font-medium text-gray-600 mb-1">Tekrar Kayıtlar</h3>
              <p className="text-lg font-bold text-red-600 mb-1">
                {qualityStats.duplicateEmails.toLocaleString()}
              </p>
              <p className="text-xs text-gray-500">Duplicate e-mail adresi</p>
            </div>
            <div 
              className={`bg-white rounded-lg p-4 border border-blue-200 cursor-pointer transition-all hover:shadow-md ${
                qualityFilter === 'invalidEmails' ? 'ring-2 ring-orange-500 bg-orange-50' : ''
              }`}
              onClick={() => setQualityFilter(qualityFilter === 'invalidEmails' ? null : 'invalidEmails')}
            >
              <h3 className="text-sm font-medium text-gray-600 mb-1">Geçersiz E-mail</h3>
              <p className="text-lg font-bold text-orange-600 mb-1">
                {qualityStats.invalidEmails.toLocaleString()}
              </p>
              <p className="text-xs text-gray-500">Hatalı format</p>
            </div>
            <div 
              className={`bg-white rounded-lg p-4 border border-blue-200 cursor-pointer transition-all hover:shadow-md ${
                qualityFilter === 'emptyNames' ? 'ring-2 ring-yellow-500 bg-yellow-50' : ''
              }`}
              onClick={() => setQualityFilter(qualityFilter === 'emptyNames' ? null : 'emptyNames')}
            >
              <h3 className="text-sm font-medium text-gray-600 mb-1">Eksik İsimler</h3>
              <p className="text-lg font-bold text-yellow-600 mb-1">
                {qualityStats.emptyNames.toLocaleString()}
              </p>
              <p className="text-xs text-gray-500">Boş isim alanı</p>
            </div>
            <div 
              className={`bg-white rounded-lg p-4 border border-blue-200 cursor-pointer transition-all hover:shadow-md ${
                qualityFilter === 'validRecords' ? 'ring-2 ring-green-500 bg-green-50' : ''
              }`}
              onClick={() => setQualityFilter(qualityFilter === 'validRecords' ? null : 'validRecords')}
            >
              <h3 className="text-sm font-medium text-gray-600 mb-1">Geçerli Kayıtlar</h3>
              <p className="text-lg font-bold text-green-600 mb-1">
                {qualityStats.validRecords.toLocaleString()}
              </p>
              <p className="text-xs text-gray-500">Tam ve geçerli veri</p>
            </div>
            <div 
              className={`bg-white rounded-lg p-4 border border-blue-200 cursor-pointer transition-all hover:shadow-md ${
                qualityFilter === 'spamEmails' ? 'ring-2 ring-purple-500 bg-purple-50' : ''
              }`}
              onClick={() => setQualityFilter(qualityFilter === 'spamEmails' ? null : 'spamEmails')}
            >
              <h3 className="text-sm font-medium text-gray-600 mb-1">Spam E-mail</h3>
              <p className="text-lg font-bold text-purple-600 mb-1">
                {qualityStats.spamEmails.toLocaleString()}
              </p>
              <p className="text-xs text-gray-500">Geçici/Spam servis</p>
            </div>
          </div>
        </div>

        {/* File Upload */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center gap-4 mb-4">
            <Upload className="w-5 h-5 text-blue-500" />
            <h2 className="text-xl font-semibold text-gray-900">
              Excel Dosyası Yükle
            </h2>
          </div>
          <input
            type="file"
            accept=".xlsx,.xls"
            onChange={handleFileUpload}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          {data.length > 0 && (
            <p className="text-sm text-gray-600 mt-2">
              {data.length.toLocaleString()} kayıt yüklendi
            </p>
          )}
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center gap-4 mb-4">
            <Filter className="w-5 h-5 text-green-500" />
            <h2 className="text-xl font-semibold text-gray-900">Filtreler</h2>
            <button
              onClick={resetFilters}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Filtreleri Temizle
            </button>
            {qualityFilter && (
              <span className="text-sm bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                Kalite Filtresi: {
                  qualityFilter === 'duplicateEmails' ? 'Tekrar Kayıtlar' :
                  qualityFilter === 'invalidEmails' ? 'Geçersiz E-mail' :
                  qualityFilter === 'emptyNames' ? 'Eksik İsimler' :
                  qualityFilter === 'validRecords' ? 'Geçerli Kayıtlar' :
                  qualityFilter === 'spamEmails' ? 'Spam E-mail' : ''
                }
              </span>
            )}
          </div>

          {/* Search */}
          <div className="mb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="İsim, email veya şirket ara..."
                value={filters.searchTerm}
                onChange={(e) => handleSearchChange(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-500"
              />
            </div>
          </div>

          {/* Segment Filters */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <label className="flex flex-col space-y-1">
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={filters.segments.mevcutMusteriler}
                  onChange={() => handleSegmentFilterChange('mevcutMusteriler')}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm font-semibold text-gray-800">
                  Mevcut Müşteriler ({segmentCounts.mevcutMusteriler.toLocaleString()})
                </span>
              </div>
              <div className="ml-6 text-xs text-gray-500">
                Tüm mevcut müşteri verileri (Dynamics 365 + Allplan)
              </div>
            </label>
            <label className="flex flex-col space-y-1">
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={filters.segments.potansiyelMusteriler}
                  onChange={() => handleSegmentFilterChange('potansiyelMusteriler')}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm font-semibold text-gray-800">
                  Potansiyel Müşteriler ({segmentCounts.potansiyelMusteriler.toLocaleString()})
                </span>
              </div>
              <div className="ml-6 text-xs text-gray-500">
                Sadece Mautic'ten gelen potansiyel müşteriler
              </div>
            </label>
            <label className="flex flex-col space-y-1">
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={filters.segments.salesHubMevcut}
                  onChange={() => handleSegmentFilterChange('salesHubMevcut')}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm font-semibold text-gray-800">
                  Sales Hub ({segmentCounts.salesHubMevcut.toLocaleString()})
                </span>
              </div>
              <div className="ml-6 text-xs text-gray-500">
                Aktif satış sürecindeki müşteriler
              </div>
            </label>
          </div>
          
          {/* Lisans Filtreleme */}
          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Lisans Filtreleme (Autocomplete)
            </label>
            <div className="relative">
              <input
                type="text"
                value={licenseSearch}
                placeholder="Lisans ara... (örn: SSA-12, V2023)"
                className="w-full p-3 border-2 border-gray-300 rounded-lg bg-white text-sm text-gray-800 placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
                onFocus={() => setShowLicenseDropdown(true)}
                onChange={(e) => {
                  setLicenseSearch(e.target.value);
                  setShowLicenseDropdown(true);
                }}
                onBlur={() => setTimeout(() => setShowLicenseDropdown(false), 200)}
              />
              
              {/* Autocomplete dropdown */}
              {showLicenseDropdown && licenseSearch && (
                <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-48 overflow-y-auto">
                  {getUniqueLicenses(data)
                    .filter(license => 
                      license.toLowerCase().includes(licenseSearch.toLowerCase()) &&
                      !filters.licenses.includes(license)
                    )
                    .slice(0, 10)
                    .map(license => (
                      <button
                        key={license}
                        className="w-full px-3 py-2 text-left hover:bg-blue-50 text-sm border-b border-gray-100 last:border-b-0 transition-colors"
                        onClick={() => {
                          setFilters(prev => ({
                            ...prev,
                            licenses: [...prev.licenses, license]
                          }));
                          setLicenseSearch('');
                          setShowLicenseDropdown(false);
                        }}
                      >
                        <div className="flex justify-between items-center">
                          <span className="text-gray-800 font-medium">{license}</span>
                          <span className="text-blue-600 text-xs bg-blue-100 px-2 py-1 rounded-full">
                            {data.filter(item => item.license === license).length} kayıt
                          </span>
                        </div>
                      </button>
                    ))}
                  {getUniqueLicenses(data)
                    .filter(license => 
                      license.toLowerCase().includes(licenseSearch.toLowerCase()) &&
                      !filters.licenses.includes(license)
                    ).length === 0 && (
                    <div className="px-3 py-2 text-gray-600 text-sm">
                      🔍 Eşleşen lisans bulunamadı
                    </div>
                  )}
                </div>
              )}
              
              {/* Seçili lisansları göster */}
              {filters.licenses.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2">
                  {filters.licenses.map(license => (
                    <span key={license} className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-600 text-white shadow-sm">
                      {license} 
                      <span className="ml-1 text-blue-200">
                        ({data.filter(item => item.license === license).length})
                      </span>
                      <button
                        onClick={() => {
                          setFilters(prev => ({
                            ...prev,
                            licenses: prev.licenses.filter(l => l !== license)
                          }));
                        }}
                        className="ml-2 text-blue-200 hover:text-white bg-blue-500 hover:bg-blue-700 rounded-full w-4 h-4 flex items-center justify-center text-xs transition-colors"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>
            <p className="text-sm text-gray-700 mt-2 font-medium">
              {filters.licenses.length > 0 
                ? `✅ Seçilen ${filters.licenses.length} lisans: ${filters.licenses.join(', ')}` 
                : '💡 Lisans aramak için yazmaya başlayın (SSA-12, SUB-12, V2023, vb.)'}
            </p>
          </div>
        </div>

        {/* Export Button */}
        {filteredData.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
            <div className="flex items-center gap-4">
              <button
                onClick={handleExport}
                className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Download className="w-4 h-4" />
                Filtrelenmiş Veriyi İndir ({filteredData.length.toLocaleString()} kayıt)
              </button>
              {(() => {
                const duplicateInfo = getDuplicateEmailInfo(filteredData);
                if (duplicateInfo.duplicateCount > 0) {
                  return (
                    <div className="text-sm text-amber-600 bg-amber-50 px-3 py-1 rounded-lg">
                      📧 {duplicateInfo.duplicateCount} duplicate email otomatik kaldırılacak
                    </div>
                  );
                }
                return null;
              })()}
            </div>
          </div>
        )}

        {/* Data Table */}
        {loading ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Veriler yükleniyor...</p>
          </div>
        ) : filteredData.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <div className="w-16 h-16 mx-auto mb-4 text-gray-400">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Seçilen filtrede kayıt bulunamadı
            </h3>
            <p className="text-gray-600 mb-4">
              Arama kriterlerinize uygun kayıt bulunamadı. Lütfen filtreleri kontrol edin.
            </p>
            <button
              onClick={() =>              setFilters({
                searchTerm: '',
                segments: {
                  mevcutMusteriler: false,
                  potansiyelMusteriler: false,
                  salesHubMevcut: false
                },
                licenses: []
              })}
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              🔄 Filtreleri Temizle
            </button>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-sm overflow-hidden">
            <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">
                  Kayıt Listesi ({filteredData.length.toLocaleString()})
                </h3>
                {/* Telefon göster butonu geçici olarak gizlendi
                <button
                  onClick={() => setShowPhone(!showPhone)}
                  className="inline-flex items-center gap-2 px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  📞 Telefon {showPhone ? 'Gizle' : 'Göster'}
                </button>
                */}
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full table-fixed">
                <colgroup><col className="w-48" /><col className="w-64" /><col className="w-48" /><col className="w-32" /><col className="w-40" /><col className="w-36" /></colgroup>
                <thead className="bg-gray-50">
                  <tr>
                    <th 
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                      onClick={() => handleSort('name')}
                    >
                      <div className="flex items-center gap-2">
                        İsim
                        {sortConfig.key === 'name' && (
                          sortConfig.direction === 'asc' ? 
                            <ChevronUp className="w-4 h-4" /> : 
                            <ChevronDown className="w-4 h-4" />
                        )}
                      </div>
                    </th>
                    <th 
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                      onClick={() => handleSort('email')}
                    >
                      <div className="flex items-center gap-2">
                        Email
                        {sortConfig.key === 'email' && (
                          sortConfig.direction === 'asc' ? 
                            <ChevronUp className="w-4 h-4" /> : 
                            <ChevronDown className="w-4 h-4" />
                        )}
                      </div>
                    </th>
                    <th 
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                      onClick={() => handleSort('spamScore')}
                    >
                      <div className="flex items-center gap-2">
                        Spam Puanı
                        {sortConfig.key === 'spamScore' && (
                          sortConfig.direction === 'asc' ? 
                            <ChevronUp className="w-4 h-4" /> : 
                            <ChevronDown className="w-4 h-4" />
                        )}
                      </div>
                    </th>
                    <th 
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                      onClick={() => handleSort('company')}
                    >
                      <div className="flex items-center gap-2">
                        Şirket
                        {sortConfig.key === 'company' && (
                          sortConfig.direction === 'asc' ? 
                            <ChevronUp className="w-4 h-4" /> : 
                            <ChevronDown className="w-4 h-4" />
                        )}
                      </div>
                    </th>
                    {/* Telefon sütunu geçici olarak gizlendi
                    {showPhone && (
                      <th 
                        className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                        onClick={() => handleSort('phone')}
                      >
                        <div className="flex items-center gap-2">
                          Telefon
                          {sortConfig.key === 'phone' && (
                            sortConfig.direction === 'asc' ? 
                              <ChevronUp className="w-4 h-4" /> : 
                              <ChevronDown className="w-4 h-4" />
                          )}
                        </div>
                      </th>
                    )}
                    */}
                    <th 
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                      onClick={() => handleSort('license')}
                    >
                      <div className="flex items-center gap-2">
                        Lisans
                        {sortConfig.key === 'license' && (
                          sortConfig.direction === 'asc' ? 
                            <ChevronUp className="w-4 h-4" /> : 
                            <ChevronDown className="w-4 h-4" />
                        )}
                      </div>
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Segment
                    </th>
                    <th 
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-colors"
                      onClick={() => handleSort('processingStatus')}
                    >
                      <div className="flex items-center gap-2">
                        İşlenme Durumu
                        {sortConfig.key === 'processingStatus' && (
                          sortConfig.direction === 'asc' ? 
                            <ChevronUp className="w-4 h-4" /> : 
                            <ChevronDown className="w-4 h-4" />
                        )}
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {sortedData.slice(0, displayCount).map((item, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 text-sm font-medium text-gray-900">
                        <div className="truncate" title={item.name}>
                          {item.name}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">
                        <div className="truncate" title={item.email}>
                          {item.email}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <div className="flex items-center gap-2">
                          <div className={`px-3 py-1 rounded-full text-sm font-bold min-w-[3rem] text-center ${
                            item.spamScore >= 80 ? 'bg-red-500 text-white' :
                            item.spamScore >= 60 ? 'bg-orange-500 text-white' :
                            item.spamScore >= 40 ? 'bg-yellow-500 text-white' :
                            item.spamScore >= 20 ? 'bg-blue-500 text-white' :
                            'bg-green-500 text-white'
                          }`}>
                            {item.spamScore}
                          </div>
                          <div className="flex flex-col">
                            <span className="text-xs font-medium text-gray-700">
                              {item.spamScore >= 80 ? 'Çok Yüksek Risk' :
                               item.spamScore >= 60 ? 'Yüksek Risk' :
                               item.spamScore >= 40 ? 'Orta Risk' :
                               item.spamScore >= 20 ? 'Düşük Risk' :
                               'Güvenli'}
                            </span>
                            {item.spamScore > 0 && (
                              <span className="text-xs text-gray-400" title={item.spamReason}>
                                {item.spamReason.split(',')[0]}
                              </span>
                            )}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">
                        <div className="truncate" title={item.company}>
                          {item.company}
                        </div>
                      </td>
                      {/* Telefon sütunu geçici olarak gizlendi
                      {showPhone && (
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {item.phone}
                        </td>
                      )}
                      */}
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {item.license || '-'}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">
                        <div className="flex flex-wrap gap-1">
                          {item.isMevcutMusteriler && (
                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              Mevcut Müşteri
                            </span>
                          )}
                          {item.isPotansiyelMusteriler && (
                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                              Potansiyel Müşteri
                            </span>
                          )}
                          {item.isSalesHubMevcut && (
                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                              Sales Hub
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          item.processingStatus === 'Sales Hub İşlenmiş' ? 'bg-green-100 text-green-800' :
                          item.processingStatus === 'Sales Hub İşlenmemiş' ? 'bg-yellow-100 text-yellow-800' :
                          item.processingStatus === 'Potansiyel' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {item.processingStatus === 'Sales Hub İşlenmiş' ? '✅ İşlenmiş' :
                           item.processingStatus === 'Sales Hub İşlenmemiş' ? '⏳ İşlenmemiş' :
                           item.processingStatus === 'Potansiyel' ? '🔍 Potansiyel' :
                           '❓ Diğer'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {displayCount < sortedData.length && (
              <div className="px-6 py-4 bg-gray-50 text-center">
                <button
                  onClick={loadMore}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Daha Fazla Yükle ({displayCount} / {sortedData.length.toLocaleString()})
                </button>
              </div>
            )}
            {displayCount >= sortedData.length && sortedData.length > 100 && (
              <div className="px-6 py-4 bg-gray-50 text-center text-sm text-gray-600">
                Tüm {sortedData.length.toLocaleString()} kayıt gösteriliyor.
              </div>
            )}
          </div>
        )}

        {/* Spam Filter Modal */}
      {showSpamModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-gray-900">🛡️ Spam E-mail Filtresi Özellikleri</h2>
                <button
                  onClick={() => setShowSpamModal(false)}
                  className="text-gray-400 hover:text-gray-600 text-2xl"
                >
                  ×
                </button>
              </div>
              
              <div className="space-y-6">
                {/* Spam Tespit Yöntemleri */}
                <div className="bg-gradient-to-r from-red-50 to-orange-50 rounded-lg p-4 border border-red-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">📊 Spam Tespit Yöntemleri</h3>
                  <div className="space-y-2 text-sm text-gray-700">
                    <div><strong>Geçici Email Servisleri:</strong> 10minutemail, tempmail, guerrillamail, mailinator vb.</div>
                    <div><strong>Spam Domain&apos;ler:</strong> Bilinen spam domain&apos;leri tespit eder</div>
                    <div><strong>Şüpheli Pattern&apos;ler:</strong> &quot;temp&quot;, &quot;disposable&quot;, &quot;fake&quot; içeren domain&apos;ler</div>
                    <div><strong>Karakter Analizi:</strong> Çok sayıda rakam içeren şüpheli email&apos;ler</div>
                    <div><strong>Typo Domain&apos;ler:</strong> gmial.com, yahooo.com gibi hatalı yazımlar</div>
                  </div>
                </div>

                {/* Kalite Kartı */}
                <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-4 border border-purple-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">🎯 Yeni Kalite Kartı</h3>
                  <div className="space-y-2 text-sm text-gray-700">
                    <div><strong>Spam E-mail:</strong> Mor renkte, tıklanabilir kart</div>
                    <div><strong>Gerçek Zamanlı Sayım:</strong> Spam email sayısını gösterir</div>
                    <div><strong>Filtreleme:</strong> Tıklandığında sadece spam email&apos;leri listeler</div>
                  </div>
                </div>

                {/* Filtreleme Özellikleri */}
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">🔍 Filtreleme Özellikleri</h3>
                  <div className="space-y-2 text-sm text-gray-700">
                    <div><strong>Kombine Filtreleme:</strong> Diğer kalite filtreleri ile kombine edilebilir</div>
                    <div><strong>Segment Uyumu:</strong> Segment filtreleri ile birlikte çalışır</div>
                    <div><strong>Arama Entegrasyonu:</strong> Arama ile kombine edilebilir</div>
                    <div><strong>Görsel Geri Bildirim:</strong> &quot;Spam E-mail&quot; badge&apos;i ile aktif filtre gösterilir</div>
                  </div>
                </div>

                {/* Teknik Detaylar */}
                <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-lg p-4 border border-green-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">📈 Teknik Detaylar</h3>
                  <div className="space-y-2 text-sm text-gray-700">
                    <div><strong>40+ Spam Domain:</strong> Kapsamlı spam domain listesi</div>
                    <div><strong>Pattern Matching:</strong> Akıllı şüpheli email tespiti</div>
                    <div><strong>Performans:</strong> Hızlı client-side filtering</div>
                    <div><strong>Accuracy:</strong> Yüksek doğruluk oranı</div>
                  </div>
                </div>
              </div>

              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => setShowSpamModal(false)}
                  className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                >
                  Kapat
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
      </div>
    </div>
  );
}
