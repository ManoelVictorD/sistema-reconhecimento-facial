import os
import sqlite3
from PIL import Image
import time

def registrar_log(tipo_operacao, status, detalhes="", usuario_id=None, nome_usuario=""):
    try:
        conn = sqlite3.connect('instance/banco_de_dados.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO logs_acesso 
            (data_hora, usuario_id, nome_usuario, tipo_operacao, status, detalhes, ip_origem)
        VALUES 
            (datetime('now'), ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, nome_usuario, tipo_operacao, status, detalhes, request.remote_addr))
        conn.commit()
    except Exception as e:
        print(f"Erro ao registrar log: {str(e)}")
    finally:
        conn.close()

def resize_image(image_path, size=(300, 300)):
    with Image.open(image_path) as img:
        img_resized = img.resize(size, Image.LANCZOS)
        return img_resized