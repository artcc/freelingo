"""Danish C1 grammar and discourse in practical settings."""

from app.data._types import GrammarExample, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "da-source-attribution-c1",
        "Ifølge, oplyser og angiveligt",
        "C1",
        "Kilder",
        "Vis, hvem der står inde for en oplysning.",
        "Ifølge henviser til en kilde uden i sig selv at bekræfte den. Oplyser knytter et "
        "udsagn til en afsender. Angiveligt markerer ofte afstand til en oplysning, som "
        "skribenten ikke selv har efterprøvet. Valget påvirker læserens tillid og må derfor "
        "ikke ændres tilfældigt i et referat.",
        rules=[
            "Bevar både kilde og eventuel usikkerhed ved en omskrivning.",
            "Angiveligt er ikke et neutralt alternativ til dokumenteret.",
        ],
        examples=[
            GrammarExample("Ifølge viceværten bliver vandet lukket mellem ni og elleve."),
            GrammarExample("Fejlen er angiveligt rettet; vi afventer stadig en prøvekørsel."),
        ],
        related=["da-knowledge-limits-c1"],
    ),
    GrammarTopic(
        "da-inference-modals-c1",
        "Må være, kan være og skulle være",
        "C1",
        "Modalitet",
        "Skeln mellem en slutning, en mulighed og noget, du har hørt.",
        "Må være kan udtrykke en stærk slutning: Lyset er tændt, så nogen må være hjemme. "
        "Kan være åbner en mulighed. Skulle være kan gengive en oplysning med afstand: "
        "Hun skulle være tilbage på mandag. Sammenhængen afgør, om skulle i stedet "
        "handler om en plan eller forventning.",
        rules=[
            "En slutning er ikke det samme som en direkte iagttagelse.",
            "Gengiv ikke et refererende skulle som et ubetinget faktum.",
        ],
        examples=[
            GrammarExample("Det kan være en gammel regning; datoen er svær at læse."),
            GrammarExample("Den nye kasserer skulle være revisor, men jeg har ikke mødt hende."),
        ],
        related=["da-source-attribution-c1"],
    ),
    GrammarTopic(
        "da-knowledge-limits-c1",
        "Så vidt, efter alt at dømme og tilsyneladende",
        "C1",
        "Forbehold",
        "Afgræns dit vidensgrundlag uden at skjule din vurdering.",
        "Så vidt jeg ved afgrænser udsagnet til talerens viden. Efter alt at dømme bygger "
        "en vurdering på de tilgængelige tegn. Tilsyneladende beskriver, hvordan noget "
        "fremtræder, og kan åbne for, at virkeligheden er anderledes. Et nyttigt forbehold "
        "viser, hvad der mangler, ikke blot at taleren er forsigtig.",
        rules=[
            "Placér forbeholdet, så det er klart, hvilken påstand det gælder.",
            "Forklar begrænsningen, når modtageren skal træffe en beslutning.",
        ],
        examples=[
            GrammarExample("Så vidt jeg ved, har bestyrelsen kun godkendt undersøgelsen."),
            GrammarExample("Efter alt at dømme er taget tæt, men loftsrummet er ikke besigtiget."),
        ],
    ),
    GrammarTopic(
        "da-conditional-fronting-c1",
        "Kommer tilbuddet i dag, kan vi nå det",
        "C1",
        "Betingelser",
        "Brug en betingelsessætning uden hvis i en konkret aftale.",
        "En betingelse kan begynde med det finitte verbum: Kommer tilbuddet i dag, kan vi "
        "nå at behandle det. Første del er her ikke et spørgsmål. Når betingelsen står "
        "foran, kommer hovedsætningens finitte verbum før subjektet. Formen er kompakt "
        "og bruges blandt andet i instruktioner og forhandlinger.",
        structure="Betingelse med verbet først + finit verbum + subjekt",
        rules=[
            "Læs betingelse og følge samlet, før du afgør sætningens funktion.",
            "Bevar forskellen mellem kan nå og vil nå ved en omskrivning med hvis.",
        ],
        examples=[
            GrammarExample("Får vi adgang til lokalet fredag, kan arbejdet begynde mandag."),
            GrammarExample("Skulle leveringen blive forsinket, kontakter vi jer straks."),
        ],
        related=["da-unless-boundaries-c1"],
    ),
    GrammarTopic(
        "da-unless-boundaries-c1",
        "Medmindre og kun hvis",
        "C1",
        "Betingelser",
        "Afgræns undtagelser uden at vende aftalens logik om.",
        "Medmindre indfører en undtagelse til det, der ellers gælder. Vi går videre, "
        "medmindre prisen stiger betyder, at en prisstigning kan ændre planen. Vi går "
        "kun videre, hvis prisen falder gør derimod et prisfald til en nødvendig "
        "betingelse. Det siger ikke i sig selv, at prisfaldet er tilstrækkeligt.",
        rules=[
            "Undgå at indsætte en ekstra nægtelse efter medmindre uden grund.",
            "Skeln mellem en nødvendig betingelse og et løfte om handling.",
        ],
        examples=[
            GrammarExample("Vi fastholder datoen, medmindre håndværkeren melder afbud."),
            GrammarExample("Vi bestiller kun materialerne, hvis finansieringen er på plads."),
        ],
    ),
    GrammarTopic(
        "da-concessive-clauses-c1",
        "Selvom og uanset om",
        "C1",
        "Indrømmelse",
        "Anerkend et modhensyn og fasthold en begrundet beslutning.",
        "Selvom sætter et forhold i modsætning til det forventede resultat. Uanset om "
        "gør beslutningen uafhængig af de nævnte muligheder. Selvom hun er erfaren "
        "præsenterer erfaring som et indrømmet forhold; uanset om hun er erfaren "
        "lader spørgsmålet stå åbent. De to konstruktioner er derfor ikke frit udskiftelige.",
        rules=[
            "En indrømmelse er ikke nødvendigvis en tilslutning til modpartens konklusion.",
            "Bevar, om et forhold fremstilles som givet eller som uafklaret.",
        ],
        examples=[
            GrammarExample("Selvom prisen er rimelig, kan vi ikke acceptere betalingsfristen."),
            GrammarExample("Uanset om hun deltager, skal hendes indsigelse fremgå af referatet."),
        ],
    ),
    GrammarTopic(
        "da-passive-accountability-c1",
        "Passiv og synligt ansvar",
        "C1",
        "Aktør og handling",
        "Vælg passiv med omtanke, når en opgave skal fordeles.",
        "Passiv kan lade en sag stå i centrum: Regnskabet gennemgås på tirsdag. Formen "
        "er hensigtsmæssig, hvis aktøren er kendt eller uvigtig. I en opgavefordeling kan "
        "den derimod skjule et manglende tilsagn. En omskrivning til aktiv kræver, at "
        "du faktisk kender den ansvarlige; den må ikke opfinde en aktør.",
        rules=[
            "Spørg hvem, når opfølgningen afhænger af en bestemt person.",
            "Skeln mellem skal behandles, bliver behandlet og er blevet behandlet.",
        ],
        examples=[
            GrammarExample("Der skal indhentes to tilbud; hvem påtager sig opgaven?"),
            GrammarExample("Kassereren gennemgår regnskabet på tirsdag."),
        ],
        related=["da-unpacking-nouns-c1"],
    ),
    GrammarTopic(
        "da-unpacking-nouns-c1",
        "Fra navneordskæde til tydelig handling",
        "C1",
        "Skriftlig fremstilling",
        "Pak tætte formuleringer ud med bevaret tid og ansvar.",
        "Navneord som godkendelse, udsættelse og gennemgang samler handlinger i korte "
        "udtryk. Bestyrelsens forslag om udsættelse af renoveringen indeholder både "
        "en afsender og en foreslået ændring. Bestyrelsen har udsat renoveringen er "
        "ikke en loyal omskrivning: forslaget er blevet til en vedtaget handling.",
        rules=[
            "Bevar forskellen mellem et forslag, en beslutning og en udført handling.",
            "Skriv aktøren ind, når den er oplyst, og efterspørg den ellers.",
        ],
        examples=[
            GrammarExample("Bestyrelsen foreslår, at renoveringen udsættes."),
            GrammarExample("Godkendelsen af lånet afventer bankens vurdering."),
        ],
    ),
    GrammarTopic(
        "da-infinitive-agents-c1",
        "Hvem lover, og hvem skal gøre det?",
        "C1",
        "Infinitiv",
        "Find den underforståede aktør efter love, bede og få.",
        "I Asta lovede Bo at ringe er Asta den, der påtager sig opgaven. I Asta bad Bo "
        "om at ringe er Bo den, der bliver bedt om den. Asta fik Bo til at ringe "
        "fremstiller opkaldet som noget, Asta fik til at ske. Verbet og konstruktionen "
        "styrer både aktørfordeling og graden af gennemførelse.",
        rules=[
            "En anmodning viser ikke i sig selv, at handlingen blev udført.",
            "Brug en fuld ledsætning, hvis den underforståede aktør er uklar.",
        ],
        examples=[
            GrammarExample("Jeg lovede naboen at undersøge sagen, ikke at løse den."),
            GrammarExample("Jeg bad naboen om at kontakte bestyrelsen."),
        ],
    ),
    GrammarTopic(
        "da-cleft-focus-c1",
        "Det er fristen, vi er uenige om",
        "C1",
        "Informationsstruktur",
        "Brug sætningskløvning til at rette den relevante misforståelse.",
        "Det er eller det var kan fremhæve et led, mens resten af sætningen knytter "
        "an til noget kendt. Det er fristen, vi er uenige om retter fokus mod fristen "
        "frem for eksempelvis prisen. Kløvningen er ikke blot pynt; den styrer, "
        "hvilket alternativ modtageren skal overveje.",
        rules=[
            "Fremhæv kun det led, der faktisk skal korrigeres eller kontrasteres.",
            "Som kan udelades i mange objektkløvninger, men ikke bare i en subjektkløvning.",
        ],
        examples=[
            GrammarExample("Det var Mette, der foreslog pausen, ikke mødelederen."),
            GrammarExample("Det er betalingsfristen, vi gerne vil ændre."),
        ],
    ),
    GrammarTopic(
        "da-quantifier-scope-c1",
        "Ikke alle, ingen og ikke nødvendigvis",
        "C1",
        "Rækkevidde",
        "Bevar styrken i et udsagn om grupper og nødvendighed.",
        "Ikke alle afviser, at hele den relevante gruppe er omfattet; det angiver "
        "ikke en bestemt andel. Ingen udelukker hele gruppen. Ikke nødvendigvis "
        "afviser, at en følge er sikker, men udelukker ikke, at den kan indtræffe. "
        "En sammenfatning må ikke gøre disse svagere udsagn stærkere.",
        rules=[
            "Sæt ikke lighedstegn mellem ikke alle og de færreste.",
            "Gør tydeligt, hvilken gruppe eller følge nægtelsen vedrører.",
        ],
        examples=[
            GrammarExample("Ikke alle beboere har svaret; vi kender endnu ikke fordelingen."),
            GrammarExample("En lavere pris giver ikke nødvendigvis en lavere samlet udgift."),
        ],
    ),
    GrammarTopic(
        "da-only-focus-c1",
        "Kun, også og netop",
        "C1",
        "Fokus",
        "Vis, hvilket led du afgrænser eller føjer til.",
        "Kun afgrænser muligheder, også tilføjer noget, og netop kan fremhæve et "
        "særligt relevant led. Placering og tryk spiller sammen. Kun Lea læste bilaget "
        "afgrænser læserne; Lea læste kun bilaget afgrænser normalt det læste. Ved "
        "tvetydighed er en udbygget formulering mere pålidelig end en flytning alene.",
        rules=[
            "Kontrollér, hvad fokusordet gælder, før du forkorter en formulering.",
            "Brug en eksplicit kontrast, når trykket ikke kan høres i skrift.",
        ],
        examples=[
            GrammarExample("Kun driften er medregnet; anskaffelsen kommer oveni."),
            GrammarExample("Det er netop den usikkerhed, vi bør nævne."),
        ],
        related=["da-cleft-focus-c1"],
    ),
    GrammarTopic(
        "da-jo-vel-vist-nok-c1",
        "Jo, vel, vist og nok",
        "C1",
        "Samtalepartikler",
        "Afstem viden, forventning og sandsynlighed med samtalepartneren.",
        "Jo fremstiller ofte noget som fælles eller genkendelig viden. Vel kan søge "
        "tilslutning til en forventning. Vist markerer ofte usikker viden, mens nok "
        "kan udtrykke en sandsynlig vurdering eller beroligelse. Tonefald og placering "
        "kan ændre virkningen; ordene har ikke én fast betydning hver.",
        rules=[
            "Jo kan virke pressende, hvis modparten netop bestrider oplysningen.",
            "Skeln mellem nok som sandsynlighed og nok som tilstrækkelig mængde.",
        ],
        examples=[
            GrammarExample("Du har vel fået den nye dagsorden?"),
            GrammarExample("Hun er vist på kursus i dag. Vi finder nok en anden løsning."),
        ],
    ),
    GrammarTopic(
        "da-da-ellers-c1",
        "Da og ellers som reaktion",
        "C1",
        "Samtalepartikler",
        "Forstå overraskelse og brud med en forventning.",
        "Da kan i en replik fremhæve noget som indlysende eller udtrykke overraskelse: "
        "Det er da flot! Ellers kan pege på en modsætning til en tidligere forventning: "
        "Jeg havde ellers forstået, at mødet var aflyst. Begge ord afhænger af "
        "sammenhængen og kan lyde venlige, undrende eller skarpe.",
        rules=[
            "Skeln mellem ellers som forventningsbrud og ellers i betydningen hvis ikke.",
            "Spørg ind til hensigten, hvis tonefaldet og situationen trækker i hver sin retning.",
        ],
        examples=[
            GrammarExample("Nå, jeg troede ellers, at du havde fri om fredagen."),
            GrammarExample("Det kan vi da godt undersøge sammen."),
        ],
    ),
    GrammarTopic(
        "da-polite-distance-c1",
        "Jeg ville høre, om det kunne lade sig gøre",
        "C1",
        "Høflighed og register",
        "Brug tidslig og modal afstand uden at udviske dit budskab.",
        "Ville og kunne kan i en aktuel henvendelse skabe høflig afstand, selv om "
        "formen ligner fortid. Jeg ville høre, om fristen kunne rykkes er en "
        "anmodning nu, ikke nødvendigvis en opgivet hensigt. Et høfligt afslag bør "
        "stadig gøre klart, hvad der ikke er muligt, og hvad der eventuelt tilbydes.",
        rules=[
            "En forsigtig formulering er ikke det samme som et løfte.",
            "Tilpas graden af indirekte sprog til relation og situation.",
        ],
        examples=[
            GrammarExample("Jeg ville høre, om vi kunne dele betalingen i to rater."),
            GrammarExample("Jeg kan desværre ikke nå fredag, men jeg kan sende et udkast mandag."),
        ],
    ),
    GrammarTopic(
        "da-narrative-viewpoint-c1",
        "Fortid, tilbageblik og levende nutid",
        "C1",
        "Fortælling",
        "Styr tidslinjen, når du fortæller en oplevelse.",
        "Datid kan bære fortællingens forløb, og førdatid markerer noget forud for et "
        "fortidigt holdepunkt. Historisk nutid kan gøre en episode nærværende: Så står "
        "jeg dér uden nøgle. Et skift er ikke i sig selv en fejl, men modtageren skal "
        "kunne følge, hvornår du forlader og vender tilbage til hovedforløbet.",
        rules=[
            "Brug tidsmarkører ved tilbageblik, hvis rækkefølgen ellers bliver uklar.",
            "Lad et perspektivskift have en tydelig fortællende funktion.",
        ],
        examples=[
            GrammarExample("Jeg kom hjem klokken ti. Jeg havde lagt nøglen på køkkenbordet."),
            GrammarExample("Og så står jeg dér i regnen, mens katten kigger på mig indefra."),
        ],
    ),
    GrammarTopic(
        "da-contextual-irony-c1",
        "Når rosen ikke skal læses bogstaveligt",
        "C1",
        "Pragmatik",
        "Genkend mulig ironi uden at gætte på en fælles hensigt.",
        "Ironi kan opstå, når ordene står i tydelig modsætning til situationen. "
        "Sikke en god start kan efter et uheld udtrykke frustration snarere end ros. "
        "Tonefald, relation og fælles viden støtter tolkningen, men den er ikke givet "
        "af ordene alene. Selvironi retter ofte humoren mod taleren selv.",
        rules=[
            "Beskriv en ironisk læsning som mulig, når konteksten ikke afgør den.",
            "En vittig hensigt gør ikke nødvendigvis virkningen venlig.",
        ],
        examples=[
            GrammarExample("Jeg glemte både nøgler og telefon. Flot klaret af mig."),
            GrammarExample("Mener du det som ros, eller er du utilfreds med løsningen?"),
        ],
    ),
    GrammarTopic(
        "da-spoken-resumption-c1",
        "Den regning, den må vi lige se på",
        "C1",
        "Talesprog",
        "Følg tema og genoptagelse i en spontan samtale.",
        "Et led kan placeres uden for selve sætningen og genoptages med et pronomen: "
        "Den regning, den må vi lige se på. Det hjælper taleren med at etablere et tema "
        "og modtageren med at følge det. I et kort referat vil Den regning må vi se på "
        "ofte være mere kompakt. Forskellen handler om genre, ikke om at taleformen "
        "generelt er ugrammatisk.",
        rules=[
            "Bevar temaet og aktøren, når du redigerer tale til skrift.",
            "Skeln mellem et udskilt tema og et almindeligt led i forfeltet.",
        ],
        examples=[
            GrammarExample("Min nabo, hun har allerede meldt sig til arbejdsdagen."),
            GrammarExample("Det finder vi ud af, det med adgangskoden."),
        ],
    ),
    GrammarTopic(
        "da-cohesive-reference-c1",
        "Det, dette og den beslutning",
        "C1",
        "Tekstbinding",
        "Gør klart, hvad næste sætning bygger videre på.",
        "Det kan henvise til en ting, en handling eller et helt tidligere udsagn. "
        "Hvis flere mulige henvisninger konkurrerer, kan et præcist navneord gøre "
        "teksten tydelig: afslaget, beregningen eller den foreslåede udsættelse. "
        "Navngivningen skal passe til indholdet; et forslag bliver ikke en beslutning, "
        "blot fordi teksten har brug for et kort henvisningsled.",
        rules=[
            "Vælg et henvisningsled, der bevarer oplysningens status.",
            "Gentag hellere et præcist ord end at skabe uklarhed med det.",
        ],
        examples=[
            GrammarExample("Udvalget foreslog at sænke gebyret. Forslaget behandles i juni."),
            GrammarExample(
                "Hun afviste beregningen, men ikke projektet. Afvisningen skal begrundes."
            ),
        ],
    ),
    GrammarTopic(
        "da-relative-comment-c1",
        "Som og hvilket: ting eller hel sætning?",
        "C1",
        "Ledsætninger",
        "Skeln mellem en beskrivelse og en kommentar til et forløb.",
        "Som knytter normalt en relativsætning til et nominalt led. Hvilket kan også "
        "indlede en kommentar til hele den foregående sætning: Mødet blev flyttet, "
        "hvilket gav os mere tid. Her er det flytningen, ikke et bestemt navneord, "
        "der gav mere tid. En omskrivning med det forhold, at kan tydeliggøre sammenhængen.",
        rules=[
            "Afgør, om kommentaren gælder en genstand eller hele udsagnet.",
            "Sæt en sætningskommentar efter et tydeligt afsluttet udsagn.",
        ],
        examples=[
            GrammarExample("Vi modtog et bilag, som forklarede beregningen."),
            GrammarExample("Bilaget kom først efter mødet, hvilket gjorde drøftelsen vanskelig."),
        ],
        related=["da-cohesive-reference-c1"],
    ),
    GrammarTopic(
        "da-register-recasting-c1",
        "Samme indhold, anden modtager",
        "C1",
        "Register",
        "Tilpas formuleringen uden at ændre tilsagnet.",
        "Et mundtligt Det kan jeg godt lige kigge på kan i en arbejdsbesked blive til "
        "Jeg kan gennemgå det kort. Det er ikke det samme som Jeg godkender det. "
        "Når tale omsættes til referat, skal småord, modalitet og begrænsninger "
        "vurderes for deres funktion, ikke blot slettes som fyld.",
        rules=[
            "Bevar, om taleren tilbyder en undersøgelse, en vurdering eller et resultat.",
            "Klarsprog kan være præcist og professionelt uden tunge navneordskæder.",
        ],
        examples=[
            GrammarExample("Jeg ser på det i morgen, men jeg kan ikke love et svar samme dag."),
            GrammarExample(
                "Sagen gennemgås i morgen; tidspunktet for svaret er endnu ikke aftalt."
            ),
        ],
        related=["da-polite-distance-c1", "da-unpacking-nouns-c1"],
    ),
]
