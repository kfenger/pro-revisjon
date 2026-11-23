from playwright.sync_api import sync_playwright
args=['--ignore-certificate-errors','--host-resolver-rules=MAP pro-revisjon.no 127.0.0.1','--no-proxy-server']
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=args)
    ctx=b.new_context(viewport={'width':1280,'height':800},ignore_https_errors=True)
    pg=ctx.new_page(); errs=[]
    pg.on('console',lambda m: errs.append(m.text) if m.type in('error','warning') else None)
    pg.goto('https://pro-revisjon.no/')
    pg.keyboard.press('Tab')
    print('1st tab:', pg.evaluate('document.activeElement.textContent.trim()'), 'visible:', pg.evaluate('document.activeElement.getBoundingClientRect().top>=0'))
    pg.keyboard.press('Enter'); print('after skip, focus on:', pg.evaluate('document.activeElement.id'))
    # walk all focusables, check visible focus indicator
    pg.goto('https://pro-revisjon.no/personvern/'); n=0; bad=[]
    for i in range(80):
        pg.keyboard.press('Tab')
        info=pg.evaluate('''()=>{const e=document.activeElement;if(e===document.body)return null;const s=getComputedStyle(e);return [e.tagName,(e.textContent||'').trim().slice(0,30),s.outlineStyle,s.outlineWidth]}''')
        if not info: break
        n+=1
        if info[2]=='none' or info[3]=='0px': bad.append(info)
    print('focusables on personvern:',n,'without focus ring:',bad)
    pg.goto('https://pro-revisjon.no/personvern/#klage'); print('anchor scroll target top:', pg.evaluate("Math.round(document.getElementById('klage').getBoundingClientRect().top)"))
    print('console:',errs)
    # text spacing 1.4.12
    ctx2=b.new_context(viewport={'width':375,'height':800},bypass_csp=True,ignore_https_errors=True)
    for path in ['/','/ansatte/','/kontakt/','/nyttige-lenker/']:
        q=ctx2.new_page(); q.goto('https://pro-revisjon.no'+path)
        q.add_style_tag(content='*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}')
        ov=q.evaluate('''()=>[...document.querySelectorAll('body *')].filter(e=>e.scrollWidth>e.clientWidth+1 && getComputedStyle(e).overflow!=='visible').length''')
        print('text-spacing',path,'page overflow:',q.evaluate('document.documentElement.scrollWidth>innerWidth'),'clipped:',ov)
        q.screenshot(path=f'shots/spacing{path.strip("/") or "home"}.png',full_page=True)
    # forced colors
    ctx3=b.new_context(viewport={'width':1280,'height':800},forced_colors='active',ignore_https_errors=True)
    r=ctx3.new_page(); r.goto('https://pro-revisjon.no/'); r.screenshot(path='shots/forced.png')
    b.close()
