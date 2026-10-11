
from src.llm import ask_llm
from src.pubmed import search_pubmed


def answer_research_question(question: str) -> str:
    papers = search_pubmed(question, max_results=5)

    if not papers:
        return "No PubMed papers were found for this query."

    evidence = "\n\n".join(
        f"Title: {paper['title']}\n"
        f"Journal: {paper['journal']} ({paper['year']})\n"
        f"PMID: {paper['pmid']}\n"
        f"URL: {paper['url']}\n"
        f"Abstract: {paper['abstract']}"
        for paper in papers
    )


    prompt = f"""
Answer the biomedical research question using the PubMed evidence below.

Question: {question}

PubMed evidence:
{evidence}

Instructions:
- Base scientific claims on the provided evidence.
- Cite papers using their PMID and URL.
- Distinguish evidence from hypotheses.
- If the abstracts do not answer the question, say so.
- Do not invent findings or citations.
"""

    return ask_llm(prompt)


if __name__ == "__main__":
    question = "How do macrophages communicate with endothelial cells?"
    print(answer_research_question(question))
