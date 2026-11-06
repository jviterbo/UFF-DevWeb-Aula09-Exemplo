# Trecho a colar no arquivo WSGI do PythonAnywhere (aba Web > "WSGI configuration file").
# Substitua "seuusuario" e o nome da pasta do projeto.
import os
import sys

pasta = "/home/seuusuario/UFF-DevWeb-Recados"
if pasta not in sys.path:
    sys.path.insert(0, pasta)

# variáveis de ambiente: lê o arquivo .env do projeto
from dotenv import load_dotenv
load_dotenv(os.path.join(pasta, ".env"))

from app import app as application      # o PythonAnywhere procura por "application"
