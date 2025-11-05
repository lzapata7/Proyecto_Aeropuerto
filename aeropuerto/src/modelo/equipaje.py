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
