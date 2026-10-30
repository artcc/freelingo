"""Italian grammar topics — B1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="congiuntivo-presente",
        title="Congiuntivo presente",
        level="B1",
        category="Congiuntivo",
        summary="Il modo della soggettività: dubbi, opinioni, desideri, emozioni.",
        explanation="Il **congiuntivo** è il modo della soggettività.\n\n**Formazione regolare:**\n- parlare: parli, parli, parli, parliamo, parliate, parlino.\n- leggere: legga, legga, legga, leggiamo, leggiate, leggano.\n- dormire: dorma, dorma, dorma, dormiamo, dormiate, dormano.\n- finire (-isc-): finisca, finisca, finisca, finiamo, finiate, finiscano.\n\n**Irregolari:** essere (sia), avere (abbia), andare (vada), fare (faccia), volere (voglia), potere (possa), dovere (debba), sapere (sappia), venire (venga), uscire (esca), dire (dica), bere (beva), stare (stia), dare (dia).",
        structure="-are → -i/-i/-i/-iamo/-iate/-ino\n-ere → -a/-a/-a/-iamo/-iate/-ano\n-ire → -a/-a/-a/-iamo/-iate/-ano (o -isca)",
        rules=[
            "Il congiuntivo si usa dopo verbi di opinione, desiderio, dubbio, emozione.",
            "Dopo espressioni impersonali: è importante che, bisogna che.",
            "Le tre persone singolari sono identiche.",
            "-are → -i; -ere/-ire → -a per le prime tre persone.",
        ],
        examples=[
            GrammarExample(text="Penso che lui sia bravissimo.", translation=None),
            GrammarExample(
                text="Spero che tu possa venire alla festa.",
                translation=None,
            ),
            GrammarExample(
                text="È importante che voi parliate italiano.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Penso che lui è bravo.",
                correct="Penso che lui sia bravo.",
                note="Dopo pensare che si usa il congiuntivo, non l'indicativo.",
            ),
            GrammarMistake(
                wrong="Credo che hai ragione.",
                correct="Credo che tu abbia ragione.",
                note="Dopo credere che serve il congiuntivo.",
            ),
        ],
        related=[
            "verbi-opinione",
            "espressioni-impersonali",
            "congiuntivo-volonta",
            "congiuntivo-emozioni",
        ],
    ),
    GrammarTopic(
        slug="verbi-opinione",
        title="Verbi di opinione + congiuntivo",
        level="B1",
        category="Congiuntivo",
        summary="Pensare, credere, ritenere, sembrare e il congiuntivo.",
        explanation="I verbi di opinione richiedono il **congiuntivo** nella subordinata.\n\n- pensare che: *Penso che sia tardi.*\n- credere che: *Credo che tu abbia ragione.*\n- ritenere che, sembrare che, avere l'impressione che, supporre che.\n\n**Eccezione:** stesso soggetto → di + infinito: *Penso **di** avere ragione.* (NON: Penso che io abbia ragione.)",
        rules=[
            "Verbi di opinione + che + congiuntivo (soggetti diversi).",
            "Verbi di opinione + di + infinito (stesso soggetto).",
            "Sembrare impersonale: Sembra che + congiuntivo.",
            "Con certezza oggettiva alcuni ammettono l'indicativo.",
        ],
        examples=[
            GrammarExample(
                text="Penso che questo film sia molto bello.",
                translation=None,
            ),
            GrammarExample(
                text="Credo di aver capito tutto.",
                translation=None,
                note="stesso soggetto",
            ),
            GrammarExample(text="Sembra che domani piova.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Penso di che tu abbia ragione.",
                correct="Penso che tu abbia ragione.",
                note="Di solo con stesso soggetto; altrimenti che.",
            ),
            GrammarMistake(
                wrong="Penso che io ho ragione.",
                correct="Penso di avere ragione.",
                note="Stesso soggetto → di + infinito.",
            ),
        ],
        related=[
            "congiuntivo-presente",
            "espressioni-impersonali",
            "congiuntivo-dubbi",
        ],
    ),
    GrammarTopic(
        slug="espressioni-impersonali",
        title="Espressioni impersonali + congiuntivo",
        level="B1",
        category="Congiuntivo",
        summary="È importante che, bisogna che, è necessario che e le frasi impersonali.",
        explanation="Espressioni impersonali di necessità/possibilità/importanza richiedono il congiuntivo.\n\n**Con congiuntivo:** è importante che, è necessario che, bisogna che, è meglio che, è possibile che, è probabile che, può darsi che, vale la pena che.\n\n**Senza congiuntivo** (certezza oggettiva): è vero che, è certo che, è sicuro che, è evidente che, è ovvio che → indicativo.",
        rules=[
            "Espressioni di necessità/possibilità → congiuntivo.",
            "Espressioni di certezza → indicativo.",
            "Bisogna che, occorre che, conviene che → congiuntivo.",
            "Stesso soggetto: è importante + infinito.",
        ],
        examples=[
            GrammarExample(
                text="È importante che tu mangi sano.",
                translation=None,
            ),
            GrammarExample(text="Bisogna che arriviamo in orario.", translation=None),
            GrammarExample(text="Può darsi che loro non lo sappiano.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="È importante che tu mangia sano.",
                correct="È importante che tu mangi sano.",
                note="Dopo 'è importante che' si usa il congiuntivo: tu mangi.",
            ),
            GrammarMistake(
                wrong="È possibile che lui arriva tardi.",
                correct="È possibile che lui arrivi tardi.",
                note="Con è possibile che si usa il congiuntivo.",
            ),
        ],
        related=["congiuntivo-presente", "verbi-opinione", "si-impersonale"],
    ),
    GrammarTopic(
        slug="congiuntivo-volonta",
        title="Congiuntivo di volontà",
        level="B1",
        category="Congiuntivo",
        summary="Volere, desiderare, preferire che + congiuntivo.",
        explanation="I verbi di volontà/desiderio richiedono il congiuntivo (soggetti diversi).\n\n- volere che: *Voglio che tu venga.*\n- desiderare che, preferire che, pretendere che, esigere che, augurarsi che, sperare che.\n\n**Stesso soggetto → infinito:** *Voglio venire.* (non: Voglio che io venga.)\n\nIn frasi indipendenti il congiuntivo esprime augurio: *Che tu possa essere felice!*",
        rules=[
            "Volontà + che + congiuntivo (soggetti diversi).",
            "Volontà + di + infinito (stesso soggetto).",
            "Sperare che regge il congiuntivo.",
            "Frasi indipendenti: Che tu possa essere felice! (augurio).",
        ],
        examples=[
            GrammarExample(text="Voglio che tu sia felice.", translation=None),
            GrammarExample(text="Preferisco che andiamo domani.", translation=None),
            GrammarExample(
                text="Spero che abbiate fatto buon viaggio.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Voglio che tu vai.",
                correct="Voglio che tu vada.",
                note="Dopo volere che ci vuole il congiuntivo.",
            ),
            GrammarMistake(
                wrong="Voglio che io parto.",
                correct="Voglio partire.",
                note="Stesso soggetto → infinito.",
            ),
        ],
        related=[
            "congiuntivo-presente",
            "verbi-opinione",
            "congiuntivo-emozioni",
            "vorrei",
        ],
    ),
    GrammarTopic(
        slug="congiuntivo-emozioni",
        title="Congiuntivo di emozione",
        level="B1",
        category="Congiuntivo",
        summary="Esprimere sentimenti e reazioni emotive con il congiuntivo.",
        explanation="Emozioni e sentimenti richiedono il congiuntivo.\n\n- essere contento/felice/triste/arrabbiato che: *Sono contento che tu sia qui.*\n- avere paura che, dispiacere che, preoccuparsi che, sorprendere che.\n- è un peccato che, che peccato che, è strano che.\n\nA differenza di volontà e opinione, le emozioni richiedono sempre il congiuntivo (anche con stesso soggetto: Sono felice di essere qui).",
        rules=[
            "Emozioni + che + congiuntivo.",
            "Le emozioni richiedono sempre il congiuntivo nella lingua standard.",
            "Stesso soggetto: Sono felice di essere qui.",
            "Nella lingua parlata informale si può sentire l'indicativo, ma non è corretto.",
        ],
        examples=[
            GrammarExample(text="Sono felice che tu sia venuto.", translation=None),
            GrammarExample(
                text="Mi dispiace che non possiate restare.",
                translation=None,
            ),
            GrammarExample(text="Ho paura che lui si perda.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Sono contento che tu sei qui.",
                correct="Sono contento che tu sia qui.",
                note="Le emozioni richiedono il congiuntivo.",
            ),
            GrammarMistake(
                wrong="Mi dispiace che non puoi venire.",
                correct="Mi dispiace che tu non possa venire.",
                note="Dopo dispiacere che serve il congiuntivo.",
            ),
        ],
        related=["congiuntivo-presente", "congiuntivo-volonta", "congiuntivo-dubbi"],
    ),
    GrammarTopic(
        slug="congiuntivo-dubbi",
        title="Congiuntivo di dubbio",
        level="B1",
        category="Congiuntivo",
        summary="Dubitare, non sapere, non essere sicuro che + congiuntivo.",
        explanation="Il dubbio e l'incertezza richiedono il congiuntivo.\n\n- dubitare che: *Dubito che lui dica la verità.*\n- non sapere che, non essere sicuro che, non credere che, non pensare che.\n\n**Attenzione:** l'affermazione opposta usa l'indicativo:\n- *So che è vero. Sono sicuro che funziona.*",
        rules=[
            "Dubitare, non sapere, non essere sicuro, non credere → congiuntivo.",
            "Sapere, essere sicuro, essere certo → indicativo.",
            'Dopo "non so se" si può usare indicativo o congiuntivo.',
            "La negazione trasforma l'indicativo in congiuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Dubito che lui arrivi in orario.",
                translation=None,
            ),
            GrammarExample(
                text="Non sono sicuro che questa sia la strada giusta.",
                translation=None,
            ),
            GrammarExample(
                text="Non credo che loro vogliano venire.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Dubito che lui arriva.",
                correct="Dubito che lui arrivi.",
                note="Dubitare richiede il congiuntivo.",
            ),
            GrammarMistake(
                wrong="Non so se lui è a casa. (formale)",
                correct="Non so se lui sia a casa.",
                note="Nel registro formale, dopo non so se si preferisce il congiuntivo.",
            ),
        ],
        related=["congiuntivo-presente", "verbi-opinione", "espressioni-impersonali"],
    ),
    GrammarTopic(
        slug="trapassato-prossimo-b1",
        title="Trapassato prossimo (B1)",
        level="B1",
        category="Tempi verbali",
        summary="Approfondimento del trapassato prossimo con congiuntivo e concordanza.",
        explanation="Ripasso e approfondimento del trapassato prossimo:\n\n- Azione passata precedente: *Era già uscito quando ho chiamato.*\n- Dopo dopo che, quando (anteriorità): *Dopo che ebbe finito, uscì.*\n- Nel periodo ipotetico dell'irrealtà (3º tipo): *Se avessi saputo, sarei venuto.*",
        rules=[
            "Trapassato prossimo = imperfetto ausiliare + participio.",
            "Esprime anteriorità rispetto a un passato.",
            "Nel periodo ipotetico del 3º tipo con congiuntivo trapassato.",
            "Non confondere con il trapassato remoto (ebbi fatto).",
        ],
        examples=[
            GrammarExample(
                text="Quando arrivai, erano già partiti tutti.",
                translation=None,
            ),
            GrammarExample(
                text="Se avessi studiato, avresti passato l'esame.",
                translation=None,
            ),
            GrammarExample(
                text="Non avevo mai visto niente di simile.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se avevo soldi, compravo la casa.",
                correct="Se avessi avuto soldi, avrei comprato la casa.",
                note="Periodo ipotetico 3º tipo: congiuntivo trapassato + condizionale passato.",
            ),
            GrammarMistake(
                wrong="Dopo che ho mangiato, sono uscito.",
                correct="Dopo aver mangiato, sono uscito.",
                note="Con lo stesso soggetto: dopo + infinito passato.",
            ),
        ],
        related=["trapassato-prossimo", "concordanza-tempi", "periodo-ipotetico-2"],
    ),
    GrammarTopic(
        slug="futuro-anteriore",
        title="Futuro anteriore",
        level="B1",
        category="Tempi verbali",
        summary="Esprimere un'azione futura che sarà completata prima di un'altra.",
        explanation="Il **futuro anteriore** esprime un'azione futura anteriore a un'altra futura.\n\n- *Quando avrò finito, ti chiamerò.*\n- *Appena sarà arrivato, cominceremo.*\n\nSi usa anche per ipotesi/supposizioni nel passato:\n- *Sarà già partito?* (Do you think he has already left?)\n- *Non ha risposto: avrà dimenticato.* (He must have forgotten.)",
        structure="futuro di avere/essere + participio passato",
        rules=[
            "Futuro semplice di avere/essere + participio passato.",
            "Anteriorità rispetto a un futuro semplice.",
            "Ipotesi/supposizioni sul passato: Sarà già arrivato.",
            "Con espressioni temporali: quando, appena, dopo che + futuro anteriore.",
        ],
        examples=[
            GrammarExample(
                text="Quando avrò finito i compiti, uscirò.",
                translation=None,
            ),
            GrammarExample(
                text="Saranno già partiti? Non rispondono.",
                translation=None,
            ),
            GrammarExample(
                text="Avrà dimenticato l'appuntamento.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando finirò, ti chiamo.",
                correct="Quando avrò finito, ti chiamerò.",
                note="Dopo quando + futuro si usa il futuro anteriore per anteriorità, poi futuro semplice.",
            ),
            GrammarMistake(
                wrong="Sarà arrivato ieri, forse.",
                correct="Sarà arrivato ieri.",
                note="Con il futuro anteriore la supposizione è già implicita.",
            ),
        ],
        related=["futuro-semplice", "concordanza-tempi", "condizionale-presente"],
    ),
    GrammarTopic(
        slug="concordanza-tempi",
        title="La concordanza dei tempi",
        level="B1",
        category="Avanzato",
        summary="Coordinare i tempi verbali tra principale e subordinata.",
        explanation="La concordanza dei tempi (consecutio temporum) regola il rapporto temporale tra principale e subordinata.\n\n**Principale al presente:** subordinata al tempo richiesto dal significato.\n- *Penso che sia / sia stato / sarà vero.*\n\n**Principale al passato:** la subordinata deve adattarsi:\n- Presente → imperfetto: *Pensavo che fosse vero.*\n- Passato → trapassato: *Pensavo che fosse stato vero.*\n- Futuro → condizionale passato: *Pensavo che sarebbe stato vero.*",
        rules=[
            "Principale al presente: libertà nella scelta del tempo.",
            "Principale al passato: la subordinata va al passato.",
            "Presente → imperfetto congiuntivo.",
            "Futuro → condizionale passato.",
        ],
        examples=[
            GrammarExample(text="Penso che Marco sia malato.", translation=None),
            GrammarExample(text="Pensavo che Marco fosse malato.", translation=None),
            GrammarExample(text="Speravo che sarebbe venuto.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Pensavo che Marco sia malato.",
                correct="Pensavo che Marco fosse malato.",
                note="Principale al passato → subordinata al passato.",
            ),
            GrammarMistake(
                wrong="Credevo che verrà.",
                correct="Credevo che sarebbe venuto.",
                note="Futuro nel passato → condizionale passato.",
            ),
        ],
        related=[
            "congiuntivo-presente",
            "congiuntivo-imperfetto",
            "discorso-indiretto-passato",
        ],
    ),
    GrammarTopic(
        slug="forma-passiva",
        title="La forma passiva",
        level="B1",
        category="Voce passiva",
        summary="Costruire la forma passiva con essere, venire e andare.",
        explanation="La forma passiva sposta il focus sull'oggetto che subisce l'azione.\n\n- **Essere + participio**: *Il libro è stato scritto da Eco.*\n- **Venire + participio** (solo tempi semplici): *Il libro viene letto da molti.*\n- **Andare + participio** (necessità/obbligo): *Questo lavoro va fatto subito.*\n\nIl participio concorda in genere e numero con il soggetto.\n\nL'agente è introdotto da **da**: *La torta è stata preparata dalla nonna.*",
        structure="essere/venire + participio passato (+ da + agente)",
        rules=[
            "Essere + participio per tutti i tempi.",
            "Venire + participio solo per tempi semplici (alternativa a essere).",
            "Andare + participio = dover essere (obbligo/necessità).",
            "Participio concorda con il soggetto in genere e numero.",
            "Agente introdotto da da.",
        ],
        examples=[
            GrammarExample(
                text="La lettera è stata spedita ieri.",
                translation=None,
            ),
            GrammarExample(
                text="Il museo viene visitato da molti turisti.",
                translation=None,
            ),
            GrammarExample(text="Queste regole vanno rispettate.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="La lettera ha stata spedita.",
                correct="La lettera è stata spedita.",
                note="La forma passiva usa essere, non avere.",
            ),
            GrammarMistake(
                wrong="Il libro viene essendo letto.",
                correct="Il libro viene letto.",
                note="Venire + participio; non serve essere.",
            ),
        ],
        related=["si-passivante", "passato-prossimo-essere", "concordanza-tempi"],
    ),
    GrammarTopic(
        slug="si-impersonale",
        title="Si impersonale",
        level="B1",
        category="Pronomi",
        summary="Usare il si per esprimere azioni impersonali e generali.",
        explanation="Il **si impersonale** si usa per frasi generali senza soggetto specifico.\n\n- *In Italia si mangia bene.* = People eat well in Italy.\n- *Si dice che...* = It is said that...\n\nCon verbi che hanno già il si riflessivo, si usa **ci si**: *Ci si alza presto.*\n\nCon aggettivi, il verbo è sempre singolare ma l'aggettivo va al plurale: *Si è stanchi.* (one is tired).",
        structure="si + verbo (3ª persona singolare)",
        rules=[
            "Si + verbo 3ª singolare: azione generale.",
            "Con verbi riflessivi: ci si + 3ª singolare.",
            "Con aggettivi: verbo singolare, aggettivo plurale.",
            "Il si impersonale non indica una persona specifica.",
        ],
        examples=[
            GrammarExample(text="In Italia si mangia bene.", translation=None),
            GrammarExample(
                text='Come si dice "casa" in inglese?',
                translation='How do you say "casa" in English?',
            ),
            GrammarExample(
                text="Quando si è giovani, si fanno molti errori.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Si mangiano bene in Italia.",
                correct="In Italia si mangia bene.",
                note="Il si impersonale usa la 3ª singolare, non plurale.",
            ),
            GrammarMistake(
                wrong="Ci si alziamo presto.",
                correct="Ci si alza presto.",
                note="Ci si + 3ª singolare (non plurale).",
            ),
        ],
        related=["si-passivante", "verbi-riflessivi", "pronomi-indiretti"],
    ),
    GrammarTopic(
        slug="si-passivante",
        title="Si passivante",
        level="B1",
        category="Voce passiva",
        summary="Il si usato per formare la voce passiva impersonale.",
        explanation="Il **si passivante** è simile alla forma passiva ma con il soggetto che segue il verbo e ne determina il numero.\n\n- *Si vendono libri.* = Books are sold. (libri è soggetto)\n- *Si vende la casa.* = The house is sold.\n\nDifferenza dal si impersonale:\n- Si passivante: soggetto espresso, verbo concorda col soggetto.\n- Si impersonale: nessun soggetto, verbo sempre 3ª singolare.",
        structure="si + verbo (3ª singolare o plurale) + soggetto",
        rules=[
            "Si + verbo + soggetto: il verbo concorda col soggetto.",
            "Soggetto singolare → verbo singolare.",
            "Soggetto plurale → verbo plurale.",
            "Usato per regole, divieti, istruzioni: Qui si parla italiano.",
        ],
        examples=[
            GrammarExample(text="Qui si vendono biglietti.", translation=None),
            GrammarExample(text="Si affitta appartamento.", translation=None),
            GrammarExample(
                text="Non si accettano carte di credito.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Si vende libri.",
                correct="Si vendono libri.",
                note="Libri è plurale → si vendono.",
            ),
            GrammarMistake(
                wrong="Si affittano appartamento.",
                correct="Si affitta appartamento.",
                note="Appartamento è singolare → si affitta.",
            ),
        ],
        related=["si-impersonale", "forma-passiva", "verbi-riflessivi"],
    ),
    GrammarTopic(
        slug="che-relativo",
        title="Che relativo",
        level="B1",
        category="Proposizioni",
        summary="Il pronome relativo che come soggetto e complemento oggetto.",
        explanation="**Che** è il pronome relativo più comune. Sostituisce il soggetto o il complemento oggetto.\n\n- Soggetto: *La ragazza **che** parla è mia sorella.* (che = la ragazza, soggetto di parla)\n- Oggetto: *Il libro **che** ho letto è interessante.* (che = il libro, oggetto di ho letto)\n\nChe è invariabile (non cambia per genere o numero).\n\nNon si usa mai la preposizione prima di che: *La ragazza **con cui** parlo* (NON: con che).",
        rules=[
            "Che sostituisce soggetto o complemento oggetto.",
            "Che è invariabile.",
            "Non si usa preposizione prima di che (usare cui).",
            "Che non può essere omesso come in inglese (that).",
        ],
        examples=[
            GrammarExample(
                text="La donna che parla è mia zia.",
                translation=None,
            ),
            GrammarExample(
                text="Il film che abbiamo visto era bello.",
                translation=None,
            ),
            GrammarExample(
                text="La cosa che mi piace di più è viaggiare.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="La ragazza con che parlo.",
                correct="La ragazza con cui parlo.",
                note="Dopo preposizione si usa cui, non che.",
            ),
            GrammarMistake(
                wrong="Il film abbiamo visto era bello.",
                correct="Il film che abbiamo visto era bello.",
                note="In italiano il pronome relativo non si può omettere.",
            ),
        ],
        related=["cui", "il-quale", "pronomi-diretti"],
    ),
    GrammarTopic(
        slug="cui",
        title="Cui: il complemento indiretto relativo",
        level="B1",
        category="Proposizioni",
        summary="Il pronome relativo cui per i complementi indiretti.",
        explanation="**Cui** si usa come pronome relativo dopo preposizioni.\n\n- *La ragazza **a cui** ho dato il libro.*\n- *Il paese **in cui** vivo.*\n- *La persona **di cui** ti parlavo.*\n\nCui può anche esprimere possesso: *La ragazza **il cui** padre è medico.* (la ragazza, il padre della quale...)\n\nCui è invariabile.",
        rules=[
            "Cui si usa dopo preposizione: a cui, di cui, con cui, da cui, in cui, su cui.",
            "Il cui / la cui / i cui / le cui = possesso.",
            "Cui è invariabile.",
            "Non confondere cui (relativo) con qui (luogo).",
        ],
        examples=[
            GrammarExample(text="La città in cui vivo è Roma.", translation=None),
            GrammarExample(
                text="L'amico di cui ti parlavo è arrivato.",
                translation=None,
            ),
            GrammarExample(
                text="La ragazza il cui fratello è attore si chiama Anna.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="La città in che vivo.",
                correct="La città in cui vivo.",
                note="Dopo preposizione si usa cui, mai che.",
            ),
            GrammarMistake(
                wrong="L'amico cui ti parlavo.",
                correct="L'amico di cui ti parlavo.",
                note="Cui ha bisogno della preposizione esplicita.",
            ),
        ],
        related=["che-relativo", "il-quale", "pronomi-indiretti"],
    ),
    GrammarTopic(
        slug="il-quale",
        title="Il quale / la quale / i quali / le quali",
        level="B1",
        category="Proposizioni",
        summary="I pronomi relativi variabili per chiarezza e registro formale.",
        explanation="**Il quale** (variabile: la quale, i quali, le quali) può sostituire che e cui, specialmente per evitare ambiguità o in contesti formali.\n\n- *La madre di Marco, la quale è insegnante...* (chiarisce: la madre è insegnante)\n- Dopo preposizione: *La persona alla quale mi riferivo.* (più formale di cui)\n\nSi usa spesso dopo preposizioni articolate: *del quale, al quale, sul quale*, ecc.",
        rules=[
            "Variabile: il quale, la quale, i quali, le quali.",
            "Utile per evitare ambiguità su chi sia il referente.",
            "Dopo preposizioni articolate: del quale, al quale.",
            "Registro più formale rispetto a che/cui.",
        ],
        examples=[
            GrammarExample(
                text="Il fratello di Maria, il quale vive a Londra, è medico.",
                translation=None,
            ),
            GrammarExample(
                text="La persona alla quale mi sono rivolto è stata gentile.",
                translation=None,
            ),
            GrammarExample(
                text="I motivi per i quali ho deciso di partire sono molti.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="La madre di Marco, che è insegnante... (ambiguo)",
                correct="La madre di Marco, la quale è insegnante...",
                note="Con che non si capisce se è la madre o Marco a essere insegnante.",
            ),
            GrammarMistake(
                wrong="Il quale che ho visto.",
                correct="Il quale ho visto. (o: che ho visto.)",
                note="Non si combina il quale con che.",
            ),
        ],
        related=["che-relativo", "cui", "connettivi-avanzati"],
    ),
    GrammarTopic(
        slug="periodo-ipotetico-1",
        title="Periodo ipotetico: 1º tipo (realtà)",
        level="B1",
        category="Condizionali",
        summary="Se + indicativo presente/futuro + indicativo presente/futuro.",
        explanation="Il **periodo ipotetico del 1º tipo** esprime un'ipotesi reale o molto probabile.\n\n- *Se piove, prendo l'ombrello.* (reale)\n- *Se studierai, passerai l'esame.* (probabile)\n- *Se hai fame, mangia qualcosa!* (imperativo)\n\nSi usa il modo indicativo sia nella protasi (se) che nell'apodosi (conseguenza).",
        structure="se + presente/futuro indicativo → presente/futuro indicativo (o imperativo)",
        rules=[
            "Protasi (se): indicativo presente o futuro.",
            "Apodosi: indicativo presente, futuro o imperativo.",
            "Esprime ipotesi reali o molto probabili.",
            "Non si usa mai il congiuntivo in questo tipo.",
        ],
        examples=[
            GrammarExample(text="Se piove, resto a casa.", translation=None),
            GrammarExample(text="Se avrò tempo, ti aiuterò.", translation=None),
            GrammarExample(
                text="Se hai fame, prendi una mela.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se pioverei, resterei a casa.",
                correct="Se piove, resto a casa.",
                note="Nel 1º tipo non si usa mai il condizionale nella protasi.",
            ),
            GrammarMistake(
                wrong="Se piove, resterei a casa.",
                correct="Se piove, resto a casa. (o: Se piovesse, resterei a casa.)",
                note="Non mischiare protasi reale con apodosi ipotetica.",
            ),
        ],
        related=["periodo-ipotetico-2", "se-congiuntivo", "condizionale-presente"],
    ),
    GrammarTopic(
        slug="periodo-ipotetico-2",
        title="Periodo ipotetico: 2º tipo (possibilità)",
        level="B1",
        category="Condizionali",
        summary="Se + congiuntivo imperfetto + condizionale presente.",
        explanation="Il **periodo ipotetico del 2º tipo** esprime un'ipotesi possibile ma non certa.\n\n- *Se avessi soldi, comprerei una casa.* (possibilità)\n- *Se potessi, verrei alla festa.*\n\nProtasi: congiuntivo imperfetto.\nApodosi: condizionale presente.",
        structure="se + congiuntivo imperfetto → condizionale presente",
        rules=[
            "Protasi: se + congiuntivo imperfetto.",
            "Apodosi: condizionale presente.",
            "Ipotesi possibili ma incerte.",
            "Mai il condizionale nella protasi.",
        ],
        examples=[
            GrammarExample(
                text="Se avessi tempo, viaggerei di più.",
                translation=None,
            ),
            GrammarExample(
                text="Se facesse bel tempo, andrei al mare.",
                translation=None,
            ),
            GrammarExample(
                text="Se potessi parlare italiano, vivrei a Roma.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se avrei soldi, comprerei una casa.",
                correct="Se avessi soldi, comprerei una casa.",
                note="In questa condizione ipotetica si usa il congiuntivo imperfetto; se interrogativo può invece precedere un condizionale.",
            ),
            GrammarMistake(
                wrong="Se avessi soldi, compravo una casa.",
                correct="Se avessi soldi, comprerei una casa.",
                note="L'apodosi vuole il condizionale presente, non l'imperfetto indicativo.",
            ),
        ],
        related=[
            "periodo-ipotetico-1",
            "se-congiuntivo",
            "congiuntivo-imperfetto",
            "condizionale-presente",
        ],
    ),
    GrammarTopic(
        slug="se-congiuntivo",
        title="Se + congiuntivo: regole generali",
        level="B1",
        category="Congiuntivo",
        summary="Distinguere se condizionale e se interrogativo indiretto.",
        explanation="Nel periodo ipotetico, se introduce la condizione:\n- Se piove, prendo l'ombrello.\n- Se piovesse, prenderei l'ombrello.\n- Se avesse piovuto, avrei preso l'ombrello.\n\nIn queste costruzioni il condizionale esprime la conseguenza, non sostituisce il congiuntivo nella condizione.\n\nSe può anche introdurre una **domanda indiretta**: Non so se verrebbe con noi. Qui il condizionale è corretto, perché se non introduce una condizione.",
        rules=[
            "Non sostituire il congiuntivo con il condizionale nella protasi ipotetica; distingui se interrogativo.",
            "1º tipo: se + indicativo.",
            "2º tipo: se + congiuntivo imperfetto → condizionale presente.",
            "3º tipo: se + congiuntivo trapassato → condizionale passato.",
        ],
        examples=[
            GrammarExample(text="Se potessi, lo farei.", translation=None),
            GrammarExample(
                text="Se avessi saputo, sarei venuto.",
                translation=None,
            ),
            GrammarExample(text="Se vuoi, possiamo uscire.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Se potrei, lo farei.",
                correct="Se potessi, lo farei.",
                note="Qui se introduce una condizione ipotetica, non una domanda indiretta.",
            ),
            GrammarMistake(
                wrong="Se avrei saputo, sarei venuto.",
                correct="Se avessi saputo, sarei venuto.",
                note="Dopo se si usa congiuntivo trapassato, non condizionale passato.",
            ),
        ],
        related=[
            "periodo-ipotetico-1",
            "periodo-ipotetico-2",
            "congiuntivo-imperfetto",
            "congiuntivo-trapassato",
        ],
    ),
    GrammarTopic(
        slug="discorso-indiretto-passato",
        title="Discorso indiretto al passato",
        level="B1",
        category="Discorso indiretto",
        summary="Riferire al passato: trasformazione dei tempi verbali e indicatori.",
        explanation="Per riportare parole da una prospettiva passata, usa l'imperfetto per la contemporaneità (Disse che era stanco), il trapassato per l'anteriorità (Disse che aveva mangiato) e il condizionale passato per la posteriorità (Disse che sarebbe venuto).\n\nIl cambiamento non è automatico: Ha detto che è stanco è corretto se lo è ancora; Ha detto che verrà domani mantiene un futuro rispetto a chi parla. Adatta qui/lì, oggi/quel giorno e domani/il giorno dopo solo se cambiano i riferimenti.",
        rules=[
            "Presente → imperfetto.",
            "Passato prossimo → trapassato prossimo.",
            "Futuro → condizionale passato.",
            "Imperfetto e trapassato restano invariati.",
            "Conserva tempi e indicatori ancora validi dal punto di vista di chi riporta.",
        ],
        examples=[
            GrammarExample(text="Ha detto che era stanco.", translation=None),
            GrammarExample(
                text="Disse che sarebbe arrivato il giorno dopo.",
                translation=None,
            ),
            GrammarExample(
                text="Mi spiegò che aveva già finito il lavoro.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ha detto che erano stanco. (riferito a Marco)",
                correct="Ha detto che era stanco.",
                note="Il verbo concorda con Marco; è stanco resta possibile se la situazione è ancora attuale.",
            ),
            GrammarMistake(
                wrong="Ha detto che sarebbe venire il giorno dopo.",
                correct="Ha detto che sarebbe venuto il giorno dopo.",
                note="Il condizionale passato richiede il participio venuto. Verrà domani è possibile se l'evento è ancora futuro.",
            ),
        ],
        related=["discorso-indiretto", "concordanza-tempi", "trasformazioni-temporali"],
    ),
    GrammarTopic(
        slug="connettivi-argomentativi",
        title="Connettivi argomentativi",
        level="B1",
        category="Avanzato",
        summary="Perciò, quindi, infatti, tuttavia, benché, purché per argomentare.",
        explanation="I connettivi argomentativi strutturano un discorso logico:\n\n- **Causa:** perché, poiché, dato che, siccome, visto che.\n- **Conseguenza:** quindi, perciò, dunque, di conseguenza.\n- **Contrasto:** ma, però, tuttavia, eppure, invece, mentre.\n- **Concessione:** benché, sebbene, nonostante, malgrado (+ congiuntivo).\n- **Scopo:** affinché, perché (+ congiuntivo).\n- **Condizione:** purché, a patto che, a condizione che (+ congiuntivo).",
        rules=[
            "Causa: perché, poiché, siccome + indicativo.",
            "Conseguenza: quindi, perciò, dunque + indicativo.",
            "Concessione: benché, sebbene + congiuntivo.",
            "Condizione: purché, a patto che + congiuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Siccome pioveva, siamo rimasti a casa.",
                translation=None,
            ),
            GrammarExample(
                text="Non ho studiato, quindi non ho passato l'esame.",
                translation=None,
            ),
            GrammarExample(
                text="Benché fosse tardi, abbiamo continuato.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Benché era tardi, siamo usciti.",
                correct="Benché fosse tardi, siamo usciti.",
                note="Benché richiede il congiuntivo.",
            ),
            GrammarMistake(
                wrong="Siccome pioveva, perciò siamo rimasti a casa.",
                correct="Siccome pioveva, siamo rimasti a casa.",
                note="Non usare due connettivi causali/consecutivi insieme.",
            ),
        ],
        related=["connettivi-narrativi", "congiuntivo-presente", "connettivi-avanzati"],
    ),
    GrammarTopic(
        slug="trasformazioni-temporali",
        title="Trasformazioni temporali nel discorso indiretto",
        level="B1",
        category="Discorso indiretto",
        summary="Come cambiano oggi, domani, qui e altri indicatori nel discorso indiretto.",
        explanation="Nel discorso indiretto al passato, gli indicatori di tempo e luogo cambiano:\n\n- oggi → quel giorno\n- ieri → il giorno prima\n- domani → il giorno dopo / il giorno seguente\n- adesso → in quel momento / allora\n- qui / qua → lì / là\n- questo/a → quello/a\n- tra due giorni → due giorni dopo\n- ... fa → ... prima\n- la settimana prossima → la settimana seguente",
        rules=[
            "Oggi → quel giorno; ieri → il giorno prima.",
            "Domani → il giorno dopo/seguente.",
            "Qui → lì; questo → quello.",
            "Tempo fa → tempo prima.",
        ],
        examples=[
            GrammarExample(
                text="Disse che quel giorno era stanco. (oggi)",
                translation=None,
            ),
            GrammarExample(
                text="Mi disse che sarebbe partito il giorno dopo. (domani)",
                translation=None,
            ),
            GrammarExample(
                text="Disse che era stato lì il giorno prima. (qui / ieri)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Disse che oggi era stanco.",
                correct="Disse che quel giorno era stanco.",
                note="Con verbo principale al passato, oggi → quel giorno.",
            ),
            GrammarMistake(
                wrong="Ieri ha detto che domani partirà.",
                correct="Ieri ha detto che oggi sarebbe partito. (o: il giorno dopo)",
                note="Adattare il riferimento temporale al momento del discorso indiretto.",
            ),
        ],
        related=[
            "discorso-indiretto-passato",
            "discorso-indiretto",
            "marcatori-temporali",
        ],
    ),
]
