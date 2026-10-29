"""Spanish grammar topics — A2."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="preterito-perfecto",
        title="Pretérito perfecto compuesto",
        level="A2",
        category="Tiempos verbales",
        summary="He hablado, has comido, han vivido — experiencias y hechos pasados vinculados al presente.",
        explanation="El **pretérito perfecto compuesto** se forma con el presente de **haber + participio**. El participio es invariable: *he comido*, no *he comida*.\n\n| Persona | Haber | Participio |\n|---------|-------|------------|\n| yo | he | hablado/comido/vivido |\n| tú | has | hablado/comido/vivido |\n| él/ella/usted | ha | hablado/comido/vivido |\n| nosotros/as | hemos | hablado/comido/vivido |\n| vosotros/as | habéis | hablado/comido/vivido |\n| ellos/ellas/ustedes | han | hablado/comido/vivido |\n\nSe utiliza para experiencias (*He visitado Japón*), resultados vinculados al presente (*He perdido las llaves*) y, en buena parte de España, hechos dentro de un periodo que se considera abierto (*Hoy he ido al médico*).\n\nEl contraste *hoy he ido / ayer fui* es frecuente en buena parte de España, pero no universal. En muchas variedades americanas y en algunas zonas españolas se usa también el indefinido en contextos como *Hoy fui al médico*. Los marcadores temporales orientan la elección, pero no imponen siempre un único tiempo.",
        structure="haber (he/has/ha/hemos/habéis/han) + participio (-ado/-ido)",
        rules=[
            "El participio no concuerda con el sujeto: ella ha comido, ellas han comido.",
            "Participios regulares: hablar → hablado, comer → comido, vivir → vivido.",
            "Participios irregulares frecuentes: hecho, dicho, visto, escrito, puesto, vuelto, roto, muerto, abierto, cubierto.",
            "Hoy, esta semana, ya, todavía no y alguna vez aparecen con frecuencia con el perfecto; su uso depende del contexto y de la variedad.",
        ],
        examples=[
            GrammarExample(text="Hoy he comido paella.", translation=None),
            GrammarExample(text="¿Has estado alguna vez en México?", translation=None),
            GrammarExample(text="Todavía no hemos terminado el proyecto.", translation=None),
            GrammarExample(text="Ya he visto esa película.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ella ha comida paella.",
                correct="Ella ha comido paella.",
                note="Con haber, el participio es invariable.",
            ),
            GrammarMistake(
                wrong="Han rompido la ventana.",
                correct="Han roto la ventana.",
                note='El participio de romper es "roto".',
            ),
        ],
        related=["pluscuamperfecto", "marcadores-perfecto", "preterito-indefinido-regular"],
    ),
    GrammarTopic(
        slug="por-para",
        title="Por y para: usos y diferencias",
        level="A2",
        category="Preposiciones",
        summary="Usos de por (causa, medio y recorrido) y para (finalidad, destinatario y plazo).",
        explanation="**Por** y **para** tienen distintos usos según el contexto.\n\n**Por**:\n- Causa: *Llegué tarde por el tráfico*.\n- Medio: *Te llamo por teléfono*.\n- Recorrido: *Paseamos por el parque*.\n- Ubicación aproximada: *Está por aquí*.\n- Parte del día: *Llegaré por la tarde*.\n- Precio: *Lo compré por diez euros*.\n- Frecuencia: *Voy dos veces por semana*.\n- Sustitución: *Hoy trabajo por mi compañero*.\n\n**Para**:\n- Finalidad: *Estudio para aprender*.\n- Destinatario: *El regalo es para ti*.\n- Dirección: *Salgo para Madrid*.\n- Plazo: *Lo necesito para el lunes*.\n- Opinión: *Para mí, es la mejor opción*.\n\n**Ampliación**: por también introduce al agente de la pasiva (*El libro fue escrito por Ana*); para puede contrastar con una expectativa (*Para ser principiante, habla muy bien*). No hay una sustitución única que explique todos los usos: aprende cada preposición en su contexto.",
        structure="POR: causa · medio · recorrido · precio · frecuencia · agente\nPARA: finalidad · destinatario · dirección · plazo · opinión",
        rules=[
            'Por introduce una causa: "Lo hice por necesidad".',
            'Para + infinitivo expresa finalidad: "Ahorro para viajar".',
            'El medio se expresa con por: "Lo envío por correo".',
            'El destinatario se expresa con para: "El regalo es para Ana".',
            'Por y para pueden formar frases correctas con sentidos distintos: "Trabaja por su familia" (motivo) y "Trabaja para una empresa" (destinatario de su trabajo).',
        ],
        examples=[
            GrammarExample(
                text="Estudio español para viajar por Latinoamérica.",
                translation=None,
                note="para = finalidad; por = recorrido",
            ),
            GrammarExample(text="Gracias por todo. El regalo es para ti.", translation=None),
            GrammarExample(text="Pasé por tu oficina, pero no estabas.", translation=None),
            GrammarExample(text="Este informe es para el viernes.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gracias para la invitación.",
                correct="Gracias por la invitación.",
                note='Con "gracias" se usa por para introducir el motivo del agradecimiento.',
            ),
            GrammarMistake(
                wrong="Estudio para aprenderé español.",
                correct="Estudio para aprender español.",
                note="Para expresar la finalidad con el mismo sujeto, se usa para + infinitivo.",
            ),
        ],
        related=["preposiciones-lugar", "voz-pasiva", "conectores-avanzados"],
    ),
    GrammarTopic(
        slug="preterito-indefinido-regular",
        title="Pretérito indefinido regular",
        level="A2",
        category="Tiempos verbales",
        summary="El pasado simple para acciones terminadas: conjugación regular de -ar, -er, -ir.",
        explanation="El **pretérito indefinido** (o pretérito perfecto simple) presenta hechos pasados como completos o delimitados. Pueden tener consecuencias actuales: *Ayer perdí las llaves y aún no las encuentro*.\n\n| Persona | -ar (hablar) | -er (comer) | -ir (vivir) |\n|--------|-------------|-------------|------------|\n| yo | hablé | comí | viví |\n| tú | hablaste | comiste | viviste |\n| él/ella/usted | habló | comió | vivió |\n| nosotros | hablamos | comimos | vivimos |\n| vosotros | hablasteis | comisteis | vivisteis |\n| ellos/ellas/ustedes | hablaron | comieron | vivieron |\n\nLas terminaciones de -er e -ir son idénticas en el indefinido. Las formas de nosotros/as de -ar y -ir coinciden con las del presente: *hablamos, vivimos*. El contexto aclara el tiempo. La primera persona singular no coincide: *hablo / hablé*.",
        structure="raíz + -é/-aste/-ó/-amos/-asteis/-aron (AR) · -í/-iste/-ió/-imos/-isteis/-ieron (ER/IR)",
        rules=[
            "-er e -ir comparten las mismas terminaciones en indefinido.",
            "La primera persona del singular (yo) siempre lleva tilde: hablé, comí, viví.",
            "La tercera persona del singular lleva tilde: habló, comió, vivió.",
            "Se usa para acciones completadas en un momento concreto del pasado.",
            "Con marcadores como ayer, la semana pasada, el año pasado, en 2020.",
        ],
        examples=[
            GrammarExample(
                text="Ayer hablé con mi madre por teléfono.",
                translation=None,
            ),
            GrammarExample(text="Comimos paella el domingo pasado.", translation=None),
            GrammarExample(
                text="¿Viviste en Barcelona el año pasado?",
                translation=None,
            ),
            GrammarExample(text="Ellos llegaron a las ocho.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ayer hablo con Juan.",
                correct="Ayer hablé con Juan.",
                note='"Hablo" es presente; para el pasado se necesita "hablé" con tilde.',
            ),
            GrammarMistake(
                wrong="Ayer ellos comió paella.",
                correct="Ayer ellos comieron paella.",
                note="El verbo debe concordar con el sujeto plural: ellos comieron.",
            ),
        ],
        related=[
            "preterito-irregular",
            "marcadores-temporales",
            "preterito-vs-imperfecto",
        ],
    ),
    GrammarTopic(
        slug="marcadores-temporales",
        title="Marcadores temporales del pasado",
        level="A2",
        category="Adjetivos y adverbios",
        summary="Ayer, la semana pasada, hace dos días, en 2020... palabras que señalan cuándo ocurrió algo.",
        explanation="Los **marcadores temporales** son palabras o expresiones que sitúan una acción en el tiempo. Son fundamentales para elegir entre pretérito indefinido e imperfecto.\n\n**Con pretérito indefinido** (acciones puntuales terminadas):\n- *ayer, anoche, anteayer*\n- *el lunes/mes/año pasado*\n- *la semana pasada*\n- *hace dos días / tres meses / un año*\n- *en 2019, en julio*\n- *de repente, de pronto*\n\n**Con pretérito imperfecto** (descripciones, hábitos):\n- *antes, de pequeño/a, cuando era joven*\n- *todos los días, siempre, cada verano*\n- *mientras*\n\nEl marcador temporal ayuda a identificar qué tiempo usar.",
        structure="ayer · anoche · la semana pasada · el mes/año pasado · hace + tiempo · en + año",
        rules=[
            '"Hace + cantidad de tiempo" indica cuánto tiempo ha pasado desde la acción.',
            '"En + año/mes" se usa con indefinido para localizar una acción concreta.',
            '"Desde hace" indica duración que continúa en el presente.',
            'No confundir "hace" (marcador) con "desde hace" (duración continua).',
        ],
        examples=[
            GrammarExample(text="Ayer fui al cine.", translation=None),
            GrammarExample(
                text="La semana pasada visité a mis abuelos.",
                translation=None,
            ),
            GrammarExample(
                text="Hace tres años empecé a estudiar español.",
                translation=None,
            ),
            GrammarExample(text="En 2015 nos mudamos a Madrid.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Hace dos años viajemos a Chile.",
                correct="Hace dos años viajamos a Chile.",
                note="Para afirmar este hecho pasado se usa indicativo, no el presente de subjuntivo viajemos.",
            ),
            GrammarMistake(
                wrong="Desde dos años vivo aquí.",
                correct="Vivo aquí desde hace dos años.",
                note='"Desde hace" expresa duración desde el pasado hasta ahora.',
            ),
        ],
        related=[
            "preterito-indefinido-regular",
            "preterito-irregular",
            "preterito-perfecto",
        ],
    ),
    GrammarTopic(
        slug="preterito-irregular",
        title="Pretérito indefinido irregular",
        level="A2",
        category="Tiempos verbales",
        summary="Los principales verbos irregulares en pretérito indefinido.",
        explanation="Muchos de los verbos más frecuentes tienen un **pretérito indefinido irregular** con raíces especiales y terminaciones sin tilde.\n\n**Verbos con raíz irregular (pretéritos fuertes)**:\n\n| Infinitivo | Raíz | yo | tú | él |\n|-----------|------|----|----|-----|\n| tener | tuv- | tuve | tuviste | tuvo |\n| estar | estuv- | estuve | estuviste | estuvo |\n| hacer | hic- (hiz-) | hice | hiciste | hizo |\n| poner | pus- | puse | pusiste | puso |\n| poder | pud- | pude | pudiste | pudo |\n| saber | sup- | supe | supiste | supo |\n| querer | quis- | quise | quisiste | quiso |\n| venir | vin- | vine | viniste | vino |\n| decir | dij- | dije | dijiste | dijo |\n| traer | traj- | traje | trajiste | trajo |\n| conducir | conduj- | conduje | condujiste | condujo |\n| andar | anduv- | anduve | anduviste | anduvo |\n\n**Ir y ser comparten la misma conjugación**: *fui, fuiste, fue, fuimos, fuisteis, fueron*.\n**Dar** es como un verbo -er/-ir: *di, diste, dio, dimos, disteis, dieron*.\n**Ver**: *vi, viste, vio, vimos, visteis, vieron* (sin tilde).",
        structure="raíz irregular + -e/-iste/-o/-imos/-isteis/-ieron (sin tilde)",
        rules=[
            "Las terminaciones de los pretéritos fuertes NO llevan tilde.",
            '"Hacer" cambia c→z en la tercera persona: hizo (no ~~hico~~).',
            '"Decir" y verbos en -ducir tienen j en toda la conjugación: dijo, condujo.',
            "Ir y ser son idénticos en indefinido; el contexto indica el significado.",
        ],
        examples=[
            GrammarExample(
                text="Ayer no tuve tiempo para llamarte.",
                translation=None,
            ),
            GrammarExample(text="¿Qué hiciste el fin de semana?", translation=None),
            GrammarExample(
                text="Fui al médico y luego fui muy feliz.",
                translation=None,
                note="ir y ser",
            ),
            GrammarExample(
                text="Ellos no quisieron venir a la cena.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ayer hací la comida.",
                correct="Ayer hice la comida.",
                note='La forma correcta del indefinido de "hacer" (yo) es "hice".',
            ),
            GrammarMistake(
                wrong="Él hico la maleta.",
                correct="Él hizo la maleta.",
                note='La tercera persona de hacer es "hizo", con z, no con c.',
            ),
        ],
        related=[
            "preterito-indefinido-regular",
            "marcadores-temporales",
            "preterito-vs-imperfecto",
        ],
    ),
    GrammarTopic(
        slug="imperfecto",
        title="Pretérito imperfecto",
        level="A2",
        category="Tiempos verbales",
        summary="Describir hábitos pasados, escenas y acciones en desarrollo en el pasado.",
        explanation="El **pretérito imperfecto** presenta situaciones pasadas sin enfocar su inicio o final: hábitos, descripciones y acciones en desarrollo. No significa que sigan ocurriendo ahora. Los irregulares básicos son *ir, ser, ver*.\n\n| Persona | -ar (hablar) | -er (comer) | -ir (vivir) |\n|--------|-------------|-------------|-------------|\n| yo | hablaba | comía | vivía |\n| tú | hablabas | comías | vivías |\n| él/ella/ud. | hablaba | comía | vivía |\n| nosotros | hablábamos | comíamos | vivíamos |\n| vosotros | hablabais | comíais | vivíais |\n| ellos/ellas/uds. | hablaban | comían | vivían |\n\nIrregulares: *ir → iba, ser → era, ver → veía*.\n\n- **Hábito**: *De pequeño jugaba al fútbol*.\n- **Descripción**: *Era una noche oscura*.\n- **Acción en desarrollo**: *Mientras cocinaba, sonó el teléfono*.\n\nUn hábito también puede resumirse como un periodo cerrado con indefinido: *Durante aquel verano fui a nadar todos los días*. La perspectiva, no solo el marcador temporal, determina la elección.",
        structure="raíz + -aba/-abas/-aba/-ábamos/-abais/-aban (AR) · -ía/-ías/-ía/-íamos/-íais/-ían (ER/IR)",
        rules=[
            "El imperfecto de -er e -ir es idéntico.",
            "Presenta situaciones pasadas desde dentro, sin enfocar su principio o final.",
            "Solo tres verbos irregulares: ir, ser y ver.",
            "Se usa para describir circunstancias que rodean una acción puntual (en indefinido).",
        ],
        examples=[
            GrammarExample(
                text="Cuando era pequeño, vivía en un pueblo.",
                translation=None,
            ),
            GrammarExample(
                text="Antes íbamos a la playa todos los veranos.",
                translation=None,
            ),
            GrammarExample(
                text="Ella leía mientras yo cocinaba.",
                translation=None,
            ),
            GrammarExample(
                text="Hacía frío y llovía sin parar.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="De pequeños, nosotros jugaban al fútbol.",
                correct="De pequeños, nosotros jugábamos al fútbol.",
                note="El imperfecto concuerda con el sujeto: nosotros jugábamos, ellos jugaban.",
            ),
            GrammarMistake(
                wrong="Antes ellos iba al cine solos.",
                correct="Antes ellos iban al cine solos.",
                note="La forma de tercera persona plural de ir en imperfecto es iban.",
            ),
        ],
        related=["preterito-vs-imperfecto", "solia", "marcadores-temporales"],
    ),
    GrammarTopic(
        slug="preterito-vs-imperfecto",
        title="Contraste: pretérito indefinido vs. imperfecto",
        level="A2",
        category="Tiempos verbales",
        summary="Cuándo usar cada pasado: acción puntual vs. descripción o hábito.",
        explanation="La elección entre **indefinido** e **imperfecto** depende de **cómo se presenta la situación**.\n\nEl indefinido presenta un hecho completo o delimitado: *Llegué a casa, cené y me acosté*. No tiene que ser breve: *Viví allí veinte años*.\n\nEl imperfecto presenta contexto, hábitos o acciones en desarrollo: *Eran las ocho. Llovía. Estaba cansado*.\n\nAmbos se combinan: *Mientras paseaba, vi a un amigo*. Ayer o mientras no imponen automáticamente un tiempo: *Ayer estaba cocinando cuando llamaste* es correcta.\n\nAlgunos verbos cambian de interpretación: *Supe la verdad* suele equivaler a *me enteré*; *sabía la verdad* presenta un conocimiento ya existente. No todo estado en indefinido implica un cambio: *Siempre creí en ti*.",
        rules=[
            'Imperfecto = descripción, hábito, acción de fondo, "escenario".',
            "Indefinido = acción concreta, terminada, que hace avanzar la narración.",
            'Imperfecto con "mientras" cuando dos acciones son simultáneas y durativas.',
            "Algunos verbos cambian de interpretación según el aspecto: supe suele significar me enteré; no todo estado en indefinido expresa un cambio.",
        ],
        examples=[
            GrammarExample(
                text="Estudiaba cuando me llamaste.",
                translation=None,
            ),
            GrammarExample(
                text="De joven, salía todos los viernes.",
                translation=None,
            ),
            GrammarExample(
                text="El verano pasado fui a Italia y visité Roma.",
                translation=None,
            ),
            GrammarExample(
                text="Hacía sol y los pájaros cantaban. De repente, empezó a llover.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mientras yo cocinabas, sonó el teléfono.",
                correct="Mientras yo cocinaba, sonó el teléfono.",
                note="Cocinaba concuerda con yo y presenta la actividad en curso cuando sonó el teléfono.",
            ),
            GrammarMistake(
                wrong="Ayer yo estuvé en casa todo el día.",
                correct="Ayer yo estuve en casa todo el día.",
                note="Estuve se escribe sin tilde. El indefinido presenta aquí el día como un periodo completo.",
            ),
        ],
        related=[
            "imperfecto",
            "preterito-indefinido-regular",
            "solia",
            "marcadores-temporales",
        ],
    ),
    GrammarTopic(
        slug="solia",
        title="Soler + infinitivo",
        level="A2",
        category="Tiempos verbales",
        summary="Expresar acciones habituales en pasado y presente con el verbo soler.",
        explanation='El verbo **soler** (cambio o→ue) significa "tener la costumbre de".\n\nEn **presente**: *Suelo desayunar a las ocho.*\nEn **imperfecto**: *Solía jugar al tenis.*\n\n**Solía + infinitivo** enfatiza un hábito pasado. En A2 se practican sobre todo estos dos tiempos. Soler tiene un uso defectivo: no se emplea normalmente en todos los tiempos, pero también existen usos en subjuntivo (*No creo que suela faltar*) o en perfecto compuesto (*Siempre he solido madrugar*).',
        structure="soler (conjugado) + infinitivo",
        rules=[
            "Los tiempos más frecuentes de soler son el presente y el imperfecto de indicativo, pero no son los únicos posibles.",
            'Siempre va seguido de infinitivo: "Suelo comer a las dos".',
            '"Soler + infinitivo" expresa frecuencia habitual, no capacidad.',
            'No confundir "solía" (hábito) con "solo/a" (sin compañía).',
        ],
        examples=[
            GrammarExample(text="Suelo leer antes de dormir.", translation=None),
            GrammarExample(
                text="De niño, solía pasar los veranos en el pueblo.",
                translation=None,
            ),
            GrammarExample(text="¿Sueles hacer ejercicio?", translation=None),
            GrammarExample(
                text="Antes no solíamos viajar tanto.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Yo sueles ir al parque.",
                correct="Yo suelo ir al parque.",
                note="La forma de primera persona es suelo; sueles corresponde a tú.",
            ),
            GrammarMistake(
                wrong="Suelo a comer a las dos.",
                correct="Suelo comer a las dos.",
                note="Soler rige infinitivo sin preposición.",
            ),
        ],
        related=["imperfecto", "preterito-vs-imperfecto", "marcadores-temporales"],
    ),
    GrammarTopic(
        slug="pronombres-objeto-directo",
        title="Pronombres de objeto directo",
        level="A2",
        category="Pronombres",
        summary="me, te, lo, la, nos, os, los, las — sustituir el complemento directo.",
        explanation="Los **pronombres de objeto directo** sustituyen al complemento que recibe directamente la acción del verbo. Responden a *¿qué?* o *¿a quién?*.\n\n| Persona | Pronombre OD |\n|---------|-------------|\n| yo | me |\n| tú | te |\n| él/usted (masc.) | lo |\n| ella/usted (fem.) | la |\n| nosotros/as | nos |\n| vosotros/as | os |\n| ellos/ustedes (masc.) | los |\n| ellas/ustedes (fem.) | las |\n\nSe colocan **delante del verbo conjugado**: *Lo compré ayer.*\nCon **infinitivo o gerundio** pueden ir detrás soldados a la palabra: *Voy a comprarlo. / Estoy comprándolo.*",
        structure="pronombre OD + verbo conjugado · infinitivo/gerundio + pronombre OD",
        rules=[
            "Concuerdan en género y número con el sustantivo que sustituyen.",
            "Delante del verbo conjugado; detrás soldados al infinitivo o gerundio.",
            '"Lo" se usa también para ideas o frases enteras: "No lo sé".',
            'En España hay tendencia al leísmo de persona, pero lo normativo es "lo" para OD masculino.',
        ],
        examples=[
            GrammarExample(text="¿El libro? Lo leí ayer.", translation=None),
            GrammarExample(
                text="A María la vi en el supermercado.",
                translation=None,
            ),
            GrammarExample(text="No puedo encontrarlo.", translation=None),
            GrammarExample(
                text="Estamos preparándola para la fiesta.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Lo vi a María.",
                correct="La vi. / Vi a María.",
                note='Si el OD es femenino, el pronombre debe ser "la".',
            ),
            GrammarMistake(
                wrong="¿Las flores? Le compré ayer.",
                correct="¿Las flores? Las compré ayer.",
                note='OD femenino plural → "las", no "le".',
            ),
        ],
        related=[
            "pronombres-objeto-indirecto",
            "doble-objeto",
            "imperativo-afirmativo",
        ],
    ),
    GrammarTopic(
        slug="pronombres-objeto-indirecto",
        title="Pronombres de objeto indirecto",
        level="A2",
        category="Pronombres",
        summary="me, te, le, nos, os, les — sustituir el complemento indirecto (a quién).",
        explanation="Los **pronombres de objeto indirecto** sustituyen a la persona o entidad que recibe el beneficio o daño de la acción. Responden a *¿a quién?* o *¿para quién?*.\n\n| Persona | Pronombre OI |\n|---------|-------------|\n| yo | me |\n| tú | te |\n| él/ella/usted | le |\n| nosotros/as | nos |\n| vosotros/as | os |\n| ellos/ellas/ustedes | les |\n\nA diferencia del OD, el OI **no distingue género**: *le* sirve para masculino y femenino singular; *les* para plural.\n\nSe colocan igual que los OD: delante del verbo conjugado o detrás del infinitivo/gerundio. La duplicación del OI es frecuente: *Le di el libro a Juan.*",
        structure="pronombre OI + verbo conjugado",
        rules=[
            "No distinguen género: le/les para masculino y femenino.",
            'Se suele duplicar el OI con "a + persona" para aclarar: "Le dije a María".',
            "Colocación: delante del verbo conjugado o soldado al infinitivo/gerundio.",
            "Con verbos como gustar, encantar, doler, el sujeto va después y el OI va delante.",
        ],
        examples=[
            GrammarExample(
                text="Le escribí una carta a mi abuela.",
                translation=None,
            ),
            GrammarExample(text="¿Me puedes prestar tu boli?", translation=None),
            GrammarExample(
                text="Les explicamos la situación a los clientes.",
                translation=None,
            ),
            GrammarExample(
                text="Voy a darle el regalo mañana.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="La di el libro a María.",
                correct="Le di el libro a María.",
                note='El OI es "le" (invariable en género), no "la".',
            ),
            GrammarMistake(
                wrong="Dí a Juan la noticia.",
                correct="Le di la noticia a Juan.",
                note="El OI debe aparecer con el pronombre, especialmente si se menciona la persona.",
            ),
        ],
        related=["pronombres-objeto-directo", "doble-objeto", "gustar"],
    ),
    GrammarTopic(
        slug="doble-objeto",
        title="Combinación de pronombres OD y OI",
        level="A2",
        category="Pronombres",
        summary="Usar juntos los pronombres de OD y OI: se lo, me lo, te la...",
        explanation='Cuando en una misma oración aparecen pronombres de **objeto indirecto y objeto directo**, el OI va **siempre antes** del OD.\n\nLa regla más importante: cuando el OI es **le o les** y va seguido de un OD de tercera persona (**lo, la, los, las**), el OI se transforma en **se**:\n- *Le di el libro.* → *Se lo di.* (NO ~~Le lo di~~)\n- *Les mandé las cartas.* → *Se las mandé.*\n\nOrden: **OI + OD + verbo**.\n\nCon infinitivo o gerundio, ambos se colocan detrás: *Voy a decírtelo. / Estoy explicándoselo.*\n\nLa duplicación del OI es posible y frecuente: "Se lo di a ella".',
        structure="OI + OD + verbo · se + lo/la/los/las (cuando OI es le/les)",
        rules=[
            "El OI siempre precede al OD.",
            "le/les + lo/la/los/las → se + lo/la/los/las.",
            "Con ambos pronombres al final del infinitivo/gerundio, se acentúa la palabra.",
            'La duplicación del OI es posible: "Se lo di a ella".',
        ],
        examples=[
            GrammarExample(
                text="¿El informe? Te lo envío ahora.",
                translation=None,
            ),
            GrammarExample(text="Se lo expliqué a mis padres.", translation=None),
            GrammarExample(text="¿Me lo puedes repetir?", translation=None),
            GrammarExample(
                text="No quiero contárselo todavía.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Le lo dije.",
                correct="Se lo dije.",
                note='La combinación "le lo" no existe; se convierte en "se lo".',
            ),
            GrammarMistake(
                wrong="Lo se di.",
                correct="Se lo di.",
                note="El OI (se) debe ir antes del OD (lo).",
            ),
        ],
        related=[
            "pronombres-objeto-directo",
            "pronombres-objeto-indirecto",
            "imperativo-afirmativo",
        ],
    ),
    GrammarTopic(
        slug="comparativos",
        title="Comparativos",
        level="A2",
        category="Adjetivos y adverbios",
        summary="Comparar personas, objetos y acciones: más... que, menos... que, tan... como.",
        explanation="En español hay tres tipos de **comparación**:\n\n**Comparativo de superioridad**: *más + adjetivo/sustantivo/adverbio + que*\n- *Ella es más alta que yo. / Tengo más trabajo que antes.*\n\n**Comparativo de inferioridad**: *menos + adjetivo/sustantivo/adverbio + que*\n- *Este coche es menos caro que aquel.*\n\n**Comparativo de igualdad**: *tan + adjetivo/adverbio + como* / *tanto/a/os/as + sustantivo + como*\n- *Es tan inteligente como su hermano. / Tengo tantos libros como tú.*\n\n**Comparativos irregulares**:\n- bueno → mejor · malo → peor · grande → mayor · pequeño → menor\n- *Mejor/peor que*, nunca ~~más mejor~~.",
        structure="más + adjetivo/sustantivo/adverbio + que · menos + ... + que · tan + adjetivo + como",
        rules=[
            '"Más/menos + adjetivo + que" para superioridad e inferioridad.',
            '"Tan + adjetivo + como" para igualdad con adjetivos; "tanto/a/os/as + sustantivo + como" con sustantivos.',
            'Los comparativos irregulares no usan "más": mejor, peor, mayor, menor.',
            'Con números se usa "más de": "Más de cien personas".',
        ],
        examples=[
            GrammarExample(
                text="Madrid es más grande que Barcelona.",
                translation=None,
            ),
            GrammarExample(
                text="Este ejercicio es menos difícil que el anterior.",
                translation=None,
            ),
            GrammarExample(
                text="Ella es tan simpática como su hermana.",
                translation=None,
            ),
            GrammarExample(
                text="Esta película es mejor que la otra.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Es más mejor que el otro.",
                correct="Es mejor que el otro.",
                note='"Mejor" ya es comparativo; no necesita "más".',
            ),
            GrammarMistake(
                wrong="Es tan alto que su padre.",
                correct="Es tan alto como su padre.",
                note='Las comparaciones de igualdad usan "tan... como", no "tan... que".',
            ),
        ],
        related=["superlativos", "tan-como", "adjetivos-descriptivos"],
    ),
    GrammarTopic(
        slug="superlativos",
        title="Superlativos",
        level="A2",
        category="Adjetivos y adverbios",
        summary="Expresar el grado máximo de una cualidad: el más..., el mejor, -ísimo.",
        explanation="El **superlativo** expresa el grado máximo de una cualidad. Hay dos formas:\n\n**Superlativo relativo**: destaca un elemento dentro de un grupo.\n- *el/la/los/las + más/menos + adjetivo + de*: *Es la más inteligente de la clase.*\n\n**Superlativo absoluto**: expresa un grado muy alto sin comparar.\n- *muy + adjetivo*: *Es muy bueno.*\n- *adjetivo + -ísimo/a*: *Es buenísimo. / Es facilísimo.*\n\nIrregulares:\n- bueno → óptimo / buenísimo\n- malo → pésimo / malísimo\n- grande → máximo / grandísimo\n- pequeño → mínimo / pequeñísimo\n\nCambios ortográficos al añadir -ísimo: largo → larguísimo, feliz → felicísimo, rico → riquísimo.",
        structure="el/la/los/las + más/menos + adjetivo + de · adjetivo + -ísimo/a/os/as",
        rules=[
            'Superlativo relativo: "el más + adjetivo + de".',
            'Superlativo absoluto: "-ísimo/a/os/as" o "muy + adjetivo".',
            "Los adjetivos en -ble forman -bilísimo: amable → amabilísimo.",
            "Los terminados en -co/-go cambian a -qu/-gu: rico → riquísimo, largo → larguísimo.",
        ],
        examples=[
            GrammarExample(
                text="Es el edificio más alto del mundo.",
                translation=None,
            ),
            GrammarExample(text="La paella está buenísima.", translation=None),
            GrammarExample(
                text="Es la persona menos puntual de la oficina.",
                translation=None,
            ),
            GrammarExample(text="El examen fue facilísimo.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Es el más mejor de todos.",
                correct="Es el mejor de todos.",
                note='"Mejor" ya es la forma superlativa de "bueno" para el relativo.',
            ),
            GrammarMistake(
                wrong="La sopa está buenísimos.",
                correct="La sopa está buenísima.",
                note="El superlativo absoluto concuerda con el sustantivo: sopa es femenino singular.",
            ),
        ],
        related=["comparativos", "tan-como", "adjetivos-descriptivos"],
    ),
    GrammarTopic(
        slug="tan-como",
        title="Tan y tanto... como",
        level="A2",
        category="Adjetivos y adverbios",
        summary="Expresar igualdad: tan + adjetivo + como; tanto/a/os/as + sustantivo + como.",
        explanation="**Tan** y **tanto** expresan **igualdad** en la comparación. La forma correcta depende de qué se compara:\n\n- **Tan + adjetivo + como**: *Eres tan alto como tu hermano.*\n- **Tan + adverbio + como**: *Corre tan rápido como un profesional.*\n- **Tanto/a/os/as + sustantivo + como**: concuerda en género y número. *Tengo tanto dinero como tú. / Hay tantas chicas como chicos.*\n- **Verbo + tanto como**: *Estudio tanto como puedo.*\n\nEn oraciones consecutivas se usa **tan/tanto... que**: *Es tan gracioso que todos se ríen. / Habla tanto que me cansa.*",
        structure="tan + adjetivo/adverbio + como · tanto/a/os/as + sustantivo + como · verbo + tanto como",
        rules=[
            '"Tan" es invariable: siempre igual, con adjetivos y adverbios.',
            '"Tanto" concuerda en género y número con el sustantivo.',
            '"Tanto como" con verbos (invariable).',
            '"Tan... que" y "tanto... que" para consecuencias, no comparación.',
        ],
        examples=[
            GrammarExample(text="No soy tan paciente como tú.", translation=None),
            GrammarExample(
                text="En esta ciudad hay tanta contaminación como en otras capitales.",
                translation=None,
            ),
            GrammarExample(
                text="No hablo español tan bien como me gustaría.",
                translation=None,
            ),
            GrammarExample(
                text="Estaba tan cansado que me dormí en el sofá.",
                translation=None,
                note="consecutivo",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Tengo tan dinero como tú.",
                correct="Tengo tanto dinero como tú.",
                note='Con sustantivos se usa "tanto/a/os/as", no "tan".',
            ),
            GrammarMistake(
                wrong="Es tanto amable como su madre.",
                correct="Es tan amable como su madre.",
                note='Con adjetivos se usa "tan", no "tanto".',
            ),
        ],
        related=["comparativos", "superlativos", "muy-mucho"],
    ),
    GrammarTopic(
        slug="imperativo-afirmativo",
        title="Imperativo afirmativo",
        level="A2",
        category="Verbos",
        summary="Dar órdenes, instrucciones y consejos con el imperativo afirmativo.",
        explanation='El **imperativo afirmativo** se usa para dar órdenes, instrucciones, consejos o hacer invitaciones. Tiene formas propias para **tú** y **vosotros**; las formas de **usted** y **ustedes** se toman del **presente de subjuntivo**.\n\n**Formación regular**:\n\n| | -ar (hablar) | -er (comer) | -ir (escribir) |\n|---|-------------|-------------|---------------|\n| tú | habla | come | escribe |\n| usted | hable | coma | escriba |\n| vosotros | hablad | comed | escribid |\n| ustedes | hablen | coman | escriban |\n\nEl imperativo de **tú** afirmativo coincide con la tercera persona singular del presente de indicativo: *él habla → ¡habla tú!*\nEl de **vosotros** se forma sustituyendo la -r del infinitivo por -d: *hablar → hablad*.\n\nLos pronombres van **detrás y soldados**: *cómpralo, siéntate, dime, dáselo*.\nEl imperativo de vosotros pierde la -d ante "os": *sentad + os → sentaos*.',
        structure="tú: 3ª pers. sing. presente · usted: 3ª pers. sing. subjuntivo · vosotros: infinitivo -r + d",
        rules=[
            "Tú afirmativo: como la 3ª persona singular del presente (habla, come, escribe).",
            "Vosotros afirmativo: cambiar -r del infinitivo por -d (hablad, comed, escribid).",
            "Usted/ustedes: igual que el presente de subjuntivo.",
            'Los pronombres van detrás: "dime", "cómpralo", "siéntate".',
        ],
        examples=[
            GrammarExample(text="¡Come más despacio!", translation=None),
            GrammarExample(
                text="Hablad más bajo, por favor.",
                translation=None,
                note="vosotros",
            ),
            GrammarExample(text="Dime la verdad.", translation=None),
            GrammarExample(text="Siéntese, por favor.", translation=None, note="usted"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="¡Comes más despacio!",
                correct="¡Come más despacio!",
                note='El imperativo de tú es "come", no "comes".',
            ),
            GrammarMistake(
                wrong="Sentaros aquí.",
                correct="Sentaos aquí.",
                note='El imperativo de vosotros pierde la -d delante de "os": sentad + os → sentaos.',
            ),
        ],
        related=[
            "imperativo-negativo",
            "imperativo-irregular",
            "pronombres-objeto-directo",
        ],
    ),
    GrammarTopic(
        slug="imperativo-negativo",
        title="Imperativo negativo",
        level="A2",
        category="Verbos",
        summary="Prohibir o desaconsejar con el imperativo negativo.",
        explanation="El **imperativo negativo** usa siempre las formas del **presente de subjuntivo**, para todas las personas, incluido tú y vosotros.\n\n| Persona | -ar (hablar) | -er (comer) | -ir (escribir) |\n|--------|-------------|-------------|---------------|\n| tú | no hables | no comas | no escribas |\n| usted | no hable | no coma | no escriba |\n| vosotros | no habléis | no comáis | no escribáis |\n| ustedes | no hablen | no coman | no escriban |\n\nLos pronombres en el imperativo negativo van **delante del verbo** (a diferencia del afirmativo):\n- *Cómpralo. → No lo compres.*\n- *Siéntate. → No te sientes.*",
        structure="no + presente de subjuntivo",
        rules=[
            "El imperativo negativo usa siempre el presente de subjuntivo.",
            'Los pronombres van delante del verbo en el negativo: "No lo hagas".',
            '"No + subjuntivo" reemplaza completamente al imperativo afirmativo para prohibiciones.',
            "La forma de vosotros negativo termina en -éis (AR) o -áis (ER/IR): no habléis, no comáis.",
        ],
        examples=[
            GrammarExample(text="No hables tan alto.", translation=None),
            GrammarExample(
                text="No comáis tantos dulces.",
                translation=None,
                note="vosotros",
            ),
            GrammarExample(text="Por favor, no se preocupe.", translation=None, note="usted"),
            GrammarExample(text="No lo toques, está caliente.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="No habla tan alto.",
                correct="No hables tan alto.",
                note='El imperativo negativo de tú es "no hables", no "no habla".',
            ),
            GrammarMistake(
                wrong="No sentaros aquí.",
                correct="No os sentéis aquí.",
                note='En el negativo los pronombres van delante: "no os sentéis".',
            ),
        ],
        related=[
            "imperativo-afirmativo",
            "imperativo-irregular",
            "subjuntivo-presente",
        ],
    ),
    GrammarTopic(
        slug="imperativo-irregular",
        title="Imperativo irregular",
        level="A2",
        category="Verbos",
        summary="Los imperativos irregulares de tú: ven, di, sal, haz, ten, ve, pon, sé.",
        explanation="El imperativo afirmativo de **tú** tiene **ocho formas irregulares** muy frecuentes:\n\n| Infinitivo | Imperativo tú |\n|-----------|--------------|\n| decir | **di** |\n| hacer | **haz** |\n| ir | **ve** |\n| poner | **pon** |\n| salir | **sal** |\n| ser | **sé** |\n| tener | **ten** |\n| venir | **ven** |\n\nEstas formas irregulares mantienen los pronombres soldados detrás: *dime, hazlo, ponte, vete, tenlo, ven aquí*.\n\nPara **vosotros**, el imperativo es siempre regular (salvo ir → id).\n\nEl imperativo negativo usa el subjuntivo y sigue las irregularidades del presente de subjuntivo: *no digas, no hagas, no vayas, no pongas...*",
        structure="ocho formas irregulares de tú",
        rules=[
            "Solo ocho verbos tienen imperativo de tú irregular.",
            "Las formas de vosotros son siempre regulares (infinitivo -r + d).",
            'Los imperativos irregulares de tú se memorizan: "di, haz, ve, pon, sal, sé, ten, ven".',
            "El imperativo negativo irregular sigue el subjuntivo.",
        ],
        examples=[
            GrammarExample(text="Di la verdad.", translation=None),
            GrammarExample(text="Haz los deberes ahora.", translation=None),
            GrammarExample(text="Ten paciencia.", translation=None),
            GrammarExample(text="Pon la mesa, por favor.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Hace los deberes.",
                correct="Haz los deberes.",
                note='El imperativo de hacer es "haz". "Hace" es presente de indicativo.',
            ),
            GrammarMistake(
                wrong="Pone la mesa.",
                correct="Pon la mesa.",
                note='El imperativo de poner es "pon". "Pone" es presente de indicativo.',
            ),
        ],
        related=["imperativo-afirmativo", "imperativo-negativo", "presente-regular"],
    ),
    GrammarTopic(
        slug="futuro-simple",
        title="Futuro simple",
        level="A2",
        category="Tiempos verbales",
        summary="Hablar de acciones futuras: hablaré, comerás, vivirán.",
        explanation="El **futuro simple** se forma añadiendo las terminaciones al **infinitivo completo** (sin quitar -ar/-er/-ir). Es igual para las tres conjugaciones.\n\n| Persona | -ar (hablar) | -er (comer) | -ir (vivir) |\n|--------|-------------|-------------|------------|\n| yo | hablaré | comeré | viviré |\n| tú | hablarás | comerás | vivirás |\n| él/ella/usted | hablará | comerá | vivirá |\n| nosotros | hablaremos | comeremos | viviremos |\n| vosotros | hablaréis | comeréis | viviréis |\n| ellos/ellas/uds. | hablarán | comerán | vivirán |\n\n**Irregulares**: modifican la raíz pero mantienen las mismas terminaciones:\n- decir → dir- · hacer → har- · querer → querr- · poder → podr- · saber → sabr- · salir → saldr- · tener → tendr- · venir → vendr- · poner → pondr- · valer → valdr- · haber → habr- · caber → cabr-\n\nSe usa también para expresar **probabilidad o conjetura** en el presente: *Serán las tres* (probablemente son las tres).",
        structure="infinitivo completo + -é/-ás/-á/-emos/-éis/-án",
        rules=[
            "Las terminaciones se añaden al infinitivo completo; igual para -ar, -er, -ir.",
            'Todas las formas llevan tilde menos "nosotros" (no lleva tilde: hablaremos).',
            "Los irregulares cambian la raíz pero mantienen las mismas terminaciones.",
            'También expresa conjetura: "Estará enfermo" = probablemente está enfermo.',
        ],
        examples=[
            GrammarExample(
                text="El año que viene estudiaré en Granada.",
                translation=None,
            ),
            GrammarExample(text="¿Vendrás a la boda?", translation=None),
            GrammarExample(
                text="No podremos llegar a tiempo.",
                translation=None,
            ),
            GrammarExample(
                text="¿Dónde estará Juan? — Estará en casa.",
                translation=None,
                note="conjetura",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mañana voy a viajaré.",
                correct="Mañana viajaré. / Mañana voy a viajar.",
                note='No mezclar "ir a" con el futuro simple; se usa uno u otro.',
            ),
        ],
        related=["ir-a-futuro", "condicional-simple", "si-presente-futuro"],
    ),
    GrammarTopic(
        slug="condicional-simple",
        title="Condicional simple",
        level="A2",
        category="Condicionales",
        summary="Expresar deseos, cortesía, probabilidad en el pasado y situaciones hipotéticas.",
        explanation="El **condicional simple** se forma añadiendo terminaciones al **infinitivo completo**. Los mismos verbos que son irregulares en futuro lo son en condicional.\n\n| Persona | -ar (hablar) | -er (comer) | -ir (vivir) |\n|--------|-------------|-------------|------------|\n| yo | hablaría | comería | viviría |\n| tú | hablarías | comerías | vivirías |\n| él/ella/ud. | hablaría | comería | viviría |\n| nosotros | hablaríamos | comeríamos | viviríamos |\n| vosotros | hablaríais | comeríais | viviríais |\n| ellos/ellas/uds. | hablarían | comerían | vivirían |\n\nUsos:\n- **Deseo**: *Me gustaría viajar a Japón.*\n- **Cortesía**: *¿Podría ayudarme?*\n- **Consejo**: *Deberías estudiar más.*\n- **Probabilidad en el pasado**: *Serían las tres cuando llegó.*\n- **Futuro del pasado**: *Dijo que vendría.*",
        structure="infinitivo completo + -ía/-ías/-ía/-íamos/-íais/-ían",
        rules=[
            "Terminaciones sobre el infinitivo completo. Siempre llevan tilde.",
            "Mismos irregulares que el futuro: diría, haría, querría, podría, sabría, saldría, tendría, vendría, pondría, valdría, habría, cabría.",
            '"Debería" + infinitivo para consejos; "me gustaría" para deseos corteses.',
            'No se usa "si" con condicional simple en la prótasis.',
        ],
        examples=[
            GrammarExample(
                text="Me gustaría aprender a tocar la guitarra.",
                translation=None,
            ),
            GrammarExample(text="¿Podrías pasarme la sal?", translation=None),
            GrammarExample(text="Deberías dormir más horas.", translation=None),
            GrammarExample(
                text="Dijo que llegaría a las ocho.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Si tendría dinero, viajaría.",
                correct="Si tuviera dinero, viajaría.",
                note='En las oraciones condicionales con "si", el condicional no va en la prótasis.',
            ),
            GrammarMistake(
                wrong="¿Puederías ayudarme?",
                correct="¿Podrías ayudarme?",
                note='El condicional de poder es "podrías", con -dr-.',
            ),
        ],
        related=["futuro-simple", "si-presente-futuro", "subjuntivo-presente"],
    ),
    GrammarTopic(
        slug="si-presente-futuro",
        title="Oraciones condicionales: si + presente + futuro",
        level="A2",
        category="Condicionales",
        summary="Condiciones reales o probables con si + presente de indicativo + futuro.",
        explanation='Las **condicionales de primer tipo** expresan condiciones **posibles o probables**. La estructura es:\n\n**Si + presente de indicativo, + futuro / presente / imperativo.**\n\n- *Si **estudias**, **aprobarás** el examen.* (condición probable -> resultado futuro)\n- *Si **quieres**, te **ayudo**.* (presente en ambas partes)\n- *Si **tienes** hambre, **come** algo.* (imperativo en la principal)\n\nLa prótasis (la parte con "si") NUNCA lleva futuro ni condicional en español: *Si llueve* (NO ~~Si lloverá~~).',
        structure="si + presente de indicativo + futuro simple / presente / imperativo",
        rules=[
            'En la subordinada con "si" se usa presente de indicativo, nunca futuro ni condicional.',
            "La oración principal puede ir en futuro, presente o imperativo.",
            'El orden puede invertirse: "Te ayudo si quieres". En ese caso no hay coma.',
            "Se usa para condiciones realistas, no hipotéticas ni irreales.",
        ],
        examples=[
            GrammarExample(text="Si llueve, no saldremos.", translation=None),
            GrammarExample(text="Si tienes tiempo, llámame.", translation=None),
            GrammarExample(
                text="Te lo compro si no es muy caro.",
                translation=None,
            ),
            GrammarExample(
                text="Si quieres, vamos al cine.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Si lloverá, no salgo.",
                correct="Si llueve, no saldré.",
                note='Después de "si" condicional nunca se usa futuro.',
            ),
            GrammarMistake(
                wrong="Si tendrás tiempo, llámame.",
                correct="Si tienes tiempo, llámame.",
                note='"Si" no admite futuro ni condicional en la prótasis.',
            ),
        ],
        related=["futuro-simple", "condicional-simple", "si-imperfecto-subjuntivo"],
    ),
    GrammarTopic(
        slug="conectores-narrativos",
        title="Conectores narrativos",
        level="A2",
        category="Oraciones",
        summary="Palabras para organizar un relato: primero, luego, entonces, después, al final.",
        explanation="Los **conectores narrativos** ayudan a ordenar cronológicamente los hechos de un relato o una secuencia de acciones en el pasado.\n\n**Secuencia temporal**:\n- *Primero / En primer lugar / Para empezar* → inicio.\n- *Luego / Después / Más tarde / A continuación* → continuación.\n- *Entonces / En ese momento / De repente* → acontecimiento puntual.\n- *Finalmente / Por último / Al final* → conclusión.\n\nEn narraciones en pasado, estos conectores frecuentemente van con **pretérito indefinido** porque introducen acciones que hacen avanzar la historia:\n- *Primero desayuné; después salí de casa; entonces vi a Marta; finalmente llegué al trabajo.*",
        rules=[
            '"Entonces" introduce un acontecimiento puntual o una consecuencia lógica.',
            '"De repente" marca una acción inesperada; suele ir con indefinido.',
            '"Al final" ≠ "finalmente": al final indica un desenlace que puede ser sorprendente; finalmente es neutro.',
            'Los conectores pueden ir al inicio, en medio o precedidos de "y": "y entonces...".',
        ],
        examples=[
            GrammarExample(
                text="Primero fui al banco, luego pasé por el supermercado y finalmente volví a casa.",
                translation=None,
            ),
            GrammarExample(
                text="Estaba leyendo cuando de repente se apagó la luz.",
                translation=None,
            ),
            GrammarExample(
                text="Entonces decidí llamar a la policía.",
                translation=None,
            ),
            GrammarExample(
                text="Al final todo salió bien.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Después de fui a su casa.",
                correct="Después fui a su casa.",
                note='"Después" va directamente con verbo conjugado; "después de" se usa con sustantivo o infinitivo.',
            ),
        ],
        related=[
            "secuencia-temporal",
            "preterito-indefinido-regular",
            "preterito-vs-imperfecto",
        ],
    ),
    GrammarTopic(
        slug="secuencia-temporal",
        title="Secuencia temporal en la narración",
        level="A2",
        category="Oraciones",
        summary="Coordinar tiempos verbales en una historia: imperfecto de fondo, indefinido de avance.",
        explanation="En una narración en pasado, los tiempos verbales no se eligen al azar. Siguen una **secuencia temporal** que distingue:\n\n**Imperfecto** → descripción del contexto, circunstancias, acciones de fondo:\n  *Era un día soleado. Los pájaros cantaban. Ana paseaba por el parque.*\n\n**Indefinido** → acciones que hacen avanzar la historia:\n  *De repente, vio a un amigo. Se acercó y lo saludó.*\n\n**Pluscuamperfecto** → acción anterior a otra pasada:\n  *Cuando llegué, ya habían cerrado.*\n\nCombinarlos correctamente da fluidez al relato y guía al oyente sobre qué es esencial y qué es contexto.",
        rules=[
            'Imperfecto para el "telón de fondo" (descripciones, circunstancias).',
            "Indefinido para las acciones principales que mueven la trama.",
            "Pluscuamperfecto para lo que ya había ocurrido antes del momento narrado.",
            "Los conectores temporales ayudan a marcar la secuencia.",
        ],
        examples=[
            GrammarExample(
                text="Eran las diez de la noche. Llovía con fuerza. De repente, alguien llamó a la puerta.",
                translation=None,
            ),
            GrammarExample(
                text="Mientras desayunaba, leí el periódico.",
                translation=None,
            ),
            GrammarExample(
                text="Cuando llegamos al cine, ya había empezado la película.",
                translation=None,
            ),
            GrammarExample(
                text="Paseaba por la calle cuando me encontré con un viejo amigo.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Era un día soleado. De repente, alguien llamaron a la puerta.",
                correct="Era un día soleado. De repente, alguien llamó a la puerta.",
                note="Alguien requiere un verbo en singular. El indefinido presenta aquí un hecho completo dentro del relato.",
            ),
            GrammarMistake(
                wrong="Cuando llegué, ya habían cerrar.",
                correct="Cuando llegué, ya habían cerrado.",
                note="El pluscuamperfecto se forma con haber en imperfecto y participio, no infinitivo.",
            ),
        ],
        related=[
            "conectores-narrativos",
            "preterito-vs-imperfecto",
            "pluscuamperfecto",
        ],
    ),
    GrammarTopic(
        slug="estilo-indirecto",
        title="Estilo indirecto (presente → pasado)",
        level="A2",
        category="Estilo indirecto",
        summary="Contar lo que alguien dijo adaptando los tiempos verbales.",
        explanation='El **estilo indirecto** reproduce lo que alguien ha dicho sin una cita literal. Con un verbo introductor en pasado, es frecuente adoptar el punto de vista de aquel momento:\n\n| Estilo directo | Relato desde el pasado |\n|---------------|------------------------|\n| "Estoy cansado" | Dijo que **estaba** cansado |\n| "He comido" | Dijo que **había comido** |\n| "Iré mañana" | Dijo que **iría** al día siguiente |\n\nNo es una transformación automática: *Dijo que está cansado* es válida si el cansancio sigue vigente; *Dijo que vendrá mañana* puede referirse al día siguiente al momento en que hablamos. Las referencias de persona, tiempo y lugar se ajustan cuando cambia su punto de referencia. El pluscuamperfecto y las transformaciones más complejas se desarrollan en B1.',
        rules=[
            'Con verbo introductor en presente ("dice que"), no hay cambio de tiempos.',
            "Con un verbo introductor en pasado, se puede adoptar una perspectiva pasada o mantener una referencia aún vigente.",
            "Los pronombres y referencias espaciales se adaptan si cambia quién habla o desde dónde se habla.",
            '"Que" es obligatorio para introducir la subordinada: "Dijo que vendría".',
        ],
        examples=[
            GrammarExample(
                text="Dijo que estaba cansado.",
                translation=None,
                note='directo: "Estoy cansado"',
            ),
            GrammarExample(
                text="Me contó que había vivido en París.",
                translation=None,
                note='directo: "He vivido en París"',
            ),
            GrammarExample(
                text="Aseguró que llegaría al día siguiente.",
                translation=None,
                note='directo: "Llegaré mañana"',
            ),
            GrammarExample(
                text="Nos explicaron que no podían ayudarnos.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ana dijo de que estaba cansada.",
                correct="Ana dijo que estaba cansada.",
                note="Decir introduce aquí el contenido con que, sin de.",
            ),
            GrammarMistake(
                wrong="Ana dijo que ellos estaba cansados.",
                correct="Ana dijo que ellos estaban cansados.",
                note="El verbo subordinado concuerda con su propio sujeto: ellos estaban.",
            ),
        ],
        related=["cambios-temporales", "imperfecto", "condicional-simple"],
    ),
    GrammarTopic(
        slug="conectores-argumentativos",
        title="Conectores argumentativos",
        level="A2",
        category="Oraciones",
        summary="Conectores para causa, consecuencia y contraste: porque, así que, sin embargo.",
        explanation="Los **conectores argumentativos** unen ideas y permiten expresar relaciones lógicas: causa, consecuencia, oposición.\n\n**Causa**: *porque, ya que, puesto que, debido a que*\n- *No fui a la fiesta **porque** estaba enfermo.*\n- *Ya que has terminado, puedes salir.*\n\n**Consecuencia**: *así que, por eso, por lo tanto, en consecuencia*\n- *Tenía hambre, **así que** me preparé un bocadillo.*\n- *No estudió nada; **por eso** suspendió.*\n\n**Contraste**: *pero, sin embargo, no obstante, aunque, en cambio*\n- *Es caro, **pero** merece la pena.*\n- *Hace frío; **sin embargo**, saldré a correr.*",
        rules=[
            '"Porque" (causa) junto, sin tilde. "Por qué" (interrogativo) separado y con tilde.',
            '"Así que" introduce una consecuencia y se escribe separado.',
            '"Pero" une dos elementos de la misma categoría; "sino" corrige una negación.',
            '"Aunque" puede ir con indicativo (hecho real) o subjuntivo (hipótesis).',
        ],
        examples=[
            GrammarExample(
                text="No salí porque llovía mucho.",
                translation=None,
            ),
            GrammarExample(
                text="Estaba agotado, así que me fui a dormir temprano.",
                translation=None,
            ),
            GrammarExample(
                text="Me gusta el chocolate, pero no debo comer tanto.",
                translation=None,
            ),
            GrammarExample(
                text="Hizo mucho esfuerzo; sin embargo, no consiguió el puesto.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="No es caro, pero barato.",
                correct="No es caro, sino barato.",
                note='Tras una negación, para corregir se usa "sino", no "pero".',
            ),
            GrammarMistake(
                wrong="No vine por que estaba enfermo.",
                correct="No vine porque estaba enfermo.",
                note='"Porque" (causa) se escribe junto y sin tilde.',
            ),
        ],
        related=["conectores-narrativos", "conectores-avanzados", "si-presente-futuro"],
    ),
    GrammarTopic(
        slug="cambios-temporales",
        title="Cambios temporales en el estilo indirecto",
        level="A2",
        category="Estilo indirecto",
        summary="Cómo cambian las referencias de tiempo y lugar al pasar al estilo indirecto.",
        explanation='Las referencias temporales y espaciales se adaptan al **punto de vista de quien reproduce el mensaje**, no automáticamente al tiempo de dijo.\n\nSi ya no compartimos el mismo día o lugar, son frecuentes estas correspondencias:\n- hoy → aquel día\n- ayer → el día anterior\n- mañana → el día siguiente\n- esta semana → aquella semana\n- la semana pasada → la semana anterior\n- la semana que viene → la semana siguiente\n- ahora → entonces\n- aquí → allí\n- este → aquel/ese\n- hace un año → hacía un año\n\nEl lunes Ana dice: "Mañana voy al médico". Si lo contamos el viernes: *Ana dijo que el martes iba al médico* o *que al día siguiente iba al médico*. Si lo contamos ese mismo lunes, es posible: *Ana ha dicho que mañana va al médico*.\n\nPodemos conservar hoy, mañana o aquí si siguen señalando el mismo día o lugar. También podemos usar fechas y nombres de lugares para evitar ambigüedad.',
        rules=[
            "Hoy puede pasar a aquel día si el relato se hace en otro día.",
            "Ahora puede pasar a entonces si cambia el momento de referencia.",
            "Aquí puede mantenerse si seguimos en el mismo lugar.",
            "Hace un año pasa a hacía un año al medir el intervalo desde un punto del pasado.",
        ],
        examples=[
            GrammarExample(
                text="Me dijo que aquel día no podía quedar.",
                translation=None,
                note='directo: "Hoy no puedo quedar"',
            ),
            GrammarExample(
                text="Aseguró que la semana anterior había estado de vacaciones.",
                translation=None,
            ),
            GrammarExample(
                text="Comentó que entonces vivía en Barcelona.",
                translation=None,
            ),
            GrammarExample(
                text="Explicaron que hacía dos años que no se veían.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=[
            "estilo-indirecto",
            "estilo-indirecto-pasado",
            "conectores-narrativos",
        ],
    ),
    GrammarTopic(
        slug="acentuacion-general",
        title="Acentuación general",
        level="A2",
        category="Adjetivos y adverbios",
        summary="Reglas base de acentuación: agudas, llanas y esdrújulas.",
        explanation="La acentuación gráfica en español sigue reglas generales:\n\n- **Agudas**: llevan tilde si terminan en vocal, **n** o **s** (*café, canción*).\n- **Llanas**: llevan tilde si **no** terminan en vocal, **n** o **s** (*árbol, lápiz*).\n- **Esdrújulas y sobresdrújulas**: llevan tilde siempre (*música, devuélvemelo*).\n\nEn este nivel es clave automatizar las reglas de palabras frecuentes para mejorar la escritura de pasado, futuro y condicional.",
        structure="aguda + (vocal/n/s) -> tilde · llana + (no vocal/n/s) -> tilde · esdrújula -> siempre tilde",
        rules=[
            "Las esdrújulas y sobresdrújulas siempre llevan tilde.",
            "Las agudas solo se tildan si terminan en vocal, n o s.",
            "Las llanas se tildan cuando terminan en consonante distinta de n o s.",
            "La tilde distingue formas verbales: hablo (presente) vs hablé (pasado).",
        ],
        examples=[
            GrammarExample(text="Ayer hablo con Ana -> Ayer hablé con Ana.", translation=None),
            GrammarExample(text="La canción es bonita.", translation=None),
            GrammarExample(text="Ese árbol es muy alto.", translation=None),
            GrammarExample(text="La música me encanta.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ayer hablo con mi madre.",
                correct="Ayer hablé con mi madre.",
                note="Falta tilde en pretérito de primera persona.",
            ),
            GrammarMistake(
                wrong="Ese lapiz es mio.",
                correct="Ese lápiz es mío.",
                note="Lápiz y mío llevan tilde.",
            ),
        ],
        related=["preterito-indefinido-regular", "futuro-simple", "condicional-simple"],
    ),
    GrammarTopic(
        slug="b-v-basico",
        title="Ortografía básica de b y v",
        level="A2",
        category="Verbos",
        summary="Reglas de alta frecuencia para distinguir b y v en escritura cotidiana.",
        explanation="En español, **b** y **v** suenan igual en la mayoría de variedades, por eso conviene aprender reglas prácticas de ortografía.\n\nReglas muy útiles:\n- Después de **m**, se escribe **b**: *también, cambio, ambulancia*.\n- Las terminaciones del imperfecto de -ar llevan **b**: *cantaba, hablábamos*.\n- Muchos verbos en **-bir** van con b: *escribir, recibir, prohibir* (excepto *hervir, servir, vivir*).\n- Muchos verbos en **-olver** van con v: *volver, resolver, devolver*.\n\nEstas reglas reducen errores frecuentes en redacciones A2.",
        structure="m + b · imperfecto -aba/-abas/-ábamos... · -bir (con excepciones) · -olver",
        rules=[
            "Después de m se escribe b.",
            "El imperfecto de verbos en -ar se escribe con b.",
            "Los verbos en -bir suelen escribirse con b, salvo hervir, servir y vivir.",
            "Los verbos terminados en -olver se escriben con v.",
        ],
        examples=[
            GrammarExample(text="También quiero cambiar de trabajo.", translation=None),
            GrammarExample(text="Cuando era niño, jugaba en la plaza.", translation=None),
            GrammarExample(text="Voy a escribir un correo.", translation=None),
            GrammarExample(text="Tenemos que resolver este problema.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Iva a venir, pero no pudo.",
                correct="Iba a venir, pero no pudo.",
                note="El imperfecto de ir se escribe con b: iba.",
            ),
            GrammarMistake(
                wrong="Quiero escrivir mejor.",
                correct="Quiero escribir mejor.",
                note="El verbo escribir termina en -bir y va con b.",
            ),
        ],
        related=[
            "imperativo-afirmativo",
            "preterito-indefinido-regular",
            "condicional-simple",
        ],
    ),
]
