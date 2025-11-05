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
