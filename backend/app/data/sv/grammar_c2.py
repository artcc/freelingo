"""Swedish C2: precision, inference and adaptable interaction."""

from app.data._types import GrammarExample, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "sv-presupposition-c2",
        "Det som tas för givet",
        "C2",
        "Pragmatik",
        "Skilj uttryckligt innehåll från förutsatta uppgifter.",
        "Har du slutat avbryta? tar normalt för givet att mottagaren tidigare avbrutit. Även en nekande reaktion kan lämna förutsättningen orörd. Vid saklig återgivning bör du inte okritiskt göra en sådan förutsättning till ett verifierat faktum. Den kan ifrågasättas direkt.",
        rules=[
            "Identifiera vad frågan förutsätter innan du besvarar den.",
            "Förutsättningar kan vara felaktiga eller omstridda.",
        ],
        examples=[
            GrammarExample("Jag delar inte förutsättningen att rutinen har misslyckats."),
            GrammarExample("När började problemen? förutsätter att problem har uppstått."),
        ],
    ),
    GrammarTopic(
        "sv-implicature-c2",
        "Det antydda är inte alltid det sagda",
        "C2",
        "Pragmatik",
        "Tolka en möjlig slutsats utan att göra den nödvändig.",
        "Några svarade antyder ofta att inte alla svarade, men det är inte samma uttryckliga påstående som några men inte alla. Antydningen kan upphävas: några svarade, kanske rentav alla. I sammanfattning och medling måste du hålla isär ordens innehåll och rimliga men osäkra slutsatser.",
        rules=[
            "Pröva om tillägget faktiskt motsäger meningen eller bara bryter en förväntan.",
            "Markera tolkningar som tolkningar när de har praktisk betydelse.",
        ],
        examples=[
            GrammarExample("Hon har läst några av rapporterna, möjligen samtliga."),
            GrammarExample("Att förslaget inte nämns behöver inte betyda att det avvisats."),
        ],
    ),
    GrammarTopic(
        "sv-metalinguistic-negation-c2",
        "Inte bra – utmärkt",
        "C2",
        "Negation och fokus",
        "Känn igen när en formulering snarare än ett faktum avvisas.",
        "Det var inte bra, det var utmärkt avvisar ordet bra som otillräckligt, inte den positiva bedömningen. Sådan metalingvistisk negation kräver tydliga signaler. Utan fortsättningen kan Det var inte bra tolkas som vanlig negation. Bevara den retoriska korrigeringens riktning vid omskrivning.",
        rules=[
            "Läs hela korrigeringen innan du sammanfattar värderingen.",
            "En starkare synonym kan vara rättelsen, inte motsatsen.",
        ],
        examples=[
            GrammarExample("Hon är inte skicklig – hon är enastående."),
            GrammarExample("Det är inte en försening, säger de, utan en omplanering."),
        ],
    ),
    GrammarTopic(
        "sv-layered-modality-c2",
        "Skulle kunna ha och måste ha kunnat",
        "C2",
        "Modalitet",
        "Följ räckvidden i flera modala led.",
        "Skulle kunna ha bidragit lämnar ett möjligt bidrag öppet i en tänkt eller försiktigt bedömd situation. Måste ha kunnat anger en stark slutsats om en tidigare möjlighet, inte säkert att handlingen utfördes. Identifiera vad varje modal gäller och vilken tid bedömningen avser.",
        rules=[
            "Möjlighet till en handling är inte handlingens genomförande.",
            "Förenkla formen bara om säkerhetsgrad och tidsförhållande bevaras.",
        ],
        examples=[
            GrammarExample("Åtgärden skulle kunna ha minskat risken, men det är inte visat."),
            GrammarExample("Hon måste ha kunnat höra oss, men vi vet inte om hon lyssnade."),
        ],
    ),
    GrammarTopic(
        "sv-free-indirect-c2",
        "Berättarröst och personens perspektiv",
        "C2",
        "Litterär förståelse",
        "Känn igen fri indirekt framställning.",
        "En berättelse kan återge en persons tankar utan citattecken eller hon tänkte: Hon såg brevet. Skulle hon verkligen behöva svara nu? Berättarens grammatiska perspektiv kan blandas med personens värderingar och tidsord. Avgör vem som kan stå för bedömningen innan du tillskriver den författaren.",
        rules=[
            "Skilj författare, berättare och person.",
            "Flera röster kan samverka utan en tydlig citatgräns.",
        ],
        examples=[
            GrammarExample("Erik stannade. Så detta var alltså tacken."),
            GrammarExample("Hon lade ifrån sig telefonen. Imorgon skulle allt bli annorlunda."),
        ],
    ),
    GrammarTopic(
        "sv-archaic-recognition-c2",
        "Vore, må och historiska verbformer",
        "C2",
        "Register och läsning",
        "Förstå markerade former utan att använda dem överallt.",
        "Vore är levande i hypotetiska uttryck. Må i Må du leva länge uttrycker en önskan. Äldre texter kan ha pluralformer som vi äro och de gingo; modern standardsvenska använder vi är och de gick. Dessa former tränas främst för läsförståelse och stilmedvetenhet, inte som krav i vardagligt tal.",
        rules=[
            "Skilj levande fasta uttryck från historisk böjning.",
            "Modernisera inte en citerad text utan att markera ingreppet.",
        ],
        examples=[
            GrammarExample("Det vore klokt att avvakta."),
            GrammarExample("Må bästa lag vinna!"),
            GrammarExample("De gingo hem. – De gick hem."),
        ],
    ),
    GrammarTopic(
        "sv-legal-scope-c2",
        "Undantag, led och villkorskedjor",
        "C2",
        "Precis sakprosa",
        "Avgränsa vad ett undantag faktiskt gäller.",
        "I täta regler kan ett efterställt undantag syfta på ett led eller hela bestämmelsen. För att klargöra texten kan du dela upp huvudregel, villkor och undantag. Lägg inte till en rättighet som bara är möjlig och ta inte bort ett nödvändigt villkor. Vid verklig tvetydighet behövs precisering, inte en självsäker gissning.",
        rules=[
            "Kontrollera räckvidden för endast, om inte och såvida.",
            "En språklig omskrivning ska inte ändra den normativa styrkan.",
        ],
        examples=[
            GrammarExample(
                "Ersättning kan beviljas om ansökan är fullständig; det innebär inte att den alltid beviljas."
            ),
            GrammarExample("Undantaget gäller tidsfristen, inte kravet på underlag."),
        ],
    ),
    GrammarTopic(
        "sv-ambiguity-c2",
        "Tvetydighet som behöver lösas",
        "C2",
        "Referens och struktur",
        "Upptäck när flera rimliga läsningar återstår.",
        "Hon såg mannen med kikaren kan betyda att hon använde kikaren eller att mannen hade den. Grammatiskt möjliga läsningar är inte alltid lika rimliga i sammanhanget, men redigering bör säkra den avsedda betydelsen. Fråga om avsikten när underlaget inte räcker.",
        rules=[
            "Skilj språklig möjlighet från belagd avsikt.",
            "Välj en precisering som bevarar den bekräftade tolkningen.",
        ],
        examples=[
            GrammarExample("Med hjälp av kikaren såg hon mannen."),
            GrammarExample("Hon såg mannen som bar en kikare."),
        ],
    ),
    GrammarTopic(
        "sv-rhetorical-questions-c2",
        "Frågor som driver ett argument",
        "C2",
        "Retorik",
        "Skilj en begäran om svar från ett påtryckande påstående.",
        "Vem vill betala mer för mindre? kan driva ett argument snarare än efterfråga namn. Den retoriska frågan framställer ofta svaret som självklart. En neutral omskrivning bör visa talarens ståndpunkt utan att presentera det underförstådda svaret som ett bevisat gruppsamförstånd.",
        rules=[
            "Retorisk form ersätter inte belägg.",
            "I ett verkligt samtal kan mottagaren ändå besvara frågan sakligt.",
        ],
        examples=[
            GrammarExample("Är det verkligen rimligt att kunden ska bära hela risken?"),
            GrammarExample("Talaren ifrågasätter att kunden ensam ska bära risken."),
        ],
    ),
    GrammarTopic(
        "sv-understatement-c2",
        "Inte helt lyckat och andra underdrifter",
        "C2",
        "Stil och samspel",
        "Tolka försiktig kritik i sitt sammanhang.",
        "Inte helt lyckat kan vara mild kritik eller en kraftig underdrift. Litotes uttrycker ibland en positiv eller negativ värdering genom att negera motsatsen: inte illa. Betydelsen kan inte räknas ut enbart ur negationen. Relation, tonfall och följande förslag hjälper tolkningen.",
        rules=[
            "Överdriv inte kritiken i en sammanfattning utan stöd.",
            "Kontrollera vad mottagaren förväntas göra efter omdömet.",
        ],
        examples=[
            GrammarExample("Det var inte illa för ett första försök."),
            GrammarExample("Formuleringen är inte helt lyckad; vi behöver skriva om den."),
        ],
    ),
    GrammarTopic(
        "sv-analogy-c2",
        "Liknelse, metafor och argument",
        "C2",
        "Retorik och betydelse",
        "Använd bilder utan att förväxla dem med bevis.",
        "En flaskhals i processen beskriver en begränsande del med en metafor. En jämförelse kan förklara en relation men bevisar inte att två situationer är lika i alla relevanta avseenden. Vid saklig omformulering ska relationen bevaras och bildens begränsningar framgå vid behov.",
        rules=[
            "Ange vilka egenskaper jämförelsen faktiskt gäller.",
            "Skilj metonymisk hänvisning från bokstavlig aktör: kommunen kan avse dess företrädare.",
        ],
        examples=[
            GrammarExample("Granskningen har blivit en flaskhals: ärenden väntar på samma steg."),
            GrammarExample("Kommunen meddelar att tidsplanen ändras."),
        ],
    ),
    GrammarTopic(
        "sv-turn-management-c2",
        "Avbryta, återknyta och lämna ordet",
        "C2",
        "Samspel",
        "Styr ett komplext samtal utan att tappa andras poänger.",
        "En artig avbrytning kan markera syfte och begränsning: Får jag stanna vid en sak innan vi går vidare? Återknyt sedan till den andres argument och lämna tillbaka ordet. Fraserna fungerar bara om handlingen följer dem; ett långt avbrott blir inte kort av att kallas en liten fråga.",
        rules=[
            "Skilj behov av förtydligande från ett ämnesbyte.",
            "Bevara den punkt som tillfälligt skjuts upp.",
        ],
        examples=[
            GrammarExample("Jag vill bara kontrollera tidsfristen, sedan får du fortsätta."),
            GrammarExample("Om jag återknyter till det du sa om kostnaden ..."),
        ],
    ),
    GrammarTopic(
        "sv-negotiated-commitment-c2",
        "Öppenhet är inte ett åtagande",
        "C2",
        "Förhandling",
        "Formulera exakt vad parterna har och inte har lovat.",
        "Vi är öppna för att diskutera är svagare än vi avser att genomföra, som i sin tur inte är samma sak som vi förbinder oss att genomföra. En förhandling kan nå samsyn om nästa steg utan att lösa sakfrågan. Protokoll ska skilja erbjudande, villkor och bindande åtagande.",
        rules=[
            "Lägg inte till löften vid en vänligare omskrivning.",
            "Ange ansvar, villkor och tid när ett åtagande faktiskt görs.",
        ],
        examples=[
            GrammarExample("Vi kan pröva förslaget, men har ännu inte godkänt finansieringen."),
            GrammarExample(
                "Parterna enades om att utreda frågan, inte om att genomföra ändringen."
            ),
        ],
    ),
    GrammarTopic(
        "sv-humour-repair-c2",
        "Reagera på humor och reparera tonen",
        "C2",
        "Samspel",
        "Hantera skämt som inte landar som avsett.",
        "Humor bygger ofta på delad kunskap, överdrift eller ett oväntat perspektiv. Om ett skämt missförstås kan du förklara avsikten och erkänna effekten utan att skuldbelägga mottagaren. Jag skämtade bara räcker inte alltid som reparation. En saklig återgång hjälper samtalet vidare.",
        rules=[
            "Avsikt och faktisk effekt är olika saker.",
            "Välj förtydligande eller ursäkt efter situationen, inte efter en fast mall.",
        ],
        examples=[
            GrammarExample(
                "Det var tänkt som självironi, men jag hör att det lät som kritik mot dig."
            ),
            GrammarExample("Jag uttryckte mig klumpigt. Låt mig säga vad jag faktiskt menar."),
        ],
    ),
    GrammarTopic(
        "sv-adaptive-reformulation-c2",
        "Samma innehåll för olika mottagare",
        "C2",
        "Medling och stil",
        "Ändra uttryckssätt utan att ändra sakförhållanden.",
        "En facktext kan göras mer tillgänglig genom kortare satser, förklarade termer och tydliga aktörer. Bevara villkor, kvantifiering, tid och grad av säkerhet. Ett samband i materialet får inte bli en bevisad orsak, och ett genomsnitt säger inte hur varje individ påverkas.",
        rules=[
            "Förenkla språket, inte bort reservationer som bär betydelse.",
            "Skilj språklig tillgänglighet från en ny slutsats.",
        ],
        examples=[
            GrammarExample("Studien visar ett samband, men fastställer inte vad som orsakar vad."),
            GrammarExample("I genomsnitt minskade väntetiden; vissa fick ändå vänta längre."),
        ],
    ),
    GrammarTopic(
        "sv-synthesis-c2",
        "Väga belägg och avsluta öppna resonemang",
        "C2",
        "Argumentation",
        "Sammanfatta vad underlaget medger och vad som återstår.",
        "En syntes väger källornas räckvidd, invändningar och gemensamma punkter. Sammantaget markerar en helhetsbedömning men skapar inte säkerhet i sig. Avsluta med en slutsats som motsvarar beläggen och skilj den från ett praktiskt förslag om hur man bör gå vidare.",
        rules=[
            "Redovisa kvarstående oenighet när den påverkar slutsatsen.",
            "Ett handlingsförslag kan vara rimligt trots osäkerhet, men är inte därmed ett faktum.",
        ],
        examples=[
            GrammarExample(
                "Sammantaget talar underlaget för ett försök i liten skala, inte för ett omedelbart fullständigt införande."
            ),
            GrammarExample(
                "Vi vet ännu inte om effekten består; därför föreslår vi en uppföljning."
            ),
        ],
    ),
]
