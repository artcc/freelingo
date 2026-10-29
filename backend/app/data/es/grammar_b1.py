"""Spanish grammar topics — B1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="subjuntivo-presente",
        title="Presente de subjuntivo",
        level="B1",
        category="Subjuntivo",
        summary="Formación y usos básicos del presente de subjuntivo: deseo, duda, emoción, negación.",
        explanation="El **presente de subjuntivo** expresa acciones no factuales: deseos, dudas, emociones, mandatos negativos, opiniones negadas y finalidad. Se forma a partir de la primera persona singular del presente de indicativo, cambiando la **vocal temática**:\n\n| | -ar (hablar) | -er (comer) | -ir (vivir) |\n|---|-------------|-------------|-------------|\n| yo | hable | coma | viva |\n| tú | hables | comas | vivas |\n| él/ella/usted | hable | coma | viva |\n| nosotros | hablemos | comamos | vivamos |\n| vosotros | habléis | comáis | viváis |\n| ellos/ellas/uds. | hablen | coman | vivan |\n\n**Irregulares**: los verbos que son irregulares en la primera persona del presente de indicativo mantienen la irregularidad en el subjuntivo:\n- tener → tengo → tenga, tengas...\n- hacer → hago → haga, hagas...\n- decir → digo → diga, digas...\n- conocer → conozco → conozca, conozcas...\n- salir → salgo → salga, salgas...\n\nLos verbos con cambio vocálico (e→ie, o→ue) tienen el mismo cambio en las formas tónicas, y además en -ir cambian también e→i o o→u en nosotros/vosotros: *dormir → durmamos, pedir → pidamos*.",
        structure="raíz de 1ª pers. sing. presente indicativo + vocal opuesta (-ar → -e; -er/-ir → -a)",
        rules=[
            '-ar toma vocal -e; -er/-ir toman vocal -a (principio de "vocal opuesta").',
            "La raíz se toma de la 1ª persona singular del presente de indicativo.",
            "Se usa tras expresiones de deseo, emoción, duda, finalidad y en imperativos negativos.",
            'No se usa subjuntivo tras "creer que / pensar que" en afirmativo, pero sí en negativo.',
        ],
        examples=[
            GrammarExample(text="Quiero que vengas a mi fiesta.", translation=None),
            GrammarExample(text="Espero que tengas un buen viaje.", translation=None),
            GrammarExample(text="No creo que sea buena idea.", translation=None),
            GrammarExample(text="Dudo que llueva hoy.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quiero que vienes.",
                correct="Quiero que vengas.",
                note='Con "querer que" se usa subjuntivo, no indicativo.',
            ),
            GrammarMistake(
                wrong="Espero que tienes un buen día.",
                correct="Espero que tengas un buen día.",
                note='"Esperar que" rige subjuntivo.',
            ),
        ],
        related=[
            "expresiones-deseo",
            "ojala",
            "subjuntivo-recomendacion",
            "subjuntivo-duda",
            "subjuntivo-valoracion",
        ],
    ),
    GrammarTopic(
        slug="expresiones-deseo",
        title="Subjuntivo con expresiones de deseo",
        level="B1",
        category="Subjuntivo",
        summary="Usar el subjuntivo para expresar deseos: espero que, quiero que, deseo que, necesito que.",
        explanation="Las **expresiones de deseo o voluntad** que proyectan una acción hacia el futuro o expresan un deseo sobre otra persona llevan el verbo subordinado en **subjuntivo**.\n\n**Verbo de voluntad + que + subjuntivo**\n\nVerbos de voluntad más comunes:\n- *querer que, desear que, esperar que, necesitar que, preferir que, exigir que, pedir que, rogar que, recomendar que, sugerir que, prohibir que, permitir que*\n\nCuando el sujeto del verbo de voluntad y del verbo subordinado es **el mismo**, se usa el **infinitivo** (no el subjuntivo):\n- *Quiero ir.* (yo quiero + yo voy) -> NO ~~Quiero que yo vaya~~.\n- *Quiero que vayas.* (yo quiero + tú vas) -> correcto con subjuntivo.\n\nEn este uso, *esperar que* expresa deseo y rige subjuntivo.",
        rules=[
            "Verbo de voluntad + que + subjuntivo cuando los sujetos son distintos.",
            'Si el sujeto es el mismo, se usa infinitivo: "Quiero descansar".',
            '"Ojalá" es una expresión de deseo que siempre rige subjuntivo.',
            '"Esperar que" + subjuntivo expresa deseo o expectativa no factual.',
        ],
        examples=[
            GrammarExample(text="Espero que te guste el regalo.", translation=None),
            GrammarExample(
                text="Mis padres quieren que estudie medicina.",
                translation=None,
            ),
            GrammarExample(
                text="Necesito que me ayudes con esto.",
                translation=None,
            ),
            GrammarExample(text="Prefiero que vengáis mañana.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Espero que te gusta.",
                correct="Espero que te guste.",
                note='"Esperar que" rige subjuntivo, no indicativo.',
            ),
            GrammarMistake(
                wrong="Quiero que yo vaya.",
                correct="Quiero ir.",
                note="Cuando el sujeto es el mismo, se usa infinitivo.",
            ),
        ],
        related=["subjuntivo-presente", "ojala", "subjuntivo-recomendacion"],
    ),
    GrammarTopic(
        slug="ojala",
        title="Ojalá + subjuntivo",
        level="B1",
        category="Subjuntivo",
        summary="La expresión de deseo más intensa del español, de origen árabe.",
        explanation='**Ojalá** es una de las expresiones más características del español. Procede del árabe hispánico *law šáʼ Alláh* ("si Dios quisiera"). Se usa para expresar un **deseo intenso**.\n\n**Ojalá + presente de subjuntivo**: deseo sobre el presente o futuro que se considera **posible**.\n- *Ojalá llueva mañana.*\n- *Ojalá (que) lleguen a tiempo.*\n\n**Ojalá + imperfecto de subjuntivo**: deseo sobre el presente considerado **difícil o improbable**.\n- *Ojalá tuviera más tiempo.*\n\n**Ojalá + pluscuamperfecto de subjuntivo**: deseo sobre el pasado que **no se cumplió** (irreal).\n- *Ojalá hubiera estudiado más.*\n\nLa conjunción "que" es opcional: *Ojalá que venga* = *Ojalá venga*.',
        structure="ojalá (que) + presente de subjuntivo (posible) · imperfecto/pluscuamperfecto de subjuntivo (difícil/imposible)",
        rules=[
            '"Ojalá" rige siempre subjuntivo. Nunca lleva indicativo.',
            "Con presente de subjuntivo: deseo realizable en el presente/futuro.",
            "Con imperfecto de subjuntivo: deseo difícil o contrario a la realidad presente.",
            "Con pluscuamperfecto de subjuntivo: deseo sobre un pasado que no se cumplió.",
        ],
        examples=[
            GrammarExample(text="Ojalá pueda ir a tu boda.", translation=None),
            GrammarExample(
                text="Ojalá no llueva durante las vacaciones.",
                translation=None,
            ),
            GrammarExample(
                text="Ojalá tuviera más dinero.",
                translation=None,
                note="deseo difícil",
            ),
            GrammarExample(
                text="Ojalá hubiera aprendido español de niño.",
                translation=None,
                note="deseo irreal sobre el pasado",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ojalá tengo tiempo.",
                correct="Ojalá tenga tiempo.",
                note='"Ojalá" siempre rige subjuntivo.',
            ),
            GrammarMistake(
                wrong="Ojalá que vendrá.",
                correct="Ojalá que venga.",
                note='No se usa futuro con "ojalá".',
            ),
        ],
        related=[
            "expresiones-deseo",
            "subjuntivo-presente",
            "subjuntivo-imperfecto",
            "pluscuamperfecto",
        ],
    ),
    GrammarTopic(
        slug="subjuntivo-recomendacion",
        title="Subjuntivo con recomendaciones y consejos",
        level="B1",
        category="Subjuntivo",
        summary="Aconsejar y recomendar usando el subjuntivo.",
        explanation="Las **recomendaciones, consejos y sugerencias** que se dirigen a otra persona llevan el verbo subordinado en **subjuntivo**.\n\n**Verbo de influencia + que + subjuntivo**\n\nVerbos de influencia más comunes:\n- *recomendar que, sugerir que, aconsejar que, proponer que, insistir en que, rogar que, suplicar que, pedir que*\n\nTambién funcionan con esta estructura las expresiones impersonales:\n- *Es recomendable que, Es aconsejable que, Es importante que, Es necesario que, Conviene que, Más vale que*\n\nEjemplos:\n- *Te recomiendo que **leas** este libro.*\n- *Es importante que **lleguéis** puntuales.*",
        structure="recomendar/sugerir/aconsejar + que + subjuntivo",
        rules=[
            "Verbos de influencia + que + subjuntivo cuando el sujeto de la influencia es distinto.",
            "Cuando el sujeto es el mismo, se usa infinitivo.",
            '"Decir que" pidiendo acción rige subjuntivo; informando rige indicativo.',
            '"Insistir en que" + subjuntivo significa presionar; + indicativo significa repetir afirmación.',
        ],
        examples=[
            GrammarExample(
                text="Te recomiendo que visites Granada.",
                translation=None,
            ),
            GrammarExample(
                text="Es importante que bebas mucha agua en verano.",
                translation=None,
            ),
            GrammarExample(
                text="Sugiero que lleguéis media hora antes.",
                translation=None,
            ),
            GrammarExample(
                text="Conviene que reserves con antelación.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Recomiendo que visitas Granada.",
                correct="Recomiendo que visites Granada.",
                note='"Recomendar que" rige subjuntivo.',
            ),
            GrammarMistake(
                wrong="Es importante que llegas puntual.",
                correct="Es importante que llegues puntual.",
                note="Las expresiones impersonales de influencia rigen subjuntivo.",
            ),
        ],
        related=["subjuntivo-presente", "expresiones-deseo", "imperativo-afirmativo"],
    ),
    GrammarTopic(
        slug="subjuntivo-duda",
        title="Subjuntivo con expresiones de duda",
        level="B1",
        category="Subjuntivo",
        summary="Usar el subjuntivo para expresar duda, probabilidad baja o negación.",
        explanation="Las **expresiones de duda o incertidumbre** llevan el verbo subordinado en **subjuntivo**. La regla fundamental es:\n\n**Afirmación** (certeza) → **indicativo**\n**Negación de la afirmación** (duda) → **subjuntivo**\n\n| Certeza (indicativo) | Duda (subjuntivo) |\n|---------------------|-------------------|\n| Creo que viene | No creo que venga |\n| Pienso que es cierto | No pienso que sea cierto |\n| Estoy seguro de que sabe | No estoy seguro de que sepa |\n| Es verdad que llueve | No es verdad que llueva |\n\nExpresiones que siempre llevan subjuntivo:\n- *Dudo que..., Es posible que..., Puede (ser) que..., Quizá(s)..., Tal vez...* (cuando el hablante expresa verdadera duda).",
        structure="dudar que / no creer que / es posible que + subjuntivo",
        rules=[
            'Con verbos de opinión en negativo rigen subjuntivo: "No creo que venga".',
            'Los verbos de duda siempre rigen subjuntivo: "Dudo que sepas".',
            '"Quizá(s)" y "tal vez" pueden llevar indicativo o subjuntivo según el grado de certeza.',
            '"Es posible/probable que" siempre rige subjuntivo.',
        ],
        examples=[
            GrammarExample(text="No creo que él tenga razón.", translation=None),
            GrammarExample(
                text="Dudo que puedan terminar a tiempo.",
                translation=None,
            ),
            GrammarExample(
                text="Es posible que llueva mañana.",
                translation=None,
            ),
            GrammarExample(
                text="Quizás vayamos a la playa este fin de semana.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="No creo que tiene razón.",
                correct="No creo que tenga razón.",
                note='"No creer que" rige subjuntivo, no indicativo.',
            ),
            GrammarMistake(
                wrong="Dudo que viene.",
                correct="Dudo que venga.",
                note='"Dudar que" siempre rige subjuntivo.',
            ),
        ],
        related=["subjuntivo-presente", "subjuntivo-valoracion", "expresiones-deseo"],
    ),
    GrammarTopic(
        slug="subjuntivo-valoracion",
        title="Subjuntivo con expresiones de valoración",
        level="B1",
        category="Subjuntivo",
        summary="Emitir juicios y valoraciones con el subjuntivo: es bueno que, me alegra que, me sorprende que.",
        explanation="Las **expresiones de valoración o reacción emocional** rigen **subjuntivo** cuando el verbo subordinado tiene un sujeto diferente. La estructura es:\n\n**ser/estar + adjetivo + que + subjuntivo**:\n- *Es bueno que **hayas** venido.*\n- *Es injusto que **tengan** que pagar tanto.*\n- *Está mal que **digas** eso.*\n\n**Verbos de emoción + que + subjuntivo**:\n- *Me alegra que **estés** aquí.*\n- *Me molesta que **llegues** tarde.*\n- *Me sorprende que no lo **sepas**.*\n- *Siento que no **puedas** venir.*\n- *Temo que **haya** problemas.*\n\nAdjetivos comunes con esta estructura: *bueno, malo, lógico, normal, raro, extraño, increíble, estupendo, maravilloso, horrible, terrible, injusto, justo, importante, necesario*.",
        structure="ser/estar + adjetivo + que + subjuntivo · me alegra/molesta/sorprende + que + subjuntivo",
        rules=[
            "Expresiones impersonales de valoración + que + subjuntivo.",
            "Verbos de emoción (alegrar, molestar, sorprender, gustar, temer, sentir) + que + subjuntivo.",
            'Cuando el sujeto es el mismo, se usa infinitivo: "Me alegra estar aquí".',
            '"Es cierto/evidente/obvio que" NO rigen subjuntivo (expresan certeza).',
        ],
        examples=[
            GrammarExample(
                text="Me alegra que hayas encontrado trabajo.",
                translation=None,
            ),
            GrammarExample(
                text="Es increíble que no lo sepas.",
                translation=None,
            ),
            GrammarExample(
                text="Siento que no puedas venir a la boda.",
                translation=None,
            ),
            GrammarExample(
                text="Es normal que estés cansado después del viaje.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Me alegra que estás aquí.",
                correct="Me alegra que estés aquí.",
                note="Las expresiones de emoción rigen subjuntivo.",
            ),
            GrammarMistake(
                wrong="Es bueno que haces ejercicio.",
                correct="Es bueno que hagas ejercicio.",
                note='"Es bueno que" rige subjuntivo.',
            ),
        ],
        related=["subjuntivo-presente", "subjuntivo-duda", "expresiones-deseo"],
    ),
    GrammarTopic(
        slug="pluscuamperfecto",
        title="Pretérito pluscuamperfecto",
        level="B1",
        category="Tiempos verbales",
        summary="Había hablado, habías comido... — acción pasada anterior a otra pasada.",
        explanation="El **pretérito pluscuamperfecto** expresa una acción pasada **anterior a otra acción también pasada**. Se forma con el **imperfecto de haber + participio**.\n\n| Persona | Haber (imperfecto) | + Participio |\n|---------|-------------------|--------------|\n| yo | había | hablado/comido/vivido |\n| tú | habías | hablado/comido/vivido |\n| él/ella/usted | había | hablado/comido/vivido |\n| nosotros | habíamos | hablado/comido/vivido |\n| vosotros | habíais | hablado/comido/vivido |\n| ellos/ellas/uds. | habían | hablado/comido/vivido |\n\nEs muy frecuente en narraciones para marcar que algo ocurrió antes que el punto de referencia pasado.\n\nEjemplo: *Cuando llegué, ella ya se había ido.*",
        structure="haber (imperfecto: había/habías/había/habíamos/habíais/habían) + participio",
        rules=[
            "Acción pasada anterior a otra acción pasada.",
            "Se forma con el imperfecto de haber + participio invariable.",
            "Frecuente en narraciones para establecer orden cronológico.",
            'Con "ya" y "todavía no" en pasado: "Ya había salido cuando llamé".',
        ],
        examples=[
            GrammarExample(
                text="Cuando llegué al cine, la película ya había empezado.",
                translation=None,
            ),
            GrammarExample(
                text="Nunca había visto algo tan bonito.",
                translation=None,
            ),
            GrammarExample(
                text="No habían terminado los deberes cuando llegó su madre.",
                translation=None,
            ),
            GrammarExample(
                text="Me dijo que ya había estado en ese restaurante.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Cuando llegué, ellos ya habían comidos.",
                correct="Cuando llegué, ellos ya habían comido.",
                note="El participio con haber no concuerda con el sujeto: habían comido.",
            ),
            GrammarMistake(
                wrong="Nunca he visto algo tan bonito hasta ese día.",
                correct="Nunca había visto algo tan bonito hasta ese día.",
                note="Hasta un momento pasado se usa pluscuamperfecto, no perfecto.",
            ),
        ],
        related=["preterito-perfecto", "marcadores-perfecto", "secuencia-temporal"],
    ),
    GrammarTopic(
        slug="marcadores-perfecto",
        title="Marcadores temporales del perfecto",
        level="B1",
        category="Adjetivos y adverbios",
        summary="Hoy, esta semana, ya, todavía no, nunca, alguna vez — marcadores del pretérito perfecto.",
        explanation="Los **marcadores temporales** orientan la elección del pasado, pero no determinan por sí solos un único tiempo.\n\nEn buena parte de España, el perfecto es frecuente con periodos que se consideran abiertos (*hoy, esta semana, este año*) o experiencias conectadas con el presente (*alguna vez, todavía no, últimamente*). Para hechos en periodos cerrados, como *ayer* o *el año pasado*, suele emplearse el indefinido.\n\nHay variación regional y contextual: *Hoy fui al médico* es correcta y habitual en muchas zonas. *Nunca fui a ese colegio* y *Nunca he ido a ese colegio* presentan la experiencia desde perspectivas distintas. *Esta mañana* puede considerarse un periodo abierto o cerrado según cuándo y cómo se relate. No conviertas los marcadores en reglas automáticas.",
        rules=[
            "En buena parte de España, un periodo abierto favorece el perfecto, sin excluir otros usos regionales.",
            "Un periodo presentado como cerrado favorece el indefinido; considera también el contexto y la variedad.",
            '"Ya" y "todavía no" van frecuentemente con perfecto para expresar acciones completadas o pendientes.',
            '"Nunca" y "alguna vez" con perfecto para experiencias vitales.',
        ],
        examples=[
            GrammarExample(
                text="Esta semana he ido al gimnasio tres veces.",
                translation=None,
            ),
            GrammarExample(
                text="¿Alguna vez has probado el ceviche?",
                translation=None,
            ),
            GrammarExample(
                text="Todavía no he encontrado las llaves.",
                translation=None,
            ),
            GrammarExample(
                text="Últimamente no hemos tenido mucho trabajo.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["preterito-perfecto", "pluscuamperfecto", "marcadores-temporales"],
    ),
    GrammarTopic(
        slug="voz-pasiva",
        title="Voz pasiva con ser + participio",
        level="B1",
        category="Voz pasiva",
        summary="Construir oraciones pasivas: ser + participio (+ por + agente).",
        explanation='La **voz pasiva** en español se forma con el verbo **ser + participio**. A diferencia del perfecto, aquí el participio **sí concuerda en género y número** con el sujeto paciente.\n\n| Voz activa | Voz pasiva |\n|-----------|-----------|\n| El chef preparó la cena. | La cena **fue preparada** por el chef. |\n| Los alumnos entregaron los trabajos. | Los trabajos **fueron entregados** por los alumnos. |\n| Cervantes escribió el Quijote. | El Quijote **fue escrito** por Cervantes. |\n\nLa voz pasiva es mucho menos frecuente en español que en inglés. Se prefiere:\n- La **pasiva refleja** con "se": *Se venden pisos.*\n- La **voz activa** con cambio de orden: *El Quijote lo escribió Cervantes.*\n\nLa pasiva con "ser" es más propia de registros formales, periodísticos y académicos.',
        structure="sujeto paciente + ser (conjugado) + participio (concuerda) + (por + agente)",
        rules=[
            'El verbo "ser" se conjuga en el tiempo que corresponda.',
            "El participio concuerda en género y número con el sujeto paciente.",
            'El agente se introduce con "por" (a veces "de" para estados mentales).',
            "No confundir pasiva de proceso (ser + participio) con pasiva de resultado (estar + participio).",
        ],
        examples=[
            GrammarExample(
                text="El edificio fue diseñado por un arquitecto famoso.",
                translation=None,
            ),
            GrammarExample(
                text="Las cartas serán enviadas mañana.",
                translation=None,
            ),
            GrammarExample(
                text="La decisión ha sido tomada por el comité.",
                translation=None,
            ),
            GrammarExample(
                text="Los ladrones fueron detenidos por la policía.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="La cena fue preparado por el chef.",
                correct="La cena fue preparada por el chef.",
                note="El participio debe concordar con el sujeto paciente (cena, femenino).",
            ),
            GrammarMistake(
                wrong="Los libros fueron escrito por Cervantes.",
                correct="Los libros fueron escritos por Cervantes.",
                note="En la pasiva con ser, el participio concuerda con el sujeto paciente plural.",
            ),
        ],
        related=["se-impersonal", "se-pasivo", "pasiva-refleja"],
    ),
    GrammarTopic(
        slug="se-impersonal",
        title="Se impersonal",
        level="B1",
        category="Voz pasiva",
        summary='Construcciones impersonales con "se": Se vive bien aquí. Se recibió a los invitados.',
        explanation="El **se impersonal** presenta acciones con un agente humano no especificado y **sin sujeto gramatical**. El verbo va en tercera persona del singular:\n- *Se vive bien en esta ciudad*.\n- *Se trabaja mucho aquí*.\n- *Se recibió a los invitados*.\n\nCon un complemento directo de persona determinada se conserva la a personal: *Se busca a los responsables*. No se hace concordar el verbo con ese complemento plural.\n\nNo debe confundirse con la pasiva refleja: en *Se necesitan camareros*, camareros es sujeto paciente y el verbo concuerda con él. Con un sintagma singular, como *Se habla español*, la forma del verbo no basta para distinguir las construcciones.",
        structure="se + verbo en 3ª persona singular",
        rules=[
            "El verbo va en 3ª persona singular, nunca en plural.",
            "La construcción es impersonal: no hay sujeto.",
            'Con complemento directo de persona determinada se mantiene la a personal: "Se busca a los testigos".',
            "En la pasiva refleja el verbo concuerda con el sujeto paciente, no con un objeto.",
        ],
        examples=[
            GrammarExample(
                text="Se trabaja mucho en la recepción.",
                translation=None,
            ),
            GrammarExample(
                text="Se come muy bien en este restaurante.",
                translation=None,
            ),
            GrammarExample(text="Se vive bien en esta ciudad.", translation=None),
            GrammarExample(
                text="Se busca a los criminales.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se vende coches aquí.",
                correct="Se venden coches aquí.",
                note='Con "coches" (plural), en pasiva refleja el verbo debe concordar: "se venden".',
            ),
            GrammarMistake(
                wrong="Se busca los documentos.",
                correct="Se buscan los documentos.",
                note="Con cosa se suele usar pasiva refleja con concordancia: se buscan.",
            ),
        ],
        related=["se-pasivo", "voz-pasiva", "pasiva-refleja"],
    ),
    GrammarTopic(
        slug="se-pasivo",
        title="Pasiva refleja (se + verbo)",
        level="B1",
        category="Voz pasiva",
        summary='Se venden pisos, se alquilan coches — la pasiva con "se" más natural del español.',
        explanation="La **pasiva refleja** es la forma pasiva más común en español. Se construye con **se + verbo en tercera persona** y el verbo **concuerda en número** con el sujeto paciente (el objeto de la acción).\n\n- *Se vende piso.* (singular: un piso)\n- *Se venden pisos.* (plural: varios pisos)\n\nA diferencia del se impersonal (siempre singular), en la pasiva refleja el verbo puede ir en plural:\n- *Se alquila apartamento.* → un apartamento\n- *Se alquilan apartamentos.* → varios apartamentos\n\n**Diferencias con la voz pasiva con ser**:\n- Ser + participio → más formal, menos frecuente, suele mencionar agente.\n- Se + verbo → más natural y frecuente, no menciona agente.",
        structure="se + verbo en 3ª persona (concuerda con el sujeto paciente)",
        rules=[
            "El verbo concuerda con el sujeto paciente en número: se vende / se venden.",
            "No se menciona el agente.",
            "Es la forma pasiva preferida en español coloquial.",
            'Solo funciona en 3ª persona; no existe "me vendo" como pasiva refleja.',
        ],
        examples=[
            GrammarExample(text="Se venden flores frescas.", translation=None),
            GrammarExample(text="Se alquila habitación.", translation=None),
            GrammarExample(text="Se necesitan voluntarios.", translation=None),
            GrammarExample(
                text="Aquí se hablan varios idiomas.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se vende flores.",
                correct="Se venden flores.",
                note="El verbo debe concordar en número con el sujeto (flores, plural).",
            ),
            GrammarMistake(
                wrong="Se alquila apartamentos.",
                correct="Se alquilan apartamentos.",
                note="En la pasiva refleja hay concordancia de número.",
            ),
        ],
        related=["se-impersonal", "voz-pasiva", "pasiva-refleja"],
    ),
    GrammarTopic(
        slug="que-relativo",
        title="Pronombres relativos: que",
        level="B1",
        category="Oraciones",
        summary="El pronombre relativo más versátil: que para unir oraciones.",
        explanation="El pronombre relativo **que** es el más usado en español. Puede referirse a **personas, cosas o ideas** y funciona como sujeto o complemento directo de la oración subordinada.\n\nUsos:\n- **Con antecedente explícito**: *El libro **que** leí es fascinante.*\n- **Sin antecedente (sustantivado)**: *El **que** quiera participar, que levante la mano.*\n- **Con artículo**: *el que, la que, los que, las que, lo que*: *Lo que dijiste no es cierto.*\n\n**Que vs. quien/cual**:\n- **Que** es el más versátil y se usa en la mayoría de los casos.\n- **Quien** solo para personas y principalmente en explicativas o sin antecedente.\n- **El/la cual** es más formal y se usa con preposiciones o para evitar ambigüedad.",
        structure="antecedente + que + oración subordinada",
        rules=[
            '"Que" es invariable: no cambia de género ni número.',
            "Puede referirse a personas o cosas.",
            'Con preposición: "en que", "con que", "a que", "de que".',
            '"Lo que" se usa para ideas abstractas: "No entiendo lo que dices".',
        ],
        examples=[
            GrammarExample(
                text="La chica que conocí ayer es italiana.",
                translation=None,
            ),
            GrammarExample(
                text="El coche que compré es eléctrico.",
                translation=None,
            ),
            GrammarExample(
                text="Lo que me contaste es increíble.",
                translation=None,
            ),
            GrammarExample(
                text="La ciudad en que vivo es muy tranquila.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="La ciudad que vivo es tranquila.",
                correct="La ciudad en que vivo es tranquila. / La ciudad donde vivo es tranquila.",
                note='Con complemento de lugar se necesita preposición o usar "donde".',
            ),
            GrammarMistake(
                wrong="El chico cual vino ayer.",
                correct="El chico que vino ayer.",
                note='"El cual" no se usa como sujeto de oraciones especificativas.',
            ),
        ],
        related=["donde-cuando-relativo", "cuyo", "se-impersonal"],
    ),
    GrammarTopic(
        slug="donde-cuando-relativo",
        title="Pronombres relativos: donde y cuando",
        level="B1",
        category="Oraciones",
        summary="Usar donde (lugar) y cuando (tiempo) como relativos.",
        explanation="**Donde** y **cuando** funcionan como adverbios relativos que introducen oraciones subordinadas de lugar y tiempo respectivamente.\n\n**Donde**:\n- Se refiere a un lugar mencionado antes.\n- *Esta es la casa **donde** nací.*\n- Puede llevar preposición: *adonde, en donde, de donde, por donde*.\n- *El pueblo **de donde** vengo es muy pequeño.*\n\n**Cuando**:\n- Se refiere a un momento temporal.\n- *Recuerdo el día **cuando** nos conocimos.*\n- Con subjuntivo expresa futuro: *Cuando **llegues**, llámame.*\n\nTambién pueden usarse sin antecedente explícito:\n- *Ponlo **donde** quieras.*\n- *Ven **cuando** puedas.*",
        structure="antecedente + donde/cuando + oración subordinada",
        rules=[
            '"Donde" para lugar; con preposición según el verbo: ir a → adonde / a donde.',
            '"Cuando" para tiempo; con subjuntivo para acciones futuras.',
            '"Donde" y "cuando" pueden sustituirse por "en que": "la casa en que nací".',
            "Sin antecedente funcionan como conjunciones subordinantes.",
        ],
        examples=[
            GrammarExample(
                text="El bar donde quedamos está en el centro.",
                translation=None,
            ),
            GrammarExample(
                text="Volveré a la ciudad donde crecí.",
                translation=None,
            ),
            GrammarExample(
                text="Llegó justo cuando empezábamos a comer.",
                translation=None,
            ),
            GrammarExample(text="Cuando termines, avísame.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="La ciudad adonde vivo.",
                correct="La ciudad donde vivo. / La ciudad en la que vivo.",
                note='"Adonde" implica dirección (ir a); para ubicación se usa "donde" o "en donde".',
            ),
        ],
        related=["que-relativo", "cuyo", "conectores-narrativos"],
    ),
    GrammarTopic(
        slug="cuyo",
        title="El relativo posesivo cuyo",
        level="B1",
        category="Oraciones",
        summary="El pronombre relativo de posesión: cuyo, cuya, cuyos, cuyas.",
        explanation='**Cuyo** es el único pronombre relativo que expresa **posesión**. Tiene cuatro formas que **concuerdan en género y número con el sustantivo que sigue** (la cosa poseída), no con el antecedente.\n\n- *cuyo* (masc. sing.) · *cuya* (fem. sing.) · *cuyos* (masc. pl.) · *cuyas* (fem. pl.)\n\nEjemplos:\n- *El escritor **cuya** novela ganó el premio es colombiano.* → La novela (fem. sing.) del escritor.\n- *La empresa **cuyos** empleados están en huelga.* → Los empleados (masc. pl.) de la empresa.\n\nCuyo equivale a "whose" en inglés, pero concuerda con lo poseído, no con el poseedor. Es propio del registro formal; en lenguaje coloquial se evita con construcciones como "que su": *El escritor que su novela ganó...* (coloquial pero frecuente).',
        structure="antecedente + cuyo/a/os/as + sustantivo + oración",
        rules=[
            "Concuerda en género y número con el sustantivo que lo sigue (la cosa poseída).",
            "No concuerda con el antecedente (el poseedor).",
            'Nunca lleva artículo: "el cuyo libro" es incorrecto.',
            'En registro coloquial se sustituye a menudo por "que su".',
        ],
        examples=[
            GrammarExample(
                text="El autor cuyo libro leí ayer es argentino.",
                translation=None,
            ),
            GrammarExample(
                text="La ciudad cuyas calles son tan estrechas es Toledo.",
                translation=None,
            ),
            GrammarExample(
                text="Es una persona de cuya honestidad no dudo.",
                translation=None,
            ),
            GrammarExample(
                text="Los estudiantes cuyos trabajos fueron seleccionados recibirán un premio.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="El escritor cuyo su libro es famoso.",
                correct="El escritor cuyo libro es famoso.",
                note='"Cuyo" ya incluye el valor posesivo; "su" es redundante.',
            ),
            GrammarMistake(
                wrong="La chica cuya el padre es médico.",
                correct="La chica cuyo padre es médico.",
                note='"Cuyo" concuerda con "padre" (masc.), no con "chica". No lleva artículo.',
            ),
        ],
        related=["que-relativo", "donde-cuando-relativo", "adjetivos-posesivos"],
    ),
    GrammarTopic(
        slug="condicional-compuesto",
        title="Condicional compuesto",
        level="B1",
        category="Condicionales",
        summary="Habría hablado, habrías comido — hipótesis sobre el pasado, consejos no seguidos.",
        explanation="El **condicional compuesto** se forma con el condicional simple de **haber + participio**. Expresa:\n\n- **Consecuencia no realizada de una condición irreal pasada**:\n  *Si hubiera estudiado, **habría aprobado**.*\n\n- **Conjetura o probabilidad sobre el pasado**:\n  *No sé qué pasó. Se **habría enfadado**.* (Probablemente se enfadó.)\n\n- **Consejo o reproche sobre algo que ya no se puede cambiar**:\n  *Deberías haberme avisado. / **Habrías debido** llamar antes.*\n\n- **Futuro del pasado en estilo indirecto sobre acciones anteriores**:\n  *Dijo que cuando llegáramos ya **habría terminado**.*",
        structure="haber (condicional simple: habría/habrías/habría/habríamos/habríais/habrían) + participio",
        rules=[
            "Condicional simple de haber + participio invariable.",
            "Expresa la apódosis de condicionales irreales de pasado.",
            'También conjetura sobre el pasado: "Habrían sido las tres".',
            'En registro coloquial se sustituye a menudo por pluscuamperfecto de subjuntivo: "Si hubiera estudiado, hubiera aprobado".',
        ],
        examples=[
            GrammarExample(
                text="Si me lo hubieras dicho, te habría ayudado.",
                translation=None,
            ),
            GrammarExample(
                text="No contestan. Se habrían ido ya.",
                translation=None,
                note="conjetura",
            ),
            GrammarExample(
                text="Habrías disfrutado mucho en la fiesta.",
                translation=None,
            ),
            GrammarExample(
                text="Dijo que para entonces ya habría llegado.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Si habrías estudiado, habrías aprobado.",
                correct="Si hubieras estudiado, habrías aprobado.",
                note='En la prótasis con "si" nunca se usa condicional.',
            ),
            GrammarMistake(
                wrong="Habría ido si tenía tiempo.",
                correct="Habría ido si hubiera tenido tiempo.",
                note="Condición irreal pasada pide pluscuamperfecto de subjuntivo.",
            ),
        ],
        related=["condicional-simple", "si-imperfecto-subjuntivo", "pluscuamperfecto"],
    ),
    GrammarTopic(
        slug="si-imperfecto-subjuntivo",
        title="Condicionales irreales: si + imperfecto de subjuntivo",
        level="B1",
        category="Condicionales",
        summary="Condiciones hipotéticas o contrarias a la realidad presente.",
        explanation='Las **condicionales de segundo tipo** expresan condiciones **hipotéticas, improbables o contrarias a la realidad presente**. La estructura es:\n\n**Si + imperfecto de subjuntivo, + condicional simple**\n\n- *Si **tuviera** dinero, **viajaría** por el mundo.* (No tengo dinero ahora.)\n- *Si **fueras** más organizado, **terminarías** a tiempo.* (No eres organizado.)\n- *Si **viviera** en la playa, **estaría** feliz.* (No vivo en la playa.)\n\nTambién se puede invertir el orden: *Viajaría por el mundo si tuviera dinero.*\n\nLa prótasis con "si" NUNCA lleva condicional. El imperfecto de subjuntivo tiene dos formas: -ra (hablara) y -se (hablase). Ambas son correctas, aunque -ra es más frecuente.',
        structure="si + imperfecto de subjuntivo + condicional simple",
        rules=[
            "Si + imperfecto de subjuntivo + condicional simple.",
            "Expresa condición contraria a la realidad presente o improbable.",
            'Nunca usar condicional en la prótasis: "~~Si tendría~~" es incorrecto.',
            "El imperfecto de subjuntivo tiene dos terminaciones: -ra y -se; ambas válidas.",
        ],
        examples=[
            GrammarExample(
                text="Si tuviera más tiempo, aprendería francés.",
                translation=None,
            ),
            GrammarExample(
                text="Si fueras más alto, podrías jugar al baloncesto.",
                translation=None,
            ),
            GrammarExample(
                text="Me compraría esa casa si no fuera tan cara.",
                translation=None,
            ),
            GrammarExample(
                text="Si vivieras aquí, nos veríamos más a menudo.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Si tendría dinero, viajaría.",
                correct="Si tuviera/tuviese dinero, viajaría.",
                note="En la prótasis se usa subjuntivo, no condicional.",
            ),
            GrammarMistake(
                wrong="Si yo sería tú, estudiaría más.",
                correct="Si yo fuera tú, estudiaba más. / Yo que tú, estudiaría más.",
                note='"Si yo fuera" es la forma correcta, con imperfecto de subjuntivo de ser.',
            ),
        ],
        related=[
            "subjuntivo-imperfecto",
            "condicional-simple",
            "condicional-compuesto",
        ],
    ),
    GrammarTopic(
        slug="suposiciones-futuro",
        title="Expresar suposiciones sobre el futuro",
        level="B1",
        category="Condicionales",
        summary="Futuro simple, condicional e indicativo para hacer hipótesis.",
        explanation="El español usa varios mecanismos para expresar **suposiciones, probabilidad y conjetura**, según el marco temporal:\n\n**Sobre el presente**: *futuro simple*\n- *¿Dónde está Juan? — Estará en casa.* (Probablemente está en casa.)\n- *Serán las ocho.* (Probablemente son las ocho.)\n\n**Sobre el pasado**: *condicional simple*\n- *¿Por qué no vino? — Estaría cansado.* (Probablemente estaba cansado.)\n- *Serían las tres cuando llegó.*\n\n**Sobre el futuro**: *futuro simple* o *ir a + infinitivo*\n- *¿Vendrá a la fiesta? — No sé, supongo que sí.*\n- También con adverbios: *quizás, tal vez, a lo mejor* + indicativo/subjuntivo.",
        rules=[
            'Futuro simple para conjetura presente: "Estará en casa" = probablemente está.',
            'Condicional simple para conjetura pasada: "Estaría cansado" = probablemente estaba.',
            '"A lo mejor" + indicativo; "quizás/tal vez" pueden llevar indicativo o subjuntivo.',
            "Las expresiones de probabilidad (es probable/posible que) rigen subjuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Estará en el trabajo, no contesta el móvil.",
                translation=None,
            ),
            GrammarExample(
                text="No sé qué le pasaba; tendría un mal día.",
                translation=None,
            ),
            GrammarExample(text="A lo mejor llueve mañana.", translation=None),
            GrammarExample(text="Es probable que lleguen tarde.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Es probable que llegan tarde.",
                correct="Es probable que lleguen tarde.",
                note='"Es probable que" rige subjuntivo.',
            ),
            GrammarMistake(
                wrong="A lo mejor venga.",
                correct="A lo mejor viene.",
                note='"A lo mejor" siempre rige indicativo.',
            ),
        ],
        related=["futuro-simple", "condicional-simple", "subjuntivo-duda"],
    ),
    GrammarTopic(
        slug="estilo-indirecto-pasado",
        title="Estilo indirecto en pasado",
        level="B1",
        category="Estilo indirecto",
        summary="Transformaciones avanzadas del estilo indirecto con verbos en pretérito.",
        explanation='Al reproducir palabras desde una perspectiva pasada, son frecuentes estas correspondencias:\n\n| Estilo directo | Relato desde el pasado |\n|---------------|------------------------|\n| "Voy" | Dijo que **iba** |\n| "He ido" | Dijo que **había ido** |\n| "Fui" | Dijo que **había ido** / que **fue**, según el contexto |\n| "Iba" | Dijo que **iba** |\n| "Había ido" | Dijo que **había ido** |\n| "Iré" | Dijo que **iría** |\n| "Habré ido" | Dijo que **habría ido** |\n| "Iría" | Dijo que **iría** |\n\nNo hay un retroceso obligatorio de todos los tiempos: *Dijo que vive aquí* es posible si sigue viviendo aquí; *Dijo que vendrá mañana* mantiene una referencia futura vigente.\n\nLas órdenes y peticiones se reproducen con subjuntivo: *Me pidió que fuera* o, si la petición se proyecta sobre un momento aún vigente, *Me pidió que vaya mañana*. Ajusta personas y referencias al contexto real.',
        rules=[
            "Desde una perspectiva pasada, el presente suele pasar a imperfecto y los hechos anteriores pueden expresarse en pluscuamperfecto.",
            "El imperfecto, el pluscuamperfecto y el condicional pueden mantenerse; la elección depende de la relación temporal.",
            "El futuro suele pasar a condicional desde una perspectiva pasada; las peticiones se reproducen con subjuntivo.",
            'Las preguntas indirectas no llevan signos de interrogación: "Preguntó qué quería".',
        ],
        examples=[
            GrammarExample(
                text="Me dijo que había estado en Madrid el verano anterior.",
                translation=None,
            ),
            GrammarExample(
                text="Preguntó si íbamos a venir a la cena.",
                translation=None,
            ),
            GrammarExample(
                text="Me pidió que le ayudara con la mudanza.",
                translation=None,
                note="imperativo → subjuntivo",
            ),
            GrammarExample(
                text="Explicó que para entonces ya habrían terminado.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Dijo de que había ido al médico.",
                correct="Dijo que había ido al médico.",
                note="Decir introduce el contenido con que, sin de.",
            ),
            GrammarMistake(
                wrong="Me pidió que le ayudo.",
                correct="Me pidió que le ayudara/ayudase.",
                note="Petición en pasado → imperfecto de subjuntivo.",
            ),
        ],
        related=["estilo-indirecto", "cambios-temporales", "subjuntivo-imperfecto"],
    ),
    GrammarTopic(
        slug="tildes-diacriticas",
        title="Tildes diacríticas frecuentes",
        level="B1",
        category="Oraciones",
        summary="Diferencias de significado en pares como tu/tú, el/él, mas/más, se/sé, de/dé.",
        explanation="La **tilde diacrítica** diferencia palabras que se escriben igual pero tienen función distinta.\n\nPares de alta frecuencia:\n- **tu / tú**: *tu casa* (posesivo) vs *tú vienes* (pronombre).\n- **el / él**: *el libro* (artículo) vs *él habla* (pronombre).\n- **mi / mí**: *mi coche* vs *para mí*.\n- **de / dé**: *vas de azul* vs *quiero que me dé tiempo*.\n- **se / sé**: *se fue* (pronombre) vs *sé la respuesta* (verbo saber).\n- **mas / más**: *mas no pude* (conjunción formal) vs *más tarde* (cantidad).\n- **si / sí**: *si vienes* (condición) vs *sí, claro* (afirmación).\n- **aun / aún**: *aun cansado* (= incluso) vs *aún no llega* (= todavía).\n\nAdemás, los interrogativos y exclamativos llevan tilde en preguntas directas e indirectas: **qué, quién, cuál, cómo, cuándo, cuánto, dónde**.",
        structure="palabra sin tilde (funcion gramatical) · palabra con tilde (valor diacritico)",
        rules=[
            "La tilde diacrítica distingue funciones gramaticales y significado.",
            "Qué, quién, cuál, cómo, cuándo, cuánto y dónde llevan tilde en interrogativas y exclamativas directas e indirectas.",
            "Aun = incluso; aún = todavía.",
            "Mas sin tilde es conjunción de registro formal; más expresa cantidad.",
        ],
        examples=[
            GrammarExample(text="Tu hermano dijo que tú llegabas hoy.", translation=None),
            GrammarExample(text="No sé si él vendrá.", translation=None),
            GrammarExample(text="Aún no sé qué hacer.", translation=None),
            GrammarExample(text="Quiero que me dé una respuesta clara.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Tu tienes razon, mas yo no.",
                correct="Tú tienes razón, más yo no.",
                note="Faltan tildes diacríticas y acentuación léxica.",
            ),
            GrammarMistake(
                wrong="No se que quieres.",
                correct="No sé qué quieres.",
                note="Sé (verbo saber) y qué interrogativo llevan tilde.",
            ),
        ],
        related=[
            "conectores-argumentativos",
            "estilo-indirecto-pasado",
            "acentuacion-general",
        ],
    ),
    GrammarTopic(
        slug="g-j-h",
        title="Ortografía de g, j y h",
        level="B1",
        category="Verbos",
        summary="Reglas productivas de g/j en verbos y uso frecuente de h en familias léxicas.",
        explanation="En B1 conviene consolidar reglas ortográficas que afectan mucho a la escritura:\n\n**g / j en verbos**\n- Verbos en **-ger/-gir**: ante *o/a* suele aparecer **j** en algunas formas: *dirigir -> dirijo*, *escoger -> escojo*.\n- Se mantiene **g** ante *e/i*: *diriges, dirigimos*.\n\n**j en palabras frecuentes**\n- *trabajo, viaje, ajeno, juventud*.\n\n**h etimológica**\n- No suena, pero se escribe en muchas familias: *hacer/hecho*, *hervir/hervido*, *humo/fumar* (sin h en derivados no emparentados).\n- Se escribe h en formas de *haber*: *he, has, ha, hemos, han*.",
        structure="-ger/-gir: g ante e/i, j en ciertas formas ante o/a · h etimologica en familias frecuentes",
        rules=[
            "En muchos verbos -ger/-gir, la primera persona del presente lleva j: dirijo, escojo.",
            "Las formas de haber se escriben con h: he, has, ha, hemos, han.",
            "La h no suena, pero su ausencia puede cambiar la corrección ortográfica.",
            "Conviene aprender familias léxicas completas para fijar la grafía.",
        ],
        examples=[
            GrammarExample(text="Siempre dirijo yo la reunión.", translation=None),
            GrammarExample(text="Hoy he hecho la tarea.", translation=None),
            GrammarExample(text="Ellos escogieron una opción más segura.", translation=None),
            GrammarExample(text="La juventud necesita oportunidades.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Yo dirigo el proyecto.",
                correct="Yo dirijo el proyecto.",
                note="Primera persona de dirigir se escribe con j.",
            ),
            GrammarMistake(
                wrong="A echo un gran esfuerzo.",
                correct="Ha hecho un gran esfuerzo.",
                note="Ha (haber) y hecho (participio de hacer) se escriben con h.",
            ),
        ],
        related=["preterito-irregular", "imperativo-irregular", "b-v-basico"],
    ),
]
