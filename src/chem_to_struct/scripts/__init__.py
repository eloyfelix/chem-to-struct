import ahocorasick
import pickle
import argparse
import csv


def create_file():

    parser = argparse.ArgumentParser(
        description="Create a dictionary file for use with chem-to-struct."
    )
    parser.add_argument(
        "synonyms_filepath",
        type=str,
        help="Path to a headerless TSV file containing two columns: synonym and canonical_smiles.",
    )
    parser.add_argument(
        "--automaton_filename",
        type=str,
        help="Optional path to an external file specifying the name of the automaton file.",
        default="automaton.pkl",
    )

    args = parser.parse_args()

    automaton = ahocorasick.Automaton()

    with open(args.synonyms_filepath, mode="r", newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter="\t")
        for idx, (synonym, smiles) in enumerate(csvreader):
            automaton.add_word(synonym.lower(), (idx, (synonym.lower(), smiles)))

    automaton.make_automaton()

    with open(args.automaton_filename, "wb") as file:
        pickle.dump(automaton, file)
