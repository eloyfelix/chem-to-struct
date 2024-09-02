from .xml_utils import parse_mesh
import ahocorasick
import pickle
import argparse


pharmacological_actions_tree = "D27.505"
proteins_tree = "D12.776"
tissues_tree = "A10"
cells_tree = "A11"
organisms_tree = "B"
diseases_tree = "C"


def create_file():

    parser = argparse.ArgumentParser(description="Create a dictionary file.")
    parser.add_argument(
        "mesh_path",
        type=str,
        help="Path to the MeSH XML desc.",
    )
    parser.add_argument(
        "--automaton_filename",
        type=str,
        help="Optional path to an external file specifying the name of the automaton file.",
        default="automaton.pkl",
    )

    args = parser.parse_args()

    automaton = ahocorasick.Automaton()

    descriptor_records = parse_mesh(args.mesh_path)
    for ds in descriptor_records:
        if ds.tree_numbers:
            if any(
                tn.startswith(pharmacological_actions_tree) for tn in ds.tree_numbers
            ):
                entity = "PharmacologicalAction"
            elif any(tn.startswith(proteins_tree) for tn in ds.tree_numbers):
                entity = "Protein"
            elif any(tn.startswith(tissues_tree) for tn in ds.tree_numbers):
                entity = "Tissue"
            elif any(tn.startswith(cells_tree) for tn in ds.tree_numbers):
                entity = "Cell"
            elif any(tn.startswith(organisms_tree) for tn in ds.tree_numbers):
                entity = "Organism"
            elif any(tn.startswith(diseases_tree) for tn in ds.tree_numbers):
                entity = "Disease"
            else:
                continue

            for con in ds.concepts:
                for term in con.terms:
                    tt = term.name.lower()
                    automaton.add_word(tt, (tt, (ds.name, entity, ds.ui)))

    automaton.make_automaton()

    with open(args.automaton_filename, "wb") as file:
        pickle.dump(automaton, file)
