"""Croatian C2 grammar, discourse and pragmatic control."""

from app.data._types import GrammarExample, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "hr-reference-repair-c2",
        "Nejasne zamjenice i provjera upućivanja",
        "C2",
        "Povezivanje iskaza",
        "Razjasnite osobu ili predmet prije nego što nastavite razgovor.",
        "U iskazu s više mogućih prethodnika zamjenica ne mora jednoznačno upućivati "
        "na najbližu imenicu. Rečenica „Ana je rekla Petri da će ona nazvati” bez "
        "dodatnog konteksta ne određuje pouzdano tko će zvati. Ponovite ime ili "
        "postavite kratko pitanje. Povratno-posvojna zamjenica svoj u pravilu označava "
        "pripadnost subjektu vlastite surečenice; promjenom subjekta može se promijeniti vlasnik.",
        rules=[
            "Ne pripisujte radnju osobi samo zato što je zadnja spomenuta.",
            "Pri zamjeni zamjenice imenom sačuvajte stvarnog govornika, izvršitelja i vlasnika.",
        ],
        examples=[
            GrammarExample(
                "Ana je rekla Petri da će ona nazvati. — Misliš na Anu ili na Petru?",
                note="Pitanje razjašnjava upućivanje, a ne osporava najavu poziva.",
            ),
            GrammarExample(
                "Luka je rekao Ivanu da ponese svoju bilježnicu. — "
                "Luka je rekao Ivanu da ponese Ivanovu bilježnicu.",
                note="U uobičajenom čitanju subjekt radnje ponijeti jest Ivan, a bilježnica "
                "pripada njemu. Preoblikovanje čuva i podatak da je uputu dao Luka.",
            ),
        ],
        related=["hr-attachment-c2", "hr-self-correction-c2"],
    ),
    GrammarTopic(
        "hr-attachment-c2",
        "Dvosmisleno povezivanje dodataka",
        "C2",
        "Rečenična struktura",
        "Razlikujte moguća vezivanja dodatka i izrecite namjeravano značenje.",
        "Prijedložna skupina može opisivati osobu ili okolnosti radnje. U rečenici "
        "„Fotografirao je djevojku na balkonu” na balkonu može biti djevojka, "
        "fotograf ili oboje. Sama blizina riječi nije dovoljan dokaz. Kad je prostorni "
        "odnos važan, navedite ga zasebnom surečenicom nakon provjere.",
        rules=[
            "Najprije odredite koje su interpretacije moguće u danom kontekstu.",
            "Razjašnjenjem nemojte dodavati položaj ili sudionika koji nije potvrđen.",
        ],
        examples=[
            GrammarExample(
                "Fotografirao je djevojku koja je stajala na balkonu.",
                note="Određuje se položaj djevojke; položaj fotografa ostaje otvoren.",
            ),
            GrammarExample(
                "Dok je stajao na balkonu, fotografirao je djevojku u vrtu.",
                note="Oba su položaja izričita; ova je inačica primjerena samo ako su potvrđena.",
            ),
        ],
        related=["hr-reference-repair-c2", "hr-nominal-compression-c2"],
    ),
    GrammarTopic(
        "hr-self-correction-c2",
        "Ispravak u hodu i granice preoblikovanja",
        "C2",
        "Govorna interakcija",
        "Ispravite pogrešan dio iskaza bez nepotrebnog povlačenja ostatka.",
        "Izrazi odnosno, točnije i zapravo mogu uvoditi pojašnjenje ili ispravak. "
        "Njihov doseg mora biti prepoznatljiv: mijenja li se datum, sudionik ili "
        "čitava tvrdnja? Nakon prekida ponovite dio koji se mijenja. Izraz drugim "
        "riječima najavljuje preoblikovanje smisla, a ne opravdava promjenu činjenica.",
        rules=[
            "Ako ispravak mijenja činjenicu, označite ga kao ispravak, a ne kao istoznačno tumačenje.",
            "Kod važnog roka ili iznosa ponovite točan podatak u cjelovitoj rečenici.",
        ],
        examples=[
            GrammarExample(
                "Sastajemo se u četvrtak — oprostite, u petak, u isto vrijeme.",
                note="Mijenja se dan; sat ostaje isti.",
            ),
            GrammarExample(
                "Maja je poslala dopis, točnije nacrt dopisa; konačna verzija još nije poslana.",
                note="Ispravlja se status dokumenta, ne osoba koja ga je poslala.",
            ),
        ],
        related=["hr-evidence-scope-c2", "hr-register-recasting-c2"],
    ),
    GrammarTopic(
        "hr-nominal-compression-c2",
        "Glagolske imenice bez skrivanja izvršitelja",
        "C2",
        "Sažimanje i razlaganje",
        "Razložite imeničke nizove uz očuvanje odgovornosti i vremena radnje.",
        "Glagolske imenice kao odobrenje i odbijanje sažimaju događaj, ali mogu "
        "prikriti tko djeluje na koga. „Odbijanje povjerenstva” može označavati "
        "odluku povjerenstva ili odbijanje samog povjerenstva. Izraz od strane "
        "može razjasniti izvršitelja u administrativnom tekstu; u razgovoru je "
        "često jasnija aktivna rečenica. Vrijeme radnje preuzmite iz konteksta.",
        rules=[
            "Genitiv uz glagolsku imenicu nemojte automatski tumačiti kao izvršitelja radnje.",
            "Ako izvršitelj nije poznat, zadržite neosobnu ili pasivnu formulaciju.",
        ],
        examples=[
            GrammarExample(
                "Jučerašnje odbijanje zahtjeva od strane povjerenstva iznenadilo je stanare. "
                "— Povjerenstvo je jučer odbilo zahtjev, što je iznenadilo stanare.",
                note="Očuvani su izvršitelj, predmet, vrijeme i reakcija.",
            ),
            GrammarExample(
                "Došlo je do otkazivanja sastanka. — Sastanak je otkazan.",
                note="Nijedna inačica ne otkriva tko je otkazao sastanak.",
            ),
        ],
        related=["hr-attachment-c2", "hr-evidence-scope-c2"],
    ),
    GrammarTopic(
        "hr-evidence-scope-c2",
        "Izvor tvrdnje i stupanj sigurnosti",
        "C2",
        "Modalnost i izvori",
        "Razdvojite ono što znate od onoga što netko tvrdi ili zaključuje.",
        "Navodno upućuje na prenesenu, nepotvrđenu informaciju, dok čini se "
        "označava procjenu govornika. Prema nalazu navodi izvor, ali ne jamči "
        "točnost svakog mogućeg zaključka. U sažetku ograda mora ostati uz tvrdnju "
        "na koju se odnosi; izostavljanjem ograde mogućnost postaje prividna činjenica.",
        rules=[
            "Navođenje izvora ne zamjenjuje oznaku nesigurnosti koju izvor sam upotrebljava.",
            "Sačuvajte razliku između nije dokazano i dokazano je da nije.",
        ],
        examples=[
            GrammarExample(
                "Prema procjeni servisa, kvar je možda nastao zbog vlage.",
                note="I izvor i nesigurnost uzroka ostaju izričiti.",
            ),
            GrammarExample(
                "Nije dokazano da je voda onečišćena; to ne znači da je potvrđena njezina ispravnost.",
                note="To što tvrdnja nije dokazana ne znači da je dokazana njezina suprotnost.",
            ),
        ],
        related=["hr-negation-scope-c2", "hr-commitment-c2"],
    ),
    GrammarTopic(
        "hr-negation-scope-c2",
        "Doseg niječne tvrdnje",
        "C2",
        "Nijekanje i količina",
        "Razlikujte što se točno poriče i koliko se slučajeva obuhvaća.",
        "„Nisu svi pristali” poriče opću suglasnost, ali samo po sebi ne govori "
        "koliko je ljudi pristalo. „Nitko nije pristao” isključuje svakoga. "
        "U hrvatskom se niječne zamjenice redovito povezuju s niječnim glagolom: "
        "nitko nije nije potvrdni iskaz. Kod ispravljanja izraza može se odbaciti "
        "naziv ili ocjena, a ne sam događaj.",
        rules=[
            "Iz djelomičnog nijekanja nemojte izvoditi precizan broj pristalih.",
            "Naznačite poričete li činjenicu ili samo način na koji je opisana.",
        ],
        examples=[
            GrammarExample(
                "Nisu svi odbili prijedlog: dvije su se osobe složile, a ostale su bile protiv.",
                note="Dodatak navodi raspodjelu koju prva surečenica sama ne daje.",
            ),
            GrammarExample(
                "Nije pobjegla sa sastanka; otišla je u unaprijed dogovoreno vrijeme.",
                note="Osporava se opis odlaska kao bijega, ne činjenica da je otišla.",
            ),
        ],
        related=["hr-presupposition-c2", "hr-focus-particles-c2"],
    ),
    GrammarTopic(
        "hr-ironic-echo-c2",
        "Ironično ponavljanje tuđe procjene",
        "C2",
        "Pragmatika i humor",
        "Prepoznajte odmak od ponovljene pohvale i provjerite nejasnu namjeru.",
        "Nakon obećanja da će sve ići glatko, rečenica „Baš glatko!” izgovorena "
        "pred zaključanim vratima može ironično ponoviti tuđe riječi. Ironija "
        "proizlazi iz nesklada sa situacijom, intonacije i zajedničkog znanja, "
        "ne iz same čestice baš. U pisanju navodnici mogu označavati i običan "
        "citat, pa nisu samostalan dokaz poruge.",
        rules=[
            "U tumačenju povežite doslovnu poruku s prethodnom izjavom i ishodom.",
            "Kad je odnos osjetljiv, provjerite namjeru umjesto automatskog pripisivanja podsmijeha.",
        ],
        examples=[
            GrammarExample(
                "„To traje samo minutu”, rekao si. Evo nas već pola sata: stvarno samo minutu.",
                note="Ponovljena procjena služi kritici njezine netočnosti.",
            ),
            GrammarExample(
                "Kad kažeš da smo se proslavili, misliš na uspjeh ili na našu zabunu s imenima?",
                note="Sugovornik provjerava ironično čitanje umjesto da ga pretpostavi.",
            ),
        ],
        related=["hr-implicature-c2", "hr-understatement-c2"],
    ),
    GrammarTopic(
        "hr-implicature-c2",
        "Nagovještaj koji se može povući",
        "C2",
        "Neizravno značenje",
        "Razlikujte izrečeni sadržaj od zaključka koji proizlazi iz situacije.",
        "Odgovor „Sutra rano ustajem” na poziv na još jedno piće može značiti "
        "odbijanje, ali nije doslovno odbijanje. Nastavak „ali mogu ostati još "
        "deset minuta” ne proturječi činjenici o ranom ustajanju. Pri tumačenju "
        "uzmite u obzir odnos sugovornika i prethodne replike; neizravnost ne "
        "oslobađa govornika odgovornosti za učinak šale.",
        rules=[
            "Zaključak izveden iz konteksta provjerite kad utječe na zajednički plan.",
            "Pri pojašnjenju odvojite stvarnu namjeru od učinka koji je poruka već imala.",
        ],
        examples=[
            GrammarExample(
                "Sutra rano ustajem, ali ostajem još deset minuta.",
                note="Nastavak povlači moguće tumačenje da govornik odmah odlazi.",
            ),
            GrammarExample(
                "Htio sam se našaliti, ali čujem da je zvučalo kao prigovor. Žao mi je.",
                note="Objašnjenje namjere ne poništava priznanje učinka.",
            ),
        ],
        related=["hr-ironic-echo-c2", "hr-presupposition-c2"],
    ),
    GrammarTopic(
        "hr-presupposition-c2",
        "Pitanje s neprihvaćenom pretpostavkom",
        "C2",
        "Upravljanje razgovorom",
        "Odgovorite na pitanje bez prešutnog prihvaćanja sporne polazne tvrdnje.",
        "Pitanje „Zašto ste opet zakasnili?” predstavlja kašnjenje kao činjenicu "
        "i izrazom opet priziva ranije kašnjenje. Odgovor navođenjem razloga može "
        "ostaviti oba dijela neosporenima. Ako je sporan samo raniji slučaj, "
        "izdvojite ga i zatim odgovorite na današnji problem.",
        rules=[
            "Odvojite sadašnju tvrdnju od pretpostavke o prethodnim događajima.",
            "Ispravkom pretpostavke nemojte poricati činjenicu koju prihvaćate.",
        ],
        examples=[
            GrammarExample(
                "Danas jesam zakasnio, ali na koje ranije kašnjenje mislite kad kažete opet?",
                note="Prihvaća se današnji događaj, a provjerava tvrdnja o ponavljanju.",
            ),
            GrammarExample(
                "Pitate kad smo prestali obavještavati stanare, no obavijesti i dalje šaljemo svaki tjedan.",
                note="Osporava se pretpostavka da je obavještavanje prestalo.",
            ),
        ],
        related=["hr-negation-scope-c2", "hr-self-correction-c2"],
    ),
    GrammarTopic(
        "hr-literary-past-c2",
        "Aorist i imperfekt u književnom čitanju",
        "C2",
        "Književni pripovjedni oblici",
        "Prepoznajte prošla vremena i njihov učinak bez zahtjeva za svakodnevnom uporabom.",
        "Aorist često prikazuje prošlu radnju kao cjelinu i u pripovijedanju može "
        "ubrzati niz događaja: zastade, pogleda, ode. Imperfekt prikazuje trajanje "
        "ili ponavljanje u prošlosti: bijaše, govoraše. U suvremenom neutralnom "
        "razgovoru uglavnom se rabi perfekt; aorist se ipak može pojaviti i u "
        "kratkim porukama ili ekspresivnom govoru. Cilj je prepoznavanje književnog "
        "učinka, a ne zamjena svakodnevnog perfekta tim oblicima.",
        rules=[
            "Vrijeme prepoznajte iz oblika, a ulogu u priči iz šireg konteksta.",
            "Pri neutralnom prepričavanju perfektom sačuvajte glagolski vid i slijed događaja.",
        ],
        examples=[
            GrammarExample(
                "Zastade pred vratima, pogleda broj i ode.",
                note="Aoristi nižu završene radnje: zastao je, pogledao je i otišao je.",
            ),
            GrammarExample(
                "Bijaše tiho, a starac govoraše kao da ga netko sluša.",
                note="Imperfekti stvaraju pozadinu i trajanje: bilo je tiho; starac je govorio.",
            ),
        ],
        related=["hr-narrative-time-c2", "hr-free-indirect-c2"],
    ),
    GrammarTopic(
        "hr-free-indirect-c2",
        "Misao lika u pripovjedačevoj rečenici",
        "C2",
        "Pripovjedna perspektiva",
        "Prepoznajte slobodni neupravni govor i ne pripisujte svaku procjenu pripovjedaču.",
        "U slobodnom neupravnom govoru pripovijedanje može zadržati treće lice, "
        "a preuzeti uzvik, pitanje ili vremensku perspektivu lika bez uvoda pomislio "
        "je. Pitanje usred opisa stoga može izražavati dvojbu lika, ne pitanje "
        "sveznajućeg pripovjedača. Tumačenje treba potkrijepiti susjednim rečenicama.",
        rules=[
            "Procjenu lika razlikujte od potvrđene činjenice u svijetu pripovijesti.",
            "Pri prepričavanju naznačite čija je misao ako bi se inače izgubila perspektiva.",
        ],
        examples=[
            GrammarExample(
                "Marta je stisnula pismo. Zar su doista mislili da će ona odustati? Nisu je poznavali.",
                note="Pitanje i prkos prirodno se čitaju kao Martina unutarnja reakcija.",
            ),
            GrammarExample(
                "Ivan je pogledao praznu stolicu. Opet ga je zaboravila! Tako je barem zaključio.",
                note="Završetak ograničava prethodni sud na Ivanovo tumačenje.",
            ),
        ],
        related=["hr-literary-past-c2", "hr-evidence-scope-c2"],
    ),
    GrammarTopic(
        "hr-narrative-time-c2",
        "Povratak u prošlost i promjena vremenskog uporišta",
        "C2",
        "Vremenska organizacija",
        "Pratite vrijeme događaja odvojeno od redoslijeda njihova iznošenja.",
        "Pripovijest može početi posljedicom, vratiti se ranijem događaju i "
        "zatim nastaviti prvotni prizor. Izrazi dan prije, dotad i poslije toga "
        "odnose se na trenutačno vremensko uporište, ne nužno na trenutak govora. "
        "Pluskvamperfekt može naglasiti prethodnost, ali je često dovoljan perfekt "
        "s jasnom vremenskom oznakom. Historijski prezent približava prošli prizor.",
        rules=[
            "Pri svakom povratku provjerite prema kojem se događaju određuje ranije ili kasnije.",
            "Promjena pripovjednog vremena ne mijenja sama po sebi stvarni redoslijed događaja.",
        ],
        examples=[
            GrammarExample(
                "Kad sam stigla u Rijeku, on je već bio otišao. Dan prije ostavio mi je ključ.",
                note="Ostavljanje ključa prethodi dolasku; odlazak se također dogodio prije dolaska.",
            ),
            GrammarExample(
                "Jučer ulazim u kuhinju, a ondje susjed s mojom tortom!",
                note="Prezent živopisno prikazuje prošli događaj; ne označava današnju radnju.",
            ),
        ],
        related=["hr-literary-past-c2", "hr-interwoven-discourse-c2"],
    ),
    GrammarTopic(
        "hr-conditional-exceptions-c2",
        "Uvjet unutar iznimke",
        "C2",
        "Složeni uvjeti",
        "Objasnite kome iznimka pripada i pod kojim ograničenjima.",
        "Pravilo s osim ako ili uz uvjet da može sadržavati više ograničenja. "
        "Dopuštenje jednoj skupini ne prenosi se automatski na druge, a iznimka od "
        "roka ne ukida ostale obveze. U razgovoru je često bolje najprije navesti "
        "opće pravilo, zatim nositelje iznimke, a potom njezine uvjete.",
        rules=[
            "Uvjet pridružite upravo onom dopuštenju koje ograničava.",
            "Navedite koje obveze ostaju na snazi i kad se iznimka primijeni.",
        ],
        examples=[
            GrammarExample(
                "Terasa se zatvara u deset; gosti hotela mogu ostati do jedanaest ako nema glazbe.",
                note="Kasniji boravak nije dopušten svim posjetiteljima niti uključuje glazbu.",
            ),
            GrammarExample(
                "Zahtjev predajte do petka, osim ako vam referent pisano odobri produljenje. "
                "Dokaze morate priložiti i tada.",
                note="Iznimka mijenja rok, a ne obvezu dostave dokaza.",
            ),
        ],
        related=["hr-commitment-c2", "hr-focus-particles-c2"],
    ),
    GrammarTopic(
        "hr-commitment-c2",
        "Namjera, pokušaj i preuzeta obveza",
        "C2",
        "Modalnost u dogovoru",
        "Razlikujte spremnost na razgovor od obećanja ishoda.",
        "Pokušat ću dogovoriti obećava pokušaj, ne uspjeh pregovora. Mogli bismo "
        "razmotriti označava prijedlog, a obvezujemo se preuzimanje obveze. Pri "
        "zapisivanju razgovora zadržite modalni izraz i izvršitelja radnje. "
        "Ljubaznost iskaza ne mora značiti da je njegov sadržaj neobvezan.",
        rules=[
            "Nemojte pretvoriti provjeru mogućnosti u potvrdu dostupnosti.",
            "Odvojite osobu koja pregovara od osobe koja smije donijeti odluku.",
        ],
        examples=[
            GrammarExample(
                "Pokušat ću s vlasnicom dogovoriti nižu cijenu; ona još nije pristala.",
                note="Govornik preuzima razgovor, ali ne jamči odluku vlasnice.",
            ),
            GrammarExample(
                "Obvezujemo se poslati nacrt do petka. Konačnu verziju tada još ne obećavamo.",
                note="Obveza se odnosi na nacrt i određeni rok.",
            ),
        ],
        related=["hr-evidence-scope-c2", "hr-concessive-negotiation-c2"],
    ),
    GrammarTopic(
        "hr-concessive-negotiation-c2",
        "Ustupak bez odustajanja od ključne potrebe",
        "C2",
        "Dopusni odnosi i pregovaranje",
        "Priznajte tuđi razlog i ponudite dogovor koji ne briše vlastito ograničenje.",
        "Iako uvodi prihvaćenu okolnost koja ne mijenja zaključak. Čak i ako "
        "može razmatrati hipotetski slučaj bez potvrde da se dogodio. Kad dvije "
        "osobe žele različite stvari, dopusni odnos pomaže priznati obje potrebe, "
        "a uvjetna ponuda određuje što se stvarno nudi u zamjenu.",
        rules=[
            "Razlikujte priznatu činjenicu od zamišljenog najpovoljnijeg ili najnepovoljnijeg slučaja.",
            "U kompromisu izrecite konkretnu promjenu i granicu iza koje ponuda ne vrijedi.",
        ],
        examples=[
            GrammarExample(
                "Iako mi više odgovara jutro, prihvatit ću termin u tri ako završimo do četiri.",
                note="Govornik mijenja termin uz izričitu granicu trajanja.",
            ),
            GrammarExample(
                "Čak i ako dobijemo popust, ne možemo rezervirati bez pristanka cijele grupe.",
                note="Popust nije potvrđen i ne bi sam uklonio potrebu za pristankom.",
            ),
        ],
        related=["hr-conditional-exceptions-c2", "hr-commitment-c2"],
    ),
    GrammarTopic(
        "hr-interwoven-discourse-c2",
        "Isprepletene teme i pripisivanje izjava",
        "C2",
        "Vođenje višeglasnog razgovora",
        "Povežite replike s njihovom temom i govornikom nakon prekida ili umetka.",
        "U živom razgovoru odgovor može stići nakon nekoliko replika o drugoj "
        "temi. Izrazi što se tiče, da se vratim na i prema onome što je rekla "
        "označavaju temu ili izvor. Sažetak mora razlikovati prijedlog jedne osobe "
        "od zajedničke odluke; šutnja drugih ne dokazuje njihov pristanak.",
        rules=[
            "Nakon promjene teme ponovite predmet odgovora ako bi kratak odgovor bio nejasan.",
            "U sažetku navedite tko nešto predlaže, a što je skupina doista prihvatila.",
        ],
        examples=[
            GrammarExample(
                "Da se vratim na tvoje pitanje o prijevozu: kombi jest slobodan, vozač još nije potvrđen.",
                note="Povratak je označen, a dvije različite dostupnosti ostaju razdvojene.",
            ),
            GrammarExample(
                "Ivana predlaže subotu; za nedjelju se zasad izjasnio samo Dario.",
                note="Nijedan prijedlog nije prikazan kao zajednička odluka.",
            ),
        ],
        related=["hr-elliptical-replies-c2", "hr-reference-repair-c2"],
    ),
    GrammarTopic(
        "hr-elliptical-replies-c2",
        "Skraćene replike i oporavak izostavljenog",
        "C2",
        "Elipsa u razgovoru",
        "Dopunite ono što je izostavljeno samo kad je zajednički kontekst dovoljno jasan.",
        "Replike „Ja ne” i „Može, ali ne sutra” preuzimaju predikat ili prijedlog "
        "iz prethodnog razgovora. Ako su otvorena dva pitanja, takva replika može "
        "imati više tumačenja. U bilješci vratite izostavljene dijelove uz potvrdu, "
        "a ne prema vlastitom očekivanju.",
        rules=[
            "Povežite elipsu s odgovarajućom replikom, ne automatski sa zadnjom rečenicom.",
            "Nakon dvosmislenog pristanka provjerite predmet pristanka prije postupanja.",
        ],
        examples=[
            GrammarExample(
                "Petra će donijeti stolice, a Marko projektor.",
                note="U drugoj se surečenici podrazumijeva da će Marko donijeti projektor.",
            ),
            GrammarExample(
                "„Možemo pomaknuti ručak ili otkazati šetnju.” — „Može.” — "
                "„Pristaješ na pomicanje ručka ili na otkazivanje šetnje?”",
                note="Dopuna se traži jer pristanak sam ne odabire jednu od ponuda.",
            ),
        ],
        related=["hr-interwoven-discourse-c2", "hr-self-correction-c2"],
    ),
    GrammarTopic(
        "hr-focus-particles-c2",
        "Samo, tek i čak: precizno usmjeravanje pozornosti",
        "C2",
        "Doseg čestica",
        "Jasno odredite ograničava li se osoba, radnja, predmet ili vrijeme.",
        "Čestica samo može izdvojiti sudionika ili ograničiti dopuštenu radnju. "
        "Tek često označava kasniji trenutak ili manju količinu od očekivane, "
        "a čak nešto neočekivano uključuje. Položaj i naglasak surađuju; u "
        "pisanom pravilu dodatna rečenica može spriječiti oslanjanje na nečujnu intonaciju.",
        rules=[
            "Ograničavajuću česticu smjestite uz dio na koji se odnosi i po potrebi dodajte pojašnjenje.",
            "Ne zamjenjujte tek sa samo ako bi se izgubila vremenska ili očekivana granica.",
        ],
        examples=[
            GrammarExample(
                "Samo Iva smije otkazati rezervaciju; ostali nemaju to ovlaštenje.",
                note="Ograničen je krug osoba, ne popis Ivinih drugih ovlasti.",
            ),
            GrammarExample(
                "Odgovor je stigao tek u petak, iako smo ga očekivali u utorak.",
                note="Tek označava kasniji trenutak od očekivanoga.",
            ),
        ],
        related=["hr-negation-scope-c2", "hr-clitics-rhythm-c2"],
    ),
    GrammarTopic(
        "hr-register-recasting-c2",
        "Promjena registra uz očuvanje poruke",
        "C2",
        "Stil i sugovornik",
        "Izrecite isti zahtjev prirodno različitim sugovornicima.",
        "Prijelaz iz službenog dopisa u razgovor uključuje kraće rečenice, "
        "izravnije glagole i drukčije oslovljavanje. Ne mijenja automatski obvezu, "
        "rok ili dopuštenje. Regionalni i razgovorni izrazi nisu sami po sebi "
        "pogrešni; birajte ih prema odnosu i situaciji. U javnoj obavijesti "
        "prednost ima razumljiv standardni izraz bez nepotrebnog administrativnog tereta.",
        rules=[
            "Prije prerade izdvojite izvršitelja, rok, uvjet i stupanj obveznosti.",
            "Prijateljski ton ne smije pretvoriti obvezu u neobvezan prijedlog.",
        ],
        examples=[
            GrammarExample(
                "Uplatu ste dužni izvršiti do petka. — Morate platiti do petka.",
                note="Jednostavnija formulacija zadržava obvezu i rok.",
            ),
            GrammarExample(
                "Preporučujemo da nam unaprijed najavite dolazak. — "
                "Bilo bi dobro da nam prije dolaska javite da dolazite.",
                note="Obje inačice preporučuju najavu; nijedna je ne proglašava uvjetom ulaska.",
            ),
        ],
        related=["hr-nominal-compression-c2", "hr-commitment-c2"],
    ),
    GrammarTopic(
        "hr-clitics-rhythm-c2",
        "Enklitike, naglasak i ritam složenog iskaza",
        "C2",
        "Red riječi i govorne cjeline",
        "Preoblikujte zahtjevan iskaz tako da ostane prirodan i razumljiv.",
        "Enklitike poput je, sam, mu i se nemaju vlastiti naglasak i vežu se uz "
        "naglašenu riječ u govornoj cjelini. Često dolaze rano u rečenici, ali "
        "pravilo nije mehaničko brojanje druge napisane riječi. Duga umetnuta "
        "objašnjenja mogu otežati praćenje; tada preuredite iskaz ili ga podijelite. "
        "Kad je osobna zamjenica suprotstavljena drugoj, birajte naglašeni oblik.",
        rules=[
            "Ne stavljajte enklitiku na samostalan početak rečenice ili odgovora.",
            "Za izričito suprotstavljanje osoba upotrijebite naglašeni oblik, primjerice njemu.",
        ],
        examples=[
            GrammarExample(
                "Poslala sam mu odgovor. — Njemu sam poslala odgovor, ne njegovoj sestri.",
                note="Naglašeni oblik omogućuje izričitu suprotnost primatelja.",
            ),
            GrammarExample(
                "Taj se prijedlog, nakon dugog razgovora sa stanarima, pokazao prihvatljivim.",
                note="Enklitika je u glavnoj cjelini; umetak ne prekida vezu prijedloga i predikata.",
            ),
        ],
        related=["hr-focus-particles-c2", "hr-register-recasting-c2"],
    ),
    GrammarTopic(
        "hr-understatement-c2",
        "Suzdržana ocjena, litota i obzirna kritika",
        "C2",
        "Pragmatičko nijansiranje",
        "Procijenite koliko blaga formulacija u danoj situaciji zapravo govori.",
        "Izraz nije loše može značiti umjerenu ili znatnu pohvalu, ovisno o "
        "govorniku i kontekstu. „Imamo mali problem” može ublažiti ozbiljnu "
        "poteškoću, ali iz samog izraza ne slijedi njezin opseg. Litota potvrđuje "
        "nešto nijekanjem suprotnoga; njezin pragmatički intenzitet nije stalan. "
        "Na poslu razjasnite konkretan problem umjesto pogađanja po tonu.",
        rules=[
            "Ne pripisujte ublaženom izrazu isti stupanj pohvale ili kritike u svim situacijama.",
            "Kad ublažavanje prikriva praktične posljedice, zatražite konkretan opis.",
        ],
        examples=[
            GrammarExample(
                "„Nije baš idealno”, rekla je gledajući poplavljenu dvoranu.",
                note="Velik nesklad sa situacijom podupire tumačenje snažnije kritike.",
            ),
            GrammarExample(
                "Kad kažete da raspored nije najsretniji, koji se termini točno preklapaju?",
                note="Odgovor pretvara suzdržanu kritiku u pitanje koje se može riješiti.",
            ),
        ],
        related=["hr-ironic-echo-c2", "hr-concessive-negotiation-c2"],
    ),
]
