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
]
