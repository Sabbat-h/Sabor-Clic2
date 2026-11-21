# Sabor-Clic2

Sistema web de cardápio e gerenciamento de pedidos de sobremesas, desenvolvido com Python e Flask. O projeto reúne uma interface em tons de vermelho, rosa e branco com funcionalidades de compra, controle de estoque e acompanhamento de pedidos.

O sistema foi organizado seguindo o padrão MVC (Model–View–Controller) e utiliza SQLite para armazenar os dados.

Funcionalidades

Página inicial e cardápio digital de sobremesas, com pesquisa e filtros por categoria.
Cadastro de clientes e login por usuário ou e-mail.
Carrinho de compras que abre na lateral do cardápio ao clicar no ícone, com adição, remoção e alteração de quantidades.
Finalização de pedidos com registro no banco de dados e atualização do estoque.
Comprovante e detalhes do pedido realizado.
Histórico de pedidos e fila da cozinha para a equipe autorizada.
Atualização dos pedidos para os estados Aguardando, Em Preparo, Pronto, Entregue e Não entregue.
Cadastro, edição e exclusão de pratos pelo administrador.
Exportação de informações de pratos e pedidos para planilhas Excel (.xlsx). Observação: o projeto registra pedidos, mas não possui integração com um serviço de pagamento on-line.
Perfis de acesso: Funcionalidade Cliente Cozinheiro Administrador

Consultar o cardápio ✅ ✅ ✅ Criar conta pelo site ✅ — — Fazer pedido pelo carrinho ✅ — ✅ Visualizar o histórico geral de pedidos — ✅ ✅ Acessar a fila da cozinha — ✅ ✅ Atualizar o status e confirmar a entrega — ✅ ✅ Cadastrar, editar e excluir pratos — — ✅

O cadastro público cria apenas contas do tipo CLIENTE. As contas de COZINHEIRO e ADMIN são criadas localmente por meio do script criar_equipe.py, e as permissões são verificadas também nas rotas do servidor.

O cliente não tem acesso ao histórico geral, mas pode consultar o comprovante de um pedido próprio.

Tecnologias utilizadas

Python e Flask — aplicação web, rotas e autenticação por sessão.
HTML5, CSS3 e JavaScript — páginas, estilização e interação do carrinho.
Jinja2 — renderização dos templates.
SQLite — persistência de usuários, pratos e pedidos.
Werkzeug — geração e verificação de hashes de senhas.
OpenPyXL — exportação de planilhas .xlsx.
Estrutura do projeto Sabor-Clic2/ ├── app2/ │ ├── app.py # Inicialização da aplicação Flask │ ├── config.py # Configurações │ ├── database.py # Conexão e estrutura do SQLite │ ├── criar_equipe.py # Cadastro local de equipe autorizada │ ├── controllers/ # Rotas e regras de acesso │ ├── models/ # Consultas e operações de dados │ ├── templates/ # Páginas HTML com Jinja2 │ ├── static/ # CSS, JavaScript e imagens │ ├── tests/ # Arquivos de teste │ └── requirements.txt # Dependências do Python ├── DER_MER/ ├── img/ └── README.md Como executar no Windows Tenha o Python instalado (recomenda-se a versão 3.11 ou 3.12) e abra o PowerShell na pasta do repositório.

Entre na aplicação: cd app2

Crie e ative um ambiente virtual: py -m venv venv .\venv\Scripts\Activate.ps1 Se o PowerShell bloquear a ativação, use a permissão temporária para esta sessão e tente novamente: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass .\venv\Scripts\Activate.ps1

Instale as dependências: python -m pip install -r requirements.txt

Inicie a aplicação: python app.py

Abra no navegador: http://127.0.0.1:5000

As tabelas do SQLite são criadas na inicialização se ainda não existirem. Para parar o servidor, pressione Ctrl + C no PowerShell. Como cadastrar a equipe O formulário público é exclusivo para clientes. Para criar uma conta de cozinheiro ou administrador no banco de dados local, execute, na pasta app2: python criar_equipe.py Selecione COZINHEIRO ou ADMIN e informe os dados solicitados pelo programa. Não publique credenciais reais nem o banco SQLite no GitHub. Segurança e publicação Este projeto foi desenvolvido para execução local e fins de aprendizado. Antes de disponibilizá-lo na internet, é necessário rever as configurações de segurança: usar uma SECRET_KEY secreta e configurável, desativar o modo de depuração (debug=True), revisar proteção de formulários e configurar um servidor adequado para produção.

Ao publicar o código no GitHub, não inclua o ambiente virtual (venv/), bancos de dados (*.sqlite, *.db), arquivos .env, senhas ou arquivos temporários (pycache/). Os testes existentes também devem ser revisados para refletir as rotas atuais do Sabor & Clic. Sabor & Clic — Traga sabor à sua vida, apenas com um clic!


Site público: https://saboreclic.pythonanywhere.com/
