"""Spanish grammar topics — C1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="subjuntivo-concesivo",
        title="Subjuntivo concesivo",
        level="C1",
        category="Subjuntivo",
        summary="Expresar objeción o contraste con aunque, a pesar de que, por más que + subjuntivo.",
        explanation="Las **oraciones concesivas** expresan una objeción o contraste que no impide el cumplimiento de la acción principal. Pueden llevar indicativo o subjuntivo según el matiz:\n\n**Indicativo**: la objeción es un hecho real, conocido.\n- *Aunque **llueve**, saldré a correr.* (Sé que llueve.)\n\n**Subjuntivo**: la objeción es hipotética, desconocida o irrelevante.\n- *Aunque **llueva**, saldré.* (No sé si lloverá o no; da igual.)\n- *Aunque **lloviera**, saldría.* (Hipótesis improbable.)\n\n**Conectores concesivos**:\n- *aunque, a pesar de que, pese a que, si bien, aun cuando*\n- *por más que, por mucho que, por muy + adjetivo + que*\n- *por poco que, por + adjetivo + que*\n\n*Por más que lo intento, no lo consigo.* (indicativo: es un hecho.)\n*Por más que lo intente, no lo conseguiré.* (subjuntivo: hipótesis.)",
        structure="aunque / a pesar de que / por más que / por mucho que + subjuntivo",
        rules=[
            "Concesivas con indicativo: hecho real. Con subjuntivo: hipotético o irrelevante.",
            "El subjuntivo concesivo puede presentar una hipótesis o un hecho conocido que se considera irrelevante para la conclusión.",
            '"Por más que" + subjuntivo refuerza la idea de que el obstáculo no importa.',
            '"Por muy + adjetivo + que" siempre con subjuntivo: "Por muy difícil que sea".',
        ],
        examples=[
            GrammarExample(
                text="Aunque no estés de acuerdo, respeto tu opinión.",
                translation=None,
                note="desacuerdo hipotético o conocido que no impide respetar la opinión",
            ),
            GrammarExample(
                text="Por más que se lo explico, no lo entiende.",
                translation=None,
                note="indicativo: hecho real",
            ),
            GrammarExample(
                text="Por muy cansado que esté, siempre ayuda a los demás.",
                translation=None,
            ),
            GrammarExample(
                text="Aunque me lo hubieras dicho antes, no habría podido ir.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Por muy difícil que es, lo intentaré.",
                correct="Por muy difícil que sea, lo intentaré.",
                note="En la construcción concesiva por muy + adjetivo + que se emplea subjuntivo.",
            ),
        ],
        related=[
            "subjuntivo-final",
            "subjuntivo-relativo",
            "subjuntivo-presente",
            "contraargumentacion",
        ],
    ),
    GrammarTopic(
        slug="subjuntivo-final",
        title="Subjuntivo final",
        level="C1",
        category="Subjuntivo",
        summary="Expresar finalidad con para que, a fin de que, con el objeto de que + subjuntivo.",
        explanation="Las **oraciones finales** expresan la finalidad o propósito de una acción. En español, cuando el sujeto de la principal y de la final es **distinto**, se usa **subjuntivo**:\n\n- *Te llamo para que **vengas**.* (yo llamo ≠ tú vienes)\n- *Cerré la puerta para que no **entrara** el frío.* (yo cerré ≠ el frío entraba)\n\nCuando el sujeto es el **mismo**, se usa **infinitivo**:\n- *Voy al gimnasio para estar en forma.* (yo voy + yo estoy)\n\n**Conectores finales**:\n- *para que, a fin de que, con el objeto de que, con el propósito de que*\n- *con tal de que* (condición mínima suficiente).\n- *no sea que / no vaya a ser que* (finalidad negativa, precaución).\n\n*Lleva el paraguas, no sea que llueva.*",
        structure="para que / a fin de que / con el objeto de que / con tal de que + subjuntivo",
        rules=[
            "Finales con sujeto distinto: para que + subjuntivo.",
            "Finales con mismo sujeto: para + infinitivo.",
            '"No sea que" + subjuntivo expresa cautela o temor.',
            'Con verbo principal en pasado, la final va en imperfecto de subjuntivo: "Fui para que me vieras".',
        ],
        examples=[
            GrammarExample(
                text="Te lo explico para que lo entiendas mejor.",
                translation=None,
            ),
            GrammarExample(
                text="Habla más alto para que todos te oigan.",
                translation=None,
            ),
            GrammarExample(
                text="Salí temprano a fin de que no me pillara el tráfico.",
                translation=None,
            ),
            GrammarExample(
                text="Lleva el abrigo, no sea que haga frío.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Te llamo para que vienes.",
                correct="Te llamo para que vengas.",
                note='"Para que" siempre rige subjuntivo.',
            ),
            GrammarMistake(
                wrong="Fui para que me veas.",
                correct="Fui para que me vieras.",
                note="Con verbo principal en pasado, la final va en imperfecto de subjuntivo.",
            ),
        ],
        related=[
            "subjuntivo-concesivo",
            "subjuntivo-relativo",
            "concordancia-temporal",
        ],
    ),
    GrammarTopic(
        slug="subjuntivo-relativo",
        title="Subjuntivo en oraciones de relativo",
        level="C1",
        category="Subjuntivo",
        summary="Uso del subjuntivo en oraciones de relativo para expresar antecedente desconocido o inexistente.",
        explanation="En las **oraciones de relativo**, la elección entre indicativo y subjuntivo depende del conocimiento o la existencia del antecedente:\n\n**Indicativo**: antecedente conocido, específico, que existe.\n- *Busco al profesor **que habla** japonés.* (Sé que hay uno; lo busco.)\n\n**Subjuntivo**: antecedente desconocido, inespecífico, que quizá no existe.\n- *Busco un profesor **que hable** japonés.* (No sé si existe; lo necesito.)\n\n**Negación del antecedente**:\n- *No hay nadie **que sepa** la respuesta.* (No existe tal persona.)\n- *No encontré ningún libro **que me gustara**.*\n\n**Superlativo o expresiones de unicidad**:\n- *Es el mejor libro **que haya leído** nunca.*\n- *La única persona **que pueda** ayudarte es ella.*",
        structure="antecedente (desconocido/negado) + que + subjuntivo",
        rules=[
            "Indicativo en la relativa: antecedente específico y conocido.",
            "Subjuntivo en la relativa: antecedente inespecífico, hipotético o negado.",
            'Con "el/la/los/las + que" en oraciones explicativas se usa indicativo.',
            'Tras superlativo o palabras como "único/primero/último" es frecuente el subjuntivo.',
        ],
        examples=[
            GrammarExample(
                text="Busco una casa que tenga jardín.",
                translation=None,
                note="subjuntivo: no sé si existe",
            ),
            GrammarExample(
                text="Busco la casa que tiene la puerta azul.",
                translation=None,
                note="indicativo: sé que existe",
            ),
            GrammarExample(
                text="No hay nadie que sepa tocar el piano aquí.",
                translation=None,
            ),
            GrammarExample(
                text="Es lo mejor que me haya pasado en la vida.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Busco alguien que habla inglés.",
                correct="Busco a alguien que hable inglés.",
                note="Antecedente inespecífico → subjuntivo.",
            ),
            GrammarMistake(
                wrong="No hay nadie que sabe la respuesta.",
                correct="No hay nadie que sepa la respuesta.",
                note="Antecedente negado → subjuntivo.",
            ),
        ],
        related=[
            "subjuntivo-concesivo",
            "subjuntivo-final",
            "que-relativo",
            "superlativos",
        ],
    ),
    GrammarTopic(
        slug="pasiva-refleja",
        title="Pasiva refleja avanzada",
        level="C1",
        category="Voz pasiva",
        summary="Usos avanzados de la pasiva refleja en registros formales y académicos.",
        explanation='La **pasiva refleja** con "se" es la forma pasiva predominante en español. En niveles avanzados se dominan sus matices:\n\n**Pasiva refleja vs. impersonal con se**:\n- *Se vende piso.* → pasiva refleja (sujeto: piso; concuerda).\n- *Se vende pisos.* → impersonal (verbo en singular; menos frecuente).\n\n**Con verbos de percepción y comunicación**:\n- *Se oyeron disparos.* / *Se comenta que dimitirá.*\n\n**En textos académicos y científicos**:\n- *Se analizaron los datos. / Se observó un aumento.*\n\n**Diferencias dialectales**:\n- En algunas zonas de América se prefiere la impersonal con "se" + verbo en singular incluso con complemento plural: *Se vende casas* (frecuente en carteles, aunque la norma culta prefiere *Se venden casas*).\n\n**Pasiva refleja con verbos pronominales**:\n- No se puede usar si el verbo ya lleva "se" pronominal: *~~Se se arrepintió~~* → Impersonal con "uno": *Uno se arrepiente*.',
        rules=[
            "En la pasiva refleja el verbo concuerda con el sujeto paciente.",
            'En textos académicos se prefiere la pasiva refleja a la pasiva con "ser".',
            "Con verbos ya pronominales no se puede usar pasiva refleja.",
            'La impersonal con "se" + verbo singular es frecuente pero menos normativa con objetos plurales.',
        ],
        examples=[
            GrammarExample(
                text="Se analizaron más de mil muestras en el laboratorio.",
                translation=None,
            ),
            GrammarExample(
                text="Se espera que las temperaturas bajen en los próximos días.",
                translation=None,
            ),
            GrammarExample(
                text="En esta revista se publican artículos de divulgación científica.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["se-pasivo", "se-impersonal", "voz-pasiva"],
    ),
    GrammarTopic(
        slug="nominalizacion",
        title="Nominalización",
        level="C1",
        category="Avanzado",
        summary="Transformar verbos y adjetivos en sustantivos para crear textos más densos y formales.",
        explanation="La **nominalización** consiste en convertir verbos o adjetivos en sustantivos, lo que permite condensar información y dar un tono más formal y abstracto al discurso.\n\n**Sufijos de nominalización**:\n- *-ción/-sión*: construir → construcción, decidir → decisión\n- *-miento*: pensar → pensamiento, conocer → conocimiento\n- *-dad/-tad*: libre → libertad, bueno → bondad\n- *-eza*: triste → tristeza, rico → riqueza\n- *-ancia/-encia*: tolerar → tolerancia, creer → creencia\n- *-ismo*: optimista → optimismo\n\n**Ventajas de la nominalización**:\n- Economía lingüística: *La construcción del puente se retrasó* (en lugar de *Construir el puente se retrasó*).\n- Impersonalidad: *Se procedió a la revisión de los documentos.*\n\n**Abuso de la nominalización**: en exceso produce textos farragosos. *Proceder a la realización de un estudio* en lugar de *Estudiar*.",
        structure="verbo/adjetivo → sustantivo abstracto (-ción, -miento, -dad, -eza, -ancia...)",
        rules=[
            "Las nominalizaciones son propias de registros formales, académicos y administrativos.",
            "Abusar de ellas genera textos pesados y difíciles de leer.",
            "En textos claros se prefiere el verbo a la nominalización innecesaria.",
            "La nominalización permite tematizar la acción como objeto de análisis.",
        ],
        examples=[
            GrammarExample(
                text="La destrucción del hábitat natural es una amenaza grave.",
                translation=None,
            ),
            GrammarExample(
                text="Se ha producido un aumento significativo de la demanda.",
                translation=None,
            ),
            GrammarExample(
                text="La falta de comunicación fue la causa del conflicto.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["impersonalidad", "registro-formal", "cohesion-textual"],
    ),
    GrammarTopic(
        slug="impersonalidad",
        title="Impersonalidad en el discurso formal",
        level="C1",
        category="Avanzado",
        summary="Mecanismos para ocultar el agente o generalizar: se, uno, pasiva, nominalización.",
        explanation='La **impersonalidad** es un rasgo del discurso formal, académico y científico. Se logra por varios medios:\n\n**Construcciones con "se"**:\n- *Se recomienda reservar con antelación.*\n- *Se puede observar una tendencia al alza.*\n\n**El pronombre "uno"**:\n- *Uno no sabe qué hacer en estas situaciones.*\n- *Cuando uno viaja, se da cuenta de otras realidades.*\n\n**Voz pasiva**:\n- *Los resultados fueron analizados por un equipo de expertos.*\n\n**Nominalización**:\n- *La implementación de la medida se llevará a cabo en enero.*\n\n**Tercera persona plural indeterminada**:\n- *Llaman a la puerta. / Dicen que va a nevar.*\n\n**Infinitivo con valor impersonal**:\n- *Prohibido fumar. / Conviene madrugar.*',
        rules=[
            '"Se" es el recurso más versátil para impersonalizar.',
            '"Uno" personaliza ligeramente pero mantiene generalidad.',
            "La tercera persona plural indeterminada es común en la lengua oral.",
            "El abuso de la impersonalidad puede hacer el texto frío y distante.",
        ],
        examples=[
            GrammarExample(
                text="Se ha demostrado que el ejercicio regular mejora la salud mental.",
                translation=None,
            ),
            GrammarExample(
                text="Cuando uno aprende un idioma, descubre otra cultura.",
                translation=None,
            ),
            GrammarExample(
                text="Dicen que el precio de la vivienda va a bajar.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["nominalizacion", "se-impersonal", "voz-pasiva"],
    ),
    GrammarTopic(
        slug="campos-semanticos",
        title="Campos semánticos y precisión léxica",
        level="C1",
        category="Avanzado",
        summary="Agrupar palabras por significado para ampliar vocabulario con precisión.",
        explanation="Un **campo semántico** es un conjunto de palabras relacionadas por su significado. Dominar los matices entre palabras de un mismo campo permite una comunicación más precisa.\n\n**Ejemplos de campos semánticos**:\n\n**Movimiento**: *andar, caminar, deambular, pasear, vagar, errar, marchar, desfilar, corretear, trotar*\n- No es lo mismo *caminar* (neutro) que *deambular* (sin rumbo) o *desfilar* (en formación).\n\n**Habla**: *decir, hablar, pronunciar, declarar, afirmar, susurrar, murmurar, gritar, vociferar, balbucear, tartamudear*\n- *Susurrar* es hablar bajito; *vociferar* es gritar con furia.\n\n**Mirada**: *ver, mirar, observar, contemplar, examinar, ojear, atisbar, vislumbrar, escrutar, divisar*\n- *Contemplar* implica admiración; *escrutar* implica análisis minucioso.\n\n**Temperatura**: *caliente, cálido, templado, tibio, fresco, frío, gélido, helado*\n- *Tibio* es menos que caliente; *gélido* es extremadamente frío.",
        rules=[
            "Los sinónimos dentro de un campo semántico rara vez son intercambiables al 100%.",
            "Cada palabra tiene matices de intensidad, formalidad o contexto.",
            "Consultar diccionarios de uso y de sinónimos para afinar la precisión.",
            'En contextos formales se prefiere la palabra más precisa ("manifestar" en lugar de "decir").',
        ],
        examples=[
            GrammarExample(
                text='No es lo mismo decir "hace frío" que "hace un frío gélido". La segunda opción intensifica.',
                translation=None,
            ),
            GrammarExample(
                text='En el artículo el periodista no "dice", sino que "sostiene" o "argumenta".',
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["precision-lexica", "derivacion", "registro-formal"],
    ),
    GrammarTopic(
        slug="derivacion",
        title="Derivación y familias de palabras",
        level="C1",
        category="Avanzado",
        summary="Formar nuevas palabras con prefijos y sufijos: aumentar, disminuir o matizar el significado.",
        explanation="La **derivación** es el mecanismo por el cual se forman nuevas palabras añadiendo prefijos y sufijos a una raíz.\n\n**Prefijos productivos**:\n- *re-* (repetición): rehacer, releer, reescribir\n- *des-* (negación, inversión): deshacer, desconectar, desconfiar\n- *in-/im-/i-* (negación): incapaz, imposible, ilegal\n- *pre-* (anterioridad): predecir, prejuzgar, precocinar\n- *sobre-* (exceso): sobrevalorar, sobrecargar, sobrevolar\n- *sub-* (debajo, inferior): subestimar, subterráneo, subtítulo\n- *inter-* (entre): internacional, intercambiar, interconectar\n- *multi-/pluri-* (muchos): multinacional, pluriempleo\n- *anti-* (oposición): antinatural, antivirus, antirrobo\n\n**Sufijos productivos**:\n- *-ble* (capacidad): comible, lavable, creíble\n- *-dor/-dora* (agente): trabajador, escritora, conductor\n- *-ería* (lugar, actividad): panadería, carnicería\n- *-azo* (golpe, aumentativo): portazo, golazo, cochazo\n- *-ito/-illo* (diminutivo): poquito, chiquillo, mesita",
        rules=[
            'Un mismo prefijo puede tener varios significados: "re-" puede ser repetición o intensificación.',
            "La derivación permite crear palabras que no están en el diccionario pero son comprensibles.",
            "No todos los prefijos se pueden aplicar a todas las palabras; hay restricciones léxicas.",
            "Los sufijos apreciativos (-ito, -azo, -ón) son muy productivos en el habla coloquial.",
        ],
        examples=[
            GrammarExample(
                text="Es imposible predecir el resultado con exactitud.",
                translation=None,
            ),
            GrammarExample(
                text="Tendrás que reescribir el informe porque está incompleto.",
                translation=None,
            ),
            GrammarExample(
                text="¡Menudo golazo marcó en el último minuto!",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["campos-semanticos", "precision-lexica", "nominalizacion"],
    ),
    GrammarTopic(
        slug="precision-lexica",
        title="Precisión léxica",
        level="C1",
        category="Avanzado",
        summary="Elegir la palabra exacta: diferencias entre sinónimos parciales y cómo evitar la vaguedad.",
        explanation="La **precisión léxica** consiste en seleccionar la palabra que expresa exactamente lo que se quiere decir, evitando términos comodín como *cosa, hacer, tener, poner, decir*.\n\n**Palabras comodín y alternativas**:\n- *Cosa* → elemento, aspecto, factor, cuestión, asunto, objeto, fenómeno\n- *Hacer* → realizar, elaborar, fabricar, ejecutar, confeccionar, emprender\n- *Tener* → poseer, disponer de, contar con, albergar, presentar, sufrir\n- *Decir* → afirmar, manifestar, declarar, expresar, sostener, apuntar\n- *Poner* → colocar, situar, depositar, instalar, aplicar, introducir\n\n**Distinción de falsos sinónimos**:\n- *Escuchar* (prestar atención) ≠ *oír* (percibir sonido)\n- *Mirar* (dirigir la vista) ≠ *ver* (percibir con la vista)\n- *Pedir* (solicitar algo) ≠ *preguntar* (formular una pregunta)\n- *Conocer* (a personas, lugares, hechos) ≠ *saber* (información, habilidades)\n\nEn niveles C1 se espera el uso de un léxico variado y preciso.",
        rules=[
            "Evitar palabras comodín; buscar el término más específico.",
            "Distinguir entre sinónimos parciales: no son intercambiables en todos los contextos.",
            "Consultar diccionarios combinatorios para saber qué verbo acompaña a cada sustantivo.",
            'El contexto determina la elección: no es lo mismo "oler" que "apestar" o "perfumar".',
        ],
        examples=[
            GrammarExample(
                text="El gobierno implementó nuevas medidas para paliar la crisis.",
                translation=None,
                note='no "hizo" medidas ni "arreglar" la crisis',
            ),
            GrammarExample(
                text="Escucho música mientras trabajo, pero oigo el ruido del tráfico de fondo.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["campos-semanticos", "derivacion", "falsos-amigos"],
    ),
    GrammarTopic(
        slug="ironia",
        title="Ironía",
        level="C1",
        category="Avanzado",
        summary="Expresar lo contrario de lo que se piensa con intención humorística o crítica.",
        explanation="La **ironía** consiste en decir lo contrario de lo que se quiere comunicar, esperando que el receptor lo interprete correctamente por el contexto o la entonación.\n\n**Marcas de ironía en español**:\n- Entonación particular (en oral).\n- Uso de cuantificadores exagerados: *¡Qué listo eres!* (cuando ha hecho algo torpe).\n- Adjetivos elogiosos en contexto negativo: *¡Menudo negocio has montado!*\n- Diminutivos irónicos: *¡Vaya problemita tenemos!*\n- Combinación de formalidad excesiva con crítica: *Su excelentísima majestad ha decidido no fregar los platos.*\n\n**Tipos de ironía**:\n- **Ironía verbal**: lo dicho es lo contrario de lo significado.\n- **Ironía situacional**: el resultado contradice lo esperado.\n- **Sarcasmo**: ironía con intención hiriente.\n\nEn español, la ironía es muy frecuente en la conversación cotidiana y en el humor.",
        rules=[
            "La ironía depende del contraste entre lo dicho y el contexto.",
            "En la escritura, la ironía se marca con comillas, signos de exclamación o elección léxica.",
            "El sarcasmo es ironía más agresiva.",
            "En contextos formales se evita la ironía para no generar malentendidos.",
        ],
        examples=[
            GrammarExample(
                text="¡Qué bien! Justo lo que necesitaba.",
                translation=None,
                note="dicho al recibir una mala noticia",
            ),
            GrammarExample(
                text="Menudo amigo estás hecho.",
                translation=None,
                note="ironía: no es buen amigo",
            ),
            GrammarExample(
                text="Claro, tú siempre tienes razón.",
                translation=None,
                note="dicho con tono irónico",
            ),
        ],
        common_mistakes=[],
        related=["sarcasmo", "doble-sentido", "expresiones-coloquiales"],
    ),
    GrammarTopic(
        slug="sarcasmo",
        title="Sarcasmo",
        level="C1",
        category="Avanzado",
        summary="Ironía mordaz con intención de herir, burlarse o criticar duramente.",
        explanation='El **sarcasmo** es una forma de ironía más agresiva y directa que busca ridiculizar, humillar o criticar de forma mordaz.\n\n**Características del sarcasmo**:\n- Intención manifiesta de herir o burlarse.\n- Tono de voz más cortante que la ironía.\n- Suele incluir hipérboles o comparaciones hirientes.\n\n**Ejemplos**:\n- *"Eres un genio"* (después de que alguien cometa un error evidente).\n- *"No te esfuerces demasiado"* (cuando alguien no está haciendo nada).\n- *"Qué sorpresa, has llegado tarde otra vez"* (falso asombro).\n\n**Diferencia con la ironía**:\n- La ironía puede ser humorística o incluso afectuosa.\n- El sarcasmo siempre tiene una carga negativa y busca provocar.\n\nEn el ámbito hispanohablante el sarcasmo varía culturalmente: es muy frecuente en España, mientras que en algunos países latinoamericanos puede considerarse más agresivo.',
        rules=[
            "El sarcasmo se apoya en la exageración y el falso elogio.",
            "La entonación es crucial para distinguir sarcasmo de elogio sincero.",
            "En la escritura, el sarcasmo puede marcarse con comillas o cursiva.",
            "Culturalmente, el sarcasmo no se percibe igual en todos los países hispanohablantes.",
        ],
        examples=[
            GrammarExample(
                text="No, si tú eres muy listo.",
                translation=None,
                note="sarcasmo: ha sido imprudente",
            ),
            GrammarExample(
                text="Sí, claro, ahora mismo lo hago.",
                translation=None,
                note="dicho cuando no hay intención de hacerlo",
            ),
        ],
        common_mistakes=[],
        related=["ironia", "doble-sentido", "expresiones-coloquiales"],
    ),
    GrammarTopic(
        slug="doble-sentido",
        title="Doble sentido",
        level="C1",
        category="Avanzado",
        summary="Ambigüedad intencionada: palabras o frases con más de una interpretación.",
        explanation="El **doble sentido** consiste en usar palabras o expresiones que admiten dos interpretaciones, generalmente una inocente y otra maliciosa, humorística o crítica.\n\n**Mecanismos del doble sentido**:\n\n**Homonimia y polisemia**:\n- *Banco* (asiento / entidad financiera): *Me senté en el banco a esperar.*\n- *Gato* (animal / herramienta para elevar coches).\n\n**Ambigüedad sintáctica**:\n- *Vi a tu hermano con prismáticos.* (¿Quién llevaba los prismáticos?)\n\n**Juegos de palabras (calambur)**:\n- *Entre el clavel y la rosa, su majestad escoja.* (es coja / escoja)\n\n**Contextos marcados**:\n- El doble sentido es habitual en chistes, publicidad y humor.\n- En literatura (Cervantes, Quevedo) el doble sentido es recurso erudito.\n\nEn niveles C1 se espera comprender y, con cuidado, usar el doble sentido respetando el contexto y la relación con el interlocutor.",
        rules=[
            "El doble sentido depende del contexto y de la complicidad entre hablantes.",
            "La ambigüedad puede ser léxica (una palabra) o sintáctica (estructura de la oración).",
            "En contextos formales se evita el doble sentido para no generar malentendidos.",
            "Muchos refranes y frases hechas admiten juegos de doble sentido.",
        ],
        examples=[
            GrammarExample(
                text="Como siempre, llega a la hora.",
                translation=None,
                note="depende de la entonación y el contexto",
            ),
            GrammarExample(
                text="Se venden calcetines para caballeros de lana.",
                translation=None,
                note="ambigüedad sintáctica",
            ),
        ],
        common_mistakes=[],
        related=["ironia", "sarcasmo", "metaforas"],
    ),
    GrammarTopic(
        slug="recursos-retoricos",
        title="Recursos retóricos",
        level="C1",
        category="Avanzado",
        summary="Herramientas clásicas de la retórica aplicadas al discurso argumentativo.",
        explanation="Los **recursos retóricos** son técnicas persuasivas heredadas de la tradición clásica que organizan y embellecen el discurso.\n\n**Operaciones retóricas**:\n1. *Intellectio*: comprender el tema.\n2. *Inventio*: encontrar argumentos.\n3. *Dispositio*: ordenar el discurso (introducción, desarrollo, conclusión).\n4. *Elocutio*: elegir las palabras y figuras adecuadas.\n5. *Memoria* y *actio*: memorizar y pronunciar.\n\n**Figuras retóricas argumentativas**:\n- **Pregunta retórica**: pregunta que no espera respuesta. *¿Acaso no merecemos un futuro mejor?*\n- **Anáfora**: repetición al inicio. *Queremos justicia, queremos paz, queremos futuro.*\n- **Paralelismo**: estructuras sintácticas similares. *Sin esfuerzo no hay éxito; sin riesgo no hay gloria.*\n- **Antítesis**: contraposición. *Es pequeño en estatura pero grande en corazón.*\n- **Tríada o regla de tres**: enumerar tres elementos para dar fuerza.\n\nEstos recursos son frecuentes en discursos políticos, publicidad y ensayos.",
        rules=[
            "Las preguntas retóricas involucran al receptor sin esperar respuesta literal.",
            "La anáfora y el paralelismo crean ritmo y énfasis.",
            "La antítesis resalta contrastes para reforzar un argumento.",
            "La regla de tres es un patrón persuasivo muy efectivo.",
        ],
        examples=[
            GrammarExample(
                text="¿Cuántas veces tenemos que repetir lo mismo?",
                translation=None,
                note="pregunta retórica",
            ),
            GrammarExample(
                text="Trabajamos sin descanso, luchamos sin tregua, soñamos sin límites.",
                translation=None,
                note="paralelismo y tríada",
            ),
            GrammarExample(
                text="Es la peor de las soluciones, pero es la única que tenemos.",
                translation=None,
                note="antítesis",
            ),
        ],
        common_mistakes=[],
        related=["persuasion", "estructura-argumentativa", "figuras-literarias"],
    ),
    GrammarTopic(
        slug="persuasion",
        title="Persuasión y estrategias discursivas",
        level="C1",
        category="Avanzado",
        summary="Técnicas para convencer: apelación a la razón (logos), a la emoción (pathos) y a la credibilidad (ethos).",
        explanation="La **persuasión** es el arte de convencer. Según la retórica clásica (Aristóteles), se apoya en tres pilares:\n\n**Logos (razón)**:\n- Argumentos lógicos, datos, estadísticas, hechos comprobables.\n- *Según un estudio de la OMS, el 80% de los casos...*\n\n**Pathos (emoción)**:\n- Apelar a sentimientos: empatía, miedo, esperanza, indignación.\n- *Imagina que fueras tú el que necesita ayuda...*\n\n**Ethos (credibilidad del emisor)**:\n- Construir confianza mostrando conocimiento, experiencia o valores.\n- *Como médico con veinte años de experiencia, puedo afirmar que...*\n\n**Estrategias lingüísticas persuasivas**:\n- Primera persona plural inclusiva: *Todos sabemos que... / Nos afecta a todos.*\n- Verbos de opinión atenuados o reforzados.\n- Uso de ejemplos concretos y cercanos.\n- Anticipar y refutar objeciones.",
        rules=[
            "Combinar logos, pathos y ethos para una argumentación completa.",
            "El pathos solo es efectivo si se equilibra con argumentos sólidos.",
            "La credibilidad (ethos) se construye desde el inicio.",
            'En español, el uso del plural inclusivo es muy persuasivo: "Tenemos que actuar".',
        ],
        examples=[
            GrammarExample(
                text="Todos sabemos que el cambio climático es real. Como sociedad, tenemos la responsabilidad de actuar. No podemos mirar hacia otro lado.",
                translation=None,
            ),
            GrammarExample(
                text="Según los últimos datos del INE, la pobreza infantil ha aumentado un 12%. Detrás de cada cifra hay un niño que no tiene para comer.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=[
            "recursos-retoricos",
            "estructura-argumentativa",
            "figuras-literarias",
        ],
    ),
    GrammarTopic(
        slug="figuras-literarias",
        title="Figuras literarias",
        level="C1",
        category="Avanzado",
        summary="Principales figuras retóricas: metáfora, metonimia, sinécdoque, hipérbaton, asíndeton, polisíndeton.",
        explanation="Las **figuras literarias** o **tropos** enriquecen el lenguaje más allá de su uso literal.\n\n**Figuras de significado (tropos)**:\n- **Metáfora**: identificación de dos realidades. *La vida es un río.*\n- **Metonimia**: sustitución por relación. *Bebió una copa.* (continente por contenido).\n- **Sinécdoque**: la parte por el todo o viceversa. *Quedan tres almas en el pueblo.* (alma por persona).\n- **Sinestesia**: mezcla de sensaciones. *Un silencio amargo.*\n\n**Figuras de orden**:\n- **Hipérbaton**: alterar el orden lógico. *Del salón en el ángulo oscuro...* (Bécquer).\n- **Anáfora**: repetición al inicio de versos o frases.\n\n**Figuras de repetición**:\n- **Aliteración**: repetición de sonidos. *El ruido con que rueda la ronca tempestad.*\n- **Polisíndeton**: multiplicación de conjunciones. *Y llegó, y miró, y venció.*\n- **Asíndeton**: omisión de conjunciones. *Llegué, vi, vencí.*\n\nEn niveles C1 se espera reconocer estas figuras y usarlas puntualmente.",
        rules=[
            "La metáfora es la figura más común y versátil.",
            "Metonimia y sinécdoque son frecuentes incluso en la lengua coloquial.",
            "El hipérbaton es más literario; en prosa se usa con moderación.",
            "Polisíndeton ralentiza; asíndeton acelera el ritmo.",
        ],
        examples=[
            GrammarExample(
                text="Y los niños corren, y los perros ladran, y los coches pitan, y el mundo sigue girando.",
                translation=None,
                note="polisíndeton",
            ),
            GrammarExample(
                text="Llegué, vi, vencí.",
                translation=None,
                note="asíndeton",
            ),
            GrammarExample(
                text="El dulce sonido del silencio.",
                translation=None,
                note="sinestesia",
            ),
        ],
        common_mistakes=[],
        related=["metaforas", "recursos-retoricos", "descripcion-literaria"],
    ),
    GrammarTopic(
        slug="espanol-latinoamerica",
        title="Español de América Latina",
        level="C1",
        category="Avanzado",
        summary="Principales rasgos del español hablado en Latinoamérica frente al español peninsular.",
        explanation="El **español de América Latina** reúne variedades diversas, con rasgos legítimos que no deben tratarse como errores.\n\n**Fonética**:\n- **Seseo**: s y las grafías z/c ante e/i representan /s/: *casa* y *caza* son homófonos. También existe en Canarias y partes de Andalucía.\n- **Yeísmo**: ll e y no se distinguen en numerosas variedades americanas y españolas. Su realización cambia por región, por ejemplo en el Río de la Plata.\n- La aspiración o pérdida de s final de sílaba aparece en algunas zonas, especialmente caribeñas y costeras, pero no es general en América.\n\n**Gramática**:\n- **Ustedes** es el tratamiento plural habitual tanto formal como informal.\n- El **voseo** tiene distintas formas y valoraciones regionales: *vos tenés* es un ejemplo rioplatense.\n- El uso del perfecto y el indefinido varía: *Ya lo hice* es frecuente en muchas zonas; el perfecto también tiene usos propios, no desaparece.\n- Los diminutivos, como *ahorita* o *cafecito*, tienen funciones que dependen de cada comunidad.\n\n**Léxico**: *carro, coche, auto*; *computadora, ordenador*; *celular, móvil*. Las preferencias varían dentro de cada país y hay aportaciones de lenguas indígenas y africanas.",
        rules=[
            "El seseo no es un error; es la norma culta en América Latina.",
            '"Ustedes" sustituye a "vosotros" en toda América; la conjugación es la de 3ª persona plural.',
            "El voseo modifica la conjugación: vos tenés, vos querés, vos sos.",
            "El léxico varía enormemente por país; una palabra inocente en uno puede ser ofensiva en otro.",
        ],
        examples=[
            GrammarExample(
                text="Ustedes tienen razón.",
                translation=None,
                note="única forma plural en América Latina",
            ),
            GrammarExample(
                text="Vos sabés lo que hiciste.",
                translation=None,
                note="voseo rioplatense",
            ),
            GrammarExample(
                text="Ahorita te llamo.",
                translation=None,
                note='diminutivo; el alcance temporal de "ahorita" depende del contexto y de la región',
            ),
        ],
        common_mistakes=[],
        related=["diferencias-regionales", "voseo", "falsos-amigos"],
    ),
    GrammarTopic(
        slug="diferencias-regionales",
        title="Diferencias regionales en el español",
        level="C1",
        category="Avanzado",
        summary="Variación léxica y gramatical entre los países hispanohablantes.",
        explanation="El español es una lengua pluricéntrica con varias normas cultas. Las fronteras lingüísticas no coinciden siempre con las nacionales.\n\n**Léxico**:\n- *Coche, carro, auto* se distribuyen de forma diferente según la región; en México se usan tanto coche como carro.\n- *Ordenador/computadora* y *móvil/celular* muestran preferencias regionales.\n- *Papa* se usa en América, Canarias y zonas de Andalucía; *patata* es frecuente en el resto de España.\n- *Coger* es neutral en España y en parte de América; tiene un sentido sexual vulgar en países como México y Argentina. Hay que atender al país y al contexto.\n\n**Gramática**:\n- El leísmo es el uso de le/les como complemento directo. Se admite le para persona masculina singular: *A Juan le vi*. No todo leísmo pertenece a la norma general.\n- El voseo presenta diferentes patrones, no una única conjugación continental.\n- El perfecto y el indefinido varían dentro de España y América; no forman una oposición rígida entre continentes.\n\n**Tratamientos**: en algunas zonas de Colombia, usted también se usa entre personas cercanas. Ustedes es formal e informal en América y Canarias; en buena parte de España contrasta con vosotros/as informal. La relación entre interlocutores y la situación también condicionan la elección.",
        rules=[
            'No existe una variedad "correcta" del español; cada norma culta es válida.',
            "Al aprender español conviene elegir una variedad meta y ser consciente de las demás.",
            "El contexto determina qué variedad usar: en entornos internacionales se tiende a un español neutro.",
            "Muchas palabras son comprensibles en todos los países aunque no sean las locales.",
        ],
        examples=[
            GrammarExample(
                text="Voy a coger el autobús.",
                translation=None,
                note="neutral en España y parte de América; puede tener connotaciones vulgares en otros países",
            ),
            GrammarExample(
                text="Manejo hasta tu casa en media hora.",
                translation=None,
                note="Argentina/México",
            ),
            GrammarExample(
                text="¿Me pasas la papa, por favor?",
                translation=None,
                note="papa se usa en América, Canarias y zonas de Andalucía; patata es frecuente en otras zonas españolas",
            ),
        ],
        common_mistakes=[],
        related=["espanol-latinoamerica", "voseo", "falsos-amigos"],
    ),
    GrammarTopic(
        slug="voseo",
        title="Voseo",
        level="C1",
        category="Avanzado",
        summary='El uso de "vos" como pronombre de segunda persona singular en el español rioplatense y centroamericano.',
        explanation="El **voseo** es el uso del pronombre **vos** en lugar de **tú** para la segunda persona del singular. Es normativo y culto en Argentina, Uruguay y Paraguay, y frecuente en partes de Centroamérica.\n\n**Conjugación del voseo (rioplatense)**:\n\n| Verbo | Presente | Imperativo |\n|-------|----------|------------|\n| tener | vos tenés | tené |\n| querer | vos querés | queré |\n| poder | vos podés | podé |\n| ser | vos sos | sé |\n| ir | vos vas | andá (irregular) |\n| haber | vos has | — |\n\n**Patrón**: se acentúa la última sílaba; se pierde la -d final del imperativo.\n\n**Variantes regionales**:\n- *Voseo pronominal y verbal* (Argentina): *vos tenés*.\n- *Voseo solo verbal* (Chile, zonas de Colombia): *tú tenís*.\n\nEl voseo se combina con el pronombre *te* y el posesivo *tu/tuyo*: *Vos te llamás... y tu casa...*",
        structure="vos + verbo con acento en la última sílaba (vos tenés, vos querés, vos sos)",
        rules=[
            "El voseo es normativo y culto en las regiones donde se usa.",
            "La conjugación difiere de la de tú: se pierde el diptongo (tú tienes → vos tenés).",
            "El imperativo voseante pierde la -d: hablá, comé, escribí.",
            'El verbo "ser" tiene forma propia: vos sos (no ~~vos erés~~).',
        ],
        examples=[
            GrammarExample(
                text="Vos tenés que venir a conocer Buenos Aires.",
                translation=None,
                note="voseo rioplatense",
            ),
            GrammarExample(text="¿De dónde sos?", translation=None),
            GrammarExample(
                text="Hablá más fuerte que no te escucho.",
                translation=None,
                note="imperativo voseante",
            ),
        ],
        common_mistakes=[],
        related=[
            "espanol-latinoamerica",
            "diferencias-regionales",
            "pronombres-sujeto",
        ],
    ),
    GrammarTopic(
        slug="sintesis-textual",
        title="Síntesis textual",
        level="C1",
        category="Avanzado",
        summary="Resumir, parafrasear y sintetizar información de forma precisa y concisa.",
        explanation="La **síntesis textual** es la habilidad de condensar información manteniendo las ideas esenciales. Es fundamental en el ámbito académico y profesional.\n\n**Técnicas de síntesis**:\n\n1. **Identificar la idea principal** y las ideas secundarias.\n2. **Eliminar**: ejemplos, repeticiones, digresiones.\n3. **Generalizar**: agrupar detalles bajo un concepto común.\n4. **Parafrasear**: expresar con palabras propias sin cambiar el significado.\n\n**Paráfrasis vs. resumen**:\n- *Paráfrasis*: misma extensión aproximadamente, distintas palabras.\n- *Resumen*: reducción significativa manteniendo lo esencial.\n\n**Verbos útiles para sintetizar**:\n- *resumir, sintetizar, condensar, recapitular*\n- *El autor sostiene / argumenta / cuestiona / analiza / propone*\n\n**Conectores de síntesis**: *en resumen, en síntesis, en conclusión, en pocas palabras, en definitiva*.",
        rules=[
            "Un buen resumen no aporta opiniones personales.",
            "La paráfrasis no debe modificar el sentido original.",
            "Identificar la tesis del autor es el primer paso para sintetizar.",
            "En síntesis académicas se debe citar la fuente original.",
        ],
        examples=[
            GrammarExample(
                text="En resumen, el artículo plantea que el bilingüismo aporta beneficios cognitivos medibles, aunque advierte de la necesidad de más estudios longitudinales.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["critica-constructiva", "reformulacion", "estructura-argumentativa"],
    ),
    GrammarTopic(
        slug="critica-constructiva",
        title="Crítica constructiva",
        level="C1",
        category="Avanzado",
        summary="Expresar desacuerdo u objeciones de forma respetuosa y productiva.",
        explanation="La **crítica constructiva** señala aspectos mejorables de una idea o trabajo sin descalificar, ofreciendo alternativas y manteniendo un tono respetuoso.\n\n**Estrategias lingüísticas**:\n\n**Atenuar la crítica**:\n- *Quizás se podría considerar...*\n- *Me pregunto si no sería mejor...*\n- *Entiendo tu punto, pero...*\n\n**Enfocar en el problema, no en la persona**:\n- *El informe contiene algunos errores.* (no *Eres descuidado.*)\n- *La propuesta necesita más desarrollo.* (no *Es una mala propuesta.*)\n\n**Ofrecer alternativas o soluciones**:\n- *Tal vez podríamos probar con...*\n- *¿Has considerado la posibilidad de...?*\n- *Una alternativa sería...*\n\n**Usar condicional y subjuntivo para atenuar**:\n- *Convendría revisar esta sección.*\n- *Sería recomendable que incluyeras datos más recientes.*\n\nEn español la crítica suele ser más indirecta que en inglés por razones culturales de cortesía.",
        rules=[
            "Atenuar con condicional y subjuntivo.",
            "Separar a la persona del problema.",
            "Siempre ofrecer una alternativa o solución.",
            "Empezar con un aspecto positivo antes de señalar lo mejorable.",
        ],
        examples=[
            GrammarExample(
                text="Me ha gustado mucho tu presentación. Quizás podrías añadir más ejemplos para hacerla aún más clara.",
                translation=None,
            ),
            GrammarExample(
                text="Entiendo tu enfoque, pero me pregunto si no sería mejor considerar otras opciones.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=[
            "reformulacion",
            "sintesis-textual",
            "condicional-simple",
            "matizadores",
        ],
    ),
    GrammarTopic(
        slug="reformulacion",
        title="Reformulación",
        level="C1",
        category="Avanzado",
        summary="Parafrasear y reformular para aclarar, corregir o matizar lo dicho.",
        explanation="La **reformulación** es una estrategia discursiva que permite volver a expresar una idea de forma más clara, precisa o matizada.\n\n**Tipos de reformulación**:\n\n**Explicativa** (aclarar):\n- *es decir, o sea, esto es, a saber, en otras palabras*\n- *La situación es insostenible, es decir, no podemos seguir así.*\n\n**Rectificativa** (corregir):\n- *mejor dicho, más bien, digo, quiero decir*\n- *Es caro, mejor dicho, es carísimo.*\n\n**Recapitulativa** (resumir):\n- *en resumen, en conclusión, en definitiva, total, al fin y al cabo*\n- *Total, que no vamos a la playa.*\n\n**De distanciamiento** (matizar):\n- *en cualquier caso, de todas formas, en todo caso*\n- *No sé si es la mejor opción; en cualquier caso, es la que tenemos.*\n\nLa reformulación es una habilidad clave en el nivel C1 para negociar significado, aclarar malentendidos y demostrar dominio léxico.",
        rules=[
            '"Es decir" introduce una aclaración de lo dicho.',
            '"Mejor dicho" corrige o matiza lo anterior.',
            '"Total" en registro coloquial introduce un resumen o conclusión.',
            "La reformulación demuestra control activo del discurso.",
        ],
        examples=[
            GrammarExample(
                text="El proyecto es viable, es decir, contamos con los recursos necesarios para llevarlo a cabo.",
                translation=None,
            ),
            GrammarExample(
                text="No me gusta la idea. Mejor dicho, me parece terrible.",
                translation=None,
            ),
            GrammarExample(
                text="No estudié nada, llovió todo el día y encima perdí el tren. Total, un desastre de día.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["sintesis-textual", "critica-constructiva", "conectores-avanzados"],
    ),
    GrammarTopic(
        slug="ortotipografia-academica",
        title="Ortotipografía académica",
        level="C1",
        category="Avanzado",
        summary="Convenciones de mayúsculas, comillas, cursivas y citación breve en textos formales.",
        explanation="La **ortotipografía académica** regula la presentación formal del texto y contribuye a su legibilidad y credibilidad.\n\nAspectos clave:\n- **Mayúsculas/minúsculas**: instituciones, cargos, títulos y gentilicios según norma.\n- **Comillas**: preferencia de comillas españolas (« ») en edición formal; comillas dobles o simples para niveles internos.\n- **Cursiva**: extranjerismos no adaptados, títulos de obras largas y énfasis técnico puntual.\n- **Abreviaturas y siglas**: coherencia, primer desarrollo y uso posterior estabilizado.\n\nEn C1 se espera aplicar estas convenciones en informes, ensayos y reseñas de manera consistente.",
        structure="norma ortotipografica + coherencia editorial en todo el texto",
        rules=[
            "Mantener un criterio único de comillas en todo el documento.",
            "Usar cursiva para extranjerismos no adaptados y títulos de obras largas.",
            "Evitar mayúsculas innecesarias en meses, días y gentilicios.",
            "Desarrollar siglas la primera vez que aparecen.",
        ],
        examples=[
            GrammarExample(
                text="Según el Instituto Nacional de Estadística (INE), la tendencia se mantiene estable.",
                translation=None,
            ),
            GrammarExample(
                text="El concepto de *feedback* se ha integrado en la didáctica actual.",
                translation=None,
            ),
            GrammarExample(
                text="La autora sostiene: «El cambio no es opcional, sino imprescindible».",
                translation=None,
            ),
            GrammarExample(
                text="En abril se publicará un nuevo informe sobre educación superior.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="En Abril, El Ministerio publicó datos.",
                correct="En abril, el ministerio publicó datos.",
                note="Meses y cargos comunes van en minúscula en uso general.",
            ),
            GrammarMistake(
                wrong="El informe afirma \"La medida es eficaz'.",
                correct="El informe afirma: «La medida es eficaz».",
                note="Hay que cerrar correctamente comillas y puntuación.",
            ),
        ],
        related=["registro-formal", "sintesis-textual", "edicion"],
    ),
]
