/** Current page path without the deployment base (e.g. GitHub Pages sub-path), always ending in '/'. */
export function pagePath(url: URL): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const p = base && url.pathname.startsWith(base) ? url.pathname.slice(base.length) : url.pathname;
  return p || '/';
}
export const isPreview = import.meta.env.BASE_URL !== '/' || process.env.PREVIEW === '1';
