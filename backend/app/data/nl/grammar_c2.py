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
    GrammarTopic(
        slug="metaforische-patronen",
        title="Beeldspraak als kader voor een redenering",
        level="C2",
        category="Betekenis",
        summary="Herken hoe een metafoor verwachtingen oproept zonder haar letterlijk te maken.",
        explanation="Een tekst kan een debat als strijd, een loopbaan als reis of een organisatie als machine voorstellen. Zo'n beeld activeert bijpassende woorden en verwachtingen: een aanval weerleggen, een koers kiezen, een radertje vervangen. Die verwachtingen zijn geen feitelijke eigenschappen van het onderwerp.\n\nAnalyseer welke aspecten het beeld zichtbaar maakt en welke het verbergt. Een organisatie als machine kan menselijke autonomie uit beeld drukken. Bij parafraseren moet de bedoelde beoordeling behouden blijven zonder alle onderdelen van het beeld letterlijk over te nemen. Een gemengd beeld kan onbedoeld onduidelijk zijn, maar ook bewust komisch werken; context bepaalt de beoordeling.",
        rules=[
            "Scheid letterlijke inhoud van door het beeld opgeroepen associaties.",
            "Volg een metafoor door meerdere zinnen heen.",
            "Beoordeel beeldvermenging op functie, niet alleen op aanwezigheid.",
        ],
        examples=[
            GrammarExample(
                "De onderhandelingen zitten muurvast; beide partijen zoeken een uitweg."
            ),
            GrammarExample(
                "De auteur noemt werknemers radertjes en zet daarmee hun individuele ruimte op de achtergrond."
            ),
        ],
        common_mistakes=[],
        related=["implicatuur-presuppositie", "retorische-focus"],
    ),
    GrammarTopic(
        slug="litotes-meervoudige-ontkenning",
        title="Niet onaardig en niet zonder gevolgen",
        level="C2",
        category="Pragmatiek",
        summary="Interpreteer ontkennende omschrijvingen zonder nuance tot een absoluut oordeel te reduceren.",
        explanation="Een litotes formuleert een oordeel via ontkenning van het tegendeel: niet onaardig, niet onbelangrijk. De betekenis kan voorzichtig positief zijn, maar ook sterker waarderend klinken door intonatie. Niet onaardig is daarom niet in elke context een exacte vervanging voor geweldig.\n\nIn niet zonder gevolgen wordt het ontbreken van gevolgen ontkend. Dat zegt nog niets over hun omvang of wenselijkheid. Bij meerdere ontkenningen helpt een stapsgewijze parafrase, maar een louter logische omzetting kan pragmatische terughoudendheid verliezen. Onderscheid betekenis, gebruikelijke suggestie en toon, vooral wanneer een tekst verantwoordelijkheid of waardering bewust afzwakt.",
        rules=[
            "Een dubbele ontkenning kan een pragmatisch voorzichtiger oordeel geven.",
            "Niet zonder gevolgen zegt niet automatisch ernstige gevolgen.",
            "Controleer bereik en intonatie voordat je de uitspraak versterkt.",
        ],
        examples=[
            GrammarExample("Het resultaat is niet onaardig, al blijft verbetering mogelijk."),
            GrammarExample("Die keuze was niet zonder gevolgen voor de samenwerking."),
        ],
        common_mistakes=[],
        related=["bereik-ontkenning", "ironie-onderstatement"],
    ),
    GrammarTopic(
        slug="stilistische-inversie",
        title="Vooropplaatsing, contrast en retorisch ritme",
        level="C2",
        category="Stijl",
        summary="Gebruik gemarkeerde woordvolgorde doelgericht met behoud van grammaticale rollen.",
        explanation="Een vooropgeplaatst zinsdeel kan een argument markeren: Onbegrijpelijk is vooral de haast waarmee het besluit is genomen. De formulering begint met een oordeel en stelt de toelichting uit. In Dat besluit, dat verdedig ik niet herneemt een verwijswoord het vooropgeplaatste onderwerp van gesprek. Dat is een ander patroon dan gewone inversie.\n\nDeze vormen passen niet automatisch bij iedere zakelijke tekst. Ze kunnen in een betoog, gesprek of literaire passage nadruk en ritme geven. Behoud bij een neutralere versie de precieze beperking: vooral de haast is niet hetzelfde als alles aan het besluit. Ook gemarkeerde volgorde moet begrijpelijke relaties houden.",
        rules=[
            "Onderscheid gewone vooropplaatsing van een los thema met hervatting.",
            "Gemarkeerde volgorde is een stijlmiddel, geen universele verbetering.",
            "Controleer onderwerp, voorwerp en bereik van het contrast.",
        ],
        examples=[
            GrammarExample("Opvallend is juist wat de brief niet vermeldt."),
            GrammarExample("Die ene voorwaarde, daar wil ik niet van afwijken."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Dat besluit ik verdedig niet.",
                "Dat besluit verdedig ik niet.",
                "Zonder los thema en hervatting blijft de persoonsvorm op de tweede zinsdeelplaats.",
            )
        ],
        related=["focus-woordvolgorde", "retorische-focus"],
    ),
    GrammarTopic(
        slug="zeugma-samentrekking",
        title="Een gedeeld woord met twee verschillende functies",
        level="C2",
        category="Stijl",
        summary="Onderscheid een heldere ellips van een onbedoelde of speelse betekenisbotsing.",
        explanation="Een gedeeld woord kan in twee verbonden delen een verschillende betekenis krijgen: Hij nam zijn jas en afscheid. Het werkwoord nemen hoort hier bij een concreet voorwerp en bij de vaste verbinding afscheid nemen. Het effect kan bewust geestig zijn; in een neutraal verslag kan dezelfde botsing ongewenst afleiden.\n\nBij gewone samentrekking moet de aanvulling grammaticaal en inhoudelijk begrijpelijk blijven. Schrijf beide delen eerst volledig uit. Controleer of het gedeelde woord werkelijk dezelfde functie heeft en of het publiek het bedoelde spel kan volgen. Een stilistische afwijking is niet automatisch een bruikbaar productiemodel voor elke tekstsoort.",
        rules=[
            "Vul het weggelaten deel in beide constructies aan.",
            "Onderscheid grammaticale functie van woordbetekenis.",
            "Beoordeel een bewust zeugma vanuit genre en effect.",
        ],
        examples=[
            GrammarExample(
                "Hij nam zijn jas en afscheid: de zin speelt met twee betekenissen van nemen."
            ),
            GrammarExample("In het verslag staat neutraler: Hij pakte zijn jas en nam afscheid."),
        ],
        common_mistakes=[],
        related=["ellips-parallelisme", "idiomatische-werkwoordverbindingen"],
    ),
    GrammarTopic(
        slug="ritme-zinslengte",
        title="Zinsritme, herhaling en stiltes",
        level="C2",
        category="Tekst",
        summary="Analyseer hoe syntaxis tempo, perspectief en ondertoon beïnvloedt.",
        explanation="Een reeks korte zinnen kan haast, afstand of spanning oproepen; een lange zin kan een gedachte uitstellen, verbinden of laten voortstromen. De vorm bepaalt dat effect niet alleen: woordkeuze, genre en omliggende zinnen blijven nodig. Een fragment als Te laat kan in een verhaal betekenisvol zijn zonder een volledige persoonsvorm.\n\nBij redactie moet je bepalen wat een ritmische ingreep verandert. Het splitsen van een lange zin kan een voorwaarde losmaken van de uitspraak waarop zij betrekking heeft. Herhaling kan nadruk geven of perspectief markeren en is niet altijd overbodig. Bewaar de stem van de spreker of verteller wanneer je de leesbaarheid verbetert.",
        rules=[
            "Koppel een stijleffect aan concrete contextuele aanwijzingen.",
            "Een zinsfragment kan doelbewust functioneren binnen een tekst.",
            "Laat bij opsplitsing voorwaarden en verwijzingen intact.",
        ],
        examples=[
            GrammarExample("Hij wachtte. Geen voetstappen. Geen antwoord."),
            GrammarExample(
                "Ze wilde antwoorden, maar terwijl ze naar woorden zocht, sloeg de deur al dicht."
            ),
        ],
        common_mistakes=[],
        related=["perspectief-vrije-indirecte-rede", "tangconstructies"],
    ),
    GrammarTopic(
        slug="versteende-naamvallen",
        title="Ten behoeve van en ter zake",
        level="C2",
        category="Register",
        summary="Herken historische vormen in vaste uitdrukkingen zonder er productieve regels van te maken.",
        explanation="Oudere naamvalsvormen leven voort in vaste combinaties: ten behoeve van, ter plaatse, ter zake en in de loop der jaren. Deze uitdrukkingen kunnen formeel, ambtelijk of volledig ingeburgerd zijn. Hun vorm is niet vrij uitbreidbaar naar elk nieuw naamwoord. Leer ze als vaste eenheden.\n\nEen moderne parafrase kan de betekenis toegankelijker maken: ten behoeve van het onderzoek wordt voor het onderzoek. Maar register en soms precieze relatie veranderen mee. Controleer daarom de functie in de zin en gebruik zulke vormen in eigen teksten alleen wanneer genre en publiek dat rechtvaardigen. Historische herkenning is belangrijker dan kunstmatig plechtig schrijven.",
        rules=[
            "Behandel historische vormen als vaste uitdrukkingen.",
            "Controleer spelling en voorzetsel bij twijfel.",
            "Parafraseer op basis van context, niet alleen op woordniveau.",
        ],
        examples=[
            GrammarExample("De gegevens zijn uitsluitend ten behoeve van dit onderzoek verzameld."),
            GrammarExample("De situatie wordt ter plaatse beoordeeld."),
        ],
        common_mistakes=[
            GrammarMistake(
                "De situatie wordt ten plaatse beoordeeld.",
                "De situatie wordt ter plaatse beoordeeld.",
                "De vaste uitdrukking is ter plaatse.",
            )
        ],
        related=["formele-vaste-vormen", "formeel-informeel"],
    ),
    GrammarTopic(
        slug="conjunctief-wensen",
        title="Leve, moge en men neme",
        level="C2",
        category="Register",
        summary="Herken vaste aanvoegende vormen als wens, aansporing of genrekenmerk.",
        explanation="De aanvoegende wijs komt in het huidige Nederlands vooral voor in vaste, plechtige of stilistisch gemarkeerde uitdrukkingen: Leve de vrijheid; Moge het u goed gaan; Men neme een ruime kom. De vorm kan een wens of aansporing uitdrukken, niet een vastgestelde gebeurtenis.\n\nVerwar moge niet met gewone toestemming door mogen. De spreker die Moge het u goed gaan zegt, wenst iets toe. In moderne instructies is Neem een ruime kom meestal natuurlijker dan Men neme. Het doel is zulke vormen correct interpreteren en passend parafraseren, niet ze verplicht in alledaagse gesprekken produceren.",
        rules=[
            "Een aanvoegende vorm kan een wens of aansporing uitdrukken.",
            "Leve is in deze formule geen gewone persoonsvorm leeft.",
            "Pas eigen productie aan genre en publiek aan.",
        ],
        examples=[
            GrammarExample("Moge deze samenwerking lang voortduren."),
            GrammarExample("Leve de vrijheid!"),
        ],
        common_mistakes=[],
        related=["formele-vaste-vormen", "gebiedende-wijs"],
    ),
    GrammarTopic(
        slug="register-idiomatiek",
        title="Idioom, sociale afstand en betekenisbehoud",
        level="C2",
        category="Idiomatiek",
        summary="Kies en parafraseer uitdrukkingen met aandacht voor toon en relatie.",
        explanation="Een idioom heeft naast zijn kernbetekenis vaak een register en houding. De boot afhouden suggereert afstand tot een verzoek; voorlopig niet instemmen kan neutraler klinken. Geen blad voor de mond nemen kan als openhartig of als weinig tactvol worden gewaardeerd, afhankelijk van de situatie.\n\nEen letterlijke vertaling bewaart het beeld soms maar verliest de gebruikelijke betekenis. Een neutrale parafrase kan juist de ondertoon wissen. Benoem wat je wilt behouden: feitelijke inhoud, evaluatie, humor of sociale afstand. Vermijd zeldzame uitdrukkingen als versiering wanneer een gewone formulering beter past. Natuurlijk taalgebruik vraagt een keuze, geen maximale idiomendichtheid.",
        rules=[
            "Analyseer betekenis, register en impliciete beoordeling afzonderlijk.",
            "Een parafrase moet de voor de opdracht relevante ondertoon behouden.",
            "Idiomatisch spreken betekent passende combinaties kiezen.",
        ],
        examples=[
            GrammarExample(
                "Hij hield de boot af: hij wilde zich nog niet aan het voorstel verbinden."
            ),
            GrammarExample(
                "Zij zei het tussen neus en lippen door, alsof het slechts een bijzaak was."
            ),
        ],
        common_mistakes=[],
        related=["idiomatische-werkwoordverbindingen", "variatie-norm", "ironie-onderstatement"],
    ),
]
