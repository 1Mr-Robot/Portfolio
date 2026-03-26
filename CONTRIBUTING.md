# Guia de contribucion

Esta guia cubre todo lo necesario para configurar el proyecto en un entorno de desarrollo local y trabajar en el codigo.

## Requisitos previos

- **Python** 3.10 o superior
- **Git**
- Un editor de codigo compatible con Django (VS Code, PyCharm, etc.)

## Estructura del proyecto

```
Portfolio/
├── Portfolio/           # Configuracion del proyecto Django
├── core/                # App: habilidades, redes sociales, vistas principales
├── projects/            # App: proyectos, imagenes, tecnologias
├── media/               # Archivos subidos por usuarios
├── manage.py             # CLI de Django
├── requirements.txt      # Dependencias de produccion
├── requirements-dev.txt  # Dependencias de desarrollo
└── .env                  # Variables de entorno (crear desde .env.example)
```

## Instalacion paso a paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/1Mr-Robot/ProyectoAPS.git
cd Portfolio
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
```

En **Windows**:

```bash
venv\Scripts\activate
```

En **macOS / Linux**:

```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Para instalar dependencias de desarrollo:

```bash
pip install -r requirements-dev.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y ajustalo:

```bash
cp .env.example .env
```

Edita el archivo `.env` creado:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=127.0.0.1,localhost
```

> Para generar una SECRET_KEY segura puedes usar:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Ejecutar migraciones de base de datos

```bash
python manage.py migrate
```

Esto crea las tablas en la base de datos SQLite (`db.sqlite3`) segun los modelos definidos en `core` y `projects`.

### 6. Crear un superusuario (opcional, necesario para el admin)

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para establecer usuario y contrasena.

### 7. Recolectar archivos estaticos (para produccion)

```bash
python manage.py collectstatic
```

Para desarrollo esto no es necesario ya que Django sirve los archivos estaticos automaticamente con `DEBUG=True`.

### 8. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

El sitio estará disponible en:

- **Web**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/

## Comandos de Django de uso frecuente

| Comando | Descripcion |
|---------|-------------|
| `python manage.py runserver` | Iniciar servidor de desarrollo |
| `python manage.py makemigrations` | Crear archivos de migracion segun cambios en modelos |
| `python manage.py migrate` | Aplicar migraciones a la base de datos |
| `python manage.py createsuperuser` | Crear usuario administrador |
| `python manage.py collectstatic` | Recolectar archivos estaticos en un directorio |
| `python manage.py shell` | Abrir shell interactivo de Django |
| `python manage.py check` | Validar la configuracion del proyecto |

## Flujo de trabajo comun

### Trabajar en modelos

Si modificas un modelo en `core/models.py` o `projects/models.py`:

1. Genera las migraciones:
   ```bash
   python manage.py makemigrations
   ```

2. Aplicalas a la base de datos:
   ```bash
   python manage.py migrate
   ```

### Trabajar en el panel de administracion

El admin esta configurado en `core/admin.py` y `projects/admin.py`. Las principales caracteristicas disponibles:

- **Ordenamiento drag-and-drop** gracias a `adminsortable2` en modelos ordenables.
- **Editor CKEditor 5** en campos de texto largo (descripciones de habilidades y proyectos).

### Trabajar con imagenes

Las imagenes se procesan automaticamente via signals:

- **OG Images** (`Project.og_image`): se redimensionan a 1200x630 px y se convierten a JPG.
- **Imagenes de proyecto** (`ProjectImage.image`): se convierten a WebP con calidad 85%.

Para que los signals funcionen correctamente, asegurate de que los receivers esten conectados. En `apps.py` de cada app debe estar configurado el metodo `ready()` que importa los signals:

```python
# projects/apps.py
class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'

    def ready(self):
        import projects.signals  # noqa: F401
```

### Trabajar con plantillas

El proyecto usa **Django Cotton** para componentes reutilizables. Los componentes se definen en archivos `.html` dentro de directorios `cotton/` en cada app.

Estructura de templates:

```
core/
└── templates/
    ├── core/
    │   └── home.html
    ├── cotton/           # Componentes Cotton
    ├── elements/         # Elementos reutilizables (header, footer)
    └── error/             # Paginas de error (404, 500)
```

### Trabajar con CSS y JS

Los archivos estaticos estan organizados por app:

```
core/static/core/styles/
├── variables.css    # Variables CSS (colores, fuentes, espaciados)
├── layout.css       # Estructura general de pagina
├── main.css         # Estilos del hero
├── header.css       # Estilos del header
├── footer.css       # Estilos del footer
├── skills.css       # Estilos de la seccion de habilidades
├── projects.css     # Estilos de la seccion de proyectos
├── contact.css      # Estilos de la seccion de contacto
├── responsive.css   # Media queries para responsividad
└── error.css        # Estilos de paginas de error

core/static/core/js/
├── header.js        # Logica del header (scroll, interactividad)
├── skills.js        # Logica de la seccion de habilidades
└── projects.js      # Logica de la seccion de proyectos
```

Para agregar nuevos archivos estaticos, asegurate de:

1. Colocarlos en la carpeta `static/` correspondiente a la app.
2. Cargarlos en las plantillas con `{% load static %}` y la etiqueta `{% static 'path/to/file.css' %}`.

### Trabajar con SEO y sitemap

El sitemap se genera automaticamente y se actualiza cada vez que se crea o modifica un proyecto activo. Las clases `StaticSitemap` y `ProjectSitemap` en `core/sitemaps.py` definen las rutas y sus prioridades.

Para verificar el sitemap:

```
http://127.0.0.1:8000/sitemap.xml
```

## Dockerizacion del proyecto

El proyecto esta configurado para ejecutarse en contenedores Docker con tres servicios: MySQL, Django (Gunicorn) y Nginx.

### Estructura de contenedores

| Servicio | Imagen | Descripcion |
|----------|--------|-------------|
| `db` | mysql:8 | Base de datos MySQL 8 |
| `web` | Dockerfile | Aplicacion Django con Gunicorn |
| `nginx` | nginx:alpine | Servidor web inverso |

### Variables de entorno

Copia `.env.example` a `.env` y configura las siguientes variables:

```env
# Configuracion Django
DEBUG=False
SECRET_KEY=tu-clave-secreta-segura
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
CSRF_TRUSTED_ORIGINS=https://tudominio.com

# Superuser (se crea automaticamente)
SUPERUSER_USERNAME=admin
SUPERUSER_EMAIL=admin@tudominio.com
SUPERUSER_PASSWORD=password-seguro

# Base de datos MySQL
DB_NAME=portfolio
DB_USER=user
DB_PASSWORD=super_secure_password
DB_HOST=db
DB_PORT=3306

# Variables MySQL (deben coincidir con DB_*)
MYSQL_DATABASE=portfolio
MYSQL_USER=user
MYSQL_PASSWORD=super_secure_password
MYSQL_ROOT_PASSWORD=very_strong_root_password
```

### Ejecutar con Docker Compose

1. Construir y ejecutar los contenedores:

```bash
docker-compose up --build
```

2. La aplicacion estara disponible en `http://localhost:8000`

3. Para detener los contenedores:

```bash
docker-compose down
```

Para ejecutar en segundo plano:

```bash
docker-compose up -d --build
```

Ver logs:

```bash
docker-compose logs -f web
```

### Volumenes persistentes

Los volumenes Docker mantienen los datos persistentes:

- `mysql_data`: Datos de la base de datos MySQL
- `static_volume`: Archivos estaticos de Django
- `media_volume`: Archivos subidos por usuarios

### Nginx

Nginx actua como servidor web inverso y sirve:

- Archivos estaticos (`/static/`) desde el volumen
- Archivos media (`/media/`) desde el volumen
- Peticiones dinamicas dirigidas a Gunicorn (`/`)

Configuracion en `nginx/default.conf`:

- Puerto de entrada: 80
- Tamano maximo de subida: 20MB
- Proxy a Django: `http://web:8000`

### Ejecucion sin Docker Compose

Si deseas ejecutar solo el contenedor Django con una base de datos MySQL local:

```bash
# Construir imagen
docker build -t portfolio .

# Ejecutar contenedor
docker run -p 8000:8000 --env-file .env portfolio
```

Configura `.env` con los valores de tu base de datos local:

```env
DB_NAME=portfolio
DB_USER=root
DB_PASSWORD=password
DB_HOST=host.docker.internal
DB_PORT=3306
```

> **Nota**: En Windows, `host.docker.internal` permite acceder al servidor host.

### Personalizacion

- **Puertos**: Modifica los puertos en `docker-compose.yml`
- **Dominio**: Cambia `server_name` en `nginx/default.conf`
- **Superuser**: Las variables `SUPERUSER_*` crean el admin automaticamente en el primer inicio

## Configuracion de produccion

Para desplegar en produccion:

1. Cambia `DEBUG=False` en `.env`.
2. Establece una `SECRET_KEY` segura.
3. Configura `ALLOWED_HOSTS` con el dominio de produccion.
4. Usa un servidor WSGI como **Gunicorn** o **uWSGI**.
5. Configura un servidor web inverso (Nginx, Apache) para servir archivos estaticos y media.
6. Ejecuta `python manage.py collectstatic --noinput` antes de desplegar.

Ejemplo con Gunicorn:

```bash
pip install gunicorn
gunicorn Portfolio.wsgi:application --bind 0.0.0.0:8000
```

## Estructura de la base de datos

La base de datos SQLite (`db.sqlite3`) contiene las siguientes tablas principales:

- `core_skillcategory` — Categorias de habilidades
- `core_skill` — Habilidades individuales
- `core_socialnetwork` — Redes sociales
- `core_socialuser` — Perfiles del usuario en redes sociales
- `projects_projecttype` — Tipos de proyectos
- `projects_projectrole` — Roles en proyectos
- `projects_project` — Proyectos
- `projects_projectimage` — Imagenes de proyectos
- `projects_projectcharacteristic` — Caracteristicas de proyectos
- `projects_projecttechnology` — Tecnologias
- `projects_projecttechnologylink` — Enlace proyecto-tecnologia
- `django_admin_log` — Log de acciones del admin
- `django_content_type` — Registro de modelos
- `auth_*` — Tablas de autenticacion de Django

## Notas importantes

- El campo `order` en la mayoria de modelos controla el orden de presentacion. Usa el admin sortable para reorganizar facilmente.
- Los campos `slug` deben ser unicos; se usan para las URLs de los proyectos.
- El campo `active` en modelos principales permite ocultar contenido sin eliminarlo de la base de datos.
- Los iconos se definen como **SVG inline** directamente en los campos de texto de los modelos.