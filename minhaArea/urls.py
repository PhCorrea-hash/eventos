from django.urls import path
from minhaArea.views import area, criar_grupo, adicionar_membro, pagina_grupo, adicionar_mensagem, adicionar_agenda, remover_da_agenda, listar_membros

# Urls do app minhaArea
urlpatterns = [
    path('area/', area, name='area'),
    path('criar_grupo/', criar_grupo, name='criar_grupo'),
    path('membros/', listar_membros, name='listar_membros'),
    path('grupo/<int:grupo_id>/adicionar/', adicionar_membro, name='adicionar_membro'),
    path('grupo/<int:grupo_id>/', pagina_grupo, name='pagina_grupo'),
    path('grupo/<int:grupo_id>/mensagem/', adicionar_mensagem, name='adicionar_mensagem'),
    path('adicionar-agenda/<int:evento_id>/', adicionar_agenda, name='adicionar_agenda'),
    path('remover-agenda/<int:evento_id>/', remover_da_agenda, name='remover_agenda'),
]