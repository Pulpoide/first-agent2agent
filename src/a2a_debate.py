"""
A2A Debate — Punto de entrada principal.

Dos modos de ejecución:
  uv run python -m src.a2a_debate            → Debate interactivo en terminal
  uv run python -m src.a2a_debate --server   → Servidor FastAPI en localhost:8000
"""

import json
import asyncio
from datetime import datetime

from langchain_core.messages import HumanMessage

from src.config import logger
from src.agent_cards import AGENT_CARDS
from src.handlers import (
    handler_sacerdote,
    handler_critico_cine,
    handler_critico_del_critico,
    handler_juez,
)
from src.grafo import registro, construir_grafo_debate


# =============================================================================
#  EJECUCIÓN DEL DEBATE
# =============================================================================


async def ejecutar_debate_completo(tema: str) -> dict:
    """Ejecuta el flujo completo del debate entre los 4 agentes."""

    logger.info("╔══════════════════════════════════════════════════════════╗")
    logger.info("║       A2A DEBATE — SISTEMA MULTI-AGENTE                 ║")
    logger.info("║       Sacerdote × Crítico × Meta-Crítico × Juez         ║")
    logger.info("╠══════════════════════════════════════════════════════════╣")
    logger.info(f"║  Tema: {tema:<49}║")
    logger.info("╚══════════════════════════════════════════════════════════╝")
    logger.info("")

    # 1) Registrar agentes en el ecosistema A2A
    logger.info("📋 Registrando agentes en el ecosistema A2A...")
    registro.registrar("sacerdote", AGENT_CARDS["sacerdote"], handler_sacerdote)
    registro.registrar(
        "critico_cine", AGENT_CARDS["critico_cine"], handler_critico_cine
    )
    registro.registrar(
        "critico_del_critico",
        AGENT_CARDS["critico_del_critico"],
        handler_critico_del_critico,
    )
    registro.registrar("juez", AGENT_CARDS["juez"], handler_juez)
    logger.info("")

    # 2) Listar agentes descubiertos
    logger.info("🔎 Agentes descubiertos en el registro A2A:")
    for agente in registro.listar():
        logger.info(f"   • {agente['name']} → Skills: {', '.join(agente['skills'])}")
    logger.info("")

    # 3) Construir y ejecutar el StateGraph
    logger.info("🏗️  Construyendo StateGraph del debate...")
    grafo = construir_grafo_debate().compile()
    logger.info(
        "   Flujo: START → Sacerdote → Crítico de Cine → Crítico del Crítico → Juez → END"
    )
    logger.info("")

    estado_inicial = {
        "tema": tema,
        "opinion_sacerdote": "",
        "critica_cine": "",
        "contra_critica": "",
        "veredicto": "",
        "messages": [HumanMessage(content=f"Tema de debate: {tema}")],
        "task_log": [],
    }

    # 4) Ejecutar el grafo
    resultado = await grafo.ainvoke(estado_inicial)

    # 5) Presentar resultados
    logger.info("")
    logger.info("╔══════════════════════════════════════════════════════════╗")
    logger.info("║              DEBATE FINALIZADO                          ║")
    logger.info("╚══════════════════════════════════════════════════════════╝")

    resumen = {
        "tema": tema,
        "timestamp": datetime.now().isoformat(),
        "agentes_participantes": [
            AGENT_CARDS[a]["name"]
            for a in ["sacerdote", "critico_cine", "critico_del_critico", "juez"]
        ],
        "fases": {
            "opinion_sacerdote": resultado["opinion_sacerdote"],
            "critica_cine": resultado["critica_cine"],
            "contra_critica": resultado["contra_critica"],
            "veredicto": resultado["veredicto"],
        },
        "tasks_a2a": resultado["task_log"],
        "total_tasks": len(resultado["task_log"]),
    }

    return resumen


def imprimir_resultado(resumen: dict):
    """Imprime el resultado del debate de forma legible."""
    print("\n" + "=" * 70)
    print(f"  🎙️  DEBATE A2A: {resumen['tema']}")
    print("=" * 70)

    print(f"\n📅 Timestamp: {resumen['timestamp']}")
    print(f"👥 Agentes: {', '.join(resumen['agentes_participantes'])}")
    print(f"📊 Total tareas A2A: {resumen['total_tasks']}")

    print("\n" + "─" * 70)
    print("⛪ FASE 1 — PERSPECTIVA DEL SACERDOTE")
    print("─" * 70)
    print(resumen["fases"]["opinion_sacerdote"])

    print("\n" + "─" * 70)
    print("🎬 FASE 2 — CRÍTICA CINEMATOGRÁFICA")
    print("─" * 70)
    print(resumen["fases"]["critica_cine"])

    print("\n" + "─" * 70)
    print("🔥 FASE 3 — CONTRA-CRÍTICA (CRÍTICO DEL CRÍTICO)")
    print("─" * 70)
    print(resumen["fases"]["contra_critica"])

    print("\n" + "─" * 70)
    print("⚖️ FASE 4 — VEREDICTO DEL JUEZ")
    print("─" * 70)
    print(resumen["fases"]["veredicto"])

    print("\n" + "=" * 70)
    print("  ✅ Debate A2A finalizado exitosamente")
    print("=" * 70)


# =============================================================================
#  SERVIDOR FastAPI
# =============================================================================


def crear_servidor():
    """Crea un servidor FastAPI que expone los endpoints A2A."""
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI(
        title="A2A Debate Server",
        description="Servidor multi-agente con protocolo A2A — Debate cultural",
        version="1.0.0",
    )

    @app.get("/.well-known/agent-cards")
    async def listar_agentes():
        return JSONResponse(content=registro.listar())

    for nombre, card in AGENT_CARDS.items():

        @app.get(f"/agents/{nombre}/.well-known/agent-card.json")
        async def get_agent_card(agent_name=nombre):
            card_data = registro.descubrir(agent_name)
            if card_data:
                return JSONResponse(content=card_data)
            return JSONResponse(
                status_code=404,
                content={"error": f"Agente '{agent_name}' no encontrado"},
            )

    @app.post("/debate")
    async def ejecutar_debate_endpoint(request: dict):
        tema = request.get("tema", "La película Oppenheimer")
        resultado = await ejecutar_debate_completo(tema)
        return JSONResponse(content=resultado)

    return app


# =============================================================================
#  PUNTO DE ENTRADA
# =============================================================================


async def main():
    """Punto de entrada principal: ejecuta el debate directamente."""
    tema = input(
        "\n🎙️  Ingresa el tema del debate (o presiona Enter para usar el default):\n"
        "   Default: 'La película Oppenheimer: ¿obra maestra o sobrevalorada?'\n\n"
        "   👉 "
    ).strip()

    if not tema:
        tema = "La película Oppenheimer: ¿obra maestra o sobrevalorada?"

    resumen = await ejecutar_debate_completo(tema)
    imprimir_resultado(resumen)

    # Guardar resultado en JSON
    output_file = "resultado_debate.json"
    with open(output_file, "w", encoding="utf-8") as f:
        resumen_serializable = {
            "tema": resumen["tema"],
            "timestamp": resumen["timestamp"],
            "agentes_participantes": resumen["agentes_participantes"],
            "fases": resumen["fases"],
            "total_tasks": resumen["total_tasks"],
        }
        json.dump(resumen_serializable, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Resultado guardado en: {output_file}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        import uvicorn

        app = crear_servidor()
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        asyncio.run(main())
