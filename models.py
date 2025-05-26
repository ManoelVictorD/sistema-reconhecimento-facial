import sqlite3

def init_db():
    conn = sqlite3.connect('instance/banco_de_dados.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        encoding_rosto TEXT NOT NULL,
        data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs_acesso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora TEXT NOT NULL,
        usuario_id INTEGER,
        nome_usuario TEXT,
        tipo_operacao TEXT CHECK(tipo_operacao IN ('CADASTRO', 'ACESSO', 'REMOCAO', 'AUTH')),
        status TEXT CHECK(status IN ('SUCESSO', 'FALHA', 'AVISO')),
        detalhes TEXT,
        ip_origem TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('instance/banco_de_dados.db')