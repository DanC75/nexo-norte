# Nexo Norte

Landing y base operativa de una empresa ficticia que ayuda a pequeños negocios a conectar ventas, inventario y seguridad.

La primera versión utiliza la dirección visual **Impulso Norte**: una identidad tecnológica de alto contraste, con azul eléctrico y verde lima, diseñada para sentirse enérgica sin perder claridad.

## Arquitectura

- Django 6 y Python 3.14
- PostgreSQL 17
- Plantillas HTML, CSS y JavaScript progresivo
- Gunicorn y WhiteNoise
- Docker y Docker Compose
- GitHub Actions, CodeQL y Dependabot

El código está organizado por dominio:

- `config/settings/`: configuración separada para local, pruebas y producción.
- `apps/accounts/`: identidad y usuario extensible.
- `apps/organizations/`: empresas, membresías y roles.
- `apps/audit/`: trazabilidad de eventos relevantes.
- `apps/website/`: experiencia pública y composición de la landing.
- `apps/diagnostics/`: formulario, modelo y administración de solicitudes.
- `apps/monitoring/`: endpoint de salud para operación y contenedores.
- `templates/` y `static/`: presentación separada de la lógica de negocio.

La explicación completa está en [`docs/architecture.md`](docs/architecture.md).

## Funcionalidades actuales

- Landing responsive y accesible.
- Explicación de ventas, inventario y seguridad.
- Formulario de diagnóstico almacenado en la base de datos.
- Administración de solicitudes desde Django Admin.
- Endpoint de salud en `/health/`.
- Controles de seguridad configurables para producción.
- Pruebas automatizadas y validación en CI.

## Inicio rápido con Docker

1. Copia `.env.example` como `.env` y cambia los secretos.
2. Construye y levanta los servicios:

   ```powershell
   docker compose up --build
   ```

3. Abre `http://localhost:8000`.

La aplicación espera a que PostgreSQL esté saludable, aplica las migraciones y arranca el servidor automáticamente.

## Desarrollo local sin Docker

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
```

Cuando no se define `POSTGRES_HOST`, Django utiliza SQLite solamente para facilitar pruebas locales. Docker y CI verifican el funcionamiento real con PostgreSQL.

## Comandos de verificación

```powershell
ruff format --check .
ruff check .
mypy apps config
python manage.py makemigrations --check --dry-run --settings=config.settings.test
pytest --cov=apps
pip-audit -r requirements-dev.txt --strict
python manage.py check --deploy --settings=config.settings.production
docker compose config
docker build -t nexo-norte:local .
```

## Variables de entorno

| Variable | Propósito |
| --- | --- |
| `DJANGO_SECRET_KEY` | Firma criptográfica de Django. Nunca debe versionarse. |
| `DJANGO_DEBUG` | Activa información de desarrollo. Debe ser `false` en producción. |
| `DJANGO_ALLOWED_HOSTS` | Dominios autorizados, separados por comas. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Orígenes HTTPS confiables para formularios. |
| `POSTGRES_DB` | Nombre de la base de datos. |
| `POSTGRES_USER` | Usuario de PostgreSQL. |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL. |
| `POSTGRES_HOST` | Host del servidor de base de datos. |
| `POSTGRES_PORT` | Puerto de PostgreSQL. |

## Flujo de Git

- `main` conserva versiones estables.
- El desarrollo se realiza en ramas `codex/<tema>`.
- Los commits siguen Conventional Commits: `feat:`, `fix:`, `test:`, `docs:`, `chore:` y `ci:`.
- Cada cambio llega a `main` mediante un pull request validado por CI.

## Seguridad

- Los secretos se suministran por variables de entorno.
- `.env` y las bases locales están excluidos de Git.
- Las solicitudes POST usan protección CSRF.
- Las cookies seguras, HSTS y redirección HTTPS se activan fuera de desarrollo.
- CodeQL analiza el código y Dependabot vigila dependencias y acciones.
- Gitleaks busca secretos y Dependency Review bloquea dependencias vulnerables en pull requests.
- La cobertura mínima exigida es 80 % y cada cambio pasa formato, lint, tipado y pruebas.

Consulta [SECURITY.md](SECURITY.md) para reportar vulnerabilidades y
[`docs/threat-model.md`](docs/threat-model.md) para conocer las amenazas consideradas.
