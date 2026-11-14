"""Danish C1 placement items: judgement, agreement and contextual interpretation."""

from app.data._types import AssessmentQuestion

C1_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "da-g-c1-001",
        "grammar",
        "C1",
        "Efter en opringning til receptionen skriver Lea om reparationen: "
        "'Teknikeren skulle være færdig på torsdag.' Hvilken læsning passer bedst her?",
        [
            "Lea pålægger på receptionens vegne teknikeren at afslutte arbejdet torsdag.",
            "Lea gengiver receptionens oplysning om torsdag uden selv at garantere den.",
            "Lea kritiserer receptionens plan om torsdag som en frist, teknikeren har overskredet.",
            "Lea foreslår receptionen torsdag som en ny frist, der endnu skal forhandles.",
        ],
        "Lea gengiver receptionens oplysning om torsdag uden selv at garantere den.",
        "da-inference-modals-c1",
    ),
    AssessmentQuestion(
        "da-g-c1-002",
        "grammar",
        "C1",
        "Der står: 'Vi gennemfører arbejdsdagen, medmindre der varsles storm, "
        "eller adgangsvejen lukkes.' "
        "Du skal omskrive beskeden uden at tilføje nye betingelser. Hvilken version passer?",
        [
            "Arbejdsdagen gennemføres, hvis der ikke varsles storm, også selv om adgangsvejen lukkes.",
            "Arbejdsdagen gennemføres, hvis adgangsvejen er åben, også selv om der varsles storm.",
            "Arbejdsdagen aflyses kun, hvis både stormvarslet og vejlukningen bliver aktuelle.",
            "Arbejdsdagen gennemføres, hvis hverken stormvarslet eller vejlukningen bliver aktuelle.",
        ],
        "Arbejdsdagen gennemføres, hvis hverken stormvarslet eller vejlukningen bliver aktuelle.",
        "da-unless-boundaries-c1",
    ),
    AssessmentQuestion(
        "da-g-c1-003",
        "grammar",
        "C1",
        "I referatet står: 'Nora lovede Emil at bede udlejeren om at bestille ekstra nøgler.' "
        "Hvilken gengivelse bevarer både ansvarsfordelingen og graden af tilsagn?",
        [
            "Nora har påtaget sig at spørge udlejeren; en bestilling er ikke bekræftet.",
            "Emil har påtaget sig at spørge udlejeren; Nora skal bagefter hente nøglerne.",
            "Udlejeren har påtaget sig at bestille nøglerne; Nora skal orientere Emil.",
            "Nora har påtaget sig at bestille nøglerne; udlejeren skal blot godkende prisen.",
        ],
        "Nora har påtaget sig at spørge udlejeren; en bestilling er ikke bekræftet.",
        "da-infinitive-agents-c1",
    ),
    AssessmentQuestion(
        "da-g-c1-004",
        "grammar",
        "C1",
        "Et notat siger: 'Ikke alle afdelinger har meldt tilbage om begge forslag.' "
        "Hvilken konklusion kan drages uden oplysninger om de enkelte svar?",
        [
            "Mindst én afdeling har endnu ikke meldt tilbage om nogen af forslagene.",
            "Hver afdeling har meldt tilbage om mindst ét forslag, men ikke om dem begge.",
            "Mindst én afdeling mangler at melde tilbage om mindst ét af forslagene.",
            "Det ene forslag har fået svar fra alle, mens det andet kun har fået enkelte svar.",
        ],
        "Mindst én afdeling mangler at melde tilbage om mindst ét af forslagene.",
        "da-quantifier-scope-c1",
    ),
    AssessmentQuestion(
        "da-g-c1-005",
        "grammar",
        "C1",
        "En kollega siger: 'Vi er jo enige om at skære åbningstiden ned.' "
        "På sidste møde bad du om flere oplysninger, men tilsluttede dig ikke forslaget. "
        "Du vil rette antagelsen og holde drøftelsen åben. Hvad siger du?",
        [
            "Ja, lad os tage datoen for ændringen, når de sidste oplysninger er kommet.",
            "Det er vist bedst, at vi først orienterer kunderne om den nye åbningstid.",
            "Jeg er enig i, at vi nok skal have kortere åbningstid; spørgsmålet er hvor meget.",
            "Jeg har ikke tilsluttet mig endnu. Lad os se tallene, før vi beslutter noget.",
        ],
        "Jeg har ikke tilsluttet mig endnu. Lad os se tallene, før vi beslutter noget.",
        "da-jo-vel-vist-nok-c1",
    ),
    AssessmentQuestion(
        "da-g-c1-006",
        "grammar",
        "C1",
        "På mødet siger Ali: 'Jeg kan godt lige kigge på udkastet i morgen, men "
        "jeg når næppe en grundig gennemgang.' Hvilket referat bevarer hans tilsagn?",
        [
            "Ali færdigbehandler udkastet i morgen og vender tilbage med sin godkendelse.",
            "Ali tilbyder at se på udkastet i morgen; en grundig gennemgang er usandsynlig.",
            "Ali undersøger i morgen, om han senere får tid til at åbne udkastet.",
            "Ali gennemgår udkastet grundigt, men forventer først at svare efter i morgen.",
        ],
        "Ali tilbyder at se på udkastet i morgen; en grundig gennemgang er usandsynlig.",
        "da-register-recasting-c1",
    ),
    AssessmentQuestion(
        "da-v-c1-001",
        "vocabulary",
        "C1",
        "Midt i en drøftelse siger mødelederen: 'Jeg har en bagkant klokken halv fire.' "
        "Hvilken reaktion passer bedst, hvis I vil sikre hendes deltagelse i beslutningen?",
        [
            "Så venter vi med afstemningen, til du kommer tilbage efter halv fire.",
            "Så tager vi de første spørgsmål uden dig og samler op klokken halv fire.",
            "Så tager vi beslutningspunktet nu og gemmer orienteringen til sidst.",
            "Så aftaler vi, at du sender dine bemærkninger, inden mødet begynder.",
        ],
        "Så tager vi beslutningspunktet nu og gemmer orienteringen til sidst.",
    ),
    AssessmentQuestion(
        "da-v-c1-002",
        "vocabulary",
        "C1",
        "Efter et afslag svarer foreningen kommunen: 'Vi tager afgørelsen til efterretning.' "
        "Hvilken læsning holder sig inden for svarets betydning?",
        [
            "Den noterer afgørelsen uden dermed at tilslutte sig dens begrundelse.",
            "Den accepterer begrundelsen, men ønsker et andet praktisk resultat.",
            "Den betragter afgørelsen som et foreløbigt forslag, der endnu kan forhandles.",
            "Den trækker sin kritik tilbage mod at få en nærmere forklaring senere.",
        ],
        "Den noterer afgørelsen uden dermed at tilslutte sig dens begrundelse.",
    ),
    AssessmentQuestion(
        "da-v-c1-003",
        "vocabulary",
        "C1",
        "Sofie leder forgæves efter sine talepapirer, går i stå midt i en sætning "
        "og siger med et glimt i øjet: "
        "'Som I kan høre, er jeg jo grundigt forberedt.' Hvilken reaktion matcher "
        "bedst tonen uden at gøre hende til grin?",
        [
            "Du lyder godt forberedt; så lad os gå direkte til de punkter, du allerede har skrevet ned.",
            "Vi kan springe dit oplæg over, så du ikke behøver at forklare noget uden papirerne.",
            "Vi bør finde ud af, hvem der skulle have sendt dig materialet, før vi begynder.",
            "Hukommelsen får vist lidt ekstra arbejde i dag. Du må gerne låne mine noter.",
        ],
        "Hukommelsen får vist lidt ekstra arbejde i dag. Du må gerne låne mine noter.",
    ),
    AssessmentQuestion(
        "da-v-c1-004",
        "vocabulary",
        "C1",
        "En kunde skriver: 'Omfanget ligger fast, men der er lidt råderum i tidsplanen.' "
        "Hvilket forslag udnytter netop det råderum, kunden nævner?",
        [
            "Vi kan beholde datoen, hvis I fjerner den sidste del af opgaven.",
            "Vi kan levere hele opgaven mandag i stedet for fredag til den aftalte pris.",
            "Vi kan levere en mindre løsning fredag og aftale en ny pris bagefter.",
            "Vi kan fastholde planen, hvis I selv overtager kontrollen af leverancen.",
        ],
        "Vi kan levere hele opgaven mandag i stedet for fredag til den aftalte pris.",
    ),
    AssessmentQuestion(
        "da-r-c1-001",
        "reading",
        "C1",
        "Læs: 'Bestyrelsen anbefaler nye vinduer. Et flertal vil dog først se en "
        "samlet beregning af lån og vedligeholdelse. Der blev derfor kun afsat penge "
        "til en rådgiver. Næste møde skal behandle rådgiverens oplæg.' "
        "Hvilken besked til en fraværende beboer er dækkende?",
        [
            "Udskiftningen er vedtaget, mens rådgiveren skal afklare lån og vedligeholdelse.",
            "Rådgiveren skal kun beregne vedligeholdelse, da lånet allerede er godkendt.",
            "Udskiftningen er udsat på ubestemt tid; rådgiveren skal finde en anden løsning.",
            "Pengene går foreløbig til rådgivning; selve udskiftningen er ikke vedtaget.",
        ],
        "Pengene går foreløbig til rådgivning; selve udskiftningen er ikke vedtaget.",
    ),
    AssessmentQuestion(
        "da-r-c1-002",
        "reading",
        "C1",
        "Læs: 'Jeg havde afsat en halv time til at samle reolen. Tre timer senere "
        "sad jeg på gulvet med to skruer tilovers. Min karriere som møbelsnedker "
        "måtte vist vente lidt endnu.' Hvilken virkning har den sidste sætning?",
        [
            "Den forklarer, at fortælleren har søgt en læreplads, som nu må udsættes.",
            "Den gør fortællerens overvurdering af egne evner til en humoristisk pointe.",
            "Den flytter ansvaret for forsinkelsen over på producentens mangelfulde anvisning.",
            "Den antyder, at fortælleren trods forsinkelsen har bevist sin faglige dygtighed.",
        ],
        "Den gør fortællerens overvurdering af egne evner til en humoristisk pointe.",
    ),
    AssessmentQuestion(
        "da-r-c1-003",
        "reading",
        "C1",
        "Læs: 'Butikkerne ønsker længere parkeringstid. Beboerne frygter mere trafik. "
        "Begge grupper har sagt ja til at tælle biler i to uger. Butikkerne understreger, "
        "at optællingen ikke erstatter deres ønske; beboerne vil se tallene først.' "
        "Hvad kan mødelederen skrive?",
        [
            "Parterne har aftalt et fælles undersøgelsesgrundlag, men har ikke afklaret ændringen.",
            "Parterne støtter længere parkeringstid, hvis optællingen gennemføres som planlagt.",
            "Butikkerne har sat deres ønske i bero, mens beboerne forbereder et modforslag.",
            "Beboerne har accepteret butikkernes behov, men mangler at vælge optællingsdatoerne.",
        ],
        "Parterne har aftalt et fælles undersøgelsesgrundlag, men har ikke afklaret ændringen.",
    ),
    AssessmentQuestion(
        "da-r-c1-004",
        "reading",
        "C1",
        "Læs: 'Efter indførelsen af fællesspisning faldt madspildet i kantinen. "
        "Samtidig blev portionerne mindre, og antallet af gæster ændrede sig. "
        "Køkkenlederen er glad for udviklingen, men efterlyser tal pr. gæst.' "
        "Hvorfor er de ekstra tal relevante?",
        [
            "De kan vise, om gæsterne foretrækker fællesspisning frem for individuel servering.",
            "De kan afgøre, om mindre portioner var den eneste årsag til faldet i madspild.",
            "De kan belyse, om faldet også ses, når ændringen i gæsteantal tages i betragtning.",
            "De kan vise, om de mindre portioner har gjort kantinens samlede indkøb billigere.",
        ],
        "De kan belyse, om faldet også ses, når ændringen i gæsteantal tages i betragtning.",
    ),
]
