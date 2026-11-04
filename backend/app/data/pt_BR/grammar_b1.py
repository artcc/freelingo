"""Brazilian Portuguese (grammar_b1) learning content."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="presente-conjuntivo",
        title="Presente do subjuntivo",
        level="B1",
        category="Subjuntivo",
        summary="Formação e uso do presente do subjuntivo.",
        explanation="| | falar | comer | abrir |\n|---|-------|-------|-------|\n| eu | fale | coma | abra |\n| tu | fales | comas | abras |\n| ele | fale | coma | abra |\n| nós | falemos | comamos | abramos |\n| eles | falem | comam | abram |\n\nIrregulares: ser (seja), estar (esteja), ter (tenha), ir (vá), saber (saiba), querer (queira), fazer (faça), pôr (ponha).",
        rules=[
            "Forma-se a partir da 1.ª pessoa do presente.",
            "Substitui-se -o por -e (-ar) ou -a (-er/-ir).",
            "Usa-se após desejo, dúvida, necessidade, emoção.",
            "Muitos irregulares.",
        ],
        examples=[
            GrammarExample(
                text="Espero que fales com ela.",
            ),
            GrammarExample(
                text="Duvido que ele venha.",
                note="vir, irregular",
            ),
            GrammarExample(
                text="É importante que tu estudes.",
            ),
            GrammarExample(
                text="Queres que eu vá contigo?",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Espero que tu falas com ela.",
                correct="Espero que tu fales com ela.",
                note="Espero que seleciona subjuntivo neste desejo; que sozinho não determina o modo: Sei que você fala é indicativo.",
            ),
            GrammarMistake(
                wrong="É preciso que ele vai.",
                correct="É preciso que ele vá.",
                note="Ir no subjuntivo: vá.",
            ),
        ],
        related=[
            "talvez",
            "expressoes-desejo",
            "subjuntivo-recomendacao",
        ],
    ),
    GrammarTopic(
        slug="expressoes-desejo",
        title="Expressões de desejo",
        level="B1",
        category="Subjuntivo",
        summary="Usar o subjuntivo após expressões de desejo como espero que, quero que, oxalá.",
        explanation="O subjuntivo é obrigatório após desejo:\n- *Espero que venhas. / Quero que sejas feliz. / Oxalá chova.*\n- *Tomara que ela passe.* / *Deus queira que não chova.*",
        rules=[
            "Subjuntivo obrigatório após expressões de desejo.",
            "Querer que, esperar que, desejar que + subjuntivo.",
            "Oxalá e tomara que + subjuntivo.",
            "Mudança de sujeito ativa o subjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Espero que tenhas uma boa viagem.",
            ),
            GrammarExample(
                text="Quero que vocês sejam felizes.",
            ),
            GrammarExample(
                text="Oxalá não chova amanhã.",
            ),
            GrammarExample(
                text="Tomara que ela consiga o emprego.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Espero que tens sucesso.",
                correct="Espero que tenhas sucesso.",
                note="Subjuntivo após espero que.",
            ),
            GrammarMistake(
                wrong="Quero que ele é pontual.",
                correct="Quero que ele seja pontual.",
                note="Ser no subjuntivo: seja.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "talvez",
            "subjuntivo-recomendacao",
        ],
    ),
    GrammarTopic(
        slug="talvez",
        title="Talvez",
        level="B1",
        category="Subjuntivo",
        summary="Usar talvez com subjuntivo para expressar possibilidade.",
        explanation="**Talvez** + subjuntivo (padrão): *Talvez ele venha amanhã.*\nTalvez + indicativo (coloquial, mais certeza): *Talvez ele vem amanhã.*",
        rules=[
            "Talvez + subjuntivo é a forma padrão.",
            "Talvez + indicativo é coloquial.",
            "Talvez pode ir antes ou depois do verbo.",
        ],
        examples=[
            GrammarExample(
                text="Talvez vá à festa.",
            ),
            GrammarExample(
                text="Talvez ela saiba a resposta.",
            ),
            GrammarExample(
                text="Vamos talvez ao cinema.",
            ),
            GrammarExample(
                text="Talvez seja melhor esperar.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Talvez ele vai.",
                correct="Talvez ele vá.",
                note="O padrão com talvez é o subjuntivo.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "expressoes-desejo",
            "subjuntivo-duvida",
        ],
    ),
    GrammarTopic(
        slug="subjuntivo-recomendacao",
        title="Subjuntivo com recomendações",
        level="B1",
        category="Subjuntivo",
        summary="Subjuntivo após expressões impessoais de recomendação e necessidade.",
        explanation="Usa-se subjuntivo após:\n- *É preciso que... / É necessário que... / É importante que...*\n- *Convém que... / É melhor que...*",
        rules=[
            "É preciso/necessário/importante que + subjuntivo.",
            "Convém que + subjuntivo.",
            "É melhor que + subjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="É preciso que acabes o trabalho.",
            ),
            GrammarExample(
                text="É importante que todos participem.",
            ),
            GrammarExample(
                text="Convém que tragas o passaporte.",
            ),
            GrammarExample(
                text="É melhor que vás ao médico.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É preciso que tu acabas.",
                correct="É preciso que tu acabes.",
                note="É preciso que exige subjuntivo.",
            ),
            GrammarMistake(
                wrong="É importante ele vai.",
                correct="É importante que ele vá.",
                note="Ir no subjuntivo: vá.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "expressoes-desejo",
            "subjuntivo-avaliacao",
        ],
    ),
    GrammarTopic(
        slug="subjuntivo-duvida",
        title="Subjuntivo com dúvida",
        level="B1",
        category="Subjuntivo",
        summary="Usar o subjuntivo para expressar dúvida, incerteza e probabilidade.",
        explanation="Dúvida → subjuntivo:\n- *Duvido que ele venha. / Não acho que seja boa ideia.*\n- *É possível que chova. / Pode ser que ainda dê tempo.*",
        rules=[
            "Duvido que, não acho que + subjuntivo.",
            "É possível/provável que + subjuntivo.",
            "Pode ser que + subjuntivo.",
            "Negação do verbo de opinião ativa o subjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Duvido que ela saiba a resposta.",
            ),
            GrammarExample(
                text="Não acho que seja uma boa ideia.",
            ),
            GrammarExample(
                text="É possível que cheguemos atrasados.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Não acho que ele tem razão.",
                correct="Não acho que ele tenha razão.",
                note="Negação + que → subjuntivo.",
            ),
            GrammarMistake(
                wrong="É possível que ela sabe.",
                correct="É possível que ela saiba.",
                note="É possível que exige subjuntivo.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "talvez",
            "subjuntivo-recomendacao",
        ],
    ),
    GrammarTopic(
        slug="subjuntivo-avaliacao",
        title="Subjuntivo com avaliações",
        level="B1",
        category="Subjuntivo",
        summary="Usar o subjuntivo após expressões de avaliação emocional.",
        explanation="Avaliação → subjuntivo:\n- *É bom que tenhas vindo. / É uma pena que vás embora.*\n- *Que bom que estejas aqui! / Que pena que não possas vir.*",
        rules=[
            "É bom/mau/triste/pena que + subjuntivo.",
            "Expressões emocionais ativam o subjuntivo.",
            "Que bom que/Que pena que + subjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="É bom que estejas aqui.",
            ),
            GrammarExample(
                text="É uma pena que não possas vir.",
            ),
            GrammarExample(
                text="Que bom que tenhas gostado!",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É bom que estás aqui.",
                correct="É bom que estejas aqui.",
                note="É bom que exige subjuntivo.",
            ),
        ],
        related=[
            "presente-conjuntivo",
            "subjuntivo-recomendacao",
            "subjuntivo-duvida",
        ],
    ),
    GrammarTopic(
        slug="preterito-perfeito-composto",
        title="Pretérito perfeito composto",
        level="B1",
        category="Tempos verbais",
        summary="Expressar ações repetidas ou contínuas que se prolongam até ao presente.",
        explanation="Presente de **ter** + particípio passado.\n\n- *Tenho estudado muito.* (= ação repetida até agora)\n- *Ela tem trabalhado bastante.*\n\n**Valor aspectual:** NÃO equivale ao perfeito inglês para ações únicas. *Comi ontem* (única), *Tenho comido bem* (repetida).",
        rules=[
            "Ter (presente) + particípio.",
            "Ação repetida/contínua até ao presente.",
            "NÃO equivale ao present perfect para ações únicas.",
            "Ação única: pretérito perfeito simples.",
        ],
        examples=[
            GrammarExample(
                text="Tenho ido ao ginásio todas as semanas.",
                note="repetida",
            ),
            GrammarExample(
                text="Ela tem andado muito cansada.",
            ),
            GrammarExample(
                text="Ultimamente tenho pensado em ti.",
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
                note="literário",
            ),
            GrammarExample(
                text="Quando cheguei, ela já tinha saído.",
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
            "Ultimamente e nos últimos tempos combinam com o composto quando se destaca repetição ou continuidade.",
            "Até agora + composto = ação contínua.",
            "Desde + data + que + composto.",
        ],
        examples=[
            GrammarExample(
                text="Ultimamente tenho pensado muito nisso.",
            ),
            GrammarExample(
                text="Nos últimos meses tenho trabalhado muito.",
            ),
            GrammarExample(
                text="Até agora tudo tem corrido bem.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ultimamente tenho estudo muito.",
                correct="Ultimamente tenho estudado muito.",
                note="O composto exige particípio. Ultimamente estudei muito também é possível se o falante resumir o período como concluído.",
            ),
        ],
        related=[
            "preterito-perfeito-composto",
            "marcadores-temporais",
        ],
    ),
    GrammarTopic(
        slug="voz-passiva",
        title="Voz passiva",
        level="B1",
        category="Voz passiva",
        summary="Formação e uso da voz passiva com ser + particípio passado.",
        explanation="**Ser** + particípio passado (concordante com sujeito):\n\n- Ativa: *O chef preparou o jantar.*\n- Passiva: *O jantar foi preparado pelo chef.*\n\nO agente é introduzido por *por*. O particípio concorda em gênero e número.",
        rules=[
            "Ser + particípio passado (concordante).",
            "Agente = por + substantivo.",
            "Particípio concorda.",
            "Mais comum na escrita formal.",
        ],
        examples=[
            GrammarExample(
                text="O bolo foi feito pela minha avó.",
            ),
            GrammarExample(
                text="As cartas são entregues de manhã.",
            ),
            GrammarExample(
                text="A ponte foi construída em 1900.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="As cartas foram entregue ontem.",
                correct="As cartas foram entregues ontem.",
                note="Na passiva com ser, o particípio concorda com o sujeito. Por minha avó e pela minha avó são válidos no Brasil.",
            ),
        ],
        related=[
            "se-impessoal",
            "se-passivo",
            "passiva-reflexa",
        ],
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
            GrammarExample(
                text="Vive-se bem nesta cidade.",
            ),
            GrammarExample(
                text="Precisa-se de voluntários.",
                note="singular",
            ),
            GrammarExample(
                text="Aqui come-se bem.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Precisam-se de voluntários.",
                correct="Precisa-se de voluntários.",
                note="Se impessoal: verbo fica no singular.",
            ),
        ],
        related=[
            "se-passivo",
            "voz-passiva",
        ],
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
            GrammarExample(
                text="Vende-se este apartamento.",
            ),
            GrammarExample(
                text="Vendem-se carros usados.",
            ),
            GrammarExample(
                text="Alugam-se quartos.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Vende-se carros.",
                correct="Vendem-se carros.",
                note="Se passivo: verbo concorda com carros (plural).",
            ),
        ],
        related=[
            "se-impessoal",
            "voz-passiva",
            "passiva-reflexa",
        ],
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
            ),
            GrammarExample(
                text="A pessoa que telefonou não deixou nome.",
            ),
            GrammarExample(
                text="O filme de que te falei ganhou um prémio.",
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
        related=[
            "onde-quando-relativo",
            "cujo",
        ],
    ),
    GrammarTopic(
        slug="onde-quando-relativo",
        title="Pronomes relativos onde e quando",
        level="B1",
        category="Orações",
        summary="Usar onde (lugar) e quando (tempo) como pronomes relativos.",
        explanation="**Onde**: lugar físico. **Na escrita formal:** NÃO usar onde para situações abstratas; usar *em que* ou *no qual*.\n**Quando**: tempo.",
        rules=[
            "Onde = lugar físico. Não usar para situações abstratas.",
            "Quando = tempo.",
            "Para situações abstratas: em que / no qual.",
        ],
        examples=[
            GrammarExample(
                text="A casa onde cresci era no campo.",
            ),
            GrammarExample(
                text="O país de onde venho é frio.",
            ),
            GrammarExample(
                text="Lembro-me do dia quando nos conhecemos.",
            ),
            GrammarExample(
                text="Esta é a razão pela qual não fui.",
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
        related=[
            "que-relativo",
            "cujo",
        ],
    ),
    GrammarTopic(
        slug="cujo",
        title="Pronome relativo cujo",
        level="B1",
        category="Orações",
        summary="Usar cujo/a/os/as para expressar posse em orações relativas.",
        explanation="**Cujo** (= whose) concorda em gênero e número com a **coisa possuída** (não com o possuidor).\n\n- *O homem cujo filho é médico.* (filho = masc. sing.)\n- *A mulher cuja casa visitei.* (casa = fem. sing.)\n\nCujo NUNCA é seguido de artigo.",
        rules=[
            "Cujo concorda com a coisa possuída.",
            "NUNCA se usa artigo depois de cujo.",
        ],
        examples=[
            GrammarExample(
                text="O escritor cujo livro ganhou o prémio.",
            ),
            GrammarExample(
                text="A garota cuja mãe você conhece chegou.",
            ),
            GrammarExample(
                text="As empresas cujos funcionários estão em greve.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="O homem cujo o filho é médico.",
                correct="O homem cujo filho é médico.",
                note="Cujo nunca leva artigo.",
            ),
        ],
        related=[
            "que-relativo",
            "onde-quando-relativo",
        ],
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
            "Usa-se com se + MQP subjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Se tivesse estudado, teria passado no exame.",
            ),
            GrammarExample(
                text="Ela teria vindo se soubesse.",
            ),
            GrammarExample(
                text="Sem a tua ajuda, não teríamos conseguido.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se tinha estudado, teria passado.",
                correct="Se tivesse estudado, teria passado.",
                note="Se + condição passada: MQP subjuntivo.",
            ),
        ],
        related=[
            "condicional",
            "se-imperfeito-subjuntivo",
        ],
    ),
    GrammarTopic(
        slug="se-imperfeito-subjuntivo",
        title="Se + imperfeito do subjuntivo",
        level="B1",
        category="Condicionais",
        summary="Construir orações condicionais com se + imperfeito do subjuntivo.",
        explanation="**Estrutura:** *Se + imperfeito subjuntivo + condicional*\n- *Se tivesse dinheiro, viajaria pelo mundo.*\n- Coloquial brasileiro: *Se tivesse dinheiro, viajava.* (imperfeito em vez de condicional)\n\nFormação: da 3.ª pl. do pretérito perfeito: falaram → falasse.",
        rules=[
            "Se + imperfeito conj. → condição hipotética.",
            "Principal usa condicional ou imperfeito (coloquial).",
            "Forma-se da 3.ª pl. do pretérito perfeito.",
        ],
        examples=[
            GrammarExample(
                text="Se eu tivesse tempo, ia contigo.",
                note="coloquial",
            ),
            GrammarExample(
                text="Se ela estudasse mais, passaria.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se eu tinha dinheiro, viajava.",
                correct="Se eu tivesse dinheiro, viajava.",
                note="Condição hipotética: se + subjuntivo.",
            ),
        ],
        related=[
            "condicional",
            "condicional-composto",
            "futuro-do-conjuntivo",
        ],
    ),
    GrammarTopic(
        slug="futuro-do-conjuntivo",
        title="Futuro do subjuntivo",
        level="B1",
        category="Subjuntivo",
        summary="Usar o futuro do subjuntivo em condições e referências futuras.",
        explanation="Forma-se a partir da 3.ª pl. do pretérito perfeito (sem -am):\n*falaram → falar, falares, falar, falarmos, falarem*\n\nUsa-se com **quando, se, assim que, logo que, enquanto** para ações futuras hipotéticas.\n\nTempo quase exclusivo do português!",
        rules=[
            "Da 3.ª pl. do pretérito perfeito sem -am.",
            "Com quando, se, assim que, logo que, enquanto.",
            "Ação futura hipotética ou condicionada.",
            "Frequente no português brasileiro: Quando você chegar, avise.",
        ],
        examples=[
            GrammarExample(
                text="Quando chegares, avisa-me.",
            ),
            GrammarExample(
                text="Se puderem, venham cedo.",
            ),
            GrammarExample(
                text="Assim que souber, digo-te.",
            ),
            GrammarExample(
                text="Enquanto houver esperança, continuaremos.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando chegas, avisa-me.",
                correct="Quando chegares, avisa-me.",
                note="Ação futura: quando + futuro subjuntivo.",
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
        explanation="Ao adotar uma perspectiva passada, usa o imperfeito para simultaneidade (Disse que estava cansada), o mais-que-perfeito para anterioridade (Disse que tinha saído) e o condicional para posterioridade (Disse que viria). Um pedido pode passar a Pediu que eu fosse.\n\nMantém tempos atuais quando o contexto o justifica: Disse que está cansada, se ainda está; Disse que virá amanhã, se o evento continua futuro. Ajusta também pronomes e referências de lugar e tempo.",
        rules=[
            "O recuo temporal depende da perspectiva adotada e da validade atual da informação.",
            "Presente→imperfeito; perfeito→MQP; futuro→condicional.",
            "Imperativo→imperfeito subjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Ela disse: Estou cansada. → Ela disse que estava cansada.",
            ),
            GrammarExample(
                text="Ele perguntou: Já comeste? → Ele perguntou se eu já tinha comido.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ela disse que estar cansada.",
                correct="Ela disse que estava cansada.",
                note="A oração com que precisa de verbo conjugado; está cansada é válido se a situação continua atual.",
            ),
        ],
        related=[
            "discurso-indireto",
            "mudancas-temporais",
            "discurso-reportado",
        ],
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
            "Embora/ainda que → concessão (+ subjuntivo).",
        ],
        examples=[
            GrammarExample(
                text="Fiquei em casa porque estava a chover.",
                note="causa",
            ),
            GrammarExample(
                text="Estava a chover, por isso fiquei em casa.",
                note="consequência",
            ),
            GrammarExample(
                text="Embora estivesse a chover, fui passear.",
                note="concessão + subjuntivo",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Embora está chovendo, vou sair.",
                correct="Embora esteja chovendo, vou sair.",
                note="Embora exige subjuntivo.",
            ),
        ],
        related=[
            "conectores-narrativos",
            "conectores-avancados",
        ],
    ),
    GrammarTopic(
        slug="por-para",
        title="Por e para: usos e diferenças",
        level="B1",
        category="Preposicoes",
        summary="Distinção entre as preposições por e para conforme expressem causa, finalidade, destinatário, meio, direção e outros contextos.",
        explanation="Por pode indicar causa (por causa do trânsito), meio (por telefone), duração (por três horas), preço (por dez reais), agente da passiva (escrito por Machado de Assis) e frequência (duas vezes por semana).\n\nPara pode indicar finalidade (Estudo para aprender), destinatário (O presente é para você), direção (Vou para Recife), prazo (Preciso disso para segunda-feira), opinião (Para mim, é a melhor opção) e comparação (Para iniciante, fala muito bem).\n\nCompare Fiz isso por você, que pode indicar motivo ou substituição, com Fiz isso para você, que destaca o destinatário. Expressões usuais incluem por isso, por favor, por acaso, por enquanto, por exemplo e para sempre.",
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
                note="para = finalidade; por = lugar aproximado",
            ),
            GrammarExample(
                text="Obrigado por tudo. O presente é para ti.",
                note="por = causa do agradecimento; para = destinatário",
            ),
            GrammarExample(
                text="Passei por tua casa mas não estavas.",
                note="lugar",
            ),
            GrammarExample(
                text="Este relatório é para sexta-feira.",
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
                wrong="A ponte foi construída por os romanos.",
                correct="A ponte foi construída pelos romanos.",
                note="Por + os se contrai em pelos. Para os romanos indica beneficiários, não construtores; não são reformulações equivalentes.",
            ),
        ],
        related=[
            "preposicoes-lugar",
            "voz-passiva",
            "conectores-argumentativos",
        ],
    ),
]
