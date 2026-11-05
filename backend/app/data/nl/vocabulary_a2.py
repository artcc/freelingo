"""Dutch A2 vocabulary for practical independent exchanges."""

from app.data._types import VocabularyEntry, VocabularySet

A2_SETS: list[VocabularySet] = [
    VocabularySet(
        id="reizen_a2",
        level="A2",
        topic="Een reis maken",
        unit_ref="a2-unit-1",
        words=[
            VocabularyEntry(
                "het kaartje",
                "noun",
                "Een bewijs dat je voor een reis of toegang hebt betaald.",
                "Ik heb een kaartje gekocht.",
            ),
            VocabularyEntry(
                "het perron",
                "noun",
                "De plek langs het spoor waar reizigers wachten.",
                "We wachten op het perron.",
            ),
            VocabularyEntry(
                "de vertraging",
                "noun",
                "De extra tijd waardoor iets later gebeurt dan gepland.",
                "De trein heeft tien minuten vertraging.",
            ),
            VocabularyEntry(
                "de overstap",
                "noun",
                "Het wisselen van het ene vervoermiddel naar het andere.",
                "In Utrecht hebben we een overstap.",
            ),
            VocabularyEntry(
                "de bagage",
                "noun",
                "Tassen en koffers die je op reis meeneemt.",
                "Mijn bagage staat naast de deur.",
            ),
            VocabularyEntry(
                "het verblijf",
                "noun",
                "De tijd die je ergens doorbrengt.",
                "Ons verblijf duurde drie dagen.",
            ),
            VocabularyEntry(
                "vertrekken",
                "verb",
                "Een plaats verlaten om ergens anders heen te gaan.",
                "We zijn vroeg vertrokken.",
            ),
            VocabularyEntry(
                "aankomen", "verb", "De bestemming bereiken.", "Wanneer ben je aangekomen?"
            ),
            VocabularyEntry(
                "overstappen",
                "verb",
                "Tijdens een reis een ander vervoermiddel nemen.",
                "Ik moet in Amersfoort overstappen.",
            ),
            VocabularyEntry(
                "reserveren",
                "verb",
                "Vooraf een plaats of dienst vastleggen.",
                "We hebben een kamer gereserveerd.",
            ),
        ],
    ),
    VocabularySet(
        id="herinneringen_a2",
        level="A2",
        topic="Vroeger en verandering",
        unit_ref="a2-unit-2",
        words=[
            VocabularyEntry(
                "de jeugd",
                "noun",
                "De periode waarin iemand kind of jongere is.",
                "Mijn jeugd was prettig.",
            ),
            VocabularyEntry(
                "de herinnering",
                "noun",
                "Iets uit het verleden dat je nog weet.",
                "Ik heb een mooie herinnering aan die reis.",
            ),
            VocabularyEntry(
                "de vakantie",
                "noun",
                "Een periode waarin je vrij bent van werk of school.",
                "Tijdens de vakantie gingen we kamperen.",
            ),
            VocabularyEntry(
                "de gewoonte",
                "noun",
                "Iets wat je vaak op dezelfde manier doet.",
                "Vroeg opstaan was een gewoonte.",
            ),
            VocabularyEntry(
                "vroeger", "adverb", "In een periode vóór nu.", "Vroeger woonden we in een dorp."
            ),
            VocabularyEntry(
                "toen", "adverb", "Op dat moment in het verleden.", "Ik was toen tien jaar."
            ),
            VocabularyEntry(
                "verhuizen",
                "verb",
                "Op een ander adres gaan wonen.",
                "Wij verhuisden naar Haarlem.",
            ),
            VocabularyEntry(
                "veranderen", "verb", "Anders worden of anders maken.", "De buurt is veranderd."
            ),
            VocabularyEntry(
                "ontmoeten",
                "verb",
                "Bij iemand komen en contact maken.",
                "Ik ontmoette haar op school.",
            ),
            VocabularyEntry(
                "vergeten",
                "verb",
                "Iets niet meer weten of er niet aan denken.",
                "Ik heb zijn naam vergeten.",
            ),
        ],
    ),
    VocabularySet(
        id="afspraken_a2",
        level="A2",
        topic="Tijden en wijzigingen",
        unit_ref="a2-unit-3",
        words=[
            VocabularyEntry(
                "de afspraak",
                "noun",
                "Een gezamenlijk vastgelegde tijd of regeling.",
                "Onze afspraak is om tien uur.",
            ),
            VocabularyEntry(
                "de agenda",
                "noun",
                "Een overzicht waarin je afspraken noteert.",
                "Ik kijk even in mijn agenda.",
            ),
            VocabularyEntry(
                "de reden",
                "noun",
                "Waarom iemand iets doet of iets gebeurt.",
                "Wat is de reden voor de wijziging?",
            ),
            VocabularyEntry(
                "de wijziging",
                "noun",
                "Een verschil met wat eerder was afgesproken.",
                "Er is een wijziging in het programma.",
            ),
            VocabularyEntry(
                "beschikbaar",
                "adjective",
                "Vrij om gebruikt te worden of mee te doen.",
                "Ben je maandag beschikbaar?",
            ),
            VocabularyEntry(
                "druk",
                "adjective",
                "Met veel werk, activiteiten of mensen.",
                "Ik heb een drukke week.",
            ),
            VocabularyEntry(
                "uitstellen",
                "verb",
                "Iets later laten gebeuren dan gepland.",
                "We stellen de afspraak uit.",
            ),
            VocabularyEntry(
                "afzeggen",
                "verb",
                "Laten weten dat een afspraak niet doorgaat.",
                "Ik moet mijn afspraak afzeggen.",
            ),
            VocabularyEntry(
                "bevestigen",
                "verb",
                "Laten weten dat iets klopt of doorgaat.",
                "Kunt u de tijd bevestigen?",
            ),
            VocabularyEntry(
                "op tijd", "phrase", "Niet later dan de afgesproken tijd.", "Ik ben morgen op tijd."
            ),
        ],
    ),
    VocabularySet(
        id="wonen_a2",
        level="A2",
        topic="Een woning zoeken",
        unit_ref="a2-unit-4",
        words=[
            VocabularyEntry(
                "de huur",
                "noun",
                "Het bedrag dat je betaalt om iets tijdelijk te gebruiken.",
                "De huur is hoger dan vorig jaar.",
            ),
            VocabularyEntry(
                "de verhuurder",
                "noun",
                "Iemand die een woning of zaak tegen betaling laat gebruiken.",
                "De verhuurder repareert de deur.",
            ),
            VocabularyEntry(
                "de huurder",
                "noun",
                "Iemand die betaalt om een woning of zaak te gebruiken.",
                "De huurder krijgt een sleutel.",
            ),
            VocabularyEntry(
                "de verdieping",
                "noun",
                "Een woon- of werklaag in een gebouw.",
                "Wij wonen op de tweede verdieping.",
            ),
            VocabularyEntry(
                "het balkon",
                "noun",
                "Een kleine buitenruimte aan een hogere verdieping.",
                "De woning heeft een balkon.",
            ),
            VocabularyEntry(
                "de verwarming",
                "noun",
                "Een systeem dat een ruimte warm maakt.",
                "De verwarming staat aan.",
            ),
            VocabularyEntry(
                "de sleutel",
                "noun",
                "Een voorwerp waarmee je een slot opent.",
                "Ik heb twee sleutels.",
            ),
            VocabularyEntry("ruim", "adjective", "Met veel plaats.", "De woonkamer is ruim."),
            VocabularyEntry(
                "rustig", "adjective", "Met weinig lawaai of drukte.", "Dit is een rustige straat."
            ),
            VocabularyEntry(
                "huren",
                "verb",
                "Betalen om iets tijdelijk te gebruiken.",
                "We willen een appartement huren.",
            ),
        ],
    ),
    VocabularySet(
        id="gezondheid_a2",
        level="A2",
        topic="Klachten en hulp",
        unit_ref="a2-unit-5",
        words=[
            VocabularyEntry(
                "de huisarts",
                "noun",
                "Een arts voor algemene klachten en eerste medische hulp.",
                "Ik maak een afspraak bij de huisarts.",
            ),
            VocabularyEntry(
                "de apotheek",
                "noun",
                "Een plaats waar je medicijnen krijgt of koopt.",
                "Het recept ligt bij de apotheek.",
            ),
            VocabularyEntry(
                "de pijn",
                "noun",
                "Een onaangenaam gevoel in je lichaam.",
                "Ik heb pijn in mijn rug.",
            ),
            VocabularyEntry(
                "de koorts",
                "noun",
                "Een lichaamstemperatuur die hoger is dan normaal bij ziekte.",
                "Ik heb sinds gisteren koorts.",
            ),
            VocabularyEntry(
                "de klacht",
                "noun",
                "Een probleem dat iemand ervaart, bijvoorbeeld met de gezondheid.",
                "Welke klachten heeft u?",
            ),
            VocabularyEntry(
                "het medicijn",
                "noun",
                "Een middel om een ziekte of klacht te behandelen.",
                "Vraag de apotheker hoe je het medicijn gebruikt.",
            ),
            VocabularyEntry(
                "het recept",
                "noun",
                "Een voorschrift van een bevoegde behandelaar voor medicijnen.",
                "De arts schrijft een recept.",
            ),
            VocabularyEntry(
                "hoesten", "verb", "Lucht plotseling uit je keel stoten.", "Ik moet vaak hoesten."
            ),
            VocabularyEntry(
                "uitrusten",
                "verb",
                "Rust nemen om weer energie te krijgen.",
                "Ik ga thuis uitrusten.",
            ),
            VocabularyEntry(
                "zich voelen",
                "verb",
                "Een lichamelijke of emotionele toestand ervaren.",
                "Ik voel me vandaag beter.",
            ),
        ],
    ),
    VocabularySet(
        id="werk_a2",
        level="A2",
        topic="Werk en opleiding",
        unit_ref="a2-unit-6",
        words=[
            VocabularyEntry(
                "de collega", "noun", "Iemand met wie je werkt.", "Mijn collega helpt me."
            ),
            VocabularyEntry(
                "het rooster",
                "noun",
                "Een overzicht van werk- of lestijden.",
                "Het nieuwe rooster begint maandag.",
            ),
            VocabularyEntry(
                "de pauze",
                "noun",
                "Een korte onderbreking om te rusten.",
                "We hebben om twaalf uur pauze.",
            ),
            VocabularyEntry(
                "de cursus",
                "noun",
                "Een reeks lessen over een onderwerp of vaardigheid.",
                "Ik volg een cursus Nederlands.",
            ),
            VocabularyEntry(
                "de opleiding",
                "noun",
                "Lessen en oefening voor een beroep of niveau.",
                "Zij begint een nieuwe opleiding.",
            ),
            VocabularyEntry(
                "het formulier",
                "noun",
                "Een document waarop je gevraagde gegevens invult.",
                "Vul dit formulier in.",
            ),
            VocabularyEntry(
                "de ervaring",
                "noun",
                "Kennis die je krijgt door iets zelf te doen.",
                "Ik heb ervaring in een winkel.",
            ),
            VocabularyEntry(
                "solliciteren",
                "verb",
                "Vragen of je een bepaalde baan kunt krijgen.",
                "Ik ga bij een boekwinkel solliciteren.",
            ),
            VocabularyEntry(
                "zich aanmelden",
                "verb",
                "Laten weten dat je wilt deelnemen.",
                "Ik meld me aan voor de cursus.",
            ),
            VocabularyEntry(
                "oefenen", "verb", "Iets herhalen om het beter te leren.", "We oefenen iedere dag."
            ),
        ],
    ),
    VocabularySet(
        id="service_a2",
        level="A2",
        topic="Een probleem oplossen",
        unit_ref="a2-unit-7",
        words=[
            VocabularyEntry(
                "de bestelling",
                "noun",
                "Producten of diensten die je hebt aangevraagd om te kopen.",
                "Mijn bestelling is niet aangekomen.",
            ),
            VocabularyEntry(
                "de bon",
                "noun",
                "Een bewijs van wat je hebt gekocht en betaald.",
                "Ik heb de bon bewaard.",
            ),
            VocabularyEntry(
                "de garantie",
                "noun",
                "Een toezegging over herstel of kwaliteit onder bepaalde voorwaarden.",
                "Valt deze reparatie onder de garantie?",
            ),
            VocabularyEntry(
                "de klantenservice",
                "noun",
                "De afdeling die klanten helpt met vragen en problemen.",
                "Ik bel de klantenservice.",
            ),
            VocabularyEntry(
                "het pakket",
                "noun",
                "Een ingepakt voorwerp dat wordt verstuurd.",
                "Het pakket is beschadigd.",
            ),
            VocabularyEntry(
                "kapot",
                "adjective",
                "Niet meer heel of niet meer werkend.",
                "Mijn telefoon is kapot.",
            ),
            VocabularyEntry(
                "ruilen",
                "verb",
                "Iets teruggeven en iets anders ervoor krijgen.",
                "Kan ik deze jas ruilen?",
            ),
            VocabularyEntry(
                "repareren",
                "verb",
                "Iets dat kapot is weer goed maken.",
                "De monteur repareert mijn fiets.",
            ),
            VocabularyEntry(
                "terugsturen",
                "verb",
                "Iets weer naar de afzender zenden.",
                "Ik stuur het pakket terug.",
            ),
            VocabularyEntry(
                "oplossen",
                "verb",
                "Zorgen dat een probleem verdwijnt.",
                "Hoe kunnen we dit oplossen?",
            ),
        ],
    ),
    VocabularySet(
        id="samen_a2",
        level="A2",
        topic="Een activiteit organiseren",
        unit_ref="a2-unit-8",
        words=[
            VocabularyEntry(
                "de uitnodiging",
                "noun",
                "Een verzoek om bij een activiteit aanwezig te zijn.",
                "Bedankt voor de uitnodiging.",
            ),
            VocabularyEntry(
                "de deelnemer",
                "noun",
                "Iemand die aan een activiteit meedoet.",
                "Er zijn twintig deelnemers.",
            ),
            VocabularyEntry(
                "de ingang",
                "noun",
                "De plaats waar je een gebouw binnenkomt.",
                "We wachten bij de ingang.",
            ),
            VocabularyEntry(
                "de uitgang",
                "noun",
                "De plaats waar je een gebouw verlaat.",
                "De uitgang is aan de andere kant.",
            ),
            VocabularyEntry(
                "de bijdrage",
                "noun",
                "Geld, werk of iets anders waarmee je helpt.",
                "Iedereen betaalt een kleine bijdrage.",
            ),
            VocabularyEntry(
                "meenemen",
                "verb",
                "Iets bij je hebben als je ergens heen gaat.",
                "Neem iets te drinken mee.",
            ),
            VocabularyEntry(
                "doorgaan",
                "verb",
                "Toch of volgens plan plaatsvinden; ook verdergaan.",
                "Het feest gaat morgen door.",
            ),
            VocabularyEntry(
                "voorbereiden",
                "verb",
                "Vooraf regelen wat later nodig is.",
                "We bereiden de activiteit samen voor.",
            ),
            VocabularyEntry(
                "verdelen",
                "verb",
                "Delen aan verschillende personen geven.",
                "We verdelen de taken.",
            ),
            VocabularyEntry(
                "gezellig",
                "adjective",
                "Prettig door sfeer of samenzijn.",
                "Het was een gezellige avond.",
            ),
        ],
    ),
]
