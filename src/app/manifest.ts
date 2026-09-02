import type { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Nexus XAU Engine',
    short_name: 'Nexus XAU',
    description: 'Live display for the Nexus XAU trading engine.',
    start_url: '/',
    display: 'standalone',
    orientation: 'portrait',
    background_color: '#020617',
    theme_color: '#020617',
    icons: [
      { src: '/file.svg', type: 'image/svg+xml', purpose: 'any', sizes: 'any' },
      { src: '/globe.svg', type: 'image/svg+xml', purpose: 'any', sizes: 'any' },
    ],
  };
}