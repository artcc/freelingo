"""Croatian A1 spelling, pronunciation and functional grammar."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "hr-alphabet-a1",
        "Hrvatska abeceda",
        "A1",
        "Pisanje i izgovor",
        "Prepoznaj hrvatska slova i pravilno zapiši svoje ime.",
        "Hrvatski pišemo latinicom. Abeceda ima 30 slova: a, b, c, č, ć, d, dž, đ, "
        "e, f, g, h, i, j, k, l, lj, m, n, nj, o, p, r, s, š, t, u, v, z, ž. "
        "Dvoslovi dž, lj i nj imaju po dva znaka, ali svaki je jedno slovo abecede.\n\n"
        "Č, ć, đ, š i ž nisu isto što i c, d, s i z. Znakove treba zadržati i u porukama. "
        "Imena ljudi i mjesta pišemo velikim početnim slovom: Đurđa, Šibenik. "
        "Nazive jezika pišemo malim slovom: hrvatski.",
        rules=[
            "Pri slovkanju razlikuj č od ć te dž od đ.",
            "Na početku imena pišemo Lj, Nj i Dž: Ljiljana, Njivice, Dživo.",
            "U uobičajenom tekstu ne dodajemo znakove za naglasak.",
        ],
        examples=[
            GrammarExample("Ja sam Đurđa.", note="Ime počinje velikim slovom Đ."),
            GrammarExample("Ovo je Ljiljana.", note="Lj je dvoslov na početku imena."),
            GrammarExample("Učim hrvatski.", note="Naziv jezika počinje malim slovom."),
        ],
        related=["hr-sounds-a1"],
    ),
    GrammarTopic(
        "hr-sounds-a1",
        "Glasovi, slogovi i slušanje",
        "A1",
        "Pisanje i izgovor",
        "Slušaj razlike među glasovima i ponavljaj cijele riječi.",
        "Samoglasnici su a, e, i, o i u. U riječi prst slog nosi r; ne treba dodavati "
        "samoglasnik između p i r. U riječima ljubav, njega i džep dvoslovi lj, nj i dž "
        "označuju po jedan glas.\n\n"
        "U standardnom izgovoru razlikujemo č i ć te dž i đ. Č i dž izgovaraju se tvrđe, "
        "a ć i đ mekše. Slušaj parove čar – ćar i džak – đak. Regionalni izgovori mogu "
        "se razlikovati. Hrvatski naglasak nije uvijek na prvom slogu; mjesto, duljinu i "
        "ton uči slušanjem poznatih riječi, bez zaključivanja iz običnog zapisa.\n\n"
        "Standardni hrvatski ima ijekavske oblike. Zapis ije ili je uči uz riječ: "
        "mlijeko, dijete, vrijeme, ali mjesto i pjesma. Ne zamjenjuj svaki je skupom ije.",
        rules=[
            "Š i ž nisu isti glasovi kao s i z: slušaj šal i žaba.",
            "Ne izgovaraj lj u ljubav kao odvojeno l pa j.",
            "Dijakritički znak u č ili š ne označuje naglasak.",
        ],
        examples=[
            GrammarExample("Ovo je džep.", note="U riječi džep dvoslov dž označuje jedan glas."),
            GrammarExample("Njegovo ime je Đuro.", note="Slušaj nj i đ kao različite glasove."),
            GrammarExample("To je prst.", note="R nosi slog; nema dodatnog samoglasnika."),
        ],
        related=["hr-alphabet-a1"],
    ),
    GrammarTopic(
        "hr-biti-a1",
        "Ja sam, ti si, mi smo",
        "A1",
        "Glagoli i zamjenice",
        "Predstavi se glagolom biti i odaberi ti ili vi.",
        "Osobne zamjenice u jednini su ja, ti, on, ona i ono, a u množini mi, vi, "
        "oni, one i ona. Oblik ona uz je označuje ženski rod jednine, a uz su "
        "srednji rod množine. "
        "Nenaglašeni oblici glagola biti u prezentu su sam, si, je, smo, ste, su. "
        "Zamjenicu često izostavljamo: Ja sam Ana. / Ana sam.\n\n"
        "Kratki oblici poput sam i smo ne stoje sami na početku obične izjavne rečenice. "
        "Kažemo: Mi smo ovdje. / Ovdje smo. Jednom prijatelju govorimo ti, a nepoznatoj "
        "odrasloj osobi obično vi. Za uljudno obraćanje upotrebljavamo ste.",
        structure="ja sam · ti si · on/ona/ono je · mi smo · vi ste · oni/one/ona su",
        rules=[
            "U rečenici Ja sam student ne izostavljaj glagol sam.",
            "Vi ste može se odnositi na više ljudi ili uljudno na jednu osobu.",
            "Zovem se Ana nauči kao izraz za predstavljanje.",
        ],
        examples=[
            GrammarExample("Ja sam Ivan.", note="Uz ja upotrebljavamo sam."),
            GrammarExample("Dobar dan, jeste li vi gospodin Horvat?", note="Uljudno obraćanje."),
            GrammarExample("Ovdje smo.", note="Smo dolazi iza prve naglašene riječi."),
        ],
        common_mistakes=[
            GrammarMistake("Ja je Ana.", "Ja sam Ana.", "Oblik je pripada trećoj osobi jednine.")
        ],
        related=["hr-questions-a1", "hr-negation-a1"],
    ),
    GrammarTopic(
        "hr-gender-a1",
        "Muški, ženski i srednji rod",
        "A1",
        "Imenice",
        "Uči imenicu zajedno s njezinim rodom.",
        "Imenice imaju muški, ženski ili srednji rod: ovaj stol, ova kuća, ovo selo. "
        "Hrvatski nema članove; ovaj, ova i ovo pokazuju na nešto i nisu obvezni uz imenicu.\n\n"
        "Mnoge imenice muškog roda završavaju suglasnikom, ženskog na -a, a srednjeg "
        "na -o ili -e. To je pomoć, a ne pravilo bez iznimaka: tata je muškog roda, "
        "noć ženskog, a dijete srednjeg.\n\n"
        "U nominativu množine česti su oblici studenti, kuće i sela. Kratke muške "
        "imenice često imaju dulju osnovu: stol — stolovi, ključ — ključevi. "
        "Posebne oblike uči uz riječ: čovjek — ljudi, dijete — djeca.",
        rules=[
            "Uz novu imenicu zapamti rod: grad — muški, soba — ženski, more — srednji.",
            "Rod se ne određuje uvijek prema završnom slovu.",
            "Za množinu uči konkretne oblike: stolovi, kuće, sela.",
        ],
        examples=[
            GrammarExample("Ovo je moj tata.", note="Tata je muškog roda iako završava na -a."),
            GrammarExample("Ova soba je velika.", note="Soba je ženskog roda."),
        ],
        related=["hr-agreement-a1", "hr-possessives-a1"],
    ),
    GrammarTopic(
        "hr-agreement-a1",
        "Mala soba, mali stan",
        "A1",
        "Pridjevi",
        "Uskladi pridjev s imenicom koju opisuje.",
        "Pridjev se slaže s imenicom u rodu, broju i padežu. Za početak opisujemo "
        "osobu ili stvar u nominativu: mali stan, mala soba, malo selo. "
        "Česti nastavci u množini su -i, -e i -a: mali stanovi, male sobe, mala sela.\n\n"
        "U predikatu su česti oblici bez završnog -i u muškom rodu: Stan je malen. "
        "Grad je velik. Oblici pridjeva mogu se razlikovati: dobar čovjek, dobra osoba. "
        "Uči kratke, potpune izraze.",
        rules=[
            "Za ženski rod često upotrebljavamo -a, a za srednji -o ili -e.",
            "Množina nije jednaka za sve rodove: novi stolovi, nove torbe, nova sela.",
            "Pri opisu mijenjaj pridjev zajedno s imenicom.",
        ],
        examples=[
            GrammarExample(
                "To je nova torba.", note="Nova se slaže s imenicom torba u ženskom rodu."
            ),
            GrammarExample("Ovo su nova sela.", note="Nova je ovdje srednji rod množine."),
        ],
        related=["hr-gender-a1", "hr-accusative-a1"],
    ),
    GrammarTopic(
        "hr-possessives-a1",
        "Moj, tvoj, naš i vaš",
        "A1",
        "Zamjenice",
        "Reci komu nešto pripada.",
        "Posvojne zamjenice pokazuju pripadanje: moj, tvoj, njegov, njezin, naš, vaš, "
        "njihov. Njihov oblik ovisi o imenici uz koju stoje: moj brat, moja sestra, "
        "moje dijete. Spol osobe koja govori ne mijenja taj izbor.\n\n"
        "Pitanje za pripadanje glasi čiji, čija ili čije: Čija je ovo torba? "
        "To je moja torba. Za uljudno obraćanje jednoj osobi upotrebljavamo vaš: "
        "Je li ovo vaša torba?",
        rules=[
            "Uz imenicu ženskog roda upotrijebi moja, tvoja, naša ili vaša.",
            "I muškarac i žena kažu moj telefon i moja adresa.",
            "Uči oblike zajedno s imenicom: njegov stan, njezina soba, njihovo selo.",
        ],
        examples=[
            GrammarExample("Ovo je naša kuća.", note="Naša se slaže s imenicom kuća."),
            GrammarExample("Čiji je ovo ključ?", note="Čiji odgovara muškom rodu imenice ključ."),
        ],
        related=["hr-gender-a1", "hr-agreement-a1"],
    ),
    GrammarTopic(
        "hr-present-a1",
        "Što radiš svaki dan?",
        "A1",
        "Glagoli",
        "Prezentom opiši sadašnju radnju i naviku.",
        "Prezent služi za radnje sada i za navike: Sada čitam. Svaki dan radim. "
        "Različiti glagoli imaju različite obrasce: čitati — čitam, čitaš, čita, "
        "čitamo, čitate, čitaju; raditi — radim, radiš, radi, radimo, radite, rade.\n\n"
        "Uči infinitiv i prvi oblik prezenta zajedno. Nije dovoljno svakom glagolu "
        "dodati isti nastavak: piti — pijem, ići — idem. Zamjenica često nije potrebna "
        "jer oblik pokazuje osobu: Čitamo. Radite li?",
        rules=[
            "U trećoj osobi množine razlikuj čitaju, rade i piju.",
            "Za navike koristi izraze svaki dan, često ili obično.",
            "Biti ima posebne oblike: sam, si, je, smo, ste, su.",
        ],
        examples=[
            GrammarExample("Čitam poruku.", note="Čitam označuje prvu osobu jednine."),
            GrammarExample("Ana i Marko rade.", note="Dvije osobe traže treću osobu množine."),
        ],
        related=["hr-biti-a1", "hr-negation-a1", "hr-reflexive-a1"],
    ),
    GrammarTopic(
        "hr-questions-a1",
        "Tko, što, gdje i li",
        "A1",
        "Pitanja",
        "Traži osobu, stvar, mjesto ili potvrdu.",
        "Tko pita za osobu, što za stvar ili radnju, gdje za mjesto, a kako za način "
        "ili stanje: Tko je to? Što radiš? Gdje radiš? Kako si?\n\n"
        "Za odgovor da ili ne često stavljamo li iza glagola: Govorite li hrvatski? "
        "Kod glagola biti upotrebljavamo jesam li, jesi li, je li, jesmo li, jeste li, "
        "jesu li. U razgovoru se pitanje može označiti i intonacijom: Vi ste Ana?",
        rules=[
            "Česticu li pišemo odvojeno: Je li to vaš ključ?",
            "Koliko pita za broj ili cijenu: Koliko košta?",
            "U standardnim pitanjima razlikuj gdje za mjesto i kamo za odredište.",
        ],
        examples=[
            GrammarExample("Gdje stanuješ?", note="Tražimo mjesto stanovanja."),
            GrammarExample("Jeste li vi učiteljica?", note="Jeste li uvodi pitanje s biti."),
        ],
        related=["hr-biti-a1", "hr-destination-a1"],
    ),
    GrammarTopic(
        "hr-negation-a1",
        "Ne radim, nisam, nemam",
        "A1",
        "Nijekanje",
        "Izreci jednostavan negativan odgovor.",
        "Većinu glagola niječemo odvojenom riječju ne: ne radim, ne čitam, ne razumijem. "
        "Glagol biti ima posebne niječne oblike: nisam, nisi, nije, nismo, niste, nisu.\n\n"
        "Niječni oblici glagola imati pišu se zajedno: nemam, nemaš, nema, nemamo, "
        "nemate, nemaju. Kratak odgovor može glasiti: Ne, nisam. / Ne, nemam. "
        "Niječni oblik sam po sebi ne zahtijeva još jedno ne.",
        rules=[
            "Piši ne znam odvojeno.",
            "Piši nisam i nemam zajedno.",
            "Niječnim oblikom zadrži osobu: mi radimo — mi ne radimo.",
        ],
        examples=[
            GrammarExample("Ne razumijem pitanje.", note="Ne stoji odvojeno ispred glagola."),
            GrammarExample("Nisam liječnik.", note="Nisam je niječni oblik za ja."),
        ],
        common_mistakes=[
            GrammarMistake("Ne imam kartu.", "Nemam kartu.", "Imati ima oblik nemam.")
        ],
        related=["hr-present-a1", "hr-biti-a1"],
    ),
    GrammarTopic(
        "hr-numbers-a1",
        "Brojevi, cijene i telefonski broj",
        "A1",
        "Brojevi",
        "Pročitaj osnovne brojeve i prepoznaj cijenu.",
        "Počni brojevima nula, jedan, dva, tri, četiri, pet, šest, sedam, osam, devet, "
        "deset. Zatim uči jedanaest, dvanaest, trinaest, četrnaest, petnaest, šesnaest, "
        "sedamnaest, osamnaest, devetnaest, dvadeset, trideset, četrdeset, "
        "pedeset, šezdeset, sedamdeset, osamdeset, devedeset i sto. "
        "Višečlane brojeve pišemo odvojeno: dvadeset jedan.\n\n"
        "Jedan se slaže s imenicom: jedan euro, jedna karta, jedno mjesto. "
        "Uz dva razlikujemo dva eura i dvije karte. Za cijene nauči izraze jedan euro, "
        "dva eura, pet eura. Telefonski broj možeš čitati znamenku po znamenku.",
        rules=[
            "Uz ženski rod upotrebljavamo jedna i dvije.",
            "Nakon tri i četiri kažemo eura, a nakon pet do deset također eura.",
            "Zapis 2,50 € znači dva eura i pedeset centi.",
        ],
        examples=[
            GrammarExample("Kava košta dva eura.", note="Cijena s brojem dva."),
            GrammarExample("Ovdje su dvije karte.", note="Uz ženski rod koristimo oblik dvije."),
        ],
        related=["hr-accusative-a1", "hr-time-a1"],
    ),
    GrammarTopic(
        "hr-accusative-a1",
        "Želim kavu: osnovni akuzativ",
        "A1",
        "Padeži",
        "Imenuj ono što želiš, imaš ili kupuješ.",
        "Akuzativ često označuje izravni objekt: Kupujem kruh. Želim kavu. "
        "Imenice ženskog roda na -a obično dobivaju -u: voda — vodu, karta — kartu. "
        "Kod muškog roda za neživo oblik je često jednak nominativu: kruh — kruh.\n\n"
        "Muške imenice za živo često imaju -a: Vidim prijatelja. Vidim psa. "
        "Kod srednjeg roda oblik je često isti: Želim mlijeko. Pridjev i zamjenica "
        "također se mijenjaju: jedna mala kava — jednu malu kavu.\n\n"
        "U množini muške imenice često imaju -e i za živo i za neživo: vidim "
        "prijatelje, kupujem stolove. Ženske imenice na -a imaju -e: kupujem jabuke. "
        "Srednji rod obično zadržava oblik nominativa množine: vidim sela. "
        "Uči cijele skupine: vidim dobre prijatelje, kupujem nove torbe.",
        rules=[
            "Za osnovni objekt pitamo koga ili što: Koga vidiš? Što kupuješ?",
            "Ne dodaj -a svakoj muškoj imenici: kupujem kruh, ali vidim prijatelja.",
            "Vježbaj cijelu skupinu: tvoja torba — vidim tvoju torbu.",
        ],
        examples=[
            GrammarExample("Molim jednu malu kavu.", note="Ženski oblici završavaju na -u."),
            GrammarExample("Imam telefon.", note="Telefon označuje neživo i ne mijenja oblik."),
        ],
        related=["hr-gender-a1", "hr-agreement-a1", "hr-destination-a1"],
    ),
    GrammarTopic(
        "hr-polite-a1",
        "Molim, hvala i oprostite",
        "A1",
        "Uljudna komunikacija",
        "Zatraži nešto jasno i pristojno.",
        "Molim ublažava zahtjev: Kavu, molim. Molim račun. Hvala izražava zahvalnost, "
        "a oprostite privlači pozornost ili uvodi ispriku. Prijatelju kažemo oprosti, "
        "a nepoznatoj odrasloj osobi oprostite.\n\n"
        "Za početak nauči cijele izraze: Možete li ponoviti? Govorite li engleski? "
        "Ne razumijem. Za molbu nije potrebno govoriti glasnije; važni su jasan izraz "
        "i prikladno obraćanje.",
        rules=[
            "Uz nepoznatu odraslu osobu obično koristi vi i glagolski oblik za vi.",
            "Molim može stajati prije ili poslije narudžbe.",
            "Na hvala možeš odgovoriti nema na čemu.",
        ],
        examples=[
            GrammarExample("Račun, molim.", note="Kratka uljudna molba u kafiću."),
            GrammarExample(
                "Oprostite, možete li ponoviti?", note="Tražimo ponavljanje od sugovornika."
            ),
        ],
        related=["hr-questions-a1", "hr-modals-a1"],
    ),
    GrammarTopic(
        "hr-locative-a1",
        "Gdje? U gradu i na trgu",
        "A1",
        "Padeži i prijedlozi",
        "Reci gdje se netko ili nešto nalazi.",
        "Za mjesto uz u i na često upotrebljavamo lokativ: u gradu, u školi, na trgu. "
        "Lokativ uvijek dolazi s prijedlogom. U čestim imenicama muškog i srednjeg roda "
        "nalazimo -u, a kod ženskih na -a nastavak -i: park — u parku, selo — u selu, "
        "soba — u sobi.\n\n"
        "Prijedlog u ili na uči uz mjesto: u trgovini, u Zagrebu, na tržnici, na plaži. "
        "Ne određuje se svaki izbor samo prema tome je li prostor zatvoren ili otvoren.",
        rules=[
            "Pitanje gdje traži mjesto: Gdje si? U hotelu.",
            "Uči promjene u čestim riječima: banka — u banci.",
            "Za neke izraze koristimo druge oblike: kod kuće je ustaljen izraz.",
        ],
        examples=[
            GrammarExample("Ana je u školi.", note="Školi označuje mjesto uz prijedlog u."),
            GrammarExample("Mi smo na trgu.", note="Uz trg učimo prijedlog na i oblik trgu."),
        ],
        related=["hr-destination-a1", "hr-gender-a1"],
    ),
    GrammarTopic(
        "hr-destination-a1",
        "Kamo? Idem u grad",
        "A1",
        "Kretanje",
        "Razlikuj mjesto od odredišta.",
        "Za odredište uz u i na upotrebljavamo akuzativ: Idem u školu. Idemo na plažu. "
        "Usporedi: U školi sam. / Idem u školu. Na trgu sam. / Idem na trg.\n\n"
        "Glagol ići u prezentu glasi idem, ideš, ide, idemo, idete, idu. "
        "Pitanje kamo pita za odredište. Za povratak kući često kažemo idem kući, "
        "bez prijedloga. Taj izraz nauči kao cjelinu.",
        rules=[
            "Uz u i na mjesto odgovara na gdje, a odredište na kamo.",
            "U i na ostaju isti, ali padež se mijenja: u trgovini — u trgovinu.",
            "Ići samo po sebi ne govori uvijek kojim prijevoznim sredstvom putujemo.",
        ],
        examples=[
            GrammarExample(
                "Idem u Zagreb.", note="Zagreb je odredište; akuzativ nema novi nastavak."
            ),
            GrammarExample("Idemo na tržnicu.", note="Tržnica u akuzativu postaje tržnicu."),
        ],
        related=["hr-accusative-a1", "hr-locative-a1", "hr-present-a1"],
    ),
    GrammarTopic(
        "hr-time-a1",
        "Koliko je sati? Kada se vidimo?",
        "A1",
        "Vrijeme",
        "Pročitaj vrijeme i dogovori dan susreta.",
        "Za vrijeme pitamo Koliko je sati? Kažemo: Jedan je sat. Dva su sata. "
        "Pet je sati. Digitalni zapis može se čitati brojevima: 14:30 — četrnaest i "
        "trideset. U razgovoru se često kaže pola tri za 14:30 ili 2:30; dio dana "
        "razjašnjava značenje.\n\n"
        "Za dogovor koristimo u: Vidimo se u pet. Radim u ponedjeljak. "
        "Uči izraze u ponedjeljak, u utorak, u srijedu, u četvrtak, u petak, "
        "u subotu, u nedjelju. Danas, sutra i jučer ne trebaju prijedlog.",
        rules=[
            "Razlikuj vrijeme na satu od vremena susreta: Pet je sati. / Dolazim u pet.",
            "Za pola tri misli na pola sata prije tri, ne poslije tri.",
            "U rasporedima je čest zapis od 0 do 23 sata.",
        ],
        examples=[
            GrammarExample("Vidimo se u subotu u deset.", note="Navodimo dan i sat susreta."),
            GrammarExample(
                "Sada je pola osam.", note="To znači 7:30 ili 19:30, ovisno o dijelu dana."
            ),
        ],
        related=["hr-numbers-a1", "hr-reflexive-a1"],
    ),
    GrammarTopic(
        "hr-reflexive-a1",
        "Zovem se i odmaram se",
        "A1",
        "Glagoli",
        "Ne izostavljaj riječ se uz glagole koji je trebaju.",
        "Neki glagoli dolaze s riječju se: zvati se, odmarati se, tuširati se, "
        "osjećati se. Glagol mijenja oblik, a se ostaje isto: odmaram se, odmaraš se, "
        "odmaramo se.\n\n"
        "U kratkoj rečenici se obično dolazi iza prve naglašene riječi ili skupine: "
        "Odmaram se. / Ja se odmaram. Pitanje glasi Kako se zoveš? "
        "Se nije dodatak svakom glagolu: kažemo Čitam knjigu.",
        rules=[
            "Se pišemo odvojeno od glagola.",
            "U pitanjima s li kažemo Odmaraš li se?",
            "Zvati nekoga i zvati se nemaju isto značenje: Zovem Anu. / Zovem se Ana.",
        ],
        examples=[
            GrammarExample("Ujutro se tuširam.", note="Se dolazi iza početnog ujutro."),
            GrammarExample("Kako se osjećate?", note="Osjećati se koristimo za vlastito stanje."),
        ],
        related=["hr-present-a1", "hr-questions-a1"],
    ),
    GrammarTopic(
        "hr-modals-a1",
        "Mogu, moram i želim",
        "A1",
        "Glagoli",
        "Izrazi mogućnost, obvezu i želju.",
        "Mogu označuje mogućnost ili sposobnost, moram obvezu, a želim želju. "
        "Uz njih često dolazi infinitiv: Mogu čekati. Moram raditi. Želim jesti. "
        "Osoba se vidi na prvom glagolu; infinitiv ostaje isti.\n\n"
        "Moći ima oblike mogu, možeš, može, možemo, možete, mogu. "
        "Morati: moram, moraš, mora, moramo, morate, moraju. "
        "Željeti: želim, želiš, želi, želimo, želite, žele.",
        rules=[
            "Ne mogu pišemo odvojeno.",
            "Ne moram znači da nemam obvezu, a ne da je radnja zabranjena.",
            "Možete li pomoći? uljudna je molba.",
        ],
        examples=[
            GrammarExample("Moram kupiti lijek.", note="Kupiti ostaje u infinitivu."),
            GrammarExample("Ne mogu doći danas.", note="Govornik nema mogućnost doći."),
        ],
        related=["hr-polite-a1", "hr-negation-a1"],
    ),
    GrammarTopic(
        "hr-coordination-a1",
        "I, ali i ili",
        "A1",
        "Povezivanje rečenica",
        "Poveži dvije jednostavne informacije.",
        "I dodaje informaciju: Imam kartu i putovnicu. Ali pokazuje suprotnost: "
        "Želim doći, ali ne mogu. Ili nudi izbor: Želite li čaj ili kavu?\n\n"
        "Povezivati možemo riječi ili kratke rečenice. Zadrži jasno značenje: "
        "Ana čita, a Ivan piše. A ovdje uspoređuje dvije osobe i njihove radnje.",
        rules=[
            "I upotrebljavamo za dodavanje, a ili za izbor.",
            "Ispred ali i a obično pišemo zarez.",
            "Ispred jednog i ili ili pri običnom nabrajanju ne pišemo zarez.",
        ],
        examples=[
            GrammarExample("Boli me glava i trebam odmor.", note="I povezuje dvije informacije."),
            GrammarExample(
                "Imam telefon, ali nemam punjač.", note="Ali uvodi suprotnu informaciju."
            ),
        ],
        related=["hr-negation-a1", "hr-modals-a1"],
    ),
]
