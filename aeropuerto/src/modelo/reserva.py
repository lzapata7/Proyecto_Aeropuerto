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
