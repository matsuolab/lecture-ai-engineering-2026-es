"""Lecture 02, tarea avanzada: crear pares de preguntas y respuestas para SFT (JSONL) a partir del glosario.

Uso:
    uv run python scripts/make_sft_dataset.py > glossary_sft.jsonl

Sube el archivo generado a Colab y úsalo como datos de entrenamiento con LoRA.
Prueba a añadir otras formulaciones, crear preguntas con alias o reservar una parte para validación.
"""

import json
import sys
from pathlib import Path

GLOSSARY = Path(__file__).resolve().parent.parent / "data" / "glossary.json"
TEMPLATES = ["¿Qué es «{term}»?", "Explica brevemente qué es {term}."]


def main() -> None:
    terms = json.loads(GLOSSARY.read_text(encoding="utf-8"))["terms"]
    for t in terms:
        for template in TEMPLATES:
            record = {
                "messages": [
                    {"role": "user", "content": template.format(term=t["term"])},
                    {"role": "assistant", "content": t["definition"]},
                ]
            }
            sys.stdout.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
