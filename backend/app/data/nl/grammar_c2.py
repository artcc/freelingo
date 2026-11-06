"""Dutch C2: nuanced interaction, expressive language and precise mediation."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="implicatuur-presuppositie",
        title="Reageren op aannames en onuitgesproken verwachtingen",
        level="C2",
        category="Pragmatiek",
        summary="Stel een aanname tactvol bij en vraag door zonder onbedoeld iets toe te zeggen.",
        explanation="Sommige formuleringen presenteren informatie als al bekend. Wanneer neem jij de planning weer over? gaat ervan uit dat jij die eerder beheerde en opnieuw zult overnemen. Je hoeft dat uitgangspunt niet te aanvaarden: De planning lag niet bij mij; ik wil wel bespreken hoe ik kan helpen. Een implicatuur ontstaat uit context: Sommige deelnemers stemden voor suggereert vaak niet allemaal, maar die beperking kan worden ingetrokken: misschien zelfs allemaal.\n\nReageer op wat voor de afspraak van belang is. Met Als je bedoelt dat ... kun je een mogelijke verwachting navragen zonder haar als feit te presenteren. Dat ik meedenk, wil niet zeggen dat ik de uitvoering op me neem begrenst een toezegging. Oefen een gesprek waarin de ander je antwoord te ruim opvat: herstel die indruk, erken diens behoefte en formuleer wat je wel kunt doen. De termen helpen bij de uitleg; in je reactie hoef je ze niet te gebruiken.",
        rules=[
            "Scheid letterlijke inhoud van contextuele gevolgtrekking.",
            "Vooronderstellingen kunnen worden betwist.",
            "Controleer of een implicatuur zonder tegenspraak kan worden ingetrokken.",
        ],
        examples=[
            GrammarExample(
                "Dat ik ernaar wil kijken, betekent nog niet dat ik het vandaag kan afronden."
            ),
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
        summary="Sluit aan op humor, herken een gevoelig punt en herstel een verkeerd gevallen grap.",
        explanation="Ironie kan een spanning oproepen tussen de letterlijke uitspraak en de bedoelde beoordeling. Na de derde storing kan Dat gaat lekker! kritiek uitdrukken, maar zonder context kan dezelfde zin oprecht positief zijn. Een understatement zwakt iets bewust af: Dat was niet ideaal kan een ernstige mislukking beschrijven.\n\nStem je reactie af op relatie en situatie. Bij een gedeelde tegenslag kan zelfspot de spanning verminderen; een grap over de fout van een onbekende kan kleinerend overkomen. Vraag bij twijfel: Bedoel je dat serieus, of mis ik de grap? Herstel een mislukte grap door bedoeling én effect te benoemen: Ik maakte een grap over mijn planning, maar ik merk dat die verkeerd viel. Oefen twee reacties op dezelfde opmerking: een luchtige tegen een goede vriend en een zorgvuldige tegen een teleurgestelde klant. Leid ironie niet alleen uit losse woorden af.",
        rules=[
            "Baseer interpretatie op concrete aanwijzingen.",
            "Onderscheid ironie van letterlijk commentaar.",
            "Behoud ruimte voor meerdere lezingen als de tekst die toelaat.",
        ],
        examples=[
            GrammarExample(
                "Na de derde storing zei ze: 'Het papier doet het gelukkig nog. Zal ik de hand-outs uitdelen?'"
            ),
            GrammarExample(
                "Na de mislukte lancering noemde hij het resultaat 'niet helemaal ideaal'."
            ),
        ],
        common_mistakes=[],
        related=["partikels-interactie", "implicatuur-presuppositie"],
    ),
    GrammarTopic(
        slug="retorische-focus",
        title="Met contrast een bezwaar of onderhandelingsgrens formuleren",
        level="C2",
        category="Stijl",
        summary="Richt kritiek op het bedoelde punt en maak duidelijk waar wel en geen ruimte voor overleg is.",
        explanation="Contrast helpt om een verkeerd begrepen bezwaar bij te stellen: Niet het doel staat ter discussie, maar de manier waarop we het willen bereiken. Met Over de termijn kunnen we praten; over de veiligheid niet maak je onderhandelingsruimte zichtbaar. Een gespleten zin legt focus: Het is de uitvoering die tekortschiet. Of die nadruk andere problemen uitsluit, hangt mede van de context af.\n\nEen retorische vraag als Wie wil er nu onveilig drinkwater? kan instemming met een doel als steun voor één plan presenteren. Reageer door het gedeelde doel te erkennen en de keuze opnieuw te openen: Veiliger water willen we allemaal; welke andere aanpakken zijn onderzocht? Oefen een overleg waarin je een misverstand over je bezwaar herstelt en daarna een concreet compromis voorstelt. Gebruik herhaling om je grens helder te maken, niet om een ontbrekend argument te verbergen.",
        rules=[
            "Een retorische vraag is geen bewijs.",
            "Controleer of focus exclusiviteit suggereert of werkelijk uitdrukt.",
            "Gebruik herhaling doelgericht, niet als vervanging van argumentatie.",
        ],
        examples=[
            GrammarExample("Het is niet de ambitie, maar de uitvoering die tekortschiet."),
            GrammarExample(
                "Over de volgorde kan ik meebewegen; over het overslaan van de controle niet."
            ),
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
        summary="Vraag gericht door en leg een afspraak vast zonder ontbrekende informatie in te vullen.",
        explanation="De zin Ik zag de man met de verrekijker kan gaan over het instrument waarmee ik keek of over een man die een verrekijker had. In praktische afspraken zijn de gevolgen vaak groter: De aanvraag moet vrijdag rond zijn kan doelen op indienen of op goedkeuren. Vraag dan welke handeling en welk moment bedoeld zijn. Ook het bereik van een beperking telt: Je hoeft niet alle bijlagen door te sturen betekent niet dat je geen enkele bijlage hoeft door te sturen.\n\nControleer verwijswoorden, het bereik van ontkenning, uitzonderingen en tijdsaanduidingen. Een huisgenoot kan bijvoorbeeld tegelijk een geregistreerde bewoner zijn; een instructie die de eerste groep uitsluit en de tweede aanschrijft vraagt verduidelijking. Oefen een kort gesprek: formuleer de twee relevante lezingen, laat de ander kiezen en bevestig de afspraak in één ondubbelzinnige zin. Maak de tekst niet preciezer door zelf een bevoegdheid, datum of uitzondering te verzinnen.",
        rules=[
            "Benoem eerst de mogelijke lezingen.",
            "Kies alleen een lezing die door context of opdracht wordt gesteund.",
            "Controleer deelnemers, instrument, tijd en bereik.",
        ],
        examples=[
            GrammarExample(
                "Bedoelt u met rond dat de aanvraag vrijdag ingediend of goedgekeurd moet zijn?"
            ),
            GrammarExample(
                "Dan spreken we af dat u de aanvraag vrijdag indient; de goedkeuring volgt later."
            ),
        ],
        common_mistakes=[],
        related=["samengestelde-zinnen", "bereik-ontkenning"],
    ),
    GrammarTopic(
        slug="formele-vaste-vormen",
        title="Formele vaste vormen herkennen",
        level="C2",
        category="Register",
        summary="Begrijp een formeel aanbod en reageer met behoud van voorwaarden en eigen grenzen.",
        explanation="In juridische, bestuurlijke of plechtige teksten komen vaste vormen voor zoals onverminderd, behoudens, zij het en hoe het ook zij. Zij het introduceert meestal een beperking of concessie: Het plan is uitvoerbaar, zij het tegen hoge kosten. Behoudens betekent doorgaans met uitzondering van of onder voorbehoud van, afhankelijk van de combinatie. Onverminderd geeft aan dat het daarna genoemde blijft gelden: een betaling onverminderd een verplichting heft die verplichting niet op.\n\nVertaal een formele mededeling naar handelingen: wie moet wat doen, vóór welk moment en onder welke voorwaarden? Oefen een antwoord op een aanbod dat je gedeeltelijk wilt aannemen. Benoem expliciet wat je aanvaardt en welk punt nog openstaat. Gebruik gewone woorden als ze dezelfde betekenis bewaren. Bij juridische formuleringen gaat deze oefening over de gegeven taalbetekenis; een korte parafrase is geen volledige beoordeling van rechtsgevolgen.",
        rules=[
            "Leer vaste uitdrukkingen als geheel.",
            "Zij het voegt een beperking toe en trekt niet de hele uitspraak in.",
            "Pas register aan genre en publiek aan.",
        ],
        examples=[
            GrammarExample(
                "Wij stemmen in, zij het onder voorbehoud van goedkeuring door het bestuur."
            ),
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
        title="Berichten samenbrengen en afspraken bemiddelen",
        level="C2",
        category="Tekst",
        summary="Vat uiteenlopende bijdragen samen en formuleer een vervolgstap zonder schijnbare overeenstemming.",
        explanation="Een synthese ordent bijdragen rond een vraag en maakt overeenstemming, verschil en onzekerheid zichtbaar. Dat is ook nodig in een gesprek: de planner kan vrijdag toezeggen als onderdelen woensdag bij ons zijn, terwijl de leverancier woensdag alleen als verwachte ontvangst bij zichzelf noemt. Samen leveren die berichten nog geen toezegging voor vrijdag op. Twee kranten die hetzelfde persbericht overnemen zijn evenmin twee onafhankelijke bevestigingen.\n\nBehoud voorwaarden, tijd, aantallen en de persoon aan wie een uitspraak toebehoort. Oefen bemiddeling tussen twee mensen die hetzelfde doel steunen maar onverenigbare voorwaarden stellen. Benoem wat gedeeld is, wat openblijft en welke beslissing of informatie nodig is. Laat de betrokkenen je samenvatting corrigeren. Herzie bij nieuwe informatie alleen het deel van je conclusie dat daardoor verandert. Bij onderzoek geldt hetzelfde: een resultaat in één steekproef mag niet worden uitgebreid tot iedereen.",
        rules=[
            "Bewaar bronstatus, voorwaarden en reikwijdte.",
            "Scheid overeenstemming van onafhankelijke bevestiging.",
            "Laat onzekerheid zichtbaar in de eindconclusie.",
        ],
        examples=[
            GrammarExample(
                "Jullie steunen allebei het ontwerp, maar over de avondopenstelling zijn jullie het nog niet eens."
            ),
            GrammarExample(
                "Als de leverancier woensdag bedoelt als aankomst bij hem, kunnen wij vrijdag nog niet toezeggen."
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
        summary="Geef terughoudende waardering en formuleer een bezwaar zonder je oordeel onbedoeld te versterken.",
        explanation="Een litotes formuleert een oordeel via ontkenning van het tegendeel: niet onaardig, niet onbelangrijk. De betekenis kan voorzichtig positief zijn, maar ook sterker waarderend klinken door intonatie. Niet onaardig is daarom niet in elke context een exacte vervanging voor geweldig.\n\nIn niet zonder gevolgen wordt het ontbreken van gevolgen ontkend. Dat zegt nog niets over hun omvang of wenselijkheid. Bij meerdere ontkenningen helpt een stapsgewijze parafrase, maar een louter logische omzetting kan pragmatische terughoudendheid verliezen. Onderscheid betekenis, gebruikelijke suggestie en toon, vooral wanneer een tekst verantwoordelijkheid of waardering bewust afzwakt.",
        rules=[
            "Een dubbele ontkenning kan een pragmatisch voorzichtiger oordeel geven.",
            "Niet zonder gevolgen zegt niet automatisch ernstige gevolgen.",
            "Controleer bereik en intonatie voordat je de uitspraak versterkt.",
            "Oefen feedback met waardering én een concreet verbeterpunt; laat de ander navragen hoe sterk je oordeel is.",
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
        summary="Vertel een ervaring met passend ritme en behoud het perspectief van degene die haar beleefde.",
        explanation="Een reeks korte zinnen kan haast, afstand of spanning oproepen; een lange zin kan een gedachte uitstellen, verbinden of laten voortstromen. De vorm bepaalt dat effect niet alleen: woordkeuze, genre en omliggende zinnen blijven nodig. Een fragment als Te laat kan in een verhaal betekenisvol zijn zonder een volledige persoonsvorm.\n\nBij redactie moet je bepalen wat een ritmische ingreep verandert. Het splitsen van een lange zin kan een voorwaarde losmaken van de uitspraak waarop zij betrekking heeft. Herhaling kan nadruk geven of perspectief markeren en is niet altijd overbodig. Bewaar de stem van de spreker of verteller wanneer je de leesbaarheid verbetert.",
        rules=[
            "Koppel een stijleffect aan concrete contextuele aanwijzingen.",
            "Een zinsfragment kan doelbewust functioneren binnen een tekst.",
            "Laat bij opsplitsing voorwaarden en verwijzingen intact.",
            "Vertel dezelfde gebeurtenis als persoonlijk relaas en als zakelijk verslag; verander ritme en toon zonder feiten toe te voegen.",
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
        summary="Wissel natuurlijk tussen een vertrouwelijk gesprek en een zakelijke reactie zonder je grens te veranderen.",
        explanation="Een idioom heeft naast zijn kernbetekenis vaak een register en houding. De boot afhouden suggereert afstand tot een verzoek; voorlopig niet instemmen kan neutraler klinken. Geen blad voor de mond nemen kan als openhartig of als weinig tactvol worden gewaardeerd. Water bij de wijn doen betekent toegeven om tot overeenstemming te komen; iemand voor het blok zetten beperkt diens ruimte om vrij te kiezen.\n\nTegen een vriend kun je zeggen: Ik wil best water bij de wijn doen, maar ik laat me niet voor het blok zetten. Tegen een nieuwe zakenpartner kan dat worden: Ik zie ruimte voor aanpassingen, maar wil de voorwaarden afwegen voordat ik mij verbind. Oefen beide versies en reageer op een onverwachte tegenwerping. Behoud bereidheid, grens en mate van instemming; maak een voorzichtig antwoord niet stelliger alleen om het formeler te laten klinken. Kies gangbare verbindingen die bij de relatie passen, geen opeenstapeling van idiomen.",
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
