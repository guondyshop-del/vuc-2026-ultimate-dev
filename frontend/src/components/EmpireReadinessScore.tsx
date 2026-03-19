'use client';

import { useState, useEffect } from 'react';
import { Progress } from '@/components/ui/progress';
import { Shield, Zap, AlertCircle, CheckCircle } from 'lucide-react';

const getWidthClass = (percentage: number) => {
  if (percentage === 0) return 'w-0';
  if (percentage <= 25) return 'w-1/4';
  if (percentage <= 50) return 'w-1/2';
  if (percentage <= 75) return 'w-3/4';
  return 'w-full';
};

interface ReadinessMetric {
  id: string;
  label: string;
  value: number;
  max: number;
  icon: React.ElementType;
  status: 'complete' | 'partial' | 'missing';
}

export default function EmpireReadinessScore() {
  const [readiness, setReadiness] = useState(0);
  const [metrics, setMetrics] = useState<ReadinessMetric[]>([
    {
      id: 'api_connections',
      label: 'API Bağlantıları',
      value: 0,
      max: 4,
      icon: Shield,
      status: 'missing'
    },
    {
      id: 'persona_setup',
      label: 'Persona Konfigürasyonu',
      value: 0,
      max: 2,
      icon: Zap,
      status: 'missing'
    },
    {
      id: 'proxy_health',
      label: 'Proxy Sağlığı',
      value: 0,
      max: 3,
      icon: Shield,
      status: 'missing'
    },
    {
      id: 'strategy_config',
      label: 'Strateji Ayarları',
      value: 0,
      max: 3,
      icon: Zap,
      status: 'missing'
    }
  ]);

  useEffect(() => {
    // Simulate real-time readiness calculation
    const calculateReadiness = () => {
      const totalValue = metrics.reduce((sum, metric) => sum + metric.value, 0);
      const totalMax = metrics.reduce((sum, metric) => sum + metric.max, 0);
      const score = Math.round((totalValue / totalMax) * 100);
      setReadiness(score);

      // Update metric statuses
      const updatedMetrics = metrics.map(metric => {
        const percentage = (metric.value / metric.max) * 100;
        let status: 'complete' | 'partial' | 'missing' = 'missing';
        if (percentage === 100) status = 'complete';
        else if (percentage > 0) status = 'partial';
        
        return { ...metric, status };
      });
      setMetrics(updatedMetrics);
    };

    calculateReadiness();
    const interval = setInterval(calculateReadiness, 5000);
    return () => clearInterval(interval);
  }, []); // Empty dependency array to prevent infinite loop

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'complete': return 'text-green-400';
      case 'partial': return 'text-yellow-400';
      case 'missing': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'complete': return <CheckCircle className="w-4 h-4" />;
      case 'partial': return <AlertCircle className="w-4 h-4" />;
      case 'missing': return <AlertCircle className="w-4 h-4" />;
      default: return null;
    }
  };

  const getProgressColor = (value: number, max: number) => {
    const percentage = (value / max) * 100;
    if (percentage === 100) return 'bg-green-500';
    if (percentage > 0) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-4 border border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Shield className="w-5 h-5 text-blue-400" />
          <span className="text-sm font-medium text-white">Empire Hazırlık Skoru</span>
        </div>
        <div className="flex items-center gap-2">
          <span className={`text-2xl font-bold ${readiness >= 80 ? 'text-green-400' : readiness >= 50 ? 'text-yellow-400' : 'text-red-400'}`}>
            %{readiness}
          </span>
          {readiness >= 80 && <CheckCircle className="w-5 h-5 text-green-400" />}
          {readiness >= 50 && readiness < 80 && <AlertCircle className="w-5 h-5 text-yellow-400" />}
          {readiness < 50 && <AlertCircle className="w-5 h-5 text-red-400" />}
        </div>
      </div>

      <Progress value={readiness} className="h-2 mb-4" />

      <div className="space-y-2">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          const percentage = (metric.value / metric.max) * 100;
          
          return (
            <div key={metric.id} className="flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <Icon className={`w-3 h-3 ${getStatusColor(metric.status)}`} />
                <span className="text-gray-400">{metric.label}</span>
                {getStatusIcon(metric.status)}
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-500">{metric.value}/{metric.max}</span>
                <div className="w-16 h-1 bg-gray-700 rounded-full overflow-hidden">
                  <div 
                    className={`h-full ${getProgressColor(metric.value, metric.max)} transition-all duration-300 ${getWidthClass(percentage)}`}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {readiness >= 80 && (
        <div className="mt-4 p-2 bg-green-500/10 border border-green-500/30 rounded-lg">
          <p className="text-xs text-green-400 text-center">
            🚀 Empire hazır! Omniverse dashboard'a geçebilirsiniz.
          </p>
        </div>
      )}
    </div>
  );
}
