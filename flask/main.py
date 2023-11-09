from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://joao:@localhost/crm'

db = SQLAlchemy(app)

class Cliente(db.Model):
    cliente_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

class BatePapo(db.Model):
    bate_papo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)

class Chamada(db.Model):
    chamada_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, nullable=False)
    funcionario_id = db.Column(db.Integer, nullable=False)
    motivo_id = db.Column(db.Integer, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)

    def __init__(self, cliente_id, funcionario_id, motivo_id, data_hora):
        self.cliente_id = cliente_id
        self.funcionario_id = funcionario_id
        self.motivo_id = motivo_id
        self.data_hora = data_hora

class Funcionario(db.Model):
    funcionario_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    setor_id = db.Column(db.Integer)

    def __init__(self, nome, setor_id):
        self.nome = nome
        self.setor_id = setor_id      

class Motivo(db.Model):
    motivo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False)

    def __init__(self, descricao):
        self.descricao = descricao          

class RegistroEmail(db.Model):
    registro_email_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    assunto = db.Column(db.String(255), nullable=False)
    corpo = db.Column(db.Text)

    def __init__(self, cliente_id, data_hora, assunto, corpo):
        self.cliente_id = cliente_id
        self.data_hora = data_hora
        self.assunto = assunto
        self.corpo = corpo

class Usuario(db.Model):
    usuario_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

class Setor(db.Model):
    setor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)

    def __init__(self, nome):
        self.nome = nome

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        nome = request.form['nome']
        email = request.form['email']
        
        novo_cliente = Cliente(nome=nome, email=email)
        db.session.add(novo_cliente)
        db.session.commit()
        
    clientes = Cliente.query.all()
    return render_template('cliente.html', clientes=clientes)

@app.route('/bate_papo', methods=['GET', 'POST'])
def bate_papo():
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        nova_mensagem = request.form['nova_mensagem']
        
        usuario_existente = Usuario.query.filter_by(usuario_id=usuario_id).first()

        if not usuario_existente:
            return "Erro: Usuário com ID especificado não existe."

        if usuario_id and nova_mensagem:
            mensagem = BatePapo(usuario_id=usuario_id, mensagem=nova_mensagem)
            db.session.add(mensagem)
            db.session.commit()

    mensagens = BatePapo.query.all()
    return render_template('bate_papo.html', mensagens=mensagens)

@app.route('/chamadas', methods=['GET', 'POST'])
def chamadas():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        funcionario_id = request.form['funcionario_id']
        motivo_id = request.form['motivo_id']
        data_hora = request.form['data_hora']
        
        if cliente_id and funcionario_id and motivo_id and data_hora:
            chamada = Chamada(cliente_id, funcionario_id, motivo_id, data_hora)
            db.session.add(chamada)
            db.session.commit()
    
    chamadas = Chamada.query.all()
    return render_template('chamada.html', chamadas=chamadas)

@app.route('/funcionarios', methods=['GET', 'POST'])
def funcionarios():
    if request.method == 'POST':
        nome = request.form['nome']
        setor_id = request.form['setor_id']
        
        if nome:
            funcionario = Funcionario(nome, setor_id)
            db.session.add(funcionario)
            db.session.commit()
    
    funcionarios = Funcionario.query.all()
    return render_template('funcionario.html', funcionarios=funcionarios)

@app.route('/motivos', methods=['GET', 'POST'])
def motivos():
    if request.method == 'POST':
        descricao = request.form['descricao']
        
        if descricao:
            motivo = Motivo(descricao)
            db.session.add(motivo)
            db.session.commit()
    
    motivos = Motivo.query.all()
    return render_template('motivo.html', motivos=motivos)

@app.route('/registros_email', methods=['GET', 'POST'])
def registros_email():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        data_hora = request.form['data_hora']
        assunto = request.form['assunto']
        corpo = request.form['corpo']
        
        if cliente_id and data_hora and assunto and corpo:
            registro_email = RegistroEmail(cliente_id, data_hora, assunto, corpo)
            db.session.add(registro_email)
            db.session.commit()
    
    registros_email = RegistroEmail.query.all()
    return render_template('registro_email.html', registros_email=registros_email)

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        if nome and email and senha:
            usuario = Usuario(nome, email, senha)
            db.session.add(usuario)
            db.session.commit()
    
    usuarios = Usuario.query.all()
    return render_template('usuario.html', usuarios=usuarios)

@app.route('/setores', methods=['GET', 'POST'])
def setores():
    if request.method == 'POST':
        nome = request.form['nome']
        
        if nome:
            setor = Setor(nome)
            db.session.add(setor)
            db.session.commit()
    
    setores = Setor.query.all()
    return render_template('setor.html', setores=setores)

if __name__ == '__main__':
    app.run(debug=True)
