"""
FormValidator - Componente para validação de formulários em tempo real
"""
import re
import tkinter as tk
from typing import Dict, Callable, Optional

class FormValidator:
    """Validador de formulários com feedback visual"""
    
    def __init__(self):
        self.errors = {}
        self.validators = {}
        self.error_labels = {}
    
    def add_validator(self, field_name: str, validator_func: Callable, error_message: str):
        """Adiciona um validador para um campo"""
        if field_name not in self.validators:
            self.validators[field_name] = []
        self.validators[field_name].append({
            'func': validator_func,
            'message': error_message
        })
    
    def validate_field(self, field_name: str, value: str) -> bool:
        """Valida um campo específico"""
        if field_name not in self.validators:
            return True
        
        for validator in self.validators[field_name]:
            if not validator['func'](value):
                self.errors[field_name] = validator['message']
                return False
        
        # Remove erro se validação passou
        if field_name in self.errors:
            del self.errors[field_name]
        return True
    
    def validate_all(self, form_data: Dict[str, str]) -> bool:
        """Valida todos os campos do formulário"""
        self.errors = {}
        all_valid = True
        
        for field_name, value in form_data.items():
            if not self.validate_field(field_name, value):
                all_valid = False
        
        return all_valid
    
    def get_error(self, field_name: str) -> Optional[str]:
        """Retorna mensagem de erro de um campo"""
        return self.errors.get(field_name)
    
    def clear_errors(self):
        """Limpa todos os erros"""
        self.errors = {}
        for label in self.error_labels.values():
            if label and label.winfo_exists():
                label.config(text="", fg="#FFFFFF")
    
    def show_error(self, field_name: str, error_label: tk.Label):
        """Mostra erro em um label"""
        self.error_labels[field_name] = error_label
        error = self.get_error(field_name)
        if error:
            error_label.config(text=error, fg="#DC3545")
        else:
            error_label.config(text="", fg="#FFFFFF")
    
    def highlight_field(self, widget, is_valid: bool):
        """Destaca campo como válido ou inválido"""
        if hasattr(widget, 'configure'):
            if is_valid:
                # Remove destaque de erro
                try:
                    widget.configure(border_color="#3B82F6" if hasattr(widget, 'border_color') else None)
                except:
                    pass
            else:
                # Destaca como erro
                try:
                    widget.configure(border_color="#DC3545" if hasattr(widget, 'border_color') else None)
                except:
                    pass


# Validadores comuns
def validate_required(value: str) -> bool:
    """Valida se campo é obrigatório"""
    return value.strip() != "" if value else False

def validate_email(value: str) -> bool:
    """Valida formato de email"""
    if not value:
        return True  # Email pode ser opcional
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, value))

def validate_phone(value: str) -> bool:
    """Valida formato de telefone"""
    if not value:
        return True  # Telefone pode ser opcional
    # Remove caracteres não numéricos
    digits = re.sub(r'\D', '', value)
    # Aceita telefones com 10 ou 11 dígitos
    return len(digits) >= 10 and len(digits) <= 11

def validate_min_length(min_len: int):
    """Retorna validador de comprimento mínimo"""
    def validator(value: str) -> bool:
        if not value:
            return True
        return len(value.strip()) >= min_len
    return validator

def validate_password_strength(value: str) -> bool:
    """Valida força da senha (mínimo 6 caracteres)"""
    if not value:
        return True
    return len(value) >= 6

def validate_passwords_match(password: str, confirm_password: str) -> bool:
    """Valida se senhas coincidem"""
    if not password or not confirm_password:
        return True
    return password == confirm_password

