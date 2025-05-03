import pytest
import responses
import json

from module import fetch_questions 

@responses.activate
def test_fetch_questions_success():
    mock_response = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677858242,
        "model": "gpt-4",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "1. What is Newton's First Law?\nA) Law of Inertia\nB) Law of Acceleration\nC) Law of Action-Reaction\nD) Law of Gravity\n\n2. What is Newton's Second Law?\nA) F = ma\nB) F = m/a\nC) F = a/m\nD) F = m²a\n\n3. What is Newton's Third Law?\nA) For every action, there is an equal and opposite reaction\nB) Objects at rest stay at rest\nC) Force equals mass times acceleration\nD) Gravity is proportional to mass\n\n4. The SI unit of force is:\nA) Joule\nB) Newton\nC) Watt\nD) Pascal\n\n5. An object's inertia depends on its:\nA) Volume\nB) Mass\nC) Density\nD) Weight"
                },
                "finish_reason": "stop",
                "index": 0
            }
        ],
        "usage": {
            "prompt_tokens": 13,
            "completion_tokens": 323,
            "total_tokens": 336
        }
    }
    responses.add(
        responses.POST,
        "https://api.openai.com/v1/chat/completions",
        json=mock_response,
        status=200
    )
    result = fetch_questions("dummy_api_key")
    try:
        assert "Newton's First Law" in result
        assert "Newton's Second Law" in result
        assert len(responses.calls) == 1
        request_body = json.loads(responses.calls[0].request.body)
        assert request_body["model"] == "gpt-4"
        assert request_body["messages"][0]["content"] == "Give 5 MCQs on Laws of Motion for Grade 9"
        assert responses.calls[0].request.headers["Authorization"] == "Bearer dummy_api_key"
        print("test_fetch_questions_success: PASSED")
    except AssertionError as e:
        print("test_fetch_questions_success: FAILED")
        raise

@responses.activate
def test_fetch_questions_api_error():
    responses.add(
        responses.POST,
        "https://api.openai.com/v1/chat/completions",
        json={"error": {"message": "Invalid API key"}},
        status=401
    )
    result = fetch_questions("invalid_api_key")
    try:
        assert result is None
        print("test_fetch_questions_api_error: PASSED")
    except AssertionError:
        print("test_fetch_questions_api_error: FAILED")
        raise

@responses.activate
def test_fetch_questions_parsing_error():
    responses.add(
        responses.POST,
        "https://api.openai.com/v1/chat/completions",
        json={"id": "chatcmpl-123", "choices": []},  # Malformed response
        status=200
    )
    result = fetch_questions("dummy_api_key")
    try:
        assert result is None
        print("test_fetch_questions_parsing_error: PASSED")
    except AssertionError:
        print("test_fetch_questions_parsing_error: FAILED")
        raise
