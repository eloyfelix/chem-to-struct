import importlib.resources
import pickle


def merge_results(*lists):
    """
    Merge results from different automatons keeping the longest match when there are overlaps.

    disease_res = [
        (0, 6, ('cancer', 'disease', 'MONDO:0004992')),
        (0, 11, ('lung cancer', 'disease', 'MONDO:0005070'))
    ]
    tissue_res = [
        (0, 4, ('lung', 'tissue', 'UBERON:0002048')),
        (20, 25, ('heart', 'tissue', 'UBERON:0000948'))
    ]
    merge_results(disease_res, tissue_res)

    [
        (0, 11, ('lung cancer', 'disease', 'MONDO:0005070')),  # Only "lung cancer" kept for disease_res
        (20, 25, ('heart', 'tissue', 'UBERON:0000948'))        # "lung" is removed for tissue_res
    ]
    """
    all_matches = []
    for automaton_matches in lists:
        for start, end, (term, entity_type, entity_id) in automaton_matches:
            all_matches.append((start, end, term, entity_type, entity_id))

    # Sort matches by start position, prioritizing longer matches in case of overlap
    all_matches.sort(key=lambda x: (x[0], -(x[1] - x[0])))

    filtered_matches = []
    current_longest = None
    for start, end, term, entity_type, entity_id in all_matches:
        if current_longest and start < current_longest[1]:
            # Skip if this match overlaps with the current longest
            continue
        # Otherwise, add the match and update the current longest
        filtered_matches.append((start, end, (term, entity_type, entity_id)))
        current_longest = (start, end)

    return filtered_matches


class BioAhoTagger:

    stop_chars = [" ", ",", ".", "\n"]

    def __init__(self, file_path=None):
        self.automaton = self.load_automaton(file_path)

    def load_automaton(self, file_path):
        if file_path is None:
            # Load from package resource
            with importlib.resources.open_binary(
                "bio_aho_tagger.data", "chembl_smiles.pkl"
            ) as file:
                return pickle.load(file)
        else:
            # load from external file
            with open(file_path, "rb") as file:
                return pickle.load(file)

    def get(self, name):
        return self.automaton.get(name.lower(), None)

    def extract_entities(self, text):
        entities = []
        for end_index, original_value in self.automaton.iter_long(text.lower()):
            start_index = end_index - len(original_value[0]) + 1
            if end_index + 1 <= len(text):
                if (end_index + 1 == len(text)) or (
                    text[end_index + 1] in self.stop_chars
                ):
                    if start_index == 0 or text[start_index - 1] in self.stop_chars:
                        entities.append((start_index, end_index + 1, (original_value)))
        return entities
