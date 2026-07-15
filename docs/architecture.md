# Arquitectura de Nexo Norte

## Objetivo

Nexo Norte será una plataforma multiempresa para acompañar a pequeños negocios en ventas, inventario y seguridad operativa. La base actual prioriza módulos pequeños, límites claros y evolución segura.

## Capas

1. **Presentación:** plantillas en `templates/` y activos en `static/`.
2. **Aplicación:** vistas, formularios y casos de uso dentro de cada app.
3. **Dominio:** modelos y reglas de `accounts`, `organizations`, `diagnostics` y `audit`.
4. **Infraestructura:** PostgreSQL, Gunicorn, WhiteNoise, Docker y GitHub Actions.

Las apps no se concentran en un núcleo único. Cada dominio conserva sus modelos, migraciones, administración y pruebas. `config/` solo compone la aplicación y sus entornos.

## Entornos

- `config.settings.local`: desarrollo cómodo, con SQLite si no se configura PostgreSQL.
- `config.settings.test`: pruebas deterministas; CI usa PostgreSQL real.
- `config.settings.production`: secretos obligatorios, HTTPS, cookies seguras y HSTS.

ASGI y WSGI apuntan a producción por defecto. `manage.py` usa local para reducir errores durante el desarrollo.

## Dominios actuales

- **Accounts:** usuario personalizado desde el inicio para evitar migraciones destructivas futuras.
- **Organizations:** empresas y membresías con roles explícitos.
- **Audit:** eventos inmutables para trazabilidad administrativa.
- **Diagnostics:** solicitudes comerciales recibidas desde la landing.
- **Monitoring:** salud del proceso y conexión a base de datos.
- **Website:** navegación y contenido público.

## Flujo de entrega

Cada pull request ejecuta formato, lint, tipado, migraciones, pruebas con cobertura, auditoría de dependencias, configuración de despliegue y construcción reproducible del contenedor. CodeQL, Gitleaks, Dependabot y Dependency Review agregan controles sobre código, secretos y cadena de suministro.

## Próximas decisiones

- API versionada y autenticación para el portal privado.
- permisos por organización en cada caso de uso;
- cola de tareas para trabajos largos;
- almacenamiento de archivos externo;
- observabilidad con métricas, logs estructurados y trazas;
- despliegue con OIDC y entornos protegidos.
