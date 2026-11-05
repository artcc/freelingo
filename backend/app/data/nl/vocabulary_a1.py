"""Dutch A1 vocabulary with articles, meaningful definitions and usable examples."""

from app.data._types import VocabularyEntry, VocabularySet

A1_SETS: list[VocabularySet] = [
    VocabularySet(
        id="kennismaken_a1",
        level="A1",
        topic="Kennismaken",
        unit_ref="a1-unit-1",
        words=[
            VocabularyEntry(
                "de naam", "noun", "Zo heet een persoon of een ding.", "Mijn naam is Noor."
            ),
            VocabularyEntry(
                "de voornaam",
                "noun",
                "Je persoonlijke naam, vóór je achternaam.",
                "Mijn voornaam is Sam.",
            ),
            VocabularyEntry(
                "de achternaam", "noun", "De naam van je familie.", "Wat is uw achternaam?"
            ),
            VocabularyEntry(
                "het land",
                "noun",
                "Een gebied met een eigen bestuur, zoals Nederland.",
                "Uit welk land kom je?",
            ),
            VocabularyEntry(
                "de taal",
                "noun",
                "Woorden en regels waarmee mensen communiceren.",
                "Welke taal spreek je?",
            ),
            VocabularyEntry("heten", "verb", "Een bepaalde naam hebben.", "Hoe heet je?"),
            VocabularyEntry(
                "spreken", "verb", "Met woorden iets zeggen.", "Ik spreek een beetje Nederlands."
            ),
            VocabularyEntry(
                "begrijpen", "verb", "Weten wat iemand bedoelt.", "Ik begrijp de vraag."
            ),
            VocabularyEntry(
                "herhalen", "verb", "Iets nog een keer zeggen of doen.", "Kunt u dat herhalen?"
            ),
            VocabularyEntry(
                "welkom",
                "adjective",
                "Fijn dat je er bent; je mag hier zijn.",
                "Je bent hier welkom.",
            ),
        ],
    ),
    VocabularySet(
        id="familie_a1",
        level="A1",
        topic="Familie en mensen",
        unit_ref="a1-unit-2",
        words=[
            VocabularyEntry(
                "de moeder", "noun", "Een vrouwelijke ouder.", "Mijn moeder woont in Delft."
            ),
            VocabularyEntry(
                "de vader", "noun", "Een mannelijke ouder.", "Mijn vader heeft een fiets."
            ),
            VocabularyEntry("de ouder", "noun", "Een moeder of vader.", "Mijn ouders wonen samen."),
            VocabularyEntry(
                "het kind",
                "noun",
                "Een jong persoon; ook een zoon of dochter.",
                "Het kind is zes jaar.",
            ),
            VocabularyEntry(
                "de broer",
                "noun",
                "Een jongen of man met dezelfde ouder of ouders als jij.",
                "Mijn broer heet Daan.",
            ),
            VocabularyEntry(
                "de zus",
                "noun",
                "Een meisje of vrouw met dezelfde ouder of ouders als jij.",
                "Ik heb twee zussen.",
            ),
            VocabularyEntry(
                "de partner",
                "noun",
                "De persoon met wie iemand een liefdesrelatie heeft.",
                "Dit is mijn partner.",
            ),
            VocabularyEntry(
                "de vriend",
                "noun",
                "Een man of jongen die je goed kent en graag ziet.",
                "Mijn vriend woont dichtbij.",
            ),
            VocabularyEntry(
                "vriendelijk",
                "adjective",
                "Aardig tegen andere mensen.",
                "Onze buurvrouw is vriendelijk.",
            ),
            VocabularyEntry("jong", "adjective", "Nog niet oud.", "Mijn zus is nog jong."),
        ],
    ),
    VocabularySet(
        id="dag_a1",
        level="A1",
        topic="De dag en de klok",
        unit_ref="a1-unit-3",
        words=[
            VocabularyEntry(
                "de ochtend",
                "noun",
                "Het eerste deel van de dag, vóór twaalf uur.",
                "Ik werk in de ochtend.",
            ),
            VocabularyEntry(
                "de middag",
                "noun",
                "Het deel van de dag na twaalf uur en vóór de avond.",
                "In de middag lees ik.",
            ),
            VocabularyEntry(
                "de avond",
                "noun",
                "Het deel van de dag tussen middag en nacht.",
                "Wij eten in de avond.",
            ),
            VocabularyEntry(
                "het uur", "noun", "Een periode van zestig minuten.", "De les duurt een uur."
            ),
            VocabularyEntry(
                "de minuut",
                "noun",
                "Een periode van zestig seconden.",
                "De bus komt over vijf minuten.",
            ),
            VocabularyEntry("vandaag", "adverb", "Op deze dag.", "Vandaag werk ik thuis."),
            VocabularyEntry("morgen", "adverb", "Op de dag na vandaag.", "Morgen ben ik vrij."),
            VocabularyEntry(
                "opstaan",
                "verb",
                "Uit bed komen of van een stoel omhoogkomen.",
                "Ik sta om zeven uur op.",
            ),
            VocabularyEntry(
                "werken",
                "verb",
                "Een taak of beroep uitvoeren.",
                "Mijn partner werkt in een winkel.",
            ),
            VocabularyEntry(
                "slapen",
                "verb",
                "Rusten met je ogen dicht zonder wakker te zijn.",
                "Ik slaap acht uur.",
            ),
        ],
    ),
    VocabularySet(
        id="eten_a1",
        level="A1",
        topic="Aan tafel",
        unit_ref="a1-unit-4",
        words=[
            VocabularyEntry(
                "het brood",
                "noun",
                "Voedsel van meel en water dat in een oven wordt gebakken.",
                "Ik eet brood met kaas.",
            ),
            VocabularyEntry(
                "de kaas",
                "noun",
                "Een stevig voedingsmiddel dat van melk wordt gemaakt.",
                "Wilt u kaas op uw brood?",
            ),
            VocabularyEntry(
                "het water",
                "noun",
                "Een heldere vloeistof die je kunt drinken.",
                "Mag ik een glas water?",
            ),
            VocabularyEntry(
                "de koffie",
                "noun",
                "Een warme drank van gemalen koffiebonen.",
                "Ik drink koffie zonder melk.",
            ),
            VocabularyEntry(
                "de thee",
                "noun",
                "Een drank van heet water met bladeren of kruiden.",
                "De thee is warm.",
            ),
            VocabularyEntry(
                "de melk",
                "noun",
                "Een witte vloeistof van bijvoorbeeld een koe.",
                "Er is geen melk meer.",
            ),
            VocabularyEntry(
                "de appel",
                "noun",
                "Een ronde vrucht met een schil en pitten.",
                "Ik wil een groene appel.",
            ),
            VocabularyEntry(
                "eten", "verb", "Voedsel in je mond nemen en doorslikken.", "Wij eten om zes uur."
            ),
            VocabularyEntry(
                "drinken",
                "verb",
                "Een vloeistof in je mond nemen en doorslikken.",
                "Wil je iets drinken?",
            ),
            VocabularyEntry(
                "lekker",
                "adjective",
                "Met een fijne smaak of een prettig gevoel.",
                "De soep is lekker.",
            ),
        ],
    ),
    VocabularySet(
        id="stad_a1",
        level="A1",
        topic="Thuis en in de stad",
        unit_ref="a1-unit-5",
        words=[
            VocabularyEntry(
                "het huis", "noun", "Een gebouw waarin mensen wonen.", "Ons huis heeft drie kamers."
            ),
            VocabularyEntry(
                "de kamer",
                "noun",
                "Een deel van een gebouw met muren eromheen.",
                "Dit is mijn kamer.",
            ),
            VocabularyEntry(
                "de straat",
                "noun",
                "Een weg tussen huizen of andere gebouwen.",
                "De winkel is in deze straat.",
            ),
            VocabularyEntry(
                "het station",
                "noun",
                "Een plaats waar treinen stoppen en reizigers instappen.",
                "Het station is dichtbij.",
            ),
            VocabularyEntry(
                "de trein", "noun", "Een vervoermiddel dat op rails rijdt.", "Ik ga met de trein."
            ),
            VocabularyEntry(
                "de fiets",
                "noun",
                "Een voertuig met twee wielen dat je met pedalen beweegt.",
                "Mijn fiets staat buiten.",
            ),
            VocabularyEntry(
                "de winkel", "noun", "Een plaats waar je producten koopt.", "De winkel is open."
            ),
            VocabularyEntry(
                "de supermarkt",
                "noun",
                "Een grote winkel voor eten en dagelijkse producten.",
                "Ik ga naar de supermarkt.",
            ),
            VocabularyEntry(
                "links", "adverb", "Aan de kant tegenover rechts.", "Het station is links."
            ),
            VocabularyEntry(
                "rechts", "adverb", "Aan de kant tegenover links.", "De apotheek is rechts."
            ),
        ],
    ),
    VocabularySet(
        id="vrije_tijd_a1",
        level="A1",
        topic="Hobby's en afspraken",
        unit_ref="a1-unit-6",
        words=[
            VocabularyEntry(
                "de hobby",
                "noun",
                "Iets dat je graag in je vrije tijd doet.",
                "Mijn hobby is tekenen.",
            ),
            VocabularyEntry(
                "het boek",
                "noun",
                "Bladzijden met tekst of beelden, samen in een kaft.",
                "Ik lees een mooi boek.",
            ),
            VocabularyEntry(
                "de muziek",
                "noun",
                "Klanken met een ritme of melodie.",
                "Ik luister graag naar muziek.",
            ),
            VocabularyEntry(
                "de film",
                "noun",
                "Een verhaal of verslag met bewegende beelden.",
                "We kijken vanavond een film.",
            ),
            VocabularyEntry(
                "lezen", "verb", "Geschreven woorden bekijken en begrijpen.", "Ik lees iedere dag."
            ),
            VocabularyEntry(
                "wandelen", "verb", "Lopen voor je plezier.", "We wandelen in het park."
            ),
            VocabularyEntry("zwemmen", "verb", "Je lichaam door water bewegen.", "Kun je zwemmen?"),
            VocabularyEntry("graag", "adverb", "Met plezier.", "Ik fiets graag."),
            VocabularyEntry("samen", "adverb", "Met elkaar.", "We eten samen."),
            VocabularyEntry(
                "afspreken",
                "verb",
                "Een tijd of plan met iemand bepalen.",
                "Kunnen we morgen afspreken?",
            ),
        ],
    ),
    VocabularySet(
        id="winkelen_a1",
        level="A1",
        topic="Kleding en betalen",
        unit_ref="a1-unit-7",
        words=[
            VocabularyEntry(
                "de jas",
                "noun",
                "Kleding die je buiten over andere kleding draagt.",
                "Deze jas is warm.",
            ),
            VocabularyEntry(
                "de broek",
                "noun",
                "Kleding met twee delen voor je benen.",
                "Ik zoek een blauwe broek.",
            ),
            VocabularyEntry(
                "de schoen",
                "noun",
                "Iets dat je aan je voet draagt om buiten te lopen.",
                "Deze schoenen zijn te klein.",
            ),
            VocabularyEntry(
                "de maat",
                "noun",
                "Een nummer of letter voor de grootte van kleding.",
                "Welke maat heeft u?",
            ),
            VocabularyEntry("de prijs", "noun", "Het bedrag dat iets kost.", "Wat is de prijs?"),
            VocabularyEntry(
                "de euro",
                "noun",
                "Het geld dat onder meer in Nederland wordt gebruikt.",
                "Dat kost tien euro.",
            ),
            VocabularyEntry(
                "betalen",
                "verb",
                "Geld geven voor een product of dienst.",
                "Kan ik met mijn pinpas betalen?",
            ),
            VocabularyEntry(
                "passen",
                "verb",
                "Kleding aantrekken om de maat te proberen.",
                "Mag ik deze jas passen?",
            ),
            VocabularyEntry("duur", "adjective", "Met een hoge prijs.", "Die schoenen zijn duur."),
            VocabularyEntry(
                "goedkoop", "adjective", "Met een lage prijs.", "Deze tas is goedkoop."
            ),
        ],
    ),
    VocabularySet(
        id="contact_a1",
        level="A1",
        topic="Een bericht sturen",
        unit_ref="a1-unit-8",
        words=[
            VocabularyEntry(
                "het adres",
                "noun",
                "De straat, het huisnummer en de plaats waar iemand woont.",
                "Wat is je adres?",
            ),
            VocabularyEntry(
                "het nummer",
                "noun",
                "Een getal waarmee je iets of iemand kunt vinden.",
                "Mijn huisnummer is twaalf.",
            ),
            VocabularyEntry(
                "de telefoon",
                "noun",
                "Een apparaat waarmee je iemand kunt bellen.",
                "Mijn telefoon ligt op tafel.",
            ),
            VocabularyEntry(
                "het bericht",
                "noun",
                "Informatie die iemand naar een ander stuurt.",
                "Ik stuur je een bericht.",
            ),
            VocabularyEntry(
                "de vraag",
                "noun",
                "Iets wat je zegt om informatie te krijgen.",
                "Ik heb een vraag.",
            ),
            VocabularyEntry(
                "het antwoord",
                "noun",
                "Wat iemand op een vraag zegt of schrijft.",
                "Bedankt voor uw antwoord.",
            ),
            VocabularyEntry(
                "bellen", "verb", "Via de telefoon met iemand praten.", "Ik bel mijn zus."
            ),
            VocabularyEntry(
                "schrijven",
                "verb",
                "Woorden op papier of op een scherm zetten.",
                "Schrijf je naam hier.",
            ),
            VocabularyEntry(
                "sturen", "verb", "Iets naar iemand verzenden.", "Ik stuur morgen een e-mail."
            ),
            VocabularyEntry(
                "tot ziens",
                "phrase",
                "Een groet als je weggaat en iemand later weer kunt zien.",
                "Bedankt en tot ziens!",
            ),
        ],
    ),
    VocabularySet(
        id="getallen_a1",
        level="A1",
        topic="Getallen en hoeveelheden",
        unit_ref="a1-unit-1",
        words=[
            VocabularyEntry(
                "nul",
                "numeral",
                "Het getal 0: er is niets van iets.",
                "De temperatuur is nul graden.",
            ),
            VocabularyEntry(
                "één", "numeral", "Het getal 1; één enkel ding.", "Ik heb één broer, niet twee."
            ),
            VocabularyEntry(
                "twee", "numeral", "Het getal 2: één en nog één.", "Ik koop twee appels."
            ),
            VocabularyEntry(
                "drie", "numeral", "Het getal 3, na twee en vóór vier.", "Er zijn drie kamers."
            ),
            VocabularyEntry(
                "vier", "numeral", "Het getal 4, twee keer twee.", "De tafel heeft vier poten."
            ),
            VocabularyEntry(
                "vijf", "numeral", "Het getal 5, de helft van tien.", "Dat kost vijf euro."
            ),
            VocabularyEntry(
                "zes", "numeral", "Het getal 6, na vijf en vóór zeven.", "We eten om zes uur."
            ),
            VocabularyEntry(
                "zeven",
                "numeral",
                "Het getal 7, het aantal dagen in een week.",
                "Ik sta om zeven uur op.",
            ),
            VocabularyEntry(
                "acht", "numeral", "Het getal 8, twee keer vier.", "De les begint om acht uur."
            ),
            VocabularyEntry(
                "negen", "numeral", "Het getal 9, één minder dan tien.", "Mijn kind is negen jaar."
            ),
            VocabularyEntry(
                "tien", "numeral", "Het getal 10, twee keer vijf.", "Er zijn tien studenten."
            ),
            VocabularyEntry(
                "elf", "numeral", "Het getal 11, één meer dan tien.", "Mijn zus is elf jaar."
            ),
            VocabularyEntry(
                "twaalf",
                "numeral",
                "Het getal 12, twee meer dan tien.",
                "Mijn huisnummer is twaalf.",
            ),
            VocabularyEntry(
                "dertien",
                "numeral",
                "Het getal 13, drie meer dan tien.",
                "Er zijn dertien studenten.",
            ),
            VocabularyEntry(
                "veertien",
                "numeral",
                "Het getal 14, vier meer dan tien.",
                "Mijn broer is veertien jaar.",
            ),
            VocabularyEntry(
                "vijftien",
                "numeral",
                "Het getal 15, vijf meer dan tien.",
                "De reis duurt vijftien minuten.",
            ),
            VocabularyEntry(
                "zestien", "numeral", "Het getal 16, zes meer dan tien.", "Ik ben zestien jaar."
            ),
            VocabularyEntry(
                "zeventien",
                "numeral",
                "Het getal 17, zeven meer dan tien.",
                "De bus heeft nummer zeventien.",
            ),
            VocabularyEntry(
                "achttien", "numeral", "Het getal 18, acht meer dan tien.", "Zij is achttien jaar."
            ),
            VocabularyEntry(
                "negentien",
                "numeral",
                "Het getal 19, één minder dan twintig.",
                "Het boek kost negentien euro.",
            ),
            VocabularyEntry(
                "twintig",
                "numeral",
                "Het getal 20, twee keer tien.",
                "De reis duurt twintig minuten.",
            ),
            VocabularyEntry(
                "eenentwintig",
                "numeral",
                "Het getal 21: zeg eerst één, dan en, dan twintig.",
                "Ik ben eenentwintig jaar.",
            ),
            VocabularyEntry(
                "dertig", "numeral", "Het getal 30, drie keer tien.", "Hij is dertig jaar."
            ),
            VocabularyEntry(
                "veertig", "numeral", "Het getal 40, vier keer tien.", "De jas kost veertig euro."
            ),
            VocabularyEntry(
                "vijftig", "numeral", "Het getal 50, vijf keer tien.", "Er zijn vijftig plaatsen."
            ),
            VocabularyEntry(
                "zestig", "numeral", "Het getal 60, zes keer tien.", "Een uur heeft zestig minuten."
            ),
            VocabularyEntry(
                "zeventig",
                "numeral",
                "Het getal 70, zeven keer tien.",
                "Mijn oma is zeventig jaar.",
            ),
            VocabularyEntry(
                "tachtig", "numeral", "Het getal 80, acht keer tien.", "Dat kost tachtig euro."
            ),
            VocabularyEntry(
                "negentig",
                "numeral",
                "Het getal 90, negen keer tien.",
                "Mijn opa is negentig jaar.",
            ),
            VocabularyEntry(
                "honderd",
                "numeral",
                "Het getal 100, tien keer tien.",
                "De fiets kost honderd euro.",
            ),
        ],
    ),
    VocabularySet(
        id="kalender_a1",
        level="A1",
        topic="Dagen en de kalender",
        unit_ref="a1-unit-3",
        words=[
            VocabularyEntry(
                "maandag", "noun", "De dag na zondag en vóór dinsdag.", "Op maandag werk ik thuis."
            ),
            VocabularyEntry(
                "dinsdag", "noun", "De dag na maandag en vóór woensdag.", "Dinsdag heb ik les."
            ),
            VocabularyEntry(
                "woensdag", "noun", "De dag tussen dinsdag en donderdag.", "Woensdag ben ik vrij."
            ),
            VocabularyEntry(
                "donderdag",
                "noun",
                "De dag tussen woensdag en vrijdag.",
                "De afspraak is op donderdag.",
            ),
            VocabularyEntry(
                "vrijdag",
                "noun",
                "De dag na donderdag en vóór zaterdag.",
                "Vrijdag komen mijn ouders.",
            ),
            VocabularyEntry(
                "zaterdag",
                "noun",
                "De dag na vrijdag en vóór zondag.",
                "We gaan zaterdag wandelen.",
            ),
            VocabularyEntry(
                "zondag", "noun", "De dag na zaterdag en vóór maandag.", "Op zondag slaap ik lang."
            ),
            VocabularyEntry(
                "de week", "noun", "Een periode van zeven dagen.", "Ik werk vier dagen per week."
            ),
            VocabularyEntry(
                "de maand",
                "noun",
                "Een van de twaalf delen van een jaar.",
                "Deze maand heb ik vakantie.",
            ),
            VocabularyEntry(
                "het jaar", "noun", "Een periode van twaalf maanden.", "Mijn zus is twintig jaar."
            ),
            VocabularyEntry(
                "het weekend", "noun", "Zaterdag en zondag samen.", "In het weekend ben ik vrij."
            ),
            VocabularyEntry(
                "de datum",
                "noun",
                "Een bepaalde dag met maand en jaar.",
                "Wat is de datum van de afspraak?",
            ),
        ],
    ),
    VocabularySet(
        id="huis_a1",
        level="A1",
        topic="Kamers en voorwerpen",
        unit_ref="a1-unit-5",
        words=[
            VocabularyEntry(
                "de keuken", "noun", "De ruimte waar je eten maakt.", "De keuken is klein."
            ),
            VocabularyEntry(
                "de badkamer", "noun", "De ruimte waar je je wast.", "De badkamer is boven."
            ),
            VocabularyEntry(
                "de slaapkamer",
                "noun",
                "De kamer waar je slaapt.",
                "Er staat een bed in de slaapkamer.",
            ),
            VocabularyEntry(
                "het toilet",
                "noun",
                "Een voorziening om te plassen of te poepen.",
                "Waar is het toilet?",
            ),
            VocabularyEntry(
                "de tafel",
                "noun",
                "Een meubel met een vlak blad op poten.",
                "Het boek ligt op tafel.",
            ),
            VocabularyEntry(
                "de stoel",
                "noun",
                "Een meubel voor één persoon om op te zitten.",
                "Er staan vier stoelen.",
            ),
            VocabularyEntry(
                "het bed", "noun", "Een meubel om op te slapen.", "Het bed staat bij het raam."
            ),
            VocabularyEntry(
                "de deur",
                "noun",
                "Een beweegbaar deel waarmee je een ingang sluit.",
                "De deur is open.",
            ),
            VocabularyEntry(
                "het raam",
                "noun",
                "Een opening met glas waardoor licht naar binnen komt.",
                "Ik kijk door het raam.",
            ),
            VocabularyEntry(
                "liggen", "verb", "In een horizontale positie zijn.", "De krant ligt op tafel."
            ),
            VocabularyEntry(
                "staan", "verb", "Rechtop op een plaats zijn.", "De fles staat in de keuken."
            ),
            VocabularyEntry(
                "hangen",
                "verb",
                "Aan iets vastzitten zonder van onderen te worden gesteund.",
                "De jas hangt aan de deur.",
            ),
        ],
    ),
    VocabularySet(
        id="kleuren_a1",
        level="A1",
        topic="Kleuren en eigenschappen",
        unit_ref="a1-unit-7",
        words=[
            VocabularyEntry(
                "rood", "adjective", "Met de kleur van een rijpe tomaat.", "Ik draag een rode jas."
            ),
            VocabularyEntry(
                "blauw", "adjective", "Met de kleur van een heldere lucht.", "Mijn broek is blauw."
            ),
            VocabularyEntry("groen", "adjective", "Met de kleur van gras.", "De tas is groen."),
            VocabularyEntry(
                "geel",
                "adjective",
                "Met de kleur van een rijpe citroen.",
                "Hij heeft een gele fiets.",
            ),
            VocabularyEntry(
                "zwart", "adjective", "Met de donkerste kleur.", "Ik zoek zwarte schoenen."
            ),
            VocabularyEntry(
                "wit", "adjective", "Met de kleur van verse sneeuw.", "Het witte shirt is mooi."
            ),
            VocabularyEntry(
                "groot",
                "adjective",
                "Met veel ruimte of een flinke omvang.",
                "Deze jas is te groot.",
            ),
            VocabularyEntry(
                "klein",
                "adjective",
                "Met weinig ruimte of een beperkte omvang.",
                "Ik heb een kleine tas.",
            ),
            VocabularyEntry(
                "nieuw",
                "adjective",
                "Pas gemaakt, gekocht of begonnen.",
                "Dit is mijn nieuwe fiets.",
            ),
            VocabularyEntry(
                "oud", "adjective", "Al lang bestaand of niet meer jong.", "Dat is een oud huis."
            ),
            VocabularyEntry(
                "warm", "adjective", "Met een aangenaam hoge temperatuur.", "Deze trui is warm."
            ),
            VocabularyEntry("koud", "adjective", "Met een lage temperatuur.", "Het water is koud."),
        ],
    ),
]
