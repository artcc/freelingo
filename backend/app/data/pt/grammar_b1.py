"""Portuguese grammar topics — B1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="presente-conjuntivo",
        title="Presente do conjuntivo",
        level="B1",
        category="Conjuntivo",
        summary="Formação e uso do presente do conjuntivo.",
        explanation="| | falar | comer | abrir |\n|---|-------|-------|-------|\n| eu | fale | coma | abra |\n| tu | fales | comas | abras |\n| ele | fale | coma | abra |\n| nós | falemos | comamos | abramos |\n| eles | falem | comam | abram |\n\nIrregulares: ser (seja), estar (esteja), ter (tenha), ir (vá), saber (saiba), querer (queira), fazer (faça), pôr (ponha).",
        rules=[
            "Forma-se a partir da 1.ª pessoa do presente.",
            "Substitui-se -o por -e (-ar) ou -a (-er/-ir).",
            "Usa-se após desejo, dúvida, necessidade, emoção.",
            "Muitos irregulares.",
        ],
        examples=[
            GrammarExample(text="Espero que fales com ela.", translation=None),
            GrammarExample(
                text="Duvido que ele venha.",
                translation=None,
                note="vir, irregular",
            ),
            GrammarExample(text="É importante que tu estudes.", translation=None),
            GrammarExample(text="Queres que eu vá contigo?", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Espero que tu falas com ela.",
                correct="Espero que tu fales com ela.",
                note="Depois de que, usa-se conjuntivo.",
            ),
            GrammarMistake(
                wrong="É preciso que ele vai.",
                correct="É preciso que ele vá.",
                note="Ir no conjuntivo: vá.",
            ),
        ],
        related=["talvez", "expressoes-desejo", "subjuntivo-recomendacao"],
    ),
    GrammarTopic(
        slug="expressoes-desejo",
        title="Expressões de desejo",
        level="B1",
        category="Conjuntivo",
        summary="Usar o conjuntivo após expressões de desejo como espero que, quero que, oxalá.",
        explanation="O conjuntivo é obrigatório após desejo:\n- *Espero que venhas. / Quero que sejas feliz. / Oxalá chova.*\n- *Tomara que ela passe.* / *Deus queira que não chova.*",
        rules=[
            "Conjuntivo obrigatório após expressões de desejo.",
            "Querer que, esperar que, desejar que + conjuntivo.",
            "Oxalá e tomara que + conjuntivo.",
            "Mudança de sujeito ativa o conjuntivo.",
        ],
        examples=[
            GrammarExample(text="Espero que tenhas uma boa viagem.", translation=None),
            GrammarExample(text="Quero que vocês sejam felizes.", translation=None),
            GrammarExample(text="Oxalá não chova amanhã.", translation=None),
            GrammarExample(text="Tomara que ela consiga o emprego.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Espero que tens sucesso.",
                correct="Espero que tenhas sucesso.",
                note="Conjuntivo após espero que.",
            ),
            GrammarMistake(
                wrong="Quero que ele é pontual.",
                correct="Quero que ele seja pontual.",
                note="Ser no conjuntivo: seja.",
            ),
        ],
        related=["presente-conjuntivo", "talvez", "subjuntivo-recomendacao"],
    ),
    GrammarTopic(
        slug="talvez",
        title="Talvez",
        level="B1",
        category="Conjuntivo",
        summary="Usar talvez com conjuntivo para expressar possibilidade.",
        explanation="**Talvez** + conjuntivo (padrão): *Talvez ele venha amanhã.*\nTalvez + indicativo (coloquial, mais certeza): *Talvez ele vem amanhã.*",
        rules=[
            "Talvez + conjuntivo é a forma padrão.",
            "Talvez + indicativo é coloquial.",
            "Talvez pode ir antes ou depois do verbo.",
        ],
        examples=[
            GrammarExample(text="Talvez vá à festa.", translation=None),
            GrammarExample(text="Talvez ela saiba a resposta.", translation=None),
            GrammarExample(text="Vamos talvez ao cinema.", translation=None),
            GrammarExample(text="Talvez seja melhor esperar.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Talvez ele vai.",
                correct="Talvez ele vá.",
                note="O padrão com talvez é o conjuntivo.",
            ),
        ],
        related=["presente-conjuntivo", "expressoes-desejo", "subjuntivo-duvida"],
    ),
    GrammarTopic(
        slug="subjuntivo-recomendacao",
        title="Conjuntivo com recomendações",
        level="B1",
        category="Conjuntivo",
        summary="Conjuntivo após expressões impessoais de recomendação e necessidade.",
        explanation="Usa-se conjuntivo após:\n- *É preciso que... / É necessário que... / É importante que...*\n- *Convém que... / É melhor que...*",
        rules=[
            "É preciso/necessário/importante que + conjuntivo.",
            "Convém que + conjuntivo.",
            "É melhor que + conjuntivo.",
        ],
        examples=[
            GrammarExample(text="É preciso que acabes o trabalho.", translation=None),
            GrammarExample(
                text="É importante que todos participem.",
                translation=None,
            ),
            GrammarExample(
                text="Convém que tragas o passaporte.",
                translation=None,
            ),
            GrammarExample(text="É melhor que vás ao médico.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É preciso que tu acabas.",
                correct="É preciso que tu acabes.",
                note="É preciso que exige conjuntivo.",
            ),
            GrammarMistake(
                wrong="É importante ele vai.",
                correct="É importante que ele vá.",
                note="Ir no conjuntivo: vá.",
            ),
        ],
        related=["presente-conjuntivo", "expressoes-desejo", "subjuntivo-avaliacao"],
    ),
    GrammarTopic(
        slug="subjuntivo-duvida",
        title="Conjuntivo com dúvida",
        level="B1",
        category="Conjuntivo",
        summary="Usar o conjuntivo para expressar dúvida, incerteza e probabilidade.",
        explanation="Dúvida → conjuntivo:\n- *Duvido que ele venha. / Não acho que seja boa ideia.*\n- *É possível que chova. / Pode ser que ainda dê tempo.*",
        rules=[
            "Duvido que, não acho que + conjuntivo.",
            "É possível/provável que + conjuntivo.",
            "Pode ser que + conjuntivo.",
            "Negação do verbo de opinião ativa o conjuntivo.",
        ],
        examples=[
            GrammarExample(text="Duvido que ela saiba a resposta.", translation=None),
            GrammarExample(
                text="Não acho que seja uma boa ideia.",
                translation=None,
            ),
            GrammarExample(
                text="É possível que cheguemos atrasados.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Não acho que ele tem razão.",
                correct="Não acho que ele tenha razão.",
                note="Negação + que → conjuntivo.",
            ),
            GrammarMistake(
                wrong="É possível que ela sabe.",
                correct="É possível que ela saiba.",
                note="É possível que exige conjuntivo.",
            ),
        ],
        related=["presente-conjuntivo", "talvez", "subjuntivo-recomendacao"],
    ),
    GrammarTopic(
        slug="subjuntivo-avaliacao",
        title="Conjuntivo com avaliações",
        level="B1",
        category="Conjuntivo",
        summary="Usar o conjuntivo após expressões de avaliação emocional.",
        explanation="Avaliação → conjuntivo:\n- *É bom que tenhas vindo. / É uma pena que vás embora.*\n- *Que bom que estejas aqui! / Que pena que não possas vir.*",
        rules=[
            "É bom/mau/triste/pena que + conjuntivo.",
            "Expressões emocionais ativam o conjuntivo.",
            "Que bom que/Que pena que + conjuntivo.",
        ],
        examples=[
            GrammarExample(text="É bom que estejas aqui.", translation=None),
            GrammarExample(text="É uma pena que não possas vir.", translation=None),
            GrammarExample(text="Que bom que tenhas gostado!", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É bom que estás aqui.",
                correct="É bom que estejas aqui.",
                note="É bom que exige conjuntivo.",
            ),
        ],
        related=["presente-conjuntivo", "subjuntivo-recomendacao", "subjuntivo-duvida"],
    ),
    GrammarTopic(
        slug="preterito-perfeito-composto",
        title="Pretérito perfeito composto",
        level="B1",
        category="Tempos verbais",
        summary="Expressar ações repetidas ou contínuas que se prolongam até ao presente.",
        explanation="Presente de **ter** + particípio passado.\n\n- *Tenho estudado muito.* (= I have been studying — ação repetida até agora)\n- *Ela tem trabalhado bastante.*\n\n**Diferenciação EP:** NÃO equivale ao present perfect inglês para ações únicas. *Comi ontem* (única), *Tenho comido bem* (repetida).",
        rules=[
            "Ter (presente) + particípio.",
            "Ação repetida/contínua até ao presente.",
            "NÃO equivale ao present perfect para ações únicas.",
            "Ação única: pretérito perfeito simples.",
        ],
        examples=[
            GrammarExample(
                text="Tenho ido ao ginásio todas as semanas.",
                translation=None,
                note="repetida",
            ),
            GrammarExample(text="Ela tem andado muito cansada.", translation=None),
            GrammarExample(
                text="Ultimamente tenho pensado em ti.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Tenho comido bacalhau ontem.",
                correct="Comi bacalhau ontem.",
                note="Ação única passada: pretérito simples, não composto.",
            ),
        ],
        related=[
            "marcadores-composto",
            "mais-que-perfeito",
            "preterito-perfeito-regular",
        ],
    ),
    GrammarTopic(
        slug="mais-que-perfeito",
        title="Pretérito mais-que-perfeito simples",
        level="B1",
        category="Tempos verbais",
        summary="Expressar uma ação passada anterior a outra ação passada.",
        explanation="Forma-se da 3.ª pl. do pretérito perfeito (-ram):\n\n*Falaram → falara, falaras, falara, faláramos, falaram.*\n\nUso literário/formal. Na fala, prefere-se o composto: *tinha falado*.",
        rules=[
            "Forma-se a partir da 3.ª pl. do pretérito perfeito.",
            "Uso literário/formal.",
            "Na fala: ter (imperf.) + particípio.",
        ],
        examples=[
            GrammarExample(
                text="Quando cheguei, ela já saíra.",
                translation=None,
                note="literário",
            ),
            GrammarExample(
                text="Quando cheguei, ela já tinha saído.",
                translation=None,
                note="composto, comum",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando cheguei, ela já tinha saíra.",
                correct="Quando cheguei, ela já tinha saído. / Quando cheguei, ela já saíra.",
                note="Não combines a forma simples saíra com tinha; o composto usa o particípio saído.",
            ),
        ],
        related=[
            "preterito-perfeito-composto",
            "marcadores-composto",
            "preterito-mais-que-perfeito",
        ],
    ),
    GrammarTopic(
        slug="marcadores-composto",
        title="Marcadores do pretérito perfeito composto",
        level="B1",
        category="Adjetivos e advérbios",
        summary="Expressões que indicam ação contínua/repetida até ao presente.",
        explanation="Marcadores típicos:\n\n- Ultimamente: *Ultimamente tenho dormido mal.*\n- Nos últimos tempos/meses/anos: *Tenho andado ocupado.*\n- Até agora: *Até agora tenho conseguido.*\n- Desde + data: *Desde janeiro que tenho ido.*",
        rules=[
            "Ultimamente, nos últimos tempos → composto.",
            "Até agora + composto = ação contínua.",
            "Desde + data + que + composto.",
        ],
        examples=[
            GrammarExample(
                text="Ultimamente tenho pensado muito nisso.",
                translation=None,
            ),
            GrammarExample(
                text="Nos últimos meses tenho trabalhado muito.",
                translation=None,
            ),
            GrammarExample(
                text="Até agora tudo tem corrido bem.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ultimamente estudei muito.",
                correct="Ultimamente tenho estudado muito.",
                note="Ultimamente pede composto.",
            ),
        ],
        related=["preterito-perfeito-composto", "marcadores-temporais"],
    ),
    GrammarTopic(
        slug="voz-passiva",
        title="Voz passiva",
        level="B1",
        category="Voz passiva",
        summary="Formação e uso da voz passiva com ser + particípio passado.",
        explanation="**Ser** + particípio passado (concordante com sujeito):\n\n- Ativa: *O chef preparou o jantar.*\n- Passiva: *O jantar foi preparado pelo chef.*\n\nO agente é introduzido por *por*. O particípio concorda em género e número.",
        rules=[
            "Ser + particípio passado (concordante).",
            "Agente = por + substantivo.",
            "Particípio concorda.",
            "Mais comum na escrita formal.",
        ],
        examples=[
            GrammarExample(
                text="O bolo foi feito pela minha avó.",
                translation=None,
            ),
            GrammarExample(
                text="As cartas são entregues de manhã.",
                translation=None,
            ),
            GrammarExample(text="A ponte foi construída em 1900.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="O bolo foi feito por minha avó.",
                correct="O bolo foi feito pela minha avó.",
                note="Pela = por+a, contração obrigatória.",
            ),
        ],
        related=["se-impessoal", "se-passivo", "passiva-reflexa"],
    ),
    GrammarTopic(
        slug="se-impessoal",
        title="Se impessoal",
        level="B1",
        category="Voz passiva",
        summary="Usar a partícula se para expressar sujeito indeterminado.",
        explanation="**Se** como índice de indeterminação do sujeito:\n- Verbo sempre na 3.ª singular: *Vive-se bem em Portugal.*\n- *Precisa-se de empregados.* (singular, mesmo com objeto plural)\n\nNÃO confundir com se passivo (verbo concorda com sujeito).",
        rules=[
            "Se impessoal: verbo sempre na 3.ª singular.",
            "Usa-se com verbos intransitivos ou transitivos indiretos.",
        ],
        examples=[
            GrammarExample(text="Vive-se bem nesta cidade.", translation=None),
            GrammarExample(
                text="Precisa-se de voluntários.",
                translation=None,
                note="singular",
            ),
            GrammarExample(text="Aqui come-se bem.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Precisam-se de voluntários.",
                correct="Precisa-se de voluntários.",
                note="Se impessoal: verbo fica no singular.",
            ),
        ],
        related=["se-passivo", "voz-passiva"],
    ),
    GrammarTopic(
        slug="se-passivo",
        title="Se passivo",
        level="B1",
        category="Voz passiva",
        summary="Usar a partícula se para formar a voz passiva sintética.",
        explanation="**Se passivo**: verbo concorda com o sujeito paciente.\n- *Vende-se uma casa. / Vendem-se casas.*\n\nEquivale a: *Uma casa é vendida. / Casas são vendidas.*\n\nMuito comum em anúncios.",
        rules=[
            "Se passivo: verbo concorda com sujeito.",
            "Equivale à passiva com ser.",
            "Comum em anúncios e linguagem formal.",
        ],
        examples=[
            GrammarExample(text="Vende-se este apartamento.", translation=None),
            GrammarExample(text="Vendem-se carros usados.", translation=None),
            GrammarExample(text="Alugam-se quartos.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Vende-se carros.",
                correct="Vendem-se carros.",
                note="Se passivo: verbo concorda com carros (plural).",
            ),
        ],
        related=["se-impessoal", "voz-passiva", "passiva-reflexa"],
    ),
    GrammarTopic(
        slug="que-relativo",
        title="Pronome relativo que",
        level="B1",
        category="Orações",
        summary="Usar que como pronome relativo para orações subordinadas.",
        explanation="**Que** refere-se a pessoas e coisas, pode ser sujeito ou objeto:\n\n- *O livro que li é interessante.*\n- *A pessoa que chegou é o diretor.*\n\nCom preposição: *de que, a que, em que, por que* (formal).",
        rules=[
            "Que refere-se a pessoas e coisas.",
            "Pode ser sujeito ou objeto.",
            "Com preposição: de que, a que, em que.",
        ],
        examples=[
            GrammarExample(
                text="O livro que estou a ler é fascinante.",
                translation=None,
            ),
            GrammarExample(
                text="A pessoa que telefonou não deixou nome.",
                translation=None,
            ),
            GrammarExample(
                text="O filme de que te falei ganhou um prémio.",
                translation=None,
                note="formal",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="O livro que eu gosto.",
                correct="O livro de que eu gosto.",
                note="Gostar exige de: de que.",
            ),
        ],
        related=["onde-quando-relativo", "cujo"],
    ),
    GrammarTopic(
        slug="onde-quando-relativo",
        title="Pronomes relativos onde e quando",
        level="B1",
        category="Orações",
        summary="Usar onde (lugar) e quando (tempo) como pronomes relativos.",
        explanation="**Onde** (= where): lugar físico. **Nota EP:** NÃO usar onde para situações abstratas; usar *em que* ou *no qual*.\n**Quando** (= when): tempo.",
        rules=[
            "Onde = lugar físico. Não usar para situações abstratas.",
            "Quando = tempo.",
            "Para situações abstratas: em que / no qual.",
        ],
        examples=[
            GrammarExample(
                text="A casa onde cresci era no campo.",
                translation=None,
            ),
            GrammarExample(text="O país de onde venho é frio.", translation=None),
            GrammarExample(
                text="Lembro-me do dia quando nos conhecemos.",
                translation=None,
            ),
            GrammarExample(
                text="Esta é a razão pela qual não fui.",
                translation=None,
                note="razão → pela qual",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Uma situação onde todos ganham.",
                correct="Uma situação em que todos ganham.",
                note="Onde é só para lugar físico.",
            ),
        ],
        related=["que-relativo", "cujo"],
    ),
    GrammarTopic(
        slug="cujo",
        title="Pronome relativo cujo",
        level="B1",
        category="Orações",
        summary="Usar cujo/a/os/as para expressar posse em orações relativas.",
        explanation="**Cujo** (= whose) concorda em género e número com a **coisa possuída** (não com o possuidor).\n\n- *O homem cujo filho é médico.* (filho = masc. sing.)\n- *A mulher cuja casa visitei.* (casa = fem. sing.)\n\nCujo NUNCA é seguido de artigo.",
        rules=[
            "Cujo concorda com a coisa possuída.",
            "NUNCA se usa artigo depois de cujo.",
        ],
        examples=[
            GrammarExample(
                text="O escritor cujo livro ganhou o prémio.",
                translation=None,
            ),
            GrammarExample(text="A rapariga cuja mãe conheces.", translation=None),
            GrammarExample(
                text="As empresas cujos funcionários estão em greve.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="O homem cujo o filho é médico.",
                correct="O homem cujo filho é médico.",
                note="Cujo nunca leva artigo.",
            ),
        ],
        related=["que-relativo", "onde-quando-relativo"],
    ),
    GrammarTopic(
        slug="condicional-composto",
        title="Condicional composto",
        level="B1",
        category="Condicionais",
        summary="Expressar condições não realizadas no passado.",
        explanation="Ter (condicional) + particípio passado.\n\n- *Se tivesse estudado, teria passado.*\n- *Ela teria vindo se soubesse.*",
        rules=[
            "Ter (condicional) + particípio.",
            "Condição não realizada no passado.",
            "Usa-se com se + MQP conjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Se tivesse estudado, teria passado no exame.",
                translation=None,
            ),
            GrammarExample(
                text="Ela teria vindo se soubesse.",
                translation=None,
            ),
            GrammarExample(
                text="Sem a tua ajuda, não teríamos conseguido.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se tinha estudado, teria passado.",
                correct="Se tivesse estudado, teria passado.",
                note="Se + condição passada: MQP conjuntivo.",
            ),
        ],
        related=["condicional", "se-imperfeito-subjuntivo"],
    ),
    GrammarTopic(
        slug="se-imperfeito-subjuntivo",
        title="Se + imperfeito do conjuntivo",
        level="B1",
        category="Condicionais",
        summary="Construir orações condicionais com se + imperfeito do conjuntivo.",
        explanation="**Estrutura:** *Se + imperfeito conjuntivo + condicional*\n- *Se tivesse dinheiro, viajaria pelo mundo.*\n- Coloquial EP: *Se tivesse dinheiro, viajava.* (imperfeito em vez de condicional)\n\nFormação: da 3.ª pl. do pretérito perfeito: falaram → falasse.",
        rules=[
            "Se + imperfeito conj. → condição hipotética.",
            "Principal usa condicional ou imperfeito (coloquial).",
            "Forma-se da 3.ª pl. do pretérito perfeito.",
        ],
        examples=[
            GrammarExample(
                text="Se eu tivesse tempo, ia contigo.",
                translation=None,
                note="coloquial",
            ),
            GrammarExample(
                text="Se ela estudasse mais, passaria.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se eu tinha dinheiro, viajava.",
                correct="Se eu tivesse dinheiro, viajava.",
                note="Condição hipotética: se + conjuntivo.",
            ),
        ],
        related=["condicional", "condicional-composto", "futuro-do-conjuntivo"],
    ),
    GrammarTopic(
        slug="futuro-do-conjuntivo",
        title="Futuro do conjuntivo",
        level="B1",
        category="Conjuntivo",
        summary="O futuro do conjuntivo — tempo exclusivo do português, essencial em EP.",
        explanation="Forma-se a partir da 3.ª pl. do pretérito perfeito (sem -am):\n*falaram → falar, falares, falar, falarmos, falarem*\n\nUsa-se com **quando, se, assim que, logo que, enquanto** para ações futuras hipotéticas.\n\nTempo quase exclusivo do português!",
        rules=[
            "Da 3.ª pl. do pretérito perfeito sem -am.",
            "Com quando, se, assim que, logo que, enquanto.",
            "Ação futura hipotética ou condicionada.",
            "Essencial no EP.",
        ],
        examples=[
            GrammarExample(text="Quando chegares, avisa-me.", translation=None),
            GrammarExample(text="Se puderem, venham cedo.", translation=None),
            GrammarExample(text="Assim que souber, digo-te.", translation=None),
            GrammarExample(
                text="Enquanto houver esperança, continuaremos.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando chegas, avisa-me.",
                correct="Quando chegares, avisa-me.",
                note="Ação futura: quando + futuro conjuntivo.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "se-imperfeito-subjuntivo",
            "imperfeito-conjuntivo",
        ],
    ),
    GrammarTopic(
        slug="discurso-indireto-passado",
        title="Discurso indireto no passado",
        level="B1",
        category="Discurso indireto",
        summary="Relatar discurso quando o verbo introdutor está no passado.",
        explanation="Ao adotar uma perspetiva passada, usa o imperfeito para simultaneidade (Disse que estava cansada), o mais-que-perfeito para anterioridade (Disse que tinha saído) e o condicional para posterioridade (Disse que viria). Um pedido pode passar a Pediu que eu fosse.\n\nMantém tempos atuais quando o contexto o justifica: Disse que está cansada, se ainda está; Disse que virá amanhã, se o evento continua futuro. Ajusta também pronomes e referências de lugar e tempo.",
        rules=[
            "O recuo temporal depende da perspetiva adotada e da validade atual da informação.",
            "Presente→imperfeito; perfeito→MQP; futuro→condicional.",
            "Imperativo→imperfeito conjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Ela disse: Estou cansada. → Ela disse que estava cansada.",
                translation=None,
            ),
            GrammarExample(
                text="Ele perguntou: Já comeste? → Ele perguntou se eu já tinha comido.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ela disse que estar cansada.",
                correct="Ela disse que estava cansada.",
                note="A oração com que precisa de verbo conjugado; está cansada é válido se a situação continua atual.",
            ),
        ],
        related=["discurso-indireto", "mudancas-temporais", "discurso-reportado"],
    ),
    GrammarTopic(
        slug="conectores-argumentativos",
        title="Conectores argumentativos",
        level="B1",
        category="Orações",
        summary="Conectores para estruturar argumentos: causa, consequência, oposição, concessão.",
        explanation="**Causa:** porque, visto que, já que. **Consequência:** por isso, portanto, assim. **Oposição:** mas, porém, contudo. **Concessão:** embora, mesmo que, ainda que. **Adição:** além disso, também, não só... como também.",
        rules=[
            "Porque/visto que/já que → causa.",
            "Por isso/portanto → consequência.",
            "Mas/porém/contudo → oposição.",
            "Embora/ainda que → concessão (+ conjuntivo).",
        ],
        examples=[
            GrammarExample(
                text="Fiquei em casa porque estava a chover.",
                translation=None,
                note="causa",
            ),
            GrammarExample(
                text="Estava a chover, por isso fiquei em casa.",
                translation=None,
                note="consequência",
            ),
            GrammarExample(
                text="Embora estivesse a chover, fui passear.",
                translation=None,
                note="concessão + conjuntivo",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Embora está a chover, vou sair.",
                correct="Embora esteja a chover, vou sair.",
                note="Embora exige conjuntivo.",
            ),
        ],
        related=["conectores-narrativos", "conectores-avancados"],
    ),
    GrammarTopic(
        slug="por-para",
        title="Por e para: usos e diferenças",
        level="B1",
        category="Preposicoes",
        summary="Distinção entre as preposições por e para conforme expressem causa, finalidade, destinatário, meio, direção e outros contextos.",
        explanation="**Por** e **para** são duas preposições que causam confusão porque em muitas línguas traduzem-se por uma só palavra.\n\n### Usos principais de POR\n\n- **Causa ou motivo:** *Cheguei tarde por causa do trânsito.*\n- **Meio:** *Falo contigo por telefone.*\n- **Duração:** *Estudei por três horas.*\n- **Troca ou preço:** *Comprei o livro por dez euros.*\n- **Agente da passiva:** *Os Lusíadas foi escrito por Camões.*\n- **Frequência:** *Vou ao ginásio duas vezes por semana.*\n- **Substituição:** *Veio o meu irmão por mim.*\n\n### Usos principais de PARA\n\n- **Finalidade:** *Estudo para aprender.*\n- **Destinatário:** *O presente é para ti.*\n- **Direção:** *Parto para Lisboa amanhã.*\n- **Prazo:** *Preciso disto para segunda-feira.*\n- **Opinião:** *Para mim, é a melhor opção.*\n- **Comparação:** *Para principiante, fala muito bem.*\n\n### Expressões fixas com POR\n\n- *por isso* (therefore), *por favor* (please), *por acaso* (by chance), *por enquanto* (for now), *por exemplo* (for example)\n\n### Expressões fixas com PARA\n\n- *para já* (for now), *para sempre* (forever), *para além de* (beyond)",
        structure="POR: causa/motivo · meio · duração · troca · agente da passiva · opinião\nPARA: finalidade · destinatário · direção · prazo · opinião · comparação",
        rules=[
            '"Por" exprime a causa ou motivo de uma ação.',
            '"Para" exprime a finalidade ou o propósito.',
            '"Por" indica o meio ou canal: por correio, por telefone.',
            '"Para" indica o destinatário: para ti, para o João.',
            'Na voz passiva, o agente é introduzido por "por".',
        ],
        examples=[
            GrammarExample(
                text="Estudo português para viajar por Portugal.",
                translation=None,
                note="para = finalidade; por = lugar aproximado",
            ),
            GrammarExample(
                text="Obrigado por tudo. O presente é para ti.",
                translation=None,
                note="por = causa do agradecimento; para = destinatário",
            ),
            GrammarExample(
                text="Passei por tua casa mas não estavas.",
                translation=None,
                note="lugar",
            ),
            GrammarExample(
                text="Este relatório é para sexta-feira.",
                translation=None,
                note="prazo",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Obrigado para a ajuda.",
                correct="Obrigado pela ajuda.",
                note='Com "obrigado" usa-se "por".',
            ),
            GrammarMistake(
                wrong="Estudo por ser médico.",
                correct="Estudo para ser médico.",
                note='"Para" + infinitivo indica o propósito.',
            ),
            GrammarMistake(
                wrong="A ponte foi construída para os romanos.",
                correct="A ponte foi construída pelos romanos.",
                note='O agente da passiva introduz-se com "por".',
            ),
        ],
        related=["preposicoes-lugar", "voz-passiva", "conectores-argumentativos"],
    ),
]
