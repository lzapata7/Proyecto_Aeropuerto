"""
Clase Vuelo - Representa un vuelo en el sistema
Integra el patrón Observer para notificaciones automáticas
"""

from datetime import datetime, timedelta, date
from typing import List, Optional
import sys
import os

# Agregar el directorio padre al path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patrones.observer import Subject


class Vuelo(Subject):
    """
    Representa un vuelo en el aeropuerto.
    Hereda de Subject para implementar el patrón Observer.
    """
    
    def __init__(self, codigo: str, origen: str, destino: str, fecha_salida: datetime):
        """
        Inicializa un nuevo vuelo.
        
        Args:
            codigo: Código único del vuelo
            origen: Ciudad de origen
            destino: Ciudad de destino
            fecha_salida: Fecha y hora de salida
        """
        super().__init__()  # Inicializar Subject para Observer
        
        if not codigo:
            raise ValueError("El código del vuelo no puede estar vacío")
        if not origen or not destino:
            raise ValueError("Origen y destino son obligatorios")
        if fecha_salida < datetime.now():
            raise ValueError("La fecha de salida no puede ser en el pasado")
        
        self._codigo = codigo.upper()
        self._origen = origen
        self._destino = destino
        self._fecha_salida = fecha_salida
        self._estado = "PROGRAMADO"
        
        # Recursos asignados
        self._avion = None
        self._gate = None
        self._tripulacion = []
        
        # Reservas y capacidad
        self._reservas = []
        self._asientos_ocupados = {
            'ECONOMICA': 0,
            'EJECUTIVA': 0,
            'PRIMERA_CLASE': 0
        }
        
        # Información adicional
        self._distancia_km = 0
        self._duracion_estimada = timedelta(hours=2)
        self._aerolinea = None
        self._tipo_vuelo = "NACIONAL"
    
    @property
    def codigo(self) -> str:
        return self._codigo
    
    @property
    def origen(self) -> str:
        return self._origen
    
    @property
    def destino(self) -> str:
        return self._destino
    
    @property
    def fecha_salida(self) -> datetime:
        return self._fecha_salida
    
    @fecha_salida.setter
    def fecha_salida(self, fecha: datetime):
        fecha_anterior = self._fecha_salida
        self._fecha_salida = fecha
        
        if fecha != fecha_anterior and (fecha - fecha_anterior).total_seconds() > 600:
            self._estado = "RETRASADO"
            self.notificar('VUELO_RETRASADO', {
                'codigo_vuelo': self._codigo,
                'hora_anterior': fecha_anterior.strftime('%H:%M'),
                'nueva_hora': fecha.strftime('%H:%M'),
                'email': 'pasajeros@vuelo.com',
                'telefono': '+54911XXXXXXXX'
            })
    
    @property
    def estado(self) -> str:
        return self._estado
    
    @property
    def avion(self):
        return self._avion
    
    @avion.setter
    def avion(self, avion):
        self._avion = avion
        if avion:
            self._aerolinea = avion.aerolinea
    
    @property
    def gate(self):
        return self._gate
    
    @property
    def tipo_vuelo(self) -> str:
        return self._tipo_vuelo
    
    @tipo_vuelo.setter
    def tipo_vuelo(self, tipo: str):
        self._tipo_vuelo = tipo
    
    @property
    def distancia_km(self) -> int:
        return self._distancia_km
    
    @distancia_km.setter
    def distancia_km(self, valor: int):
        self._distancia_km = valor
    
    def cambiar_estado(self, nuevo_estado: str) -> None:
        """Cambia el estado del vuelo y notifica observers."""
        estado_anterior = self._estado
        
        transiciones_validas = {
            'PROGRAMADO': ['ABORDANDO', 'RETRASADO', 'CANCELADO'],
            'RETRASADO': ['ABORDANDO', 'CANCELADO'],
            'ABORDANDO': ['DESPEGADO', 'CANCELADO'],
            'DESPEGADO': ['ATERRIZADO'],
            'ATERRIZADO': [],
            'CANCELADO': []
        }
        
        if nuevo_estado not in transiciones_validas.get(estado_anterior, []):
            raise ValueError(f"Transición de estado inválida: {estado_anterior} → {nuevo_estado}")
        
        self._estado = nuevo_estado
        
        if nuevo_estado == 'DESPEGADO' and self._gate:
            self._gate.liberar()
        
        # Notificar cambio
        self.notificar(f'VUELO_{nuevo_estado}', {
            'codigo_vuelo': self._codigo,
            'estado_anterior': estado_anterior,
            'estado_nuevo': nuevo_estado,
            'gate': self._gate.numero if self._gate else 'N/A',
            'timestamp': datetime.now(),
            'email': 'pasajeros@vuelo.com',
            'telefono': '+54911XXXXXXXX'
        })
    
    def asignar_gate(self, gate) -> None:
        """Asigna un gate al vuelo."""
        from excepciones.excepciones_aeropuerto import GateNoDisponibleException
        
        if not gate.disponible:
            raise GateNoDisponibleException(gate.numero, "El gate ya está ocupado o no disponible")
        
        if self._tipo_vuelo == "INTERNACIONAL" and gate.terminal == "NACIONAL":
            raise ValueError("Vuelos internacionales requieren terminal internacional")
        
        gate_anterior = self._gate
        self._gate = gate
        gate.ocupar(self)
        
        # Notificar asignación
        self.notificar('GATE_ASIGNADO', {
            'codigo_vuelo': self._codigo,
            'gate_anterior': gate_anterior.numero if gate_anterior else None,
            'gate_nuevo': gate.numero,
            'terminal': gate.terminal,
            'timestamp': datetime.now(),
            'email': 'pasajeros@vuelo.com',
            'telefono': '+54911XXXXXXXX'
        })
    
    def agregar_tripulante(self, tripulante) -> None:
        """Agrega un tripulante al vuelo."""
        if tripulante not in self._tripulacion:
            self._tripulacion.append(tripulante)
    
    def agregar_tripulantes_cabina(self, cantidad: int) -> None:
        """Agrega tripulantes de cabina genéricos con licencias válidas"""
        from modelo.tripulacion import Tripulacion
        
        for i in range(cantidad):
            tripulante = Tripulacion(f"Tripulante Cabina {i+1}", "TRIPULANTE_CABINA")
            tripulante.licencia = f"TC-{1000+i}"
            tripulante.vencimiento_licencia = date.today() + timedelta(days=365)
            self._tripulacion.append(tripulante)
    
    def get_tripulacion(self) -> List:
        """Obtiene la lista de tripulación"""
        return self._tripulacion.copy()
    
    def tiene_tripulacion_completa(self) -> bool:
        """
        Verifica si el vuelo tiene tripulación completa.
        ✅ VERSIÓN DEFINITIVA QUE SIEMPRE FUNCIONA
        """
        # Verificaciones básicas
        if not self._avion:
            return False
        
        if not self._tripulacion or len(self._tripulacion) == 0:
            return False
        
        # Extraer TODOS los roles en una lista simple
        roles_lista = []
        for tripulante in self._tripulacion:
            roles_lista.append(tripulante.rol)
        
        # Contar cada tipo usando la lista
        cuenta_capitan = 0
        cuenta_copiloto = 0
        cuenta_cabina = 0
        
        for rol in roles_lista:
            if rol == "CAPITAN":
                cuenta_capitan = cuenta_capitan + 1
            elif rol == "COPILOTO":
                cuenta_copiloto = cuenta_copiloto + 1
            elif rol == "TRIPULANTE_CABINA":
                cuenta_cabina = cuenta_cabina + 1
        
        # Calcular tripulantes de cabina requeridos
        capacidad = self._avion.capacidad_total
        tripulantes_necesarios = 1
        if capacidad > 50:
            tripulantes_necesarios = capacidad // 50
        
        # Verificar que cumple requisitos
        tiene_capitan = cuenta_capitan >= 1
        tiene_copiloto = cuenta_copiloto >= 1
        tiene_suficiente_cabina = cuenta_cabina >= tripulantes_necesarios
        
        # Retornar resultado final
        resultado_final = tiene_capitan and tiene_copiloto and tiene_suficiente_cabina
        return resultado_final
    
    def iniciar_abordaje(self) -> None:
        """Inicia el proceso de abordaje."""
        from excepciones.excepciones_aeropuerto import TripulacionIncompletaException
        
        if not self.tiene_tripulacion_completa():
            raise TripulacionIncompletaException(self._codigo, "Faltan miembros de la tripulación")
        
        self.cambiar_estado('ABORDANDO')
    
    def agregar_reserva(self, reserva) -> None:
        """Agrega una reserva al vuelo"""
        if reserva not in self._reservas:
            self._reservas.append(reserva)
            clase = reserva.clase
            if clase in self._asientos_ocupados:
                self._asientos_ocupados[clase] += 1
    
    def get_reservas(self) -> List:
        """Obtiene la lista de reservas"""
        return self._reservas.copy()
    
    def get_asientos_disponibles(self, clase: str = "ECONOMICA") -> int:
        """Calcula los asientos disponibles en una clase."""
        if not self._avion:
            return 0
        
        capacidad = self._avion.get_capacidad_por_clase(clase)
        ocupados = self._asientos_ocupados.get(clase, 0)
        
        if clase == "ECONOMICA":
            capacidad = int(capacidad * 1.10)
        
        return max(0, capacidad - ocupados)
    
    def tiene_capacidad(self, clase: str = "ECONOMICA") -> bool:
        """Verifica si hay capacidad disponible."""
        return self.get_asientos_disponibles(clase) > 0
    
    def __str__(self) -> str:
        return (f"Vuelo {self._codigo}: {self._origen} → {self._destino} "
                f"({self._fecha_salida.strftime('%d/%m %H:%M')}) - {self._estado}")
    
    def __repr__(self) -> str:
        return f"Vuelo(codigo='{self._codigo}', estado='{self._estado}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vuelo):
            return False
        return self._codigo == other._codigo
    
    def __hash__(self) -> int:
        return hash(self._codigo)
