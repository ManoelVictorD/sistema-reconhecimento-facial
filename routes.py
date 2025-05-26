from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from werkzeug.utils import secure_filename
import os
import face_recognition
import numpy as np
import asyncio
from PIL import Image
import jwt
from datetime import datetime
from .utils import registrar_log, resize_image

def register_routes(app):
    @app.route('/')
    def index():
        return redirect(url_for('acesso'))

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if request.method == 'POST':
            if 'nome' not in request.form or 'foto' not in request.files:
                flash('Formulário inválido', 'error')
                return redirect(url_for('cadastro'))

            nome = request.form['nome']
            foto = request.files['foto']

            if not nome or len(nome.strip()) < 3:
                flash('Nome inválido', 'error')
                return redirect(url_for('cadastro'))

            if foto.filename == '':
                flash('Nenhuma foto selecionada', 'error')
                return redirect(url_for('cadastro'))

            try:
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                filename = secure_filename(foto.filename)
                caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto.save(caminho_foto)
                print(f"📁 Arquivo salvo temporariamente em: {caminho_foto}")

                resized_image = resize_image(caminho_foto, (300, 300))
                resized_image.save(caminho_foto)

                start_time = time.time()
                imagem = face_recognition.load_image_file(caminho_foto)
                rostos = face_recognition.face_encodings(imagem)
                processing_time = time.time() - start_time
                
                print(f"⏱️ Tempo de processamento: {processing_time:.2f} segundos")
                print(f"🔍 Rostos detectados: {len(rostos)}")

                if len(rostos) == 0:
                    os.remove(caminho_foto)
                    flash('Nenhum rosto detectado. Envie uma foto frontal clara.', 'error')
                    return redirect(url_for('cadastro'))
                
                if len(rostos) > 1:
                    os.remove(caminho_foto)
                    flash('Múltiplos rostos detectados. Envie uma foto com apenas uma pessoa.', 'error')
                    return redirect(url_for('cadastro'))

                encoding_rosto = rostos[0].tolist()
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO usuarios (nome, encoding_rosto) VALUES (?, ?)', (nome, str(encoding_rosto)))
                    conn.commit()

                os.remove(caminho_foto)
                flash(f'Usuário "{nome}" cadastrado com sucesso!', 'success')
                registrar_log('CADASTRO', 'SUCESSO', f'Usuário {nome} cadastrado')
                return redirect(url_for('cadastro'))

            except Exception as e:
                print(f"🔥 ERRO CRÍTICO: {str(e)}")
                if 'caminho_foto' in locals() and os.path.exists(caminho_foto):
                    os.remove(caminho_foto)
                flash('Erro durante o processamento. Tente novamente.', 'error')
                registrar_log('CADASTRO', 'FALHA', str(e))
                return redirect(url_for('cadastro'))

        return render_template('cadastro.html')

    @app.route('/acesso', methods=['GET', 'POST'])
    def acesso():
        if request.method == 'POST':
            if 'foto' not in request.files:
                flash('Nenhuma foto enviada', 'error')
                return redirect(url_for('acesso'))
            foto = request.files['foto']
            if foto.filename == '':
                flash('Nenhuma foto selecionada', 'error')
                return redirect(url_for('acesso'))

            try:
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                filename = secure_filename(foto.filename)
                caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto.save(caminho_foto)
                resized_image = resize_image(caminho_foto, (300, 300))
                resized_image.save(caminho_foto)

                imagem = face_recognition.load_image_file(caminho_foto)
                encoding = face_recognition.face_encodings(imagem)[0]
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT id, nome, encoding_rosto FROM usuarios')
                    for row in cursor.fetchall():
                        db_encoding = np.array(eval(row[2]))
                        if face_recognition.compare_faces([db_encoding], encoding)[0]:
                            session['user_id'] = row[0]
                            registrar_log('AUTH', 'SUCESSO', f'Usuário {row[1]} autenticado')
                            return redirect(url_for('dashboard'))
                flash('Rosto não reconhecido', 'error')
                registrar_log('AUTH', 'FALHA', 'Rosto não encontrado')
                os.remove(caminho_foto)
                return redirect(url_for('acesso'))
            except Exception as e:
                print(f"🔥 ERRO CRÍTICO: {str(e)}")
                if 'caminho_foto' in locals() and os.path.exists(caminho_foto):
                    os.remove(caminho_foto)
                flash('Erro durante o processamento. Tente novamente.', 'error')
                registrar_log('AUTH', 'FALHA', str(e))
                return redirect(url_for('acesso'))

        return render_template('acesso.html')

    @app.route('/admin_login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username == config('ADMIN_USERNAME', default='admin') and password == config('ADMIN_PASSWORD', default='senha_segura'):
                token = jwt.encode({'user': 'admin', 'exp': datetime.utcnow().timestamp() + 1800}, app.config['JWT_SECRET_KEY'], algorithm='HS256')
                session['jwt_token'] = token
                session['is_admin'] = True
                flash('Login bem-sucedido!', 'success')
                registrar_log('ACESSO', 'SUCESSO', 'Admin logado')
                next_url = request.args.get('next')
                return redirect(next_url or url_for('listar_usuarios'))
            flash('Credenciais inválidas', 'error')
            registrar_log('ACESSO', 'FALHA', 'Credenciais inválidas')
        return render_template('admin_login.html')

    @app.route('/admin_logout')
    @login_required
    def admin_logout():
        session.pop('jwt_token', None)
        session.pop('is_admin', None)
        flash('Logout realizado com sucesso!', 'success')
        registrar_log('ACESSO', 'SUCESSO', 'Admin deslogado')
        return redirect(url_for('admin_login'))

    @app.route('/listar_usuarios')
    @login_required
    def listar_usuarios():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios')
            usuarios = cursor.fetchall()
        return render_template('admin_usuarios.html', usuarios=usuarios)

    @app.route('/remover_usuario/<int:usuario_id>', methods=['POST'])
    @login_required
    def remover_usuario(usuario_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))
            conn.commit()
        flash('Usuário removido com sucesso!', 'success')
        registrar_log('REMOCAO', 'SUCESSO', f'Usuário ID {usuario_id} removido')
        return redirect(url_for('listar_usuarios'))

    @app.route('/visualizar_logs')
    @login_required
    def visualizar_logs():
        pagina = int(request.args.get('pagina', 1))
        por_pagina = 10
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM logs_acesso')
            total = cursor.fetchone()[0]
            total_paginas = (total + por_pagina - 1) // por_pagina
            offset = (pagina - 1) * por_pagina
            cursor.execute('SELECT * FROM logs_acesso ORDER BY data_hora DESC LIMIT ? OFFSET ?', (por_pagina, offset))
            logs = cursor.fetchall()
        return render_template('logs.html', logs=logs, pagina=pagina, total_paginas=total_paginas)

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')