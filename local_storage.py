import json


def save_json_file(data, path: str):
    with open(path, "w") as j_file:
        json.dump(data, j_file)


def load_json_file(path: str):
    with open(path, "r", encoding='utf-8-sig') as file:
        data = json.load(file)

    updated_keys_data = {}

    for key in data:
        updated_keys_data[int(key)] = data[key]

    return updated_keys_data


def load_text_file(path: str):
    with open(path) as f:
        file_text = f.read()

    return file_text
