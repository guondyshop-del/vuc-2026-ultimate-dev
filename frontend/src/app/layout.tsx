import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navigation from '@/components/Navigation';
import { Toaster } from 'react-hot-toast';
import AIStatusPanel from '@/components/AIStatusPanel';

const inter = Inter({ 
  subsets: ['latin', 'latin-ext'],
  display: 'swap',
  fallback: ['system-ui', 'sans-serif']
})

export const metadata: Metadata = {
  title: 'ONX - Neural Empire Manager',
  description: 'Otonom YouTube İmparatorluğu Yönetim Sistemi',
  keywords: ['youtube', 'automation', 'ai', 'video production', 'content management'],
  authors: [{ name: 'ONX Team' }],
  openGraph: {
    title: 'ONX - Neural Empire Manager',
    description: 'Otonom YouTube İmparatorluğu Yönetim Sistemi',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'ONX - Neural Empire Manager',
    description: 'Otonom YouTube İmparatorluğu Yönetim Sistemi',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="tr">
      <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJYs7IxrPPSx4woyNZ/0PirhA6xmjyJx2v7b5dZJdZ0g==" crossOrigin="anonymous" referrerPolicy="no-referrer" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className={`${inter.className} bg-gray-900 text-white`}>
        <main className="min-h-screen bg-gray-950">
          <Navigation />
          {children}
          <AIStatusPanel />
        </main>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#1f2937',
              color: '#f9fafb',
              border: '1px solid #374151',
            },
            success: {
              iconTheme: {
                primary: '#10b981',
                secondary: '#065f46',
              },
            },
            error: {
              iconTheme: {
                primary: '#ef4444',
                secondary: '#991b1b',
              },
            },
          }}
        />
      </body>
    </html>
  );
}
