# Fontes e procedência

IPEA. **Mapa das Organizações da Sociedade Civil: Base de Dados.** Portal oficial:
<https://mapaosc.ipea.gov.br/base-dados>. A página informa coleta e envio em agosto
de 2026. Arquivo consultado:
<https://mapaosc.ipea.gov.br/download/20260806_MOSC_baseDivulgacao.csv>.
Extração em 4 nov. 2026. O arquivo contém OSCs com diferentes situações cadastrais,
incluindo baixadas. A análise separa o recorte completo das ativas e não removidas.

IBGE. **Censo Demográfico 2022: População residente, tabela SIDRA 4714, variável 93.**
API oficial: <https://apisidra.ibge.gov.br/values/t/4714/n6/all/v/93/p/2022>.
Extração em 4 nov. 2026. Os 5.570 registros municipais são preservados no JSON da API,
com a linha inicial de metadados. A população é de 2022, não uma estimativa para 2026.

KIPPER, Marina. **Panorama das ONGs no Brasil: desafios e perspectivas do Terceiro
Setor.** HYB, 9 abr. 2026.
<https://blog.hyb.com.br/panorama-das-ongs-no-brasil-desafios-e-perspectivas-do-terceiro-setor/>.
Artigo sugerido como contextualização do tema; não forneceu os microdados analisados.

IDIS. **Panorama das ONGs: estudo revela resiliência do terceiro setor no Brasil
diante do aumento de demandas e desafios de sustentabilidade.** 20 jan. 2026.
<https://www.idis.org.br/panorama-das-ongs-estudo-revela-resiliencia-do-terceiro-setor-no-brasil/>.
Fonte institucional de contexto sobre sustentabilidade, gestão e transparência.
O levantamento descrito nessa página é diferente da base cadastral do Ipea.

VIEIRA, Felipe Barbosa; BEZERRA, Calebe Mendes. **Definição do Projeto Pescadores Web.**
Versão 2.0, set. 2026. Documento original preservado no repositório.

## Reprodução

As URLs diretas, critérios de seleção, número de linhas e hashes SHA-256 ficam em
`dados/brutos/FONTES.json`. `scripts/obter_dados.py` repete a aquisição, sem gerar
observações artificiais. `scripts/analise.py` executa as transformações documentadas.
Os recortes são cadastrais; nenhuma fonte utilizada contém estoque ou doações da ONG.
