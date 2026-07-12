/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_LAWIM_USE_MOCKS?: string;
  readonly VITE_CAMPAY_WIDGET_ENABLED?: string;
  readonly VITE_CAMPAY_WIDGET_SCRIPT_URL?: string;
  readonly VITE_CAMPAY_WIDGET_APP_ID?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

declare module '*.css';
