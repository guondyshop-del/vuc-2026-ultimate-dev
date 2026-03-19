'use client';

import { useState, useEffect } from 'react';
import { getStatusColor, getStatusBg, getWidthClass } from '@/lib/styles';
import { motion } from 'framer-motion';
import { 
  User, 
  Shield, 
  Globe, 
  Smartphone, 
  Monitor, 
  Zap, 
  Eye,
  AlertCircle,
  CheckCircle,
  Settings,
  RefreshCw,
  Activity,
  Fingerprint,
  Lock
} from 'lucide-react';

export default function PersonaVault() {
  const [personas, setPersonas] = useState([
    {
      id: 1,
      name: 'Hazal',
      niche: 'Teknoloji',
      proxy: 'Moldova',
      status: 'active',
      health: 94,
      fingerprint: 'iPhone 15 Pro Max',
      lastActivity: '2 dakika önce',
      platforms: ['youtube', 'tiktok', 'instagram'],
      riskLevel: 'low'
    },
    {
      id: 2,
      name: 'Elif',
      niche: 'Eğitim',
      proxy: 'İzlanda',
      status: 'active',
      health: 87,
      fingerprint: 'Sony A7S III',
      lastActivity: '5 dakika önce',
      platforms: ['youtube', 'instagram'],
      riskLevel: 'low'
    },
    {
      id: 3,
      name: 'Zeynep',
      niche: 'İş',
      proxy: 'Almanya',
      status: 'warning',
      health: 72,
      fingerprint: 'MacBook Pro M3',
      lastActivity: '15 dakika önce',
      platforms: ['tiktok', 'facebook'],
      riskLevel: 'medium'
    }
  ]);

  const [proxyHealth, setProxyHealth] = useState([
    { location: 'Moldova', status: 'healthy', responseTime: '45ms', uptime: '99.8%' },
    { location: 'İzlanda', status: 'healthy', responseTime: '52ms', uptime: '99.5%' },
    { location: 'Almanya', status: 'warning', responseTime: '89ms', uptime: '97.2%' },
    { location: 'Hollanda', status: 'healthy', responseTime: '38ms', uptime: '99.9%' },
    { location: 'ABD', status: 'healthy', responseTime: '67ms', uptime: '98.7%' }
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setPersonas(prev => prev.map(persona => ({
        ...persona,
        health: Math.max(0, Math.min(100, persona.health + (Math.random() - 0.5) * 5))
      })));
      
      setProxyHealth(prev => prev.map(proxy => ({
        ...proxy,
        responseTime: Math.max(20, Math.min(200, parseInt(proxy.responseTime) + (Math.random() - 0.5) * 10)) + 'ms'
      })));
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
      case 'healthy': return 'text-green-400';
      case 'warning': return 'text-yellow-400';
      case 'error':
      case 'offline': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'active':
      case 'healthy': return 'bg-green-500/20';
      case 'warning': return 'bg-yellow-500/20';
      case 'error':
      case 'offline': return 'bg-red-500/20';
      default: return 'bg-gray-500/20';
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'text-green-400';
      case 'medium': return 'text-yellow-400';
      case 'high': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getHealthColor = (health: number) => {
    if (health >= 90) return 'text-green-400';
    if (health >= 70) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getHealthBg = (health: number) => {
    if (health >= 90) return 'bg-green-500/20';
    if (health >= 70) return 'bg-yellow-500/20';
    return 'bg-red-500/20';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">👤 Persona Vault</h2>
          <p className="text-gray-400">Proxy health + Device fingerprint management</p>
        </div>
        <div className="flex items-center space-x-2">
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-medium transition-colors flex items-center gap-2">
            <User className="w-4 h-4" />
            Yeni Persona
          </button>
          <button className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-white font-medium transition-colors flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            Tümünü Yenile
          </button>
        </div>
      </div>

      {/* Active Personas */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {personas.map((persona) => (
          <div key={persona.id} className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-full flex items-center justify-center">
                  <User className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">{persona.name}</h3>
                  <p className="text-sm text-gray-400">{persona.niche}</p>
                </div>
              </div>
              <div className={`px-2 py-1 rounded ${getStatusBg(persona.status)} ${getStatusColor(persona.status)} text-xs`}>
                {persona.status === 'active' ? 'Aktif' : persona.status === 'warning' ? 'Uyarı' : 'Offline'}
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Proxy</span>
                <div className="flex items-center gap-2">
                  <Globe className="w-4 h-4 text-blue-400" />
                  <span className="text-sm text-white">{persona.proxy}</span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Sağlık</span>
                <div className="flex items-center gap-2">
                  <div className="w-16 bg-gray-700 rounded-full h-2">
                    <div 
                      className={`${getHealthColor(persona.health)} h-2 rounded-full transition-all duration-500 ${getWidthClass(persona.health)}`}
                    />
                  </div>
                  <span className={`text-xs ${getHealthColor(persona.health)}`}>{persona.health}%</span>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Fingerprint</span>
                <div className="flex items-center gap-2">
                  <Fingerprint className="w-4 h-4 text-purple-400" />
                  <span className="text-xs text-white">{persona.fingerprint}</span>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Risk Level</span>
                <span className={`text-xs font-medium ${getRiskColor(persona.riskLevel)}`}>
                  {persona.riskLevel === 'low' ? 'Düşük' : persona.riskLevel === 'medium' ? 'Orta' : 'Yüksek'}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Son Aktivite</span>
                <span className="text-xs text-gray-400">{persona.lastActivity}</span>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-700">
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">Platformlar</span>
                <div className="flex items-center gap-2">
                  {persona.platforms.map((platform) => (
                    <div key={platform} className="w-6 h-6 bg-gray-700 rounded flex items-center justify-center">
                      <span className="text-xs text-gray-400">
                        {platform === 'youtube' ? 'YT' : 
                         platform === 'tiktok' ? 'TT' : 
                         platform === 'instagram' ? 'IG' : 
                         platform === 'facebook' ? 'FB' : 'X'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="mt-4 flex items-center gap-2">
              <button className="flex-1 px-3 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white text-sm transition-colors">
                <Settings className="w-3 h-3 inline mr-1" />
                Ayarlar
              </button>
              <button className="flex-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white text-sm transition-colors">
                <Activity className="w-3 h-3 inline mr-1" />
                İzle
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Proxy Health Dashboard */}
      <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Shield className="w-5 h-5 text-green-400" />
          Proxy Sağlık Dashboard
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {proxyHealth.map((proxy, index) => (
            <div key={index} className="bg-gray-900/50 rounded-lg p-4 border border-gray-600">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Globe className="w-4 h-4 text-blue-400" />
                  <span className="text-sm font-medium text-white">{proxy.location}</span>
                </div>
                <div className={`w-2 h-2 rounded-full ${
                  proxy.status === 'healthy' ? 'bg-green-400' : 
                  proxy.status === 'warning' ? 'bg-yellow-400' : 'bg-red-400'
                }`} />
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-400">Response</span>
                  <span className="text-xs text-white">{proxy.responseTime}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-400">Uptime</span>
                  <span className="text-xs text-white">{proxy.uptime}</span>
                </div>
              </div>

              <div className={`mt-3 px-2 py-1 rounded text-center text-xs ${
                proxy.status === 'healthy' ? 'bg-green-500/20 text-green-400' : 
                proxy.status === 'warning' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-red-500/20 text-red-400'
              }`}>
                {proxy.status === 'healthy' ? 'Sağlıklı' : proxy.status === 'warning' ? 'Uyarı' : 'Hata'}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Stealth 4.0 Features */}
      <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-xl p-6 border border-green-500/30">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Lock className="w-5 h-5 text-green-400" />
          Stealth 4.0 Aktif Özellikler
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600">
            <Fingerprint className="w-6 h-6 text-green-400 mb-2" />
            <div className="text-sm text-white font-medium">Device Fingerprint</div>
            <div className="text-xs text-gray-400">Canvas/WebGPU spoofing</div>
            <div className="mt-2 flex items-center gap-1">
              <CheckCircle className="w-3 h-3 text-green-400" />
              <span className="text-xs text-green-400">Aktif</span>
            </div>
          </div>
          
          <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600">
            <Eye className="w-6 h-6 text-blue-400 mb-2" />
            <div className="text-sm text-white font-medium">Human Interaction</div>
            <div className="text-xs text-gray-400">Scroll/like patterns</div>
            <div className="mt-2 flex items-center gap-1">
              <CheckCircle className="w-3 h-3 text-green-400" />
              <span className="text-xs text-green-400">Aktif</span>
            </div>
          </div>
          
          <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600">
            <Zap className="w-6 h-6 text-purple-400 mb-2" />
            <div className="text-sm text-white font-medium">Pixel Noise</div>
            <div className="text-xs text-gray-400">MD5 hash bypass</div>
            <div className="mt-2 flex items-center gap-1">
              <CheckCircle className="w-3 h-3 text-green-400" />
              <span className="text-xs text-green-400">Aktif</span>
            </div>
          </div>
          
          <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600">
            <Smartphone className="w-6 h-6 text-yellow-400 mb-2" />
            <div className="text-sm text-white font-medium">FPS Jitter</div>
            <div className="text-xs text-gray-400">Micro-variation ±0.001</div>
            <div className="mt-2 flex items-center gap-1">
              <CheckCircle className="w-3 h-3 text-green-400" />
              <span className="text-xs text-green-400">Aktif</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
