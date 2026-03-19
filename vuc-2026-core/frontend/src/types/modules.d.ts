declare module 'framer-motion' {
  const motion: any
  const AnimatePresence: any
  export { motion, AnimatePresence }
}

declare module '@/lib/api' {
  const apiClient: any
  const getStatusColor: any
  const formatDuration: any
  export { apiClient, getStatusColor, formatDuration }
}
