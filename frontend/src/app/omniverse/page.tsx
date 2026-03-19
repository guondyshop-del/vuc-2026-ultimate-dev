'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Video, Globe, Users, Search, DollarSign, Fingerprint, BarChart3,
  Play, Zap, Activity, CheckCircle, AlertTriangle, Eye, Crosshair,
  Smartphone, Instagram, Twitter, Monitor, Layers, ChevronRight,
  Radio, TrendingUp, Shield, Cpu, Image
} from 'lucide-react';

// Trust score → nearest-5 Tailwind width class (avoids inline styles)
const TRUST_WIDTH_CLASSES: Record<number, string> = {
  0:'w-0', 5:'w-[5%]', 10:'w-[10%]', 15:'w-[15%]', 20:'w-[20%]',
  25:'w-1/4', 30:'w-[30%]', 35:'w-[35%]', 40:'w-[40%]', 45:'w-[45%]',
  50:'w-1/2', 55:'w-[55%]', 60:'w-[60%]', 65:'w-[65%]', 70:'w-[70%]',
  75:'w-3/4', 80:'w-[80%]', 85:'w-[85%]', 90:'w-[90%]', 95:'w-[95%]',
  100:'w-full',
};
const trustWidthClass = (trust: number) =>
  TRUST_WIDTH_CLASSES[Math.round(Math.min(10, Math.max(0, trust)) * 10 / 5) * 5] || 'w-0';

// ─── Tabs ──────────────────────────────────────────────────────────────────

const TABS = [
  { id: 'production', label: 'Üretim Lab', icon: Video, color: 'blue' },
  { id: 'multiverse', label: 'Multi-Verse', icon: Globe, color: 'purple' },
  { id: 'persona', label: 'Persona Vault', icon: Users, color: 'green' },
  { id: 'espionage', label: 'Casusluk', icon: Search, color: 'yellow' },
  { id: 'revenue', label: 'Gelir', icon: DollarSign, color: 'emerald' },
  { id: 'stealth', label: 'Stealth 4.0', icon: Fingerprint, color: 'red' },
  { id: 'analytics', label: 'Global Analiz', icon: BarChart3, color: 'pink' },
];

const API = 'http://localhost:8000';

// ─── Shared helpers ─────────────────────────────────────────────────────────

const StatusBadge = ({ status }: { status: string }) => {
  const map: Record<string, string> = {
    healthy: 'bg-green-500/20 text-green-400',
    active:  'bg-green-500/20 text-green-400',
    idle:    'bg-gray-500/20 text-gray-400',
    critical:'bg-red-500/20 text-red-400',
    high:    'bg-red-500/20 text-red-400',
    medium:  'bg-yellow-500/20 text-yellow-400',
    low:     'bg-blue-500/20 text-blue-400',
    minimal: 'bg-green-500/20 text-green-400',
  };
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${map[status] || 'bg-gray-600/50 text-gray-400'}`}>
      {status}
    </span>
  );
};

// ─── Tab: Production ────────────────────────────────────────────────────────

function ProductionTab() {
  const [form, setForm] = useState({
    topic: '', script_type: 'educational', tone: 'professional',
    seo_keywords: '', duration_target: 300, resolution: '1920x1080',
    shadowban_shield: true, device_type: 'iphone_15_pro', platform: 'youtube'
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runCampaign = async () => {
    if (!form.topic) return;
    setLoading(true);
    try {
      const body = {
        ...form,
        seo_keywords: form.seo_keywords.split(',').map(k => k.trim()).filter(Boolean),
        title: form.topic,
        description: `${form.topic} hakkında kapsamlı rehber.`,
        tags: form.seo_keywords.split(',').map(k => k.trim()).filter(Boolean),
        category: 'Education',
        privacy_status: 'public',
        video_file: { size_mb: 150 }
      };
      const res = await fetch(`${API}/api/empire/campaign/execute`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      setResult(data);
    } catch { setResult({ success: false, error: 'Bağlantı hatası' }); }
    finally { setLoading(false); }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Campaign Form */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-bold mb-5 flex items-center gap-2">
          <Play className="w-5 h-5 text-blue-400" /> Video Kampanyası Başlat
        </h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Konu *</label>
            <input
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Yapay Zeka ile Para Kazanma 2026"
              value={form.topic}
              onChange={e => setForm(f => ({ ...f, topic: e.target.value }))}
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Senaryo Türü</label>
              <select
                title="Senaryo türü seçin"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
                value={form.script_type}
                onChange={e => setForm(f => ({ ...f, script_type: e.target.value }))}
              >
                <option value="educational">Eğitici</option>
                <option value="entertainment">Eğlence</option>
                <option value="business">İş</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Ton</label>
              <select
                title="Video tonu seçin"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
                value={form.tone}
                onChange={e => setForm(f => ({ ...f, tone: e.target.value }))}
              >
                <option value="professional">Profesyonel</option>
                <option value="casual">Samimi</option>
                <option value="emotional">Duygusal</option>
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">SEO Anahtar Kelimeler</label>
            <input
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              placeholder="yapay zeka, para kazanma, AI 2026"
              value={form.seo_keywords}
              onChange={e => setForm(f => ({ ...f, seo_keywords: e.target.value }))}
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Cihaz Profili (Spoofing)</label>
            <select
              title="Cihaz profili seçin"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              value={form.device_type}
              onChange={e => setForm(f => ({ ...f, device_type: e.target.value }))}
            >
              <option value="iphone_15_pro">iPhone 15 Pro (YouTube)</option>
              <option value="sony_a7siii">Sony A7S III (YouTube)</option>
            </select>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-400">Shadowban Shield</span>
            <button
              onClick={() => setForm(f => ({ ...f, shadowban_shield: !f.shadowban_shield }))}
              title={form.shadowban_shield ? 'Shadowban Shield kapat' : 'Shadowban Shield aç'}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${form.shadowban_shield ? 'bg-blue-500' : 'bg-gray-600'}`}
            >
              <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${form.shadowban_shield ? 'translate-x-6' : 'translate-x-1'}`} />
            </button>
          </div>
          <button
            onClick={runCampaign}
            disabled={!form.topic || loading}
            className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loading ? (
              <><div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /><span>İşleniyor...</span></>
            ) : (
              <><Zap className="w-4 h-4" /><span>Kampanyayı Başlat</span></>
            )}
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-bold mb-5 flex items-center gap-2">
          <Activity className="w-5 h-5 text-green-400" /> Kampanya Sonuçları
        </h3>
        {result ? (
          <div className="space-y-3">
            <div className={`p-3 rounded-lg border ${result.success ? 'bg-green-500/10 border-green-500/30' : 'bg-red-500/10 border-red-500/30'}`}>
              <div className="flex items-center gap-2">
                {result.success ? <CheckCircle className="w-4 h-4 text-green-400" /> : <AlertTriangle className="w-4 h-4 text-red-400" />}
                <span className="font-medium text-sm">
                  {result.success ? `${result.successful_steps}/4 adım tamamlandı` : result.error || 'Hata oluştu'}
                </span>
              </div>
            </div>
            {result.results?.map((r: any, i: number) => (
              <div key={i} className="flex items-center justify-between bg-gray-700/50 rounded-lg p-3">
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${r.orchestration?.success ? 'bg-green-400' : 'bg-red-400'}`} />
                  <span className="text-sm capitalize">{r.agent?.replace('_agent', '')}</span>
                </div>
                <div className="flex items-center gap-2">
                  {r.orchestration?.confidence && (
                    <span className="text-xs text-gray-400">Güven: {r.orchestration.confidence.toFixed(0)}%</span>
                  )}
                  <StatusBadge status={r.orchestration?.success ? 'active' : 'critical'} />
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-48 text-gray-500">
            <Video className="w-12 h-12 mb-3 opacity-30" />
            <p className="text-sm">Kampanya başlatmak için formu doldurun</p>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Tab: Multi-Verse ───────────────────────────────────────────────────────

function MultiverseTab() {
  const [form, setForm] = useState({
    title: '', script: '', keywords: '', niche: 'technology',
    youtube_url: 'https://youtube.com/watch'
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [activeAdapt, setActiveAdapt] = useState<string | null>(null);

  const runAdaptation = async () => {
    if (!form.title) return;
    setLoading(true);
    try {
      const body = {
        ...form,
        keywords: form.keywords.split(',').map(k => k.trim()).filter(Boolean)
      };
      const res = await fetch(`${API}/api/omniverse/multiverse/adapt-all`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();
      setResult(data);
    } catch { setResult({ success: false }); }
    finally { setLoading(false); }
  };

  const platformIcons: Record<string, any> = {
    tiktok: Smartphone, instagram: Instagram, twitter: Twitter,
    facebook: Globe, youtube_community: Monitor
  };

  const platformColors: Record<string, string> = {
    tiktok: 'text-pink-400', instagram: 'text-purple-400', twitter: 'text-blue-400',
    facebook: 'text-blue-600', youtube_community: 'text-red-400'
  };

  return (
    <div className="space-y-6">
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-bold mb-5 flex items-center gap-2">
          <Layers className="w-5 h-5 text-purple-400" /> İçerik Çoklu Platform Adaptasyonu
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Başlık *</label>
            <input
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              placeholder="Yapay Zeka Rehberi 2026"
              value={form.title}
              onChange={e => setForm(f => ({ ...f, title: e.target.value }))}
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Niş</label>
            <select
              title="Niş seçin"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              value={form.niche}
              onChange={e => setForm(f => ({ ...f, niche: e.target.value }))}
            >
              {['technology', 'business', 'education', 'entertainment', 'gaming'].map(n => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Anahtar Kelimeler</label>
            <input
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              placeholder="yapay zeka, AI, 2026"
              value={form.keywords}
              onChange={e => setForm(f => ({ ...f, keywords: e.target.value }))}
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">YouTube URL</label>
            <input
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              placeholder="https://youtube.com/watch?v=..."
              value={form.youtube_url}
              onChange={e => setForm(f => ({ ...f, youtube_url: e.target.value }))}
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm text-gray-400 mb-1">Senaryo Özeti</label>
            <textarea
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm h-20 resize-none"
              placeholder="Video senaryosunu buraya girin..."
              value={form.script}
              onChange={e => setForm(f => ({ ...f, script: e.target.value }))}
            />
          </div>
        </div>
        <button
          onClick={runAdaptation}
          disabled={!form.title || loading}
          className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-600 text-white font-bold rounded-lg hover:from-purple-600 hover:to-pink-700 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
        >
          {loading ? (
            <><div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /><span>Adapte ediliyor...</span></>
          ) : (
            <><Globe className="w-4 h-4" /><span>5 Platforma Adapte Et</span></>
          )}
        </button>
      </div>

      {/* Platform Results */}
      {result?.result?.adaptations && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(result.result.adaptations).map(([platform, data]: [string, any]) => {
            const Icon = platformIcons[platform] || Globe;
            const colorClass = platformColors[platform] || 'text-gray-400';
            const isActive = activeAdapt === platform;
            return (
              <motion.div
                key={platform}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden"
              >
                <button
                  className="w-full p-4 flex items-center justify-between text-left hover:bg-gray-700/50 transition-colors"
                  onClick={() => setActiveAdapt(isActive ? null : platform)}
                >
                  <div className="flex items-center gap-3">
                    <Icon className={`w-5 h-5 ${colorClass}`} />
                    <span className="font-medium text-sm">{data.platform}</span>
                  </div>
                  <ChevronRight className={`w-4 h-4 transition-transform ${isActive ? 'rotate-90' : ''}`} />
                </button>
                {isActive && (
                  <div className="px-4 pb-4 text-xs text-gray-300 space-y-2">
                    {data.hook && <div><span className="text-gray-500">Hook: </span>{data.hook}</div>}
                    {data.caption_variations?.[0] && <div><span className="text-gray-500">Caption: </span>{data.caption_variations[0]}</div>}
                    {data.hashtags && <div className="flex flex-wrap gap-1 mt-2">{data.hashtags.slice(0, 5).map((h: string) => <span key={h} className="bg-gray-700 px-2 py-0.5 rounded text-gray-300">{h}</span>)}</div>}
                    {data.production_notes && (
                      <ul className="mt-2 space-y-1">
                        {data.production_notes.slice(0, 3).map((n: string, i: number) => (
                          <li key={i} className="text-gray-400">• {n}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
}

// ─── Tab: Persona Vault ─────────────────────────────────────────────────────

function PersonaVaultTab() {
  const [trustScores, setTrustScores] = useState<Record<string, number>>({});
  const [lurkerForm, setLurkerForm] = useState({ persona_id: '', niche: 'technology', duration_minutes: 15 });
  const [lurkerResult, setLurkerResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchTrustScores = useCallback(async () => {
    try {
      const res = await fetch(`${API}/api/empire/lurker/trust-scores`);
      const data = await res.json();
      if (data.success) setTrustScores(data.trust_scores);
    } catch { /* noop */ }
  }, []);

  useEffect(() => { fetchTrustScores(); }, [fetchTrustScores]);

  const runLurker = async () => {
    if (!lurkerForm.persona_id) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/empire/lurker/run-session`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(lurkerForm)
      });
      const data = await res.json();
      setLurkerResult(data);
      await fetchTrustScores();
    } catch { setLurkerResult({ success: false }); }
    finally { setLoading(false); }
  };

  // Mock personas
  const mockPersonas = [
    { id: 'TechWizard_TR', niche: 'technology', avatar: '🧙', trust: trustScores['TechWizard_TR'] ?? 6.2 },
    { id: 'BusinessGuru_TR', niche: 'business', avatar: '👨‍💼', trust: trustScores['BusinessGuru_TR'] ?? 7.8 },
    { id: 'ProGamer_TR', niche: 'gaming', avatar: '🎮', trust: trustScores['ProGamer_TR'] ?? 5.1 },
    { id: 'Hazal_K', niche: 'entertainment', avatar: '😎', trust: trustScores['Hazal_K'] ?? 8.5 },
    { id: 'Elif_M', niche: 'education', avatar: '📚', trust: trustScores['Elif_M'] ?? 7.2 },
    { id: 'CodeNinja_TR', niche: 'technology', avatar: '🥷', trust: trustScores['CodeNinja_TR'] ?? 6.9 },
  ];

  return (
    <div className="space-y-6">
      {/* Persona Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {mockPersonas.map(persona => (
          <div
            key={persona.id}
            className="bg-gray-800 rounded-xl p-4 border border-gray-700 text-center cursor-pointer hover:border-gray-500 transition-colors"
            onClick={() => setLurkerForm(f => ({ ...f, persona_id: persona.id, niche: persona.niche }))}
          >
            <div className="text-3xl mb-2">{persona.avatar}</div>
            <div className="text-xs font-medium mb-1">{persona.id}</div>
            <div className="text-xs text-gray-500 mb-2">{persona.niche}</div>
            <div className="text-sm font-bold text-blue-400">{persona.trust.toFixed(1)}/10</div>
            <div className="text-xs text-gray-500">Trust Skoru</div>
            <div className="mt-2 w-full bg-gray-700 rounded-full h-1">
              <div className={`h-1 bg-blue-500 rounded-full ${trustWidthClass(persona.trust)}`} />
            </div>
          </div>
        ))}
      </div>

      {/* Lurker Session */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-bold mb-5 flex items-center gap-2">
          <Eye className="w-5 h-5 text-green-400" /> Lurker Protokolü — Organik Güven İnşası
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Persona ID</label>
            <input
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              placeholder="TechWizard_TR"
              value={lurkerForm.persona_id}
              onChange={e => setLurkerForm(f => ({ ...f, persona_id: e.target.value }))}
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Niş</label>
            <select
              title="Niş seçin"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              value={lurkerForm.niche}
              onChange={e => setLurkerForm(f => ({ ...f, niche: e.target.value }))}
            >
              {['technology', 'business', 'education', 'gaming', 'entertainment'].map(n => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Süre (dk)</label>
            <input
              type="number"
              title="Oturum süresi (dakika)"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              value={lurkerForm.duration_minutes}
              onChange={e => setLurkerForm(f => ({ ...f, duration_minutes: +e.target.value }))}
              min={5} max={60}
            />
          </div>
        </div>
        <button
          onClick={runLurker}
          disabled={!lurkerForm.persona_id || loading}
          className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition-all disabled:opacity-50 flex items-center gap-2"
        >
          {loading ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <Eye className="w-4 h-4" />}
          <span>Lurker Oturumu Başlat</span>
        </button>

        {lurkerResult?.result && (
          <div className="mt-4 p-4 bg-gray-700/50 rounded-lg text-sm space-y-1">
            <div className="flex justify-between">
              <span className="text-gray-400">Eylem sayısı</span>
              <span>{lurkerResult.result.session_result?.actions_performed}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Trust Delta</span>
              <span className="text-green-400">+{lurkerResult.result.session_result?.trust_delta?.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Yeni Trust Skoru</span>
              <span className="text-blue-400">{lurkerResult.result.session_result?.new_trust_score?.toFixed(2)}/10</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Tab: Espionage ─────────────────────────────────────────────────────────

function EspionageTab() {
  const [spyForm, setSpyForm] = useState({ target_channel: '', niche: 'technology', depth: 'standard' });
  const [thumbForm, setThumbForm] = useState({ niche: 'technology', sample_count: 20 });
  const [spyResult, setSpyResult] = useState<any>(null);
  const [thumbResult, setThumbResult] = useState<any>(null);
  const [loadingSpy, setLoadingSpy] = useState(false);
  const [loadingThumb, setLoadingThumb] = useState(false);

  const runSpy = async () => {
    if (!spyForm.target_channel) return;
    setLoadingSpy(true);
    try {
      const res = await fetch(`${API}/api/empire/spy/analyze`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(spyForm)
      });
      setSpyResult(await res.json());
    } catch { setSpyResult({ success: false }); }
    finally { setLoadingSpy(false); }
  };

  const runThumb = async () => {
    setLoadingThumb(true);
    try {
      const res = await fetch(`${API}/api/omniverse/thumbnail-analyzer/analyze`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(thumbForm)
      });
      setThumbResult(await res.json());
    } catch { setThumbResult({ success: false }); }
    finally { setLoadingThumb(false); }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Spy Agent */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-bold mb-5 flex items-center gap-2">
          <Crosshair className="w-5 h-5 text-yellow-400" /> Rakip Espiyonajı
        </h3>
        <div className="space-y-3">
          <input
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
            placeholder="Kanal ID: UCxxxxxxx"
            value={spyForm.target_channel}
            onChange={e => setSpyForm(f => ({ ...f, target_channel: e.target.value }))}
          />
          <div className="grid grid-cols-2 gap-3">
            <select
              title="Niş seçin"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              value={spyForm.niche}
              onChange={e => setSpyForm(f => ({ ...f, niche: e.target.value }))}
            >
              {['technology', 'business', 'education', 'gaming', 'entertainment'].map(n => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
            <select
              title="Analiz derinliği seçin"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              value={spyForm.depth}
              onChange={e => setSpyForm(f => ({ ...f, depth: e.target.value }))}
            >
              <option value="standard">Standart</option>
              <option value="deep">Derin</option>
            </select>
          </div>
          <button
            onClick={runSpy}
            disabled={!spyForm.target_channel || loadingSpy}
            className="w-full py-2 bg-yellow-600 hover:bg-yellow-700 text-white font-bold rounded-lg disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loadingSpy ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <Search className="w-4 h-4" />}
            <span>Espiyonaj Başlat</span>
          </button>

          {spyResult?.spy_intelligence && (
            <div className="mt-2 space-y-2 text-sm">
              <div className="flex justify-between bg-gray-700/50 rounded p-2">
                <span className="text-gray-400">Fırsat Skoru</span>
                <span className="text-yellow-400 font-bold">{spyResult.spy_intelligence.opportunity_score?.toFixed(1)}/10</span>
              </div>
              <div className="bg-gray-700/50 rounded p-2">
                <p className="text-gray-400 mb-1">İçerik Boşlukları</p>
                {spyResult.spy_intelligence.content_gaps?.slice(0, 3).map((gap: string, i: number) => (
                  <p key={i} className="text-xs text-gray-300">• {gap}</p>
                ))}
              </div>
              <div className="bg-gray-700/50 rounded p-2">
                <p className="text-gray-400 mb-1">Başarılı Stratejiler</p>
                {spyResult.spy_intelligence.successful_strategies?.slice(0, 3).map((s: string, i: number) => (
                  <p key={i} className="text-xs text-gray-300">• {s}</p>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Thumbnail Analyzer */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-bold mb-5 flex items-center gap-2">
          <Image className="w-5 h-5 text-pink-400" /> Thumbnail Renk Gap Analizi
        </h3>
        <div className="space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <select
              title="Niş seçin"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              value={thumbForm.niche}
              onChange={e => setThumbForm(f => ({ ...f, niche: e.target.value }))}
            >
              {['technology', 'business', 'education', 'gaming', 'entertainment'].map(n => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
            <input
              type="number"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm"
              placeholder="Örnek sayısı"
              value={thumbForm.sample_count}
              onChange={e => setThumbForm(f => ({ ...f, sample_count: +e.target.value }))}
              min={5} max={50}
            />
          </div>
          <button
            onClick={runThumb}
            disabled={loadingThumb}
            className="w-full py-2 bg-pink-600 hover:bg-pink-700 text-white font-bold rounded-lg disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loadingThumb ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <Image className="w-4 h-4" />}
            <span>Renk Analizi Başlat</span>
          </button>

          {thumbResult?.analysis && (
            <div className="mt-2 space-y-2 text-sm">
              <div className="flex justify-between bg-gray-700/50 rounded p-2">
                <span className="text-gray-400">Hakimiyet Skoru</span>
                <span className="text-pink-400 font-bold">{thumbResult.analysis.visual_dominance_score?.toFixed(1)}/10</span>
              </div>
              {thumbResult.analysis.winning_palette && (
                <div className="bg-gray-700/50 rounded p-2">
                  <p className="text-gray-400 mb-2 text-xs">Önerilen Palette</p>
                  <div className="flex gap-2">
                    {Object.entries(thumbResult.analysis.winning_palette)
                      .filter(([k]) => ['primary', 'secondary', 'accent', 'background', 'text'].includes(k))
                      .map(([key, color]: [string, any]) => (
                        <div key={key} className="text-center">
                          <div
                            className={`w-8 h-8 rounded border border-gray-600 mx-auto mb-1 bg-[${color}]`}
                          />
                          <span className="text-xs text-gray-500">{key.slice(0, 3)}</span>
                        </div>
                      ))}
                  </div>
                </div>
              )}
              <div className="bg-gray-700/50 rounded p-2">
                {thumbResult.analysis.design_recommendations?.slice(0, 3).map((r: string, i: number) => (
                  <p key={i} className="text-xs text-gray-300">• {r}</p>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Tab: Analytics ─────────────────────────────────────────────────────────

function AnalyticsTab() {
  const [performanceData, setPerformanceData] = useState<any>(null);
  const [devopsHealth, setDevopsHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [perfRes, devopsRes] = await Promise.all([
          fetch(`${API}/api/empire/metrics/performance`).catch(() => null),
          fetch(`${API}/api/empire/devops/health`).catch(() => null)
        ]);
        if (perfRes?.ok) setPerformanceData(await perfRes.json());
        if (devopsRes?.ok) setDevopsHealth(await devopsRes.json());
      } catch { /* noop */ }
      finally { setLoading(false); }
    };
    fetchData();
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, []);

  const kpiCards = [
    { label: 'Toplam Kanal', value: performanceData?.empire_metrics?.total_channels ?? 8, icon: Globe, color: 'blue' },
    { label: 'Aktif Kampanya', value: performanceData?.empire_metrics?.active_campaigns ?? 12, icon: Radio, color: 'green' },
    { label: 'Aylık Gelir', value: `$${(performanceData?.empire_metrics?.monthly_revenue ?? 12840).toLocaleString()}`, icon: TrendingUp, color: 'yellow' },
    { label: 'Hata Sayısı', value: devopsHealth?.health_report?.total_unique_errors ?? 0, icon: AlertTriangle, color: 'red' },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {kpiCards.map(kpi => (
          <div key={kpi.label} className="bg-gray-800 rounded-xl p-5 border border-gray-700">
            <div className="flex items-center gap-2 mb-2">
              <kpi.icon className={`w-5 h-5 text-${kpi.color}-400`} />
              <span className="text-gray-400 text-sm">{kpi.label}</span>
            </div>
            <div className="text-2xl font-bold">{loading ? '...' : kpi.value}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* DevOps Health */}
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5 text-green-400" /> DevOps Sağlık
          </h3>
          {devopsHealth?.health_report ? (
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Toplam Hata Olayı</span>
                <span>{devopsHealth.health_report.total_error_events}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Kara Listedeki</span>
                <span className={devopsHealth.health_report.blacklisted_count > 0 ? 'text-red-400' : 'text-green-400'}>
                  {devopsHealth.health_report.blacklisted_count}
                </span>
              </div>
              {devopsHealth.health_report.top_errors?.slice(0, 3).map((err: any, i: number) => (
                <div key={i} className="bg-gray-700/50 rounded p-2 text-xs">
                  <div className="flex justify-between mb-1">
                    <span className="text-gray-300">{err.module}</span>
                    <span className={`${err.occurrences >= 3 ? 'text-red-400' : 'text-yellow-400'}`}>
                      x{err.occurrences}
                    </span>
                  </div>
                  <span className="text-gray-500">{err.error?.slice(0, 60)}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              {loading ? <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto" /> : 'Veri yüklenemedi'}
            </div>
          )}
        </div>

        {/* Agent Performance */}
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-blue-400" /> Ajan Performansı
          </h3>
          {performanceData?.agent_performance?.all_agents ? (
            <div className="space-y-3">
              {Object.entries(performanceData.agent_performance.all_agents).map(([agent, data]: [string, any]) => (
                <div key={agent} className="flex items-center justify-between text-sm">
                  <span className="text-gray-300 capitalize">{agent.replace('_agent', '')}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-gray-400 text-xs">{data.average_confidence?.toFixed(0) ?? '—'}% güven</span>
                    <StatusBadge status={data.health_status ?? 'idle'} />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              {loading ? <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto" /> : 'Veri yüklenemedi'}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Tab: Revenue Maximization ────────────────────────────────────────────────

function RevenueTab() {
  const [abTestForm, setAbTestForm] = useState({
    video_id: '',
    base_title: '',
    niche: 'technology',
    primary_keyword: ''
  });
  const [abTestResult, setAbTestResult] = useState<any>(null);
  const [revenueReport, setRevenueReport] = useState<any>(null);
  const [affiliateOpportunities, setAffiliateOpportunities] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const createABTest = async () => {
    if (!abTestForm.video_id || !abTestForm.base_title) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/omniverse/revenue/ab-test/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(abTestForm)
      });
      const data = await res.json();
      setAbTestResult(data);
    } catch { setAbTestResult({ success: false, error: 'Bağlantı hatası' }); }
    finally { setLoading(false); }
  };

  const detectAffiliate = async () => {
    if (!abTestForm.video_id) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/omniverse/revenue/detect-affiliate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          video_id: abTestForm.video_id,
          transcript: `Bu video ${abTestForm.primary_keyword} hakkında. ${abTestForm.base_title}`,
          description: abTestForm.base_title
        })
      });
      const data = await res.json();
      if (data.success) {
        setAffiliateOpportunities(data.opportunities || []);
      }
    } catch { /* ignore */ }
    finally { setLoading(false); }
  };

  const loadRevenueReport = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/omniverse/revenue/report/demo_channel`);
      const data = await res.json();
      setRevenueReport(data.report);
    } catch { /* ignore */ }
    finally { setLoading(false); }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* A/B Test Creator */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-bold mb-5 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-emerald-400" /> A/B Title Testi
        </h3>
        <div className="space-y-4">
          <input
            type="text"
            value={abTestForm.video_id}
            onChange={(e) => setAbTestForm({ ...abTestForm, video_id: e.target.value })}
            placeholder="Video ID"
            className="w-full px-3 py-2 bg-gray-700 rounded-lg text-sm"
          />
          <input
            type="text"
            value={abTestForm.base_title}
            onChange={(e) => setAbTestForm({ ...abTestForm, base_title: e.target.value })}
            placeholder="Mevcut başlık"
            className="w-full px-3 py-2 bg-gray-700 rounded-lg text-sm"
          />
          <input
            type="text"
            value={abTestForm.primary_keyword}
            onChange={(e) => setAbTestForm({ ...abTestForm, primary_keyword: e.target.value })}
            placeholder="Ana anahtar kelime"
            className="w-full px-3 py-2 bg-gray-700 rounded-lg text-sm"
          />
          <select
            title="Niş seçin"
            value={abTestForm.niche}
            onChange={(e) => setAbTestForm({ ...abTestForm, niche: e.target.value })}
            className="w-full px-3 py-2 bg-gray-700 rounded-lg text-sm"
          >
            <option value="technology">Teknoloji</option>
            <option value="business">İş & Finans</option>
            <option value="education">Eğitim</option>
            <option value="gaming">Oyun</option>
          </select>
          <div className="flex gap-2">
            <button
              onClick={createABTest}
              disabled={loading}
              className="flex-1 px-4 py-2 bg-emerald-600 rounded-lg text-sm font-medium hover:bg-emerald-500 disabled:opacity-50"
            >
              {loading ? 'Oluşturuluyor...' : 'Test Oluştur'}
            </button>
            <button
              onClick={detectAffiliate}
              disabled={loading}
              className="flex-1 px-4 py-2 bg-blue-600 rounded-lg text-sm font-medium hover:bg-blue-500 disabled:opacity-50"
            >
              Affiliate Bul
            </button>
          </div>
        </div>

        {abTestResult?.success && (
          <div className="mt-4 p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
            <p className="text-sm text-emerald-400 font-medium">✓ Test oluşturuldu: {abTestResult.test_id}</p>
            <div className="mt-2 space-y-1">
              {abTestResult.variants?.map((v: any) => (
                <p key={v.id} className="text-xs text-gray-400">{v.id}: {v.title}</p>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Affiliate Opportunities */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-bold mb-5 flex items-center gap-2">
          <DollarSign className="w-5 h-5 text-green-400" /> Affiliate Fırsatları
        </h3>
        {affiliateOpportunities.length > 0 ? (
          <div className="space-y-3">
            {affiliateOpportunities.map((opp: any, i: number) => (
              <div key={i} className="bg-gray-700/50 rounded-lg p-3">
                <div className="flex items-center gap-2">
                  <div>
                    <p className="text-sm font-medium text-white">{opp.product}</p>
                    <p className="text-xs text-gray-400">{opp.category}</p>
                  </div>
                  <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">
                    {opp.commission}
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-2">Öncelik: {opp.priority}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-500 py-8">
            Affiliate fırsatları için "Affiliate Bul" butonuna tıklayın
          </div>
        )}
      </div>

      {/* Revenue Report */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 lg:col-span-2">
        <div className="flex justify-between items-center mb-5">
          <h3 className="text-lg font-bold flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-purple-400" /> Gelir Raporu
          </h3>
          <button
            onClick={loadRevenueReport}
            disabled={loading}
            className="px-3 py-1.5 bg-purple-600 rounded-lg text-sm hover:bg-purple-500 disabled:opacity-50"
          >
            {loading ? 'Yükleniyor...' : 'Yenile'}
          </button>
        </div>
        {revenueReport ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-700/50 rounded-lg p-4">
              <p className="text-xs text-gray-400 mb-1">A/B Test İyileştirmesi</p>
              <p className="text-2xl font-bold text-emerald-400">
                {revenueReport.ab_testing?.avg_ctr_improvement || '+0%'}
              </p>
              <p className="text-xs text-gray-500">CTR artışı</p>
            </div>
            <div className="bg-gray-700/50 rounded-lg p-4">
              <p className="text-xs text-gray-400 mb-1">Aylık Potansiyel</p>
              <p className="text-2xl font-bold text-green-400">
                {revenueReport.revenue_summary?.optimized_monthly || '0₺'}
              </p>
              <p className="text-xs text-gray-500">Optimize gelir</p>
            </div>
            <div className="bg-gray-700/50 rounded-lg p-4">
              <p className="text-xs text-gray-400 mb-1">İyileştirme</p>
              <p className="text-2xl font-bold text-blue-400">
                {revenueReport.revenue_summary?.improvement || '+0%'}
              </p>
              <p className="text-xs text-gray-500">Genel artış</p>
            </div>
          </div>
        ) : (
          <div className="text-center text-gray-500 py-8">
            Rapor yüklemek için "Yenile" butonuna tıklayın
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Tab: Stealth 4.0 ───────────────────────────────────────────────────────

function StealthTab() {
  const [personaId, setPersonaId] = useState('');
  const [proxyLocation, setProxyLocation] = useState('tr');
  const [stealthProfile, setStealthProfile] = useState<any>(null);
  const [stealthReport, setStealthReport] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const generateProfile = async () => {
    if (!personaId) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/omniverse/stealth/generate-profile/${personaId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ proxy_location: proxyLocation })
      });
      const data = await res.json();
      setStealthProfile(data);
    } catch { setStealthProfile({ success: false, error: 'Bağlantı hatası' }); }
    finally { setLoading(false); }
  };

  const rotateFingerprint = async () => {
    if (!personaId) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/omniverse/stealth/rotate/${personaId}`, {
        method: 'POST'
      });
      const data = await res.json();
      if (data.success) {
        setStealthReport({ rotation: 'success', timestamp: new Date().toISOString() });
      }
    } catch { /* ignore */ }
    finally { setLoading(false); }
  };

  const loadReport = async () => {
    if (!personaId) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/omniverse/stealth/report/${personaId}`);
      const data = await res.json();
      setStealthReport(data.report);
    } catch { /* ignore */ }
    finally { setLoading(false); }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Profile Generator */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-bold mb-5 flex items-center gap-2">
          <Fingerprint className="w-5 h-5 text-red-400" /> Stealth Profil Oluşturucu
        </h3>
        <div className="space-y-4">
          <input
            type="text"
            value={personaId}
            onChange={(e) => setPersonaId(e.target.value)}
            placeholder="Persona ID"
            className="w-full px-3 py-2 bg-gray-700 rounded-lg text-sm"
          />
          <select
            title="Proxy konumu"
            value={proxyLocation}
            onChange={(e) => setProxyLocation(e.target.value)}
            className="w-full px-3 py-2 bg-gray-700 rounded-lg text-sm"
          >
            <option value="tr">Türkiye (Residential)</option>
            <option value="de">Almanya (Residential)</option>
            <option value="us_east">ABD Doğu (Residential)</option>
            <option value="us_west">ABD Batı (Residential)</option>
            <option value="uk">İngiltere (Residential)</option>
            <option value="nl">Hollanda (Residential)</option>
          </select>
          <div className="flex gap-2">
            <button
              onClick={generateProfile}
              disabled={loading}
              className="flex-1 px-4 py-2 bg-red-600 rounded-lg text-sm font-medium hover:bg-red-500 disabled:opacity-50"
            >
              {loading ? 'Oluşturuluyor...' : 'Profil Oluştur'}
            </button>
            <button
              onClick={rotateFingerprint}
              disabled={loading || !personaId}
              className="flex-1 px-4 py-2 bg-orange-600 rounded-lg text-sm font-medium hover:bg-orange-500 disabled:opacity-50"
            >
              Rotasyon Yap
            </button>
          </div>
          <button
            onClick={loadReport}
            disabled={loading || !personaId}
            className="w-full px-4 py-2 bg-gray-600 rounded-lg text-sm font-medium hover:bg-gray-500 disabled:opacity-50"
          >
            Rapor Yükle
          </button>
        </div>

        {stealthProfile?.success && (
          <div className="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
            <p className="text-sm text-red-400 font-medium">✓ Stealth profil aktif</p>
            <div className="mt-2 space-y-1 text-xs text-gray-400">
              <p>WebGL: {stealthProfile.profile?.webgl_vendor?.slice(0, 30)}...</p>
              <p>Timezone: {stealthProfile.profile?.timezone}</p>
              <p>Screen: {stealthProfile.profile?.screen_resolution}</p>
              <p>Fonts: {stealthProfile.profile?.font_count} font</p>
              <p>Hardware: {stealthProfile.profile?.hardware_concurrency} core, {stealthProfile.profile?.device_memory}GB</p>
            </div>
          </div>
        )}
      </div>

      {/* Stealth Report */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-bold mb-5 flex items-center gap-2">
          <Shield className="w-5 h-5 text-green-400" /> Stealth Durumu
        </h3>
        {stealthReport ? (
          <div className="space-y-4">
            {stealthReport.fingerprint_status && (
              <div className="space-y-2">
                <p className="text-sm font-medium text-white">Fingerprint Masking</p>
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(stealthReport.fingerprint_status).map(([key, value]: [string, any]) => (
                    <div key={key} className="flex items-center gap-2 text-xs">
                      <CheckCircle className="w-3 h-3 text-green-400" />
                      <span className="text-gray-400 capitalize">{key.replace('_', ' ')}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {stealthReport.detection_resistance && (
              <div className="space-y-2">
                <p className="text-sm font-medium text-white">Detection Resistance</p>
                <div className="space-y-1">
                  {Object.entries(stealthReport.detection_resistance).map(([key, value]: [string, any]) => (
                    <div key={key} className="flex justify-between text-xs">
                      <span className="text-gray-400">{key}</span>
                      <span className={value === 'resistant' ? 'text-green-400' : 'text-yellow-400'}>{value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {stealthReport.current_profile_summary && (
              <div className="bg-gray-700/50 rounded-lg p-3">
                <p className="text-xs text-gray-400 mb-2">Profil Özeti</p>
                <p className="text-xs text-gray-300">{stealthReport.current_profile_summary.hardware}</p>
                <p className="text-xs text-gray-300">{stealthReport.current_profile_summary.screen}</p>
                <p className="text-xs text-gray-300">{stealthReport.current_profile_summary.timezone}</p>
              </div>
            )}
            {stealthReport.rotation_recommended && (
              <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-2">
                <p className="text-xs text-yellow-400">⚠️ Fingerprint rotasyonu önerilir</p>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center text-gray-500 py-8">
            Stealth raporu için "Rapor Yükle" butonuna tıklayın
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Main Page ──────────────────────────────────────────────────────────────

export default function OmniversePage() {
  const [activeTab, setActiveTab] = useState('production');

  const tabComponents: Record<string, JSX.Element> = {
    production: <ProductionTab />,
    multiverse: <MultiverseTab />,
    persona: <PersonaVaultTab />,
    espionage: <EspionageTab />,
    revenue: <RevenueTab />,
    stealth: <StealthTab />,
    analytics: <AnalyticsTab />,
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl shadow-lg">
              <Globe className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-black bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                VUC-2026 Omniverse
              </h1>
              <p className="text-gray-400 text-sm">Multi-Platform Medya İmparatorluğu</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-2 px-3 py-1.5 bg-green-500/20 rounded-lg">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-xs text-green-400 font-medium">Canlı</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Tabs */}
      <div className="flex space-x-1 mb-6 bg-gray-800/50 p-1 rounded-xl border border-gray-700 overflow-x-auto">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${
              activeTab === tab.id
                ? `bg-gray-700 text-${tab.color}-400 shadow-sm`
                : 'text-gray-400 hover:text-gray-200 hover:bg-gray-700/50'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.15 }}
        >
          {tabComponents[activeTab]}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
