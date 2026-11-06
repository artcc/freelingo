"""Dutch B1: narration, explanation and independent interaction."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="verhaaltijden",
        title="Gebeurtenis, achtergrond en eerdere handeling",
        level="B1",
        category="Tijd",
        summary="Bouw een verhaal op met verschillende verleden tijden.",
        explanation="Het perfectum kan een afgeronde gebeurtenis introduceren; de onvoltooid verleden tijd beschrijft vaak achtergrond of een reeks gebeurtenissen. Het plusquamperfectum bestaat uit had of was met een voltooid deelwoord en plaatst iets vóór een ander verleden moment: Toen ik aankwam, was de trein al vertrokken.\n\nKies tijden vanuit het perspectief van de verteller. Er bestaat geen absolute regel dat een eenmalige gebeurtenis altijd het perfectum krijgt. Bewaar de tijdsvolgorde bij het navertellen en maak met al, nog, eerst en daarna de samenhang duidelijk.",
        rules=[
            "Gebruik had/was + deelwoord voor een eerdere verleden gebeurtenis.",
            "Houd de tijdslijn consequent.",
            "Vermijd mechanische tijdkeuze op basis van alleen gisteren.",
        ],
        examples=[
            GrammarExample("Ik heb een oude vriend ontmoet. Hij zat op een terras."),
            GrammarExample("Ze had al gegeten toen ik belde."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Toen ik aankwam, had de trein al vertrokken.",
                "Toen ik aankwam, was de trein al vertrokken.",
                "Vertrekken krijgt zijn, dus was in deze tijd.",
            )
        ],
        related=["perfectum", "verleden-tijd"],
    ),
    GrammarTopic(
        slug="indirecte-vragen",
        title="Indirect vragen met of en vraagwoorden",
        level="B1",
        category="Zinsbouw",
        summary="Vraag om informatie in een ingebedde vraag.",
        explanation="Een indirecte ja-neevraag begint met of: Ik weet niet of de winkel open is. Bij een vraagwoord blijft dat woord staan: Kunt u zeggen waar het station is? De ingebedde vraag krijgt bijzinvolgorde. Het vraagteken hangt af van de hele zin: Ik vraag me af waar hij woont. tegenover Weet jij waar hij woont?\n\nOf kan ook een keuze verbinden: koffie of thee. Dat is een andere functie. Gebruik geen directe vraagvolgorde binnen een indirecte vraag.",
        rules=[
            "Ja/nee → of; waar/wanneer/hoe blijven staan.",
            "Zet het werkwoord achteraan in de ingebedde vraag.",
            "Bepaal de interpunctie vanuit de volledige zin.",
        ],
        examples=[
            GrammarExample("Weet u wanneer de bus vertrekt?"),
            GrammarExample("Ik vraag me af of hij tijd heeft."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Weet je waar woont hij?",
                "Weet je waar hij woont?",
                "De ingebedde vraag heeft bijzinvolgorde.",
            )
        ],
        related=["omdat-dat", "vragen-inversie"],
    ),
    GrammarTopic(
        slug="er-voorzetsel",
        title="Erop, eraan en ermee",
        level="B1",
        category="Voornaamwoorden",
        summary="Verwijs naar zaken met een voorzetsel en er.",
        explanation="Bij verwijzing naar een zaak kan er een voornaamwoord met voorzetsel vervangen: Ik wacht op het antwoord → Ik wacht erop. De delen kunnen gescheiden staan: Ik wacht er al lang op. Met wordt mee: Ik werk ermee.\n\nBij personen is een voorzetsel met een persoonlijk voornaamwoord vaak duidelijker: Ik wacht op haar. Gebruik waar + voorzetsel voor vragen over zaken: Waar denk je aan? Vaste voorzetsels horen bij de betekenis van het werkwoord: denken aan, wachten op, praten over. Maak geen woordelijke vertaling vanuit een andere taal.",
        rules=[
            "Op het antwoord → erop; met het apparaat → ermee.",
            "Splitsing is mogelijk: er lang op wachten.",
            "Behoud het juiste vaste voorzetsel.",
        ],
        examples=[
            GrammarExample("Ik ben ermee begonnen."),
            GrammarExample("Daar denk ik vaak aan."),
            GrammarExample("Waar gaat het over?"),
        ],
        common_mistakes=[
            GrammarMistake("Ik werk ermet.", "Ik werk ermee.", "Met krijgt mee in deze combinatie.")
        ],
        related=["er-plaats", "betrekkelijk-voorzetsel"],
    ),
    GrammarTopic(
        slug="betrekkelijk-voorzetsel",
        title="Met wie, waarmee en wat",
        level="B1",
        category="Zinsbouw",
        summary="Verbind informatie met een duidelijk verwijswoord.",
        explanation="Bij een persoon met voorzetsel gebruik je vaak met wie, aan wie of over wie: de collega met wie ik samenwerk. Bij een zaak gebruik je waarmee, waaraan of waarover: het programma waarmee ik werk. Een gesplitste vorm is ook mogelijk: het programma waar ik mee werk.\n\nWat kan verwijzen naar een hele voorafgaande zin: De trein viel uit, wat vervelend was. Na alles, niets en iets is wat gebruikelijk; in verschillende constructies kan dat ook voorkomen. Vermijd een toets waarin zulke geldige alternatieven zonder context fout worden gerekend.",
        rules=[
            "Gebruik met wie bij een persoon en waarmee bij een zaak als helder leermodel.",
            "Waarmee en waar ... mee kunnen beide correct zijn.",
            "Maak duidelijk of wat naar een naamwoord of een hele mededeling verwijst.",
        ],
        examples=[
            GrammarExample("Dit is de collega met wie ik reis."),
            GrammarExample("De bus kwam te laat, wat iedereen vervelend vond."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Het apparaat met wie ik werk is kapot.",
                "Het apparaat waarmee ik werk is kapot.",
                "Een apparaat is een zaak; gebruik hier waarmee in plaats van met wie.",
            )
        ],
        related=["betrekkelijk-die-dat", "er-voorzetsel"],
    ),
    GrammarTopic(
        slug="passief-basis",
        title="Worden en zijn in de lijdende vorm",
        level="B1",
        category="Werkwoorden",
        summary="Leg de nadruk op wat er gebeurt of is gebeurd.",
        explanation="In de lijdende vorm wordt het lijdend voorwerp van de actieve zin onderwerp: De monteur repareert de fiets → De fiets wordt gerepareerd. De handelende persoon kan met door worden toegevoegd als die relevant is.\n\nEen passief perfectum gebruikt zijn: De fiets is gerepareerd. In het Nederlands voeg je daarbij normaal geen geworden toe. De zin met is kan ook de resulterende toestand benadrukken. Gebruik de passieve vorm als handeling of resultaat belangrijker is dan de uitvoerder; kies actief als verantwoordelijkheid duidelijk moet blijven.",
        rules=[
            "Wordt/worden + deelwoord voor een passieve tegenwoordige tijd.",
            "Is/zijn + deelwoord voor een passief perfectum.",
            "Laat de uitvoerder alleen weg als dat de betekenis niet misleidend verandert.",
        ],
        examples=[
            GrammarExample("De brug wordt morgen geopend."),
            GrammarExample("De brief is gisteren verstuurd."),
        ],
        common_mistakes=[
            GrammarMistake(
                "De brieven wordt verstuurd.",
                "De brieven worden verstuurd.",
                "Het werkwoord volgt het meervoudige onderwerp.",
            )
        ],
        related=["perfectum", "voltooid-deelwoord"],
    ),
    GrammarTopic(
        slug="voorwaarden-zou",
        title="Voorwaarden, wensen en advies met zou",
        level="B1",
        category="Modaliteit",
        summary="Bespreek een denkbeeldige situatie en geef voorzichtig advies.",
        explanation="Een open voorwaarde kan de tegenwoordige tijd gebruiken: Als ik tijd heb, kom ik. Voor een denkbeeldige situatie gebruik je vaak een verleden vorm en zou: Als ik meer tijd had, zou ik vaker lezen. Een verleden vorm betekent hier niet noodzakelijk een verleden tijdstip.\n\nZou kan ook een beleefd verzoek of advies geven: Zou u dat kunnen toelichten? Ik zou eerst bellen. Beschrijf niet iedere zin met zou als onzekerheid: de functie volgt uit context. Zowel als ik kon als als ik zou kunnen kan in passende context correct zijn.",
        rules=[
            "Maak onderscheid tussen open en denkbeeldige voorwaarden.",
            "Zou + infinitief krijgt geen te.",
            "Stem advies af op wat de gesprekspartner nodig heeft.",
        ],
        examples=[
            GrammarExample("Als ik dichterbij woonde, zou ik fietsen."),
            GrammarExample("Ik zou de huisarts bellen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Als ik tijd had, ik zou komen.",
                "Als ik tijd had, zou ik komen.",
                "Na de vooropgeplaatste bijzin volgt inversie.",
            )
        ],
        related=["als-wanneer", "toekomst-plannen"],
    ),
    GrammarTopic(
        slug="verbindingswoorden",
        title="Toch, daarom, hoewel en dus",
        level="B1",
        category="Verbindingen",
        summary="Maak oorzaak, gevolg en tegenstelling herkenbaar.",
        explanation="Daarom en toch kunnen het eerste zinsdeel zijn en krijgen dan inversie: Het regent. Daarom blijf ik thuis. Hoewel leidt een bijzin in: Hoewel het regent, ga ik fietsen. Maar en want verbinden hoofdzinnen zonder zelf de eerste zinsdeelplaats te vullen.\n\nDus kan verschillende zinsfuncties hebben: Het regent, dus ik blijf thuis; Het regent; dus blijf ik thuis. Beide patronen komen voor. Leer verbindingswoorden met een volledige voorbeeldzin en kies ze op basis van betekenis, niet alleen grammaticale vorm.",
        rules=[
            "Daarom geeft gevolg of reden voor een keuze.",
            "Hoewel geeft een niet-doorslaggevende tegenwerping.",
            "Bepaal of de verbinding een bijzin of hoofdzin inleidt.",
        ],
        examples=[
            GrammarExample("Ik was moe. Toch ging ik mee."),
            GrammarExample("Hoewel het duur is, koop ik het."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Daarom ik blijf thuis.",
                "Daarom blijf ik thuis.",
                "Daarom vult hier de eerste zinsdeelplaats.",
            )
        ],
        related=["omdat-dat", "en-maar-want"],
    ),
    GrammarTopic(
        slug="duur-en-voortgang",
        title="Al, sinds en aan het",
        level="B1",
        category="Tijd",
        summary="Vertel hoelang iets duurt en wat op dit moment bezig is.",
        explanation="Voor een situatie die in het verleden begon en nog duurt, is de tegenwoordige tijd natuurlijk: Ik woon hier al drie jaar; Ik werk hier sinds mei. Sinds geeft een beginpunt; al drie jaar geeft een duur. Geleden plaatst een gebeurtenis vóór nu: Ik verhuisde drie jaar geleden.\n\nZijn + aan het + infinitief benadrukt een lopende activiteit: Ik ben aan het koken. Ook zitten/staan/liggen te + infinitief kan een activiteit beschrijven: Ze zit te lezen. De gewone tegenwoordige tijd kan dezelfde huidige activiteit uitdrukken; de progressieve vorm is niet altijd verplicht.",
        rules=[
            "Sinds + beginpunt; al + duur; geleden + tijd vóór nu.",
            "Aan het krijgt een infinitief.",
            "Gebruik een progressieve vorm als het bezig-zijn relevant is.",
        ],
        examples=[
            GrammarExample("We wonen hier sinds september."),
            GrammarExample("Ik ben aan het koken."),
            GrammarExample("Hij zit een boek te lezen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik ben aan het gekookt.",
                "Ik ben aan het koken.",
                "Aan het krijgt hier geen voltooid deelwoord.",
            )
        ],
        related=["tegenwoordige-tijd", "te-infinitief"],
    ),
    GrammarTopic(
        slug="onbepaalde-woorden",
        title="Iedereen, niemand, iets en niets",
        level="B1",
        category="Voornaamwoorden",
        summary="Geef hoeveelheden en onbekende personen of zaken aan.",
        explanation="Iedereen, iemand en niemand krijgen een enkelvoudige persoonsvorm: Iedereen is welkom. Alle deelnemers krijgt meervoud: Alle deelnemers zijn welkom. Elk en ieder staan bij een enkelvoudig het-woord; elke en iedere bij een de-woord: elk huis, iedere straat.\n\nNa iets, niets, veel en weinig krijgt een bijvoeglijk naamwoord vaak -s: iets leuks, niets nieuws. Vergelijk veel mooie boeken: daar hoort mooie bij boeken en gebruik je geen -s. Vermijd een dubbele ontkenning als neutraal geschreven model: Ik zie niemand, niet Ik zie niemand niet.",
        rules=[
            "Iedereen is; alle mensen zijn.",
            "Iets nieuws, maar nieuwe dingen.",
            "Elk boek; iedere fiets.",
        ],
        examples=[
            GrammarExample("Iedereen heeft iets lekkers meegenomen."),
            GrammarExample("Ik heb niets bijzonders gezien."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Iedereen zijn welkom.",
                "Iedereen is welkom.",
                "Iedereen is grammaticaal enkelvoud.",
            )
        ],
        related=["niet-geen", "bijvoeglijke-naamwoorden"],
    ),
    GrammarTopic(
        slug="indirecte-rede",
        title="Navertellen wat iemand zegt",
        level="B1",
        category="Tekst",
        summary="Geef uitspraken weer zonder persoon, tijd of zekerheid te veranderen.",
        explanation="Bij indirecte rede pas je verwijzingen aan het vertelperspectief aan. Noor zegt: 'Ik kom morgen.' Later kun je zeggen: Noor zei dat ze de volgende dag zou komen. Als morgen op het moment van navertellen nog dezelfde dag aanduidt, kan morgen blijven staan.\n\nHet Nederlands verplicht niet altijd tot terugschuiven van de werkwoordstijd: Zij zei dat ze in Utrecht woont kan aangeven dat dit nog geldt. Behoud modaliteit: misschien komen mag niet veranderen in zeker komen. Maak duidelijk of je citeert, samenvat of een eigen conclusie geeft.",
        rules=[
            "Pas ik/jij/hier/morgen aan als het perspectief verandert.",
            "Behoud mogelijkheid, verplichting en twijfel.",
            "Gebruik een tijd die bij het bedoelde moment past.",
        ],
        examples=[
            GrammarExample("Hij zegt dat hij geen tijd heeft."),
            GrammarExample("Ze vroeg of ik haar kon helpen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Hij zegt dat heeft hij tijd.",
                "Hij zegt dat hij tijd heeft.",
                "Na dat volgt bijzinvolgorde.",
            )
        ],
        related=["indirecte-vragen", "verhaaltijden"],
    ),
    GrammarTopic(
        slug="er-bijzin",
        title="Ervoor zorgen dat en erop rekenen dat",
        level="B1",
        category="Zinsbouw",
        summary="Verbind een werkwoord met een voorzetsel aan een inhoudelijke bijzin.",
        explanation="Sommige werkwoorden behouden hun voorzetsel als de aanvulling een hele zin is: rekenen op iets wordt erop rekenen dat iets gebeurt. Zorgen voor iets wordt ervoor zorgen dat iets gebeurt. Er met het voorzetsel kondigt hier de inhoud van de dat-bijzin aan.\n\nLeer zulke verbindingen per werkwoord. Ik hoop dat het lukt heeft geen erop nodig; Ik reken erop dat je komt wel in het hier gebruikte patroon. Schrijf aaneen als er en het voorzetsel naast elkaar staan: erop. Bij scheiding: Ik reken er echt op dat je komt. De bijzin houdt zijn eigen werkwoordvolgorde.",
        rules=[
            "Rekenen op → erop rekenen dat.",
            "Zorgen voor → ervoor zorgen dat.",
            "Een ander werkwoord kan een ander patroon vereisen.",
        ],
        examples=[
            GrammarExample("Ik reken erop dat je mij op tijd informeert."),
            GrammarExample("We zorgen ervoor dat iedereen het bericht ontvangt."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik reken erop dat kom je morgen.",
                "Ik reken erop dat je morgen komt.",
                "Na dat gebruikt de inhoudelijke bijzin bijzinvolgorde.",
            )
        ],
        related=["omdat-dat", "er-voorzetsel"],
    ),
    GrammarTopic(
        slug="infinitief-of-dat",
        title="Proberen te en hopen dat",
        level="B1",
        category="Zinsbouw",
        summary="Kies een aanvulling die duidelijk maakt wie de handeling uitvoert.",
        explanation="Na proberen kan een infinitief met te staan: Ik probeer op tijd te komen. De persoon die probeert is hier ook degene die komt. Een dat-bijzin kan een eigen onderwerp noemen: Ik hoop dat mijn broer op tijd komt. Ook bij hetzelfde onderwerp kan een dat-bijzin mogelijk zijn, afhankelijk van het werkwoord.\n\nJe kunt deze patronen niet vrij voor ieder werkwoord verwisselen. Ik wil vertrekken en Ik wil dat zij vertrekt verschillen in uitvoerder. Ik besluit te vertrekken legt de beslissing bij ik. Controleer bij inkorten of je dezelfde personen en dezelfde bedoeling behoudt.",
        rules=[
            "Bepaal het onderwerp van iedere handeling.",
            "Willen krijgt zonder dat een infinitief zonder te.",
            "Leer welke aanvulling bij het werkwoord en de betekenis past.",
        ],
        examples=[
            GrammarExample("Ik probeer het formulier vandaag in te vullen."),
            GrammarExample("Ik wil dat mijn collega de gegevens controleert."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik wil dat mijn collega de gegevens controleren.",
                "Ik wil dat mijn collega de gegevens controleert.",
                "De dat-bijzin heeft hier een eigen persoonsvorm bij mijn collega.",
            )
        ],
        related=["te-infinitief", "omdat-dat"],
    ),
    GrammarTopic(
        slug="vaste-voorzetsels",
        title="Wachten op, deelnemen aan en tevreden met",
        level="B1",
        category="Voorzetsels",
        summary="Leer voorzetsels als onderdeel van een betekenisvolle combinatie.",
        explanation="Bij veel werkwoorden en bijvoeglijke naamwoorden hoort een vaste combinatie: wachten op, deelnemen aan, belangstelling hebben voor, tevreden zijn met. De keuze is niet altijd uit een ruimtelijke betekenis af te leiden. Leer daarom een volledige zin en niet alleen een los voorzetsel.\n\nEen ander voorzetsel kan een andere relatie aangeven: denken aan iemand tegenover denken over een voorstel. Bij verwijzing naar zaken kan er het naamwoord vervangen: Ik wacht op het antwoord; Ik wacht erop. Bij personen is op hem of op haar vaak duidelijker. Kies eerst de betekenis en bepaal daarna de juiste verwijzing.",
        rules=[
            "Deelnemen aan een activiteit; wachten op een antwoord.",
            "Tevreden met een resultaat; geïnteresseerd in een onderwerp.",
            "Behoud het vaste voorzetsel in een er-verbinding.",
        ],
        examples=[
            GrammarExample("Ik ben geïnteresseerd in de cursus en neem eraan deel."),
            GrammarExample("We wachten op haar reactie."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik neem op de cursus deel.",
                "Ik neem aan de cursus deel.",
                "Deelnemen krijgt hier aan.",
            )
        ],
        related=["er-voorzetsel", "betrekkelijk-voorzetsel"],
    ),
    GrammarTopic(
        slug="laten-infinitief",
        title="Laten repareren en laten weten",
        level="B1",
        category="Werkwoorden",
        summary="Beschrijf een handeling die je door iemand anders laat uitvoeren.",
        explanation="Laten met een infinitief kan aangeven dat je een ander iets laat doen: Ik laat mijn fiets repareren. Je organiseert de reparatie, maar voert haar niet noodzakelijk zelf uit. De infinitief krijgt in dit patroon geen te. Met een genoemde persoon: Ik laat de monteur naar de fiets kijken.\n\nLaten kan ook toestemming geven: We laten de kinderen buiten spelen. In vaste combinaties krijgt het een praktische betekenis: Laat het me weten vraagt om informatie. De context bepaalt of het om een opdracht, gelegenheid of toestemming gaat. Beschrijf dus niet iedere zin met laten als dwang.",
        rules=[
            "Laten + infinitief zonder te.",
            "De persoon die laat uitvoeren is niet automatisch de uitvoerder.",
            "Laat het me weten is een verzoek om informatie.",
        ],
        examples=[
            GrammarExample("Ik laat mijn jas bij de kleermaker inkorten."),
            GrammarExample("Laat me weten wanneer je de documenten ontvangt."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik laat mijn fiets te repareren.",
                "Ik laat mijn fiets repareren.",
                "Na laten staat in dit patroon geen te.",
            )
        ],
        related=["modale-werkwoorden", "passief-basis"],
    ),
    GrammarTopic(
        slug="lidwoord-gebruik",
        title="Een beroep, een algemeen begrip en een bekende zaak",
        level="B1",
        category="Naamwoorden",
        summary="Gebruik lidwoorden op basis van betekenis en bekendheid.",
        explanation="Bij een beroep na zijn staat vaak geen lidwoord: Zij is arts. Met een beschrijving kan wel een lidwoord staan: Zij is een ervaren arts. Voor een algemeen niet-telbaar begrip ontbreekt vaak een: Water is belangrijk; Ik zoek informatie. Voor een specifieke bekende hoeveelheid kan de of het verschijnen: De informatie in de brief is duidelijk.\n\nHet verschil zit niet alleen in enkelvoud of meervoud, maar ook in wat voor de lezer identificeerbaar is. Vergelijk Ik zoek een huisarts met Ik bel de huisarts. Presenteer een contextueel passende keuze niet als fout doordat slechts één standaardvoorbeeld wordt gebruikt.",
        rules=[
            "Zij is arts; zij is een ervaren arts.",
            "Informatie en advies zijn vaak niet-telbaar gebruikt.",
            "Een bekende, specifieke zaak kan de of het krijgen.",
        ],
        examples=[
            GrammarExample("Ik zoek informatie over een verzekering."),
            GrammarExample("De informatie op dit formulier is verouderd."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik heb een informatie nodig.",
                "Ik heb informatie nodig.",
                "Informatie is hier niet-telbaar; voor één element kan een stukje informatie.",
            )
        ],
        related=["lidwoorden-meervoud", "onbepaalde-woorden"],
    ),
    GrammarTopic(
        slug="hoeven-modale-nuance",
        title="Niet hoeven, niet mogen en beter kunnen",
        level="B1",
        category="Modaliteit",
        summary="Onderscheid advies, verbod, verplichting en afwezigheid van noodzaak.",
        explanation="Je hoeft niet te komen betekent dat komen niet noodzakelijk is; Je mag niet komen sluit toestemming uit. Je moet komen drukt noodzaak of een verplichting uit. Je kunt beter eerst bellen geeft advies en is dus minder dwingend. Een kleine verandering kan de praktische boodschap omkeren.\n\nOok beperking kan hoeven mogelijk maken: Je hoeft alleen je naam te noemen. Bij ontkenning met moeten kan de bedoeling van de situatie afhangen; kies een expliciet model zoals Je mag niet parkeren wanneer een verbod bedoeld is. Behoud bij doorgeven van regels precies hoeveel keuze iemand heeft.",
        rules=[
            "Niet hoeven is geen verbod.",
            "Niet mogen betekent geen toestemming.",
            "Kunt beter geeft advies, geen gegarandeerd resultaat.",
        ],
        examples=[
            GrammarExample("Je hoeft niet te wachten; je mag het formulier online versturen."),
            GrammarExample("Je kunt beter eerst vragen welke documenten nodig zijn."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Je hoeft morgen niet werken.",
                "Je hoeft morgen niet te werken.",
                "In dit basispatroon krijgt hoeven een infinitief met te.",
            )
        ],
        related=["te-infinitief", "voorwaarden-zou"],
    ),
    GrammarTopic(
        slug="adjectief-stof",
        title="Een houten tafel en een plastic tas",
        level="B1",
        category="Bijvoeglijke naamwoorden",
        summary="Beschrijf materialen en onderscheid ze van gewone eigenschappen.",
        explanation="Veel stofadjectieven eindigen op -en: hout wordt houten, wol wordt wollen, goud wordt gouden. Die vorm blijft meestal gelijk: een houten tafel, het houten huis, houten stoelen. Voeg niet nog een gewone adjectiefuitgang toe. Bij sommige materialen blijft de vorm ongewijzigd, zoals plastic en aluminium.\n\nEen omschrijving met van is vaak ook mogelijk: een tafel van hout. Maak onderscheid tussen materiaal en figuurlijke betekenis: een gouden ring kan van goud zijn; een gouden kans is een bijzonder goede gelegenheid. Het betekenisverschil is geen reden om de materiaalregel op elke figuurlijke combinatie toe te passen.",
        rules=[
            "Houten blijft houten bij de-woorden, het-woorden en meervoud.",
            "Plastic en aluminium kunnen onveranderd vóór een naamwoord staan.",
            "Controleer of het om letterlijk materiaal gaat.",
        ],
        examples=[
            GrammarExample("Ik kies een wollen trui in plaats van een synthetische."),
            GrammarExample("De houten stoelen zijn duurder dan de plastic stoelen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "een houtene tafel",
                "een houten tafel",
                "Het stofadjectief houten krijgt geen extra -e.",
            )
        ],
        related=["bijvoeglijke-naamwoorden", "vergelijken"],
    ),
    GrammarTopic(
        slug="tijd-en-voorwaarde",
        title="Voordat, nadat, zodra en zolang",
        level="B1",
        category="Verbindingen",
        summary="Maak tijdsrelaties en voorwaarden in langere berichten duidelijk.",
        explanation="Voordat plaatst een gebeurtenis eerder dan een andere: Bel voordat je vertrekt. Nadat plaatst de inhoud van de bijzin eerder: Nadat ik had gegeten, ging ik naar buiten. Zodra benadrukt het beginmoment; zolang geeft aan dat twee situaties gedurende een periode samen gelden.\n\nDeze woorden leiden bijzinnen in en krijgen dus bijzinvolgorde. De werkwoordstijden volgen de tijdslijn, niet alleen het voegwoord. In een praktische afspraak kan zodra ook een noodzakelijke stap aangeven: Zodra de betaling binnen is, versturen we het pakket. Maak de gewenste volgorde expliciet bij het samenvatten.",
        rules=[
            "Voordat en nadat geven tegengestelde tijdsrelaties.",
            "Zodra benadrukt het moment waarop iets begint of geldt.",
            "Een vooropgeplaatste bijzin geeft inversie in de hoofdzin.",
        ],
        examples=[
            GrammarExample(
                "Nadat de gemeente de aanvraag had ontvangen, stuurde zij een bevestiging."
            ),
            GrammarExample("Zolang de weg dicht is, nemen we de omleiding."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Zodra de weg open is, we nemen de bus.",
                "Zodra de weg open is, nemen we de bus.",
                "Na de vooropgeplaatste bijzin volgt de persoonsvorm.",
            )
        ],
        related=["verhaaltijden", "als-wanneer", "tijdvolgorde"],
    ),
    GrammarTopic(
        slug="woordvorming-samenstellingen",
        title="Werkdag, taalcursus en fietsroute",
        level="B1",
        category="Woordvorming",
        summary="Herken de betekenis en spelling van samengestelde naamwoorden.",
        explanation="Een samenstelling vormt één woord uit twee of meer delen: werk + dag wordt werkdag; taal + cursus wordt taalcursus. Het laatste deel bepaalt meestal de hoofdsoort, het lidwoord en het meervoud: de route, de fietsroute, de fietsroutes. Het eerste deel maakt de betekenis specifieker.\n\nSchrijf gewone Nederlandse samenstellingen aaneen. Een koppelteken is in bepaalde gevallen nodig, bijvoorbeeld bij klinkerbotsing: auto-ongeluk. Tussenletters zoals -s- en -en- hebben eigen spellingregels; raadpleeg bij twijfel een woordenlijst. Niet iedere woordgroep is een samenstelling: een nieuwe cursus blijft los.",
        rules=[
            "Het laatste deel is meestal de betekenis- en grammaticakern.",
            "Een taalcursus is één woord; een nieuwe cursus is een woordgroep.",
            "Controleer tussenletters en koppeltekens bij twijfel.",
        ],
        examples=[
            GrammarExample("Mijn werkdag begint met een teamoverleg."),
            GrammarExample("Deze fietsroute loopt langs drie basisscholen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik volg een taal cursus.",
                "Ik volg een taalcursus.",
                "Taalcursus is hier één samengesteld naamwoord.",
            )
        ],
        related=["lidwoorden-meervoud", "klanken-spelling"],
    ),
]
