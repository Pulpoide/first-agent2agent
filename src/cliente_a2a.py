"""
Cliente A2A con HTTPX — Para comunicación via HTTP.

Permite conectarse al servidor FastAPI y:
- Descubrir agentes disponibles
- Obtener Agent Cards individuales
- Iniciar un debate completo
"""

import httpx


class ClienteA2A:
    """
    Cliente A2A que usa httpx para comunicarse con agentes remotos.
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=120.0)

    async def descubrir_agentes(self) -> list:
        """GET /.well-known/agent-cards — Descubre todos los agentes."""
        response = await self.client.get(f"{self.base_url}/.well-known/agent-cards")
        response.raise_for_status()
        return response.json()

    async def obtener_agent_card(self, nombre: str) -> dict:
        """GET /agents/{nombre}/.well-known/agent-card.json"""
        response = await self.client.get(
            f"{self.base_url}/agents/{nombre}/.well-known/agent-card.json"
        )
        response.raise_for_status()
        return response.json()

    async def iniciar_debate(self, tema: str) -> dict:
        """POST /debate — Inicia un debate completo."""
        response = await self.client.post(
            f"{self.base_url}/debate",
            json={"tema": tema},
        )
        response.raise_for_status()
        return response.json()

    async def cerrar(self):
        await self.client.aclose()
