"""
Patrón Singleton - Sistema de Gestión de Aeropuerto

El patrón Singleton garantiza que una clase tenga una única instancia
y proporciona un punto de acceso global a ella.

USO EN EL PROYECTO:
- Se aplica a GestorAeropuerto para asegurar que solo exista una instancia
  del gestor principal del sistema
"""


class SingletonMeta(type):
    """
    Metaclase que implementa el patrón Singleton.
    Garantiza que solo exista una instancia de la clase.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Controla la creación de instancias.
        Si no existe instancia, la crea. Si existe, retorna la existente.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# Ejemplo de uso del Singleton
class GestorAeropuertoSingleton(metaclass=SingletonMeta):
    """
    Clase base para implementar Singleton en GestorAeropuerto.
    
    Uso:
        gestor1 = GestorAeropuerto()
        gestor2 = GestorAeropuerto()
        gestor1 is gestor2  # True - misma instancia
    """
    
    def __init__(self):
        """
        El inicializador se llama solo la primera vez.
        Después retorna la instancia existente.
        """
        if not hasattr(self, 'initialized'):
            self.initialized = True
            # Aquí va la inicialización real del gestor
    
    @classmethod
    def reset_instance(cls):
        """
        Método para resetear la instancia (útil para testing).
        """
        if cls in SingletonMeta._instances:
            del SingletonMeta._instances[cls]


# Decorador alternativo para Singleton (más simple)
def singleton(cls):
    """
    Decorador que convierte una clase en Singleton.
    
    Uso:
        @singleton
        class MiClase:
            pass
    """
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


# Ejemplo de uso con decorador
@singleton
class ConfiguracionAeropuerto:
    """
    Configuración global del aeropuerto usando decorador singleton.
    """
    def __init__(self):
        self.nombre_aeropuerto = "Aeropuerto Internacional"
        self.codigo_iata = "AEP"
        self.max_vuelos_simultaneos = 50
        self.capacidad_total_pasajeros = 10000
    
    def __str__(self):
        return f"{self.nombre_aeropuerto} ({self.codigo_iata})"


# Testing del Singleton
if __name__ == "__main__":
    print("=== Prueba del Patrón Singleton ===\n")
    
    # Prueba con metaclase
    print("1. Prueba con Metaclase:")
    gestor1 = GestorAeropuertoSingleton()
    gestor2 = GestorAeropuertoSingleton()
    print(f"gestor1 es gestor2: {gestor1 is gestor2}")
    print(f"ID gestor1: {id(gestor1)}")
    print(f"ID gestor2: {id(gestor2)}")
    
    # Prueba con decorador
    print("\n2. Prueba con Decorador:")
    config1 = ConfiguracionAeropuerto()
    config2 = ConfiguracionAeropuerto()
    print(f"config1 es config2: {config1 is config2}")
    print(f"Configuración: {config1}")
    
    print("\n✓ Singleton funcionando correctamente")
