# Facial Authentication System

## 🚀 Como Executar
```bash
# 1. Clone o repositório
git clone https://github.com/seu-user/facial-auth.git
cd facial-auth

# 2. Configure o ambiente
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# 3. Configure o .env
SECRET_KEY=sua_chave_secreta
JWT_SECRET_KEY=outra_chave_super_secreta
ADMIN_USERNAME=admin
ADMIN_PASSWORD=senha_forte

# 4. Execute
python app.py