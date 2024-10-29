import ahocorasick
import pickle
import argparse
import csv


def main():

    parser = argparse.ArgumentParser(
        description="Create a dictionary file for chemicals/drugs."
    )
    parser.add_argument(
        "synonyms_filepath",
        type=str,
        help="Path to a headerless TSV file containing two columns: synonym and canonical_smiles.",
    )

    args = parser.parse_args()

    automaton = ahocorasick.Automaton()

    with open(args.synonyms_filepath, mode="r", newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter="\t")
        for idx, (synonym, smiles) in enumerate(csvreader):
            syn = synonym.lower()
            automaton.add_word(syn, (syn, (syn, "Chemical", smiles)))

    automaton.make_automaton()

    with open("chembl_smiles.pkl", "wb") as file:
        pickle.dump(automaton, file)


if __name__ == "__main__":
    main()
