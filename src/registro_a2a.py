"""
Registro A2A — Descubrimiento y comunicación entre agentes.

Simula los endpoints del protocolo A2A:
- GET  /.well-known/agent-card.json  → descubrimiento de agente
- POST /  con method: message/send   → envío de mensajes

Task lifecycle: submitted → working → completed | failed
"""

import uuid
from src.config import logger


class RegistroA2A:
    """
    Registro central que simula el descubrimiento y la comunicación
    entre agentes siguiendo el protocolo A2A (Agent-to-Agent).

    En producción, cada agente sería un servidor HTTP independiente.
    """

    def __init__(self):
        self.agentes: dict = {}
        self.task_store: dict = {}
        logger.info("╔══════════════════════════════════════════╗")
        logger.info("║   Registro A2A inicializado              ║")
        logger.info("╚══════════════════════════════════════════╝")

    def registrar(self, nombre: str, card: dict, handler):
        """Registra un agente en el ecosistema A2A."""
        self.agentes[nombre] = {"card": card, "handler": handler}
        logger.info(f"  ✅ Registrado: {card['name']}")

    def descubrir(self, nombre: str) -> dict | None:
        """GET /.well-known/agent-card.json — Descubrimiento de agente."""
        entry = self.agentes.get(nombre)
        if entry:
            logger.info(f"  🔎 Descubierto: {entry['card']['name']}")
            return entry["card"]
        logger.warning(f"  ❌ Agente '{nombre}' no encontrado")
        return None

    def listar(self) -> list:
        """Lista todos los agentes registrados y sus skills."""
        return [
            {
                "id": k,
                "name": v["card"]["name"],
                "description": v["card"]["description"],
                "skills": [s["name"] for s in v["card"]["skills"]],
            }
            for k, v in self.agentes.items()
        ]

    async def enviar_mensaje(
        self,
        nombre_agente: str,
        texto: str,
        context_id: str | None = None,
    ) -> dict:
        """
        POST / con method: message/send — Protocolo A2A.

        Lifecycle: submitted → working → completed | failed
        """
        entry = self.agentes.get(nombre_agente)
        if not entry:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32001,
                    "message": f"Agente '{nombre_agente}' no encontrado",
                },
            }

        ctx = context_id or str(uuid.uuid4())[:8]
        task_id = str(uuid.uuid4())[:8]

        # Task empieza como "submitted"
        task = {
            "taskId": task_id,
            "contextId": ctx,
            "status": {"state": "submitted"},
            "from_agent": entry["card"]["name"],
            "artifacts": [],
        }
        self.task_store[task_id] = task
        logger.info(f"  📨 Task {task_id} → {entry['card']['name']} [submitted]")

        # Cambia a "working"
        task["status"]["state"] = "working"
        logger.info(f"  ⚙️  Task {task_id} → {entry['card']['name']} [working]")

        try:
            resultado = await entry["handler"](texto, ctx)
            task["status"]["state"] = "completed"
            task["artifacts"] = [
                {
                    "name": "response",
                    "parts": [{"kind": "text", "text": resultado}],
                }
            ]
            logger.info(f"  ✅ Task {task_id} → {entry['card']['name']} [completed]")
            return {"jsonrpc": "2.0", "result": task}

        except Exception as e:
            task["status"]["state"] = "failed"
            task["status"]["error"] = str(e)
            logger.error(f"  ❌ Task {task_id} → {entry['card']['name']} [failed]: {e}")
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32000, "message": str(e)},
            }
