(function(){
  var link=document.querySelector('[data-secret-path]'), veil=document.querySelector('.secret-dissolve');
  if(!link||!veil) return;
  function playSecretTone(){
    try{
      var AC=window.AudioContext||window.webkitAudioContext,ctx=new AC(),now=ctx.currentTime+.02;
      var master=ctx.createGain(),comp=ctx.createDynamicsCompressor();
      comp.threshold.setValueAtTime(-12,now); comp.knee.setValueAtTime(18,now); comp.ratio.setValueAtTime(4,now); comp.attack.setValueAtTime(.004,now); comp.release.setValueAtTime(.22,now);
      master.gain.setValueAtTime(.0001,now); master.gain.exponentialRampToValueAtTime(.24,now+.035); master.gain.exponentialRampToValueAtTime(.0001,now+1.78); master.connect(comp); comp.connect(ctx.destination);
      [[58,'sine',0,1.28,.78],[87,'triangle',.025,1.08,.34],[116,'sine',.06,.86,.2]].forEach(function(v){
        var o=ctx.createOscillator(),g=ctx.createGain(); o.type=v[1]; o.frequency.setValueAtTime(v[0],now+v[2]); o.frequency.exponentialRampToValueAtTime(v[0]*.92,now+v[2]+v[3]); g.gain.setValueAtTime(.0001,now+v[2]); g.gain.exponentialRampToValueAtTime(v[4],now+v[2]+.028); g.gain.exponentialRampToValueAtTime(.0001,now+v[2]+v[3]); o.connect(g); g.connect(master); o.start(now+v[2]); o.stop(now+v[2]+v[3]+.06);
      });
      var delay=ctx.createDelay(1),feedback=ctx.createGain(),wet=ctx.createGain(); delay.delayTime.setValueAtTime(.19,now); feedback.gain.setValueAtTime(.2,now); wet.gain.setValueAtTime(.34,now); delay.connect(feedback); feedback.connect(delay); delay.connect(wet); wet.connect(master);
      [[392,.18,1.42,.28],[523.25,.245,1.23,.22],[783.99,.31,1.02,.13]].forEach(function(v){
        var o=ctx.createOscillator(),g=ctx.createGain(); o.type='sine'; o.frequency.setValueAtTime(v[0],now+v[1]); g.gain.setValueAtTime(.0001,now+v[1]); g.gain.exponentialRampToValueAtTime(v[3],now+v[1]+.014); g.gain.exponentialRampToValueAtTime(.0001,now+v[1]+v[2]); o.connect(g); g.connect(master); g.connect(delay); o.start(now+v[1]); o.stop(now+v[1]+v[2]+.06);
      });
      var b=ctx.createBuffer(1,Math.floor(ctx.sampleRate*1.4),ctx.sampleRate),d=b.getChannelData(0); for(var i=0;i<d.length;i++) d[i]=(Math.random()*2-1)*Math.pow(1-i/d.length,2); var n=ctx.createBufferSource(),hp=ctx.createBiquadFilter(),ng=ctx.createGain(); n.buffer=b; hp.type='highpass'; hp.frequency.setValueAtTime(1100,now); ng.gain.setValueAtTime(.0001,now); ng.gain.exponentialRampToValueAtTime(.06,now+.26); ng.gain.exponentialRampToValueAtTime(.0001,now+1.35); n.connect(hp); hp.connect(ng); ng.connect(master); n.start(now); n.stop(now+1.4);
      setTimeout(function(){try{ctx.close()}catch(_){}},2200);
    }catch(_){}
  }
  var activated=false;
  link.addEventListener('click',function(e){
    if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||e.button>0||activated) return;
    e.preventDefault(); activated=true;
    if(typeof window.gtag==='function') gtag('event','easter_egg_activate',{secret_id:'jaytree_interactive',trigger_location:'homepage_footer_root',reduced_motion:window.matchMedia('(prefers-reduced-motion: reduce)').matches,transport_type:'beacon'});
    playSecretTone();
    try{sessionStorage.setItem('jt-secret-enter','1')}catch(_){}
    if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){window.location.href=link.href;return;}
    veil.classList.add('is-entering');
    document.documentElement.classList.add('secret-path-open');
    setTimeout(function(){window.location.href=link.href},1450);
  });
})();
