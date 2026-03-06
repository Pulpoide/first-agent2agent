"""
StateGraph — Flujo orquestado entre los 4 agentes.

Define el estado compartido (DebateState) y los nodos del grafo.
Cada nodo corresponde a un agente A2A que:
1. Se descubre via Agent Card
2. Recibe un mensaje via message/send
3. Devuelve su respuesta como artifact
"""

from typing import TypedDict, Annotated

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages

from src.config import logger
from src.registro_a2a import RegistroA2A


# ─── Estado compartido del debate ────────────────────────────────────────────


class DebateState(TypedDict):
    """Estado compartido del debate entre agentes."""

    tema: str  # Tema del debate
    opinion_sacerdote: str  # Perspectiva moral
    critica_cine: str  # Crítica cinematográfica
    contra_critica: str  # Contra-crítica
    veredicto: str  # Veredicto del juez
    messages: Annotated[list, add_messages]  # Historial de mensajes
    task_log: list[dict]  # Log de tareas A2A


# ─── Instancia global del registro A2A ───────────────────────────────────────

registro = RegistroA2A()


# ─── Nodos del grafo (cada nodo = un agente A2A) ────────────────────────────


async def nodo_sacerdote(state: DebateState) -> dict:
    """Nodo 1: El Sacerdote da su perspectiva moral y espiritual."""
    tema = state["tema"]
    logger.info("━" * 60)
    logger.info("⛪ FASE 1: PERSPECTIVA DEL SACERDOTE")
    logger.info("━" * 60)

    card = registro.descubrir("sacerdote")
    logger.info(f"   Agent Card: {card['name']} v{card['version']}")

    response = await registro.enviar_mensaje(
        "sacerdote",
        f"Analiza el siguiente tema desde tu perspectiva moral y espiritual:\n\n{tema}",
    )
    resultado = response["result"]
    opinion = resultado["artifacts"][0]["parts"][0]["text"]

    return {
        "opinion_sacerdote": opinion,
        "messages": [AIMessage(content=f"[SACERDOTE]\n{opinion}")],
        "task_log": [resultado],
    }


async def nodo_critico_cine(state: DebateState) -> dict:
    """Nodo 2: El Crítico de Cine da su análisis artístico."""
    tema = state["tema"]
    logger.info("━" * 60)
    logger.info("🎬 FASE 2: CRÍTICA CINEMATOGRÁFICA")
    logger.info("━" * 60)

    card = registro.descubrir("critico_cine")
    logger.info(f"   Agent Card: {card['name']} v{card['version']}")

    prompt = (
        f"Tema de debate: {tema}\n\n"
        f"El Sacerdote ya dio su perspectiva moral:\n{state['opinion_sacerdote']}\n\n"
        f"Ahora da TU análisis como crítico de cine. Puedes coincidir o disentir."
    )

    response = await registro.enviar_mensaje("critico_cine", prompt)
    resultado = response["result"]
    critica = resultado["artifacts"][0]["parts"][0]["text"]

    return {
        "critica_cine": critica,
        "messages": [AIMessage(content=f"[CRÍTICO DE CINE]\n{critica}")],
        "task_log": state.get("task_log", []) + [resultado],
    }


async def nodo_critico_del_critico(state: DebateState) -> dict:
    """Nodo 3: El Crítico del Crítico desafía al Crítico de Cine."""
    tema = state["tema"]
    logger.info("━" * 60)
    logger.info("🔥 FASE 3: CONTRA-CRÍTICA")
    logger.info("━" * 60)

    card = registro.descubrir("critico_del_critico")
    logger.info(f"   Agent Card: {card['name']} v{card['version']}")

    prompt = (
        f"Tema de debate: {tema}\n\n"
        f"El Crítico de Cine dijo lo siguiente:\n{state['critica_cine']}\n\n"
        f"Desmonta su crítica. Encuentra sesgos, falacias y lo que se le escapa. "
        f"Defiende al público general."
    )

    response = await registro.enviar_mensaje("critico_del_critico", prompt)
    resultado = response["result"]
    contra = resultado["artifacts"][0]["parts"][0]["text"]

    return {
        "contra_critica": contra,
        "messages": [AIMessage(content=f"[CRÍTICO DEL CRÍTICO]\n{contra}")],
        "task_log": state.get("task_log", []) + [resultado],
    }


async def nodo_juez(state: DebateState) -> dict:
    """Nodo 4: El Juez evalúa todas las perspectivas y emite veredicto."""
    logger.info("━" * 60)
    logger.info("⚖️ FASE 4: VEREDICTO")
    logger.info("━" * 60)

    card = registro.descubrir("juez")
    logger.info(f"   Agent Card: {card['name']} v{card['version']}")

    prompt = (
        f"═══ DEBATE: {state['tema']} ═══\n\n"
        f"⛪ PERSPECTIVA DEL SACERDOTE (moral/espiritual):\n"
        f"{state['opinion_sacerdote']}\n\n"
        f"{'─' * 40}\n\n"
        f"🎬 CRÍTICA DEL CRÍTICO DE CINE (artístico/cultural):\n"
        f"{state['critica_cine']}\n\n"
        f"{'─' * 40}\n\n"
        f"🔥 CONTRA-CRÍTICA DEL CRÍTICO DEL CRÍTICO:\n"
        f"{state['contra_critica']}\n\n"
        f"{'─' * 40}\n\n"
        f"Analiza las tres perspectivas y emite tu VEREDICTO: "
        f"¿quién tiene más razón y por qué?"
    )

    response = await registro.enviar_mensaje("juez", prompt)
    resultado = response["result"]
    veredicto = resultado["artifacts"][0]["parts"][0]["text"]

    return {
        "veredicto": veredicto,
        "messages": [AIMessage(content=f"[JUEZ]\n{veredicto}")],
        "task_log": state.get("task_log", []) + [resultado],
    }


# ─── Construcción del grafo ──────────────────────────────────────────────────


def construir_grafo_debate():
    """
    Construye el StateGraph del debate A2A.

    Flujo:
    START → sacerdote → critico_cine → critico_del_critico → juez → END
    """
    grafo = StateGraph(DebateState)

    # Agregar nodos (cada nodo = un agente A2A)
    grafo.add_node("sacerdote", nodo_sacerdote)
    grafo.add_node("critico_cine", nodo_critico_cine)
    grafo.add_node("critico_del_critico", nodo_critico_del_critico)
    grafo.add_node("juez", nodo_juez)

    # Definir flujo (edges)
    grafo.add_edge(START, "sacerdote")
    grafo.add_edge("sacerdote", "critico_cine")
    grafo.add_edge("critico_cine", "critico_del_critico")
    grafo.add_edge("critico_del_critico", "juez")
    grafo.add_edge("juez", END)

    return grafo
