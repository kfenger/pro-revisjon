import type { APIRoute } from 'astro';

const pages = ['/', '/tjenester/', '/tjenester/revisjon/', '/tjenester/regnskap-og-skatt/', '/tjenester/radgivning/', '/om-oss/', '/ansatte/', '/kontakt/', '/nyttige-lenker/', '/personvern/'];

export const GET: APIRoute = ({ site }) => {
  const urls = pages.map((p) => `  <url><loc>${new URL(p, site).href}</loc></url>`).join('\n');
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
