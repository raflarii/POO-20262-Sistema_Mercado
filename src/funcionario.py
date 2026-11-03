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
        if novo_nome.strip(): 
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

    def autenticar(self, senha_tentativa: str) -> bool: 
        if self.__senha == senha_tentativa:
            self.logado = True
            return True
        return False

    @abstractmethod 
    def obter_permissoes(self) -> str:
        pass


class OperadorCaixa(Funcionario): 
    def obter_permissoes(self) -> str:
        return "Permissão restrita: Processar vendas no caixa."

class Gerente(Funcionario):
    def obter_permissoes(self) -> str:
        return "Permissão total: Operar caixa, alterar estoque e acessar relatórios."



def carregar_funcionarios_do_txt(caminho_arquivo: str):
    lista_funcionarios = [] # Lista simples, similar ao std::vector do C++
    
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue # pula linhas em branco
                
                
                nome, id_func, senha, cargo = linha.split() #  split() vazio separa a string pelos espaços automaticamente
                id_func = int(id_func) # converte o texto do ID para número inteiro
                
                if cargo == "Gerente":
                    lista_funcionarios.append(Gerente(nome, id_func, senha))
                elif cargo == "Operador":
                    lista_funcionarios.append(OperadorCaixa(nome, id_func, senha))
                    
    except FileNotFoundError:
        print(f"Aviso: O arquivo '{caminho_arquivo}' não foi encontrado.")
    except ValueError:
        print("Erro: O arquivo txt deve conter Nome ID Senha Cargo separados por espaço.")
        
    return lista_funcionarios