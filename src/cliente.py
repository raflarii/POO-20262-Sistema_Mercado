import os

class Cliente:
    def __init__(self, nome: str, cpf: str): # encapsulamento dos atributos privados
        self.__nome = nome
        self.__cpf = cpf
        self.__total_gasto = 0.0
        self.__historico_compras = []

    @property # uso da property para guardar os atributos 
    def nome(self):
        return self.__nome

    @property
    def cpf(self):
        return self.__cpf

    @property
    def total_gasto(self):
        return self.__total_gasto

    def registrar_compra(self, descricao: str, valor: float):
        self.__historico_compras.append(descricao)
        self.__total_gasto += valor

    def mostrar_historico(self):
        print(f"Histórico de compras de {self.__nome}:")
        for item in self.__historico_compras:
            print(f"- {item}")
        print(f"Total gasto: R$ {self.__total_gasto:.2f}")

    def salvar_historico(self):
        os.makedirs("data", exist_ok=True) 
        nome_arquivo = f"data/historico_{self.__cpf}.txt"
        
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo: 
                arquivo.write(f"Cliente: {self.__nome} ({self.__cpf})\n")
                arquivo.write("Compras:\n")
                for item in self.__historico_compras:
                    arquivo.write(f"- {item}\n")
                arquivo.write(f"Total gasto: {self.__total_gasto:.2f}\n")
        except IOError:
            print("Erro ao salvar histórico.")

    def carregar_historico(self):
        nome_arquivo = f"data/historico_{self.__cpf}.txt"
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
                historico = []
                total_gasto = 0.0
                for linha in arquivo:
                    if linha.startswith("- "):
                        historico.append(linha[2:].strip())
                    elif linha.startswith("Total gasto:"):
                        valor = linha.split(":", 1)[1].strip()
                        total_gasto = float(valor)

                self.__historico_compras = historico
                self.__total_gasto = total_gasto
        except FileNotFoundError:
            # Cliente ainda não realizou compras.
            pass
        except (ValueError, OSError):
            print("Erro ao carregar histórico de compras do cliente.")



def carregar_clientes_do_txt(caminho_arquivo: str):
    lista_clientes = [] 
    
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue 
                
                cpf, nome = linha.split()  # desempacota seguindo a ordem do seu txt: CPF primeiro, Nome depois

                
                lista_clientes.append(Cliente(nome, cpf))
                
    except FileNotFoundError:
        print(f"Aviso: O arquivo '{caminho_arquivo}' não foi encontrado.")
    except ValueError:
        print("Erro: O arquivo txt deve conter CPF e Nome separados por espaço.")
        
    return lista_clientes