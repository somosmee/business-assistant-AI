'''
 PREPROCESSING TEXT
'''
import unicodedata
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize


class Preprocess:

    stemmer = RSLPStemmer()

    @staticmethod
    def normalize(message):
        normalized = unicodedata.normalize('NFKD', message).encode(
            'ASCII',
            'ignore').decode('utf-8')

        return normalized.lower()

    @staticmethod
    def stem(message):
        words = word_tokenize(message)
        words = [Preprocess.stemmer.stem(word) for word in words]
        return ' '.join(words)

    @staticmethod
    def remove_stopwords(message):
        blacklist = set(stopwords.words('portuguese') + list(punctuation))
        clean_words = [word for word in word_tokenize(message) if word not in blacklist]
        return ' '.join(clean_words)

    @staticmethod
    def preprocess_message(message):
        message = Preprocess.normalize(message)
        message = Preprocess.remove_stopwords(message)
    #     message = stem(message)
        return message

    @staticmethod
    def preprocess(df, column_in='message', column_out='message_clean'):
        df[column_out] = df[column_in].apply(
            lambda message: Preprocess.preprocess_message(message))
