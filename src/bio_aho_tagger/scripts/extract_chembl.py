from sqlalchemy import create_engine, text
import os, csv


# DB URI env variable in SQLAlchemy format
db_uri = os.getenv("DB_URI")
engine = create_engine(db_uri)

# union drops duplicates between 2 queries.
query = """
SELECT ms.SYNONYMS, cs.canonical_smiles, md.max_phase, 1 AS rank_priority
FROM COMPOUND_STRUCTURES cs
JOIN MOLECULE_SYNONYMS ms ON cs.MOLREGNO = ms.MOLREGNO
JOIN MOLECULE_DICTIONARY md ON cs.MOLREGNO = md.MOLREGNO
WHERE LENGTH(ms.SYNONYMS) > 3

UNION

SELECT md.pref_name AS SYNONYMS, cs.CANONICAL_SMILES, md.max_phase, 2 AS rank_priority
FROM COMPOUND_STRUCTURES cs
JOIN MOLECULE_DICTIONARY md ON cs.MOLREGNO = md.MOLREGNO
WHERE LENGTH(md.pref_name) > 3

ORDER BY max_phase ASC NULLS FIRST, rank_priority ASC
"""
with engine.connect() as conn:
    res = conn.execute(text(query))

    with open("chembl_smiles.tsv", "w", newline="") as file:
        writer = csv.writer(file, delimiter="\t")

        for row in res:
            writer.writerow(row[:2])