
import json
import ollama
from src.llm import ask_llm


def extract_interactions(text: str) -> list[dict]:
    prompt = f"""
You are assisting with cell-cell communication research.

Extract candidate ligand-receptor interactions explicitly mentioned
in the text below.

Return only a JSON array. Each item must contain:
- ligand: ligand name
- receptor: receptor name
- sender_cell: sender cell type, or "Unknown"
- receiver_cell: receiver cell type, or "Unknown"
- evidence: short supporting phrase from the text

Rules:
- Do not invent genes, interactions, or cell types.
- Include only interactions explicitly supported by the text.
- If no specific ligand-receptor pair is stated, return [].
- These are extracted candidates, not experimentally validated results.

Text:
{text}
"""

    response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {"role": "user", "content": prompt}
    ],
    format="json",
    )["message"]["content"]
    
    try:
        result = json.loads(response)

        if isinstance(result, dict):
            result = [result]

    except json.JSONDecodeError:
        return []

    if not isinstance(result, list):
        return []

    required_keys = {
        "ligand", "receptor", "sender_cell", "receiver_cell", "evidence"
    }

    return [
        item for item in result
        if isinstance(item, dict) and required_keys.issubset(item.keys())
    ]


if __name__ == "__main__":
    sample_text = """
    Endothelial cells release CXCL12, which binds to CXCR4 on immune cells.
    """

    print(json.dumps(extract_interactions(sample_text), indent=2))
