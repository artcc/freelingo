"""Dutch A1: sound, sentence structure and everyday interaction."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="klanken-spelling",
        title="Klanken, letters en klemtoon",
        level="A1",
        category="Uitspraak",
        summary="Herken korte en lange klinkers en spel je naam.",
        explanation="Luister naar het verschil tussen man en maan, bom en boom, en vis en vies. Een lange klinker staat vaak dubbel in een gesloten lettergreep: raam. In een open lettergreep is één letter genoeg: ramen. Na een korte klinker verdubbelt de medeklinker vaak: man, mannen. Dit is een basispatroon, geen regel voor ieder leenwoord.\n\nOe klinkt anders dan uu; eu en ui zijn verschillende klanken. Ei en ij klinken in het Standaardnederlands hetzelfde. De uitspraak van g en r verschilt binnen Nederland. Leer de klemtoon met het woord en vraag om herhaling.",
        rules=[
            "Vergelijk raam/ramen en man/mannen.",
            "Schrijf IJ aan het begin van een naam met twee hoofdletters: IJssel.",
            "Luister naar het hele woord; spelling voorspelt niet alle klanken.",
        ],
        examples=[
            GrammarExample("Mijn naam is Noor: N-O-O-R."),
            GrammarExample("Kunt u dat herhalen?"),
            GrammarExample("Een maan, twee manen; een man, twee mannen."),
        ],
        common_mistakes=[
            GrammarMistake("twee raamen", "twee ramen", "De lange a staat in een open lettergreep.")
        ],
        related=["lidwoorden-meervoud"],
    ),
    GrammarTopic(
        slug="voornaamwoorden-zijn",
        title="Ik ben, jij bent: personen en zijn",
        level="A1",
        category="Werkwoorden",
        summary="Stel jezelf voor en kies je of u.",
        explanation="Gebruik meestal een onderwerp: ik, jij/je, hij, zij/ze, het, wij/we, jullie, zij/ze. Zijn verandert: ik ben, jij bent, hij/zij/het is, wij/jullie/zij zijn. U bent is de gewone beleefde vorm. Je en u passen bij de relatie; niet iedere onbekende verwacht u.\n\nZij kan één vrouw of meerdere personen betekenen: zij is / zij zijn. De korte vormen je, ze en we hebben meestal geen nadruk. Bij een tegenstelling gebruik je bijvoorbeeld jij: Jij bent docent, ik ben student. Leeftijd krijgt zijn: Ik ben dertig jaar.",
        rules=[
            "Gebruik zijn voor naam, leeftijd, herkomst en toestand.",
            "Kies je of u passend bij de situatie.",
            "Bij jij na het werkwoord: ben jij, niet bent jij.",
        ],
        examples=[
            GrammarExample("Ik ben Sam. Ik ben dertig jaar."),
            GrammarExample("Wij zijn uit Utrecht."),
            GrammarExample("Bent u de docent?"),
        ],
        common_mistakes=[GrammarMistake("Ik is student.", "Ik ben student.", "Bij ik hoort ben.")],
        related=["vragen-inversie", "hebben"],
    ),
    GrammarTopic(
        slug="hebben",
        title="Hebben: bezit en dagelijkse behoeften",
        level="A1",
        category="Werkwoorden",
        summary="Vertel wat iemand heeft of nodig heeft.",
        explanation="De vormen zijn ik heb, jij hebt, hij/zij/het heeft en wij/jullie/zij hebben. Zowel u hebt als u heeft is correct. Met jij na het werkwoord verdwijnt de t: Heb jij tijd? Bij u blijft de vorm: Hebt u tijd?\n\nGebruik hebben voor bezit en in vaste combinaties: honger hebben, dorst hebben, tijd hebben en nodig hebben. Leeftijd krijgt zijn: Ik ben twintig jaar. Leer zulke combinaties als geheel, in plaats van ze letterlijk uit een andere taal te vertalen.",
        rules=[
            "Ik heb; jij hebt; zij heeft; we hebben.",
            "U hebt en u heeft zijn allebei correct.",
            "Gebruik zijn voor leeftijd.",
        ],
        examples=[
            GrammarExample("Ik heb een fiets."),
            GrammarExample("We hebben dorst."),
            GrammarExample("Heb je hulp nodig?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Wij heeft tijd.", "Wij hebben tijd.", "Een meervoudig onderwerp krijgt hebben."
            )
        ],
        related=["voornaamwoorden-zijn", "vragen-inversie"],
    ),
    GrammarTopic(
        slug="tegenwoordige-tijd",
        title="De tegenwoordige tijd en de tweede plaats",
        level="A1",
        category="Werkwoorden",
        summary="Beschrijf wat je doet en plaats het werkwoord correct.",
        explanation="Bij veel werkwoorden gebruik je de stam bij ik, stam + t bij jij/hij/zij en het hele werkwoord bij meervoud: ik werk, jij werkt, wij werken. Let op de spelling: wonen wordt ik woon; reizen wordt ik reis. Eindigt de stam op t, dan komt er geen extra t: hij zit.\n\nIn een gewone hoofdzin staat de persoonsvorm op de tweede zinsdeelplaats. Het eerste zinsdeel kan meerdere woorden bevatten: Iedere maandag werk ik thuis. Dit betekent niet dat het werkwoord altijd het tweede woord is.",
        rules=[
            "Ik werk; jij werkt; we werken.",
            "Een tijdsbepaling vooraan geeft inversie: Vandaag werk ik.",
            "Leer veelgebruikte onregelmatige vormen: ik ga, zij gaat; ik doe, zij doet.",
        ],
        examples=[
            GrammarExample("Ik woon in Leiden."),
            GrammarExample("Vandaag werken we thuis."),
            GrammarExample("Mijn buurman gaat naar school."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Vandaag ik werk thuis.",
                "Vandaag werk ik thuis.",
                "De persoonsvorm staat direct na het eerste zinsdeel.",
            )
        ],
        related=["vragen-inversie", "scheidbare-werkwoorden"],
    ),
    GrammarTopic(
        slug="lidwoorden-meervoud",
        title="De, het, een en het meervoud",
        level="A1",
        category="Naamwoorden",
        summary="Leer zelfstandige naamwoorden met hun lidwoord en meervoud.",
        explanation="Leer de fiets en het huis als een geheel. Het lidwoord is vaak niet uit de betekenis af te leiden. Een staat bij een niet-specifiek enkelvoud: een fiets, een huis. In het meervoud gebruik je de: de fietsen, de huizen. Een heeft geen meervoudsvorm: Ik koop appels.\n\nVeel meervouden eindigen op -en of -s: boeken, tafels. Let op klank en spelling: raam/ramen, bus/bussen, brief/brieven, foto/foto's. Leer onregelmatige vormen apart: kind/kinderen. Verkleinwoorden hebben in het enkelvoud het: het huisje.",
        rules=[
            "Leer bij elk nieuw naamwoord het lidwoord.",
            "Een meervoud met bepaald lidwoord krijgt de.",
            "Gebruik een apostrof waar nodig om de uitspraak te bewaren: auto's.",
        ],
        examples=[
            GrammarExample("De fiets staat bij het huis."),
            GrammarExample("Ik heb een boek en drie foto's."),
            GrammarExample("De kinderen lezen."),
        ],
        common_mistakes=[
            GrammarMistake("het boeken", "de boeken", "Het bepaalde lidwoord bij meervoud is de.")
        ],
        related=["klanken-spelling", "bijvoeglijke-naamwoorden"],
    ),
    GrammarTopic(
        slug="vragen-inversie",
        title="Vragen met en zonder vraagwoord",
        level="A1",
        category="Zinsbouw",
        summary="Vraag naar personen, plaatsen, tijden en redenen.",
        explanation="In een ja-neevraag komt de persoonsvorm voor het onderwerp: Woon je hier? Een vraagwoord komt meestal eerst: Waar woon je? Gebruik wie voor een persoon, wat voor iets, waar voor een plaats, wanneer voor een tijd en hoe voor een manier.\n\nStaat jij of je als onderwerp direct na de persoonsvorm, dan vervalt de t: Werk jij? Dat gebeurt niet bij u: Werkt u? In Werkt je broer hier? is je broer het onderwerp; je is daar een bezittelijk woord. Wie als onderwerp krijgt meestal enkelvoud: Wie woont hier?",
        rules=[
            "Maak een ja-neevraag met werkwoord + onderwerp.",
            "Gebruik vraagwoord + werkwoord + onderwerp als het vraagwoord niet zelf onderwerp is.",
            "Let op het verschil tussen werk je en werkt je broer.",
        ],
        examples=[
            GrammarExample("Waar woont je zus?"),
            GrammarExample("Hoe heet u?"),
            GrammarExample("Wie heeft een pen?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Waar jij woont?", "Waar woon jij?", "Dit is een directe vraag, geen bijzin."
            )
        ],
        related=["tegenwoordige-tijd", "voornaamwoorden-zijn"],
    ),
    GrammarTopic(
        slug="niet-geen",
        title="Ontkennen met niet en geen",
        level="A1",
        category="Ontkenning",
        summary="Zeg dat iets niet zo is of ontbreekt.",
        explanation="Geen ontkent vaak een naamwoord met een of zonder lidwoord: Ik heb een auto → Ik heb geen auto. Ik drink koffie → Ik drink geen koffie. Niet ontkent onder meer een eigenschap, bepaalde zaak of handeling: niet duur, niet mijn tas, Ik kom niet.\n\nDe plaats van niet hangt af van wat je ontkent. Het staat vóór een ontkende eigenschap of plaatsbepaling: Het is niet duur; Ik woon niet in Delft. Met een bepaald lijdend voorwerp: Ik koop het boek niet. Bij een infinitief aan het einde: Ik kan niet komen.",
        rules=[
            "Een fiets → geen fiets; koffie → geen koffie.",
            "De fiets en mijn fiets worden met niet ontkend.",
            "Plaats niet vóór de informatie die je uitdrukkelijk ontkent.",
        ],
        examples=[
            GrammarExample("Dit is niet mijn jas."),
            GrammarExample("We hebben geen kinderen."),
            GrammarExample("De winkel is niet open."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Het is geen duur.",
                "Het is niet duur.",
                "Duur is hier een bijvoeglijk naamwoord zonder zelfstandig naamwoord.",
            )
        ],
        related=["lidwoorden-meervoud", "modale-werkwoorden"],
    ),
    GrammarTopic(
        slug="bezit-aanwijzen",
        title="Mijn boek, deze tas en dat huis",
        level="A1",
        category="Voornaamwoorden",
        summary="Geef bezit aan en wijs iets aan.",
        explanation="Bezittelijke woorden zijn mijn, jouw/je, uw, zijn, haar, ons/onze, jullie en hun. Ons staat bij een enkelvoudig het-woord; onze bij de-woorden en meervoud: ons huis, onze fiets, onze huizen. Het woord verwijst naar de bezitter: haar boek is het boek van haar.\n\nBij enkelvoudige de-woorden en meervoud gebruik je deze/die. Bij enkelvoudige het-woorden gebruik je dit/dat: deze tafel, dat huis, die huizen. Deze/dit wijst vaak dichtbij, die/dat verder weg of terug naar iets dat al genoemd is.",
        rules=[
            "Ons huis, maar onze huizen.",
            "Deze/die fiets; dit/dat boek.",
            "Gebruik geen lidwoord vóór mijn, jouw of ons.",
        ],
        examples=[
            GrammarExample("Dit is mijn boek."),
            GrammarExample("Onze buren hebben een hond."),
            GrammarExample("Is die tas van jou?"),
        ],
        common_mistakes=[
            GrammarMistake("onze huis", "ons huis", "Huis is een enkelvoudig het-woord.")
        ],
        related=["lidwoorden-meervoud", "objectvormen"],
    ),
    GrammarTopic(
        slug="bijvoeglijke-naamwoorden",
        title="Een mooi huis en de mooie huizen",
        level="A1",
        category="Bijvoeglijke naamwoorden",
        summary="Beschrijf personen en dingen met de juiste uitgang.",
        explanation="Voor een naamwoord krijgt een bijvoeglijk naamwoord meestal -e: de kleine tas, het kleine huis, kleine huizen. Bij een onbepaald enkelvoudig het-woord ontbreekt die -e meestal: een klein huis, geen groot probleem. Bij een de-woord blijft -e: een kleine tas.\n\nNa zijn blijft het bijvoeglijk naamwoord meestal onveranderd: Het huis is klein; De huizen zijn klein. Let op spelling: groot/grote en wit/witte. Leer uitzonderingen, zoals vaste combinaties, later in hun context.",
        rules=[
            "De mooie fiets; het mooie huis.",
            "Een mooie fiets, maar een mooi huis.",
            "Na zijn: de fietsen zijn mooi.",
        ],
        examples=[
            GrammarExample("Ik draag een witte jas."),
            GrammarExample("Dat is een oud gebouw."),
            GrammarExample("Het gebouw is oud."),
        ],
        common_mistakes=[
            GrammarMistake(
                "De huizen zijn grote.",
                "De huizen zijn groot.",
                "Een predicatief gebruikt adjectief na zijn krijgt hier geen -e.",
            )
        ],
        related=["lidwoorden-meervoud", "bezit-aanwijzen"],
    ),
    GrammarTopic(
        slug="tijd-getallen",
        title="Getallen, dagen en de klok",
        level="A1",
        category="Tijd",
        summary="Spreek een tijd af en begrijp prijzen en data.",
        explanation="Vanaf eenentwintig staat de eenheid vóór het tiental: tweeëntwintig, vijfendertig. In prijzen gebruik je een komma: € 2,50 is twee euro vijftig. Dagen en maanden krijgen normaal een kleine letter.\n\nHalf drie betekent 14.30 of 2.30: een halfuur vóór drie. Kwart over twee is 2.15; kwart voor drie is 2.45. Geef bij afspraken zo nodig ochtend of middag aan, of gebruik de 24-uursnotatie. Gebruik om bij een kloktijd, op bij een dag en in bij een maand: om negen uur, op maandag, in mei.",
        rules=[
            "Half acht is 7.30, niet 8.30.",
            "Om tien uur; op dinsdag; in juni.",
            "Schrijf dagen en maanden met een kleine letter.",
        ],
        examples=[
            GrammarExample("De afspraak is om half drie."),
            GrammarExample("Het kost twee euro vijftig."),
            GrammarExample("Ik kom op vrijdag."),
        ],
        common_mistakes=[
            GrammarMistake("op negen uur", "om negen uur", "Gebruik om vóór een kloktijd.")
        ],
        related=["tegenwoordige-tijd", "plaats-richting"],
    ),
    GrammarTopic(
        slug="modale-werkwoorden",
        title="Kunnen, moeten, mogen en willen",
        level="A1",
        category="Werkwoorden",
        summary="Praat over mogelijkheden, wensen en regels.",
        explanation="Een modaal werkwoord krijgt een infinitief zonder te: Ik kan zwemmen; We moeten werken. De persoonsvorm staat op de tweede plaats; de infinitief meestal achteraan. Kunnen gaat over vaardigheid of mogelijkheid, moeten over noodzaak, mogen over toestemming en willen over een wens.\n\nLeer frequente vormen: ik kan, jij kunt/kan, hij kan; ik moet, wij moeten; ik mag, wij mogen; ik wil, hij wil, wij willen. Niet mogen betekent een verbod. Niet hoeven betekent dat iets niet nodig is; die combinatie leer je bij te + infinitief.",
        rules=[
            "Gebruik een infinitief zonder te na deze modale werkwoorden.",
            "Jij kan en jij kunt zijn beide mogelijk.",
            "Hij wil heeft geen t.",
        ],
        examples=[
            GrammarExample("Mag ik hier zitten?"),
            GrammarExample("Ik wil een kaartje kopen."),
            GrammarExample("We kunnen morgen komen."),
        ],
        common_mistakes=[
            GrammarMistake("Ik kan te zwemmen.", "Ik kan zwemmen.", "Kunnen krijgt hier geen te.")
        ],
        related=["tegenwoordige-tijd", "niet-geen"],
    ),
    GrammarTopic(
        slug="scheidbare-werkwoorden",
        title="Opstaan, meenemen en aankomen",
        level="A1",
        category="Werkwoorden",
        summary="Gebruik veelvoorkomende scheidbare werkwoorden.",
        explanation="Sommige werkwoorden bestaan uit een beklemtoond eerste deel en een werkwoord: opstaan, meenemen, aankomen. In een hoofdzin met dit werkwoord als persoonsvorm staat het eerste deel meestal achteraan: Ik sta om zeven uur op.\n\nNa een modaal werkwoord blijft de infinitief heel: Ik moet vroeg opstaan. Niet ieder werkwoord met een beginstuk is scheidbaar: begrijpen blijft bij elkaar. Leer scheidbaarheid en klemtoon met het werkwoord. Gebruik eenvoudige routines om het patroon te oefenen.",
        rules=[
            "Ik sta op; jij neemt mee; de trein komt aan.",
            "Met moeten: ik moet opstaan.",
            "Houd de betekenis van het hele werkwoord bij elkaar.",
        ],
        examples=[
            GrammarExample("Neem je een jas mee?"),
            GrammarExample("De bus komt om acht uur aan."),
            GrammarExample("Wij willen morgen uitslapen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik opsta vroeg.", "Ik sta vroeg op.", "In deze hoofdzin wordt opstaan gescheiden."
            )
        ],
        related=["tegenwoordige-tijd", "modale-werkwoorden"],
    ),
    GrammarTopic(
        slug="plaats-richting",
        title="In, op, bij en naar",
        level="A1",
        category="Voorzetsels",
        summary="Zeg waar iets is en waar je naartoe gaat.",
        explanation="Gebruik in voor een ruimte of plaats, op voor een oppervlak en bij voor nabijheid of aanwezigheid: in de kamer, op tafel, bij de dokter. Naar geeft vaak een bestemming aan: naar school, naar Amsterdam. Thuis is een plaats; naar huis is een richting.\n\nLeren waar een voorwerp ligt, staat of hangt helpt om natuurlijk te beschrijven: Het boek ligt op tafel; De fles staat op tafel; De jas hangt aan de kapstok. De keuze hangt af van positie en voorwerp; is kan in veel contexten ook, maar geeft minder informatie.",
        rules=[
            "Ik ben thuis; ik ga naar huis.",
            "Gebruik naast, tussen en tegenover voor eenvoudige plaatsbeschrijvingen.",
            "Leer vaste combinaties zoals op school en bij de huisarts.",
        ],
        examples=[
            GrammarExample("De apotheek is naast de supermarkt."),
            GrammarExample("De sleutels liggen op tafel."),
            GrammarExample("We gaan met de trein naar Utrecht."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik ga naar thuis.",
                "Ik ga naar huis.",
                "De vaste combinatie voor de richting is naar huis.",
            )
        ],
        related=["er-plaats", "tijd-getallen"],
    ),
    GrammarTopic(
        slug="objectvormen",
        title="Mij, jou, hem en haar",
        level="A1",
        category="Voornaamwoorden",
        summary="Verwijs naar personen die niet het onderwerp zijn.",
        explanation="Gebruik ik, jij en wij als onderwerp, maar mij/me, jou/je en ons als voorwerp of na een voorzetsel: Zij ziet mij; Dit is voor jou; Hij komt met ons. Andere vormen zijn hem, haar, het, jullie en hen/hun/ze. De precieze geschreven verdeling van hen en hun volgt later.\n\nMe en je zijn onbeklemtoonde vormen. Mij en jou passen bij nadruk: niet voor mij, maar voor jou. U kan zowel onderwerp als voorwerp zijn: Ik help u. Verwar jou niet met jouw: voor jou, maar jouw fiets.",
        rules=[
            "Ik zie hem; hij ziet mij.",
            "Na voor, met en bij gebruik je geen ik of jij.",
            "Jou verwijst zelfstandig; jouw staat bij een bezit.",
        ],
        examples=[
            GrammarExample("Kunt u mij helpen?"),
            GrammarExample("Ik bel je morgen."),
            GrammarExample("Zij gaat met ons mee."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Dit is voor ik.", "Dit is voor mij.", "Na voor gebruik je de objectvorm."
            )
        ],
        related=["voornaamwoorden-zijn", "bezit-aanwijzen"],
    ),
    GrammarTopic(
        slug="er-plaats",
        title="Er is, er zijn en daar",
        level="A1",
        category="Zinsbouw",
        summary="Vertel wat ergens aanwezig is.",
        explanation="Met er is en er zijn introduceer je iets: Er is een bank in deze straat; Er zijn twee winkels. Het werkwoord volgt het aantal: een bank is enkelvoud, twee winkels is meervoud. Daarna kun je naar die bekende zaak verwijzen: De bank is naast het station.\n\nEr kan ook een bekende plaats vervangen: Woon je in Delft? Ja, ik woon er. Daar kan meer nadruk krijgen of iets aanwijzen: Daar is het station. Er heeft nog andere functies; oefen hier alleen aanwezigheid en plaats.",
        rules=[
            "Er is één winkel; er zijn twee winkels.",
            "Introduceer iets nieuws met er en beschrijf het daarna nader.",
            "Gebruik daar als je een plaats nadrukkelijk aanwijst.",
        ],
        examples=[
            GrammarExample("Er is geen lift."),
            GrammarExample("Er zijn drie kamers."),
            GrammarExample("Is er een toilet?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Er is twee winkels.",
                "Er zijn twee winkels.",
                "Twee winkels vraagt een meervoudige persoonsvorm.",
            )
        ],
        related=["plaats-richting", "lidwoorden-meervoud"],
    ),
    GrammarTopic(
        slug="en-maar-want",
        title="Zinnen verbinden met en, maar en want",
        level="A1",
        category="Verbindingen",
        summary="Voeg informatie, een tegenstelling of een reden toe.",
        explanation="En voegt iets toe, maar geeft een tegenstelling en want geeft een reden: Ik blijf thuis, want ik ben moe. Na deze woorden blijft de gewone hoofdzinvolgorde staan. Vergelijk Ik ben moe en Vandaag ben ik moe: een ander eerste zinsdeel geeft nog steeds inversie.\n\nAls het onderwerp hetzelfde is, kun je het soms weglaten: Ik werk en studeer. Begin met korte volledige zinnen en verbind ze tot een begrijpelijk bericht. Want en omdat hebben een verwante betekenis, maar omdat krijgt bijzinvolgorde; dat volgt op A2.",
        rules=[
            "En, maar en want veranderen op zichzelf de woordvolgorde niet.",
            "Gebruik maar voor een echte tegenstelling.",
            "Geef met want een reden voor je uitspraak.",
        ],
        examples=[
            GrammarExample("Ik fiets, maar mijn broer loopt."),
            GrammarExample("We blijven thuis, want het regent."),
            GrammarExample("Ik werk vandaag en morgen ben ik vrij."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik blijf thuis, want ik moe ben.",
                "Ik blijf thuis, want ik ben moe.",
                "Na want staat hier een hoofdzin.",
            )
        ],
        related=["tegenwoordige-tijd", "niet-geen"],
    ),
]
