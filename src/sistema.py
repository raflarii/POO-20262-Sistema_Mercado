import os
from funcionario import Gerente, OperadorCaixa
from cliente import Cliente

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
        # self.estoque = Estoque() 

    def limpar_ecra(self):
        """Limpa o terminal dependendo do sistema operacional."""
        os.system('cls' if os.name == 'nt' else 'clear')

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

    def _menu_cliente_principal(self):
        """Menu que direciona o cliente para o login ou registro."""
        while True:
            self.limpar_ecra()
            print("--- MENU DO CLIENTE ---")
            print("1. Fazer Login")
            print("2. Criar Registo")
            print("3. Voltar")
            
            try:
                opcao = int(input("\nEscolha uma opção: "))
                
                if opcao == 1:
                    self._login_cliente()
                    if self.cliente_logado:
                        self._menu_compras_cliente()
                elif opcao == 2:
                    self._registar_cliente()
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
            id_func = int(input("ID: "))
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
            else:
                print("\nAcesso negado: Credenciais incorretas ou funcionário inexistente.")
                self.pausar()
        except ValueError:
            print("\nErro: O ID deve ser composto apenas por números.")
            self.pausar()

    def _login_cliente(self):
        """Valida a existência do CPF na lista de clientes carregados."""
        self.limpar_ecra()
        print("--- LOGIN ---")
        cpf = input("Digite o seu CPF: ").strip()
        
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                self.cliente_logado = cliente
                print("\nLogin efetuado com sucesso!")
                self.pausar()
                return
        
        print("\nCPF não encontrado no sistema.")
        self.pausar()

    def _registar_cliente(self):
        """Grava um novo cliente na memória e atualiza o ficheiro .txt."""
        self.limpar_ecra()
        print("--- NOVO REGISTRO :D ---")
        nome = input("Nome: ").strip()
        cpf = input("CPF: ").strip()
        
        for cliente in self.clientes: # verifica se o CPF já existe
            if cliente.cpf == cpf:
                print("\nErro: Este CPF já está registado.")
                self.pausar()
                return
            
        novo_cliente = Cliente(nome, cpf)
        self.clientes.append(novo_cliente)
        
        try:
            with open("data/clientes.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{cpf} {nome}")
            print("\nRegisto concluído!")
        except IOError:
            print("\nErro ao gravar o ficheiro de clientes.")
            
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
                    # self.caixa = Caixa(self.estoque)
                    # self.caixa.iniciar_atendimento(self.cliente_logado)
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
            with open("data/funcionarios.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    if linha.strip():
                        nome, id_func, senha, cargo = linha.split()
                        if cargo == "Gerente":
                            lista.append(Gerente(nome, int(id_func), senha))
                        elif cargo == "Operador":
                            lista.append(OperadorCaixa(nome, int(id_func), senha))
        except (FileNotFoundError, ValueError):
            print("Aviso: Falha ao carregar funcionários. Verifique o ficheiro txt.")
        return lista

    def _carregar_clientes(self) -> list:
        """Lê o arquivo e instancia a lista de clientes."""
        lista = []
        try:
            with open("data/clientes.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    if linha.strip():
                        cpf, nome = linha.split()
                        lista.append(Cliente(nome, cpf))
        except (FileNotFoundError, ValueError):
            print("Aviso: Falha ao carregar clientes. Verifique o arquivo txt.")
        return lista

if __name__ == "__main__":
    app = Sistema()
    app.iniciar()