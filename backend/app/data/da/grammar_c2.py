"""Danish C2 grammar for interpretation, editing and delicate interaction."""

from app.data._types import GrammarExample, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "da-mixed-counterfactuals-c2",
        "En anden fortid, en anden nutid",
        "C2",
        "Kontrafaktiske forløb",
        "Hold årsagens og følgens tidspunkter adskilt.",
        "Havde vi isoleret loftet sidste år, ville vi bruge mindre varme nu forbinder "
        "en tænkt ændring i fortiden med en tænkt følge i nutiden. Ville have brugt "
        "mindre varme sidste vinter flytter derimod følgen tilbage. Den betingede "
        "form er ikke en oplysning om, at arbejdet eller besparelsen faktisk fandt sted.",
        rules=[
            "Bestem tidspunktet for både betingelse og følge før en omskrivning.",
            "Bevar forskellen mellem ville og kunne, også i tænkte forløb.",
        ],
        examples=[
            GrammarExample("Hvis vi havde gemt tegningerne, kunne vi sammenligne løsningerne nu."),
            GrammarExample("Havde vi bestilt tidligere, ville varerne være kommet inden jul."),
        ],
        related=["da-perfect-infinitive-c2"],
    ),
    GrammarTopic(
        "da-skulle-have-c2",
        "Skulle have: plan, kritik eller rygte?",
        "C2",
        "Modalitet",
        "Afgør funktionen ud fra kilde, tidsforløb og samtalehandling.",
        "Han skulle have ringet kan betegne en forventet handling, en bebrejdelse "
        "eller en ubekræftet oplysning om et opkald. Fortsættelser som men glemte det, "
        "før han traf beslutningen og ifølge receptionisten støtter forskellige "
        "læsninger. Formen alene afgør hverken, om opkaldet skete, eller om taleren "
        "kritiserer personen.",
        rules=[
            "Udled ikke manglende gennemførelse af skulle have uden kontekst.",
            "Angiv kilden, når en refererende læsning ellers kan lyde som kritik.",
        ],
        examples=[
            GrammarExample("Hun skulle have åbnet mødet, men blev syg om morgenen."),
            GrammarExample(
                "Han skulle have sendt brevet i går; sekretæren siger, at hun så ham "
                "lægge det i postkassen.",
                note="Taleren gengiver en oplysning fra sekretæren uden selv at bekræfte den.",
            ),
            GrammarExample(
                "Det var en fejl at beslutte det alene; han skulle have ringet først.",
                note="Taleren kritiserer, at opkaldet ikke kom før beslutningen.",
            ),
        ],
        related=["da-inference-modals-c1"],
    ),
    GrammarTopic(
        "da-perfect-infinitive-c2",
        "At have gjort noget før et holdepunkt",
        "C2",
        "Infinitiv og tid",
        "Bevar afsluttethed og tidsrelation i komprimerede udsagn.",
        "Perfektum infinitiv består af have eller være sammen med et perfektum "
        "participium, ofte med at foran: Hun hævder at have afleveret nøglen. "
        "Handlingen placeres før det relevante holdepunkt, mens hævder bevarer "
        "kildeafstanden. Efter et modalverbum udelades at: Hun må have afleveret nøglen. "
        "I Han regner med "
        "at være rejst inden fredag ligger holdepunktet fremme i tiden; formen er "
        "ikke bundet til fortid i forhold til taletidspunktet.",
        rules=[
            "Bevar både hjælpeverbum og tidsmarkør ved udfoldning til en ledsætning.",
            "At have afleveret beviser ikke, at en fremsat påstand er sand.",
        ],
        examples=[
            GrammarExample("Hun benægter at have modtaget påmindelsen."),
            GrammarExample("Vi forventer at have afsluttet gennemgangen inden mødet."),
        ],
    ),
    GrammarTopic(
        "da-presupposed-background-c2",
        "Igen, stadig og indbyggede præmisser",
        "C2",
        "Pragmatik",
        "Opdag den baggrund, et udsagn beder dig acceptere.",
        "Hvorfor har I igen udsat afstemningen? fremstiller en tidligere udsættelse "
        "som baggrund. Stadig kan tilsvarende forudsætte, at en tilstand har varet ved. "
        "Hvis denne baggrund er omstridt, kan et direkte svar på hvorfor utilsigtet "
        "acceptere den. Skeln mellem at svare på spørgsmålet og at korrigere præmissen.",
        rules=[
            "Undersøg både det sagte og den baggrund, formuleringen tager for givet.",
            "Afvis præmissen konkret frem for blot at afvise samtalen.",
        ],
        examples=[
            GrammarExample(
                "Afstemningen er ikke udsat igen; den har hele tiden været sat til juni."
            ),
            GrammarExample("Når du siger stadig, hvilken tidligere aftale henviser du så til?"),
        ],
    ),
    GrammarTopic(
        "da-corrective-negation-c2",
        "Ikke en besparelse, men en udskydelse",
        "C2",
        "Negation og betegnelser",
        "Ret en kategorisering uden at benægte selve hændelsen.",
        "Ikke kan rette et ordvalg eller en vurdering snarere end at benægte, at noget "
        "er sket. Det er ikke en besparelse, men en udskydelse accepterer, at betalingen "
        "ændres, men bestrider dens kategorisering. I Det var ikke godt; det var "
        "fremragende afvises en for svag vurdering, ikke kvaliteten.",
        rules=[
            "Læs rettelsen efter men eller pausen, før du bestemmer nægtelsens rækkevidde.",
            "Forklar, hvilken del af beskrivelsen du korrigerer.",
        ],
        examples=[
            GrammarExample("Jeg afviser ikke opgaven; jeg afviser den foreslåede tidsplan."),
            GrammarExample("Det er ikke en rabat, men et lån, der skal betales tilbage."),
        ],
    ),
    GrammarTopic(
        "da-cancellable-inference-c2",
        "Det antydede kan trækkes tilbage",
        "C2",
        "Samtaleslutninger",
        "Skeln mellem logisk indhold og en rimelig forventning.",
        "Nogle har svaret antyder ofte, at ikke alle har svaret, fordi taleren ellers "
        "kunne have valgt alle. Antydningen kan ophæves: nogle, måske endda alle. "
        "Det gør ikke det oprindelige udsagn selvmodsigende. En tolkning bygger "
        "på både ordvalg og situation og må ikke uden videre blive til en fast kendsgerning.",
        rules=[
            "Prøv, om et tillæg kan ophæve antydningen uden at modsige udsagnet.",
            "Skeln mellem et ubesvaret spørgsmål og en indirekte, men tydelig afvisning.",
        ],
        examples=[
            GrammarExample("Flere har læst udkastet; om det gælder alle, ved jeg ikke."),
            GrammarExample("Jeg har et møde klokken seks, men jeg kan godt nå kaffen inden da."),
        ],
    ),
    GrammarTopic(
        "da-nested-exceptions-c2",
        "Undtagelser inde i betingelser",
        "C2",
        "Regler og aftaler",
        "Gør en tæt regel anvendelig uden at udvide dens undtagelser.",
        "En regel kan indeholde både en undtagelse og en betingelse for undtagelsen: "
        "Lokalet må normalt kun bruges indtil klokken 22. Lukkede arrangementer må dog "
        "fortsætte senere, men kun hvis bestyrelsen har godkendt det. Her er både arrangementets "
        "type og godkendelsen nødvendige for undtagelsen. Del reglen op i hovedregel, "
        "relevant gruppe og ekstra krav, før du omskriver den.",
        rules=[
            "Bevar, om betingelser skal være opfyldt samtidig eller hver for sig.",
            "Spørg om rækkevidden, hvis en undtagelse kan knytte sig til flere led.",
        ],
        examples=[
            GrammarExample(
                "Ansøgningen skal sendes digitalt. Ansøgere uden digital adgang må dog sende "
                "den på papir, hvis det er aftalt med sagsbehandleren."
            ),
            GrammarExample(
                "Gæster må overnatte i højst tre døgn, dog længere med særskilt tilladelse."
            ),
        ],
    ),
    GrammarTopic(
        "da-modal-scope-c2",
        "Må ikke, behøver ikke og kan undlade",
        "C2",
        "Forpligtelse og rækkevidde",
        "Bevar forskellen mellem et forbud og fraværet af en pligt.",
        "Må ikke indfører normalt et forbud. Behøver ikke ophæver nødvendighed eller "
        "pligt uden at forbyde handlingen. Kan undlade fremstiller en mulighed for "
        "ikke at handle. I lange bestemmelser skal du desuden afgøre, om modaliteten "
        "gælder alle deltagere, en undergruppe eller en bestemt situation.",
        rules=[
            "Omskriv ikke en fritagelse som et forbud.",
            "Et ikke nødvendigvis krævet bilag kan stadig være påkrævet i bestemte tilfælde.",
        ],
        examples=[
            GrammarExample(
                "Ansøgere med en gyldig godkendelse behøver ikke indsende bilaget igen."
            ),
            GrammarExample("Bilaget må ikke indeholde andre beboeres personoplysninger."),
        ],
        related=["da-quantifier-scope-c1", "da-nested-exceptions-c2"],
    ),
    GrammarTopic(
        "da-free-indirect-view-c2",
        "Dækket direkte tale og farvet fortælling",
        "C2",
        "Perspektiv",
        "Følg en figurs vurdering uden at gøre den til fortællerens sandhed.",
        "Dækket direkte tale kan lade en figurs spørgsmål, ordvalg eller værdier "
        "træde frem uden et indledende tænkte hun. Fortællingen kan blive i tredje "
        "person og datid, mens vurderingen tilhører figuren. Sammenhængen er afgørende; "
        "et følelsesladet ord er ikke alene bevis for et bestemt perspektiv.",
        rules=[
            "Find støtte i figurens situation og den omgivende fortælling.",
            "Skeln mellem forfatter, fortæller og figur, når du forklarer en vurdering.",
        ],
        examples=[
            GrammarExample("Liv stirrede på regningen. Skulle hun nu betale for deres sjusk?"),
            GrammarExample("Han lagde brevet fra sig. Så meget for den lovede åbenhed."),
        ],
    ),
    GrammarTopic(
        "da-nok-men-c2",
        "Nok dygtig, men ikke den rette",
        "C2",
        "Argumentation",
        "Fortolk nok som indrømmelse og vurder argumentets retning.",
        "I Hun er nok dygtig, men hun mangler lokalkendskab kan nok indrømme en "
        "egenskab, mens men fremhæver et modhensyn. Det er ikke nødvendigvis et "
        "usikkert gæt om dygtigheden. Argumentets videre retning ligger ofte efter "
        "men, men den første del bliver ikke dermed trukket tilbage.",
        rules=[
            "Skeln mellem sandsynligheds-nok og indrømmende nok ud fra fortsættelsen.",
            "Bevar begge vurderinger i et loyalt referat.",
        ],
        examples=[
            GrammarExample("Det er nok den billigste løsning, men vedligeholdelsen bliver dyr."),
            GrammarExample("Jeg forstår nok din bekymring, men deler ikke din konklusion."),
        ],
        related=["da-jo-vel-vist-nok-c1"],
    ),
    GrammarTopic(
        "da-echo-and-distance-c2",
        "Når man gentager modpartens egne ord",
        "C2",
        "Humor og distance",
        "Genkend et ekko som citat, afprøvning eller kritik.",
        "En gentagelse kan vise, at et udtryk tilhører en anden stemme. Et hurtigt "
        "ærinde, siger du, mens vi står her på tredje time kan tage ironisk afstand "
        "fra beskrivelsen. Anførselstegn kan markere samme distance i skrift, men "
        "hverken gentagelse eller tegn fastlægger alene en hånlig hensigt.",
        rules=[
            "Afklar, om taleren citerer, spørger til eller kritiserer udtrykket.",
            "Tilpas et humoristisk svar til relationen og modtagerens reaktion.",
        ],
        examples=[
            GrammarExample("Så det var altså den 'lille justering', der krævede tre ekstra møder."),
            GrammarExample(
                "Når du siger fleksibel, mener du så, at arbejdstiden kan ændres dagligt?"
            ),
        ],
    ),
    GrammarTopic(
        "da-conversational-repair-c2",
        "Rettelse uden at miste samtalen",
        "C2",
        "Interaktion",
        "Ret formulering, hensigt eller virkning med tydelig afgrænsning.",
        "Altså, eller rettere og det kom forkert ud kan indlede en selvrettelse. "
        "Rettelsen bør vise, hvad der erstattes, og hvad der stadig gælder. Efter "
        "en uheldig vittighed kan en forklaring af hensigten kombineres med ansvar "
        "for virkningen; Det var bare for sjov kan derimod lyde som en afvisning "
        "af modtagerens oplevelse.",
        rules=[
            "Afgræns rettelsen, så den ikke ligner en tilbagetrækning af hele budskabet.",
            "Giv ordet tilbage, når den nødvendige præcisering er foretaget.",
        ],
        examples=[
            GrammarExample("Jeg sagde aflyse; jeg mente udsætte til næste uge."),
            GrammarExample(
                "Den bemærkning blev for personlig. Undskyld. Lad os holde os til forslaget."
            ),
        ],
    ),
    GrammarTopic(
        "da-ellipsis-parallelism-c2",
        "Når udeladte led bærer på flere relationer",
        "C2",
        "Sammenbinding",
        "Genskab parallelle led uden at udjævne betydningsforskelle.",
        "I Lea vil læse rapporten, og Bo vil også er læse rapporten underforstået "
        "efter det andet vil. Modaliteten gælder begge personer, men ingen af "
        "handlingerne fremstilles som udført. Ved redigering skal paralleliteten "
        "kontrolleres; et fælles led kan skjule, at to verber kræver forskellige "
        "konstruktioner.",
        rules=[
            "Genskab først den fulde struktur, og kontrollér derefter deltagere og modalitet.",
            "Gentag et led, hvis forkortelsen giver tvetydighed eller en skæv konstruktion.",
        ],
        examples=[
            GrammarExample("Lea har læst bilaget, men Bo har ikke."),
            GrammarExample("Hun deltog i mødet og bidrog til drøftelsen."),
        ],
    ),
    GrammarTopic(
        "da-reference-disambiguation-c2",
        "Sin, hendes og den rette ejer",
        "C2",
        "Referencer",
        "Opløs uklarhed uden at opfinde en ny ejer.",
        "I Maja fortalte, at Liv havde solgt sin cykel henviser sin normalt til "
        "Liv, subjektet i ledsætningen. Hendes kan pege på Maja eller en anden "
        "relevant kvinde. I mere komplekse infinitivforbindelser kan både struktur "
        "og perspektiv spille ind; gentag navnet, når et praktisk dokument kræver "
        "entydighed frem for en sandsynlig læsning.",
        rules=[
            "Bestem den lokale sætningsstruktur, før du afgør en refleksiv henvisning.",
            "En entydig omskrivning kræver viden om den tilsigtede referent.",
        ],
        examples=[
            GrammarExample("Maja fortalte, at Liv havde solgt Majas cykel."),
            GrammarExample("Mener du Livs egen fuldmagt eller Majas?"),
        ],
    ),
    GrammarTopic(
        "da-calibrated-synthesis-c2",
        "Fordi, samtidig med og på den baggrund",
        "C2",
        "Faglig formidling",
        "Sammenbind kilder uden at tilføre en ubegrundet årsag.",
        "Fordi fastlægger en årsagsrelation, som samtidig med ikke gør. På den "
        "baggrund kan indlede en vurdering eller anbefaling, men beviser ikke "
        "årsagen til et observeret forhold. Når kilder sammenfattes, skal "
        "forbindelsesordene afspejle deres faktiske støtte, og forskelle i målgruppe "
        "eller metode skal bevares.",
        rules=[
            "Gør ikke samtidighed til årsag alene ved at vælge et stærkere bindeord.",
            "Adskil kildens resultat, din tolkning og dit handlingsforslag.",
        ],
        examples=[
            GrammarExample("Fraværet faldt, samtidig med at vagtplanen blev ændret."),
            GrammarExample(
                "På den baggrund foreslår vi et forsøg; effekten er endnu ikke fastslået."
            ),
        ],
    ),
    GrammarTopic(
        "da-sentence-rhythm-c2",
        "Rytme, vægt og præcis forenkling",
        "C2",
        "Genre og formidling",
        "Skift mellem tæt skrift og mundtlig klarhed med samme indhold.",
        "En lang foranstillet betingelse kan være præcis på skrift, men vanskelig "
        "at fastholde i tale. Del den op, og gentag det afgørende vilkår ved "
        "konklusionen. Korte sætninger er ikke automatisk klarere, hvis forbindelsen "
        "mellem dem forsvinder. Parallelle led kan fremhæve en kontrast uden at "
        "forenkle den til et falsk enten-eller.",
        rules=[
            "Bevar betingelsernes rækkevidde, når du indsætter punktummer.",
            "Lad den vigtigste nye oplysning få vægt uden at skjule nødvendige forbehold.",
        ],
        examples=[
            GrammarExample("Vi mangler finansiering. Derfor kan vi endnu ikke bestille arbejdet."),
            GrammarExample(
                "Det er en mulighed, ikke en aftale. En aftale kræver begge parters tilsagn."
            ),
        ],
        related=["da-register-recasting-c1", "da-calibrated-synthesis-c2"],
    ),
]
