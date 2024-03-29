from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from time import localtime, mktime
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
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

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
                "data": estado.date_created.astimezone()
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
        linha += "-> Requisitou retomada de execucao\n"
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
    cargo = request.json.get('cargo')
    momento_text = request.json.get('momento')

    if cargo is None or momento_text is None:
        return {}, 400, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

    if cargo != "administrador":
        return {}, 401, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

    momento = datetime.strptime(momento_text, "%d/%m/%Y %H:%M:%S")
    
    momento_formatado = momento.strftime("%Y-%m-%d %H:%M:%S")
    
    res = os.system('timedatectl set-time \'%s\' ' % momento_formatado)
    
    if(res != 0):
        print(res)
        return {},500, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}
    

    return {},200, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}



@app.route('/modatividade', methods=['OPTIONS'])
def modatividadeOP():
    return {}, 200, {
            "Content-Type" : "text/html; charset=utf-8",
            "Allow" : "OPTIONS,POST",
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Headers" : "*"
        }

@app.route('/modatividade', methods=['POST'])
def modatividade():
    global shared
    cargo = request.json.get('cargo')
    porcentagem = request.json.get('porcentagem')
    duracao     = request.json.get('duracao')
    
    if cargo is None or porcentagem is None or duracao is None:
        return {}, 400, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

    if cargo != "administrador":
        return {}, 401, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}
    
    
    porcentagem = int(porcentagem)
    duracao     = int(duracao)
    
    tempoAtivo = timedelta(seconds=int(porcentagem/100 * duracao * 60))
    
    agora = datetime.fromtimestamp(mktime(localtime()))

    inicio     = Estado(nome="Invalido", date_created = (agora - timedelta(minutes=duracao)))
    fimAtivo   = Estado(nome="Inativo" , date_created = (agora - tempoAtivo))
    fimInativo = Estado(nome="Ativo"   , date_created = agora)
    
    for estado in Estado.query.all():
        db.session.delete(estado)
    
    db.session.add(inicio)
    db.session.add(fimAtivo)
    db.session.add(fimInativo)
    db.session.commit()
    
    return {},200, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}



@app.route('/modhistoricopecas', methods=['OPTIONS'])
def modhistoricopecasOP():
    return {}, 200, {
            "Content-Type" : "text/html; charset=utf-8",
            "Allow" : "OPTIONS,POST",
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Headers" : "*"
        }

@app.route('/modhistoricopecas', methods=['POST'])
def modhistoricopecas():
    global shared
    cargo = request.json.get('cargo')
    historico     = request.json.get('historico')
    concluidas    = request.json.get('concluidas')
    retrabalhadas = request.json.get('retrabalhadas')
    refugadas     = request.json.get('refugadas')
    
    if cargo is None or historico is None or concluidas is None or retrabalhadas is None or refugadas is None:
        return {}, 400, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}

    if cargo != "administrador":
        return {}, 401, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}
    
    concluidas    = int(concluidas)
    retrabalhadas = int(retrabalhadas)
    refugadas     = int(refugadas)
    
    
    for peca in Peca.query.all():
        db.session.delete(peca)
    
    data = datetime.now()
    
    for i in range(concluidas):
        peca = Peca(resultado="concluida", date_created=data)
        db.session.add(peca)

    for i in range(retrabalhadas):
        peca = Peca(resultado="retrabalhada", date_created=data)
        db.session.add(peca)

    for i in range(refugadas):
        peca = Peca(resultado="refugada", date_created=data)
        db.session.add(peca)
    
    for i in range(6):
        data = (datetime.now() - timedelta(days = (6 - i)))
        for _ in range(int(historico[i])):
            peca = Peca(resultado="concluida", date_created=data)
            db.session.add(peca)

    db.session.commit()
    
    
    return {},200, {"Access-Control-Allow-Origin" : "*", "Access-Control-Allow-Headers" : "*"}




def log_to_file(linha):
    with open('../log', 'a') as f:
        f.write(linha)
        f.close()


if __name__ == "__main__":
    app.run(debug=True)
