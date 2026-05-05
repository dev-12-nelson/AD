import sys, socket as s

HOST = 'localhost'
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = 9999

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
list = []

while True:
    (conn_sock, addr) = sock.accept()
    try:
        tmp = conn_sock.recv(1024)
        msg = tmp.decode()
        resp = 'Ack'
        if msg == 'LIST':
            resp = str(list)
        elif msg == 'CLEAR':
            list = []
            resp = 'Lista apagada'
        else:
            list.append(msg)
        
        conn_sock.sendall(resp.encode())
        print ('list= %s' % list)
        conn_sock.close()
    except:
        print ('socket fechado!')
        conn_sock.close()
        sock.close()