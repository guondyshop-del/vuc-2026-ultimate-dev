"use client";

import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Users, Eye, ThumbsUp, MessageCircle, Clock, Calendar, Download, Filter } from 'lucide-react';

interface AnalyticsData {
  channel_id: string;
  channel_title: string;
  total_views: number;
  total_subscribers: number;
  total_videos: number;
  watch_time_hours: number;
  average_view_duration: number;
  subscriber_growth: number;
  revenue_total: number;
  top_videos: string[];
  demographics: {
    age_groups: Record<string, number>;
    genders: Record<string, number>;
    devices: Record<string, number>;
  };
}

interface VideoAnalytics {
  video_id: string;
  title: string;
  views: number;
  likes: number;
  comments: number;
  shares: number;
  watch_time_minutes: number;
  average_view_duration: number;
  audience_retention: number;
  click_through_rate: number;
  impressions: number;
  unique_viewers: number;
  revenue: number;
  published_at: string;
}

interface YouTubeAnalyticsProps {
  channelId: string;
}

const YouTubeAnalytics: React.FC<YouTubeAnalyticsProps> = ({ channelId }) => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [videoAnalytics, setVideoAnalytics] = useState<VideoAnalytics[]>([]);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState({
    start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0]
  });
  const [selectedMetric, setSelectedMetric] = useState('views');

  useEffect(() => {
    fetchAnalytics();
  }, [channelId, dateRange]);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        start_date: dateRange.start,
        end_date: dateRange.end
      });

      const response = await fetch(`/api/youtube/analytics/channel/${channelId}?${params}`);
      const data = await response.json();
      
      if (data.success) {
        setAnalytics(data.data);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const formatDuration = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  const exportReport = async (format: string) => {
    try {
      const params = new URLSearchParams({
        channel_id: channelId,
        start_date: dateRange.start,
        end_date: dateRange.end,
        format
      });

      const response = await fetch(`/api/youtube/analytics/export?${params}`);
      const data = await response.json();
      
      if (data.success) {
        // Create download link
        const link = document.createElement('a');
        link.href = `/api/reports/${data.data.report_path.split('/').pop()}`;
        link.download = data.data.report_path.split('/').pop();
        link.click();
      }
    } catch (error) {
      console.error('Error exporting report:', error);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto p-6">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="h-32 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="max-w-7xl mx-auto p-6">
        <div className="text-center py-12">
          <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No analytics data available</h3>
          <p className="text-gray-500">Connect your YouTube channel to view analytics</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">YouTube Analytics</h1>
            <p className="text-gray-600">{analytics.channel_title}</p>
          </div>
          <div className="flex items-center gap-4">
            <div>
              <label htmlFor="start-date" className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
              <input
                type="date"
                value={dateRange.start}
                onChange={(e) => setDateRange({...dateRange, start: e.target.value})}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                id="start-date"
              />
            </div>
            <div>
              <label htmlFor="end-date" className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
              <input
                type="date"
                value={dateRange.end}
                onChange={(e) => setDateRange({...dateRange, end: e.target.value})}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                id="end-date"
              />
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => exportReport('csv')}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                Export CSV
              </button>
              <button
                onClick={() => exportReport('json')}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                Export JSON
              </button>
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-blue-50 rounded-lg p-6">
            <div className="flex items-center justify-between mb-2">
              <Eye className="w-8 h-8 text-blue-600" />
              <span className="text-sm text-blue-600 font-medium">Total Views</span>
            </div>
            <p className="text-2xl font-bold text-blue-900">{formatNumber(analytics.total_views)}</p>
            <p className="text-sm text-blue-700 mt-1">All time</p>
          </div>

          <div className="bg-green-50 rounded-lg p-6">
            <div className="flex items-center justify-between mb-2">
              <Users className="w-8 h-8 text-green-600" />
              <span className="text-sm text-green-600 font-medium">Subscribers</span>
            </div>
            <p className="text-2xl font-bold text-green-900">{formatNumber(analytics.total_subscribers)}</p>
            <p className="text-sm text-green-700 mt-1">
              {analytics.subscriber_growth > 0 ? '+' : ''}{formatNumber(analytics.subscriber_growth)} this period
            </p>
          </div>

          <div className="bg-purple-50 rounded-lg p-6">
            <div className="flex items-center justify-between mb-2">
              <Clock className="w-8 h-8 text-purple-600" />
              <span className="text-sm text-purple-600 font-medium">Watch Time</span>
            </div>
            <p className="text-2xl font-bold text-purple-900">{formatNumber(Math.floor(analytics.watch_time_hours))}h</p>
            <p className="text-sm text-purple-700 mt-1">Avg: {formatDuration(analytics.average_view_duration)}</p>
          </div>

          <div className="bg-orange-50 rounded-lg p-6">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="w-8 h-8 text-orange-600" />
              <span className="text-sm text-orange-600 font-medium">Videos</span>
            </div>
            <p className="text-2xl font-bold text-orange-900">{analytics.total_videos}</p>
            <p className="text-sm text-orange-700 mt-1">Total content</p>
          </div>
        </div>
      </div>

      {/* Demographics */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Audience Demographics</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Age Groups */}
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-3">Age Groups</h3>
            <div className="space-y-2">
              {Object.entries(analytics.demographics.age_groups).map(([age, count]) => (
                <div key={age} className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">{age}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-24 bg-gray-200 rounded-full h-2">
                      <div className="progress-bar">
                        <div
                          className="progress-bar-fill"
                          data-progress={Math.round((count / Math.max(...Object.values(analytics.demographics.age_groups))) * 100)}
                        />
                      </div>
                    </div>
                    <span className="text-sm text-gray-900 w-12 text-right">{formatNumber(count)}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Gender */}
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-3">Gender</h3>
            <div className="space-y-2">
              {Object.entries(analytics.demographics.genders).map(([gender, count]) => (
                <div key={gender} className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 capitalize">{gender}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-24 bg-gray-200 rounded-full h-2">
                      <div className="progress-bar">
                        <div
                          className="analytics-bar-green"
                          data-width={Math.round((count / Math.max(...Object.values(analytics.demographics.genders))) * 100)}
                        />
                      </div>
                    </div>
                    <span className="text-sm text-gray-900 w-12 text-right">{formatNumber(count)}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Devices */}
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-3">Devices</h3>
            <div className="space-y-2">
              {Object.entries(analytics.demographics.devices).map(([device, count]) => (
                <div key={device} className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 capitalize">{device}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-24 bg-gray-200 rounded-full h-2">
                      <div className="progress-bar">
                        <div
                          className="analytics-bar-purple"
                          data-width={Math.round((count / Math.max(...Object.values(analytics.demographics.devices))) * 100)}
                        />
                      </div>
                    </div>
                    <span className="text-sm text-gray-900 w-12 text-right">{formatNumber(count)}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Top Videos */}
      {analytics.top_videos.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Top Performing Videos</h2>
          <div className="space-y-4">
            {analytics.top_videos.map((videoTitle, index) => (
              <div key={index} className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-sm">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{videoTitle}</p>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <Eye className="w-4 h-4" />
                  <span>High performance</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Performance Chart Placeholder */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Performance Trends</h2>
          <select
            value={selectedMetric}
            onChange={(e) => setSelectedMetric(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            aria-label="Select performance metric"
          >
            <option value="views">Views</option>
            <option value="subscribers">Subscribers</option>
            <option value="engagement">Engagement</option>
            <option value="revenue">Revenue</option>
          </select>
        </div>
        
        <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
          <div className="text-center">
            <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">Performance chart would be displayed here</p>
            <p className="text-sm text-gray-400 mt-1">Integration with charting library needed</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default YouTubeAnalytics;
