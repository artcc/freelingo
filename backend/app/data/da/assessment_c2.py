"""Danish C2 placement items: precise implications and flexible social judgement."""

from app.data._types import AssessmentQuestion

C2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "da-g-c2-001",
        "grammar",
        "C2",
        "En projektleder siger: 'Havde vi fået målingerne i maj, kunne vi stå med "
        "en anden løsning nu.' Hvilken gengivelse bevarer både tid og sikkerhedsgrad?",
        [
            "Målingerne fra maj begrunder et tidligere valg af den løsning, vi bruger nu.",
            "Målingerne i maj ville med sikkerhed have givet os en anden løsning nu.",
            "Med målingerne i maj kunne vores nuværende løsning have været en anden.",
            "Får vi målingerne nu, kan vi ændre den løsning, der blev valgt i maj.",
        ],
        "Med målingerne i maj kunne vores nuværende løsning have været en anden.",
        "da-mixed-counterfactuals-c2",
    ),
    AssessmentQuestion(
        "da-g-c2-002",
        "grammar",
        "C2",
        "Journalisten spørger: 'Hvorfor har I igen holdt beboerne udenfor?' "
        "Foreningens talsperson vil først udfordre den historik, spørgsmålet bygger på. "
        "Hvilket svar gør det mest præcist?",
        [
            "Hvilken tidligere sag mener du? Vi bestrider, at beboerne blev holdt udenfor.",
            "Sidst fik beboerne materialet sent, fordi vi måtte afvente rådgiverens svar.",
            "Vi beklager den tidligere udelukkelse, men denne gang blev planen sendt til alle.",
            "Sidste gang skete udelukkelsen ved en fejl; nu skyldes den hensynet til tidsplanen.",
        ],
        "Hvilken tidligere sag mener du? Vi bestrider, at beboerne blev holdt udenfor.",
        "da-presupposed-background-c2",
    ),
    AssessmentQuestion(
        "da-g-c2-003",
        "grammar",
        "C2",
        "Om en omstridt betaling siger rådgiveren: 'Det er ikke en rabat; "
        "beløbet bliver bare opkrævet til efteråret.' Hvad korrigerer rådgiveren?",
        [
            "Hun afviser, at kunden får en senere betalingsfrist end oprindeligt aftalt.",
            "Hun afviser efterårets opkrævning, men accepterer en mindre betaling nu.",
            "Hun begrænser rabatten til betalinger inden efteråret.",
            "Hun skelner mellem en udskudt betaling og et lavere samlet beløb.",
        ],
        "Hun skelner mellem en udskudt betaling og et lavere samlet beløb.",
        "da-corrective-negation-c2",
    ),
    AssessmentQuestion(
        "da-g-c2-004",
        "grammar",
        "C2",
        "En vejledning siger: 'Ansøgere, der allerede er godkendt, behøver ikke "
        "vedlægge dokumentationen igen, medmindre der er sket ændringer.' "
        "En tidligere godkendt ansøger har uændrede forhold. Hvad følger af formuleringen?",
        [
            "Ansøgeren kan udsætte dokumentationen, men skal sende den, før sagen afgøres.",
            "Kravet bortfalder her; teksten siger ikke, at genindsendelse er forbudt.",
            "Ansøgeren må kun gensende bilaget efter en ny godkendelse.",
            "Ansøgeren behøver heller ikke oplyse om senere ændringer.",
        ],
        "Kravet bortfalder her; teksten siger ikke, at genindsendelse er forbudt.",
        "da-modal-scope-c2",
    ),
    AssessmentQuestion(
        "da-g-c2-005",
        "grammar",
        "C2",
        "Læs: 'Nogle af kollegerne har læst oplægget; det kan for den sags skyld "
        "være dem alle.' Hvordan virker tilføjelsen?",
        [
            "Den ophæver antydningen 'ikke alle', men fastholder, at nogen har læst oplægget.",
            "Den retter første dels fejl og bekræfter, at alle har læst oplægget.",
            "Den ændrer, hvem kollegerne omfatter, men fastholder, at nogle af dem ikke har læst.",
            "Den svækker første del ved også at åbne for, at ingen kolleger har læst oplægget.",
        ],
        "Den ophæver antydningen 'ikke alle', men fastholder, at nogen har læst oplægget.",
        "da-cancellable-inference-c2",
    ),
    AssessmentQuestion(
        "da-g-c2-006",
        "grammar",
        "C2",
        "En faglig vurdering lyder: 'Ordningen er nok billig at etablere, "
        "men driften er dyrere end i de øvrige modeller.' Hvilket referat er loyalt?",
        [
            "Den lave etableringspris opvejer den dyrere drift, så ordningen samlet set anbefales.",
            "Vurderingen afviser, at etableringsprisen er lav, fordi driften ændrer beregningen.",
            "Vurderingen medgiver fordelen ved etableringen, men peger på driften som et modhensyn.",
            "Vurderingen stiller den lave etableringspris som betingelse for at undersøge driften.",
        ],
        "Vurderingen medgiver fordelen ved etableringen, men peger på driften som et modhensyn.",
        "da-nok-men-c2",
    ),
    AssessmentQuestion(
        "da-v-c2-001",
        "vocabulary",
        "C2",
        "I en klage står: 'Vi kræver aftalen ophævet, subsidiært et afslag i prisen.' "
        "Hvad vil det sige for behandlingen af kravene?",
        [
            "Prisafslaget skal lægges oven i ophævelsen, hvis begge krav kan gennemføres.",
            "Prisafslaget er et alternativ, hvis kravet om ophævelse ikke imødekommes.",
            "Prisafslaget skal afgøres først, før klageren tager stilling til en ophævelse.",
            "Ophævelsen gælder kun, hvis parterne først bliver enige om prisafslagets størrelse.",
        ],
        "Prisafslaget er et alternativ, hvis kravet om ophævelse ikke imødekommes.",
    ),
    AssessmentQuestion(
        "da-v-c2-002",
        "vocabulary",
        "C2",
        "En kollega siger efter en vanskelig samtale: 'Jeg prøvede at glatte ud, "
        "men endte med at få kritikken til at lyde uvæsentlig.' Hvilket næste svar "
        "hjælper hende med at rette netop den virkning?",
        [
            "Så må vi forklare, hvorfor du nedtonede kritikken for at dæmpe konflikten.",
            "Så må vi forklare vores gode hensigter frem for at genåbne indvendingerne.",
            "Så lad os fremhæve enighedspunkterne og vente lidt med indvendingerne.",
            "Så lad os tage kritikken alvorligt og følge op på de ubesvarede spørgsmål.",
        ],
        "Så lad os tage kritikken alvorligt og følge op på de ubesvarede spørgsmål.",
    ),
    AssessmentQuestion(
        "da-v-c2-003",
        "vocabulary",
        "C2",
        "Udvalget vil gerne tale med leverandøren, men formanden siger: "
        "'Kontakten må ikke foregribe generalforsamlingens beslutning.' "
        "Hvilken indledning til samtalen passer?",
        [
            "Vi undersøger vilkårene; forsamlingen skal stadig godkende en bestilling.",
            "Vi er klar til at bestille, hvis I holder den pris, vi orienterer forsamlingen om.",
            "Vi har valgt jer som leverandør, men venter med at offentliggøre det til forsamlingen.",
            "Vi kan give et foreløbigt tilsagn, som forsamlingen senere får mulighed for at justere.",
        ],
        "Vi undersøger vilkårene; forsamlingen skal stadig godkende en bestilling.",
    ),
    AssessmentQuestion(
        "da-v-c2-004",
        "vocabulary",
        "C2",
        "En undersøgelse af tre store hospitaler anbefales som grundlag for en lille "
        "klinik. En læser efterlyser en vurdering af overførbarheden. Hvad vil hun have belyst?",
        [
            "Om resultaterne er beskrevet i et sprog, som klinikkens ansatte forstår.",
            "Om hospitalernes resultater kan sammenlignes, fordi målemetoden er ens.",
            "Om forskelle i rammerne begrænser resultaternes anvendelse på klinikken.",
            "Om klinikken kan kontrollere, at hospitalernes registreringer er fejlfrie.",
        ],
        "Om forskelle i rammerne begrænser resultaternes anvendelse på klinikken.",
    ),
    AssessmentQuestion(
        "da-r-c2-001",
        "reading",
        "C2",
        "Læs: 'Rasmus læste beskeden igen. Mødet var flyttet uden hans samtykke. "
        "Sådan behandlede man altså folk, der havde holdt foreningen kørende i tyve år. "
        "Han lagde telefonen med skærmen nedad.' Hvilken læsning er bedst underbygget?",
        [
            "Den tredje sætning lader Rasmus' oplevelse af krænkelse farve fremstillingen.",
            "Den tredje sætning gengiver en fælles vurdering, som de øvrige medlemmer har tilsluttet sig.",
            "Fortælleren dokumenterer her, at foreningen bevidst ønskede at ydmyge Rasmus.",
            "Rasmus citerer med den tredje sætning en begrundelse, han har læst i beskeden.",
        ],
        "Den tredje sætning lader Rasmus' oplevelse af krænkelse farve fremstillingen.",
    ),
    AssessmentQuestion(
        "da-r-c2-002",
        "reading",
        "C2",
        "Læs: 'Et forsøg med færre møder gav mere sammenhængende arbejdstid i to "
        "afdelinger. Deltagerne havde selv meldt sig, og begge afdelinger havde "
        "erfarne koordinatorer. Rapporten anbefaler et større forsøg. Direktøren "
        "vil indføre ordningen permanent i hele virksomheden næste måned.' Hvilken vurdering "
        "skelner mest præcist mellem grundlag og beslutning?",
        [
            "En permanent indførelse følger anbefalingen, fordi den omfatter flere afdelinger end forsøget.",
            "Kun frivillige afdelinger med erfarne koordinatorer bør deltage i næste forsøg for at sikre overførbarhed.",
            "Forsøget taler for videre afprøvning; en permanent udrulning bygger på yderligere antagelser.",
            "Koordinatorernes erfaring forklarer effekten; næste forsøg behøver ikke ændre mødeantallet.",
        ],
        "Forsøget taler for videre afprøvning; en permanent udrulning bygger på yderligere antagelser.",
    ),
    AssessmentQuestion(
        "da-r-c2-003",
        "reading",
        "C2",
        "Læs: 'Efter den tredje ekstra arbejdsweekend sagde Maja: Sikke et familievenligt "
        "projekt. Lederen lo kort, men Maja fortsatte: Jeg har faktisk brug for, at vi "
        "taler om planen. Lederen lagde kalenderen på bordet.' Lederen vil først afklare "
        "hendes bekymring uden at lægge en bestemt forklaring i munden på hende. Hvad siger han?",
        [
            "Er det især fordelingen mellem kollegerne, du mener er urimelig, selv om antallet af weekender passer?",
            "Hvad betyder de ekstra weekender for dig, og hvilke dele af planen skal vi se nærmere på?",
            "Vil du hellere bytte næste weekend med en kollega, så vi kan fortsætte efter den aftalte plan?",
            "Vil du have, at vi aftaler regler for den slags jokes, så tonen på møderne bliver bedre?",
        ],
        "Hvad betyder de ekstra weekender for dig, og hvilke dele af planen skal vi se nærmere på?",
    ),
    AssessmentQuestion(
        "da-r-c2-004",
        "reading",
        "C2",
        "Læs: 'Beboergruppen accepterer en prøveordning frem til oktober, forudsat "
        "at støjen måles, og at aftalen kan ophæves ved overskridelser. Arrangøren "
        "accepterer målingerne, men ønsker kun genforhandling ved overskridelser. "
        "Begge vil gerne åbne i juni.' Hvilken sammenfatning bør mægleren give?",
        [
            "Parterne har aftalt åbningen; kun metoden til støjmålingen er uafklaret.",
            "Retten til ophævelse er aftalt; det er kun tidspunktet for den, der er omstridt.",
            "Arrangøren accepterer vilkårene til gengæld for en garanti om åbning i juni.",
            "Åbningen er et fælles ønske; retten til at ophæve aftalen er fortsat omstridt.",
        ],
        "Åbningen er et fælles ønske; retten til at ophæve aftalen er fortsat omstridt.",
    ),
]
