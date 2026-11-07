
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import GOOGLE_SHEET_ID
from google_docs import autenticar_google


class GoogleSheets:
    """Gerencia o registro de chamados no Google Sheets."""

    def __init__(self):
        # Verifica se o ID da planilha foi configurado
        if not GOOGLE_SHEET_ID:
            raise ValueError(
                "GOOGLE_SHEET_ID não foi configurado no arquivo .env."
            )

        # Autentica na conta Google
        credenciais = autenticar_google()

        # Inicializa o serviço Google Sheets
        self.service = build(
            "sheets",
            "v4",
            credentials=credenciais,
            cache_discovery=False
        )

        self.spreadsheet_id = GOOGLE_SHEET_ID

    def registrar_chamado(
        self,
        nome,
        email,
        solicitacao,
        categoria,
        prioridade,
        motivo
    ):
        """
        Registra um chamado na primeira aba da planilha.
        """

        try:
            # Obtém a data e hora atual
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # Organiza os dados conforme as colunas da planilha
            valores = [[
                data_hora,
                nome,
                email,
                solicitacao,
                categoria,
                prioridade,
                motivo,
                "Aberto"
            ]]

            # Define o intervalo de inserção
            intervalo = "Chamados!A:H"

            # Insere os dados na próxima linha disponível
            resultado = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=intervalo,
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body={
                    "values": valores
                }
            ).execute()

            return {
                "sucesso": True,
                "mensagem": "Chamado registrado com sucesso.",
                "intervalo": resultado.get("updates", {}).get(
                    "updatedRange"
                )
            }

        except HttpError as erro:
            raise RuntimeError(
                f"Erro ao registrar chamado no Google Sheets: {erro}"
            ) from erro
