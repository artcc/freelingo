"""Danish B2 placement items testing perspective, inference and interaction."""

from app.data._types import AssessmentQuestion

B2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "da-g-b2-001",
        "grammar",
        "B2",
        "Vælg neutral ordstilling uden kontrasttryk: Jeg har ___ siden høringen.",
        [
            "hende ikke mødt",
            "mødt ikke hende",
            "ikke mødt hende",
            "ikke hende mødt",
        ],
        "ikke mødt hende",
        "da-object-shift-b2",
    ),
    AssessmentQuestion(
        "da-g-b2-002",
        "grammar",
        "B2",
        "Der var ti deltagere. Referatet siger: Ikke alle støttede forslaget. "
        "Hvad kan man udlede af den formulering alene?",
        [
            "Mindst én deltager støttede ikke forslaget.",
            "Mindst seks deltagere var imod forslaget.",
            "Præcis fem deltagere støttede forslaget.",
            "Alle deltagere undlod at tage stilling.",
        ],
        "Mindst én deltager støttede ikke forslaget.",
        "da-negation-scope-b2",
    ),
    AssessmentQuestion(
        "da-g-b2-003",
        "grammar",
        "B2",
        "Læs: Hvis vi havde fået advarslen i tide, kunne vi have flyttet arrangementet. "
        "Hvilken gengivelse bevarer betydningen?",
        [
            "Vi fik advarslen i tide, men valgte at beholde stedet.",
            "Vi flyttede arrangementet, før advarslen kom.",
            "En advarsel i tide ville have gjort flytning unødvendig.",
            "En tidligere advarsel ville have givet os mulighed for at flytte det.",
        ],
        "En tidligere advarsel ville have givet os mulighed for at flytte det.",
        "da-counterfactual-b2",
    ),
    AssessmentQuestion(
        "da-g-b2-004",
        "grammar",
        "B2",
        "Du sagde: 'Prisen er acceptabel, men vi kan ikke vente seks uger.' "
        "En kollega har forstået det som en indvending mod beløbet. "
        "Hvilket svar retter netop den misforståelse?",
        [
            "Det var prisen, der gjorde leveringstiden længere.",
            "Det var leveringstiden, jeg kritiserede, ikke prisen.",
            "Det var kritikken, der fik prisen til at stige.",
            "Det var leveringen, jeg roste på grund af prisen.",
        ],
        "Det var leveringstiden, jeg kritiserede, ikke prisen.",
        "da-cleft-b2",
    ),
    AssessmentQuestion(
        "da-g-b2-005",
        "grammar",
        "B2",
        "Læs: Lederen lovede Sara at kontakte leverandøren. "
        "Hvem har påtaget sig at kontakte leverandøren?",
        [
            "Sara, fordi hun bliver nævnt efter lovede.",
            "Lederen, som gav løftet om handlingen.",
            "Leverandøren, som skal kontakte Sara.",
            "Sara og leverandøren, som skal kontakte lederen.",
        ],
        "Lederen, som gav løftet om handlingen.",
        "da-infinitive-controls-b2",
    ),
    AssessmentQuestion(
        "da-g-b2-006",
        "grammar",
        "B2",
        "Aftalen siger: Lokalet kan kun lånes, hvis foreningen har en ansvarsforsikring. "
        "Hvilken læsning er præcis?",
        [
            "Forsikringen er valgfri, når en forening låner lokalet.",
            "Alle forsikrede foreninger er garanteret adgang til lokalet.",
            "Forsikringen kræves kun, hvis der allerede er sket en skade.",
            "Forsikring er nødvendig, men teksten udelukker ikke andre krav.",
        ],
        "Forsikring er nødvendig, men teksten udelukker ikke andre krav.",
        "da-conditional-restrictions-b2",
    ),
    AssessmentQuestion(
        "da-g-b2-007",
        "grammar",
        "B2",
        "En ven siger: Den nye café skulle være rigtig god; det siger mine naboer i hvert fald. "
        "Hvordan præsenterer vennen vurderingen?",
        [
            "Som en oplysning fra andre, ikke som sin egen sikre erfaring.",
            "Som et krav, caféen skal opfylde for at få lov at åbne.",
            "Som en tidligere plan om selv at drive caféen.",
            "Som en sikker konklusion efter selv at have spist der.",
        ],
        "Som en oplysning fra andre, ikke som sin egen sikre erfaring.",
        "da-evidential-modals-b2",
    ),
    AssessmentQuestion(
        "da-g-b2-008",
        "grammar",
        "B2",
        "Du kan ligesom din kollega ikke deltage fredag. Kollegaen siger: Jeg kan ikke "
        "komme fredag. Hvilket svar tilslutter sig dette uden at ændre modaliteten?",
        [
            "Det gør jeg også.",
            "Det kan jeg godt.",
            "Det kan jeg heller ikke.",
            "Det er jeg heller ikke.",
        ],
        "Det kan jeg heller ikke.",
        "da-elliptical-responses-b2",
    ),
    AssessmentQuestion(
        "da-v-b2-001",
        "vocabulary",
        "B2",
        "Efter en forhandling siger formanden: Vi har givet køb på tempoet, men ikke "
        "på kvaliteten. Hvad har foreningen accepteret?",
        [
            "At sænke kvalitetskravene for at blive hurtigere færdig.",
            "At bruge længere tid og bevare kvalitetskravene.",
            "At fastholde tidsplanen og lade kvaliteten afhænge af prisen.",
            "At stoppe arbejdet, fordi kvaliteten allerede var for lav.",
        ],
        "At bruge længere tid og bevare kvalitetskravene.",
    ),
    AssessmentQuestion(
        "da-v-b2-002",
        "vocabulary",
        "B2",
        "Projektlederen siger: Godkendelsen er vores flaskehals. " "Hvilket problem peger hun på?",
        [
            "At medarbejderne bruger forskellige kriterier til at vurdere samme sag.",
            "At opgaverne bliver fordelt uklart mellem projektets afdelinger.",
            "At godkendte sager ofte skal laves om på grund af fejl i materialet.",
            "At den begrænsede kapacitet i ét trin bremser hele forløbet.",
        ],
        "At den begrænsede kapacitet i ét trin bremser hele forløbet.",
    ),
    AssessmentQuestion(
        "da-v-b2-003",
        "vocabulary",
        "B2",
        "En beboer vil gøre indsigelse mod en byggeplan. Hvilken handling passer til ønsket?",
        [
            "At sende en begrundet protest mod en del af planen.",
            "At bestille en kopi for at følge med uden at kommentere.",
            "At melde sig som frivillig til byggearbejdet.",
            "At erklære sin støtte til planen uden forbehold.",
        ],
        "At sende en begrundet protest mod en del af planen.",
    ),
    AssessmentQuestion(
        "da-v-b2-004",
        "vocabulary",
        "B2",
        "Du leder et møde. To deltagere bruger ordet fleksibilitet om henholdsvis "
        "arbejdstid og opgavevalg. Hvilken bemærkning hjælper bedst med at afklare "
        "deres uenighed?",
        [
            "Lad os vælge det korteste forslag, så vi kan komme videre.",
            "I er enige om ordet, så vi behøver ikke flere forklaringer.",
            "Måske taler vi forbi hinanden; hvad vil hver af jer kunne ændre?",
            "Begge forslag er lige uklare, så vi tager dem af dagsordenen.",
        ],
        "Måske taler vi forbi hinanden; hvad vil hver af jer kunne ændre?",
    ),
    AssessmentQuestion(
        "da-r-b2-001",
        "reading",
        "B2",
        "Læs uddraget: Forsøget med længere åbningstid gav flere besøg om aftenen. "
        "Det samlede besøgstal steg dog kun lidt, fordi nogle gæster flyttede deres "
        "besøg fra eftermiddagen. Biblioteket fortsætter forsøget, men vil undersøge "
        "omkostningen pr. ekstra besøgende. Hvilken konklusion er bedst underbygget?",
        [
            "De fleste aftenbesøg kom fra helt nye brugere.",
            "Det højere aftental beviser, at ordningen allerede betaler sig.",
            "Biblioteket har besluttet at erstatte eftermiddagsåbningen.",
            "Aftentallet alene viser ikke, hvor stor den samlede gevinst er.",
        ],
        "Aftentallet alene viser ikke, hvor stor den samlede gevinst er.",
    ),
    AssessmentQuestion(
        "da-r-b2-002",
        "reading",
        "B2",
        "Læs mailen: Vi kan fastholde den tilbudte pris, hvis I bekræfter bestillingen "
        "senest fredag. Levering i uge 12 er fortsat vores mål, men afhænger af, at "
        "komponenterne kommer som varslet. Vi giver en ny status mandag. "
        "Hvad kan kunden med rimelighed lægge til grund?",
        [
            "En rettidig bekræftelse sikrer prisen, men ikke nødvendigvis leveringsugen.",
            "En bekræftelse fredag sikrer både prisen og ubetinget levering i uge 12.",
            "Prisen kan først fastlægges mandag, uanset hvornår kunden bekræfter.",
            "Levering i uge 12 er opgivet, selv hvis komponenterne kommer til tiden.",
        ],
        "En rettidig bekræftelse sikrer prisen, men ikke nødvendigvis leveringsugen.",
    ),
    AssessmentQuestion(
        "da-r-b2-003",
        "reading",
        "B2",
        "Læs referatet: Udvalget støttede behovet for et nyt samlingssted. Placeringen "
        "blev ikke godkendt, da adgangsforholdene endnu ikke var undersøgt. "
        "Forvaltningen blev bedt om at belyse to mulige adresser før næste møde. "
        "Hvilken overskrift gengiver beslutningen loyalt?",
        [
            "Udvalget afviser behovet for et nyt samlingssted",
            "To samlingssteder godkendt med fælles adgangsvej",
            "Opbakning til samlingssted, men placeringen afventer undersøgelse",
            "Forvaltningen får lov til selv at vælge den endelige adresse",
        ],
        "Opbakning til samlingssted, men placeringen afventer undersøgelse",
    ),
    AssessmentQuestion(
        "da-r-b2-004",
        "reading",
        "B2",
        "Læs: Sofie siger, at den nye vagtplan giver hende mindre fleksibilitet. "
        "Lederen svarer, at alle nu har lige mange aftenvagter. Sofie forklarer, "
        "at hun ikke ønsker færre aftenvagter, men mulighed for at bytte dem med "
        "kort varsel. Hvad bør samtalen nu handle om?",
        [
            "Om Sofie skal have færre aftenvagter end kollegerne.",
            "Om reglerne for vagtbytte kan ændres uden at ændre fordelingen.",
            "Om lederen har regnet antallet af aftenvagter forkert sammen.",
            "Om alle aftenvagter kan afskaffes i den næste plan.",
        ],
        "Om reglerne for vagtbytte kan ændres uden at ændre fordelingen.",
    ),
    AssessmentQuestion(
        "da-r-b2-005",
        "reading",
        "B2",
        "Læs: En undersøgelse viser, at 62 procent af de adspurgte støtter den nye "
        "buslinje. Deltagerne blev rekrutteret ved busstoppesteder i myldretiden. "
        "Rapporten anbefaler en bredere undersøgelse, før man beskriver resultatet "
        "som hele byens holdning. Hvorfor er anbefalingen relevant?",
        [
            "Resultatet bør især læses som en sammenligning af morgen- og aftenrejsende.",
            "Rapporten viser, at busbrugere og andre borgere vurderer forslaget forskelligt.",
            "Den oplyste andel kan bruges som et præcist mål for hele byens opbakning.",
            "Udvælgelsen kan have givet bestemte brugergrupper for stor vægt.",
        ],
        "Udvælgelsen kan have givet bestemte brugergrupper for stor vægt.",
    ),
    AssessmentQuestion(
        "da-r-b2-006",
        "reading",
        "B2",
        "Læs svaret: Tak for forslaget. Det er da spændende, men jeg er ikke helt "
        "overbevist om, at vi har folk nok til at gennemføre det allerede i marts. "
        "Kunne vi begynde med én afdeling? Hvordan bør modtageren forstå svaret?",
        [
            "Som et tilsagn om at begynde i marts, hvis der først bliver ansat flere.",
            "Som et ønske om at udsætte hele forslaget, indtil bemandingen er øget.",
            "Som interesse kombineret med en bemandingsbekymring og et mindre første skridt.",
            "Som en godkendelse af opstart i én afdeling med den nuværende bemanding.",
        ],
        "Som interesse kombineret med en bemandingsbekymring og et mindre første skridt.",
    ),
    AssessmentQuestion(
        "da-r-b2-007",
        "reading",
        "B2",
        "Læs: Under mødet lovede Emil at sende leverandørens svar videre til Asta. "
        "Asta skulle derefter ajourføre budgettet. Svaret er kommet, men Asta "
        "har endnu ikke modtaget det og mangler derfor de nye priser. "
        "Hvilken opfølgning svarer til den aftalte ansvarsfordeling?",
        [
            "Asta skal opdatere budgettet uden priser, så Emil kan sende det til leverandøren.",
            "Emil skal videresende svaret, så Asta kan opdatere budgettet på det aftalte grundlag.",
            "Leverandøren skal overtage Astas opgave og skrive et helt nyt budget.",
            "Asta skal minde Emil om, at han selv lovede at opdatere budgettet.",
        ],
        "Emil skal videresende svaret, så Asta kan opdatere budgettet på det aftalte grundlag.",
    ),
    AssessmentQuestion(
        "da-r-b2-008",
        "reading",
        "B2",
        "Læs: Beboerne ønskede mere ro i gården, mens caféen ønskede at bevare "
        "udeserveringen. Parterne aftalte, at serveringen fortsætter, men stopper "
        "en time tidligere. Efter to måneder vurderer de sammen støjniveauet "
        "og behovet for yderligere ændringer. Hvad kendetegner løsningen?",
        [
            "Den giver begge parter noget og gør plads til en senere fælles vurdering.",
            "Den opfylder caféens ønske uden at ændre dens tidligere åbningstid.",
            "Den erstatter udeserveringen med en permanent lukning af gården.",
            "Den udsætter enhver ændring, indtil parterne har målt støjen i to måneder.",
        ],
        "Den giver begge parter noget og gør plads til en senere fælles vurdering.",
    ),
]
