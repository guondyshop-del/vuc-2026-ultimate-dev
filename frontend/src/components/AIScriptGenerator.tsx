'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Zap, 
  Clock, 
  TrendingUp, 
  Target,
  Lightbulb,
  Play,
  Download
} from 'lucide-react';

interface ScriptRequest {
  topic: string;
  niche: string;
  target_audience: string;
  duration_minutes: number;
  style: string;
  keywords: string[];
  language: string;
}

interface ScriptResponse {
  success: boolean;
  title: string;
  content: string;
  seo_tags: string[];
  description: string;
  estimated_views: number;
  viral_score: number;
  thumbnail_ideas: string[];
  hooks: string[];
  ctas: string[];
  processing_time: number;
  message: string;
}

export default function AIScriptGenerator() {
  const [scriptRequest, setScriptRequest] = useState<ScriptRequest>({
    topic: '',
    niche: 'teknoloji',
    target_audience: 'genç yetişkinler',
    duration_minutes: 10,
    style: 'engaging',
    keywords: [],
    language: 'tr'
  });
  
  const [generatedScript, setGeneratedScript] = useState<ScriptResponse | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [keywordInput, setKeywordInput] = useState('');

  const handleGenerateScript = async () => {
    if (!scriptRequest.topic.trim()) {
      alert('Lütfen bir konu girin');
      return;
    }

    setIsGenerating(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/scripts/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(scriptRequest),
      });

      const data: ScriptResponse = await response.json();
      
      if (response.ok) {
        setGeneratedScript(data);
      } else {
        alert('Script oluşturma başarısız: ' + data.message);
      }
    } catch (error) {
      console.error('Script generation error:', error);
      alert('Script oluşturulurken hata oluştu');
    } finally {
      setIsGenerating(false);
    }
  };

  const addKeyword = () => {
    if (keywordInput.trim() && !scriptRequest.keywords.includes(keywordInput.trim())) {
      setScriptRequest(prev => ({
        ...prev,
        keywords: [...prev.keywords, keywordInput.trim()]
      }));
      setKeywordInput('');
    }
  };

  const removeKeyword = (keyword: string) => {
    setScriptRequest(prev => ({
      ...prev,
      keywords: prev.keywords.filter(k => k !== keyword)
    }));
  };

  const downloadScript = () => {
    if (!generatedScript) return;
    
    const content = `Başlık: ${generatedScript.title}\n\nAçıklama: ${generatedScript.description}\n\nSEO Etiketleri: ${generatedScript.seo_tags.join(', ')}\n\nTahmini İzlenme: ${generatedScript.estimated_views}\nViral Skor: ${generatedScript.viral_score}/10\n\nScript:\n${generatedScript.content}`;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${generatedScript.title.replace(/[^a-z0-9]/gi, '_')}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold mb-2 flex items-center">
            <Brain className="w-8 h-8 mr-3 text-purple-500" />
            AI Senaryo Üretici
          </h1>
          <p className="text-gray-400">Gemini 2.0 Pro ile viral senaryolar otomatik olarak üretilir</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            {/* Topic */}
            <div>
              <label className="block text-sm font-medium mb-2">Konu *</label>
              <input
                type="text"
                value={scriptRequest.topic}
                onChange={(e) => setScriptRequest(prev => ({ ...prev, topic: e.target.value }))}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                placeholder="Örn: 10 Yanlış Bilinen Teknoloji Mitleri"
              />
            </div>

            {/* Niche */}
            <div>
              <label className="block text-sm font-medium mb-2">Niş</label>
              <select
                value={scriptRequest.niche}
                onChange={(e) => setScriptRequest(prev => ({ ...prev, niche: e.target.value }))}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                aria-label="Niş seçimi"
                title="Video niş alanını seçin"
              >
                <option value="teknoloji">Teknoloji</option>
                <option value="eğitim">Eğitim</option>
                <option value="finans">Finans</option>
                <option value="sağlık">Sağlık</option>
                <option value="oyun">Oyun</option>
                <option value="seyahat">Seyahat</option>
                <option value="yemek">Yemek</option>
                <option value="spor">Spor</option>
              </select>
            </div>

            {/* Target Audience */}
            <div>
              <label className="block text-sm font-medium mb-2">Hedef Kitle</label>
              <input
                type="text"
                value={scriptRequest.target_audience}
                onChange={(e) => setScriptRequest(prev => ({ ...prev, target_audience: e.target.value }))}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                placeholder="Örn: Genç yetişkinler, öğrenciler"
              />
            </div>

            {/* Duration */}
            <div>
              <label className="block text-sm font-medium mb-2">Süre (dakika)</label>
              <input
                type="number"
                min="5"
                max="30"
                value={scriptRequest.duration_minutes}
                onChange={(e) => setScriptRequest(prev => ({ ...prev, duration_minutes: parseInt(e.target.value) }))}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                aria-label="Süre (dakika)"
                placeholder="5-30 dakika arası"
              />
            </div>

            {/* Style */}
            <div>
              <label className="block text-sm font-medium mb-2">Stil</label>
              <select
                value={scriptRequest.style}
                onChange={(e) => setScriptRequest(prev => ({ ...prev, style: e.target.value }))}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                aria-label="Stil seçimi"
                title="Video stilini seçin"
              >
                <option value="engaging">Eğlenceli & Etkileşimli</option>
                <option value="educational">Eğitici & Bilgilendirici</option>
                <option value="entertaining">Eğlenceli & Mizahi</option>
                <option value="professional">Profesyonel & Ciddi</option>
                <option value="viral">Viral & Trend Odaklı</option>
              </select>
            </div>

            {/* Keywords */}
            <div>
              <label className="block text-sm font-medium mb-2">Anahtar Kelimeler</label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={keywordInput}
                  onChange={(e) => setKeywordInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addKeyword()}
                  className="flex-1 px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-purple-500"
                  placeholder="Anahtar kelime ekle"
                />
                <button
                  onClick={addKeyword}
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
                >
                  Ekle
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {scriptRequest.keywords.map((keyword, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-purple-500/20 border border-purple-500/30 rounded-full text-sm flex items-center gap-2"
                  >
                    {keyword}
                    <button
                      onClick={() => removeKeyword(keyword)}
                      className="text-purple-400 hover:text-purple-300"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerateScript}
              disabled={isGenerating}
              className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 rounded-lg font-semibold transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isGenerating ? (
                <>
                  <Clock className="w-5 h-5 mr-2 animate-spin" />
                  AI Senaryo Üretiliyor...
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5 mr-2" />
                  Senaryo Üret
                </>
              )}
            </button>
          </motion.div>

          {/* Results */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            {generatedScript ? (
              <>
                {/* Script Stats */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <TrendingUp className="w-5 h-5 text-green-500" />
                      <span className="text-2xl font-bold text-green-500">{generatedScript.viral_score}/10</span>
                    </div>
                    <div className="text-sm text-gray-400">Viral Skor</div>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <Target className="w-5 h-5 text-blue-500" />
                      <span className="text-2xl font-bold text-blue-500">{(generatedScript.estimated_views / 1000).toFixed(0)}K</span>
                    </div>
                    <div className="text-sm text-gray-400">Tahmini İzlenme</div>
                  </div>
                </div>

                {/* Script Content */}
                <div className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-xl font-bold mb-4">{generatedScript.title}</h3>
                  <p className="text-gray-400 mb-4">{generatedScript.description}</p>
                  
                  <div className="mb-4">
                    <h4 className="font-semibold mb-2 flex items-center">
                      <Lightbulb className="w-4 h-4 mr-2 text-yellow-500" />
                      Kancalar (Hooks)
                    </h4>
                    <ul className="list-disc list-inside text-gray-300">
                      {generatedScript.hooks.map((hook, index) => (
                        <li key={index}>{hook}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="mb-4">
                    <h4 className="font-semibold mb-2">Senaryo</h4>
                    <div className="bg-gray-900 rounded p-4 max-h-64 overflow-y-auto">
                      <pre className="whitespace-pre-wrap text-sm text-gray-300">
                        {generatedScript.content}
                      </pre>
                    </div>
                  </div>

                  <div className="mb-4">
                    <h4 className="font-semibold mb-2">SEO Etiketleri</h4>
                    <div className="flex flex-wrap gap-2">
                      {generatedScript.seo_tags.map((tag, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-blue-500/20 border border-blue-500/30 rounded-full text-sm"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="mb-4">
                    <h4 className="font-semibold mb-2">Thumbnail Fikirleri</h4>
                    <ul className="list-disc list-inside text-gray-300">
                      {generatedScript.thumbnail_ideas.map((idea, index) => (
                        <li key={index}>{idea}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="flex gap-4">
                    <button
                      onClick={downloadScript}
                      className="flex-1 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors flex items-center justify-center"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      İndir
                    </button>
                    <button
                      onClick={() => setGeneratedScript(null)}
                      className="flex-1 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
                    >
                      Yeni Senaryo
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <div className="bg-gray-800 rounded-lg p-12 text-center">
                <Brain className="w-16 h-16 mx-auto mb-4 text-purple-500 opacity-50" />
                <h3 className="text-xl font-semibold mb-2">AI Senaryo Hazır</h3>
                <p className="text-gray-400">Formu doldurun ve viral senaryonuzu üretin</p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
