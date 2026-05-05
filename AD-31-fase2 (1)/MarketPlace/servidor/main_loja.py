import sys
import select
from servidor.skeleton import Skeleton
from servidor.rede_loja import TCPSocketServidor
from shared.excepcoes_shared import ExcepcaoConfiguracaoInvalida
from shared.socket_utilities import PontoAcesso

def main():
    if len(sys.argv) != 2:
        print("SERVIDOR> Uso: python -m servidor.main_loja <porto>")
        sys.exit(1)

    skeleton = Skeleton()
    try:
        ponto_acesso = PontoAcesso(endereco_ip='localhost', porto=int(sys.argv[1]))
        print("SERVIDOR> Configuração do servidor válida.")
    except ExcepcaoConfiguracaoInvalida as e:
        print("SERVIDOR>", e)
        sys.exit(1)

    servidor = TCPSocketServidor(ponto_acesso)

    try:
        servidor.criar_socket()
        servidor.bind()
        servidor.listen()
        print(f"SERVIDOR> A ouvir no porto {ponto_acesso.porto}...")

        sockets_monitorizados = [servidor.sock, sys.stdin]

        em_execucao = True

        while em_execucao:
            
            ready_to_read, _, _ = select.select(sockets_monitorizados, [], [])

            for s in ready_to_read:
                if s is servidor.sock:
                    conn_sock, addr = servidor.accept()
                   
                    sockets_monitorizados.append(conn_sock)

                
                elif s is sys.stdin:
                    comando_consola = sys.stdin.readline().strip().lower()
                    if comando_consola in ['exit', 'quit']:
                        print("SERVIDOR> A encerrar o servidor ")
                        em_execucao = False
                        break

                
                else:
                    try:
                        
                        pedido = servidor.receber(s)


                        if not pedido:
                            print("SERVIDOR> Cliente desligou-se.")
                            sockets_monitorizados.remove(s)
                            servidor.fechar_cliente(s)
                        else:
                            print(f"SERVIDOR> Recebido: {pedido}")
                            
                            resposta = skeleton.processar_comando(pedido)
                            
                            servidor.enviar(s, resposta)

                    except Exception as e:
                        print(f"SERVIDOR> Erro na ligação com cliente: {e}")
                        sockets_monitorizados.remove(s)
                        servidor.fechar_cliente(s)

    except Exception as e:
        print(f"SERVIDOR> Erro fatal: {e}")

    finally:
        print("SERVIDOR> A fechar as ligações...")
        for s in sockets_monitorizados:
            if s is not sys.stdin and s is not servidor.sock:
                servidor.fechar_cliente(s)
        servidor.fechar_servidor()
        print("SERVIDOR> Terminado.")

if __name__ == "__main__":
    main()