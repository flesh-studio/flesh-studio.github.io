/* Flesh Studio — formulario de presupuesto (sin backend: arma el mensaje para WhatsApp o email) */
(function () {
  "use strict";
  var form = document.getElementById("qform"); if (!form) return;
  var WA = "5492944152161", MAIL = "contacto.flesh@gmail.com";
  var ok = form.querySelector(".form-ok");
  var group = document.getElementById("c-servicio");
  // anti-spam: campo trampa, tiempo mínimo de llenado y pausa entre envíos
  var T0 = Date.now(), lastSend = 0;
  function looksLikeBot() {
    var hp = form.elements.web2;
    if (hp && hp.value) return true;
    if (Date.now() - T0 < 4000) return true;
    return false;
  }
  function tooSoon() { return Date.now() - lastSend < 15000; }

  // preselección desde ?servicio=
  try {
    var q = new URLSearchParams(location.search).get("servicio");
    if (q) { var el = form.querySelector('input[name="servicio"][value="' + q.replace(/[^a-z]/g, "") + '"]'); if (el) el.checked = true; }
  } catch (e) {}

  // elección hecha en Servicios: ?formato=Web Pro  ó  ?solucion=hotel
  var formato = "", solucion = "";
  var SOL = {
    hotel: { label: "Hotel / cabañas", svcs: ["branding", "audiovisual", "web", "ia"], rubro: "Turismo / hotelería" },
    restaurante: { label: "Restaurante", svcs: ["marketing", "audiovisual", "web", "ia"], rubro: "Gastronomía" },
    inmobiliaria: { label: "Inmobiliaria / desarrollo", svcs: ["audiovisual", "masterplan", "web", "ia"], rubro: "Real estate / desarrollo" }
  };
  function pick(v) { var i = form.querySelector('input[name="servicio"][value="' + v + '"]'); if (i) i.checked = true; }
  function banner(kind, name, clear) {
    var tag = document.createElement("p"); tag.className = "q-formato";
    tag.innerHTML = kind + ': <b></b> <button type="button">Quitar</button>';
    tag.querySelector("b").textContent = name;
    tag.querySelector("button").setAttribute("aria-label", "Quitar " + kind.toLowerCase());
    tag.querySelector("button").addEventListener("click", function () { clear(); tag.remove(); });
    group.parentNode.insertBefore(tag, group);
  }
  try {
    var qs = new URLSearchParams(location.search), f = qs.get("formato") || "", sk = qs.get("solucion") || "", s = Object.prototype.hasOwnProperty.call(SOL, sk) ? SOL[sk] : null;
    if (group && ["Web Start", "Web Pro", "Web Business", "Web Experience"].indexOf(f) > -1) {
      formato = f; pick("web"); banner("Formato elegido", f, function () { formato = ""; });
    }
    if (group && s) {
      solucion = s.label; s.svcs.forEach(pick);
      var rb = form.elements.rubro; if (rb && !rb.value) rb.value = s.rubro;
      banner("Solución elegida", s.label, function () { solucion = ""; });
    }
  } catch (e) {}

  function fieldOf(input) { return input.closest(".field"); }
  function validate() {
    var first = null, valid = true;
    ["nombre", "email", "tel", "detalle"].forEach(function (n) {
      var i = form.elements[n], f = fieldOf(i), v = i.value.trim(), bad = !v;
      if (n === "email" && v) bad = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
      if (n === "tel" && v) bad = v.replace(/\D/g, "").length < 7;
      f.classList.toggle("has-error", bad); i.setAttribute("aria-invalid", bad ? "true" : "false");
      if (bad) { valid = false; first = first || i; }
    });
    var anyS = form.querySelectorAll('input[name="servicio"]:checked').length > 0;
    group.classList.toggle("has-error", !anyS);
    if (!anyS) { valid = false; first = first || group.querySelector("input"); }
    if (first) first.focus();
    return valid;
  }
  form.addEventListener("input", function (e) {
    var f = e.target.closest(".field"); if (f && f.classList.contains("has-error")) { f.classList.remove("has-error"); e.target.setAttribute("aria-invalid", "false"); }
    if (e.target.name === "servicio") group.classList.remove("has-error");
  });

  function message() {
    var d = form.elements;
    var svcs = Array.prototype.map.call(form.querySelectorAll('input[name="servicio"]:checked'), function (i) { return i.dataset.label; }).join(", ");
    var plazo = (form.querySelector('input[name="plazo"]:checked') || {}).value || "";
    var lines = [
      "Hola Flesh Studio! Quiero pedir una propuesta.",
      "",
      "• Nombre / empresa: " + d.nombre.value.trim(),
      "• Email: " + d.email.value.trim(),
      "• WhatsApp: " + d.tel.value.trim()
    ];
    if (d.ciudad.value.trim()) lines.push("• Ciudad: " + d.ciudad.value.trim());
    lines.push("• Servicios: " + svcs);
    if (formato) lines.push("• Formato web: " + formato);
    if (solucion) lines.push("• Solución integral: " + solucion);
    if (d.rubro.value) lines.push("• Rubro: " + d.rubro.value);
    if (d.ref.value.trim()) lines.push("• Web / IG: " + d.ref.value.trim());
    if (d.prioridades && d.prioridades.value) {
      var cap = function (k) { return k.charAt(0).toUpperCase() + k.slice(1); };
      lines.push("• Prioridades: " + d.prioridades.value.split(",").map(cap).join(" + ") + (d.descartado.value ? " (no es " + d.descartado.value + ")" : ""));
    }
    if (plazo) lines.push("• Plazo: " + plazo);
    lines.push("", "Proyecto:", d.detalle.value.trim());
    return lines.join("\n");
  }
  function done(channel, href) {
    ok.textContent = "¡Listo! Abrimos " + channel + " con tu solicitud. Si no se abrió, ";
    var a = document.createElement("a"); a.href = href; a.target = "_blank"; a.rel = "noopener noreferrer"; a.textContent = "hacé clic acá";
    ok.appendChild(a); ok.appendChild(document.createTextNode("."));
    ok.classList.add("is-on");
  }
  function guard() {
    if (looksLikeBot()) { ok.textContent = "Revisá los datos y volvé a intentar en unos segundos."; ok.classList.add("is-on"); return false; }
    if (tooSoon()) { ok.textContent = "Ya enviaste tu solicitud. Esperá unos segundos antes de reenviarla."; ok.classList.add("is-on"); return false; }
    lastSend = Date.now(); return true;
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault(); if (!validate() || !guard()) return;
    var href = "https://wa.me/" + WA + "?text=" + encodeURIComponent(message());
    window.open(href, "_blank", "noopener,noreferrer"); done("WhatsApp", href);
  });
  document.getElementById("send-mail").addEventListener("click", function () {
    if (!validate() || !guard()) return;
    var href = "mailto:" + MAIL + "?subject=" + encodeURIComponent("Solicitud de propuesta — " + form.elements.nombre.value.trim()) + "&body=" + encodeURIComponent(message());
    location.href = href; done("tu email", href);
  });
})();
