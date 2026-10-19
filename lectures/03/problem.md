# Lecture 03: ejercicios y tarea — crear un agente de apoyo al aprendizaje

## Objetivos de esta sesión

- Comprobar en tu propio código que un agente se compone de «modelo + bucle + herramientas»
- Identificar qué herramienta se ha llamado y con qué argumentos
- Añadir una herramienta

## Preparación

Si has terminado el trabajo de las sesiones anteriores, crea la rama `lec03` desde `main`.

```bash
git switch main && git switch -c lec03
```

Si no has terminado, puedes crear una rama desde el código inicial de esta sesión en el repositorio del curso (etiqueta `lec03-start`).

```bash
git remote -v                     # Si no existe upstream, añádelo con la siguiente línea
git remote add upstream https://github.com/matsuolab/lecture-ai-engineering-2026.git
git fetch upstream --tags
git switch -c lec03 lec03-start
```

## Ejercicios (30 minutos)

### 1. Hacer al agente la misma pregunta que en Lecture 01

```bash
uv run python -m app.agent "¿Qué es la «etiqueta lecNN-start» que se usa en el curso AIE2026?"
```

Compárala con la respuesta de `app.ask` en Lecture 01.

### 2. Leer las llamadas a herramientas

```bash
uv run python -m app.agent --trace "¿Cuál es la diferencia entre LoRA y QLoRA?"
```

En las líneas `[tool call]`, comprueba qué herramienta ha llamado el modelo y con qué argumentos. El campo `requests` de `[usage]` indica cuántas veces se ha llamado al LLM para responder a una pregunta.

### 3. Añadir una herramienta

Añade `make_quiz` a `app/tools.py` y regístrala en el lugar marcado como `TODO(Lecture 03: ejercicio)` de `app/agent.py`.

- Ejemplo: elige un término de la sesión indicada (`lecture: int`) y devuelve una pregunta del tipo «¿Qué significa este término?» junto con su respuesta
- Escribe en el docstring «cuándo y para qué se debe usar la herramienta» (el modelo lo lee para decidir si la utiliza)

```bash
uv run python -m app.agent --trace "Hazme una pregunta de repaso sobre el contenido de Lecture 02"
uv run pytest -q
```

### 4. Entregar el trabajo

Completa `lectures/03/answer.md` y crea un PR de `lec03` hacia `main` de tu propio fork.

## Tarea (basta con completar un nivel)

| Nivel | Contenido |
|---|---|
| Básico | Modifica `INSTRUCTIONS` o los docstrings de las herramientas y usa `--trace` para comparar y registrar cómo cambian las llamadas a herramientas y las respuestas |
| Implementación | Crea una herramienta `save_learning_log` que guarde un registro de aprendizaje en `learning_log/`. Pide confirmación al usuario antes de guardar (`requires_approval=True` de Pydantic AI). Escribe también pruebas con TestModel |
| Avanzado | Elige una opción. (a) Vuelve a crear el mismo agente con ADK de Google y compara la forma de escribirlo y de visualizarlo en `adk web`. (b) Ejecuta en Codespaces Pi, presentado en clase, y compara su prompt de sistema público con las `INSTRUCTIONS` de tu agente |

### Cómo realizar la opción avanzada (b)

Pi es un agente de programación capaz de leer y escribir archivos y ejecutar comandos; no pide confirmación cada vez que ejecuta una herramienta. Pruébalo dentro de Codespaces, en lugar de ejecutarlo en tu PC.

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
pi
```

- Gemini lee la variable de entorno `GEMINI_API_KEY`, así que puedes usar directamente el secret de Codespaces si ya lo tienes. Escribe `/model` dentro de Pi y selecciona un modelo de Gemini
- El nombre del paquete npm es `@earendil-works/pi-coding-agent` (`@mariozechner/...`, que aparece en artículos antiguos, es el nombre anterior)
- El prompt de sistema de Pi está en `packages/coding-agent/src/core/system-prompt.ts` del repositorio público https://github.com/earendil-works/pi. Compáralo con tus `INSTRUCTIONS` y observa qué incluye y qué omite
- Documentación oficial: https://github.com/earendil-works/pi/tree/main/packages/coding-agent/docs

## Referencias

- Pydantic AI: https://ai.pydantic.dev/
- ADK: https://google.github.io/adk-docs/
