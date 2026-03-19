'use client';

import { useState, useEffect } from 'react';
import { getStatusColor, getStatusBg, getWidthClass } from '@/lib/styles';
import { motion } from 'framer-motion';
import { 
  Link2, 
  Shield, 
  Key, 
  Globe, 
  Zap, 
  Eye,
  AlertCircle,
  CheckCircle,
  RefreshCw,
  Settings,
  Lock,
  Database,
  Cloud,
  FileText
} from 'lucide-react';

export default function Connections() {
  const [connections, setConnections] = useState([
    {
      id: 'google',
      name: 'Google AI (Gemini)',
      status: 'connected',
      lastCheck: '2 dakika önce',
      quotaUsed: 67,
      quotaLimit: 100,
      responseTime: '234ms',
      icon: Cloud,
      color: 'blue'
    },
    {
      id: 'youtube',
      name: 'YouTube Data API',
      status: 'connected',
      lastCheck: '1 dakika önce',
      quotaUsed: 45,
      quotaLimit: 1000,
      responseTime: '189ms',
      icon: Globe,
      color: 'red'
    },
    {
      id: 'meta',
      name: 'Meta Graph API',
      status: 'warning',
      lastCheck: '5 dakika önce',
      quotaUsed: 89,
      quotaLimit: 100,
      responseTime: '445ms',
      icon: Eye,
      color: 'purple'
    },
    {
      id: 'tiktok',
      name: 'TikTok Research API',
      status: 'connected',
      lastCheck: '3 dakika önce',
      quotaUsed: 23,
      quotaLimit: 100,
      responseTime: '567ms',
      icon: Zap,
      color: 'pink'
    },
    {
      id: 'elevenlabs',
      name: 'ElevenLabs Voice',
      status: 'connected',
      lastCheck: '1 dakika önce',
      quotaUsed: 34,
      quotaLimit: 100,
      responseTime: '123ms',
      icon: Key,
      color: 'green'
    }
  ]);

  const [apiKeys] = useState([
    {
      service: 'Google AI',
      key: 'AIzaSyC*********************',
      encrypted: true,
      lastRotated: '7 gün önce',
      status: 'active'
    },
    {
      service: 'YouTube Data API',
      key: 'AIzaSyD*********************',
      encrypted: true,
      lastRotated: '14 gün önce',
      status: 'active'
    },
    {
      service: 'Meta Graph API',
      key: 'EAAC****************************',
      encrypted: true,
      lastRotated: '30 gün önce',
      status: 'warning'
    },
    {
      service: 'TikTok Research API',
      key: 'act_***************************',
      encrypted: true,
      lastRotated: '3 gün önce',
      status: 'active'
    },
    {
      service: 'ElevenLabs',
      key: 'ak_***************************',
      encrypted: true,
      lastRotated: '10 gün önce',
      status: 'active'
    }
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setConnections(prev => prev.map(conn => ({
        ...conn,
        quotaUsed: Math.max(0, Math.min(conn.quotaLimit, conn.quotaUsed + (Math.random() - 0.5) * 5)),
        responseTime: Math.max(50, Math.min(1000, parseInt(conn.responseTime) + (Math.random() - 0.5) * 50)) + 'ms'
      })));
    }, 3000);
    
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected':
      case 'active': return 'text-green-400';
      case 'warning': return 'text-yellow-400';
      case 'error':
      case 'offline': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'connected':
      case 'active': return 'bg-green-500/20';
      case 'warning': return 'bg-yellow-500/20';
      case 'error':
      case 'offline': return 'bg-red-500/20';
      default: return 'bg-gray-500/20';
    }
  };

  const getQuotaColor = (used: number, limit: number) => {
    const percentage = (used / limit) * 100;
    if (percentage < 70) return 'text-green-400';
    if (percentage < 90) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getQuotaBg = (used: number, limit: number) => {
    const percentage = (used / limit) * 100;
    if (percentage < 70) return 'bg-green-500/20';
    if (percentage < 90) return 'bg-yellow-500/20';
    return 'bg-red-500/20';
  };

  const apiUrls = {
    google: 'https://makersuite.google.com/app/apikey',
    youtube: 'https://console.cloud.google.com/apis/credentials',
    meta: 'https://developers.facebook.com/tools/explorer',
    tiktok: 'https://developers.tiktok.com/',
    elevenlabs: 'https://elevenlabs.io/app/settings/api-keys'
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">🔌 Connections</h2>
          <p className="text-gray-400">Encrypted API Vault + Step-by-step Documentation</p>
        </div>
        <div className="flex items-center space-x-2">
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-medium transition-colors flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            Tümünü Test Et
          </button>
          <button className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-white font-medium transition-colors flex items-center gap-2">
            <Key className="w-4 h-4" />
            Yeni API Ekle
          </button>
        </div>
      </div>

      {/* Connection Status Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {connections.map((connection) => {
          const Icon = connection.icon;
          const quotaPercentage = (connection.quotaUsed / connection.quotaLimit) * 100;
          
          return (
            <div key={connection.id} className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 bg-${connection.color}-500/20 rounded-lg flex items-center justify-center`}>
                    <Icon className={`w-5 h-5 text-${connection.color}-400`} />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white">{connection.name}</h3>
                    <p className="text-sm text-gray-400">{connection.lastCheck}</p>
                  </div>
                </div>
                <div className={`px-2 py-1 rounded ${getStatusBg(connection.status)} ${getStatusColor(connection.status)} text-xs`}>
                  {connection.status === 'connected' ? 'Bağlı' : 
                   connection.status === 'warning' ? 'Uyarı' : 
                   connection.status === 'error' ? 'Hata' : 'Offline'}
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Response Time</span>
                  <span className="text-sm text-white">{connection.responseTime}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Kota Kullanımı</span>
                  <span className={`text-sm ${getQuotaColor(connection.quotaUsed, connection.quotaLimit)}`}>
                    {connection.quotaUsed}/{connection.quotaLimit}
                  </span>
                </div>
                
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div 
                    className={`${getQuotaColor(connection.quotaUsed, connection.quotaLimit)} h-2 rounded-full transition-all duration-500 ${getWidthClass(quotaPercentage)}`}
                  />
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-700 flex items-center justify-between">
                <a 
                  href={apiUrls[connection.id as keyof typeof apiUrls]}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-blue-400 hover:text-blue-300 flex items-center gap-1"
                >
                  <Link2 className="w-3 h-3" />
                  Console
                </a>
                <button className="text-xs text-blue-400 hover:text-blue-300 flex items-center gap-1" title="Göster">
                    <Link2 className="w-3 h-3" />
                    Göster
                  </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* API Keys Vault */}
      <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Lock className="w-5 h-5 text-green-400" />
            Şifrelenmiş API Anahtarları
          </h3>
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1">
              <Shield className="w-4 h-4 text-green-400" />
              <span className="text-xs text-green-400">AES-256 Şifreleme Aktif</span>
            </div>
          </div>
        </div>
        
        <div className="space-y-3">
          {apiKeys.map((apiKey, index) => (
            <div key={index} className="bg-gray-900/50 rounded-lg p-4 border border-gray-600">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Key className="w-4 h-4 text-yellow-400" />
                  <div>
                    <span className="text-sm font-medium text-white">{apiKey.service}</span>
                    <div className="text-xs text-gray-400 mt-1">
                      Son rotasyon: {apiKey.lastRotated}
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-1">
                    <Lock className="w-3 h-3 text-green-400" />
                    <span className="text-xs text-green-400">Şifrelenmiş</span>
                  </div>
                  
                  <div className={`px-2 py-1 rounded ${getStatusBg(apiKey.status)} ${getStatusColor(apiKey.status)} text-xs`}>
                    {apiKey.status === 'active' ? 'Aktif' : 'Uyarı'}
                  </div>
                  
                  <button className="text-xs text-blue-400 hover:text-blue-300">
                    Göster
                  </button>
                  
                  <button className="text-xs text-gray-400 hover:text-white" title="Yenile">
                    <RefreshCw className="w-3 h-3" />
                  </button>
                </div>
              </div>
              
              <div className="mt-3 p-2 bg-gray-800/50 rounded border border-gray-700">
                <code className="text-xs text-gray-400 font-mono">{apiKey.key}</code>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Connection Health Monitor */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Database className="w-5 h-5 text-blue-400" />
            Bağlantı Metrikleri
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Toplam API Çağrısı (Bugün)</span>
              <span className="text-sm text-white font-medium">1,247</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Başarılı Çağrılar</span>
              <span className="text-sm text-green-400 font-medium">1,189 (95.3%)</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Hatalı Çağrılar</span>
              <span className="text-sm text-red-400 font-medium">58 (4.7%)</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Ortalama Response Time</span>
              <span className="text-sm text-white font-medium">324ms</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-400">Uptime</span>
              <span className="text-sm text-green-400 font-medium">99.8%</span>
            </div>
          </div>
        </div>

        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <FileText className="w-5 h-5 text-purple-400" />
            API Dokümantasyonu
          </h3>
          <div className="space-y-3">
            <div className="p-3 bg-gray-900/50 rounded-lg border border-gray-600">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium text-white">Google AI Integration</div>
                  <div className="text-xs text-gray-400">Gemini 2.0 Pro API Setup</div>
                </div>
                <button className="text-xs text-blue-400 hover:text-blue-300">Görüntüle</button>
              </div>
            </div>
            
            <div className="p-3 bg-gray-900/50 rounded-lg border border-gray-600">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium text-white">YouTube Data API</div>
                  <div className="text-xs text-gray-400">Video Upload & Analytics</div>
                </div>
                <button className="text-xs text-blue-400 hover:text-blue-300">Görüntüle</button>
              </div>
            </div>
            
            <div className="p-3 bg-gray-900/50 rounded-lg border border-gray-600">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium text-white">Multi-Platform Setup</div>
                  <div className="text-xs text-gray-400">TikTok, Instagram, Facebook</div>
                </div>
                <button className="text-xs text-blue-400 hover:text-blue-300">Görüntüle</button>
              </div>
            </div>
            
            <div className="p-3 bg-gray-900/50 rounded-lg border border-gray-600">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium text-white">Security Best Practices</div>
                  <div className="text-xs text-gray-400">API Key Management</div>
                </div>
                <button className="text-xs text-blue-400 hover:text-blue-300">Görüntüle</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-6 border border-blue-500/30">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5 text-blue-400" />
          Hızlı API Operasyonları
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-blue-500 transition-colors">
            <RefreshCw className="w-6 h-6 text-blue-400 mb-2" />
            <div className="text-sm text-white font-medium">Tümünü Test Et</div>
            <div className="text-xs text-gray-400">Sağlık kontrolü</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-purple-500 transition-colors">
            <Key className="w-6 h-6 text-purple-400 mb-2" />
            <div className="text-sm text-white font-medium">Anahtar Rotasyonu</div>
            <div className="text-xs text-gray-400">Otomatik güncelleme</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-green-500 transition-colors">
            <Shield className="w-6 h-6 text-green-400 mb-2" />
            <div className="text-sm text-white font-medium">Güvenlik Taraması</div>
            <div className="text-xs text-gray-400">Zayıflık analizi</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-yellow-500 transition-colors">
            <FileText className="w-6 h-6 text-yellow-400 mb-2" />
            <div className="text-sm text-white font-medium">Log İndir</div>
            <div className="text-xs text-gray-400">API aktivitesi</div>
          </button>
        </div>
      </div>
    </div>
  );
}
