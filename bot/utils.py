from collections import defaultdict

import fitz


def to_float(string):
        if ',' not in string:
            return float(string)
        string = string.replace(',', '.')
        return float(string)


def get_data_from_food_report(path):
    nutrients = defaultdict(None)
    error_pdf = 'Incorrect pdf-file.'

    try:
        with fitz.open(path) as pdf:
            last_page = pdf.loadPage(-1)
            text = last_page.getText('text').strip()
    except RuntimeError:
        raise ValueError('Arg "path" must point to pdf-file.')

    data = text.split('\n')
    total_indexes = data[-1:-11:-1]
    total_indexes.reverse()

    if not total_indexes or len(total_indexes) != 10:
        raise ValueError(error_pdf)

    try:
        total_indexes = list(map(to_float, total_indexes))
    except ValueError:
        raise ValueError(error_pdf)

    nutrients['proteins'] = total_indexes[6]
    nutrients['fats'] = total_indexes[1]
    nutrients['carbohydrates'] = total_indexes[3]
    nutrients['calories'] = total_indexes[0]
    nutrients['cellulose'] = total_indexes[4]

    return nutrients
