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
                text="Espero que você fale com ela.",
            ),
            GrammarExample(
                text="Duvido que ele venha.",
                note="vir, irregular",
            ),
            GrammarExample(
                text="É importante que você estude.",
            ),
            GrammarExample(
                text="Você quer que eu vá com você?",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Espero que você falam com ela.",
                correct="Espero que você fale com ela.",
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
        explanation="Para desejar uma ação de outra pessoa, use querer/esperar/desejar que + subjuntivo: Quero que você venha; Espero que ela consiga. Para um desejo do próprio sujeito, o infinitivo é usual: Quero viajar; Espero chegar cedo. Não é o sentido de desejo sozinho que obriga o subjuntivo, mas a construção escolhida.\n\nTomara que é frequente no Brasil: Tomara que dê certo! Oxalá também expressa desejo, mas costuma ter tom literário ou solene. O tempo verbal depende da situação e da perspectiva.",
        rules=[
            "Nas construções de desejo com que, pratique o subjuntivo; com infinitivo, não há flexão de modo.",
            "Querer que, esperar que, desejar que + subjuntivo.",
            "Oxalá e tomara que + subjuntivo.",
            "Diferencie Quero viajar de Quero que você viaje; não transforme essa preferência em regra automática para toda oração.",
        ],
        examples=[
            GrammarExample(
                text="Espero que você tenha uma boa viagem.",
            ),
            GrammarExample(
                text="Quero que vocês sejam felizes.",
            ),
            GrammarExample(
                text="Oxalá não chova amanhã.",
                note="tom mais literário; na conversa, Tomara que não chova amanhã",
            ),
            GrammarExample(
                text="Tomara que ela consiga o emprego.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Espero que você tem sucesso.",
                correct="Espero que você tenha sucesso.",
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
        explanation="Talvez apresenta uma possibilidade, sem afirmar sua realização. Antes do verbo, a norma-padrão usa geralmente subjuntivo: Talvez ela venha amanhã. Depois de uma oração, pode ocorrer com indicativo: Ela vem amanhã, talvez.\n\nNa conversa brasileira, também se encontra Talvez ela vem amanhã. A distribuição depende de uso, posição e registro; não se pode deduzir automaticamente um grau maior de certeza apenas pelo indicativo. Para uma produção escrita formal com talvez antes do verbo, pratique o subjuntivo.",
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
                wrong="Talvez eles venha amanhã.",
                correct="Talvez eles venham amanhã.",
                note="Com eles, a forma do subjuntivo é venham. A escolha entre modos também depende do registro e da posição de talvez.",
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
                text="É preciso que você termine o trabalho.",
            ),
            GrammarExample(
                text="É importante que todos participem.",
            ),
            GrammarExample(
                text="Convém que você traga o passaporte.",
            ),
            GrammarExample(
                text="É melhor que você vá ao médico.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É preciso que você termina.",
                correct="É preciso que você termine.",
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
        explanation="Construções como Duvido que ele venha, Não acho que seja boa ideia, É possível que chova e Pode ser que ainda dê tempo usam subjuntivo para apresentar dúvida ou possibilidade.\n\nA negação sozinha não determina o modo. Compare Não acho que ele tenha razão, que não apresenta a opinião como um fato aceito, com Não sabia que você estava aqui, que mantém a informação como factual. Considere a construção e o sentido, não apenas a presença de não e que.",
        rules=[
            "Duvido que, não acho que + subjuntivo.",
            "É possível/provável que + subjuntivo.",
            "Pode ser que + subjuntivo.",
            "A escolha do modo depende da construção e da perspectiva: Não acho que tenha razão; Não sabia que estava aqui.",
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
                wrong="Não acho que eles tenha razão.",
                correct="Não acho que eles tenham razão.",
                note="Com eles, o presente do subjuntivo é tenham. Não generalize a escolha do modo para toda oração com negação: Não sabia que você estava aqui usa indicativo.",
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
        summary="Escolher o modo verbal em avaliações e reações emocionais.",
        explanation="Construções como É bom que você esteja aqui e É uma pena que você não possa vir usam subjuntivo para avaliar uma situação. Isso não torna obrigatório o subjuntivo em toda expressão de emoção.\n\nNo português brasileiro, Que bom que e Que pena que aparecem normalmente com indicativo ao comentar fatos: Que bom que você veio!; Que pena que você não pode ficar! O subjuntivo também é possível, sobretudo em registro mais formal: Que bom que você tenha gostado! A emoção não determina o modo sozinha, e o subjuntivo também pode avaliar fatos ocorridos: É uma pena que ela tenha perdido o voo.",
        rules=[
            "Pratique o subjuntivo em construções como É bom que você esteja aqui e É uma pena que ela tenha saído.",
            "Uma avaliação emocional pode comentar um fato; subjuntivo não significa necessariamente dúvida.",
            "Que bom que e Que pena que admitem indicativo ao comentar fatos: Que bom que você veio! Considere construção, sentido e registro.",
        ],
        examples=[
            GrammarExample(
                text="É bom que você esteja aqui.",
            ),
            GrammarExample(
                text="É uma pena que você não possa vir.",
            ),
            GrammarExample(
                text="Que bom que você gostou!",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="É bom que vocês esteja aqui.",
                correct="É bom que vocês estejam aqui.",
                note="Vocês exige estejam no subjuntivo. Em Que bom que vocês estão aqui!, o indicativo é válido para comentar um fato.",
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
        explanation="Presente de **ter** + particípio passado.\n\n- *Tenho estudado muito.* (= atividade repetida até agora)\n- *Ela tem trabalhado bastante.*\n\n**Valor aspectual:** apresenta repetição ou continuidade em um período que chega ao presente. Não corresponde automaticamente ao present perfect do inglês: para uma ocorrência concluída ontem, diga Comi ontem.\n\nO perfeito simples também pode apresentar repetição em um período delimitado: Fui à academia três vezes na semana passada. Compare com Tenho ido à academia, que apresenta uma prática recorrente até o presente.",
        rules=[
            "Ter (presente) + particípio.",
            "Ação repetida/contínua até ao presente.",
            "NÃO equivale ao present perfect para ações únicas.",
            "O perfeito simples apresenta situações delimitadas, únicas ou repetidas: Fui três vezes na semana passada.",
        ],
        examples=[
            GrammarExample(
                text="Tenho ido à academia todas as semanas.",
                note="repetida",
            ),
            GrammarExample(
                text="Ela tem andado muito cansada.",
            ),
            GrammarExample(
                text="Ultimamente tenho pensado em você.",
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
        title="Mais-que-perfeito: anterioridade no passado",
        level="B1",
        category="Tempos verbais",
        summary="Expressar uma ação passada anterior a outra ação passada.",
        explanation="Para uma ação anterior a outra referência passada, use tinha + particípio: Quando ela chegou, eu já tinha saído. O auxiliar concorda com o sujeito; o particípio permanece invariável: nós tínhamos saído, elas tinham escrito.\n\nA forma simples aparece sobretudo em literatura e registros formais: Quando ela chegou, eu já saíra. Para formar o paradigma, retire -ram da terceira pessoa do plural do perfeito e acrescente -ra, -ras, -ra, -ramos, -reis, -ram, ajustando a acentuação: falaram → falara, falaras, falara, faláramos, faláreis, falaram. Compare fizeram → fizera.\n\nO contexto distingue falaram no perfeito e no mais-que-perfeito simples; a forma composta costuma ser mais transparente na conversa brasileira. Pratique tinha falado e reconheça falara na leitura, sem tomar uma forma como mais correta que a outra.",
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
        explanation="Ultimamente, nos últimos meses e até agora podem acompanhar uma atividade repetida ou contínua: Ultimamente tenho dormido mal; Nos últimos meses tenho trabalhado bastante. Desde + data pode marcar o início: Desde janeiro, tenho ido à academia.\n\nEssas expressões não impõem o composto: Até agora terminei três relatórios apresenta resultados delimitados. O aspecto depende do verbo, do contexto e da perspectiva, não de uma palavra isolada.",
        rules=[
            "Ultimamente e nos últimos tempos combinam com o composto quando se destaca repetição ou continuidade.",
            "Até agora pode combinar com tempos diferentes conforme a perspectiva.",
            "Desde + data pode localizar o início: Desde janeiro, tenho estudado português.",
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
        explanation="Na norma-padrão, se pode indeterminar quem realiza a ação com verbo na terceira pessoa do singular: Vive-se bem nesta cidade; Precisa-se de funcionários. Em precisar de, funcionários não é sujeito do verbo.\n\nCompare com a passiva sintética: Publicam-se os resultados, em que os resultados é sujeito e exige plural. Na conversa brasileira, Aqui se vive bem é natural; a próclise não é um erro. Analise a função do se separadamente de sua posição antes ou depois do verbo.",
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
                text="Aqui se come bem.",
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
        explanation="Na norma-padrão, se passivo acompanha verbo transitivo e há concordância com o sujeito paciente: Vende-se uma casa; Vendem-se casas. A segunda frase equivale a Casas são vendidas.\n\nNo uso brasileiro, também se encontram construções invariáveis como Vende-se casas, frequentemente analisadas como impessoais. Ao revisar um anúncio segundo a norma-padrão escrita, pratique a concordância Vendem-se casas; não generalize esse critério como condenação de toda fala regional.",
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
                wrong="Vende-se carros. (em anúncio que deve seguir a norma-padrão escrita)",
                correct="Vendem-se carros.",
                note="Na norma-padrão escrita, se passivo exige concordância com carros. O singular também ocorre em usos brasileiros impessoais.",
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
        explanation="Que pode retomar pessoas ou coisas: O livro que li; A pessoa que chegou. Na norma-padrão escrita, conserve a preposição exigida pelo verbo: gostar de → O livro de que gosto; falar de alguém → A pessoa de quem falei.\n\nA conversa brasileira também usa relativas sem essa preposição: O livro que eu gosto. Essa construção, chamada relativa cortadora, é frequente na oralidade. Ao adaptar um texto à norma-padrão escrita, use de que ou de quem; a revisão ajusta registro, não prova que a construção oral seja ilegítima.",
        rules=[
            "Que refere-se a pessoas e coisas.",
            "Pode ser sujeito ou objeto.",
            "Com preposição: de que, a que, em que.",
        ],
        examples=[
            GrammarExample(
                text="O livro que estou lendo é fascinante.",
            ),
            GrammarExample(
                text="A pessoa que telefonou não deixou nome.",
            ),
            GrammarExample(
                text="O filme de que te falei ganhou um prêmio.",
                note="formal",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A pessoa que chegou estão aqui.",
                correct="A pessoa que chegou está aqui.",
                note="O verbo principal concorda com a pessoa. A omissão de preposição em relativas orais deve ser discutida como diferença de registro, não como erro universal.",
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
        explanation="Onde retoma um lugar: A casa onde cresci; O bairro onde moro. Na escrita formal, prefira em que ou no qual para uma situação abstrata: Uma situação em que todos ganham. A extensão de onde a referentes abstratos ocorre no uso; a adequação depende do registro.\n\nPara um nome temporal, em que é uma opção natural: Lembro do dia em que nos conhecemos. Quando também pode retomar uma referência temporal: Foi em maio, quando nos conhecemos. Não traduza mecanicamente o inglês the day when como o dia quando em todo contexto.",
        rules=[
            "Na escrita formal, reserve onde para lugares e prefira em que para situações abstratas.",
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
                text="Eu me lembro do dia em que nos conhecemos.",
            ),
            GrammarExample(
                text="Esta é a razão pela qual não fui.",
                note="razão → pela qual",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Uma situação onde todos ganham. (revisão para escrita formal)",
                correct="Uma situação em que todos ganham.",
                note="A revisão formal prefere em que para um referente abstrato; o uso ampliado de onde existe na língua.",
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
                text="O escritor cujo livro ganhou o prêmio chegou.",
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
                text="Se eu tivesse tempo, ia com você.",
                note="coloquial",
            ),
            GrammarExample(
                text="Se ela estudasse mais, passaria.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se eu tivessem dinheiro, viajaria mais.",
                correct="Se eu tivesse dinheiro, viajaria mais.",
                note="Eu exige tivesse, não tivessem. Se eu tinha dinheiro, viajava é válido para um hábito passado e não equivale necessariamente a uma hipótese presente.",
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
        explanation="Retire -am da terceira pessoa do plural do pretérito perfeito para obter a forma de eu/você: falaram → falar; fizeram → fizer; tiveram → tiver; puderam → puder; foram → for; viram (ver) → vir; vieram (vir) → vier. Com nós, acrescente -mos; com vocês, -em: fizermos, fizerem. Com tu, a norma-padrão usa -es: fizeres.\n\nUse em condições ou referências futuras introduzidas por se, quando, assim que, logo que e enquanto: Se você puder, venha; Quando você chegar, me avise. Compare Quando chego cedo, faço café (hábito) e Quando chegar amanhã, vou fazer café (evento futuro).\n\nNão use esse tempo com todo conector de sentido futuro: Caso você possa vir e Talvez você venha amanhã usam presente do subjuntivo. Distingua também Quando eu vir Ana (ver) de Quando eu vier aqui (vir).",
        rules=[
            "Da 3.ª pl. do pretérito perfeito sem -am.",
            "Com quando, se, assim que, logo que, enquanto.",
            "Ação futura hipotética ou condicionada.",
            "Frequente no português brasileiro: Quando você chegar, avise.",
        ],
        examples=[
            GrammarExample(
                text="Quando você chegar, me avise.",
            ),
            GrammarExample(
                text="Se puderem, venham cedo.",
            ),
            GrammarExample(
                text="Assim que souber, aviso você.",
            ),
            GrammarExample(
                text="Enquanto houver esperança, continuaremos.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando eu ver Ana amanhã, vou avisar.",
                correct="Quando eu vir Ana amanhã, vou avisar.",
                note="O futuro do subjuntivo de ver é vir; o de vir é vier. O infinitivo ver aparece em para eu ver.",
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
                text="Ele perguntou: Você já comeu? → Ele perguntou se eu já tinha comido.",
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
                text="Fiquei em casa porque estava chovendo.",
                note="causa",
            ),
            GrammarExample(
                text="Estava chovendo, por isso fiquei em casa.",
                note="consequência",
            ),
            GrammarExample(
                text="Embora estivesse chovendo, fui passear.",
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
        slug="infinitivo-pessoal",
        title="Infinitivo pessoal: sujeito e finalidade",
        level="B1",
        category="Verbos",
        summary="Explicitar quem realiza uma ação depois de preposições e expressões impessoais.",
        explanation="O infinitivo pessoal pode ter um sujeito próprio. Com eu e você/ele/ela, mantém a forma do infinitivo; com nós, recebe -mos; com vocês/eles/elas, -em: para eu falar, para você falar, para nós falarmos, para eles falarem. Com tu, a norma-padrão usa falares.\n\nUse-o quando ajuda a identificar quem realiza a ação: Preparei a sala para eles estudarem. Também pode ocorrer com o mesmo sujeito da principal: Para chegarmos a tempo, precisamos sair agora. Não se flexiona automaticamente qualquer infinitivo: Devemos estudar, não Devemos estudarmos.\n\nEm para eu fazer, eu é sujeito de fazer. Em Este presente é para mim, mim é complemento da preposição, sem infinitivo do qual seja sujeito. Não conclua que qualquer mim perto de infinitivo esteja errado: Para mim, estudar é importante apresenta um ponto de vista.\n\nDistinga infinitivo pessoal de futuro do subjuntivo: para eu fazer / quando eu fizer; para eu ver / quando eu vir; para eu vir / quando eu vier. Nos verbos regulares, as formas podem coincidir, mas a construção e o sentido são diferentes.",
        rules=[
            "Identifique o sujeito do infinitivo antes de escolher a forma.",
            "Use para eu fazer quando eu realiza a ação; para mim indica destinatário ou ponto de vista.",
            "Não flexione o infinitivo automaticamente depois de verbos modais: Podemos sair.",
        ],
        examples=[
            GrammarExample(text="Ela trouxe o texto para nós lermos."),
            GrammarExample(text="É importante vocês chegarem cedo."),
            GrammarExample(text="Antes de sair, confira o endereço."),
            GrammarExample(
                text="Quando eu fizer o jantar, aviso; preciso de tempo para fazer tudo."
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Nós devemos estudarmos hoje.",
                correct="Nós devemos estudar hoje.",
                note="Depois do modal devemos, o infinitivo permanece invariável.",
            ),
            GrammarMistake(
                wrong="Trouxe os textos para nós lerem.",
                correct="Trouxe os textos para nós lermos.",
                note="O sujeito nós corresponde a lermos, não lerem.",
            ),
        ],
        related=["futuro-do-conjuntivo", "por-para", "presente-conjuntivo"],
    ),
    GrammarTopic(
        slug="participios",
        title="Particípios e tempos compostos",
        level="B1",
        category="Tempos verbais",
        summary="Formar particípios regulares e frequentes irregulares, distinguindo tempo composto e passiva.",
        explanation="Nos verbos regulares, troque -ar por -ado e -er/-ir por -ido: falar/falado, comer/comido, partir/partido. Memorize os irregulares frequentes: fazer/feito, dizer/dito, ver/visto, escrever/escrito, abrir/aberto, pôr/posto e vir/vindo.\n\nCom ter, o particípio permanece invariável: Ela tem escrito cartas; Eles tinham feito o trabalho. A flexão está no auxiliar: tenho/tem/temos/têm estudado; tinha/tínhamos/tinham estudado. Compare com a passiva, em que há concordância: A carta foi escrita; Os textos foram escritos.\n\nAlguns verbos têm particípios duplos. O padrão tradicional distingue tinha aceitado de foi aceito e tinha entregado de foi entregue, mas aceito e entregue também são usados com ter no Brasil. As preferências variam conforme verbo e registro; não imponha a regra de um par a todos os verbos. Aprenda primeiro as formas frequentes em contexto.",
        rules=[
            "Use -ado para -ar e -ido para -er/-ir nos particípios regulares.",
            "Com ter, não faça concordância do particípio com sujeito ou objeto.",
            "Na passiva com ser, faça concordância com o sujeito paciente.",
            "Consulte o uso do verbo quando houver particípios duplos, sem generalizações automáticas.",
        ],
        examples=[
            GrammarExample(text="Tenho trabalhado bastante ultimamente."),
            GrammarExample(text="Quando cheguei, ela já tinha feito o almoço."),
            GrammarExample(text="Elas tinham escrito as cartas."),
            GrammarExample(text="As cartas foram escritas ontem."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Tenho fazido o almoço.",
                correct="Tenho feito o almoço.",
                note="O particípio de fazer é feito.",
            ),
            GrammarMistake(
                wrong="Elas tinham escritas as cartas.",
                correct="Elas tinham escrito as cartas.",
                note="Com ter, o particípio é invariável; na passiva, As cartas foram escritas tem concordância.",
            ),
        ],
        related=["preterito-perfeito-composto", "mais-que-perfeito", "voz-passiva"],
    ),
]
