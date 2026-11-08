"""Ajustes de SEO posteriores al render (Quarto lo ejecuta solo, vía post-render).

Cloudflare Pages sirve cada página en su dirección "limpia":
    servicios.html        -> /servicios
    index.html            -> /
    portfolio/index.html  -> /portfolio/
y redirige las variantes con .html a esas direcciones. Este script:

1. agrega <link rel="canonical"> y <meta property="og:url"> a cada página,
   con la dirección limpia definitiva;
2. reescribe sitemap.xml para que liste esas mismas direcciones
   (Google desaconseja incluir en el sitemap URL que redirigen).

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
    corregir_sitemap()
    print("SEO: direcciones canónicas y sitemap actualizados.")
