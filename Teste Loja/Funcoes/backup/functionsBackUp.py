import sqlite3
from getpass import getpass
import pwinput
from time import sleep

def teste():
    print("Estou recebendo sinal ") # testar chamadas 



# Cria a base de dados com a tabela se nao existir
def iniciaDB():
    with sqlite3.connect("agapeshop.db") as conn:  # tabela de produtos FALTA CRIAR AS OUTRAS TABELAS
        cursor = conn.cursor()
        

        #1 Tabela Usuario
        cursor.execute(''' CREATE TABLE IF NOT EXISTS usuario (
                       usuario_id INTEGER PRIMARY KEY AUTOINCREMENT ,
                       nome VARCHAR(100),
                       senha VARCHAR(50)) ''')
        print("Tabela usuario criada com suceso ")


        # 2 Categoria dos produtos
        cursor.execute(''' CREATE TABLE IF NOT EXISTS categoria (
                           categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome_categoria VARCHAR(100) )''')
        print("Tabela categoria Criada com Sucesso1 ")

        #3 TABELA DE PRODUTOS
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS produtos(
                    produto_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_produto TEXT,
                    descricao_produto VARCHAR(100),   
                    preco DECIMAL,
                    quantidade_estoque INTEGER,
                    categoria_id INTEGER,
                    FOREIGN KEY (categoria_id) REFERENCES categoria (categoria_id) )''')
        print("Tabela Produtos para Agape Shop Criada com Sucesso")
        

        #4 Tabela de  Fatura
        cursor.execute(''' CREATE TABLE IF NOT EXISTS fatura(
                       fatura_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       data_venda DATE,
                       total_venda DECIMAL,
                       usuario_id INTEGER,
                       pagamento_id INTEGER,
                       FOREIGN KEY (usuario_id) REFERENCES usuario (usuario_id),
                       FOREIGN KEY (pagamento_id) REFERENCES tipo_pagamento (pagamento_id) )''')
        print("Tabela Fatura Criada com sucesso ")


        #5 Tabela Itens da venda
        cursor.execute(''' CREATE TABLE IF NOT EXISTS item_venda (
                       item_venda_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       quantidade_venda INTEGER,
                       preco_unidade DECIMAL,
                       fatura_id INTEGER,
                       produto_id INTEGER,
                       FOREIGN KEY (fatura_id) REFERENCES fatura (fatura_id),
                       FOREIGN KEY (produto_id) REFERENCES produtos (produto_id) )''')
        print("Tabela Item venda criada com sucesso ")


        #6 Tipo de Pagamento 
        cursor.execute(''' CREATE TABLE IF NOT EXISTS tipo_pagamento (
                       pagamento_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       metodo_pagamento VARCHAR(50) )''')
        print("Tabela tipo de pagamento Criada com sucesso ")



        conn.commit()
        print("BASE DA DADOS CRAIADA COM SUCESSO ! ")





# Cabeçalho
def cabecalho():
    titulo = "AGAPE SHOP"
    tam = int(len(titulo)/2)+2
    print('--' * tam)
    print(f'  {titulo}  ')
    print('--' * tam)
    sleep(0.5)


# Cadastrar Usuario
def cadastro():
    while True:
        global user_id
        print(f"Deseja fazer Login ou Cadastro?")
        print("1. Login")
        print("2. Cadastro")
        print("3. Sair ")
        

        try:
            opcao = int(input("Escolha uma opção: "))

            if opcao == 1:
                print(" --- LOGIN --- ")
                nome = input("\nDigite o seu nome : ")
                #senha = input("Digite a sua password: ") sem o getpass
                senha = pwinput.pwinput("Digite a sua senha: ", mask="*") 
                print("\nA validar...\n")
                sleep(1)
                
                #conexao ao db e verificacao de user 
                with sqlite3.connect('agapeshop.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT usuario_id FROM usuario WHERE nome = ? AND senha = ?", (nome,senha))
                    user = cursor.fetchone()
                    

                    if user:  # Verifica se o usuário existe
                        user_id = user[0]
                        print("Login efetuado com sucesso!\n")
                        sleep(0.5)
                        break
                    else:
                        print("Nome de usuário ou senha incorretos. Você precisa se cadastrar primeiro.")
                        print("Você deseja se cadastrar? (s/n)")
                        if input().strip().lower() == 's':
                            continue

                
            elif opcao == 2:
                print(" --- CADASTRO --- ")  
                nome = input("Digite seu nome de usuario: ")
                senha = input("Digite sua senha: ")

                with sqlite3.connect('agapeshop.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO usuario (nome , senha) VALUES(?, ?)",(nome, senha))
                    conn.commit()
                    print(f"Usuario {nome} cadastrado com suceso! ")

                    return nome
                

            elif opcao == 3:
                print("Saindo... Até a próxima!")
                break

            else:
                print("Opção Inválida! Tente novamente.")

        

        except ValueError:
            print("Erro: Por favor, insira um número válido.")
    



# Menu para o usuário inserir produtos
def menu():
    while True:
        print("1. Inserir Produto")
        print("2. Alterar Produto")
        print("3. Mostrar produtos")
        print("4. Apagar  Produto")
        print("5. Sair\n")
        
        escolha = input("Escolha uma opção: \n").strip()


        if escolha == '1':
            categoria = input("Qual a Categoria do produto: \n").strip().title()
            insertCategoria(categoria)
            sleep(0.5)

            nome_produto = input("Nome do Produto: ").strip().title()
            descricao_produto = input("Descricao do produto: ").strip().title()
            preco = float(input("Preço do Produto: "))
            quantidade_estoque = int(input("Quantidade em Estoque: "))
            
            insert(nome_produto,descricao_produto, preco, quantidade_estoque )
            sleep(0.5)

        elif escolha == '2':
            update()
        elif escolha == '3':
            mostrarProdutos()
            print()
        elif escolha == '4':
            delete()
        elif escolha == '5':
            print("saindo da Agape Shop ...\n")
            break
        else:
            print("Opção inválida, tente novamente.\n")
    print()
   


# Insere uma categoria
def insertCategoria(categoria):
    try:
        with sqlite3.connect('agapeshop.db') as conn:
            cursor = conn.cursor()
            
            
            cursor.execute(''' INSERT INTO categoria (nome_categoria) VALUES (?)''',(categoria,))
            conn.commit() 

            print("Categoria inserida com sucesso \n")
    except sqlite3.Error as e:
        print(f"Erro ao inserir Categoria {e}")     
          
        

# Insere um novo produto
def insert(nome_produto,descricao_produto, preco, quantidade_estoque,):
    try:
        with sqlite3.connect('agapeshop.db') as conn:  
            cursor = conn.cursor()

            #inserir produto
            cursor.execute('''  
                INSERT INTO produtos(nome_produto,descricao_produto, preco, quantidade_estoque )
                VALUES (?, ?, ?, ?) 
            ''', (nome_produto, descricao_produto, preco, quantidade_estoque , ))
            conn.commit()

            print("Novo produto inserido com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inserir produto: {e}")



# Atualiza um produto
def update():
    try:
        with sqlite3.connect('agapeshop.db') as conn:
            cursor = conn.cursor()
            cursor.execute(''' SELECT * FROM produtos ''')
            produtos = cursor.fetchall()
            
            for produto in produtos:
                print(f'ID: {produto[0]} | NOME: {produto[1]} | PRECO: {produto[2]} | ESTOQUE: {produto[3]}')

            alteraProduto = input("Digite o nome do produto que deseja alterar: ").strip().title()
            novo_preco = float(input("Digite o novo preço: "))
            novo_stock = int(input("Digite o novo estoque: "))
            cursor.execute(''' 
                UPDATE produtos SET preco = ?, stock = ? WHERE nome = ?
            ''', (novo_preco, novo_stock, alteraProduto))
            conn.commit()
            print(f"Produto '{alteraProduto}' alterado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao alterar produto: {e}")



#Mostar produtos 

def mostrarProdutos():
    try:
        with sqlite3.connect('agapeshop.db') as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM produtos')
            produtos = cursor.fetchall()

            if not produtos:
                print("Nenhum produto encontrado .")
                return produtos
            
            for produto in produtos:
                print(f"Categoria:{produto[0]} \nNome: {produto[1]} \nPreco: {produto[3]} €  \nEstoque: {produto[4]}\n ")  #0Categoria 1Nome do produto,3preco do produto, 4 estoque do produto
            return produtos

    except sqlite3.Error as e:
        print(f"Erro ao mostrar produtos {e}")        




#funcao para deletar um produto
def delete():
    try:
        nome_produto = input("Digite o nome do produto que deseja deletar: ").strip().title()
       
        with sqlite3.connect('agapeshop.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produtos WHERE nome = ? ", (nome_produto,))

            produto = cursor.fetchone()

            if produto:
               cursor.execute(''' DELETE FROM produtos WHERE nome = ? ''',(nome_produto,))
               conn.commit()
               print(f"Produto {nome_produto} excluido com sucesso")
            else:
                print(f"Nenhum produto encontrado com o nome {nome_produto} .")

            

    except sqlite3.Erro as e:
        print(f"Erro ao deletar produto {e}")                    