"""Dutch A2 requests, arrangements and everyday problems."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="reis_hulp_a2",
        level="A2",
        situation="Een reis regelen",
        icon="🧳",
        phrases=[
            PhrasebookEntry(
                "Moet ik onderweg overstappen?",
                "Een reisroute controleren.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Ik heb een kamer voor twee nachten gereserveerd.",
                "Je bij een accommodatie melden.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Onze trein is niet aangekomen. Wat kunnen we doen?",
                "Hulp vragen bij een onderbroken reis.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Hoe was je vakantie?", "Naar een ervaring vragen.", "informal", "a2-unit-2"
            ),
            PhrasebookEntry(
                "Vroeger gingen we vaak kamperen.",
                "Een vroegere gewoonte beschrijven.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Ik ben mijn tas kwijt.",
                "Melden dat je een voorwerp niet kunt vinden.",
                "neutral",
                "a2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="woning_afspraak_a2",
        level="A2",
        situation="Afspraken en wonen",
        icon="🏠",
        phrases=[
            PhrasebookEntry(
                "Kunnen we de afspraak naar vrijdag verplaatsen?",
                "Een andere dag voorstellen.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Ik kom later omdat mijn trein vertraging heeft.",
                "Een vertraging uitleggen.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Is de huur inclusief verwarming?",
                "Vragen welke kosten inbegrepen zijn.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Wanneer kan ik de woning bekijken?",
                "Een bezichtiging aanvragen.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Deze kamer is groter dan de andere.",
                "Twee opties vergelijken.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Hoeveel sleutels krijg ik? Ik heb er twee nodig.",
                "Een praktische behoefte aangeven.",
                "neutral",
                "a2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        id="zorg_werk_a2",
        level="A2",
        situation="Zorg en werk regelen",
        icon="📋",
        phrases=[
            PhrasebookEntry(
                "Ik wil graag een afspraak bij de huisarts maken.",
                "Een consult aanvragen.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Ik heb sinds gisteren pijn in mijn rug.",
                "Een klacht en het begin ervan noemen.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Hoe moet ik dit medicijn gebruiken?",
                "Een behandelaar of apotheker om uitleg vragen.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Ik voel me niet goed en kan vandaag niet werken.",
                "Je ziek melden.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Ik wil me aanmelden voor de cursus.",
                "Deelnemen aan een opleiding aanvragen.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Zou u mijn aanmelding willen bevestigen?",
                "Beleefd om een bevestiging vragen.",
                "formal",
                "a2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        id="oplossing_a2",
        level="A2",
        situation="Problemen oplossen en organiseren",
        icon="🤝",
        phrases=[
            PhrasebookEntry(
                "De jas die ik heb besteld is te klein.",
                "Een probleem met een bestelling beschrijven.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Kan ik het product ruilen of mijn geld terugkrijgen?",
                "Naar beschikbare oplossingen vragen.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Ik heb de bon bij me.", "Een aankoopbewijs aanbieden.", "neutral", "a2-unit-7"
            ),
            PhrasebookEntry(
                "Wat zal ik meenemen?",
                "Bij een uitnodiging hulp aanbieden.",
                "informal",
                "a2-unit-8",
            ),
            PhrasebookEntry(
                "Gaat de activiteit door als het regent?",
                "Een praktische voorwaarde navragen.",
                "neutral",
                "a2-unit-8",
            ),
            PhrasebookEntry(
                "Bedankt voor de gezellige avond.",
                "Na een bijeenkomst bedanken.",
                "neutral",
                "a2-unit-8",
            ),
        ],
    ),
]
