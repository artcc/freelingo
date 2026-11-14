"""Romanian C1 placement items with balanced answer positions within each skill."""

from app.data._types import AssessmentQuestion

C1_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "ro-g-c1-001",
        "grammar",
        "C1",
        "Irina ajunge la atelier și găsește ușa încuiată. Spune: "
        "«O fi plecat după materiale; mai aștept câteva minute.» "
        "Cum poate fi redată fidel poziția Irinei?",
        [
            "Irina presupune că persoana a plecat după materiale, fără să aibă confirmarea.",
            "Irina transmite vestea că persoana a plecat după materiale, primită de la aceasta.",
            "Irina își amintește că persoana anunțase o plecare după materiale în acea dimineață.",
            "Irina conchide că persoana va pleca după materiale după redeschiderea atelierului.",
        ],
        "Irina presupune că persoana a plecat după materiale, fără să aibă confirmarea.",
        "ro-presumptive-evidence-c1",
    ),
    AssessmentQuestion(
        "ro-g-c1-002",
        "grammar",
        "C1",
        "Administratorul scrie: «Putem închiria sala numai dacă primim avizul de siguranță.» "
        "Avizul tocmai a sosit. Ce concluzie permite mesajul, fără informații suplimentare?",
        [
            "Închirierea este confirmată, iar disponibilitatea sălii rezultă din primirea avizului.",
            "Închirierea trebuie reanalizată deoarece avizul a sosit după mesajul administratorului.",
            "O condiție necesară este îndeplinită, dar închirierea nu este astfel confirmată.",
            "O condiție recomandată este îndeplinită, deși sala se putea închiria și fără aviz.",
        ],
        "O condiție necesară este îndeplinită, dar închirierea nu este astfel confirmată.",
        "ro-restrictive-condition-c1",
    ),
    AssessmentQuestion(
        "ro-g-c1-003",
        "grammar",
        "C1",
        "În program scrie: «Cercetătoarea ale cărei concluzii le-a contestat editorul "
        "va răspunde mâine întrebărilor.» Cine a contestat concluziile cui?",
        [
            "Cercetătoarea a contestat concluziile editorului și va explica mâine obiecțiile.",
            "Editorul a contestat concluziile cercetătoarei, care va răspunde mâine întrebărilor.",
            "Editorul a contestat întrebările cercetătoarei, care își va prezenta mâine concluziile.",
            "Cercetătoarea a contestat propriile concluzii, iar editorul va răspunde mâine.",
        ],
        "Editorul a contestat concluziile cercetătoarei, care va răspunde mâine întrebărilor.",
        "ro-relative-case-c1",
    ),
    AssessmentQuestion(
        "ro-g-c1-004",
        "grammar",
        "C1",
        "Instrucțiunea spune: «Nu este obligatoriu să ridicați documentele personal; "
        "le poate ridica și o persoană împuternicită.» Ce mesaj păstrează regula?",
        [
            "Este preferabil să trimiteți un reprezentant, deși puteți veni și personal.",
            "Puteți veni personal numai dacă persoana împuternicită nu este disponibilă.",
            "Trebuie să desemnați un reprezentant înainte de a putea veni personal.",
            "Puteți veni personal sau puteți trimite pe cineva care are împuternicire.",
        ],
        "Puteți veni personal sau puteți trimite pe cineva care are împuternicire.",
        "ro-modal-scope-c1",
    ),
    AssessmentQuestion(
        "ro-g-c1-005",
        "grammar",
        "C1",
        "Un raport precizează: «Extinderea programului nu duce neapărat la creșterea "
        "numărului de cititori.» Care reformulare păstrează forța afirmației?",
        [
            "Extinderea programului poate mări numărul de cititori doar dacă taxele scad.",
            "Extinderea programului are un efect prea mic pentru a putea fi măsurat.",
            "Extinderea programului poate atrage cititori, însă acest efect nu este garantat.",
            "Extinderea programului este probabil să reducă numărul actual de cititori.",
        ],
        "Extinderea programului poate atrage cititori, însă acest efect nu este garantat.",
        "ro-quantified-negation-c1",
    ),
    AssessmentQuestion(
        "ro-g-c1-006",
        "grammar",
        "C1",
        "Într-o discuție, Ana spune: «I-am cerut lui Vlad să-mi trimită schița joi, "
        "dar încă nu mi-a confirmat.» Ce însemnare redă fidel situația?",
        [
            "Ana a cerut ca Vlad să-i trimită schița joi; acceptarea termenului rămâne neconfirmată.",
            "Vlad a cerut ca Ana să-i trimită schița joi; acceptarea termenului rămâne neconfirmată.",
            "Ana a promis că îi trimite lui Vlad schița joi; primirea ei rămâne neconfirmată.",
            "Vlad a promis că îi trimite Anei schița joi; încheierea lucrării rămâne neconfirmată.",
        ],
        "Ana a cerut ca Vlad să-i trimită schița joi; acceptarea termenului rămâne neconfirmată.",
        "ro-subjunctive-agency-c1",
    ),
    AssessmentQuestion(
        "ro-v-c1-001",
        "vocabulary",
        "C1",
        "După mai multe observații vagi, Mara îți spune: «Prefer să-mi spui pe șleau.» "
        "Vrei să îi respecți cererea și să rămâi cooperant. Ce răspunzi?",
        [
            "Cred că ai înțeles ce vreau să spun; mai bine revenim când se liniștesc lucrurile.",
            "Mă deranjează schimbările de ultim moment; te rog să mă anunți cu o zi înainte.",
            "Sunt câteva aspecte care ar merita poate privite altfel, dacă găsim momentul potrivit.",
            "Mai întâi să vedem ce cred și ceilalți; după aceea îți pot spune și părerea mea.",
        ],
        "Mă deranjează schimbările de ultim moment; te rog să mă anunți cu o zi înainte.",
    ),
    AssessmentQuestion(
        "ro-v-c1-002",
        "vocabulary",
        "C1",
        "Se presupunea că poarta fusese închisă înainte de ora opt. "
        "O înregistrare datată arată că era încă deschisă la opt și jumătate. "
        "Ce verb descrie raportul dintre înregistrare și presupunerea inițială?",
        [
            "Înregistrarea coroborează presupunerea.",
            "Înregistrarea fundamentează presupunerea.",
            "Înregistrarea reiterează presupunerea.",
            "Înregistrarea infirmă presupunerea.",
        ],
        "Înregistrarea infirmă presupunerea.",
    ),
    AssessmentQuestion(
        "ro-v-c1-003",
        "vocabulary",
        "C1",
        "Locatarii au cerut publicarea procesului-verbal. Asociația răspunde: "
        "«Vom da curs cererii de publicare a procesului-verbal.» "
        "Ce intenție exprimă asociația?",
        [
            "Asociația intenționează să răspundă favorabil cererii de publicare.",
            "Asociația intenționează să transfere cererea altei instituții pentru soluționare.",
            "Asociația intenționează să amâne decizia până la o nouă solicitare.",
            "Asociația intenționează să ceară retragerea solicitării de publicare.",
        ],
        "Asociația intenționează să răspundă favorabil cererii de publicare.",
    ),
    AssessmentQuestion(
        "ro-v-c1-004",
        "vocabulary",
        "C1",
        "Un club folosește o sală «cu titlu provizoriu, până la încheierea lucrărilor "
        "din sediul propriu». Cum trebuie înțeleasă această formulare?",
        [
            "Folosirea este gratuită, iar durata depinde de programul obișnuit al clubului.",
            "Folosirea este exclusivă, iar celelalte grupuri trebuie să caute un alt spațiu.",
            "Folosirea este temporară, iar aranjamentul este legat de finalizarea lucrărilor.",
            "Folosirea este aprobată definitiv, iar mutarea ulterioară rămâne opțională.",
        ],
        "Folosirea este temporară, iar aranjamentul este legat de finalizarea lucrărilor.",
    ),
    AssessmentQuestion(
        "ro-r-c1-001",
        "reading",
        "C1",
        "Anunțul bibliotecii: «Recomandăm înscrierea online pentru reducerea timpului "
        "de așteptare. Cererile pe hârtie se primesc în continuare, între 10 și 14. "
        "Programarea telefonică este necesară doar pentru consultarea fondului vechi.» "
        "Mihai vrea să depună singur cererea pentru un abonament obișnuit, fără internet "
        "și fără o programare inutilă. Ce variantă este susținută de anunț?",
        [
            "Poate cere telefonic o programare pentru fondul vechi și apoi solicita abonamentul.",
            "Poate trimite pe cineva să completeze online cererea înainte de a veni personal.",
            "Poate depune cererea după ora 14, când înscrierile online nu mai au prioritate.",
            "Poate depune cererea pe hârtie în intervalul anunțat, fără programarea menționată.",
        ],
        "Poate depune cererea pe hârtie în intervalul anunțat, fără programarea menționată.",
    ),
    AssessmentQuestion(
        "ro-r-c1-002",
        "reading",
        "C1",
        "«Când am ajuns la cabană, gazda plecase. Am crezut că uitase de noi. "
        "Abia când am găsit semnal am citit mesajul trimis în ajun: cheia era la vecină. "
        "Gazda ne ceruse confirmarea, dar noi nu văzuserăm mesajul.» "
        "Ce explică cel mai bine neînțelegerea?",
        [
            "Instrucțiunile fuseseră trimise, dar grupul nu le consultase înainte de sosire.",
            "Gazda a trimis instrucțiunile după plecare, când a aflat că grupul ajunsese.",
            "Grupul confirmase primirea instrucțiunilor, dar vecina nu primise încă cheia.",
            "Instrucțiunile erau cunoscute, dar grupul a ales să aștepte întoarcerea gazdei.",
        ],
        "Instrucțiunile fuseseră trimise, dar grupul nu le consultase înainte de sosire.",
    ),
    AssessmentQuestion(
        "ro-r-c1-003",
        "reading",
        "C1",
        "La finalul unei ședințe, moderatoarea spune: «Bugetul a fost acceptat de toți. "
        "Pentru sâmbătă s-au pronunțat patru persoane, iar celelalte două au cerut "
        "să își verifice programul. Rezervarea o facem după răspunsul lor.» "
        "Ce mesaj ar fi fidel pentru participanții absenți?",
        [
            "Bugetul și data sunt stabilite; rezervarea așteaptă doar confirmarea costului sălii.",
            "Bugetul se va aproba după alegerea datei; patru persoane susțin deja sâmbăta.",
            "Bugetul este stabilit; data și rezervarea rămân în așteptarea celor două răspunsuri.",
            "Data a fost respinsă de două persoane; trebuie căutată o altă zi în același buget.",
        ],
        "Bugetul este stabilit; data și rezervarea rămân în așteptarea celor două răspunsuri.",
    ),
    AssessmentQuestion(
        "ro-r-c1-004",
        "reading",
        "C1",
        "După ce a încurcat de două ori sălile, Radu spune zâmbind: «Se vede că mă pricep "
        "la orientare!» Apoi îți întinde programul și adaugă: «Mai bine verificăm împreună.» "
        "Vrei să răspunzi în spiritul glumei și să ajuți. Ce replică se potrivește cel mai bine?",
        [
            "Ai dreptate, orientarea e punctul tău forte; alegerea următoarei săli îți aparține.",
            "Am făcut turul complet datorită ție! Hai să găsim acum sala trecută în program.",
            "Dacă nu cunoști clădirea, ar fi bine să nu mai propui trasee pentru ceilalți.",
            "Programul pare să fi fost greșit; hai să cerem organizatorilor să își ceară scuze.",
        ],
        "Am făcut turul complet datorită ție! Hai să găsim acum sala trecută în program.",
    ),
]
