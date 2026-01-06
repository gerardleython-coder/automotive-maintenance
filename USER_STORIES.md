# Historias de Usuario - Sistema de Gestión de Flota

## HU-001: Registrar kilometraje de vehículos

**Como** gestor de flota  
**Quiero** registrar el kilometraje de mis vehículos  
**Para** recibir alertas de mantenimiento preventivo

### Criterios de Aceptación

#### Escenario 1: Registro de kilometraje exitoso y disparo de alerta

```gherkin
Given un vehículo con ID 'V-123' y kilometraje actual de 5,000 km
And una regla de mantenimiento cada 10,000 km
When registro un nuevo kilometraje de 10,001 km
Then el kilometraje del vehículo debe actualizarse a 10,001 km
And se debe generar una alerta de mantenimiento automáticamente
```

#### Escenario 2: Error por kilometraje menor al actual (Anti-Happy Path)

```gherkin
Given un vehículo con kilometraje de 5,000 km
When intento registrar un kilometraje de 4,000 km
Then el sistema debe lanzar una excepción de negocio 'InvalidMileageException'
```

#### Escenario 3: Validaciones adicionales de kilometraje

```gherkin
Given un vehículo registrado
When intento actualizar el kilometraje con un valor inválido
Then el sistema debe rechazar la operación

Ejemplos de valores inválidos:
- Kilometraje negativo
- Kilometraje que excede 1,000,000 km
- Incremento mayor a 50,000 km de una sola vez
```

## Reglas de Negocio

- RN-001: El kilometraje debe ser siempre mayor al valor actual
- RN-002: El kilometraje no puede ser negativo
- RN-003: El kilometraje máximo permitido es 1,000,000 km
- RN-004: El incremento máximo permitido es 50,000 km
- RN-005: Se genera alerta cada 10,000 km (mantenimiento básico)
- RN-006: Se genera alerta cada 50,000 km (mantenimiento mayor)
- RN-007: Se genera alerta crítica al superar 100,000 km
