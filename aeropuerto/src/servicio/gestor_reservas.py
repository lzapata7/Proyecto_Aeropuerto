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
