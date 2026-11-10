# Sistema de Totem de Caixa de Supermercado

Este repositório contém os artefatos do sistema de Totem de Supermercado, um sistema de autoatendimento e também de caixa para facilitar a experiência do cliente e apoiar funcionários no gerenciamento de estoque e vendas utilizando Python. O foco principal é a aplicação prática de conceitos de Programação Orientada a Objetos (POO), como herança, polimorfismo, classes abstratas e encapsulamento, através de uma arquitetura modular.


## Funcionalidades

O sistema foi dividido em módulos de responsabilidade única para atender diferentes perfis de usuário:

**Controle de Acesso e Segurança**
- Cadastro e autenticação de Clientes por CPF.
- Autenticação de Funcionários (Gerentes e Operadores) com controle de privilégios e permissões por herança.

**Gestão de Estoque (Área Restrita)**
- Painel de controle exclusivo para a Gerência.
- Reposição de inventário com validação rigorosa de dados (produtos unitários vs. pesáveis).
- Visualização completa do catálogo de produtos.

**Autoatendimento (Área do Cliente)**
- Processamento interativo de vendas através do módulo de Caixa.
- Carrinho de compras com cálculo automático de valores.
- Registro de histórico de compras vinculado ao perfil do cliente.

**Persistência de Dados**
- Leitura e gravação de dados em arquivos `.txt` (estoque, clientes, funcionários) utilizando tratamento `utf-8-sig` para prevenção de erros de codificação.

## Estrutura do Projeto

A arquitetura do repositório foi organizada para separar a lógica de negócio dos dados e da documentação:

- `src/`: Diretório contendo as classes principais do sistema (`produtos.py`, `funcionario.py`, `estoque.py`, `caixa.py`, `sistema.py`).
- `data/`: Armazena os arquivos de texto (`.txt`) atuando como o banco de dados do sistema.
- `docs/`: Diretório destinado ao armazenamento do diagrama UML, modelos e o relatório final do projeto.
- `README.md`: Documentação estrutural e instruções de execução.

## Conceitos de POO Aplicados

Para a construção de um sistema robusto e seguro, foram implementados os seguintes pilares:
- Encapsulamento: proteção de atributos sensíveis (como listas de clientes e inventário) utilizando variáveis privadas (`__`) e acesso via métodos controlados/properties.
- Herança e Polimorfismo: especialização de classes base (ex: `Funcionario` gerando `Gerente` e `OperadorCaixa`; `Produto` gerando `ProdutoUnitario` e `ProdutoPesavel`) garantindo comportamentos específicos sem duplicação de código.
- Classes Abstratas: utilização do módulo `abc` para impedir a instanciação de entidades genéricas e forçar a implementação de métodos nas subclasses.
- Tratamento de Exceções: blocos `try/except` distribuídos de forma estratégica para capturar erros de digitação (ValueError) e falhas de leitura de arquivos (IOError/FileNotFoundError), impedindo a quebra do sistema.

Para executar o programa, é necessário ter o Python 3.x instalado na máquina e de um terminal com suporte a códigos ANSI para limpeza de tela dinâmica. Abaixo, segue o passo a passo para realizar a execução do projeto: 

1. Clone este repositório ou faça o download dos arquivos.
2. Abra o terminal e navegue até a raiz do projeto (a pasta que contém `src` e `data`).
3. Execute o comando abaixo para iniciar o sistema:

```bash
python3 src/sistema.py
``` 

## Integrantes do grupo

- Bárbara Stella Sena Barbosa
- Cecilia Scofield Carneiro 
- Larissa Rafaele Vieira Silva
- Pedro Azevedo Andrade

