


def str_list_to_json(txt: str) -> str:
    #
    replacements: dict[str, str] = {
        "None": "null",
        "False": "false",
        "True": "true",
        "'": "\""
    }
    #
    for r, v in replacements.items():
        #
        txt = txt.replace(r, v)
    #
    return txt


