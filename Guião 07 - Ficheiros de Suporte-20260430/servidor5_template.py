import json
import socket
import sys
from kazoo.client import KazooClient

class ZooKeeperClient(): 
    
    def __init__(self): 
        pass
    
    def connect(self): 
        self.zk = KazooClient(hosts="127.0.0.1:2181")
        self.zk.start()

    def set(self, path, value):
        value = self.zk.set(path, value.encode())

    def get(self, path):
        value = self.zk.get(path)
        print(value[0].decode())

    def create(self, path, value):
        #TODO : criar no persistente
        pass
            
    def create_ephemeral(self, path, value): 
        #TODO: criar no efemero
        pass
            
    def close(self): 
        self.zk.stop()
        self.zk.close()
        
    def get_root(self): 
        children = self.zk.get_children("/")
        return children

    def delete(self, path):
        self.zk.delete(path, recursive = True)


def main(ip, porto): 
    zk_interface = ZooKeeperClient()
    zk_interface.connect()
    
    # TODO: create /servers e /server_0000000XXX efémero
    
    #TODO: CRIAR SOCKET DE ESCUTA

    #TODO: ACEITAR LIGACOES
        
if __name__ == "__main__": 
    if len(sys.argv) == 3:
        ip = sys.argv[1]
        port = int(sys.argv[2])
    else:
        print("Uso: python3 <executavel.py> <ip> <porto>")
        exit(1)
    main(ip, port)