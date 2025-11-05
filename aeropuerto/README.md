# Sistema de Gestión de Aeropuerto ✈️ - Python

## Descripción del Proyecto

Sistema integral para la gestión de operaciones de un aeropuerto, desarrollado en **Python 3.8+**, implementando **4 patrones de diseño**: Singleton, Strategy, Observer y Factory.

## 🎯 Patrones de Diseño Implementados

### 1. **Singleton** 
- **Ubicación**: `src/servicio/gestor_aeropuerto.py`
- **Propósito**: Garantiza que solo exista una instancia del gestor principal del aeropuerto
- **Implementación**: Metaclase `SingletonMeta`

### 2. **Strategy**
- **Ubicación**: `src/patrones/strategy.py` + `src/modelo/reserva.py`
- **Propósito**: Cálculo dinámico de precios según temporada (alta, media, baja)
- **Estrategias**: `PrecioTemporadaAlta`, `PrecioTemporadaMedia`, `PrecioTemporadaBaja`

### 3. **Observer**
- **Ubicación**: `src/patrones/observer.py` + `src/modelo/vuelo.py`
- **Propósito**: Notificaciones automáticas de cambios de estado en vuelos
- **Observers**: `NotificadorEmail`, `NotificadorSMS`, `NotificadorApp`, `RegistroEventos`

### 4. **Factory**
- **Ubicación**: `src/patrones/factory.py` + gestores
- **Propósito**: Creación controlada de objetos (vuelos, reservas)
- **Factories**: `FactoriaVuelos`, `FactoriaReservas`

## 📁 Estructura del Proyecto

```
aeropuerto/
├── src/
│   ├── __init__.py
│   ├── modelo/
│   │   ├── __init__.py
│   │   ├── enums.py                    # Enumeraciones del dominio
│   │   ├── aerolinea.py                # Clase Aerolinea
│   │   ├── avion.py                    # Clase Avion
│   │   ├── gate.py                     # Clase Gate
│   │   ├── equipaje.py                 # Clase Equipaje
│   │   ├── tripulacion.py              # Clase Tripulacion
│   │   ├── pasajero.py                 # Clase Pasajero
│   │   ├── vuelo.py                    # Clase Vuelo (con Observer)
│   │   └── reserva.py                  # Clase Reserva (con Strategy)
│   ├── excepciones/
│   │   ├── __init__.py
│   │   └── excepciones_aeropuerto.py   # 11 excepciones personalizadas
│   ├── patrones/
│   │   ├── __init__.py
│   │   ├── singleton.py                # Patrón Singleton
│   │   ├── strategy.py                 # Patrón Strategy
│   │   ├── observer.py                 # Patrón Observer
│   │   └── factory.py                  # Patrón Factory
│   ├── servicio/
│   │   ├── __init__.py
│   │   ├── gestor_vuelos.py            # Gestor de vuelos
│   │   ├── gestor_pasajeros.py         # Gestor de pasajeros
│   │   ├── gestor_reservas.py          # Gestor de reservas
│   │   └── gestor_aeropuerto.py        # Gestor principal (Singleton)
│   └── main.py                         # Programa principal
├── requirements.txt
├── README.md
└── USER_STORIES.md
```

## 🚀 Funcionalidades Principales

### 1. Gestión de Vuelos
- Creación y registro de vuelos (nacionales/internacionales)
- Asignación de aviones y tripulación
- Control de capacidad y disponibilidad
- Gestión de horarios de salida y llegada
- Estados: PROGRAMADO, ABORDANDO, DESPEGADO, ATERRIZADO, CANCELADO, RETRASADO
- **Usa patrón Observer para notificar cambios**

### 2. Gestión de Pasajeros
- Registro de pasajeros en el sistema
- Validación de documentos (pasaporte, DNI)
- Historial de vuelos por pasajero
- Gestión de programas de viajero frecuente
- Verificación de restricciones de edad

### 3. Gestión de Reservas
- Reserva de asientos en vuelos
- Selección de clase (ECONOMICA, EJECUTIVA, PRIMERA_CLASE)
- **Usa patrón Strategy para cálculo de precios**
- Gestión de equipaje (facturado y de mano)
- Check-in online
- Cancelación y modificación de reservas

### 4. Gestión de Aeronaves
- Registro de aviones por aerolínea
- Control de capacidad por clase
- Estado de mantenimiento
- Tipos: COMERCIAL, CARGA, PRIVADO
- **Usa patrón Factory para creación**

### 5. Gestión de Infraestructura
- Asignación de gates de embarque
- Control de ocupación de puertas
- Gestión de terminales (Nacional/Internacional)

### 6. Gestión de Tripulación
- Registro de pilotos y personal de cabina
- Asignación a vuelos
- Control de horas de vuelo (límites de fatiga)
- Certificaciones y licencias

## 🔧 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

```bash
# 1. Clonar o descargar el proyecto
cd aeropuerto

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# 3. Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Ejecución

### Ejecutar el Programa Principal

```bash
# Desde la raíz del proyecto
python src/main.py

# O si estás en src/
python main.py
```

```

## 💻 Ejemplo de Uso

```python
from src.servicio.gestor_aeropuerto import GestorAeropuerto
from src.modelo.aerolinea import Aerolinea
from src.modelo.avion import Avion
from src.modelo.pasajero import Pasajero
from src.modelo.gate import Gate
from datetime import datetime, timedelta

# Inicializar el sistema (Singleton)
gestor = GestorAeropuerto()

# Crear aerolínea
aerolinea = Aerolinea("AA", "American Airlines", "Estados Unidos")

# Registrar avión
avion = Avion("N12345", "COMERCIAL", aerolinea)
avion.capacidad_economica = 150
avion.capacidad_ejecutiva = 30
avion.capacidad_primera = 20

# Crear vuelo (Factory)
fecha_salida = datetime.now() + timedelta(hours=5)
vuelo = gestor.crear_vuelo("AA1001", "Buenos Aires", "Miami", fecha_salida)
vuelo.avion = avion

# Asignar gate
gate = Gate("A15", "INTERNACIONAL")
vuelo.asignar_gate(gate)

# Registrar pasajero
pasajero = Pasajero("Juan Pérez", "AB123456", "PASAPORTE")

# Hacer reserva (Strategy aplicado para precio)
try:
    reserva = gestor.crear_reserva(vuelo, pasajero, "ECONOMICA")
    print(f"✓ Reserva creada: {reserva.codigo_reserva}")
    print(f"  Precio: ${reserva.precio}")
    
    # Agregar equipaje
    reserva.equipaje.agregar_maleta_bodega(20.5)
    reserva.equipaje.agregar_maleta_bodega(22.0)
    
    # Hacer check-in
    gestor.hacer_checkin(reserva)
    print(f"✓ Check-in exitoso. Asiento: {reserva.asiento_asignado}")
    
except Exception as e:
    print(f"✗ Error: {e}")
```

## 📋 Reglas de Negocio

### Reservas
1. No se pueden hacer reservas en vuelos llenos
2. Check-in disponible entre 24 horas y 45 minutos antes del vuelo
3. Se permite sobreventa del 10% en clase económica
4. Límites de equipaje por clase:
   - Económica: 2 maletas de 23kg
   - Ejecutiva: 3 maletas de 32kg
   - Primera: 3 maletas de 32kg

### Vuelos
1. Un vuelo debe tener tripulación completa para despegar
2. Los vuelos internacionales requieren pasaporte válido
3. Menores de 12 años no pueden viajar solos en vuelos internacionales
4. Un gate solo puede ser asignado a un vuelo a la vez

### Pasajeros
1. Documento de identidad obligatorio y válido
2. Los menores de 18 años requieren autorización para viajar solos
3. Viajeros frecuentes con más de 50,000 millas obtienen prioridad

### Tripulación
1. Piloto debe tener licencia vigente
2. Máximo 9 horas de vuelo por día
3. Mínimo 12 horas de descanso entre vuelos
4. Ratio: 1 tripulante de cabina por cada 50 pasajeros

## 🎨 Excepciones Personalizadas (11)

El sistema maneja 11 tipos de excepciones específicas del dominio:

1. **VueloLlenoException**: Vuelo sin capacidad disponible
2. **VueloNoEncontradoException**: Vuelo no existe en el sistema
3. **PasajeroNoEncontradoException**: Pasajero no registrado
4. **ReservaNoEncontradaException**: Código de reserva inválido
5. **DocumentoInvalidoException**: Documento vencido o tipo incorrecto
6. **CheckInNoDisponibleException**: Fuera de ventana de check-in
7. **GateNoDisponibleException**: Gate ocupado o no disponible
8. **EquipajeExcedidoException**: Peso o cantidad de maletas excedido
9. **VueloYaDespegadoException**: Operación no permitida en vuelo en curso
10. **EdadInsuficienteException**: Menor sin autorización o edad mínima
11. **TripulacionIncompletaException**: No hay suficiente personal asignado

## 📊 Salida del Main

Cuando ejecutes `python src/main.py`, verás:

```
============================================================
   SISTEMA DE GESTIÓN DE AEROPUERTO
============================================================

--- Inicializando Sistema ---
✓ Aerolínea registrada: American Airlines (AA)
✓ Avión registrado: N12345 - Capacidad: 200 pasajeros
✓ Vuelo creado: AA1001 (Buenos Aires → Miami)
✓ Gate asignado: A15 - Terminal INTERNACIONAL
✓ Tripulación completa asignada: 5 miembros

--- Registro de Pasajero ---
✓ Pasajero registrado: Juan Pérez (PASAPORTE: AB123456)

--- Creando Reserva ---
✓ Reserva confirmada: RES001
✓ Clase: ECONOMICA
✓ Precio calculado (Strategy): $12,000.00

--- Agregando Equipaje ---
✓ Equipaje registrado: 20.5 kg
✓ Equipaje registrado: 22.0 kg
✓ Peso total: 42.5 kg

--- Realizando Check-In ---
✓ Check-in exitoso
✓ Asiento asignado: 15A
✓ Puerta de embarque: A15

--- NOTIFICACIONES (Observer Pattern) ---
📧 [EMAIL] Cambio de estado: ABORDANDO
📱 [SMS] Vuelo AA1001 - Abordaje iniciado
📲 [APP] Notificación push enviada

============================================================
   CASOS DE EXCEPCIÓN
============================================================

--- Intento: Reserva en vuelo lleno ---
✗ VueloLlenoException: El vuelo AA2050 está lleno...

--- Intento: Check-in muy temprano ---
✗ CheckInNoDisponibleException: El check-in solo está disponible...

[... 6 excepciones más demostradas ...]

============================================================
   ESTADÍSTICAS DEL SISTEMA
============================================================
Total de vuelos: 8
Total de pasajeros: 12
Total de reservas activas: 10
Ocupación promedio: 75%

✓ Demostración completada exitosamente
============================================================
```

## 📚 Documentación Adicional

- **USER_STORIES.md**: 11 historias de usuario con casos de prueba
- **RUBRICA_EVALUACION.md**: Criterios de evaluación (100 puntos)
- **RUBRICA_AUTOMATIZADA.md**: Script de evaluación automática

## 🛠️ Tecnologías

- **Python 3.8+**: Lenguaje de programación
- **datetime**: Manejo de fechas y horas
- **typing**: Type hints para mejor legibilidad
- **enum**: Enumeraciones tipadas

## 👥 Patrones de Diseño - Detalles de Implementación

### Singleton en GestorAeropuerto
```python
from patrones.singleton import SingletonMeta

class GestorAeropuerto(metaclass=SingletonMeta):
    def __init__(self):
        # Solo se ejecuta una vez
        self.vuelos = []
        self.pasajeros = []
        self.reservas = []

# Siempre retorna la misma instancia
gestor1 = GestorAeropuerto()
gestor2 = GestorAeropuerto()
assert gestor1 is gestor2  # True
```

### Strategy en Cálculo de Precios
```python
from patrones.strategy import PrecioTemporadaAlta, CalculadoraPrecio

# Cambiar estrategia dinámicamente
calculadora = CalculadoraPrecio(PrecioTemporadaAlta())
precio = calculadora.calcular(10000, "ECONOMICA", 6000)
# Aplica recargo del 50% en temporada alta
```

### Observer en Vuelos
```python
from patrones.observer import NotificadorEmail

# Vuelo hereda de Subject
vuelo = Vuelo("AA1001", "BUE", "MIA", fecha)

# Agregar observers
vuelo.agregar_observer(NotificadorEmail())
vuelo.agregar_observer(NotificadorSMS())

# Automáticamente notifica al cambiar estado
vuelo.cambiar_estado('RETRASADO')  # Envía notificaciones
```

### Factory para Creación
```python
from patrones.factory import FactoriaVuelos

# Crea el tipo correcto automáticamente
vuelo = FactoriaVuelos.crear_vuelo(
    "AA1001", "Buenos Aires", "París", "AUTO"
)
# Detecta que es INTERNACIONAL y crea VueloInternacional
```

## 🤝 Contribución

Este es un proyecto académico. Para mejoras:
1. Fork del repositorio
2. Crear rama feature
3. Commit de cambios
4. Push y Pull Request

## 📄 Licencia

Proyecto académico - Programación Orientada a Objetos

## ✨ Características Destacadas

- ✅ **4 Patrones de Diseño** completamente implementados
- ✅ **11 Excepciones personalizadas** con manejo robusto
- ✅ **11 Historias de usuario** documentadas
- ✅ **Type hints** en todo el código
- ✅ **Documentación completa** con docstrings
- ✅ **Código limpio** siguiendo PEP 8
- ✅ **Arquitectura modular** por capas

## 📞 Soporte

Para consultas sobre el proyecto:
- Revisar la documentación en `/docs`
- Consultar los ejemplos en `main.py`

---

**Desarrollado con Python 🐍 aplicando patrones de diseño profesionales**
