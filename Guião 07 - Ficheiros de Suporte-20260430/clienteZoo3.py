# Cliente Zookeeper #

from kazoo.client import KazooClient

zk = KazooClient(hosts='127.0.0.1:2181') #porto default do Zookeeper
zk.start()

if not zk.exists("/servers_2526"):
    zk.create("/servers_2526")

if not zk.exists("/servers_2526/server_1"):
    zk.create("/servers_2526/server_1")

try:
    while True:
        pass
except KeyboardInterrupt:
    zk.stop()
