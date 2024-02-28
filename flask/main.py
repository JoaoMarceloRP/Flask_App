from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://joao:@localhost/crm'

db = SQLAlchemy(app)

class Cliente(db.Model):
    cliente_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    registros_email = db.relationship('RegistroEmail', back_populates='cliente')


class BatePapo(db.Model):
    bate_papo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    
    usuario = db.relationship('Usuario', backref=db.backref('mensagens', lazy=True))

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
    registro_email_id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.cliente_id'))
    data_hora = db.Column(db.DateTime, nullable=False)
    assunto = db.Column(db.String(255), nullable=False)
    corpo = db.Column(db.Text)

    cliente = db.relationship('Cliente', back_populates='registros_email', primaryjoin='Cliente.cliente_id == RegistroEmail.cliente_id')

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
        nome = request.form['nome']
        email = request.form['email']
        
        novo_cliente = Cliente(nome=nome, email=email)
        db.session.add(novo_cliente)
        db.session.commit()
    
    clientes = Cliente.query.all()
    return render_template('cliente.html', clientes=clientes)

@app.route('/del_cliente/<int:cliente_id>', methods=['GET', 'POST'])
def del_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)

    registros_email_associados = cliente.registros_email
    for registro_email in registros_email_associados:
        db.session.delete(registro_email)

    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for('clientes'))

@app.route('/clientes/editar/<int:cliente_id>', methods=['GET', 'POST'])
def edt_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)

    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.email = request.form['email']
        db.session.commit()
        return redirect(url_for('clientes'))

    return render_template('cliente_edt.html', cliente=cliente)

@app.route('/bate_papo', methods=['GET', 'POST'])
def bate_papo():
    if request.method == 'POST':
        usuario_id = request.form['usuario_id']
        nova_mensagem = request.form['nova_mensagem']
        data = request.form['data']
        hora = request.form['hora']

        usuario_existente = Usuario.query.filter_by(usuario_id=usuario_id).first()

        if not usuario_existente:
            return "Erro: Usuário com ID especificado não existe."

        if usuario_id and nova_mensagem and data and hora:
            data_hora_str = f"{data} {hora}"
            data_hora = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M')
            mensagem = BatePapo(usuario_id=usuario_id, mensagem=nova_mensagem, data_hora=data_hora)
            db.session.add(mensagem)
            db.session.commit()

    mensagens = BatePapo.query.all()
    return render_template('bate_papo.html', mensagens=mensagens)
'''
@app.route('/batepapos/excluir/<int:batepapo_id>', methods=['POST'])
def excluir_batepapo(batepapo_id):
    batepapo = BatePapo.query.get_or_404(batepapo_id)
    
    usuario_id_relacionado = batepapo.usuario_id

    try:
        db.session.delete(batepapo)
        db.session.commit()
    except Exception as e:
        return f"Erro ao excluir a mensagem: {str(e)}"

    return redirect(url_for('bate_papo'))'''

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

        setor_existente = Setor.query.filter_by(setor_id=setor_id).first()

        if not setor_existente:
            return "Erro: Setor com ID especificado não existe."

        if nome:
            funcionario = Funcionario(nome, setor_id)
            db.session.add(funcionario)
            db.session.commit()

    funcionarios = Funcionario.query.all()
    return render_template('funcionario.html', funcionarios=funcionarios, setores=Setor.query.all())

@app.route('/del_funcionario/<int:funcionario_id>', methods=['GET', 'POST'])
def del_funcionario(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)
    if funcionario:
        db.session.delete(funcionario)
        db.session.commit()
        return redirect(url_for('funcionarios'))
    else:
        return "Funcionario não encontrado."
    
@app.route('/funcionarios/editar/<int:funcionario_id>', methods=['GET', 'POST'])
def edt_funcionario(funcionario_id):
    funcionario = Funcionario.query.get_or_404(funcionario_id)

    if request.method == 'POST':
        funcionario.nome = request.form['nome']
        setor_id = request.form['setor_id']

        setor_existente = Setor.query.filter_by(setor_id=setor_id).first()
        if not setor_existente:
            return "Erro: Setor com ID especificado não existe."

        funcionario.setor_id = setor_id
        db.session.commit()
        return redirect(url_for('funcionarios'))

    return render_template('funcionario_edt.html', funcionario=funcionario)

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
        assunto = request.form['assunto']
        corpo = request.form['corpo']
        data = request.form['data']
        hora = request.form['hora']

        if cliente_id and assunto and data and hora:
            data_hora_str = f"{data} {hora}"
            data_hora = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M')

            registro_email = RegistroEmail(cliente_id=cliente_id, assunto=assunto, corpo=corpo, data_hora=data_hora)
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

@app.route('/del_usuario/<int:usuario_id>', methods=['GET', 'POST'])
def del_usuario(usuario_id):
    usuario_id = Usuario.query.get(usuario_id)
    if usuario_id:
        db.session.delete(usuario_id)
        db.session.commit()
        return redirect(url_for('usuarios'))
    else:
        return "Usuario não encontrado."
    
@app.route('/usuario/editar/<int:usuario_id>', methods=['GET', 'POST'])
def edt_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.senha = request.form['senha']
        db.session.commit()
        return redirect(url_for('usuarios'))

    return render_template('usuario_edt.html', usuario=usuario) 

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

@app.route('/setores/excluir/<int:setor_id>', methods=['POST'])
def excluir_setor(setor_id):
    setor = Setor.query.get_or_404(setor_id)
    funcionarios_associados = Funcionario.query.filter_by(setor_id=setor.setor_id).all()

    if funcionarios_associados:
        for funcionario in funcionarios_associados:
            db.session.delete(funcionario)

    db.session.delete(setor)
    db.session.commit()

    return redirect(url_for('setores'))

@app.route('/setores/editar/<int:setor_id>', methods=['GET', 'POST'])
def editar_setor(setor_id):
    setor = Setor.query.get_or_404(setor_id)

    if request.method == 'POST':
        novo_nome = request.form['novo_nome']

        if novo_nome:
            setor.nome = novo_nome
            db.session.commit()
            return redirect(url_for('setores'))

    return render_template('setor_edt.html', setor=setor)    

if __name__ == '__main__':
    app.run(debug=True)