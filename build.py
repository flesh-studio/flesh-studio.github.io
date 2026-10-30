# -*- coding: utf-8 -*-
"""Genera las páginas del sitio de Flesh Studio con header/footer compartidos."""
import json, os, random, hashlib, base64

OUT = os.environ.get("OUT", "/home/claude/site")
BASE_URL = os.environ.get("BASE_URL", "https://flesh-studio.com/")
WA_NUM = "5492944152161"
WA_TXT = "Hola%20Flesh%20Studio%2C%20quiero%20hablar%20sobre%20un%20proyecto"
WA = f"https://wa.me/{WA_NUM}?text={WA_TXT}"
MAIL = "contacto.flesh@gmail.com"
IG = "https://instagram.com/flesh_studio"

BOLT_D = "M38 0H78L58 62H86L28 160L44 86H16Z"
def bolt(cls, label=None):
    a = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    return (f'<svg class="bolt {cls}" viewBox="-4 -4 150 180" {a}>'
            f'<path transform="translate(40 0)" d="{BOLT_D}"/>'
            f'<path transform="translate(20 5)" d="{BOLT_D}"/>'
            f'<path transform="translate(0 10)" d="{BOLT_D}"/></svg>')

ARROW = '<svg class="icon arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ARROW_UR = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'
WA_ICON = '<svg class="icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5.1 5.2-1.4A9.9 9.9 0 1 0 12.04 2Zm0 18.1c-1.5 0-3-.4-4.3-1.2l-.3-.2-3.1.8.8-3-.2-.3a8.2 8.2 0 1 1 7.1 3.9Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>'
IG_ICON = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor"/></svg>'
CHECK = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m5 12 4.5 4.5L19 7"/></svg>'

SHOW_PROYECTOS = False   # página Proyectos oculta hasta cargar todo el material (True = visible)
NAV = [("index.html", "Inicio"), ("proyectos.html", "Proyectos"), ("studio.html", "Studio"),
       ("servicios.html", "Servicios"), ("presupuesto.html", "Presupuesto")]
if not SHOW_PROYECTOS:
    NAV = [x for x in NAV if x[0] != "proyectos.html"]

NOJS = '(function(d){d.className=d.className.replace("no-js","js");if(window.matchMedia("(prefers-reduced-motion: reduce)").matches)d.className+=" rm";})(document.documentElement);'
NOJS_HASH = "sha256-" + base64.b64encode(hashlib.sha256(NOJS.encode()).digest()).decode()
# Política de contenido: solo recursos propios; el único script inline permitido es NOJS (por hash).
CSP = ("default-src 'self'; script-src 'self' '" + NOJS_HASH + "'; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data: blob:; media-src 'self' blob:; font-src 'self'; connect-src 'self'; "
       "object-src 'none'; base-uri 'self'; form-action 'self'; frame-src 'none'; worker-src 'self' blob:; "
       "manifest-src 'self'; upgrade-insecure-requests")

def head(title, desc, path, extra=""):
    url = BASE_URL + ("" if path == "index.html" else path)
    return f'''<!doctype html>
<html lang="es" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B0B0C">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="Flesh Studio">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}assets/img/og-image.jpg">
<meta property="og:image:width" content="630">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE_URL}assets/img/og-image.jpg">
<link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
<link rel="apple-touch-icon" href="assets/img/favicon-180.png">
<script>{NOJS}</script>
<link rel="preload" href="assets/fonts/unbounded-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-tight-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/styles.css">
{extra}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
'''

def header(active):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == active else ""}>{t}</a>' for h, t in NAV)
    mlinks = "".join(f'<a href="{h}"{cur if h == active else ""}><small>0{i+1}</small>{t}</a>' for i, (h, t) in enumerate(NAV))
    return f'''<header class="header">
  <div class="wrap header__in">
    <a class="brand" href="index.html" aria-label="Flesh Studio — inicio">{bolt("brand__mark")}<span>FLESH STUDIO</span></a>
    <nav class="nav" aria-label="Principal">{links}</nav>
    <div class="header__cta">
      <div class="socials"><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram de Flesh Studio">{IG_ICON}</a><a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp de Flesh Studio">{WA_ICON}</a></div>
      <a class="btn" href="presupuesto.html" data-magnetic>Pedir propuesta {ARROW}</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Abrir menú"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
  <nav aria-label="Menú móvil">{mlinks}</nav>
  <div class="mobile-menu__foot">
    <a href="{WA}" target="_blank" rel="noopener">WhatsApp · +54 9 2944 15-2161</a>
    <a href="mailto:{MAIL}">{MAIL}</a>
    <a href="{IG}" target="_blank" rel="noopener">@flesh_studio</a>
  </div>
</div>
'''

def cta_block():
    return f'''<section class="cta" aria-labelledby="cta-t">
  <div class="wrap">
    <p class="kicker" style="justify-content:center">Hablemos</p>
    <h2 id="cta-t" class="sr-only">¿Tenés un proyecto? Hablemos</h2>
    <p class="cta__big" aria-hidden="true"><span>¿Tenés un</span><br><span class="o">proyecto?</span></p>
    <p>Contanos qué querés lograr. Te armamos una propuesta clara, con alcance, tiempos y el formato que mejor le sirve a tu negocio.</p>
    <div class="cta__btns">
      <a class="btn" href="presupuesto.html" data-magnetic>Solicitar propuesta {ARROW}</a>
      <a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener">{WA_ICON} Escribir por WhatsApp</a>
    </div>
    <a class="cta__mail" href="mailto:{MAIL}">{MAIL}</a>
  </div>
</section>
'''

def footer(scripts=""):
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="brand" href="index.html" aria-label="Flesh Studio — inicio">{bolt("brand__mark")}<span>FLESH STUDIO</span></a>
        <p>Agencia de marketing, agentes IA y producción audiovisual para marcas que quieren vender más.</p>
      </div>
      <div><h4>Sitio</h4><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}</ul></div>
      <div><h4>Servicios</h4><ul>
        <li><a href="servicios.html#marketing">Marketing</a></li>
        <li><a href="servicios.html#agentes-ia">Agentes IA</a></li>
        <li><a href="servicios.html#audiovisual">Audiovisual</a></li>
        <li><a href="servicios.html#diseno-web">Diseño web</a></li>
        <li><a href="servicios.html#masterplan-360">Masterplan & 360°</a></li>
        <li><a href="servicios.html#branding">Branding</a></li></ul></div>
      <div><h4>Contacto</h4><ul>
        <li><a href="{WA}" target="_blank" rel="noopener">+54 9 2944 15-2161</a></li>
        <li><a href="mailto:{MAIL}">{MAIL}</a></li>
        <li><a href="{IG}" target="_blank" rel="noopener">@flesh_studio</a></li>
        <li>PATAGONIA — ARG — WORLDWIDE</li></ul></div>
    </div>
    <div class="footer__bottom"><span>© <span data-year>2026</span> Flesh Studio</span><span>Hecho en la Patagonia · con energía</span></div>
  </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Escribinos por WhatsApp">{WA_ICON}</a>
<script src="assets/vendor/gsap.min.js" defer></script>
<script src="assets/vendor/ScrollTrigger.min.js" defer></script>
<script src="assets/vendor/lenis.min.js" defer></script>
<script src="assets/js/main.js" defer></script>
{scripts}
</body>
</html>
'''

def marquee_big():
    item = (f'<div class="marquee__item"><span>Marketing</span>{bolt("")}<span class="o">IA</span>{bolt("")}'
            f'<span>Video</span>{bolt("")}<span class="o">Reels</span>{bolt("")}<span>Drone</span>{bolt("")}'
            f'<span class="o">Contenido</span>{bolt("")}</div>')
    hidden = item.replace('<div class="marquee__item">', '<div class="marquee__item" aria-hidden="true">')
    return (f'<div class="marquee" data-speed="30" role="img" aria-label="Marketing, IA, Video, Reels, Drone, Contenido">'
            f'<div class="marquee__track" aria-hidden="true">{item}{hidden}</div></div>')

SECTORS = ["Real estate & desarrollos", "Turismo & hotelería", "Gastronomía", "Construcción",
           "Marcas personales", "Startups & branding"]
def marquee_small():
    it = "".join(f"<span>{s}</span><i></i>" for s in SECTORS)
    item = f'<div class="marquee__item">{it}</div>'
    return (f'<div class="marquee marquee--small" data-dir="right" data-speed="40">'
            f'<p class="sr-only">Sectores: {", ".join(SECTORS)}</p>'
            f'<div class="marquee__track" aria-hidden="true">{item}{item}</div></div>')

IA_USES = ["Hoteles & cabañas", "Reservas 24/7", "Inmobiliarias", "Calificación de leads", "Restaurantes",
           "Turnos automáticos", "Clínicas & consultorios", "Atención por WhatsApp", "E-commerce",
           "Seguimiento de ventas", "Agencias de turismo", "Respuestas al instante", "Gimnasios & estética",
           "Derivación al equipo"]
def marquee_ia():
    it = "".join(f"<span>{s}</span><i></i>" for s in IA_USES)
    item = f'<div class="marquee__item">{it}</div>'
    return (f'<div class="marquee marquee--small" data-dir="left" data-speed="46">'
            f'<p class="sr-only">Rubros y tareas para agentes IA: {", ".join(IA_USES)}</p>'
            f'<div class="marquee__track" aria-hidden="true">{item}{item}</div></div>')

# Demo de agentes IA: conversaciones de ejemplo (out = cliente, in = agente IA, sys = aviso)
WA_CHATS = [
    dict(tab="Turismo", name="Cabañas del Lago", ini="CL", color="#0e7c66", time="21:14", msgs=[
        ("out", "Hola! ¿Tienen lugar para 4 personas del 12 al 15 de enero?"),
        ("in", "¡Hola! 👋 Sí, para esas fechas está libre la Cabaña Bosque: vista al lago, parrilla y 2 habitaciones."),
        ("out", "¿Aceptan mascotas?"),
        ("in", "Sí, mascotas pequeñas sin costo extra 🐶 ¿Te la reservo y te mando el link para pagar la seña?"),
        ("out", "Dale, reservá!"),
        ("sys", "✓ Reserva pre-confirmada · lead enviado al equipo")]),
    dict(tab="Real estate", name="Lotes Río Rual", ini="RR", color="#8a5a2b", time="10:02", msgs=[
        ("out", "Hola, vi el anuncio de los lotes. ¿Qué medidas tienen?"),
        ("in", "¡Hola! Hay lotes desde 1.000 m², con servicios y acceso pavimentado. ¿Lo buscás para vivir o como inversión?"),
        ("out", "Para construir mi casa. ¿Tienen financiación?"),
        ("in", "Sí, con anticipo y cuotas. ¿Querés visitar el loteo este sábado? Tengo lugar a las 10:30 o a las 16:00."),
        ("out", "Sábado 10:30 perfecto"),
        ("sys", "✓ Visita agendada · lead calificado en el CRM")]),
    dict(tab="Gastronomía", name="Fuego Patagónico", ini="FP", color="#b8432a", time="18:47", msgs=[
        ("out", "Hola! ¿Tienen mesa para 6 hoy a la noche?"),
        ("in", "¡Hola! Sí, a las 21:30 tengo una mesa junto a la ventana para 6 🔥 ¿Te la reservo?"),
        ("out", "Sí! Una persona es celíaca, ¿hay opciones?"),
        ("in", "Claro, tenemos menú sin TACC y le avisamos a cocina. ¿A nombre de quién la dejo?"),
        ("out", "Martina"),
        ("sys", "✓ Mesa reservada · 21:30 · 6 personas")]),
    dict(tab="Estética", name="Estética Aura", ini="EA", color="#7a4fa3", time="09:31", msgs=[
        ("out", "Hola, quería un turno para limpieza facial"),
        ("in", "¡Hola! Tengo turnos el jueves a las 11:00 o el viernes a las 17:30. ¿Cuál te queda mejor?"),
        ("out", "Viernes 17:30"),
        ("in", "¡Listo! Te lo agendo y el día anterior te mando un recordatorio por acá 😊"),
        ("sys", "✓ Turno confirmado · recordatorio automático")]),
    dict(tab="E-commerce", name="Tienda Andina", ini="TA", color="#2b6cb0", time="23:08", msgs=[
        ("out", "Hola! ¿La campera negra está en talle M?"),
        ("in", "¡Hola! Sí, queda stock en M 🙌 ¿A qué ciudad te la enviamos?"),
        ("out", "A Rosario"),
        ("in", "Llega en 3 a 5 días hábiles. Te paso el link de pago así te la reservo ahora."),
        ("out", "Genial, gracias!"),
        ("sys", "✓ Link de pago enviado · venta cerrada por el agente")]),
]

WA_TICK = '<svg class="wa-tick" viewBox="0 0 16 11" aria-hidden="true"><path d="M11.07.65 4.98 7.9 2.4 5.4 1.3 6.5l3.74 3.6 7.13-8.5zM14.6.65 8.5 7.9l-.88-.86-1.1 1.13 2.03 1.96 7.13-8.5z" fill="currentColor"/></svg>'

def _wa_time(t, add):
    h, m = map(int, t.split(":")); m = h * 60 + m + add
    return f"{(m // 60) % 24:02d}:{m % 60:02d}"

def _wa_msgs(c):
    out, prev = [], None
    for i, (k, t) in enumerate(c["msgs"]):
        if k == "sys":
            out.append(f'<div class="wa-sys">{t}</div>'); prev = None; continue
        cont = " cont" if prev == k else ""
        tick = WA_TICK if k == "out" else ""
        out.append(f'<div class="wa-msg {k}{cont}">{t}<em>{_wa_time(c["time"], i)}{tick}</em></div>'); prev = k
    return "".join(out)

def wa_demo():
    c = WA_CHATS[0]
    data = json.dumps([dict(name=x["name"], ini=x["ini"], color=x["color"], time=x["time"], msgs=x["msgs"]) for x in WA_CHATS], ensure_ascii=False).replace("</", "<\\/")
    tabs = "".join(f'<button type="button" class="wa-tab" aria-pressed="{"true" if i == 0 else "false"}">{x["tab"]}</button>' for i, x in enumerate(WA_CHATS))
    ic = lambda d, vb="0 0 24 24": f'<svg viewBox="{vb}" aria-hidden="true">{d}</svg>'
    return f'''<div class="wa-demo">
      <p class="sr-only">Demo animada: conversaciones de ejemplo por WhatsApp entre clientes y agentes IA de turismo, real estate, gastronomía, estética y e-commerce.</p>
      <div class="iph" aria-hidden="true">
        <i class="iph__btn iph__btn--act"></i><i class="iph__btn iph__btn--vu"></i><i class="iph__btn iph__btn--vd"></i><i class="iph__btn iph__btn--pw"></i><i class="iph__btn iph__btn--cam"></i>
        <div class="iph__screen">
          <div class="iph__island"></div>
          <div class="iph__status"><span class="iph__time">{c["time"]}</span><span class="iph__icons">{ic('<path d="M2 17h3v4H2zM7 13h3v8H7zM12 9h3v12h-3zM17 5h3v16h-3z" fill="currentColor"/>')}{ic('<path d="M12 18.5 9.6 16a3.4 3.4 0 0 1 4.8 0zm-4.6-4.7-1.8-1.8a9 9 0 0 1 12.8 0l-1.8 1.8a6.4 6.4 0 0 0-9.2 0zM3.2 9.6 1.4 7.8a15 15 0 0 1 21.2 0l-1.8 1.8a12.4 12.4 0 0 0-17.6 0z" fill="currentColor"/>')}<b class="iph__bat"><i></i></b></span></div>
          <div class="wa-head">
            {ic('<path d="M15 5 8 12l7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')}
            <span class="wa-av" style="background:{c["color"]}">{c["ini"]}</span>
            <span class="wa-who"><b class="wa-name">{c["name"]}</b><small class="wa-status">en línea</small></span>
            <span class="wa-acts">{ic('<path d="M3 7.5A1.5 1.5 0 0 1 4.5 6h9A1.5 1.5 0 0 1 15 7.5v9a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 3 16.5zM16 10l5-3v10l-5-3z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>')}{ic('<path d="M6.6 3.5 9 3l1.6 4-2 1.4a10 10 0 0 0 5 5l1.4-2 4 1.6-.5 2.4a2 2 0 0 1-2 1.6A15 15 0 0 1 5 5.5a2 2 0 0 1 1.6-2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>')}</span>
          </div>
          <div class="wa-body"><span class="wa-day">Hoy</span>{_wa_msgs(c)}</div>
          <div class="wa-input">
            <span class="wa-field">{ic('<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M8.5 14.5a4.5 4.5 0 0 0 7 0" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><circle cx="9" cy="10" r="1.2" fill="currentColor"/><circle cx="15" cy="10" r="1.2" fill="currentColor"/>')}<span class="wa-text"></span>{ic('<path d="m16 7-7.5 7.5a2.1 2.1 0 0 0 3 3L19 10a4 4 0 0 0-5.7-5.7l-7.6 7.6a6 6 0 0 0 8.5 8.5L20 14.6" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>')}</span>
            <span class="wa-mic">{ic('<path d="M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3zM6 11a6 6 0 0 0 12 0M12 17v4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>')}</span>
          </div>
          <div class="iph__home"></div>
        </div>
      </div>
      <div class="wa-tabs" role="group" aria-label="Elegí un rubro">{tabs}</div>
      <p class="demo-note">Demo ilustrativa · conversaciones de ejemplo</p>
      <script type="application/json" id="wa-data">{data}</script>
    </div>'''

# ---------------------------------------------------------------- data
SERVICES = [
    ("marketing", "Marketing", "Estrategia · redes sociales · campañas y pauta · copywriting de conversión", "work-petunia.webp"),
    ("agentes-ia", "Agentes IA", "Atención 24/7 · WhatsApp & CRM · calificación de leads · reservas y turnos", "reel-poster.jpg"),
    ("audiovisual", "Contenido audiovisual", "Video 4K · drone 4K · reels · fotografía · postproducción", "work-petunia-2.webp"),
]
SERVICES_MORE = [("diseno-web", "Diseño web"), ("masterplan-360", "Masterplan & 360°"), ("branding", "Branding")]

PROJECTS = [
    dict(slug="petunia", cls="card--lg", cat="turismo web audiovisual", tag="Turismo & hospitalidad",
         title="Petunia · Refugio de Lago", place="Bariloche, Argentina", year="2026",
         desc="Sitio bilingüe con video aéreo de fondo, reservas por WhatsApp y alojamientos explicados en un solo recorrido.",
         img="work-petunia.webp", video="work-puerto.mp4", url="https://flesh-studio.github.io/petunia-bariloche/",
         alt="Fogón grupal frente al lago en Petunia, Bariloche",
         scope="Diseño web · Desarrollo · Edición de video drone · ES/EN"),
    dict(slug="casa", cls="card--md", cat="realestate web", tag="Real estate",
         title="Casa La Cruzada", place="Puerto Varas, Chile", year="2026",
         desc="Landing de venta en verde para Río Rual: renders, planos, escalonamiento de precios y contacto directo.",
         img="work-casa.webp", video="work-casa.mp4", url="https://flesh-studio.github.io/casa-la-cruzada/",
         alt="Render de Casa La Cruzada, casa contemporánea en Puerto Varas",
         scope="Estrategia comercial · Diseño web · Copy de venta"),
]

# Carrusel del home: carpeta assets/proyectos/<slug>/ con portada.webp (+ video.mp4 opcional)
REEL = [
    ("02-casa-la-cruzada", "Renders", "Real estate · Web", "https://flesh-studio.github.io/casa-la-cruzada/", True),
    ("04-patagonia", "Spot publicitario", "Drone · Audiovisual", "", True),
    ("05-produccion", "Producción", "Contenido para redes", "", True),
    ("06-agentes-ia", "Agentes IA", "Automatización", "", True),
    ("07-desarrollo-web", "Desarrollo web", "Diseño · Desarrollo", "", True),
    ("08-masterplan", "Masterplan 360°", "Experiencia interactiva", "", True),
    ("09-interiores", "Interiores", "Real estate · Foto y video", "", True),
    ("10-gastronomia", "Gastronomía", "Audiovisual · Redes", "", True),
]

def reel_card(item, clone=False):
    slug, title, tag, url, vid = item
    href = url or ("proyectos.html" if SHOW_PROYECTOS else "")
    ext = ' target="_blank" rel="noopener"' if url else ""
    hid = (' aria-hidden="true" tabindex="-1"' if href else ' aria-hidden="true"') if clone else ""
    v = (f'<video muted loop playsinline preload="none" data-src="assets/proyectos/{slug}/video.mp4" aria-hidden="true"></video>' if vid else "")
    tag_open, tag_close = (f'<a class="pr-card" href="{href}"{ext}{hid}>', '</a>') if href else (f'<div class="pr-card"{hid}>', '</div>')
    return (tag_open +
            f'<img src="assets/proyectos/{slug}/portada.webp" alt="{"" if clone else title + " — " + tag}" loading="lazy" decoding="async" width="600" height="1030">{v}'
            f'<span class="pr-card__shade" aria-hidden="true"></span>'
            f'<span class="pr-card__info"><small>{tag}</small><b>{title}</b></span>' + tag_close)

def card(p, list_mode=False):
    cls = "card" if list_mode else p["cls"]
    vid = (f'<video muted loop playsinline preload="none" data-src="assets/video/{p["video"]}" aria-hidden="true"></video>'
           if p["video"] else "")
    return f'''<article class="{cls}" data-cat="{p["cat"]}" data-reveal>
  <div class="card__media" data-cursor="view" data-cursor-label="VER">
    <span class="card__tag">{p["tag"]}</span>
    <img src="assets/img/{p["img"]}" alt="{p["alt"]}" loading="lazy" decoding="async" width="1000" height="1250">
    {vid}
  </div>
  <div class="card__body">
    <div>
      <h3><a class="stretch" href="{p["url"]}" target="_blank" rel="noopener">{p["title"]}</a></h3>
      <p>{p["desc"]}</p>
      {f'<p style="font-family:var(--font-mono);font-size:12px;letter-spacing:.06em;margin-top:10px;color:var(--faint)">{p["scope"]}</p>' if list_mode else ''}
      <div class="card__links"><a href="{p["url"]}" target="_blank" rel="noopener">Ver sitio en vivo ↗</a></div>
    </div>
    <span class="card__year">{p["place"]}<br>{p["year"]}</span>
  </div>
</article>'''

def next_card(extra_cls=""):
    return f'''<article class="card {extra_cls}" data-reveal>
  <a class="coming" href="presupuesto.html">
    <div>{bolt("", None).replace('class="bolt "', 'class="bolt" style="width:56px;margin:0 auto 18px;color:var(--orange)"')}
    <h3>Tu proyecto, acá</h3>
    <p style="margin:0 0 18px">El próximo caso puede ser el tuyo. Contanos qué querés lanzar.</p>
    <span class="btn" style="pointer-events:none">Empezar {ARROW}</span></div>
  </a>
</article>'''

# ---------------------------------------------------------------- INDEX
def lots_html():
    random.seed(7)
    states = ["disponible"] * 14 + ["reservado"] * 5 + ["vendido"] * 5
    random.shuffle(states)
    orient = ["Norte", "Noreste", "Oeste", "Este", "Noroeste"]
    out, n = [], 0
    for row in range(5):
        if row == 2:
            out.append('<span class="plan__gap" aria-hidden="true"></span>'); continue
        for col in range(6):
            s = states[n]; n += 1
            m2 = 600 + ((n * 137) % 9) * 100
            m2s = f"{m2:,}".replace(",", ".")
            out.append(f'<button type="button" class="lot" data-s="{s}" data-m2="{m2s}" data-o="{random.choice(orient)}" aria-pressed="false" aria-label="Lote {n}, {s}">{n:02d}</button>')
    return "".join(out)

def index():
    svc_items = "".join(f'''<li class="svc-item"><a href="servicios.html#{sid}"><span class="n">0{i+1}</span><h3>{name}</h3><span class="tags">{tags}</span><span class="go">{ARROW_UR}</span></a></li>'''
                        for i, (sid, name, tags, img) in enumerate(SERVICES))
    svc_more = " ".join(f'<a href="servicios.html#{sid}">{name}</a>' for sid, name in SERVICES_MORE)
    work = "".join(card(p) for p in PROJECTS)
    schema = {
        "@context": "https://schema.org", "@type": "ProfessionalService", "name": "Flesh Studio",
        "description": "Agencia de marketing, agentes de IA y producción audiovisual. También diseño web, contenido 360° y branding.",
        "url": BASE_URL, "image": BASE_URL + "assets/img/og-image.jpg", "email": MAIL, "telephone": "+5492944152161",
        "areaServed": ["Argentina", "Chile"],
        "address": [{"@type": "PostalAddress", "addressLocality": "San Carlos de Bariloche", "addressRegion": "Río Negro", "addressCountry": "AR"},
                    {"@type": "PostalAddress", "addressLocality": "Rosario", "addressRegion": "Santa Fe", "addressCountry": "AR"}],
        "sameAs": [IG],
        "knowsAbout": ["Marketing digital", "Redes sociales", "Agentes de IA", "Automatización de ventas", "Producción audiovisual", "Reels", "Drone", "Diseño web", "Recorridos virtuales 360°", "Branding"]}
    steps = [
        ("Diagnóstico", "Entendemos tu negocio, tu público y qué tiene que pasar para que esto sea un éxito comercial.", ["Rubro", "Público", "Objetivos", "Competencia"]),
        ("Estrategia", "Definimos la propuesta de valor, el recorrido del cliente y la acción que queremos que haga.", ["Propuesta de valor", "Arquitectura", "Conversión"]),
        ("Producción", "Rodaje, edición, contenido para redes, campañas y agentes IA. Todo en casa, con un mismo criterio.", ["Rodaje", "Contenido", "Campañas", "IA"]),
        ("Lanzamiento", "Publicamos, medimos y optimizamos. SEO, analytics y automatizaciones para que siga rindiendo.", ["SEO", "Analytics", "Automatización"]),
    ]
    steps_html = "".join(f'''<article class="step"><span class="step__n" aria-hidden="true">0{i+1}</span><div><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in tags)}</ul></div></article>''' for i, (t, d, tags) in enumerate(steps))
    steps_html += f'''<article class="step" style="background:var(--orange);color:var(--ink);border-color:var(--orange)"><span class="step__n" style="-webkit-text-stroke-color:var(--ink)" aria-hidden="true">→</span><div><h3>¿Arrancamos?</h3><p style="color:rgba(11,11,12,.75)">Primera reunión sin costo para entender tu proyecto y proponerte el camino más directo.</p><a class="btn" style="--bg:var(--ink);--fg:var(--bone);margin-top:22px" href="presupuesto.html">Solicitar propuesta {ARROW}</a></div></article>'''

    body = f'''{header("index.html")}
<main id="main">
<section class="hero hero--reel" aria-labelledby="hero-t">
  <video class="hero__video" muted loop playsinline preload="none" poster="assets/img/hero-poster.jpg" data-src-desktop="assets/video/hero-1080.mp4" data-src-mobile="assets/video/hero-720.mp4" aria-hidden="true"></video>
  <div class="hero__shade" aria-hidden="true"></div>
  <div class="hero__glow" aria-hidden="true"></div>
  <div class="hero__canvas">{bolt("hero__poster")}</div>
  <h1 id="hero-t" class="sr-only">Flesh Studio — agencia de marketing, agentes IA y producción audiovisual</h1>
  <span class="scroll-hint" aria-hidden="true">SCROLL</span>
</section>

<section class="section manifesto" aria-labelledby="man-t">
  <div class="wrap">
    <div class="manifesto__label"><p class="kicker">Flesh Studio <b>/</b> Manifiesto</p><p class="kicker">PATAGONIA — ARG — WORLDWIDE</p></div>
    <h2 id="man-t" class="sr-only">Manifiesto</h2>
    <p class="manifesto__text" data-hi="atrae,responde,enamora" data-mark="resultados a corto plazo">Marketing que atrae, IA que responde y contenido que enamora. Un solo equipo para optimizar tus resultados a corto plazo.</p>
    <div class="manifesto__grid">
      <div data-reveal><span class="num">01 — Marketing</span><h3>Lo que atrae</h3><p>Estrategia, redes y campañas pensadas para atraer a los clientes correctos, no solo likes.</p></div>
      <div data-reveal><span class="num">02 — Agentes IA</span><h3>Lo que responde</h3><p>Asistentes que atienden, califican y reservan por WhatsApp, Instagram y tu web, las 24 horas.</p></div>
      <div data-reveal><span class="num">03 — Audiovisual</span><h3>Lo que enamora</h3><p>Video 4K, drone, reels y fotografía con estética de cine para que tu marca se elija.</p></div>
    </div>
  </div>
</section>

<section class="reel" aria-label="Reel">
  <div class="wrap">
    <div class="reel__frame">
      <video autoplay muted loop playsinline preload="metadata" poster="assets/img/reel-flesh-poster.jpg" aria-label="Video para RP Aberturas en Cerro Bayo">
        <source src="assets/video/reel-flesh.mp4" type="video/mp4">
      </video>
      <div class="reel__overlay">
        <div class="reel__cap"><span>Spot publicitario</span><button class="reel__toggle" type="button" aria-pressed="false"><svg class="icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 5h3v14H7zM14 5h3v14h-3z"/></svg><span>Pausar</span></button></div>
        <p class="reel__big" aria-hidden="true">Energía<br>que se ve</p>
        <div class="reel__cap"><span>Cerro Bayo, La Angostura</span><span>RP Aberturas</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" aria-labelledby="svc-t">
  <div class="wrap">
    <div class="svc__head">
      <div><p class="kicker">Flesh Studio <b>/</b> Qué hacemos</p><h2 id="svc-t" class="h-lg" data-split style="margin-top:18px">Tres motores, <em>un solo equipo.</em></h2></div>
      <p class="lead" data-reveal>Marketing para que te encuentren, IA para que ninguna consulta quede sin respuesta y contenido para que te elijan. Entramos en una etapa puntual o tomamos tu proyecto de punta a punta.</p>
    </div>
    <ul class="svc-list">{svc_items}</ul>
    <p class="svc-more" data-reveal><span>También hacemos</span>{svc_more}</p>
  </div>
</section>

{marquee_big()}

<section class="section mp ai" aria-labelledby="ai-t">
  <div class="wrap mp__grid">
    <div class="mp__copy">
      <p class="kicker">Agentes IA <b>/</b> Ventas 24/7</p>
      <h2 id="ai-t" class="h-lg" data-split style="margin-top:18px">Tu mejor vendedor <em>no duerme.</em></h2>
      <p class="lead" style="margin-top:22px" data-reveal>Un agente entrenado con la información de tu negocio responde al instante por WhatsApp, Instagram o tu web, califica cada consulta y le pasa a tu equipo las que están listas para cerrar.</p>
      <ul data-reveal>
        <li>{CHECK}<span><strong>Respuesta en segundos</strong>Precios, disponibilidad, horarios y preguntas frecuentes, a cualquier hora.</span></li>
        <li>{CHECK}<span><strong>Leads calificados</strong>Pregunta lo que tu equipo necesita saber y ordena cada contacto en tu CRM.</span></li>
        <li>{CHECK}<span><strong>Reservas y turnos</strong>Agenda, confirma y deriva a una persona cuando hace falta.</span></li>
      </ul>
      <div class="mp__ctas" data-reveal>
        <a class="btn" href="presupuesto.html?servicio=ia" data-magnetic>Quiero mi agente IA {ARROW}</a>
        <a class="btn btn--ghost" href="servicios.html#agentes-ia">Cómo funciona</a>
      </div>
    </div>
    {wa_demo()}
  </div>
</section>

{marquee_ia()}

<section class="section" style="padding-bottom:clamp(40px,5vw,70px)" aria-labelledby="work-t">
  <div class="wrap">
    <div class="work__head">
      <div><p class="kicker">Flesh Studio <b>/</b> Trabajo seleccionado</p><h2 id="work-t" class="h-lg" data-split style="margin-top:18px">Proyectos <em>recientes</em></h2></div>
      {f'<a class="btn btn--ghost" href="proyectos.html">Ver todos {ARROW}</a>' if SHOW_PROYECTOS else ""}
    </div>
  </div>
  <div class="pr" role="region" aria-label="Carrusel de proyectos. Pasá el mouse para frenarlo y ver el video.">
    <div class="pr__track">{"".join(reel_card(x) for x in REEL)}{"".join(reel_card(x, True) for x in REEL)}</div>
  </div>
  <p class="wrap pr__hint" aria-hidden="true">Pasá el mouse para frenar y ver el video · Click para abrir</p>
</section>

{marquee_small()}

<section class="section process" aria-labelledby="pr-t" style="padding-top:clamp(40px,6vw,80px)">
  <div class="wrap process__head">
    <div><p class="kicker">Flesh Studio <b>/</b> Cómo trabajamos</p><h2 id="pr-t" class="h-lg" data-split style="margin-top:18px">De la idea <em>al impacto.</em></h2></div>
    <p class="lead" style="max-width:40ch" data-reveal>Un proceso corto y claro. Sabés qué pasa en cada etapa y qué vas a recibir.</p>
  </div>
  <div class="process__pin"><div class="process__track">{steps_html}</div></div>
  <div class="process__bar" aria-hidden="true"><i></i></div>
</section>

{cta_block()}
</main>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
'''
    return (head("Flesh Studio — Agencia de marketing, agentes IA y producción audiovisual",
                 "Agencia de marketing en Bariloche y Rosario: estrategia y redes, agentes IA que atienden y venden 24/7 y contenido audiovisual con drone para marcas que quieren vender más.",
                 "index.html")
            + body + footer('<script src="assets/js/hero3d.bundle.js" defer></script>'))

# ---------------------------------------------------------------- SERVICIOS
SVC_DETAIL = [
    ("masterplan-360", "Masterplan & tours 360°", "Para desarrollos inmobiliarios, loteos, hoteles y destinos turísticos que necesitan mostrar lo que todavía no se puede visitar — o lo que está lejos.",
     ["Masterplan interactivo con lotes, sectores y amenities", "Recorridos virtuales 360° con óptica 8K", "Tomas aéreas con drone 4K integradas", "Disponibilidad y precios conectados a tu CRM", "Visitas narradas y modo realidad virtual", "Métricas de comportamiento con Google Analytics"],
     "masterplan", "work-casa-2.webp", "Render de living de Casa La Cruzada"),
    ("agentes-ia", "Agentes IA & automatización", "Un asistente que conoce tu negocio, responde en segundos y no se toma vacaciones. Pensado como herramienta comercial, no como novedad tecnológica.",
     ["Atención 24/7 en WhatsApp, web e Instagram", "Calificación de leads y derivación al equipo", "Reservas y turnos automáticos", "Integración con CRM y herramientas de gestión", "Memoria y contexto en cada conversación", "Reportes de consultas frecuentes"],
     "ia", None, None),
    ("diseno-web", "Diseño web", "Sitios rápidos, mobile first y construidos alrededor de una acción: reservar, consultar, comprar o pedir presupuesto.",
     ["Landing pages de campaña o lanzamiento", "Sitios corporativos con SEO técnico", "Tiendas online con pagos y envíos", "Webs para turismo con reservas y multidioma", "Formularios, WhatsApp y tracking integrados", "Hosting, dominio y mantenimiento"],
     "web", "work-casa.webp", "Sitio web de Casa La Cruzada"),
    ("audiovisual", "Producción audiovisual", "Imagen con estética de cine para que tu marca se vea como se merece en web, redes y campañas.",
     ["Video institucional y publicitario", "Drone 4K y tomas aéreas", "Fotografía de producto, espacios y retrato", "Reels y contenido vertical para redes", "Edición, color y postproducción", "Cobertura de eventos"],
     "audiovisual", "work-petunia-2.webp", "Motorhome al atardecer frente al lago en Petunia"),
    ("branding", "Branding & diseño", "Una identidad coherente que se reconoce en todos los puntos de contacto, de la web al cartel de la entrada.",
     ["Logo e identidad visual", "Manual de marca", "Paleta, tipografías y sistema gráfico", "Piezas gráficas y papelería", "Key visuals para campañas", "Brochures y presentaciones comerciales"],
     "branding", None, None),
    ("marketing", "Marketing & contenido", "Estrategia, contenido y distribución con un objetivo claro: que la gente correcta te encuentre y te elija.",
     ["Estrategia de marketing digital", "Gestión de redes sociales", "Copywriting de conversión", "Campañas y pauta", "SEO local y Google Business", "Automatización de publicaciones"],
     "marketing", "svc-marketing.webp", "Ilustración: perfil de redes, calendario de contenido, campaña activa y estrategia"),
]
_ORDER = ["marketing", "agentes-ia", "audiovisual", "diseno-web", "masterplan-360", "branding"]
SVC_DETAIL.sort(key=lambda s: _ORDER.index(s[0]))
PACKS = [
    ("Web Start", "Landing o sitio básico", "Para validar una idea, lanzar un servicio o captar consultas rápido."),
    ("Web Pro", "Sitio profesional", "Sitio completo con SEO, analytics, WhatsApp e integraciones."),
    ("Web Business", "Web + estrategia", "Sitio, estrategia de contenido y automatizaciones para generar oportunidades."),
    ("Web Experience", "La solución integral", "Web + foto/video/drone + 360° + agente IA. Para marcas que quieren destacarse.", True),
]
COMBO_KEYS = ["hotel", "restaurante", "inmobiliaria"]
COMBOS = [
    ("Hotel / cabañas", "Branding · foto y drone · video · web con reservas · SEO local · agente IA"),
    ("Restaurante", "Fotografía gastronómica · reels · landing · reservas · Google · agente IA"),
    ("Inmobiliaria / desarrollo", "Drone · recorridos 360° · masterplan · landing por proyecto · CRM · automatización"),
]

def servicios():
    blocks = ""
    for i, (sid, name, lead, items, q, img, alt) in enumerate(SVC_DETAIL):
        fig = f'<figure data-reveal><img src="assets/img/{img}" alt="{alt}" loading="lazy" width="1000" height="1250"></figure>' if img else ""
        if sid == "agentes-ia" and not img:
            fig = f'<div class="wa-mini">{wa_demo()}</div>'
        if sid == "diseno-web":
            fig = ('<figure data-reveal><video autoplay muted loop playsinline preload="metadata" poster="assets/img/svc-web.jpg" '
                   'aria-label="Animación: diseño y desarrollo de sitios web en laptop"><source src="assets/video/svc-web.mp4" type="video/mp4"></video></figure>')
        if sid == "masterplan-360":
            fig = ('<figure data-reveal><video autoplay muted loop playsinline preload="metadata" poster="assets/img/svc-masterplan.jpg" '
                   'aria-label="Animación: masterplan interactivo y disponibilidad de unidades conectada al CRM"><source src="assets/video/svc-masterplan.mp4" type="video/mp4"></video></figure>')
        if sid == "branding":
            fig = ('<figure data-reveal><video autoplay muted loop playsinline preload="metadata" poster="assets/img/svc-branding.jpg" '
                   'aria-label="Animación: piezas de diseño e identidad visual"><source src="assets/video/svc-branding.mp4" type="video/mp4"></video></figure>')
        if sid == "audiovisual":
            fig = ('<figure data-reveal><video autoplay muted loop playsinline preload="metadata" poster="assets/img/svc-audiovisual.jpg" '
                   'aria-label="Detrás de escena: cámara y producción de contenido"><source src="assets/video/svc-audiovisual.mp4" type="video/mp4"></video></figure>')
        packs = ""
        if sid == "diseno-web":
            packs = '<div class="packs">' + "".join(
                f'<a class="pack{" pack--hot" if len(p) > 3 else ""}" href="presupuesto.html?servicio=web&amp;formato={p[0].replace(" ", "+")}" data-reveal><small>{p[1]}</small><h3>{p[0]}</h3><p>{p[2]}</p><span class="pack__go">Pedir este formato {ARROW}</span></a>' for p in PACKS) + '</div>'
        if i == 3:
            blocks += '<p class="kicker svc-sep">También hacemos</p>'
        blocks += f'''<section class="svc-detail" id="{sid}" aria-labelledby="{sid}-t">
  <span class="n" aria-hidden="true">0{i+1}</span>
  <div><h2 id="{sid}-t" data-split>{name}</h2><p class="lead" data-reveal>{lead}</p>{fig}</div>
  <div data-reveal><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul><a class="btn" href="presupuesto.html?servicio={q}">Pedir propuesta {ARROW}</a></div>
</section>
{f'<div style="padding-bottom:clamp(48px,7vw,96px);border-bottom:1px solid var(--line)"><p class="kicker">Formatos web</p>{packs}</div>' if packs else ''}'''
    combos = "".join(f'<a class="pillar pillar--link" href="presupuesto.html?solucion={k}" data-tilt data-reveal><span class="n">Solución integral</span><div><h3>{t}</h3><p>{d}</p><span class="pack__go">Pedir esta solución {ARROW}</span></div></a>' for k, (t, d) in zip(COMBO_KEYS, COMBOS))
    body = f'''{header("servicios.html")}
<main id="main">
<section class="page-hero">
  {bolt("page-hero__bolt")}
  <div class="wrap">
    <p class="kicker">Flesh Studio <b>/</b> Qué hacemos</p>
    <h1 data-split>Servicios</h1>
    <p class="lead" data-reveal>Nuestro foco: marketing, agentes IA y contenido audiovisual. Entramos en una etapa puntual o tomamos el proyecto completo, de la estrategia al lanzamiento.</p>
  </div>
</section>
<div class="wrap">{blocks}</div>
<section class="section" aria-labelledby="combo-t">
  <div class="wrap">
    <p class="kicker">Flesh Studio <b>/</b> Todo junto rinde más</p>
    <h2 id="combo-t" class="h-lg" data-split style="margin:18px 0 clamp(36px,5vw,60px)">Soluciones <em>por rubro</em></h2>
    <div class="pillars">{combos}</div>
  </div>
</section>
{marquee_big()}
{cta_block()}
</main>
'''
    return head("Servicios — Flesh Studio | Marketing, agentes IA y producción audiovisual",
                "Marketing y redes, agentes IA que atienden y venden 24/7, producción audiovisual con drone y reels. También diseño web, recorridos 360° y branding.",
                "servicios.html") + body + footer()

# ---------------------------------------------------------------- PROYECTOS
def proyectos():
    cards = "".join(card(p, True) for p in PROJECTS)
    filters = [("all", "Todos"), ("realestate", "Real estate"), ("turismo", "Turismo"), ("web", "Web"), ("audiovisual", "Audiovisual")]
    chips = "".join(f'<button type="button" class="chip" data-filter="{f}" aria-pressed="{"true" if f=="all" else "false"}">{t}</button>' for f, t in filters)
    body = f'''{header("proyectos.html")}
<main id="main">
<section class="page-hero">
  {bolt("page-hero__bolt")}
  <div class="wrap">
    <p class="kicker">Flesh Studio <b>/</b> Trabajo seleccionado</p>
    <h1 data-split>Proyectos</h1>
    <p class="lead" data-reveal>Cada proyecto arranca con una pregunta: ¿qué tiene que hacer la persona que llega? Reservar, consultar, comprar o recordarte.</p>
  </div>
</section>
<section class="section" style="padding-top:clamp(40px,6vw,70px)">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filtrar proyectos">{chips}</div>
    <div class="work-list">{cards}{next_card()}</div>
  </div>
</section>
{marquee_small()}
{cta_block()}
</main>
'''
    return head("Proyectos — Flesh Studio | Trabajo seleccionado",
                "Webs, contenido audiovisual y soluciones digitales para turismo y real estate en Argentina y Chile.",
                "proyectos.html") + body + footer()

# ---------------------------------------------------------------- STUDIO
def studio():
    pillars = [("01", "Marketing", "Estrategia, redes y campañas con estética editorial para que tu marca no solo esté: domine."),
               ("02", "Agentes IA", "El cerebro que opera sin descanso: responde, califica, reserva y ordena tus oportunidades."),
               ("03", "Contenido audiovisual", "Video, drone, reels y fotografía con mirada de cine, producidos por el mismo equipo que piensa la estrategia.")]
    p_html = "".join(f'<div class="pillar" data-tilt data-reveal><span class="n">{n}</span><div><h3>{t}</h3><p>{d}</p></div></div>' for n, t, d in pillars)
    gear = [("Sony Full Frame", "Video y foto 4K con look cinematográfico"), ("Drone 4K", "Tomas aéreas para campañas, turismo y real estate"),
            ("Agentes IA", "Memoria y contexto, integrados a WhatsApp y CRM"), ("Óptica 360° 8K", "Recorridos virtuales de alta definición"),
            ("Desarrollo web", "Sitios a medida, rápidos y optimizados para SEO"), ("Dos bases", "Rosario y Bariloche, con proyectos en Argentina y Chile")]
    g_html = "".join(f'<div data-reveal><b>{t}</b><span>{d}</span></div>' for t, d in gear)
    values = ["Claridad", "Impacto", "Estética", "Tecnología", "Conversión", "Cercanía"]
    body = f'''{header("studio.html")}
<main id="main">
<section class="page-hero">
  {bolt("page-hero__bolt")}
  <div class="wrap">
    <p class="kicker">Flesh Studio <b>/</b> Studio</p>
    <h1 data-split>Somos <em>Flesh.</em></h1>
    <p class="lead" data-reveal>Un estudio multidisciplinario que fusiona precisión técnica con realidad tangible. Programamos, filmamos y activamos marcas para sectores que necesitan destacarse.</p>
  </div>
</section>
<section class="section" aria-labelledby="st-t">
  <div class="wrap two-col">
    <div><p class="kicker">El motor invisible</p><h2 id="st-t" class="h-md" data-split style="margin-top:18px">Detrás de tu próxima <em>gran impresión.</em></h2></div>
    <div data-reveal>
      <p class="lead" style="max-width:none">Convertimos contenido crudo en experiencias de alto impacto. Nuestra misión es que tu negocio sea transitable, inteligente y, sobre todo, real.</p>
      <p style="color:var(--mute)">Trabajamos con gastronomía, construcción, real estate, hotelería, turismo y marcas personales. La diferencia está en tener imagen, tecnología y estrategia bajo el mismo techo: menos intermediarios, un solo criterio y resultados que se pueden medir.</p>
      <div class="values" aria-label="Valores">{"".join(f"<span>{v}</span>" for v in values)}</div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0" aria-labelledby="pil-t">
  <div class="wrap">
    <p class="kicker">Tres pilares</p>
    <h2 id="pil-t" class="h-lg" data-split style="margin:18px 0 clamp(36px,5vw,60px)">Lo que nos <em>mueve</em></h2>
    <div class="pillars">{p_html}</div>
  </div>
</section>
<section class="reel" aria-label="Reel">
  <div class="wrap">
    <div class="reel__frame">
      <video autoplay muted loop playsinline preload="metadata" poster="assets/img/hero-poster.jpg" aria-label="Showreel de Flesh Studio">
        <source src="assets/video/hero-1080.mp4" type="video/mp4">
      </video>
      <div class="reel__overlay"><div class="reel__cap"><span>Showreel</span><span>Flesh Studio</span></div><p class="reel__big" aria-hidden="true">Velocidad<br>con criterio</p><div class="reel__cap"><span>Marketing · IA · Audiovisual</span><span>Patagonia — Arg — Worldwide</span></div></div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0" aria-labelledby="gear-t">
  <div class="wrap">
    <p class="kicker">Capacidades</p>
    <h2 id="gear-t" class="h-lg" data-split style="margin:18px 0 clamp(36px,5vw,60px)">Equipo <em>& herramientas</em></h2>
    <div class="gear">{g_html}</div>
  </div>
</section>
{marquee_small()}
{cta_block()}
</main>
'''
    return head("Studio — Flesh Studio | Tecnología con esencia",
                "Flesh Studio es una agencia de marketing, agentes IA y producción audiovisual con bases en Rosario y Bariloche.",
                "studio.html") + body + footer()

# ---------------------------------------------------------------- PRESUPUESTO
def presupuesto():
    services = [("marketing", "Marketing & redes"), ("ia", "Agente IA / automatización"), ("audiovisual", "Video, foto o drone"),
                ("web", "Sitio web / landing"), ("masterplan", "Masterplan / tour 360°"), ("branding", "Branding / diseño"), ("otro", "Otro")]
    s_html = "".join(f'<label class="choice"><input type="checkbox" name="servicio" value="{v}" data-label="{t}"><span>{t}</span></label>' for v, t in services)
    plazos = ["Lo antes posible", "En 1 a 2 meses", "En 3 meses o más", "Sin fecha definida"]
    p_html = "".join(f'<label class="choice"><input type="radio" name="plazo" value="{p}"{" checked" if i==3 else ""}><span>{p}</span></label>' for i, p in enumerate(plazos))
    rubros = ["Real estate / desarrollo", "Turismo / hotelería", "Gastronomía", "Construcción", "Marca personal", "Comercio / e-commerce", "Empresa / servicios", "Otro"]
    body = f'''{header("presupuesto.html")}
<main id="main">
<section class="page-hero">
  {bolt("page-hero__bolt")}
  <div class="wrap">
    <p class="kicker">Presupuesto online</p>
    <h1 data-split>Pedí tu <em>propuesta.</em></h1>
    <p class="lead" data-reveal>Contanos qué necesitás. Con esta información preparamos una propuesta a medida de tu proyecto. Te toma 2 minutos.</p>
  </div>
</section>
<section class="section" style="padding-top:clamp(40px,6vw,70px)">
  <div class="wrap q-layout">
    <form class="qform" id="qform" novalidate>
      <div class="hp" aria-hidden="true"><label for="f-web2">No completar</label><input id="f-web2" name="web2" type="text" tabindex="-1" autocomplete="off"></div>
      <fieldset class="qstep"><legend><small>01</small>Tus datos</legend>
        <div class="qstep__body"><div class="fields">
          <div class="field"><label for="f-nombre">Nombre / empresa <span class="req">*</span></label><input id="f-nombre" name="nombre" autocomplete="name" required maxlength="80"><span class="err">Contanos cómo te llamás.</span></div>
          <div class="field"><label for="f-email">Email <span class="req">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="120"><span class="err">Revisá el email.</span></div>
          <div class="field"><label for="f-tel">WhatsApp <span class="req">*</span></label><input id="f-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" required maxlength="30"><span class="err">Necesitamos un número para contactarte.</span><span class="hint">Solo lo usamos para responder esta solicitud.</span></div>
          <div class="field"><label for="f-ciudad">Ciudad</label><input id="f-ciudad" name="ciudad" autocomplete="address-level2" maxlength="80"></div>
        </div></div>
      </fieldset>
      <fieldset class="qstep"><legend><small>02</small>¿Qué necesitás?</legend>
        <div class="qstep__body"><div class="choices" id="c-servicio">{s_html}</div><span class="group-err">Elegí al menos una opción.</span></div>
      </fieldset>
      <fieldset class="qstep"><legend><small>03</small>Tu proyecto</legend>
        <div class="qstep__body"><div class="fields">
          <div class="field"><label for="f-rubro">Rubro</label><select id="f-rubro" name="rubro"><option value="">Elegí una opción</option>{"".join(f"<option>{r}</option>" for r in rubros)}</select></div>
          <div class="field"><label for="f-ref">Web o Instagram actual</label><input id="f-ref" name="ref" type="url" inputmode="url" placeholder="https://" maxlength="200"></div>
          <div class="field field--full"><label for="f-detalle">Contanos sobre el proyecto <span class="req">*</span></label><textarea id="f-detalle" name="detalle" required maxlength="2000" placeholder="Qué querés lograr, a quién apuntás, qué tenés hoy…"></textarea><span class="err">Escribí al menos una línea sobre el proyecto.</span></div>
        </div></div>
      </fieldset>
      <fieldset class="qstep"><legend><small>04</small>Prioridades</legend>
        <div class="qstep__body"><div class="bbb" data-bbb>
          <div class="bbb__flash" aria-hidden="true"></div>
          <div class="bbb__hud" aria-hidden="true"><span>Elegí dos · Las tres juntas no existen</span><span class="bbb__count"><span class="bbb__pips"><i class="bbb__pip"></i><i class="bbb__pip"></i></span><b class="bbb__num">0/2</b></span></div>
          <div class="bbb__rows" role="group" aria-label="Elegí dos prioridades"><button type="button" class="bbb__row" data-k="bueno" aria-pressed="false"><span class="bbb__fill"></span><span class="bbb__idx">01</span><span class="bbb__state"><svg viewBox="16 0 70 160" aria-hidden="true"><path d="M38 0H78L58 62H86L28 160L44 86H16Z"/></svg><b>—</b></span><span class="bbb__word"><span class="bbb__half bbb__half--top">Bueno</span><span class="bbb__half bbb__half--bot" aria-hidden="true">Bueno</span></span><svg class="bbb__zap" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><polyline points="-2,55 14,42 24,60 40,36 52,63 66,40 78,58 102,46"/></svg></button><button type="button" class="bbb__row" data-k="bonito" aria-pressed="false"><span class="bbb__fill"></span><span class="bbb__idx">02</span><span class="bbb__state"><svg viewBox="16 0 70 160" aria-hidden="true"><path d="M38 0H78L58 62H86L28 160L44 86H16Z"/></svg><b>—</b></span><span class="bbb__word"><span class="bbb__half bbb__half--top">Bonito</span><span class="bbb__half bbb__half--bot" aria-hidden="true">Bonito</span></span><svg class="bbb__zap" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><polyline points="-2,48 12,60 26,38 38,62 54,40 64,61 80,37 102,54"/></svg></button><button type="button" class="bbb__row" data-k="barato" aria-pressed="false"><span class="bbb__fill"></span><span class="bbb__idx">03</span><span class="bbb__state"><svg viewBox="16 0 70 160" aria-hidden="true"><path d="M38 0H78L58 62H86L28 160L44 86H16Z"/></svg><b>—</b></span><span class="bbb__word"><span class="bbb__half bbb__half--top">Barato</span><span class="bbb__half bbb__half--bot" aria-hidden="true">Barato</span></span><svg class="bbb__zap" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><polyline points="-2,52 16,38 28,62 42,40 56,60 70,36 84,60 102,44"/></svg></button></div>
          <div class="bbb__msg" aria-live="polite"><span class="bbb__tag"></span><p class="bbb__text"></p></div>
          <div class="bbb__ticker" aria-hidden="true"><div class="bbb__ticker-track"></div></div>
          <input type="hidden" name="prioridades" value=""><input type="hidden" name="descartado" value="">
        </div></div>
      </fieldset>
      <fieldset class="qstep"><legend><small>05</small>Plazo</legend>
        <div class="qstep__body"><div class="choices">{p_html}</div></div>
      </fieldset>
      <div class="qsubmit">
        <p>Al enviar se abre WhatsApp con tu solicitud lista para mandar. Si preferís, también podés enviarla por email.</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap">
          <button class="btn" type="submit" data-magnetic>{WA_ICON} Enviar por WhatsApp</button>
          <button class="btn btn--ghost" type="button" id="send-mail">Enviar por email</button>
        </div>
      </div>
      <div class="form-ok" role="status" aria-live="polite"></div>
    </form>
    <aside class="aside-card" aria-label="Contacto directo">
      <h3>¿Preferís hablar directo?</h3>
      <p>Escribinos y coordinamos una primera reunión sin costo.</p>
      <a href="{WA}" target="_blank" rel="noopener">{WA_ICON} +54 9 2944 15-2161</a>
      <a href="mailto:{MAIL}"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg> {MAIL}</a>
      <a href="{IG}" target="_blank" rel="noopener">{IG_ICON} @flesh_studio</a>
    </aside>
  </div>
</section>
</main>
'''
    return head("Presupuesto — Flesh Studio | Pedí tu propuesta",
                "Solicitá una propuesta de marketing, agente IA o contenido audiovisual (también webs y 360°). Respuesta directa por WhatsApp o email.",
                "presupuesto.html") + body + footer('<script src="assets/js/bbb.js" defer></script>\n<script src="assets/js/form.js" defer></script>')

pages = {"index.html": index(), "servicios.html": servicios(), "proyectos.html": proyectos(),
         "studio.html": studio(), "presupuesto.html": presupuesto()}
if not SHOW_PROYECTOS:
    pages["proyectos.html"] = pages["proyectos.html"].replace('<meta name="theme-color"', '<meta name="robots" content="noindex, nofollow">\n<meta name="theme-color"', 1)
HTACCESS = r"""# Flesh Studio — seguridad y rendimiento (Apache / Hostinger)
Options -Indexes
ServerSignature Off
DirectoryIndex index.html
<IfModule mod_rewrite.c>
  RewriteEngine On
  # HTTPS obligatorio y dominio sin www
  RewriteCond %{HTTPS} off [OR]
  RewriteCond %{HTTP_HOST} ^www\. [NC]
  RewriteRule ^ https://flesh-studio.com%{REQUEST_URI} [L,R=301]
  # archivos internos que no deben servirse
  RewriteRule (^|/)\.(?!well-known/) - [F]
  RewriteRule ^(build\.py|gen_carrusel\.py|README\.md|LEEME\.txt)$ - [F,NC]
  RewriteRule ^_ - [F]
</IfModule>
<IfModule mod_headers.c>
  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
  Header always set Content-Security-Policy "%CSP%; frame-ancestors 'none'"
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "DENY"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()"
  Header always set Cross-Origin-Opener-Policy "same-origin"
  Header unset X-Powered-By
  <FilesMatch "\.(webp|jpg|png|svg|woff2|mp4)$">
    Header set Cache-Control "public, max-age=2592000"
  </FilesMatch>
  <FilesMatch "\.(css|js)$">
    Header set Cache-Control "public, max-age=604800"
  </FilesMatch>
  <FilesMatch "\.html$">
    Header set Cache-Control "no-cache"
  </FilesMatch>
</IfModule>
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/json
</IfModule>
AddType video/mp4 .mp4
AddType font/woff2 .woff2
AddType image/webp .webp
"""
extra_files = {
    ".htaccess": HTACCESS.replace("%CSP%", CSP),
    "robots.txt": f"User-agent: *\nAllow: /\nDisallow: /proyectos.html\nSitemap: {BASE_URL}sitemap.xml\n" if not SHOW_PROYECTOS else f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n",
    "sitemap.xml": '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{BASE_URL}{'' if n == 'index.html' else n}</loc></url>\n" for n in pages if SHOW_PROYECTOS or n != "proyectos.html") + "</urlset>\n",
}
for name, txt in extra_files.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(txt)
for name, html in pages.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)
    print(name, len(html))
