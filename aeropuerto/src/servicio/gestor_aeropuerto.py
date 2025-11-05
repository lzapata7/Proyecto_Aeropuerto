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
