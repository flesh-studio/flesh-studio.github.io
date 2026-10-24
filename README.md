# Flesh Studio — sitio web

Sitio estático (HTML/CSS/JS, sin build) de Flesh Studio: agencia de marketing, 360°, agentes IA y producción audiovisual.

- **Páginas:** `index.html`, `proyectos.html`, `studio.html`, `servicios.html`, `presupuesto.html`
- **Generador:** las 5 páginas salen de `build.py` (header y footer compartidos). Editar ahí y correr `OUT=. python3 build.py`.
- **Estilos / motion:** `assets/css/styles.css`, `assets/js/main.js` (GSAP + ScrollTrigger + Lenis), `assets/js/hero3d.js` (Three.js), `assets/js/form.js`.
- **Librerías y fuentes self-hosted** en `assets/vendor` y `assets/fonts` (sin CDNs).
- Imágenes y videos de portfolio tomados de los sitios de clientes (Petunia, Casa La Cruzada, Cat Díaz).
