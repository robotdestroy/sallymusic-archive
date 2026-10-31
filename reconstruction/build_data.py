"""Prepare recovered content for the HTML reconstruction; no external requests."""
from pathlib import Path
from markdown_it import MarkdownIt
from urllib.parse import urlparse,unquote
import re,json
ROOT=Path(__file__).resolve().parents[1]
md=MarkdownIt('commonmark',{'html':False,'breaks':True})
mapping={'Biography.md':'biography.html','News.md':'news.html','Recovery Notes.md':'recovery.html','Tour Dates.md':'shows.html','audio.html':'audio.html','media.html':'audio.html','biography.html':'biography.html','biography1.html':'biography.html','discography.html':'discography.html','eplyrics.html':'lyrics.html','lyrics.html':'lyrics.html','secret.html':'lyrics.html','shows.html':'shows.html','news.html':'news.html','merch.html':'merchandise.html','pictures.html':'audio.html','links.html':'links.html'}
def safe_url(u):
 p=urlparse(u);name=unquote(p.path).rsplit('/',1)[-1]
 if p.hostname=='web.archive.org':return u
 if not p.hostname or p.hostname in ['sallymusic.com','www.sallymusic.com']:
  if name in mapping:return mapping[name]
  if p.path in ['','/','/cms/']:return 'html-site.html'
 if p.scheme in ['http','https']:return 'https://web.archive.org/web/20070929/'+u
 return 'services.html'
def link(tokens,idx,options,env):
 t=tokens[idx];t.attrSet('href',safe_url(t.attrGet('href') or ''));return md.renderer.renderToken(tokens,idx,options,env)
md.renderer.rules['link_open']=link
render=lambda x:md.render(x)
content=lambda n:(ROOT/'content'/n).read_text()
news=[]
for block in re.split(r'(?m)^### ',content('News.md'))[1:]:
 m=re.search(r'CMS item (\d+)\.',block)
 if m:news.append((int(m[1]),block))
news_html='<p class="source-note">Recovered news · <a href="news.html">all posts & sources</a></p>'
for item,block in sorted(news,key=lambda x:x[0],reverse=True):
 body=re.sub(r'(?m)^\*Original date label:.*\*\s*','',block)
 body=re.sub(r'(?m)^\*\*Archive evidence:\*\*.*','',body)
 news_html+='<section>'+render('### '+body)+'<p class="source-link"><a href="item-'+str(item)+'.html">entry & source</a></p></section>'
bio=content('Biography.md').split('## Version 3 —')[1].split('## Version 4 —')[0];bio=bio.split('\n',1)[1]
bio_html='<p class="source-note">The Flash biography feed is missing. This is the earlier biography preserved in the August 2004 HTML page.</p>'+render(bio)+'<p><a href="biography.html">All recovered biographies and revisions</a></p>'
shows=content('Tour Dates.md');tour_html=render(shows)+'<p><a href="shows.html">Open the full gigography</a></p>'
merch=content('Merchandise.md').split('merch booth',1)[1]
merch_html='<p class="source-note">Historical merchandise. Purchases are inactive. The Flash shop feed is missing; these descriptions survive in the older HTML page.</p>'+render(merch)+'<p><a href="discography.html">Discography</a> · <a href="merchandise.html">source</a></p>'
links=content('Links and Press.md').split('## Version 1 —')[1].split('## Version 2 —')[0];links=links.split('\n',1)[1]
links_html='<p class="source-note">Earlier recovered links; the Flash feed is missing. Historical destinations open Wayback.</p>'+render(links)+'<p><a href="links.html">All links and press versions</a></p>'
photos=[('20050722-sallymouth600-1.jpg','Sally — recovered group photograph'),('20050722-sallytable.jpg','Sally at a table'),('20050722-liveblackwhite.jpg','Sally performing'),('20050722-sallytreehouse.jpg','Sally — group photograph at a wooden window'),('20050719-sallylean600.jpg','Sally — recovered promotional photograph'),('20050719-acoustic.jpg','Acoustic performance')]
tracks=[('goldielocks.mp3','goldie locks'),('watermelon.mp3','watermelon'),('clarks_on_lincoln.mp3','clarks on lincoln'),('abundantsunshine.mp3','abundant sunshine'),('thank_god_for_sunglasses.mp3','thank god for sunglasses'),('sunglasses128.mp3','thank god for sunglasses — alternate file'),('the_ungrateful_interlude.mp3','the ungrateful interlude'),('important.mp3','important'),('teach_me.mp3','teach me'),('guac.mp3','guac')]
data={'news':news_html,'bio':bio_html,'tour':tour_html,'merch':merch_html,'links':links_html,'photos':[{'file':a,'caption':b} for a,b in photos],'tracks':[{'file':a,'title':b} for a,b in tracks]}
s=json.dumps(data,ensure_ascii=False)
assert not re.search(r'[\w.+%-]+@[\w.-]+\.[A-Za-z]{2,}',s)
(ROOT/'site/experience/data.json').write_text(s)
print('Prepared content for seven sections, six reviewed photos and ten existing MP3s')
