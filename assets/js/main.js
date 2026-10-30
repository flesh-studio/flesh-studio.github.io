/* =========================================================
   FLESH STUDIO — main.js
   GSAP + ScrollTrigger + Lenis (único motor de smooth-scroll)
   Cada módulo corre aislado: si uno falla, el resto del sitio sigue.
   ========================================================= */
(function () {
  "use strict";
  var root = document.documentElement;
  var RM = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var FINE = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var hasGSAP = typeof window.gsap !== "undefined" && typeof window.ScrollTrigger !== "undefined";
  if (hasGSAP) gsap.registerPlugin(ScrollTrigger);
  var lenis = null;

  function safe(name, fn) { try { fn(); } catch (e) { console.warn("[flesh] " + name + " falló:", e); } }
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* ---------- smooth scroll (Lenis) ---------- */
  function initLenis() {
    if (RM || !hasGSAP || typeof window.Lenis === "undefined") return;
    lenis = new Lenis({ duration: 1.15, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }, smoothWheel: true });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    window.addEventListener("pagehide", function () { lenis && lenis.destroy(); });
    // anchors
    $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener("click", function (e) {
        var id = a.getAttribute("href");
        if (id.length < 2) return;
        var t = $(id); if (!t) return;
        e.preventDefault(); lenis.scrollTo(t, { offset: -80 });
      });
    });
  }

  /* ---------- header ---------- */
  function initHeader() {
    var h = $(".header"); if (!h) return;
    var last = 0;
    function on() {
      var y = window.scrollY;
      h.classList.toggle("is-scrolled", y > 30);
      root.classList.toggle("show-wa", y > (document.querySelector(".hero") ? innerHeight * .8 : 200));
      h.classList.toggle("is-hidden", y > last && y > 400 && !root.classList.contains("menu-open"));
      last = y;
    }
    window.addEventListener("scroll", on, { passive: true }); on();
  }

  /* ---------- mobile menu ---------- */
  function initMenu() {
    var b = $(".burger"), m = $(".mobile-menu"); if (!b || !m) return;
    function set(open) {
      root.classList.toggle("menu-open", open);
      b.setAttribute("aria-expanded", open ? "true" : "false");
      b.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
      m.setAttribute("aria-hidden", open ? "false" : "true");
      if (lenis) open ? lenis.stop() : lenis.start();
      document.body.style.overflow = open ? "hidden" : "";
      if (open) { var f = m.querySelector("a"); f && setTimeout(function () { f.focus(); }, 300); }
    }
    b.addEventListener("click", function () { set(!root.classList.contains("menu-open")); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && root.classList.contains("menu-open")) { set(false); b.focus(); } });
    $$("a", m).forEach(function (a) { a.addEventListener("click", function () { set(false); }); });
  }

  /* ---------- cursor ---------- */
  function initCursor() {
    if (!FINE || RM) return;
    var c = document.createElement("div"); c.className = "cursor"; c.setAttribute("aria-hidden", "true");
    c.innerHTML = '<span class="cursor__label">VER</span>'; document.body.appendChild(c);
    var x = innerWidth / 2, y = innerHeight / 2, cx = x, cy = y, raf = null;
    function loop() { cx += (x - cx) * .22; cy += (y - cy) * .22; c.style.transform = "translate(" + cx + "px," + cy + "px)"; raf = Math.abs(x - cx) + Math.abs(y - cy) > .1 ? requestAnimationFrame(loop) : null; }
    window.addEventListener("pointermove", function (e) { x = e.clientX; y = e.clientY; c.classList.add("is-on"); if (!raf) raf = requestAnimationFrame(loop); }, { passive: true });
    document.addEventListener("pointerleave", function () { c.classList.remove("is-on"); });
    window.addEventListener("blur", function () { c.classList.remove("is-on"); });
    document.addEventListener("pointerover", function (e) {
      var v = e.target.closest("[data-cursor='view']");
      var l = e.target.closest("a,button,input,select,textarea,label,.lot");
      c.classList.toggle("is-view", !!v); c.classList.toggle("is-hover", !v && !!l);
      if (v) c.querySelector(".cursor__label").textContent = v.getAttribute("data-cursor-label") || "VER";
    });
  }

  /* ---------- split text (palabra por palabra, accesible) ---------- */
  function splitWords(el) {
    if (el.dataset.splitDone) return;
    el.setAttribute("aria-label", el.textContent.replace(/\s+/g, " ").trim());
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var parts = n.textContent.split(/(\s+)/), frag = document.createDocumentFragment();
          parts.forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(" ")); return; }
            var w = document.createElement("span"); w.className = "split-w"; w.setAttribute("aria-hidden", "true");
            var i = document.createElement("span"); i.textContent = p; w.appendChild(i); frag.appendChild(w);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== "BR") { n.setAttribute("aria-hidden", "true"); walk(n); }
      });
    })(el);
    el.dataset.splitDone = "1";
  }
  function initSplit() {
    if (!hasGSAP || RM) return;
    $$("[data-split]").forEach(function (el) {
      if (el.closest(".hero")) return; // el hero tiene su propia intro
      splitWords(el);
      gsap.from(el.querySelectorAll(".split-w > span"), {
        yPercent: 110, duration: 1, ease: "expo.out", stagger: .06,
        scrollTrigger: { trigger: el, start: "top 85%", once: true }
      });
    });
  }

  /* ---------- generic reveals ---------- */
  function initReveal() {
    var els = $$("[data-reveal]"); if (!els.length) return;
    if (!hasGSAP || RM) { els.forEach(function (e) { e.style.opacity = 1; e.style.transform = "none"; }); return; }
    ScrollTrigger.batch(els, {
      start: "top 88%", once: true,
      onEnter: function (b) { gsap.to(b, { opacity: 1, y: 0, duration: 1, ease: "expo.out", stagger: .08 }); }
    });
  }

  /* ---------- hero intro ---------- */
  function initHeroIntro() {
    var h = $(".hero"); if (!h || !hasGSAP || RM || !$(".hero__in", h)) return;
    var title = $("h1", h); splitWords(title);
    var tl = gsap.timeline({ defaults: { ease: "expo.out" } });
    tl.from(title.querySelectorAll(".split-w > span"), { yPercent: 115, duration: 1.3, stagger: .05 }, .15)
      .from(".hero__top > *", { opacity: 0, y: 16, duration: .8, stagger: .1 }, .1)
      .from(".hero__sub", { opacity: 0, y: 24, duration: 1 }, .7)
      .from(".hero__ctas > *", { opacity: 0, y: 20, duration: .9, stagger: .08 }, .8)
      .from(".scroll-hint", { opacity: 0, duration: 1 }, 1.2);
    // salida del hero al scrollear
    gsap.to(".hero__in", { yPercent: -18, opacity: .2, ease: "none", scrollTrigger: { trigger: h, start: "top top", end: "bottom top", scrub: true } });
  }

  /* ---------- hero: showreel de fondo (1080p en desktop, 720p en mobile) ---------- */
  function initHeroVideo() {
    var v = $(".hero__video"); if (!v) return;
    var mobile = window.matchMedia("(max-width: 900px)").matches;
    v.src = mobile ? v.dataset.srcMobile : v.dataset.srcDesktop;
    if (RM) return;                       // movimiento reducido: queda el póster
    v.preload = "auto";
    var io = new IntersectionObserver(function (es) { es[0].isIntersecting ? v.play().catch(function () {}) : v.pause(); }, { threshold: .05 });
    io.observe(v);
  }

  /* ---------- manifiesto: palabras que se encienden ---------- */
  function initManifesto() {
    var t = $(".manifesto__text"); if (!t) return;
    t.setAttribute("aria-label", t.textContent.replace(/\s+/g, " ").trim());
    var esc = function (s) { return s.replace(/[&<>"']/g, function (ch) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]; }); };
    var html = "", words = t.textContent.trim().split(/\s+/).map(esc);
    var mk = (t.getAttribute("data-mark") || "").toLowerCase().split(/\s+/).filter(Boolean), m0 = -1;
    if (mk.length) for (var i = 0; i + mk.length <= words.length; i++) {
      if (words.slice(i, i + mk.length).map(function (w) { return w.toLowerCase().replace(/[.,;:!?]+$/, ""); }).join(" ") === mk.join(" ")) { m0 = i; break; }
    }
    words.forEach(function (w, i) {
      var tail = "";
      if (i === m0) html += '<span class="mmark">';
      if (m0 > -1 && i === m0 + mk.length - 1) { tail = (w.match(/[.,;:!?]+$/) || [""])[0]; w = w.slice(0, w.length - tail.length); }
      html += '<span class="mw" aria-hidden="true">' + w + "</span>";
      if (m0 > -1 && i === m0 + mk.length - 1) html += "</span>" + (tail ? '<span class="mw" aria-hidden="true">' + tail + "</span>" : "");
      html += " ";
    });
    var hi = (t.getAttribute("data-hi") || "").split(",");
    t.innerHTML = html;
    var mark = $(".mmark", t);
    $$(".mw", t).forEach(function (s) { if (hi.indexOf(s.textContent.replace(/[.,]/g, "")) > -1) s.style.color = "var(--orange)"; });
    if (!hasGSAP || RM) return;
    gsap.to($$(".mw", t), { opacity: 1, stagger: .1, ease: "none", scrollTrigger: { trigger: t, start: "top 80%", end: "bottom 45%", scrub: true } });
    if (mark) { mark.classList.add("is-wait"); ScrollTrigger.create({ trigger: t, start: "bottom 52%", onEnter: function () { mark.classList.remove("is-wait"); }, onLeaveBack: function () { mark.classList.add("is-wait"); } }); }
  }

  /* ---------- reel: se expande con el scroll ---------- */
  function initReel() {
    var f = $(".reel__frame"); if (!f) return;
    var v = $("video", f), btn = $(".reel__toggle");
    if (v) {
      if (RM) { v.removeAttribute("autoplay"); v.pause(); }
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (!v.dataset.paused) e.isIntersecting ? v.play().catch(function () {}) : v.pause(); }); }, { threshold: .1 });
      io.observe(v);
      if (btn) btn.addEventListener("click", function () {
        if (v.paused) { v.dataset.paused = ""; v.play().catch(function () {}); btn.querySelector("span").textContent = "Pausar"; btn.setAttribute("aria-pressed", "false"); }
        else { v.dataset.paused = "1"; v.pause(); btn.querySelector("span").textContent = "Reproducir"; btn.setAttribute("aria-pressed", "true"); }
      });
    }
    if (!hasGSAP || RM) return;
    gsap.fromTo(f, { clipPath: "inset(0% 18% 0% 18% round 24px)" }, { clipPath: "inset(0% 0% 0% 0% round 14px)", ease: "none", scrollTrigger: { trigger: f, start: "top 85%", end: "top 15%", scrub: true } });
    gsap.from(".reel__big", { yPercent: 40, ease: "none", scrollTrigger: { trigger: f, start: "top bottom", end: "bottom top", scrub: true } });
  }

  /* ---------- servicios: imagen que sigue al cursor ---------- */
  function initSvcFloat() {
    var list = $(".svc-list"), fl = $(".svc-float"); if (!list || !fl || !FINE) return;
    var imgs = $$("img", fl), x = 0, y = 0, cx = 0, cy = 0, raf = null;
    function loop() { cx += (x - cx) * .15; cy += (y - cy) * .15; fl.style.left = cx + 20 + "px"; fl.style.top = cy - 140 + "px"; raf = requestAnimationFrame(loop); }
    $$(".svc-item", list).forEach(function (it, i) {
      it.addEventListener("pointerenter", function () { imgs.forEach(function (im, j) { im.classList.toggle("is-active", j === i); }); fl.classList.add("is-on"); if (!raf) raf = requestAnimationFrame(loop); });
    });
    list.addEventListener("pointermove", function (e) { x = e.clientX; y = e.clientY; });
    list.addEventListener("pointerleave", function () { fl.classList.remove("is-on"); cancelAnimationFrame(raf); raf = null; });
  }

  /* ---------- marquee reactiva a la velocidad de scroll ---------- */
  function initMarquee() {
    $$(".marquee").forEach(function (m) {
      var tr = $(".marquee__track", m); if (!tr) return;
      if (!hasGSAP || RM) return;
      var dir = m.dataset.dir === "right" ? 1 : -1;
      var tw = gsap.fromTo(tr, { xPercent: dir < 0 ? 0 : -50 }, { xPercent: dir < 0 ? -50 : 0, duration: parseFloat(m.dataset.speed || 28), ease: "none", repeat: -1 });
      var skew = gsap.quickTo(tr, "skewX", { duration: .4, ease: "power3" });
      ScrollTrigger.create({
        trigger: m, start: "top bottom", end: "bottom top",
        onToggle: function (s) { s.isActive ? tw.play() : tw.pause(); },
        onUpdate: function (s) {
          var v = s.getVelocity();
          gsap.to(tw, { timeScale: (v < 0 ? -1 : 1) * Math.min(4, 1 + Math.abs(v) / 600), duration: .3, overwrite: true, onComplete: function () { gsap.to(tw, { timeScale: v < 0 ? -1 : 1, duration: 1 }); } });
          skew(gsap.utils.clamp(-8, 8, v / -300));
        }
      });
    });
  }

  /* ---------- masterplan demo ---------- */
  function initMasterplan() {
    var stage = $(".mp__stage"); if (!stage) return;
    var plan = $(".plan", stage), card = $(".mp__card", stage);
    var lots = $$(".lot", stage);
    function show(l) {
      lots.forEach(function (o) { o.classList.toggle("is-active", o === l); o.setAttribute("aria-pressed", o === l ? "true" : "false"); });
      var s = l.dataset.s;
      $("[data-f='lote']", card).textContent = "Lote " + l.textContent.trim();
      $("[data-f='m2']", card).textContent = l.dataset.m2 + " m²";
      $("[data-f='orient']", card).textContent = l.dataset.o;
      var b = $("[data-f='estado']", card); b.textContent = s; b.setAttribute("data-s", s);
    }
    lots.forEach(function (l) {
      l.addEventListener("click", function () { show(l); });
      l.addEventListener("pointerenter", function () { if (FINE) show(l); });
    });
    if (!hasGSAP || RM) return;
    gsap.fromTo(plan, { rotateX: 62, rotateZ: -36, scale: .9 }, { rotateX: 30, rotateZ: -16, scale: 1, ease: "none", scrollTrigger: { trigger: stage, start: "top 90%", end: "center 40%", scrub: true } });
    gsap.from(lots, { opacity: 0, z: 40, duration: .6, stagger: { each: .025, from: "random" }, ease: "power3.out", scrollTrigger: { trigger: stage, start: "top 75%", once: true } });
  }

  /* ---------- demo de agente IA: mensajes en secuencia ---------- */
  function initChat() {
    var root = $(".wa-demo"), src = $("#wa-data"); if (!root || !src) return;
    var data; try { data = JSON.parse(src.textContent); } catch (e) { return; }
    var body = $(".wa-body", root), nameEl = $(".wa-name", root), st = $(".wa-status", root), av = $(".wa-av", root),
        clock = $(".iph__time", root), field = $(".wa-field", root), txt = $(".wa-text", root), tabs = $$(".wa-tab", root);
    var TICK = '<svg class="wa-tick" viewBox="0 0 16 11" aria-hidden="true"><path d="M11.07.65 4.98 7.9 2.4 5.4 1.3 6.5l3.74 3.6 7.13-8.5zM14.6.65 8.5 7.9l-.88-.86-1.1 1.13 2.03 1.96 7.13-8.5z" fill="currentColor"/></svg>';
    var cur = 0, run = 0, visible = false, started = false, waiting = null;
    function esc(s) { return s.replace(/[&<>]/g, function (ch) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[ch]; }); }
    function hm(t, add) { var p = t.split(":"), m = (+p[0]) * 60 + (+p[1]) + add; return ("0" + Math.floor(m / 60) % 24).slice(-2) + ":" + ("0" + m % 60).slice(-2); }
    function setStatus(typing) { st.textContent = typing ? "escribiendo…" : "en línea"; st.classList.toggle("is-typing", !!typing); }
    function head(c) {
      nameEl.textContent = c.name; av.textContent = c.ini; av.style.background = c.color; clock.textContent = c.time; setStatus(false);
      tabs.forEach(function (b, i) { b.setAttribute("aria-pressed", i === cur ? "true" : "false"); });
    }
    function add(m, i, c, prev) {
      var el = document.createElement("div");
      if (m[0] === "sys") { el.className = "wa-sys"; el.textContent = m[1]; }
      else { el.className = "wa-msg " + m[0] + (prev === m[0] ? " cont" : ""); el.innerHTML = esc(m[1]) + "<em>" + hm(c.time, i) + (m[0] === "out" ? TICK : "") + "</em>"; }
      body.appendChild(el);
    }
    function reset(c) { body.innerHTML = '<span class="wa-day">Hoy</span>'; txt.textContent = ""; field.classList.remove("is-typing"); head(c); }
    function showAll(idx) { cur = idx; var c = data[idx], prev = null; reset(c); c.msgs.forEach(function (m, i) { add(m, i, c, prev); prev = m[0] === "sys" ? null : m[0]; }); }
    if (RM || !("IntersectionObserver" in window)) {
      tabs.forEach(function (b, i) { b.addEventListener("click", function () { showAll(i); }); });
      return;
    }
    root.classList.add("is-armed");
    function play(idx) {
      var my = ++run; cur = idx; var c = data[idx], i = 0, prev = null;
      reset(c); body.classList.remove("is-out");
      function later(fn, ms) { setTimeout(function () { if (my === run) fn(); }, ms); }
      function typeField(s, done) {
        var n = 0, step = Math.max(22, Math.min(55, 1300 / s.length));
        field.classList.add("is-typing");
        (function tick() {
          if (my !== run) return;
          txt.textContent = s.slice(0, ++n);
          if (n < s.length) setTimeout(tick, step);
          else later(function () { txt.textContent = ""; field.classList.remove("is-typing"); done(); }, 280);
        })();
      }
      function next() {
        if (i >= c.msgs.length) {
          later(function () {
            var go = function () { body.classList.add("is-out"); later(function () { play((cur + 1) % data.length); }, 450); };
            visible ? go() : (waiting = go);
          }, 3800);
          return;
        }
        var m = c.msgs[i], k = i; i++;
        if (m[0] === "out") typeField(m[1], function () { add(m, k, c, prev); prev = "out"; later(next, 850); });
        else if (m[0] === "in") {
          setStatus(true);
          var ty = document.createElement("div"); ty.className = "wa-typing"; ty.innerHTML = "<i></i><i></i><i></i>"; body.appendChild(ty);
          later(function () { ty.remove(); setStatus(false); add(m, k, c, prev); prev = "in"; later(next, 1150); }, Math.min(2300, 800 + m[1].length * 12));
        } else later(function () { add(m, k, c, prev); prev = null; later(next, 300); }, 450);
      }
      later(next, 700);
    }
    tabs.forEach(function (b, i) { b.addEventListener("click", function () { waiting = null; started = true; play(i); }); });
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      if (!visible) return;
      if (!started) { started = true; play(0); }
      else if (waiting) { var f = waiting; waiting = null; f(); }
    }, { threshold: .3 }).observe(root);
  }

  /* ---------- carrusel de proyectos (home): avanza solo, frena con el mouse ---------- */
  function initProjectsReel() {
    var box = $(".pr"), tr = $(".pr__track"); if (!box || !tr) return;
    var cards = $$(".pr-card", tr);
    function load(v) { if (v && !v.src && v.dataset.src) v.src = v.dataset.src; }
    function play(c) { var v = $("video", c); if (!v) return; load(v); var p = v.play(); if (p && p.catch) p.catch(function () {}); c.classList.add("is-playing"); }
    function stop(c) { var v = $("video", c); if (!v) return; v.pause(); c.classList.remove("is-playing"); }
    if (RM) return;                                   // movimiento reducido: scroll manual, sin autoplay

    if (!FINE) {                                      // táctil: scroll nativo + avance automático + video en la tarjeta visible
      box.classList.add("is-touch");
      var hold = 0, t0 = performance.now(), visible = false;
      box.addEventListener("touchstart", function () { hold = performance.now() + 2500; }, { passive: true });
      (function loop(now) {
        var dt = Math.min(50, now - t0); t0 = now;
        if (visible && now > hold) { box.scrollLeft += dt * 0.045; if (box.scrollLeft >= tr.scrollWidth / 2) box.scrollLeft -= tr.scrollWidth / 2; }
        requestAnimationFrame(loop);
      })(t0);
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(box);
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? play(e.target) : stop(e.target); }); }, { root: box, threshold: .75 });
      cards.forEach(function (c) { io.observe(c); });
      return;
    }

    var x = 0, speed = 0, BASE = 0.055, target = BASE, half = 0, last = performance.now(), on = false, raf = 0;
    function measure() { half = tr.scrollWidth / 2; }
    function frame(now) {
      var dt = Math.min(50, now - last); last = now;
      speed += (target - speed) * Math.min(1, dt / 220);          // frena y arranca con suavidad
      x -= speed * dt; if (half && -x >= half) x += half;
      tr.style.transform = "translate3d(" + x.toFixed(2) + "px,0,0)";
      raf = on ? requestAnimationFrame(frame) : 0;
    }
    function start() { if (on) return; on = true; last = performance.now(); raf = requestAnimationFrame(frame); }
    function halt() { on = false; cancelAnimationFrame(raf); }
    measure(); window.addEventListener("resize", measure); window.addEventListener("load", measure);
    new IntersectionObserver(function (es) { es[0].isIntersecting && !document.hidden ? start() : halt(); }).observe(box);
    document.addEventListener("visibilitychange", function () { document.hidden ? halt() : start(); });
    box.addEventListener("pointerenter", function () { target = 0; });
    box.addEventListener("pointerleave", function () { target = BASE; });
    box.addEventListener("focusin", function () { target = 0; });
    box.addEventListener("focusout", function () { target = BASE; });
    cards.forEach(function (c) {
      c.addEventListener("pointerenter", function () { play(c); });
      c.addEventListener("pointerleave", function () { stop(c); });
      c.addEventListener("focus", function () { play(c); });
      c.addEventListener("blur", function () { stop(c); });
    });
  }

  /* ---------- tarjetas de trabajo: video al hover + tilt 3D ---------- */
  function initCards() {
    $$(".card").forEach(function (c) {
      var media = $(".card__media", c), v = $("video", c);
      if (v && FINE && !RM) {
        c.addEventListener("pointerenter", function () {
          if (!v.src && v.dataset.src) { v.src = v.dataset.src; v.addEventListener("loadeddata", function () { v.classList.add("is-ready"); }, { once: true }); }
          v.play().catch(function () {});
        });
        c.addEventListener("pointerleave", function () { v.pause(); });
      }
      if (!media || !FINE || RM) return;
      c.addEventListener("pointermove", function (e) {
        var r = media.getBoundingClientRect(), px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5;
        media.style.transform = "perspective(900px) rotateY(" + px * 7 + "deg) rotateX(" + -py * 7 + "deg)";
      });
      c.addEventListener("pointerleave", function () { media.style.transform = ""; });
    });
    if (!hasGSAP || RM) return;
    $$(".card__media img").forEach(function (im) {
      gsap.fromTo(im, { yPercent: -6, scale: 1.12 }, { yPercent: 6, scale: 1.12, ease: "none", scrollTrigger: { trigger: im.parentNode, start: "top bottom", end: "bottom top", scrub: true } });
    });
  }

  /* ---------- proceso horizontal (pin en desktop) ---------- */
  function initProcess() {
    var pin = $(".process__pin"), tr = $(".process__track"); if (!pin || !tr || !hasGSAP || RM) return;
    var mm = gsap.matchMedia();
    mm.add("(min-width: 901px)", function () {
      var dist = function () { return tr.scrollWidth - window.innerWidth; };
      var tw = gsap.to(tr, { x: function () { return -dist(); }, ease: "none",
        scrollTrigger: { trigger: ".process", start: "top top", end: function () { return "+=" + dist(); }, pin: true, scrub: 1, invalidateOnRefresh: true, anticipatePin: 1 } });
      gsap.to(".process__bar i", { scaleX: 1, ease: "none", scrollTrigger: { trigger: ".process", start: "top top", end: function () { return "+=" + dist(); }, scrub: true } });
      return function () { tw.scrollTrigger && tw.scrollTrigger.kill(); };
    });
  }

  /* ---------- contadores ---------- */
  function initCounters() {
    $$("[data-count]").forEach(function (el) {
      var end = parseFloat(el.dataset.count);
      if (!hasGSAP || RM) { el.textContent = end; return; }
      var o = { v: 0 };
      gsap.to(o, { v: end, duration: 2, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 88%", once: true },
        onUpdate: function () { el.textContent = Math.round(o.v); } });
    });
  }

  /* ---------- botones magnéticos ---------- */
  function initMagnetic() {
    if (!FINE || RM || !hasGSAP) return;
    $$("[data-magnetic]").forEach(function (b) {
      var xTo = gsap.quickTo(b, "x", { duration: .5, ease: "power3" }), yTo = gsap.quickTo(b, "y", { duration: .5, ease: "power3" });
      b.addEventListener("pointermove", function (e) { var r = b.getBoundingClientRect(); xTo((e.clientX - r.left - r.width / 2) * .3); yTo((e.clientY - r.top - r.height / 2) * .4); });
      b.addEventListener("pointerleave", function () { xTo(0); yTo(0); });
    });
  }

  /* ---------- CTA gigante ---------- */
  function initCTA() {
    var big = $(".cta__big"); if (!big || !hasGSAP || RM) return;
    gsap.from($$("span", big), { yPercent: 100, opacity: 0, duration: 1.2, ease: "expo.out", stagger: .12, scrollTrigger: { trigger: big, start: "top 85%", once: true } });
  }

  /* ---------- tilt en pilares (studio) ---------- */
  function initTilt() {
    if (!FINE || RM) return;
    $$("[data-tilt]").forEach(function (el) {
      el.addEventListener("pointermove", function (e) { var r = el.getBoundingClientRect(), px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5; el.style.transform = "perspective(800px) rotateY(" + px * 10 + "deg) rotateX(" + -py * 10 + "deg)"; });
      el.addEventListener("pointerleave", function () { el.style.transform = ""; });
    });
  }

  /* ---------- filtros de proyectos ---------- */
  function initFilters() {
    var chips = $$(".filters .chip"); if (!chips.length) return;
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        var f = c.dataset.filter;
        chips.forEach(function (o) { o.setAttribute("aria-pressed", o === c ? "true" : "false"); });
        $$(".work-list .card").forEach(function (card) {
          var show = f === "all" || (card.dataset.cat || "").split(" ").indexOf(f) > -1;
          card.classList.toggle("is-hidden", !show);
        });
        hasGSAP && ScrollTrigger.refresh();
      });
    });
  }

  function initYear() { $$("[data-year]").forEach(function (e) { e.textContent = new Date().getFullYear(); }); }

  function boot() {
    safe("lenis", initLenis);
    safe("header", initHeader);
    safe("menu", initMenu);
    safe("cursor", initCursor);
    safe("heroIntro", initHeroIntro);
    safe("heroVideo", initHeroVideo);
    safe("split", initSplit);
    safe("reveal", initReveal);
    safe("manifesto", initManifesto);
    safe("reel", initReel);
    safe("svcFloat", initSvcFloat);
    safe("marquee", initMarquee);
    safe("masterplan", initMasterplan);
    safe("chat", initChat);
    safe("cards", initCards);
    safe("projectsReel", initProjectsReel);
    safe("process", initProcess);
    safe("counters", initCounters);
    safe("magnetic", initMagnetic);
    safe("cta", initCTA);
    safe("tilt", initTilt);
    safe("filters", initFilters);
    safe("year", initYear);
    if (hasGSAP) {
      window.addEventListener("load", function () { ScrollTrigger.refresh(); });
      document.fonts && document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
