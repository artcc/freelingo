"""Croatian C2 placement items for grammar, vocabulary and reading."""

from app.data._types import AssessmentQuestion

C2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "hr-g-c2-001",
        "grammar",
        "C2",
        "U razgovoru je utvrđeno da će Petra, a ne Ana, nazvati majstora. "
        "Zapis glasi: „Ana je rekla Petri da će ona nazvati majstora.” "
        "Koja prerada uklanja nejasnoću i čuva govornika i izvršiteljicu poziva?",
        [
            "Petra je rekla Ani da će Ana nazvati majstora.",
            "Ana je rekla Petri da će sama nazvati majstora.",
            "Ana je rekla Petri da će Petra nazvati majstora.",
            "Petra je rekla Ani da će Petra nazvati majstora.",
        ],
        "Ana je rekla Petri da će Petra nazvati majstora.",
        "hr-reference-repair-c2",
    ),
    AssessmentQuestion(
        "hr-g-c2-002",
        "grammar",
        "C2",
        "U zapisniku stoji: „Jučerašnje odbijanje zahtjeva stanara od strane "
        "povjerenstva potaknulo je upravitelja da zatraži obrazloženje.” "
        "Koja rečenica čuva raspodjelu uloga i vrijeme odbijanja?",
        [
            "Povjerenstvo je jučer odbilo zahtjev stanara pa je upravitelj zatražio obrazloženje.",
            "Stanari su jučer odbili zahtjev povjerenstva pa je upravitelj zatražio obrazloženje.",
            "Upravitelj je jučer odbio zahtjev stanara pa je povjerenstvo zatražilo obrazloženje.",
            "Povjerenstvo je zatražilo obrazloženje jer je upravitelj jučer odbio zahtjev stanara.",
        ],
        "Povjerenstvo je jučer odbilo zahtjev stanara pa je upravitelj zatražio obrazloženje.",
        "hr-nominal-compression-c2",
    ),
    AssessmentQuestion(
        "hr-g-c2-003",
        "grammar",
        "C2",
        "Novinar pita: „Zašto ste opet poslali obavijest prekasno?” "
        "Predstavnica prihvaća da je današnja obavijest zakasnila, ali osporava "
        "tvrdnju o ponavljanju. Koji odgovor to izražava?",
        [
            "Kao i prošli put, zakasnili smo jer smo dugo čekali potvrdu.",
            "Razumijem pitanje, ali ni današnja obavijest nije poslana prekasno.",
            "Prethodno je kašnjenje bilo opravdano, a za današnje ćemo se ispričati.",
            "Danas smo zakasnili; na koji raniji slučaj mislite kad kažete opet?",
        ],
        "Danas smo zakasnili; na koji raniji slučaj mislite kad kažete opet?",
        "hr-presupposition-c2",
    ),
    AssessmentQuestion(
        "hr-g-c2-004",
        "grammar",
        "C2",
        "Pravilo glasi: „Dvorana se zatvara u deset. Članovi udruge mogu ostati "
        "do jedanaest ako to upravitelj prethodno odobri. Pospremaju svi korisnici.” "
        "Koji sažetak čuva doseg iznimke i preostalu obvezu?",
        [
            "Uz prethodno odobrenje svi korisnici mogu ostati do jedanaest i moraju pospremiti.",
            "Članovi mogu ostati do jedanaest uz prethodno odobrenje te i tada moraju pospremiti.",
            "Članovi mogu ostati do jedanaest bez odobrenja ako nakon toga pospreme dvoranu.",
            "Članovi s prethodnim odobrenjem ostaju do jedanaest, a pospremaju raniji korisnici.",
        ],
        "Članovi mogu ostati do jedanaest uz prethodno odobrenje te i tada moraju pospremiti.",
        "hr-conditional-exceptions-c2",
    ),
    AssessmentQuestion(
        "hr-g-c2-005",
        "grammar",
        "C2",
        "Govornica želi izričito ispraviti primatelja poruke: poslala ju je "
        "Luki, ne njegovoj sestri. Koja je rečenica prikladna za taj kontrast?",
        [
            "Njegovoj sam sestri poslala poruku, a njemu odgovor.",
            "Njemu sam poslala poruku, ne njegovoj sestri.",
            "On mi je poslao poruku, ne njegova sestra.",
            "Poruku sam mu proslijedila od njegove sestre.",
        ],
        "Njemu sam poslala poruku, ne njegovoj sestri.",
        "hr-clitics-rhythm-c2",
    ),
    AssessmentQuestion(
        "hr-g-c2-006",
        "grammar",
        "C2",
        "U priči piše: „Bijaše tiho. Putnik zastade pred kućom i pokuca.” "
        "Koje neutralno prepričavanje čuva pozadinu i završene radnje?",
        [
            "Bit će tiho. Putnik će zastati pred kućom i pokucati.",
            "Bilo je tiho. Putnik je zastajao pred kućom i kucao.",
            "Bilo je tiho. Putnik je pokucao pa zastao pred kućom.",
            "Bilo je tiho. Putnik je zastao pred kućom i pokucao.",
        ],
        "Bilo je tiho. Putnik je zastao pred kućom i pokucao.",
        "hr-literary-past-c2",
    ),
    AssessmentQuestion(
        "hr-g-c2-007",
        "grammar",
        "C2",
        "U pisanoj uputi treba ograničiti krug osoba koje smiju povući zahtjev, "
        "ali ne i ostale Ivine ovlasti. Koja formulacija to nedvosmisleno čini?",
        [
            "Samo Iva smije povući zahtjev; ostali za to nisu ovlašteni.",
            "Iva smije samo povući zahtjev; druge promjene nisu joj dopuštene.",
            "Iva smije povući samo svoj zahtjev; tuđe ne smije povlačiti.",
            "Iva smije povući zahtjev samo danas; sutra to više neće moći.",
        ],
        "Samo Iva smije povući zahtjev; ostali za to nisu ovlašteni.",
        "hr-focus-particles-c2",
    ),
    AssessmentQuestion(
        "hr-g-c2-008",
        "grammar",
        "C2",
        "Voditelj kaže: „Pokušat ću s vlasnicom dogovoriti povrat pologa, "
        "ali ona još nije pristala.” Koji zapis čuva jačinu obećanja?",
        [
            "Vlasnica će razmotriti povrat pologa nakon voditeljeve potvrde.",
            "Voditelj će osigurati povrat pologa uz naknadnu potvrdu vlasnice.",
            "Voditelj obećava pokušaj, a ishod ovisi o vlasničinu pristanku.",
            "Voditelj je s vlasnicom dogovorio povrat pologa, ali čeka uplatu.",
        ],
        "Voditelj obećava pokušaj, a ishod ovisi o vlasničinu pristanku.",
        "hr-commitment-c2",
    ),
    AssessmentQuestion(
        "hr-v-c2-001",
        "vocabulary",
        "C2",
        "Nakon što je servis napisao da je vlaga mogući uzrok kvara, urednica "
        "kaže: „Nemoj izbaciti tu ogradu.” Na što se odnosi riječ ograda?",
        [
            "Na podatak koji pokazuje tko treba platiti popravak.",
            "Na izraz koji ograničava sigurnost tvrdnje o uzroku.",
            "Na objašnjenje zašto servis nije prihvatio popravak.",
            "Na upozorenje da uređaj više nije siguran za uporabu.",
        ],
        "Na izraz koji ograničava sigurnost tvrdnje o uzroku.",
        "hr-evidence-scope-c2",
    ),
    AssessmentQuestion(
        "hr-v-c2-002",
        "vocabulary",
        "C2",
        "Organizatorica kaže: „Cijenu više ne možemo mijenjati, ali za termine "
        "imamo manevarskog prostora.” Što poručuje?",
        [
            "Raspored je utvrđen, a oko naknade se još može pregovarati.",
            "Cijena se može mijenjati ako sudionici pristanu na novi termin.",
            "Datum je privremen jer ovisi o naknadnom dogovoru o cijeni.",
            "Cijena ostaje ista, a datumi se još mogu prilagoditi.",
        ],
        "Cijena ostaje ista, a datumi se još mogu prilagoditi.",
        "hr-concessive-negotiation-c2",
    ),
    AssessmentQuestion(
        "hr-v-c2-003",
        "vocabulary",
        "C2",
        "Urednica traži jezgrovit sažetak dogovora za stanare. Koji opis najbolje "
        "odgovara tom zahtjevu?",
        [
            "Kratak tekst koji čuva bitne obveze i uvjete.",
            "Svečan tekst s dojmljivim izrazima zahvalnosti.",
            "Oprezan tekst koji izbjegava navesti odgovorne.",
            "Opširan tekst koji prati redoslijed svih replika.",
        ],
        "Kratak tekst koji čuva bitne obveze i uvjete.",
        "hr-register-recasting-c2",
    ),
    AssessmentQuestion(
        "hr-v-c2-004",
        "vocabulary",
        "C2",
        "Poslije kolegine neugodne primjedbe Ivan kaže: „Ono o njezinu otkazu bilo je "
        "podbadanje, ne savjet.” Kako Ivan tumači tu primjedbu?",
        [
            "Kao nenamjernu zamjenu osobe o kojoj se govorilo.",
            "Kao neizravnu preporuku za sljedeći razgovor za posao.",
            "Kao izazivanje zajedljivom opaskom na osjetljivu temu.",
            "Kao otvoreno objašnjenje razloga prekida zaposlenja.",
        ],
        "Kao izazivanje zajedljivom opaskom na osjetljivu temu.",
        "hr-implicature-c2",
    ),
    AssessmentQuestion(
        "hr-v-c2-005",
        "vocabulary",
        "C2",
        "U razgovoru o romanu netko kaže: „Njezina slutnja da će se brat vratiti "
        "nije isto što i saznanje.” Što riječ slutnja ovdje označava?",
        [
            "Sjećanje na događaj koji je već osobno doživjela.",
            "Tuđu vijest koju je prihvatila kao pouzdanu.",
            "Zaključak zasnovan na provjerenim podacima.",
            "Neodređen osjećaj o onome što bi moglo doći.",
        ],
        "Neodređen osjećaj o onome što bi moglo doći.",
        "hr-free-indirect-c2",
    ),
    AssessmentQuestion(
        "hr-v-c2-006",
        "vocabulary",
        "C2",
        "Organizator je poruku „Načelno podržavam izlet; troškovnik još nisam vidjela” "
        "unio u popis konačnih prijava. Kojom replikom sudionica najpreciznije "
        "ispravlja status svoje potpore?",
        [
            "Podržala sam zamisao, ali time nisam prihvatila financijske uvjete.",
            "Prihvatila sam troškove, ali još nisam potvrdila odabir mjesta izleta.",
            "Moja je prijava konačna, ali zadržavam pravo na kasniji povrat novca.",
            "Podržala sam odlazak drugih, ali sam isključila svoje sudjelovanje.",
        ],
        "Podržala sam zamisao, ali time nisam prihvatila financijske uvjete.",
        "hr-commitment-c2",
    ),
    AssessmentQuestion(
        "hr-v-c2-007",
        "vocabulary",
        "C2",
        "Na sastanku se razgovor s roka za obnovu prebacio na uspomene iz škole. "
        "Voditelj kaže: „Zanimljiva digresija, ali vratimo se roku.” "
        "Što označava digresija?",
        [
            "Sažimanje onoga što je već usuglašeno.",
            "Ponovno otvaranje prethodno riješenog pitanja.",
            "Privremeno udaljavanje od glavne teme.",
            "Ispravljanje netočnog podatka o terminu.",
        ],
        "Privremeno udaljavanje od glavne teme.",
        "hr-interwoven-discourse-c2",
    ),
    AssessmentQuestion(
        "hr-v-c2-008",
        "vocabulary",
        "C2",
        "Urednica traži da se obavijest „Povrat pologa izvršit će se po utvrđenju "
        "da nema nepodmirenih obveza” preformulira za stanare, bez promjene uvjeta. "
        "Koja verzija odgovara tom zahtjevu?",
        [
            "Polog će biti vraćen prije provjere, a eventualni dug naplaćen poslije.",
            "Polog će biti vraćen nakon što se potvrdi da nema nepodmirenih obveza.",
            "Polog može biti vraćen ako obećate da ćete podmiriti preostale obveze.",
            "Polog će biti vraćen nakon provjere, umanjen za utvrđena dugovanja.",
        ],
        "Polog će biti vraćen nakon što se potvrdi da nema nepodmirenih obveza.",
        "hr-register-recasting-c2",
    ),
    AssessmentQuestion(
        "hr-r-c2-001",
        "reading",
        "C2",
        "Prije izleta Dario je uvjeravao grupu: „Ovim putem nema čekanja.” "
        "Sada već četrdeset minuta stoje pred radovima. Maja pogleda sat "
        "i ponovi: „Da, ovdje stvarno nema čekanja.” Dario uzdahne. "
        "Što najbolje objašnjava Majinu repliku?",
        [
            "Brani Darijev izbor jer radove smatra nepredvidivom iznimkom.",
            "Traži potvrdu da će nakon radova nastaviti bez novih zastoja.",
            "Ponavlja uputu onima koji nisu čuli plan prije polaska.",
            "Suprotstavlja Darijevo ranije uvjeravanje sadašnjem iskustvu.",
        ],
        "Suprotstavlja Darijevo ranije uvjeravanje sadašnjem iskustvu.",
        "hr-ironic-echo-c2",
    ),
    AssessmentQuestion(
        "hr-r-c2-002",
        "reading",
        "C2",
        "„Sutra rano ustajem”, odgovori Lea kad je prijatelji pozovu na još "
        "jedno piće. Ivan počne skupljati njezine stvari. Lea doda: "
        "„Ali deset minuta mogu ostati; ne moramo baš odmah krenuti.” "
        "Što njezin dodatak mijenja?",
        [
            "Povlači tvrdnju da sutra mora ustati ranije.",
            "Ispravlja zaključak da želi odmah otići.",
            "Prihvaća da Ivan ode dok ona ostaje cijelu večer.",
            "Objašnjava da je prvotni odgovor bio ironičan.",
        ],
        "Ispravlja zaključak da želi odmah otići.",
        "hr-implicature-c2",
    ),
    AssessmentQuestion(
        "hr-r-c2-003",
        "reading",
        "C2",
        "Luka želi apartman u centru da bi navečer mogao pješice kući. "
        "Ivi smeta noćna buka. Predloži stan u mirnoj ulici petnaest minuta "
        "hoda od centra. Luka pristaje ako taj put nema stepenica. "
        "Iva kaže da će provjeriti. Što je zasad utvrđeno?",
        [
            "Pristali su na stan jer je potvrđeno da put nema stepenica.",
            "Iva je odustala od tišine kako bi Luka bio bliže centru.",
            "Prijedlog povezuje obje potrebe, ali jedan uvjet još nije provjeren.",
            "Luka je prihvatio stan i prepustio Ivi izbor načina povratka.",
        ],
        "Prijedlog povezuje obje potrebe, ali jedan uvjet još nije provjeren.",
        "hr-concessive-negotiation-c2",
    ),
    AssessmentQuestion(
        "hr-r-c2-004",
        "reading",
        "C2",
        "Marta je zastala pred zaključanom dvoranom. Naravno, za nju opet nije "
        "bilo mjesta! Stisnula je torbu i okrenula se prema izlazu. "
        "Nije vidjela natpis na vratima: sastanak je premješten na kat. "
        "Kako treba razumjeti uzvik o mjestu?",
        [
            "Kao Martinu procjenu koju kasniji podatak dovodi u pitanje.",
            "Kao pripovjedačevu potvrdu da su Martu namjerno isključili.",
            "Kao tuđu primjedbu koju je Marta čula prije ulaska.",
            "Kao Martinu ironiju jer je već znala za promjenu prostorije.",
        ],
        "Kao Martinu procjenu koju kasniji podatak dovodi u pitanje.",
        "hr-free-indirect-c2",
    ),
    AssessmentQuestion(
        "hr-r-c2-005",
        "reading",
        "C2",
        "Na sastanku Ana predloži subotu. Dario pita može li se unajmiti kombi. "
        "Dok Ivana traži cijenu, Marko kaže: „Meni odgovara nedjelja.” "
        "Ana zatim doda: „Što se kombija tiče, to mogu provjeriti ja.” "
        "Koji bi zapis vjerno sažeo razgovor?",
        [
            "Ana nudi provjeriti kombi; subota i nedjelja ostaju različiti prijedlozi.",
            "Ana je prihvatila nedjelju i preuzela provjeru dostupnosti kombija.",
            "Marko je odabrao nedjelju pa Ivana treba unajmiti kombi za taj dan.",
            "Dario će provjeriti kombi, a Ana i Marko usuglasit će datum s Ivanom.",
        ],
        "Ana nudi provjeriti kombi; subota i nedjelja ostaju različiti prijedlozi.",
        "hr-interwoven-discourse-c2",
    ),
    AssessmentQuestion(
        "hr-r-c2-006",
        "reading",
        "C2",
        "Kad se Tea u petak vratila u stan i vidjela popravljen prozor, pomislila je "
        "da je posao obavljen još prije nego što joj je susjed u četvrtak poslao "
        "fotografiju. Tek je navečer pročitala majstorovu poruku poslanu toga jutra: "
        "„Upravo sam završio; susjedova fotografija prikazuje stanje prije popravka.” "
        "Kako ta poruka mijenja Teino prvotno tumačenje?",
        [
            "Popravak smješta prije slanja fotografije, ali poslije snimanja oštećenja.",
            "Popravak smješta nakon svojeg povratka, neposredno prije čitanja poruke.",
            "Popravak smješta nakon slanja fotografije, ali i dalje prije svojeg povratka.",
            "Slanje fotografije smješta u petak, neposredno nakon dovršetka popravka.",
        ],
        "Popravak smješta nakon slanja fotografije, ali i dalje prije svojeg povratka.",
        "hr-narrative-time-c2",
    ),
    AssessmentQuestion(
        "hr-r-c2-007",
        "reading",
        "C2",
        "Raspored je trima zasebnim radionicama dodijelio istu prostoriju "
        "u isto vrijeme. Uredno složene mape nisu mnogo pomogle. "
        "Koordinatorica ih pogleda i kaže: „Organizacija nam nije baš "
        "idealna.” Zatim zamoli kolegu da odmah nazove predavače. "
        "Što njezina formulacija najvjerojatnije čini?",
        [
            "Izdvaja izgled mapa kao glavni nedostatak pripreme.",
            "Suzdržano izražava ozbiljniju kritiku praktičnog propusta.",
            "Uspoređuje prihvatljiv raspored s nedostižnim savršenstvom.",
            "Prebacuje odgovornost na predavače koji nisu pratili raspored.",
        ],
        "Suzdržano izražava ozbiljniju kritiku praktičnog propusta.",
        "hr-understatement-c2",
    ),
    AssessmentQuestion(
        "hr-r-c2-008",
        "reading",
        "C2",
        "U dopisu stoji: „Preporučuje se prethodna najava dolaska.” "
        "Djelatnik na telefonu kaže: „Bilo bi dobro da nam prije dolaska "
        "javite, ali primit ćemo vas i bez najave.” Kolegica predlaže da "
        "u sažetku napišu: „Bez najave nema ulaska.” Zašto njezin prijedlog "
        "nije vjeran prethodnim porukama?",
        [
            "Preporuku ograničava na telefonske, umjesto na sve vrste najave.",
            "Obvezu najave prenosi s posjetitelja na djelatnika ustanove.",
            "Dopuštenje dolaska pretvara u obećanje prijma u određeno vrijeme.",
            "Preporučeni postupak pretvara u nužan uvjet za ulazak.",
        ],
        "Preporučeni postupak pretvara u nužan uvjet za ulazak.",
        "hr-register-recasting-c2",
    ),
]
