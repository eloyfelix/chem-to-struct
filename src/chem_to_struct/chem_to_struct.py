import importlib.resources
import pickle

stop_chars = [" ", ",", "."]

with importlib.resources.open_binary('chem_to_struct.data', 'automaton.pkl') as file:
    automaton = pickle.load(file)

def name_to_structure(name):
    try:
        structure = automaton.get(name)
    except:
        structure = None
    return structure


def extract_entities(text):
    chemicals = []
    for end_index, (insert_order, original_value) in automaton.iter_long(text.lower()):
        start_index = end_index - len(original_value[0]) + 1
        if end_index + 1 <= len(text):
            if (end_index + 1 == len(text)) or (text[end_index + 1] in stop_chars):
                if start_index == 0 or text[start_index - 1] in stop_chars:
                    chemicals.append(
                        (start_index, end_index + 1, (insert_order, original_value))
                    )
    return chemicals
