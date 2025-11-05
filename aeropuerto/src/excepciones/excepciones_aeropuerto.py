"""
Excepciones Personalizadas del Sistema de Gestión de Aeropuerto
Contiene las 11 excepciones específicas del dominio
"""


class AeropuertoException(Exception):
    """Excepción base para todas las excepciones del aeropuerto"""
    def __init__(self, mensaje: str, causa: Exception = None):
        self.mensaje = mensaje
        self.causa = causa
        super().__init__(self.mensaje)


class VueloLlenoException(AeropuertoException):
    """
    Se lanza cuando se intenta reservar en un vuelo que no tiene capacidad disponible
    """
    def __init__(self, codigo_vuelo: str, clase: str):
        mensaje = f"El vuelo {codigo_vuelo} está lleno. No hay asientos disponibles en clase {clase}."
        super().__init__(mensaje)


class VueloNoEncontradoException(AeropuertoException):
    """
    Se lanza cuando se busca un vuelo que no existe en el sistema
    """
    def __init__(self, codigo_vuelo: str):
        mensaje = f"El vuelo con código {codigo_vuelo} no fue encontrado en el sistema."
        super().__init__(mensaje)


class PasajeroNoEncontradoException(AeropuertoException):
    """
    Se lanza cuando se busca un pasajero que no está registrado
    """
    def __init__(self, numero_documento: str):
        mensaje = f"El pasajero con documento {numero_documento} no fue encontrado en el sistema."
        super().__init__(mensaje)


class ReservaNoEncontradaException(AeropuertoException):
    """
    Se lanza cuando se busca una reserva con código inválido
    """
    def __init__(self, codigo_reserva: str):
        mensaje = f"La reserva con código {codigo_reserva} no fue encontrada en el sistema."
        super().__init__(mensaje)


class DocumentoInvalidoException(AeropuertoException):
    """
    Se lanza cuando un documento está vencido o es de tipo incorrecto
    """
    def __init__(self, numero_documento: str, razon: str):
        mensaje = f"El documento {numero_documento} es inválido. Razón: {razon}"
        super().__init__(mensaje)


class CheckInNoDisponibleException(AeropuertoException):
    """
    Se lanza cuando se intenta hacer check-in fuera de la ventana permitida
    (24 horas a 45 minutos antes del vuelo)
    """
    def __init__(self, razon: str):
        mensaje = f"El check-in no está disponible. {razon}"
        super().__init__(mensaje)


class GateNoDisponibleException(AeropuertoException):
    """
    Se lanza cuando se intenta asignar un gate que está ocupado o no disponible
    """
    def __init__(self, numero_gate: str, razon: str = "Gate ocupado"):
        mensaje = f"El gate {numero_gate} no está disponible. {razon}"
        super().__init__(mensaje)


class EquipajeExcedidoException(AeropuertoException):
    """
    Se lanza cuando el equipaje excede los límites de peso o cantidad por clase
    """
    def __init__(self, clase: str, razon: str):
        mensaje = f"Equipaje excedido para clase {clase}. {razon}"
        super().__init__(mensaje)


class VueloYaDespegadoException(AeropuertoException):
    """
    Se lanza cuando se intenta realizar una operación en un vuelo que ya despegó
    """
    def __init__(self, codigo_vuelo: str):
        mensaje = f"El vuelo {codigo_vuelo} ya ha despegado. No se pueden realizar más operaciones."
        super().__init__(mensaje)


class EdadInsuficienteException(AeropuertoException):
    """
    Se lanza cuando un menor no cumple los requisitos de edad para viajar
    """
    def __init__(self, edad: int, tipo_vuelo: str):
        if tipo_vuelo == "INTERNACIONAL":
            mensaje = f"Los menores de 12 años no pueden viajar solos en vuelos internacionales. Edad: {edad}"
        else:
            mensaje = f"Los menores de 5 años no pueden viajar solos. Edad: {edad}"
        super().__init__(mensaje)


class TripulacionIncompletaException(AeropuertoException):
    """
    Se lanza cuando un vuelo no tiene la tripulación completa requerida
    """
    def __init__(self, codigo_vuelo: str, razon: str):
        mensaje = f"El vuelo {codigo_vuelo} no tiene tripulación completa. {razon}"
        super().__init__(mensaje)
