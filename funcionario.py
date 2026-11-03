from abc import ABC, abstractmethod

class Funcionario(ABC):
    def __init__(self, nome: str, id_func: int, senha: str):
        self.__nome = nome
        self.__id = id_func
        self.__senha = senha
        self.__logado = False  

    @property
    def nome(self):
        return self.__nome

    @property
    def id(self):
        return self.__id

    @property
    def senha(self):
        return self.__senha

    @property
    def logado(self):
        return self.__logado

    @nome.setter
    def nome(self, novo_nome: str):
        if novo_nome.strip(): # validação para impedir nomes vazios
            self.__nome = novo_nome
        else:
            raise ValueError("O nome não pode estar vazio.")

    @id.setter
    def id(self, novo_id: int):
        self.__id = novo_id

    @senha.setter
    def senha(self, nova_senha: str):
        self.__senha = nova_senha

    @logado.setter
    def logado(self, status: bool):
        self.__logado = status

    def autenticar(self, senha_tentativa: str) -> bool: # encapsulamento da lógica de login
        if self.__senha == senha_tentativa:
            self.logado = True
            return True
        return False

    @abstractmethod # o metodo abstrato eh usado pra obrigar as classes filhas a definirem suas permissões
    def obter_permissoes(self) -> str:
        pass


class OperadorCaixa(Funcionario): # uso da herança!!
    def obter_permissoes(self) -> str:
        return "Permissão restrita: Processar vendas no caixa."

class Gerente(Funcionario):
    def obter_permissoes(self) -> str:
        return "Permissão total: Operar caixa, alterar estoque e acessar relatórios."