"""
Gestor de Pasajeros - Maneja operaciones relacionadas con pasajeros
"""

from typing import List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelo.pasajero import Pasajero
from excepciones.excepciones_aeropuerto import PasajeroNoEncontradoException


class GestorPasajeros:
    """
    Gestor para operaciones de pasajeros.
    Centraliza la lógica de gestión de pasajeros.
    """
    
    def __init__(self):
        """Inicializa el gestor de pasajeros"""
        self._pasajeros: List[Pasajero] = []
    
    def registrar_pasajero(self, nombre: str, numero_documento: str, 
                          tipo_documento: str) -> Pasajero:
        """
        Registra un nuevo pasajero.
        
        Args:
            nombre: Nombre completo
            numero_documento: Número del documento
            tipo_documento: Tipo de documento
        
        Returns:
            Pasajero registrado
        """
        # ✅ CORRECCIÓN: Verificar si ya existe primero
        try:
            existente = self.buscar_por_documento(numero_documento, tipo_documento)
            print(f"   ℹ️ Pasajero ya existe: {existente.nombre}")
            return existente  # Ya existe, retornar el existente
        except PasajeroNoEncontradoException:
            pass  # No existe, crear nuevo
        
        # Crear nuevo pasajero
        pasajero = Pasajero(nombre, numero_documento, tipo_documento)
        self._pasajeros.append(pasajero)
        
        # ✅ CORRECCIÓN: Confirmar registro
        print(f"   ✓ Pasajero registrado: {pasajero.nombre} (Total: {len(self._pasajeros)})")
        
        return pasajero
    
    def buscar_por_documento(self, numero_documento: str, 
                            tipo_documento: str) -> Pasajero:
        """
        Busca un pasajero por número de documento.
        
        Args:
            numero_documento: Número del documento
            tipo_documento: Tipo de documento
        
        Returns:
            Pasajero encontrado
        
        Raises:
            PasajeroNoEncontradoException: Si no existe
        """
        for pasajero in self._pasajeros:
            if (pasajero.numero_documento == numero_documento and 
                pasajero.tipo_documento == tipo_documento):
                return pasajero
        
        raise PasajeroNoEncontradoException(numero_documento)
    
    def buscar_por_id(self, id_pasajero: int) -> Pasajero:
        """
        Busca un pasajero por ID.
        
        Args:
            id_pasajero: ID del pasajero
        
        Returns:
            Pasajero encontrado
        
        Raises:
            PasajeroNoEncontradoException: Si no existe
        """
        for pasajero in self._pasajeros:
            if pasajero.id == id_pasajero:
                return pasajero
        
        raise PasajeroNoEncontradoException(str(id_pasajero))
    
    def buscar_por_nombre(self, nombre: str) -> List[Pasajero]:
        """
        Busca pasajeros por nombre (búsqueda parcial).
        
        Args:
            nombre: Nombre o parte del nombre
        
        Returns:
            Lista de pasajeros que coinciden
        """
        nombre_lower = nombre.lower()
        return [p for p in self._pasajeros 
                if nombre_lower in p.nombre.lower()]
    
    def listar_pasajeros(self) -> List[Pasajero]:
        """
        Lista todos los pasajeros.
        
        Returns:
            Lista de pasajeros
        """
        return self._pasajeros.copy()
    
    def listar_viajeros_frecuentes(self) -> List[Pasajero]:
        """
        Lista pasajeros viajeros frecuentes (>50,000 millas).
        
        Returns:
            Lista de viajeros frecuentes
        """
        return [p for p in self._pasajeros if p.es_viajero_frecuente()]
    
    def get_total_pasajeros(self) -> int:
        """Obtiene el total de pasajeros registrados"""
        total = len(self._pasajeros)
        return total
    
    def get_estadisticas(self) -> dict:
        """
        Obtiene estadísticas de pasajeros.
        
        Returns:
            Diccionario con estadísticas
        """
        viajeros_frecuentes = len(self.listar_viajeros_frecuentes())
        
        tipos_documento = {}
        for pasajero in self._pasajeros:
            tipo = pasajero.tipo_documento
            tipos_documento[tipo] = tipos_documento.get(tipo, 0) + 1
        
        total_millas = sum(p.millas_acumuladas for p in self._pasajeros)
        
        return {
            'total_pasajeros': len(self._pasajeros),
            'viajeros_frecuentes': viajeros_frecuentes,
            'por_tipo_documento': tipos_documento,
            'millas_totales': total_millas,
            'promedio_millas': total_millas / len(self._pasajeros) if self._pasajeros else 0
        }
    
    def actualizar_millas(self, numero_documento: str, tipo_documento: str, 
                         millas: int) -> None:
        """
        Actualiza las millas de un pasajero.
        
        Args:
            numero_documento: Número del documento
            tipo_documento: Tipo de documento
            millas: Millas a acumular
        """
        pasajero = self.buscar_por_documento(numero_documento, tipo_documento)
        pasajero.acumular_millas(millas)
    
    def eliminar_pasajero(self, numero_documento: str, tipo_documento: str) -> None:
        """
        Elimina un pasajero del sistema (solo si no tiene reservas activas).
        
        Args:
            numero_documento: Número del documento
            tipo_documento: Tipo de documento
        """
        pasajero = self.buscar_por_documento(numero_documento, tipo_documento)
        
        # Verificar que no tenga reservas activas
        reservas_activas = [r for r in pasajero.get_reservas() 
                           if r.estado not in ['CANCELADA', 'ABORDADO']]
        
        if reservas_activas:
            raise ValueError(
                f"No se puede eliminar pasajero con {len(reservas_activas)} reservas activas"
            )
        
        self._pasajeros.remove(pasajero)


# Testing
if __name__ == "__main__":
    from datetime import date, timedelta
    
    print("=== Prueba del GestorPasajeros ===\n")
    
    gestor = GestorPasajeros()
    
    # Registrar pasajeros
    print("1. Registrando pasajeros...")
    p1 = gestor.registrar_pasajero("Juan Pérez", "AB123456", "PASAPORTE")
    p1.fecha_nacimiento = date(1985, 3, 15)
    print(f"   ✓ {p1}")
    
    p2 = gestor.registrar_pasajero("María López", "12345678", "DNI")
    p2.acumular_millas(55000)
    print(f"   ✓ {p2}")
    
    # Buscar pasajero
    print("\n2. Buscando pasajero...")
    encontrado = gestor.buscar_por_documento("AB123456", "PASAPORTE")
    print(f"   ✓ Encontrado: {encontrado.nombre}")
    
    # Listar viajeros frecuentes
    print("\n3. Viajeros frecuentes:")
    frecuentes = gestor.listar_viajeros_frecuentes()
    for p in frecuentes:
        print(f"   ✓ {p.nombre} - {p.millas_acumuladas} millas")
    
    # Estadísticas
    print("\n4. Estadísticas:")
    stats = gestor.get_estadisticas()
    print(f"   Total: {stats['total_pasajeros']}")
    print(f"   Viajeros frecuentes: {stats['viajeros_frecuentes']}")
    print(f"   Promedio millas: {stats['promedio_millas']:.0f}")
    
    print("\n✓ GestorPasajeros funcionando correctamente")
