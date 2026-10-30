"""Italian grammar topics — C2."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="ripasso-congiuntivo",
        title="Ripasso avanzato del congiuntivo",
        level="C2",
        category="Congiuntivo",
        summary="Dominio completo del congiuntivo in tutti i contesti e registri.",
        explanation="A livello C2 il congiuntivo deve essere usato con sicurezza in ogni contesto:\n- Concordanze complesse.\n- Congiuntivo indipendente (augurativo, esortativo, dubitativo).\n- Sfumature tra indicativo e congiuntivo dove entrambi sono possibili.\n- Uso letterario e arcaico del congiuntivo.\n\n*Che la festa abbia inizio!* (esortativo)\n*Non so se sia il caso.* (dubitativo)",
        rules=[
            "Congiuntivo in frasi indipendenti: Che tu sia maledetto!",
            "Scelta tra indicativo/congiuntivo con verbi come immaginare, sospettare.",
            "Congiuntivo nelle comparative ipotetiche: Come se fosse...",
            "Uso del congiuntivo nella prosa letteraria contemporanea.",
        ],
        examples=[
            GrammarExample(
                text="Che la forza sia con te!",
                translation=None,
                note="ottativo/desiderativo",
            ),
            GrammarExample(
                text="Non sapevo che avesse già pubblicato tre romanzi.",
                translation=None,
            ),
            GrammarExample(
                text="Comportati come se niente fosse successo.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Evitare sempre il congiuntivo nel parlato.",
                correct="Usare il congiuntivo con naturalezza, anche nel parlato informale dove appropriato.",
                note="Il vero C2 usa il congiuntivo senza sforzo, non lo evita.",
            ),
        ],
        related=[
            "congiuntivo-presente",
            "congiuntivo-imperfetto",
            "congiuntivo-trapassato",
            "concordanza-congiuntivo",
        ],
    ),
    GrammarTopic(
        slug="ripasso-condizionale",
        title="Ripasso avanzato del condizionale",
        level="C2",
        category="Condizionali",
        summary="Uso avanzato del condizionale: dissociazione, futuro nel passato, cortesia.",
        explanation="Usi avanzati del condizionale:\n- **Dissociazione giornalistica:** *Il premier si dimetterebbe.*\n- **Futuro nel passato:** *Disse che sarebbe venuto.*\n- **Cortesia estrema:** *Le sarei immensamente grato se volesse...*\n- **Condizionale di modestia:** *Direi che...*\n- **Ipotesi non realizzata:** *Avrei voluto dirtelo prima.*",
        rules=[
            "Condizionale composto per azioni non realizzate nel passato.",
            "Condizionale di dissociazione solo in contesti formali/giornalistici.",
            "Il condizionale passato presenta il futuro da una prospettiva passata; un futuro ancora attuale può restare al futuro semplice.",
            "Sfumature tra condizionale e congiuntivo nelle ipotetiche.",
        ],
        examples=[
            GrammarExample(
                text="Secondo indiscrezioni, il ministro rassegnerebbe le dimissioni.",
                translation=None,
                note="dissociazione",
            ),
            GrammarExample(
                text="Avrei tanto voluto conoscerti prima.",
                translation=None,
                note="desiderio irrealizzato",
            ),
            GrammarExample(
                text="Promisero che avrebbero fatto tutto il possibile.",
                translation=None,
                note="futuro nel passato",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ha detto che sarebbe venire.",
                correct="Ha detto che sarebbe venuto.",
                note="Il condizionale passato richiede il participio. Ha detto che verrà è corretto se l'arrivo è ancora futuro.",
            ),
            GrammarMistake(
                wrong="Maria sarebbe dovuto andare.",
                correct="Maria sarebbe dovuta andare.",
                note="Concordanza del participio con il soggetto.",
            ),
        ],
        related=[
            "condizionale-presente",
            "condizionale-cortesia",
            "discorso-riportato",
        ],
    ),
    GrammarTopic(
        slug="concordanza-di-genere",
        title="Concordanza avanzata di genere e numero",
        level="C2",
        category="Avanzato",
        summary="Padroneggiare casi complessi di concordanza in italiano.",
        explanation="Casi complessi di concordanza:\n- **Plurali doppi:** *il braccio → i bracci / le braccia* (significato diverso).\n- **Accordo a senso:** *La maggior parte degli studenti sono arrivati.*\n- **Plurali di nomi composti:** *il capostazione → i capistazione.*\n- **Participio con verbi servili:** *Non ho potuto andarci / Non sono potuto andarci.*\n- **Accordo del participio con ne:** *Ne ho comprate tre.*",
        rules=[
            "Plurali doppi: il muro (i muri / le mura).",
            "Accordo a senso: la maggior parte + plurale.",
            "Plurale dei nomi composti: capo- + -stazione → capistazione.",
            "Con verbi servili + essere: sono dovuto/a andare.",
        ],
        examples=[
            GrammarExample(
                text="Le mura della città sono antiche. (mura = mura difensive)",
                translation=None,
                note="mura vs muri",
            ),
            GrammarExample(
                text="La maggior parte degli invitati erano contenti. (accordo a senso)",
                translation=None,
                note="accordo a senso",
            ),
            GrammarExample(
                text="Non sono potuta venire ieri. (femminile)",
                translation=None,
                note="accordo con essere",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="I muri della città.",
                correct="Le mura della città.",
                note="Mura = mura difensive/di cinta; muri = pareti.",
            ),
            GrammarMistake(
                wrong="Non ho potuta andare.",
                correct="Non sono potuta andare.",
                note="Con verbi che richiedono essere all'infinito, il servile prende essere.",
            ),
        ],
        related=["genere-nomi", "passato-prossimo-essere", "concordanza-tempi"],
    ),
    GrammarTopic(
        slug="stile-letterario",
        title="Stile letterario",
        level="C2",
        category="Avanzato",
        summary="Analizzare e riprodurre lo stile letterario italiano classico e moderno.",
        explanation="Lo stile letterario italiano si caratterizza per:\n- **Ipotassi:** frasi lunghe con molte subordinate.\n- **Lessico ricercato:** arcaismi, latinismi, termini rari.\n- **Figure retoriche:** metafore, similitudini, anafore.\n- **Ritmo e musicalità:** attenzione alla sonorita delle parole.\n\nAutori di riferimento: Dante, Boccaccio, Manzoni, Calvino, Eco.",
        rules=[
            "Ipotassi: uso esteso di subordinate implicite ed esplicite.",
            "Lessico elevato e preciso.",
            "Attenzione al ritmo e alla cadenza della frase.",
            "Variatio: variare strutture per evitare monotonia.",
        ],
        examples=[
            GrammarExample(
                text="Ed ecco, quasi al cominciar de l'erta, una lonza leggera e presta molto, che di pel macolato era coverta. (Dante)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Scrivere in modo artificiosamente complesso.",
                correct="La complessità deve essere al servizio del significato, non fine a se stessa.",
                note="Lo stile elevato non è accumulo di parole difficili.",
            ),
        ],
        related=["voce-narrativa", "figure-stilistiche", "tempi-narrativi"],
    ),
    GrammarTopic(
        slug="voce-narrativa",
        title="Voce narrativa",
        level="C2",
        category="Avanzato",
        summary="Sviluppare una voce narrativa personale in italiano.",
        explanation="La voce narrativa e la personalita che emerge dal testo.\n\nElementi:\n- **Punto di vista:** prima persona (io narrante), terza persona (onnisciente o limitato).\n- **Tono:** ironico, serio, malinconico, distaccato.\n- **Distanza:** vicinanza emotiva o distacco critico.\n- **Registro:** formale, colloquiale, lirico.\n\nSviluppare una voce propria richiede lettura, pratica e consapevolezza stilistica.",
        rules=[
            "Scegliere un punto di vista coerente.",
            "Mantenere tono e registro uniformi.",
            "La voce narrativa riflette la personalita dell'autore.",
            "Leggere molto per sviluppare orecchio stilistico.",
        ],
        examples=[
            GrammarExample(
                text="Non so perché quel giorno decisi di prendere il treno invece dell'autobus. Forse fu il cielo grigio, forse la voglia di cambiare qualcosa, qualsiasi cosa.",
                translation=None,
                note="prima persona, tono riflessivo",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Cambiare punto di vista all'interno dello stesso testo.",
                correct="Mantenere coerenza nel punto di vista scelto.",
                note="Salti di punto di vista confondono il lettore.",
            ),
        ],
        related=["stile-letterario", "descrizione-letteraria", "tempi-narrativi"],
    ),
    GrammarTopic(
        slug="figure-stilistiche",
        title="Figure stilistiche avanzate",
        level="C2",
        category="Avanzato",
        summary="Anafora, epifora, chiasmo, climax, anticlimax e altre figure di stile.",
        explanation="Figure stilistiche per la scrittura avanzata:\n- **Anafora:** ripetere all'inizio. *Senza di te... Senza di te...*\n- **Epifora:** ripetere alla fine.\n- **Chiasmo:** incrocio. *Mangio per vivere, non vivo per mangiare.*\n- **Climax:** crescendo. *Spero, credo, so.*\n- **Anticlimax:** decrescendo.\n- **Asindeto:** senza congiunzioni. *Veni, vidi, vici.*\n- **Polisindeto:** con molte congiunzioni. *E mangio e bevo e dormo.*",
        rules=[
            "Anafora enfatizza un concetto ripetendolo.",
            "Chiasmo crea simmetria e contrasto.",
            "Climax/anticlimax creano tensione.",
            "Usare con moderazione per non appesantire.",
        ],
        examples=[
            GrammarExample(
                text="Non chiedermi di restare. Non chiedermi di capire. Non chiedermi niente.",
                translation=None,
                note="anafora",
            ),
            GrammarExample(
                text="Veni, vidi, vici. (asindeto)",
                translation=None,
                note="asindeto",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Abusare delle figure retoriche.",
                correct="Usare le figure con parsimonia per creare effetto.",
                note="Troppe figure retoriche rendono il testo artificioso.",
            ),
        ],
        related=["figure-retoriche", "stile-letterario", "voce-narrativa"],
    ),
    GrammarTopic(
        slug="equivalenza",
        title="Equivalenza traduttiva",
        level="C2",
        category="Avanzato",
        summary="Strategie per tradurre mantenendo significato, tono e stile dell'originale.",
        explanation="Principi di equivalenza traduttiva:\n- **Equivalenza semantica:** mantenere il significato esatto.\n- **Equivalenza pragmatica:** stesso effetto sul destinatario.\n- **Equivalenza stilistica:** stesso registro e tono.\n\nStrategie:\n- **Traduzione letterale:** quando possibile.\n- **Adattamento:** quando il concetto non esiste.\n- **Compensazione:** perdere una sfumatura qui, recuperarla li.",
        rules=[
            "Fedelta al significato dell'originale.",
            "Naturalezza nella lingua di arrivo.",
            "Adattare riferimenti culturali quando necessario.",
            "La traduzione perfetta spesso non esiste: scegliere la soluzione migliore.",
        ],
        examples=[
            GrammarExample(
                text="EN: It's raining cats and dogs. IT: Piove a catinelle. (non: Piovono cani e gatti)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Tradurre letteralmente espressioni idiomatiche.",
                correct="Cercare l'equivalente idiomatico nella lingua d'arrivo.",
                note="Le espressioni idiomatiche raramente si traducono parola per parola.",
            ),
        ],
        related=["sfumature-traduzione", "falsi-amici", "precisione-lessicale"],
    ),
    GrammarTopic(
        slug="sfumature-traduzione",
        title="Sfumature nella traduzione",
        level="C2",
        category="Avanzato",
        summary="Cogliere e rendere le sfumature di significato nel passaggio tra lingue.",
        explanation="Sfumature critiche nella traduzione IT-EN:\n- **Tu vs Lei vs Voi:** in inglese sempre you.\n- **Passato prossimo vs remoto:** entrambi simple past/present perfect.\n- **Congiuntivo:** spesso perso in inglese.\n- **Diminutivi/accrescitivi:** -ino, -one non hanno equivalenti fissi.\n- **Regionali e dialettali:** difficili da rendere.",
        rules=[
            "Il congiuntivo italiano spesso non ha equivalente inglese.",
            "Diminutivi e accrescitivi richiedono perifrasi.",
            "Lei di cortesia: in inglese si perde la distinzione formale/informale.",
            "Il passato remoto letterario può essere reso con il simple past.",
        ],
        examples=[
            GrammarExample(
                text="IT: Ti presento la mia sorellina. EN: I'd like you to meet my little sister.",
                translation=None,
                note="-ina → little",
            ),
            GrammarExample(
                text="IT: Penso che sia vero. EN: I think it's true. (congiuntivo perso)",
                translation=None,
                note="congiuntivo -> indicativo",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Tradurre ogni parola senza considerare la perdita di sfumature.",
                correct="Compensare le perdite con altre strategie traduttive.",
                note="La traduzione e sempre un compromesso.",
            ),
        ],
        related=["equivalenza", "falsi-amici", "congiuntivo-presente"],
    ),
    GrammarTopic(
        slug="falsi-amici",
        title="Falsi amici italiano-inglese",
        level="C2",
        category="Avanzato",
        summary="Parole simili ma con significato diverso tra italiano e inglese.",
        explanation="Falsi amici comuni:\n- **Actually** ≠ attualmente (attualmente = currently).\n- **Sensible** ≠ sensibile (sensibile = sensitive; sensato = sensible).\n- **Library** ≠ libreria (libreria = bookstore; biblioteca = library).\n- **Parents** ≠ parenti (parenti = relatives; genitori = parents).\n- **Education** ≠ educazione (educazione = manners; istruzione = education).\n- **Firm** ≠ firma (firma = signature; azienda = firm).",
        rules=[
            "Verificare sempre il significato di parole simili.",
            "Attenzione ai falsi amici in contesti professionali.",
            "Molti falsi amici derivano da evoluzioni divergenti dal latino.",
            "Lista sempre aggiornata di falsi amici da consultare.",
        ],
        examples=[
            GrammarExample(
                text="Actually, I disagree. ≠ Attualmente, non sono d'accordo. (SBAGLIATO: significa In realtà, non sono d'accordo.)",
                translation=None,
                note="actually ≠ attualmente",
            ),
            GrammarExample(
                text="She is very sensible. ≠ Lei e molto sensibile. (SBAGLIATO: significa Lei e molto ragionevole.)",
                translation=None,
                note="sensible ≠ sensibile",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Tradurre attualmente con actually.",
                correct="Attualmente = currently; actually = in realtà.",
                note="Uno dei falsi amici più comuni e pericolosi.",
            ),
        ],
        related=["sfumature-traduzione", "equivalenza", "precisione-lessicale"],
    ),
    GrammarTopic(
        slug="evoluzione-linguistica",
        title="Evoluzione della lingua italiana",
        level="C2",
        category="Avanzato",
        summary="Come l'italiano e cambiato dal latino a oggi.",
        explanation="Tappe dell'evoluzione:\n- **Latino volgare (I-IX sec):** dal latino classico alle lingue romanze.\n- **Primi documenti (IX-X sec):** Placito Capuano (960) primo documento in volgare.\n- **Dante e il Trecento:** il fiorentino diventa modello letterario.\n- **Questione della lingua (XVI sec):** Bembo codifica il modello petrarchesco-boccacciano.\n- **Manzoni e i Promessi Sposi:** avvicina la lingua scritta al parlato fiorentino.\n- **Italiano moderno:** TV, media, diffusione dell'italiano standard.",
        rules=[
            "L'italiano deriva dal latino volgare, non da quello classico.",
            "Il fiorentino del Trecento e la base dell'italiano standard.",
            "La lingua letteraria ha influenzato fortemente la lingua parlata.",
            "L'italiano e in continua evoluzione (neostandard, anglicismi).",
        ],
        examples=[
            GrammarExample(
                text="Latino: Illa mulier pulchra est. Italiano: Quella donna e bella.",
                translation=None,
                note="evoluzione dal latino all'italiano",
            ),
            GrammarExample(
                text="Dai Promessi Sposi: Quel ramo del lago di Como... (incipit celebre)",
                translation=None,
                note="L'italiano manzoniano",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Pensare che l'italiano sia sempre stato uguale.",
                correct="Conoscere le tappe principali dell'evoluzione linguistica.",
                note="La lingua e un organismo vivo in costante cambiamento.",
            ),
        ],
        related=["latinismi", "prestiti-linguistici", "italiano-standard"],
    ),
    GrammarTopic(
        slug="latinismi",
        title="Latinismi nella lingua italiana",
        level="C2",
        category="Avanzato",
        summary="Parole ed espressioni latine ancora vive nell'italiano colto.",
        explanation="Latinismi comuni:\n- **Ex aequo:** a pari merito.\n- **Sui generis:** del suo genere, unico.\n- **Curriculum vitae:** percorso di vita (CV).\n- **Ad hoc:** per questo scopo.\n- **In extremis:** all'ultimo momento.\n- **Una tantum:** una volta soltanto.\n- **Pro capite:** a persona.\n- **Conditio sine qua non:** condizione indispensabile.\n- **De facto:** di fatto.\n- **Iter:** procedura, percorso.",
        rules=[
            "I latinismi sono usati nel linguaggio colto e formale.",
            "Molti latinismi sono nel linguaggio giuridico e burocratico.",
            "Attenzione alla pronuncia: in italiano si pronunciano all'italiana.",
            "Alcuni latinismi suonano antiquati o pretenziosi se abusati.",
        ],
        examples=[
            GrammarExample(
                text="Il candidato e stato assunto dopo un lungo iter burocratico.",
                translation=None,
                note="iter = procedura",
            ),
            GrammarExample(
                text="La riunione e stata aggiornata ad hoc per discutere l'emergenza.",
                translation=None,
                note="ad hoc = appositamente",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Pronunciare i latinismi alla latina (specie in contesti italiani).",
                correct="In italiano i latinismi si pronunciano secondo la fonetica italiana.",
                note="Curriculum vitae in italiano corrente si pronuncia in genere con fonetica italianizzata: /kurriˈkulum ˈviːtae/.",
            ),
        ],
        related=["prestiti-linguistici", "evoluzione-linguistica", "registro-formale"],
    ),
    GrammarTopic(
        slug="prestiti-linguistici",
        title="Prestiti linguistici e anglicismi",
        level="C2",
        category="Avanzato",
        summary="L'influenza di altre lingue sull'italiano contemporaneo.",
        explanation="Prestiti in italiano:\n- **Francese:** garage, menù, blu, peluche, cabaret.\n- **Spagnolo:** flamenco, siesta, fiesta, tango.\n- **Arabo:** algebra, algoritmo, zucchero, arancia.\n- **Tedesco:** kitsch, kaputt, strudel.\n- **Giapponese:** sushi, origami, tsunami.\n\n**Anglicismi moderni:** computer, mouse, smartphone, social media, meeting, deadline.\n\nL'Accademia della Crusca cerca di proporre alternative italiane, non sempre con successo.",
        rules=[
            "I prestiti antichi sono integrati (zucchero).",
            "I prestiti moderni spesso restano invariati (computer).",
            "Alcuni prestiti sviluppano significati diversi in italiano.",
            "L'italiano ha sempre assorbito parole da altre lingue.",
        ],
        examples=[
            GrammarExample(
                text="Ho comprato un computer nuovo. (nessun equivalente italiano accettato)",
                translation=None,
                note="anglicismo",
            ),
            GrammarExample(
                text="Lo zucchero viene dall'arabo sukkar.",
                translation=None,
                note="prestito arabo antico",
            ),
            GrammarExample(
                text="C'e chi dice smart working e chi dice lavoro agile.",
                translation=None,
                note="anglicismo vs alternativa italiana",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Usare anglicismi inutili quando esiste un equivalente italiano preciso.",
                correct="Preferire l'equivalente italiano se disponibile e naturale.",
                note="Non tutti gli anglicismi sono necessari.",
            ),
        ],
        related=["latinismi", "evoluzione-linguistica", "italiano-standard"],
    ),
    GrammarTopic(
        slug="generi-testuali",
        title="Generi testuali",
        level="C2",
        category="Avanzato",
        summary="Padroneggiare diversi generi testuali: saggio, relazione, articolo, recensione.",
        explanation="Principali generi testuali:\n- **Saggio argomentativo:** tesi, argomenti, conclusione.\n- **Relazione tecnica:** dati, analisi, raccomandazioni.\n- **Articolo di opinione:** punto di vista personale, stile brillante.\n- **Recensione:** descrizione, valutazione, consiglio.\n- **Lettera formale:** formule standard, registro elevato.\n- **Racconto breve:** narrativa, descrizione, dialogo.",
        rules=[
            "Ogni genere ha convenzioni specifiche.",
            "Il registro varia a seconda del genere e del pubblico.",
            "La struttura e parte integrante del genere.",
            "Leggere esempi del genere prima di scrivere.",
        ],
        examples=[
            GrammarExample(
                text="Saggio: In questo saggio si intende dimostrare che... Relazione: Dati alla mano, si evince che... Recensione: L'ultimo film di Sorrentino e un capolavoro visivo...",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mescolare le convenzioni di generi diversi.",
                correct="Rispettare le caratteristiche specifiche di ogni genere.",
                note="Una relazione tecnica non è un saggio personale.",
            ),
        ],
        related=["struttura-argomentativa", "registro-formale", "sintesi-testuale"],
    ),
    GrammarTopic(
        slug="creativita-linguistica",
        title="Creativita linguistica",
        level="C2",
        category="Avanzato",
        summary="Giocare con la lingua: neologismi, metafore originali, invenzioni lessicali.",
        explanation="La creativita linguistica a livello C2:\n- **Neologismi:** creare parole nuove per concetti nuovi.\n- **Metafore originali:** non quelle cristallizzate, ma immagini nuove.\n- **Giochi di parole consapevoli:** calembour, doppi sensi.\n- **Scrittura creativa:** rompere le regole dopo averle padroneggiate.\n\nEsempi di creativita: *petaloso* (neologismo di un bambino, entrato nei dizionari); *buonista* (dispregiativo moderno).",
        rules=[
            "La creativita funziona quando le regole sono già padroneggiate.",
            "I neologismi efficaci colgono un bisogno espressivo reale.",
            "Le metafore fresche sorprendono e illuminano.",
            "La lingua e plastica: le regole descrivono, non prescrivono.",
        ],
        examples=[
            GrammarExample(
                text="Era un tramonto petaloso, di quelli che ti restano negli occhi per giorni.",
                translation=None,
                note="neologismo",
            ),
            GrammarExample(
                text="Le sue parole erano coltelli di vetro: trasparenti, affilati, invisibili fino al colpo.",
                translation=None,
                note="metafora originale",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Creare neologismi senza conoscere le regole di formazione delle parole.",
                correct="I neologismi devono rispettare la morfologia italiana per essere accettati.",
                note="La creativita e libertà nella regola, non ignoranza della regola.",
            ),
        ],
        related=["derivazione", "precisione-lessicale", "stile-letterario"],
    ),
    GrammarTopic(
        slug="editing",
        title="Editing e revisione testuale",
        level="C2",
        category="Avanzato",
        summary="Tecniche per revisionare e migliorare testi propri e altrui.",
        explanation="Processo di editing professionale:\n1. **Revisione strutturale:** organizzazione, flusso logico.\n2. **Revisione stilistica:** tono, registro, chiarezza.\n3. **Revisione linguistica:** grammatica, sintassi, ortografia.\n4. **Editing finale:** refusi, formattazione.\n\nTecniche:\n- Leggere ad alta voce.\n- Distanziamento temporale prima di rileggere.\n- Checklist di controllo.\n- Editing a strati (un aspetto alla volta).",
        rules=[
            "Editing strutturale prima di quello linguistico.",
            "Leggere ad alta voce rivela problemi di ritmo.",
            "Prendere distanza dal testo prima di revisionarlo.",
            "Un buon editing migliora senza stravolgere la voce dell'autore.",
        ],
        examples=[
            GrammarExample(
                text="Prima: L'azienda ha fatto un sacco di cose per migliorare la situazione. Dopo: L'azienda ha implementato diverse strategie per ottimizzare i processi interni.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Limitarsi alla correzione dei refusi.",
                correct="Revisionare a tutti i livelli: struttura, stile, lingua.",
                note="L'editing efficace va oltre la grammatica.",
            ),
        ],
        related=["sintesi-testuale", "riformulazione", "precisione-lessicale"],
    ),
    GrammarTopic(
        slug="espressione-sfumata",
        title="Espressione sfumata e diplomatica",
        level="C2",
        category="Avanzato",
        summary="Esprimersi con sfumature e diplomazia nel discorso professionale e sociale.",
        explanation="Tecniche di espressione sfumata:\n- **Attenuatori:** *forse, magari, un po', piuttosto, alquanto.*\n- **Condizionale di cortesia:** *Vorrei, potrei, mi piacerebbe.*\n- **Domande invece di affermazioni:** *Non crede che...?*\n- **Understatement:** *Non è il massimo* (invece di *e orribile*).\n- **Formule di cautela:** *A mio modesto parere, se non sbaglio, mi sembra che.*",
        rules=[
            "Attenuare affermazioni categoriche.",
            "Preferire domande a imposizioni.",
            "Riconoscere punti di vista diversi: Capisco la sua posizione, tuttavia...",
            "Il linguaggio diplomatico evita conflitti e mantiene relazioni.",
        ],
        examples=[
            GrammarExample(
                text="Mi sembra che forse ci sia un piccolo margine di miglioramento in questa sezione.",
                translation=None,
                note="attenuazione diplomatica",
            ),
            GrammarExample(
                text="Non è esattamente quello che avevamo in mente. (invece di: E completamente sbagliato.)",
                translation=None,
                note="understatement",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Questo e inaccettabile! (in contesto professionale)",
                correct="Ho alcune perplessita su questo aspetto. Potremmo valutare delle alternative?",
                note="La diplomazia preserva la relazione professionale.",
            ),
        ],
        related=["critica-costruttiva", "registro-formale", "condizionale-cortesia"],
    ),
    GrammarTopic(
        slug="integrazione-grammaticale",
        title="Integrazione grammaticale completa",
        level="C2",
        category="Avanzato",
        summary="Usare simultaneamente tutte le strutture grammaticali con fluidità e precisione.",
        explanation="A livello C2 tutte le strutture grammaticali devono integrarsi naturalmente:\n- Congiuntivo + condizionale + periodo ipotetico.\n- Subordinate implicite ed esplicite alternate.\n- Pronomi combinati in contesti complessi.\n- Dislocazioni e frasi marcate con consapevolezza.\n- Passaggio fluido tra registri.\n\nL'obiettivo è usare la grammatica con precisione e flessibilità per esprimere significati complessi, senza dover imitare l'identità linguistica di un madrelingua.",
        rules=[
            "Alternare strutture semplici e complesse per il ritmo.",
            "Usare il congiuntivo senza pensarci.",
            "Scegliere il registro appropriato al contesto.",
            "La grammatica e al servizio dell'espressione, non viceversa.",
        ],
        examples=[
            GrammarExample(
                text="Se avessi saputo che sarebbe stato così difficile, ci avrei pensato due volte prima di accettare, ma ormai quel che è fatto è fatto.",
                translation=None,
                note="periodo ipotetico 3 tipo + connettivo",
            ),
            GrammarExample(
                text="Benché non condivida pienamente la sua posizione, devo ammettere che le sue argomentazioni, per quanto provocatorie, non sono prive di fondamento.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Evitare strutture complesse per paura dell'errore.",
                correct="Usare strutture complesse con sicurezza, accettando che l'errore occasionale e normale.",
                note="La fluidità C2 non significa perfezione assoluta, ma naturalezza.",
            ),
        ],
        related=["fluidita-nativa", "ripasso-congiuntivo", "ripasso-condizionale"],
    ),
    GrammarTopic(
        slug="fluidita-nativa",
        title="Fluidità e autonomia avanzate",
        level="C2",
        category="Avanzato",
        summary="Comunicare con precisione, flessibilità e autonomia in situazioni complesse.",
        explanation="A livello C2 si comprendono significati impliciti, si riformula con precisione e si adatta il registro al contesto. Ritmo, pause e intonazione sostengono l'intelligibilità.\n\nNon è necessario perdere il proprio accento o diventare indistinguibili da un madrelingua. Lettura, ascolto e pratica costante sviluppano autonomia, competenza pragmatica e flessibilità espressiva.",
        rules=[
            "Immersione: vivere la lingua, non solo studiarla.",
            "Leggere di tutto: giornali, romanzi, saggistica.",
            "Parlare con madrelingua di argomenti vari.",
            "Accettare che ci sara sempre qualcosa da imparare.",
        ],
        examples=[
            GrammarExample(
                text="Mah, insomma, non è che mi entusiasmi l'idea, pero tutto sommato si potrebbe anche fare, dai.",
                translation=None,
                note="parlato naturale con segnali discorsivi",
            ),
            GrammarExample(
                text="Certe volte basta uno sguardo per capirsi, senza bisogno di tante parole.",
                translation=None,
                note="fluidità espressiva",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Cercare la perfezione assoluta.",
                correct="Cercare la naturalezza: anche i madrelingua fanno errori nel parlato.",
                note="La fluidità e comunicazione efficace, non perfezione grammaticale.",
            ),
        ],
        related=[
            "integrazione-grammaticale",
            "espressione-sfumata",
            "italiano-standard",
        ],
    ),
    GrammarTopic(
        slug="revisione",
        title="Revisione e auto-editing avanzato",
        level="C2",
        category="Avanzato",
        summary="Tecniche di revisione critica del proprio testo per raggiungere la massima qualità espressiva.",
        explanation="La **revisione** a livello C2 va oltre la correzione di errori grammaticali: implica un'analisi critica della chiarezza, coerenza, stile e appropriatezza del testo.\n\n**Fasi della revisione:**\n1. **Contenuto**: il messaggio è chiaro? Le argomentazioni sono complete e ben strutturate?\n2. **Coesione e coerenza**: i connettori logici guidano il lettore? Ogni paragrafo ha un'unità tematica?\n3. **Registro e stile**: il tono è appropriato al contesto? Le scelte lessicali sono precise?\n4. **Grammatica e sintassi**: concordanze, consecutio temporum, preposizioni, articoli.\n5. **Leggibilità**: frasi troppo lunghe? Varietà nella struttura sintattica?\n\n**Tecniche pratiche:**\n- Leggere ad alta voce per individuare problemi di ritmo.\n- Distanziarsi dal testo (lasciarlo riposare alcune ore o giorni).\n- Chiedere un feedback esterno.\n- Revisione a strati: un passaggio per ogni aspetto (contenuto, stile, grammatica).",
        rules=[
            "Revisione a strati: contenuto → coesione → stile → grammatica → leggibilità.",
            "Leggere ad alta voce per testare il ritmo del testo.",
            "Distanziarsi dal testo prima della revisione finale.",
            "Verificare la varietà sintattica: alternare frasi brevi e lunghe.",
            "Controllare che ogni capoverso abbia un'unica idea principale.",
        ],
        examples=[
            GrammarExample(
                text="Prima della revisione: Il progetto è importante. Avrà un impatto. Dobbiamo considerare molti fattori.",
                translation=None,
                note="Da frasi telegrafiche a un unico periodo coeso.",
            ),
            GrammarExample(
                text="Prima: La ricerca ha dimostrato che la gente mangia troppi zuccheri.",
                translation=None,
                note="Registro accademico e precisione lessicale.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Revisionare tutto in un unico passaggio.",
                correct="Fare più passaggi, ciascuno focalizzato su un aspetto specifico.",
                note="La revisione è un processo stratificato.",
            ),
            GrammarMistake(
                wrong="Non eliminare ridondanze per paura di perdere contenuto.",
                correct="Ogni parola deve giustificare la propria presenza.",
                note="Concisione.",
            ),
        ],
        related=[
            "riformulazione",
            "sintesi-testuale",
            "precisione-lessicale",
            "generi-testuali",
        ],
    ),
    GrammarTopic(
        slug="italofonia-contemporanea",
        title="L'italofonia contemporanea",
        level="C2",
        category="Espressione",
        summary="Istituzioni, dinamiche e diversità dell'italofonia nel XXI secolo.",
        explanation="L'**italofonia** è la comunità globale di circa 85 milioni di parlanti di italiano, distribuiti tra Italia (58 milioni), Svizzera italiana, comunità storiche in Istria, Dalmazia, Malta, e le diffuse comunità di emigrati in Argentina, Brasile, Stati Uniti, Australia.\n\n**Istituzioni chiave**:\n- **Accademia della Crusca** (1582): la più antica accademia linguistica d'Europa, oggi rinnovata con un ruolo descrittivo e consulenziale.\n- **Società Dante Alighieri** (1889): diffonde la lingua e la cultura italiana nel mondo con 500+ comitati in 80 paesi.\n\n**Dinamiche regionali**:\n- L'italiano in Svizzera è una delle quattro lingue ufficiali, parlato in Ticino e Grigioni.\n- In Istria (Croazia, Slovenia) l'italiano conserva lo status di lingua minoritaria protetta.\n- Le comunità italo-argentine e italo-brasiliane mantengono forme di italiano regionale e dialetti.\n\n**Dibattiti**: italiano come lingua ereditaria (heritage language), insegnamento dell'italiano all'estero, il ruolo dei media italiani (RAI) nella diffusione globale.",
        rules=[
            "L'italofonia non è un blocco monolitico: include lingue ereditarie, dialetti, varietà regionali.",
            "La Crusca oggi ha un approccio descrittivo, non prescrittivo.",
            "La Società Dante Alighieri è il principale strumento di diplomazia culturale italiana.",
            "Le comunità italofone all'estero mantengono tratti linguistici spesso arcaici rispetto all'italiano contemporaneo.",
        ],
        examples=[
            GrammarExample(
                text="In Argentina, si parla ancora di 'botiglia' per 'bottiglia', un tratto conservativo dell'italiano ottocentesco.",
                translation=None,
                note="italiano di emigrazione",
            ),
            GrammarExample(
                text="Il Ticino ha una Radiotelevisione svizzera in lingua italiana (RSI) che produce contenuti per l'intera italofonia.",
                translation=None,
            ),
            GrammarExample(
                text="La Dante Alighieri organizza corsi di italiano per oltre 200.000 studenti all'anno nel mondo.",
                translation=None,
                note="diffusione culturale",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="L'italofonia coincide con l'Italia.",
                correct="L'italofonia comprende comunità in Svizzera, Slovenia, Croazia, Malta e le numerose diaspore nel mondo.",
                note="L'italofonia non si esaurisce nei confini nazionali.",
            ),
        ],
        related=[
            "politica-linguistica-it",
            "prestiti-linguistici",
            "evoluzione-linguistica",
        ],
    ),
    GrammarTopic(
        slug="politica-linguistica-it",
        title="Politica linguistica in Italia",
        level="C2",
        category="Espressione",
        summary="Dall'Accademia della Crusca alle leggi di tutela: le politiche linguistiche italiane tra standard, dialetti e minoranze.",
        explanation="L'Italia ha una **politica linguistica complessa** e spesso implicita. A differenza di Francia e Spagna, l'Italia non ha mai avuto un'istituzione statale normativa paragonabile all'Académie française.\n\n**L'Accademia della Crusca**:\n- Ruolo storico di custode della purezza linguistica (Vocabolario degli Accademici della Crusca, 1612).\n- Oggi è un'istituzione rinnovata: il suo sito offre consulenza linguistica gratuita, il periodico *La Crusca per voi*, e promuove il dibattito sull'italiano contemporaneo.\n\n**Legislazione**:\n- **Legge 482/1999**: tutela delle minoranze linguistiche storiche (albanese, catalano, tedesco, greco, sloveno, croato, francese, franco-provenzale, friulano, ladino, occitano, sardo).\n- **Costituzione, art. 6**: 'La Repubblica tutela con apposite norme le minoranze linguistiche'.\n\n**Dibattiti contemporanei**:\n- **Dialetti vs. italiano standard**: l'Italia è un paese di diglossia storica; oggi il 45% degli italiani alterna italiano e dialetto.\n- **Anglicismi**: il dibattito tra puristi e aperturisti è costante; la Crusca ha una posizione equilibrata.\n- **Linguaggio di genere**: femminili professionali (la ministra, l'avvocata, l'architetta) tra resistenze e accettazione.",
        rules=[
            "La Crusca ha un ruolo consultivo, non legislativo.",
            "I dialetti italiani sono lingue romanze a pieno titolo, non varietà 'degradate' dell'italiano.",
            "La legge 482/1999 protegge dodici minoranze linguistiche storiche.",
            "Il dibattito sugli anglicismi in Italia è acceso ma non ha prodotto leggi restrittive come in Francia.",
        ],
        examples=[
            GrammarExample(
                text="Art. 6 Costituzione: 'La Repubblica tutela con apposite norme le minoranze linguistiche.'",
                translation=None,
                note="tutela costituzionale",
            ),
            GrammarExample(
                text="La Crusca ha riconosciuto 'petaloso' come neologismo corretto, mostrando il suo approccio descrittivo moderno.",
                translation=None,
                note="neologismo e Crusca",
            ),
            GrammarExample(
                text="Il sardo è riconosciuto come lingua minoritaria dalla legge 482/1999, insieme ad altre undici varietà.",
                translation=None,
                note="minoranze linguistiche",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="La Crusca decide cosa è corretto in italiano.",
                correct="La Crusca non ha potere normativo vincolante: osserva, descrive e consiglia, ma non legifera.",
                note="Ruolo descrittivo, non prescrittivo.",
            ),
            GrammarMistake(
                wrong="I dialetti sono forme scorrette dell'italiano.",
                correct="I dialetti italiani sono sistemi linguistici autonomi, evoluti dal latino volgare parallelamente all'italiano standard.",
                note="I dialetti non sono 'errori', sono altre lingue.",
            ),
        ],
        related=[
            "italofonia-contemporanea",
            "evoluzione-linguistica",
            "italiano-standard",
        ],
    ),
    GrammarTopic(
        slug="evoluzione-digitale-it",
        title="L'italiano nell'era digitale",
        level="C2",
        category="Espressione",
        summary="Come l'italiano evolve con il digitale: social media, messaggistica, IA e nuovi usi linguistici.",
        explanation="Il **digitale sta trasformando l'italiano** a una velocità inedita. Il web e i social media hanno accelerato fenomeni già esistenti (abbreviazioni, prestiti) e ne hanno creati di nuovi.\n\n**Messaggistica e social media**:\n- Abbreviazioni: *xké* (perché), *nn* (non), *cmq* (comunque), *tvb* (ti voglio bene), *xk* (perché).\n- Emoticon ed emoji come punteggiatura emotiva.\n- Hashtag e la loro sintassi: *#iorestoacasa, #savethechildren*.\n\n**Neologismi digitali**:\n- Verbi: *googlare, whatsappare, twittare, taggare, postare, shazammare, spoilerare, cliccare, scrollare*.\n- Nomi: *selfie, blogger, influencer, youtuber, follower, like/laikare*.\n- Calco e adattamento: *scaricare* (download), *caricare* (upload), *condividere* (share), *cestinare* (delete).\n\n**Anglicismi nel digitale**:\n- Penetrazione massiccia: *computer, smartphone, tablet, browser, chat, emoji, streaming, podcast*.\n- Resistenza lessicale: *dominio* (domain), *motore di ricerca* (search engine), *posta elettronica* (email), *allegato* (attachment).\n\n**IA e italiano**:\n- ChatGPT, DeepL, Google Translate: impatto sull'apprendimento e sull'uso dell'italiano.\n- Modelli linguistici addestrati prevalentemente su dati in inglese: rischio di appiattimento delle varietà linguistiche.\n- Sfida della sovranità linguistica digitale per l'italiano.",
        rules=[
            "L'italiano digitale non è 'degradato': è un registro adeguato al medium.",
            "I prestiti dall'inglese nel digitale sono massicci, ma l'italiano ha una tradizione di adattamento (bistecca < beef steak, gol < goal).",
            "I social media accelerano l'evoluzione linguistica ma anche l'obsolescenza dei neologismi.",
            "La Crusca monitora l'italiano digitale senza demonizzarlo né idealizzarlo.",
        ],
        examples=[
            GrammarExample(
                text="nn lo so xké nn me l'ha detto, cmq ci vediamo dopo",
                translation=None,
                note="linguaggio SMS / messaggistica",
            ),
            GrammarExample(
                text="Ho whatsappato a Maria e mi ha risposto con un vocale di tre minuti.",
                translation=None,
                note="neologismo digitale",
            ),
            GrammarExample(
                text="Su Instagram ha postato un selfie che ha ricevuto mille like in un'ora.",
                translation=None,
                note="anglicismi integrati",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="L'italiano dei social è 'cattivo italiano'.",
                correct="Ogni medium sviluppa un proprio registro: l'italiano digitale è una varietà situazionale, non una degenerazione.",
                note="Evitare giudizi di valore sulle varietà linguistiche.",
            ),
        ],
        related=[
            "italofonia-contemporanea",
            "politica-linguistica-it",
            "creativita-linguistica",
        ],
    ),
]
