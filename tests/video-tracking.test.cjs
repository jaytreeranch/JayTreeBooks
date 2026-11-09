const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
function player(){
 const events=[],handlers={};
 const video={dataset:{upcomingVideo:'upcoming_novels_teaser_v1'},duration:100,currentTime:0,played:{length:0,start:()=>0,end:()=>0},addEventListener:(k,f)=>handlers[k]=f};
 const area={dataset:{upcomingSurface:'landing'}};
 const document={readyState:'complete',visibilityState:'visible',querySelectorAll:s=>s==='[data-upcoming-surface]'?[area]:s==='[data-upcoming-video]'?[video]:[],addEventListener:()=>{}};
 const window={location:{hostname:'jaytreebooks.com',pathname:'/upcoming-books.html',search:''},gtag:(...x)=>events.push(x)};
 vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../upcoming.js'),'utf8'),{window,document,URLSearchParams,Set});
 return{events,fire:k=>handlers[k]?.(),watch:percent=>{video.played={length:1,start:()=>0,end:()=>percent};},seek:percent=>{video.currentTime=percent;}};
}
test('video start and viewing milestones are each counted once per visit',()=>{
 const p=player();p.fire('play');p.fire('play');
 assert.equal(p.events.filter(e=>e[1]==='upcoming_video_start').length,1);
 p.watch(52);p.fire('timeupdate');p.fire('timeupdate');
 assert.deepEqual(p.events.filter(e=>e[1]==='upcoming_video_progress').map(e=>e[2].video_percent),[25,50]);
 p.watch(100);p.fire('timeupdate');p.fire('ended');p.fire('ended');
 assert.equal(p.events.filter(e=>e[1]==='upcoming_video_complete').length,1);
});
test('seeking to the end never counts as a completed viewing',()=>{
 const p=player();p.fire('play');p.seek(100);p.fire('timeupdate');p.fire('ended');
 assert.equal(p.events.filter(e=>e[1]==='upcoming_video_complete').length,0);
 assert.equal(p.events.filter(e=>e[1]==='upcoming_video_progress').length,0);
});

