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
