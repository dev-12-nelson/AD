from shared.excepcoes_shared import OpCodes

class Stub:

    
    def __init__(self, rede, id_perfil, id_utilizador):
        self.rede = rede
 
        self.id_perfil = id_perfil
        self.id_utilizador = id_utilizador

    def _fazer_chamada_rpc(self, op_code, argumentos):

        pedido = [op_code, argumentos, self.id_perfil, self.id_utilizador]
        

        self.rede.enviar(pedido)
        
       
        resposta = self.rede.receber()
        return resposta


    # Funções RPC 

    
    def cria_categoria(self, nome):
        return self._fazer_chamada_rpc(OpCodes.CRIA_CATEGORIA, [nome])

    def lista_categorias(self):
        return self._fazer_chamada_rpc(OpCodes.LISTA_CATEGORIAS, [])

    def remove_categoria(self, nome):
        return self._fazer_chamada_rpc(OpCodes.REMOVE_CATEGORIA, [nome])

    def cria_produto(self, nome_produto, nome_categoria, preco, quantidade):
        return self._fazer_chamada_rpc(OpCodes.CRIA_PRODUTO, [nome_produto, nome_categoria, float(preco), int(quantidade)])

    def lista_produtos(self):
        return self._fazer_chamada_rpc(OpCodes.LISTA_PRODUTOS, [])

    def aumenta_stock(self, nome_produto, quantidade):
        return self._fazer_chamada_rpc(OpCodes.AUMENTA_STOCK, [nome_produto, int(quantidade)])

    def atualiza_preco(self, nome_produto, novo_preco):
        return self._fazer_chamada_rpc(OpCodes.ATUALIZA_PRECO, [nome_produto, float(novo_preco)])

    def cria_cliente(self, nome, email, password):
        return self._fazer_chamada_rpc(OpCodes.CRIA_CLIENTE, [nome, email, password])

    def lista_clientes(self):
        return self._fazer_chamada_rpc(OpCodes.LISTA_CLIENTES, [])

    def adiciona_produto_carrinho(self, nome_produto, quantidade):
        return self._fazer_chamada_rpc(OpCodes.ADICIONA_PRODUTO_CARRINHO, [nome_produto, int(quantidade)])

    def remove_produto_carrinho(self, nome_produto):
        return self._fazer_chamada_rpc(OpCodes.REMOVE_PRODUTO_CARRINHO, [nome_produto])

    def lista_carrinho(self):
        return self._fazer_chamada_rpc(OpCodes.LISTA_CARRINHO, [])

    def checkout_carrinho(self):
        return self._fazer_chamada_rpc(OpCodes.CHECKOUT_CARRINHO, [])

    def lista_encomendas(self, id_cliente_alvo):
        
        return self._fazer_chamada_rpc(OpCodes.LISTA_ENCOMENDAS, [int(id_cliente_alvo)])