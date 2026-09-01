from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
  # LOGIN
  #--------------------------------------#
  #--------------------------------------#
  path('login/', TokenObtainPairView.as_view(), name='login'),
  path('refresh/', TokenRefreshView.as_view(), name='refresh'),
  #--------------------------------------#
  #--------------------------------------#

  # SOLICS PESQUISA
  #--------------------------------------#
  #--------------------------------------#
  path('pesq_solicitadas/', pesquisas_solicitadas),
  path('info_pesq/', info_pesquisa),
  path('info_membros_pesq/', info_membro_pesq),

  path('decidir_pesq/', decidir_pesq),
  #--------------------------------------#
  #--------------------------------------#

  # SOLICS DE UGAI
  #--------------------------------------#
  #--------------------------------------#
  path('ugais_solics/', ugais_solicitadas),
  path('info_ugai/', info_ugai),

  path('decidir_ugai/', decidir_ugai),

  path('gestao_ugais/', gestao_ugais)
  #--------------------------------------#
  #--------------------------------------#
]