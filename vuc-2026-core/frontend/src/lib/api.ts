/**
 * VUC-2026 API Client
 * Axios-based API client with interceptors and error handling
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { toast } from 'react-hot-toast'

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add request timestamp
    config.metadata = { startTime: new Date() }
    
    // Log request in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
    }
    
    return config
  },
  (error) => {
    console.error('❌ Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response: AxiosResponse) => {
    // Calculate request duration
    const endTime = new Date()
    const duration = endTime.getTime() - response.config.metadata?.startTime?.getTime()
    
    // Log response in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`✅ API Response: ${response.status} (${duration}ms)`)
    }
    
    return response
  },
  (error) => {
    // Handle different error types
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response
      
      console.error(`❌ API Error ${status}:`, data)
      
      // Show user-friendly error messages
      switch (status) {
        case 400:
          toast.error('Geçersiz istek. Lütfen bilgilerinizi kontrol edin.')
          break
        case 401:
          toast.error('Yetkilendirme hatası. Lütfen tekrar giriş yapın.')
          break
        case 403:
          toast.error('Bu işlem için yetkiniz bulunmuyor.')
          break
        case 404:
          toast.error('İstenen kaynak bulunamadı.')
          break
        case 422:
          const validationErrors = data?.detail || 'Doğrulama hatası'
          toast.error(validationErrors)
          break
        case 429:
          toast.error('Çok fazla istek gönderdiniz. Lütfen bekleyin.')
          break
        case 500:
          toast.error('Sunucu hatası. Lütfen daha sonra tekrar deneyin.')
          break
        default:
          toast.error('Beklenmedik bir hata oluştu.')
      }
    } else if (error.request) {
      // Request was made but no response received
      console.error('❌ Network Error:', error.message)
      toast.error('Ağ bağlantısı hatası. İnternet bağlantınızı kontrol edin.')
    } else {
      // Something else happened
      console.error('❌ Unknown Error:', error.message)
      toast.error('Beklenmedik bir hata oluştu.')
    }
    
    return Promise.reject(error)
  }
)

// API Client Types
export interface JobCreateRequest {
  topic: string
  age_group: {
    min_months: number
    max_months: number
  }
  priority: string
  quality: string
  duration_minutes: number
  render_config?: any
  youtube_metadata?: any
  client_id?: string
  custom_metadata?: any
}

export interface JobResponse {
  job_id: string
  topic: string
  age_range: string
  status: string
  progress: number
  created_at: string
  started_at?: string
  completed_at?: string
  video_duration?: number
  video_quality?: string
  youtube_video_id?: string
  view_count: number
  like_count: number
  comment_count: number
  error_message?: string
  processing_duration?: number
}

export interface JobStatusResponse {
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

export interface SystemHealth {
  status: string
  database: any
  redis: any
  api_services: any
  background_tasks: any
  storage: any
  uptime: string
  version: string
}

export interface JobMetrics {
  total_jobs: number
  completed_jobs: number
  failed_jobs: number
  average_processing_time: number
  success_rate: number
  daily_job_count: number
  queue_depth: number
  system_load: {
    cpu_usage: number
    memory_usage: number
    disk_usage: number
    active_workers: number
  }
}

// API Functions
export const apiClient = {
  // Job Management
  jobs: {
    create: async (data: JobCreateRequest): Promise<JobResponse> => {
        const response = await api.post<JobResponse>('/jobs', data)
        return response.data
      },
      
      get: async (jobId: string): Promise<JobResponse> => {
        const response = await api.get<JobResponse>(`/jobs/${jobId}`)
        return response.data
      },
      
      list: async (params?: {
        status?: string
        client_id?: string
        page?: number
        per_page?: number
      }): Promise<{
        jobs: JobResponse[]
        total: number
        page: number
        per_page: number
        has_next: boolean
        has_prev: boolean
      }> => {
        const response = await api.get('/jobs', { params })
        return response.data
      },
      
      getStatus: async (jobId: string): Promise<JobStatusResponse> => {
        const response = await api.get<JobStatusResponse>(`/jobs/${jobId}/status`)
        return response.data
      },
      
      updateStatus: async (jobId: string, status: string, progress?: number): Promise<void> => {
        await api.put(`/jobs/${jobId}/status`, { status, progress })
      },
      
      delete: async (jobId: string): Promise<void> => {
        await api.delete(`/jobs/${jobId}`)
      },
      
      getPending: async (limit: number = 10): Promise<{
        pending_jobs: Array<{
          job_id: string
          topic: string
          age_range: string
          priority: number
          created_at: string
          estimated_duration: number
        }>
        queue_depth: number
        max_concurrent_jobs: number
      }> => {
        const response = await api.get('/jobs/queue/pending', { params: { limit } })
        return response.data
      }
  },
  
  // System
  system: {
    getHealth: async (): Promise<SystemHealth> => {
        const response = await api.get<SystemHealth>('/health')
        return response.data
      },
      
    getMetrics: async (): Promise<JobMetrics> => {
        const response = await api.get<JobMetrics>('/metrics')
        return response.data
      }
  },
  
  // Root endpoint
  root: async (): Promise<{
    application: string
    version: string
    environment: string
    status: string
    timestamp: string
    endpoints: {
      docs: string
      redoc: string
      health: string
      jobs: string
    }
  }> => {
    const response = await api.get('/')
    return response.data
  }
}

// Utility functions
export const formatDuration = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = Math.floor(seconds % 60)
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

export const getStatusColor = (status: string): string => {
  switch (status.toLowerCase()) {
    case 'pending':
      return 'text-yellow-600 bg-yellow-50'
    case 'processing':
    case 'rendering':
    case 'uploading':
      return 'text-blue-600 bg-blue-50'
    case 'completed':
      return 'text-green-600 bg-green-50'
    case 'failed':
      return 'text-red-600 bg-red-50'
    default:
      return 'text-gray-600 bg-gray-50'
  }
}

export const getProgressColor = (progress: number): string => {
  if (progress >= 90) return 'bg-green-500'
  if (progress >= 60) return 'bg-blue-500'
  if (progress >= 30) return 'text-yellow-500'
  return 'bg-red-500'
}

export default api
