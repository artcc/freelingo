"""Romanian A2 vocabulary: seven sets of twenty-six distinct entries."""

from app.data._types import VocabularyEntry, VocabularySet

A2_SETS: list[VocabularySet] = [
    VocabularySet(
        "ro_travel_a2",
        "A2",
        "Călătorii și cazare",
        "a2-unit-1",
        [
            VocabularyEntry(
                "călătorie",
                "noun",
                "Deplasare într-un alt loc, adesea pentru mai multe zile.",
                "Călătoria a durat trei zile.",
            ),
            VocabularyEntry(
                "vacanță",
                "noun",
                "Perioadă de odihnă fără cursuri sau serviciu.",
                "Am petrecut vacanța la mare.",
            ),
            VocabularyEntry(
                "bagaj",
                "noun",
                "Lucruri transportate în timpul unei călătorii.",
                "Am avut un singur bagaj.",
            ),
            VocabularyEntry(
                "valiză",
                "noun",
                "Geantă mare pentru haine și alte obiecte.",
                "Am pus hainele în valiză.",
            ),
            VocabularyEntry("rucsac", "noun", "Geantă purtată pe spate.", "Am luat un rucsac mic."),
            VocabularyEntry(
                "peron", "noun", "Spațiu din gară de unde urcăm în tren.", "Am așteptat pe peron."
            ),
            VocabularyEntry(
                "vagon",
                "noun",
                "Parte a unui tren, pentru călători sau mărfuri.",
                "Am călătorit în primul vagon.",
            ),
            VocabularyEntry(
                "loc",
                "noun",
                "Spațiu rezervat unei persoane într-un vehicul sau într-o sală.",
                "Am cumpărat un bilet cu loc.",
            ),
            VocabularyEntry(
                "dus-întors",
                "adjective",
                "Pentru călătoria la destinație și revenirea la locul de plecare.",
                "Am cumpărat un bilet dus-întors.",
            ),
            VocabularyEntry(
                "întârziere",
                "noun",
                "Sosire sau plecare după ora stabilită.",
                "Trenul a avut o întârziere de zece minute.",
            ),
            VocabularyEntry(
                "plecare",
                "noun",
                "Momentul în care începe deplasarea dintr-un loc.",
                "Plecarea a fost la șapte.",
            ),
            VocabularyEntry(
                "sosire", "noun", "Momentul ajungerii la destinație.", "Sosirea a fost la prânz."
            ),
            VocabularyEntry(
                "destinație",
                "noun",
                "Locul spre care călătorim.",
                "Destinația noastră a fost Oradea.",
            ),
            VocabularyEntry(
                "rezervare",
                "noun",
                "Păstrarea unui loc sau a unei camere pentru cineva.",
                "Am făcut o rezervare pentru două nopți.",
            ),
            VocabularyEntry(
                "recepție",
                "noun",
                "Loc din hotel unde sunt primiți oaspeții.",
                "Am lăsat cheia la recepție.",
            ),
            VocabularyEntry(
                "pensiune",
                "noun",
                "Unitate de cazare, de obicei mai mică decât un hotel.",
                "Am stat la o pensiune.",
            ),
            VocabularyEntry(
                "cazare",
                "noun",
                "Asigurarea unui loc pentru dormit în timpul unei călătorii.",
                "Cazarea a costat două sute de lei.",
            ),
            VocabularyEntry(
                "mic dejun", "phrase", "Prima masă a zilei.", "Am luat micul dejun la opt."
            ),
            VocabularyEntry(
                "prosop",
                "noun",
                "Bucată de material pentru ștergerea corpului.",
                "Am cerut un prosop curat.",
            ),
            VocabularyEntry(
                "vedere",
                "noun",
                "Peisaj care poate fi văzut dintr-un loc.",
                "Camera a avut vedere spre munte.",
            ),
            VocabularyEntry(
                "a rezerva",
                "verb",
                "A cere păstrarea unui loc pentru o anumită dată.",
                "Am rezervat o cameră.",
            ),
            VocabularyEntry("a sosi", "verb", "A ajunge la destinație.", "Am sosit seara."),
            VocabularyEntry("a pleca", "verb", "A părăsi un loc.", "Am plecat din Iași ieri."),
            VocabularyEntry(
                "a vizita",
                "verb",
                "A merge să vezi un loc sau o persoană.",
                "Am vizitat cetatea din Alba Iulia.",
            ),
            VocabularyEntry(
                "ieri", "adverb", "În ziua dinainte de astăzi.", "Ieri am ajuns acasă."
            ),
            VocabularyEntry(
                "alaltăieri",
                "adverb",
                "În ziua de dinainte de ieri.",
                "Alaltăieri am cumpărat biletele.",
            ),
        ],
    ),
    VocabularySet(
        "ro_routines_memories_a2",
        "A2",
        "Rutine și amintiri",
        "a2-unit-2",
        [
            VocabularyEntry(
                "a se trezi", "verb", "A ieși din starea de somn.", "M-am trezit la șase."
            ),
            VocabularyEntry(
                "a se ridica",
                "verb",
                "A trece într-o poziție mai înaltă sau în picioare.",
                "M-am ridicat din pat.",
            ),
            VocabularyEntry(
                "a se spăla",
                "verb",
                "A curăța propriul corp cu apă.",
                "Mă spăl pe mâini înainte de masă.",
            ),
            VocabularyEntry(
                "a se îmbrăca", "verb", "A pune haine pe corp.", "M-am îmbrăcat repede."
            ),
            VocabularyEntry(
                "a se pregăti",
                "verb",
                "A face lucrurile necesare înaintea unei activități.",
                "Ne pregătim pentru plecare.",
            ),
            VocabularyEntry(
                "a se grăbi", "verb", "A acționa repede pentru a ajunge la timp.", "Nu m-am grăbit."
            ),
            VocabularyEntry(
                "a se odihni",
                "verb",
                "A întrerupe efortul pentru a recăpăta energie.",
                "M-am odihnit după drum.",
            ),
            VocabularyEntry(
                "a se culca", "verb", "A merge în pat pentru somn.", "M-am culcat devreme."
            ),
            VocabularyEntry(
                "a se plimba",
                "verb",
                "A merge fără grabă pentru relaxare.",
                "Ne plimbam în fiecare seară.",
            ),
            VocabularyEntry(
                "a se întâlni",
                "verb",
                "A ajunge în același loc cu altă persoană.",
                "M-am întâlnit cu Ana.",
            ),
            VocabularyEntry(
                "copilărie",
                "noun",
                "Perioada vieții în care suntem copii.",
                "În copilărie locuiam la țară.",
            ),
            VocabularyEntry(
                "amintire",
                "noun",
                "Imagine sau întâmplare păstrată în minte.",
                "Am o amintire frumoasă din școală.",
            ),
            VocabularyEntry(
                "obicei",
                "noun",
                "Acțiune repetată în mod regulat.",
                "Plimbarea de seară era un obicei.",
            ),
            VocabularyEntry(
                "sat",
                "noun",
                "Localitate rurală mai mică decât un oraș.",
                "Bunicii locuiau într-un sat.",
            ),
            VocabularyEntry(
                "curte", "noun", "Spațiu deschis din jurul unei case.", "Ne jucam în curte."
            ),
            VocabularyEntry(
                "grădină",
                "noun",
                "Teren unde cresc flori, legume sau pomi.",
                "Bunica lucra în grădină.",
            ),
            VocabularyEntry(
                "vecin",
                "noun",
                "Persoană care locuiește aproape de casa noastră.",
                "Vecinul era un prieten al bunicului.",
            ),
            VocabularyEntry(
                "coleg",
                "noun",
                "Persoană cu care învățăm sau lucrăm.",
                "Colegul meu venea cu bicicleta.",
            ),
            VocabularyEntry(
                "uniformă",
                "noun",
                "Haine de același model purtate de membrii unui grup.",
                "La școală purtam uniformă.",
            ),
            VocabularyEntry(
                "jucărie",
                "noun",
                "Obiect folosit de copii pentru joacă.",
                "Aveam multe jucării din lemn.",
            ),
            VocabularyEntry(
                "poveste",
                "noun",
                "Relatare a unor întâmplări reale sau imaginare.",
                "Bunicul spunea povești seara.",
            ),
            VocabularyEntry(
                "devreme",
                "adverb",
                "Înaintea orei obișnuite sau la începutul zilei.",
                "M-am trezit devreme.",
            ),
            VocabularyEntry(
                "târziu",
                "adverb",
                "După ora obișnuită sau spre sfârșitul zilei.",
                "M-am culcat târziu.",
            ),
            VocabularyEntry(
                "atunci", "adverb", "În momentul despre care se vorbește.", "Atunci aveam zece ani."
            ),
            VocabularyEntry(
                "des", "adverb", "De multe ori într-o perioadă.", "Mergeam des la bunici."
            ),
            VocabularyEntry(
                "rar", "adverb", "De puține ori într-o perioadă.", "Călătoream rar cu trenul."
            ),
        ],
    ),
    VocabularySet(
        "ro_housing_neighbours_a2",
        "A2",
        "Locuință și vecinătate",
        "a2-unit-3",
        [
            VocabularyEntry(
                "proprietar",
                "noun",
                "Persoană căreia îi aparține un bun.",
                "Îi scriu proprietarului apartamentului.",
            ),
            VocabularyEntry(
                "chiriaș",
                "noun",
                "Persoană care plătește pentru a folosi o locuință.",
                "Chiriașul îi dă cheia proprietarului.",
            ),
            VocabularyEntry(
                "chirie",
                "noun",
                "Sumă plătită periodic pentru folosirea unei locuințe.",
                "Chiria apartamentului este mare.",
            ),
            VocabularyEntry(
                "contract",
                "noun",
                "Acord scris care stabilește drepturi și obligații.",
                "Contractul chiriașului este pe masă.",
            ),
            VocabularyEntry(
                "factură",
                "noun",
                "Document care arată suma de plătit pentru produse sau servicii.",
                "Factura de curent a venit ieri.",
            ),
            VocabularyEntry(
                "întreținere",
                "noun",
                "Cheltuieli comune pentru funcționarea unui bloc.",
                "Plătesc întreținerea în fiecare lună.",
            ),
            VocabularyEntry(
                "bloc",
                "noun",
                "Clădire cu mai multe apartamente.",
                "Intrarea blocului este curată.",
            ),
            VocabularyEntry(
                "etaj",
                "noun",
                "Nivel al unei clădiri deasupra parterului.",
                "Locuiesc la etajul doi.",
            ),
            VocabularyEntry(
                "parter",
                "noun",
                "Nivelul unei clădiri aflat la sol.",
                "Apartamentul vecinei este la parter.",
            ),
            VocabularyEntry(
                "lift",
                "noun",
                "Cabină care transportă persoane între etajele unei clădiri.",
                "Liftul blocului nu funcționează.",
            ),
            VocabularyEntry(
                "scară",
                "noun",
                "Construcție cu trepte pentru urcare și coborâre.",
                "Scara blocului este îngustă.",
            ),
            VocabularyEntry(
                "balcon",
                "noun",
                "Spațiu exterior al unui apartament, cu balustradă.",
                "Ușa balconului este închisă.",
            ),
            VocabularyEntry(
                "acoperiș",
                "noun",
                "Partea de sus care protejează o clădire.",
                "Acoperișul casei este nou.",
            ),
            VocabularyEntry(
                "perete",
                "noun",
                "Parte verticală care separă sau închide camere.",
                "Culoarea peretelui este albă.",
            ),
            VocabularyEntry(
                "podea",
                "noun",
                "Suprafață pe care călcăm într-o încăpere.",
                "Podeaua camerei este din lemn.",
            ),
            VocabularyEntry(
                "robinet",
                "noun",
                "Dispozitiv cu care deschidem sau închidem apa.",
                "Robinetul băii curge.",
            ),
            VocabularyEntry(
                "chiuvetă",
                "noun",
                "Vas fix în care spălăm mâinile sau vasele.",
                "Chiuveta bucătăriei este nouă.",
            ),
            VocabularyEntry(
                "calorifer",
                "noun",
                "Aparat prin care se încălzește o cameră.",
                "Caloriferul camerei este rece.",
            ),
            VocabularyEntry(
                "priză",
                "noun",
                "Punct de conectare a aparatelor la curent.",
                "Priza din bucătărie nu funcționează.",
            ),
            VocabularyEntry(
                "bec",
                "noun",
                "Obiect care produce lumină cu ajutorul curentului.",
                "Becul din hol este ars.",
            ),
            VocabularyEntry(
                "reparație",
                "noun",
                "Lucrare prin care un obiect este făcut din nou funcțional.",
                "Proprietarul plătește reparația.",
            ),
            VocabularyEntry(
                "zgomot",
                "noun",
                "Sunet puternic sau deranjant.",
                "Zgomotul vecinilor mă deranjează.",
            ),
            VocabularyEntry(
                "liniște", "noun", "Lipsa zgomotului.", "Îmi place liniștea cartierului."
            ),
            VocabularyEntry(
                "a împrumuta",
                "verb",
                "A da sau a primi ceva pentru folosire temporară.",
                "Îi împrumut vecinei o scară.",
            ),
            VocabularyEntry(
                "a trimite",
                "verb",
                "A face ca un obiect sau un mesaj să ajungă la cineva.",
                "Îi trimit proprietarului o fotografie.",
            ),
            VocabularyEntry(
                "a repara",
                "verb",
                "A face un obiect defect să funcționeze din nou.",
                "Un instalator repară robinetul.",
            ),
        ],
    ),
    VocabularySet(
        "ro_services_health_a2",
        "A2",
        "Documente, servicii și sănătate",
        "a2-unit-4",
        [
            VocabularyEntry(
                "ghișeu",
                "noun",
                "Loc unde un angajat primește cereri și documente.",
                "Caut ghișeul pentru informații.",
            ),
            VocabularyEntry(
                "formular",
                "noun",
                "Document cu spații pentru completarea datelor.",
                "Formularul? Îl completez acum.",
            ),
            VocabularyEntry(
                "cerere", "noun", "Document prin care solicităm ceva.", "Cererea? Am depus-o ieri."
            ),
            VocabularyEntry(
                "semnătură",
                "noun",
                "Nume scris într-o formă personală pentru confirmare.",
                "Semnătura este la sfârșitul cererii.",
            ),
            VocabularyEntry(
                "buletin",
                "noun",
                "Denumire uzuală pentru actul de identitate.",
                "Buletinul? L-am adus.",
            ),
            VocabularyEntry(
                "pașaport",
                "noun",
                "Document de identitate folosit în călătorii internaționale.",
                "Pașaportul îl țin în geantă.",
            ),
            VocabularyEntry(
                "copie", "noun", "Reproducere a unui document.", "Copia am lăsat-o la ghișeu."
            ),
            VocabularyEntry(
                "original",
                "noun",
                "Documentul inițial, nu reproducerea lui.",
                "Originalul îl păstrez.",
            ),
            VocabularyEntry(
                "programare",
                "noun",
                "Oră și dată stabilite pentru o consultație sau un serviciu.",
                "Am o programare la medic.",
            ),
            VocabularyEntry(
                "coadă",
                "noun",
                "Șir de persoane care așteaptă să fie servite.",
                "Am stat la coadă zece minute.",
            ),
            VocabularyEntry(
                "funcționar",
                "noun",
                "Angajat care lucrează cu acte și solicitări.",
                "Îl întreb pe funcționar despre cerere.",
            ),
            VocabularyEntry(
                "cabinet",
                "noun",
                "Încăpere în care un specialist primește clienți sau pacienți.",
                "Cabinetul îl găsiți la etaj.",
            ),
            VocabularyEntry(
                "consultație",
                "noun",
                "Întâlnire în care medicul examinează un pacient.",
                "Consultația am plătit-o la recepție.",
            ),
            VocabularyEntry(
                "rețetă",
                "noun",
                "Document medical care indică medicamentele recomandate.",
                "Rețeta am primit-o ieri.",
            ),
            VocabularyEntry(
                "tratament",
                "noun",
                "Măsuri și medicamente folosite pentru vindecare.",
                "Tratamentul îl urmez acasă.",
            ),
            VocabularyEntry(
                "pastilă",
                "noun",
                "Medicament solid de dimensiune mică.",
                "Pastila am luat-o după masă.",
            ),
            VocabularyEntry(
                "sirop", "noun", "Medicament lichid, adesea dulce.", "Siropul îl iau seara."
            ),
            VocabularyEntry(
                "tuse",
                "noun",
                "Eliminare bruscă și zgomotoasă a aerului din plămâni.",
                "Am o tuse de două zile.",
            ),
            VocabularyEntry(
                "alergie",
                "noun",
                "Reacție exagerată a organismului la o substanță de obicei inofensivă.",
                "Am o alergie la acest medicament.",
            ),
            VocabularyEntry(
                "amețeală",
                "noun",
                "Senzație că lucrurile se învârt sau că pierdem echilibrul.",
                "Am o stare de amețeală.",
            ),
            VocabularyEntry(
                "asigurare",
                "noun",
                "Contract care acoperă anumite riscuri și cheltuieli.",
                "Asigurarea medicală o am aici.",
            ),
            VocabularyEntry(
                "urgență", "noun", "Situație care cere ajutor imediat.", "Este o urgență medicală."
            ),
            VocabularyEntry(
                "a completa",
                "verb",
                "A scrie informațiile cerute în spațiile unui document.",
                "Îl completez cu litere mari.",
            ),
            VocabularyEntry(
                "a semna",
                "verb",
                "A pune propria semnătură pe un document.",
                "Am semnat cererea și am depus-o.",
            ),
            VocabularyEntry(
                "a depune",
                "verb",
                "A preda oficial un document sau o sumă.",
                "Am depus actele la ghișeu.",
            ),
            VocabularyEntry(
                "a verifica",
                "verb",
                "A controla dacă ceva este corect.",
                "Funcționarul verifică pașaportul.",
            ),
        ],
    ),
    VocabularySet(
        "ro_shopping_choices_a2",
        "A2",
        "Produse, cantități și alegeri",
        "a2-unit-5",
        [
            VocabularyEntry(
                "reducere",
                "noun",
                "Scădere a prețului inițial.",
                "Geaca este mai ieftină după reducere.",
            ),
            VocabularyEntry(
                "ofertă",
                "noun",
                "Propunere de vânzare cu anumite condiții.",
                "Această ofertă este mai bună.",
            ),
            VocabularyEntry(
                "bon", "noun", "Dovadă tipărită a unei cumpărături.", "Nu am găsit niciun bon."
            ),
            VocabularyEntry(
                "rest",
                "noun",
                "Bani primiți înapoi când plătim mai mult decât prețul.",
                "Am primit cinci lei rest.",
            ),
            VocabularyEntry(
                "numerar", "noun", "Bani sub formă de bancnote și monede.", "Plătesc în numerar."
            ),
            VocabularyEntry(
                "card",
                "noun",
                "Instrument electronic folosit pentru plată.",
                "Pot plăti cu cardul?",
            ),
            VocabularyEntry(
                "mărime",
                "noun",
                "Dimensiune standard a hainelor sau încălțămintei.",
                "Aveți o mărime mai mică?",
            ),
            VocabularyEntry(
                "probă",
                "noun",
                "Încercare a unui produs înainte de alegere.",
                "Cabina de probă este liberă.",
            ),
            VocabularyEntry(
                "geacă",
                "noun",
                "Haină scurtă purtată peste alte haine.",
                "Geaca albastră este mai groasă.",
            ),
            VocabularyEntry(
                "cămașă",
                "noun",
                "Haină cu mâneci și nasturi pentru partea de sus a corpului.",
                "Cămașa albă este la fel de scumpă.",
            ),
            VocabularyEntry(
                "pantaloni",
                "noun",
                "Haină care acoperă separat fiecare picior.",
                "Acești pantaloni sunt prea lungi.",
            ),
            VocabularyEntry(
                "pantof",
                "noun",
                "Încălțăminte care acoperă piciorul până sub gleznă.",
                "Pantofii negri sunt mai comozi.",
            ),
            VocabularyEntry(
                "comod",
                "adjective",
                "Care oferă confort la folosire.",
                "Acești pantofi sunt comozi.",
            ),
            VocabularyEntry(
                "strâmt", "adjective", "Care lasă prea puțin spațiu.", "Cămașa este prea strâmtă."
            ),
            VocabularyEntry(
                "ieftin", "adjective", "Cu un preț mic.", "Acesta este cel mai ieftin model."
            ),
            VocabularyEntry(
                "scump", "adjective", "Cu un preț mare.", "Modelul nou este mai scump."
            ),
            VocabularyEntry(
                "potrivit",
                "adjective",
                "Care corespunde unei nevoi sau unei situații.",
                "Nu am găsit nimic potrivit.",
            ),
            VocabularyEntry(
                "kilogram",
                "noun",
                "Unitate de măsură a masei egală cu o mie de grame.",
                "Cumpăr un kilogram de mere.",
            ),
            VocabularyEntry(
                "gram",
                "noun",
                "A mia parte dintr-un kilogram.",
                "Vreau două sute de grame de brânză.",
            ),
            VocabularyEntry(
                "litru",
                "noun",
                "Unitate de măsură pentru volumul lichidelor.",
                "Cumpăr doi litri de lapte.",
            ),
            VocabularyEntry(
                "sticlă", "noun", "Recipient pentru păstrarea lichidelor.", "Vreau o sticlă de apă."
            ),
            VocabularyEntry(
                "pungă",
                "noun",
                "Ambalaj ușor pentru transportul produselor.",
                "Pun legumele într-o pungă.",
            ),
            VocabularyEntry(
                "făină",
                "noun",
                "Pulbere obținută din cereale măcinate.",
                "Am nevoie de puțină făină.",
            ),
            VocabularyEntry(
                "ulei", "noun", "Grăsime lichidă folosită la gătit.", "Pun puțin ulei în tigaie."
            ),
            VocabularyEntry(
                "a cântări", "verb", "A măsura masa unui produs.", "Vânzătorul cântărește merele."
            ),
            VocabularyEntry(
                "a schimba",
                "verb",
                "A înlocui ceva cu altceva.",
                "Vreau să schimb cămașa cu una mai mare.",
            ),
        ],
    ),
    VocabularySet(
        "ro_work_plans_a2",
        "A2",
        "Muncă, învățare și planuri",
        "a2-unit-6",
        [
            VocabularyEntry(
                "angajat",
                "noun",
                "Persoană care lucrează pentru un salariu.",
                "Noul angajat o să înceapă luni.",
            ),
            VocabularyEntry(
                "șef",
                "noun",
                "Persoană care conduce o echipă sau o activitate.",
                "Aș dori să vorbesc cu șeful.",
            ),
            VocabularyEntry(
                "echipă",
                "noun",
                "Grup de persoane care lucrează împreună.",
                "O să lucrăm în aceeași echipă.",
            ),
            VocabularyEntry(
                "ședință",
                "noun",
                "Întâlnire de lucru pentru discutarea unor subiecte.",
                "Ședința va începe la zece.",
            ),
            VocabularyEntry(
                "program",
                "noun",
                "Orele și activitățile stabilite pentru o perioadă.",
                "Aș dori un program mai flexibil.",
            ),
            VocabularyEntry(
                "salariu",
                "noun",
                "Bani primiți pentru munca efectuată.",
                "Salariul va fi plătit vineri.",
            ),
            VocabularyEntry(
                "concediu",
                "noun",
                "Perioadă aprobată în care un angajat nu lucrează.",
                "O să am concediu în august.",
            ),
            VocabularyEntry(
                "sarcină",
                "noun",
                "Lucru concret pe care cineva trebuie să îl facă.",
                "Trebuie să termin această sarcină.",
            ),
            VocabularyEntry(
                "termen", "noun", "Dată până la care trebuie făcut ceva.", "Termenul este vineri."
            ),
            VocabularyEntry(
                "proiect",
                "noun",
                "Activitate organizată pentru obținerea unui rezultat.",
                "O să începem un proiect nou.",
            ),
            VocabularyEntry(
                "interviu",
                "noun",
                "Discuție în care sunt evaluate experiența și aptitudinile unei persoane.",
                "Mâine o să am un interviu.",
            ),
            VocabularyEntry(
                "experiență",
                "noun",
                "Cunoștințe dobândite prin activități făcute anterior.",
                "Am experiență în vânzări.",
            ),
            VocabularyEntry(
                "examen",
                "noun",
                "Probă prin care sunt evaluate cunoștințele.",
                "Examenul va fi luni.",
            ),
            VocabularyEntry(
                "înscriere",
                "noun",
                "Înregistrare oficială pentru participarea la o activitate.",
                "Aș dori informații despre înscriere.",
            ),
            VocabularyEntry(
                "atelier",
                "noun",
                "Activitate practică de învățare în grup.",
                "O să particip la un atelier de fotografie.",
            ),
            VocabularyEntry(
                "invitație",
                "noun",
                "Propunere de participare la un eveniment.",
                "Mulțumesc pentru invitație.",
            ),
            VocabularyEntry(
                "petrecere",
                "noun",
                "Întâlnire pentru sărbătoare și distracție.",
                "Petrecerea va fi sâmbătă.",
            ),
            VocabularyEntry(
                "aniversare",
                "noun",
                "Sărbătorirea unui eveniment la aceeași dată în alt an.",
                "O să merg la aniversarea Anei.",
            ),
            VocabularyEntry(
                "cadou",
                "noun",
                "Obiect oferit cuiva fără plată, ca semn de atenție.",
                "Aș vrea să cumpăr un cadou.",
            ),
            VocabularyEntry(
                "plan",
                "noun",
                "Idee organizată despre ce urmează să facem.",
                "Avem un plan pentru weekend.",
            ),
            VocabularyEntry(
                "a propune",
                "verb",
                "A prezenta o idee pentru a fi discutată sau acceptată.",
                "Propun să plecăm la opt.",
            ),
            VocabularyEntry(
                "a accepta",
                "verb",
                "A spune da unei oferte sau unei propuneri.",
                "Accept invitația cu plăcere.",
            ),
            VocabularyEntry(
                "a refuza",
                "verb",
                "A spune că nu dorești sau nu poți accepta ceva.",
                "Trebuie să refuz invitația.",
            ),
            VocabularyEntry(
                "a amâna",
                "verb",
                "A muta o activitate la un moment ulterior.",
                "O să amânăm întâlnirea până luni.",
            ),
            VocabularyEntry(
                "a participa",
                "verb",
                "A lua parte la o activitate.",
                "Aș dori să particip la curs.",
            ),
            VocabularyEntry(
                "disponibil",
                "adjective",
                "Care poate fi folosit sau poate participa.",
                "Sunt disponibil joi după-amiază.",
            ),
        ],
    ),
    VocabularySet(
        "ro_outings_instructions_a2",
        "A2",
        "Ieșiri, vreme și instrucțiuni",
        "a2-unit-7",
        [
            VocabularyEntry(
                "excursie",
                "noun",
                "Călătorie scurtă pentru recreere sau cunoaștere.",
                "Amânăm excursia pentru că plouă.",
            ),
            VocabularyEntry(
                "traseu",
                "noun",
                "Drum ales pentru o deplasare.",
                "Alege traseul care trece prin sat.",
            ),
            VocabularyEntry(
                "hartă",
                "noun",
                "Reprezentare a unui teritoriu și a locurilor sale.",
                "Ia harta înainte să pleci.",
            ),
            VocabularyEntry(
                "indicator",
                "noun",
                "Semn care oferă o direcție sau o informație.",
                "Urmează indicatorul spre cabană.",
            ),
            VocabularyEntry(
                "intersecție",
                "noun",
                "Loc unde se întâlnesc două sau mai multe drumuri.",
                "Oprește la prima intersecție.",
            ),
            VocabularyEntry(
                "trecere de pietoni",
                "phrase",
                "Loc marcat pentru traversarea străzii pe jos.",
                "Traversează pe trecerea de pietoni.",
            ),
            VocabularyEntry(
                "semafor",
                "noun",
                "Dispozitiv cu lumini care dirijează circulația.",
                "Așteaptă până când semaforul este verde.",
            ),
            VocabularyEntry(
                "pod",
                "noun",
                "Construcție care permite trecerea peste apă sau alt obstacol.",
                "Podul pe care îl traversăm este vechi.",
            ),
            VocabularyEntry(
                "pădure", "noun", "Suprafață mare acoperită cu arbori.", "Nu lăsa gunoi în pădure."
            ),
            VocabularyEntry(
                "munte",
                "noun",
                "Formă de relief înaltă.",
                "Mergem la munte pentru că este răcoare.",
            ),
            VocabularyEntry(
                "lac",
                "noun",
                "Întindere de apă înconjurată de uscat.",
                "Lacul pe care îl vedem este adânc.",
            ),
            VocabularyEntry(
                "plajă",
                "noun",
                "Zonă de nisip sau pietriș la marginea apei.",
                "Mergem la plajă după ce mâncăm.",
            ),
            VocabularyEntry(
                "cabană",
                "noun",
                "Clădire pentru cazare, adesea la munte.",
                "Cabana care apare pe hartă este aproape.",
            ),
            VocabularyEntry(
                "vreme",
                "noun",
                "Starea aerului și a cerului într-un anumit moment.",
                "Verifică vremea înainte să pleci.",
            ),
            VocabularyEntry(
                "soare",
                "noun",
                "Astrul care luminează și încălzește Pământul.",
                "Stăm la umbră pentru că soarele este puternic.",
            ),
            VocabularyEntry(
                "ploaie",
                "noun",
                "Apă care cade din nori sub formă de picături.",
                "Luăm umbrela pentru că vine ploaia.",
            ),
            VocabularyEntry(
                "ninsoare",
                "noun",
                "Cădere de fulgi de zăpadă.",
                "Drumul este greu din cauza ninsorii.",
            ),
            VocabularyEntry(
                "vânt", "noun", "Mișcare a aerului.", "Închide fereastra, pentru că bate vântul."
            ),
            VocabularyEntry(
                "nor",
                "noun",
                "Masă vizibilă de picături sau cristale de apă pe cer.",
                "Norii care vin dinspre munte sunt întunecați.",
            ),
            VocabularyEntry(
                "umbrelă",
                "noun",
                "Obiect care protejează de ploaie sau de soare.",
                "Ia umbrela pe care am lăsat-o lângă ușă.",
            ),
            VocabularyEntry(
                "a traversa",
                "verb",
                "A trece de pe o parte pe cealaltă.",
                "Traversează strada pe verde.",
            ),
            VocabularyEntry(
                "a urma",
                "verb",
                "A merge în direcția indicată sau după cineva.",
                "Urmați săgețile albastre.",
            ),
            VocabularyEntry(
                "a opri",
                "verb",
                "A întrerupe mișcarea sau funcționarea.",
                "Opriți mașina înainte de pod.",
            ),
            VocabularyEntry(
                "a continua",
                "verb",
                "A face mai departe o activitate începută.",
                "Continuați până la cabană.",
            ),
            VocabularyEntry(
                "a proteja",
                "verb",
                "A feri de pericol sau de deteriorare.",
                "Protejați natura și luați gunoiul cu voi.",
            ),
            VocabularyEntry(
                "a anula",
                "verb",
                "A decide că un eveniment planificat nu mai are loc.",
                "Anulăm plimbarea pentru că este furtună.",
            ),
        ],
    ),
]
