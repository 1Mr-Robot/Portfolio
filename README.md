# Portfolio Web

Portfolio personal de Uziel Flores — desarrollador backend y creador de contenido tecnico.

## Proposito

Este proyecto es un sitio web portfolio dinamico construido con Django 6.0.1 que muestra proyectos de software, habilidades tecnicas y presencia en redes sociales. A diferencia de un portfolio estatico, este se gestiona completamente desde el panel de administracion de Django, permitiendo agregar, editar y organizar contenido sin necesidad de tocar codigo.

## Arquitectura

El proyecto sigue una arquitectura monolitica clsica de Django organizada en dos aplicaciones (apps):

```
Portfolio/
├── Portfolio/              # Configuracion del proyecto Django
│   ├── settings.py         # Configuracion global (BD, apps, middlewares, etc.)
│   ├── urls.py             # Rutas principales del proyecto
│   ├── wsgi.py             # Punto de entrada WSGI para servidores
│   └── asgi.py             # Punto de entrada ASGI (para async/WebSockets)
├── core/                   # App: contenido general del sitio
│   ├── models.py           # SkillCategory, Skill, SocialNetwork, SocialUser
│   ├── views.py            # Vista home y archivo robots.txt
│   ├── urls.py             # Rutas de la app core
│   ├── sitemaps.py         # Generacion de sitemap XML (estatico + proyectos)
│   ├── admin.py            # Configuracion del panel de administracion
│   └── templates/          # Plantillas HTML (base, home, errores)
├── projects/               # App: gestion de proyectos
│   ├── models.py           # Project, ProjectImage, ProjectType, etc.
│   ├── views.py            # Vista de detalle de proyecto
│   ├── urls.py             # Rutas de la app projects
│   ├── signals.py          # Procesamiento de OG images y conversion a WebP
│   ├── admin.py            # Configuracion del panel de administracion
│   └── services/           # Logica de negocio reutilizable
│       ├── og_image_processing.py  # Procesamiento de imagenes OG
│       └── get_og_content.py        # Obtencion de datos OG
├── db.sqlite3              # Base de datos SQLite
├── manage.py               # Utilidad CLI de Django
├── requirements.txt        # Dependencias de produccion
└── requirements-dev.txt    # Dependencias de desarrollo
```

### Modelos de datos

**App `core`**
- `SkillCategory` — Categorias para agrupar habilidades (lenguajes, frameworks, herramientas).
- `Skill` — Habilidades individuales con nombre, descripcion (CKEditor), icono SVG, categoria y orden.
- `SocialNetwork` — Redes sociales disponibles con nombre, slug, URL base y validador.
- `SocialUser` — Perfiles del usuario en cada red social con username, texto a mostrar, opcion de aparecer en el hero, y orden.

**App `projects`**
- `ProjectType` — Tipos de proyectos (web, CLI, movil, etc.).
- `ProjectRole` — Roles desempenados (desarrollador, lider tecnico, etc.).
- `Project` — Proyectos con titulo, slug, descripcion (CKEditor), descripcion corta, resumen, fecha de fin, URLs, duracion, numero de miembros, imagen OG (1200x630 JPG), y orden.
- `ProjectImage` — Imagenes de cada proyecto (convertidas automaticamente a WebP).
- `ProjectCharacteristic` — Caracteristicas/claves de cada proyecto con titulo, descripcion y icono SVG.
- `ProjectTechnology` — Tecnologias usadas en proyectos (independientes de Skill para reutilizar en cualquier proyecto).
- `ProjectTechnologyLink` — Relacion many-to-many entre proyectos y tecnologias.

### Rutas principales

| Ruta | Vista | Descripcion |
|------|-------|-------------|
| `/` | `core.views.home` | Pagina principal con hero, habilidades, proyectos y footer |
| `/projects/<slug>/` | `projects.views.project` | Pagina de detalle de un proyecto |
| `/sitemap.xml` | Sitemap de Django | Generacion automatica de sitemap para SEO |
| `/robots.txt` | `core.views.robots_txt` | Archivo robots.txt |

## Herramientas y dependencias

| Paquete | Version | Proposito |
|---------|---------|-----------|
| Django | 6.0.1 | Framework web principal |
| django-cotton | 2.6.2 | Sistema de componentes reutilizables para templates |
| django-ckeditor-5 | 0.2.20 | Editor de texto enriquecido en el admin |
| django-admin-sortable2 | 2.3.1 | Ordenamiento drag-and-drop en el admin |
| Pillow | 12.1.0 | Procesamiento de imagenes (resize, conversion de formato) |
| python-dotenv | 1.2.1 | Carga de variables de entorno desde archivo `.env` |

### Procesamiento de imagenes

- **OG Images de proyectos**: al subir una imagen, se redimensiona automaticamente a **1200x630 px en formato JPG** y se guarda con el nombre del proyecto.
- **Imagenes de proyectos**: se convierten automaticamente a formato **WebP con calidad 85%** para optimizar el peso.

### SEO

- Generacion automatica de `sitemap.xml` que incluye paginas estaticas y proyectos activos.
- Sitemap implementa `lastmod` con la fecha de modificacion del proyecto.
- Archivo `robots.txt` servible como archivo estatico.

## Stack de frontend

- **HTML/CSS/JS** vanilla con bootstrap.
- **Django Cotton** para componentes reutilizables.
- **CSS modular** organizado por secciones: variables, layout, header, footer, hero, skills, projects, contact, errores, responsive.
- **SVG inline** para iconos (habilidades, redes sociales, caracteristicas de proyecto).
- **Responsive design** con media queries.

## Instalacion local

Ver [CONTRIBUTING.md](./CONTRIBUTING.md) para instrucciones detalladas de configuracion y ejecucion del proyecto en entorno local.