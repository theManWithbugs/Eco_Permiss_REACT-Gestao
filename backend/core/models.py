from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import uuid
import os
import re

#Local imports
from .choices import *

def validador_cpf(cpf):
    numeros = [int(digito) for digito in cpf if digito.isdigit()]

    if len(numeros) != 11:
        raise ValidationError("CPF inválido.")

    soma1 = sum(a * b for a, b in zip(numeros[0:9], range(10, 1, -1)))
    digito1 = (soma1 * 10 % 11) % 10

    if numeros[9] != digito1:
        raise ValidationError("CPF inválido.")

    soma2 = sum(a * b for a, b in zip(numeros[0:10], range(11, 1, -1)))
    digito2 = (soma2 * 10 % 11) % 10

    if numeros[10] != digito2:
        raise ValidationError("CPF inválido.")

def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 Megabytes em bytes
    if value.size > limit:
        raise ValidationError('O arquivo não pode ser maior que 5MB.')

def _normalizar_nome_arquivo(filename):
    if not filename:
        return filename

    name, ext = os.path.splitext(filename)
    name_limpo = slugify(name)
    if not name_limpo:
        name_limpo = 'arquivo'

    base_name = re.sub(r'[^a-zA-Z0-9]+', '_', name_limpo).strip('_')
    if not base_name:
        base_name = 'arquivo'

    return f"{base_name}{ext.lower()}"


def get_path_rel(_instance, filename):
    ano = timezone.now().year
    mes_num = timezone.now().month
    meses = [
        None,'janeiro','fevereiro','março','abril','maio','junho',
        'julho','agosto','setembro','outubro','novembro','dezembro'
    ]
    mes = meses[mes_num]

    filename_limpo = _normalizar_nome_arquivo(filename)
    return os.path.join('docs_pesquisa', str(ano), mes, 'rel_final', filename_limpo)

def get_path_doc(_instance, filename):
    ano = timezone.now().year
    mes_num = timezone.now().month
    meses = [
        None,'janeiro','fevereiro','março','abril','maio','junho',
        'julho','agosto','setembro','outubro','novembro','dezembro'
    ]
    mes = meses[mes_num]

    filename_limpo = _normalizar_nome_arquivo(filename)
    return os.path.join('doc_usuario', str(ano), mes, filename_limpo)


def get_path_membro_doc(_instance, filename):
    ano = timezone.now().year
    mes_num = timezone.now().month
    meses = [
        None,'janeiro','fevereiro','março','abril','maio','junho',
        'julho','agosto','setembro','outubro','novembro','dezembro'
    ]
    mes = meses[mes_num]

    filename_limpo = _normalizar_nome_arquivo(filename)
    return os.path.join('docs_pesquisa', str(ano), mes, 'doc_membro_equipe', filename_limpo)

class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

class DadosPessoais(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dados_pessoais')
    ori_sexual = models.CharField(choices=SEXO, blank=False, max_length=12)
    estado = models.CharField(
        choices=ESTADOS_BRASIL_CHOICES, blank=False, max_length=20)
    municipio = models.CharField(max_length=80, blank=False)
    logradouro = models.CharField(blank=True, max_length=30)
    numero = models.IntegerField(blank=False)
    bairro = models.CharField(max_length=80, blank=False)
    telefone = models.CharField(max_length=13)
    rg = models.CharField(blank=False, max_length=20, verbose_name='RG', unique=True)
    org_emiss = models.CharField(
        blank=False, max_length=30, verbose_name='Orgão emissor(RG)')
    cpf = models.CharField(blank=False, validators=[
                           validador_cpf], max_length=14, verbose_name='CPF', unique=True)
    telefone_fixo = models.CharField(max_length=10, blank=True)
    cep = models.CharField(blank=True, max_length=9, verbose_name='CEP')
    profissao = models.CharField(blank=False, max_length=30, verbose_name='Profissão/Ocupação')
    codigo_recup = models.IntegerField()

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username

    class Meta:
        db_table = "dados_pessoais"

class UnidadesConservacao(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nome = models.CharField(max_length=80, blank=False, null=False)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        db_table = "unidades_conserv"

class AreaAtuacao(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    nome = models.CharField(max_length=80, blank=False, null=False)

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        db_table = "area_atuacao"

class DadosSolicPesquisa(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_public = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True  # Indexa e garante unicidade sem ser PK
    )

    user_solic = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="solicitacoes"
    )

    data_solicitacao = models.DateField(default=timezone.localdate)
    acao_realizada = models.CharField(max_length=80, blank=False)
    unidades = models.ManyToManyField(UnidadesConservacao)

    foto = models.CharField(
        choices=YES_OR_NOT,
        max_length=3,
        blank=False,
        null=False
    )

    inicio_atividade = models.DateField(default=timezone.localdate, blank=False, null=False)
    final_atividade = models.DateField(default=timezone.localdate, blank=False, null=False)
    retorno_comuni = models.CharField(max_length=150, blank=False)
    area_atuacao = models.ManyToManyField(AreaAtuacao)

    gestor_resp = models.CharField(
        max_length=80,
        blank=True,
        null=True
    )

    recusa_motivo = models.CharField(
        max_length=400,
        blank=True,
        null=True
    )

    # Documentos obrigatórios
    doc_ident = models.FileField(
        upload_to=get_path_doc,
        blank=False,
        null=False,
        validators=[validate_file_size]
    )

    doc_cpf = models.FileField(
        upload_to=get_path_doc,
        blank=False,
        null=False,
        validators=[validate_file_size]
    )

    doc_seg_vida = models.FileField(
        upload_to=get_path_doc,
        blank=False,
        null=False,
        validators=[validate_file_size]
    )

    status = models.CharField(
        choices=CHOICES_STATUS,
        max_length=10
    )

    def __str__(self):
        return f"{self.user_solic} - {self.data_solicitacao}"

    # def save(self, *args, **kwargs):
    #     for field in self._meta.concrete_fields:
    #         if isinstance(field, models.CharField):
    #             value = getattr(self, field.name)
    #             if value:
    #                 setattr(self, field.name, value.upper())

    #     super().save(*args, **kwargs)

    def clean(self):
        super().clean() # Mantém as validações nativas do django
        # Valida se a data inicial não é maior que a data atual
        if self.inicio_atividade and self.final_atividade:
            if self.inicio_atividade > self.final_atividade:
                raise ValidationError({
                    'final_atividade': 'A data final da atividade não pode ser anterior à data de início.'
                })

    class Meta:
        db_table = "solic_pesquisa"


class AnexExtraPesqLicenca(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        editable=False
    )

    solicitacao = models.ForeignKey(
        DadosSolicPesquisa,
        on_delete=models.CASCADE,
        related_name='licencas'
    )

    doc_url = models.FileField(
        upload_to=get_path_doc,
        validators=[validate_file_size]
    )

    class Meta:
        db_table = "anex_pesq_licenca"

class AnexExtraPesqOutros(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        editable=False
    )

    solicitacao = models.ForeignKey(
        DadosSolicPesquisa,
        on_delete=models.CASCADE,
        related_name='outros_documentos'
    )

    doc_url = models.FileField(
        upload_to=get_path_doc,
        validators=[validate_file_size]
    )

    class Meta:
        db_table = "anex_pesq_outros"

class MembroEquipePesq(models.Model):
    pesquisa = models.ForeignKey(
        DadosSolicPesquisa, on_delete=models.CASCADE, related_name='pesquisa')
    nome = models.CharField(blank=False, null=False, max_length=80)
    rg = models.CharField(blank=False, null=False,
                          max_length=20, verbose_name='RG')
    cpf = models.CharField(blank=False, null=False, max_length=14, verbose_name='CPF')
    ori_sexual = models.CharField(blank=False, null=False, choices=IDENTIDADE_GENERO_CHOICES,
                                  max_length=12, verbose_name='Orientação sexual')
    instituicao = models.CharField(
        blank=False, null=False, verbose_name='Instituição', max_length=80)
    email = models.EmailField(max_length=80, blank=False, null=False, verbose_name='Email')
    email_enviado = models.BooleanField(default=False)
    confirmado = models.BooleanField(default=False)
    token_confirmacao = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    data_confirm = models.DateTimeField(null=True, blank=True)

    def confirmar(self):
        self.confirmado = True
        self.data_confirm = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.nome}"

class AnexoMembroEquipe(models.Model):
    membro = models.ForeignKey(
        'MembroEquipePesq',
        on_delete=models.CASCADE,
        related_name='anexos'
    )
    nome_original = models.CharField(max_length=255, blank=True, null=True)
    upado_em = models.DateTimeField(default=timezone.now)
    doc_ident = models.FileField(upload_to=get_path_membro_doc, blank=False, null=False, validators=[validate_file_size])
    doc_cpf = models.FileField(upload_to=get_path_membro_doc, blank=False, null=False, validators=[validate_file_size])
    doc_seg_vida = models.FileField(upload_to=get_path_membro_doc, blank=False, null=False, validators=[validate_file_size])
    doc_cart_vacin = models.FileField(upload_to=get_path_membro_doc, blank=True, null=True, validators=[validate_file_size])
    licenca = models.FileField(upload_to=get_path_membro_doc, blank=True, null=True, validators=[validate_file_size])
    outros = models.FileField(upload_to=get_path_membro_doc, blank=True, null=True, validators=[validate_file_size])

    def __str__(self):
        return self.nome_original or str(self.membro)

class Ugai(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    total_vagas = models.PositiveIntegerField()

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "ugai"

    #"lte less than or equal", menor ou igual a data que foi solicitada
    #"gte greater than or equal": maior ou igual a data que foi solicitada
    # def vagas_ocupadas(self, inicio, fim):
    #     resultado = self.solicitacoes.filter(
    #         status='APROVADO',
    #         data_inicio__lte=fim,
    #         data_final__gte=inicio
    #     ).aggregate(
    #         total=Sum("quantidade_pessoas")
    #     )

    #     return resultado["total"] or 0

    # # 🔹 Calcula vagas disponíveis
    # def vagas_disponiveis(self, inicio, fim):
    #     return self.total_vagas - self.vagas_ocupadas(inicio, fim)

class DadosSolicUgai(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_public = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True  # Indexa e garante unicidade sem ser PK
    )

    user_solic = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="solicitacoes_ugai"
    )

    ugai = models.ForeignKey(
        Ugai,
        on_delete=models.PROTECT,
        related_name="solicitacoes"
    )

    quantidade_pessoas = models.PositiveIntegerField()

    instituicao = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name='Instituição'
    )

    setor = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )

    cargo = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )

    ativ_desenv = models.CharField(
        max_length=200,
        verbose_name='Atividades que irá desenvolver'
    )

    publico_alvo = models.CharField(
        max_length=80,
        verbose_name='Público alvo'
    )

    recusa_motivo = models.CharField(
        max_length=400,
        blank=True,
        null=True
    )

    status = models.CharField(
        choices=CHOICES_STATUS,
        max_length=10
    )

    data_solicitacao = models.DateField(
        default=timezone.localdate
    )

    data_inicio = models.DateField(
        default=timezone.localdate
    )

    data_final = models.DateField(
        default=timezone.localdate
    )

    class Meta:
        db_table = "solic_ugai"
        indexes = [
            models.Index(
                fields=["ugai", "data_inicio", "data_final"]
            ),
        ]

    def __str__(self):
        return f"{self.ugai.nome} - {self.user_solic}"

    def clean(self):
        if self.data_inicio > self.data_final:
            raise ValidationError(
                "Data final não pode ser menor que data inicial."
            )

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            value = getattr(self, field.name)

            if isinstance(field, models.CharField) and value:
                setattr(
                    self,
                    field.name,
                    value.upper()
                )

        self.full_clean()

        super().save(*args, **kwargs)

class MembroEquipeUGAI(models.Model):
    solicitacao_ref = models.ForeignKey(
        DadosSolicUgai,
        on_delete=models.PROTECT,
        related_name='membros'
    )
    nome = models.CharField(max_length=80, blank=False, null=False)
    email = models.EmailField(max_length=150, blank=True, null=True)
    telefone = models.CharField(max_length=11, blank=False, null=False)
    cor_raca = models.CharField(choices=RACA_CHOICES, blank=False, null=False, max_length=10)
    genero = models.CharField(choices=IDENTIDADE_GENERO_CHOICES, blank=False, null=False, max_length=12)
    data_nasc = models.DateField()

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        db_table = "equipe_ugai"
        indexes = [
            models.Index(fields=["solicitacao_ref"]),
        ]

class ArquivosRelFinal(models.Model):
    pesquisa_ref = models.ForeignKey(
        DadosSolicPesquisa, on_delete=models.CASCADE, related_name='arq_pesquisa')
    documento = models.FileField(upload_to=get_path_rel)
    upado_em = models.DateTimeField(default=timezone.now)

    def delete_documento(self):
        if self.documento:
            if os.path.isfile(self.documento.path):
                os.remove(self.documento.path)
            self.documento = None
        self.delete()

    def __str__(self):
        return f"{self.pesquisa_ref.acao_realizada}"
