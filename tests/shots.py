import sys
from playwright.sync_api import sync_playwright
pages=sys.argv[2].split(',') ; w=int(sys.argv[1]); tag=sys.argv[3] if len(sys.argv)>3 else ''
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--host-resolver-rules=MAP pro-revisjon.no 127.0.0.1','--no-proxy-server'])
    c=b.new_context(viewport={'width':w,'height':900},ignore_https_errors=True,device_scale_factor=1)
    for path in pages:
        pg=c.new_page(); pg.goto('https://pro-revisjon.no'+path, wait_until='networkidle')
        # scroll-load: trigger lazy images and scroll-driven reveals, then return to top
        H=pg.evaluate('document.documentElement.scrollHeight')
        for y in range(0,H,400): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(80)
        pg.wait_for_load_state('networkidle'); pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(1800)
        n=(path.strip('/') or 'home').replace('/','_')
        pg.screenshot(path=f'shots/v2-{w}-{n}{tag}.png', full_page=True); pg.close()
    b.close()
