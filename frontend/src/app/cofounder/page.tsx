'use client';

import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { 
  MessageSquare, 
  Brain, 
  Users, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle,
  Clock,
  ThumbsUp,
  ThumbsDown,
  RefreshCw,
  Send,
  Bot,
  User,
  Zap,
  Target,
  Lightbulb,
  Shield
} from 'lucide-react';

interface Consultation {
  id: string;
  timestamp: string;
  agent: string;
  confidence_score: number;
  data_summary: string;
  question: string;
  options: Array<{
    id: string;
    label: string;
    action: string;
  }>;
  status: string;
  response?: string;
  response_message?: string;
  response_timestamp?: string;
}

interface ChatMessage {
  id: string;
  type: 'user' | 'ai';
  message: string;
  timestamp: string;
  consultation_id?: string;
}

export default function CoFounderPage() {
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [selectedConsultation, setSelectedConsultation] = useState<Consultation | null>(null);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [responding, setResponding] = useState(false);

  useEffect(() => {
    fetchConsultations();
    
    const interval = setInterval(() => {
      fetchConsultations();
    }, 10000); // Update every 10 seconds
    
    return () => clearInterval(interval);
  }, []);

  const fetchConsultations = async () => {
    try {
      const response = await fetch('/api/empire/consultations/pending');
      const data = await response.json();
      
      if (data.success) {
        setConsultations(data.pending_consultations);
      }
    } catch (error) {
      console.error('Danışmanlıklar alınamadı:', error);
    } finally {
      setLoading(false);
    }
  };

  const respondToConsultation = async (consultationId: string, action: string, message?: string) => {
    setResponding(true);
    
    try {
      const response = await fetch(`/api/empire/consultations/${consultationId}/respond`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: action,
          message: message || ''
        }),
      });

      const data = await response.json();
      
      if (data.success) {
        // Update consultation status
        setConsultations(prev => 
          prev.map(c => 
            c.id === consultationId 
              ? { 
                  ...c, 
                  status: 'responded',
                  response: action,
                  response_message: message,
                  response_timestamp: data.timestamp
                }
              : c
          )
        );
        
        // Add to chat
        const userMessage: ChatMessage = {
          id: `user_${Date.now()}`,
          type: 'user',
          message: message || `Action: ${action}`,
          timestamp: new Date().toISOString(),
          consultation_id: consultationId
        };
        
        const aiMessage: ChatMessage = {
          id: `ai_${Date.now()}`,
          type: 'ai',
          message: `Kararınız alındı: ${action}. ${data.execution_result?.message || ''}`,
          timestamp: new Date().toISOString(),
          consultation_id: consultationId
        };
        
        setChatMessages(prev => [...prev, userMessage, aiMessage]);
        
        // Clear selection if this was the selected consultation
        if (selectedConsultation?.id === consultationId) {
          setSelectedConsultation(null);
        }
      }
    } catch (error) {
      console.error('Danışmanlık yanıtlama hatası:', error);
    } finally {
      setResponding(false);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim()) return;
    
    const userMessage: ChatMessage = {
      id: `user_${Date.now()}`,
      type: 'user',
      message: newMessage,
      timestamp: new Date().toISOString()
    };
    
    setChatMessages(prev => [...prev, userMessage]);
    
    // Simulate AI response
    setTimeout(() => {
      const aiMessage: ChatMessage = {
        id: `ai_${Date.now()}`,
        type: 'ai',
        message: "Mesajınız alındı. VUC-2026 sistemi olarak en iyi kararı vereceğim. Sistem performansını analiz ediyorum...",
        timestamp: new Date().toISOString()
      };
      
      setChatMessages(prev => [...prev, aiMessage]);
    }, 1000);
    
    setNewMessage('');
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 90) return 'text-green-500';
    if (score >= 75) return 'text-yellow-500';
    return 'text-red-500';
  };

  const getConfidenceBg = (score: number) => {
    if (score >= 90) return 'bg-green-500/20';
    if (score >= 75) return 'bg-yellow-500/20';
    return 'bg-red-500/20';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <Brain className="w-16 h-16 animate-pulse text-blue-500" />
          <p className="text-xl">Co-Founder Desk yükleniyor...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl">
              <Users className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                Co-Founder Desk
              </h1>
              <p className="text-gray-400">VUC-2026 Neural Architecture Decision Center</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 px-4 py-2 bg-blue-500/20 rounded-lg">
              <Brain className="w-4 h-4 text-blue-500" />
              <span className="text-sm font-medium">
                {consultations.length} Bekleyen Danışmanlık
              </span>
            </div>
            <button
              onClick={fetchConsultations}
              className="p-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"
              title="Yenile"
            >
              <RefreshCw className="w-5 h-5" />
            </button>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Consultations List */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="lg:col-span-1"
        >
          <div className="bg-gray-800 rounded-xl border border-gray-700">
            <div className="p-6 border-b border-gray-700">
              <h2 className="text-xl font-bold flex items-center space-x-3">
                <MessageSquare className="w-6 h-6 text-blue-500" />
                <span>Bekleyen Danışmanlıklar</span>
              </h2>
            </div>
            
            <div className="max-h-96 overflow-y-auto">
              {consultations.length > 0 ? (
                <div className="p-4 space-y-3">
                  {consultations.map((consultation, index) => (
                    <motion.div
                      key={index}
                      whileHover={{ scale: 1.02 }}
                      onClick={() => setSelectedConsultation(consultation)}
                      className={`p-4 rounded-lg border cursor-pointer transition-all ${
                        selectedConsultation?.id === consultation.id
                          ? 'bg-blue-500/20 border-blue-500'
                          : 'bg-gray-700 border-gray-600 hover:border-gray-500'
                      }`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <Bot className="w-4 h-4 text-blue-400" />
                          <span className="text-sm font-medium capitalize">
                            {consultation.agent?.replace('_agent', '')}
                          </span>
                        </div>
                        <span className={`text-xs px-2 py-1 rounded ${getConfidenceBg(consultation.confidence_score || 0)} ${getConfidenceColor(consultation.confidence_score || 0)}`}>
                          {consultation.confidence_score}%
                        </span>
                      </div>
                      
                      <p className="text-sm text-gray-300 mb-2 line-clamp-2">
                        {consultation.question}
                      </p>
                      
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>{consultation.data_summary}</span>
                        <span>{new Date(consultation.timestamp || '').toLocaleTimeString('tr-TR')}</span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              ) : (
                <div className="p-8 text-center text-gray-500">
                  <CheckCircle className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>Bekleyen danışmanlık yok</p>
                  <p className="text-sm mt-2">Sistem otonom olarak çalışıyor</p>
                </div>
              )}
            </div>
          </div>
        </motion.div>

        {/* Selected Consultation / Chat */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="lg:col-span-2"
        >
          <div className="bg-gray-800 rounded-xl border border-gray-700 h-full">
            {selectedConsultation ? (
              <div className="flex flex-col h-full">
                {/* Consultation Header */}
                <div className="p-6 border-b border-gray-700">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <Bot className="w-6 h-6 text-blue-500" />
                      <div>
                        <h3 className="font-semibold capitalize">
                          {selectedConsultation.agent?.replace('_agent', '')} Danışmanlığı
                        </h3>
                        <p className="text-sm text-gray-400">
                          Güven Seviyesi: {selectedConsultation.confidence_score}%
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={() => setSelectedConsultation(null)}
                      className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
                      title="Kapat"
                    >
                      ×
                    </button>
                  </div>
                  
                  <div className={`p-4 rounded-lg ${getConfidenceBg(selectedConsultation.confidence_score || 0)}`}>
                    <p className="text-lg font-medium mb-2">
                      {selectedConsultation.question}
                    </p>
                    <p className="text-sm text-gray-400">
                      {selectedConsultation.data_summary}
                    </p>
                  </div>
                </div>

                {/* Response Options */}
                <div className="p-6 border-b border-gray-700">
                  <h4 className="font-semibold mb-4">Karar Seçenekleri</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {selectedConsultation.options?.map((option: any) => (
                      <button
                        key={option.id}
                        onClick={() => respondToConsultation(
                          selectedConsultation.id || '',
                          option.action,
                          option.label
                        )}
                        disabled={responding}
                        className="p-4 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <div className="flex flex-col items-center space-y-2">
                          {option.action === 'approve' && <ThumbsUp className="w-6 h-6 text-green-500" />}
                          {option.action === 'modify' && <RefreshCw className="w-6 h-6 text-yellow-500" />}
                          {option.action === 'reject' && <ThumbsDown className="w-6 h-6 text-red-500" />}
                          <span className="text-sm font-medium">{option.label}</span>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Custom Response */}
                <div className="p-6 border-b border-gray-700">
                  <h4 className="font-semibold mb-4">Özel Mesaj</h4>
                  <div className="flex space-x-4">
                    <input
                      type="text"
                      className="flex-1 px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Özel yanıt girin..."
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    />
                    <button
                      onClick={sendMessage}
                      disabled={!newMessage.trim() || responding}
                      className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      title="Mesaj gönder"
                    >
                      <Send className="w-5 h-5" />
                    </button>
                  </div>
                </div>

                {/* Chat Messages */}
                <div className="flex-1 p-6 overflow-y-auto">
                  <div className="space-y-4">
                    {chatMessages
                      .filter(msg => msg.consultation_id === selectedConsultation.id)
                      .map((message) => (
                        <div
                          key={message.id}
                          className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                          <div className={`max-w-xs lg:max-w-md ${
                            message.type === 'user'
                              ? 'bg-blue-500 text-white'
                              : 'bg-gray-700 text-gray-100'
                          } rounded-lg p-3`}>
                            <div className="flex items-start space-x-2">
                              {message.type === 'user' ? (
                                <User className="w-4 h-4 mt-1 flex-shrink-0" />
                              ) : (
                                <Bot className="w-4 h-4 mt-1 flex-shrink-0" />
                              )}
                              <p className="text-sm">{message.message}</p>
                            </div>
                            <p className="text-xs opacity-70 mt-1">
                              {new Date(message.timestamp).toLocaleTimeString('tr-TR')}
                            </p>
                          </div>
                        </div>
                      ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-8 h-full flex flex-col items-center justify-center text-center">
                <div className="mb-6">
                  <div className="p-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl mb-4">
                    <Brain className="w-12 h-12 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2">Co-Founder Desk</h3>
                  <p className="text-gray-400 mb-4">
                    VUC-2026 Neural Architecture karar merkezi
                  </p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-2xl">
                  <div className="bg-gray-700 rounded-lg p-4">
                    <Target className="w-8 h-8 text-blue-500 mx-auto mb-2" />
                    <h4 className="font-medium mb-1">Otonom Kararlar</h4>
                    <p className="text-sm text-gray-400">90+ güven seviyesi</p>
                  </div>
                  
                  <div className="bg-gray-700 rounded-lg p-4">
                    <Lightbulb className="w-8 h-8 text-yellow-500 mx-auto mb-2" />
                    <h4 className="font-medium mb-1">Danışma Gereken</h4>
                    <p className="text-sm text-gray-400">75-89 güven seviyesi</p>
                  </div>
                  
                  <div className="bg-gray-700 rounded-lg p-4">
                    <Shield className="w-8 h-8 text-green-500 mx-auto mb-2" />
                    <h4 className="font-medium mb-1">Manuel Müdahale</h4>
                    <p className="text-sm text-gray-400">75- güven seviyesi</p>
                  </div>
                </div>
                
                <div className="mt-8 text-gray-500">
                  <p className="text-sm">Bekleyen danışmanlık olduğunda burada görünecek</p>
                  <p className="text-sm mt-1">Sistem otonom olarak çalışıyor</p>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      </div>

      {/* System Status Bar */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mt-6 bg-gray-800 rounded-xl border border-gray-700 p-4"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2">
              <Zap className="w-5 h-5 text-green-500" />
              <span className="text-sm">Sistem Aktif</span>
            </div>
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-5 h-5 text-blue-500" />
              <span className="text-sm">Performans: %95</span>
            </div>
            <div className="flex items-center space-x-2">
              <Clock className="w-5 h-5 text-purple-500" />
              <span className="text-sm">Son güncelleme: {new Date().toLocaleTimeString('tr-TR')}</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 text-sm text-gray-400">
            <AlertTriangle className="w-4 h-4" />
            <span>Otomatik karar modu aktif</span>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
