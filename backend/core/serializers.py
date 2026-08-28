from rest_framework import serializers

from .models import *

# SOLICS DE PESQUISA
class SerializerAnexosOutros(serializers.ModelSerializer):
    class Meta:
        model = AnexExtraPesqOutros
        fields = "__all__"

class SerializerAnexosLicenca(serializers.ModelSerializer):
    class Meta:
        model = AnexExtraPesqLicenca
        fields = "__all__"

class SerializerInfoPesq(serializers.ModelSerializer):
    outros_documentos = SerializerAnexosOutros(many=True, read_only=True)
    licencas = SerializerAnexosLicenca(many=True, read_only=True)

    class Meta:
        model = DadosSolicPesquisa
        exclude = ["unidades", "area_atuacao"]

# SOLICS DE UGAI
class SerializerGetDataUgai(serializers.ModelSerializer):
    """
    Serializa DadosSolicUgai para listagem/detalhe.
    """
    # Pegando campo de outro modelo interligado e enviando direto
    nome_ugai = serializers.ReadOnlyField(source='ugai.nome')

    class Meta:
        model = DadosSolicUgai
        exclude = ['id']

class SerializerMembrosUgai(serializers.ModelSerializer):
    class Meta:
        model = MembroEquipeUGAI
        exclude = ['solicitacao_ref']
