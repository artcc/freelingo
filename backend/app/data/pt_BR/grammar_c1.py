"""Brazilian Portuguese (grammar_c1) learning content."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="subjuntivo-concessivo",
        title="Subjuntivo em orações concessivas",
        level="C1",
        category="Subjuntivo",
        summary="Uso avançado do subjuntivo em orações concessivas.",
        explanation="Por mais que, por muito que, ainda que, mesmo que, nem que + subjuntivo.",
        rules=[
            "Por mais/muito que + subjuntivo.",
            "Ainda que/mesmo que + subjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Por mais que tentes, nem sempre vais conseguir.",
            ),
            GrammarExample(
                text="Mesmo que me pagassem, não faria esse trabalho.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Por mais que tentas.",
                correct="Por mais que tentes.",
                note="Por mais que exige subjuntivo.",
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
        title="Subjuntivo em orações finais",
        level="C1",
        category="Subjuntivo",
        summary="Subjuntivo após conectores finais.",
        explanation="Para que/a fim de que/de modo a que + subjuntivo (sujeito diferente). Mesmo sujeito: para + infinitivo.",
        rules=[
            "Para que + conj. (sujeito diferente).",
            "Mesmo sujeito: para + inf.",
        ],
        examples=[
            GrammarExample(
                text="Enviei o email para que todos fiquem informados.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Estudo para eu passarão.",
                correct="Estudo para passar.",
                note="Com o mesmo sujeito, para + infinitivo é geralmente mais econômico; para que eu passe também pode ser gramatical.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "conectores-avancados",
            "infinitivo-pessoal",
        ],
    ),
    GrammarTopic(
        slug="subjuntivo-relativo",
        title="Subjuntivo em orações relativas",
        level="C1",
        category="Subjuntivo",
        summary="Subjuntivo com antecedente indeterminado.",
        explanation="Subjuntivo para antecedente desconhecido. Indicativo para específico. Há quem / Não há quem + subjuntivo.",
        rules=[
            "Subjuntivo: hipotético.",
            "Indicativo: específico.",
        ],
        examples=[
            GrammarExample(
                text="Procuro alguém que fale chinês.",
                note="indeterminado",
            ),
            GrammarExample(
                text="Conheço alguém que fala chinês.",
                note="específico",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Procuro alguém que falem chinês.",
                correct="Procuro alguém que fale chinês.",
                note="Alguém exige singular. O subjuntivo apresenta um perfil desejado; o indicativo pode referir alguém cuja existência é assumida.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "que-relativo",
        ],
    ),
    GrammarTopic(
        slug="passiva-reflexa",
        title="Voz passiva reflexa",
        level="C1",
        category="Voz passiva",
        summary="Usos avançados da voz passiva com o pronome se.",
        explanation="Aprecia-se, comenta-se, realizar-se-á (mesóclise), observa-se. Uso acadêmico e jornalístico.",
        rules=[
            "Aprecia-se/comenta-se = passiva reflexa.",
            "Realizar-se-á = será realizado.",
        ],
        examples=[
            GrammarExample(
                text="Comenta-se que o acordo será assinado amanhã.",
            ),
            GrammarExample(
                text="Observa-se uma melhoria significativa.",
            ),
        ],
        related=[
            "voz-passiva",
            "se-impessoal",
            "se-passivo",
        ],
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
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A realização da implementação da verificação.",
                correct="A verificação dos dados.",
                note="Evitar cadeias.",
            ),
        ],
        related=[
            "impessoalidade",
            "registo-formal",
            "coesao-textual",
        ],
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
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Foram observado aumentos significativos.",
                correct="Foram observados aumentos significativos.",
                note="O particípio concorda com aumentos. A primeira pessoa é válida em vários gêneros acadêmicos; a escolha depende das convenções da área.",
            ),
        ],
        related=[
            "nominalizacao",
            "voz-passiva",
            "registo-formal",
        ],
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
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Usar léxico de campo errado.",
                correct="Verificar o campo semântico adequado.",
                note="",
            ),
        ],
        related=[
            "derivacao",
            "precisao-lexica",
        ],
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
            GrammarExample(
                text="feliz -> infeliz -> felicidade",
            ),
            GrammarExample(
                text="construir -> construção -> reconstrutivo",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A desfelicidade dele era evidente.",
                correct="A infelicidade dele era evidente.",
                note="Infelicidade é a forma lexical estabelecida; nem todos os prefixos se combinam livremente com todas as bases.",
            ),
        ],
        related=[
            "campos-semanticos",
            "precisao-lexica",
        ],
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
            "Saber (fato) vs conhecer (familiaridade).",
        ],
        examples=[
            GrammarExample(
                text="Sei a resposta. / Conheço bem essa pessoa.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Conheço nadar.",
                correct="Sei nadar.",
                note="Saber + infinitivo exprime uma capacidade. Conheço a resposta e Sei a resposta são ambas construções válidas.",
            ),
        ],
        related=[
            "derivacao",
            "campos-semanticos",
            "falsos-amigos",
        ],
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
        related=[
            "humor-brasileiro",
            "duplo-sentido",
            "recursos-retoricos",
        ],
    ),
    GrammarTopic(
        slug="humor-brasileiro",
        title="Humor, ironia e contexto no Brasil",
        level="C1",
        category="Avançado",
        summary="Interpretar humor sem transformar diferenças culturais em estereótipos.",
        explanation="O humor pode explorar contraste entre expectativa e realidade, exagero, trocadilho e ironia. No Brasil, esses recursos aparecem em conversas, crônicas, tirinhas e comédia. Nenhum recurso define todos os brasileiros. O tom, a relação e a situação permitem distinguir brincadeira, crítica e ofensa.",
        rules=[
            "Identifique o sentido literal e o sentido sugerido.",
            "Considere contexto e reação do interlocutor.",
            "Não atribua uma única personalidade a uma população.",
        ],
        examples=[
            GrammarExample(
                text="Que pontualidade! disse ela quando o amigo chegou uma hora atrasado.",
            ),
            GrammarExample(
                text="O orçamento encolheu, mas a lista de desejos cresceu.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Todo comentário sarcástico é uma brincadeira amigável.",
                correct="O efeito do sarcasmo depende do contexto e da relação.",
                note="Sarcasmo também pode ofender.",
            ),
        ],
        related=[
            "ironia",
            "duplo-sentido",
            "expressoes-idiomaticas",
        ],
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
        related=[
            "ironia",
            "humor-brasileiro",
            "recursos-retoricos",
        ],
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
            ),
            GrammarExample(
                text="O silêncio ensurdecedor da noite. (paradoxo)",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Uso excessivo.",
                correct="Dosear as figuras.",
                note="",
            ),
        ],
        related=[
            "persuasao",
            "figuras-literarias",
        ],
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
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Apelos emocionais sem fundamentação.",
                correct="Combinar pathos com logos.",
                note="",
            ),
        ],
        related=[
            "recursos-retoricos",
            "estrutura-argumentativa",
        ],
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
            GrammarExample(
                text="O tempo é dinheiro. (metáfora)",
            ),
            GrammarExample(
                text="Portugal venceu o jogo. (metonímia)",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Confundir metáfora com comparação.",
                correct="Metáfora = identificação. Comparação = como.",
                note="",
            ),
        ],
        related=[
            "descricao-literaria",
            "recursos-retoricos",
            "estilo-literario",
        ],
    ),
    GrammarTopic(
        slug="portugues-brasileiro",
        title="Português brasileiro e outras variedades",
        level="C1",
        category="Avançado",
        summary="Comparar variedades sem hierarquizar os falantes.",
        explanation="O português é pluricêntrico. No Brasil são comuns estar + gerúndio, você com terceira pessoa, a gente com singular e próclise na conversa. Portugal costuma usar estar a + infinitivo e tem outras preferências de colocação pronominal. Há variação interna nos dois países. As normas escritas compartilham muitos recursos, mas não são idênticas.",
        rules=[
            "Compare tendências, não regras absolutas sobre todos os falantes.",
            "Mantenha a variedade-alvo quando o exercício pedir produção consistente.",
            "Não trate diferenças legítimas como inferioridade linguística.",
        ],
        examples=[
            GrammarExample(
                text="Brasil: Estou estudando. Portugal: Estou a estudar.",
            ),
            GrammarExample(
                text="Brasil: celular. Portugal: telemóvel.",
            ),
            GrammarExample(
                text="Brasil: café da manhã. Portugal: pequeno-almoço.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Todo brasileiro usa os mesmos pronomes e o mesmo sotaque.",
                correct="O Brasil apresenta variação regional, social e situacional.",
                note="Você e tu têm distribuições variadas.",
            ),
        ],
        related=[
            "portugues-europeu",
            "diferencas-regionais",
        ],
    ),
    GrammarTopic(
        slug="portugues-europeu",
        title="Português europeu: leitura contrastiva",
        level="C1",
        category="Avançado",
        summary="Reconhecer usos portugueses sem os impor à produção brasileira.",
        explanation="Em muitos contextos de Portugal, encontram-se estar a + infinitivo, ênclise em frases afirmativas e artigo antes de possessivos e nomes. Na leitura comparativa, compreenda Estou a ler como Estou lendo. Isso não autoriza classificar o gerúndio como inexistente em Portugal, nem a próclise como exclusiva do Brasil. O registro também influencia as escolhas.",
        rules=[
            "Reconheça vocabulário regional como comboio e autocarro.",
            "Diferencie compreensão de outra variedade e produção na variedade-alvo.",
            "Evite generalizações absolutas sobre colocação pronominal.",
        ],
        examples=[
            GrammarExample(
                text="Portugal: O Pedro está a estudar. Brasil: Pedro está estudando.",
            ),
            GrammarExample(
                text="Portugal: comboio. Brasil: trem.",
            ),
            GrammarExample(
                text="Portugal: autocarro. Brasil: ônibus.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Estou lendo é um erro em português.",
                correct="Estou lendo é uma construção normal no português brasileiro.",
                note="A avaliação deve considerar a variedade e o contexto.",
            ),
        ],
        related=[
            "portugues-brasileiro",
            "diferencas-regionais",
            "estar-gerundio",
        ],
    ),
    GrammarTopic(
        slug="diferencas-regionais",
        title="Variação regional no Brasil",
        level="C1",
        category="Avançado",
        summary="Reconhecer diferenças de pronúncia, vocabulário e tratamento.",
        explanation="O Brasil reúne variedades regionais e sociais que não coincidem perfeitamente com fronteiras estaduais. Tu e você têm distribuições diferentes e também variam dentro de uma mesma cidade. Mandioca, aipim e macaxeira mostram diversidade lexical, embora os usos comerciais e locais possam distinguir variedades da planta. A realização de r, s, t e d varia. Nenhum sotaque é intrinsecamente mais correto.",
        rules=[
            "Considere região, grupo social e situação de comunicação.",
            "Não confunda norma escrita com um único sotaque.",
            "Use exemplos regionais como tendências, não como fronteiras rígidas.",
        ],
        examples=[
            GrammarExample(
                text="Você quer café? e Tu queres café? pertencem a repertórios brasileiros.",
            ),
            GrammarExample(
                text="A palavra mandioca também convive com aipim e macaxeira.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Só existe um sotaque brasileiro correto.",
                correct="Existem vários sotaques brasileiros legítimos.",
                note="Convenções de escrita não eliminam a variação oral.",
            ),
        ],
        related=[
            "portugues-europeu",
            "portugues-brasileiro",
        ],
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
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Síntese demasiado longa.",
                correct="Síntese concisa.",
                note="",
            ),
        ],
        related=[
            "coesao-textual",
            "critica-construtiva",
            "reformulacao",
        ],
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
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Isto está errado.",
                correct="Esta secção poderia beneficiar de uma revisão.",
                note="",
            ),
        ],
        related=[
            "reformulacao",
            "matizadores",
            "registo-formal",
        ],
    ),
    GrammarTopic(
        slug="reformulacao",
        title="Reformulação",
        level="C1",
        category="Avançado",
        summary="Técnicas para reformular ideias.",
        explanation="Isto é, ou seja, dito de outra forma. Parafrasear, mudar registro, alterar voz.",
        rules=[
            "Isto é / ou seja.",
            "Adaptar registro.",
        ],
        examples=[
            GrammarExample(
                text="O evento foi cancelado. Ou seja, não haverá concerto.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ou seja, tipo, quer dizer...",
                correct="Ou seja,...",
                note="Um reformulador é suficiente.",
            ),
        ],
        related=[
            "sintese-textual",
            "critica-construtiva",
            "registo-formal",
        ],
    ),
]
