# Reconhecimento Facial para Controle de Acesso

## Descrição
Este projeto é um sistema de autenticação facial desenvolvido em Python com Flask, usando a biblioteca `face_recognition` para reconhecimento facial e SQLite como banco de dados. Ele permite:
- Cadastro de usuários com nome e foto facial.
- Autenticação via reconhecimento facial.
- Gerenciamento de usuários e logs por um painel administrativo.

O sistema foi projetado com boas práticas de desenvolvimento, incluindo modularização do código, uso de ambiente virtual e versionamento com Git.

## Tecnologias Utilizadas
- **Backend**: Python, Flask, face_recognition, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Outras Bibliotecas**: PIL (Pillow), PyJWT, python-decouple, Flask-WTF

## Como Rodar o Projeto

### Pré-requisitos
- Python 3.8 ou superior instalado
- Git instalado

### Passos
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu_usuario/reconhecimento_facial_acesso.git
   cd reconhecimento_facial_acesso