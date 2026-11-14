"""Danish A2 phrases for practical negotiation and connected interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "da-travel-a2",
        "A2",
        "Rejseplaner og forsinkelser",
        "🚆",
        [
            PhrasebookEntry(
                "Skal jeg skifte tog undervejs?",
                "Kontroller, om rejsen er direkte.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Kan jeg nå forbindelsen i Fredericia?",
                "Spørg om et bestemt skift, når dit tog er forsinket.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Gælder min billet til den næste afgang?",
                "Undersøg billettens gyldighed efter en ændring.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Jeg har reserveret et værelse i to nætter.",
                "Fortæl receptionen om din reservation.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Er morgenmad med i prisen?",
                "Afklar, hvad overnatningen omfatter.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Vi bliver lidt forsinkede, men vi kommer i aften.",
                "Giv overnatningsstedet besked om senere ankomst.",
                "neutral",
                "a2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-housing-a2",
        "A2",
        "Spørge til boligen og melde fejl",
        "🔑",
        [
            PhrasebookEntry(
                "Er varme og vand med i huslejen?",
                "Afklar løbende udgifter, før du vælger en bolig.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Hvornår kan jeg flytte ind?",
                "Spørg udlejeren om boligens tilgængelighed.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Den lille vandhane i badeværelset drypper.",
                "Beskriv præcist, hvilken installation der har et problem.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Kan vi aftale en tid til reparationen?",
                "Find et tidspunkt, hvor nogen kan få adgang til boligen.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Vil du skrue lidt ned for musikken?",
                "Bed en nabo dæmpe lyden.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Denne bolig er billigere, men der er længere til arbejdet.",
                "Sammenlign to muligheder ud fra både pris og transport.",
                "neutral",
                "a2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-health-a2",
        "A2",
        "Lægebesøg og ændrede aftaler",
        "🩺",
        [
            PhrasebookEntry(
                "Jeg har haft ondt i halsen siden mandag.",
                "Beskriv symptomets varighed ved en lægesamtale.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Det gør mest ondt, når jeg går.",
                "Forklar, hvilken aktivitet der hænger sammen med smerten.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Jeg vil gerne ændre min tid, fordi jeg ikke kan komme.",
                "Forklar en ændring uden at give unødvendige personlige oplysninger.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Er der en ledig tid senere på dagen?",
                "Spørg efter et alternativ, der passer bedre.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Hvordan skal jeg tage medicinen?",
                "Bed behandleren forklare den konkrete anvisning.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Hvornår skal jeg kontakte jer igen?",
                "Afklar med behandleren, hvordan du følger op.",
                "neutral",
                "a2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-work-study-a2",
        "A2",
        "Opgaver og information på arbejde eller kursus",
        "📚",
        [
            PhrasebookEntry(
                "Kan du fortælle mig, hvornår mødet slutter?",
                "Spørg indirekte om et mødes sluttidspunkt.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Jeg er ikke sikker på, hvad jeg skal gøre først.",
                "Forklar, at opgavens rækkefølge er uklar.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Er det den fil, som du sendte i går?",
                "Kontroller, at I arbejder med samme dokument.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Jeg prøver at blive færdig inden frokost.",
                "Beskriv dit mål uden at love, at opgaven er klar.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Kan vi bytte vagt på fredag?",
                "Spørg en kollega om en konkret ændring i arbejdsplanen.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Tak for din besked. Jeg sender dokumentet i morgen.",
                "Svar kort og sagligt i en arbejdsrelateret mail.",
                "neutral",
                "a2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-shopping-a2",
        "A2",
        "Bytte varer og følge en bestilling",
        "🛍️",
        [
            PhrasebookEntry(
                "Jeg købte den her for tre dage siden.",
                "Oplys købstidspunktet, når du henvender dig om en vare.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Kan jeg bytte den til en større størrelse?",
                "Spørg efter samme vare i en anden størrelse.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Den virker ikke, og jeg har bonen med.",
                "Beskriv en fejl og vis, at du kan dokumentere købet.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Hvornår får jeg pengene tilbage?",
                "Spørg til tidspunktet efter en aftalt tilbagebetaling.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Jeg har ikke fået nogen bekræftelse endnu.",
                "Forklar, at en forventet besked efter en bestilling mangler.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Kan I undersøge, hvor min pakke er?",
                "Bed kundeservice finde oplysninger om en forsendelse.",
                "neutral",
                "a2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-community-a2",
        "A2",
        "Deltage og lave aftaler",
        "🤝",
        [
            PhrasebookEntry(
                "Jeg vil gerne melde mig til holdet.",
                "Spørg om at deltage regelmæssigt i en aktivitet.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Skal jeg selv have udstyr med?",
                "Afklar, hvad du skal medbringe første gang.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Kan vi hjælpe hinanden med at rydde op?",
                "Foreslå en fælles praktisk opgave efter en aktivitet.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Jeg tager gerne en salat med.",
                "Tilbyd et bidrag til en fælles middag.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Tak for invitationen, men jeg kan desværre ikke den dag.",
                "Afslå en invitation venligt uden at opfinde en begrundelse.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Skal vi finde en anden dag?",
                "Foreslå, at I laver en ny aftale.",
                "neutral",
                "a2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-services-a2",
        "A2",
        "Blanketter, beskeder og hjælp",
        "📄",
        [
            PhrasebookEntry(
                "Hvilke dokumenter skal jeg tage med?",
                "Forbered et besøg hos borgerservice.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Jeg har brug for hjælp til at udfylde blanketten.",
                "Bed om praktisk hjælp til felterne i et dokument.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Bliver dokumentet sendt med digital post?",
                "Afklar, hvor du skal lede efter svaret.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Hvad gør jeg, hvis hjemmesiden ikke virker?",
                "Spørg efter en løsning, hvis den digitale vej er lukket.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Hvornår bliver affaldet hentet?",
                "Spørg om den lokale afhentning.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Vil I bekræfte, at I har modtaget dokumenterne?",
                "Bed skriftligt om en kvittering for indsendte papirer.",
                "formal",
                "a2-unit-7",
            ),
        ],
    ),
]
