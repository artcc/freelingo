"""Brazilian Portuguese (grammar_c2) learning content."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="revisao-conjuntivo",
        title="Revisão geral do subjuntivo",
        level="C2",
        category="Subjuntivo",
        summary="Domínio completo do subjuntivo.",
        explanation="Presente (que, talvez), Imperfeito (se), Futuro (quando), MQP Composto (se + tivesse + part.).",
        rules=[
            "Presente, Imperfeito, Futuro, MQP Composto.",
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
        explanation="Tipo 1: Se estudares, passas. Tipo 2: Se estudasses, passavas. Tipo 3: Se tivesses estudado, tinhas passado.",
        rules=[
            "Tipo 1, 2, 3.",
            "Coloquial brasileiro: imperfeito em vez de condicional.",
        ],
        examples=[
            GrammarExample(
                text="Se estudares, passas.",
            ),
            GrammarExample(
                text="Se estudasses, passavas.",
                note="coloquial brasileiro",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se tu estudasse, passavas.",
                correct="Se estudasses, passavas.",
                note="Tu exige estudasses. Se estudavas, passavas também pode ser correto para uma relação habitual no passado.",
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
        explanation="Variedade sintática, léxico preciso, figuras de estilo com moderação, mostrar em vez de dizer.",
        rules=[
            "Variar estruturas.",
            "Léxico preciso.",
            "Mostrar, não dizer.",
        ],
        examples=[
            GrammarExample(
                text="O sol morria no horizonte, tingindo o Tejo de ouro líquido.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Abusar de adjetivos.",
                correct="Menos é mais.",
                note="",
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
        explanation="1a pessoa, 3a omnisciente, 3a objetiva, discurso indireto livre.",
        rules=[
            "1a pessoa = personagem.",
            "3a omnisciente = pensamentos.",
            "Discurso indireto livre.",
        ],
        examples=[
            GrammarExample(
                text="Maria abriu a porta devagar, sem saber que o destino a esperava. (omnisciente)",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Alternar voz sem necessidade.",
                correct="Manter consistência.",
                note="",
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
        explanation="Sinestesia (cheiro doce), aliteração (vento varria vielas), quiasmo (Não vivemos para comer, comemos para viver).",
        rules=[
            "Sinestesia, aliteração, assonância, quiasmo.",
        ],
        examples=[
            GrammarExample(
                text="O cheiro doce da manhã. (sinestesia)",
            ),
            GrammarExample(
                text="O vento varria as velhas vielas. (aliteração)",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Aliteração forçada.",
                correct="Usar com naturalidade.",
                note="",
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
        explanation="Latim vulgar -> Galego-português (XII-XIV) -> Português antigo -> Clássico -> Moderno. Mudanças: populu > povo, plenu > cheio, manu > mão.",
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
        explanation="a priori, ad hoc, ipso fato, per capita, sine qua non, grosso modo, curriculum vitae, lato sensu.",
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
        explanation="~1000 palavras: arroz, azeite, açúcar, álgebra, algoritmo, zero, aldeia. Muitas com al- (artigo árabe).",
        rules=[
            "~1000 palavras.",
            "al- = artigo árabe.",
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
                wrong="Ignorar a origem árabe.",
                correct="O português é uma língua de encontros culturais.",
                note="",
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
        explanation="Ensaio, acadêmico, relatório, editorial, carta formal, discurso. Cada um com convenções específicas.",
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
                wrong="Misturar convenções de gêneros.",
                correct="Cada gênero tem registro e estrutura próprios.",
                note="",
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
        explanation="Neologismos (googlar), amálgamas (portunhol), trocadilhos (Não é só ver, é prever), estrangeirismos adaptados (futebol).",
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
                wrong="Neologismos incompreensíveis.",
                correct="Devem ser intuitivos.",
                note="",
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
        explanation="Conteúdo, estilo, gramática, tipografia. Ler em voz alta. Distância temporal.",
        rules=[
            "Conteúdo, estilo, gramática, tipografia.",
        ],
        examples=[
            GrammarExample(
                text="Rever: Os aluno terminou -> Os alunos terminaram.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Rever apenas gramática.",
                correct="Edição eficaz revê tudo.",
                note="",
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
        explanation="Certeza (é indubitável), probabilidade (tudo indica), incerteza (diria que), cortesia (permita-me, gostaria de).",
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
                wrong="Afirmações demasiado categóricas.",
                correct="Matizar quando não há certeza.",
                note="",
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
        explanation="Subjuntivo/indicativo natural. Ênclise/próclise/mesóclise. Concordância temporal. Escolha contextual de registro.",
        rules=[
            "Subjuntivo/indicativo.",
            "Ênclise/próclise/mesóclise.",
            "Concordância.",
            "Registro contextualizado.",
        ],
        examples=[
            GrammarExample(
                text="Se eu tivesse sabido que seria tão difícil, ter-me-ia preparado melhor.",
                note="integração completa",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Hesitação subjuntivo/indicativo.",
                correct="Com prática, torna-se intuitivo.",
                note="",
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
                text="A fluência não é só falar corretamente -- é pensar, sentir e sonhar em português.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Achar que C2 é o fim.",
                correct="A aprendizagem nunca termina.",
                note="",
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
        explanation="A **lusofonia** abrange comunidades ligadas pelo uso do português, com histórias, variedades e situações de multilinguismo distintas. Não se confunde com uma organização única.\n\nA **CPLP**, Comunidade dos Países de Língua Portuguesa, é uma organização intergovernamental de cooperação. O **IILP** promove a língua no âmbito dessa comunidade.\n\nO Brasil concentra a maior parte dos falantes de português. Países africanos como Angola e Moçambique têm um papel importante no seu crescimento demográfico. A presença oficial do português não implica que seja a língua materna ou maioritária de toda a população.\n\nOs debates incluem diversidade normativa, educação multilingue, circulação cultural e acesso à ciência.",
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
                text="O Brasil criou o VOLP (Vocabulário Ortográfico da Língua Portuguesa) para gerir a norma brasileira no quadro do Acordo Ortográfico.",
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
                text="Portugal europeu: 'Dá-me o livro.' — Brasil: 'Me dá o livro.' — A colocação pronominal é uma das diferenças mais visíveis entre as normas.",
                note="PE vs. PB — próclise",
            ),
            GrammarExample(
                text="O Acordo Ortográfico eliminou as consoantes mudas em Portugal: 'acção' passou a 'ação', 'óptimo' passou a 'ótimo'.",
                note="AO90",
            ),
            GrammarExample(
                text="Em Moçambique, palavras como 'machimbombo' (ônibus) e 'candongueiro' (minibus) mostram a criatividade lexical do português africano.",
                note="português moçambicano",
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
                text="obg pela msg, depois falamos cmg :) bjs!",
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
