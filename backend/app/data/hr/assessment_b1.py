"""Croatian B1 placement questions with balanced keys within each skill."""

from app.data._types import AssessmentQuestion

B1_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "hr-g-b1-001",
        "grammar",
        "B1",
        "Ivan kaže: Jučer sam popravljao bicikl dva sata, ali danas ga ipak moram "
        "odnijeti majstoru jer kočnice još ne rade. Što njegove riječi znače?",
        [
            "Ivan je završio popravak i želi samo provjeru.",
            "Ivan je radio na biciklu, ali problem nije riješen.",
            "Ivan je odnio bicikl majstoru prije popravka.",
            "Ivan je odgodio početak popravka za danas.",
        ],
        "Ivan je radio na biciklu, ali problem nije riješen.",
        "hr-narrative-aspect-b1",
    ),
    AssessmentQuestion(
        "hr-g-b1-002",
        "grammar",
        "B1",
        "Govorite u ime cijele skupine. Dopunite standardnim oblikom: "
        "Kad bismo počeli u osam, mi ___ ranije.",
        ["završili biste", "završio bih", "završili bi", "završili bismo"],
        "završili bismo",
        "hr-hypothetical-conditions-b1",
    ),
    AssessmentQuestion(
        "hr-g-b1-003",
        "grammar",
        "B1",
        "Dopunite: Razgovarao sam sa susjedom Anom ___ sam jučer posudio ljestve.",
        ["kojoj", "koju", "koja", "koje"],
        "kojoj",
        "hr-relative-clauses-b1",
    ),
    AssessmentQuestion(
        "hr-g-b1-004",
        "grammar",
        "B1",
        "Luka je Ani pokazao put na karti. Put zamjenjujemo s ga, a Ani s joj. "
        "Koji je standardni red nenaglasnica u rečenici Luka ___ pokazao na karti?",
        ["je ga joj", "ga joj je", "joj ga je", "joj je ga"],
        "joj ga je",
        "hr-clitic-order-b1",
    ),
    AssessmentQuestion(
        "hr-g-b1-005",
        "grammar",
        "B1",
        "Službenica se obraća skupini muškaraca i žena. Dopunite futurom drugim: "
        "Dok vi ___ obrazac, ja ću pripremiti potvrde.",
        [
            "budemo ispunjavali",
            "budete ispunjavala",
            "budete ispunjavali",
            "budu ispunjavali",
        ],
        "budete ispunjavali",
        "hr-future-second-b1",
    ),
    AssessmentQuestion(
        "hr-g-b1-006",
        "grammar",
        "B1",
        "U ponedjeljak je Ana rekla: Poslat ću dokumente sutra. U srijedu prenosite "
        "samo sadržaj njezine izjave; ne znate je li ih poslala. Koja rečenica čuva poruku?",
        [
            "Ana je u ponedjeljak rekla da će dokumente poslati u utorak.",
            "Ana je u ponedjeljak rekla da je dokumente poslala u utorak.",
            "Ana je u ponedjeljak rekla da će dokumente poslati u četvrtak.",
            "Ana je u ponedjeljak rekla da je dokumente poslala u nedjelju.",
        ],
        "Ana je u ponedjeljak rekla da će dokumente poslati u utorak.",
        "hr-reported-speech-b1",
    ),
    AssessmentQuestion(
        "hr-g-b1-007",
        "grammar",
        "B1",
        "Niste ni s jednom osobom razgovarali o promjeni termina. "
        "Kako to izraziti standardnim oblikom: O promjeni nisam razgovarao ___?",
        ["s ništa", "ni s koga", "s nikoga", "ni s kim"],
        "ni s kim",
        "hr-negative-concord-b1",
    ),
    AssessmentQuestion(
        "hr-g-b1-008",
        "grammar",
        "B1",
        "Dvorana je skuplja, ali je skupina ipak odabrala upravo nju. "
        "Dopunite: Odabrali smo je unatoč ___.",
        ["višu cijenu", "višoj cijeni", "više cijene", "višom cijenom"],
        "višoj cijeni",
        "hr-concession-b1",
    ),
    AssessmentQuestion(
        "hr-v-b1-001",
        "vocabulary",
        "B1",
        "Prvi vlak stiže u 10.15, a drugi polazi u 10.25 s drugog perona. "
        "Putnik pita: Je li deset minuta dovoljno za ___?",
        ["održavanje", "preuzimanje", "presjedanje", "ovjeravanje"],
        "presjedanje",
    ),
    AssessmentQuestion(
        "hr-v-b1-002",
        "vocabulary",
        "B1",
        "Najmodavac pri useljenju traži iznos koji će vratiti nakon pregleda stana "
        "ako nema štete ni dugovanja. Kako se zove taj iznos?",
        ["polog", "najamnina", "pristojba", "pričuva"],
        "polog",
    ),
    AssessmentQuestion(
        "hr-v-b1-003",
        "vocabulary",
        "B1",
        "Ured vam vraća zahtjev jer nedostaje potvrda o uplati. Ostali su dokumenti "
        "ispravni. Što trebate učiniti sa zahtjevom?",
        ["povući ga", "odbiti ga", "prepričati ga", "dopuniti ga"],
        "dopuniti ga",
    ),
    AssessmentQuestion(
        "hr-v-b1-004",
        "vocabulary",
        "B1",
        "Jedna skupina želi sastanak u devet, a druga u deset. "
        "Obje prihvaćaju početak u pola deset. Postigle su ___.",
        ["zamjenu", "kompromis", "održavanje", "kašnjenje"],
        "kompromis",
    ),
    AssessmentQuestion(
        "hr-v-b1-005",
        "vocabulary",
        "B1",
        "U poruci piše: Raspored je u privitku. Gdje biste ga trebali potražiti?",
        [
            "U datoteci dodanoj poruci.",
            "U naslovu primljene poruke.",
            "U adresi pošiljatelja poruke.",
            "U potpisu na kraju poruke.",
        ],
        "U datoteci dodanoj poruci.",
    ),
    AssessmentQuestion(
        "hr-v-b1-006",
        "vocabulary",
        "B1",
        "Na kraju rasprave voditelj želi u nekoliko rečenica iznijeti samo glavne "
        "odluke. Kaže: Sada ću ___ naš dogovor.",
        ["poreći", "odgoditi", "odbiti", "sažeti"],
        "sažeti",
    ),
    AssessmentQuestion(
        "hr-v-b1-007",
        "vocabulary",
        "B1",
        "Maja kaže: Mogla bih preuzeti tvoju subotnju smjenu. Što nudi kolegici?",
        [
            "Da zajedno zatraže ukidanje subotnje smjene.",
            "Da ona obavi kolegičin posao te subote.",
            "Da kolegica dođe ranije na subotnju smjenu.",
            "Da obje zamijene subotnju smjenu za nedjeljnu.",
        ],
        "Da ona obavi kolegičin posao te subote.",
    ),
    AssessmentQuestion(
        "hr-v-b1-008",
        "vocabulary",
        "B1",
        "Imate dvije moguće lokacije radionice. Voditelj vas pita zašto predlažete "
        "onu udaljeniju. Želi da svoj prijedlog ___.",
        ["proslijedite", "ovjerite", "obrazložite", "preuzmete"],
        "obrazložite",
    ),
    AssessmentQuestion(
        "hr-r-b1-001",
        "reading",
        "B1",
        "Pročitajte poruku: Zbog radova vlak završava vožnju u Karlovcu. Do Duge Rese "
        "nastavlja zamjenski autobus ispred kolodvora. Vaša karta vrijedi i u autobusu. "
        "Polazak je deset minuta nakon dolaska vlaka.\n\n"
        "Što treba učiniti putnik čije je odredište Duga Resa?",
        [
            "Ostati u vlaku do završetka radova.",
            "Kupiti novu kartu na izlazu iz kolodvora.",
            "Pričekati redoviti autobus na drugom peronu.",
            "Izaći iz vlaka i nastaviti organiziranim autobusom.",
        ],
        "Izaći iz vlaka i nastaviti organiziranim autobusom.",
    ),
    AssessmentQuestion(
        "hr-r-b1-002",
        "reading",
        "B1",
        "Pročitajte poruku najmodavca: Majstor može doći u utorak između 9 i 11. "
        "Ako tada niste kod kuće, javite mi do ponedjeljka popodne. Dogovorit ću da "
        "ga dočekam ja. Molim vas da prostor ispod sudopera bude prazan.\n\n"
        "Podstanarka u utorak radi cijelo jutro. Kako može omogućiti popravak?",
        [
            "Ostaviti stvari ispod sudopera i pričekati majstorov poziv.",
            "Najmodavcu na vrijeme javiti odsutnost i osloboditi prostor.",
            "Otkazati popravak jer najmodavac ne može ući u stan.",
            "Doći kući u podne i zamoliti majstora da do tada čeka.",
        ],
        "Najmodavcu na vrijeme javiti odsutnost i osloboditi prostor.",
    ),
    AssessmentQuestion(
        "hr-r-b1-003",
        "reading",
        "B1",
        "Pročitajte obavijest: Zahtjevi se predaju do petka. Presliku dokumenta "
        "možete poslati elektronički, a izvornik ćete pokazati pri preuzimanju potvrde. "
        "O datumu preuzimanja obavijestit ćemo vas nakon obrade zahtjeva.\n\n"
        "Što osoba koja danas ima samo presliku može zaključiti?",
        [
            "Presliku mora najprije zamijeniti ovjerenim dokumentom.",
            "Izvornik mora poslati elektronički zajedno s preslikom.",
            "Može predati zahtjev sada, a izvornik pokazati poslije.",
            "Potvrdu može preuzeti u petak bez dodatne obavijesti.",
        ],
        "Može predati zahtjev sada, a izvornik pokazati poslije.",
    ),
    AssessmentQuestion(
        "hr-r-b1-004",
        "reading",
        "B1",
        "Pročitajte razgovor: Petra kaže: Mogu zamijeniti smjenu u subotu, ali samo "
        "ako završim do dva. Ivan odgovara: U redu, ja ću preuzeti posao od dva do "
        "zatvaranja. Petra dodaje: Još trebamo potvrdu voditeljice pa ti se javim.\n\n"
        "Kakav je trenutačni status dogovora?",
        [
            "Raspodijelili su sate, ali promjena još nije odobrena.",
            "Dogovor je konačan i voditeljica je već obaviještena.",
            "Petra će raditi do zatvaranja ako Ivan ne stigne.",
            "Ivan čeka da Petra odluči može li raditi poslije dva.",
        ],
        "Raspodijelili su sate, ali promjena još nije odobrena.",
    ),
    AssessmentQuestion(
        "hr-r-b1-005",
        "reading",
        "B1",
        "Pročitajte poruku: Jučer sam vam poslala nacrt rasporeda. Danas mi je Ana "
        "javila da petkom ipak ne može dolaziti. Molim vas da zasad ne prosljeđujete "
        "jučerašnju verziju polaznicima. Novu ću poslati čim uskladimo termine.\n\n"
        "Zašto treba pričekati prije obavještavanja polaznika?",
        [
            "Polaznici su već dobili izmijenjeni raspored od Ane.",
            "Ana će sama potvrditi svaki termin polaznicima.",
            "Poslana verzija treba promjenu zbog nove informacije.",
            "Autorica poruke nije sigurna je li nacrt uopće poslan.",
        ],
        "Poslana verzija treba promjenu zbog nove informacije.",
    ),
    AssessmentQuestion(
        "hr-r-b1-006",
        "reading",
        "B1",
        "Pročitajte poruku udruge: Dvorana A je jeftinija, ali do ulaza vode stepenice "
        "i nema dizala. Dvorana B ima ulaz bez stepenica i blizu je autobusne stanice. "
        "Iako je skuplja, odabrali smo je jer nekoliko sudionika koristi invalidska "
        "kolica.\n\nŠto je najviše utjecalo na izbor?",
        [
            "Veći broj slobodnih termina u skupljoj dvorani.",
            "Mogućnost da svi prijavljeni sudionici dođu i uđu.",
            "Želja da se izbjegne putovanje javnim prijevozom.",
            "Potreba da se smanji ukupan trošak radionice.",
        ],
        "Mogućnost da svi prijavljeni sudionici dođu i uđu.",
    ),
    AssessmentQuestion(
        "hr-r-b1-007",
        "reading",
        "B1",
        "Pročitajte poruku: Marko, kad sam rekla da doneseš stolice u petak, mislila "
        "sam na petak prije priredbe, 18. lipnja. Ovaj petak dvorana još nije slobodna. "
        "Oprosti, trebala sam odmah napisati datum. Javi odgovara li ti novi dogovor.\n\n"
        "Što pošiljateljica želi postići?",
        [
            "Premjestiti priredbu na ovaj petak i zamijeniti dvoranu.",
            "Obavijestiti Marka da stolice za priredbu više nisu potrebne.",
            "Potvrditi da je Marko već prihvatio dostavu 18. lipnja.",
            "Razjasniti dan dostave i provjeriti može li Marko tada doći.",
        ],
        "Razjasniti dan dostave i provjeriti može li Marko tada doći.",
    ),
    AssessmentQuestion(
        "hr-r-b1-008",
        "reading",
        "B1",
        "Pročitajte poruku organizatora: Ako sutra bude padala kiša, prvo ćemo u "
        "dvorani pripremiti oznake za biljke. Kad se vrijeme popravi, nastavit ćemo "
        "sadnju vani. Zato ponesite obuću za vrt čak i ako ujutro bude oblačno.\n\n"
        "Što sudionici mogu očekivati ako ujutro pada kiša, a popodne se razvedri?",
        [
            "Aktivnosti će početi unutra, a zatim će se preseliti u vrt.",
            "Cijeli će se program održati u dvorani bez izlaska.",
            "Sadnja će se odgoditi, a oznake će izraditi kod kuće.",
            "Program će početi tek popodne izravno u vrtu.",
        ],
        "Aktivnosti će početi unutra, a zatim će se preseliti u vrt.",
    ),
]
