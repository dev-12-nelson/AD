import socket
import struct
import pickle

class TCPSocketServidor:
    def __init__(self, ponto_acesso):
        self.ponto_acesso = ponto_acesso
        self.sock = None

    def criar_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self):
        self.sock.bind((self.ponto_acesso.endereco_ip, self.ponto_acesso.porto))

    def listen(self, backlog=5):
        self.sock.listen(backlog)

    def accept(self):
        return self.sock.accept()

    def _receive_all(self, sock, tamanho_esperado):
        buffer = bytearray()
        while len(buffer) < tamanho_esperado:
            
            pacote = sock.recv(tamanho_esperado - len(buffer))
            if not pacote:
                return None 
            buffer.extend(pacote)
        return bytes(buffer)

    def receber(self, socket_cliente):
        try:
            
            tamanho_bytes = self._receive_all(socket_cliente, 4)
            if not tamanho_bytes:
                return None
                
           
            tamanho = struct.unpack('i', tamanho_bytes)[0]
            
            
            dados_bytes = self._receive_all(socket_cliente, tamanho)
            if not dados_bytes:
                return None
                

            return pickle.loads(dados_bytes)
            
        except Exception as e:
            print(f"REDE> Erro ao receber dados: {e}")
            return None

    def enviar(self, socket_cliente, dados):
        try:
           
            dados_bytes = pickle.dumps(dados)

            cabecalho = struct.pack('i', len(dados_bytes))
            socket_cliente.sendall(cabecalho + dados_bytes)
        except Exception as e:
            print(f"REDE> Erro ao enviar dados: {e}")

    def fechar_cliente(self, socket_cliente):
        try:
            socket_cliente.close()
        except:
            pass

    def fechar_servidor(self):
        if self.sock:
            self.sock.close()