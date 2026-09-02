import type { Metadata, Viewport } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import './globals.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: { default: 'Nexus XAU Engine', template: '%s · Nexus XAU' },
  description: 'Live display for the Nexus XAU trading engine — signal dashboard, history, detail,and system status.',
	applicationName: 'Nexus XAU Engine',
	manifest: '/manifest.webmanifest',
	appleWebApp: { capable: true, statusBarStyle: 'black-translucent', title: 'Nexus XAU' },
	icons: { icon: [{ url: '/file.svg', type: 'image/svg+xml' }] },
};

export const viewport: Viewport = {
  themeColor: '#020617',
  width: 'device-width',
  initialScale: 1,
  viewportFit: 'cover',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}>
      <body className="min-h-dvh bg-slate-950 text-slate-100">{children}</body>
    </html>
  );
}