# chem-to-struct

Simple dictionary based package using ChEMBL molecule synonyms to resolve chemical structures. Using [pyahocorasick](https://github.com/WojciechMula/pyahocorasick).

ChEMBL synonyms extracted using the following query on ChEMBL_34 SQLite dump:

```sql
SELECT ms.SYNONYMS, cs.canonical_smiles, md.max_phase, 1 AS rank_priority
FROM COMPOUND_STRUCTURES cs
JOIN MOLECULE_SYNONYMS ms ON cs.MOLREGNO = ms.MOLREGNO
JOIN MOLECULE_DICTIONARY md ON cs.MOLREGNO = md.MOLREGNO
WHERE LENGTH(ms.SYNONYMS) >= 3

UNION

SELECT md.pref_name AS SYNONYMS, cs.CANONICAL_SMILES, md.max_phase, 2 AS rank_priority
FROM COMPOUND_STRUCTURES cs
JOIN MOLECULE_DICTIONARY md ON cs.MOLREGNO = md.MOLREGNO
WHERE LENGTH(md.pref_name) >= 3

ORDER BY max_phase ASC NULLS FIRST, rank_priority ASC
```

## To use it

Pass a name and retrieve its structure (if available)

```python
from chem_to_struct import ChemToStruct

c2s = ChemToStruct()
# Or initialize with an external file
# extractor = ChemToStruct('/path/to/external/automaton.pkl')

structure = c2s.name_to_structure("aspirin")
```

Extract all entities found in a text

```python
from chem_to_struct import ChemToStruct

c2s = ChemToStruct()

text = "aspirin, paracetamol something, something else, paracetamolxxxxx, loloparacetamol something"
entities = c2s.extract_entities(text)
```
