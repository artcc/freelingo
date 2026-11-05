"""Brazilian Portuguese (phrasebook_c1) learning content."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="presentations_c1",
        level="C1",
        situation="Apresentações e oratória",
        icon="🎤",
        phrases=[
            PhrasebookEntry(
                text="Senhoras e senhores, bom dia.",
                context="Abertura formal de uma apresentação",
                register="formal",
            ),
            PhrasebookEntry(
                text="Hoje gostaria de falar com vocês sobre um tema muito importante para mim.",
                context="Introduzir o tema com envolvimento emotivo",
                register="formal",
            ),
            PhrasebookEntry(
                text="A minha apresentação está dividida em três partes.",
                context="Ilustrar a estrutura",
                register="formal",
            ),
            PhrasebookEntry(
                text="Como podem ver neste slide...",
                context="Comentar um slide",
                register="formal",
            ),
            PhrasebookEntry(
                text="Para aprofundar este aspecto...",
                context="Aprofundar um ponto",
                register="formal",
            ),
            PhrasebookEntry(
                text="Gostaria de chamar a atenção de vocês para este gráfico.",
                context="Atrair a atenção para um dado visual",
                register="formal",
            ),
            PhrasebookEntry(
                text="Permitam-me abrir um breve parêntese.",
                context="Fazer uma digressão",
                register="formal",
            ),
            PhrasebookEntry(
                text="Em conclusão, considero fundamental sublinhar que...",
                context="Concluir com ênfase",
                register="formal",
            ),
            PhrasebookEntry(
                text="Agradeço a atenção de vocês.",
                context="Agradecer no final",
                register="formal",
            ),
            PhrasebookEntry(
                text="Se houver perguntas, estou à disposição de vocês.",
                context="Abrir às perguntas",
                register="formal",
            ),
            PhrasebookEntry(
                text="Para resumir o que foi dito até agora...",
                context="Resumir a meio da apresentação",
                register="formal",
            ),
            PhrasebookEntry(
                text="Gostaria de concluir com uma citação de...",
                context="Fechar com uma citação",
                register="formal",
            ),
            PhrasebookEntry(
                text="Passo agora à segunda parte.",
                context="Transição entre seções",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="complex_arguments_c1",
        level="C1",
        situation="Argumentações complexas",
        icon="🧠",
        phrases=[
            PhrasebookEntry(
                text="Reconhecendo embora a validade das suas observações, discordaria.",
                context="Concessão seguida de objeção",
                register="formal",
            ),
            PhrasebookEntry(
                text="É inegável que os dados mostram uma tendência preocupante.",
                context="Afirmar um fato indiscutível",
                register="formal",
            ),
            PhrasebookEntry(
                text="Contudo, há que considerar também o contexto em que estes eventos ocorreram.",
                context="Introduzir um contra-argumento",
                register="formal",
            ),
            PhrasebookEntry(
                text="A meu ver, o ponto crucial da questão reside no fato de...",
                context="Identificar o ponto central",
                register="formal",
            ),
            PhrasebookEntry(
                text="Não se pode prescindir das implicações éticas desta escolha.",
                context="Levantar questões éticas",
                register="formal",
            ),
            PhrasebookEntry(
                text="Embora a proposta seja aliciante, comporta riscos não negligenciáveis.",
                context="Usar concessiva com subjuntivo",
                register="formal",
            ),
            PhrasebookEntry(
                text="Poder-se-ia objetar que os custos são excessivos.",
                context="Apresentar uma possível objeção",
                register="formal",
            ),
            PhrasebookEntry(
                text="Seria redutor limitarmo-nos a uma só interpretação do fenômeno.",
                context="Criticar uma visão limitada",
                register="formal",
            ),
            PhrasebookEntry(
                text="A questão merece ser examinada de uma perspectiva mais ampla.",
                context="Pedir uma visão mais ampla",
                register="formal",
            ),
            PhrasebookEntry(
                text="É uma tese fascinante, mas a meu ver não resiste a uma análise aprofundada.",
                context="Refutar com elegância",
                register="formal",
            ),
            PhrasebookEntry(
                text="Se é verdade que X, daí não decorre necessariamente Y.",
                context="Desmontar uma falácia lógica",
                register="formal",
            ),
            PhrasebookEntry(
                text="Considero que se trata de uma simplificação excessiva.",
                context="Criticar uma simplificação",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="professional_networking_c1",
        level="C1",
        situation="Networking profissional",
        icon="🤝",
        phrases=[
            PhrasebookEntry(
                text="Muito prazer em conhecê-lo. Tenho acompanhado com interesse o seu trabalho.",
                context="Apresentar-se com um elogio profissional",
                register="formal",
            ),
            PhrasebookEntry(
                text="Teria muito gosto em aprofundar uma possível colaboração.",
                context="Propor uma colaboração",
                register="formal",
            ),
            PhrasebookEntry(
                text="Trabalho no setor há mais de dez anos.",
                context="Descrever a experiência profissional",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Ocupo-me sobretudo de desenvolvimento internacional.",
                context="Descrever o próprio cargo",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Posso deixar-lhe o meu cartão de visita?",
                context="Oferecer o cartão de visita",
                register="formal",
            ),
            PhrasebookEntry(
                text="Seria um prazer manter o contato.",
                context="Exprimir desejo de manter contato",
                register="formal",
            ),
            PhrasebookEntry(
                text="A nossa empresa está interessada em explorar novas parcerias.",
                context="Aludir a oportunidades de negócio",
                register="formal",
            ),
            PhrasebookEntry(
                text="Apreciei muito a sua intervenção no congresso.",
                context="Fazer um elogio específico",
                register="formal",
            ),
            PhrasebookEntry(
                text="Poderíamos marcar uma reunião para discutir mais a fundo.",
                context="Propor um encontro futuro",
                register="formal",
            ),
            PhrasebookEntry(
                text="Se me permite uma sugestão, entre em contato com nosso escritório.",
                context="Dar uma sugestão profissional",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="conflict_resolution_c1",
        level="C1",
        situation="Resolução de conflitos",
        icon="🕊️",
        phrases=[
            PhrasebookEntry(
                text="Compreendo o seu ponto de vista, mas gostaria de esclarecer melhor a nossa posição.",
                context="Mostrar compreensão antes de discordar",
                register="formal",
            ),
            PhrasebookEntry(
                text="É possível que tenha havido um mal-entendido.",
                context="Colocar a hipótese de um equívoco",
                register="neutral",
            ),
            PhrasebookEntry(
                text="O objetivo comum deveria ser encontrar uma solução que satisfaça ambos.",
                context="Recordar o objetivo comum",
                register="formal",
            ),
            PhrasebookEntry(
                text="Estou disposto/a a reconsiderar a minha posição se...",
                context="Mostrar flexibilidade condicionada",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Considero que a transparência é fundamental para resolver a questão.",
                context="Invocar transparência",
                register="formal",
            ),
            PhrasebookEntry(
                text="Não era minha intenção faltar ao respeito.",
                context="Desculpar-se por uma ofensa involuntária",
                register="formal",
            ),
            PhrasebookEntry(
                text="Proponho darmos um passo atrás e recomeçarmos pelos pontos em que concordamos.",
                context="Propor um reset da discussão",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Estou certo/a de que conseguiremos chegar a um entendimento.",
                context="Exprimir otimismo construtivo",
                register="formal",
            ),
            PhrasebookEntry(
                text="Peço desculpa se as minhas palavras foram mal interpretadas.",
                context="Desculpar-se por um mal-entendido",
                register="formal",
            ),
            PhrasebookEntry(
                text="Envolvamos um mediador se acharmos que não conseguimos resolver sozinhos.",
                context="Propor mediação externa",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="academica_profissional_c1",
        level="C1",
        situation="Linguagem acadêmica e profissional",
        icon="📊",
        phrases=[
            PhrasebookEntry(
                text="O presente artigo propõe-se analisar as implicações do fenômeno em três vertentes distintas.",
                context="Introduzir o objetivo de um artigo acadêmico",
                register="formal",
                unit_ref="c1-unit-5",
            ),
            PhrasebookEntry(
                text="Cumpre desde já assinalar que a literatura existente sobre o tema é escassa.",
                context="Reconhecer limitações da bibliografia disponível",
                register="formal",
                unit_ref="c1-unit-5",
            ),
            PhrasebookEntry(
                text="Encaminho por e-mail a proposta em anexo para sua consideração.",
                context="Abertura de e-mail profissional com anexo",
                register="formal",
                unit_ref="c1-unit-5",
            ),
            PhrasebookEntry(
                text="Sem prejuízo de uma análise mais aprofundada, adianto desde já as principais conclusões.",
                context="Resumir conclusões preliminares em contexto profissional",
                register="formal",
                unit_ref="c1-unit-5",
            ),
            PhrasebookEntry(
                text="A presente comunicação destina-se a um público especializado na matéria.",
                context="Especificar o público-alvo de uma apresentação",
                register="formal",
                unit_ref="c1-unit-5",
            ),
            PhrasebookEntry(
                text="Resta-me agradecer a atenção dispensada e ficar ao dispor para quaisquer esclarecimentos adicionais.",
                context="Fecho de e-mail profissional",
                register="formal",
                unit_ref="c1-unit-5",
            ),
            PhrasebookEntry(
                text="A fundamentação teórica que subjaz a esta investigação assenta em três eixos principais.",
                context="Apresentar o quadro teórico de uma investigação",
                register="formal",
                unit_ref="c1-unit-5",
            ),
            PhrasebookEntry(
                text="Solicito a Vossa Excelência que se digne apreciar o requerimento junto.",
                context="Fórmula de requerimento formal à administração",
                register="formal",
                unit_ref="c1-unit-5",
            ),
        ],
    ),
]
