import sys
import shlex
from shared.socket_utilities import PontoAcesso
from shared.excepcoes_shared import OpCodes
from cliente.rede import TCPSocketCliente
from cliente.stub import Stub

def traduzir_erro(op_code):
    """Função auxiliar para avisar o utilizador quando vem um erro do servidor"""
    print(f"SERVIDOR> A operação falhou. Código de erro devolvido: {op_code}")

def main():
    if len(sys.argv) != 2:
        print("CLIENTE> Uso: python -m cliente.main <porto>")
        sys.exit(1)

    try:
        ponto_acesso = PontoAcesso(endereco_ip='localhost', porto=int(sys.argv[1]))
    except Exception as e:
        print(f"CLIENTE> Erro de configuracao: {e}")
        sys.exit(1)

    # 1. Autenticação inicial conforme requisito da Fase 2
    print("=========================================")
    print("          BEM-VINDO AO MARKETCENTER      ")
    print("=========================================")
    try:
        id_perfil = int(input("CLIENTE> Introduza o seu Perfil (0:Anónimo, 1:Registado, 2:Funcionário, 3:Admin): "))
        id_utilizador = int(input("CLIENTE> Introduza o seu ID de Utilizador: "))
    except ValueError:
        print("CLIENTE> Valores inválidos. O programa vai terminar.")
        sys.exit(1)

    cliente_rede = TCPSocketCliente(ponto_acesso)

    try:
        # 2. Estabelecer ligação permanente
        cliente_rede.ligar()
        print("CLIENTE> Ligação ao servidor estabelecida com sucesso!")
        
        # 3. Inicializar o Stub com a ligação e as credenciais
        stub = Stub(cliente_rede, id_perfil, id_utilizador)

        while True:
            comando_bruto = input("\nCLIENTE> ").strip()
            
            if not comando_bruto:
                continue
                
            if comando_bruto.upper() in ["EXIT", "QUIT"]:
                break

            try:
                partes = shlex.split(comando_bruto)
            except ValueError:
                print("CLIENTE> Comando mal formatado (ex: aspas abertas).")
                continue

            comando = partes[0].upper()
            args = partes[1:]

            # 4. Traduzir o comando de texto numa chamada RPC do Stub
            try:
                # ---------------------------------------------
                # CATEGORIAS
                # ---------------------------------------------
                if comando == "CRIA_CATEGORIA":
                    op_code, retornos = stub.cria_categoria(args[0])
                    if op_code == OpCodes.OK_CRIA_CATEGORIA:
                        categoria = retornos[0]
                        print(f"SERVIDOR> Categoria {categoria.nome} criada com sucesso.")
                    else:
                        traduzir_erro(op_code)

                elif comando == "LISTA_CATEGORIAS":
                    op_code, retornos = stub.lista_categorias()
                    if op_code == OpCodes.OK_LISTA_CATEGORIAS:
                        categorias, produtos = retornos
                        print(f"SERVIDOR> Total Categorias: {len(categorias)}")
                        print(f"SERVIDOR> Total Produtos: {len(produtos)}")
                        for c in categorias:
                            count = sum(1 for p in produtos if p["categoria"].id_categoria == c.id_categoria)
                            print(f"{c.id_categoria} - {c.nome} ({count} produtos);")
                    else:
                        traduzir_erro(op_code)

                elif comando == "REMOVE_CATEGORIA":
                    op_code, retornos = stub.remove_categoria(args[0])
                    if op_code == OpCodes.OK_REMOVE_CATEGORIA:
                        print(f"SERVIDOR> Categoria {args[0]} removida com sucesso.")
                    else:
                        traduzir_erro(op_code)

                # ---------------------------------------------
                # PRODUTOS
                # ---------------------------------------------
                elif comando == "CRIA_PRODUTO":
                    op_code, retornos = stub.cria_produto(args[0], args[1], args[2], args[3])
                    if op_code == OpCodes.OK_CRIA_PRODUTO:
                        produto = retornos[0]
                        print(f"SERVIDOR> Produto {produto['nome']} criado com sucesso.")
                    else:
                        traduzir_erro(op_code)

                elif comando == "LISTA_PRODUTOS":
                    op_code, retornos = stub.lista_produtos()
                    if op_code == OpCodes.OK_LISTA_PRODUTOS:
                        categorias, produtos = retornos
                        total_qtd = sum(p['quantidade'] for p in produtos)
                        print(f"SERVIDOR> Total Produtos: {len(produtos)}")
                        print(f"SERVIDOR> Total Quantidade: {total_qtd}")
                        for p in produtos:
                            print(f"{p['id_produto']} - {p['nome']} ({p['categoria'].nome}, {p['preco']:.2f} euros, {p['quantidade']} unidades);")
                    else:
                        traduzir_erro(op_code)

                elif comando == "AUMENTA_STOCK_PRODUTO":
                    op_code, retornos = stub.aumenta_stock(args[0], args[1])
                    if op_code == OpCodes.OK_AUMENTA_STOCK:
                        produto = retornos[0]
                        print(f"SERVIDOR> Stock do produto {produto['nome']} aumentado em {args[1]} unidades com sucesso.")
                    else:
                        traduzir_erro(op_code)

                elif comando == "ATUALIZA_PRECO_PRODUTO":
                    op_code, retornos = stub.atualiza_preco(args[0], args[1])
                    if op_code == OpCodes.OK_ATUALIZA_PRECO:
                        produto = retornos[0]
                        print(f"SERVIDOR> O preço do produto {produto['nome']} foi atualizado para {produto['preco']:.2f} com sucesso.")
                    else:
                        traduzir_erro(op_code)

                # ---------------------------------------------
                # CLIENTES
                # ---------------------------------------------
                elif comando == "CRIA_CLIENTE":
                    op_code, retornos = stub.cria_cliente(args[0], args[1], args[2])
                    if op_code == OpCodes.OK_CRIA_CLIENTE:
                        cliente = retornos[0]
                        print(f"SERVIDOR> Cliente criado com sucesso com identificador único {cliente['id_cliente']}.")
                    else:
                        traduzir_erro(op_code)

                elif comando == "LISTA_CLIENTES":
                    op_code, retornos = stub.lista_clientes()
                    if op_code == OpCodes.OK_LISTA_CLIENTES:
                        clientes = retornos[0]
                        print(f"SERVIDOR> Total Clientes: {len(clientes)}")
                        for c in clientes:
                            print(f"{c['id_cliente']} - {c['nome']} ({c['email']});")
                    else:
                        traduzir_erro(op_code)

                # ---------------------------------------------
                # CARRINHO DE COMPRAS
                # ---------------------------------------------
                elif comando == "ADICIONA_PRODUTO_CARRINHO":
                    op_code, retornos = stub.adiciona_produto_carrinho(args[0], args[1])
                    if op_code == OpCodes.OK_ADICIONA_CARRINHO:
                        produto = retornos[0]
                        print(f"SERVIDOR> Produto {produto['nome']} adicionado com sucesso ao carrinho.")
                    else:
                        traduzir_erro(op_code)

                elif comando == "REMOVE_PRODUTO_CARRINHO":
                    op_code, retornos = stub.remove_produto_carrinho(args[0])
                    if op_code == OpCodes.OK_REMOVE_CARRINHO:
                        produto = retornos[0]
                        print(f"SERVIDOR> Produto {produto['nome']} removido com sucesso do carrinho de compras.")
                    else:
                        traduzir_erro(op_code)

                elif comando == "LISTA_CARRINHO":
                    op_code, retornos = stub.lista_carrinho()
                    if op_code == OpCodes.OK_LISTA_CARRINHO:
                        categorias, carrinho = retornos
                        if not carrinho:
                            print("SERVIDOR> Carrinho vazio.")
                        else:
                            total_produtos = len(carrinho)
                            total_qtd = sum(item["quantidade"] for item in carrinho)
                            total_preco = sum(item["subtotal"] for item in carrinho)
                            
                            print(f"SERVIDOR> Total Produtos: {total_produtos}")
                            print(f"SERVIDOR> Total Quantidade: {total_qtd}")
                            print(f"SERVIDOR> Total Preço: {total_preco:.2f} euros")
                            for item in carrinho:
                                print(f"{item['id']} - {item['nome']} ({item['categoria']}, {item['preco']:.2f} euros, {item['quantidade']} unidades);")
                    else:
                        traduzir_erro(op_code)

                elif comando == "CHECKOUT_CARRINHO":
                    op_code, retornos = stub.checkout_carrinho()
                    if op_code == OpCodes.OK_CHECKOUT:
                        print("SERVIDOR> Checkout de carrinho de compras efetuado com sucesso. Encomenda criada com sucesso a partir do carrinho.")
                    else:
                        traduzir_erro(op_code)

                # ---------------------------------------------
                # ENCOMENDAS
                # ---------------------------------------------
                elif comando == "LISTA_ENCOMENDAS":
                    op_code, retornos = stub.lista_encomendas(args[0])
                    if op_code == OpCodes.OK_LISTA_ENCOMENDAS:
                        encomendas, _ = retornos

                        if not encomendas:
                            print("SERVIDOR> Sem encomendas.")
                        else:
                            print(f"SERVIDOR> Total Encomendas: {len(encomendas)}")

                            for enc in encomendas:
                                print(f"ID Encomenda: {enc['id_encomenda']}")
                                print(f"Data: {enc['data'].strftime('%Y-%m-%d %H:%M:%S')}")
                                print(f"Total: {enc['total_preco']:.2f} euros")

                                for item in enc['produtos']:
                                    print(f"  -> {item['nome']} ({item['quantidade']} unidades, {item['preco']:.2f} euros/unidade)")
                    else:
                        traduzir_erro(op_code)

                else:
                    print(f"CLIENTE> Comando '{comando}' não reconhecido.")

            except IndexError:
                print("CLIENTE> Faltam argumentos para executar esse comando.")
            except ValueError:
                print("CLIENTE> Tipos de argumentos inválidos.")
            except Exception as e:
                print(f"CLIENTE> Erro ao executar pedido localmente: {e}")

    except Exception as e:
        print(f"CLIENTE> Falha na ligação ao servidor: {e}")
    finally:
        cliente_rede.fechar()
        print("CLIENTE> Ligação terminada.")

if __name__ == "__main__":
    main()