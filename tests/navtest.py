from playwright.sync_api import sync_playwright
BASE='https://pro-revisjon.no'
args=['--host-resolver-rules=MAP pro-revisjon.no 127.0.0.1','--no-proxy-server']
fails=[]; n=0
def ok(cond,msg):
    global n; n+=1
    if not cond: fails.append(msg)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=args)
    # ---- desktop: header nav
    pg=b.new_page(viewport={'width':1280,'height':800},ignore_https_errors=True)
    expected={'Tjenester':'/tjenester/','Om oss':'/om-oss/','Ansatte':'/ansatte/','Kontakt':'/kontakt/'}
    for label,path in expected.items():
        pg.goto(BASE+'/'); pg.click(f'.site-header .header-inner > :is(.nav-desktop, .header-contact) >> text="{label}"'); pg.wait_for_load_state()
        ok(pg.url==BASE+path, f'desktop nav {label} -> {pg.url}')
        cur=pg.eval_on_selector('.header-inner > :is(.nav-desktop,.header-contact) a[aria-current="page"]','e=>e.textContent.trim()') if pg.query_selector('.header-inner > :is(.nav-desktop,.header-contact) a[aria-current="page"]') else None
        ok(cur==label, f'desktop aria-current on {path} = {cur}')
    pg.goto(BASE+'/'); pg.click('.header-phone'.replace('.header-phone','.hero-actions .btn')); ok(pg.url==BASE+'/kontakt/', 'hero CTA -> kontakt')
    # logo goes home
    pg.goto(BASE+'/kontakt/'); pg.click('.brand'); ok(pg.url==BASE+'/', 'logo -> home')
    # section highlight on subpage
    pg.goto(BASE+'/tjenester/revisjon/')
    ok(pg.eval_on_selector('.nav-desktop a[href="/tjenester/"]','e=>e.classList.contains("is-active")'), 'Tjenester active on subpage')
    # breadcrumbs
    for path,crumbs in {'/tjenester/revisjon/':['Hjem','Tjenester','Revisjon'],'/nyttige-lenker/':['Hjem','Nyttige lenker'],'/personvern/':['Hjem','Personvernerklæring']}.items():
        pg.goto(BASE+path); got=pg.eval_on_selector_all('.breadcrumbs li','e=>e.map(x=>x.textContent.trim())'); ok(got==crumbs, f'crumbs {path}: {got}')
        for a in pg.eval_on_selector_all('.breadcrumbs a','e=>e.map(x=>x.getAttribute("href"))'):
            r=pg.goto(BASE+a); ok(r.status==200, f'crumb link {a} {r.status}'); pg.goto(BASE+path)
    # service cards on home + rows + aside links + footer + topbar
    pg.goto(BASE+'/')
    hrefs=pg.eval_on_selector_all('.index-list a','e=>e.map(x=>x.getAttribute("href"))'); ok(len(hrefs)==3,'3 services on home')
    for href in hrefs:
        pg.goto(BASE+'/'); pg.click(f'.index-list a[href="{href}"]'); ok(pg.url==BASE+href, f'home service {href}')
        ok(pg.query_selector('h1') is not None, f'h1 on {href}')
    for href in ['/tjenester/revisjon/','/tjenester/regnskap-og-skatt/','/tjenester/radgivning/']:
        pg.goto(BASE+'/tjenester/'); pg.click(f'main .index-list a[href="{href}"]'); ok(pg.url==BASE+href, f'overview entry {href}')
        others=pg.eval_on_selector_all('.next-links a','e=>e.map(x=>x.getAttribute("href"))'); ok(len(others)==2 and href not in others, f'next-links on {href}: {others}')
        for o in others:
            r=pg.goto(BASE+o); ok(r.status==200, f'next link {o}'); pg.goto(BASE+href)
    pg.goto(BASE+'/'); pg.click('text="Om Pro-Revisjon"'); ok(pg.url==BASE+'/om-oss/','home -> om oss')
    pg.click('text="Møt de ansatte"'); ok(pg.url==BASE+'/ansatte/','om oss -> ansatte')
    for path in ['/','/tjenester/','/om-oss/','/ansatte/','/nyttige-lenker/','/personvern/']:
        pg.goto(BASE+path); ok(pg.query_selector('.footer-cta') is not None, f'footer contact on {path}')
    pg.goto(BASE+'/kontakt/'); ok(pg.query_selector('.footer-cta') is None, 'no duplicate footer contact on kontakt')
    pg.goto(BASE+'/')
    for href in pg.eval_on_selector_all('.site-footer a[href^="/"]','e=>[...new Set(e.map(x=>x.getAttribute("href")))]'):
        r=pg.goto(BASE+href); ok(r.status==200, f'footer {href} {r.status}')
    pg.goto(BASE+'/')
    tel=pg.eval_on_selector_all('a[href^="tel:"]','e=>[...new Set(e.map(x=>x.getAttribute("href")))]'); ok(tel==['tel:+4738144444'], f'tel links {tel}')
    # TOC anchors keep heading below sticky header
    pg.goto(BASE+'/personvern/'); pg.click('.toc a[href="#klage"]'); pg.wait_for_timeout(200)
    top=pg.evaluate("document.getElementById('klage').getBoundingClientRect().top"); hh=pg.evaluate("document.querySelector('.site-header').getBoundingClientRect().height")
    ok(top>=hh, f'anchor hidden under sticky header: top={top} header={hh}')
    # slideshow has no pause control; header bar has no phone number on desktop
    pg.goto(BASE+'/'); ok(pg.query_selector('.slideshow-control, #slideshow-pause') is None, 'no slideshow pause control')
    ok(pg.query_selector('.header-inner a[href^="tel:"]:not(.nav-mobile a)') is None, 'no phone number in desktop header')
    ok(pg.evaluate("Math.round(document.querySelector('.brand').getBoundingClientRect().left)")==pg.evaluate("Math.round(document.querySelector('.hero-copy').getBoundingClientRect().left)"), 'logo aligned with page content')
    # ---- mobile: menu
    m=b.new_page(viewport={'width':375,'height':740},ignore_https_errors=True)
    for label,path in {'Hjem':'/', **expected}.items():
        m.goto(BASE+'/ansatte/' if path=='/' else BASE+'/')
        ok(not m.is_visible('.nav-mobile nav'), 'mobile menu closed by default')
        ok(not m.is_visible('.nav-desktop'), 'desktop nav hidden on mobile')
        m.click('.nav-mobile summary'); ok(m.is_visible('.nav-mobile nav'), 'menu opens')
        m.click(f'.nav-mobile nav >> text="{label}"'); m.wait_for_load_state()
        ok(m.url==BASE+path, f'mobile nav {label} -> {m.url}')
        ok(not m.is_visible('.nav-mobile nav'), f'menu closed after navigating to {path}')
    # tap outside the open menu closes it; taps inside the panel do not
    m.goto(BASE+'/tjenester/'); m.click('.nav-mobile summary')
    vh=m.viewport_size['height']; m.mouse.click(200, vh-20); ok(not m.is_visible('.nav-mobile nav'), 'menu closes on tap outside')
    m.click('.nav-mobile summary'); m.click('.nav-mobile-contact', position={'x':300,'y':5}); ok(m.is_visible('.nav-mobile nav'), 'menu stays open on tap inside panel')
    # keyboard: open menu with Enter
    m.goto(BASE+'/'); m.focus('.nav-mobile summary'); m.keyboard.press('Enter'); ok(m.is_visible('.nav-mobile nav'),'menu opens with keyboard')
    m.keyboard.press('Tab'); ok(m.evaluate('document.activeElement.textContent.trim()')=='Hjem','tab moves into menu')
    b.close()
print(f'{n} checks, {len(fails)} failures'); [print(' FAIL',f) for f in fails]
