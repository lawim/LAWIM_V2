import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import path from 'path';
import os from 'os';

const sharedCacheDir = process.env.LAWIM_VITE_CACHE_DIR ?? path.join(os.tmpdir(), 'lawim-v2-vite-cache');

export default defineConfig({
  cacheDir: sharedCacheDir,
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg', 'robots.txt', 'logo.svg'],
      manifest: {
        name: 'LAWIM',
        short_name: 'LAWIM',
        description: 'LAWIM · L’immobilier autrement.',
        theme_color: '#0a0a0a',
        background_color: '#0a0a0a',
        lang: 'fr',
        display: 'standalone',
        start_url: '/',
        icons: [
          {
            src: 'logo.svg',
            sizes: '192x192',
            type: 'image/svg+xml'
          },
          {
            src: 'logo.svg',
            sizes: '512x512',
            type: 'image/svg+xml'
          }
        ]
      },
      workbox: {
        runtimeCaching: [
          {
            urlPattern: /\.(?:png|jpg|jpeg|svg|webp)$/,
            handler: 'CacheFirst',
            options: {
              cacheName: 'images-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24 * 30
              }
            }
          },
          {
            urlPattern: /^https?:.*\/_api\//,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              networkTimeoutSeconds: 10
            }
          }
        ]
      },
      devOptions: {
        enabled: true
      }
    })
  ],
  resolve: {
    alias: {
      '@ui': path.resolve(__dirname, './packages/ui/src/index.ts'),
      '@design-system': path.resolve(__dirname, './packages/design-system/src/index.ts'),
      '@api-sdk': path.resolve(__dirname, './packages/api-sdk/src/index.ts'),
      '@auth': path.resolve(__dirname, './packages/auth/src/index.ts'),
      '@maps': path.resolve(__dirname, './packages/maps/src/index.ts'),
      '@charts': path.resolve(__dirname, './packages/charts/src/index.ts'),
      '@forms': path.resolve(__dirname, './packages/forms/src/index.ts'),
      '@brain': path.resolve(__dirname, './packages/brain/src/index.ts'),
      '@conversation': path.resolve(__dirname, './packages/conversation/src/index.ts'),
      '@memory': path.resolve(__dirname, './packages/memory/src/index.ts'),
      '@digital-twin': path.resolve(__dirname, './packages/digital-twin/src/index.ts'),
      '@learning': path.resolve(__dirname, './packages/learning/src/index.ts'),
      '@agents': path.resolve(__dirname, './packages/agents/src/index.ts'),
      '@knowledge': path.resolve(__dirname, './packages/knowledge/src/index.ts'),
      '@workflows': path.resolve(__dirname, './packages/workflows/src/index.ts')
    }
  },
  test: {
    cache: {
      dir: path.join(sharedCacheDir, 'vitest')
    }
  },
    build: {
    target: 'es2020',
    sourcemap: false,
    cssCodeSplit: true,
    chunkSizeWarningLimit: 800,
    rollupOptions: {
      input: {
        web: path.resolve(__dirname, 'index.html'),
        admin: path.resolve(__dirname, 'apps/admin/index.html')
      },
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('zustand') || id.includes('use-sync-external-store')) return 'vendor-react';
            if (id.includes('react-router')) return 'vendor-router';
            if (id.includes('react') || id.includes('react-dom')) return 'vendor-react';
            if (id.includes('@tanstack')) return 'vendor-query';
            if (id.includes('workbox') || id.includes('vite-plugin-pwa')) return 'vendor-pwa';
            return 'vendor';
          }
          if (id.includes('/packages/ui/')) return 'ui';
          if (id.includes('/packages/api-sdk/')) return 'api-sdk';
          if (id.includes('/packages/auth/')) return 'auth';
          if (id.includes('/packages/brain/')) return 'brain';
          if (id.includes('/packages/conversation/')) return 'conversation';
          if (id.includes('/packages/workflows/')) return 'workflows';
        }
      }
    }
  },
  server: {
    port: 4173
  }
});
