"""
Clase Pasajero - Representa un pasajero en el sistema
"""

from datetime import date, datetime
from typing import List, Optional


class Pasajero:
    """
    Representa un pasajero que viaja en el aeropuerto.
    
    Attributes:
        nombre: Nombre completo del pasajero
        numero_documento: Número del documento de identidad
        tipo_documento: Tipo de documento (DNI, PASAPORTE, LICENCIA)
        edad: Edad del pasajero
    """
    
    _contador_id = 1000
    
    def __init__(self, nombre: str, numero_documento: str, tipo_documento: str):
        """
        Inicializa un nuevo pasajero.
        
        Args:
            nombre: Nombre completo
            numero_documento: Número del documento
            tipo_documento: DNI, PASAPORTE o LICENCIA
        
        Raises:
            ValueError: Si los datos son inválidos
        """
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if not numero_documento:
            raise ValueError("El número de documento no puede estar vacío")
        
        self._id = Pasajero._generar_id()
        self._nombre = nombre
        self._numero_documento = numero_documento
        self._tipo_documento = tipo_documento
        
        # Información adicional
        self._fecha_nacimiento = None
        self._fecha_vencimiento_doc = None
        self._email = ""
        self._telefono = ""
        self._nacionalidad = "Argentina"
        
        # Viajero frecuente
        self._millas_acumuladas = 0
        self._historial_vuelos = []
        self._reservas = []
        
        # Permisos
        self._tiene_autorizacion = False  # Para menores
        self._es_menor = False
    
    @classmethod
    def _generar_id(cls) -> int:
        """Genera un ID único para el pasajero"""
        cls._contador_id += 1
        return cls._contador_id
    
    @property
    def id(self) -> int:
        """Obtiene el ID del pasajero"""
        return self._id
    
    @property
    def nombre(self) -> str:
        """Obtiene el nombre del pasajero"""
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor: str):
        """Establece el nombre del pasajero"""
        if not valor:
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor
    
    @property
    def numero_documento(self) -> str:
        """Obtiene el número de documento"""
        return self._numero_documento
    
    @property
    def tipo_documento(self) -> str:
        """Obtiene el tipo de documento"""
        return self._tipo_documento
    
    @property
    def fecha_nacimiento(self) -> Optional[date]:
        """Obtiene la fecha de nacimiento"""
        return self._fecha_nacimiento
    
    @fecha_nacimiento.setter
    def fecha_nacimiento(self, fecha: date):
        """Establece la fecha de nacimiento"""
        self._fecha_nacimiento = fecha
        # Actualizar si es menor
        if fecha:
            self._es_menor = self.get_edad() < 18
    
    @property
    def fecha_vencimiento_doc(self) -> Optional[date]:
        """Obtiene la fecha de vencimiento del documento"""
        return self._fecha_vencimiento_doc
    
    @fecha_vencimiento_doc.setter
    def fecha_vencimiento_doc(self, fecha: date):
        """Establece la fecha de vencimiento del documento"""
        self._fecha_vencimiento_doc = fecha
    
    @property
    def email(self) -> str:
        """Obtiene el email"""
        return self._email
    
    @email.setter
    def email(self, valor: str):
        """Establece el email"""
        self._email = valor
    
    @property
    def telefono(self) -> str:
        """Obtiene el teléfono"""
        return self._telefono
    
    @telefono.setter
    def telefono(self, valor: str):
        """Establece el teléfono"""
        self._telefono = valor
    
    @property
    def millas_acumuladas(self) -> int:
        """Obtiene las millas acumuladas"""
        return self._millas_acumuladas
    
    @property
    def tiene_autorizacion(self) -> bool:
        """Indica si el menor tiene autorización para viajar"""
        return self._tiene_autorizacion
    
    @tiene_autorizacion.setter
    def tiene_autorizacion(self, valor: bool):
        """Establece la autorización"""
        self._tiene_autorizacion = valor
    
    def get_edad(self) -> Optional[int]:
        """
        Calcula la edad del pasajero.
        
        Returns:
            Edad en años o None si no hay fecha de nacimiento
        """
        if not self._fecha_nacimiento:
            return None
        
        hoy = date.today()
        edad = hoy.year - self._fecha_nacimiento.year
        
        # Ajustar si aún no cumplió años este año
        if (hoy.month, hoy.day) < (self._fecha_nacimiento.month, self._fecha_nacimiento.day):
            edad -= 1
        
        return edad
    
    def es_menor(self) -> bool:
        """
        Verifica si es menor de edad.
        
        Returns:
            True si es menor de 18 años
        """
        edad = self.get_edad()
        return edad < 18 if edad is not None else False
    
    def tiene_documento_valido(self) -> bool:
        """
        Verifica si el documento es válido.
        
        Returns:
            True si el documento es válido
        """
        if not self._fecha_vencimiento_doc:
            return True  # Si no tiene fecha, asumir válido
        
        return self._fecha_vencimiento_doc >= date.today()
    
    def validar_documento(self) -> None:
        """
        Valida el documento del pasajero.
        
        Raises:
            DocumentoInvalidoException: Si el documento no es válido
        """
        from excepciones.excepciones_aeropuerto import DocumentoInvalidoException
        
        if not self._numero_documento:
            raise DocumentoInvalidoException(
                "Sin documento",
                "El pasajero no tiene documento registrado"
            )
        
        if self._fecha_vencimiento_doc and self._fecha_vencimiento_doc < date.today():
            raise DocumentoInvalidoException(
                self._numero_documento,
                f"Documento vencido el {self._fecha_vencimiento_doc}"
            )
    
    def puede_viajar_solo(self, tipo_vuelo: str = "NACIONAL") -> bool:
        """
        Verifica si puede viajar solo según su edad.
        
        Args:
            tipo_vuelo: NACIONAL o INTERNACIONAL
        
        Returns:
            True si puede viajar solo
        """
        edad = self.get_edad()
        if edad is None:
            return True  # Si no sabemos la edad, asumir que sí
        
        if tipo_vuelo == "INTERNACIONAL":
            # Menores de 12 no pueden viajar solos en internacionales
            if edad < 12:
                return False
            # Entre 12 y 17 necesitan autorización
            if edad < 18:
                return self._tiene_autorizacion
        else:  # NACIONAL
            # Menores de 5 no pueden viajar solos
            if edad < 5:
                return False
        
        return True
    
    def validar_para_vuelo(self, tipo_vuelo: str = "NACIONAL") -> None:
        """
        Valida si el pasajero puede tomar el vuelo.
        
        Args:
            tipo_vuelo: NACIONAL o INTERNACIONAL
        
        Raises:
            EdadInsuficienteException: Si no cumple requisitos de edad
            DocumentoInvalidoException: Si el documento no es válido
        """
        from excepciones.excepciones_aeropuerto import EdadInsuficienteException, DocumentoInvalidoException
        
        # Validar documento
        self.validar_documento()
        
        # Validar documento tipo para internacional
        if tipo_vuelo == "INTERNACIONAL" and self._tipo_documento != "PASAPORTE":
            raise DocumentoInvalidoException(
                self._numero_documento,
                "Se requiere pasaporte para vuelos internacionales"
            )
        
        # Validar edad
        if not self.puede_viajar_solo(tipo_vuelo):
            edad = self.get_edad()
            raise EdadInsuficienteException(edad, tipo_vuelo)
    
    def agregar_reserva(self, reserva) -> None:
        """Agrega una reserva al historial del pasajero"""
        if reserva not in self._reservas:
            self._reservas.append(reserva)
    
    def get_reservas(self) -> List:
        """Obtiene la lista de reservas"""
        return self._reservas.copy()
    
    def agregar_vuelo_historial(self, vuelo) -> None:
        """Agrega un vuelo al historial"""
        if vuelo not in self._historial_vuelos:
            self._historial_vuelos.append(vuelo)
    
    def get_historial_vuelos(self) -> List:
        """Obtiene el historial de vuelos"""
        return self._historial_vuelos.copy()
    
    def acumular_millas(self, millas: int) -> None:
        """
        Acumula millas del viajero frecuente.
        
        Args:
            millas: Cantidad de millas a acumular
        """
        self._millas_acumuladas += millas
    
    def es_viajero_frecuente(self) -> bool:
        """
        Verifica si es viajero frecuente (>50,000 millas).
        
        Returns:
            True si tiene más de 50,000 millas
        """
        return self._millas_acumuladas >= 50000
    
    def get_nivel_viajero(self) -> str:
        """
        Obtiene el nivel de viajero según millas.
        
        Returns:
            Nivel del viajero
        """
        if self._millas_acumuladas < 10000:
            return "BASICO"
        elif self._millas_acumuladas < 50000:
            return "PLATA"
        elif self._millas_acumuladas < 100000:
            return "ORO"
        else:
            return "PLATINUM"
    
    def __str__(self) -> str:
        """Representación en string del pasajero"""
        return f"{self._nombre} ({self._tipo_documento}: {self._numero_documento})"
    
    def __repr__(self) -> str:
        """Representación para debugging"""
        return f"Pasajero(id={self._id}, nombre='{self._nombre}')"
    
    def __eq__(self, other) -> bool:
        """Compara dos pasajeros por documento"""
        if not isinstance(other, Pasajero):
            return False
        return (self._numero_documento == other._numero_documento and
                self._tipo_documento == other._tipo_documento)
    
    def __hash__(self) -> int:
        """Hash basado en documento"""
        return hash((self._numero_documento, self._tipo_documento))


# Testing
if __name__ == "__main__":
    print("=== Prueba de la clase Pasajero ===\n")
    
    # Crear pasajero adulto
    pasajero = Pasajero("Juan Pérez", "AB123456", "PASAPORTE")
    pasajero.fecha_nacimiento = date(1985, 3, 15)
    pasajero.fecha_vencimiento_doc = date.today().replace(year=date.today().year + 5)
    pasajero.email = "juan@email.com"
    pasajero.telefono = "+54911XXXXXXXX"
    
    print(f"1. Pasajero creado: {pasajero}")
    print(f"   ID: {pasajero.id}")
    print(f"   Edad: {pasajero.get_edad()} años")
    print(f"   Es menor: {pasajero.es_menor()}")
    print(f"   Documento válido: {pasajero.tiene_documento_valido()}")
    
    print("\n2. Validando para vuelo internacional...")
    try:
        pasajero.validar_para_vuelo("INTERNACIONAL")
        print("   ✓ Puede viajar")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n3. Sistema de millas:")
    pasajero.acumular_millas(15000)
    print(f"   Millas acumuladas: {pasajero.millas_acumuladas}")
    print(f"   Nivel: {pasajero.get_nivel_viajero()}")
    print(f"   Viajero frecuente: {pasajero.es_viajero_frecuente()}")
    
    # Crear pasajero menor
    print("\n4. Pasajero menor de edad:")
    menor = Pasajero("Sofía Martínez", "44556677", "PASAPORTE")
    menor.fecha_nacimiento = date.today().replace(year=date.today().year - 10)
    print(f"   {menor}")
    print(f"   Edad: {menor.get_edad()} años")
    print(f"   Puede viajar solo (internacional): {menor.puede_viajar_solo('INTERNACIONAL')}")
    
    print("\n✓ Clase Pasajero funcionando correctamente")
