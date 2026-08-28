YES_OR_NOT = (
  ('NA', 'Selecione'),
  ('SIM', 'Sim'),
  ('NAO', 'Não')
)

TIPO_SOLIC = (
  ('NA', 'Selecione'),
  ('AUTORIZAÇÃO', 'Autorização'),
  ('RENOVACAO', 'Renovação')
)

SEXO = (
  ('NA', 'Selecione'),
  ('M', 'Masculino'),
  ('F', 'Feminino'),
  ('NB', 'Não binário'),
  ('AG', 'Agênero'),
  ('GF', 'Gênero fluido'),
  ('OT', 'Outro'),
  ('PN', 'Prefiro não informar'),
)

RACA_CHOICES = (
  ('PRETA', 'Preta'),
  ('PARDA', 'Parda'),
  ('INDIGENA', 'Indigena'),
  ('AMARELA', 'Amarela'),
  ('BRANCA', 'Branca')
)

IDENTIDADE_GENERO_CHOICES = (
  ("mulher_trans", "Mulher Trans"),
  ("homem_trans", "Homem Trans"),
  ("mulher_cis", "Mulher Cis"),
  ("homem_cis", "Homem Cis"),
  ("outros", "Outros"),
)

ORIENTACOES_CHOICES = [
  ("Heterossexual", "HETEROSEXUAL"),
  ("Homossexual", "HOMOSEXUAL"),
  ("Bissexual", "BISSEXUAL"),
  ("Assexual", "ASSEXUAL"),
  ("Pansexual", "PANSEXUAL")
]

ESTADOS_BRASIL_CHOICES = (
  ('NA', 'Selecione'),
  ('AC', 'Acre'),
  ('AL', 'Alagoas'),
  ('AP', 'Amapá'),
  ('AM', 'Amazonas'),
  ('BA', 'Bahia'),
  ('CE', 'Ceará'),
  ('DF', 'Distrito Federal'),
  ('ES', 'Espírito Santo'),
  ('GO', 'Goiás'),
  ('MA', 'Maranhão'),
  ('MT', 'Mato Grosso'),
  ('MS', 'Mato Grosso do Sul'),
  ('MG', 'Minas Gerais'),
  ('PA', 'Pará'),
  ('PB', 'Paraíba'),
  ('PR', 'Paraná'),
  ('PE', 'Pernambuco'),
  ('PI', 'Piauí'),
  ('RJ', 'Rio de Janeiro'),
  ('RN', 'Rio Grande do Norte'),
  ('RS', 'Rio Grande do Sul'),
  ('RO', 'Rondônia'),
  ('RR', 'Roraima'),
  ('SC', 'Santa Catarina'),
  ('SP', 'São Paulo'),
  ('SE', 'Sergipe'),
  ('TO', 'Tocantins'),
)

MUNICIPIOS_CHOICES = (
  ('NA', 'Selecione'),
  ('ACRELANDIA', 'Acrelândia'),
  ('ASSIS_BRASIL', 'Assis Brasil'),
  ('BRASILEIA', 'Brasiléia'),
  ('BUJARI', 'Bujari'),
  ('CAPIXABA', 'Capixaba'),
  ('CRUZEIRO_SUL', 'Cruzeiro do Sul'),
  ('EPITACIOLANDIA', 'Epitaciolândia'),
  ('FEIJO', 'Feijó'),
  ('JORDAO', 'Jordão'),
  ('MANOEL_URB', 'Manoel Urbano'),
  ('MARECHAL_THAU', 'Marechal Thaumaturgo'),
  ('MANCIO_LIMA', 'Mâncio Lima'),
  ('PLACIDO_CAS', 'Plácido de Castro'),
  ('PORTO_ACRE', 'Porto Acre'),
  ('PORTO_WALT', 'Porto Walter'),
  ('RIO_BRANCO', 'Rio Branco'),
  ('RODRIGUES_ALV', 'Rodrigues Alves'),
  ('SANTA_ROSA', 'Santa Rosa do Purus'),
  ('SENA_MADURE', 'Sena Madureira'),
  ('SENADOR_GUIOM', 'Senador Guiomard'),
  ('TARAUACA', 'Tarauacá'),
  ('XAPURI', 'Xapuri'),
)

CHOICES_AREA_ATUACAO = (
  # ('NA', 'Selecione'),
  ('FAUNA', 'Fauna'),
  ('FLORA', 'Flora'),
  ('ECOLOGIA', 'Ecologia'),
  ('GEOLOGIA', 'Geologia'),
  ('SOCIOECONOMIA', 'Socioeconomia'),
  ('ARQUEOLOGIA', 'Arqueologia'),
  ('TURISMO', 'Turismo'),
  ('RECURSOS HIDRICOS', 'Recursos hidricos'),
  ('EDUCAÇÃO AMBIENTAL', 'Educação Ambiental'),
  ('CAVIDADES NATURAIS', 'Cavidades Naturais'),
  # ('OUTROS', 'Outros')
)

CHOICES_UGAIS = (
  ('UGAI LIBERDADE', 'UGAI Liberdade'),
  ('UGAI ACURAUA', 'UGAI Acuraua'),
  ('UGAI JURUPARI', 'UGAI Jurupari'),
  ('UGAI ANTIMARY', 'UGAI Antimary'),
  ('UGAI CHANDLESS', 'UGAI Chandles')
)

CHOICES_STATUS = (
  ('APROVADO', 'Aprovado'),
  ('PENDENTE', 'Pendente'),
  ('INDEFERIDO', 'Indeferido'),
  ('ENCERRADO', 'Encerrado')
)

UCS_CHOICES = (
  ("parque_estadual_chandless", "Parque Estadual Chandless"),
  ("apa_lago_do_amapa", "APA Lago do Amapá"),
  ("apa_igarape_sao_francisco", "APA Igarapé São Francisco"),
  ("floresta_estadual_antimary", "Floresta Estadual do Antimary"),
  ("floresta_estadual_rio_gregorio", "Floresta Estadual do Rio Gregório"),
  ("floresta_estadual_mogno", "Floresta Estadual do Mogno"),
  ("floresta_estadual_liberdade", "Floresta Estadual Liberdade"),
  ("floresta_estadual_afluente", "Floresta Estadual Afluente"),
  ("arie_japiim_pentecoste", "ARIE Japiim Pentecoste")
)