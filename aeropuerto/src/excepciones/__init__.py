"""
Paquete excepciones - Contiene todas las excepciones personalizadas del sistema
"""

from .excepciones_aeropuerto import (
    AeropuertoException,
    VueloLlenoException,
    VueloNoEncontradoException,
    PasajeroNoEncontradoException,
    ReservaNoEncontradaException,
    DocumentoInvalidoException,
    CheckInNoDisponibleException,
    GateNoDisponibleException,
    EquipajeExcedidoException,
    VueloYaDespegadoException,
    EdadInsuficienteException,
    TripulacionIncompletaException
)

__all__ = [
    'AeropuertoException',
    'VueloLlenoException',
    'VueloNoEncontradoException',
    'PasajeroNoEncontradoException',
    'ReservaNoEncontradaException',
    'DocumentoInvalidoException',
    'CheckInNoDisponibleException',
    'GateNoDisponibleException',
    'EquipajeExcedidoException',
    'VueloYaDespegadoException',
    'EdadInsuficienteException',
    'TripulacionIncompletaException'
]
