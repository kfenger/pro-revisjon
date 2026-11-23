// Support for building a test copy under a sub-path (e.g. GitHub Pages: https://user.github.io/repo/).
// Production builds (no BASE_PATH) are completely unaffected.
import { readdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

export const BASE_PATH = process.env.BASE_PATH || '/';
export const IS_PREVIEW = BASE_PATH !== '/' || process.env.PREVIEW === '1';

async function* htmlFiles(dir) {
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) yield* htmlFiles(p);
    else if (e.name.endsWith('.html')) yield p;
  }
}

export default function previewBuild() {
  return {
    name: 'preview-build',
    hooks: {
      'astro:build:done': async ({ dir }) => {
        if (!IS_PREVIEW) return;
        const base = BASE_PATH.replace(/\/$/, '');
        const root = dir.pathname;
        if (base) {
          // Prefix root-relative links (Astro already prefixes its own /_astro/ assets).
          const re = new RegExp(`(href|src)="/(?!/|${base.slice(1)}/)`, 'g');
          for await (const f of htmlFiles(root)) {
            const html = await readFile(f, 'utf8');
            await writeFile(f, html.replace(re, `$1="${base}/`));
          }
        }
        // Test copies must never be indexed or compete with pro-revisjon.no in search.
        await writeFile(join(root, 'robots.txt'), 'User-agent: *\nDisallow: /\n');
        await writeFile(join(root, '.nojekyll'), '');
      },
    },
  };
}
