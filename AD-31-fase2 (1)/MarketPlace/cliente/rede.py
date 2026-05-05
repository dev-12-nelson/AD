import socket
import struct
import pickle

class TCPSocketCliente:
    def __init__(self, ponto_acesso):
        self.ponto_acesso = ponto_acesso
        self.sock = None

    def ligar(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ponto_acesso.endereco_ip, self.ponto_acesso.porto))

    def _receive_all(self, sock, tamanho_esperado):
        """Mesma lógica do servidor, aplicada à rede do cliente."""
        buffer = bytearray()
        while len(buffer) < tamanho_esperado:
            pacote = sock.recv(tamanho_esperado - len(buffer))
            if not pacote:
                return None
            buffer.extend(pacote)
        return bytes(buffer)

    def receber(self):
        try:
            tamanho_bytes = self._receive_all(self.sock, 4)
            if not tamanho_bytes:
                return None
            tamanho = struct.unpack('i', tamanho_bytes)[0]
            
            dados_bytes = self._receive_all(self.sock, tamanho)
            if not dados_bytes:
                return None
                
            return pickle.loads(dados_bytes)
        except Exception as e:
            print(f"REDE> Erro ao receber dados do servidor: {e}")
            return None

    def enviar(self, dados):
        try:
            dados_bytes = pickle.dumps(dados)
            cabecalho = struct.pack('i', len(dados_bytes))
            self.sock.sendall(cabecalho + dados_bytes)
        except Exception as e:
            print(f"REDE> Erro ao enviar dados ao servidor: {e}")

    def fechar(self):
        if self.sock:
            self.sock.close()