"""Swedish A2: connected narration, descriptions and subordinate clauses."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "sv-preterite-a2",
        "Preteritum i berättelser",
        "A2",
        "Verb",
        "Berätta om något vid en avslutad tidpunkt.",
        "Regelbundna verb har olika preteritumändelser: tala – talade, ringa – ringde, köpa – köpte, bo – bodde. Starka verb kan ändra vokal: skriva – skrev. Lär infinitiv, presens och preteritum tillsammans. Preteritum fungerar även utan ett tidsord när en dåtida ram redan är tydlig.",
        rules=[
            "Efter igår används normalt preteritum om det som hände då.",
            "Dåtid har samma verbform för alla personer.",
        ],
        examples=[
            GrammarExample("Vi köpte biljetter igår."),
            GrammarExample("Hon ringde och berättade om resan."),
        ],
        related=["sv-past-basics"],
    ),
    GrammarTopic(
        "sv-perfect-a2",
        "Har och supinum",
        "A2",
        "Verb",
        "Knyt en tidigare händelse till nuet.",
        "Perfekt bildas med har och supinum: har talat, har köpt, har bott, har skrivit. Tiden är ofta inte avslutad eller inte preciserad: Jag har varit i Umeå. Preteritum anger i stället en avslutad dåtida ram: Jag var där i juni. Skillnaden handlar om perspektiv, inte om hur länge en handling varade.",
        rules=[
            "Efter har behövs supinum, inte preteritum.",
            "Jag har bott här i två år betyder normalt att jag fortfarande bor här.",
        ],
        examples=[GrammarExample("Har du ätit?"), GrammarExample("Jag har redan köpt biljetten.")],
        common_mistakes=[
            GrammarMistake("Jag har skrev.", "Jag har skrivit.", "Har följs av supinum.")
        ],
    ),
    GrammarTopic(
        "sv-future-a2",
        "Ska, kommer att och presens",
        "A2",
        "Verb",
        "Prata om planer och förväntningar.",
        "Ska används ofta om en plan eller avsikt. Kommer att används ofta om en förutsägelse. Presens kan uttrycka framtid när tiden är tydlig: Tåget går imorgon. Former kan överlappa; de är inte alltid rätt eller fel utan sammanhang. I samtal utelämnas att ibland efter kommer.",
        rules=[
            "Ska följs av infinitiv utan att.",
            "Välj framtidsform efter vad du vill säga om planering och förväntan.",
        ],
        examples=[
            GrammarExample("Jag ska ringa vårdcentralen."),
            GrammarExample("Det kommer att ta tid."),
            GrammarExample("Vi ses på fredag."),
        ],
    ),
    GrammarTopic(
        "sv-adjective-definite-a2",
        "Den röda jackan",
        "A2",
        "Adjektiv",
        "Beskriv en bestämd sak.",
        "I ett vanligt bestämt uttryck med adjektiv används den, det eller de, adjektivets a-form och substantivets bestämda form: den röda jackan. Efter possessiv används a-form men obestämt substantiv: min röda jacka. Det finns fasta namn och särskilda uttryck med andra mönster.",
        rules=[
            "Ett rött hus blir det röda huset.",
            "Min röda jacka har ingen extra bestämd artikel.",
        ],
        examples=[
            GrammarExample("De nya skorna är sköna."),
            GrammarExample("Var är mitt gröna kort?"),
        ],
        related=["sv-adjectives", "sv-possessives"],
    ),
    GrammarTopic(
        "sv-comparison-a2",
        "Större, mindre och lika stor",
        "A2",
        "Adjektiv",
        "Jämför egenskaper hos två saker.",
        "Många adjektiv får -are och -ast: billig, billigare, billigast. Vanliga oregelbundna former är bra – bättre – bäst och stor – större – störst. Mindre är komparativ av liten. Använd än efter komparativ och lika … som för likhet.",
        rules=[
            "Dyrare än uttrycker skillnad; lika dyr som uttrycker samma grad.",
            "Alla adjektiv får inte -are: mer intressant är ett vanligt mönster.",
        ],
        examples=[
            GrammarExample("Bussen är billigare än taxin."),
            GrammarExample("Mitt rum är lika stort som ditt."),
        ],
    ),
    GrammarTopic(
        "sv-adverbs-a2",
        "Snabb och snabbt",
        "A2",
        "Adjektiv och adverb",
        "Skilj mellan egenskaper och hur något görs.",
        "Adjektiv beskriver substantiv: en snabb cyklist. Adverb kan beskriva verb: Hon cyklar snabbt. Många adverb får -t, men det finns andra former som bra, fort och gärna. Samma form kan vara ett adjektiv med ett-genus eller ett adverb; funktionen i meningen avgör.",
        rules=[
            "Ett snabbt tåg innehåller ett adjektiv.",
            "Tåget går snabbt innehåller ett adverb.",
        ],
        examples=[
            GrammarExample("Han talar tydligt."),
            GrammarExample("Hon är glad och skrattar glatt."),
        ],
    ),
    GrammarTopic(
        "sv-subclauses-a2",
        "Att, eftersom och när",
        "A2",
        "Ordföljd",
        "Bygg en bisats med subjekt före verb.",
        "En bisats kan börja med att, eftersom eller när. I en neutral bisats står subjektet före det böjda verbet: eftersom jag arbetar. Ett satsadverb som inte står före det böjda verbet: eftersom jag inte arbetar. Jämför huvudsatsen Jag arbetar inte.",
        rules=[
            "Bisats: inledare + subjekt + inte + böjt verb.",
            "En orsak med eftersom behöver ett tydligt samband med huvudsatsen.",
        ],
        examples=[
            GrammarExample("Jag stannar hemma eftersom jag är sjuk."),
            GrammarExample("Hon säger att hon inte kan komma."),
        ],
        common_mistakes=[
            GrammarMistake(
                "eftersom jag kan inte komma",
                "eftersom jag inte kan komma",
                "Inte står före det böjda verbet i denna bisats.",
            )
        ],
    ),
    GrammarTopic(
        "sv-initial-subclause-a2",
        "När jag kommer hem, lagar jag mat",
        "A2",
        "Ordföljd",
        "Sätt en hel bisats först i meningen.",
        "En inledande bisats räknas som första satsdel i huvudsatsen. Huvudsatsens böjda verb kommer därför direkt efter bisatsen: När jag kommer hem lagar jag mat. Komma kan användas för tydlighet, särskilt efter en längre bisats, men behövs inte mekaniskt efter varje kort bisats.",
        rules=[
            "Bisatsens egen ordföljd ändras inte när den står först.",
            "Efter den inledande bisatsen kommer huvudsatsens verb före subjektet.",
        ],
        examples=[
            GrammarExample("Eftersom jag inte har bil tar jag bussen."),
            GrammarExample("När det regnar stannar vi inne."),
        ],
        related=["sv-subclauses-a2", "sv-v2"],
    ),
    GrammarTopic(
        "sv-reflexive-a2",
        "Tvätta sig och känna sig",
        "A2",
        "Pronomen",
        "Låt handlingen syfta tillbaka på subjektet.",
        "Reflexiva uttryck använder mig med jag, dig med du, oss med vi, er med ni och sig med han, hon, hen, den, det eller de. I Jag tvättar mig är subjekt och objekt samma person. Känna sig används om ett tillstånd: Jag känner mig trött.",
        rules=[
            "Sig används i tredje person, inte efter jag eller du.",
            "Lär reflexiva verb som uttryck: skynda sig, sätta sig.",
        ],
        examples=[
            GrammarExample("Barnen klär på sig."),
            GrammarExample("Vi känner oss bättre idag."),
        ],
    ),
    GrammarTopic(
        "sv-reflexive-possessive-a2",
        "Sin, sitt och sina",
        "A2",
        "Pronomen",
        "Visa att något tillhör subjektet i samma sats.",
        "Sin, sitt och sina syftar normalt tillbaka på ett subjekt i tredje person i samma sats: Sara tar sin väska. Saras egen väska avses. Sara tar hennes väska syftar normalt på en annan kvinnas väska. Formen beror på det som ägs, inte ägaren. I subjektet används inte sin: Hennes väska är röd.",
        rules=[
            "Sin bok, sitt barn, sina böcker.",
            "Jag och du använder min respektive din, inte sin.",
        ],
        examples=[GrammarExample("Ali hämtar sina barn."), GrammarExample("De säljer sitt hus.")],
        related=["sv-possessives"],
    ),
    GrammarTopic(
        "sv-relative-a2",
        "Personen som bor här",
        "A2",
        "Bisatser",
        "Beskriv vem eller vad du menar.",
        "Som kan inleda en relativ bisats efter ett substantiv: en person som arbetar här. När som är subjekt behövs inget extra han eller hon. När som är objekt har bisatsen ett annat subjekt: boken som jag läser. Som kan då ofta utelämnas, men inte när det är subjekt.",
        rules=[
            "Relativsatsen beskriver ordet eller gruppen före som.",
            "Även här står inte före det böjda verbet i neutral bisatsordföljd.",
        ],
        examples=[
            GrammarExample("Jag söker en lägenhet som inte är så dyr."),
            GrammarExample("Filmen som vi såg var bra."),
        ],
    ),
    GrammarTopic(
        "sv-indirect-question-a2",
        "Jag undrar var bussen stannar",
        "A2",
        "Bisatser",
        "Bädda in en fråga i ett påstående eller en artig fråga.",
        "En indirekt fråga har bisatsordföljd: Vet du var bussen stannar? En ja-nej-fråga inleds med om: Jag undrar om hon kommer. När frågeordet är subjekt lägger man normalt till som: Vet du vem som kommer?",
        rules=[
            "Direkt: Var bor du? Indirekt: Jag undrar var du bor.",
            "Om betyder här en fråga med ja eller nej som möjligt svar.",
        ],
        examples=[
            GrammarExample("Vet du när tåget går?"),
            GrammarExample("Kan du säga vem som arbetar idag?"),
        ],
    ),
    GrammarTopic(
        "sv-particles-a2",
        "Sätta på och stänga av",
        "A2",
        "Verb",
        "Lär vanliga partikelverb som hela uttryck.",
        "En betonad partikel kan ändra verbets betydelse: sätta på radion, stänga av lampan, gå upp. Lär uttrycket tillsammans med betydelse och betoning. I många partikelverb står objektet efter partikeln: Sätt på den. Alla verb följda av en preposition är inte partikelverb.",
        rules=[
            "Partikeln är ofta betonad.",
            "Sätt på radion och sätt dig på stolen har olika konstruktioner.",
        ],
        examples=[
            GrammarExample("Jag går upp klockan sju."),
            GrammarExample("Kan du stänga av den?"),
        ],
    ),
    GrammarTopic(
        "sv-duration-a2",
        "I två timmar, för två dagar sedan",
        "A2",
        "Tid",
        "Skilj mellan varaktighet och tidpunkt.",
        "I två timmar anger hur länge något pågår eller pågick. För två dagar sedan anger en tidigare tidpunkt. Om två dagar anger tid från nu till något framtida. På två timmar kan ange tiden som behövs för att slutföra något: Jag läste boken på två timmar.",
        rules=[
            "Välj tidsuttryck efter frågan: hur länge, när eller hur lång tid det tar.",
            "Sedan i måndags anger en startpunkt med fortsatt relevans.",
        ],
        examples=[
            GrammarExample("Jag har väntat i en timme."),
            GrammarExample("Vi åker om tre dagar."),
            GrammarExample("Hon kom för en vecka sedan."),
        ],
    ),
    GrammarTopic(
        "sv-indefinites-a2",
        "Någon, något och några",
        "A2",
        "Pronomen",
        "Tala om personer och saker utan att precisera dem.",
        "Någon används med en-ord eller om en person, något med ett-ord eller om en ospecificerad sak och några med plural. Ingen, inget och inga uttrycker frånvaro. I enkla meningar behövs inte också inte: Jag har inga pengar. Med sammansatt verb används ofta inte några: Jag har inte köpt några biljetter.",
        rules=[
            "Har du någon fråga? Har du något förslag?",
            "Ingen kommer betyder att noll personer kommer.",
        ],
        examples=[
            GrammarExample("Jag behöver något att dricka."),
            GrammarExample("Det finns inga lediga rum."),
        ],
    ),
    GrammarTopic(
        "sv-infinitive-a2",
        "Att läsa och börja läsa",
        "A2",
        "Verb",
        "Använd infinitiv efter vanliga uttryck.",
        "En infinitivfras med att kan beteckna en aktivitet: Att läsa är roligt. Efter vill, kan och ska används inget att. Efter andra verb varierar mönstret: försöka att förstå och försöka förstå är båda möjliga. Lär verbens konstruktioner i exempel i stället för att sätta att före varje infinitiv.",
        rules=["Det är roligt att läsa har att.", "Jag vill läsa har inte att."],
        examples=[
            GrammarExample("Jag lär mig att simma."),
            GrammarExample("Hon börjar arbeta klockan nio."),
        ],
    ),
    GrammarTopic(
        "sv-genitive-a2",
        "Saras cykel och husets dörr",
        "A2",
        "Substantiv",
        "Uttryck ägande och andra relationer med s.",
        "Genitiv bildas ofta med s direkt på ordet utan apostrof: Saras cykel, husets dörr. Substantivet efter genitiven står normalt i obestämd form. Namn som redan slutar på s får normalt inget ytterligare s: Lars cykel. En omskrivning kan göra relationen tydligare.",
        rules=[
            "Svensk genitiv använder normalt inte engelsk apostrof.",
            "Saras nya cykel har adjektivets a-form.",
        ],
        examples=[
            GrammarExample("Det är lärarens bok."),
            GrammarExample("Vi står vid husets dörr."),
        ],
    ),
    GrammarTopic(
        "sv-superlative-a2",
        "Den bästa vägen",
        "A2",
        "Adjektiv",
        "Välj ett alternativ ur en grupp.",
        "Superlativ jämför med en hel grupp: snabbast, billigast, bäst. Före ett bestämt substantiv används ofta en längre form: den snabbaste vägen, det bästa alternativet. Efter verb kan den obestämda formen användas: Den här vägen är snabbast.",
        rules=[
            "Bra blir bäst och den bästa.",
            "Jämförelsegruppen behöver vara tydlig i sammanhanget.",
        ],
        examples=[
            GrammarExample("Vilken biljett är billigast?"),
            GrammarExample("Vi tar den kortaste vägen."),
        ],
        related=["sv-comparison-a2"],
    ),
    GrammarTopic(
        "sv-polite-requests-a2",
        "Skulle du kunna hjälpa mig?",
        "A2",
        "Samspel",
        "Be om något utan att låta som en order.",
        "Skulle kunna och skulle vilja kan mjuka upp frågor och önskemål: Skulle du kunna hjälpa mig? Här behöver skulle inte betyda förfluten tid. Tack, ursäkta och en tydlig fråga bidrar till vänligt tilltal. Du är vanligt också i kontakt med personal och myndigheter.",
        rules=[
            "Skulle du kunna följs av infinitiv.",
            "En längre formulering är inte automatiskt vänligare; anpassa tonen till situationen.",
        ],
        examples=[
            GrammarExample("Jag skulle vilja boka en tid."),
            GrammarExample("Ursäkta, kan du visa mig vägen?"),
        ],
    ),
    GrammarTopic(
        "sv-condition-a2",
        "Om det regnar tar vi bussen",
        "A2",
        "Samband",
        "Beskriv ett öppet villkor.",
        "Om kan uttrycka ett möjligt villkor. Presens används ofta både i villkoret och om den framtida följden: Om det regnar tar vi bussen. Det betyder inte att det redan regnar. En inledande om-sats följs av huvudsatsens böjda verb.",
        rules=[
            "Skilj villkors-om från om i en indirekt ja-nej-fråga.",
            "Sätt inte före verbet i om-satsen: Om du inte kan komma …",
        ],
        examples=[
            GrammarExample("Om jag hinner ringer jag ikväll."),
            GrammarExample("Vi går ut om det inte regnar."),
        ],
        related=["sv-initial-subclause-a2"],
    ),
    GrammarTopic(
        "sv-short-answers-a2",
        "Ja, det gör jag och jo",
        "A2",
        "Samspel",
        "Svara kort och tydligt på frågor.",
        "I kortsvar återanvänds ofta hjälpverbet: Kan du simma? Ja, det kan jag. Med ett vanligt huvudverb används göra: Arbetar du här? Ja, det gör jag. Jo används för att säga emot ett negativt antagande: Kommer du inte? Jo, jag kommer.",
        rules=[
            "Nej bekräftar ofta den negativa situationen: Nej, jag kan inte.",
            "Lägg till en hel sats om ett kort svar kan missförstås.",
        ],
        examples=[
            GrammarExample("Har du ätit? Ja, det har jag."),
            GrammarExample("Är du inte klar? Jo, jag är klar."),
        ],
    ),
    GrammarTopic(
        "sv-compounds-a2",
        "Skriv sammansatta ord tillsammans",
        "A2",
        "Ordbildning",
        "Förstå ord som busshållplats och tvättstuga.",
        "Svenska bildar många nya ord genom sammansättning: buss + hållplats blir busshållplats. Delarna skrivs normalt ihop, och den sista delen bestämmer genus: en hållplats – en busshållplats. Betoningen hjälper oss att höra skillnaden mellan en sammansättning och två fristående ord. I vissa ord finns en fogebokstav, till exempel s i arbetsdag; lär hela ordet när formen inte är självklar.",
        rules=[
            "Dela inte automatiskt upp svenska sammansättningar efter ett annat språks stavning.",
            "Ett sammansatt ord kan behöva bindestreck i särskilda fall, till exempel vid siffror: 20-åring.",
        ],
        examples=[
            GrammarExample("Bussen stannar vid busshållplatsen."),
            GrammarExample("Vi bokar tvättstugan på måndag."),
        ],
        common_mistakes=[
            GrammarMistake(
                "buss hållplats",
                "busshållplats",
                "En plats där bussen stannar benämns här med ett sammansatt ord.",
            )
        ],
    ),
    GrammarTopic(
        "sv-ordinals-a2",
        "Datum, ordning och våningar",
        "A2",
        "Tid och antal",
        "Skilj antal från plats i en ordning.",
        "Grundtal anger antal: tre böcker. Ordningstal anger plats: den tredje boken. Vanliga ordningstal är första, andra, tredje, fjärde, femte, sjätte, sjunde, åttonde, nionde, tionde, elfte och tolfte. Datum läses med ordningstal: den femte maj, den tjugoförsta juni. Månadsnamn har liten bokstav. I siffror kan datum skrivas 5 maj; följ det format som efterfrågas i ett formulär.",
        rules=[
            "Tre våningar är ett antal; tredje våningen är en bestämd plats.",
            "För årtal och telefonnummer: läs tydligt och kontrollera siffrorna vid behov.",
        ],
        examples=[
            GrammarExample("Jag bor på tredje våningen."),
            GrammarExample("Mötet är den tjugoförsta juni."),
        ],
    ),
]
