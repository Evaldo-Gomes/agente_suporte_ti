
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import (
    GOOGLE_CREDENTIALS_FILE,
    GOOGLE_TOKEN_FILE,
    GOOGLE_DOC_ID
)


# Permissões necessárias para o projeto
SCOPES = [
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/spreadsheets"
]


def autenticar_google():
    """Autentica o programa na conta Google utilizando OAuth 2.0."""

    credenciais = None

    if Path(GOOGLE_TOKEN_FILE).exists():
        credenciais = Credentials.from_authorized_user_file(
            str(GOOGLE_TOKEN_FILE),
            SCOPES
        )

    if credenciais and credenciais.expired and credenciais.refresh_token:
        credenciais.refresh(Request())

    if not credenciais or not credenciais.valid:
        fluxo = InstalledAppFlow.from_client_secrets_file(
            str(GOOGLE_CREDENTIALS_FILE),
            SCOPES
        )

        credenciais = fluxo.run_local_server(port=0)

    Path(GOOGLE_TOKEN_FILE).write_text(
        credenciais.to_json(),
        encoding="utf-8"
    )

    return credenciais


def extrair_texto(elementos):
    """
    Extrai textos de parágrafos e tabelas
    presentes na estrutura do Google Docs.
    """

    textos = []

    for elemento in elementos:

        # Extrai texto de parágrafos
        if "paragraph" in elemento:
            for parte in elemento["paragraph"].get("elements", []):
                texto = parte.get("textRun", {}).get("content", "")
                textos.append(texto)

        # Extrai texto de tabelas
        elif "table" in elemento:
            tabela = elemento["table"]

            for linha in tabela.get("tableRows", []):
                for celula in linha.get("tableCells", []):
                    conteudo = extrair_texto(
                        celula.get("content", [])
                    )
                    textos.append(conteudo)

        # Trata tabelas de conteúdo
        elif "tableOfContents" in elemento:
            conteudo = extrair_texto(
                elemento["tableOfContents"].get("content", [])
            )
            textos.append(conteudo)

    return "\n".join(textos)


def obter_documentacao():
    """
    Acessa o Google Docs e retorna o texto
    da documentação técnica de suporte.
    """

    if not GOOGLE_DOC_ID:
        raise ValueError(
            "GOOGLE_DOC_ID não foi configurado no arquivo .env."
        )

    try:
        # Realiza a autenticação
        credenciais = autenticar_google()

        # Inicializa o serviço Google Docs
        servico = build(
            "docs",
            "v1",
            credentials=credenciais,
            cache_discovery=False
        )

        # Obtém o conteúdo do documento
        documento = servico.documents().get(
            documentId=GOOGLE_DOC_ID
        ).execute()

        # Extrai o texto do corpo do documento
        conteudo = documento.get("body", {}).get("content", [])
        texto = extrair_texto(conteudo).strip()

        if not texto:
            raise ValueError(
                "O documento Google Docs não contém texto no corpo."
            )

        return texto

    except HttpError as erro:
        raise RuntimeError(
            f"Erro ao acessar o Google Docs: {erro}"
        ) from erro
