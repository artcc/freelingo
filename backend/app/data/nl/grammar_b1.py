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
]
