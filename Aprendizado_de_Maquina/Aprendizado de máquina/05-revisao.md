<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# Questões de revisão — Registro individual

## Identificação

- Estudante ou equipe: **Felipe Barbosa Vieira**
- Turma: **SI 7/8 Noturno — Sistemas de Informação**
- Data de realização: **16/10/2026**
- Integrantes e contribuições (se em equipe): **Não se aplica, o registro é individual.**

Responda com suas palavras e apresente os cálculos quando solicitados. Os números dos exercícios manuais não são os resultados do laboratório.

## 1. Explique a diferença entre regra programada para bloquear uma palavra e modelo de spam treinado com exemplos.

**Resposta:** Na regra programada, uma pessoa escolhe o critério ("se aparecer a palavra X, bloqueie"), e o sistema só repete essa decisão. É transparente, mas não se adapta: bloqueia mensagens legítimas que usam a palavra e deixa passar variações dela. No modelo treinado, o critério é obtido a partir de muitas mensagens já marcadas como spam ou legítimas. Ele pesa vários indícios ao mesmo tempo e pode ser atualizado com exemplos novos, mas sua qualidade depende dos rótulos, e seus erros são menos previsíveis.

## 2. Por que codificar evadiu/permaneceu como 1/0 não transforma classificação em regressão?

**Resposta:** O número é só uma etiqueta para a categoria. A tarefa continua sendo escolher entre duas classes: não existe valor 0,5 com significado, e "1 − 0" não mede quantidade alguma. Se eu tratasse como regressão e calculasse MAE, estaria medindo distância entre etiquetas. O que se avalia é a classe certa ou errada, com matriz de confusão, acurácia e sensibilidade.

## 3. Uma biblioteca quer estimar empréstimos e descobrir perfis. Que tarefas correspondem a cada pergunta?

**Resposta:** Estimar empréstimos é **regressão**: supervisionada, com alvo numérico (quantidade por semana). Descobrir perfis é **agrupamento**: não supervisionado, sem alvo, procurando grupos de usuários ou de padrões de uso que ninguém definiu antes.

## 4. O que são atributo, alvo e unidade de análise no laboratório educacional?

**Resposta:** A **unidade de análise** é o estudante fictício: cada linha do conjunto. Os **atributos** são o que se sabe dele na semana 4 e entra no modelo: `frequencia_sem4`, `nota_sem4` e `entregas_sem4`. O **alvo** é o que se quer prever e só é conhecido no fim do semestre: `evasao_fim_semestre` (0 = permaneceu, 1 = evadiu).

## 5. Por que calcular a mediana antes de dividir os dados pode invalidar a avaliação?

**Resposta:** A mediana calculada com todas as linhas inclui as notas do teste. Os registros de treino seriam preenchidos com um valor que já "conhece" o teste, e o teste deixaria de ser totalmente novo. Isso é vazamento de dados. Com 30 ausências o efeito pode ser pequeno, mas o procedimento fica errado e tende a deixar a avaliação otimista. O correto é aprender a mediana só no treino (no notebook, com `SimpleImputer` dentro do `Pipeline`) e apenas aplicá-la ao teste.

## 6. Em uma matriz didática com TN=80, FP=5, FN=10, TP=5, calcule acurácia e sensibilidade. O resultado é suficiente para aprovar o modelo?

**Resposta:**
- Total: 80 + 5 + 10 + 5 = 100 casos, dos quais 15 positivos (FN + TP).
- Acurácia = (TN + TP) / total = (80 + 5) / 100 = **0,85**.
- Sensibilidade = TP / (TP + FN) = 5 / (5 + 10) = 5 / 15 ≈ **0,333**.

Não é suficiente. Prever sempre negativo daria (80 + 5) / 100 = 0,85, a mesma acurácia, sem esforço algum. O modelo encontra só 1 de cada 3 positivos. Antes de aprovar, eu compararia com essa referência, discutiria o custo dos 10 falsos negativos e avaliaria em outro conjunto. Com 15 positivos, a sensibilidade ainda é muito instável.

## 7. Valores reais 100, 120, 140 e previsões 110, 115, 130. Calcule MAE e informe a unidade se o alvo for vendas em reais.

**Resposta:**
- Erros absolutos: |100 − 110| = 10; |120 − 115| = 5; |140 − 130| = 10.
- MAE = (10 + 5 + 10) / 3 = 25 / 3 ≈ **R$ 8,33**.

Em média, cada previsão se afasta R$ 8,33 do valor real, para cima ou para baixo. O MAE fica na mesma unidade do alvo.

## 8. Um R² de -0,2 significa “20% de acertos negativos”? Explique.

**Resposta:** Não. O R² não conta acertos. Ele vale 1 − (erro quadrático do modelo / erro quadrático de prever sempre a média do conjunto avaliado). Com R² = −0,2, essa razão é 1,2, ou seja, o modelo erra 20% **mais** (em soma de quadrados) do que simplesmente usar a média. Seria melhor descartar o modelo e usar a média.

## 9. Uma árvore tem acurácia 1,00 no treino e 0,65 na validação. Que hipótese investigar e como?

**Resposta:** A hipótese principal é **sobreajuste**: a árvore criou regras para cada caso do treino, inclusive para o ruído. Como investigar: comparar por validação cruzada no treino versões com `max_depth` menor e `min_samples_leaf` maior, observando se a distância treino–validação cai e a validação sobe. No meu laboratório, a folha 40 reduziu essa distância de 0,154 para 0,047. Também verificaria se a validação supera a referência, se há poucos dados por classe e se algum atributo funciona como identificador (um código único permite "decorar" cada linha).

## 10. Por que escolher a profundidade pelo teste prejudica a estimativa final?

**Resposta:** Quando o teste ajuda a escolher, ele vira parte do ajuste. A profundidade escolhida será a que deu sorte nesses 150 registros, e a acurácia de teste reportada fica inflada. Não sobra nenhum dado novo para estimar o desempenho honestamente. A escolha deve ser feita na validação do treino, e o teste é aberto uma vez, no fim. Se depois disso eu quiser trocar o modelo, preciso de outro conjunto de teste.

## 11. Baixa frequência associada à evasão demonstra causa? Proponha explicação alternativa.

**Resposta:** Não. A associação é compatível com várias histórias. Explicação alternativa: um estudante que passa a cuidar de um familiar doente começa a faltar e, mais tarde, abandona o curso. A causa das duas coisas é a sobrecarga em casa, não as faltas. Também pode haver causalidade invertida: quem já decidiu sair deixa de ir às aulas. Nesses casos, cobrar presença não resolveria nada.

## 12. Um modelo sinaliza um estudante como possível evasão. Que ação responsável pode ser adotada?

**Resposta:** Alguém da equipe de apoio confere o caso e envia um convite neutro e opcional (monitoria, orientação, informação sobre auxílios), sem mencionar "risco de evasão". O estudante pode recusar sem consequência e pode pedir para ver e corrigir os dados usados. A sinalização nunca altera nota, matrícula ou bolsa, a lista fica com acesso restrito e é apagada ao fim do semestre.

## Fontes adicionais consultadas

- Material do Módulo IV e notebook didático (Profa. Kadidja Valéria, UDF, 2026.2).
- SCIKIT-LEARN. *User Guide* e *Common pitfalls and recommended practices*. Disponível em: https://scikit-learn.org/stable/. Acesso em: 16 out. 2026.
- Os números do laboratório citados na questão 9 vêm do meu [notebook executado](notebooks/laboratorio-equipe.ipynb).
- Uso de ferramentas de IA: **PREENCHER pelo estudante**

[Voltar ao início](README.md).
