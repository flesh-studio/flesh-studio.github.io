/* =========================================================
   FLESH STUDIO — hero3d.js
   Triple rayo de la marca extruido en 3D (Three.js).
   Responsabilidad única: la pieza focal del hero.
   - DPR limitado, pausa fuera de pantalla / pestaña oculta
   - Reduced motion o sin WebGL → queda el SVG estático (poster)
   ========================================================= */
import * as THREE from "../vendor/three.module.min.js";

const host = document.querySelector(".hero__canvas");
const hero = document.querySelector(".hero");
const RM = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function webglOK() {
  try { const c = document.createElement("canvas"); return !!(c.getContext("webgl2") || c.getContext("webgl")); }
  catch (e) { return false; }
}

if (host && hero && !RM && webglOK()) {
  try { init(); } catch (e) { console.warn("[flesh] hero3d", e); }
}

function boltShape() {
  // Mismo trazo que el isotipo SVG (caja 100x160), centrado y escalado
  const pts = [[38, 0], [78, 0], [58, 62], [86, 62], [28, 160], [44, 86], [16, 86]];
  const s = new THREE.Shape();
  pts.forEach(([x, y], i) => {
    const X = (x - 50) / 50, Y = -(y - 80) / 50;
    i ? s.lineTo(X, Y) : s.moveTo(X, Y);
  });
  s.closePath();
  return s;
}

function init() {
  const canvas = document.createElement("canvas");
  canvas.setAttribute("aria-hidden", "true");
  host.appendChild(canvas);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: "high-performance" });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  camera.position.set(0, 0, 9);

  // --- geometría compartida
  const geo = new THREE.ExtrudeGeometry(boltShape(), {
    depth: 0.34, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.035, bevelSegments: 4, curveSegments: 1
  });
  geo.center();
  const faceMat = new THREE.MeshStandardMaterial({ color: 0x151517, metalness: 0.55, roughness: 0.28 });
  const sideMat = new THREE.MeshStandardMaterial({ color: 0xff5b1f, emissive: 0xff5b1f, emissiveIntensity: 0.55, metalness: 0.2, roughness: 0.35 });

  const group = new THREE.Group();
  const bolts = [];
  for (let i = 0; i < 3; i++) {
    const m = new THREE.Mesh(geo, [faceMat, sideMat]);
    m.position.set(i * 0.42 - 0.42, i * 0.22 - 0.22, -i * 0.42);
    group.add(m); bolts.push(m);
  }
  group.rotation.set(0.12, -0.5, 0.06);
  scene.add(group);

  // --- partículas (profundidad sutil)
  const N = 260, pos = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    pos[i * 3] = (Math.random() - 0.5) * 16;
    pos[i * 3 + 1] = (Math.random() - 0.5) * 10;
    pos[i * 3 + 2] = (Math.random() - 0.5) * 8 - 2;
  }
  const pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const pMat = new THREE.PointsMaterial({ color: 0xff8a3d, size: 0.03, transparent: true, opacity: 0.6, depthWrite: false });
  const points = new THREE.Points(pGeo, pMat);
  scene.add(points);

  // --- luces
  scene.add(new THREE.AmbientLight(0xffffff, 0.35));
  const key = new THREE.DirectionalLight(0xfff1e4, 2.2); key.position.set(3, 4, 5); scene.add(key);
  const rim = new THREE.PointLight(0xff5b1f, 40, 20); rim.position.set(-3, -1, -2); scene.add(rim);
  const fill = new THREE.PointLight(0xffffff, 12, 15); fill.position.set(-4, 3, 4); scene.add(fill);

  // --- layout responsivo
  let w = 0, h = 0;
  function resize() {
    w = host.clientWidth; h = host.clientHeight;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    const wide = camera.aspect > 1.1;
    group.position.set(wide ? 2.75 : 0.9, wide ? 0.1 : 1.5, 0);
    const s = wide ? 0.88 : 0.78;
    group.scale.setScalar(s);
  }
  const ro = new ResizeObserver(resize); ro.observe(host); resize();

  // --- puntero (aditivo, con fallback táctil)
  const target = { x: 0, y: 0 }, cur = { x: 0, y: 0 };
  let lastMove = 0;
  function onMove(e) {
    const now = performance.now(); if (now - lastMove < 16) return; lastMove = now;
    target.x = (e.clientX / innerWidth) * 2 - 1;
    target.y = (e.clientY / innerHeight) * 2 - 1;
  }
  function reset() { target.x = 0; target.y = 0; }
  window.addEventListener("pointermove", onMove, { passive: true });
  window.addEventListener("blur", reset);
  document.addEventListener("pointerleave", reset);

  // --- scroll
  let scrollP = 0;
  function onScroll() { scrollP = Math.min(1, window.scrollY / (hero.offsetHeight || 1)); }
  window.addEventListener("scroll", onScroll, { passive: true });

  // --- loop con pausa
  let raf = 0, running = false, visible = true;
  const clock = new THREE.Clock();
  function frame() {
    const t = clock.getElapsedTime();
    cur.x += (target.x - cur.x) * 0.05; cur.y += (target.y - cur.y) * 0.05;
    group.rotation.y = -0.5 + Math.sin(t * 0.45) * 0.35 + cur.x * 0.45 + scrollP * 1.4;
    group.rotation.x = 0.12 + Math.sin(t * 0.3) * 0.06 + cur.y * 0.25;
    bolts.forEach((b, i) => { b.position.y = i * 0.22 - 0.22 + Math.sin(t * 1.2 + i * 0.9) * 0.05; });
    sideMat.emissiveIntensity = 0.5 + Math.sin(t * 2) * 0.12;
    points.rotation.y = t * 0.02 + cur.x * 0.1;
    camera.position.z = 9 + scrollP * 3;
    renderer.render(scene, camera);
    raf = requestAnimationFrame(frame);
  }
  function start() { if (running || !visible || document.hidden) return; running = true; clock.start(); raf = requestAnimationFrame(frame); }
  function stop() { running = false; cancelAnimationFrame(raf); }

  const io = new IntersectionObserver(([e]) => { visible = e.isIntersecting; visible ? start() : stop(); }, { threshold: 0 });
  io.observe(hero);
  document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));

  canvas.addEventListener("webglcontextlost", (e) => { e.preventDefault(); stop(); hero.classList.remove("has-webgl"); });

  renderer.render(scene, camera);
  hero.classList.add("has-webgl");
  start();

  window.addEventListener("pagehide", () => {
    stop(); ro.disconnect(); io.disconnect();
    window.removeEventListener("pointermove", onMove);
    window.removeEventListener("scroll", onScroll);
    geo.dispose(); faceMat.dispose(); sideMat.dispose(); pGeo.dispose(); pMat.dispose();
    renderer.dispose();
  });
}
