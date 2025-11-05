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
