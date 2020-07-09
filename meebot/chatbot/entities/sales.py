import os
import pendulum
from string import Template
from bson.objectid import ObjectId
from meebot.chatbot.helper import Helper

class EntitySalesAnswer:

    sales_template = Template('Você vendeu R$ $totalSales $timeFrame')

    @staticmethod
    def reply(entities, db) -> str:
        sales_template = EntitySalesAnswer.sales_template
        query = { 'grocery': ObjectId(os.getenv('USER_OID')) }
        dates_count = Helper.count_entities(entities, 'DATE')

        if dates_count == 1 and (entities[0][0] == 'hoje' or entities[0][0] == 'ontem'):
            entity = entities[0][0]
            start = None
            end = None

            if entity == 'hoje':
                start = pendulum.today().start_of('day')
                end = pendulum.today().end_of('day')
            elif entity == 'ontem':
                start = pendulum.yesterday().start_of('day')
                end = pendulum.yesterday().end_of('day')
            else:
                # we need to check what is this
                return answer

            query['status'] = 'closed'
            query['createdAt'] = { '$gte': start, '$lte': end }

            answer = sales_template.safe_substitute({'timeFrame': 'no dia de {}'.format(entity)})

        elif dates_count == 1 and Helper.is_month(entities[0][0]):
            entity = entities[0][0]
            month_index = Helper.get_month_index(entity)

            dt = pendulum.now()
            dt = dt.set(month=month_index)

            start = dt.start_of('month')
            end = dt.end_of('month')

            query['status'] = 'closed'
            query['createdAt'] = { '$gte': start, '$lte': end }

            answer = sales_template.safe_substitute({'timeFrame': 'no mês de {}'.format(entity)})

        elif dates_count == 2 and Helper.is_month(entities[0][0]) and Helper.is_month(entities[1][0]):
            entity_ini = entities[0][0]
            entity_end = entities[1][0]

            month_ini_index = Helper.get_month_index(entity_ini)
            month_end_index = Helper.get_month_index(entity_end)

            dt = pendulum.now()

            dt_ini = dt.set(month=month_ini_index)
            dt_end = dt.set(month=month_end_index)

            start = dt_ini.start_of('month')
            end = dt_end.end_of('month')

            query['status'] = 'closed'
            query['createdAt'] = { '$gte': start, '$lte': end }

            answer = sales_template.safe_substitute({'timeFrame': 'entre os meses de {} e {}'.format(entity_ini, entity_end)})

        elif dates_count == 2:
            start = pendulum.from_format(entities[0][0], 'DD/MM/YYYY')
            end = pendulum.from_format(entities[1][0], 'DD/MM/YYYY')

            query['status'] = 'closed'
            query['createdAt'] = { '$gte': start, '$lte': end }

            answer = sales_template.safe_substitute({ 'timeFrame': 'entre {} e {}'.format(start.format('DD/MM/YYYY'), end.format('DD/MM/YYYY')) })
        else:
            return answer

        print('QUERY:', query)

        cursor = db.orders.find(query)
        stats = Helper.compile_stats(cursor)

        answer = Template(answer).safe_substitute({ 'totalSales': '{:,.2f}'.format(stats['totalSales']) })
        return answer
