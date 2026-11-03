from abc import ABC, abstractmethod

class Produto(ABC):
    def __init__(self, id_produto: int, nome: str, preco: float):
        self.__id = id_produto
        self.__nome = nome
        self.__preco = preco
        self.__disponivel = True

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

    @abstractmethod # nesta linha a abstração obriga as classes filhas a implementarem este método
    def calcular_valor_venda(self, quantidade) -> float:
        pass


class ProdutoUnitario(Produto): # herança: ProdutoUnitario herda de Produto

    def __init__(self, id_produto: int, nome: str, preco: float):
        super().__init__(id_produto, nome, preco)

    def calcular_valor_venda(self, quantidade: int) -> float:   # polimorfismo implementa o método abstrato 

        return self.preco * quantidade