import sys
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (opcional, para rodar localmente)
load_dotenv()

# Garante que o Python encontre os módulos na pasta app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mangum import Mangum
from app.main import app

handler = Mangum(app)
