"""Danish A1 phrases with practical contexts and stable unit references."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "da-introductions-a1",
        "A1",
        "Hilse og forstå hinanden",
        "👋",
        [
            PhrasebookEntry(
                "Hej, jeg hedder Amina.",
                "Præsenter dig; brug dit eget navn.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Hvad hedder du?", "Spørg en person om navnet.", "neutral", "a1-unit-1"
            ),
            PhrasebookEntry(
                "Hyggeligt at møde dig.",
                "Sig noget venligt ved den første præsentation.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Jeg lærer dansk.",
                "Forklar kort, hvorfor du måske taler langsomt.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Kan du sige det igen?",
                "Bed om gentagelse, når du ikke hører eller forstår.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Vil du tale lidt langsommere?",
                "Bed venligt om et lavere taletempo.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Hvordan staver du dit navn?",
                "Bed om bogstaverne, så du kan skrive navnet.",
                "neutral",
                "a1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-people-a1",
        "A1",
        "Familie, venner og ejendele",
        "🏠",
        [
            PhrasebookEntry(
                "Det er min ven Jonas.",
                "Præsenter en ven for en anden person.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Jeg bor sammen med min søster.",
                "Fortæl, hvem du deler bolig med; tilpas personen.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Jeg har to børn.",
                "Fortæl kort om din familie; tilpas antallet.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Er det din taske?",
                "Kontroller, hvem en taske tilhører.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Nej, den er ikke min.",
                "Svar om en nævnt taske, der tilhører en anden.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Hvor er mine nøgler?",
                "Spørg efter dine nøgler derhjemme.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Sikke et fint værelse!",
                "Sig noget positivt, når du ser en andens værelse.",
                "informal",
                "a1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-time-a1",
        "A1",
        "Klokken og hverdagsaftaler",
        "🕘",
        [
            PhrasebookEntry("Hvad er klokken?", "Spørg om tiden lige nu.", "neutral", "a1-unit-3"),
            PhrasebookEntry(
                "Hvornår begynder vi?",
                "Spørg om starttidspunktet for en aktivitet.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Jeg møder klokken halv otte.",
                "Fortæl, at din arbejdsdag begynder 7.30; gør tidspunktet tydeligt.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Jeg arbejder ikke om søndagen.",
                "Fortæl om en fast fridag.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Passer det klokken ti?",
                "Foreslå et tidspunkt og bed om bekræftelse.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Kan du skrive tidspunktet?",
                "Bed om en skriftlig tid, hvis du er usikker på tallet.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Vi ses i morgen!",
                "Afslut en samtale, når I allerede har en aftale næste dag.",
                "informal",
                "a1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-food-a1",
        "A1",
        "Bestille og købe mad",
        "🥖",
        [
            PhrasebookEntry(
                "Jeg vil gerne have to boller.",
                "Bestil hos bageren; tilpas antallet.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "En kop kaffe, tak.",
                "Bestil en drik ved disken.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Må jeg få lidt vand?",
                "Bed om vand ved et måltid.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Hvad koster det?",
                "Spørg om prisen på en vare, du viser.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Er der mælk i?",
                "Spørg til indholdet i en bestemt ret eller drik.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Jeg spiser ikke kød.",
                "Oplys om et madvalg, når du bestiller.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Det var det hele, tak.",
                "Sig, at du ikke ønsker flere varer.",
                "neutral",
                "a1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-directions-a1",
        "A1",
        "På vej i byen",
        "🚌",
        [
            PhrasebookEntry(
                "Undskyld, hvor ligger stationen?",
                "Få kontakt og spørg om vej.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Er der et toilet her?",
                "Spørg, om stedet har et toilet, du kan bruge.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Går denne bus til centrum?",
                "Kontroller destinationen, før du stiger på.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Hvor skal jeg stå af?",
                "Spørg om stoppestedet til dit mål.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Gå ligeud og drej til venstre.",
                "Giv en kort vejbeskrivelse.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Er der langt at gå?",
                "Spørg til afstanden til fods.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Kan du vise det på kortet?",
                "Bed personen udpege stedet på et kort.",
                "neutral",
                "a1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-leisure-a1",
        "A1",
        "Invitere og være sammen",
        "☕",
        [
            PhrasebookEntry(
                "Har du lyst til en kop kaffe?",
                "Inviter til en kort, uformel pause.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Skal vi gå en tur?",
                "Foreslå en fælles aktivitet.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Ja tak, det vil jeg gerne.",
                "Tag imod en invitation.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Jeg kan ikke i dag.",
                "Afslå en invitation til samme dag.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Hvad med på lørdag?",
                "Foreslå en anden dag.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Vent lige på mig!",
                "Bed venner vente et øjeblik, før I går videre.",
                "informal",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Tak for i dag!",
                "Sig farvel efter en fælles aktivitet.",
                "neutral",
                "a1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-help-a1",
        "A1",
        "Hjælp og små problemer",
        "🩹",
        [
            PhrasebookEntry(
                "Kan du hjælpe mig?",
                "Bed en person om hjælp med et konkret problem.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Jeg kan ikke finde min taske.",
                "Forklar, hvad du leder efter.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Jeg har ondt i maven.",
                "Beskriv, hvor smerten er, uden at stille en diagnose.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Jeg vil gerne bestille en tid.",
                "Indled en samtale med lægens reception.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Jeg var også syg i går.",
                "Fortæl kort, at problemet ikke kun gælder i dag.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Kan jeg betale med kort?",
                "Spørg om betalingsmuligheden i en butik.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Må jeg få en kvittering?",
                "Bed om et bevis på betalingen.",
                "neutral",
                "a1-unit-7",
            ),
        ],
    ),
]
