"""
Enumeraciones del Sistema de Gestión de Aeropuerto
Contiene todos los tipos enumerados utilizados en el dominio
"""

from enum import Enum


class EstadoVuelo(Enum):
    """Estados posibles de un vuelo"""
    PROGRAMADO = "PROGRAMADO"
    ABORDANDO = "ABORDANDO"
    DESPEGADO = "DESPEGADO"
    ATERRIZADO = "ATERRIZADO"
    CANCELADO = "CANCELADO"
    RETRASADO = "RETRASADO"


class EstadoReserva(Enum):
    """Estados posibles de una reserva"""
    CONFIRMADA = "CONFIRMADA"
    CHECK_IN_REALIZADO = "CHECK_IN_REALIZADO"
    ABORDADO = "ABORDADO"
    CANCELADA = "CANCELADA"


class ClaseAsiento(Enum):
    """Clases de asientos disponibles"""
    ECONOMICA = "ECONOMICA"
    EJECUTIVA = "EJECUTIVA"
    PRIMERA_CLASE = "PRIMERA_CLASE"


class TipoDocumento(Enum):
    """Tipos de documentos de identidad"""
    DNI = "DNI"
    PASAPORTE = "PASAPORTE"
    LICENCIA = "LICENCIA"


class Terminal(Enum):
    """Terminales del aeropuerto"""
    NACIONAL = "NACIONAL"
    INTERNACIONAL = "INTERNACIONAL"


class RolTripulacion(Enum):
    """Roles de la tripulación"""
    CAPITAN = "CAPITAN"
    COPILOTO = "COPILOTO"
    TRIPULANTE_CABINA = "TRIPULANTE_CABINA"


class TipoAvion(Enum):
    """Tipos de aviones"""
    COMERCIAL = "COMERCIAL"
    CARGA = "CARGA"
    PRIVADO = "PRIVADO"
