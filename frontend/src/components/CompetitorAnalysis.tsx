'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Search, 
  TrendingUp, 
  Users, 
  Eye, 
  Clock,
  Zap,
  Target,
  AlertCircle,
  CheckCircle,
  BarChart3,
  Lightbulb,
  Play
} from 'lucide-react';

interface CompetitorAnalysis {
  success: boolean;
  competitor: {
    channel_id: string;
    channel_name: string;
    subscriber_count: number;
    video_count: number;
    total_views: number;
    avg_views_per_video: number;
    upload_frequency: number;
    top_performing_videos: any[];
    content_gaps: string[];
    strengths: string[];
    weaknesses: string[];
    thumbnail_styles: string[];
    title_patterns: string[];
    upload_schedule: Record<string, number>;
  };
  recommendations: string[];
}

export default function CompetitorAnalysis() {
  const [channelUrl, setChannelUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<CompetitorAnalysis | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'content' | 'thumbnails' | 'schedule'>('overview');

  const handleAnalyze = async () => {
    if (!channelUrl.trim()) {
      alert('Lütfen bir kanal URL\'si girin');
      return;
    }

    setIsAnalyzing(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/competitor-analysis/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          channel_url: channelUrl,
          analysis_depth: 'detailed',
          include_video_analysis: true,
          include_thumbnail_analysis: true
        }),
      });

      const data: CompetitorAnalysis = await response.json();
      
      if (response.ok) {
        setAnalysisResult(data);
      } else {
        alert('Analiz başarısız: ' + (data as any).message);
      }
    } catch (error) {
      console.error('Analysis error:', error);
      alert('Analiz sırasında hata oluştu');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const getAnalysisLevel = (score: number) => {
    if (score >= 8) return { level: 'Yüksek', color: 'text-green-500' };
    if (score >= 6) return { level: 'Orta', color: 'text-yellow-500' };
    return { level: 'Düşük', color: 'text-red-500' };
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
            <Search className="w-8 h-8 mr-3 text-blue-500" />
            Rakip Analizi
          </h1>
          <p className="text-gray-400">YouTube rakiplerinizi analiz edin, fırsatları yakalayın</p>
        </motion.div>

        {/* Search Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gray-800 rounded-lg p-6 mb-8"
        >
          <div className="flex gap-4">
            <input
              type="text"
              value={channelUrl}
              onChange={(e) => setChannelUrl(e.target.value)}
              placeholder="YouTube kanal URL'sini girin (örn: https://youtube.com/channel/...)"
              className="flex-1 px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {isAnalyzing ? (
                <>
                  <Clock className="w-5 h-5 mr-2 animate-spin" />
                  Analiz Ediliyor...
                </>
              ) : (
                <>
                  <Search className="w-5 h-5 mr-2" />
                  Analiz Et
                </>
              )}
            </button>
          </div>
        </motion.div>

        {/* Results */}
        {analysisResult && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            {/* Channel Overview */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-2xl font-bold mb-6 flex items-center">
                <Users className="w-6 h-6 mr-2 text-blue-500" />
                {analysisResult.competitor?.channel_name || 'Kanal Adı'}
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-500 mb-2">
                    {formatNumber(analysisResult.competitor?.subscriber_count || 0)}
                  </div>
                  <div className="text-gray-400 text-sm">Abone</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-500 mb-2">
                    {analysisResult.competitor?.video_count || 0}
                  </div>
                  <div className="text-gray-400 text-sm">Video</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-500 mb-2">
                    {formatNumber(analysisResult.competitor?.avg_views_per_video || 0)}
                  </div>
                  <div className="text-gray-400 text-sm">Ortalama İzlenme</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-500 mb-2">
                    {(analysisResult.competitor?.upload_frequency || 0).toFixed(1)}
                  </div>
                  <div className="text-gray-400 text-sm">Haftalık Yükleme</div>
                </div>
              </div>

              {/* Tabs */}
              <div className="border-b border-gray-700 mb-6">
                <div className="flex space-x-8">
                  {[
                    { id: 'overview', label: 'Genel Bakış', icon: BarChart3 },
                    { id: 'content', label: 'İçerik Analizi', icon: Play },
                    { id: 'thumbnails', label: 'Thumbnail Stratejisi', icon: Eye },
                    { id: 'schedule', label: 'Yükleme Programı', icon: Clock }
                  ].map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id as any)}
                      className={`pb-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
                        activeTab === tab.id
                          ? 'border-blue-500 text-blue-500'
                          : 'border-transparent text-gray-400 hover:text-gray-300'
                      }`}
                    >
                      <tab.icon className="w-4 h-4" />
                      {tab.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Tab Content */}
              <div>
                {activeTab === 'overview' && (
                  <div className="space-y-6">
                    {/* Strengths */}
                    <div>
                      <h3 className="text-lg font-semibold mb-3 flex items-center">
                        <CheckCircle className="w-5 h-5 mr-2 text-green-500" />
                        Güçlü Yönler
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {analysisResult.competitor?.strengths?.map((strength, index) => (
                          <div key={index} className="flex items-center gap-2 bg-green-500/10 border border-green-500/30 rounded-lg p-3">
                            <CheckCircle className="w-4 h-4 text-green-500" />
                            <span className="text-sm">{strength}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Weaknesses */}
                    <div>
                      <h3 className="text-lg font-semibold mb-3 flex items-center">
                        <AlertCircle className="w-5 h-5 mr-2 text-red-500" />
                        Zayıf Yönler
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {analysisResult.competitor?.weaknesses?.map((weakness, index) => (
                          <div key={index} className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 rounded-lg p-3">
                            <AlertCircle className="w-4 h-4 text-red-500" />
                            <span className="text-sm">{weakness}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Recommendations */}
                    <div>
                      <h3 className="text-lg font-semibold mb-3 flex items-center">
                        <Lightbulb className="w-5 h-5 mr-2 text-yellow-500" />
                        Öneriler
                      </h3>
                      <div className="space-y-2">
                        {analysisResult.recommendations.map((recommendation, index) => (
                          <div key={index} className="flex items-center gap-2 bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3">
                            <Target className="w-4 h-4 text-yellow-500" />
                            <span className="text-sm">{recommendation}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'content' && (
                  <div className="space-y-6">
                    {/* Content Gaps */}
                    <div>
                      <h3 className="text-lg font-semibold mb-3 flex items-center">
                        <Zap className="w-5 h-5 mr-2 text-purple-500" />
                        İçerik Boşlukları (Fırsatlar)
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {analysisResult.competitor?.content_gaps?.map((gap, index) => (
                          <div key={index} className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-3">
                            <div className="flex items-center gap-2 mb-2">
                              <Zap className="w-4 h-4 text-purple-500" />
                              <span className="font-medium">{gap}</span>
                            </div>
                            <div className="text-sm text-gray-400">Bu konuda içerik üretin</div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Title Patterns */}
                    <div>
                      <h3 className="text-lg font-semibold mb-3">Başlık Desenleri</h3>
                      <div className="flex flex-wrap gap-2">
                        {analysisResult.competitor?.title_patterns?.map((pattern, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-blue-500/20 border border-blue-500/30 rounded-full text-sm"
                          >
                            {pattern}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Top Videos */}
                    <div>
                      <h3 className="text-lg font-semibold mb-3 flex items-center">
                        <TrendingUp className="w-5 h-5 mr-2 text-green-500" />
                        En Popüler Videolar
                      </h3>
                      <div className="space-y-3">
                        {analysisResult.competitor?.top_performing_videos?.slice(0, 5).map((video, index) => (
                          <div key={index} className="bg-gray-700 rounded-lg p-4">
                            <div className="flex items-center justify-between">
                              <div>
                                <h4 className="font-medium">{video.title}</h4>
                                <div className="text-sm text-gray-400 mt-1">
                                  {formatNumber(video.views)} izlenme
                                </div>
                              </div>
                              <div className="text-green-500">
                                <TrendingUp className="w-5 h-5" />
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'thumbnails' && (
                  <div className="space-y-6">
                    <h3 className="text-lg font-semibold mb-3 flex items-center">
                      <Eye className="w-5 h-5 mr-2 text-orange-500" />
                      Thumbnail Stratejileri
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {analysisResult.competitor?.thumbnail_styles?.map((style, index) => (
                        <div key={index} className="bg-orange-500/10 border border-orange-500/30 rounded-lg p-4">
                          <div className="flex items-center gap-2 mb-2">
                            <Eye className="w-4 h-4 text-orange-500" />
                            <span className="font-medium">{style}</span>
                          </div>
                          <div className="text-sm text-gray-400">Bu stil kullanılıyor</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {activeTab === 'schedule' && (
                  <div className="space-y-6">
                    <h3 className="text-lg font-semibold mb-3 flex items-center">
                      <Clock className="w-5 h-5 mr-2 text-indigo-500" />
                      Yükleme Programı
                    </h3>
                    <div className="grid grid-cols-7 gap-2">
                      {Object.entries(analysisResult.competitor?.upload_schedule || {}).map(([day, count]) => (
                        <div key={day} className="text-center">
                          <div className="bg-gray-700 rounded-lg p-3">
                            <div className="text-xs text-gray-400 mb-1">{day.slice(0, 3)}</div>
                            <div className="text-lg font-bold text-indigo-500">{count}</div>
                            <div className="text-xs text-gray-400">video</div>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-lg p-4">
                      <div className="text-sm text-indigo-400">
                        En aktif gün: {Object.entries(analysisResult.competitor?.upload_schedule || {})
                          .sort(([,a], [,b]) => b - a)[0]?.[0] || 'Belirsiz'}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
