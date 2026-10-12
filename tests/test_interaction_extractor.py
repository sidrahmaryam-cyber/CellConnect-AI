
from unittest.mock import patch

from src.interaction_extractor import extract_interactions


@patch("src.interaction_extractor.ollama.chat")
def test_extract_interaction(mock_chat):
    mock_chat.return_value = {
        "message": {
            "content": (
                '{"ligand": "CXCL12", "receptor": "CXCR4", '
                '"sender_cell": "Endothelial cells", '
                '"receiver_cell": "Immune cells", '
                '"evidence": "CXCL12 binds to CXCR4."}'
            )
        }
    }

    result = extract_interactions(
        "Endothelial cells release CXCL12, which binds to CXCR4."
    )

    assert len(result) == 1
    assert result[0]["ligand"] == "CXCL12"
    assert result[0]["receptor"] == "CXCR4"


@patch("src.interaction_extractor.ollama.chat")
def test_extract_no_interactions(mock_chat):
    mock_chat.return_value = {
        "message": {"content": "[]"}
    }

    result = extract_interactions("Cells communicate in complex ways.")

    assert result == []
