"""Italian grammar topics — B2."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="congiuntivo-imperfetto",
        title="Congiuntivo imperfetto",
        level="B2",
        category="Congiuntivo",
        summary="Il congiuntivo imperfetto: formazione e uso nel passato.",
        explanation="Il **congiuntivo imperfetto** si usa:\n- Nel periodo ipotetico del 2 tipo: *Se potessi, verrei.*\n- Dopo verbi al passato + che: *Pensavo che fosse vero.*\n- Dopo vorrei che: *Vorrei che tu venissi.*\n\nEssere è irregolare: fossi, fossi, fosse, fossimo, foste, fossero.",
        structure="-are: -assi/-assi/-asse/-assimo/-aste/-assero\n-ere: -essi/-essi/-esse/-essimo/-este/-essero\n-ire: -issi/-issi/-isse/-issimo/-iste/-issero",
        rules=[
            "Usato nella protasi del periodo ipotetico (2 tipo).",
            "Usato dopo verbi al passato + che (concordanza).",
            "Dopo vorrei che: Vorrei che tu venissi.",
            "Essere: fossi, fossi, fosse...",
        ],
        examples=[
            GrammarExample(
                text="Se potessi, viaggerei in tutto il mondo.",
                translation=None,
            ),
            GrammarExample(
                text="Pensavo che tu fossi già partito.",
                translation=None,
            ),
            GrammarExample(text="Vorrei che fosse sempre estate.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se potrei, viaggerei.",
                correct="Se potessi, viaggerei.",
                note="Nella protasi ipotetica si usa il congiuntivo imperfetto; se interrogativo può ammettere il condizionale.",
            ),
            GrammarMistake(
                wrong="Pensavo che tu eri partito.",
                correct="Pensavo che tu fossi partito.",
                note="Verbo principale al passato: congiuntivo imperfetto.",
            ),
        ],
        related=[
            "congiuntivo-presente",
            "congiuntivo-trapassato",
            "concordanza-congiuntivo",
            "periodo-ipotetico-2",
        ],
    ),
    GrammarTopic(
        slug="congiuntivo-trapassato",
        title="Congiuntivo trapassato",
        level="B2",
        category="Congiuntivo",
        summary="Il congiuntivo trapassato: periodo ipotetico del 3 tipo (irrealta).",
        explanation="**Congiuntivo trapassato** = congiuntivo imperfetto di avere/essere + participio passato.\n\n- avere: avessi, avessi, avesse, avessimo, aveste, avessero + participio.\n- essere: fossi... + participio (concordato).\n\nUsi:\n- Periodo ipotetico 3 tipo: *Se avessi studiato, avresti passato l'esame.*\n- Concordanza: *Pensavo che fosse già arrivato.*",
        structure="congiuntivo imperfetto di avere/essere + participio passato",
        rules=[
            "Congiuntivo imperfetto di avere/essere + participio passato.",
            "Periodo ipotetico 3 tipo (irrealta nel passato).",
            "Concordanza: anteriorità rispetto a un passato.",
            "Con essere il participio concorda col soggetto.",
        ],
        examples=[
            GrammarExample(
                text="Se avessi saputo, sarei venuto prima.",
                translation=None,
            ),
            GrammarExample(
                text="Credevo che fossero già partiti.",
                translation=None,
            ),
            GrammarExample(
                text="Se avessi studiato, avresti passato l'esame.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se avrei saputo, sarei venuto.",
                correct="Se avessi saputo, sarei venuto.",
                note="Per questa condizione passata non realizzata si usa il congiuntivo trapassato.",
            ),
            GrammarMistake(
                wrong="Credevo che hanno finito.",
                correct="Credevo che avessero finito.",
                note="Verbo principale al passato + anteriorità = congiuntivo trapassato.",
            ),
        ],
        related=[
            "congiuntivo-imperfetto",
            "periodo-ipotetico-2",
            "se-congiuntivo",
            "concordanza-congiuntivo",
        ],
    ),
    GrammarTopic(
        slug="concordanza-congiuntivo",
        title="Concordanza del congiuntivo",
        level="B2",
        category="Congiuntivo",
        summary="Coordinare correttamente i tempi del congiuntivo con la principale.",
        explanation="**Principale al presente:**\n- Contemporaneità: congiuntivo presente. *Penso che sia vero.*\n- Anteriorità: congiuntivo passato. *Penso che sia stato vero.*\n\n**Principale al passato:**\n- Contemporaneità: congiuntivo imperfetto. *Pensavo che fosse vero.*\n- Anteriorità: congiuntivo trapassato. *Pensavo che fosse stato vero.*",
        rules=[
            "Princ. presente + contemporaneità = congiuntivo presente.",
            "Princ. presente + anteriorità = congiuntivo passato.",
            "Princ. passato + contemporaneità = congiuntivo imperfetto.",
            "Princ. passato + anteriorità = congiuntivo trapassato.",
        ],
        examples=[
            GrammarExample(text="Penso che lui dica la verità.", translation=None),
            GrammarExample(
                text="Penso che lui abbia detto la verità.",
                translation=None,
            ),
            GrammarExample(
                text="Pensavo che lui dicesse la verità.",
                translation=None,
            ),
            GrammarExample(
                text="Pensavo che lui avesse detto la verità.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Penso che lui dicano la verità.",
                correct="Penso che lui dica la verità.",
                note="Lui richiede dica, non dicano. Dicesse è possibile per una situazione passata.",
            ),
            GrammarMistake(
                wrong="Pensavo che lui dicessero la verità.",
                correct="Pensavo che lui dicesse la verità.",
                note="Lui richiede dicesse, non dicessero. Il tempo va scelto secondo la prospettiva temporale.",
            ),
        ],
        related=[
            "congiuntivo-presente",
            "congiuntivo-imperfetto",
            "congiuntivo-trapassato",
            "concordanza-tempi",
        ],
    ),
    GrammarTopic(
        slug="andare-gerundio",
        title="Andare + gerundio",
        level="B2",
        category="Tempi verbali",
        summary="Esprimere azioni graduali e progressive con andare + gerundio.",
        explanation="**Andare + gerundio** esprime:\n- Processo graduale: *La situazione va migliorando.*\n- Sviluppo lento: *Va facendo progressi.*\n- Azione continuativa: *Vado dicendo a tutti che...*\n\nDiverso da stare + gerundio (puntuale): sottolinea l'evoluzione nel tempo.",
        structure="andare + gerundio",
        rules=[
            "Andare + gerundio = processo graduale/progressivo.",
            "Sottolinea evoluzione nel tempo.",
            "Diverso da stare + gerundio (più puntuale).",
            "Spesso con verbi di cambiamento.",
        ],
        examples=[
            GrammarExample(text="La situazione va migliorando.", translation=None),
            GrammarExample(text="Il tempo andava peggiorando.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Vado a migliorando.",
                correct="Vado migliorando.",
                note="Andare + gerundio senza preposizione.",
            ),
        ],
        related=["stare-gerundio", "venire-gerundio", "imperfetto"],
    ),
    GrammarTopic(
        slug="venire-gerundio",
        title="Venire + gerundio",
        level="B2",
        category="Tempi verbali",
        summary="Esprimere azioni progressive con enfasi tramite venire + gerundio.",
        explanation="**Venire + gerundio** è simile a stare + gerundio ma con enfasi sul processo.\n- *Ti vengo dicendo da tempo che...* (enfasi)\n- *Vengono arrivando notizie.* (ripetizione)\n\nMeno comune, più formale/letterario.",
        structure="venire + gerundio",
        rules=[
            "Venire + gerundio = azione progressiva con enfasi.",
            "Simile a stare + gerundio ma meno comune.",
            "Uso più formale o letterario.",
            "Sottolinea continuità o ripetizione.",
        ],
        examples=[
            GrammarExample(
                text="Ti vengo dicendo da mesi di fare attenzione.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Vengo a dicendo.",
                correct="Vengo dicendo.",
                note="Venire + gerundio senza preposizione.",
            ),
        ],
        related=["stare-gerundio", "andare-gerundio", "imperfetto"],
    ),
    GrammarTopic(
        slug="connettivi-avanzati",
        title="Connettivi avanzati",
        level="B2",
        category="Avanzato",
        summary="Nondimeno, ciononostante, peraltro, bensì, eppure e altri connettivi complessi.",
        explanation="Connettivi avanzati:\n- **Nondimeno / ciononostante**: tuttavia.\n- **Bensì**: ma piuttosto. *Non è cattivo, bensì timido.*\n- **Eppure**: e tuttavia. *Sembrava facile, eppure ho sbagliato.*\n- **Anzi**: al contrario. *Non è brutto, anzi è bellissimo.*\n- **Ovvero / ossia**: cioè.",
        rules=[
            "Bensì dopo negazione per correggere: non X, bensì Y.",
            "Anzi per rafforzare o correggere.",
            "Eppure per contrasto con aspettativa delusa.",
            "Ovvero/ossia per spiegare o ridefinire.",
        ],
        examples=[
            GrammarExample(
                text="Non è pigro, bensì molto metodico.",
                translation=None,
            ),
            GrammarExample(
                text="Avevo studiato molto, eppure non ho passato l'esame.",
                translation=None,
            ),
            GrammarExample(
                text="Non mi piace, anzi lo detesto.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="È rosso, bensì blu. (si vuole negare che sia rosso)",
                correct="Non è rosso, bensì blu.",
                note="Bensì introduce l'alternativa dopo una negazione. Ma bensì è una combinazione ammessa, anche se spesso basta bensì.",
            ),
        ],
        related=[
            "connettivi-argomentativi",
            "controargomentazione",
            "struttura-argomentativa",
        ],
    ),
    GrammarTopic(
        slug="coesione-testuale",
        title="Coesione testuale",
        level="B2",
        category="Avanzato",
        summary="Strategie per rendere un testo coeso: anafora, catafora, connettivi.",
        explanation="Meccanismi di coesione:\n- **Anafora:** riprendere un elemento. *Marco è arrivato. Lui era stanco.*\n- **Catafora:** anticipare. *Lo vedo che sei triste.*\n- **Ellissi:** omettere elementi recuperabili.\n- **Coesione lessicale:** sinonimi, iperonimi.\n- **Connettivi:** relazioni logiche tra frasi.",
        rules=[
            "Anafora: pronomi, sinonimi per riprendere elementi.",
            "Catafora: anticipare con pronomi o avverbi.",
            "Ellissi: omettere ciò che è recuperabile.",
            "Coesione lessicale: ripetizione, sinonimia, iperonimia.",
        ],
        examples=[
            GrammarExample(
                text="Ho comprato un libro. L'ho letto in due giorni.",
                translation=None,
                note="anafora",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Marco ha comprato un libro. Il quaderno era interessante.",
                correct="Marco ha comprato un libro. Il libro era interessante.",
                note="Mancanza di coesione.",
            ),
        ],
        related=["connettivi-avanzati", "struttura-argomentativa", "sintesi-testuale"],
    ),
    GrammarTopic(
        slug="registro-formale",
        title="Registro formale",
        level="B2",
        category="Avanzato",
        summary="Padroneggiare il registro formale: Lei, congiuntivo, lessico elevato.",
        explanation="Caratteristiche del registro formale:\n- **Pronomi:** Lei di cortesia.\n- **Congiuntivo:** uso rigoroso.\n- **Lessico:** evitare colloquialismi.\n- **Sintassi:** frasi complesse, subordinate implicite.\n- **Fraseologia:** *La ringrazio, Le porgo i miei saluti.*",
        rules=[
            "Usare il Lei con verbo alla 3a singolare.",
            "Congiuntivo obbligatorio nelle subordinate.",
            "Evitare colloquialismi e dislocazioni.",
            "Formule di apertura e chiusura appropriate.",
        ],
        examples=[
            GrammarExample(
                text="La ringrazio per la Sua disponibilita.",
                translation=None,
            ),
            GrammarExample(
                text="Le sarei grato se volesse rispondermi.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ti ringrazio (in mail formale).",
                correct="La ringrazio.",
                note="Contesto formale = Lei, non tu.",
            ),
        ],
        related=["congiuntivo-presente", "pronomi-soggetto", "discorso-indiretto"],
    ),
    GrammarTopic(
        slug="modi-di-dire",
        title="Modi di dire italiani",
        level="B2",
        category="Avanzato",
        summary="Espressioni idiomatiche italiane comuni e il loro significato.",
        explanation="Modi di dire comuni:\n- *In bocca al lupo!* = Buona fortuna!\n- *Acqua in bocca!* = Non dire niente.\n- *Essere al verde* = Non avere soldi.\n- *Non vedere l'ora* = Aspettare con impazienza.\n- *Piovere a catinelle* = Piovere forte.\n- *Avere un chiodo fisso* = Avere un'ossessione.",
        rules=[
            "I modi di dire sono espressioni fisse, non si modificano.",
            "Il significato è metaforico, non letterale.",
            "Variano da regione a regione.",
            "Usarli rende il discorso più naturale.",
        ],
        examples=[
            GrammarExample(text="In bocca al lupo per l'esame!", translation=None),
            GrammarExample(text="Sono al verde questo mese.", translation=None),
            GrammarExample(text="Non vedo l'ora di vederti!", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="In bocca di lupo!",
                correct="In bocca al lupo!",
                note="Espressione fissa: al lupo, non di lupo.",
            ),
        ],
        related=[
            "espressioni-colloquiali",
            "proverbi-italiani",
            "linguaggio-giornalistico",
        ],
    ),
    GrammarTopic(
        slug="espressioni-colloquiali",
        title="Espressioni colloquiali",
        level="B2",
        category="Avanzato",
        summary="Il linguaggio di tutti i giorni: dai, insomma, figurati, magari, boh.",
        explanation="Espressioni tipiche del parlato informale:\n- **Dai!**: suvvia, forza (incoraggiamento o incredulità).\n- **Insomma**: in conclusione.\n- **Figurati!**: non preoccuparti, di niente.\n- **Magari!**: sarebbe bello, lo spero tanto.\n- **Boh!**: non lo so.\n- **Mica**: rafforza la negazione. *Mica male!*\n- **Ci sta**: è accettabile, ha senso.\n- **Va be'**: va bene (rassegnazione).",
        rules=[
            "Usare solo in contesti informali.",
            "Dai può esprimere incoraggiamento o incredulità.",
            "Magari esprime desiderio o possibilità remota.",
            "Mica rafforza la negazione nel parlato.",
        ],
        examples=[
            GrammarExample(text="Dai, andiamo al cinema!", translation=None),
            GrammarExample(
                text="Hai visto la partita? — Magari! Ero al lavoro.",
                translation=None,
            ),
            GrammarExample(
                text="— Grazie mille! — Figurati!",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Figurati! (a un professore)",
                correct="Si figuri! (o: Di niente.)",
                note="Con il Lei formale si usa si figuri.",
            ),
            GrammarMistake(
                wrong="Magari piove. (per dire forse)",
                correct="Forse piove.",
                note="Magari = sarebbe bello se, non = forse.",
            ),
        ],
        related=["modi-di-dire", "registro-formale", "proverbi-italiani"],
    ),
    GrammarTopic(
        slug="proverbi-italiani",
        title="Proverbi italiani",
        level="B2",
        category="Avanzato",
        summary="I proverbi italiani più famosi e il loro significato culturale.",
        explanation="Proverbi celebri:\n- *Chi dorme non piglia pesci.* = L'impegno porta risultati.\n- *Il mattino ha l'oro in bocca.* = Le prime ore sono produttive.\n- *Chi va piano va sano e va lontano.* = Costanza > fretta.\n- *Tra il dire e il fare c'è di mezzo il mare.* = Tra parole e azioni c'è molta differenza.\n- *Non tutto il male viene per nuocere.* = Aspetti positivi dalle avversità.\n- *Meglio tardi che mai.*\n- *Paese che vai, usanza che trovi.*",
        rules=[
            "I proverbi sono espressioni fisse e immutabili.",
            "Spesso contengono rime o assonanze.",
            "Riflettono la cultura e la storia italiana.",
            "Si usano per dare autorevolezza a un discorso.",
        ],
        examples=[
            GrammarExample(
                text="Chi dorme non piglia pesci: alzati presto e mettiti a studiare!",
                translation=None,
            ),
            GrammarExample(
                text="Non preoccuparti: non tutto il male viene per nuocere.",
                translation=None,
            ),
            GrammarExample(
                text="Ho consegnato il progetto in ritardo, ma meglio tardi che mai!",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Chi non dorme piglia pesci.",
                correct="Chi dorme non piglia pesci.",
                note="Il proverbio è fisso.",
            ),
            GrammarMistake(
                wrong="Meglio mai che tardi.",
                correct="Meglio tardi che mai.",
                note="L'ordine è importante nel proverbio.",
            ),
        ],
        related=["modi-di-dire", "espressioni-colloquiali", "italiano-regionale"],
    ),
    GrammarTopic(
        slug="struttura-argomentativa",
        title="Struttura argomentativa",
        level="B2",
        category="Avanzato",
        summary="Costruire un testo argomentativo: tesi, antitesi, prove, conclusione.",
        explanation="Struttura del testo argomentativo:\n1. **Introduzione:** tema e tesi.\n2. **Argomenti a favore:** prove, esempi, dati.\n3. **Antitesi:** obiezioni.\n4. **Confutazione:** rispondere alle obiezioni.\n5. **Conclusione:** riaffermare la tesi.\n\nConnettivi: *innanzitutto, inoltre, infatti, d'altra parte, tuttavia, quindi, in conclusione.*",
        rules=[
            "Tesi chiara all'inizio del testo.",
            "Ogni paragrafo sviluppa un argomento.",
            "Antitesi e confutazione rafforzano la posizione.",
            "Conclusione che riprende la tesi senza ripetere.",
        ],
        examples=[
            GrammarExample(
                text="In questo saggio sosterrò che lo studio delle lingue straniere è fondamentale. Innanzitutto... Inoltre... Tuttavia alcuni obiettano che... Ma queste obiezioni non tengono conto di...",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Tesi confusa o assente all'inizio.",
                correct="Esplicitare la tesi nel primo paragrafo.",
                note="Un testo argomentativo deve far capire subito la posizione dell'autore.",
            ),
            GrammarMistake(
                wrong="Saltare dalla tesi alla conclusione senza argomenti.",
                correct="Sviluppare almeno 2-3 argomenti a favore.",
                note="La parte argomentativa è il cuore del testo.",
            ),
        ],
        related=["controargomentazione", "connettivi-avanzati", "coesione-testuale"],
    ),
    GrammarTopic(
        slug="controargomentazione",
        title="Tecniche di controargomentazione",
        level="B2",
        category="Avanzato",
        summary="Rispondere alle obiezioni in modo strutturato ed efficace.",
        explanation="Tecniche di controargomentazione:\n- **Concessione limitata:** *È vero che... tuttavia...*\n- **Confutazione diretta:** *Si potrebbe obiettare che... ma in realtà...*\n- **Ribaltamento:** *Alcuni dicono che... al contrario...*\n- **Riduzione all'assurdo:** *Se fosse vero che... allora...*\n\nConnettivi: *certamente, è vero che, si potrebbe pensare che, ciononostante.*",
        rules=[
            "Riconoscere il punto di vista avversario.",
            "Usare connettivi concessivi: benché, sebbene, anche se.",
            "Ribattere con argomenti più forti.",
            "Mantenere un tono rispettoso anche nel dissenso.",
        ],
        examples=[
            GrammarExample(
                text="È vero che l'intelligenza artificiale può sostituire alcuni lavori, tuttavia ne creerà di nuovi.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ignorare completamente le obiezioni.",
                correct="Affrontare le obiezioni principali e confutarle.",
                note="Una buona argomentazione considera anche i punti deboli.",
            ),
        ],
        related=["struttura-argomentativa", "connettivi-avanzati", "coesione-testuale"],
    ),
    GrammarTopic(
        slug="sfumature",
        title="Sfumature di significato",
        level="B2",
        category="Avanzato",
        summary="Distinguere sinonimi con sfumature diverse e scegliere la parola giusta.",
        explanation="Sinonimi con sfumature:\n- Vedere / Guardare / Osservare: generico / volontario / attento.\n- Dire / Affermare / Dichiarare: intensita crescente.\n- Contento / Felice / Euforico: intensita crescente.\n- Casa / Abitazione / Dimora: registro crescente.\n- Fare / Realizzare / Effettuare: da generico a formale.",
        rules=[
            "Preferire il termine più preciso al generico.",
            "Adeguare il lessico al registro (formale/informale).",
            "Considerare l'intensita della parola.",
            "Usare il dizionario dei sinonimi per esplorare opzioni.",
        ],
        examples=[
            GrammarExample(
                text="Ho osservato il quadro per ore.",
                translation=None,
                note="osservare = guardare con attenzione",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ho visto il panorama con attenzione.",
                correct="Ho osservato/ammirato il panorama con attenzione.",
                note="Vedere è generico; per attenzione si usa osservare.",
            ),
        ],
        related=["precisione-lessicale", "registro-formale", "campi-semantici"],
    ),
    GrammarTopic(
        slug="tempi-narrativi",
        title="Tempi narrativi",
        level="B2",
        category="Tempi verbali",
        summary="Usare imperfetto, passato remoto e trapassato per narrare eventi.",
        explanation="Nella narrazione letteraria:\n- **Imperfetto:** sfondo, descrizioni. *Era una notte buia.*\n- **Passato remoto:** azioni che avanzano la trama. *Entrò, si guardò intorno.*\n- **Trapassato prossimo:** flashback. *Aveva già deciso di partire.*\n\nL'alternanza crea profondità narrativa.",
        rules=[
            "Imperfetto = sfondo, descrizione, atmosfera.",
            "Passato remoto = azioni principali, avanzamento trama.",
            "Trapassato prossimo = flashback, anteriorità.",
            "Alternare i tempi per creare ritmo narrativo.",
        ],
        examples=[
            GrammarExample(
                text="Era una notte buia e tempestosa. All'improvviso, un lampo illuminò la stanza. Qualcuno era entrato.",
                translation=None,
                note="imperfetto + pass. remoto + trapassato",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Usare solo passato prossimo per narrare.",
                correct="Alternare imperfetto, passato remoto e trapassato.",
                note="Il passato remoto è il tempo della narrazione per eccellenza.",
            ),
        ],
        related=[
            "imperfetto",
            "passato-remoto",
            "trapassato-prossimo",
            "descrizione-letteraria",
        ],
    ),
    GrammarTopic(
        slug="descrizione-letteraria",
        title="Descrizione letteraria",
        level="B2",
        category="Avanzato",
        summary="Tecniche per descrizioni efficaci nella scrittura creativa e letteraria.",
        explanation="Tecniche di descrizione letteraria:\n- **Cinque sensi:** vista, udito, olfatto, tatto, gusto.\n- **Aggettivazione mirata:** pochi aggettivi ma precisi.\n- **Similitudini e metafore:** *Il cielo era come un mare di fuoco.*\n- **Personificazione:** *Il vento sussurrava tra gli alberi.*\n- **Sinestesia:** mescolare i sensi. *Un profumo dolce.*",
        rules=[
            "Coinvolgere tutti e cinque i sensi.",
            "Usare aggettivi specifici, non generici.",
            "Similitudini e metafore per descrizioni vivide.",
            "Mostrare, non dire (show, don't tell).",
        ],
        examples=[
            GrammarExample(
                text="Il sole al tramonto tingeva il cielo di arancione e viola. Un vento tiepido portava il profumo del mare.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Era bello. (descrizione generica)",
                correct="Il panorama era mozzafiato: colline verdi si estendevano a perdita d'occhio.",
                note="Mostrare con dettagli concreti invece di dire solo che è bello.",
            ),
        ],
        related=["tempi-narrativi", "voce-narrativa", "figure-stilistiche"],
    ),
    GrammarTopic(
        slug="passato-remoto",
        title="Passato remoto",
        level="B2",
        category="Tempi verbali",
        summary="Il passato remoto: formazione e uso nella narrazione e nel Sud Italia.",
        explanation="Il **passato remoto** esprime azioni concluse in un passato lontano, senza legami col presente.\n\n**Formazione:**\n- parlare: parlai, parlasti, parlò, parlammo, parlaste, parlarono.\n- leggere: lessi, leggesti, lesse, leggemmo, leggeste, lessero.\n- dormire: dormii, dormisti, dormì, dormimmo, dormiste, dormirono.\n\nMolti verbi hanno il passato remoto irregolare (spesso nella 1a e 3a singolare e 3a plurale).\n\nNell'Italia settentrionale si usa poco, sostituito dal passato prossimo; al Sud e in letteratura è vivo.",
        structure="-are → -ai/-asti/-o/-ammo/-aste/-arono\n-ere → -ei/-esti/-e/-emmo/-este/-erono\n-ire → -ii/-isti/-i/-immo/-iste/-irono",
        rules=[
            "Passato remoto = azione conclusa in passato lontano.",
            "Molti verbi irregolari: essere (fui), avere (ebbi), fare (feci), dire (dissi), scrivere (scrissi).",
            "Uso vivo al Sud; al Nord spesso sostituito dal passato prossimo.",
            "E il tempo narrativo per eccellenza.",
        ],
        examples=[
            GrammarExample(
                text="Dante nacque a Firenze nel 1265.",
                translation=None,
            ),
            GrammarExample(
                text="Lessi quel libro l'estate scorsa. (Sud)",
                translation=None,
            ),
            GrammarExample(
                text="Fecero tutto il possibile per aiutarci.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ieri andiedi al cinema.",
                correct="Ieri andai al cinema. (o: sono andato)",
                note="Andare: passato remoto irregolare → andai.",
            ),
            GrammarMistake(
                wrong="Usare il passato remoto per eventi recenti (al Nord).",
                correct="Preferire il passato prossimo per eventi recenti al Nord.",
                note="Al Nord il passato remoto e sentito come formale/letterario.",
            ),
        ],
        related=[
            "imperfetto",
            "tempi-narrativi",
            "trapassato-prossimo",
            "concordanza-tempi",
        ],
    ),
    GrammarTopic(
        slug="linguaggio-giornalistico",
        title="Linguaggio giornalistico",
        level="B2",
        category="Avanzato",
        summary="Caratteristiche del linguaggio dei giornali italiani.",
        explanation="Il linguaggio giornalistico italiano ha caratteristiche proprie:\n- **Titoli:** spesso senza articolo, con ellissi verbale. *Governo in crisi, elezioni anticipate.*\n- **Stile nominale:** *Allarme rosso per l'economia.*\n- **Participi assoluti:** *Concluso il vertice, il premier ha parlato.*\n- **Lessico tecnico-politico:** *vertice, crisi, manovra, decreto.*\n- **Neologismi e anglicismi:** *spread, spending review, Jobs Act.*\n- **Ripetizioni evitare:** ampio uso di sinonimi e perifrasi.",
        rules=[
            "Titoli stringati, spesso senza verbo o articolo.",
            "Stile nominale: sostantivi invece di verbi.",
            "Participi assoluti per esprimere anteriorità.",
            "Lessico specifico del settore trattato.",
        ],
        examples=[
            GrammarExample(
                text="Crisi di governo: il Presidente sale al Quirinale.",
                translation=None,
            ),
            GrammarExample(
                text="Firmato l'accordo, le parti hanno rilasciato dichiarazioni.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Usare linguaggio colloquiale in un articolo formale.",
                correct="Mantenere un registro formale e oggettivo.",
                note="Il giornalismo richiede un registro più elevato.",
            ),
        ],
        related=["titoli", "registro-formale", "discorso-riportato"],
    ),
    GrammarTopic(
        slug="titoli",
        title="Titoli giornalistici",
        level="B2",
        category="Avanzato",
        summary="Come sono costruiti i titoli nei giornali italiani.",
        explanation="I titoli giornalistici italiani seguono regole precise:\n- **Ellissi dell'articolo:** *Borsa in rialzo* (non: La borsa in rialzo).\n- **Presente storico:** *Crolla il governo.*\n- **Stile nominale:** *Paura per il terremoto.*\n- **Ellissi verbale:** *Scontri a Roma.*\n\nI titoli a effetto usano anche metafore, giochi di parole e riferimenti culturali.",
        rules=[
            "Spesso senza articolo iniziale.",
            "Presente storico per eventi passati.",
            "Stile nominale senza verbo.",
            "Metafore e giochi di parole per attirare l'attenzione.",
        ],
        examples=[
            GrammarExample(
                text="Crolla la Borsa: persi 50 miliardi.",
                translation=None,
            ),
            GrammarExample(
                text="Mafia, maxi-operazione: 50 arresti.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Titolo troppo lungo e descrittivo.",
                correct="Titolo breve, incisivo, spesso senza verbo o articolo.",
                note="I titoli italiani sono stringati e d'effetto.",
            ),
        ],
        related=["linguaggio-giornalistico", "discorso-riportato", "registro-formale"],
    ),
    GrammarTopic(
        slug="discorso-riportato",
        title="Discorso riportato nei media",
        level="B2",
        category="Discorso indiretto",
        summary="Come i media italiani riportano le dichiarazioni altrui.",
        explanation="Il discorso riportato nei media:\n- **Condizionale di dissociazione:** il giornalista prende le distanze. *Il ministro avrebbe dichiarato...*\n- **Virgolettato:** citazione diretta.\n- **Discorso indiretto libero:** mescola diretto e indiretto.\n\nIl condizionale di dissociazione e tipico: segnala che la notizia non è confermata.",
        rules=[
            "Condizionale di dissociazione per notizie non confermate.",
            "Virgolettato per citazioni testuali.",
            "Indiretto libero per fluidità narrativa.",
            "Verbi dichiarativi: affermare, dichiarare, sostenere, riferire.",
        ],
        examples=[
            GrammarExample(
                text="Secondo fonti vicine al governo, il premier si dimetterebbe entro domani.",
                translation=None,
                note="condizionale di dissociazione",
            ),
            GrammarExample(
                text='"Non abbiamo nulla da nascondere", ha dichiarato il portavoce.',
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Il ministro ha detto che si dimettera. (senza fonte certa)",
                correct="Il ministro si dimetterebbe. (condizionale di dissociazione)",
                note="Se la notizia non è confermata, si usa il condizionale.",
            ),
        ],
        related=[
            "linguaggio-giornalistico",
            "titoli",
            "discorso-indiretto",
            "condizionale-presente",
        ],
    ),
]
