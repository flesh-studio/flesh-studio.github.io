/* Flesh Studio — prioridades "bueno, bonito, barato": se eligen dos y la tercera queda cortada */
(function () {
  "use strict";
  var REDUCED = document.documentElement.classList.contains("rm") ||
    (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  var GLYPHS = "▓▒░#/\\<>01";
  var KEYS = ["bueno", "bonito", "barato"];
  var NOMBRE = { bueno: "Bueno", bonito: "Bonito", barato: "Barato" };
  // la clave es la opción que queda afuera
  var FRASES = {
    barato: { tag: "No es barato", text: "Lo bueno y lindo lleva tiempo, talento y cuidado. Es una inversión, y se nota." },
    bonito: { tag: "No es bonito", text: "Funciona, cumple y no rompe el bolsillo. Eso sí: no va a ganar ningún premio de diseño." },
    bueno:  { tag: "No es bueno",  text: "Se ve increíble en la foto. Después… que sea lo que tenga que ser." }
  };
  var VACIO = { tag: "", text: "Elegí dos. El tercero se va solo." };
  var UNO = { tag: "", text: "Bien. Ahora elegí uno más." };

  document.querySelectorAll("[data-bbb]").forEach(function (root) {
    var rows = Array.prototype.slice.call(root.querySelectorAll(".bbb__row"));
    var tag = root.querySelector(".bbb__tag"), text = root.querySelector(".bbb__text");
    var pips = root.querySelectorAll(".bbb__pip"), num = root.querySelector(".bbb__num");
    var track = root.querySelector(".bbb__ticker-track");
    var inPri = root.querySelector('input[name="prioridades"]'), inDesc = root.querySelector('input[name="descartado"]');
    var order = [], lastMsg = null, lastOff = null, raf = 0;

    function scramble(el, target) {
      cancelAnimationFrame(raf);
      if (REDUCED) { el.textContent = target; return; }
      var start = performance.now(), dur = Math.min(650, 240 + target.length * 6);
      (function step(now) {
        var p = Math.min(1, (now - start) / dur), cut = Math.floor(target.length * p), out = target.slice(0, cut);
        for (var i = cut; i < Math.min(target.length, cut + 10); i++) out += target[i] === " " ? " " : GLYPHS[(Math.random() * GLYPHS.length) | 0];
        el.textContent = out;
        if (p < 1) raf = requestAnimationFrame(step);
      })(start);
    }
    function setMsg(m) {
      if (lastMsg === m) return;
      lastMsg = m;
      tag.textContent = m.tag ? "✕ " + m.tag : "";
      scramble(text, m.text);
    }
    function setTicker(off) {
      var line;
      if (off) line = ["Elegiste " + order.map(function (k) { return NOMBRE[k]; }).join(" + "), "No es " + NOMBRE[off].toLowerCase(), "Flesh Studio"];
      else if (order.length === 1) line = [NOMBRE[order[0]] + " cargado", "Falta uno", "Flesh Studio"];
      else line = ["Elegí dos", "El tercero se va solo", "Flesh Studio"];
      var html = line.map(function (s) { return "<span>" + s + "</span><span>⚡</span>"; }).join("");
      track.innerHTML = html + html + html + html;
    }
    function render(popKey) {
      var off = order.length === 2 ? KEYS.filter(function (k) { return order.indexOf(k) < 0; })[0] : null;
      rows.forEach(function (r) {
        var k = r.dataset.k, on = order.indexOf(k) > -1;
        r.classList.toggle("is-on", on);
        r.classList.toggle("is-off", k === off);
        r.classList.remove("is-pop");
        if (k === popKey && on && !REDUCED) { void r.offsetWidth; r.classList.add("is-pop"); }
        r.querySelector(".bbb__state b").textContent = on ? "On" : k === off ? "Cortado" : "—";
        r.setAttribute("aria-pressed", on ? "true" : "false");
      });
      pips.forEach(function (p, i) { p.classList.toggle("is-on", i < order.length); });
      num.textContent = order.length + "/2";
      if (off && off !== lastOff && !REDUCED) { root.classList.remove("is-flash"); void root.offsetWidth; root.classList.add("is-flash"); }
      lastOff = off;
      setMsg(off ? FRASES[off] : order.length === 1 ? UNO : VACIO);
      setTicker(off);
      inPri.value = order.join(",");
      inDesc.value = off || "";
      root.dispatchEvent(new CustomEvent("bbb:change", { bubbles: true, detail: { elegidos: order.slice(), descartado: off } }));
    }
    rows.forEach(function (r) {
      r.addEventListener("click", function () {
        var k = r.dataset.k, i = order.indexOf(k), pop = null;
        if (i > -1) order.splice(i, 1);
        else { order.push(k); if (order.length > 2) order.shift(); pop = k; }
        render(pop);
      });
    });
    render();
  });
})();
