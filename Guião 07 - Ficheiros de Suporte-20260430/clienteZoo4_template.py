from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError

# ligar ao ZooKeeper
zk = KazooClient(hosts="127.0.0.1:2181")
zk.start()
print("Ligado ao ZooKeeper")

def set(path, value):
    pass

def get(path):
    pass

def create(path, value): 
    pass
        
def get_rootchildren(): 
    pass

def delete(path): 
    pass

def main():
    try:
        while True:
            comando = input("Insira comando >")
            if comando.lower().startswith("ls"): 
                pass
            elif comando.lower().startswith("create"): 
                pass
            elif comando.lower().startswith("quit"): 
                break
        # fechar ligação
        print("Ligação fechada")
        zk.stop()
        zk.close()
            
    except KeyboardInterrupt:
        # fechar ligação
        print("Ligação fechada")
        zk.stop()
        zk.close()
        

if __name__ == "__main__":
    main()