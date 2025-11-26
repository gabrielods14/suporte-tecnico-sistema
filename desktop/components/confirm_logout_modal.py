"""
ConfirmLogoutModal - Modal de confirmação de logout
Replica ConfirmLogoutModal.jsx do web
"""
from components.confirm_modal import ConfirmModal

class ConfirmLogoutModal:
    """Modal de confirmação de logout"""
    
    def __init__(self, parent, is_open, on_confirm, on_cancel):
        self.modal = None
        if is_open:
            self.modal = ConfirmModal(
                parent,
                title="Confirmar Logout",
                message="Tem certeza que deseja sair?",
                on_confirm=on_confirm,
                on_cancel=on_cancel,
                confirm_text="Sim",
                cancel_text="Cancelar"
            )
    
    def close(self):
        """Fecha o modal"""
        if self.modal:
            self.modal.close()



