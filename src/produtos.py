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

    @preco.setter
    def preco(self, novo_preco: float):
        if novo_preco > 0:
            self.__preco = novo_preco
        else:
            raise ValueError("O preço deve ser maior que zero.")

    def atualizar_disponibilidade(self, status: bool):
        self.__disponivel = status

    @abstractmethod 
    def calcular_valor_venda(self, quantidade) -> float:
        pass


class ProdutoUnitario(Produto): 
    def __init__(self, id_produto: int, nome: str, preco: float):
        super().__init__(id_produto, nome, preco)

    def calcular_valor_venda(self, quantidade: int) -> float:   
        return self.preco * quantidade



class ProdutoPesavel(Produto):
    def __init__(self, id_produto: int, nome: str, preco: float):
        super().__init__(id_produto, nome, preco)

    def calcular_valor_venda(self, peso_kg: float) -> float:   
        return self.preco * peso_kg



def carregar_produtos_do_txt(caminho_arquivo: str):
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
                preco = float(preco) # Converte o preço de texto para decimal
                
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