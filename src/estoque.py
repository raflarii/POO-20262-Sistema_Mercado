from produtos import ProdutoUnitario, ProdutoPesavel

# Iniciando a classe
class Estoque:
    def __init__(self, caminho_arquivo="data/estoque.txt"):
        self.__produtos = [] # Lista recebe os produtos com tuplas
        self.__quantidades = {} # Dicionário recebe a quantidade com o id
        self.__caminho_arquivo = caminho_arquivo
        self.carregar_estoque() # Carrega o arquivo e atribui os produtos para os dois selfs acima

    def buscar_produto(self, id_produto):
        for produto in self.__produtos:
            if produto.id == id_produto:
                return produto
        return None

    def adicionar_produto(self, produto, quantidade):
        if self.buscar_produto(produto.id) is not None:
            print("Erro: Já existe um produto com esse ID.")
            return

        if quantidade <= 0:
            print("Erro: A quantidade deve ser maior que zero.")
            return

        if isinstance(produto, ProdutoUnitario) and not isinstance(quantidade, int):
            print("Erro: A quantidade de produtos unitários deve ser inteira.")
            return

        self.__produtos.append(produto)
        self.__quantidades[produto.id] = quantidade

        self.salvar_estoque()
        print("Produto adicionado com sucesso!")

    def remover_produto(self, id_produto):
        produto = self.buscar_produto(id_produto)

        if produto is None:
            print("Produto não encontrado.")
            return

        self.__produtos.remove(produto)
        del self.__quantidades[id_produto]

        self.salvar_estoque()
        print("Produto removido com sucesso!")

    def consultar_quantidade(self, id_produto):
        if self.buscar_produto(id_produto) is None:
            print("Produto não encontrado.")
            return

        return self.__quantidades[id_produto]

    def adicionar_quantidade(self, id_produto, quantidade):
        produto = self.buscar_produto(id_produto)

        if produto is None:
            print("Produto não encontrado.")
            return

        if quantidade <= 0:
            print("Erro: A quantidade deve ser maior que zero.")
            return

        if isinstance(produto, ProdutoUnitario) and not isinstance(quantidade, int):
            print("Erro: A quantidade deve ser inteira.")
            return

        self.__quantidades[id_produto] += quantidade
        self.salvar_estoque()
        print("Quantidade adicionada com sucesso!")

    def retirar_quantidade(self, id_produto, quantidade):
        produto = self.buscar_produto(id_produto)

        if produto is None:
            print("Produto não encontrado.")
            return

        if quantidade <= 0:
            print("Erro: A quantidade deve ser maior que zero.")
            return

        if isinstance(produto, ProdutoUnitario) and not isinstance(quantidade, int):
            print("Erro: A quantidade deve ser inteira.")
            return

        if quantidade > self.__quantidades[id_produto]:
            print("Erro: Quantidade insuficiente no estoque.")
            return

        self.__quantidades[id_produto] -= quantidade
        self.salvar_estoque()
        print("Quantidade retirada com sucesso!")

    def listar_produtos(self):
        if not self.__produtos:
            print("O estoque está vazio.")
            return

        print("--- PRODUTOS DO ESTOQUE ---")

        for produto in self.__produtos:
            quantidade = self.__quantidades[produto.id]

            if isinstance(produto, ProdutoUnitario):
                unidade = "unidades"
            else:
                unidade = "kg"

            print(f"ID: {produto.id}")
            print(f"Nome: {produto.nome}")
            print(f"Preço: R$ {produto.preco:.2f}")
            print(f"Quantidade: {quantidade} {unidade}")
            print("--------------------------")

    def carregar_estoque(self):
        try:
            with open(self.__caminho_arquivo, "r", encoding="utf-8-sig") as arquivo:
                for linha in arquivo:
                    linha = linha.strip()

                    if not linha:
                        continue

                    id_produto, nome, preco, tipo, quantidade = linha.split()

                    id_produto = int(id_produto)
                    preco = float(preco)

                    if tipo == "Unitario":
                        produto = ProdutoUnitario(id_produto, nome, preco)
                        quantidade = int(quantidade)

                    elif tipo == "Pesavel":
                        produto = ProdutoPesavel(id_produto, nome, preco)
                        quantidade = float(quantidade)

                    else:
                        print(f"Tipo de produto inválido: {tipo}")
                        continue

                    self.__produtos.append(produto)
                    self.__quantidades[id_produto] = quantidade

        except FileNotFoundError:
            print("Arquivo de estoque não encontrado. Estoque iniciado vazio.")

        except ValueError:
            print("Erro ao ler o arquivo de estoque. Verifique seu formato.")

    def repor_item(self): # adcionada a função repor_item() para o menu do operador
        """Interface interativa que conecta o sistema.py à lógica do Estoque."""
        print("\n--- REPOSIÇÃO DE PRODUTOS ---")
        try:
            id_produto = int(input("Digite o ID do produto: ").strip())
            quantidade = float(input("Quantidade a adicionar: ").strip())

            if quantidade.is_integer(): # foi adcionada estas duas linhas para converter a quantidade para inteiro caso seja um número inteiro
                quantidade = int(quantidade)
            
            self.adicionar_quantidade(id_produto, quantidade)
        except ValueError:
            print("Erro: Digite apenas números válidos.")

    def salvar_estoque(self):
        try:
            with open(self.__caminho_arquivo, "w", encoding="utf-8") as arquivo:
                for produto in self.__produtos:
                    quantidade = self.__quantidades[produto.id]

                    if isinstance(produto, ProdutoUnitario):
                        tipo = "Unitario"
                    else:
                        tipo = "Pesavel"

                    arquivo.write(
                        f"{produto.id} {produto.nome} "
                        f"{produto.preco:.2f} {tipo} {quantidade:g}\n"
                    )

        except IOError:
            print("Erro ao salvar o arquivo de estoque.")