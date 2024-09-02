import importlib.resources
import pickle


class BioAhoTagger:

    stop_chars = [" ", ",", ".", "\n"]

    def __init__(self, file_path=None):
        self.automaton = self.load_automaton(file_path)

    def load_automaton(self, file_path):
        if file_path is None:
            # Load from package resource
            with importlib.resources.open_binary(
                "bio_aho_tagger.data", "automaton.pkl"
            ) as file:
                return pickle.load(file)
        else:
            # Load from external file
            with open(file_path, "rb") as file:
                return pickle.load(file)

    def get(self, name):
        return self.automaton.get(name.lower(), None)

    def extract_entities(self, text):
        entities = []
        for end_index, original_value in self.automaton.iter_long(
            text.lower()
        ):
            start_index = end_index - len(original_value[0]) + 1
            if end_index + 1 <= len(text):
                if (end_index + 1 == len(text)) or (
                    text[end_index + 1] in self.stop_chars
                ):
                    if start_index == 0 or text[start_index - 1] in self.stop_chars:
                        entities.append(
                            (start_index, end_index + 1, (original_value))
                        )
        return entities
