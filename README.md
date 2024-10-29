# BioAhoTagger

Baseline dictionary based package to tag biological entities. Using [pyahocorasick](https://github.com/WojciechMula/pyahocorasick).

## To use it

Extract all entities found in a text

```python
from bio_aho_tagger import BioAhoTagger

bt = BioAhoTagger()

entities = bt.extract_entities(text)
```
