
import pandas as pd

from src.interaction_validator import validate_interaction


def test_validate_known_ligand_receptor_pair(monkeypatch):
    annotations = pd.DataFrame([
        {
            "genesymbol": "CXCL12",
            "category": "ligand",
            "transmitter": True,
            "receiver": False,
        },
        {
            "genesymbol": "CXCR4",
            "category": "receptor",
            "transmitter": False,
            "receiver": True,
        },
    ])

    interactions = pd.DataFrame([
        {
            "source": "P48061",
            "target": "P61073",
            "sources": "CellPhoneDB;CellChatDB",
            "references": "12345678",
        },
    ])

    monkeypatch.setattr(
        "src.interaction_validator.op.requests.Intercell.get",
        lambda: annotations,
    )
    monkeypatch.setattr(
        "src.interaction_validator.op.interactions.LigRecExtra.get",
        lambda: interactions,
    )

    result = validate_interaction("CXCL12", "CXCR4")

    assert result["role_check_passed"] is True
    assert result["pair_found"] is True
    assert result["pair_check_passed"] is True
    assert result["pair_validation_status"] == "confirmed"
