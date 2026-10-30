"""Portuguese grammar topics — A2."""

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
            "-ar: -ei, -aste, -ou, -ámos, -aram.",
            "-er: -i, -este, -eu, -emos, -eram.",
            "-ir: -i, -iste, -iu, -imos, -iram.",
            "Ação concluída e pontual no passado.",
            "A forma nós é igual no presente e pretérito para -ar.",
        ],
        examples=[
            GrammarExample(text="Ontem falei com a Maria.", translation=None),
            GrammarExample(text="Ela comeu tudo.", translation=None),
            GrammarExample(text="Nós abrimos a loja às oito.", translation=None),
            GrammarExample(
                text="Eles venderam a casa no ano passado.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ontem eu falo com ela.",
                correct="Ontem eu falei com ela.",
                note="Ontem requer pretérito perfeito.",
            ),
            GrammarMistake(
                wrong="Nós falemos.",
                correct="Nós falamos.",
                note="Falemos é conjuntivo/imperativo, não pretérito.",
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
        explanation="Marcadores por tempo:\n\n**Pretérito perfeito:** ontem, anteontem, a semana passada, há dois dias, já, ainda não, nunca.\n**Imperfeito:** todos os dias (no passado), antigamente, quando era criança, sempre, frequentemente.\n**Presente:** hoje, agora, atualmente, geralmente.\n**Futuro:** amanhã, na próxima semana, daqui a dois dias.",
        rules=[
            "Ontem, há + tempo → pretérito perfeito.",
            "Antigamente, quando era..., todos os dias (passado) → imperfeito.",
            "Já = already; Ainda não = not yet (perfeito).",
            "Nunca pode usar-se com perfeito ou presente.",
        ],
        examples=[
            GrammarExample(text="Ontem fui ao cinema.", translation=None),
            GrammarExample(text="Já leste o livro?", translation=None),
            GrammarExample(
                text="Ainda não terminei o trabalho.",
                translation=None,
            ),
            GrammarExample(
                text="Quando era criança, brincava na rua.",
                translation=None,
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
                translation=None,
                note="ir",
            ),
            GrammarExample(text="A festa foi ótima.", translation=None, note="ser"),
            GrammarExample(text="Ela teve uma ideia brilhante.", translation=None),
            GrammarExample(text="Nós fizemos o jantar.", translation=None),
            GrammarExample(text="Eles vieram cedo.", translation=None),
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
                translation=None,
            ),
            GrammarExample(text="Ela cantava muito bem.", translation=None),
            GrammarExample(
                text="Estava a chover quando saí de casa.",
                translation=None,
            ),
            GrammarExample(text="Eram cinco da tarde.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando era criança eu brinquei na rua.",
                correct="Quando era criança, brincava na rua.",
                note="Hábitos passados exigem imperfeito, não perfeito.",
            ),
        ],
        related=["perfeito-vs-imperfeito", "costumava", "marcadores-temporais"],
    ),
    GrammarTopic(
        slug="perfeito-vs-imperfeito",
        title="Perfeito vs imperfeito",
        level="A2",
        category="Tempos verbais",
        summary="Quando usar o pretérito perfeito e quando usar o pretérito imperfeito.",
        explanation="**Perfeito:** ação concluída, pontual. *Ontem fui ao cinema.*\n**Imperfeito:** ação habitual, contínua, descritiva. *Quando era criança, ia ao cinema.*\n\nRegra prática: imperfeito = CCTV (filme); perfeito = fotografia (momento).",
        rules=[
            "Perfeito: ação concluída, contada como facto.",
            "Imperfeito: cenário, hábito, descrição.",
            "Com ontem, já, há → perfeito.",
            "Com todos os dias, quando... → imperfeito.",
            "Imperfeito pinta o fundo; perfeito avança a história.",
        ],
        examples=[
            GrammarExample(
                text="Estava a dormir quando o despertador tocou.",
                translation=None,
                note="imperfeito + perfeito",
            ),
            GrammarExample(
                text="Quando vivia em Lisboa, ia à praia todos os fins de semana.",
                translation=None,
            ),
            GrammarExample(text="Ontem comi bacalhau.", translation=None, note="perfeito"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ontem chovia muito.",
                correct="Ontem choveu muito.",
                note="Ontem refere-se a facto concluído → perfeito.",
            ),
        ],
        related=["preterito-perfeito-regular", "preterito-imperfeito", "costumava"],
    ),
    GrammarTopic(
        slug="costumava",
        title="Costumar (hábitos passados)",
        level="A2",
        category="Tempos verbais",
        summary="Expressar hábitos passados com costumar + infinitivo.",
        explanation="**Costumar** no imperfeito + infinitivo = hábitos passados:\n\n- *Costumava ir à praia.* (= I used to go)\n- *Ele costumava fumar, mas deixou.*\n\nConjugação: costumava, costumavas, costumava, costumávamos, costumavam.",
        rules=[
            "Costumar no imperfeito + infinitivo = hábitos passados.",
            "Enfatiza que o hábito já não é atual.",
            "Alternativa: usar diretamente o imperfeito.",
            "Costumar no presente = hábito atual.",
        ],
        examples=[
            GrammarExample(text="Costumava acordar cedo.", translation=None),
            GrammarExample(text="Ela costumava cantar no coro.", translation=None),
            GrammarExample(
                text="Costumávamos jantar fora às sextas.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Costumei ir à praia.",
                correct="Costumava ir à praia.",
                note="Hábitos passados usam imperfeito, não perfeito.",
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
        summary="O, a, os, as — pronomes átonos que substituem o complemento direto.",
        explanation="Pronomes de objeto direto:\n\n- o (masc. sing.): *Comprei o livro → Comprei-o.*\n- a (fem. sing.): *Vi a Maria → Vi-a.*\n- os (masc. pl.) / as (fem. pl.)\n\nAdaptações: verbo -r/-s/-z → -lo/-la; verbo -m/-ão/-õe → -no/-na.",
        rules=[
            "Pronomes o/a/os/as substituem o objeto direto.",
            "Após -r/-s/-z: lo, la, los, las.",
            "Após -m/-ão/-õe: no, na, nos, nas.",
            "Em EP, colocação enclítica.",
        ],
        examples=[
            GrammarExample(text="Comprei-o ontem.", translation=None),
            GrammarExample(text="Vou comprá-lo.", translation=None, note="-r → -lo"),
            GrammarExample(text="Eles compraram-no.", translation=None, note="-m → -no"),
            GrammarExample(text="Conheço-a.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Vou comprar-o.",
                correct="Vou comprá-lo.",
                note="Verbo em -r: pronome transforma-se em -lo.",
            ),
            GrammarMistake(
                wrong="Comprei ele.",
                correct="Comprei-o.",
                note="Ele é pronome sujeito, nunca objeto direto.",
            ),
        ],
        related=["pronomes-objeto-indireto", "colocacao-pronominal"],
    ),
    GrammarTopic(
        slug="pronomes-objeto-indireto",
        title="Pronomes de objeto indireto",
        level="A2",
        category="Pronomes",
        summary="Me, te, lhe, nos, lhes — pronomes que substituem o complemento indireto.",
        explanation="| Pessoa | Pronome | Exemplo |\n|--------|---------|---------|\n| eu | me | *Deu-me o livro.* |\n| tu | te | *Ofereci-te um presente.* |\n| ele/você | lhe | *Disse-lhe a verdade.* |\n| nós | nos | *Emprestaram-nos o carro.* |\n| eles/vocês | lhes | *Expliquei-lhes a situação.* |",
        rules=[
            "Me, te, lhe, nos, lhes substituem complemento com a.",
            "Lhe/lhes são para a 3.ª pessoa.",
            "Em EP, colocação enclítica é a regra geral.",
            "Podem combinar-se com OD: mo, to, lho.",
        ],
        examples=[
            GrammarExample(text="Dei-lhe o recado.", translation=None),
            GrammarExample(text="A Maria emprestou-me o livro.", translation=None),
            GrammarExample(
                text="Não te disse nada.",
                translation=None,
                note="negação → próclise",
            ),
            GrammarExample(
                text="O professor explicou-lhes a matéria.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Dei para ele o livro.",
                correct="Dei-lhe o livro.",
                note="Usa-se pronome lhe em vez de para ele.",
            ),
            GrammarMistake(
                wrong="Eu lhe dei o livro.",
                correct="Eu dei-lhe o livro.",
                note="Frase afirmativa EP: pronome depois do verbo.",
            ),
        ],
        related=["pronomes-objeto-direto", "colocacao-pronominal"],
    ),
    GrammarTopic(
        slug="colocacao-pronominal",
        title="Colocação pronominal (EP)",
        level="A2",
        category="Pronomes",
        summary="Regras de colocação dos pronomes átonos em português europeu.",
        explanation="**1. Ênclise (depois do verbo) — regra geral:** *Chamo-me João.*\n**2. Próclise (antes) — com palavras atrativas:** negação, advérbios, pronomes relativos, interrogativos. *Não me digas. Já te disse.*\n**3. Mesóclise (no meio) — futuro e condicional:** *Dar-te-ei o livro.* (formal)",
        rules=[
            "Ênclise é a regra geral em EP.",
            "Próclise obrigatória com negação, advérbios, relativos, interrogativos.",
            "Mesóclise com futuro e condicional (formal).",
            "Nunca se começa frase com pronome átono em EP.",
        ],
        examples=[
            GrammarExample(text="Chamo-me Ana.", translation=None, note="ênclise"),
            GrammarExample(text="Não te esqueças.", translation=None, note="próclise"),
            GrammarExample(
                text="Já lhe contei tudo.",
                translation=None,
                note="próclise com advérbio",
            ),
            GrammarExample(
                text="Dar-te-ei uma resposta amanhã.",
                translation=None,
                note="mesóclise, formal",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Não esqueças-te.",
                correct="Não te esqueças.",
                note="Com negação, pronome vai antes do verbo.",
            ),
            GrammarMistake(
                wrong="Me chamo João.",
                correct="Chamo-me João.",
                note="EP não começa frase com pronome átono.",
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
                translation=None,
            ),
            GrammarExample(
                text="Este livro é melhor do que o filme.",
                translation=None,
                note="bom→melhor",
            ),
            GrammarExample(
                text="Ela é tão inteligente como o irmão.",
                translation=None,
            ),
            GrammarExample(
                text="Hoje está menos frio do que ontem.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É mais bom.",
                correct="É melhor.",
                note="Comparativo de bom é melhor.",
            ),
        ],
        related=["superlativos", "tao-como", "adjetivos-descritivos"],
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
                translation=None,
            ),
            GrammarExample(text="Este restaurante é ótimo.", translation=None),
            GrammarExample(text="A torre é altíssima.", translation=None, note="sintético"),
            GrammarExample(
                text="Este é o filme menos interessante do ano.",
                translation=None,
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
        related=["comparativos", "tao-como", "adjetivos-descritivos"],
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
            GrammarExample(text="É tão inteligente como tu.", translation=None),
            GrammarExample(
                text="Tenho tanto trabalho como na semana passada.",
                translation=None,
            ),
            GrammarExample(text="Ela dorme tanto como eu.", translation=None),
            GrammarExample(
                text="Estava tão cansada que adormeceu no sofá.",
                translation=None,
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
        related=["comparativos", "superlativos", "adjetivos-descritivos"],
    ),
    GrammarTopic(
        slug="imperativo-afirmativo",
        title="Imperativo afirmativo",
        level="A2",
        category="Verbos",
        summary="Dar ordens, instruções e conselhos de forma afirmativa.",
        explanation="**Tu**: radical do presente sem -s: *fala!, come!, abre!*\n**Você/Vocês**: presente do conjuntivo: *fale!, comam!*\n**Nós**: presente do conjuntivo: *falemos!*\n\nCom pronomes (ênclise): *Diz-me!, Senta-te!, Levantem-se!*",
        rules=[
            "Tu: radical do presente sem -s.",
            "Você/vocês: presente do conjuntivo.",
            "Pronomes átonos seguem o verbo (ênclise).",
        ],
        examples=[
            GrammarExample(
                text="Fala mais devagar, por favor.",
                translation=None,
                note="tu",
            ),
            GrammarExample(text="Coma a sopa.", translation=None, note="você"),
            GrammarExample(text="Digam-me a verdade.", translation=None, note="vocês + pronome"),
            GrammarExample(text="Senta-te.", translation=None, note="tu, reflexivo"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Falas mais devagar!",
                correct="Fala mais devagar!",
                note="Imperativo tu perde o -s.",
            ),
            GrammarMistake(
                wrong="Senta-se! (para tu)",
                correct="Senta-te!",
                note="Para tu, o pronome é te.",
            ),
        ],
        related=["imperativo-negativo", "imperativo-irregular", "colocacao-pronominal"],
    ),
    GrammarTopic(
        slug="imperativo-negativo",
        title="Imperativo negativo",
        level="A2",
        category="Verbos",
        summary="Dar ordens negativas, proibições e conselhos negativos.",
        explanation="O imperativo negativo usa o **presente do conjuntivo** para **todas** as pessoas:\n- *Não fales alto!* (tu)\n- *Não fale alto!* (você)\n- *Não falemos alto!* (nós)\n- *Não falem alto!* (vocês)\n\nCom pronomes (próclise): *Não te esqueças!*",
        rules=[
            "Imperativo negativo usa sempre o presente do conjuntivo.",
            "Para tu, a forma negativa é diferente da afirmativa.",
            "Com negação, pronomes vão antes do verbo (próclise).",
            "Você e vocês têm a mesma forma.",
        ],
        examples=[
            GrammarExample(text="Não fales tão alto.", translation=None, note="tu"),
            GrammarExample(text="Não coma isso.", translation=None, note="você"),
            GrammarExample(
                text="Não se esqueçam do passaporte.",
                translation=None,
                note="vocês + próclise",
            ),
            GrammarExample(text="Não me interrompas.", translation=None, note="tu, próclise"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Não fala alto! (para tu)",
                correct="Não fales alto!",
                note="Para tu, usa-se o conjuntivo.",
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
        explanation="| Verbo | tu | você |\n|-------|-----|------|\n| dizer | diz | diga |\n| fazer | faz | faça |\n| ser | sê | seja |\n| estar | está | esteja |\n| ir | vai | vá |\n| ter | tem | tenha |\n| pôr | põe | ponha |\n| vir | vem | venha |\n| ver | vê | veja |\n\nNegativo: sempre conjuntivo (*não digas, não faças*).",
        rules=[
            "Cada verbo irregular deve ser memorizado.",
            "Tu: deriva do presente sem -s.",
            "Você/vocês: presente do conjuntivo.",
            "Negativo: sempre conjuntivo.",
        ],
        examples=[
            GrammarExample(text="Sê simpático.", translation=None, note="ser, tu"),
            GrammarExample(text="Faça o favor de entrar.", translation=None, note="fazer, você"),
            GrammarExample(text="Põe a mesa, por favor.", translation=None, note="pôr, tu"),
            GrammarExample(
                text="Não ponhas os pés em cima da mesa.",
                translation=None,
                note="negativo, tu",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Seja feliz! (para tu)",
                correct="Sê feliz!",
                note="Para tu, imperativo de ser é sê.",
            ),
            GrammarMistake(
                wrong="Não faz isso!",
                correct="Não faças isso!",
                note="Negativo: não faças (tu).",
            ),
        ],
        related=["imperativo-afirmativo", "imperativo-negativo", "presente-conjuntivo"],
    ),
    GrammarTopic(
        slug="futuro-do-presente",
        title="Futuro do presente",
        level="A2",
        category="Tempos verbais",
        summary="Conjugação do futuro simples do indicativo.",
        explanation="Infinitivo + terminações: -ei, -ás, -á, -emos, -ão.\n\nIrregulares: dizer→direi, fazer→farei, trazer→trarei.\n\nNa fala, prefere-se *ir + infinitivo*. Com pronomes: mesóclise (*dir-te-ei*).",
        rules=[
            "Forma-se com infinitivo + -ei, -ás, -á, -emos, -ão.",
            "Três irregulares: dizer, fazer, trazer.",
            "Na fala, pouco usado.",
            "Com pronomes: mesóclise (formal).",
        ],
        examples=[
            GrammarExample(text="Falaremos sobre isso amanhã.", translation=None),
            GrammarExample(
                text="O concerto realizar-se-á no sábado.",
                translation=None,
                note="mesóclise",
            ),
            GrammarExample(text="Direi a verdade.", translation=None, note="irregular"),
            GrammarExample(text="Ela fará o jantar.", translation=None, note="irregular"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Nós fazeremos.",
                correct="Nós faremos.",
                note="Fazer no futuro é irregular: farei, farás...",
            ),
        ],
        related=["ir-futuro", "condicional", "futuro-composto", "futuro-do-conjuntivo"],
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
                translation=None,
                note="pedido cordial",
            ),
            GrammarExample(
                text="Se tivesse dinheiro, viajaria pelo mundo.",
                translation=None,
            ),
            GrammarExample(
                text="Ele disse que chegaria às três.",
                translation=None,
            ),
            GrammarExample(text="Poderia ajudar-me?", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se tivesse dinheiro, viajava pelo mundo.",
                correct="Se tivesse dinheiro, viajaria pelo mundo.",
                note="Se+imperfeito conj. → condicional.",
            ),
            GrammarMistake(
                wrong="Eu gostava de um café.",
                correct="Eu gostaria de um café.",
                note="Gostaria é mais cordial.",
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
                translation=None,
            ),
            GrammarExample(
                text="Ele ainda não chegou; terá havido trânsito.",
                translation=None,
                note="suposição",
            ),
            GrammarExample(
                text="Amanhã a esta hora já teremos partido.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando chegares, já terei jantar.",
                correct="Quando chegares, já terei jantado.",
                note="O composto usa o particípio jantado. Vou ter jantado é uma alternativa perifrástica válida.",
            ),
        ],
        related=["futuro-do-presente", "condicional", "preterito-perfeito-composto"],
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
            "Vírgula após conector no início em EP.",
        ],
        examples=[
            GrammarExample(
                text="Primeiro, tomei o pequeno-almoço. Depois, fui trabalhar.",
                translation=None,
            ),
            GrammarExample(
                text="Enquanto esperava, li um livro.",
                translation=None,
            ),
            GrammarExample(
                text="Por fim, conseguimos terminar o projeto.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Enquanto que esperava.",
                correct="Enquanto esperava.",
                note="Enquanto é conjunção; não precisa de que.",
            ),
        ],
        related=["sequencia-temporal", "conectores-argumentativos"],
    ),
    GrammarTopic(
        slug="sequencia-temporal",
        title="Sequência temporal",
        level="A2",
        category="Orações",
        summary="Expressões que indicam a ordem cronológica de eventos.",
        explanation="**Anterioridade:** *Antes de + inf.* / *Antes que + conj.* **Posterioridade:** *Depois de + inf.* / *Mal + verbo.* **Simultaneidade:** *Ao + inf.* **Duração:** *Enquanto, Até que.*",
        rules=[
            "Antes de/Depois de + inf. (sujeito igual).",
            "Antes que/Depois que + conj. (sujeito diferente).",
            "Ao + inf. = simultaneidade.",
            "Mal + verbo = assim que.",
        ],
        examples=[
            GrammarExample(
                text="Antes de sair, desliguei as luzes.",
                translation=None,
            ),
            GrammarExample(
                text="Depois de comer, lavámos a louça.",
                translation=None,
            ),
            GrammarExample(
                text="Mal entrei em casa, o telefone tocou.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Antes de que chegues.",
                correct="Antes que chegues.",
                note="Sem de com que + conjuntivo.",
            ),
        ],
        related=["conectores-narrativos", "preterito-imperfeito"],
    ),
    GrammarTopic(
        slug="discurso-indireto",
        title="Discurso indireto",
        level="A2",
        category="Discurso indireto",
        summary="Relatar o que alguém disse sem citar textualmente.",
        explanation="O discurso indireto ajusta pronomes e referências à perspetiva de quem relata. Numa perspetiva passada: Ela disse que estava cansada; Contou que tinha saído; Disse que viria.\n\nO recuo não é obrigatório se a referência continua válida: Ela disse que está cansada; Disse que virá amanhã. Ajusta os tempos ao sentido, não mecanicamente.",
        rules=[
            "Declarações usam que; perguntas totais usam se e perguntas parciais conservam o interrogativo.",
            "Os tempos podem recuar numa perspetiva passada ou conservar uma referência ainda atual.",
            "Pronomes e referências ajustam-se.",
            "Perguntas indiretas não usam interrogação.",
        ],
        examples=[
            GrammarExample(text="Ela disse que estava doente.", translation=None),
            GrammarExample(
                text="Ele perguntou se eu queria café.",
                translation=None,
                note="pergunta indireta com se",
            ),
            GrammarExample(
                text="O professor explicou que a prova seria na sexta.",
                translation=None,
            ),
            GrammarExample(
                text="A Maria contou que tinha ido a Lisboa.",
                translation=None,
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
        explanation="Quando muda o ponto de referência, hoje pode passar a naquele dia, amanhã a no dia seguinte e aqui a ali/lá. Numa perspetiva passada, são frequentes o imperfeito para simultaneidade, o mais-que-perfeito para anterioridade e o condicional para posterioridade. Se o lugar, o dia ou a situação continuam válidos, podem manter-se as referências originais.",
        rules=[
            "Hoje→naquele dia; amanhã→no dia seguinte; ontem→no dia anterior.",
            "Aqui→ali/lá; aí→ali/lá.",
            "Os ajustes dependem do contexto; não há recuo automático de todos os tempos.",
            "Pronomes ajustam-se à perspetiva do narrador.",
        ],
        examples=[
            GrammarExample(
                text="Ele disse que ia ao médico no dia seguinte. (direto: Vou ao médico amanhã.)",
                translation=None,
            ),
            GrammarExample(
                text="Ela disse que estava ali. (direto: Estou aqui.)",
                translation=None,
            ),
            GrammarExample(
                text="Ela disse que tinha visto o filme no dia anterior. (direto: Vi o filme ontem.)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Na segunda disse: Vou amanhã. Na sexta relato: Ele disse que vinha amanhã.",
                correct="Na sexta relato: Ele disse que vinha no dia seguinte, terça-feira.",
                note="Amanhã contado a partir de sexta já não designa a terça-feira original; adapta a referência para preservar a data.",
            ),
        ],
        related=["discurso-indireto", "discurso-indireto-passado"],
    ),
    GrammarTopic(
        slug="combinacao-pronominal",
        title="Combinação de pronomes: mo, to, lho",
        level="A2",
        category="Pronomes",
        summary="Fusão dos pronomes de complemento direto e indireto numa só forma.",
        explanation="Em português europeu, quando um pronome de **complemento indireto** (me, te, lhe, nos, vos, lhes) e um de **complemento direto** (o, a, os, as) aparecem juntos, fundem-se numa só forma.\n\n**Regras de combinação:**\n- me + o/a/os/as → mo/ma/mos/mas\n- te + o/a/os/as → to/ta/tos/tas\n- lhe + o/a/os/as → lho/lha/lhos/lhas\n- nos + o/a/os/as → no-lo/no-la/no-los/no-las\n- vos + o/a/os/as → vo-lo/vo-la/vo-los/vo-las\n- lhes + o/a/os/as → lho/lha/lhos/lhas (igual a lhe)\n\n**Posição:** em frases afirmativas, o pronome combinado coloca-se depois do verbo com hífen:\n- *Ele deu-mo.* (= Ele deu isso a mim)\n- *Vou explicar-to.* (= Vou explicar isso a ti)\n\nCom negação, coloca-se antes do verbo:\n- *Não mo deu.* (= Não me deu isso)\n\nNota: no Brasil, estas formas são raras e muitas vezes evitadas.",
        structure="me+o → mo · te+o → to · lhe+o → lho · nos+o → no-lo · vos+o → vo-lo · lhes+o → lho",
        rules=[
            "A combinação é obrigatória no português europeu quando OD e OI coocorrem.",
            "A forma resultante concorda com o OD em género e número: mo/ma/mos/mas.",
            "O pronome combinado une o OI (1.ª parte) ao OD (2.ª parte).",
            "Após verbo conjugado, usa-se hífen: Deu-mo.",
            "Com negação, próclise: Não mo deu.",
        ],
        examples=[
            GrammarExample(
                text="Ele deu-mo ontem.",
                translation=None,
                note="me + o → mo",
            ),
            GrammarExample(
                text="Quem te contou isso? — A Maria contou-to.",
                translation=None,
                note="te + o → to",
            ),
            GrammarExample(
                text="O livro? Emprestei-lho na semana passada.",
                translation=None,
                note="lhe + o → lho",
            ),
            GrammarExample(
                text="Não no-lo entregaram a tempo.",
                translation=None,
                note="nos + o → no-lo; próclise com negação",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Deu-me-o.",
                correct="Deu-mo.",
                note="Os pronomes devem fundir-se: me+o → mo.",
            ),
            GrammarMistake(
                wrong="Não deu-mo.",
                correct="Não mo deu.",
                note="Com negação, o pronome vai antes do verbo.",
            ),
        ],
        related=[
            "pronomes-objeto-direto",
            "pronomes-objeto-indireto",
            "colocacao-pronominal",
        ],
    ),
]
