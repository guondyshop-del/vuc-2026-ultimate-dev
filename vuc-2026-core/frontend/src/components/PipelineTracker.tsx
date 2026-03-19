/**
 * VUC-2026 Pipeline Tracker Component
 * Real-time progress tracking for video production pipeline
 */

'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Activity, 
  Clock, 
  CheckCircle, 
  XCircle, 
  PlayCircle,
  Zap,
  Target,
  Settings,
  Upload,
  Eye,
  BarChart3
} from 'lucide-react'
import { apiClient, formatDuration, getStatusColor } from '@/lib/api'

interface JobStatus {
  job_id: string
  status: string
  progress: number
  current_stage: string
  estimated_completion?: string
  processing_metrics: {
    total_processing_time?: number
    psychology_time?: number
    render_time?: number
    upload_time?: number
    retry_count: number
  }
}

interface PipelineTrackerProps {
  jobId: string
  onClose?: () => void
}

export default function PipelineTracker({ jobId, onClose }: PipelineTrackerProps) {
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadJobStatus = async () => {
      try {
        const status = await apiClient.jobs.getStatus(jobId)
        setJobStatus(status)
        setError(null)
      } catch (err) {
        console.error('Failed to load job status:', err)
        setError('Durum yüklenemedi')
      } finally {
        setLoading(false)
      }
    }

    loadJobStatus()

    // Auto-refresh every 5 seconds for active jobs
    if (!jobStatus || ['pending', 'processing', 'rendering', 'uploading'].includes(jobStatus.status)) {
      const interval = setInterval(loadJobStatus, 5000)
      return () => clearInterval(interval)
    }
  }, [jobId, jobStatus?.status])

  const getStageIcon = (stage: string) => {
    switch (stage.toLowerCase()) {
      case 'psychology_analysis':
        return <Target className="w-5 h-5" />
      case 'video_rendering':
        return <Settings className="w-5 h-5" />
      case 'youtube_upload':
        return <Upload className="w-5 h-5" />
      case 'completed':
        return <CheckCircle className="w-5 h-5" />
      case 'failed':
        return <XCircle className="w-5 h-5" />
      default:
        return <Clock className="w-5 h-5" />
    }
  }

  const getStageColor = (stage: string) => {
    switch (stage.toLowerCase()) {
      case 'psychology_analysis':
        return 'text-purple-600 bg-purple-50'
      case 'video_rendering':
        return 'text-blue-600 bg-blue-50'
      case 'youtube_upload':
        return 'text-green-600 bg-green-50'
      case 'completed':
        return 'text-green-600 bg-green-50'
      case 'failed':
        return 'text-red-600 bg-red-50'
      default:
        return 'text-gray-600 bg-gray-50'
    }
  }

  const getStageName = (stage: string) => {
    switch (stage.toLowerCase()) {
      case 'psychology_analysis':
        return 'Psikoloji Analizi'
      case 'video_rendering':
        return 'Video İşleme'
      case 'youtube_upload':
        return 'YouTube Yükleme'
      case 'completed':
        return 'Tamamlandı'
      case 'failed':
        return 'Başarısız'
      default:
        return 'Beklemede'
    }
  }

  const pipelineStages = [
    { key: 'psychology_analysis', name: 'Psikoloji Analizi', icon: Target },
    { key: 'asset_generation', name: 'Varlık Üretimi', icon: Zap },
    { key: 'video_rendering', name: 'Video İşleme', icon: Settings },
    { key: 'youtube_upload', name: 'YouTube Yükleme', icon: Upload },
    { key: 'completed', name: 'Tamamlandı', icon: CheckCircle }
  ]

  const getCurrentStageIndex = () => {
    if (!jobStatus) return 0
    
    const currentStage = jobStatus.current_stage.toLowerCase()
    return pipelineStages.findIndex(stage => stage.key.toLowerCase().includes(currentStage.replace('_', '')))
  }

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-6 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-vuc-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Durum yükleniyor...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-6 text-center">
          <XCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Kapat
          </button>
        </div>
      </div>
    )
  }

  if (!jobStatus) {
    return null
  }

  const currentStageIndex = getCurrentStageIndex()
  const isCompleted = jobStatus.status === 'completed'
  const isFailed = jobStatus.status === 'failed'

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-vuc-primary-600 to-vuc-secondary-600 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Activity className="w-6 h-6 text-white" />
              <h2 className="text-xl font-bold text-white">Video Üretim Durumu</h2>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 transition-colors"
            >
              <XCircle className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="p-6">
          {/* Job Info */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="text-sm text-gray-500">Görev ID</p>
                <p className="font-mono text-sm text-gray-900">{jobId}</p>
              </div>
              <div className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(jobStatus.status)}`}>
                {jobStatus.status === 'pending' && 'Beklemede'}
                {jobStatus.status === 'processing' && 'İşleniyor'}
                {jobStatus.status === 'rendering' && 'İşleniyor'}
                {jobStatus.status === 'uploading' && 'Yükleniyor'}
                {jobStatus.status === 'completed' && 'Tamamlandı'}
                {jobStatus.status === 'failed' && 'Başarısız'}
              </div>
            </div>

            {/* Progress Bar */}
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600">İlerleme</span>
                <span className="font-medium text-gray-900">{Math.round(jobStatus.progress)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <motion.div
                  className="bg-gradient-to-r from-vuc-primary-600 to-vuc-secondary-600 h-3 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${jobStatus.progress}%` }}
                  transition={{ duration: 0.5 }}
                />
              </div>
            </div>

            {/* Current Stage */}
            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              {getStageIcon(jobStatus.current_stage)}
              <div>
                <p className="text-sm font-medium text-gray-900">
                  {getStageName(jobStatus.current_stage)}
                </p>
                {jobStatus.estimated_completion && (
                  <p className="text-xs text-gray-500">
                    Tahmini bitiş: {new Date(jobStatus.estimated_completion).toLocaleString('tr-TR')}
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Pipeline Stages */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Üretim Hattı</h3>
            <div className="space-y-3">
              {pipelineStages.map((stage, index) => {
                const Icon = stage.icon
                const isActive = index === currentStageIndex
                const isCompleted = index < currentStageIndex
                const isFailed = isFailed && index === currentStageIndex

                return (
                  <motion.div
                    key={stage.key}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className={`flex items-center space-x-3 p-3 rounded-lg border ${
                      isFailed
                        ? 'border-red-200 bg-red-50'
                        : isCompleted
                        ? 'border-green-200 bg-green-50'
                        : isActive
                        ? 'border-vuc-primary-200 bg-vuc-primary-50'
                        : 'border-gray-200 bg-gray-50'
                    }`}
                  >
                    <div className={`p-2 rounded-lg ${
                      isFailed
                        ? 'bg-red-100 text-red-600'
                        : isCompleted
                        ? 'bg-green-100 text-green-600'
                        : isActive
                        ? 'bg-vuc-primary-100 text-vuc-primary-600'
                        : 'bg-gray-100 text-gray-600'
                    }`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <div className="flex-1">
                      <p className={`font-medium ${
                        isFailed
                          ? 'text-red-900'
                          : isCompleted
                          ? 'text-green-900'
                          : isActive
                          ? 'text-vuc-primary-900'
                          : 'text-gray-900'
                      }`}>
                        {stage.name}
                      </p>
                      <p className="text-sm text-gray-500">
                        {isCompleted && 'Tamamlandı'}
                        {isActive && 'Devam ediyor...'}
                        {!isCompleted && !isActive && 'Bekliyor'}
                      </p>
                    </div>
                    <div>
                      {isCompleted && <CheckCircle className="w-5 h-5 text-green-600" />}
                      {isActive && <Activity className="w-5 h-5 text-vuc-primary-600 animate-pulse" />}
                      {isFailed && <XCircle className="w-5 h-5 text-red-600" />}
                    </div>
                  </motion.div>
                )
              })}
            </div>
          </div>

          {/* Processing Metrics */}
          {jobStatus.processing_metrics && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">İşlem Metrikleri</h3>
              <div className="grid grid-cols-2 gap-4">
                {jobStatus.processing_metrics.psychology_time && (
                  <div className="p-3 bg-purple-50 rounded-lg">
                    <div className="flex items-center space-x-2 mb-1">
                      <Target className="w-4 h-4 text-purple-600" />
                      <span className="text-sm font-medium text-purple-900">Psikoloji Analizi</span>
                    </div>
                    <p className="text-lg font-semibold text-purple-900">
                      {formatDuration(jobStatus.processing_metrics.psychology_time)}
                    </p>
                  </div>
                )}

                {jobStatus.processing_metrics.render_time && (
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center space-x-2 mb-1">
                      <Settings className="w-4 h-4 text-blue-600" />
                      <span className="text-sm font-medium text-blue-900">Video İşleme</span>
                    </div>
                    <p className="text-lg font-semibold text-blue-900">
                      {formatDuration(jobStatus.processing_metrics.render_time)}
                    </p>
                  </div>
                )}

                {jobStatus.processing_metrics.upload_time && (
                  <div className="p-3 bg-green-50 rounded-lg">
                    <div className="flex items-center space-x-2 mb-1">
                      <Upload className="w-4 h-4 text-green-600" />
                      <span className="text-sm font-medium text-green-900">YouTube Yükleme</span>
                    </div>
                    <p className="text-lg font-semibold text-green-900">
                      {formatDuration(jobStatus.processing_metrics.upload_time)}
                    </p>
                  </div>
                )}

                {jobStatus.processing_metrics.total_processing_time && (
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-2 mb-1">
                      <Clock className="w-4 h-4 text-gray-600" />
                      <span className="text-sm font-medium text-gray-900">Toplam Süre</span>
                    </div>
                    <p className="text-lg font-semibold text-gray-900">
                      {formatDuration(jobStatus.processing_metrics.total_processing_time)}
                    </p>
                  </div>
                )}
              </div>

              {jobStatus.processing_metrics.retry_count > 0 && (
                <div className="mt-4 p-3 bg-yellow-50 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <Zap className="w-4 h-4 text-yellow-600" />
                    <span className="text-sm font-medium text-yellow-900">
                      Yeniden deneme sayısı: {jobStatus.processing_metrics.retry_count}
                    </span>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end space-x-3">
            <button
              onClick={() => window.open(`/jobs/${jobId}`, '_blank')}
              className="flex items-center space-x-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Eye className="w-4 h-4" />
              <span>Detaylar</span>
            </button>

            {isCompleted && (
              <button
                onClick={() => window.open(`/analytics/${jobId}`, '_blank')}
                className="flex items-center space-x-2 px-4 py-2 bg-vuc-primary-600 text-white rounded-lg hover:bg-vuc-primary-700 transition-colors"
              >
                <BarChart3 className="w-4 h-4" />
                <span>Analizler</span>
              </button>
            )}

            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
            >
              Kapat
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
