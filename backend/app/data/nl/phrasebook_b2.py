"""Dutch B2 negotiation and evidence-aware discussion."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="werk_terugblik_b2",
        level="B2",
        situation="Werk en evaluatie",
        icon="💼",
        phrases=[
            PhrasebookEntry(
                "Ik heb deze week meerdere taken moeten overnemen.",
                "Een complexe werksituatie toelichten.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Welke verantwoordelijkheden horen precies bij deze functie?",
                "Rollen en bevoegdheden verduidelijken.",
                "formal",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Ik wil de werkdruk bespreken voordat die verder oploopt.",
                "Een probleem tijdig bespreekbaar maken.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Als we eerder hadden overlegd, hadden we dit mogelijk voorkomen.",
                "Een alternatief bespreken zonder zekerheid te claimen.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Achteraf gezien hebben we de benodigde tijd onderschat.",
                "Een eerdere inschatting evalueren.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Mijn bedoeling is om hiervan te leren, niet om iemand iets te verwijten.",
                "De toon van een evaluatie verduidelijken.",
                "neutral",
                "b2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="onderhandelen_b2",
        level="B2",
        situation="Voorwaarden en verantwoordelijkheid",
        icon="🤝",
        phrases=[
            PhrasebookEntry(
                "We kunnen instemmen, mits de planning wordt aangepast.",
                "Een voorwaarde bij instemming stellen.",
                "formal",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Tenzij er nieuwe bezwaren zijn, kunnen we dit afronden.",
                "Een uitzondering op een voorgestelde vervolgstap noemen.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Op dit punt zijn we bereid een concessie te doen.",
                "Ruimte voor een compromis aanbieden.",
                "formal",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Wie is verantwoordelijk voor de uitvoering?",
                "De uitvoerder expliciet maken.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Er is bezwaar ingediend; wat betekent dat voor de termijn?",
                "Naar het effect van een procedure vragen.",
                "formal",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Ik hoor graag hoe bewoners bij dit besluit worden betrokken.",
                "Om transparantie en inspraak vragen.",
                "formal",
                "b2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        id="bewijs_b2",
        level="B2",
        situation="Informatie kritisch bespreken",
        icon="🔎",
        phrases=[
            PhrasebookEntry(
                "De kop suggereert meer zekerheid dan het artikel zelf.",
                "Een verschil in berichtgeving benoemen.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Op welke bron is deze uitspraak gebaseerd?",
                "Onderbouwing opvragen.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Dat verband betekent nog niet dat het ene het andere veroorzaakt.",
                "Samenhang van oorzakelijkheid onderscheiden.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Hoe representatief is de onderzochte groep?",
                "Een beperking van gegevens onderzoeken.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Kunt u het proces in gewone woorden uitleggen?",
                "Een toegankelijke uitleg vragen.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Deze bevinding ondersteunt het voorstel, maar bewijst niet dat het overal werkt.",
                "Een conclusie begrenzen.",
                "formal",
                "b2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        id="advies_presenteren_b2",
        level="B2",
        situation="Een advies verdedigen",
        icon="🎤",
        phrases=[
            PhrasebookEntry(
                "Welke perspectieven ontbreken nog in dit debat?",
                "Een cultureel of maatschappelijk debat verbreden.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Ik begrijp de waarde van de traditie, maar zie ook de bezwaren.",
                "Een genuanceerd standpunt introduceren.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Mijn aanbeveling berust op drie overwegingen.",
                "Een advies structureren.",
                "formal",
                "b2-unit-8",
            ),
            PhrasebookEntry(
                "De haalbaarheid hangt af van de beschikbare middelen.",
                "Een praktische beperking benoemen.",
                "neutral",
                "b2-unit-8",
            ),
            PhrasebookEntry(
                "Dit alternatief verdient nader onderzoek.",
                "Een optie openhouden zonder die al te kiezen.",
                "formal",
                "b2-unit-8",
            ),
            PhrasebookEntry(
                "Welk onderdeel van de onderbouwing vindt u onvoldoende?",
                "Gerichte feedback op een advies vragen.",
                "formal",
                "b2-unit-8",
            ),
        ],
    ),
]
