<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# Módulo IV — Exercícios realizados

Este repositório registra as atividades de introdução ao Machine Learning e de aprendizado supervisionado. Preencha os modelos com suas próprias respostas e evidências de execução. Os arquivos contêm enunciados e campos de registro, sem gabarito.

## Identificação do repositório

- Estudante ou equipe: **Felipe Barbosa Vieira** (trabalho individual)
- Turma: **SI 7/8 Noturno — Sistemas de Informação**
- Repositório: **[lipefe11/Ciencia_Dados_Aprendizagem_Maquina](https://github.com/lipefe11/Ciencia_Dados_Aprendizagem_Maquina)**. O conteúdo fica na pasta `Aprendizado_de_Maquina/Aprendizado de máquina/`.
- Contexto usado nas aplicações: meu TCC **Pescadores Web**, desenvolvido em dupla com Calebe Mendes Bezerra ([definição do projeto](../../Unidade_4/Definicao_Projeto_PescadoresWeb_v2.docx)), e o meu [projeto de ciência de dados com dados públicos do Ipea e do IBGE](../../Projeto_ciencia_de_dados/README.md).

## Atividades

| Arquivo | Entregável |
| --- | --- |
| [01-aula1-conceitos.md](01-aula1-conceitos.md) | Quadro comparativo e classificação justificada de pelo menos cinco problemas |
| [02-pbl-biblioteca.md](02-pbl-biblioteca.md) | Canvas da investigação |
| [03-aula2-laboratorio.md](03-aula2-laboratorio.md) | Registro do modelo, métricas, erros e experimentos em Python |
| [04-pbl-permanencia.md](04-pbl-permanencia.md) | Proposta de apoio educacional, com avaliação e limites |
| [05-revisao.md](05-revisao.md) | Respostas individuais às questões de revisão |
| [06-autoavaliacao.md](06-autoavaliacao.md) | Checklist, contribuições e reflexão final |
| [07-aplicacao-pescadores-web.md](07-aplicacao-pescadores-web.md) | Aplicação dos conceitos ao TCC Pescadores Web: classificação de municípios sem OSC de assistência social ativa, com dados reais do Ipea e do IBGE |

## Arquivos de apoio

| Arquivo | Conteúdo | Colab |
| --- | --- | --- |
| [notebooks/laboratorio.ipynb](notebooks/laboratorio.ipynb) | Notebook didático da professora, sem alterações | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lipefe11/Ciencia_Dados_Aprendizagem_Maquina/blob/main/Aprendizado_de_Maquina/Aprendizado%20de%20m%C3%A1quina/notebooks/laboratorio.ipynb) |
| [notebooks/laboratorio-equipe.ipynb](notebooks/laboratorio-equipe.ipynb) | Minha execução do laboratório, com os exercícios de investigação, dois experimentos próprios e as interpretações | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lipefe11/Ciencia_Dados_Aprendizagem_Maquina/blob/main/Aprendizado_de_Maquina/Aprendizado%20de%20m%C3%A1quina/notebooks/laboratorio-equipe.ipynb) |
| [notebooks/pescadores-web-municipios-sem-osc.ipynb](notebooks/pescadores-web-municipios-sem-osc.ipynb) | Experimento da atividade 07 (dados públicos reais) | [![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lipefe11/Ciencia_Dados_Aprendizagem_Maquina/blob/main/Aprendizado_de_Maquina/Aprendizado%20de%20m%C3%A1quina/notebooks/pescadores-web-municipios-sem-osc.ipynb) |

- [CSV sintético](dados/educacionais-sinteticos.csv): mesmos 600 registros fictícios da prática de classificação, para uso no Orange. O notebook confere que a simulação reproduz esse arquivo.
- [Tabela municipal de OSCs](dados/municipios_oscs_assistencia.csv): 5.570 municípios com população do Censo 2022 e contagem de OSCs de assistência social ativas (Mapa das OSCs/Ipea, arquivo 20260806). É uma cópia de cinco colunas de `Projeto_ciencia_de_dados/dados/tratados/municipios.csv`. Procedência, filtros e hashes estão em [FONTES.json](../../Projeto_ciencia_de_dados/dados/brutos/FONTES.json).
- [notebooks/resultados_execucao.json](notebooks/resultados_execucao.json) e [notebooks/resultados_pescadores_web.json](notebooks/resultados_pescadores_web.json): números gravados pelas execuções.
- `assets/`: logomarca e figuras geradas pelos notebooks: [matriz de confusão](assets/matriz-confusao.png), [árvore](assets/arvore.png), [observado × previsto](assets/regressao-observado-previsto.png), [resíduos](assets/regressao-residuos.png), [matriz da atividade 07](assets/pescadores-web-matriz.png) e [árvore da atividade 07](assets/pescadores-web-arvore.png).

**Todos os registros educacionais são sintéticos. Não representam estudantes reais da UDF.** A atividade 07 usa somente dados públicos agregados, sem pessoas físicas, e nenhum registro inventado. O Pescadores Web ainda não tem dados operacionais.

## Como colocar no GitHub

1. Extraia o ZIP no computador e abra a pasta `Exercicios_ML_UDF`.
2. Neste repositório, o conteúdo foi colocado em `Aprendizado_de_Maquina/Aprendizado de máquina/`, ao lado das pastas das outras unidades.
3. Use **Add file > Upload files** e envie o conteúdo da pasta, incluindo as subpastas.
4. Registre um commit, por exemplo `Adiciona modelos das atividades do módulo IV`.
5. Abra cada `.md`, clique no lápis de edição, preencha os campos e confira a prévia. Registre um commit que descreva o exercício realizado.
6. No Colab, abra o notebook pelo botão **Abrir no Colab**, execute as células na ordem e acrescente suas interpretações em células Markdown. Baixe o `.ipynb` e envie para `notebooks/laboratorio-equipe.ipynb`. Localmente, dentro de `notebooks/`, rode `jupyter nbconvert --to notebook --execute --inplace laboratorio-equipe.ipynb`.
7. Se usar Orange, envie o fluxo `.ows` e imagens de resultados, e preencha o relatório da atividade 03. Informe o caminho real dos arquivos. Neste repositório foi usado apenas o percurso Python.
8. Atualize os links das evidências, confira se abrem no GitHub e envie o endereço do repositório no ambiente indicado pela professora.

Os notebooks procuram os dados primeiro nas pastas do repositório. No Colab, baixam os arquivos do GitHub e gravam as figuras em `./assets/`.

## Convenções de registro

- Substitua **PREENCHER** pelo seu registro. Use “não se aplica” com justificativa quando necessário.
- Mantive os enunciados e acrescentei as respostas nos espaços indicados.
- Separo **resultado calculado**, **interpretação** e **hipótese**.
- Os valores citados são os das execuções salvas: Python 3.13.18, scikit-learn 1.9.1, pandas 3.0.5, NumPy 2.5.3, matplotlib 3.11.2, semente 42.
- Não há matrículas, telefones, credenciais nem dados pessoais. A tabela da atividade 07 é agregada por município.
- As fontes consultadas estão referenciadas em cada atividade. A declaração sobre uso de ferramentas de IA está em [06-autoavaliacao.md](06-autoavaliacao.md).

## Situação das entregas

- [x] Aula 1: quadro comparativo e problemas justificados.
- [x] PBL Biblioteca em Foco.
- [x] Aula 2: notebook e relatório.
- [x] PBL Apoio à Permanência.
- [x] Revisão e autoavaliação.
- [x] Aplicação ao TCC (Pescadores Web).

## Fonte da atividade

Material do estudante do Módulo IV — Aprendizado de Máquina. Profa. Kadidja Valéria, UDF, 2026. Consulte as referências do material e a documentação oficial indicada nas atividades.
