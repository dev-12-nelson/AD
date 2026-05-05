from shared.excepcoes_shared import OpCodes, ExcepcaoBase, NumeroArgumentosInvalido
from servidor.loja import Loja

class Skeleton:
    """
    Camada Processador (Skeleton / Dispatcher):
    - Recebe a lista RPC: [op_code, [args], id_perfil, id_utilizador]
    - Valida o formato base do protocolo
    - Valida autorizações de perfil
    - Encaminha para o método certo (handler)
    - Devolve SEMPRE uma lista: [op_code_resposta, [lista_de_retornos]]
    """

    def __init__(self):
        self.loja = Loja()
        
        
        self.HANDLERS = {
            OpCodes.CRIA_CATEGORIA: self._cmd_cria_categoria,
            OpCodes.LISTA_CATEGORIAS: self._cmd_lista_categorias,
            OpCodes.REMOVE_CATEGORIA: self._cmd_remove_categoria,
            
            OpCodes.CRIA_PRODUTO: self._cmd_cria_produto,
            OpCodes.LISTA_PRODUTOS: self._cmd_lista_produtos,
            OpCodes.AUMENTA_STOCK: self._cmd_aumenta_stock,
            OpCodes.ATUALIZA_PRECO: self._cmd_atualiza_preco,
            
            OpCodes.CRIA_CLIENTE: self._cmd_cria_cliente,
            OpCodes.LISTA_CLIENTES: self._cmd_lista_clientes,
            
            OpCodes.ADICIONA_PRODUTO_CARRINHO: self._cmd_adiciona_carrinho,
            OpCodes.REMOVE_PRODUTO_CARRINHO: self._cmd_remove_carrinho,
            OpCodes.LISTA_CARRINHO: self._cmd_lista_carrinho,
            OpCodes.CHECKOUT_CARRINHO: self._cmd_checkout_carrinho,
            
            OpCodes.LISTA_ENCOMENDAS: self._cmd_lista_encomendas,
        }

        
        self.PERMISSOES = {
            OpCodes.CRIA_CATEGORIA: [3],
            OpCodes.LISTA_CATEGORIAS: [0, 1, 2, 3],
            OpCodes.REMOVE_CATEGORIA: [3],
            
            OpCodes.CRIA_PRODUTO: [2, 3],
            OpCodes.LISTA_PRODUTOS: [0, 1, 2, 3],
            OpCodes.AUMENTA_STOCK: [2, 3],
            OpCodes.ATUALIZA_PRECO: [2, 3],
            
            OpCodes.CRIA_CLIENTE: [0],
            OpCodes.LISTA_CLIENTES: [2, 3],
            
            OpCodes.ADICIONA_PRODUTO_CARRINHO: [1],
            OpCodes.REMOVE_PRODUTO_CARRINHO: [1],
            OpCodes.LISTA_CARRINHO: [1],
            OpCodes.CHECKOUT_CARRINHO: [1],
            
            OpCodes.LISTA_ENCOMENDAS: [1, 2, 3],
        }

    def reset(self): 
        self.loja.reset()

    def processar_comando(self, pedido):
        """Ponto de entrada único chamado pelo main_loja.py"""
        try:
            
            if not isinstance(pedido, list):
                return [39903, []] 
                
            if len(pedido) != 4:
                return [39904, []] 
                
            op_code, args, id_perfil, id_utilizador = pedido
            
            if not isinstance(args, list):
                return [39905, []]
                
            if op_code not in self.HANDLERS:
                return [OpCodes.OP_CODE_INVALIDO, []]

            perfis_permitidos = self.PERMISSOES.get(op_code, [])
            if id_perfil not in perfis_permitidos:
                return [OpCodes.OPERACAO_NAO_AUTORIZADA, []]
        
            if not isinstance(id_perfil, int) or id_perfil not in [0,1,2,3]:
                return [39906, []]

            
            if not isinstance(id_utilizador, int) or id_utilizador < 0:
                return [39907, []]
            
            handler = self.HANDLERS[op_code]            
            op_code_resposta, retornos = handler(args, id_perfil, id_utilizador)
            
            return [op_code_resposta, retornos]

        except ExcepcaoBase as e:
            return [e.code, []]
            
        except Exception as e:
            print(f"SERVIDOR> Erro Crítico Interno: {e}")
            return [OpCodes.ERRO_INTERNO_SERVIDOR, []]

    # HANDLERS 
    def _validar_n_args(self, args, esperado):
        if len(args) != esperado:
            raise NumeroArgumentosInvalido(esperado, len(args))

    def _cmd_cria_categoria(self, args, id_perfil, id_utilizador):
        self._validar_n_args(args, 1)
        categoria = self.loja.criar_categoria(args[0])
        return OpCodes.OK_CRIA_CATEGORIA, [categoria]

    def _cmd_lista_categorias(self, args, id_perfil, id_utilizador):
            self._validar_n_args(args, 0)
            categorias = self.loja.listar_categorias()
            return OpCodes.OK_LISTA_CATEGORIAS, [categorias]

    def _cmd_remove_categoria(self, args, id_perfil, id_utilizador):
        self._validar_n_args(args, 1)
        self.loja.remover_categoria(args[0])
        return OpCodes.OK_REMOVE_CATEGORIA, []

    def _cmd_cria_produto(self, args, id_perfil, id_utilizador):
        self._validar_n_args(args, 4)
        produto = self.loja.criar_produto(args[0], args[1], float(args[2]), int(args[3]))
        return OpCodes.OK_CRIA_PRODUTO, [produto]

    def _cmd_lista_produtos(self, args, id_perfil, id_utilizador):
            self._validar_n_args(args, 0)
            produtos = self.loja.listar_produtos()
            return OpCodes.OK_LISTA_PRODUTOS, [produtos]

    def _cmd_aumenta_stock(self, args, id_perfil, id_utilizador):
        self._validar_n_args(args, 2)
        produto = self.loja.aumenta_stock_produto(args[0], int(args[1]))
        return OpCodes.OK_AUMENTA_STOCK, [produto]

    def _cmd_atualiza_preco(self, args, id_perfil, id_utilizador):
        self._validar_n_args(args, 2)
        produto = self.loja.atualiza_preco_produto(args[0], float(args[1]))
        return OpCodes.OK_ATUALIZA_PRECO, [produto]

    def _cmd_cria_cliente(self, args, id_perfil, id_utilizador):
        self._validar_n_args(args, 3)
        cliente = self.loja.criar_cliente(args[0], args[1], args[2])
        return OpCodes.OK_CRIA_CLIENTE, [cliente]

    def _cmd_lista_clientes(self, args, id_perfil, id_utilizador):
        self._validar_n_args(args, 0)
        clientes = self.loja.listar_clientes()
        return OpCodes.OK_LISTA_CLIENTES, [clientes]

    def _cmd_adiciona_carrinho(self, args, id_perfil, id_utilizador):

        self._validar_n_args(args, 2)
        produto = self.loja.adiciona_produto_carrinho(id_utilizador, args[0], int(args[1]))
        return OpCodes.OK_ADICIONA_CARRINHO, [produto]

    def _cmd_remove_carrinho(self, args, id_perfil, id_utilizador):
        self._validar_n_args(args, 1)
        produto = self.loja.remove_produto_carrinho(id_utilizador, args[0])
        return OpCodes.OK_REMOVE_CARRINHO, [produto]

    def _cmd_lista_carrinho(self, args, id_perfil, id_utilizador):
            self._validar_n_args(args, 0)
            carrinho = self.loja.listar_carrinho(id_utilizador)
            return OpCodes.OK_LISTA_CARRINHO, [carrinho]

    def _cmd_checkout_carrinho(self, args, id_perfil, id_utilizador):
        self._validar_n_args(args, 0)
        encomenda = self.loja.checkout_carrinho(id_utilizador)
        return OpCodes.OK_CHECKOUT, [encomenda]

    def _cmd_lista_encomendas(self, args, id_perfil, id_utilizador):
            self._validar_n_args(args, 1)
            id_alvo = int(args[0])
            encomendas = self.loja.listar_encomendas(id_alvo)
            return OpCodes.OK_LISTA_ENCOMENDAS, [encomendas]