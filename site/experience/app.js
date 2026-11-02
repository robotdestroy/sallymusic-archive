// Modern reconstruction. The SWF files and the reference emulator are never loaded here.
const root=new URL('../',import.meta.url),assets=new URL('assets/',import.meta.url);
const stage=document.querySelector('#stage'),panel=document.querySelector('#content-panel'),art=document.querySelector('#scene-art'),bugs=document.querySelector('#bugs'),music=document.querySelector('#music');
const recordingHotspot=document.querySelector('#recording-hotspot'),recordingDialog=document.querySelector('#recording-dialog'),recording=document.querySelector('#hidden-recording');
let recordingHistoryEntry=false;
const sections=['news','audio','pictures','bio','tour','merch','links'];
// One visual playback rate shared with CSS. Native audio remains at its default 1× rate.
const MOTION_SPEED=Number(getComputedStyle(document.documentElement).getPropertyValue('--motion-speed'))||.5625;
const VISUAL_FRAME_INTERVAL=1000/(31*MOTION_SPEED);
const names={news:'news',audio:'audio',pictures:'pictures',bio:'biography',tour:'tour dates',merch:'merchandise',links:'links'};
const routes={news:'news.html',audio:'radio.html',pictures:'audio.html',bio:'biography.html',tour:'shows.html',merch:'merchandise.html',links:'links.html'};
let data,scene='news',motion=!matchMedia('(prefers-reduced-motion: reduce)').matches,track=0,last=0,arrivalTimer;
const viewport=document.querySelector('#stage-viewport');
new ResizeObserver(()=>{document.documentElement.style.setProperty('--scale',Math.min(viewport.clientWidth/1007,1));}).observe(viewport);
function fixContentLinks(){for(const a of panel.querySelectorAll('a[href]')){const href=a.getAttribute('href');if(!href.startsWith('https:')&&!href.startsWith('#'))a.href=new URL(href,root);}}
function setScene(next,transition=true){
 if(!sections.includes(next))next='news';scene=next;stage.dataset.scene=next;art.src=new URL(next+'-scene.png',assets);panel.className='content-panel '+next;panel.setAttribute('aria-label','Recovered '+names[next]);document.title='Sally — '+names[next];
 if(transition&&motion){art.classList.remove('changing');requestAnimationFrame(()=>art.classList.add('changing'));}
 document.querySelector('#player-controls').hidden=next!=='audio';bugs.hidden=next!=='news';
 recordingHotspot.hidden=next!=='news';
 if(next==='pictures'){
  panel.innerHTML='<p class="source-note">Recovered website photographs. Original album order and gallery feed are missing.</p><div class="gallery">'+data.photos.map((p,i)=>`<button data-photo="${i}" aria-label="Enlarge ${p.caption}"><img src="${new URL(p.file,assets)}" alt="${p.caption}" loading="lazy"></button>`).join('')+'</div>';
 }else if(next==='audio'){
  panel.innerHTML='<p class="source-note">Original Sally Radio files. The Flash playlist feed is missing, so this order is reconstructed.</p><div class="mobile-player"><button data-action="play">play / pause</button><button data-action="stop">stop</button><button data-action="next">next</button></div><div class="track-list">'+data.tracks.map((t,i)=>`<button data-track="${i}">${t.title}</button>`).join('')+'</div><p><a href="radio.html">plain audio player</a></p>';
 }else{panel.innerHTML=data[next];}
 panel.scrollTop=0;fixContentLinks();
 document.querySelectorAll('[data-scene]').forEach(a=>{if(a instanceof HTMLAnchorElement){if(a.dataset.scene===next)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');}});updatePlayer();
}
function choose(next){if(location.hash==='#'+next)setScene(next);else location.hash=next;}
function syncRoute(transition=true){
 if(!data)return;
 const route=location.hash.slice(1)||new URLSearchParams(location.search).get('sub')||'news';
 if(route==='mark-berlin'){
  setScene('news',transition);
  if(!recording.src)recording.src=new URL('assets/audio/markberlin.mp3',root);
  if(!recordingDialog.open)recordingDialog.showModal();
 }else{
  recordingHistoryEntry=false;
  if(recordingDialog.open)recordingDialog.close();
  setScene(route,transition);
 }
}
addEventListener('hashchange',()=>syncRoute());
recordingHotspot.addEventListener('click',()=>{recordingHistoryEntry=true;location.hash='mark-berlin';});
function closeRecording(){
 if(recordingHistoryEntry&&location.hash==='#mark-berlin')history.back();
 else{history.replaceState(null,'','#news');syncRoute(false);}
}
document.querySelector('#close-recording').addEventListener('click',closeRecording);
recordingDialog.addEventListener('cancel',e=>{e.preventDefault();closeRecording();});
recordingDialog.addEventListener('close',()=>{recording.pause();if(scene==='news')recordingHotspot.focus({preventScroll:true});});
recording.addEventListener('error',()=>document.querySelector('#recording-status').hidden=false);
document.addEventListener('click',e=>{
 const a=e.target.closest('a[data-scene]');if(a){e.preventDefault();choose(a.dataset.scene);return;}
 const b=e.target.closest('[data-photo]');if(b){const p=data.photos[Number(b.dataset.photo)];document.querySelector('#large-photo').src=new URL(p.file,assets);document.querySelector('#large-photo').alt=p.caption;document.querySelector('#photo-caption').textContent=p.caption+' · source: '+p.file;document.querySelector('#photo-dialog').showModal();return;}
 const song=e.target.closest('[data-track]');if(song){track=Number(song.dataset.track);loadTrack(true);return;}
 const control=e.target.closest('[data-action]');if(control){if(control.dataset.action==='play')togglePlay();if(control.dataset.action==='stop')stop();if(control.dataset.action==='next')nextTrack(1);}
});
document.querySelector('#close-photo').addEventListener('click',()=>document.querySelector('#photo-dialog').close());
function updatePlayer(){if(!data)return;const title=data.tracks[track].title;document.querySelector('#now-playing').textContent=music.error?'File unavailable — use the plain audio player':(music.paused?'▷ ':'♫ ')+title;stage.classList.toggle('playing',!music.paused);const globalControl=document.querySelector('#global-audio');globalControl.hidden=!music.src;globalControl.textContent=music.paused?'resume music':'pause music';document.querySelector('#player-controls .play').setAttribute('aria-label',music.paused?'Play song':'Pause song');document.querySelectorAll('[data-track]').forEach(b=>b.setAttribute('aria-current',String(Number(b.dataset.track)===track)));}
function loadTrack(play=false){music.src=new URL('assets/audio/'+data.tracks[track].file,root);updatePlayer();if(play)music.play().catch(()=>updatePlayer());}
function togglePlay(){if(!music.src)loadTrack(true);else if(music.paused)music.play().catch(()=>updatePlayer());else music.pause();}
function stop(){music.pause();if(music.readyState>0)music.currentTime=0;updatePlayer();}
function nextTrack(direction){track=(track+direction+data.tracks.length)%data.tracks.length;loadTrack(!music.paused);}
document.querySelector('#global-audio').addEventListener('click',togglePlay);document.querySelector('#player-controls .play').addEventListener('click',togglePlay);document.querySelector('#player-controls .stop').addEventListener('click',stop);document.querySelector('#player-controls .previous').addEventListener('click',()=>nextTrack(-1));document.querySelector('#player-controls .next').addEventListener('click',()=>nextTrack(1));
for(const event of ['play','pause','error'])music.addEventListener(event,updatePlayer);music.addEventListener('ended',()=>{track=(track+1)%data.tracks.length;loadTrack(true);});
const ambient=document.querySelector('#ambient-track');ambient.volume=.3;
recording.addEventListener('play',()=>{music.pause();ambient.pause();const b=document.querySelector('#ambience');b.setAttribute('aria-pressed','false');b.textContent='ambient sound off';});
document.querySelector('#ambience').addEventListener('click',async e=>{const button=e.currentTarget;if(ambient.paused){try{await ambient.play();button.setAttribute('aria-pressed','true');button.textContent='ambient sound on';}catch{button.textContent='ambient sound unavailable';}}else{ambient.pause();button.setAttribute('aria-pressed','false');button.textContent='ambient sound off';}});
function applyMotion(){stage.classList.toggle('still',!motion);const b=document.querySelector('#motion');b.setAttribute('aria-pressed',String(!motion));b.textContent=motion?'pause motion':'resume motion';if(!motion){clearTimeout(arrivalTimer);document.querySelector('#arrival').hidden=true;stage.classList.remove('arriving');panel.classList.remove('arriving');}}
document.querySelector('#motion').addEventListener('click',()=>{motion=!motion;applyMotion();});
async function arrive(){if(!motion)return;const im=document.querySelector('#arrival');stage.classList.add('arriving');panel.classList.add('arriving');im.src=new URL('arrival.webp?replay='+Date.now(),assets);try{await im.decode();}catch{stage.classList.remove('arriving');panel.classList.remove('arriving');return;}im.hidden=false;stage.classList.add('arriving');panel.classList.add('arriving');clearTimeout(arrivalTimer);arrivalTimer=setTimeout(()=>{im.hidden=true;stage.classList.remove('arriving');panel.classList.remove('arriving');},2700/MOTION_SPEED);}
document.querySelector('#replay').addEventListener('click',arrive);
// Original createBugs/reset/move parameters: six bugs, bounds 630×430, 5–14px per 31fps frame.
const flying=[];function target(b){b.tx=30+Math.random()*630;b.ty=30+Math.random()*430;b.speed=5+Math.random()*9;const distance=Math.hypot(b.tx-b.x,b.ty-b.y)||1;b.dx=(b.tx-b.x)*b.speed/distance;b.dy=(b.ty-b.y)*b.speed/distance;}
for(const [i,key] of ['audio','bio','links','tour','merch','pictures'].entries()){
 const a=document.createElement('a');a.className='bug';a.href=new URL(routes[key],root);a.dataset.scene=key;a.setAttribute('aria-label','Flying '+names[key]+' navigation');a.innerHTML='<img src="'+new URL('bug-1.png',assets)+'" alt=""><span class="label">'+names[key]+'</span>';
 const b={a,img:a.querySelector('img'),x:100+(i%3)*180,y:130+Math.floor(i/3)*170,scale:.5+Math.random()*.25,hover:false,frame:0};target(b);a.addEventListener('pointerenter',()=>b.hover=true);a.addEventListener('pointerleave',()=>b.hover=false);a.addEventListener('focus',()=>b.hover=true);a.addEventListener('blur',()=>b.hover=false);bugs.append(a);flying.push(b);
}
function animate(now){requestAnimationFrame(animate);if(now-last<VISUAL_FRAME_INTERVAL)return;last=now-((now-last)%VISUAL_FRAME_INTERVAL);for(const b of flying){if(motion&&scene==='news'&&!b.hover&&!document.hidden){if(Math.hypot(b.tx-b.x,b.ty-b.y)>b.speed){b.x+=b.dx;b.y+=b.dy;}else target(b);b.frame=(b.frame+1)%6;b.img.src=new URL('bug-'+(b.frame+1)+'.png',assets);}b.a.style.transform=`translate(${b.x-60}px,${b.y-55}px) scale(${b.hover?1:b.scale})`;}}
requestAnimationFrame(animate);applyMotion();
try{const response=await fetch(new URL('data.json',import.meta.url));if(!response.ok)throw Error('content');data=await response.json();syncRoute(false);if(!location.hash)arrive();}catch{panel.innerHTML='<p>The recovered content could not load. <a href="'+new URL('html-site.html',root)+'">Open the plain HTML archive</a>.</p>';}
