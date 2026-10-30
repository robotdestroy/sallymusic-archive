from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import re,urllib.request,json,time
root=Path(__file__).parent
base='http://www.sallymusic.com/cms/skins/sally/'
css=(root/'source-material/sallymusic.css').read_text()
home=(root/'source-material/home.html').read_text()
paths=set(re.findall(r'url\(([^)]+)\)',css))
paths.update(u.replace(base,'') for u in re.findall(r'<img[^>]+src="([^"]+)"',home))
paths.update(['images/go_home.gif','images/dates_header.gif','images/our_garbage.gif','images/garbage.gif'])
def fetch(path):
 out=root/'site/assets'/path
 out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists(): return {'path':path,'status':'existing'}
 url='https://web.archive.org/web/20070929161501id_/'+base+path
 try:
  with urllib.request.urlopen(url,timeout=45) as r:
   b=r.read(); final=r.url; mime=r.headers.get('Content-Type','')
  if not mime.startswith('image/'): raise ValueError(mime)
  out.write_bytes(b)
  return {'path':path,'url':final,'bytes':len(b),'status':'ok'}
 except Exception as e: return {'path':path,'status':str(e)}
with ThreadPoolExecutor(max_workers=6) as pool:
 results=list(pool.map(fetch,sorted(paths)))
(root/'source-material/assets.json').write_text(json.dumps(results,indent=2))
for x in results: print(x['path'],x['status'])
