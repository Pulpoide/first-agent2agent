"""
Configuración global: LLM, logging y variables de entorno.
"""

import os
import logging

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# ─── Variables de entorno ────────────────────────────────────────────────────

load_dotenv()

# ─── Logging ─────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("A2A-Debate")

# ─── LLM (OpenAI) ───────────────────────────────────────────────────────────

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.0002,
    max_tokens=1000,
)
