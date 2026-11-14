"""Romanian C1 grammar, evidential nuance and interaction."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "ro-presumptive-evidence-c1",
        "Prezumtivul: explicații posibile, nu fapte confirmate",
        "C1",
        "Modalitate și surse",
        "Interpretează formele prezumtive în raport cu indiciile și momentul acțiunii.",
        "Forme precum «o fi lucrând» și «o fi plecat» pot prezenta o presupunere. "
        "Prima poate viza o acțiune în desfășurare, iar a doua una anterioară. "
        "Contextul este decisiv: «va fi terminat» poate exprima și un viitor anterior, "
        "nu doar o presupunere. Într-o explicație practică, numește indiciul și păstrează "
        "incertitudinea când transmiți informația mai departe.",
        structure="o fi + gerunziu / participiu, interpretat în context",
        rules=[
            "Un indiciu sprijină presupunerea, dar nu o transformă în observație directă.",
            "Nu confunda forma participială prezumtivă cu o confirmare a rezultatului.",
        ],
        examples=[
            GrammarExample(
                "Nu răspunde la telefon. O fi lucrând în atelier.",
                note="Vorbitorul propune o explicație, fără să fi verificat-o.",
            ),
            GrammarExample(
                "Lumina e stinsă; o fi plecat deja.",
                note="Plecarea este o ipoteză despre un eveniment anterior.",
            ),
        ],
        related=["ro-reported-conditional-c1", "ro-modal-scope-c1"],
    ),
    GrammarTopic(
        "ro-reported-conditional-c1",
        "Condiționalul în informația neconfirmată",
        "C1",
        "Modalitate și surse",
        "Separă relatarea atribuită unei surse de asumarea adevărului ei.",
        "În știri, «ar fi decis» poate transmite o informație neconfirmată, fără o condiție "
        "exprimată. Acesta nu este singurul sens al condiționalului perfect: într-un context "
        "ipotetic, aceeași formă poate descrie un rezultat nerealizat. Expresii precum "
        "«potrivit unor surse» și existența unei condiții ajută la diferențiere. "
        "În rezumat, păstrează atât atribuirea, cât și rezerva.",
        rules=[
            "Nu înlocui automat «ar fi aprobat» cu «a aprobat» într-o știre neconfirmată.",
            "Menționează sursa când ea delimitează responsabilitatea pentru afirmație.",
        ],
        examples=[
            GrammarExample(
                "Potrivit unor surse locale, firma ar fi renunțat la proiect.",
                note="Renunțarea este relatată, nu confirmată de vorbitor.",
            ),
            GrammarExample(
                "Firma ar fi renunțat dacă finanțarea nu ar fi fost prelungită.",
                note="Aici există o condiție ipotetică; nu este o simplă atribuire jurnalistică.",
            ),
        ],
        related=["ro-presumptive-evidence-c1", "ro-counterfactual-reproach-c1"],
    ),
    GrammarTopic(
        "ro-modal-scope-c1",
        "Necesitate, probabilitate și negație",
        "C1",
        "Modalitate și surse",
        "Stabilește dacă o expresie modală formulează o obligație sau o deducție.",
        "«Trebuie să» poate exprima o cerință, dar și o concluzie foarte probabilă. "
        "În «Trebuie să fie acasă, fiindcă i-am văzut bicicleta», contextul susține "
        "o deducție. «Nu este obligatoriu să» exclude obligația, pe când «este obligatoriu "
        "să nu» impune evitarea acțiunii. Când «nu trebuie să» ar fi neclar, explicitează "
        "sensul în loc să te bazezi numai pe intonație.",
        rules=[
            "Păstrează diferența dintre absența obligației și interdicție.",
            "Într-o reformulare, nu transforma probabilitatea ridicată în certitudine verificată.",
        ],
        examples=[
            GrammarExample(
                "Trebuie să fi încurcat datele; altfel nu se explică diferența.",
                note="Este o deducție despre trecut, nu o obligație trecută.",
            ),
            GrammarExample(
                "Nu este obligatoriu să vii personal; poți trimite un reprezentant.",
                note="Prezența personală este permisă, dar nu impusă.",
            ),
        ],
        related=["ro-presumptive-evidence-c1", "ro-quantified-negation-c1"],
    ),
    GrammarTopic(
        "ro-restrictive-condition-c1",
        "Numai dacă, cu condiția să și limitele acordului",
        "C1",
        "Condiții și negociere",
        "Deosebește o condiție necesară de o garanție suficientă.",
        "«Aprobăm cererea numai dacă dosarul este complet» exclude aprobarea unui dosar "
        "incomplet, dar nu spune că orice dosar complet va fi aprobat. Într-o ofertă, "
        "«cu condiția să» delimitează angajamentul. Formulează separat eventualele verificări "
        "rămase, ca interlocutorul să nu confunde îndeplinirea unui criteriu cu decizia finală.",
        rules=[
            "Din «numai dacă» nu deduce automat și relația inversă.",
            "Într-un acord, păstrează persoana care își asumă fiecare condiție.",
        ],
        examples=[
            GrammarExample(
                "Putem închiria sala numai dacă primim avizul; disponibilitatea se verifică separat.",
                note="Avizul este necesar, dar nu garantează că sala este liberă.",
            ),
            GrammarExample(
                "Acceptăm amânarea cu condiția să ne trimiteți astăzi noul calendar.",
                note="Condiția privește oferta de amânare și destinatarul ei.",
            ),
        ],
        related=["ro-concessive-alternatives-c1", "ro-modal-scope-c1"],
    ),
    GrammarTopic(
        "ro-concessive-alternatives-c1",
        "Deși, chiar dacă și indiferent dacă",
        "C1",
        "Condiții și negociere",
        "Recunoaște o împrejurare fără să retragi concluzia principală.",
        "«Deși» prezintă de regulă o împrejurare acceptată ca fapt. «Chiar dacă» poate "
        "introduce o situație ipotetică sau, în context, una reală. «Indiferent dacă» "
        "menține concluzia în ambele alternative. Alege construcția după statutul "
        "informației; nu prezenta o reducere posibilă drept reducere deja obținută.",
        rules=[
            "Concesia recunoaște un argument, nu implică acceptarea concluziei celuilalt.",
            "Contextul stabilește dacă situația introdusă prin «chiar dacă» este reală.",
        ],
        examples=[
            GrammarExample(
                "Deși oferta este mai ieftină, termenul de livrare nu ne convine.",
                note="Prețul mai mic este recunoscut; oferta nu este încă acceptată.",
            ),
            GrammarExample(
                "Chiar dacă ar reduce prețul, tot ar trebui să verificăm garanția.",
                note="Reducerea este ipotetică și nu elimină verificarea.",
            ),
        ],
        related=["ro-restrictive-condition-c1", "ro-mediation-links-c1"],
    ),
    GrammarTopic(
        "ro-counterfactual-reproach-c1",
        "Condiționalul perfect între reproș și alternativă",
        "C1",
        "Condiții și negociere",
        "Interpretează ce se reproșează fără să confunzi alternativa trecută cu o cerere prezentă.",
        "«Ai fi putut să mă anunți» poate reproșa o acțiune neîndeplinită, dar exprimă "
        "literal o posibilitate trecută. Contextul și tonul îi dau forța de reproș. "
        "«Ar fi trebuit să» evaluează retrospectiv ceea ce era necesar sau potrivit. "
        "Pentru o soluție actuală, adaugă explicit ce dorești de acum înainte.",
        rules=[
            "O evaluare retrospectivă nu precizează singură o obligație viitoare.",
            "La relatare, păstrează cine ar fi trebuit să acționeze și cine era afectat.",
        ],
        examples=[
            GrammarExample(
                "Ai fi putut să mă anunți că întârzii; am așteptat degeaba.",
                note="Așteptarea nereușită susține lectura de reproș.",
            ),
            GrammarExample(
                "Ar fi trebuit să verificăm adresa. Data viitoare o confirmăm înainte de plecare.",
                note="Evaluarea trecutului și soluția viitoare sunt exprimate separat.",
            ),
            GrammarExample(
                "Înțeleg că te-a deranjat așteptarea și îmi pare rău. "
                "Data viitoare te anunț imediat dacă întârzii.",
                note="Răspunsul recunoaște efectul întârzierii și propune o soluție concretă.",
            ),
        ],
        related=["ro-reported-conditional-c1", "ro-focus-repair-c1"],
    ),
    GrammarTopic(
        "ro-genitive-chains-c1",
        "Acordul lui al în grupuri nominale complexe",
        "C1",
        "Referință și posesie",
        "Urmărește obiectul posedat chiar când între el și posesor apar alte cuvinte.",
        "Articolul genitival «al, a, ai, ale» se acordă cu obiectul posedat, nu cu "
        "posesorul. În «două propuneri noi ale comisiei», «ale» corespunde propunerilor. "
        "Lanțurile de genitive pot ascunde relațiile; la nevoie, separă-le în propoziții. "
        "Forma «a» din «înaintea ședinței» nu se analizează ca articol genitival independent.",
        rules=[
            "Identifică mai întâi substantivul determinat de grupul genitival.",
            "În reformulare, păstrează relația de apartenență sau de autor, fără a le confunda.",
        ],
        examples=[
            GrammarExample("Am discutat două observații importante ale coordonatoarei."),
            GrammarExample(
                "Un exemplar al raportului comisiei a rămas la secretariat.",
                note="«Al» leagă exemplarul de raport; «comisiei» determină «raportului».",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                "Două propuneri noi a comisiei au fost acceptate.",
                "Două propuneri noi ale comisiei au fost acceptate.",
                "Articolul se acordă cu «propuneri», feminin plural.",
            )
        ],
        related=["ro-relative-case-c1", "ro-nominalisation-roles-c1"],
    ),
    GrammarTopic(
        "ro-relative-case-c1",
        "Căruia, căreia și acordul posesiv în relative",
        "C1",
        "Referință și posesie",
        "Leagă cazul relativului de funcția lui și acordul posesiv de obiectul posedat.",
        "În «colega căreia i-am scris», verbul «a scrie cuiva» cere dativul, iar "
        "pronumele neaccentuat reia destinatarul. În «colega al cărei articol», «cărei» "
        "se raportează la colegă, iar «al» la articol. Aceste două acorduri trebuie "
        "urmărite separat, mai ales când substantivul posedat este la plural.",
        rules=[
            "Alege cazul după rolul relativului în propoziția pe care o introduce.",
            "Acordă «al, a, ai, ale» cu substantivul care denumește obiectul posedat.",
        ],
        examples=[
            GrammarExample("Aceasta este colega căreia i-am încredințat dosarul."),
            GrammarExample(
                "Am invitat cercetătoarea ale cărei studii le-am discutat.",
                note="«Cărei» trimite la cercetătoare; «ale» se acordă cu «studii».",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                "Colega a cărei articol l-am citit va participa.",
                "Colega al cărei articol l-am citit va participa.",
                "«Articol» este neutru singular și cere forma «al», ca substantivele masculine la singular.",
            )
        ],
        related=["ro-genitive-chains-c1", "ro-relative-information-c1"],
    ),
    GrammarTopic(
        "ro-possessive-dative-c1",
        "Dativul posesiv și persoana afectată",
        "C1",
        "Referință și posesie",
        "Deosebește posesorul, destinatarul și beneficiarul când forma pronominală este aceeași.",
        "În «Mi-am uitat cheile», «mi-» indică posesia raportată la subiect. În "
        "«I-am reparat bicicleta», dativul poate indica persoana în beneficiul căreia "
        "lucrez; contextul poate sugera și că bicicleta îi aparține. Cele două interpretări "
        "nu sunt mereu identice. Dacă proprietatea contează, precizează «bicicleta ei» "
        "sau «bicicleta închiriată de ea».",
        rules=[
            "Nu deduce automat proprietatea juridică dintr-un dativ de interes.",
            "Păstrează persoana afectată când transformi un clitic într-un grup nominal.",
        ],
        examples=[
            GrammarExample("Și-a lăsat actele pe birou și s-a întors după ele."),
            GrammarExample(
                "I-am dus valiza până la taxi; era împrumutată de la sora ei.",
                note="Ajutorul o privește pe destinatară, dar valiza nu îi aparține.",
            ),
        ],
        related=["ro-ethical-dative-c1", "ro-relative-case-c1"],
    ),
    GrammarTopic(
        "ro-narrative-perspective-c1",
        "Mai-mult-ca-perfectul și reperele unei relatări",
        "C1",
        "Organizarea povestirii",
        "Integrează o întoarcere în timp și revino clar la firul principal.",
        "Mai-mult-ca-perfectul situează o acțiune înaintea unui reper trecut. Repere precum "
        "«cu o zi înainte» se raportează la scena relatată, nu obligatoriu la ziua vorbirii. "
        "Alternanța cu perfectul compus și imperfectul organizează evenimentele și fundalul; "
        "nu impune ordinea în care trebuie povestite. La revenire, numește reperul dacă "
        "altfel succesiunea ar deveni neclară.",
        rules=[
            "Separă ordinea prezentării de ordinea în care au avut loc evenimentele.",
            "La o schimbare de reper, verifică sensul lui «atunci», «înainte» și «a doua zi».",
        ],
        examples=[
            GrammarExample(
                "Când am ajuns la Brașov, gazda plecase deja. Cu o seară înainte îmi trimisese codul.",
                note="Ambele acțiuni ale gazdei precedă sosirea.",
            ),
            GrammarExample(
                "Am deschis ușa. Înăuntru mirosea a vopsea: cineva zugrăvise în lipsa mea.",
                note="Acțiunea anterioară explică starea observată.",
            ),
        ],
        related=["ro-gerund-controller-c1", "ro-relative-information-c1"],
    ),
    GrammarTopic(
        "ro-gerund-controller-c1",
        "Gerunziul și identificarea autorului acțiunii",
        "C1",
        "Organizarea povestirii",
        "Folosește construcții condensate numai dacă relația dintre acțiuni rămâne clară.",
        "În «Citind mesajul, Irina a observat greșeala», subiectul gerunziului se înțelege "
        "din propoziția principală. Româna admite și gerunzii cu subiect propriu, de exemplu "
        "«Venind ploaia, ne-am adăpostit». Problema nu este simpla existență a două subiecte, "
        "ci lipsa unei legături clare. O subordonată cu verb personal poate elimina ambiguitatea "
        "și preciza dacă relația este temporală sau cauzală.",
        rules=[
            "Nu atribui mecanic orice gerunziu subiectului principalei.",
            "Nu transforma simultaneitatea într-o relație cauzală dacă textul nu o susține.",
        ],
        examples=[
            GrammarExample(
                "Recitind contractul, Ioana a găsit clauza. — Când a recitit contractul, Ioana a găsit clauza."
            ),
            GrammarExample(
                "Fiind deja târziu, am amânat discuția.",
                note="Construcția impersonală exprimă împrejurarea care motivează amânarea.",
            ),
        ],
        related=["ro-narrative-perspective-c1", "ro-nominalisation-roles-c1"],
    ),
    GrammarTopic(
        "ro-relative-information-c1",
        "Relative restrictive și explicații suplimentare",
        "C1",
        "Organizarea povestirii",
        "Arată dacă o relativă selectează un grup sau adaugă o informație despre el.",
        "«Participanții care au confirmat primesc un mesaj» selectează participanții "
        "care au confirmat. «Participanții, care au confirmat, primesc un mesaj» prezintă "
        "confirmarea ca informație suplimentară despre grupul deja identificat. În scris, "
        "virgulele marchează diferența; în vorbire intervin pauzele și contextul. "
        "Nu folosi punctuația pentru a sugera o generalizare pe care datele nu o susțin.",
        rules=[
            "Într-un anunț, verifică dacă instrucțiunea se adresează tuturor sau unui subgrup.",
            "La reformulare, păstrează domeniul grupului vizat.",
        ],
        examples=[
            GrammarExample(
                "Locatarii care au depus cereri vor primi răspuns individual.",
                note="Nu se afirmă că toți locatarii au depus cereri.",
            ),
            GrammarExample(
                "Cele două vecine, care depuseseră deja cererile, au primit răspuns.",
                note="Relativa adaugă o informație despre ambele vecine.",
            ),
        ],
        related=["ro-relative-case-c1", "ro-quantified-negation-c1"],
    ),
    GrammarTopic(
        "ro-evaluative-supine-c1",
        "Supinul în evaluări și sarcini rămase",
        "C1",
        "Condensare și argumentare",
        "Interpretează construcțiile cu supin fără să le atribui un agent neexprimat.",
        "«Este greu de verificat» evaluează dificultatea, iar «rămâne de verificat» "
        "indică o sarcină neîncheiată. Niciuna nu spune singură cine o va executa. "
        "În «probleme greu de rezolvat», adverbul «greu» nu se acordă cu substantivul. "
        "Pentru organizarea muncii, completează evaluarea cu un responsabil și un termen "
        "numai dacă aceștia au fost conveniți.",
        rules=[
            "Dificultatea unei acțiuni nu înseamnă imposibilitatea ei.",
            "Nu transforma «de verificat» în «verificat» când rezumi stadiul unei lucrări.",
        ],
        examples=[
            GrammarExample("Explicația este plauzibilă, dar rămâne de verificat."),
            GrammarExample(
                "Sunt două neconcordanțe greu de lămurit fără documentele originale.",
                note="Se exprimă dificultatea și condiția de lucru, nu un rezultat final.",
            ),
        ],
        related=["ro-impersonal-responsibility-c1", "ro-nominalisation-roles-c1"],
    ),
    GrammarTopic(
        "ro-nominalisation-roles-c1",
        "Nominalizarea și rolurile participanților",
        "C1",
        "Condensare și argumentare",
        "Transformă numele unei acțiuni în propoziție fără să inversezi participanții.",
        "În «respingerea cererii de către comisie», cererea este obiectul respingerii, "
        "iar comisia este autorul. Un genitiv izolat poate fi ambiguu: «critica "
        "profesorului» poate avea profesorul ca autor sau ca țintă a criticii. "
        "Nu alege o interpretare doar pentru a simplifica textul; cere contextul lipsă. "
        "Timpul și modalitatea se recuperează din enunțul complet.",
        rules=[
            "Păstrează deosebirea dintre o propunere de acțiune și acțiunea realizată.",
            "Dacă autorul nu este cunoscut, nu îl inventa într-o reformulare activă.",
        ],
        examples=[
            GrammarExample(
                "Respingerea cererii de către comisie a surprins-o pe Ana. "
                "— Comisia a respins cererea, ceea ce a surprins-o pe Ana."
            ),
            GrammarExample(
                "Se propune revizuirea programului. — Există o propunere ca programul să fie revizuit.",
                note="Revizuirea nu este prezentată drept fapt împlinit.",
            ),
        ],
        related=["ro-genitive-chains-c1", "ro-impersonal-responsibility-c1"],
    ),
    GrammarTopic(
        "ro-quantified-negation-c1",
        "Nu toți, niciunul și limitele generalizării",
        "C1",
        "Condensare și argumentare",
        "Păstrează domeniul negației în concluzii și rezumate.",
        "«Nu toți au acceptat» respinge acceptarea unanimă, dar nu precizează câți au "
        "acceptat. «Niciunul nu a acceptat» exclude fiecare membru al grupului. "
        "În română, pronumele negative se asociază în mod normal cu negația verbală; "
        "această concordanță nu produce un sens afirmativ. «Nu neapărat» contestă "
        "necesitatea concluziei, nu afirmă automat contrariul.",
        rules=[
            "Nu extrage un procent sau o majoritate dintr-o negație parțială.",
            "Păstrează distincția dintre «nu este sigur că» și «este sigur că nu».",
        ],
        examples=[
            GrammarExample(
                "Nu toate observațiile au fost respinse; două au fost preluate în proiect.",
                note="A doua parte oferă un număr pe care prima nu îl preciza.",
            ),
            GrammarExample(
                "Un buget mai mare nu înseamnă neapărat un termen mai scurt.",
                note="Efectul este posibil, dar nu garantat.",
            ),
        ],
        related=["ro-modal-scope-c1", "ro-relative-information-c1"],
    ),
    GrammarTopic(
        "ro-discourse-particles-c1",
        "Păi, doar și totuși în gestionarea replicilor",
        "C1",
        "Interacțiune și atitudine",
        "Interpretează legătura dintre replică, așteptare și informația considerată comună.",
        "«Păi» poate introduce o explicație, o ezitare sau o obiecție în conversație. "
        "«Doar» poate restrânge cantitatea, dar în «Doar am stabilit asta!» invocă "
        "un fapt considerat comun. «Totuși» menține o concluzie în ciuda unei așteptări. "
        "Tonul poate transforma o reamintire într-un reproș; nu trata particula izolată "
        "ca probă sigură a intenției.",
        rules=[
            "Verifică dacă «doar» înseamnă «numai» sau invocă un argument cunoscut.",
            "Într-un mesaj formal, înlocuiește o replică abruptă cu o explicație explicită.",
        ],
        examples=[
            GrammarExample(
                "Păi, tocmai de aceea te-am sunat: să nu pleci înainte să confirmăm.",
                note="Particula leagă explicația de replica anterioară.",
            ),
            GrammarExample(
                "Doar am convenit să ne consultăm; de ce ai trimis deja răspunsul?",
                note="Vorbitorul invocă acordul comun și formulează un reproș.",
            ),
        ],
        related=["ro-focus-repair-c1", "ro-ethical-dative-c1"],
    ),
    GrammarTopic(
        "ro-ethical-dative-c1",
        "Dativul etic și implicarea afectivă",
        "C1",
        "Interacțiune și atitudine",
        "Recunoaște o marcă de implicare fără să adaugi un beneficiar acțiunii.",
        "În formulări familiare precum «Să nu-mi răcești!», «mi-» poate exprima "
        "grija sau implicarea vorbitorului, nu un destinatar propriu-zis. Acest dativ "
        "etic apare mai ales în registrul oral și expresiv. Nu orice dativ este etic: "
        "în «Mi-a trimis scrisoarea», pronumele indică destinatarul. Interpretarea "
        "depinde de verb și de context, nu doar de forma scurtă.",
        rules=[
            "Pentru producție neutră, poți exprima direct grija în locul dativului expresiv.",
            "Nu transfera automat această familiaritate într-un mesaj instituțional.",
        ],
        examples=[
            GrammarExample(
                "Să nu-mi răcești pe drum; ia-ți fularul!",
                note="«Mi-» marchează implicarea afectivă a persoanei care vorbește.",
            ),
            GrammarExample(
                "Și mi ți-l ia la întrebări de față cu toată lumea!",
                note="Construcție narativă familiară, de recunoscut: mi implică afectiv "
                "naratorul, ți implică interlocutorul, iar l îl desemnează pe cel luat la întrebări.",
            ),
        ],
        related=["ro-possessive-dative-c1", "ro-discourse-particles-c1"],
    ),
    GrammarTopic(
        "ro-focus-repair-c1",
        "Focalizare contrastivă și corectarea unei neînțelegeri",
        "C1",
        "Interacțiune și atitudine",
        "Corectează partea greșită a unei interpretări fără să retragi restul mesajului.",
        "Ordinea cuvintelor și accentul pot izola elementul corectat: «Anei i-am trimis "
        "schița, nu lui Vlad». Reluarea prin clitic păstrează construcția firească "
        "în acest tip de focalizare. «Mai precis» restrânge sau clarifică, iar «de fapt» "
        "poate revizui o afirmație. În scris, repetă informația decisivă în loc să "
        "depindă totul de un accent care nu se aude.",
        rules=[
            "Numește exact elementul corectat: destinatar, document, dată sau grad de certitudine.",
            "Nu prezenta o schimbare de fapt drept simplă reformulare echivalentă.",
        ],
        examples=[
            GrammarExample("Anei i-am trimis schița, nu lui Vlad; Vlad a primit doar invitația."),
            GrammarExample(
                "Ne vedem joi — mă corectez, vineri, la aceeași oră.",
                note="Se schimbă ziua, nu ora întâlnirii.",
            ),
        ],
        related=["ro-discourse-particles-c1", "ro-subjunctive-agency-c1"],
    ),
    GrammarTopic(
        "ro-subjunctive-agency-c1",
        "Conjunctivul și atribuirea sarcinii",
        "C1",
        "Mediere și responsabilitate",
        "Păstrează distincte persoana care cere, persoana care acționează și destinatarul rezultatului.",
        "În «Ana i-a cerut lui Vlad să trimită dosarul», Vlad este cel căruia i se cere "
        "acțiunea. În «Ana i-a promis lui Vlad că va trimite dosarul», Ana este, în "
        "lectura obișnuită, cea care își asumă trimiterea. Forma subordonatei și verbul "
        "regent ghidează interpretarea. Dacă apar mai mulți participanți, repetă numele "
        "în rezumat când altfel subiectul ar rămâne ambiguu.",
        rules=[
            "Nu transforma o cerere într-o promisiune sau o recomandare într-o decizie.",
            "Păstrează persoana gramaticală și destinatarul când treci la relatare.",
        ],
        examples=[
            GrammarExample(
                "Ana i-a cerut lui Vlad să-i trimită ei dosarul până joi.",
                note="Ana cere; Vlad trebuie să trimită; Ana este destinatarul.",
            ),
            GrammarExample(
                "Vlad a propus ca Ana să prezinte rezultatele.",
                note="Propunerea îi aparține lui Vlad; prezentarea ar urma să o facă Ana.",
            ),
        ],
        related=["ro-focus-repair-c1", "ro-impersonal-responsibility-c1"],
    ),
    GrammarTopic(
        "ro-impersonal-responsibility-c1",
        "Construcții impersonale și răspundere explicită",
        "C1",
        "Mediere și responsabilitate",
        "Explică ce se cere fără să atribui artificial autoritate sau responsabilitate.",
        "«Se recomandă», «se impune» și «s-a decis» nu au aceeași forță. Pasivul și "
        "construcțiile impersonale pot omite autorul, dar nu justifică inventarea lui. "
        "În «se trimit notificările», verbul se acordă cu subiectul plural; în "
        "«se lucrează la notificări» construcția este impersonală. Pentru coordonare, "
        "cere separat cine execută sarcina și cine a autorizat-o.",
        rules=[
            "Păstrează diferența dintre recomandare, necesitate și decizie realizată.",
            "Precizează agentul doar dacă informația este disponibilă și relevantă.",
        ],
        examples=[
            GrammarExample(
                "Se recomandă înscrierea online, dar cererile se primesc și la ghișeu.",
                note="Recomandarea nu exclude cealaltă procedură.",
            ),
            GrammarExample(
                "S-a decis amânarea. — Cine a luat decizia și cine îi anunță pe participanți?",
                note="Autorul deciziei și executantul comunicării pot fi diferiți.",
            ),
        ],
        related=["ro-evaluative-supine-c1", "ro-subjunctive-agency-c1"],
    ),
    GrammarTopic(
        "ro-mediation-links-c1",
        "Coeziunea unui rezumat de negociere",
        "C1",
        "Mediere și responsabilitate",
        "Leagă pozițiile fără să creezi un consens sau o cauzalitate inexistente.",
        "«Pe de o parte... pe de altă parte» organizează perspective, iar «în schimb» "
        "poate introduce contrastul ori o contraprestație. «Prin urmare» anunță o "
        "concluzie, nu doar o nouă informație. Într-un proces-verbal, «s-a propus» "
        "și «s-a convenit» trebuie păstrate distincte. Numește punctele comune și "
        "rezervele fiecărei părți înainte de concluzie.",
        rules=[
            "Nu folosi un conector concluziv dacă legătura logică nu este susținută.",
            "Lipsa unei obiecții consemnate nu dovedește automat acordul tuturor.",
        ],
        examples=[
            GrammarExample(
                "Locatarii acceptă lucrările dimineața; în schimb, cer liniște după ora șase.",
                note="Se prezintă condițiile unui posibil compromis.",
            ),
            GrammarExample(
                "Am convenit asupra bugetului. În privința datei, au rămas două propuneri.",
                note="Acordul parțial nu este extins la aspectul încă deschis.",
            ),
        ],
        related=["ro-concessive-alternatives-c1", "ro-subjunctive-agency-c1"],
    ),
]
