import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@ui': path.resolve(__dirname, './packages/ui/src/index.ts'),
      '@design-system': path.resolve(__dirname, './packages/design-system/src/index.ts'),
      '@api-sdk': path.resolve(__dirname, './packages/api-sdk/src/index.ts'),
      '@auth': path.resolve(__dirname, './packages/auth/src/index.ts'),
      '@maps': path.resolve(__dirname, './packages/maps/src/index.ts'),
      '@charts': path.resolve(__dirname, './packages/charts/src/index.ts'),
      '@forms': path.resolve(__dirname, './packages/forms/src/index.ts')
    }
  },
  test: {
    environment: 'jsdom',
    globals: true
  }
});
