'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { CheckCircle, Circle, AlertCircle, Rocket, Settings, Users, Target, Play, Sparkles } from 'lucide-react'
import { toast } from 'react-hot-toast'

interface OnboardingData {
  step1: {
    youtube_api_connected: boolean
    google_credentials: string
    channel_id: string
  }
  step2: {
    channel_name: string
    niche: string
    target_audience: string
    brand_style: string
    expert_persona: string
  }
  step3: {
    proxy_enabled: boolean
    proxy_config: {
      type: string
      country: string
      rotation: string
    }
    stealth_level: string
    ai_deception: boolean
  }
  step4: {
    autopilot_enabled: boolean
    daily_video_target: number
    production_schedule: string[]
    auto_upload: boolean
    auto_optimization: boolean
  }
}

const VUCOnboardingWizard: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(1)
  const [isCompleted, setIsCompleted] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  
  const [onboardingData, setOnboardingData] = useState<OnboardingData>({
    step1: {
      youtube_api_connected: false,
      google_credentials: '',
      channel_id: ''
    },
    step2: {
      channel_name: '',
      niche: '',
      target_audience: '',
      brand_style: 'pastel_family',
      expert_persona: '',
    },
    step3: {
      proxy_enabled: false,
      proxy_config: {
        type: 'residential',
        country: 'MD',
        rotation: 'every_request'
      },
      stealth_level: 'moderate',
      ai_deception: true
    },
    step4: {
      autopilot_enabled: true,
      daily_video_target: 3,
      production_schedule: ['09:00', '15:00', '20:00'],
      auto_upload: true,
      auto_optimization: true
    }
  })

  const [apiStatus, setApiStatus] = useState({
    youtube: 'disconnected',
    google: 'disconnected',
    production: 'disconnected',
    stealth: 'disconnected'
  })

  const totalSteps = 4

  useEffect(() => {
    // Calculate progress
    const stepProgress = (currentStep / totalSteps) * 100
    setProgress(stepProgress)
  }, [currentStep])

  const connectYouTubeAPI = async () => {
    try {
      setIsGenerating(true)
      const response = await fetch('/api/youtube/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          credentials: onboardingData.step1.google_credentials,
          channel_id: onboardingData.step1.channel_id
        })
      })

      if (response.ok) {
        setOnboardingData(prev => ({
          ...prev,
          step1: { ...prev.step1, youtube_api_connected: true }
        }))
        setApiStatus(prev => ({ ...prev, youtube: 'connected' }))
        toast.success('YouTube API başarıyla bağlandı!')
      } else {
        throw new Error('API bağlantısı başarısız')
      }
    } catch (error) {
      toast.error('YouTube API bağlantısı başarısız oldu')
    } finally {
      setIsGenerating(false)
    }
  }

  const generateBrandIdentity = async () => {
    try {
      setIsGenerating(true)
      const response = await fetch('/api/visual-assets/brand/identity', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          channel_name: onboardingData.step2.channel_name,
          niche: onboardingData.step2.niche,
          target_audience: onboardingData.step2.target_audience
        })
      })

      if (response.ok) {
        const brandData = await response.json()
        toast.success('Marka kimliği başarı oluşturuldu!')
        return brandData.brand_guidelines
      } else {
        throw new Error('Marka kimliği oluşturulamadı')
      }
    } catch (error) {
      toast.error('Marka kimliği oluşturulamadı')
      throw error
    } finally {
      setIsGenerating(false)
    }
  }

  const generateVideoMatrix = async () => {
    try {
      setIsGenerating(true)
      const response = await fetch('/api/family-kids-empire/generate-matrix', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          optimization_level: 'omnipotent',
          target_duration_minutes: 18
        })
      })

      if (response.ok) {
        const matrixData = await response.json()
        toast.success(`${matrixData.video_count} videoluk matris oluşturuldu!`)
        return matrixData
      } else {
        throw new Error('Video matrisi oluşturulamadı')
      }
    } catch (error) {
      toast.error('Video matrisi oluşturulamadı')
      throw error
    } finally {
      setIsGenerating(false)
    }
  }

  const startAutopilot = async () => {
    try {
      setIsGenerating(true)
      const response = await fetch('/api/family-kids-empire/autopilot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          daily_video_target: onboardingData.step4.daily_video_target,
          auto_upload_enabled: onboardingData.step4.auto_upload,
          auto_optimization_enabled: onboardingData.step4.auto_optimization,
          production_hours: onboardingData.step4.production_schedule
        })
      })

      if (response.ok) {
        const autopilotData = await response.json()
        toast.success('Otopilot modu aktifleştirildi!')
        return autopilotData
      } else {
        throw new Error('Otopilot başlatılamadı')
      }
    } catch (error) {
      toast.error('Otopilot başlatılamadı')
      throw error
    } finally {
      setIsGenerating(false)
    }
  }

  const nextStep = async () => {
    if (currentStep === 2) {
      // Generate brand identity and video matrix
      try {
        await generateBrandIdentity()
        await generateVideoMatrix()
      } catch (error) {
        return
      }
    }
    
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const completeOnboarding = async () => {
    try {
      setIsGenerating(true)
      await startAutopilot()
      setIsCompleted(true)
      toast.success('VUC-2026 İmparatorluğu başarıyla kuruldu! 🚀')
    } catch (error) {
      toast.error('İmparatorluk kurulumu tamamlanamadı')
    } finally {
      setIsGenerating(false)
    }
  }

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <Card className="w-full max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="w-5 h-5" />
                Adım 1: Google/YouTube API Bağlantısı
              </CardTitle>
              <CardDescription>
                YouTube API ve Google Cloud servislerini bağlayarak içerik üretim otomasyonunu başlatın.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div>
                  <Label htmlFor="google-credentials">Google Cloud JSON Kimliği</Label>
                  <Textarea
                    id="google-credentials"
                    placeholder="Google Cloud service account JSON dosyasını yapıştırın..."
                    value={onboardingData.step1.google_credentials}
                    onChange={(e) => setOnboardingData(prev => ({
                      ...prev,
                      step1: { ...prev.step1, google_credentials: e.target.value }
                    }))}
                    className="min-h-[100px]"
                  />
                </div>
                
                <div>
                  <Label htmlFor="channel-id">YouTube Kanal ID</Label>
                  <Input
                    id="channel-id"
                    placeholder="UC..."
                    value={onboardingData.step1.channel_id}
                    onChange={(e) => setOnboardingData(prev => ({
                      ...prev,
                      step1: { ...prev.step1, channel_id: e.target.value }
                    }))}
                  />
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="font-medium">API Durumu</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="flex items-center gap-2">
                    {apiStatus.youtube === 'connected' ? (
                      <CheckCircle className="w-4 h-4 text-green-500" />
                    ) : (
                      <Circle className="w-4 h-4 text-gray-400" />
                    )}
                    <span className="text-sm">YouTube API</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {apiStatus.google === 'connected' ? (
                      <CheckCircle className="w-4 h-4 text-green-500" />
                    ) : (
                      <Circle className="w-4 h-4 text-gray-400" />
                    )}
                    <span className="text-sm">Google Cloud</span>
                  </div>
                </div>
              </div>

              <Button 
                onClick={connectYouTubeAPI}
                disabled={!onboardingData.step1.google_credentials || !onboardingData.step1.channel_id || isGenerating}
                className="w-full"
              >
                {isGenerating ? 'Bağlanıyor...' : 'API Bağlantısını Kur'}
              </Button>

              {onboardingData.step1.youtube_api_connected && (
                <Alert>
                  <CheckCircle className="w-4 h-4" />
                  <AlertDescription>
                    API bağlantısı başarıyla kuruldu! Bir sonraki adıma geçebilirsiniz.
                  </AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>
        )

      case 2:
        return (
          <Card className="w-full max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5" />
                Adım 2: Niş ve Marka Persona Tanımlama
              </CardTitle>
              <CardDescription>
                Kanalınızın kimliğini, hedef kitlesini ve uzmanlık alanını belirleyin.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="channel-name">Kanal Adı</Label>
                  <Input
                    id="channel-name"
                    placeholder="Uzman Anne Hazal"
                    value={onboardingData.step2.channel_name}
                    onChange={(e) => setOnboardingData(prev => ({
                      ...prev,
                      step2: { ...prev.step2, channel_name: e.target.value }
                    }))}
                  />
                </div>
                
                <div>
                  <Label htmlFor="niche">Niş Alan</Label>
                  <Select
                    value={onboardingData.step2.niche}
                    onValueChange={(value) => setOnboardingData(prev => ({
                      ...prev,
                      step2: { ...prev.step2, niche: value }
                    }))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Niş seçin" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="baby">Bebek Bakımı</SelectItem>
                      <SelectItem value="pregnancy">Gebelik</SelectItem>
                      <SelectItem value="toddler">Toddler Gelişimi</SelectItem>
                      <SelectItem value="parenting_education">Ebeveyn Eğitimi</SelectItem>
                      <SelectItem value="montessori">Montessori</SelectItem>
                      <SelectItem value="premium_parenting">Premium Ebeveynlik</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label htmlFor="target-audience">Hedef Kitle</Label>
                <Textarea
                  id="target-audience"
                  placeholder="Yeni anneler, 25-35 yaş arası, eğitimli, teknolojiye açık..."
                  value={onboardingData.step2.target_audience}
                  onChange={(e) => setOnboardingData(prev => ({
                    ...prev,
                    step2: { ...prev.step2, target_audience: e.target.value }
                  }))}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="brand-style">Marka Stili</Label>
                  <Select
                    value={onboardingData.step2.brand_style}
                    onValueChange={(value) => setOnboardingData(prev => ({
                      ...prev,
                      step2: { ...prev.step2, brand_style: value }
                    }))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Stil seçin" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="pastel_family">Pastel Aile Odaklı</SelectItem>
                      <SelectItem value="modern_minimal">Modern Minimal</SelectItem>
                      <SelectItem value="playful_colorful">Oyuncak Renkli</SelectItem>
                      <SelectItem value="professional_educational">Profesyonel Eğitim</SelectItem>
                      <SelectItem value="luxury_premium">Luxury Premium</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="expert-persona">Uzman Persona</Label>
                  <Input
                    id="expert-persona"
                    placeholder="Uzman Pediatri Hemşire"
                    value={onboardingData.step2.expert_persona}
                    onChange={(e) => setOnboardingData(prev => ({
                      ...prev,
                      step2: { ...prev.step2, expert_persona: e.target.value }
                    }))}
                  />
                </div>
              </div>

              <Alert>
                <Sparkles className="w-4 h-4" />
                <AlertDescription>
                  Bu adımda otomatik olarak marka kimliği ve 100 videoluk içerik matrisi oluşturulacaktır.
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>
        )

      case 3:
        return (
          <Card className="w-full max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="w-5 h-5" />
                Adım 3: Gizlilik ve AI Koruma Ayarları
              </CardTitle>
              <CardDescription>
                Platform algılama sistemlerini baypas etmek için gizlilik ve AI koruma katmanlarını yapılandırın.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <h4 className="font-medium">Proxy Ayarları</h4>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="proxy-type">Proxy Tipi</Label>
                    <Select
                      value={onboardingData.step3.proxy_config.type}
                      onValueChange={(value) => setOnboardingData(prev => ({
                        ...prev,
                        step3: {
                          ...prev.step3,
                          proxy_config: { ...prev.step3.proxy_config, type: value }
                        }
                      }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="residential">Residential</SelectItem>
                        <SelectItem value="datacenter">Datacenter</SelectItem>
                        <SelectItem value="mobile">Mobile</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="proxy-country">Ülke</Label>
                    <Select
                      value={onboardingData.step3.proxy_config.country}
                      onValueChange={(value) => setOnboardingData(prev => ({
                        ...prev,
                        step3: {
                          ...prev.step3,
                          proxy_config: { ...prev.step3.proxy_config, country: value }
                        }
                      }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="MD">Moldova</SelectItem>
                        <SelectItem value="TR">Türkiye</SelectItem>
                        <SelectItem value="US">ABD</SelectItem>
                        <SelectItem value="DE">Almanya</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="proxy-rotation">Rotasyon</Label>
                    <Select
                      value={onboardingData.step3.proxy_config.rotation}
                      onValueChange={(value) => setOnboardingData(prev => ({
                        ...prev,
                        step3: {
                          ...prev.step3,
                          proxy_config: { ...prev.step3.proxy_config, rotation: value }
                        }
                      }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="every_request">Her İstek</SelectItem>
                        <SelectItem value="every_minute">Her Dakika</SelectItem>
                        <SelectItem value="every_hour">Her Saat</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="font-medium">AI Gizlilik Seviyesi</h4>
                <Select
                  value={onboardingData.step3.stealth_level}
                  onValueChange={(value) => setOnboardingData(prev => ({
                    ...prev,
                    step3: { ...prev.step3, stealth_level: value }
                  }))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="subtle">Hafif (%5 gürültü)</SelectItem>
                    <SelectItem value="moderate">Orta (%10 gürültü)</SelectItem>
                    <SelectItem value="advanced">İleri (%15 gürültü)</SelectItem>
                    <SelectItem value="stealth">Stealth (%20 gürültü)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="ai-deception"
                  title="AI Deception - Enable AI-powered content optimization"
                  aria-label="AI Deception - Enable AI-powered content optimization"
                  checked={onboardingData.step3.ai_deception}
                  onChange={(e) => setOnboardingData(prev => ({
                    ...prev,
                    step3: { ...prev.step3, ai_deception: e.target.checked }
                  }))}
                  className="rounded"
                />
                <Label htmlFor="ai-deception">AI Tespit Koruması Aktif</Label>
              </div>

              <Alert>
                <AlertCircle className="w-4 h-4" />
                <AlertDescription>
                  Bu ayarlar YouTube'un AI-generated içerik filtrelerini baypas etmek için tasarlanmıştır.
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>
        )

      case 4:
        return (
          <Card className="w-full max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Play className="w-5 h-5" />
                Adım 4: Otopilot Üretim Başlatma
              </CardTitle>
              <CardDescription>
                Otomatik video üretimini başlatın ve VUC-2026 İmparatorluğu'nu devreye alın.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="daily-target">Günlük Video Hedefi</Label>
                    <Select
                      value={onboardingData.step4.daily_video_target.toString()}
                      onValueChange={(value) => setOnboardingData(prev => ({
                        ...prev,
                        step4: { ...prev.step4, daily_video_target: parseInt(value) }
                      }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1">1 Video</SelectItem>
                        <SelectItem value="3">3 Video</SelectItem>
                        <SelectItem value="5">5 Video</SelectItem>
                        <SelectItem value="10">10 Video</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label>Üretim Saatleri</Label>
                    <div className="flex gap-2">
                      {['09:00', '15:00', '20:00'].map((time) => (
                        <Badge
                          key={time}
                          variant={onboardingData.step4.production_schedule.includes(time) ? "default" : "outline"}
                          className="cursor-pointer"
                          onClick={() => {
                            const schedule = onboardingData.step4.production_schedule
                            if (schedule.includes(time)) {
                              setOnboardingData(prev => ({
                                ...prev,
                                step4: {
                                  ...prev.step4,
                                  production_schedule: schedule.filter(t => t !== time)
                                }
                              }))
                            } else {
                              setOnboardingData(prev => ({
                                ...prev,
                                step4: {
                                  ...prev.step4,
                                  production_schedule: [...schedule, time]
                                }
                              }))
                            }
                          }}
                        >
                          {time}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="auto-upload"
                      title="Auto Upload - Automatically upload generated content"
                      aria-label="Auto Upload - Automatically upload generated content"
                      checked={onboardingData.step4.auto_upload}
                      onChange={(e) => setOnboardingData(prev => ({
                        ...prev,
                        step4: { ...prev.step4, auto_upload: e.target.checked }
                      }))}
                      className="rounded"
                    />
                    <Label htmlFor="auto-upload">Otomatik Yükleme Aktif</Label>
                  </div>

                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="auto-optimization"
                      title="Auto Optimization - Automatically optimize content performance"
                      aria-label="Auto Optimization - Automatically optimize content performance"
                      checked={onboardingData.step4.auto_optimization}
                      onChange={(e) => setOnboardingData(prev => ({
                        ...prev,
                        step4: { ...prev.step4, auto_optimization: e.target.checked }
                      }))}
                      className="rounded"
                    />
                    <Label htmlFor="auto-optimization">Otomatik Optimizasyon Aktif</Label>
                  </div>

                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="autopilot-enabled"
                      title="Autopilot Enabled - Enable fully automated content management"
                      aria-label="Autopilot Enabled - Enable fully automated content management"
                      checked={onboardingData.step4.autopilot_enabled}
                      onChange={(e) => setOnboardingData(prev => ({
                        ...prev,
                        step4: { ...prev.step4, autopilot_enabled: e.target.checked }
                      }))}
                      className="rounded"
                    />
                    <Label htmlFor="autopilot-enabled">Otopilot Modu Aktif</Label>
                  </div>
                </div>
              </div>

              <Alert>
                <Rocket className="w-4 h-4" />
                <AlertDescription>
                  🚀 İmparatorluğu başlatmaya hazır! Otopilot modu aktifleştirildiğinde sistem tamamen otonom olarak çalışacaktır.
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>
        )

      default:
        return null
    }
  }

  if (isCompleted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 p-8">
        <div className="max-w-4xl mx-auto">
          <Card className="text-center">
            <CardContent className="pt-6">
              <div className="space-y-6">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                  <Rocket className="w-8 h-8 text-green-600" />
                </div>
                
                <div>
                  <h1 className="text-3xl font-bold text-green-600 mb-2">
                    🎉 VUC-2026 İmparatorluğu Kuruldu!
                  </h1>
                  <p className="text-gray-600">
                    Aile ve Çocuk içerik imparatorluğunuz başarıyla devreye alındı. Otopilot modu aktif!
                  </p>
                </div>

                <div className="grid grid-cols-3 gap-4 text-center">
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">100</div>
                    <div className="text-sm text-gray-600">Video Matris</div>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">{onboardingData.step4.daily_video_target}</div>
                    <div className="text-sm text-gray-600">Günlük Video</div>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600">Otopilot</div>
                    <div className="text-sm text-gray-600">Mod Aktif</div>
                  </div>
                </div>

                <div className="space-y-3">
                  <h3 className="font-semibold">Aktif Özellikler:</h3>
                  <div className="flex flex-wrap gap-2 justify-center">
                    <Badge>✅ AI Script Üretimi</Badge>
                    <Badge>✅ Ses Sentezi</Badge>
                    <Badge>✅ Video Rendering</Badge>
                    <Badge>✅ SEO Optimizasyonu</Badge>
                    <Badge>✅ Otomatik Yükleme</Badge>
                    <Badge>✅ AI Gizlilik Kalkanı</Badge>
                    <Badge>✅ Analitik Takip</Badge>
                  </div>
                </div>

                <Button 
                  onClick={() => window.location.href = '/dashboard'}
                  className="w-full"
                  size="lg"
                >
                  Kontrol Paneline Git
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto">
            <Rocket className="w-8 h-8 text-purple-600" />
          </div>
          
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              VUC-2026: Family & Kids Empire
            </h1>
            <p className="text-gray-600">
              4 adımda YouTube imparatorluğunuzu kurun ve otonom içerik üretimini başlatın
            </p>
          </div>

          {/* Progress */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-gray-600">
              <span>Adım {currentStep} / {totalSteps}</span>
              <span>{Math.round(progress)}% Tamamlandı</span>
            </div>
            <Progress value={progress} className="w-full" />
          </div>
        </div>

        {/* Step Content */}
        {renderStep()}

        {/* Navigation */}
        <div className="flex justify-between max-w-2xl mx-auto">
          <Button
            variant="outline"
            onClick={prevStep}
            disabled={currentStep === 1}
          >
            Önceki Adım
          </Button>

          {currentStep === totalSteps ? (
            <Button
              onClick={completeOnboarding}
              disabled={isGenerating || !onboardingData.step4.autopilot_enabled}
              size="lg"
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
            >
              {isGenerating ? 'İmparatorluk Kuruluyor...' : '🚀 İmparatorluğu Başlat'}
            </Button>
          ) : (
            <Button
              onClick={nextStep}
              disabled={
                (currentStep === 1 && !onboardingData.step1.youtube_api_connected) ||
                (currentStep === 2 && (!onboardingData.step2.channel_name || !onboardingData.step2.niche)) ||
                isGenerating
              }
            >
              {isGenerating ? 'İşleniyor...' : 'Sonraki Adım'}
            </Button>
          )}
        </div>

        {/* Quick Status */}
        <div className="grid grid-cols-4 gap-4 max-w-2xl mx-auto">
          {[1, 2, 3, 4].map((step) => (
            <div
              key={step}
              className={`p-3 rounded-lg text-center ${
                step === currentStep
                  ? 'bg-purple-100 border-2 border-purple-300'
                  : step < currentStep
                  ? 'bg-green-50 border-2 border-green-200'
                  : 'bg-gray-50 border-2 border-gray-200'
              }`}
            >
              <div className="text-lg font-bold">
                {step < currentStep ? '✅' : step}
              </div>
              <div className="text-xs text-gray-600">
                {step === 1 && 'API'}
                {step === 2 && 'Marka'}
                {step === 3 && 'Gizlilik'}
                {step === 4 && 'Otopilot'}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default VUCOnboardingWizard
