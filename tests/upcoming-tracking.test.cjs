const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const file=path.join(__dirname,'..','upcoming.js');
function setup({host='jaytreebooks.com',surface='landing',analytics=true,observer=true,visibility='visible'}={}){
  assert.ok(fs.existsSync(file),'Promo tracking must exist');
  const events=[],listeners={},observed=[],removed=[];
  const area={dataset:{upcomingSurface:surface}};
  const card={dataset:{upcomingBook:'where-mercy-stood'}};
  let onIntersect;
  const document={readyState:'complete',visibilityState:visibility,querySelectorAll:s=>s==='[data-upcoming-surface]'?[area]:s==='[data-upcoming-book]'?[card]:[],addEventListener:(n,f)=>{listeners[n]=f;}};
  const window={location:{hostname:host,pathname:surface==='landing'?'/upcoming-books.html':'/',search:''}};
  if(analytics)window.gtag=(...a)=>events.push(a);
  if(observer)window.IntersectionObserver=class{constructor(cb){onIntersect=cb;}observe(el){observed.push(el);}unobserve(el){removed.push(el);}};
  vm.runInNewContext(fs.readFileSync(file,'utf8'),{window,document,URLSearchParams,Set});
  return {events,listeners,observed,area,card,show:()=>{document.visibilityState='visible';listeners.visibilitychange?.();},intersect:(el,ratio=0.6)=>onIntersect?.([{target:el,isIntersecting:true,intersectionRatio:ratio}]),click:(action)=>{const el={dataset:{promoAction:action,book:'the-correction'},getAttribute:()=>'/chapters/book-5-first-chapter.html'};listeners.click?.({target:{closest:s=>s==='[data-promo-action]'?el:null}});}};
}
test('landing visit once; card visibility must reach threshold and never double-count',()=>{
  const x=setup();assert.equal(x.events.filter(e=>e[1]==='upcoming_promo_view').length,1);
  x.intersect(x.card,.1);assert.equal(x.events.filter(e=>e[1]==='upcoming_book_view').length,0);
  x.intersect(x.card);x.intersect(x.card);
  assert.equal(x.events.filter(e=>e[1]==='upcoming_book_view').length,1);
  assert.equal(x.events.find(e=>e[1]==='upcoming_book_view')[2].book,'where-mercy-stood');
});
test('homepage counts exposure only after section enters view',()=>{
  const x=setup({surface:'homepage'});assert.equal(x.events.length,0);
  x.intersect(x.area);x.intersect(x.area);
  assert.equal(x.events.filter(e=>e[1]==='upcoming_promo_view').length,1);
  assert.equal(x.events[0][2].placement,'homepage');
});
test('chapter click preserves campaign and reader-start funnel without claiming purchase',()=>{
  const x=setup();x.click('chapter');
  assert.equal(x.events.filter(e=>e[1]==='upcoming_chapter_click').length,1);
  assert.equal(x.events.filter(e=>e[1]==='chapter').length,1);
  assert.equal(x.events.find(e=>e[1]==='chapter')[2].book,'the-correction');
  assert.ok(x.events.every(e=>!['purchase','sign_up'].includes(e[1])));
});
test('newsletter click is intent only',()=>{
  const x=setup();x.click('notify');assert.equal(x.events.filter(e=>e[1]==='upcoming_notify_click').length,1);
  assert.ok(x.events.every(e=>!['sign_up','generate_lead'].includes(e[1])));
});
test('local preview does not pollute production analytics; missing GA never breaks navigation',()=>{
  const x=setup({host:'localhost'});x.click('notify');assert.equal(x.events.length,0);
  assert.doesNotThrow(()=>setup({analytics:false}).click('chapter'));
  assert.doesNotThrow(()=>setup({observer:false}).click('chapter'));
});
test('background landing is counted once when the reader opens its tab',()=>{
  const x=setup({visibility:'hidden'});assert.equal(x.events.length,0);
  x.show();x.show();
  assert.equal(x.events.filter(e=>e[1]==='upcoming_promo_view').length,1);
});
