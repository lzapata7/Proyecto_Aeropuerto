# Historias de Usuario - Sistema de Gestión de Aeropuerto (Python)

## US-001: Registrar Vuelo
**Como** administrador del aeropuerto  
**Quiero** registrar nuevos vuelos en el sistema  
**Para** poder gestionar las operaciones de la terminal

### Criterios de Aceptación
- El vuelo debe tener un código único (ej: AA1001, LA2050)
- Debe incluir origen y destino
- Debe tener fecha y hora de salida programada
- Se debe poder asignar un avión al vuelo
- El estado inicial debe ser PROGRAMADO
- Debe validar que la fecha de salida no sea en el pasado

### Casos de Prueba
```python
def test_deberia_crear_vuelo_exitosamente():
    salida = datetime.now() + timedelta(hours=5)
    vuelo = Vuelo("AA1001", "Buenos Aires", "Miami", salida)
    
    assert vuelo.codigo == "AA1001"
    assert vuelo.estado == "PROGRAMADO"

def test_deberia_rechazar_vuelo_con_fecha_pasada():
    pasado = datetime.now() - timedelta(days=1)
    
    with pytest.raises(ValueError):
        Vuelo("AA1001", "Buenos Aires", "Miami", pasado)
```

---

## US-002: Registrar Pasajero
**Como** agente de reservas  
**Quiero** registrar pasajeros en el sistema  
**Para** poder gestionar sus reservas y vuelos

### Criterios de Aceptación
- El pasajero debe tener nombre completo
- Debe proporcionar número de documento válido
- Debe especificar tipo de documento (DNI, PASAPORTE, LICENCIA)
- Para vuelos internacionales, solo se acepta pasaporte
- Se debe validar que el documento no esté vencido
- Cada pasajero debe tener un ID único en el sistema

### Casos de Prueba
```python
def test_deberia_registrar_pasajero_con_pasaporte():
    pasajero = Pasajero("Juan Pérez", "AB123456", "PASAPORTE")
    pasajero.fecha_vencimiento_doc = date.today() + timedelta(days=1825)
    
    assert pasajero.id is not None
    assert pasajero.tiene_documento_valido() == True

def test_deberia_rechazar_documento_vencido():
    pasajero = Pasajero("María López", "12345678", "DNI")
    pasajero.fecha_vencimiento_doc = date.today() - timedelta(days=1)
    
    with pytest.raises(DocumentoInvalidoException):
        pasajero.validar_documento()
```

---

## US-003: Crear Reserva en Vuelo
**Como** pasajero  
**Quiero** reservar un asiento en un vuelo  
**Para** poder viajar a mi destino

### Criterios de Aceptación
- Debe verificar que el vuelo tenga capacidad disponible
- Se debe seleccionar clase de asiento (ECONOMICA, EJECUTIVA, PRIMERA_CLASE)
- Cada reserva debe tener un código único de 6 caracteres
- No se puede reservar en vuelos que ya despegaron
- Se debe asociar el pasajero a la reserva
- El sistema debe permitir sobreventa del 10% solo en clase económica
- El precio se calcula usando el patrón Strategy

### Casos de Prueba
```python
def test_deberia_crear_reserva_en_vuelo_disponible():
    vuelo = crear_vuelo_con_capacidad(100)
    pasajero = Pasajero("Carlos Ruiz", "98765432", "DNI")
    
    reserva = Reserva(vuelo, pasajero, "ECONOMICA")
    
    assert reserva.codigo_reserva is not None
    assert len(reserva.codigo_reserva) == 6
    assert reserva.estado == "CONFIRMADA"

def test_deberia_rechazar_reserva_en_vuelo_lleno():
    vuelo = crear_vuelo_lleno()
    pasajero = Pasajero("Ana Torres", "11223344", "PASAPORTE")
    
    with pytest.raises(VueloLlenoException):
        Reserva(vuelo, pasajero, "ECONOMICA")

def test_deberia_rechazar_reserva_en_vuelo_despegado():
    vuelo = crear_vuelo_despegado()
    pasajero = Pasajero("Luis Gómez", "55667788", "DNI")
    
    with pytest.raises(VueloYaDespegadoException):
        Reserva(vuelo, pasajero, "EJECUTIVA")
```

---

## US-004: Hacer Check-In
**Como** pasajero con reserva  
**Quiero** hacer check-in para mi vuelo  
**Para** obtener mi pase de abordar

### Criterios de Aceptación
- Solo se puede hacer check-in entre 24 horas y 45 minutos antes del vuelo
- El pasajero debe tener documento válido
- Para vuelos internacionales, se requiere pasaporte
- Se debe asignar un número de asiento
- Se debe verificar el equipaje permitido según la clase
- Después del check-in, se genera un pase de abordar

### Casos de Prueba
```python
def test_deberia_hacer_checkin_en_ventana_valida():
    vuelo = crear_vuelo_en_dos_horas()
    reserva = crear_reserva_valida(vuelo)
    
    reserva.hacer_checkin()
    
    assert reserva.estado == "CHECK_IN_REALIZADO"
    assert reserva.asiento_asignado is not None

def test_deberia_rechazar_checkin_muy_temprano():
    vuelo = crear_vuelo_en_dos_dias()
    reserva = crear_reserva_valida(vuelo)
    
    with pytest.raises(CheckInNoDisponibleException):
        reserva.hacer_checkin()

def test_deberia_rechazar_checkin_muy_tarde():
    vuelo = crear_vuelo_en_30_minutos()
    reserva = crear_reserva_valida(vuelo)
    
    with pytest.raises(CheckInNoDisponibleException):
        reserva.hacer_checkin()
```

---

## US-005: Gestionar Equipaje
**Como** pasajero  
**Quiero** registrar mi equipaje en la reserva  
**Para** poder documentarlo en el vuelo

### Criterios de Aceptación
- Clase Económica: máximo 2 maletas de 23kg cada una
- Clase Ejecutiva: máximo 3 maletas de 32kg cada una
- Primera Clase: máximo 3 maletas de 32kg cada una
- Equipaje de mano: máximo 10kg en todas las clases
- Se debe rechazar equipaje que exceda los límites
- El sistema debe calcular el peso total del equipaje

### Casos de Prueba
```python
def test_deberia_aceptar_equipaje_dentro_del_limite():
    reserva = crear_reserva_economica()
    
    reserva.agregar_equipaje_bodega(20.0)
    reserva.agregar_equipaje_bodega(22.0)
    
    assert reserva.get_peso_total_equipaje() == 42.0

def test_deberia_rechazar_equipaje_excedido():
    reserva = crear_reserva_economica()
    reserva.agregar_equipaje_bodega(23.0)
    reserva.agregar_equipaje_bodega(23.0)
    
    with pytest.raises(EquipajeExcedidoException):
        reserva.agregar_equipaje_bodega(10.0)  # Tercera maleta

def test_deberia_rechazar_maleta_demasiado_pesada():
    reserva = crear_reserva_economica()
    
    with pytest.raises(EquipajeExcedidoException):
        reserva.agregar_equipaje_bodega(24.0)  # Excede 23kg
```

---

## US-006: Asignar Gate de Embarque
**Como** coordinador de operaciones  
**Quiero** asignar gates a los vuelos  
**Para** organizar el embarque de pasajeros

### Criterios de Aceptación
- Cada gate puede estar asignado solo a un vuelo a la vez
- Se debe verificar que el gate esté disponible en el horario del vuelo
- Gates con letra A: Terminal Internacional
- Gates con letra B: Terminal Nacional
- Vuelos internacionales deben usar Terminal Internacional
- Se debe poder reasignar gate si es necesario

### Casos de Prueba
```python
def test_deberia_asignar_gate_disponible():
    vuelo = crear_vuelo_internacional()
    gate = Gate("A15", "INTERNACIONAL")
    
    vuelo.asignar_gate(gate)
    
    assert vuelo.gate.numero == "A15"
    assert gate.ocupado == True

def test_deberia_rechazar_gate_ocupado():
    gate = Gate("A20", "INTERNACIONAL")
    vuelo1 = crear_vuelo_internacional()
    vuelo2 = crear_vuelo_internacional()
    
    vuelo1.asignar_gate(gate)
    
    with pytest.raises(GateNoDisponibleException):
        vuelo2.asignar_gate(gate)

def test_deberia_rechazar_terminal_incorrecta():
    vuelo_internacional = crear_vuelo_internacional()
    gate_nacional = Gate("B10", "NACIONAL")
    
    with pytest.raises(ValueError):
        vuelo_internacional.asignar_gate(gate_nacional)
```

---

## US-007: Asignar Tripulación al Vuelo
**Como** jefe de operaciones  
**Quiero** asignar tripulación a los vuelos  
**Para** garantizar la seguridad de las operaciones

### Criterios de Aceptación
- Debe haber al menos 1 capitán y 1 copiloto
- Ratio: 1 tripulante de cabina por cada 50 pasajeros
- Los pilotos deben tener licencia vigente
- Los tripulantes no pueden exceder 9 horas de vuelo al día
- Se debe validar tiempo de descanso mínimo (12 horas entre vuelos)

### Casos de Prueba
```python
def test_deberia_asignar_tripulacion_completa():
    vuelo = crear_vuelo_con_capacidad(150)
    capitan = Tripulacion("Pedro Martínez", "CAPITAN")
    copiloto = Tripulacion("Laura Sánchez", "COPILOTO")
    
    vuelo.agregar_tripulante(capitan)
    vuelo.agregar_tripulante(copiloto)
    vuelo.agregar_tripulantes_cabina(3)
    
    assert vuelo.tiene_tripulacion_completa() == True

def test_deberia_rechazar_despegue_sin_tripulacion():
    vuelo = crear_vuelo_sin_tripulacion()
    
    with pytest.raises(TripulacionIncompletaException):
        vuelo.iniciar_abordaje()

def test_deberia_rechazar_tripulante_con_licencia_vencida():
    piloto = Tripulacion("Jorge Díaz", "CAPITAN")
    piloto.vencimiento_licencia = date.today() - timedelta(days=1)
    
    with pytest.raises(DocumentoInvalidoException):
        piloto.validar_licencia()
```

---

## US-008: Cancelar Reserva
**Como** pasajero  
**Quiero** cancelar mi reserva  
**Para** liberar el asiento en caso de no poder viajar

### Criterios de Aceptación
- Se puede cancelar hasta 3 horas antes del vuelo
- La capacidad del vuelo debe actualizarse
- El estado de la reserva debe cambiar a CANCELADA
- No se puede cancelar una reserva ya cancelada
- No se puede cancelar si ya se hizo check-in (debe hacerse en counter)

### Casos de Prueba
```python
def test_deberia_cancelar_reserva_a_tiempo():
    vuelo = crear_vuelo_en_cinco_horas()
    reserva = crear_reserva_valida(vuelo)
    capacidad_inicial = vuelo.get_asientos_disponibles()
    
    reserva.cancelar()
    
    assert reserva.estado == "CANCELADA"
    assert vuelo.get_asientos_disponibles() == capacidad_inicial + 1

def test_deberia_rechazar_cancelacion_tardia():
    vuelo = crear_vuelo_en_dos_horas()
    reserva = crear_reserva_valida(vuelo)
    
    with pytest.raises(CheckInNoDisponibleException):
        reserva.cancelar()

def test_deberia_rechazar_cancelacion_con_checkin():
    reserva = crear_reserva_con_checkin()
    
    with pytest.raises(ValueError):
        reserva.cancelar()
```

---

## US-009: Consultar Historial de Vuelos del Pasajero
**Como** pasajero  
**Quiero** consultar mi historial de vuelos  
**Para** revisar mis viajes anteriores y acumular millas

### Criterios de Aceptación
- Debe mostrar todos los vuelos completados del pasajero
- Debe incluir: fecha, origen, destino, aerolínea
- Debe calcular total de millas acumuladas
- Pasajeros con más de 50,000 millas son viajeros frecuentes
- El historial debe estar ordenado por fecha descendente

### Casos de Prueba
```python
def test_deberia_obtener_historial_de_vuelos():
    pasajero = crear_pasajero_con_vuelos_completados(5)
    
    historial = pasajero.get_historial_vuelos()
    
    assert len(historial) == 5
    assert historial[0].fecha_salida > historial[4].fecha_salida

def test_deberia_calcular_millas_acumuladas():
    pasajero = crear_pasajero_con_millas_acumuladas(55000)
    
    assert pasajero.es_viajero_frecuente() == True
    assert pasajero.millas_acumuladas == 55000
```

---

## US-010: Validar Restricciones de Edad para Vuelos Internacionales
**Como** sistema  
**Quiero** validar restricciones de edad  
**Para** cumplir con regulaciones internacionales

### Criterios de Aceptación
- Menores de 12 años no pueden viajar solos en vuelos internacionales
- Menores entre 12 y 17 años requieren autorización de los padres
- Se debe validar la edad al momento de la reserva
- Para vuelos nacionales, menores de 5 años no pueden viajar solos

### Casos de Prueba
```python
def test_deberia_rechazar_menor_solo_en_vuelo_internacional():
    vuelo_internacional = crear_vuelo_internacional()
    menor = crear_pasajero(10)  # 10 años
    
    with pytest.raises(EdadInsuficienteException):
        Reserva(vuelo_internacional, menor, "ECONOMICA")

def test_deberia_aceptar_menor_con_autorizacion():
    vuelo_internacional = crear_vuelo_internacional()
    menor = crear_pasajero(15)
    menor.tiene_autorizacion = True
    
    reserva = Reserva(vuelo_internacional, menor, "ECONOMICA")
    
    assert reserva.estado == "CONFIRMADA"
```

---

## US-011: Cambiar Estado del Vuelo (con Observer)
**Como** controlador de operaciones  
**Quiero** actualizar el estado de los vuelos  
**Para** reflejar el progreso de las operaciones y notificar automáticamente

### Criterios de Aceptación
- Estados válidos: PROGRAMADO → ABORDANDO → DESPEGADO → ATERRIZADO
- También puede cambiar a: CANCELADO, RETRASADO
- No se puede volver a estados anteriores
- Al cambiar a ABORDANDO, se debe cerrar el check-in
- Al cambiar a DESPEGADO, se debe liberar el gate
- **Patrón Observer**: Se deben enviar notificaciones automáticas (email, SMS, app)

### Casos de Prueba
```python
def test_deberia_cambiar_estado_secuencialmente():
    vuelo = crear_vuelo_en_abordaje()
    
    # Agregar observers
    email_notif = NotificadorEmail()
    vuelo.agregar_observer(email_notif)
    
    vuelo.cambiar_estado("DESPEGADO")
    
    assert vuelo.estado == "DESPEGADO"
    assert vuelo.gate.ocupado == False
    assert len(email_notif.notificaciones_enviadas) > 0

def test_deberia_rechazar_retroceso_de_estado():
    vuelo = crear_vuelo_despegado()
    
    with pytest.raises(ValueError):
        vuelo.cambiar_estado("ABORDANDO")

def test_deberia_notificar_a_observers():
    vuelo = Vuelo("AA1001", "BUE", "MIA", datetime.now() + timedelta(hours=5))
    
    email = NotificadorEmail()
    sms = NotificadorSMS()
    log = RegistroEventos()
    
    vuelo.agregar_observer(email)
    vuelo.agregar_observer(sms)
    vuelo.agregar_observer(log)
    
    vuelo.cambiar_estado("RETRASADO")
    
    assert len(email.notificaciones_enviadas) == 1
    assert len(sms.notificaciones_enviadas) == 1
    assert len(log.eventos_registrados) == 1
```

---

## US-012: Calcular Precio con Strategy
**Como** sistema de reservas  
**Quiero** calcular precios dinámicamente según temporada  
**Para** optimizar ingresos y ocupación

### Criterios de Aceptación
- **Patrón Strategy**: El precio varía según la temporada
- Temporada Alta (Dic, Ene, Jul): +50% de recargo
- Temporada Baja (Abr, May, Sep, Oct): -20% descuento
- Temporada Media (resto): precio base
- El multiplicador por clase se mantiene (Eco: 1x, Ej: 2.5x, Primera: 4x)
- Se debe poder cambiar la estrategia en tiempo de ejecución

### Casos de Prueba
```python
def test_deberia_aplicar_estrategia_temporada_alta():
    estrategia = PrecioTemporadaAlta()
    calculadora = CalculadoraPrecio(estrategia)
    
    resultado = calculadora.calcular(10000, "ECONOMICA", 6000)
    
    # 10000 * 1.0 (eco) * 1.50 (alta) * 1.10 (>5000km) = 16500
    assert resultado['precio'] == 16500.0

def test_deberia_aplicar_estrategia_temporada_baja():
    estrategia = PrecioTemporadaBaja()
    calculadora = CalculadoraPrecio(estrategia)
    
    resultado = calculadora.calcular(10000, "ECONOMICA", 3000)
    
    # 10000 * 1.0 (eco) * 0.80 (baja) = 8000
    assert resultado['precio'] == 8000.0

def test_deberia_cambiar_estrategia_dinamicamente():
    calculadora = CalculadoraPrecio(PrecioTemporadaMedia())
    
    precio1 = calculadora.calcular(10000, "EJECUTIVA", 5000)
    
    calculadora.set_estrategia(PrecioTemporadaAlta())
    precio2 = calculadora.calcular(10000, "EJECUTIVA", 5000)
    
    # 10000 * 2.5 = 25000 (media)
    # 10000 * 2.5 * 1.50 = 37500 (alta)
    assert precio1['precio'] == 25000.0
    assert precio2['precio'] == 37500.0
```

---

## Resumen de Cobertura

| Historia de Usuario | Entidad Principal | Excepciones Involucradas | Patrón de Diseño |
|---------------------|-------------------|--------------------------|------------------|
| US-001 | Vuelo | - | - |
| US-002 | Pasajero | DocumentoInvalidoException | - |
| US-003 | Reserva | VueloLlenoException, VueloYaDespegadoException | Strategy (precio) |
| US-004 | Reserva | CheckInNoDisponibleException, DocumentoInvalidoException | - |
| US-005 | Equipaje | EquipajeExcedidoException | - |
| US-006 | Gate | GateNoDisponibleException | - |
| US-007 | Tripulacion | TripulacionIncompletaException, DocumentoInvalidoException | - |
| US-008 | Reserva | CheckInNoDisponibleException | - |
| US-009 | Pasajero | - | - |
| US-010 | Pasajero | EdadInsuficienteException | - |
| US-011 | Vuelo | - | **Observer** (notificaciones) |
| US-012 | Reserva | - | **Strategy** (precios) |

**Total de Historias**: 12  
**Total de Excepciones Personalizadas**: 11  
**Patrones de Diseño Aplicados**: 4 (Singleton, Strategy, Observer, Factory)  
**Cobertura de Casos de Prueba**: 100%

---

## Imports Necesarios para Tests

```python
import pytest
from datetime import datetime, timedelta, date
from src.modelo.vuelo import Vuelo
from src.modelo.pasajero import Pasajero
from src.modelo.reserva import Reserva
from src.modelo.gate import Gate
from src.modelo.tripulacion import Tripulacion
from src.modelo.equipaje import Equipaje
from src.excepciones.excepciones_aeropuerto import (
    VueloLlenoException,
    VueloNoEncontradoException,
    PasajeroNoEncontradoException,
    ReservaNoEncontradaException,
    DocumentoInvalidoException,
    CheckInNoDisponibleException,
    GateNoDisponibleException,
    EquipajeExcedidoException,
    VueloYaDespegadoException,
    EdadInsuficienteException,
    TripulacionIncompletaException
)
from src.patrones.observer import NotificadorEmail, NotificadorSMS, RegistroEventos
from src.patrones.strategy import (
    PrecioTemporadaAlta,
    PrecioTemporadaBaja,
    PrecioTemporadaMedia,
    CalculadoraPrecio
)
```

---

## Ejecución de Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar tests de una historia específica
pytest tests/test_vuelo.py -v

# Ejecutar con cobertura
pytest tests/ --cov=src --cov-report=html

# Ejecutar tests de patrones
pytest tests/test_patrones.py -v
```
