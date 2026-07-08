import type { Config } from 'tailwindcss';

export default {
  content: [
    './apps/**/*.{ts,tsx}',
    './packages/**/*.{ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#fff8eb',
          100: '#f8e8c6',
          200: '#efd59b',
          300: '#e4c375',
          400: '#dab455',
          500: '#d8b46a',
          600: '#b99145',
          700: '#8f6f33',
          800: '#624a21',
          900: '#3b2c15'
        }
      },
      boxShadow: {
        soft: '0 10px 30px rgba(15, 23, 42, 0.08)'
      }
    }
  },
  plugins: []
} satisfies Config;
