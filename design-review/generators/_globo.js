(function(){
  const cv = document.getElementById('globe');
  if(!cv) return;
  const ctx = cv.getContext('2d');
  const parado = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // --- pontos distribuídos uniformemente na esfera (espiral de Fibonacci) ---
  const N = 2400, PHI = Math.PI * (3 - Math.sqrt(5)), pts = [];
  for(let i=0;i<N;i++){
    const y = 1 - (i/(N-1))*2, r = Math.sqrt(1-y*y), t = PHI*i;
    pts.push([Math.cos(t)*r, y, Math.sin(t)*r]);
  }

  const rad = d => d*Math.PI/180;
  // (arco Brasil ↔ Moçambique removido a pedido do usuário, 2026-09-12)

  const TILT = rad(16);
  function girar(p, ang){
    const [x,y,z]=p;
    const x1 = x*Math.cos(ang) + z*Math.sin(ang);
    const z1 = -x*Math.sin(ang) + z*Math.cos(ang);
    const y2 = y*Math.cos(TILT) - z1*Math.sin(TILT);
    const z2 = y*Math.sin(TILT) + z1*Math.cos(TILT);
    return [x1, y2, z2];
  }

  let W=0,H=0,R=0,cx=0,cy=0;
  function medir(){
    const dpr = Math.min(devicePixelRatio||1, 2);
    W = cv.clientWidth; H = cv.clientHeight;
    cv.width = W*dpr; cv.height = H*dpr;
    ctx.setTransform(dpr,0,0,dpr,0,0);
    R = Math.min(W,H)*0.36; cx = W/2; cy = H/2;
  }
  medir(); addEventListener('resize', medir);

  function desenhar(ang){
    ctx.clearRect(0,0,W,H);

    // pontos: só o hemisfério visível, opacidade pela profundidade
    for(const p of pts){
      const [x,y,z] = girar(p, ang);
      if(z < 0) continue;
      const px = cx + x*R, py = cy - y*R;
      const a = 0.16 + z*0.62;
      ctx.beginPath();
      ctx.arc(px, py, 0.8 + z*1.25, 0, 6.2832);
      ctx.fillStyle = 'rgba(143,59,21,' + a.toFixed(3) + ')';
      ctx.fill();
    }

  }

  if(parado){ desenhar(rad(-97.65)); return; }   // acessibilidade: sem animação
  // dentro do deck (index.html), só desenha enquanto a capa está na tela
  const sec = cv.closest('.slide-sec');
  let t0 = null;
  (function loop(ts){
    if(t0===null) t0=ts;
    if(!sec || sec.classList.contains('on'))
      desenhar(((ts-t0)/1000) * 0.045 + rad(-97.65));   // ~1 volta a cada 114s
    requestAnimationFrame(loop);
  })(performance.now());
})();
