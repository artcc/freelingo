"""Dutch A1 practical exchanges."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="kennismaken_a1",
        level="A1",
        situation="Kennismaken en hulp bij taal",
        icon="👋",
        phrases=[
            PhrasebookEntry(
                "Hallo, ik heet Noor. Hoe heet jij?",
                "Een eerste informeel contact leggen.",
                "informal",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Goedemorgen, mijn naam is Sam de Vries.",
                "Jezelf voorstellen bij een afspraak.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Aangenaam kennis te maken.",
                "Beleefd reageren op een voorstelling.",
                "formal",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Kunt u wat langzamer spreken?",
                "Om een lager spreektempo vragen.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Hoe schrijf je dat?",
                "Naar de spelling van een woord vragen.",
                "informal",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Dit is mijn zus. Zij woont in Leiden.",
                "Een familielid voorstellen.",
                "neutral",
                "a1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="bestellen_a1",
        level="A1",
        situation="Bestellen en betalen",
        icon="☕",
        phrases=[
            PhrasebookEntry(
                "Mag ik een koffie, alstublieft?", "Een drankje bestellen.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Ik wil graag water zonder prik.",
                "Aangeven dat je geen koolzuur wilt.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Zit er melk in?", "Naar een ingrediënt vragen.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Voor mij geen suiker, dank u.",
                "Een voorkeur bij de bestelling aangeven.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry("Hoeveel kost dit?", "Naar een prijs vragen.", "neutral", "a1-unit-7"),
            PhrasebookEntry(
                "Kan ik met mijn pinpas betalen?",
                "De betaalmogelijkheid controleren.",
                "neutral",
                "a1-unit-7",
            ),
        ],
    ),
    PhrasebookCategory(
        id="onderweg_a1",
        level="A1",
        situation="De weg en de tijd vragen",
        icon="🚉",
        phrases=[
            PhrasebookEntry(
                "Pardon, waar is het station?",
                "Een onbekende om de weg vragen.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Is er hier een toilet?", "Een voorziening zoeken.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry(
                "Hoe laat vertrekt de trein?", "Een vertrektijd navragen.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry("Ik ga naar Utrecht.", "Je bestemming noemen.", "neutral", "a1-unit-5"),
            PhrasebookEntry(
                "Is dat links of rechts?", "Een richting controleren.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry(
                "De afspraak is om half drie.",
                "Een tijd afspreken: 2.30 of 14.30, afhankelijk van de context.",
                "neutral",
                "a1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        id="contact_a1",
        level="A1",
        situation="Afspreken en contact houden",
        icon="📱",
        phrases=[
            PhrasebookEntry(
                "Heb je morgen tijd?",
                "Een vriend naar beschikbaarheid vragen.",
                "informal",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Ik kan niet komen, want ik werk.",
                "Eenvoudig uitleggen waarom je niet kunt.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Wat is je telefoonnummer?", "Contactgegevens vragen.", "informal", "a1-unit-8"
            ),
            PhrasebookEntry(
                "Ik stuur je een bericht.",
                "Aangeven hoe je contact opneemt.",
                "informal",
                "a1-unit-8",
            ),
            PhrasebookEntry(
                "Bedankt voor uw hulp.", "Iemand beleefd bedanken.", "neutral", "a1-unit-8"
            ),
            PhrasebookEntry(
                "Tot morgen!",
                "Afscheid nemen als je elkaar de volgende dag ziet.",
                "neutral",
                "a1-unit-8",
            ),
        ],
    ),
]
