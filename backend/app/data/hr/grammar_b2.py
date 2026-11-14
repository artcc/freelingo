"""Croatian B2 grammar: scope, stance and practical extended discourse."""

from app.data._types import GrammarExample, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "hr-concession-b2",
        "Dopuštanje: iako, premda i unatoč",
        "B2",
        "Složena rečenica",
        "Priznajte okolnost koja ne sprječava neočekivani ishod.",
        "Dopusna rečenica uvodi okolnost zbog koje bismo očekivali drukčiji rezultat: "
        "Iako je projekt skup, podržavamo ga. Iako i premda uvode rečenicu, dok unatoč "
        "stoji uz imenski izraz u dativu. Izraz čak i ako otvara zamišljen slučaj; "
        "sam po sebi ne potvrđuje da se taj slučaj ostvario.",
        rules=[
            "Uz unatoč upotrijebite dativ: unatoč kašnjenju, unatoč poteškoćama.",
            "Razlikujte priznatu činjenicu uz iako od mogućeg uvjeta uz čak i ako.",
            "Dopusnu rečenicu odvojite zarezom: Iako se ne slažemo, možemo surađivati.",
        ],
        examples=[
            GrammarExample(
                "Premda je dvorana mala, u njoj se mogu održavati radionice.",
                note="Mala površina priznata je činjenica, ali ne isključuje predloženu namjenu.",
            ),
            GrammarExample(
                "Unatoč protivljenju dijela stanara, prijedlog je prihvaćen.",
                note="Imenica protivljenje stoji u dativu; odluka je donesena usprkos otporu.",
            ),
            GrammarExample(
                "Čak i ako ne dobijemo potporu, nastavit ćemo projekt.",
                note="Govornik se obvezuje nastaviti i u nepovoljnome mogućem slučaju.",
            ),
        ],
        related=["hr-hypothetical-conditions-b2", "hr-contrast-b2"],
    ),
    GrammarTopic(
        "hr-contrast-b2",
        "Suprotnost i ispravak: dok, međutim i nego",
        "B2",
        "Povezivanje tvrdnji",
        "Razlikujte usporedbu dvaju stajališta od ispravljanja pogrešne tvrdnje.",
        "Dok može uspoređivati istodobne, ali suprotne pojave: Jedni traže park, dok "
        "drugi žele parkiralište. Međutim uvodi obrat u odnosu na prethodno očekivanje. "
        "Konstrukcija ne X, nego Y odbacuje X i zamjenjuje ga s Y; ne znači samo da "
        "među njima postoji razlika. Dok u drugim kontekstima označuje vrijeme.",
        rules=[
            "Za izričito ispravljanje upotrijebite nije X, nego Y i sačuvajte isti predmet rasprave.",
            "Kod dok iz sadržaja provjerite je li riječ o vremenu ili usporedbi.",
            "Međutim ne pretvara sljedeću tvrdnju u dokaz; njime se označuje odnos u tekstu.",
        ],
        examples=[
            GrammarExample(
                "Problem nije cijena, nego nedostatak prostora.",
                note="Govornik odbacuje jednu dijagnozu problema i nudi drugu.",
            ),
            GrammarExample(
                "Centar ima dobru vezu tramvajem, dok je pristup iz predgrađa slabiji.",
                note="Dok uspoređuje dostupnost dvaju područja, a ne trajanje radnji.",
            ),
        ],
        related=["hr-concession-b2", "hr-discourse-markers-b2"],
    ),
    GrammarTopic(
        "hr-cause-result-b2",
        "Uzrok, posljedica i zaključak",
        "B2",
        "Argumentacija",
        "Odvojite razlog događaja od zaključka koji izvodite iz podataka.",
        "Budući da i zato što uvode uzrok, a stoga i zato upućuju na posljedicu ili "
        "zaključak. Veza toliko… da opisuje intenzitet s posljedicom. Riječ dakle može "
        "označiti zaključivanje, ali njegova valjanost ovisi o razlozima u tekstu. "
        "Sama vremenska blizina dvaju događaja ne dokazuje uzročnost.",
        rules=[
            "Ne zamjenjujte uzrok i posljedicu pri sažimanju argumenta.",
            "Zbog povežite s genitivom kada navodite imenski uzrok: zbog radova.",
            "U konstrukciji toliko… da navedite posljedicu izraženog intenziteta.",
        ],
        examples=[
            GrammarExample(
                "Budući da je most zatvoren, autobus vozi obilazno.",
                note="Zatvaranje mosta navedeni je razlog promjene trase.",
            ),
            GrammarExample(
                "Odaziv je bio toliko velik da smo otvorili dodatnu skupinu.",
                note="Dodatna skupina posljedica je velikog broja prijava.",
            ),
        ],
        related=["hr-discourse-markers-b2", "hr-proportional-comparison-b2"],
    ),
    GrammarTopic(
        "hr-reported-source-b2",
        "Tuđe riječi i odgovornost za tvrdnju",
        "B2",
        "Prenošenje informacija",
        "Prenesite tko nešto tvrdi i koliko je izvor siguran.",
        "Reći, tvrditi, potvrditi i pretpostaviti različito predstavljaju tuđu izjavu. "
        "Prema izvješću navodi dokument kao izvor, a navodno označuje informaciju za "
        "koju se govornik ne obvezuje da je provjerena. Pri prepričavanju ne pretvarajte "
        "pretpostavku u potvrdu niti tuđe obećanje u već ostvaren rezultat.",
        rules=[
            "Sačuvajte ogradu iz izvornog iskaza: možda ne smije postati sigurno.",
            "Navedite izvor kada je važno razlikovati vlastito znanje od prenesene tvrdnje.",
            "Glagol tvrditi sam po sebi ne znači da je tvrdnja ni dokazana ni opovrgnuta.",
        ],
        examples=[
            GrammarExample(
                "Voditelj procjenjuje da će radovi vjerojatno završiti u lipnju.",
                note="I procjenjuje i vjerojatno čuvaju nesigurnost prognoze.",
            ),
            GrammarExample(
                "Prema zapisniku, odbor je prihvatio prijedlog bez izmjena.",
                note="Zapisnik je izričito naveden kao izvor informacije.",
            ),
        ],
        related=["hr-temporal-perspective-b2", "hr-epistemic-modality-b2"],
    ),
    GrammarTopic(
        "hr-temporal-perspective-b2",
        "Vremenska perspektiva u neupravnom govoru",
        "B2",
        "Prenošenje informacija",
        "Uskladite vrijeme, mjesto i osobe s trenutkom prepričavanja.",
        "Hrvatski nema obvezno pomicanje glagolskih vremena unatrag nakon prošlog "
        "glagola govorenja. U rečenici Rekla je da radi u školi prezent je moguć. "
        "Izbor vremena prati vremenski odnos i smisao. Izrazi danas, sutra i ovdje "
        "mogu se promijeniti kako novi slušatelj ne bi pogrešno odredio vrijeme ili mjesto.",
        rules=[
            "Ne mijenjajte prezent u prošlo vrijeme samo zato što prethodi rekla je.",
            "Kad se dan prepričavanja promijeni, upotrijebite datum ili naziv dana ako treba.",
            "Prilagodite osobne zamjenice stvarnim sudionicima, a ne samo obliku citata.",
        ],
        examples=[
            GrammarExample(
                "U ponedjeljak je Ana rekla da će nacrt poslati u utorak.",
                note="Pri kasnijem prepričavanju utorak jasno prenosi njezino tadašnje sutra.",
            ),
            GrammarExample(
                "Marko je rekao da živi u Splitu.",
                note="Prezent u zavisnoj rečenici nije gramatička pogreška nakon rekao je.",
            ),
        ],
        related=["hr-reported-source-b2"],
    ),
    GrammarTopic(
        "hr-epistemic-modality-b2",
        "Procjena sigurnosti: mora da, možda i mogao bi",
        "B2",
        "Modalnost",
        "Prepoznajte zaključak, mogućnost i obvezu.",
        "Mora da je zaboravio izražava snažnu pretpostavku, a ne nečiju obvezu da "
        "zaboravi. Mora poslati račun obično znači obvezu. Mogao bi kasniti može biti "
        "procjena mogućeg razvoja, dok pitanje Bi li mogao doći? često služi kao molba. "
        "Namjeru određuju kontekst i vrsta iskaza.",
        rules=[
            "Razlikujte procjenu govornika od potvrde na temelju provjerenih podataka.",
            "Možda i vjerojatno ne izražavaju isti stupanj sigurnosti.",
            "Ne tumačite svaki kondicional kao nestvaran uvjet; može ublažavati prognozu ili molbu.",
        ],
        examples=[
            GrammarExample(
                "Svjetla su ugašena; mora da su već otišli.",
                note="Govornik zaključuje iz opažanja, ali nije izravno vidio odlazak.",
            ),
            GrammarExample(
                "Zbog najavljenog štrajka isporuka bi mogla kasniti.",
                note="Kašnjenje je mogućnost koju treba uzeti u obzir, a ne potvrđena činjenica.",
            ),
        ],
        related=["hr-reported-source-b2", "hr-professional-requests-b2"],
    ),
    GrammarTopic(
        "hr-passive-agency-b2",
        "Pasiv i navođenje izvršitelja",
        "B2",
        "Glagolsko stanje",
        "Usmjerite pozornost na zahvaćeni predmet, a sačuvajte odgovornost za radnju.",
        "Pasiv se može izraziti glagolom biti i glagolskim pridjevom trpnim: Zahtjev "
        "je odobren. Pridjev se slaže sa subjektom u rodu i broju. Izvršitelj često "
        "nije naveden. Izraz od strane povjerenstva moguć je u administrativnom tekstu, "
        "ali aktiv Povjerenstvo je odobrilo zahtjev često je jasniji i kraći.",
        rules=[
            "Pri pretvaranju u aktiv ne izmišljajte izvršitelja kojeg tekst ne navodi.",
            "Sačuvajte vrijeme i vid: razmatran je nije isto što i razmotren je.",
            "Složite oblike s predmetom opisa: ugovor je potpisan, odluke su objavljene.",
        ],
        examples=[
            GrammarExample(
                "Prijedlog je prihvaćen na sjednici gradskog vijeća.",
                note="U središtu je ishod; rečenica ne imenuje svakoga tko je glasao za prijedlog.",
            ),
            GrammarExample(
                "Dokumentacija je pregledana od strane ovlaštenog stručnjaka.",
                note="Izvršitelj je naveden; jasniji aktiv glasi: "
                "Ovlašteni stručnjak pregledao je dokumentaciju.",
            ),
        ],
        related=["hr-se-constructions-b2", "hr-nominalisation-b2"],
    ),
    GrammarTopic(
        "hr-se-constructions-b2",
        "Pasivne i bezlične rečenice sa se",
        "B2",
        "Glagolsko stanje",
        "Razlikujte opći postupak od radnje s imenovanim subjektom.",
        "U rečenici Prijave se zaprimaju elektronički riječ prijave subjekt je u množini, "
        "pa je i glagol u množini. U bezličnoj rečenici O tome se dugo raspravljalo "
        "nema takvog subjekta; oblik je u srednjem rodu jednine. Nije svaka rečenica "
        "sa se pasivna: Ana se smije opisuje radnju glagola smijati se.",
        rules=[
            "Kod pasivnog se pazite na slaganje: odluka se donosi, odluke se donose.",
            "Bezlične konstrukcije ne govore same po sebi tko je sudjelovao.",
            "Za zahtjev za odgovornošću upitajte tko provodi postupak umjesto da nagađate.",
        ],
        examples=[
            GrammarExample(
                "Potvrde se izdaju na prvom katu.",
                note="Potvrde su subjekt; rečenica opisuje uobičajeni postupak.",
            ),
            GrammarExample(
                "Na sastanku se razgovaralo o novom rasporedu.",
                note="Bezlični oblik razgovaralo ne otkriva tko je govorio ni što je odlučeno.",
            ),
        ],
        related=["hr-passive-agency-b2"],
    ),
    GrammarTopic(
        "hr-nominalisation-b2",
        "Glagolske imenice i jasnoća službenog teksta",
        "B2",
        "Imenski izrazi",
        "Sažmite radnju imenicom, ali ne izgubite podatak tko što radi.",
        "Imenice poput odobrenje, dostava i razmatranje omogućuju sažet službeni izraz. "
        "Nizovi imenica mogu prikriti sudionike: odobrenje zahtjeva ne govori nužno tko "
        "ga odobrava. Pri preoblikovanju u rečenicu navedite izvršitelja samo ako je "
        "poznat. Nakon primitka dokumentacije opisuje redoslijed, ali ne jamči odobrenje.",
        rules=[
            "Provjerite označuje li genitiv predmet radnje ili njezina izvršitelja.",
            "Duge imenske nizove razložite u glagolske rečenice kada time povećavate jasnoću.",
            "Nemojte dodavati obvezu, rok ili rezultat koji ne proizlazi iz izvornog teksta.",
        ],
        examples=[
            GrammarExample(
                "Nakon primitka računa računovodstvo će provjeriti iznos.",
                note="Može se pojasniti: Nakon što račun bude primljen, računovodstvo će provjeriti iznos.",
            ),
            GrammarExample(
                "Zahtjev za produljenje roka treba obrazložiti.",
                note="Imenski izraz sažima što se traži; iz rečenice još ne znamo tko odlučuje.",
            ),
        ],
        related=["hr-passive-agency-b2", "hr-infinitive-subject-b2"],
    ),
    GrammarTopic(
        "hr-hypothetical-conditions-b2",
        "Mogući i zamišljeni uvjeti",
        "B2",
        "Pogodbene rečenice",
        "Odvojite otvoren plan od zamišljenog scenarija.",
        "Ako dobijemo sredstva, zaposlit ćemo još jednu osobu predstavlja uvjet kao "
        "otvorenu mogućnost. Kad bismo imali više sredstava, zaposlili bismo još jednu "
        "osobu zamišlja situaciju i njezinu posljedicu. Kondicional sam po sebi ne dokazuje "
        "da je uvjet nemoguć; stav govornika i kontekst određuju koliko je udaljen od stvarnosti.",
        rules=[
            "Za zamišljen uvjet upotrijebite odgovarajući kondicional: kad bih, kad bismo, kad biste.",
            "Razlikujte pregovarački prijedlog od čvrstog obećanja.",
            "U hrvatskom su mogući i obrasci s da: Da imamo vremena, ostali bismo dulje.",
        ],
        examples=[
            GrammarExample(
                "Ako smanjite predujam, prihvatit ćemo ponudu.",
                note="Govornik se obvezuje na prihvaćanje ako se navedeni uvjet ispuni.",
            ),
            GrammarExample(
                "Kad bismo rok pomaknuli za tjedan dana, mogli bismo uključiti još jednu provjeru.",
                note="Predlaže se zamišljena izmjena rasporeda i njezina moguća korist.",
            ),
        ],
        related=["hr-past-counterfactual-b2", "hr-necessary-conditions-b2"],
    ),
    GrammarTopic(
        "hr-past-counterfactual-b2",
        "Neostvareni uvjet u prošlosti",
        "B2",
        "Pogodbene rečenice",
        "Razgovarajte o propuštenoj mogućnosti bez mijenjanja stvarnog ishoda.",
        "U rečenici Da smo ranije krenuli, stigli bismo na trajekt kontekst upućuje na "
        "neostvaren prošli uvjet. U glavnoj rečenici kondicional prvi može izražavati "
        "prošlu posljedicu. Kondicional drugi, primjerice bili bismo stigli, također "
        "postoji, ali nije obvezan u svakom takvom iskazu i rjeđi je u svakodnevnom govoru.",
        rules=[
            "Prošlo neostvarenje učinite jasnim kontekstom, a ne samo oblikom kondicionala.",
            "Ne proglašavajte stigli bismo pogrešnim samo zato što se posljedica odnosi na prošlost.",
            "Za miješani odnos jasno navedite sadašnju posljedicu prošlog uvjeta.",
        ],
        examples=[
            GrammarExample(
                "Nismo provjerili vozni red pa smo propustili zadnji vlak. "
                "Da smo ga provjerili, ne bismo propustili zadnji vlak.",
                note="Prva rečenica potvrđuje da provjera i željeni ishod nisu ostvareni.",
            ),
            GrammarExample(
                "Da sam jučer prihvatila ponudu, danas bih radila na drugom projektu.",
                note="Neostvareni jučerašnji uvjet povezan je sa zamišljenom sadašnjom posljedicom.",
            ),
        ],
        related=["hr-hypothetical-conditions-b2"],
    ),
    GrammarTopic(
        "hr-necessary-conditions-b2",
        "Nužni uvjeti, iznimke i ograničenja",
        "B2",
        "Uvjeti i opseg",
        "Razlikujte što je potrebno od onoga što jamči ishod.",
        "Samo ako uvodi nužan uvjet: Povrat je moguć samo ako sačuvate račun. To ne "
        "isključuje postojanje drugih uvjeta povrata. Osim ako uvodi iznimku: Sastanak "
        "ostaje u petak, osim ako se svi dogovorimo drukčije. Pod uvjetom da izričito "
        "veže ponuđenu radnju uz ispunjenje uvjeta.",
        rules=[
            "Iz nužnog uvjeta ne zaključujte automatski da je on i dovoljan.",
            "Uz osim ako utvrdite koje se pravilo mijenja u slučaju iznimke.",
            "U dogovoru navedite uvjet dovoljno precizno da ga obje strane mogu provjeriti.",
        ],
        examples=[
            GrammarExample(
                "Prijava se razmatra samo ako je dokumentacija potpuna.",
                note="Potpuna dokumentacija nužan je uvjet, ali sama ne jamči "
                "da će prijava biti razmotrena ili odobrena.",
            ),
            GrammarExample(
                "Zadržat ćemo isti termin, osim ako predavač zatraži promjenu.",
                note="Zahtjev predavača navedena je iznimka od planiranog termina.",
            ),
        ],
        related=["hr-hypothetical-conditions-b2", "hr-negation-scope-b2"],
    ),
    GrammarTopic(
        "hr-negation-scope-b2",
        "Doseg negacije: nitko, nisu svi i ne mora",
        "B2",
        "Negacija i značenje",
        "Odredite odnosi li se nijekanje na cijelu skupinu, obvezu ili zaključak.",
        "Nitko nije odgovorio isključuje odgovor svakog člana skupine. Nisu svi odgovorili "
        "negira tvrdnju da je odgovorila cijela skupina, ali ne određuje točan broj. "
        "Svi nisu odgovorili može biti nejasno, pa je bolje izabrati jednoznačniji oblik. "
        "Ne morate doći uklanja obvezu; ne smijete doći izriče zabranu.",
        rules=[
            "Uz niječne zamjenice zadržite niječni glagol: Nitko ništa nije predložio.",
            "Za djelomično nijekanje jasno postavite nisu svi, a za potpuno nitko nije.",
            "Ne mora značiti odbacuje nužnost zaključka, a ne potvrđuje njegovu suprotnost.",
        ],
        examples=[
            GrammarExample(
                "Nisu svi zahtjevi odbijeni; tri su još u postupku.",
                note="Odbijanje se ne odnosi na sve zahtjeve, ali ne slijedi da je neki već odobren.",
            ),
            GrammarExample(
                "Dulji rok ne mora značiti višu cijenu.",
                note="Viša cijena nije nužna posljedica; rečenica ne jamči da će cijena ostati ista.",
            ),
        ],
        related=["hr-necessary-conditions-b2", "hr-focus-particles-b2"],
    ),
    GrammarTopic(
        "hr-contrastive-order-b2",
        "Red riječi, naglasak i ispravak nesporazuma",
        "B2",
        "Obavijesno ustrojstvo",
        "Istaknite novu ili suprotstavljenu informaciju bez promjene sudionika.",
        "Hrvatski red riječi omogućuje prilagodbu poznatoj i novoj informaciji. "
        "Izvješće je sastavila Iva prirodno može odgovoriti na pitanje tko ga je sastavio. "
        "Naglasak i kontekst mogu promijeniti žarište i bez promjene reda riječi. "
        "Pri isticanju zamjenice rabi se naglašeni oblik: Njemu sam poslala nacrt, ne tebi. "
        "Nenaglašene oblike ne treba premještati kao da su samostalno naglašene riječi.",
        rules=[
            "Padežima i slaganjem sačuvajte tko vrši radnju i na koga se ona odnosi.",
            "Za kontrast osobe odaberite naglašeni oblik: meni, njemu, njoj.",
            "Ne svodite zanaglasnice na pravilo da uvijek moraju stajati iza prve riječi.",
        ],
        examples=[
            GrammarExample(
                "Raspored je promijenio organizator, ne predavač.",
                note="Završni dio ispravlja pretpostavku o odgovornoj osobi.",
            ),
            GrammarExample(
                "Njoj sam poslao konačnu verziju, a tebi radnu.",
                note="Naglašeni dativni oblici ističu različite primatelje.",
            ),
        ],
        related=["hr-focus-particles-b2", "hr-reference-cohesion-b2"],
    ),
    GrammarTopic(
        "hr-focus-particles-b2",
        "Samo, čak i tek",
        "B2",
        "Čestice i značenje",
        "Prepoznajte ograničenje, neočekivano uključivanje i kasniji trenutak.",
        "Samo ograničuje skup ili dio tvrdnje: Samo je Lea potpisala znači da drugi nisu. "
        "Čak naglašava uključivanje koje govornik predstavlja kao neočekivano. Tek uz "
        "vremenski izraz često označuje da nešto nije nastupilo ranije: Odgovor je stigao "
        "tek u petak. Točno žarište ovisi i o naglasku, pa nejasnoću po potrebi razjasnite.",
        rules=[
            "Provjerite ograničuje li samo osobu, predmet, radnju ili količinu.",
            "Čak ne označuje samo činjenicu nego i govornikovo očekivanje.",
            "Ne zaključujte razlog kašnjenja samo iz izraza tek u petak.",
        ],
        examples=[
            GrammarExample(
                "Samo sam provjerila iznos; račun nisam odobrila.",
                note="Drugi dio jasno određuje da je ograničena radnja, a ne broj osoba.",
            ),
            GrammarExample(
                "Čak je i najoprezniji član podržao prijedlog.",
                note="Podrška toga člana prikazana je kao neočekivana.",
            ),
            GrammarExample(
                "Podatke smo dobili tek nakon sastanka.",
                note="Govornici su podatke dobili tek nakon sastanka; rečenica ne govori "
                "jesu li podaci ranije bili dostupni drugdje.",
            ),
        ],
        related=["hr-contrastive-order-b2", "hr-negation-scope-b2"],
    ),
    GrammarTopic(
        "hr-infinitive-subject-b2",
        "Tko izvršava radnju uz infinitiv i zavisnu rečenicu?",
        "B2",
        "Dopune glagola",
        "U poslovnom dogovoru nedvosmisleno odredite izvršitelja.",
        "U Ana je odlučila poslati ponudu Ana donosi odluku, a podrazumijevani izvršitelj "
        "slanja također je Ana; rečenica ne potvrđuje da je ponuda poslana. "
        "Uz Zamolio sam Anu da pošalje ponudu očekivani izvršitelj slanja jest Ana, "
        "a molbu izriče govornik. U "
        "Odobreno je produljiti rok izvršitelj nije naveden. Infinitiv je u hrvatskom "
        "uobičajen, ali zavisna rečenica s da može jasnije odrediti drugog sudionika.",
        rules=[
            "Ne pripisujte radnju automatski subjektu glavne rečenice bez provjere glagola.",
            "Ako se izvršitelj mijenja, izričito ga navedite kad bi zamjenica bila nejasna.",
            "Pri preoblikovanju sačuvajte razliku između odluke, molbe i dopuštenja.",
        ],
        examples=[
            GrammarExample(
                "Odlučili smo poslati dopunu do srijede.",
                note="Mi donosimo odluku i preuzimamo slanje dopune.",
            ),
            GrammarExample(
                "Zamolili smo dobavljača da pošalje dopunu do srijede.",
                note="Mi izričemo molbu; očekivani izvršitelj slanja jest dobavljač.",
            ),
        ],
        related=["hr-nominalisation-b2", "hr-reference-cohesion-b2"],
    ),
    GrammarTopic(
        "hr-professional-requests-b2",
        "Ublažene molbe i jasno odbijanje",
        "B2",
        "Registar i uljudnost",
        "Budite obzirni, ali jasno izrazite što tražite ili možete ponuditi.",
        "Kondicional u Biste li mogli provjeriti iznos? ublažava zahtjev. Oblik "
        "Molim vas da provjerite iznos izravniji je, ali i dalje može biti uljudan. "
        "Izrazi bojim se da i nažalost mogu uvoditi odbijanje, no ne smiju prikriti "
        "njegov stvarni sadržaj. U poruci razlikujte prijedlog od potvrđenog dogovora.",
        rules=[
            "Uz uljudno vi rabite množinske glagolske oblike: biste li mogli.",
            "Navedite konkretan zadatak i potreban rok umjesto niza neodređenih ublaživača.",
            "Kada odbijate, jasno recite što nije moguće i po potrebi ponudite izvedivu zamjenu.",
        ],
        examples=[
            GrammarExample(
                "Biste li nam mogli dostaviti ispravljen račun do četvrtka?",
                note="Kondicional ublažava molbu, a predmet i rok ostaju konkretni.",
            ),
            GrammarExample(
                "Nažalost, ne možemo završiti do petka, ali nacrt možemo poslati u četvrtak.",
                note="Odbijanje prvog roka ne skriva se iza pristojnosti; "
                "ponuđen je ograničen korak.",
            ),
        ],
        related=["hr-epistemic-modality-b2", "hr-hypothetical-conditions-b2"],
    ),
    GrammarTopic(
        "hr-reference-cohesion-b2",
        "Jasne zamjeničke veze u duljem tekstu",
        "B2",
        "Tekstna povezanost",
        "Neka bude jasno na koga ili na što upućuju zamjenice.",
        "U duljoj poruci on, ona, to i svoj mogu postati nejasni ako postoji više "
        "mogućih referenata. Svoj u uobičajenoj rečenici označuje pripadnost subjektu: "
        "Iva je poslala svoj nacrt. Njezin može upućivati na drugu žensku osobu. U "
        "složenim rečenicama i uz više sudionika ponavljanje imena često je najjasnije.",
        rules=[
            "Za svoj najprije utvrdite subjekt rečenice u kojoj se nalazi.",
            "Kad rod i broj ne razrješuju referencu, ponovite ime ili naziv dokumenta.",
            "Ne zamjenjujte naziv zamjenicom ako bi time postalo nejasno što je dogovoreno.",
        ],
        examples=[
            GrammarExample(
                "Iva je razgovarala s Lanom. Lana će poslati revidirani nacrt.",
                note="Ponavljanje imena jasno određuje izvršiteljicu nakon spominjanja dviju osoba.",
            ),
            GrammarExample(
                "Petar je predao svoj izvještaj voditeljici.",
                note="Svoj se odnosi na Petra, subjekt ove rečenice.",
            ),
        ],
        related=["hr-infinitive-subject-b2", "hr-reformulation-b2"],
    ),
    GrammarTopic(
        "hr-discourse-markers-b2",
        "Povezivanje obrazloženja i zaključka",
        "B2",
        "Organizacija diskursa",
        "Vodite sugovornika kroz objašnjenje, ogradu i preporuku.",
        "Naime uvodi dodatno objašnjenje prethodne tvrdnje. Dakle označuje zaključak "
        "ili sažimanje, a pritom dodaje okolnost koja vrijedi uz opisanu radnju. "
        "S jedne strane i s druge strane organiziraju dvije perspektive. Vezna sredstva "
        "trebaju odgovarati stvarnom odnosu među mislima, ne samo zvučati formalno.",
        rules=[
            "Uz naime objasnite prethodnu tvrdnju, umjesto da bez veze promijenite temu.",
            "Za zaključak provjerite podupiru li ga izneseni razlozi.",
            "Pri usporedbi dviju strana navedite relevantnu prednost i ograničenje.",
        ],
        examples=[
            GrammarExample(
                "Predlažem raniji polazak. Naime, poslijepodne se očekuje gužva.",
                note="Druga rečenica obrazlaže preporuku iz prve.",
            ),
            GrammarExample(
                "Možemo smanjiti opseg radova i pritom zadržati pristup za osobe s invaliditetom.",
                note="Pritom povezuje uštedu s uvjetom koji ostaje zadovoljen.",
            ),
        ],
        related=["hr-cause-result-b2", "hr-contrast-b2"],
    ),
    GrammarTopic(
        "hr-proportional-comparison-b2",
        "Što…, to… i odnosi promjena",
        "B2",
        "Usporedba",
        "Opišite kako se dvije pojave mijenjaju zajedno.",
        "Konstrukcija što s komparativom i to s komparativom povezuje dvije promjene: "
        "Što dulje čekamo, to manje vremena imamo. Može izraziti i poželjnu granicu "
        "u kraćem obrascu što prije, to bolje. Takvo povezivanje ne objašnjava uvijek "
        "uzrok i ne zamjenjuje podatke koji su potrebni za provjeru tvrdnje.",
        rules=[
            "Rabite odgovarajući komparativ: što više, to bolje; što manje, to lakše.",
            "Sačuvajte smjer promjene; veće ne mora voditi drugom većem svojstvu.",
            "U pregovoru objasnite na koje se rokove, troškove ili potrebe usporedba odnosi.",
        ],
        examples=[
            GrammarExample(
                "Što ranije potvrdimo broj sudionika, to ćemo lakše dogovoriti prijevoz.",
                note="Ranija potvrda povezuje se s jednostavnijom organizacijom.",
            ),
            GrammarExample(
                "Što je ponuda detaljnija, to je manji prostor za nesporazume.",
                note="Povećanje jasnoće povezuje se sa smanjenjem rizika.",
            ),
        ],
        related=["hr-cause-result-b2", "hr-discourse-markers-b2"],
    ),
    GrammarTopic(
        "hr-reformulation-b2",
        "Preoblikovanje, ograda i provjera razumijevanja",
        "B2",
        "Posredovanje",
        "Razjasnite poruku bez mijenjanja tuđeg stava.",
        "Drugim riječima uvodi preoblikovanje koje treba sačuvati smisao. Točnije "
        "može suziti ili ispraviti prethodnu formulaciju. Ako sam dobro razumio "
        "označuje provjeru, a ne tvrdnju da je sugovornik već prihvatio vaš sažetak. "
        "Pri humoru i pretjerivanju provjerite ton prije nego što izraz shvatite doslovno.",
        rules=[
            "U sažetku zadržite sudionike, uvjete i stupanj sigurnosti izvornog iskaza.",
            "Ako sužavate preširoku tvrdnju, jasno označite ispravak izrazom točnije.",
            "Sugovorniku ostavite mogućnost da potvrdi ili popravi vaš sažetak.",
        ],
        examples=[
            GrammarExample(
                "Ako sam dobro razumjela, podržavate projekt, ali ne i predloženi rok?",
                note="Govornica provjerava razliku između cilja i načina provedbe.",
            ),
            GrammarExample(
                "Sve je stalo. Točnije, čeka se samo potpis na ugovoru.",
                note="Druga rečenica izričito ispravlja pretjerano široku prvu tvrdnju.",
            ),
            GrammarExample(
                "Kad kažeš da ti treba sto godina, misliš li da je rok prekratak?",
                note="Pretjerivanje se provjerava kao izraz poteškoće, ne prenosi se doslovno.",
            ),
        ],
        related=["hr-reference-cohesion-b2", "hr-reported-source-b2"],
    ),
]
