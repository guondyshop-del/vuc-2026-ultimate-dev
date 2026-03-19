"use client";

import React, { useState } from 'react';
import { Search, Upload, BarChart3, Brain, Settings, Play, Users, TrendingUp, Youtube } from 'lucide-react';
import YouTubeSearch from '../components/YouTube/YouTubeSearch';
import YouTubeUpload from '../components/YouTube/YouTubeUpload';
import YouTubeAnalytics from '../components/YouTube/YouTubeAnalytics';
import YouTubeNeuralCore from '../components/YouTube/YouTubeNeuralCore';
import YouTubeSettings from '../components/YouTube/YouTubeSettings';

const YouTubeDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'search' | 'upload' | 'analytics' | 'neural' | 'settings'>('search');
  const [selectedVideo, setSelectedVideo] = useState<any>(null);

  const tabs = [
    { id: 'search', label: 'Search', icon: Search, description: 'Find YouTube content' },
    { id: 'upload', label: 'Upload', icon: Upload, description: 'Upload videos to YouTube' },
    { id: 'analytics', label: 'Analytics', icon: BarChart3, description: 'View performance metrics' },
    { id: 'neural', label: 'Neural Core', icon: Brain, description: 'AI-powered optimization' },
    { id: 'settings', label: 'Settings', icon: Settings, description: 'Configure YouTube settings' }
  ];

  const handleVideoSelect = (video: any) => {
    setSelectedVideo(video);
    // You could open a modal or navigate to a video detail page
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'search':
        return <YouTubeSearch onVideoSelect={handleVideoSelect} />;
      case 'upload':
        return <YouTubeUpload onUploadComplete={(result) => console.log('Upload complete:', result)} />;
      case 'analytics':
        return <YouTubeAnalytics channelId="YOUR_CHANNEL_ID" />;
      case 'neural':
        return <YouTubeNeuralCore />;
      case 'settings':
        return <YouTubeSettings />;
      default:
        return <YouTubeSearch onVideoSelect={handleVideoSelect} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-red-600 rounded-lg">
                <Youtube className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">YouTube Integration</h1>
                <p className="text-sm text-gray-600">VUC-2026 Ultimate YouTube Management</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                API Connected
              </div>
              <button 
                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg" 
                aria-label="Open settings"
                title="Settings"
              >
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-3 px-1 py-4 border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-red-600 text-red-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <div className="text-left">
                    <div className="font-medium">{tab.label}</div>
                    <div className="text-xs text-gray-500">{tab.description}</div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6">
        {renderContent()}
      </main>

      {/* Selected Video Modal (optional) */}
      {selectedVideo && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto m-4">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-xl font-bold text-gray-900">{selectedVideo.title}</h2>
                <button
                  onClick={() => setSelectedVideo(null)}
                  className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
                  aria-label="Close video modal"
                  title="Close modal"
                >
                  ×
                </button>
              </div>
              
              <div className="aspect-video bg-gray-100 rounded-lg mb-4">
                <iframe
                  src={selectedVideo.embed_url}
                  title={selectedVideo.title}
                  className="w-full h-full rounded-lg"
                  allowFullScreen
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div className="flex items-center gap-2">
                  <Play className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-600">
                    {selectedVideo.view_count?.toLocaleString()} views
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-600">
                    {selectedVideo.channel_title}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-600">
                    {new Date(selectedVideo.published_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
              
              <div className="text-gray-700">
                <p className="whitespace-pre-wrap">{selectedVideo.description}</p>
              </div>
              
              {selectedVideo.tags && selectedVideo.tags.length > 0 && (
                <div className="mt-4">
                  <h3 className="text-sm font-medium text-gray-900 mb-2">Tags</h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedVideo.tags.map((tag: string, index: number) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default YouTubeDashboard;
