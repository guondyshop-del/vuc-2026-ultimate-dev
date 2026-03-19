'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, 
  Activity, 
  Zap, 
  Shield, 
  TrendingUp, 
  Clock,
  CheckCircle,
  AlertTriangle,
  MessageSquare,
  Minimize2,
  Maximize2,
  Send,
  Bot
} from 'lucide-react';

interface AIStatus {
  status: 'active' | 'processing' | 'idle' | 'error';
  current_task: string;
  activity_log: Array<{
    timestamp: string;
    message: string;
    type: 'info' | 'success' | 'warning' | 'error';
    details?: any;
  }>;
  system_metrics: {
    cpu_usage: number;
    memory_usage: number;
    active_processes: number;
    queue_size: number;
  };
  ai_decisions: Array<{
    timestamp: string;
    decision: string;
    reasoning: string;
    confidence: number;
  }>;
}

export default function AIStatusPanel() {
  const [isMinimized, setIsMinimized] = useState(false);
  const [userMessage, setUserMessage] = useState('');
  const [chatMessages, setChatMessages] = useState<Array<{
    type: 'user' | 'ai';
    message: string;
    timestamp: string;
  }>>([]);
  const [aiStatus, setAiStatus] = useState<AIStatus>({
    status: 'active',
    current_task: 'Hazal persona için video render başlatılıyor',
    activity_log: [
      {
        timestamp: new Date().toISOString(),
        message: 'Hazal için video render başlatıldı',
        type: 'info',
        details: { platform: 'youtube', duration: '300s' }
      },
      {
        timestamp: new Date(Date.now() - 30000).toISOString(),
        message: 'Proxy Moldova bağlantısı kuruldu',
        type: 'success',
        details: { proxy: '185.123.456.789', latency: '45ms' }
      },
      {
        timestamp: new Date(Date.now() - 60000).toISOString(),
        message: 'Gemini 2.0 Pro script oluşturdu',
        type: 'success',
        details: { topic: 'Yapay Zeka Para Kazanma', confidence: 0.94 }
      }
    ],
    system_metrics: {
      cpu_usage: 67,
      memory_usage: 45,
      active_processes: 3,
      queue_size: 12
    },
    ai_decisions: [
      {
        timestamp: new Date(Date.now() - 15000).toISOString(),
        decision: 'En iyi yayın zamanını 19:00 olarak belirledi',
        reasoning: 'Hedef kitle 18-22 yaş arası, en aktif saatler',
        confidence: 0.87
      },
      {
        timestamp: new Date(Date.now() - 45000).toISOString(),
        decision: 'Thumbnail renk paletini değiştirdi',
        reasoning: 'Rakip analizi sonrası mavi tonları daha etkili',
        confidence: 0.92
      }
    ]
  });

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setAiStatus(prev => {
        // Update system metrics
        const newMetrics = {
          cpu_usage: Math.max(20, Math.min(95, prev.system_metrics.cpu_usage + (Math.random() - 0.5) * 10)),
          memory_usage: Math.max(30, Math.min(85, prev.system_metrics.memory_usage + (Math.random() - 0.5) * 8)),
          active_processes: Math.max(1, Math.min(10, prev.system_metrics.active_processes + Math.floor((Math.random() - 0.5) * 2))),
          queue_size: Math.max(0, prev.system_metrics.queue_size + Math.floor((Math.random() - 0.5) * 3))
        };

        // Occasionally add new activity
        const activities = [
          'Elif için TikTok video adaptasyonu tamamlandı',
          'Meta API kotası yenilendi',
          'Yeni trend pattern tespit edildi: "AI Tools"',
          'Viral skor hesaplaması: 94.2%',
          'Stealth modu aktifleştirildi',
          'ExifTool metadata eklendi',
          'Lurker protokolü başlatıldı',
          'Analytics verileri senkronize edildi'
        ];

        const newLog = prev.activity_log;

        if (Math.random() > 0.7) {
          newLog.unshift({
            timestamp: new Date().toISOString(),
            message: activities[Math.floor(Math.random() * activities.length)],
            type: Math.random() > 0.8 ? 'warning' : Math.random() > 0.6 ? 'success' : 'info'
          });

          // Keep only last 10 logs
          if (newLog.length > 10) {
            newLog.pop();
          }
        }

        // Update current task occasionally
        const tasks = [
          'Hazal için YouTube video render ediliyor',
          'Elif için Instagram content hazırlanıyor',
          'TikTok trend analizi yapılıyor',
          'Viral skor optimizasyonu aktif',
          'Multi-platform dağıtım sıralanıyor',
          'Persona trust skorları güncelleniyor',
          'Stealth 4.0 parametreleri ayarlanıyor'
        ];

        const newTask = Math.random() > 0.8 ? tasks[Math.floor(Math.random() * tasks.length)] : prev.current_task;

        // Occasionally add AI decisions
        const newDecisions = [...prev.ai_decisions];
        if (Math.random() > 0.9) {
          const decisions = [
            {
              decision: 'Video başlığını optimize etti',
              reasoning: 'A/B test sonuçlarına göre "2026" kelimesi daha etkili',
              confidence: 0.91
            },
            {
              decision: 'Yayın frekansını artırdı',
              reasoning: 'Engagement oranı yükseldi, momentum korunmalı',
              confidence: 0.85
            },
            {
              decision: 'Yeni persona oluşturdu',
              reasoning: 'Gaming nişinde boşluk tespit edildi',
              confidence: 0.88
            }
          ];

          newDecisions.unshift({
            timestamp: new Date().toISOString(),
            ...decisions[Math.floor(Math.random() * decisions.length)]
          });

          if (newDecisions.length > 5) {
            newDecisions.pop();
          }
        }

        return {
          ...prev,
          system_metrics: newMetrics,
          activity_log: newLog,
          current_task: newTask,
          ai_decisions: newDecisions
        };
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400';
      case 'processing': return 'text-blue-400';
      case 'idle': return 'text-yellow-400';
      case 'error': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500/20';
      case 'processing': return 'bg-blue-500/20';
      case 'idle': return 'bg-yellow-500/20';
      case 'error': return 'bg-red-500/20';
      default: return 'bg-gray-500/20';
    }
  };

  const getLogIcon = (type: string) => {
    switch (type) {
      case 'success': return <CheckCircle className="w-3 h-3 text-green-400" />;
      case 'warning': return <AlertTriangle className="w-3 h-3 text-yellow-400" />;
      case 'error': return <AlertTriangle className="w-3 h-3 text-red-400" />;
      default: return <Activity className="w-3 h-3 text-blue-400" />;
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    
    if (diff < 60000) return 'Az önce';
    if (diff < 3600000) return `${Math.floor(diff / 60000)} dk önce`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)} sa önce`;
    return date.toLocaleDateString('tr-TR');
  };

  const handleSendMessage = () => {
    if (!userMessage.trim()) return;

    const newMessage = {
      type: 'user' as const,
      message: userMessage,
      timestamp: new Date().toISOString()
    };

    setChatMessages(prev => [...prev, newMessage]);
    setUserMessage('');

    // Simulate AI response
    setTimeout(() => {
      const aiResponses = [
        'Mevcut durum: 3 video paralel işleniyor, sistem sağlığı %94.',
        'Elif persona için 2 TikTok video tamamlandı, viral skor 87.3.',
        'Yeni trend tespit edildi: "AI Tools" nişinde %42 büyüme potansiyeli.',
        'Proxy rotasyonu başarılı, Moldova IP ile %98 başarı oranı.',
        'Stealth 4.0 aktif, pixel-noise seviyesi optimize edildi.'
      ];

      const aiResponse = {
        type: 'ai' as const,
        message: aiResponses[Math.floor(Math.random() * aiResponses.length)],
        timestamp: new Date().toISOString()
      };

      setChatMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  if (isMinimized) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="bg-gray-900/90 backdrop-blur-lg border border-gray-700 rounded-lg p-3 cursor-pointer"
          onClick={() => setIsMinimized(false)}
        >
          <div className="flex items-center gap-2">
            <Brain className={`w-4 h-4 ${getStatusColor(aiStatus.status)}`} />
            <span className="text-xs text-white">AI Asistan</span>
            <Maximize2 className="w-3 h-3 text-gray-400" />
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 w-96 z-50">
      <motion.div
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-gray-900/95 backdrop-blur-lg border border-gray-700 rounded-lg shadow-2xl"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center gap-2">
            <Brain className={`w-5 h-5 ${getStatusColor(aiStatus.status)}`} />
            <div>
              <h3 className="text-sm font-semibold text-white">AI Asistan</h3>
              <p className="text-xs text-gray-400">VUC-2026 Neural Core</p>
            </div>
          </div>
          <button
            onClick={() => setIsMinimized(true)}
            className="text-gray-400 hover:text-white transition-colors"
            title="Paneli küçült"
          >
            <Minimize2 className="w-4 h-4" />
          </button>
        </div>

        {/* Current Status */}
        <div className="p-4 border-b border-gray-700">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-gray-400">Mevcut Görev</span>
            <div className={`px-2 py-1 rounded text-xs ${getStatusBg(aiStatus.status)} ${getStatusColor(aiStatus.status)}`}>
              {aiStatus.status === 'active' ? 'Aktif' : 
               aiStatus.status === 'processing' ? 'İşleniyor' : 
               aiStatus.status === 'idle' ? 'Beklemede' : 'Hata'}
            </div>
          </div>
          <p className="text-sm text-white mb-3">{aiStatus.current_task}</p>
          
          {/* System Metrics */}
          <div className="grid grid-cols-4 gap-2 text-xs">
            <div className="text-center">
              <div className="text-gray-400">CPU</div>
              <div className="text-white font-medium">{aiStatus.system_metrics.cpu_usage}%</div>
            </div>
            <div className="text-center">
              <div className="text-gray-400">RAM</div>
              <div className="text-white font-medium">{aiStatus.system_metrics.memory_usage}%</div>
            </div>
            <div className="text-center">
              <div className="text-gray-400">Proses</div>
              <div className="text-white font-medium">{aiStatus.system_metrics.active_processes}</div>
            </div>
            <div className="text-center">
              <div className="text-gray-400">Kuyruk</div>
              <div className="text-white font-medium">{aiStatus.system_metrics.queue_size}</div>
            </div>
          </div>
        </div>

        {/* Activity Log */}
        <div className="p-4 border-b border-gray-700 max-h-48 overflow-y-auto">
          <h4 className="text-xs font-semibold text-gray-400 mb-2">Aktivite Log</h4>
          <div className="space-y-2">
            <AnimatePresence>
              {aiStatus.activity_log.map((log, index) => (
                <motion.div
                  key={`${log.timestamp}-${index}`}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="flex items-start gap-2"
                >
                  {getLogIcon(log.type)}
                  <div className="flex-1">
                    <p className="text-xs text-white">{log.message}</p>
                    <p className="text-xs text-gray-500">{formatTimestamp(log.timestamp)}</p>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>

        {/* AI Decisions */}
        <div className="p-4 border-b border-gray-700 max-h-32 overflow-y-auto">
          <h4 className="text-xs font-semibold text-gray-400 mb-2">AI Kararları</h4>
          <div className="space-y-2">
            {aiStatus.ai_decisions.map((decision, index) => (
              <div key={decision.timestamp} className="text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-white font-medium">{decision.decision}</span>
                  <span className="text-gray-400">{Math.round(decision.confidence * 100)}%</span>
                </div>
                <p className="text-gray-500">{decision.reasoning}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Chat Interface */}
        <div className="p-4">
          <div className="mb-3 max-h-32 overflow-y-auto">
            <AnimatePresence>
              {chatMessages.map((msg, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`mb-2 ${msg.type === 'user' ? 'text-right' : 'text-left'}`}
                >
                  <div className={`inline-block px-3 py-1 rounded-lg text-xs ${
                    msg.type === 'user' 
                      ? 'bg-blue-500/20 text-blue-400' 
                      : 'bg-gray-700 text-gray-300'
                  }`}>
                    {msg.message}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {formatTimestamp(msg.timestamp)}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
          
          <div className="flex gap-2">
            <input
              type="text"
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="AI asistana sor..."
              className="flex-1 px-3 py-1 bg-gray-800 border border-gray-600 rounded text-xs text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={handleSendMessage}
              className="p-1 bg-blue-600 hover:bg-blue-700 rounded text-white transition-colors"
              title="Mesaj gönder"
            >
              <Send className="w-3 h-3" />
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
