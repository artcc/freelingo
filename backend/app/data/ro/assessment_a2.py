"""Romanian A2 placement: eight questions per skill with balanced answer positions."""

from app.data._types import AssessmentQuestion

A2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "ro-g-a2-001",
        "grammar",
        "A2",
        "Completează relatarea Anei și a Ioanei: «Noi am ___ ieri din Brașov.»",
        ["venit", "venite", "venea", "venim"],
        "venit",
        "ro-perfect-a2",
    ),
    AssessmentQuestion(
        "ro-g-a2-002",
        "grammar",
        "A2",
        "Vorbești despre tine: «Ieri ___ trezit la șase, apoi am plecat la gară.»",
        ["s-a", "te-ai", "m-am", "v-ați"],
        "m-am",
        "ro-reflexive-perfect-a2",
    ),
    AssessmentQuestion(
        "ro-g-a2-003",
        "grammar",
        "A2",
        "Completează cu numele posesoarei, în româna standard: «Aceasta este camera ___.»",
        ["Maria", "Mariei", "pe Maria", "cu Maria"],
        "Mariei",
        "ro-genitive-a2",
    ),
    AssessmentQuestion(
        "ro-g-a2-004",
        "grammar",
        "A2",
        "Mesajul este pentru vecinii mei, adică pentru ei: «___ trimit un mesaj.»",
        ["Îmi", "Îți", "Îi", "Le"],
        "Le",
        "ro-dative-clitics-a2",
    ),
    AssessmentQuestion(
        "ro-g-a2-005",
        "grammar",
        "A2",
        "Răspunzi despre cererea depusă ieri. Alege forma standard.",
        ["L-am depus ieri.", "O am depus ieri.", "Am depus-o ieri.", "Am depuse-o ieri."],
        "Am depus-o ieri.",
        "ro-perfect-clitics-a2",
    ),
    AssessmentQuestion(
        "ro-g-a2-006",
        "grammar",
        "A2",
        "Nu găsești niciun angajat în magazin. Completează: «Nimeni ___ la casă.»",
        ["nu este", "nu sunt", "este", "sunt"],
        "nu este",
        "ro-negative-pronouns-a2",
    ),
    AssessmentQuestion(
        "ro-g-a2-007",
        "grammar",
        "A2",
        "Te adresezi singur recepționerei și formulezi o cerere politicoasă: «___ dori o cameră.»",
        ["Ai", "Ați", "Ar", "Aș"],
        "Aș",
        "ro-polite-conditional-a2",
    ),
    AssessmentQuestion(
        "ro-g-a2-008",
        "grammar",
        "A2",
        "Completează în româna standard: «Acesta este traseul ___ îl alegem pentru excursie.»",
        ["care", "pe care", "cui", "unde"],
        "pe care",
        "ro-relative-care-a2",
    ),
    AssessmentQuestion(
        "ro-v-a2-001",
        "vocabulary",
        "A2",
        "Cum se numește suma pe care o plătești lunar pentru a locui în apartamentul altei persoane?",
        ["Salariu.", "Rest.", "Chirie.", "Reducere."],
        "Chirie.",
    ),
    AssessmentQuestion(
        "ro-v-a2-002",
        "vocabulary",
        "A2",
        "La magazin vrei să schimbi o cămașă. Vânzătoarea cere dovada cumpărării. Ce îi arăți?",
        ["Bonul.", "Programul.", "Formularul de înscriere.", "Pașaportul."],
        "Bonul.",
    ),
    AssessmentQuestion(
        "ro-v-a2-003",
        "vocabulary",
        "A2",
        "Ai stabilit o vizită la medic pentru marți la ora nouă. Ce ai făcut?",
        ["O reparație.", "O copie.", "O reducere.", "O programare."],
        "O programare.",
    ),
    AssessmentQuestion(
        "ro-v-a2-004",
        "vocabulary",
        "A2",
        "Întâlnirea nu mai este vineri, ci luni. Ea va avea totuși loc. Ce face echipa?",
        ["Anulează întâlnirea.", "Amână întâlnirea.", "Refuză întâlnirea.", "Începe întâlnirea."],
        "Amână întâlnirea.",
    ),
    AssessmentQuestion(
        "ro-v-a2-005",
        "vocabulary",
        "A2",
        "Vrei să mergi de la Iași la București și apoi să revii la Iași. Ce fel de bilet ceri?",
        ["Dus-întors.", "Doar dus.", "De intrare la muzeu.", "Abonament lunar de autobuz."],
        "Dus-întors.",
    ),
    AssessmentQuestion(
        "ro-v-a2-006",
        "vocabulary",
        "A2",
        "Înainte de plecare, pui hainele în geanta mare cu roți. În ce le pui?",
        ["În dulap.", "În rucsac.", "În pungă.", "În valiză."],
        "În valiză.",
    ),
    AssessmentQuestion(
        "ro-v-a2-007",
        "vocabulary",
        "A2",
        "Poți lua doar jumătate din cantitatea de făină dintr-o pungă de un kilogram. Cât iei?",
        ["O sută de grame.", "Cinci sute de grame.", "Două sute de grame.", "O mie de grame."],
        "Cinci sute de grame.",
        "ro-quantities-a2",
    ),
    AssessmentQuestion(
        "ro-v-a2-008",
        "vocabulary",
        "A2",
        "Pantofii te strâng și te dor picioarele când mergi. Vrei altă pereche. Ce ceri?",
        [
            "O pereche mai elegantă.",
            "O pereche mai închisă la culoare.",
            "O pereche mai comodă.",
            "O pereche mai lucioasă.",
        ],
        "O pereche mai comodă.",
        "ro-comparison-a2",
    ),
    AssessmentQuestion(
        "ro-r-a2-001",
        "reading",
        "A2",
        "Citește mesajul pensiunii: «Camera este pregătită de la ora 15. Dacă "
        "ajungeți mai devreme, puteți lăsa bagajele la recepție și puteți reveni "
        "după plimbare. Micul dejun se servește de la 7 la 9. În ziua plecării, "
        "vă rugăm să eliberați camera până la 11.» Ana ajunge la 12. Ce poate face atunci?",
        [
            "Poate intra imediat în camera rezervată.",
            "Poate lăsa valiza și poate ieși în oraș.",
            "Poate lua micul dejun la pensiune.",
            "Trebuie să plece cu bagajele până la 15.",
        ],
        "Poate lăsa valiza și poate ieși în oraș.",
    ),
    AssessmentQuestion(
        "ro-r-a2-002",
        "reading",
        "A2",
        "Citește: «Când eram copil, mergeam vara la bunici cu autobuzul. Drumul "
        "dura două ore și plecam devreme. Anul trecut am mers cu mașina și am "
        "ajuns într-o oră. Casa bunicilor este aceeași, dar acum în sat există "
        "și o farmacie.» Ce s-a schimbat la ultima călătorie descrisă?",
        [
            "Persoana a plecat la bunici în alt anotimp.",
            "Bunicii locuiau într-o altă casă din sat.",
            "Autobuzul a făcut drumul într-o singură oră.",
            "Persoana a folosit alt transport și a ajuns mai repede.",
        ],
        "Persoana a folosit alt transport și a ajuns mai repede.",
        "ro-imperfect-a2",
    ),
    AssessmentQuestion(
        "ro-r-a2-003",
        "reading",
        "A2",
        "Citește mesajul proprietarului: «Instalatorul poate veni marți între "
        "10 și 12. Știu că ești la serviciu atunci. Eu pot să îl aștept în "
        "apartament, dar am nevoie de cheie. Dacă ești de acord, las-o luni "
        "la vecina de la parter și spune-mi.» Ce trebuie să facă chiriașul "
        "pentru a accepta această soluție?",
        [
            "Să lase cheia vecinei și să anunțe proprietarul.",
            "Să rămână obligatoriu acasă marți dimineața.",
            "Să îi ceară vecinei să facă reparația luni.",
            "Să ducă cheia instalatorului marți după serviciu.",
        ],
        "Să lase cheia vecinei și să anunțe proprietarul.",
        "ro-dative-a2",
    ),
    AssessmentQuestion(
        "ro-r-a2-004",
        "reading",
        "A2",
        "Citește anunțul: «Pentru înscriere aveți nevoie de formularul completat, "
        "de actul de identitate în original și de o copie. Originalul se "
        "restituie imediat după verificare. Copia rămâne la dosar. Ghișeul "
        "este deschis până la ora 14.» Mihai are formularul și originalul, "
        "dar nu are copia. Ce îi lipsește?",
        [
            "Un alt formular, fără date completate.",
            "Un al doilea act de identitate în original.",
            "O reproducere a actului pentru dosar.",
            "O confirmare că originalul va rămâne la ghișeu.",
        ],
        "O reproducere a actului pentru dosar.",
    ),
    AssessmentQuestion(
        "ro-r-a2-005",
        "reading",
        "A2",
        "Citește: «Geaca albastră costă 180 de lei și se poate spăla acasă. "
        "Geaca verde costă 150 de lei, dar trebuie curățată la un serviciu "
        "specializat. Ambele sunt disponibile în mărimea Anei. Ana are "
        "200 de lei și vrea o geacă pe care să o poată spăla singură.» "
        "Ce alegere respectă ambele condiții ale Anei?",
        [
            "Geaca verde, pentru că are prețul mai mic.",
            "Oricare geacă, fiindcă ambele au aceeași întreținere.",
            "Nicio geacă, fiindcă ambele depășesc suma disponibilă.",
            "Geaca albastră, care se încadrează în buget și se spală acasă.",
        ],
        "Geaca albastră, care se încadrează în buget și se spală acasă.",
        "ro-comparison-a2",
    ),
    AssessmentQuestion(
        "ro-r-a2-006",
        "reading",
        "A2",
        "Citește schimbul de mesaje: «Vrei să mergem la film vineri la șase?» "
        "«Aș vrea, dar termin serviciul abia la șase și jumătate. Pot ajunge "
        "la cinema la șapte. Sâmbătă sunt plecată.» «Există și o proiecție "
        "vineri la opt.» Ce propunere este potrivită pentru programul ei?",
        [
            "Filmul de vineri, de la șase.",
            "Filmul de vineri, de la opt.",
            "O proiecție sâmbătă după-amiază.",
            "O proiecție vineri înainte de șase.",
        ],
        "Filmul de vineri, de la opt.",
        "ro-polite-conditional-a2",
    ),
    AssessmentQuestion(
        "ro-r-a2-007",
        "reading",
        "A2",
        "Citește instrucțiunile: «De la gară, mergeți drept până la semafor. "
        "Traversați strada, apoi faceți la stânga. Muzeul este după bibliotecă, "
        "pe partea dreaptă. Nu intrați pe ușa din față: intrarea pentru "
        "vizitatori este în curte.» Ce trebuie să facă un vizitator ajuns "
        "în fața muzeului?",
        [
            "Să folosească ușa dinspre stradă.",
            "Să intre prin clădirea bibliotecii.",
            "Să caute accesul din curte.",
            "Să revină la semafor înainte de intrare.",
        ],
        "Să caute accesul din curte.",
        "ro-imperative-a2",
    ),
    AssessmentQuestion(
        "ro-r-a2-008",
        "reading",
        "A2",
        "Citește: «Am cumpărat bilete pentru excursia de sâmbătă. Astăzi "
        "organizatorul ne-a anunțat că va ploua puternic, deci excursia nu "
        "mai are loc. Putem primi banii înapoi sau putem folosi biletele "
        "duminica viitoare. Noi suntem plecați atunci și am cerut restituirea "
        "banilor.» De ce au ales persoanele această variantă?",
        [
            "Nu pot participa la data oferită în locul celei inițiale.",
            "Organizatorul nu permite folosirea biletelor altă dată.",
            "Au decis să participe sâmbătă, chiar dacă plouă.",
            "Au cumpărat din greșeală bilete pentru duminică.",
        ],
        "Nu pot participa la data oferită în locul celei inițiale.",
        "ro-connectors-a2",
    ),
]
