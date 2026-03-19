'use client';

import { useState, useEffect } from 'react';
import { getStatusColor, getStatusBg, getWidthClass } from '@/lib/styles';
import { motion } from 'framer-motion';
import { 
  Globe, 
  Scissors, 
  Upload, 
  Play, 
  Eye, 
  TrendingUp, 
  Zap,
  Smartphone,
  Monitor,
  Camera,
  Video,
  BarChart3,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react';

export default function MultiVerse() {
  const [activePlatforms, setActivePlatforms] = useState(['youtube', 'tiktok', 'instagram']);
  const [processingVideos, setProcessingVideos] = useState([
    { id: 1, title: "AI ile Para Kazanma 2026", platforms: ['youtube', 'tiktok'], status: 'processing', progress: 65 },
    { id: 2, title: "ChatGPT 5.0 İnceleme", platforms: ['instagram', 'facebook'], status: 'queued', progress: 0 },
    { id: 3, title: "Yapay Zeka Trendleri", platforms: ['youtube', 'tiktok', 'instagram'], status: 'completed', progress: 100 }
  ]);

  const platformConfigs = [
    {
      id: 'youtube',
      name: 'YouTube',
      icon: Monitor,
      ratio: '16:9',
      resolution: '1920x1080',
      maxDuration: '12:00',
      color: 'red',
      active: true
    },
    {
      id: 'tiktok',
      name: 'TikTok',
      icon: Smartphone,
      ratio: '9:16',
      resolution: '1080x1920',
      maxDuration: '3:00',
      color: 'pink',
      active: true
    },
    {
      id: 'instagram',
      name: 'Instagram Reels',
      icon: Camera,
      ratio: '9:16',
      resolution: '1080x1920',
      maxDuration: '1:30',
      color: 'purple',
      active: true
    },
    {
      id: 'facebook',
      name: 'Facebook',
      icon: Globe,
      ratio: '16:9',
      resolution: '1920x1080',
      maxDuration: '10:00',
      color: 'blue',
      active: false
    },
    {
      id: 'twitter',
      name: 'X/Twitter',
      icon: Video,
      ratio: '16:9',
      resolution: '1920x1080',
      maxDuration: '2:20',
      color: 'black',
      active: false
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setProcessingVideos(prev => prev.map(video => {
        if (video.status === 'processing' && video.progress < 100) {
          return { ...video, progress: Math.min(100, video.progress + Math.random() * 8) };
        }
        return video;
      }));
    }, 2000);
    
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-400';
      case 'processing': return 'text-yellow-400';
      case 'queued': return 'text-gray-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500/20';
      case 'processing': return 'bg-yellow-500/20';
      case 'queued': return 'bg-gray-500/20';
      default: return 'bg-gray-500/20';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed': return 'Tamamlandı';
      case 'processing': return 'İşleniyor';
      case 'queued': return 'Sırada';
      default: return 'Bilinmiyor';
    }
  };

  const togglePlatform = (platformId: string) => {
    setActivePlatforms(prev => 
      prev.includes(platformId) 
        ? prev.filter(id => id !== platformId)
        : [...prev, platformId]
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">🌌 Multi-Verse</h2>
          <p className="text-gray-400">AI-Cutter (9:16) + Platform adaptation (TikTok/IG/X/FB)</p>
        </div>
        <div className="flex items-center space-x-2">
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-medium transition-colors flex items-center gap-2">
            <Scissors className="w-4 h-4" />
            Auto-Cutter
          </button>
          <button className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-white font-medium transition-colors flex items-center gap-2">
            <Upload className="w-4 h-4" />
            Bulk Upload
          </button>
        </div>
      </div>

      {/* Platform Selector */}
      <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Globe className="w-5 h-5 text-blue-400" />
          Platform Adaptasyonu
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {platformConfigs.map((platform) => {
            const Icon = platform.icon;
            const isActive = activePlatforms.includes(platform.id);
            
            return (
              <button
                key={platform.id}
                onClick={() => togglePlatform(platform.id)}
                className={`p-4 rounded-lg border transition-all ${
                  isActive 
                    ? `bg-${platform.color}-500/20 border-${platform.color}-500 text-${platform.color}-400`
                    : 'bg-gray-900/50 border-gray-600 text-gray-400 hover:border-gray-500'
                }`}
              >
                <Icon className="w-6 h-6 mb-2 mx-auto" />
                <div className="text-sm font-medium">{platform.name}</div>
                <div className="text-xs text-gray-400 mt-1">{platform.ratio}</div>
                <div className="text-xs text-gray-500">{platform.maxDuration}</div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Processing Queue */}
      <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-400" />
            Multi-Platform İşlem Kuyruğu
          </h3>
          <span className="text-xs text-gray-400">{processingVideos.length} video işleniyor</span>
        </div>
        <div className="space-y-4">
          {processingVideos.map((video) => (
            <div key={video.id} className="bg-gray-900/50 rounded-lg p-4 border border-gray-600">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <h4 className="text-white font-medium">{video.title}</h4>
                  <div className="flex items-center gap-2 mt-1">
                    {video.platforms.map((platform) => {
                      const config = platformConfigs.find(p => p.id === platform);
                      const Icon = config?.icon || Monitor;
                      return (
                        <span key={platform} className="flex items-center gap-1 text-xs text-gray-400">
                          <Icon className="w-3 h-3" />
                          {config?.name}
                        </span>
                      );
                    })}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`text-xs px-2 py-1 rounded ${getStatusBg(video.status)} ${getStatusColor(video.status)}`}>
                    {getStatusText(video.status)}
                  </span>
                  {video.status === 'completed' && <CheckCircle className="w-4 h-4 text-green-400" />}
                  {video.status === 'processing' && <AlertCircle className="w-4 h-4 text-yellow-400" />}
                </div>
              </div>
              
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs text-gray-400">İşlem Süreci</span>
                <span className="text-xs text-gray-400">{video.progress}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div 
                  className={`bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-500 ${getWidthClass(video.progress)}`}
                />
              </div>
              
              {/* Platform Progress */}
              <div className="grid grid-cols-5 gap-2 mt-3">
                {platformConfigs.map((platform) => {
                  const isProcessing = video.platforms.includes(platform.id);
                  const Icon = platform.icon;
                  
                  return (
                    <div key={platform.id} className="text-center">
                      <Icon className={`w-4 h-4 mx-auto mb-1 ${
                        isProcessing ? 'text-blue-400' : 'text-gray-600'
                      }`} />
                      <div className="text-xs text-gray-400">{platform.name}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* AI-Cutter Settings */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Scissors className="w-5 h-5 text-purple-400" />
            AI-Cutter Ayarları
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-300">Otomatik 9:16 Dönüşüm</span>
              <div className="w-12 h-6 bg-blue-600 rounded-full relative">
                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-300">Smart Cropping</span>
              <div className="w-12 h-6 bg-blue-600 rounded-full relative">
                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-300">Focus Point Detection</span>
              <div className="w-12 h-6 bg-blue-600 rounded-full relative">
                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-300">Motion Tracking</span>
              <div className="w-12 h-6 bg-gray-600 rounded-full relative">
                <div className="absolute left-1 top-1 w-4 h-4 bg-white rounded-full"></div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-green-400" />
            Platform Performansı
          </h3>
          <div className="space-y-4">
            {platformConfigs.filter(p => activePlatforms.includes(p.id)).map((platform) => {
              const Icon = platform.icon;
              const performance = Math.random() * 100;
              
              return (
                <div key={platform.id} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Icon className="w-4 h-4 text-gray-400" />
                    <span className="text-sm text-gray-300">{platform.name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-24 bg-gray-700 rounded-full h-2">
                      <div 
                        className={`bg-green-500 h-2 rounded-full ${getWidthClass(performance)}`}
                      />
                    </div>
                    <span className="text-xs text-gray-400">{performance}%</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-gradient-to-r from-pink-500/10 to-purple-500/10 rounded-xl p-6 border border-pink-500/30">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5 text-pink-400" />
          Hızlı Platform Operasyonları
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-pink-500 transition-colors">
            <Scissors className="w-6 h-6 text-pink-400 mb-2" />
            <div className="text-sm text-white font-medium">Tümünü Kes</div>
            <div className="text-xs text-gray-400">9:16 format</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-purple-500 transition-colors">
            <Upload className="w-6 h-6 text-purple-400 mb-2" />
            <div className="text-sm text-white font-medium">Toplu Yükle</div>
            <div className="text-xs text-gray-400">Tüm platformlar</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-blue-500 transition-colors">
            <Eye className="w-6 h-6 text-blue-400 mb-2" />
            <div className="text-sm text-white font-medium">Performans</div>
            <div className="text-xs text-gray-400">Analiz et</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-green-500 transition-colors">
            <TrendingUp className="w-6 h-6 text-green-400 mb-2" />
            <div className="text-sm text-white font-medium">Optimizasyon</div>
            <div className="text-xs text-gray-400">AI destekli</div>
          </button>
        </div>
      </div>
    </div>
  );
}
