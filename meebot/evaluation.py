import pprint
import pandas as pd

intents_dataset = pd.DataFrame([
     # sales
     ['vendas do último mês', 'sales'],
     ['quanto vendi esse mês', 'sales'],
     ['quanto vendi no mês de agosto', 'sales'],
     ['quais são os 10 produtos que mais vendi esse ano', 'sales'],
     ['quais são os 10 produtos que mais vendi esse mês', 'sales'],
     ['quais são os 10 produtos que mais vendi hoje', 'sales'],
     ['qual produto eu mais vendi hoje', 'sales'],
     # products
     ['quantos produtos eu tenho na minha base', 'products'],
     ['quantos produtos eu tenho na minha base de dados', 'products'],
     ['quantos produtos eu tenho na minha loja', 'products'],
     ['quantos refrigerantes eu vendo na minha loja', 'products'],
     ['quanto é o preço da coca-cola', 'products'],
     ['qual é o preço da coca-cola', 'products'],
     ['quantos refrigerantes tenho no estoque', 'products']
 ], columns=['message', 'label'])

expected = [
    {'intent': 'sales', 'entities': [('hoje', 'DATE')]},
    {'intent': 'sales', 'entities': [('ontem', 'DATE')]},
    {'intent': 'sales', 'entities': [('março', 'DATE')]},
    {'intent': 'sales', 'entities': [('março', 'DATE'), ('junho', 'DATE')]},
    {'intent': 'sales', 'entities': [('fev', 'DATE'), ('jun', 'DATE')]},
    {'intent': 'sales', 'entities': [
        ('01/02/2020', 'DATE'),
        ('01/06/2020', 'DATE')
    ]},
    {'intent': 'products', 'entities': [('heinekens', 'PRODUCT')]},
    {'intent': 'products', 'entities': []},
    {'intent': 'products', 'entities': []}
]

messages = [
    # -- inactive -- 'qual produto eu mais vendi hoje',
    'como foram minhas vendas hoje ?',
    'como foram minhas vendas ontem ?',
    'como foram minhas vendas no mês de março ?',
    'como foram minhas vendas entre março e junho ?',
    'como foram minhas vendas entre fev e jun ?',
    'como foram minhas vendas entre 01/02/2020 e 01/06/2020',
    'quantas heinekens tenho no meu estoque ?',
    'como está o meu estoque ?',
    'quais produtos do meu estoque estão perto de acabar ?'
]


def report(expected, replies):
    pp = pprint.PrettyPrinter(indent=2)
    right_labels = 0
    wrong_labels = 0
    missing_entities = []

    total = len(replies)
    for i in range(total):
        intent = None
        entities = None
        reply = replies[i]

        if 'meta' in reply:
            intent = reply['meta']['intent']
            entities = reply['meta']['entities']

        if intent and expected[i]['intent'] == intent:
            right_labels += 1
        else:
            wrong_labels += 1

        if entities and len(expected[i]['entities']) != len(entities):
            missing_entities.append({
                'message': messages[i],
                'expected': expected[i]['entities'],
                'actual': entities})

    print('--- CLASSIFICATION ---')
    print('')
    print('RIGHT_LABELS:', right_labels)
    print('WRONG_LABELS:', wrong_labels)
    print('')
    print('--- ENTITIES ---')
    print('')
    if len(missing_entities) == 0:
        print('ALL ENTITIES MATCH ✅')
    else:
        pp.pprint(missing_entities)


def run_tests(chatbot):
    replies = []
    for message in messages:
        reply = chatbot.reply(message)
        print('REPLY:', reply)
        print('')
        replies.append(reply)

    print('--- REPORT ---')
    print('')
    report(expected, replies)
