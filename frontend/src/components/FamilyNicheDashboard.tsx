"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Progress } from '@/components/ui/progress'
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  DollarSign, 
  Target, 
  Eye, 
  MessageSquare, 
  Video,
  Baby,
  Heart,
  Brain,
  ToyBrick,
  UserCheck,
  Shield,
  Zap,
  Clock,
  Calendar,
  AlertCircle,
  CheckCircle,
  ArrowUp,
  ArrowDown,
  MoreHorizontal
} from 'lucide-react'

interface VideoMatrix {
  title: string
  category: string
  priority_score: number
  estimated_views: number
  estimated_revenue: number
  status: 'planned' | 'in_production' | 'published'
  production_complexity: 'low' | 'medium' | 'high' | 'very_high'
}

interface CompetitorAnalysis {
  competitor: string
  threat_level: 'high' | 'medium' | 'low'
  opportunity_score: number
  hijack_opportunities: number
  thumbnail_gaps: number
}

interface CommunityMetrics {
  total_comments: number
  auto_replies: number
  engagement_rate: number
  sentiment_score: number
  top_personas: Array<{
    persona: string
    count: number
    percentage: number
  }>
}

interface AdSlotMetrics {
  total_videos: number
  optimized_videos: number
  avg_ctr_improvement: number
  estimated_revenue_lift: number
  coppa_compliant: number
}

const FamilyNicheDashboard: React.FC = () => {
  const [videoMatrix, setVideoMatrix] = useState<VideoMatrix[]>([])
  const [competitorAnalysis, setCompetitorAnalysis] = useState<CompetitorAnalysis[]>([])
  const [communityMetrics, setCommunityMetrics] = useState<CommunityMetrics | null>(null)
  const [adSlotMetrics, setAdSlotMetrics] = useState<AdSlotMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  // Mock data - in production, this would come from API calls
  useEffect(() => {
    const mockData = {
      videoMatrix: [
        {
          title: "Pregnancy Week 12: Baby Development & What to Expect",
          category: "pregnancy",
          priority_score: 0.95,
          estimated_views: 250000,
          estimated_revenue: 875.0,
          status: "planned",
          production_complexity: "high"
        },
        {
          title: "GIANT Surprise Egg Opening: Amazing Toy Discoveries",
          category: "toddler_toys_edutainment",
          priority_score: 0.92,
          estimated_views: 450000,
          estimated_revenue: 1260.0,
          status: "in_production",
          production_complexity: "medium"
        },
        {
          title: "High Contrast Cards for Newborns: Black & White Visual Stimulation",
          category: "baby_sensory_brain_dev",
          priority_score: 0.89,
          estimated_views: 180000,
          estimated_revenue: 450.0,
          status: "published",
          production_complexity: "low"
        },
        {
          title: "Postpartum Workout: Safe Exercises for New Moms",
          category: "mother_wellbeing",
          priority_score: 0.91,
          estimated_views: 320000,
          estimated_revenue: 960.0,
          status: "planned",
          production_complexity: "medium"
        },
        {
          title: "Newborn Sleep Schedule: Day 1 to Week 12 Complete Guide",
          category: "newborn_survival",
          priority_score: 0.94,
          estimated_views: 380000,
          estimated_revenue: 1216.0,
          status: "in_production",
          production_complexity: "high"
        }
      ],
      competitorAnalysis: [
        {
          competitor: "Cocomelon",
          threat_level: "high",
          opportunity_score: 0.75,
          hijack_opportunities: 15,
          thumbnail_gaps: 4
        },
        {
          competitor: "Ryan Toy Review",
          threat_level: "high", 
          opportunity_score: 0.82,
          hijack_opportunities: 12,
          thumbnail_gaps: 3
        },
        {
          competitor: "BabyCenter",
          threat_level: "medium",
          opportunity_score: 0.68,
          hijack_opportunities: 8,
          thumbnail_gaps: 2
        }
      ],
      communityMetrics: {
        total_comments: 15420,
        auto_replies: 12456,
        engagement_rate: 0.089,
        sentiment_score: 0.87,
        top_personas: [
          { persona: "expectant_mothers", count: 5234, percentage: 33.9 },
          { persona: "new_parents", count: 4892, percentage: 31.7 },
          { persona: "experienced_parents", count: 3124, percentage: 20.3 },
          { persona: "kids_viewers", count: 2170, percentage: 14.1 }
        ]
      },
      adSlotMetrics: {
        total_videos: 45,
        optimized_videos: 38,
        avg_ctr_improvement: 0.23,
        estimated_revenue_lift: 2840.0,
        coppa_compliant: 45
      }
    }

    setVideoMatrix(mockData.videoMatrix as VideoMatrix[])
    setCompetitorAnalysis(mockData.competitorAnalysis as CompetitorAnalysis[])
    setCommunityMetrics(mockData.communityMetrics)
    setAdSlotMetrics(mockData.adSlotMetrics)
    setLoading(false)
  }, [])

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'pregnancy': return <Heart className="h-4 w-4" />
      case 'newborn_survival': return <Baby className="h-4 w-4" />
      case 'baby_sensory_brain_dev': return <Brain className="h-4 w-4" />
      case 'toddler_toys_edutainment': return <ToyBrick className="h-4 w-4" />
      case 'mother_wellbeing': return <UserCheck className="h-4 w-4" />
      default: return <Video className="h-4 w-4" />
    }
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'pregnancy': return 'bg-pink-100 text-pink-800'
      case 'newborn_survival': return 'bg-blue-100 text-blue-800'
      case 'baby_sensory_brain_dev': return 'bg-purple-100 text-purple-800'
      case 'toddler_toys_edutainment': return 'bg-yellow-100 text-yellow-800'
      case 'mother_wellbeing': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'low': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'high': return 'bg-orange-100 text-orange-800'
      case 'very_high': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'planned': return 'bg-gray-100 text-gray-800'
      case 'in_production': return 'bg-blue-100 text-blue-800'
      case 'published': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getThreatLevelColor = (level: string) => {
    switch (level) {
      case 'high': return 'bg-red-100 text-red-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'low': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Aile & Çocuk Nişi Yükleniyor...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Niş Matrisi: Aile</h1>
          <p className="text-gray-600">VUC-2026 Aile & Çocuk İmparatorluğu Kontrol Paneli</p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm">
            <Calendar className="h-4 w-4 mr-2" />
            Takvim
          </Button>
          <Button variant="outline" size="sm">
            <Zap className="h-4 w-4 mr-2" />
            Hızlı Eylem
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Toplam Video Planı</CardTitle>
            <Video className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">100</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600">25 Hamilelik</span> • 
              <span className="text-blue-600"> 20 Yenidoğan</span> • 
              <span className="text-purple-600"> 20 Gelişim</span>
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tahmini Gelir</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$4,280</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600">+23.5%</span> geçen aya göre
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Otomatik Yanıtlar</CardTitle>
            <MessageSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12,456</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600">80.8%</span> yanıt oranı
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">CTR İyileştirme</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">23%</div>
            <p className="text-xs text-muted-foreground">
              Reklam slot optimizasyonu
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Genel Bakış</TabsTrigger>
          <TabsTrigger value="video-matrix">Video Matrisi</TabsTrigger>
          <TabsTrigger value="competitors">Rakip Analizi</TabsTrigger>
          <TabsTrigger value="community">Topluluk</TabsTrigger>
          <TabsTrigger value="optimization">Optimizasyon</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Video Matrix Overview */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Video className="h-5 w-5 mr-2" />
                  Video Matrisi Durumu
                </CardTitle>
                <CardDescription>
                  100-video stratejik içerik planı
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {videoMatrix.slice(0, 3).map((video, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2">
                          {getCategoryIcon(video.category)}
                          <span className="font-medium text-sm">{video.title}</span>
                        </div>
                        <div className="flex items-center space-x-2 mt-1">
                          <Badge className={getCategoryColor(video.category)}>
                            {video.category.replace('_', ' ')}
                          </Badge>
                          <Badge className={getStatusColor(video.status)}>
                            {video.status}
                          </Badge>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">{video.estimated_views.toLocaleString()} görüntülenme</div>
                        <div className="text-xs text-gray-500">${video.estimated_revenue.toFixed(0)}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Competitor Threats */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Shield className="h-5 w-5 mr-2" />
                  Rakip Tehdit Analizi
                </CardTitle>
                <CardDescription>
                  Ana rakiplerin tehdit seviyesi ve fırsatları
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {competitorAnalysis.map((competitor, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex-1">
                        <div className="font-medium">{competitor.competitor}</div>
                        <div className="flex items-center space-x-2 mt-1">
                          <Badge className={getThreatLevelColor(competitor.threat_level)}>
                            {competitor.threat_level} tehdit
                          </Badge>
                          <span className="text-sm text-gray-500">
                            {competitor.hijack_opportunities} fırsat
                          </span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">
                          {(competitor.opportunity_score * 100).toFixed(0)}% fırsat
                        </div>
                        <Progress value={competitor.opportunity_score * 100} className="w-20 mt-1" />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Hızlı Eylemler</CardTitle>
              <CardDescription>
                Aile & Çocuk nişi için yaygın görevler
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Button className="h-20 flex-col">
                  <Baby className="h-6 w-6 mb-2" />
                  Yeni Bebek İçeriği
                </Button>
                <Button variant="outline" className="h-20 flex-col">
                  <Target className="h-6 w-6 mb-2" />
                  Rakip Analizi
                </Button>
                <Button variant="outline" className="h-20 flex-col">
                  <MessageSquare className="h-6 w-6 mb-2" />
                  Yorum Yanıtları
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Video Matrix Tab */}
        <TabsContent value="video-matrix" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>100-Video Stratejik Matris</CardTitle>
              <CardDescription>
                Öncelik skoruna göre sıralanmış içerik planı
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {videoMatrix.map((video, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          {getCategoryIcon(video.category)}
                          <h3 className="font-medium">{video.title}</h3>
                          <Badge className={getCategoryColor(video.category)}>
                            {video.category.replace('_', ' ')}
                          </Badge>
                        </div>
                        <div className="flex items-center space-x-4 text-sm text-gray-600">
                          <span>Öncelik: {(video.priority_score * 100).toFixed(0)}%</span>
                          <span>Karmaşıklık: 
                            <Badge className={getComplexityColor(video.production_complexity)}>
                              {video.production_complexity}
                            </Badge>
                          </span>
                          <span>Durum:
                            <Badge className={getStatusColor(video.status)}>
                              {video.status}
                            </Badge>
                          </span>
                        </div>
                      </div>
                      <div className="text-right ml-4">
                        <div className="text-lg font-medium">{video.estimated_views.toLocaleString()}</div>
                        <div className="text-sm text-gray-500">görüntülenme</div>
                        <div className="text-lg font-medium text-green-600">${video.estimated_revenue.toFixed(0)}</div>
                        <div className="text-sm text-gray-500">tahmini gelir</div>
                      </div>
                    </div>
                    <Progress value={video.priority_score * 100} className="mt-3" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Competitors Tab */}
        <TabsContent value="competitors" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {competitorAnalysis.map((competitor, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>{competitor.competitor}</span>
                    <Badge className={getThreatLevelColor(competitor.threat_level)}>
                      {competitor.threat_level} tehdit
                    </Badge>
                  </CardTitle>
                  <CardDescription>
                    Fırsat skoru: {(competitor.opportunity_score * 100).toFixed(0)}%
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span>Keyword Hijack Fırsatları</span>
                      <span className="font-medium">{competitor.hijack_opportunities}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Thumbnail Boşlukları</span>
                      <span className="font-medium">{competitor.thumbnail_gaps}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Fırsat Skoru</span>
                      <Progress value={competitor.opportunity_score * 100} className="w-24" />
                    </div>
                    <div className="pt-2">
                      <Button className="w-full">
                        <Target className="h-4 w-4 mr-2" />
                        Detaylı Analiz
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Community Tab */}
        <TabsContent value="community" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Community Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Users className="h-5 w-5 mr-2" />
                  Topluluk Metrikleri
                </CardTitle>
                <CardDescription>
                  AI destekli topluluk yönetimi performansı
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Toplam Yorumlar</span>
                    <span className="font-medium">{communityMetrics?.total_comments.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Otomatik Yanıtlar</span>
                    <span className="font-medium">{communityMetrics?.auto_replies.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Etkileşim Oranı</span>
                    <span className="font-medium">{((communityMetrics?.engagement_rate || 0) * 100).toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Duygu Skoru</span>
                    <span className="font-medium">{((communityMetrics?.sentiment_score || 0) * 100).toFixed(1)}%</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Top Personas */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <UserCheck className="h-5 w-5 mr-2" />
                  Üst Personalar
                </CardTitle>
                <CardDescription>
                  Yorumcuların persona dağılımı
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {communityMetrics?.top_personas.map((persona, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="font-medium">{persona.persona.replace('_', ' ')}</div>
                        <div className="text-sm text-gray-500">{persona.count} yorum</div>
                      </div>
                      <div className="text-right">
                        <div className="font-medium">{persona.percentage.toFixed(1)}%</div>
                        <Progress value={persona.percentage} className="w-20 mt-1" />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Optimization Tab */}
        <TabsContent value="optimization" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Ad Slot Optimization */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="h-5 w-5 mr-2" />
                  Reklam Slot Optimizasyonu
                </CardTitle>
                <CardDescription>
                  Dinamik mid-roll yerleşimi ve COPPA uyumluluğu
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Toplam Videolar</span>
                    <span className="font-medium">{adSlotMetrics?.total_videos}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Optimize Edilen</span>
                    <span className="font-medium">{adSlotMetrics?.optimized_videos}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Ortalama CTR İyileştirme</span>
                    <span className="font-medium text-green-600">+{((adSlotMetrics?.avg_ctr_improvement || 0) * 100).toFixed(0)}%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Tahmini Gelir Artışı</span>
                    <span className="font-medium text-green-600">${adSlotMetrics?.estimated_revenue_lift.toFixed(0)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>COPPA Uyumlu</span>
                    <span className="font-medium">{adSlotMetrics?.coppa_compliant}/{adSlotMetrics?.total_videos}</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Performance Metrics */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BarChart3 className="h-5 w-5 mr-2" />
                  Performans Metrikleri
                </CardTitle>
                <CardDescription>
                  Niş performans göstergeleri
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>İzlenme Oranı</span>
                    <div className="flex items-center">
                      <ArrowUp className="h-4 w-4 text-green-600 mr-1" />
                      <span className="font-medium">67.8%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Tutma Oranı</span>
                    <div className="flex items-center">
                      <ArrowUp className="h-4 w-4 text-green-600 mr-1" />
                      <span className="font-medium">45.2%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Abone Kazanımı</span>
                    <div className="flex items-center">
                      <ArrowUp className="h-4 w-4 text-green-600 mr-1" />
                      <span className="font-medium">2.3%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>İçerik Skoru</span>
                    <div className="flex items-center">
                      <ArrowDown className="h-4 w-4 text-red-600 mr-1" />
                      <span className="font-medium">8.2/10</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default FamilyNicheDashboard
