import http.client
ligacao = http.client.HTTPConnection("localhost", 8888)
corpo = "teste"
ligacao.request("GET", "/caminho/sub1/sub2", corpo)
resposta = ligacao.getresponse()
print ("*** Resultado do pedido:")
print (resposta.status, resposta.reason)
print ("*** Cabecalho da resposta (clausulas):")
print ("Clausula Content-type : ", resposta.getheader("Content-type"))
print ("*** Corpo da resposta:")
print(resposta.read().decode())
