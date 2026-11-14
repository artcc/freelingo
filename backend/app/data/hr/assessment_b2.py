"""Croatian B2 placement: contextual form, lexical choice and inference."""

from app.data._types import AssessmentQuestion

B2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "hr-g-b2-001",
        "grammar",
        "B2",
        "Dopunite pisanu obavijest tako da protivljenje prikažete kao prepreku "
        "koja nije spriječila odluku: „___ protivljenju dijela stanara, radionica "
        "ostaje u prizemlju.”",
        ["Unatoč", "Zbog", "Premda", "Iako"],
        "Unatoč",
        "hr-concession-b2",
    ),
    AssessmentQuestion(
        "hr-g-b2-002",
        "grammar",
        "B2",
        "U izvješću stoji: „Nisu svi kandidati zadovoljili uvjete.” "
        "Koji zaključak proizlazi iz same te rečenice?",
        [
            "Većina kandidata ispunila je tražene uvjete.",
            "Nijedan kandidat nije zadovoljio uvjete.",
            "Barem jedan kandidat nije zadovoljio uvjete.",
            "Uvjeti su ispunjeni kod polovice kandidata.",
        ],
        "Barem jedan kandidat nije zadovoljio uvjete.",
        "hr-negation-scope-b2",
    ),
    AssessmentQuestion(
        "hr-g-b2-003",
        "grammar",
        "B2",
        "U ponedjeljak je Lea rekla: „Možda ću nacrt poslati sutra.” "
        "U četvrtak kolegi prenosite samo tu izjavu. Koja verzija čuva "
        "njezinu vremensku perspektivu i stupanj sigurnosti?",
        [
            "Lea je u ponedjeljak obećala da će nacrt poslati u utorak.",
            "Lea je u ponedjeljak rekla da će nacrt možda poslati u petak.",
            "Lea je u ponedjeljak potvrdila da je nacrt poslala u nedjelju.",
            "Lea je u ponedjeljak rekla da će nacrt možda poslati u utorak.",
        ],
        "Lea je u ponedjeljak rekla da će nacrt možda poslati u utorak.",
        "hr-temporal-perspective-b2",
    ),
    AssessmentQuestion(
        "hr-g-b2-004",
        "grammar",
        "B2",
        "Preoblikujte u aktiv uz iste sudionike, vrijeme i dovršenost: "
        "„Dokumentacija je pregledana od strane ovlaštenog stručnjaka.”",
        [
            "Ovlašteni stručnjak pregledavao je dokumentaciju.",
            "Ovlašteni stručnjak pregledao je dokumentaciju.",
            "Ovlašteno povjerenstvo pregledalo je dokumentaciju.",
            "Ovlašteni stručnjak pregledat će dokumentaciju.",
        ],
        "Ovlašteni stručnjak pregledao je dokumentaciju.",
        "hr-passive-agency-b2",
    ),
    AssessmentQuestion(
        "hr-g-b2-005",
        "grammar",
        "B2",
        "Propustili ste jučerašnju prezentaciju jer niste dobili obavijest. "
        "Koja rečenica izražava neostvarenu prošlu mogućnost?",
        [
            "Ako dobijem obavijest, doći ću na prezentaciju.",
            "Da sam dobila obavijest, došla bih na prezentaciju.",
            "Budući da sam dobila obavijest, došla sam na prezentaciju.",
            "Iako sam dobila obavijest, nisam došla na prezentaciju.",
        ],
        "Da sam dobila obavijest, došla bih na prezentaciju.",
        "hr-past-counterfactual-b2",
    ),
    AssessmentQuestion(
        "hr-g-b2-006",
        "grammar",
        "B2",
        "Nakon rasprave netko kaže: „Čak je i Tomislav podržao prijedlog.” "
        "Što riječ čak pokazuje o govornikovu stavu?",
        [
            "Tomislavova podrška prikazana je kao nedovoljna za odluku.",
            "Tomislavova podrška prikazana je kao uvjet podrške ostalih.",
            "Tomislavova podrška prikazana je kao jedina u skupini.",
            "Tomislavova podrška prikazana je kao nešto neočekivano.",
        ],
        "Tomislavova podrška prikazana je kao nešto neočekivano.",
        "hr-focus-particles-b2",
    ),
    AssessmentQuestion(
        "hr-g-b2-007",
        "grammar",
        "B2",
        "Koja rečenica jasno kaže da uprava traži radnju, a dobavljač je treba izvršiti?",
        [
            "Uprava je zamolila dobavljača da pošalje novi troškovnik.",
            "Uprava je odlučila poslati dobavljaču novi troškovnik.",
            "Dobavljač je zamolio upravu da pošalje novi troškovnik.",
            "Uprava je dobavljaču obećala poslati novi troškovnik.",
        ],
        "Uprava je zamolila dobavljača da pošalje novi troškovnik.",
        "hr-infinitive-subject-b2",
    ),
    AssessmentQuestion(
        "hr-g-b2-008",
        "grammar",
        "B2",
        "Pravilo glasi: „Trošak se može nadoknaditi samo ako je priložen račun.” "
        "Koja tvrdnja vrijedi na temelju toga pravila?",
        [
            "Priložen račun jamči isplatu punog iznosa.",
            "Račun se može zamijeniti usmenom potvrdom kupnje.",
            "Bez priloženog računa nadoknada nije moguća.",
            "Zahtjevi s računom rješavaju se prije ostalih.",
        ],
        "Bez priloženog računa nadoknada nije moguća.",
        "hr-necessary-conditions-b2",
    ),
    AssessmentQuestion(
        "hr-v-b2-001",
        "vocabulary",
        "B2",
        "Kolegica je procijenila da će nova usluga imati tisuću korisnika. "
        "Tražite podatke koji podupiru tu brojku. Dopunite: "
        "„Možete li tu procjenu ___ rezultatima ankete?”",
        ["ublažiti", "odgoditi", "potkrijepiti", "zaprimiti"],
        "potkrijepiti",
    ),
    AssessmentQuestion(
        "hr-v-b2-002",
        "vocabulary",
        "B2",
        "Načuli ste da se natječaj ponavlja, no nadležni ured to još nije potvrdio. "
        "Koji prilog čuva taj status informacije: „Natječaj će ___ biti ponovljen”?",
        ["navodno", "službeno", "nesumnjivo", "zajamčeno"],
        "navodno",
    ),
    AssessmentQuestion(
        "hr-v-b2-003",
        "vocabulary",
        "B2",
        "Ured je evidentirao vaš dokument i dodijelio mu broj predmeta. "
        "O sadržaju se još nije odlučivalo. Koja riječ odgovara obavijesti "
        "„Vaš je zahtjev ___”?",
        ["odobren", "zaprimljen", "obustavljen", "odbijen"],
        "zaprimljen",
    ),
    AssessmentQuestion(
        "hr-v-b2-004",
        "vocabulary",
        "B2",
        "Dobavljač je ponudio isporuku za deset dana po cijeni od 800 eura. "
        "Vi predlažete 750 eura i dopuštate isporuku za petnaest dana. "
        "Što mu šaljete?",
        ["Žalbu na račun.", "Potvrdu narudžbe.", "Zahtjev za povrat.", "Protuponudu."],
        "Protuponudu.",
    ),
    AssessmentQuestion(
        "hr-v-b2-005",
        "vocabulary",
        "B2",
        "Stručnjakinja kaže: „Prema dosadašnjim mjerenjima uređaj troši manje, "
        "ali ispitivanje još nije završeno.” Što dodaje drugim dijelom rečenice?",
        [
            "Potvrdu konačnog rezultata.",
            "Objašnjenje uzroka uštede.",
            "Ispravak ranijeg mjerenja.",
            "Ogradu uz procjenu.",
        ],
        "Ogradu uz procjenu.",
    ),
    AssessmentQuestion(
        "hr-v-b2-006",
        "vocabulary",
        "B2",
        "Kolega za dva tjedna odlazi na dulji dopust. Trebate preuzeti njegove "
        "otvorene zadatke, pristupne upute i kontakte. Što dogovarate?",
        [
            "Ocjenjivanje njegova rada.",
            "Primopredaju poslova.",
            "Produljenje njegova ugovora.",
            "Objavu natječaja.",
        ],
        "Primopredaju poslova.",
    ),
    AssessmentQuestion(
        "hr-v-b2-007",
        "vocabulary",
        "B2",
        "Želite vikendom koristiti dvoranu oba dana, a druga skupina želi isto. "
        "Predlažete da vi koristite subotu, a oni nedjelju. Koji izraz opisuje takav dogovor?",
        [
            "Izvući stvar iz konteksta.",
            "Ostati pri svim zahtjevima.",
            "Naći se na pola puta.",
            "Prepustiti drugima cijeli termin.",
        ],
        "Naći se na pola puta.",
    ),
    AssessmentQuestion(
        "hr-v-b2-008",
        "vocabulary",
        "B2",
        "Ugovor ne predviđa naknadu organizatora za otkazivanje. "
        "Prostor ste već platili i novac vam se ne vraća. "
        "Koji izraz najbolje opisuje vaš položaj?",
        [
            "Snosite trošak najma.",
            "Odobravate povrat najma.",
            "Jamčite novu rezervaciju.",
            "Odgađate uplatu najma.",
        ],
        "Snosite trošak najma.",
    ),
    AssessmentQuestion(
        "hr-r-b2-001",
        "reading",
        "B2",
        "Pročitajte: „Knjižnica predlaže dulje radno vrijeme srijedom. Dio zaposlenika "
        "upozorava na manjak osoblja, a studenti podržavaju prijedlog. Uprava zato predlaže "
        "probno razdoblje od mjesec dana, bez ukidanja jutarnjih termina. Nakon toga "
        "usporedit će posjećenost s dodatnim troškovima.” Koja je svrha probnog razdoblja?",
        [
            "Pripremiti korisnike za već doneseno trajno ukidanje jutarnjih termina.",
            "Prikupiti podatke za odluku uz privremeno zadržavanje postojećih termina.",
            "Provjeriti mogu li studenti preuzeti smjene zaposlenika koji nedostaju.",
            "Utvrditi podržavaju li zaposlenici prijedlog prije početka javne rasprave.",
        ],
        "Prikupiti podatke za odluku uz privremeno zadržavanje postojećih termina.",
        "hr-cause-result-b2",
    ),
    AssessmentQuestion(
        "hr-r-b2-002",
        "reading",
        "B2",
        "Pročitajte: „Naslov portala glasi: Most se otvara u lipnju. U tekstu se, međutim, "
        "navodi izjava voditeljice radova: Ako vrijeme posluži i stigne naručena oprema, "
        "mogli bismo završiti do kraja lipnja. Za sada ne možemo potvrditi datum otvaranja.” "
        "Kako se naslov odnosi prema izjavi?",
        [
            "Zadržava uvjete i oprez koji su jasno navedeni u izjavi.",
            "Najavljuje kasnije otvaranje od onoga koje voditeljica jamči.",
            "Prenosi potvrđeni završetak radova, ali mijenja mjesec otvaranja.",
            "Prikazuje uvjetnu mogućnost sigurnije nego što je izvor dopušta.",
        ],
        "Prikazuje uvjetnu mogućnost sigurnije nego što je izvor dopušta.",
        "hr-reported-source-b2",
    ),
    AssessmentQuestion(
        "hr-r-b2-003",
        "reading",
        "B2",
        "Pročitajte: „U obavijesti piše da je raspored promijenjen te da su korisnici "
        "obaviješteni elektroničkom poštom. Nije navedeno tko je odlučio o izmjeni. "
        "Marta želi zatražiti obrazloženje, ali još ne želi osporavati odluku.” "
        "Koji je upit najprikladniji njezinoj namjeri?",
        [
            "Možete li me uputiti osobi nadležnoj za izmjenu rasporeda?",
            "Možete li potvrditi da je moj zahtjev za ukidanje izmjene prihvaćen?",
            "Možete li ostalim korisnicima poslati moju žalbu na novu satnicu?",
            "Možete li mi ponovno poslati obavijest na istu elektroničku adresu?",
        ],
        "Možete li me uputiti osobi nadležnoj za izmjenu rasporeda?",
        "hr-passive-agency-b2",
    ),
    AssessmentQuestion(
        "hr-r-b2-004",
        "reading",
        "B2",
        "Pročitajte: „Dobavljač nudi nižu cijenu pod uvjetom da uplatimo polovicu iznosa "
        "prije početka rada. Možemo to prihvatiti samo ako ugovor jasno uređuje povrat "
        "u slučaju neisporuke. Dobavljač zasad jamči rok, ali nije odgovorio na pitanje "
        "o povratu.” Što još treba razjasniti prije prihvaćanja ponude?",
        [
            "Hoće li se početak rada odgoditi do uplate cijelog iznosa.",
            "Želi li dobavljač zamijeniti popust duljim rokom isporuke.",
            "Hoće li ugovor zaštititi unaprijed uplaćeni iznos ako isporuka izostane.",
            "Pristaje li kupac na nižu cijenu bez prethodne uplate.",
        ],
        "Hoće li ugovor zaštititi unaprijed uplaćeni iznos ako isporuka izostane.",
        "hr-necessary-conditions-b2",
    ),
    AssessmentQuestion(
        "hr-r-b2-005",
        "reading",
        "B2",
        "Pročitajte: „Ne predlažem da se sve radionice presele na internet. "
        "Za teorijski dio to bi mnogima olakšalo sudjelovanje. Praktični rad s opremom "
        "treba ostati u učionici, a polaznicima bez odgovarajuće veze treba omogućiti "
        "dolazak i na teoriju.” Koji sažetak najvjernije prenosi prijedlog?",
        [
            "Praktični dio ostaje uživo, a dolazak na teoriju više neće biti moguć.",
            "Cijeli se program seli na internet čim se riješi pristup opremi.",
            "Predlaže se kombinacija oblika rada uz pristup onima s tehničkim ograničenjima.",
            "Teorija ostaje u učionici, a praktični dio prelazi u mrežni oblik.",
        ],
        "Predlaže se kombinacija oblika rada uz pristup onima s tehničkim ograničenjima.",
        "hr-negation-scope-b2",
    ),
    AssessmentQuestion(
        "hr-r-b2-006",
        "reading",
        "B2",
        "Pročitajte poruku: „Hvala na nacrtu. Uvod je jasan, ali za konačno odobrenje "
        "nedostaje usporedba troškova. Biste li je mogli dodati do četvrtka? Ako to "
        "nije izvedivo, molim vas da danas javite koji je najraniji mogući termin. "
        "Nacrt zasad nemojte slati klijentu.” Što primatelj treba učiniti "
        "ako ne može završiti do četvrtka?",
        [
            "Danas predložiti prvi izvedivi rok i zasad zadržati nacrt unutar tima.",
            "U četvrtak poslati klijentu postojeći nacrt uz napomenu o nedostatku.",
            "Danas zatražiti od klijenta da sam usporedi predložene troškove.",
            "Pričekati završetak usporedbe pa tek onda javiti da je rok pomaknut.",
        ],
        "Danas predložiti prvi izvedivi rok i zasad zadržati nacrt unutar tima.",
        "hr-professional-requests-b2",
    ),
    AssessmentQuestion(
        "hr-r-b2-007",
        "reading",
        "B2",
        "Pročitajte: „Stanari traže mir nakon dvadeset sati, a glazbena udruga traži "
        "prostor za večernje probe. Voditelj predlaže da probe radnim danima završe do "
        "osam navečer, a jedna subotnja proba mjesečno do devet navečer, uz prethodnu "
        "najavu. Stanari i udruga pristaju isprobati raspored.” Što je omogućilo dogovor?",
        [
            "Stanari su prihvatili kasniju probu svake subote uz prethodnu najavu.",
            "Udruga je dobila kasnije probe radnim danima uz raniji završetak subotom.",
            "Strane su prihvatile radne dane, a subotnji su termin ostavile za novi dogovor.",
            "Obje su strane prihvatile ograničenu prilagodbu svojih zahtjeva.",
        ],
        "Obje su strane prihvatile ograničenu prilagodbu svojih zahtjeva.",
        "hr-reformulation-b2",
    ),
    AssessmentQuestion(
        "hr-r-b2-008",
        "reading",
        "B2",
        "Pročitajte razgovor nakon dugog čekanja pred uredom: "
        "„Ivan: Ovim tempom ovdje ću dočekati mirovinu. "
        "Nika: Hoćeš da odemo ili samo kažeš da se red sporo miče? "
        "Ivan: Ne, ostanimo. Predugo sam čekao da sad odustanem.” "
        "Što Nika postiže svojim pitanjem?",
        [
            "Provjerava može li Ivan ostati u redu dok ona ode obaviti drugi posao.",
            "Razdvaja moguću namjeru odlaska od pretjeranog izraza nezadovoljstva.",
            "Traži procjenu preostalog čekanja kako bi mogla isplanirati ostatak dana.",
            "Zaključuje da je Ivan već odustao i traži razlog njegove odluke.",
        ],
        "Razdvaja moguću namjeru odlaska od pretjeranog izraza nezadovoljstva.",
        "hr-reformulation-b2",
    ),
]
