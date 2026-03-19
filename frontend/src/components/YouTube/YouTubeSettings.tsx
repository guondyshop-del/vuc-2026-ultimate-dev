"use client";

import React, { useState, useEffect } from 'react';
import { Settings, Upload, User, Clock, Brain, BarChart3, DollarSign, Users, Shield, Wifi, Save, RotateCcw, Check, X, AlertTriangle } from 'lucide-react';

interface YouTubeContentSettings {
  default_category: string;
  default_privacy: string;
  default_made_for_kids: boolean;
  max_video_duration: number;
  max_file_size: number;
  supported_formats: string;
  thumbnail_max_size: number;
  thumbnail_formats: string;
}

interface YouTubeProfileSettings {
  channel_title: string;
  channel_description: string;
  channel_keywords: string;
  default_language: string;
  default_country: string;
  channel_privacy: string;
}

interface YouTubeScheduleSettings {
  auto_schedule_enabled: boolean;
  optimal_upload_times: string;
  timezone: string;
  batch_upload_enabled: boolean;
  max_concurrent_uploads: number;
  retry_attempts: number;
  retry_delay: number;
}

interface YouTubeOptimizationSettings {
  auto_tags_enabled: boolean;
  max_tags: number;
  tag_generation_model: string;
  title_optimization_enabled: boolean;
  description_templates_enabled: boolean;
  thumbnail_auto_generation: boolean;
}

interface YouTubeAnalyticsSettings {
  analytics_enabled: boolean;
  performance_tracking: boolean;
  audience_retention_analysis: boolean;
  engagement_monitoring: boolean;
  revenue_tracking: boolean;
  competitor_analysis: boolean;
}

interface YouTubeMonetizationSettings {
  monetization_enabled: boolean;
  ad_formats: string;
  content_suitability: string;
  auto_content_rating: boolean;
}

interface YouTubeCommunitySettings {
  auto_comments_response: boolean;
  comment_moderation: boolean;
  community_posts_enabled: boolean;
  live_streaming_enabled: boolean;
  premiere_features: boolean;
}

interface YouTubeSafetySettings {
  content_warnings: boolean;
  copyright_check: boolean;
  community_guidelines_check: boolean;
  child_safety_mode: boolean;
  auto_content_id_check: boolean;
}

interface YouTubeAPISettings {
  api_quota_enabled: boolean;
  daily_quota_limit: number;
  rate_limit_per_minute: number;
  burst_limit: number;
  quota_reset_time: string;
}

interface YouTubeAllSettings {
  content: YouTubeContentSettings;
  profile: YouTubeProfileSettings;
  schedule: YouTubeScheduleSettings;
  optimization: YouTubeOptimizationSettings;
  analytics: YouTubeAnalyticsSettings;
  monetization: YouTubeMonetizationSettings;
  community: YouTubeCommunitySettings;
  safety: YouTubeSafetySettings;
  api: YouTubeAPISettings;
}

const YouTubeSettings: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('content');
  const [settings, setSettings] = useState<YouTubeAllSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notification, setNotification] = useState<{ type: 'success' | 'error' | 'warning'; message: string } | null>(null);

  const categories = [
    { id: "1", title: "Film & Animation" },
    { id: "2", title: "Autos & Vehicles" },
    { id: "10", title: "Music" },
    { id: "15", title: "Pets & Animals" },
    { id: "17", title: "Sports" },
    { id: "19", title: "Travel & Events" },
    { id: "20", title: "Gaming" },
    { id: "22", title: "People & Blogs" },
    { id: "23", title: "Comedy" },
    { id: "24", title: "Entertainment" },
    { id: "25", title: "News & Politics" },
    { id: "26", title: "Howto & Style" },
    { id: "27", title: "Education" },
    { id: "28", title: "Science & Technology" },
    { id: "29", title: "Nonprofits & Activism" }
  ];

  const privacyOptions = [
    { value: "private", label: "Private" },
    { value: "unlisted", label: "Unlisted" },
    { value: "public", label: "Public" }
  ];

  const languages = [
    { code: "tr", name: "Türkçe" },
    { code: "en", name: "English" },
    { code: "de", name: "Deutsch" },
    { code: "fr", name: "Français" },
    { code: "es", name: "Español" }
  ];

  const countries = [
    { code: "TR", name: "Turkey" },
    { code: "US", name: "United States" },
    { code: "DE", name: "Germany" },
    { code: "FR", name: "France" },
    { code: "ES", name: "Spain" }
  ];

  const tabs = [
    { id: 'content', label: 'Content Settings', icon: Upload, description: 'Upload and content configuration' },
    { id: 'profile', label: 'Profile Settings', icon: User, description: 'Channel and profile information' },
    { id: 'schedule', label: 'Schedule', icon: Clock, description: 'Upload scheduling and automation' },
    { id: 'optimization', label: 'Optimization', icon: Brain, description: 'AI-powered optimization' },
    { id: 'analytics', label: 'Analytics', icon: BarChart3, description: 'Performance tracking' },
    { id: 'monetization', label: 'Monetization', icon: DollarSign, description: 'Revenue and ads configuration' },
    { id: 'community', label: 'Community', icon: Users, description: 'Engagement and interaction' },
    { id: 'safety', label: 'Safety', icon: Shield, description: 'Content safety and compliance' },
    { id: 'api', label: 'API Settings', icon: Wifi, description: 'API configuration and limits' }
  ];

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/youtube-settings');
      if (response.ok) {
        const data = await response.json();
        setSettings(data);
      } else {
        throw new Error('Failed to fetch settings');
      }
    } catch (error) {
      showNotification('error', 'Failed to load YouTube settings');
    } finally {
      setLoading(false);
    }
  };

  const saveSettings = async (category: string, categorySettings: any) => {
    try {
      setSaving(true);
      const response = await fetch(`/api/youtube-settings/${category}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(categorySettings),
      });

      if (response.ok) {
        showNotification('success', `${category} settings saved successfully`);
        fetchSettings(); // Refresh settings
      } else {
        throw new Error('Failed to save settings');
      }
    } catch (error) {
      showNotification('error', `Failed to save ${category} settings`);
    } finally {
      setSaving(false);
    }
  };

  const resetSettings = async () => {
    try {
      setSaving(true);
      const response = await fetch('/api/youtube-settings/reset', {
        method: 'POST',
      });

      if (response.ok) {
        showNotification('success', 'Settings reset to defaults');
        fetchSettings();
      } else {
        throw new Error('Failed to reset settings');
      }
    } catch (error) {
      showNotification('error', 'Failed to reset settings');
    } finally {
      setSaving(false);
    }
  };

  const showNotification = (type: 'success' | 'error' | 'warning', message: string) => {
    setNotification({ type, message });
    setTimeout(() => setNotification(null), 3000);
  };

  const updateSettings = (category: string, updates: Partial<any>) => {
    if (!settings) return;
    
    setSettings({
      ...settings,
      [category]: {
        ...settings[category as keyof YouTubeAllSettings],
        ...updates
      }
    });
  };

  const renderContentSettings = () => {
    if (!settings) return null;
    
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Default Category</label>
            <select
              value={settings.content.default_category}
              onChange={(e) => updateSettings('content', { default_category: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              aria-label="Select default video category"
              title="Default video category for uploads"
            >
              {categories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.title}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Default Privacy</label>
            <select
              value={settings.content.default_privacy}
              onChange={(e) => updateSettings('content', { default_privacy: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              aria-label="Select default privacy setting"
              title="Default privacy setting for uploads"
            >
              {privacyOptions.map(option => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="space-y-4">
          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.content.default_made_for_kids}
              onChange={(e) => updateSettings('content', { default_made_for_kids: e.target.checked })}
              className="rounded"
              aria-label="Default content made for kids"
              title="Mark content as made for kids by default"
            />
            <span className="text-sm font-medium text-gray-700">Default content made for kids</span>
          </label>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Max Video Duration (seconds)</label>
              <input
                type="number"
                value={settings.content.max_video_duration}
                onChange={(e) => updateSettings('content', { max_video_duration: parseInt(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                aria-label="Maximum video duration in seconds"
                title="Maximum allowed video duration in seconds"
                placeholder="14400"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Max File Size (bytes)</label>
              <input
                type="number"
                value={settings.content.max_file_size}
                onChange={(e) => updateSettings('content', { max_file_size: parseInt(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                aria-label="Maximum file size in bytes"
                title="Maximum allowed file size in bytes"
                placeholder="268435456000"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Supported Formats</label>
            <input
              type="text"
              value={settings.content.supported_formats}
              onChange={(e) => updateSettings('content', { supported_formats: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="mp4,webm,avi,mov,mpeg,flv,wmv"
              aria-label="Supported video formats"
              title="Comma-separated list of supported video formats"
            />
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={() => saveSettings('content', settings.content)}
            disabled={saving}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            {saving ? 'Saving...' : 'Save Content Settings'}
          </button>
        </div>
      </div>
    );
  };

  const renderProfileSettings = () => {
    if (!settings) return null;
    
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Channel Title</label>
            <input
              type="text"
              value={settings.profile.channel_title}
              onChange={(e) => updateSettings('profile', { channel_title: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              aria-label="Channel title"
              title="Your YouTube channel title"
              placeholder="Enter channel title"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Channel Keywords</label>
            <input
              type="text"
              value={settings.profile.channel_keywords}
              onChange={(e) => updateSettings('profile', { channel_keywords: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="technology,ai,development,programming,automation"
              aria-label="Channel keywords"
              title="Comma-separated keywords for your channel"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Channel Description</label>
          <textarea
            value={settings.profile.channel_description}
            onChange={(e) => updateSettings('profile', { channel_description: e.target.value })}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            aria-label="Channel description"
            title="Description of your YouTube channel"
            placeholder="Describe your channel content and purpose"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Default Language</label>
            <select
              value={settings.profile.default_language}
              onChange={(e) => updateSettings('profile', { default_language: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              aria-label="Default language"
              title="Default language for your content"
            >
              {languages.map(lang => (
                <option key={lang.code} value={lang.code}>{lang.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Default Country</label>
            <select
              value={settings.profile.default_country}
              onChange={(e) => updateSettings('profile', { default_country: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              aria-label="Default country"
              title="Default country for your channel"
            >
              {countries.map(country => (
                <option key={country.code} value={country.code}>{country.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Channel Privacy</label>
            <select
              value={settings.profile.channel_privacy}
              onChange={(e) => updateSettings('profile', { channel_privacy: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              aria-label="Channel privacy setting"
              title="Privacy setting for your channel"
            >
              {privacyOptions.map(option => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={() => saveSettings('profile', settings.profile)}
            disabled={saving}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            {saving ? 'Saving...' : 'Save Profile Settings'}
          </button>
        </div>
      </div>
    );
  };

  const renderTabContent = () => {
    if (loading) {
      return (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      );
    }

    switch (activeTab) {
      case 'content':
        return renderContentSettings();
      case 'profile':
        return renderProfileSettings();
      default:
        return (
          <div className="text-center py-12">
            <Settings className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">Settings for {activeTab} coming soon...</p>
          </div>
        );
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        {/* Header */}
        <div className="border-b border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">YouTube Settings</h1>
              <p className="text-sm text-gray-600 mt-1">Configure your YouTube integration and content sharing preferences</p>
            </div>
            <button
              onClick={resetSettings}
              disabled={saving}
              className="px-4 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2"
            >
              <RotateCcw className="w-4 h-4" />
              Reset to Defaults
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-3 px-1 py-4 border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-600 text-blue-600'
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
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {renderTabContent()}
        </div>
      </div>

      {/* Notification */}
      {notification && (
        <div className={`fixed bottom-4 right-4 p-4 rounded-lg shadow-lg flex items-center gap-3 z-50 ${
          notification.type === 'success' ? 'bg-green-500 text-white' :
          notification.type === 'error' ? 'bg-red-500 text-white' :
          'bg-yellow-500 text-white'
        }`}>
          {notification.type === 'success' && <Check className="w-5 h-5" />}
          {notification.type === 'error' && <X className="w-5 h-5" />}
          {notification.type === 'warning' && <AlertTriangle className="w-5 h-5" />}
          <span>{notification.message}</span>
        </div>
      )}
    </div>
  );
};

export default YouTubeSettings;
