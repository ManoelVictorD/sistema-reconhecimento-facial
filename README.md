# Sistema de Reconhecimento Facial para Controle de Acesso

## 📌 Visão Geral
Sistema de autenticação biométrica desenvolvido em Python com:
- Cadastro facial via upload de imagens
- Reconhecimento em tempo real
- Painel administrativo com logs de acesso

## 🛠 Tecnologias
- **Backend**: Python, Flask, SQLite
- **Reconhecimento Facial**: Biblioteca `face_recognition` (dlib/OpenCV)
- **Frontend**: HTML/CSS com Design System moderno
- **Segurança**: JWT, CSRF Protection

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Git instalado

### Passo a Passo
```bash
# 1. Clone o repositório
git clone https://github.com/ManoelVictorD/sistema-reconhecimento-facial.git
cd sistema-reconhecimento-facial

# 2. Crie e ative o ambiente virtual (Windows)
python -m venv .venv
.venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o sistema
python app.py