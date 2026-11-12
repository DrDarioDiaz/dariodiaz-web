"""Ajustes de SEO posteriores al render (Quarto lo ejecuta solo, vía post-render).

Cloudflare Pages sirve cada página en su dirección "limpia":
    servicios.html        -> /servicios
    index.html            -> /
    portfolio/index.html  -> /portfolio/
y redirige las variantes con .html a esas direcciones. Este script:

1. agrega <link rel="canonical"> y <meta property="og:url"> a cada página,
   con la dirección limpia definitiva;
2. reescribe sitemap.xml para que liste esas mismas direcciones
   (Google desaconseja incluir en el sitemap URL que redirigen);
3. reescribe los enlaces internos (menú, pie, botones, listado del
   portfolio) para que apunten a la dirección limpia y no a la variante
   .html. Así Googlebot no descubre URL que redirigen, que Search Console
   informa como "Página con redirección" o, si el rastreo coincide con una
   publicación, como "Error de redirección".

Nota: después de este paso, la vista previa con `python -m http.server`
no resuelve /servicios (falta el .html); para revisar en local use
`npx wrangler pages dev docs` o el servidor de prueba de la skill.

Es idempotente: si se ejecuta dos veces no duplica nada.
"""
from pathlib import Path
import re

SITIO = "https://dariodiaz.com.ar"
SALIDA = Path(__file__).resolve().parent / "docs"


def url_limpia(ruta_relativa: str) -> str:
    ruta = ruta_relativa.replace("\\", "/")
    if ruta == "index.html":
        return SITIO + "/"
    if ruta.endswith("/index.html"):
        return f"{SITIO}/{ruta[: -len('index.html')]}"
    if ruta.endswith(".html"):
        return f"{SITIO}/{ruta[: -len('.html')]}"
    return f"{SITIO}/{ruta}"


def paginas():
    for archivo in sorted(SALIDA.rglob("*.html")):
        rel = archivo.relative_to(SALIDA).as_posix()
        if rel.startswith("site_libs/") or "_files/" in rel:
            continue
        yield archivo, rel


def marcar_canonica(archivo: Path, rel: str) -> None:
    html = archivo.read_text(encoding="utf-8")
    destino = url_limpia(rel)
    html = re.sub(r'\s*<link rel="canonical"[^>]*>', "", html)
    html = re.sub(r'\s*<meta property="og:url"[^>]*>', "", html)
    etiquetas = (
        f'\n<link rel="canonical" href="{destino}">'
        f'\n<meta property="og:url" content="{destino}">\n'
    )
    html = html.replace("</head>", etiquetas + "</head>", 1)
    archivo.write_text(html, encoding="utf-8")


ENLACE = re.compile(r'(href=")([^"]*)(")')


def limpiar_href(href: str) -> str:
    """Convierte un enlace interno a su dirección limpia, conservando
    la ruta relativa y el fragmento: servicios.html#muestras -> servicios#muestras,
    ./portfolio/index.html -> ./portfolio/, ../index.html -> ../"""
    if href.startswith(SITIO + "/"):
        prefijo, ruta = SITIO + "/", href[len(SITIO) + 1:]
    elif "://" in href or href.startswith(("mailto:", "tel:", "#", "//", "data:")):
        return href
    else:
        prefijo, ruta = "", href
    m = re.match(r"^([^#?]*)([#?].*)?$", ruta)
    camino, cola = m.group(1), m.group(2) or ""
    if camino.startswith("site_libs/") or "/site_libs/" in camino or not camino.endswith(".html"):
        return href
    if camino == "index.html" or camino.endswith("/index.html"):
        camino = camino[: -len("index.html")] or "./"
    else:
        camino = camino[: -len(".html")]
    return prefijo + camino + cola


def limpiar_enlaces(archivo: Path) -> None:
    html = archivo.read_text(encoding="utf-8")
    nuevo = ENLACE.sub(lambda m: m.group(1) + limpiar_href(m.group(2)) + m.group(3), html)
    if nuevo != html:
        archivo.write_text(nuevo, encoding="utf-8")


def corregir_sitemap() -> None:
    sitemap = SALIDA / "sitemap.xml"
    if not sitemap.exists():
        return
    xml = sitemap.read_text(encoding="utf-8")

    def reemplazo(m: re.Match) -> str:
        url = m.group(1)
        if url.startswith(SITIO + "/"):
            url = url_limpia(url[len(SITIO) + 1:])
        return f"<loc>{url}</loc>"

    xml = re.sub(r"<loc>([^<]+)</loc>", reemplazo, xml)
    sitemap.write_text(xml, encoding="utf-8")


if __name__ == "__main__":
    for archivo, rel in paginas():
        marcar_canonica(archivo, rel)
        limpiar_enlaces(archivo)
    corregir_sitemap()
    print("SEO: direcciones canónicas, enlaces internos y sitemap actualizados.")
