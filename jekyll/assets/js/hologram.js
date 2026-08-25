/*
 * CallGuard 표지 홀로그램 — 구체 와이어프레임이 회전하며 음성 레벨(또는 idle 호흡)에
 * 반응한다. 원본 컨셉: /Users/ryujun/Downloads/hologram-blog.html
 * (관측 기록 — Observation Log) 를 CallGuard 표지용으로 가져와 단순화했다.
 *
 * "통화 음성을 실시간으로 듣는다"는 제품 자체의 이야기와 맞아떨어지도록,
 * 마이크를 연결하면 실제 음성 레벨에 홀로그램이 반응한다. 연결 안 하면
 * idle 호흡 패턴으로 계속 살아있게 움직인다 — 정적 이미지가 아니다.
 *
 * prefers-reduced-motion: reduce 인 경우 한 프레임만 그리고 멈춘다.
 */
(() => {
  'use strict';

  const cv = document.getElementById('hologram');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  let W = 0, H = 0, DPR = 1, R = 0, CX = 0, CY = 0;

  let nodes = [], links = [], bands = [], spikes = [], pulses = [];

  function spherePoint(i, n) {
    const y = 1 - (i / (n - 1)) * 2;
    const r = Math.sqrt(Math.max(0, 1 - y * y));
    const th = i * 2.399963229728653; // 황금각
    return { x: Math.cos(th) * r, y, z: Math.sin(th) * r };
  }

  function buildSphere() {
    const N = W < 700 ? 320 : 560;
    nodes = [];
    for (let i = 0; i < N; i++) {
      const p = spherePoint(i, N);
      const cluster = 0.55 + 0.45 * Math.sin(p.y * 7.3 + p.x * 4.1) * Math.cos(p.z * 5.7);
      nodes.push({
        ...p,
        s: 0.5 + Math.pow(Math.random(), 2.4) * 2.2,
        a: 0.25 + Math.abs(cluster) * 0.75,
        ph: Math.random() * Math.PI * 2,
        hot: Math.random() < 0.07,
      });
    }

    links = [];
    const maxD = 0.30;
    for (let i = 0; i < nodes.length; i += 1) {
      const a = nodes[i];
      let tries = 0, made = 0;
      while (tries < 14 && made < 2) {
        const j = (i + 1 + ((Math.random() * 40) | 0)) % nodes.length;
        const b = nodes[j];
        const d = Math.hypot(a.x - b.x, a.y - b.y, a.z - b.z);
        if (d < maxD && d > 0.04) {
          const t = 0.35 + Math.random() * 0.3;
          const m = { x: a.x + (b.x - a.x) * t, y: a.y, z: a.z + (b.z - a.z) * t };
          const L = Math.hypot(m.x, m.y, m.z) || 1;
          m.x /= L; m.y /= L; m.z /= L;
          links.push({ a, b, m, w: 0.4 + Math.random() * 0.7, o: 0.10 + Math.random() * 0.30 });
          made++;
        }
        tries++;
      }
    }

    bands = [];
    for (let i = 0; i < 4; i++) {
      bands.push({
        tilt: (Math.random() - 0.5) * 1.9,
        roll: Math.random() * Math.PI,
        spin: (Math.random() < 0.5 ? -1 : 1) * (0.10 + Math.random() * 0.22),
        rad: 0.72 + Math.random() * 0.30,
        w: 1.0 + Math.random() * 1.8,
        o: 0.20 + Math.random() * 0.30,
        arc: 0.9 + Math.random() * 1.5,
      });
    }

    spikes = [];
    const S = W < 700 ? 70 : 120;
    for (let i = 0; i < S; i++) {
      const p = spherePoint((i * 7 + 3) % 997, 997);
      spikes.push({ ...p, len: 0.04 + Math.pow(Math.random(), 2) * 0.22, o: 0.15 + Math.random() * 0.45 });
    }

    pulses = [];
    for (let i = 0; i < 22; i++) {
      pulses.push({ li: (Math.random() * links.length) | 0, t: Math.random(), sp: 0.25 + Math.random() * 0.7 });
    }
  }

  const FOV = 3.1;
  let rotY = 0, rotX = -0.18;

  function project(p, scale) {
    const cy = Math.cos(rotY), sy = Math.sin(rotY);
    const x1 = p.x * cy + p.z * sy;
    const z1 = -p.x * sy + p.z * cy;
    const cx = Math.cos(rotX), sx = Math.sin(rotX);
    const y2 = p.y * cx - z1 * sx;
    const z2 = p.y * sx + z1 * cx;
    const k = FOV / (FOV + z2);
    return { x: CX + x1 * R * scale * k, y: CY + y2 * R * scale * k, d: (z2 + 1) / 2, k };
  }

  // --- 음성 레벨 (마이크 연결 시 실제 입력, 아니면 idle 호흡) ---
  const micBtn = document.getElementById('hologramMic');
  let analyser = null, timeData = null, audioCtx = null, live = false;
  let level = 0;
  const RINGN = 160;
  const ring = new Float32Array(RINGN);

  async function toggleMic() {
    if (live) { stopMic(); return; }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const src = audioCtx.createMediaStreamSource(stream);
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 1024;
      analyser.smoothingTimeConstant = 0.7;
      src.connect(analyser);
      timeData = new Uint8Array(analyser.fftSize);
      live = true;
      if (micBtn) { micBtn.textContent = '음성 연결 해제'; micBtn.dataset.live = 'true'; }
      micBtn._stream = stream;
    } catch (e) {
      if (micBtn) micBtn.textContent = '마이크 권한 거부됨';
    }
  }
  function stopMic() {
    micBtn?._stream?.getTracks().forEach((t) => t.stop());
    audioCtx?.close();
    analyser = null; live = false;
    if (micBtn) { micBtn.textContent = '음성으로 확인하기'; micBtn.dataset.live = 'false'; }
  }
  micBtn?.addEventListener('click', toggleMic);

  function idleSignal(t) {
    let peak = 0;
    const breathe = 0.20 + 0.16 * Math.sin(t * 0.5) + 0.09 * Math.sin(t * 0.23 + 1.3);
    for (let i = 0; i < RINGN; i++) {
      const u = (i / RINGN) * Math.PI * 2;
      const v = Math.sin(u * 3 + t * 1.1) * 0.5 + Math.sin(u * 7 - t * 1.7) * 0.3 + Math.sin(u * 13 + t * 2.6) * 0.16;
      ring[i] = v * breathe;
      peak = Math.max(peak, Math.abs(ring[i]));
    }
    return peak;
  }
  function readMic() {
    analyser.getByteTimeDomainData(timeData);
    const step = Math.floor(timeData.length / RINGN);
    let peak = 0;
    for (let i = 0; i < RINGN; i++) {
      const v = (timeData[i * step] - 128) / 128;
      ring[i] = v * 2.2;
      peak = Math.max(peak, Math.abs(v));
    }
    return Math.min(1, peak * 2.4);
  }

  function drawSphere(t) {
    const scale = 1 + level * 0.10;
    ctx.globalCompositeOperation = 'lighter';

    const cr = R * (0.34 + level * 0.16);
    const cg = ctx.createRadialGradient(CX, CY, 0, CX, CY, cr);
    cg.addColorStop(0, `rgba(255,240,205,${0.55 + level * 0.35})`);
    cg.addColorStop(0.18, `rgba(255,214,138,${0.28 + level * 0.22})`);
    cg.addColorStop(0.52, `rgba(245,166,35,${0.10 + level * 0.10})`);
    cg.addColorStop(1, 'rgba(180,83,9,0)');
    ctx.fillStyle = cg;
    ctx.fillRect(CX - cr, CY - cr, cr * 2, cr * 2);

    for (const b of bands) {
      b.roll += b.spin * 0.006;
      ctx.beginPath();
      const steps = 80;
      for (let i = 0; i <= steps; i++) {
        const th = b.roll + (i / steps) * b.arc * Math.PI;
        const p0 = { x: Math.cos(th) * b.rad, y: Math.sin(th) * b.rad * Math.sin(b.tilt), z: Math.sin(th) * b.rad * Math.cos(b.tilt) };
        const p = project(p0, scale);
        i === 0 ? ctx.moveTo(p.x, p.y) : ctx.lineTo(p.x, p.y);
      }
      ctx.strokeStyle = `rgba(255,205,120,${b.o * (0.5 + level * 0.6)})`;
      ctx.lineWidth = b.w * (1 + level * 0.5);
      ctx.shadowColor = 'rgba(245,166,35,.9)';
      ctx.shadowBlur = 10 + level * 22;
      ctx.stroke();
      ctx.shadowBlur = 0;
    }

    ctx.lineWidth = 0.7;
    for (const l of links) {
      const A = project(l.a, scale), M = project(l.m, scale), B = project(l.b, scale);
      const d = (A.d + B.d) / 2;
      const a = l.o * (0.16 + d * 0.9);
      if (a < 0.02) continue;
      ctx.beginPath();
      ctx.moveTo(A.x, A.y); ctx.lineTo(M.x, M.y); ctx.lineTo(B.x, B.y);
      ctx.strokeStyle = `rgba(245,166,35,${a})`;
      ctx.stroke();
    }

    for (const pu of pulses) {
      const l = links[pu.li]; if (!l) continue;
      pu.t += pu.sp * 0.012 * (1 + level * 2.2);
      if (pu.t > 1) { pu.t = 0; pu.li = (Math.random() * links.length) | 0; }
      const seg = pu.t < 0.5 ? [l.a, l.m, pu.t * 2] : [l.m, l.b, (pu.t - 0.5) * 2];
      const p0 = project(seg[0], scale), p1 = project(seg[1], scale);
      const x = p0.x + (p1.x - p0.x) * seg[2];
      const y = p0.y + (p1.y - p0.y) * seg[2];
      ctx.beginPath();
      ctx.arc(x, y, 1.4 + level * 2.2, 0, 7);
      ctx.fillStyle = `rgba(255,244,214,${0.35 + p0.d * 0.5})`;
      ctx.shadowColor = 'rgba(255,214,138,.9)';
      ctx.shadowBlur = 8;
      ctx.fill();
      ctx.shadowBlur = 0;
    }

    for (const s of spikes) {
      const p0 = project(s, scale);
      const out = { x: s.x * (1 + s.len), y: s.y * (1 + s.len), z: s.z * (1 + s.len) };
      const p1 = project(out, scale);
      const limb = 1 - Math.abs(p0.d * 2 - 1);
      const a = s.o * (0.25 + level * 0.6) * (0.35 + limb * 0.8);
      ctx.beginPath();
      ctx.moveTo(p0.x, p0.y); ctx.lineTo(p1.x, p1.y);
      ctx.strokeStyle = `rgba(255,190,90,${a})`;
      ctx.lineWidth = 0.8;
      ctx.stroke();
    }

    for (const n of nodes) {
      const p = project(n, scale);
      const tw = 0.7 + 0.3 * Math.sin(t * 1.6 + n.ph);
      const a = n.a * tw * (0.14 + p.d * 0.95) * (1 + level * 0.5);
      if (a < 0.02) continue;
      const r = n.s * p.k * (1 + level * 0.35);
      ctx.beginPath();
      ctx.arc(p.x, p.y, r, 0, 7);
      ctx.fillStyle = n.hot ? `rgba(255,244,214,${Math.min(1, a * 1.25)})` : `rgba(245,176,60,${a})`;
      ctx.fill();
    }
  }

  function drawRing() {
    ctx.globalCompositeOperation = 'lighter';
    const base = R * 1.20;
    ctx.beginPath();
    for (let i = 0; i <= RINGN; i++) {
      const idx = i % RINGN;
      const th = (i / RINGN) * Math.PI * 2 - Math.PI / 2;
      const rr = base + ring[idx] * R * 0.24;
      const x = CX + Math.cos(th) * rr;
      const y = CY + Math.sin(th) * rr * 0.99;
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.strokeStyle = `rgba(255,214,138,${0.30 + level * 0.55})`;
    ctx.lineWidth = 1.1 + level * 1.6;
    ctx.shadowColor = 'rgba(245,166,35,.8)';
    ctx.shadowBlur = 8 + level * 20;
    ctx.stroke();
    ctx.shadowBlur = 0;

    ctx.strokeStyle = `rgba(110,143,214,${0.20 + level * 0.2})`;
    ctx.lineWidth = 1;
    for (let i = 0; i < 40; i++) {
      const th = (i / 40) * Math.PI * 2 - Math.PI / 2;
      const tall = i % 5 === 0;
      const r0 = base + R * 0.075, r1 = r0 + (tall ? R * 0.038 : R * 0.016);
      ctx.beginPath();
      ctx.moveTo(CX + Math.cos(th) * r0, CY + Math.sin(th) * r0);
      ctx.lineTo(CX + Math.cos(th) * r1, CY + Math.sin(th) * r1);
      ctx.stroke();
    }
  }

  function clear() {
    ctx.globalCompositeOperation = 'source-over';
    ctx.clearRect(0, 0, W, H);
  }

  let raf = null;
  function frame(ms) {
    const t = ms / 1000;
    const peak = live && analyser ? readMic() : idleSignal(t);
    level += (peak - level) * 0.13;
    rotY += 0.0014 + level * 0.004;

    clear();
    drawSphere(t);
    drawRing();
    ctx.globalCompositeOperation = 'source-over';
    raf = requestAnimationFrame(frame);
  }

  function resize() {
    const rect = cv.parentElement.getBoundingClientRect();
    DPR = Math.min(devicePixelRatio || 1, 2);
    W = rect.width; H = rect.height;
    cv.width = W * DPR; cv.height = H * DPR;
    cv.style.width = W + 'px'; cv.style.height = H + 'px';
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    CX = W / 2; CY = H / 2;
    R = Math.min(W, H) * 0.34;
    buildSphere();
  }

  let rt;
  addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(resize, 160); });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) { cancelAnimationFrame(raf); raf = null; }
    else if (!raf && !reduced) raf = requestAnimationFrame(frame);
  });

  resize();
  if (reduced) {
    level = 0.18; idleSignal(1.4);
    clear(); drawSphere(1.4); drawRing();
    ctx.globalCompositeOperation = 'source-over';
    if (micBtn) micBtn.style.display = 'none';
  } else {
    raf = requestAnimationFrame(frame);
  }
})();
