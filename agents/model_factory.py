"""
Fábrica de modelos LLM.

Retorna o modelo configurado via variável de ambiente LLM_PROVIDER.
Valores aceitos: "groq" (padrão) ou "openai".
"""

import os


def get_model():
    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider == "openai":
        from agno.models.openai import OpenAIChat
        return OpenAIChat(id="gpt-4o-mini")

    from agno.models.groq import Groq
    return Groq(id="llama-3.3-70b-versatile")
