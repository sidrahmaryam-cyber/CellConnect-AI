
from src.llm import SYSTEM_PROMPT


def test_system_prompt():
    assert "single-cell" in SYSTEM_PROMPT
    assert "Never inventing" in SYSTEM_PROMPT
