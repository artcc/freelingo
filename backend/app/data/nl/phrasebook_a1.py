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
    PhrasebookCategory(
        id="dagelijks_leven_a1",
        level="A1",
        situation="Thuis, familie en dagelijkse gewoonten",
        icon="🏠",
        phrases=[
            PhrasebookEntry(
                "Ik woon alleen in een klein appartement.",
                "Je woonsituatie beschrijven.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Heb je broers of zussen?", "Naar iemands familie vragen.", "informal", "a1-unit-2"
            ),
            PhrasebookEntry(
                "Onze kat heet Mies.", "Een huisdier voorstellen.", "neutral", "a1-unit-2"
            ),
            PhrasebookEntry(
                "Mijn broer heeft kort, donker haar.",
                "Een familielid beschrijven.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Ik ontbijt iedere dag om acht uur.",
                "Een dagelijkse gewoonte noemen.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Op zondag werk ik niet.", "Vertellen wanneer je vrij bent.", "neutral", "a1-unit-3"
            ),
            PhrasebookEntry(
                "Mijn verjaardag is in november.",
                "De maand van je verjaardag noemen.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Hoe laat begint de les?", "Naar de begintijd vragen.", "neutral", "a1-unit-3"
            ),
            PhrasebookEntry(
                "De sleutels liggen op tafel.",
                "Zeggen waar een voorwerp ligt.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Ik ben moe. Ik ga naar huis.",
                "Je gevoel en een eenvoudig plan noemen.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Ik luister graag naar muziek.",
                "Een vrijetijdsvoorkeur aangeven.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Wil je samen wandelen?", "Een vriend uitnodigen.", "informal", "a1-unit-6"
            ),
        ],
    ),
    PhrasebookCategory(
        id="boodschappen_kleding_a1",
        level="A1",
        situation="Eten en kleding kopen",
        icon="🛍️",
        phrases=[
            PhrasebookEntry(
                "Een kilo appels, alstublieft.",
                "Een hoeveelheid fruit bestellen.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Heeft u ook vegetarische soep?",
                "Naar een gerecht zonder vlees of vis vragen.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry("Mag ik een lepel?", "Om bestek vragen.", "neutral", "a1-unit-4"),
            PhrasebookEntry(
                "Voor mij een kopje thee, graag.",
                "Een warme drank bestellen.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Ik heb dorst. Heb je water?", "Iemand om drinken vragen.", "informal", "a1-unit-6"
            ),
            PhrasebookEntry(
                "De soep is erg lekker.", "Een gerecht waarderen.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Ik zoek een warme trui.",
                "Een winkelmedewerker vertellen wat je zoekt.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Heeft u deze jas in het blauw?",
                "Naar een andere kleur vragen.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Waar kan ik dit passen?", "Een paskamer zoeken.", "neutral", "a1-unit-7"
            ),
            PhrasebookEntry(
                "Deze schoenen zijn te klein.",
                "Een probleem met de maat aangeven.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry("Ik betaal contant.", "Je betaalwijze noemen.", "neutral", "a1-unit-7"),
            PhrasebookEntry(
                "Een tas is niet nodig, dank u.",
                "Een tas beleefd weigeren.",
                "neutral",
                "a1-unit-7",
            ),
        ],
    ),
    PhrasebookCategory(
        id="stad_taal_a1",
        level="A1",
        situation="In de stad en in de les",
        icon="🗺️",
        phrases=[
            PhrasebookEntry(
                "Ik spreek een beetje Nederlands.",
                "Je taalvaardigheid kort aangeven.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Wat betekent dit woord?",
                "Om een eenvoudige uitleg vragen.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry("Kunt u dat herhalen?", "Om herhaling vragen.", "neutral", "a1-unit-1"),
            PhrasebookEntry(
                "Ik begrijp de vraag niet.", "Een begripsprobleem melden.", "neutral", "a1-unit-1"
            ),
            PhrasebookEntry(
                "Is het museum vandaag open?",
                "Controleren of een bezoek mogelijk is.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Waar stopt de bus naar het centrum?",
                "De juiste halte zoeken.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Ik ga op de fiets.", "Je vervoermiddel noemen.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry(
                "Het station is niet ver.", "Een korte afstand aangeven.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry(
                "Het regent. Ik neem mijn paraplu mee.",
                "Op het weer reageren.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Hoe laat is het nu?", "Naar de huidige tijd vragen.", "neutral", "a1-unit-3"
            ),
            PhrasebookEntry(
                "Sorry, ik ben te laat.",
                "Je bij aankomst verontschuldigen.",
                "neutral",
                "a1-unit-8",
            ),
            PhrasebookEntry(
                "Fijne dag nog!", "Vriendelijk afscheid nemen.", "neutral", "a1-unit-8"
            ),
        ],
    ),
]
