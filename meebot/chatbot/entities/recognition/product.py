from string import punctuation
from nltk.corpus import stopwords
from spacy.lang.pt import Portuguese
from nltk.tokenize import word_tokenize
from nltk.metrics.distance import edit_distance
from sklearn.feature_extraction.text import CountVectorizer


class Preprocessing:
    def __init__(self):
        pass

    def remove_stop_words(self, message, tokenizer, tokenized=True):
        blacklist = set(stopwords.words('portuguese') + list(punctuation))
        tokens = []
        if tokenizer:
            tokens = tokenizer(message)
        else:
            tokens = word_tokenize(message)
        clean_words = [word for word in tokens if word not in blacklist]
        if tokenized:
            return clean_words
        else:
            return ' '.join(clean_words)


class ProductNER:
    '''
     NER - Named Entity Recognition Approaches created by Mee 🤖🔮💜
     Author: Guilherme Kodama 07/2020
    '''

    def __init__(self, corpus):
        self.nlp = Portuguese()
        self.vectorizer = CountVectorizer()
        self.preprocessing = Preprocessing()
        self.matrix = self.vectorizer.fit_transform(corpus)
        self.vocab = self.vectorizer.vocabulary_
        self.tokenizer = self.vectorizer.build_tokenizer()

    def recognize(self, message, algo='perfect_match', threshold=2):
        tokens = self.preprocessing.remove_stop_words(
            message,
            tokenizer=self.tokenizer)

        flag_tokens = {}

        for i, token in enumerate(tokens):

            if algo == 'perfect_match':
                if token in self.vocab:
                    flag_tokens[i] = i

            # Calculate the Levenshtein edit-distance
            # https://www.nltk.org/api/nltk.metrics.html#nltk.metrics.distance.edit_distance
            elif algo == 'edit_distance':
                for word in self.vectorizer.get_feature_names():
                    if edit_distance(token, word) <= threshold:
                        flag_tokens[i] = word

        if len(flag_tokens) == 0:
            return None

        return [(' '.join(
            [flag_tokens[key] for key in flag_tokens.keys()]),
            'PRODUCT')
            ]
