from datetime import datetime
from functools import reduce

class PrepareData():
    '''
    Формирование условий запроса на основе параметров фильтров и сортировки от пользователя (extjs grid)
    '''
    def __init__(self, data):
        '''
        :param data: Исходные данные
        '''
        self.data = data

    def get_filter_data(self, params, query_operator):
        '''
        Фильтрация данных на основе параметров-предикатов
        :param params: список предикатов [('param1','value1'), ('param2','value2')..]
        :param query_operator: sql оператор  (or, and)
        :return: отфильтрованные данные
        '''
        predicates = self._create_filter_predicates(params, self._get_filter_count(params))
        from django.db.models import Q
        q_list = [Q(x) for x in predicates]
        if len(q_list) > 0:
            return self.data.filter(reduce(query_operator, q_list))
        else:
            return self.data

    def get_sorted_data(self, params):
        if "sort" in params:
            if params["dir"]=="DESC":
                dir = "-"
            else:
                dir=""
            self.objects.order_by(dir+params["sort"])
        else:
            return self.objects

    def _get_filter_count(self, params):
        filter_count = 0
        while (True):
            if self._key_field(filter_count) in params:
                filter_count = filter_count + 1
            else:
                return filter_count

    def _key_field(self, index):
        return "filter[" + str(index) + "][field]"

    def _key_type(self, index):
        return "filter[" + str(index) + "][data][type]"

    def _key_value(self, index):
        return "filter[" + str(index) + "][data][value]"

    def _key_comparison(self, index):
        return "filter[" + str(index) + "][data][comparison]"

    def _create_filter_predicates(self, params, count):
        result = []
        for iter in range(count):
            field_value = params[self._key_value(iter)]
            field_name = params[self._key_field(iter)]
            if self._key_comparison(iter) in params:
                if params[self._key_comparison(iter)] == "eq":
                    field_comparison = "__exact"
                elif params[self._key_comparison(iter)] == "gt":
                    field_comparison = "__gt"
                elif params[self._key_comparison(iter)] == "lt":
                    field_comparison = "__lt"
                else:
                    field_comparison = "__exact"
            else:
                if params[self._key_type(iter)] == "string":
                    field_comparison = "__contains"
                elif params[self._key_type(iter)] == "boolean":
                    field_comparison = "__exact"

            if params[self._key_type(iter)] == "date":
                field_value = str(datetime.strptime(field_value, '%m/%d/%Y').date())
            if params[self._key_type(iter)] == "boolean":
                field_value = field_value[0].upper() + field_value[1:]
            result.append((field_name + field_comparison, field_value))
        return result




