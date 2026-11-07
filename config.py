
import os
from pathlib import Path
from dotenv import load_dotenv

# Localização da pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent

# Carrega as variáveis do arquivo .env
load_dotenv(BASE_DIR / ".env")

# Configurações da Groq Cloud
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

# Configurações do Google Workspace
GOOGLE_DOC_ID = os.getenv("GOOGLE_DOC_ID")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

GOOGLE_CREDENTIALS_FILE = BASE_DIR / "credentials.json"
GOOGLE_TOKEN_FILE = BASE_DIR / "token.json"


def validar_configuracao_groq():
    """Verifica se a chave da API Groq foi configurada."""

    if not GROQ_API_KEY:
        raise ValueError(
            "A variável GROQ_API_KEY não foi encontrada no arquivo .env."
        )

    return True
