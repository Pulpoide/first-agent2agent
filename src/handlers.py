"""
Handlers — Lógica de cada agente (invocación al LLM).

Cada handler recibe un texto y un context_id,
y devuelve la respuesta del LLM como string.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from src.config import llm


async def handler_sacerdote(texto: str, ctx: str) -> str:
    """Handler del Agente Sacerdote: perspectiva moral y espiritual."""
    messages = [
        SystemMessage(
            content=(
                "Eres un sacerdote reflexivo. Analizas temas desde la moral, ética y "
                "espiritualidad. Sé BREVE y CONCISO: da exactamente 3 puntos cortos "
                "(máximo 2 oraciones cada uno). Responde en español."
            )
        ),
        HumanMessage(content=texto),
    ]
    response = await llm.ainvoke(messages)
    return response.content


async def handler_critico_cine(texto: str, ctx: str) -> str:
    """Handler del Agente Crítico de Cine: análisis artístico y cultural."""
    messages = [
        SystemMessage(
            content=(
                "Eres un crítico de cine mordaz e intelectual. Analizas desde el arte: "
                "dirección, guion, actuaciones y narrativa. Sé BREVE y CONCISO: "
                "da exactamente 3 puntos cortos (máximo 2 oraciones cada uno). "
                "Responde en español."
            )
        ),
        HumanMessage(content=texto),
    ]
    response = await llm.ainvoke(messages)
    return response.content


async def handler_critico_del_critico(texto: str, ctx: str) -> str:
    """Handler del Agente Crítico del Crítico: desafía al crítico de cine."""
    messages = [
        SystemMessage(
            content=(
                "Eres el crítico del crítico: sarcástico y agudo. Desmontas sesgos "
                "y falacias del crítico de cine. Defiendes al público general. "
                "Sé BREVE: da exactamente 3 puntos cortos (máximo 2 oraciones cada uno). "
                "Responde en español."
            )
        ),
        HumanMessage(content=texto),
    ]
    response = await llm.ainvoke(messages)
    return response.content


async def handler_juez(texto: str, ctx: str) -> str:
    """Handler del Agente Juez: evalúa todos los argumentos y emite veredicto."""
    messages = [
        SystemMessage(
            content=(
                "Eres un juez imparcial. Evalúas 3 perspectivas: Sacerdote, Crítico "
                "de Cine y Crítico del Crítico. Sé BREVE. Formato:\n"
                "⛪ SACERDOTE: [1 oración]\n"
                "🎬 CRÍTICO: [1 oración]\n"
                "🔥 CONTRA-CRÍTICO: [1 oración]\n"
                "⚖️ VEREDICTO: [quién tiene razón, 2-3 oraciones]\n"
                "Responde en español."
            )
        ),
        HumanMessage(content=texto),
    ]
    response = await llm.ainvoke(messages)
    return response.content
