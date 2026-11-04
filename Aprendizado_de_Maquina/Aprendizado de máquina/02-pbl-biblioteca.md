<img src="assets/logo-udf.jpg" alt="UDF Centro Universitário" width="230">

**Profa. Kadidja Valéria | UDF**  
Ciência de Dados e Aprendizado de Máquina · Sistemas de Informação · 2026.2

# PBL — Biblioteca em Foco

## Identificação

- Estudante ou equipe: **Felipe Barbosa Vieira**
- Turma: **SI 7/8 Noturno — Sistemas de Informação**
- Data de realização: **16/10/2026**
- Integrantes e contribuições (se em equipe): **Não se aplica, o trabalho é individual. Fiz a delimitação, o canvas e a conclusão.**

## Situação-problema

Uma biblioteca universitária enfrenta filas em horários específicos e baixa utilização de alguns serviços. A coordenação deseja melhorar o atendimento e planejar recursos. Este é um cenário didático.

**Público-alvo:** estudantes usuários, equipe de atendimento e gestão.

**Questão norteadora:** como os dados podem orientar o planejamento da biblioteca e a oferta de serviços sem identificar ou discriminar seus usuários?

## Investigação em equipe

1. Delimitem o problema e a decisão a apoiar.
2. Registrem o que já sabem e o que precisam investigar.
3. Formulem duas perguntas de negócio.
4. Definam a unidade de análise, os atributos e o alvo, quando houver.
5. Justifiquem a abordagem e indiquem se uma análise descritiva já seria suficiente.
6. Proponham avaliação, cuidados com os dados e limitações.

## Canvas da equipe

| Campo | Registro |
| --- | --- |
| Problema e decisão | A coordenação não sabe **antecipar** os momentos em que o balcão fica sobrecarregado e conhece mal o motivo da baixa procura de alguns serviços. Decisão principal: a cada semana, marcar quais turnos precisam de um segundo atendente ou do autoatendimento de devolução ligado. Decisão secundária: em que ponto do percurso o estudante deixa de usar um serviço (não sabe que existe, não consegue reservar ou reserva e não comparece) e qual ajuste fazer. |
| Público-alvo | Estudantes (menos tempo em pé na fila), atendentes (menos picos imprevistos) e gestão (alocação justificada de pessoal). |
| O que sabemos | As filas aparecem em horários específicos. Alguns serviços têm pouca procura. Empréstimos e devoluções são registrados com data e hora. É provável que o sistema de reservas de salas e equipamentos guarde pedidos e comparecimentos. |
| O que precisamos investigar | O tempo de espera não é medido hoje: precisamos de um registro mínimo, como uma senha numerada com hora de emissão e de chamada. É preciso verificar se os picos acompanham o horário de troca de aulas e o calendário de provas e de entrega de TCC, e se há reservas feitas e não usadas, o que indicaria um problema de acesso e não de interesse. |
| Pergunta de negócio 1 | Na próxima semana, quais turnos (dia × faixa de uma hora) devem ter espera acima de 10 minutos no balcão? |
| Pergunta de negócio 2 | Para cada serviço pouco usado, em qual etapa (conhecer, reservar, comparecer) a maior parte dos estudantes fica pelo caminho? |
| Unidade de análise e período | P1: um turno de uma hora em um dia letivo, ao longo de dois semestres. P2: o serviço em um semestre, com contagens agregadas de cada etapa. |
| Atributos, unidades e origem pretendida | P1: dia da semana, hora, semana do semestre e tipo de semana (aulas normais, provas, recesso) do calendário acadêmico; empréstimos e devoluções do mesmo turno na semana anterior (contagem, sistema da biblioteca); entradas na catraca (contagem); atendentes escalados (pessoas). P2: visualizações da página do serviço (contagem), reservas feitas, reservas comparecidas e respostas de uma pesquisa anônima (sim/não: "conhecia o serviço?"). |
| Alvo e momento em que será conhecido, ou ausência de alvo | P1: alvo = turno com espera mediana acima de 10 minutos (sim/não). É conhecido ao fim do turno, depois que o registro de senhas existir, e a previsão é feita na sexta-feira anterior. P2: sem alvo; é um funil descritivo. |
| Abordagem e justificativa | P1 como **classificação** dos turnos críticos, porque a decisão é binária (reforçar ou não). Antes, porém, a referência descritiva: marcar como crítico todo turno que foi crítico na mesma semana do calendário no semestre anterior. Se essa regra acertar quase tudo, o modelo não é necessário. P2 dispensa ML: as contagens de cada etapa já respondem a pergunta. |
| Alternativa sem ML | Tabela dia × hora com a proporção de turnos críticos, separada por tipo de semana. Escala ajustada à mão a partir dela. Funil de cada serviço no painel da gestão. |
| Como avaliar a proposta | P1: treinar com o primeiro semestre e testar no segundo (divisão temporal), olhando **sensibilidade** (turnos críticos que o modelo encontrou) e falsos alarmes (atendente extra sem necessidade), sempre comparados à regra do semestre anterior. Para o resultado real, comparar a espera mediana antes e depois da nova escala. P2: variação das reservas comparecidas depois do ajuste de cada etapa. |
| Privacidade e limitações | Senhas e catraca sem vínculo com a matrícula. Só contagens por turno entram na análise, e a pesquisa é anônima. Os registros brutos são apagados depois da agregação mensal. Limitações: o registro de espera ainda não existe, então os primeiros meses servem só para coletar dados. Quem desiste antes de pegar a senha não aparece. Mudanças de grade horária alteram os picos de um semestre para o outro. Cursos com poucos alunos na biblioteca ficam sub-representados na pesquisa. |

## Registro de colaboração

| Integrante | Papel | Contribuição |
| --- | --- | --- |
| Felipe Barbosa Vieira | Todos os papéis (trabalho individual) | Delimitei as duas decisões, propus o registro de senhas como fonte do alvo, defini unidade, atributos e alvo, montei a avaliação temporal e os cuidados com privacidade, e escrevi a conclusão. |

## Conclusão da equipe

**Proposta:** primeiro **medir** a espera, que hoje não é registrada, com senhas numeradas e horário de chamada. Com um semestre de registros, montar a tabela de turnos críticos e testar se uma classificação supera a regra "repetir o semestre anterior" na sensibilidade, sem gerar muitos falsos alarmes. Para os serviços pouco usados, o funil conhecer → reservar → comparecer, sem ML. A mesma lógica aparece no meu TCC: as perguntas de negócio do Pescadores Web (estoque abaixo do mínimo, doações por período, participação de voluntários) são respondidas primeiro com indicadores descritivos no dashboard, e não com previsões.

**Dúvida ainda aberta:** qual limite de espera (10 minutos?) os estudantes consideram aceitável? Esse corte define o alvo e, portanto, muda o que é "turno crítico".

**Feedback recebido e melhoria realizada:** A registrar após a apresentação.

## Entrega

Canvas preenchido e síntese para apresentação de dois minutos. Avaliar coerência da pergunta, dados, abordagem, responsabilidade e colaboração. [Voltar ao início](README.md).
