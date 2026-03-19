'use client';

import { useState, useEffect } from 'react';
import { getStatusColor, getStatusBg, getWidthClass } from '@/lib/styles';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Mic, 
  Video, 
  Play, 
  Settings, 
  Zap, 
  Clock, 
  FileText,
  Upload,
  Eye,
  TrendingUp,
  Sparkles,
  Target
} from 'lucide-react';

export default function ProductionLab() {
  const [activeProject, setActiveProject] = useState(null);
  const [renderQueue, setRenderQueue] = useState([
    { id: 1, title: "AI ile Para Kazanma 2026", status: "rendering", progress: 78, duration: "12:34" },
    { id: 2, title: "ChatGPT 5.0 İnceleme", status: "queued", progress: 0, duration: "08:45" },
    { id: 3, title: "Yapay Zeka Trendleri", status: "completed", progress: 100, duration: "15:22" }
  ]);

  const [scriptQueue, setScriptQueue] = useState([
    { id: 1, title: "Tesla Bot 2026", status: "generating", progress: 45 },
    { id: 2, title: "Meta Quest 4", status: "queued", progress: 0 },
    { id: 3, title: "Apple Vision Pro 2", status: "completed", progress: 100 }
  ]);

  const [voiceQueue, setVoiceQueue] = useState([
    { id: 1, title: "AI ile Para Kazanma 2026", voice: "Elif", status: "recording", progress: 92 },
    { id: 2, title: "ChatGPT 5.0 İnceleme", voice: "Hazal", status: "queued", progress: 0 }
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setRenderQueue(prev => prev.map(item => {
        if (item.status === 'rendering' && item.progress < 100) {
          return { ...item, progress: Math.min(100, item.progress + Math.random() * 5) };
        }
        return item;
      }));
      
      setScriptQueue(prev => prev.map(item => {
        if (item.status === 'generating' && item.progress < 100) {
          return { ...item, progress: Math.min(100, item.progress + Math.random() * 8) };
        }
        return item;
      }));
      
      setVoiceQueue(prev => prev.map(item => {
        if (item.status === 'recording' && item.progress < 100) {
          return { ...item, progress: Math.min(100, item.progress + Math.random() * 6) };
        }
        return item;
      }));
    }, 2000);
    
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-400';
      case 'rendering':
      case 'generating':
      case 'recording': return 'text-yellow-400';
      case 'queued': return 'text-gray-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500/20';
      case 'rendering':
      case 'generating':
      case 'recording': return 'bg-yellow-500/20';
      case 'queued': return 'bg-gray-500/20';
      default: return 'bg-gray-500/20';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed': return 'Tamamlandı';
      case 'rendering': return 'Render Ediliyor';
      case 'generating': return 'Senaryo Üretiliyor';
      case 'recording': return 'Seslendiriliyor';
      case 'queued': return 'Sırada';
      default: return 'Bilinmiyor';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">🎬 Production Lab</h2>
          <p className="text-gray-400">Gemini 2.0 Pro Scripting + ElevenLabs Voice + FFmpeg Master Rendering</p>
        </div>
        <div className="flex items-center space-x-2">
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-medium transition-colors flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            Yeni Proje
          </button>
          <button className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-white font-medium transition-colors flex items-center gap-2">
            <Zap className="w-4 h-4" />
            Hızlı Üretim
          </button>
        </div>
      </div>

      {/* Production Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <Brain className="w-5 h-5 text-purple-400" />
            <span className="text-xs text-gray-400">Gemini 2.0 Pro</span>
          </div>
          <div className="text-2xl font-bold text-white mb-1">127</div>
          <div className="text-xs text-gray-400">Senaryo Üretildi</div>
        </div>
        
        <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <Mic className="w-5 h-5 text-blue-400" />
            <span className="text-xs text-gray-400">ElevenLabs</span>
          </div>
          <div className="text-2xl font-bold text-white mb-1">89</div>
          <div className="text-xs text-gray-400">Seslendirme Tamamlandı</div>
        </div>
        
        <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <Video className="w-5 h-5 text-green-400" />
            <span className="text-xs text-gray-400">FFmpeg</span>
          </div>
          <div className="text-2xl font-bold text-white mb-1">64</div>
          <div className="text-xs text-gray-400">Video Render Edildi</div>
        </div>
        
        <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <Target className="w-5 h-5 text-red-400" />
            <span className="text-xs text-gray-400">Viral Score</span>
          </div>
          <div className="text-2xl font-bold text-white mb-1">94%</div>
          <div className="text-xs text-gray-400">Başarı Oranı</div>
        </div>
      </div>

      {/* Production Queues */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Script Generation Queue */}
        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <FileText className="w-5 h-5 text-purple-400" />
              Senaryo Kuyruğu
            </h3>
            <span className="text-xs text-gray-400">{scriptQueue.length} proje</span>
          </div>
          <div className="space-y-3">
            {scriptQueue.map((item) => (
              <div key={item.id} className="bg-gray-900/50 rounded-lg p-3 border border-gray-600">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-white font-medium">{item.title}</span>
                  <span className={`text-xs px-2 py-1 rounded ${getStatusBg(item.status)} ${getStatusColor(item.status)}`}>
                    {getStatusText(item.status)}
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div 
                    className={`bg-purple-500 h-2 rounded-full transition-all duration-500 ${getWidthClass(item.progress)}`}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Voice Recording Queue */}
        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <Mic className="w-5 h-5 text-blue-400" />
              Seslendirme Kuyruğu
            </h3>
            <span className="text-xs text-gray-400">{voiceQueue.length} proje</span>
          </div>
          <div className="space-y-3">
            {voiceQueue.map((item) => (
              <div key={item.id} className="bg-gray-900/50 rounded-lg p-3 border border-gray-600">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-white font-medium">{item.title}</span>
                  <span className={`text-xs px-2 py-1 rounded ${getStatusBg(item.status)} ${getStatusColor(item.status)}`}>
                    {getStatusText(item.status)}
                  </span>
                </div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-gray-400">Ses: {item.voice}</span>
                  <span className="text-xs text-gray-400">{item.progress}%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div 
                    className={`bg-blue-500 h-2 rounded-full transition-all duration-500 ${getWidthClass(item.progress)}`}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Video Render Queue */}
        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <Video className="w-5 h-5 text-green-400" />
              Render Kuyruğu
            </h3>
            <span className="text-xs text-gray-400">{renderQueue.length} proje</span>
          </div>
          <div className="space-y-3">
            {renderQueue.map((item) => (
              <div key={item.id} className="bg-gray-900/50 rounded-lg p-3 border border-gray-600">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-white font-medium">{item.title}</span>
                  <span className={`text-xs px-2 py-1 rounded ${getStatusBg(item.status)} ${getStatusColor(item.status)}`}>
                    {getStatusText(item.status)}
                  </span>
                </div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-gray-400">Süre: {item.duration}</span>
                  <span className="text-xs text-gray-400">{item.progress}%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div 
                    className={`bg-green-500 h-2 rounded-full transition-all duration-500 ${getWidthClass(item.progress)}`}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-xl p-6 border border-purple-500/30">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5 text-purple-400" />
          Hızlı Üretim Modülleri
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-purple-500 transition-colors">
            <FileText className="w-6 h-6 text-purple-400 mb-2" />
            <div className="text-sm text-white font-medium">Viral Script</div>
            <div className="text-xs text-gray-400">1 dakikada hazır</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-blue-500 transition-colors">
            <Mic className="w-6 h-6 text-blue-400 mb-2" />
            <div className="text-sm text-white font-medium">Hızlı Ses</div>
            <div className="text-xs text-gray-400">30 saniyede hazır</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-green-500 transition-colors">
            <Video className="w-6 h-6 text-green-400 mb-2" />
            <div className="text-sm text-white font-medium">Auto Render</div>
            <div className="text-xs text-gray-400">5 dakikada hazır</div>
          </button>
          <button className="p-4 bg-gray-800/50 rounded-lg border border-gray-600 hover:border-red-500 transition-colors">
            <Upload className="w-6 h-6 text-red-400 mb-2" />
            <div className="text-sm text-white font-medium">Bulk Upload</div>
            <div className="text-xs text-gray-400">Tüm platformlara</div>
          </button>
        </div>
      </div>
    </div>
  );
}
