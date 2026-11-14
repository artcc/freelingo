"""Croatian C2 phrases for spontaneous repair, mediation and stylistic control."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "hr_clarifying_dialogue_c2",
        "C2",
        "Razjasniti nečiji iskaz bez prekidanja suradnje",
        "🔎",
        [
            PhrasebookEntry(
                "Kad kažeš da će ona preuzeti ključeve, misliš na Maju ili na njezinu sestru?",
                "Dvije su žene spomenute u dogovoru o ulasku u stan.",
                "informal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Samo da provjerim jesam li dobro povezao: vi šaljete nacrt, a vlasnik ga odobrava?",
                "Provjera podjele poslova nakon brzog telefonskog razgovora.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Ispravak: rekla sam „srijeda”, a mislila sam „četvrtak”; mjesto i sat ostaju isti.",
                "Trenutačno ispravljanje dana sastanka bez mijenjanja ostalih pojedinosti.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "To mogu razumjeti na dva načina; odnosi li se ograničenje na posjetitelje ili na osoblje?",
                "Razjašnjavanje obavijesti prije organiziranja ulaska grupe.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Ne osporavam što se dogodilo, samo još ne znam na koga se taj dio odnosi.",
                "Sprječavanje dojma da pitanje o sudioniku znači nepovjerenje prema cijeloj priči.",
                "neutral",
                "c2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_responsibility_dialogue_c2",
        "C2",
        "Objasniti nalaz i sačuvati ogradu",
        "📋",
        [
            PhrasebookEntry(
                "U zapisniku piše da je zahtjev odbijen, ali ne i tko ga je odbio.",
                "Razdvajanje potvrđene odluke od nepoznatog izvršitelja prije slanja prigovora.",
                "formal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "To je mogući uzrok, ne potvrđen nalaz; tako bih to i prenio stanarima.",
                "Dogovor o obavijesti nakon preliminarnog pregleda kvara.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Možemo skratiti tekst, ali moramo zadržati tko je odluku donio i na temelju čega.",
                "Uređivanje sažetka zapisnika bez prikrivanja odgovornosti.",
                "formal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Kad kažem da nisu svi pristali, ne tvrdim da je većina bila protiv.",
                "Ispravak preširokog zaključka nakon razgovora o zajedničkom trošku.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Prema onome što zasad znamo, uplata kasni; razlog još provjeravamo.",
                "Obavještavanje suradnika bez preuranjenog optuživanja platitelja.",
                "formal",
                "c2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_humour_dialogue_c2",
        "C2",
        "Odgovoriti na ironiju i popraviti neuspjelu šalu",
        "💬",
        [
            PhrasebookEntry(
                "Ovo tvoje „baš smo se usrećili” zvuči ironično; misliš na gužvu ili na smještaj?",
                "Provjera predmeta šale tijekom zajedničkog putovanja.",
                "informal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Šala je ispala na tvoj račun. Žao mi je; nisam trebao spominjati tvoj razgovor za posao.",
                "Preuzimanje odgovornosti za neugodnu šalu među prijateljima.",
                "informal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Ako sam dobro uhvatila aluziju, vraćaš me na naš prošli pokušaj kuhanja.",
                "Prepoznavanje zajedničke uspomene iza duhovite primjedbe.",
                "informal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Kad kažete „opet”, na koji se raniji slučaj pozivate?",
                "Provjera pretpostavke o ponovljenom propustu u formalnom razgovoru.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Znam da si se šalio, ali taj mi dio nije bio ugodan. Možemo li ga ostaviti?",
                "Postavljanje granice bez osporavanja sugovornikove navedene namjere.",
                "informal",
                "c2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_story_dialogue_c2",
        "C2",
        "Razgovarati o priči i prepričati iskustvo",
        "📖",
        [
            PhrasebookEntry(
                "To da ga je ona zaboravila zasad je njegov zaključak, ne činjenica koju tekst potvrđuje.",
                "Razgovor u čitateljskom klubu o perspektivi povrijeđenog lika.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Ovdje se vraćamo na dan prije susreta; dolazak na kolodvor događa se tek poslije.",
                "Pojašnjavanje redoslijeda prizora sugovorniku koji je izgubio vremensku nit.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Prepričat ću to običnim riječima, ali ne bih htjela izgubiti onu neizvjesnost na kraju.",
                "Usmeno predstavljanje književnog ulomka prijatelju koji ga nije čitao.",
                "informal",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Tada mi je njegova šutnja djelovala hladno; danas je razumijem drukčije.",
                "Pričanje osobnog iskustva uz odvajanje tadašnje i današnje perspektive.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Rečenica „Bijaše tiho” zvuči mi starinski; "
                "u običnom bih razgovoru rekla „Bilo je tiho”.",
                "Objašnjavanje dojma književnog vremena bez zahtjeva za njegovom svakodnevnom uporabom.",
                "neutral",
                "c2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_negotiating_dialogue_c2",
        "C2",
        "Pomiriti suprotne želje bez nejasnih obećanja",
        "🤝",
        [
            PhrasebookEntry(
                "Tebi je važan mir, meni blizina centra; potražimo sporednu ulicu na pješačkoj udaljenosti.",
                "Zajednički odabir smještaja uz dvije različite potrebe.",
                "informal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Mogu pristati na kasniji početak ako unaprijed ograničimo trajanje na sat vremena.",
                "Uvjetni ustupak pri traženju termina koji odgovara objema stranama.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Mogu provjeriti mogućnost povrata, ali ne mogu unaprijed obećati da će biti odobren.",
                "Odgovor zaposlenika koji može pokrenuti provjeru, ali ne donosi konačnu odluku.",
                "formal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Iznimka vrijedi za taj termin; obveza pospremanja ostaje ista.",
                "Pojašnjavanje dopuštenja za kasniji završetak događaja u zajedničkom prostoru.",
                "formal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Kažemo da oboje popuštamo, ali dogovor nije održiv "
                "ako svaki put odustaje ista osoba.",
                "Provjera pravednosti dogovora o ponavljajućim obiteljskim obvezama.",
                "neutral",
                "c2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_threads_dialogue_c2",
        "C2",
        "Održati pregled nad isprepletenim razgovorom",
        "🗣️",
        [
            PhrasebookEntry(
                "Da se vratim na tvoje prvo pitanje: vozilo imamo, ali vozač još nije potvrđen.",
                "Povratak na otvorenu temu nakon nekoliko upadica o smještaju.",
                "informal",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Kad kažeš „može”, pristaješ na promjenu datuma ili samo na provjeru drugog prostora?",
                "Razjašnjavanje skraćene replike koja može odgovarati na dva prijedloga.",
                "informal",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "To je Anin prijedlog; još nismo čuli slaže li se ostatak skupine.",
                "Ispravak sažetka koji pojedinačno mišljenje prikazuje kao odluku svih.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Zabilježimo to kao otvoreno pitanje, pa se vratimo na ono o čemu danas moramo odlučiti.",
                "Vođenje sastanka na kojem sporedna tema prijeti potisnuti glavni cilj.",
                "formal",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Čini mi se da odgovaramo na različita pitanja: ti govoriš o cijeni, a ja o pristupačnosti.",
                "Prepoznavanje prividnog neslaganja kad se replike odnose na različite kriterije.",
                "informal",
                "c2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_tone_dialogue_c2",
        "C2",
        "Prilagoditi ton i razumjeti suzdržanu poruku",
        "📝",
        [
            PhrasebookEntry(
                "Reći ću to jednostavnije: trebamo vaš potpis prije nego što možemo poslati zahtjev.",
                "Objašnjavanje službenog postupka građaninu uz očuvanje obveznog uvjeta.",
                "formal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Ova verzija zvuči kao naredba, a htjeli smo dati preporuku.",
                "Zajedničko uređivanje obavijesti u kojoj ton mijenja dojam obveznosti.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Kad kažete da rezultat nije najsretniji, što biste prvo promijenili?",
                "Pretvaranje suzdržane kritike u konkretan razgovor o poboljšanju.",
                "formal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Mogu biti izravnija, ali ne želim da jasno odbijanje zazvuči kao osobni prigovor.",
                "Priprema odgovora prijatelju čiji se prijedlog ne može prihvatiti.",
                "informal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Skratimo uvod i odmah recimo rok; obrazloženje može doći nakon toga.",
                "Uređivanje govorne obavijesti koju slušatelji trebaju razumjeti iz prvog slušanja.",
                "neutral",
                "c2-unit-7",
            ),
        ],
    ),
]
