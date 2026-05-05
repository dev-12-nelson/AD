from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/aluno', methods = ["PUT"])
@app.route('/aluno/<int:id>', methods = ["GET"])
def aluno(id = None):
    if request.method == "GET":
        # Ler dados do aluno com id na base de dados
        r = make_response('Dados do aluno %d' % id)
        r.status_code = 200
        return r
    if request.method == "PUT":
        # Ler dados do aluno no pedido e inserir na base de dados
        # Em caso de sucesso responder com a localização do novo recurso
        r = make_response()
        r.headers['location'] = '/alunos/123' # 123 para exemplo
        return r

@app.route('/notas', methods = ["POST", "GET"])
def notas():
    if request.method == "POST":
        #ler dados no pedido e inserir na base de dados
        r = make_response()
        return r
    if request.method == "GET":
        #ler campos no pedido e fazer query de acordo
        r = make_response(request.data) #Devolve os dados no pedido
        return r

if __name__ == '__main__':
    app.run(debug = True)