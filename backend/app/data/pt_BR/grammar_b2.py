"""Brazilian Portuguese (grammar_b2) learning content."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="imperfeito-conjuntivo",
        title="Imperfeito do subjuntivo",
        level="B2",
        category="Subjuntivo",
        summary="Formação e uso do imperfeito do subjuntivo.",
        explanation="Da 3a pl. do pretérito perfeito: falaram -> falasse, falasses... Usos: condições hipotéticas, desejos, após embora/como se.",
        rules=[
            "Da 3a pl. do pret. perfeito.",
            "Com se, embora, como se.",
        ],
        examples=[
            GrammarExample(
                text="Se eu tivesse mais tempo, viajava mais.",
            ),
            GrammarExample(
                text="Embora chovesse, fomos à praia.",
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
        title="Mais-que-perfeito do subjuntivo",
        level="B2",
        category="Subjuntivo",
        summary="Expressar condições passadas não realizadas.",
        explanation="Forma composta: tivesse + particípio passado. Se tivesse estudado, teria passado.",
        rules=[
            "Forma composta: tivesse + particípio.",
            "Condição NÃO realizada no passado.",
        ],
        examples=[
            GrammarExample(
                text="Se tivesse estudado, teria passado.",
            ),
            GrammarExample(
                text="Se ela tivesse vindo, teria sido melhor.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se eu tivesse estudar, teria passado.",
                correct="Se eu tivesse estudado, teria passado.",
                note="O mais-que-perfeito do subjuntivo usa tivesse + particípio, não infinitivo.",
            ),
        ],
        related=[
            "imperfeito-conjuntivo",
            "condicional-composto",
        ],
    ),
    GrammarTopic(
        slug="concordancia-temporal",
        title="Concordância temporal",
        level="B2",
        category="Tempos verbais",
        summary="Regras de correspondência entre tempos verbais.",
        explanation="A escolha do tempo depende da relação temporal e da perspectiva, não apenas do tempo da oração principal.\n\nEspero que venhas apresenta uma ação simultânea ou posterior; Espero que tenhas chegado apresenta anterioridade. Queria que viesses usa o imperfeito; Duvidava que tivesse chegado usa o mais-que-perfeito para anterioridade passada. Uma principal presente admite referência passada: Duvido que fosse verdade.",
        rules=[
            "Distingue simultaneidade, anterioridade e posterioridade.",
            "A perspectiva temporal determina a escolha entre formas simples e compostas.",
        ],
        examples=[
            GrammarExample(
                text="Queria que viesses.",
                note="pretérito -> imperfeito conj.",
            ),
            GrammarExample(
                text="Espero que chegues.",
                note="presente -> presente conj.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Queria que tu viesse.",
                correct="Queria que viesses.",
                note="Com tu, a forma é viesses; o tempo depende da perspectiva temporal.",
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
        title="Perífrases aspectuais",
        level="B2",
        category="Verbos",
        summary="Marcar início, continuidade, repetição e conclusão.",
        explanation="Começar a + infinitivo marca início; estar + gerúndio apresenta ação em curso; continuar + gerúndio mantém uma ação; acabar de + infinitivo indica conclusão recente; voltar a + infinitivo indica retomada. Compare Comecei a estudar, Estou estudando e Acabei de estudar. A escolha do auxiliar muda a perspectiva sobre a ação.",
        rules=[
            "Começar a e voltar a exigem a antes do infinitivo.",
            "Estar e continuar admitem gerúndio.",
            "Acabar de descreve conclusão recente nesse uso.",
        ],
        examples=[
            GrammarExample(
                text="Comecei a aprender português.",
            ),
            GrammarExample(
                text="Continuo estudando todos os dias.",
            ),
            GrammarExample(
                text="Acabei de chegar.",
            ),
            GrammarExample(
                text="Voltei a trabalhar ontem.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Comecei estudar.",
                correct="Comecei a estudar.",
                note="Use a antes do infinitivo.",
            ),
            GrammarMistake(
                wrong="Estou a estudando.",
                correct="Estou estudando.",
                note="Use a construção brasileira com gerúndio.",
            ),
        ],
        related=[
            "estar-gerundio",
            "andar-estar-gerundio",
            "costumava",
        ],
    ),
    GrammarTopic(
        slug="perifrases-modais",
        title="Perífrases modais",
        level="B2",
        category="Verbos",
        summary="Expressar obrigação, necessidade e possibilidade.",
        explanation="Ter que e ter de + infinitivo indicam obrigação: Tenho que sair. Precisar + infinitivo é muito comum no Brasil: Preciso estudar; antes de substantivo, use de: Preciso de ajuda. Poder expressa possibilidade ou permissão. Haver de pode expressar expectativa ou determinação, mas costuma ser mais marcado: Hei de conseguir.",
        rules=[
            "Use precisar de antes de substantivo.",
            "Depois de auxiliar modal, mantenha o infinitivo.",
            "Diferencie obrigação de possibilidade.",
        ],
        examples=[
            GrammarExample(
                text="Tenho que terminar o relatório.",
            ),
            GrammarExample(
                text="Preciso estudar hoje.",
            ),
            GrammarExample(
                text="Preciso de ajuda.",
            ),
            GrammarExample(
                text="Você pode entrar.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Preciso ajuda.",
                correct="Preciso de ajuda.",
                note="Antes do substantivo ajuda, precisar exige de.",
            ),
            GrammarMistake(
                wrong="Você pode entra.",
                correct="Você pode entrar.",
                note="Depois de poder, use infinitivo.",
            ),
        ],
        related=[
            "perifrases-aspetuais",
            "querer-poder",
            "andar-estar-gerundio",
        ],
    ),
    GrammarTopic(
        slug="andar-estar-gerundio",
        title="Andar e estar + gerúndio",
        level="B2",
        category="Verbos",
        summary="Distinguir ação atual e comportamento recorrente.",
        explanation="Estar + gerúndio pode situar uma ação no momento de referência: Estou lendo agora. Andar + gerúndio costuma apresentar atividade recorrente ou prolongada num período recente: Ando lendo bastante. O contexto define a duração; não são formas sempre intercambiáveis. Estar também pode abranger um período: Estou trabalhando em um projeto este mês.",
        rules=[
            "Use andar + gerúndio para um comportamento recente ou recorrente.",
            "Use estar + gerúndio para ação em curso no momento ou período indicado.",
            "A diferença é aspectual e depende do contexto.",
        ],
        examples=[
            GrammarExample(
                text="Estou lendo agora.",
            ),
            GrammarExample(
                text="Ando lendo muito ultimamente.",
            ),
            GrammarExample(
                text="Ela anda trabalhando demais.",
            ),
            GrammarExample(
                text="Estamos preparando o relatório desta semana.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ando a trabalhando demais.",
                correct="Ando trabalhando demais.",
                note="Não misture a + infinitivo com gerúndio.",
            ),
        ],
        related=[
            "estar-gerundio",
            "perifrases-aspetuais",
        ],
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
            ),
            GrammarExample(
                text="Para chegarmos a tempo, temos de sair.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É importante tu estudar.",
                correct="É importante tu estudares.",
                note="Sujeito diferente -> infinitivo pessoal.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "colocacao-pronominal",
        ],
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
            ),
            GrammarExample(
                text="Sairei mais cedo, a menos que haja reunião.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Desde que tu também vais.",
                correct="Desde que tu também vás.",
                note="Desde que condicional + subjuntivo.",
            ),
        ],
        related=[
            "conectores-argumentativos",
            "coesao-textual",
        ],
    ),
    GrammarTopic(
        slug="coesao-textual",
        title="Coesão textual",
        level="B2",
        category="Avançado",
        summary="Mecanismos para textos coesos.",
        explanation="Referência, substituição, elipse, conjunção, coesão lexical.",
        rules=[
            "Pronomes, sinônimos, conectores.",
            "Elipse quando possível.",
        ],
        examples=[
            GrammarExample(
                text="O João comprou um carro. Ele está contente com o veículo.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="O João comprou um carro. O João está contente.",
                correct="O João comprou um carro. Ele está contente.",
                note="Evitar repetição excessiva.",
            ),
        ],
        related=[
            "conectores-avancados",
            "conectores-argumentativos",
        ],
    ),
    GrammarTopic(
        slug="registo-formal",
        title="Registro formal",
        level="B2",
        category="Avançado",
        summary="Comunicar-se com clareza, precisão e cortesia.",
        explanation="O registro formal depende do gênero e do destinatário. Em e-mails profissionais brasileiros, Prezada Ana e Atenciosamente são opções usuais. Pedidos com poderia ou gostaria suavizam a solicitação. Evite gírias quando o contexto exigir neutralidade, mas não confunda formalidade com frases rebuscadas ou mesóclise obrigatória.",
        rules=[
            "Escolha tratamento adequado ao destinatário.",
            "Prefira clareza a rebuscamento.",
            "Mantenha concordância e convenções do gênero textual.",
        ],
        examples=[
            GrammarExample(
                text="Poderia me informar o horário?",
            ),
            GrammarExample(
                text="Prezada Ana, envio o documento solicitado.",
            ),
            GrammarExample(
                text="O senhor deseja mais alguma informação?",
            ),
            GrammarExample(
                text="Agradeço a atenção.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Os documento segue anexo.",
                correct="Os documentos seguem anexos.",
                note="Sujeito, verbo e adjetivo devem concordar.",
            ),
        ],
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
        summary="Interpretar expressões idiomáticas usadas no Brasil.",
        explanation="Andar com a pulga atrás da orelha, dar o braço a torcer, estar de mau humor, custar os olhos da cara.",
        rules=[
            "Expressões fixas.",
            "Sentido literal diferente do figurado.",
        ],
        examples=[
            GrammarExample(
                text="Ando com a pulga atrás da orelha.",
            ),
            GrammarExample(
                text="Ela está de mau humor hoje.",
            ),
        ],
        related=[
            "expressoes-coloquiais",
            "proverbios",
            "registo-formal",
        ],
    ),
    GrammarTopic(
        slug="expressoes-coloquiais",
        title="Expressões coloquiais brasileiras",
        level="B2",
        category="Avançado",
        summary="Interpretar expressões informais conforme o contexto.",
        explanation="Legal pode avaliar algo positivamente: O filme foi legal. Beleza pode indicar acordo ou funcionar como pergunta informal. Bora é um convite coloquial, e valeu pode agradecer. Essas formas variam por região, idade e situação; não representam toda a fala brasileira. Em mensagens formais, prefira opções neutras como Obrigado e De acordo.",
        rules=[
            "Considere relação, região e grau de formalidade.",
            "Não traduza expressões literalmente.",
            "Em documentos formais, prefira equivalentes neutros.",
        ],
        examples=[
            GrammarExample(
                text="Que filme legal!",
            ),
            GrammarExample(
                text="Bora tomar um café?",
            ),
            GrammarExample(
                text="Valeu pela ajuda!",
            ),
            GrammarExample(
                text="Tudo bem? Beleza!",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Valeu, galera! em uma resposta institucional solene.",
                correct="Agradeço a colaboração de todos.",
                note="A reformulação ajusta o registro; a expressão original é válida na conversa.",
            ),
        ],
        related=[
            "expressoes-idiomaticas",
            "proverbios",
            "registo-formal",
        ],
    ),
    GrammarTopic(
        slug="proverbios",
        title="Provérbios em português",
        level="B2",
        category="Avançado",
        summary="Interpretar provérbios usados no Brasil e em outros países lusófonos.",
        explanation="Água mole em pedra dura..., Quem vê caras não vê corações, Mais vale um pássaro na mão..., Depois da tempestade vem a bonança.",
        rules=[
            "Provérbios fixos.",
            "Sabedoria popular.",
        ],
        examples=[
            GrammarExample(
                text="Água mole em pedra dura, tanto bate até que fura.",
            ),
            GrammarExample(
                text="Mais vale um pássaro na mão do que dois voando.",
            ),
        ],
        related=[
            "expressoes-idiomaticas",
            "expressoes-coloquiais",
        ],
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
            ),
            GrammarExample(
                text="Concluindo, os benefícios superam os riscos.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Os dados mostra que a medida funciona.",
                correct="Os dados mostram que a medida funciona.",
                note="O verbo concorda com dados. A primeira pessoa não é proibida num texto argumentativo; escolhe o registro conforme o gênero e as instruções.",
            ),
        ],
        related=[
            "contra-argumentacao",
            "conectores-argumentativos",
            "coesao-textual",
        ],
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
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Isso é mentira. (agressivo)",
                correct="Essa perspectiva parece ignorar alguns fatos.",
                note="Contra-argumentação respeitosa.",
            ),
        ],
        related=[
            "estrutura-argumentativa",
            "matizadores",
            "conectores-argumentativos",
        ],
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
            ),
            GrammarExample(
                text="De certa forma, concordo.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Possivelmente talvez seja melhor.",
                correct="Provavelmente é melhor.",
                note="Evitar acumular matizadores.",
            ),
        ],
        related=[
            "estrutura-argumentativa",
            "contra-argumentacao",
        ],
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
                text="O sol punha-se no horizonte, tingindo o céu de tons alaranjados.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A casa era bonita. (pobre)",
                correct="A casa exibia uma beleza melancólica.",
                note="Vocabulário rico.",
            ),
        ],
        related=[
            "tempos-narrativos",
            "recursos-estilisticos",
            "figuras-literarias",
        ],
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
        summary="Organizar notícias e distinguir informação de opinião.",
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
                note="lead",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Os dados comprova a hipótese.",
                correct="Os dados comprovam a hipótese.",
                note="Dados exige plural. A primeira pessoa pode ocorrer em reportagem autoral; preserve os fatos ao reformular.",
            ),
        ],
        related=[
            "titulos",
            "discurso-reportado",
            "registo-formal",
        ],
    ),
    GrammarTopic(
        slug="titulos",
        title="Títulos jornalísticos",
        level="B2",
        category="Avançado",
        summary="Estrutura e estilo dos títulos na imprensa brasileira.",
        explanation="Concisão, omissão de artigos, presente histórico, vírgula em vez de conjunção.",
        rules=[
            "Omitir artigos.",
            "Presente histórico.",
            "Vírgula = e/mas.",
        ],
        examples=[
            GrammarExample(
                text="Incêndio atinge área de preservação no Cerrado.",
            ),
            GrammarExample(
                text="Seleção vence e avança para a final.",
            ),
        ],
        related=[
            "linguagem-jornalistica",
            "discurso-reportado",
        ],
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
