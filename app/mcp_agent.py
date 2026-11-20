"""Agente de apoyo al aprendizaje y cliente MCP de la clase 06.

    uv run python -m app.mcp_agent --list-tools
    uv run python -m app.mcp_agent --trace "¿Qué es LoRA?"

En la clase 03 registramos directamente las funciones de tools.py. Aquí el
agente descubre las herramientas que ofrecen los servidores de
app/mcp_servers.json. Se mantiene el esquema de modelo, bucle y herramientas.
"""

import argparse
import inspect
import json
from pathlib import Path

from fastmcp import Client
from mcp.shared.exceptions import MCPError
from pydantic_ai import Agent
from pydantic_ai.exceptions import AgentRunError, ModelHTTPError, UserError
from pydantic_ai.mcp import MCPToolset, StdioTransport
from pydantic_ai.messages import RetryPromptPart, ToolCallPart, ToolReturnPart
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.test import TestModel
from pydantic_ai.providers.google import GoogleProvider

from app.config import MODEL, api_error_message, get_api_key

# Guía al agente en el uso del glosario y de los demás servidores configurados.
INSTRUCTIONS = """\
Eres el agente de apoyo al aprendizaje del curso de ingeniería de IA (AIE2026). Responde en español.
- Consulta el glosario mediante search_glossary antes de responder sobre términos o cuestiones del curso.
- Usa get_lecture_summary si te preguntan por el contenido de una clase.
- Si el término no figura en el glosario, indícalo y evita hacer suposiciones.
- Termina cada respuesta con el número de clase correspondiente (Lecture N).
- Ofrece pistas sobre el enfoque para que el estudiante resuelva su propia tarea.
- Usa una herramienta adecuada cuando esté disponible para temas ajenos al glosario, como páginas web o documentación de AWS.
"""

# Configuración de servidores en formato "mcpServers", como en Claude Desktop y Cursor.
MCP_CONFIG = Path(__file__).resolve().parent / "mcp_servers.json"


class ConfigError(Exception):
    """Error en la configuración de app/mcp_servers.json."""


def read_config(config_path: Path = MCP_CONFIG) -> dict:
    """Devuelve los nombres y los ajustes de los servidores en mcpServers."""
    try:
        config = json.loads(Path(config_path).read_text(encoding="utf-8"))["mcpServers"]
    except json.JSONDecodeError as e:
        raise ConfigError(f"JSON no válido cerca de la línea {e.lineno} ({e.msg})") from e
    except KeyError as e:
        raise ConfigError('Falta "mcpServers"') from e
    for name, spec in config.items():
        if "command" not in spec and "url" not in spec:
            raise ConfigError(f'El servidor "{name}" necesita "command" o "url"')
    return config


def load_mcp_servers(config_path: Path = MCP_CONFIG) -> list[MCPToolset]:
    """Crea un conjunto de herramientas MCP por cada servidor configurado.

    command inicia un subproceso mediante stdio. url conecta con un servidor
    activo por Streamable HTTP. El nombre del servidor funciona como prefijo
    y permite distinguir herramientas con el mismo nombre.

    Pydantic AI ofrece load_mcp_toolsets(). El modo legacy evita los avisos
    de detección automática al conectar con SDK antiguos como el de fetch.
    """
    toolsets = []
    for name, spec in read_config(config_path).items():
        if "url" in spec:
            transport = spec["url"]
        else:
            transport = StdioTransport(spec["command"], spec.get("args", []), env=spec.get("env"))
        toolsets.append(MCPToolset(Client(transport, mode="legacy")).prefixed(name))
    return toolsets


def describe_servers(config_path: Path = MCP_CONFIG) -> list[str]:
    """Describe cómo se inicia o se conecta cada servidor configurado."""
    lines = []
    for name, spec in read_config(config_path).items():
        if "url" in spec:
            lines.append(f"[server] {name}: conexión a la URL ({spec['url']})")
        else:
            command = " ".join([spec["command"], *spec.get("args", [])])
            lines.append(f"[server] {name}: inicio mediante el comando ({command})")
    return lines


def build_mcp_agent(config_path: Path = MCP_CONFIG) -> Agent:
    """Crea un agente con herramientas MCP. El modelo se proporciona al ejecutarlo."""
    return Agent(instructions=INSTRUCTIONS, toolsets=load_mcp_servers(config_path))


def build_model() -> GoogleModel:
    return GoogleModel(MODEL, provider=GoogleProvider(api_key=get_api_key()))


def print_tools(target: Agent) -> None:
    """Muestra nombres, descripciones y argumentos usando un modelo de prueba.

    TestModel permite consultar las definiciones sin llamar a un LLM.
    """
    model = TestModel(call_tools=[])
    target.run_sync("Lista de herramientas", model=model)
    tools_seen = model.last_model_request_parameters.function_tools
    print(f"Herramientas visibles para el modelo: {len(tools_seen)}")
    for tool in tools_seen:
        print(f"\n[{tool.name}]")
        print("  " + inspect.cleandoc(tool.description or "").replace("\n", "\n  "))
        params = tool.parameters_json_schema.get("properties", {})
        print(f"  Argumentos: {json.dumps(params, ensure_ascii=False)}")


def print_trace(result) -> None:
    """Muestra las llamadas a herramientas, sus argumentos y sus resultados."""
    print("\n--- trace ---")
    for message in result.all_messages():
        for part in message.parts:
            if isinstance(part, ToolCallPart):
                print(f"[tool call]   {part.tool_name}({part.args})")
            elif isinstance(part, ToolReturnPart):
                print(f"[tool return] {part.tool_name} -> {str(part.content)[:120]}…")
            elif isinstance(part, RetryPromptPart) and part.tool_name:
                # El modelo puede usar este error para decidir si vuelve a llamar a la herramienta.
                print(f"[tool error]  {part.tool_name} -> {str(part.content)[:120]}")
    usage = result.usage
    print(f"[usage] entrada {usage.input_tokens:,} tokens / salida {usage.output_tokens:,} tokens / respuestas del modelo {usage.requests}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Haz una pregunta al agente de apoyo con herramientas MCP")
    parser.add_argument("question", nargs="?")
    parser.add_argument("--trace", action="store_true", help="Mostrar las llamadas a herramientas")
    parser.add_argument("--list-tools", action="store_true", help="Listar las herramientas visibles para el modelo y salir (sin clave API)")
    args = parser.parse_args()
    if not args.list_tools and not args.question:
        parser.error("Escribe una pregunta")

    try:
        target = build_mcp_agent()
        print("\n".join(describe_servers()))
    except ConfigError as e:
        print(f"No se pudo leer app/mcp_servers.json: {e}")
        print("Comprueba que haya una coma entre servidores y que no sobre una después del último.")
        raise SystemExit(1)
    try:
        if args.list_tools:
            print_tools(target)
            return
        model = build_model()
        print(f"[model] {MODEL}")
        print(f"[tools] Servidores MCP ({MCP_CONFIG.relative_to(MCP_CONFIG.parent.parent)})")
        result = target.run_sync(args.question, model=model)
    except ModelHTTPError as e:
        print(api_error_message(e.status_code, str(e.body)[:200]))
        raise SystemExit(1)
    except (AgentRunError, UserError):
        raise  # Muestra el error original de ejecución del agente.
    except (MCPError, RuntimeError, OSError) as e:
        # El servidor no se pudo iniciar o conectar.
        print(f"No se pudo conectar con un servidor MCP: {e}")
        print("Comprueba el comando o la URL del servidor en app/mcp_servers.json.")
        raise SystemExit(1)
    print(result.output)
    if args.trace:
        print_trace(result)


if __name__ == "__main__":
    main()
