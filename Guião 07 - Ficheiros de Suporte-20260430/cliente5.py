import json
import socket
import sys
from kazoo.client import KazooClient

zk = KazooClient(hosts="127.0.0.1:2181")
zk.start()

children = zk.get_children("/servers")

# Ordena lexicograficamente (funciona por causa dos zeros à esquerda)
sorted_nodes = sorted(children)

# Maior = último da lista
max_node = sorted_nodes[-1]

# ir buscar os dados ao ZooKeeper
data, _ = zk.get(f"/servers/{max_node}")

# converter bytes → dict
info = json.loads(data.decode())

s = socket.socket()
s.connect((info["host"], info["port"]))
s.send(b"ola")
print(s.recv(1024).decode())
s.close()
