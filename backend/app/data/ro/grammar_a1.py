"""Romanian A1 grammar, using contemporary standard Romanian orthography."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "ro-sounds-a1",
        "Litere și sunete: ă, â, î, ș, ț",
        "A1",
        "Scriere și pronunțare",
        "Citim și scriem sunetele specifice limbii române.",
        "Ă și a sunt vocale diferite: măr, mare. Â și î notează același sunet: român, "
        "în. În cuvintele obișnuite scriem î la început și la sfârșit, iar â în interior: "
        "înger, a coborî, pâine. Există excepții în cuvinte formate cu prefixe: neînțeles.\n\n"
        "Ș și ț au virgulă dedesubt. Ce și ci se citesc ca la începutul cuvintelor ceai "
        "și cinci; che și chi păstrează sunetul din casă: cheie, chitară. Ge și gi diferă "
        "de ghe și ghi: ger, girafă, gheață, ghid. Litera i de la sfârșitul unor "
        "cuvinte nu formează o silabă separată, ci modifică pronunțarea consoanei "
        "precedente: bani. În taxi, i formează o silabă.\n\n"
        "În eu, el, ea, ei, ele, ești și este, începutul se pronunță cu un sunet "
        "scurt ca la începutul lui iepure. Nu extindem această pronunțare la orice "
        "cuvânt cu e: elev începe direct cu vocala e.",
        structure="ă ≠ a; â = î ca sunet; ce / che; ge / ghe",
        rules=[
            "Păstrăm diacriticele: fată și fata sunt forme diferite.",
            "Scriem sunt, suntem, sunteți în româna standard actuală.",
            "Învățăm accentul odată cu fiecare cuvânt; el nu se marchează în scrierea obișnuită.",
        ],
        examples=[
            GrammarExample("Bună! Sunt din România.", note="Ă și â sunt sunete diferite."),
            GrammarExample(
                "Șase cărți și cinci chei.", note="Ș, ț, ci și che au sunete distincte."
            ),
        ],
        common_mistakes=[
            GrammarMistake("Sunt din Romînia.", "Sunt din România.", "În acest cuvânt scriem â.")
        ],
        related=["ro-pronouns-fi-a1"],
    ),
    GrammarTopic(
        "ro-pronouns-fi-a1",
        "Eu sunt, tu ești: pronume și a fi",
        "A1",
        "Verbe",
        "Prezentăm persoane și folosim formule de adresare.",
        "Pronumele personale sunt eu, tu, el, ea, noi, voi, ei, ele. Verbul a fi are "
        "formele sunt, ești, este, suntem, sunteți, sunt. Este și e sunt ambele corecte; "
        "e apare des în conversație.\n\nPronumele poate lipsi când persoana este clară: "
        "Sunt Ana. Pentru adresare politicoasă folosim dumneavoastră cu sunteți, chiar "
        "dacă vorbim cu o singură persoană. În saluturi și cereri putem folosi "
        "formele de adresare domnule și doamnă: Bună ziua, doamnă Popescu! "
        "Mulțumesc, domnule Ionescu! Separăm adresarea prin virgulă.",
        structure="eu sunt; tu ești; el/ea este; noi suntem; voi sunteți; ei/ele sunt",
        rules=[
            "Eu și tu se folosesc pentru o persoană; noi și voi pentru mai multe persoane.",
            "Dumneavoastră cere forma de persoana a doua plural a verbului.",
            "Nu este obligatoriu să repetăm pronumele înaintea fiecărui verb.",
        ],
        examples=[
            GrammarExample("Eu sunt Andrei. Ea este Ana."),
            GrammarExample("Dumneavoastră sunteți profesor?"),
        ],
        common_mistakes=[
            GrammarMistake("Noi sunt aici.", "Noi suntem aici.", "Cu noi folosim suntem.")
        ],
        related=["ro-negation-questions-a1"],
    ),
    GrammarTopic(
        "ro-gender-plural-a1",
        "Un, o, doi, două: genul și pluralul",
        "A1",
        "Substantive",
        "Recunoaștem substantive masculine, feminine și neutre.",
        "Învățăm substantivul împreună cu formele de singular și plural. Masculin: "
        "un frate, doi frați. Feminin: o soră, două surori. Neutrul se comportă ca "
        "masculinul la singular și ca femininul la plural: un scaun, două scaune.\n\n"
        "Pluralul nu are o singură terminație: casă – case, carte – cărți, "
        "oraș – orașe, telefon – telefoane. Un și o prezintă de obicei ceva nou; "
        "niște poate introduce un plural nespecificat: niște cărți. Cu un substantiv "
        "care numește o substanță, niște poate indica o cantitate neprecizată: niște apă.",
        structure="un / o + singular; doi / două + plural; niște cărți / niște apă",
        rules=[
            "Nu toate substantivele terminate în consoană sunt masculine.",
            "Un scaun este neutru: la plural spunem două scaune.",
            "La plural pot apărea schimbări în interiorul cuvântului: fată – fete.",
        ],
        examples=[
            GrammarExample("Un băiat și două fete."),
            GrammarExample("O casă, două case; un pat, două paturi."),
        ],
        common_mistakes=[
            GrammarMistake("Doi scaune.", "Două scaune.", "Scaun este neutru, nu masculin.")
        ],
        related=["ro-definite-article-a1", "ro-numbers-a1"],
    ),
    GrammarTopic(
        "ro-definite-article-a1",
        "Casa și băiatul: articolul hotărât",
        "A1",
        "Substantive",
        "Vorbim despre o persoană sau un obiect deja identificat.",
        "Articolul hotărât se atașează de obicei la sfârșitul substantivului: "
        "băiat – băiatul, casă – casa, carte – cartea. În aceste exemple, articolul se scrie "
        "împreună cu substantivul, nu ca un cuvânt separat înaintea lui.\n\n"
        "La plural întâlnim băieți – băieții, fete – fetele, "
        "scaune – scaunele. Forma articulată poate schimba finalul cuvântului: "
        "frate – fratele. Învățăm aceste forme împreună cu substantivul.",
        structure="un băiat → băiatul; o casă → casa; niște cărți → cărțile",
        rules=[
            "Forma nearticulată introduce adesea ceva nou: o carte.",
            "Forma articulată indică un obiect identificabil în context: cartea.",
            "Numărul de litere i contează: băieți și băieții au funcții diferite.",
        ],
        examples=[
            GrammarExample("Aici este o casă. Casa este mare."),
            GrammarExample("Aici sunt două scaune. Scaunele sunt mici."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Casă este aici.", "Casa este aici.", "Pentru casa cunoscută folosim casa."
            )
        ],
        related=["ro-gender-plural-a1"],
    ),
    GrammarTopic(
        "ro-present-a1",
        "Prezentul: am, lucrez, merg",
        "A1",
        "Verbe",
        "Spunem ce facem acum sau în mod obișnuit.",
        "La prezent verbul își schimbă forma după persoană. A avea: am, ai, are, avem, "
        "aveți, au. A lucra: lucrez, lucrezi, lucrează, lucrăm, lucrați, lucrează. "
        "A merge: merg, mergi, merge, mergem, mergeți, merg.\n\n"
        "Alte modele frecvente sunt a citi: citesc, citești, citește, citim, citiți, "
        "citesc; a mânca: mănânc, mănânci, mănâncă, mâncăm, mâncați, mănâncă. "
        "Nu toate verbele primesc -ez sau -esc.",
        structure="persoană + forma potrivită a verbului la prezent",
        rules=[
            "A avea exprimă și vârsta: Am douăzeci de ani.",
            "Prezentul poate descrie o acțiune obișnuită: Lucrez zilnic.",
            "Învățăm modelul fiecărui verb, nu adăugăm aceeași terminație tuturor verbelor.",
        ],
        examples=[
            GrammarExample("Lucrez acasă. Ana lucrează la birou."),
            GrammarExample("Avem o pauză. Citim o carte."),
        ],
        common_mistakes=[
            GrammarMistake("Eu are timp.", "Eu am timp.", "A avea se acordă cu persoana.")
        ],
        related=["ro-pronouns-fi-a1", "ro-negation-questions-a1"],
    ),
    GrammarTopic(
        "ro-negation-questions-a1",
        "Nu, cine, ce, unde: negația și întrebarea",
        "A1",
        "Propoziții",
        "Negăm o informație și cerem detalii simple.",
        "Nu stă înaintea verbului: Nu lucrez. Nu sunt acasă. O întrebare cu răspuns "
        "da sau nu poate păstra ordinea unei afirmații; vocea și semnul întrebării "
        "arată întrebarea: Ai timp?\n\nCine cere o persoană, ce cere un lucru sau o "
        "activitate, unde cere un loc, iar cum cere un mod sau o stare. Nu adăugăm "
        "un verb auxiliar special numai pentru a forma întrebarea.",
        structure="nu + verb; Cine / Ce / Unde / Cum + verb?",
        rules=[
            "Întrebăm Cine este? despre o persoană și Ce este? despre un lucru.",
            "Putem răspunde scurt: Da, am. / Nu, nu am.",
            "Scriem nu am sau n-am; ambele forme sunt corecte.",
        ],
        examples=[
            GrammarExample("Unde lucrezi? Lucrez la școală."),
            GrammarExample("Ai o mașină? Nu, nu am."),
        ],
        common_mistakes=[
            GrammarMistake("Eu am nu timp.", "Eu nu am timp.", "Nu se pune înaintea verbului.")
        ],
        related=["ro-present-a1"],
    ),
    GrammarTopic(
        "ro-numbers-a1",
        "Numere, cantități și prețuri",
        "A1",
        "Numerale",
        "Numărăm persoane și produse și înțelegem prețuri.",
        "Numărăm: zero, unu, doi, trei, patru, cinci, șase, șapte, opt, nouă, zece. "
        "Urmează unsprezece, doisprezece, treisprezece, paisprezece, cincisprezece, "
        "șaisprezece, șaptesprezece, optsprezece, nouăsprezece. Zecile sunt douăzeci, "
        "treizeci, patruzeci, cincizeci, șaizeci, șaptezeci, optzeci și nouăzeci; "
        "100 se citește o sută. Legăm zecile de unități prin și: douăzeci și trei.\n\n"
        "Folosim un măr, o pară, doi lei, două mere. De la trei la nouăsprezece "
        "nu punem de înaintea substantivului: trei mere, zece lei. Pentru numerele "
        "de la douăzeci la o sută folosim de: douăzeci de lei, treizeci și doi de lei, "
        "o sută de lei. Aici exersăm numerele până la o sută.\n\n"
        "Un leu are o sută de bani. În prețul scris 12,50 lei, virgula separă leii "
        "de bani: doisprezece lei și cincizeci de bani. Învățăm și douăsprezece mere, "
        "cu forma feminină pentru substantivul neutru la plural.",
        structure="doi lei / două mere; douăzeci de lei",
        rules=[
            "Unu devine un înaintea unui substantiv masculin sau neutru: un leu.",
            "Doi și doisprezece au forme feminine: două, douăsprezece.",
            "În scrierea românească a prețurilor folosim de obicei virgula zecimală.",
        ],
        examples=[
            GrammarExample("Cumpăr două mere și trei pere."),
            GrammarExample("Cafeaua costă doisprezece lei."),
        ],
        common_mistakes=[GrammarMistake("Două lei.", "Doi lei.", "Leu este masculin.")],
        related=["ro-gender-plural-a1"],
    ),
    GrammarTopic(
        "ro-adjective-agreement-a1",
        "Un măr roșu, două mere roșii",
        "A1",
        "Adjective",
        "Acordăm însușirea cu persoana sau obiectul descris.",
        "Adjectivul stă frecvent după substantiv și se acordă în gen și număr: "
        "un băiat frumos, o fată frumoasă, băieți frumoși, fete frumoase. "
        "La neutru avem un măr roșu și două mere roșii.\n\n"
        "Nu toate adjectivele au patru forme diferite: mare are pluralul mari "
        "pentru toate genurile. Folosim același acord și după a fi: Casa este "
        "mare. Casele sunt mari.",
        structure="substantiv + adjectiv acordat; substantiv + a fi + adjectiv acordat",
        rules=[
            "Genul și numărul substantivului determină forma adjectivului.",
            "La plural, substantivele neutre cer forma feminină a adjectivului.",
            "Învățăm forme precum bun, bună, buni, bune împreună.",
        ],
        examples=[
            GrammarExample("Pâinea este proaspătă. Merele sunt proaspete."),
            GrammarExample("Cumpăr o cafea mică și un ceai mare."),
        ],
        common_mistakes=[
            GrammarMistake("O cafea mic.", "O cafea mică.", "Cafea este feminin la singular.")
        ],
        related=["ro-gender-plural-a1", "ro-definite-article-a1"],
    ),
    GrammarTopic(
        "ro-place-prepositions-a1",
        "În, la, din, de la: locul și direcția",
        "A1",
        "Prepoziții",
        "Spunem unde suntem, unde mergem și de unde venim.",
        "În indică adesea interiorul: în casă, în autobuz. La indică un punct sau "
        "o destinație: la gară, la școală. Din poate indica originea sau ieșirea "
        "dintr-un loc: Sunt din România. Ies din magazin. De la indică punctul "
        "de plecare: Vin de la gară.\n\n"
        "Pe și sub localizează obiecte: pe masă, sub scaun. În expresiile simple "
        "fără alte determinări spunem în parc și pe masă, de obicei fără articol "
        "hotărât. Există construcții diferite, pe care le învățăm separat: cu "
        "autobuzul, acasă.",
        structure="unde? în / la; de unde? din / de la; unde merg? la / în",
        rules=[
            "Merg la gară și sunt la gară folosesc aceeași prepoziție.",
            "Acasă nu cere la: Sunt acasă.",
            "Mijlocul de transport apare frecvent cu articol: cu trenul.",
        ],
        examples=[
            GrammarExample("Merg cu autobuzul la gară."),
            GrammarExample("Cartea este pe masă, lângă telefon."),
        ],
        common_mistakes=[
            GrammarMistake("Sunt la acasă.", "Sunt acasă.", "Acasă se folosește fără la.")
        ],
        related=["ro-demonstratives-a1"],
    ),
    GrammarTopic(
        "ro-demonstratives-a1",
        "Acest autobuz și acea stradă",
        "A1",
        "Determinare",
        "Arătăm persoane sau lucruri apropiate și îndepărtate.",
        "Înaintea substantivului folosim acest băiat, această fată, acești băieți, "
        "aceste fete. Pentru depărtare: acel băiat, acea fată, acei băieți, acele "
        "fete. Substantivul nu primește atunci articol hotărât.\n\n"
        "Există și forme după substantiv: băiatul acesta, fata aceasta. Fără "
        "substantiv folosim acesta, aceasta, aceștia, acestea: Acesta este Radu. "
        "La acest nivel exersăm mai ales ordinea cu demonstrativul înainte. În conversație "
        "se aud și ăsta și asta; acestea sunt forme familiare.",
        structure="acest / această / acești / aceste + substantiv nearticulat",
        rules=[
            "La neutru: acest autobuz, aceste autobuze.",
            "Formele acest și acel nu se folosesc singure în locul substantivului.",
            "Aici și acolo indică locul; acest și acel determină un substantiv.",
        ],
        examples=[
            GrammarExample("Acest autobuz merge la gară."),
            GrammarExample("Acea stradă este lungă."),
        ],
        common_mistakes=[
            GrammarMistake("Acest strada.", "Această stradă.", "Stradă este feminin.")
        ],
        related=["ro-gender-plural-a1", "ro-place-prepositions-a1"],
    ),
    GrammarTopic(
        "ro-time-a1",
        "Când? Zilele, data și ora",
        "A1",
        "Timp",
        "Spunem când are loc o activitate.",
        "Pentru o întâlnire spunem luni, marți sau vineri, fără o prepoziție înaintea "
        "zilei. Pentru oră folosim la: luni la ora trei. Ora poate fi exprimată "
        "prin ceasul de 24 de ore sau prin formule uzuale: trei și jumătate, "
        "patru fără un sfert.\n\nDimineața, după-amiaza și seara sunt expresii "
        "obișnuite pentru părțile zilei. În fiecare luni și lunea descriu un "
        "obicei repetat. Spunem la ora unu, dar la ora două.\n\n"
        "Lunile sunt ianuarie, februarie, martie, aprilie, mai, iunie, iulie, august, "
        "septembrie, octombrie, noiembrie și decembrie. Pentru lună spunem în mai; "
        "pentru o dată, pe zece mai. Pentru prima zi a lunii folosim întâi: pe întâi mai. "
        "Lunile se scriu cu literă mică.\n\n"
        "Pentru ordine folosim primul și prima: primul curs, prima zi. Urmează "
        "al doilea curs, a doua zi, al treilea curs, a treia zi. Aceste forme arată "
        "poziția într-o serie, nu numărul total: două zile, dar a doua zi.",
        structure="luni la ora trei; pe zece mai; primul curs; în fiecare sâmbătă",
        rules=[
            "Când? întreabă despre timp; Cât este ceasul? întreabă ora.",
            "La trei și jumătate înseamnă 3:30.",
            "Zilele săptămânii se scriu cu literă mică în interiorul propoziției.",
        ],
        examples=[
            GrammarExample("Cursul începe marți la ora nouă."),
            GrammarExample("Sâmbăta citesc. Duminică merg la cinema."),
            GrammarExample("Primul curs este pe zece mai, la ora două."),
        ],
        common_mistakes=[
            GrammarMistake("Ne vedem la luni.", "Ne vedem luni.", "Ziua nu cere la în acest tipar.")
        ],
        related=["ro-numbers-a1", "ro-present-a1"],
    ),
    GrammarTopic(
        "ro-possessives-a1",
        "Familia mea și prietenii mei",
        "A1",
        "Posesie",
        "Spunem cui aparține un lucru familiar.",
        "După un substantiv articulat, posesivul se acordă cu lucrul posedat: "
        "fratele meu, sora mea, frații mei, surorile mele. Pentru tu avem tău, ta, "
        "tăi, tale; pentru noi: nostru, noastră, noștri, noastre; pentru voi: vostru, "
        "voastră, voștri, voastre.\n\nPentru alte persoane putem folosi lui, ei, lor: "
        "cartea lui, cartea ei, cărțile lor. Aceste trei forme nu se schimbă după "
        "lucrul posedat. Pentru adresare politicoasă: telefonul dumneavoastră.",
        structure="substantiv articulat + meu / mea / mei / mele",
        rules=[
            "Forma mea descrie genul lucrului posedat, nu genul vorbitorului.",
            "Un substantiv neutru cere meu la singular și mele la plural.",
            "În această structură spunem cartea mea, cu articol hotărât.",
        ],
        examples=[
            GrammarExample("Telefonul meu este aici. Cărțile mele sunt acasă."),
            GrammarExample("Acesta este prietenul nostru."),
        ],
        common_mistakes=[
            GrammarMistake("Sora meu.", "Sora mea.", "Sora cere posesivul feminin mea.")
        ],
        related=["ro-definite-article-a1", "ro-adjective-agreement-a1"],
    ),
    GrammarTopic(
        "ro-modal-sa-a1",
        "Vreau să…, pot să…, trebuie să…",
        "A1",
        "Verbe",
        "Exprimăm dorința, posibilitatea și necesitatea în situații simple.",
        "După vreau, pot și trebuie folosim frecvent să și un verb: Vreau să "
        "citesc. Pot să merg. Trebuie să plec. La persoanele eu, tu, noi și voi, "
        "multe forme de după să sunt identice cu prezentul: să merg, să mergi, "
        "să mergem, să mergeți.\n\nLa el, ea, ei și ele apar forme ca să meargă "
        "și să citească. Învățăm acum câteva expresii utile, iar formele neregulate "
        "se dezvoltă ulterior. A putea are formele pot, poți, poate, putem, puteți, pot. "
        "A vrea: vreau, vrei, vrea, vrem, vreți, vor.\n\n"
        "Pentru nevoi imediate învățăm expresii întregi: Am nevoie de apă. Mi-e foame. "
        "Mi-e sete. Mi-e frig. Mă simt rău. Mi-e înseamnă îmi este în aceste expresii. "
        "Pentru ajutor: Puteți să mă ajutați? Formele mi-, îmi și mă se explică "
        "în detaliu la nivelul următor.",
        structure="vreau / pot / trebuie + să + verb",
        rules=[
            "Trebuie să plec și trebuie să plecăm păstrează trebuie în acest tipar.",
            "Pot merge este și el corect; exersăm aici forma pot să merg.",
            "Nu pot să vin neagă posibilitatea de a veni.",
        ],
        examples=[
            GrammarExample("Vreau să vorbesc cu un medic."),
            GrammarExample("Puteți să repetați? Nu pot să citesc acest cuvânt."),
            GrammarExample("Mi-e sete. Vreau să beau apă.", note="Exprim o nevoie imediată."),
        ],
        common_mistakes=[
            GrammarMistake("Vreau să mergi eu.", "Vreau să merg eu.", "Eu cere forma merg.")
        ],
        related=["ro-present-a1", "ro-negation-questions-a1"],
    ),
    GrammarTopic(
        "ro-coordination-a1",
        "Și, dar, sau: legăm idei",
        "A1",
        "Propoziții",
        "Adăugăm o informație, exprimăm un contrast sau oferim o alegere.",
        "Și adaugă: Am apă și pâine. Dar arată o diferență importantă: Vreau să "
        "plec, dar nu pot. Sau prezintă alternative: Ceai sau cafea?\n\n"
        "Când subiectul este același, nu trebuie repetat: Citesc și scriu. "
        "Punem de obicei virgulă înainte de dar, nu între două cuvinte legate "
        "simplu prin «și» ori «sau».",
        structure="informație și informație; idee, dar contrast; opțiune sau opțiune",
        rules=[
            "În exemplele de bază folosim și pentru adăugare și dar pentru un contrast explicit.",
            "Sau nu înseamnă că alegem obligatoriu ambele lucruri.",
            "Verbul rămâne acordat cu subiectul fiecărei propoziții.",
        ],
        examples=[
            GrammarExample("Am un telefon, dar nu am internet."),
            GrammarExample("Vreți apă sau ceai?"),
        ],
        common_mistakes=[
            GrammarMistake("Eu citesc și tu scrie.", "Eu citesc și tu scrii.", "Tu cere scrii.")
        ],
        related=["ro-present-a1", "ro-modal-sa-a1"],
    ),
]
