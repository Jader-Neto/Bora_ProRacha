"""
BaseService - Classe base para todos os serviços com métodos utilitários comuns
"""
from typing import Optional, List
import logging


class BaseService:
    """Serviço base com métodos utilitários comuns para todos os serviços"""

    def __init__(self, logger_name: str = "Service"):
        self.logger = logging.getLogger(logger_name)

    def log(self, mensagem: str) -> None:
        """Registra mensagem de informação"""
        self.logger.info(mensagem)

    def aviso(self, mensagem: str) -> None:
        """Registra mensagem de aviso"""
        self.logger.warning(mensagem)

    def erro(self, mensagem: str) -> None:
        """Registra mensagem de erro"""
        self.logger.error(mensagem)

    def validar_string(self, valor: str, campo: str) -> None:
        """Valida campo string"""
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} deve ser uma string não vazia")

    def validar_numero(self, valor: float, campo: str, minimo: float = 0) -> None:
        """Valida campo numérico"""
        if not isinstance(valor, (int, float)):
            raise ValueError(f"{campo} deve ser um número")
        if valor < minimo:
            raise ValueError(f"{campo} deve ser >= {minimo}")

    def validar_lista(self, lista: List, campo: str) -> None:
        """Valida campo lista"""
        if not isinstance(lista, list):
            raise ValueError(f"{campo} deve ser uma lista")
        if len(lista) == 0:
            raise ValueError(f"{campo} não pode estar vazia")
