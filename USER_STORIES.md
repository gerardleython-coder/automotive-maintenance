# Historias de Usuario - Sistema de Gestión de Flota

## HU-001: Registro automático de kilometraje de vehículos

**Como** gestor de flota
**Quiero** que el sistema registre automáticamente el kilometraje de mis vehículos
**Para** recibir alertas oportunas de mantenimiento preventivo, mayor y crítico

### Criterios de Aceptación

#### Escenario 1: Registro automático exitoso y generación de alerta

```gherkin
Given un vehículo con ID 'V-123' y kilometraje actual de 5,000 km
And existen reglas de mantenimiento cada 10,000 km
When registro un nuevo kilometraje de 10,001 km
Then el kilometraje del vehículo debe actualizarse a 10,001 km
And se debe generar una alerta de mantenimiento automáticamente
```

#### Escenario 2: Error por kilometraje menor al actual (Anti-Happy Path)

```gherkin
Given un vehículo con kilometraje actual de 5,000 km
When intento registrar un kilometraje de 4,000 km
Then el sistema debe lanzar una excepción de negocio 'InvalidMileageException'
```

#### Escenario 3: Validación de valores inválidos de kilometraje

```gherkin
Given un vehículo con kilometraje actual registrado
When intento actualizar el kilometraje con un valor inválido
Then el sistema debe rechazar la operación

Ejemplos de valores inválidos:
- Kilometraje negativo
- Kilometraje superior a 1,000,000 km
- Incremento mayor a 50,000 km respecto al último registro
```

#### Escenario 4: Registro sin generación de alerta

```gherkin
Given un vehículo con kilometraje actual de 5,000 km
When registro un nuevo kilometraje de 8,000 km
Then el kilometraje del vehículo debe actualizarse a 8,000 km
And no se debe generar ninguna alerta de mantenimiento
```

---

## HU-002: Registro de nuevos vehículos en la flota

**Como** gestor de flota
**Quiero** registrar nuevos vehículos en el sistema
**Para** poder gestionar su mantenimiento preventivo desde el inicio de su operación

### Criterios de Aceptación

#### Escenario 1: Registro exitoso de vehículo nuevo

```gherkin
Given que no existe un vehículo con ID 'V-456' en el sistema
And no existe un vehículo con placa 'XYZ-789'
When registro un nuevo vehículo con los siguientes datos:
  | Campo               | Valor        |
  | ID                  | V-456        |
  | Placa               | XYZ-789      |
  | Modelo              | Honda Civic  |
  | Kilometraje Inicial | 0            |
Then el vehículo debe ser registrado exitosamente
And debe estar disponible para consulta posterior
```

#### Escenario 2: Error por ID duplicado (Anti-Happy Path)

```gherkin
Given que existe un vehículo con ID 'V-123' en el sistema
When intento registrar un nuevo vehículo con ID 'V-123'
Then el sistema debe lanzar una excepción 'DuplicateVehicleException'
And el mensaje debe indicar "Ya existe un vehículo con ID V-123"
```

#### Escenario 3: Error por placa duplicada (Anti-Happy Path)

```gherkin
Given que existe un vehículo con placa 'ABC-123'
When intento registrar un nuevo vehículo con placa 'ABC-123'
Then el sistema debe lanzar una excepción 'DuplicatePlateException'
And el mensaje debe indicar "Ya existe un vehículo con placa ABC-123"
```

#### Escenario 4: Validación de datos obligatorios

```gherkin
When intento registrar un vehículo con datos incompletos
Then el sistema debe rechazar la operación

Ejemplos de datos inválidos:
- ID vacío o nulo
- Placa vacía o nula
- Modelo vacío o nulo
- Formato de placa inválido (debe ser XXX-### o XXX-####)
```

#### Escenario 5: Validación de kilometraje inicial

```gherkin
Given datos válidos para un nuevo vehículo
When intento registrar el vehículo con kilometraje inicial inválido
Then el sistema debe rechazar la operación

Ejemplos de kilometraje inicial inválido:
- Kilometraje negativo
- Kilometraje superior a 500,000 km (vehículos usados)
```

#### Escenario 6: Registro de vehículo usado con kilometraje inicial

```gherkin
Given que no existe un vehículo con ID 'V-789'
When registro un vehículo usado con kilometraje inicial de 25,000 km
Then el vehículo debe ser registrado exitosamente
And el kilometraje actual debe ser 25,000 km
And no se deben generar alertas automáticas en el registro inicial
```

---

## Reglas de Negocio

- RN-001: El kilometraje debe ser siempre mayor al valor actual
- RN-002: El kilometraje no puede ser negativo
- RN-003: El kilometraje máximo permitido es 1,000,000 km
- RN-004: El incremento máximo permitido es 50,000 km
- RN-005: Se genera alerta cada 10,000 km (mantenimiento básico)
- RN-006: Se genera alerta cada 50,000 km (mantenimiento mayor)
- RN-007: Se genera alerta crítica al superar 100,000 km
- RN-008: El ID del vehículo debe ser único en el sistema
- RN-009: La placa del vehículo debe ser única en el sistema
- RN-010: El formato de placa debe seguir el estándar colombiano (XXX-### o XXX-####)
- RN-011: El ID del vehículo debe seguir el formato V-XXX
- RN-012: El modelo del vehículo no puede estar vacío
- RN-013: El kilometraje inicial debe estar entre 0 y 500,000 km
- RN-014: No se generan alertas durante el registro inicial del vehículo

---