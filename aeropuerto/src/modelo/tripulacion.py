"""
Clase Tripulacion - Representa un miembro de la tripulación
"""

from datetime import date, datetime, timedelta
from typing import List, Optional


class Tripulacion:
    """
    Representa un miembro de la tripulación de un vuelo.
    
    Attributes:
        nombre: Nombre completo del tripulante
        rol: Rol en la tripulación (CAPITAN, COPILOTO, TRIPULANTE_CABINA)
        licencia: Número de licencia
        horas_vuelo_totales: Horas de vuelo acumuladas
    """
    
    # Límites de horas de vuelo
    MAX_HORAS_DIA = 9
    DESCANSO_MINIMO_HORAS = 12
    
    def __init__(self, nombre: str, rol: str):
        """
        Inicializa un miembro de la tripulación.
        
        Args:
            nombre: Nombre completo
            rol: CAPITAN, COPILOTO o TRIPULANTE_CABINA
        
        Raises:
            ValueError: Si el nombre está vacío
        """
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        
        self._nombre = nombre
        self._rol = rol
        self._licencia = ""
        self._vencimiento_licencia = None
        self._horas_vuelo_totales = 0.0
        self._horas_vuelo_hoy = 0.0
        self._ultimo_vuelo_fecha = None
        self._disponible = True
        self._vuelos_asignados = []
    
    @property
    def nombre(self) -> str:
        """Obtiene el nombre del tripulante"""
        return self._nombre
    
    @property
    def rol(self) -> str:
        """Obtiene el rol del tripulante"""
        return self._rol
    
    @property
    def licencia(self) -> str:
        """Obtiene el número de licencia"""
        return self._licencia
    
    @licencia.setter
    def licencia(self, valor: str):
        """Establece el número de licencia"""
        self._licencia = valor
    
    @property
    def vencimiento_licencia(self) -> Optional[date]:
        """Obtiene la fecha de vencimiento de la licencia"""
        return self._vencimiento_licencia
    
    @vencimiento_licencia.setter
    def vencimiento_licencia(self, fecha: date):
        """Establece la fecha de vencimiento de la licencia"""
        self._vencimiento_licencia = fecha
    
    @property
    def horas_vuelo_totales(self) -> float:
        """Obtiene las horas totales de vuelo"""
        return self._horas_vuelo_totales
    
    @property
    def horas_vuelo_hoy(self) -> float:
        """Obtiene las horas de vuelo de hoy"""
        return self._horas_vuelo_hoy
    
    @property
    def disponible(self) -> bool:
        """Indica si el tripulante está disponible"""
        return self._disponible and self.tiene_licencia_valida()
    
    def tiene_licencia_valida(self) -> bool:
        """
        Verifica si la licencia está vigente.
        
        Returns:
            True si la licencia es válida
        """
        if not self._licencia or not self._vencimiento_licencia:
            return False
        
        return self._vencimiento_licencia >= date.today()
    
    def validar_licencia(self) -> None:
        """
        Valida la licencia del tripulante.
        
        Raises:
            DocumentoInvalidoException: Si la licencia no es válida
        """
        from excepciones.excepciones_aeropuerto import DocumentoInvalidoException
        
        if not self._licencia:
            raise DocumentoInvalidoException(
                "Sin licencia",
                "El tripulante no tiene licencia registrada"
            )
        
        if not self._vencimiento_licencia:
            raise DocumentoInvalidoException(
                self._licencia,
                "No se ha registrado fecha de vencimiento de licencia"
            )
        
        if self._vencimiento_licencia < date.today():
            raise DocumentoInvalidoException(
                self._licencia,
                f"Licencia vencida el {self._vencimiento_licencia}"
            )
    
    def puede_volar_mas(self) -> bool:
        """
        Verifica si puede volar más horas hoy.
        
        Returns:
            True si puede volar más
        """
        return self._horas_vuelo_hoy < self.MAX_HORAS_DIA
    
    def horas_disponibles_hoy(self) -> float:
        """
        Calcula cuántas horas más puede volar hoy.
        
        Returns:
            Horas disponibles
        """
        return max(0, self.MAX_HORAS_DIA - self._horas_vuelo_hoy)
    
    def necesita_descanso(self) -> bool:
        """
        Verifica si necesita descanso según último vuelo.
        
        Returns:
            True si necesita descanso
        """
        if not self._ultimo_vuelo_fecha:
            return False
        
        tiempo_desde_ultimo = datetime.now() - self._ultimo_vuelo_fecha
        return tiempo_desde_ultimo < timedelta(hours=self.DESCANSO_MINIMO_HORAS)
    
    def tiempo_hasta_disponible(self) -> Optional[timedelta]:
        """
        Calcula cuánto tiempo falta para que esté disponible.
        
        Returns:
            Timedelta o None si ya está disponible
        """
        if not self.necesita_descanso():
            return None
        
        tiempo_requerido = self._ultimo_vuelo_fecha + timedelta(hours=self.DESCANSO_MINIMO_HORAS)
        return tiempo_requerido - datetime.now()
    
    def registrar_vuelo(self, duracion_horas: float, vuelo=None) -> None:
        """
        Registra un vuelo realizado.
        
        Args:
            duracion_horas: Duración del vuelo en horas
            vuelo: Instancia del vuelo (opcional)
        """
        self._horas_vuelo_totales += duracion_horas
        self._horas_vuelo_hoy += duracion_horas
        self._ultimo_vuelo_fecha = datetime.now()
        
        if vuelo:
            self._vuelos_asignados.append(vuelo)
    
    def resetear_horas_dia(self) -> None:
        """Resetea el contador de horas del día (llamar a medianoche)"""
        self._horas_vuelo_hoy = 0.0
    
    def marcar_no_disponible(self, razon: str = "No disponible") -> None:
        """Marca el tripulante como no disponible"""
        self._disponible = False
    
    def marcar_disponible(self) -> None:
        """Marca el tripulante como disponible"""
        self._disponible = True
    
    def get_vuelos_asignados(self) -> List:
        """Obtiene la lista de vuelos asignados"""
        return self._vuelos_asignados.copy()
    
    def get_nivel_experiencia(self) -> str:
        """
        Determina el nivel de experiencia según horas de vuelo.
        
        Returns:
            Nivel de experiencia
        """
        if self._horas_vuelo_totales < 500:
            return "JUNIOR"
        elif self._horas_vuelo_totales < 2000:
            return "INTERMEDIO"
        elif self._horas_vuelo_totales < 5000:
            return "SENIOR"
        else:
            return "EXPERTO"
    
    def __str__(self) -> str:
        """Representación en string del tripulante"""
        return f"{self._rol}: {self._nombre} ({self._horas_vuelo_totales:.0f}h)"
    
    def __repr__(self) -> str:
        """Representación para debugging"""
        return f"Tripulacion(nombre='{self._nombre}', rol='{self._rol}')"
    
    def __eq__(self, other) -> bool:
        """Compara dos tripulantes"""
        if not isinstance(other, Tripulacion):
            return False
        return self._nombre == other._nombre and self._licencia == other._licencia
    
    def __hash__(self) -> int:
        """Hash basado en nombre y licencia"""
        return hash((self._nombre, self._licencia))


# Testing
if __name__ == "__main__":
    print("=== Prueba de la clase Tripulacion ===\n")
    
    # Crear tripulantes
    capitan = Tripulacion("Pedro Martínez", "CAPITAN")
    capitan.licencia = "ATP-12345"
    capitan.vencimiento_licencia = date.today() + timedelta(days=730)
    capitan._horas_vuelo_totales = 3500
    
    copiloto = Tripulacion("Laura Sánchez", "COPILOTO")
    copiloto.licencia = "CPL-67890"
    copiloto.vencimiento_licencia = date.today() + timedelta(days=365)
    
    print(f"1. Capitán creado: {capitan}")
    print(f"   Licencia válida: {capitan.tiene_licencia_valida()}")
    print(f"   Nivel experiencia: {capitan.get_nivel_experiencia()}")
    print(f"   Disponible: {capitan.disponible}")
    
    print(f"\n2. Copiloto creado: {copiloto}")
    print(f"   Rol: {copiloto.rol}")
    
    print("\n3. Registrando vuelo...")
    capitan.registrar_vuelo(5.5)
    print(f"   Horas voladas hoy: {capitan.horas_vuelo_hoy}")
    print(f"   Horas disponibles hoy: {capitan.horas_disponibles_hoy()}")
    print(f"   Puede volar más: {capitan.puede_volar_mas()}")
    
    print("\n4. Verificando descanso...")
    print(f"   Necesita descanso: {capitan.necesita_descanso()}")
    if capitan.necesita_descanso():
        tiempo = capitan.tiempo_hasta_disponible()
        print(f"   Tiempo hasta disponible: {tiempo}")
    
    print("\n5. Validando licencia...")
    try:
        capitan.validar_licencia()
        print(f"   ✓ Licencia válida")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n✓ Clase Tripulacion funcionando correctamente")
