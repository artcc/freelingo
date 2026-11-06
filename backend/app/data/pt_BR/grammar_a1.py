"""Brazilian Portuguese (grammar_a1) learning content."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="ser",
        title="Ser: identidade e características",
        level="A1",
        category="Verbos",
        summary="Apresentar identidade, origem, profissão e características.",
        explanation="Ser apresenta identidade (Sou Ana), origem (Sou de Recife), profissão (Ela é médica), características (A casa é grande), horas (São duas horas) e eventos (A reunião é aqui). Não indica apenas permanência: Hoje sou o responsável.\n\nPresente: eu sou; você/ele/ela é; nós somos; vocês/eles/elas são. Tu és é a forma da norma-padrão nas regiões que usam tu. O artigo antes de nomes próprios varia regionalmente: Ana e a Ana são possíveis.",
        rules=[
            "Use ser para identidade, profissão, origem e caracterização.",
            "Ser + de indica origem ou posse.",
            "Não confunda ser com estar para localizar pessoas e objetos.",
        ],
        examples=[
            GrammarExample(
                text="Sou brasileira.",
            ),
            GrammarExample(
                text="Você é professor?",
            ),
            GrammarExample(
                text="Nós somos de Salvador.",
            ),
            GrammarExample(
                text="A palestra é no auditório.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eu é estudante.",
                correct="Eu sou estudante.",
                note="O verbo concorda com eu.",
            ),
            GrammarMistake(
                wrong="Sou em casa.",
                correct="Estou em casa.",
                note="A localização de uma pessoa usa estar.",
            ),
        ],
        related=[
            "estar",
            "ser-nacionalidade",
            "horas",
        ],
    ),
    GrammarTopic(
        slug="estar",
        title="Estar: estados, localização e ações em curso",
        level="A1",
        category="Verbos",
        summary="Descrever estados e usar estar + gerúndio.",
        explanation="Estar apresenta estados (Estou cansado), localização (O livro está na mesa) e condições (A sopa está quente). Não se limita a situações temporárias: Está morto.\n\nPara uma ação em curso, use estar + gerúndio: Estou estudando; Está chovendo. Presente: estou, está, estamos, estão; com tu, a norma-padrão usa estás.",
        rules=[
            "Use estar para estados e localização de pessoas ou objetos.",
            "Use estar + gerúndio para ações em andamento.",
            "A nacionalidade normalmente é apresentada com ser.",
        ],
        examples=[
            GrammarExample(
                text="Estou em Recife.",
            ),
            GrammarExample(
                text="Ela está cansada hoje.",
            ),
            GrammarExample(
                text="Estamos estudando português.",
            ),
            GrammarExample(
                text="Está chovendo.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Sou em casa.",
                correct="Estou em casa.",
                note="Use estar para localização.",
            ),
            GrammarMistake(
                wrong="Estamos estudar.",
                correct="Estamos estudando.",
                note="A perífrase progressiva usa gerúndio.",
            ),
        ],
        related=[
            "ser",
            "estar-gerundio",
            "preposicoes-lugar",
        ],
    ),
    GrammarTopic(
        slug="pronomes-sujeito",
        title="Pronomes sujeito: você, tu, nós e a gente",
        level="A1",
        category="Pronomes",
        summary="Escolher pronomes e manter a concordância.",
        explanation="No Brasil, você é frequente e combina com a terceira pessoa: você fala. Vocês falam indica plural. Tu também é usado em várias regiões; a norma-padrão associa tu a falas, embora a fala regional também apresente tu fala. Reconhecer a variação não significa usar qualquer forma em qualquer registro.\n\nNós falamos e a gente fala podem designar o mesmo grupo. A gente é comum na conversa e exige singular no modelo ensinado. O senhor/a senhora expressa respeito conforme a situação. Vós é raro fora de textos antigos, religiosos ou usos muito específicos.",
        rules=[
            "Você/ele/ela fala; vocês/eles/elas falam.",
            "Nós falamos; a gente fala.",
            "Adapte o tratamento à relação e ao contexto, sem estigmatizar usos regionais.",
        ],
        examples=[
            GrammarExample(
                text="Você mora aqui?",
            ),
            GrammarExample(
                text="A gente estuda à noite.",
            ),
            GrammarExample(
                text="Nós falamos português.",
            ),
            GrammarExample(
                text="A senhora precisa de ajuda?",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Você moram aqui?",
                correct="Você mora aqui?",
                note="Você usa terceira pessoa do singular.",
            ),
            GrammarMistake(
                wrong="A gente estudamos.",
                correct="A gente estuda.",
                note="No modelo-padrão, a gente concorda no singular.",
            ),
        ],
        related=[
            "ser",
            "estar",
            "colocacao-pronominal",
        ],
    ),
    GrammarTopic(
        slug="artigos-definidos",
        title="Artigos definidos",
        level="A1",
        category="Artigos",
        summary="Usar o, a, os e as com concordância.",
        explanation="Os artigos definidos identificam referências conhecidas e concordam com o substantivo: o livro, a casa, os livros, as casas. No português brasileiro, o artigo antes de possessivos pode ser omitido: Meu livro e O meu livro são válidos. Antes de nomes de pessoas, o uso varia regionalmente: Ana e a Ana. Nomes de países têm convenções próprias: o Brasil, a França, Portugal.",
        rules=[
            "Faça concordância de gênero e número.",
            "Não trate o artigo antes de possessivos ou nomes pessoais como obrigatório em todo o Brasil.",
            "Use contrações quando a preposição e o artigo estiverem presentes: de + o = do.",
        ],
        examples=[
            GrammarExample(
                text="O carro é azul.",
            ),
            GrammarExample(
                text="As alunas chegaram.",
            ),
            GrammarExample(
                text="Meu irmão mora aqui.",
            ),
            GrammarExample(
                text="O meu irmão mora aqui.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="O senhora chegou.",
                correct="A senhora chegou.",
                note="Senhora é feminino.",
            ),
            GrammarMistake(
                wrong="As livro estão aqui.",
                correct="Os livros estão aqui.",
                note="Artigo e substantivo devem concordar.",
            ),
        ],
        related=[
            "artigos-indefinidos",
            "contracoes-preposicionais",
            "adjetivos-possessivos",
        ],
    ),
    GrammarTopic(
        slug="ser-nacionalidade",
        title="Ser + nacionalidades",
        level="A1",
        category="Verbos",
        summary="Como expressar nacionalidades e países de origem com o verbo ser.",
        explanation="Para expressar nacionalidade usa-se o verbo **ser** seguido do adjetivo de nacionalidade. Os adjetivos concordam em gênero e número com o sujeito.\n\nAlgumas nacionalidades: português/portuguesa, espanhol/espanhola, francês/francesa, inglês/inglesa, alemão/alemã, italiano/italiana, brasileiro/brasileira.",
        rules=[
            "O verbo ser apresenta nacionalidade, sem implicar que ela seja imutável.",
            "O adjetivo de nacionalidade concorda em gênero e número.",
            "Normalmente não se usa artigo em Sou brasileiro; nacionalidades se escrevem com minúscula.",
            "Nomes de países têm gênero: a França, o Brasil, a Alemanha.",
        ],
        examples=[
            GrammarExample(
                text="Sou espanhol.",
                note="masculino",
            ),
            GrammarExample(
                text="Ela é portuguesa.",
            ),
            GrammarExample(
                text="Nós somos franceses.",
                note="plural masculino",
            ),
            GrammarExample(
                text="Eles são brasileiros.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Estou português.",
                correct="Sou português.",
                note="A nacionalidade se apresenta com ser; isso não implica que nunca possa mudar.",
            ),
            GrammarMistake(
                wrong="Sou Portuguesa.",
                correct="Sou portuguesa.",
                note="Adjetivos de nacionalidade escrevem-se com minúscula.",
            ),
        ],
        related=[
            "ser",
            "genero-substantivos",
            "artigos-definidos",
        ],
    ),
    GrammarTopic(
        slug="genero-substantivos",
        title="Gênero dos substantivos",
        level="A1",
        category="Substantivos",
        summary="Regras gerais para identificar o gênero (masculino/feminino) dos substantivos.",
        explanation="Os substantivos têm gênero masculino ou feminino. Aprende cada nome com o artigo.\n\nAs terminações dão pistas, não garantias: -o é frequentemente masculino e -a feminino; -dade e -tude são habitualmente femininos. Muitos nomes em -gem são femininos (a viagem), mas personagem admite os dois gêneros.\n\nHá exceções: o dia, a mão, o problema, o sistema, o tema. Problema, sistema e tema têm origem grega; essa origem não explica dia ou mão.",
        rules=[
            "Substantivos em -o são geralmente masculinos; em -a, femininos.",
            "As terminações -dade e -tude são habitualmente femininas; em -gem, lembra a exceção o/a personagem.",
            "Problema, sistema e tema são masculinos; a origem grega e a terminação -ma não garantem o gênero: asma é feminino.",
            "O artigo definido indica o gênero: memorize o artigo com o substantivo.",
        ],
        examples=[
            GrammarExample(
                text="O carro vermelho.",
                note="masculino",
            ),
            GrammarExample(
                text="A casa branca.",
                note="feminino",
            ),
            GrammarExample(
                text="A cidade é bonita.",
                note="-dade, feminina",
            ),
            GrammarExample(
                text="O problema é difícil.",
                note="origem grega, masculino",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A problema.",
                correct="O problema.",
                note="Problema é masculino. Aprenda o artigo com a palavra, sem generalizar para todos os nomes em -ma.",
            ),
            GrammarMistake(
                wrong="O viagem.",
                correct="A viagem.",
                note="Viagem é feminino; a terminação -gem é uma pista, não uma regra sem exceções.",
            ),
        ],
        related=[
            "artigos-definidos",
            "artigos-indefinidos",
            "adjetivos-descritivos",
        ],
    ),
    GrammarTopic(
        slug="artigos-indefinidos",
        title="Artigos indefinidos",
        level="A1",
        category="Artigos",
        summary="Um, uma, uns, umas — artigos para substantivos não específicos.",
        explanation="| | Masculino | Feminino |\n|---|-----------|----------|\n| **Singular** | um | uma |\n| **Plural** | uns | umas |\n\nUsam-se para algo mencionado pela primeira vez, quantidade aproximada ou algo não específico.",
        rules=[
            "Usa-se um/uma para singular; uns/umas para plural indefinido.",
            "Uns/umas + numeral indica aproximação.",
            "Para indicar profissão, Sou professor é a forma neutra; Sou um professor também é possível conforme o contexto.",
        ],
        examples=[
            GrammarExample(
                text="Comprei um livro.",
            ),
            GrammarExample(
                text="Há uma árvore no jardim.",
            ),
            GrammarExample(
                text="Ela tem uns trinta anos.",
            ),
            GrammarExample(
                text="Umas pessoas estão à espera.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ela é um professora.",
                correct="Ela é uma professora.",
                note="Quando há artigo, ele concorda com o substantivo; o artigo não é proibido antes de profissão.",
            ),
            GrammarMistake(
                wrong="Um outra pessoa.",
                correct="Uma outra pessoa.",
                note="Artigo concorda com o substantivo que segue.",
            ),
        ],
        related=[
            "artigos-definidos",
            "genero-substantivos",
            "contracoes-preposicionais",
        ],
    ),
    GrammarTopic(
        slug="ter",
        title="Ter (Verbo)",
        level="A1",
        category="Verbos",
        summary="O verbo ter exprime posse, idade, existência e obrigação.",
        explanation="**Ter** é um verbo irregular e essencial. Usa-se para:\n\n- **Posse**: *Tenho um carro.*\n- **Idade**: *Tenho vinte e cinco anos.*\n- **Obrigação**: *Tenho de estudar.*\n- **Sensações**: *Tenho fome / sede / sono / medo.* No Brasil, também é muito comum usar **estar com**: *Estou com fome / sede / sono / frio / calor / medo / pressa.*\n\nConjugação: eu tenho / tu tens / ele-você tem / nós temos / eles-vocês têm",
        rules=[
            "Idade expressa-se com ter (NUNCA ser).",
            "Sensações admitem ter ou estar com: Tenho fome; Estou com fome. Estar exige com nessa construção.",
            "Ter de / ter que + infinitivo = obrigação.",
            "Na fala brasileira, ter substitui haver.",
        ],
        examples=[
            GrammarExample(
                text="Tenho dois irmãos.",
            ),
            GrammarExample(
                text="Ela tem vinte anos.",
                note="idade = ter",
            ),
            GrammarExample(
                text="Você está com fome?",
                note="sensação",
            ),
            GrammarExample(
                text="Tenho que ir ao médico.",
                note="obrigação",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Sou 25 anos.",
                correct="Tenho 25 anos.",
                note="Idade usa ter, nunca ser.",
            ),
            GrammarMistake(
                wrong="Estou fome.",
                correct="Tenho fome.",
                note="Estou fome não funciona sem a preposição: Estou com fome e Tenho fome são formas válidas.",
            ),
        ],
        related=[
            "haver",
            "querer-poder",
            "presente-regular",
        ],
    ),
    GrammarTopic(
        slug="adjetivos-possessivos",
        title="Possessivos e formas de posse",
        level="A1",
        category="Adjetivos e advérbios",
        summary="Concordar o possessivo com a coisa possuída e evitar ambiguidades.",
        explanation="Meu/minha, seu/sua e nosso/nossa concordam com o que é possuído: minha casa, meus livros. O artigo é opcional em muitos contextos: Minha casa e A minha casa. Seu pode indicar de você, dele ou dela; explicite o possuidor quando houver ambiguidade. Para a gente, é comum usar da gente: a casa da gente.",
        rules=[
            "Concorde com a coisa possuída, não com o possuidor.",
            "Use dele/dela/de vocês para esclarecer a posse.",
            "Não exija artigo antes de todo possessivo.",
        ],
        examples=[
            GrammarExample(
                text="Minha irmã chegou.",
            ),
            GrammarExample(
                text="O meu carro é azul.",
            ),
            GrammarExample(
                text="Este é o livro dela.",
            ),
            GrammarExample(
                text="A casa da gente fica perto.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Minha livros chegaram.",
                correct="Meus livros chegaram.",
                note="Livros é masculino plural.",
            ),
            GrammarMistake(
                wrong="Nosso casa é pequena.",
                correct="Nossa casa é pequena.",
                note="Casa é feminino singular.",
            ),
        ],
        related=[
            "artigos-definidos",
            "pronomes-objeto-direto",
            "pronomes-objeto-indireto",
        ],
    ),
    GrammarTopic(
        slug="adjetivos-descritivos",
        title="Adjetivos descritivos",
        level="A1",
        category="Adjetivos e advérbios",
        summary="Adjetivos que descrevem qualidades e concordam em gênero e número.",
        explanation="Os adjetivos em português concordam em gênero e número com o substantivo.\n\n**Adjetivos uniformes** têm a mesma forma nos dois gêneros: um homem inteligente / uma mulher inteligente; um rapaz ágil / uma moça ágil. Muitos terminam em -e, -l ou -ista, mas a terminação não basta: espanhol tem o feminino espanhola.\n\n**Posição:** Geralmente depois; antes pode mudar o sentido (*grande amigo* vs *amigo grande*).\n\n**Bom/mau** são irregulares: bom→boa, bons, boas; mau→má, maus, más.",
        rules=[
            "Adjetivos concordam em gênero e número com o substantivo.",
            "Grande, inteligente, ágil e egoísta são uniformes; espanhol/espanhola varia em gênero, apesar de terminar em -l.",
            "Posição normal: depois do substantivo.",
            "Bom/boa, mau/má são irregulares.",
        ],
        examples=[
            GrammarExample(
                text="Uma casa bonita.",
            ),
            GrammarExample(
                text="Um homem inteligente.",
                note="adjetivo uniforme",
            ),
            GrammarExample(
                text="Um grande escritor.",
                note="grande antes = qualidade",
            ),
            GrammarExample(
                text="As flores são bonitas.",
                note="concordância plural",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Umas flores bonito.",
                correct="Umas flores bonitas.",
                note="Adjetivo concorda em gênero e número.",
            ),
            GrammarMistake(
                wrong="Uma homem grande.",
                correct="Um homem grande.",
                note="Artigo e adjetivo devem concordar.",
            ),
        ],
        related=[
            "genero-substantivos",
            "comparativos",
            "superlativos",
        ],
    ),
    GrammarTopic(
        slug="presente-regular",
        title="Presente do indicativo (regulares)",
        level="A1",
        category="Tempos verbais",
        summary="Conjugação dos verbos regulares no presente em -ar, -er, -ir.",
        explanation="| | fal**ar** | com**er** | abr**ir** |\n|---|-----------|-----------|----------|\n| eu | falo | como | abro |\n| tu | falas | comes | abres |\n| ele/você | fala | come | abre |\n| nós | falamos | comemos | abrimos |\n| eles/vocês | falam | comem | abrem |",
        rules=[
            "-ar: -o, -as, -a, -amos, -am.",
            "-er: -o, -es, -e, -emos, -em.",
            "-ir: -o, -es, -e, -imos, -em.",
            "A conjugação nós é igual no presente e pretérito perfeito para -ar.",
        ],
        examples=[
            GrammarExample(
                text="Eu falo português todos os dias.",
            ),
            GrammarExample(
                text="Ela come fruta no almoço.",
            ),
            GrammarExample(
                text="Nós abrimos a loja às nove.",
            ),
            GrammarExample(
                text="Eles vendem livros usados.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eu falar português.",
                correct="Eu falo português.",
                note="O verbo deve ser conjugado.",
            ),
            GrammarMistake(
                wrong="Eles come muito.",
                correct="Eles comem muito.",
                note="Não se esqueça do -m no plural.",
            ),
        ],
        related=[
            "ser",
            "estar",
            "ter",
            "ir-futuro",
        ],
    ),
    GrammarTopic(
        slug="verbos-reflexivos",
        title="Verbos reflexivos e pronominais",
        level="A1",
        category="Verbos",
        summary="Usar me, te, se e nos em ações reflexivas.",
        explanation="O pronome reflexivo acompanha a pessoa: eu me levanto; você se levanta; nós nos levantamos; vocês se levantam. No Brasil, a próclise depois de sujeito expresso é muito natural: Eu me chamo Ana. Na conversa, também é comum iniciar a frase com o pronome: Me chamo Ana. A escrita formal tradicional evita esse início e admite Chamo-me Ana.\n\nNem todo verbo com pronome é literalmente reflexivo: lembrar-se de algo é pronominal. Também existe lembrar algo, com outra regência.",
        rules=[
            "Mantenha a concordância entre sujeito, pronome e verbo.",
            "Use próclise após negação: Não me lembro.",
            "Diferencie convenção escrita formal e uso conversacional.",
        ],
        examples=[
            GrammarExample(
                text="Eu me levanto às sete.",
            ),
            GrammarExample(
                text="Você se chama Ana?",
            ),
            GrammarExample(
                text="Nós nos encontramos amanhã.",
            ),
            GrammarExample(
                text="Não me lembro do endereço.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eu se levanto cedo.",
                correct="Eu me levanto cedo.",
                note="Eu corresponde a me.",
            ),
            GrammarMistake(
                wrong="Nós se levantamos.",
                correct="Nós nos levantamos.",
                note="Nós corresponde a nos.",
            ),
        ],
        related=[
            "colocacao-pronominal",
            "presente-regular",
            "pronomes-sujeito",
        ],
    ),
    GrammarTopic(
        slug="horas",
        title="As horas",
        level="A1",
        category="Substantivos",
        summary="Perguntar e dizer as horas no português brasileiro.",
        explanation="Para perguntar: *Que horas são?* / *Tem horas?* (coloquial)\n\nPara responder:\n- *É uma hora.* (1:00)\n- *São duas horas.* (2:00)\n- *São duas e um quarto.* (2:15)\n- *São duas e meia.* (2:30)\n- *São quinze para as três.* (2:45)\n- *É meio-dia./É meia-noite.*",
        rules=[
            "Usa-se o verbo ser para as horas.",
            "1:00, meio-dia e meia-noite usam singular.",
            "E um quarto = 15 min, e meia = 30 min.",
            "Depois da meia hora, são possíveis São três e cinquenta e São dez para as quatro.",
        ],
        examples=[
            GrammarExample(
                text="Que horas são?",
            ),
            GrammarExample(
                text="São três e um quarto.",
            ),
            GrammarExample(
                text="É meio-dia.",
            ),
            GrammarExample(
                text="São vinte para as seis.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Estão três horas.",
                correct="São três horas.",
                note="Horas usam ser, nunca estar.",
            ),
            GrammarMistake(
                wrong="São uma hora.",
                correct="É uma hora.",
                note="Uma hora exige singular; três e cinquenta e dez para as quatro são alternativas válidas.",
            ),
        ],
        related=[
            "ser",
            "dias-semana",
            "numeros-ordinais",
        ],
    ),
    GrammarTopic(
        slug="gostar-de",
        title="Gostar de",
        level="A1",
        category="Verbos",
        summary="Expressar gostos e preferências com a preposição de.",
        explanation="O verbo **gostar** exige sempre a preposição **de**:\n\n- *Gosto de café. / Gosto de cantar.*\n\nCom artigos, formam-se contrações: *Gosto do livro* (de+o), *Gosto da música* (de+a).",
        rules=[
            "Gostar exige sempre a preposição de.",
            "De + artigo = contração: do, da, dos, das.",
            "Com infinitivo: gostar de + verbo no infinitivo.",
            "Para preferência: gostar mais de... do que...",
        ],
        examples=[
            GrammarExample(
                text="Gosto de chocolate.",
            ),
            GrammarExample(
                text="Ela gosta do cinema português.",
                note="de+o=do",
            ),
            GrammarExample(
                text="Nós gostamos de viajar.",
            ),
            GrammarExample(
                text="Não gosto de acordar cedo.",
                note="negação",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gosto chocolate.",
                correct="Gosto de chocolate.",
                note="Gostar exige sempre a preposição de.",
            ),
            GrammarMistake(
                wrong="Gosto o livro.",
                correct="Gosto do livro.",
                note="de + o = do.",
            ),
        ],
        related=[
            "contracoes-preposicionais",
            "tambem-tampouco",
            "muito-pouco",
        ],
    ),
    GrammarTopic(
        slug="tambem-tampouco",
        title="Também e tampouco",
        level="A1",
        category="Adjetivos e advérbios",
        summary="Expressar concordância e discordância.",
        explanation="Também acrescenta uma informação ou concordância: Eu também gosto. Também não acrescenta uma negação: Não vi o filme; também não li o livro. Tampouco pode ter esse valor negativo, especialmente em escrita formal. O sujeito pode ficar implícito quando o contexto o identifica: Também não gosto é uma frase válida.",
        rules=[
            "Também usa-se em frases afirmativas.",
            "Tampouco é formal.",
            "Também não é a forma coloquial mais comum.",
            "Também pode ir antes ou depois do verbo.",
        ],
        examples=[
            GrammarExample(
                text="Eu também gosto de praia.",
            ),
            GrammarExample(
                text="Não vi o filme. — Eu também não.",
                note="coloquial",
            ),
            GrammarExample(
                text="Não fui à festa. — Eu tampouco.",
                note="formal",
            ),
            GrammarExample(
                text="Ela também quer ir.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eu também não gosta.",
                correct="Eu também não gosto.",
                note="O verbo concorda com eu. A omissão do sujeito é possível: Também não gosto.",
            ),
        ],
        related=[
            "muito-pouco",
            "gostar-de",
            "comparativos",
        ],
    ),
    GrammarTopic(
        slug="muito-pouco",
        title="Muito e pouco",
        level="A1",
        category="Adjetivos e advérbios",
        summary="Quantificadores que expressam quantidade ou intensidade.",
        explanation="**Muito** e **pouco** como adjetivos (variam): *Tenho muitos livros.* / Como advérbios (invariáveis): *Ela é muito bonita.*",
        rules=[
            "Como adjetivo, muito/pouco concordam em gênero e número.",
            "Como advérbio, muito/pouco são invariáveis.",
            "Muito antes de adjetivo/advérbio é invariável.",
            "Muito antes de substantivo varia.",
        ],
        examples=[
            GrammarExample(
                text="Tenho muito trabalho.",
            ),
            GrammarExample(
                text="Ela tem muitos amigos.",
            ),
            GrammarExample(
                text="Ele é muito alto.",
                note="invariável",
            ),
            GrammarExample(
                text="Há poucas pessoas na rua.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ela é muita bonita.",
                correct="Ela é muito bonita.",
                note="Antes de adjetivo, muito é invariável.",
            ),
            GrammarMistake(
                wrong="Tenho muito amigos.",
                correct="Tenho muitos amigos.",
                note="Antes de substantivo plural, varia.",
            ),
        ],
        related=[
            "tambem-tampouco",
            "adjetivos-descritivos",
            "comparativos",
        ],
    ),
    GrammarTopic(
        slug="haver",
        title="Haver e ter: existência",
        level="A1",
        category="Verbos",
        summary="Distinguir existência, posse e tempo decorrido.",
        explanation="Haver existencial é impessoal e fica no singular: Há vagas; Havia muitas pessoas; Houve problemas. Na conversa brasileira, ter também indica existência: Tem uma farmácia aqui perto. Em textos formais que seguem a norma-padrão tradicional, prefira haver ou existir.\n\nHá + duração indica tempo decorrido: Cheguei há duas horas. Ter também indica posse: Tenho um carro.",
        rules=[
            "Use haver no singular quando indicar existência.",
            "Reconheça ter existencial na fala brasileira sem o confundir com posse.",
            "Existir concorda com o sujeito: Existem vagas.",
        ],
        examples=[
            GrammarExample(
                text="Há duas vagas.",
            ),
            GrammarExample(
                text="Tem uma farmácia aqui perto?",
            ),
            GrammarExample(
                text="Existem várias soluções.",
            ),
            GrammarExample(
                text="Cheguei há três dias.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Houveram problemas.",
                correct="Houve problemas.",
                note="Haver existencial é impessoal.",
            ),
            GrammarMistake(
                wrong="Cheguei a dois dias.",
                correct="Cheguei há dois dias.",
                note="Tempo decorrido se escreve com há.",
            ),
        ],
        related=[
            "ter",
            "preposicoes-lugar",
        ],
    ),
    GrammarTopic(
        slug="preposicoes-lugar",
        title="Preposições de lugar",
        level="A1",
        category="Preposicoes",
        summary="Em, no, na, a, para, de — como indicar localização.",
        explanation="Em indica localização: Estou na cozinha. A e para podem indicar destino: Vou ao mercado; Vou para casa. De indica origem: Sou de Recife. Para localizar objetos, use também perto de, longe de, ao lado de, em frente a, atrás de e entre: O banco fica ao lado da farmácia.\n\nContrações frequentes: em + o = no; em + a = na; a + o = ao; de + o = do; por + a = pela. Ir no mercado é comum na conversa brasileira; em escrita formal tradicional, prefira ir ao mercado ou para o mercado.",
        rules=[
            "Em + artigo = no, na, nos, nas.",
            "Estar + em = localização estática.",
            "Ir + a/para = movimento.",
            "Use ir a ou ir para conforme o destino e o contexto: Vou ao mercado; Vou para casa.",
        ],
        examples=[
            GrammarExample(
                text="O livro está na mesa.",
            ),
            GrammarExample(
                text="Moro em Recife.",
            ),
            GrammarExample(
                text="Vou ao cinema.",
                note="a+o=ao",
            ),
            GrammarExample(
                text="Ela veio do Rio de Janeiro.",
                note="de+o=do",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Estou em o carro.",
                correct="Estou no carro.",
                note="em + o = no (contração obrigatória).",
            ),
            GrammarMistake(
                wrong="O banco fica ao lado a farmácia.",
                correct="O banco fica ao lado da farmácia.",
                note="Ao lado de exige de; de + a = da. Ir no supermercado é uma variante conversacional e não um erro universal.",
            ),
        ],
        related=[
            "contracoes-preposicionais",
            "estar",
            "ir-futuro",
        ],
    ),
    GrammarTopic(
        slug="contracoes-preposicionais",
        title="Contrações preposicionais",
        level="A1",
        category="Preposicoes",
        summary="Combinações obrigatórias de preposições com artigos e pronomes.",
        explanation="Quando preposição e artigo estão presentes na mesma construção, use as contrações: de + o/a/os/as = do/da/dos/das; em + o/a/os/as = no/na/nos/nas; por + o/a/os/as = pelo/pela/pelos/pelas. Com a: a + o/os = ao/aos; a + a/as = à/às.\n\nO acento grave marca a crase em Vou à escola, assim como se diz Vou ao mercado. Aparece também em expressões frequentes: à direita, à tarde, às duas horas. Não se coloca antes de qualquer palavra feminina: Vi a professora não tem preposição a; Vou a pé não tem artigo feminino.\n\nAntes de possessivos e nomes pessoais, o artigo pode variar: Falei de Ana e Falei da Ana; gosto de meu bairro e gosto do meu bairro. A contração depende da presença do artigo, não torna esse artigo obrigatório.",
        rules=[
            "As contrações são obrigatórias na escrita padrão.",
            "de+artigo=do, da, dos, das.",
            "em+artigo=no, na, nos, nas.",
            "a+o=ao; por+artigo=pelo, pela.",
        ],
        examples=[
            GrammarExample(
                text="O carro do meu pai.",
                note="de+o=do",
            ),
            GrammarExample(
                text="Ela está na escola.",
                note="em+a=na",
            ),
            GrammarExample(
                text="Vou ao médico amanhã.",
                note="a+o=ao",
            ),
            GrammarExample(
                text="Passeamos pela cidade.",
                note="por+a=pela",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="O livro de o Pedro.",
                correct="O livro do Pedro.",
                note="A contração é obrigatória.",
            ),
            GrammarMistake(
                wrong="Estou em a sala.",
                correct="Estou na sala.",
                note="em + a = na.",
            ),
        ],
        related=[
            "preposicoes-lugar",
            "artigos-definidos",
            "adjetivos-possessivos",
        ],
    ),
    GrammarTopic(
        slug="ir-futuro",
        title="Ir + infinitivo (futuro próximo)",
        level="A1",
        category="Tempos verbais",
        summary="Expressar planos e futuro próximo com ir + infinitivo.",
        explanation="O futuro próximo se forma com ir no presente + infinitivo: eu vou / você vai / nós vamos / vocês vão. Com tu, a norma-padrão usa vais.\n\nNa conversa brasileira, esta construção é muito frequente para planos e intenções: Vou estudar amanhã. O contexto também permite previsões: Vai chover.",
        rules=[
            "Ir no presente + verbo principal no infinitivo.",
            "Não se usa preposição entre ir e o infinitivo.",
            "Uso comum para planos e intenções próximas.",
            "No PB, o futuro simples é menos comum na fala.",
        ],
        examples=[
            GrammarExample(
                text="Vou visitar os meus pais no domingo.",
            ),
            GrammarExample(
                text="Ela vai começar um novo trabalho.",
            ),
            GrammarExample(
                text="Vamos viajar para a Bahia.",
            ),
            GrammarExample(
                text="O que você vai fazer amanhã?",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Vou a estudar.",
                correct="Vou estudar.",
                note="Não se usa preposição entre ir e o infinitivo.",
            ),
            GrammarMistake(
                wrong="Eu ir estudar.",
                correct="Eu vou estudar.",
                note="O verbo ir deve ser conjugado.",
            ),
        ],
        related=[
            "presente-regular",
            "querer-poder",
            "futuro-do-presente",
        ],
    ),
    GrammarTopic(
        slug="querer-poder",
        title="Querer e poder",
        level="A1",
        category="Verbos",
        summary="Verbos irregulares que expressam desejo e capacidade.",
        explanation="**Querer**: eu quero / tu queres / ele-você quer / nós queremos / eles-vocês querem\n**Poder**: eu posso / tu podes / ele-você pode / nós podemos / eles-vocês podem",
        rules=[
            "Querer e Poder são irregulares na 1.ª pessoa (quero, posso).",
            "Querer + infinitivo = desejo.",
            "Poder + infinitivo = capacidade ou permissão.",
            "No PB, ser capaz de é alternativa a poder.",
        ],
        examples=[
            GrammarExample(
                text="Quero uma passagem para Salvador.",
            ),
            GrammarExample(
                text="Você pode me ajudar?",
                note="pedido cotidiano com você",
            ),
            GrammarExample(
                text="Não posso sair hoje.",
            ),
            GrammarExample(
                text="Ela quer ser médica.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eu podo falar inglês.",
                correct="Eu posso falar inglês.",
                note="Poder→eu posso, não podo.",
            ),
            GrammarMistake(
                wrong="Você pode ajuda?",
                correct="Você pode ajudar?",
                note="Depois de poder, use o infinitivo para indicar a ação.",
            ),
        ],
        related=[
            "presente-regular",
            "gostar-de",
            "ir-futuro",
            "presente-conjuntivo",
        ],
    ),
    GrammarTopic(
        slug="dias-semana",
        title="Dias da semana",
        level="A1",
        category="Substantivos",
        summary="Os dias da semana e como usá-los com artigos e preposições.",
        explanation="Dias da semana: segunda-feira, terça-feira, quarta-feira, quinta-feira, sexta-feira, sábado, domingo.\n\nNotas:\n- Dias úteis terminam em -feira.\n- Na fala, omite-se -feira: *na segunda, na terça*.\n- Com artigos: *na segunda-feira* (em+a); *no sábado* (em+o).",
        rules=[
            "Dias podem usar-se com ou sem artigo.",
            "Com artigo: na segunda-feira.",
            "A reunião é segunda-feira e A reunião é na segunda-feira são formas correntes, sem oposição obrigatória de formalidade.",
            "Na fala, omite-se -feira.",
            "Sábado e domingo usam artigo masculino.",
        ],
        examples=[
            GrammarExample(
                text="A aula é na terça-feira.",
            ),
            GrammarExample(
                text="No sábado vou à praia.",
            ),
            GrammarExample(
                text="O restaurante fecha às segundas-feiras.",
                note="hábito semanal; na segunda-feira pode indicar uma ocasião específica",
            ),
            GrammarExample(
                text="Que dia é hoje? Hoje é quinta.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="No segunda-feira.",
                correct="Na segunda-feira.",
                note="Segunda-feira é feminino: na, não no.",
            ),
            GrammarMistake(
                wrong="A reunião é em segunda.",
                correct="A reunião é na segunda.",
                note="em+a=na.",
            ),
        ],
        related=[
            "horas",
            "preposicoes-lugar",
            "contracoes-preposicionais",
        ],
    ),
    GrammarTopic(
        slug="estar-gerundio",
        title="Estar + gerúndio",
        level="A1",
        category="Tempos verbais",
        summary="Expressar ações em andamento no português brasileiro.",
        explanation="A perífrase estar + gerúndio apresenta uma ação em curso: Estou lendo; Ela está trabalhando. Forme o gerúndio substituindo -ar por -ando, -er por -endo e -ir por -indo: falar → falando; comer → comendo; partir → partindo. Irregular frequente: pôr → pondo.\n\nO presente simples indica um hábito (Estudo todos os dias); o progressivo situa uma ação em andamento (Estou estudando agora). Estava lendo apresenta uma ação em curso no passado. Estar a + infinitivo é característico de muitos usos portugueses e não é o modelo principal deste curso.",
        rules=[
            "Conjugue estar e mantenha o gerúndio invariável.",
            "Use -ando, -endo e -indo conforme a conjugação.",
            "Diferencie hábito de ação em andamento.",
        ],
        examples=[
            GrammarExample(
                text="Estou trabalhando agora.",
            ),
            GrammarExample(
                text="Você está ouvindo música?",
            ),
            GrammarExample(
                text="Estamos lendo um livro.",
            ),
            GrammarExample(
                text="Ela estava dormindo quando liguei.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Estou a estudando.",
                correct="Estou estudando.",
                note="Não misture as duas construções regionais.",
            ),
            GrammarMistake(
                wrong="Estamos trabalham.",
                correct="Estamos trabalhando.",
                note="Depois de estar, use gerúndio na perífrase progressiva.",
            ),
        ],
        related=[
            "estar",
            "andar-estar-gerundio",
        ],
    ),
    GrammarTopic(
        slug="demonstrativos",
        title="Os demonstrativos: este, esse, aquele",
        level="A1",
        category="Adjetivos e advérbios",
        summary="Uso dos pronomes e adjetivos demonstrativos para indicar a posição de algo em relação às pessoas do discurso.",
        explanation="Os demonstrativos situam pessoas, objetos e ideias. Na distinção tradicional, este se aproxima de quem fala, esse de quem ouve e aquele indica distância de ambos. Na conversa brasileira, esse e este nem sempre mantêm essa oposição; isso é uma variação de uso, não um erro automático.\n\nConcorde em gênero e número: este livro, estas casas, aqueles prédios. Isto, isso e aquilo retomam ideias ou objetos sem nomeá-los: Isso que você disse é importante.\n\nUse contrações quando necessário: em + este = neste; de + esse = desse; a + aquele = àquele. Em textos formais, os demonstrativos também organizam referências ao que já foi dito ou ao que será apresentado.",
        structure="este/esta/estes/estas (perto de quem fala) · esse/essa/esses/essas (perto de quem ouve) · aquele/aquela/aqueles/aquelas (longe) · isto/isso/aquilo (neutro)",
        rules=[
            '"Este/esta" indica o que está perto de quem fala (aqui).',
            '"Esse/essa" indica o que está perto de quem ouve (aí).',
            '"Aquele/aquela" indica o que está longe de ambos (ali/acolá).',
            "As formas neutras (isto, isso, aquilo) referem-se a ideias ou objetos não nomeados.",
            "Contraem-se com as preposições em e de: neste, desse, naquele, desta, daquela.",
        ],
        examples=[
            GrammarExample(
                text="Este livro é muito interessante.",
                note="perto de quem fala",
            ),
            GrammarExample(
                text="Essa mochila que você tem aí é nova?",
                note="perto de quem ouve",
            ),
            GrammarExample(
                text="Aquele senhor ali é o meu avô.",
                note="longe de ambos",
            ),
            GrammarExample(
                text="O que é isto?",
                note="forma neutra",
            ),
            GrammarExample(
                text="Neste momento não posso falar.",
                note="contração em+este",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A este casa é bonita.",
                correct="Esta casa é bonita.",
                note="O demonstrativo não leva artigo.",
            ),
            GrammarMistake(
                wrong="Aquilo livro é meu.",
                correct="Aquele livro é meu.",
                note='"Aquilo" é a forma neutra; para acompanhar "livro" usa-se "aquele".',
            ),
        ],
        related=[
            "adjetivos-descritivos",
            "adjetivos-possessivos",
            "artigos-definidos",
        ],
    ),
    GrammarTopic(
        slug="numeros-ordinais",
        title="Números ordinais",
        level="A1",
        category="Adjetivos e advérbios",
        summary="Formação e uso dos números ordinais em português.",
        explanation="Os **números ordinais** indicam a ordem ou posição numa sequência.\n\n- 1.º — primeiro/primeira\n- 2.º — segundo/segunda\n- 3.º — terceiro/terceira\n- 4.º — quarto/quarta\n- 5.º — quinto/quinta\n- 6.º — sexto/sexta\n- 7.º — sétimo/sétima\n- 8.º — oitavo/oitava\n- 9.º — nono/nona\n- 10.º — décimo/décima\n\nFrequentemente vêm **antes do nome**: *o primeiro dia, a segunda aula, o terceiro andar*. Também podem vir depois: *capítulo primeiro*.\n\nApós nomes de reis e papas, a leitura convencional usa ordinais até dez e cardinais a partir de onze: *Dom Pedro II (segundo), Luís XIV (quatorze)*.\n\n**Abreviam-se** com ponto abreviativo e indicador de gênero:\n- 1.º (primeiro), 1.ª (primeira)\n- 2.º, 2.ª, etc.\n\nPara perguntar a posição: *Em que lugar você ficou? — Fiquei em terceiro.*",
        structure="primeiro · segundo · terceiro · quarto · quinto · sexto · sétimo · oitavo · nono · décimo",
        rules=[
            "Os ordinais concordam em gênero com o nome: primeiro/primeira, segundo/segunda.",
            "A posição antes do nome é frequente, mas não obrigatória: o primeiro capítulo; capítulo primeiro.",
            "Abreviam-se com .º (masculino) e .ª (feminino).",
            "Use o terceiro andar para indicar posição; após nomes de reis e papas, leia ordinais até dez e cardinais a partir de onze.",
        ],
        examples=[
            GrammarExample(
                text="Moro no terceiro andar.",
                note="ordinal antes do nome",
            ),
            GrammarExample(
                text="É a primeira vez que visito o Brasil.",
                note="primeira (feminino)",
            ),
            GrammarExample(
                text="Ficou em segundo lugar na corrida.",
                note="posição",
            ),
            GrammarExample(
                text="Esta é a 15.ª edição do festival.",
                note="abreviatura",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Dom Pedro II (dois).",
                correct="Dom Pedro II (segundo).",
                note="Na leitura convencional de nomes de reis, use ordinal até dez; a partir de onze, use cardinal: Luís XIV (quatorze).",
            ),
            GrammarMistake(
                wrong="É a primeiro vez.",
                correct="É a primeira vez.",
                note='"Vez" é feminino → primeira.',
            ),
        ],
        related=[
            "horas",
            "dias-semana",
        ],
    ),
    GrammarTopic(
        slug="perguntas-basicas",
        title="Perguntas do dia a dia",
        level="A1",
        category="Orações",
        summary="Pedir informações com quem, o que, onde, quando, como, quanto e por que.",
        explanation="Uma pergunta de sim ou não pode conservar a ordem da afirmação: Você mora aqui. → Você mora aqui? Na fala, a entoação ajuda a indicar a pergunta; na escrita, use ?. Não acrescente um auxiliar como do do inglês.\n\nQuem pergunta por pessoas; o que, por coisas ou ações; onde, por lugar; de onde, por origem; quando, por tempo; como, por modo ou estado; quanto, por quantidade ou preço. Quanto concorda quando acompanha um nome: Quantos livros? Quantas pessoas?\n\nUse por que para perguntar a razão e porque para responder: Por que você estuda português? Porque trabalho no Brasil. No fim da pergunta, escreva por quê: Você saiu por quê? O substantivo o porquê significa o motivo. As formas é que e cadê aparecem na conversa: Onde é que você mora? Cadê a chave?",
        rules=[
            "Mantenha a concordância do verbo: Onde você mora? Onde vocês moram?",
            "Use de onde para origem e onde para localização.",
            "Distinga a pergunta por que da resposta porque; use por quê no fim da pergunta.",
            "Quanto/quantos/quantas acompanha o nome; Quanto custa? pergunta o preço.",
        ],
        examples=[
            GrammarExample(text="Como você se chama?"),
            GrammarExample(text="De onde vocês são?"),
            GrammarExample(text="Quando começa a aula?"),
            GrammarExample(text="Quantas pessoas moram aqui?"),
            GrammarExample(text="Por que você está aqui? Porque tenho uma reunião."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Onde você moram?", correct="Onde você mora?", note="Você exige singular."
            ),
            GrammarMistake(
                wrong="Quantos pessoas vieram?",
                correct="Quantas pessoas vieram?",
                note="Pessoas é feminino plural.",
            ),
        ],
        related=["pronomes-sujeito", "negacao-basica", "preposicoes-lugar"],
    ),
    GrammarTopic(
        slug="negacao-basica",
        title="Não, nunca, nada e ninguém",
        level="A1",
        category="Orações",
        summary="Negar ações e indicar ausência sem copiar a estrutura de outra língua.",
        explanation="A negação básica usa não antes do verbo: Eu não moro aqui; Ela não gosta de café. Com mais de um verbo, não normalmente precede o primeiro: Não posso sair; Não estou trabalhando.\n\nNunca indica ausência de ocorrências; nada, ausência de coisas; ninguém, ausência de pessoas. Antes do verbo, essas palavras já podem negar a oração: Nunca viajo; Ninguém chegou; Nada mudou. Depois do verbo, combine com não ou outra expressão negativa: Não viajo nunca; Não vi ninguém; Não quero nada. Essa combinação é normal em português e não transforma a frase em afirmação.\n\nNa conversa brasileira, também se ouve Não quero, não e Sei não. Reconheça essas construções; pratique primeiro não antes do verbo. Não confunda nada com ninguém: Não comprei nada; Não conheço ninguém aqui.",
        rules=[
            "Coloque não antes do verbo na construção básica.",
            "Nunca, nada e ninguém antes do verbo não exigem outro não.",
            "Depois do verbo, use concordância negativa: Não vi ninguém.",
            "Na negação com pronome, use Não me lembro, não Não lembro-me.",
        ],
        examples=[
            GrammarExample(text="Eu não trabalho aos domingos."),
            GrammarExample(text="Nunca tomo café à noite."),
            GrammarExample(text="Não quero nada, obrigado."),
            GrammarExample(text="Ninguém chegou ainda."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eu não gosta de café.",
                correct="Eu não gosto de café.",
                note="A negação não muda a concordância com eu.",
            ),
            GrammarMistake(
                wrong="Não conheço nada nesta cidade. (referindo-se a pessoas)",
                correct="Não conheço ninguém nesta cidade.",
                note="Ninguém retoma pessoas; nada retoma coisas ou situações.",
            ),
        ],
        related=["perguntas-basicas", "tambem-tampouco", "verbos-reflexivos"],
    ),
    GrammarTopic(
        slug="plural-substantivos",
        title="Plural dos substantivos e concordância",
        level="A1",
        category="Substantivos",
        summary="Formar plurais frequentes e concordar artigos e adjetivos.",
        explanation="Em palavras terminadas em vogal, normalmente acrescente -s: casa/casas, livro/livros, café/cafés. Em -r e -z, acrescente -es: mulher/mulheres, luz/luzes. Em -m, troque por -ns: homem/homens, jardim/jardins.\n\nEm -al, -el, -ol e -ul, são frequentes -ais, -éis, -óis e -uis: animal/animais, papel/papéis, farol/faróis, azul/azuis. Há exceções, como mal/males. Em -il, compare a sílaba tônica: funil/funis, mas fácil/fáceis.\n\nPalavras em -ão têm plurais diferentes, que devem ser aprendidos com cada nome: coração/corações, pão/pães, mão/mãos. Não basta trocar todo -ão por -ões. Algumas admitem mais de uma forma. Em -s, observe o acento tônico: mês/meses, país/países, mas lápis/lápis e ônibus/ônibus.\n\nNa escrita padrão, marque também o plural nos determinantes e adjetivos: os meus livros novos, duas mulheres brasileiras. Há variação de concordância na fala; o modelo escrito ensinado mantém todas as marcas.",
        rules=[
            "Aprenda artigo, singular e plural juntos, sobretudo nas terminações -ão e -s.",
            "Troque -m por -ns: um homem, dois homens.",
            "Conserve os acentos necessários: papel/papéis, país/países.",
            "Concorde artigo, nome e adjetivo na escrita padrão.",
        ],
        examples=[
            GrammarExample(text="As casas são pequenas."),
            GrammarExample(text="Comprei dois pães e três cafés."),
            GrammarExample(text="Os homens trouxeram os papéis."),
            GrammarExample(text="Os ônibus passam perto dos jardins."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Dois pãoes.", correct="Dois pães.", note="O plural de pão é pães."
            ),
            GrammarMistake(
                wrong="Três homems.", correct="Três homens.", note="A terminação -m passa a -ns."
            ),
        ],
        related=["genero-substantivos", "adjetivos-descritivos", "artigos-definidos"],
    ),
    GrammarTopic(
        slug="verbos-frequentes-presente",
        title="Verbos frequentes no presente",
        level="A1",
        category="Verbos",
        summary="Usar fazer, vir, ver, saber e dizer em situações cotidianas.",
        explanation="Alguns verbos frequentes não seguem apenas o modelo regular. Pratique com eu; você/ele/ela; nós; vocês/eles/elas:\n\n- fazer: faço, faz, fazemos, fazem;\n- vir: venho, vem, vimos, vêm;\n- ver: vejo, vê, vemos, veem;\n- saber: sei, sabe, sabemos, sabem;\n- dizer: digo, diz, dizemos, dizem.\n\nVocê usa a terceira pessoa; a gente também: A gente faz o almoço. Nas variedades que usam tu, a norma-padrão traz fazes, vens, vês, sabes e dizes; a concordância oral varia regionalmente.\n\nCompare Nós vimos de Recife (vir no presente) e Nós vemos o mar (ver no presente). Vocês vêm indica movimento para cá; vocês veem indica percepção visual. Saber + infinitivo indica uma habilidade: Sei nadar; conhecer indica familiaridade: Conheço esta cidade.",
        rules=[
            "Memorize a primeira pessoa com um exemplo: faço o almoço, venho de ônibus, vejo o mar, sei nadar, digo a verdade.",
            "Diferencie vem/vêm (vir) de vê/veem (ver), inclusive na escrita.",
            "Com você e a gente, use a terceira pessoa do singular.",
        ],
        examples=[
            GrammarExample(text="O que você faz de manhã?"),
            GrammarExample(text="Eu venho de ônibus e ela vem de bicicleta."),
            GrammarExample(text="Nós vemos nossos amigos aos sábados."),
            GrammarExample(text="Não sei o endereço, mas conheço o bairro."),
            GrammarExample(text="Ela diz que mora aqui."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eu faz o almoço.",
                correct="Eu faço o almoço.",
                note="Fazer tem a forma faço com eu.",
            ),
            GrammarMistake(
                wrong="Eles vê o mar.",
                correct="Eles veem o mar.",
                note="O plural de vê é veem, sem acento; vêm pertence a vir.",
            ),
        ],
        related=["presente-regular", "perguntas-basicas", "negacao-basica"],
    ),
    GrammarTopic(
        slug="pronuncia-ortografia-basica",
        title="Sons, sílaba tônica e escrita",
        level="A1",
        category="Pronúncia e ortografia",
        summary="Relacionar sons e grafias frequentes sem impor um único sotaque brasileiro.",
        explanation="Toda palavra tem uma organização sonora; nas palavras tônicas, uma sílaba se destaca. O acento gráfico nem sempre aparece: casa tem força em ca; café tem força em fé. Compare avó e avô: o acento ajuda a distinguir vogais abertas e fechadas nessas palavras.\n\nO til indica nasalidade em mãe, pão e põe; não é um acento de intensidade. M ou n no fim de sílaba também pode indicar nasalidade, como em campo e canto. Compare oralidade e nasalidade ouvindo pares como lá/lã.\n\nNh e lh representam sons diferentes de n e l: ninho, filho. Ç tem som de s e ocorre antes de a, o ou u: açúcar, almoço. C antes de e/i também pode ter som de s: cedo, cidade. Compare caro/carro e casa/caça; uma letra ou dígrafo pode distinguir palavras.\n\nNo Brasil, a realização de r e s e a pronúncia de t/d antes de som de i variam conforme a região. Dia pode começar com um som de d ou com uma realização africada; ambas pertencem a variedades brasileiras. Busque inteligibilidade, ritmo e contrastes de significado, sem tratar um sotaque regional como o único correto.",
        rules=[
            "Aprenda a sílaba tônica junto com a palavra, sem pressupor que toda sílaba tônica tenha acento gráfico.",
            "Conserve til, cedilha e acentos na escrita: pão, açúcar, café.",
            "Distinga caro/carro e casa/caça pelo som e pela grafia.",
            "Reconheça variação regional de pronúncia sem confundi-la com erro.",
        ],
        examples=[
            GrammarExample(
                text="Minha avó e meu avô moram aqui.", note="avó tem ó aberto; avô tem ô fechado"
            ),
            GrammarExample(text="O pão está na mesa.", note="ão é um ditongo nasal"),
            GrammarExample(text="Meu filho encontrou um ninho.", note="contraste entre lh e nh"),
            GrammarExample(text="O carro é caro.", note="contraste entre rr e r entre vogais"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quero um cafe sem acucar.",
                correct="Quero um café sem açúcar.",
                note="Na escrita padrão, conserve os acentos e a cedilha.",
            ),
            GrammarMistake(
                wrong="Todo brasileiro pronuncia o r do mesmo jeito.",
                correct="A pronúncia do r varia entre regiões e contextos.",
                note="A diversidade de sotaques faz parte do português brasileiro.",
            ),
        ],
        related=["plural-substantivos", "pronomes-sujeito"],
    ),
]
