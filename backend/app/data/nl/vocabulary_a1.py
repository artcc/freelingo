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
    VocabularySet(
        id="beroepen_a1",
        level="A1",
        topic="Werk en mensen",
        unit_ref="a1-unit-1",
        words=[
            VocabularyEntry(
                "de docent",
                "noun",
                "Iemand die lesgeeft; meervoud: docenten.",
                "Mijn broer is docent.",
            ),
            VocabularyEntry(
                "de student",
                "noun",
                "Iemand die aan een opleiding studeert; meervoud: studenten.",
                "Ik ben student in Leiden.",
            ),
            VocabularyEntry(
                "de arts",
                "noun",
                "Iemand die zieke mensen onderzoekt en behandelt; meervoud: artsen.",
                "Mijn zus is arts.",
            ),
            VocabularyEntry(
                "de kok",
                "noun",
                "Iemand die als beroep eten maakt; meervoud: koks.",
                "De kok werkt in een restaurant.",
            ),
            VocabularyEntry(
                "de bakker",
                "noun",
                "Iemand die brood maakt of verkoopt; meervoud: bakkers.",
                "De bakker begint vroeg.",
            ),
            VocabularyEntry(
                "de chauffeur",
                "noun",
                "Iemand die voor zijn werk een voertuig bestuurt; meervoud: chauffeurs.",
                "De chauffeur rijdt de bus.",
            ),
            VocabularyEntry(
                "het beroep",
                "noun",
                "Het soort werk dat iemand doet; meervoud: beroepen.",
                "Wat is uw beroep?",
            ),
            VocabularyEntry(
                "het kantoor",
                "noun",
                "Een plek waar mensen administratief werk doen; meervoud: kantoren.",
                "Ik werk op kantoor.",
            ),
            VocabularyEntry(
                "de school",
                "noun",
                "Een plaats waar je les krijgt; meervoud: scholen.",
                "De school is dichtbij.",
            ),
            VocabularyEntry(
                "studeren",
                "verb",
                "Leren voor een opleiding of examen.",
                "Ik studeer in Amsterdam.",
            ),
        ],
    ),
    VocabularySet(
        id="herkomst_a1",
        level="A1",
        topic="Waar kom je vandaan?",
        unit_ref="a1-unit-1",
        words=[
            VocabularyEntry(
                "de stad",
                "noun",
                "Een grote woonplaats met veel gebouwen; meervoud: steden.",
                "Utrecht is een mooie stad.",
            ),
            VocabularyEntry(
                "het dorp",
                "noun",
                "Een kleine woonplaats; meervoud: dorpen.",
                "Ik woon in een dorp.",
            ),
            VocabularyEntry(
                "wonen", "verb", "Een vaste plek hebben waar je leeft.", "Waar woon je?"
            ),
            VocabularyEntry(
                "komen",
                "verb",
                "Naar een plaats bewegen; ook gebruikt voor herkomst.",
                "Ik kom uit Spanje.",
            ),
            VocabularyEntry(
                "uit",
                "preposition",
                "Geeft onder meer de plaats van herkomst aan.",
                "Zij komt uit Nederland.",
            ),
            VocabularyEntry(
                "in", "preposition", "Binnen een ruimte of gebied.", "Wij wonen in Rotterdam."
            ),
            VocabularyEntry("hier", "adverb", "Op deze plaats.", "Ik woon hier."),
            VocabularyEntry("daar", "adverb", "Op die andere plaats.", "Mijn school is daar."),
            VocabularyEntry(
                "Nederlands",
                "noun",
                "De taal die onder meer in Nederland wordt gesproken.",
                "Ik leer Nederlands.",
            ),
            VocabularyEntry(
                "Engels",
                "noun",
                "De taal die onder meer in Engeland wordt gesproken.",
                "Spreekt u Engels?",
            ),
        ],
    ),
    VocabularySet(
        id="uiterlijk_a1",
        level="A1",
        topic="Een persoon beschrijven",
        unit_ref="a1-unit-2",
        words=[
            VocabularyEntry(
                "het haar",
                "noun",
                "De haren op iemands hoofd, als geheel.",
                "Mijn zus heeft lang haar.",
            ),
            VocabularyEntry(
                "het oog",
                "noun",
                "Een lichaamsdeel waarmee je kijkt; meervoud: ogen.",
                "Mijn vader heeft blauwe ogen.",
            ),
            VocabularyEntry(
                "de bril",
                "noun",
                "Glazen voor je ogen om beter te zien; meervoud: brillen.",
                "Mijn moeder draagt een bril.",
            ),
            VocabularyEntry("lang", "adjective", "Met een grote lengte.", "Mijn broer is lang."),
            VocabularyEntry(
                "kort", "adjective", "Met een kleine lengte of duur.", "Hij heeft kort haar."
            ),
            VocabularyEntry(
                "blond",
                "adjective",
                "Met een lichte, geelachtige haarkleur.",
                "Zij heeft blond haar.",
            ),
            VocabularyEntry(
                "donker",
                "adjective",
                "Met weinig licht of een diepe kleur.",
                "Hij heeft donkere ogen.",
            ),
            VocabularyEntry(
                "de man",
                "noun",
                "Een volwassen mannelijk persoon; meervoud: mannen.",
                "Die man is mijn vader.",
            ),
            VocabularyEntry(
                "de vrouw",
                "noun",
                "Een volwassen vrouwelijk persoon; meervoud: vrouwen.",
                "Deze vrouw is mijn zus.",
            ),
            VocabularyEntry(
                "dragen", "verb", "Kleding aanhebben of iets bij je houden.", "Ik draag een bril."
            ),
        ],
    ),
    VocabularySet(
        id="dieren_a1",
        level="A1",
        topic="Dieren om ons heen",
        unit_ref="a1-unit-2",
        words=[
            VocabularyEntry(
                "de hond",
                "noun",
                "Een huisdier dat blaft; meervoud: honden.",
                "Onze hond is klein.",
            ),
            VocabularyEntry(
                "de kat",
                "noun",
                "Een huisdier dat miauwt; meervoud: katten.",
                "De kat slaapt op de stoel.",
            ),
            VocabularyEntry(
                "de vogel",
                "noun",
                "Een dier met veren en vleugels; meervoud: vogels.",
                "Er zit een vogel in de tuin.",
            ),
            VocabularyEntry(
                "de vis",
                "noun",
                "Een dier dat in water leeft en kieuwen heeft; meervoud: vissen.",
                "We hebben twee vissen.",
            ),
            VocabularyEntry(
                "het paard",
                "noun",
                "Een groot dier waarop mensen kunnen rijden; meervoud: paarden.",
                "Dat paard is bruin.",
            ),
            VocabularyEntry(
                "de koe",
                "noun",
                "Een groot boerderijdier dat melk geeft; meervoud: koeien.",
                "De koe staat buiten.",
            ),
            VocabularyEntry(
                "het dier",
                "noun",
                "Een levend wezen zoals een hond of vogel; meervoud: dieren.",
                "Welk dier is dat?",
            ),
            VocabularyEntry(
                "het huisdier",
                "noun",
                "Een dier dat mensen thuis verzorgen; meervoud: huisdieren.",
                "Heeft u een huisdier?",
            ),
            VocabularyEntry(
                "de tuin",
                "noun",
                "Een stuk grond bij een huis met planten; meervoud: tuinen.",
                "De hond is in de tuin.",
            ),
            VocabularyEntry(
                "lief", "adjective", "Aardig en zacht in het contact.", "Onze kat is lief."
            ),
        ],
    ),
    VocabularySet(
        id="maanden_a1",
        level="A1",
        topic="Maanden en seizoenen",
        unit_ref="a1-unit-3",
        words=[
            VocabularyEntry(
                "januari", "noun", "De eerste maand van het jaar.", "In januari is het vaak koud."
            ),
            VocabularyEntry(
                "februari",
                "noun",
                "De tweede maand van het jaar.",
                "Mijn broer is in februari jarig.",
            ),
            VocabularyEntry(
                "maart", "noun", "De derde maand van het jaar.", "De cursus begint in maart."
            ),
            VocabularyEntry(
                "april", "noun", "De vierde maand van het jaar.", "In april heb ik vakantie."
            ),
            VocabularyEntry(
                "mei", "noun", "De vijfde maand van het jaar.", "Mijn zus komt in mei."
            ),
            VocabularyEntry(
                "juni", "noun", "De zesde maand van het jaar.", "In juni gaan we naar zee."
            ),
            VocabularyEntry(
                "juli", "noun", "De zevende maand van het jaar.", "De school is in juli dicht."
            ),
            VocabularyEntry(
                "augustus", "noun", "De achtste maand van het jaar.", "In augustus werk ik niet."
            ),
            VocabularyEntry(
                "september",
                "noun",
                "De negende maand van het jaar.",
                "De lessen beginnen in september.",
            ),
            VocabularyEntry(
                "oktober", "noun", "De tiende maand van het jaar.", "De afspraak is in oktober."
            ),
            VocabularyEntry(
                "november", "noun", "De elfde maand van het jaar.", "Ik ben in november jarig."
            ),
            VocabularyEntry(
                "december",
                "noun",
                "De twaalfde maand van het jaar.",
                "Mijn familie komt in december.",
            ),
            VocabularyEntry(
                "de lente",
                "noun",
                "Het seizoen tussen winter en zomer.",
                "In de lente wandelen we veel.",
            ),
            VocabularyEntry(
                "de zomer",
                "noun",
                "Het seizoen tussen lente en herfst.",
                "In de zomer zwem ik graag.",
            ),
            VocabularyEntry(
                "de herfst",
                "noun",
                "Het seizoen tussen zomer en winter.",
                "In de herfst regent het vaak.",
            ),
            VocabularyEntry(
                "de winter",
                "noun",
                "Het seizoen tussen herfst en lente.",
                "In de winter draag ik een warme jas.",
            ),
        ],
    ),
    VocabularySet(
        id="dagelijks_a1",
        level="A1",
        topic="Wat doe je iedere dag?",
        unit_ref="a1-unit-3",
        words=[
            VocabularyEntry(
                "ontbijten",
                "verb",
                "De eerste maaltijd van de dag eten.",
                "Ik ontbijt om acht uur.",
            ),
            VocabularyEntry(
                "douchen",
                "verb",
                "Je lichaam onder stromend water wassen.",
                "Ik douche iedere ochtend.",
            ),
            VocabularyEntry(
                "beginnen",
                "verb",
                "Een eerste stap zetten of van start gaan.",
                "De les begint om negen uur.",
            ),
            VocabularyEntry(
                "stoppen", "verb", "Niet verdergaan met iets.", "Ik stop om vijf uur met werken."
            ),
            VocabularyEntry("thuiskomen", "verb", "Thuis aankomen.", "Ik kom om zes uur thuis."),
            VocabularyEntry(
                "koken", "verb", "Eten klaarmaken met warmte.", "Mijn partner kookt vandaag."
            ),
            VocabularyEntry(
                "altijd", "adverb", "Op ieder moment of iedere keer.", "Ik ontbijt altijd thuis."
            ),
            VocabularyEntry("vaak", "adverb", "Op veel momenten.", "We eten vaak samen."),
            VocabularyEntry(
                "soms", "adverb", "Af en toe, niet iedere keer.", "Soms werk ik op zaterdag."
            ),
            VocabularyEntry("nooit", "adverb", "Op geen enkel moment.", "Ik werk nooit op zondag."),
        ],
    ),
    VocabularySet(
        id="voedsel_a1",
        level="A1",
        topic="Eten kiezen",
        unit_ref="a1-unit-4",
        words=[
            VocabularyEntry(
                "het ei",
                "noun",
                "Voedsel uit de schaal die een kip legt; meervoud: eieren.",
                "Ik eet een ei bij het ontbijt.",
            ),
            VocabularyEntry(
                "de rijst",
                "noun",
                "Kleine witte of bruine korrels die je gekookt eet.",
                "We eten rijst met groenten.",
            ),
            VocabularyEntry(
                "de aardappel",
                "noun",
                "Een eetbare knol; meervoud: aardappelen of aardappels.",
                "Ik koop een kilo aardappelen.",
            ),
            VocabularyEntry(
                "de groente",
                "noun",
                "Een eetbaar deel van een plant; meervoud: groenten of groentes.",
                "Ik eet iedere dag groente.",
            ),
            VocabularyEntry(
                "het fruit",
                "noun",
                "Eetbare vruchten, zoals appels en peren.",
                "Er ligt fruit op tafel.",
            ),
            VocabularyEntry(
                "het vlees",
                "noun",
                "Delen van dieren die als voedsel worden gebruikt.",
                "Ik eet geen vlees.",
            ),
            VocabularyEntry(
                "de soep",
                "noun",
                "Een vloeibaar gerecht met bijvoorbeeld groenten.",
                "De soep is warm.",
            ),
            VocabularyEntry(
                "het zout",
                "noun",
                "Een witte stof waarmee je eten hartiger maakt.",
                "Er zit veel zout in de soep.",
            ),
            VocabularyEntry(
                "de suiker",
                "noun",
                "Een zoete stof die je aan eten of drinken toevoegt.",
                "Wilt u suiker in de thee?",
            ),
            VocabularyEntry(
                "vegetarisch",
                "adjective",
                "Zonder vlees of vis als voedingsmiddel.",
                "Heeft u een vegetarisch gerecht?",
            ),
        ],
    ),
    VocabularySet(
        id="hoeveelheden_a1",
        level="A1",
        topic="Porties en servies",
        unit_ref="a1-unit-4",
        words=[
            VocabularyEntry(
                "het glas",
                "noun",
                "Een voorwerp waaruit je drinkt; meervoud: glazen.",
                "Mag ik een glas water?",
            ),
            VocabularyEntry(
                "het kopje",
                "noun",
                "Een klein drinkbakje met een oor; meervoud: kopjes.",
                "Ik wil een kopje koffie.",
            ),
            VocabularyEntry(
                "het bord",
                "noun",
                "Een plat voorwerp waarop je eten legt; meervoud: borden.",
                "Het brood ligt op het bord.",
            ),
            VocabularyEntry(
                "de lepel",
                "noun",
                "Een voorwerp waarmee je bijvoorbeeld soep eet; meervoud: lepels.",
                "Ik heb een lepel nodig.",
            ),
            VocabularyEntry(
                "de fles",
                "noun",
                "Een verpakking voor vloeistof met een smalle opening; meervoud: flessen.",
                "Er staat een fles water op tafel.",
            ),
            VocabularyEntry(
                "de kilo", "noun", "Duizend gram; meervoud: kilo's.", "Ik koop een kilo appels."
            ),
            VocabularyEntry(
                "de liter",
                "noun",
                "Een maat voor hoeveel vloeistof iets bevat; meervoud: liters.",
                "Deze fles bevat een liter water.",
            ),
            VocabularyEntry(
                "het stuk", "noun", "Een deel van iets; meervoud: stukken.", "Wil je een stuk kaas?"
            ),
            VocabularyEntry("veel", "numeral", "Een grote hoeveelheid.", "Ik drink veel water."),
            VocabularyEntry("weinig", "numeral", "Een kleine hoeveelheid.", "Er is weinig melk."),
        ],
    ),
    VocabularySet(
        id="vervoer_a1",
        level="A1",
        topic="Een korte reis",
        unit_ref="a1-unit-5",
        words=[
            VocabularyEntry(
                "de bus",
                "noun",
                "Een groot voertuig voor meerdere reizigers; meervoud: bussen.",
                "De bus stopt hier.",
            ),
            VocabularyEntry(
                "de tram",
                "noun",
                "Een voertuig op rails door de stad; meervoud: trams.",
                "Ik neem de tram naar het centrum.",
            ),
            VocabularyEntry(
                "de auto",
                "noun",
                "Een motorvoertuig voor enkele personen; meervoud: auto's.",
                "Mijn auto staat buiten.",
            ),
            VocabularyEntry(
                "de halte",
                "noun",
                "Een plaats waar een bus of tram stopt; meervoud: haltes.",
                "Waar is de halte?",
            ),
            VocabularyEntry(
                "het centrum",
                "noun",
                "Het centrale deel van een stad of dorp; meervoud: centra.",
                "De winkel is in het centrum.",
            ),
            VocabularyEntry(
                "lopen", "verb", "Je verplaatsen op je voeten.", "Ik loop naar school."
            ),
            VocabularyEntry(
                "fietsen", "verb", "Je met een fiets verplaatsen.", "We fietsen naar het station."
            ),
            VocabularyEntry(
                "rijden",
                "verb",
                "Je verplaatsen met een voertuig op wielen.",
                "Deze bus rijdt naar Delft.",
            ),
            VocabularyEntry(
                "dichtbij", "adverb", "Op een kleine afstand.", "Het station is dichtbij."
            ),
            VocabularyEntry("ver", "adjective", "Op een grote afstand.", "Is het nog ver?"),
        ],
    ),
    VocabularySet(
        id="weer_a1",
        level="A1",
        topic="Het weer buiten",
        unit_ref="a1-unit-5",
        words=[
            VocabularyEntry(
                "de zon", "noun", "De ster die overdag licht en warmte geeft.", "De zon schijnt."
            ),
            VocabularyEntry(
                "de regen",
                "noun",
                "Waterdruppels die uit de wolken vallen.",
                "Ik fiets niet graag in de regen.",
            ),
            VocabularyEntry("de wind", "noun", "Lucht die buiten beweegt.", "Er staat veel wind."),
            VocabularyEntry(
                "de sneeuw",
                "noun",
                "Witte, bevroren vlokken die uit de lucht vallen.",
                "Er ligt sneeuw in de tuin.",
            ),
            VocabularyEntry(
                "de wolk",
                "noun",
                "Kleine waterdruppels of ijskristallen samen in de lucht; meervoud: wolken.",
                "Ik zie een donkere wolk.",
            ),
            VocabularyEntry(
                "regenen",
                "verb",
                "Waterdruppels uit de lucht laten vallen, gezegd van het weer.",
                "Het regent vandaag.",
            ),
            VocabularyEntry("schijnen", "verb", "Licht geven.", "De zon schijnt door het raam."),
            VocabularyEntry("nat", "adjective", "Met water erop of erin.", "Mijn jas is nat."),
            VocabularyEntry(
                "droog", "adjective", "Zonder water of regen.", "Mijn schoenen zijn droog."
            ),
            VocabularyEntry(
                "het weer",
                "noun",
                "De toestand van de lucht buiten, zoals regen of zon.",
                "Het weer is mooi vandaag.",
            ),
        ],
    ),
    VocabularySet(
        id="sport_a1",
        level="A1",
        topic="Bewegen en ontspannen",
        unit_ref="a1-unit-6",
        words=[
            VocabularyEntry(
                "de sport",
                "noun",
                "Een lichamelijke activiteit met oefening of spelregels; meervoud: sporten.",
                "Welke sport doe je?",
            ),
            VocabularyEntry(
                "voetballen",
                "verb",
                "Met een bal een spel spelen waarbij je vooral je voeten gebruikt.",
                "Mijn broer voetbalt op zaterdag.",
            ),
            VocabularyEntry("hardlopen", "verb", "Snel lopen als sport.", "Ik loop graag hard."),
            VocabularyEntry("dansen", "verb", "Je lichaam op muziek bewegen.", "We dansen samen."),
            VocabularyEntry("zingen", "verb", "Met je stem muziek maken.", "Zij zingt graag."),
            VocabularyEntry(
                "tekenen", "verb", "Een afbeelding maken met lijnen.", "Ik teken een huis."
            ),
            VocabularyEntry(
                "spelen",
                "verb",
                "Voor je plezier een activiteit of spel doen.",
                "De kinderen spelen buiten.",
            ),
            VocabularyEntry(
                "luisteren", "verb", "Aandacht geven aan wat je hoort.", "Ik luister naar muziek."
            ),
            VocabularyEntry(
                "het park",
                "noun",
                "Een groene openbare plek om te wandelen of te spelen; meervoud: parken.",
                "Het park is dichtbij.",
            ),
            VocabularyEntry(
                "het zwembad",
                "noun",
                "Een plek met water om te zwemmen; meervoud: zwembaden.",
                "Het zwembad is open.",
            ),
        ],
    ),
    VocabularySet(
        id="gevoelens_a1",
        level="A1",
        topic="Hoe gaat het?",
        unit_ref="a1-unit-6",
        words=[
            VocabularyEntry(
                "blij",
                "adjective",
                "Met een prettig, vrolijk gevoel.",
                "Ik ben blij met je bericht.",
            ),
            VocabularyEntry(
                "verdrietig",
                "adjective",
                "Met een gevoel van pijn of gemis.",
                "Zij is vandaag verdrietig.",
            ),
            VocabularyEntry(
                "moe",
                "adjective",
                "Met weinig energie en behoefte aan rust.",
                "Na mijn werk ben ik moe.",
            ),
            VocabularyEntry("ziek", "adjective", "Niet gezond.", "Mijn vriend is ziek."),
            VocabularyEntry(
                "boos",
                "adjective",
                "Met een sterk gevoel dat iets niet goed of eerlijk is.",
                "Ben je boos op mij?",
            ),
            VocabularyEntry(
                "bang",
                "adjective",
                "Met angst voor iets of iemand.",
                "Ik ben bang voor grote honden.",
            ),
            VocabularyEntry("honger", "noun", "Het gevoel dat je wilt eten.", "Ik heb honger."),
            VocabularyEntry("dorst", "noun", "Het gevoel dat je wilt drinken.", "Heb je dorst?"),
            VocabularyEntry("leuk", "adjective", "Prettig of plezierig.", "Dat is een leuke film."),
            VocabularyEntry(
                "saai", "adjective", "Met weinig afwisseling of plezier.", "Ik vind die film saai."
            ),
        ],
    ),
    VocabularySet(
        id="boodschappen_a1",
        level="A1",
        topic="In de winkel",
        unit_ref="a1-unit-7",
        words=[
            VocabularyEntry(
                "de tas",
                "noun",
                "Een voorwerp waarin je spullen draagt; meervoud: tassen.",
                "Heeft u een tas?",
            ),
            VocabularyEntry(
                "de kassa",
                "noun",
                "De plaats in een winkel waar je betaalt; meervoud: kassa's.",
                "Ik betaal bij de kassa.",
            ),
            VocabularyEntry(
                "de pinpas",
                "noun",
                "Een kaart waarmee je via je bank betaalt; meervoud: pinpassen.",
                "Kan ik met mijn pinpas betalen?",
            ),
            VocabularyEntry(
                "het geld",
                "noun",
                "Munten, biljetten of een bedrag op een rekening.",
                "Ik heb geen geld bij me.",
            ),
            VocabularyEntry(
                "kopen", "verb", "Iets tegen betaling krijgen.", "Ik koop een nieuwe jas."
            ),
            VocabularyEntry(
                "kosten", "verb", "Een bepaalde prijs hebben.", "Hoeveel kosten deze appels?"
            ),
            VocabularyEntry(
                "zoeken", "verb", "Proberen iets te vinden.", "Ik zoek een kleine tas."
            ),
            VocabularyEntry(
                "open", "adjective", "Toegankelijk; niet gesloten.", "De supermarkt is open."
            ),
            VocabularyEntry(
                "dicht",
                "adjective",
                "Gesloten; niet toegankelijk.",
                "De winkel is op zondag dicht.",
            ),
            VocabularyEntry("contant", "adverb", "Met munten of biljetten.", "Ik betaal contant."),
        ],
    ),
    VocabularySet(
        id="persoonlijk_a1",
        level="A1",
        topic="Kleding en persoonlijke spullen",
        unit_ref="a1-unit-7",
        words=[
            VocabularyEntry(
                "het shirt",
                "noun",
                "Een dun kledingstuk voor het bovenlichaam; meervoud: shirts.",
                "Dit shirt is te klein.",
            ),
            VocabularyEntry(
                "de trui",
                "noun",
                "Een warm kledingstuk voor het bovenlichaam; meervoud: truien.",
                "Ik draag een warme trui.",
            ),
            VocabularyEntry(
                "de rok",
                "noun",
                "Een kledingstuk vanaf de taille zonder broekspijpen; meervoud: rokken.",
                "Die rok is rood.",
            ),
            VocabularyEntry(
                "de sok",
                "noun",
                "Een kledingstuk voor de voet; meervoud: sokken.",
                "Waar zijn mijn sokken?",
            ),
            VocabularyEntry(
                "de paraplu",
                "noun",
                "Een scherm dat je boven je hoofd tegen de regen houdt; meervoud: paraplu's.",
                "Ik neem een paraplu mee.",
            ),
            VocabularyEntry(
                "het horloge",
                "noun",
                "Een kleine klok die je bij je draagt; meervoud: horloges.",
                "Mijn horloge ligt op tafel.",
            ),
            VocabularyEntry(
                "de portemonnee",
                "noun",
                "Een klein hoesje voor geld en pasjes; meervoud: portemonnees.",
                "Mijn portemonnee zit in mijn tas.",
            ),
            VocabularyEntry(
                "bruin",
                "adjective",
                "Met de kleur van bijvoorbeeld chocolade.",
                "Ik zoek bruine schoenen.",
            ),
            VocabularyEntry(
                "grijs", "adjective", "Met een kleur tussen wit en zwart.", "Mijn jas is grijs."
            ),
            VocabularyEntry(
                "mooi", "adjective", "Prettig om naar te kijken.", "Dat is een mooie trui."
            ),
        ],
    ),
]
