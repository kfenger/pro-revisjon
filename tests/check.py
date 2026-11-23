import json, sys
from playwright.sync_api import sync_playwright
pages = ['/wp-login.php', '/', '/tjenester/revisjon/', '/tjenester/regnskap-og-skatt/', '/tjenester/radgivning/', '/om-oss/', '/tjenester/', '/ansatte/', '/kontakt/', '/nyttige-lenker/', '/personvern/', '/finnes-ikke/']
sizes = {'desktop': (1440, 900), 'tablet': (820, 1180), 'mobile': (375, 812)}
axe = open('node_modules/axe-core/axe.min.js').read()
results = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--host-resolver-rules=MAP pro-revisjon.no 127.0.0.1','--no-proxy-server'])
    for sname, (w, h) in sizes.items():
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, ignore_https_errors=True)
        for path in pages:
            pg = ctx.new_page()
            msgs = []
            pg.on('console', lambda m: msgs.append(f'{m.type}: {m.text}'))
            pg.on('requestfailed', lambda r: msgs.append(f'FAILED {r.url}'))
            pg.goto('https://pro-revisjon.no' + path, wait_until='networkidle')
            overflow = pg.evaluate('document.documentElement.scrollWidth > window.innerWidth')
            name = (path.strip('/') or 'home').replace('/', '_')
            pg.screenshot(path=f'shots/{sname}-{name}.png', full_page=True)
            key = f'{sname} {path}'
            results[key] = {'overflow': overflow, 'console': msgs}
            if sname != 'tablet':
                # axe can't be injected as inline script under CSP, so evaluate via CDP-level evaluate
                pg.evaluate(axe)
                r = pg.evaluate("axe.run(document, {runOnly: ['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']})")
                results[key]['axe'] = [(v['id'], v['impact'], len(v['nodes'])) for v in r['violations']]
            pg.close()
        ctx.close()
    b.close()
for k, v in results.items():
    print(k, json.dumps(v, ensure_ascii=False))
