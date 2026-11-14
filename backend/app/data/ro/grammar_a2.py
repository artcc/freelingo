"""Romanian A2 grammar for narration, pronoun reference and practical interaction."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "ro-perfect-a2",
        "Perfectul compus: am plecat, am venit",
        "A2",
        "Trecut",
        "Relatăm evenimente încheiate.",
        "Perfectul compus are un auxiliar și un participiu: am, ai, a, am, ați, au "
        "+ plecat. Auxiliarul arată persoana: eu am plecat, noi am plecat. Participiul "
        "nu se acordă cu subiectul.\n\nÎnvățăm participiile frecvente: a merge – mers, "
        "a face – făcut, a vedea – văzut, a veni – venit, a fi – fost, a avea – avut. "
        "Acest timp apare des cu ieri și săptămâna trecută.",
        structure="am / ai / a / am / ați / au + participiu",
        rules=[
            "Ana a venit și Andrei a venit au același participiu.",
            "Eu și noi folosesc am; contextul sau pronumele arată persoana.",
            "Nu formăm toate participiile prin adăugarea terminației -at.",
        ],
        examples=[
            GrammarExample("Ieri am ajuns la Brașov."),
            GrammarExample("Ana și Ioana au mers cu trenul."),
        ],
        common_mistakes=[
            GrammarMistake("Ele au venite.", "Ele au venit.", "Participiul rămâne neschimbat.")
        ],
        related=["ro-perfect-questions-a2", "ro-past-time-a2"],
    ),
    GrammarTopic(
        "ro-perfect-questions-a2",
        "Ai plecat? Nu am plecat.",
        "A2",
        "Trecut",
        "Punem întrebări și negăm evenimente trecute.",
        "Într-o întrebare păstrăm auxiliarul și participiul: Ai cumpărat biletul? "
        "Putem adăuga un cuvânt interogativ: Când ai plecat? Cu cine ai venit?\n\n"
        "La negație, cuvântul «nu» se pune înaintea auxiliarului: Nu am plecat. Formele "
        "n-am, n-ai, n-a, n-ați și n-au sunt contrageri corecte, scrise cu cratimă. "
        "În răspunsul scurt putem păstra numai auxiliarul: Da, am.",
        structure="Ai + participiu?; nu + auxiliar + participiu",
        rules=[
            "Nu mutăm participiul înaintea auxiliarului pentru a forma întrebarea obișnuită.",
            "N-am și nu am au același sens de bază.",
            "Un răspuns negativ poate fi: Nu, nu am cumpărat.",
        ],
        examples=[
            GrammarExample("Unde ați stat? Am stat la un hotel."),
            GrammarExample("Nu am luat autobuzul. Am venit pe jos."),
        ],
        common_mistakes=[
            GrammarMistake("Am nu plecat.", "Nu am plecat.", "Negația precedă auxiliarul.")
        ],
        related=["ro-perfect-a2"],
    ),
    GrammarTopic(
        "ro-past-time-a2",
        "Ieri, acum două zile, apoi",
        "A2",
        "Timp",
        "Localizăm și ordonăm evenimente trecute.",
        "Ieri indică ziua de dinainte de azi, iar alaltăieri ziua de dinainte de "
        "ieri. Acum două zile plasează un eveniment cu două zile înainte de momentul "
        "vorbirii; acum nu înseamnă aici prezent.\n\nMai întâi, apoi și la sfârșit "
        "ajută la ordonarea unei relatări. De două zile exprimă o durată începută "
        "în trecut și poate apărea cu prezentul: Sunt aici de două zile.",
        structure="acum + durată; săptămâna trecută; mai întâi → apoi → la sfârșit",
        rules=[
            "Acum două zile și de două zile nu exprimă aceeași relație temporală.",
            "Săptămâna trecută se referă la săptămâna anterioară celei curente.",
            "Apoi introduce un eveniment ulterior celui deja relatat.",
        ],
        examples=[
            GrammarExample("Am sosit acum două zile. Sunt aici de două zile."),
            GrammarExample("Mai întâi am cumpărat bilete, apoi am vizitat muzeul."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Sunt aici acum două zile.",
                "Sunt aici de două zile.",
                "Pentru șederea care continuă folosim de.",
            )
        ],
        related=["ro-perfect-a2", "ro-imperfect-a2"],
    ),
    GrammarTopic(
        "ro-reflexive-present-a2",
        "Mă trezesc și mă pregătesc",
        "A2",
        "Verbe reflexive",
        "Descriem activități personale cu pronume reflexive.",
        "Unele verbe se învață cu un pronume reflexiv: a se trezi, a se îmbrăca, "
        "a se odihni. La prezent folosim mă, te, se, ne, vă, se înaintea verbului: "
        "mă trezesc, te trezești, se trezește, ne trezim, vă treziți, se trezesc.\n\n"
        "Nu fiecare acțiune personală este reflexivă: spunem dorm, nu mă dorm. "
        "Negația precedă pronumele: Nu mă grăbesc.",
        structure="mă / te / se / ne / vă / se + verb",
        rules=[
            "Pronumele reflexiv și verbul se potrivesc cu aceeași persoană.",
            "Pronumele face parte din construcția învățată a verbului.",
            "Mă spăl și spăl mașina au construcții și sensuri diferite.",
        ],
        examples=[
            GrammarExample("Ne trezim la șapte și ne pregătim pentru curs."),
            GrammarExample("Ioana se odihnește după serviciu."),
        ],
        common_mistakes=[
            GrammarMistake("Eu se trezesc.", "Eu mă trezesc.", "Eu cere pronumele mă.")
        ],
        related=["ro-reflexive-perfect-a2"],
    ),
    GrammarTopic(
        "ro-reflexive-perfect-a2",
        "M-am trezit: reflexivul la trecut",
        "A2",
        "Verbe reflexive",
        "Povestim ce am făcut folosind verbe reflexive.",
        "La perfectul compus, pronumele reflexiv precedă auxiliarul: m-am trezit, "
        "te-ai trezit, s-a trezit, ne-am trezit, v-ați trezit, s-au trezit. "
        "Cratima leagă formele pronunțate împreună.\n\nNegația se pune înaintea "
        "grupului: Nu m-am grăbit. Într-o întrebare păstrăm același grup: "
        "La ce oră te-ai trezit? Participiul nu se acordă cu subiectul.",
        structure="m-am / te-ai / s-a / ne-am / v-ați / s-au + participiu",
        rules=[
            "Se devine s- înaintea auxiliarului a sau au.",
            "La voi folosim v-ați, nu vă ați.",
            "Nu omitem pronumele la un verb reflexiv folosit cu acest sens.",
        ],
        examples=[
            GrammarExample("M-am îmbrăcat repede."),
            GrammarExample("Fetele s-au odihnit după drum."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Eu s-am trezit la șapte.",
                "Eu m-am trezit la șapte.",
                "Pentru eu folosim m-am; s-a și s-au apar la persoana a treia.",
            )
        ],
        related=["ro-reflexive-present-a2", "ro-perfect-a2"],
    ),
    GrammarTopic(
        "ro-imperfect-a2",
        "Eram, aveam, mergeam: obiceiuri în trecut",
        "A2",
        "Trecut",
        "Descriem un cadru sau un obicei trecut.",
        "Imperfectul descrie frecvent un obicei sau o situație în desfășurare: "
        "În copilărie mergeam la bunici. A fi: eram, erai, era, eram, erați, erau. "
        "A avea: aveam, aveai, avea, aveam, aveați, aveau.\n\n"
        "Modele utile sunt lucram, lucrai, lucra, lucram, lucrați, lucrau și "
        "mergeam, mergeai, mergea, mergeam, mergeați, mergeau. Contrastăm un "
        "obicei cu un eveniment încheiat: Mergeam des acolo. Ieri am mers o dată.",
        structure="obicei / cadru: imperfect; eveniment încheiat: perfect compus",
        rules=[
            "Imperfectul nu este doar o altă formă pentru orice acțiune trecută.",
            "În relatări, imperfectul poate descrie vremea sau locul.",
            "Persoanele eu și noi au adesea aceeași formă.",
        ],
        examples=[
            GrammarExample("Când eram mic, locuiam la țară."),
            GrammarExample("Era frig. Am intrat într-o cafenea."),
        ],
        common_mistakes=[GrammarMistake("Ei era acasă.", "Ei erau acasă.", "Ei cere forma erau.")],
        related=["ro-perfect-a2", "ro-past-time-a2"],
    ),
    GrammarTopic(
        "ro-genitive-a2",
        "Ușa vecinului și camera Mariei",
        "A2",
        "Cazuri",
        "Indicăm apartenența prin genitiv.",
        "Genitivul identifică posesorul: ușa vecinului, camera vecinei, cheile "
        "vecinilor. Formele hotărâte frecvente sunt vecinul – vecinului, "
        "vecina – vecinei, vecinii – vecinilor.\n\nLa nume masculine folosim "
        "lui înaintea numelui: camera lui Andrei. La multe nume feminine "
        "folosim o terminație: camera Mariei, telefonul Anei. Unele nume "
        "feminine cer lui: camera lui Carmen. În conversația familiară se aude și "
        "camera lui Maria; pentru exprimarea standard îngrijită exersăm camera Mariei.",
        structure="obiect identificat + posesor la genitiv",
        rules=[
            "Lui poate preceda un nume propriu; nu îl adăugăm înainte de vecinului.",
            "Genitivul poate indica și relația cu un loc: ușa apartamentului.",
            "Învățăm forma feminină împreună cu substantivul: casă – casei.",
        ],
        examples=[
            GrammarExample("Ușa apartamentului este deschisă."),
            GrammarExample("Aceasta este bicicleta lui Radu, iar aceea este bicicleta Mariei."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Camera vecina.", "Camera vecinei.", "Posesorul cere aici genitivul vecinei."
            )
        ],
        related=["ro-dative-a2"],
    ),
    GrammarTopic(
        "ro-dative-a2",
        "Cui? Vecinului, vecinei, lui Andrei",
        "A2",
        "Cazuri",
        "Numim destinatarul unei acțiuni.",
        "Dativul răspunde la cui? și apare când dăm, trimitem sau spunem ceva "
        "unei persoane: Dau cheia vecinului. Formele substantivului sunt "
        "aceleași ca la genitiv, dar rolul este diferit: cheia vecinului arată "
        "posesorul, dau vecinului cheia arată destinatarul.\n\n"
        "Pentru o persoană încă neidentificată avem unui vecin, unei vecine, "
        "unor vecini. La nume proprii: Trimit un mesaj lui Andrei. Scriu Mariei.",
        structure="dau / trimit / spun + ceva + cui?",
        rules=[
            "Dativul numește destinatarul, nu obiectul trimis.",
            "Folosim unei vecine la feminin, nu unui vecină.",
            "În vorbirea obișnuită destinatarul este adesea reluat printr-un pronume scurt.",
        ],
        examples=[
            GrammarExample("Trimit un mesaj unei vecine."),
            GrammarExample("Dau cheia lui Andrei."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Dau cheia vecinul.", "Dau cheia vecinului.", "Destinatarul cere dativul."
            )
        ],
        related=["ro-genitive-a2", "ro-dative-clitics-a2"],
    ),
    GrammarTopic(
        "ro-dative-clitics-a2",
        "Îmi, îți, îi: cui îi spunem?",
        "A2",
        "Pronume",
        "Folosim pronume scurte pentru destinatar.",
        "La prezent folosim îmi, îți, îi, ne, vă, le: Îmi scrie. Îți dau cheia. "
        "Le trimit un mesaj. Pronumele apare înaintea verbului și poate "
        "relua un destinatar exprimat: Îi dau vecinei cheia.\n\n"
        "Îi poate însemna lui sau ei; contextul arată persoana. În expresiile "
        "îmi place și îmi plac, verbul se acordă cu lucrul apreciat: Îmi place "
        "camera. Îmi plac ferestrele.",
        structure="îmi / îți / îi / ne / vă / le + verb",
        rules=[
            "Îi se folosește pentru un destinatar, le pentru mai mulți.",
            "Negația precedă pronumele: Nu îți dau cheia.",
            "Îmi plac cărțile are verb la plural pentru cărțile.",
        ],
        examples=[
            GrammarExample("Îi trimit proprietarului un mesaj."),
            GrammarExample("Ne place apartamentul, dar nu ne plac scările."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Îmi place ferestrele.", "Îmi plac ferestrele.", "Ferestrele cere plural."
            )
        ],
        related=["ro-dative-a2", "ro-accusative-clitics-a2"],
    ),
    GrammarTopic(
        "ro-accusative-clitics-a2",
        "Îl caut, o citesc: pronume de obiect",
        "A2",
        "Pronume",
        "Evităm repetarea numelor de persoane sau de lucruri.",
        "Pronumele de acuzativ sunt mă, te, îl, o, ne, vă, îi, le. Pentru un obiect "
        "masculin sau neutru la singular folosim îl: formularul – îl completez. "
        "Pentru feminin folosim o: cererea – o completez.\n\nLa plural avem îi "
        "pentru masculin și le pentru feminin și neutru: medicii – îi cunosc; "
        "documentele – le aduc. Pronumele stă înaintea verbului la prezent.",
        structure="mă / te / îl / o / ne / vă / îi / le + verb",
        rules=[
            "Genul pronumelui urmează substantivul înlocuit, nu persoana care vorbește.",
            "Îi poate fi acuzativ plural sau dativ singular; verbul și contextul ajută.",
            "Negația precedă pronumele: Nu o găsesc.",
        ],
        examples=[
            GrammarExample("Unde este rețeta? O am aici."),
            GrammarExample("Documentele sunt gata. Le aduc mâine."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Cererea? Îl completez.", "Cererea? O completez.", "Cerere este feminin."
            )
        ],
        related=["ro-personal-pe-a2", "ro-perfect-clitics-a2"],
    ),
    GrammarTopic(
        "ro-personal-pe-a2",
        "Îl caut pe Andrei",
        "A2",
        "Cazuri",
        "Marcăm obiectul direct când este o persoană identificată.",
        "În construcții cu nume de persoane folosim pe și, de obicei, un pronume "
        "scurt care reia persoana: Îl caut pe Andrei. O aștept pe Maria. "
        "Același tipar este frecvent cu o persoană precis identificată: "
        "Îl aștept pe medic.\n\nNu punem pe înaintea tuturor obiectelor: "
        "Caut un formular. Pentru o profesie nespecificată putem spune "
        "Caut un medic, fără să desemnăm o persoană anume.",
        structure="îl / o / îi / le + verb + pe + persoană identificată",
        rules=[
            "Pe din Îl văd pe Andrei nu exprimă poziția deasupra unui lucru.",
            "Pronumele scurt și persoana numită se referă la același participant.",
            "Caut un medic și îl caut pe medic diferă prin identificarea persoanei.",
        ],
        examples=[
            GrammarExample("O sun pe Ana după consultație."),
            GrammarExample("Îi așteptăm pe colegi la intrare."),
        ],
        common_mistakes=[
            GrammarMistake("O caut Maria.", "O caut pe Maria.", "Numele persoanei cere pe aici.")
        ],
        related=["ro-accusative-clitics-a2"],
    ),
    GrammarTopic(
        "ro-perfect-clitics-a2",
        "L-am adus, am citit-o",
        "A2",
        "Pronume",
        "Folosim pronume de obiect la perfectul compus.",
        "Majoritatea pronumelor scurte stau înaintea auxiliarului și se leagă "
        "prin cratimă: m-a văzut, te-am sunat, l-am adus, ne-a chemat, v-am "
        "așteptat, i-am văzut, le-am trimis.\n\nO, pronumele feminin singular, "
        "stă după participiu: Am citit-o. Am adus-o. În l-am adus, l- poate "
        "înlocui documentul; în am adus-o, o poate înlocui rețeta.",
        structure="l-am + participiu; am + participiu + -o",
        rules=[
            "O are o poziție diferită de celelalte pronume în acest timp.",
            "Participiul nu se acordă cu obiectul: rețeta – am adus-o.",
            "Negația precedă grupul verbal: Nu am găsit-o.",
        ],
        examples=[
            GrammarExample("Buletinul? L-am lăsat acasă."),
            GrammarExample("Cererea? Am completat-o ieri."),
        ],
        common_mistakes=[
            GrammarMistake(
                "O am citit ieri.", "Am citit-o ieri.", "La perfectul compus o urmează participiul."
            )
        ],
        related=["ro-accusative-clitics-a2", "ro-perfect-a2"],
    ),
    GrammarTopic(
        "ro-comparison-a2",
        "Mai ieftin decât și la fel de bun",
        "A2",
        "Comparație",
        "Comparăm însușiri și alegem între opțiuni.",
        "Mai + adjectiv + decât exprimă o diferență: mai ieftin decât. "
        "La fel de + adjectiv + ca exprimă egalitatea: la fel de bun ca. "
        "Mai puțin + adjectiv exprimă un grad mai mic: mai puțin zgomotos.\n\n"
        "Pentru un element dintr-un grup folosim cel mai, cea mai, cei mai, "
        "cele mai: cea mai ieftină cameră. Adjectivul se acordă în continuare "
        "cu substantivul.",
        structure="mai + adjectiv + decât; la fel de + adjectiv + ca",
        rules=[
            "Cel mai își schimbă forma: cele mai ieftine bilete.",
            "Nu omitem de din la fel de bun.",
            "Comparația poate privi și o acțiune: ajung mai repede decât tine.",
        ],
        examples=[
            GrammarExample("Această geacă este mai ieftină decât aceea."),
            GrammarExample("Ambele modele sunt la fel de bune."),
        ],
        common_mistakes=[
            GrammarMistake("Cea mai ieftin geacă.", "Cea mai ieftină geacă.", "Geacă cere ieftină.")
        ],
        related=["ro-quantities-a2"],
    ),
    GrammarTopic(
        "ro-quantities-a2",
        "Cât, câți, câte și expresii de cantitate",
        "A2",
        "Cantitate",
        "Cerem cantități precise sau aproximative.",
        "Cât se folosește cu un masculin sau neutru singular, câtă cu un feminin "
        "singular, câți cu masculin plural, câte cu feminin sau neutru plural: "
        "cât zahăr, câtă apă, câți cartofi, câte mere.\n\n"
        "Multe măsuri se leagă de produs prin de: un kilogram de mere, o sticlă "
        "de apă. Spunem câteva mere, puțină sare, multă apă. Puțin și mult se "
        "acordă când determină un substantiv.",
        structure="cât / câtă / câți / câte + substantiv; măsură + de + produs",
        rules=[
            "La plural, un neutru folosește câte: câte kilograme.",
            "Câteva exprimă un număr mic, dar neprecizat.",
            "O jumătate de kilogram este o cantitate; jumătate din mere este o parte dintr-un grup.",
        ],
        examples=[
            GrammarExample("Câtă făină trebuie? O jumătate de kilogram."),
            GrammarExample("Cumpăr câțiva cartofi și câteva roșii."),
        ],
        common_mistakes=[
            GrammarMistake("O sticlă apă.", "O sticlă de apă.", "Măsura se leagă prin de.")
        ],
        related=["ro-comparison-a2"],
    ),
    GrammarTopic(
        "ro-negative-pronouns-a2",
        "Nimeni nu…, nu… nimic",
        "A2",
        "Negație",
        "Exprimăm absența persoanelor sau a lucrurilor.",
        "Nimeni înseamnă nicio persoană, iar nimic înseamnă niciun lucru. În "
        "propoziția obișnuită apar împreună cu nu: Nimeni nu răspunde. Nu "
        "cumpăr nimic. Într-un răspuns scurt fără verb putem spune doar Nimic.\n\n"
        "Înaintea unui substantiv folosim niciun sau nicio: Nu am niciun "
        "bon. Nu am nicio întrebare. Niciodată și nicăieri cer de asemenea "
        "negația verbului în aceste construcții.",
        structure="nimeni + nu + verb; nu + verb + nimic / niciun / nicio",
        rules=[
            "Cu nimeni folosim verb la singular.",
            "Niciun și nicio se scriu într-un singur cuvânt în aceste contexte.",
            "Prezența lui nimeni nu elimină negația nu.",
        ],
        examples=[
            GrammarExample("Nu am găsit nimic potrivit."),
            GrammarExample("Nimeni nu este la casă."),
        ],
        common_mistakes=[
            GrammarMistake("Nimeni răspunde.", "Nimeni nu răspunde.", "Verbul trebuie negat.")
        ],
        related=["ro-perfect-questions-a2"],
    ),
    GrammarTopic(
        "ro-subjunctive-a2",
        "Să fiu, să am, să vin",
        "A2",
        "Moduri verbale",
        "Exprimăm scopuri și acțiuni dorite prin conjunctiv.",
        "După vreau, trebuie și pot folosim des conjunctivul: Vreau să vin. "
        "Conjunctivul poate exprima și scopul: Vin să discutăm. "
        "La multe verbe, persoana a treia diferă "
        "de indicativ: vine – să vină, face – să facă, citește – să citească.\n\n"
        "A fi are formele să fiu, să fii, să fie, să fim, să fiți, să fie. A avea "
        "are să am, să ai, să aibă, să avem, să aveți, să aibă. Subiectul poate "
        "fi diferit de cel al primului verb: Vreau să vii tu.",
        structure="să + verb acordat cu persoana care face acțiunea",
        rules=[
            "La persoana a treia singular și plural formele sunt identice: să vină.",
            "Negația «nu» vine după «să»: Vreau să nu întârzii.",
            "Să fii are doi i la persoana a doua singular.",
        ],
        examples=[
            GrammarExample("Trebuie să fim la birou la nouă."),
            GrammarExample("Ana vrea să aibă mai mult timp liber."),
        ],
        common_mistakes=[
            GrammarMistake("Vreau să ești aici.", "Vreau să fii aici.", "După să folosim fii.")
        ],
        related=["ro-future-a2", "ro-polite-conditional-a2"],
    ),
    GrammarTopic(
        "ro-future-a2",
        "O să plec și voi pleca",
        "A2",
        "Viitor",
        "Vorbim despre planuri și evenimente viitoare.",
        "În conversație folosim des o să + conjunctiv: o să plec, o să pleci, "
        "o să plece, o să plecăm, o să plecați, o să plece. O nu se schimbă "
        "după persoană.\n\nUn alt viitor standard este voi, vei, va, vom, veți, "
        "vor + infinitiv fără a: voi pleca, vom veni. Acesta apare și în "
        "anunțuri. Mâine plec este de asemenea posibil când contextul "
        "arată clar viitorul.",
        structure="o să + conjunctiv; voi / vei / va / vom / veți / vor + infinitiv fără a",
        rules=[
            "O să plecăm este corect și pentru noi; o nu devine vom în același tipar.",
            "După voi folosim pleca, nu plec.",
            "Negația este nu o să plec sau nu voi pleca.",
        ],
        examples=[
            GrammarExample("Mâine o să lucrăm de acasă."),
            GrammarExample("Cursul va începe la ora zece."),
        ],
        common_mistakes=[
            GrammarMistake("Vom să venim.", "O să venim.", "Nu amestecăm cele două tipare.")
        ],
        related=["ro-subjunctive-a2"],
    ),
    GrammarTopic(
        "ro-polite-conditional-a2",
        "Aș dori și ați putea: cereri politicoase",
        "A2",
        "Politețe",
        "Formulăm o dorință sau o cerere fără un ton direct.",
        "Condiționalul prezent are formele aș, ai, ar, am, ați, ar + infinitiv "
        "fără a: aș dori, ai putea, ar vrea. În servicii folosim frecvent "
        "Aș dori o rezervare și Ați putea să mă ajutați?\n\n"
        "Aș vrea să plec exprimă o dorință; nu confirmă singur o rezervare sau "
        "un plan stabilit. La acest nivel exersăm cereri și preferințe, nu "
        "întregul sistem al ipotezelor.",
        structure="aș dori + substantiv; ați putea + să + verb?",
        rules=[
            "Aș se referă la eu, ați la voi sau dumneavoastră.",
            "După auxiliar folosim infinitivul fără a: aș vrea, nu aș vreau.",
            "Vă rog poate însoți cererea politicoasă.",
        ],
        examples=[
            GrammarExample("Aș dori două bilete pentru vineri."),
            GrammarExample("Ați putea să repetați adresa, vă rog?"),
        ],
        common_mistakes=[
            GrammarMistake("Eu ar dori un loc.", "Eu aș dori un loc.", "Eu cere auxiliarul aș.")
        ],
        related=["ro-subjunctive-a2"],
    ),
    GrammarTopic(
        "ro-imperative-a2",
        "Ascultă! Nu pleca! Intrați!",
        "A2",
        "Instrucțiuni",
        "Dăm instrucțiuni și formulăm interdicții simple.",
        "Imperativul afirmativ singular se învață cu verbul: ascultă, citește, "
        "mergi. Câteva forme sunt neregulate: vino, fă, du, fii. La plural "
        "și la adresarea politicoasă folosim forme ca ascultați, citiți, veniți.\n\n"
        "La singular negativ folosim nu + infinitiv fără a: Nu pleca! Nu face! "
        "Nu fi supărat! La plural: Nu plecați! Pronumele se atașează la afirmativ "
        "și precedă verbul la negativ: Citește-o! Nu o citi!",
        structure="tu: vino / nu veni; dumneavoastră: veniți / nu veniți",
        rules=[
            "Vă rog sau te rog face instrucțiunea mai politicoasă.",
            "Fii atent are doi i, iar nu fi neatent are un singur i în forma verbală.",
            "Imperativul poate avea un ton prea direct fără context sau formulă de politețe.",
        ],
        examples=[
            GrammarExample("Completați formularul și semnați aici, vă rog."),
            GrammarExample("Ia harta! Nu o uita acasă!"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Nu fă zgomot!",
                "Nu face zgomot!",
                "În româna standard, imperativul negativ singular cere face; fă este afirmativ.",
            )
        ],
        related=["ro-subjunctive-a2", "ro-accusative-clitics-a2"],
    ),
    GrammarTopic(
        "ro-relative-care-a2",
        "Autobuzul care pleacă și cartea pe care o citesc",
        "A2",
        "Propoziții",
        "Identificăm un lucru sau o persoană printr-o informație suplimentară.",
        "Care poate fi subiectul unei propoziții: Autobuzul care pleacă la "
        "opt merge la Sibiu. Verbul se acordă cu lucrul descris: autobuzele "
        "care pleacă.\n\nCând care este obiect direct, folosim pe care și "
        "un pronume scurt: cartea pe care o citesc, muzeul pe care îl vizităm. "
        "Acest pe apare și pentru lucruri, nu numai pentru persoane.",
        structure="subiect: care + verb; obiect: pe care + pronume scurt + verb",
        rules=[
            "Care singur nu înlocuiește pe care când este obiect direct în acest tipar standard.",
            "Pronumele scurt se acordă cu substantivul: cartea – o; muzeul – îl.",
            "Care are aceeași formă pentru masculin, feminin, singular și plural în aceste exemple.",
        ],
        examples=[
            GrammarExample("Caut autobuzul care merge la centru."),
            GrammarExample("Acesta este traseul pe care îl alegem."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Cartea care o citesc.", "Cartea pe care o citesc.", "Obiectul direct cere pe care."
            )
        ],
        related=["ro-personal-pe-a2", "ro-accusative-clitics-a2"],
    ),
    GrammarTopic(
        "ro-connectors-a2",
        "Pentru că, când, după ce, dacă",
        "A2",
        "Propoziții",
        "Explicăm motive, condiții simple și ordinea activităților.",
        "Pentru că și fiindcă introduc un motiv: Rămân acasă pentru că plouă. "
        "Când leagă o acțiune de un moment: Când ajung, te sun. După ce arată "
        "că o acțiune o urmează pe alta: După ce termin, plec.\n\n"
        "Înainte să introduce o acțiune ulterioară față de cea principală: "
        "Cumpăr apă înainte să plec. Folosim deci pentru o concluzie simplă: "
        "Este închis, deci revenim mâine. Dacă introduce o condiție posibilă: "
        "Dacă plouă, rămânem acasă. Aici folosim prezentul pentru o situație reală "
        "sau posibilă, fără forme ipotetice complexe.",
        structure="motiv: pentru că; moment: când; ordine: după ce / înainte să; condiție: dacă",
        rules=[
            "După ce și înainte să nu au aceeași ordine a evenimentelor.",
            "Pentru că introduce motivul, deci introduce consecința.",
            "După când putem folosi prezentul pentru un plan viitor.",
        ],
        examples=[
            GrammarExample("Luăm umbrela pentru că plouă."),
            GrammarExample("După ce cumpărăm biletele, intrăm în muzeu."),
            GrammarExample("Dacă ajungem devreme, lăsăm bagajele la recepție."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Plec înainte să termină ploaia.",
                "Plec înainte să se termine ploaia.",
                "A se termina este reflexiv și cere conjunctiv după să.",
            )
        ],
        related=["ro-subjunctive-a2", "ro-past-time-a2"],
    ),
]
