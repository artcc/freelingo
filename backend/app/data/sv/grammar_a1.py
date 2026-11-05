"""Swedish A1: sound, sentence structure and everyday communication."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "sv-alphabet",
        "Alfabetet och å, ä, ö",
        "A1",
        "Uttal och skrift",
        "Läs och stava namn och korta ord.",
        "Svenska har 29 bokstäver. Å, ä och ö är egna bokstäver efter z i alfabetet, inte varianter av a och o. Stor bokstav används i namn och i början av en mening. Språk, veckodagar och månader skrivs normalt med liten bokstav.",
        rules=[
            "Behåll å, ä och ö när du skriver: år, är, ö.",
            "Lyssna på bokstavsnamnen när du övar att stava.",
        ],
        examples=[GrammarExample("Jag heter Åsa."), GrammarExample("Jag läser svenska på måndag.")],
        common_mistakes=[
            GrammarMistake(
                "Jag läser Svenska.", "Jag läser svenska.", "Språknamn har liten bokstav."
            )
        ],
        related=["sv-length"],
    ),
    GrammarTopic(
        "sv-length",
        "Långa och korta ljud",
        "A1",
        "Uttal och skrift",
        "Hör skillnaden mellan till exempel tak och tack.",
        "I en betonad stavelse följs en lång vokal normalt av en kort konsonant och en kort vokal av en lång konsonant eller flera konsonanter. Vokalens klang kan också ändras. Dubbel konsonant är en viktig ledtråd: tak och tack. Stavningen är inte en fullständig uttalsregel: vanliga ord som en, men och som behöver läras med ljud. Svenskans ordmelodi varierar regionalt; lyssna och härma hela ord och fraser.",
        rules=[
            "Öva vokal och konsonant tillsammans, inte bara vokalen.",
            "Å, ä och ö har både långa och korta uttal.",
        ],
        examples=[GrammarExample("Ett tak. Tack!"), GrammarExample("En glass. Ett glas.")],
        related=["sv-alphabet"],
    ),
    GrammarTopic(
        "sv-subject-present",
        "Jag är, du heter, vi bor",
        "A1",
        "Verb och pronomen",
        "Använd subjekt och presens för att presentera dig.",
        "Personliga subjekt är jag, du, han, hon, hen, den, det, vi, ni och de. Hen används bland annat när könet är okänt eller när personen använder det pronomenet. Presens har samma form för alla personer: jag bor, vi bor. Lär infinitiv och presens tillsammans: arbeta–arbetar, läsa–läser, bo–bor. Vanliga oregelbundna former är vara–är, ha–har, göra–gör och gå–går. Presens beskriver bland annat det som händer nu och vanor. Svenska påståenden behöver normalt ett subjekt.",
        rules=[
            "Lär infinitiv och presens tillsammans: bo – bor, heta – heter, vara – är.",
            "Du är normalt tilltal till en person; ni används till flera och är inte automatiskt artigare till en person.",
        ],
        examples=[
            GrammarExample("Jag är lärare."),
            GrammarExample("Vi bor i Malmö."),
            GrammarExample("Vad heter du?"),
        ],
        common_mistakes=[
            GrammarMistake("Jag vara lärare.", "Jag är lärare.", "Här behövs presensformen är.")
        ],
    ),
    GrammarTopic(
        "sv-noun-gender",
        "En bok och ett bord",
        "A1",
        "Substantiv",
        "Lär substantiv tillsammans med en eller ett.",
        "Substantiv har en-genus eller ett-genus: en bok, ett bord. Genus går inte alltid att gissa. Obestämd form används när vi introducerar en sak: Jag har en bok. Vid yrke utan beskrivande tillägg saknas artikeln ofta: Hon är läkare.",
        rules=[
            "Spara nya substantiv med en eller ett.",
            "En och ett kan också betyda antalet ett.",
        ],
        examples=[GrammarExample("Det är en stol."), GrammarExample("Jag har ett barn.")],
        common_mistakes=[GrammarMistake("ett bok", "en bok", "Bok är ett en-ord.")],
        related=["sv-definite", "sv-plural"],
    ),
    GrammarTopic(
        "sv-definite",
        "Boken och bordet",
        "A1",
        "Substantiv",
        "Använd bestämd form för något känt.",
        "När lyssnaren vet vilken sak du menar använder du ofta bestämd form. Ändelsen fogas till substantivet: en bok – boken, en flicka – flickan, ett bord – bordet, ett äpple – äpplet. Välj form efter betydelsen i sammanhanget, inte efter en direkt översättning från ett annat språk.",
        rules=[
            "En-ord får ofta -en eller -n; ett-ord ofta -et eller -t.",
            "Lär hela formen när stavningen ändras.",
        ],
        examples=[
            GrammarExample("Jag har en bok. Boken är bra."),
            GrammarExample("Här är ett äpple. Äpplet är grönt."),
        ],
        related=["sv-noun-gender"],
    ),
    GrammarTopic(
        "sv-plural",
        "En stol, två stolar",
        "A1",
        "Substantiv",
        "Känn igen vanliga pluralformer.",
        "Svenska har flera pluralmönster: en flicka – flickor, en stol – stolar, en bild – bilder, ett äpple – äpplen och ett hus – hus. Det finns också oregelbundna former: en bok – böcker, en man – män. Lär pluralformen med ordet; en enda ändelse fungerar inte för alla substantiv.\n\nBestämd plural används om kända saker: flickorna, stolarna, bilderna, äpplena, husen. Många pluralord på -or, -ar och -er får -na. Ett-ord som äpple får äpplen–äpplena och ett-ord utan pluraländelse får ofta -en: hus–husen, barn–barnen. Lär hela ordserien: en bok, boken, böcker, böckerna.",
        rules=[
            "Efter två och andra antal över ett används plural.",
            "Många ett-ord som slutar på konsonant har samma obestämda form i singular och plural.",
        ],
        examples=[GrammarExample("Vi har två stolar."), GrammarExample("Här finns tre hus.")],
        common_mistakes=[GrammarMistake("två bok", "två böcker", "Bok har pluralformen böcker.")],
        related=["sv-noun-gender"],
    ),
    GrammarTopic(
        "sv-v2",
        "Verbet på andra plats",
        "A1",
        "Ordföljd",
        "Börja ett påstående med person, tid eller plats.",
        "I en vanlig påståendesats står det böjda verbet som andra satsdel. Första satsdelen kan innehålla flera ord: På måndag arbetar jag. När tiden står först kommer subjektet efter verbet. Regeln gäller satsdelar, inte antalet skrivna ord.",
        rules=[
            "Jag arbetar idag. Idag arbetar jag.",
            "Börja med det du vill knyta an till och behåll verbets plats.",
        ],
        examples=[
            GrammarExample("På morgonen dricker jag te."),
            GrammarExample("Hemma talar vi svenska."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Idag jag arbetar.",
                "Idag arbetar jag.",
                "Tidsuttrycket står först; verbet kommer före subjektet.",
            )
        ],
    ),
    GrammarTopic(
        "sv-questions",
        "Frågor med och utan frågeord",
        "A1",
        "Ordföljd",
        "Fråga om personer, platser och vardagliga fakta.",
        "En ja-nej-fråga börjar normalt med det böjda verbet: Bor du här? Med frågeord kommer frågeledet först: Var bor du? Vanliga frågeord är vad, vem, var, vart, när och hur. När vem är subjekt står inget extra subjekt efter verbet: Vem kommer?",
        rules=[
            "Var frågar om plats; vart frågar om riktning.",
            "Hur gammal är du? frågar om ålder.",
        ],
        examples=[
            GrammarExample("När börjar lektionen?"),
            GrammarExample("Är du trött?"),
            GrammarExample("Vem bor här?"),
        ],
        related=["sv-v2"],
    ),
    GrammarTopic(
        "sv-negation",
        "Inte i enkla huvudsatser",
        "A1",
        "Ordföljd",
        "Säg att något inte stämmer.",
        "I en enkel huvudsats med subjektet först står inte efter det böjda verbet: Jag arbetar inte. Med hjälpverb står inte mellan hjälpverbet och infinitiven: Jag kan inte komma. I en neutral fråga står inte efter subjektet: Kommer du inte? Placeringen i bisatser lär du dig senare.",
        rules=[
            "Negera hela påståendet med inte.",
            "Lär mönstret jag är inte, jag har inte, jag kan inte.",
        ],
        examples=[
            GrammarExample("Jag dricker inte kaffe."),
            GrammarExample("Vi kan inte komma idag."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Jag inte bor här.", "Jag bor inte här.", "I denna huvudsats står inte efter bor."
            )
        ],
        related=["sv-v2", "sv-modals"],
    ),
    GrammarTopic(
        "sv-modals",
        "Kan, vill, ska och måste",
        "A1",
        "Verb",
        "Uttryck förmåga, önskemål, planer och behov.",
        "Efter kan, vill, ska och måste används infinitiv utan att: Jag kan simma. Kan uttrycker bland annat förmåga och möjlighet; vill uttrycker önskan. Ska används bland annat om planer och måste om nödvändighet. Inte måste betyder att något inte är nödvändigt, inte att det är förbjudet.",
        rules=[
            "Skriv vill äta, inte vill att äta.",
            "Måste inte och får inte betyder olika saker.",
        ],
        examples=[
            GrammarExample("Jag vill ha vatten."),
            GrammarExample("Vi ska resa imorgon."),
            GrammarExample("Du måste inte följa med."),
        ],
    ),
    GrammarTopic(
        "sv-objects",
        "Mig, dig och andra objektsformer",
        "A1",
        "Pronomen",
        "Skilj mellan den som gör något och den som berörs.",
        "Objektsformer är mig, dig, honom, henne, hen, den, det, oss, er och dem. Använd dem efter ett verb eller en preposition när pronomenet är objekt: Hon ser mig. Jag väntar på dig. De och dem uttalas ofta dom; i neutral standardskrift skiljer man på de som subjekt och dem som objekt.",
        rules=["Jag ser henne. Hon ser mig.", "Efter till kan du säga till oss eller till dem."],
        examples=[GrammarExample("Kan du hjälpa mig?"), GrammarExample("Vi väntar på er.")],
    ),
    GrammarTopic(
        "sv-possessives",
        "Min, mitt, mina",
        "A1",
        "Pronomen",
        "Visa vem något tillhör.",
        "Min, din, vår och er böjs efter det som ägs: min bok, mitt hus, mina böcker. Hans, hennes, hens och deras böjs inte. Efter ett possessivt pronomen står substantivet i obestämd form. Jämför boken och min bok.",
        rules=[
            "Lär min–mitt–mina och din–ditt–dina tillsammans.",
            "Hans hus kan vara ett hus eller flera; sammanhanget visar antalet.",
        ],
        examples=[GrammarExample("Det är mitt rum."), GrammarExample("Här är våra väskor.")],
        common_mistakes=[
            GrammarMistake("min boken", "min bok", "Possessivet följs här av obestämd form.")
        ],
    ),
    GrammarTopic(
        "sv-adjectives",
        "En grön stol, ett grönt bord",
        "A1",
        "Adjektiv",
        "Beskriv personer och saker med rätt adjektivform.",
        "Vanliga adjektiv får -t med ett-ord och -a i plural: grön, grönt, gröna. Samma skillnad finns efter är: Bordet är grönt. Vissa adjektiv följer andra mönster, till exempel bra som inte böjs. Lär vanliga avvikelser som stor – stort – stora.",
        rules=[
            "Adjektivet följer substantivets genus och antal.",
            "Plural används också om flera personer: Vi är trötta.",
        ],
        examples=[GrammarExample("En röd bil. Ett rött hus."), GrammarExample("Bilarna är röda.")],
        related=["sv-noun-gender", "sv-plural"],
    ),
    GrammarTopic(
        "sv-place-direction",
        "Här och hit, där och dit",
        "A1",
        "Plats och riktning",
        "Skilj mellan var något finns och vart någon går.",
        "Här och där anger plats. Hit och dit anger riktning. Samma mönster finns i hemma–hem, inne–in och ute–ut. Prepositioner lärs med vanliga uttryck: i Sverige, på jobbet, till skolan. De kan inte alltid översättas ord för ord.",
        rules=["Jag är hemma. Jag går hem.", "Till anger ofta ett mål; i och på kan ange plats."],
        examples=[
            GrammarExample("Kom hit!"),
            GrammarExample("Nyckeln ligger på bordet."),
            GrammarExample("Hon går till skolan."),
        ],
    ),
    GrammarTopic(
        "sv-existential",
        "Det är och det finns",
        "A1",
        "Satsmönster",
        "Presentera något och tala om vad som finns.",
        "Det är används för att identifiera eller beskriva: Det är min syster. Det finns säger att något existerar eller är tillgängligt på en plats: Det finns ett apotek här. Det fungerar som inledande subjekt även när flera saker följer.",
        rules=[
            "Använd det finns både med singular och plural.",
            "Det är kallt beskriver vädret utan ett personligt subjekt.",
        ],
        examples=[
            GrammarExample("Det finns två stolar i köket."),
            GrammarExample("Det är min lärare."),
            GrammarExample("Det är kallt idag."),
        ],
    ),
    GrammarTopic(
        "sv-time",
        "Klockan, dagar och tider",
        "A1",
        "Tid och antal",
        "Förstå vanliga tider och boka en enkel träff.",
        "Halv åtta betyder 7.30, alltså en halvtimme före åtta. Kvart över åtta är 8.15 och kvart i åtta är 7.45. Använd på måndag om en kommande måndag och på måndagar om en vana. Idag, imorgon och igår anger tid i förhållande till nu.",
        rules=[
            "Klockan åtta anger tidpunkten.",
            "Ett tidsuttryck först i en huvudsats följs av verbet.",
        ],
        examples=[
            GrammarExample("Vi ses klockan halv åtta."),
            GrammarExample("På måndagar arbetar jag hemma."),
        ],
        related=["sv-v2"],
    ),
    GrammarTopic(
        "sv-coordination",
        "Och, men och eller",
        "A1",
        "Samband",
        "Koppla ihop ord och enkla påståenden.",
        "Och lägger till information, men visar en kontrast och eller presenterar alternativ. Du kan koppla ihop ord eller hela huvudsatser. När subjektet är samma kan det ofta utelämnas i den andra delen: Jag äter och dricker.",
        rules=[
            "Men byter inte plats på subjekt och verb i en vanlig följande huvudsats.",
            "Eller används när du erbjuder ett val.",
        ],
        examples=[
            GrammarExample("Jag vill komma, men jag arbetar."),
            GrammarExample("Vill du ha te eller kaffe?"),
        ],
    ),
    GrammarTopic(
        "sv-imperative",
        "Lyssna, läs och kom",
        "A1",
        "Verb",
        "Förstå korta instruktioner och be om hjälp.",
        "Imperativ används i instruktioner och uppmaningar. Vanliga former är lyssna, läs, skriv, kom och var. Lär formen med verbet: läsa – läser – läs. Subjektet du står normalt inte med. Tonfall och situation avgör hur en uppmaning uppfattas; en fråga med kan du är ofta mjukare.",
        rules=[
            "Sätt inte efter imperativen när du avråder: Vänta inte.",
            "Var är imperativ av vara: Var försiktig.",
        ],
        examples=[
            GrammarExample("Läs texten."),
            GrammarExample("Kan du öppna dörren?"),
            GrammarExample("Kom in!"),
        ],
    ),
    GrammarTopic(
        "sv-demonstratives",
        "Den här boken och det där huset",
        "A1",
        "Pronomen",
        "Peka ut en viss sak.",
        "Den här används med en-ord, det här med ett-ord och de här med plural. Substantivet står i bestämd form: den här boken, det här huset, de här böckerna. Där används på samma sätt för att peka ut något längre bort eller något som redan nämnts.",
        rules=[
            "Hela uttrycket anpassas till substantivet.",
            "Det här är en bok presenterar en sak; den här boken pekar ut en bestämd bok.",
        ],
        examples=[
            GrammarExample("Jag vill ha den här jackan."),
            GrammarExample("De där skorna är fina."),
        ],
        related=["sv-definite", "sv-plural"],
    ),
    GrammarTopic(
        "sv-quantity",
        "Mycket, många och lite",
        "A1",
        "Tid och antal",
        "Uttryck mängd och antal i vardagen.",
        "Många används med sådant vi räknar i plural: många böcker. Mycket används bland annat med ämnen och abstrakta mängder: mycket vatten, mycket tid. Lite anger en liten mängd och några ett mindre antal: lite mjölk, några äpplen.",
        rules=[
            "Använd hur många med plural och hur mycket med mängd eller pris.",
            "Ett glas vatten anger en avgränsad mängd.",
        ],
        examples=[
            GrammarExample("Hur många barn har du?"),
            GrammarExample("Jag vill ha lite mjölk."),
            GrammarExample("Hur mycket kostar det?"),
        ],
    ),
    GrammarTopic(
        "sv-past-basics",
        "Igår var jag hemma",
        "A1",
        "Verb",
        "Berätta kort om en avslutad dag.",
        "Preteritum används om en avslutad tid, till exempel igår. Börja med vanliga former: är – var, har – hade, går – gick, gör – gjorde och arbetar – arbetade. Formen är samma för alla personer. Lär oregelbundna former som hela ord; byt inte bara ut sista bokstaven.",
        rules=[
            "Även i dåtid gäller verbets andra plats i påståenden.",
            "Inte står efter det böjda verbet när subjektet står först.",
        ],
        examples=[
            GrammarExample("Igår arbetade jag hemma."),
            GrammarExample("Vi var inte trötta."),
            GrammarExample("Jag hade en ledig dag."),
        ],
        related=["sv-v2", "sv-negation"],
    ),
    GrammarTopic(
        "sv-vowel-quality",
        "Vokalerna i, y och u",
        "A1",
        "Uttal och skrift",
        "Lyssna efter både klang och längd hos vokalerna.",
        "Vokalbokstäverna är a, e, i, o, u, y, å, ä och ö. De står inte alltid för samma ljud som i ditt första språk. Y uttalas med rundade läppar och är en vokal: ny, fyra. Även u har ett eget rundat uttal som behöver övas med ljud: du, hus. Lyssna på par som sil–syl och ful–fylld för att höra hur både klang och längd kan skilja ord åt. Bokstaven o kan låta olika i olika ord, till exempel sol och som; lär uttalet med ordet.",
        rules=[
            "Öva att lyssna, härma och jämföra med en ljudmodell.",
            "Byt inte å mot o eller ä mot a i skrift för att förenkla uttalet.",
        ],
        examples=[
            GrammarExample("Du bor i ett hus."),
            GrammarExample("Fyra nya stolar."),
            GrammarExample("En sil. En syl."),
        ],
        related=["sv-alphabet", "sv-length"],
    ),
    GrammarTopic(
        "sv-consonant-sounds",
        "Sj-ljud, tj-ljud och mjuka konsonanter",
        "A1",
        "Uttal och skrift",
        "Känn igen vanliga ljud som kan stavas på flera sätt.",
        "Sj-ljudet hörs i sjö, sju och skina. Liknande stavningar behöver inte ha samma ljud: skola börjar med s och k, medan skina börjar med sj-ljud. Tj-ljudet hörs i tjugo och köra. K och g får ofta ett mjukare uttal före e, i, y, ä och ö: köra, ge. Det finns undantag, särskilt i lånord, så lyssna på varje nytt ord. Sj-ljudets uttal varierar regionalt; målet är begriplighet, inte att alla låter likadant.",
        rules=[
            "Lär ljudet tillsammans med hela ordet.",
            "Sj och tj skiljer ofta ord åt och behöver lyssningsövning.",
        ],
        examples=[
            GrammarExample("Sju personer ser en sjö."),
            GrammarExample("Jag kan köra till skolan."),
            GrammarExample("Tjugo kronor, tack."),
        ],
        related=["sv-alphabet", "sv-vowel-quality"],
    ),
]
