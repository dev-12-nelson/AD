import json
import socket
import sys
from kazoo.client import KazooClient

class ZooKeeperClient(): 
    
    def __init__(self): 
        pass
    
    def connect(self): 
        pass

    def set(self, path, value):
        pass

    def get(self, path):
        pass
            
    def close(self): 
        pass
        
    def get_root(self): 
        pass
        
    def get_tail(self, path): 
        pass
    
    def get_head(self, path): 
        pass
  
  
def main():
    zkCli = ZooKeeperClient()
    zkCli.connect()
    
    data = zkCli.get_head("/servers")
    info = json.loads(data.decode())
   
    s = socket.socket()
    s.connect((info["host"], info["port"]))
    s.send(b"ola")
    print(s.recv(1024).decode())
    s.close()

if __name__ == "__main__":
    main()
    
       

