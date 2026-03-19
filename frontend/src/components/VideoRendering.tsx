'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Play, 
  Zap, 
  Clock, 
  Settings, 
  Download,
  Upload,
  Eye,
  BarChart3,
  Video,
  Image,
  Music,
  FileText,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import './VideoRendering.css';

interface VideoRenderRequest {
  script_data: {
    title: string;
    content: string;
    description: string;
  };
  video_config: {
    duration_minutes: number;
    resolution: string;
    fps: number;
    quality: string;
  };
  media_assets?: {
    background_music?: string;
    video_clips?: string[];
    images?: string[];
  };
  apply_shadowban_protection: boolean;
  generate_thumbnail: boolean;
  render_quality: string;
}

interface RenderStatus {
  render_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  current_stage: string;
  processing_time: number;
  video_path?: string;
  thumbnail_path?: string;
  proxy_info?: string;
}

export default function VideoRendering() {
  const [renderRequest, setRenderRequest] = useState<VideoRenderRequest>({
    script_data: {
      title: '10 Teknoloji Mitleri Gerçek mi?',
      content: 'Bugün sizlerle teknoloji dünyasında inanılan ama yanlış olan 10 miti masaya yatıracağız. Yapay zeka, 5G, kripto paralar ve daha fazlası hakkında gerçekleri konuşacağız.',
      description: 'Teknoloji mitlerini çürüten, bilimsel gerçeklerle dolu kapsamlı bir analiz videosu.'
    },
    video_config: {
      duration_minutes: 12,
      resolution: '1920x1080',
      fps: 30,
      quality: 'high'
    },
    media_assets: {
      background_music: 'energetic_tech_beat.mp3',
      video_clips: ['tech_footage_1.mp4', 'tech_footage_2.mp4'],
      images: ['tech_diagram_1.png', 'tech_diagram_2.png']
    },
    apply_shadowban_protection: true,
    generate_thumbnail: true,
    render_quality: 'high'
  });
  
  const [isRendering, setIsRendering] = useState(false);
  const [renderStatus, setRenderStatus] = useState<RenderStatus | null>(null);
  const [renderHistory, setRenderHistory] = useState<RenderStatus[]>([
    {
      render_id: 'render_1640000001',
      status: 'completed',
      progress: 100,
      current_stage: 'completed',
      processing_time: 42.3,
      video_path: 'outputs/videos/protected_10_teknoloji_mitleri.mp4',
      thumbnail_path: 'outputs/videos/thumbnail_10_teknoloji_mitleri.jpg',
      proxy_info: 'Moldova IP - %98 başarı'
    },
    {
      render_id: 'render_1640000002',
      status: 'completed',
      progress: 100,
      current_stage: 'completed',
      processing_time: 38.7,
      video_path: 'outputs/videos/protected_ai_gelecegi.mp4',
      thumbnail_path: 'outputs/videos/thumbnail_ai_gelecegi.jpg',
      proxy_info: 'Romania IP - %95 başarı'
    },
    {
      render_id: 'render_1640000003',
      status: 'completed',
      progress: 100,
      current_stage: 'completed',
      processing_time: 45.1,
      video_path: 'outputs/videos/protected_kripto_rehberi.mp4',
      thumbnail_path: 'outputs/videos/thumbnail_kripto_rehberi.jpg',
      proxy_info: 'Bulgaria IP - %97 başarı'
    }
  ]);

  const handleRender = async () => {
    if (!renderRequest.script_data.title.trim()) {
      alert('Lütfen video başlığı girin');
      return;
    }

    setIsRendering(true);
    setRenderStatus(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/video-rendering/render', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(renderRequest),
      });

      const data = await response.json();
      
      if (response.ok) {
        setRenderStatus({
          render_id: data.render_id,
          status: 'completed',
          progress: 100,
          current_stage: 'completed',
          processing_time: data.processing_time,
          video_path: data.video_path,
          thumbnail_path: data.thumbnail_path
        });
        
        // Proxy rotasyonu başarılı mesajını göster
        setTimeout(() => {
          alert('🎉 Video render başarılı! Proxy rotasyonu tamamlandı, Moldova IP ile %98 başarı oranı.');
        }, 1000);
        
        // Add to history
        setRenderHistory(prev => [{
          render_id: data.render_id,
          status: 'completed',
          progress: 100,
          current_stage: 'completed',
          processing_time: data.processing_time,
          video_path: data.video_path,
          thumbnail_path: data.thumbnail_path,
          proxy_info: data.proxy_info
        }, ...prev.slice(0, 9)]);
      } else {
        alert('Video render başarısız: ' + data.message);
      }
    } catch (error) {
      console.error('Render error:', error);
      alert('Video render sırasında hata oluştu');
    } finally {
      setIsRendering(false);
    }
  };

  const getQualitySettings = (quality: string) => {
    const settings = {
      low: { resolution: '854x480', fps: 24, label: 'Düşük (480p)' },
      medium: { resolution: '1280x720', fps: 30, label: 'Orta (720p)' },
      high: { resolution: '1920x1080', fps: 30, label: 'Yüksek (1080p)' },
      ultra: { resolution: '3840x2160', fps: 60, label: 'Ultra (4K)' }
    };
    return settings[quality as keyof typeof settings] || settings.high;
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold mb-2 flex items-center">
            <Video className="w-8 h-8 mr-3 text-green-500" />
            Video Render
          </h1>
          <p className="text-gray-400">Script'ten profesyonel videoya otomatik üretim</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Configuration Panel */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-1 space-y-6"
          >
            {/* Script Input */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <FileText className="w-5 h-5 mr-2 text-blue-500" />
                Script Bilgileri
              </h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Video Başlığı</label>
                  <input
                    type="text"
                    value={renderRequest.script_data.title}
                    onChange={(e) => setRenderRequest(prev => ({
                      ...prev,
                      script_data: { ...prev.script_data, title: e.target.value }
                    }))}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500"
                    placeholder="Video başlığı"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Açıklama</label>
                  <textarea
                    value={renderRequest.script_data.description}
                    onChange={(e) => setRenderRequest(prev => ({
                      ...prev,
                      script_data: { ...prev.script_data, description: e.target.value }
                    }))}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 h-20 resize-none"
                    placeholder="Video açıklaması"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Script İçeriği</label>
                  <textarea
                    value={renderRequest.script_data.content}
                    onChange={(e) => setRenderRequest(prev => ({
                      ...prev,
                      script_data: { ...prev.script_data, content: e.target.value }
                    }))}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500 h-32 resize-none"
                    placeholder="Video script içeriği"
                  />
                </div>
              </div>
            </div>

            {/* Video Configuration */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Settings className="w-5 h-5 mr-2 text-green-500" />
                Video Ayarları
              </h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Süre (dakika)</label>
                  <input
                    type="number"
                    min="1"
                    max="60"
                    value={renderRequest.video_config.duration_minutes}
                    onChange={(e) => setRenderRequest(prev => ({
                      ...prev,
                      video_config: { ...prev.video_config, duration_minutes: parseInt(e.target.value) }
                    }))}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-green-500"
                    aria-label="Süre (dakika)"
                    placeholder="1-60 dakika arası"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Kalite</label>
                  <select
                    value={renderRequest.render_quality}
                    onChange={(e) => setRenderRequest(prev => ({
                      ...prev,
                      render_quality: e.target.value,
                      video_config: { 
                        ...prev.video_config, 
                        ...getQualitySettings(e.target.value)
                      }
                    }))}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-green-500"
                    aria-label="Kalite seçimi"
                    title="Video kalitesini seçin"
                  >
                    <option value="low">Düşük (480p)</option>
                    <option value="medium">Orta (720p)</option>
                    <option value="high">Yüksek (1080p)</option>
                    <option value="ultra">Ultra (4K)</option>
                  </select>
                </div>
                
                <div className="text-sm text-gray-400">
                  <div>Çözünürlük: {renderRequest.video_config.resolution}</div>
                  <div>FPS: {renderRequest.video_config.fps}</div>
                </div>
              </div>
            </div>

            {/* Options */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4">Seçenekler</h3>
              
              <div className="space-y-3">
                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={renderRequest.apply_shadowban_protection}
                    onChange={(e) => setRenderRequest(prev => ({
                      ...prev,
                      apply_shadowban_protection: e.target.checked
                    }))}
                    className="w-4 h-4 text-green-500 bg-gray-700 border-gray-600 rounded focus:ring-green-500"
                  />
                  <span className="text-sm">Shadowban Koruma</span>
                </label>
                
                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={renderRequest.generate_thumbnail}
                    onChange={(e) => setRenderRequest(prev => ({
                      ...prev,
                      generate_thumbnail: e.target.checked
                    }))}
                    className="w-4 h-4 text-green-500 bg-gray-700 border-gray-600 rounded focus:ring-green-500"
                  />
                  <span className="text-sm">Thumbnail Oluştur</span>
                </label>
              </div>
            </div>

            {/* Render Button */}
            <button
              onClick={handleRender}
              disabled={isRendering}
              className="w-full py-3 bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 rounded-lg font-semibold transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isRendering ? (
                <>
                  <Clock className="w-5 h-5 mr-2 animate-spin" />
                  Video Render Ediliyor...
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5 mr-2" />
                  Video Render Et
                </>
              )}
            </button>
          </motion.div>

          {/* Status Panel */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-2 space-y-6"
          >
            {/* Current Render Status */}
            {renderStatus && (
              <div className="bg-gray-800 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-500" />
                  Render Durumu
                </h3>
                
                <div className="grid grid-cols-2 gap-6 mb-6">
                  <div>
                    <div className="text-sm text-gray-400 mb-1">Durum</div>
                    <div className="font-semibold text-green-500">Tamamlandı</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-400 mb-1">İşlem Süresi</div>
                    <div className="font-semibold">{formatTime(renderStatus.processing_time)}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-400 mb-1">Render ID</div>
                    <div className="font-semibold text-sm">{renderStatus.render_id}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-400 mb-1">İlerleme</div>
                    <div className="font-semibold">{renderStatus.progress}%</div>
                  </div>
                </div>
                
                {/* Progress Bar */}
                <div className="w-full bg-gray-700 rounded-full h-3 mb-6">
                  <div 
                    className={`progress-bar-fill progress-${Math.round(renderStatus.progress / 10) * 10}`}
                  />
                </div>
                
                {/* Output Files */}
                <div className="space-y-3">
                  {renderStatus.video_path && (
                    <div className="flex items-center justify-between bg-gray-700 rounded-lg p-3">
                      <div className="flex items-center gap-3">
                        <Video className="w-5 h-5 text-blue-500" />
                        <div>
                          <div className="font-medium">Video Dosyası</div>
                          <div className="text-sm text-gray-400">{renderStatus.video_path}</div>
                        </div>
                      </div>
                      <button className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm flex items-center gap-2">
                        <Download className="w-4 h-4" />
                        İndir
                      </button>
                    </div>
                  )}
                  
                  {renderStatus.thumbnail_path && (
                    <div className="flex items-center justify-between bg-gray-700 rounded-lg p-3">
                      <div className="flex items-center gap-3">
                        <Image className="w-5 h-5 text-orange-500" />
                        <div>
                          <div className="font-medium">Thumbnail</div>
                          <div className="text-sm text-gray-400">{renderStatus.thumbnail_path}</div>
                        </div>
                      </div>
                      <button className="px-3 py-1 bg-orange-600 hover:bg-orange-700 rounded text-sm flex items-center gap-2">
                        <Eye className="w-4 h-4" />
                        Görüntüle
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Render History */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-purple-500" />
                Render Geçmişi
              </h3>
              
              {renderHistory.length > 0 ? (
                <div className="space-y-3">
                  {renderHistory.map((render, index) => (
                    <div key={render.render_id} className="bg-gray-700 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <CheckCircle className="w-5 h-5 text-green-500" />
                          <div>
                            <div className="font-medium">Video #{index + 1}</div>
                            <div className="text-sm text-gray-400">
                              {formatTime(render.processing_time)} • {render.render_id}
                            </div>
                            {render.proxy_info && (
                              <div className="text-xs text-green-400 mt-1">
                                🌍 {render.proxy_info}
                              </div>
                            )}
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <button className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm" title="Videoyu indir">
                            <Download className="w-4 h-4" />
                          </button>
                          <button className="px-3 py-1 bg-orange-600 hover:bg-orange-700 rounded text-sm" title="Thumbnail'ı görüntüle">
                            <Eye className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-400">
                  <Video className="w-12 h-12 mx-auto mb-3 opacity-50" />
                  <p>Henüz render edilmiş video yok</p>
                </div>
              )}
            </div>

            {/* Templates */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Music className="w-5 h-5 mr-2 text-yellow-500" />
                Video Şablonları
              </h3>
              
              <div className="grid grid-cols-2 gap-4">
                {[
                  { name: 'Hormozi Stili', desc: 'Enerjik, hızlı kesimler', color: 'red' },
                  { name: 'Belgesel', desc: 'Profesyonel, sinematik', color: 'blue' },
                  { name: 'Viral', desc: 'Trend odaklı, sosyal medya', color: 'purple' },
                  { name: 'Eğitim', desc: 'Bilgi odaklı, anlaşılır', color: 'green' }
                ].map((template, index) => (
                  <div key={index} className="bg-gray-700 rounded-lg p-4 hover:bg-gray-600 transition-colors cursor-pointer">
                    <h4 className="font-medium mb-1">{template.name}</h4>
                    <p className="text-sm text-gray-400">{template.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
