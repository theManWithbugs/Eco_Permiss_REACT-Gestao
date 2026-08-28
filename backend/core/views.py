from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from collections import Counter
from datetime import date

#Local imports
from .models import *
from .serializers import *

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pesquisas_solicitadas(request):
    status_pesq = request.GET.get('status', 'PENDENTE')
    objs = DadosSolicPesquisa.objects.filter(status=status_pesq).values(
        'id_public', 'acao_realizada', 'status', 'data_solicitacao'
    ).order_by('-data_solicitacao')

    page_number = request.GET.get('page', 1)
    paginator = Paginator(objs, 10)
    page_obj = paginator.get_page(page_number)

    #Aqui é feito diferente porque quando se usa values é retornado um dicionario
    itens_json = []
    for item in page_obj:
        itens_json.append(item)

    return JsonResponse({
        'objs': itens_json,
        'currentPage': page_obj.number,
        'totalPages': paginator.num_pages,
        'hasNext': page_obj.has_next(),
        'hasPrevious': page_obj.has_previous()
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ugais_solicitadas(request):
    status_solic = request.GET.get('status', 'PENDENTE')
    objs = DadosSolicUgai.objects.filter(
        status=status_solic).select_related('ugai').order_by('-data_solicitacao')

    print(objs)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(objs, 10)
    page_obj = paginator.get_page(page_number)

    itens_json = []
    for item in page_obj:
        d = model_to_dict(item)
        d["ugai"] = str(item.ugai)
        if 'id' in d:
            del d['id']
        d['id_public'] = str(item.id_public)
        itens_json.append(d)

    return JsonResponse({
        'objs': itens_json,
        'currentPage': page_obj.number,
        'totalPages': paginator.num_pages,
        'hasNext': page_obj.has_next(),
        'hasPrevious': page_obj.has_previous()
    })

# Informações de PESQUISA e UGAI
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def info_pesquisa(request):
    id_public = request.data
    obj = get_object_or_404(DadosSolicPesquisa, id_public=id_public)

    serializer = SerializerInfoPesq(
        instance=obj,
        context={'request': request}
    )

    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def info_ugai(request):
    id_public = request.data

    if not id_public:
        return Response({"message": "O campo id é necessario!"}, status=400)

    obj = get_object_or_404(DadosSolicUgai.objects,
                            id_public=id_public)

    obj_ugai = MembroEquipeUGAI.objects.filter(solicitacao_ref=obj.id)

    serializer = SerializerGetDataUgai(instance=obj)
    serializer_membro = SerializerMembrosUgai(instance=obj_ugai, many=True)

    return Response({
        "solicitacao": serializer.data,
        "membros": serializer_membro.data
    }, status=200)
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#

# São quase iguais!, apenas coloque uma variavel de controle
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decidir_pesq(request):
    acao = request.data.get('acao')
    id_public = request.data.get('id_public')

    obj = get_object_or_404(DadosSolicPesquisa, id_public=id_public)

    if obj.status != 'PENDENTE':
        Response({"message": "Apenas pesquisas pendentes podem ser alteradas!"}, status=401)

    if acao == 'APROVAR':
        obj.status = 'APROVADO'
    elif acao == 'RECUSAR':
        obj.status = 'INDEFERIDO'
    else:
        return Response({"message": "Ação inválida."}, status=400)

    obj.save(update_fields=['status'])

    return Response({"message": "Ação realizada com sucesso!", "status": obj.status}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decidir_ugai(request):
    acao = request.data.get('acao')
    id_public = request.data.get('id_public')

    obj = get_object_or_404(DadosSolicUgai, id_public=id_public)

    if obj.status != 'PENDENTE':
        Response({"message": "Apenas solicitações pendentes podem ser alteradas!"}, status=401)

    if acao == 'APROVAR':
        obj.status = 'APROVADO'
    elif acao == 'RECUSAR':
        obj.status = 'INDEFERIDO'
    else:
        return Response({"message": "Ação inválida."}, status=400)

    obj.save(update_fields=['status'])

    return Response({"message": "Ação realizada com sucesso!", "status": obj.status}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gestao_ugais(request):

    class SerializerVagasUgai(serializers.Serializer):
        nome_ugai = serializers.CharField(max_length=80)
        vagas_ocupadas = serializers.IntegerField()

    hoje = date.today()
    solicitacoes = DadosSolicUgai.objects.filter(status='APROVADO', data_final__gte=hoje)

    ocupacoes = Counter()
    for x in solicitacoes:
        ocupacoes[x.ugai] += x.quantidade_pessoas

    # Deve estar em formato chave valor antes de ir para o serializer
    dados_formatados = []
    for ugai_obj, quantidade in ocupacoes.items():
        dados_formatados.append({
            "nome_ugai": ugai_obj.nome,
            "vagas_ocupadas": quantidade
        })

    serializer = SerializerVagasUgai(data=dados_formatados, many=True)

    if serializer.is_valid():
        return Response({"dados": serializer.data}, status=200)
    return  Response({"message": "Error", "dados": serializer.errors}, status=401)

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#