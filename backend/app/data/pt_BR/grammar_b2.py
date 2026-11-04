"""Brazilian Portuguese (grammar_b2) learning content."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="imperfeito-conjuntivo",
        title="Imperfeito do subjuntivo",
        level="B2",
        category="Subjuntivo",
        summary="Formação e uso do imperfeito do subjuntivo.",
        explanation="Retire -ram da terceira pessoa do plural do pretérito perfeito e acrescente -sse, -sses, -sse, -ssemos, -sseis, -ssem: falaram -> falasse; tiveram -> tivesse; foram -> fosse. O imperfeito pode situar um desejo no passado (Queria que ela viesse) ou uma hipótese presente/futura (Se tivesse tempo, iria). Com embora, pode apresentar um fato concedido: Embora chovesse, saímos; com como se, uma comparação hipotética: Falava como se soubesse tudo.",
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
        explanation="Use ter ou haver no imperfeito do subjuntivo + particípio: tivesse estudado, houvesse concluído. A forma apresenta anterioridade em relação a uma referência passada ou hipotética: Duvidava que ela tivesse chegado. Em Se tivesse estudado, teria passado, a condição passada é apresentada como não realizada. O tempo também ocorre fora de condições contrafactuais: Embora tivesse estudado, ficou nervoso.",
        rules=[
            "Forma composta: tivesse + particípio.",
            "Pode expressar condição passada não realizada, mas também anterioridade em outros contextos.",
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
                note="Na norma-padrão, o infinitivo com sujeito explícito tu recebe -es; a oração principal impessoal não exige um sujeito diferente.",
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
        explanation="Desde que, a menos que e caso introduzem condições com subjuntivo: Vou desde que você vá; Irei, a menos que chova. Para que e a fim de que exprimem finalidade: Expliquei para que entendessem. Ainda que e mesmo que introduzem concessão: Mesmo que chova, iremos. Desde que também pode ser temporal e usar indicativo: Desde que chegou, trabalha aqui.",
        rules=[
            "Desde que condicional e a menos que usam subjuntivo; desde que temporal pode usar indicativo.",
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
        explanation="A coesão liga partes de um texto. Pronomes retomam referentes (Ana chegou. Ela trouxe os dados); elipses evitam repetir elementos recuperáveis (Ana revisou o texto e enviou o arquivo); conectores explicitam relações (O prazo acabou, portanto encerraremos as inscrições). Sinônimos e termos relacionados mantêm o tema, mas não são sempre intercambiáveis. Repetir um termo técnico pode ser mais claro do que substituí-lo por um sinônimo impreciso.",
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
                wrong="Ana enviou a versão a Carla. Ela será publicada amanhã.",
                correct="Ana enviou a versão a Carla. Essa versão será publicada amanhã.",
                note="A reformulação explicita que o referente é a versão; repetir um nome é útil quando o pronome permite leituras concorrentes.",
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
        explanation="Andar com a pulga atrás da orelha significa desconfiar; dar o braço a torcer é reconhecer um erro ou ceder; custar os olhos da cara indica preço muito alto. Estar de mau humor descreve irritação ou indisposição. O contexto distingue sentidos figurados e literais: dar o braço a torcer numa discussão não descreve uma lesão física.",
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
        explanation="Uma argumentação apresenta uma tese, sustenta-a com razões e evidências e conclui dentro dos limites dessas evidências. Por exemplo: ampliar o horário da biblioteca favorece quem trabalha (tese); uma pesquisa local identifica demanda noturna (apoio); os custos de pessoal exigem um projeto-piloto (ressalva). A conclusão pode recomendar o teste da proposta, sem afirmar que seus benefícios já foram comprovados. Conectores como porque, porém e portanto tornam explícita a relação entre as ideias.",
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
        explanation="Contra-argumentar exige representar com fidelidade a posição discutida. Uma concessão reconhece um ponto válido antes de limitar sua conclusão: Embora a medida reduza custos imediatos, a manutenção pode encarecê-la. Também é possível questionar uma premissa ou apresentar evidência contrária. Diferencie discordar da conclusão, contestar os dados e atacar a pessoa; apenas os dois primeiros enfrentam o argumento.",
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
                wrong="A proposta de Ana é inviável porque ela é antipática.",
                correct="A proposta de Ana é inviável porque seu custo supera o orçamento disponível.",
                note="O exemplo troca um ataque pessoal por uma razão pertinente; a alegação sobre o custo precisa ser sustentada por dados.",
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
        explanation="Matizadores ajustam o compromisso com uma afirmação ou limitam seu alcance. Provavelmente indica uma avaliação de probabilidade; talvez apresenta uma possibilidade e, antes do verbo, costuma usar subjuntivo: Talvez funcione. Até certo ponto limita a concordância, e apenas restringe o alcance: Apenas dois grupos participaram. Ao reformular, preserve a certeza, a intensidade e o alcance do original; tornar uma frase mais curta não autoriza torná-la mais categórica.",
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
                correct="Talvez seja melhor.",
                note="A versão concisa elimina a redundância sem trocar possibilidade por probabilidade; a original pode ser uma hesitação oral, não um erro de concordância.",
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
        explanation="O imperfeito apresenta situações em curso ou habituais no passado; o perfeito apresenta eventos como concluídos; o mais-que-perfeito situa um evento antes de outra referência passada. Compare: Chovia quando Ana chegou. Ela tinha esquecido o guarda-chuva. Essas funções orientam a narrativa, mas não são rótulos exclusivos: o perfeito também pode resumir um período (Morou ali por dez anos).",
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
                wrong="As paredes da casa era azuladas.",
                correct="As paredes da casa eram azuladas.",
                note="O verbo concorda com paredes. Uma frase simples como A casa era bonita é válida; acrescentar melancolia mudaria o sentido, não apenas o estilo.",
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
        explanation="Uma notícia organiza informações verificáveis e atribui declarações às fontes. O lide costuma responder ao que aconteceu, com quem, quando, onde e por quê ou como, conforme os dados disponíveis. A terceira pessoa, a passiva e as nominalizações são recursos possíveis, mas não garantem objetividade. Diferencie fatos confirmados, alegações e interpretações; não transforme suspeitas em certezas ao resumir.",
        rules=[
            "Título conciso.",
            "Lide: o quê, quem, quando, onde, por quê e como, conforme a informação disponível.",
            "Atribua alegações às fontes; a pessoa gramatical não garante objetividade.",
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
        explanation="Títulos sintetizam o fato principal. Podem usar presente para dar atualidade a fatos recentes e omitir artigos quando a leitura continuar clara. A vírgula pode separar orações em uma construção assindética, mas não substitui automaticamente qualquer conjunção: retirar mas ou porque pode apagar uma relação importante. Preserve autoria, condição e grau de certeza, mesmo sob um limite de espaço.",
        rules=[
            "Omita artigos apenas quando isso mantiver clareza e naturalidade.",
            "Presente histórico.",
            "Não elimine conectores que sejam necessários para preservar a relação entre os fatos.",
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
        explanation="A citação direta preserva as palavras entre aspas; a indireta integra o conteúdo à fala do narrador; a mista combina as duas. Ajuste pessoa, tempo e referências sem alterar quem fez ou disse algo. Paulo disse: Estou cansado pode ser relatado como Paulo disse que estava cansado ou que está cansado, conforme a perspectiva temporal. Ele disse que estou cansado também é gramatical: nesse caso, o cansaço é de quem relata. Afirmar, admitir e garantir não são sinônimos perfeitos; escolha o verbo conforme a atitude da fonte.",
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
                wrong="Paulo disse que ele próprio estavam cansado.",
                correct="Paulo disse que ele próprio estava cansado.",
                note="Corrija a concordância sem mudar o participante. A escolha entre está e estava depende da referência temporal.",
            ),
        ],
        related=[
            "discurso-indireto",
            "discurso-indireto-passado",
            "linguagem-jornalistica",
        ],
    ),
]
