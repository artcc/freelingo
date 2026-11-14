"""Danish B2 grammar: scope, register and interpersonal meaning."""

from app.data._types import GrammarExample, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "da-object-shift-b2",
        "Jeg kender ham ikke",
        "B2",
        "Ordstilling",
        "Placér et tryksvagt objektspronomen i forhold til ikke.",
        "I en enkel hovedsætning med det fulde verbum på anden plads står et "
        "tryksvagt objektspronomen normalt før ikke: Jeg kender ham ikke. "
        "Hvis et hovedverbum bliver stående efter et hjælpeverbum, flytter "
        "objektet ikke foran dette verbum: Jeg har ikke mødt ham. Et betonet "
        "pronomen kan stå senere for at markere kontrast: Jeg kender ikke HAM.",
        rules=[
            "Skeln mellem tryksvage stedord og fulde navneordsled.",
            "Brug Jeg kender ikke naboen med et almindeligt navneordsobjekt.",
        ],
        examples=[
            GrammarExample("Jeg så hende ikke ved mødet."),
            GrammarExample("Jeg har ikke set hende siden mødet."),
            GrammarExample("Jeg så ikke hende, men hendes søster.", note="Tydelig kontrast."),
        ],
        related=["da-subordinate-negation-b1"],
    ),
    GrammarTopic(
        "da-negation-scope-b2",
        "Ikke alle og alle ikke",
        "B2",
        "Betydning og fokus",
        "Afklar præcis, hvad en benægtelse omfatter.",
        "Ikke alle siger, at en påstand ikke gælder for hele gruppen; det angiver "
        "ikke en bestemt andel. Ingen benægter derimod for hvert medlem af "
        "gruppen. Placering og tryk kan ændre, hvad ikke rammer. Alle kom ikke "
        "kan være tvetydigt i praksis, så skriv ikke alle kom eller ingen kom, "
        "når forskellen er vigtig.",
        rules=[
            "Ikke nødvendigvis afviser en sikker slutning, ikke selve muligheden.",
            "Kun knytter en begrænsning til et bestemt led; placér det tæt på det led.",
        ],
        examples=[
            GrammarExample("Ikke alle har svaret; vi mangler stadig tre svar."),
            GrammarExample("En høj pris betyder ikke nødvendigvis høj kvalitet."),
        ],
    ),
    GrammarTopic(
        "da-cleft-b2",
        "Det var tidspunktet, der var problemet",
        "B2",
        "Fokus",
        "Fremhæv den oplysning, der retter en misforståelse.",
        "En sætningskløvning bruger det er eller det var til at fremhæve et led. "
        "Det fremhævede led efterfølges af en relativ del: Det var Mette, der "
        "ringede. Som kan også bruges ved et fremhævet grundled. Ved et objekt "
        "bruges som eller ingen markør: Det var Mette, jeg ringede til. "
        "Konstruktionen er særlig nyttig, når man korrigerer fokus i samtalen.",
        rules=[
            "Bevar deltagernes roller, når en almindelig sætning kløves.",
            "Vælg nutid eller datid efter den situation, du beskriver.",
        ],
        examples=[
            GrammarExample("Det er leveringen, vi venter på, ikke betalingen."),
            GrammarExample("Det var Sofie, der foreslog at udsætte mødet."),
        ],
        related=["da-relative-som-der-b1"],
    ),
    GrammarTopic(
        "da-counterfactual-b2",
        "Hvis vi havde vidst det",
        "B2",
        "Betingelser",
        "Undersøg et alternativ til et afsluttet forløb.",
        "Hvis med førdatid kan beskrive en betingelse, som ikke blev opfyldt. "
        "Følgen står ofte med ville eller kunne have og kort tillægsform. "
        "Også en form som havde vi vidst det, var vi blevet hjemme er mulig "
        "og naturlig. Tidsudtryk kan forbinde en fortidig betingelse med en "
        "nutidig følge: Hvis vi havde sparet op, havde vi flere muligheder nu.",
        rules=[
            "Kunne have angiver en mulighed; ville have angiver et forventet tænkt udfald.",
            "Læs kontrafaktisk betydning ud fra sammenhængen, ikke kun verbformen.",
        ],
        examples=[
            GrammarExample("Hvis du havde ringet, kunne jeg have hentet dig."),
            GrammarExample("Havde vi bestilt før, ville vi have fået rabat."),
        ],
        related=["da-hypothetical-b1", "da-pluperfect-b1"],
    ),
    GrammarTopic(
        "da-modal-perfect-b2",
        "Burde have, kunne have og må have",
        "B2",
        "Modalitet",
        "Vurdér en fortidig handling uden at gøre vurderingen til et faktum.",
        "Burde have kan udtrykke en efterfølgende vurdering af, hvad der var "
        "bedst at gøre. Kunne have kan beskrive en ubrugt mulighed eller en "
        "usikker forklaring. Må have bruges ofte om en stærk slutning på "
        "grundlag af tegn. Konstruktionerne viser forskellige grader og typer "
        "af vurdering, ikke blot forskellige tider.",
        rules=[
            "En slutning med må have er ikke det samme som et øjenvidneudsagn.",
            "Burde have antyder ofte kritik, men fortæller ikke alene hele hændelsesforløbet.",
        ],
        examples=[
            GrammarExample("Vi burde have bedt om et skriftligt tilbud."),
            GrammarExample("Lyset er slukket; de må være gået hjem."),
            GrammarExample("Hun kunne have misforstået datoen."),
        ],
    ),
    GrammarTopic(
        "da-conditional-restrictions-b2",
        "Kun hvis, medmindre og så længe",
        "B2",
        "Betingelser",
        "Gør aftalens nødvendige betingelser og undtagelser tydelige.",
        "Kun hvis angiver en nødvendig betingelse, men siger ikke altid, at "
        "betingelsen er tilstrækkelig. Medmindre indfører en undtagelse: Vi "
        "gennemfører turen, medmindre det stormer. Så længe kan angive en "
        "vedvarende betingelse eller en tidsmæssig varighed. Afklar begge "
        "muligheder, når du formulerer en aftale.",
        rules=[
            "Tilføj ikke automatisk ikke efter medmindre; det kan vende betydningen.",
            "Skeln mellem det, der kræves, og det, der garanterer et resultat.",
        ],
        examples=[
            GrammarExample("Du kan kun låne lokalet, hvis du er medlem."),
            GrammarExample("Aftalen fortsætter, medmindre en af parterne opsiger den."),
            GrammarExample("Du må ændre tidspunktet, så længe du giver besked dagen før."),
        ],
    ),
    GrammarTopic(
        "da-passive-perspectives-b2",
        "Procedure, hændelse og resultat",
        "B2",
        "Passiv og ansvar",
        "Vælg passivform efter tekstens fokus og tidslige perspektiv.",
        "S-passiv er almindelig i procedurer: Sagerne fordeles hver morgen. "
        "Blive-passiv fremhæver ofte en hændelse: Sagen blev fordelt i går. "
        "Være med kort tillægsform kan beskrive et resultat: Sagen er afsluttet. "
        "Grænserne er ikke absolutte; en form som er sendt kan også læses som "
        "en afsluttet passiv handling. Tid, kontekst og verbets betydning hjælper.",
        rules=[
            "En udeladt aktør er ikke nødvendigvis ukendt; teksten kan nedtone ansvaret.",
            "Ved omskrivning til aktiv skal den handlende være kendt fra sammenhængen.",
        ],
        examples=[
            GrammarExample("Henvendelser registreres, før de bliver fordelt til medarbejderne."),
            GrammarExample("Døren blev låst klokken seks og er stadig låst."),
        ],
        related=["da-s-passive-b1", "da-blive-passive-b1"],
    ),
    GrammarTopic(
        "da-participial-adjectives-b2",
        "En afsluttet sag og de berørte beboere",
        "B2",
        "Tillægsformer",
        "Brug tillægsformer til at beskrive tilstande og deltagere.",
        "Kort tillægsform kan bruges som tillægsord: en lukket dør, de lukkede "
        "døre. Bøjningen afhænger af ordet og konstruktionen; former på -et får "
        "ofte -ede i bestemt form og flertal. Lang tillægsform på -ende bøjes "
        "ikke: en ventende kunde, de ventende kunder. Lær faste forbindelser "
        "som gældende regler og berørte beboere i deres sammenhæng.",
        rules=[
            "Overfør ikke automatisk tillægsordsbøjning til en verbal passiv.",
            "Lang tillægsform betyder ikke i sig selv, at dansk kræver en særlig løbende tid.",
        ],
        examples=[
            GrammarExample("De underskrevne aftaler ligger i mappen."),
            GrammarExample("Vi orienterer de berørte beboere om de gældende regler."),
        ],
    ),
    GrammarTopic(
        "da-impersonal-b2",
        "Der arbejdes på sagen",
        "B2",
        "Upersonlige konstruktioner",
        "Beskriv en aktivitet eller en oplysning uden et konkret grundled.",
        "Der kan være formelt grundled i upersonlig passiv: Der arbejdes på "
        "sagen. Det kan indlede en konstruktion med en efterfølgende indholdssætning: "
        "Det forventes, at arbejdet slutter fredag. Konstruktionerne er almindelige "
        "i offentlige beskeder, men kan skjule, hvem der arbejder eller forventer noget. "
        "Brug en navngiven aktør, når ansvaret er vigtigt.",
        rules=[
            "Upersonlig passiv kan dannes med verber uden genstandsled: Der danses.",
            "Der arbejdes og det forventes følger forskellige sætningsmønstre.",
        ],
        examples=[
            GrammarExample("Der bliver arbejdet på vejen hele natten."),
            GrammarExample("Det oplyses, at borgermødet er flyttet."),
        ],
        related=["da-passive-perspectives-b2"],
    ),
    GrammarTopic(
        "da-concession-nuance-b2",
        "Ganske vist, men; selv hvis; uanset om",
        "B2",
        "Argumentation",
        "Anerkend et forhold, eller gør resultatet uafhængigt af en betingelse.",
        "Ganske vist anerkender en oplysning og følges ofte af men med et modargument. "
        "Selv hvis fremhæver en tænkt betingelse som utilstrækkelig til at ændre "
        "resultatet. Uanset om siger, at resultatet gælder på tværs af de nævnte "
        "muligheder. Selv om kan både være faktuelt og hypotetisk; selv hvis "
        "gør den betingede læsning tydeligere.",
        rules=[
            "Et anerkendt argument skal gengives loyalt, selv når du er uenig i konklusionen.",
            "Uanset om A eller B kræver, at den efterfølgende påstand gælder i begge tilfælde.",
        ],
        examples=[
            GrammarExample("Det er ganske vist dyrere, men vi får også en længere garanti."),
            GrammarExample("Selv hvis vi får tilskud, skal vi finde flere frivillige."),
            GrammarExample("Vi holder mødet, uanset om formanden kan deltage eller ej."),
        ],
        related=["da-concession-b1"],
    ),
    GrammarTopic(
        "da-correlative-b2",
        "Jo mere, desto bedre",
        "B2",
        "Sammenhænge",
        "Beskriv to størrelser, der ændrer sig i forhold til hinanden.",
        "Jo og en sammenligningsform kan kobles med desto eller jo og endnu "
        "en sammenligningsform: Jo tidligere vi bestiller, desto billigere "
        "bliver det. Konstruktionen beskriver en sammenhæng, men beviser ikke "
        "i sig selv, at det ene er årsag til det andet. I korte svar kan "
        "verber udelades: Jo før, jo bedre.",
        rules=[
            "Både jo ... desto og jo ... jo er almindelige mønstre.",
            "I den fulde anden sætning står det bøjede verbum før grundleddet.",
        ],
        examples=[
            GrammarExample("Jo længere vi venter, desto færre muligheder har vi."),
            GrammarExample("Jo mere præcist du spørger, jo lettere er det at svare."),
        ],
    ),
    GrammarTopic(
        "da-relative-prepositions-b2",
        "Den løsning, vi talte om",
        "B2",
        "Relativsætninger",
        "Bevar forholdsordet, når et led bliver en relativ beskrivelse.",
        "I almindeligt dansk står forholdsordet ofte sidst: den kollega, jeg "
        "arbejder sammen med. I mere formelt sprog kan det stå foran hvilken "
        "eller hvem: den kollega, med hvem jeg samarbejder. Hvis kan udtrykke "
        "ejeforhold i en relativsætning: en borger, hvis sag er afsluttet. "
        "Dette hvis er ikke en betingelse.",
        rules=[
            "Et afsluttende forholdsord er naturligt dansk, også i mange skrevne tekster.",
            "Vælg formel omskrivning efter modtageren, ikke for at gøre teksten unødigt tung.",
        ],
        examples=[
            GrammarExample("Det er det forslag, vi tog stilling til i går."),
            GrammarExample("Vi kontaktede de beboere, hvis boliger var berørt."),
        ],
        related=["da-relative-som-der-b1"],
    ),
    GrammarTopic(
        "da-particles-vel-da-b2",
        "Du kommer vel? Det er da fint!",
        "B2",
        "Samtalens småord",
        "Fortolk forventning, bekræftelse og modspil i småord.",
        "Vel søger ofte bekræftelse på en forventning: Du har vel fået besked? "
        "Da kan blandt andet udtrykke en reaktion, en positiv vurdering eller "
        "modsigelse af en forventning: Det kan da ikke passe! Tonefaldet kan "
        "gøre det samme småord venligt, overrasket eller irriteret. Dette da "
        "er ikke tidsordet i da jeg kom hjem.",
        rules=[
            "Vel kan lægge pres på modtageren, hvis en bestemt bekræftelse forventes.",
            "Småord skal fortolkes sammen med situation og tonefald.",
        ],
        examples=[
            GrammarExample("Du har vel ikke noget imod, at vi åbner vinduet?"),
            GrammarExample("Nå, det er da en god nyhed!"),
            GrammarExample("Det var da dig, der foreslog tidspunktet."),
        ],
        related=["da-particles-jo-nok-b1"],
    ),
    GrammarTopic(
        "da-evidential-modals-b2",
        "Det må være; det skulle være",
        "B2",
        "Kilder og sikkerhed",
        "Skeln mellem en slutning og en oplysning fra andre.",
        "Må kan markere en slutning: De må være hjemme, for lyset er tændt. "
        "Skulle kan i en bestemt sammenhæng markere noget, man har hørt: "
        "Den nye udstilling skulle være god. Det garanterer ikke oplysningens "
        "rigtighed. Skulle kan også udtrykke plan, pligt eller en tænkt mulighed; "
        "man må finde den relevante betydning i sammenhængen.",
        rules=[
            "Gør kilden tydelig, når modtageren skal vurdere oplysningens vægt.",
            "Kan være er en mulighed, mens må være typisk er en stærkere slutning.",
        ],
        examples=[
            GrammarExample("Ifølge naboerne skulle caféen åbne igen til foråret."),
            GrammarExample("Der står tre cykler udenfor, så de må have gæster."),
        ],
        related=["da-modal-perfect-b2"],
    ),
    GrammarTopic(
        "da-reported-perspective-b2",
        "Gengivelse uden at overtage påstanden",
        "B2",
        "Kilder og perspektiv",
        "Bevar taler, tidspunkt og grad af sikkerhed i en gengivelse.",
        "Ifølge, oplyser, vurderer og hævder angiver forskellige relationer til "
        "en kilde. Hævder kan signalere afstand, mens oplyser ofte virker "
        "mere neutralt. Flyt stedord og tidsudtryk til den nye fortællesituation, "
        "men bevar forbehold som måske, forventer og muligvis. En forventning "
        "må ikke blive til et løfte ved omskrivning.",
        rules=[
            "Datid i gengivelsen er mulig uden at gøre indholdet ugyldigt i nutiden.",
            "Skeln mellem kildens vurdering og din egen konklusion.",
        ],
        examples=[
            GrammarExample("Lederen vurderer, at vi måske kan åbne mandag."),
            GrammarExample("Ifølge referatet forventede udvalget et svar ugen efter."),
        ],
        related=["da-reported-speech-b1", "da-evidential-modals-b2"],
    ),
    GrammarTopic(
        "da-nominalisation-b2",
        "Fra at beslutte til en beslutning",
        "B2",
        "Skriftlig fremstilling",
        "Saml information med navneord uden at skjule handling og ansvar.",
        "Verbhandlinger kan udtrykkes med navneord som behandling, vurdering og "
        "godkendelse. Det gør det muligt at henvise kort til et helt forløb: "
        "Behandlingen tager to uger. Mange nominaliseringer i samme sætning "
        "kan dog gøre teksten tung. Når du omskriver til et verbum, skal "
        "du bevare aktør, tidspunkt og eventuelle forbehold.",
        rules=[
            "Gør det klart, hvem der foretager en vurdering eller en godkendelse.",
            "Et kortere udtryk er ikke altid mere præcist.",
        ],
        examples=[
            GrammarExample("Efter udvalgets godkendelse sender vi aftalen til underskrift."),
            GrammarExample("Når udvalget har godkendt aftalen, sender vi den til underskrift."),
        ],
    ),
    GrammarTopic(
        "da-infinitive-controls-b2",
        "Hvem skal gøre hvad?",
        "B2",
        "Navneform og deltagere",
        "Find den tænkte handlende i en navneformskonstruktion.",
        "I Jeg lover at ringe er det jeg, der skal ringe. I Jeg beder dig "
        "om at ringe er det dig. Hvilket led der styrer navneformen, afhænger "
        "af det overordnede verbum. Ved sanseverber bruges ofte objekt og "
        "navneform uden at: Jeg hørte hende synge. Vælg en hel ledsætning, "
        "hvis ansvarsfordelingen ellers bliver uklar.",
        rules=[
            "Lær lover at og beder nogen om at som forskellige mønstre.",
            "Bevar den handlende ved omskrivning til en sætning med at.",
        ],
        examples=[
            GrammarExample("Lederen lovede medarbejderen at undersøge sagen."),
            GrammarExample("Lederen bad medarbejderen om at undersøge sagen."),
        ],
    ),
    GrammarTopic(
        "da-fronting-b2",
        "Den del vender vi tilbage til",
        "B2",
        "Informationsrækkefølge",
        "Sæt kendt eller kontrasteret information først uden at miste sætningsstrukturen.",
        "Første plads i en fremsættende hovedsætning kan rumme et objekt, et "
        "tidsled eller en hel ledsætning. Det bøjede verbum står derefter på "
        "anden plads, forstået som anden sætningsdel. I tale kan et led stå "
        "uden for selve sætningen og genoptages: Den del, den vender vi tilbage til. "
        "Det er et særskilt samtalemønster, ikke fri dobbeltbesættelse i alle tekster.",
        rules=[
            "Et langt indledende led tæller som én sætningsdel.",
            "Brug fremrykning til sammenhæng eller kontrast, ikke blot til variation.",
        ],
        examples=[
            GrammarExample("Den økonomiske del har vi endnu ikke gennemgået."),
            GrammarExample("Efter en kort drøftelse vedtog bestyrelsen forslaget."),
        ],
        related=["da-object-shift-b2"],
    ),
    GrammarTopic(
        "da-det-references-b2",
        "Det, den og en hel påstand",
        "B2",
        "Tekstsammenhæng",
        "Vis, om et stedord henviser til en ting eller til et helt udsagn.",
        "Den og det kan genoptage navneord efter køn: aftalen → den, tilbuddet "
        "→ det. Det kan også henvise til indholdet af en hel sætning: Hun vil "
        "udsætte mødet. Det overrasker mig. En uklar henvisning kan få en kritik "
        "til at ramme personen i stedet for forslaget. Gentag et præcist navneord, "
        "når flere mulige henvisninger konkurrerer.",
        rules=[
            "En hel påstand genoptages normalt med det, uanset køn på navneordene i den.",
            "Kontrollér henvisningen, når et afsnit omtaler flere forslag.",
        ],
        examples=[
            GrammarExample("Planen er dyr, men den kan gennemføres."),
            GrammarExample("De vil spare på vedligeholdelsen. Det er jeg uenig i."),
        ],
    ),
    GrammarTopic(
        "da-elliptical-responses-b2",
        "Det gør jeg også; det kan jeg ikke",
        "B2",
        "Svar og udeladelse",
        "Undgå gentagelse uden at ændre betydningen af det foregående udsagn.",
        "I korte svar kan gøre erstatte et almindeligt handlingsverbum: "
        "Jeg cykler på arbejde. Det gør jeg også. Modalverber og være gentages "
        "ofte i stedet: Jeg kan komme. Det kan jeg ikke. Heller bruges typisk "
        "ved en fælles benægtelse. Jo kan modsige et negativt spørgsmål eller "
        "udsagn; ja og nej skal forstås i den konkrete samtale.",
        rules=[
            "Vælg hjælpeverbum efter det, svaret genoptager.",
            "Gør svaret længere, hvis et kort ja eller nej kan misforstås.",
        ],
        examples=[
            GrammarExample("Jeg kan ikke komme torsdag. — Det kan jeg heller ikke."),
            GrammarExample("Har du ikke læst beskeden? — Jo, men jeg har ikke svaret endnu."),
            GrammarExample("Jeg foretrækker en fælles løsning. — Det gør jeg også."),
        ],
    ),
    GrammarTopic(
        "da-pragmatic-softening-b2",
        "Kunne vi måske finde en anden løsning?",
        "B2",
        "Høflighed og styrke",
        "Tilpas en anmodning uden at gøre ønsket uklart.",
        "Kunne, måske og en indledning som jeg vil gerne høre kan gøre en "
        "anmodning mindre direkte. Fortidsformen kunne viser her afstand "
        "og høflighed, ikke en fortidig evne. Lige kan få en opgave til at "
        "lyde lille og kan derfor også virke pressende. Kombinationer af "
        "for mange forbehold kan gøre en vigtig besked utydelig.",
        rules=[
            "Angiv stadig, hvad du beder om, og hvornår du har brug for det.",
            "Et indirekte spørgsmål kan være en anmodning, ikke blot et spørgsmål om evne.",
        ],
        examples=[
            GrammarExample("Kunne du sende dit forslag inden torsdag, så vi kan nå at læse det?"),
            GrammarExample("Jeg er ikke helt overbevist om, at vi har tid nok."),
            GrammarExample("Skal vi prøve at finde en løsning, begge parter kan leve med?"),
        ],
        related=["da-particles-vel-da-b2"],
    ),
]
