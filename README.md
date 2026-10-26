# Sitio web de Darío Díaz · Científico de Datos y Estadístico

Sitio estático construido con [Quarto](https://quarto.org). Las páginas se escriben en Markdown (`.qmd`), los casos del portfolio ejecutan código Python y el resultado se genera en la carpeta `docs/`, que es lo que se publica.

## Estructura

| Archivo | Contenido |
|---|---|
| `_quarto.yml` | Configuración general: menú, pie de página, dominio, tema |
| `styles.scss` | Colores y tipografías |
| `index.qmd` | Portada |
| `servicios.qmd` | Detalle de servicios |
| `capacitaciones.qmd` | Catálogo de cursos |
| `portfolio/` | Listado de casos y un archivo `.qmd` por caso |
| `sobre-mi.qmd` | Formación, docencia, investigación y publicaciones |
| `independencia.qmd` | Declaración de independencia y confidencialidad |
| `contacto.qmd` | Contacto y datos fiscales |
| `img/` | Logo, favicon y, si se agrega, la foto |
| `docs/` | Sitio generado; **no se edita a mano** |
| `_freeze/` | Resultados guardados del código; evita reejecutarlo en cada render |

## 1. Completar antes de publicar

Ya están cargados LinkedIn (`dr-dario-ezequiel-diaz`), GitHub (`DrDarioDiaz`), el dominio `dariodiaz.com.ar` (en `_quarto.yml` y `CNAME`) y la foto (`img/foto.jpg`). Queda pendiente un solo cambio:

- Cuando funcione el correo con dominio propio, reemplazar `drdarioezequieldiaz@gmail.com` por `contacto@dariodiaz.com.ar` en `contacto.qmd`.

La imagen `img/og.jpg` es la tarjeta que se muestra al compartir el enlace en LinkedIn, WhatsApp u otras redes.

## 2. Ver y generar el sitio en la computadora

Una sola vez:

```bash
# Instalar Quarto desde https://quarto.org/docs/get-started/
pip install -r requirements.txt
```

Cada vez que se modifica algo:

```bash
quarto preview   # abre el sitio en el navegador y lo actualiza al guardar
quarto render    # genera la versión final en docs/
```

## 3. Subir a GitHub

```bash
git init
git add .
git commit -m "Primera versión del sitio"
git branch -M main
git remote add origin https://github.com/DrDarioDiaz/dariodiaz-web.git
git push -u origin main
```

Luego, cada actualización se publica con `quarto render`, `git add .`, `git commit -m "..."` y `git push`.

## 4. Publicar (elegir una opción)

**Opción recomendada: Cloudflare Pages (gratuita).**

1. Crear una cuenta en Cloudflare y entrar en *Workers & Pages* → *Create* → *Pages* → *Connect to Git*.
2. Elegir el repositorio `dariodiaz-web`.
3. Configuración de compilación: sin framework, **comando de compilación vacío**, **directorio de salida `docs`**.
4. Guardar. El sitio queda disponible en una dirección `*.pages.dev` y se actualiza solo con cada `git push`.
5. En *Custom domains*, agregar el dominio propio.

**Alternativa: GitHub Pages.** En el repositorio, *Settings* → *Pages* → *Deploy from a branch* → rama `main`, carpeta `/docs`. El archivo `CNAME` ya indica el dominio.

## 5. Dominio .com.ar

1. Registrarlo en [nic.ar](https://nic.ar) con CUIT y clave fiscal; la renovación es anual.
2. Si se publica con Cloudflare: agregar el dominio en Cloudflare, copiar los dos servidores DNS que indica y cargarlos en NIC Argentina como *delegación* del dominio.
3. Si se publica con GitHub Pages: crear en el proveedor de DNS los registros que indica la documentación de GitHub Pages para dominios propios.

## 6. Correo con dominio propio (gratuito)

Con el dominio en Cloudflare, *Email Routing* permite crear `contacto@dominio` y reenviarlo a Gmail. Para responder desde esa dirección, Gmail admite agregarla en *Configuración* → *Cuentas* → *Enviar como*.

## 7. Agregar un caso al portfolio

1. Copiar uno de los archivos de `portfolio/` con un nombre nuevo.
2. Cambiar `title`, `subtitle`, `description`, `date` y `categories` en el encabezado.
3. Escribir el caso y ejecutar `quarto render`. El listado del portfolio se actualiza solo.

Regla de oro: **usar únicamente datos públicos o simulados**, nunca información de clientes ni datos a los que se acceda por la función pública.
