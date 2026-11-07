
from google_sheets import GoogleSheets


class TicketManager:
    """Controla a abertura e o registro de chamados de TI."""

    def __init__(self):
        """Inicializa o gerenciador de chamados."""

        self.google_sheets = None

    def registrar_se_autorizado(
        self,
        nome,
        email,
        solicitacao,
        resultado_ia
    ):
        """
        Avalia a classificação da IA e solicita autorização
        antes de registrar um chamado no Google Sheets.
        """

        classificacao = resultado_ia["classification"]

        # Se a IA encontrou uma solução documentada,
        # não existe necessidade de abrir um chamado.
        if classificacao == "resolved":
            return {
                "registrado": False,
                "mensagem": "Solicitação resolvida pela documentação."
            }

        # Verifica se a IA identificou necessidade de suporte
        elif classificacao in {
            "technical_support",
            "insufficient_information"
        }:

            print("\nA solicitação precisa de atendimento técnico.")
            print(
                "Motivo apresentado pela IA:",
                resultado_ia["reason"]
            )

            # Solicita autorização explícita do colaborador
            autorizacao = input(
                "\nDeseja abrir um chamado de suporte? (s/n): "
            ).strip().lower()

            if autorizacao not in {"s", "sim"}:
                return {
                    "registrado": False,
                    "mensagem": "Abertura do chamado não autorizada."
                }

            # Inicializa a conexão com o Google Sheets
            if self.google_sheets is None:
                self.google_sheets = GoogleSheets()

            # Registra o chamado após a autorização
            resultado = self.google_sheets.registrar_chamado(
                nome=nome,
                email=email,
                solicitacao=solicitacao,
                categoria=resultado_ia["category"],
                prioridade=resultado_ia["priority"],
                motivo=resultado_ia["reason"]
            )

            return {
                "registrado": resultado["sucesso"],
                "mensagem": resultado["mensagem"],
                "intervalo": resultado["intervalo"]
            }

        else:
            raise ValueError(
                f"Classificação desconhecida: {classificacao}"
            )
