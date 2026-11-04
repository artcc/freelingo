"""Brazilian Portuguese (grammar_c2) learning content."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="revisao-conjuntivo",
        title="Revisão geral do subjuntivo",
        level="C2",
        category="Subjuntivo",
        summary="Domínio completo do subjuntivo.",
        explanation="O subjuntivo articula a perspectiva do falante e a relação temporal, sem corresponder sempre a dúvida. Compare Espero que venha (ação simultânea ou posterior), Espero que tenha chegado (anterioridade), Queria que viesse (perspectiva passada ou desejo atenuado) e Duvidava que tivesse chegado (anterioridade passada). O futuro ocorre em Quando chegar, avise; o futuro composto, em Quando tiver terminado, avise, destaca conclusão anterior a outra ação futura. A escolha depende também do conector: Caso venha amanhã usa presente apesar da referência futura; Embora tenha estudado pode conceder um fato.",
        rules=[
            "Distinga presente, imperfeito e futuro, com suas formas compostas de anterioridade.",
            "Considere conector, perspectiva temporal e estatuto da informação; subjuntivo não equivale sempre a irrealidade.",
        ],
        examples=[
            GrammarExample(
                text="Qualquer que seja a decisão, estou de acordo.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Qualquer que é a decisão.",
                correct="Qualquer que seja a decisão.",
                note="Qualquer que + subjuntivo.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "imperfeito-conjuntivo",
            "futuro-do-conjuntivo",
        ],
    ),
    GrammarTopic(
        slug="revisao-condicional",
        title="Revisão geral dos condicionais",
        level="C2",
        category="Condicionais",
        summary="Domínio de todas as estruturas condicionais.",
        explanation="Uma condição aberta pode usar futuro do subjuntivo: Se você estudar, terá mais chances. Uma hipótese presente ou futura pode usar imperfeito do subjuntivo com futuro do pretérito: Se estudasse, saberia responder. Para uma condição passada não realizada: Se tivesse estudado, teria passado. Uma condicional mista relaciona tempos diferentes: Se tivesse estudado ontem, saberia a resposta agora. Na conversa brasileira, o imperfeito pode substituir o futuro do pretérito (Se tivesse tempo, ia), sem que isso torne os tempos equivalentes em todos os contextos. Se estudava, passava também pode descrever um hábito passado real.",
        rules=[
            "Diferencie condição aberta, hipótese e condição passada não realizada.",
            "Em condições mistas, identifique separadamente o tempo da condição e o da consequência.",
            "Interprete o imperfeito conforme contexto e registro, sem o classificar automaticamente como erro.",
        ],
        examples=[
            GrammarExample(
                text="Se você estudar, terá mais chances.",
            ),
            GrammarExample(
                text="Se eu tivesse tempo, ia com você.",
                note="coloquial brasileiro",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se eu tivesse estudar ontem, saberia a resposta agora.",
                correct="Se eu tivesse estudado ontem, saberia a resposta agora.",
                note="A forma composta exige particípio; a condição é passada e a consequência é presente.",
            ),
        ],
        related=[
            "condicional",
            "se-imperfeito-subjuntivo",
            "condicional-composto",
        ],
    ),
    GrammarTopic(
        slug="mesoclise",
        title="Mesóclise: leitura e registro",
        level="C2",
        category="Pronomes",
        summary="Reconhecer uma construção marcada da escrita formal.",
        explanation="A mesóclise insere um pronome no futuro do presente ou no futuro do pretérito: Entregar-lhe-ei; Dar-lhe-ia. É pouco frequente na conversa brasileira e ocorre em textos muito formais ou literários. Não equivale a maior correção em qualquer situação. Com elemento que exige próclise, use Não lhe entregarei. Na conversa, Vou entregar o documento para você preserva a intenção sem reproduzir a construção marcada.",
        rules=[
            "Reconheça o pronome entre radical e terminação.",
            "Não use mesóclise após negação no padrão formal.",
            "Escolha a construção conforme o registro, não por uma hierarquia de prestígio.",
        ],
        examples=[
            GrammarExample(
                text="Entregar-lhe-ei o relatório amanhã.",
            ),
            GrammarExample(
                text="Não lhe entregarei o relatório hoje.",
            ),
            GrammarExample(
                text="Vou entregar o relatório para você amanhã.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Não entregar-lhe-ei o relatório.",
                correct="Não lhe entregarei o relatório.",
                note="A negação exige próclise no padrão formal.",
            ),
        ],
        related=[
            "colocacao-pronominal",
            "futuro-do-presente",
            "condicional",
        ],
    ),
    GrammarTopic(
        slug="estilo-literario",
        title="Estilo literário",
        level="C2",
        category="Avançado",
        summary="Desenvolver uma voz literária autêntica.",
        explanation="O estilo resulta de escolhas de ritmo, sintaxe, léxico e ponto de vista. Frases curtas podem acelerar uma cena; períodos longos podem prolongar a percepção, sem que um formato seja sempre superior. Compare Ela estava apreensiva com Ela dobrou a carta três vezes antes de abrir a porta: a segunda versão sugere um estado por ações, mas acrescenta acontecimentos e não é uma paráfrase exata. Mostrar e contar são recursos complementares. Avalie cada escolha pelo efeito pretendido e pela coerência da voz narrativa.",
        rules=[
            "Variar estruturas.",
            "Léxico preciso.",
            "Combine descrição explícita e sugestão por ações conforme o efeito pretendido.",
        ],
        examples=[
            GrammarExample(
                text="O sol morria no horizonte, tingindo o São Francisco de ouro líquido.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Frases longas são sempre superiores às curtas em textos literários.",
                correct="A extensão das frases deve servir ao ritmo, à perspectiva e ao efeito do texto.",
                note="Uma preferência estilística não constitui uma regra universal de correção.",
            ),
        ],
        related=[
            "descricao-literaria",
            "recursos-estilisticos",
            "voz-narrativa",
        ],
    ),
    GrammarTopic(
        slug="voz-narrativa",
        title="Voz narrativa",
        level="C2",
        category="Avançado",
        summary="Tipos de narrador e construção da voz narrativa.",
        explanation="Distinga quem narra de quem percebe. Um narrador em primeira pessoa participa da história, mas pode desconhecer fatos ou interpretar mal outras personagens. Um narrador em terceira pessoa pode ter acesso amplo aos pensamentos (onisciência), limitar-se à perspectiva de uma personagem ou descrever apenas ações observáveis. No discurso indireto livre, a voz narrativa incorpora avaliações da personagem sem um verbo introdutor: Ana fechou a carta. Por que ele voltava justamente agora? A mudança de perspectiva pode ser intencional, desde que o texto a torne interpretável.",
        rules=[
            "Separe pessoa gramatical, participação na história e alcance do conhecimento do narrador.",
            "Terceira pessoa não implica onisciência.",
            "No discurso indireto livre, identifique de quem são as avaliações e os marcadores de perspectiva.",
        ],
        examples=[
            GrammarExample(
                text="Maria abriu a porta, aliviada; do outro lado, João escondia o medo. (acesso aos estados de duas personagens)",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="O relato está na terceira pessoa, portanto o narrador conhece todos os pensamentos.",
                correct="A terceira pessoa pode ter perspectiva limitada; é preciso observar a informação a que o narrador tem acesso.",
                note="A pessoa gramatical não determina sozinha a focalização.",
            ),
        ],
        related=[
            "estilo-literario",
            "descricao-literaria",
        ],
    ),
    GrammarTopic(
        slug="recursos-estilisticos",
        title="Recursos estilísticos avançados",
        level="C2",
        category="Avançado",
        summary="Sinestesia, aliteração, assonância, quiasmo.",
        explanation="A sinestesia aproxima sensações de domínios diferentes: uma voz aveludada associa audição e tato. A aliteração repete sons consonantais (O vento varria as vielas); a assonância repete sons vocálicos, como os /a/ de A clara madrugada alagava a sala. O quiasmo inverte a ordem de elementos em estruturas paralelas: Não vivemos para comer; comemos para viver. A anáfora repete o início de segmentos; a epífora, o final: Pediram justiça, exigiram justiça. Analise como som, repetição e ordem contribuem para o sentido, sem exigir essas figuras em todo texto.",
        rules=[
            "Sinestesia, aliteração, assonância, quiasmo.",
        ],
        examples=[
            GrammarExample(
                text="Sua voz aveludada acalmou a sala. (sinestesia)",
            ),
            GrammarExample(
                text="O vento varria as velhas vielas. (aliteração)",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Em O vento varria as vielas, a repetição de /v/ é assonância.",
                correct="A repetição do som consonantal /v/ é aliteração; assonância envolve sons vocálicos.",
                note="Identifique o som repetido, não apenas a letra ou a presença de repetição.",
            ),
        ],
        related=[
            "figuras-literarias",
            "estilo-literario",
        ],
    ),
    GrammarTopic(
        slug="equivalencia",
        title="Equivalência na tradução",
        level="C2",
        category="Avançado",
        summary="Princípios de equivalência tradutória.",
        explanation="A equivalência funcional preserva o efeito comunicativo, não necessariamente as mesmas palavras. Em uma expressão como Custou os olhos da cara, a tradução deve comunicar preço muito alto, sem sugerir uma lesão física. Considere também o registro, o público e o contexto cultural; às vezes uma paráfrase é mais adequada do que outra expressão idiomática.",
        rules=[
            "Equivalência funcional.",
            "Evitar calques.",
        ],
        examples=[
            GrammarExample(
                text="Custou os olhos da cara.",
                translation="It cost an arm and a leg.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Interpretar estar com a pulga atrás da orelha como uma descrição de um inseto, em um contexto de desconfiança.",
                correct="Preservar o sentido de estar desconfiado ao traduzir ou parafrasear.",
                note="Uma expressão figurada exige interpretação contextual; a tradução literal nem sempre preserva o sentido.",
            ),
        ],
        related=[
            "falsos-amigos",
            "matizes-traducao",
        ],
    ),
    GrammarTopic(
        slug="matizes-traducao",
        title="Matizes de tradução",
        level="C2",
        category="Avançado",
        summary="Nuances que distinguem uma boa tradução.",
        explanation="Uma boa tradução preserva registro, relações temporais e conotações relevantes. Não existe correspondência automática entre tempos verbais de línguas diferentes. Saudade também pode ser traduzida, mas a solução varia conforme se refere a uma pessoa, a um lugar ou a uma experiência; evite declarar uma palavra universalmente intraduzível.",
        rules=[
            "Registro e formalidade.",
            "O perfeito composto português normalmente indica repetição ou continuidade; não corresponde a todo uso do perfeito inglês.",
            "Conotações culturais.",
        ],
        examples=[
            GrammarExample(
                text="Tenho pensado nisso ultimamente.",
                translation="I have been thinking about that lately.",
            ),
            GrammarExample(
                text="Estou com saudade de você.",
                translation="I miss you.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Tenho comido ontem.",
                correct="Comi ontem.",
                note="Ação única: pretérito simples.",
            ),
        ],
        related=[
            "equivalencia",
            "falsos-amigos",
        ],
    ),
    GrammarTopic(
        slug="falsos-amigos",
        title="Falsos amigos",
        level="C2",
        category="Avançado",
        summary="Palavras portuguesas que parecem inglesas.",
        explanation="Atualmente indica o momento presente, não uma correção equivalente a na verdade. Pretender significa ter a intenção de fazer algo, não fingir. Compromisso pode designar uma obrigação ou encontro, mas também um acordo entre partes; a tradução depende do contexto e pode corresponder a compromise nesse último sentido.",
        rules=[
            "Atualmente indica o momento presente; não substitui automaticamente na verdade.",
            "Compromisso pode ser uma obrigação, um encontro marcado ou um acordo; o contexto decide a tradução.",
            "Pretender expressa intenção; fingir expressa simulação.",
        ],
        examples=[
            GrammarExample(
                text="Atualmente moro em São Paulo.",
                translation="I currently live in São Paulo.",
            ),
            GrammarExample(
                text="Tenho um compromisso às três.",
                translation="I have an appointment at three.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Usar atualmente para corrigir uma informação, apenas porque se parece com a palavra inglesa actually.",
                correct="Para corrigir a informação, use na verdade; atualmente indica tempo presente.",
                note="A semelhança de forma não garante equivalência de sentido.",
            ),
        ],
        related=[
            "equivalencia",
            "matizes-traducao",
        ],
    ),
    GrammarTopic(
        slug="evolucao-linguistica",
        title="Evolução linguística",
        level="C2",
        category="Avançado",
        summary="Como a língua portuguesa evoluiu do latim.",
        explanation="O português se formou a partir de variedades do latim falado na Península Ibérica, passando por uma fase galego-portuguesa medieval e por processos posteriores de diferenciação. As divisões em períodos são convenções de estudo, não rupturas instantâneas. Populu -> povo ilustra mudanças consonantais; plenu -> cheio envolve palatalização e outras mudanças; manu -> mão envolve perda de consoante e nasalização. No Brasil, a história da língua inclui colonização, contato com línguas indígenas e africanas, migrações e escolarização. Mudança linguística não equivale a deterioração.",
        rules=[
            "Latim vulgar > Galego-português > Moderno.",
            "Queda de consoantes, palatalização, nasalização.",
        ],
        examples=[
            GrammarExample(
                text="Latim: populu -> Português: povo",
            ),
            GrammarExample(
                text="Latim: plenu -> Português: cheio",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Confundir evolução com corrupção.",
                correct="Mudança linguística é natural.",
                note="",
            ),
        ],
        related=[
            "latinismos",
            "arabismos-portugueses",
        ],
    ),
    GrammarTopic(
        slug="latinismos",
        title="Latinismos",
        level="C2",
        category="Avançado",
        summary="Expressões e palavras latinas no português.",
        explanation="Latinismos preservam formas e sentidos do latim em registros especializados. A priori indica uma consideração anterior à experiência; a posteriori, baseada na experiência. Ad hoc qualifica algo feito para um fim específico; ipso facto significa pelo próprio fato; per capita, por pessoa; sine qua non indica condição indispensável; grosso modo, aproximadamente; lato sensu, em sentido amplo. Use-os quando forem compreensíveis ao público e mantenha sua grafia, sem adaptar facto para fato dentro da expressão latina ipso facto.",
        rules=[
            "Comuns no registro formal.",
            "Usar com precisão.",
        ],
        examples=[
            GrammarExample(
                text="A segurança é uma condição sine qua non.",
            ),
            GrammarExample(
                text="Grosso modo, a proposta é aceitável.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="À posteriori.",
                correct="A posteriori.",
                note="A é preposição latina, não leva crase.",
            ),
        ],
        related=[
            "evolucao-linguistica",
            "arabismos-portugueses",
            "registo-formal",
        ],
    ),
    GrammarTopic(
        slug="arabismos-portugueses",
        title="Arabismos portugueses",
        level="C2",
        category="Avançado",
        summary="A herança árabe no léxico português.",
        explanation="O português incorporou palavras de origem árabe em diferentes épocas e por diferentes caminhos. Azeite, arroz, açúcar e aldeia mostram a presença desse contato no cotidiano; álgebra e algoritmo, no vocabulário científico. Em muitos arabismos, o antigo artigo árabe al- foi incorporado à palavra, às vezes com assimilação sonora. Nem toda palavra iniciada por al- é árabe, e nem todo arabismo entrou diretamente durante a presença islâmica na Península Ibérica; confirme a etimologia de cada termo.",
        rules=[
            "Diferencie origem etimológica e caminho de transmissão.",
            "Al- pode refletir o artigo árabe, mas a sequência inicial não prova a origem.",
            "Alimentos, ciência, arquitetura.",
        ],
        examples=[
            GrammarExample(
                text="azeite (az-zayt)",
            ),
            GrammarExample(
                text="arroz (ar-ruzz)",
            ),
            GrammarExample(
                text="álgebra (al-jabr)",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Toda palavra portuguesa começada por al- tem origem árabe.",
                correct="A origem árabe precisa ser confirmada por evidência etimológica, não apenas pelas letras iniciais.",
                note="Semelhança de forma não basta para estabelecer a história de uma palavra.",
            ),
        ],
        related=[
            "evolucao-linguistica",
            "latinismos",
        ],
    ),
    GrammarTopic(
        slug="generos-textuais",
        title="Gêneros textuais",
        level="C2",
        category="Avançado",
        summary="Domínio de todos os gêneros textuais.",
        explanation="O gênero orienta a finalidade, a estrutura e a relação com o leitor. Um relatório apresenta procedimentos, resultados e limites; um artigo de opinião sustenta uma posição; um editorial expressa uma posição institucional; uma carta formal identifica destinatário e propósito. Um ensaio pode explorar uma questão sem seguir a estrutura de um relatório. As convenções variam por área e instituição. Ao reescrever o mesmo conteúdo para outro gênero, ajuste organização e registro sem transformar hipótese em resultado nem opinião em fato.",
        rules=[
            "Cada gênero tem convenções.",
            "Conhecer o gênero orienta escolhas.",
        ],
        examples=[
            GrammarExample(
                text="O presente relatório apresenta os resultados do inquérito.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Como o texto é um relatório, toda conclusão nele apresentada é um fato comprovado.",
                correct="Um relatório também pode apresentar hipóteses e limitações, que devem ser identificadas como tais.",
                note="O gênero não garante o estatuto factual de cada afirmação.",
            ),
        ],
        related=[
            "registo-formal",
            "estrutura-argumentativa",
        ],
    ),
    GrammarTopic(
        slug="criatividade-linguistica",
        title="Criatividade linguística",
        level="C2",
        category="Avançado",
        summary="Brincar com a língua: neologismos, trocadilhos.",
        explanation="A criatividade pode combinar bases, explorar sentidos ou adaptar empréstimos. Portunhol funde partes de português e espanhol; googlar adapta um nome de marca à morfologia verbal; um trocadilho aproxima formas ou sentidos para criar efeito. Futebol é um empréstimo historicamente adaptado, não uma palavra nova no uso atual. A novidade depende da época, do grupo e do sentido empregado. Em textos formais, defina criações que o leitor não possa interpretar pelo contexto.",
        rules=[
            "Neologismos, amálgamas, trocadilhos.",
        ],
        examples=[
            GrammarExample(
                text="Vou googlar esse termo. (neologismo)",
            ),
            GrammarExample(
                text="Não é só ver, é prever! (trocadilho)",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Futebol é necessariamente um neologismo atual porque veio do inglês.",
                correct="Futebol é um empréstimo consolidado; ser neologismo depende de novidade de forma ou sentido em um contexto histórico.",
                note="Origem estrangeira e novidade são critérios diferentes.",
            ),
        ],
        related=[
            "derivacao",
            "expressoes-coloquiais",
            "expressao-matizada",
        ],
    ),
    GrammarTopic(
        slug="edicao",
        title="Edição e revisão de textos",
        level="C2",
        category="Avançado",
        summary="Técnicas de edição para clareza e elegância.",
        explanation="Revise em camadas: primeiro a coerência dos fatos e argumentos; depois a organização e o registro; por fim, concordância, ortografia e tipografia. Leia comparando o original com a versão editada: a retirada de apenas, talvez ou desde que pode mudar alcance, certeza ou condição. Elimine ambiguidades quando necessário, mas não atribua um referente sem evidência. A leitura em voz alta ajuda a perceber ritmo e construções difíceis; não substitui a conferência de dados e fontes.",
        rules=[
            "Conteúdo, estilo, gramática, tipografia.",
        ],
        examples=[
            GrammarExample(
                text="Revisar: Apenas dois grupos talvez concluam o estudo -> É possível que somente dois grupos concluam o estudo.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Original: A maioria dos participantes respondeu. Revisão: Todos os participantes responderam.",
                correct="A maioria dos participantes respondeu.",
                note="Trocar maioria por todos altera a informação; uma edição não pode ampliar a quantidade por conveniência estilística.",
            ),
        ],
        related=[
            "reformulacao",
            "coesao-textual",
            "expressao-matizada",
        ],
    ),
    GrammarTopic(
        slug="expressao-matizada",
        title="Expressão matizada",
        level="C2",
        category="Avançado",
        summary="Arte de matizar o discurso.",
        explanation="A expressão matizada diferencia certeza, probabilidade, alcance e atitude interpessoal. Tudo indica que sugere apoio forte sem equivaler a prova definitiva; não se pode excluir admite uma possibilidade sem a declarar provável; em parte limita o alcance de uma avaliação. Gostaria de e poderia podem atenuar pedidos, não apenas localizar fatos no passado. Escolha a formulação pelo compromisso que os dados permitem e preserve essas diferenças ao resumir ou traduzir.",
        rules=[
            "Certeza, probabilidade, incerteza, cortesia.",
        ],
        examples=[
            GrammarExample(
                text="É indubitável que a medida trouxe benefícios.",
            ),
            GrammarExample(
                text="Diria que a situação é complexa.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Não se pode excluir essa hipótese significa que ela é a mais provável.",
                correct="Não se pode excluir essa hipótese mantém uma possibilidade em aberto, sem classificá-la como a mais provável.",
                note="Possibilidade, probabilidade e certeza correspondem a compromissos diferentes.",
            ),
        ],
        related=[
            "matizadores",
            "recursos-retoricos",
            "critica-construtiva",
        ],
    ),
    GrammarTopic(
        slug="integracao-gramatical",
        title="Integração gramatical",
        level="C2",
        category="Avançado",
        summary="Síntese de todos os conhecimentos gramaticais.",
        explanation="Integrar recursos gramaticais exige coordenar tempo, referência, modo e registro. Em Se eu tivesse sabido que seria tão difícil, teria me preparado melhor, a condição não realizada é passada, seria projeta uma dificuldade a partir desse passado e a consequência é contrafactual. Ter-me-ia preparado é uma alternativa marcada da escrita formal, não uma melhoria obrigatória. Ao reformular, mantenha o sujeito, a anterioridade e o caráter hipotético; a correção de uma forma isolada não compensa uma mudança de sentido.",
        rules=[
            "Subjuntivo/indicativo.",
            "Ênclise/próclise/mesóclise.",
            "Concordância.",
            "Registro contextualizado.",
        ],
        examples=[
            GrammarExample(
                text="Se eu tivesse sabido que seria tão difícil, teria me preparado melhor.",
                note="condição passada, posterioridade em relação ao passado e colocação pronominal corrente no Brasil",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se eu tivesse sabido que seria tão difícil, teria me preparar melhor.",
                correct="Se eu tivesse sabido que seria tão difícil, teria me preparado melhor.",
                note="A forma composta exige particípio; a revisão preserva as relações temporais e o participante.",
            ),
        ],
        related=[
            "revisao-conjuntivo",
            "revisao-condicional",
            "expressao-matizada",
        ],
    ),
    GrammarTopic(
        slug="fluencia-nativa",
        title="Fluência e autonomia avançadas",
        level="C2",
        category="Avançado",
        summary="Comunicar com precisão, flexibilidade e autonomia em situações complexas.",
        explanation="C2 implica compreender sentidos implícitos, reformular com precisão e adaptar o registro a contextos exigentes. Não exige perder o sotaque nem tornar-se indistinguível de um falante nativo. A inteligibilidade, a adequação e a autonomia são mais relevantes do que imitar uma identidade linguística.",
        rules=[
            "Expressão espontânea.",
            "Domínio cultural.",
            "Entoação brasileira.",
            "Flexibilidade de registros.",
        ],
        examples=[
            GrammarExample(
                text="Posso reformular a conclusão sem eliminar a ressalva feita pela autora.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Uma pessoa só atinge C2 se não tiver sotaque estrangeiro.",
                correct="C2 envolve precisão, flexibilidade e compreensão de sentidos implícitos; não exige eliminar o sotaque.",
                note="Avalie a eficácia comunicativa em tarefas complexas, não a imitação de uma identidade nativa.",
            ),
        ],
        related=[
            "integracao-gramatical",
            "expressao-matizada",
        ],
    ),
    GrammarTopic(
        slug="tupinismos",
        title="Tupinismos — palavras de origem tupi-guarani",
        level="C2",
        category="Avançado",
        summary="Reconhecer e compreender os tupinismos integrados no português brasileiro.",
        explanation="Os **tupinismos** são palavras de origem tupi incorporadas ao português através do contato linguístico no Brasil. Muitas designam fauna, flora, alimentos e lugares.\n\nExemplos: tatu, piranha, capivara, arara, tucano; abacaxi, mandioca, caju; pipoca, tapioca; Ipanema, Paraná e Iguaçu. Nem todas as palavras indígenas nem todos os topônimos brasileiros têm origem tupi: cada etimologia deve ser verificada.",
        rules=[
            "Tupinismos designam majoritariamente fauna, flora e topônimos brasileiros.",
            "Alguns termos designam realidades locais; outros circulam também em Portugal, como abacaxi e mandioca.",
            "São parte integrante do vocabulário ativo brasileiro.",
            "Reconhecer a origem tupi demonstra conhecimento avançado da cultura e história da língua.",
        ],
        examples=[
            GrammarExample(
                text="Vou comer um abacaxi com tapioca.",
            ),
            GrammarExample(
                text="O tucano e a arara são aves típicas do Brasil.",
            ),
            GrammarExample(
                text="A capivara é o maior roedor do mundo.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Afirmar que abacaxi nunca se usa em Portugal.",
                correct="Abacaxi e ananás usam-se em Portugal; as preferências e distinções comerciais variam.",
                note="Não reduzir os usos a uma oposição absoluta entre países.",
            ),
            GrammarMistake(
                wrong="Confundir mandioca com batata-doce.",
                correct="Mandioca (ou aipim/macaxeira) é uma raiz diferente, da qual se faz farinha e tapioca.",
                note="Distinção botânica.",
            ),
        ],
        related=[
            "arabismos-portugueses",
            "evolucao-linguistica",
            "portugues-brasileiro",
        ],
    ),
    GrammarTopic(
        slug="lusofonia-contemporanea",
        title="A Lusofonia contemporânea",
        level="C2",
        category="Expressão",
        summary="Instituições, diversidade e desafios da comunidade lusófona no século XXI.",
        explanation="A **lusofonia** abrange comunidades ligadas pelo uso do português, com histórias, variedades e situações de multilinguismo distintas. Não se confunde com uma organização única.\n\nA **CPLP**, Comunidade dos Países de Língua Portuguesa, é uma organização intergovernamental de cooperação. O **IILP** promove a língua no âmbito dessa comunidade.\n\nO Brasil concentra a maior parte dos falantes de português. Países africanos como Angola e Moçambique têm um papel importante no seu crescimento demográfico. A presença oficial do português não implica que seja a língua materna ou majoritária de toda a população.\n\nOs debates incluem diversidade normativa, educação multilíngue, circulação cultural e acesso à ciência.",
        rules=[
            "A Lusofonia não é um bloco monolítico — cada país tem a sua variedade e política linguística.",
            "O Brasil concentra a maioria dos falantes; o crescimento africano não elimina as diferenças de uso entre países.",
            "A CPLP promove o plurilinguismo e a diversidade cultural, não o monolinguismo português.",
        ],
        examples=[
            GrammarExample(
                text="Em Angola, expressões como 'maka' (conflito, confusão) ou 'bué' (muito) enriquecem o português local com influências das línguas bantu.",
                note="português angolano",
            ),
            GrammarExample(
                text="O VOLP (Vocabulário Ortográfico da Língua Portuguesa), da Academia Brasileira de Letras, é uma referência para a grafia brasileira.",
            ),
            GrammarExample(
                text="Uma projeção sobre falantes deve indicar a fonte, a data e se conta língua materna, segunda língua ou ambas.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Lusofonia e CPLP são a mesma organização.",
                correct="Lusofonia designa um espaço linguístico e cultural; a CPLP é uma organização intergovernamental.",
                note="As comunidades lusófonas incluem também diásporas e não se limitam à pertença institucional à CPLP.",
            ),
        ],
        related=[
            "politica-linguistica-pt",
            "evolucao-linguistica",
        ],
    ),
    GrammarTopic(
        slug="politica-linguistica-pt",
        title="Política linguística no mundo lusófono",
        level="C2",
        category="Expressão",
        summary="Do Acordo Ortográfico à difusão do português: políticas e tensões linguísticas nos países de língua portuguesa.",
        explanation="As políticas linguísticas são definidas por instituições nacionais e por mecanismos de cooperação. As academias publicam obras lexicográficas e estudos; não controlam sozinhas todos os usos ou decisões educativas. O IILP promove a cooperação no âmbito da CPLP.\n\nO **Acordo Ortográfico de 1990** procura aproximar a escrita; a adoção e aplicação variam entre países. Não uniformiza pronúncia, gramática ou vocabulário.\n\nO português é pluricêntrico: as variedades europeia, brasileira e africanas têm usos próprios. As diferenças de colocação pronominal dependem também do registro: Me dá é comum na fala brasileira, mas não resume a norma escrita formal.\n\nA educação em contextos multilíngues deve considerar o português e as outras línguas das comunidades.",
        rules=[
            "O Acordo Ortográfico é um tratado internacional, não uma imposição — cada país decide a sua aplicação.",
            "O português é uma língua pluricêntrica: PE e PB são normas de igual legitimidade.",
            "As variedades africanas estão se afirmando como normas com trajetórias e traços próprios.",
        ],
        examples=[
            GrammarExample(
                text="Na conversa, 'Dá-me o livro' é frequente em Portugal e 'Me dá o livro' é frequente no Brasil; o registro e a região também influenciam a escolha.",
                note="Tendências de colocação pronominal na fala, sem equiparar conversa e norma escrita formal.",
            ),
            GrammarExample(
                text="O Acordo Ortográfico eliminou as consoantes mudas em Portugal: 'acção' passou a 'ação', 'óptimo' passou a 'ótimo'.",
                note="AO90",
            ),
            GrammarExample(
                text="Machimbombo pode designar ônibus em Moçambique; em Angola, candongueiro designa um transporte coletivo informal, geralmente em minibus.",
                note="Vocabulário de países diferentes; não há uma única variedade africana.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A Academia das Ciências de Lisboa dita as regras do português em todos os países lusófonos.",
                correct="Instituições como a ACL e a ABL publicam obras de referência; políticas linguísticas também envolvem governos, escolas e comunidades.",
                note="Distinguir norma europeia de norma internacional.",
            ),
        ],
        related=[
            "lusofonia-contemporanea",
            "evolucao-linguistica",
        ],
    ),
    GrammarTopic(
        slug="evolucao-digital-pt",
        title="O português na era digital",
        level="C2",
        category="Expressão",
        summary="Como o português evolui com o digital: redes sociais, IA, anglicismos e novos usos linguísticos.",
        explanation="A comunicação digital cria abreviaturas como vc (você), tb (também), msg (mensagem), bjs (beijos) e obg (obrigado). Essas formas podem funcionar em mensagens informais, mas precisam ser expandidas quando o gênero exigir escrita formal.\n\nEmojis e sinais de pontuação ajudam a expressar atitude, sem garantir uma interpretação única. Hashtags organizam temas, como #Brasil e #LiteraturaBrasileira.\n\nNeologismos como postar e clicar convivem com empréstimos como streaming e podcast. A escolha entre baixar um arquivo e fazer um download depende do público e do contexto.\n\nAssistentes de inteligência artificial e tradução automática podem reproduzir vieses e deixar variedades regionais pouco representadas. Avalie seus resultados pelo sentido, pela variedade-alvo e pela adequação ao registro, sem tratar inovação linguística como degradação automática.",
        rules=[
            "O português digital não é uma versão 'degradada' da língua — é um registro adaptado ao meio e ao contexto.",
            "Os anglicismos na tecnologia são frequentes, mas o português também cria alternativas (baixar, carregar, e-mail).",
            "A IA e a tradução automática levantam questões de soberania linguística e representatividade das variedades do português.",
        ],
        examples=[
            GrammarExample(
                text="obg pela msg, depois falamos :) bjs!",
                note="linguagem SMS no português brasileiro",
            ),
            GrammarExample(
                text="Vou googlar esse termo e depois faço o download do arquivo.",
                note="mistura de neologismo e anglicismo",
            ),
            GrammarExample(
                text="Os modelos de IA generativa ainda produzem um português com forte viés brasileiro, o que levanta questões sobre a representatividade das variedades europeia e africanas.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A linguagem das redes sociais é 'mau português'.",
                correct="Cada contexto comunicativo exige um registro adequado — a linguagem digital é funcional e criativa no seu meio, não sendo inferior ao registro formal.",
                note="Evitar preconceitos linguísticos sobre variedades e registros.",
            ),
        ],
        related=[
            "lusofonia-contemporanea",
            "criatividade-linguistica",
        ],
    ),
]
