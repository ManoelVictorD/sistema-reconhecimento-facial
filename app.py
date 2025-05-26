from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
import os
import face_recognition
import numpy as np
from datetime import datetime
import asyncio
from PIL import Image
import jwt
import time
from functools import wraps
from decouple import config
from .models import init_db, get_db_connection
from .routes import register_routes
from .utils import registrar_log, resize_image

app = Flask(__name__)

# Configurações principais
app.secret_key = config('SECRET_KEY', default='fallback_secret_key')
app.config['UPLOAD_FOLDER'] = 'fotos'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutos
app.config['SESSION_COOKIE_NAME'] = 'facial_auth_session'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY', default='fallback_jwt_secret')
csrf = CSRFProtect(app)

# Inicialização do banco de dados
init_db()

# Registro das rotas
register_routes(app)

# Função de proteção JWT
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('jwt_token')
        if not token:
            flash('Acesso não autorizado', 'error')
            return redirect(url_for('admin_login', next=request.url))
        try:
            jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except:
            flash('Sessão inválida', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Limpeza de arquivos antigos na pasta fotos
def clean_old_files():
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(file_path) and (time.time() - os.path.getmtime(file_path)) > 3600:  # 1 hora
            os.remove(file_path)

@app.before_request
def before_request():
    clean_old_files()
    if request.endpoint in ['listar_usuarios', 'visualizar_logs', 'remover_usuario']:
        return login_required(lambda: None)(lambda: None)()

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'], mode=0o777)
    if not os.path.exists('instance'):
        os.makedirs('instance', mode=0o777)
    app.run(debug=True, port=5001)