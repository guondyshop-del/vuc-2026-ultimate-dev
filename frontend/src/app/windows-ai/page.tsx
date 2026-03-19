'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Cpu, 
  Zap, 
  Image, 
  Video, 
  Mic, 
  Brain,
  Monitor,
  Settings,
  Activity,
  CheckCircle,
  AlertCircle,
  Download
} from 'lucide-react';

interface WindowsAIStatus {
  available: boolean;
  services: {
    ocr: boolean;
    speech: boolean;
    image_analysis: boolean;
    video_enhancement: boolean;
    phi3: boolean;
    directml: boolean;
  };
  device_info: {
    provider: string;
    device_type: string;
    capabilities: string[];
    memory_info: Record<string, string>;
  };
  performance_metrics: Record<string, any>;
}

interface AIModel {
  name: string;
  type: string;
  status: 'loaded' | 'available' | 'downloading' | 'error';
  size: string;
  description: string;
}

export default function WindowsAIPage() {
  const [activeTab, setActiveTab] = useState<'status' | 'models' | 'performance'>('status');
  const [windowsAIStatus, setWindowsAIStatus] = useState<WindowsAIStatus | null>(null);
  const [availableModels, setAvailableModels] = useState<AIModel[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWindowsAIStatus();
  }, []);

  const fetchWindowsAIStatus = async () => {
    try {
      const response = await fetch('/api/windows-ai/status');
      if (response.ok) {
        const data = await response.json();
        setWindowsAIStatus(data);
      }

      // Modelleri çek
      const modelsResponse = await fetch('/api/windows-ai/models');
      if (modelsResponse.ok) {
        const models = await modelsResponse.json();
        setAvailableModels(models);
      }
    } catch (error) {
      console.error('Windows AI durumu çekilemedi:', error);
    } finally {
      setLoading(false);
    }
  };

  const downloadModel = async (modelName: string) => {
    try {
      const response = await fetch(`/api/windows-ai/models/${modelName}/download`, {
        method: 'POST'
      });
      
      if (response.ok) {
        // Model listesini güncelle
        fetchWindowsAIStatus();
      }
    } catch (error) {
      console.error('Model indirme hatası:', error);
    }
  };

  const getStatusColor = (status: boolean) => {
    return status ? 'text-green-400' : 'text-red-400';
  };

  const getStatusIcon = (status: boolean) => {
    return status ? (
      <CheckCircle className="w-5 h-5 text-green-400" />
    ) : (
      <AlertCircle className="w-5 h-5 text-red-400" />
    );
  };

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold mb-2">
            <span className="gradient-text">Windows AI Entegrasyonu</span>
          </h1>
          <p className="text-gray-400">
            Microsoft Foundry on Windows AI API'leri ve DirectML hızlandırma
          </p>
        </motion.div>

        {/* Tab Navigation */}
        <div className="flex space-x-4 mb-8 border-b border-gray-800">
          <button
            onClick={() => setActiveTab('status')}
            className={`pb-4 px-6 font-semibold transition-all duration-300 ${
              activeTab === 'status'
                ? 'text-amber-500 border-b-2 border-amber-500'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <Monitor className="w-5 h-5 inline mr-2" />
            Sistem Durumu
          </button>
          <button
            onClick={() => setActiveTab('models')}
            className={`pb-4 px-6 font-semibold transition-all duration-300 ${
              activeTab === 'models'
                ? 'text-amber-500 border-b-2 border-amber-500'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <Brain className="w-5 h-5 inline mr-2" />
            AI Modeller
          </button>
          <button
            onClick={() => setActiveTab('performance')}
            className={`pb-4 px-6 font-semibold transition-all duration-300 ${
              activeTab === 'performance'
                ? 'text-amber-500 border-b-2 border-amber-500'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <Activity className="w-5 h-5 inline mr-2" />
            Performans
          </button>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500"></div>
          </div>
        ) : (
          <>
            {/* Sistem Durumu Tab */}
            {activeTab === 'status' && windowsAIStatus && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-8"
              >
                {/* Genel Durum */}
                <div className="glass-effect rounded-xl p-6">
                  <h2 className="text-2xl font-bold mb-6 flex items-center">
                    <Cpu className="w-7 h-7 mr-3 text-amber-500" />
                    Windows AI Durumu
                  </h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                      <div className="flex items-center">
                        {getStatusIcon(windowsAIStatus.available)}
                        <span className="ml-3 font-semibold">Windows AI</span>
                      </div>
                      <span className={getStatusColor(windowsAIStatus.available)}>
                        {windowsAIStatus.available ? 'Aktif' : 'Pasif'}
                      </span>
                    </div>

                    <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                      <div className="flex items-center">
                        <Zap className="w-5 h-5 mr-3 text-purple-500" />
                        <span className="font-semibold">DirectML</span>
                      </div>
                      <span className={getStatusColor(windowsAIStatus.services.directml)}>
                        {windowsAIStatus.services.directml ? 'Aktif' : 'Pasif'}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Servisler */}
                <div className="glass-effect rounded-xl p-6">
                  <h2 className="text-2xl font-bold mb-6">AI Servisleri</h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div className="p-4 bg-gray-800/50 rounded-lg border border-gray-700">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center">
                          <Image className="w-5 h-5 mr-2 text-blue-500" />
                          <span className="font-semibold">OCR</span>
                        </div>
                        {getStatusIcon(windowsAIStatus.services.ocr)}
                      </div>
                      <p className="text-sm text-gray-400">
                        Görüntüden metin çıkarma
                      </p>
                    </div>

                    <div className="p-4 bg-gray-800/50 rounded-lg border border-gray-700">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center">
                          <Mic className="w-5 h-5 mr-2 text-green-500" />
                          <span className="font-semibold">Speech Recognition</span>
                        </div>
                        {getStatusIcon(windowsAIStatus.services.speech)}
                      </div>
                      <p className="text-sm text-gray-400">
                        Ses transkripsiyonu
                      </p>
                    </div>

                    <div className="p-4 bg-gray-800/50 rounded-lg border border-gray-700">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center">
                          <Brain className="w-5 h-5 mr-2 text-purple-500" />
                          <span className="font-semibold">Image Analysis</span>
                        </div>
                        {getStatusIcon(windowsAIStatus.services.image_analysis)}
                      </div>
                      <p className="text-sm text-gray-400">
                        Görüntü analizi ve açıklama
                      </p>
                    </div>

                    <div className="p-4 bg-gray-800/50 rounded-lg border border-gray-700">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center">
                          <Video className="w-5 h-5 mr-2 text-red-500" />
                          <span className="font-semibold">Video Enhancement</span>
                        </div>
                        {getStatusIcon(windowsAIStatus.services.video_enhancement)}
                      </div>
                      <p className="text-sm text-gray-400">
                        Video kalite artırma
                      </p>
                    </div>

                    <div className="p-4 bg-gray-800/50 rounded-lg border border-gray-700">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center">
                          <Settings className="w-5 h-5 mr-2 text-amber-500" />
                          <span className="font-semibold">Phi3 LLM</span>
                        </div>
                        {getStatusIcon(windowsAIStatus.services.phi3)}
                      </div>
                      <p className="text-sm text-gray-400">
                        Yerel dil modeli
                      </p>
                    </div>
                  </div>
                </div>

                {/* Cihaz Bilgileri */}
                <div className="glass-effect rounded-xl p-6">
                  <h2 className="text-2xl font-bold mb-6">Cihaz Bilgileri</h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="text-lg font-semibold mb-3 text-amber-400">Donanım</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Sağlayıcı:</span>
                          <span>{windowsAIStatus.device_info.provider}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Cihaz Tipi:</span>
                          <span>{windowsAIStatus.device_info.device_type}</span>
                        </div>
                      </div>
                    </div>

                    <div>
                      <h3 className="text-lg font-semibold mb-3 text-blue-400">Bellek</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Toplam:</span>
                          <span>{windowsAIStatus.device_info.memory_info.total_memory}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Mevcut:</span>
                          <span>{windowsAIStatus.device_info.memory_info.available_memory}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="mt-6">
                    <h3 className="text-lg font-semibold mb-3 text-green-400">Yetenekler</h3>
                    <div className="flex flex-wrap gap-2">
                      {windowsAIStatus.device_info.capabilities.map((capability, index) => (
                        <span key={index} className="px-3 py-1 bg-green-500/20 text-green-400 rounded-lg text-sm">
                          {capability}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {/* AI Modeller Tab */}
            {activeTab === 'models' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-6"
              >
                <div className="glass-effect rounded-xl p-6">
                  <h2 className="text-2xl font-bold mb-6">Mevcut AI Modeller</h2>
                  
                  {availableModels.length === 0 ? (
                    <div className="text-center py-12 text-gray-400">
                      Henüz yüklenmiş model bulunmuyor
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {availableModels.map((model, index) => (
                        <motion.div
                          key={model.name}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.1 }}
                          className="p-6 bg-gray-800/50 rounded-xl border border-gray-700"
                        >
                          <div className="flex items-center justify-between mb-4">
                            <h3 className="text-lg font-semibold">{model.name}</h3>
                            {getStatusIcon(model.status === 'loaded')}
                          </div>
                          
                          <div className="space-y-2 text-sm">
                            <div>
                              <span className="text-gray-400">Tip:</span>
                              <span className="ml-2">{model.type}</span>
                            </div>
                            <div>
                              <span className="text-gray-400">Boyut:</span>
                              <span className="ml-2">{model.size}</span>
                            </div>
                            <div>
                              <span className="text-gray-400">Durum:</span>
                              <span className={`ml-2 ${
                                model.status === 'loaded' ? 'text-green-400' : 
                                model.status === 'downloading' ? 'text-yellow-400' : 
                                'text-gray-400'
                              }`}>
                                {model.status === 'loaded' ? 'Yüklü' :
                                 model.status === 'downloading' ? 'İndiriliyor' :
                                 model.status === 'available' ? 'Mevcut' : 'Hata'}
                              </span>
                            </div>
                          </div>
                          
                          <p className="text-sm text-gray-400 mt-3">
                            {model.description}
                          </p>
                          
                          {model.status === 'available' && (
                            <button
                              onClick={() => downloadModel(model.name)}
                              className="mt-4 w-full py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-lg transition-colors flex items-center justify-center"
                            >
                              <Download className="w-4 h-4 mr-2" />
                              İndir
                            </button>
                          )}
                        </motion.div>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            )}

            {/* Performans Tab */}
            {activeTab === 'performance' && windowsAIStatus && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-6"
              >
                <div className="glass-effect rounded-xl p-6">
                  <h2 className="text-2xl font-bold mb-6">Performans Metrikleri</h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="p-4 bg-gray-800/50 rounded-lg">
                      <h3 className="text-lg font-semibold mb-3 text-blue-400">İşlem Hızı</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Görüntü Analizi:</span>
                          <span className="text-green-400">~2.3s</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">OCR:</span>
                          <span className="text-green-400">~1.1s</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Video Enhancement:</span>
                          <span className="text-green-400">~15.2s</span>
                        </div>
                      </div>
                    </div>

                    <div className="p-4 bg-gray-800/50 rounded-lg">
                      <h3 className="text-lg font-semibold mb-3 text-green-400">Performans Kazancı</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-gray-400">GPU vs CPU:</span>
                          <span className="text-green-400">+45%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">DirectML:</span>
                          <span className="text-green-400">+32%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">NPU:</span>
                          <span className="text-green-400">+28%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
