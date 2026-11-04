# Dicionário da análise com dados reais

O recorte preserva valores de 11 colunas do arquivo do Ipea. O delimitador original
é ponto e vírgula; o recorte usa vírgula. A fonte mistura caracteres válidos e
caracteres inválidos em nomes municipais. A decodificação usa UTF-8 com substituição
explícita de bytes inválidos; não se inventam nomes para reparar a fonte.

| Campo original Ipea | Uso |
|---|---|
| cnpj | Identificador público do estabelecimento, preservado como texto de 14 dígitos |
| tx_razao_social_osc | Razão social pública; não usada como característica preditiva |
| natureza_juridica | Código cadastral; tratado como categoria, não quantidade |
| matriz_filial | Identificação fornecida pela fonte; excluída dos preditores |
| situacao_cadastral | Ativa, Inapta, Suspensa ou Nula ou Baixada; alvo observado |
| dt_fundacao_osc | Data de fundação; transformada em idade na referência 31/08/2026 |
| removida_do_mosc | Marca de remoção do Mapa; nunca usada como preditor |
| cd_municipio | Código municipal usado na junção com o IBGE |
| municipio_nome | Nome na fonte; preservado mesmo com grafia corrompida |
| UF_Sigla | Unidade da Federação; característica categórica |
| Area_Assistencia_social | Marcador que define o recorte: igual a 1 |

A página oficial oferece um dicionário XLSX amplo, com campos de diferentes tabelas
da plataforma; a presença e os nomes no CSV desta extração são documentados acima.

## Campos derivados

| Campo | Regra |
|---|---|
| cnpj_raiz | Primeiros 8 dígitos do CNPJ; grupo da divisão dos conjuntos |
| nao_ativa | 1 se situação cadastral não é Ativa; 0 se é Ativa |
| ativa_no_mapa | Situação Ativa e removida_do_mosc igual a não |
| idade_anos | Dias entre fundação e 31/08/2026 divididos por 365,25 |
| ano_fundacao | Ano extraído da data; ausente quando a data é inválida |
| oscs_ativas | Contagem de CNPJs ativos e não removidos por município |
| populacao_2022 | Valor observado V do IBGE, Censo 2022 |
| oscs_por_100mil | oscs_ativas / populacao_2022 × 100.000 |
| idade_mediana | Mediana da idade das OSCs ativas no município |
| fracao_fundadas_2010 | Fração das OSCs ativas fundada em 2010 ou depois |

Os nomes oficiais municipais usados no painel vêm de D1N do IBGE; os códigos são
D1C. A UF é o sufixo da identificação municipal do IBGE. A primeira linha da API
contém rótulos, não um município, e é removida antes da análise. A UF ausente na
linha do Ipea não impede uma agregação territorial se o código municipal for válido;
a UF territorial é a do município do IBGE. A classificação usa a UF cadastral e
exclui registros com esse campo ausente.

Municípios do Censo sem correspondência de OSC ativa recebem contagem zero. As
idades e frações desses municípios continuam ausentes. Não se imputam valores de
registros individuais. Sem dados de fundação válidos não há entrada na classificação.

## Avaliação

Somente idade_anos, UF e natureza_juridica entram nos classificadores. Alvo positivo:
não ativa. As raízes de CNPJ são disjuntas entre treino, validação e teste. A escolha
é pelo F1 da validação, com limiar fixo de 0,5. Reajuste em treino + validação, depois
avaliação final no teste. Não há corte temporal, dados de demanda ou previsão de risco
financeiro. K-means usa densidade em log, idade mediana e fração desde 2010 em 1.491
municípios com pelo menos cinco OSCs ativas.
