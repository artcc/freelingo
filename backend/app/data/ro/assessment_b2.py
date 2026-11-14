"""Romanian B2 placement questions with contextual distinctions and balanced keys."""

from app.data._types import AssessmentQuestion

B2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "ro-g-b2-001",
        "grammar",
        "B2",
        "Nu știm dacă echipa a primit mesajul trimis ieri. Completați ipoteza "
        "referitoare la o acțiune anterioară: «E posibil ca ei să ___ mesajul, "
        "dar încă nu avem confirmarea.»",
        ["primesc", "fi primit", "fie primit", "vor primi"],
        "fi primit",
        "ro-subjunctive-perfect-b2",
    ),
    AssessmentQuestion(
        "ro-g-b2-002",
        "grammar",
        "B2",
        "Nu am modernizat clădirea anul trecut, iar acum plătim mult pentru încălzire. "
        "Care reformulare leagă alternativa trecută de un efect prezent?",
        [
            "Dacă modernizăm clădirea acum, am fi plătit mai puțin anul trecut.",
            "Dacă am fi modernizat clădirea, am fi plătit mai puțin anul trecut.",
            "Dacă am moderniza clădirea anul viitor, am plăti mai puțin după lucrări.",
            "Dacă am fi modernizat clădirea anul trecut, acum am plăti mai puțin.",
        ],
        "Dacă am fi modernizat clădirea anul trecut, acum am plăti mai puțin.",
        "ro-mixed-conditions-b2",
    ),
    AssessmentQuestion(
        "ro-g-b2-003",
        "grammar",
        "B2",
        "Completați ambele acorduri: «Am contactat asociația ___ membri au "
        "propus amenajarea curții.»",
        ["ai cărei", "ale cărei", "ai căror", "al cărei"],
        "ai cărei",
        "ro-relative-cases-b2",
    ),
    AssessmentQuestion(
        "ro-g-b2-004",
        "grammar",
        "B2",
        "Responsabila spune: «Am verificat documentele primite; mai avem de verificat "
        "doar anexele.» Ce indică expresia «avem de verificat»?",
        [
            "Anexele au fost deja verificate și acceptate.",
            "Anexele au fost verificate, dar trebuie înlocuite.",
            "Verificarea anexelor este o sarcină încă neîncheiată.",
            "Verificarea anexelor a fost eliminată din procedură.",
        ],
        "Verificarea anexelor este o sarcină încă neîncheiată.",
        "ro-supine-b2",
    ),
    AssessmentQuestion(
        "ro-g-b2-005",
        "grammar",
        "B2",
        "După trei apeluri fără răspuns, Mihai spune: «O fi în ședință; "
        "îl mai sun peste o oră.» Ce statut are informația despre ședință?",
        [
            "Este o programare pe care Mihai o confirmă pentru ora următoare.",
            "Este o presupunere prin care Mihai explică lipsa răspunsului.",
            "Este o obligație pe care Mihai i-o transmite persoanei sunate.",
            "Este o informație pe care persoana sunată i-a comunicat-o explicit.",
        ],
        "Este o presupunere prin care Mihai explică lipsa răspunsului.",
        "ro-presumptive-b2",
    ),
    AssessmentQuestion(
        "ro-g-b2-006",
        "grammar",
        "B2",
        "În discuție apar două formulări: «Doar Ana a trimis raportul» și "
        "«Ana a trimis doar raportul». Ce afirmă a doua, fără să afirme și prima?",
        [
            "Restricția privește ce a trimis Ana, nu identitatea tuturor expeditorilor.",
            "Restricția privește cine a trimis raportul, nu celelalte documente.",
            "Ana a trimis raportul și cel puțin încă un document.",
            "Altcineva a trimis raportul în locul Anei.",
        ],
        "Restricția privește ce a trimis Ana, nu identitatea tuturor expeditorilor.",
        "ro-focus-b2",
    ),
    AssessmentQuestion(
        "ro-v-b2-001",
        "vocabulary",
        "B2",
        "La negociere, firma acceptă să livreze cu două zile mai devreme, deși inițial "
        "refuzase acest lucru. În schimb, clientul renunță la plata în trei rate. "
        "Cum se numesc aceste ajustări făcute pentru a facilita acordul?",
        ["Obiecții.", "Penalități.", "Concesii.", "Contestații."],
        "Concesii.",
    ),
    AssessmentQuestion(
        "ro-v-b2-002",
        "vocabulary",
        "B2",
        "O organizație declară: «Susținem în principiu proiectul, dar cerem verificarea "
        "costurilor înainte de aprobarea formei finale.» Ce înseamnă aici «în principiu»?",
        [
            "Acceptă direcția generală, păstrând deschise anumite detalii.",
            "Aprobă toate detaliile, urmând doar să comunice decizia.",
            "Respinge direcția generală, dar acceptă cheltuielile propuse.",
            "Suspendă orice opinie până la începerea lucrărilor.",
        ],
        "Acceptă direcția generală, păstrând deschise anumite detalii.",
    ),
    AssessmentQuestion(
        "ro-v-b2-003",
        "vocabulary",
        "B2",
        "Înainte de a accepta reparația, ceri un document care separă costul pieselor "
        "de costul muncii și estimează suma totală. Ce document soliciți?",
        ["Un proces-verbal de recepție.", "O împuternicire.", "O autorizație.", "Un deviz."],
        "Un deviz.",
    ),
    AssessmentQuestion(
        "ro-v-b2-004",
        "vocabulary",
        "B2",
        "Două asociații au poziții diferite. Tu nu vrei să decizi în locul lor, "
        "ci să le ajuți să clarifice nevoile și să ajungă la o înțelegere. "
        "Ce rol îți propui?",
        [
            "Să contești înțelegerea dintre asociații.",
            "Să mediezi discuția dintre asociații.",
            "Să reprezinți exclusiv una dintre asociații.",
            "Să avizezi oficial hotărârea asociațiilor.",
        ],
        "Să mediezi discuția dintre asociații.",
    ),
    AssessmentQuestion(
        "ro-v-b2-005",
        "vocabulary",
        "B2",
        "Un articol afirmă că un centru se închide. Conducerea publică imediat un comunicat "
        "în care declară informația falsă și anunță programul normal. Ce a făcut conducerea?",
        [
            "A confirmat informația.",
            "A nuanțat motivul închiderii.",
            "A dezmințit informația.",
            "A estimat durata închiderii.",
        ],
        "A dezmințit informația.",
    ),
    AssessmentQuestion(
        "ro-r-b2-001",
        "reading",
        "B2",
        "Citiți nota: «După extinderea programului de seară, biblioteca a înregistrat "
        "mai multe vizite. În aceeași perioadă au început însă și cursurile gratuite "
        "de limbi străine. Datele disponibile nu separă participanții la cursuri de "
        "ceilalți vizitatori. Echipa propune păstrarea temporară a noului program și "
        "colectarea unor date mai detaliate înainte de a decide extinderea permanentă.» "
        "Care concluzie respectă limitele notei?",
        [
            "Creșterea demonstrează că programul de seară este cauza principală.",
            "Cursurile explică întreaga creștere, iar programul nu a avut niciun efect.",
            "Lipsa datelor separate arată că extinderea programului a eșuat.",
            "Creșterea este observată, dar contribuția fiecărei schimbări rămâne neclară.",
        ],
        "Creșterea este observată, dar contribuția fiecărei schimbări rămâne neclară.",
    ),
    AssessmentQuestion(
        "ro-r-b2-002",
        "reading",
        "B2",
        "Furnizorul scrie: «Putem păstra prețul actual dacă primim comanda semnată "
        "până joi. Livrarea în zece zile este posibilă numai după confirmarea stocului. "
        "Semnarea comenzii rezervă prețul, nu și data livrării. Dacă termenul este "
        "esențial pentru dumneavoastră, vă recomandăm să așteptați confirmarea stocului; "
        "în acest caz, prețul ar putea fi recalculat după joi.» "
        "Ce compromis trebuie să evalueze clientul?",
        [
            "Semnarea până joi garantează data, dar lasă prețul deschis.",
            "Așteptarea clarifică disponibilitatea, dar poate duce la pierderea prețului actual.",
            "Confirmarea stocului obligă furnizorul să păstreze prețul și după joi.",
            "Comanda semnată permite clientului să aleagă ulterior orice dată de livrare.",
        ],
        "Așteptarea clarifică disponibilitatea, dar poate duce la pierderea prețului actual.",
    ),
    AssessmentQuestion(
        "ro-r-b2-003",
        "reading",
        "B2",
        "Într-o consultare, locatarii cer păstrarea arborilor, iar comercianții cer "
        "acces pentru aprovizionare. Proiectul inițial elimina doi arbori pentru o bandă "
        "auto permanentă. Mediatoarea propune păstrarea arborilor și acces auto doar "
        "dimineața, pe traseul deja existent. Locatarii acceptă discutarea variantei, "
        "cu verificarea siguranței pietonilor; comercianții cer testarea timpului de descărcare. "
        "Cum poate fi rezumat stadiul discuției?",
        [
            "Există o variantă comună de analizat, iar acceptarea finală depinde de verificări.",
            "Ambele grupuri au aprobat fără rezerve forma definitivă a proiectului.",
            "Locatarii au acceptat eliminarea arborilor pentru o bandă permanentă.",
            "Comercianții au renunțat la accesul auto în schimbul păstrării arborilor.",
        ],
        "Există o variantă comună de analizat, iar acceptarea finală depinde de verificări.",
    ),
    AssessmentQuestion(
        "ro-r-b2-004",
        "reading",
        "B2",
        "Raportul tehnic precizează: «Echipa a lucrat trei zile la instalație. "
        "Alimentarea a fost restabilită pentru testare, însă două componente urmează "
        "să fie înlocuite. Funcționarea observată în timpul probei nu reprezintă recepția "
        "finală. Folosirea obișnuită va fi permisă după verificarea componentelor noi "
        "și semnarea procesului-verbal. Până atunci, accesul rămâne limitat la personalul tehnic.» "
        "Ce ar fi incorect să comunice administratorul utilizatorilor?",
        [
            "Instalația a fost alimentată pentru efectuarea unei probe.",
            "Mai sunt necesare intervenții și o verificare înainte de recepție.",
            "Instalația este gata pentru folosire obișnuită fiindcă a funcționat la probă.",
            "Accesul obișnuit depinde de încheierea etapelor prevăzute în raport.",
        ],
        "Instalația este gata pentru folosire obișnuită fiindcă a funcționat la probă.",
    ),
    AssessmentQuestion(
        "ro-r-b2-005",
        "reading",
        "B2",
        "O jurnalistă scrie: «Potrivit reprezentantului firmei, toate cererile depuse "
        "în termen ar fi fost soluționate. Redacția a verificat patru cazuri: trei persoane "
        "au primit răspuns, iar a patra spune că nu a primit nimic. Firma nu a precizat "
        "dacă solicitarea acestei persoane fusese depusă în termen. Am cerut lămuriri "
        "și vom actualiza articolul după primirea lor.» Ce permite materialul să afirmăm?",
        [
            "Cazul fără răspuns dovedește deja că firma și-a încălcat promisiunea.",
            "Verificarea celor trei răspunsuri confirmă situația tuturor solicitanților.",
            "A patra cerere a fost depusă cu întârziere, conform verificării redacției.",
            "Afirmația generală a firmei nu este confirmată independent de cazurile verificate.",
        ],
        "Afirmația generală a firmei nu este confirmată independent de cazurile verificate.",
    ),
]
