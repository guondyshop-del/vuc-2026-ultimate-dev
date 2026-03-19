"use client";

import React, { useState } from 'react';
import { Brain, TrendingUp, Target, Zap, Lightbulb, BarChart3, Users, Video, Clock, Star } from 'lucide-react';

interface ContentStrategy {
  title_optimization: string;
  description_optimization: string;
  tags_optimization: string[];
  thumbnail_suggestions: string[];
  publish_timing: string;
  target_audience: any;
  predicted_performance: number;
  confidence_score: number;
}

interface TrendingPattern {
  pattern_type: string;
  keywords: string[];
  topics: string[];
  duration_trend: string;
  style_preferences: any;
  engagement_factors: string[];
  virality_score: number;
  time_sensitivity: number;
}

interface CompetitiveInsight {
  competitor_channel: string;
  top_performing_content: string[];
  content_gaps: string[];
  engagement_strategies: any;
  market_position: string;
  opportunity_score: number;
}

const YouTubeNeuralCore: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'strategy' | 'trends' | 'competition'>('strategy');
  const [loading, setLoading] = useState(false);
  const [strategy, setStrategy] = useState<ContentStrategy | null>(null);
  const [trends, setTrends] = useState<TrendingPattern[]>([]);
  const [competition, setCompetition] = useState<CompetitiveInsight[]>([]);
  
  const [formData, setFormData] = useState({
    video_topic: '',
    target_audience: {
      age_groups: 'mixed',
      interests: '',
      experience_level: 'beginner'
    },
    competitor_analysis: true
  });

  const generateStrategy = async () => {
    if (!formData.video_topic.trim()) {
      alert('Please enter a video topic');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/youtube/neural/strategy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const result = await response.json();
      
      if (result.success) {
        setStrategy(result.data);
      }
    } catch (error) {
      console.error('Error generating strategy:', error);
    } finally {
      setLoading(false);
    }
  };

  const analyzeTrends = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/youtube/neural/trends?region=US');
      const result = await response.json();
      
      if (result.success) {
        setTrends(result.data.patterns);
      }
    } catch (error) {
      console.error('Error analyzing trends:', error);
    } finally {
      setLoading(false);
    }
  };

  const analyzeCompetition = async (channelId: string) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/youtube/neural/competition/${channelId}`);
      const result = await response.json();
      
      if (result.success) {
        setCompetition(result.data.insights);
      }
    } catch (error) {
      console.error('Error analyzing competition:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPerformanceColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 bg-green-50';
    if (score >= 0.6) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.85) return 'text-green-600';
    if (score >= 0.7) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-6">
          <Brain className="w-8 h-8 text-purple-600" />
          <div>
            <h1 className="text-2xl font-bold text-gray-900">VUC-2026 Neural Core</h1>
            <p className="text-gray-600">AI-powered YouTube optimization and automation</p>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
          <button
            onClick={() => setActiveTab('strategy')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-colors ${
              activeTab === 'strategy'
                ? 'bg-white text-purple-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Target className="w-4 h-4" />
            Content Strategy
          </button>
          <button
            onClick={() => setActiveTab('trends')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-colors ${
              activeTab === 'trends'
                ? 'bg-white text-purple-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <TrendingUp className="w-4 h-4" />
            Trend Analysis
          </button>
          <button
            onClick={() => setActiveTab('competition')}
            className={`flex items-center gap-2 px-4 py-2 rounded-md transition-colors ${
              activeTab === 'competition'
                ? 'bg-white text-purple-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            Competition
          </button>
        </div>
      </div>

      {/* Content Strategy Tab */}
      {activeTab === 'strategy' && (
        <div className="space-y-6">
          {/* Strategy Generator */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Generate Content Strategy</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="video-topic" className="block text-sm font-medium text-gray-700 mb-2">Video Topic *</label>
                <input
                  type="text"
                  value={formData.video_topic}
                  onChange={(e) => setFormData({...formData, video_topic: e.target.value})}
                  placeholder="Enter your video topic"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  id="video-topic"
                  aria-required="true"
                />
              </div>

              <div>
                <label htmlFor="age-groups" className="block text-sm font-medium text-gray-700 mb-2">Target Audience</label>
                <select
                  value={formData.target_audience.age_groups}
                  onChange={(e) => setFormData({
                    ...formData,
                    target_audience: {...formData.target_audience, age_groups: e.target.value}
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  id="age-groups"
                  aria-label="Select target audience age group"
                >
                  <option value="mixed">Mixed Age Groups</option>
                  <option value="young">18-24 years</option>
                  <option value="adult">25-44 years</option>
                  <option value="mature">45+ years</option>
                </select>
              </div>

              <div>
                <label htmlFor="interests" className="block text-sm font-medium text-gray-700 mb-2">Interests</label>
                <input
                  type="text"
                  value={formData.target_audience.interests}
                  onChange={(e) => setFormData({
                    ...formData,
                    target_audience: {...formData.target_audience, interests: e.target.value}
                  })}
                  placeholder="e.g., technology, gaming, education"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  id="interests"
                />
              </div>

              <div>
                <label htmlFor="experience-level" className="block text-sm font-medium text-gray-700 mb-2">Experience Level</label>
                <select
                  value={formData.target_audience.experience_level}
                  onChange={(e) => setFormData({
                    ...formData,
                    target_audience: {...formData.target_audience, experience_level: e.target.value}
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  id="experience-level"
                  aria-label="Select experience level"
                >
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                  <option value="expert">Expert</option>
                </select>
              </div>
            </div>

            <div className="flex items-center gap-4 mt-6">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={formData.competitor_analysis}
                  onChange={(e) => setFormData({...formData, competitor_analysis: e.target.checked})}
                  className="rounded"
                  id="competitor-analysis"
                  aria-label="Include competitor analysis"
                />
                <span className="text-sm text-gray-700">Include competitor analysis</span>
              </label>
              
              <button
                onClick={generateStrategy}
                disabled={loading}
                className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 flex items-center gap-2"
              >
                <Zap className="w-4 h-4" />
                {loading ? 'Generating...' : 'Generate Strategy'}
              </button>
            </div>
          </div>

          {/* Strategy Results */}
          {strategy && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">AI-Generated Strategy</h3>
                <div className="flex items-center gap-4">
                  <div className="text-sm">
                    <span className="text-gray-500">Performance Score:</span>
                    <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${getPerformanceColor(strategy.predicted_performance)}`}>
                      {(strategy.predicted_performance * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-500">Confidence:</span>
                    <span className={`ml-2 font-medium ${getConfidenceColor(strategy.confidence_score)}`}>
                      {(strategy.confidence_score * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-2">
                    <Video className="w-4 h-4" />
                    Optimized Title
                  </h4>
                  <p className="text-gray-700 bg-gray-50 p-3 rounded-lg">{strategy.title_optimization}</p>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-2">
                    <Clock className="w-4 h-4" />
                    Best Publish Time
                  </h4>
                  <p className="text-gray-700 bg-gray-50 p-3 rounded-lg">
                    {new Date(strategy.publish_timing).toLocaleString()}
                  </p>
                </div>

                <div className="md:col-span-2">
                  <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-2">
                    <Lightbulb className="w-4 h-4" />
                    Optimized Description
                  </h4>
                  <p className="text-gray-700 bg-gray-50 p-3 rounded-lg max-h-32 overflow-y-auto">
                    {strategy.description_optimization}
                  </p>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-2">
                    <Star className="w-4 h-4" />
                    Recommended Tags
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {strategy.tags_optimization.map((tag, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-2">
                    <Target className="w-4 h-4" />
                    Thumbnail Ideas
                  </h4>
                  <ul className="space-y-1">
                    {strategy.thumbnail_suggestions.map((suggestion, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-center gap-2">
                        <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                        {suggestion}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Trend Analysis Tab */}
      {activeTab === 'trends' && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Trending Pattern Analysis</h2>
              <button
                onClick={analyzeTrends}
                disabled={loading}
                className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 flex items-center gap-2"
              >
                <TrendingUp className="w-4 h-4" />
                {loading ? 'Analyzing...' : 'Analyze Trends'}
              </button>
            </div>

            {trends.length > 0 && (
              <div className="space-y-6">
                {trends.map((pattern, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-semibold text-gray-900 capitalize">{pattern.pattern_type}</h3>
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-gray-500">Virality Score:</span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPerformanceColor(pattern.virality_score)}`}>
                          {(pattern.virality_score * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-2">Trending Keywords</h4>
                        <div className="flex flex-wrap gap-2">
                          {pattern.keywords.slice(0, 8).map((keyword, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm"
                            >
                              {keyword}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-2">Hot Topics</h4>
                        <div className="flex flex-wrap gap-2">
                          {pattern.topics.slice(0, 6).map((topic, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-green-100 text-green-700 rounded text-sm"
                            >
                              {topic}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-2">Engagement Factors</h4>
                        <div className="flex flex-wrap gap-2">
                          {pattern.engagement_factors.map((factor, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-sm"
                            >
                              {factor}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-2">Content Style</h4>
                        <div className="space-y-1 text-sm text-gray-600">
                          <div>Duration: <span className="font-medium">{pattern.duration_trend}</span></div>
                          <div>Time Sensitive: <span className="font-medium">{pattern.time_sensitivity}h</span></div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Competition Tab */}
      {activeTab === 'competition' && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Competitive Analysis</h2>
            
            <div className="mb-6">
              <label htmlFor="channel-id" className="block text-sm font-medium text-gray-700 mb-2">Channel ID</label>
              <div className="flex gap-4">
                <input
                  type="text"
                  placeholder="Enter YouTube channel ID"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                  id="channel-id"
                  aria-label="Enter YouTube channel ID"
                />
                <button
                  onClick={() => {
                    const input = document.querySelector('input[placeholder="Enter YouTube channel ID"]') as HTMLInputElement;
                    if (input.value) {
                      analyzeCompetition(input.value);
                    }
                  }}
                  disabled={loading}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 flex items-center gap-2"
                >
                  <BarChart3 className="w-4 h-4" />
                  {loading ? 'Analyzing...' : 'Analyze'}
                </button>
              </div>
            </div>

            {competition.length > 0 && (
              <div className="space-y-6">
                {competition.map((insight, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-semibold text-gray-900">{insight.competitor_channel}</h3>
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-gray-500">Opportunity Score:</span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPerformanceColor(insight.opportunity_score)}`}>
                          {(insight.opportunity_score * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-2">Top Content</h4>
                        <ul className="space-y-1">
                          {insight.top_performing_content.slice(0, 3).map((content, idx) => (
                            <li key={idx} className="text-sm text-gray-600 flex items-center gap-2">
                              <div className="neural-progress">
                                <div
                                  className="neural-progress-fill"
                                  data-progress={80}
                                />
                              </div>
                              {content}
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-2">Content Gaps</h4>
                        <div className="flex flex-wrap gap-2">
                          {insight.content_gaps.map((gap, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-orange-100 text-orange-700 rounded text-sm"
                            >
                              {gap}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div className="md:col-span-2">
                        <h4 className="text-sm font-medium text-gray-700 mb-2">Market Position</h4>
                        <div className="flex items-center gap-4">
                          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                            insight.market_position === 'competitive' 
                              ? 'bg-red-100 text-red-700'
                              : 'bg-yellow-100 text-yellow-700'
                          }`}>
                            {insight.market_position}
                          </span>
                          <span className="text-sm text-gray-600">
                            Posting frequency: {insight.engagement_strategies.posting_frequency?.toFixed(1) || 'N/A'} videos/month
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default YouTubeNeuralCore;
