"""
Patrón Observer - Sistema de Gestión de Aeropuerto

El patrón Observer define una dependencia uno-a-muchos entre objetos,
de forma que cuando un objeto cambia de estado, todos sus dependientes
son notificados y actualizados automáticamente.

USO EN EL PROYECTO:
- Notificaciones de cambios de estado de vuelos
- Alertas de cambios en gates
- Notificaciones a pasajeros sobre su reserva
- Sistema de notificaciones por email, SMS, app
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime


# ============= INTERFACES DEL PATRÓN OBSERVER =============

class Observer(ABC):
    """
    Interfaz Observer - Define el método de actualización que será
    llamado cuando el Subject cambie.
    """
    
    @abstractmethod
    def actualizar(self, evento: str, datos: Dict[str, Any]):
        """
        Método llamado cuando el Subject notifica un cambio.
        
        Args:
            evento: Tipo de evento que ocurrió
            datos: Información relevante del evento
        """
        pass


class Subject(ABC):
    """
    Interfaz Subject - Mantiene una lista de observers y los notifica
    cuando hay cambios.
    """
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def agregar_observer(self, observer: Observer):
        """Agrega un observer a la lista"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remover_observer(self, observer: Observer):
        """Remueve un observer de la lista"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notificar(self, evento: str, datos: Dict[str, Any]):
        """Notifica a todos los observers sobre un cambio"""
        for observer in self._observers:
            observer.actualizar(evento, datos)


# ============= OBSERVERS CONCRETOS =============

class NotificadorEmail(Observer):
    """
    Observer que envía notificaciones por email.
    """
    
    def __init__(self, nombre: str = "Email"):
        self.nombre = nombre
        self.notificaciones_enviadas = []
    
    def actualizar(self, evento: str, datos: Dict[str, Any]):
        """Procesa el evento y envía email"""
        email_destino = datos.get('email', 'usuario@ejemplo.com')
        mensaje = self._construir_mensaje(evento, datos)
        
        # Simulación de envío de email
        self._enviar_email(email_destino, evento, mensaje)
        
        self.notificaciones_enviadas.append({
            'tipo': 'EMAIL',
            'evento': evento,
            'timestamp': datetime.now(),
            'datos': datos
        })
    
    def _construir_mensaje(self, evento: str, datos: Dict[str, Any]) -> str:
        """Construye el mensaje según el tipo de evento"""
        mensajes = {
            'VUELO_RETRASADO': f"Su vuelo {datos.get('codigo_vuelo')} ha sido retrasado. "
                              f"Nueva hora: {datos.get('nueva_hora')}",
            'VUELO_CANCELADO': f"Lamentamos informar que el vuelo {datos.get('codigo_vuelo')} "
                              f"ha sido cancelado.",
            'GATE_CAMBIADO': f"El gate de su vuelo {datos.get('codigo_vuelo')} ha cambiado "
                            f"de {datos.get('gate_anterior')} a {datos.get('gate_nuevo')}",
            'CHECK_IN_DISPONIBLE': f"Ya puede realizar el check-in online para su vuelo "
                                  f"{datos.get('codigo_vuelo')}",
            'ABORDAJE_INICIADO': f"Ha iniciado el abordaje del vuelo {datos.get('codigo_vuelo')}. "
                                f"Diríjase al gate {datos.get('gate')}"
        }
        return mensajes.get(evento, f"Notificación sobre {evento}")
    
    def _enviar_email(self, destino: str, asunto: str, mensaje: str):
        """Simula el envío de email"""
        print(f"   📧 [EMAIL] To: {destino}")
        print(f"      Subject: {asunto}")
        print(f"      Message: {mensaje}")


class NotificadorSMS(Observer):
    """
    Observer que envía notificaciones por SMS.
    """
    
    def __init__(self, nombre: str = "SMS"):
        self.nombre = nombre
        self.notificaciones_enviadas = []
    
    def actualizar(self, evento: str, datos: Dict[str, Any]):
        """Procesa el evento y envía SMS"""
        telefono = datos.get('telefono', '+54911XXXXXXXX')
        mensaje = self._construir_mensaje_corto(evento, datos)
        
        # Simulación de envío de SMS
        self._enviar_sms(telefono, mensaje)
        
        self.notificaciones_enviadas.append({
            'tipo': 'SMS',
            'evento': evento,
            'timestamp': datetime.now(),
            'datos': datos
        })
    
    def _construir_mensaje_corto(self, evento: str, datos: Dict[str, Any]) -> str:
        """Construye mensaje corto para SMS (máximo 160 caracteres)"""
        mensajes = {
            'VUELO_RETRASADO': f"Vuelo {datos.get('codigo_vuelo')} retrasado. "
                              f"Nueva hora: {datos.get('nueva_hora')}",
            'VUELO_CANCELADO': f"Vuelo {datos.get('codigo_vuelo')} CANCELADO. "
                              f"Contacte aerolínea.",
            'GATE_CAMBIADO': f"Cambio de gate: {datos.get('gate_nuevo')}. "
                            f"Vuelo {datos.get('codigo_vuelo')}",
            'CHECK_IN_DISPONIBLE': f"Check-in disponible para {datos.get('codigo_vuelo')}",
            'ABORDAJE_INICIADO': f"Abordaje iniciado. Gate {datos.get('gate')}. "
                                f"{datos.get('codigo_vuelo')}"
        }
        return mensajes.get(evento, f"{evento}: {datos.get('codigo_vuelo')}")
    
    def _enviar_sms(self, telefono: str, mensaje: str):
        """Simula el envío de SMS"""
        print(f"   📱 [SMS] To: {telefono}")
        print(f"      Message: {mensaje}")


class NotificadorApp(Observer):
    """
    Observer que envía notificaciones push a la app móvil.
    """
    
    def __init__(self, nombre: str = "App"):
        self.nombre = nombre
        self.notificaciones_enviadas = []
    
    def actualizar(self, evento: str, datos: Dict[str, Any]):
        """Procesa el evento y envía notificación push"""
        usuario_id = datos.get('pasajero_id', 'unknown')
        
        # Simulación de envío de notificación push
        self._enviar_push(usuario_id, evento, datos)
        
        self.notificaciones_enviadas.append({
            'tipo': 'APP_PUSH',
            'evento': evento,
            'timestamp': datetime.now(),
            'datos': datos
        })
    
    def _enviar_push(self, usuario_id: str, evento: str, datos: Dict[str, Any]):
        """Simula el envío de notificación push"""
        print(f"   📲 [APP PUSH] User: {usuario_id}")
        print(f"      Notification: {evento}")
        print(f"      Data: {datos.get('codigo_vuelo', 'N/A')}")


class RegistroEventos(Observer):
    """
    Observer que registra todos los eventos en un log.
    """
    
    def __init__(self, nombre: str = "Log"):
        self.nombre = nombre
        self.eventos_registrados = []
    
    def actualizar(self, evento: str, datos: Dict[str, Any]):
        """Registra el evento en el log"""
        registro = {
            'timestamp': datetime.now(),
            'evento': evento,
            'datos': datos
        }
        self.eventos_registrados.append(registro)
        
        print(f"   📝 [LOG] {datetime.now().strftime('%H:%M:%S')} - {evento} - "
              f"Vuelo: {datos.get('codigo_vuelo', 'N/A')}")
    
    def obtener_historial(self) -> List[Dict]:
        """Retorna el historial de eventos registrados"""
        return self.eventos_registrados


# ============= SUBJECT CONCRETO =============

class VueloObservable(Subject):
    """
    Subject concreto que representa un vuelo que puede ser observado.
    Notifica a los observers cuando cambia su estado.
    """
    
    def __init__(self, codigo_vuelo: str):
        super().__init__()
        self.codigo_vuelo = codigo_vuelo
        self._estado = "PROGRAMADO"
        self._gate = None
        self._hora_salida = None
    
    def cambiar_estado(self, nuevo_estado: str):
        """Cambia el estado del vuelo y notifica a observers"""
        estado_anterior = self._estado
        self._estado = nuevo_estado
        
        evento = f"VUELO_{nuevo_estado}"
        datos = {
            'codigo_vuelo': self.codigo_vuelo,
            'estado_anterior': estado_anterior,
            'estado_nuevo': nuevo_estado,
            'timestamp': datetime.now()
        }
        
        self.notificar(evento, datos)
    
    def cambiar_gate(self, nuevo_gate: str):
        """Cambia el gate del vuelo y notifica"""
        gate_anterior = self._gate
        self._gate = nuevo_gate
        
        datos = {
            'codigo_vuelo': self.codigo_vuelo,
            'gate_anterior': gate_anterior,
            'gate_nuevo': nuevo_gate,
            'timestamp': datetime.now()
        }
        
        self.notificar('GATE_CAMBIADO', datos)
    
    def retrasar_vuelo(self, nueva_hora: str):
        """Retrasa el vuelo y notifica"""
        hora_anterior = self._hora_salida
        self._hora_salida = nueva_hora
        
        datos = {
            'codigo_vuelo': self.codigo_vuelo,
            'hora_anterior': hora_anterior,
            'nueva_hora': nueva_hora,
            'email': 'pasajero@email.com',
            'telefono': '+54911XXXXXXXX',
            'timestamp': datetime.now()
        }
        
        self.notificar('VUELO_RETRASADO', datos)
    
    def cancelar_vuelo(self, razon: str = "Problemas técnicos"):
        """Cancela el vuelo y notifica"""
        self._estado = "CANCELADO"
        
        datos = {
            'codigo_vuelo': self.codigo_vuelo,
            'razon': razon,
            'email': 'pasajero@email.com',
            'telefono': '+54911XXXXXXXX',
            'timestamp': datetime.now()
        }
        
        self.notificar('VUELO_CANCELADO', datos)
    
    def iniciar_abordaje(self):
        """Inicia el abordaje y notifica"""
        self._estado = "ABORDANDO"
        
        datos = {
            'codigo_vuelo': self.codigo_vuelo,
            'gate': self._gate or 'A15',
            'timestamp': datetime.now()
        }
        
        self.notificar('ABORDAJE_INICIADO', datos)


# ============= TESTING =============

if __name__ == "__main__":
    print("=== Prueba del Patrón Observer ===\n")
    
    # Crear el vuelo observable
    vuelo = VueloObservable("AA1001")
    
    # Crear observers
    notificador_email = NotificadorEmail()
    notificador_sms = NotificadorSMS()
    notificador_app = NotificadorApp()
    registro_log = RegistroEventos()
    
    # Suscribir observers al vuelo
    vuelo.agregar_observer(notificador_email)
    vuelo.agregar_observer(notificador_sms)
    vuelo.agregar_observer(notificador_app)
    vuelo.agregar_observer(registro_log)
    
    print("Observers suscritos al vuelo AA1001\n")
    
    # Simular eventos
    print("1. Cambio de Gate:")
    vuelo.cambiar_gate("B20")
    
    print("\n2. Retraso del Vuelo:")
    vuelo.retrasar_vuelo("15:30")
    
    print("\n3. Inicio de Abordaje:")
    vuelo.iniciar_abordaje()
    
    print("\n4. Desuscribir notificador SMS:")
    vuelo.remover_observer(notificador_sms)
    print("   SMS desuscrito")
    
    print("\n5. Cambio de Estado (solo Email, App y Log recibirán):")
    vuelo.cambiar_estado("DESPEGADO")
    
    # Mostrar estadísticas
    print(f"\n=== Estadísticas ===")
    print(f"Emails enviados: {len(notificador_email.notificaciones_enviadas)}")
    print(f"SMS enviados: {len(notificador_sms.notificaciones_enviadas)}")
    print(f"Notificaciones App: {len(notificador_app.notificaciones_enviadas)}")
    print(f"Eventos registrados: {len(registro_log.eventos_registrados)}")
    
    print("\n✓ Observer funcionando correctamente")
