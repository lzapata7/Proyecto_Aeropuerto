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
