# Sistema de Caixa de Supermercado

**Objetivo**
Este projeto implementa um sistema automatizado de gerenciamento de caixa de supermercado utilizando Python. O foco principal é a aplicação prática de conceitos de Programação Orientada a Objetos (POO), como herança, polimorfismo, classes abstratas e encapsulamento, através de uma arquitetura modular.

**Funcionalidades**
* **Gestão de Produtos:** Cadastro e diferenciação de itens (vendidos por unidade ou pesáveis) com cálculo dinâmico de preços.
* **Controle de Estoque:** Atualização automática de inventário após vendas, separação por categorias e tratamento de erros para estoque insuficiente.
* **Controle de Acesso:** Sistema de permissões diferenciado entre Gerentes (acesso a relatórios e alteração de preços) e Operadores de Caixa (registro de vendas).
* **Processamento de Vendas:** Operação de transações via caixa tradicional (funcionário) ou totem de autoatendimento (cliente), processando carrinho e formas de pagamento.
* **Persistência de Dados:** Armazenamento seguro de registros, estoque e dados de funcionários utilizando banco de dados local.

**Estrutura do Projeto**
O repositório abandona a divisão clássica de cabeçalhos e implementações para adotar a estrutura modular do Python:

* `src/`: Diretório com as classes principais do sistema (`produto.py`, `funcionario.py`, `estoque.py`, `caixa.py`, `sistema.py`).
* `data/`: Armazena o banco de dados SQLite ou arquivos `.txt` contendo o inventário e histórico.
* `tests/`: Scripts para testar o comportamento das classes de forma isolada.
* `main.py`: Ponto de entrada que inicializa as instâncias e roda a interface do sistema.
* `README.md`: Documentação estrutural e objetivos do projeto.

* 
