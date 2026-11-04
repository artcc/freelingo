"""Brazilian Portuguese (phrasebook_c2) learning content."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="rhetoric_c2",
        level="C2",
        situation="Retórica e persuasão",
        icon="⚖️",
        phrases=[
            PhrasebookEntry(
                text="Não há sombra de dúvida de que as evidências falam por si.",
                context="Reforçar uma afirmação com força retórica",
                register="formal",
            ),
            PhrasebookEntry(
                text="Quem ousaria afirmar o contrário?",
                context="Pergunta retórica para reforçar a tese",
                register="formal",
            ),
            PhrasebookEntry(
                text="Chegou o momento de enfrentar a verdade, por mais incômoda que seja.",
                context="Apelo emotivo à verdade",
                register="formal",
            ),
            PhrasebookEntry(
                text="Não podemos ficar inertes perante uma tão grande injustiça.",
                context="Apelo à ação",
                register="formal",
            ),
            PhrasebookEntry(
                text="As consequências de uma falta de ação seriam catastróficas.",
                context="Aviso sobre as consequências",
                register="formal",
            ),
            PhrasebookEntry(
                text="Apelo ao senso de responsabilidade de todos em relação às gerações futuras.",
                context="Apelo às gerações futuras",
                register="formal",
            ),
            PhrasebookEntry(
                text="Isto não é uma questão de direita ou de esquerda, mas de bom senso.",
                context="Ultrapassar divisões políticas",
                register="formal",
            ),
            PhrasebookEntry(
                text="Deixem-me contar uma história que ilustra melhor do que mil palavras o que pretendo dizer.",
                context="Usar uma narrativa persuasiva",
                register="formal",
            ),
            PhrasebookEntry(
                text="Estamos numa encruzilhada histórica, e a escolha que fizermos hoje definirá o nosso futuro.",
                context="Criar urgência histórica",
                register="formal",
            ),
            PhrasebookEntry(
                text="Não nos iludamos: a estrada é íngreme, mas é transitável.",
                context="Reconhecer dificuldades mas infundir esperança",
                register="formal",
            ),
            PhrasebookEntry(
                text="Quem não faz parte da solução faz parte do problema.",
                context="Dicotomia retórica",
                register="formal",
            ),
            PhrasebookEntry(
                text="Permitam-me sonhar por um instante com um mundo em que...",
                context="Abertura visionária",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="nuanced_discourse_c2",
        level="C2",
        situation="Discurso matizado e atenuacao",
        icon="🔬",
        phrases=[
            PhrasebookEntry(
                text="Na minha modesta opinião, a questão é bem mais complexa do que parece à primeira vista.",
                context="Minimizar a própria opinião por diplomacia",
                register="formal",
            ),
            PhrasebookEntry(
                text="Não se pode excluir à partida que tenha havido mal-entendidos.",
                context="Abrir a possibilidades alternativas",
                register="formal",
            ),
            PhrasebookEntry(
                text="Tenderia a crer que as coisas são diferentes, mas estou pronto/a a mudar de ideias.",
                context="Exprimir opinião com abertura à mudança",
                register="formal",
            ),
            PhrasebookEntry(
                text="Seria arriscado tirar conclusões definitivas com base nos dados atuais.",
                context="Alertar contra conclusões precipitadas",
                register="formal",
            ),
            PhrasebookEntry(
                text="No que me diz respeito, não haveria objeções de princípio, mas haveria que avaliar os detalhes operacionais.",
                context="Acordo condicionado",
                register="formal",
            ),
            PhrasebookEntry(
                text="Admitindo, sem conceder, que a premissa seja correta, a conclusão não é evidente.",
                context="Aceitar hipoteticamente uma premissa",
                register="formal",
            ),
            PhrasebookEntry(
                text="Não gostaria que as minhas palavras fossem interpretadas como uma crítica, mas antes como uma sugestão de reflexão.",
                context="Atenuar uma potencial crítica",
                register="formal",
            ),
            PhrasebookEntry(
                text="É verossímil que a situação evolua numa direção diferente da prevista.",
                context="Exprimir probabilidade com cautela",
                register="formal",
            ),
            PhrasebookEntry(
                text="Longe de mim a ideia de querer impor a minha visão.",
                context="Prevenir acusações de arrogância",
                register="formal",
            ),
            PhrasebookEntry(
                text="Poder-se-ia talvez arriscar a hipótese de as causas serem mais profundas.",
                context="Propor hipótese com cautela",
                register="formal",
            ),
            PhrasebookEntry(
                text="É inegavelmente um passo em frente, embora subsistam algumas dificuldades.",
                context="Equilibrar elogio e crítica",
                register="formal",
            ),
            PhrasebookEntry(
                text="Seria cauteloso/a em atribuir pura e simplesmente a responsabilidade a um único fator.",
                context="Alertar contra atribuições simplistas",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="legal_contractual_c2",
        level="C2",
        situation="Linguagem jurídica e contratual",
        icon="📜",
        phrases=[
            PhrasebookEntry(
                text="Nos termos do artigo 3.º do presente contrato, as partes acordam no seguinte.",
                context="Referência a uma cláusula contratual",
                register="formal",
            ),
            PhrasebookEntry(
                text="O presente acordo é regido pela legislação brasileira.",
                context="Especificar a jurisdição",
                register="formal",
            ),
            PhrasebookEntry(
                text="Sem prejuízo do disposto no número anterior.",
                context="Fazer uma reserva legal",
                register="formal",
            ),
            PhrasebookEntry(
                text="O presente documento constitui a totalidade do acordo entre as partes.",
                context="Cláusula de integralidade contratual",
                register="formal",
            ),
            PhrasebookEntry(
                text="Qualquer alteração deverá ser feita por escrito e assinada por ambas as partes.",
                context="Cláusula de alteração",
                register="formal",
            ),
            PhrasebookEntry(
                text="A parte incumpridora será responsável pelo pagamento de perdas e danos.",
                context="Cláusula de incumprimento",
                register="formal",
            ),
            PhrasebookEntry(
                text="As partes elegem domicílio nas respectivas sedes sociais.",
                context="Eleição de domicílio",
                register="formal",
            ),
            PhrasebookEntry(
                text="O contrato é nulo quando contrário a normas imperativas.",
                context="Cláusula de nulidade",
                register="formal",
            ),
            PhrasebookEntry(
                text="Por ser verdade, as partes assinam o presente documento.",
                context="Fórmula de fecho legal",
                register="formal",
            ),
            PhrasebookEntry(
                text="A formalização deste ato depende dos registros exigidos pela legislação aplicável.",
                context="Obrigação de registro",
                register="formal",
            ),
            PhrasebookEntry(
                text="Os litígios serão dirimidos no foro competente, observadas as regras legais de competência.",
                context="Cláusula do foro competente",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="social_commentary_c2",
        level="C2",
        situation="Comentário social e debate",
        icon="🗞️",
        phrases=[
            PhrasebookEntry(
                text="A sociedade contemporânea enfrenta desafios sem precedentes.",
                context="Abertura de um comentário social",
                register="formal",
            ),
            PhrasebookEntry(
                text="A distância entre ricos e pobres está aumentando de forma alarmante.",
                context="Denúncia de desigualdade",
                register="formal",
            ),
            PhrasebookEntry(
                text="É indispensável uma mudança de paradigma se quisermos garantir um futuro sustentável.",
                context="Apelo à mudança",
                register="formal",
            ),
            PhrasebookEntry(
                text="Já não podemos dar-nos ao luxo de ignorar as consequências das nossas ações no planeta.",
                context="Apelo ecológico",
                register="formal",
            ),
            PhrasebookEntry(
                text="A crise que atravessamos não é apenas econômica, mas também de valores.",
                context="Análise multidimensional",
                register="formal",
            ),
            PhrasebookEntry(
                text="As novas tecnologias oferecem oportunidades extraordinárias, mas também levantam interrogações éticas inquietantes.",
                context="Equilibrar progresso e riscos",
                register="formal",
            ),
            PhrasebookEntry(
                text="Assistimos a uma progressiva erosão da confiança nas instituições democráticas.",
                context="Análise política",
                register="formal",
            ),
            PhrasebookEntry(
                text="É nosso dever moral empenharmo-nos por uma sociedade mais justa e inclusiva.",
                context="Apelo moral",
                register="formal",
            ),
            PhrasebookEntry(
                text="O debate público foi contaminado por uma onda de desinformação sem precedentes.",
                context="Crítica dos media",
                register="formal",
            ),
            PhrasebookEntry(
                text="A cultura, entendida no seu sentido mais amplo, é o único verdadeiro antídoto contra a intolerância.",
                context="Elogio da cultura",
                register="formal",
            ),
            PhrasebookEntry(
                text="Sem uma educação de qualidade, qualquer discurso sobre progresso social está condenado a ser letra morta.",
                context="Defesa da educação",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="lusofonia_contemporanea_pt_c2",
        level="C2",
        situation="Lusofonia e desafios contemporâneos",
        icon="🌍",
        phrases=[
            PhrasebookEntry(
                text="A cooperação institucional na CPLP ultrapassa o simples compartilhamento de uma língua comum.",
                context="Distinguir a Lusofonia institucional da mera comunidade linguística — discurso formal",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="O centro de gravidade demográfico do português desloca-se progressivamente para a África lusófona.",
                context="Discutir o deslocamento demográfico dos falantes de português — discurso geopolítico",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="Não existe um, mas vários portugueses: cada espaço lusófono desenvolve as suas próprias normas endógenas.",
                context="Defender o reconhecimento de múltiplas normas — linguagem acadêmica",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="A insegurança linguística continua a ser um obstáculo ao pleno desenvolvimento dos falantes das variedades periféricas.",
                context="Abordar a insegurança linguística entre falantes não europeus",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="O Acordo Ortográfico, conquanto imperfeitamente aplicado, representa um esforço de unificação com vantagens e desvantagens inegáveis.",
                context="Avaliar o Acordo Ortográfico de forma equilibrada — discurso acadêmico",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="A questão da norma-padrão, longe de ser meramente técnica, toca na própria identidade cultural dos povos lusófonos.",
                context="Abordar o debate sobre a norma-padrão — perspectiva cultural",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="Os socioletos urbanos e as gírias digitais não são uma degeneração do português, mas um laboratório de inovação linguística.",
                context="Defender os socioletos digitais como inovação linguística legítima — perspectiva sociolinguística",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="As redes sociais aceleram a evolução lexical a um ritmo sem precedentes na história da língua.",
                context="Comentar a aceleração da evolução lexical provocada pelas redes sociais",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="A competição entre o português europeu e o brasileiro no ensino da língua a estrangeiros reflete dinâmicas geopolíticas mais amplas.",
                context="Analisar a competição PE vs. PB no ensino do português como língua estrangeira",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="Não se pode dissociar a língua das relações de poder que a atravessam.",
                context="Afirmar que a língua é indissociável das relações de poder — sociolinguística crítica",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="Na era da inteligência artificial, a soberania linguística torna-se uma questão geopolítica de primeira ordem.",
                context="Apresentar a soberania linguística como questão geopolítica na era da IA",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="Entre o purismo ortográfico e o laissez-faire, uma política linguística equilibrada está ainda por inventar no espaço lusófono.",
                context="Criticar tanto o purismo como o laissez-faire — discurso diplomático",
                register="formal",
                unit_ref="c2-unit-7",
            ),
        ],
    ),
    PhrasebookCategory(
        id="retorica_discurso_c2",
        level="C2",
        situation="Retórica e discurso público",
        icon="🎙️",
        phrases=[
            PhrasebookEntry(
                text="Senhoras e senhores, tomo hoje a palavra movido por uma convicção profunda e inabalável.",
                context="Abertura solene de um discurso apaixonado",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="A eloquência não reside na abundância de palavras, mas na precisão com que estas atingem o seu alvo.",
                context="Definir a verdadeira eloquência",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="Permitam-me dirigir estas palavras não apenas à razão, mas também à consciência de todos.",
                context="Apelar à consciência do auditório",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="Se as palavras que aqui profiro tiverem o condão de fazer germinar uma só dúvida, terei cumprido o meu propósito.",
                context="Concluir um discurso com humildade retórica",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="Há momentos na história em que o silêncio é cumplicidade e a omissão é covardia.",
                context="Criar um dilema moral inescapável",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="Não é por ser difícil que hesitamos; é por hesitarmos que se torna difícil.",
                context="Inverter causa e efeito para efeito retórico",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="O poder da palavra é o poder de moldar realidades — usemo-lo, pois, com a responsabilidade que tal poder exige.",
                context="Refletir sobre o poder do discurso",
                register="formal",
                unit_ref="c2-unit-7",
            ),
            PhrasebookEntry(
                text="Concluo com uma pergunta para nossa reflexão: que legado queremos deixar aos que virão depois de nós?",
                context="Fechar com uma pergunta retórica em aberto",
                register="formal",
                unit_ref="c2-unit-7",
            ),
        ],
    ),
]
