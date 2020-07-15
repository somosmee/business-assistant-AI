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
    # {'label': 'sales', 'entities': [('hoje', 'DATE')]},
    # {'label': 'sales', 'entities': [('ontem', 'DATE')]},
    # {'label': 'sales', 'entities': [('março', 'DATE')]},
    # {'label': 'sales', 'entities': [('março', 'DATE'), ('junho', 'DATE')]},
    # {'label': 'sales', 'entities': [('fev', 'DATE'), ('jun', 'DATE')]},
    # {'label': 'sales', 'entities': [
    #     ('01/02/2020', 'DATE'),
    #     ('01/06/2020', 'DATE')
    # ]},
    {'label': 'products', 'entities': [('heinekens', 'PRODUCT')]}
]

messages = [
    # -- inactive -- 'qual produto eu mais vendi hoje',
    # 'como foram minhas vendas hoje ?',
    # 'como foram minhas vendas ontem ?',
    # 'como foram minhas vendas no mês de março ?',
    # 'como foram minhas vendas entre março e junho ?',
    # 'como foram minhas vendas entre fev e jun ?',
    # 'como foram minhas vendas entre 01/02/2020 e 01/06/2020',
    'quantas heinekens tenho no meu estoque ?'
]


def report(expected, responses):
    pp = pprint.PrettyPrinter(indent=2)
    right_labels = 0
    wrong_labels = 0
    missing_entities = []

    total = len(responses)
    for i in range(total):
        if expected[i]['label'] == responses[i]['prediction']['label']:
            right_labels += 1
        else:
            wrong_labels += 1

        if len(expected[i]['entities']) != len(responses[i]['entities']):
            missing_entities.append({
                'message': messages[i],
                'expected': expected[i]['entities'],
                'actual': responses[i]['entities']})

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
    # responses = []
    for message in messages:
        reply = chatbot.reply(message)
        print('REPLY:', reply)
        # resp = chatbot.understand(message)
        # print(resp)
        # print('')
        # responses.append(resp)

    # print('--- REPORT ---')
    # print('')
    # report(expected, responses)
