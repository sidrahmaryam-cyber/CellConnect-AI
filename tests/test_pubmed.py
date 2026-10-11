
from unittest.mock import patch

from src.pubmed import search_pubmed


@patch("src.pubmed.Entrez.read")
@patch("src.pubmed.Entrez.efetch")
@patch("src.pubmed.Entrez.esearch")
def test_search_pubmed_no_results(
    mock_esearch, mock_efetch, mock_read
):
    mock_read.return_value = {"IdList": []}

    result = search_pubmed("test query")

    assert result == []
    mock_efetch.assert_not_called()
