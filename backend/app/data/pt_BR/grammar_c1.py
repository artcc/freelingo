"""Brazilian Portuguese (grammar_c1) learning content."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="subjuntivo-concessivo",
        title="Subjuntivo em orações concessivas",
        level="C1",
        category="Subjuntivo",
        summary="Uso avançado do subjuntivo em orações concessivas.",
        explanation="Uma concessiva apresenta uma circunstância que não impede a conclusão. Embora e ainda que podem conceder um fato (Embora tenha estudado, não passou); mesmo que pode introduzir uma hipótese (Mesmo que chova, iremos). Por mais que destaca um esforço ou grau insuficiente para alterar o resultado: Por mais que explique, a dúvida permanece. Escolha o tempo pela relação temporal e pela perspectiva: Embora esteja cansada, continuará; Embora estivesse cansada, continuou.",
        rules=[
            "Por mais/muito que + subjuntivo.",
            "Ainda que/mesmo que + subjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Por mais que você tente, nem sempre vai conseguir.",
            ),
            GrammarExample(
                text="Mesmo que me pagassem, não faria esse trabalho.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Por mais que você tenta, a dúvida continua.",
                correct="Por mais que você tente, a dúvida continua.",
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
        explanation="Para que e a fim de que introduzem finalidade com subjuntivo: Enviei os dados para que a equipe possa decidir. O presente ou o imperfeito depende da perspectiva: Enviei os dados para que a equipe pudesse decidir situa a finalidade no passado. Com o mesmo sujeito, para + infinitivo costuma ser mais econômico (Estudo para aprender), mas para que eu aprenda também é possível. O infinitivo pessoal pode ter sujeito próprio: Preparei a sala para eles estudarem.",
        rules=[
            "Para que e a fim de que usam subjuntivo para exprimir finalidade.",
            "Não reduza a escolha a sujeitos iguais ou diferentes; considere construção, ênfase e referência temporal.",
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
        explanation="O modo indica como o falante apresenta o referente, não apenas se ele é conhecido. Procuro uma revisora que conheça o tema descreve um perfil desejado, sem afirmar que alguém o satisfaça. Procuro a revisora que conhece o tema apresenta essa competência como um fato. Até um antecedente definido admite subjuntivo em contexto hipotético: Contrataremos o candidato que apresentar a melhor proposta. Há quem discorde e Não há quem resolva isso são construções frequentes com subjuntivo.",
        rules=[
            "Subjuntivo: propriedade desejada, hipotética ou não afirmada como fato.",
            "Indicativo: propriedade apresentada como factual; o contexto determina a interpretação.",
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
        explanation="Na passiva sintética, se acompanha um verbo transitivo e o verbo concorda com o sujeito paciente: Publicam-se os resultados equivale a Os resultados são publicados. Uma oração inteira pode funcionar como sujeito: Comenta-se que haverá mudanças. Não confunda esse se com o de Precisa-se de revisores: com a preposição exigida por precisar, o sujeito é indeterminado e o verbo fica no singular na norma-padrão. A mesóclise em Realizar-se-á a reunião é uma opção marcada da escrita formal, não uma exigência de todo texto acadêmico.",
        rules=[
            "Na passiva sintética, concorde o verbo com o sujeito paciente: Publica-se o texto; Publicam-se os textos.",
            "Distinga passiva de indeterminação do sujeito pela construção e pela regência verbal.",
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
        explanation="A nominalização transforma uma ação ou propriedade em nome: implementar -> implementação; construir -> construção; claro -> clareza. Ela permite retomar processos, mas pode ocultar responsáveis e relações temporais. Compare A equipe revisou o texto antes de publicar com A revisão do texto pela equipe precedeu a publicação. A segunda versão preserva agente e ordem dos fatos; uma cadeia como realização da implementação da revisão pode obscurecê-los. Simplifique sem apagar etapas nem acrescentar participantes.",
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
                wrong="A revisão dos dados pelos pesquisadores foram concluídas ontem.",
                correct="A revisão dos dados pelos pesquisadores foi concluída ontem.",
                note="O núcleo do sujeito é revisão, não pesquisadores. A nominalização mantém explícito quem revisou os dados.",
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
        explanation="A impessoalidade desloca o foco de quem escreve para processos, resultados ou argumentos. Compare Nós observamos um aumento com Foi observado um aumento: a segunda versão omite o observador, mas não torna a observação automaticamente objetiva. Quando a autoria importa, explicite-a: A equipe observou um aumento.\n\nUse construções impessoais como Convém destacar o limite da amostra e É necessário verificar os dados. Distinga se passivo (Analisaram-se os resultados, com concordância) de sujeito indeterminado (Precisa-se de dados adicionais, no singular na norma-padrão).\n\nA nominalização pode condensar um processo (a análise dos dados), mas sequências longas escondem agentes e ações. Primeira pessoa é aceita em vários gêneros acadêmicos; escolha conforme a área e mantenha coerência. Não apague responsabilidades, fontes ou limites de evidência para produzir um tom aparentemente neutro.",
        rules=[
            "Escolha entre voz ativa, passiva e construção impessoal conforme o foco e a necessidade de identificar o agente.",
            "Diferencie concordância da passiva sintética e singular de sujeito indeterminado.",
            "Não confunda ausência de primeira pessoa com ausência de opinião ou viés.",
        ],
        examples=[
            GrammarExample(
                text="Foi observado um aumento significativo.",
            ),
            GrammarExample(
                text="A equipe observou um aumento, mas os dados não permitem atribuí-lo à intervenção."
            ),
            GrammarExample(text="Convém explicitar os critérios antes da análise."),
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
        explanation="Um campo semântico reúne palavras relacionadas a um domínio, como justiça: tribunal, juiz, réu, sentença, julgar, condenar e absolver. Pertencer ao mesmo campo não torna as palavras sinônimas: o juiz profere a sentença, enquanto a defesa apresenta argumentos. Observe as combinações usuais e o papel de cada participante. Uma troca lexical inadequada pode mudar a ação ou atribuí-la à pessoa errada.",
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
                wrong="O réu proferiu a sentença que o absolveu.",
                correct="O juiz proferiu a sentença que absolveu o réu.",
                note="No contexto de um julgamento, proferir a sentença cabe ao juiz; a correção distingue os papéis jurídicos.",
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
        explanation="Prefixos podem alterar o sentido de uma base: refazer indica repetição; infeliz nega uma propriedade; desfazer pode indicar reversão. Sufixos também mudam classe e sentido: organizar -> organização; feliz -> felicidade; lavar -> lavável. A formação não é totalmente livre: infelicidade é a forma estabelecida, não desfelicidade. Palavras derivadas da mesma base podem ter usos distintos: clareza de uma explicação e claridade da sala. Compare padrões produtivos com palavras já lexicalizadas antes de criar uma forma nova.",
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
        explanation="Precisão lexical depende do sentido, da construção e da combinação entre palavras, não de trocar toda palavra simples por uma rara. Dizer tende a introduzir uma informação (Disse que voltaria); falar pode indicar interação ou língua (Falou com Ana; Fala português). Há sobreposição em certos contextos: Falou que voltaria é corrente no Brasil, não um erro automático.\n\nVer pode apresentar percepção ou resultado; olhar destaca a orientação da atenção: Olhei para o painel, mas não vi o aviso. Ouvir e escutar também se sobrepõem no uso; escutar pode destacar atenção deliberada, mas não existe uma separação absoluta em toda frase. Saber pode indicar conhecimento ou habilidade (Sei nadar); conhecer, familiaridade (Conheço a pesquisadora). Conheço a resposta e Sei a resposta são ambas possíveis.\n\nEm texto profissional, preserve o grau de evidência: sugerir uma relação não equivale a demonstrar uma relação; contestar uma hipótese não significa refutá-la. Confira colocações: formular uma hipótese, apresentar uma proposta, exercer uma função. Compare claro (compreensível) e preciso (bem delimitado): um texto pode ser claro sem ser tecnicamente preciso.\n\nAo substituir um termo, mantenha agente, regência, intensidade e campo de uso. Um sinônimo de dicionário pode alterar a conclusão ou o registro no contexto.",
        rules=[
            "Escolha o verbo com seus complementos e colocações, reconhecendo sobreposições legítimas.",
            "Não transforme indício em prova: sugerir, indicar, demonstrar e comprovar têm compromissos diferentes.",
            "Prefira precisão contextual a palavras rebuscadas ou substituições automáticas por sinônimos.",
        ],
        examples=[
            GrammarExample(
                text="Sei a resposta. / Conheço bem essa pessoa.",
            ),
            GrammarExample(text="Olhei para a tela, mas não vi a mensagem."),
            GrammarExample(
                text="Os dados sugerem uma associação; ainda não demonstram causalidade."
            ),
            GrammarExample(
                text="A comissão contestou a hipótese, mas não apresentou evidência para refutá-la."
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Conheço nadar.",
                correct="Sei nadar.",
                note="Saber + infinitivo exprime uma capacidade. Conheço a resposta e Sei a resposta são ambas construções válidas.",
            ),
            GrammarMistake(
                wrong="Original: Os dados sugerem uma relação. Revisão: Os dados comprovam uma relação.",
                correct="Os dados sugerem uma relação.",
                note="A substituição muda o grau de evidência; comprovar não preserva o sentido de sugerir.",
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
                note="irônico, se o contexto indicar descrença",
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
        explanation="A ambiguidade lexical explora sentidos diferentes de uma palavra: banco pode designar assento ou instituição financeira. A sintática permite relações diferentes entre os mesmos termos: Vi o homem com os binóculos pode indicar o instrumento da observação ou uma característica do homem. Humor e publicidade podem explorar essas leituras; em instruções e documentos, explicite o referente quando a ambiguidade comprometer a ação esperada.",
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
                wrong="Ana informou a Carla que seu pedido foi aceito.",
                correct="Ana informou a Carla que o pedido de Carla foi aceito.",
                note="Se o pedido é de Carla, a reformulação elimina a ambiguidade de seu. A frase original é gramatical, mas pode ser insuficiente sem contexto.",
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
        explanation="A pergunta retórica orienta uma conclusão sem pedir informação: Quem nunca errou? A anáfora repete um início para dar ênfase: Queremos acesso, queremos respeito, queremos participação. A epífora repete o final: Estudamos por justiça, trabalhamos por justiça, lutamos por justiça. O quiasmo inverte elementos em uma estrutura cruzada: Não vivemos para trabalhar; trabalhamos para viver.\n\nA gradação organiza intensidade: Pediu, insistiu, implorou. A antítese aproxima ideias opostas: Uns acumulam, outros carecem. O paradoxo combina ideias aparentemente incompatíveis para provocar reflexão: Quanto mais aprende, mais percebe o que não sabe.\n\nIdentifique o efeito no argumento, não apenas o nome da figura. A repetição pode criar solidariedade ou soar mecânica; uma pergunta retórica pode convidar à reflexão ou constranger o público. Escolha o recurso conforme a situação e não o use como substituto de evidência.",
        rules=[
            "Relacione a repetição, a oposição ou a pergunta à intenção e ao público.",
            "Uma figura pode reforçar um argumento, mas não substitui a evidência.",
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
                wrong="Em Quem nunca errou?, o orador pede uma lista de pessoas infalíveis.",
                correct="Em um discurso que defende tolerância, Quem nunca errou? sugere que todos cometem erros.",
                note="A leitura retórica depende do contexto; aqui a pergunta favorece uma conclusão compartilhada.",
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
        explanation="Ethos constrói credibilidade, pathos mobiliza emoções e logos organiza razões e evidências. Uma médica pode mencionar sua experiência (ethos), descrever o impacto de uma doença nas famílias (pathos) e apresentar dados de prevenção (logos). Nenhum recurso garante por si só a verdade da conclusão. Avalie se a autoridade é pertinente, se a emoção é relevante e se os dados sustentam a inferência, adaptando a linguagem ao público.",
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
                wrong="A campanha comoveu o público; portanto, sua proposta é eficaz.",
                correct="A campanha comoveu o público; sua eficácia precisa ser avaliada por resultados.",
                note="Uma reação emocional não demonstra a eficácia da proposta.",
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
        explanation="A metáfora transfere sentido por semelhança: A vida é uma viagem. A comparação explicita a aproximação: A vida é como uma viagem. A metonímia relaciona elementos associados: Li Machado de Assis significa li uma obra dele. A sinédoque, frequentemente tratada como tipo de metonímia, usa parte pelo todo: Precisamos de mais braços para o trabalho. A personificação atribui ações humanas a outros seres ou objetos (A cidade acordou); a hipérbole exagera para produzir efeito (Esperei uma eternidade). A interpretação depende do contexto.",
        rules=[
            "Metáfora, metonímia.",
            "Personificação, hipérbole.",
        ],
        examples=[
            GrammarExample(
                text="O tempo é dinheiro. (metáfora)",
            ),
            GrammarExample(
                text="O Brasil venceu o jogo. (metonímia: o país pela seleção)",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A vida é como uma viagem é uma metáfora sem comparação explícita.",
                correct="A vida é como uma viagem é uma comparação explícita; A vida é uma viagem exemplifica a metáfora.",
                note="Neste par, como explicita a comparação. Nem toda ocorrência de como é uma figura literária.",
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
                wrong="Original: A medida pode reduzir custos se houver adesão. Síntese: A medida reduzirá custos.",
                correct="A medida pode reduzir custos, dependendo da adesão.",
                note="A síntese precisa preservar tanto a possibilidade quanto a condição.",
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
        explanation="Uma crítica construtiva identifica um problema específico, explica seu efeito e propõe uma ação viável. O condicional pode suavizar a sugestão (Seria útil indicar a fonte), mas não deve ocultar a informação necessária. Reconhecer um mérito pode ajudar; não é uma etapa obrigatória. Em uma emergência ou diante de erro factual claro, a formulação direta pode ser adequada. Evite transformar a crítica ao texto em julgamento sobre a pessoa.",
        rules=[
            "Descreva o problema e uma ação possível, considerando a relação e a urgência.",
            "Condicional: seria, poderia.",
        ],
        examples=[
            GrammarExample(
                text="O relatório está muito completo. Talvez fosse útil incluir mais dados.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Você é incapaz de escrever um relatório.",
                correct="Esta seção não identifica a fonte dos dados; inclua a referência para que possamos verificá-los.",
                note="A reformulação substitui o ataque pessoal por uma observação específica e uma ação verificável.",
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
        explanation="Reformular é reapresentar uma ideia para esclarecer, resumir ou ajustar o registro. Isto é, ou seja e dito de outra forma sinalizam essa relação. Preserve participantes, negação, condições e grau de certeza: Talvez a equipe adie a entrega não equivale a A entrega será adiada. Ao mudar a voz, mantenha o agente quando ele for relevante: A comissão aprovou o texto -> O texto foi aprovado pela comissão.",
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
                wrong="O projeto talvez seja viável; ou seja, sua viabilidade está comprovada.",
                correct="O projeto talvez seja viável; ou seja, há uma possibilidade de que possa ser realizado.",
                note="Uma reformulação não pode elevar uma possibilidade à condição de certeza.",
            ),
        ],
        related=[
            "sintese-textual",
            "critica-construtiva",
            "registo-formal",
        ],
    ),
]
