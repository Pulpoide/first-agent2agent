"""
Agent Cards — Definición de capacidades de cada agente (protocolo A2A).

Cada Agent Card es el equivalente a un /.well-known/agent-card.json
que describe: nombre, skills, versión del protocolo y URL del agente.
"""

AGENT_CARDS = {
    "sacerdote": {
        "name": "⛪ Agente Sacerdote",
        "description": "Analiza temas desde una perspectiva moral, ética y espiritual",
        "url": "http://localhost:8001",
        "version": "1.0.0",
        "protocolVersion": "0.3.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
        },
        "skills": [
            {
                "id": "moral",
                "name": "Análisis Moral y Espiritual",
                "description": "Evalúa temas desde la fe, la ética y los valores humanos",
                "examples": [
                    "¿Qué opinas moralmente de esta película?",
                    "Analiza el mensaje espiritual de esta obra",
                ],
            },
        ],
    },
    "critico_cine": {
        "name": "🎬 Agente Crítico de Cine",
        "description": "Analiza obras desde la perspectiva artística, cinematográfica y cultural",
        "url": "http://localhost:8002",
        "version": "1.0.0",
        "protocolVersion": "0.3.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
        },
        "skills": [
            {
                "id": "critica",
                "name": "Crítica Cinematográfica",
                "description": "Evalúa películas y obras culturales con ojo experto",
                "examples": [
                    "Analiza la cinematografía de esta película",
                    "¿Cuál es tu veredicto artístico?",
                ],
            },
        ],
    },
    "critico_del_critico": {
        "name": "🔥 Agente Crítico del Crítico",
        "description": "Cuestiona y desafía los argumentos del Crítico de Cine",
        "url": "http://localhost:8003",
        "version": "1.0.0",
        "protocolVersion": "0.3.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
        },
        "skills": [
            {
                "id": "contra_critica",
                "name": "Contra-Crítica",
                "description": "Desmonta argumentos del crítico de cine, encuentra sesgos y falacias",
                "examples": [
                    "Refuta la crítica anterior",
                    "¿Qué se le escapa al crítico?",
                ],
            },
        ],
    },
    "juez": {
        "name": "⚖️ Agente Juez",
        "description": "Evalúa todas las perspectivas y emite un veredicto imparcial",
        "url": "http://localhost:8004",
        "version": "1.0.0",
        "protocolVersion": "0.3.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
        },
        "skills": [
            {
                "id": "juzgar",
                "name": "Emisión de Veredicto",
                "description": "Analiza los argumentos de todos y determina quién tiene la razón",
                "examples": [
                    "¿Quién tiene la razón en este debate?",
                    "Emite tu veredicto final",
                ],
            },
        ],
    },
}
