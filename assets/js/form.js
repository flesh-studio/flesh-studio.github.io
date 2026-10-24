/* Flesh Studio — formulario de presupuesto (sin backend: arma el mensaje para WhatsApp o email) */
(function () {
  "use strict";
  var form = document.getElementById("qform"); if (!form) return;
  var WA = "5492944152161", MAIL = "contacto.flesh@gmail.com";
  var ok = form.querySelector(".form-ok");
  var group = document.getElementById("c-servicio");

  // preselección desde ?servicio=
  try {
    var q = new URLSearchParams(location.search).get("servicio");
    if (q) { var el = form.querySelector('input[name="servicio"][value="' + q.replace(/[^a-z]/g, "") + '"]'); if (el) el.checked = true; }
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
    if (d.rubro.value) lines.push("• Rubro: " + d.rubro.value);
    if (d.ref.value.trim()) lines.push("• Web / IG: " + d.ref.value.trim());
    if (plazo) lines.push("• Plazo: " + plazo);
    lines.push("", "Proyecto:", d.detalle.value.trim());
    return lines.join("\n");
  }
  function done(channel, href) {
    ok.innerHTML = "¡Listo! Abrimos " + channel + " con tu solicitud. Si no se abrió, <a href=\"" + href + "\" target=\"_blank\" rel=\"noopener\">hacé clic acá</a>.";
    ok.classList.add("is-on");
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault(); if (!validate()) return;
    var href = "https://wa.me/" + WA + "?text=" + encodeURIComponent(message());
    window.open(href, "_blank", "noopener"); done("WhatsApp", href);
  });
  document.getElementById("send-mail").addEventListener("click", function () {
    if (!validate()) return;
    var href = "mailto:" + MAIL + "?subject=" + encodeURIComponent("Solicitud de propuesta — " + form.elements.nombre.value.trim()) + "&body=" + encodeURIComponent(message());
    location.href = href; done("tu email", href);
  });
})();
