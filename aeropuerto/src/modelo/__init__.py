"""
Paquete modelo - Contiene todas las clases del dominio del aeropuerto
"""

from .enums import (
    EstadoVuelo,
    EstadoReserva,
    ClaseAsiento,
    TipoDocumento,
    Terminal,
    RolTripulacion,
    TipoAvion
)

from .aerolinea import Aerolinea
from .avion import Avion
from .gate import Gate
from .equipaje import Equipaje
from .tripulacion import Tripulacion
from .pasajero import Pasajero
from .vuelo import Vuelo
from .reserva import Reserva

__all__ = [
    # Enumeraciones
    'EstadoVuelo',
    'EstadoReserva',
    'ClaseAsiento',
    'TipoDocumento',
    'Terminal',
    'RolTripulacion',
    'TipoAvion',
    
    # Clases del modelo
    'Aerolinea',
    'Avion',
    'Gate',
    'Equipaje',
    'Tripulacion',
    'Pasajero',
    'Vuelo',
    'Reserva'
]
