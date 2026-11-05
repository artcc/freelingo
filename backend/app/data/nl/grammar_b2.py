"""Dutch B2: argumentation, complex clauses and precision."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="werkwoordclusters",
        title="Werkwoordgroepen en de vervangende infinitief",
        level="B2",
        category="Zinsbouw",
        summary="Gebruik meerdere werkwoorden zonder geldige volgordes uit te sluiten.",
        explanation="Bij twee werkwoorden in een bijzin zijn vaak twee volgordes mogelijk: dat zij heeft gewerkt en dat zij gewerkt heeft. Bij grotere groepen gelden specifiekere patronen. In Ik heb moeten werken staat moeten als infinitief in plaats van een voltooid deelwoord; dit heet de vervangende infinitief.\n\nGebruik als productief model: omdat ik heb moeten werken en omdat ik wil kunnen blijven. Leer clusters per constructie. Verklaar niet dat alle volgordes uitwisselbaar zijn of dat iedere regionale variant fout is. De betekenis bepaalt welk werkwoord bij welk ander werkwoord hoort.",
        rules=[
            "Heb moeten werken, niet heb gemoeten werken in deze constructie.",
            "Tweeledige clusters kunnen meer dan één standaardvolgorde hebben.",
            "Controleer de hiërarchie: willen kunnen is niet kunnen willen.",
        ],
        examples=[
            GrammarExample("Ze zegt dat ze heeft moeten overwerken."),
            GrammarExample("Ik heb hem zien vertrekken."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik heb gemoeten werken.",
                "Ik heb moeten werken.",
                "Moeten krijgt hier de vervangende infinitief.",
            )
        ],
        related=["perfectum", "omdat-dat"],
    ),
    GrammarTopic(
        slug="onwerkelijk-verleden",
        title="Een andere afloop in het verleden",
        level="B2",
        category="Modaliteit",
        summary="Bespreek gemiste mogelijkheden zonder ze als feiten te presenteren.",
        explanation="Een onwerkelijke voorwaarde over het verleden gebruikt vaak had/was + deelwoord: Als ik eerder was vertrokken, had ik de trein gehaald. Ook zou hebben gehaald is mogelijk. De zin presenteert een denkbeeldig alternatief, geen werkelijk behaalde trein.\n\nMaak onderscheid tussen spijt, verwijt en neutrale analyse. Had ik maar eerder gebeld drukt spijt uit. Je had moeten bellen kan als verwijt klinken. Behoud bij een herformulering wat vaststaat en wat verondersteld wordt; verander een voorwaarde niet in een bewezen oorzaak.",
        rules=[
            "Eerdere niet-gerealiseerde voorwaarde: als ik had/was ...",
            "Had gehaald en zou hebben gehaald kunnen beide passen.",
            "Stem de toon af op verantwoordelijkheid en onzekerheid.",
        ],
        examples=[
            GrammarExample("Als zij was gebleven, hadden we verder kunnen praten."),
            GrammarExample("Had ik maar beter geluisterd."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Als ik eerder had vertrokken, had ik de trein gehaald.",
                "Als ik eerder was vertrokken, had ik de trein gehaald.",
                "Vertrekken krijgt zijn als hulpwerkwoord.",
            )
        ],
        related=["voorwaarden-zou", "verhaaltijden"],
    ),
    GrammarTopic(
        slug="concessie-voorwaarden",
        title="Hoewel, tenzij en mits",
        level="B2",
        category="Verbindingen",
        summary="Formuleer beperkingen en voorwaarden nauwkeurig.",
        explanation="Hoewel geeft een tegenstelling die het resultaat niet verhindert. Zelfs als beschrijft een uiterste voorwaarde: Zelfs als het regent, gaat het feest door. Tenzij betekent behalve als; mits betekent op voorwaarde dat. Ze zijn geen synoniemen.\n\nJe mag deelnemen mits je je inschrijft stelt inschrijving als voorwaarde. Je mag deelnemen tenzij de groep vol is noemt een uitzondering. Pas op met niet na tenzij: dat kan de bedoelde voorwaarde omkeren. Controleer de logica door de zin met als te herformuleren.",
        rules=[
            "Mits geeft een vereiste; tenzij een uitzondering.",
            "Hoewel en zelfs als drukken niet dezelfde zekerheid uit.",
            "Controleer ontkenning binnen de voorwaarde.",
        ],
        examples=[
            GrammarExample("We gaan door tenzij de veiligheid in gevaar komt."),
            GrammarExample("U krijgt toegang mits u zich legitimeert."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Hoewel het regent, maar gaan we door.",
                "Hoewel het regent, gaan we door.",
                "In dit standaardpatroon staat geen extra maar voor de hoofdzin.",
            )
        ],
        related=["verbindingswoorden", "voorwaarden-zou"],
    ),
    GrammarTopic(
        slug="passief-onpersoonlijk",
        title="Er wordt gewerkt en er zijn afspraken gemaakt",
        level="B2",
        category="Zinsbouw",
        summary="Beschrijf processen en beoordeel of de uitvoerder zichtbaar moet zijn.",
        explanation="Een onpersoonlijk passief heeft geen gewoon naamwoordelijk onderwerp: Er wordt hier gewerkt. Bij een meervoudig onderwerp volgt de persoonsvorm het aantal: Er worden afspraken gemaakt. In het perfectum: Er is gewerkt; Er zijn afspraken gemaakt.\n\nEen passief kan nuttig zijn in procesbeschrijvingen, maar ook verantwoordelijkheid verbergen. Vergelijk Er zijn fouten gemaakt met De afdeling heeft de aanvragen verkeerd verwerkt. Voeg alleen een uitvoerder toe als de bron die werkelijk noemt. Het grammaticale onderwerp van een passieve zin is niet automatisch de handelende persoon.",
        rules=[
            "Zonder naamwoordelijk onderwerp: er wordt/is gewerkt.",
            "Met meervoudig onderwerp: er worden/zijn afspraken gemaakt.",
            "Behoud broninformatie over de uitvoerder.",
        ],
        examples=[
            GrammarExample("Er wordt aan een oplossing gewerkt."),
            GrammarExample("Er zijn drie bezwaren ingediend."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Er wordt drie bezwaren ingediend.",
                "Er worden drie bezwaren ingediend.",
                "Drie bezwaren is meervoud.",
            )
        ],
        related=["passief-basis", "er-plaats"],
    ),
    GrammarTopic(
        slug="focus-woordvolgorde",
        title="Bekende informatie, nieuwe informatie en nadruk",
        level="B2",
        category="Tekst",
        summary="Orden zinnen op basis van samenhang en contrast.",
        explanation="Het eerste zinsdeel kan een onderwerp, tijd, plaats of voorwerp zijn. De persoonsvorm blijft in een gewone hoofdzin op de tweede zinsdeelplaats: Dat voorstel steun ik. Vooropplaatsing maakt een onderwerp of contrast zichtbaar; het verandert niet vanzelf wie de handeling uitvoert.\n\nBekende informatie komt vaak eerder dan nieuwe informatie, maar nadruk en context kunnen dat patroon veranderen. Alleen verschuift de betekenis afhankelijk van de plaats: Alleen Noor heeft gebeld tegenover Noor heeft alleen gebeld. Maak bij dubbelzinnigheid de bedoelde beperking expliciet.",
        rules=[
            "Vooropplaatsing verandert de grammaticale rollen niet automatisch.",
            "Controleer het bereik van alleen en ook.",
            "Gebruik nadruk om een echt contrast te markeren.",
        ],
        examples=[
            GrammarExample("Dat boek heb ik al gelezen."),
            GrammarExample("Alleen de voorzitter mag stemmen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Dat voorstel ik steun.",
                "Dat voorstel steun ik.",
                "De persoonsvorm volgt het vooropgeplaatste voorwerp.",
            )
        ],
        related=["tegenwoordige-tijd", "onbepaalde-woorden"],
    ),
    GrammarTopic(
        slug="men-er-je",
        title="Men, je en onpersoonlijk er",
        level="B2",
        category="Register",
        summary="Kies een algemene formulering die bij tekst en publiek past.",
        explanation="Men verwijst algemeen naar mensen en klinkt vaak formeel: Men verwacht vertraging. Je kan in algemene uitspraken staan zonder specifiek de lezer aan te spreken: In Nederland kun je vaak met de fiets reizen. Dat past niet bij elke zakelijke tekst.\n\nEen onpersoonlijk er kan de gebeurtenis centraal zetten: Er wordt vertraging verwacht. Deze varianten zijn niet altijd inhoudelijk gelijk: De directie verwacht vertraging noemt een specifieke bron. Laat bij herformuleren niet onbedoeld een bron verdwijnen of een algemene uitspraak veranderen in persoonlijk advies.",
        rules=[
            "Men krijgt enkelvoud.",
            "Algemeen je is niet altijd letterlijk de aangesprokene.",
            "Behoud een relevante bron of verantwoordelijke partij.",
        ],
        examples=[
            GrammarExample("Men verwacht morgen meer duidelijkheid."),
            GrammarExample("Er wordt nog onderhandeld."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Men verwachten vertraging.",
                "Men verwacht vertraging.",
                "Men vraagt een enkelvoudige persoonsvorm.",
            )
        ],
        related=["passief-onpersoonlijk", "passief-basis"],
    ),
    GrammarTopic(
        slug="hen-hun-register",
        title="Hen, hun en ze in context",
        level="B2",
        category="Voornaamwoorden",
        summary="Pas de geschreven hen/hun-regel toe zonder spreektaal te veroordelen.",
        explanation="De traditionele schrijfregel gebruikt hen als lijdend voorwerp en na een voorzetsel, en hun als meewerkend voorwerp zonder voorzetsel: Ik zie hen; Ik geef hun het boek; Ik geef het boek aan hen. Ze is vaak een natuurlijke onbeklemtoonde vorm: Ik geef ze het boek.\n\nIn de praktijk is hen/hun niet bij ieder werkwoord eenduidig: mailen kan verschillende grammaticale constructies hebben. Gebruik zulke gevallen niet als toets met één antwoord zonder extra context. Hun als onderwerp, zoals Hun hebben het gedaan, hoort niet bij de standaardtaal; zij en ze wel.",
        rules=[
            "Na een voorzetsel: aan hen, met hen.",
            "Hun kan ook bezit aangeven: hun huis.",
            "Ze kan onbeklemtoond naar personen verwijzen.",
        ],
        examples=[
            GrammarExample("Ik heb met hen gesproken."),
            GrammarExample("Ik geef hun een kans."),
            GrammarExample("Zij hebben hun werk af."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Hun hebben het verslag geschreven.",
                "Zij hebben het verslag geschreven.",
                "In de standaardtaal is hun geen onderwerp.",
            )
        ],
        related=["objectvormen", "bezit-aanwijzen"],
    ),
    GrammarTopic(
        slug="nominalisatie",
        title="Van werkwoord naar naamwoord",
        level="B2",
        category="Tekst",
        summary="Gebruik naamwoordstijl doelgericht en herschrijf onduidelijke zinnen.",
        explanation="Een handeling kan als naamwoord verschijnen: het beoordelen van aanvragen, de beoordeling van aanvragen. Dat helpt om naar een proces als geheel te verwijzen. Te veel nominalisaties kunnen echter verbergen wie wat doet.\n\nVergelijk De uitvoering van de controle vindt plaats met De inspecteur controleert de installatie. De tweede zin is alleen een trouwe herformulering als de inspecteur werkelijk de uitvoerder is en de installatie het juiste object. Voeg geen verzonnen deelnemers toe om een zin actiever te maken. Kies compactheid of expliciete rollen op basis van tekstdoel.",
        rules=[
            "Een zelfstandig gebruikte infinitief krijgt het.",
            "Controleer wie handelt bij het terugvormen naar een werkwoord.",
            "Behoud tijd, modaliteit en ontkenning.",
        ],
        examples=[
            GrammarExample("Het beoordelen van de aanvragen kost tijd."),
            GrammarExample("De commissie beoordeelt de aanvragen morgen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Het beoordelen van de aanvragen kosten tijd.",
                "Het beoordelen van de aanvragen kost tijd.",
                "Het onderwerp is het enkelvoudige beoordelen, niet aanvragen.",
            )
        ],
        related=["passief-basis", "focus-woordvolgorde"],
    ),
    GrammarTopic(
        slug="deelwoord-bijvoeglijk",
        title="Een verraste reiziger en een verrassend bericht",
        level="B2",
        category="Woordvorming",
        summary="Onderscheid een toestand van een eigenschap die iets veroorzaakt.",
        explanation="Een voltooid deelwoord kan bijvoeglijk gebruikt worden: een gesloten deur, een verraste reiziger. Een tegenwoordig deelwoord op -end kan een lopende handeling of kenmerk aangeven: een wachtende reiziger, een verrassend bericht.\n\nLet op de rollen: een geïnteresseerde lezer toont belangstelling; een interessant boek wekt belangstelling. De woordvorm alleen vertelt niet alles over tijd of oorzaak. Verbogen deelwoorden volgen hun spellingpatroon: de vergrote foto, de verbrande brief, de geredde kat. Leer het verschil tussen een persoonsvorm en een bijvoeglijke vorm: hij vergrootte tegenover de vergrote foto.",
        rules=[
            "Een toestand: verbaasd; een effect veroorzakend: verbazend.",
            "Bijvoeglijke vormen krijgen alleen noodzakelijke spellingverdubbeling.",
            "Behoud wie iets ervaart en wat het veroorzaakt.",
        ],
        examples=[
            GrammarExample("De verraste bezoekers lazen het verrassende nieuws."),
            GrammarExample("De geredde hond slaapt."),
        ],
        common_mistakes=[
            GrammarMistake(
                "de vergrootte foto",
                "de vergrote foto",
                "Hier staat een bijvoeglijke vorm, geen verleden persoonsvorm.",
            )
        ],
        related=["voltooid-deelwoord", "bijvoeglijke-naamwoorden"],
    ),
    GrammarTopic(
        slug="samengestelde-zinnen",
        title="Verbanden en verwijzingen in langere zinnen",
        level="B2",
        category="Tekst",
        summary="Schrijf complexe zinnen die de lezer kan volgen.",
        explanation="Een langere zin kan meerdere bijzinnen bevatten, maar elke verwijzing moet duidelijk blijven. Zet een betrekkelijke bijzin zo dicht mogelijk bij het naamwoord dat hij beschrijft. Vermijd dat die, dat of hij naar twee mogelijke personen verwijst.\n\nEen komma kan extra informatie afbakenen: De medewerkers, die een training hadden gevolgd, hielpen de bezoekers. Zonder komma kan de bijzin een groep beperken: De medewerkers die een training hadden gevolgd hielpen de bezoekers. De context moet de bedoelde groep ondersteunen; voeg geen komma toe als daarmee de inhoud verandert.",
        rules=[
            "Maak het antecedent van elk verwijswoord duidelijk.",
            "Een beperkende bijzin selecteert; een uitbreidende geeft extra informatie.",
            "Splits een zin als meerdere inbeddingen de rollen onduidelijk maken.",
        ],
        examples=[
            GrammarExample("De deelnemers die zich hebben aangemeld krijgen een bericht."),
            GrammarExample("Noor, die de bijeenkomst organiseert, stuurt de uitnodiging."),
        ],
        common_mistakes=[
            GrammarMistake(
                "De deelnemers die zich heeft aangemeld komen morgen.",
                "De deelnemers die zich hebben aangemeld komen morgen.",
                "Die verwijst naar het meervoud deelnemers.",
            )
        ],
        related=["betrekkelijk-die-dat", "betrekkelijk-voorzetsel"],
    ),
]
