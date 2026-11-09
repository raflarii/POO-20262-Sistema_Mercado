from abc import ABC, abstractmethod

class Funcionario(ABC):
    """Classe abstrata que reúne os dados comuns dos funcionários."""
    def __init__(self, nome: str, id_func: int, senha: str):
        """Inicializa os dados e o estado de login."""
        self.__nome = nome
        self.__id = id_func
        self.__senha = senha
        self.__logado = False  

    @property
    def nome(self):
        """Consulta ou altera o nome do funcionário."""
        return self.__nome

    @property
    def id(self):
        """Consulta ou altera o identificador do funcionário."""
        return self.__id

    @property
    def senha(self):
        """Consulta ou altera a senha do funcionário."""
        return self.__senha

    @property
    def logado(self):
        """Consulta ou altera o estado de login."""
        return self.__logado

    @nome.setter
    def nome(self, novo_nome: str):
        """Consulta ou altera o nome do funcionário."""
        if novo_nome.strip(): 
            self.__nome = novo_nome
        else:
            raise ValueError("O nome não pode estar vazio.")

    @id.setter
    def id(self, novo_id: int):
        """Consulta ou altera o identificador do funcionário."""
        self.__id = novo_id

    @senha.setter
    def senha(self, nova_senha: str):
        """Consulta ou altera a senha do funcionário."""
        self.__senha = nova_senha

    @logado.setter
    def logado(self, status: bool):
        """Consulta ou altera o estado de login."""
        self.__logado = status

    def autenticar(self, senha_tentativa: str) -> bool: 
        """Valida a senha informada e registra o login."""
        if self.__senha == senha_tentativa:
            self.logado = True
            return True
        return False

    @abstractmethod 
    def obter_permissoes(self) -> str:
        """Define as permissões específicas de cada cargo."""
        pass

class OperadorCaixa(Funcionario): 
    """Representa um funcionário com permissões de operador."""
    def obter_permissoes(self) -> str:
        """Retorna as permissões do operador de caixa."""
        return "Permissão restrita: Processar vendas no caixa."

class Gerente(Funcionario):
    """Representa um funcionário com permissões de gerente."""
    def obter_permissoes(self) -> str:
        """Retorna as permissões do gerente."""
        return "Permissão total: Operar caixa, alterar estoque e acessar relatórios."

def carregar_funcionarios_do_txt(caminho_arquivo: str):
    """Lê os funcionários cadastrados em arquivo de texto."""
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