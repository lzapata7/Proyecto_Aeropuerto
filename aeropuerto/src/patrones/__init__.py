"""
Paquete patrones - Contiene la implementación de los 4 patrones de diseño
"""

# Patrón Singleton
from .singleton import SingletonMeta, GestorAeropuertoSingleton

# Patrón Strategy
from .strategy import (
    EstrategiaPrecio,
    PrecioTemporadaBaja,
    PrecioTemporadaMedia,
    PrecioTemporadaAlta,
    CalculadoraPrecio,
    FactoriaEstrategias
)

# Patrón Observer
from .observer import (
    Observer,
    Subject,
    NotificadorEmail,
    NotificadorSMS,
    NotificadorApp,
    RegistroEventos
)

# Patrón Factory
from .factory import (
    VueloBase,
    VueloNacional,
    VueloInternacional,
    VueloCarga,
    FactoriaVuelos,
    ReservaBase,
    ReservaEconomica,
    ReservaEjecutiva,
    ReservaPrimeraClase,
    FactoriaReservas
)

__all__ = [
    # Singleton
    'SingletonMeta',
    'GestorAeropuertoSingleton',
    
    # Strategy
    'EstrategiaPrecio',
    'PrecioTemporadaBaja',
    'PrecioTemporadaMedia',
    'PrecioTemporadaAlta',
    'CalculadoraPrecio',
    'FactoriaEstrategias',
    
    # Observer
    'Observer',
    'Subject',
    'NotificadorEmail',
    'NotificadorSMS',
    'NotificadorApp',
    'RegistroEventos',
    
    # Factory
    'VueloBase',
    'VueloNacional',
    'VueloInternacional',
    'VueloCarga',
    'FactoriaVuelos',
    'ReservaBase',
    'ReservaEconomica',
    'ReservaEjecutiva',
    'ReservaPrimeraClase',
    'FactoriaReservas'
]
