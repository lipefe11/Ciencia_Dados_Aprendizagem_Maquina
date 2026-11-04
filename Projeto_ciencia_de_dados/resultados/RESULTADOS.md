# Resultados com dados públicos reais

Pergunta: qual é o perfil e a distribuição das OSCs de assistência social e como os
dados cadastrais podem apoiar o planejamento de parcerias do Pescadores Web?

## Fontes e recortes

Ipea/Mapa das OSCs: arquivo oficial 20260806, coleta agosto/2026 conforme portal.
IBGE: Censo 2022, população residente municipal, SIDRA tabela 4714, variável 93.
Extração em 4/11/2026. A fonte integral tem 1,113,949 CNPJs;
o filtro Area_Assistencia_social = 1 resulta em 58,184 estabelecimentos.
Há 39,836 CNPJs com situação Ativa e não removidos do Mapa.
São CNPJs de estabelecimentos, incluindo filiais, não necessariamente instituições
independentes. As áreas de atuação podem se sobrepor na base original.

O arquivo integral (343 MB) fica fora do repositório; o recorte exato de linhas e
colunas está em dados/brutos. URLs, filtros e hashes SHA-256 estão em FONTES.json.
Não há observações artificiais, erros inseridos ou preenchimento de valores faltantes
das OSCs. Zeros municipais são contagens obtidas após o cruzamento, não OSCs inventadas.

## Qualidade

| verificacao | ocorrencias |
| --- | --- |
| cnpj_invalido | 0 |
| cnpj_duplicado | 0 |
| data_fundacao_ausente_ou_invalida | 4 |
| fundacao_posterior_referencia | 0 |
| uf_invalida | 14 |
| nome_municipio_com_caractere_substituido | 24879 |
| oscs_ativas_sem_correspondencia_municipal_censo2022 | 0 |

O nome municipal do Ipea contém caracteres substituídos em parte das linhas.
Não reconstruímos grafias por palpite: agregações usam código municipal e os nomes
do IBGE. Datas inválidas/futuras ficam fora da modelagem. Linhas sem vínculo municipal
são registradas em sem_correspondencia.csv; não são redistribuídas.

## Distribuição e relação com a população

Dos 5570 municípios/territórios municipais retornados pelo Censo,
3954 têm ao menos uma OSC ativa no recorte. O DF tem
894 estabelecimentos no recorte completo, somando situações cadastrais.
As taxas relacionam numerador 2026 a denominador 2022: não são taxas oficiais de
2026. Contagem e densidade não medem capacidade de atendimento nem necessidade social.

Regressão: ln(1 + OSCs ativas) = 1.6659 × log10(população 2022)
+ -5.6601. Treino: 4456 municípios; teste:
1114. R² no teste em escala log: 0.595; MAE na
escala de contagem após transformação inversa: 3.52 OSCs.
No cálculo do MAE, previsões invertidas negativas são limitadas a zero. O gráfico
mostra a reta linear bruta; ela pode extrapolar valores negativos para municípios
pequenos. Modelos próprios para contagens são uma alternativa para a próxima etapa.
É associação transversal, sem causalidade ou previsão de crescimento futuro.

## Classificação cadastral

Alvo positivo: situação diferente de Ativa (Inapta, Suspensa ou Nula ou Baixada).
Características: idade cadastral, UF e natureza jurídica. Situação, remoção,
fechamento, razão social, CNAE e marcador matriz/filial não entram nas características.
É uma demonstração de associação cadastral; a situação real já está disponível
na fonte e deve ser consultada diretamente, sem substituir o cadastro por previsão.

Divisão por raiz do CNPJ (8 dígitos): 37228 treino, 9265 validação e 11673
teste, com 3504 positivos. Matriz e filiais não atravessam partições.
Não é teste temporal e não valida previsão de encerramento ou dificuldade financeira.
Modelo escolhido por F1 na validação, antes de usar o teste: **Arvore**.

Validação:

| modelo | acuracia | precisao | recall | f1 | auc_roc | ap |
| --- | --- | --- | --- | --- | --- | --- |
| Maioria | 0.684 | 0.000 | 0.000 | 0.000 | 0.500 | 0.316 |
| Regressao logistica | 0.570 | 0.364 | 0.483 | 0.415 | 0.555 | 0.368 |
| Arvore | 0.553 | 0.400 | 0.832 | 0.540 | 0.662 | 0.423 |
| Random Forest | 0.555 | 0.400 | 0.814 | 0.536 | 0.659 | 0.444 |

Teste após reajuste em treino + validação:

| modelo | acuracia | precisao | recall | f1 | auc_roc | ap |
| --- | --- | --- | --- | --- | --- | --- |
| Maioria | 0.700 | 0.000 | 0.000 | 0.000 | 0.500 | 0.300 |
| Regressao logistica | 0.570 | 0.339 | 0.456 | 0.389 | 0.550 | 0.343 |
| Arvore | 0.552 | 0.388 | 0.851 | 0.533 | 0.678 | 0.421 |
| Random Forest | 0.550 | 0.385 | 0.832 | 0.526 | 0.668 | 0.429 |

Precisão mede a fração de positivos previstos que se confirmam; recall mede a fração
dos não ativos identificados. AP é average precision. O limiar é fixo em 0,5.
Os resultados têm utilidade didática e não justificam negar parcerias ou atribuir
falhas operacionais a uma organização.

## K-means e aplicação ao TCC

1491 municípios com pelo menos cinco OSCs ativas são agrupados por densidade
(log), idade mediana e fração fundada desde 2010. k = 2, silhueta =
0.360. Grupos são exploratórios, sem rótulos de carência ou impacto.

O Pescadores Web pode usar os indicadores para conhecer o contexto territorial e
preparar uma lista de organizações a verificar. O painel pode ser incorporado como
contextualização; não contém doações, estoque, voluntários ou atendimentos da ONG.
Não há integração automática ao Laravel nem mensagens enviadas às organizações.

## Limitações e próxima etapa

Cadastro não comprova funcionamento, capacidade, saúde financeira ou qualidade do
serviço. Há diferença entre datas das fontes, possibilidade de desatualização e
variação de cobertura. Zero no recorte não prova ausência de assistência social.
As divisões aleatórias por grupo não eliminam dependência regional. Revalidar os
indicadores quando a base mudar, guardar os hashes e confirmar informações antes
de estabelecer uma parceria. Para analisar falta de estoque serão necessários
registros operacionais reais; essa previsão foi retirada desta versão.
