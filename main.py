import mysql.connector
from flask import *
import random
import smtplib
from email.mime.text import MIMEText







app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'
# Cria ou conecta ao banco de dados
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1903',
)
cursor = conn.cursor()

# Cria o banco de dados se não existir
cursor.execute("CREATE DATABASE IF NOT EXISTS users_db")
conn.commit()

# Conecta ao banco de dados recém-criado
conn.database = 'users_db'

# Cria a tabela de usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
)
''')

conn.commit()
conn.close()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Guarda os dados na sessão, não salva no banco ainda!
        session['email'] = email
        session['username'] = username
        session['password'] = password
        return redirect(url_for('confirmacao'))
    return render_template('register.html')

@app.route('/confirmacao')
def confirmacao():
    email = session.get('email')
    if not email:
        return redirect(url_for('register'))

    # Gera código de 6 dígitos
    codigo = ''.join([str(random.randint(0,9)) for _ in range(6)])
    session['codigo_confirmacao'] = codigo

    # Envia o e-mail
    remetente = 'lorita.lolo1324@gmail.com'
    senha_email = 'sobu khhs wvvx zikf'
    assunto = 'Seu código de confirmação'
    mensagem = f'Olá somos da ????, e vimos que você acabou de criar uma conta usando este email. Aqui está o seu código de confirmação: {codigo}'

    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remetente, senha_email)
            smtp.sendmail(remetente, email, msg.as_string())
    except Exception as e:
        return f'Erro ao enviar e-mail: {e}'
    
    return render_template('confirmation.html')

@app.route('/confirmar_codigo', methods=['POST'])
def confirmar_codigo():
    # Recebe os 6 dígitos do formulário
    codigo_digitado = ''.join([
        request.form.get('codigo1', ''),
        request.form.get('codigo2', ''),
        request.form.get('codigo3', ''),
        request.form.get('codigo4', ''),
        request.form.get('codigo5', ''),
        request.form.get('codigo6', '')
    ])
    codigo_correto = session.get('codigo_confirmacao')
    if codigo_digitado == codigo_correto:
        # Salva no banco de dados
        username = session.get('username')
        email = session.get('email')
        password = session.get('password')
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1903',
            database='users_db'
        )
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            conn.commit()
            msg = 'Cadastro confirmado e salvo com sucesso!'
        except mysql.connector.Error as err:
            msg = f'Erro ao salvar: {err}'
        finally:
            cursor.close()
            conn.close()
        # Limpa sessão
        session.pop('username', None)
        session.pop('email', None)
        session.pop('password', None)
        session.pop('codigo_confirmacao', None)
        # Redireciona para tela de login
        return redirect(url_for('login'))
    else:
        return render_template('confirmation.html', erro='Código incorreto, tente novamente.')


@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1903',
            database='users_db'
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (email, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return "Login realizado com sucesso!"
        else:
            erro = "E-mail ou senha incorretos."
    return render_template('login.html', erro=erro)

if __name__ == '__main__':
    app.run(debug=True)