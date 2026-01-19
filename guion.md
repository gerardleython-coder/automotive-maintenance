# Guía Explicativa del Proyecto: Automotive - Gestión de Flota y Mantenimiento

---

## 1. Introducción y Objetivo

Este documento explica paso a paso el sistema "Automotive: Gestión de Flota y Mantenimiento" desarrollado como reto parcial, cumpliendo estrictamente TDD, Arquitectura Limpia y principios SOLID. Aquí encontrarás la arquitectura, patrones, reglas de negocio, evidencias de buenas prácticas y referencias directas a los archivos y módulos relevantes.


## 2. Tipo de Arquitectura y Tecnologías Usadas

### Arquitectura Limpia (Clean Architecture)
El proyecto implementa **Arquitectura Limpia**, que separa el sistema en capas independientes para facilitar la mantenibilidad, escalabilidad y testeo. Las dependencias siempre apuntan hacia el dominio, permitiendo que la lógica de negocio sea independiente de frameworks, bases de datos y detalles externos.

**Características principales:**

**Estructura de carpetas:**
```
src/
├── domain/            # Entidades, excepciones, contratos, estrategias
├── application/       # Casos de uso, lógica de negocio
├── infrastructure/    # Implementaciones concretas (DB, repositorios, observadores)
└── web/               # API REST (FastAPI), dependencias
```

### Relación con Arquitectura Hexagonal
La **Arquitectura Hexagonal** (Ports and Adapters) es un enfoque muy similar, donde el núcleo de la aplicación interactúa con el exterior a través de puertos (interfaces) y adaptadores (implementaciones concretas). En este proyecto, la presencia de interfaces en `domain/ports` y adaptadores en `infrastructure/repositories` y `infrastructure/observers` refleja este patrón.

Sin embargo, la organización y documentación siguen el estándar de **Arquitectura Limpia**, que prioriza capas concéntricas y dependencias hacia el dominio. Por lo tanto, el sistema es compatible con ambos enfoques, pero se presenta y explica como Clean Architecture.

**Ejemplo en el código:**
- Puertos (interfaces): [vehicle_repository.py](src/domain/ports/vehicle_repository.py), [alert_repository.py](src/domain/ports/alert_repository.py)
- Adaptadores: [sqlite_vehicle_repository.py](src/infrastructure/repositories/sqlite_vehicle_repository.py), [maintenance_alert_observer.py](src/infrastructure/observers/maintenance_alert_observer.py)

- **Backend:** Python 3.11+ con FastAPI
- **Base de datos:** SQLite
- **Frontend:** JavaScript (JS) puro
- **Pruebas:** pytest, pytest-cov
- **Automatización:** PowerShell (start_servers.ps1)
- **CI/CD:** GitHub Actions
- **Documentación:** Markdown (.md)

**Referencias de archivos:**
- Backend principal: [main.py](src/web/main.py)
- Modelos y lógica de dominio: [vehicle.py](src/domain/entities/vehicle.py), [maintenance_alert.py](src/domain/entities/maintenance_alert.py)
- Persistencia: [sqlite_vehicle_repository.py](src/infrastructure/repositories/sqlite_vehicle_repository.py)
- Frontend: [app.js](frontend/js/app.js), [api.js](frontend/js/api.js)
- Pruebas: [tests/](tests)
- CI/CD: [.github/workflows/ci.yml](.github/workflows/ci.yml)
- Script de automatización: [start_servers.ps1](start_servers.ps1)
- Documentación: [README.md](README.md), [reto.md](reto.md)


El proyecto sigue **Arquitectura Limpia** (Clean Architecture), separando responsabilidades en capas:

- **Domain**: Entidades, excepciones, interfaces y estrategias ([src/domain](src/domain)).
- **Application**: Casos de uso y lógica de negocio ([src/application](src/application)).
- **Infrastructure**: Implementaciones concretas (DB, repositorios, observadores) ([src/infrastructure](src/infrastructure)).
- **Web/API**: Endpoints y dependencias ([src/web](src/web)).

Referencia: [reto.md](reto.md)

---

## 3. Principios SOLID Aplicados

- **SRP (Single Responsibility Principle)**: Cada clase tiene una única responsabilidad. Ejemplo: [vehicle.py](src/domain/entities/vehicle.py) solo modela el vehículo.
- **OCP (Open/Closed Principle)**: Las reglas de mantenimiento se extienden con nuevas estrategias sin modificar código existente ([maintenance_strategy.py](src/domain/strategies/maintenance_strategy.py)).
- **LSP (Liskov Substitution Principle)**: Las implementaciones cumplen los contratos definidos en interfaces ([vehicle_repository.py](src/domain/ports/vehicle_repository.py)).
- **ISP (Interface Segregation Principle)**: Interfaces específicas y pequeñas ([alert_repository.py](src/domain/ports/alert_repository.py)).
- **DIP (Dependency Inversion Principle)**: La lógica depende de abstracciones, no implementaciones concretas ([use_cases](src/application/use_cases), [repositories](src/infrastructure/repositories)).

---

## 4. Patrones de Diseño

### Observer
- Implementado para notificar cuando un vehículo alcanza umbrales de kilometraje.
- Código: [observer.py](src/domain/ports/observer.py), [maintenance_alert_observer.py](src/infrastructure/observers/maintenance_alert_observer.py)

### Strategy
- Define reglas de mantenimiento extensibles.
- Código: [maintenance_strategy.py](src/domain/strategies/maintenance_strategy.py), [basic_maintenance_strategy.py](src/domain/strategies/basic_maintenance_strategy.py), [major_maintenance_strategy.py](src/domain/strategies/major_maintenance_strategy.py), [critical_threshold_strategy.py](src/domain/strategies/critical_threshold_strategy.py)

---

## 5. Reglas de Negocio

### Gestión de Vehículos
- Registrar vehículos: `id`, `placa`, `modelo`, `kilometraje_actual` ([register_vehicle_use_case.py](src/application/use_cases/register_vehicle_use_case.py)).
- Actualizar kilometraje ([update_vehicle_mileage_use_case.py](src/application/use_cases/update_vehicle_mileage_use_case.py)):
  - Nuevo kilometraje > actual
  - No negativo
  - No cero si ya tiene registro
  - No exceder 1,000,000 km
  - No incrementar más de 50,000 km de una vez

### Sistema de Alertas
- Notifica cuando:
  - Múltiplo de 10,000 km
  - Umbral crítico (100,000 km)
- Registro de alertas: `id`, `vehiculo_id`, `tipo_alerta`, `kilometraje`, `fecha` ([maintenance_alert.py](src/domain/entities/maintenance_alert.py), [sqlite_alert_repository.py](src/infrastructure/repositories/sqlite_alert_repository.py))

### Reglas de Mantenimiento
- **Básico**: cada 10,000 km ([basic_maintenance_strategy.py](src/domain/strategies/basic_maintenance_strategy.py))
- **Mayor**: cada 50,000 km ([major_maintenance_strategy.py](src/domain/strategies/major_maintenance_strategy.py))
- **Crítico**: >100,000 km ([critical_threshold_strategy.py](src/domain/strategies/critical_threshold_strategy.py))

---

## 6. TDD Estricto y Cobertura de Pruebas

- Ciclo RED → GREEN → REFACTOR evidenciado en el historial de Git.
- Pruebas unitarias y de integración en [tests/](tests):
  - Dominio: [test_vehicle.py](tests/domain/test_vehicle.py), [test_maintenance_alert.py](tests/domain/test_maintenance_alert.py)
  - Casos de uso: [test_register_vehicle_use_case.py](tests/application/test_register_vehicle_use_case.py), etc.
  - Infraestructura: [test_sqlite_vehicle_repository.py](tests/infrastructure/test_sqlite_vehicle_repository.py)
  - Integración: [test_api_endpoints.py](tests/integration/test_api_endpoints.py)
- Cobertura >95% con `pytest --cov=src`

---

## 7. Persistencia y API

- Persistencia con SQLite: [connection.py](src/infrastructure/database/connection.py), [models.py](src/infrastructure/database/models.py)
- Repositorios: [sqlite_vehicle_repository.py](src/infrastructure/repositories/sqlite_vehicle_repository.py), [sqlite_alert_repository.py](src/infrastructure/repositories/sqlite_alert_repository.py)
- API REST con FastAPI: [main.py](src/web/main.py), [dependencies.py](src/web/dependencies.py)

---

## 8. Frontend y Pruebas de API

- Frontend JS: [app.js](frontend/js/app.js), [api.js](frontend/js/api.js)
- Colección Postman para pruebas de API: [postman/](postman)
- Documentación de pruebas: [README.md](README.md), [reto.md](reto.md)

---

## 9. Automatización y CI/CD

- Script PowerShell para iniciar backend y frontend: [start_servers.ps1](start_servers.ps1)
- Pipeline CI/CD con GitHub Actions: [.github/workflows/ci.yml](.github/workflows/ci.yml)

---

## 10. Documentación y Recursos

- Documentación técnica y de usuario: [README.md](README.md), [reto.md](reto.md), [USER_STORIES.md](USER_STORIES.md), [DESIGN.md](docs/DESIGN.md)
- Instrucciones de instalación y ejecución en [README.md](README.md)

---

## 11. Buenas Prácticas y Extensibilidad

- Nombres claros, código limpio, commits atómicos.
- El sistema permite agregar nuevas reglas de mantenimiento sin modificar código existente (OCP).
- Validaciones y excepciones bien definidas ([exceptions](src/domain/exceptions)).

---

## 12. Ejemplo de Presentación Oral

1. Explicar la arquitectura y capas con referencias a los archivos.
2. Mostrar cómo se aplican los principios SOLID y los patrones.
3. Detallar las reglas de negocio y validaciones.
4. Evidenciar el ciclo TDD y la cobertura de pruebas.
5. Demostrar la API y el frontend funcionando.
6. Resaltar la automatización y CI/CD.
7. Concluir con buenas prácticas y extensibilidad.

---

**¡Listo para presentar y defender el reto!** 🚗⚙️
