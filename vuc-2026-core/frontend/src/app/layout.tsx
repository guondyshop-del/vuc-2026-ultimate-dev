/**
 * VUC-2026 Root Layout
 * Enterprise layout with providers and global styles
 */

import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'VUC-2026 Enterprise Dashboard',
  description: 'Autonomous YouTube Content Production System',
  keywords: ['youtube', 'content', 'production', 'ai', 'automation'],
  authors: [{ name: 'VUC-2026 Team' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#2563eb',
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="tr">
      <body className={inter.className}>
        <div id="root">
          {children}
        </div>
      </body>
    </html>
  )
}
