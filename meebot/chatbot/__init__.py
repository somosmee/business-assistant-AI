'''
 Business Chat Bot by Mee 🤖🔮💜
 Author: Guilherme Kodama 06/2020
'''

import os
from string import Template
from pymongo import MongoClient
from bson.objectid import ObjectId
from spacy.lang.pt import Portuguese
from meebot.regex import months_regex
from spacy.pipeline import EntityRuler

# local modules
from meebot.ner import NER
from meebot.chatbot.helper import Helper
from meebot.chatbot.preprocess import Preprocess
from meebot.chatbot.intent import IntentClassifier
from meebot.chatbot.entities.sales import EntitySalesAnswer


class ChatBot:

    def __init__(self, df, column_message='message', column_label='label'):
        self.df = df.copy()
        # self.nlp = spacy.load('pt')
        self.nlp = Portuguese()
        self.ruler = EntityRuler(self.nlp)

        # Intent classifier
        self.classifier = IntentClassifier(self.df)
        self.classifier.train()

        # Database
        client = MongoClient(os.getenv('MONGO_URI'))
        self.db = client.mee
        self.USER_OID = ObjectId('5d2c89e514b9f2001dcb059b')

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

        # load product NER corpus
        product_corpus = []
        cursor = self.db.usersProducts.find({'grocery': self.USER_OID})
        for product in cursor:
            product_corpus.append(Preprocess.normalize(product['name']))

        self.product_ner = NER(product_corpus)

    '''
        ANSWERS
    '''

    def understand(self, message):
        prediction = self.classifier.predict(message)
        entities = self.extract_entities(message, prediction['label'])
        return {'prediction': prediction, 'entities': entities}

    def look_for_answers(self, intent, entities):
        answer = 'Não entendi a sua pergunta'
        products_template = Template('Você tem $inventory $product no seu estoque atualmente')

        if intent == 'sales':
            reply = EntitySalesAnswer.reply(entities, self.db)
            if reply:
                answer = reply

        if intent == 'products':
            product_count = Helper.count_entities(entities, 'PRODUCT')
            if product_count == 1:
                product_name = entities[0][0]
                inventory = self.db.inventory.find_one({
                    'grocery': self.USER_OID,
                    'product': ObjectId('5d2df07227e8c0001d8735aa')})
                answer = products_template.safe_substitute({
                    'inventory': inventory['balance'],
                    'product': product_name})

        return answer

    def reply(self, message):
        print('MESSAGE: ', message)
        message = message.lower()

        info = self.understand(message)
        intent = info['prediction']['label']
        entities = info['entities']
        answer = self.look_for_answers(intent, entities)

        return answer

    '''
     NER - Named Entity Recognition
    '''

    def extract_entities(self, message, intent):
        doc = self.nlp(message)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        if intent == 'products':
            product_entities = self.product_ner.recognize(
                message,
                algo='edit_distance')

            print('product_entities:', product_entities)

            if product_entities:
                entities = entities + product_entities
        return entities
