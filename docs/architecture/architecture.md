# Arquitectura del Sistema: Automotive - Gestión de Flota y Mantenimiento

---

## 1. Visión General

Este documento describe la arquitectura del sistema, sus capas, componentes principales, patrones aplicados y el flujo de interacción entre módulos. Incluye una estructura para agregar diagramas visuales y explicaciones detalladas.

---

## 2. Diagrama General de Capas

![Diagrama de Capas](diagrama-capas.png)
*Coloca aquí un diagrama visual que muestre las capas: Domain, Application, Infrastructure, Web/API, Frontend.*

---

## 3. Estructura de Carpetas y Componentes

```
project-root/
├── src/
│   ├── domain/            # Entidades, excepciones, interfaces, estrategias
│   ├── application/       # Casos de uso, lógica de negocio
│   ├── infrastructure/    # DB, repositorios, observadores
│   └── web/               # API REST (FastAPI), dependencias
├── frontend/              # JS, HTML, CSS, docs de frontend
├── tests/                 # Pruebas unitarias, integración
├── docs/
│   ├── architecture/      # Diagramas y documentación de arquitectura
│   ├── design/            # Mockups, diseño visual
│   └── postman/           # Colección y docs de pruebas API
├── .github/               # CI/CD workflows
├── start_servers.ps1      # Script de automatización
├── requirements.txt       # Dependencias Python
├── README.md              # Documentación principal
└── ...
```

---

## 4. Capas y Responsabilidades

### 4.1 Domain
- Entidades: [vehicle.py](../../src/domain/entities/vehicle.py), [maintenance_alert.py](../../src/domain/entities/maintenance_alert.py)
- Excepciones: [exceptions/](../../src/domain/exceptions)
- Interfaces (puertos): [ports/](../../src/domain/ports)
- Estrategias: [strategies/](../../src/domain/strategies)

### 4.2 Application
- Casos de uso: [use_cases/](../../src/application/use_cases)
- Orquestación de lógica de negocio

### 4.3 Infrastructure
- Persistencia: [database/](../../src/infrastructure/database), [repositories/](../../src/infrastructure/repositories)
- Observadores: [observers/](../../src/infrastructure/observers)

### 4.4 Web/API
- Endpoints REST: [main.py](../../src/web/main.py)
- Inyección de dependencias: [dependencies.py](../../src/web/dependencies.py)

### 4.5 Frontend
- JS: [app.js](../../frontend/js/app.js), [api.js](../../frontend/js/api.js)
- HTML/CSS: [index.html](../../frontend/index.html), [styles.css](../../frontend/css/styles.css)

---

## 5. Patrones de Diseño

- **Observer:** Notificación de alertas de mantenimiento ([observer.py](../../src/domain/ports/observer.py), [maintenance_alert_observer.py](../../src/infrastructure/observers/maintenance_alert_observer.py))
- **Strategy:** Reglas de mantenimiento extensibles ([maintenance_strategy.py](../../src/domain/strategies/maintenance_strategy.py), [basic_maintenance_strategy.py](../../src/domain/strategies/basic_maintenance_strategy.py), [major_maintenance_strategy.py](../../src/domain/strategies/major_maintenance_strategy.py), [critical_threshold_strategy.py](../../src/domain/strategies/critical_threshold_strategy.py))

---

## 6. Flujo de Datos y Dependencias

1. El usuario interactúa con el **Frontend** (JS/HTML) o la **API REST** (FastAPI).
2. Las solicitudes llegan a la capa **Web/API**, que delega en los **Casos de Uso** de la capa **Application**.
3. Los casos de uso utilizan entidades y estrategias del **Domain** y dependen de interfaces (puertos).
4. Las implementaciones concretas (repositorios, observadores) están en **Infrastructure** y se inyectan por dependencias.
5. Las alertas y actualizaciones se notifican usando el patrón Observer.
6. La persistencia se realiza en SQLite a través de los repositorios.

---

## 7. Extensibilidad y Buenas Prácticas

- El sistema permite agregar nuevas reglas de mantenimiento sin modificar el código existente (OCP).
- Las dependencias siempre apuntan hacia el dominio.
- Pruebas unitarias y de integración cubren >95% del código.
- CI/CD automatizado con GitHub Actions.
- Documentación y mockups en docs/design.

---

## 8. Estructura para Diagramas

- diagrama-capas.png: Diagrama de capas generales.
- diagrama-flujo.png: Diagrama de flujo de datos.
- diagrama-componentes.png: Diagrama de componentes y dependencias.

*Puedes agregar imágenes en esta carpeta y referenciarlas en este archivo para futuras presentaciones.*

---

**Fin del documento de arquitectura.**
