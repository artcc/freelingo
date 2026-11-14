"""Romanian B2 grammar for scope, evidence and extended discourse."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "ro-subjunctive-perfect-b2",
        "Conjunctivul perfect: o acțiune anterioară",
        "B2",
        "Mod și anterioritate",
        "Exprimați posibilitatea sau evaluarea unei acțiuni deja petrecute.",
        "Conjunctivul perfect are forma să fi urmat de participiu: să fi plecat. "
        "Fi și participiul nu se schimbă după persoană: eu să fi plecat, ei să fi plecat. "
        "Contextul precizează persoana și reperul temporal. Comparați E posibil să plece "
        "cu E posibil să fi plecat: a doua formulare privește o plecare anterioară.",
        rules=[
            "Nu acordați participiul cu subiectul în această formă verbală.",
            "Negația precedă fi: să nu fi primit.",
            "Forma nu confirmă evenimentul când este introdusă prin e posibil.",
        ],
        examples=[
            GrammarExample("E posibil ca ei să fi înțeles alt termen."),
            GrammarExample("Este posibil să nu fi primit invitația."),
        ],
        common_mistakes=[
            GrammarMistake(
                "E posibil ca ea să fie plecat ieri.",
                "E posibil ca ea să fi plecat ieri.",
                "Pentru acțiunea anterioară, conjunctivul perfect folosește fi.",
            ),
        ],
        related=["ro-conditional-perfect-b2", "ro-modal-certainty-b2"],
    ),
    GrammarTopic(
        "ro-conditional-perfect-b2",
        "Condiționalul perfect: alternative nerealizate",
        "B2",
        "Mod și anterioritate",
        "Discutați ce s-ar fi putut întâmpla în alte condiții.",
        "Condiționalul perfect se formează cu aș, ai, ar, am, ați, ar + fi + participiu. "
        "Într-un context contrafactual, condiția și rezultatul privesc un trecut diferit "
        "de cel cunoscut: Dacă aș fi știut, aș fi venit. Forma poate avea și alte valori, "
        "de exemplu atribuirea prudentă unei surse; sensul contrafactual nu este automat.",
        rules=[
            "Participiul rămâne invariabil: ele ar fi venit.",
            "Plasați negația înaintea auxiliarului: nu aș fi acceptat.",
            "Distingeți regretul vorbitorului de o acuzație sau de o simplă relatare.",
        ],
        examples=[
            GrammarExample("Dacă am fi primit devizul ieri, am fi discutat costurile la ședință."),
            GrammarExample("Aș fi preferat să mă anunțați înainte de modificare."),
        ],
        related=["ro-mixed-conditions-b2", "ro-reported-stance-b2"],
    ),
    GrammarTopic(
        "ro-mixed-conditions-b2",
        "Ipoteze cu repere temporale diferite",
        "B2",
        "Condiție și consecință",
        "Legați o decizie trecută de un efect prezent sau o trăsătură de un rezultat trecut.",
        "Timpul condiției și timpul consecinței se aleg după sens. Dacă am fi investit atunci, "
        "am avea acum mai mult spațiu leagă un trecut nerealizat de un rezultat prezent. "
        "Dacă aș fi mai atent, nu aș fi ratat acel detaliu leagă o caracteristică generală "
        "de un episod trecut. Adverbele atunci, acum și ieri ajută la interpretare.",
        rules=[
            "Nu impuneți același timp ambelor propoziții dacă reperele diferă.",
            "Păstrați persoanele și gradul de certitudine când reformulați o ipoteză.",
        ],
        examples=[
            GrammarExample("Dacă ar fi plecat la timp, acum ar fi aici."),
            GrammarExample("Dacă aș cunoaște mai bine zona, nu m-aș fi rătăcit ieri."),
        ],
        related=["ro-conditional-perfect-b2", "ro-restrictive-conditions-b2"],
    ),
    GrammarTopic(
        "ro-clitic-placement-b2",
        "Clitice în grupuri verbale și în cereri",
        "B2",
        "Pronume și domeniul referinței",
        "Păstrați obiectul și destinatarul când schimbați forma unei solicitări.",
        "Cliticele au poziții legate de forma verbală: mi-l trimite, să mi-l trimită, "
        "mi l-ar trimite, trimite-mi-l. Imperativul afirmativ le atașează după verb; "
        "la imperativul negativ stau înainte: nu mi-l trimite. Pentru femininul singular, "
        "perfectul compus păstrează o după participiu: mi-a trimis-o.",
        rules=[
            "Cu infinitiv: pentru a mi-l trimite; cu conjunctiv: ca să mi-l trimită.",
            "În ar putea să mi-l trimită, grupul mi-l aparține verbului a trimite.",
            "Verificați separat persoana destinatarului și genul obiectului.",
        ],
        examples=[
            GrammarExample("Raportul este final. Trimiteți-mi-l până mâine, vă rog."),
            GrammarExample("Ciorna nu este verificată; nu mi-o trimite încă."),
            GrammarExample("Ar putea să ni le explice la întâlnire."),
        ],
        related=["ro-possessive-dative-b2", "ro-relative-cases-b2"],
    ),
    GrammarTopic(
        "ro-possessive-dative-b2",
        "Dativul posesiv și persoana afectată",
        "B2",
        "Pronume și domeniul referinței",
        "Interpretați legătura dintre o persoană și obiectul afectat de acțiune.",
        "În Mi-am pierdut cheile, mi indică legătura cu posesorul și coincide cu subiectul. "
        "În Mi-a pierdut cheile, subiectul este altcineva, iar cheile sunt ale vorbitorului "
        "în interpretarea obișnuită. Un dativ poate marca și persoana afectată fără posesie "
        "literală: Mi-au schimbat programul. Contextul stabilește relația.",
        rules=[
            "Comparați și-a verificat dosarul cu i-a verificat dosarul.",
            "Articolul hotărât poate apărea fără posesiv explicit: mi-am luat geanta.",
            "Nu presupuneți că orice dativ indică proprietatea juridică.",
        ],
        examples=[
            GrammarExample("Și-a actualizat datele înainte de înscriere."),
            GrammarExample("Asistenta mi-a verificat tensiunea."),
            GrammarExample("Mi-au amânat interviul, așa că trebuie să schimb biletul."),
        ],
        related=["ro-clitic-placement-b2", "ro-relative-cases-b2"],
    ),
    GrammarTopic(
        "ro-relative-cases-b2",
        "Căruia, căreia, cărora și acordul posesiei",
        "B2",
        "Propoziții relative",
        "Exprimați destinatarul sau posesia într-o descriere precisă.",
        "Căruia, căreia și cărora se aleg după antecedent: colegul căruia îi scriu, "
        "colega căreia îi scriu, colegii cărora le scriu. În construcția posesivă apar "
        "două acorduri: instituția ale cărei proiecte au fost aprobate. Cărei trimite "
        "la instituția, iar ale se acordă cu proiecte.",
        rules=[
            "Dativul relativ este reluat prin clitic: persoana căreia i-am răspuns.",
            "În posesie, al/a/ai/ale se acordă cu substantivul posedat.",
            "Antecedentul determină cărui/cărei/căror, nu articolul genitival.",
        ],
        examples=[
            GrammarExample("Acesta este autorul al cărui articol l-am citit."),
            GrammarExample("Am contactat asociația ai cărei membri au făcut propunerea."),
            GrammarExample("Au răspuns firmele cărora le-am cerut oferte."),
        ],
        related=["ro-clitic-placement-b2", "ro-possessive-dative-b2"],
    ),
    GrammarTopic(
        "ro-agent-passive-b2",
        "Pasivul cu a fi și exprimarea autorului",
        "B2",
        "Acțiune și rezultat",
        "Mutați accentul de la autor la acțiunea suferită de un participant.",
        "Pasivul cu a fi și participiu permite prezentarea unui document, a unei persoane "
        "sau a unei lucrări ca subiect: Cererea a fost aprobată de comisie. Participiul "
        "se acordă cu subiectul. Autorul poate fi exprimat prin de sau de către; de către "
        "este frecvent în stilul administrativ și nu trebuie adăugat mecanic peste tot.",
        rules=[
            "Păstrați timpul acțiunii: comisia a aprobat — cererea a fost aprobată.",
            "La plural: cererile au fost aprobate.",
            "Omiterea autorului nu înseamnă că acesta este necunoscut.",
        ],
        examples=[
            GrammarExample("Raportul va fi analizat de o echipă independentă."),
            GrammarExample("Participanții au fost informați prin e-mail."),
        ],
        related=["ro-participial-result-b2", "ro-supine-b2"],
    ),
    GrammarTopic(
        "ro-participial-result-b2",
        "Participiul: eveniment sau stare rezultată?",
        "B2",
        "Acțiune și rezultat",
        "Distingeți descrierea unei stări de relatarea unei intervenții.",
        "Un participiu poate participa la pasiv sau poate descrie o stare. În Ușa este închisă, "
        "contextul poate indica starea actuală; în Ușa este închisă de portar în fiecare seară, "
        "este descrisă o acțiune repetată. Expresii precum deja, încă, de către și un reper "
        "temporal contribuie la interpretare, fără a funcționa ca etichete infailibile.",
        rules=[
            "Participiul cu valoare adjectivală se acordă: dosare completate, cereri respinse.",
            "Comparați a fost reparată ieri cu este reparată și poate fi folosită.",
            "Precizați acțiunea dacă diferența are consecințe practice.",
        ],
        examples=[
            GrammarExample("La sosirea echipei, poarta era deja închisă."),
            GrammarExample("Poarta a fost închisă de paznic la ora opt."),
            GrammarExample("Documentele semnate sunt în dosarul albastru."),
        ],
        related=["ro-agent-passive-b2", "ro-discourse-aspect-b2"],
    ),
    GrammarTopic(
        "ro-supine-b2",
        "Supinul: de făcut, de verificat, de citit",
        "B2",
        "Forme nepersonale",
        "Numiți sarcina rămasă, destinația unui obiect sau dificultatea unei acțiuni.",
        "Supinul are forma participiului precedată de o prepoziție, frecvent de: "
        "am de completat, documente de verificat. Spre deosebire de participiul adjectival, "
        "supinul nu se acordă: cereri de completat. În am de trimis, persoana responsabilă "
        "este indicată de verbul a avea.",
        rules=[
            "Distingeți formulare completate de formulare de completat.",
            "Este greu de explicat descrie dificultatea, nu o acțiune deja realizată.",
            "O construcție fără autor explicit poate cere clarificare într-un plan de lucru.",
        ],
        examples=[
            GrammarExample("Mai avem de verificat trei facturi."),
            GrammarExample("Acesta este un aparat de măsurat umiditatea."),
            GrammarExample("Diferența este greu de observat fără grafic."),
        ],
        related=["ro-participial-result-b2", "ro-infinitive-b2"],
    ),
    GrammarTopic(
        "ro-gerund-b2",
        "Gerunziul și identificarea autorului",
        "B2",
        "Forme nepersonale",
        "Legați acțiuni simultane sau exprimați împrejurarea unei concluzii.",
        "Gerunziul se termină în -ând sau -ind: lucrând, citind, fiind. Autorul se "
        "identifică adesea prin subiectul propoziției principale: Citind raportul, "
        "am observat eroarea. Gerunziul poate avea și un subiect propriu: "
        "Terminându-se ședința, participanții au ieșit. Nu impuneți același subiect "
        "tuturor construcțiilor; verificați cine participă la fiecare acțiune.",
        rules=[
            "Negația se poate forma cu ne-: neștiind, neavând.",
            "Cliticele se atașează: explicându-i, citindu-l, spunându-le.",
            "Când participanții diferă, o propoziție explicită este adesea mai clară.",
        ],
        examples=[
            GrammarExample("Comparând ofertele, am observat diferența de garanție."),
            GrammarExample("Neavând toate datele, comisia a amânat decizia."),
            GrammarExample(
                "Terminându-se ședința, participanții au ieșit.",
                note="Ședința se termină, participanții ies: subiectele sunt diferite și explicite.",
            ),
        ],
        related=["ro-infinitive-b2", "ro-discourse-aspect-b2"],
    ),
    GrammarTopic(
        "ro-infinitive-b2",
        "Infinitivul în explicații și în stilul profesional",
        "B2",
        "Forme nepersonale",
        "Alegeți între infinitiv și conjunctiv după construcție și registru.",
        "Infinitivul cu a apare în structuri precum înainte de a semna, fără a modifica, "
        "pentru a clarifica și dreptul de a contesta. În conversație, variantele cu să "
        "sunt adesea firești: înainte să semnez. Alegerea nu permite ștergerea diferenței "
        "dintre subiecte; precizați persoana când ar putea apărea o ambiguitate.",
        rules=[
            "După a putea se folosește și infinitivul fără a: putem verifica.",
            "Negația urmează a: pentru a nu întârzia.",
            "Nu generalizați infinitivul la orice verb: vreau să particip este tiparul uzual.",
        ],
        examples=[
            GrammarExample("Vă rugăm să citiți condițiile înainte de a semna."),
            GrammarExample("Am reformulat paragraful fără a modifica obligațiile."),
            GrammarExample("Avem dreptul de a cere o explicație."),
        ],
        related=["ro-gerund-b2", "ro-supine-b2"],
    ),
    GrammarTopic(
        "ro-discourse-aspect-b2",
        "Început, continuare, rezultat și reluare",
        "B2",
        "Timp și organizarea discursului",
        "Arătați stadiul unei activități, nu doar momentul ei.",
        "Româna exprimă perspectiva asupra desfășurării prin timpuri, sensul verbului și "
        "construcții precum începe să, continuă să, termină de, reia. A lucra la un raport "
        "nu afirmă finalizarea lui; a termina raportul o afirmă. Tot în tot insistă poate "
        "marca repetarea persistentă, iar încă în încă lucrează indică menținerea situației.",
        rules=[
            "Nu deduceți finalizarea numai din durata delimitată: a lucrat două ore.",
            "A încetat să lucreze nu înseamnă neapărat că a terminat lucrarea.",
            "Din nou poate marca reluarea; nu îl confundați cu în continuare.",
        ],
        examples=[
            GrammarExample("A lucrat la raport toată dimineața, dar nu l-a terminat."),
            GrammarExample("După pauză, echipa a reluat verificările."),
            GrammarExample("Nu mai trimite mesaje, dar încă așteaptă răspunsul."),
        ],
        related=["ro-participial-result-b2", "ro-gerund-b2"],
    ),
    GrammarTopic(
        "ro-hypothetical-concession-b2",
        "Concesie factuală și concesie ipotetică",
        "B2",
        "Argumentare și condiții",
        "Distingeți un obstacol recunoscut de unul doar luat în calcul.",
        "Deși și cu toate că prezintă de regulă un fapt acceptat. Chiar dacă poate "
        "introduce un scenariu posibil; timpul și contextul arată interpretarea. "
        "Chiar dacă am primi finanțarea, tot ar trebui să reducem costurile arată "
        "că ipoteza favorabilă nu elimină o necesitate.",
        rules=[
            "Nu înlocuiți deși cu chiar dacă dacă astfel transformați faptul în ipoteză.",
            "Cu toate că introduce o propoziție; în ciuda introduce un grup nominal în genitiv.",
            "Tot poate sublinia persistența rezultatului în ciuda condiției.",
        ],
        examples=[
            GrammarExample("În ciuda întârzierilor, lucrările au fost finalizate."),
            GrammarExample(
                "Chiar dacă termenul s-ar prelungi, echipa tot ar avea nevoie de ajutor."
            ),
        ],
        related=["ro-restrictive-conditions-b2", "ro-mixed-conditions-b2"],
    ),
    GrammarTopic(
        "ro-restrictive-conditions-b2",
        "Numai dacă, cu condiția să și dacă nu",
        "B2",
        "Argumentare și condiții",
        "Stabiliți limitele unui acord fără să inversați condiția și rezultatul.",
        "Numai dacă prezintă o condiție necesară: Rambursăm suma numai dacă prezentați bonul "
        "nu promite că bonul este singura cerință. Cu condiția să formulează explicit o "
        "cerință pentru acord. Dacă nu introduce o condiție negativă, iar în caz contrar "
        "trimite la neîndeplinirea situației descrise anterior.",
        rules=[
            "Dacă P, Q și Q numai dacă P nu au aceeași direcție logică.",
            "După cu condiția folosiți să: cu condiția să confirmați.",
            "Precizați ce condiție se neagă înainte de în caz contrar.",
        ],
        examples=[
            GrammarExample("Acceptăm schimbarea cu condiția să păstrați garanția."),
            GrammarExample("Accesul este permis numai dacă aveți ecuson și programare."),
            GrammarExample("Confirmați până joi; în caz contrar, rezervarea expiră."),
        ],
        related=["ro-hypothetical-concession-b2", "ro-proportion-b2"],
    ),
    GrammarTopic(
        "ro-proportion-b2",
        "Cu cât… cu atât și pe măsură ce",
        "B2",
        "Argumentare și condiții",
        "Descrieți două variații corelate și evoluția treptată.",
        "Cu cât… cu atât leagă două grade: Cu cât comanda este mai mare, cu atât prețul "
        "pe bucată este mai mic. Pe măsură ce prezintă o evoluție simultană și progresivă. "
        "O corelație observată nu dovedește singură o cauză; formularea trebuie să respecte datele.",
        rules=[
            "Păstrați sensul comparativelor: mai mare poate corespunde lui mai mic.",
            "Distingeți cantitatea totală de valoarea pe unitate.",
        ],
        examples=[
            GrammarExample("Cu cât amânăm reparația, cu atât cresc costurile."),
            GrammarExample("Pe măsură ce primesc răspunsuri, actualizez lista."),
            GrammarExample("Cu cât explicația este mai clară, cu atât apar mai puține întrebări."),
        ],
        related=["ro-restrictive-conditions-b2", "ro-text-cohesion-b2"],
    ),
    GrammarTopic(
        "ro-reported-stance-b2",
        "Afirmația sursei și poziția celui care relatează",
        "B2",
        "Sursă și certitudine",
        "Atribuiți informația fără să o transformați într-un fapt verificat.",
        "Potrivit raportului, conform declarației și reprezentantul susține că atribuie "
        "informația unei surse. În știri, condiționalul perfect poate marca informații "
        "neconfirmate: Firma ar fi încălcat acordul. Această valoare se distinge din context "
        "de ipoteza contrafactuală; forma singură nu identifică sursa.",
        rules=[
            "Susține că nu implică automat nici adevărul, nici falsitatea afirmației.",
            "Citați separat ce a fost verificat și ce rămâne atribuit.",
            "Nu eliminați ar fi într-un rezumat dacă astfel transformați relatarea în certitudine.",
        ],
        examples=[
            GrammarExample("Potrivit organizatorilor, numărul participanților a crescut."),
            GrammarExample(
                "Presa locală scrie că firma ar fi primit o amendă; nu avem confirmarea."
            ),
        ],
        related=["ro-conditional-perfect-b2", "ro-presumptive-b2", "ro-modal-certainty-b2"],
    ),
    GrammarTopic(
        "ro-presumptive-b2",
        "Recunoașterea prezumtivului: o fi, va fi fiind",
        "B2",
        "Sursă și certitudine",
        "Recunoașteți presupunerea în conversație și în texte.",
        "Forme precum o fi acasă și o fi uitat exprimă adesea o presupunere, nu o informație "
        "confirmată. O fi este frecvent în conversație. Formele cu va fi și gerunziu, precum "
        "va fi lucrând, sunt mai puțin obișnuite și se urmăresc aici pentru recunoaștere. "
        "Va fi plecat poate avea și valoare de viitor anterior: o acțiune încheiată "
        "înaintea unui reper viitor. Acesta se formează cu voi, vei, va, vom, veți, vor "
        "+ fi + participiu. Reperul temporal și contextul disting anterioritatea de presupunere.",
        rules=[
            "O fi uitat nu dovedește uitarea; vorbitorul propune o explicație.",
            "Într-un mesaj formal, probabil sau este posibil să pot exprima presupunerea mai transparent.",
            "Nu interpretați orice va fi ca marcă de incertitudine.",
        ],
        examples=[
            GrammarExample("Nu răspunde. O fi în ședință.", note="Presupunere conversațională."),
            GrammarExample("O fi citit mesajul, dar încă nu avem un răspuns."),
            GrammarExample(
                "Va fi fiind obosit după atâta drum.",
                note="Formă mai rară; se urmărește înțelegerea, nu folosirea obligatorie.",
            ),
            GrammarExample(
                "Până vei ajunge mâine, voi fi terminat raportul.",
                note="Viitor anterior: terminarea precedă sosirea de mâine.",
            ),
        ],
        related=["ro-modal-certainty-b2", "ro-reported-stance-b2"],
    ),
    GrammarTopic(
        "ro-modal-certainty-b2",
        "Poate, trebuie să și gradele de certitudine",
        "B2",
        "Sursă și certitudine",
        "Distingeți posibilitatea, deducția și obligația.",
        "Poate fi are sens de posibilitate sau capacitate, după context. Trebuie să "
        "poate exprima obligația, dar și o deducție: Lumina este aprinsă; trebuie să fie acasă. "
        "Probabil, se pare că și este posibil să limitează certitudinea în moduri diferite. "
        "O concluzie plauzibilă nu devine dovadă doar fiindcă folosește trebuie.",
        rules=[
            "Căutați regula ori indiciul care motivează trebuie să.",
            "Nu întăriți se pare că până la este sigur că într-o reformulare.",
            "Nu este sigur că a venit nu înseamnă este sigur că nu a venit.",
        ],
        examples=[
            GrammarExample("Conform regulamentului, trebuie să depună cererea până vineri."),
            GrammarExample("Are bagajele în hol; probabil se pregătește să plece."),
            GrammarExample("Este posibil să nu fi primit ultima versiune."),
        ],
        related=["ro-presumptive-b2", "ro-subjunctive-perfect-b2"],
    ),
    GrammarTopic(
        "ro-focus-b2",
        "Focalizare: doar, nici măcar, nu… ci",
        "B2",
        "Nuanțe și organizarea mesajului",
        "Precizați ce excludeți, ce adăugați și ce corectați.",
        "Poziția lui doar schimbă domeniul restricției: Doar Ana a trimis raportul exclude "
        "alți expeditori; Ana a trimis doar raportul exclude alte obiecte trimise. "
        "Nu… ci corectează o identificare sau o interpretare. Nici măcar marchează o "
        "așteptare minimă neîndeplinită și apare într-o construcție negativă.",
        rules=[
            "Nu confundați nu doar… ci și, care adaugă, cu nu… ci, care corectează.",
            "Româna folosește concordanța negativă: Nici măcar Ana nu a răspuns.",
            "Plasați elementul focalizat astfel încât contrastul să fie ușor de identificat.",
        ],
        examples=[
            GrammarExample("Nu contestăm scopul proiectului, ci modul de finanțare."),
            GrammarExample("Au venit nu doar angajații, ci și câțiva foști colegi."),
            GrammarExample("Nici măcar confirmarea de primire nu a sosit."),
        ],
        related=["ro-text-cohesion-b2", "ro-hypothetical-concession-b2"],
    ),
    GrammarTopic(
        "ro-text-cohesion-b2",
        "Coeziune: referință, reformulare și contrast",
        "B2",
        "Nuanțe și organizarea mesajului",
        "Construiți un text coerent și rezumați pozițiile fără ambiguități.",
        "Acest lucru poate relua o idee întreagă, iar acesta și aceasta pot trimite la un "
        "substantiv. Când există mai mulți candidați, repetați termenul relevant. "
        "Cu alte cuvinte reformulează, în schimb contrastează, iar prin urmare introduce "
        "o concluzie. Reformularea trebuie să păstreze condițiile și rezervele inițiale.",
        rules=[
            "Nu folosiți un pronume ambiguu când decizia depinde de identificarea persoanei.",
            "Pe de o parte… pe de altă parte organizează perspective, nu impune contradicția.",
            "Un rezumat fidel păstrează sursa și gradul de certitudine.",
        ],
        examples=[
            GrammarExample("Programul a fost redus. Acest lucru a afectat accesul navetiștilor."),
            GrammarExample("Varianta este mai ieftină; în schimb, necesită mai mult timp."),
            GrammarExample(
                "Acceptăm în principiu; cu alte cuvinte, suntem de acord cu ideea generală, "
                "dar detaliile încă trebuie negociate."
            ),
        ],
        related=["ro-focus-b2", "ro-reported-stance-b2", "ro-proportion-b2"],
    ),
]
