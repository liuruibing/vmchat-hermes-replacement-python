import pytest

from scripts.mandate_risk_v2_omp_server import parse_assistant


def test_omp_adapter_preserves_json_text_and_real_usage():
    text, usage = parse_assistant({
        'content': [{'type': 'thinking', 'thinking': 'private'},
                    {'type': 'text', 'text': '{"complete":true}'}],
        'stopReason': 'stop',
        'usage': {'input': 20, 'cacheRead': 10, 'output': 5, 'totalTokens': 35},
    })
    assert text == '{"complete":true}'
    assert usage == {'prompt_tokens': 30, 'completion_tokens': 5, 'total_tokens': 35}


@pytest.mark.parametrize('reason', ['error', 'aborted', 'length'])
def test_omp_adapter_rejects_failed_or_truncated_answers(reason):
    with pytest.raises(RuntimeError, match='OMP_MODEL_FAILED'):
        parse_assistant({'stopReason': reason, 'content': [{'type': 'text', 'text': 'partial'}]})


def test_omp_adapter_does_not_treat_thinking_as_a_final_answer():
    with pytest.raises(RuntimeError, match='OMP_EMPTY_RESPONSE'):
        parse_assistant({'content': [{'type': 'thinking', 'thinking': 'not an answer'}]})
