"""Servidor MCP del glosario y los resúmenes de la clase 06.

    uv run python -m app.mcp_agent --list-tools
    uv run python -m app.mcp_server --http

El primer comando lista las herramientas sin clave API. El segundo inicia
Streamable HTTP en http://127.0.0.1:8000/mcp.

De forma predeterminada, el servidor espera datos por stdio. Los clientes MCP
como app.mcp_agent lo lanzan como subproceso. Si lo ejecutas directamente,
queda a la espera. Las funciones registradas en la clase 03 están disponibles
a través del mismo protocolo para el agente y para otros clientes MCP.
"""

import argparse

from mcp.server.mcpserver import MCPServer

from app import tools

# Nombre y descripción del servidor, visibles en el cliente (distintos de la clave "glossary" de la configuración)
server = MCPServer(
    "aie2026-glossary",
    instructions="Ofrece el glosario y los puntos clave de las sesiones de AI Engineering Pilot Course (AIE2026).",
)

# Ofrece las mismas funciones de Lecture 03 como herramientas MCP. Los docstrings y las anotaciones de tipos forman la descripción
server.tool()(tools.search_glossary)

# TODO(Tarea básica): expón también get_lecture_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor MCP del glosario")
    parser.add_argument("--http", action="store_true", help="Iniciar con Streamable HTTP (stdio de forma predeterminada)")
    args = parser.parse_args()
    if args.http:
        print("Iniciando el servidor MCP en http://127.0.0.1:8000/mcp (Ctrl+C para detenerlo)")
        server.run(transport="streamable-http")
    else:
        # Con stdio, la salida estándar es el canal del protocolo: no se debe usar print
        server.run()


if __name__ == "__main__":
    main()
