"""Romanian C2 placement items on scope, pragmatic inference and faithful reformulation."""

from app.data._types import AssessmentQuestion

C2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "ro-g-c2-001",
        "grammar",
        "C2",
        "Redacția scrie: «Primăria confirmă că a primit raportul în care expertul "
        "sugerează că fisurile ar putea fi legate de vibrații.» "
        "Ce rezumat păstrează nivelurile de asumare?",
        [
            "Primăria confirmă ipoteza expertului, dar nu stabilește încă amploarea fisurilor.",
            "Expertul confirmă legătura cu vibrațiile, iar primăria verifică primirea raportului.",
            "Redacția confirmă cauza fisurilor, citând raportul pe care primăria l-a primit.",
            "Primăria confirmă primirea raportului, iar expertul propune o posibilă explicație.",
        ],
        "Primăria confirmă primirea raportului, iar expertul propune o posibilă explicație.",
        "ro-layered-evidence-c2",
    ),
    AssessmentQuestion(
        "ro-g-c2-002",
        "grammar",
        "C2",
        "Regula spune: «Cererile se depun vineri. Cei aflați în delegație le pot depune luni "
        "dacă anunță până joi. Dovada plății se anexează în toate cazurile.» "
        "Ioana este în delegație de miercuri până marțea următoare și a anunțat miercuri. "
        "Poate trimite actele prin curier. Ce variantă respectă regula?",
        [
            "Ioana poate depune cererea luni și poate aduce dovada plății după întoarcere.",
            "Ioana poate depune cererea luni, cu dovada plății anexată la depunere.",
            "Ioana trebuie să depună cererea vineri, întrucât anunțul trebuia făcut joi.",
            "Ioana poate depune cererea la întoarcere, dacă anexează dovada plății atunci.",
        ],
        "Ioana poate depune cererea luni, cu dovada plății anexată la depunere.",
        "ro-nested-exceptions-c2",
    ),
    AssessmentQuestion(
        "ro-g-c2-003",
        "grammar",
        "C2",
        "Ana spune: «Dacă aș fi acceptat atunci postul din Iași, acum aș locui mai aproape "
        "de părinți.» Care relatare păstrează participanții și reperele temporale?",
        [
            "Ana își imaginează că ar locui acum mai aproape de părinți dacă ar fi acceptat acel post.",
            "Ana se imaginează în trecut mai aproape de părinți, ca efect al unei decizii actuale.",
            "Ana regretă că părinții nu au acceptat atunci un post care i-ar fi apropiat de ea.",
            "Ana anunță că va accepta postul din Iași pentru a locui mai aproape de părinți.",
        ],
        "Ana își imaginează că ar locui acum mai aproape de părinți dacă ar fi acceptat acel post.",
        "ro-counterfactual-alignment-c2",
    ),
    AssessmentQuestion(
        "ro-g-c2-004",
        "grammar",
        "C2",
        "Ordinea de zi include «analizarea de către comisie a propunerii de suspendare "
        "a evaluării cererilor depuse de asociații». Ce se poate afirma fără a adăuga informații?",
        [
            "Asociațiile propun suspendarea, iar comisia va analiza cererile depuse de acestea.",
            "Comisia a suspendat evaluarea și urmează să analizeze obiecțiile asociațiilor.",
            "Comisia va analiza o propunere; asociațiile sunt cele care au depus cererile.",
            "Asociațiile vor evalua propunerea comisiei înainte de suspendarea cererilor.",
        ],
        "Comisia va analiza o propunere; asociațiile sunt cele care au depus cererile.",
        "ro-dense-nominals-c2",
    ),
    AssessmentQuestion(
        "ro-g-c2-005",
        "grammar",
        "C2",
        "La acuzația că Ioana «a fugit din ședință», Vlad răspunde: "
        "«Nu a fugit; a plecat la ora pe care o anunțase de la început.» "
        "Ce anume contestă Vlad?",
        [
            "Contestă ora plecării Ioanei, dar acceptă că aceasta a fost neanunțată.",
            "Contestă descrierea plecării ca evitare, fără să nege plecarea însăși.",
            "Contestă faptul că Ioana a părăsit ședința și invocă un anunț greșit.",
            "Contestă dreptul Ioanei de a pleca, deși recunoaște că anunțase ora.",
        ],
        "Contestă descrierea plecării ca evitare, fără să nege plecarea însăși.",
        "ro-metalinguistic-negation-c2",
    ),
    AssessmentQuestion(
        "ro-g-c2-006",
        "grammar",
        "C2",
        "Regula internă precizează: «Doar Ana poate aproba plata; Vlad poate doar verifica "
        "documentele.» Care reformulare păstrează domeniul celor două restricții?",
        [
            "Ana se ocupă exclusiv de aprobări, iar Vlad este singurul care poate verifica actele.",
            "Ana și Vlad pot aproba plata împreună, după ce Vlad verifică toate documentele.",
            "Ana poate verifica documentele, iar Vlad poate aproba plata verificată de ea.",
            "Aprobarea îi este rezervată Anei; rolul lui Vlad este limitat la verificarea actelor.",
        ],
        "Aprobarea îi este rezervată Anei; rolul lui Vlad este limitat la verificarea actelor.",
        "ro-scalar-focus-c2",
    ),
    AssessmentQuestion(
        "ro-v-c2-001",
        "vocabulary",
        "C2",
        "La sfârșitul medierii, Sorin spune: «Subscriu la obiectiv, dar nu și la mijloacele "
        "propuse.» Ce consemnare păstrează sensul lui «a subscrie» în acest context?",
        [
            "Sorin confirmă finanțarea obiectivului, dar lasă implementarea în seama celorlalți.",
            "Sorin își retrage sprijinul pentru obiectiv și cere discutarea unor mijloace noi.",
            "Sorin susține scopul urmărit, însă nu își dă acordul pentru metodele prezentate.",
            "Sorin acceptă metodele ca punct de plecare și amână evaluarea scopului urmărit.",
        ],
        "Sorin susține scopul urmărit, însă nu își dă acordul pentru metodele prezentate.",
    ),
    AssessmentQuestion(
        "ro-v-c2-002",
        "vocabulary",
        "C2",
        "Într-o petiție apare: «Solicităm anularea taxei și, în subsidiar, reducerea ei.» "
        "Ce relație există între cele două solicitări?",
        [
            "Reducerea este cerută ca soluție secundară dacă anularea nu este acceptată.",
            "Reducerea este cerută ca primă etapă obligatorie înainte de anularea taxei.",
            "Reducerea este cerută numai pentru persoanele care nu au semnat petiția.",
            "Reducerea este cerută în paralel cu anularea, pentru o altă taxă neprecizată.",
        ],
        "Reducerea este cerută ca soluție secundară dacă anularea nu este acceptată.",
    ),
    AssessmentQuestion(
        "ro-v-c2-003",
        "vocabulary",
        "C2",
        "O colegă spune: «Raportul pune în perspectivă scăderea din iunie: "
        "pe ansamblul ultimilor cinci ani, numărul vizitatorilor a crescut.» "
        "Ce face raportul prin această operație?",
        [
            "Retrage datele din iunie, deoarece contrazic evoluția observată pe termen lung.",
            "Atribuie scăderea din iunie schimbării metodei de numărare a vizitatorilor.",
            "Prezintă scăderea din iunie drept începutul probabil al unei tendințe viitoare.",
            "Plasează scăderea din iunie într-un cadru temporal mai larg, fără să o nege.",
        ],
        "Plasează scăderea din iunie într-un cadru temporal mai larg, fără să o nege.",
    ),
    AssessmentQuestion(
        "ro-v-c2-004",
        "vocabulary",
        "C2",
        "După câteva răspunsuri despre profit, jurnalista observă: "
        "«Invitatul a eludat întrebarea privind cine a autorizat plata.» "
        "Ce comportament descrie aici verbul «a eluda»?",
        [
            "Invitatul a respins explicit premisa întrebării și a numit persoana responsabilă.",
            "Invitatul a evitat să răspundă direct la aspectul despre care fusese întrebat.",
            "Invitatul a reformulat întrebarea pentru a verifica identitatea persoanei vizate.",
            "Invitatul a răspuns printr-un exemplu care clarifică traseul autorizării plății.",
        ],
        "Invitatul a evitat să răspundă direct la aspectul despre care fusese întrebat.",
    ),
    AssessmentQuestion(
        "ro-r-c2-001",
        "reading",
        "C2",
        "«Mara împături scrisoarea. Așadar, pentru ei nu fusese decât o înlocuitoare. "
        "Mâine aveau să afle că se puteau descurca și fără ea. Pe ultima pagină, "
        "pe care nu o citise încă, colegii îi propuneau prelungirea contractului.» "
        "Ce efect produce ultima frază?",
        [
            "Confirmă că hotărârea colegilor era definitivă și că Mara o înțelesese corect.",
            "Creează o distanță între interpretarea Marei și informația disponibilă cititorului.",
            "Arată că Mara respinsese deja prelungirea și încearcă să își justifice alegerea.",
            "Mută acuzația asupra naratorului, care împărtășește evaluarea făcută de Mara.",
        ],
        "Creează o distanță între interpretarea Marei și informația disponibilă cititorului.",
    ),
    AssessmentQuestion(
        "ro-r-c2-002",
        "reading",
        "C2",
        "Organizatorul promisese o înscriere «fără bătăi de cap». După ce completează "
        "a treia oară același formular, Radu spune: «Într-adevăr, o experiență de "
        "neuitat.» Colega râde, apoi îl ajută să găsească numărul cererii. "
        "Care interpretare este cel mai bine susținută?",
        [
            "Radu apreciază originalitatea procedurii, iar colega îl ajută să o recomande altora.",
            "Radu critică memoria colegei, iar aceasta repară greșeala prin găsirea numărului.",
            "Radu anunță că va abandona înscrierea, iar colega încearcă să îl facă să revină.",
            "Radu ironizează promisiunea prin contrast cu experiența, iar colega îi oferă sprijin.",
        ],
        "Radu ironizează promisiunea prin contrast cu experiența, iar colega îi oferă sprijin.",
    ),
    AssessmentQuestion(
        "ro-r-c2-003",
        "reading",
        "C2",
        "Ioana citește o invitație și spune: «Nu e tocmai fericită formularea despre cei "
        "care au întârziat.» Autorul răspunde: «Dar n-am vrut să jignesc pe nimeni.» "
        "Ioana arată pasajul și adaugă: «Intenția o înțeleg; mă gândesc la cei care "
        "îl vor citi fără explicația ta.» Autorul vrea să păstreze cererea de punctualitate "
        "și să revizuiască pasajul care poate jigni. Ce răspuns servește acestui scop?",
        [
            "Să înlocuim reproșul cu o explicație a efectului întârzierilor asupra programului comun.",
            "Să păstrăm reproșul și să adăugăm că intenția autorului a fost înțeleasă greșit.",
            "Să numim persoanele care întârzie, pentru ca reproșul să nu mai pară adresat tuturor.",
            "Să renunțăm la orice referire la oră, lăsând participanții să își aleagă sosirea.",
        ],
        "Să înlocuim reproșul cu o explicație a efectului întârzierilor asupra programului comun.",
    ),
    AssessmentQuestion(
        "ro-r-c2-004",
        "reading",
        "C2",
        "Într-o cronică se citește: «Directorul numește noul program un „succes deplin”. "
        "Cifrele arată într-adevăr mai multe vizite, dar nu spun câți vizitatori au revenit. "
        "Așadar, expresia descrie mai bine entuziasmul conducerii decât ceea ce putem "
        "conchide deocamdată din date.» Care este poziția autoarei?",
        [
            "Contestă creșterea numărului de vizite și atribuie conducerii o raportare intenționat falsă.",
            "Acceptă succesul deplin, dar consideră că directorul l-a prezentat cu prea mult entuziasm.",
            "Acceptă creșterea observată, dar refuză să preia evaluarea globală în lipsa altor date.",
            "Respinge programul ca nereușit, considerând lipsa datelor despre reveniri o dovadă suficientă.",
        ],
        "Acceptă creșterea observată, dar refuză să preia evaluarea globală în lipsa altor date.",
    ),
]
