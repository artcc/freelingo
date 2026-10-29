"""Italian grammar topics — C1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="congiuntivo-concessivo",
        title="Congiuntivo concessivo",
        level="C1",
        category="Congiuntivo",
        summary="Benché, sebbene, nonostante, malgrado + congiuntivo per esprimere concessione.",
        explanation="Le congiunzioni concessive richiedono il congiuntivo.\n\n- **Benché** / **Sebbene** + congiuntivo: *Benché piovesse, uscimmo.*\n- **Nonostante** / **Malgrado** + congiuntivo: *Nonostante fosse tardi, continuarono.*\n- **Anche se** + indicativo (eccezione): *Anche se pioveva, uscimmo.*\n\nLa scelta del tempo del congiuntivo segue la concordanza.",
        rules=[
            "Benché, sebbene, nonostante, malgrado + congiuntivo.",
            "Anche se + indicativo (eccezione nelle concessive).",
            "Concordanza: presente → cong. presente; passato → cong. imperfetto.",
            "Registro formale richiede il congiuntivo.",
        ],
        examples=[
            GrammarExample(
                text="Benché fosse stanco, continuo a lavorare.",
                translation=None,
            ),
            GrammarExample(
                text="Nonostante abbia studiato molto, non ha passato l'esame.",
                translation=None,
            ),
            GrammarExample(
                text="Sebbene sia tardi, resto ancora un po.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Benché era stanco, continuo.",
                correct="Benché fosse stanco, continuo.",
                note="Benché richiede sempre il congiuntivo.",
            ),
            GrammarMistake(
                wrong="Anche se fosse tardi... (non necessario)",
                correct="Anche se era tardi...",
                note="Anche se regge l'indicativo, non il congiuntivo.",
            ),
        ],
        related=[
            "congiuntivo-presente",
            "congiuntivo-imperfetto",
            "connettivi-argomentativi",
        ],
    ),
    GrammarTopic(
        slug="congiuntivo-finale",
        title="Congiuntivo finale (scopo)",
        level="C1",
        category="Congiuntivo",
        summary="Affinché, perché (scopo) + congiuntivo per esprimere lo scopo di un'azione.",
        explanation="Le proposizioni finali esprimono lo scopo e richiedono il congiuntivo.\n\n- **Affinché** + congiuntivo: *Parlo lentamente affinché tu capisca.*\n- **Perché** + congiuntivo: *Te lo dico perché tu lo sappia.*\n- **Acciocché** (letterario) + congiuntivo.\n\nCon lo stesso soggetto si usa per + infinito: *Studio per imparare.*",
        rules=[
            "Affinché, perché (scopo) + congiuntivo.",
            "Stesso soggetto: per + infinito.",
            "Tempo del congiuntivo secondo concordanza.",
            "Registro formale: affinché; colloquiale: perché.",
        ],
        examples=[
            GrammarExample(
                text="Ti scrivo affinché tu sia informato.",
                translation=None,
            ),
            GrammarExample(
                text="Parlo ad alta voce perché tutti sentano.",
                translation=None,
            ),
            GrammarExample(
                text="Studio ogni giorno per migliorare. (stesso soggetto)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ti scrivo affinché sei informato.",
                correct="Ti scrivo affinché tu sia informato.",
                note="Affinché richiede il congiuntivo.",
            ),
            GrammarMistake(
                wrong="Studio per che imparo.",
                correct="Studio per imparare. (o: Studio affinché io impari.)",
                note="Stesso soggetto → per + infinito.",
            ),
        ],
        related=[
            "congiuntivo-presente",
            "congiuntivo-concessivo",
            "connettivi-argomentativi",
        ],
    ),
    GrammarTopic(
        slug="congiuntivo-relativo",
        title="Congiuntivo nelle relative",
        level="C1",
        category="Congiuntivo",
        summary="Uso del congiuntivo nelle proposizioni relative per esprimere carattere restrittivo o eventuale.",
        explanation="Il congiuntivo nelle relative esprime:\n- **Carattere eventuale/ipotetico:** *Cerco una persona che parli inglese.* (non so se esista)\n- **Con superlativo relativo:** *È il libro più bello che io abbia mai letto.*\n- **Dopo negazione o restrizione:** *Non c'è nessuno che possa aiutarmi.*\n\nL'indicativo si usa per fatti certi: *Conosco una persona che parla inglese.*",
        rules=[
            "Congiuntivo = ipotetico/non certo.",
            "Indicativo = fatto certo/reale.",
            "Dopo superlativo relativo si usa il congiuntivo.",
            "Dopo espressioni negative restrittive: nessuno che, niente che.",
        ],
        examples=[
            GrammarExample(
                text="Cerco un libro che spieghi bene la grammatica. (non so se esiste)",
                translation=None,
                note="ipotetico",
            ),
            GrammarExample(
                text="È il film più emozionante che io abbia mai visto.",
                translation=None,
                note="superlativo",
            ),
            GrammarExample(
                text="Conosco un libro che spiega bene la grammatica.",
                translation=None,
                note="certo → indicativo",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Cerco una persona che parla inglese. (ma non so se esista)",
                correct="Cerco una persona che parli inglese.",
                note="Se la persona non è certa, si usa il congiuntivo.",
            ),
            GrammarMistake(
                wrong="È il più bello che io abbiano mai visto.",
                correct="È il più bello che abbia mai visto.",
                note="Con io si usa abbia, non abbiano. Dopo un superlativo il congiuntivo sottolinea la valutazione; l'indicativo è possibile in un'affermazione fattuale.",
            ),
        ],
        related=["che-relativo", "cui", "congiuntivo-presente", "superlativi"],
    ),
    GrammarTopic(
        slug="nominalizzazione",
        title="Nominalizzazione",
        level="C1",
        category="Avanzato",
        summary="Trasformare verbi e aggettivi in nomi per uno stile più formale e denso.",
        explanation="La nominalizzazione trasforma verbi/aggettivi in sostantivi, tipica dello stile formale e accademico.\n\n- Verbo → nome: *costruire → la costruzione; analizzare → l'analisi.*\n- Aggettivo → nome: *rapido → la rapidità; bello → la bellezza.*\n\nVantaggi: concisione, oggettività, formalità.\nSvantaggi: può rendere il testo pesante e astratto.",
        rules=[
            "Verbi in -zione, -mento, -aggio: costruzione, cambiamento, atterraggio.",
            "Aggettivi in -(e)zza, -ita: bellezza, rapidità.",
            "Utile nello stile accademico, giuridico, tecnico.",
            "Evitare accumulo eccessivo di nominalizzazioni.",
        ],
        examples=[
            GrammarExample(
                text="L'analisi dei dati ha richiesto tre mesi. (invece di: Abbiamo analizzato i dati per tre mesi.)",
                translation=None,
            ),
            GrammarExample(
                text="La costruzione del ponte fu completata nel 2010.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eccesso di nominalizzazioni: 'L'effettuazione della verifica della documentazione...'",
                correct="Verificare la documentazione...",
                note="Troppe nominalizzazioni appesantiscono il testo.",
            ),
        ],
        related=["registro-formale", "sintesi-testuale", "impersonalita"],
    ),
    GrammarTopic(
        slug="impersonalita",
        title="Impersonalità e distacco",
        level="C1",
        category="Avanzato",
        summary="Tecniche per esprimere impersonalità e distacco nel registro formale.",
        explanation="Strategie per l'impersonalità:\n- **Si impersonale/passivante:** *Si ritiene che...*\n- **Forma passiva:** *È stato dimostrato che...*\n- **Costruzioni impersonali:** *Bisogna, occorre, è necessario.*\n- **Soggetto generico:** *Uno, taluni, certi.*\n- **Infinito sostantivato:** *Il fare, il dire.*",
        rules=[
            "Si impersonale per affermazioni generali.",
            "Forma passiva per mettere in risalto l'azione.",
            "Evitare prima persona (io, noi) in testi formali.",
            "Costruzioni con va + participio: va notato, va detto.",
        ],
        examples=[
            GrammarExample(
                text="Si ritiene che la situazione sia migliorata.",
                translation=None,
            ),
            GrammarExample(
                text="È stato osservato un aumento dei prezzi.",
                translation=None,
            ),
            GrammarExample(
                text="Va notato che i risultati sono preliminari.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Io penso che... (in un testo accademico)",
                correct="Si ritiene che... / È opinione diffusa che...",
                note="In testi formali evitare la prima persona.",
            ),
        ],
        related=["si-impersonale", "forma-passiva", "registro-formale"],
    ),
    GrammarTopic(
        slug="campi-semantici",
        title="Campi semantici",
        level="C1",
        category="Avanzato",
        summary="Raggruppare e organizzare il lessico per campi semantici.",
        explanation="Un campo semantico è un insieme di parole legate da significato comune.\n\nEsempi:\n- **Meteorologia:** pioggia, neve, grandine, vento, nuvola, temporale.\n- **Emozioni:** gioia, tristezza, rabbia, paura, sorpresa, disgusto.\n- **Politica:** governo, parlamento, elezioni, partito, riforma.\n\nL'organizzazione in campi semantici facilita l'apprendimento del lessico.",
        rules=[
            "Organizzare il lessico per aree tematiche.",
            "Riconoscere iponimi e iperonimi.",
            "Espandere il vocabolario per singolo campo.",
            "Utile per la scrittura tematica e traduzione.",
        ],
        examples=[
            GrammarExample(
                text="Nel campo semantico del cibo: pasta, pizza, risotto, insalata, formaggio, vino.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Imparare liste di parole isolate.",
                correct="Imparare parole organizzate per campi semantici.",
                note="Il cervello memorizza meglio parole collegate tra loro.",
            ),
        ],
        related=["precisione-lessicale", "derivazione", "sfumature"],
    ),
    GrammarTopic(
        slug="derivazione",
        title="Derivazione delle parole",
        level="C1",
        category="Avanzato",
        summary="Prefissi e suffissi per creare nuove parole italiane.",
        explanation="La derivazione crea parole nuove con prefissi e suffissi.\n\n**Prefissi:**\n- ri- (ripetizione): *rifare, rileggere.*\n- s- (negazione/contrario): *scomodo, sfortunato.*\n- dis- (negazione): *disordinato, disonesto.*\n- pre- (prima): *prevedere, preistoria.*\n\n**Suffissi:**\n- -zione (azione): *costruzione, traduzione.*\n- -tore/-trice (agente): *lavoratore, scrittrice.*\n- -bile (possibilità): *leggibile, mangiabile.*\n- -ezza/-ita (qualità): *bellezza, rapidità.*",
        rules=[
            "Prefissi modificano il significato della radice.",
            "Suffissi cambiano la categoria grammaticale.",
            "I suffissi alterativi (-ino, -one, -accio) esprimono sfumature.",
            "Attenzione ai falsi derivati.",
        ],
        examples=[
            GrammarExample(
                text="Rileggere il testo aiuta a trovare errori.",
                translation=None,
                note="ri- = di nuovo",
            ),
            GrammarExample(
                text="La situazione è migliorabile.",
                translation=None,
                note="-bile = che può essere",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Usare suffissi in modo arbitrario.",
                correct="Conoscere i suffissi produttivi per ogni categoria.",
                note="Non tutti i verbi formano nomi con -zione.",
            ),
        ],
        related=["campi-semantici", "precisione-lessicale", "prestiti-linguistici"],
    ),
    GrammarTopic(
        slug="precisione-lessicale",
        title="Precisione lessicale",
        level="C1",
        category="Avanzato",
        summary="Scegliere la parola esatta: evitare genericità e approssimazioni.",
        explanation="La precisione lessicale distingue un parlante C1.\n\nTecniche:\n- Sostituire parole generiche con termini specifici.\n- *Cosa → oggetto, elemento, fenomeno, questione.*\n- *Fare → realizzare, effettuare, compiere, eseguire.*\n- *Bello → splendido, incantevole, affascinante, suggestivo.*\n- Usare collocazioni appropriate (combinazioni tipiche di parole).",
        rules=[
            "Preferire il termine specifico a quello generico.",
            "Consultare dizionari dei sinonimi e collocazioni.",
            "Adeguare la scelta al registro e contesto.",
            "Evitare il verbo generico fare quando possibile.",
        ],
        examples=[
            GrammarExample(
                text="Il governo ha adottato misure per contrastare l'inflazione. (non: ha fatto cose)",
                translation=None,
            ),
            GrammarExample(
                text="Il tramonto dipingeva il cielo di sfumature purpuree. (non: era bello)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ho fatto una bella esperienza.",
                correct="Ho vissuto un'esperienza entusiasmante/formativa/indimenticabile.",
                note="Bello è generico; scegliere aggettivo più preciso.",
            ),
        ],
        related=["sfumature", "campi-semantici", "registro-formale"],
    ),
    GrammarTopic(
        slug="ironia-italiana",
        title="Ironia e sarcasmo all'italiana",
        level="C1",
        category="Avanzato",
        summary="Capire e usare l'ironia italiana: sfumature culturali e linguistiche.",
        explanation="L'ironia italiana si basa spesso su:\n- **Antifrasi:** dire il contrario di ciò che si pensa. *Che bella giornata!* (quando piove).\n- **Iperbole:** esagerazione. *Ci metto un secondo!* (in realtà 10 minuti).\n- **Understatement:** minimizzare. *Non è niente, solo un graffietto.* (ferita grave).\n- **Tono:** fondamentale per distinguere ironia da affermazione seria.",
        rules=[
            "L'ironia si basa sul contrasto tra detto e inteso.",
            "Il tono di voce è cruciale per segnalare ironia.",
            "Nello scritto si usano punti esclamativi, virgolette.",
            "Attenzione: l'ironia può non essere capita da non nativi.",
        ],
        examples=[
            GrammarExample(
                text="Ma figurati, non vedevo l'ora di passare tre ore in coda alla posta!",
                translation=None,
                note="ironia antifrastica",
            ),
            GrammarExample(
                text="Ah, sei riuscito ad arrivare in orario! Miracolo!",
                translation=None,
                note="ironia bonaria",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Prendere l'ironia alla lettera.",
                correct="Riconoscere l'ironia dal contesto e dal tono.",
                note="L'ironia italiana può essere sottile e confondere.",
            ),
        ],
        related=["umorismo", "doppio-senso", "modi-di-dire"],
    ),
    GrammarTopic(
        slug="umorismo",
        title="Umorismo italiano",
        level="C1",
        category="Avanzato",
        summary="L'umorismo nella cultura italiana: tipologie e caratteristiche.",
        explanation="L'umorismo italiano è variegato:\n- **Giochi di parole:** basati su doppi sensi (*La volpe e l'uva*).\n- **Barzellette:** brevi storie a sorpresa.\n- **Autoironia:** prendere in giro se stessi o la propria città/regione.\n- **Satira:** critica sociale e politica mascherata da umorismo.\n- **Commedia dell'arte:** maschere e stereotipi regionali.",
        rules=[
            "L'umorismo varia per regione e generazione.",
            "I giochi di parole sono molto apprezzati.",
            "L'autoironia è segno di intelligenza e umiltà.",
            "La satira politica è molto diffusa (giornali, TV).",
        ],
        examples=[
            GrammarExample(
                text="Non capisco perché tutti dicano che gli italiani gesticolano... (mentre gesticola vistosamente)",
                translation=None,
                note="autoironia",
            ),
            GrammarExample(
                text="Il milanese e il napoletano si incontrano... (tipica barzelletta regionale)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Non capire l'umorismo regionale.",
                correct="Conoscere gli stereotipi regionali per capire le barzellette.",
                note="Molto umorismo italiano si basa su rivalita regionali.",
            ),
        ],
        related=["ironia-italiana", "doppio-senso", "italiano-regionale"],
    ),
    GrammarTopic(
        slug="doppio-senso",
        title="Doppi sensi e giochi di parole",
        level="C1",
        category="Avanzato",
        summary="Parole e frasi a doppio senso: capire l'ambiguità linguistica italiana.",
        explanation="Il doppio senso si basa su parole con più significati:\n- **Omonimia:** stessa forma, significato diverso. *Il riso* (cereale o azione di ridere).\n- **Polisemia:** stesso termine con accezioni diverse. *La chiave* (strumento o concetto).\n- **Ambiguità sintattica:** *Ho visto un uomo con il binocolo.* (chi aveva il binocolo?)\n\nMolto usato nella pubblicità, nei titoli e nell'umorismo.",
        rules=[
            "Riconoscere parole polisemiche e omonimi.",
            "L'ambiguità può essere voluta (umorismo) o involontaria.",
            "Il contesto di solito chiarisce il significato.",
            "Attenzione ai double entendre involontari in traduzione.",
        ],
        examples=[
            GrammarExample(
                text="Il riso abbonda sulla bocca degli sciocchi. (riso = ridere, ma anche cereale)",
                translation=None,
                note="doppio senso voluto",
            ),
            GrammarExample(
                text="Ho lasciato la chiave sotto lo zerbino. (chiave fisica o soluzione?)",
                translation=None,
                note="polisemia",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Non cogliere il doppio senso in un titolo o barzelletta.",
                correct="Considerare tutti i significati possibili di una parola nel contesto.",
                note="I doppi sensi sono onnipresenti nella comunicazione italiana.",
            ),
        ],
        related=["ironia-italiana", "umorismo", "figure-retoriche"],
    ),
    GrammarTopic(
        slug="figure-retoriche",
        title="Figure retoriche",
        level="C1",
        category="Avanzato",
        summary="Metafora, metonimia, sineddoche, iperbole e altre figure retoriche.",
        explanation="Principali figure retoriche italiane:\n- **Metafora:** sostituzione per analogia. *Quell'uomo è un leone.*\n- **Metonimia:** sostituzione per contiguità. *Bere un bicchiere.* (il contenuto per il contenitore).\n- **Sineddoche:** parte per il tutto. *Tetto* per casa.\n- **Iperbole:** esagerazione. *Te l'ho detto un milione di volte.*\n- **Litote:** negazione del contrario. *Non è male* = è buono.\n- **Eufemismo:** attenuazione. *È passato a miglior vita.*",
        rules=[
            "Metafora: confronto implicito senza come.",
            "Metonimia: relazione di contiguità logica.",
            "Iperbole: esagerazione a effetto.",
            "Litote ed eufemismo attenuano o ammorbidiscono.",
        ],
        examples=[
            GrammarExample(text="Ha un cuore d'oro.", translation=None, note="metafora"),
            GrammarExample(
                text="Non è affatto stupido. (litote per: è molto intelligente)",
                translation=None,
                note="litote",
            ),
            GrammarExample(
                text="Ci vediamo tra due secondi! (iperbole)",
                translation=None,
                note="iperbole",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Confondere metonimia e metafora.",
                correct="Metafora = somiglianza; metonimia = contiguità.",
                note="Bere un bicchiere = metonimia (contenuto x contenitore).",
            ),
        ],
        related=["figure-stilistiche", "doppio-senso", "descrizione-letteraria"],
    ),
    GrammarTopic(
        slug="persuasione",
        title="Tecniche di persuasione",
        level="C1",
        category="Avanzato",
        summary="Strategie linguistiche per persuadere: retorica classica e moderna.",
        explanation="Tecniche persuasive in italiano:\n- **Ethos:** credibilità dell'oratore. *Da esperto del settore, posso affermare che...*\n- **Pathos:** appello alle emozioni. *Pensate ai vostri figli, al loro futuro.*\n- **Logos:** argomentazione logica. *I dati dimostrano che...*\n- **Domanda retorica:** *Vogliamo davvero continuare così?*\n- **Ripetizione (anafora):** *Noi crediamo... Noi vogliamo... Noi possiamo...*",
        rules=[
            "Ethos: stabilire la propria autorità e credibilità.",
            "Pathos: coinvolgere emotivamente l'uditorio.",
            "Logos: usare dati, statistiche, ragionamenti logici.",
            "Domanda retorica e anafora rafforzano il messaggio.",
        ],
        examples=[
            GrammarExample(
                text="Avete mai pensato a cosa significhi per i nostri figli crescere in un mondo senza rispetto per l'ambiente?",
                translation=None,
                note="pathos + domanda retorica",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Usare solo pathos senza dati.",
                correct="Bilanciare ethos, pathos e logos.",
                note="Un discorso persuasivo efficace combina tutte e tre le componenti.",
            ),
        ],
        related=[
            "struttura-argomentativa",
            "controargomentazione",
            "tecniche-oratorie",
        ],
    ),
    GrammarTopic(
        slug="tecniche-oratorie",
        title="Tecniche oratorie",
        level="C1",
        category="Avanzato",
        summary="L'arte del discorso pubblico in italiano: struttura, ritmo e figure.",
        explanation="Tecniche per un discorso efficace:\n- **Exordium:** catturare l'attenzione. Aneddoto, citazione, domanda.\n- **Narratio/Argumentatio:** esporre fatti e argomenti.\n- **Peroratio:** conclusione appassionata.\n- **Pause strategiche:** dare peso alle parole.\n- **Variazione di ritmo:** accelerare per entusiasmo, rallentare per solennità.\n- **Tricolon:** tre elementi in parallelo (*Veni, vidi, vici*).",
        rules=[
            "Apertura forte per catturare l'attenzione.",
            "Struttura chiara in tre parti.",
            "Pause e ritmo per enfatizzare.",
            "Conclusione memorabile.",
        ],
        examples=[
            GrammarExample(
                text="Amici, romani, connazionali... prestatemi orecchio. (Shakespeare in italiano)",
                translation=None,
                note="tricolon + invocazione",
            ),
            GrammarExample(
                text="Una domanda semplice: siete soddisfatti di come vanno le cose? (pausa) Io no. E credo nemmeno voi.",
                translation=None,
                note="domanda retorica + pausa",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Leggere un discorso senza pause ne enfasi.",
                correct="Provare il discorso ad alta voce, segnare le pause.",
                note="L'oratoria è performance, non solo testo.",
            ),
        ],
        related=["persuasione", "struttura-argomentativa", "registro-formale"],
    ),
    GrammarTopic(
        slug="italiano-regionale",
        title="Italiano regionale",
        level="C1",
        category="Avanzato",
        summary="Le varietà regionali dell'italiano: differenze lessicali e grammaticali.",
        explanation="L'italiano regionale varia in:\n- **Lessico:** *anguria* (Nord) vs *cocomero* (Centro) vs *melone d'acqua* (Sud).\n- **Fonetica:** apertura vocali, pronuncia di s e z.\n- **Sintassi:** uso di passato prossimo (Nord) vs passato remoto (Sud).\n- **Geosinonimi:** *papà* vs *babbo*, *ora* vs *adesso*.\n\nLe differenze sono accettate e contribuiscono alla ricchezza dell'italiano.",
        rules=[
            "L'italiano standard è influenzato dalla regione di provenienza.",
            "Geosinonimi: termini diversi per lo stesso oggetto.",
            "Alcune costruzioni regionali sono considerate errori in contesti formali.",
            "La scuola insegna l'italiano standard, ma le varietà regionali persistono.",
        ],
        examples=[
            GrammarExample(
                text="A Milano prendo un caffè, a Napoli prendo un caffè. (pronuncia e preparazione diversa)",
                translation=None,
                note="differenza culturale + linguistica",
            ),
            GrammarExample(
                text="Al Nord: 'Ho visto Marco ieri.' Al Sud: 'Vidi Marco ieri.'",
                translation=None,
                note="passato prossimo vs remoto",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Pensare che l'italiano sia uniforme in tutta Italia.",
                correct="Riconoscere e apprezzare le varietà regionali.",
                note="L'Italia ha una straordinaria diversita linguistica interna.",
            ),
        ],
        related=["dialetti", "italiano-standard", "modi-di-dire"],
    ),
    GrammarTopic(
        slug="dialetti",
        title="Dialetti italiani",
        level="C1",
        category="Avanzato",
        summary="Conoscere i principali dialetti italiani e il loro rapporto con l'italiano standard.",
        explanation="I dialetti italiani non sono varianti dell'italiano ma lingue sorelle derivate dal latino.\n\nGruppi principali:\n- **Gallo-italici:** piemontese, lombardo, ligure, emiliano-romagnolo.\n- **Veneti:** veneziano, veronese.\n- **Toscani:** fiorentino (base dell'italiano standard).\n- **Mediani:** romanesco, umbro, marchigiano.\n- **Meridionali:** napoletano, pugliese, calabrese, siciliano.\n- **Sardo:** considerato lingua a se.\n\nMolti italiani sono bilingui (italiano + dialetto).",
        rules=[
            "I dialetti sono lingue autonome, non varianti degradate.",
            "L'italiano standard deriva dal fiorentino del Trecento.",
            "In contesti formali si usa l'italiano; in famiglia spesso il dialetto.",
            "Il dialetto è patrimonio culturale protetto.",
        ],
        examples=[
            GrammarExample(
                text="In veneto: 'Come xeo che la va?' (Come va?)",
                translation=None,
            ),
            GrammarExample(
                text="A Napoli: 'Sto buono, guaglio!' (Stai bene, ragazzo!)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Confondere dialetto con italiano sgrammaticato.",
                correct="Il dialetto ha regole grammaticali proprie e una storia antica.",
                note="I dialetti italiani sono lingue romanze con pari dignita.",
            ),
        ],
        related=["italiano-regionale", "italiano-standard", "evoluzione-linguistica"],
    ),
    GrammarTopic(
        slug="italiano-standard",
        title="Italiano standard e neostandard",
        level="C1",
        category="Avanzato",
        summary="L'evoluzione dell'italiano standard verso un neostandard più flessibile.",
        explanation="L'italiano standard tradizionale è quello normativo (grammatiche, Accademia della Crusca).\n\nL'italiano **neostandard** (o dell'uso medio) accetta:\n- **gli** per a loro (invece di loro).\n- **lui/lei** soggetto (invece di egli/ella).\n- **che** polivalente (temporale, causale).\n- **ci** con avere: *c'ho fame* (colloquiale).\n- **dislocazioni:** *Il caffè, lo prendo dopo.*\n\nQueste forme, un tempo considerate errori, sono ora accettate nell'uso comune.",
        rules=[
            "L'italiano standard è quello delle grammatiche.",
            "Il neostandard accoglie fenomeni del parlato.",
            "Alcune forme neostandard sono ancora evitate nello scritto formale.",
            "La lingua evolve: oggi è normale ciò che ieri era errore.",
        ],
        examples=[
            GrammarExample(
                text="Standard: Ho telefonato loro. / Neostandard: Gli ho telefonato.",
                translation=None,
            ),
            GrammarExample(
                text="Standard: Il libro che ho comprato. / Neostandard: Il libro che l'ho comprato.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Considerare sempre errore le forme neostandard.",
                correct="Distinguere tra registri: accettabile nel parlato, evitare nello scritto formale.",
                note="Il confine tra errore e innovazione linguistica è fluido.",
            ),
        ],
        related=["italiano-regionale", "registro-formale", "evoluzione-linguistica"],
    ),
    GrammarTopic(
        slug="sintesi-testuale",
        title="Sintesi testuale",
        level="C1",
        category="Avanzato",
        summary="Tecniche per riassumere e sintetizzare testi complessi in italiano.",
        explanation="Per una buona sintesi:\n1. **Lettura analitica:** individuare tesi, argomenti, conclusione.\n2. **Gerarchizzare:** distinguere essenziale da accessorio.\n3. **Parafrasare:** riformulare con parole proprie.\n4. **Eliminare:** esempi ridondanti, digressioni, ripetizioni.\n5. **Unificare:** fondere concetti simili.\n6. **Mantenere il registro e lo stile originale.**",
        rules=[
            "Identificare la struttura del testo originale.",
            "Isolare le idee principali.",
            "Riformulare senza tradire il significato.",
            "Mantenere coesione e coerenza.",
        ],
        examples=[
            GrammarExample(
                text="Riassunto di 300 parole: il testo originale analizza le cause del declino economico italiano identificando tre fattori: demografia, produttività e debito pubblico.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Copiare frasi intere dall'originale.",
                correct="Riformulare con parole proprie, condensando.",
                note="La sintesi non è un collage di citazioni.",
            ),
        ],
        related=["coesione-testuale", "riformulazione", "critica-costruttiva"],
    ),
    GrammarTopic(
        slug="critica-costruttiva",
        title="Critica costruttiva",
        level="C1",
        category="Avanzato",
        summary="Esprimere critiche in modo costruttivo e diplomatico in italiano.",
        explanation="Per esprimere critiche costruttive:\n- **Ammorbidire:** *Forse si potrebbe...*\n- **Condizionale:** *Sarebbe meglio se...*\n- **Domanda invece di affermazione:** *Hai considerato la possibilità di...?*\n- **Sandwich feedback:** positivo - critica - positivo.\n- **Evitare assoluti:** mai dire *sempre* o *mai*.",
        rules=[
            "Usare il condizionale per attenuare.",
            "Evitare toni accusatori.",
            "Concentrarsi sul problema, non sulla persona.",
            "Proporre alternative, non solo criticare.",
        ],
        examples=[
            GrammarExample(
                text="Il tuo lavoro è molto interessante. Forse si potrebbe approfondire la parte sui dati. Nel complesso, ottimo lavoro!",
                translation=None,
                note="sandwich feedback",
            ),
            GrammarExample(
                text="Hai considerato di strutturare diversamente questa sezione? Renderebbe il tutto più chiaro.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Questo lavoro è sbagliato. Devi rifarlo.",
                correct="Questo lavoro ha alcuni punti da rivedere. Vediamoli insieme per migliorarlo.",
                note="La critica costruttiva offre soluzioni, non solo giudizi.",
            ),
        ],
        related=["riformulazione", "condizionale-cortesia", "registro-formale"],
    ),
    GrammarTopic(
        slug="riformulazione",
        title="Riformulazione e parafrasi",
        level="C1",
        category="Avanzato",
        summary="Tecniche per riformulare concetti in modo chiaro e preciso.",
        explanation="Riformulare significa esprimere lo stesso concetto con parole diverse.\n\nTecniche:\n- **Sinonimi:** *l'edificio → la costruzione, lo stabile.*\n- **Cambio di categoria:** *Analizzare → fare un'analisi.*\n- **Da attivo a passivo:** *Il governo ha approvato → È stata approvata dal governo.*\n- **Da specifico a generale:** *Il gatto → l'animale domestico.*\n- **Definizione:** *Un cardiologo → un medico specializzato nel cuore.*",
        rules=[
            "Mantenere il significato originale.",
            "Variare lessico e struttura sintattica.",
            "Adeguare il registro al nuovo contesto.",
            "Utile per evitare ripetizioni nella scrittura.",
        ],
        examples=[
            GrammarExample(
                text="Originale: La crisi economica ha colpito duramente le famiglie. Riformulato: I nuclei familiari hanno subito pesantemente gli effetti della recessione.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Cambiare il significato durante la riformulazione.",
                correct="Verificare che il messaggio originale sia preservato.",
                note="La riformulazione non deve alterare il contenuto.",
            ),
        ],
        related=["sintesi-testuale", "precisione-lessicale", "sfumature"],
    ),
    GrammarTopic(
        slug="passivo-accademico",
        title="Il passivo nel registro accademico e formale",
        level="C1",
        category="Avanzato",
        summary="Uso della forma passiva per conferire oggettività e impersonalità alla scrittura accademica.",
        explanation="Nel registro accademico e formale, la **forma passiva** è ampiamente utilizzata per conferire oggettività e impersonalità al discorso.\n\n- **Si passivante**: *Si analizzeranno i dati raccolti.* → equivalente a *I dati raccolti saranno analizzati.*\n- **Passivo con essere/venire**: *Il fenomeno è stato osservato / venne studiato.*\n- **Andare + participio** (obbligo): *I risultati vanno interpretati con cautela.*\n\n**Strategie di impersonalità accademica:**\n- Uso del *si* impersonale: *Si ritiene che...*\n- Costruzioni con *è/sembra/risulta + aggettivo + che*: *È evidente che..., Risulta chiaro che...*\n- Forme nominali: *L'analisi dei dati mostra...* piuttosto che *Abbiamo analizzato i dati...*\n\nIl passivo accademico permette di mettere in primo piano il contenuto della ricerca piuttosto che il ricercatore.",
        rules=[
            "Il passivo sposta il focus dall'agente all'azione o al risultato.",
            "Essere ammette anche tempi composti; venire passivo e andare con valore di obbligo si usano nei tempi semplici.",
            "Costruzioni impersonali con si: si osserva, si nota, si evince.",
            "Evitare la prima persona (io/noi) nella scrittura accademica formale.",
            'Usare forme nominali per oggettività: "l\'analisi rivela" invece di "abbiamo analizzato".',
        ],
        examples=[
            GrammarExample(
                text="I dati sono stati raccolti mediante un questionario anonimo.",
                translation=None,
                note="passivo con essere",
            ),
            GrammarExample(
                text="Si è osservato un aumento significativo dei casi.",
                translation=None,
                note="si passivante",
            ),
            GrammarExample(
                text="I risultati vanno interpretati alla luce del contesto storico.",
                translation=None,
                note="andare + participio (obbligo)",
            ),
            GrammarExample(
                text="È emerso che la maggioranza degli intervistati preferisce...",
                translation=None,
                note="costruzione impersonale",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Abbiamo scoperto che il fenomeno è frequente.",
                correct="È emerso che il fenomeno risulta frequente.",
                note="Evitare la prima persona nel registro accademico.",
            ),
            GrammarMistake(
                wrong="Si è analizzato i dati.",
                correct="Si sono analizzati i dati.",
                note="Il si passivante richiede accordo col soggetto.",
            ),
        ],
        related=["nominalizzazione", "si-passivante", "impersonalita"],
    ),
]
