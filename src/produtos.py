from abc import ABC, abstractmethod

class Produto(ABC):
    """Classe abstrata com os dados comuns dos produtos."""
    def __init__(self, id_produto: int, nome: str, preco: float):
        """Inicializa os atributos básicos do produto."""
        self.__id = id_produto
        self.__nome = nome
        self.__preco = preco
        self.__disponivel = True

    @property
    def id(self):
        """Retorna o identificador do produto."""
        return self.__id

    @property
    def nome(self):
        """Retorna o nome do produto."""
        return self.__nome

    @property
    def preco(self):
        """Consulta ou altera o preço do produto."""
        return self.__preco

    @property
    def disponivel(self):
        """Indica se o produto está disponível."""
        return self.__disponivel

    @preco.setter
    def preco(self, novo_preco: float):
        """Consulta ou altera o preço do produto."""
        if novo_preco > 0:
            self.__preco = novo_preco
        else:
            raise ValueError("O preço deve ser maior que zero.")

    def atualizar_disponibilidade(self, status: bool):
        """Atualiza a disponibilidade do produto."""
        self.__disponivel = status

    @abstractmethod 
    def calcular_valor_venda(self, quantidade) -> float:
        """Define o cálculo do valor de venda."""
        pass

class ProdutoUnitario(Produto): 
    """Representa produtos vendidos por unidade."""
    def __init__(self, id_produto: int, nome: str, preco: float):
        """Inicializa um produto vendido por unidade."""
        super().__init__(id_produto, nome, preco)

    def calcular_valor_venda(self, quantidade: int) -> float:   
        """Calcula o valor pela quantidade de unidades."""
        return self.preco * quantidade

class ProdutoPesavel(Produto):
    """Representa produtos vendidos por peso."""
    def __init__(self, id_produto: int, nome: str, preco: float):
        """Inicializa um produto vendido por peso."""
        super().__init__(id_produto, nome, preco)

    def calcular_valor_venda(self, peso_kg: float) -> float:   
        """Calcula o valor pelo peso em quilogramas."""
        return self.preco * peso_kg

def carregar_produtos_do_txt(caminho_arquivo: str):
    """Lê os produtos cadastrados em arquivo de texto."""
    lista_produtos = [] 

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue 
                
                # desempacota assumindo formato: ID Nome Preço Tipo
                id_prod, nome, preco, tipo = linha.split()
                
                id_prod = int(id_prod)
                preco = float(preco) # converte o preço de texto para decimal
                
                # polimorfismo na instanciação
                if tipo == "Unitario":
                    lista_produtos.append(ProdutoUnitario(id_prod, nome, preco))
                elif tipo == "Pesavel":
                    lista_produtos.append(ProdutoPesavel(id_prod, nome, preco))
                
    except FileNotFoundError:
        print(f"Aviso: O arquivo '{caminho_arquivo}' não foi encontrado.")
    except ValueError:
        print("Erro: O estoque.txt deve conter ID Nome Preco Tipo separados por espaço.")
        
    return lista_produtos