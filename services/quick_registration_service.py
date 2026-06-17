"""
QuickRegistrationService - Funcionalidade 2: Registro Rápido

Concito: Registro rápido do usuário com conta do Google
Propósito: Reduzir atrito no processo de registro
"""
from domain.user import User
from services.base import BaseService


class QuickRegistrationService(BaseService):
    """Serviço de registro rápido com login social"""

    def __init__(self):
        super().__init__("QuickRegistrationService")
        self._usuarios = {}

    def login_com_google(self, email: str) -> User:
        """
        Login rápido com conta do Google
        
        Args:
            email: Email do usuário do Google
            
        Returns:
            Objeto do usuário
        """
        self.validar_string(email, "Email")

        usuario_id = f"google_{email.split('@')[0]}"
        if usuario_id in self._usuarios:
            return self._usuarios[usuario_id]

        usuario = User(
            usuario_id,
            email.split("@")[0].title(),
            email,
            None,
            "CADASTRO_PARCIAL"
        )

        self._usuarios[usuario_id] = usuario
        self.log(f"Usuário do Google registrado: {email}")
        return usuario

    def login_com_facebook(self, email: str, nome: str) -> User:
        """Login com conta do Facebook"""
        self.validar_string(email, "Email")
        self.validar_string(nome, "Nome")

        usuario_id = f"facebook_{email.split('@')[0]}"

        usuario = User(
            usuario_id,
            nome,
            email,
            None,
            "CADASTRO_PARCIAL"
        )

        self._usuarios[usuario_id] = usuario
        self.log(f"Usuário do Facebook registrado: {nome}")
        return usuario

    def obter_progresso_cadastro(self, usuario: User) -> int:
        """
        Obtém percentual de progresso do registro

        Args:
            usuario: Objeto do usuário

        Returns:
            Percentual de progresso (0-100)
        """
        progresso_map = {
            "NAO_CADASTRADO": 0,
            "CADASTRO_PARCIAL": 50,
            "CADASTRO_COMPLETO": 100
        }
        return progresso_map.get(usuario.status, 0)

    def completar_cadastro(self, usuario: User, telefone: str) -> User:
        """Completa o registro do usuário"""
        self.validar_string(telefone, "Telefone")
        usuario.completar_cadastro(telefone)
        self.log(f"Registro do usuário concluído: {usuario.nome}")
        return usuario
