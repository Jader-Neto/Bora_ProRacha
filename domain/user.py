"""
Usuário - Entidade representando um usuário do sistema
Com encapsulamento: atributos privados com propriedades
"""
from datetime import datetime
from typing import Optional, Literal
from .base import BaseEntity

UserStatus = Literal["NAO_CADASTRADO", "CADASTRO_PARCIAL", "CADASTRO_COMPLETO"]


class User(BaseEntity):
    """
    Entidade de usuário com encapsulamento e validação.
    """
    def __init__(
        self,
        user_id: str,
        nome: str,
        email: str,
        telefone: Optional[str] = None,
        status: UserStatus = "NAO_CADASTRADO"
    ):
        super().__init__(user_id)
        self._nome = nome
        self._email = email
        self._telefone = telefone
        self._status = status
        self._data_cadastro = datetime.now()
        self._validar()

    def _validar(self) -> None:
        """Validar dados do usuário"""
        if "@" not in self._email:
            raise ValueError("Email inválido")
        if self._status == "CADASTRO_COMPLETO" and not self._telefone:
            raise ValueError("Telefone é obrigatório para cadastro completo")

    # Propriedades
    @property
    def nome(self) -> str:
        return self._nome

    @property
    def email(self) -> str:
        return self._email

    @property
    def telefone(self) -> Optional[str]:
        return self._telefone

    @property
    def status(self) -> UserStatus:
        return self._status

    @property
    def data_cadastro(self) -> datetime:
        return self._data_cadastro

    # Modificadores com validação
    @nome.setter
    def nome(self, nome: str) -> None:
        if not nome or not nome.strip():
            raise ValueError("Nome não pode ser vazio")
        self._nome = nome

    @email.setter
    def email(self, email: str) -> None:
        if "@" not in email:
            raise ValueError("Email inválido")
        self._email = email

    @telefone.setter
    def telefone(self, telefone: str) -> None:
        if not telefone or not telefone.strip():
            raise ValueError("Telefone não pode ser vazio")
        self._telefone = telefone

    # Métodos de negócio
    def completar_cadastro(self, telefone: str) -> None:
        """Completar registro do usuário"""
        if not telefone or not telefone.strip():
            raise ValueError("Telefone não pode ser vazio")
        self._telefone = telefone
        self._status = "CADASTRO_COMPLETO"

    def pode_reservar(self) -> bool:
        """Verificar se o usuário pode fazer reservas"""
        return self._status == "CADASTRO_COMPLETO"

    def __repr__(self):
        return f"User(id={self.id}, nome={self._nome}, email={self._email}, status={self._status})"
