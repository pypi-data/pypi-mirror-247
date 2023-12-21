__all__ = ("update_dict",)

def update_dict(d1: dict, d2: dict):
    """
    Updates dictionary 1 with dictionary 2 without overwriting the sub dictionaries.

    Stolen from https://stackoverflow.com/questions/22093793/generic-way-of-updating-python-dictionary-without-overwriting-the-subdictionarie
    """
    d1_copy = d1.copy()
    for key in d2:

        if key in d1:

            if isinstance(d1_copy[key], dict):
                #d1_copy[key].update(d2[key])
                d1_copy[key] = update_dict(d1_copy[key], d2[key])
            else:
                d1_copy[key] = d2[key]

        else:
            d1_copy[key] = d2[key]

    return d1_copy