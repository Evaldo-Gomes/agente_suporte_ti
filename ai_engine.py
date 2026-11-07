
import json

from openai import OpenAI

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    validar_configuracao_groq
)

from prompts.triagem_prompt import criar_prompt_triagem

from google_docs import obter_documentacao


class AIEngine:
    """Gerencia a comunicação com o modelo GPT-OSS-20B."""

    def __init__(self):
        # Verifica se a chave da API está configurada
        validar_configuracao_groq()

        # Inicializa o cliente da Groq
        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        self.model = GROQ_MODEL

    def verificar_conexao(self):
        """Verifica a comunicação com o modelo."""

        try:
            resposta = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "Responda apenas: Conexão estabelecida."
                    }
                ],
                max_completion_tokens=100
            )

            return resposta.choices[0].message.content

        except Exception as erro:
            raise RuntimeError(
                f"Falha na comunicação com a Groq Cloud: {erro}"
            ) from erro

    def analisar_solicitacao(
        self,
        nome,
        email,
        solicitacao,
        documentacao
    ):
        """
        Analisa uma solicitação de suporte utilizando
        a documentação técnica disponível.
        """

        # Cria o prompt com os dados do colaborador
        prompt = criar_prompt_triagem(
            nome,
            email,
            solicitacao,
            documentacao
        )

        try:
            resposta = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_completion_tokens=1500
            )

            # Obtém o conteúdo retornado pelo modelo
            conteudo = resposta.choices[0].message.content

            if not conteudo:
                raise ValueError("O modelo retornou uma resposta vazia.")

            # Converte o JSON recebido em um dicionário Python
            resultado = json.loads(conteudo)

            # Verifica se todos os campos obrigatórios existem
            campos_obrigatorios = {
                "classification",
                "category",
                "response",
                "reason",
                "priority"
            }

            if not campos_obrigatorios.issubset(resultado.keys()):
                raise ValueError(
                    "A resposta não contém todos os campos obrigatórios."
                )

            # Valida os valores permitidos
            classificacoes_validas = {
                "resolved",
                "technical_support",
                "insufficient_information"
            }

            categorias_validas = {
                "network",
                "printer",
                "hardware",
                "software",
                "access",
                "other"
            }

            prioridades_validas = {
                "low",
                "medium",
                "high"
            }

            if resultado["classification"] not in classificacoes_validas:
                raise ValueError("Classificação inválida.")

            if resultado["category"] not in categorias_validas:
                raise ValueError("Categoria inválida.")

            if resultado["priority"] not in prioridades_validas:
                raise ValueError("Prioridade inválida.")

            return resultado

        except Exception as erro:
            raise RuntimeError(
                f"Falha na análise da solicitação: {erro}"
            ) from erro

    def analisar_com_documentacao(
        self,
        nome,
        email,
        solicitacao
    ):
        """
        Obtém a documentação diretamente do Google Docs
        e utiliza seu conteúdo na análise da solicitação.
        """

        try:
            # Busca a documentação atualizada no Google Docs
            documentacao = obter_documentacao()

            # Encaminha os dados para o modelo de IA
            resultado = self.analisar_solicitacao(
                nome,
                email,
                solicitacao,
                documentacao
            )

            return resultado

        except Exception as erro:
            raise RuntimeError(
                "Falha na análise com a documentação do Google Docs: "
                f"{erro}"
            ) from erro
