import requests
import json

def print_request(): 
    # TODO: 
    # Deve apresentar o método pedido (r.request.method)
    # Deve apresentar o URL pedido (r.url)
    # Deve apresentar o corpo do pedido (r.request.body) e o seu tipo (type)
    pass

def print_resposta():
    # TODO: 
    # Deve apresentar o status code
    # Deve apresentar os vários items do header (r.header.items())
    # Deve apresentar o conteudo da resposta (r.content.decode())
    pass

dados = {'numero': 123, 'nome': 'Carabino Tiro Certo', 'idade': 18}
r = requests.put('http://localhost:5000/aluno', json = dados)
print_request()
print_resposta()

r = requests.get('http://localhost:5000/aluno/123')
print_request()
print_resposta()

notas = {'numero_aluno': 123, 'ano': '1988/1989', 'cadeira': 'AD', 'nota': 20}
r = requests.post('http://localhost:5000/notas', json = notas)
print_request()
print_resposta()

pesquisa = {'ano': '1988/1989', 'cadeira': 'AD'}
r = requests.get('http://localhost:5000/notas', json = pesquisa)
print_request()
print_resposta()