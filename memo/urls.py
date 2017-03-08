
from django.conf.urls import url, include
from django.views.generic import DetailView

from memo import accounts_views
from memo import views
app_name = 'memo'
urlpatterns = [

    url(r'^$', views.MemoListView.as_view(), name='list'),
    url(r'^form/(?P<id>[0-9]+|new)/$', views.MemoFormView.as_view(), name='form'),
    url(r'^(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.MemoDetailView.as_view(),name='card'),
    #ссылки на вспомогательные обработчики
    url(r'^data/(?P<operation>[a-z]+)/$', views.memo_data, name='data'),
    url(r'^edit/$', views.memo_edit, name='dataform'),
    #аутентификация
    url(r'^registration/$', accounts_views.RegisterFormView.as_view(), name='registration'),
    url(r'^login/$', accounts_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', accounts_views.LogoutView.as_view(), name='logout'),
]