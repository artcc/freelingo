"""Brazilian Portuguese (grammar_a2) learning content."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="preterito-perfeito-regular",
        title="Pretérito perfeito simples (regulares)",
        level="A2",
        category="Tempos verbais",
        summary="Conjugação do pretérito perfeito para verbos regulares em -ar, -er, -ir.",
        explanation="| | fal**ar** | com**er** | abr**ir** |\n|---|-----------|-----------|----------|\n| eu | falei | comi | abri |\n| tu | falaste | comeste | abriste |\n| ele/você | falou | comeu | abriu |\n| nós | falamos | comemos | abrimos |\n| eles/vocês | falaram | comeram | abriram |",
        rules=[
            "-ar: -ei, -aste, -ou, -amos, -aram.",
            "-er: -i, -este, -eu, -emos, -eram.",
            "-ir: -i, -iste, -iu, -imos, -iram.",
            "Ação concluída e pontual no passado.",
            "A forma nós é igual no presente e pretérito para -ar.",
        ],
        examples=[
            GrammarExample(
                text="Ontem falei com a Maria.",
            ),
            GrammarExample(
                text="Ela comeu tudo.",
            ),
            GrammarExample(
                text="Nós abrimos a loja às oito.",
            ),
            GrammarExample(
                text="Eles venderam a casa no ano passado.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ontem eu falo com ela.",
                correct="Ontem eu falei com ela.",
                note="Para apresentar a ação como concluída, use falei. Ontem não exige sempre o perfeito: Ontem eu falava com ela quando você chegou também é válido.",
            ),
            GrammarMistake(
                wrong="Nós falemos.",
                correct="Nós falamos.",
                note="Falemos é subjuntivo/imperativo, não pretérito.",
            ),
        ],
        related=[
            "marcadores-temporais",
            "preterito-imperfeito",
            "perfeito-vs-imperfeito",
        ],
    ),
    GrammarTopic(
        slug="marcadores-temporais",
        title="Marcadores temporais",
        level="A2",
        category="Adjetivos e advérbios",
        summary="Palavras e expressões que situam ações no tempo.",
        explanation="Os marcadores situam acontecimentos no tempo, mas não escolhem sozinhos o tempo verbal. Ontem, anteontem, na semana passada e há dois dias remetem ao passado: Ontem chovia quando saí combina imperfeito e perfeito. Há também pode indicar uma duração que continua no presente: Moro aqui há dois anos.\n\nAntigamente e quando era criança aparecem frequentemente em descrições e hábitos passados. Todos os dias, sempre e frequentemente indicam repetição em diferentes tempos: Estudo todos os dias; Estudava todos os dias.\n\nHoje pode acompanhar passado, presente ou futuro: Hoje trabalhei cedo; Hoje estou em casa; Hoje vou sair. Amanhã e daqui a dois dias situam eventos futuros, que também podem ser expressos pelo presente: Amanhã viajo. Já, ainda não e nunca relacionam a ação a uma expectativa ou experiência: Já sei; Ainda não terminei; Nunca tinha visto isso.",
        rules=[
            "Ontem situa a ação no passado; perfeito e imperfeito apresentam perspectivas diferentes sobre ela.",
            "Há + tempo pode localizar um fato passado ou indicar duração até o presente: Cheguei há dois anos; Moro aqui há dois anos.",
            "Marcadores de frequência não determinam o tempo verbal: Viajo sempre; Viajava sempre.",
            "Já, ainda não e nunca combinam com diferentes tempos conforme a referência e o sentido.",
        ],
        examples=[
            GrammarExample(
                text="Ontem fui ao cinema.",
            ),
            GrammarExample(
                text="Já leste o livro?",
            ),
            GrammarExample(
                text="Ainda não terminei o trabalho.",
            ),
            GrammarExample(
                text="Quando era criança, brincava na rua.",
                note="imperfeito",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ontem eu vou ao cinema.",
                correct="Ontem eu fui ao cinema.",
                note="Ontem requer passado.",
            ),
        ],
        related=[
            "preterito-perfeito-regular",
            "preterito-imperfeito",
            "perfeito-vs-imperfeito",
        ],
    ),
    GrammarTopic(
        slug="preterito-perfeito-irregular",
        title="Pretérito perfeito (irregulares)",
        level="A2",
        category="Tempos verbais",
        summary="Verbos irregulares mais comuns no pretérito perfeito.",
        explanation="**Ser/Ir** (idênticos): fui, foste, foi, fomos, foram\n**Estar**: estive, estiveste, esteve, estivemos, estiveram\n**Ter**: tive, tiveste, teve, tivemos, tiveram\n**Fazer**: fiz, fizeste, fez, fizemos, fizeram\n**Querer**: quis, quiseste, quis, quisemos, quiseram\n**Poder**: pude, pudeste, pôde, pudemos, puderam\n**Saber**: soube, soubeste, soube, soubemos, souberam\n**Dar**: dei, deste, deu, demos, deram\n**Ver**: vi, viste, viu, vimos, viram\n**Vir**: vim, vieste, veio, viemos, vieram",
        rules=[
            "Ser e Ir são idênticos no pretérito perfeito.",
            "Muitos irregulares têm raiz diferente.",
            "A 3.ª pl. termina em -ram.",
            "Memorizar estes verbos: são de uso diário.",
        ],
        examples=[
            GrammarExample(
                text="Eu fui ao médico ontem.",
                note="ir",
            ),
            GrammarExample(
                text="A festa foi ótima.",
                note="ser",
            ),
            GrammarExample(
                text="Ela teve uma ideia brilhante.",
            ),
            GrammarExample(
                text="Nós fizemos o jantar.",
            ),
            GrammarExample(
                text="Eles vieram cedo.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eu fazi o trabalho.",
                correct="Eu fiz o trabalho.",
                note="Fazer no pretérito: fiz, fizeste, fez...",
            ),
        ],
        related=[
            "preterito-perfeito-regular",
            "marcadores-temporais",
            "perfeito-vs-imperfeito",
        ],
    ),
    GrammarTopic(
        slug="preterito-imperfeito",
        title="Pretérito imperfeito",
        level="A2",
        category="Tempos verbais",
        summary="Descrever ações habituais, contínuas ou descritivas no passado.",
        explanation="| | fal**ar** | com**er** | abr**ir** |\n|---|-----------|-----------|----------|\n| eu | falava | comia | abria |\n| tu | falavas | comias | abrias |\n| ele | falava | comia | abria |\n| nós | falávamos | comíamos | abríamos |\n| eles | falavam | comiam | abriam |\n\nIrregulares (poucos!): ser (era), ter (tinha), vir (vinha), pôr (punha).",
        rules=[
            "-ar: -ava; -er/-ir: -ia.",
            "Usa-se para hábitos passados, descrições e ações de fundo.",
            "Só quatro irregulares: ser, ter, vir, pôr.",
            "Imperfeito = cenário; perfeito = ação pontual.",
        ],
        examples=[
            GrammarExample(
                text="Quando era pequeno, morava no Porto.",
            ),
            GrammarExample(
                text="Ela cantava muito bem.",
            ),
            GrammarExample(
                text="Estava chovendo quando saí de casa.",
            ),
            GrammarExample(
                text="Eram cinco da tarde.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando nós era crianças, brincava na rua.",
                correct="Quando nós éramos crianças, brincávamos na rua.",
                note="Nós exige plural. Brinquei pode resumir uma experiência concluída; brincava apresenta o hábito sem delimitar seu fim.",
            ),
        ],
        related=[
            "perfeito-vs-imperfeito",
            "costumava",
            "marcadores-temporais",
        ],
    ),
    GrammarTopic(
        slug="perfeito-vs-imperfeito",
        title="Perfeito vs imperfeito",
        level="A2",
        category="Tempos verbais",
        summary="Quando usar o pretérito perfeito e quando usar o pretérito imperfeito.",
        explanation="O perfeito apresenta a situação como um todo delimitado: Ontem fui ao cinema; Morei lá por dez anos. O imperfeito apresenta uma situação em curso, um cenário ou um hábito sem destacar seus limites: Chovia quando saí; Quando era criança, ia ao cinema.\n\nA duração real não determina o tempo: uma situação longa pode usar perfeito. Marcadores como ontem também não escolhem o tempo sozinhos: Ontem choveu muito e Ontem chovia quando saí são válidos.",
        rules=[
            "Perfeito: ação concluída, contada como fato.",
            "Imperfeito: cenário, hábito, descrição.",
            "Escolha o tempo conforme a perspectiva e os limites da situação, não só pelo marcador temporal.",
            "Hábitos podem ser apresentados pelo imperfeito ou resumidos como um período concluído pelo perfeito.",
            "Imperfeito pinta o fundo; perfeito avança a história.",
        ],
        examples=[
            GrammarExample(
                text="Estava dormindo quando o despertador tocou.",
                note="imperfeito + perfeito",
            ),
            GrammarExample(
                text="Quando vivia em Lisboa, ia à praia todos os fins de semana.",
            ),
            GrammarExample(
                text="Ontem comi bacalhau.",
                note="perfeito",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando eu chegou, ela estava lendo.",
                correct="Quando eu cheguei, ela estava lendo.",
                note="Cheguei concorda com eu; o perfeito apresenta a chegada e o imperfeito a leitura em curso.",
            ),
        ],
        related=[
            "preterito-perfeito-regular",
            "preterito-imperfeito",
            "costumava",
        ],
    ),
    GrammarTopic(
        slug="costumava",
        title="Costumar (hábitos passados)",
        level="A2",
        category="Tempos verbais",
        summary="Expressar hábitos passados com costumar + infinitivo.",
        explanation="Costumar no imperfeito + infinitivo apresenta um hábito passado: Eu costumava ir à praia; Nós costumávamos jantar fora. O contexto informa se o hábito terminou ou se apenas se fala de um período anterior. No presente, costumo indica hábito atual.",
        rules=[
            "Costumar no imperfeito + infinitivo = hábitos passados.",
            "Apresenta um hábito passado; seu término depende do contexto.",
            "Alternativa: usar diretamente o imperfeito.",
            "Costumar no presente = hábito atual.",
        ],
        examples=[
            GrammarExample(
                text="Costumava acordar cedo.",
            ),
            GrammarExample(
                text="Ela costumava cantar no coro.",
            ),
            GrammarExample(
                text="Costumávamos jantar fora às sextas.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Nós costumava ir à praia.",
                correct="Nós costumávamos ir à praia.",
                note="O verbo concorda com nós. O perfeito de costumar existe, embora o imperfeito seja o modelo usual para hábitos passados.",
            ),
        ],
        related=[
            "preterito-imperfeito",
            "perfeito-vs-imperfeito",
            "marcadores-temporais",
        ],
    ),
    GrammarTopic(
        slug="pronomes-objeto-direto",
        title="Pronomes de objeto direto",
        level="A2",
        category="Pronomes",
        summary="Retomar o objeto com formas adequadas ao registro.",
        explanation="O, a, os e as retomam objetos diretos na escrita formal: Vi o filme → Eu o vi. Com infinitivo terminado em -r, use -lo/-la e ajuste a grafia: ver + o → vê-lo; comprar + a → comprá-la. Me, te e nos também podem ser objetos diretos.\n\nNa conversa brasileira, são comuns a repetição do nome, a omissão recuperável e formas como Vi ele. A escrita formal tradicional prefere Eu o vi ou Vi-o. Não confunda descrição do uso com recomendação para todo registro.",
        rules=[
            "O pronome concorda com o referente: o livro → o; as cartas → as.",
            "Diferencie o/a de lhe, normalmente indireto no padrão formal.",
            "Observe as alterações com infinitivos: fazer → fazê-lo.",
        ],
        examples=[
            GrammarExample(
                text="Eu a encontrei ontem.",
            ),
            GrammarExample(
                text="Você me viu?",
            ),
            GrammarExample(
                text="Vou comprá-lo amanhã.",
            ),
            GrammarExample(
                text="Não os conheço.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Vou comprar-o.",
                correct="Vou comprá-lo.",
                note="O infinitivo perde r e recebe -lo.",
            ),
            GrammarMistake(
                wrong="As cartas? Eu o li.",
                correct="As cartas? Eu as li.",
                note="As retoma cartas, feminino plural.",
            ),
        ],
        related=[
            "pronomes-objeto-indireto",
            "colocacao-pronominal",
        ],
    ),
    GrammarTopic(
        slug="pronomes-objeto-indireto",
        title="Pronomes de objeto indireto",
        level="A2",
        category="Pronomes",
        summary="Indicar destinatários com me, te, lhe, nos e lhes.",
        explanation="O objeto indireto pode indicar o destinatário: Entreguei o livro à professora → Entreguei-lhe o livro. Na fala brasileira, são naturais Eu entreguei o livro para ela e Eu te mandei uma mensagem. Lhe pode retomar ele, ela ou você na escrita formal, conforme o contexto.\n\nNão substitua toda expressão preposicionada por lhe: Gosto dela, e não Gosto-lhe. A regência do verbo determina a construção.",
        rules=[
            "Me, te, nos, lhe e lhes podem indicar destinatário.",
            "Use lhes para referente plural na norma-padrão.",
            "Explicite para ele/ela/você quando isso evitar ambiguidade.",
        ],
        examples=[
            GrammarExample(
                text="Ela me deu um presente.",
            ),
            GrammarExample(
                text="Enviei-lhe o documento.",
            ),
            GrammarExample(
                text="Vou mandar a resposta para vocês.",
            ),
            GrammarExample(
                text="Não lhes contei o segredo.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gosto-lhe muito.",
                correct="Gosto muito dela.",
                note="Gostar de não admite lhe nessa substituição.",
            ),
            GrammarMistake(
                wrong="Enviei o documento aos diretores e lhe pedi uma resposta.",
                correct="Enviei o documento aos diretores e lhes pedi uma resposta.",
                note="O referente diretores é plural.",
            ),
        ],
        related=[
            "pronomes-objeto-direto",
            "colocacao-pronominal",
        ],
    ),
    GrammarTopic(
        slug="colocacao-pronominal",
        title="Colocação pronominal no português brasileiro",
        level="A2",
        category="Pronomes",
        summary="Distinguir a próclise frequente na fala das convenções formais.",
        explanation="Na conversa brasileira, é natural usar o pronome antes do verbo: Eu me lembro; Ela te chamou. Frases como Me ajuda? são comuns na oralidade. A escrita formal tradicional evita pronome átono no início absoluto: Ajude-me.\n\nNegação, relativos e outras palavras favorecem ou exigem próclise na norma-padrão: Não me diga; O livro que me deram. Ênclise é frequente com infinitivos e em textos formais: Vou ajudá-lo. A mesóclise é muito marcada e não é requisito de uma conversa natural. A escolha depende também do pronome, da construção e do registro.",
        rules=[
            "Use Não me diga, não Não diga-me, no padrão formal.",
            "Não marque Eu me lembro como erro.",
            "Reconheça Me ajuda na fala e Ajude-me na escrita formal.",
        ],
        examples=[
            GrammarExample(
                text="Eu me lembro do endereço.",
            ),
            GrammarExample(
                text="Não me conte o final.",
            ),
            GrammarExample(
                text="Ela me entregou o livro.",
            ),
            GrammarExample(
                text="Ajude-me, por favor.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Não diga-me isso.",
                correct="Não me diga isso.",
                note="A negação atrai o pronome na norma-padrão.",
            ),
            GrammarMistake(
                wrong="Ela se entregou o livro para mim.",
                correct="Ela me entregou o livro.",
                note="Me identifica o destinatário; se mudaria a relação entre os participantes.",
            ),
        ],
        related=[
            "pronomes-objeto-direto",
            "pronomes-objeto-indireto",
            "verbos-reflexivos",
        ],
    ),
    GrammarTopic(
        slug="comparativos",
        title="Comparativos",
        level="A2",
        category="Adjetivos e advérbios",
        summary="Mais... do que, menos... do que — expressar comparações.",
        explanation="**Superioridade:** mais + adjetivo + que/do que. **Inferioridade:** menos + adjetivo + que/do que. Ambas as variantes são válidas: Lisboa é mais cara que o Porto / do que o Porto. **Igualdade:** tão + adjetivo + como/quanto.\n\nComparativos irregulares: bom → melhor, mau → pior, grande → maior, pequeno → menor.",
        rules=[
            "Mais [adj] do que = superioridade.",
            "Menos [adj] do que = inferioridade.",
            "Tão [adj] como = igualdade.",
            "Bom/mau/grande/pequeno: melhor, pior, maior, menor.",
        ],
        examples=[
            GrammarExample(
                text="Lisboa é mais bonita do que Madrid.",
            ),
            GrammarExample(
                text="Este livro é melhor do que o filme.",
                note="bom→melhor",
            ),
            GrammarExample(
                text="Ela é tão inteligente como o irmão.",
            ),
            GrammarExample(
                text="Hoje está menos frio do que ontem.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É mais bom.",
                correct="É melhor.",
                note="Comparativo de bom é melhor.",
            ),
        ],
        related=[
            "superlativos",
            "tao-como",
            "adjetivos-descritivos",
        ],
    ),
    GrammarTopic(
        slug="superlativos",
        title="Superlativos",
        level="A2",
        category="Adjetivos e advérbios",
        summary="Expressar o grau máximo de uma qualidade.",
        explanation="**Relativo:** *o/a mais + adj + de*. **Absoluto sintético:** adj + -íssimo (*bonitíssimo*). **Absoluto analítico:** *muito + adj*.\n\nIrregulares: bom→ótimo, mau→péssimo, grande→máximo, pequeno→mínimo.",
        rules=[
            "Superlativo relativo: o mais + adj + de.",
            "Absoluto sintético: adj + -íssimo.",
            "Irregulares: ótimo, péssimo, máximo, mínimo.",
            "Na fala, muito + adjetivo é mais comum.",
        ],
        examples=[
            GrammarExample(
                text="Ela é a pessoa mais simpática que conheço.",
            ),
            GrammarExample(
                text="Este restaurante é ótimo.",
            ),
            GrammarExample(
                text="A torre é altíssima.",
                note="sintético",
            ),
            GrammarExample(
                text="Este é o filme menos interessante do ano.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É a mais boa.",
                correct="É a melhor.",
                note="Superlativo de bom é melhor/ótima.",
            ),
            GrammarMistake(
                wrong="Este livro é muito ótimo.",
                correct="Este livro é ótimo.",
                note="Ótimo já é superlativo.",
            ),
        ],
        related=[
            "comparativos",
            "tao-como",
            "adjetivos-descritivos",
        ],
    ),
    GrammarTopic(
        slug="tao-como",
        title="Tão... como / tanto... como",
        level="A2",
        category="Adjetivos e advérbios",
        summary="Comparativos de igualdade com tão e tanto.",
        explanation="**Tão... como** (qualidade): *É tão alto como o pai.*\n**Tanto/a/os/as... como** (quantidade): *Tenho tanto dinheiro como ele.*\n**Tanto como** (verbos): *Estudo tanto como tu.*\n**Tão... que** (consequência): *É tão caro que ninguém compra.*",
        rules=[
            "Tão + adj/adv + como = igualdade de qualidade.",
            "Tanto/a/os/as + subst + como = igualdade de quantidade.",
            "Verbo + tanto como = igualdade de ação.",
            "Tão... que = consequência.",
        ],
        examples=[
            GrammarExample(
                text="É tão inteligente como tu.",
            ),
            GrammarExample(
                text="Tenho tanto trabalho como na semana passada.",
            ),
            GrammarExample(
                text="Ela dorme tanto como eu.",
            ),
            GrammarExample(
                text="Estava tão cansada que adormeceu no sofá.",
                note="consequência",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É tão alto do que tu.",
                correct="É tão alto como tu.",
                note="Tão... como, não tão... do que.",
            ),
            GrammarMistake(
                wrong="Tenho tão dinheiro como ele.",
                correct="Tenho tanto dinheiro como ele.",
                note="Com substantivo: tanto, não tão.",
            ),
        ],
        related=[
            "comparativos",
            "superlativos",
            "adjetivos-descritivos",
        ],
    ),
    GrammarTopic(
        slug="imperativo-afirmativo",
        title="Imperativo afirmativo",
        level="A2",
        category="Verbos",
        summary="Dar instruções, fazer pedidos e adequar o tratamento.",
        explanation="Com você, a norma-padrão usa formas do presente do subjuntivo: fale, coma, abra. Com vocês: falem, comam, abram. Com tu: fala, come, abre. A fala brasileira apresenta variação entre formas do imperativo, mesmo em regiões que usam você; o contexto e a entoação também marcam cortesia.\n\nUm pedido pode usar por favor ou uma pergunta com poder: Você pode abrir a porta? Na escrita formal: Sente-se. Na conversa: Pode se sentar.",
        rules=[
            "Mantenha um tratamento coerente em instruções formais.",
            "Use por favor ou uma pergunta para suavizar pedidos.",
            "Não confunda variação oral com erro universal.",
        ],
        examples=[
            GrammarExample(
                text="Abra a porta, por favor.",
            ),
            GrammarExample(
                text="Preencham o formulário.",
            ),
            GrammarExample(
                text="Pode se sentar.",
            ),
            GrammarExample(
                text="Fale mais devagar, por favor.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Vocês, abra o livro.",
                correct="Vocês, abram o livro.",
                note="O verbo deve concordar com o plural.",
            ),
            GrammarMistake(
                wrong="Você, fazer o exercício agora.",
                correct="Você, faça o exercício agora.",
                note="O imperativo dirigido a você usa faça.",
            ),
        ],
        related=[
            "imperativo-negativo",
            "imperativo-irregular",
            "colocacao-pronominal",
        ],
    ),
    GrammarTopic(
        slug="imperativo-negativo",
        title="Imperativo negativo",
        level="A2",
        category="Verbos",
        summary="Dar ordens negativas, proibições e conselhos negativos.",
        explanation="Na norma-padrão, o imperativo negativo usa o **presente do subjuntivo**:\n- *Não fales alto!* (tu)\n- *Não fale alto!* (você)\n- *Não falemos alto!* (nós)\n- *Não falem alto!* (vocês)\n\nCom pronomes, use próclise: *Não se esqueça!* A conversa brasileira também apresenta formas como Não fala isso e Não faz isso, conforme região e situação; não confunda essa variação com as convenções de uma instrução formal.",
        rules=[
            "Na norma-padrão, o imperativo negativo usa o presente do subjuntivo.",
            "Para tu, a norma-padrão distingue fala/não fales, come/não comas e abre/não abras.",
            "Com negação, pronomes vão antes do verbo (próclise).",
            "Para você e vocês, a forma verbal coincide com a do imperativo afirmativo, mas distingue singular e plural: fale/não fale; falem/não falem.",
        ],
        examples=[
            GrammarExample(
                text="Não fales tão alto.",
                note="tu",
            ),
            GrammarExample(
                text="Não coma isso.",
                note="você",
            ),
            GrammarExample(
                text="Não se esqueçam do passaporte.",
                note="vocês + próclise",
            ),
            GrammarExample(
                text="Não me interrompas.",
                note="tu, próclise",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Não falaram alto! (como instrução a vocês)",
                correct="Não falem alto!",
                note="Falaram relata uma ação passada; falem dá a instrução. A fala brasileira também apresenta variação entre formas do imperativo.",
            ),
            GrammarMistake(
                wrong="Não esqueças-te!",
                correct="Não te esqueças!",
                note="Com negação, pronome vai antes do verbo.",
            ),
        ],
        related=[
            "imperativo-afirmativo",
            "imperativo-irregular",
            "presente-conjuntivo",
        ],
    ),
    GrammarTopic(
        slug="imperativo-irregular",
        title="Imperativo irregular",
        level="A2",
        category="Verbos",
        summary="Formas irregulares do imperativo dos verbos mais comuns.",
        explanation="Formas da norma-padrão:\n\n| Verbo | tu | você |\n|-------|-----|------|\n| dizer | diz | diga |\n| fazer | faz | faça |\n| ser | sê | seja |\n| estar | está | esteja |\n| ir | vai | vá |\n| ter | tem | tenha |\n| pôr | põe | ponha |\n| vir | vem | venha |\n| ver | vê | veja |\n\nNo negativo, a norma-padrão usa subjuntivo (*não digas, não faças*). A fala brasileira admite outras distribuições das formas conforme região e situação, inclusive com você.",
        rules=[
            "Cada verbo irregular deve ser memorizado.",
            "Para tu, em geral retire -s do presente; ser tem a forma especial sê.",
            "Você/vocês: presente do subjuntivo.",
            "No negativo, use subjuntivo quando o exercício pedir a norma-padrão.",
        ],
        examples=[
            GrammarExample(
                text="Sê simpático.",
                note="ser, tu",
            ),
            GrammarExample(
                text="Faça o favor de entrar.",
                note="fazer, você",
            ),
            GrammarExample(
                text="Põe a mesa, por favor.",
                note="pôr, tu",
            ),
            GrammarExample(
                text="Não ponhas os pés em cima da mesa.",
                note="negativo, tu",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Seje feliz!",
                correct="Seja feliz!",
                note="A forma da norma-padrão para você é seja.",
            ),
            GrammarMistake(
                wrong="Vocês, não façam-se de desentendidos! (na escrita formal)",
                correct="Vocês, não se façam de desentendidos!",
                note="A negação exige próclise na escrita formal; Não faz isso é um uso conversacional brasileiro frequente.",
            ),
        ],
        related=[
            "imperativo-afirmativo",
            "imperativo-negativo",
            "presente-conjuntivo",
        ],
    ),
    GrammarTopic(
        slug="futuro-do-presente",
        title="Futuro do presente",
        level="A2",
        category="Tempos verbais",
        summary="Expressar previsões e compromissos futuros.",
        explanation="O futuro simples acrescenta -ei, -á, -emos e -ão ao infinitivo no paradigma com eu, você, nós e vocês. Irregulares: direi, farei, trarei. Na conversa, ir + infinitivo é muito frequente: Vou estudar. O futuro simples aparece em previsões, promessas e textos formais: Enviarei o relatório.\n\nA mesóclise pertence a registros muito formais: Enviar-lhe-ei. Com negação: Não lhe enviarei. Na conversa, use Vou enviar o documento para você.",
        rules=[
            "Use fará, dirá e trará, sem o infinitivo completo.",
            "Distinga previsão, promessa e planejamento pelo contexto.",
            "Não trate a mesóclise como padrão obrigatório de conversa.",
        ],
        examples=[
            GrammarExample(
                text="A reunião será amanhã.",
            ),
            GrammarExample(
                text="Nós faremos a inscrição.",
            ),
            GrammarExample(
                text="Vou enviar o documento.",
            ),
            GrammarExample(
                text="Eles chegarão à noite.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eu fazerei a inscrição.",
                correct="Eu farei a inscrição.",
                note="Fazer tem radical irregular no futuro.",
            ),
            GrammarMistake(
                wrong="Vocês chegará amanhã.",
                correct="Vocês chegarão amanhã.",
                note="Vocês exige plural.",
            ),
        ],
        related=[
            "ir-futuro",
            "condicional",
            "futuro-composto",
            "futuro-do-conjuntivo",
        ],
    ),
    GrammarTopic(
        slug="condicional",
        title="Condicional simples",
        level="A2",
        category="Condicionais",
        summary="Expressar hipóteses, desejos, pedidos cordiais e ações condicionadas.",
        explanation="Infinitivo + -ia, -ias, -ia, -íamos, -iam. Irregulares: dizer→diria, fazer→faria, trazer→traria.\n\nUsos: hipóteses, desejos, pedidos cordiais, condicionais com se, futuro do pretérito.",
        rules=[
            "Infinitivo + -ia, -ias, -ia, -íamos, -iam.",
            "Mesmos irregulares do futuro.",
            "Pedidos cordiais e hipóteses.",
            "Mesóclise (formal): dar-te-ia.",
        ],
        examples=[
            GrammarExample(
                text="Gostaria de um café, por favor.",
                note="pedido cordial",
            ),
            GrammarExample(
                text="Se tivesse dinheiro, viajaria pelo mundo.",
            ),
            GrammarExample(
                text="Ele disse que chegaria às três.",
            ),
            GrammarExample(
                text="Poderia ajudar-me?",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se eu tivesse dinheiro, viajariam pelo mundo. (sujeito: eu)",
                correct="Se tivesse dinheiro, viajaria pelo mundo.",
                note="O futuro do pretérito concorda com eu. Viajava também pode expressar a consequência na conversa.",
            ),
            GrammarMistake(
                wrong="Eu gostariam de um café.",
                correct="Eu gostaria de um café.",
                note="Gostaria concorda com eu. Gostava pode ter outros usos válidos conforme a variedade e o contexto.",
            ),
        ],
        related=[
            "futuro-do-presente",
            "condicional-composto",
            "se-imperfeito-subjuntivo",
        ],
    ),
    GrammarTopic(
        slug="futuro-composto",
        title="Futuro composto",
        level="A2",
        category="Tempos verbais",
        summary="Expressar ações que estarão concluídas num ponto futuro.",
        explanation="Ter (futuro) + particípio passado.\n\nUsos: ação concluída antes de momento futuro, suposição sobre o passado (*Ele terá chegado atrasado?* = provavelmente).",
        rules=[
            "Ter (futuro) + particípio passado.",
            "Ação concluída antes de momento futuro.",
            "Suposição/probabilidade sobre o passado.",
            "Particípio passado é invariável.",
        ],
        examples=[
            GrammarExample(
                text="Quando chegares, já terei terminado o trabalho.",
            ),
            GrammarExample(
                text="Ele ainda não chegou; terá havido trânsito.",
                note="suposição",
            ),
            GrammarExample(
                text="Amanhã a esta hora já teremos partido.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando chegares, já terei jantar.",
                correct="Quando chegares, já terei jantado.",
                note="O composto usa o particípio jantado. Vou ter jantado é uma alternativa perifrástica válida.",
            ),
        ],
        related=[
            "futuro-do-presente",
            "condicional",
            "preterito-perfeito-composto",
        ],
    ),
    GrammarTopic(
        slug="conectores-narrativos",
        title="Conectores narrativos",
        level="A2",
        category="Orações",
        summary="Palavras e expressões para organizar uma narrativa no tempo.",
        explanation="**Início:** primeiro, no início. **Continuação:** depois, em seguida, então. **Simultaneidade:** enquanto, entretanto. **Conclusão:** por fim, finalmente. **Rutura:** de repente, contudo.",
        rules=[
            "Primeiro/depois/em seguida/por fim para ordenar eventos.",
            "Enquanto/entretanto para ações simultâneas.",
            "De repente para eventos súbitos.",
            "Vírgula após conector no início no PB.",
        ],
        examples=[
            GrammarExample(
                text="Primeiro, tomei o café da manhã. Depois, fui trabalhar.",
            ),
            GrammarExample(
                text="Enquanto esperava, li um livro.",
            ),
            GrammarExample(
                text="Por fim, conseguimos terminar o projeto.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Enquanto que esperava.",
                correct="Enquanto esperava.",
                note="Enquanto é conjunção; não precisa de que.",
            ),
        ],
        related=[
            "sequencia-temporal",
            "conectores-argumentativos",
        ],
    ),
    GrammarTopic(
        slug="sequencia-temporal",
        title="Sequência temporal",
        level="A2",
        category="Orações",
        summary="Expressões que indicam a ordem cronológica de eventos.",
        explanation="**Ordem dos acontecimentos:** Antes de sair, fechei a janela; Depois de comer, lavei a louça. Antes que usa subjuntivo: Saí antes que chovesse. Depois que pode apresentar um fato ocorrido no indicativo (Depois que chegou, telefonou) ou uma situação futura com futuro do subjuntivo (Depois que chegar, telefone).\n\n**Simultaneidade:** Ao sair, encontrei Ana. **Sucessão imediata:** Mal cheguei, o telefone tocou. Enquanto e até que relacionam ações no tempo; a escolha verbal depende de fatos, hipóteses e referência temporal.",
        rules=[
            "Antes de e depois de usam infinitivo; um sujeito próprio pode ser explicitado: Depois de eles chegarem, jantamos.",
            "Antes que usa subjuntivo; depois que admite indicativo ou subjuntivo conforme o sentido e o tempo, não apenas conforme o sujeito.",
            "Ao + inf. = simultaneidade.",
            "Mal + verbo = assim que.",
        ],
        examples=[
            GrammarExample(
                text="Antes de sair, desliguei as luzes.",
            ),
            GrammarExample(
                text="Depois de comer, lavamos a louça.",
            ),
            GrammarExample(
                text="Mal entrei em casa, o telefone tocou.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Antes de que chegues.",
                correct="Antes que chegues.",
                note="Sem de com que + subjuntivo.",
            ),
        ],
        related=[
            "conectores-narrativos",
            "preterito-imperfeito",
        ],
    ),
    GrammarTopic(
        slug="discurso-indireto",
        title="Discurso indireto",
        level="A2",
        category="Discurso indireto",
        summary="Relatar o que alguém disse sem citar textualmente.",
        explanation="O discurso indireto ajusta pronomes e referências à perspectiva de quem relata. Numa perspectiva passada: Ela disse que estava cansada; Contou que tinha saído; Disse que viria.\n\nO recuo não é obrigatório se a referência continua válida: Ela disse que está cansada; Disse que virá amanhã. Ajusta os tempos ao sentido, não mecanicamente.",
        rules=[
            "Declarações usam que; perguntas totais usam se e perguntas parciais conservam o interrogativo.",
            "Os tempos podem recuar numa perspectiva passada ou conservar uma referência ainda atual.",
            "Pronomes e referências ajustam-se.",
            "Perguntas indiretas não usam interrogação.",
        ],
        examples=[
            GrammarExample(
                text="Ela disse que estava doente.",
            ),
            GrammarExample(
                text="Ele perguntou se eu queria café.",
                note="pergunta indireta com se",
            ),
            GrammarExample(
                text="O professor explicou que a prova seria na sexta.",
            ),
            GrammarExample(
                text="A Maria contou que tinha ido a Lisboa.",
                note="mais-que-perfeito",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ela disse que estavam cansada. (referindo-se a ela própria)",
                correct="Ela disse que estava cansada.",
                note="O verbo concorda com ela. Está cansada também é possível se a situação ainda se mantém.",
            ),
            GrammarMistake(
                wrong="Ele perguntou que eu queria café.",
                correct="Ele perguntou se eu queria café.",
                note="Perguntas sim/não usam se.",
            ),
        ],
        related=[
            "mudancas-temporais",
            "discurso-indireto-passado",
            "discurso-reportado",
        ],
    ),
    GrammarTopic(
        slug="mudancas-temporais",
        title="Mudanças temporais no discurso indireto",
        level="A2",
        category="Discurso indireto",
        summary="Transformações de tempo, lugar e pronomes ao relatar discurso.",
        explanation="Quando muda o ponto de referência, hoje pode passar a naquele dia, amanhã a no dia seguinte e aqui a ali/lá. Numa perspectiva passada, são frequentes o imperfeito para simultaneidade, o mais-que-perfeito para anterioridade e o condicional para posterioridade. Se o lugar, o dia ou a situação continuam válidos, podem manter-se as referências originais.",
        rules=[
            "Hoje→naquele dia; amanhã→no dia seguinte; ontem→no dia anterior.",
            "Aqui→ali/lá; aí→ali/lá.",
            "Os ajustes dependem do contexto; não há recuo automático de todos os tempos.",
            "Pronomes ajustam-se à perspectiva do narrador.",
        ],
        examples=[
            GrammarExample(
                text="Ele disse que ia ao médico no dia seguinte. (direto: Vou ao médico amanhã.)",
            ),
            GrammarExample(
                text="Ela disse que estava ali. (direto: Estou aqui.)",
            ),
            GrammarExample(
                text="Ela disse que tinha visto o filme no dia anterior. (direto: Vi o filme ontem.)",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Na segunda, Paulo disse: Vou ao médico amanhã. Na sexta, relato: Paulo disse que ia ao médico amanhã.",
                correct="Na sexta, relato: Paulo disse que ia ao médico no dia seguinte à conversa, terça-feira.",
                note="Amanhã contado a partir de sexta já não designa a terça-feira original. A reformulação preserva a data, o participante e o verbo ir.",
            ),
        ],
        related=[
            "discurso-indireto",
            "discurso-indireto-passado",
        ],
    ),
    GrammarTopic(
        slug="combinacao-pronominal",
        title="Dois complementos: objeto e destinatário",
        level="A2",
        category="Pronomes",
        summary="Retomar dois complementos com clareza e reconhecer formas raras.",
        explanation="No Brasil, prefira construções transparentes: Ela me deu o livro; Entreguei o documento para ele; Não me deu isso. As combinações mo, to e lho existem na tradição escrita, mas são raras na conversa brasileira. Em textos literários ou antigos, Deu-mo significa Deu isso a mim.\n\nNão é necessário produzir essas combinações para falar naturalmente. Com dois referentes, a prioridade é preservar quem entrega, o que é entregue e quem recebe.",
        rules=[
            "Use um pronome e um objeto explícito quando isso facilitar a compreensão.",
            "Reconheça mo = me + o e lho = lhe + o em leitura formal ou literária.",
            "Não atribua à fala brasileira a obrigação de combinar dois clíticos.",
        ],
        examples=[
            GrammarExample(
                text="Ela me entregou o relatório.",
            ),
            GrammarExample(
                text="Eu dei o livro para ela.",
            ),
            GrammarExample(
                text="Não me deu isso.",
            ),
            GrammarExample(
                text="Deu-mo. equivale a Deu isso a mim em registro literário.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ela entregou eu o livro.",
                correct="Ela me entregou o livro.",
                note="Eu é sujeito; me pode indicar o destinatário.",
            ),
            GrammarMistake(
                wrong="Eu dei ela para o livro.",
                correct="Eu dei o livro para ela.",
                note="Mantenha objeto e destinatário nas posições corretas.",
            ),
        ],
        related=[
            "pronomes-objeto-direto",
            "pronomes-objeto-indireto",
            "colocacao-pronominal",
        ],
    ),
]
