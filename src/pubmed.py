
from Bio import Entrez


# NCBI requests an email to identify the application.
Entrez.email = "sidrah.maryam@gmail.com"


def search_pubmed(query: str, max_results: int = 5) -> list[dict]:
    """Search PubMed and return basic details for matching papers."""

    with Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results,
        sort="relevance",
    ) as handle:
        search_results = Entrez.read(handle)

    paper_ids = search_results["IdList"]

    if not paper_ids:
        return []

    with Entrez.efetch(
        db="pubmed",
        id=paper_ids,
        rettype="abstract",
        retmode="xml",
    ) as handle:
        papers = Entrez.read(handle)

    
    results = []

    for paper in papers["PubmedArticle"]:
        citation = paper["MedlineCitation"]
        article = citation["Article"]

        title = str(article.get("ArticleTitle", "No title"))
        abstract_parts = article.get("Abstract", {}).get("AbstractText", [])
        abstract = " ".join(str(part) for part in abstract_parts)

        journal = str(
            article.get("Journal", {}).get("Title", "Unknown journal")
        )

        pub_date = article.get("Journal", {}).get(
            "JournalIssue", {}
        ).get("PubDate", {})

        year = str(pub_date.get("Year", "Unknown year"))

        results.append({
            "title": title,
            "abstract": abstract,
            "pmid": str(citation["PMID"]),
            "journal": journal,
            "year": year,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{citation['PMID']}/",
        })

    return results



if __name__ == "__main__":
    papers = search_pubmed("single-cell ligand receptor cell communication")

    for paper in papers:
        print(f"\nTitle: {paper['title']}")
        print(f"PMID: {paper['pmid']}")
        print(f"Journal: {paper['journal']}")
        print(f"Year: {paper['year']}")
        print(f"URL: {paper['url']}")
        print(f"Abstract: {paper['abstract'][:300]}...")
