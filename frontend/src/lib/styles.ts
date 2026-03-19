/**
 * Utility functions for dynamic styling
 */

/**
 * Get Tailwind width class for percentage values
 * @param percentage - Percentage value (0-100)
 * @returns Tailwind width class string
 */
export const getWidthClass = (percentage: number): string => {
  const rounded = Math.round(percentage);
  return `w-${rounded}`;
};

/**
 * Get dynamic color class based on value
 * @param value - Current value
 * @param max - Maximum value
 * @returns Color class string
 */
export const getProgressColorClass = (value: number, max: number): string => {
  const percentage = (value / max) * 100;
  
  if (percentage < 30) return 'bg-red-500';
  if (percentage < 60) return 'bg-yellow-500';
  if (percentage < 80) return 'bg-blue-500';
  return 'bg-green-500';
};

/**
 * Get status color class
 * @param status - Status string
 * @returns Color class string
 */
export const getStatusColor = (status: string): string => {
  switch (status) {
    case 'active':
    case 'healthy':
    case 'connected':
      return 'text-green-400';
    case 'warning':
    case 'pending':
      return 'text-yellow-400';
    case 'error':
    case 'critical':
    case 'offline':
      return 'text-red-400';
    case 'idle':
      return 'text-gray-400';
    default:
      return 'text-gray-400';
  }
};

/**
 * Get status background class
 * @param status - Status string
 * @returns Background class string
 */
export const getStatusBg = (status: string): string => {
  switch (status) {
    case 'active':
    case 'healthy':
    case 'connected':
      return 'bg-green-500/20';
    case 'warning':
    case 'pending':
      return 'bg-yellow-500/20';
    case 'error':
    case 'critical':
    case 'offline':
      return 'bg-red-500/20';
    case 'idle':
      return 'bg-gray-500/20';
    default:
      return 'bg-gray-500/20';
  }
};

/**
 * Get progress color class (legacy compatibility)
 * @param value - Current value
 * @param max - Maximum value
 * @returns Color class string
 */
export const getProgressColor = (value: number, max: number): string => {
  return getProgressColorClass(value, max);
};
