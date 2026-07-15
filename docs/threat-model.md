# Modelo de amenazas inicial

## Activos protegidos

- credenciales, sesiones y datos personales;
- información comercial de cada organización;
- integridad de diagnósticos y eventos de auditoría;
- secretos de despliegue y cadena de suministro;
- disponibilidad de la aplicación y PostgreSQL.

## Límites de confianza

Internet no es confiable. El navegador, Django, PostgreSQL, GitHub Actions y el futuro proveedor de nube son zonas separadas. Toda entrada que cruza un límite debe validarse y toda identidad debe autorizarse nuevamente en el servidor.

## Riesgos prioritarios y controles

| Riesgo | Control actual | Próximo control |
| --- | --- | --- |
| Acceso entre empresas | Membresías y roles explícitos | Pruebas de aislamiento por organización |
| Robo de sesión | CSRF, cookies seguras y HTTPS en producción | MFA para cuentas privilegiadas |
| Inyección o datos inválidos | ORM y formularios de Django | Validación central de casos de uso |
| Fuga de secretos | Variables de entorno, `.gitignore` y Gitleaks | Gestor de secretos y OIDC |
| Dependencia comprometida | Dependabot, `pip-audit` y Dependency Review | SBOM firmado y attestations |
| Cambio sin trazabilidad | Eventos de auditoría | Correlación por solicitud y alertas |
| Indisponibilidad | Health check y reinicio de contenedores | Métricas, alertas y runbooks |

## Reglas de diseño

- denegar por defecto y otorgar el permiso mínimo;
- nunca confiar en un identificador de organización enviado por el cliente;
- no registrar contraseñas, tokens ni contenido sensible;
- conservar eventos de auditoría como solo lectura;
- revisar este documento cuando aparezca un nuevo flujo, integración o dato sensible.
