"""
ConfirmSaveModal - Modal de confirmação de salvamento
Replica ConfirmSaveModal.jsx do web
"""
from components.confirm_modal import ConfirmModal

class ConfirmSaveModal:
    """Modal de confirmação de salvamento"""
    
    def __init__(self, parent, is_open, title, message, on_confirm, on_cancel):
        self.modal = None
        if is_open:
            self.modal = ConfirmModal(
                parent,
                title=title,
                message=message,
                on_confirm=on_confirm,
                on_cancel=on_cancel,
                confirm_text="Confirmar",
                cancel_text="Cancelar"
            )
    
    def close(self):
        """Fecha o modal"""
        if self.modal:
            self.modal.close()






