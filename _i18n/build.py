import re,html,os,sys
sys.path.insert(0,os.path.dirname(__file__))
from tr import T
src=open(os.path.join(os.path.dirname(__file__),'en-source.html')).read()
L=['en','fr','it','es']
def build(lang):
    s=src
    i=L.index(lang)-1
    s=s.replace('src="images/','src="/images/').replace('href="images/','href="/images/')
    s=s.replace('<html lang="en">',f'<html lang="{"fr-CA" if lang=="fr" else lang}">',1)
    alt=''.join(f'<link rel="alternate" hreflang="{l}" href="https://boatingdockbook.github.io/{"" if l=="en" else l+"/"}">\n' for l in L)+'<link rel="alternate" hreflang="x-default" href="https://boatingdockbook.github.io/">\n'
    s=s.replace('<link rel="icon"',alt+'<link rel="icon"',1)
    sw='<nav class="lang" aria-label="Language">'+' · '.join(f'<a href="/{"" if l=="en" else l+"/"}" lang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{l.upper()}</a>' for l in L)+'</nav>'
    old='<span class="lang" title="Also in French, Italian and Spanish">EN · FR · IT · ES</span>'
    assert old in s; s=s.replace(old,sw)
    s=s.replace('href="privacy.html"',f'href="/privacy.html#{lang}"')
    s=s.replace('.lang{','.lang a{color:inherit;text-decoration:none;padding:2px 2px}\n.lang a[aria-current]{color:#E6C483;font-weight:600}\n.lang a:hover{color:#fff}\n.lang{',1)
    if lang!='en':
        # longest first so a short string never replaces inside a longer one
        for en in sorted(T,key=len,reverse=True):
            tr=T[en][i]
            for form in {en, html.escape(en,quote=False)}:
                ef=re.escape(form)
                s=re.sub(r'(>\s*)'+ef+r'(\s*<)', lambda m: m.group(1)+html.escape(tr,quote=False)+m.group(2), s)
                s=re.sub(r'(="\s*)'+ef+r'(\s*")', lambda m: m.group(1)+html.escape(tr)+m.group(2), s)
    return s
out=sys.argv[1]
for l in L:
    p=os.path.join(out,'index.html' if l=='en' else l+'/index.html')
    os.makedirs(os.path.dirname(p) or '.',exist_ok=True)
    open(p,'w').write(build(l))
print('built')
