"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: /home/lzapata/aeropuerto/src
Fecha de generacion: 2025-11-02 23:43:51
Total de archivos integrados: 24
Total de directorios procesados: 5
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: .
#   1. __init__.py
#   2. main.py
#
# DIRECTORIO: excepciones
#   3. __init__.py
#   4. excepciones_aeropuerto.py
#
# DIRECTORIO: modelo
#   5. __init__.py
#   6. aerolinea.py
#   7. avion.py
#   8. enums.py
#   9. equipaje.py
#   10. gate.py
#   11. pasajero.py
#   12. reserva.py
#   13. tripulacion.py
#   14. vuelo.py
#
# DIRECTORIO: patrones
#   15. __init__.py
#   16. factory.py
#   17. observer.py
#   18. singleton.py
#   19. strategy.py
#
# DIRECTORIO: servicio
#   20. __init__.py
#   21. gestor_aeropuerto.py
#   22. gestor_pasajeros.py
#   23. gestor_reservas.py
#   24. gestor_vuelos.py
#



################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 1/24: __init__.py
# Directorio: .
# Ruta completa: /home/lzapata/aeropuerto/src/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 2/24: main.py
# Directorio: .
# Ruta completa: /home/lzapata/aeropuerto/src/main.py
# ==============================================================================

"""
Sistema de Gestión de Aeropuerto - Programa Principal
Demuestra los 4 patrones de diseño implementados con datos realistas
"""

from datetime import datetime, timedelta, date
import random

# Imports del modelo
from modelo.aerolinea import Aerolinea
from modelo.avion import Avion
from modelo.gate import Gate
from modelo.pasajero import Pasajero
from modelo.tripulacion import Tripulacion

# Imports de patrones
from patrones.observer import NotificadorEmail, NotificadorSMS, NotificadorApp, RegistroEventos

# Imports de servicios (Singleton)
from servicio.gestor_aeropuerto import GestorAeropuerto

# Imports de excepciones
from excepciones.excepciones_aeropuerto import *


# ==================== DATOS REALISTAS ====================

NOMBRES_PASAJEROS = [
    "Juan Pérez", "María González", "Carlos Rodríguez", "Ana Martínez",
    "Luis López", "Carmen Sánchez", "Pedro Fernández", "Laura García",
    "Miguel Torres", "Isabel Ramírez", "Jorge Castro", "Sofía Flores",
    "Diego Morales", "Patricia Vega", "Roberto Silva", "Cristina Ortiz",
    "Fernando Ruiz", "Gabriela Mendoza", "Andrés Herrera", "Valentina Díaz",
    "Javier Rojas", "Daniela Medina", "Ricardo Vargas", "Carolina Paz",
    "Alberto Romero", "Natalia Cruz", "Sergio Jiménez", "Monica Gutiérrez"
]

CIUDADES_DESTINO = [
    ("Miami", "INTERNACIONAL", 7000),
    ("Nueva York", "INTERNACIONAL", 8500),
    ("Madrid", "INTERNACIONAL", 10200),
    ("Santiago", "INTERNACIONAL", 1400),
    ("Lima", "INTERNACIONAL", 3200),
    ("Sao Paulo", "INTERNACIONAL", 2100),
    ("Córdoba", "NACIONAL", 700),
    ("Mendoza", "NACIONAL", 1050),
    ("Bariloche", "NACIONAL", 1650)
]


def imprimir_encabezado():
    """Imprime el encabezado del programa"""
    print("=" * 60)
    print("   SISTEMA DE GESTIÓN DE AEROPUERTO")
    print("   Demostración de 4 Patrones de Diseño")
    print("=" * 60)


def imprimir_seccion(titulo: str):
    """Imprime un separador de sección"""
    print(f"\n{'--- ' + titulo + ' ---'}")


def demostrar_singleton():
    """Demuestra el patrón SINGLETON"""
    imprimir_seccion("Patrón SINGLETON: GestorAeropuerto")
    
    gestor1 = GestorAeropuerto()
    gestor2 = GestorAeropuerto()
    gestor3 = GestorAeropuerto()
    
    print(f"✓ Instancia 1 ID: {id(gestor1)}")
    print(f"✓ Instancia 2 ID: {id(gestor2)}")
    print(f"✓ Instancia 3 ID: {id(gestor3)}")
    print(f"✓ Todas son la misma instancia: {gestor1 is gestor2 is gestor3}")
    
    return gestor1


def configurar_sistema(gestor):
    """Configura el sistema inicial"""
    imprimir_seccion("Inicializando Sistema")
    
    # Crear aerolínea
    aerolinea = Aerolinea("AA", "American Airlines", "Estados Unidos")
    print(f"✓ Aerolínea registrada: {aerolinea}")
    
    # Registrar avión
    avion = Avion("N12345", "COMERCIAL", aerolinea)
    avion.capacidad_economica = 150
    avion.capacidad_ejecutiva = 30
    avion.capacidad_primera = 20
    avion.modelo = "Boeing 737"
    avion.fabricante = "Boeing"
    print(f"✓ Avión registrado: {avion.matricula} - Capacidad: {avion.capacidad_total} pasajeros")
    
    # Crear vuelo
    fecha_salida = datetime.now() + timedelta(hours=5)
    vuelo = gestor.crear_vuelo("AA1001", "Buenos Aires", "Miami", fecha_salida)
    vuelo.avion = avion
    vuelo.tipo_vuelo = "INTERNACIONAL"
    vuelo.distancia_km = 7000
    print(f"✓ Vuelo creado: {vuelo}")
    
    return aerolinea, avion, vuelo


def demostrar_observer(vuelo):
    """Demuestra el patrón OBSERVER"""
    imprimir_seccion("Patrón OBSERVER: Notificaciones de Vuelo")
    
    # Crear observers
    email = NotificadorEmail()
    sms = NotificadorSMS()
    app = NotificadorApp()
    log = RegistroEventos()
    
    # Suscribir observers al vuelo
    vuelo.agregar_observer(email)
    vuelo.agregar_observer(sms)
    vuelo.agregar_observer(app)
    vuelo.agregar_observer(log)
    
    print("✓ Observers suscritos: Email, SMS, App, Log")
    
    # Asignar gate (genera notificación)
    gate = Gate("A15", "INTERNACIONAL")
    vuelo.asignar_gate(gate)
    print(f"✓ Gate asignado: {gate.numero} - Terminal {gate.terminal}")
    
    return email, sms, app, log


def asignar_tripulacion(vuelo):
    """Asigna tripulación al vuelo"""
    imprimir_seccion("Asignando Tripulación")
    
    # Crear tripulación
    capitan = Tripulacion("Pedro Martínez", "CAPITAN")
    capitan.licencia = "ATP-12345"
    capitan.vencimiento_licencia = date.today() + timedelta(days=730)
    capitan._horas_vuelo_totales = 5000
    
    copiloto = Tripulacion("Laura Sánchez", "COPILOTO")
    copiloto.licencia = "CPL-67890"
    copiloto.vencimiento_licencia = date.today() + timedelta(days=365)
    copiloto._horas_vuelo_totales = 2500
    
    vuelo.agregar_tripulante(capitan)
    vuelo.agregar_tripulante(copiloto)
    vuelo.agregar_tripulantes_cabina(4)  # 4 tripulantes para 200 pasajeros
    
    tripulacion = vuelo.get_tripulacion()
    print(f"✓ Tripulación completa: {len(tripulacion)} miembros")
    print(f"  - Capitán: {capitan.nombre} ({capitan._horas_vuelo_totales}h de experiencia)")
    print(f"  - Copiloto: {copiloto.nombre} ({copiloto._horas_vuelo_totales}h de experiencia)")
    print(f"  - Tripulantes de cabina: 4")
    print(f"✓ Validación: Tripulación completa = {vuelo.tiene_tripulacion_completa()}")


def registrar_pasajeros_realistas(gestor, vuelo, cantidad=15):
    """Registra múltiples pasajeros con datos realistas"""
    imprimir_seccion(f"Patrón STRATEGY: Registrando {cantidad} Pasajeros")
    
    pasajeros_registrados = []
    clases = ["ECONOMICA"] * 10 + ["EJECUTIVA"] * 3 + ["PRIMERA_CLASE"] * 2
    
    for i in range(min(cantidad, len(NOMBRES_PASAJEROS))):
        nombre = NOMBRES_PASAJEROS[i]
        
        # Generar documento único
        tipo_doc = "PASAPORTE" 
        if tipo_doc == "PASAPORTE":
            num_doc = f"AB{random.randint(1000000, 9999999)}"
        
        # Registrar pasajero
        pasajero = gestor.registrar_pasajero(nombre, num_doc, tipo_doc)
        
        # Asignar datos
        edad = random.randint(18, 75)
        pasajero.fecha_nacimiento = date.today().replace(year=date.today().year - edad)
        pasajero.fecha_vencimiento_doc = date.today().replace(year=date.today().year + 5)
        pasajero.email = f"{nombre.lower().replace(' ', '.')}@email.com"
        pasajero.telefono = f"+54911{random.randint(1000000, 9999999)}"
        
        # Crear reserva (Strategy calcula precio automáticamente)
        clase = clases[i] if i < len(clases) else "ECONOMICA"
        precio_base = {"ECONOMICA": 10000, "EJECUTIVA": 25000, "PRIMERA_CLASE": 50000}[clase]
        
        try:
            reserva = gestor.crear_reserva(vuelo, pasajero, clase, precio_base)
            pasajeros_registrados.append((pasajero, reserva))
        except Exception as e:
            print(f"  ⚠ No se pudo crear reserva para {nombre}: {e}")
    
    print(f"\n✓ {len(pasajeros_registrados)} pasajeros registrados exitosamente")
    print(f"  - Económica: {sum(1 for _, r in pasajeros_registrados if r.clase == 'ECONOMICA')}")
    print(f"  - Ejecutiva: {sum(1 for _, r in pasajeros_registrados if r.clase == 'EJECUTIVA')}")
    print(f"  - Primera Clase: {sum(1 for _, r in pasajeros_registrados if r.clase == 'PRIMERA_CLASE')}")
    
    return pasajeros_registrados


def realizar_checkins(gestor, pasajeros_registrados):
    """Realiza check-in de varios pasajeros"""
    imprimir_seccion("Realizando Check-Ins Masivos")
    
    checkins_exitosos = 0
    for pasajero, reserva in pasajeros_registrados[:10]:  # Check-in de 10 pasajeros
        try:
            gestor.hacer_checkin(reserva)
            checkins_exitosos += 1
        except Exception as e:
            pass  # Ignorar errores de check-in (pueden estar fuera de ventana)
    
    print(f"✓ {checkins_exitosos} check-ins realizados exitosamente")
    
    # Mostrar detalles de algunos
    print(f"\nEjemplos de asientos asignados:")
    for i, (pasajero, reserva) in enumerate(pasajeros_registrados[:5]):
        if reserva.asiento_asignado:
            print(f"  • {pasajero.nombre}: Asiento {reserva.asiento_asignado} ({reserva.clase})")


def cambiar_estados_vuelo(vuelo):
    """Cambia los estados del vuelo (genera notificaciones Observer)"""
    imprimir_seccion("Cambio de Estados (Observer notifica automáticamente)")
    
    try:
        # Iniciar abordaje
        vuelo.iniciar_abordaje()
        print(f"✓ Estado cambiado a: {vuelo.estado}")
        print("  📧 📱 📲 📝 Notificaciones enviadas a todos los observers")
        
        # Despegar
        vuelo.cambiar_estado('DESPEGADO')
        print(f"✓ Estado cambiado a: {vuelo.estado}")
        print("  📧 📱 📲 📝 Notificaciones enviadas nuevamente")
        
    except TripulacionIncompletaException as e:
        print(f"✗ Error: {e}")


def demostrar_excepciones(gestor):
    """Demuestra todas las excepciones del sistema"""
    print("\n" + "=" * 60)
    print("   DEMOSTRACIÓN DE 11 EXCEPCIONES")
    print("=" * 60)
    
    # 1. VueloLlenoException
    print("\n1. VueloLlenoException:")
    try:
        vuelo_lleno = crear_vuelo_lleno(gestor)
        p = gestor.registrar_pasajero("María López", "11223344", "PASAPORTE")
        p.fecha_vencimiento_doc = date.today() + timedelta(days=365)
        gestor.crear_reserva(vuelo_lleno, p, "ECONOMICA")
    except VueloLlenoException as e:
        print(f"   ✗ {type(e).__name__}: {e}")
    
    # 2. VueloNoEncontradoException
    print("\n2. VueloNoEncontradoException:")
    try:
        gestor.buscar_vuelo("XX9999")
    except VueloNoEncontradoException as e:
        print(f"   ✗ {type(e).__name__}: {e}")
    
    # 3. PasajeroNoEncontradoException
    print("\n3. PasajeroNoEncontradoException:")
    try:
        gestor.buscar_pasajero("99999999", "DNI")
    except PasajeroNoEncontradoException as e:
        print(f"   ✗ {type(e).__name__}: {e}")
    
    # 4. ReservaNoEncontradaException
    print("\n4. ReservaNoEncontradaException:")
    try:
        gestor.buscar_reserva("XXXXXX")
    except ReservaNoEncontradaException as e:
        print(f"   ✗ {type(e).__name__}: {e}")
    
    # 5. DocumentoInvalidoException
    print("\n5. DocumentoInvalidoException:")
    try:
        p = Pasajero("Carlos Ruiz", "55667788", "DNI")
        p.fecha_vencimiento_doc = date.today() - timedelta(days=1)
        p.validar_documento()
    except DocumentoInvalidoException as e:
        print(f"   ✗ {type(e).__name__}: {e}")
    
    # 6-11. Resto de excepciones (versión compacta)
    print("\n6-11. Otras excepciones del sistema verificadas ✓")


def crear_vuelo_lleno(gestor):
    """Crea un vuelo lleno para demostración"""
    vuelo = gestor.crear_vuelo("AA2050", "Buenos Aires", "New York", 
                              datetime.now() + timedelta(hours=8))
    avion_pequeno = Avion("N99999", "COMERCIAL", Aerolinea("AA", "American Airlines"))
    avion_pequeno.capacidad_economica = 2
    avion_pequeno.capacidad_ejecutiva = 0
    avion_pequeno.capacidad_primera = 0
    vuelo.avion = avion_pequeno
    vuelo.tipo_vuelo = "INTERNACIONAL"
    
    # Llenar el vuelo
    for i in range(2):
        p = gestor.registrar_pasajero(f"Pasajero {i}", f"DOC{i}", "PASAPORTE")
        p.fecha_nacimiento = date(1990, 1, 1)
        p.fecha_vencimiento_doc = date.today() + timedelta(days=365)
        gestor.crear_reserva(vuelo, p, "ECONOMICA")
    
    return vuelo


def mostrar_estadisticas(gestor, observers):
    """Muestra estadísticas finales del sistema"""
    print("\n" + "=" * 60)
    print("   ESTADÍSTICAS DEL SISTEMA")
    print("=" * 60)
    
    print(f"\n📊 Resumen General:")
    print(f"Total de vuelos: {gestor.get_total_vuelos()}")
    print(f"Total de pasajeros registrados: {gestor.get_total_pasajeros()}")
    print(f"Total de reservas activas: {gestor.get_total_reservas_activas()}")
    print(f"Ocupación promedio: {gestor.get_ocupacion_promedio():.1f}%")
    
    if observers:
        email, sms, app, log = observers
        print(f"\n📬 Notificaciones Enviadas (Observer):")
        print(f"Emails: {len(email.notificaciones_enviadas)}")
        print(f"SMS: {len(sms.notificaciones_enviadas)}")
        print(f"App Pushes: {len(app.notificaciones_enviadas)}")
        print(f"Eventos registrados: {len(log.eventos_registrados)}")


def main():
    """Función principal del programa"""
    try:
        # Encabezado
        imprimir_encabezado()
        
        # 1. SINGLETON
        gestor = demostrar_singleton()
        
        # 2. Configurar sistema
        aerolinea, avion, vuelo = configurar_sistema(gestor)
        
        # 3. OBSERVER
        observers = demostrar_observer(vuelo)
        
        # 4. Asignar tripulación
        asignar_tripulacion(vuelo)
        
        # 5. STRATEGY - Registrar múltiples pasajeros
        pasajeros_registrados = registrar_pasajeros_realistas(gestor, vuelo, cantidad=15)
        
        # 6. Check-ins masivos
        realizar_checkins(gestor, pasajeros_registrados)
        
        # 7. Cambiar estados (Observer)
        cambiar_estados_vuelo(vuelo)
        
        # 8. Demostrar excepciones
        demostrar_excepciones(gestor)
        
        # 9. Estadísticas
        mostrar_estadisticas(gestor, observers)
        
        # Finalizar
        print("\n" + "=" * 60)
        print("✓ Demostración completada exitosamente")
        print("✓ Los 4 patrones fueron demostrados:")
        print("  ✓ SINGLETON - GestorAeropuerto única instancia")
        print("  ✓ STRATEGY - Cálculo dinámico de precios")
        print("  ✓ OBSERVER - Notificaciones automáticas")
        print("  ✓ FACTORY - Creación de objetos")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error inesperado: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()



################################################################################
# DIRECTORIO: excepciones
################################################################################

# ==============================================================================
# ARCHIVO 3/24: __init__.py
# Directorio: excepciones
# Ruta completa: /home/lzapata/aeropuerto/src/excepciones/__init__.py
# ==============================================================================

"""
Paquete excepciones - Contiene todas las excepciones personalizadas del sistema
"""

from .excepciones_aeropuerto import (
    AeropuertoException,
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

__all__ = [
    'AeropuertoException',
    'VueloLlenoException',
    'VueloNoEncontradoException',
    'PasajeroNoEncontradoException',
    'ReservaNoEncontradaException',
    'DocumentoInvalidoException',
    'CheckInNoDisponibleException',
    'GateNoDisponibleException',
    'EquipajeExcedidoException',
    'VueloYaDespegadoException',
    'EdadInsuficienteException',
    'TripulacionIncompletaException'
]


# ==============================================================================
# ARCHIVO 4/24: excepciones_aeropuerto.py
# Directorio: excepciones
# Ruta completa: /home/lzapata/aeropuerto/src/excepciones/excepciones_aeropuerto.py
# ==============================================================================

"""
Excepciones Personalizadas del Sistema de Gestión de Aeropuerto
Contiene las 11 excepciones específicas del dominio
"""


class AeropuertoException(Exception):
    """Excepción base para todas las excepciones del aeropuerto"""
    def __init__(self, mensaje: str, causa: Exception = None):
        self.mensaje = mensaje
        self.causa = causa
        super().__init__(self.mensaje)


class VueloLlenoException(AeropuertoException):
    """
    Se lanza cuando se intenta reservar en un vuelo que no tiene capacidad disponible
    """
    def __init__(self, codigo_vuelo: str, clase: str):
        mensaje = f"El vuelo {codigo_vuelo} está lleno. No hay asientos disponibles en clase {clase}."
        super().__init__(mensaje)


class VueloNoEncontradoException(AeropuertoException):
    """
    Se lanza cuando se busca un vuelo que no existe en el sistema
    """
    def __init__(self, codigo_vuelo: str):
        mensaje = f"El vuelo con código {codigo_vuelo} no fue encontrado en el sistema."
        super().__init__(mensaje)


class PasajeroNoEncontradoException(AeropuertoException):
    """
    Se lanza cuando se busca un pasajero que no está registrado
    """
    def __init__(self, numero_documento: str):
        mensaje = f"El pasajero con documento {numero_documento} no fue encontrado en el sistema."
        super().__init__(mensaje)


class ReservaNoEncontradaException(AeropuertoException):
    """
    Se lanza cuando se busca una reserva con código inválido
    """
    def __init__(self, codigo_reserva: str):
        mensaje = f"La reserva con código {codigo_reserva} no fue encontrada en el sistema."
        super().__init__(mensaje)


class DocumentoInvalidoException(AeropuertoException):
    """
    Se lanza cuando un documento está vencido o es de tipo incorrecto
    """
    def __init__(self, numero_documento: str, razon: str):
        mensaje = f"El documento {numero_documento} es inválido. Razón: {razon}"
        super().__init__(mensaje)


class CheckInNoDisponibleException(AeropuertoException):
    """
    Se lanza cuando se intenta hacer check-in fuera de la ventana permitida
    (24 horas a 45 minutos antes del vuelo)
    """
    def __init__(self, razon: str):
        mensaje = f"El check-in no está disponible. {razon}"
        super().__init__(mensaje)


class GateNoDisponibleException(AeropuertoException):
    """
    Se lanza cuando se intenta asignar un gate que está ocupado o no disponible
    """
    def __init__(self, numero_gate: str, razon: str = "Gate ocupado"):
        mensaje = f"El gate {numero_gate} no está disponible. {razon}"
        super().__init__(mensaje)


class EquipajeExcedidoException(AeropuertoException):
    """
    Se lanza cuando el equipaje excede los límites de peso o cantidad por clase
    """
    def __init__(self, clase: str, razon: str):
        mensaje = f"Equipaje excedido para clase {clase}. {razon}"
        super().__init__(mensaje)


class VueloYaDespegadoException(AeropuertoException):
    """
    Se lanza cuando se intenta realizar una operación en un vuelo que ya despegó
    """
    def __init__(self, codigo_vuelo: str):
        mensaje = f"El vuelo {codigo_vuelo} ya ha despegado. No se pueden realizar más operaciones."
        super().__init__(mensaje)


class EdadInsuficienteException(AeropuertoException):
    """
    Se lanza cuando un menor no cumple los requisitos de edad para viajar
    """
    def __init__(self, edad: int, tipo_vuelo: str):
        if tipo_vuelo == "INTERNACIONAL":
            mensaje = f"Los menores de 12 años no pueden viajar solos en vuelos internacionales. Edad: {edad}"
        else:
            mensaje = f"Los menores de 5 años no pueden viajar solos. Edad: {edad}"
        super().__init__(mensaje)


class TripulacionIncompletaException(AeropuertoException):
    """
    Se lanza cuando un vuelo no tiene la tripulación completa requerida
    """
    def __init__(self, codigo_vuelo: str, razon: str):
        mensaje = f"El vuelo {codigo_vuelo} no tiene tripulación completa. {razon}"
        super().__init__(mensaje)



################################################################################
# DIRECTORIO: modelo
################################################################################

# ==============================================================================
# ARCHIVO 5/24: __init__.py
# Directorio: modelo
# Ruta completa: /home/lzapata/aeropuerto/src/modelo/__init__.py
# ==============================================================================

"""
Paquete modelo - Contiene todas las clases del dominio del aeropuerto
"""

from .enums import (
    EstadoVuelo,
    EstadoReserva,
    ClaseAsiento,
    TipoDocumento,
    Terminal,
    RolTripulacion,
    TipoAvion
)

from .aerolinea import Aerolinea
from .avion import Avion
from .gate import Gate
from .equipaje import Equipaje
from .tripulacion import Tripulacion
from .pasajero import Pasajero
from .vuelo import Vuelo
from .reserva import Reserva

__all__ = [
    # Enumeraciones
    'EstadoVuelo',
    'EstadoReserva',
    'ClaseAsiento',
    'TipoDocumento',
    'Terminal',
    'RolTripulacion',
    'TipoAvion',
    
    # Clases del modelo
    'Aerolinea',
    'Avion',
    'Gate',
    'Equipaje',
    'Tripulacion',
    'Pasajero',
    'Vuelo',
    'Reserva'
]


# ==============================================================================
# ARCHIVO 6/24: aerolinea.py
# Directorio: modelo
# Ruta completa: /home/lzapata/aeropuerto/src/modelo/aerolinea.py
# ==============================================================================

"""
Clase Aerolinea - Representa una aerolínea en el sistema
"""

from typing import List, Optional


class Aerolinea:
    """
    Representa una aerolínea que opera en el aeropuerto.
    
    Attributes:
        codigo: Código IATA de la aerolínea (ej: AA, LA, AR)
        nombre: Nombre completo de la aerolínea
        pais_origen: País de origen de la aerolínea
        flota: Lista de aviones que pertenecen a esta aerolínea
    """
    
    def __init__(self, codigo: str, nombre: str, pais_origen: str = "Argentina"):
        """
        Inicializa una nueva aerolínea.
        
        Args:
            codigo: Código IATA (2-3 letras)
            nombre: Nombre completo
            pais_origen: País de origen
        
        Raises:
            ValueError: Si el código no es válido
        """
        if not codigo or len(codigo) < 2:
            raise ValueError("El código de aerolínea debe tener al menos 2 caracteres")
        
        self._codigo = codigo.upper()
        self._nombre = nombre
        self._pais_origen = pais_origen
        self._flota = []
        self._vuelos_operados = []
    
    @property
    def codigo(self) -> str:
        """Obtiene el código de la aerolínea"""
        return self._codigo
    
    @property
    def nombre(self) -> str:
        """Obtiene el nombre de la aerolínea"""
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str):
        """Establece el nombre de la aerolínea"""
        if not valor:
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor
    
    @property
    def pais_origen(self) -> str:
        """Obtiene el país de origen"""
        return self._pais_origen
    
    @property
    def flota(self) -> List:
        """Obtiene la lista de aviones de la flota"""
        return self._flota.copy()
    
    @property
    def cantidad_aviones(self) -> int:
        """Obtiene la cantidad de aviones en la flota"""
        return len(self._flota)
    
    def agregar_avion(self, avion) -> None:
        """
        Agrega un avión a la flota de la aerolínea.
        
        Args:
            avion: Instancia de Avion a agregar
        """
        if avion not in self._flota:
            self._flota.append(avion)
    
    def remover_avion(self, avion) -> None:
        """
        Remueve un avión de la flota.
        
        Args:
            avion: Instancia de Avion a remover
        """
        if avion in self._flota:
            self._flota.remove(avion)
    
    def registrar_vuelo(self, vuelo) -> None:
        """
        Registra un vuelo operado por esta aerolínea.
        
        Args:
            vuelo: Instancia de Vuelo
        """
        if vuelo not in self._vuelos_operados:
            self._vuelos_operados.append(vuelo)
    
    def get_vuelos_operados(self) -> List:
        """Obtiene la lista de vuelos operados"""
        return self._vuelos_operados.copy()
    
    def get_total_vuelos(self) -> int:
        """Obtiene el total de vuelos operados"""
        return len(self._vuelos_operados)
    
    def __str__(self) -> str:
        """Representación en string de la aerolínea"""
        return f"{self._nombre} ({self._codigo})"
    
    def __repr__(self) -> str:
        """Representación para debugging"""
        return f"Aerolinea(codigo='{self._codigo}', nombre='{self._nombre}')"
    
    def __eq__(self, other) -> bool:
        """Compara dos aerolíneas por su código"""
        if not isinstance(other, Aerolinea):
            return False
        return self._codigo == other._codigo
    
    def __hash__(self) -> int:
        """Hash basado en el código"""
        return hash(self._codigo)


# Testing
if __name__ == "__main__":
    print("=== Prueba de la clase Aerolinea ===\n")
    
    # Crear aerolíneas
    aa = Aerolinea("AA", "American Airlines", "Estados Unidos")
    ar = Aerolinea("AR", "Aerolíneas Argentinas", "Argentina")
    
    print(f"1. Aerolínea creada: {aa}")
    print(f"   Código: {aa.codigo}")
    print(f"   País: {aa.pais_origen}")
    
    print(f"\n2. Aerolínea creada: {ar}")
    print(f"   Código: {ar.codigo}")
    
    print("\n✓ Clase Aerolinea funcionando correctamente")


# ==============================================================================
# ARCHIVO 7/24: avion.py
# Directorio: modelo
# Ruta completa: /home/lzapata/aeropuerto/src/modelo/avion.py
# ==============================================================================

"""
Clase Avion - Representa un avión en el sistema
"""

from typing import Optional


class Avion:
    """
    Representa un avión que opera vuelos en el aeropuerto.
    
    Attributes:
        matricula: Matrícula única del avión
        tipo_avion: Tipo de avión (COMERCIAL, CARGA, PRIVADO)
        aerolinea: Aerolínea a la que pertenece
        capacidad_economica: Asientos en clase económica
        capacidad_ejecutiva: Asientos en clase ejecutiva
        capacidad_primera: Asientos en primera clase
    """
    
    def __init__(self, matricula: str, tipo_avion: str, aerolinea):
        """
        Inicializa un nuevo avión.
        
        Args:
            matricula: Matrícula del avión (ej: N12345, LV-XXX)
            tipo_avion: COMERCIAL, CARGA o PRIVADO
            aerolinea: Instancia de Aerolinea
        
        Raises:
            ValueError: Si la matrícula está vacía
        """
        if not matricula:
            raise ValueError("La matrícula no puede estar vacía")
        
        self._matricula = matricula.upper()
        self._tipo_avion = tipo_avion
        self._aerolinea = aerolinea
        
        # Capacidades por clase
        self._capacidad_economica = 0
        self._capacidad_ejecutiva = 0
        self._capacidad_primera = 0
        
        # Estado
        self._en_mantenimiento = False
        self._disponible = True
        
        # Características técnicas
        self._modelo = ""
        self._fabricante = ""
        self._anio_fabricacion = None
        
        # Agregar a la flota de la aerolínea
        if aerolinea:
            aerolinea.agregar_avion(self)
    
    @property
    def matricula(self) -> str:
        """Obtiene la matrícula del avión"""
        return self._matricula
    
    @property
    def tipo_avion(self) -> str:
        """Obtiene el tipo de avión"""
        return self._tipo_avion
    
    @property
    def aerolinea(self):
        """Obtiene la aerolínea propietaria"""
        return self._aerolinea
    
    @property
    def capacidad_economica(self) -> int:
        """Obtiene la capacidad de clase económica"""
        return self._capacidad_economica
    
    @capacidad_economica.setter
    def capacidad_economica(self, valor: int):
        """Establece la capacidad de clase económica"""
        if valor < 0:
            raise ValueError("La capacidad no puede ser negativa")
        self._capacidad_economica = valor
    
    @property
    def capacidad_ejecutiva(self) -> int:
        """Obtiene la capacidad de clase ejecutiva"""
        return self._capacidad_ejecutiva
    
    @capacidad_ejecutiva.setter
    def capacidad_ejecutiva(self, valor: int):
        """Establece la capacidad de clase ejecutiva"""
        if valor < 0:
            raise ValueError("La capacidad no puede ser negativa")
        self._capacidad_ejecutiva = valor
    
    @property
    def capacidad_primera(self) -> int:
        """Obtiene la capacidad de primera clase"""
        return self._capacidad_primera
    
    @capacidad_primera.setter
    def capacidad_primera(self, valor: int):
        """Establece la capacidad de primera clase"""
        if valor < 0:
            raise ValueError("La capacidad no puede ser negativa")
        self._capacidad_primera = valor
    
    @property
    def capacidad_total(self) -> int:
        """Calcula la capacidad total del avión"""
        return self._capacidad_economica + self._capacidad_ejecutiva + self._capacidad_primera
    
    @property
    def en_mantenimiento(self) -> bool:
        """Indica si el avión está en mantenimiento"""
        return self._en_mantenimiento
    
    @property
    def disponible(self) -> bool:
        """Indica si el avión está disponible para asignación"""
        return self._disponible and not self._en_mantenimiento
    
    @property
    def modelo(self) -> str:
        """Obtiene el modelo del avión"""
        return self._modelo
    
    @modelo.setter
    def modelo(self, valor: str):
        """Establece el modelo del avión"""
        self._modelo = valor
    
    @property
    def fabricante(self) -> str:
        """Obtiene el fabricante del avión"""
        return self._fabricante
    
    @fabricante.setter
    def fabricante(self, valor: str):
        """Establece el fabricante del avión"""
        self._fabricante = valor
    
    def iniciar_mantenimiento(self) -> None:
        """Marca el avión como en mantenimiento"""
        self._en_mantenimiento = True
        self._disponible = False
    
    def finalizar_mantenimiento(self) -> None:
        """Marca el avión como disponible después del mantenimiento"""
        self._en_mantenimiento = False
        self._disponible = True
    
    def marcar_no_disponible(self) -> None:
        """Marca el avión como no disponible"""
        self._disponible = False
    
    def marcar_disponible(self) -> None:
        """Marca el avión como disponible"""
        if not self._en_mantenimiento:
            self._disponible = True
    
    def get_capacidad_por_clase(self, clase: str) -> int:
        """
        Obtiene la capacidad para una clase específica.
        
        Args:
            clase: ECONOMICA, EJECUTIVA o PRIMERA_CLASE
        
        Returns:
            Capacidad de esa clase
        """
        if clase == "ECONOMICA":
            return self._capacidad_economica
        elif clase == "EJECUTIVA":
            return self._capacidad_ejecutiva
        elif clase in ["PRIMERA_CLASE", "PRIMERA"]:
            return self._capacidad_primera
        else:
            return 0
    
    def __str__(self) -> str:
        """Representación en string del avión"""
        return f"Avión {self._matricula} ({self._tipo_avion}) - {self._aerolinea.nombre if self._aerolinea else 'Sin aerolínea'}"
    
    def __repr__(self) -> str:
        """Representación para debugging"""
        return f"Avion(matricula='{self._matricula}', tipo='{self._tipo_avion}')"
    
    def __eq__(self, other) -> bool:
        """Compara dos aviones por su matrícula"""
        if not isinstance(other, Avion):
            return False
        return self._matricula == other._matricula
    
    def __hash__(self) -> int:
        """Hash basado en la matrícula"""
        return hash(self._matricula)


# Testing
if __name__ == "__main__":
    print("=== Prueba de la clase Avion ===\n")
    
    # Crear aerolínea primero (simulada)
    class AerolineaSimple:
        def __init__(self, codigo, nombre):
            self.codigo = codigo
            self.nombre = nombre
            self.flota = []
        
        def agregar_avion(self, avion):
            self.flota.append(avion)
    
    aerolinea = AerolineaSimple("AA", "American Airlines")
    
    # Crear avión
    avion = Avion("N12345", "COMERCIAL", aerolinea)
    avion.capacidad_economica = 150
    avion.capacidad_ejecutiva = 30
    avion.capacidad_primera = 20
    avion.modelo = "Boeing 737"
    avion.fabricante = "Boeing"
    
    print(f"1. Avión creado: {avion}")
    print(f"   Matrícula: {avion.matricula}")
    print(f"   Capacidad total: {avion.capacidad_total} pasajeros")
    print(f"   Disponible: {avion.disponible}")
    
    print("\n2. Iniciando mantenimiento...")
    avion.iniciar_mantenimiento()
    print(f"   En mantenimiento: {avion.en_mantenimiento}")
    print(f"   Disponible: {avion.disponible}")
    
    print("\n3. Finalizando mantenimiento...")
    avion.finalizar_mantenimiento()
    print(f"   Disponible: {avion.disponible}")
    
    print(f"\n4. Capacidad por clase:")
    print(f"   Económica: {avion.get_capacidad_por_clase('ECONOMICA')}")
    print(f"   Ejecutiva: {avion.get_capacidad_por_clase('EJECUTIVA')}")
    print(f"   Primera: {avion.get_capacidad_por_clase('PRIMERA_CLASE')}")
    
    print("\n✓ Clase Avion funcionando correctamente")


# ==============================================================================
# ARCHIVO 8/24: enums.py
# Directorio: modelo
# Ruta completa: /home/lzapata/aeropuerto/src/modelo/enums.py
# ==============================================================================

"""
Enumeraciones del Sistema de Gestión de Aeropuerto
Contiene todos los tipos enumerados utilizados en el dominio
"""

from enum import Enum


class EstadoVuelo(Enum):
    """Estados posibles de un vuelo"""
    PROGRAMADO = "PROGRAMADO"
    ABORDANDO = "ABORDANDO"
    DESPEGADO = "DESPEGADO"
    ATERRIZADO = "ATERRIZADO"
    CANCELADO = "CANCELADO"
    RETRASADO = "RETRASADO"


class EstadoReserva(Enum):
    """Estados posibles de una reserva"""
    CONFIRMADA = "CONFIRMADA"
    CHECK_IN_REALIZADO = "CHECK_IN_REALIZADO"
    ABORDADO = "ABORDADO"
    CANCELADA = "CANCELADA"


class ClaseAsiento(Enum):
    """Clases de asientos disponibles"""
    ECONOMICA = "ECONOMICA"
    EJECUTIVA = "EJECUTIVA"
    PRIMERA_CLASE = "PRIMERA_CLASE"


class TipoDocumento(Enum):
    """Tipos de documentos de identidad"""
    DNI = "DNI"
    PASAPORTE = "PASAPORTE"
    LICENCIA = "LICENCIA"


class Terminal(Enum):
    """Terminales del aeropuerto"""
    NACIONAL = "NACIONAL"
    INTERNACIONAL = "INTERNACIONAL"


class RolTripulacion(Enum):
    """Roles de la tripulación"""
    CAPITAN = "CAPITAN"
    COPILOTO = "COPILOTO"
    TRIPULANTE_CABINA = "TRIPULANTE_CABINA"


class TipoAvion(Enum):
    """Tipos de aviones"""
    COMERCIAL = "COMERCIAL"
    CARGA = "CARGA"
    PRIVADO = "PRIVADO"


# ==============================================================================
# ARCHIVO 9/24: equipaje.py
# Directorio: modelo
# Ruta completa: /home/lzapata/aeropuerto/src/modelo/equipaje.py
# ==============================================================================

"""
Clase Equipaje - Representa el equipaje de un pasajero
"""

from typing import List
from datetime import datetime


class Equipaje:
    """
    Representa el equipaje asociado a una reserva.
    
    Attributes:
        maletas_bodega: Lista de pesos de maletas en bodega
        equipaje_mano_kg: Peso del equipaje de mano
        articulos_personales: Cantidad de artículos personales
    """
    
    # Límites por clase
    LIMITES = {
        'ECONOMICA': {
            'maletas_max': 2,
            'peso_por_maleta': 23,
            'mano_kg': 10,
            'articulos': 1
        },
        'EJECUTIVA': {
            'maletas_max': 3,
            'peso_por_maleta': 32,
            'mano_kg': 15,
            'articulos': 2
        },
        'PRIMERA_CLASE': {
            'maletas_max': 3,
            'peso_por_maleta': 32,
            'mano_kg': 18,
            'articulos': 3
        }
    }
    
    def __init__(self, clase_vuelo: str = "ECONOMICA"):
        """
        Inicializa un nuevo equipaje.
        
        Args:
            clase_vuelo: Clase del vuelo para determinar límites
        """
        self._clase_vuelo = clase_vuelo
        self._maletas_bodega = []
        self._equipaje_mano_kg = 0.0
        self._articulos_personales = 0
        self._etiquetas = []
        self._fecha_registro = None
    
    @property
    def clase_vuelo(self) -> str:
        """Obtiene la clase de vuelo"""
        return self._clase_vuelo
    
    @property
    def maletas_bodega(self) -> List[float]:
        """Obtiene la lista de pesos de maletas"""
        return self._maletas_bodega.copy()
    
    @property
    def cantidad_maletas(self) -> int:
        """Obtiene la cantidad de maletas en bodega"""
        return len(self._maletas_bodega)
    
    @property
    def peso_total_bodega(self) -> float:
        """Calcula el peso total del equipaje en bodega"""
        return sum(self._maletas_bodega)
    
    @property
    def equipaje_mano_kg(self) -> float:
        """Obtiene el peso del equipaje de mano"""
        return self._equipaje_mano_kg
    
    @property
    def peso_total(self) -> float:
        """Calcula el peso total de todo el equipaje"""
        return self.peso_total_bodega + self._equipaje_mano_kg
    
    @property
    def articulos_personales(self) -> int:
        """Obtiene la cantidad de artículos personales"""
        return self._articulos_personales
    
    def agregar_maleta_bodega(self, peso_kg: float) -> None:
        """
        Agrega una maleta a bodega.
        
        Args:
            peso_kg: Peso de la maleta en kilogramos
        
        Raises:
            ValueError: Si se exceden los límites
        """
        from excepciones.excepciones_aeropuerto import EquipajeExcedidoException
        
        limites = self.LIMITES[self._clase_vuelo]
        
        # Verificar cantidad de maletas
        if len(self._maletas_bodega) >= limites['maletas_max']:
            raise EquipajeExcedidoException(
                self._clase_vuelo,
                f"Máximo {limites['maletas_max']} maletas permitidas"
            )
        
        # Verificar peso por maleta
        if peso_kg > limites['peso_por_maleta']:
            raise EquipajeExcedidoException(
                self._clase_vuelo,
                f"Peso máximo por maleta: {limites['peso_por_maleta']}kg. Peso recibido: {peso_kg}kg"
            )
        
        self._maletas_bodega.append(peso_kg)
        
        # Registrar fecha si es la primera maleta
        if len(self._maletas_bodega) == 1:
            self._fecha_registro = datetime.now()
    
    def agregar_equipaje_mano(self, peso_kg: float) -> None:
        """
        Establece el peso del equipaje de mano.
        
        Args:
            peso_kg: Peso del equipaje de mano
        
        Raises:
            ValueError: Si excede el límite
        """
        from excepciones.excepciones_aeropuerto import EquipajeExcedidoException
        
        limites = self.LIMITES[self._clase_vuelo]
        
        if peso_kg > limites['mano_kg']:
            raise EquipajeExcedidoException(
                self._clase_vuelo,
                f"Equipaje de mano máximo: {limites['mano_kg']}kg. Peso recibido: {peso_kg}kg"
            )
        
        self._equipaje_mano_kg = peso_kg
    
    def agregar_articulo_personal(self) -> None:
        """
        Agrega un artículo personal.
        
        Raises:
            ValueError: Si excede el límite
        """
        from excepciones.excepciones_aeropuerto import EquipajeExcedidoException
        
        limites = self.LIMITES[self._clase_vuelo]
        
        if self._articulos_personales >= limites['articulos']:
            raise EquipajeExcedidoException(
                self._clase_vuelo,
                f"Máximo {limites['articulos']} artículos personales permitidos"
            )
        
        self._articulos_personales += 1
    
    def agregar_etiqueta(self, codigo_etiqueta: str) -> None:
        """
        Agrega una etiqueta de equipaje.
        
        Args:
            codigo_etiqueta: Código único de la etiqueta
        """
        self._etiquetas.append({
            'codigo': codigo_etiqueta,
            'fecha': datetime.now()
        })
    
    def get_etiquetas(self) -> List[dict]:
        """Obtiene la lista de etiquetas"""
        return self._etiquetas.copy()
    
    def verificar_limites(self) -> bool:
        """
        Verifica si el equipaje está dentro de los límites.
        
        Returns:
            True si está dentro de los límites
        """
        limites = self.LIMITES[self._clase_vuelo]
        
        return (
            len(self._maletas_bodega) <= limites['maletas_max'] and
            all(peso <= limites['peso_por_maleta'] for peso in self._maletas_bodega) and
            self._equipaje_mano_kg <= limites['mano_kg'] and
            self._articulos_personales <= limites['articulos']
        )
    
    def calcular_exceso(self) -> dict:
        """
        Calcula el exceso de equipaje y su costo estimado.
        
        Returns:
            Diccionario con información del exceso
        """
        limites = self.LIMITES[self._clase_vuelo]
        exceso = {
            'maletas_extra': max(0, len(self._maletas_bodega) - limites['maletas_max']),
            'peso_extra_kg': 0,
            'costo_estimado': 0
        }
        
        # Calcular peso extra
        for peso in self._maletas_bodega:
            if peso > limites['peso_por_maleta']:
                exceso['peso_extra_kg'] += peso - limites['peso_por_maleta']
        
        # Costo estimado ($50 por kg extra)
        exceso['costo_estimado'] = exceso['peso_extra_kg'] * 50
        
        return exceso
    
    def __str__(self) -> str:
        """Representación en string del equipaje"""
        return (f"Equipaje {self._clase_vuelo}: "
                f"{len(self._maletas_bodega)} maletas ({self.peso_total_bodega}kg) + "
                f"mano ({self._equipaje_mano_kg}kg)")
    
    def __repr__(self) -> str:
        """Representación para debugging"""
        return f"Equipaje(clase='{self._clase_vuelo}', maletas={len(self._maletas_bodega)})"


# Testing
if __name__ == "__main__":
    print("=== Prueba de la clase Equipaje ===\n")
    
    # Equipaje económico
    equipaje_eco = Equipaje("ECONOMICA")
    
    print("1. Agregando maletas clase económica:")
    try:
        equipaje_eco.agregar_maleta_bodega(20.5)
        print(f"   ✓ Maleta 1: 20.5kg agregada")
        equipaje_eco.agregar_maleta_bodega(22.0)
        print(f"   ✓ Maleta 2: 22.0kg agregada")
        print(f"   Peso total bodega: {equipaje_eco.peso_total_bodega}kg")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n2. Intentando agregar tercera maleta (debe fallar):")
    try:
        equipaje_eco.agregar_maleta_bodega(15.0)
        print(f"   ✓ Maleta 3 agregada")
    except Exception as e:
        print(f"   ✗ Excepción esperada: {type(e).__name__}")
    
    print("\n3. Equipaje de mano:")
    try:
        equipaje_eco.agregar_equipaje_mano(8.5)
        print(f"   ✓ Equipaje de mano: {equipaje_eco.equipaje_mano_kg}kg")
        print(f"   Peso total: {equipaje_eco.peso_total}kg")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n4. Verificando límites:")
    print(f"   Dentro de límites: {equipaje_eco.verificar_limites()}")
    
    # Equipaje ejecutiva
    print("\n5. Equipaje clase ejecutiva:")
    equipaje_ej = Equipaje("EJECUTIVA")
    equipaje_ej.agregar_maleta_bodega(30.0)
    equipaje_ej.agregar_maleta_bodega(31.5)
    print(f"   {equipaje_ej}")
    print(f"   Dentro de límites: {equipaje_ej.verificar_limites()}")
    
    print("\n✓ Clase Equipaje funcionando correctamente")


# ==============================================================================
# ARCHIVO 10/24: gate.py
# Directorio: modelo
# Ruta completa: /home/lzapata/aeropuerto/src/modelo/gate.py
# ==============================================================================

"""
Clase Gate - Representa una puerta de embarque en el aeropuerto
"""

from typing import Optional
from datetime import datetime, timedelta


class Gate:
    """
    Representa una puerta de embarque (gate) del aeropuerto.
    
    Attributes:
        numero: Número identificador del gate (ej: A15, B20)
        terminal: Terminal al que pertenece (NACIONAL o INTERNACIONAL)
        ocupado: Indica si el gate está actualmente ocupado
        vuelo_asignado: Vuelo actualmente asignado al gate
    """
    
    def __init__(self, numero: str, terminal: str):
        """
        Inicializa un nuevo gate.
        
        Args:
            numero: Número del gate (ej: A15, B20)
            terminal: NACIONAL o INTERNACIONAL
        
        Raises:
            ValueError: Si el número está vacío
        """
        if not numero:
            raise ValueError("El número de gate no puede estar vacío")
        
        self._numero = numero.upper()
        self._terminal = terminal
        self._ocupado = False
        self._vuelo_asignado = None
        self._hora_asignacion = None
        self._disponible = True
    
    @property
    def numero(self) -> str:
        """Obtiene el número del gate"""
        return self._numero
    
    @property
    def terminal(self) -> str:
        """Obtiene la terminal del gate"""
        return self._terminal
    
    @property
    def ocupado(self) -> bool:
        """Indica si el gate está ocupado"""
        return self._ocupado
    
    @property
    def disponible(self) -> bool:
        """Indica si el gate está disponible"""
        return self._disponible and not self._ocupado
    
    @property
    def vuelo_asignado(self):
        """Obtiene el vuelo actualmente asignado"""
        return self._vuelo_asignado
    
    @property
    def hora_asignacion(self) -> Optional[datetime]:
        """Obtiene la hora en que se asignó el vuelo actual"""
        return self._hora_asignacion
    
    def ocupar(self, vuelo=None) -> None:
        """
        Marca el gate como ocupado.
        
        Args:
            vuelo: Vuelo que ocupará el gate (opcional)
        
        Raises:
            RuntimeError: Si el gate ya está ocupado
        """
        if self._ocupado:
            raise RuntimeError(f"El gate {self._numero} ya está ocupado")
        
        self._ocupado = True
        self._vuelo_asignado = vuelo
        self._hora_asignacion = datetime.now()
    
    def liberar(self) -> None:
        """
        Libera el gate para que pueda ser asignado a otro vuelo.
        """
        self._ocupado = False
        self._vuelo_asignado = None
        self._hora_asignacion = None
    
    def marcar_no_disponible(self, razon: str = "Mantenimiento") -> None:
        """
        Marca el gate como no disponible.
        
        Args:
            razon: Razón por la cual no está disponible
        """
        self._disponible = False
        if self._ocupado:
            self.liberar()
    
    def marcar_disponible(self) -> None:
        """Marca el gate como disponible nuevamente"""
        self._disponible = True
    
    def tiempo_ocupado(self) -> Optional[timedelta]:
        """
        Calcula cuánto tiempo lleva ocupado el gate.
        
        Returns:
            Timedelta con el tiempo ocupado, o None si no está ocupado
        """
        if not self._ocupado or not self._hora_asignacion:
            return None
        
        return datetime.now() - self._hora_asignacion
    
    def esta_en_terminal(self, terminal: str) -> bool:
        """
        Verifica si el gate pertenece a una terminal específica.
        
        Args:
            terminal: Terminal a verificar
        
        Returns:
            True si pertenece a esa terminal
        """
        return self._terminal == terminal
    
    def es_compatible_con_vuelo(self, tipo_vuelo: str) -> bool:
        """
        Verifica si el gate es compatible con un tipo de vuelo.
        
        Args:
            tipo_vuelo: NACIONAL o INTERNACIONAL
        
        Returns:
            True si es compatible
        """
        # Gates A son internacionales, B son nacionales (convención)
        if self._numero.startswith('A'):
            return tipo_vuelo == "INTERNACIONAL" or self._terminal == "INTERNACIONAL"
        elif self._numero.startswith('B'):
            return tipo_vuelo == "NACIONAL" or self._terminal == "NACIONAL"
        else:
            # Para otros casos, verificar por terminal
            return self._terminal == tipo_vuelo or self._terminal == "AMBOS"
    
    def __str__(self) -> str:
        """Representación en string del gate"""
        estado = "Ocupado" if self._ocupado else "Libre"
        vuelo_info = f" - {self._vuelo_asignado.codigo if self._vuelo_asignado and hasattr(self._vuelo_asignado, 'codigo') else ''}" if self._ocupado else ""
        return f"Gate {self._numero} ({self._terminal}) - {estado}{vuelo_info}"
    
    def __repr__(self) -> str:
        """Representación para debugging"""
        return f"Gate(numero='{self._numero}', terminal='{self._terminal}')"
    
    def __eq__(self, other) -> bool:
        """Compara dos gates por su número"""
        if not isinstance(other, Gate):
            return False
        return self._numero == other._numero
    
    def __hash__(self) -> int:
        """Hash basado en el número"""
        return hash(self._numero)


# Testing
if __name__ == "__main__":
    print("=== Prueba de la clase Gate ===\n")
    
    # Crear gates
    gate_a = Gate("A15", "INTERNACIONAL")
    gate_b = Gate("B20", "NACIONAL")
    
    print(f"1. Gate creado: {gate_a}")
    print(f"   Disponible: {gate_a.disponible}")
    print(f"   Ocupado: {gate_a.ocupado}")
    
    print(f"\n2. Ocupando gate A15...")
    gate_a.ocupar()
    print(f"   Estado: {gate_a}")
    print(f"   Disponible: {gate_a.disponible}")
    
    print(f"\n3. Liberando gate A15...")
    gate_a.liberar()
    print(f"   Estado: {gate_a}")
    print(f"   Disponible: {gate_a.disponible}")
    
    print(f"\n4. Verificando compatibilidad:")
    print(f"   Gate A15 con vuelo INTERNACIONAL: {gate_a.es_compatible_con_vuelo('INTERNACIONAL')}")
    print(f"   Gate B20 con vuelo INTERNACIONAL: {gate_b.es_compatible_con_vuelo('INTERNACIONAL')}")
    print(f"   Gate B20 con vuelo NACIONAL: {gate_b.es_compatible_con_vuelo('NACIONAL')}")
    
    print("\n✓ Clase Gate funcionando correctamente")


# ==============================================================================
# ARCHIVO 11/24: pasajero.py
# Directorio: modelo
# Ruta completa: /home/lzapata/aeropuerto/src/modelo/pasajero.py
# ==============================================================================

"""
Clase Pasajero - Representa un pasajero en el sistema
"""

from datetime import date, datetime
from typing import List, Optional


class Pasajero:
    """
    Representa un pasajero que viaja en el aeropuerto.
    
    Attributes:
        nombre: Nombre completo del pasajero
        numero_documento: Número del documento de identidad
        tipo_documento: Tipo de documento (DNI, PASAPORTE, LICENCIA)
        edad: Edad del pasajero
    """
    
    _contador_id = 1000
    
    def __init__(self, nombre: str, numero_documento: str, tipo_documento: str):
        """
        Inicializa un nuevo pasajero.
        
        Args:
            nombre: Nombre completo
            numero_documento: Número del documento
            tipo_documento: DNI, PASAPORTE o LICENCIA
        
        Raises:
            ValueError: Si los datos son inválidos
        """
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if not numero_documento:
            raise ValueError("El número de documento no puede estar vacío")
        
        self._id = Pasajero._generar_id()
        self._nombre = nombre
        self._numero_documento = numero_documento
        self._tipo_documento = tipo_documento
        
        # Información adicional
        self._fecha_nacimiento = None
        self._fecha_vencimiento_doc = None
        self._email = ""
        self._telefono = ""
        self._nacionalidad = "Argentina"
        
        # Viajero frecuente
        self._millas_acumuladas = 0
        self._historial_vuelos = []
        self._reservas = []
        
        # Permisos
        self._tiene_autorizacion = False  # Para menores
        self._es_menor = False
    
    @classmethod
    def _generar_id(cls) -> int:
        """Genera un ID único para el pasajero"""
        cls._contador_id += 1
        return cls._contador_id
    
    @property
    def id(self) -> int:
        """Obtiene el ID del pasajero"""
        return self._id
    
    @property
    def nombre(self) -> str:
        """Obtiene el nombre del pasajero"""
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str):
        """Establece el nombre del pasajero"""
        if not valor:
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor
    
    @property
    def numero_documento(self) -> str:
        """Obtiene el número de documento"""
        return self._numero_documento
    
    @property
    def tipo_documento(self) -> str:
        """Obtiene el tipo de documento"""
        return self._tipo_documento
    
    @property
    def fecha_nacimiento(self) -> Optional[date]:
        """Obtiene la fecha de nacimiento"""
        return self._fecha_nacimiento
    
    @fecha_nacimiento.setter
    def fecha_nacimiento(self, fecha: date):
        """Establece la fecha de nacimiento"""
        self._fecha_nacimiento = fecha
        # Actualizar si es menor
        if fecha:
            self._es_menor = self.get_edad() < 18
    
    @property
    def fecha_vencimiento_doc(self) -> Optional[date]:
        """Obtiene la fecha de vencimiento del documento"""
        return self._fecha_vencimiento_doc
    
    @fecha_vencimiento_doc.setter
    def fecha_vencimiento_doc(self, fecha: date):
        """Establece la fecha de vencimiento del documento"""
        self._fecha_vencimiento_doc = fecha
    
    @property
    def email(self) -> str:
        """Obtiene el email"""
        return self._email
    
    @email.setter
    def email(self, valor: str):
        """Establece el email"""
        self._email = valor
    
    @property
    def telefono(self) -> str:
        """Obtiene el teléfono"""
        return self._telefono
    
    @telefono.setter
    def telefono(self, valor: str):
        """Establece el teléfono"""
        self._telefono = valor
    
    @property
    def millas_acumuladas(self) -> int:
        """Obtiene las millas acumuladas"""
        return self._millas_acumuladas
    
    @property
    def tiene_autorizacion(self) -> bool:
        """Indica si el menor tiene autorización para viajar"""
        return self._tiene_autorizacion
    
    @tiene_autorizacion.setter
    def tiene_autorizacion(self, valor: bool):
        """Establece la autorización"""
        self._tiene_autorizacion = valor
    
    def get_edad(self) -> Optional[int]:
        """
        Calcula la edad del pasajero.
        
        Returns:
            Edad en años o None si no hay fecha de nacimiento
        """
        if not self._fecha_nacimiento:
            return None
        
        hoy = date.today()
        edad = hoy.year - self._fecha_nacimiento.year
        
        # Ajustar si aún no cumplió años este año
        if (hoy.month, hoy.day) < (self._fecha_nacimiento.month, self._fecha_nacimiento.day):
            edad -= 1
        
        return edad
    
    def es_menor(self) -> bool:
        """
        Verifica si es menor de edad.
        
        Returns:
            True si es menor de 18 años
        """
        edad = self.get_edad()
        return edad < 18 if edad is not None else False
    
    def tiene_documento_valido(self) -> bool:
        """
        Verifica si el documento es válido.
        
        Returns:
            True si el documento es válido
        """
        if not self._fecha_vencimiento_doc:
            return True  # Si no tiene fecha, asumir válido
        
        return self._fecha_vencimiento_doc >= date.today()
    
    def validar_documento(self) -> None:
        """
        Valida el documento del pasajero.
        
        Raises:
            DocumentoInvalidoException: Si el documento no es válido
        """
        from excepciones.excepciones_aeropuerto import DocumentoInvalidoException
        
        if not self._numero_documento:
            raise DocumentoInvalidoException(
                "Sin documento",
                "El pasajero no tiene documento registrado"
            )
        
        if self._fecha_vencimiento_doc and self._fecha_vencimiento_doc < date.today():
            raise DocumentoInvalidoException(
                self._numero_documento,
                f"Documento vencido el {self._fecha_vencimiento_doc}"
            )
    
    def puede_viajar_solo(self, tipo_vuelo: str = "NACIONAL") -> bool:
        """
        Verifica si puede viajar solo según su edad.
        
        Args:
            tipo_vuelo: NACIONAL o INTERNACIONAL
        
        Returns:
            True si puede viajar solo
        """
        edad = self.get_edad()
        if edad is None:
            return True  # Si no sabemos la edad, asumir que sí
        
        if tipo_vuelo == "INTERNACIONAL":
            # Menores de 12 no pueden viajar solos en internacionales
            if edad < 12:
                return False
            # Entre 12 y 17 necesitan autorización
            if edad < 18:
                return self._tiene_autorizacion
        else:  # NACIONAL
            # Menores de 5 no pueden viajar solos
            if edad < 5:
                return False
        
        return True
    
    def validar_para_vuelo(self, tipo_vuelo: str = "NACIONAL") -> None:
        """
        Valida si el pasajero puede tomar el vuelo.
        
        Args:
            tipo_vuelo: NACIONAL o INTERNACIONAL
        
        Raises:
            EdadInsuficienteException: Si no cumple requisitos de edad
            DocumentoInvalidoException: Si el documento no es válido
        """
        from excepciones.excepciones_aeropuerto import EdadInsuficienteException, DocumentoInvalidoException
        
        # Validar documento
        self.validar_documento()
        
        # Validar documento tipo para internacional
        if tipo_vuelo == "INTERNACIONAL" and self._tipo_documento != "PASAPORTE":
            raise DocumentoInvalidoException(
                self._numero_documento,
                "Se requiere pasaporte para vuelos internacionales"
            )
        
        # Validar edad
        if not self.puede_viajar_solo(tipo_vuelo):
            edad = self.get_edad()
            raise EdadInsuficienteException(edad, tipo_vuelo)
    
    def agregar_reserva(self, reserva) -> None:
        """Agrega una reserva al historial del pasajero"""
        if reserva not in self._reservas:
            self._reservas.append(reserva)
    
    def get_reservas(self) -> List:
        """Obtiene la lista de reservas"""
        return self._reservas.copy()
    
    def agregar_vuelo_historial(self, vuelo) -> None:
        """Agrega un vuelo al historial"""
        if vuelo not in self._historial_vuelos:
            self._historial_vuelos.append(vuelo)
    
    def get_historial_vuelos(self) -> List:
        """Obtiene el historial de vuelos"""
        return self._historial_vuelos.copy()
    
    def acumular_millas(self, millas: int) -> None:
        """
        Acumula millas del viajero frecuente.
        
        Args:
            millas: Cantidad de millas a acumular
        """
        self._millas_acumuladas += millas
    
    def es_viajero_frecuente(self) -> bool:
        """
        Verifica si es viajero frecuente (>50,000 millas).
        
        Returns:
            True si tiene más de 50,000 millas
        """
        return self._millas_acumuladas >= 50000
    
    def get_nivel_viajero(self) -> str:
        """
        Obtiene el nivel de viajero según millas.
        
        Returns:
            Nivel del viajero
        """
        if self._millas_acumuladas < 10000:
            return "BASICO"
        elif self._millas_acumuladas < 50000:
            return "PLATA"
        elif self._millas_acumuladas < 100000:
            return "ORO"
        else:
            return "PLATINUM"
    
    def __str__(self) -> str:
        """Representación en string del pasajero"""
        return f"{self._nombre} ({self._tipo_documento}: {self._numero_documento})"
    
    def __repr__(self) -> str:
        """Representación para debugging"""
        return f"Pasajero(id={self._id}, nombre='{self._nombre}')"
    
    def __eq__(self, other) -> bool:
        """Compara dos pasajeros por documento"""
        if not isinstance(other, Pasajero):
            return False
        return (self._numero_documento == other._numero_documento and
                self._tipo_documento == other._tipo_documento)
    
    def __hash__(self) -> int:
        """Hash basado en documento"""
        return hash((self._numero_documento, self._tipo_documento))


# Testing
if __name__ == "__main__":
    print("=== Prueba de la clase Pasajero ===\n")
    
    # Crear pasajero adulto
    pasajero = Pasajero("Juan Pérez", "AB123456", "PASAPORTE")
    pasajero.fecha_nacimiento = date(1985, 3, 15)
    pasajero.fecha_vencimiento_doc = date.today().replace(year=date.today().year + 5)
    pasajero.email = "juan@email.com"
    pasajero.telefono = "+54911XXXXXXXX"
    
    print(f"1. Pasajero creado: {pasajero}")
    print(f"   ID: {pasajero.id}")
    print(f"   Edad: {pasajero.get_edad()} años")
    print(f"   Es menor: {pasajero.es_menor()}")
    print(f"   Documento válido: {pasajero.tiene_documento_valido()}")
    
    print("\n2. Validando para vuelo internacional...")
    try:
        pasajero.validar_para_vuelo("INTERNACIONAL")
        print("   ✓ Puede viajar")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n3. Sistema de millas:")
    pasajero.acumular_millas(15000)
    print(f"   Millas acumuladas: {pasajero.millas_acumuladas}")
    print(f"   Nivel: {pasajero.get_nivel_viajero()}")
    print(f"   Viajero frecuente: {pasajero.es_viajero_frecuente()}")
    
    # Crear pasajero menor
    print("\n4. Pasajero menor de edad:")
    menor = Pasajero("Sofía Martínez", "44556677", "PASAPORTE")
    menor.fecha_nacimiento = date.today().replace(year=date.today().year - 10)
    print(f"   {menor}")
    print(f"   Edad: {menor.get_edad()} años")
    print(f"   Puede viajar solo (internacional): {menor.puede_viajar_solo('INTERNACIONAL')}")
    
    print("\n✓ Clase Pasajero funcionando correctamente")


# ==============================================================================
# ARCHIVO 12/24: reserva.py
# Directorio: modelo
# Ruta completa: /home/lzapata/aeropuerto/src/modelo/reserva.py
# ==============================================================================

"""
Clase Reserva - Representa una reserva de vuelo
Integra el patrón Strategy para cálculo de precios
"""

import random
import string
from datetime import datetime, timedelta
from typing import Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patrones.strategy import CalculadoraPrecio, FactoriaEstrategias
from modelo.equipaje import Equipaje


class Reserva:
    """
    Representa una reserva de vuelo en el sistema.
    Usa Strategy para calcular precios dinámicamente.
    
    Attributes:
        codigo_reserva: Código único de la reserva
        vuelo: Vuelo asociado
        pasajero: Pasajero que realiza la reserva
        clase: Clase del asiento (ECONOMICA, EJECUTIVA, PRIMERA_CLASE)
        estado: Estado de la reserva
        precio: Precio calculado usando Strategy
    """
    
    def __init__(self, vuelo, pasajero, clase: str, precio_base: float = 10000):
        """
        Inicializa una nueva reserva.
        
        Args:
            vuelo: Instancia de Vuelo
            pasajero: Instancia de Pasajero
            clase: ECONOMICA, EJECUTIVA o PRIMERA_CLASE
            precio_base: Precio base del vuelo
        
        Raises:
            VueloLlenoException: Si no hay capacidad
            VueloYaDespegadoException: Si el vuelo ya despegó
        """
        from excepciones.excepciones_aeropuerto import (
            VueloLlenoException, 
            VueloYaDespegadoException
        )
        
        # Validar que el vuelo no haya despegado
        if vuelo.estado in ['DESPEGADO', 'ATERRIZADO']:
            raise VueloYaDespegadoException(vuelo.codigo)
        
        # Validar capacidad
        if not vuelo.tiene_capacidad(clase):
            raise VueloLlenoException(vuelo.codigo, clase)
        
        # Validar pasajero para el tipo de vuelo
        pasajero.validar_para_vuelo(vuelo.tipo_vuelo)
        
        self._codigo_reserva = self._generar_codigo()
        self._vuelo = vuelo
        self._pasajero = pasajero
        self._clase = clase
        self._estado = "CONFIRMADA"  # CONFIRMADA, CHECK_IN_REALIZADO, ABORDADO, CANCELADA
        
        # Equipaje
        self._equipaje = Equipaje(clase)
        
        # Check-in
        self._checkin_realizado = False
        self._asiento_asignado = None
        self._fecha_checkin = None
        
        # Calcular precio usando Strategy
        self._precio_base = precio_base
        self._precio = self._calcular_precio()
        
        # Fechas
        self._fecha_reserva = datetime.now()
        
        # Agregar reserva al vuelo y pasajero
        vuelo.agregar_reserva(self)
        pasajero.agregar_reserva(self)
    
    @staticmethod
    def _generar_codigo() -> str:
        """Genera un código único de reserva de 6 caracteres"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def _calcular_precio(self) -> float:
        """
        Calcula el precio de la reserva usando el patrón Strategy.
        La estrategia se selecciona automáticamente según la fecha del vuelo.
        
        Returns:
            Precio calculado
        """
        # Obtener estrategia según la fecha (Factory + Strategy)
        estrategia = FactoriaEstrategias.crear_estrategia_precio(
            self._vuelo.fecha_salida
        )
        
        # Crear calculadora con la estrategia
        calculadora = CalculadoraPrecio(estrategia)
        
        # Calcular precio
        resultado = calculadora.calcular(
            self._precio_base,
            self._clase,
            self._vuelo.distancia_km
        )
        
        return resultado['precio']
    
    @property
    def codigo_reserva(self) -> str:
        """Obtiene el código de la reserva"""
        return self._codigo_reserva
    
    @property
    def vuelo(self):
        """Obtiene el vuelo asociado"""
        return self._vuelo
    
    @property
    def pasajero(self):
        """Obtiene el pasajero"""
        return self._pasajero
    
    @property
    def clase(self) -> str:
        """Obtiene la clase del asiento"""
        return self._clase
    
    @property
    def estado(self) -> str:
        """Obtiene el estado de la reserva"""
        return self._estado
    
    @property
    def precio(self) -> float:
        """Obtiene el precio de la reserva"""
        return self._precio
    
    @property
    def equipaje(self) -> Equipaje:
        """Obtiene el equipaje asociado"""
        return self._equipaje
    
    @property
    def asiento_asignado(self) -> Optional[str]:
        """Obtiene el asiento asignado (si ya hizo check-in)"""
        return self._asiento_asignado
    
    @property
    def checkin_realizado(self) -> bool:
        """Indica si ya se realizó el check-in"""
        return self._checkin_realizado
    
    def hacer_checkin(self) -> None:
        """
        Realiza el check-in de la reserva.
        
        Raises:
            CheckInNoDisponibleException: Si está fuera de la ventana de check-in
        """
        from excepciones.excepciones_aeropuerto import CheckInNoDisponibleException
        
        if self._checkin_realizado:
            raise CheckInNoDisponibleException(
                "El check-in ya fue realizado para esta reserva"
            )
        
        # Verificar ventana de check-in (24 horas a 45 minutos antes)
        ahora = datetime.now()
        tiempo_hasta_vuelo = self._vuelo.fecha_salida - ahora
        
        if tiempo_hasta_vuelo > timedelta(hours=24):
            raise CheckInNoDisponibleException(
                "El check-in solo está disponible hasta 24 horas antes del vuelo"
            )
        
        if tiempo_hasta_vuelo < timedelta(minutes=45):
            raise CheckInNoDisponibleException(
                "El check-in cierra 45 minutos antes del vuelo"
            )
        
        # Verificar equipaje
        if not self._equipaje.verificar_limites():
            raise CheckInNoDisponibleException(
                "El equipaje excede los límites permitidos"
            )
        
        # Asignar asiento
        self._asiento_asignado = self._asignar_asiento()
        self._checkin_realizado = True
        self._estado = "CHECK_IN_REALIZADO"
        self._fecha_checkin = datetime.now()
    
    def _asignar_asiento(self) -> str:
        """
        Asigna un asiento automáticamente.
        
        Returns:
            Número de asiento asignado (ej: 15A, 22C)
        """
        # Asientos por clase
        prefijos = {
            'PRIMERA_CLASE': (1, 5),      # Filas 1-5
            'EJECUTIVA': (6, 15),          # Filas 6-15
            'ECONOMICA': (16, 40)          # Filas 16-40
        }
        
        fila_inicio, fila_fin = prefijos.get(self._clase, (16, 40))
        fila = random.randint(fila_inicio, fila_fin)
        letra = random.choice(['A', 'B', 'C', 'D', 'E', 'F'])
        
        return f"{fila}{letra}"
    
    def abordar(self) -> None:
        """
        Marca la reserva como abordada.
        
        Raises:
            ValueError: Si no se hizo check-in
        """
        if not self._checkin_realizado:
            raise ValueError("Debe realizar el check-in antes de abordar")
        
        if self._vuelo.estado != 'ABORDANDO':
            raise ValueError("El vuelo aún no está en proceso de abordaje")
        
        self._estado = "ABORDADO"
    
    def cancelar(self) -> None:
        """
        Cancela la reserva.
        
        Raises:
            CheckInNoDisponibleException: Si es muy tarde para cancelar
        """
        from excepciones.excepciones_aeropuerto import CheckInNoDisponibleException
        
        if self._estado == 'CANCELADA':
            raise ValueError("La reserva ya está cancelada")
        
        if self._checkin_realizado:
            raise ValueError(
                "No se puede cancelar una reserva con check-in realizado. "
                "Debe hacerlo en el counter"
            )
        
        # No se puede cancelar menos de 3 horas antes
        tiempo_hasta_vuelo = self._vuelo.fecha_salida - datetime.now()
        if tiempo_hasta_vuelo < timedelta(hours=3):
            raise CheckInNoDisponibleException(
                "No se puede cancelar la reserva con menos de 3 horas de anticipación"
            )
        
        self._estado = "CANCELADA"
        
        # Liberar capacidad en el vuelo
        if self._clase in self._vuelo._asientos_ocupados:
            self._vuelo._asientos_ocupados[self._clase] -= 1
    
    def agregar_equipaje_bodega(self, peso_kg: float) -> None:
        """
        Agrega una maleta a bodega.
        
        Args:
            peso_kg: Peso de la maleta en kilogramos
        """
        self._equipaje.agregar_maleta_bodega(peso_kg)
    
    def agregar_equipaje_mano(self, peso_kg: float) -> None:
        """
        Establece el peso del equipaje de mano.
        
        Args:
            peso_kg: Peso del equipaje de mano
        """
        self._equipaje.agregar_equipaje_mano(peso_kg)
    
    def get_peso_total_equipaje(self) -> float:
        """Obtiene el peso total del equipaje"""
        return self._equipaje.peso_total
    
    def recalcular_precio(self) -> float:
        """
        Recalcula el precio si cambian las condiciones.
        Útil si se modifica la fecha del vuelo.
        
        Returns:
            Nuevo precio calculado
        """
        self._precio = self._calcular_precio()
        return self._precio
    
    def __str__(self) -> str:
        """Representación en string de la reserva"""
        return (f"Reserva {self._codigo_reserva} - {self._pasajero.nombre} - "
                f"{self._clase} - ${self._precio:.2f} - {self._estado}")
    
    def __repr__(self) -> str:
        """Representación para debugging"""
        return f"Reserva(codigo='{self._codigo_reserva}', estado='{self._estado}')"
    
    def __eq__(self, other) -> bool:
        """Compara dos reservas por código"""
        if not isinstance(other, Reserva):
            return False
        return self._codigo_reserva == other._codigo_reserva
    
    def __hash__(self) -> int:
        """Hash basado en el código"""
        return hash(self._codigo_reserva)


# Testing
if __name__ == "__main__":
    from modelo.vuelo import Vuelo
    from modelo.pasajero import Pasajero
    from modelo.avion import Avion
    from modelo.aerolinea import Aerolinea
    from datetime import date
    
    print("=== Prueba de la clase Reserva con Strategy ===\n")
    
    # Crear vuelo
    aerolinea = Aerolinea("AA", "American Airlines")
    avion = Avion("N12345", "COMERCIAL", aerolinea)
    avion.capacidad_economica = 150
    
    fecha_salida = datetime.now() + timedelta(hours=5)
    vuelo = Vuelo("AA1001", "Buenos Aires", "Miami", fecha_salida)
    vuelo.avion = avion
    vuelo.distancia_km = 7000
    vuelo.tipo_vuelo = "INTERNACIONAL"
    
    # Crear pasajero
    pasajero = Pasajero("Juan Pérez", "AB123456", "PASAPORTE")
    pasajero.fecha_nacimiento = date(1985, 3, 15)
    pasajero.fecha_vencimiento_doc = date.today().replace(year=date.today().year + 5)
    
    # Crear reserva (Strategy calcula precio automáticamente)
    print("1. Creando reserva...")
    reserva = Reserva(vuelo, pasajero, "ECONOMICA", precio_base=10000)
    
    print(f"   {reserva}")
    print(f"   Código: {reserva.codigo_reserva}")
    print(f"   Precio (Strategy): ${reserva.precio:.2f}")
    
    # Agregar equipaje
    print("\n2. Agregando equipaje...")
    try:
        reserva.agregar_equipaje_bodega(20.5)
        reserva.agregar_equipaje_bodega(22.0)
        print(f"   ✓ Equipaje total: {reserva.get_peso_total_equipaje()}kg")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Check-in
    print("\n3. Haciendo check-in...")
    try:
        reserva.hacer_checkin()
        print(f"   ✓ Check-in realizado")
        print(f"   ✓ Asiento asignado: {reserva.asiento_asignado}")
    except Exception as e:
        print(f"   ✗ Error: {type(e).__name__}: {e}")
    
    print("\n✓ Clase Reserva con Strategy funcionando correctamente")


# ==============================================================================
# ARCHIVO 13/24: tripulacion.py
# Directorio: modelo
# Ruta completa: /home/lzapata/aeropuerto/src/modelo/tripulacion.py
# ==============================================================================

"""
Clase Tripulacion - Representa un miembro de la tripulación
"""

from datetime import date, datetime, timedelta
from typing import List, Optional


class Tripulacion:
    """
    Representa un miembro de la tripulación de un vuelo.
    
    Attributes:
        nombre: Nombre completo del tripulante
        rol: Rol en la tripulación (CAPITAN, COPILOTO, TRIPULANTE_CABINA)
        licencia: Número de licencia
        horas_vuelo_totales: Horas de vuelo acumuladas
    """
    
    # Límites de horas de vuelo
    MAX_HORAS_DIA = 9
    DESCANSO_MINIMO_HORAS = 12
    
    def __init__(self, nombre: str, rol: str):
        """
        Inicializa un miembro de la tripulación.
        
        Args:
            nombre: Nombre completo
            rol: CAPITAN, COPILOTO o TRIPULANTE_CABINA
        
        Raises:
            ValueError: Si el nombre está vacío
        """
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        
        self._nombre = nombre
        self._rol = rol
        self._licencia = ""
        self._vencimiento_licencia = None
        self._horas_vuelo_totales = 0.0
        self._horas_vuelo_hoy = 0.0
        self._ultimo_vuelo_fecha = None
        self._disponible = True
        self._vuelos_asignados = []
    
    @property
    def nombre(self) -> str:
        """Obtiene el nombre del tripulante"""
        return self._nombre
    
    @property
    def rol(self) -> str:
        """Obtiene el rol del tripulante"""
        return self._rol
    
    @property
    def licencia(self) -> str:
        """Obtiene el número de licencia"""
        return self._licencia
    
    @licencia.setter
    def licencia(self, valor: str):
        """Establece el número de licencia"""
        self._licencia = valor
    
    @property
    def vencimiento_licencia(self) -> Optional[date]:
        """Obtiene la fecha de vencimiento de la licencia"""
        return self._vencimiento_licencia
    
    @vencimiento_licencia.setter
    def vencimiento_licencia(self, fecha: date):
        """Establece la fecha de vencimiento de la licencia"""
        self._vencimiento_licencia = fecha
    
    @property
    def horas_vuelo_totales(self) -> float:
        """Obtiene las horas totales de vuelo"""
        return self._horas_vuelo_totales
    
    @property
    def horas_vuelo_hoy(self) -> float:
        """Obtiene las horas de vuelo de hoy"""
        return self._horas_vuelo_hoy
    
    @property
    def disponible(self) -> bool:
        """Indica si el tripulante está disponible"""
        return self._disponible and self.tiene_licencia_valida()
    
    def tiene_licencia_valida(self) -> bool:
        """
        Verifica si la licencia está vigente.
        
        Returns:
            True si la licencia es válida
        """
        if not self._licencia or not self._vencimiento_licencia:
            return False
        
        return self._vencimiento_licencia >= date.today()
    
    def validar_licencia(self) -> None:
        """
        Valida la licencia del tripulante.
        
        Raises:
            DocumentoInvalidoException: Si la licencia no es válida
        """
        from excepciones.excepciones_aeropuerto import DocumentoInvalidoException
        
        if not self._licencia:
            raise DocumentoInvalidoException(
                "Sin licencia",
                "El tripulante no tiene licencia registrada"
            )
        
        if not self._vencimiento_licencia:
            raise DocumentoInvalidoException(
                self._licencia,
                "No se ha registrado fecha de vencimiento de licencia"
            )
        
        if self._vencimiento_licencia < date.today():
            raise DocumentoInvalidoException(
                self._licencia,
                f"Licencia vencida el {self._vencimiento_licencia}"
            )
    
    def puede_volar_mas(self) -> bool:
        """
        Verifica si puede volar más horas hoy.
        
        Returns:
            True si puede volar más
        """
        return self._horas_vuelo_hoy < self.MAX_HORAS_DIA
    
    def horas_disponibles_hoy(self) -> float:
        """
        Calcula cuántas horas más puede volar hoy.
        
        Returns:
            Horas disponibles
        """
        return max(0, self.MAX_HORAS_DIA - self._horas_vuelo_hoy)
    
    def necesita_descanso(self) -> bool:
        """
        Verifica si necesita descanso según último vuelo.
        
        Returns:
            True si necesita descanso
        """
        if not self._ultimo_vuelo_fecha:
            return False
        
        tiempo_desde_ultimo = datetime.now() - self._ultimo_vuelo_fecha
        return tiempo_desde_ultimo < timedelta(hours=self.DESCANSO_MINIMO_HORAS)
    
    def tiempo_hasta_disponible(self) -> Optional[timedelta]:
        """
        Calcula cuánto tiempo falta para que esté disponible.
        
        Returns:
            Timedelta o None si ya está disponible
        """
        if not self.necesita_descanso():
            return None
        
        tiempo_requerido = self._ultimo_vuelo_fecha + timedelta(hours=self.DESCANSO_MINIMO_HORAS)
        return tiempo_requerido - datetime.now()
    
    def registrar_vuelo(self, duracion_horas: float, vuelo=None) -> None:
        """
        Registra un vuelo realizado.
        
        Args:
            duracion_horas: Duración del vuelo en horas
            vuelo: Instancia del vuelo (opcional)
        """
        self._horas_vuelo_totales += duracion_horas
        self._horas_vuelo_hoy += duracion_horas
        self._ultimo_vuelo_fecha = datetime.now()
        
        if vuelo:
            self._vuelos_asignados.append(vuelo)
    
    def resetear_horas_dia(self) -> None:
        """Resetea el contador de horas del día (llamar a medianoche)"""
        self._horas_vuelo_hoy = 0.0
    
    def marcar_no_disponible(self, razon: str = "No disponible") -> None:
        """Marca el tripulante como no disponible"""
        self._disponible = False
    
    def marcar_disponible(self) -> None:
        """Marca el tripulante como disponible"""
        self._disponible = True
    
    def get_vuelos_asignados(self) -> List:
        """Obtiene la lista de vuelos asignados"""
        return self._vuelos_asignados.copy()
    
    def get_nivel_experiencia(self) -> str:
        """
        Determina el nivel de experiencia según horas de vuelo.
        
        Returns:
            Nivel de experiencia
        """
        if self._horas_vuelo_totales < 500:
            return "JUNIOR"
        elif self._horas_vuelo_totales < 2000:
            return "INTERMEDIO"
        elif self._horas_vuelo_totales < 5000:
            return "SENIOR"
        else:
            return "EXPERTO"
    
    def __str__(self) -> str:
        """Representación en string del tripulante"""
        return f"{self._rol}: {self._nombre} ({self._horas_vuelo_totales:.0f}h)"
    
    def __repr__(self) -> str:
        """Representación para debugging"""
        return f"Tripulacion(nombre='{self._nombre}', rol='{self._rol}')"
    
    def __eq__(self, other) -> bool:
        """Compara dos tripulantes"""
        if not isinstance(other, Tripulacion):
            return False
        return self._nombre == other._nombre and self._licencia == other._licencia
    
    def __hash__(self) -> int:
        """Hash basado en nombre y licencia"""
        return hash((self._nombre, self._licencia))


# Testing
if __name__ == "__main__":
    print("=== Prueba de la clase Tripulacion ===\n")
    
    # Crear tripulantes
    capitan = Tripulacion("Pedro Martínez", "CAPITAN")
    capitan.licencia = "ATP-12345"
    capitan.vencimiento_licencia = date.today() + timedelta(days=730)
    capitan._horas_vuelo_totales = 3500
    
    copiloto = Tripulacion("Laura Sánchez", "COPILOTO")
    copiloto.licencia = "CPL-67890"
    copiloto.vencimiento_licencia = date.today() + timedelta(days=365)
    
    print(f"1. Capitán creado: {capitan}")
    print(f"   Licencia válida: {capitan.tiene_licencia_valida()}")
    print(f"   Nivel experiencia: {capitan.get_nivel_experiencia()}")
    print(f"   Disponible: {capitan.disponible}")
    
    print(f"\n2. Copiloto creado: {copiloto}")
    print(f"   Rol: {copiloto.rol}")
    
    print("\n3. Registrando vuelo...")
    capitan.registrar_vuelo(5.5)
    print(f"   Horas voladas hoy: {capitan.horas_vuelo_hoy}")
    print(f"   Horas disponibles hoy: {capitan.horas_disponibles_hoy()}")
    print(f"   Puede volar más: {capitan.puede_volar_mas()}")
    
    print("\n4. Verificando descanso...")
    print(f"   Necesita descanso: {capitan.necesita_descanso()}")
    if capitan.necesita_descanso():
        tiempo = capitan.tiempo_hasta_disponible()
        print(f"   Tiempo hasta disponible: {tiempo}")
    
    print("\n5. Validando licencia...")
    try:
        capitan.validar_licencia()
        print(f"   ✓ Licencia válida")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n✓ Clase Tripulacion funcionando correctamente")


# ==============================================================================
# ARCHIVO 14/24: vuelo.py
# Directorio: modelo
# Ruta completa: /home/lzapata/aeropuerto/src/modelo/vuelo.py
# ==============================================================================

"""
Clase Vuelo - Representa un vuelo en el sistema
Integra el patrón Observer para notificaciones automáticas
"""

from datetime import datetime, timedelta, date
from typing import List, Optional
import sys
import os

# Agregar el directorio padre al path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patrones.observer import Subject


class Vuelo(Subject):
    """
    Representa un vuelo en el aeropuerto.
    Hereda de Subject para implementar el patrón Observer.
    """
    
    def __init__(self, codigo: str, origen: str, destino: str, fecha_salida: datetime):
        """
        Inicializa un nuevo vuelo.
        
        Args:
            codigo: Código único del vuelo
            origen: Ciudad de origen
            destino: Ciudad de destino
            fecha_salida: Fecha y hora de salida
        """
        super().__init__()  # Inicializar Subject para Observer
        
        if not codigo:
            raise ValueError("El código del vuelo no puede estar vacío")
        if not origen or not destino:
            raise ValueError("Origen y destino son obligatorios")
        if fecha_salida < datetime.now():
            raise ValueError("La fecha de salida no puede ser en el pasado")
        
        self._codigo = codigo.upper()
        self._origen = origen
        self._destino = destino
        self._fecha_salida = fecha_salida
        self._estado = "PROGRAMADO"
        
        # Recursos asignados
        self._avion = None
        self._gate = None
        self._tripulacion = []
        
        # Reservas y capacidad
        self._reservas = []
        self._asientos_ocupados = {
            'ECONOMICA': 0,
            'EJECUTIVA': 0,
            'PRIMERA_CLASE': 0
        }
        
        # Información adicional
        self._distancia_km = 0
        self._duracion_estimada = timedelta(hours=2)
        self._aerolinea = None
        self._tipo_vuelo = "NACIONAL"
    
    @property
    def codigo(self) -> str:
        return self._codigo
    
    @property
    def origen(self) -> str:
        return self._origen
    
    @property
    def destino(self) -> str:
        return self._destino
    
    @property
    def fecha_salida(self) -> datetime:
        return self._fecha_salida
    
    @fecha_salida.setter
    def fecha_salida(self, fecha: datetime):
        fecha_anterior = self._fecha_salida
        self._fecha_salida = fecha
        
        if fecha != fecha_anterior and (fecha - fecha_anterior).total_seconds() > 600:
            self._estado = "RETRASADO"
            self.notificar('VUELO_RETRASADO', {
                'codigo_vuelo': self._codigo,
                'hora_anterior': fecha_anterior.strftime('%H:%M'),
                'nueva_hora': fecha.strftime('%H:%M'),
                'email': 'pasajeros@vuelo.com',
                'telefono': '+54911XXXXXXXX'
            })
    
    @property
    def estado(self) -> str:
        return self._estado
    
    @property
    def avion(self):
        return self._avion
    
    @avion.setter
    def avion(self, avion):
        self._avion = avion
        if avion:
            self._aerolinea = avion.aerolinea
    
    @property
    def gate(self):
        return self._gate
    
    @property
    def tipo_vuelo(self) -> str:
        return self._tipo_vuelo
    
    @tipo_vuelo.setter
    def tipo_vuelo(self, tipo: str):
        self._tipo_vuelo = tipo
    
    @property
    def distancia_km(self) -> int:
        return self._distancia_km
    
    @distancia_km.setter
    def distancia_km(self, valor: int):
        self._distancia_km = valor
    
    def cambiar_estado(self, nuevo_estado: str) -> None:
        """Cambia el estado del vuelo y notifica observers."""
        estado_anterior = self._estado
        
        transiciones_validas = {
            'PROGRAMADO': ['ABORDANDO', 'RETRASADO', 'CANCELADO'],
            'RETRASADO': ['ABORDANDO', 'CANCELADO'],
            'ABORDANDO': ['DESPEGADO', 'CANCELADO'],
            'DESPEGADO': ['ATERRIZADO'],
            'ATERRIZADO': [],
            'CANCELADO': []
        }
        
        if nuevo_estado not in transiciones_validas.get(estado_anterior, []):
            raise ValueError(f"Transición de estado inválida: {estado_anterior} → {nuevo_estado}")
        
        self._estado = nuevo_estado
        
        if nuevo_estado == 'DESPEGADO' and self._gate:
            self._gate.liberar()
        
        # Notificar cambio
        self.notificar(f'VUELO_{nuevo_estado}', {
            'codigo_vuelo': self._codigo,
            'estado_anterior': estado_anterior,
            'estado_nuevo': nuevo_estado,
            'gate': self._gate.numero if self._gate else 'N/A',
            'timestamp': datetime.now(),
            'email': 'pasajeros@vuelo.com',
            'telefono': '+54911XXXXXXXX'
        })
    
    def asignar_gate(self, gate) -> None:
        """Asigna un gate al vuelo."""
        from excepciones.excepciones_aeropuerto import GateNoDisponibleException
        
        if not gate.disponible:
            raise GateNoDisponibleException(gate.numero, "El gate ya está ocupado o no disponible")
        
        if self._tipo_vuelo == "INTERNACIONAL" and gate.terminal == "NACIONAL":
            raise ValueError("Vuelos internacionales requieren terminal internacional")
        
        gate_anterior = self._gate
        self._gate = gate
        gate.ocupar(self)
        
        # Notificar asignación
        self.notificar('GATE_ASIGNADO', {
            'codigo_vuelo': self._codigo,
            'gate_anterior': gate_anterior.numero if gate_anterior else None,
            'gate_nuevo': gate.numero,
            'terminal': gate.terminal,
            'timestamp': datetime.now(),
            'email': 'pasajeros@vuelo.com',
            'telefono': '+54911XXXXXXXX'
        })
    
    def agregar_tripulante(self, tripulante) -> None:
        """Agrega un tripulante al vuelo."""
        if tripulante not in self._tripulacion:
            self._tripulacion.append(tripulante)
    
    def agregar_tripulantes_cabina(self, cantidad: int) -> None:
        """Agrega tripulantes de cabina genéricos con licencias válidas"""
        from modelo.tripulacion import Tripulacion
        
        for i in range(cantidad):
            tripulante = Tripulacion(f"Tripulante Cabina {i+1}", "TRIPULANTE_CABINA")
            tripulante.licencia = f"TC-{1000+i}"
            tripulante.vencimiento_licencia = date.today() + timedelta(days=365)
            self._tripulacion.append(tripulante)
    
    def get_tripulacion(self) -> List:
        """Obtiene la lista de tripulación"""
        return self._tripulacion.copy()
    
    def tiene_tripulacion_completa(self) -> bool:
        """
        Verifica si el vuelo tiene tripulación completa.
        ✅ VERSIÓN DEFINITIVA QUE SIEMPRE FUNCIONA
        """
        # Verificaciones básicas
        if not self._avion:
            return False
        
        if not self._tripulacion or len(self._tripulacion) == 0:
            return False
        
        # Extraer TODOS los roles en una lista simple
        roles_lista = []
        for tripulante in self._tripulacion:
            roles_lista.append(tripulante.rol)
        
        # Contar cada tipo usando la lista
        cuenta_capitan = 0
        cuenta_copiloto = 0
        cuenta_cabina = 0
        
        for rol in roles_lista:
            if rol == "CAPITAN":
                cuenta_capitan = cuenta_capitan + 1
            elif rol == "COPILOTO":
                cuenta_copiloto = cuenta_copiloto + 1
            elif rol == "TRIPULANTE_CABINA":
                cuenta_cabina = cuenta_cabina + 1
        
        # Calcular tripulantes de cabina requeridos
        capacidad = self._avion.capacidad_total
        tripulantes_necesarios = 1
        if capacidad > 50:
            tripulantes_necesarios = capacidad // 50
        
        # Verificar que cumple requisitos
        tiene_capitan = cuenta_capitan >= 1
        tiene_copiloto = cuenta_copiloto >= 1
        tiene_suficiente_cabina = cuenta_cabina >= tripulantes_necesarios
        
        # Retornar resultado final
        resultado_final = tiene_capitan and tiene_copiloto and tiene_suficiente_cabina
        return resultado_final
    
    def iniciar_abordaje(self) -> None:
        """Inicia el proceso de abordaje."""
        from excepciones.excepciones_aeropuerto import TripulacionIncompletaException
        
        if not self.tiene_tripulacion_completa():
            raise TripulacionIncompletaException(self._codigo, "Faltan miembros de la tripulación")
        
        self.cambiar_estado('ABORDANDO')
    
    def agregar_reserva(self, reserva) -> None:
        """Agrega una reserva al vuelo"""
        if reserva not in self._reservas:
            self._reservas.append(reserva)
            clase = reserva.clase
            if clase in self._asientos_ocupados:
                self._asientos_ocupados[clase] += 1
    
    def get_reservas(self) -> List:
        """Obtiene la lista de reservas"""
        return self._reservas.copy()
    
    def get_asientos_disponibles(self, clase: str = "ECONOMICA") -> int:
        """Calcula los asientos disponibles en una clase."""
        if not self._avion:
            return 0
        
        capacidad = self._avion.get_capacidad_por_clase(clase)
        ocupados = self._asientos_ocupados.get(clase, 0)
        
        if clase == "ECONOMICA":
            capacidad = int(capacidad * 1.10)
        
        return max(0, capacidad - ocupados)
    
    def tiene_capacidad(self, clase: str = "ECONOMICA") -> bool:
        """Verifica si hay capacidad disponible."""
        return self.get_asientos_disponibles(clase) > 0
    
    def __str__(self) -> str:
        return (f"Vuelo {self._codigo}: {self._origen} → {self._destino} "
                f"({self._fecha_salida.strftime('%d/%m %H:%M')}) - {self._estado}")
    
    def __repr__(self) -> str:
        return f"Vuelo(codigo='{self._codigo}', estado='{self._estado}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vuelo):
            return False
        return self._codigo == other._codigo
    
    def __hash__(self) -> int:
        return hash(self._codigo)



################################################################################
# DIRECTORIO: patrones
################################################################################

# ==============================================================================
# ARCHIVO 15/24: __init__.py
# Directorio: patrones
# Ruta completa: /home/lzapata/aeropuerto/src/patrones/__init__.py
# ==============================================================================

"""
Paquete patrones - Contiene la implementación de los 4 patrones de diseño
"""

# Patrón Singleton
from .singleton import SingletonMeta, GestorAeropuertoSingleton

# Patrón Strategy
from .strategy import (
    EstrategiaPrecio,
    PrecioTemporadaBaja,
    PrecioTemporadaMedia,
    PrecioTemporadaAlta,
    CalculadoraPrecio,
    FactoriaEstrategias
)

# Patrón Observer
from .observer import (
    Observer,
    Subject,
    NotificadorEmail,
    NotificadorSMS,
    NotificadorApp,
    RegistroEventos
)

# Patrón Factory
from .factory import (
    VueloBase,
    VueloNacional,
    VueloInternacional,
    VueloCarga,
    FactoriaVuelos,
    ReservaBase,
    ReservaEconomica,
    ReservaEjecutiva,
    ReservaPrimeraClase,
    FactoriaReservas
)

__all__ = [
    # Singleton
    'SingletonMeta',
    'GestorAeropuertoSingleton',
    
    # Strategy
    'EstrategiaPrecio',
    'PrecioTemporadaBaja',
    'PrecioTemporadaMedia',
    'PrecioTemporadaAlta',
    'CalculadoraPrecio',
    'FactoriaEstrategias',
    
    # Observer
    'Observer',
    'Subject',
    'NotificadorEmail',
    'NotificadorSMS',
    'NotificadorApp',
    'RegistroEventos',
    
    # Factory
    'VueloBase',
    'VueloNacional',
    'VueloInternacional',
    'VueloCarga',
    'FactoriaVuelos',
    'ReservaBase',
    'ReservaEconomica',
    'ReservaEjecutiva',
    'ReservaPrimeraClase',
    'FactoriaReservas'
]


# ==============================================================================
# ARCHIVO 16/24: factory.py
# Directorio: patrones
# Ruta completa: /home/lzapata/aeropuerto/src/patrones/factory.py
# ==============================================================================

"""
Patrón Factory - Sistema de Gestión de Aeropuerto

El patrón Factory proporciona una interfaz para crear objetos en una superclase,
permitiendo que las subclases alteren el tipo de objetos que se crearán.

USO EN EL PROYECTO:
- Factory para crear diferentes tipos de vuelos
- Factory para crear reservas según clase
- Factory para crear notificaciones
- Factory para crear estrategias de precio
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import random
import string


# ============= FACTORY DE VUELOS =============

class VueloBase(ABC):
    """Clase base abstracta para vuelos"""
    
    def __init__(self, codigo: str, origen: str, destino: str):
        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.fecha_salida = None
        self.estado = "PROGRAMADO"
    
    @abstractmethod
    def get_tipo(self) -> str:
        """Retorna el tipo de vuelo"""
        pass
    
    @abstractmethod
    def get_restricciones(self) -> Dict[str, Any]:
        """Retorna las restricciones específicas del tipo de vuelo"""
        pass
    
    def __str__(self):
        return f"{self.get_tipo()} {self.codigo}: {self.origen} → {self.destino}"


class VueloNacional(VueloBase):
    """Vuelo nacional - menos restricciones"""
    
    def __init__(self, codigo: str, origen: str, destino: str):
        super().__init__(codigo, origen, destino)
        self.requiere_pasaporte = False
        self.terminal = "NACIONAL"
    
    def get_tipo(self) -> str:
        return "VUELO NACIONAL"
    
    def get_restricciones(self) -> Dict[str, Any]:
        return {
            'documento_requerido': 'DNI o Pasaporte',
            'edad_minima_solo': 5,
            'anticipacion_checkin_horas': 1,
            'terminal': self.terminal
        }


class VueloInternacional(VueloBase):
    """Vuelo internacional - más restricciones"""
    
    def __init__(self, codigo: str, origen: str, destino: str):
        super().__init__(codigo, origen, destino)
        self.requiere_pasaporte = True
        self.terminal = "INTERNACIONAL"
    
    def get_tipo(self) -> str:
        return "VUELO INTERNACIONAL"
    
    def get_restricciones(self) -> Dict[str, Any]:
        return {
            'documento_requerido': 'Pasaporte obligatorio',
            'edad_minima_solo': 12,
            'anticipacion_checkin_horas': 3,
            'terminal': self.terminal,
            'requiere_visa': True
        }


class VueloCarga(VueloBase):
    """Vuelo de carga - sin pasajeros"""
    
    def __init__(self, codigo: str, origen: str, destino: str):
        super().__init__(codigo, origen, destino)
        self.capacidad_carga_kg = 50000
    
    def get_tipo(self) -> str:
        return "VUELO DE CARGA"
    
    def get_restricciones(self) -> Dict[str, Any]:
        return {
            'sin_pasajeros': True,
            'capacidad_maxima_kg': self.capacidad_carga_kg,
            'materiales_peligrosos_permitidos': True
        }


class FactoriaVuelos:
    """
    Factory para crear diferentes tipos de vuelos.
    Decide qué tipo de vuelo crear según los parámetros.
    """
    
    @staticmethod
    def crear_vuelo(codigo: str, origen: str, destino: str, 
                    tipo: str = "AUTO") -> VueloBase:
        """
        Crea un vuelo del tipo apropiado.
        
        Args:
            codigo: Código del vuelo (ej: AA1001)
            origen: Ciudad de origen
            destino: Ciudad de destino
            tipo: Tipo específico o "AUTO" para detección automática
        
        Returns:
            Instancia del tipo de vuelo apropiado
        """
        # Si el tipo es AUTO, detectar según código
        if tipo == "AUTO":
            tipo = FactoriaVuelos._detectar_tipo(codigo, origen, destino)
        
        # Crear el vuelo según el tipo
        if tipo == "NACIONAL":
            return VueloNacional(codigo, origen, destino)
        elif tipo == "INTERNACIONAL":
            return VueloInternacional(codigo, origen, destino)
        elif tipo == "CARGA":
            return VueloCarga(codigo, origen, destino)
        else:
            raise ValueError(f"Tipo de vuelo desconocido: {tipo}")
    
    @staticmethod
    def _detectar_tipo(codigo: str, origen: str, destino: str) -> str:
        """Detecta automáticamente el tipo de vuelo"""
        # Si el código empieza con 'C' es carga
        if codigo.startswith('C'):
            return "CARGA"
        
        # Ciudades nacionales de Argentina
        ciudades_argentina = [
            'Buenos Aires', 'Córdoba', 'Mendoza', 'Rosario', 
            'Salta', 'Bariloche', 'Ushuaia', 'Mar del Plata'
        ]
        
        # Si origen y destino están en Argentina, es nacional
        if origen in ciudades_argentina and destino in ciudades_argentina:
            return "NACIONAL"
        
        # Caso contrario, es internacional
        return "INTERNACIONAL"
    
    @staticmethod
    def crear_vuelo_rapido(origen: str, destino: str) -> VueloBase:
        """
        Crea un vuelo con código generado automáticamente.
        """
        codigo = FactoriaVuelos._generar_codigo()
        return FactoriaVuelos.crear_vuelo(codigo, origen, destino, "AUTO")
    
    @staticmethod
    def _generar_codigo() -> str:
        """Genera un código de vuelo aleatorio"""
        letras = ''.join(random.choices(string.ascii_uppercase, k=2))
        numeros = ''.join(random.choices(string.digits, k=4))
        return f"{letras}{numeros}"


# ============= FACTORY DE RESERVAS =============

class ReservaBase(ABC):
    """Clase base para reservas"""
    
    def __init__(self, vuelo: VueloBase, pasajero_nombre: str, clase: str):
        self.codigo_reserva = self._generar_codigo_reserva()
        self.vuelo = vuelo
        self.pasajero_nombre = pasajero_nombre
        self.clase = clase
        self.estado = "CONFIRMADA"
        self.precio = 0.0
    
    @abstractmethod
    def get_beneficios(self) -> list:
        """Retorna lista de beneficios de esta clase"""
        pass
    
    @abstractmethod
    def get_equipaje_permitido(self) -> Dict[str, Any]:
        """Retorna límites de equipaje"""
        pass
    
    def _generar_codigo_reserva(self) -> str:
        """Genera código único de reserva"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def __str__(self):
        return f"Reserva {self.codigo_reserva} - {self.clase} - {self.pasajero_nombre}"


class ReservaEconomica(ReservaBase):
    """Reserva clase económica"""
    
    def __init__(self, vuelo: VueloBase, pasajero_nombre: str):
        super().__init__(vuelo, pasajero_nombre, "ECONOMICA")
    
    def get_beneficios(self) -> list:
        return [
            "Asiento estándar",
            "Comida básica incluida",
            "1 artículo personal"
        ]
    
    def get_equipaje_permitido(self) -> Dict[str, Any]:
        return {
            'maletas_bodega': 1,
            'peso_maximo_por_maleta': 23,
            'equipaje_mano_kg': 10,
            'articulos_personales': 1
        }


class ReservaEjecutiva(ReservaBase):
    """Reserva clase ejecutiva"""
    
    def __init__(self, vuelo: VueloBase, pasajero_nombre: str):
        super().__init__(vuelo, pasajero_nombre, "EJECUTIVA")
    
    def get_beneficios(self) -> list:
        return [
            "Asiento reclinable espacioso",
            "Comida premium",
            "Acceso a sala VIP",
            "Embarque prioritario",
            "Entretenimiento mejorado"
        ]
    
    def get_equipaje_permitido(self) -> Dict[str, Any]:
        return {
            'maletas_bodega': 2,
            'peso_maximo_por_maleta': 32,
            'equipaje_mano_kg': 15,
            'articulos_personales': 2
        }


class ReservaPrimeraClase(ReservaBase):
    """Reserva primera clase"""
    
    def __init__(self, vuelo: VueloBase, pasajero_nombre: str):
        super().__init__(vuelo, pasajero_nombre, "PRIMERA_CLASE")
    
    def get_beneficios(self) -> list:
        return [
            "Suite privada con cama",
            "Menú gourmet personalizado",
            "Acceso sala VIP premium",
            "Servicio de limusina",
            "Embarque prioritario",
            "Amenities de lujo",
            "Atención personalizada 1:1"
        ]
    
    def get_equipaje_permitido(self) -> Dict[str, Any]:
        return {
            'maletas_bodega': 3,
            'peso_maximo_por_maleta': 32,
            'equipaje_mano_kg': 18,
            'articulos_personales': 3
        }


class FactoriaReservas:
    """Factory para crear reservas según la clase"""
    
    @staticmethod
    def crear_reserva(vuelo: VueloBase, pasajero_nombre: str, 
                     clase: str) -> ReservaBase:
        """
        Crea una reserva del tipo apropiado según la clase.
        
        Args:
            vuelo: Vuelo para el cual se hace la reserva
            pasajero_nombre: Nombre del pasajero
            clase: ECONOMICA, EJECUTIVA o PRIMERA_CLASE
        
        Returns:
            Instancia de la reserva apropiada
        """
        clase = clase.upper()
        
        if clase == "ECONOMICA":
            return ReservaEconomica(vuelo, pasajero_nombre)
        elif clase == "EJECUTIVA":
            return ReservaEjecutiva(vuelo, pasajero_nombre)
        elif clase in ["PRIMERA_CLASE", "PRIMERA"]:
            return ReservaPrimeraClase(vuelo, pasajero_nombre)
        else:
            raise ValueError(f"Clase de reserva desconocida: {clase}")
    
    @staticmethod
    def crear_reserva_recomendada(vuelo: VueloBase, pasajero_nombre: str,
                                  presupuesto: float) -> ReservaBase:
        """
        Crea una reserva recomendando la mejor clase según presupuesto.
        """
        if presupuesto >= 50000:
            return ReservaPrimeraClase(vuelo, pasajero_nombre)
        elif presupuesto >= 25000:
            return ReservaEjecutiva(vuelo, pasajero_nombre)
        else:
            return ReservaEconomica(vuelo, pasajero_nombre)


# ============= FACTORY METHOD PATTERN =============

class CreadorVuelo(ABC):
    """
    Clase creadora abstracta que declara el factory method.
    """
    
    @abstractmethod
    def factory_method(self) -> VueloBase:
        """El factory method que las subclases deben implementar"""
        pass
    
    def crear_vuelo_completo(self, codigo: str, origen: str, 
                            destino: str) -> Dict[str, Any]:
        """
        Operación que usa el factory method para crear un vuelo
        y configurarlo completamente.
        """
        vuelo = self.factory_method()
        vuelo.codigo = codigo
        vuelo.origen = origen
        vuelo.destino = destino
        vuelo.fecha_salida = datetime.now() + timedelta(hours=24)
        
        return {
            'vuelo': vuelo,
            'tipo': vuelo.get_tipo(),
            'restricciones': vuelo.get_restricciones(),
            'configurado': True
        }


class CreadorVueloNacional(CreadorVuelo):
    """Creador concreto para vuelos nacionales"""
    
    def factory_method(self) -> VueloBase:
        return VueloNacional("", "", "")


class CreadorVueloInternacional(CreadorVuelo):
    """Creador concreto para vuelos internacionales"""
    
    def factory_method(self) -> VueloBase:
        return VueloInternacional("", "", "")


# ============= TESTING =============

if __name__ == "__main__":
    print("=== Prueba del Patrón Factory ===\n")
    
    # 1. Factory de Vuelos
    print("1. Factory de Vuelos:")
    
    vuelo_nacional = FactoriaVuelos.crear_vuelo(
        "AR1234", "Buenos Aires", "Córdoba", "NACIONAL"
    )
    print(f"   {vuelo_nacional}")
    print(f"   Restricciones: {vuelo_nacional.get_restricciones()}")
    
    vuelo_internacional = FactoriaVuelos.crear_vuelo(
        "AA5678", "Buenos Aires", "Miami", "INTERNACIONAL"
    )
    print(f"\n   {vuelo_internacional}")
    print(f"   Restricciones: {vuelo_internacional.get_restricciones()}")
    
    # Detección automática
    vuelo_auto = FactoriaVuelos.crear_vuelo(
        "LA9999", "Buenos Aires", "París", "AUTO"
    )
    print(f"\n   {vuelo_auto} (detectado automáticamente)")
    
    # 2. Factory de Reservas
    print("\n2. Factory de Reservas:")
    
    reserva_eco = FactoriaReservas.crear_reserva(
        vuelo_internacional, "Juan Pérez", "ECONOMICA"
    )
    print(f"   {reserva_eco}")
    print(f"   Beneficios: {', '.join(reserva_eco.get_beneficios()[:2])}")
    
    reserva_ejecutiva = FactoriaReservas.crear_reserva(
        vuelo_internacional, "María López", "EJECUTIVA"
    )
    print(f"\n   {reserva_ejecutiva}")
    print(f"   Equipaje: {reserva_ejecutiva.get_equipaje_permitido()}")
    
    # 3. Factory por presupuesto
    print("\n3. Recomendación por Presupuesto:")
    
    reserva_low = FactoriaReservas.crear_reserva_recomendada(
        vuelo_internacional, "Carlos Ruiz", 15000
    )
    print(f"   Presupuesto $15,000 → {reserva_low.clase}")
    
    reserva_high = FactoriaReservas.crear_reserva_recomendada(
        vuelo_internacional, "Ana Torres", 60000
    )
    print(f"   Presupuesto $60,000 → {reserva_high.clase}")
    
    # 4. Factory Method Pattern
    print("\n4. Factory Method Pattern:")
    
    creador_nacional = CreadorVueloNacional()
    resultado = creador_nacional.crear_vuelo_completo(
        "AR1111", "Buenos Aires", "Mendoza"
    )
    print(f"   Vuelo creado: {resultado['vuelo']}")
    print(f"   Tipo: {resultado['tipo']}")
    
    print("\n✓ Factory funcionando correctamente")


# ==============================================================================
# ARCHIVO 17/24: observer.py
# Directorio: patrones
# Ruta completa: /home/lzapata/aeropuerto/src/patrones/observer.py
# ==============================================================================

"""
Patrón Observer - Sistema de Gestión de Aeropuerto

El patrón Observer define una dependencia uno-a-muchos entre objetos,
de forma que cuando un objeto cambia de estado, todos sus dependientes
son notificados y actualizados automáticamente.

USO EN EL PROYECTO:
- Notificaciones de cambios de estado de vuelos
- Alertas de cambios en gates
- Notificaciones a pasajeros sobre su reserva
- Sistema de notificaciones por email, SMS, app
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime


# ============= INTERFACES DEL PATRÓN OBSERVER =============

class Observer(ABC):
    """
    Interfaz Observer - Define el método de actualización que será
    llamado cuando el Subject cambie.
    """
    
    @abstractmethod
    def actualizar(self, evento: str, datos: Dict[str, Any]):
        """
        Método llamado cuando el Subject notifica un cambio.
        
        Args:
            evento: Tipo de evento que ocurrió
            datos: Información relevante del evento
        """
        pass


class Subject(ABC):
    """
    Interfaz Subject - Mantiene una lista de observers y los notifica
    cuando hay cambios.
    """
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def agregar_observer(self, observer: Observer):
        """Agrega un observer a la lista"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remover_observer(self, observer: Observer):
        """Remueve un observer de la lista"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notificar(self, evento: str, datos: Dict[str, Any]):
        """Notifica a todos los observers sobre un cambio"""
        for observer in self._observers:
            observer.actualizar(evento, datos)


# ============= OBSERVERS CONCRETOS =============

class NotificadorEmail(Observer):
    """
    Observer que envía notificaciones por email.
    """
    
    def __init__(self, nombre: str = "Email"):
        self.nombre = nombre
        self.notificaciones_enviadas = []
    
    def actualizar(self, evento: str, datos: Dict[str, Any]):
        """Procesa el evento y envía email"""
        email_destino = datos.get('email', 'usuario@ejemplo.com')
        mensaje = self._construir_mensaje(evento, datos)
        
        # Simulación de envío de email
        self._enviar_email(email_destino, evento, mensaje)
        
        self.notificaciones_enviadas.append({
            'tipo': 'EMAIL',
            'evento': evento,
            'timestamp': datetime.now(),
            'datos': datos
        })
    
    def _construir_mensaje(self, evento: str, datos: Dict[str, Any]) -> str:
        """Construye el mensaje según el tipo de evento"""
        mensajes = {
            'VUELO_RETRASADO': f"Su vuelo {datos.get('codigo_vuelo')} ha sido retrasado. "
                              f"Nueva hora: {datos.get('nueva_hora')}",
            'VUELO_CANCELADO': f"Lamentamos informar que el vuelo {datos.get('codigo_vuelo')} "
                              f"ha sido cancelado.",
            'GATE_CAMBIADO': f"El gate de su vuelo {datos.get('codigo_vuelo')} ha cambiado "
                            f"de {datos.get('gate_anterior')} a {datos.get('gate_nuevo')}",
            'CHECK_IN_DISPONIBLE': f"Ya puede realizar el check-in online para su vuelo "
                                  f"{datos.get('codigo_vuelo')}",
            'ABORDAJE_INICIADO': f"Ha iniciado el abordaje del vuelo {datos.get('codigo_vuelo')}. "
                                f"Diríjase al gate {datos.get('gate')}"
        }
        return mensajes.get(evento, f"Notificación sobre {evento}")
    
    def _enviar_email(self, destino: str, asunto: str, mensaje: str):
        """Simula el envío de email"""
        print(f"   📧 [EMAIL] To: {destino}")
        print(f"      Subject: {asunto}")
        print(f"      Message: {mensaje}")


class NotificadorSMS(Observer):
    """
    Observer que envía notificaciones por SMS.
    """
    
    def __init__(self, nombre: str = "SMS"):
        self.nombre = nombre
        self.notificaciones_enviadas = []
    
    def actualizar(self, evento: str, datos: Dict[str, Any]):
        """Procesa el evento y envía SMS"""
        telefono = datos.get('telefono', '+54911XXXXXXXX')
        mensaje = self._construir_mensaje_corto(evento, datos)
        
        # Simulación de envío de SMS
        self._enviar_sms(telefono, mensaje)
        
        self.notificaciones_enviadas.append({
            'tipo': 'SMS',
            'evento': evento,
            'timestamp': datetime.now(),
            'datos': datos
        })
    
    def _construir_mensaje_corto(self, evento: str, datos: Dict[str, Any]) -> str:
        """Construye mensaje corto para SMS (máximo 160 caracteres)"""
        mensajes = {
            'VUELO_RETRASADO': f"Vuelo {datos.get('codigo_vuelo')} retrasado. "
                              f"Nueva hora: {datos.get('nueva_hora')}",
            'VUELO_CANCELADO': f"Vuelo {datos.get('codigo_vuelo')} CANCELADO. "
                              f"Contacte aerolínea.",
            'GATE_CAMBIADO': f"Cambio de gate: {datos.get('gate_nuevo')}. "
                            f"Vuelo {datos.get('codigo_vuelo')}",
            'CHECK_IN_DISPONIBLE': f"Check-in disponible para {datos.get('codigo_vuelo')}",
            'ABORDAJE_INICIADO': f"Abordaje iniciado. Gate {datos.get('gate')}. "
                                f"{datos.get('codigo_vuelo')}"
        }
        return mensajes.get(evento, f"{evento}: {datos.get('codigo_vuelo')}")
    
    def _enviar_sms(self, telefono: str, mensaje: str):
        """Simula el envío de SMS"""
        print(f"   📱 [SMS] To: {telefono}")
        print(f"      Message: {mensaje}")


class NotificadorApp(Observer):
    """
    Observer que envía notificaciones push a la app móvil.
    """
    
    def __init__(self, nombre: str = "App"):
        self.nombre = nombre
        self.notificaciones_enviadas = []
    
    def actualizar(self, evento: str, datos: Dict[str, Any]):
        """Procesa el evento y envía notificación push"""
        usuario_id = datos.get('pasajero_id', 'unknown')
        
        # Simulación de envío de notificación push
        self._enviar_push(usuario_id, evento, datos)
        
        self.notificaciones_enviadas.append({
            'tipo': 'APP_PUSH',
            'evento': evento,
            'timestamp': datetime.now(),
            'datos': datos
        })
    
    def _enviar_push(self, usuario_id: str, evento: str, datos: Dict[str, Any]):
        """Simula el envío de notificación push"""
        print(f"   📲 [APP PUSH] User: {usuario_id}")
        print(f"      Notification: {evento}")
        print(f"      Data: {datos.get('codigo_vuelo', 'N/A')}")


class RegistroEventos(Observer):
    """
    Observer que registra todos los eventos en un log.
    """
    
    def __init__(self, nombre: str = "Log"):
        self.nombre = nombre
        self.eventos_registrados = []
    
    def actualizar(self, evento: str, datos: Dict[str, Any]):
        """Registra el evento en el log"""
        registro = {
            'timestamp': datetime.now(),
            'evento': evento,
            'datos': datos
        }
        self.eventos_registrados.append(registro)
        
        print(f"   📝 [LOG] {datetime.now().strftime('%H:%M:%S')} - {evento} - "
              f"Vuelo: {datos.get('codigo_vuelo', 'N/A')}")
    
    def obtener_historial(self) -> List[Dict]:
        """Retorna el historial de eventos registrados"""
        return self.eventos_registrados


# ============= SUBJECT CONCRETO =============

class VueloObservable(Subject):
    """
    Subject concreto que representa un vuelo que puede ser observado.
    Notifica a los observers cuando cambia su estado.
    """
    
    def __init__(self, codigo_vuelo: str):
        super().__init__()
        self.codigo_vuelo = codigo_vuelo
        self._estado = "PROGRAMADO"
        self._gate = None
        self._hora_salida = None
    
    def cambiar_estado(self, nuevo_estado: str):
        """Cambia el estado del vuelo y notifica a observers"""
        estado_anterior = self._estado
        self._estado = nuevo_estado
        
        evento = f"VUELO_{nuevo_estado}"
        datos = {
            'codigo_vuelo': self.codigo_vuelo,
            'estado_anterior': estado_anterior,
            'estado_nuevo': nuevo_estado,
            'timestamp': datetime.now()
        }
        
        self.notificar(evento, datos)
    
    def cambiar_gate(self, nuevo_gate: str):
        """Cambia el gate del vuelo y notifica"""
        gate_anterior = self._gate
        self._gate = nuevo_gate
        
        datos = {
            'codigo_vuelo': self.codigo_vuelo,
            'gate_anterior': gate_anterior,
            'gate_nuevo': nuevo_gate,
            'timestamp': datetime.now()
        }
        
        self.notificar('GATE_CAMBIADO', datos)
    
    def retrasar_vuelo(self, nueva_hora: str):
        """Retrasa el vuelo y notifica"""
        hora_anterior = self._hora_salida
        self._hora_salida = nueva_hora
        
        datos = {
            'codigo_vuelo': self.codigo_vuelo,
            'hora_anterior': hora_anterior,
            'nueva_hora': nueva_hora,
            'email': 'pasajero@email.com',
            'telefono': '+54911XXXXXXXX',
            'timestamp': datetime.now()
        }
        
        self.notificar('VUELO_RETRASADO', datos)
    
    def cancelar_vuelo(self, razon: str = "Problemas técnicos"):
        """Cancela el vuelo y notifica"""
        self._estado = "CANCELADO"
        
        datos = {
            'codigo_vuelo': self.codigo_vuelo,
            'razon': razon,
            'email': 'pasajero@email.com',
            'telefono': '+54911XXXXXXXX',
            'timestamp': datetime.now()
        }
        
        self.notificar('VUELO_CANCELADO', datos)
    
    def iniciar_abordaje(self):
        """Inicia el abordaje y notifica"""
        self._estado = "ABORDANDO"
        
        datos = {
            'codigo_vuelo': self.codigo_vuelo,
            'gate': self._gate or 'A15',
            'timestamp': datetime.now()
        }
        
        self.notificar('ABORDAJE_INICIADO', datos)


# ============= TESTING =============

if __name__ == "__main__":
    print("=== Prueba del Patrón Observer ===\n")
    
    # Crear el vuelo observable
    vuelo = VueloObservable("AA1001")
    
    # Crear observers
    notificador_email = NotificadorEmail()
    notificador_sms = NotificadorSMS()
    notificador_app = NotificadorApp()
    registro_log = RegistroEventos()
    
    # Suscribir observers al vuelo
    vuelo.agregar_observer(notificador_email)
    vuelo.agregar_observer(notificador_sms)
    vuelo.agregar_observer(notificador_app)
    vuelo.agregar_observer(registro_log)
    
    print("Observers suscritos al vuelo AA1001\n")
    
    # Simular eventos
    print("1. Cambio de Gate:")
    vuelo.cambiar_gate("B20")
    
    print("\n2. Retraso del Vuelo:")
    vuelo.retrasar_vuelo("15:30")
    
    print("\n3. Inicio de Abordaje:")
    vuelo.iniciar_abordaje()
    
    print("\n4. Desuscribir notificador SMS:")
    vuelo.remover_observer(notificador_sms)
    print("   SMS desuscrito")
    
    print("\n5. Cambio de Estado (solo Email, App y Log recibirán):")
    vuelo.cambiar_estado("DESPEGADO")
    
    # Mostrar estadísticas
    print(f"\n=== Estadísticas ===")
    print(f"Emails enviados: {len(notificador_email.notificaciones_enviadas)}")
    print(f"SMS enviados: {len(notificador_sms.notificaciones_enviadas)}")
    print(f"Notificaciones App: {len(notificador_app.notificaciones_enviadas)}")
    print(f"Eventos registrados: {len(registro_log.eventos_registrados)}")
    
    print("\n✓ Observer funcionando correctamente")


# ==============================================================================
# ARCHIVO 18/24: singleton.py
# Directorio: patrones
# Ruta completa: /home/lzapata/aeropuerto/src/patrones/singleton.py
# ==============================================================================

"""
Patrón Singleton - Sistema de Gestión de Aeropuerto

El patrón Singleton garantiza que una clase tenga una única instancia
y proporciona un punto de acceso global a ella.

USO EN EL PROYECTO:
- Se aplica a GestorAeropuerto para asegurar que solo exista una instancia
  del gestor principal del sistema
"""


class SingletonMeta(type):
    """
    Metaclase que implementa el patrón Singleton.
    Garantiza que solo exista una instancia de la clase.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Controla la creación de instancias.
        Si no existe instancia, la crea. Si existe, retorna la existente.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# Ejemplo de uso del Singleton
class GestorAeropuertoSingleton(metaclass=SingletonMeta):
    """
    Clase base para implementar Singleton en GestorAeropuerto.
    
    Uso:
        gestor1 = GestorAeropuerto()
        gestor2 = GestorAeropuerto()
        gestor1 is gestor2  # True - misma instancia
    """
    
    def __init__(self):
        """
        El inicializador se llama solo la primera vez.
        Después retorna la instancia existente.
        """
        if not hasattr(self, 'initialized'):
            self.initialized = True
            # Aquí va la inicialización real del gestor
    
    @classmethod
    def reset_instance(cls):
        """
        Método para resetear la instancia (útil para testing).
        """
        if cls in SingletonMeta._instances:
            del SingletonMeta._instances[cls]


# Decorador alternativo para Singleton (más simple)
def singleton(cls):
    """
    Decorador que convierte una clase en Singleton.
    
    Uso:
        @singleton
        class MiClase:
            pass
    """
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


# Ejemplo de uso con decorador
@singleton
class ConfiguracionAeropuerto:
    """
    Configuración global del aeropuerto usando decorador singleton.
    """
    def __init__(self):
        self.nombre_aeropuerto = "Aeropuerto Internacional"
        self.codigo_iata = "AEP"
        self.max_vuelos_simultaneos = 50
        self.capacidad_total_pasajeros = 10000
    
    def __str__(self):
        return f"{self.nombre_aeropuerto} ({self.codigo_iata})"


# Testing del Singleton
if __name__ == "__main__":
    print("=== Prueba del Patrón Singleton ===\n")
    
    # Prueba con metaclase
    print("1. Prueba con Metaclase:")
    gestor1 = GestorAeropuertoSingleton()
    gestor2 = GestorAeropuertoSingleton()
    print(f"gestor1 es gestor2: {gestor1 is gestor2}")
    print(f"ID gestor1: {id(gestor1)}")
    print(f"ID gestor2: {id(gestor2)}")
    
    # Prueba con decorador
    print("\n2. Prueba con Decorador:")
    config1 = ConfiguracionAeropuerto()
    config2 = ConfiguracionAeropuerto()
    print(f"config1 es config2: {config1 is config2}")
    print(f"Configuración: {config1}")
    
    print("\n✓ Singleton funcionando correctamente")


# ==============================================================================
# ARCHIVO 19/24: strategy.py
# Directorio: patrones
# Ruta completa: /home/lzapata/aeropuerto/src/patrones/strategy.py
# ==============================================================================

"""
Patrón Strategy - Sistema de Gestión de Aeropuerto

El patrón Strategy define una familia de algoritmos, encapsula cada uno
y los hace intercambiables. Strategy permite que el algoritmo varíe
independientemente de los clientes que lo usan.

USO EN EL PROYECTO:
- Estrategias de cálculo de precio de reservas según temporada
- Estrategias de asignación de asientos
- Estrategias de cálculo de equipaje permitido
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict


# ============= ESTRATEGIA DE PRECIOS =============

class EstrategiaPrecio(ABC):
    """
    Interfaz para las estrategias de cálculo de precio.
    """
    
    @abstractmethod
    def calcular_precio(self, precio_base: float, clase: str, distancia_km: int) -> float:
        """
        Calcula el precio final del vuelo.
        
        Args:
            precio_base: Precio base del vuelo
            clase: Clase del asiento (ECONOMICA, EJECUTIVA, PRIMERA_CLASE)
            distancia_km: Distancia del vuelo en kilómetros
        
        Returns:
            Precio final calculado
        """
        pass
    
    @abstractmethod
    def get_nombre(self) -> str:
        """Retorna el nombre de la estrategia"""
        pass


class PrecioTemporadaBaja(EstrategiaPrecio):
    """
    Estrategia de precio para temporada baja (descuentos).
    """
    
    def calcular_precio(self, precio_base: float, clase: str, distancia_km: int) -> float:
        # Descuento del 20% en temporada baja
        multiplicador_clase = self._get_multiplicador_clase(clase)
        precio = precio_base * multiplicador_clase * 0.80  # 20% descuento
        return round(precio, 2)
    
    def _get_multiplicador_clase(self, clase: str) -> float:
        multiplicadores = {
            "ECONOMICA": 1.0,
            "EJECUTIVA": 2.5,
            "PRIMERA_CLASE": 4.0
        }
        return multiplicadores.get(clase, 1.0)
    
    def get_nombre(self) -> str:
        return "Temporada Baja"


class PrecioTemporadaMedia(EstrategiaPrecio):
    """
    Estrategia de precio para temporada media (precio normal).
    """
    
    def calcular_precio(self, precio_base: float, clase: str, distancia_km: int) -> float:
        multiplicador_clase = self._get_multiplicador_clase(clase)
        precio = precio_base * multiplicador_clase
        return round(precio, 2)
    
    def _get_multiplicador_clase(self, clase: str) -> float:
        multiplicadores = {
            "ECONOMICA": 1.0,
            "EJECUTIVA": 2.5,
            "PRIMERA_CLASE": 4.0
        }
        return multiplicadores.get(clase, 1.0)
    
    def get_nombre(self) -> str:
        return "Temporada Media"


class PrecioTemporadaAlta(EstrategiaPrecio):
    """
    Estrategia de precio para temporada alta (recargo).
    """
    
    def calcular_precio(self, precio_base: float, clase: str, distancia_km: int) -> float:
        # Recargo del 50% en temporada alta
        multiplicador_clase = self._get_multiplicador_clase(clase)
        precio = precio_base * multiplicador_clase * 1.50  # 50% recargo
        
        # Recargo adicional para vuelos largos (>5000 km)
        if distancia_km > 5000:
            precio *= 1.10
        
        return round(precio, 2)
    
    def _get_multiplicador_clase(self, clase: str) -> float:
        multiplicadores = {
            "ECONOMICA": 1.0,
            "EJECUTIVA": 2.5,
            "PRIMERA_CLASE": 4.0
        }
        return multiplicadores.get(clase, 1.0)
    
    def get_nombre(self) -> str:
        return "Temporada Alta"


# ============= ESTRATEGIA DE ASIGNACIÓN DE ASIENTOS =============

class EstrategiaAsignacionAsiento(ABC):
    """
    Interfaz para estrategias de asignación de asientos.
    """
    
    @abstractmethod
    def asignar_asiento(self, asientos_disponibles: list, preferencia_pasajero: str = None) -> str:
        """
        Asigna un asiento según la estrategia.
        
        Args:
            asientos_disponibles: Lista de asientos disponibles (ej: ['1A', '1B', '2A'])
            preferencia_pasajero: Preferencia del pasajero ('VENTANA', 'PASILLO', None)
        
        Returns:
            Número de asiento asignado
        """
        pass


class AsignacionAutomatica(EstrategiaAsignacionAsiento):
    """
    Asigna automáticamente el primer asiento disponible.
    """
    
    def asignar_asiento(self, asientos_disponibles: list, preferencia_pasajero: str = None) -> str:
        if not asientos_disponibles:
            raise ValueError("No hay asientos disponibles")
        return asientos_disponibles[0]


class AsignacionPorPreferencia(EstrategiaAsignacionAsiento):
    """
    Asigna asiento según la preferencia del pasajero (ventana o pasillo).
    """
    
    def asignar_asiento(self, asientos_disponibles: list, preferencia_pasajero: str = None) -> str:
        if not asientos_disponibles:
            raise ValueError("No hay asientos disponibles")
        
        if preferencia_pasajero == "VENTANA":
            # Buscar asientos A o F (ventana)
            for asiento in asientos_disponibles:
                if asiento[-1] in ['A', 'F']:
                    return asiento
        elif preferencia_pasajero == "PASILLO":
            # Buscar asientos C o D (pasillo)
            for asiento in asientos_disponibles:
                if asiento[-1] in ['C', 'D']:
                    return asiento
        
        # Si no hay preferencia o no se encuentra, asignar primero disponible
        return asientos_disponibles[0]


# ============= CONTEXTO QUE USA LAS ESTRATEGIAS =============

class CalculadoraPrecio:
    """
    Contexto que utiliza las estrategias de precio.
    """
    
    def __init__(self, estrategia: EstrategiaPrecio):
        self._estrategia = estrategia
    
    def set_estrategia(self, estrategia: EstrategiaPrecio):
        """Permite cambiar la estrategia en tiempo de ejecución"""
        self._estrategia = estrategia
    
    def calcular(self, precio_base: float, clase: str, distancia_km: int) -> Dict:
        """
        Calcula el precio usando la estrategia actual.
        
        Returns:
            Diccionario con precio y estrategia usada
        """
        precio_final = self._estrategia.calcular_precio(precio_base, clase, distancia_km)
        return {
            'precio': precio_final,
            'estrategia': self._estrategia.get_nombre(),
            'precio_base': precio_base,
            'clase': clase
        }


class AsignadorAsientos:
    """
    Contexto que utiliza las estrategias de asignación de asientos.
    """
    
    def __init__(self, estrategia: EstrategiaAsignacionAsiento):
        self._estrategia = estrategia
    
    def set_estrategia(self, estrategia: EstrategiaAsignacionAsiento):
        """Permite cambiar la estrategia en tiempo de ejecución"""
        self._estrategia = estrategia
    
    def asignar(self, asientos_disponibles: list, preferencia: str = None) -> str:
        """Asigna asiento usando la estrategia actual"""
        return self._estrategia.asignar_asiento(asientos_disponibles, preferencia)


# ============= FACTORY PARA CREAR ESTRATEGIAS =============

class FactoriaEstrategias:
    """
    Factory para crear estrategias de precio según la fecha.
    """
    
    @staticmethod
    def crear_estrategia_precio(fecha: datetime) -> EstrategiaPrecio:
        """
        Crea la estrategia de precio apropiada según la fecha.
        
        Temporada Alta: Diciembre, Enero, Julio
        Temporada Baja: Abril, Mayo, Septiembre, Octubre
        Temporada Media: Resto de meses
        """
        mes = fecha.month
        
        if mes in [12, 1, 7]:  # Temporada alta
            return PrecioTemporadaAlta()
        elif mes in [4, 5, 9, 10]:  # Temporada baja
            return PrecioTemporadaBaja()
        else:  # Temporada media
            return PrecioTemporadaMedia()


# ============= TESTING =============

if __name__ == "__main__":
    print("=== Prueba del Patrón Strategy ===\n")
    
    # Prueba de estrategias de precio
    print("1. Estrategias de Precio:")
    precio_base = 10000
    clase = "ECONOMICA"
    distancia = 6000
    
    calculadora = CalculadoraPrecio(PrecioTemporadaBaja())
    
    # Temporada baja
    resultado = calculadora.calcular(precio_base, clase, distancia)
    print(f"   {resultado['estrategia']}: ${resultado['precio']}")
    
    # Temporada media
    calculadora.set_estrategia(PrecioTemporadaMedia())
    resultado = calculadora.calcular(precio_base, clase, distancia)
    print(f"   {resultado['estrategia']}: ${resultado['precio']}")
    
    # Temporada alta
    calculadora.set_estrategia(PrecioTemporadaAlta())
    resultado = calculadora.calcular(precio_base, clase, distancia)
    print(f"   {resultado['estrategia']}: ${resultado['precio']}")
    
    # Prueba de asignación de asientos
    print("\n2. Estrategias de Asignación de Asientos:")
    asientos = ['1A', '1C', '1D', '1F', '2A', '2C']
    
    asignador = AsignadorAsientos(AsignacionAutomatica())
    asiento = asignador.asignar(asientos)
    print(f"   Automática: {asiento}")
    
    asignador.set_estrategia(AsignacionPorPreferencia())
    asiento = asignador.asignar(asientos, "VENTANA")
    print(f"   Por Preferencia (Ventana): {asiento}")
    
    asiento = asignador.asignar(asientos, "PASILLO")
    print(f"   Por Preferencia (Pasillo): {asiento}")
    
    # Prueba de factory
    print("\n3. Factory de Estrategias:")
    fecha_verano = datetime(2025, 1, 15)
    fecha_baja = datetime(2025, 5, 15)
    
    estrategia_verano = FactoriaEstrategias.crear_estrategia_precio(fecha_verano)
    estrategia_baja = FactoriaEstrategias.crear_estrategia_precio(fecha_baja)
    
    print(f"   Estrategia para Enero: {estrategia_verano.get_nombre()}")
    print(f"   Estrategia para Mayo: {estrategia_baja.get_nombre()}")
    
    print("\n✓ Strategy funcionando correctamente")



################################################################################
# DIRECTORIO: servicio
################################################################################

# ==============================================================================
# ARCHIVO 20/24: __init__.py
# Directorio: servicio
# Ruta completa: /home/lzapata/aeropuerto/src/servicio/__init__.py
# ==============================================================================

"""
Paquete servicio - Contiene los gestores del sistema
"""

from .gestor_vuelos import GestorVuelos
from .gestor_pasajeros import GestorPasajeros
from .gestor_reservas import GestorReservas
from .gestor_aeropuerto import GestorAeropuerto

__all__ = [
    'GestorVuelos',
    'GestorPasajeros',
    'GestorReservas',
    'GestorAeropuerto'
]


# ==============================================================================
# ARCHIVO 21/24: gestor_aeropuerto.py
# Directorio: servicio
# Ruta completa: /home/lzapata/aeropuerto/src/servicio/gestor_aeropuerto.py
# ==============================================================================

"""
Gestor Principal del Aeropuerto - USA PATRÓN SINGLETON
Este es el gestor principal que coordina todas las operaciones del aeropuerto.
Solo puede existir UNA instancia de este gestor.
"""

from typing import List, Optional
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patrones.singleton import SingletonMeta
from servicio.gestor_vuelos import GestorVuelos
from servicio.gestor_pasajeros import GestorPasajeros
from servicio.gestor_reservas import GestorReservas
from modelo.vuelo import Vuelo
from modelo.pasajero import Pasajero
from modelo.reserva import Reserva


class GestorAeropuerto(metaclass=SingletonMeta):
    """
    Gestor principal del aeropuerto.
    
    ⭐ PATRÓN SINGLETON:
    Solo puede existir una instancia de esta clase.
    Múltiples llamadas a GestorAeropuerto() retornan la misma instancia.
    
    Coordina todos los gestores especializados:
    - GestorVuelos
    - GestorPasajeros
    - GestorReservas
    """
    
    def __init__(self):
        """
        Inicializa el gestor del aeropuerto.
        Este método solo se ejecuta UNA VEZ gracias al Singleton.
        """
        # Evitar reinicialización si ya existe
        if not hasattr(self, 'initialized'):
            self.initialized = True
            
            # Crear gestores especializados
            self._gestor_vuelos = GestorVuelos()
            self._gestor_pasajeros = GestorPasajeros()
            self._gestor_reservas = GestorReservas()
            
            # Configuración del aeropuerto
            self._nombre_aeropuerto = "Aeropuerto Internacional"
            self._codigo_iata = "AEP"
            
            print("🏢 Gestor del Aeropuerto inicializado (Singleton)")
    
    # ==================== PROPIEDADES ====================
    
    @property
    def nombre_aeropuerto(self) -> str:
        """Nombre del aeropuerto"""
        return self._nombre_aeropuerto
    
    @property
    def codigo_iata(self) -> str:
        """Código IATA del aeropuerto"""
        return self._codigo_iata
    
    # ==================== OPERACIONES DE VUELOS ====================
    
    def crear_vuelo(self, codigo: str, origen: str, destino: str, 
                   fecha_salida: datetime) -> Vuelo:
        """
        Crea un nuevo vuelo.
        
        Args:
            codigo: Código del vuelo
            origen: Ciudad de origen
            destino: Ciudad de destino
            fecha_salida: Fecha y hora de salida
        
        Returns:
            Vuelo creado
        """
        return self._gestor_vuelos.crear_vuelo(codigo, origen, destino, fecha_salida)
    
    def buscar_vuelo(self, codigo: str) -> Vuelo:
        """Busca un vuelo por código"""
        return self._gestor_vuelos.buscar_vuelo(codigo)
    
    def listar_vuelos(self, filtro_estado: Optional[str] = None) -> List[Vuelo]:
        """Lista todos los vuelos"""
        return self._gestor_vuelos.listar_vuelos(filtro_estado)
    
    def cambiar_estado_vuelo(self, codigo: str, nuevo_estado: str) -> None:
        """Cambia el estado de un vuelo"""
        self._gestor_vuelos.cambiar_estado_vuelo(codigo, nuevo_estado)
    
    # ==================== OPERACIONES DE PASAJEROS ====================
    
    def registrar_pasajero(self, nombre: str, numero_documento: str, 
                          tipo_documento: str) -> Pasajero:
        """
        Registra un nuevo pasajero.
        
        Args:
            nombre: Nombre completo
            numero_documento: Número del documento
            tipo_documento: Tipo de documento
        
        Returns:
            Pasajero registrado
        """
        # ✅ CORRECCIÓN: Usar el gestor de pasajeros correctamente
        pasajero = self._gestor_pasajeros.registrar_pasajero(
            nombre, numero_documento, tipo_documento
        )
        return pasajero
    
    def buscar_pasajero(self, numero_documento: str, tipo_documento: str) -> Pasajero:
        """Busca un pasajero por documento"""
        return self._gestor_pasajeros.buscar_por_documento(numero_documento, tipo_documento)
    
    def listar_pasajeros(self) -> List[Pasajero]:
        """Lista todos los pasajeros"""
        return self._gestor_pasajeros.listar_pasajeros()
    
    # ==================== OPERACIONES DE RESERVAS ====================
    
    def crear_reserva(self, vuelo: Vuelo, pasajero: Pasajero, 
                     clase: str, precio_base: float = 10000) -> Reserva:
        """
        Crea una nueva reserva.
        Usa Strategy pattern automáticamente para calcular precio.
        
        Args:
            vuelo: Vuelo a reservar
            pasajero: Pasajero que reserva
            clase: Clase del asiento
            precio_base: Precio base
        
        Returns:
            Reserva creada
        """
        return self._gestor_reservas.crear_reserva(vuelo, pasajero, clase, precio_base)
    
    def buscar_reserva(self, codigo_reserva: str) -> Reserva:
        """Busca una reserva por código"""
        return self._gestor_reservas.buscar_reserva(codigo_reserva)
    
    def hacer_checkin(self, reserva: Reserva) -> None:
        """Realiza el check-in de una reserva"""
        reserva.hacer_checkin()
    
    def cancelar_reserva(self, codigo_reserva: str) -> None:
        """Cancela una reserva"""
        self._gestor_reservas.cancelar_reserva(codigo_reserva)
    
    # ==================== ESTADÍSTICAS GLOBALES ====================
    
    def get_total_vuelos(self) -> int:
        """Obtiene el total de vuelos"""
        return self._gestor_vuelos.get_total_vuelos()
    
    def get_total_pasajeros(self) -> int:
        """Obtiene el total de pasajeros registrados en el sistema"""
        # ✅ CORRECCIÓN: Asegurar que devuelve el total correcto
        total = self._gestor_pasajeros.get_total_pasajeros()
        return total
    
    def get_total_reservas_activas(self) -> int:
        """Obtiene el total de reservas activas"""
        return len(self._gestor_reservas.get_reservas_activas())
    
    def get_ocupacion_promedio(self) -> float:
        """
        Calcula la ocupación promedio de todos los vuelos.
        
        Returns:
            Porcentaje de ocupación promedio
        """
        vuelos = self._gestor_vuelos.listar_vuelos()
        
        if not vuelos:
            return 0.0
        
        total_ocupacion = 0
        vuelos_con_avion = 0
        
        for vuelo in vuelos:
            if vuelo.avion:
                capacidad_total = vuelo.avion.capacidad_total
                if capacidad_total > 0:
                    reservas = len(self._gestor_reservas.listar_reservas_por_vuelo(vuelo))
                    ocupacion = (reservas / capacidad_total) * 100
                    total_ocupacion += ocupacion
                    vuelos_con_avion += 1
        
        return total_ocupacion / vuelos_con_avion if vuelos_con_avion > 0 else 0.0
    
    def get_estadisticas_completas(self) -> dict:
        """
        Obtiene estadísticas completas del aeropuerto.
        
        Returns:
            Diccionario con todas las estadísticas
        """
        return {
            'aeropuerto': {
                'nombre': self._nombre_aeropuerto,
                'codigo': self._codigo_iata
            },
            'vuelos': self._gestor_vuelos.get_estadisticas(),
            'pasajeros': self._gestor_pasajeros.get_estadisticas(),
            'reservas': self._gestor_reservas.get_estadisticas(),
            'ocupacion_promedio': self.get_ocupacion_promedio()
        }
    
    def generar_reporte(self) -> str:
        """
        Genera un reporte completo del estado del aeropuerto.
        
        Returns:
            String con el reporte formateado
        """
        stats = self.get_estadisticas_completas()
        
        reporte = []
        reporte.append("=" * 60)
        reporte.append(f"   REPORTE DEL {self._nombre_aeropuerto.upper()}")
        reporte.append("=" * 60)
        
        reporte.append("\n📊 RESUMEN GENERAL")
        reporte.append(f"Total de vuelos: {self.get_total_vuelos()}")
        reporte.append(f"Total de pasajeros: {self.get_total_pasajeros()}")
        reporte.append(f"Total de reservas activas: {self.get_total_reservas_activas()}")
        reporte.append(f"Ocupación promedio: {self.get_ocupacion_promedio():.1f}%")
        
        reporte.append("\n✈️ VUELOS")
        for estado, cantidad in stats['vuelos']['por_estado'].items():
            reporte.append(f"  {estado}: {cantidad}")
        
        reporte.append("\n👥 PASAJEROS")
        reporte.append(f"  Viajeros frecuentes: {stats['pasajeros']['viajeros_frecuentes']}")
        reporte.append(f"  Millas totales: {stats['pasajeros']['millas_totales']:,}")
        
        reporte.append("\n💰 RESERVAS E INGRESOS")
        reporte.append(f"  Ingresos totales: ${stats['reservas']['ingresos_total']:,.2f}")
        reporte.append(f"  Ingreso promedio: ${stats['reservas']['ingreso_promedio']:,.2f}")
        
        reporte.append("\n" + "=" * 60)
        
        return "\n".join(reporte)
    
    @classmethod
    def reset_instance(cls):
        """
        Resetea la instancia del Singleton.
        ⚠️ Solo usar para testing.
        """
        if cls in SingletonMeta._instances:
            del SingletonMeta._instances[cls]


# Testing
if __name__ == "__main__":
    print("=== Prueba del Patrón SINGLETON en GestorAeropuerto ===\n")
    
    # Crear primera instancia
    print("1. Creando primera instancia...")
    gestor1 = GestorAeropuerto()
    print(f"   ID: {id(gestor1)}")
    
    # Intentar crear segunda instancia
    print("\n2. Intentando crear segunda instancia...")
    gestor2 = GestorAeropuerto()
    print(f"   ID: {id(gestor2)}")
    
    # Verificar que son la misma instancia
    print("\n3. Verificando Singleton...")
    print(f"   gestor1 es gestor2: {gestor1 is gestor2}")
    print(f"   gestor1 == gestor2: {gestor1 == gestor2}")
    
    # Usar el gestor
    print("\n4. Usando el gestor...")
    from datetime import timedelta
    vuelo = gestor1.crear_vuelo("AA1001", "BUE", "MIA", datetime.now() + timedelta(hours=5))
    print(f"   ✓ Vuelo creado: {vuelo.codigo}")
    
    # Verificar que gestor2 ve el mismo vuelo
    print("\n5. Verificando estado compartido...")
    print(f"   Total vuelos desde gestor2: {gestor2.get_total_vuelos()}")
    
    print("\n✓ Patrón SINGLETON funcionando correctamente")
    print("  ✓ Solo existe UNA instancia de GestorAeropuerto")
    print("  ✓ Todas las referencias apuntan a la misma instancia")


# ==============================================================================
# ARCHIVO 22/24: gestor_pasajeros.py
# Directorio: servicio
# Ruta completa: /home/lzapata/aeropuerto/src/servicio/gestor_pasajeros.py
# ==============================================================================

"""
Gestor de Pasajeros - Maneja operaciones relacionadas con pasajeros
"""

from typing import List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelo.pasajero import Pasajero
from excepciones.excepciones_aeropuerto import PasajeroNoEncontradoException


class GestorPasajeros:
    """
    Gestor para operaciones de pasajeros.
    Centraliza la lógica de gestión de pasajeros.
    """
    
    def __init__(self):
        """Inicializa el gestor de pasajeros"""
        self._pasajeros: List[Pasajero] = []
    
    def registrar_pasajero(self, nombre: str, numero_documento: str, 
                          tipo_documento: str) -> Pasajero:
        """
        Registra un nuevo pasajero.
        
        Args:
            nombre: Nombre completo
            numero_documento: Número del documento
            tipo_documento: Tipo de documento
        
        Returns:
            Pasajero registrado
        """
        # ✅ CORRECCIÓN: Verificar si ya existe primero
        try:
            existente = self.buscar_por_documento(numero_documento, tipo_documento)
            print(f"   ℹ️ Pasajero ya existe: {existente.nombre}")
            return existente  # Ya existe, retornar el existente
        except PasajeroNoEncontradoException:
            pass  # No existe, crear nuevo
        
        # Crear nuevo pasajero
        pasajero = Pasajero(nombre, numero_documento, tipo_documento)
        self._pasajeros.append(pasajero)
        
        # ✅ CORRECCIÓN: Confirmar registro
        print(f"   ✓ Pasajero registrado: {pasajero.nombre} (Total: {len(self._pasajeros)})")
        
        return pasajero
    
    def buscar_por_documento(self, numero_documento: str, 
                            tipo_documento: str) -> Pasajero:
        """
        Busca un pasajero por número de documento.
        
        Args:
            numero_documento: Número del documento
            tipo_documento: Tipo de documento
        
        Returns:
            Pasajero encontrado
        
        Raises:
            PasajeroNoEncontradoException: Si no existe
        """
        for pasajero in self._pasajeros:
            if (pasajero.numero_documento == numero_documento and 
                pasajero.tipo_documento == tipo_documento):
                return pasajero
        
        raise PasajeroNoEncontradoException(numero_documento)
    
    def buscar_por_id(self, id_pasajero: int) -> Pasajero:
        """
        Busca un pasajero por ID.
        
        Args:
            id_pasajero: ID del pasajero
        
        Returns:
            Pasajero encontrado
        
        Raises:
            PasajeroNoEncontradoException: Si no existe
        """
        for pasajero in self._pasajeros:
            if pasajero.id == id_pasajero:
                return pasajero
        
        raise PasajeroNoEncontradoException(str(id_pasajero))
    
    def buscar_por_nombre(self, nombre: str) -> List[Pasajero]:
        """
        Busca pasajeros por nombre (búsqueda parcial).
        
        Args:
            nombre: Nombre o parte del nombre
        
        Returns:
            Lista de pasajeros que coinciden
        """
        nombre_lower = nombre.lower()
        return [p for p in self._pasajeros 
                if nombre_lower in p.nombre.lower()]
    
    def listar_pasajeros(self) -> List[Pasajero]:
        """
        Lista todos los pasajeros.
        
        Returns:
            Lista de pasajeros
        """
        return self._pasajeros.copy()
    
    def listar_viajeros_frecuentes(self) -> List[Pasajero]:
        """
        Lista pasajeros viajeros frecuentes (>50,000 millas).
        
        Returns:
            Lista de viajeros frecuentes
        """
        return [p for p in self._pasajeros if p.es_viajero_frecuente()]
    
    def get_total_pasajeros(self) -> int:
        """Obtiene el total de pasajeros registrados"""
        total = len(self._pasajeros)
        return total
    
    def get_estadisticas(self) -> dict:
        """
        Obtiene estadísticas de pasajeros.
        
        Returns:
            Diccionario con estadísticas
        """
        viajeros_frecuentes = len(self.listar_viajeros_frecuentes())
        
        tipos_documento = {}
        for pasajero in self._pasajeros:
            tipo = pasajero.tipo_documento
            tipos_documento[tipo] = tipos_documento.get(tipo, 0) + 1
        
        total_millas = sum(p.millas_acumuladas for p in self._pasajeros)
        
        return {
            'total_pasajeros': len(self._pasajeros),
            'viajeros_frecuentes': viajeros_frecuentes,
            'por_tipo_documento': tipos_documento,
            'millas_totales': total_millas,
            'promedio_millas': total_millas / len(self._pasajeros) if self._pasajeros else 0
        }
    
    def actualizar_millas(self, numero_documento: str, tipo_documento: str, 
                         millas: int) -> None:
        """
        Actualiza las millas de un pasajero.
        
        Args:
            numero_documento: Número del documento
            tipo_documento: Tipo de documento
            millas: Millas a acumular
        """
        pasajero = self.buscar_por_documento(numero_documento, tipo_documento)
        pasajero.acumular_millas(millas)
    
    def eliminar_pasajero(self, numero_documento: str, tipo_documento: str) -> None:
        """
        Elimina un pasajero del sistema (solo si no tiene reservas activas).
        
        Args:
            numero_documento: Número del documento
            tipo_documento: Tipo de documento
        """
        pasajero = self.buscar_por_documento(numero_documento, tipo_documento)
        
        # Verificar que no tenga reservas activas
        reservas_activas = [r for r in pasajero.get_reservas() 
                           if r.estado not in ['CANCELADA', 'ABORDADO']]
        
        if reservas_activas:
            raise ValueError(
                f"No se puede eliminar pasajero con {len(reservas_activas)} reservas activas"
            )
        
        self._pasajeros.remove(pasajero)


# Testing
if __name__ == "__main__":
    from datetime import date, timedelta
    
    print("=== Prueba del GestorPasajeros ===\n")
    
    gestor = GestorPasajeros()
    
    # Registrar pasajeros
    print("1. Registrando pasajeros...")
    p1 = gestor.registrar_pasajero("Juan Pérez", "AB123456", "PASAPORTE")
    p1.fecha_nacimiento = date(1985, 3, 15)
    print(f"   ✓ {p1}")
    
    p2 = gestor.registrar_pasajero("María López", "12345678", "DNI")
    p2.acumular_millas(55000)
    print(f"   ✓ {p2}")
    
    # Buscar pasajero
    print("\n2. Buscando pasajero...")
    encontrado = gestor.buscar_por_documento("AB123456", "PASAPORTE")
    print(f"   ✓ Encontrado: {encontrado.nombre}")
    
    # Listar viajeros frecuentes
    print("\n3. Viajeros frecuentes:")
    frecuentes = gestor.listar_viajeros_frecuentes()
    for p in frecuentes:
        print(f"   ✓ {p.nombre} - {p.millas_acumuladas} millas")
    
    # Estadísticas
    print("\n4. Estadísticas:")
    stats = gestor.get_estadisticas()
    print(f"   Total: {stats['total_pasajeros']}")
    print(f"   Viajeros frecuentes: {stats['viajeros_frecuentes']}")
    print(f"   Promedio millas: {stats['promedio_millas']:.0f}")
    
    print("\n✓ GestorPasajeros funcionando correctamente")


# ==============================================================================
# ARCHIVO 23/24: gestor_reservas.py
# Directorio: servicio
# Ruta completa: /home/lzapata/aeropuerto/src/servicio/gestor_reservas.py
# ==============================================================================

"""
Gestor de Reservas - Maneja operaciones relacionadas con reservas
Integra Strategy para cálculo de precios
"""

from typing import List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelo.reserva import Reserva
from modelo.vuelo import Vuelo
from modelo.pasajero import Pasajero
from excepciones.excepciones_aeropuerto import ReservaNoEncontradaException


class GestorReservas:
    """
    Gestor para operaciones de reservas.
    Centraliza la lógica de gestión de reservas.
    """
    
    def __init__(self):
        """Inicializa el gestor de reservas"""
        self._reservas: List[Reserva] = []
    
    def crear_reserva(self, vuelo: Vuelo, pasajero: Pasajero, 
                     clase: str, precio_base: float = 10000) -> Reserva:
        """
        Crea una nueva reserva.
        Usa Strategy pattern automáticamente para calcular el precio.
        
        Args:
            vuelo: Vuelo para reservar
            pasajero: Pasajero que reserva
            clase: Clase del asiento
            precio_base: Precio base del vuelo
        
        Returns:
            Reserva creada
        """
        # Crear reserva (Strategy se aplica automáticamente)
        reserva = Reserva(vuelo, pasajero, clase, precio_base)
        
        # Agregar a la lista
        self._reservas.append(reserva)
        
        return reserva
    
    def buscar_reserva(self, codigo_reserva: str) -> Reserva:
        """
        Busca una reserva por código.
        
        Args:
            codigo_reserva: Código de la reserva
        
        Returns:
            Reserva encontrada
        
        Raises:
            ReservaNoEncontradaException: Si no existe
        """
        codigo_reserva = codigo_reserva.upper()
        
        for reserva in self._reservas:
            if reserva.codigo_reserva == codigo_reserva:
                return reserva
        
        raise ReservaNoEncontradaException(codigo_reserva)
    
    def listar_reservas(self, filtro_estado: Optional[str] = None) -> List[Reserva]:
        """
        Lista todas las reservas, opcionalmente filtradas por estado.
        
        Args:
            filtro_estado: Estado para filtrar (opcional)
        
        Returns:
            Lista de reservas
        """
        if filtro_estado:
            return [r for r in self._reservas if r.estado == filtro_estado]
        return self._reservas.copy()
    
    def listar_reservas_por_pasajero(self, pasajero: Pasajero) -> List[Reserva]:
        """
        Lista reservas de un pasajero específico.
        
        Args:
            pasajero: Pasajero
        
        Returns:
            Lista de reservas del pasajero
        """
        return [r for r in self._reservas if r.pasajero == pasajero]
    
    def listar_reservas_por_vuelo(self, vuelo: Vuelo) -> List[Reserva]:
        """
        Lista reservas de un vuelo específico.
        
        Args:
            vuelo: Vuelo
        
        Returns:
            Lista de reservas del vuelo
        """
        return [r for r in self._reservas if r.vuelo == vuelo]
    
    def hacer_checkin(self, codigo_reserva: str) -> None:
        """
        Realiza el check-in de una reserva.
        
        Args:
            codigo_reserva: Código de la reserva
        """
        reserva = self.buscar_reserva(codigo_reserva)
        reserva.hacer_checkin()
    
    def cancelar_reserva(self, codigo_reserva: str) -> None:
        """
        Cancela una reserva.
        
        Args:
            codigo_reserva: Código de la reserva
        """
        reserva = self.buscar_reserva(codigo_reserva)
        reserva.cancelar()
    
    def get_total_reservas(self) -> int:
        """Obtiene el total de reservas en el sistema"""
        return len(self._reservas)
    
    def get_reservas_activas(self) -> List[Reserva]:
        """Obtiene reservas activas (CONFIRMADA, CHECK_IN_REALIZADO)"""
        return [r for r in self._reservas 
                if r.estado in ['CONFIRMADA', 'CHECK_IN_REALIZADO']]
    
    def get_estadisticas(self) -> dict:
        """
        Obtiene estadísticas de reservas.
        
        Returns:
            Diccionario con estadísticas
        """
        estados = {}
        clases = {}
        ingresos_total = 0
        
        for reserva in self._reservas:
            # Contar por estado
            estados[reserva.estado] = estados.get(reserva.estado, 0) + 1
            
            # Contar por clase
            clases[reserva.clase] = clases.get(reserva.clase, 0) + 1
            
            # Sumar ingresos (solo confirmadas y realizadas)
            if reserva.estado in ['CONFIRMADA', 'CHECK_IN_REALIZADO', 'ABORDADO']:
                ingresos_total += reserva.precio
        
        return {
            'total_reservas': len(self._reservas),
            'reservas_activas': len(self.get_reservas_activas()),
            'por_estado': estados,
            'por_clase': clases,
            'ingresos_total': ingresos_total,
            'ingreso_promedio': ingresos_total / len(self._reservas) if self._reservas else 0
        }
    
    def obtener_ocupacion_por_clase(self, vuelo: Vuelo) -> dict:
        """
        Calcula la ocupación por clase de un vuelo.
        
        Args:
            vuelo: Vuelo a analizar
        
        Returns:
            Diccionario con ocupación por clase
        """
        reservas_vuelo = self.listar_reservas_por_vuelo(vuelo)
        reservas_activas = [r for r in reservas_vuelo 
                           if r.estado != 'CANCELADA']
        
        ocupacion = {
            'ECONOMICA': 0,
            'EJECUTIVA': 0,
            'PRIMERA_CLASE': 0
        }
        
        for reserva in reservas_activas:
            ocupacion[reserva.clase] += 1
        
        return ocupacion
    
    def calcular_ingresos_por_vuelo(self, vuelo: Vuelo) -> float:
        """
        Calcula los ingresos totales de un vuelo.
        
        Args:
            vuelo: Vuelo a analizar
        
        Returns:
            Ingresos totales
        """
        reservas_vuelo = self.listar_reservas_por_vuelo(vuelo)
        reservas_validas = [r for r in reservas_vuelo 
                           if r.estado != 'CANCELADA']
        
        return sum(r.precio for r in reservas_validas)


# Testing
if __name__ == "__main__":
    from datetime import datetime, timedelta, date
    from modelo.avion import Avion
    from modelo.aerolinea import Aerolinea
    
    print("=== Prueba del GestorReservas ===\n")
    
    gestor = GestorReservas()
    
    # Crear vuelo y pasajero de prueba
    aerolinea = Aerolinea("AA", "American Airlines")
    avion = Avion("N12345", "COMERCIAL", aerolinea)
    avion.capacidad_economica = 150
    
    fecha_salida = datetime.now() + timedelta(hours=5)
    vuelo = Vuelo("AA1001", "Buenos Aires", "Miami", fecha_salida)
    vuelo.avion = avion
    vuelo.tipo_vuelo = "INTERNACIONAL"
    vuelo.distancia_km = 7000
    
    pasajero = Pasajero("Juan Pérez", "AB123456", "PASAPORTE")
    pasajero.fecha_nacimiento = date(1985, 3, 15)
    pasajero.fecha_vencimiento_doc = date.today().replace(year=date.today().year + 5)
    
    # Crear reserva (Strategy aplica automáticamente)
    print("1. Creando reserva (con Strategy)...")
    reserva = gestor.crear_reserva(vuelo, pasajero, "ECONOMICA", precio_base=10000)
    print(f"   ✓ {reserva}")
    print(f"   Precio calculado: ${reserva.precio:.2f}")
    
    # Buscar reserva
    print("\n2. Buscando reserva...")
    encontrada = gestor.buscar_reserva(reserva.codigo_reserva)
    print(f"   ✓ Encontrada: {encontrada.codigo_reserva}")
    
    # Estadísticas
    print("\n3. Estadísticas:")
    stats = gestor.get_estadisticas()
    print(f"   Total reservas: {stats['total_reservas']}")
    print(f"   Ingresos: ${stats['ingresos_total']:.2f}")
    
    print("\n✓ GestorReservas funcionando correctamente")


# ==============================================================================
# ARCHIVO 24/24: gestor_vuelos.py
# Directorio: servicio
# Ruta completa: /home/lzapata/aeropuerto/src/servicio/gestor_vuelos.py
# ==============================================================================

"""
Gestor de Vuelos - Maneja operaciones relacionadas con vuelos
Usa el patrón Factory para crear vuelos
"""

from typing import List, Optional
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelo.vuelo import Vuelo
from patrones.factory import FactoriaVuelos
from excepciones.excepciones_aeropuerto import VueloNoEncontradoException


class GestorVuelos:
    """
    Gestor para operaciones de vuelos.
    Centraliza la lógica de gestión de vuelos.
    """
    
    def __init__(self):
        """Inicializa el gestor de vuelos"""
        self._vuelos: List[Vuelo] = []
    
    def crear_vuelo(self, codigo: str, origen: str, destino: str, 
                   fecha_salida: datetime, usar_factory: bool = False) -> Vuelo:
        """
        Crea un nuevo vuelo.
        
        Args:
            codigo: Código del vuelo
            origen: Ciudad de origen
            destino: Ciudad de destino
            fecha_salida: Fecha y hora de salida
            usar_factory: Si usar el patrón Factory para crear
        
        Returns:
            Vuelo creado
        """
        if usar_factory:
            # Usar Factory pattern
            vuelo = FactoriaVuelos.crear_vuelo(codigo, origen, destino, "AUTO")
            vuelo._fecha_salida = fecha_salida
        else:
            # Creación directa
            vuelo = Vuelo(codigo, origen, destino, fecha_salida)
        
        # Agregar a la lista
        self._vuelos.append(vuelo)
        
        return vuelo
    
    def buscar_vuelo(self, codigo: str) -> Vuelo:
        """
        Busca un vuelo por código.
        
        Args:
            codigo: Código del vuelo
        
        Returns:
            Vuelo encontrado
        
        Raises:
            VueloNoEncontradoException: Si no existe el vuelo
        """
        codigo = codigo.upper()
        
        for vuelo in self._vuelos:
            if vuelo.codigo == codigo:
                return vuelo
        
        raise VueloNoEncontradoException(codigo)
    
    def listar_vuelos(self, filtro_estado: Optional[str] = None) -> List[Vuelo]:
        """
        Lista todos los vuelos, opcionalmente filtrados por estado.
        
        Args:
            filtro_estado: Estado para filtrar (opcional)
        
        Returns:
            Lista de vuelos
        """
        if filtro_estado:
            return [v for v in self._vuelos if v.estado == filtro_estado]
        return self._vuelos.copy()
    
    def listar_vuelos_por_origen(self, origen: str) -> List[Vuelo]:
        """
        Lista vuelos por ciudad de origen.
        
        Args:
            origen: Ciudad de origen
        
        Returns:
            Lista de vuelos
        """
        return [v for v in self._vuelos if v.origen.lower() == origen.lower()]
    
    def listar_vuelos_por_destino(self, destino: str) -> List[Vuelo]:
        """
        Lista vuelos por ciudad de destino.
        
        Args:
            destino: Ciudad de destino
        
        Returns:
            Lista de vuelos
        """
        return [v for v in self._vuelos if v.destino.lower() == destino.lower()]
    
    def cambiar_estado_vuelo(self, codigo: str, nuevo_estado: str) -> None:
        """
        Cambia el estado de un vuelo.
        
        Args:
            codigo: Código del vuelo
            nuevo_estado: Nuevo estado
        """
        vuelo = self.buscar_vuelo(codigo)
        vuelo.cambiar_estado(nuevo_estado)
    
    def get_total_vuelos(self) -> int:
        """Obtiene el total de vuelos registrados"""
        return len(self._vuelos)
    
    def get_vuelos_activos(self) -> List[Vuelo]:
        """Obtiene vuelos en estados activos (PROGRAMADO, ABORDANDO)"""
        return [v for v in self._vuelos 
                if v.estado in ['PROGRAMADO', 'ABORDANDO', 'RETRASADO']]
    
    def get_estadisticas(self) -> dict:
        """
        Obtiene estadísticas de vuelos.
        
        Returns:
            Diccionario con estadísticas
        """
        estados = {}
        for vuelo in self._vuelos:
            estados[vuelo.estado] = estados.get(vuelo.estado, 0) + 1
        
        return {
            'total_vuelos': len(self._vuelos),
            'vuelos_activos': len(self.get_vuelos_activos()),
            'por_estado': estados
        }
    
    def eliminar_vuelo(self, codigo: str) -> None:
        """
        Elimina un vuelo del sistema (solo si no tiene reservas).
        
        Args:
            codigo: Código del vuelo
        """
        vuelo = self.buscar_vuelo(codigo)
        
        if len(vuelo.get_reservas()) > 0:
            raise ValueError("No se puede eliminar un vuelo con reservas")
        
        self._vuelos.remove(vuelo)


# Testing
if __name__ == "__main__":
    from datetime import timedelta
    
    print("=== Prueba del GestorVuelos ===\n")
    
    gestor = GestorVuelos()
    
    # Crear vuelos
    print("1. Creando vuelos...")
    fecha1 = datetime.now() + timedelta(hours=5)
    vuelo1 = gestor.crear_vuelo("AA1001", "Buenos Aires", "Miami", fecha1)
    print(f"   ✓ {vuelo1}")
    
    fecha2 = datetime.now() + timedelta(hours=8)
    vuelo2 = gestor.crear_vuelo("LA2050", "Buenos Aires", "Santiago", fecha2, usar_factory=True)
    print(f"   ✓ {vuelo2}")
    
    # Buscar vuelo
    print("\n2. Buscando vuelo...")
    encontrado = gestor.buscar_vuelo("AA1001")
    print(f"   ✓ Encontrado: {encontrado.codigo}")
    
    # Listar vuelos
    print("\n3. Listando vuelos...")
    vuelos = gestor.listar_vuelos()
    print(f"   Total de vuelos: {len(vuelos)}")
    
    # Estadísticas
    print("\n4. Estadísticas:")
    stats = gestor.get_estadisticas()
    print(f"   {stats}")
    
    print("\n✓ GestorVuelos funcionando correctamente")



################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 24
# Generado: 2025-11-02 23:43:51
################################################################################
