from shared.utilities import normalizar_nome
from shared.excepcoes_shared import (
    CategoriaJaExiste, CategoriaNaoExiste, CategoriaComProdutos,
    ProdutoJaExiste, ProdutoNaoExiste, PrecoInvalido, QuantidadeInvalida,
    EmailJaExiste, ClienteNaoExiste, StockInsuficiente,
    ProdutoNaoNoCarrinho, CarrinhoVazio
)
from servidor.categoria import Categoria
from datetime import datetime

class Loja:

    def __init__(self):
        self._categorias = {}
        self._produtos={}
        self._clientes={}
        self._carrinhos={}
        self._encomendas={}

    def reset(self): 
        Categoria._contador_global = 1
        self._categorias.clear()
        self._produtos.clear()
        self._clientes.clear()
        self._carrinhos.clear()
        self._encomendas.clear()

    # -----------------------------
    # Categorias
    # -----------------------------
    def criar_categoria(self, nome):
        nome = normalizar_nome(nome)
        if self.obter_id_categoria(nome) is not None:
            raise CategoriaJaExiste(nome) 
        categoria = Categoria(nome)
        self._categorias[categoria.id_categoria] = categoria
        return categoria
    
    def obter_id_categoria(self, nome): 
        for c in self._categorias.values(): 
            if nome == c.nome: 
                return c.id_categoria
        return None

    def listar_categorias(self):
        return list(self._categorias.values())
    
    def remover_categoria(self, nome):
        nome = normalizar_nome(nome)
        categoria_id = self.obter_id_categoria(nome)
        if categoria_id is None:
            raise CategoriaNaoExiste(nome) 
        for p in self._produtos.values():
            if p["categoria"].id_categoria == categoria_id and p["quantidade"] > 0:
                raise CategoriaComProdutos(nome) 
        categoria = self._categorias.pop(categoria_id)
        return categoria

    # -----------------------------
    # Produtos
    # -----------------------------
    def criar_produto(self, nome_produto, nome_categoria, preco, quantidade):
        nome_categoria=normalizar_nome(nome_categoria)
        nome_produto=normalizar_nome(nome_produto)
        categoria_id = self.obter_id_categoria(nome_categoria)
        
        if preco <= 0:
            raise PrecoInvalido() 
        if quantidade < 0:
            raise QuantidadeInvalida() 
            
        for p in self._produtos.values():
            if p["nome"] == nome_produto:
                raise ProdutoJaExiste(nome_produto) 
                
        if categoria_id is None:
            raise CategoriaNaoExiste(nome_categoria) 
            
        categoria=self._categorias[categoria_id]
        produto = {
            "id_produto": len(self._produtos) + 1,
            "nome": nome_produto,
            "preco": round(float(preco), 2),
            "quantidade": quantidade,
            "categoria": categoria
        }
        self._produtos[produto["id_produto"]] = produto
        return produto

    def listar_produtos(self):
        return list(self._produtos.values())

    def aumenta_stock_produto(self, nome_produto, quantidade):
        nome_produto = normalizar_nome(nome_produto)
        if quantidade <= 0:
            raise QuantidadeInvalida() 

        for produto in self._produtos.values():
            if produto["nome"] == nome_produto:
                produto["quantidade"] += quantidade
                return produto
        raise ProdutoNaoExiste(nome_produto) 

    def atualiza_preco_produto(self, nome_produto, novo_preco):
        nome_produto = normalizar_nome(nome_produto)
        if novo_preco <= 0:
            raise PrecoInvalido() 

        for produto in self._produtos.values():
            if produto["nome"] == nome_produto:
                produto["preco"] = novo_preco
                return produto
        raise ProdutoNaoExiste(nome_produto) 

    #---------------------
    # CLientes
    #-----------------
    def criar_cliente(self, nome_cliente, email, password):
        nome_cliente=normalizar_nome(nome_cliente)
        email_normalizado=email.lower()
        for cliente in self._clientes.values():
            if cliente["email"] == email_normalizado:
                raise EmailJaExiste() 
        cliente={
            "id_cliente":len(self._clientes)+1,
            "nome":nome_cliente,
            "email":email_normalizado,
            "password":password
        }
        self._clientes[cliente["id_cliente"]]=cliente
        return cliente

    def listar_clientes(self):
        return list(self._clientes.values())
    
    #---------------------
    # Carrinho
    #-----------------
    def adiciona_produto_carrinho(self, id_cliente, nome_produto, quantidade):
        if id_cliente not in self._clientes:
            raise ClienteNaoExiste() 
            
        nome_produto = normalizar_nome(nome_produto)
        produto_encontrado = None
        for produto in self._produtos.values():
            if produto["nome"] == nome_produto:
                produto_encontrado = produto
                break

        if produto_encontrado is None:
            raise ProdutoNaoExiste(nome_produto) 

        if quantidade <= 0:
            raise QuantidadeInvalida() 
        if quantidade > produto_encontrado["quantidade"]:
            raise StockInsuficiente()
        
        if id_cliente not in self._carrinhos:
            self._carrinhos[id_cliente] = {}

        carrinho_cliente = self._carrinhos[id_cliente]

        if produto_encontrado["id_produto"] in carrinho_cliente:
            nova_quantidade = carrinho_cliente[produto_encontrado["id_produto"]] + quantidade
            if nova_quantidade > produto_encontrado["quantidade"]:
                raise StockInsuficiente() 
            carrinho_cliente[produto_encontrado["id_produto"]] = nova_quantidade
        else:
            carrinho_cliente[produto_encontrado["id_produto"]] = quantidade
            
        produto_encontrado["quantidade"] -= quantidade
        return produto_encontrado

    def remove_produto_carrinho(self, id_cliente, nome_produto):
        if id_cliente not in self._clientes:
            raise ClienteNaoExiste() 

        nome_produto = normalizar_nome(nome_produto)
        produto_encontrado = None
        for produto in self._produtos.values():
            if produto["nome"] == nome_produto:
                produto_encontrado = produto
                break
                
        if produto_encontrado is None:
            raise ProdutoNaoExiste(nome_produto) 

        if id_cliente not in self._carrinhos:
            raise ProdutoNaoNoCarrinho() 

        carrinho_cliente = self._carrinhos[id_cliente]

        if produto_encontrado["id_produto"] not in carrinho_cliente:
            raise ProdutoNaoNoCarrinho() 

        quantidade_no_carrinho = carrinho_cliente[produto_encontrado["id_produto"]]
        del carrinho_cliente[produto_encontrado["id_produto"]]
        produto_encontrado["quantidade"] += quantidade_no_carrinho

        return produto_encontrado

    def listar_carrinho(self, id_cliente):
        if id_cliente not in self._clientes:
            raise ClienteNaoExiste() 

        if id_cliente not in self._carrinhos or not self._carrinhos[id_cliente]:
            return []

        carrinho_cliente = self._carrinhos[id_cliente]
        resultado = []

        for id_produto, quantidade in carrinho_cliente.items():
            produto = self._produtos[id_produto]
            subtotal = produto["preco"] * quantidade

            resultado.append({
                "id": produto["id_produto"],
                "nome": produto["nome"],
                "categoria": produto["categoria"].nome,
                "preco": produto["preco"],
                "quantidade": quantidade,
                "subtotal": subtotal
            })

        return resultado

    def checkout_carrinho(self, id_cliente):
        if id_cliente not in self._clientes:
            raise ClienteNaoExiste()  

        if id_cliente not in self._carrinhos or not self._carrinhos[id_cliente]:
            raise CarrinhoVazio() 

        carrinho_cliente = self._carrinhos[id_cliente]
        total = 0
        itens_encomenda = []

        for id_produto, quantidade in carrinho_cliente.items():
            produto = self._produtos[id_produto]
            preco_atual = produto["preco"]  
            total += preco_atual * quantidade
            itens_encomenda.append({
                "id_produto": id_produto,
                "nome": produto["nome"],
                "preco": round(preco_atual, 2),
                "quantidade": quantidade
            })

        id_encomenda = len(self._encomendas) + 1

        encomenda = {
            "id_encomenda": id_encomenda,
            "id_cliente": id_cliente,
            "data": datetime.now(),
            "produtos": itens_encomenda,
            "total_preco": total
        }

        self._encomendas[id_encomenda] = encomenda
        self._carrinhos[id_cliente] = {}
        return encomenda

    #--------------------
    # Encomendas
    #--------------------
    def listar_encomendas(self, id_cliente):
        if id_cliente not in self._clientes:
            raise ClienteNaoExiste() 

        encomendas_cliente = [
            e for e in self._encomendas.values()
            if e["id_cliente"] == id_cliente
        ]

        return encomendas_cliente