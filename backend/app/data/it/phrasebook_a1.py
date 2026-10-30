"""Italian phrasebook — A1 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="greetings",
        level="A1",
        situation="Saluti e presentazioni",
        icon="\U0001f44b",
        phrases=[
            PhrasebookEntry(text="Ciao!", context="Saluto informale", register="informal"),
            PhrasebookEntry(
                text="Buongiorno.",
                context="Saluto durante la prima parte della giornata, anche in contesti informali",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Buon pomeriggio.",
                context="Saluto nel pomeriggio",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Buonasera.",
                context="Saluto dal pomeriggio o dalla sera, secondo gli usi locali",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Come stai?",
                context="Chiedere come sta qualcuno (informale)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Come sta?",
                context="Chiedere come sta qualcuno (formale)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Sto bene, grazie. E tu?",
                context="Rispondere e ricambiare (informale)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Sto bene, grazie. E Lei?",
                context="Rispondere e ricambiare (formale)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Piacere di conoscerti.",
                context="Al primo incontro (informale)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Piacere di conoscerLa.",
                context="Al primo incontro (formale)",
                register="formal",
            ),
            PhrasebookEntry(text="Mi chiamo Marco.", context="Presentarsi", register="neutral"),
            PhrasebookEntry(
                text="Di dove sei?",
                context="Chiedere la provenienza (informale)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Sono italiano / italiana.",
                context="Indicare la nazionalit\u00e0",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Arrivederci!",
                context="Congedo comune, anche in situazioni formali",
                register="neutral",
            ),
            PhrasebookEntry(text="A presto!", context="Congedo informale", register="informal"),
        ],
    ),
    PhrasebookCategory(
        id="basic_requests",
        level="A1",
        situation="Richieste di base e cortesia",
        icon="\U0001f64f",
        phrases=[
            PhrasebookEntry(
                text="Per favore.",
                context="Chiedere qualcosa educatamente",
                register="neutral",
            ),
            PhrasebookEntry(text="Grazie.", context="Ringraziare", register="neutral"),
            PhrasebookEntry(
                text="Grazie mille!",
                context="Ringraziare con enfasi",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Prego.",
                context="Rispondere a un ringraziamento",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Scusa.", context="Chiedere scusa (informale)", register="informal"
            ),
            PhrasebookEntry(
                text="Mi scusi.", context="Chiedere scusa (formale)", register="formal"
            ),
            PhrasebookEntry(
                text="Mi dispiace.", context="Esprimere dispiacere", register="neutral"
            ),
            PhrasebookEntry(
                text="Non c'\u00e8 problema.",
                context="Rassicurare dopo delle scuse",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Puoi aiutarmi?",
                context="Chiedere aiuto (informale)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Pu\u00f2 aiutarmi?",
                context="Chiedere aiuto (formale)",
                register="formal",
            ),
            PhrasebookEntry(
                text="Posso...?",
                context="Chiedere il permesso (es: Posso entrare?)",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Non capisco.",
                context="Indicare che non si capisce",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="numbers_time_a1",
        level="A1",
        situation="Numeri e ora",
        icon="\U0001f552",
        phrases=[
            PhrasebookEntry(text="Che ora \u00e8?", context="Chiedere l'ora", register="neutral"),
            PhrasebookEntry(text="Sono le tre.", context="Dire l'ora esatta", register="neutral"),
            PhrasebookEntry(
                text="\u00c8 l'una.",
                context="Dire l'una (singolare)",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Sono le tre e mezza.",
                context="Dire la mezz'ora",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Sono le quattro meno un quarto.",
                context='Dire l\'ora con "meno"',
                register="neutral",
            ),
            PhrasebookEntry(
                text="A che ora parte?",
                context="Chiedere l'orario di partenza",
                register="neutral",
            ),
            PhrasebookEntry(text="Quanto costa?", context="Chiedere il prezzo", register="neutral"),
            PhrasebookEntry(
                text="Costa dieci euro.",
                context="Indicare il prezzo",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Quanti anni hai?",
                context="Chiedere l'et\u00e0 (informale)",
                register="informal",
            ),
            PhrasebookEntry(
                text="Che ora \u00e8? \u2014 Sono le [ora].",
                context="Chiedere e dire l'ora",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="shopping_basic_a1",
        level="A1",
        situation="Fare acquisti",
        icon="\U0001f6cd\ufe0f",
        phrases=[
            PhrasebookEntry(text="Quanto costa?", context="Chiedere il prezzo", register="neutral"),
            PhrasebookEntry(
                text="\u00c8 troppo caro.",
                context="Dire che qualcosa \u00e8 costoso",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Avete qualcosa di pi\u00f9 economico?",
                context="Chiedere un'alternativa meno cara",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Posso pagare con la carta?",
                context="Chiedere se accettano carte",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Pago in contanti.",
                context="Indicare pagamento in contanti",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Mi d\u00e0 uno scontrino, per favore?",
                context="Chiedere lo scontrino",
                register="formal",
            ),
            PhrasebookEntry(
                text="Che taglia porta?",
                context="Chiedere la taglia (negozio abbigliamento)",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Posso provarlo?",
                context="Chiedere di provare un capo",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Avete questo in un altro colore?",
                context="Chiedere varianti di colore",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Prendo questo, grazie.",
                context="Confermare l'acquisto",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="asking_directions_a1",
        level="A1",
        situation="Chiedere indicazioni",
        icon="\U0001f5fa\ufe0f",
        phrases=[
            PhrasebookEntry(
                text="Scusi, dov'\u00e8 la stazione?",
                context="Chiedere dove si trova un luogo",
                register="formal",
            ),
            PhrasebookEntry(
                text="\u00c8 lontano?",
                context="Chiedere se un luogo \u00e8 distante",
                register="neutral",
            ),
            PhrasebookEntry(
                text="\u00c8 qui vicino.",
                context="Rispondere che \u00e8 vicino",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Gira a destra.",
                context="Dare indicazione: destra",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Gira a sinistra.",
                context="Dare indicazione: sinistra",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Va' sempre dritto.",
                context="Dare indicazione: dritto",
                register="informal",
            ),
            PhrasebookEntry(
                text="\u00c8 all'angolo.",
                context="Indicare la posizione all'angolo",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Dov'\u00e8 il bagno?",
                context="Chiedere del bagno",
                register="neutral",
            ),
            PhrasebookEntry(
                text="C'\u00e8 una farmacia qui vicino?",
                context="Chiedere di un servizio specifico",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Mi sono perso / persa.",
                context="Dire che ci si \u00e8 persi",
                register="neutral",
            ),
        ],
    ),
]
