"""Brazilian Portuguese (phrasebook_b2) learning content."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="formal_emails_b2",
        level="B2",
        situation="Emails formais e correspondência",
        icon="📧",
        phrases=[
            PhrasebookEntry(
                text="Prezado Sr. Silva,",
                context="Abertura de e-mail formal (homem)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Prezada Professora Sousa,",
                context="Abertura de e-mail formal (mulher)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Em anexo envio o documento solicitado.",
                context="Enviar um anexo",
                register="formal",
            ),
            PhrasebookEntry(
                text="Agradeço a sua disponibilidade.",
                context="Agradecer a disponibilidade",
                register="formal",
            ),
            PhrasebookEntry(
                text="Aguardo sua resposta.",
                context="Pedir uma resposta educadamente",
                register="formal",
            ),
            PhrasebookEntry(
                text="Na sequência do seu e-mail de...",
                context="Referir uma comunicação anterior",
                register="formal",
            ),
            PhrasebookEntry(
                text="Escrevo para solicitar informações sobre...",
                context="Introduzir o objetivo do e-mail",
                register="formal",
            ),
            PhrasebookEntry(
                text="Cordialmente,",
                context="Fecho formal padrão",
                register="formal",
            ),
            PhrasebookEntry(
                text="Atenciosamente,",
                context="Fecho muito formal",
                register="formal",
            ),
            PhrasebookEntry(
                text="Peço desculpa pela demora na resposta.",
                context="Desculpar-se pela demora",
                register="formal",
            ),
            PhrasebookEntry(
                text="Permito-me solicitar uma resposta.",
                context="Solicitar uma resposta",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="negotiations_b2",
        level="B2",
        situation="Discussões e negociações",
        icon="🤝",
        phrases=[
            PhrasebookEntry(
                text="Proponho um compromisso.",
                context="Propor um compromisso",
                register="formal",
            ),
            PhrasebookEntry(
                text="Vamos tentar chegar a um acordo.",
                context="Convidar a negociar",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Qual é a proposta de vocês?",
                context="Pedir uma proposta",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Parece-me uma oferta razoável.",
                context="Avaliar positivamente",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Infelizmente não podemos aceitar estas condições.",
                context="Recusar educadamente",
                register="formal",
            ),
            PhrasebookEntry(
                text="Poderíamos rever os termos do contrato?",
                context="Pedir para renegociar",
                register="formal",
            ),
            PhrasebookEntry(
                text="Estamos dispostos a negociar o preço.",
                context="Mostrar flexibilidade no preço",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Gostaria de ter tempo para avaliar.",
                context="Ganhar tempo para decidir",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Podemos encontrar uma solução vantajosa para ambos.",
                context="Propor solução vantajosa para ambas as partes",
                register="formal",
            ),
            PhrasebookEntry(
                text="Vamos pôr por escrito.",
                context="Pedir confirmação escrita",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="academic_discussion_b2",
        level="B2",
        situation="Discussões acadêmicas",
        icon="🎓",
        phrases=[
            PhrasebookEntry(
                text="Segundo a minha investigação...",
                context="Introduzir os próprios resultados",
                register="formal",
            ),
            PhrasebookEntry(
                text="Este dado apoia a hipótese inicial.",
                context="Relacionar dados e hipótese",
                register="formal",
            ),
            PhrasebookEntry(
                text="Pelo contrário, os estudos de Silva sugerem que...",
                context="Contrapor investigações diferentes",
                register="formal",
            ),
            PhrasebookEntry(
                text="É importante sublinhar que...",
                context="Enfatizar um ponto",
                register="formal",
            ),
            PhrasebookEntry(
                text="A metodologia utilizada apresenta algumas limitações.",
                context="Reconhecer limites da investigação",
                register="formal",
            ),
            PhrasebookEntry(
                text="Esta conclusão é apoiada por evidências empíricas.",
                context="Reforçar uma afirmação",
                register="formal",
            ),
            PhrasebookEntry(
                text="Poderia esclarecer melhor este ponto?",
                context="Pedir esclarecimentos acadêmicos",
                register="formal",
            ),
            PhrasebookEntry(
                text="O tema foi amplamente debatido na literatura.",
                context="Referir literatura existente",
                register="formal",
            ),
            PhrasebookEntry(
                text="Considero que esta interpretação é discutível.",
                context="Exprimir desacordo acadêmico",
                register="formal",
            ),
            PhrasebookEntry(
                text="Em síntese, os resultados indicam que...",
                context="Resumir conclusões",
                register="formal",
            ),
            PhrasebookEntry(
                text="Quais são as implicações deste estudo?",
                context="Discutir as consequências de uma investigação",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="argumentacao_b2",
        level="B2",
        situation="Argumentação e debate",
        icon="🗣️",
        phrases=[
            PhrasebookEntry(
                text="Discordo frontalmente dessa perspectiva.",
                context="Exprimir desacordo de forma direta e firme",
                register="neutral",
                unit_ref="b2-unit-5",
            ),
            PhrasebookEntry(
                text="Permita-me que apresente um ponto de vista divergente.",
                context="Introduzir uma opinião contrária com educação",
                register="formal",
                unit_ref="b2-unit-5",
            ),
            PhrasebookEntry(
                text="A meu ver, a questão é mais complexa do que se possa imaginar.",
                context="Matizar um debate simplificado",
                register="neutral",
                unit_ref="b2-unit-5",
            ),
            PhrasebookEntry(
                text="Com a devida vênia, essa afirmação merece ser revista.",
                context="Contradizer respeitosamente",
                register="formal",
                unit_ref="b2-unit-5",
            ),
            PhrasebookEntry(
                text="Sustento que os fatos apontam noutra direção.",
                context="Afirmar que os dados contradizem o interlocutor",
                register="formal",
                unit_ref="b2-unit-5",
            ),
            PhrasebookEntry(
                text="Esta discussão seria mais produtiva se nos centrássemos nos dados objetivos.",
                context="Reconduzir o debate a fatos",
                register="neutral",
                unit_ref="b2-unit-5",
            ),
            PhrasebookEntry(
                text="Compreendo o argumento, mas não posso deixar de assinalar uma contradição.",
                context="Reconhecer o argumento alheio antes de o refutar",
                register="formal",
                unit_ref="b2-unit-5",
            ),
            PhrasebookEntry(
                text="Vejamos a questão por outro prisma.",
                context="Convidar a mudar de perspectiva",
                register="neutral",
                unit_ref="b2-unit-5",
            ),
            PhrasebookEntry(
                text="Respeitosamente, creio que está confundindo causa com consequência.",
                context="Apontar um erro lógico com cortesia",
                register="formal",
                unit_ref="b2-unit-5",
            ),
            PhrasebookEntry(
                text="É legítimo questionar se os fins justificam os meios.",
                context="Levantar uma questão ética no debate",
                register="formal",
                unit_ref="b2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        id="cultura_brasileira_b2",
        level="B2",
        situation="Cultura e diversidade brasileira",
        icon="🇵🇹",
        phrases=[
            PhrasebookEntry(
                text="O samba de roda do Recôncavo Baiano reúne música, dança e formas de convivência transmitidas entre gerações.",
                context="Apresentar uma tradição afro-brasileira sem reduzir toda a música do país a um gênero",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="A culinária brasileira resulta de encontros e conflitos históricos, com ingredientes e técnicas que variam muito entre regiões.",
                context="Descrever diversidade culinária",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="O pão de queijo é associado a Minas Gerais e também faz parte do cotidiano de muitas outras regiões.",
                context="Contextualizar um alimento sem o apresentar como universal",
                register="neutral",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="O artesanato brasileiro inclui cerâmica, cestaria, bordado e muitos outros saberes de comunidades específicas.",
                context="Valorizar a diversidade dos ofícios",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="As festas juninas combinam música, dança e comida, com tradições locais que não se limitam a uma única região.",
                context="Apresentar festas populares",
                register="neutral",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="O cultivo do café influenciou a economia e a formação de várias cidades brasileiras.",
                context="Relacionar produção agrícola e história urbana",
                register="neutral",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="A arquitetura de Brasília permite discutir tanto inovação modernista quanto os desafios da vida urbana.",
                context="Relacionar arquitetura e sociedade",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="O cordel combina narrativas em verso, circulação popular e debates sobre a vida cotidiana.",
                context="Explicar uma tradição literária",
                register="neutral",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="A literatura brasileira reúne vozes como Machado de Assis, Conceição Evaristo e Clarice Lispector.",
                context="Apresentar autores de diferentes trajetórias",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="Preservar o patrimônio cultural brasileiro exige ouvir as comunidades que mantêm esses saberes vivos.",
                context="Argumentar sobre preservação e participação",
                register="formal",
                unit_ref="b2-unit-3",
            ),
        ],
    ),
]
