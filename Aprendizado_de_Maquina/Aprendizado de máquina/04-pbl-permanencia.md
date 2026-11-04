<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# PBL integrador — Apoio à Permanência

## Identificação

- Estudante ou equipe: **Felipe Barbosa Vieira**
- Turma: **SI 7/8 Noturno — Sistemas de Informação**
- Data de realização: **16/10/2026**
- Integrantes e contribuições (se em equipe): **Não se aplica, o trabalho é individual. Elaborei todas as seções da proposta a partir do meu notebook de laboratório.**

## Contexto

Uma instituição quer compreender sinais associados à evasão e oferecer apoio antes do fim do semestre. Público-alvo: estudantes matriculados e equipe de apoio acadêmico. O cenário é didático e a prática usa dados sintéticos.

**Questão norteadora:** como identificar situações que merecem atenção e oferecer apoio, reconhecendo erros do modelo e dificuldades que os dados não capturam?

## Proposta da equipe

### 1. Delimitação

- Problema e público: **A equipe de apoio acadêmico costuma descobrir que um estudante abandonou o curso só quando ele já deixou de aparecer. Os beneficiários são os estudantes matriculados. A equipe de apoio é quem usa a informação, e a coordenação define as regras de uso.**
- Decisão que o resultado pode apoiar: **A ordem e o tipo de contato na semana 5: quem recebe primeiro uma mensagem convidando para monitoria, plantão de dúvidas ou conversa com a orientação, dentro do número de contatos que a equipe consegue fazer.**
- Definição de evasão, unidade e horizonte: **Evasão = não renovar a matrícula para o semestre seguinte nem concluir o curso, sem pedido formal de trancamento ou transferência. Trancamento e transferência são registrados à parte, porque pedem outro tipo de acompanhamento. Unidade: estudante em um semestre letivo. Horizonte: dados até a semana 4 para prever a situação na rematrícula.**

### 2. Perguntas de negócio

1. **Com os registros acadêmicos das quatro primeiras semanas, quais estudantes têm estimativa mais alta de não seguir para o semestre seguinte e deveriam ser contatados primeiro?**
2. **Entre os sinalizados, qual sinal pesa mais (nota baixa, frequência baixa ou poucas entregas), para que o convite ofereça o apoio certo: reforço de conteúdo, conversa sobre rotina e horários ou ajuda com prazos?**

### 3. Dados necessários

| Dado | Papel no projeto | Disponível quando? | Origem pretendida | Necessidade e risco |
| --- | --- | --- | --- | --- |
| Presença acumulada até a semana 4 (%) | Atributo | Fim da semana 4 | Diário eletrônico | Necessário. Faltas abonadas e lançamentos atrasados podem distorcer o valor. |
| Média parcial das avaliações até a semana 4 | Atributo | Fim da semana 4 | Sistema acadêmico | Necessário. Há ausências quando a avaliação ainda não foi lançada (5% no laboratório), o que exige imputação aprendida no treino. |
| Atividades entregues até a semana 4 | Atributo | Fim da semana 4 | Ambiente virtual de aprendizagem | Útil. Depende de a disciplina usar o ambiente, e disciplinas sem atividades on-line gerariam zeros falsos. |
| Situação na rematrícula | Alvo | Início do semestre seguinte | Secretaria | Indispensável para treinar e avaliar. Precisa seguir a definição acima, aplicada igualmente a todos os cursos. |
| Código pseudônimo do estudante | Ligação entre as bases, fora do modelo | Sempre | Secretaria, com chave guardada separadamente | Necessário para juntar os registros. Risco de reidentificação: a chave fica só com a secretaria. |
| Turno, curso e forma de ingresso | Auditoria de erros por grupo, não usados como atributo | Matrícula | Secretaria | Útil para verificar se o modelo falha mais com algum grupo. Uso restrito à auditoria, com finalidade registrada. |
| Pedido espontâneo de ajuda (o estudante procurou o apoio) | Fora do modelo | A qualquer momento | Equipe de apoio | Não deve virar atributo: quem pede ajuda seria tratado como "risco" por ter pedido. |

Diferencie dados usados na simulação e dados que seriam necessários para uma investigação real: **No laboratório há 600 estudantes fictícios, três atributos gerados por uma fórmula, ruído sorteado e 5% de notas apagadas de propósito. Não existe curso, turno nem tempo. Uma investigação real exigiria vários semestres, para treinar no passado e testar no futuro, a definição oficial de evasão, informações de grupo para auditoria, a escuta dos estudantes sobre o que os dados não mostram (trabalho, deslocamento, cuidado com familiares), aprovação ética e base legal pela LGPD.**

### 4. Abordagem e algoritmo

- Classificação, regressão ou outra formulação, com justificativa: **Classificação supervisionada binária: o desfecho histórico é uma categoria (seguiu ou não seguiu), e a decisão também é categórica (contatar agora ou depois).**
- Algoritmo introdutório escolhido: **Árvore de decisão com imputação pela mediana em `Pipeline`, `max_depth=5` e `min_samples_leaf=40`. As folhas grandes fazem cada regra valer para um grupo de pelo menos 40 estudantes, o que reduz o sobreajuste e permite explicar as regras à equipe.**
- Referência simples: **`DummyClassifier(strategy='most_frequent')`, que prevê sempre "permaneceu".**

### 5. Avaliação

- Preparação, divisão e validação: **Holdout estratificado 75/25 (450/150, semente 42). A mediana é aprendida só no treino. Grade de profundidade × folha por validação cruzada estratificada em 5 partes, com regra de escolha definida antes. Teste usado uma vez. Com dados reais: treinar com semestres anteriores e testar no seguinte.**
- Métricas e razão da escolha: **Sensibilidade da classe 1 como métrica principal, porque o erro mais caro é não procurar quem vai sair. Precisão para dimensionar o trabalho da equipe (quantos contatos são necessários para alcançar um estudante em risco). Acurácia e comparação com a referência como verificação geral.**
- Resultados efetivamente calculados e link da evidência: **Validação de 0,729 ± 0,030. Teste com acurácia de 0,780 contra 0,593 da referência. TN = 70, FP = 19, FN = 14, TP = 47. Sensibilidade de 0,770 e precisão de 0,712. A validação repetida 10 vezes deu 0,714 para esta configuração e 0,722 para a do roteiro, ou seja, desempenho equivalente. Evidências: [notebook](notebooks/laboratorio-equipe.ipynb), [registro do laboratório](03-aula2-laboratorio.md) e [matriz](assets/matriz-confusao.png).**
- Erros relevantes e consequências: **14 dos 61 estudantes que evadiram (23%) não seriam sinalizados e dependeriam de outros caminhos até o apoio. Dos 66 sinalizados, 19 não precisavam, e a equipe gastaria cerca de 1 contato a cada 3,5 com quem ia permanecer. Esse custo é aceitável se o convite for respeitoso e opcional.**

### 6. Limites e proteção

- Por que os resultados não demonstram causalidade? **A árvore só aprendeu quais combinações de atributos aparecem junto com a evasão nos dados. Ninguém alterou a nota ou a frequência de alguém para ver o que acontecia. Nota baixa pode ser consequência do mesmo problema que leva à saída (jornada de trabalho, por exemplo), e não a causa. Nesta prática, a associação foi escrita na fórmula da simulação.**
- Por que dados sintéticos não validam uso institucional? **Porque a simulação devolve as hipóteses de quem a escreveu: os pesos, o ruído e a ausência de grupos foram decididos no código. Um bom resultado mostra que o método funciona quando a relação existe, mas não mostra que ela existe nos estudantes da instituição.**
- Que grupos podem ser mal representados? Como investigar isso com evidências apropriadas? **Estudantes do noturno que trabalham, ingressantes do primeiro semestre (sem histórico), cursos pequenos, estudantes com deficiência (frequência e prazos podem seguir outras regras) e quem cursa disciplinas sem atividades no ambiente virtual. Com dados reais e autorizados, eu compararia sensibilidade e taxa de falsos positivos por grupo, com intervalos de incerteza, porque grupos pequenos geram números instáveis, e ouviria os próprios estudantes. O conjunto sintético não tem grupos e não permite afirmar nada sobre equidade.**
- Como minimizar dados, restringir acesso e definir retenção? **Usar somente os três sinais acadêmicos e o alvo. Pseudonimizar, com a chave guardada pela secretaria. O acesso à lista fica restrito à equipe de apoio, com registro de consultas, e professores e coordenação de curso não acessam a lista individual. A lista é apagada ao fim do semestre, e o histórico para reavaliar o modelo fica apenas em forma agregada. É a mesma lógica do meu TCC, o Pescadores Web: lá o acesso é separado por perfis (Administrador e Voluntário), e a página pública exibe apenas estatísticas agregadas.**
- Como garantir revisão humana e contestação? **Uma pessoa da equipe revisa cada nome antes do contato e pode retirar ou acrescentar estudantes. O estudante é informado de como os dados foram usados, pode recusar o convite sem qualquer consequência e pode pedir a correção de um dado errado. A coordenação revisa o modelo a cada semestre, comparando sinalizações e desfechos.**

### 7. Recomendações de apoio

- Ação voluntária proposta: **Mensagem curta, sem a palavra "risco", oferecendo três opções: monitoria da disciplina com nota mais baixa, conversa com a orientação acadêmica sobre rotina e horários, ou informação sobre auxílios. A escolha da opção segue o sinal que mais pesou para aquele estudante (pergunta 2).**
- Como acolher estudantes não sinalizados pelo modelo: **Divulgar os mesmos serviços para todas as turmas na semana 4, manter um formulário de autoindicação e permitir que professores encaminhem estudantes. O modelo é apenas uma das portas de entrada.**
- O que precisa ser verificado antes de aplicação real: **Desempenho com dados reais em divisão temporal; auditoria de erros por grupo; aprovação ética e jurídica; capacidade real da equipe (quantos contatos por semana), para escolher quantos sinalizar; piloto em poucas turmas, medindo se o apoio oferecido muda o desfecho.**

Previsões não são certezas. Priorize apoio e revisão humana, sem punições ou decisões automáticas prejudiciais.

## Apresentação de cinco minutos

| Tempo | Conteúdo | Responsável |
| --- | --- | --- |
| 1 minuto | Problema e dados | Felipe Barbosa Vieira |
| 2 minutos | Método e resultados | Felipe Barbosa Vieira |
| 1 minuto | Limitações | Felipe Barbosa Vieira |
| 1 minuto | Recomendações de apoio | Felipe Barbosa Vieira |

## Contribuições

| Integrante | Contribuição verificável |
| --- | --- |
| Felipe Barbosa Vieira | Trabalho individual. Todas as seções desta proposta e a execução do [notebook](notebooks/laboratorio-equipe.ipynb) que fornece os números da seção 5. |

[Voltar ao início](README.md).
