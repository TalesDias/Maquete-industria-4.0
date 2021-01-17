from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from multiprocessing import Process
import memcache, sys, os

shared = memcache.Client(['127.0.0.1:11211'])

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../maquete.db'

db = SQLAlchemy(app)

class Peca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resultado = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

class Estado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
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
    global shared
    
    estados = []
    for estado in Estado.query.order_by(Estado.date_created).all():
        if estado.date_created > (datetime.now() - timedelta(days=31)):
            estados.append({            
                "nome": estado.nome,            
                "data": estado.date_created
            })
        
    pecas = []
    for peca in Peca.query.order_by(Peca.date_created).all():
        if peca.date_created > (datetime.now() - timedelta(days=7)):
            pecas.append({
                "resultado": peca.resultado,
                "data": peca.date_created
            })

    return {
        "estado_atual": shared.get("Estado"),
        "estados": estados,
        "pecas": pecas
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
        return {}, 400, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}


    user = Usuario.query.\
        filter(Usuario.apelido == apelido).\
        filter(Usuario.senha == senha).first()
    if user is None:
        return {}, 404, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}


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
        return {}, 400, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

    linha = str(datetime.now())
    linha += " @ "
    linha += apelido
    linha += "-> Realizou logout\n"
    log_to_file(linha)

    return {'msg': 'sucesso'}, 200, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}



@app.route('/log', methods=['OPTIONS'])
def logOP():
    return {}, 200, {
            "Content-Type" : "text/html; charset=utf-8",
            "Allow" : "OPTIONS,POST",
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Headers" : "*",
            "Expires":"1"
        }

@app.route('/log', methods=['POST'])
def log():
    cargo = request.json.get('cargo')
    if cargo is None:
        return {}, 400, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

    if cargo == 'administrador':
        with open('../log', 'r') as f:
            contents = f.readlines()
            f.close()
            return {
                'contents': contents
            }, 200, {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Headers" : "*",
                "Expires":"1"
            }

    return {}, 401, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}



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
    global shared
    apelido = request.json.get('apelido')
    tipo = request.json.get('tipo')

    if apelido is None or tipo is None:
        return {}, 400, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

    if tipo == "manutencao":
        shared.set("Estado", "Manutencao")
        linha = str(datetime.now())
        linha += " @ "
        linha += apelido
        linha += "-> Requisitou parada de manutencao\n"
        log_to_file(linha)

    elif tipo == "retomada":
        shared.set("Estado", "Inativo")
        linha = str(datetime.now())
        linha += " @ "
        linha += apelido
        linha += "-> Requisitou parada de retomada\n"
        log_to_file(linha)

    else:
        return {}, 400, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

    return {},200, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}




@app.route('/settime', methods=['OPTIONS'])
def settimeOP():
    return {}, 200, {
            "Content-Type" : "text/html; charset=utf-8",
            "Allow" : "OPTIONS,POST",
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Headers" : "*"
        }

@app.route('/settime', methods=['POST'])
def settime():
    global shared
    apelido = request.json.get('apelido')
    momento_text = request.json.get('momento')

    if apelido is None or momento_text is None:
        return {}, 400, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

    if apelido != "sudo":
        return {}, 401, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

    momento = datetime.strptime(momento_text, "%d/%m/%Y %H:%M:%S")
    
    momento_formatado = momento.strftime("%Y-%m-%d %H:%M:%S")
    
    res = os.system('timedatectl set-time \'%s\' ' % momento_formatado)
    
    if(res != 0):
        print(res)
        return {},500, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}
    

    return {},200, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}


def log_to_file(linha):
    with open('../log', 'a') as f:
        f.write(linha)
        f.close()


if __name__ == "__main__":
    app.run(debug=True)
