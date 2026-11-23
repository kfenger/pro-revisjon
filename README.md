# pro-revisjon.no

The Pro-Revisjon AS website. It is built with [Astro](https://astro.build) and outputs plain static HTML and CSS,
with **no JavaScript, database, cookies, analytics or admin login**.

## Requirements
- Node.js 22.12 or newer

## Commands
| Command           | What it does                                |
| ----------------- | ------------------------------------------- |
| `npm install`     | Install dependencies (Astro + two font packages) |
| `npm run dev`     | Local preview at http://localhost:4321      |
| `npm run build`   | Build the finished site into `dist/`        |
| `npm run preview` | Serve the built `dist/` locally             |

## Editing content
- **Company details, staff, phone numbers and useful links:** `src/data/site.ts`. Changes here appear on every page.
- **Page text:** `src/pages/*.astro`
- **Colours, fonts and spacing:** the variables at the top of `src/styles/global.css`
- **Logo:** save the original logo as `src/assets/images/logo.png` (or .svg/.webp). It replaces the text wordmark in the header automatically.
- **Staff photos:** save them as `src/assets/images/ansatte/oystein.jpg`, `bernt.jpg` and `morten.jpg` (the names match
  `photo:` in `src/data/site.ts`). They are converted to AVIF/WebP at the right sizes during the build. Until a file exists,
  the person's initials are shown. Portrait orientation (about 4:5) and at least 480 px wide gives the sharpest result.
- **Pages:** `/` (home), `/tjenester/` with `/tjenester/revisjon/`, `/tjenester/regnskap-og-skatt/` and `/tjenester/radgivning/`,
  `/om-oss/`, `/ansatte/`, `/kontakt/`, `/nyttige-lenker/` and `/personvern/`. Shared parts live in `src/components/`.
- **Privacy policy:** `src/pages/personvern.astro`. Update the `updated` date whenever the text changes.

## Security headers and redirects
Edit **`config/server.mjs`** only. The build generates `dist/.htaccess`, `dist/_headers` and `dist/_redirects`
from it, so Apache and Netlify/Cloudflare always get identical headers.

## Test copy on GitHub Pages
Every push to `main` builds the site and publishes a test copy via `.github/workflows/pages.yml`
(repository → Settings → Pages → Source: **GitHub Actions**). The test copy lives under a sub-path
(`https://<user>.github.io/<repo>/`), is marked `noindex`, and its `robots.txt` blocks all crawlers.
GitHub Pages ignores `.htaccess`/`_headers`, so the security headers only apply on the real host.

To build such a copy locally: `BASE_PATH=/repo-name/ npm run build`.

## Deploying
Run `npm run build` and upload the **contents** of `dist/` to the web root.

- **Apache web hotel** (for example Domeneshop, one.com or Webhuset): `dist/.htaccess` forces HTTPS and the bare domain,
  redirects old WordPress URLs and sets security headers. It requires `mod_rewrite` and `mod_headers`.
- **Netlify / Cloudflare Pages:** `dist/_headers` and `dist/_redirects` are used automatically.
  Build command: `npm run build`; output directory: `dist`.

Make sure the hidden files (`.htaccess` and `.well-known/`) are uploaded too. Many FTP clients hide them by default.

### After going live
1. Check the headers at https://securityheaders.com, aiming for grade A+.
2. Submit `https://pro-revisjon.no/sitemap.xml` in Google Search Console. The old site told Google not to index it,
   so this speeds up getting listed.
3. Once HTTPS is confirmed working everywhere, you can raise HSTS to
   `max-age=63072000; includeSubDomains; preload`. Only do this if every subdomain also runs HTTPS.
4. Shut down the old WordPress installation so it is no longer reachable.

## Security notes
- Content-Security-Policy is `default-src 'none'` and allows only same-origin CSS, fonts and images. No inline styles
  or scripts are used. Keep it that way when editing; use classes in `global.css` instead of `style="…"`.
- Fonts are self-hosted, so there are no requests to Google Fonts or other third parties.
- `.well-known/security.txt` expires 2027-11-22. Renew the date yearly.
- Run `npm audit` and `npm update` a few times a year. Install with `npm ci`, which uses the exact versions in `package-lock.json`.
- `.npmrc` sets `ignore-scripts=true`, so a compromised package can't run code during install. The site doesn't need any install scripts.
- Astro collects anonymous build telemetry. Turn it off once per machine with `npx astro telemetry disable`.
- Content is escaped automatically. Never use `set:html` with text that comes from outside the project.
- `.htaccess` answers only GET and HEAD, hides dot-files and returns **410 Gone** for old WordPress paths
  (`wp-login.php`, `xmlrpc.php`, `wp-admin` …) so bots stop probing.

### Ask the web host (server-level, outside this project)
- Hide the server version: `ServerTokens Prod` and `ServerSignature Off`.
- A valid TLS certificate for **both** `pro-revisjon.no` and `www.pro-revisjon.no` (needed for the www → apex redirect).
- TLS 1.2+ only. Check at https://www.ssllabs.com/ssltest/ and aim for grade A.
- `.htaccess` only needs `AllowOverride FileInfo`, so it also works on locked-down hosts (tested).
