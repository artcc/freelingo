"""Portuguese grammar topics — B2."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="imperfeito-conjuntivo",
        title="Imperfeito do conjuntivo",
        level="B2",
        category="Conjuntivo",
        summary="Formação e uso do imperfeito do conjuntivo.",
        explanation="Da 3a pl. do pretérito perfeito: falaram -> falasse, falasses... Usos: condições hipotéticas, desejos, após embora/como se.",
        rules=[
            "Da 3a pl. do pret. perfeito.",
            "Com se, embora, como se.",
        ],
        examples=[
            GrammarExample(
                text="Se eu tivesse mais tempo, viajava mais.",
                translation=None,
            ),
            GrammarExample(
                text="Embora chovesse, fomos à praia.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se eu tivesses tempo, ia.",
                correct="Se eu tivesse tempo, ia.",
                note="Eu exige tivesse, não tivesses. Se eu tinha tempo, ia é possível para um hábito passado.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "se-imperfeito-subjuntivo",
            "mais-que-perfeito-conjuntivo",
        ],
    ),
    GrammarTopic(
        slug="mais-que-perfeito-conjuntivo",
        title="Mais-que-perfeito do conjuntivo",
        level="B2",
        category="Conjuntivo",
        summary="Expressar condições passadas não realizadas.",
        explanation="Forma composta: tivesse + particípio passado. Se tivesse estudado, teria passado.",
        rules=[
            "Forma composta: tivesse + particípio.",
            "Condição NÃO realizada no passado.",
        ],
        examples=[
            GrammarExample(
                text="Se tivesse estudado, teria passado.",
                translation=None,
            ),
            GrammarExample(
                text="Se ela tivesse vindo, teria sido melhor.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se eu tivesse estudar, teria passado.",
                correct="Se eu tivesse estudado, teria passado.",
                note="O mais-que-perfeito do conjuntivo usa tivesse + particípio, não infinitivo.",
            ),
        ],
        related=["imperfeito-conjuntivo", "condicional-composto"],
    ),
    GrammarTopic(
        slug="concordancia-temporal",
        title="Concordância temporal",
        level="B2",
        category="Tempos verbais",
        summary="Regras de correspondência entre tempos verbais.",
        explanation="A escolha do tempo depende da relação temporal e da perspetiva, não apenas do tempo da oração principal.\n\nEspero que venhas apresenta uma ação simultânea ou posterior; Espero que tenhas chegado apresenta anterioridade. Queria que viesses usa o imperfeito; Duvidava que tivesse chegado usa o mais-que-perfeito para anterioridade passada. Uma principal presente admite referência passada: Duvido que fosse verdade.",
        rules=[
            "Distingue simultaneidade, anterioridade e posterioridade.",
            "A perspetiva temporal determina a escolha entre formas simples e compostas.",
        ],
        examples=[
            GrammarExample(
                text="Queria que viesses.",
                translation=None,
                note="pretérito -> imperfeito conj.",
            ),
            GrammarExample(
                text="Espero que chegues.",
                translation=None,
                note="presente -> presente conj.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Queria que tu viesse.",
                correct="Queria que viesses.",
                note="Com tu, a forma é viesses; o tempo depende da perspetiva temporal.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "imperfeito-conjuntivo",
            "futuro-do-conjuntivo",
        ],
    ),
    GrammarTopic(
        slug="perifrases-aspetuais",
        title="Perífrases aspetuais",
        level="B2",
        category="Verbos",
        summary="Construções verbais que expressam aspetos da ação.",
        explanation="Começar a + inf., estar a + inf., continuar a + inf., acabar de + inf., voltar a + inf.",
        rules=[
            "Começar a = início.",
            "Estar a = curso (EP).",
            "Acabar de = recém-concluída.",
            "Voltar a = repetição.",
        ],
        examples=[
            GrammarExample(
                text="Comecei a aprender português há um ano.",
                translation=None,
            ),
            GrammarExample(text="Acabei de comer.", translation=None),
        ],
        common_mistakes=[],
        related=["estar-a-infinitivo", "andar-a-estar-a", "costumava"],
    ),
    GrammarTopic(
        slug="perifrases-modais",
        title="Perífrases modais",
        level="B2",
        category="Verbos",
        summary="Construções verbais para obrigação, possibilidade e intenção.",
        explanation="Ter de/que + inf. (obrigação), precisar de + inf. (necessidade), poder + inf. (possibilidade), haver de + inf. (determinação, típico EP).",
        rules=[
            "Ter de/que = obrigação.",
            "Precisar de = necessidade.",
            "Haver de = determinação (EP).",
        ],
        examples=[
            GrammarExample(
                text="Tenho de terminar este relatório.",
                translation=None,
            ),
            GrammarExample(
                text="Hei de visitar os Açores um dia!",
                translation=None,
                note="determinação EP",
            ),
        ],
        common_mistakes=[],
        related=["perifrases-aspetuais", "querer-poder", "andar-a-estar-a"],
    ),
    GrammarTopic(
        slug="andar-a-estar-a",
        title="Andar a vs estar a",
        level="B2",
        category="Verbos",
        summary="Diferença entre andar a + infinitivo e estar a + infinitivo.",
        explanation="Estar a = agora. Andar a = repetido/persistente ao longo do tempo.",
        rules=[
            "Estar a = agora.",
            "Andar a = repetido/persistente.",
        ],
        examples=[
            GrammarExample(text="Estou a ler um livro.", translation=None, note="agora"),
            GrammarExample(text="Ando a ler um livro.", translation=None, note="dias"),
            GrammarExample(text="Ela anda a trabalhar demais.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Estou a comendo agora.",
                correct="Estou a comer agora.",
                note="Estar a exige infinitivo. Ando a comer pode apresentar um comportamento prolongado; não é errado por si só.",
            ),
        ],
        related=["estar-a-infinitivo", "perifrases-aspetuais"],
    ),
    GrammarTopic(
        slug="infinitivo-pessoal",
        title="Infinitivo pessoal",
        level="B2",
        category="Verbos",
        summary="O infinitivo pessoal.",
        explanation="O infinitivo pessoal pode explicitar o sujeito: falar, falares, falar, falarmos, falardes, falarem. É frequente quando o sujeito difere do da principal: Pedi silêncio para eles estudarem. Também ocorre com o mesmo sujeito para o salientar: Para chegarmos a tempo, temos de sair. Não se flexiona automaticamente qualquer infinitivo: Devemos estudar, não Devemos estudarmos.",
        rules=[
            "Infinitivo com terminações.",
            "Pode marcar um sujeito próprio, diferente ou não do da oração principal; depende da construção.",
        ],
        examples=[
            GrammarExample(
                text="É importante estudares mais.",
                translation=None,
            ),
            GrammarExample(
                text="Para chegarmos a tempo, temos de sair.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É importante tu estudar.",
                correct="É importante tu estudares.",
                note="Sujeito diferente -> infinitivo pessoal.",
            ),
        ],
        related=["presente-conjuntivo", "colocacao-pronominal"],
    ),
    GrammarTopic(
        slug="conectores-avancados",
        title="Conectores avançados",
        level="B2",
        category="Orações",
        summary="Conectores sofisticados para argumentação.",
        explanation="Desde que/a menos que/caso + conj. Para que/a fim de que + conj. Ainda que/mesmo que + conj.",
        rules=[
            "Desde que, a menos que + conj.",
            "Para que, a fim de que + conj.",
            "Ainda que, mesmo que + conj.",
        ],
        examples=[
            GrammarExample(
                text="Vou à festa desde que tu também vás.",
                translation=None,
            ),
            GrammarExample(
                text="Sairei mais cedo, a menos que haja reunião.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Desde que tu também vais.",
                correct="Desde que tu também vás.",
                note="Desde que condicional + conjuntivo.",
            ),
        ],
        related=["conectores-argumentativos", "coesao-textual"],
    ),
    GrammarTopic(
        slug="coesao-textual",
        title="Coesão textual",
        level="B2",
        category="Avançado",
        summary="Mecanismos para textos coesos.",
        explanation="Referência, substituição, elipse, conjunção, coesão lexical.",
        rules=[
            "Pronomes, sinónimos, conectores.",
            "Elipse quando possível.",
        ],
        examples=[
            GrammarExample(
                text="O João comprou um carro. Ele está contente com o veículo.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="O João comprou um carro. O João está contente.",
                correct="O João comprou um carro. Ele está contente.",
                note="Evitar repetição excessiva.",
            ),
        ],
        related=["conectores-avancados", "conectores-argumentativos"],
    ),
    GrammarTopic(
        slug="registo-formal",
        title="Registo formal",
        level="B2",
        category="Avançado",
        summary="Características do registo formal em EP.",
        explanation="Vocabulário cuidado, passiva, mesóclise, condicional de cortesia, tratamento o senhor/a senhora.",
        rules=[
            "Vocabulário cuidado.",
            "Passiva, mesóclise.",
            "Tratamento formal.",
        ],
        examples=[
            GrammarExample(
                text="Poder-me-ia informar sobre o horário?",
                translation=None,
                note="cortesia + mesóclise",
            ),
            GrammarExample(
                text="O senhor deseja mais alguma coisa?",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=[
            "expressoes-idiomaticas",
            "expressoes-coloquiais",
            "linguagem-jornalistica",
        ],
    ),
    GrammarTopic(
        slug="expressoes-idiomaticas",
        title="Expressões idiomáticas",
        level="B2",
        category="Avançado",
        summary="Expressões idiomáticas portuguesas.",
        explanation="Andar com a pulga atrás da orelha, dar o braço a torcer, estar com os azeites, custar os olhos da cara.",
        rules=[
            "Expressões fixas.",
            "Sentido literal diferente do figurado.",
        ],
        examples=[
            GrammarExample(text="Ando com a pulga atrás da orelha.", translation=None),
            GrammarExample(text="Ela está com os azeites hoje.", translation=None),
        ],
        common_mistakes=[],
        related=["expressoes-coloquiais", "proverbios", "registo-formal"],
    ),
    GrammarTopic(
        slug="expressoes-coloquiais",
        title="Expressões coloquiais",
        level="B2",
        category="Avançado",
        summary="Linguagem coloquial e gíria do português europeu.",
        explanation="Bué/altamente/fixe, tá-se bem, bora, ya, pá, giro/gira, desenrascar.",
        rules=[
            "Coloquialismos informais.",
            "Variação regional.",
        ],
        examples=[
            GrammarExample(text="Que filme tão fixe!", translation=None),
            GrammarExample(text="Bora tomar um café?", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Que filme fixe! (registo formal)",
                correct="Que filme interessante!",
                note="Evitar fixe em registo formal.",
            ),
        ],
        related=["expressoes-idiomaticas", "proverbios", "registo-formal"],
    ),
    GrammarTopic(
        slug="proverbios",
        title="Provérbios portugueses",
        level="B2",
        category="Avançado",
        summary="Provérbios tradicionais portugueses.",
        explanation="Água mole em pedra dura..., Quem vê caras não vê corações, Mais vale um pássaro na mão..., Depois da tempestade vem a bonança.",
        rules=[
            "Provérbios fixos.",
            "Sabedoria popular.",
        ],
        examples=[
            GrammarExample(
                text="Água mole em pedra dura, tanto bate até que fura.",
                translation=None,
            ),
            GrammarExample(
                text="Mais vale um pássaro na mão do que dois a voar.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["expressoes-idiomaticas", "expressoes-coloquiais"],
    ),
    GrammarTopic(
        slug="estrutura-argumentativa",
        title="Estrutura argumentativa",
        level="B2",
        category="Avançado",
        summary="Construir textos argumentativos.",
        explanation="Introdução (tese), desenvolvimento (argumentos), conclusão (retoma).",
        rules=[
            "Introdução, desenvolvimento, conclusão.",
            "Conectores específicos.",
        ],
        examples=[
            GrammarExample(
                text="Em primeiro lugar, a educação é fundamental.",
                translation=None,
            ),
            GrammarExample(
                text="Concluindo, os benefícios superam os riscos.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Os dados mostra que a medida funciona.",
                correct="Os dados mostram que a medida funciona.",
                note="O verbo concorda com dados. A primeira pessoa não é proibida num texto argumentativo; escolhe o registo conforme o género e as instruções.",
            ),
        ],
        related=["contra-argumentacao", "conectores-argumentativos", "coesao-textual"],
    ),
    GrammarTopic(
        slug="contra-argumentacao",
        title="Contra-Argumentação",
        level="B2",
        category="Avançado",
        summary="Técnicas para refutar argumentos.",
        explanation="Concessão + refutação, questionamento, evidência contrária.",
        rules=[
            "Concessão + refutação.",
            "Questionamento.",
            "Evidência.",
        ],
        examples=[
            GrammarExample(
                text="Embora alguns defendam o contrário, os estudos mostram que...",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Isso é mentira. (agressivo)",
                correct="Essa perspetiva parece ignorar alguns factos.",
                note="Contra-argumentação respeitosa.",
            ),
        ],
        related=["estrutura-argumentativa", "matizadores", "conectores-argumentativos"],
    ),
    GrammarTopic(
        slug="matizadores",
        title="Matizadores",
        level="B2",
        category="Avançado",
        summary="Palavras que suavizam ou relativizam afirmações.",
        explanation="Provavelmente, talvez, de certa forma, até certo ponto, um pouco, apenas.",
        rules=[
            "Suavizar afirmações.",
            "Evitar categóricas.",
        ],
        examples=[
            GrammarExample(
                text="Provavelmente, esta é a melhor abordagem.",
                translation=None,
            ),
            GrammarExample(text="De certa forma, concordo.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Possivelmente talvez seja melhor.",
                correct="Provavelmente é melhor.",
                note="Evitar acumular matizadores.",
            ),
        ],
        related=["estrutura-argumentativa", "contra-argumentacao"],
    ),
    GrammarTopic(
        slug="tempos-narrativos",
        title="Tempos narrativos",
        level="B2",
        category="Tempos verbais",
        summary="Articulação dos tempos verbais na narrativa.",
        explanation="Imperfeito (cenário), perfeito (ação principal), mais-que-perfeito (flashback).",
        rules=[
            "Imperfeito = cenário.",
            "Perfeito = ação.",
            "MQP = flashback.",
        ],
        examples=[
            GrammarExample(
                text="Era uma noite de tempestade. De repente, a porta abriu-se.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="De repente, começou chover.",
                correct="De repente, começou a chover.",
                note="Começar exige a antes do infinitivo. De repente não obriga, por si só, a usar um tempo verbal específico.",
            ),
        ],
        related=[
            "preterito-imperfeito",
            "perfeito-vs-imperfeito",
            "descricao-literaria",
        ],
    ),
    GrammarTopic(
        slug="descricao-literaria",
        title="Descrição literária",
        level="B2",
        category="Avançado",
        summary="Recursos para descrições vívidas.",
        explanation="Adjetivação rica, sensações, metáforas, personificação, imperfeito descritivo.",
        rules=[
            "Adjetivos sensoriais.",
            "Imperfeito descritivo.",
            "Metáforas, personificação.",
        ],
        examples=[
            GrammarExample(
                text="O sol punha-se no horizonte, tingindo o ceu de tons alaranjados.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A casa era bonita. (pobre)",
                correct="A casa exibia uma beleza melancólica.",
                note="Vocabulário rico.",
            ),
        ],
        related=["tempos-narrativos", "recursos-estilisticos", "figuras-literarias"],
    ),
    GrammarTopic(
        slug="preterito-mais-que-perfeito",
        title="Pretérito mais-que-perfeito composto",
        level="B2",
        category="Tempos verbais",
        summary="Revisão do MQP composto.",
        explanation="Ter (imperfeito) + particípio. Muito mais comum que a forma simples.",
        rules=[
            "Ter (imperfeito) + particípio.",
            "Mais comum que a forma simples.",
        ],
        examples=[
            GrammarExample(
                text="Quando cheguei, ela já tinha saído.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando cheguei, ela já tinha saiu.",
                correct="Quando cheguei, ela já tinha saído.",
                note="Ter + particípio (saído).",
            ),
        ],
        related=[
            "mais-que-perfeito",
            "preterito-imperfeito",
            "discurso-indireto-passado",
        ],
    ),
    GrammarTopic(
        slug="linguagem-jornalistica",
        title="Linguagem jornalística",
        level="B2",
        category="Avançado",
        summary="Características da linguagem jornalística em EP.",
        explanation="Título conciso, lead 5W, objetividade (3a pessoa), passiva, nominalizações, presente histórico.",
        rules=[
            "Título conciso.",
            "Lead 5W.",
            "3a pessoa, passiva.",
            "Presente histórico.",
        ],
        examples=[
            GrammarExample(
                text="O Governo anunciou ontem um novo pacote de medidas.",
                translation=None,
                note="lead",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eu entrevistei o presidente.",
                correct="O presidente afirmou que...",
                note="Jornalismo evita 1a pessoa.",
            ),
        ],
        related=["titulos", "discurso-reportado", "registo-formal"],
    ),
    GrammarTopic(
        slug="titulos",
        title="Títulos jornalísticos",
        level="B2",
        category="Avançado",
        summary="Estrutura e estilo dos títulos na imprensa portuguesa.",
        explanation="Concisão, omissão de artigos, presente histórico, vírgula em vez de conjunção.",
        rules=[
            "Omitir artigos.",
            "Presente histórico.",
            "Vírgula = e/mas.",
        ],
        examples=[
            GrammarExample(
                text="Incendio devasta milhares de hectares no Algarve.",
                translation=None,
            ),
            GrammarExample(text="Benfica vence, Porto empata.", translation=None),
        ],
        common_mistakes=[],
        related=["linguagem-jornalistica", "discurso-reportado"],
    ),
    GrammarTopic(
        slug="discurso-reportado",
        title="Discurso reportado",
        level="B2",
        category="Discurso indireto",
        summary="Técnicas avançadas de citação e reportagem.",
        explanation="Citação direta, indireta, mista. Verbos introdutores variados: afirmar, salientar, admitir, garantir, anunciar.",
        rules=[
            "Variar verbos introdutores.",
            "Direta, indireta, mista.",
        ],
        examples=[
            GrammarExample(
                text="O ministro salientou que os resultados são animadores.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ele disse que estou cansado.",
                correct="Ele disse que estava cansado.",
                note="Citação indireta adapta tempos.",
            ),
        ],
        related=[
            "discurso-indireto",
            "discurso-indireto-passado",
            "linguagem-jornalistica",
        ],
    ),
]
