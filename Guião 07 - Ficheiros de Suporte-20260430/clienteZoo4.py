from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError

# ligar ao ZooKeeper
zk = KazooClient(hosts="127.0.0.1:2181")
zk.start()
print("Ligado ao ZooKeeper")
# criar nó efémero
path = "/teste_ephemeral"
value = "127.0.0.1:4000"

try:
    created = zk.create(
        path,
        value.encode("utf-8"),
        ephemeral=True,
        makepath=True
    )
    print("Nó efémero criado:", created)
except NodeExistsError:
    print("O nó já existe.")

# listar raiz
children = zk.get_children("/")
print("Conteúdo de / :", children)

# fechar ligação
zk.stop()
zk.close()

print("Ligação fechada")
