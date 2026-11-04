-- SQLite. Registros reais do Ipea; população real do Censo IBGE 2022.
-- CONSULTA 01_situacao_cadastral
SELECT situacao_cadastral, COUNT(*) AS estabelecimentos
FROM oscs GROUP BY situacao_cadastral ORDER BY estabelecimentos DESC;

-- CONSULTA 02_ativas_por_uf
SELECT uf, SUM(oscs_ativas) AS oscs_ativas
FROM municipios GROUP BY uf ORDER BY oscs_ativas DESC;

-- CONSULTA 03_densidade_por_uf
SELECT uf, SUM(oscs_ativas) AS oscs_ativas, SUM(populacao_2022) AS populacao_2022,
ROUND(100000.0*SUM(oscs_ativas)/SUM(populacao_2022),2) AS oscs_por_100mil
FROM municipios GROUP BY uf ORDER BY oscs_por_100mil DESC;

-- CONSULTA 04_maiores_contagens_municipais
SELECT cd_municipio, municipio, oscs_ativas, populacao_2022,
ROUND(oscs_por_100mil,2) AS oscs_por_100mil
FROM municipios ORDER BY oscs_ativas DESC LIMIT 20;

-- CONSULTA 05_distrito_federal
SELECT situacao_cadastral, COUNT(*) AS estabelecimentos
FROM oscs WHERE uf='DF' GROUP BY situacao_cadastral ORDER BY estabelecimentos DESC;

-- CONSULTA 06_natureza_juridica
SELECT natureza_juridica, COUNT(*) AS estabelecimentos,
SUM(ativa_no_mapa) AS ativas_no_mapa
FROM oscs GROUP BY natureza_juridica ORDER BY estabelecimentos DESC;

-- CONSULTA 07_integridade
SELECT COUNT(*) AS linhas, COUNT(DISTINCT cnpj) AS cnpjs_distintos,
SUM(CASE WHEN idade_anos<0 THEN 1 ELSE 0 END) AS datas_futuras
FROM oscs;

-- CONSULTA 08_faixas_idade
SELECT CASE WHEN idade_anos<10 THEN '01: menos de 10'
WHEN idade_anos<20 THEN '02: 10 a 19'
WHEN idade_anos<30 THEN '03: 20 a 29'
ELSE '04: 30 ou mais' END AS faixa, COUNT(*) AS oscs_ativas
FROM oscs WHERE ativa_no_mapa=1 AND idade_anos>=0
GROUP BY faixa ORDER BY faixa;
