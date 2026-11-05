"""Dutch B1 independent interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="verhaal_informatie_b1",
        level="B1",
        situation="Vertellen en verduidelijken",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                "Toen ik aankwam, was de bijeenkomst al begonnen.",
                "Een gebeurtenis in een tijdslijn plaatsen.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Gelukkig liep het uiteindelijk goed af.",
                "Een verhaal afsluiten met de uitkomst.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Weet u of ik hiervoor een afspraak nodig heb?",
                "Indirect naar een procedure vragen.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Als ik u goed begrijp, moet ik eerst het formulier invullen.",
                "Je begrip van een instructie controleren.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Zij zei dat ze waarschijnlijk later zou komen.",
                "Een boodschap met onzekerheid doorgeven.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Kunt u dat met een voorbeeld toelichten?",
                "Om concretere uitleg vragen.",
                "formal",
                "b1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="samen_regelen_b1",
        level="B1",
        situation="Samenwerken en aanvragen",
        icon="📄",
        phrases=[
            PhrasebookEntry(
                "Ik begrijp je punt, maar ik zie het anders.",
                "Een meningsverschil respectvol beginnen.",
                "informal",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Daar moeten we rekening mee houden.",
                "Een relevant belang erkennen.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Met wie kan ik hierover overleggen?",
                "De juiste contactpersoon zoeken.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Mijn aanvraag is ingediend, maar ik heb nog geen antwoord ontvangen.",
                "De status van een aanvraag navragen.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Welke documenten ontbreken er nog?",
                "Ontbrekende informatie opvragen.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Binnen welke termijn kan ik een reactie verwachten?",
                "Een antwoordtermijn navragen.",
                "formal",
                "b1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        id="advies_mening_b1",
        level="B1",
        situation="Advies en een mening geven",
        icon="💡",
        phrases=[
            PhrasebookEntry(
                "Als ik jou was, zou ik eerst informatie aanvragen.",
                "Voorzichtig advies geven.",
                "informal",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Het voordeel is de prijs; het nadeel is de lange reistijd.",
                "Twee kanten van een keuze benoemen.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Ik twijfel nog tussen beide mogelijkheden.",
                "Aangeven dat je nog niet hebt gekozen.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Hoewel het plan duur is, kan het de buurt veiliger maken.",
                "Een voordeel met een tegenwerping verbinden.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Volgens mij moeten bewoners kunnen meepraten.",
                "Een mening over een publiek plan geven.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Daarom lijkt deze oplossing mij het beste.",
                "Een eerder gegeven argument afronden.",
                "neutral",
                "b1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        id="overleg_b1",
        level="B1",
        situation="Vooruitgang en afspraken bespreken",
        icon="📝",
        phrases=[
            PhrasebookEntry(
                "Ik oefen al een paar maanden en merk vooruitgang.",
                "Een doorgaande ontwikkeling beschrijven.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Niet iedereen heeft dezelfde ondersteuning nodig.",
                "Verschillen binnen een groep erkennen.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Zullen we de taken onder elkaar verdelen?",
                "Een gezamenlijke werkwijze voorstellen.",
                "neutral",
                "b1-unit-8",
            ),
            PhrasebookEntry(
                "Wie neemt deze taak op zich?",
                "Een verantwoordelijke afspreken.",
                "neutral",
                "b1-unit-8",
            ),
            PhrasebookEntry(
                "Ik vat de afspraken nog even samen.",
                "Controleren wat gezamenlijk is afgesproken.",
                "neutral",
                "b1-unit-8",
            ),
            PhrasebookEntry(
                "Laat het weten als ik iets verkeerd heb begrepen.",
                "Ruimte geven voor correctie.",
                "neutral",
                "b1-unit-8",
            ),
        ],
    ),
]
