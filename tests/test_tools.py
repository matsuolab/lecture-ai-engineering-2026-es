"""Pruebas de herramientas (sin LLM ni clave API)."""

import json

from app import tools


def test_glossary_ids_are_unique_and_related_links_exist():
    terms = tools.load_glossary()
    ids = [t["id"] for t in terms]
    assert len(ids) == len(set(ids))
    for t in terms:
        for r in t["related"]:
            assert r in ids, f"ID inexistente en related de {t['id']}: {r}"


def test_search_finds_term_by_name_and_alias():
    for query in ["LoRA", "lora", "Low-Rank Adaptation"]:
        hits = json.loads(tools.search_glossary(query))
        assert hits[0]["term"] == "LoRA", query


def test_search_finds_course_specific_term():
    hits = json.loads(tools.search_glossary("lecNN-start"))
    assert hits[0]["term"] == "etiqueta lecNN-start"


def test_search_limits_number_of_results():
    hits = json.loads(tools.search_glossary("agente"))
    assert 1 <= len(hits) <= tools.MAX_RESULTS


def test_search_reports_not_found():
    assert "No se ha encontrado" in tools.search_glossary("término inexistente xyz")


def test_lecture_summary():
    assert "agente" in tools.get_lecture_summary(3)
    assert "Todavía no hay" in tools.get_lecture_summary(99)


def test_default_question_of_lecture1_is_answerable_from_glossary():
    """La pregunta predeterminada de Lecture 01 (app.ask) puede responderse correctamente con el glosario mediante el agente de Lecture 03."""
    from app.ask import DEFAULT_QUESTION

    assert "3 niveles" in DEFAULT_QUESTION
    hits = json.loads(tools.search_glossary("3 niveles"))
    assert hits[0]["term"] == "3 niveles de las tareas"
