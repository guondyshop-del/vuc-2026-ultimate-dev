'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle, ChevronRight, ChevronLeft, Key, User, Target, Play,
  Shield, Zap, Globe, Database, Link2, RefreshCw, AlertCircle
} from 'lucide-react';

interface WizardStep {
  id: number;
  title: string;
  description: string;
  icon: React.ElementType;
}

const STEPS: WizardStep[] = [
  { id: 1, title: 'Bağlantılar', description: 'API Anahtarları & Güvenli Vault', icon: Key },
  { id: 2, title: 'Persona', description: 'İlk Dijital Hayaletinizi Oluşturun', icon: User },
  { id: 3, title: 'Strateji', description: 'Niş & Rakip Analizi', icon: Target },
  { id: 4, title: 'İlk Yayın', description: 'Master İçerik & Shadow Snippetler', icon: Play },
];

interface ConnectionStatus {
  google: 'pending' | 'connected' | 'error';
  youtube: 'pending' | 'connected' | 'error';
  meta: 'pending' | 'connected' | 'error';
  tiktok: 'pending' | 'connected' | 'error';
}

export default function OnboardingWizard() {
  const [currentStep, setCurrentStep] = useState(1);
  const [isCompleted, setIsCompleted] = useState(false);
  const [progress, setProgress] = useState(0);
  
  // Step 1: API Connections
  const [connections, setConnections] = useState<ConnectionStatus>({
    google: 'pending',
    youtube: 'pending',
    meta: 'pending',
    tiktok: 'pending'
  });
  
  // Step 2: Persona Creation
  const [persona, setPersona] = useState({
    name: '',
    niche: 'technology',
    proxy: 'residential_tr',
    age: '25-34'
  });
  
  // Step 3: Strategy
  const [strategy, setStrategy] = useState({
    targetNiche: '',
    primaryKeyword: '',
    competitorChannel: ''
  });
  
  // Step 4: Content
  const [content, setContent] = useState({
    title: '',
    scriptType: 'educational',
    platforms: ['youtube', 'tiktok', 'instagram']
  });

  // Health check simulation
  useEffect(() => {
    const checkHealth = async () => {
      const statuses: ConnectionStatus = { ...connections };
      
      // Simulate API health checks
      const apis = ['google', 'youtube', 'meta', 'tiktok'] as const;
      for (const api of apis) {
        await new Promise(r => setTimeout(r, 500));
        statuses[api] = Math.random() > 0.3 ? 'connected' : 'error';
        setConnections({ ...statuses });
      }
      
      // Calculate progress
      const connected = Object.values(statuses).filter(s => s === 'connected').length;
      const baseProgress = (connected / 4) * 25;
      const stepProgress = ((currentStep - 1) / 4) * 75;
      setProgress(Math.min(100, baseProgress + stepProgress));
    };
    
    if (currentStep === 1) {
      checkHealth();
    } else {
      setProgress(((currentStep - 1) / 4) * 100);
    }
  }, [currentStep]);

  const getStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-white mb-2">API Bağlantıları</h2>
              <p className="text-gray-400">Google, Meta, TikTok ve YouTube API anahtarlarınızı güvenli vault'a ekleyin</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { key: 'google', name: 'Google AI (Gemini)', url: 'https://makersuite.google.com/app/apikey' },
                { key: 'youtube', name: 'YouTube Data API', url: 'https://console.cloud.google.com/apis/credentials' },
                { key: 'meta', name: 'Meta Graph API', url: 'https://developers.facebook.com/tools/explorer' },
                { key: 'tiktok', name: 'TikTok Research API', url: 'https://developers.tiktok.com/' }
              ].map((api) => (
                <div key={api.key} className="bg-gray-800 rounded-xl p-4 border border-gray-700">
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-medium text-white">{api.name}</span>
                    {connections[api.key as keyof ConnectionStatus] === 'connected' ? (
                      <CheckCircle className="w-5 h-5 text-green-400" />
                    ) : connections[api.key as keyof ConnectionStatus] === 'error' ? (
                      <AlertCircle className="w-5 h-5 text-red-400" />
                    ) : (
                      <RefreshCw className="w-5 h-5 text-yellow-400 animate-spin" />
                    )}
                  </div>
                  <a 
                    href={api.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-sm text-blue-400 hover:text-blue-300 transition-colors"
                  >
                    <Link2 className="w-4 h-4" />
                    API Console'a Git
                  </a>
                </div>
              ))}
            </div>
            
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4">
              <div className="flex items-center gap-3">
                <Shield className="w-5 h-5 text-blue-400" />
                <div>
                  <p className="text-sm font-medium text-blue-300">Güvenli Vault Aktif</p>
                  <p className="text-xs text-gray-400">API anahtarlarınız şifrelenmiş olarak saklanıyor</p>
                </div>
              </div>
            </div>
          </div>
        );
        
      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-white mb-2">Dijital Persona Oluştur</h2>
              <p className="text-gray-400">İlk hayalet kimliğinizi oluşturun ve proxy atayın</p>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Persona Adı</label>
                <input
                  type="text"
                  value={persona.name}
                  onChange={(e) => setPersona({ ...persona, name: e.target.value })}
                  placeholder="örn: TechWizard_TR"
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  aria-label="Persona adı girin"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Niş</label>
                  <select
                    value={persona.niche}
                    onChange={(e) => setPersona({ ...persona, niche: e.target.value })}
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:ring-2 focus:ring-blue-500"
                    aria-label="Niş seçin"
                  >
                    <option value="technology">Teknoloji</option>
                    <option value="business">İş & Finans</option>
                    <option value="education">Eğitim</option>
                    <option value="gaming">Oyun</option>
                    <option value="entertainment">Eğlence</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Proxy Konumu</label>
                  <select
                    value={persona.proxy}
                    onChange={(e) => setPersona({ ...persona, proxy: e.target.value })}
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:ring-2 focus:ring-blue-500"
                    aria-label="Proxy konumu seçin"
                  >
                    <option value="residential_tr">Türkiye (Residential)</option>
                    <option value="residential_de">Almanya (Residential)</option>
                    <option value="residential_us">ABD (Residential)</option>
                    <option value="residential_nl">Hollanda (Residential)</option>
                  </select>
                </div>
              </div>
              
              <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
                <div className="flex items-center gap-3 mb-3">
                  <Shield className="w-5 h-5 text-green-400" />
                  <span className="font-medium text-white">Stealth 4.0 Aktif</span>
                </div>
                <ul className="space-y-2 text-sm text-gray-400">
                  <li className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    Canvas/WebGPU Spoofing
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    AudioContext Fingerprint Masking
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    Font List Randomization
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    Human-like Interaction Jitter
                  </li>
                </ul>
              </div>
            </div>
          </div>
        );
        
      case 3:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-white mb-2">Strateji & Rakip Analizi</h2>
              <p className="text-gray-400">Hedef nişinizi ve rakiplerinizi tanımlayın</p>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Hedef Niş</label>
                <input
                  type="text"
                  value={strategy.targetNiche}
                  onChange={(e) => setStrategy({ ...strategy, targetNiche: e.target.value })}
                  placeholder="örn: Yapay Zeka ile Para Kazanma"
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-400 mb-2">Ana Anahtar Kelime</label>
                <input
                  type="text"
                  value={strategy.primaryKeyword}
                  onChange={(e) => setStrategy({ ...strategy, primaryKeyword: e.target.value })}
                  placeholder="örn: yapay zeka"
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-400 mb-2">Rakip Kanal (Opsiyonel)</label>
                <input
                  type="text"
                  value={strategy.competitorChannel}
                  onChange={(e) => setStrategy({ ...strategy, competitorChannel: e.target.value })}
                  placeholder="örn: UCxxxxxxxxxxxxxxxxxxx"
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-500/30 rounded-xl p-4">
                <div className="flex items-start gap-3">
                  <Zap className="w-5 h-5 text-purple-400 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-purple-300">Omni-Spy 5.0 Hazır</p>
                    <p className="text-xs text-gray-400 mt-1">
                    Sırada: Script reverse-engineering, retention gap analizi, saliency map optimizasyonu
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
        
      case 4:
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-white mb-2">İlk Yayınınızı Oluşturun</h2>
              <p className="text-gray-400">Master içerik ve multi-platform snippetler</p>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Video Başlığı</label>
                <input
                  type="text"
                  value={content.title}
                  onChange={(e) => setContent({ ...content, title: e.target.value })}
                  placeholder="örn: Yapay Zeka ile 2026'da Para Kazanmanın 5 Yolu!"
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-400 mb-2">Senaryo Türü</label>
                <select
                  value={content.scriptType}
                  onChange={(e) => setContent({ ...content, scriptType: e.target.value })}
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:ring-2 focus:ring-blue-500"
                  aria-label="Senaryo türü seçin"
                >
                  <option value="educational">Eğitici (Tutorial)</option>
                  <option value="storytelling">Hikaye Anlatımı</option>
                  <option value="review">İnceleme</option>
                  <option value="news">Haber/Analiz</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm text-gray-400 mb-2">Hedef Platformlar</label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {[
                    { key: 'youtube', name: 'YouTube', color: 'red' },
                    { key: 'tiktok', name: 'TikTok', color: 'pink' },
                    { key: 'instagram', name: 'Instagram', color: 'purple' },
                    { key: 'twitter', name: 'X/Twitter', color: 'blue' }
                  ].map((platform) => (
                    <button
                      key={platform.key}
                      onClick={() => {
                        const platforms = content.platforms.includes(platform.key)
                          ? content.platforms.filter(p => p !== platform.key)
                          : [...content.platforms, platform.key];
                        setContent({ ...content, platforms });
                      }}
                      className={`px-4 py-3 rounded-xl border transition-all ${
                        content.platforms.includes(platform.key)
                          ? `bg-${platform.color}-500/20 border-${platform.color}-500 text-${platform.color}-400`
                          : 'bg-gray-800 border-gray-700 text-gray-400 hover:border-gray-500'
                      }`}
                      aria-label={`${platform.name} platformunu ${content.platforms.includes(platform.key) ? 'kaldır' : 'ekle'}`}
                    >
                      {platform.name}
                    </button>
                  ))}
                </div>
              </div>
              
              <div className="bg-green-500/10 border border-green-500/30 rounded-xl p-4">
                <div className="flex items-center gap-3">
                  <Database className="w-5 h-5 text-green-400" />
                  <div>
                    <p className="text-sm font-medium text-green-300">Otomasyon Hazır</p>
                    <p className="text-xs text-gray-400">Script → Seslendirme → 9:16 Reframes → Thumbnail → Yayın</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };

  if (isCompleted) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center p-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-md w-full text-center"
        >
          <div className="w-24 h-24 bg-gradient-to-br from-green-400 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-4">Empire Hazır!</h1>
          <p className="text-gray-400 mb-8">
            VUC-2026 Omniverse sisteminiz başarıyla yapılandırıldı. 
            İlk kampanyanızı başlatmaya hazırsınız.
          </p>
          <a
            href="/omniverse"
            className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all"
          >
            <Globe className="w-5 h-5" />
            Omniverse Dashboard'a Git
          </a>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Progress Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-white">VUC-2026 Kurulum Sihirbazı</h1>
            <span className="text-sm text-gray-400">%{Math.round(progress)} Tamamlandı</span>
          </div>
          <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-blue-500 to-purple-600"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
          
          {/* Step Indicators */}
          <div className="flex justify-between mt-6">
            {STEPS.map((step) => {
              const Icon = step.icon;
              const isActive = currentStep === step.id;
              const isPast = currentStep > step.id;
              
              return (
                <div key={step.id} className="flex flex-col items-center">
                  <div
                    className={`w-12 h-12 rounded-full flex items-center justify-center mb-2 transition-all ${
                      isActive
                        ? 'bg-blue-500 text-white ring-4 ring-blue-500/30'
                        : isPast
                        ? 'bg-green-500 text-white'
                        : 'bg-gray-800 text-gray-400'
                    }`}
                  >
                    {isPast ? (
                      <CheckCircle className="w-6 h-6" />
                    ) : (
                      <Icon className="w-6 h-6" />
                    )}
                  </div>
                  <span className={`text-xs ${isActive ? 'text-white' : 'text-gray-500'}`}>
                    {step.title}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
        
        {/* Step Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 border border-gray-700"
          >
            {getStepContent()}
          </motion.div>
        </AnimatePresence>
        
        {/* Navigation */}
        <div className="flex justify-between mt-8">
          <button
            onClick={() => setCurrentStep(Math.max(1, currentStep - 1))}
            disabled={currentStep === 1}
            className="flex items-center gap-2 px-6 py-3 text-gray-400 hover:text-white disabled:opacity-30 transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
            Geri
          </button>
          
          <button
            onClick={() => {
              if (currentStep === 4) {
                setIsCompleted(true);
              } else {
                setCurrentStep(Math.min(4, currentStep + 1));
              }
            }}
            className="flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all"
          >
            {currentStep === 4 ? 'Empire Başlat' : 'Devam Et'}
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
