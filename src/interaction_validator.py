
import omnipath as op


# Human UniProt IDs for the test pair.
# We will extend this mapping as needed.
UNIPROT_IDS = {
    "CXCL12": "P48061",
    "CXCR4": "P61073",
}


def validate_interaction(ligand: str, receptor: str) -> dict:
    """Validate ligand/receptor roles and curated pair evidence."""

    ligand = ligand.upper()
    receptor = receptor.upper()

    # Check ligand and receptor annotations.
    annotations = op.requests.Intercell.get()

    ligand_rows = annotations[
        (annotations["genesymbol"].str.upper() == ligand)
        & (annotations["category"].str.lower() == "ligand")
        & annotations["transmitter"]
    ]

    receptor_rows = annotations[
        (annotations["genesymbol"].str.upper() == receptor)
        & (annotations["category"].str.lower() == "receptor")
        & annotations["receiver"]
    ]

    role_check_passed = (
        not ligand_rows.empty and not receptor_rows.empty
    )

    # Check whether the specific pair exists in curated interactions.
    ligand_id = UNIPROT_IDS.get(ligand)
    receptor_id = UNIPROT_IDS.get(receptor)

    pair_found = None
    evidence_sources = None
    references = None

    if ligand_id and receptor_id:
        pair_found = False
        interactions = op.interactions.LigRecExtra.get()

        pair_rows = interactions[
            (interactions["source"] == ligand_id)
            & (interactions["target"] == receptor_id)
        ]

        pair_found = not pair_rows.empty

        if pair_found:
            evidence_sources = pair_rows.iloc[0]["sources"]
            references = pair_rows.iloc[0]["references"]

    return {
        "ligand": ligand,
        "receptor": receptor,
        "ligand_annotated": not ligand_rows.empty,
        "receptor_annotated": not receptor_rows.empty,
        "role_check_passed": role_check_passed,
        "pair_found": pair_found,
        "pair_check_passed": pair_found,
        "evidence_sources": evidence_sources,
        "references": references,
        "pair_validation_status": (
        "confirmed" if pair_found is True
        else "not_found" if pair_found is False
        else "not_checked"  
            ),
        "validation_source": "OmniPath Intercell + LigRecExtra",
    }


if __name__ == "__main__":
    print(validate_interaction("CXCL12", "CXCR4"))
