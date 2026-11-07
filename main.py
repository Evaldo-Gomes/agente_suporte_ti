
from ai_engine import AIEngine
from ticket_manager import TicketManager


def exibir_cabecalho():
    """Apresenta a identificação do assistente."""

    print("\n" + "=" * 60)
    print("       ASSISTENTE INTELIGENTE DE SUPORTE DE TI")
    print("=" * 60)
    print("Atendimento automatizado de dúvidas e problemas de TI.")
    print("Descreva seu problema para receber uma orientação.")
    print("=" * 60)


def coletar_dados_colaborador():
    """Solicita os dados básicos do colaborador."""

    print("\nIDENTIFICAÇÃO DO COLABORADOR")

    nome = input("Nome completo: ").strip()
    while not nome:
        print("O nome não pode ficar vazio.")
        nome = input("Nome completo: ").strip()

    email = input("E-mail corporativo: ").strip()
    while not email or "@" not in email:
        print("Informe um endereço de e-mail válido.")
        email = input("E-mail corporativo: ").strip()

    return nome, email


def coletar_solicitacao():
    """Recebe a descrição do problema de TI."""

    print("\nDESCRIÇÃO DO PROBLEMA")

    solicitacao = input(
        "Descreva sua dúvida ou problema de TI: "
    ).strip()

    while not solicitacao:
        print("A descrição não pode ficar vazia.")
        solicitacao = input(
            "Descreva sua dúvida ou problema de TI: "
        ).strip()

    return solicitacao


def executar_atendimento():
    """Coordena o atendimento automatizado."""

    exibir_cabecalho()

    nome, email = coletar_dados_colaborador()
    solicitacao = coletar_solicitacao()

    print("\nAnalisando sua solicitação...")
    print("Consultando a documentação de suporte de TI...")

    try:
        # Inicializa o mecanismo de inteligência artificial.
        assistente = AIEngine()

        # Analisa o problema utilizando a documentação do Google Docs.
        resultado = assistente.analisar_com_documentacao(
            nome=nome,
            email=email,
            solicitacao=solicitacao
        )

        print("\n" + "=" * 60)
        print("RESULTADO DO ATENDIMENTO")
        print("=" * 60)

        print("\nOrientação:")
        print(resultado["response"])

        # Exibe o encaminhamento quando a documentação não resolve.
        if resultado["classification"] == "resolved":
            print("\nSua solicitação foi respondida com base na documentação.")
            print("Atendimento encerrado.")

        else:
            # O registro só acontece após autorização do colaborador.
            gerente = TicketManager()

            registro = gerente.registrar_se_autorizado(
                nome=nome,
                email=email,
                solicitacao=solicitacao,
                resultado_ia=resultado
            )

            print("\nRESULTADO DO ENCAMINHAMENTO")
            print(registro["mensagem"])

            if registro.get("intervalo"):
                print(
                    "Registro na planilha:",
                    registro["intervalo"]
                )

        print("\n" + "=" * 60)
        print("Obrigado por utilizar o Assistente de Suporte de TI.")
        print("=" * 60)

    except Exception as erro:
        print("\nNão foi possível concluir o atendimento.")
        print("Detalhes:", erro)
        print(
            "\nTente novamente mais tarde ou procure "
            "o suporte de TI."
        )


if __name__ == "__main__":
    executar_atendimento()
