<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# Autoavaliação e conferência da entrega

## Identificação

- Estudante ou equipe: **Felipe Barbosa Vieira**
- Turma: **SI 7/8 Noturno — Sistemas de Informação**
- Data de realização: **16/10/2026**
- Integrantes e contribuições (se em equipe): **Não se aplica, o trabalho é individual.**

## Checklist

- [x] Diferenciei IA, Ciência de Dados e ML com um exemplo.
- [x] Completei o quadro supervisionado/não supervisionado.
- [x] Justifiquei pelo menos cinco situações-problema.
- [x] Registrei a investigação da biblioteca.
- [x] Identifiquei atributos, alvo, unidade e momento da previsão.
- [x] Executei e documentei a prática em Python ou Orange.
- [x] Escolhi configurações usando treino/validação.
- [x] Mantive o teste fora do ajuste e da seleção.
- [x] Interpretei acurácia, matriz, MAE e R².
- [x] Comparei com uma referência e discuti erros.
- [x] Registrei limitações, dados sintéticos, privacidade e vieses.
- [x] Formulei recomendações de apoio com revisão humana.
- [x] Respondi às questões individuais.
- [x] Conferi os links e os arquivos de evidências.
- [ ] Substituí os campos PREENCHER ou justifiquei os não aplicáveis. *(Falta a declaração sobre uso de IA, aqui e na [revisão](05-revisao.md).)*

## Reflexão individual

- O que aprendi e consigo explicar: **Separar o teste antes de qualquer cálculo; fixar a regra de escolha antes de ver os números; ler uma matriz de confusão pensando no custo de cada tipo de erro; e comparar sempre com uma referência simples, que pode ser um `DummyClassifier` ou uma regra escrita à mão. Na [atividade 07](07-aplicacao-pescadores-web.md), a regra "população < 10.500" empatou em F1 com a árvore, e isso me mostrou que nem todo problema pede ML.**
- Qual foi minha principal dificuldade: **Aceitar que uma diferença de 0,007 na validação não significa nada. A validação repetida mostrou que a configuração que eu tinha escolhido não era melhor que a do roteiro, e precisei registrar isso sem trocar o modelo depois de ver o teste.**
- Qual evidência mostra meu avanço: **O [notebook executado](notebooks/laboratorio-equipe.ipynb), com a grade completa antes do teste, a validação repetida e a curva de aprendizado; o cálculo manual 117/150 = 0,78 e 47/61 ≈ 0,770 no [registro do laboratório](03-aula2-laboratorio.md); e o [experimento com dados reais](07-aplicacao-pescadores-web.md), em que reportei um resultado modesto.**
- Como contribuímos com a equipe: **Trabalho individual. Liguei o módulo ao TCC Pescadores Web, que desenvolvo com Calebe Mendes Bezerra, e ao meu projeto de ciência de dados, reaproveitando a base pública já preparada lá.**
- O que preciso revisar: **Validação com dependência espacial e temporal (o `GroupKFold` por UF da atividade 07 mostrou como a validação comum pode ser otimista), escolha de limiar de decisão e métricas para classes raras, como precisão média.**
- Ferramentas de apoio utilizadas, incluindo IA quando houver, e como verifiquei as respostas: **Python 3.13.18, Jupyter/nbconvert (os notebooks também abrem no Google Colab), scikit-learn 1.9.1, pandas 3.0.5, NumPy 2.5.3 e matplotlib 3.11.2. Consultei a documentação do scikit-learn (User Guide e Common pitfalls) e o material da disciplina. Verifiquei os números reexecutando os notebooks do início ao fim com a semente 42 e refazendo à mão os cálculos da matriz. Uso de ferramentas de IA: PREENCHER pelo estudante.**

## Critérios de avaliação

Escala sugerida do material: nível 3 consistente, 2 adequado com lacunas, 1 parcial, 0 ausente/incoerente. Nota do critério = peso × nível/3. A professora pode ajustar a aplicação.

| Critério | Peso aula 1 | Peso aula 2/PBL |
| --- | --- | --- |
| Problema e conceitos | 3,0 | 2,0 |
| Dados e justificativa | 2,0 | 2,0 |
| Método e avaliação | 1,0 | 3,0 |
| Interpretação e responsabilidade | 2,0 | 2,0 |
| Clareza e colaboração | 2,0 | 1,0 |
| Total | 10,0 | 10,0 |

Na aula 1, método corresponde à avaliação proposta. Na aula 2, inclui execução e interpretação. A maior acurácia isolada não assegura a melhor avaliação da atividade.

## Fontes de apoio

- SCIKIT-LEARN. *User Guide*. https://scikit-learn.org/stable/user_guide.html.
- SCIKIT-LEARN. *Common pitfalls and recommended practices*. https://scikit-learn.org/stable/common_pitfalls.html.
- ORANGE DATA MINING. *Test and Score*. https://orangedatamining.com/widget-catalog/evaluate/testandscore/.

Referências indicadas no material didático do módulo, consultadas em 14 out. 2026. Registre a data da sua própria consulta quando utilizar novas fontes.

[Voltar ao início](README.md).
