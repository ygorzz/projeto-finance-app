# FinanceApp

![Python](https://img.shields.io/badge/python-3.x-blue)
![Flask](https://img.shields.io/badge/flask-web%20framework-black)
![SQLite](https://img.shields.io/badge/sqlite-database-003B57)
![Bootstrap](https://img.shields.io/badge/bootstrap-5-purple)
![Chart.js](https://img.shields.io/badge/chart.js-dashboard-orange)
![License](https://img.shields.io/badge/license-MIT-informational)

## Descrição

O **FinanceApp** é uma aplicação web completa para controle financeiro pessoal, desenvolvida como projeto de conclusão do curso **CS50: Introduction to Computer Science** da Universidade de Harvard.

A aplicação foi criada com o objetivo de oferecer uma interface intuitiva para gerenciamento financeiro, permitindo que usuários acompanhem orçamentos, categorias, entradas, saídas e histórico de transações de forma organizada.

O projeto integra front-end e back-end em uma aplicação full stack, utilizando Flask no servidor, SQLite para persistência de dados e JavaScript para interatividade dinâmica da interface.

---

## Tecnologias utilizadas

| Tecnologia | Versão | Função |
|---|---|---|
| [Python](https://www.python.org/) | 3.x | Linguagem principal da aplicação |
| [Flask](https://flask.palletsprojects.com/) | — | Framework web back-end |
| [SQLite](https://www.sqlite.org/) | — | Banco de dados relacional |
| [Bootstrap 5](https://getbootstrap.com/) | 5.x | Estilização e responsividade |
| JavaScript (ES6+) | — | Interatividade e lógica client-side |
| [Chart.js](https://www.chartjs.org/) | — | Criação de gráficos dinâmicos |
| HTML5 | — | Estruturação das páginas |
| CSS3 | — | Estilização personalizada |

A aplicação utiliza integração completa entre front-end e back-end através do Flask e manipulação dinâmica de dados utilizando JavaScript.

---

## Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Autenticação | Sistema de login e registro de usuários |
| Gestão de Categorias | Criação e personalização de categorias financeiras |
| Orçamentos | Definição de limites financeiros por categoria |
| Fluxo de Caixa | Registro de entradas e saídas |
| Histórico de Transações | Visualização detalhada das movimentações |
| Dashboard Dinâmico | Resumo visual utilizando gráficos interativos |

### Sistema de autenticação

Permite criação de contas e autenticação de usuários para gerenciamento individualizado das informações financeiras.

### Gestão financeira

Os usuários podem cadastrar receitas e despesas, organizando os dados em categorias personalizadas.

### Dashboard interativo

A aplicação apresenta gráficos dinâmicos para acompanhamento visual da saúde financeira utilizando o Chart.js.

---

## Funcionalidades e diferenciais

- **Aplicação Full Stack** — Integração completa entre front-end, back-end e banco de dados.
- **Arquitetura Flask** — Estruturação da aplicação utilizando rotas, templates e lógica separada.
- **Persistência de dados** — Utilização do SQLite para armazenamento das informações financeiras.
- **Dashboard dinâmico** — Gráficos interativos construídos com Chart.js.
- **Interface responsiva** — Layout adaptável utilizando Bootstrap 5.
- **Interatividade com JavaScript** — Manipulação do DOM, eventos e requisições assíncronas.
- **Sistema de autenticação** — Login e registro de usuários.
- **Organização financeira** — Controle de categorias, orçamentos e transações.
- **Projeto acadêmico completo** — Desenvolvido como projeto final do CS50 Harvard.
- **Integração front-end e back-end** — Comunicação dinâmica entre interface e servidor Flask.

---

## Como executar o projeto

### Pré-requisitos

- [Python](https://www.python.org/) 3.x
- `pip` instalado

### Passo a passo

**1. Clone o repositório e acesse a pasta do projeto:**

```bash
git clone <url-do-repositorio>
cd projeto-finance-app
```

---

**2. Crie um ambiente virtual:**

```bash
python -m venv venv
```

---

**3. Ative o ambiente virtual:**

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

**4. Instale as dependências:**

```bash
pip install -r requirements.txt
```

---

**5. Execute a aplicação:**

```bash
flask run
```

O servidor será iniciado localmente e poderá ser acessado pelo navegador.

---

## Observações

- O projeto foi desenvolvido como trabalho final do curso CS50 de Harvard.
- A aplicação integra conceitos de desenvolvimento full stack.
- O banco de dados SQLite é utilizado para persistência local dos dados.
- O projeto utiliza JavaScript moderno para interatividade dinâmica da interface.
- O dashboard financeiro é construído utilizando gráficos com Chart.js.
- Futuramente o projeto poderá receber refatorações, melhorias estruturais e novas funcionalidades.

---

## Licença

Este projeto está sob a licença [MIT](https://opensource.org/licenses/MIT).

---

*Desenvolvido por **Ygor Santos** — [LinkedIn](https://www.linkedin.com/in/ygor-santos-869152325/) | [GitHub](https://github.com/ygorzz)*
