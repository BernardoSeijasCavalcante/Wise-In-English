# observer_pattern.py
import streamlit as st

class Subject:
    """Classe que mantém a lista de observadores e notifica quando há mudança."""
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, message, success=True):
        for observer in self._observers:
            observer.update(message, success)


class Observer:
    """Interface básica para observadores."""
    def update(self, message, success=True):
        pass


# ==== Observadores Concretos ====

class StreamlitNotifier(Observer):
    """Mostra mensagens diretamente na interface do Streamlit."""
    def update(self, message, success=True):
        if success:
            st.info(f"🔔 **Notificação:** {message}")
        else:
            st.warning(f"⚠️ **Aviso:** {message}")


class LoginLogger(Observer):
    """Simula o registro de log no console."""
    def update(self, message, success=True):
        print(f"[LOG] {message}")
