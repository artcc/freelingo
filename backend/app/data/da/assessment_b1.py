"""Danish B1 placement items with contextualised, balanced answer positions."""

from app.data._types import AssessmentQuestion

B1_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "da-g-b1-001",
        "grammar",
        "B1",
        "Vælg neutral skriftlig ordstilling: Vi flytter mødet, fordi Maja ___.",
        [
            "kan ikke deltage",
            "ikke kan deltage",
            "ikke deltage kan",
            "deltage ikke kan",
        ],
        "ikke kan deltage",
        "da-subordinate-negation-b1",
    ),
    AssessmentQuestion(
        "da-g-b1-002",
        "grammar",
        "B1",
        "Mikkel og Jonas har hver en cykel. Mikkel vil låne Jonas' cykel. "
        "Hvilken sætning beskriver det?",
        [
            "Mikkel vil låne sin cykel af Jonas.",
            "Jonas vil låne Mikkels cykel.",
            "Mikkel vil låne sin cykel ud til Jonas.",
            "Mikkel vil låne hans cykel.",
        ],
        "Mikkel vil låne hans cykel.",
        "da-reflexive-possession-b1",
    ),
    AssessmentQuestion(
        "da-g-b1-003",
        "grammar",
        "B1",
        "Der er tale om en vane, som stadig gælder: Jeg ___ gå en tur efter aftensmaden.",
        [
            "plejer at",
            "plejede",
            "plejer til",
            "plejede på",
        ],
        "plejer at",
        "da-habits-b1",
    ),
    AssessmentQuestion(
        "da-g-b1-004",
        "grammar",
        "B1",
        "Læs: Da jeg kom til mødet, havde de fordelt opgaverne. Hvad skete først?",
        [
            "Jeg kom, og bagefter begyndte de at fordele opgaverne.",
            "Jeg fordelte opgaverne, før de andre kom.",
            "De fordelte opgaverne, før jeg kom.",
            "Vi fordelte opgaverne, mens jeg kom ind.",
        ],
        "De fordelte opgaverne, før jeg kom.",
        "da-pluperfect-b1",
    ),
    AssessmentQuestion(
        "da-g-b1-005",
        "grammar",
        "B1",
        "Værkstedet skriver: Cyklen er først klar på torsdag. " "Hvilken plan passer med beskeden?",
        [
            "Jeg kan hente den onsdag, hvis jeg kommer sent.",
            "Jeg skal hente den senest onsdag aften.",
            "Jeg må finde anden transport indtil torsdag.",
            "Jeg kan kun hente den før torsdag.",
        ],
        "Jeg må finde anden transport indtil torsdag.",
        "da-time-limits-b1",
    ),
    AssessmentQuestion(
        "da-g-b1-006",
        "grammar",
        "B1",
        "Du spørger, om der kommer flere til fællesspisningen. "
        "Arrangøren svarer: Der kommer nok nogle efter arbejde. Hvad udtrykker nok her?",
        [
            "En forventning, som arrangøren ikke gør helt sikker.",
            "En bekræftelse på, at alle allerede er kommet.",
            "En oplysning om, at der er mad nok til alle.",
            "Et krav om, at deltagerne skal arbejde først.",
        ],
        "En forventning, som arrangøren ikke gør helt sikker.",
        "da-particles-jo-nok-b1",
    ),
    AssessmentQuestion(
        "da-g-b1-007",
        "grammar",
        "B1",
        "Omskriv uden at ændre tid eller ansvar: Viceværten reparerede låsen i går.",
        [
            "Låsen bliver repareret af viceværten i morgen.",
            "Låsen blev repareret af en låsesmed i går.",
            "Låsen skulle repareres af viceværten i går.",
            "Låsen blev repareret af viceværten i går.",
        ],
        "Låsen blev repareret af viceværten i går.",
        "da-blive-passive-b1",
    ),
    AssessmentQuestion(
        "da-g-b1-008",
        "grammar",
        "B1",
        "Du vil vide, om aflevering på papir er nødvendig. "
        "Vælg et korrekt indirekte spørgsmål: Kan du sige mig, ___?",
        [
            "om skal vi aflevere på papir",
            "om vi skal aflevere på papir",
            "skal om vi aflevere på papir",
            "om vi aflevere skal på papir",
        ],
        "om vi skal aflevere på papir",
        "da-indirect-questions-b1",
    ),
    AssessmentQuestion(
        "da-v-b1-001",
        "vocabulary",
        "B1",
        "Brevet siger: Vedhæft en kopi af lejekontrakten. Hvad skal du gøre?",
        [
            "Aflevere nøglerne sammen med kontrakten.",
            "Skrive en ny kontrakt med samme betingelser.",
            "Tilføje kopien som en fil til din henvendelse.",
            "Fjerne kopien fra den gemte henvendelse.",
        ],
        "Tilføje kopien som en fil til din henvendelse.",
    ),
    AssessmentQuestion(
        "da-v-b1-002",
        "vocabulary",
        "B1",
        "En kollega siger: Jeg kan afløse dig ved skranken, mens du holder pause. "
        "Hvad tilbyder kollegaen?",
        [
            "At overtage din opgave i en kort periode.",
            "At tage sin egen pause samtidig med dig.",
            "At flytte skranken til et andet lokale.",
            "At forklare dig, hvor skranken skal stå.",
        ],
        "At overtage din opgave i en kort periode.",
    ),
    AssessmentQuestion(
        "da-v-b1-003",
        "vocabulary",
        "B1",
        "Efter flytningen siger Nanna: Jeg er begyndt at falde til. Hvad mener hun?",
        [
            "Hun overvejer at flytte tilbage til sin gamle by.",
            "Hun er blevet usikker på, hvor hun skal bo.",
            "Hun er faldet på trappen i den nye opgang.",
            "Hun føler sig mere hjemme i sine nye omgivelser.",
        ],
        "Hun føler sig mere hjemme i sine nye omgivelser.",
    ),
    AssessmentQuestion(
        "da-v-b1-004",
        "vocabulary",
        "B1",
        "Klubben skriver: Kontingentet betales halvårligt. Hvad betaler medlemmerne for?",
        [
            "En bøde for at aflyse en træning.",
            "Deres medlemskab af klubben.",
            "En billet til en bestemt kamp.",
            "Et lån af en træners private bil.",
        ],
        "Deres medlemskab af klubben.",
    ),
    AssessmentQuestion(
        "da-v-b1-005",
        "vocabulary",
        "B1",
        "Vejrudsigten lover storm. Vi vil udsætte turen. Hvilken besked passer?",
        [
            "Vi finder en ny dato senere på måneden.",
            "Vi tager af sted tidligere samme morgen.",
            "Vi gennemfører turen som aftalt.",
            "Vi lader en anden gruppe tage med os.",
        ],
        "Vi finder en ny dato senere på måneden.",
    ),
    AssessmentQuestion(
        "da-v-b1-006",
        "vocabulary",
        "B1",
        "Efter måltidet siger værten: Gem resterne, så vi mindsker madspild. Hvad er målet?",
        [
            "At bruge mindre tid på at rydde bordet.",
            "At servere mindre mad for gæsterne næste gang.",
            "At undgå at smide mad ud, som stadig kan spises.",
            "At få gæsterne til at købe deres egen mad.",
        ],
        "At undgå at smide mad ud, som stadig kan spises.",
    ),
    AssessmentQuestion(
        "da-v-b1-007",
        "vocabulary",
        "B1",
        "Naboen spørger: Kan du give en hånd med bordene? Hvilket svar imødekommer ønsket?",
        [
            "Ja, jeg kan fortælle dig, hvad bordene kostede.",
            "Ja, hvilken ende skal jeg tage fat i?",
            "Ja, jeg kan skrive antallet ned til dig.",
            "Ja, jeg kan vise dig et billede af dem.",
        ],
        "Ja, hvilken ende skal jeg tage fat i?",
    ),
    AssessmentQuestion(
        "da-v-b1-008",
        "vocabulary",
        "B1",
        "Butikken skriver: Vi har registreret din reklamation. "
        "Hvad har kunden sandsynligvis henvendt sig om?",
        [
            "Et ønske om at få butikkens reklamer.",
            "En bestilling af en vare til fuld pris.",
            "En ansøgning om arbejde i butikken.",
            "En fejl ved en vare, kunden har købt.",
        ],
        "En fejl ved en vare, kunden har købt.",
    ),
    AssessmentQuestion(
        "da-r-b1-001",
        "reading",
        "B1",
        "Læs opslaget: Vaskeriet er lukket tirsdag fra klokken 8 til 14 på grund af "
        "service. Reservationer i dette tidsrum bliver slettet. Beboerne skal selv "
        "reservere en ny tid. Amina havde bestilt en maskine tirsdag klokken 10. "
        "Hvad skal hun gøre for at få en anden vasketid?",
        [
            "Møde op klokken 10 og vente på en ledig maskine.",
            "Regne med, at hendes tid automatisk flyttes til klokken 14.",
            "Aflevere vasketøjet til den medarbejder, der udfører service.",
            "Foretage en ny reservation uden for lukkeperioden.",
        ],
        "Foretage en ny reservation uden for lukkeperioden.",
    ),
    AssessmentQuestion(
        "da-r-b1-002",
        "reading",
        "B1",
        "Læs beskeden: Hej Søren. Jeg kan godt tage din lørdagsvagt, hvis du tager "
        "min vagt næste onsdag. Jeg skal dog gå senest klokken 15 på lørdag. "
        "Kan du spørge lederen, om det kan lade sig gøre? Hilsen Lea. "
        "Hvad mangler, før byttet er afklaret?",
        [
            "Lea skal først finde ud af, om hun er ledig lørdag.",
            "Søren skal undersøge, om Leas tidlige afgang kan accepteres.",
            "Lederen skal finde en anden til at tage onsdagsvagten.",
            "Søren skal bede Lea om at arbejde hele søndagen.",
        ],
        "Søren skal undersøge, om Leas tidlige afgang kan accepteres.",
    ),
    AssessmentQuestion(
        "da-r-b1-003",
        "reading",
        "B1",
        "Læs: Vi har modtaget din ansøgning, men mangler dokumentation for din "
        "adresse. Send den senest den 18. maj. Vi kan først behandle sagen, når "
        "alle bilag er modtaget. Hvorfor har ansøgeren endnu ikke fået en afgørelse?",
        [
            "Ansøgningen er kommet til den forkerte kommune.",
            "Kommunen har afvist den oplyste adresse.",
            "Kommunen mangler en oplysning, der skal dokumenteres.",
            "Ansøgeren har bedt om at vente til efter den 18. maj.",
        ],
        "Kommunen mangler en oplysning, der skal dokumenteres.",
    ),
    AssessmentQuestion(
        "da-r-b1-004",
        "reading",
        "B1",
        "Læs: Jonas plejede at tage bilen til arbejde. Efter flytningen tager "
        "han toget, fordi han kan læse undervejs. Turen varer lidt længere, "
        "men han synes, at morgenerne er mere rolige nu. "
        "Hvilket hensyn har fået størst betydning for hans valg?",
        [
            "At han kan bruge rejsetiden på en behagelig måde.",
            "At han kommer hurtigere frem end tidligere.",
            "At han ikke længere behøver at møde om morgenen.",
            "At han kan køre kollegerne med i sin bil.",
        ],
        "At han kan bruge rejsetiden på en behagelig måde.",
    ),
    AssessmentQuestion(
        "da-r-b1-005",
        "reading",
        "B1",
        "Læs invitationen: Til fællesspisningen laver køkkenholdet varm mad. "
        "Tag selv tallerken og bestik med. Du må gerne tage kage med, men skriv "
        "det på listen, så vi ikke får for meget. Hvad forventes af alle deltagere?",
        [
            "At de bager en kage og skriver den på listen.",
            "At de medbringer noget at spise af og med.",
            "At de laver en varm ret hjemmefra.",
            "At de melder sig til køkkenholdet.",
        ],
        "At de medbringer noget at spise af og med.",
    ),
    AssessmentQuestion(
        "da-r-b1-006",
        "reading",
        "B1",
        "Læs beskeden fra værkstedet: Vi kan reparere lampen for 350 kroner. "
        "Reservedelen kommer først fredag. Svar inden onsdag klokken 12, hvis "
        "du vil have os til at bestille den. Hvornår skal kunden handle?",
        [
            "Når reservedelen er ankommet fredag.",
            "Efter at lampen er blevet repareret.",
            "Onsdag eftermiddag, når prisen er kendt.",
            "Inden onsdag middag for at godkende bestillingen.",
        ],
        "Inden onsdag middag for at godkende bestillingen.",
    ),
    AssessmentQuestion(
        "da-r-b1-007",
        "reading",
        "B1",
        "Læs: Aftenkurset blev flyttet til et lokale på anden sal. Fatima kan "
        "ikke gå på trapper. Underviseren skrev, at der er elevator ved "
        "bagindgangen, og at han kan vise hende vej første gang. "
        "Hvilken løsning beskriver teksten?",
        [
            "Fatima kan nå det nye lokale via en anden indgang.",
            "Holdet flytter tilbage til det oprindelige lokale.",
            "Underviseren tilbyder Fatima undervisning hjemme.",
            "Fatima skal vente, til der bliver bygget en elevator.",
        ],
        "Fatima kan nå det nye lokale via en anden indgang.",
    ),
    AssessmentQuestion(
        "da-r-b1-008",
        "reading",
        "B1",
        "Læs: Til arbejdsdagen skal hegnet males, og gården skal ryddes. "
        "Hvis det regner, rydder vi i stedet op i kælderen. Frokosten holdes "
        "i fælleshuset uanset vejret. Lørdag morgen regner det kraftigt. "
        "Hvilket program følger opslaget?",
        [
            "Maling af hegnet og derefter frokost udendørs.",
            "Oprydning i gården, mens frokosten bliver aflyst.",
            "Oprydning i kælderen og frokost i fælleshuset.",
            "Aflysning af både arbejdet og den fælles frokost.",
        ],
        "Oprydning i kælderen og frokost i fælleshuset.",
    ),
]
