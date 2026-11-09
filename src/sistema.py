import os
from funcionario import Gerente, OperadorCaixa
from cliente import Cliente
from estoque import Estoque
from caixa import Caixa 

class Sistema:
    """
    Matriz do sistema de supermercado.

    Responsável por inicializar os menus iterativos, gerir a autenticação
    dos usuários e garantir o tratamento de erros durante a interação
    através do terminal.
    """

    def __init__(self):
        """
        Inicializa o sistema e carrega os dados persistentes.

        As listas instanciam os objetos diretamente a partir dos arquivos
        .txt locais para simular a base de dados do projeto.
        """
        self.funcionarios = self._carregar_funcionarios()
        self.clientes = self._carregar_clientes()
        self.cliente_logado = None
        self.estoque = Estoque()

    def limpar_ecra(self):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print('\033c', end='')

    def pausar(self):
        """Pausa a execução para que o usuário possa ler as mensagens do sistema."""
        input("\nPressione ENTER para continuar...")

    def iniciar(self):
        """
        Loop principal que exibe o menu de entrada do supermercado.

        Garante o tratamento de erros com blocos try/except caso o usuário
        digite caracteres inválidos.
        """
        while True:
            self.limpar_ecra()
            print(" SUPERMERCADO - MENU PRINCIPAL ")
            print("1. Área do Cliente")
            print("2. Área do Funcionário")
            print("3. Sair")

            try:
                opcao = int(input("\nEscolha uma opção: "))

                if opcao == 1:
                    self._menu_cliente_principal()
                elif opcao == 2:
                    self._menu_funcionario_login()
                elif opcao == 3:
                    print("\nEncerrando o sistema...")
                    break
                else:
                    print("\nOpção inválida.")
                    self.pausar()
            except ValueError:
                print("\nErro: Por favor, digite apenas números inteiros.")
                self.pausar()

    def _login_cliente(self):
        """Valida a existência do CPF na lista de clientes carregados."""
        self.limpar_ecra()
        print("--- LOGIN ---")

        if not self.clientes:
            print("Que pena! Não há nenhum cliente registrado. Por favor, registre-se primeiro.") 
            self.pausar()
            return        

        cpf_input = input("Digite o seu CPF: ").strip()

        for cliente in self.clientes: 
            if cliente.cpf == cpf_input: 
                self.cliente_logado = cliente
                print(f"\nLogin efetuado com sucesso! Bem-vindo(a), {cliente.nome}.")
                self.pausar()
                
                self._menu_compras_cliente()
                return

        print("\nCPF não encontrado no sistema.")
        self.pausar()

    def _menu_cliente_principal(self):
        """Menu que direciona o cliente para o login ou registro."""
        while True:
            self.limpar_ecra()
            print("--- MENU DO CLIENTE ---")
            print("1. Fazer Login")
            print("2. Criar Registro")
            print("3. Voltar")

            try:
                opcao = int(input("\nEscolha uma opção: "))

                if opcao == 1:
                    self._login_cliente()
                elif opcao == 2:
                    self._registrar_cliente()
                elif opcao == 3:
                    break
                else:
                    print("\nOpção inválida.")
                    self.pausar()
            except ValueError:
                print("\nErro: Entrada inválida.")
                self.pausar()

    def _menu_funcionario_login(self):
        """
        Processa a autenticação de Gerentes e Operadores.

        Interage com o método 'autenticar' da classe Funcionario,
        protegendo as senhas originais.
        """
        self.limpar_ecra()
        print("--- ACESSO RESTRITO ---")
        try:
            id_func = int(input("ID: ").strip())
            senha = input("Senha: ")

            # procura o funcionário na lista carregada
            funcionario_encontrado = None
            for func in self.funcionarios:
                if func.id == id_func:
                    funcionario_encontrado = func
                    break

            if funcionario_encontrado and funcionario_encontrado.autenticar(senha):
                print(f"\nBem-vindo, {funcionario_encontrado.nome}!")
                print(funcionario_encontrado.obter_permissoes())
                self.pausar()
                self._menu_gestao(funcionario_encontrado)
            else:
                print("\nAcesso negado: Credenciais incorretas ou funcionário inexistente.")
                self.pausar()
        except ValueError:
            print("\nErro: O ID deve ser composto apenas por números.")
            self.pausar()

    def _menu_gestao(self, funcionario):
        """Painel de controle com restrição de acesso por herança."""
        while True:
            self.limpar_ecra()
            print(f"--- PAINEL DE CONTROLE: {funcionario.nome.upper()} ---")
            
            is_gerente = isinstance(funcionario, Gerente) # verifica de qual classe o objeto veio
            
            if is_gerente:
                print("1. Repor Estoque (Exclusivo Gerência)")
                
            print("2. Visualizar Estoque Completo")
            print("3. Fazer Logout")
            
            try:
                opcao = int(input("\nEscolha uma opção: ").strip())
                
                if opcao == 1 and is_gerente:
                    self.limpar_ecra()
                    self.estoque.repor_item() # aciona a função interativa de reposição do estoque
                    self.pausar()
                    
                elif opcao == 1 and not is_gerente:
                    print("\nErro: Acesso negado. Opção restrita à gerência.")
                    self.pausar()
                    
                elif opcao == 2:
                    self.limpar_ecra()
                    self.estoque.listar_produtos()  # executa a função de listagem do estoque
                    self.pausar()
                    
                elif opcao == 3:
                    print(f"\nEncerrando a sessão de {funcionario.nome}...")
                    self.pausar()
                    break 
                else:
                    print("\nOpção inválida.")
                    self.pausar()
                    
            except ValueError:
                print("\nErro: Digite apenas o número da opção.")
                self.pausar()


    def _registrar_cliente(self):
        """Grava um novo cliente na memória e atualiza o arquivo .txt."""
        self.limpar_ecra()
        print("--- NOVO REGISTRO :D ---")
        nome = input("Nome: ").strip()
        cpf = input("CPF: ").strip()

        if not nome or not cpf: # esta linha foi adcionada para evitar que o usuário registre um cliente com nome ou CPF vazio
            print("\nErro: Nome e CPF não podem estar vazios.")
            self.pausar()
            return

        if not cpf.isdigit(): # aqui verifica se o CPF contém apenas números, caso contrário, retorna um erro
            print("\nErro: O CPF deve conter apenas números.")
            self.pausar()
            return
        
        for cliente in self.clientes: # verifica se o CPF já existe
            if cliente.cpf == cpf:
                print("\nErro: Este CPF já está registado.")
                self.pausar()
                return

        try:
            import os
            os.makedirs("data", exist_ok=True)  # cria a pasta "data" se não existir

            with open("data/clientes.txt", "a", encoding="utf-8") as f:
                f.write(f"{cpf} {nome}\n") # grava o novo cliente no arquivo
            novo_cliente = Cliente(nome, cpf)
            self.clientes.append(novo_cliente)
            print("\nEba! Registro concluído!")
        except IOError:
            print("\nUai... Falha ao gravar no arquivo de clientes. O cadastro não foi concluído.")

        self.pausar()

    def _menu_compras_cliente(self):
        """Menu restrito para clientes autenticados realizarem compras."""
        while self.cliente_logado:
            self.limpar_ecra()
            print(f"Olá, {self.cliente_logado.nome}!")
            print("1. Iniciar Compra")
            print("2. Ver Histórico")
            print("3. Logout")

            try:
                opcao = int(input("\nEscolha: "))

                if opcao == 1:
                    print("\nDirecionando para o Caixa...")
                    self.pausar()
                    self.caixa = Caixa(self.estoque)
                    self.caixa.iniciar_atendimento(self.cliente_logado)
                elif opcao == 2:
                    self.limpar_ecra()
                    self.cliente_logado.mostrar_historico()
                    self.pausar()
                elif opcao == 3:
                    self.cliente_logado = None
                else:
                    print("\nOpção inválida.")
                    self.pausar()
            except ValueError:
                print("\nErro: Por favor, digite uma opção válida.")
                self.pausar()


    def _carregar_funcionarios(self) -> list:
        """Lê o arquivo e instancia a lista de funcionários."""
        lista = []
        try:
            with open("data/funcionarios.txt", "r", encoding="utf-8-sig") as f:
                for linha in f:
                    linha = linha.strip()
                    if linha.strip():
                        partes = linha.split()
                        if len(partes) == 4:
                            nome, id_func, senha, cargo = partes
                            if cargo == "Gerente":
                                lista.append(Gerente(nome, int(id_func), senha))
                            elif cargo == "Operador":
                                lista.append(OperadorCaixa(nome, int(id_func), senha))
        except (FileNotFoundError, ValueError):
            print("Uai... Falha ao carregar funcionários")
        return lista


    def _carregar_clientes(self) -> list:
        """Lê o arquivo e instancia a lista de clientes."""
        lista = []
        try:
            with open("data/clientes.txt", "r", encoding="utf-8-sig") as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:
                        partes = linha.split(maxsplit=1)
                        if len(partes) == 2:
                            cpf = partes[0].strip()
                            nome = partes[1].strip()
                            cliente = Cliente(nome, cpf)
                            cliente.carregar_historico()
                            lista.append(cliente)
        except (FileNotFoundError, ValueError):
            print("Uai... Falha ao carregar clientes")
        return lista

if __name__ == "__main__":
    app = Sistema()
    app.iniciar()
