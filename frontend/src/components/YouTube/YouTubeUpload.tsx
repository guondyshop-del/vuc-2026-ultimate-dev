"use client";

import React, { useState, useRef } from 'react';
import { Upload, FileVideo, X, Eye, Clock, Calendar, Tag, Settings, Play, AlertCircle } from 'lucide-react';

interface VideoMetadata {
  title: string;
  description: string;
  tags: string[];
  category_id: string;
  privacy_status: string;
  made_for_kids: boolean;
}

interface YouTubeUploadProps {
  onUploadComplete?: (result: any) => void;
}

const YouTubeUpload: React.FC<YouTubeUploadProps> = ({ onUploadComplete }) => {
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [thumbnailFile, setThumbnailFile] = useState<File | null>(null);
  const [metadata, setMetadata] = useState<VideoMetadata>({
    title: '',
    description: '',
    tags: [],
    category_id: '22',
    privacy_status: 'private',
    made_for_kids: false
  });
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [validation, setValidation] = useState<any>(null);
  const [tagInput, setTagInput] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);
  const thumbnailInputRef = useRef<HTMLInputElement>(null);

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
    { value: "private", label: "Private", description: "Only you can view" },
    { value: "unlisted", label: "Unlisted", description: "Anyone with link can view" },
    { value: "public", label: "Public", description: "Everyone can view" }
  ];

  const handleVideoFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setVideoFile(file);
      
      // Validate file
      const formData = new FormData();
      formData.append('video_file', file);
      
      try {
        const response = await fetch('/api/youtube/validate/video', {
          method: 'POST',
          body: formData
        });
        const result = await response.json();
        setValidation(result.data);
      } catch (error) {
        console.error('Validation error:', error);
        setValidation({ valid: false, error: 'Validation failed' });
      }
    }
  };

  const handleThumbnailFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setThumbnailFile(file);
    }
  };

  const addTag = () => {
    if (tagInput.trim() && !metadata.tags.includes(tagInput.trim())) {
      setMetadata({
        ...metadata,
        tags: [...metadata.tags, tagInput.trim()]
      });
      setTagInput('');
    }
  };

  const removeTag = (tagToRemove: string) => {
    setMetadata({
      ...metadata,
      tags: metadata.tags.filter(tag => tag !== tagToRemove)
    });
  };

  const handleUpload = async () => {
    if (!videoFile || !metadata.title.trim()) {
      alert('Please select a video file and provide a title');
      return;
    }

    setUploading(true);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append('video_file', videoFile);
      formData.append('title', metadata.title);
      formData.append('description', metadata.description);
      formData.append('tags', metadata.tags.join(','));
      formData.append('category_id', metadata.category_id);
      formData.append('privacy_status', metadata.privacy_status);
      formData.append('made_for_kids', metadata.made_for_kids.toString());
      
      if (thumbnailFile) {
        formData.append('thumbnail_file', thumbnailFile);
      }

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 1000);

      const response = await fetch('/api/youtube/upload', {
        method: 'POST',
        body: formData
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      const result = await response.json();
      
      if (result.success) {
        onUploadComplete?.(result.data);
        // Reset form
        setVideoFile(null);
        setThumbnailFile(null);
        setMetadata({
          title: '',
          description: '',
          tags: [],
          category_id: '22',
          privacy_status: 'private',
          made_for_kids: false
        });
      } else {
        alert('Upload failed: ' + (result.data?.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Upload to YouTube</h1>
        
        {/* Video File Upload */}
        <div className="space-y-4">
          <div>
            <label htmlFor="video-file" className="block text-sm font-medium text-gray-700 mb-2">Video File</label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
              <input
                ref={fileInputRef}
                type="file"
                accept="video/*"
                onChange={handleVideoFileChange}
                className="hidden"
                id="video-file"
                aria-label="Select a video file"
              />
              
              {videoFile ? (
                <div className="space-y-3">
                  <div className="flex items-center justify-center">
                    <FileVideo className="w-12 h-12 text-blue-600" />
                  </div>
                  <div className="text-sm">
                    <p className="font-medium text-gray-900">{videoFile.name}</p>
                    <p className="text-gray-500">{formatFileSize(videoFile.size)}</p>
                  </div>
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="text-sm text-blue-600 hover:text-blue-700"
                    aria-label="Choose different video file"
                  >
                    Choose different file
                  </button>
                </div>
              ) : (
                <div className="space-y-3">
                  <div className="flex items-center justify-center">
                    <Upload className="w-12 h-12 text-gray-400" />
                  </div>
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                    aria-label="Select a video file"
                  >
                    Choose Video File
                  </button>
                  <p className="text-sm text-gray-500 mt-2">
                    MP4, WebM, AVI, MOV up to 256GB
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Validation Results */}
          {validation && (
            <div className={`p-4 rounded-lg ${validation.valid ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
              <div className="flex items-start gap-3">
                {validation.valid ? (
                  <div className="text-green-600">
                    <Eye className="w-5 h-5" />
                  </div>
                ) : (
                  <div className="text-red-600">
                    <AlertCircle className="w-5 h-5" />
                  </div>
                )}
                <div className="flex-1">
                  <p className={`font-medium ${validation.valid ? 'text-green-900' : 'text-red-900'}`}>
                    {validation.valid ? 'Video validated successfully' : 'Validation failed'}
                  </p>
                  {validation.error && (
                    <p className="text-sm text-red-700 mt-1">{validation.error}</p>
                  )}
                  {validation.valid && (
                    <div className="text-sm text-green-700 mt-1">
                      <p>Duration: {Math.floor(validation.duration / 60)}:{(validation.duration % 60).toString().padStart(2, '0')}</p>
                      <p>Format: {validation.mime_type}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Thumbnail Upload */}
          <div>
            <label htmlFor="thumbnail-file" className="block text-sm font-medium text-gray-700 mb-2">Thumbnail (Optional)</label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
              <input
                ref={thumbnailInputRef}
                type="file"
                accept="image/*"
                onChange={handleThumbnailFileChange}
                className="hidden"
                id="thumbnail-file"
                aria-label="Select a thumbnail file"
              />
              
              {thumbnailFile ? (
                <div className="space-y-3">
                  <img
                    src={URL.createObjectURL(thumbnailFile)}
                    alt="Thumbnail preview"
                    className="w-32 h-18 object-cover mx-auto rounded"
                  />
                  <div className="text-sm">
                    <p className="font-medium text-gray-900">{thumbnailFile.name}</p>
                    <p className="text-gray-500">{formatFileSize(thumbnailFile.size)}</p>
                  </div>
                  <button
                    onClick={() => thumbnailInputRef.current?.click()}
                    className="text-sm text-blue-600 hover:text-blue-700"
                    aria-label="Choose different thumbnail file"
                  >
                    Choose different thumbnail
                  </button>
                </div>
              ) : (
                <div className="space-y-3">
                  <div className="flex items-center justify-center">
                    <Upload className="w-8 h-8 text-gray-400" />
                  </div>
                  <button
                    onClick={() => thumbnailInputRef.current?.click()}
                    className="px-3 py-1 text-sm bg-gray-600 text-white rounded hover:bg-gray-700"
                    aria-label="Select a thumbnail file"
                  >
                    Choose Thumbnail
                  </button>
                  <p className="text-xs text-gray-500">
                    JPG, PNG, GIF up to 2MB
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Metadata */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">Title *</label>
              <input
                type="text"
                value={metadata.title}
                onChange={(e) => setMetadata({...metadata, title: e.target.value})}
                maxLength={100}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                id="title"
                aria-label="Enter video title"
                placeholder="Enter video title"
              />
              <p className="text-xs text-gray-500 mt-1">{metadata.title.length}/100 characters</p>
            </div>

            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">Category</label>
              <select
                value={metadata.category_id}
                onChange={(e) => setMetadata({...metadata, category_id: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                id="category"
                aria-label="Select video category"
              >
                {categories.map(cat => (
                  <option key={cat.id} value={cat.id}>{cat.title}</option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea
              value={metadata.description}
              onChange={(e) => setMetadata({...metadata, description: e.target.value})}
              maxLength={5000}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              id="description"
              aria-label="Enter video description"
              placeholder="Describe your video"
            />
            <p className="text-xs text-gray-500 mt-1">{metadata.description.length}/5000 characters</p>
          </div>

          <div>
            <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-2">Tags</label>
            <div className="space-y-3">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
                  placeholder="Add a tag"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  id="tags"
                  aria-label="Enter a tag"
                />
                <button
                  onClick={addTag}
                  className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
                  aria-label="Add tag"
                >
                  Add
                </button>
              </div>
              
              {metadata.tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {metadata.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                    >
                      <Tag className="w-3 h-3" />
                      {tag}
                      <button
                        onClick={() => removeTag(tag)}
                        className="hover:text-blue-900"
                        aria-label={`Remove tag ${tag}`}
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="privacy" className="block text-sm font-medium text-gray-700 mb-2">Privacy</label>
              <div className="space-y-2">
                {privacyOptions.map(option => (
                  <label key={option.value} className="flex items-start gap-3">
                    <input
                      type="radio"
                      name="privacy"
                      value={option.value}
                      checked={metadata.privacy_status === option.value}
                      onChange={(e) => setMetadata({...metadata, privacy_status: e.target.value})}
                      className="mt-1"
                      id={`privacy-${option.value}`}
                      aria-label={option.label}
                    />
                    <div>
                      <p className="font-medium text-gray-900">{option.label}</p>
                      <p className="text-sm text-gray-500">{option.description}</p>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label htmlFor="made-for-kids" className="block text-sm font-medium text-gray-700 mb-2">Content Settings</label>
              <label className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={metadata.made_for_kids}
                  onChange={(e) => setMetadata({...metadata, made_for_kids: e.target.checked})}
                  className="rounded"
                  id="made-for-kids"
                  aria-label="This content is intended for children"
                />
                <div>
                  <p className="font-medium text-gray-900">Made for kids</p>
                  <p className="text-sm text-gray-500">This content is intended for children</p>
                </div>
              </label>
            </div>
          </div>

          {/* Upload Progress */}
          {uploading && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="font-medium">Uploading...</span>
                <span>{uploadProgress}%</span>
              </div>
              <div className="upload-progress">
                <div
                  className="upload-progress-fill"
                  data-progress={uploadProgress}
                  aria-label={`Upload progress: ${uploadProgress}%`}
                />
              </div>
            </div>
          )}

          {/* Upload Button */}
          <div className="flex justify-end">
            <button
              onClick={handleUpload}
              disabled={uploading || !videoFile || !metadata.title.trim() || (validation && !validation.valid)}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <Upload className="w-4 h-4" />
              {uploading ? 'Uploading...' : 'Upload Video'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default YouTubeUpload;
