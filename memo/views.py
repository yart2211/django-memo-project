import logging
import json
import operator
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from memo.PrepareData import  PrepareData
from memo.models import Memo, CategoryMemo

class MemoListView(LoginRequiredMixin, generic.ListView):
    '''
    Класс-представление списка заметок
    '''
    template_name = 'memo/list.html'
    context_object_name = 'memo_list'
    model = Memo

    '''def get_context_data(self, **kwargs):
        if self.request.method == 'GET':
            context = super(MemoListView, self).get_context_data(**kwargs)
            context["data"] = "init"
        return context
    '''


class MemoDetailView(generic.DetailView):
    '''
    Класс-представление карточки заметки
    '''
    template_name = 'memo/card.html'
    context_object_name = 'memo_object'
    model = Memo
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    #def get_object(self):
    #    return Memo.objects.get(uuid=self.kwargs.get("uuid"))
    def get_context_data(self, **kwargs):
        context = super(MemoDetailView, self).get_context_data(**kwargs)
        context['context_data'] = "тест"
        context["header"] = context["object"].header
        return context


@csrf_exempt
def memo_data(request, operation):
    '''
    Обработчик действий над списком заметок в гриде
    :param request: объект http запроса
    :param operation: имя операции (read, changefavorite, destroy)
    :return:
    '''
    if request.method == 'POST':
        if operation=='read':
            objects = Memo.objects.filter(user=request.user)
            # Применение клиентского фильтра и сортировки
            prepareData = PrepareData(objects)
            objects = prepareData.get_filter_data(request.POST, operator.and_)
            if "sort" in request.POST:
                if request.POST["dir"] == "DESC":
                    dir = "-"
                else:
                    dir = ""
                objects = objects.order_by(dir + request.POST["sort"])
            # Формирование данных
            list_object = []
            count = objects.count()
            for item in objects:
                dict_resp = {}
                dict_resp['id'] = item.id
                dict_resp['header'] = item.header
                dict_resp['is_favorite'] = item.is_favorite
                dict_resp['category__name'] = item.category.name
                dict_resp['date'] = item.date.strftime('%d.%m.%Y %H:%M')
                dict_resp['uuid'] = item.uuid
                list_object.append(dict_resp)
            # Формирование json ответа
            dict_result = {"data": list_object, "meta": {"success": "true", "msg": "", "total": str(count)}}
            json_result = json.dumps(dict_result)
            return HttpResponse(json_result)

        elif  operation=='changefavorite':
            id = request.POST["id"]
            memo = Memo.objects.get(pk=id)
            memo.is_favorite = not memo.is_favorite
            memo.save()
            response_object = {'data':memo.is_favorite}
            return HttpResponse(json.dumps(response_object))

        elif operation=='destroy':
            id = request.POST["id"]
            memo = Memo.objects.get(pk=id)
            memo.delete()
            response_object = {'is_delete': 'true'}
            return HttpResponse(json.dumps(response_object))
    return None


class MemoFormView(LoginRequiredMixin, generic.FormView):
    '''
    Класс-представление формы регистрации\редактирования заметки
    '''
    template_name = 'memo/form.html'
    context_object_name = 'data'
    model = Memo
    success_url = '/thanks/'
    form_class = forms.Form
    def get_context_data(self, **kwargs):
        context = super(MemoFormView, self).get_context_data(**kwargs)
        object_id = self.kwargs["id"]
        context["object_id"] = object_id
        #Формирование данных для списка
        category_list = []
        for category_item in CategoryMemo.objects.all():
            category_list.append([category_item.id, category_item.name])
        if len(category_list) != 0:
            context["category_value"] = category_list[0][0]
        #значения по умолчанию для нового объекта
        context["category_list"] = category_list
        if object_id!="new":
            context["title"] = "Редактирование заметки"
            memo_object = Memo.objects.get(id=int(object_id))
            if memo_object.user != self.request.user:
                context["error"] = "Нет прав для редактирования данной заметки"
            context["header"] = memo_object.header
            context["is_favorite"] = memo_object.is_favorite
            context["content"] = memo_object.content
            context["category_value"] = memo_object.category.id
        else:
            context["title"] = "Регистрация заметки"

        return context


@csrf_exempt
def memo_edit(request):
    '''
    Обработчик данных от формы редактирования
    '''
    if (request.method == "POST"):
        if request.POST["object_id"]!="new":
            memo = Memo.objects.get(id=request.POST["object_id"])
        else:
            memo = Memo()
        memo.header = request.POST["header"]
        category = CategoryMemo.objects.get(id=request.POST["category"])
        memo.category = category
        memo.user = request.user
        if "is_favorite" in request.POST and request.POST["is_favorite"]=="on":
            memo.is_favorite = True
        else:
            memo.is_favorite = False
        memo.content = str(request.POST["content"]).replace("\r","").replace("\n","")
        memo.save()
        response_object = {"success":True, "uuid": str(memo.uuid)}
        return HttpResponse(json.dumps(response_object))