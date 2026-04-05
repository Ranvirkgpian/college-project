import pytest
from unittest.mock import patch
from src.evaluator import run_llm_judge, evaluate_response

def test_run_llm_judge_success():
    mock_response = type('MockResponse', (), {
        'choices': [
            type('MockChoice', (), {
                'message': type('MockMessage', (), {'content': '{"passed": true, "reasoning": "Looks good."}'})
            })
        ]
    })

    with patch('src.evaluator.completion', return_value=mock_response):
        result = run_llm_judge("Q?", "A", "Expected", "fake-model")
        assert result["passed"] == True
        assert result["reasoning"] == "Looks good."

def test_run_llm_judge_malformed_json():
    mock_response = type('MockResponse', (), {
        'choices': [
            type('MockChoice', (), {
                'message': type('MockMessage', (), {'content': 'Not JSON'})
            })
        ]
    })

    with patch('src.evaluator.completion', return_value=mock_response):
        result = run_llm_judge("Q?", "A", "Expected", "fake-model")
        assert result["passed"] == False
        assert "malformed JSON" in result["reasoning"]

def test_evaluate_response_mock_judge():
    test_case = {"input": "Q?", "expected_behavior": "Expected"}
    result = evaluate_response("Answer", 1.5, test_case, "mock")

    assert result["passed"] == True
    assert result["response_time"] == 1.5
    assert result["llm_judge"]["passed"] == True
    assert "Mock judge automatically passes" in result["llm_judge"]["reasoning"]

def test_evaluate_response_real_judge():
    test_case = {"input": "Q?", "expected_behavior": "Expected"}

    mock_llm_metrics = {"passed": False, "reasoning": "Failed to match behavior."}

    with patch('src.evaluator.run_llm_judge', return_value=mock_llm_metrics):
        result = evaluate_response("Answer", 2.0, test_case, "gpt-4o-mini")

        assert result["passed"] == False
        assert result["response_time"] == 2.0
        assert result["llm_judge"]["passed"] == False
