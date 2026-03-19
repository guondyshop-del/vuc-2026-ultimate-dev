"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Progress } from '@/components/ui/progress'
import { 
  Baby, 
  Clock, 
  Globe, 
  PlayCircle, 
  Calendar, 
  TrendingUp, 
  Heart, 
  Music,
  Palette,
  Mic,
  Video,
  Sparkles,
  Target
} from 'lucide-react'

interface BabyContent {
  id: string
  story_type: string
  character: string
  theme: string
  language: string
  duration: number
  estimated_views: number
  estimated_revenue: number
  priority_score: number
  status: 'idea' | 'generating' | 'ready' | 'uploading' | 'published'
}

interface ContentTemplate {
  story_types: Record<string, any>
  characters: Record<string, string>
  themes: Record<string, string[]>
  languages: Record<string, any>
}

export default function BabyContentDashboard() {
  const [contentIdeas, setContentIdeas] = useState<BabyContent[]>([])
  const [templates, setTemplates] = useState<ContentTemplate | null>(null)
  const [loading, setLoading] = useState(false)
  const [selectedContent, setSelectedContent] = useState<BabyContent | null>(null)
  const [generationProgress, setGenerationProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('ideas')

  // Form states
  const [formData, setFormData] = useState({
    story_type: '',
    character: '',
    theme: '',
    language: 'tr',
    duration: 900
  })

  useEffect(() => {
    loadContentIdeas()
    loadTemplates()
  }, [])

  const loadContentIdeas = async () => {
    try {
      const response = await fetch('/api/baby-content/ideas?limit=20')
      const data = await response.json()
      if (data.success) {
        setContentIdeas(data.data.ideas.map((idea: any, index: number) => ({
          ...idea,
          id: `idea-${index}`,
          status: 'idea' as const
        })))
      }
    } catch (error) {
      console.error('İçerik fikirleri yüklenemedi:', error)
    }
  }

  const loadTemplates = async () => {
    try {
      const response = await fetch('/api/baby-content/templates')
      const data = await response.json()
      if (data.success) {
        setTemplates(data.data)
      }
    } catch (error) {
      console.error('Şablonlar yüklenemedi:', error)
    }
  }

  const generateContent = async () => {
    if (!formData.story_type || !formData.character || !formData.theme) {
      alert('Lütfen tüm alanları doldurun')
      return
    }

    setLoading(true)
    setGenerationProgress(0)

    try {
      // Simüle edilmiş progress
      const progressInterval = setInterval(() => {
        setGenerationProgress(prev => Math.min(prev + 10, 90))
      }, 500)

      const response = await fetch('/api/baby-content/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      clearInterval(progressInterval)
      setGenerationProgress(100)

      const data = await response.json()
      if (data.success) {
        alert('İçerik başarıyla oluşturuldu!')
        loadContentIdeas()
        setGenerationProgress(0)
      } else {
        alert('İçerik oluşturulamadı: ' + data.message)
      }
    } catch (error) {
      console.error('İçerik oluşturulamadı:', error)
      alert('İçerik oluşturulamadı')
    } finally {
      setLoading(false)
      setTimeout(() => setGenerationProgress(0), 2000)
    }
  }

  const batchGenerate = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/baby-content/batch-generate?count=10&auto_schedule=true', {
        method: 'POST'
      })
      const data = await response.json()
      if (data.success) {
        alert(`${data.data.generated_count} içerik toplu olarak oluşturuldu!`)
        loadContentIdeas()
      }
    } catch (error) {
      console.error('Toplu oluşturulamadı:', error)
      alert('Toplu oluşturulamadı')
    } finally {
      setLoading(false)
    }
  }

  const createSchedule = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/baby-content/schedule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          daily_count: 3,
          upload_times: ['09:00', '15:00', '20:00']
        })
      })
      const data = await response.json()
      if (data.success) {
        alert(`${data.data.total_videos} videoluk takvim oluşturuldu!`)
      }
    } catch (error) {
      console.error('Takvim oluşturulamadı:', error)
      alert('Takvim oluşturulamadı')
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'idea': return 'bg-gray-500'
      case 'generating': return 'bg-yellow-500'
      case 'ready': return 'bg-green-500'
      case 'uploading': return 'bg-blue-500'
      case 'published': return 'bg-purple-500'
      default: return 'bg-gray-500'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'idea': return 'Fikir'
      case 'generating': return 'Oluşturuluyor'
      case 'ready': return 'Hazır'
      case 'uploading': return 'Yükleniyor'
      case 'published': return 'Yayında'
      default: return 'Bilinmiyor'
    }
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Baby className="w-8 h-8 text-pink-500" />
          <div>
            <h1 className="text-3xl font-bold">YouTube Kids Bebek İçerik Merkezi</h1>
            <p className="text-gray-600">Otomatik bebek video üretim ve yönetim sistemi</p>
          </div>
        </div>
        <div className="flex space-x-2">
          <Button onClick={batchGenerate} disabled={loading} className="bg-purple-600 hover:bg-purple-700">
            <Sparkles className="w-4 h-4 mr-2" />
            Toplu Oluştur (10)
          </Button>
          <Button onClick={createSchedule} disabled={loading} className="bg-blue-600 hover:bg-blue-700">
            <Calendar className="w-4 h-4 mr-2" />
            Takvim Oluştur
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Toplam Fikir</p>
                <p className="text-2xl font-bold">{contentIdeas.length}</p>
              </div>
              <Target className="w-8 h-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Tahmini İzlenme</p>
                <p className="text-2xl font-bold">
                  {contentIdeas.reduce((sum, idea) => sum + idea.estimated_views, 0).toLocaleString()}
                </p>
              </div>
              <TrendingUp className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Tahmini Gelir</p>
                <p className="text-2xl font-bold">
                  ${contentIdeas.reduce((sum, idea) => sum + idea.estimated_revenue, 0).toFixed(2)}
                </p>
              </div>
              <TrendingUp className="w-8 h-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Ortalama Skor</p>
                <p className="text-2xl font-bold">
                  {(contentIdeas.reduce((sum, idea) => sum + idea.priority_score, 0) / contentIdeas.length || 0).toFixed(2)}
                </p>
              </div>
              <Heart className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Generation Progress */}
      {generationProgress > 0 && (
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-4">
              <Video className="w-6 h-6 text-blue-500 animate-pulse" />
              <div className="flex-1">
                <p className="text-sm font-medium">Video Üretimi</p>
                <Progress value={generationProgress} className="mt-2" />
              </div>
              <span className="text-sm text-gray-600">{generationProgress}%</span>
            </div>
          </CardContent>
        </Card>
      )}

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="ideas">İçerik Fikirleri</TabsTrigger>
          <TabsTrigger value="generate">Yeni İçerik</TabsTrigger>
          <TabsTrigger value="templates">Şablonlar</TabsTrigger>
        </TabsList>

        <TabsContent value="ideas" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Target className="w-5 h-5" />
                <span>Otomatik İçerik Fikirleri</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {contentIdeas.map((content) => (
                  <div key={content.id} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <Badge className={getStatusColor(content.status)}>
                            {getStatusText(content.status)}
                          </Badge>
                          <span className="font-medium">{content.character}</span>
                          <span className="text-gray-500">•</span>
                          <span className="text-gray-600">{content.theme}</span>
                          <span className="text-gray-500">•</span>
                          <span className="text-gray-600">{content.story_type}</span>
                        </div>
                        <div className="flex items-center space-x-4 text-sm text-gray-500">
                          <div className="flex items-center space-x-1">
                            <Clock className="w-4 h-4" />
                            <span>{Math.floor(content.duration / 60)}dk</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <Globe className="w-4 h-4" />
                            <span>{content.language.toUpperCase()}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <TrendingUp className="w-4 h-4" />
                            <span>{content.estimated_views.toLocaleString()} izlenme</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <span className="text-green-600">${content.estimated_revenue.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="text-right">
                          <div className="text-sm font-medium">Skor</div>
                          <div className="text-lg font-bold text-purple-600">
                            {content.priority_score.toFixed(2)}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="generate" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Sparkles className="w-5 h-5" />
                <span>Yeni Bebek İçeriği Oluştur</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="story_type">Hikaye Türü</Label>
                  <Select value={formData.story_type} onValueChange={(value) => setFormData({...formData, story_type: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Hikaye türü seçin" />
                    </SelectTrigger>
                    <SelectContent>
                      {templates?.story_types && Object.entries(templates.story_types).map(([key, value]: [string, any]) => (
                        <SelectItem key={key} value={key}>
                          {key.replace('_', ' ').toUpperCase()} - {value.age_group}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="character">Karakter</Label>
                  <Select value={formData.character} onValueChange={(value) => setFormData({...formData, character: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Karakter seçin" />
                    </SelectTrigger>
                    <SelectContent>
                      {templates?.characters && Object.entries(templates.characters).map(([key, value]) => (
                        <SelectItem key={key} value={key}>
                          {key.replace('_', ' ').toUpperCase()} - {value}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="theme">Eğitici Tema</Label>
                  <Select value={formData.theme} onValueChange={(value) => setFormData({...formData, theme: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Tema seçin" />
                    </SelectTrigger>
                    <SelectContent>
                      {templates?.themes && Object.keys(templates.themes).map((key) => (
                        <SelectItem key={key} value={key}>
                          {key.toUpperCase()}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="language">Dil</Label>
                  <Select value={formData.language} onValueChange={(value) => setFormData({...formData, language: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Dil seçin" />
                    </SelectTrigger>
                    <SelectContent>
                      {templates?.languages && Object.entries(templates.languages).map(([key, value]: [string, any]) => (
                        <SelectItem key={key} value={key}>
                          {value.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="duration">Süre (saniye)</Label>
                  <Input
                    id="duration"
                    type="number"
                    value={formData.duration}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData({...formData, duration: parseInt(e.target.value)})}
                    placeholder="900"
                  />
                </div>
              </div>

              <Button onClick={generateContent} disabled={loading} className="w-full">
                <Video className="w-4 h-4 mr-2" />
                {loading ? 'Oluşturuluyor...' : 'İçerik Oluştur'}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="templates" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Music className="w-5 h-5" />
                  <span>Hikaye Türleri</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {templates?.story_types && Object.entries(templates.story_types).map(([key, value]: [string, any]) => (
                    <div key={key} className="border rounded p-3">
                      <div className="font-medium">{key.replace('_', ' ').toUpperCase()}</div>
                      <div className="text-sm text-gray-600">
                        Yaş: {value.age_group} • Süre: {Math.floor(value.duration / 60)}dk
                      </div>
                      <div className="text-sm text-gray-500">
                        Ton: {value.tone}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Baby className="w-5 h-5" />
                  <span>Karakterler</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {templates?.characters && Object.entries(templates.characters).map(([key, value]) => (
                    <div key={key} className="border rounded p-3">
                      <div className="font-medium">{key.replace('_', ' ').toUpperCase()}</div>
                      <div className="text-sm text-gray-600">{value}</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Palette className="w-5 h-5" />
                  <span>Eğitici Temalar</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {templates?.themes && Object.entries(templates.themes).map(([key, value]) => (
                    <div key={key} className="border rounded p-3">
                      <div className="font-medium">{key.toUpperCase()}</div>
                      <div className="text-sm text-gray-600">
                        {Array.isArray(value) ? value.join(', ') : value}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Mic className="w-5 h-5" />
                  <span>Diller</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {templates?.languages && Object.entries(templates.languages).map(([key, value]: [string, any]) => (
                    <div key={key} className="border rounded p-3">
                      <div className="font-medium">{key.toUpperCase()}</div>
                      <div className="text-sm text-gray-600">{value.name}</div>
                      <div className="text-sm text-gray-500">{value.voice}</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
