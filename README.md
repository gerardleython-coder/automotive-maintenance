# Automotive: Gestión de Flota y Mantenimiento

Sistema de gestión de flota de vehículos con monitoreo de kilometraje y alertas automáticas de mantenimiento.

## Descripción

Sistema que implementa **Arquitectura Hexagonal** con **TDD estricto** para gestionar una flota de vehículos, monitoreando el kilometraje y generando alertas automáticas cuando se requiere mantenimiento.

## Características

- ✓ Gestión de vehículos y kilometraje
- ✓ Sistema de alertas automáticas (Patrón Observer)
- ✓ Reglas de mantenimiento extensibles (Strategy Pattern)
- ✓ Arquitectura Limpia (Hexagonal)
- ✓ TDD estricto con cobertura >= 70%
- ✓ Principios SOLID

## Requisitos

- Python 3.11+
- pip

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/gerardleython-coder/automotive-maintenance.git
cd automotive-maintenance

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución de Pruebas

```bash
# Ejecutar todos los tests con cobertura
pytest --cov=src --cov-report=term-missing

# Ejecutar tests de dominio
pytest tests/domain/ -v

# Ejecutar tests de integración
pytest tests/integration/ -v
```

## Arquitectura

```
src/
├── domain/            # Entidades, excepciones, contratos (ports)
├── application/       # Casos de uso, lógica de aplicación
├── infrastructure/    # Implementaciones concretas (repositories, observers)
└── web/              # API REST (FastAPI)
```

## Patrones de Diseño

- **Observer Pattern**: Sistema de eventos para alertas de mantenimiento
- **Strategy Pattern**: Reglas de mantenimiento extensibles
- **Repository Pattern**: Abstracción de persistencia (DIP)

## Desarrollo

Este proyecto sigue **TDD estricto**. El historial de Git muestra el ciclo RED → GREEN → REFACTOR.

Ver [USER_STORIES.md](USER_STORIES.md) para historias de usuario y criterios de aceptación.

## CI/CD

GitHub Actions ejecuta automáticamente:
- Linting con Ruff
- Tests con pytest
- Validación de cobertura >= 70%
