"""Swedish B2: scope, alternatives, reported claims and practical argument."""

from app.data._types import GrammarExample, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "sv-counterfactual-b2",
        "Om jag hade vetat",
        "B2",
        "Villkor och tid",
        "Resonera om ett annat förflutet.",
        "Ett kontrafaktiskt dåtida villkor uttrycks ofta med hade och supinum, följt av skulle ha och supinum: Om jag hade vetat skulle jag ha ringt. Det föreställda utfallet skiljs från vad som faktiskt hände. I samtal kan hade användas även i följden: då hade jag ringt.",
        rules=[
            "Skilj tänkt dåtid från ett öppet framtida villkor.",
            "Bevara vem som visste och vem som skulle handla.",
        ],
        examples=[
            GrammarExample("Om tåget hade gått i tid skulle vi ha hunnit."),
            GrammarExample("Jag hade följt med om du hade frågat."),
        ],
    ),
    GrammarTopic(
        "sv-future-past-b2",
        "Skulle och framtid i dåtid",
        "B2",
        "Verb och tid",
        "Tolka skulle utan att anta att planen genomfördes.",
        "Skulle kan ange framtid från en dåtida utgångspunkt: I måndags sa hon att hon skulle resa på tisdagen. Meningen berättar om planen, inte säkert om resans genomförande. Skulle används också hypotetiskt och artigt; läs sammanhanget innan du väljer tolkning.",
        rules=[
            "En återgiven avsikt är inte bevis för ett faktiskt resultat.",
            "Skulle ha rest kan beskriva en utebliven plan, men andra läsningar finns i återgivning.",
        ],
        examples=[
            GrammarExample("Vi skulle ses vid tre, men mötet ställdes in."),
            GrammarExample("Hon berättade att arbetet skulle börja veckan därpå."),
        ],
    ),
    GrammarTopic(
        "sv-passive-alternatives-b2",
        "Öppnas, blir öppnad och är öppen",
        "B2",
        "Verb och perspektiv",
        "Skilj process från förändring och tillstånd.",
        "S-passiv kan uttrycka en handling eller en generell ordning. Bli med particip betonar ofta en förändring eller händelse. Vara med particip beskriver ofta ett resultat eller tillstånd. Öppen är ett adjektiv: Butiken är öppen. Skillnaderna är inte en absolut regel; sammanhang och verbets betydelse spelar roll.",
        rules=[
            "Particip efter bli och vara kan behöva kongruens: dörrarna blev stängda.",
            "Behåll utföraren om ansvar är viktigt.",
        ],
        examples=[
            GrammarExample("Ansökan behandlas nästa vecka."),
            GrammarExample("Dörrarna blev låsta vid åtta och var fortfarande låsta vid nio."),
        ],
        related=["sv-passive-b1", "sv-participle-b1"],
    ),
    GrammarTopic(
        "sv-present-participle-b2",
        "En leende person och ett växande behov",
        "B2",
        "Particip",
        "Beskriv en pågående egenskap med presensparticip.",
        "Presensparticip slutar ofta på -ande eller -ende: arbetande, gående. Formen böjs inte efter genus eller antal. Den kan beskriva en pågående handling eller en egenskap: en leende person, ett växande behov. Svenska använder inte vara och presensparticip som en allmän motsvarighet till engelsk pågående form.",
        rules=[
            "Säg Jag arbetar för en vanlig pågående handling.",
            "Låt participets samband med det beskrivna ordet vara tydligt.",
        ],
        examples=[
            GrammarExample("Vi mötte två skrattande barn."),
            GrammarExample("Det finns ett ökande intresse för kursen."),
        ],
    ),
    GrammarTopic(
        "sv-object-shift-b2",
        "Jag såg henne inte",
        "B2",
        "Ordföljd",
        "Känn igen placeringen av obetonade objektspronomen.",
        "Ett obetonat objektspronomen kan stå före inte när huvudverbet är böjt och står före objektet: Jag såg henne inte. Med ett kvarstående huvudverb efter hjälpverbet blir det Jag har inte sett henne. Ett betonat pronomen kan stå senare: Jag såg inte HENNE, utan någon annan. Betoning och struktur påverkar valet.",
        rules=[
            "Flytta inte pronomenet förbi ett oböjt huvudverb.",
            "Båda ordföljderna kan vara möjliga med olika fokus; undvik mekaniska rättningar.",
        ],
        examples=[
            GrammarExample("Jag känner honom inte."),
            GrammarExample("Jag kan inte hjälpa honom."),
        ],
    ),
    GrammarTopic(
        "sv-scope-b2",
        "Alla kom inte och ingen kom",
        "B2",
        "Betydelse och räckvidd",
        "Bevara vad negationen omfattar.",
        "Alla kom inte betyder ofta att inte alla kom; det säger inte att ingen kom. Bara kan avgränsa olika led: Bara Sara läste rapporten och Sara läste bara rapporten har olika fokus. Skriv tydligare om ett beslut eller en sammanfattning annars kan få fel betydelse.",
        rules=[
            "Inte alla är svagare än ingen.",
            "Placera bara vid det led som ska avgränsas eller förtydliga med en omskrivning.",
        ],
        examples=[
            GrammarExample("Inte alla deltagare svarade; några avstod."),
            GrammarExample("Bara två av förslagen har granskats."),
        ],
    ),
    GrammarTopic(
        "sv-relative-preposition-b2",
        "Frågan som vi talade om",
        "B2",
        "Bisatser",
        "Använd relativsatser med preposition.",
        "I naturlig svenska står prepositionen ofta sist: frågan som vi talade om. Mer formellt kan man skriva frågan om vilken vi talade. Prepositionen följer verbets konstruktion och får inte försvinna: tala om något. Vilken böjs efter referenten: vilket, vilka.",
        rules=[
            "Som kan inte användas direkt efter en framförställd preposition i detta mönster.",
            "En preposition sist är inte automatiskt fel eller slarvigt.",
        ],
        examples=[
            GrammarExample("Det är kollegan som jag samarbetar med."),
            GrammarExample("De villkor under vilka stödet ges måste vara tydliga."),
        ],
    ),
    GrammarTopic(
        "sv-cleft-b2",
        "Det var Sara som ringde",
        "B2",
        "Informationsstruktur",
        "Framhäv en deltagare, tid eller plats.",
        "En utbrytning med det är eller det var lyfter fram ett led: Det var Sara som ringde. Formen kan korrigera en felaktig uppfattning eller besvara en fråga om vem. Det var igår som hon ringde lyfter i stället fram tiden. Fokus ändras, men deltagare och händelse ska bevaras.",
        rules=[
            "Välj fokus efter frågan i samtalet.",
            "Använd som när det utbrutna ledet är subjekt.",
        ],
        examples=[
            GrammarExample("Det var inte priset som avgjorde valet."),
            GrammarExample("Det är på fredag som vi ska träffas."),
        ],
    ),
    GrammarTopic(
        "sv-evidential-b2",
        "Sägs, lär och enligt",
        "B2",
        "Källor och modalitet",
        "Markera att en uppgift kommer från någon annan.",
        "Enligt rapporten anger en källa. Sägs och lär kan markera återgiven information utan att skribenten själv garanterar den: Hon lär vara bortrest. Lär kan också vara presens av lära i andra konstruktioner. Skilj källa, bedömning och bekräftat faktum.",
        rules=[
            "Ta inte bort källmarkören när du sammanfattar en obekräftad uppgift.",
            "Enligt anger vem uppgiften tillskrivs, inte att den är sann.",
        ],
        examples=[
            GrammarExample("Enligt kommunen öppnar badet i juni."),
            GrammarExample("Förslaget sägs ha brett stöd."),
        ],
    ),
    GrammarTopic(
        "sv-epistemic-b2",
        "Måste, kan och bör som bedömning",
        "B2",
        "Modalitet",
        "Uttryck hur säker en slutsats är.",
        "Måste kan markera en stark slutsats: Hon måste ha glömt mötet. Kan anger möjlighet: Hon kan ha glömt det. Bör kan uttrycka en förväntan: Brevet bör vara framme nu. Samma verb kan ha krav- eller tillåtelsebetydelse i andra sammanhang. En modal slutsats är inte en direkt observation.",
        rules=[
            "Håll isär epistemisk bedömning och praktiska krav.",
            "Kan inte ha betyder en bedömd omöjlighet, inte ett förbud i efterhand.",
        ],
        examples=[
            GrammarExample("Det kan ha blivit ett missförstånd."),
            GrammarExample("Med den adressen bör brevet komma rätt."),
        ],
    ),
    GrammarTopic(
        "sv-concessive-condition-b2",
        "Även om, även när och oavsett om",
        "B2",
        "Samband",
        "Skilj möjliga hinder från faktiska tillfällen.",
        "Även om kan göra följden oberoende av ett tänkt villkor. Även när anknyter till tillfällen då något händer. Oavsett om framhäver att alternativen inte ändrar följden. Formuleringarna kan överlappa men gör olika antaganden om situationen.",
        rules=[
            "Byt inte om mot när om det gör en osäker händelse säker.",
            "Ange båda alternativen när det behövs för tydlighet.",
        ],
        examples=[
            GrammarExample("Vi håller öppet även om det regnar."),
            GrammarExample("Oavsett om du tackar ja eller nej vill vi ha svar."),
        ],
    ),
    GrammarTopic(
        "sv-unless-b2",
        "Om inte och såvida inte",
        "B2",
        "Villkor",
        "Ange ett undantag från en plan eller regel.",
        "Såvida inte betyder ungefär om inte och introducerar ett undantagsvillkor: Vi åker imorgon, såvida inte tåget ställs in. Det garanterar inte att undantaget inträffar. Med dubbla negationer blir villkoret lätt otydligt; pröva att uttrycka huvudregel och undantag var för sig.",
        rules=[
            "Kontrollera vad som gäller när undantaget inte inträffar.",
            "Såvida inte inleder en bisats.",
        ],
        examples=[
            GrammarExample("Avtalet förlängs om ingen säger upp det."),
            GrammarExample("Jag deltar, såvida inte mötet flyttas till måndag."),
        ],
    ),
    GrammarTopic(
        "sv-gradual-b2",
        "Ju mer, desto bättre",
        "B2",
        "Jämförelse",
        "Beskriv hur två förändringar hänger ihop.",
        "Ju … desto kopplar två grader till varandra: Ju mer jag övar, desto säkrare blir jag. Ju-delen har bisatsliknande ordföljd. I desto-delen följer det böjda verbet efter jämförelseledet. Konstruktionen uttrycker ett samband, inte automatiskt ett vetenskapligt bevis för orsak.",
        rules=[
            "Båda leden behöver en jämförande betydelse.",
            "Skriv desto säkrare blir jag, inte desto jag blir säkrare.",
        ],
        examples=[
            GrammarExample("Ju längre vi väntar, desto dyrare blir det."),
            GrammarExample("Ju färre byten, desto enklare resa."),
        ],
    ),
    GrammarTopic(
        "sv-nominalization-b2",
        "Från att besluta till ett beslut",
        "B2",
        "Text och stil",
        "Växla mellan verb och substantiv utan att dölja ansvar.",
        "Nominalisering gör en handling till ett substantivuttryck: att granska – en granskning. Det kan binda ihop en text, men många nominaliseringar kan göra den tung. Kommunens granskning säger vem som granskar, medan granskningen ensam kan dölja ansvar. Återge inte ett planerat arbete som redan genomfört.",
        rules=[
            "Behåll deltagare och tidsförhållanden vid omskrivning.",
            "Välj verb när läsaren behöver veta vem som gör vad.",
        ],
        examples=[
            GrammarExample("Kommunen granskar förslaget. Granskningen tar två veckor."),
            GrammarExample("Vi föreslår en ändring, men inget beslut är fattat."),
        ],
    ),
    GrammarTopic(
        "sv-reference-b2",
        "Den, det, detta och vilket",
        "B2",
        "Textbindning",
        "Gör hänvisningar till tidigare information tydliga.",
        "Den och det kan syfta på substantiv, medan detta och vilket också kan syfta på en hel föregående situation. Han kom för sent, vilket förvånade oss handlar om förseningen. Om flera möjliga referenter finns, upprepa hellre ett relevant substantiv än att lämna läsaren att gissa.",
        rules=[
            "Hela satser återupptas normalt med neutrala former som det eller vilket.",
            "Närmaste substantiv är inte alltid den avsedda referenten.",
        ],
        examples=[
            GrammarExample("Bussen ställdes in. Det gjorde resan svårare."),
            GrammarExample("Hon ändrade tiden, vilket ingen hade räknat med."),
        ],
    ),
    GrammarTopic(
        "sv-restriction-b2",
        "Endast om och om",
        "B2",
        "Villkor och logik",
        "Skilj nödvändiga villkor från tillräckliga.",
        "Du får ersättning endast om du har kvitto gör kvittot nödvändigt, men säger inte att kvittot är det enda kravet. Om du har kvitto får du ersättning presenterar kvittot som tillräckligt i den aktuella formuleringen. Läs villkorsord noggrant i avtal och instruktioner.",
        rules=[
            "Endast om kan inte bytas mot om utan att logiken kan ändras.",
            "Sök efter ytterligare villkor innan du drar slutsatser om rättigheter.",
        ],
        examples=[
            GrammarExample("Du får delta endast om du är anmäld."),
            GrammarExample("Om minst tio anmäler sig blir kursen av."),
        ],
    ),
    GrammarTopic(
        "sv-particle-meaning-b2",
        "Ta upp, ta över och ta sig an",
        "B2",
        "Verb och betydelse",
        "Välj rätt konstruktion i samtal om arbete.",
        "Partiklar och reflexiva led skapar olika betydelser: ta upp en fråga betyder att börja behandla den, ta över ett arbete att överta det och ta sig an en uppgift att börja arbeta med den. Lär varje konstruktion med dess objekt och register. Ett utbyte av partikel kan ändra ansvar och avsikt.",
        rules=[
            "Spara hela uttrycket med typiskt objekt.",
            "Skilj konkret och överförd betydelse i sammanhanget.",
        ],
        examples=[
            GrammarExample("Jag tar upp frågan på mötet."),
            GrammarExample("Vem tar över uppgiften när du slutar?"),
        ],
    ),
    GrammarTopic(
        "sv-argument-connectors-b2",
        "Däremot, dessutom och däremellan",
        "B2",
        "Textbindning",
        "Välj samband efter argumentets funktion.",
        "Däremot markerar kontrast, dessutom lägger till ett argument och däremellan anger en position mellan något i tid eller rum. Därmed anger ofta följd eller medel. Sambandsord gör inte ett argument logiskt av sig självt; kontrollera relationen mellan påståendena.",
        rules=[
            "Ett inledande adverb följs av verbet i en vanlig huvudsats.",
            "Använd däremot när den andra uppgiften verkligen kontrasterar mot den första.",
        ],
        examples=[
            GrammarExample("Rummet är litet. Däremot är läget bra."),
            GrammarExample("Priset är lägre. Dessutom ingår frukost."),
        ],
    ),
    GrammarTopic(
        "sv-impersonal-b2",
        "Det behövs fler platser",
        "B2",
        "Satsmönster",
        "Presentera behov och bedömningar naturligt.",
        "Det kan vara formellt subjekt när nytt innehåll kommer senare: Det behövs fler platser. Det är viktigt att du svarar låter en att-sats bära det egentliga innehållet. Skriv inte ett extra personligt subjekt om konstruktionen inte kräver det. Skilj behövs från behöver: Vi behöver hjälp, men det behövs hjälp.",
        rules=[
            "Behövs böjs inte efter antalet platser.",
            "Behöver kräver normalt någon eller något som har behovet.",
        ],
        examples=[
            GrammarExample("Det saknas en bilaga."),
            GrammarExample("Det är svårt att bedöma följderna ännu."),
        ],
    ),
    GrammarTopic(
        "sv-register-b2",
        "Sakligt, vänligt och tydligt",
        "B2",
        "Register och samspel",
        "Anpassa ett önskemål till mottagare och syfte.",
        "Formellt språk behöver inte vara opersonligt eller svårt. Ange ärende, önskemål och eventuell tidsgräns: Jag vill be om ett skriftligt besked senast fredag. Du kan vara vänlig utan att göra ett krav otydligt. Du-tilltal är vanligt också i formella kontakter; ni är inte en generell regel för artighet.",
        rules=[
            "Behåll sakuppgifter när du ändrar ton.",
            "Skilj en begäran om besked från ett påstående om att besked redan utlovats.",
        ],
        examples=[
            GrammarExample("Tack för svaret. Kan ni precisera vilken bilaga som saknas?"),
            GrammarExample("Jag förstår förseningen men behöver ett nytt leveransdatum."),
        ],
    ),
    GrammarTopic(
        "sv-de-dem-b2",
        "De och dem i skrift",
        "B2",
        "Skrift och variation",
        "Skilj pronomenens funktion från uttalet dom.",
        "I neutral standardskrift är de subjekt och dem objekt eller form efter preposition: De hjälper oss; vi hjälper dem. Uttalet är ofta dom, som också förekommer i informell skrift och återgiven dialog. Före som kan konstruktionen behöva analyseras noga; vissa fall har accepterad variation.",
        rules=[
            "Pröva vi och oss som stöd i enkla fall.",
            "De i de nya böckerna är en bestämning och ska inte bytas mot dem.",
        ],
        examples=[
            GrammarExample("De väntar på oss och vi väntar på dem."),
            GrammarExample("Jag köpte de röda skorna."),
        ],
    ),
]
