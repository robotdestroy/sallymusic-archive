from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import re,json,sys
root=Path(__file__).parent/'site';errors=[];links=0;images=0;pages=list(root.glob('*.html'))
class Page(HTMLParser):
 def __init__(self,p):super().__init__();self.p=p;self.ids=[];self.refs=[]
 def handle_starttag(self,t,attrs):
  global links,images
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if t in ['script','iframe','form','input','object','embed']:errors.append(f'{self.p.name}: active tag {t}')
  if any(k.startswith('on') for k in a):errors.append(f'{self.p.name}: inline handler')
  for k in ['href','src']:
   if k not in a:continue
   u=a[k];p=urlparse(u)
   if p.scheme:
    if p.scheme!='https' or p.hostname!='web.archive.org':errors.append(f'{self.p.name}: unexpected external destination')
    continue
   links+=1
   target=(self.p.parent/unquote(p.path)) if p.path else self.p
   if not target.is_file():errors.append(f'{self.p.name}: missing {u}')
   elif p.fragment:self.refs.append((target,p.fragment))
  if t=='img':images+=1
parsed={}
for p in pages:
 d=Page(p);d.feed(p.read_text());parsed[p]=d
 s=p.read_text()
 if re.search(r'[\w.+%-]+@[\w.-]+\.[A-Za-z]{2,}',s):errors.append(f'{p.name}: email address')
 if "connect-src 'none'" not in s:errors.append(f'{p.name}: no connection restriction')
for p,d in parsed.items():
 for target,frag in d.refs:
  if target in parsed and frag not in parsed[target].ids:errors.append(f'{p.name}: missing fragment {target.name}#{frag}')
for css in (root/'assets').glob('*.css'):
 for u in re.findall(r'url\(([^)]+)\)',css.read_text()):
  if not (css.parent/u.strip('\'"')).is_file():errors.append(f'{css.name}: missing asset {u}')
result={'pages':len(pages),'local_references':links,'image_references':images,'errors':errors}
print(json.dumps(result,indent=2));sys.exit(bool(errors))
