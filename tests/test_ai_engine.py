
import json
from unittest.mock import Mock

import pytest

from ai_engine import AIEngine


def criar_engine_simulado(resposta_ia):
    """
    Cria uma instância simulada do AIEngine,
    sem estabelecer conexão com a Groq Cloud.
    """

    engine = AIEngine.__new__(AIEngine)

    resposta = Mock()
    resposta.choices[0].message.content = json.dumps(resposta_ia)

    engine.client = Mock()
    engine.client.chat.completions.create.return_value = resposta

    engine.model = "openai/gpt-oss-20b"

    return engine


def criar_resposta(classification):
    """Cria uma resposta simulada da inteligência artificial."""

    return {
        "classification": classification,
        "category": "hardware",
        "response": "Orientação de teste.",
        "reason": "Justificativa de teste.",
        "priority": "medium"
    }


def test_classificacao_resolved():
    """Verifica se uma resposta resolvida é aceita."""

    engine = criar_engine_simulado(
        criar_resposta("resolved")
    )

    resultado = engine.analisar_solicitacao(
        "Colaborador Teste",
        "teste@gmail.com",
        "Como configurar um monitor?",
        "Documentação de teste."
    )

    assert resultado["classification"] == "resolved"


def test_classificacao_technical_support():
    """Verifica se o encaminhamento técnico é aceito."""

    engine = criar_engine_simulado(
        criar_resposta("technical_support")
    )

    resultado = engine.analisar_solicitacao(
        "Colaborador Teste",
        "teste@gmail.com",
        "Meu computador não liga.",
        "Documentação de teste."
    )

    assert resultado["classification"] == "technical_support"


def test_classificacao_insufficient_information():
    """Verifica se a falta de informações é identificada."""

    engine = criar_engine_simulado(
        criar_resposta("insufficient_information")
    )

    resultado = engine.analisar_solicitacao(
        "Colaborador Teste",
        "teste@gmail.com",
        "Meu sistema não documentado apresenta erro.",
        "Documentação de teste."
    )

    assert resultado["classification"] == "insufficient_information"


def test_classificacao_invalida():
    """Verifica se classificações não permitidas são rejeitadas."""

    engine = criar_engine_simulado(
        criar_resposta("problema_desconhecido")
    )

    with pytest.raises(RuntimeError):
        engine.analisar_solicitacao(
            "Colaborador Teste",
            "teste@gmail.com",
            "Problema de teste.",
            "Documentação de teste."
        )


def test_resposta_sem_campo_obrigatorio():
    """Verifica se campos obrigatórios ausentes são rejeitados."""

    resposta = criar_resposta("resolved")
    del resposta["priority"]

    engine = criar_engine_simulado(resposta)

    with pytest.raises(RuntimeError):
        engine.analisar_solicitacao(
            "Colaborador Teste",
            "teste@gmail.com",
            "Problema de teste.",
            "Documentação de teste."
        )
