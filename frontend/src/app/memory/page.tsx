'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Clock, 
  TrendingUp, 
  Database, 
  FileText,
  Activity,
  BarChart3,
  Target,
  Zap
} from 'lucide-react';

interface AnalyticsData {
  version: string;
  last_updated: string;
  successful_patterns: {
    upload_times: {
      best_hours: number[];
      best_days: string[];
      conversion_rates: Record<string, number>;
    };
    title_patterns: {
      high_ctr_templates: string[];
      emotional_triggers: string[];
    };
    thumbnail_styles: {
      high_performing: Record<string, any>;
    };
    content_strategies: {
      hook_patterns: Record<string, any>;
    };
    tag_effectiveness: {
      high_performing: Record<string, string[]>;
    };
  };
  learning_metrics: {
    total_videos_analyzed: number;
    successful_patterns_identified: number;
    performance_improvement: number;
  };
}

interface DecisionEntry {
  id: string;
  timestamp: string;
  channel: string;
  topic: string;
  rationale: string;
  confidence_score: number;
  expected_results: string[];
}

export default function MemoryPage() {
  const [activeTab, setActiveTab] = useState<'analytics' | 'decisions'>('analytics');
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [decisions, setDecisions] = useState<DecisionEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMemoryData();
  }, []);

  const fetchMemoryData = async () => {
    try {
      // Analytics verilerini çek
      const analyticsResponse = await fetch('/api/memory/analytics');
      if (analyticsResponse.ok) {
        const data = await analyticsResponse.json();
        setAnalyticsData(data);
      }

      // Karar günlüğünü çek
      const decisionsResponse = await fetch('/api/memory/decisions');
      if (decisionsResponse.ok) {
        const data = await decisionsResponse.json();
        setDecisions(data);
      }
    } catch (error) {
      console.error('Sistem hafıza verileri çekilemedi:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('tr-TR');
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.85) return 'text-green-400';
    if (score >= 0.70) return 'text-yellow-400';
    return 'text-red-400';
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
            <span className="gradient-text">Sistem Hafızası</span>
          </h1>
          <p className="text-gray-400">
            VUC-2026 AI kararları ve öğrenme verileri
          </p>
        </motion.div>

        {/* Tab Navigation */}
        <div className="flex space-x-4 mb-8 border-b border-gray-800">
          <button
            onClick={() => setActiveTab('analytics')}
            className={`pb-4 px-6 font-semibold transition-all duration-300 ${
              activeTab === 'analytics'
                ? 'text-amber-500 border-b-2 border-amber-500'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <Database className="w-5 h-5 inline mr-2" />
            Analytics Vault
          </button>
          <button
            onClick={() => setActiveTab('decisions')}
            className={`pb-4 px-6 font-semibold transition-all duration-300 ${
              activeTab === 'decisions'
                ? 'text-amber-500 border-b-2 border-amber-500'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <FileText className="w-5 h-5 inline mr-2" />
            Karar Günlüğü
          </button>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500"></div>
          </div>
        ) : (
          <>
            {/* Analytics Vault Tab */}
            {activeTab === 'analytics' && analyticsData && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-8"
              >
                {/* Özet Kartları */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <div className="glass-effect rounded-xl p-6">
                    <div className="flex items-center mb-4">
                      <BarChart3 className="w-8 h-8 mr-3 text-amber-500" />
                      <h3 className="text-lg font-semibold">Analiz Edilen Video</h3>
                    </div>
                    <div className="text-3xl font-bold text-amber-400">
                      {formatNumber(analyticsData.learning_metrics.total_videos_analyzed)}
                    </div>
                  </div>

                  <div className="glass-effect rounded-xl p-6">
                    <div className="flex items-center mb-4">
                      <Target className="w-8 h-8 mr-3 text-green-500" />
                      <h3 className="text-lg font-semibold">Başarılı Pattern</h3>
                    </div>
                    <div className="text-3xl font-bold text-green-400">
                      {analyticsData.learning_metrics.successful_patterns_identified}
                    </div>
                  </div>

                  <div className="glass-effect rounded-xl p-6">
                    <div className="flex items-center mb-4">
                      <TrendingUp className="w-8 h-8 mr-3 text-blue-500" />
                      <h3 className="text-lg font-semibold">Performans İyileşme</h3>
                    </div>
                    <div className="text-3xl font-bold text-blue-400">
                      +{(analyticsData.learning_metrics.performance_improvement * 100).toFixed(1)}%
                    </div>
                  </div>

                  <div className="glass-effect rounded-xl p-6">
                    <div className="flex items-center mb-4">
                      <Zap className="w-8 h-8 mr-3 text-purple-500" />
                      <h3 className="text-lg font-semibold">Optimizasyon Döngüsü</h3>
                    </div>
                    <div className="text-3xl font-bold text-purple-400">
                      {analyticsData.learning_metrics.optimization_cycles}
                    </div>
                  </div>
                </div>

                {/* En İyi Yayın Zamanları */}
                <div className="glass-effect rounded-xl p-6">
                  <h2 className="text-2xl font-bold mb-6 flex items-center">
                    <Clock className="w-7 h-7 mr-3 text-amber-500" />
                    En İyi Yayın Zamanları
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                      <h3 className="text-lg font-semibold mb-4 text-green-400">En İyi Saatler</h3>
                      <div className="flex flex-wrap gap-2">
                        {analyticsData.successful_patterns.upload_times.best_hours.map((hour) => (
                          <span key={hour} className="px-3 py-1 bg-green-500/20 text-green-400 rounded-lg text-sm">
                            {hour}:00
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold mb-4 text-blue-400">En İyi Günler</h3>
                      <div className="flex flex-wrap gap-2">
                        {analyticsData.successful_patterns.upload_times.best_days.map((day) => (
                          <span key={day} className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-lg text-sm capitalize">
                            {day}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Başarılı Başlık Patternleri */}
                <div className="glass-effect rounded-xl p-6">
                  <h2 className="text-2xl font-bold mb-6 flex items-center">
                    <Brain className="w-7 h-7 mr-3 text-purple-500" />
                    Başarılı Başlık Patternleri
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="text-lg font-semibold mb-4 text-amber-400">Yüksek CTR Şablonları</h3>
                      <div className="space-y-2">
                        {analyticsData.successful_patterns.title_patterns.high_ctr_templates.map((template, index) => (
                          <div key={index} className="p-3 bg-gray-800/50 rounded-lg text-sm">
                            {template}
                          </div>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold mb-4 text-red-400">Duygusal Tetikleyiciler</h3>
                      <div className="flex flex-wrap gap-2">
                        {analyticsData.successful_patterns.title_patterns.emotional_triggers.map((trigger) => (
                          <span key={trigger} className="px-3 py-1 bg-red-500/20 text-red-400 rounded-lg text-sm">
                            {trigger}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Thumbnail Performansı */}
                <div className="glass-effect rounded-xl p-6">
                  <h2 className="text-2xl font-bold mb-6">Thumbnail Stilleri</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {Object.entries(analyticsData.successful_patterns.thumbnail_styles.high_performing).map(([style, data]) => (
                      <div key={style} className="p-4 bg-gray-800/50 rounded-lg">
                        <h3 className="text-lg font-semibold mb-3 capitalize text-amber-400">
                          {style} Stili
                        </h3>
                        <div className="space-y-2 text-sm">
                          <div>
                            <span className="text-gray-400">CTR Ortalama:</span>
                            <span className="text-green-400 ml-2">{(data.ctr_average * 100).toFixed(1)}%</span>
                          </div>
                          <div>
                            <span className="text-gray-400">Başarı Oranı:</span>
                            <span className="text-blue-400 ml-2">{(data.success_rate * 100).toFixed(1)}%</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {/* Karar Günlüğü Tab */}
            {activeTab === 'decisions' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-6"
              >
                <div className="glass-effect rounded-xl p-6">
                  <h2 className="text-2xl font-bold mb-6 flex items-center">
                    <FileText className="w-7 h-7 mr-3 text-amber-500" />
                    AI Karar Günlüğü
                  </h2>
                  
                  {decisions.length === 0 ? (
                    <div className="text-center py-12 text-gray-400">
                      Henüz kaydedilmiş karar bulunmuyor
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {decisions.map((decision, index) => (
                        <motion.div
                          key={decision.id}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.1 }}
                          className="p-6 bg-gray-800/50 rounded-xl border border-gray-700"
                        >
                          <div className="flex items-start justify-between mb-4">
                            <div>
                              <h3 className="text-lg font-semibold text-amber-400">
                                {decision.topic}
                              </h3>
                              <p className="text-sm text-gray-400">
                                {decision.channel} • {formatDate(decision.timestamp)}
                              </p>
                            </div>
                            <div className="text-right">
                              <div className={`text-sm font-semibold ${getConfidenceColor(decision.confidence_score)}`}>
                                Confidence: {(decision.confidence_score * 100).toFixed(0)}%
                              </div>
                            </div>
                          </div>
                          
                          <div className="mb-4">
                            <h4 className="text-sm font-semibold text-gray-300 mb-2">Karar Gerekçesi:</h4>
                            <div className="text-sm text-gray-400 bg-gray-900/50 p-3 rounded-lg">
                              {decision.rationale}
                            </div>
                          </div>
                          
                          <div>
                            <h4 className="text-sm font-semibold text-gray-300 mb-2">Beklenen Sonuçlar:</h4>
                            <div className="space-y-1">
                              {decision.expected_results.map((result, idx) => (
                                <div key={idx} className="text-sm text-gray-400 flex items-center">
                                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                                  {result}
                                </div>
                              ))}
                            </div>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
