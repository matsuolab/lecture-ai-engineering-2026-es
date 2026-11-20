# Práctica y tarea de la clase 06 — Usar herramientas de un servidor MCP desde un agente

## Objetivos de la sesión

- Usar tu propio servidor MCP desde un agente con la herramienta de glosario de la clase 03.
- Mostrar y leer los nombres, las descripciones y los argumentos de las herramientas que recibe el modelo.
- Usar servidores MCP de otros proveedores añadiéndolos a un archivo de configuración.

Trabaja en GitHub Codespaces desde tu fork. Usa la clave de la API de Gemini que registraste en la clase 01.

## Tres formas de usar un servidor MCP

Prueba estas tres opciones en orden.

| | Iniciar tu propio servidor | Usar un servidor publicado | Conectarte a un servidor remoto |
|---|---|---|---|
| Conexión | El agente inicia el servidor con un comando en tu entorno | `uvx` descarga e inicia el servidor en tu entorno | El agente se conecta a un servidor que ya está en ejecución |
| Práctica | STEP 1 y 2 (servidor del glosario) | STEP 3 (servidor fetch) | STEP 4 (servidor AWS Knowledge) |
| Configuración | `"command": "uv"` | `"command": "uvx"` | `"url": "https://…"` |

Usa `command` para iniciar un servidor en tu entorno y `url` para conectarte a uno remoto.

## Archivos de la clase 06

Durante la práctica editarás el archivo de configuración. Consulta o ejecuta los demás archivos según corresponda.

| Archivo | Función | Qué hacer |
|---|---|---|
| [app/tools.py](../../app/tools.py) | Contiene las funciones de las herramientas, entre ellas `search_glossary` y `get_lecture_summary` de la clase 03 | Consúltalo |
| [app/mcp_server.py](../../app/mcp_server.py) | Publica funciones de `app/tools.py` como herramientas MCP | Consúltalo. Añadirás una línea en la tarea básica |
| [app/mcp_servers.json](../../app/mcp_servers.json) | Configura los servidores MCP que usa el agente | Añade servidores en STEP 3 y STEP 4 |
| [app/mcp_agent.py](../../app/mcp_agent.py) | Se conecta a los servidores configurados y usa sus herramientas | Ejecútalo desde la terminal |
| [app/agent.py](../../app/agent.py) | Es el agente usado hasta la clase 05 | Ejecútalo en STEP 1 para listar sus herramientas |

## Práctica (30 minutos)

Dedica unos 23 minutos a la preparación y a los pasos STEP 1 a STEP 5.

### Preparación — Crear la rama lec06 (unos 2 minutos)

1. En la página de tu fork en GitHub, selecciona **Sync fork → Update branch** si hay una actualización disponible.
2. En la terminal de Codespaces, ejecuta estos comandos en orden.

```bash
git switch main
git pull --no-rebase
git switch -c lec06
uv sync --frozen
```

3. Ejecuta `ls app/mcp_agent.py` y comprueba que aparece el nombre del archivo.

- Si `git switch main` se detiene porque quedan cambios en la rama anterior, haz commit de tu trabajo y vuelve a intentarlo.
- Si aparece `a branch named 'lec06' already exists`, cambia a esa rama con `git switch lec06`.
- Si `git pull --no-rebase` indica `CONFLICT`, ejecuta `git merge --abort` para conservar tus cambios y sigue las instrucciones indicadas abajo.

#### Si te queda trabajo de una clase anterior

Parte del código actual de la clase 06 en el repositorio del curso. Ejecuta los comandos en orden.

```bash
git fetch https://github.com/matsuolab/lecture-ai-engineering-2026-es.git main
git switch -c lec06 FETCH_HEAD
uv sync --frozen
```

Sigue también este procedimiento si Sync fork muestra un conflicto. Para conservar tus commits, deja sin pulsar **Discard commits**.

### STEP 1 — Listar las herramientas de tu servidor (unos 4 minutos)

Comprueba que el agente inicia el servidor del glosario y entrega sus herramientas al modelo.

```bash
uv run python -m app.agent --list-tools
uv run python -m app.mcp_agent --list-tools
```

Ambos comandos funcionan sin clave API.

1. El primero lista las herramientas del agente utilizado hasta la clase 05, entre ellas `search_materials`.
2. La primera línea del segundo comando indica cómo se inició el servidor del glosario. Debajo figuran las herramientas que ofrece.
3. Compara las listas. El modelo recibe los nombres, las descripciones y los argumentos en el mismo formato.

El segundo comando muestra lo siguiente.

```text
[server] glossary: inicio mediante el comando (uv run python -m app.mcp_server)
Herramientas visibles para el modelo: 1

[glossary_search_glossary]
  Busca un término en el glosario del curso y devuelve su definición y la sesión en que se trata.

  Úsala antes de responder sobre términos de ingeniería de IA o expresiones específicas de
  este curso (AIE2026). Incluye en query un único término para consultar (por ejemplo, "LoRA").
  Argumentos: {"query": {"title": "Query", "type": "string"}}
```

Los nombres de las herramientas MCP combinan el nombre del servidor, un guion bajo y el nombre de la herramienta. En `glossary_search_glossary`, `glossary` es el servidor definido en el archivo de configuración y `search_glossary` es la función de `app/tools.py`. El prefijo permite distinguir herramientas con el mismo nombre en distintos servidores.

### STEP 2 — Preguntar al agente y revisar la llamada a la herramienta (unos 4 minutos)

Comprueba que el agente llama a la herramienta del servidor MCP al contestar una pregunta.

```bash
uv run python -m app.mcp_agent --trace "¿Cuáles son los 3 niveles de las tareas del curso AIE2026?"
```

Es la misma pregunta que en la clase 03. Revisa estas líneas después de `--- trace ---`.

1. `[tool call]` muestra `glossary_search_glossary` y los argumentos elegidos por el modelo.
2. `[tool return]` muestra el contenido del glosario que devolvió el servidor MCP.
3. `[usage]` indica al menos dos respuestas del modelo. En una llama a la herramienta. En la siguiente lee el resultado y responde.

En la clase 03, el agente llamaba directamente a la función. Ahora el servidor MCP llama a la función y devuelve el resultado al agente.

### STEP 3 — Descargar y usar un servidor publicado (unos 5 minutos)

Añade fetch, un servidor que recupera páginas web, y comprueba que el agente puede usarlo.

1. Abre `app/mcp_servers.json`. Añade una coma después de la llave de cierre de `glossary` y agrega las cuatro líneas de `"fetch"`.

```json
{
  "mcpServers": {
    "glossary": {
      "command": "uv",
      "args": ["run", "python", "-m", "app.mcp_server"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch==2026.11.11", "--no-readability-js"]
    }
  }
}
```

2. Ejecuta el primer comando. Comprueba que aparece `[server] fetch: inicio mediante el comando` y que la lista contiene `fetch_fetch`.
3. Haz la pregunta con el segundo comando. Busca `fetch_fetch` y la URL en la línea `[tool call]`.

```bash
uv run python -m app.mcp_agent --list-tools
uv run python -m app.mcp_agent --trace "Resume en tres líneas en español el inicio de https://modelcontextprotocol.io/."
```

- `uvx` descarga y ejecuta un programa publicado. El servidor fetch se ejecuta en tu Codespace. El primer comando tarda unos 10 segundos la primera vez.
- `==2026.11.11` fija la versión, pues las actualizaciones de un servidor externo pueden cambiar su comportamiento.
- `--no-readability-js` indica al servidor que extraiga el contenido de la página usando solo Python.
- El modelo recibe la descripción de `fetch_fetch` en inglés, tal como la escribió su autor.

### STEP 4 — Conectarte a un servidor remoto (unos 5 minutos)

Conéctate por URL al servidor MCP que aloja AWS y comprueba que el agente puede usarlo.

1. Abre `app/mcp_servers.json`. Añade una coma después de la llave de cierre de `fetch` y agrega la línea de `"aws"`.

```json
{
  "mcpServers": {
    "glossary": {
      "command": "uv",
      "args": ["run", "python", "-m", "app.mcp_server"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch==2026.11.11", "--no-readability-js"]
    },
    "aws": {"url": "https://knowledge-mcp.global.api.aws"}
  }
}
```

2. Ejecuta el primer comando. Busca `[server] aws: conexión a la URL` y las herramientas cuyo nombre empieza por `aws_`.
3. Haz la pregunta con el segundo comando. Busca una herramienta `aws_` en la línea `[tool call]`.

```bash
uv run python -m app.mcp_agent --list-tools
uv run python -m app.mcp_agent --trace "Consulta la documentación de AWS y explica en dos líneas el control de versiones de Amazon S3."
```

El primer comando comienza con estas tres líneas.

```text
[server] glossary: inicio mediante el comando (uv run python -m app.mcp_server)
[server] fetch: inicio mediante el comando (uvx mcp-server-fetch==2026.11.11 --no-readability-js)
[server] aws: conexión a la URL (https://knowledge-mcp.global.api.aws)
```

AWS ya ejecuta el servidor. El agente se conecta directamente a su URL y envía la pregunta a AWS.

### Qué comprobar antes de añadir herramientas externas

En STEP 3 y STEP 4 usaste servidores de otros proveedores añadiendo unas pocas líneas al archivo de configuración. Comprueba primero lo siguiente.

1. **Quién proporciona el servidor.** Identifica al proveedor y dónde se publica el código fuente. El repositorio de MCP ofrece fetch. AWS ofrece AWS Knowledge. Añade servidores cuyo origen puedas verificar.
2. **Qué riesgos están documentados.** Lee los avisos y el comportamiento predeterminado en el README o el sitio oficial. El README de fetch describe el riesgo de seguridad asociado al acceso a IP internas. En los servidores remotos, los datos que entregas a una herramienta se envían al proveedor.

Los valores predeterminados de fetch protegen los recursos internos y respetan las reglas de los sitios sobre la descarga automatizada.

| Comportamiento predeterminado | Opción |
|---|---|
| Omite direcciones privadas como `localhost` y redes internas | `--allow-private-ips` permite acceder a ellas |
| Omite páginas cuya descarga automatizada está prohibida en `robots.txt` | `--ignore-robots-txt` permite acceder a esas páginas |
| Recupera las demás páginas de cualquier host | `--allowed-hosts` limita los hosts accesibles |

Comprueba quién ofrece el servidor y los riesgos que documenta antes de añadirlo, incluidos los servidores del repositorio de MCP.

### STEP 5 — Entregar y detener Codespaces (unos 3 minutos)

Registra tus resultados en `answer.md`, abre un PR y detén el Codespace.

1. Abre `lectures/06/answer.md`. Pega el nombre de la herramienta de STEP 1 y las líneas `[tool call]` de STEP 2 a STEP 4, con los nombres y argumentos tal como se muestran.
2. Haz commit y push.

```bash
git add -A
git commit -m "Práctica de la clase 06"
git push -u origin lec06
```

3. En GitHub, abre un PR de `lec06` a `main` en tu fork. Comprueba que el repositorio base sea tu fork.
4. En la esquina inferior izquierda, selecciona **Codespaces** y luego **Stop Current Codespace**.

Ejemplo de lo que puedes escribir en `answer.md`.

```text
- Nombre de la herramienta en STEP 1 — glossary_search_glossary
- STEP 2 [tool call] — glossary_search_glossary({'query': '3 niveles'})
- STEP 3 [tool call] — fetch_fetch({'url': 'https://…'})
- STEP 4 [tool call] — aws_… (Pega la línea tal como aparece)
```

Si no llegaste a completar STEP 4, entrega lo que hayas terminado y sube el trabajo posterior a la misma rama.

### Solución de problemas

Si el problema persiste, comparte el síntoma y el mensaje que aparece en el chat.

| Síntoma | Qué hacer |
|---|---|
| `No module named app.mcp_agent` | Actualiza `main` según la preparación. Ejecuta `git switch lec06` y luego `git merge main` |
| «No se pudo leer app/mcp_servers.json» | Cerca de la línea indicada, comprueba que haya comas entre los servidores y elimina cualquier coma sobrante después del último |
| «No se pudo conectar con un servidor MCP» | Comprueba el comando o la URL en `app/mcp_servers.json` |
| El agente omite fetch al recibir una URL | Añade una línea a `INSTRUCTIONS` en `app/mcp_agent.py` que indique que use fetch para leer las URL recibidas |
| Falla la conexión después de añadir `aws` | Comprueba la URL. Si hay un límite de solicitudes, espera aproximadamente un minuto y vuelve a intentarlo |
| Se alcanzó el límite de solicitudes | Espera aproximadamente un minuto y repite el comando |
| Falta `GEMINI_API_KEY` | Regístrala como secreto de Codespaces según la clase 01 y reinicia Codespaces |

## Tarea (completa un nivel)

| Nivel | Actividad |
|---|---|
| Básico | Expón `get_lecture_summary` en el servidor del glosario editando `app/mcp_server.py`. Conserva el agente tal como está y comprueba que la herramienta aparezca en la lista y se invoque al hacer una pregunta |
| Implementación | Añade al servidor MCP tu herramienta `make_quiz` de la clase 03 o crea otra. Devuelve un mensaje claro si un argumento está fuera de rango y observa cómo lo recibe el modelo |
| Avanzado | Consulta la documentación oficial de un programa que uses, como Claude Code, Codex o Gemini CLI, para ver cómo configura los servidores MCP. Si no tienes preferencia, usa VS Code. Compara su configuración con `app/mcp_servers.json` |

### Nivel básico

| Componente | Archivo |
|---|---|
| Servidor | Edita `app/mcp_server.py`, que determina qué herramientas se ofrecen |
| Agente | Conserva `app/mcp_servers.json` y `app/mcp_agent.py` tal como están |

1. Abre `app/mcp_server.py`. Añade la última línea del ejemplo bajo el comentario `TODO` y guarda el archivo.

   ```python
   server.tool()(tools.search_glossary)

   # TODO(Tarea básica): expón también get_lecture_summary
   server.tool()(tools.get_lecture_summary)
   ```

2. Ejecuta `git status`. Si hiciste commit del trabajo de la práctica en STEP 5, `app/mcp_server.py` debe ser el único archivo modificado.
3. Comprueba que `glossary_get_lecture_summary` aparezca en la lista.
4. Pregunta qué se aprende en la clase 02 y comprueba que el agente llame a la nueva herramienta.
5. Ejecuta `uv run pytest -q` y comprueba que todas las pruebas pasen.

```bash
git status
uv run python -m app.mcp_agent --list-tools
uv run python -m app.mcp_agent --trace "¿Qué aprenderemos en la clase 02?"
uv run pytest -q
```

Cada vez que se inicia, el agente solicita al servidor sus herramientas. Así descubre la herramienta que acabas de añadir.

### Nivel de implementación

1. Expón en `app/mcp_server.py` la herramienta `make_quiz` de la clase 03, como en el nivel básico. Si necesitas crear otra, define una función en ese archivo y añade `@server.tool()` justo encima.
2. Usa `return` para devolver un mensaje claro si un argumento está fuera de rango, como el número de una clase que no existe.
3. Haz una pregunta que produzca un argumento fuera de rango y revisa `--trace`.

```bash
uv run python -m app.mcp_agent --trace "Prepara un cuestionario de la clase 99."
```

- El mensaje de `return` aparece en `[tool return]` y se entrega al modelo.
- Una excepción de `raise` aparece en `[tool error]`. Compara qué recibe el modelo en cada caso.

### Nivel avanzado

1. Elige un programa que ya uses, como Claude Code, Codex o Gemini CLI. Si ninguno te sirve, elige VS Code. Para esta investigación basta con consultar la documentación.
2. Busca en su documentación oficial cómo configurar servidores MCP.
3. Compara el procedimiento con `app/mcp_servers.json` y anota las diferencias.

| Pregunta | Qué revisar |
|---|---|
| ¿Dónde se escribe la configuración? | Nombre y ubicación del archivo o comando de registro |
| ¿Cómo se inicia un servidor mediante un comando? | El equivalente de `"command"` |
| ¿Cómo se conecta por URL? | El equivalente de `"url"` |
| ¿Dónde se aplica la configuración? | En un solo proyecto o en todos |

Anota también la fecha de consulta y la URL de la documentación oficial. El procedimiento puede cambiar.

### Entrega de la tarea

En la sección Tarea de `lectures/06/answer.md`, escribe el nivel, lo que hiciste, los resultados y tus observaciones o preguntas. Sube los cambios a la misma rama `lec06`. Puedes usar herramientas de IA. Registra lo que hayas comprobado tú.

## Referencias

- [Sitio oficial de MCP](https://modelcontextprotocol.io/)
- [Cliente MCP de Pydantic AI](https://pydantic.dev/docs/ai/mcp/client/)
- [SDK de Python de MCP para crear servidores](https://github.com/modelcontextprotocol/python-sdk)
- [Servidores MCP públicos](https://github.com/modelcontextprotocol/servers)
- [README del servidor fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)
- [Servidor MCP AWS Knowledge](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server)
- [Usar servidores MCP en VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers)
