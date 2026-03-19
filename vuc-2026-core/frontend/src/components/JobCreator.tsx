/**
 * VUC-2026 Job Creator Component
 * Modern form for creating video production jobs
 */

'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  PlayCircle, 
  Settings, 
  Clock, 
  Target, 
  Zap, 
  Upload,
  X,
  Check,
  AlertCircle
} from 'lucide-react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'react-hot-toast'

import { apiClient } from '@/lib/api'

// Form validation schema
const jobSchema = z.object({
  topic: z.string().min(1, 'Konu alanı zorunludur').max(255, 'Konu çok uzun'),
  age_group: z.object({
    min_months: z.number().min(12, 'Minimum yaş 12 ay olmalıdır').max(120, 'Maximum yaş 120 ay olabilir'),
    max_months: z.number().min(12, 'Minimum yaş 12 ay olmalıdır').max(120, 'Maximum yaş 120 ay olabilir'),
  }).refine((data: { min_months: number; max_months: number }) => data.max_months >= data.min_months, {
    message: 'Maximum yaş minimum yaştan büyük veya eşit olmalıdır',
    path: ['max_months']
  }),
  priority: z.enum(['urgent', 'high', 'normal', 'low', 'background']),
  quality: z.enum(['720p', '1080p', '1440p', '4k']),
  duration_minutes: z.number().min(1, 'Süre en az 1 dakika olmalıdır').max(20, 'Süre en fazla 20 dakika olabilir'),
  client_id: z.string().optional(),
})

type JobFormData = z.infer<typeof jobSchema>

interface JobCreatorProps {
  onSuccess?: (jobId: string) => void
  onCancel?: () => void
}

export default function JobCreator({ onSuccess, onCancel }: JobCreatorProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [currentStep, setCurrentStep] = useState(1)
  const [showAdvanced, setShowAdvanced] = useState(false)
  
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isValid },
    reset
  } = useForm<JobFormData>({
    resolver: zodResolver(jobSchema),
    defaultValues: {
      topic: '',
      age_group: {
        min_months: 36,
        max_months: 72
      },
      priority: 'normal',
      quality: '1080p',
      duration_minutes: 3,
      client_id: ''
    }
  })

  const watchedAgeGroup = watch('age_group')
  const watchedDuration = watch('duration_minutes')

  // Predefined age groups
  const agePresets = [
    { label: 'Bebek (1-2 yaş)', min: 12, max: 24 },
    { label: 'Okul Öncesi (3-4 yaş)', min: 36, max: 48 },
    { label: 'İlkokul (5-6 yaş)', min: 60, max: 72 },
    { label: 'Özel Aralık', min: 12, max: 120 }
  ]

  // Priority options
  const priorityOptions = [
    { value: 'urgent', label: 'Acil', color: 'red', icon: Zap },
    { value: 'high', label: 'Yüksek', color: 'orange', icon: Target },
    { value: 'normal', label: 'Normal', color: 'blue', icon: Clock },
    { value: 'low', label: 'Düşük', color: 'gray', icon: Settings },
    { value: 'background', label: 'Arka Plan', color: 'purple', icon: Settings }
  ]

  // Quality options
  const qualityOptions = [
    { value: '720p', label: 'HD (720p)', description: 'Standart kalite' },
    { value: '1080p', label: 'FHD (1080p)', description: 'Yüksek kalite (önerilen)' },
    { value: '1440p', label: 'QHD (1440p)', description: 'Ultra kalite' },
    { value: '4k', label: '4K', description: 'Sinema kalitesi' }
  ]

  const onSubmit = async (data: JobFormData) => {
    try {
      setIsSubmitting(true)
      
      const response = await apiClient.jobs.create(data)
      
      toast.success('Video üretim görevi başarıyla oluşturuldu!')
      reset()
      onSuccess?.(response.job_id)
      
    } catch (error) {
      console.error('Failed to create job:', error)
      toast.error('Görev oluşturulamadı. Lütfen tekrar deneyin.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const setAgePreset = (preset: typeof agePresets[0]) => {
    setValue('age_group.min_months', preset.min)
    setValue('age_group.max_months', preset.max)
  }

  const getEstimatedTime = () => {
    const baseTime = 15 // minutes
    const qualityMultiplier = {
      '720p': 1,
      '1080p': 1.5,
      '1440p': 2,
      '4k': 3
    }
    const durationMultiplier = watchedDuration / 3
    
    return Math.round(baseTime * qualityMultiplier[watchedQuality as keyof typeof qualityMultiplier] * durationMultiplier)
  }

  const watchedQuality = watch('quality')

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-vuc-primary-600 to-vuc-secondary-600 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <PlayCircle className="w-6 h-6 text-white" />
              <h2 className="text-xl font-bold text-white">Yeni Video Üretimi</h2>
            </div>
            <button
              onClick={onCancel}
              className="text-white hover:text-gray-200 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Progress Steps */}
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            {[1, 2, 3].map((step) => (
              <div key={step} className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  currentStep >= step 
                    ? 'bg-vuc-primary-600 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}>
                  {currentStep > step ? <Check className="w-4 h-4" /> : step}
                </div>
                {step < 3 && (
                  <div className={`w-full h-1 mx-2 ${
                    currentStep > step ? 'bg-vuc-primary-600' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-between mt-2">
            <span className="text-xs text-gray-600">Temel Bilgiler</span>
            <span className="text-xs text-gray-600">Hedef Kitle</span>
            <span className="text-xs text-gray-600">Teknik Ayarlar</span>
          </div>
        </div>

        {/* Form Content */}
        <form onSubmit={handleSubmit(onSubmit)} className="p-6">
          <div className="max-h-[60vh] overflow-y-auto">
            {/* Step 1: Basic Information */}
            {currentStep === 1 && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="space-y-6"
              >
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Video Konusu <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    {...register('topic')}
                    placeholder="Örn: Renkler Öğreniyoruz"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-vuc-primary-500 focus:border-transparent"
                  />
                  {errors.topic && (
                    <p className="mt-1 text-sm text-red-600 flex items-center">
                      <AlertCircle className="w-4 h-4 mr-1" />
                      {errors.topic.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Video Süresi (dakika) <span className="text-red-500">*</span>
                  </label>
                  <div className="flex items-center space-x-4">
                    <input
                      type="range"
                      min="1"
                      max="20"
                      {...register('duration_minutes', { valueAsNumber: true })}
                      className="flex-1"
                    />
                    <div className="w-16 text-center">
                      <span className="text-lg font-medium text-vuc-primary-600">{watchedDuration}</span>
                      <span className="text-sm text-gray-500 ml-1">dk</span>
                    </div>
                  </div>
                  <p className="mt-1 text-xs text-gray-500">
                    Tahmini üretim süresi: {getEstimatedTime()} dakika
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Öncelik Seviyesi
                  </label>
                  <div className="grid grid-cols-3 gap-3">
                    {priorityOptions.map((option) => {
                      const Icon = option.icon
                      return (
                        <label
                          key={option.value}
                          className={`relative flex items-center justify-center p-3 border rounded-lg cursor-pointer transition-all ${
                            watch('priority') === option.value
                              ? 'border-vuc-primary-600 bg-vuc-primary-50'
                              : 'border-gray-300 hover:border-gray-400'
                          }`}
                        >
                          <input
                            type="radio"
                            {...register('priority')}
                            value={option.value}
                            className="sr-only"
                          />
                          <div className="text-center">
                            <Icon className={`w-5 h-5 mx-auto mb-1 ${
                              option.color === 'red' ? 'text-red-500' :
                              option.color === 'orange' ? 'text-orange-500' :
                              option.color === 'blue' ? 'text-blue-500' :
                              option.color === 'gray' ? 'text-gray-500' :
                              'text-purple-500'
                            }`} />
                            <span className="text-sm font-medium">{option.label}</span>
                          </div>
                        </label>
                      )
                    })}
                  </div>
                </div>
              </motion.div>
            )}

            {/* Step 2: Target Audience */}
            {currentStep === 2 && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="space-y-6"
              >
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Hedef Yaş Grubu <span className="text-red-500">*</span>
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    {agePresets.map((preset) => (
                      <button
                        key={preset.label}
                        type="button"
                        onClick={() => setAgePreset(preset)}
                        className={`p-3 border rounded-lg text-left transition-all ${
                          watchedAgeGroup.min_months === preset.min && 
                          watchedAgeGroup.max_months === preset.max
                            ? 'border-vuc-primary-600 bg-vuc-primary-50'
                            : 'border-gray-300 hover:border-gray-400'
                        }`}
                      >
                        <div className="font-medium">{preset.label}</div>
                        <div className="text-sm text-gray-500">
                          {preset.min}-{preset.max} ay
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Minimum Yaş (ay) <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="number"
                      {...register('age_group.min_months', { valueAsNumber: true })}
                      min="12"
                      max="120"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-vuc-primary-500 focus:border-transparent"
                    />
                    {errors.age_group?.min_months && (
                      <p className="mt-1 text-sm text-red-600">{errors.age_group.min_months.message}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Maximum Yaş (ay) <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="number"
                      {...register('age_group.max_months', { valueAsNumber: true })}
                      min="12"
                      max="120"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-vuc-primary-500 focus:border-transparent"
                    />
                    {errors.age_group?.max_months && (
                      <p className="mt-1 text-sm text-red-600">{errors.age_group.max_months.message}</p>
                    )}
                  </div>
                </div>

                {errors.age_group && (
                  <p className="text-sm text-red-600 flex items-center">
                    <AlertCircle className="w-4 h-4 mr-1" />
                    {errors.age_group.message}
                  </p>
                )}

                {/* Psychology insights */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-medium text-blue-900 mb-2">Psikolojik İçgörüler</h4>
                  <div className="text-sm text-blue-800">
                    <p>🧠 Yaş aralığı: {watchedAgeGroup.min_months}-{watchedAgeGroup.max_months} ay</p>
                    <p>📈 Dikkat süresi: {watchedAgeGroup.min_months < 36 ? '3-5 dakika' : '5-10 dakika'}</p>
                    <p>🎨 Renk tercihleri: {watchedAgeGroup.min_months < 36 ? 'Yüksek kontrast, parlak renkler' : 'Çeşitli tonlar, pastel renkler'}</p>
                    <p>🎵 Ses frekansı: {watchedAgeGroup.min_months < 36 ? '500-4000 Hz' : '500-8000 Hz'}</p>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Step 3: Technical Settings */}
            {currentStep === 3 && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="space-y-6"
              >
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Video Kalitesi
                  </label>
                  <div className="space-y-2">
                    {qualityOptions.map((option) => (
                      <label
                        key={option.value}
                        className={`flex items-center p-3 border rounded-lg cursor-pointer transition-all ${
                          watch('quality') === option.value
                            ? 'border-vuc-primary-600 bg-vuc-primary-50'
                            : 'border-gray-300 hover:border-gray-400'
                        }`}
                      >
                        <input
                          type="radio"
                          {...register('quality')}
                          value={option.value}
                          className="sr-only"
                        />
                        <div className="flex-1">
                          <div className="font-medium">{option.label}</div>
                          <div className="text-sm text-gray-500">{option.description}</div>
                        </div>
                        {watch('quality') === option.value && (
                          <Check className="w-5 h-5 text-vuc-primary-600" />
                        )}
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <button
                    type="button"
                    onClick={() => setShowAdvanced(!showAdvanced)}
                    className="flex items-center space-x-2 text-vuc-primary-600 hover:text-vuc-primary-700 font-medium"
                  >
                    <Settings className="w-4 h-4" />
                    <span>Gelişmiş Ayarlar</span>
                  </button>
                </div>

                <AnimatePresence>
                  {showAdvanced && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="space-y-4 p-4 bg-gray-50 rounded-lg"
                    >
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Müşteri ID (opsiyonel)
                        </label>
                        <input
                          type="text"
                          {...register('client_id')}
                          placeholder="Müşteri tanımlayıcısı"
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-vuc-primary-500 focus:border-transparent"
                        />
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Summary */}
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h4 className="font-medium text-green-900 mb-2">Özet</h4>
                  <div className="text-sm text-green-800 space-y-1">
                    <p>📹 Konu: {watch('topic') || 'Belirtilmemiş'}</p>
                    <p>⏱️ Süre: {watchedDuration} dakika</p>
                    <p>👥 Yaş: {watchedAgeGroup.min_months}-{watchedAgeGroup.max_months} ay</p>
                    <p>🎯 Kalite: {watch('quality')}</p>
                    <p>⚡ Öncelik: {watch('priority')}</p>
                    <p>🕐 Tahmini süre: {getEstimatedTime()} dakika</p>
                  </div>
                </div>
              </motion.div>
            )}
          </div>

          {/* Navigation Buttons */}
          <div className="flex justify-between items-center mt-6 pt-6 border-t border-gray-200">
            <div className="flex space-x-3">
              {currentStep > 1 && (
                <button
                  type="button"
                  onClick={() => setCurrentStep(currentStep - 1)}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Geri
                </button>
              )}
            </div>

            <div className="flex space-x-3">
              <button
                type="button"
                onClick={onCancel}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                İptal
              </button>

              {currentStep < 3 ? (
                <button
                  type="button"
                  onClick={() => setCurrentStep(currentStep + 1)}
                  className="px-6 py-2 bg-vuc-primary-600 text-white rounded-lg hover:bg-vuc-primary-700 transition-colors"
                >
                  İleri
                </button>
              ) : (
                <button
                  type="submit"
                  disabled={!isValid || isSubmitting}
                  className="px-6 py-2 bg-vuc-primary-600 text-white rounded-lg hover:bg-vuc-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                >
                  {isSubmitting ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Oluşturuluyor...</span>
                    </>
                  ) : (
                    <>
                      <Upload className="w-4 h-4" />
                      <span>Görev Oluştur</span>
                    </>
                  )}
                </button>
              )}
            </div>
          </div>
        </form>
      </motion.div>
    </div>
  )
}
