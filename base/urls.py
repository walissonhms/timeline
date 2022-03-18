from urllib import request

from django.urls import path
from . import views
from .templates import api

urlpatterns = [
    path('arquivo/', views.importacaoVC),
    path('noticias/<int:noticia_id>', views.noticiaId),
    path('timeline/', views.timeline),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('filtro_data/', views.filtro, name='filtro'),
    path('arquivopt/', views.api_arquivopt),
    path('arquivotm/', api.arquivoTM)

]
