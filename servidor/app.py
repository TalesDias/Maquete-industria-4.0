from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../maquete.db'

db = SQLAlchemy(app)

session = {}


class Peca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resultado = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apelido = db.Column(db.String(200), nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    cargo = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['GET'])
def dashboard():
    pecas = []
    pecas_mes = 0
    for peca in Peca.query.order_by(Peca.date_created).all():
        if peca.date_created.day < datetime.now().day:
            if peca.resultado != 'refugada':
                pecas_mes += 1
        else:
            pecas.append(peca.resultado)

    ultima_man = None
    with open('../log', 'r') as f:
        for line in f.readlines():
            if line.find('requisitou parada de manutencao'):
                ultima_man = line.split('@')[0]
    f.close()

    return {
        'pecas': pecas,
        'producao_mes': pecas_mes,
        'ultima_manutencao': ultima_man
    }, 200, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}


@app.route('/login', methods=['OPTIONS'])
def entrarOP():
    return {}, 200, {
            "Content-Type" : "text/html; charset=utf-8",
            "Allow" : "OPTIONS,POST",
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Headers" : "*"
        }

@app.route('/login', methods=['POST'])
def entrar():
    apelido = request.json.get('apelido')
    senha = request.json.get('senha')

    if apelido is None or senha is None:
        return {}, 400

    user = Usuario.query.\
        filter(Usuario.apelido == apelido).\
        filter(Usuario.senha == senha).first()
    if user is None:
        return {}, 404

    session[apelido] = user.cargo

    linha = str(datetime.now())
    linha += " @ "
    linha += user.apelido
    linha += "-> Realizou login\n"
    log_to_file(linha)

    return {'cargo': user.cargo}, 200, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

@app.route('/logout', methods=['OPTIONS'])
def sairOP():
    return {}, 200, {
            "Content-Type" : "text/html; charset=utf-8",
            "Allow" : "OPTIONS,POST",
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Headers" : "*"
        }

@app.route('/logout', methods=['POST'])
def sair():
    apelido = request.json.get('apelido')
    if apelido is None:
        return {}, 400

    if session.get(apelido) is None:
        return {}, 404

    linha = str(datetime.now())
    linha += " @ "
    linha += apelido
    linha += "-> Realizou logout\n"
    log_to_file(linha)

    session.pop(apelido, None)
    return {'msg': 'sucesso'}, 200, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}


@app.route('/log', methods=['OPTIONS'])
def logOP():
    return {}, 200, {
            "Content-Type" : "text/html; charset=utf-8",
            "Allow" : "OPTIONS,POST",
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Headers" : "*"
        }

@app.route('/log', methods=['POST'])
def log():
    apelido = request.json.get('apelido')
    if apelido is None:
        return {}, 401

    if session.get(apelido) is None:
        return {}, 401

    if session.get(apelido) == 'administrador':
        with open('../log', 'r') as f:
            contents = f.readlines()
            f.close()
            return {
                'contents': contents
            }, 200, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

    return {}, 401


@app.route('/parada', methods=['OPTIONS'])
def paradaOP():
    return {}, 200, {
            "Content-Type" : "text/html; charset=utf-8",
            "Allow" : "OPTIONS,POST",
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Headers" : "*"
        }

@app.route('/parada', methods=['POST'])
def parada():
    apelido = request.json.get('apelido')
    tipo = request.json.get('tipo')

    if apelido is None or tipo is None:
        return {}, 401

    if session.get(apelido) is None:
        return {}, 401

    # requisitar para o sistema

    if tipo == "manutencao":
        linha = str(datetime.now())
        linha += " @ "
        linha += apelido
        linha += "-> Requisitou parada de manutencao\n"
        log_to_file(linha)

    elif tipo == "emergencia":
        linha = str(datetime.now())
        linha += " @ "
        linha += apelido
        linha += "-> Requisitou parada de emergencia\n"
        log_to_file(linha)

    elif tipo == "retomada":
        linha = str(datetime.now())
        linha += " @ "
        linha += apelido
        linha += "-> Requisitou parada de retomada\n"
        log_to_file(linha)

    else:
        return {}, 401

    return {},200, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

def log_to_file(linha):
    with open('../log', 'a') as f:
        f.write(linha)
        f.close()


if __name__ == "__main__":
    app.run(debug=True)
