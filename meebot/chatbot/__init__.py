'''
 Business Chat Bot by Mee 🤖🔮💜
 Author: Guilherme Kodama 06/2020
'''

import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# local modules
from meebot.chatbot.entities import SaleQA
from meebot.chatbot.entities import ProductQA
from meebot.chatbot.preprocess import Preprocess
from meebot.chatbot.intent import IntentClassifier


class ChatBot:

    def __init__(self, df, column_message='message', column_label='label'):
        self.df = df.copy()

        # Database
        client = MongoClient(os.getenv('MONGO_URI'))
        self.db = client.mee

        # load product NER corpus
        self.product_corpus = []
        self.product_ids = []
        cursor = self.db.usersProducts.find({
            'grocery': ObjectId(os.getenv('USER_OID'))}).sort('_id', 1)

        for product in cursor:
            self.product_corpus.append(Preprocess.normalize(product['name']))
            self.product_ids.append(product['product'])

        # Intent classifier
        self.classifier = IntentClassifier(self.df)
        self.classifier.train()

        # QA Entities
        self.product_qa = ProductQA(self.db, self.product_corpus, self.product_ids)
        self.sale_qa = SaleQA()

    def reply(self, message):
        print('MESSAGE: ', message)
        message = message.lower()

        prediction = self.classifier.predict(message)
        intent = prediction['label']

        answer = 'Não entendi a sua pergunta'

        if intent == 'sales':
            reply = self.sale_qa.answer(message, self.db)
            if reply:
                answer = reply

        if intent == 'products':
            reply = self.product_qa.answer(message, self.db)
            if reply:
                answer = reply

        return answer
