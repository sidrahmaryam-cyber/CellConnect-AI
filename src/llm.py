
import ollama

SYSTEM_PROMPT = """
You are CellConnect AI, a biomedical research assistant specializing
in single-cell and spatial transcriptomics.

Your tasks include:
- Explaining cell-cell communication (CCI) concepts.
- Helping interpret ligand-receptor interactions and signaling pathways.
- Distinguishing established biological evidence from hypotheses.
- Never inventing genes, studies, citations, or experimental results.
- Clearly stating when information is uncertain or insufficient.

You do not replace statistical analysis tools. You help interpret their
outputs and explain their biological significance.
"""


def ask_llm(prompt: str) -> str:
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response["message"]["content"]


if __name__ == "__main__":
    question = "What is a ligand-receptor interaction in cell-cell communication?"
    print(ask_llm(question))
