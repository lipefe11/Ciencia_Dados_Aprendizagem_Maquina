<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# Aula 1 — Conceitos e classificação de problemas

## Identificação

- Estudante ou equipe: **Felipe Barbosa Vieira**
- Turma: **SI 7/8 Noturno — Sistemas de Informação**
- Data de realização: **16/10/2026**
- Integrantes e contribuições (se em equipe): **Não se aplica, o trabalho é individual. Na seção 5 uso o meu TCC, o Pescadores Web, que desenvolvo em dupla com Calebe Mendes Bezerra.**

## Objetivos

Distinguir programação tradicional e Machine Learning, identificar atributos e alvo e diferenciar classificação, regressão e agrupamento.

## 1. Explicação com suas palavras

1. Como um modelo aprende com dados? **Na programação comum, eu escrevo a regra e o computador aplica. No aprendizado de máquina eu forneço exemplos e um procedimento de ajuste, e a regra sai dos exemplos. O procedimento testa, por exemplo, várias perguntas do tipo "nota menor que 6?" e fica com as que mais reduzem os erros nos exemplos de treino. Quando os exemplos trazem a resposta certa (aprendizado supervisionado), o erro é medido contra essa resposta. Aprender, aqui, quer dizer acertar casos **novos**. Por isso sempre separo uma parte dos dados que o ajuste não pode ver e meço o desempenho nela.**
2. Qual diferença entre algoritmo e modelo? **O algoritmo é o método genérico, como "árvore de decisão" ou "regressão linear". Ele não sabe nada sobre evasão nem sobre bibliotecas. O modelo é o objeto concreto que o algoritmo produz depois de olhar um conjunto de dados: no meu laboratório, uma árvore de profundidade 5 com folhas de pelo menos 40 estudantes, com limites numéricos já fixados em cada pergunta. O mesmo algoritmo aplicado a outra turma geraria outro modelo.**
3. Compare uma regra de bloqueio de palavra com um modelo de spam. **Uma regra como "bloquear mensagens com 'Pix grátis'" é programação tradicional: alguém decidiu o critério, e ele é fácil de auditar. Mas a regra só enxerga o que foi previsto. Basta escrever "P1x gr4tis" para passar, e uma mensagem legítima que cite a expressão é barrada. Um modelo de spam é treinado com mensagens já marcadas como spam ou legítimas e combina muitos indícios ao mesmo tempo: palavras, links, remetente, horário de envio. Ele se adapta quando é retreinado, mas herda os erros de rotulação, não explica tão facilmente por que bloqueou e também erra.**
4. Dê um exemplo de atributo e alvo e defina o momento da previsão. **No laboratório da aula 2, os atributos são `frequencia_sem4`, `nota_sem4` e `entregas_sem4`, e o alvo é `evasao_fim_semestre`. A previsão é feita ao fim da semana 4, e o alvo só existe no fim do semestre. Um exemplo **hipotético** no Pescadores Web: atributos = dia da semana da ação, ponto de distribuição e número de voluntários confirmados; alvo = quantidade de marmitas efetivamente entregues. A previsão aconteceria na véspera da ação, quando a equipe decide quanto cozinhar. O sistema ainda não tem esses registros: é uma possibilidade futura, não um dado existente.**

## 2. Quadro comparativo

| Critério | Supervisionado | Não supervisionado |
| --- | --- | --- |
| Presença de alvo no treino | Há. Cada exemplo de treino vem com o desfecho já observado. | Não há. Os exemplos trazem apenas atributos. |
| Pergunta que pode responder | "Que resposta espero para este caso novo?" | "Que estrutura existe neste conjunto?" |
| Tipo de saída | Uma classe (classificação) ou um número (regressão). | Um rótulo de grupo sem nome prévio, uma redução de dimensões ou um sinal de caso atípico. |
| Tarefas e exemplo | Classificação: o item de estoque vai acabar antes da próxima ação (sim/não). Regressão: quantas marmitas serão entregues. | Agrupamento: padrões de participação de voluntários. Detecção de anomalias: uma doação registrada com quantidade muito fora do comum, que pode ser erro de digitação. |
| Dados necessários | Histórico com o desfecho registrado de forma consistente e atributos que já existem no momento da previsão. | Atributos comparáveis (na mesma escala ou padronizados) e casos em número suficiente para os padrões se repetirem. |
| Forma de avaliação | Previsões comparadas com o alvo real em dados separados (acurácia, matriz de confusão, sensibilidade, MAE, R²) e sempre contra uma referência simples. | Medidas internas, como a silhueta, e sobretudo a avaliação de quem conhece o domínio: os grupos fazem sentido e ajudam alguma decisão? |
| Limitação | Depende de rótulos, que custam caro e podem estar errados ou enviesados. Também supõe que o futuro se parece com o histórico. | Não existe gabarito. Mudando os atributos ou a escala, mudam os grupos, e um grupo pode não ter utilidade prática. |

## 3. Situações-problema

| Caso | Situação-problema |
| --- | --- |
| 1 Educação | Prever evadiu/permaneceu com histórico rotulado de turmas anteriores. |
| 2 Saúde | Estimar o tempo de espera em minutos a partir de registros de atendimento. |
| 3 Comércio | Descobrir perfis de compra sem categorias prévias de clientes. |
| 4 Finanças | Prever inadimplente/adimplente com contratos e desfechos conhecidos. |
| 5 Segurança digital | Distinguir spam/legítima com mensagens já revisadas. |
| 6 Comércio | Estimar o total de vendas em reais na próxima semana. |
| 7 Educação | Agrupar perfis de acesso ao ambiente virtual sem rótulo de evasão. |
| 8 Saúde | Classificar exames em categorias previamente definidas por especialistas. |

| Caso escolhido | Alvo ou ausência de alvo | Categoria, quantidade ou grupos? | Abordagem e justificativa | Dados necessários e limitação |
| --- | --- | --- | --- | --- |
| 1 Educação | Alvo: evadiu ou permaneceu | Categoria (duas classes) | Supervisionado, **classificação binária**. Turmas encerradas já mostram quem saiu. Codificar como 0/1 não muda a natureza da tarefa. | Frequência, notas e entregas observadas até a data da previsão, de semestres anteriores. Limitação: a definição de evasão varia (trancamento, transferência). Além disso, dados de um curso podem não valer para outro. |
| 3 Comércio | Sem alvo | Grupos | Não supervisionado, **agrupamento**. A loja não sabe de antemão quais tipos de cliente existem. | Indicadores agregados por cliente: compras por mês, gasto médio, dias desde a última compra, mix de categorias. Limitação: cliente novo tem pouco histórico, e o número de grupos é uma decisão humana. Os grupos precisam ser validados pela equipe de vendas. |
| 4 Finanças | Alvo: inadimplente ou adimplente | Categoria | Supervisionado, **classificação**. Contratos já encerrados têm o desfecho registrado. | Valor, prazo, renda informada e histórico de pagamento. Limitação: só se conhece o desfecho de quem foi aprovado. Quem foi recusado nunca gerou rótulo. O modelo também pode repetir discriminações do passado, o que exige auditoria. |
| 5 Segurança digital | Alvo: spam ou legítima | Categoria | Supervisionado, **classificação**. Mensagens revisadas por pessoas fornecem os rótulos. | Texto, remetente, links e anexos. Limitação: os golpistas mudam de estratégia, então o modelo envelhece rápido. O spam pode ser raro na caixa, e aí a acurácia sozinha engana. |
| 7 Educação | Sem alvo (não há rótulo de evasão) | Grupos | Não supervisionado, **agrupamento** dos padrões de acesso. Serve para entender os usos do ambiente virtual, não para prever quem sai. | Acessos por semana, horários, tipos de material abertos, intervalo entre acessos. Limitação: um grupo de "pouco acesso" pode reunir quem baixa tudo de uma vez e estuda offline. Logs são dados pessoais e pedem minimização. |

## 4. Raciocínio crítico

“Detectar fraude” define sozinho o tipo de aprendizado? **Não. O nome descreve o objetivo, mas o tipo de aprendizado depende de haver ou não um rótulo confiável nos dados. Com um histórico de operações investigadas e marcadas como fraude confirmada ou legítima, cabe classificação supervisionada. Ela tende a reconhecer bem os golpes que já aconteceram, sofre com o desbalanceamento (fraudes são poucas, e um modelo que diz sempre "legítima" parece ótimo pela acurácia) e pode falhar diante de um golpe inédito. Sem rótulos, dá para procurar operações que fogem do padrão (detecção de anomalias). Isso pode revelar golpes novos, mas uma operação incomum não é necessariamente fraude: pode ser só uma compra de fim de ano. Nos dois casos, o resultado deveria disparar uma verificação humana, e não uma punição automática. Também é possível começar sem supervisão e, à medida que os alertas são investigados, acumular rótulos para um classificador.**

## 5. Conexão com o meu TCC — Pescadores Web

O **Pescadores Web** é o sistema web gratuito (Laravel, FilamentPHP e MySQL) que desenvolvo com Calebe Mendes Bezerra para uma ação social voluntária do Distrito Federal que distribui marmitas, roupas e brinquedos. Ele centraliza voluntários, doações, estoque e ações, com dashboard para os gestores e página pública com estatísticas agregadas. **O sistema ainda não acumulou registros operacionais.** Por isso, as linhas abaixo são **propostas** para quando houver histórico, e não análises realizadas. Antes de qualquer modelo, vêm os indicadores descritivos e o alerta de estoque mínimo que já estão no escopo do TCC.

| Problema no Pescadores Web | Alvo ou ausência de alvo | Categoria, quantidade ou grupos? | Abordagem e justificativa | Dados necessários e limitação |
| --- | --- | --- | --- | --- |
| Estimar quantas marmitas preparar para a próxima ação | Alvo: marmitas entregues na ação | Quantidade | Supervisionado, **regressão**. Cada ação encerrada registra o total entregue. Ajudaria a evitar falta ou desperdício de comida. | Data, ponto de distribuição, voluntários confirmados, entregas de ações anteriores no mesmo ponto. Limitação: com poucas dezenas de ações por ano, a média das últimas ações pode ser tão boa quanto um modelo. A divisão precisa respeitar a ordem do tempo. Além disso, o total entregue é limitado pelo que foi preparado: se acabou, a demanda real ficou acima do registrado. |
| Sinalizar itens de estoque com risco de acabar antes da próxima ação | Alvo: o item zerou ou não antes da ação seguinte | Categoria | Supervisionado, **classificação binária**. Complementa o alerta de estoque mínimo, que é uma regra fixa, considerando o ritmo de saídas e de doações. | Movimentações de entrada e saída por item, datas das ações, nível mínimo cadastrado. Limitação: o rótulo só existe depois de várias ações. Uma regra simples ("saída média das últimas ações maior que o saldo") é a referência que o modelo teria de superar. |
| Entender padrões de participação de voluntários e doadores | Sem alvo | Grupos | Não supervisionado, **agrupamento**. Não existe categoria prévia de "perfil de voluntário". Poderia orientar a comunicação, por exemplo convites para ações pontuais ou para recorrentes. | Participações por mês, tempo desde a última ação, tipo de doação, sempre agregados. Limitação: são dados pessoais (LGPD). Os grupos não podem virar ranking nem rótulo de "bom" ou "mau" voluntário, e o resultado deve ser visto só pelos gestores. |
| Reconhecer municípios sem OSC de assistência social ativa no cadastro, para planejar parcerias | Alvo: nenhuma OSC ativa ou pelo menos uma | Categoria | Supervisionado, **classificação**. Este é o único item testado com dados reais (Ipea e IBGE), na [atividade 07](07-aplicacao-pescadores-web.md). | População do Censo 2022 e região. Limitação: o cadastro já mostra a situação de cada município, então o modelo serve para entender o padrão, não para substituir a consulta. Zero no cadastro não prova ausência de atendimento. |

## Entrega

Salve este arquivo preenchido. Critérios: distinção conceitual, pertinência dos dados, justificativa e clareza. [Voltar ao início](README.md).
