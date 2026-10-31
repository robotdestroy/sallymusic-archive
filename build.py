#!/usr/bin/env python3
"""Build the static archive. Requires markdown-it-py; never runs legacy server code."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlparse,parse_qs,unquote
from markdown_it import MarkdownIt
import re,json,hashlib,argparse
ROOT=Path(__file__).resolve().parent
SITE=ROOT/'site'
SOURCE=ROOT/'source-material'
parser=argparse.ArgumentParser();parser.add_argument('--content',type=Path,default=ROOT/'content');args=parser.parse_args()
CONTENT=args.content
md=MarkdownIt('commonmark',{'html':False,'breaks':True})
sections={'News.md':('news.html','all recovered news'),'Biography.md':('biography.html','biography'),'Discography.md':('discography.html','discography'),'Lyrics.md':('lyrics.html','lyrics'),'Audio and Media.md':('audio.html','audio & media'),'Merchandise.md':('merchandise.html','merchandise'),'Links and Press.md':('links.html','links & press'),'Tour Dates.md':('shows.html','gigography'),'Recovery Notes.md':('recovery.html','recovery notes')}
legacy={'news.html':'news.html','news2003.html':'news.html','biography.html':'biography.html','biography1.html':'biography.html','discography.html':'discography.html','eplyrics.html':'lyrics.html','lyrics.html':'lyrics.html','secret.html':'lyrics.html','audio.html':'audio.html','media.html':'audio.html','demos.html':'audio.html','shows.html':'shows.html','pictures.html':'audio.html','pretentious.html':'audio.html','merch.html':'merchandise.html','links.html':'links.html'}
class Node:
 def __init__(self,tag='',attrs=(),children=None):self.tag=tag;self.attrs=dict(attrs);self.children=children or []
 def find(self,**attrs):
  if all(self.attrs.get(k)==v for k,v in attrs.items()):return self
  for x in self.children:
   if isinstance(x,Node):
    r=x.find(**attrs)
    if r:return r
 def html(self):
  if self.tag=='_root':return ''.join(x.html() if isinstance(x,Node) else x for x in self.children)
  s='<'+self.tag+''.join(' '+k+'="'+escape(str(v or ''),quote=True)+'"' for k,v in self.attrs.items())+'>'
  if self.tag in ['img','br','hr','meta','link','input']:return s
  return s+''.join(x.html() if isinstance(x,Node) else x for x in self.children)+'</'+self.tag+'>'
class DOM(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=False);self.root=Node('_root');self.stack=[self.root];self.feed(s)
 def handle_starttag(self,t,a):
  n=Node(t,a);self.stack[-1].children.append(n)
  if t not in ['img','br','hr','meta','link','input']:self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,x):self.stack[-1].children.append(x)
 def handle_entityref(self,x):self.handle_data('&'+x+';')
 def handle_charref(self,x):self.handle_data('&#'+x+';')

def link(u):
 if u.startswith('#'):return u
 name=unquote(urlparse(u).path).rsplit('/',1)[-1]
 if name in sections:return sections[name][0]
 p=urlparse(u);host=p.hostname or '';q=parse_qs(p.query)
 if u.startswith('mailto:'):return 'services.html#contact'
 if host=='web.archive.org':return u
 if host in ['www.sallymusic.com','sallymusic.com','']:
  if 'itemid' in q:
   i=q['itemid'][0]
   if i=='102':return 'mars.html'
   return ('shows.html' if i in ['230','231','234'] else 'item-'+i+'.html')
  path=p.path.lower()
  if 'newsletter' in path or 'memberid' in q:return 'services.html'
  if path in ['/','/cms/','/cms/index.php','index.php','']:return 'html-site.html'
  if 'merch' in u or 'buy' in u:return 'merchandise.html'
  name=path.rsplit('/',1)[-1]
  if name in legacy:return legacy[name]
  return 'https://web.archive.org/web/20070929/'+('http://sallymusic.com/'+u.lstrip('/') if not host else u)
 # Send historical external destinations through Wayback rather than today’s unrelated domains.
 return 'https://web.archive.org/web/20070929/'+u if p.scheme in ['http','https'] else 'services.html'

def scrub(n):
 if not isinstance(n,Node):return n
 if n.tag in ['script','iframe','object','embed','form','input','button','textarea','select']:return ''
 a=n.attrs
 for k in list(a):
  if k.startswith('on') or k in ['style','action','target']:del a[k]
 if n.tag=='a' and 'href' in a:a['href']=link(a['href'])
 if n.tag=='img':
  src=a.get('src','');name=src.rsplit('/',1)[-1]
  if (SITE/'assets/images'/name).exists():a['src']='assets/images/'+name
  else:return '<span class="unavailable">[archived image unavailable]</span>'
  a.setdefault('alt','')
 n.children=[scrub(c) for c in n.children];return n

def clean(s):
 d=DOM(s);scrub(d.root)
 return d.root.html()
def img(n,alt=''):return '<img src="assets/images/'+n+'" alt="'+escape(alt)+'">'
nav='<nav class="archive-nav" aria-label="Archive sections"><h3>the archive</h3><ul><li><a href="index.html">Flash reconstruction</a></li><li><a href="html-site.html">2007 homepage</a></li><li><a href="radio.html">sally radio</a></li>'+''.join('<li><a href="'+v[0]+'">'+v[1]+'</a></li>' for v in sections.values())+'<li><a href="about.html">about this restoration</a></li></ul></nav>'
original=DOM((SOURCE/'home.html').read_text())
header=clean(original.root.find(id='header').html())
# Preserve the original controls visually; replace their obsolete popup destinations.
header=header.replace('href="#"','href="services.html"',2).replace('href="#"','href="radio.html"',1)
sidebar=clean(original.root.find(id='sidebarcontainer').html())
sidebar=sidebar.replace('</div>',nav+'</div>',1)
footer='<div class="clearing"></div><div id="footer">'+img('footer_txt.gif','sallymusic.com')+'</div>'
notice='<p class="archive-notice">SallyMusic.com · historical static archive · <a href="about.html">about / sources</a>. Old services are inactive.</p>'
def page(name,title,body,home=False):
 content=body if home else '<div id="container" class="reading"><div class="content"><div class="contenttitle"><h2>'+escape(title)+'</h2></div><div class="contentbody">'+body+'</div></div></div>'
 html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="A faithful static restoration of SallyMusic.com, the Chicago band’s archived website."><meta name="referrer" content="no-referrer"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'none'; connect-src 'none'; form-action 'none'; object-src 'none'; base-uri 'none'"><title>'''+escape(title)+' · SallyMusic.com archive</title><link rel="stylesheet" href="assets/sallymusic.css"><link rel="stylesheet" href="assets/archive.css"></head><body><div id="mainwrapper"><div id="wrapper">'+header+'<nav class="mobile-menu" aria-label="Quick archive navigation"><a href="html-site.html">home</a><a href="news.html">news archive</a><a href="shows.html">shows</a><a href="audio.html">audio</a><a href="about.html">about</a></nav>'+content+sidebar+footer+notice+'</div></div></body></html>'
 (SITE/name).write_text(html)

# This is the actual captured homepage body, not re-created modern cards.
page('html-site.html','sally — the band, from chicago, illinois',clean(original.root.find(id='container').html()),True)
# Broader reading sections carry their recovery metadata and explicit revision history.
news=(CONTENT/'News.md').read_text()
for source,(dest,title) in sections.items():
 text=(CONTENT/source).read_text()
 text=re.sub(r' · raw: `[^`]+`','',text)
 text=re.sub(r'\[([^\]]+)\]\(mailto:[^)]+\)',r'\1 [historical email omitted]',text)
 text=re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b','[historical email omitted]',text)
 html=clean(md.render(text))
 # Add anchors deterministically to make long recovered pages navigable.
 count=0
 def heading(m):
  global count
  count+=1;return '<h2 id="section-'+str(count)+'">'+m[1]+'</h2>'
 html=re.sub(r'<h2>(.*?)</h2>',heading,html,flags=re.S)
 html='<p class="section-note">Recovered reading room. This section combines surviving versions; the 2007 homepage retains its original layout. <a href="html-site.html">return home</a></p>'+html
 page(dest,title,html)
# A safe browser-native replacement for the original Flash music player.
tracks=[('goldielocks.mp3','goldie locks'),('watermelon.mp3','watermelon'),('clarks_on_lincoln.mp3','clarks on lincoln'),('abundantsunshine.mp3','abundant sunshine'),('thank_god_for_sunglasses.mp3','thank god for sunglasses'),('sunglasses128.mp3','sunglasses128 — alternate file'),('the_ungrateful_interlude.mp3','the ungrateful interlude'),('important.mp3','important'),('teach_me.mp3','teach me'),('guac.mp3','guac')]
radio='<p class="section-note">Ten original files recovered from the Sally Radio directory. Standard browser audio replaces the old Flash player. Labels follow the filenames; the alternate sunglasses file is retained. Nothing autoplays.</p>'
for file,title in tracks:
 radio+='<section class="track"><h3>'+escape(title)+'</h3><audio controls preload="none" aria-label="'+escape(title)+'"><source src="assets/audio/'+file+'" type="audio/mpeg">Your browser cannot play this file. <a href="assets/audio/'+file+'">download MP3</a></audio></section>'
page('radio.html','sally radio',radio+'<p><a href="audio.html">historical audio & media descriptions</a></p>')
# Each CMS title on the homepage opens its recovered entry, retaining date uncertainty.
items={}
for block in re.split(r'(?m)^### ',news)[1:]:
 m=re.search(r'CMS item (\d+)\.',block)
 if m:items.setdefault(m[1],[]).append(block)
for item,blocks in items.items():
 html=''.join(clean(md.render('### '+b)) for b in blocks)
 page('item-'+item+'.html','news entry '+item,html+'<p><a href="news.html">all recovered news</a></p>')
# Preserved whimsical show placeholder is identified separately from the real gigography.
page('mars.html','09/09/09 : mars','<p>it\'ll be lunacy.<br>the outer realms of the universe<br>30022 quasar street, moonsville, WY 99999<br>start time eight post meridian.</p><p class="section-note">Original playful placeholder; not a real performance. In a later capture its date changed to 12/21/12.</p>')
page('services.html','old services','<p>This is a static historical archive. The original newsletter, contact popups, login, comments, shopping forms, and Flash player are inactive.</p><h3 id="contact">contact / newsletter</h3><p>No messages or signups can be sent from this restoration.</p><p><a href="audio.html">browse the recovered audio & media descriptions</a></p>')
page('about.html','about this restoration','''<p>This separate archive brings back SallyMusic.com’s paper collage news layout, its original backgrounds, typography, artwork and animated crow. It is a historical experience assembled in October 2026.</p><p>The visual reference is the late-2007 Nucleus CMS site. The homepage body and stylesheet were recovered from Wayback; original matching artwork came from the saved website files. The broader reading sections combine older surviving pages and revisions and were not originally all displayed in this CMS skin. The small archive menu, mobile adjustments and this notice are restoration additions.</p><p><a href="https://web.archive.org/web/20070828100657/http://www.sallymusic.com:80/cms/">archived homepage</a> · <a href="https://web.archive.org/web/20070929161501/http://sallymusic.com/cms/?itemid=102">archived show page</a></p><p>News: approximately 74 recovered posts, including two text revisions. Gigography: 70 real entries, 2003–2007. Missing database rows, Flash interiors and unavailable media have not been invented. Capture dates are not publication dates. The CMS didn’t print years.</p><p>Forms, shopping and comments are inactive. Ten original Sally Radio MP3s play through standard browser audio; the old Flash interface is replaced. Historical outbound links open Wayback, not the current owners of old domains. Email addresses are omitted from the public copy. No original server configuration or private archive files are included.</p><p>Artwork and historical writing remain the property of their original owners. This restoration does not assign them a new open-source license.</p><p><a href="recovery.html">full recovery notes</a></p>''')
(SITE/'assets/sallymusic.css').write_text((SOURCE/'sallymusic.css').read_text())
(SITE/'.nojekyll').touch()
print(json.dumps({'pages':len(list(SITE.glob('*.html'))),'cms_entries':len(items),'assets':len(list((SITE/'assets/images').glob('*')))}))
