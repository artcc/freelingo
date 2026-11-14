"""Finnish A2 placement: grammar, contextual vocabulary and short texts."""

from app.data._types import AssessmentQuestion

A2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "g-a2-001",
        "grammar",
        "A2",
        "Täydennä: Odotan ___ oven edessä.",
        ["kaupan", "kauppan", "kauppaa", "kaupoista"],
        "kaupan",
        "fi-gradation-a2",
    ),
    AssessmentQuestion(
        "g-a2-002",
        "grammar",
        "A2",
        "Täydennä yleiskielinen lause: Tässä kaupassa on paljon ___.",
        ["uudet kengät", "uutta kenkää", "uusia kenkiä", "uusiin kenkiin"],
        "uusia kenkiä",
        "fi-plural-partitive-a2",
    ),
    AssessmentQuestion(
        "g-a2-003",
        "grammar",
        "A2",
        "Matkustat ystävän autossa etkä tarvitse junamatkaa. Täydennä: En osta ___.",
        ["lipun", "lippua", "lippu", "lipussa"],
        "lippua",
        "fi-object-a2",
    ),
    AssessmentQuestion(
        "g-a2-004",
        "grammar",
        "A2",
        "Kerro eilisestä: Me emme ___ kokoukseen.",
        ["tuli", "tulimme", "tullut", "tulleet"],
        "tulleet",
        "fi-negative-past-a2",
    ),
    AssessmentQuestion(
        "g-a2-005",
        "grammar",
        "A2",
        "Kerro kokemuksestasi perfektissä: Olen ___ kerran Lapissa.",
        ["kävin", "käyn", "käynyt", "käydä"],
        "käynyt",
        "fi-perfect-a2",
    ),
    AssessmentQuestion(
        "g-a2-006",
        "grammar",
        "A2",
        "Kerro omasta velvollisuudestasi: ___ täytyy lähteä töihin.",
        ["Minun", "Minä", "Minua", "Minuun"],
        "Minun",
        "fi-necessity-a2",
    ),
    AssessmentQuestion(
        "g-a2-007",
        "grammar",
        "A2",
        "Olet lähdössä uimahalliin. Täydennä: Menen sinne ___.",
        ["uida", "uin", "uimassa", "uimaan"],
        "uimaan",
        "fi-infinitives-a2",
    ),
    AssessmentQuestion(
        "g-a2-008",
        "grammar",
        "A2",
        "Sää on epävarma. Haluat sanoa, että retki toteutuu vain hyvällä säällä. "
        "Täydennä: Lähdemme retkelle, ___ sää on hyvä.",
        ["vaikka", "jos", "että", "mutta"],
        "jos",
        "fi-subordination-a2",
    ),
    AssessmentQuestion(
        "v-a2-001",
        "vocabulary",
        "A2",
        "Asut toisen omistamassa asunnossa ja maksat siitä joka kuukausi. Mitä maksat?",
        ["Palkkaa.", "Vuokraa.", "Alennusta.", "Annosta."],
        "Vuokraa.",
    ),
    AssessmentQuestion(
        "v-a2-002",
        "vocabulary",
        "A2",
        "Haluat tietää, sopiiko takki sinulle, ennen kuin maksat. Mitä pyydät?",
        [
            "Voinko varata ajan?",
            "Voinko palauttaa kuitin?",
            "Voinko perua matkan?",
            "Voinko sovittaa takkia?",
        ],
        "Voinko sovittaa takkia?",
    ),
    AssessmentQuestion(
        "v-a2-003",
        "vocabulary",
        "A2",
        "Junasi lähtee kahden minuutin päästä ja olet vielä kaukana asemasta. " "Mitä pelkäät?",
        ["Myöhästymistä.", "Valmistumista.", "Muuttamista.", "Toipumista."],
        "Myöhästymistä.",
    ),
    AssessmentQuestion(
        "v-a2-004",
        "vocabulary",
        "A2",
        "Yritys haluaa tavata sinut ja kysyä työkokemuksestasi ennen valintaa. "
        "Mihin olet menossa?",
        ["Kokeeseen.", "Näyttelyyn.", "Haastatteluun.", "Muuttoon."],
        "Haastatteluun.",
    ),
    AssessmentQuestion(
        "v-a2-005",
        "vocabulary",
        "A2",
        "Lääkäri määrää lääkkeen, jota ei saa apteekista ilman määräystä. Mitä tarvitset?",
        ["Tutkinnon.", "Hakemuksen.", "Vuokrasopimuksen.", "Reseptin."],
        "Reseptin.",
    ),
    AssessmentQuestion(
        "v-a2-006",
        "vocabulary",
        "A2",
        "Lähdette metsään koko päiväksi eikä reitillä ole kahvilaa. "
        "Mitä otatte mukaan syötäväksi?",
        ["Verhot.", "Eväät.", "Luistimet.", "Muistiinpanot."],
        "Eväät.",
    ),
    AssessmentQuestion(
        "v-a2-007",
        "vocabulary",
        "A2",
        "Ystävä ehdottaa lauantaita ja sinulle sopii sunnuntai. Haluat löytää yhteisen ajan. "
        "Mitä sanot?",
        ["Unohdin lauantain.", "Olen perillä.", "Sopiiko sunnuntai?", "Kiitos neuvosta."],
        "Sopiiko sunnuntai?",
    ),
    AssessmentQuestion(
        "v-a2-008",
        "vocabulary",
        "A2",
        "Et tiedä, saatko käyttää työpaikan autoa omaan matkaan. Mitä kysyt?",
        [
            "Onko minulla lupa käyttää autoa?",
            "Mikä on auton väri?",
            "Onko autossa tilaa laukulle?",
            "Mistä auto on ostettu?",
        ],
        "Onko minulla lupa käyttää autoa?",
    ),
    AssessmentQuestion(
        "r-a2-001",
        "reading",
        "A2",
        "Vuokrailmoitus: Asunto on vapaa joulukuun alusta. Vuokranantajalle maksetaan vuokra "
        "680 euroa ja vesimaksu 20 euroa henkilöltä kuukaudessa. "
        "Sähkösopimuksen tekee asukas itse. "
        "Mitä yksi asukas maksaa vuokranantajalle kuukaudessa?",
        [
            "680 euroa ja kaikki sähkömaksut.",
            "720 euroa ilman sähköä.",
            "700 euroa ilman sähköä.",
            "700 euroa, myös sähkö sisältyy siihen.",
        ],
        "700 euroa ilman sähköä.",
    ),
    AssessmentQuestion(
        "r-a2-002",
        "reading",
        "A2",
        "Viesti: Kokous siirtyy tiistailta keskiviikolle. Aloitamme edelleen klo 10, "
        "mutta tapaamme huoneessa 5 emmekä huoneessa 2. Mikä pysyy ennallaan?",
        ["Aloitusaika.", "Viikonpäivä.", "Huone.", "Sekä huone että päivä."],
        "Aloitusaika.",
    ),
    AssessmentQuestion(
        "r-a2-003",
        "reading",
        "A2",
        "Aino kirjoittaa: Olen ostanut retkiliput, mutta en ole vielä varannut majoitusta. "
        "Soitan hotelliin huomenna. Eero, voitko tarkistaa bussin lähtöajan? "
        "Mitä Eerolta pyydetään nyt?",
        [
            "Huoneen varaamista.",
            "Retkilippujen ostamista.",
            "Hotelliin soittamista.",
            "Aikataulun tarkistamista.",
        ],
        "Aikataulun tarkistamista.",
    ),
    AssessmentQuestion(
        "r-a2-004",
        "reading",
        "A2",
        "Ohje: Jos et pääse vastaanotolle, peru aika viimeistään edellisenä päivänä klo 12. "
        "Eerolla on aika torstaina klo 9, mutta hän on silloin matkalla. "
        "Mikä näistä perumisajoista on ohjeen mukainen?",
        ["Keskiviikkona klo 15.", "Keskiviikkona klo 10.", "Torstaina klo 8.", "Torstaina klo 10."],
        "Keskiviikkona klo 10.",
    ),
]
