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
