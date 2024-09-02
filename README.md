# BioAhoTagger

Baseline dictionary based package using MeSH to tag biological entities. Using [pyahocorasick](https://github.com/WojciechMula/pyahocorasick).

- pharmacologic actions (molecular mechanisms of action, physiological effects of drugs, therapeutic uses): MeSH tree code `D27.505`
- organisms: MeSH tree code `B`
- diseases: MeSH tree code `C`
- proteins: MeSH tree code `D12.776`
- tissues : MeSH tree code `A10`
- cells : MeSH tree code `A11`

## To use it

Extract all entities found in a text

```python
from bio_aho_tagger import BioAhoTagger

bt = BioAhoTagger()

entities = bt.extract_entities(text)
```
