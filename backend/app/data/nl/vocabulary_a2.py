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
    VocabularySet(
        id="onderweg_a2",
        level="A2",
        topic="Reisinformatie en verblijf",
        unit_ref="a2-unit-1",
        words=[
            VocabularyEntry(
                "de bestemming",
                "noun",
                "De plaats waar je naartoe reist; meervoud: bestemmingen.",
                "Onze bestemming is Maastricht.",
            ),
            VocabularyEntry(
                "de vertrekhal",
                "noun",
                "De ruimte waar vertrekkende reizigers wachten; meervoud: vertrekhallen.",
                "We hebben in de vertrekhal gewacht.",
            ),
            VocabularyEntry(
                "de aansluiting",
                "noun",
                "Een volgende trein of bus die past bij je reis; meervoud: aansluitingen.",
                "We hebben onze aansluiting gemist.",
            ),
            VocabularyEntry(
                "de route",
                "noun",
                "De weg die je volgt naar een plaats; meervoud: routes.",
                "Welke route hebben jullie genomen?",
            ),
            VocabularyEntry(
                "de accommodatie",
                "noun",
                "Een plek waar je tijdens een reis verblijft; meervoud: accommodaties.",
                "Onze accommodatie ligt bij het strand.",
            ),
            VocabularyEntry(
                "inchecken",
                "verb",
                "Je bij aankomst of aan het begin van een reis aanmelden.",
                "We hebben bij het hotel ingecheckt.",
            ),
            VocabularyEntry(
                "uitchecken",
                "verb",
                "Je vertrek registreren of een reisbetaling afsluiten.",
                "Vergeet niet uit te checken na je treinreis.",
            ),
            VocabularyEntry(
                "instappen",
                "verb",
                "Een voertuig binnengaan om mee te reizen.",
                "We zijn in de verkeerde bus ingestapt.",
            ),
            VocabularyEntry(
                "uitstappen",
                "verb",
                "Een voertuig verlaten na een reisdeel.",
                "Ik ben bij het centrum uitgestapt.",
            ),
            VocabularyEntry(
                "rechtstreeks",
                "adverb",
                "Zonder tussentijds van route of vervoermiddel te wisselen.",
                "Deze trein rijdt rechtstreeks naar Arnhem.",
            ),
        ],
    ),
    VocabularySet(
        id="levensloop_a2",
        level="A2",
        topic="Veranderingen in je leven",
        unit_ref="a2-unit-2",
        words=[
            VocabularyEntry(
                "de geboorte",
                "noun",
                "Het moment waarop een kind ter wereld komt; meervoud: geboorten.",
                "Na de geboorte van hun dochter verhuisden ze.",
            ),
            VocabularyEntry(
                "de verjaardag",
                "noun",
                "De jaarlijkse dag waarop iemand zijn geboorte viert; meervoud: verjaardagen.",
                "Vroeger vierden we mijn verjaardag thuis.",
            ),
            VocabularyEntry(
                "de bruiloft",
                "noun",
                "Het feest bij een huwelijk; meervoud: bruiloften.",
                "De bruiloft was in juni.",
            ),
            VocabularyEntry(
                "het pensioen",
                "noun",
                "Inkomen dat iemand meestal na het werkzame leven ontvangt; meervoud: pensioenen.",
                "Mijn vader ging vorig jaar met pensioen.",
            ),
            VocabularyEntry(
                "de verhuizing",
                "noun",
                "Het overgaan naar een andere woning; meervoud: verhuizingen.",
                "De verhuizing duurde een hele dag.",
            ),
            VocabularyEntry(
                "opgroeien",
                "verb",
                "Van kind geleidelijk volwassen worden.",
                "Ik ben in een klein dorp opgegroeid.",
            ),
            VocabularyEntry(
                "trouwen", "verb", "Een huwelijk sluiten.", "Mijn ouders trouwden in Rotterdam."
            ),
            VocabularyEntry(
                "geboren worden", "phrase", "Ter wereld komen.", "Ik ben in Utrecht geboren."
            ),
            VocabularyEntry(
                "destijds",
                "adverb",
                "In de periode waarover je vertelt.",
                "Destijds hadden we geen auto.",
            ),
            VocabularyEntry(
                "inmiddels",
                "adverb",
                "Nu, na de veranderingen sinds een eerder moment.",
                "Inmiddels wonen we in een grotere woning.",
            ),
        ],
    ),
    VocabularySet(
        id="planning_a2",
        level="A2",
        topic="Een tijd afspreken",
        unit_ref="a2-unit-3",
        words=[
            VocabularyEntry(
                "de openingstijd",
                "noun",
                "De periode waarin een voorziening open is; meervoud: openingstijden.",
                "De openingstijden staan op de deur.",
            ),
            VocabularyEntry(
                "de sluitingstijd",
                "noun",
                "Het tijdstip waarop een voorziening dichtgaat; meervoud: sluitingstijden.",
                "Wat is de sluitingstijd op vrijdag?",
            ),
            VocabularyEntry(
                "het tijdstip",
                "noun",
                "Een bepaald moment; meervoud: tijdstippen.",
                "Past dit tijdstip voor jou?",
            ),
            VocabularyEntry(
                "de duur",
                "noun",
                "De hoeveelheid tijd die iets in beslag neemt.",
                "De duur van het gesprek is een halfuur.",
            ),
            VocabularyEntry(
                "de wachttijd",
                "noun",
                "De tijd voordat je aan de beurt bent; meervoud: wachttijden.",
                "De wachttijd is vandaag kort.",
            ),
            VocabularyEntry(
                "verplaatsen",
                "verb",
                "Iets naar een andere plek of een ander tijdstip brengen.",
                "We verplaatsen de afspraak naar donderdag.",
            ),
            VocabularyEntry(
                "opschrijven",
                "verb",
                "Informatie met letters vastleggen.",
                "Ik schrijf de nieuwe datum op.",
            ),
            VocabularyEntry(
                "uiterlijk",
                "adverb",
                "Niet later dan het genoemde tijdstip.",
                "Bel mij uiterlijk vrijdag.",
            ),
            VocabularyEntry(
                "ongeveer",
                "adverb",
                "Niet precies, maar dicht bij het genoemde aantal of moment.",
                "Het gesprek duurt ongeveer twintig minuten.",
            ),
            VocabularyEntry(
                "ondertussen",
                "adverb",
                "In de tijd dat iets anders gebeurt.",
                "Ik wacht op de bus en lees ondertussen een bericht.",
            ),
        ],
    ),
    VocabularySet(
        id="huishouden_a2",
        level="A2",
        topic="Het huis verzorgen",
        unit_ref="a2-unit-4",
        words=[
            VocabularyEntry(
                "de koelkast",
                "noun",
                "Een apparaat dat eten en drinken koud houdt; meervoud: koelkasten.",
                "De melk staat in de koelkast.",
            ),
            VocabularyEntry(
                "de wasmachine",
                "noun",
                "Een apparaat om kleding te wassen; meervoud: wasmachines.",
                "Deze wasmachine is zuiniger dan die andere.",
            ),
            VocabularyEntry(
                "de stofzuiger",
                "noun",
                "Een apparaat dat stof en vuil opzuigt; meervoud: stofzuigers.",
                "Onze stofzuiger maakt veel lawaai.",
            ),
            VocabularyEntry(
                "het stopcontact",
                "noun",
                "Een aansluiting in de muur voor elektriciteit; meervoud: stopcontacten.",
                "Er zijn twee stopcontacten naast het bed.",
            ),
            VocabularyEntry(
                "de kraan",
                "noun",
                "Een voorziening waarmee je water laat stromen; meervoud: kranen.",
                "De kraan in de keuken lekt.",
            ),
            VocabularyEntry(
                "schoonmaken", "verb", "Vuil verwijderen.", "We maken de keuken samen schoon."
            ),
            VocabularyEntry(
                "opruimen", "verb", "Spullen op hun plaats leggen.", "Ik ruim mijn kamer op."
            ),
            VocabularyEntry(
                "afwassen",
                "verb",
                "Borden en ander servies schoonmaken.",
                "Na het eten wassen we af.",
            ),
            VocabularyEntry(
                "zuinig",
                "adjective",
                "Weinig geld of energie gebruikend.",
                "Dit apparaat is zuinig.",
            ),
            VocabularyEntry("vuil", "adjective", "Niet schoon.", "Deze handdoek is vuil."),
        ],
    ),
    VocabularySet(
        id="lichaam_a2",
        level="A2",
        topic="Waar heb je last van?",
        unit_ref="a2-unit-5",
        words=[
            VocabularyEntry(
                "het hoofd",
                "noun",
                "Het lichaamsdeel boven je nek; meervoud: hoofden.",
                "Ik heb pijn in mijn hoofd.",
            ),
            VocabularyEntry(
                "de keel",
                "noun",
                "De ruimte achter in je mond waardoor je slikt; meervoud: kelen.",
                "Mijn keel doet pijn.",
            ),
            VocabularyEntry(
                "de rug",
                "noun",
                "De achterkant van je lichaam tussen nek en bekken; meervoud: ruggen.",
                "Ik heb last van mijn rug.",
            ),
            VocabularyEntry(
                "de buik",
                "noun",
                "Het lichaamsdeel tussen borst en bekken; meervoud: buiken.",
                "Mijn buik doet sinds vanochtend pijn.",
            ),
            VocabularyEntry(
                "de arm",
                "noun",
                "Een lichaamsdeel tussen schouder en hand; meervoud: armen.",
                "Ik kan mijn arm moeilijk bewegen.",
            ),
            VocabularyEntry(
                "de hand",
                "noun",
                "Het lichaamsdeel aan het einde van je arm; meervoud: handen.",
                "Was je handen voor het eten.",
            ),
            VocabularyEntry(
                "het been",
                "noun",
                "Een lichaamsdeel waarop je staat en loopt; meervoud: benen.",
                "Mijn rechterbeen is dik.",
            ),
            VocabularyEntry(
                "de voet",
                "noun",
                "Het onderste deel van je been; meervoud: voeten.",
                "Deze schoen doet pijn aan mijn voet.",
            ),
            VocabularyEntry(
                "de knie",
                "noun",
                "Het gewricht midden in je been; meervoud: knieën.",
                "Ik kan mijn knie niet goed buigen.",
            ),
            VocabularyEntry(
                "de tand",
                "noun",
                "Een hard deel in je mond om mee te bijten; meervoud: tanden.",
                "Deze tand doet pijn.",
            ),
        ],
    ),
    VocabularySet(
        id="zorg_a2",
        level="A2",
        topic="Bij een zorgverlener",
        unit_ref="a2-unit-5",
        words=[
            VocabularyEntry(
                "de tandarts",
                "noun",
                "Een zorgverlener die tanden onderzoekt en behandelt; meervoud: tandartsen.",
                "Ik wil een afspraak bij de tandarts maken.",
            ),
            VocabularyEntry(
                "de assistent",
                "noun",
                "Iemand die een beroepskracht helpt; meervoud: assistenten.",
                "De assistent vraagt naar mijn klachten.",
            ),
            VocabularyEntry(
                "de wachtkamer",
                "noun",
                "Een ruimte waar je wacht tot je afspraak begint; meervoud: wachtkamers.",
                "Neem plaats in de wachtkamer.",
            ),
            VocabularyEntry(
                "de allergie",
                "noun",
                "Een reactie van het lichaam op een bepaalde stof; meervoud: allergieën.",
                "Ik vertel de arts dat ik een allergie heb.",
            ),
            VocabularyEntry(
                "de bijwerking",
                "noun",
                "Een onbedoeld effect van een medicijn; meervoud: bijwerkingen.",
                "Welke bijwerkingen kan dit medicijn hebben?",
            ),
            VocabularyEntry(
                "de verpakking",
                "noun",
                "Materiaal om een product te beschermen; meervoud: verpakkingen.",
                "Neem de verpakking mee naar de apotheek.",
            ),
            VocabularyEntry(
                "slikken",
                "verb",
                "Iets door je keel naar je maag laten gaan.",
                "Ik heb moeite met slikken.",
            ),
            VocabularyEntry(
                "ademhalen",
                "verb",
                "Lucht in en uit je longen laten gaan.",
                "Ik kan moeilijk ademhalen.",
            ),
            VocabularyEntry(
                "duizelig",
                "adjective",
                "Met het gevoel dat jij of je omgeving draait.",
                "Ik voel me duizelig.",
            ),
            VocabularyEntry(
                "misselijk",
                "adjective",
                "Met het gevoel dat je misschien moet overgeven.",
                "Na de reis was ik misselijk.",
            ),
        ],
    ),
    VocabularySet(
        id="beroepen_a2",
        level="A2",
        topic="Een baan zoeken",
        unit_ref="a2-unit-6",
        words=[
            VocabularyEntry(
                "de vacature",
                "noun",
                "Een beschikbare werkplek waarvoor iemand wordt gezocht; meervoud: vacatures.",
                "Ik reageer op een vacature.",
            ),
            VocabularyEntry(
                "het salaris",
                "noun",
                "Geld dat je voor je werk ontvangt; meervoud: salarissen.",
                "Wanneer krijg ik mijn salaris?",
            ),
            VocabularyEntry(
                "het contract",
                "noun",
                "Een schriftelijke overeenkomst; meervoud: contracten.",
                "Ik lees het contract voordat ik teken.",
            ),
            VocabularyEntry(
                "de werkgever",
                "noun",
                "De persoon of organisatie voor wie iemand werkt; meervoud: werkgevers.",
                "Mijn werkgever betaalt de cursus.",
            ),
            VocabularyEntry(
                "de werknemer",
                "noun",
                "Iemand die tegen betaling bij een werkgever werkt; meervoud: werknemers.",
                "Nieuwe werknemers krijgen uitleg.",
            ),
            VocabularyEntry(
                "het gesprek",
                "noun",
                "Een uitwisseling van gesproken woorden; meervoud: gesprekken.",
                "Het gesprek over de baan is morgen.",
            ),
            VocabularyEntry(
                "het cv",
                "noun",
                "Een overzicht van je opleiding en werkervaring; meervoud: cv's.",
                "Ik stuur mijn cv mee.",
            ),
            VocabularyEntry(
                "verdienen", "verb", "Geld krijgen door te werken.", "Hoeveel verdien je per uur?"
            ),
            VocabularyEntry(
                "tijdelijk", "adjective", "Voor een beperkte periode.", "Ik zoek tijdelijk werk."
            ),
            VocabularyEntry(
                "deeltijd",
                "noun",
                "Een werkverband met minder uren dan een volledige werkweek.",
                "Ik wil in deeltijd werken.",
            ),
        ],
    ),
    VocabularySet(
        id="leren_a2",
        level="A2",
        topic="Een cursus volgen",
        unit_ref="a2-unit-6",
        words=[
            VocabularyEntry(
                "de les",
                "noun",
                "Een periode waarin iemand uitleg en oefening krijgt; meervoud: lessen.",
                "De les duurt een uur.",
            ),
            VocabularyEntry(
                "het huiswerk",
                "noun",
                "Werk voor een opleiding dat je buiten de les doet.",
                "We maken het huiswerk samen.",
            ),
            VocabularyEntry(
                "het examen",
                "noun",
                "Een toets om kennis of vaardigheden te beoordelen; meervoud: examens.",
                "Het examen is volgende maand.",
            ),
            VocabularyEntry(
                "het cijfer",
                "noun",
                "Een getal als beoordeling van schoolwerk; meervoud: cijfers.",
                "Ik heb een goed cijfer gekregen.",
            ),
            VocabularyEntry(
                "de opdracht",
                "noun",
                "Een taak die je moet uitvoeren; meervoud: opdrachten.",
                "We lezen de opdracht eerst.",
            ),
            VocabularyEntry(
                "de uitleg",
                "noun",
                "Informatie die iets begrijpelijk maakt.",
                "Bedankt voor de duidelijke uitleg.",
            ),
            VocabularyEntry(
                "de fout",
                "noun",
                "Iets wat niet juist is; meervoud: fouten.",
                "Ik leer van mijn fouten.",
            ),
            VocabularyEntry(
                "slagen",
                "verb",
                "Een examen met voldoende resultaat afronden.",
                "Ik hoop voor het examen te slagen.",
            ),
            VocabularyEntry(
                "zakken",
                "verb",
                "Bij een examen niet voldoende resultaat behalen.",
                "Zij is voor haar rijexamen gezakt.",
            ),
            VocabularyEntry(
                "onthouden",
                "verb",
                "Informatie in je geheugen bewaren.",
                "Ik schrijf het woord op om het te onthouden.",
            ),
        ],
    ),
    VocabularySet(
        id="digitaal_a2",
        level="A2",
        topic="Een digitaal probleem melden",
        unit_ref="a2-unit-7",
        words=[
            VocabularyEntry(
                "het wachtwoord",
                "noun",
                "Een geheime reeks tekens om toegang te krijgen; meervoud: wachtwoorden.",
                "Ik ben mijn wachtwoord vergeten.",
            ),
            VocabularyEntry(
                "het scherm",
                "noun",
                "Het deel van een apparaat waarop je tekst en beelden ziet; meervoud: schermen.",
                "Het scherm is zwart.",
            ),
            VocabularyEntry(
                "de verbinding",
                "noun",
                "Een aansluiting waarmee apparaten informatie uitwisselen; meervoud: verbindingen.",
                "De verbinding valt steeds weg.",
            ),
            VocabularyEntry(
                "het bestand",
                "noun",
                "Een verzameling digitale gegevens met een naam; meervoud: bestanden.",
                "Het bestand dat u stuurde opent niet.",
            ),
            VocabularyEntry(
                "de bijlage",
                "noun",
                "Een bestand dat met een bericht wordt meegestuurd; meervoud: bijlagen.",
                "De rekening staat in de bijlage.",
            ),
            VocabularyEntry(
                "inloggen",
                "verb",
                "Met je gegevens toegang krijgen tot een digitaal systeem.",
                "Ik kan niet inloggen.",
            ),
            VocabularyEntry(
                "opslaan",
                "verb",
                "Digitale informatie bewaren voor later.",
                "Sla het bestand op voordat je stopt.",
            ),
            VocabularyEntry(
                "downloaden",
                "verb",
                "Een bestand van een netwerk naar je apparaat halen.",
                "Ik heb het formulier gedownload.",
            ),
            VocabularyEntry(
                "opladen",
                "verb",
                "Een batterij van nieuwe energie voorzien.",
                "Mijn telefoon laadt niet meer op.",
            ),
            VocabularyEntry(
                "opnieuw", "adverb", "Nog een keer.", "Kunt u het bestand opnieuw sturen?"
            ),
        ],
    ),
    VocabularySet(
        id="vrijetijd_a2",
        level="A2",
        topic="Kaartjes en activiteiten regelen",
        unit_ref="a2-unit-7",
        words=[
            VocabularyEntry(
                "het optreden",
                "noun",
                "Een voorstelling van bijvoorbeeld muzikanten; meervoud: optredens.",
                "Het optreden dat we wilden zien is afgezegd.",
            ),
            VocabularyEntry(
                "de voorstelling",
                "noun",
                "Een uitvoering voor publiek; meervoud: voorstellingen.",
                "De voorstelling begint later.",
            ),
            VocabularyEntry(
                "de bioscoop",
                "noun",
                "Een gebouw waar films voor publiek worden vertoond; meervoud: bioscopen.",
                "Ik heb kaartjes voor de bioscoop gekocht.",
            ),
            VocabularyEntry(
                "de zitplaats",
                "noun",
                "Een plek om te zitten; meervoud: zitplaatsen.",
                "Onze zitplaatsen staan niet op de kaartjes.",
            ),
            VocabularyEntry(
                "de rij",
                "noun",
                "Mensen of dingen achter of naast elkaar; meervoud: rijen.",
                "We staan in de verkeerde rij.",
            ),
            VocabularyEntry(
                "de korting",
                "noun",
                "Een vermindering van de gewone prijs; meervoud: kortingen.",
                "Geldt deze korting ook op zaterdag?",
            ),
            VocabularyEntry(
                "uitverkocht",
                "adjective",
                "Niet meer te koop doordat alles is verkocht.",
                "De voorstelling is uitverkocht.",
            ),
            VocabularyEntry(
                "geldig",
                "adjective",
                "Bruikbaar volgens de regels of binnen een periode.",
                "Is dit kaartje morgen nog geldig?",
            ),
            VocabularyEntry(
                "annuleren",
                "verb",
                "Een afgesproken dienst of boeking niet laten doorgaan.",
                "Ik wil mijn reservering annuleren.",
            ),
            VocabularyEntry(
                "terugkrijgen",
                "verb",
                "Iets opnieuw ontvangen nadat je het hebt gegeven.",
                "Kan ik mijn geld terugkrijgen?",
            ),
        ],
    ),
]
