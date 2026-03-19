'use client';

import { useState, useEffect } from 'react';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  AlertCircle, 
  CheckCircle, 
  Download, 
  Upload, 
  Trash2, 
  Edit, 
  Eye, 
  Play, 
  Pause,
  RotateCcw,
  XCircle,
  Info,
  Zap,
  Shield,
  Activity,
  FileText,
  Video,
  Image,
  Music
} from 'lucide-react';

interface SystemError {
  id: string;
  timestamp: string;
  level: 'error' | 'warning' | 'info';
  component: string;
  message: string;
  stack?: string;
  resolved: boolean;
}

interface ProcessStatus {
  id: string;
  name: string;
  status: 'idle' | 'running' | 'completed' | 'failed';
  progress: number;
  startTime?: string;
  endTime?: string;
  type: 'render' | 'upload' | 'analysis' | 'script';
  details?: string;
}

interface MediaFile {
  id: string;
  name: string;
  type: 'video' | 'image' | 'audio' | 'document';
  size: number;
  url: string;
  thumbnail?: string;
  duration?: number;
  created_at: string;
  tags: string[];
}

export default function SystemMonitor() {
  const [errors, setErrors] = useState<SystemError[]>([
    {
      id: 'err_001',
      timestamp: new Date().toISOString(),
      level: 'error',
      component: 'VideoRendering',
      message: 'FFmpeg process timeout after 30 seconds',
      stack: 'VideoRenderingService.render_video() -> FFmpeg.execute()',
      resolved: false
    },
    {
      id: 'err_002',
      timestamp: new Date(Date.now() - 300000).toISOString(),
      level: 'warning',
      component: 'AI Script Generator',
      message: 'Gemini API rate limit approaching',
      resolved: false
    },
    {
      id: 'err_003',
      timestamp: new Date(Date.now() - 600000).toISOString(),
      level: 'info',
      component: 'Proxy Manager',
      message: 'Proxy rotation completed successfully',
      resolved: true
    }
  ]);

  const [processes, setProcesses] = useState<ProcessStatus[]>([
    {
      id: 'proc_001',
      name: '10 Teknoloji Mitleri Render',
      status: 'running',
      progress: 67,
      startTime: new Date(Date.now() - 120000).toISOString(),
      type: 'render',
      details: 'Applying shadowban protection...'
    },
    {
      id: 'proc_002',
      name: 'Kanal Analizi - TechReview',
      status: 'completed',
      progress: 100,
      startTime: new Date(Date.now() - 600000).toISOString(),
      endTime: new Date(Date.now() - 180000).toISOString(),
      type: 'analysis'
    },
    {
      id: 'proc_003',
      name: 'AI Senaryo - Kripto Güncellemeleri',
      status: 'failed',
      progress: 45,
      startTime: new Date(Date.now() - 900000).toISOString(),
      endTime: new Date(Date.now() - 600000).toISOString(),
      type: 'script',
      details: 'API quota exceeded'
    },
    {
      id: 'proc_004',
      name: 'Ghost Cloak Application',
      status: 'running',
      progress: 82,
      startTime: new Date(Date.now() - 300000).toISOString(),
      type: 'render',
      details: 'Applying stealth 4.0 protection...'
    },
    {
      id: 'proc_005',
      name: 'Multi-Verse Upload',
      status: 'running',
      progress: 34,
      startTime: new Date(Date.now() - 180000).toISOString(),
      type: 'upload',
      details: 'Uploading to YouTube, TikTok, Instagram...'
    }
  ]);

  const [mediaFiles, setMediaFiles] = useState<MediaFile[]>([
    {
      id: 'media_001',
      name: 'protected_10_teknoloji_mitleri.mp4',
      type: 'video',
      size: 125829120,
      url: 'outputs/videos/protected_10_teknoloji_mitleri.mp4',
      thumbnail: 'outputs/videos/thumbnail_10_teknoloji_mitleri.jpg',
      duration: 720,
      created_at: new Date(Date.now() - 3600000).toISOString(),
      tags: ['teknoloji', 'mitler', 'protected']
    },
    {
      id: 'media_002',
      name: 'thumbnail_ai_gelecegi.jpg',
      type: 'image',
      size: 524288,
      url: 'outputs/videos/thumbnail_ai_gelecegi.jpg',
      created_at: new Date(Date.now() - 7200000).toISOString(),
      tags: ['ai', 'gelecek', 'thumbnail']
    },
    {
      id: 'media_003',
      name: 'energetic_tech_beat.mp3',
      type: 'audio',
      size: 4194304,
      url: 'assets/music/energetic_tech_beat.mp3',
      duration: 180,
      created_at: new Date(Date.now() - 10800000).toISOString(),
      tags: ['music', 'tech', 'energetic']
    }
  ]);

  const [selectedFiles, setSelectedFiles] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState<'errors' | 'processes' | 'media' | 'empire' | 'omniverse'>('errors');

  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate real-time updates
      setProcesses(prev => prev.map(process => {
        if (process.status === 'running' && process.progress < 100) {
          return {
            ...process,
            progress: Math.min(process.progress + Math.random() * 10, 100),
            status: process.progress >= 95 ? 'completed' : 'running'
          };
        }
        return process;
      }));
    }, 2000);

    // Fetch Empire status
    const fetchEmpireStatus = async () => {
      try {
        const response = await fetch('/api/empire/status');
        if (response.ok) {
          const data = await response.json();
          console.log('Empire Status:', data);
        }
      } catch (error) {
        console.error('Empire status fetch error:', error);
      }
    };

    // Fetch Omniverse status
    const fetchOmniverseStatus = async () => {
      try {
        const response = await fetch('/api/omniverse/status');
        if (response.ok) {
          const data = await response.json();
          console.log('Omniverse Status:', data);
        }
      } catch (error) {
        console.error('Omniverse status fetch error:', error);
      }
    };

    fetchEmpireStatus();
    fetchOmniverseStatus();

    return () => clearInterval(interval);
  }, []);

  const getErrorIcon = (level: string) => {
    switch (level) {
      case 'error': return <XCircle className="w-4 h-4 text-red-500" />;
      case 'warning': return <AlertCircle className="w-4 h-4 text-yellow-500" />;
      case 'info': return <Info className="w-4 h-4 text-blue-500" />;
      default: return <AlertCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  const getProcessIcon = (type: string) => {
    switch (type) {
      case 'render': return <Video className="w-4 h-4" />;
      case 'upload': return <Upload className="w-4 h-4" />;
      case 'analysis': return <Activity className="w-4 h-4" />;
      case 'script': return <FileText className="w-4 h-4" />;
      default: return <Zap className="w-4 h-4" />;
    }
  };

  const getMediaIcon = (type: string) => {
    switch (type) {
      case 'video': return <Video className="w-4 h-4" />;
      case 'image': return <Image className="w-4 h-4" />;
      case 'audio': return <Music className="w-4 h-4" />;
      case 'document': return <FileText className="w-4 h-4" />;
      default: return <FileText className="w-4 h-4" />;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return hours > 0 ? `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}` : `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  const resolveError = (errorId: string) => {
    setErrors(prev => prev.map(error => 
      error.id === errorId ? { ...error, resolved: true } : error
    ));
  };

  const deleteError = (errorId: string) => {
    setErrors(prev => prev.filter(error => error.id !== errorId));
  };

  const toggleFileSelection = (fileId: string) => {
    setSelectedFiles(prev => 
      prev.includes(fileId) 
        ? prev.filter(id => id !== fileId)
        : [...prev, fileId]
    );
  };

  const downloadSelected = () => {
    alert(`Seçili ${selectedFiles.length} dosya indiriliyor...`);
    setSelectedFiles([]);
  };

  const deleteSelected = () => {
    if (confirm(`Seçili ${selectedFiles.length} dosyayı silmek istediğinizden emin misiniz?`)) {
      setMediaFiles(prev => prev.filter(file => !selectedFiles.includes(file.id)));
      setSelectedFiles([]);
    }
  };

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'bg-green-500';
    if (progress >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2 flex items-center gap-3">
            <Shield className="w-8 h-8 text-blue-500" />
            Sistem İzleme Paneli
          </h1>
          <p className="text-gray-400">VUC-2026 Ultimate Dev++ - Tam Sistem Kontrolü</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Aktif Hatalar</p>
                  <p className="text-2xl font-bold text-red-500">
                    {errors.filter(e => !e.resolved).length}
                  </p>
                </div>
                <XCircle className="w-8 h-8 text-red-500 opacity-50" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Çalışan İşlemler</p>
                  <p className="text-2xl font-bold text-green-500">
                    {processes.filter(p => p.status === 'running').length}
                  </p>
                </div>
                <Activity className="w-8 h-8 text-green-500 opacity-50" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Toplam Medya</p>
                  <p className="text-2xl font-bold text-blue-500">
                    {mediaFiles.length}
                  </p>
                </div>
                <Video className="w-8 h-8 text-blue-500 opacity-50" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Sistem Sağlığı</p>
                  <p className="text-2xl font-bold text-green-500">98%</p>
                </div>
                <CheckCircle className="w-8 h-8 text-green-500 opacity-50" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-700 mb-6">
          <div className="flex space-x-8">
            {[
              { id: 'errors', label: 'Hata Bildirimleri', icon: AlertCircle },
              { id: 'processes', label: 'İşlemler', icon: Activity },
              { id: 'media', label: 'Medya Dosyaları', icon: Video },
              { id: 'empire', label: 'İmparatorluk', icon: Shield },
              { id: 'omniverse', label: 'Multi-Verse', icon: Zap }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 pb-3 border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-500'
                    : 'border-transparent text-gray-400 hover:text-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                {tab.label}
                {tab.id === 'errors' && (
                  <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                    {errors.filter(e => !e.resolved).length}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        <div className="space-y-4">
          {/* Errors Tab */}
          {activeTab === 'errors' && (
            <div className="space-y-3">
              {errors.map(error => (
                <Card key={error.id} className={`bg-gray-800 border-gray-700 ${error.resolved ? 'opacity-50' : ''}`}>
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-3 flex-1">
                        {getErrorIcon(error.level)}
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-medium">{error.component}</span>
                            <span className="text-xs text-gray-400">
                              {new Date(error.timestamp).toLocaleString('tr-TR')}
                            </span>
                            {error.resolved && (
                              <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">
                                Çözüldü
                              </span>
                            )}
                          </div>
                          <p className="text-gray-300 text-sm">{error.message}</p>
                          {error.stack && (
                            <details className="mt-2">
                              <summary className="text-xs text-gray-500 cursor-pointer">Stack Trace</summary>
                              <pre className="text-xs text-gray-600 mt-1 bg-gray-900 p-2 rounded overflow-x-auto">
                                {error.stack}
                              </pre>
                            </details>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {!error.resolved && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => resolveError(error.id)}
                            className="border-green-500 text-green-500 hover:bg-green-500/10"
                          >
                            <CheckCircle className="w-4 h-4 mr-1" />
                            Çöz
                          </Button>
                        )}
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => deleteError(error.id)}
                          className="border-red-500 text-red-500 hover:bg-red-500/10"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* Processes Tab */}
          {activeTab === 'processes' && (
            <div className="space-y-3">
              {processes.map(process => (
                <Card key={process.id} className="bg-gray-800 border-gray-700">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        {getProcessIcon(process.type)}
                        <div>
                          <h3 className="font-medium">{process.name}</h3>
                          <p className="text-sm text-gray-400">{process.details}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-1 rounded text-xs ${
                          process.status === 'running' ? 'bg-blue-500/20 text-blue-400' :
                          process.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                          process.status === 'failed' ? 'bg-red-500/20 text-red-400' :
                          'bg-gray-500/20 text-gray-400'
                        }`}>
                          {process.status === 'running' ? 'Çalışıyor' :
                           process.status === 'completed' ? 'Tamamlandı' :
                           process.status === 'failed' ? 'Başarısız' : 'Beklemede'}
                        </span>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span>İşlem Yüzdesi</span>
                        <span>{Math.round(process.progress)}%</span>
                      </div>
                      <Progress value={process.progress} className="h-2" />
                      <div className="flex items-center justify-between text-xs text-gray-400">
                        <span>
                          Başlangıç: {process.startTime ? new Date(process.startTime).toLocaleTimeString('tr-TR') : '-'}
                        </span>
                        {process.endTime && (
                          <span>
                            Bitiş: {new Date(process.endTime).toLocaleTimeString('tr-TR')}
                          </span>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* Media Tab */}
          {activeTab === 'media' && (
            <div>
              {/* Action Bar */}
              <div className="flex items-center justify-between mb-4 p-4 bg-gray-800 rounded-lg">
                <div className="flex items-center gap-4">
                  <span className="text-sm text-gray-400">
                    {selectedFiles.length} dosya seçildi
                  </span>
                  {selectedFiles.length > 0 && (
                    <>
                      <Button
                        size="sm"
                        onClick={downloadSelected}
                        className="bg-blue-600 hover:bg-blue-700"
                      >
                        <Download className="w-4 h-4 mr-1" />
                        İndir
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={deleteSelected}
                        className="border-red-500 text-red-500 hover:bg-red-500/10"
                      >
                        <Trash2 className="w-4 h-4 mr-1" />
                        Sil
                      </Button>
                    </>
                  )}
                </div>
                <Button size="sm" className="bg-green-600 hover:bg-green-700">
                  <Upload className="w-4 h-4 mr-1" />
                  Yükle
                </Button>
              </div>

              {/* Media Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {mediaFiles.map(file => (
                  <Card key={file.id} className="bg-gray-800 border-gray-700">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <input
                            type="checkbox"
                            checked={selectedFiles.includes(file.id)}
                            onChange={() => toggleFileSelection(file.id)}
                            className="rounded border-gray-600 bg-gray-700 text-blue-500 focus:ring-blue-500"
                            aria-label={`Dosya seç: ${file.name}`}
                          />
                          {getMediaIcon(file.type)}
                          <div className="flex-1 min-w-0">
                            <h3 className="font-medium truncate">{file.name}</h3>
                            <p className="text-sm text-gray-400">
                              {formatFileSize(file.size)}
                              {file.duration && ` • ${formatDuration(file.duration)}`}
                            </p>
                          </div>
                        </div>
                      </div>

                      {file.thumbnail && (
                        <div className="mb-3 rounded-lg overflow-hidden bg-gray-700">
                          <img
                            src={file.thumbnail}
                            alt={file.name}
                            className="w-full h-32 object-cover"
                          />
                        </div>
                      )}

                      <div className="flex flex-wrap gap-1 mb-3">
                        {file.tags.map(tag => (
                          <span
                            key={tag}
                            className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>

                      <div className="flex items-center justify-between text-xs text-gray-400">
                        <span>{new Date(file.created_at).toLocaleDateString('tr-TR')}</span>
                        <div className="flex items-center gap-2">
                          <Button size="sm" variant="ghost">
                            <Eye className="w-3 h-3" />
                          </Button>
                          <Button size="sm" variant="ghost">
                            <Edit className="w-3 h-3" />
                          </Button>
                          <Button size="sm" variant="ghost">
                            <Download className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        {/* Empire Tab */}
          {activeTab === 'empire' && (
            <div className="space-y-4">
              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="p-6">
                  <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Shield className="w-6 h-6 text-blue-500" />
                    İmparatorluk Durumu
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div className="bg-gray-700 rounded-lg p-4">
                      <div className="text-2xl font-bold text-green-500">98.5%</div>
                      <div className="text-sm text-gray-400">İmparatorluk Sağlığı</div>
                    </div>
                    <div className="bg-gray-700 rounded-lg p-4">
                      <div className="text-2xl font-bold text-blue-500">12</div>
                      <div className="text-sm text-gray-400">Aktif Kanallar</div>
                    </div>
                    <div className="bg-gray-700 rounded-lg p-4">
                      <div className="text-2xl font-bold text-purple-500">847</div>
                      <div className="text-sm text-gray-400">Toplam Videolar</div>
                    </div>
                    <div className="bg-gray-700 rounded-lg p-4">
                      <div className="text-2xl font-bold text-yellow-500">125K</div>
                      <div className="text-sm text-gray-400">Günlük İzlenme</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold mb-4">Agent Durumları</h3>
                  <div className="space-y-3">
                    {[
                      { name: 'Script Agent', status: 'active', tasks: 23 },
                      { name: 'Media Agent', status: 'active', tasks: 18 },
                      { name: 'SEO Agent', status: 'idle', tasks: 0 },
                      { name: 'Upload Agent', status: 'active', tasks: 7 },
                      { name: 'Spy Agent', status: 'active', tasks: 12 }
                    ].map((agent, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className={`w-2 h-2 rounded-full ${
                            agent.status === 'active' ? 'bg-green-500' : 'bg-gray-500'
                          }`} />
                          <span>{agent.name}</span>
                        </div>
                        <div className="text-sm text-gray-400">
                          {agent.tasks} aktif görev
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Omniverse Tab */}
          {activeTab === 'omniverse' && (
            <div className="space-y-4">
              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="p-6">
                  <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Zap className="w-6 h-6 text-purple-500" />
                    Multi-Verse Operasyonları
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div className="bg-gray-700 rounded-lg p-4">
                      <div className="text-lg font-semibold text-purple-400 mb-2">Ghost Cloak</div>
                      <div className="text-sm text-gray-400">Stealth 4.0 Aktif</div>
                      <div className="mt-2 text-xs text-green-400">✓ 89 tehdit engellendi</div>
                    </div>
                    <div className="bg-gray-700 rounded-lg p-4">
                      <div className="text-lg font-semibold text-blue-400 mb-2">AI Cutter</div>
                      <div className="text-sm text-gray-400">Otomatik Kesim</div>
                      <div className="mt-2 text-xs text-green-400">✓ 156 video işlendi</div>
                    </div>
                    <div className="bg-gray-700 rounded-lg p-4">
                      <div className="text-lg font-semibold text-yellow-400 mb-2">Multi-Verse</div>
                      <div className="text-sm text-gray-400">Platform Adaptasyonu</div>
                      <div className="mt-2 text-xs text-green-400">✓ 5 platform aktif</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold mb-4">Platform Yüklemeleri</h3>
                  <div className="space-y-3">
                    {[
                      { platform: 'YouTube', status: 'active', uploads: 234, success_rate: 98.7 },
                      { platform: 'TikTok', status: 'active', uploads: 189, success_rate: 95.3 },
                      { platform: 'Instagram', status: 'active', uploads: 156, success_rate: 97.1 },
                      { platform: 'Twitter', status: 'idle', uploads: 89, success_rate: 92.4 }
                    ].map((platform, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className={`w-2 h-2 rounded-full ${
                            platform.status === 'active' ? 'bg-green-500' : 'bg-gray-500'
                          }`} />
                          <span>{platform.platform}</span>
                        </div>
                        <div className="flex items-center gap-4 text-sm">
                          <span className="text-gray-400">{platform.uploads} yüklemeler</span>
                          <span className="text-green-400">%{platform.success_rate} başarı</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
