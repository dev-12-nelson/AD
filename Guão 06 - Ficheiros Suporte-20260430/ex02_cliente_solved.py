import requests
import json

def print_request(): 
    print('\n\n\n')
    print('****************************************************************')
    print('****************************************************************')
    print("*************************Request********************************")
    print("Método:", r.request.method, " (r.request.method)")
    print("URL pedido: ", r.url, " (r.url)")
    print("Data: ", r.request.body, " (r.request.body)")
    print("Tipo de dados do Data: ", type(r.request.body))

def print_resposta():
    print("****************************************************************")
    print("****************************************************************")
    print("*************************Resposta*******************************")
    print ("Recebi o status code: ", r.status_code)
    print("* Header: ")
    for key, val in r.headers.items(): 
        print(f"{key}: {val}")
    print(" ")
    resposta_str = r.content.decode()
    if len(resposta_str) == 0: 
        resposta_str = "Resposta (body) vazio"
    print ("Recebi a resposta: ", resposta_str)
    print('****************************************************************')

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