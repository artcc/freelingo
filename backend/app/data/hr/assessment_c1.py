"""Croatian C1 placement items on interpretation, precision and interaction."""

from app.data._types import AssessmentQuestion

C1_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "hr-g-c1-001",
        "grammar",
        "C1",
        "Laboratorij je izvijestio: „Nije dokazano da je uzorak bio onečišćen prije prijevoza.” "
        "Koji nastavak čuva doseg negacije u toj rečenici?",
        [
            "Laboratorij je time isključio prijevoz kao mogući izvor onečišćenja.",
            "Laboratorij je potvrdio da je uzorak prije prijevoza bio čist.",
            "Vrijeme mogućeg onečišćenja još nije utvrđeno tim nalazom.",
            "Iz nalaza proizlazi da je do onečišćenja došlo tijekom prijevoza.",
        ],
        "Vrijeme mogućeg onečišćenja još nije utvrđeno tim nalazom.",
        "hr-negation-scope-c1",
    ),
    AssessmentQuestion(
        "hr-g-c1-002",
        "grammar",
        "C1",
        "U zapisniku stoji: „Prijedlog udruge za odgodu obnove razmotrit će gradsko vijeće.” "
        "Koja preoblika čuva uloge sudionika i status odluke?",
        [
            "Udruga je predložila odgodu obnove, a gradsko će vijeće razmotriti prijedlog.",
            "Gradsko je vijeće predložilo odgodu obnove, a udruga će je razmotriti.",
            "Udruga je odgodila obnovu, a gradsko će vijeće razmotriti posljedice.",
            "Gradsko će vijeće razmotriti odgodu rasprave o obnovi koju provodi udruga.",
        ],
        "Udruga je predložila odgodu obnove, a gradsko će vijeće razmotriti prijedlog.",
        "hr-nominalisation-agents-c1",
    ),
    AssessmentQuestion(
        "hr-g-c1-003",
        "grammar",
        "C1",
        "Voditeljica je na sastanku rekla: „Mogli bismo preuzeti večernju smjenu ako nam "
        "osigurate prijevoz.” Što je primjereno unijeti u zapisnik bez povećavanja obveze?",
        [
            "Ekipa će preuzeti večernju smjenu, a prijevoz će naknadno dogovoriti.",
            "Voditeljica je obećala osigurati prijevoz ekipi koja preuzima smjenu.",
            "Ekipa je prihvatila večernju smjenu pod uvjetom da dobije prijevoz.",
            "Preuzimanje smjene izneseno je kao mogućnost uz osiguran prijevoz.",
        ],
        "Preuzimanje smjene izneseno je kao mogućnost uz osiguran prijevoz.",
        "hr-conditional-stance-c1",
    ),
    AssessmentQuestion(
        "hr-g-c1-004",
        "grammar",
        "C1",
        "Urednica je pregledala članak, a zatim ga je autor poslao lektorici. Koja sažeta "
        "verzija vjerno prenosi te dvije radnje?",
        [
            "Pregledavši članak, autor ga je poslao lektorici.",
            "Nakon što je urednica pregledala članak, autor ga je poslao lektorici.",
            "Pregledavši članak, urednica ga je poslala autorovoj lektorici.",
            "Nakon što je autor pregledao članak, urednica ga je poslala lektorici.",
        ],
        "Nakon što je urednica pregledala članak, autor ga je poslao lektorici.",
        "hr-participle-agents-c1",
    ),
    AssessmentQuestion(
        "hr-g-c1-005",
        "grammar",
        "C1",
        "„Organizator je odbio prijedlog vodičice, što je iznenadilo goste.” "
        "Na što se u toj rečenici odnosi „što”?",
        [
            "Na prijedlog koji su gosti ranije podnijeli vodičici.",
            "Na to da je organizator odbio prijedlog vodičice.",
            "Na vodičicu čiji je prijedlog organizator razmatrao.",
            "Na organizatora koji je gostima predstavio vodičicu.",
        ],
        "Na to da je organizator odbio prijedlog vodičice.",
        "hr-relative-reference-c1",
    ),
    AssessmentQuestion(
        "hr-g-c1-006",
        "grammar",
        "C1",
        "Ključ je vraćen Marku, a ne Ivanu. Marko to ispravlja u razgovoru. "
        "Koja rečenica jasno ističe stvarnog primatelja i ima pravilan raspored zanaglasnica?",
        [
            "Ja sam mu ga vratio, a ne Ivanu.",
            "Meni ga vratio je, a ne Ivanu.",
            "Ivanu ga je vratio, a ne meni.",
            "Meni ga je vratio, a ne Ivanu.",
        ],
        "Meni ga je vratio, a ne Ivanu.",
        "hr-clitic-information-c1",
    ),
    AssessmentQuestion(
        "hr-g-c1-007",
        "grammar",
        "C1",
        "„Čak i kad bi izvođač snizio cijenu, ne bismo mogli prihvatiti radove u srpnju.” "
        "Koji zaključak odgovara toj izjavi?",
        [
            "Ni zamišljeni popust ne bi uklonio zapreku za srpanjski termin.",
            "Izvođač je snizio cijenu, ali je srpanjski termin ostao neprihvatljiv.",
            "Srpanjski termin mogao bi se prihvatiti tek nakon sniženja cijene.",
            "Naručitelji traže nižu cijenu kako bi mogli prihvatiti srpanjski termin.",
        ],
        "Ni zamišljeni popust ne bi uklonio zapreku za srpanjski termin.",
        "hr-hypothetical-concession-c1",
    ),
    AssessmentQuestion(
        "hr-g-c1-008",
        "grammar",
        "C1",
        "Recenzentica piše: „Tekst nije toliko nejasan zbog stručnih izraza koliko zbog "
        "neoznačenih prijelaza između tuđih i autoričinih tvrdnji.” Koja urednička odluka "
        "najbolje odgovara težištu primjedbe?",
        [
            "Zadržati način pripisivanja tvrdnji i pojednostavniti svu stručnu terminologiju.",
            "Ujednačiti duljinu odlomaka jer su oba navedena problema ocijenjena jednako važnima.",
            "Prvo razjasniti čije su tvrdnje, a zatim provjeriti treba li objasniti pojedine izraze.",
            "Ukloniti navode drugih autora jer je upotreba stručnih izraza ocijenjena primjerenom.",
        ],
        "Prvo razjasniti čije su tvrdnje, a zatim provjeriti treba li objasniti pojedine izraze.",
        "hr-scalar-focus-c1",
    ),
    AssessmentQuestion(
        "hr-v-c1-001",
        "vocabulary",
        "C1",
        "Udruga još nije pregledala proračun ni raspored. Želi izraziti podršku prijedlogu "
        "bez prihvaćanja svih pojedinosti. Koja riječ prenosi tu namjeru u izjavi: "
        "„Prijedlog podržavamo ___; "
        "o pojedinostima ćemo se očitovati nakon pregleda”?",
        [
            "bezrezervno",
            "jednoglasno",
            "naknadno",
            "načelno",
        ],
        "načelno",
        "hr-reported-commitments-c1",
    ),
    AssessmentQuestion(
        "hr-v-c1-002",
        "vocabulary",
        "C1",
        "Predstavnik smije pregovarati o cijeni, ali ugovor smije potpisati samo ravnateljica. "
        "Koji izraz najpreciznije dopunjuje: „Za potpisivanje ugovora predstavnik nema ___”?",
        [
            "suglasnost ponuđača",
            "ovlast",
            "očitovanje",
            "izvedivost",
        ],
        "ovlast",
        "hr-passive-accountability-c1",
    ),
    AssessmentQuestion(
        "hr-v-c1-003",
        "vocabulary",
        "C1",
        "Arhivska snimka jasno pokazuje da je svjetionik stajao 1920., suprotno tvrdnji da je "
        "izgrađen 1930. Koji glagol najtočnije opisuje odnos snimke prema toj tvrdnji?",
        [
            "Opovrgava je.",
            "Potkrepljuje je.",
            "Ublažava je.",
            "Preformulira je.",
        ],
        "Opovrgava je.",
        "hr-negation-scope-c1",
    ),
    AssessmentQuestion(
        "hr-v-c1-004",
        "vocabulary",
        "C1",
        "Na predstavljanju izložbe kustosica govori o radu koji je osobno obavila. "
        "Koji izraz označuje izvor njezina znanja u rečenici: "
        "„O stanju predmeta prije obnove govorim ___”?",
        [
            "iz druge ruke",
            "u dobroj vjeri",
            "iz prve ruke",
            "bez uvijanja",
        ],
        "iz prve ruke",
        "hr-source-attribution-c1",
    ),
    AssessmentQuestion(
        "hr-v-c1-005",
        "vocabulary",
        "C1",
        "Dvoje kolega sve glasnije ponavlja iste prigovore. Treća osoba želi smiriti ton i "
        "vratiti razgovor na činjenice. Koja je replika najprikladnija?",
        [
            "Hajdemo ostati pri svome; neka svatko zapiše svoju verziju dogovora.",
            "Hajdemo to staviti na stranu i prijeći na sljedeću točku dnevnog reda.",
            "Hajdemo spustiti loptu i pogledati što zapravo piše u dogovoru.",
            "Hajdemo krenuti od nule i sastaviti posve novi prijedlog dogovora.",
        ],
        "Hajdemo spustiti loptu i pogledati što zapravo piše u dogovoru.",
        "hr-diplomatic-questions-c1",
    ),
    AssessmentQuestion(
        "hr-v-c1-006",
        "vocabulary",
        "C1",
        "Stanari i organizatori još se ne slažu oko večernjih termina. Obje strane ipak traže "
        "da hitne službe uvijek mogu pristupiti zgradi. Što taj zahtjev predstavlja u pregovorima?",
        [
            "Zajedničko polazište.",
            "Obvezujući završni sporazum.",
            "Jednostrani ustupak.",
            "Otvoreno pitanje rasporeda.",
        ],
        "Zajedničko polazište.",
        "hr-cohesive-summary-c1",
    ),
    AssessmentQuestion(
        "hr-v-c1-007",
        "vocabulary",
        "C1",
        "Autorica se unaprijed odlučila za jedan zaključak te navodi samo podatke koji mu "
        "idu u prilog. Koji pojam najpreciznije opisuje problem takva prikaza?",
        [
            "Suzdržanost.",
            "Pristranost.",
            "Sljedivost.",
            "Nadležnost.",
        ],
        "Pristranost.",
        "hr-source-attribution-c1",
    ),
    AssessmentQuestion(
        "hr-v-c1-008",
        "vocabulary",
        "C1",
        "Nakon što je kao voditelj izleta poveo skupinu krivom ulicom, Luka kaže: "
        "„Za mene bi i ravna cesta trebala upute.” Kako je oblikovao šalu?",
        [
            "Podbadanjem članova skupine.",
            "Pohvalom tuđeg snalaženja.",
            "Prigovorom organizatoru izleta.",
            "Na svoj račun.",
        ],
        "Na svoj račun.",
        "hr-contextual-irony-c1",
    ),
    AssessmentQuestion(
        "hr-r-c1-001",
        "reading",
        "C1",
        "„Nakon uvođenja besplatnog ulaza porastao je broj posjeta muzeju. U istom je razdoblju "
        "otvorena dugo najavljivana izložba, a turistički ured počeo je organizirati dolaske "
        "grupa. Uprava stoga najavljuje dodatnu analizu prije odluke o trajnom ukidanju ulaznica.” "
        "Zašto uprava odgađa konačnu odluku?",
        [
            "Smatra da nova izložba nije privukla dovoljno samostalnih posjetitelja.",
            "Raspoloživi podaci ne izdvajaju učinak cijene od ostalih istodobnih promjena.",
            "Čeka da turistički ured preuzme troškove besplatnih ulaznica.",
            "Želi provjeriti jesu li grupni dolasci smanjili ukupan broj posjeta.",
        ],
        "Raspoloživi podaci ne izdvajaju učinak cijene od ostalih istodobnih promjena.",
        "hr-cause-inference-c1",
    ),
    AssessmentQuestion(
        "hr-r-c1-002",
        "reading",
        "C1",
        "„Premda podržavamo širenje pješačke zone, nacrt ne možemo prihvatiti u ovom obliku. "
        "Dostava lijekova predviđena je u istom terminu kao jutarnji dolazak učenika, a "
        "zamjenski pristup nije razrađen.” Što bi najizravnije odgovorilo na navedeni prigovor?",
        [
            "Podaci o tome koliko građana načelno podržava manje automobila u središtu.",
            "Prijedlog da se proširenje pješačke zone zamijeni dodatnim parkiralištem.",
            "Objašnjenje da je dostava lijekova važnija od ostale dostave.",
            "Razrada sigurnog pristupa i termina dostave koji ne ometa dolazak učenika.",
        ],
        "Razrada sigurnog pristupa i termina dostave koji ne ometa dolazak učenika.",
        "hr-concessive-argument-c1",
    ),
    AssessmentQuestion(
        "hr-r-c1-003",
        "reading",
        "C1",
        "Projektor je zatajio treći put. Voditeljica pogleda ugašeni zaslon i kaže: "
        "„Baš je divno kad se možemo osloniti na tehniku.” Suradnik želi priznati problem "
        "i praktično nastaviti izlaganje. Koji odgovor najbolje odgovara situaciji?",
        [
            "Slažem se, ova nam je oprema znatno olakšala današnje izlaganje.",
            "Možemo preskočiti raspravu, očito smatraš da sadržaj nije dovoljno zanimljiv.",
            "Danas nas baš iskušava; mogu podijeliti ispisane materijale dok ga ponovno uključimo.",
            "Nema potrebe za prigovorom, sudionici su ionako trebali unaprijed pročitati materijale.",
        ],
        "Danas nas baš iskušava; mogu podijeliti ispisane materijale dok ga ponovno uključimo.",
        "hr-contextual-irony-c1",
    ),
    AssessmentQuestion(
        "hr-r-c1-004",
        "reading",
        "C1",
        "Predstavnica stanara kaže: „Razgovarat ćemo o ranijem početku radova ako nam "
        "dostavite plan zaštite prolaza.” Izvođač odgovara: „Plan možemo poslati do petka, "
        "no termin još ovisi o dobavljaču.” Koji je posrednikov sažetak vjeran objema stranama?",
        [
            "Plan je uvjet za razgovor; početak radova još nije dogovoren.",
            "Stanari su prihvatili raniji početak uz dostavu plana do petka.",
            "Izvođač je potvrdio početak u petak nakon suglasnosti dobavljača.",
            "Termin je usuglašen, a preostaje samo oblikovati plan zaštite.",
        ],
        "Plan je uvjet za razgovor; početak radova još nije dogovoren.",
        "hr-reported-commitments-c1",
    ),
    AssessmentQuestion(
        "hr-r-c1-005",
        "reading",
        "C1",
        "„Kad smo došli do pristaništa, trajekt je već bio isplovio. Tek smo u kafiću pročitali "
        "jutarnju poruku kojom nas je domaćin upozorio na izmijenjeni vozni red. Na putu smo "
        "isključili obavijesti da bismo uštedjeli bateriju.” Što pripovjedač naknadno razjašnjava?",
        [
            "Domaćin je promjenu voznog reda doznao tek nakon njihova dolaska.",
            "Trajekt je isplovio prije nego što je domaćin mogao poslati upozorenje.",
            "Poruku su pročitali na vrijeme, ali su pogrešno protumačili novi vozni red.",
            "Upozorenje je bilo poslano ranije, ali ga putnici nisu pravodobno pročitali.",
        ],
        "Upozorenje je bilo poslano ranije, ali ga putnici nisu pravodobno pročitali.",
        "hr-temporal-perspective-c1",
    ),
    AssessmentQuestion(
        "hr-r-c1-006",
        "reading",
        "C1",
        "„Dvoranu možemo ustupiti samo ako ostane dostupna za redovitu nastavu. Vaš raspored "
        "zadovoljava taj zahtjev. Prije potvrde rezervacije još čekamo procjenu troškova "
        "dežurstva.” Što organizatori sada mogu opravdano javiti sudionicima?",
        [
            "Rezervacija je potvrđena, a troškovi dežurstva bit će naknadno obračunati.",
            "Zahtjev je odbijen jer ustupanje prostora zahtijeva dodatno dežurstvo.",
            "Raspored je prihvatljiv, ali rezervacija još čeka konačnu potvrdu.",
            "Dvorana će biti dostupna čim organizatori promijene termine nastave.",
        ],
        "Raspored je prihvatljiv, ali rezervacija još čeka konačnu potvrdu.",
        "hr-necessary-conditions-c1",
    ),
    AssessmentQuestion(
        "hr-r-c1-007",
        "reading",
        "C1",
        "„Prema tvrdnji vlasnika, slika je desetljećima bila u obitelji. Muzej navodi da "
        "podrijetlo još nije dokumentirano. Analiza boje zasad ne proturječi predloženoj "
        "dataciji, ali sama ne potvrđuje autorstvo.” Koji je naslov najvjerniji tekstu?",
        [
            "Autorstvo slike ostaje otvoreno; obiteljsko podrijetlo tek treba dokumentirati.",
            "Analiza boje potvrdila autorstvo, muzej još provjerava povijest vlasništva.",
            "Muzej osporio obiteljsko podrijetlo slike nakon analize njezine starosti.",
            "Vlasnik dokazao povijest slike, stručnjaci odgodili utvrđivanje njezine starosti.",
        ],
        "Autorstvo slike ostaje otvoreno; obiteljsko podrijetlo tek treba dokumentirati.",
        "hr-source-attribution-c1",
    ),
    AssessmentQuestion(
        "hr-r-c1-008",
        "reading",
        "C1",
        "„Knjižnica predlaže produljenje rada subotom, a zaposlenici traže dodatnu osobu u "
        "smjeni. Ravnateljica podržava dulju dostupnost usluge. Taj zahtjev, međutim, još "
        "nije financijski razrađen.” Urednik želi ukloniti nejasno upućivanje u posljednjoj "
        "rečenici, a zadržati zahtjev zaposlenika. Koja je zamjena primjerena?",
        [
            "Produljenje subotnjeg rada već ima osigurano financiranje.",
            "Trošak dodatne osobe u subotnjoj smjeni još nije razrađen.",
            "Ravnateljičin zahtjev za duljim radom još nije prihvaćen.",
            "Zahtjev zaposlenika za kraćom subotnjom smjenom još nije razrađen.",
        ],
        "Trošak dodatne osobe u subotnjoj smjeni još nije razrađen.",
        "hr-cohesive-summary-c1",
    ),
]
