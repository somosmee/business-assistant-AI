import re
from meebot.regex import months_regex
from meebot.chatbot.preprocess import Preprocess


class Helper:
    @staticmethod
    def is_month(entity):
        match = re.search(months_regex, entity)
        return match is not None

    @staticmethod
    def get_month_index(entity):
        months_index = {'janeiro': 1, 'fevereiro': 2, 'marco': 3, 'abril': 4, 'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12}
        months_abrev_index = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'jun': 6, 'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12 }
        match = re.search(months_regex, entity)
        if not match:
            return None
        else:
            month = match.group()
            month = Preprocess.normalize(month)

            if month in months_index:
                return months_index[month]
            elif month in months_abrev_index:
                return months_abrev_index[month]
            else:
                None

    @staticmethod
    def count_entities(entities, entity):
        count = 0
        for item in entities:
            if item[1] == entity:
                count += 1
        return count

    @staticmethod
    def compile_stats(cursor):
        totalSales = 0
        for order in cursor:
            totalSales += order['total']
        return {'totalSales': totalSales}
