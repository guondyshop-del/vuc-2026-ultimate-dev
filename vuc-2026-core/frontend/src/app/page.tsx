/**
 * VUC-2026 Main Dashboard Page
 * Enterprise-grade dashboard for video production management
 */

'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  PlayCircle, 
  BarChart3, 
  Users, 
  Video, 
  Settings, 
  Activity,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertCircle,
  XCircle
} from 'lucide-react'

import { apiClient, getStatusColor, formatDuration } from '@/lib/api'

interface DashboardStats {
  totalJobs: number
  completedJobs: number
  failedJobs: number
  activeJobs: number
  queueDepth: number
  systemHealth: 'healthy' | 'warning' | 'critical'
}

interface RecentJob {
  job_id: string
  topic: string
  status: string
  progress: number
  created_at: string
  processing_duration?: number
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [recentJobs, setRecentJobs] = useState<RecentJob[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadDashboardData()
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(loadDashboardData, 30000)
    
    return () => clearInterval(interval)
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Load metrics
      const metrics = await apiClient.system.getMetrics()
      
      // Load recent jobs
      const jobsResponse = await apiClient.jobs.list({ per_page: 5 })
      
      // Load system health
      const health = await apiClient.system.getHealth()
      
      setStats({
        totalJobs: metrics.total_jobs,
        completedJobs: metrics.completed_jobs,
        failedJobs: metrics.failed_jobs,
        activeJobs: metrics.queue_depth,
        queueDepth: metrics.queue_depth,
        systemHealth: health.status === 'healthy' ? 'healthy' : health.status === 'unhealthy' ? 'critical' : 'warning'
      })
      
      setRecentJobs(jobsResponse.jobs)
      
    } catch (err) {
      console.error('Failed to load dashboard data:', err)
      setError('Veriler yüklenemedi. Lütfen daha sonra tekrar deneyin.')
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'processing':
      case 'rendering':
      case 'uploading':
        return <Activity className="w-4 h-4 text-blue-500 animate-pulse" />
      case 'failed':
        return <XCircle className="w-4 h-4 text-red-500" />
      default:
        return <Clock className="w-4 h-4 text-yellow-500" />
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-vuc-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Dashboard yükleniyor...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600">{error}</p>
          <button 
            onClick={loadDashboardData}
            className="mt-4 px-4 py-2 bg-vuc-primary-600 text-white rounded-lg hover:bg-vuc-primary-700 transition-colors"
          >
            Tekrar Dene
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">VUC-2026</h1>
              <span className="ml-2 px-2 py-1 text-xs font-medium text-vuc-primary-600 bg-vuc-primary-50 rounded-full">
                Enterprise
              </span>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                stats?.systemHealth === 'healthy' 
                  ? 'bg-green-100 text-green-800'
                  : stats?.systemHealth === 'warning'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                Sistem Durumu: {stats?.systemHealth === 'healthy' ? 'Sağlıklı' : stats?.systemHealth === 'warning' ? 'Uyarı' : 'Kritik'}
              </div>
              
              <button 
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                aria-label="Ayarlar"
                title="Ayarlar"
              >
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white rounded-xl shadow-sm p-6 border border-gray-200"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Toplam Görevler</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{stats?.totalJobs || 0}</p>
              </div>
              <div className="p-3 bg-blue-50 rounded-lg">
                <Video className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="bg-white rounded-xl shadow-sm p-6 border border-gray-200"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Tamamlanan</p>
                <p className="text-2xl font-bold text-green-600 mt-1">{stats?.completedJobs || 0}</p>
              </div>
              <div className="p-3 bg-green-50 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bg-white rounded-xl shadow-sm p-6 border border-gray-200"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Aktif İşlem</p>
                <p className="text-2xl font-bold text-blue-600 mt-1">{stats?.activeJobs || 0}</p>
              </div>
              <div className="p-3 bg-blue-50 rounded-lg">
                <Activity className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="bg-white rounded-xl shadow-sm p-6 border border-gray-200"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Kuyruk Derinliği</p>
                <p className="text-2xl font-bold text-yellow-600 mt-1">{stats?.queueDepth || 0}</p>
              </div>
              <div className="p-3 bg-yellow-50 rounded-lg">
                <Clock className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
          </motion.div>
        </div>

        {/* Recent Jobs */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Jobs List */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="lg:col-span-2"
          >
            <div className="bg-white rounded-xl shadow-sm border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">Son Görevler</h2>
              </div>
              
              <div className="divide-y divide-gray-200">
                {recentJobs.length === 0 ? (
                  <div className="px-6 py-8 text-center">
                    <Video className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">Henüz görev bulunmuyor</p>
                  </div>
                ) : (
                  recentJobs.map((job, index) => (
                    <motion.div
                      key={job.job_id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.1 }}
                      className="px-6 py-4 hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          {getStatusIcon(job.status)}
                          <div>
                            <p className="font-medium text-gray-900">{job.topic}</p>
                            <p className="text-sm text-gray-500">
                              {new Date(job.created_at).toLocaleString('tr-TR')}
                            </p>
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-4">
                          <div className="text-right">
                            <p className={`text-sm font-medium ${getStatusColor(job.status)}`}>
                              {job.status}
                            </p>
                            {job.progress > 0 && (
                              <div className="mt-1">
                                <div className="progress-container">
                                  <div 
                                    className="progress-bar"
                                    style={{ width: `${job.progress}%` }}
                                    role="progressbar"
                                    aria-valuenow={Number(job.progress)}
                                    aria-valuemin={0}
                                    aria-valuemax={100}
                                    aria-label={`İşlem ilerlemesi: ${job.progress}%`}
                                    title={`İşlem ilerlemesi: ${job.progress}%`}
                                  ></div>
                                </div>
                              </div>
                            )}
                          </div>
                          
                          {job.processing_duration && (
                            <div className="text-right">
                              <p className="text-sm text-gray-500">
                                {formatDuration(job.processing_duration)}
                              </p>
                            </div>
                          )}
                        </div>
                      </div>
                    </motion.div>
                  ))
                )}
              </div>
            </div>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-6">Hızlı İşlemler</h2>
              
              <div className="space-y-4">
                <button className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-vuc-primary-600 text-white rounded-lg hover:bg-vuc-primary-700 transition-colors">
                  <PlayCircle className="w-5 h-5" />
                  <span>Yeni Video Üret</span>
                </button>
                
                <button className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                  <BarChart3 className="w-5 h-5" />
                  <span>Analizleri Gör</span>
                </button>
                
                <button className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                  <Users className="w-5 h-5" />
                  <span>Kullanıcıları Yönet</span>
                </button>
                
                <button className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                  <Settings className="w-5 h-5" />
                  <span>Ayarlar</span>
                </button>
              </div>
              
              {/* System Info */}
              <div className="mt-6 pt-6 border-t border-gray-200">
                <h3 className="text-sm font-medium text-gray-900 mb-4">Sistem Bilgileri</h3>
                
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Versiyon</span>
                    <span className="font-medium text-gray-900">1.0.0</span>
                  </div>
                  
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Çalışma Süresi</span>
                    <span className="font-medium text-gray-900">2h 34m</span>
                  </div>
                  
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Başarı Oranı</span>
                    <span className="font-medium text-green-600">
                      {stats?.totalJobs ? Math.round((stats.completedJobs / stats.totalJobs) * 100) : 0}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  )
}
