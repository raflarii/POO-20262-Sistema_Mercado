from decimal import Decimal, ROUND_HALF_UP
from produtos import ProdutoUnitario, ProdutoPesavel


class Caixa:
    """Controla o carrinho, o pagamento e a finalização de uma compra."""

    def __init__(self, estoque):
        self.__estoque = estoque  # reutiliza o mesmo estoque do Sistema
        self.__carrinho = {}  # ID do produto: [objeto Produto, quantidade]

    @property
    def carrinho(self):
        """Devolve uma cópia das quantidades, protegendo o carrinho original."""
        return {id_produto: item[1] for id_produto, item in self.__carrinho.items()}

    def adicionar_item(self, id_produto: int, quantidade):
        """Adiciona unidades ou kg, respeitando o tipo e o estoque disponível."""
        produto = self.__estoque.buscar_produto(id_produto)
        if produto is None:
            raise ValueError("Produto não encontrado.")

        if isinstance(quantidade, bool) or not isinstance(quantidade, (int, float)):
            raise ValueError("Digite uma quantidade numérica válida.")
        if quantidade != quantidade or quantidade == float('inf') or quantidade == float('-inf'):
            raise ValueError("A quantidade deve ser um número finito.")
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if isinstance(produto, ProdutoUnitario) and not float(quantidade).is_integer():
            raise ValueError("Produtos unitários exigem quantidade inteira.")

        if isinstance(produto, ProdutoUnitario):
            quantidade = int(quantidade)

        quantidade_atual = self.__carrinho.get(id_produto, [produto, 0])[1]
        quantidade_disponivel = self.__estoque.consultar_quantidade(id_produto)
        if quantidade_atual + quantidade > quantidade_disponivel + 1e-9:
            raise ValueError("Quantidade insuficiente no estoque.")

        self.__carrinho[id_produto] = [produto, quantidade_atual + quantidade]
        print(f"{produto.nome} adicionado ao carrinho!")

    def remover_item(self, id_produto: int):
        """Retira por completo um produto selecionado do carrinho."""
        if id_produto not in self.__carrinho:
            raise ValueError("Este produto não está no carrinho.")
        del self.__carrinho[id_produto]
        print("Produto removido do carrinho!")

    def calcular_total(self) -> float:
        """Usa o polimorfismo de Produto para calcular o total da compra."""
        total = Decimal('0')
        for produto, quantidade in self.__carrinho.values():
            subtotal = produto.calcular_valor_venda(quantidade)
            total += Decimal(str(subtotal))
        return float(total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

    def visualizar_carrinho(self):
        """Mostra os itens, subtotais e total antes do pagamento."""
        print("\n--- CARRINHO DE COMPRAS ---")
        if not self.__carrinho:
            print("Seu carrinho está vazio.")
            return

        for produto, quantidade in self.__carrinho.values():
            unidade = 'un.' if isinstance(produto, ProdutoUnitario) else 'kg'
            subtotal = produto.calcular_valor_venda(quantidade)
            print(f"{produto.nome} | {quantidade:g} {unidade} | R$ {subtotal:.2f}")
        print(f"TOTAL: R$ {self.calcular_total():.2f}")

    def finalizar_compra(self, cliente, forma_pagamento: str, valor_recebido=None) -> float:
        """Confirma uma venda, baixa o estoque e registra o histórico do cliente.

        O pagamento é apenas simulado (não se conecta a bancos ou cartões).
        Retorna o troco, ou zero para pagamentos sem dinheiro.
        """
        if not self.__carrinho:
            raise ValueError("Não é possível finalizar uma compra com carrinho vazio.")

        forma_pagamento = forma_pagamento.strip().lower()
        if forma_pagamento not in ('dinheiro', 'pix', 'cartao', 'cartão'):
            raise ValueError("Forma de pagamento inválida.")

        total = self.calcular_total()
        troco = 0.0
        if forma_pagamento == 'dinheiro':
            try:
                recebido = Decimal(str(valor_recebido))
            except (ValueError, TypeError, ArithmeticError):
                raise ValueError("Valor recebido inválido.")
            if not recebido.is_finite() or recebido < Decimal(str(total)):
                raise ValueError("Valor recebido insuficiente ou inválido.")
            troco = float((recebido - Decimal(str(total))).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP))

        # Revalida TODOS os itens antes de alterar qualquer quantidade no estoque.
        for id_produto, (_, quantidade) in self.__carrinho.items():
            disponivel = self.__estoque.consultar_quantidade(id_produto)
            if disponivel is None or quantidade > disponivel + 1e-9:
                raise ValueError("O estoque mudou. Revise seu carrinho antes de pagar.")

        descricao = []
        for id_produto, (produto, quantidade) in self.__carrinho.items():
            self.__estoque.retirar_quantidade(id_produto, quantidade)
            unidade = 'un.' if isinstance(produto, ProdutoUnitario) else 'kg'
            descricao.append(f"{produto.nome}: {quantidade:g} {unidade}")

        # Utiliza os métodos de histórico já implementados em Cliente.
        resumo = f"{' | '.join(descricao)} | R$ {total:.2f} ({forma_pagamento})"
        cliente.registrar_compra(resumo, total)
        cliente.salvar_historico()
        self.__carrinho.clear()
        print(f"\nCompra finalizada! Total: R$ {total:.2f}")
        if forma_pagamento == 'dinheiro':
            print(f"Troco: R$ {troco:.2f}")
        return troco

    def iniciar_atendimento(self, cliente):
        """Menu interativo chamado pelo menu de compras do Sistema."""
        self.__carrinho.clear()  # cada atendimento começa com carrinho vazio
        while True:
            print(f"\n--- CAIXA | CLIENTE: {cliente.nome} ---")
            print("1. Ver produtos disponíveis")
            print("2. Adicionar produto ao carrinho")
            print("3. Remover produto do carrinho")
            print("4. Ver carrinho")
            print("5. Finalizar compra")
            print("6. Cancelar e voltar")

            try:
                opcao = int(input("Escolha uma opção: ").strip())
                if opcao == 1:
                    self.__estoque.listar_produtos()
                elif opcao == 2:
                    id_produto = int(input("ID do produto: ").strip())
                    produto = self.__estoque.buscar_produto(id_produto)
                    if produto is None:
                        print("Produto não encontrado.")
                        continue
                    if isinstance(produto, ProdutoUnitario):
                        quantidade = int(input("Quantidade (unidades): ").strip())
                    elif isinstance(produto, ProdutoPesavel):
                        quantidade = float(input("Peso (kg): ").strip().replace(',', '.'))
                    else:
                        print("Tipo de produto inválido.")
                        continue
                    self.adicionar_item(id_produto, quantidade)
                elif opcao == 3:
                    id_produto = int(input("ID do produto a remover: ").strip())
                    self.remover_item(id_produto)
                elif opcao == 4:
                    self.visualizar_carrinho()
                elif opcao == 5:
                    self.visualizar_carrinho()
                    if not self.__carrinho:
                        continue
                    confirmar = input("Confirmar a compra? (s/n): ").strip().lower()
                    if confirmar != 's':
                        continue
                    print("Formas de pagamento: 1. Dinheiro  2. Pix  3. Cartão")
                    pagamento = input("Escolha a forma de pagamento: ").strip()
                    formas = {'1': 'dinheiro', '2': 'pix', '3': 'cartao'}
                    if pagamento not in formas:
                        print("Forma de pagamento inválida.")
                        continue
                    recebido = None
                    if pagamento == '1':
                        recebido = input("Valor recebido (R$): ").strip().replace(',', '.')
                    self.finalizar_compra(cliente, formas[pagamento], recebido)
                    return
                elif opcao == 6:
                    self.__carrinho.clear()
                    print("Compra cancelada. Nenhum item foi retirado do estoque.")
                    return
                else:
                    print("Opção inválida.")
            except ValueError as erro:
                print(f"Erro: {erro}")
