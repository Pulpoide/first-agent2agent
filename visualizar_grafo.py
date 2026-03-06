"""
Visualizar el StateGraph del debate A2A.

Genera una imagen PNG del grafo y la abre automaticamente.
uv run python visualizar_grafo.py
"""

import sys
import os

# Fix encoding para Windows
sys.stdout.reconfigure(encoding="utf-8")

from src.grafo import construir_grafo_debate


def main():
    print("Construyendo el grafo del debate A2A...")

    grafo = construir_grafo_debate()

    # Metodo 1: Generar PNG con Mermaid (requiere internet)
    try:
        png_data = grafo.compile().get_graph().draw_mermaid_png()
        output_file = "grafo_debate.png"
        with open(output_file, "wb") as f:
            f.write(png_data)
        print(f"Grafo guardado en: {output_file}")
        print("Abriendo imagen...")

        os.startfile(output_file)  # Windows

    except Exception as e:
        print(f"No se pudo generar PNG: {e}")
        print("")

        # Metodo 2: Imprimir el diagrama Mermaid como texto
        print("Diagrama Mermaid (copia esto a https://mermaid.live):")
        print("-" * 50)
        mermaid_str = grafo.compile().get_graph().draw_mermaid()
        print(mermaid_str)
        print("-" * 50)


if __name__ == "__main__":
    main()
