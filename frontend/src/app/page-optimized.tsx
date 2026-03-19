import { Suspense } from 'react';
import { motion } from 'framer-motion';
import { 
  Play, 
  BarChart3, 
  Users, 
  TrendingUp, 
  Settings, 
  Zap,
  Shield,
  Eye,
  Upload,
  Brain,
  Globe
} from 'lucide-react';
import LoadingSpinner from '@/components/ui/loading-spinner';

// Server Component for system status
async function getSystemStatus() {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/health`, {
      cache: 'no-store',
      next: { revalidate: 30 }
    });
    
    if (response.ok) {
      const data = await response.json();
      return {
        backend: data.status === 'healthy' ? 'active' : 'error',
        redis: data.redis === 'connected' ? 'active' : 'error',
        ai: data.database === 'connected' ? 'active' : 'active'
      };
    }
  } catch (error) {
    console.error('System status check failed:', error);
  }
  
  return {
    backend: 'error',
    redis: 'error',
    ai: 'error'
  };
}

// Server Component for stats
async function getSystemStats() {
  // Simulate fetching stats from API
  return [
    { label: 'Aktif Kanal', value: '3', icon: Globe },
    { label: 'Üretilen Video', value: '127', icon: Play },
    { label: 'Toplam İzlenme', value: '2.4M', icon: Eye },
    { label: 'Aylık Büyüme', value: '+34%', icon: TrendingUp }
  ];
}

// Server Component for Features
function FeaturesGrid() {
  const features = [
    {
      icon: Brain,
      title: 'AI Senaryo Üretimi',
      description: 'Gemini 2.0 Pro ile viral senaryolar otomatik olarak üretilir',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: Play,
      title: 'Otomatik Video Üretim',
      description: 'Konseptten yayına kadar tam otomatik video üretim hattı',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Users,
      title: 'Rakip Casusluğu',
      description: 'yt-dlp ile rakipleri analiz et, fırsatları yakala',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: Shield,
      title: 'Algoritma Kalkanı',
      description: 'Grey-Hat tekniklerle YouTube filtrelerini baypas et',
      color: 'from-red-500 to-orange-500'
    },
    {
      icon: BarChart3,
      title: 'Analytics Dashboard',
      description: 'Gerçek zamanlı performans takibi ve optimizasyon',
      color: 'from-yellow-500 to-amber-500'
    },
    {
      icon: Upload,
      title: 'Otomatik Yükleme',
      description: 'Planlı içerik takvimi ile otomatik video yükleme',
      color: 'from-indigo-500 to-purple-500'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {features.map((feature, index) => (
        <motion.div
          key={feature.title}
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: index * 0.1 }}
          className="glass-effect rounded-xl p-8 card-hover group"
        >
          <div className={`w-16 h-16 rounded-lg bg-gradient-to-r ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
            <feature.icon className="w-8 h-8 text-white" />
          </div>
          <h3 className="text-xl font-bold mb-4">{feature.title}</h3>
          <p className="text-gray-400 leading-relaxed">{feature.description}</p>
        </motion.div>
      ))}
    </div>
  );
}

// Client Component for interactive elements
function HeroSection() {
  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-amber-500/10 via-blue-500/10 to-purple-500/10" />
      <div className="relative container mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <h1 className="text-6xl font-bold mb-6">
            <span className="gradient-text">VUC-2026</span>
          </h1>
          <p className="text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Vespera Ultimate Central - Otonom YouTube İmparatorluk Yönetim Sistemi
          </p>
          <p className="text-lg text-gray-400 mb-12 max-w-2xl mx-auto">
            Yapay zeka destekli, tam otomatik video üretim ve yönetim platformu ile YouTube'da rakipsiz olun
          </p>
          
          <div className="flex flex-wrap justify-center gap-4 mb-16">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-primary"
              onClick={() => window.location.href = '/onboarding'}
            >
              <Zap className="w-5 h-5 inline mr-2" />
              Hemen Başla
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-secondary"
              onClick={() => window.location.href = '/omniverse'}
            >
              <Settings className="w-5 h-5 inline mr-2" />
              Paneli Görüntüle
            </motion.button>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

// Server Component for System Status
async function SystemStatusSection() {
  const systemStatus = await getSystemStatus();
  
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400';
      case 'checking': return 'text-yellow-400';
      case 'error': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Aktif';
      case 'checking': return 'Kontrol ediliyor';
      case 'error': return 'Hata';
      default: return 'Bilinmiyor';
    }
  };

  return (
    <section className="py-12 border-t border-gray-800">
      <div className="container mx-auto px-6">
        <h2 className="text-2xl font-bold mb-8 text-center">Sistem Durumu</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {Object.entries(systemStatus).map(([key, status]) => (
            <motion.div
              key={key}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
              className="glass-effect rounded-lg p-6 text-center"
            >
              <div className={`text-3xl font-bold mb-2 ${getStatusColor(status)}`}>
                {getStatusText(status)}
              </div>
              <div className="text-gray-400 capitalize">
                {key === 'backend' ? 'Backend API' : 
                 key === 'frontend' ? 'Frontend' : 
                 key === 'redis' ? 'Redis' : 'AI Servisi'}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

// Server Component for Stats
async function StatsSection() {
  const stats = await getSystemStats();
  
  return (
    <section className="py-16 border-t border-gray-800">
      <div className="container mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="text-center"
            >
              <div className="glass-effect rounded-lg p-6 card-hover">
                <stat.icon className="w-8 h-8 mx-auto mb-4 text-amber-500" />
                <div className="text-3xl font-bold mb-2">{stat.value}</div>
                <div className="text-gray-400">{stat.label}</div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

// Main Page Component (Server Component)
export default async function HomePage() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Suspense fallback={<LoadingSpinner size="lg" />}>
        <HeroSection />
      </Suspense>
      
      <Suspense fallback={<LoadingSpinner size="lg" />}>
        <SystemStatusSection />
      </Suspense>
      
      <Suspense fallback={<LoadingSpinner size="lg" />}>
        <StatsSection />
      </Suspense>
      
      <Suspense fallback={<LoadingSpinner size="lg" />}>
        <section className="py-20 border-t border-gray-800">
          <div className="container mx-auto px-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl font-bold mb-4">God Mode Özellikler</h2>
              <p className="text-xl text-gray-400">
                YouTube'da hakimiyet kurmak için gereken her şey
              </p>
              
              {/* Quick Navigation */}
              <div className="flex justify-center space-x-4 mb-8">
                <a
                  href="/channels"
                  className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg text-white font-semibold transition-all transform hover:scale-105"
                >
                  Kanal Yönetimi
                </a>
                <a
                  href="/management"
                  className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg text-white font-semibold transition-all transform hover:scale-105"
                >
                  Gelişmiş Yönetim
                </a>
                <a
                  href="/memory"
                  className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-lg text-white font-semibold transition-all transform hover:scale-105"
                >
                  Sistem Belleği
                </a>
              </div>
            </motion.div>

            <FeaturesGrid />
          </div>
        </section>
      </Suspense>

      <Suspense fallback={<LoadingSpinner size="lg" />}>
        <section className="py-20 border-t border-gray-800">
          <div className="container mx-auto px-6 text-center">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="max-w-3xl mx-auto"
            >
              <h2 className="text-4xl font-bold mb-6">
                YouTube İmparatorluğunu <span className="gradient-text">Şimdi Başlat</span>
              </h2>
              <p className="text-xl text-gray-400 mb-8">
                VUC-2026 ile rakipleriniz geride kalacak. Otonom üretim, akıllı analiz ve grey-hat stratejilerle zirveye ulaşın.
              </p>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-primary text-lg px-8 py-4"
                onClick={() => window.location.href = '/onboarding'}
              >
                <Zap className="w-6 h-6 inline mr-3" />
                Sistemi Kur ve Başlat
              </motion.button>
            </motion.div>
          </div>
        </section>
      </Suspense>
    </div>
  );
}
