from spacy.lang.pt import Portuguese
from spacy.pipeline import EntityRuler

# local
from meebot.regex import months_regex


class SaleNER:
    '''
     NER - Named Entity Recognition Approaches created by Mee 🤖🔮💜
     Author: Guilherme Kodama 07/2020
    '''

    def __init__(self):
        self.nlp = Portuguese()
        self.ruler = EntityRuler(self.nlp)

        # custom pattern for entity recognition
        self.patterns = [
            {
                'label': 'DATE', 'pattern':
                [    # this will run per token and check the token sequence
                     # to match the rules
                    {'TEXT': {"REGEX": "[uú]ltimo"}},
                    {'TEXT': {"REGEX": "m[êe]s"}},
                ],
                'id': 'date'
            },
            {
                'label': 'DATE', 'pattern':
                [
                    {'TEXT': {"REGEX": "[uú]ltimo"}},
                    {'TEXT': {"REGEX": r"\d"}},
                    {'TEXT': {"REGEX": "m[êe]s"}},
                ],
                'id': 'date'
            },
            {
                'label': 'DATE', 'pattern':
                [
                    {'TEXT': {"REGEX": months_regex}}
                ],
                'id': 'date'
            }, {
                'label': 'DATE', 'pattern':
                [
                    {'TEXT': {"REGEX": "(hoje|ontem)"}}
                ],
                'id': 'date'
            }, {
                'label': 'DATE', 'pattern':
                [
                    {'TEXT': {"REGEX": r"\d\d/\d\d/\d\d\d\d"}}
                ],
                'id': 'date'
            }
        ]

        self.ruler.add_patterns(self.patterns)
        self.nlp.add_pipe(self.ruler)

    def recognize(self, message):
        doc = self.nlp(message)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
