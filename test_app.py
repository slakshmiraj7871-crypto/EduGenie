"""
Automated Test Suite for EduGenie Application
Tests FastAPI routing, error handling, parameter resolution, and quiz parsing.
"""

import pytest
from fastapi.testclient import TestClient
from main import app, EduGenieRequest
import quiz_module

client = TestClient(app)

def test_health_endpoint():
    """Verify system health endpoint returns operational metadata."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data
    assert "modules" in data
    assert "qa" in data["modules"]
    assert "explain" in data["modules"]
    assert "quiz" in data["modules"]

def test_home_page():
    """Verify HTML frontend is rendered with EduGenie branding."""
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text
    assert "Google Gemini Powered Learning Assistant" in response.text
    assert "taskSelect" in response.text

def test_request_model_parameter_resolution():
    """Verify EduGenieRequest resolves various input parameter field names."""
    req1 = EduGenieRequest(prompt="Test prompt")
    assert req1.resolve_text() == "Test prompt"

    req2 = EduGenieRequest(question="What is gravity?")
    assert req2.resolve_text() == "What is gravity?"

    req3 = EduGenieRequest(concept="Pythagoras Theorem")
    assert req3.resolve_text() == "Pythagoras Theorem"

    req4 = EduGenieRequest(topic="SQL")
    assert req4.resolve_text() == "SQL"

    req5 = EduGenieRequest(text="Passage text")
    assert req5.resolve_text() == "Passage text"

    req_empty = EduGenieRequest()
    assert req_empty.resolve_text() == ""

def test_empty_input_validation():
    """Verify 400 Bad Request is returned when required input is empty."""
    endpoints = ["/qa", "/explain", "/quiz", "/summarize", "/learn/recommendations"]
    for ep in endpoints:
        resp = client.post(ep, json={"prompt": ""})
        assert resp.status_code == 400, f"Expected 400 for empty input on {ep}"
        assert "detail" in resp.json()

def test_quiz_clean_json_block():
    """Verify clean_json_block strips fences, backticks, and extra prose."""
    # Test Markdown code fences
    raw_markdown = "```json\n[\n  {\"id\": 1, \"question\": \"Test?\"}\n]\n```"
    cleaned = quiz_module.clean_json_block(raw_markdown)
    assert cleaned.startswith("[")
    assert cleaned.endswith("]")

    # Test surrounding prose
    surrounded = "Here is your requested quiz:\n[\n  {\"id\": 1}\n]\nHope this helps!"
    cleaned = quiz_module.clean_json_block(surrounded)
    assert cleaned == "[\n  {\"id\": 1}\n]"

    # Test empty string
    assert quiz_module.clean_json_block("") == ""

def test_endpoint_mock_execution(monkeypatch):
    """Verify each endpoint integrates smoothly with the service layer."""
    # Mock generate_text in gemini_client
    monkeypatch.setattr(
        "gemini_client.generate_text",
        lambda prompt, system_prompt=None, json_mode=False: "Mocked AI Response"
    )

    # 1. QnA Endpoint
    resp_qa = client.post("/qa", json={"prompt": "Which is the largest ocean?"})
    assert resp_qa.status_code == 200
    assert "Mocked AI Response" in resp_qa.json()["result"]

    # 2. Explain Endpoint
    resp_explain = client.post("/explain", json={"prompt": "The Pythagoras Theorem"})
    assert resp_explain.status_code == 200
    assert "Mocked AI Response" in resp_explain.json()["result"]

    # 3. Summarize Endpoint
    resp_sum = client.post("/summarize", json={"prompt": "Long educational text..."})
    assert resp_sum.status_code == 200
    assert "Mocked AI Response" in resp_sum.json()["result"]

    # 4. Learning Path Endpoint
    resp_lp = client.post("/learn/recommendations", json={"prompt": "SQL"})
    assert resp_lp.status_code == 200
    assert "Mocked AI Response" in resp_lp.json()["result"]

def test_quiz_mock_execution(monkeypatch):
    """Verify quiz endpoint parses and validates 3 MCQs."""
    mock_json = """
    [
      {
        "id": 1,
        "question": "What is the capital of France?",
        "options": ["Paris", "Berlin", "Madrid", "Rome"],
        "answer": "Paris",
        "explanation": "Paris is the capital and largest city of France."
      },
      {
        "id": 2,
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars",
        "explanation": "Mars appears reddish due to iron oxide on its surface."
      },
      {
        "id": 3,
        "question": "What is H2O commonly known as?",
        "options": ["Salt", "Water", "Oxygen", "Hydrogen"],
        "answer": "Water",
        "explanation": "H2O consists of two hydrogen atoms and one oxygen atom forming water."
      }
    ]
    """
    monkeypatch.setattr(
        "gemini_client.generate_text",
        lambda prompt, system_prompt=None, json_mode=False: mock_json
    )

    resp_quiz = client.post("/quiz", json={"prompt": "General Science"})
    assert resp_quiz.status_code == 200
    data = resp_quiz.json()
    assert data["success"] is True
    assert len(data["quiz"]) == 3
    assert data["quiz"][0]["question"] == "What is the capital of France?"
    assert len(data["quiz"][0]["options"]) == 4
    assert data["quiz"][0]["answer"] == "Paris"
