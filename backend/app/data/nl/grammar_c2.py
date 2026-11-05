"""Dutch C2: interpretation, rhetoric and meaning-preserving revision."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="implicatuur-presuppositie",
        title="Wat wordt gezegd en wat wordt gesuggereerd?",
        level="C2",
        category="Pragmatiek",
        summary="Onderscheid expliciete inhoud, vooronderstelling en implicatuur.",
        explanation="Sommige formuleringen presenteren informatie als al bekend: Is de directeur weer te laat? suggereert eerdere gevallen. Een gesprekspartner kan die vooronderstelling betwisten. Een implicatuur ontstaat uit context: Sommige deelnemers stemden voor suggereert vaak niet allemaal, maar die beperking is niet noodzakelijk deel van de letterlijke betekenis.\n\nTest of een suggestie kan worden ingetrokken: Sommige deelnemers stemden voor, misschien zelfs allemaal. Geef bij analyse aan wat expliciet volgt, wat wordt verondersteld en wat slechts aannemelijk is. Maak van een pragmatische verwachting geen logische zekerheid.",
        rules=[
            "Scheid letterlijke inhoud van contextuele gevolgtrekking.",
            "Vooronderstellingen kunnen worden betwist.",
            "Controleer of een implicatuur zonder tegenspraak kan worden ingetrokken.",
        ],
        examples=[
            GrammarExample("Is zij alweer vertrokken?"),
            GrammarExample("Sommige, misschien zelfs alle, deelnemers waren tevreden."),
        ],
        common_mistakes=[],
        related=["bereik-ontkenning", "modaliteit-bron"],
    ),
    GrammarTopic(
        slug="ironie-onderstatement",
        title="Ironie, understatement en context",
        level="C2",
        category="Pragmatiek",
        summary="Onderbouw een niet-letterlijke interpretatie met tekstuele aanwijzingen.",
        explanation="Ironie kan een spanning oproepen tussen de letterlijke uitspraak en de bedoelde beoordeling. Na de derde storing kan Dat gaat lekker! kritiek uitdrukken, maar zonder context kan dezelfde zin oprecht positief zijn. Een understatement zwakt iets bewust af: Dat was niet ideaal kan een ernstige mislukking beschrijven.\n\nNiet iedere negatieve formulering is ironisch en niet iedere overdrijving is onwaar bedoeld. Benoem relevante aanwijzingen: situatie, contrast, toon en reactie. Vermijd dat een interpretatie die slechts mogelijk is als enige onbetwistbare lezing wordt gepresenteerd.",
        rules=[
            "Baseer interpretatie op concrete aanwijzingen.",
            "Onderscheid ironie van letterlijk commentaar.",
            "Behoud ruimte voor meerdere lezingen als de tekst die toelaat.",
        ],
        examples=[
            GrammarExample("Na drie uur vertraging zei ze: 'Wat een perfecte planning.'"),
            GrammarExample(
                "Na de mislukte lancering noemde hij het resultaat 'niet helemaal ideaal'."
            ),
        ],
        common_mistakes=[],
        related=["partikels-interactie", "implicatuur-presuppositie"],
    ),
    GrammarTopic(
        slug="retorische-focus",
        title="Retorische vragen, contrast en herhaling",
        level="C2",
        category="Stijl",
        summary="Analyseer hoe zinsbouw een publiek stuurt.",
        explanation="Een retorische vraag vraagt vaak geen letterlijk antwoord, maar presenteert een standpunt als vanzelfsprekend: Wie wil er nu onveilig drinkwater? Dat kan een debat sturen zonder het voorgestelde beleid te onderbouwen. Contrast en herhaling kunnen argumenten ordenen of emotioneel versterken.\n\nEen gespleten zin legt focus: Het is de uitvoering die tekortschiet. Dat sluit niet automatisch andere problemen uit; de context bepaalt hoe exclusief de nadruk is. Beoordeel retorisch effect afzonderlijk van feitelijke geldigheid en herschrijf zo nodig in een neutralere vorm.",
        rules=[
            "Een retorische vraag is geen bewijs.",
            "Controleer of focus exclusiviteit suggereert of werkelijk uitdrukt.",
            "Gebruik herhaling doelgericht, niet als vervanging van argumentatie.",
        ],
        examples=[
            GrammarExample("Het is niet de ambitie, maar de uitvoering die tekortschiet."),
            GrammarExample("Wie kan daar nu tegen zijn?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Het zijn de uitvoering die tekortschiet.",
                "Het is de uitvoering die tekortschiet.",
                "De enkelvoudige focus vraagt hier is.",
            )
        ],
        related=["focus-woordvolgorde", "argumentatieve-samenhang"],
    ),
    GrammarTopic(
        slug="perspectief-vrije-indirecte-rede",
        title="Vertelstem en vrije indirecte rede",
        level="C2",
        category="Tekstinterpretatie",
        summary="Onderscheid de stem van een verteller van die van een personage.",
        explanation="Vrije indirecte rede kan gedachten van een personage laten doorklinken zonder 'dacht zij' of aanhalingstekens: Noor keek naar de lege straat. Waar bleef hij toch? De vraag kan vanuit Noors perspectief worden gelezen, terwijl de vertelling in de derde persoon blijft.\n\nTijd, deiktische woorden en emotionele woordkeuze helpen het perspectief bepalen. Een los fragment kan dubbelzinnig blijven. Onderscheid wat de verteller als feit presenteert van wat een personage vermoedt. Schrijf bij een analyse niet automatisch alle waardeoordelen aan de auteur toe.",
        rules=[
            "Zoek perspectiefsignalen in de omliggende tekst.",
            "Scheid auteur, verteller en personage.",
            "Behoud twijfel en subjectiviteit bij samenvatten.",
        ],
        examples=[
            GrammarExample("Ze las de brief opnieuw. Was dit werkelijk alles?"),
            GrammarExample("Hij keek op de klok. Morgen zou alles anders zijn, toch?"),
        ],
        common_mistakes=[],
        related=["indirecte-rede", "modaliteit-bron"],
    ),
    GrammarTopic(
        slug="ambiguiteit-herformuleren",
        title="Dubbelzinnigheid herkennen en gericht oplossen",
        level="C2",
        category="Betekenis",
        summary="Herschrijf alleen de bedoelde lezing expliciet.",
        explanation="De zin Ik zag de man met de verrekijker kan gaan over het instrument waarmee ik keek of over een man die een verrekijker had. Een herschrijving kiest een lezing: Met de verrekijker zag ik de man; Ik zag de man die een verrekijker bij zich had. Zonder context kun je niet weten welke lezing bedoeld was.\n\nAndere bronnen van dubbelzinnigheid zijn voornaamwoorden, ontkenning, nevenschikking en tijdsaanduidingen. Vraag om verduidelijking als de keuze inhoudelijke gevolgen heeft. Maak een tekst niet preciezer door ontbrekende feiten te verzinnen.",
        rules=[
            "Benoem eerst de mogelijke lezingen.",
            "Kies alleen een lezing die door context of opdracht wordt gesteund.",
            "Controleer deelnemers, instrument, tijd en bereik.",
        ],
        examples=[
            GrammarExample("Met een verrekijker zag ik de man op de dijk."),
            GrammarExample("Ik zag de man die een verrekijker droeg."),
        ],
        common_mistakes=[],
        related=["samengestelde-zinnen", "bereik-ontkenning"],
    ),
    GrammarTopic(
        slug="formele-vaste-vormen",
        title="Formele vaste vormen herkennen",
        level="C2",
        category="Register",
        summary="Begrijp vaste formele uitdrukkingen zonder ze onnodig te produceren.",
        explanation="In juridische, bestuurlijke of plechtige teksten komen vaste vormen voor zoals onverminderd, behoudens, zij het en hoe het ook zij. Zij het introduceert meestal een beperking of concessie: Het plan is uitvoerbaar, zij het tegen hoge kosten. Behoudens betekent doorgaans met uitzondering van of onder voorbehoud van, afhankelijk van de combinatie.\n\nZulke vormen zijn vooral receptief belangrijk. Gebruik een heldere moderne omschrijving als die dezelfde betekenis bewaart. Neem bij juridische formuleringen niet aan dat een alledaagse parafrase alle rechtsgevolgen weergeeft; beperk je tot de taalbetekenis en de gegeven context.",
        rules=[
            "Leer vaste uitdrukkingen als geheel.",
            "Zij het voegt een beperking toe en trekt niet de hele uitspraak in.",
            "Pas register aan genre en publiek aan.",
        ],
        examples=[
            GrammarExample("Het voorstel is aanvaardbaar, zij het onder voorwaarden."),
            GrammarExample("Hoe het ook zij, een besluit is nodig."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Het voorstel is haalbaar, zei het tegen hoge kosten.",
                "Het voorstel is haalbaar, zij het tegen hoge kosten.",
                "De vaste concessieve uitdrukking is zij het, niet de verleden vorm zei.",
            )
        ],
        related=["formeel-informeel", "concessie-voorwaarden"],
    ),
    GrammarTopic(
        slug="variatie-norm",
        title="Standaardtaal, regio en stijlkeuze",
        level="C2",
        category="Taalvariatie",
        summary="Beoordeel varianten op bruikbaarheid in hun context.",
        explanation="Het Nederlands kent standaardvariatie in Nederland, België en Suriname, naast regionale en sociale variatie. Een woord dat in Nederland minder gebruikelijk is, is niet daarom overal fout. Deze cursus kiest Nederlands uit Nederland als productiemodel, maar bespreekt andere vormen met hun context.\n\nMaak onderscheid tussen een grammaticale fout, een regionale standaardvariant, een informele vorm en een huisstijlvoorkeur. U hebt en u heeft zijn beide standaardtaal. Een organisatie mag één vorm kiezen voor consistentie, maar dat maakt de andere niet ongrammaticaal. Onderbouw normoordelen met betrouwbare taalbronnen.",
        rules=[
            "Geef aan voor welke regio en welk register een oordeel geldt.",
            "Onderscheid huisstijl van grammaticale correctheid.",
            "Behoud betekenis en sociale context bij redactie.",
        ],
        examples=[
            GrammarExample("U hebt bericht ontvangen."),
            GrammarExample("U heeft bericht ontvangen."),
        ],
        common_mistakes=[],
        related=["hen-hun-register", "formeel-informeel", "hebben"],
    ),
    GrammarTopic(
        slug="synthese-betekenisbehoud",
        title="Meerdere bronnen samenbrengen",
        level="C2",
        category="Tekst",
        summary="Schrijf een precieze synthese met zichtbare verschillen tussen bronnen.",
        explanation="Een synthese ordent bronnen rond een vraag en maakt overeenstemming, verschil en onzekerheid zichtbaar. Twee bronnen die hetzelfde persbericht overnemen vormen niet automatisch twee onafhankelijke bevestigingen. De ene bron kan een samenhang melden, terwijl de andere een mogelijke verklaring bespreekt.\n\nBehoud in de samenvatting kwantoren, voorwaarden, tijdsbereik en toeschrijving. 'In deze steekproef nam de score toe' mag niet veranderen in 'De aanpak werkt voor iedereen'. Benoem ontbrekende informatie en formuleer een conclusie die niet sterker is dan de gezamenlijke onderbouwing.",
        rules=[
            "Bewaar bronstatus, voorwaarden en reikwijdte.",
            "Scheid overeenstemming van onafhankelijke bevestiging.",
            "Laat onzekerheid zichtbaar in de eindconclusie.",
        ],
        examples=[
            GrammarExample(
                "Beide teksten melden een stijging, maar alleen de eerste noemt de omvang van de steekproef."
            ),
            GrammarExample(
                "De resultaten ondersteunen deze mogelijkheid zonder haar definitief te bewijzen."
            ),
        ],
        common_mistakes=[],
        related=["modaliteit-bron", "bereik-ontkenning", "argumentatieve-samenhang"],
    ),
]
