"""Croatian C1 grammar for attribution, agency, discourse and interaction."""

from app.data._types import GrammarExample, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "hr-source-attribution-c1",
        "Prema izvješću, navodno i kako tvrdi: izvor informacije",
        "C1",
        "Izvor i pouzdanost",
        "Pripišite tvrdnju izvoru bez preuzimanja njegove procjene kao dokazane činjenice.",
        "Izrazi prema izvješću i kako navodi autor pokazuju odakle tvrdnja potječe. "
        "Navodno označuje prenošenje informacije uz odmak, ali samo po sebi ne dokazuje "
        "da je tvrdnja netočna. U izvještavanju je imenovani izvor korisniji od neodređene "
        "glasine. Zadržite izvorne ograde poput možda ili mogao bi.",
        structure="Prema + dativ; kako + glagol izvještavanja; navodno + tvrdnja",
        rules=[
            "Prema procjeni stručnjaka nije isto što i prema potvrđenim rezultatima.",
            "Pri prenošenju tvrdnje ne uklanjajte izvor ni ogradu koja određuje njezinu sigurnost.",
            "Navodno može izraziti sumnju; tu sumnju ne pripisujte automatski izvornom govorniku.",
        ],
        examples=[
            GrammarExample(
                "Prema procjeni konzervatorice, zid bi mogao potjecati iz petnaestog stoljeća.",
                note="Izvor je imenovan, a datacija ostaje moguća, ne potvrđena.",
            ),
            GrammarExample(
                "Rukopis je navodno pronađen u privatnoj zbirci; muzej još provjerava njegovo podrijetlo."
            ),
        ],
        related=["hr-evidential-modality-c1"],
    ),
    GrammarTopic(
        "hr-evidential-modality-c1",
        "Mora biti, moglo bi biti i po svemu sudeći",
        "C1",
        "Stupnjevi sigurnosti",
        "Razlikujte zaključivanje na temelju znakova od obveze i provjerene činjenice.",
        "Mora biti u rečenici Mora biti da je došlo do zabune izražava snažan zaključak "
        "govornika, a ne nečiju obvezu. Moglo bi biti ostavlja više prostora drugim "
        "objašnjenjima. Po svemu sudeći upućuje na raspoložive znakove; ne zamjenjuje "
        "izravnu provjeru. Snaga procjene ovisi i o navedenim dokazima.",
        rules=[
            "Modalno značenje tumačite prema situaciji, a ne samo prema glagolu morati.",
            "Nemojte sažeti moglo bi biti izrazom dokazano je.",
            "Nužnost radnje i sigurnost zaključka dvije su različite uporabe modalnosti.",
        ],
        examples=[
            GrammarExample(
                "Svjetla su ugašena, a vrata zaključana; po svemu sudeći, kustosica je već otišla."
            ),
            GrammarExample(
                "Moglo bi biti da je senzor neispravan, ali najprije provjerimo napajanje."
            ),
        ],
        related=["hr-negation-scope-c1"],
    ),
    GrammarTopic(
        "hr-negation-scope-c1",
        "Nije dokazano da i dokazano je da nije",
        "C1",
        "Doseg negacije",
        "Razlikujte nedostatak potvrde, pobijanje tvrdnje i ograničenu primjenjivost.",
        "U rečenici Nije dokazano da je voda onečišćena niječe se postojanje dokaza. "
        "Voda time nije proglašena čistom. Dokazano je da voda nije onečišćena prenosi "
        "drukčiji nalaz. Slično tome, nisu svi prijedlozi prihvaćeni ne znači da nije "
        "prihvaćen nijedan prijedlog. Položaj negacije određuje opseg poricanja.",
        rules=[
            "Razlikujte negaciju glavnog predikata od negacije sadržaja zavisne rečenice.",
            "Nisu svi dopušta da neki jesu; nijedan isključuje sve članove skupa.",
            "Izraz ne mora značiti osporava nužnost zaključka, a ne nužno njegovu mogućnost.",
        ],
        examples=[
            GrammarExample(
                "Nije potvrđeno da je zvuk snimljen na otoku; mjesto snimanja još se provjerava."
            ),
            GrammarExample(
                "Veći broj posjetitelja ne mora značiti veći prihod ako su ulaznice besplatne."
            ),
        ],
        related=["hr-evidential-modality-c1"],
    ),
    GrammarTopic(
        "hr-conditional-stance-c1",
        "Kondicional: prijedlog, ograda i neostvareni ishod",
        "C1",
        "Modalnost u pregovorima",
        "Prepoznajte izražava li kondicional mogućnost, obzirnost ili zamišljenu posljedicu.",
        "Mogli bismo produljiti najam otvara mogućnost, dok produljit ćemo najam najavljuje "
        "odluku. Kondicional sam ne određuje vrijeme: prošli se neostvareni ishod može "
        "jasno izraziti vremenskim kontekstom, primjerice Da smo jučer znali, drukčije "
        "bismo postupili. Oblike bih, bi, bismo i biste uskladite s osobom.",
        rules=[
            "Ublažen prijedlog nemojte u zapisniku pretvoriti u prihvaćenu obvezu.",
            "Vrijeme zamišljene radnje odredite iz cijele rečenice i konteksta.",
            "U prvom licu množine upotrijebite bismo: razmotrili bismo, a ne mi bi razmotrili.",
        ],
        examples=[
            GrammarExample("Mogli bismo preuzeti dio troškova ako dogovorimo dulji rok otplate."),
            GrammarExample(
                "Da smo jučer dobili obavijest, rezervirali bismo drugu dvoranu.",
                note="Jučerašnja prilika nije ostvarena; kondicional nije najava buduće rezervacije.",
            ),
        ],
        related=["hr-necessary-conditions-c1"],
    ),
    GrammarTopic(
        "hr-hypothetical-concession-c1",
        "Čak i kad bi: dopusnost zamišljene okolnosti",
        "C1",
        "Hipotetska dopusnost",
        "Izrazite zaključak koji ostaje na snazi i u zamišljenom nepovoljnom slučaju.",
        "Čak i kad bi cijena pala, ne bismo kupili prostor ne tvrdi da je cijena pala. "
        "Govornik razmatra tu mogućnost i odbacuje očekivanu posljedicu. Nasuprot tome, "
        "iako je cijena pala prikazuje pad cijene kao činjenicu. U pregovorima je ta "
        "razlika važna: hipotetska formulacija sama ne govori je li ustupak već ponuđen "
        "ili prihvaćen.",
        rules=[
            "Nemojte hipotetsku okolnost prenositi kao ostvarenu činjenicu.",
            "Čak i pojačava neočekivanost, a kondicional održava zamišljeni okvir.",
            "U glavnoj rečenici jasno navedite što bi unatoč toj okolnosti ostalo isto.",
        ],
        examples=[
            GrammarExample(
                "Čak i kad bi općina platila prijevoz, dio učenika ne bi mogao krenuti prije sedam."
            ),
            GrammarExample(
                "Čak i da dobijemo dodatni tjedan, ne bismo mogli obnoviti cijeli brod."
            ),
        ],
        related=["hr-conditional-stance-c1", "hr-concessive-argument-c1"],
    ),
    GrammarTopic(
        "hr-necessary-conditions-c1",
        "Samo ako, pod uvjetom da i osim ako",
        "C1",
        "Uvjeti i iznimke",
        "Razlikujte nužan uvjet, uvjetovani pristanak i iznimku od dogovorenog postupka.",
        "Samo ako dobijemo dozvolu, otvorit ćemo terasu određuje dozvolu kao nužan uvjet; "
        "ne jamči da drugih zapreka nema. Pristajemo pod uvjetom da preuzmete osiguranje "
        "izriče uvjetovani pristanak. Osim ako uvodi iznimku od najavljenoga postupka, "
        "pa se njegova odsutnost ne smije zamijeniti prisutnošću.",
        rules=[
            "Sačuvajte samo ako pri preoblikovanju nužnog uvjeta.",
            "Razlikujte možemo prihvatiti od prihvatit ćemo.",
            "Kod osim ako utvrdite osnovno pravilo i okolnost koja ga mijenja.",
        ],
        examples=[
            GrammarExample(
                "Zahtjev ćemo razmatrati samo ako sadrži suglasnost vlasnika; provjerit ćemo i troškove."
            ),
            GrammarExample("Proba ostaje u dvorištu, osim ako ravnateljica najavi radove."),
        ],
        related=["hr-conditional-stance-c1"],
    ),
    GrammarTopic(
        "hr-nominalisation-agents-c1",
        "Glagolske imenice i očuvanje uloga",
        "C1",
        "Sažeto izražavanje",
        "Preoblikujte imenovani proces u rečenicu bez zamjene predlagatelja i izvršitelja.",
        "Glagolske imenice sažimaju radnje, ali niz genitiva može zamagliti odnose. "
        "Prijedlog udruge za obnovu mosta govori tko je predlagatelj, ne nužno tko će "
        "obnoviti most. Pri raspisivanju utvrdite tko predlaže, na koga se radnja odnosi "
        "i je li odluka već donesena. Ne dodajte izvršitelja kojeg izvor ne navodi.",
        rules=[
            "Predlaganje, odobravanje i provođenje nemojte tretirati kao istu radnju.",
            "Višeznačan genitiv razjasnite zavisnom rečenicom ili izričitim imenovanjem uloge.",
            "Neodređen izvršitelj treba ostati neodređen i u jasnijoj inačici.",
        ],
        examples=[
            GrammarExample(
                "Odbor razmatra prijedlog stanara da se obnovi pročelje; izvođač još nije odabran."
            ),
            GrammarExample(
                "Ravnateljica je zatražila provjeru obračuna, odnosno zatražila je da se obračun provjeri."
            ),
        ],
        related=["hr-passive-accountability-c1"],
    ),
    GrammarTopic(
        "hr-passive-accountability-c1",
        "Pasiv i bezličnost: što znamo o odgovornosti?",
        "C1",
        "Radnja i izvršitelj",
        "Odvojite izvršenu radnju od odluke o njoj i ne dopisujte nepoznatog izvršitelja.",
        "Obrasci je odobren i odlučeno je ističu radnju ili odluku, a izvršitelj može ostati "
        "neimenovan. Dokument je odobren ne znači da je provedba završena. Ako izvor "
        "izvršitelja navodi, aktivno preoblikovanje treba ga sačuvati. Ako ga ne navodi, "
        "jasniji tekst može izričito reći da podatak o njemu nedostaje.",
        rules=[
            "Iz gramatičkog subjekta pasivne rečenice nemojte izvesti izvršitelja radnje.",
            "Razlikujte donesenu odluku od radnje predviđene tom odlukom.",
            "Aktiv je često pregledniji, ali nije opravdanje za izmišljanje odgovorne osobe.",
        ],
        examples=[
            GrammarExample("Odlučeno je da se natječaj ponovi; novi poziv još nije objavljen."),
            GrammarExample(
                "Zahtjev je odbijen, no u obavijesti nije navedeno tko je donio odluku."
            ),
        ],
        related=["hr-nominalisation-agents-c1"],
    ),
    GrammarTopic(
        "hr-participle-agents-c1",
        "Glagolski prilozi: zajednički subjekt i vremenski odnos",
        "C1",
        "Povezivanje radnji",
        "Sažmite radnje istoga sudionika bez pogrešnog pripisivanja i promjene slijeda.",
        "U rečenici Pregledavši nacrt, arhitektica je poslala primjedbe obje radnje "
        "pripadaju arhitektici. Glagolski prilog prošli obično označuje prethodnu radnju; "
        "sadašnji prikazuje istodobnost ili okolnost. Kada radnje imaju različite "
        "subjekte, zavisna rečenica jasnije i pravilno čuva njihove uloge.",
        rules=[
            "Subjekt glagolskog priloga mora odgovarati subjektu radnje uz koju stoji.",
            "Pri preoblikovanju sačuvajte prethodnost ili istodobnost radnji.",
            "Za različite izvršitelje upotrijebite punu rečenicu s izričitim subjektom.",
        ],
        examples=[
            GrammarExample("Čitajući zapisnik, tajnica je bilježila nejasne obveze."),
            GrammarExample(
                "Nakon što je arhitektica pregledala nacrt, investitor je odobrio izmjene.",
                note="Dva su izvršitelja, pa se prva radnja ne sažima prilogom pregledavši.",
            ),
        ],
        related=["hr-temporal-perspective-c1"],
    ),
    GrammarTopic(
        "hr-relative-reference-c1",
        "Koji i što: jasna veza s osobom ili cijelom tvrdnjom",
        "C1",
        "Upućivanje u tekstu",
        "Razlikujte dopunu uz imenicu od komentara na prethodno izrečenu situaciju.",
        "U rečenici Marta je pronašla pismo koje je tražila odnosna rečenica određuje "
        "pismo. Marta je pronašla pismo, što nas je iznenadilo upućuje na cijeli događaj. "
        "Oblik zamjenice koji usklađuje rod i broj s imenicom, a padež dobiva prema "
        "svojoj ulozi u odnosnoj rečenici. Nejasne veze razriješite ponavljanjem imenice.",
        rules=[
            "Padež odnosne zamjenice ne mora biti jednak padežu imenice na koju upućuje.",
            "Što može upućivati na prethodnu tvrdnju, ali u drugim konstrukcijama i na imenicu.",
            "Kad su moguća dva prethodnika, navedite točno ime ili događaj.",
        ],
        examples=[
            GrammarExample("Razgovarali smo s vodičicom kojoj je gost predao pronađenu torbu."),
            GrammarExample(
                "Vodičica je otkazala obilazak, što je iznenadilo organizatora.",
                note="Organizatora je iznenadilo otkazivanje, a ne sama vodičica.",
            ),
        ],
        related=["hr-cohesive-summary-c1"],
    ),
    GrammarTopic(
        "hr-clitic-information-c1",
        "Zanaglasnice i isticanje sugovornika",
        "C1",
        "Red riječi i obavijesno ustrojstvo",
        "Povežite nenaglašene oblike s prirodnim redom riječi, a kontrast izrazite naglašenim oblicima.",
        "Nenaglašeni oblici poput mi, ga i je oslanjaju se na naglašenu cjelinu ispred "
        "sebe i ne mogu sami nositi kontrastni naglasak. U skupini mi ga dativ prethodi "
        "akuzativu; pomoćno je dolazi iza zamjeničkih zanaglasnica. Želite li suprotstaviti "
        "primatelje, upotrijebite meni, a ne pokušaj isticanja nenaglašenoga mi.",
        rules=[
            "Zanaglasnicu ne stavljajte na početak samostalne rečenice.",
            "Ne određujte položaj mehaničkim brojenjem riječi; važna je naglasna cjelina.",
            "Naglašeni oblik zamjenice može istaknuti kontrast bez promjene referenta.",
        ],
        examples=[
            GrammarExample("Ivan mi ga je vratio tek nakon sastanka."),
            GrammarExample(
                "Meni je vratio ključ, a Ani propusnicu.",
                note="Naglašeno meni suprotstavlja primatelje; predmeti su jasno imenovani.",
            ),
        ],
        related=["hr-relative-reference-c1"],
    ),
    GrammarTopic(
        "hr-temporal-perspective-c1",
        "Pogled unatrag u pripovijedanju",
        "C1",
        "Vremenski odnosi",
        "Odvojite slijed priče od redoslijeda kojim pripovjedač iznosi informacije.",
        "Perfekt s izrazima već, ranije i prije toga može jasno prikazati radnju koja "
        "prethodi drugoj prošloj radnji. Pluskvamperfekt, primjerice bio je otišao, "
        "dodatno ističe prethodnost, ali nije obvezan kada je odnos već jasan. "
        "Pripovjedni prezent približava događaj slušatelju; promjena vremena sama po sebi "
        "ne premješta stvarni događaj u sadašnjost.",
        rules=[
            "Vremenske odnose utvrdite iz veznika, priloga i konteksta, ne samo iz vremena.",
            "Povratak na raniji događaj označite tako da slušatelj može pratiti slijed.",
            "Pripovjedni prezent prikladan je za živu priču, ali službeni zapis traži dosljednost.",
        ],
        examples=[
            GrammarExample("Kad smo stigli na rivu, trajekt je već bio isplovio."),
            GrammarExample(
                "Jučer otvorim kofer, a unutra tuđe stvari! Tek tada shvatim da sam zamijenila prtljagu."
            ),
        ],
        related=["hr-participle-agents-c1"],
    ),
    GrammarTopic(
        "hr-concessive-argument-c1",
        "Premda, unatoč i ipak: priznati činjenicu, zadržati prigovor",
        "C1",
        "Argumentacija",
        "Priznajte relevantnu okolnost bez prihvaćanja zaključka koji se iz nje očekuje.",
        "Premda uvodi činjenicu koja bi mogla voditi drukčijem ishodu. Unatoč s dativom "
        "sažima istu vrstu odnosa. Ipak u nastavku označuje da govornikov zaključak ostaje "
        "na snazi. Priznanje da je mjera korisna ne podrazumijeva pristanak na svaki način "
        "njezine provedbe.",
        rules=[
            "Unatoč upravlja dativom: unatoč protivljenju, unatoč primjedbama.",
            "Dopusnu činjenicu nemojte pretvoriti u hipotetsku okolnost bez razloga.",
            "Jasno odvojite ono što priznajete od onoga čemu prigovarate.",
        ],
        examples=[
            GrammarExample("Premda podržavamo obnovu trga, protivimo se uklanjanju svih stabala."),
            GrammarExample("Unatoč većoj posjećenosti, knjižnica još nema dovoljno sredstava."),
        ],
        related=["hr-hypothetical-concession-c1", "hr-scalar-focus-c1"],
    ),
    GrammarTopic(
        "hr-scalar-focus-c1",
        "Samo, čak i i ne toliko koliko: opseg i težište",
        "C1",
        "Isticanje i ograničavanje",
        "Odredite na što se odnosi ograničenje ili naglasak prije nego što sažmete poruku.",
        "Samo uz različite dijelove rečenice mijenja opseg ograničenja: samo je Ana "
        "glasovala za prijedlog razlikuje Anu od drugih osoba, a Ana je glasovala samo "
        "za prvi prijedlog razlikuje prijedloge. Čak i označuje neočekivano uključivanje. "
        "Ne toliko X koliko Y pomiče težište na Y, ali ne mora potpuno isključiti X.",
        rules=[
            "Pri premještanju samo provjerite ostaje li ograničenje vezano uz isti sadržaj.",
            "Čak i nije neutralna zamjena za i jer uključuje govornikovo očekivanje.",
            "Ne toliko ne znači nužno nimalo.",
        ],
        examples=[
            GrammarExample(
                "Ovdje nije problem toliko broj turista koliko raspored njihovih dolazaka."
            ),
            GrammarExample("Čak su i protivnici prvog nacrta podržali izmijenjeni prijedlog."),
        ],
        related=["hr-negation-scope-c1"],
    ),
    GrammarTopic(
        "hr-cause-inference-c1",
        "Jer, stoga i naime: uzrok ili obrazloženje zaključka",
        "C1",
        "Logički odnosi",
        "Razlikujte ono što uzrokuje događaj od onoga što opravdava vaše tumačenje.",
        "Jer može navesti uzrok događaja ili razlog za govornikov zaključak. U iskazu "
        "Netko je unutra jer se čuju koraci koraci nisu uzrok nečije prisutnosti, nego "
        "znak na temelju kojeg zaključujemo. Stoga najavljuje posljedicu ili zaključak, "
        "a naime naknadno obrazlaže prethodnu tvrdnju.",
        rules=[
            "Pri sažimanju dokaz za zaključak nemojte pretvoriti u uzrok događaja.",
            "Naime dodaje objašnjenje; stoga usmjerava prema onome što iz njega slijedi.",
            "Spojni izraz ne čini zaključak opravdanim ako podaci nisu dostatni.",
        ],
        examples=[
            GrammarExample("Staza je zatvorena jer je odron oštetio ogradu."),
            GrammarExample(
                "Staza je vjerojatno zatvorena; naime, na ulazu su postavljene zapreke."
            ),
        ],
        related=["hr-evidential-modality-c1", "hr-concessive-argument-c1"],
    ),
    GrammarTopic(
        "hr-diplomatic-questions-c1",
        "Biste li i ne bismo li: pitanje kao prijedlog",
        "C1",
        "Uljudnost i pregovaranje",
        "Predložite promjenu bez prikrivanja vlastitog zahtjeva ili nametanja tuđeg pristanka.",
        "Biste li mogli poslati nacrt oblikuje molbu kao pitanje o mogućnosti. Ne bismo "
        "li mogli pomaknuti termin često nudi rješenje, a ne traži potvrdu nemogućnosti. "
        "Takva pitanja mogu i pritiskati sugovornika ako sugeriraju da je odgovor "
        "samorazumljiv. U osjetljivoj situaciji ostavite prostor za odbijanje.",
        rules=[
            "Upitni oblik može obavljati funkciju molbe, prijedloga ili prigovora.",
            "Negativno pitanje tumačite prema namjeri i nastavku razgovora.",
            "Formalna uljudnost ne mijenja stvarni rok ni opseg traženog posla.",
        ],
        examples=[
            GrammarExample("Biste li mogli poslati sažetak do petka ili vam treba još vremena?"),
            GrammarExample(
                "Ne bismo li mogli prvo čuti stanare pa tek onda glasovati o prijedlogu?"
            ),
        ],
        related=["hr-conditional-stance-c1", "hr-reformulation-repair-c1"],
    ),
    GrammarTopic(
        "hr-reformulation-repair-c1",
        "Točnije, odnosno i nisam mislio da: popravak poruke",
        "C1",
        "Razjašnjavanje u razgovoru",
        "Ispravite vlastitu formulaciju i navedite što se mijenja, a što ostaje na snazi.",
        "Točnije najavljuje preciziranje, a drugim riječima preoblikovanje iste poruke. "
        "Odnosno može razjašnjavati, ispravljati ili povezivati odgovarajuće članove, "
        "pa nejasan odnos radije izrazite punom rečenicom. Kad se nakon primjedbe "
        "mijenja stav, priznajte promjenu umjesto da je prikazujete kao puko ponavljanje.",
        rules=[
            "Parafraza treba očuvati sudionike, uvjete i stupanj sigurnosti.",
            "Razlikujte ispravak omaške od promjene odluke.",
            "U popravku izričito navedite pogrešno shvaćeni dio, bez napada na sugovornika.",
        ],
        examples=[
            GrammarExample(
                "Rekao sam da možemo završiti do petka; točnije, do petka možemo predati nacrt."
            ),
            GrammarExample(
                "Nisam mislio da vi kasnite, nego da nam rokovi dobavljača ostavljaju premalo prostora."
            ),
        ],
        related=["hr-register-shift-c1"],
    ),
    GrammarTopic(
        "hr-contextual-irony-c1",
        "Baš sjajno: kada pohvala izražava prigovor",
        "C1",
        "Ironija i humor",
        "Prepoznajte nesklad između doslovne pohvale i situacije te primjereno provjerite ton.",
        "Izraz Baš smo se usrećili može biti iskren ili ironičan. Značenje nastaje iz "
        "odnosa riječi, intonacije, zajedničkog iskustva i neposrednog događaja. U pisanoj "
        "poruci nedostaje dio tih znakova. Ironiju zato ne zaključujte samo iz riječi baš "
        "ili navodnika; pri dvojbi neutralno provjerite namjeru.",
        rules=[
            "Doslovno pozitivna rečenica u nepovoljnoj situaciji može prenositi kritiku.",
            "Humor nije nužno napad na sugovornika; utvrdite na što je usmjeren.",
            "Odgovor prilagodite odnosu i situaciji, osobito ako je netko već povrijeđen.",
        ],
        examples=[
            GrammarExample(
                "Nakon trećeg kvara projektora voditelj kaže: Baš nas tehnika danas služi!",
                note="Pohvala je u neskladu s ponovljenim kvarom i izražava frustraciju.",
            ),
            GrammarExample(
                "Kad kažeš da je sastanak bio nezaboravan, misliš na dobru raspravu ili na onu svađu?"
            ),
        ],
        related=["hr-reformulation-repair-c1"],
    ),
    GrammarTopic(
        "hr-reported-commitments-c1",
        "Predložila je, obećala je i pristala je: tuđe obveze",
        "C1",
        "Prenošenje govora",
        "Razlikujte tuđu zamisao, spremnost i obećanje kada posredujete između strana.",
        "Glagol izvještavanja određuje kako predstavljamo tuđi govorni čin. Predložila "
        "je da nabavimo opremu ne znači da ju je obećala nabaviti. Obećala je poslati "
        "račun pripisuje slanje istoj osobi; zamjena infinitiva zavisnom rečenicom "
        "mora sačuvati taj subjekt. U hrvatskom se vremena ne pomiču automatski samo "
        "zato što je glagol izvještavanja u prošlosti.",
        rules=[
            "Glagol obećati upotrijebite samo kada izvor doista preuzima obvezu.",
            "Prilagodite osobne i vremenske odrednice perspektivi izvjestitelja.",
            "Sačuvajte uvjet uz pristanak, čak i kada sažimate vrlo kratko.",
        ],
        examples=[
            GrammarExample(
                "Predstavnica stanara rekla je da bi prihvatili radove ako ulaz ostane prohodan."
            ),
            GrammarExample(
                "Jučer je Lea obećala poslati račun danas; nije rekla da će ga poslati računovođa."
            ),
        ],
        related=["hr-source-attribution-c1", "hr-nominalisation-agents-c1"],
    ),
    GrammarTopic(
        "hr-register-shift-c1",
        "Ista poruka za susjeda i za službeni dopis",
        "C1",
        "Registar",
        "Promijenite stil poruke bez promjene uvjeta, rokova ili odnosa među sudionicima.",
        "Formalni dopis može tražiti izričito imenovane sudionike i preglednu strukturu, "
        "ali ne mora biti prepun glagolskih imenica. Razgovorno Možemo uskočiti ako nam "
        "javite do srijede može postati Možemo preuzeti zadatak pod uvjetom da nas "
        "obavijestite do srijede. Zamjena možemo s preuzet ćemo promijenila bi obvezu, "
        "a ne samo stil.",
        rules=[
            "Pri promjeni registra očuvajte mogućnost, obvezu i eventualnu rezervu.",
            "Idiome zamijenite jasnim opisom radnje kada primatelj možda ne dijeli isti kontekst.",
            "U formalnom tekstu uklonite nejasnoće, ne nužno sve osobne glagolske oblike.",
        ],
        examples=[
            GrammarExample(
                "Nemamo još zeleno svjetlo. — Još nismo dobili odobrenje za početak radova."
            ),
            GrammarExample(
                "Mogli bismo uskočiti u petak. — Postoji mogućnost da u petak preuzmemo zamjenu."
            ),
        ],
        related=["hr-reported-commitments-c1", "hr-reformulation-repair-c1"],
    ),
    GrammarTopic(
        "hr-cohesive-summary-c1",
        "Pritom, s druge strane i takav prijedlog: povezani sažetak",
        "C1",
        "Kohezija",
        "Povežite stavove tako da se jasno vidi što je zajedničko, a što ostaje sporno.",
        "Pritom povezuje okolnost s prethodno opisanom radnjom, dok s druge strane "
        "uvodi drugu perspektivu ili protuargument. Izrazi takav prijedlog i ta obveza "
        "traže prepoznatljiv prethodnik. U sažetku pregovora ponavljanje naziva prijedloga "
        "može biti bolje od kratke zamjenice ako su spomenute dvije mogućnosti.",
        rules=[
            "Poveznicu odaberite prema stvarnom odnosu tvrdnji, ne radi stilske raznolikosti.",
            "Odobrenje jednog uvjeta nemojte sažeti kao prihvaćanje cijelog prijedloga.",
            "Uz nejasno to navedite radnju, odluku ili obvezu na koju upućujete.",
        ],
        examples=[
            GrammarExample(
                "Stanari podržavaju obnovu. Pritom traže da im tijekom radova ostane dostupan ulaz."
            ),
            GrammarExample(
                "Izvođač nudi kraći rok, a stanari traže tiše strojeve. Taj zahtjev za tišim "
                "strojevima još nije prihvaćen."
            ),
        ],
        related=["hr-relative-reference-c1", "hr-reported-commitments-c1"],
    ),
]
