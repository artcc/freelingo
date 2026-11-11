"""Swedish C1: accountable argument, discourse and nuanced interaction."""

from app.data._types import GrammarExample, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "sv-source-distance-c1",
        "Påstås, uppges och bekräftas",
        "C1",
        "Källor och hållning",
        "Bevara avståndet mellan ett påstående och en verifierad uppgift.",
        "Påstås, uppges och bekräftas fördelar ansvar och säkerhet olika. Påstås kan signalera distans; uppges hänvisar till lämnad information; bekräftas anger att en uppgift fått stöd eller bestyrkts av en viss källa. Inget av orden ersätter källkritik. Ange vem som lämnar eller bekräftar uppgiften när det är relevant.",
        rules=[
            "Byt inte uppges mot har utan stöd för en säkrare utsaga.",
            "Behåll källans avgränsning och tidpunkt.",
        ],
        examples=[
            GrammarExample(
                "Bolaget uppger att felet är åtgärdat; kunden har ännu inte kunnat kontrollera det."
            ),
            GrammarExample("Enligt protokollet bekräftade ordföranden bara datumet."),
        ],
    ),
    GrammarTopic(
        "sv-hedging-c1",
        "Torde, förefaller och tycks",
        "C1",
        "Modalitet",
        "Gradera en bedömning utan att göra den innehållslös.",
        "Torde uttrycker ofta en välgrundad men inte säker förmodan i formell stil. Tycks och förefaller presenterar ett intryck eller en bedömning. De skiljer sig från ett direkt konstaterande. Ange underlaget när en läsare behöver förstå hur slutsatsen dragits.",
        rules=[
            "Fler reservationer gör inte automatiskt ett påstående mer precist.",
            "Skilj försiktig formulering från brist på belägg.",
        ],
        examples=[
            GrammarExample("Med nuvarande bemanning torde arbetet ta ytterligare en vecka."),
            GrammarExample("Resultaten förefaller stabila, men urvalet är litet."),
        ],
    ),
    GrammarTopic(
        "sv-reporting-inference-c1",
        "Slutsats, uppgift och förmodan",
        "C1",
        "Modalitet",
        "Identifiera varför skribenten tror något.",
        "Måste ha bygger ofta en stark slutsats på omständigheter, lär ha återger ofta en uppgift och kan ha lämnar en möjlighet öppen. Meningen Hon måste ha lämnat huset är inte i sig ett ögonvittnesmål. Sammanfattningar måste behålla om informationen observerats, återgivits eller härletts.",
        rules=[
            "En stark slutsats är fortfarande en slutsats.",
            "Lär i Hon lär barnen läsa har en annan funktion än i Hon lär vara bortrest.",
        ],
        examples=[
            GrammarExample("Lampan är släckt, så de kan ha gått hem."),
            GrammarExample("Hon lär ha tackat nej, men jag har inte talat med henne."),
        ],
    ),
    GrammarTopic(
        "sv-topic-fronting-c1",
        "Det förslaget kan jag stödja",
        "C1",
        "Informationsstruktur",
        "Lyft fram det samtalet redan handlar om.",
        "Ett objekt eller annat led kan stå i fundamentet: Det förslaget kan jag stödja. Det böjda verbet står fortfarande på andra plats. Framflyttningen knyter ofta an till tidigare information eller markerar kontrast; den gör inte automatiskt ledet till subjekt.",
        rules=[
            "Kontrollera vem som handlar även när objektet står först.",
            "Välj fundament som hjälper mottagaren att följa resonemanget.",
        ],
        examples=[
            GrammarExample("Den invändningen har vi redan behandlat."),
            GrammarExample("I övrigt delar jag din bedömning."),
        ],
    ),
    GrammarTopic(
        "sv-dislocation-c1",
        "Den där frågan, den får vänta",
        "C1",
        "Talspråk och struktur",
        "Förstå återupptagna led i samtal.",
        "I samtal kan ett tema ställas utanför satsen och sedan tas upp med ett pronomen: Den där frågan, den får vänta. Detta är inte samma struktur som vanlig objektsframflyttning. Konstruktionen kan underlätta planering och fokus i tal. I koncentrerad sakprosa passar ofta en integrerad sats bättre.",
        rules=[
            "Bedöm formen utifrån genre, inte enbart skriftens V2-mall.",
            "Vid redigering ska temat och ansvarsfördelningen bevaras.",
        ],
        examples=[
            GrammarExample("Min gamla cykel, den fungerar faktiskt fortfarande."),
            GrammarExample("Det ordnar sig, det där med biljetterna."),
        ],
    ),
    GrammarTopic(
        "sv-focus-particles-c1",
        "Till och med, ens och just",
        "C1",
        "Räckvidd och fokus",
        "Tolka vilka förväntningar ett fokusord aktiverar.",
        "Till och med presenterar ofta något som överraskande på en skala: Till och med chefen hjälpte till. Ens förekommer ofta i negativa och frågande sammanhang: Hon svarade inte ens. Just kan avgränsa eller betona ett led. Förväntningen är ofta underförstådd och behöver prövas mot sammanhanget.",
        rules=[
            "Flyttas fokusordet kan det framhävda ledet ändras.",
            "En antydd förväntning är inte alltid ett uttryckligt sakpåstående.",
        ],
        examples=[
            GrammarExample("Just den frågan har vi ännu inte besvarat."),
            GrammarExample("Han hann inte ens läsa sammanfattningen."),
        ],
    ),
    GrammarTopic(
        "sv-negation-quantifiers-c1",
        "Ingen, inte varje och långt ifrån alla",
        "C1",
        "Räckvidd och logik",
        "Bevara styrkan i mängduttryck.",
        "Ingen utesluter samtliga individer i den avsedda gruppen. Inte varje och inte alla förnekar full täckning, men anger inte exakt antal. Långt ifrån alla förstärker avståndet till samtliga utan att ange en procentsats. En omskrivning till de flesta kan därför lägga till information som saknas.",
        rules=[
            "Gör inte ett obestämt antal till en bestämd andel.",
            "Ange vilken grupp mängduttrycket gäller.",
        ],
        examples=[
            GrammarExample("Inte alla som anmälde sig deltog."),
            GrammarExample("Långt ifrån alla svar var fullständiga; andelen framgår inte här."),
        ],
    ),
    GrammarTopic(
        "sv-embedded-reference-c1",
        "Sin och hennes över satsgränser",
        "C1",
        "Referens",
        "Undvik att byta ägare i en komplex mening.",
        "Reflexiva possessiv tolkas i relation till satsens subjekt, men infinitivkonstruktioner och perspektiv kan göra referensen mer komplex. I Sara sa att Lina tog sin cykel syftar sin normalt på Lina. Hennes kan få flera möjliga referenter. Upprepa namnet när en praktisk instruktion kräver entydighet.",
        rules=[
            "Analysera varje sats innan du avgör referensen.",
            "En omskrivning får inte byta den person som äger saken.",
        ],
        examples=[
            GrammarExample("Sara sa att Lina hade hämtat Saras cykel."),
            GrammarExample("Lina tog sin cykel och gav Sara hennes nycklar."),
        ],
    ),
    GrammarTopic(
        "sv-ellipsis-c1",
        "Utelämnade led i samordning",
        "C1",
        "Textbindning",
        "Återskapa det som inte upprepas.",
        "Samordnade satser kan utelämna gemensamma led: Anna tog tåget och Erik bussen. Det underförstådda verbet är tog. Vid sammanfattning måste du återställa rätt relation utan att lägga till en ny handling. Om flera möjliga återställningar finns bör formuleringen förtydligas.",
        rules=[
            "De samordnade leden behöver vara begripliga och jämförbara.",
            "Utelämning är inte samma sak som att informationen saknas helt.",
        ],
        examples=[
            GrammarExample("Några ville fortsätta, andra avbryta."),
            GrammarExample("Hon har läst rapporten men inte bilagan."),
        ],
    ),
    GrammarTopic(
        "sv-nominal-density-c1",
        "Täta nominalfraser",
        "C1",
        "Sakprosa",
        "Packa upp en informationstät formulering.",
        "En nominalfras som kommunens planerade granskning av avtalet innehåller aktör, tidsperspektiv och objekt. Omskrivningen kommunen har granskat avtalet ändrar planerat till genomfört. Packa upp leden i fullständiga satser när texten blir svårläst och behåll osäkerhet, tid och relationer.",
        rules=[
            "Markera skillnaden mellan förslag, plan och genomförande.",
            "Undvik kedjor av substantiv som döljer vem som gör vad.",
        ],
        examples=[
            GrammarExample("Den föreslagna sänkningen av avgiften har inte beslutats."),
            GrammarExample("Kommunen planerar att granska avtalet."),
        ],
    ),
    GrammarTopic(
        "sv-controlled-infinitive-c1",
        "Vem ska utföra handlingen?",
        "C1",
        "Infinitiv och referens",
        "Tolka det underförstådda subjektet.",
        "I Sara lovade Lina att ringa är Sara normalt den som ska ringa. I Sara bad Lina att ringa är Lina den avsedda utföraren. Verbets konstruktion styr tolkningen. En omformulering med att-sats kan klargöra deltagarna, men får inte göra en begäran till ett löfte.",
        rules=[
            "Lär kontrollmönstret med verbet och dess deltagare.",
            "Skriv ut subjektet när ansvar kan missförstås.",
        ],
        examples=[
            GrammarExample("Jag lovade henne att skicka underlaget."),
            GrammarExample("Jag bad henne att skicka underlaget."),
        ],
    ),
    GrammarTopic(
        "sv-conditional-inversion-c1",
        "Hade jag vetat, skulle jag ha ringt",
        "C1",
        "Villkor",
        "Känn igen villkor utan om.",
        "Ett villkor kan börja med det böjda verbet utan om: Hade jag vetat, skulle jag ha ringt. Detta är inte en fråga trots verbets första plats. Formen förekommer i både tal och skrift och kan ge en koncentrerad, ibland eftertrycklig stil. Följden måste fortfarande förstås i relation till villkoret.",
        rules=[
            "Återställ om vid kontroll av betydelsen.",
            "Verbförst kan ha andra funktioner; använd sammanhang och skiljetecken.",
        ],
        examples=[
            GrammarExample("Skulle du behöva hjälp, är det bara att ringa."),
            GrammarExample("Hade vi åkt tidigare, hade vi hunnit."),
        ],
    ),
    GrammarTopic(
        "sv-conditional-limits-c1",
        "Så länge som och förutsatt att",
        "C1",
        "Villkor och avtal",
        "Skilj varaktighet från villkor.",
        "Så länge som kan ange tid eller ett fortlöpande villkor. Förutsatt att uttrycker ett uttryckligt villkor: Vi godkänner ändringen förutsatt att kostnaden inte ökar. Ett villkorat godkännande är inte ovillkorligt. Undersök också vem som ska bedöma att villkoret är uppfyllt.",
        rules=[
            "Behåll villkoret i en sammanfattning av ett beslut.",
            "Förtydliga om så länge som handlar om tid eller förutsättning.",
        ],
        examples=[
            GrammarExample("Du får använda lokalen så länge bokningen gäller."),
            GrammarExample("Vi kan leverera på fredag förutsatt att materialet kommer idag."),
        ],
    ),
    GrammarTopic(
        "sv-concession-argument-c1",
        "Visserligen ... men och likväl",
        "C1",
        "Argumentation",
        "Medge en invändning utan att ge upp slutsatsen.",
        "Visserligen markerar ofta ett medgivande som följs av en begränsning med men. Likväl och ändå kan uttrycka att slutsatsen står kvar trots motargumentet. Mönstret kan ge den senare delen större argumentativ tyngd. Medgivandet ska återges rättvist, inte försvagas i smyg.",
        rules=[
            "Identifiera vilken slutsats texten faktiskt stödjer.",
            "Ett medgivande gäller den angivna punkten, inte nödvändigtvis hela motpartens ståndpunkt.",
        ],
        examples=[
            GrammarExample("Visserligen är priset lägre, men avtalet binder oss längre."),
            GrammarExample("Underlaget är begränsat. Likväl finns skäl att gå vidare försiktigt."),
        ],
    ),
    GrammarTopic(
        "sv-discourse-particles-c1",
        "Ju, väl och nog",
        "C1",
        "Samspel och hållning",
        "Hör hur talaren förhåller sig till mottagaren.",
        "Ju presenterar ofta information som gemensam eller självklar, väl kan söka bekräftelse och nog kan uttrycka en bedömning eller lugnande försäkran. Betydelsen beror på tonfall, placering och situation. Nog i nu är det nog anger i stället en gräns. Ingen av partiklarna har en enda översättning.",
        rules=[
            "Antagen gemensam kunskap kan uppfattas som inkluderande eller påtryckande.",
            "Kontrollera tonfall innan du tolkar en partikel som säkerhet eller tvekan.",
        ],
        examples=[
            GrammarExample("Du kommer väl på fredag?"),
            GrammarExample("Det ordnar sig nog."),
            GrammarExample("Vi har ju redan bokat."),
        ],
    ),
    GrammarTopic(
        "sv-indirect-refusal-c1",
        "Avböja utan att skapa ett falskt löfte",
        "C1",
        "Samspel",
        "Gör ett vänligt nej begripligt.",
        "En indirekt formulering som det blir svårt kan fungera som avböjande, men också som inledning till förhandling. Lägg till vad som faktiskt är möjligt när beslutet behöver vara tydligt. En mildare ton får inte förvandla ett nej till ett löfte om senare leverans.",
        rules=[
            "Skilj beklagande från åtagande.",
            "Ge ett konkret alternativ bara när det faktiskt erbjuds.",
        ],
        examples=[
            GrammarExample("Jag hinner inte till fredag, men jag kan leverera på tisdag."),
            GrammarExample("Tack för frågan. Jag behöver avstå den här gången."),
        ],
    ),
    GrammarTopic(
        "sv-mediation-c1",
        "Återge två perspektiv rättvist",
        "C1",
        "Samspel och text",
        "Sammanfatta en konflikt utan att lägga till samförstånd.",
        "Använd källmarkörer och parallella konstruktioner: Gruppen vill ... medan ledningen bedömer ... Skilj gemensamma mål från oenighet om medel. Uttryck som båda är överens om kräver att den gemensamma punkten faktiskt är belagd.",
        rules=[
            "Tillskriv varje ståndpunkt rätt deltagare.",
            "Gör inte en vilja till ett fattat beslut.",
        ],
        examples=[
            GrammarExample("Båda vill korta väntetiden, men de föreslår olika lösningar."),
            GrammarExample(
                "Personalen efterfrågar mer tid; ledningen vill först se en kostnadsberäkning."
            ),
        ],
    ),
    GrammarTopic(
        "sv-irony-c1",
        "När orden och situationen drar åt olika håll",
        "C1",
        "Pragmatik",
        "Tolka möjlig ironi utan att läsa in den överallt.",
        "Vilken tur! efter en missad buss kan uttrycka ironi snarare än glädje. Tolkningen bygger på situation, tonfall och relation, inte en särskild grammatik. I skrift kan signalerna vara svaga. Vid praktiska beslut är en kontrollfråga bättre än att anta att motsatsen alltid avses.",
        rules=[
            "Skilj ironisk hållning från det faktiska händelseinnehållet.",
            "Humor kan vara välvillig eller kritisk; relationen spelar roll.",
        ],
        examples=[
            GrammarExample("Bussen gick precis. Vilken perfekt tajming!"),
            GrammarExample("Menar du det bokstavligt, eller skämtar du?"),
        ],
    ),
    GrammarTopic(
        "sv-punctuation-c1",
        "Komma, kolon och tankstreck",
        "C1",
        "Skrift och disposition",
        "Visa textens struktur utan att ändra sambanden.",
        "Kolon kan introducera en förklaring eller uppräkning. Tankstreck kan markera ett inskott eller en efterföljande precisering. Svensk kommatering styrs i stor utsträckning av tydlighet; sätt inte komma mekaniskt vid varje bisatsgräns. Skiljetecken ersätter inte ett saknat logiskt samband.",
        rules=[
            "Använd samma princip konsekvent i en text.",
            "Kontrollera att ett inskott inte gör huvudmeningen svår att följa.",
        ],
        examples=[
            GrammarExample("Vi har ett problem: underlaget saknas."),
            GrammarExample("Beslutet – som fattades igår – gäller från januari."),
        ],
    ),
    GrammarTopic(
        "sv-register-variation-c1",
        "Talspråk, standardskrift och regional variation",
        "C1",
        "Register",
        "Anpassa form utan att döma ut giltiga varianter.",
        "Dom, sen och vissa reducerade former kan passa i dialog och informell skrift, medan de, dem och sedan ofta väljs i redigerad sakprosa. Regionalt uttal är inte i sig fel. Svenskan i Sverige varierar, och finlandssvenska är en etablerad varietet, inte bristfällig sverigesvenska.",
        rules=[
            "Ange vilken norm en redigering följer.",
            "Rätta inte regionala eller informella former som universella grammatikfel.",
        ],
        examples=[
            GrammarExample("Dom kommer sen. – De kommer sedan."),
            GrammarExample("I en intervju kan talspråkliga drag vara en del av rösten."),
        ],
    ),
    GrammarTopic(
        "sv-prosody-c1",
        "Betoning och betydelse i samtal",
        "C1",
        "Uttal och samspel",
        "Använd satsbetoning för att korrigera rätt sak.",
        "Betoningen i Jag sa att hon kunde komma kan lyfta fram vem som sa något, möjligheten eller själva ankomsten. Svenskans ordaccenter och satsmelodi varierar regionalt. Träna lyssning och funktionell betoning utan att kräva en enda regional melodi av alla talare.",
        rules=[
            "Ordaccent och kontrastbetoning är olika fenomen.",
            "En utskrift utan ljud ger inte alltid tillräckligt underlag för prosodisk tolkning.",
        ],
        examples=[
            GrammarExample("Jag sa TISDAG, inte torsdag."),
            GrammarExample("Hon KAN komma; hon har inte lovat att göra det."),
        ],
    ),
]
