import json
import socket
import sys
from kazoo.client import KazooClient

zk = KazooClient(hosts="127.0.0.1:2181")
zk.start()

if len(sys.argv) == 3:
    ip = sys.argv[1]
    port = int(sys.argv[2])
else:
    print("Uso: python3 <executavel.py> <ip> <porto>")

if not zk.exists("/servers"):
    zk.create("/servers", b"")

server_id = zk.create(
    f"/servers/server_",
    json.dumps({"host": ip, "port": port}).encode(),
    ephemeral=True,
    sequence=True
)

s = socket.socket()
s.bind((ip, port))
s.listen(5)

while True:
    conn, addr = s.accept()
    msg = conn.recv(1024).decode()
    print(server_id, "recebeu:", msg)
    conn.send(f"{server_id} respondeu".encode())
    conn.close()