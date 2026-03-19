'use client';

import { motion } from 'framer-motion';
import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  Home, 
  Brain, 
  Users, 
  Database, 
  Settings,
  BarChart3,
  Globe,
  Video,
  Upload,
  Search,
  Eye,
  Menu,
  X,
  Zap,
  TrendingUp,
  Shield,
  Type
} from 'lucide-react';
import EmpireReadinessScore from './EmpireReadinessScore';

const navigation = [
  { name: 'Ana Sayfa', href: '/', icon: Home },
  { name: 'Savaş Odası', href: '/war-room', icon: TrendingUp },
  { name: 'AI Senaryo', href: '/ai-script', icon: Brain },
  { name: 'Rakip Analiz', href: '/competitor-analysis', icon: Search },
  { name: 'Video Render', href: '/video-render', icon: Video },
  { name: 'Sistem Monitor', href: '/system-monitor', icon: Shield },
  { name: 'Türkçe Font', href: '/turkish-font-test', icon: Type, description: 'Türkçe Karakter Desteği' },
  { name: 'Omniverse', href: '/omniverse', icon: Shield, description: 'Multi-Platform İmparatorluğu' },
  { name: 'Empire Control', href: '/empire', icon: Brain, description: 'Neural Architecture' },
  { name: 'Kanallar', href: '/channels', icon: Globe, description: 'Kanal Yönetimi' },
  { name: 'Sistem Belleği', href: '/memory', icon: Database, description: 'Analytics Vault' },
  { name: 'Windows AI', href: '/windows-ai', icon: Zap, description: 'Yerel AI Servisleri' },
];

export default function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const pathname = usePathname();

  return (
    <>
      {/* Desktop Navigation */}
      <nav className="hidden lg:block">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gray-900/50 backdrop-blur-lg border-b border-gray-800"
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              {/* Logo */}
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-white">ONX</h1>
                  <p className="text-xs text-gray-400">Neural Empire Manager</p>
                </div>
              </div>

              {/* Navigation Links */}
              <div className="hidden lg:block">
                <div className="flex items-center space-x-1">
                  {navigation.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                      <Link
                        key={item.name}
                        href={item.href}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                          isActive
                            ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                            : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
                        }`}
                      >
                        <div className="flex items-center space-x-2">
                          <item.icon className="w-4 h-4" />
                          <span>{item.name}</span>
                        </div>
                      </Link>
                    );
                  })}
                </div>
              </div>

              {/* Status Indicators */}
              <div className="flex items-center space-x-4">
                <EmpireReadinessScore />
                <div className="flex items-center space-x-2 px-3 py-1 bg-green-500/20 rounded-lg">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-xs text-green-400 font-medium">Sistem Aktif</span>
                </div>
                <div className="flex items-center space-x-2 px-3 py-1 bg-blue-500/20 rounded-lg">
                  <Zap className="w-3 h-3 text-blue-400" />
                  <span className="text-xs text-blue-400 font-medium">95% Otonom</span>
                </div>
                <div className="flex items-center space-x-2 px-3 py-1 bg-purple-500/20 rounded-lg">
                  <TrendingUp className="w-3 h-3 text-purple-400" />
                  <span className="text-xs text-purple-400 font-medium">+300% Büyüme</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </nav>

      {/* Mobile Navigation */}
      <nav className="lg:hidden">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gray-900/50 backdrop-blur-lg border-b border-gray-800"
        >
          <div className="px-4 sm:px-6">
            <div className="flex items-center justify-between h-16">
              {/* Logo */}
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-white">ONX</h1>
                  <p className="text-xs text-gray-400">Neural Empire</p>
                </div>
              </div>

              {/* Mobile menu button */}
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
              >
                {mobileMenuOpen ? (
                  <X className="w-6 h-6 text-white" />
                ) : (
                  <Menu className="w-6 h-6 text-white" />
                )}
              </button>
            </div>
          </div>

          {/* Mobile menu */}
          {mobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="border-t border-gray-800"
            >
              <div className="px-4 py-4 space-y-2">
                {navigation.map((item) => {
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`block px-4 py-3 rounded-lg text-sm font-medium transition-all ${
                        isActive
                          ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                          : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <item.icon className="w-5 h-5" />
                        <div>
                          <div>{item.name}</div>
                          <div className="text-xs text-gray-500">{item.description}</div>
                        </div>
                      </div>
                    </Link>
                  );
                })}
              </div>

              {/* Mobile Status */}
              <div className="px-4 py-4 border-t border-gray-800 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-sm text-green-400">Sistem Aktif</span>
                  </div>
                  <span className="text-xs text-gray-500">24/7</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Zap className="w-4 h-4 text-blue-400" />
                    <span className="text-sm text-blue-400">Otonom</span>
                  </div>
                  <span className="text-xs text-gray-500">95%</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <TrendingUp className="w-4 h-4 text-purple-400" />
                    <span className="text-sm text-purple-400">Büyüme</span>
                  </div>
                  <span className="text-xs text-gray-500">+300%</span>
                </div>
              </div>
            </motion.div>
          )}
        </motion.div>
      </nav>

      {/* Breadcrumb Navigation */}
      {pathname !== '/' && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-gray-800/50 backdrop-blur-sm border-b border-gray-700"
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center h-12 space-x-2 text-sm">
              <Link
                href="/"
                className="text-gray-400 hover:text-white transition-colors"
              >
                <Home className="w-4 h-4" />
              </Link>
              <span className="text-gray-600">/</span>
              {navigation
                .find(item => item.href === pathname)
                ?.name || 'Sayfa'}
            </div>
          </div>
        </motion.div>
      )}
    </>
  );
}
