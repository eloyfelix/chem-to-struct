from utils import download_file
import ahocorasick
import pickle
import gzip
import re


def parse_uniprot_dat(filepath):
    """Parse the UniProt .dat.gz file to extract human proteins."""
    with gzip.open(filepath, "rt") as file:
        proteins = []
        protein = {}
        is_human = False

        for line in file:
            # get the uniprot accession
            if line.startswith("AC"):
                # primary accession (first one before the semicolon)
                accessions = line.split()[1].strip(";")
                if protein and is_human:
                    proteins.append(protein)
                protein = {
                    "accession": accessions,
                    "preferred_name": "",
                    "synonyms": [],
                }
                is_human = False

            # organism (OS)
            if line.startswith("OS") and "Homo sapiens" in line:
                is_human = True
            # taxonomy id (OX)
            if line.startswith("OX") and "9606" in line:
                is_human = True

            # preferred name (RecName)
            # strip references
            recname_match = re.match(r"DE\s+RecName:\s+Full=(.+);", line)
            if recname_match:
                protein["preferred_name"] = re.sub(
                    r"\{.*?\}", "", recname_match.group(1)
                ).strip()

            # synonyms (AltName)
            # strip references
            altname_match = re.match(r"DE\s+AltName:\s+Full=(.+);", line)
            if altname_match:
                protein["synonyms"].append(
                    re.sub(r"\{.*?\}", "", altname_match.group(1)).strip()
                )

        # last one
        if protein and is_human:
            proteins.append(protein)

    return proteins


def main():

    url = "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz"
    filename = "uniprot_sprot.dat.gz"

    download_file(url, filename)
    human_proteins = parse_uniprot_dat(filename)

    automaton = ahocorasick.Automaton()

    for prot in human_proteins:
        acc = prot["accession"]
        pref_name = prot["preferred_name"]

        for s in prot["synonyms"]:
            syn = s.lower()
            automaton.add_word(syn, (syn, (pref_name, "Protein", f"uniprot:{acc}")))

    automaton.make_automaton()

    with open("swissprot_human.pkl", "wb") as file:
        pickle.dump(automaton, file)


if __name__ == "__main__":
    main()
