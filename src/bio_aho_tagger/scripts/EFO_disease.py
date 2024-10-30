from utils import download_file
from collections import defaultdict
from rdflib import Graph
import ahocorasick
import pickle


def parse_efo_diseases(filepath):
    g = Graph()
    g.parse(filepath, format="xml")

    # Query for disease terms (EFO_0000408), including exact synonyms
    query = """
        SELECT ?term ?label ?exactSynonym WHERE {
            ?term rdfs:subClassOf* <http://www.ebi.ac.uk/efo/EFO_0000408> .
            ?term rdfs:label ?label .
            OPTIONAL { ?term <http://www.geneontology.org/formats/oboInOwl#hasExactSynonym> ?exactSynonym . }
        }
    """

    results = g.query(query)
    # init a dictionary to store results grouped by term
    diseases = defaultdict(lambda: {"label": None, "synonyms": defaultdict(list)})

    for row in results:
        term_uri = str(row.term)
        diseases[term_uri]["label"] = str(row.label)

        if row.exactSynonym:
            diseases[term_uri]["synonyms"]["Exact"].append(str(row.exactSynonym))
    return diseases


def main():

    url = "https://github.com/EBISPOT/efo/releases/download/current/efo.owl"
    filename = "efo.owl"

    download_file(url, filename)
    diseases = parse_efo_diseases(filename)

    automaton = ahocorasick.Automaton()

    for term_uri, data in diseases.items():
        if not isinstance(term_uri, str):
            continue
        o_id = ":".join(term_uri.split("/")[-1].split("_"))
        label = data["label"]
        for s in data["synonyms"]["Exact"]:
            syn = s.lower()
            automaton.add_word(syn, (syn, (label, "Disease", o_id)))

    automaton.make_automaton()

    with open("efo_disease.pkl", "wb") as file:
        pickle.dump(automaton, file)


if __name__ == "__main__":
    main()
