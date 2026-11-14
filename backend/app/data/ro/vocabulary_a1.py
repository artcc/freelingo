"""Romanian A1 vocabulary: seven sets of twenty-eight contextualised entries."""

from app.data._types import VocabularyEntry, VocabularySet

A1_SETS: list[VocabularySet] = [
    VocabularySet(
        "ro_first_contact_a1",
        "A1",
        "Primul contact și date personale",
        "a1-unit-1",
        [
            VocabularyEntry(
                "nume",
                "noun",
                "Cuvânt prin care este identificată o persoană.",
                "Numele meu este Ana.",
            ),
            VocabularyEntry(
                "prenume",
                "noun",
                "Nume personal, precum Ana sau Mihai.",
                "Prenumele meu este Mihai.",
            ),
            VocabularyEntry("persoană", "noun", "Un om.", "Această persoană este din Iași."),
            VocabularyEntry(
                "țară",
                "noun",
                "Teritoriu cu un stat și o populație.",
                "România este o țară europeană.",
            ),
            VocabularyEntry(
                "oraș",
                "noun",
                "Localitate mare, cu multe străzi și clădiri.",
                "Brașov este un oraș.",
            ),
            VocabularyEntry(
                "România", "noun", "Țară cu capitala la București.", "Sunt din România."
            ),
            VocabularyEntry(
                "română", "noun", "Limba vorbită în România.", "Acest cuvânt este în română."
            ),
            VocabularyEntry(
                "limbă",
                "noun",
                "Sistem de cuvinte folosit pentru comunicare.",
                "Româna este o limbă.",
            ),
            VocabularyEntry(
                "cuvânt", "noun", "Unitate de limbă cu un sens.", "Casă este un cuvânt."
            ),
            VocabularyEntry("literă", "noun", "Semn scris pentru un sunet.", "Ă este o literă."),
            VocabularyEntry(
                "sunet",
                "noun",
                "Ceea ce auzim când vorbim sau ascultăm.",
                "Ș este un sunet din română.",
            ),
            VocabularyEntry(
                "întrebare",
                "noun",
                "Ceea ce spunem pentru a cere o informație.",
                "Cine ești? este o întrebare.",
            ),
            VocabularyEntry(
                "răspuns", "noun", "Informație dată după o întrebare.", "Da este un răspuns scurt."
            ),
            VocabularyEntry(
                "salut",
                "noun",
                "Cuvânt sau gest la întâlnire ori la despărțire.",
                "Bună este un salut.",
            ),
            VocabularyEntry(
                "bună ziua",
                "phrase",
                "Salut politicos folosit în timpul zilei.",
                "Bună ziua, doamna Popescu!",
            ),
            VocabularyEntry(
                "la revedere",
                "phrase",
                "Formulă spusă la despărțire.",
                "La revedere, domnule Ionescu!",
            ),
            VocabularyEntry(
                "mulțumesc",
                "phrase",
                "Cuvânt prin care arătăm că apreciem un ajutor.",
                "Mulțumesc pentru răspuns.",
            ),
            VocabularyEntry(
                "vă rog",
                "phrase",
                "Formulă politicoasă care însoțește o cerere.",
                "Numele, vă rog.",
            ),
            VocabularyEntry("da", "phrase", "Răspuns prin care confirmăm ceva.", "Da, sunt Ana."),
            VocabularyEntry("nu", "adverb", "Cuvânt prin care negăm ceva.", "Nu sunt profesor."),
            VocabularyEntry(
                "eu", "pronoun", "Persoana care vorbește despre sine.", "Eu sunt din Sibiu."
            ),
            VocabularyEntry(
                "tu", "pronoun", "Persoana căreia îi vorbim familiar.", "Tu ești Radu."
            ),
            VocabularyEntry(
                "dumneavoastră",
                "pronoun",
                "Formă de adresare politicoasă.",
                "Dumneavoastră sunteți medic?",
            ),
            VocabularyEntry(
                "a fi", "verb", "Verb folosit pentru identitate, stare sau loc.", "Sunt aici."
            ),
            VocabularyEntry(
                "aici", "adverb", "În acest loc, aproape de vorbitor.", "Ana este aici."
            ),
            VocabularyEntry(
                "acolo", "adverb", "Într-un loc mai îndepărtat de vorbitor.", "Radu este acolo."
            ),
            VocabularyEntry(
                "profesor", "noun", "Persoană care predă o materie.", "El este profesor."
            ),
            VocabularyEntry(
                "student", "noun", "Persoană care învață la universitate.", "Sunt student la Cluj."
            ),
        ],
    ),
    VocabularySet(
        "ro_people_home_a1",
        "A1",
        "Familie și locuință",
        "a1-unit-2",
        [
            VocabularyEntry(
                "familie", "noun", "Grup de persoane legate prin rudenie.", "Aici este o familie."
            ),
            VocabularyEntry("mamă", "noun", "Părinte de sex feminin.", "Mama este acasă."),
            VocabularyEntry("tată", "noun", "Părinte de sex masculin.", "Tatăl este aici."),
            VocabularyEntry(
                "frate",
                "noun",
                "Băiat sau bărbat cu aceiași părinți ca altă persoană.",
                "Aici sunt doi frați.",
            ),
            VocabularyEntry(
                "soră",
                "noun",
                "Fată sau femeie cu aceiași părinți ca altă persoană.",
                "Aici sunt două surori.",
            ),
            VocabularyEntry("bunic", "noun", "Tatăl mamei sau al tatălui.", "Bunicul este acasă."),
            VocabularyEntry(
                "bunică", "noun", "Mama mamei sau a tatălui.", "Bunica este din Sibiu."
            ),
            VocabularyEntry(
                "copil", "noun", "Persoană aflată la începutul vieții.", "Aici sunt doi copii."
            ),
            VocabularyEntry(
                "soț",
                "noun",
                "Bărbat căsătorit, în relație cu partenerul său.",
                "Soțul este acasă.",
            ),
            VocabularyEntry(
                "soție",
                "noun",
                "Femeie căsătorită, în relație cu partenerul său.",
                "Soția este aici.",
            ),
            VocabularyEntry(
                "prieten",
                "noun",
                "Persoană apropiată cu care petrecem timp.",
                "Mihai este un prieten.",
            ),
            VocabularyEntry(
                "băiat", "noun", "Copil sau tânăr de sex masculin.", "Băiatul este aici."
            ),
            VocabularyEntry("fată", "noun", "Copil sau tânără de sex feminin.", "Fata este Ana."),
            VocabularyEntry(
                "bărbat", "noun", "Persoană adultă de sex masculin.", "Bărbatul este profesor."
            ),
            VocabularyEntry(
                "femeie", "noun", "Persoană adultă de sex feminin.", "Femeia este medic."
            ),
            VocabularyEntry(
                "casă", "noun", "Clădire în care locuiesc oameni.", "Aici este o casă."
            ),
            VocabularyEntry(
                "apartament",
                "noun",
                "Locuință cu camere într-o clădire.",
                "Aici este un apartament.",
            ),
            VocabularyEntry(
                "cameră",
                "noun",
                "Parte a unei locuințe, separată prin pereți.",
                "Aici sunt două camere.",
            ),
            VocabularyEntry(
                "bucătărie", "noun", "Încăpere în care pregătim mâncarea.", "Bucătăria este aici."
            ),
            VocabularyEntry("baie", "noun", "Încăpere în care ne spălăm.", "Baia este aici."),
            VocabularyEntry("ușă", "noun", "Parte mobilă care închide intrarea.", "Ușa este aici."),
            VocabularyEntry(
                "fereastră", "noun", "Deschidere cu geam într-un perete.", "Fereastra este aici."
            ),
            VocabularyEntry(
                "masă",
                "noun",
                "Mobilă pe care punem lucruri sau mâncăm.",
                "Aici sunt o masă și două scaune.",
            ),
            VocabularyEntry(
                "scaun", "noun", "Mobilă pe care stă o persoană.", "Aici este un scaun."
            ),
            VocabularyEntry("pat", "noun", "Mobilă în care dormim.", "Aici sunt două paturi."),
            VocabularyEntry(
                "dulap", "noun", "Mobilă în care păstrăm haine sau obiecte.", "Dulapul este aici."
            ),
            VocabularyEntry(
                "cheie", "noun", "Obiect cu care încuiem sau descuiem.", "Cheile sunt aici."
            ),
            VocabularyEntry("acasă", "adverb", "În locuința proprie sau spre ea.", "Suntem acasă."),
        ],
    ),
    VocabularySet(
        "ro_daily_life_a1",
        "A1",
        "O zi obișnuită",
        "a1-unit-3",
        [
            VocabularyEntry(
                "a avea", "verb", "A deține ceva sau a dispune de ceva.", "Am un telefon."
            ),
            VocabularyEntry(
                "a lucra", "verb", "A face o activitate profesională.", "Lucrez la birou."
            ),
            VocabularyEntry(
                "a învăța", "verb", "A dobândi cunoștințe sau deprinderi.", "Învăț română."
            ),
            VocabularyEntry("a citi", "verb", "A înțelege cuvinte scrise.", "Citesc o carte."),
            VocabularyEntry(
                "a scrie",
                "verb",
                "A forma litere și cuvinte pe hârtie sau pe ecran.",
                "Scriu un mesaj.",
            ),
            VocabularyEntry(
                "a vorbi", "verb", "A comunica prin cuvinte rostite.", "Vorbim română la curs."
            ),
            VocabularyEntry("a asculta", "verb", "A fi atent la ceea ce auzim.", "Ascult muzică."),
            VocabularyEntry("a merge", "verb", "A se deplasa spre un loc.", "Merg la școală."),
            VocabularyEntry(
                "a veni",
                "verb",
                "A se deplasa spre locul despre care se vorbește.",
                "Ana vine la curs.",
            ),
            VocabularyEntry("a mânca", "verb", "A consuma alimente.", "Mănânc pâine."),
            VocabularyEntry("a bea", "verb", "A consuma un lichid.", "Beau apă."),
            VocabularyEntry("a dormi", "verb", "A se odihni în starea de somn.", "Dorm opt ore."),
            VocabularyEntry("a face", "verb", "A realiza o activitate.", "Ce faci acum?"),
            VocabularyEntry(
                "a locui", "verb", "A avea casa într-un anumit loc.", "Locuiesc în București."
            ),
            VocabularyEntry(
                "serviciu", "noun", "Loc de muncă sau activitate profesională.", "Merg la serviciu."
            ),
            VocabularyEntry(
                "birou", "noun", "Încăpere în care se lucrează.", "Lucrez într-un birou."
            ),
            VocabularyEntry(
                "școală", "noun", "Instituție în care învață copiii.", "Copiii merg la școală."
            ),
            VocabularyEntry(
                "curs",
                "noun",
                "Activitate organizată pentru învățarea unei materii.",
                "Am un curs de română.",
            ),
            VocabularyEntry(
                "carte", "noun", "Obiect cu pagini și text pentru citit.", "Citesc o carte seara."
            ),
            VocabularyEntry(
                "caiet", "noun", "Pagini legate, folosite pentru scris.", "Scriu în caiet."
            ),
            VocabularyEntry("pix", "noun", "Instrument de scris cu pastă.", "Am un pix albastru."),
            VocabularyEntry(
                "telefon", "noun", "Aparat pentru apeluri și mesaje.", "Telefonul este pe masă."
            ),
            VocabularyEntry(
                "calculator",
                "noun",
                "Aparat electronic folosit pentru lucru și informații.",
                "Lucrez la calculator.",
            ),
            VocabularyEntry(
                "mesaj", "noun", "Informație scurtă trimisă unei persoane.", "Scriu un mesaj."
            ),
            VocabularyEntry(
                "pauză", "noun", "Timp scurt în care oprim o activitate.", "Avem o pauză."
            ),
            VocabularyEntry("acum", "adverb", "În momentul acesta.", "Acum citesc."),
            VocabularyEntry("zilnic", "adverb", "În fiecare zi.", "Lucrez zilnic."),
            VocabularyEntry(
                "împreună", "adverb", "Unul cu altul, în aceeași activitate.", "Învățăm împreună."
            ),
        ],
    ),
    VocabularySet(
        "ro_food_shopping_a1",
        "A1",
        "Alimente și cumpărături",
        "a1-unit-4",
        [
            VocabularyEntry(
                "apă", "noun", "Lichid fără culoare, necesar vieții.", "Beau apă rece."
            ),
            VocabularyEntry("pâine", "noun", "Aliment copt din făină și apă.", "Cumpăr o pâine."),
            VocabularyEntry(
                "lapte", "noun", "Lichid alb folosit ca aliment.", "Beau lapte dimineața."
            ),
            VocabularyEntry(
                "brânză", "noun", "Aliment obținut din lapte.", "Mănânc pâine cu brânză."
            ),
            VocabularyEntry(
                "ou", "noun", "Aliment cu coajă, albuș și gălbenuș.", "Cumpăr șase ouă."
            ),
            VocabularyEntry(
                "carne", "noun", "Aliment provenit din corpul animalelor.", "Nu mănânc carne."
            ),
            VocabularyEntry(
                "pește",
                "noun",
                "Animal care trăiește în apă, folosit și ca aliment.",
                "La prânz mănânc pește.",
            ),
            VocabularyEntry(
                "măr", "noun", "Fruct rotund, adesea roșu sau verde.", "Vreau două mere."
            ),
            VocabularyEntry(
                "pară", "noun", "Fruct mai îngust lângă codiță.", "Această pară este dulce."
            ),
            VocabularyEntry(
                "roșie",
                "noun",
                "Legumă zemoasă, adesea roșie, pentru salată.",
                "Cumpăr trei roșii.",
            ),
            VocabularyEntry(
                "cartof",
                "noun",
                "Parte comestibilă a unei plante, crescută în pământ.",
                "Cumpăr cartofi pentru cină.",
            ),
            VocabularyEntry(
                "supă", "noun", "Mâncare lichidă cu legume sau carne.", "Supa este caldă."
            ),
            VocabularyEntry(
                "ciorbă",
                "noun",
                "Mâncare lichidă, de obicei acrișoară.",
                "Vreau o ciorbă de legume.",
            ),
            VocabularyEntry(
                "cafea",
                "noun",
                "Băutură preparată din boabe prăjite și măcinate.",
                "O cafea fără zahăr, vă rog.",
            ),
            VocabularyEntry(
                "ceai", "noun", "Băutură obținută din plante și apă fierbinte.", "Beau un ceai."
            ),
            VocabularyEntry(
                "zahăr",
                "noun",
                "Aliment dulce folosit în băuturi și deserturi.",
                "Nu vreau zahăr în cafea.",
            ),
            VocabularyEntry(
                "sare", "noun", "Ingredient alb care dă gust sărat.", "Supa are multă sare."
            ),
            VocabularyEntry(
                "magazin", "noun", "Loc de unde cumpărăm produse.", "Magazinul este deschis."
            ),
            VocabularyEntry(
                "piață", "noun", "Loc cu tarabe de unde cumpărăm produse.", "Cumpăr mere din piață."
            ),
            VocabularyEntry(
                "preț", "noun", "Suma cerută pentru un produs.", "Prețul este zece lei."
            ),
            VocabularyEntry(
                "leu", "noun", "Unitatea monetară a României.", "Un leu are o sută de bani."
            ),
            VocabularyEntry(
                "ban",
                "noun",
                "A suta parte dintr-un leu.",
                "Prețul este doi lei și cincizeci de bani.",
            ),
            VocabularyEntry(
                "a cumpăra",
                "verb",
                "A primi un produs în schimbul banilor.",
                "Cumpăr pâine de aici.",
            ),
            VocabularyEntry("a costa", "verb", "A avea un anumit preț.", "Cât costă cafeaua?"),
            VocabularyEntry(
                "proaspăt", "adjective", "Făcut sau cules de curând.", "Pâinea este proaspătă."
            ),
            VocabularyEntry(
                "cald", "adjective", "Cu o temperatură plăcut ridicată.", "Ceaiul este cald."
            ),
            VocabularyEntry("rece", "adjective", "Cu o temperatură joasă.", "Apa este rece."),
            VocabularyEntry(
                "dulce", "adjective", "Cu gust asemănător zahărului.", "Mărul este dulce."
            ),
        ],
    ),
    VocabularySet(
        "ro_city_transport_a1",
        "A1",
        "Locuri și transport",
        "a1-unit-5",
        [
            VocabularyEntry(
                "stradă",
                "noun",
                "Drum dintr-o localitate, printre clădiri.",
                "Această stradă merge spre centru.",
            ),
            VocabularyEntry(
                "adresă",
                "noun",
                "Date care arată unde se află un loc.",
                "Adresa este strada Lalelelor, numărul zece.",
            ),
            VocabularyEntry(
                "centru", "noun", "Partea din mijloc a unui oraș.", "Mergem în centru."
            ),
            VocabularyEntry(
                "gară", "noun", "Loc de plecare și sosire a trenurilor.", "Gara este aproape."
            ),
            VocabularyEntry(
                "stație", "noun", "Loc unde oprește un mijloc de transport.", "Aștept în stație."
            ),
            VocabularyEntry(
                "autobuz",
                "noun",
                "Vehicul mare pentru transportul călătorilor.",
                "Acest autobuz merge la gară.",
            ),
            VocabularyEntry(
                "tramvai", "noun", "Vehicul urban care circulă pe șine.", "Merg cu tramvaiul."
            ),
            VocabularyEntry(
                "metrou",
                "noun",
                "Tren urban care circulă mai ales sub pământ.",
                "Luăm metroul în București.",
            ),
            VocabularyEntry(
                "tren",
                "noun",
                "Vehicule legate care circulă pe calea ferată.",
                "Trenul pleacă din gară.",
            ),
            VocabularyEntry(
                "taxi",
                "noun",
                "Mașină cu șofer, plătită pentru o cursă.",
                "Merg cu taxiul la hotel.",
            ),
            VocabularyEntry(
                "mașină", "noun", "Vehicul mic pentru transport rutier.", "Mașina este în parcare."
            ),
            VocabularyEntry(
                "bicicletă",
                "noun",
                "Vehicul cu două roți, pus în mișcare cu pedalele.",
                "Merg cu bicicleta în parc.",
            ),
            VocabularyEntry(
                "bilet",
                "noun",
                "Dovadă de plată pentru călătorie sau intrare.",
                "Cumpăr un bilet de autobuz.",
            ),
            VocabularyEntry(
                "parc", "noun", "Spațiu verde pentru plimbare și odihnă.", "Copiii sunt în parc."
            ),
            VocabularyEntry(
                "muzeu",
                "noun",
                "Loc unde sunt expuse obiecte de interes cultural.",
                "Muzeul este lângă parc.",
            ),
            VocabularyEntry(
                "hotel",
                "noun",
                "Clădire cu camere pentru oaspeți care plătesc.",
                "Stăm la un hotel.",
            ),
            VocabularyEntry(
                "restaurant",
                "noun",
                "Loc unde comandăm și mâncăm preparate.",
                "Restaurantul este pe această stradă.",
            ),
            VocabularyEntry(
                "farmacie",
                "noun",
                "Loc de unde cumpărăm medicamente.",
                "Farmacia este lângă magazin.",
            ),
            VocabularyEntry(
                "spital",
                "noun",
                "Instituție unde sunt îngrijiți bolnavii.",
                "Autobuzul oprește la spital.",
            ),
            VocabularyEntry(
                "bancă",
                "noun",
                "Instituție care păstrează și gestionează bani.",
                "Banca este în centru.",
            ),
            VocabularyEntry(
                "poștă", "noun", "Loc de unde trimitem scrisori și colete.", "Merg la poștă."
            ),
            VocabularyEntry(
                "intrare", "noun", "Loc pe unde pătrundem într-o clădire.", "Intrarea este aici."
            ),
            VocabularyEntry(
                "ieșire", "noun", "Loc pe unde părăsim o clădire.", "Ieșirea este acolo."
            ),
            VocabularyEntry(
                "aproape", "adverb", "La distanță mică.", "Gara este aproape de hotel."
            ),
            VocabularyEntry("departe", "adverb", "La distanță mare.", "Spitalul este departe."),
            VocabularyEntry(
                "la stânga",
                "phrase",
                "În direcția opusă părții drepte.",
                "Farmacia este la stânga.",
            ),
            VocabularyEntry(
                "la dreapta",
                "phrase",
                "În direcția opusă părții stângi.",
                "Muzeul este la dreapta.",
            ),
            VocabularyEntry(
                "înainte", "adverb", "În direcția din față.", "Mergem înainte pe această stradă."
            ),
        ],
    ),
    VocabularySet(
        "ro_time_leisure_a1",
        "A1",
        "Calendar, oră și timp liber",
        "a1-unit-6",
        [
            VocabularyEntry(
                "zi", "noun", "Perioadă de douăzeci și patru de ore.", "Astăzi este o zi liberă."
            ),
            VocabularyEntry(
                "săptămână", "noun", "Perioadă de șapte zile.", "Am două cursuri pe săptămână."
            ),
            VocabularyEntry(
                "lună",
                "noun",
                "Una dintre cele douăsprezece părți ale anului.",
                "Iunie este o lună de vară.",
            ),
            VocabularyEntry(
                "an", "noun", "Perioadă de douăsprezece luni.", "Un an are douăsprezece luni."
            ),
            VocabularyEntry("luni", "noun", "Ziua de după duminică.", "Luni am curs."),
            VocabularyEntry(
                "marți", "noun", "Ziua dintre luni și miercuri.", "Marți merg la cinema."
            ),
            VocabularyEntry(
                "miercuri", "noun", "Ziua dintre marți și joi.", "Miercuri citesc acasă."
            ),
            VocabularyEntry("joi", "noun", "Ziua dintre miercuri și vineri.", "Joi joc fotbal."),
            VocabularyEntry(
                "vineri", "noun", "Ziua de dinainte de sâmbătă.", "Vineri seara sunt liber."
            ),
            VocabularyEntry(
                "sâmbătă", "noun", "Ziua dintre vineri și duminică.", "Sâmbătă merg în parc."
            ),
            VocabularyEntry(
                "duminică", "noun", "Ziua de după sâmbătă.", "Duminică sunt cu familia."
            ),
            VocabularyEntry(
                "dimineață", "noun", "Prima parte a zilei, după noapte.", "Dimineața beau ceai."
            ),
            VocabularyEntry(
                "după-amiază", "noun", "Partea zilei dintre prânz și seară.", "După-amiaza citesc."
            ),
            VocabularyEntry(
                "seară", "noun", "Partea zilei de dinaintea nopții.", "Seara ascult muzică."
            ),
            VocabularyEntry(
                "noapte", "noun", "Perioada întunecată dintre seară și dimineață.", "Noaptea dorm."
            ),
            VocabularyEntry("astăzi", "adverb", "În ziua în care vorbim.", "Astăzi este joi."),
            VocabularyEntry("mâine", "adverb", "În ziua de după astăzi.", "Mâine am curs."),
            VocabularyEntry(
                "oră", "noun", "Perioadă de șaizeci de minute.", "Cursul durează o oră."
            ),
            VocabularyEntry(
                "minut", "noun", "A șaizecea parte dintr-o oră.", "Mai avem cinci minute."
            ),
            VocabularyEntry("ceas", "noun", "Obiect care arată ora.", "Ceasul meu este pe masă."),
            VocabularyEntry(
                "timp liber",
                "phrase",
                "Perioadă fără muncă sau alte obligații.",
                "În timpul liber citesc.",
            ),
            VocabularyEntry(
                "muzică", "noun", "Sunete organizate într-o melodie.", "Ascult muzică seara."
            ),
            VocabularyEntry(
                "film",
                "noun",
                "Poveste prezentată prin imagini în mișcare.",
                "Filmul începe la opt.",
            ),
            VocabularyEntry(
                "cinema", "noun", "Loc unde vedem filme pe un ecran mare.", "Merg la cinema vineri."
            ),
            VocabularyEntry(
                "fotbal",
                "noun",
                "Sport cu două echipe care lovesc mingea cu piciorul.",
                "Joc fotbal sâmbăta.",
            ),
            VocabularyEntry(
                "plimbare",
                "noun",
                "Mers pe jos pentru relaxare.",
                "O plimbare în parc este plăcută.",
            ),
            VocabularyEntry(
                "întâlnire",
                "noun",
                "Moment stabilit pentru a vedea o persoană.",
                "Întâlnirea este la ora șase.",
            ),
            VocabularyEntry(
                "liber",
                "adjective",
                "Fără obligații într-un anumit moment.",
                "Sunt liber mâine seară.",
            ),
        ],
    ),
    VocabularySet(
        "ro_help_health_a1",
        "A1",
        "Ajutor și starea de sănătate",
        "a1-unit-7",
        [
            VocabularyEntry(
                "ajutor", "noun", "Sprijin oferit unei persoane.", "Am nevoie de ajutor."
            ),
            VocabularyEntry(
                "medic", "noun", "Persoană care tratează bolile.", "Vreau să vorbesc cu un medic."
            ),
            VocabularyEntry(
                "durere",
                "noun",
                "Senzație neplăcută într-o parte a corpului.",
                "Am o durere de cap.",
            ),
            VocabularyEntry(
                "cap",
                "noun",
                "Partea corpului unde sunt ochii și gura.",
                "Am o durere de cap puternică.",
            ),
            VocabularyEntry("ochi", "noun", "Organ cu care vedem.", "Ochii mei sunt obosiți."),
            VocabularyEntry("ureche", "noun", "Organ cu care auzim.", "Am o durere de ureche."),
            VocabularyEntry(
                "gură",
                "noun",
                "Parte a feței folosită pentru vorbit și mâncat.",
                "Medicul spune să deschid gura.",
            ),
            VocabularyEntry(
                "dinte",
                "noun",
                "Parte tare din gură, folosită pentru mestecat.",
                "Am un dinte care doare.",
            ),
            VocabularyEntry(
                "mână", "noun", "Parte a corpului cu care ținem obiecte.", "Scriu cu mâna dreaptă."
            ),
            VocabularyEntry(
                "picior", "noun", "Parte a corpului folosită la mers.", "Am o durere la picior."
            ),
            VocabularyEntry(
                "stomac", "noun", "Organ în care ajunge mâncarea.", "Am o durere de stomac."
            ),
            VocabularyEntry(
                "febră",
                "noun",
                "Temperatură a corpului mai mare decât cea normală.",
                "Am febră și sunt obosit.",
            ),
            VocabularyEntry(
                "răceală", "noun", "Boală ușoară cu nas înfundat și uneori tuse.", "Am o răceală."
            ),
            VocabularyEntry(
                "medicament",
                "noun",
                "Produs folosit pentru tratarea unei boli.",
                "Medicamentul este în geantă.",
            ),
            VocabularyEntry(
                "obosit", "adjective", "Care are nevoie de odihnă.", "Sunt obosit și vreau să dorm."
            ),
            VocabularyEntry(
                "bolnav", "adjective", "Care are o problemă de sănătate.", "Copilul este bolnav."
            ),
            VocabularyEntry(
                "bine", "adverb", "Într-o stare bună sau într-un mod bun.", "Sunt bine, mulțumesc."
            ),
            VocabularyEntry(
                "rău", "adverb", "Într-o stare neplăcută sau într-un mod neplăcut.", "Mă simt rău."
            ),
            VocabularyEntry("foame", "noun", "Nevoia de a mânca.", "Mi-e foame."),
            VocabularyEntry("sete", "noun", "Nevoia de a bea.", "Mi-e sete. Vreau apă."),
            VocabularyEntry(
                "frig", "noun", "Temperatură joasă sau senzația produsă de ea.", "Mi-e frig."
            ),
            VocabularyEntry(
                "a putea",
                "verb",
                "A avea capacitatea sau posibilitatea de a face ceva.",
                "Pot să merg singur.",
            ),
            VocabularyEntry(
                "a vrea", "verb", "A avea dorința de a face sau primi ceva.", "Vreau să stau acasă."
            ),
            VocabularyEntry(
                "a ajuta", "verb", "A oferi sprijin unei persoane.", "Puteți să mă ajutați?"
            ),
            VocabularyEntry(
                "a înțelege",
                "verb",
                "A pricepe sensul unei informații.",
                "Nu înțeleg acest cuvânt.",
            ),
            VocabularyEntry(
                "a repeta", "verb", "A spune sau a face încă o dată.", "Puteți să repetați?"
            ),
            VocabularyEntry(
                "încet",
                "adverb",
                "Cu viteză mică sau cu voce joasă.",
                "Vă rog să vorbiți mai încet.",
            ),
            VocabularyEntry(
                "urgent", "adjective", "Care nu poate aștepta mult.", "Am o problemă urgentă."
            ),
        ],
    ),
]
