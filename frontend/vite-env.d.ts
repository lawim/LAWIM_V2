/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_LAWIM_USE_MOCKS?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

declare module '*.css';