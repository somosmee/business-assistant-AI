'''
 INTENT CLASSIFIER
'''
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from meebot.chatbot.preprocess import Preprocess
from sklearn.feature_extraction.text import TfidfVectorizer


class IntentClassifier:

    def __init__(self, df, model=''):
        self.df = df
        self.clf = MultinomialNB()
        self.vectorizer = TfidfVectorizer()

    '''
     VECTORIZE
    '''

    def vectorize(self, df, column='message'):
        X = self.vectorizer.fit_transform(df[column])
        return X

    def vectorize_message(self, message):
        return self.vectorizer.transform([message])
    '''
     PREDICTION
    '''

    def train(self):
        Preprocess.preprocess(
            self.df,
            column_in='message',
            column_out='message_clean')

        self.X = self.vectorize(self.df, column='message_clean')
        self.model = self.clf.fit(self.X, self.df['label'])

    def predict(self, message):
        vector = self.vectorize_message(message)
        predict_label = self.model.predict(vector)
        predict_proba = self.model.predict_proba(vector)

        idx_predict_class = np.argmax(predict_proba)

        return {
            'label': predict_label[0],
            'probability': predict_proba[0][idx_predict_class]
        }
