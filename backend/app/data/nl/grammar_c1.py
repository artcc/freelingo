"""Dutch C1: source-aware argumentation and register control."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="modaliteit-bron",
        title="Zekerheid, waarschijnlijkheid en bronafstand",
        level="C1",
        category="Modaliteit",
        summary="Scheid feiten, gevolgtrekkingen en onbevestigde berichten.",
        explanation="Kennelijk geeft doorgaans een gevolgtrekking uit aanwijzingen; vermoedelijk een waarschijnlijkheidsinschatting. Naar verluidt schrijft een bericht aan niet nader genoemde bronnen toe. Zou kan berichtgeving op afstand markeren: De minister zou vertrekken. Zonder context kan zou ook een voorwaarde of toekomst-in-het-verleden uitdrukken.\n\nVolgens het rapport maakt de bron zichtbaar, maar bewijst de inhoud niet. Behoud bij samenvatten het niveau van zekerheid: Er zijn aanwijzingen voor fraude is niet gelijk aan Er is fraude bewezen. Kies expliciete formuleringen als de interpretatie van een modaal woord onzeker blijft.",
        rules=[
            "Noem de bron waar die relevant is.",
            "Maak van een vermoeden geen vastgesteld feit.",
            "Lees zou in zijn volledige context.",
        ],
        examples=[
            GrammarExample("Volgens de onderzoekers kan de maatregel helpen."),
            GrammarExample("Naar verluidt zou de directeur aftreden."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Volgens de onderzoekers de maatregel kan helpen.",
                "Volgens de onderzoekers kan de maatregel helpen.",
                "De bronbepaling vult het eerste zinsdeel.",
            )
        ],
        related=["indirecte-rede", "voorwaarden-zou"],
    ),
    GrammarTopic(
        slug="bereik-ontkenning",
        title="Niet allemaal, allemaal niet en slechts",
        level="C1",
        category="Betekenis",
        summary="Controleer het bereik van ontkenning en kwantoren.",
        explanation="Niet alle aanvragen zijn goedgekeurd zegt dat minstens één aanvraag niet is goedgekeurd; het zegt op zichzelf niet hoeveel wel zijn goedgekeurd. Geen enkele aanvraag is goedgekeurd sluit alle goedkeuringen uit. Zulke verschillen zijn essentieel in rapporten en samenvattingen.\n\nWoorden als slechts, vrijwel, minstens en hoogstens begrenzen een uitspraak. Minstens tien is niet precies tien. Niet onwaarschijnlijk betekent niet automatisch zeker. Controleer bij herformuleren welke situaties door de oorspronkelijke zin worden toegestaan en sluit die niet onbedoeld uit.",
        rules=[
            "Niet alle is geen synoniem van geen enkele.",
            "Behoud grenzen zoals minstens en hoogstens.",
            "Negatieve omschrijvingen kunnen voorzichtiger zijn dan een positief absoluut oordeel.",
        ],
        examples=[
            GrammarExample("Niet alle deelnemers waren het eens."),
            GrammarExample("Hoogstens drie aanvragen worden opnieuw beoordeeld."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Geen enkele aanvragen is goedgekeurd.",
                "Geen enkele aanvraag is goedgekeurd.",
                "Geen enkele krijgt hier een enkelvoudig naamwoord.",
            )
        ],
        related=["niet-geen", "onbepaalde-woorden"],
    ),
    GrammarTopic(
        slug="ellips-parallelisme",
        title="Samentrekking en parallelle formulering",
        level="C1",
        category="Zinsbouw",
        summary="Laat herhaling weg zonder grammaticale rollen te verwarren.",
        explanation="Je kunt gedeelde informatie weglaten als de lezer die grammaticaal en inhoudelijk kan aanvullen: Noor schreef de inleiding en Sam de conclusie. De ontbrekende persoonsvorm is schreef. Een samentrekking wordt onduidelijk als een weggelaten woord in het tweede deel een andere functie of betekenis moet krijgen.\n\nParallelle formuleringen helpen in opsommingen: om kosten te beperken, tijd te besparen en fouten te voorkomen. Vermijd schijnbare symmetrie waarbij een deel een persoon en het andere een resultaat vergelijkt. Schrijf de volledige zinnen uit om de constructie te controleren.",
        rules=[
            "Controleer de aanvulling van elk weggelaten deel.",
            "Gebruik vergelijkbare grammaticale vormen in een opsomming.",
            "Compactheid mag geen onduidelijke rolverdeling veroorzaken.",
        ],
        examples=[
            GrammarExample("Noor onderzocht de oorzaken en Sam de gevolgen."),
            GrammarExample("Het doel is kosten te beperken en kwaliteit te behouden."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Het plan is om kosten te beperken en fouten voorkomen.",
                "Het plan is om kosten te beperken en fouten te voorkomen.",
                "Beide doelinfinitieven hebben hier te nodig.",
            )
        ],
        related=["te-infinitief", "samengestelde-zinnen"],
    ),
    GrammarTopic(
        slug="beknopte-bijzinnen",
        title="Beknopte bijzinnen en verzwegen onderwerpen",
        level="C1",
        category="Zinsbouw",
        summary="Maak duidelijk wie de handeling in een verkorte bijzin uitvoert.",
        explanation="In een beknopte bijzin ontbreekt een expliciet onderwerp: Na het rapport te hebben gelezen, stelde Noor vragen. Noor is degene die leest en vragen stelt. Bij een onduidelijk of verkeerd gekoppeld onderwerp ontstaat een zwevende bepaling: Lopend naar huis begon het te regenen suggereert grammaticaal een onmogelijke koppeling.\n\nHerschrijf dan met een volledige bijzin: Toen ik naar huis liep, begon het te regenen. Niet iedere beknopte constructie volgt precies hetzelfde patroon; controleer de concrete werkwoordelijke relatie in plaats van een absolute regel voor alle infinitieven te geven.",
        rules=[
            "Controleer wie het verzwegen onderwerp is.",
            "Maak een volledige bijzin als de koppeling onduidelijk is.",
            "Behoud de tijdsverhouding bij verkorting.",
        ],
        examples=[
            GrammarExample(
                "Na de cijfers te hebben gecontroleerd, publiceerde de redactie het artikel."
            ),
            GrammarExample("Om de deadline te halen, werkte het team langer door."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Lopend naar huis begon het te regenen.",
                "Toen ik naar huis liep, begon het te regenen.",
                "Maak de lopende persoon expliciet.",
            )
        ],
        related=["te-infinitief", "deelwoord-bijvoeglijk"],
    ),
    GrammarTopic(
        slug="partikels-interactie",
        title="Maar, toch, eens en even in gesprekken",
        level="C1",
        category="Pragmatiek",
        summary="Herken hoe kleine woorden de toon en verwachtingen veranderen.",
        explanation="Partikels hebben geen vaste één-op-éénvertaling. Kom maar binnen kan toestemming en geruststelling uitdrukken. Kom toch binnen kan aandringen of verbazing tonen. Kun je even kijken? verkleint vaak de voorgestelde inspanning, maar kan afhankelijk van toon ook druk uitoefenen.\n\nToch kan eerder gedeelde kennis oproepen: Je komt morgen toch? Nou markeert vaak een reactie of overgang. Interpreteer woordkeuze samen met intonatie, beurtpositie en relatie. Voeg zulke woorden niet automatisch toe om ieder verzoek beleefd te maken.",
        rules=[
            "Interpreteer partikels samen met intonatie en context.",
            "Even garandeert geen korte duur of beleefdheid.",
            "Een vraag met toch kan bevestiging verwachten.",
        ],
        examples=[
            GrammarExample("Ga maar zitten; we hebben alle tijd."),
            GrammarExample("Je hebt de uitnodiging toch ontvangen?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Kun je even kijkt?",
                "Kun je even kijken?",
                "Het partikel verandert de infinitiefconstructie na kunnen niet.",
            )
        ],
        related=["gebiedende-wijs", "focus-woordvolgorde"],
    ),
    GrammarTopic(
        slug="formeel-informeel",
        title="Register aanpassen zonder betekenisverlies",
        level="C1",
        category="Register",
        summary="Schrijf toegankelijk, zakelijk of persoonlijk met behoud van inhoud.",
        explanation="Formeel taalgebruik is niet hetzelfde als moeilijke woorden gebruiken. Een zakelijke tekst kan helder en direct zijn. Vergelijk Stuur de stukken uiterlijk vrijdag met Gelieve de stukken uiterlijk vrijdag toe te sturen: beide noemen dezelfde termijn, maar de tweede klinkt afstandelijker.\n\nBehoud bij herschrijven verplichting, termijn, bron en aanspreekvorm. Een verzoek mag niet onbedoeld een bevel worden. Je/u hangt af van relatie en huisstijl. In Nederland gebruikelijke vormen zijn niet de enige correcte Nederlandse vormen; label Belgische of Surinaamse standaardvarianten als varianten wanneer je ze bespreekt.",
        rules=[
            "Pas toon aan publiek en tekstdoel aan.",
            "Behoud verplichting, termijn en mate van zekerheid.",
            "Verwar regionale variatie niet met een taalfout.",
        ],
        examples=[
            GrammarExample("Zou u de stukken uiterlijk vrijdag willen toesturen?"),
            GrammarExample("Stuur je me de stukken uiterlijk vrijdag?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "U kunt jouw aanvraag aanpassen.",
                "U kunt uw aanvraag aanpassen.",
                "Bij verwijzing naar dezelfde aangesprokene blijft de aanspreekvorm consistent.",
            )
        ],
        related=["men-er-je", "hen-hun-register"],
    ),
    GrammarTopic(
        slug="argumentatieve-samenhang",
        title="Een stelling begrenzen en onderbouwen",
        level="C1",
        category="Tekst",
        summary="Verbind bewijs, tegenwerping en conclusie zorgvuldig.",
        explanation="Een overtuigend betoog onderscheidt een stelling, argument, voorbeeld en tegenwerping. Weliswaar ... maar erkent een punt en begrenst de betekenis ervan: De maatregel is weliswaar duur, maar voorkomt grotere schade. Dat bewijst nog niet dat de maatregel altijd wenselijk is.\n\nImmers licht vaak een eerdere uitspraak toe; derhalve presenteert een gevolgtrekking en klinkt formeel. Een verbindingswoord maakt een gevolgtrekking niet vanzelf geldig. Behoud voorwaarden en beperkingen van de bron en benoem waar aanvullende aannames nodig zijn.",
        rules=[
            "Scheid een voorbeeld van algemeen bewijs.",
            "Gebruik concessie zonder de tegenwerping te vervalsen.",
            "Laat de conclusie niet verder gaan dan de onderbouwing.",
        ],
        examples=[
            GrammarExample("De aanpak is weliswaar kostbaar, maar ook effectief."),
            GrammarExample(
                "Deze cijfers wijzen op een verband; een oorzaak is daarmee nog niet aangetoond."
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                "Hoewel de aanpak duur is, maar levert die voordeel op.",
                "Hoewel de aanpak duur is, levert die voordeel op.",
                "Kies één samenhangend concessief patroon.",
            )
        ],
        related=["concessie-voorwaarden", "modaliteit-bron"],
    ),
    GrammarTopic(
        slug="verwijzing-cohesie",
        title="Dit, dat, deze en zulke in een tekst",
        level="C1",
        category="Tekst",
        summary="Maak verwijzingen over meerdere zinnen helder.",
        explanation="Een verwijswoord kan naar een naamwoord, een gebeurtenis of een hele redenering verwijzen. Deze oplossing verwijst explicieter dan dit wanneer meerdere zaken genoemd zijn. Bij het hernemen van een gehele mededeling kan dat natuurlijk zijn: De kosten stijgen. Dat baart ons zorgen.\n\nGebruik een samenvattend naamwoord om een verband zichtbaar te maken: deze ontwikkeling, dit bezwaar, die veronderstelling. Zo'n naamwoord voegt ook een interpretatie toe. Noem een onbewezen beschuldiging daarom niet zomaar dit feit. Controleer zowel grammaticale aansluiting als inhoudelijke neutraliteit.",
        rules=[
            "Maak het antecedent eenduidig.",
            "Kies een samenvattend naamwoord dat de bronstatus behoudt.",
            "Laat herhaling staan als die nodig is voor duidelijkheid.",
        ],
        examples=[
            GrammarExample("De vraag neemt toe. Deze ontwikkeling vraagt om extra capaciteit."),
            GrammarExample(
                "De auteur noemt een mogelijkheid; die veronderstelling blijft onbewezen."
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                "De kosten stijgt. Dat baart ons zorgen.",
                "De kosten stijgen. Dat baart ons zorgen.",
                "Het onderwerp kosten is meervoud; dat verwijst daarna naar de hele mededeling.",
            )
        ],
        related=["samengestelde-zinnen", "modaliteit-bron"],
    ),
    GrammarTopic(
        slug="passief-rapportage",
        title="Er wordt aangenomen dat",
        level="C1",
        category="Register",
        summary="Maak de status en herkomst van een gerapporteerde bewering zichtbaar.",
        explanation="Er wordt aangenomen dat en Er is vastgesteld dat lijken grammaticaal op elkaar, maar geven een andere kennisstatus. Aannemen kan een veronderstelling aangeven; vaststellen presenteert een bevinding. Een passieve formulering noemt niet noodzakelijk wie dat oordeel heeft gevormd.\n\nKies een actieve bronvermelding als de lezer die nodig heeft: De onderzoekers nemen aan dat de vraag stijgt. Maak bij het samenvatten van wordt vermoed geen is bewezen. Ook lijkt te en schijnt te kunnen afstand of onzekerheid uitdrukken, maar zijn niet altijd gelijk aan een expliciet genoemde bron. Controleer de oorspronkelijke formulering en haar context.",
        rules=[
            "Behoud het verschil tussen vermoeden, aannemen en vaststellen.",
            "Een onpersoonlijk passief is geen bewijs van brede overeenstemming.",
            "Noem de beoordelaar wanneer diens identiteit relevant is.",
        ],
        examples=[
            GrammarExample("Er wordt vermoed dat de storing meerdere oorzaken heeft."),
            GrammarExample("De inspectie heeft vastgesteld dat de controle niet is uitgevoerd."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Er wordt aangenomen dat stijgt de vraag.",
                "Er wordt aangenomen dat de vraag stijgt.",
                "De inhoudelijke dat-bijzin heeft bijzinvolgorde.",
            )
        ],
        related=["passief-onpersoonlijk", "modaliteit-bron"],
    ),
    GrammarTopic(
        slug="tijdsperspectief-verslag",
        title="Tijd en perspectief in een verslag",
        level="C1",
        category="Tijd",
        summary="Houd gebeurtenistijd, spreektijd en verslagmoment uit elkaar.",
        explanation="In een verslag kunnen drie momenten meespelen: wanneer iets gebeurde, wanneer iemand daarover sprak en wanneer jij het weergeeft. Gisteren en morgen veranderen daardoor mogelijk van referentie. Wie een uitspraak van maandag op woensdag samenvat, moet duidelijk maken welke dag met morgen werd bedoeld.\n\nEen tegenwoordige tijd in indirecte rede kan aangeven dat iets nog geldt: Zij zei dat de winkel gesloten is. Een verleden tijd kan het perspectief van het oorspronkelijke gesprek volgen. Geen van beide patronen mag mechanisch als universeel verplicht worden behandeld. Controleer ook of een verwachting inmiddels is uitgekomen; dat is aanvullende informatie, geen automatische tijdsverandering.",
        rules=[
            "Bepaal gebeurtenis, oorspronkelijke uitspraak en huidig verslagmoment.",
            "Vervang deiktische woorden alleen als hun referentie verschuift.",
            "Behoud het verschil tussen een verwachting en haar latere uitkomst.",
        ],
        examples=[
            GrammarExample(
                "Op maandag kondigde zij aan dat de winkel de volgende dag zou sluiten."
            ),
            GrammarExample("Zij vertelde gisteren dat ze nog steeds in Leiden woont."),
        ],
        common_mistakes=[],
        related=["indirecte-rede", "toekomst-in-verleden", "verhaaltijden"],
    ),
    GrammarTopic(
        slug="congruentie-complex",
        title="De kern van een uitgebreid onderwerp",
        level="C1",
        category="Congruentie",
        summary="Kies de persoonsvorm bij de syntactische kern, niet bij het dichtstbijzijnde naamwoord.",
        explanation="In De beoordeling van de verschillende aanvragen kost tijd is beoordeling de kern van het onderwerp. Het meervoud aanvragen maakt de persoonsvorm niet meervoudig. Lange bepalingen tussen onderwerp en werkwoord kunnen die structuur verbergen. Zoek daarom eerst de volledige onderwerpsgroep en daarna de kern.\n\nBij woorden als aantal en groep kan zowel de grammaticale vorm als de bedoelde verzameling een rol spelen. Een aantal deelnemers is/zijn vertrokken kent variatie; maak daarvan zonder nadere context geen vraag met één juiste vorm. Voor een heldere oefening kies je een ondubbelzinnige kern, zoals de beslissing of de besluiten.",
        rules=[
            "Een voorzetselgroep verandert niet automatisch het getal van de kern.",
            "Controleer congruentie over de hele zin heen.",
            "Erken betekenisafhankelijke variatie bij collectieve aanduidingen.",
        ],
        examples=[
            GrammarExample("De beslissing van de verschillende bestuurders is nog niet bekend."),
            GrammarExample("De besluiten over de financiering zijn opnieuw besproken."),
        ],
        common_mistakes=[
            GrammarMistake(
                "De beslissing van de bestuurders zijn bindend.",
                "De beslissing van de bestuurders is bindend.",
                "De kern beslissing is enkelvoud.",
            )
        ],
        related=["nominalisatie", "bijstelling"],
    ),
    GrammarTopic(
        slug="tangconstructies",
        title="Lange zinnen leesbaar ordenen",
        level="C1",
        category="Tekst",
        summary="Verklein de afstand tussen samenhangende zinsdelen zonder betekenisverlies.",
        explanation="Een tangconstructie ontstaat wanneer nauw verbonden delen ver uit elkaar staan. Vergelijk De door de commissie na langdurig overleg vastgestelde regeling met De regeling die de commissie na langdurig overleg heeft vastgesteld. De tweede vorm kan het verwerken van de informatie vergemakkelijken, maar beide kunnen grammaticaal correct zijn.\n\nHerschrijf alleen als de lezer er werkelijk bij gebaat is. Een splitsing mag voorwaarden, uitvoerder of tijdsvolgorde niet veranderen. Niet iedere lange zin is slecht en niet iedere korte zin helder. Bepaal eerst de kernboodschap en plaats aanvullende informatie waar haar relatie zichtbaar blijft.",
        rules=[
            "Zoek delen die de lezer lang in het geheugen moet houden.",
            "Een betrekkelijke bijzin kan een zware bepaling vóór het naamwoord vervangen.",
            "Behoud beperking en bronstatus bij het splitsen.",
        ],
        examples=[
            GrammarExample(
                "De regeling die de commissie gisteren heeft vastgesteld geldt vanaf januari."
            ),
            GrammarExample("Het team heeft de installatie gecontroleerd voordat de proef begon."),
        ],
        common_mistakes=[],
        related=["samengestelde-zinnen", "verwijzing-cohesie"],
    ),
    GrammarTopic(
        slug="woordvorming-afleiding",
        title="On-, -heid, -baar en -loos",
        level="C1",
        category="Woordvorming",
        summary="Leid betekenissen af zonder ieder voor- of achtervoegsel als vrij uitwisselbaar te behandelen.",
        explanation="Afleidingen maken nieuwe woorden met voor- of achtervoegsels: duidelijk/onduidelijk, mogelijk/mogelijkheid, verklaren/verklaarbaar. Het achtervoegsel -baar geeft vaak een mogelijkheid aan; -loos vaak het ontbreken van iets. Niet elk denkbaar nieuw woord is daarom gangbaar. Controleer onbekende combinaties in een woordenlijst of betrouwbare context.\n\nBetekenis kan verder gaan dan de losse delen: onmenselijk betekent doorgaans meer dan niet menselijk. Bij onzeker en niet zeker kunnen stijl en nadruk verschillen. Gebruik afleiding om woordfamilies en tekstverbanden te herkennen, maar verwar een morfologisch mogelijke vorm niet met een passende formulering voor ieder register.",
        rules=[
            "Een afleiding kan de woordsoort veranderen.",
            "Gangbaarheid en betekenis zijn niet volledig voorspelbaar uit de delen.",
            "Let op spelling: mogelijk wordt mogelijkheid.",
        ],
        examples=[
            GrammarExample("De onduidelijkheid over de voorwaarden belemmert de uitvoering."),
            GrammarExample("Het verschil is verklaarbaar, maar daarmee nog niet aanvaardbaar."),
        ],
        common_mistakes=[],
        related=["woordvorming-samenstellingen", "nominalisatie"],
    ),
    GrammarTopic(
        slug="beknopte-perfectum",
        title="Na te hebben gelezen en na te zijn vertrokken",
        level="C1",
        category="Zinsbouw",
        summary="Druk voortijdigheid uit in een beknopte bijzin met de juiste uitvoerder.",
        explanation="Na het rapport te hebben gelezen, stelde Noor vragen plaatst het lezen vóór het vragen stellen. De beknopte bijzin bevat een voltooide infinitief met hebben of zijn. Het hulpwerkwoord volgt de gewone constructie: gelezen hebben, vertrokken zijn. Noor is hier het verzwegen onderwerp van de bijzin.\n\nEen passieve vorm vraagt extra aandacht: Na te zijn gecontroleerd, werd de installatie vrijgegeven. De installatie ondergaat beide handelingen. Herschrijf met een volledige bijzin als de koppeling tussen onderwerp en handeling onduidelijk wordt. Voortijdigheid moet behouden blijven; na is niet hetzelfde als tijdens.",
        rules=[
            "Een voltooide infinitief kan een eerdere handeling aanduiden.",
            "Kies hebben of zijn vanuit het werkwoordelijke patroon.",
            "Controleer het verzwegen onderwerp bij actieve en passieve vormen.",
        ],
        examples=[
            GrammarExample("Na de gegevens te hebben vergeleken, herschreef zij de conclusie."),
            GrammarExample("Na uit het ziekenhuis te zijn ontslagen, herstelde hij thuis verder."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Na te hebben vertrokken, belde hij zijn collega.",
                "Na te zijn vertrokken, belde hij zijn collega.",
                "Vertrekken vormt deze voltooide infinitief met zijn.",
            )
        ],
        related=["beknopte-bijzinnen", "perfectum", "passief-basis"],
    ),
    GrammarTopic(
        slug="uitloop-extrapositie",
        title="Een aanvulling na de werkwoordgroep",
        level="C1",
        category="Woordvolgorde",
        summary="Herken natuurlijke plaatsing buiten de werkwoordelijke eindgroep.",
        explanation="In bijzinnen staan de werkwoorden doorgaans laat, maar niet noodzakelijk als allerlaatste woorden. Een langere voorzetselgroep kan erna volgen: omdat zij lang heeft gesproken over de gevolgen voor de buurt. Ook omdat zij lang over de gevolgen voor de buurt heeft gesproken is mogelijk. De keuze beïnvloedt nadruk en verwerkingsgemak.\n\nNiet ieder zinsdeel kan zonder meer naar rechts worden verplaatst. Een persoonlijk voornaamwoord als lijdend voorwerp volgt andere patronen dan een zware bijzin. Leer extrapositie aan volledige voorbeelden en presenteer een gangbare uitloop niet als fout doordat het vereenvoudigde leermodel werkwoord achteraan zegt.",
        rules=[
            "Werkwoord achteraan is een basispatroon, geen verbod op iedere uitloop.",
            "Een zware voorzetselgroep kan na de werkwoordgroep staan.",
            "Beoordeel natuurlijkheid en betekenis binnen de volledige context.",
        ],
        examples=[
            GrammarExample("Ik weet dat zij heeft nagedacht over de gevolgen voor haar gezin."),
            GrammarExample("Hij zei dat hij blij was met de steun van zijn collega's."),
        ],
        common_mistakes=[],
        related=["werkwoordclusters", "focus-woordvolgorde", "tangconstructies"],
    ),
    GrammarTopic(
        slug="modale-partikels-wel-eens",
        title="Wel, eens en nou als gesprekssignalen",
        level="C1",
        category="Pragmatiek",
        summary="Onderscheid tijdsbetekenis van nadruk, geruststelling en aansporing.",
        explanation="Wel kan een tegenstelling markeren: Ik kom wel, maar niet om negen uur. In Dat komt wel goed kan het geruststelling geven. Eens kan een onbepaald moment noemen, maar in Kijk eens hier is het vaak een aansporend partikel. Nou kan een reactie voorbereiden, aarzeling tonen of ongeduld uitdrukken.\n\nDe woorden hebben dus geen vaste beleefdheidswaarde. Nou, dat weet ik niet kan een voorzichtig bezwaar inleiden; Kom nou! kan juist scherp klinken. Betrek intonatie, relatie en de voorafgaande beurt bij de interpretatie. Geef zonder die informatie ruimte aan meerdere lezingen.",
        rules=[
            "Bepaal of een woord tijd, contrast of gesprekshouding uitdrukt.",
            "Een partikel maakt een verzoek niet automatisch beleefd.",
            "Beoordeel nadruk samen met intonatie en beurtpositie.",
        ],
        examples=[
            GrammarExample("Nou, ik zie ook een paar praktische bezwaren."),
            GrammarExample("Kijk eens of dit tijdstip voor je past."),
        ],
        common_mistakes=[],
        related=["partikels-interactie", "bijwoorden-plaatsing"],
    ),
    GrammarTopic(
        slug="idiomatische-werkwoordverbindingen",
        title="Een besluit nemen en kritiek leveren",
        level="C1",
        category="Idiomatiek",
        summary="Gebruik vaste woordcombinaties en behoud hun grammaticale patroon.",
        explanation="Werkwoord en naamwoord vormen vaak een gebruikelijke combinatie: een besluit nemen, kritiek leveren, rekening houden met. De betekenis kan begrijpelijk zijn terwijl een letterlijke vertaling uit een andere taal toch onnatuurlijk klinkt. Leer daarom de combinatie inclusief voorzetsel, lidwoord en mogelijke vervoeging.\n\nSommige verbindingen laten variatie toe: een keuze maken en een keuze doen hebben niet overal dezelfde gangbaarheid. Een taalvariant vraagt een contextueel oordeel, geen automatische foutmarkering. In een nieuwe tekst kun je een eenvoudiger werkwoord gebruiken wanneer dat dezelfde betekenis en hetzelfde register bewaart: onderzoeken tegenover onderzoek doen naar.",
        rules=[
            "Leer de hele verbinding met haar vaste aanvullingen.",
            "Vervoeg het werkwoord zonder het idioom letterlijk uiteen te trekken.",
            "Maak onderscheid tussen fout, regionale variant en stijlvoorkeur.",
        ],
        examples=[
            GrammarExample("De commissie neemt morgen een besluit over de aanvraag."),
            GrammarExample("We houden rekening met de gevolgen voor kleine organisaties."),
        ],
        common_mistakes=[
            GrammarMistake(
                "We houden rekening op de planning.",
                "We houden rekening met de planning.",
                "De vaste verbinding is rekening houden met.",
            )
        ],
        related=["vaste-voorzetsels", "formeel-informeel"],
    ),
    GrammarTopic(
        slug="samengestelde-adjectieven",
        title="Veelbelovend, goed onderbouwd en langverwacht",
        level="C1",
        category="Woordvorming",
        summary="Onderscheid vaste samenstellingen van gewone woordgroepen.",
        explanation="Sommige combinaties functioneren als één bijvoeglijk naamwoord: veelbelovend, langverwacht. Andere blijven een woordgroep: goed onderbouwd, zorgvuldig gekozen. De spelling volgt niet één eenvoudige regel dat alles met een deelwoord aaneengeschreven wordt. Controleer onbekende vormen in een woordenlijst.\n\nBij verbuiging kan alleen het laatste deel veranderen: een goed onderbouwd advies, het goed onderbouwde advies. Houd betekenis en klemtoon in het oog. Een veelbelovend resultaat is niet hetzelfde als een bewezen effect. De woordvorming mag bij een samenvatting dus niet onbedoeld de zekerheid van de bron verhogen.",
        rules=[
            "Vaste samenstellingen en vrije woordgroepen hebben verschillende spelling.",
            "Een vrije bepaling zoals zorgvuldig blijft doorgaans los.",
            "Controleer verbuiging aan de hand van de volledige naamwoordgroep.",
        ],
        examples=[
            GrammarExample("Het goed onderbouwde advies overtuigde de commissie."),
            GrammarExample("De langverwachte publicatie bevat veelbelovende resultaten."),
        ],
        common_mistakes=[
            GrammarMistake(
                "het goed onderbouwd advies",
                "het goed onderbouwde advies",
                "Bij dit bepaalde enkelvoudige het-woord krijgt onderbouwd een -e.",
            )
        ],
        related=["deelwoord-bijvoeglijk", "woordvorming-samenstellingen"],
    ),
    GrammarTopic(
        slug="punctuatie-citaat",
        title="Citeren, parafraseren en leestekens",
        level="C1",
        category="Tekst",
        summary="Markeer letterlijk geciteerde woorden en houd bronstem en eigen stem gescheiden.",
        explanation="Aanhalingstekens kunnen een letterlijk citaat afbakenen: Zij zei: 'Ik kom morgen.' Een parafrase gebruikt je eigen formulering en mag niet als woordelijk citaat worden voorgesteld. Bij een ingebedde citaatzin hangt de plaats van een vraagteken af van wie de vraag stelt: vroeg de bron iets, of stel jij een vraag over haar woorden?\n\nUitgevers gebruiken verschillende conventies voor enkele of dubbele aanhalingstekens. Consistentie is belangrijker dan één universele huisstijl. Weglatingen en toevoegingen moeten herkenbaar blijven en mogen de strekking niet veranderen. Bewaar vooral ontkenning, voorwaarden en onzekerheidswoorden wanneer je een fragment selecteert.",
        rules=[
            "Onderscheid letterlijk citaat van eigen parafrase.",
            "Bepaal of het vraagteken bij het citaat of bij de omvattende zin hoort.",
            "Een huisstijlkeuze maakt een andere gangbare conventie niet grammaticaal fout.",
        ],
        examples=[
            GrammarExample("Zij vroeg: 'Wanneer begint de vergadering?'"),
            GrammarExample("Heeft zij werkelijk 'zonder voorwaarden' gezegd?"),
        ],
        common_mistakes=[],
        related=["indirecte-rede", "formeel-informeel"],
    ),
    GrammarTopic(
        slug="voornaamwoordelijke-verwijzing",
        title="Die, dat, hij, zij en een duidelijke referent",
        level="C1",
        category="Tekst",
        summary="Kies verwijzingen op basis van grammatica, betekenis en duidelijkheid.",
        explanation="Bij betrekkelijke verwijzing volg je doorgaans de grammaticale naamwoordklasse: het meisje dat, de persoon die. Bij persoonlijke verwijzing speelt ook de bedoelde persoon een rol: Het meisje kwam binnen. Zij droeg een rode jas. Dat zijn verschillende verwijssystemen, geen tegenstrijdige regels.\n\nVoor organisaties, abstracte begrippen en personen kunnen conventies en voorkeuren uiteenlopen. Gebruik de gewenste persoonsverwijzing als die bekend is en herhaal een naam of kernwoord wanneer een voornaamwoord dubbelzinnig wordt. Laat een redactionele keuze niet veranderen wie de handeling uitvoert. Een duidelijk antecedent gaat vóór het vermijden van elke herhaling.",
        rules=[
            "Onderscheid betrekkelijke van persoonlijke verwijzing.",
            "Maak bij meerdere mogelijke antecedenten de referent expliciet.",
            "Respecteer bekende persoonsverwijzingen en leg registerkeuzes uit.",
        ],
        examples=[
            GrammarExample("Het meisje dat de prijs won, vertelde dat zij verder wil studeren."),
            GrammarExample(
                "De redactie belde de onderzoeker. De onderzoeker lichtte de cijfers toe."
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                "Het rapport die gisteren verscheen bevat fouten.",
                "Het rapport dat gisteren verscheen bevat fouten.",
                "Rapport is hier een enkelvoudig het-woord.",
            )
        ],
        related=["betrekkelijk-die-dat", "verwijzing-cohesie"],
    ),
    GrammarTopic(
        slug="voorwaardelijke-inversie",
        title="Mocht dat gebeuren en had ik dat geweten",
        level="C1",
        category="Zinsbouw",
        summary="Herken een voorwaarde zonder als en behoud haar betekenis bij herformuleren.",
        explanation="Een voorwaardelijke zin kan zonder als beginnen met een persoonsvorm: Mocht de planning veranderen, dan hoort u dat. De betekenis is ongeveer als de planning verandert, met een voorzichtige of minder vanzelfsprekende voorstelling. Bij een onwerkelijk verleden: Had ik dat geweten, dan was ik eerder vertrokken.\n\nDe vorm lijkt op een vraag, maar introduceert hier een voorwaarde. Interpunctie en de volgende hoofdzin maken die functie zichtbaar. Een parafrase moet de tijd en het niet-gerealiseerde karakter behouden. Niet iedere werkwoord-eerstzin is voorwaardelijk: Neem plaats is bijvoorbeeld een instructie.",
        rules=[
            "Werkwoord-eerst kan in context een voorwaarde inleiden.",
            "Mocht maakt een mogelijke toekomstige situatie vaak voorzichtig.",
            "Had ik dat geweten verwijst naar een onwerkelijk eerder moment.",
        ],
        examples=[
            GrammarExample("Mocht u vragen hebben, dan kunt u ons bellen."),
            GrammarExample(
                "Had de commissie meer tijd gehad, dan had zij extra bronnen kunnen raadplegen."
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                "Mocht u vragen heeft, dan kunt u bellen.",
                "Mocht u vragen hebben, dan kunt u bellen.",
                "Na mocht staat de infinitief hebben.",
            )
        ],
        related=["voorwaarden-zou", "onwerkelijk-verleden"],
    ),
]
