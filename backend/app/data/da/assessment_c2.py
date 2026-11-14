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
            "Målingerne fra maj viser, at den nuværende løsning burde have været valgt tidligere.",
            "Med målingerne i maj ville en anden løsning med sikkerhed allerede være gennemført.",
            "Tidligere adgang til målingerne kunne have ført til et andet valg frem mod i dag.",
            "Hvis målingerne kommer nu, kan den løsning, der blev valgt i maj, snart ændres.",
        ],
        "Tidligere adgang til målingerne kunne have ført til et andet valg frem mod i dag.",
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
            "Hvilket tidligere forløb henviser du til? Vi mener ikke, at beboerne blev holdt udenfor dengang.",
            "Vi kan godt forklare, hvorfor den seneste høring kom senere, end beboerne ønskede.",
            "Den tidligere udelukkelse var uheldig; denne gang var der dog en anden begrundelse.",
            "Vi vil gerne inddrage beboerne tidligere næste gang, når den nye plan foreligger.",
        ],
        "Hvilket tidligere forløb henviser du til? Vi mener ikke, at beboerne blev holdt udenfor dengang.",
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
            "Hun begrænser rabatten til de kunder, der betaler inden efteråret.",
            "Hun afviser at kalde tidsforskydningen en nedsættelse af det samlede beløb.",
        ],
        "Hun afviser at kalde tidsforskydningen en nedsættelse af det samlede beløb.",
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
            "Ansøgeren skal sende dokumentationen igen, men kan nøjes med en kortere version.",
            "Ansøgeren er fritaget for at sende dokumentationen igen, uden at det dermed er forbudt.",
            "Ansøgeren må kun vedlægge dokumentationen efter at have fået en ny godkendelse.",
            "Ansøgeren er fritaget for at oplyse om senere ændringer i de godkendte forhold.",
        ],
        "Ansøgeren er fritaget for at sende dokumentationen igen, uden at det dermed er forbudt.",
        "da-modal-scope-c2",
    ),
    AssessmentQuestion(
        "da-g-c2-005",
        "grammar",
        "C2",
        "Læs: 'Nogle af kollegerne har læst oplægget; det kan for den sags skyld "
        "være dem alle.' Hvordan virker tilføjelsen?",
        [
            "Den ophæver en nærliggende antydning om en begrænset gruppe uden at modsige første del.",
            "Den retter første dels faktuelle fejl og bekræfter, at hele gruppen har læst oplægget.",
            "Den udvider den omtalte gruppe fra kollegerne til andre mulige læsere.",
            "Den svækker første del ved også at åbne for, at ingen kolleger har læst oplægget.",
        ],
        "Den ophæver en nærliggende antydning om en begrænset gruppe uden at modsige første del.",
        "da-cancellable-inference-c2",
    ),
    AssessmentQuestion(
        "da-g-c2-006",
        "grammar",
        "C2",
        "En faglig vurdering lyder: 'Ordningen er nok billig at etablere, "
        "men driften er dyrere end i de øvrige modeller.' Hvilket referat er loyalt?",
        [
            "Vurderingen er usikker på etableringsprisen, men anbefaler ordningen på grund af driften.",
            "Vurderingen afviser, at etableringsprisen er lav, fordi driften ændrer beregningen.",
            "Vurderingen anerkender den lave etableringspris og fremhæver driftsudgiften som modhensyn.",
            "Vurderingen stiller den lave etableringspris som betingelse for at undersøge driften.",
        ],
        "Vurderingen anerkender den lave etableringspris og fremhæver driftsudgiften som modhensyn.",
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
        "tager bedst højde for hendes erkendelse?",
        [
            "Så må vi forklare igen, at tonen var vigtigere end detaljerne i kritikken.",
            "Så bør vi lade sagen ligge, indtil de kritiske deltagere selv tager den op.",
            "Så kan vi samle op ved at fremhæve de punkter, som ingen havde indvendinger imod.",
            "Så lad os anerkende det konkrete problem og spørge, hvad der stadig mangler et svar.",
        ],
        "Så lad os anerkende det konkrete problem og spørge, hvad der stadig mangler et svar.",
    ),
    AssessmentQuestion(
        "da-v-c2-003",
        "vocabulary",
        "C2",
        "Udvalget vil gerne tale med leverandøren, men formanden siger: "
        "'Kontakten må ikke foregribe generalforsamlingens beslutning.' "
        "Hvilken indledning til samtalen passer?",
        [
            "Vi undersøger mulige vilkår; en eventuel bestilling kræver stadig forsamlingens godkendelse.",
            "Vi er klar til at bestille, hvis I holder den pris, vi orienterer forsamlingen om.",
            "Vi har valgt jer som leverandør, men venter med at offentliggøre det til forsamlingen.",
            "Vi kan give et foreløbigt tilsagn, som forsamlingen senere får mulighed for at justere.",
        ],
        "Vi undersøger mulige vilkår; en eventuel bestilling kræver stadig forsamlingens godkendelse.",
    ),
    AssessmentQuestion(
        "da-v-c2-004",
        "vocabulary",
        "C2",
        "En undersøgelse af tre store hospitaler anbefales som grundlag for en lille "
        "klinik. En læser efterlyser en vurdering af overførbarheden. Hvad vil hun have belyst?",
        [
            "Om undersøgelsens forfattere har formidlet resultaterne i et sprog, klinikken forstår.",
            "Om hospitalerne har brugt samme målemetode, så resultaterne kan sammenlignes indbyrdes.",
            "Om forskelle i størrelse og arbejdsgange begrænser, hvad klinikken kan bruge resultaterne til.",
            "Om klinikken kan bekræfte, at de tre hospitalers oprindelige registreringer var fejlfri.",
        ],
        "Om forskelle i størrelse og arbejdsgange begrænser, hvad klinikken kan bruge resultaterne til.",
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
        "vil indføre ordningen i hele virksomheden næste måned.' Hvilken vurdering "
        "skelner mest præcist mellem grundlag og beslutning?",
        [
            "Direktørens beslutning følger rapportens anbefaling, fordi flere afdelinger giver et større forsøg.",
            "Selvudvælgelsen gør resultatet ubrugeligt, så rapporten giver ikke grundlag for yderligere afprøvning.",
            "Resultatet støtter mere afprøvning, mens en generel indførelse kræver antagelser, forsøget ikke afklarer.",
            "Koordinatorernes erfaring forklarer forbedringen, så antallet af møder kan udelades af næste forsøg.",
        ],
        "Resultatet støtter mere afprøvning, mens en generel indførelse kræver antagelser, forsøget ikke afklarer.",
    ),
    AssessmentQuestion(
        "da-r-c2-003",
        "reading",
        "C2",
        "Læs: 'Efter den tredje ekstra arbejdsweekend sagde Maja: Sikke et familievenligt "
        "projekt. Lederen lo kort, men Maja fortsatte: Jeg har faktisk brug for, at vi "
        "taler om planen. Lederen lagde kalenderen på bordet.' Hvilket svar fra lederen "
        "følger bedst op på Majas skift til direkte tale?",
        [
            "Ja, den joke har vi efterhånden hørt et par gange. Skal vi se, hvem der kan tage næste weekend?",
            "Jeg hører, at weekenderne er blevet et reelt problem. Lad os se på, hvilke opgaver vi kan flytte.",
            "Du har ret i, at projektet er familievenligt på andre punkter. Dem bør vi også huske i planen.",
            "Det var godt at få grinet lidt af det. Vi kan vende tilbage til kalenderen, når projektet er slut.",
        ],
        "Jeg hører, at weekenderne er blevet et reelt problem. Lad os se på, hvilke opgaver vi kan flytte.",
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
            "Parterne er enige om prøveordningen og åbningen; kun metoden til støjmåling mangler.",
            "Parterne har accepteret retten til ophævelse, men skal afklare, om den gælder før oktober.",
            "Arrangøren har accepteret beboernes vilkår mod til gengæld at få en sikker åbning i juni.",
            "Parterne deler ønsket om åbning, men er uenige om, hvad en overskridelse skal give ret til.",
        ],
        "Parterne deler ønsket om åbning, men er uenige om, hvad en overskridelse skal give ret til.",
    ),
]
