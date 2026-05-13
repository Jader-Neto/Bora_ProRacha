"""
Estratégias de cálculo - Implementa o padrão Strategy
"""
from abc import ABC, abstractmethod

from .interfaces import ICalculadora


class EstrategiaCalculo(ABC, ICalculadora):
    """Classe base para estratégias de cálculo"""
    @abstractmethod
    def calcular(self, valor: float) -> float:
        pass

    @abstractmethod
    def obter_descricao(self) -> str:
        pass


class CalculoPrecoBase(EstrategiaCalculo):
    """Cálculo de preço base sem descontos"""
    def calcular(self, valor: float) -> float:
        return valor

    def obter_descricao(self) -> str:
        return "Preço base (sem desconto)"


class CalculoComDesconto(EstrategiaCalculo):
    """Cálculo de preço com desconto percentual"""
    def __init__(self, percentual_desconto: float):
        if not 0 <= percentual_desconto <= 100:
            raise ValueError("Desconto deve estar entre 0 e 100")
        self.percentual_desconto = percentual_desconto

    def calcular(self, valor: float) -> float:
        return valor * (1 - self.percentual_desconto / 100)

    def obter_descricao(self) -> str:
        return f"Preço com {self.percentual_desconto}% de desconto"


class CalculoComTaxa(EstrategiaCalculo):
    """Cálculo de preço com taxa fixa"""
    def __init__(self, taxa_fixa: float):
        if taxa_fixa < 0:
            raise ValueError("Taxa não pode ser negativa")
        self.taxa_fixa = taxa_fixa

    def calcular(self, valor: float) -> float:
        return valor + self.taxa_fixa

    def obter_descricao(self) -> str:
        return f"Preço com taxa fixa R$ {self.taxa_fixa}"


class CalculoProgressivo(EstrategiaCalculo):
    """Preço progressivo baseado em faixas de valor"""
    def __init__(self):
        self.faixas = [
            (100, 0.05),    # 5% para valores até 100
            (500, 0.10),    # 10% para valores até 500
            (float('inf'), 0.15)  # 15% para valores acima de 500
        ]

    def calcular(self, valor: float) -> float:
        for limite, desconto in self.faixas:
            if valor <= limite:
                return valor * (1 - desconto)
        return valor

    def obter_descricao(self) -> str:
        return "Desconto progressivo baseado em valor"


class CalculoComMultiplos(EstrategiaCalculo):
    """Aplicar múltiplas estratégias de cálculo sequencialmente"""
    def __init__(self, calculos: list):
        self.calculos = calculos

    def calcular(self, valor: float) -> float:
        resultado = valor
        for calculo in self.calculos:
            resultado = calculo.calcular(resultado)
        return resultado

    def obter_descricao(self) -> str:
        descricoes = [c.obter_descricao() for c in self.calculos]
        return " → ".join(descricoes)
