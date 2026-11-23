// @ts-check
import { defineConfig } from 'astro/config';
import serverFiles from './config/server-files.mjs';
import previewBuild, { BASE_PATH } from './config/preview-build.mjs';

export default defineConfig({
  site: 'https://pro-revisjon.no',
  base: BASE_PATH,
  trailingSlash: 'always',
  build: {
    format: 'directory',
    // Keep all CSS in external files so the Content-Security-Policy
    // can stay strict (no 'unsafe-inline').
    inlineStylesheets: 'never',
  },
  devToolbar: { enabled: false },
  integrations: [serverFiles(), previewBuild()],
});
