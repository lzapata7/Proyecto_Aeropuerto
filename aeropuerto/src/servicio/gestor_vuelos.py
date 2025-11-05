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
