"""Swedish B1: narrative perspective, agency and connected argument."""

from app.data._types import GrammarExample, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "sv-pluperfect-b1",
        "Hade gjort före något annat",
        "B1",
        "Verb",
        "Ordna två händelser i dåtid.",
        "Pluskvamperfekt bildas med hade och supinum. Det placerar en händelse före en annan dåtida utgångspunkt: När jag kom hade tåget gått. Preteritum för berättelsen vidare, medan pluskvamperfekt kan ge bakgrund. Man behöver inte använda pluskvamperfekt för varje tidigare händelse om tidsföljden redan är tydlig.",
        rules=["Hade följs av supinum.", "Visa vilken dåtida tidpunkt du utgår från."],
        examples=[
            GrammarExample("Jag var hungrig eftersom jag inte hade ätit."),
            GrammarExample("Hon hade redan ringt när jag kom."),
        ],
    ),
    GrammarTopic(
        "sv-narrative-time-b1",
        "Bakgrund och händelseförlopp",
        "B1",
        "Text och tid",
        "Håll ihop en berättelses tidslinje.",
        "Preteritum kan uttrycka både bakgrund och enskilda händelser: Det regnade när vi gick ut. Svenskan kräver ingen särskild pågående verbform här. Först, sedan, medan och till slut hjälper läsaren att följa händelserna. Byt tempus med ett syfte, inte mekaniskt när en mening börjar.",
        rules=[
            "Medan uttrycker ofta samtidighet.",
            "Markera ett hopp bakåt med till exempel tidigare eller hade.",
        ],
        examples=[
            GrammarExample("Medan vi väntade började det snöa."),
            GrammarExample("Först åt vi. Sedan gick vi hem."),
        ],
        related=["sv-pluperfect-b1"],
    ),
    GrammarTopic(
        "sv-used-to-b1",
        "Brukar och brukade",
        "B1",
        "Verb",
        "Beskriv vanor nu och tidigare.",
        "Brukar följs av infinitiv och beskriver något återkommande: Jag brukar cykla. Brukade beskriver en tidigare vana, ofta i kontrast till nu. En enstaka händelse behöver preteritum utan brukade. Brukar säger något om vanlighet men inte att det sker varje gång.",
        rules=[
            "Efter brukar och brukade används infinitiv utan att.",
            "Skilj vana från något som pågår just nu.",
        ],
        examples=[
            GrammarExample("Vi brukar fika efter mötet."),
            GrammarExample("Förr brukade jag ta bilen, men nu cyklar jag."),
        ],
    ),
    GrammarTopic(
        "sv-passive-b1",
        "Dörren öppnas",
        "B1",
        "Verb och perspektiv",
        "Fokusera på vad som händer med något.",
        "S-passiv bildas med s: öppna – öppnas, öppnade – öppnades, har öppnat – har öppnats. I presens försvinner normalt r: säljer – säljs. Passiv används när handlingen eller mottagaren är viktigare än utföraren. Utföraren kan anges med av.",
        rules=[
            "Alla verb på s är inte passiva: hoppas och trivas är egna verb.",
            "Behåll tiden när du byter perspektiv.",
        ],
        examples=[
            GrammarExample("Biljetterna säljs på nätet."),
            GrammarExample("Bron byggdes av ett lokalt företag."),
        ],
    ),
    GrammarTopic(
        "sv-participle-b1",
        "Ett stängt fönster",
        "B1",
        "Adjektiv och verb",
        "Beskriv ett resultat med perfekt particip.",
        "Perfekt particip kan fungera som adjektiv: en stängd dörr, ett stängt fönster, stängda dörrar. Efter vara beskriver det ofta ett tillstånd: Dörren är stängd. Lär formerna med verbet; particip och supinum är inte alltid samma: skriven – skrivet – skrivna, men har skrivit.",
        rules=[
            "Participet böjs efter substantivet när det används som adjektiv.",
            "Har följs av supinum, inte en fritt böjd participform.",
        ],
        examples=[
            GrammarExample("Brevet är skrivet på svenska."),
            GrammarExample("Butiken har stängt. Dörren är stängd."),
        ],
    ),
    GrammarTopic(
        "sv-man-b1",
        "Man, en och ens",
        "B1",
        "Pronomen",
        "Gör allmänna påståenden utan att ange en person.",
        "Man används som obestämt subjekt: Man får vänta här. Objektsformen är en och possessivformen ens: Det kan hjälpa en; ens arbete. Sin används när ägandet syftar tillbaka på man i samma sats: Man ska ta med sin biljett. Ett precist subjekt är bättre om det spelar roll vem som ansvarar.",
        rules=[
            "Verbformen ändras inte efter subjektets person eller antal i modern svenska.",
            "Allmänt man är inte samma sak som substantivet en man.",
        ],
        examples=[
            GrammarExample("Man lär sig av sina misstag."),
            GrammarExample("Det är skönt när någon lyssnar på en."),
        ],
    ),
    GrammarTopic(
        "sv-hypothetical-b1",
        "Om jag hade tid skulle jag komma",
        "B1",
        "Villkor",
        "Beskriv en tänkt situation i nutid.",
        "Preteritum i en om-sats kan uttrycka avstånd från verkligheten, inte dåtid: Om jag hade tid skulle jag komma. Följden uttrycks ofta med skulle och infinitiv. Om jag var ledig och om jag vore ledig är båda möjliga; vore är en särskild form av vara med hypotetisk betydelse.",
        rules=[
            "Tolka tempus tillsammans med villkoret och sammanhanget.",
            "Vore krävs inte efter varje om.",
        ],
        examples=[
            GrammarExample("Om vi bodde närmare skulle vi ses oftare."),
            GrammarExample("Jag skulle välja tåget om det var billigare."),
        ],
    ),
    GrammarTopic(
        "sv-obligation-b1",
        "Får inte, behöver inte och borde",
        "B1",
        "Modalitet",
        "Skilj förbud från råd och frånvaro av krav.",
        "Får inte uttrycker ofta förbud. Behöver inte säger att något inte är nödvändigt. Borde kan ge råd eller uttrycka en rimlig förväntan. Måste kan ange både krav och en stark slutsats; sammanhanget avgör. Översätt inte alla dessa uttryck med samma styrka.",
        rules=[
            "Du behöver inte betala betyder inte att betalning är förbjuden.",
            "Ett råd med borde lämnar normalt mer utrymme än ett krav med måste.",
        ],
        examples=[
            GrammarExample("Du får inte parkera här."),
            GrammarExample("Du borde vila."),
            GrammarExample("Vi behöver inte boka i förväg."),
        ],
    ),
    GrammarTopic(
        "sv-reported-b1",
        "Hon sa att hon skulle komma",
        "B1",
        "Återgivning",
        "Återge vad någon sa med rätt tid och perspektiv.",
        "Efter ett anföringsverb i dåtid används ofta dåtid även i återgivningen: Hon sa att hon var trött. Framtid från den dåtida tidpunkten uttrycks ofta med skulle. Presens kan behållas när uppgiften fortfarande gäller. Anpassa jag, här och imorgon efter vem som återger och när.",
        rules=[
            "Skilj ett ordagrant citat från en återgivning.",
            "Tempusförskjutning är inte obligatorisk i alla sammanhang.",
        ],
        examples=[
            GrammarExample("I måndags sa hon att hon skulle komma på tisdagen."),
            GrammarExample(
                "Läraren sa att vatten kokar vid ungefär hundra grader vid normalt lufttryck."
            ),
        ],
    ),
    GrammarTopic(
        "sv-concession-b1",
        "Trots att och även om",
        "B1",
        "Samband",
        "Uttryck en oväntad kontrast.",
        "Trots att följs av en sats och anger ofta ett faktiskt hinder som inte ändrar utfallet: Vi gick ut trots att det regnade. Trots följs av ett substantivuttryck: trots regnet. Även om kan ange ett tänkt hinder: Vi går även om det regnar. I vissa sammanhang överlappar betydelserna.",
        rules=[
            "Skriv trots regnet eller trots att det regnar.",
            "En inledande bisats följs av huvudsatsens verb.",
        ],
        examples=[
            GrammarExample("Trots att hon var trött kom hon."),
            GrammarExample("Vi fortsätter även om det tar tid."),
        ],
    ),
    GrammarTopic(
        "sv-purpose-b1",
        "För att och så att",
        "B1",
        "Samband",
        "Förklara mål och följder.",
        "För att med infinitiv uttrycker ofta syfte när den underförstådda utföraren är densamma: Jag ringer för att boka en tid. För att med en hel sats kan uttrycka orsak eller syfte beroende på sammanhang. Så att kan ange en följd eller ett avsett resultat. Gör avsikten tydlig när en läsare annars kan tolka fel.",
        rules=[
            "Skilj målet med en handling från ett resultat som faktiskt inträffade.",
            "Använd ett tydligt subjekt när olika personer utför handlingarna.",
        ],
        examples=[
            GrammarExample("Hon sparar för att kunna resa."),
            GrammarExample("Jag talar långsamt så att alla kan förstå."),
        ],
    ),
    GrammarTopic(
        "sv-causal-b1",
        "För, eftersom och därför",
        "B1",
        "Samband",
        "Ge en orsak och dra en följd.",
        "För kan binda ihop huvudsatser: Jag stannar, för jag är trött. Eftersom inleder en bisats: eftersom jag är trött. Därför är ett adverb som kan stå först i en huvudsats: Därför stannar jag. Samma samband kräver olika ordföljd beroende på uttrycket.",
        rules=[
            "Efter därför först i huvudsatsen följer det böjda verbet.",
            "Inte står före det böjda verbet i en neutral eftersom-sats.",
        ],
        examples=[
            GrammarExample("Bussen kom inte. Därför blev jag sen."),
            GrammarExample("Jag gick hem eftersom jag inte mådde bra."),
        ],
    ),
    GrammarTopic(
        "sv-position-verbs-b1",
        "Ligger, står, sitter och hänger",
        "B1",
        "Verb och rum",
        "Beskriv läge och placering mer precist.",
        "Svenskan använder ofta lägesverb: boken ligger, flaskan står, bilden hänger och personen sitter. Motsvarande placeringsverb är ofta lägga, ställa, hänga och sätta. Valet beror på föremål och situation; lär naturliga kombinationer i stället för en enda geometrisk regel.",
        rules=[
            "Ligga beskriver läge; lägga beskriver att placera något.",
            "Sitta kan beskriva något som är fäst: affischen sitter på väggen.",
        ],
        examples=[
            GrammarExample("Lägg boken på bordet. Den ligger där."),
            GrammarExample("Jag ställer koppen på hyllan."),
        ],
    ),
    GrammarTopic(
        "sv-reciprocal-b1",
        "Varandra och träffas",
        "B1",
        "Verb och pronomen",
        "Beskriv handlingar mellan flera personer.",
        "Varandra uttrycker en ömsesidig relation: Vi hjälper varandra. Sig uttrycker normalt att var och en handlar mot sig själv: De tvättar sig. Vissa s-verb har ömsesidig betydelse, till exempel träffas och kramas. Inte alla s-verb är passiva eller ömsesidiga.",
        rules=[
            "Vi ser varandra och vi ser oss själva har olika betydelse.",
            "Träffas kan användas utan ett uttryckt objekt.",
        ],
        examples=[
            GrammarExample("Vi hörs imorgon."),
            GrammarExample("Grannarna lånar verktyg av varandra."),
        ],
    ),
    GrammarTopic(
        "sv-each-all-b1",
        "Varje, alla, båda och hela",
        "B1",
        "Bestämningar",
        "Uttryck delar och helheter utan att blanda former.",
        "Varje följs av obestämd singular: varje dag. Alla används med plural: alla dagar eller alla barnen. Båda avser två. Hela används med ett bestämt substantivuttryck: hela dagen, hela mitt liv. Allt kan stå själv eller med ett-ord i mängdbetydelse: allt vatten.",
        rules=[
            "Varje barn betonar individerna; alla barn betonar gruppen.",
            "Båda betyder två, inte ett ospecificerat antal.",
        ],
        examples=[
            GrammarExample("Vi läser varje dag."),
            GrammarExample("Båda barnen sov hela natten."),
        ],
    ),
    GrammarTopic(
        "sv-countable-b1",
        "Färre och mindre",
        "B1",
        "Mängd",
        "Jämför antal och mängd.",
        "Färre används normalt med räkningsbara pluralord: färre bilar. Mindre används bland annat med mängd: mindre trafik. Mindre kan också beskriva storlek: mindre bilar är bilar av mindre storlek, inte nödvändigtvis ett lägre antal. Mer och fler följer ett liknande mönster.",
        rules=[
            "Fler frågor men mer tid.",
            "Välj efter avsedd betydelse, inte bara substantivets form.",
        ],
        examples=[
            GrammarExample("Vi behöver färre möten och mer tid."),
            GrammarExample("Det finns fler cyklar men mindre biltrafik."),
        ],
    ),
    GrammarTopic(
        "sv-sentence-adverbs-b1",
        "Ofta, alltid, kanske och aldrig",
        "B1",
        "Ordföljd",
        "Placera frekvens och bedömning i meningen.",
        "I en neutral huvudsats med subjekt först kommer satsadverb ofta efter det böjda verbet: Jag har aldrig varit där. I bisats kommer de före: att jag aldrig har varit där. Kanske kan stå på flera platser och har även särskilda mönster; använd till att börja med Jag kommer kanske eller Kanske kommer jag.",
        rules=[
            "Hjälpverbet är det böjda verbet i har aldrig varit.",
            "Placeringen kan påverka betoning och vad adverbet syftar på.",
        ],
        examples=[
            GrammarExample("Hon säger att hon ofta arbetar hemma."),
            GrammarExample("Vi kommer kanske senare."),
        ],
    ),
    GrammarTopic(
        "sv-inte-heller-b1",
        "Också, inte heller och både ... och",
        "B1",
        "Samband",
        "Lägg till positiv och negativ information.",
        "Också lägger till något positivt: Jag kommer också. Inte heller lägger till en negation: Jag kommer inte heller. Både ... och kopplar ihop två delar som gäller. Varken ... eller negerar normalt båda delarna utan ytterligare inte.",
        rules=[
            "Varken kaffe eller te betyder inget av de två.",
            "Placera också nära den information som ska läggas till när det finns risk för missförstånd.",
        ],
        examples=[
            GrammarExample("Hon talar både svenska och finska."),
            GrammarExample("Jag har varken tid eller pengar."),
            GrammarExample("Jag kan inte heller komma."),
        ],
    ),
    GrammarTopic(
        "sv-relative-where-b1",
        "Där, dit och vars",
        "B1",
        "Bisatser",
        "Knyt beskrivningar till platser och ägare.",
        "Där kan inleda en relativ beskrivning av plats: staden där jag bor. Dit anger ett mål: staden dit jag flyttar. Vars uttrycker en äganderelation: grannen vars hund skäller. Vars böjs inte efter ägaren eller det ägda.",
        rules=[
            "Vars följs av obestämd substantivform.",
            "Låt det framgå tydligt vilket ord relativsatsen beskriver.",
        ],
        examples=[
            GrammarExample("Det är skolan där min syster arbetar."),
            GrammarExample("Jag träffade en man vars son spelar i laget."),
        ],
    ),
    GrammarTopic(
        "sv-time-boundaries-b1",
        "Innan, efter att och tills",
        "B1",
        "Tid och samband",
        "Beskriv ordning och en tidsgräns.",
        "Innan anger att något sker före en annan händelse. Efter att anger senare tid. Tills anger en slutpunkt: Jag väntar tills du kommer. Förrän används normalt efter en negation: Jag går inte förrän du kommer. Tills och förrän kan beskriva samma gräns men med olika perspektiv.",
        rules=[
            "Efter att följs av en sats; efter kan följas av ett substantiv.",
            "Tills säger inte i sig vad som händer efter gränsen.",
        ],
        examples=[
            GrammarExample("Ring innan du åker."),
            GrammarExample("Vi stannade tills mötet var slut."),
            GrammarExample("Hon kom inte förrän klockan nio."),
        ],
    ),
    GrammarTopic(
        "sv-repair-b1",
        "Det jag menar är ...",
        "B1",
        "Samspel",
        "Förtydliga och kontrollera att du förstått.",
        "Uttryck som det jag menar är och menar du att hjälper dig att reparera ett missförstånd. En indirekt kontrollfråga använder bisatsordföljd: Menar du att vi inte ska komma? Be om precisering innan du drar slutsatser om tid, plats eller ansvar.",
        rules=[
            "Återge den del du vill kontrollera, inte en starkare version.",
            "Det jag menar kan följas av en att-sats eller ett substantivuttryck.",
        ],
        examples=[
            GrammarExample("Menar du att mötet börjar tidigare?"),
            GrammarExample("Det jag menar är att vi behöver mer tid."),
        ],
    ),
]
