from abc import ABC, abstractmethod

class Produto(ABC):
    def __init__(self, id_produto: int, nome: str, preco: float):
        # Encapsulamento: Atributos privados iniciados com __
        self.__id = id_produto
        self.__nome = nome
        self.__preco = preco
        self.__disponivel = True

    # Getters usando o decorador @property
    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def preco(self):
        return self.__preco

    @property
    def disponivel(self):
        return self.__disponivel

    # Setters para validação de regras de negócio
    @preco.setter
    def preco(self, novo_preco: float):
        if novo_preco > 0:
            self.__preco = novo_preco
        else:
            raise ValueError("O preço deve ser maior que zero.")

    def atualizar_disponibilidade(self, status: bool):
        self.__disponivel = status

    # Abstração: Obriga as classes filhas a implementarem este método
    @abstractmethod
    def calcular_valor_venda(self, quantidade) -> float:
        pass


# Herança: ProdutoUnitario herda de Produto
class ProdutoUnitario(Produto):
    def __init__(self, id_produto: int, nome: str, preco: float):
        super().__init__(id_produto, nome, preco)

    # Polimorfismo: Implementação específica do método abstrato
    def calcular_valor_venda(self, quantidade: int) -> float:
        return self.preco * quantidade