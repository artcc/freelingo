"""Danish A2 placement items with contextual readings and balanced answer positions."""

from app.data._types import AssessmentQuestion

A2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "da-g-a2-001",
        "grammar",
        "A2",
        "Fortæl i datid om rejsen: I går ___ vi på færgen i en time.",
        ["ventede", "vente", "venter", "ventet"],
        "ventede",
        "da-past-a2",
    ),
    AssessmentQuestion(
        "da-g-a2-002",
        "grammar",
        "A2",
        "Vælg hjælpeverbet i almindeligt standarddansk: Lea ___ lige kommet hjem fra arbejde.",
        ["har", "bliver", "er", "skal"],
        "er",
        "da-perfect-a2",
    ),
    AssessmentQuestion(
        "da-g-a2-003",
        "grammar",
        "A2",
        "Hvilket udtryk passer i sætningen: Vi overtager ___ på fredag?",
        ["den nye lejligheden", "den nye lejlighed", "den nyt lejlighed", "det nye lejlighed"],
        "den nye lejlighed",
        "da-definite-adjectives-a2",
    ),
    AssessmentQuestion(
        "da-g-a2-004",
        "grammar",
        "A2",
        "Vælg den neutrale ledsætningsordstilling med ikke: Sara melder afbud, ___.",
        [
            "fordi hun har tid ikke",
            "fordi har hun ikke tid",
            "fordi hun ikke tid har",
            "fordi hun ikke har tid",
        ],
        "fordi hun ikke har tid",
        "da-subordinate-a2",
    ),
    AssessmentQuestion(
        "da-g-a2-005",
        "grammar",
        "A2",
        "Kortet tilhører Amina selv: Amina tager ___ eget sundhedskort med til lægen.",
        ["sin", "sine", "sit", "sig"],
        "sit",
        "da-reflexive-possessive-a2",
    ),
    AssessmentQuestion(
        "da-g-a2-006",
        "grammar",
        "A2",
        "Hvilket indirekte spørgsmål har almindelig dansk ordstilling?",
        [
            "Ved du, hvornår kurset begynder?",
            "Ved du, hvornår begynder kurset?",
            "Ved du, begynder hvornår kurset?",
            "Ved du, kurset hvornår begynder?",
        ],
        "Ved du, hvornår kurset begynder?",
        "da-indirect-question-a2",
    ),
    AssessmentQuestion(
        "da-g-a2-007",
        "grammar",
        "A2",
        "Værelse A er 15 m², og værelse B er 10 m². Værelse A er ___ værelse B.",
        ["store som", "stor end", "størst end", "større end"],
        "større end",
        "da-comparison-a2",
    ),
    AssessmentQuestion(
        "da-g-a2-008",
        "grammar",
        "A2",
        "Det er mandag, og pakken skal komme onsdag: Pakken ankommer ___ to dage.",
        ["for", "om", "siden", "under"],
        "om",
        "da-time-prepositions-a2",
    ),
    AssessmentQuestion(
        "da-v-a2-001",
        "vocabulary",
        "A2",
        "Du betaler hver måned for at bo i en anden persons lejlighed. "
        "Hvad kaldes den person, som lejer boligen ud til dig?",
        ["en lejer", "en deltager", "en udlejer", "en træner"],
        "en udlejer",
    ),
    AssessmentQuestion(
        "da-v-a2-002",
        "vocabulary",
        "A2",
        "Du vil se, hvor mange penge der står på din bankkonto lige nu. Hvad skal du kigge efter?",
        ["saldoen", "rabatten", "lønnen", "gebyret"],
        "saldoen",
    ),
    AssessmentQuestion(
        "da-v-a2-003",
        "vocabulary",
        "A2",
        "Du skal møde op hos kommunen med legitimation for at få hjælp til et nyt pas. "
        "Hvilket sted passer til dette ærinde?",
        ["et vaskeri", "et apotek", "et vandrerhjem", "borgerservice"],
        "borgerservice",
    ),
    AssessmentQuestion(
        "da-v-a2-004",
        "vocabulary",
        "A2",
        "Du kender ordets betydning og stavning, men er usikker på lydene, når du siger det. "
        "Hvad vil du især øve?",
        ["din underskrift", "din udtale", "din ansøgning", "din tilmelding"],
        "din udtale",
    ),
    AssessmentQuestion(
        "da-v-a2-005",
        "vocabulary",
        "A2",
        "Trøjen er for stor. Du ønsker den samme model i en mindre størrelse, ikke pengene tilbage. "
        "Hvad vil du gøre?",
        ["Bytte trøjen.", "Reservere trøjen.", "Betale for trøjen.", "Reparere trøjen."],
        "Bytte trøjen.",
    ),
    AssessmentQuestion(
        "da-v-a2-006",
        "vocabulary",
        "A2",
        "Du har en tid hos lægen i morgen, men kan ikke komme. Hvilken besked skal du give?",
        ["En invitation.", "En tilmelding.", "Et afbud.", "En fuldmagt."],
        "Et afbud.",
    ),
    AssessmentQuestion(
        "da-v-a2-007",
        "vocabulary",
        "A2",
        "Klubben beder alle medlemmer betale 400 kroner om året for medlemskabet. "
        "Hvad kaldes betalingen?",
        ["et depositum", "et kontingent", "en tilbagebetaling", "en husleje"],
        "et kontingent",
    ),
    AssessmentQuestion(
        "da-v-a2-008",
        "vocabulary",
        "A2",
        "En busafgang er aflyst. Hvad betyder det?",
        [
            "Den kører fra et andet stoppested.",
            "Den kører med færre siddepladser.",
            "Den kører senere end planlagt.",
            "Den bliver ikke gennemført.",
        ],
        "Den bliver ikke gennemført.",
    ),
    AssessmentQuestion(
        "da-r-a2-001",
        "reading",
        "A2",
        "Bolig A koster 6.000 kr. om måneden inklusive varme og vand. Bolig B koster "
        "5.700 kr., og varme og vand er yderligere 700 kr. om måneden. El er ikke "
        "medregnet i nogen af priserne. Hvilken sammenligning er rigtig, når el holdes udenfor?",
        [
            "Bolig A koster 300 kr. mere om måneden.",
            "De to boliger koster det samme om måneden.",
            "Bolig B koster 400 kr. mere om måneden.",
            "Bolig B koster 700 kr. mindre om måneden.",
        ],
        "Bolig B koster 400 kr. mere om måneden.",
    ),
    AssessmentQuestion(
        "da-r-a2-002",
        "reading",
        "A2",
        "Kursuslederen skriver: Vi mødes som aftalt klokken 18, men lokale 4 er "
        "optaget. Gå derfor til lokale 7 på første sal. Sluttidspunktet er stadig "
        "19.30. Hvad skal deltagerne ændre?",
        [
            "Det lokale, de går til.",
            "Det tidspunkt, de møder.",
            "Den dag, de kommer.",
            "Det tidspunkt, de går hjem.",
        ],
        "Det lokale, de går til.",
    ),
    AssessmentQuestion(
        "da-r-a2-003",
        "reading",
        "A2",
        "En forening skriver: På søndag spiser vi sammen i gården. Tilmeld dig senest "
        "torsdag. Vi køber mad efter antallet af tilmeldte. Tag selv en tallerken og "
        "bestik med. Amir vil deltage. Hvad skal han gøre?",
        [
            "Købe mad til hele gruppen og møde op uden tilmelding.",
            "Tilmelde sig søndag og låne bestik ved ankomsten.",
            "Betale for en tallerken og vente på en invitation.",
            "Give besked senest torsdag og medbringe noget at spise af.",
        ],
        "Give besked senest torsdag og medbringe noget at spise af.",
    ),
    AssessmentQuestion(
        "da-r-a2-004",
        "reading",
        "A2",
        "Lea skriver: Jeg er ikke hjemme, når håndværkeren kommer. Min nabo Mads "
        "har nøglen og lukker ham ind. Jeg er hjemme igen klokken 16. "
        "Hvad kan håndværkeren gøre før klokken 16 ifølge aftalen?",
        [
            "Hente nøglen på Leas arbejde.",
            "Få adgang til boligen gennem Mads.",
            "Bede Lea komme hjem med nøglen.",
            "Gå ind gennem den ulåste hoveddør.",
        ],
        "Få adgang til boligen gennem Mads.",
    ),
]
