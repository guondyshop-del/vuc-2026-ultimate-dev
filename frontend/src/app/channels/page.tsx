'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Youtube, 
  Settings, 
  TrendingUp, 
  Users, 
  Calendar,
  DollarSign,
  Eye,
  Activity,
  Shield,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock,
  Target,
  Zap,
  Globe,
  Key,
  BarChart3,
  Upload
} from 'lucide-react';
import styles from './Channels.module.css';

interface Channel {
  id: number;
  name: string;
  channel_id: string;
  niche: string;
  language: string;
  target_audience?: string;
  description?: string;
  keywords: string[];
  is_active: boolean;
  auto_upload: boolean;
  upload_schedule?: any;
  created_at: string;
  updated_at: string;
  api_key?: string;
  client_secret?: string;
  daily_upload_target: number;
  target_views_per_video: number;
  competitor_analysis_enabled: boolean;
  // Analytics
  subscribers: number;
  total_views: number;
  total_videos: number;
  monthly_revenue: number;
  engagement_rate: number;
  // Status
  last_sync: string;
  health_score: number;
  quota_usage: number;
  // Logs
  recent_activities: ActivityLog[];
}

interface ActivityLog {
  id: number;
  type: 'upload' | 'sync' | 'error' | 'success';
  message: string;
  timestamp: string;
  details?: any;
}

const ChannelsPage = () => {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [selectedChannel, setSelectedChannel] = useState<Channel | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'analytics' | 'settings' | 'logs'>('overview');

  useEffect(() => {
    fetchChannels();
  }, []);

  const fetchChannels = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/channels');
      const data = await response.json();
      if (data.success) {
        setChannels(data.channels);
      }
    } catch (error) {
      console.error('Kanallar yüklenirken hata:', error);
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (score: number) => {
    if (score >= 90) return 'text-green-400';
    if (score >= 70) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getStatusIcon = (channel: Channel) => {
    if (!channel.is_active) return <XCircle className="w-4 h-4 text-red-400" />;
    if (channel.health_score >= 90) return <CheckCircle className="w-4 h-4 text-green-400" />;
    return <AlertTriangle className="w-4 h-4 text-yellow-400" />;
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('tr-TR', {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <Youtube className="w-8 h-8 text-red-500" />
            <h1 className="text-3xl font-bold">YouTube Kanalları</h1>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
          >
            <Zap className="w-4 h-4" />
            <span>Yeni Kanal Ekle</span>
          </button>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Toplam Kanal</p>
                <p className="text-2xl font-bold">{channels.length}</p>
              </div>
              <Youtube className="w-8 h-8 text-blue-400" />
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Toplam Abone</p>
                <p className="text-2xl font-bold">
                  {formatNumber(channels.reduce((sum, ch) => sum + ch.subscribers, 0))}
                </p>
              </div>
              <Users className="w-8 h-8 text-green-400" />
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Toplam İzlenme</p>
                <p className="text-2xl font-bold">
                  {formatNumber(channels.reduce((sum, ch) => sum + ch.total_views, 0))}
                </p>
              </div>
              <Eye className="w-8 h-8 text-purple-400" />
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Aylık Gelir</p>
                <p className="text-2xl font-bold">
                  ${formatNumber(channels.reduce((sum, ch) => sum + ch.monthly_revenue, 0))}
                </p>
              </div>
              <DollarSign className="w-8 h-8 text-yellow-400" />
            </div>
          </div>
        </div>
      </div>

      {/* Channels Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {channels.map((channel) => (
          <motion.div
            key={channel.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gray-800 rounded-lg border border-gray-700 hover:border-gray-600 transition-all cursor-pointer"
            onClick={() => setSelectedChannel(channel)}
          >
            <div className="p-6">
              {/* Channel Header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-red-500 to-red-600 rounded-full flex items-center justify-center">
                    <Youtube className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">{channel.name}</h3>
                    <p className="text-gray-400 text-sm">@{channel.channel_id}</p>
                  </div>
                </div>
                {getStatusIcon(channel)}
              </div>

              {/* Channel Stats */}
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-gray-400 text-xs">Aboneler</p>
                  <p className="font-semibold">{formatNumber(channel.subscribers)}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-xs">İzlenme</p>
                  <p className="font-semibold">{formatNumber(channel.total_views)}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-xs">Etkileşim</p>
                  <p className="font-semibold">{channel.engagement_rate}%</p>
                </div>
                <div>
                  <p className="text-gray-400 text-xs">Sağlık</p>
                  <p className={`font-semibold ${getHealthColor(channel.health_score)}`}>
                    {channel.health_score}%
                  </p>
                </div>
              </div>

              {/* Channel Tags */}
              <div className="flex flex-wrap gap-2 mb-4">
                <span className="bg-blue-900 text-blue-300 px-2 py-1 rounded text-xs">
                  {channel.niche}
                </span>
                <span className="bg-green-900 text-green-300 px-2 py-1 rounded text-xs">
                  {channel.language}
                </span>
                {channel.auto_upload && (
                  <span className="bg-purple-900 text-purple-300 px-2 py-1 rounded text-xs">
                    Otomatik
                  </span>
                )}
              </div>

              {/* Last Activity */}
              <div className="text-xs text-gray-400">
                Son sync: {formatDate(channel.last_sync)}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Channel Detail Modal */}
      {selectedChannel && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              {/* Modal Header */}
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-red-500 to-red-600 rounded-full flex items-center justify-center">
                    <Youtube className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold">{selectedChannel.name}</h2>
                    <p className="text-gray-400">@{selectedChannel.channel_id}</p>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedChannel(null)}
                  className="text-gray-400 hover:text-white transition-colors"
                  title="Modalı Kapat"
                  aria-label="Modalı Kapat"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>

              {/* Tabs */}
              <div className="flex space-x-1 mb-6 border-b border-gray-700">
                {(['overview', 'analytics', 'settings', 'logs'] as const).map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`px-4 py-2 capitalize transition-colors ${
                      activeTab === tab
                        ? 'text-blue-400 border-b-2 border-blue-400'
                        : 'text-gray-400 hover:text-white'
                    }`}
                    title={`${tab === 'overview' && 'Genel Bakış'}${tab === 'analytics' && 'Analitik'}${tab === 'settings' && 'Ayarlar'}${tab === 'logs' && 'Loglar'} sekmesine git`}
                    aria-label={`${tab === 'overview' && 'Genel Bakış'}${tab === 'analytics' && 'Analitik'}${tab === 'settings' && 'Ayarlar'}${tab === 'logs' && 'Loglar'} sekmesi`}
                  >
                    {tab === 'overview' && 'Genel Bakış'}
                    {tab === 'analytics' && 'Analitik'}
                    {tab === 'settings' && 'Ayarlar'}
                    {tab === 'logs' && 'Loglar'}
                  </button>
                ))}
              </div>

              {/* Tab Content */}
              <div className="min-h-[400px]">
                {activeTab === 'overview' && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="text-lg font-semibold mb-4">Kanal Bilgileri</h3>
                      <div className="space-y-3">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Niche:</span>
                          <span>{selectedChannel.niche}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Dil:</span>
                          <span>{selectedChannel.language}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Otomatik Yükleme:</span>
                          <span>{selectedChannel.auto_upload ? 'Aktif' : 'Pasif'}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Günlük Hedef:</span>
                          <span>{selectedChannel.daily_upload_target} video</span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold mb-4">Performans</h3>
                      <div className="space-y-3">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Aboneler:</span>
                          <span>{formatNumber(selectedChannel.subscribers)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Toplam İzlenme:</span>
                          <span>{formatNumber(selectedChannel.total_views)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Etkileşim Oranı:</span>
                          <span>{selectedChannel.engagement_rate}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Aylık Gelir:</span>
                          <span>${formatNumber(selectedChannel.monthly_revenue)}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'analytics' && (
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Detaylı Analitik</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="bg-gray-700 rounded-lg p-4">
                        <BarChart3 className="w-8 h-8 text-blue-400 mb-2" />
                        <p className="text-gray-400 text-sm">İzlenme Trendi</p>
                        <p className="text-xl font-bold">+12.5%</p>
                      </div>
                      <div className="bg-gray-700 rounded-lg p-4">
                        <TrendingUp className="w-8 h-8 text-green-400 mb-2" />
                        <p className="text-gray-400 text-sm">Abone Artışı</p>
                        <p className="text-xl font-bold">+2,341</p>
                      </div>
                      <div className="bg-gray-700 rounded-lg p-4">
                        <Activity className="w-8 h-8 text-purple-400 mb-2" />
                        <p className="text-gray-400 text-sm">Etkileşim</p>
                        <p className="text-xl font-bold">8.7%</p>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'settings' && (
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Kanal Ayarları</h3>
                    <div className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium mb-2" htmlFor="api_key">API Anahtarı</label>
                        <div className="flex items-center space-x-2">
                          <Key className="w-4 h-4 text-gray-400" />
                          <input
                            id="api_key"
                            type="password"
                            value={selectedChannel.api_key || ''}
                            className="flex-1 bg-gray-700 border border-gray-600 rounded px-3 py-2"
                            placeholder="YouTube API Anahtarı"
                            title="YouTube API Anahtarı"
                          />
                        </div>
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2" htmlFor="daily_upload_target">Günlük Yükleme Hedefi</label>
                        <input
                          id="daily_upload_target"
                          type="number"
                          value={selectedChannel.daily_upload_target}
                          className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2"
                          title="Günlük video yükleme hedefi"
                          placeholder="3"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-2" htmlFor="target_views_per_video">Hedef İzlenme/Video</label>
                        <input
                          id="target_views_per_video"
                          type="number"
                          value={selectedChannel.target_views_per_video}
                          className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2"
                          title="Video başına hedef izlenme sayısı"
                          placeholder="10000"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'logs' && (
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Son Aktiviteler</h3>
                    <div className="space-y-3">
                      {selectedChannel.recent_activities?.map((activity) => (
                        <div key={activity.id} className="bg-gray-700 rounded-lg p-4">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              {activity.type === 'upload' && <Upload className="w-4 h-4 text-blue-400" />}
                              {activity.type === 'sync' && <Activity className="w-4 h-4 text-green-400" />}
                              {activity.type === 'error' && <AlertTriangle className="w-4 h-4 text-red-400" />}
                              {activity.type === 'success' && <CheckCircle className="w-4 h-4 text-green-400" />}
                              <div>
                                <p className="font-medium">{activity.message}</p>
                                <p className="text-xs text-gray-400">{formatDate(activity.timestamp)}</p>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Modal Footer */}
              <div className="flex justify-end space-x-3 mt-6 pt-4 border-t border-gray-700">
                <button
                  onClick={() => setShowEditModal(true)}
                  className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors"
                  title="Kanal bilgilerini düzenle"
                  aria-label="Kanal düzenleme"
                >
                  Düzenle
                </button>
                <button
                  onClick={() => setSelectedChannel(null)}
                  className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded-lg transition-colors"
                  title="Modalı kapat"
                  aria-label="Modal kapatma"
                >
                  Kapat
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChannelsPage;
