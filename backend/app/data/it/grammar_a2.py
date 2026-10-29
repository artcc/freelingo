"""Italian grammar topics — A2."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="stare-gerundio",
        title="Stare + gerundio",
        level="A2",
        category="Tempi verbali",
        summary="Esprimere azioni in corso con stare + gerundio.",
        explanation="**Stare + gerundio** presenta un'azione in corso: Sto leggendo; Stavo dormendo quando hai chiamato.\n\nStare al presente: sto, stai, sta, stiamo, state, stanno. All'imperfetto: stavo, stavi, stava, stavamo, stavate, stavano.\n\nGerundio: -are → -ando, -ere/-ire → -endo. Forme frequenti irregolari: fare → facendo, dire → dicendo, bere → bevendo.\n\nPer un'abitudine usa normalmente il presente semplice: Leggo ogni sera. Distingui Sto mangiando (azione in corso) da Sto per mangiare (imminenza).",
        structure="stare al presente o all'imperfetto + gerundio",
        rules=[
            "Coniuga stare secondo il soggetto; il gerundio è invariabile.",
            "Distingui azioni in corso, abitudini e imminenza.",
            "Andare e venire + gerundio esprimono sfumature progressive approfondite a B2.",
        ],
        examples=[
            GrammarExample(text="Sto leggendo un libro interessante.", translation=None),
            GrammarExample(text="Cosa stavi facendo quando ti ho chiamato?", translation=None),
            GrammarExample(text="Stanno arrivando!", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Sto per mangiando.",
                correct="Sto per mangiare. / Sto mangiando.",
                note="Stare per + infinito indica imminenza; stare + gerundio indica un'azione in corso.",
            ),
            GrammarMistake(
                wrong="Sono mangiando.",
                correct="Sto mangiando.",
                note="La perifrasi progressiva usa stare, non essere.",
            ),
        ],
        related=["andare-gerundio", "venire-gerundio", "stare-per", "imperfetto"],
    ),
    GrammarTopic(
        slug="passato-prossimo-avere",
        title="Passato prossimo con avere",
        level="A2",
        category="Tempi verbali",
        summary="Esprimere azioni passate con l'ausiliare avere.",
        explanation="Il **passato prossimo** esprime azioni passate concluse e rilevanti nel presente.\n\nLa maggior parte dei verbi transitivi usa **avere**:\n- *Ho mangiato la pizza.*\n- *Hai visto quel film?*\n\n**Participio passato regolare:**\n- -are → -ato: parlato\n- -ere → -uto: creduto\n- -ire → -ito: dormito\n\nCon avere, il participio di solito resta invariato (maschile singolare).",
        structure="avere (presente) + participio passato\nho / hai / ha / abbiamo / avete / hanno + participio",
        rules=[
            "Avere + participio passato per la maggior parte dei verbi transitivi.",
            "Participio passato regolare: -ato, -uto, -ito.",
            "Con avere, il participio di solito rimane invariato.",
            "Con pronomi diretti lo, la, li, le, il participio concorda: L'ho vista.",
        ],
        examples=[
            GrammarExample(text="Ho mangiato una pizza buonissima.", translation=None),
            GrammarExample(text="Hai finito i compiti?", translation=None),
            GrammarExample(
                text="Abbiamo visitato Roma l'anno scorso.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Io ho andato al cinema.",
                correct="Sono andato al cinema.",
                note="Andare usa essere, non avere.",
            ),
            GrammarMistake(
                wrong="Ho vista la ragazza.",
                correct="Ho visto la ragazza.",
                note="Con avere il participio non concorda con il soggetto.",
            ),
        ],
        related=["passato-prossimo-essere", "participi-irregolari", "imperfetto"],
    ),
    GrammarTopic(
        slug="passato-prossimo-essere",
        title="Passato prossimo con essere",
        level="A2",
        category="Tempi verbali",
        summary="Esprimere azioni passate con l'ausiliare essere e la concordanza del participio.",
        explanation="Alcuni verbi usano **essere**. Con essere, il participio concorda in genere e numero con il soggetto.\n\nUsano essere:\n- Movimento: *andare, venire, arrivare, partire, tornare, entrare, uscire.*\n- Stato: *essere, stare, restare, rimanere.*\n- Cambiamento: *diventare, nascere, morire, crescere.*\n- Riflessivi: *alzarsi, svegliarsi, lavarsi.*\n- Impersonali: *piacere, sembrare, succedere.*",
        structure="essere (presente) + participio passato (concordato)\nsono/sei/è/siamo/siete/sono + participio (-o/-a/-i/-e)",
        rules=[
            "Con essere, il participio concorda con il soggetto in genere e numero.",
            "I verbi riflessivi usano sempre essere.",
            "Verbi intransitivi di movimento e stato → essere.",
            "Al femminile: sono andata, sei arrivata, si è svegliata.",
        ],
        examples=[
            GrammarExample(text="Sono andato al mercato.", translation=None),
            GrammarExample(
                text="Maria è arrivata ieri.",
                translation=None,
                note="arrivata: femminile",
            ),
            GrammarExample(text="Ci siamo alzati presto.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ho andato a casa.",
                correct="Sono andato a casa.",
                note="Andare usa essere come ausiliare.",
            ),
            GrammarMistake(
                wrong="Maria è arrivato.",
                correct="Maria è arrivata.",
                note="Con essere il participio deve concordare con il soggetto femminile.",
            ),
        ],
        related=["passato-prossimo-avere", "participi-irregolari", "verbi-riflessivi"],
    ),
    GrammarTopic(
        slug="participi-irregolari",
        title="Participi passati irregolari",
        level="A2",
        category="Tempi verbali",
        summary="I principali participi passati irregolari da memorizzare.",
        explanation="Molti verbi italiani hanno il participio passato irregolare:\n\n- aprire → aperto\n- bere → bevuto\n- chiedere → chiesto\n- chiudere → chiuso\n- correre → corso\n- decidere → deciso\n- dire → detto\n- fare → fatto\n- leggere → letto\n- mettere → messo\n- morire → morto\n- nascere → nato\n- prendere → preso\n- ridere → riso\n- rimanere → rimasto\n- rispondere → risposto\n- rompere → rotto\n- scegliere → scelto\n- scendere → sceso\n- scrivere → scritto\n- vedere → visto (o veduto)\n- venire → venuto\n- vincere → vinto\n- vivere → vissuto",
        rules=[
            "I verbi in -ere hanno le maggiori irregolarità.",
            "Molti participi irregolari finiscono in -so, -to, -sto.",
            "Serve memorizzarli insieme all'infinito.",
            "Alcuni verbi hanno doppio participio: visto/veduto, perso/perduto.",
        ],
        examples=[
            GrammarExample(text="Ho letto un bel libro.", translation=None),
            GrammarExample(text="Hai visto quel film?", translation=None),
            GrammarExample(text="Che cosa hai detto?", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ho leggito un libro.",
                correct="Ho letto un libro.",
                note="Il participio di leggere è letto, non leggito.",
            ),
            GrammarMistake(
                wrong="Ho apruto la finestra.",
                correct="Ho aperto la finestra.",
                note="Aprire ha il participio irregolare aperto.",
            ),
        ],
        related=["passato-prossimo-avere", "passato-prossimo-essere", "imperfetto"],
    ),
    GrammarTopic(
        slug="imperfetto",
        title="L'imperfetto",
        level="A2",
        category="Tempi verbali",
        summary="Descrivere azioni abituali, descrizioni e contesti nel passato.",
        explanation="L'**imperfetto** si usa per:\n- Azioni abituali: *Da bambino giocavo a calcio.*\n- Descrizioni: *La casa era grande.*\n- Contesto: *Mentre mangiavo, è arrivato Marco.*\n- Stati d'animo: *Avevo fame. Faceva freddo.*\n\nFormazione regolarissima; solo essere è irregolare: ero, eri, era, eravamo, eravate, erano.",
        structure="-are → -avo/-avi/-ava/-avamo/-avate/-avano\n-ere → -evo/-evi/-eva/-evamo/-evate/-evano\n-ire → -ivo/-ivi/-iva/-ivamo/-ivate/-ivano",
        rules=[
            "L'imperfetto è il più regolare dei tempi italiani.",
            "Si usa per azioni ripetute, descrizioni e contesto.",
            "Non si usa per azioni puntuali e concluse (passato prossimo).",
            "Essere è irregolare: ero, eri, era...",
        ],
        examples=[
            GrammarExample(
                text="Da piccola giocavo con le bambole.",
                translation=None,
            ),
            GrammarExample(text="Era una giornata bellissima.", translation=None),
            GrammarExample(
                text="Mentre studiavo, ha squillato il telefono.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ieri andavo al cinema.",
                correct="Ieri sono andato al cinema.",
                note="Per azione puntuale conclusa si usa il passato prossimo, non l'imperfetto.",
            ),
            GrammarMistake(
                wrong="Eravamo andati a Roma.",
                correct="Eravamo a Roma.",
                note="Non confondere imperfetto e trapassato prossimo.",
            ),
        ],
        related=[
            "passato-prossimo-vs-imperfetto",
            "marcatori-temporali",
            "passato-prossimo-avere",
        ],
    ),
    GrammarTopic(
        slug="passato-prossimo-vs-imperfetto",
        title="Passato prossimo vs imperfetto",
        level="A2",
        category="Tempi verbali",
        summary="Capire quando usare il passato prossimo e quando l'imperfetto.",
        explanation="Una delle distinzioni più difficili dell'italiano.\n\n**Passato prossimo:** azione puntuale, conclusa: *Ieri ho comprato un libro.*\n\n**Imperfetto:** azione abituale, descrizione, contesto: *Da bambino compravo caramelle.*\n\nEsempio classico:\n*Mentre **leggevo** (imperfetto — contesto), **è entrato** (passato prossimo — azione) mio padre.*",
        rules=[
            "Passato prossimo: che cosa è successo? (evento).",
            "Imperfetto: com'era la situazione? (descrizione/contesto).",
            "Con 'mentre' quasi sempre imperfetto.",
            "Indicatori: ieri → pass. prossimo; da bambino, sempre → imperfetto.",
        ],
        examples=[
            GrammarExample(
                text="Ieri ho visto un film bellissimo.",
                translation=None,
                note="pass. prossimo: evento",
            ),
            GrammarExample(
                text="Da giovane andavo sempre al mare.",
                translation=None,
                note="imperfetto: abitudine",
            ),
            GrammarExample(
                text="Mentre pioveva, sono uscito.",
                translation=None,
                note="imperfetto + pass. prossimo",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ieri mangiavo la pizza con gli amici.",
                correct="Ieri ho mangiato la pizza con gli amici.",
                note='"Ieri" indica evento concluso → passato prossimo.',
            ),
            GrammarMistake(
                wrong="Quando ero piccolo, ho giocato a calcio ogni giorno.",
                correct="Quando ero piccolo, giocavo a calcio ogni giorno.",
                note='"Ogni giorno" indica abitudine → imperfetto.',
            ),
        ],
        related=[
            "passato-prossimo-avere",
            "passato-prossimo-essere",
            "imperfetto",
            "marcatori-temporali",
        ],
    ),
    GrammarTopic(
        slug="marcatori-temporali",
        title="Marcatori temporali",
        level="A2",
        category="Avanzato",
        summary="Usare gli indicatori di tempo corretti con i diversi tempi verbali.",
        explanation="I marcatori temporali suggeriscono il tempo verbale da usare.\n\n**Passato prossimo:** ieri, l'altro ieri, ... fa, la settimana scorsa, il mese scorso, l'anno scorso, stamattina, poco fa, appena.\n\n**Imperfetto:** da bambino/a, da giovane, a quell'epoca, negli anni '90, ogni giorno, sempre, spesso, di solito, mentre, tutti i giorni.\n\n**Futuro:** domani, dopodomani, la settimana prossima, il mese prossimo, l'anno prossimo, tra poco, stasera.",
        rules=[
            "Ieri, la settimana scorsa → passato prossimo.",
            "Da bambino, sempre, ogni giorno → imperfetto.",
            "Domani, la settimana prossima → futuro semplice.",
            "Appena, poco fa → passato prossimo (prossimità).",
        ],
        examples=[
            GrammarExample(text="Due giorni fa ho visto Carlo.", translation=None),
            GrammarExample(text="Negli anni '90 vivevo a Milano.", translation=None),
            GrammarExample(
                text="La settimana prossima andremo a Parigi.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ieri andavo al supermercato.",
                correct="Ieri sono andato al supermercato.",
                note="Ieri indica evento puntuale, non abitudine.",
            ),
            GrammarMistake(
                wrong="Da bambino ho giocato sempre fuori.",
                correct="Da bambino giocavo sempre fuori.",
                note="Da bambino + sempre → abitudine passata = imperfetto.",
            ),
        ],
        related=[
            "passato-prossimo-vs-imperfetto",
            "passato-prossimo-avere",
            "imperfetto",
            "futuro-semplice",
        ],
    ),
    GrammarTopic(
        slug="pronomi-diretti",
        title="Pronomi diretti",
        level="A2",
        category="Pronomi",
        summary="Mi, ti, lo, la, ci, vi, li, le — sostituire il complemento oggetto.",
        explanation="I pronomi diretti sostituiscono il complemento oggetto (*chi? che cosa?*).\n\n- **mi** = me, **ti** = te, **lo** = lui, **la** = lei, **ci** = noi, **vi** = voi, **li** = loro (m), **le** = loro (f).\n\n*Vedi Marco? — Sì, **lo** vedo.*\n\nPosizione: di solito prima del verbo. Con infinito/imperativo possono seguire: *Voglio vederlo.* Con passato prossimo il participio concorda con lo/la/li/le: *L'ho vista.*",
        structure="mi · ti · lo/la · ci · vi · li/le (La formale)",
        rules=[
            "I pronomi diretti di solito precedono il verbo coniugato.",
            "Con l'infinito e l'imperativo: possono seguire il verbo.",
            "Con passato prossimo, il participio concorda con lo, la, li, le.",
            "Lo e la si apostrofano davanti a vocale o H: l'ho visto.",
        ],
        examples=[
            GrammarExample(
                text="Conosci Luca? — Sì, lo conosco.",
                translation=None,
            ),
            GrammarExample(
                text="Hai visto la partita? — No, non l'ho vista.",
                translation=None,
            ),
            GrammarExample(
                text="Dov'è il libro? — L'ho messo sul tavolo.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Conosci Maria? — Sì, conosco lei.",
                correct="Conosci Maria? — Sì, la conosco.",
                note="Invece di ripetere il nome si usa il pronome diretto.",
            ),
            GrammarMistake(
                wrong="Hai visto le ragazze? — Sì, li ho viste.",
                correct="Hai visto le ragazze? — Sì, le ho viste.",
                note="Le per femminile plurale; li è maschile plurale.",
            ),
        ],
        related=["pronomi-indiretti", "pronomi-combinati", "imperativo-pronomi"],
    ),
    GrammarTopic(
        slug="pronomi-indiretti",
        title="Pronomi indiretti",
        level="A2",
        category="Pronomi",
        summary="Mi, ti, gli, le, ci, vi, gli — il complemento di termine.",
        explanation="I pronomi indiretti rispondono a *a chi? a che cosa?*\n\n- **mi** = a me, **ti** = a te, **gli** = a lui, **le** = a lei, **ci** = a noi, **vi** = a voi, **gli** = a loro.\n\n*Do il libro a Marco → **Gli** do il libro.*\n*Scrivo a Maria → **Le** scrivo.*",
        structure="mi · ti · gli/le · ci · vi · gli (Le formale)",
        rules=[
            "I pronomi indiretti precedono il verbo coniugato.",
            "Gli per 'a lui' e 'a loro' (uso moderno).",
            "Le per 'a lei' e 'a Lei' (formale).",
            "Con piacere e verbi simili si usano i pronomi indiretti: Mi piace.",
        ],
        examples=[
            GrammarExample(text="Gli ho dato il mio numero.", translation=None),
            GrammarExample(text="Che cosa le hai detto?", translation=None),
            GrammarExample(text="Vi porto un regalo.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ho dato a lui il libro.",
                correct="Gli ho dato il libro.",
                note="Si usa il pronome indiretto gli invece di a lui.",
            ),
            GrammarMistake(
                wrong="A Maria le ho detto tutto.",
                correct="A Maria ho detto tutto. (o: Le ho detto tutto.)",
                note="In italiano standard e preferibile evitare il raddoppio qui; nella lingua parlata può comparire come dislocazione.",
            ),
        ],
        related=["pronomi-diretti", "pronomi-combinati", "piacere"],
    ),
    GrammarTopic(
        slug="pronomi-combinati",
        title="Pronomi combinati",
        level="A2",
        category="Pronomi",
        summary="Unire pronomi diretti e indiretti: me lo, te la, glielo, ecc.",
        explanation="Pronome indiretto + diretto = pronome combinato.\n\n- mi + lo → **me lo**: *Me lo dai?*\n- ti + la → **te la**: *Te la porto.*\n- gli/le + lo → **glielo**: *Glielo dico.*\n- ci + li → **ce li**: *Ce li ha portati.*\n- vi + le → **ve le**: *Ve le mando.*",
        structure="me lo/la/li/le · te lo/la/li/le · glielo/gliela/glieli/gliele · ce lo/la/li/le · ve lo/la/li/le",
        rules=[
            "Il pronome indiretto cambia: mi→me, ti→te, gli→glie, ci→ce, vi→ve.",
            "Glielo si scrive tutto attaccato.",
            "Con tempi composti il participio concorda con il diretto: Gliel'ho data.",
            "Con imperativo e infinito seguono il verbo: Dammelo, Voglio dartelo.",
        ],
        examples=[
            GrammarExample(text="Me lo presti il libro?", translation=None),
            GrammarExample(text="Gliel'ho detto ieri.", translation=None),
            GrammarExample(text="Ce li ha portati Maria.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mi lo dai?",
                correct="Me lo dai?",
                note="Mi diventa me quando è seguito da un altro pronome.",
            ),
            GrammarMistake(
                wrong="Gli lo dico.",
                correct="Glielo dico.",
                note="Gli + lo diventa sempre glielo, tutto unito.",
            ),
        ],
        related=["pronomi-diretti", "pronomi-indiretti", "imperativo-pronomi"],
    ),
    GrammarTopic(
        slug="comparativi",
        title="Comparativi",
        level="A2",
        category="Aggettivi e avverbi",
        summary="Confrontare persone, cose e azioni in italiano.",
        explanation="**Maggioranza:** più + agg + **di** (nomi) / **che** (verbi, agg): *più alto di Luca / più bello viaggiare che restare.*\n\n**Minoranza:** meno + agg + di/che.\n\n**Uguaglianza:** (così) + agg + **come** / (tanto) + agg + **quanto**: *alto come te / tanto alto quanto te.*\n\n**Irregolari:** buono → migliore, cattivo → peggiore, grande → maggiore, piccolo → minore.",
        structure="più/meno + aggettivo + di/che",
        rules=[
            "Più... di per confrontare due nomi diversi.",
            "Più... che per confrontare due aggettivi, verbi o avverbi.",
            "Così... come / tanto... quanto per l'uguaglianza.",
            "Comparativi irregolari: buono → migliore, cattivo → peggiore.",
        ],
        examples=[
            GrammarExample(text="Roma è più grande di Firenze.", translation=None),
            GrammarExample(text="È meno caro che veloce.", translation=None),
            GrammarExample(text="Sono alto come te.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Sono più alto che te.",
                correct="Sono più alto di te.",
                note="Tra due pronomi personali si usa di, non che.",
            ),
            GrammarMistake(
                wrong="Lei è più buona di me.",
                correct="Lei è migliore di me.",
                note="Buono ha il comparativo irregolare migliore.",
            ),
        ],
        related=["superlativi", "cosi-come", "aggettivi-descrittivi"],
    ),
    GrammarTopic(
        slug="superlativi",
        title="Superlativi",
        level="A2",
        category="Aggettivi e avverbi",
        summary="Esprimere il massimo o minimo grado di una qualità.",
        explanation="**Superlativo relativo:** il più/meno + agg + di: *il più alto della classe.*\n\n**Superlativo assoluto:**\n- -issimo: *bellissimo, grandissimo.*\n- molto, estremamente + agg: *molto bello.*\n- prefissi super-, stra-, ultra-: *superveloce, stracolmo.*\n\n**Forme irregolari:** buono → ottimo/migliore, cattivo → pessimo/peggiore, grande → massimo/maggiore, piccolo → minimo/minore.",
        structure="Articolo + più/meno + aggettivo (+ di + gruppo)\nAggettivo + -issimo/a/i/e",
        rules=[
            "Superlativo relativo: articolo + più/meno + aggettivo + di.",
            "Superlativo assoluto: -issimo, molto + aggettivo, prefissi.",
            "Aggettivi in -co/-go aggiungono H: stanchissimo, larghissimo.",
            "Forme irregolari: buono → ottimo; cattivo → pessimo.",
        ],
        examples=[
            GrammarExample(
                text="È il ristorante più famoso di Milano.",
                translation=None,
            ),
            GrammarExample(text="Questo gelato è buonissimo!", translation=None),
            GrammarExample(
                text="È la meno cara delle tre.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="È il più migliore.",
                correct="È il migliore.",
                note="Migliore è già superlativo; non si dice più migliore.",
            ),
            GrammarMistake(
                wrong="Questo caffè è molto ottimo.",
                correct="Questo caffè è ottimo.",
                note="Ottimo è già superlativo assoluto; non si rafforza.",
            ),
        ],
        related=["comparativi", "cosi-come", "aggettivi-descrittivi"],
    ),
    GrammarTopic(
        slug="cosi-come",
        title="Così... come / tanto... quanto",
        level="A2",
        category="Aggettivi e avverbi",
        summary="Costruzioni comparative di uguaglianza in italiano.",
        explanation="Comparativo di uguaglianza:\n\n- **(così) + agg/avv + come**: *Sei (così) alto come me.*\n- **(tanto) + agg/avv + quanto**: *Sei (tanto) alto quanto me.*\n- **tanto + nome + quanto**: *Ho tanti soldi quanto te.*\n\nCosì e tanto possono essere omessi nel parlato.",
        structure="(così) + aggettivo/avverbio + come\n(tanto) + aggettivo/avverbio + quanto\n(tanto) + nome + quanto",
        rules=[
            "Così... come e tanto... quanto sono intercambiabili.",
            "Così e tanto possono essere omessi.",
            "Con i nomi si usa solo tanto... quanto.",
            "Non si usa 'più come' o 'meno come'.",
        ],
        examples=[
            GrammarExample(
                text="Sei intelligente come tua sorella.",
                translation=None,
            ),
            GrammarExample(text="Ho tanto lavoro quanto te.", translation=None),
            GrammarExample(
                text="Parla italiano bene quanto un madrelingua.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Sono alto tanto come te.",
                correct="Sono alto come te. (o: tanto alto quanto te.)",
                note="Non mischiare le costruzioni: come con così, quanto con tanto.",
            ),
            GrammarMistake(
                wrong="È bravo così quanto lui.",
                correct="È bravo come lui.",
                note="Così si usa con come, non con quanto.",
            ),
        ],
        related=["comparativi", "superlativi", "aggettivi-descrittivi"],
    ),
    GrammarTopic(
        slug="imperativo-affermativo",
        title="Imperativo affermativo",
        level="A2",
        category="Tempi verbali",
        summary="Dare comandi, istruzioni e consigli in modo diretto e affermativo.",
        explanation="L'imperativo affermativo dà ordini e consigli.\n\n**Forme regolari:**\n- Tu: parl**a**! legg**i**! dorm**i**! fin**isci**!\n- Lei: parl**i**! legg**a**! dorm**a**! fin**isca**!\n- Noi: parl**iamo**! legg**iamo**!\n- Voi: parl**ate**! legg**ete**! dorm**ite**!\n\n**Irregolari comuni:** essere (sii), avere (abbi), andare (va'/vai), fare (fa'/fai), dire (di'), dare (da'/dai), stare (sta'/stai).",
        structure="Tu: -a (-are) / -i (-ere, -ire)\nLei: -i (-are) / -a (-ere, -ire)\nNoi: -iamo\nVoi: -ate / -ete / -ite\nLoro: -ino (-are) / -ano (-ere, -ire)",
        rules=[
            "Il tu dei verbi in -are prende -a.",
            "Il tu dei verbi in -ere e -ire prende -i.",
            "La forma di cortesia Lei inverte le vocali: -are→-i, -ere/-ire→-a.",
            "Con i pronomi, questi si attaccano alla fine: Dimmelo! Prendilo!",
        ],
        examples=[
            GrammarExample(text="Parla più lentamente!", translation=None),
            GrammarExample(
                text="Scusi, dov'è la stazione?",
                translation=None,
                note="Lei formale",
            ),
            GrammarExample(text="Prendiamo un caffè!", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Scusa, dov'è il bagno? (a uno sconosciuto)",
                correct="Scusi, dov'è il bagno?",
                note="Con sconosciuti si usa la forma di cortesia Lei.",
            ),
            GrammarMistake(
                wrong="Aspetta! (tu) — da aspettare",
                correct="Aspetta!",
                note="L'imperativo tu di aspettare è aspetta (regolare in -a).",
            ),
        ],
        related=["imperativo-informale", "imperativo-negativo", "imperativo-pronomi"],
    ),
    GrammarTopic(
        slug="imperativo-negativo",
        title="Imperativo negativo",
        level="A2",
        category="Tempi verbali",
        summary="Vietare o sconsigliare qualcosa: non + infinito per il tu.",
        explanation="L'imperativo negativo:\n\n- **Tu informale:** **non + infinito**. *Non parlare! Non uscire!*\n- **Altre persone:** non + imperativo affermativo. *Non parli! Non usciamo!*\n\nCon i pronomi:\n- Tu: *Non farlo! / Non lo fare!*\n- Voi: *Non fatelo!*",
        structure="Tu: non + infinito\nLei/Noi/Voi/Loro: non + imperativo",
        rules=[
            "Il tu negativo si forma con non + infinito.",
            "Lei, noi, voi, loro: non + forma imperativa.",
            "Con i pronomi: tu → non + infinito + pronome o non + pronome + infinito.",
            "Non confondere tu negativo con Lei: Non parlare! (tu) vs Non parli! (Lei).",
        ],
        examples=[
            GrammarExample(text="Non preoccuparti!", translation=None),
            GrammarExample(text="Non dite niente!", translation=None),
            GrammarExample(text="Signora, non si preoccupi!", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Non parli così! (a un amico)",
                correct="Non parlare così!",
                note="Il tu negativo usa l'infinito; non parli è Lei.",
            ),
            GrammarMistake(
                wrong="Non ti preoccupa!",
                correct="Non preoccuparti! (o: Non ti preoccupare!)",
                note="Preoccuparsi è riflessivo; il pronome va dopo infinito o prima.",
            ),
        ],
        related=[
            "imperativo-affermativo",
            "imperativo-informale",
            "imperativo-pronomi",
        ],
    ),
    GrammarTopic(
        slug="imperativo-pronomi",
        title="L'imperativo con i pronomi",
        level="A2",
        category="Pronomi",
        summary="Attaccare i pronomi all'imperativo: posizione e forme speciali.",
        explanation="Con l'imperativo, i pronomi si attaccano **dopo** il verbo (tu, noi, voi).\n\n- Tu: *Prendi**lo**! Mangia**la**!*\n- Noi: *Prendia**molo**!* (la -mo perde la o)\n- Voi: *Prende**telo**!*\n\nCon l'imperativo troncato (da', di', fa', sta', va'), la consonante del pronome raddoppia: *dammi, dimmi, fallo, stacci, vattene.*\n\nForma negativa (tu): *Non lo prendere!* o *Non prenderlo!*",
        rules=[
            "Con tu, noi, voi: il pronome si attacca dopo.",
            "Con noi, la -mo perde la o: mangiamo + lo → mangiamolo.",
            "Con imperativo troncato, raddoppia la consonante: da' + mi → dammi.",
            "Con il Lei formale, il pronome di solito precede: Lo prenda!",
        ],
        examples=[
            GrammarExample(text="Prendilo!", translation=None),
            GrammarExample(text="Dammi una mano!", translation=None),
            GrammarExample(text="Mangiamola subito!", translation=None),
            GrammarExample(text="Signore, lo guardi!", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Da mi il libro.",
                correct="Dammi il libro.",
                note="Con imperativo troncato (da') la consonante raddoppia: da' + mi → dammi.",
            ),
            GrammarMistake(
                wrong="Prendiamolo! (da prendiamo + lo)",
                correct="Prendiamolo!",
                note="Con il noi la -mo perde la vocale prima del pronome.",
            ),
        ],
        related=["imperativo-affermativo", "imperativo-negativo", "pronomi-combinati"],
    ),
    GrammarTopic(
        slug="condizionale-presente",
        title="Condizionale presente",
        level="A2",
        category="Condizionali",
        summary="Esprimere desideri, richieste cortesi e situazioni ipotetiche.",
        explanation="Il condizionale presente esprime desideri, cortesia, consigli.\n\n- Desideri: *Mi piacerebbe andare in Italia.*\n- Cortesia: *Potresti aiutarmi?*\n- Consigli: *Dovresti studiare di più.*\n\n**Formazione:**\n- -are: parlerei, parleresti...\n- -ere: leggerei...\n- -ire: dormirei...\n\n**Irregolari:** essere (sarei), avere (avrei), andare (andrei), fare (farei), dovere (dovrei), potere (potrei), volere (vorrei), sapere (saprei), vedere (vedrei), vivere (vivrei).",
        structure="-are/-ere → -erei/-eresti/-erebbe/-eremmo/-ereste/-erebbero\n-ire → -irei/-iresti/-irebbe/-iremmo/-ireste/-irebbero",
        rules=[
            "I verbi in -are cambiano la a in e: parlerei.",
            "I verbi in -ere e -ire mantengono la vocale tematica.",
            "Desideri, cortesia, consigli.",
            "Con periodo ipotetico (2º tipo) si abbina al congiuntivo imperfetto.",
        ],
        examples=[
            GrammarExample(text="Vorrei un caffè, per favore.", translation=None),
            GrammarExample(text="Potresti chiudere la finestra?", translation=None),
            GrammarExample(text="Mi piacerebbe visitare Venezia.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Vorrei che tu mi aiuti.",
                correct="Vorrei che tu mi aiutassi.",
                note="Dopo vorrei che si usa il congiuntivo imperfetto.",
            ),
            GrammarMistake(
                wrong="Io volerei un caffè.",
                correct="Io vorrei un caffè.",
                note="Volere ha il condizionale irregolare: vorrei, non volerei.",
            ),
        ],
        related=[
            "condizionale-cortesia",
            "vorrei",
            "congiuntivo-imperfetto",
            "periodo-ipotetico-1",
        ],
    ),
    GrammarTopic(
        slug="condizionale-cortesia",
        title="Condizionale di cortesia",
        level="A2",
        category="Condizionali",
        summary="Usare il condizionale per fare richieste educate e ammorbidire il tono.",
        explanation="Il condizionale ammorbidisce le richieste.\n\n- Ordinare: *Prenderei un antipasto.*\n- Informazioni: *Saprebbe dirmi dov'è la stazione?*\n- Proposte: *Ti andrebbe di uscire?*\n- Opinioni caute: *Direi che è meglio aspettare.*\n\nVerbi più usati: vorrei, potresti, piacerebbe, dispiacerebbe.",
        rules=[
            "Il condizionale rende le richieste più gentili.",
            "Vorrei è la forma più comune di richiesta cortese.",
            "Potresti + infinito = could you...?",
            "Ti andrebbe? / Andrebbe bene? sono forme colloquiali cortesi.",
        ],
        examples=[
            GrammarExample(
                text="Vorrei un tavolo per due, per favore.",
                translation=None,
            ),
            GrammarExample(text="Mi potrebbe portare il conto?", translation=None),
            GrammarExample(
                text="Ti andrebbe di prendere un caffè?",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Voglio un caffè. (in modo brusco)",
                correct="Vorrei un caffè, per favore.",
                note="Voglio è diretto e può suonare maleducato. Vorrei è sempre meglio.",
            ),
            GrammarMistake(
                wrong="Posso avere un caffè?",
                correct="Potrei avere un caffè? (o: Vorrei un caffè.)",
                note="Posso è più diretto; potrei o vorrei è più educato.",
            ),
        ],
        related=["condizionale-presente", "vorrei", "verbi-modali"],
    ),
    GrammarTopic(
        slug="vorrei",
        title="Vorrei: il condizionale di volere",
        level="A2",
        category="Condizionali",
        summary="La parola magica per chiedere educatamente qualsiasi cosa in italiano.",
        explanation="**Vorrei** è la forma più utile del condizionale:\n\n1. **Ordinare:** *Vorrei un caffè.*\n2. **Desiderio:** *Vorrei imparare l'italiano.*\n3. **Desiderio per altri** (congiuntivo!): *Vorrei che tu venissi.*\n\nDifferenza fondamentale:\n- *Vorrei* + nome/infinito = desiderio semplice.\n- *Vorrei che* + congiuntivo imperfetto = soggetti diversi.",
        structure="vorrei + nome/infinito · vorrei + che + congiuntivo imperfetto",
        rules=[
            "Vorrei + nome: Vorrei un gelato.",
            "Vorrei + infinito: Vorrei andare al mare.",
            "Vorrei che + congiuntivo imperfetto (soggetti diversi).",
            "Non usare vorrei con se ipotetico: Se potessi, andrei (non: Se potrei, vorrei).",
        ],
        examples=[
            GrammarExample(text="Vorrei un bicchiere d'acqua.", translation=None),
            GrammarExample(
                text="Vorrei visitare Firenze un giorno.",
                translation=None,
            ),
            GrammarExample(text="Vorrei che facesse più caldo.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Vorrei che tu vieni.",
                correct="Vorrei che tu venissi.",
                note="Dopo vorrei che ci vuole il congiuntivo imperfetto.",
            ),
            GrammarMistake(
                wrong="Se vorrei, andrei.",
                correct="Se volessi, andrei.",
                note="Nel periodo ipotetico il se non vuole mai il condizionale.",
            ),
        ],
        related=[
            "condizionale-presente",
            "condizionale-cortesia",
            "congiuntivo-imperfetto",
        ],
    ),
    GrammarTopic(
        slug="connettivi-narrativi",
        title="Connettivi narrativi",
        level="A2",
        category="Avanzato",
        summary="Collegare eventi in una storia: poi, dopo, infine, prima, mentre, quando.",
        explanation="Per raccontare una storia:\n\n- **prima (di)**: *Prima di uscire, chiudi la porta.*\n- **dopo (di)**: *Dopo cena, guardiamo un film.*\n- **poi**: *Ho fatto la spesa e poi sono tornato.*\n- **infine / alla fine**: *Infine, abbiamo preso il treno.*\n- **mentre**: *Mentre cucinavo, ascoltavo musica.*\n- **quando**: *Quando sono arrivato, era tardi.*\n- **all'inizio**: *All'inizio non capivo niente.*\n- **improvvisamente**: *All'improvviso ha iniziato a piovere.*",
        rules=[
            "Prima di + infinito: Prima di mangiare, lavati le mani.",
            "Dopo + nome o dopo + che + verbo: Dopo pranzo / Dopo che ho mangiato.",
            "Poi collega due azioni consecutive.",
            "Mentre regge l'imperfetto: Mentre mangiavo...",
        ],
        examples=[
            GrammarExample(
                text="Prima di uscire, ho chiuso tutte le finestre.",
                translation=None,
            ),
            GrammarExample(
                text="Siamo andati al ristorante e poi al cinema.",
                translation=None,
            ),
            GrammarExample(text="All'improvviso è apparso un gatto.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Prima uscire, mangio.",
                correct="Prima di uscire, mangio.",
                note="Prima richiede la preposizione di quando seguito da un verbo.",
            ),
            GrammarMistake(
                wrong="Dopo ho mangiato, sono uscito.",
                correct="Dopo aver mangiato, sono uscito.",
                note="Con lo stesso soggetto: dopo + infinito passato.",
            ),
        ],
        related=[
            "connettivi-argomentativi",
            "marcatori-temporali",
            "passato-prossimo-vs-imperfetto",
        ],
    ),
    GrammarTopic(
        slug="trapassato-prossimo",
        title="Trapassato prossimo",
        level="A2",
        category="Tempi verbali",
        summary="Esprimere un'azione passata precedente a un'altra azione passata.",
        explanation="Il **trapassato prossimo** esprime un'azione passata avvenuta **prima** di un'altra azione passata.\n\n- *Quando sono arrivato, Maria era già uscita.* (Maria uscita → io arrivato)\n- *Avevo già mangiato quando mi hai chiamato.*\n\nFormazione: imperfetto di avere (avevo...) o essere (ero...) + participio passato.",
        structure="imperfetto di avere/essere + participio passato",
        rules=[
            "Azione passata precedente a un'altra azione passata.",
            "Si usa spesso con già, non ancora, appena.",
            "Con essere il participio concorda: Lei era già partita.",
            "Non si usa da solo; serve un'altra azione passata di riferimento.",
        ],
        examples=[
            GrammarExample(
                text="Quando sono arrivato, il film era già cominciato.",
                translation=None,
            ),
            GrammarExample(text="Avevo già visto quel film.", translation=None),
            GrammarExample(
                text="Non avevamo mai mangiato la pizza prima di allora.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quando ho arrivato, il film era cominciato.",
                correct="Quando sono arrivato, il film era già cominciato.",
                note="Arrivare usa essere; trapassato: ero arrivato/a.",
            ),
            GrammarMistake(
                wrong="Ero già mangiato.",
                correct="Avevo già mangiato.",
                note="Mangiare usa avere; trapassato: avevo mangiato.",
            ),
        ],
        related=[
            "passato-prossimo-avere",
            "passato-prossimo-essere",
            "imperfetto",
            "connettivi-narrativi",
        ],
    ),
    GrammarTopic(
        slug="discorso-indiretto",
        title="Discorso indiretto al presente",
        level="A2",
        category="Discorso indiretto",
        summary="Riferire ciò che qualcuno ha detto adattando i pronomi e i tempi verbali.",
        explanation='Il **discorso indiretto** riferisce le parole altrui senza citazione diretta.\n\nQuando il verbo principale è al presente, il tempo della subordinata **non cambia**:\n- Diretto: *Marco dice: "Vado al cinema."*\n- Indiretto: *Marco dice che **va** al cinema.*\n\nCambiamenti:\n- Si usa **che** per introdurre.\n- Pronomi e possessivi si adattano al nuovo punto di vista.\n- Indicatori di spazio/tempo: *qui → lì, oggi → quel giorno.*',
        rules=[
            "Con verbo principale al presente, il tempo verbale non cambia.",
            "I pronomi personali e possessivi cambiano secondo il nuovo soggetto.",
            "Qui / qua → lì / là; questo / questa → quello / quella.",
            "Le domande totali usano se; quelle parziali conservano l'interrogativo: Mi chiede se esco / dove vado. L'italiano non richiede un'inversione nella domanda diretta.",
        ],
        examples=[
            GrammarExample(text="Dice che è stanco.", translation=None),
            GrammarExample(
                text="Anna dice che domani partirà.",
                translation=None,
            ),
            GrammarExample(
                text="Mi ha chiesto se mi piaceva il film.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Marco dice che va io al cinema. (Marco parla di sé)",
                correct="Marco dice che va al cinema.",
                note="Adatta i pronomi al referente. Al passato, Ha detto che andava adotta una prospettiva passata; Ha detto che va può mantenere una situazione attuale.",
            ),
            GrammarMistake(
                wrong="Lei dice che sono stanca. (riferito a lei, non a chi riporta)",
                correct="Lei dice che è stanca.",
                note="La persona verbale segue il referente. Ripetere lei è possibile per contrasto o chiarezza.",
            ),
        ],
        related=[
            "discorso-indiretto-passato",
            "discorso-riportato",
            "connettivi-narrativi",
        ],
    ),
]
