"""Portuguese grammar topics — C2."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="revisao-conjuntivo",
        title="Revisão geral do conjuntivo",
        level="C2",
        category="Conjuntivo",
        summary="Domínio completo do conjuntivo.",
        explanation="Presente (que, talvez), Imperfeito (se), Futuro (quando), MQP Composto (se + tivesse + part.).",
        rules=[
            "Presente, Imperfeito, Futuro, MQP Composto.",
        ],
        examples=[
            GrammarExample(
                text="Qualquer que seja a decisão, estou de acordo.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Qualquer que é a decisão.",
                correct="Qualquer que seja a decisão.",
                note="Qualquer que + conjuntivo.",
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
        explanation="Tipo 1: Se estudares, passas. Tipo 2: Se estudasses, passavas. Tipo 3: Se tivesses estudado, tinhas passado.",
        rules=[
            "Tipo 1, 2, 3.",
            "Coloquial EP: imperfeito em vez de condicional.",
        ],
        examples=[
            GrammarExample(text="Se estudares, passas.", translation=None),
            GrammarExample(
                text="Se estudasses, passavas.",
                translation=None,
                note="coloquial EP",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se tu estudasse, passavas.",
                correct="Se estudasses, passavas.",
                note="Tu exige estudasses. Se estudavas, passavas também pode ser correto para uma relação habitual no passado.",
            ),
        ],
        related=["condicional", "se-imperfeito-subjuntivo", "condicional-composto"],
    ),
    GrammarTopic(
        slug="mesoclise",
        title="Mesóclise",
        level="C2",
        category="Pronomes",
        summary="Domínio da mesóclise no futuro e condicional.",
        explanation="A mesóclise coloca o pronome dentro do futuro ou do condicional: Dar-te-ei; Dar-te-ia. É frequente em escrita formal. Com um elemento que exige próclise, o pronome vem antes: Não te darei; Quem te daria isso? Na conversa, são comuns alternativas como Vou dar-te o livro.",
        rules=[
            "Pronome no meio do verbo.",
            "Futuro e condicional.",
        ],
        examples=[
            GrammarExample(
                text="Enviar-lhe-ei os documentos amanhã.",
                translation=None,
                note="formal",
            ),
            GrammarExample(
                text="Poder-se-ia argumentar que...",
                translation=None,
                note="académico",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Não enviar-lhe-ei os documentos.",
                correct="Não lhe enviarei os documentos.",
                note="A negação exige próclise. A mesóclise é gramatical, embora marcada em conversa informal.",
            ),
        ],
        related=["colocacao-pronominal", "futuro-do-presente", "condicional"],
    ),
    GrammarTopic(
        slug="estilo-literario",
        title="Estilo literário",
        level="C2",
        category="Avançado",
        summary="Desenvolver uma voz literária autêntica.",
        explanation="Variedade sintática, léxico preciso, figuras de estilo com moderação, mostrar em vez de dizer.",
        rules=[
            "Variar estruturas.",
            "Léxico preciso.",
            "Mostrar, não dizer.",
        ],
        examples=[
            GrammarExample(
                text="O sol morria no horizonte, tingindo o Tejo de ouro líquido.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(wrong="Abusar de adjetivos.", correct="Menos é mais.", note=""),
        ],
        related=["descricao-literaria", "recursos-estilisticos", "voz-narrativa"],
    ),
    GrammarTopic(
        slug="voz-narrativa",
        title="Voz narrativa",
        level="C2",
        category="Avançado",
        summary="Tipos de narrador e construção da voz narrativa.",
        explanation="1a pessoa, 3a omnisciente, 3a objetiva, discurso indireto livre.",
        rules=[
            "1a pessoa = personagem.",
            "3a omnisciente = pensamentos.",
            "Discurso indireto livre.",
        ],
        examples=[
            GrammarExample(
                text="Maria abriu a porta devagar, sem saber que o destino a esperava. (omnisciente)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Alternar voz sem necessidade.",
                correct="Manter consistência.",
                note="",
            ),
        ],
        related=["estilo-literario", "descricao-literaria"],
    ),
    GrammarTopic(
        slug="recursos-estilisticos",
        title="Recursos estilísticos avançados",
        level="C2",
        category="Avançado",
        summary="Sinestesia, aliteração, assonância, quiasmo.",
        explanation="Sinestesia (cheiro doce), aliteração (vento varria vielas), quiasmo (Não vivemos para comer, comemos para viver).",
        rules=[
            "Sinestesia, aliteração, assonância, quiasmo.",
        ],
        examples=[
            GrammarExample(
                text="O cheiro doce da manhã. (sinestesia)",
                translation=None,
            ),
            GrammarExample(
                text="O vento varria as velhas vielas. (aliteração)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(wrong="Aliteração forçada.", correct="Usar com naturalidade.", note=""),
        ],
        related=["figuras-literarias", "estilo-literario"],
    ),
    GrammarTopic(
        slug="equivalencia",
        title="Equivalência na tradução",
        level="C2",
        category="Avançado",
        summary="Princípios de equivalência tradutória.",
        explanation="Equivalência funcional: desenrascanço -> knack for improvising. Evitar calques. Expressões: equivalentes culturais.",
        rules=[
            "Equivalência funcional.",
            "Evitar calques.",
        ],
        examples=[
            GrammarExample(
                text="Custou os olhos da cara. -> It cost an arm and a leg.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Estar com a pulga atrás da orelha. -> To be with the flea behind the ear.",
                correct="To be suspicious.",
                note="Expressões NÃO se traduzem literalmente.",
            ),
        ],
        related=["falsos-amigos", "matizes-traducao"],
    ),
    GrammarTopic(
        slug="matizes-traducao",
        title="Matizes de tradução",
        level="C2",
        category="Avançado",
        summary="Nuances que distinguem uma boa tradução.",
        explanation="Registo, tempos verbais, conotações culturais (saudade sem equivalente exato).",
        rules=[
            "Registo e formalidade.",
            "Tempos: composto PT != present perfect EN.",
            "Conotações culturais.",
        ],
        examples=[
            GrammarExample(
                text="Tenho andado a pensar nisso. -> I have been thinking about that.",
                translation=None,
            ),
            GrammarExample(text="Que saudades! -> I miss you so much!", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Tenho comido ontem. -> I have eaten yesterday.",
                correct="Comi ontem. -> I ate yesterday.",
                note="Ação única: pretérito simples.",
            ),
        ],
        related=["equivalencia", "falsos-amigos"],
    ),
    GrammarTopic(
        slug="falsos-amigos",
        title="Falsos amigos",
        level="C2",
        category="Avançado",
        summary="Palavras portuguesas que parecem inglesas.",
        explanation="Atualmente indica o momento presente, não uma correção equivalente a na verdade. Pretender significa ter a intenção de fazer algo, não fingir. Compromisso pode designar uma obrigação ou encontro, mas também um acordo entre partes; a tradução depende do contexto e pode corresponder a compromise nesse último sentido.",
        rules=[
            "Atualmente = currently.",
            "Compromisso pode ser uma obrigação, um encontro marcado ou um acordo; o contexto decide a tradução.",
            "Pretender = to intend.",
        ],
        examples=[
            GrammarExample(
                text="Atualmente moro em Lisboa. -> I currently live in Lisbon.",
                translation=None,
            ),
            GrammarExample(
                text="Tenho um compromisso às três. -> I have an appointment at three.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Actually -> atualmente.",
                correct="Actually = na verdade. Atualmente = currently.",
                note="",
            ),
        ],
        related=["equivalencia", "matizes-traducao"],
    ),
    GrammarTopic(
        slug="evolucao-linguistica",
        title="Evolução linguística",
        level="C2",
        category="Avançado",
        summary="Como a língua portuguesa evoluiu do latim.",
        explanation="Latim vulgar -> Galego-português (XII-XIV) -> Português antigo -> Clássico -> Moderno. Mudanças: populu > povo, plenu > cheio, manu > mão.",
        rules=[
            "Latim vulgar > Galego-português > Moderno.",
            "Queda de consoantes, palatalização, nasalização.",
        ],
        examples=[
            GrammarExample(text="Latim: populu -> Português: povo", translation=None),
            GrammarExample(text="Latim: plenu -> Português: cheio", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Confundir evolução com corrupção.",
                correct="Mudança linguística é natural.",
                note="",
            ),
        ],
        related=["latinismos", "arabismos-portugueses"],
    ),
    GrammarTopic(
        slug="latinismos",
        title="Latinismos",
        level="C2",
        category="Avançado",
        summary="Expressões e palavras latinas no português.",
        explanation="a priori, ad hoc, ipso facto, per capita, sine qua non, grosso modo, curriculum vitae, lato sensu.",
        rules=[
            "Comuns no registo formal.",
            "Usar com precisão.",
        ],
        examples=[
            GrammarExample(
                text="A segurança é uma condição sine qua non.",
                translation=None,
            ),
            GrammarExample(
                text="Grosso modo, a proposta é aceitável.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="À posteriori.",
                correct="A posteriori.",
                note="A é preposição latina, não leva crase.",
            ),
        ],
        related=["evolucao-linguistica", "arabismos-portugueses", "registo-formal"],
    ),
    GrammarTopic(
        slug="arabismos-portugueses",
        title="Arabismos portugueses",
        level="C2",
        category="Avançado",
        summary="A herança árabe no léxico português.",
        explanation="~1000 palavras: arroz, azeite, açúcar, álgebra, algoritmo, zero, aldeia. Muitas com al- (artigo árabe).",
        rules=[
            "~1000 palavras.",
            "al- = artigo árabe.",
            "Alimentos, ciência, arquitetura.",
        ],
        examples=[
            GrammarExample(text="azeite (az-zayt)", translation=None),
            GrammarExample(text="arroz (ar-ruzz)", translation=None),
            GrammarExample(text="álgebra (al-jabr)", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ignorar a origem árabe.",
                correct="O português é uma língua de encontros culturais.",
                note="",
            ),
        ],
        related=["evolucao-linguistica", "latinismos"],
    ),
    GrammarTopic(
        slug="generos-textuais",
        title="Géneros textuais",
        level="C2",
        category="Avançado",
        summary="Domínio de todos os géneros textuais.",
        explanation="Ensaio, académico, relatório, editorial, carta formal, discurso. Cada um com convenções específicas.",
        rules=[
            "Cada género tem convenções.",
            "Conhecer o género orienta escolhas.",
        ],
        examples=[
            GrammarExample(
                text="O presente relatório apresenta os resultados do inquérito.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Misturar convenções de géneros.",
                correct="Cada género tem registo e estrutura próprios.",
                note="",
            ),
        ],
        related=["registo-formal", "estrutura-argumentativa"],
    ),
    GrammarTopic(
        slug="criatividade-linguistica",
        title="Criatividade linguística",
        level="C2",
        category="Avançado",
        summary="Brincar com a língua: neologismos, trocadilhos.",
        explanation="Neologismos (googlar), amálgamas (portunhol), trocadilhos (Não é só ver, é prever), estrangeirismos adaptados (futebol).",
        rules=[
            "Neologismos, amálgamas, trocadilhos.",
        ],
        examples=[
            GrammarExample(
                text="Vou googlar esse termo. (neologismo)",
                translation=None,
            ),
            GrammarExample(
                text="Não é só ver, é prever! (trocadilho)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Neologismos incompreensíveis.",
                correct="Devem ser intuitivos.",
                note="",
            ),
        ],
        related=["derivacao", "expressoes-coloquiais", "expressao-matizada"],
    ),
    GrammarTopic(
        slug="edicao",
        title="Edição e revisão de textos",
        level="C2",
        category="Avançado",
        summary="Técnicas de edição para clareza e elegância.",
        explanation="Conteúdo, estilo, gramática, tipografia. Ler em voz alta. Distância temporal.",
        rules=[
            "Conteúdo, estilo, gramática, tipografia.",
        ],
        examples=[
            GrammarExample(
                text="Rever: Os aluno terminou -> Os alunos terminaram.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Rever apenas gramática.",
                correct="Edição eficaz revê tudo.",
                note="",
            ),
        ],
        related=["reformulacao", "coesao-textual", "expressao-matizada"],
    ),
    GrammarTopic(
        slug="expressao-matizada",
        title="Expressão matizada",
        level="C2",
        category="Avançado",
        summary="Arte de matizar o discurso.",
        explanation="Certeza (é indubitável), probabilidade (tudo indica), incerteza (diria que), cortesia (permita-me, gostaria de).",
        rules=[
            "Certeza, probabilidade, incerteza, cortesia.",
        ],
        examples=[
            GrammarExample(
                text="É indubitável que a medida trouxe benefícios.",
                translation=None,
            ),
            GrammarExample(
                text="Diria que a situação é complexa.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Afirmações demasiado categóricas.",
                correct="Matizar quando não há certeza.",
                note="",
            ),
        ],
        related=["matizadores", "recursos-retoricos", "critica-construtiva"],
    ),
    GrammarTopic(
        slug="integracao-gramatical",
        title="Integração gramatical",
        level="C2",
        category="Avançado",
        summary="Síntese de todos os conhecimentos gramaticais.",
        explanation="Conjuntivo/indicativo natural. Ênclise/próclise/mesóclise. Concordância temporal. Escolha contextual de registo.",
        rules=[
            "Conjuntivo/indicativo.",
            "Ênclise/próclise/mesóclise.",
            "Concordância.",
            "Registo contextualizado.",
        ],
        examples=[
            GrammarExample(
                text="Se eu tivesse sabido que seria tão difícil, ter-me-ia preparado melhor.",
                translation=None,
                note="integração completa",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Hesitação conjuntivo/indicativo.",
                correct="Com prática, torna-se intuitivo.",
                note="",
            ),
        ],
        related=["revisao-conjuntivo", "revisao-condicional", "expressao-matizada"],
    ),
    GrammarTopic(
        slug="fluencia-nativa",
        title="Fluência e autonomia avançadas",
        level="C2",
        category="Avançado",
        summary="Comunicar com precisão, flexibilidade e autonomia em situações complexas.",
        explanation="C2 implica compreender sentidos implícitos, reformular com precisão e adaptar o registo a contextos exigentes. Não exige perder o sotaque nem tornar-se indistinguível de um falante nativo. A inteligibilidade, a adequação e a autonomia são mais relevantes do que imitar uma identidade linguística.",
        rules=[
            "Expressão espontânea.",
            "Domínio cultural.",
            "Entoação PE.",
            "Flexibilidade de registos.",
        ],
        examples=[
            GrammarExample(
                text="A fluência não é só falar corretamente -- é pensar, sentir e sonhar em português.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Achar que C2 é o fim.",
                correct="A aprendizagem nunca termina.",
                note="",
            ),
        ],
        related=["integracao-gramatical", "expressao-matizada"],
    ),
    GrammarTopic(
        slug="tupinismos",
        title="Tupinismos — palavras de origem tupi-guarani",
        level="C2",
        category="Avançado",
        summary="Reconhecer e compreender os tupinismos integrados no português brasileiro.",
        explanation="Os **tupinismos** são palavras de origem tupi incorporadas ao português através do contacto linguístico no Brasil. Muitas designam fauna, flora, alimentos e lugares.\n\nExemplos: tatu, piranha, capivara, arara, tucano; abacaxi, mandioca, caju; pipoca, tapioca; Ipanema, Paraná e Iguaçu. Nem todas as palavras indígenas nem todos os topónimos brasileiros têm origem tupi: cada etimologia deve ser verificada.",
        rules=[
            "Tupinismos designam maioritariamente fauna, flora e topónimos brasileiros.",
            "Alguns termos designam realidades locais; outros circulam também em Portugal, como abacaxi e mandioca.",
            "São parte integrante do vocabulário ativo brasileiro.",
            "Reconhecer a origem tupi demonstra conhecimento avançado da cultura e história da língua.",
        ],
        examples=[
            GrammarExample(
                text="Vou comer um abacaxi com tapioca.",
                translation=None,
            ),
            GrammarExample(
                text="O tucano e a arara são aves típicas do Brasil.",
                translation=None,
            ),
            GrammarExample(
                text="A capivara é o maior roedor do mundo.",
                translation=None,
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
        explanation="A **lusofonia** abrange comunidades ligadas pelo uso do português, com histórias, variedades e situações de multilinguismo distintas. Não se confunde com uma organização única.\n\nA **CPLP**, Comunidade dos Países de Língua Portuguesa, é uma organização intergovernamental de cooperação. O **IILP** promove a língua no âmbito dessa comunidade.\n\nO Brasil concentra a maior parte dos falantes de português. Países africanos como Angola e Moçambique têm um papel importante no seu crescimento demográfico. A presença oficial do português não implica que seja a língua materna ou maioritária de toda a população.\n\nOs debates incluem diversidade normativa, educação multilingue, circulação cultural e acesso à ciência.",
        rules=[
            "A Lusofonia não é um bloco monolítico — cada país tem a sua variedade e política linguística.",
            "O Brasil concentra a maioria dos falantes; o crescimento africano não elimina as diferenças de uso entre países.",
            "A CPLP promove o plurilinguismo e a diversidade cultural, não o monolinguismo português.",
        ],
        examples=[
            GrammarExample(
                text="Em Angola, expressões como 'maka' (conflito, confusão) ou 'bué' (muito) enriquecem o português local com influências das línguas bantu.",
                translation=None,
                note="português angolano",
            ),
            GrammarExample(
                text="O Brasil criou o VOLP (Vocabulário Ortográfico da Língua Portuguesa) para gerir a norma brasileira no quadro do Acordo Ortográfico.",
                translation=None,
            ),
            GrammarExample(
                text="Uma projeção sobre falantes deve indicar a fonte, a data e se conta língua materna, segunda língua ou ambas.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Lusofonia e CPLP são a mesma organização.",
                correct="Lusofonia designa um espaço linguístico e cultural; a CPLP é uma organização intergovernamental.",
                note="As comunidades lusófonas incluem também diásporas e não se limitam à pertença institucional à CPLP.",
            ),
        ],
        related=["politica-linguistica-pt", "evolucao-linguistica"],
    ),
    GrammarTopic(
        slug="politica-linguistica-pt",
        title="Política linguística no mundo lusófono",
        level="C2",
        category="Expressão",
        summary="Do Acordo Ortográfico à difusão do português: políticas e tensões linguísticas nos países de língua portuguesa.",
        explanation="As políticas linguísticas são definidas por instituições nacionais e por mecanismos de cooperação. As academias publicam obras lexicográficas e estudos; não controlam sozinhas todos os usos ou decisões educativas. O IILP promove a cooperação no âmbito da CPLP.\n\nO **Acordo Ortográfico de 1990** procura aproximar a escrita; a adoção e aplicação variam entre países. Não uniformiza pronúncia, gramática ou vocabulário.\n\nO português é pluricêntrico: as variedades europeia, brasileira e africanas têm usos próprios. As diferenças de colocação pronominal dependem também do registo: Me dá é comum na fala brasileira, mas não resume a norma escrita formal.\n\nA educação em contextos multilingues deve considerar o português e as outras línguas das comunidades.",
        rules=[
            "O Acordo Ortográfico é um tratado internacional, não uma imposição — cada país decide a sua aplicação.",
            "O português é uma língua pluricêntrica: PE e PB são normas de igual legitimidade.",
            "As variedades africanas estão a afirmar-se como normas emergentes com traços próprios.",
        ],
        examples=[
            GrammarExample(
                text="Portugal europeu: 'Dá-me o livro.' — Brasil: 'Me dá o livro.' — A colocação pronominal é uma das diferenças mais visíveis entre as normas.",
                translation=None,
                note="PE vs. PB — próclise",
            ),
            GrammarExample(
                text="O Acordo Ortográfico eliminou as consoantes mudas em Portugal: 'acção' passou a 'ação', 'óptimo' passou a 'ótimo'.",
                translation=None,
                note="AO90",
            ),
            GrammarExample(
                text="Em Moçambique, palavras como 'machimbombo' (autocarro) e 'candongueiro' (minibus) mostram a criatividade lexical do português africano.",
                translation=None,
                note="português moçambicano",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A Academia das Ciências de Lisboa dita as regras do português em todos os países lusófonos.",
                correct="A ACL regula apenas a norma europeia. Cada país tem as suas instituições de regulação (ABL no Brasil, etc.).",
                note="Distinguir norma europeia de norma internacional.",
            ),
        ],
        related=["lusofonia-contemporanea", "evolucao-linguistica"],
    ),
    GrammarTopic(
        slug="evolucao-digital-pt",
        title="O português na era digital",
        level="C2",
        category="Expressão",
        summary="Como o português evolui com o digital: redes sociais, IA, anglicismos e novos usos linguísticos.",
        explanation="O **digital transforma o português** a um ritmo acelerado:\n\n**Redes sociais e mensagens**:\n- Abreviaturas: *tb* (também), *msg* (mensagem), *bjs* (beijos), *cmg* (comigo), *sff* (se faz favor), *obg* (obrigado/a).\n- Emojis como pontuação emocional e reforço pragmático.\n- Hashtags e a sua sintaxe: *#Portugal, #Lusofonia*.\n\n**Neologismos e anglicismos digitais**:\n- Neologismos: *googlar*, *tuitar*, *postar*, *clicar*, *descarregar*, *carregar*.\n- Anglicismos: *download*, *upload*, *site*, *link*, *chat*, *streaming*, *podcast*.\n- Adaptações: *clicar* (de *click*), *resetear* (de *reset*), *forwardear* (de *forward*).\n\n**IA e processamento de língua natural**:\n- ChatGPT, DeepL, tradução automática: desafios para a aprendizagem do português.\n- Assistentes virtuais em português (PE e PB).\n- Modelos de IA treinados maioritariamente em inglês — viés linguístico.\n\n**Socioletos digitais**:\n- Gíria da internet: *lol*, *troll*, *fail*, *crush*, *cringe*.\n- Mistura de registos: escrita informal digital aproxima-se da oralidade.",
        rules=[
            "O português digital não é uma versão 'degradada' da língua — é um registo adaptado ao meio e ao contexto.",
            "Os anglicismos na tecnologia são frequentes, mas o português também cria alternativas (descarregar, carregar, correio eletrónico).",
            "A IA e a tradução automática levantam questões de soberania linguística e representatividade das variedades do português.",
        ],
        examples=[
            GrammarExample(
                text="obg pela msg, depois falamos cmg :) bjs!",
                translation=None,
                note="linguagem SMS em português europeu",
            ),
            GrammarExample(
                text="Vou googlar esse termo e depois faço o download do ficheiro.",
                translation=None,
                note="mistura de neologismo e anglicismo",
            ),
            GrammarExample(
                text="Os modelos de IA generativa ainda produzem um português com forte viés brasileiro, o que levanta questões sobre a representatividade das variedades europeia e africanas.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="A linguagem das redes sociais é 'mau português'.",
                correct="Cada contexto comunicativo exige um registo adequado — a linguagem digital é funcional e criativa no seu meio, não sendo inferior ao registo formal.",
                note="Evitar preconceitos linguísticos sobre variedades e registos.",
            ),
        ],
        related=["lusofonia-contemporanea", "criatividade-linguistica"],
    ),
]
