# Tests

End-to-end checks used during development. They expect the built site (`dist/`) to be served
over HTTPS at `https://pro-revisjon.no` mapped to 127.0.0.1 (a local Apache with the generated
`.htaccess`), plus Python Playwright with Chrome and `html-validate` / `axe-core` from npm.

| File | What it checks |
| --- | --- |
| `suite.sh` | Server: redirects, security headers, 404/405/410, hidden files, caching, MIME types |
| `navtest.py` | Every navigation path on desktop and mobile, menu behaviour, slideshow pause |
| `check.py` | Accessibility (axe, WCAG 2.2 AA), console errors and horizontal overflow at 3 sizes |
| `kb.py` | Keyboard focus, text-spacing and forced-colours checks |
| `shots.py` | Full-page screenshots for visual review |
