'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  BarChart3, 
  TrendingUp, 
  Eye, 
  DollarSign, 
  Users, 
  Play,
  Globe,
  Zap,
  Activity,
  Target,
  Clock,
  ArrowUp,
  ArrowDown,
  Minus,
  Calendar,
  Filter
} from 'lucide-react';

export default function GlobalAnalytics() {
  const [timeRange, setTimeRange] = useState('7d');
  const [selectedMetrics, setSelectedMetrics] = useState(['views', 'revenue', 'engagement']);
  
  const [globalStats, setGlobalStats] = useState({
    totalViews: 2456789,
    totalRevenue: 45678,
    totalChannels: 127,
    totalVideos: 892,
    engagementRate: 8.7,
    avgCPM: 4.23,
    viralScore: 94,
    growthRate: 34.2
  });

  const [platformPerformance, setPlatformPerformance] = useState([
    {
      platform: 'YouTube',
      views: 1234567,
      revenue: 23456,
      videos: 456,
      engagement: 9.2,
      growth: 42.1,
      color: 'red'
    },
    {
      platform: 'TikTok',
      views: 876543,
      revenue: 12345,
      videos: 234,
      engagement: 12.8,
      growth: 67.3,
      color: 'pink'
    },
    {
      platform: 'Instagram',
      views: 345678,
      revenue: 8765,
      videos: 123,
      engagement: 6.4,
      growth: 23.7,
      color: 'purple'
    },
    {
      platform: 'Facebook',
      views: 234567,
      revenue: 3456,
      videos: 78,
      engagement: 4.1,
      growth: 12.3,
      color: 'blue'
    },
    {
      platform: 'X/Twitter',
      views: 123456,
      revenue: 1234,
      videos: 45,
      engagement: 3.2,
      growth: -5.4,
      color: 'black'
    }
  ]);

  const [topVideos, setTopVideos] = useState([
    {
      title: "AI ile Para Kazanma 2026",
      views: 1234567,
      revenue: 5678,
      engagement: 15.2,
      platforms: ['youtube', 'tiktok', 'instagram'],
      growth: 234.5,
      thumbnail: '/api/placeholder/320/180'
    },
    {
      title: "ChatGPT 5.0 İnceleme",
      views: 987654,
      revenue: 3456,
      engagement: 12.8,
      platforms: ['youtube', 'instagram'],
      growth: 156.7,
      thumbnail: '/api/placeholder/320/180'
    },
    {
      title: "Yapay Zeka Trendleri",
      views: 876543,
      revenue: 2345,
      engagement: 10.4,
      platforms: ['youtube', 'tiktok'],
      growth: 89.3,
      thumbnail: '/api/placeholder/320/180'
    }
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setGlobalStats(prev => ({
        ...prev,
        totalViews: prev.totalViews + Math.floor(Math.random() * 1000),
        totalRevenue: prev.totalRevenue + Math.floor(Math.random() * 100),
        engagementRate: Math.max(0, Math.min(100, prev.engagementRate + (Math.random() - 0.5) * 0.5)),
        growthRate: Math.max(0, Math.min(100, prev.growthRate + (Math.random() - 0.5) * 1))
      }));
      
      setPlatformPerformance(prev => prev.map(platform => ({
        ...platform,
        views: platform.views + Math.floor(Math.random() * 500),
        revenue: platform.revenue + Math.floor(Math.random() * 50),
        engagement: Math.max(0, Math.min(100, platform.engagement + (Math.random() - 0.5) * 0.3))
      })));
    }, 3000);
    
    return () => clearInterval(interval);
  }, []);

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const formatCurrency = (num: number) => {
    return '$' + formatNumber(num);
  };

  const getGrowthIcon = (growth: number) => {
    if (growth > 0) return <ArrowUp className="w-4 h-4 text-green-400" />;
    if (growth < 0) return <ArrowDown className="w-4 h-4 text-red-400" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
  };

  const getGrowthColor = (growth: number) => {
    if (growth > 0) return 'text-green-400';
    if (growth < 0) return 'text-red-400';
    return 'text-gray-400';
  };

  const timeRanges = [
    { id: '24h', label: '24 Saat' },
    { id: '7d', label: '7 Gün' },
    { id: '30d', label: '30 Gün' },
    { id: '90d', label: '90 Gün' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">📈 Global Analytics</h2>
          <p className="text-gray-400">Unified ROI, CPM, and Viral Velocity heatmaps</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="flex bg-gray-800 rounded-lg border border-gray-700">
            {timeRanges.map((range) => (
              <button
                key={range.id}
                onClick={() => setTimeRange(range.id)}
                className={`px-4 py-2 text-sm font-medium transition-colors ${
                  timeRange === range.id
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                {range.label}
              </button>
            ))}
          </div>
          <button className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-white font-medium transition-colors flex items-center gap-2">
            <Filter className="w-4 h-4" />
            Filtrele
          </button>
        </div>
      </div>

      {/* Global Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <Eye className="w-8 h-8 text-blue-400" />
            <div className="flex items-center gap-1">
              {getGrowthIcon(globalStats.growthRate)}
              <span className={`text-sm ${getGrowthColor(globalStats.growthRate)}`}>
                +{globalStats.growthRate}%
              </span>
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-2">
            {formatNumber(globalStats.totalViews)}
          </div>
          <div className="text-sm text-gray-400">Toplam İzlenme</div>
        </div>

        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <DollarSign className="w-8 h-8 text-green-400" />
            <div className="flex items-center gap-1">
              {getGrowthIcon(23.4)}
              <span className="text-sm text-green-400">+23.4%</span>
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-2">
            {formatCurrency(globalStats.totalRevenue)}
          </div>
          <div className="text-sm text-gray-400">Toplam Gelir</div>
        </div>

        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <Users className="w-8 h-8 text-purple-400" />
            <div className="flex items-center gap-1">
              {getGrowthIcon(12.7)}
              <span className="text-sm text-green-400">+12.7%</span>
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-2">
            {globalStats.totalChannels}
          </div>
          <div className="text-sm text-gray-400">Aktif Kanal</div>
        </div>

        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <Target className="w-8 h-8 text-red-400" />
            <div className="flex items-center gap-1">
              {getGrowthIcon(8.2)}
              <span className="text-sm text-green-400">+8.2%</span>
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-2">
            {globalStats.viralScore}%
          </div>
          <div className="text-sm text-gray-400">Viral Score</div>
        </div>
      </div>

      {/* Platform Performance */}
      <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Globe className="w-5 h-5 text-blue-400" />
          Platform Performansı
        </h3>
        <div className="space-y-4">
          {platformPerformance.map((platform) => (
            <div key={platform.platform} className="bg-gray-900/50 rounded-lg p-4 border border-gray-600">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 bg-${platform.color}-500/20 rounded-lg flex items-center justify-center`}>
                    <Play className={`w-4 h-4 text-${platform.color}-400`} />
                  </div>
                  <div>
                    <h4 className="text-white font-medium">{platform.platform}</h4>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-sm text-gray-400">{platform.videos} video</span>
                      <span className="text-gray-600">•</span>
                      <div className="flex items-center gap-1">
                        {getGrowthIcon(platform.growth)}
                        <span className={`text-sm ${getGrowthColor(platform.growth)}`}>
                          {platform.growth > 0 ? '+' : ''}{platform.growth}%
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-4 gap-4">
                <div>
                  <div className="text-sm text-gray-400 mb-1">İzlenme</div>
                  <div className="text-lg font-semibold text-white">
                    {formatNumber(platform.views)}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-400 mb-1">Gelir</div>
                  <div className="text-lg font-semibold text-white">
                    {formatCurrency(platform.revenue)}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-400 mb-1">Etkileşim</div>
                  <div className="text-lg font-semibold text-white">
                    {platform.engagement}%
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-400 mb-1">CPM</div>
                  <div className="text-lg font-semibold text-white">
                    ${((platform.revenue / platform.views) * 1000).toFixed(2)}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Top Performing Videos */}
      <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-green-400" />
          En Performanslı Videolar
        </h3>
        <div className="space-y-4">
          {topVideos.map((video, index) => (
            <div key={index} className="bg-gray-900/50 rounded-lg p-4 border border-gray-600">
              <div className="flex items-center gap-4">
                <div className="w-20 h-12 bg-gray-700 rounded-lg flex items-center justify-center">
                  <Play className="w-6 h-6 text-gray-400" />
                </div>
                <div className="flex-1">
                  <h4 className="text-white font-medium mb-1">{video.title}</h4>
                  <div className="flex items-center gap-4 text-sm text-gray-400">
                    <span className="flex items-center gap-1">
                      <Eye className="w-3 h-3" />
                      {formatNumber(video.views)}
                    </span>
                    <span className="flex items-center gap-1">
                      <DollarSign className="w-3 h-3" />
                      {formatCurrency(video.revenue)}
                    </span>
                    <span className="flex items-center gap-1">
                      <Activity className="w-3 h-3" />
                      {video.engagement}%
                    </span>
                    <div className="flex items-center gap-1">
                      {getGrowthIcon(video.growth)}
                      <span className={getGrowthColor(video.growth)}>
                        {video.growth > 0 ? '+' : ''}{video.growth}%
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {video.platforms.map((platform) => (
                    <div key={platform} className="px-2 py-1 bg-gray-700 rounded text-xs text-gray-400">
                      {platform === 'youtube' ? 'YT' : 
                       platform === 'tiktok' ? 'TT' : 
                       platform === 'instagram' ? 'IG' : 
                       platform === 'facebook' ? 'FB' : 'X'}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Analytics Heatmap */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5 text-purple-400" />
            Viral Velocity Heatmap
          </h3>
          <div className="grid grid-cols-7 gap-1">
            {['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'].map((day) => (
              <div key={day} className="text-center">
                <div className="text-xs text-gray-400 mb-2">{day}</div>
                {[...Array(24)].map((_, hour) => {
                  const intensity = Math.random();
                  const color = intensity > 0.8 ? 'bg-red-500' : 
                               intensity > 0.6 ? 'bg-orange-500' : 
                               intensity > 0.4 ? 'bg-yellow-500' : 
                               intensity > 0.2 ? 'bg-green-500' : 'bg-gray-700';
                  
                  return (
                    <div
                      key={hour}
                      className={`w-full h-4 ${color} rounded-sm mb-1`}
                      title={`${hour}:00 - ${intensity.toFixed(2)}`}
                    />
                  );
                })}
              </div>
            ))}
          </div>
          <div className="flex items-center justify-between mt-4 text-xs text-gray-400">
            <span>Düşük Aktivite</span>
            <div className="flex items-center gap-1">
              <div className="w-3 h-3 bg-gray-700 rounded-sm"></div>
              <div className="w-3 h-3 bg-green-500 rounded-sm"></div>
              <div className="w-3 h-3 bg-yellow-500 rounded-sm"></div>
              <div className="w-3 h-3 bg-orange-500 rounded-sm"></div>
              <div className="w-3 h-3 bg-red-500 rounded-sm"></div>
            </div>
            <span>Yüksek Aktivite</span>
          </div>
        </div>

        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Clock className="w-5 h-5 text-blue-400" />
            Optimal Yayın Zamanları
          </h3>
          <div className="space-y-3">
            {[
              { platform: 'YouTube', time: '19:00 - 21:00', reason: 'Prime time, yüksek engagement' },
              { platform: 'TikTok', time: '12:00 - 14:00', reason: 'Öğle arası, genç kitle aktif' },
              { platform: 'Instagram', time: '18:00 - 20:00', reason: 'İş çıkışı, story zamanı' },
              { platform: 'Facebook', time: '14:00 - 16:00', reason: 'İş saatleri, paylaşım oranı yüksek' },
              { platform: 'X/Twitter', time: '08:00 - 10:00', reason: 'Sabah haberleri, retweet potansiyeli' }
            ].map((item, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-900/50 rounded-lg border border-gray-600">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
                    <Play className="w-4 h-4 text-blue-400" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-white">{item.platform}</div>
                    <div className="text-xs text-gray-400">{item.reason}</div>
                  </div>
                </div>
                <div className="text-sm text-blue-400 font-medium">{item.time}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-xl p-6 border border-green-500/30">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5 text-green-400" />
          Hızlı Analiz Operasyonları
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-green-500 transition-colors">
            <BarChart3 className="w-6 h-6 text-green-400 mb-2" />
            <div className="text-sm text-white font-medium">Detaylı Rapor</div>
            <div className="text-xs text-gray-400">PDF İndir</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-blue-500 transition-colors">
            <Target className="w-6 h-6 text-blue-400 mb-2" />
            <div className="text-sm text-white font-medium">Trend Analizi</div>
            <div className="text-xs text-gray-400">AI destekli</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-purple-500 transition-colors">
            <Calendar className="w-6 h-6 text-purple-400 mb-2" />
            <div className="text-sm text-white font-medium">Planlama</div>
            <div className="text-xs text-gray-400">Optimal zamanlar</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-red-500 transition-colors">
            <DollarSign className="w-6 h-6 text-red-400 mb-2" />
            <div className="text-sm text-white font-medium">ROI Optimizasyon</div>
            <div className="text-xs text-gray-400">Otomatik</div>
          </button>
        </div>
      </div>
    </div>
  );
}
