"""Portuguese grammar topics — C1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="subjuntivo-concessivo",
        title="Conjuntivo em orações concessivas",
        level="C1",
        category="Conjuntivo",
        summary="Uso avançado do conjuntivo em orações concessivas.",
        explanation="Por mais que, por muito que, ainda que, mesmo que, nem que + conjuntivo.",
        rules=[
            "Por mais/muito que + conjuntivo.",
            "Ainda que/mesmo que + conjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Por mais que tentes, nem sempre vais conseguir.",
                translation=None,
            ),
            GrammarExample(
                text="Mesmo que me pagassem, não faria esse trabalho.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Por mais que tentas.",
                correct="Por mais que tentes.",
                note="Por mais que exige conjuntivo.",
            ),
        ],
        related=[
            "conectores-avancados",
            "imperfeito-conjuntivo",
            "contra-argumentacao",
        ],
    ),
    GrammarTopic(
        slug="subjuntivo-final",
        title="Conjuntivo em orações finais",
        level="C1",
        category="Conjuntivo",
        summary="Conjuntivo após conectores finais.",
        explanation="Para que/a fim de que/de modo a que + conjuntivo (sujeito diferente). Mesmo sujeito: para + infinitivo.",
        rules=[
            "Para que + conj. (sujeito diferente).",
            "Mesmo sujeito: para + inf.",
        ],
        examples=[
            GrammarExample(
                text="Enviei o email para que todos fiquem informados.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Estudo para eu passarão.",
                correct="Estudo para passar.",
                note="Com o mesmo sujeito, para + infinitivo é geralmente mais económico; para que eu passe também pode ser gramatical.",
            ),
        ],
        related=["presente-conjuntivo", "conectores-avancados", "infinitivo-pessoal"],
    ),
    GrammarTopic(
        slug="subjuntivo-relativo",
        title="Conjuntivo em orações relativas",
        level="C1",
        category="Conjuntivo",
        summary="Conjuntivo com antecedente indeterminado.",
        explanation="Conjuntivo para antecedente desconhecido. Indicativo para específico. Há quem / Não há quem + conjuntivo.",
        rules=[
            "Conjuntivo: hipotético.",
            "Indicativo: específico.",
        ],
        examples=[
            GrammarExample(
                text="Procuro alguém que fale chinês.",
                translation=None,
                note="indeterminado",
            ),
            GrammarExample(
                text="Conheço alguém que fala chinês.",
                translation=None,
                note="específico",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Procuro alguém que falem chinês.",
                correct="Procuro alguém que fale chinês.",
                note="Alguém exige singular. O conjuntivo apresenta um perfil desejado; o indicativo pode referir alguém cuja existência é assumida.",
            ),
        ],
        related=["presente-conjuntivo", "que-relativo"],
    ),
    GrammarTopic(
        slug="passiva-reflexa",
        title="Voz passiva reflexa",
        level="C1",
        category="Voz passiva",
        summary="Usos avançados da voz passiva com o pronome se.",
        explanation="Aprecia-se, comenta-se, realizar-se-á (mesóclise), observa-se. Uso académico e jornalístico.",
        rules=[
            "Aprecia-se/comenta-se = passiva reflexa.",
            "Realizar-se-á = será realizado.",
        ],
        examples=[
            GrammarExample(
                text="Comenta-se que o acordo será assinado amanhã.",
                translation=None,
            ),
            GrammarExample(
                text="Observa-se uma melhoria significativa.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["voz-passiva", "se-impessoal", "se-passivo"],
    ),
    GrammarTopic(
        slug="nominalizacao",
        title="Nominalização",
        level="C1",
        category="Avançado",
        summary="Transformar verbos e adjetivos em substantivos.",
        explanation="Implementar -> implementação. Melhorar -> melhoria. Construir -> construção. Evitar cadeias.",
        rules=[
            "Verbo -> substantivo.",
            "Evitar cadeias de nominalizações.",
        ],
        examples=[
            GrammarExample(
                text="A implementação do programa foi bem-sucedida.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A realização da implementação da verificação.",
                correct="A verificação dos dados.",
                note="Evitar cadeias.",
            ),
        ],
        related=["impessoalidade", "registo-formal", "coesao-textual"],
    ),
    GrammarTopic(
        slug="impessoalidade",
        title="Impessoalidade",
        level="C1",
        category="Avançado",
        summary="Técnicas de impessoalidade no discurso formal.",
        explanation="Voz passiva, se impessoal, nominalização, expressões impessoais (Convém salientar que...).",
        rules=[
            "Voz passiva, se impessoal.",
            "Nominalizações.",
            "Convém/importa + infinitivo.",
        ],
        examples=[
            GrammarExample(
                text="Foi observado um aumento significativo.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eu observei um aumento. (académico)",
                correct="Foi observado um aumento.",
                note="Evitar 1a pessoa.",
            ),
        ],
        related=["nominalizacao", "voz-passiva", "registo-formal"],
    ),
    GrammarTopic(
        slug="campos-semanticos",
        title="Campos semânticos",
        level="C1",
        category="Avançado",
        summary="Agrupamentos lexicais por domínios.",
        explanation="Exemplo: justiça -> tribunal, juiz, advogado, réu, sentença, julgar, condenar, absolver.",
        rules=[
            "Agrupar vocabulário por áreas.",
        ],
        examples=[
            GrammarExample(
                text="O juiz condenou o réu com base nas provas. (campo: justiça)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Usar léxico de campo errado.",
                correct="Verificar o campo semântico adequado.",
                note="",
            ),
        ],
        related=["derivacao", "precisao-lexica"],
    ),
    GrammarTopic(
        slug="derivacao",
        title="Derivação",
        level="C1",
        category="Avançado",
        summary="Mecanismos de formação de palavras.",
        explanation="Prefixos: re-, in-/im-, des-. Sufixos: -ção, -mento, -dade, -vel, -izar.",
        rules=[
            "Prefixos e sufixos formam palavras.",
        ],
        examples=[
            GrammarExample(text="feliz -> infeliz -> felicidade", translation=None),
            GrammarExample(
                text="construir -> construção -> reconstrutivo",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A desfelicidade dele era evidente.",
                correct="A infelicidade dele era evidente.",
                note="Infelicidade é a forma lexical estabelecida; nem todos os prefixos se combinam livremente com todas as bases.",
            ),
        ],
        related=["campos-semanticos", "precisao-lexica"],
    ),
    GrammarTopic(
        slug="precisao-lexica",
        title="Precisão léxica",
        level="C1",
        category="Avançado",
        summary="Escolher a palavra exata.",
        explanation="Dizer vs falar, Ver vs olhar, Ouvir vs escutar, Saber vs conhecer.",
        rules=[
            "Dizer (informação) vs falar (comunicação).",
            "Saber (facto) vs conhecer (familiaridade).",
        ],
        examples=[
            GrammarExample(
                text="Sei a resposta. / Conheço bem essa pessoa.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Conheço nadar.",
                correct="Sei nadar.",
                note="Saber + infinitivo exprime uma capacidade. Conheço a resposta e Sei a resposta são ambas construções válidas.",
            ),
        ],
        related=["derivacao", "campos-semanticos", "falsos-amigos"],
    ),
    GrammarTopic(
        slug="ironia",
        title="Ironia",
        level="C1",
        category="Avançado",
        summary="A ironia como recurso retórico.",
        explanation="A ironia cria uma distância entre o sentido literal e a intenção, frequentemente dizendo o contrário do que se pretende comunicar. A interpretação depende do contexto e da entoação; não é uma característica exclusiva de uma cultura.",
        rules=[
            "Ironia = dizer o contrário.",
            "Interpretar segundo o contexto, a relação entre interlocutores e a entoação.",
        ],
        examples=[
            GrammarExample(
                text="Pois sim, acredito muito nisso.",
                translation=None,
                note="irónico",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Interpretar ironia literalmente.",
                correct="Prestar atenção à entoação e ao contexto.",
                note="",
            ),
        ],
        related=["humor-portugues", "duplo-sentido", "recursos-retoricos"],
    ),
    GrammarTopic(
        slug="humor-portugues",
        title="Humor à portuguesa",
        level="C1",
        category="Avançado",
        summary="Características do humor português.",
        explanation="Autoironia, sarcasmo afável, resignação cómica, subentendido, desenrascanço.",
        rules=[
            "Autoironia, sarcasmo.",
            "Resignação cómica.",
            "Desenrascanço.",
        ],
        examples=[
            GrammarExample(text="Como estás? -- Vai-se andando.", translation=None),
            GrammarExample(text="Isto só acontece em Portugal.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Presumir que um comentário sarcástico é sempre amigável.",
                correct="Avaliar o contexto e a reação do interlocutor.",
                note="O sarcasmo pode ser afetuoso ou ofensivo; a nacionalidade não determina a intenção.",
            ),
        ],
        related=["ironia", "duplo-sentido", "expressoes-idiomaticas"],
    ),
    GrammarTopic(
        slug="duplo-sentido",
        title="Duplo sentido",
        level="C1",
        category="Avançado",
        summary="Jogos de palavras e ambiguidade.",
        explanation="Ambiguidade lexical e sintática. Usado em humor, publicidade e literatura.",
        rules=[
            "Ambiguidade lexical e sintática.",
        ],
        examples=[
            GrammarExample(
                text="Vi o homem com os binóculos.",
                translation=None,
                note="Pode indicar o instrumento usado para ver ou identificar o homem que tinha os binóculos.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Duplo sentido não intencional em textos formais.",
                correct="Rever para evitar ambiguidades.",
                note="",
            ),
        ],
        related=["ironia", "humor-portugues", "recursos-retoricos"],
    ),
    GrammarTopic(
        slug="recursos-retoricos",
        title="Recursos retóricos",
        level="C1",
        category="Avançado",
        summary="Catálogo de figuras de retórica.",
        explanation="Pergunta retórica, anáfora, gradação, paradoxo, antítese.",
        rules=[
            "Pergunta retórica, anáfora.",
            "Paradoxo, antítese.",
        ],
        examples=[
            GrammarExample(
                text="Quem nunca errou? (pergunta retórica)",
                translation=None,
            ),
            GrammarExample(
                text="O silêncio ensurdecedor da noite. (paradoxo)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(wrong="Uso excessivo.", correct="Dosear as figuras.", note=""),
        ],
        related=["persuasao", "figuras-literarias"],
    ),
    GrammarTopic(
        slug="persuasao",
        title="Persuasão",
        level="C1",
        category="Avançado",
        summary="Técnicas de persuasão no discurso.",
        explanation="Ethos (credibilidade), Pathos (emoção), Logos (lógica). Adaptar ao público.",
        rules=[
            "Ethos, Pathos, Logos.",
        ],
        examples=[
            GrammarExample(
                text="Enquanto profissional com 20 anos de experiência, recomendo... (ethos)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Apelos emocionais sem fundamentação.",
                correct="Combinar pathos com logos.",
                note="",
            ),
        ],
        related=["recursos-retoricos", "estrutura-argumentativa"],
    ),
    GrammarTopic(
        slug="figuras-literarias",
        title="Figuras literárias",
        level="C1",
        category="Avançado",
        summary="Metáfora, metonímia, sinédoque e outras figuras.",
        explanation="Metáfora, comparação, metonímia, sinédoque, personificação, hipérbole.",
        rules=[
            "Metáfora, metonímia.",
            "Personificação, hipérbole.",
        ],
        examples=[
            GrammarExample(text="O tempo é dinheiro. (metáfora)", translation=None),
            GrammarExample(text="Portugal venceu o jogo. (metonímia)", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Confundir metáfora com comparação.",
                correct="Metáfora = identificação. Comparação = como.",
                note="",
            ),
        ],
        related=["descricao-literaria", "recursos-retoricos", "estilo-literario"],
    ),
    GrammarTopic(
        slug="portugues-brasileiro",
        title="Português brasileiro vs europeu",
        level="C1",
        category="Avançado",
        summary="Principais diferenças entre PB e PE.",
        explanation="PB: gerúndio, próclise. PE: a + infinitivo, ênclise. Léxico diferente.",
        rules=[
            "PB: gerúndio. PE: a + inf.",
            "PB: próclise. PE: ênclise.",
        ],
        examples=[
            GrammarExample(text="PE: pequeno-almoço. / PB: café da manhã.", translation=None),
            GrammarExample(
                text="PE: Dá-me um café. / PB: Me dá um café.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Misturar PE e PB.",
                correct="Escolher uma variante e ser consistente.",
                note="",
            ),
        ],
        related=["portugues-europeu", "diferencas-regionais"],
    ),
    GrammarTopic(
        slug="portugues-europeu",
        title="Particularidades do português europeu",
        level="C1",
        category="Avançado",
        summary="Características distintivas do PE.",
        explanation="Estar a + inf., ênclise/mesóclise, artigo + possessivo, artigo + nome próprio, tu + 2a pessoa, infinitivo pessoal.",
        rules=[
            "Estar a + inf.",
            "Ênclise e mesóclise.",
            "Artigo + possessivo + nome próprio.",
        ],
        examples=[
            GrammarExample(
                text="O Pedro está a estudar para o exame.",
                translation=None,
            ),
            GrammarExample(
                text="Dar-te-ei o livro amanhã.",
                translation=None,
                note="mesóclise",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Me apetece sair.",
                correct="Apetece-me sair.",
                note="EP não começa frase com pronome átono.",
            ),
        ],
        related=["portugues-brasileiro", "diferencas-regionais", "estar-a-infinitivo"],
    ),
    GrammarTopic(
        slug="diferencas-regionais",
        title="Diferenças regionais em Portugal",
        level="C1",
        category="Avançado",
        summary="Variação dialetal dentro de Portugal.",
        explanation="Norte: vós em alguns usos regionais, fino, cimbalino. Sul: gerúndio. Ilhas: léxico próprio. Padrão: Coimbra-Lisboa.",
        rules=[
            "Norte: léxico próprio.",
            "Sul: gerúndio.",
            "Padrão: Coimbra-Lisboa.",
        ],
        examples=[
            GrammarExample(
                text="Quereis um fino? (Porto)",
                translation=None,
                note="norte",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Assumir que todo o país fala igual.",
                correct="Respeitar a variação regional.",
                note="",
            ),
        ],
        related=["portugues-europeu", "portugues-brasileiro"],
    ),
    GrammarTopic(
        slug="sintese-textual",
        title="Síntese textual",
        level="C1",
        category="Avançado",
        summary="Técnicas para resumir textos.",
        explanation="Identifica a ideia principal, preserva as relações entre argumentos e elimina detalhes dispensáveis sem acrescentar opiniões. A extensão da síntese depende do objetivo e das instruções, não de uma percentagem fixa.",
        rules=[
            "Ideia principal.",
            "Eliminar redundâncias.",
            "Respeitar o limite e o objetivo pedidos, preservando o sentido do original.",
        ],
        examples=[
            GrammarExample(
                text="Em suma, o autor defende que a globalização trouxe mais benefícios.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(wrong="Síntese demasiado longa.", correct="Síntese concisa.", note=""),
        ],
        related=["coesao-textual", "critica-construtiva", "reformulacao"],
    ),
    GrammarTopic(
        slug="critica-construtiva",
        title="Crítica construtiva",
        level="C1",
        category="Avançado",
        summary="Formular críticas de forma elegante.",
        explanation="Começar pelo positivo, usar condicional, perguntar em vez de afirmar, focar na solução.",
        rules=[
            "Positivo primeiro.",
            "Condicional: seria, poderia.",
        ],
        examples=[
            GrammarExample(
                text="O relatório está muito completo. Talvez fosse útil incluir mais dados.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Isto está errado.",
                correct="Esta secção poderia beneficiar de uma revisão.",
                note="",
            ),
        ],
        related=["reformulacao", "matizadores", "registo-formal"],
    ),
    GrammarTopic(
        slug="reformulacao",
        title="Reformulação",
        level="C1",
        category="Avançado",
        summary="Técnicas para reformular ideias.",
        explanation="Isto é, ou seja, dito de outra forma. Parafrasear, mudar registo, alterar voz.",
        rules=[
            "Isto é / ou seja.",
            "Adaptar registo.",
        ],
        examples=[
            GrammarExample(
                text="O evento foi cancelado. Ou seja, não haverá concerto.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ou seja, tipo, quer dizer...",
                correct="Ou seja,...",
                note="Um reformulador é suficiente.",
            ),
        ],
        related=["sintese-textual", "critica-construtiva", "registo-formal"],
    ),
]
