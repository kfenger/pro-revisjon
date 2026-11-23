// Single source of truth for HTTP security headers and redirects.
// The build writes dist/.htaccess (Apache) and dist/_headers + dist/_redirects
// (Netlify / Cloudflare Pages) from this file, so the two can never drift apart.

export const CANONICAL_HOST = 'pro-revisjon.no';

export const csp = [
  "default-src 'none'",
  "style-src 'self'",
  "font-src 'self'",
  "img-src 'self'",
  "connect-src 'self'", // lets tools (e.g. Lighthouse) read robots.txt; the site itself runs no scripts
  "manifest-src 'self'",
  "base-uri 'none'",
  "form-action 'none'",
  "frame-ancestors 'none'",
  'upgrade-insecure-requests',
].join('; ');

export const securityHeaders = {
  'Content-Security-Policy': csp,
  'Strict-Transport-Security': 'max-age=31536000',
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=()',
  'Cross-Origin-Opener-Policy': 'same-origin',
  'Cross-Origin-Resource-Policy': 'same-origin',
};

/** Old WordPress addresses that now point to a new page. */
export const redirects = [
  ['/testside/', '/'],
];

/** Old WordPress system paths: answered with 410 Gone so bots stop probing. */
export const gonePaths = ['wp-login.php', 'xmlrpc.php', 'wp-admin', 'wp-content', 'wp-includes', 'feed', 'files'];
