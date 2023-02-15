from flask import Flask, request
from service.modeling import Modeling
from flask_cors import CORS
import os

# Cria a instância da aplicação Flask.
app = Flask(__name__)

# Ativa a política de CORS para permitir requisições de outros domínios.
CORS(app, origins={"https://montador-de-grades-upfpc35ezq-uc.a.run.app/"})

# Cria uma instância da classe Modeling para processar os dados da API.
ucs = Modeling()

# Cria a classe Grade com os métodos que definem as rotas da API.
class Grade():

    # Rota "/disciplinas" - rota para obter as informações de todas as disciplinas, utilizando o método GET.
    @app.route("/disciplinas", methods=['GET'])
    def get():
        # Chama o método get_ucs da instância da classe Modeling e retorna a resposta em formato JSON.
        return ucs.get_ucs()

    # Rota "/disciplinas" - rota para adicionar uma nova disciplina, utilizando o método POST.
    @app.route("/disciplinas", methods=['POST'])
    def post():

        # Obtém os dados do objeto JSON enviado na requisição POST.
        data = request.get_json()

        # Chama o método uc_analizer da instância da classe Modeling e passa o objeto JSON com as informações da disciplina.
        return ucs.uc_analyzer(data['items'])

# Verifica se este arquivo é o arquivo principal que está sendo executado.
if __name__ == '__main__':
    # Executa a aplicação Flask com o método run(). 
    # O servidor é iniciado na porta especificada, que é a porta definida na variável de ambiente "PORT", ou a porta 8080 caso essa variável não esteja definida.
    # O modo de depuração é ativado para facilitar o desenvolvimento e depuração da aplicação.
    app.run(host="0.0.0.0", port=8080)
