import re

UNIT_ABBR_MAP = {
    'tsp.': 'tsp',
    'tbsp.': 'tbsp',
    'fl. oz.': 'fl oz',
    'gal.': 'gal',
    'in.':  '\"',
    'lb.': 'lb',
    'oz.':  'oz',
    'pt.':  'pt',
    'qt.':  'qt',
}


class TextNormalizationUtils:
    def __init__(self):
        self.escaped = {re.escape(key): value for key, value in UNIT_ABBR_MAP.items()}
        self.pattern = re.compile("|".join(self.escaped.keys()), re.M | re.I)
        self.replacer = lambda match: UNIT_ABBR_MAP[match.group(0)]
        self.sub = lambda string: self.pattern.sub(self.replacer, string.lower())


    def normalize_unit_abbreviations(self, input_text):
        return self.sub(input_text)

