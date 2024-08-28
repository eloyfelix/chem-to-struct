import importlib.resources
import pickle


class ChemToStruct:

    stop_chars = [" ", ",", "."]

    def __init__(self, file_path=None):
        self.automaton = self.load_automaton(file_path)

    def load_automaton(self, file_path):
        if file_path is None:
            # Load from package resource
            with importlib.resources.open_binary(
                "chem_to_struct.data", "automaton.pkl"
            ) as file:
                return pickle.load(file)
        else:
            # Load from external file
            with open(file_path, "rb") as file:
                return pickle.load(file)

    def name_to_structure(self, name):
        return self.automaton.get(name, None)

    def extract_entities(self, text):
        chemicals = []
        for end_index, (insert_order, original_value) in self.automaton.iter_long(
            text.lower()
        ):
            start_index = end_index - len(original_value[0]) + 1
            if end_index + 1 <= len(text):
                if (end_index + 1 == len(text)) or (
                    text[end_index + 1] in self.stop_chars
                ):
                    if start_index == 0 or text[start_index - 1] in self.stop_chars:
                        chemicals.append(
                            (start_index, end_index + 1, (insert_order, original_value))
                        )
        return chemicals
