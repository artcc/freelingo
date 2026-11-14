"""Romanian B1 placement questions with balanced keys within each skill."""

from app.data._types import AssessmentQuestion

B1_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "ro-g-b1-001",
        "grammar",
        "B1",
        "Mara spune: «Când am intrat în bucătărie, tata pregătea cina.» "
        "Ce aflăm despre pregătirea cinei în acel moment?",
        [
            "Se încheiase înainte de intrarea Marei.",
            "Era în desfășurare când a intrat Mara.",
            "A început după intrarea Marei.",
            "Era doar o intenție pentru mai târziu.",
        ],
        "Era în desfășurare când a intrat Mara.",
        "ro-narrative-past-b1",
    ),
    AssessmentQuestion(
        "ro-g-b1-002",
        "grammar",
        "B1",
        "Vorbim despre o singură colegă. Completați în româna standard: "
        "«Vreau ca Irina să ___ la ședință și să prezinte rezultatele.»",
        ["vin", "veniți", "vine", "vină"],
        "vină",
        "ro-subjunctive-selection-b1",
    ),
    AssessmentQuestion(
        "ro-g-b1-003",
        "grammar",
        "B1",
        "Formulați o propunere ipotetică în numele întregului grup: "
        "«Dacă am avea o sală mai mare, noi ___ mai mulți participanți.»",
        ["am invita", "ai invita", "ar invita", "ați invita"],
        "am invita",
        "ro-conditional-b1",
    ),
    AssessmentQuestion(
        "ro-g-b1-004",
        "grammar",
        "B1",
        "Îi ceri lui Dan să îți dea cheia. Alege combinația de pronume potrivită: "
        "«Dan, ___ dai, te rog?»",
        ["ți-o", "mi-l", "mi-o", "ți-l"],
        "mi-o",
        "ro-clitic-combinations-b1",
    ),
    AssessmentQuestion(
        "ro-g-b1-005",
        "grammar",
        "B1",
        "Alegeți forma standard pentru un document primit: "
        "«Contractul ___ l-am primit ieri nu conține adresa completă.»",
        ["care", "căruia", "cu care", "pe care"],
        "pe care",
        "ro-relative-clauses-b1",
    ),
    AssessmentQuestion(
        "ro-g-b1-006",
        "grammar",
        "B1",
        "Completați acordul articolului genitival: "
        "«În sertar sunt două chei ___ proprietarului.»",
        ["ale", "al", "ai", "a"],
        "ale",
        "ro-genitive-article-b1",
    ),
    AssessmentQuestion(
        "ro-g-b1-007",
        "grammar",
        "B1",
        "Recepționera spune: «Nu este nevoie să imprimați confirmarea; "
        "o puteți arăta pe telefon.» Ce instrucțiune păstrează sensul mesajului?",
        [
            "Trebuie să aduceți confirmarea atât pe hârtie, cât și pe telefon.",
            "Este interzis să prezentați confirmarea pe hârtie.",
            "Confirmarea pe telefon este suficientă, fără imprimare.",
            "Puteți intra fără să prezentați vreo confirmare.",
        ],
        "Confirmarea pe telefon este suficientă, fără imprimare.",
        "ro-obligation-b1",
    ),
    AssessmentQuestion(
        "ro-g-b1-008",
        "grammar",
        "B1",
        "Luni, Ana i-a spus lui Dan: «Vin mâine.» Marți, Dan redă mesajul. "
        "Care variantă păstrează ziua anunțată de Ana?",
        [
            "Ana a spus ieri că vine mâine.",
            "Ana a spus ieri că vine astăzi.",
            "Ana a spus astăzi că vine mâine.",
            "Ana a spus ieri că a venit duminică.",
        ],
        "Ana a spus ieri că vine astăzi.",
        "ro-reported-speech-b1",
    ),
    AssessmentQuestion(
        "ro-v-b1-001",
        "vocabulary",
        "B1",
        "Pensiunea cere 150 de lei acum, iar restul prețului se plătește la sosire. "
        "Cum se numește suma cerută acum?",
        ["O garanție.", "O taxă de anulare.", "Un avans.", "O rambursare."],
        "Un avans.",
    ),
    AssessmentQuestion(
        "ro-v-b1-002",
        "vocabulary",
        "B1",
        "Programarea era pentru joi. Cabinetul te sună și o mută pentru luni, "
        "săptămâna următoare. Ce a făcut cabinetul?",
        [
            "A amânat programarea.",
            "A anulat definitiv programarea.",
            "A devansat programarea.",
            "A păstrat neschimbată programarea.",
        ],
        "A amânat programarea.",
    ),
    AssessmentQuestion(
        "ro-v-b1-003",
        "vocabulary",
        "B1",
        "Angajatorul îți dă un document care confirmă că lucrezi în firmă. " "Ce ai primit?",
        ["O recomandare.", "O ofertă de angajare.", "O cerere de concediu.", "O adeverință."],
        "O adeverință.",
    ),
    AssessmentQuestion(
        "ro-v-b1-004",
        "vocabulary",
        "B1",
        "La început, Elena găsea dificil programul de dimineață. După două luni, "
        "acest program i se pare firesc și îl urmează fără efort. Ce s-a întâmplat?",
        [
            "A renunțat la program.",
            "S-a obișnuit cu programul.",
            "A amânat schimbarea programului.",
            "S-a opus noului program.",
        ],
        "S-a obișnuit cu programul.",
    ),
    AssessmentQuestion(
        "ro-v-b1-005",
        "vocabulary",
        "B1",
        "Nu știi dacă «întâlnirea de la zece» este online sau la sediu. "
        "Vrei un detaliu exact, nu repetarea întregului mesaj. Ce ceri?",
        [
            "Vă rog să precizați unde are loc întâlnirea.",
            "Vă rog să amânați întâlnirea de la zece.",
            "Vă rog să transmiteți colegilor invitația.",
            "Vă rog să rezumați temele întâlnirii.",
        ],
        "Vă rog să precizați unde are loc întâlnirea.",
    ),
    AssessmentQuestion(
        "ro-v-b1-006",
        "vocabulary",
        "B1",
        "Ioana spune despre un coleg: «Dacă promite că face ceva, se ține de cuvânt. "
        "Mă pot baza pe el.» Cum îl descrie?",
        ["Disponibil.", "De încredere.", "Recunoscător.", "Interesat."],
        "De încredere.",
    ),
    AssessmentQuestion(
        "ro-r-b1-001",
        "reading",
        "B1",
        "Citiți mesajul: «Biblioteca va fi închisă sâmbătă pentru reparații. "
        "Cărțile care trebuiau înapoiate atunci pot fi aduse luni, fără costuri suplimentare. "
        "Cutia de returnare din exterior nu va fi accesibilă în timpul lucrărilor.» "
        "Ai o carte cu termen sâmbătă. Ce poți face potrivit mesajului?",
        [
            "O poți lăsa sâmbătă în cutia exterioară.",
            "Trebuie să o aduci vineri pentru a evita o taxă.",
            "O poți aduce luni, dar vei plăti pentru întârziere.",
            "O poți înapoia luni fără să plătești în plus.",
        ],
        "O poți înapoia luni fără să plătești în plus.",
    ),
    AssessmentQuestion(
        "ro-r-b1-002",
        "reading",
        "B1",
        "Radu scrie: «Pot rezerva sala pentru joi sau vineri. Joi este mai ieftină, "
        "dar Maria lucrează până târziu. Ea trebuie să prezinte proiectul, așa că propun "
        "vineri. Spuneți-mi până mâine dacă sunteți de acord; încă nu am plătit nimic.» "
        "De ce preferă Radu vineri?",
        [
            "Sala nu mai poate fi rezervată joi.",
            "A plătit deja rezervarea de vineri.",
            "Vrea ca persoana care prezintă să poată participa.",
            "A găsit pentru vineri un preț mai mic.",
        ],
        "Vrea ca persoana care prezintă să poată participa.",
    ),
    AssessmentQuestion(
        "ro-r-b1-003",
        "reading",
        "B1",
        "Anunțul asociației spune: «Miercuri, între orele 9 și 12, se oprește apa rece "
        "pentru schimbarea unei conducte. Lucrarea privește scările A și B. Locatarii "
        "scării C vor avea apă, dar pot auzi zgomot în curte. Nu este necesar să rămâneți acasă.» "
        "Ce informație este corectă pentru un locatar de la scara C?",
        [
            "Va avea apă, deși este posibil să audă zgomotul lucrării.",
            "Trebuie să rămână acasă pentru accesul instalatorului.",
            "Va rămâne fără apă rece între orele 9 și 12.",
            "Va avea apă, iar lucrările se vor face în interiorul scării C.",
        ],
        "Va avea apă, deși este posibil să audă zgomotul lucrării.",
    ),
    AssessmentQuestion(
        "ro-r-b1-004",
        "reading",
        "B1",
        "Elena îi scrie lui Vlad: «Am primit factura, dar numele firmei este greșit. "
        "Suma și adresa sunt corecte. Le-am cerut să schimbe doar numele și să mi-o "
        "trimită din nou. Te rog să aștepți varianta corectată înainte să o achiți.» "
        "Ce trebuie să facă Vlad acum?",
        [
            "Să plătească factura, fiindcă suma este corectă.",
            "Să ceară schimbarea adresei firmei.",
            "Să amâne plata până primește documentul corectat.",
            "Să achite factura și să solicite apoi corectarea numelui.",
        ],
        "Să amâne plata până primește documentul corectat.",
    ),
    AssessmentQuestion(
        "ro-r-b1-005",
        "reading",
        "B1",
        "Organizatorii anunță: «Pentru curățenia din parc, aducem noi sacii și mănușile. "
        "Participanții sunt rugați să aibă apă și încălțăminte potrivită. Dacă plouă ușor, "
        "activitatea are loc. În caz de furtună, publicăm o nouă dată pe pagina asociației.» "
        "Ce ar trebui să faci dacă se anunță furtună?",
        [
            "Să mergi la parc, deoarece activitatea are loc pe orice vreme.",
            "Să verifici pagina asociației pentru schimbarea datei.",
            "Să cumperi saci și mănuși pentru organizatori.",
            "Să alegi singur o altă zi pentru întregul grup.",
        ],
        "Să verifici pagina asociației pentru schimbarea datei.",
    ),
    AssessmentQuestion(
        "ro-r-b1-006",
        "reading",
        "B1",
        "Mara povestește: «Am vrut să termin raportul în tren, dar nu am găsit un loc "
        "la masă. Am citit notițele pe telefon și am făcut o listă cu ce lipsea. "
        "Seara am completat raportul acasă. Călătoria nu a fost suficientă pentru tot, "
        "însă m-a ajutat să mă organizez.» Cum evaluează Mara timpul petrecut în tren?",
        [
            "A fost suficient ca să încheie redactarea raportului.",
            "A fost pierdut, fiindcă nu a putut lucra deloc.",
            "A fost dedicat corectării raportului deja terminat.",
            "A fost util, dar a mai avut de lucru acasă.",
        ],
        "A fost util, dar a mai avut de lucru acasă.",
    ),
]
