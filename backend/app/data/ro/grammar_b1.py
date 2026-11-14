"""Romanian B1 grammar for narration, reference and independent interaction."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "ro-narrative-past-b1",
        "Imperfectul și perfectul compus în povestire",
        "B1",
        "Timp și perspectivă",
        "Distingeți cadrul unei întâmplări de evenimentele prezentate ca încheiate.",
        "Imperfectul prezintă o situație în desfășurare, un obicei sau cadrul unei povești. "
        "Perfectul compus prezintă un eveniment ca întreg. Alegerea depinde de perspectiva "
        "vorbitorului, nu numai de durata acțiunii: Am locuit acolo zece ani prezintă "
        "o perioadă delimitată, deși aceasta este lungă.",
        rules=[
            "Folosiți imperfectul pentru fundal: Ploua și strada era goală.",
            "Folosiți perfectul compus pentru evenimente succesive: Am intrat și am sunat.",
            "Imperfectul singur nu afirmă că o acțiune a ajuns la rezultat.",
        ],
        examples=[
            GrammarExample("Când am ajuns, Ana pregătea cina.", note="Pregătirea era în curs."),
            GrammarExample("Ana a pregătit cina, apoi ne-a chemat la masă."),
            GrammarExample("În copilărie mergeam la bunici în fiecare vară."),
        ],
        related=["ro-pluperfect-b1", "ro-temporal-links-b1"],
    ),
    GrammarTopic(
        "ro-pluperfect-b1",
        "Mai-mult-ca-perfectul: înaintea unui moment trecut",
        "B1",
        "Timp și perspectivă",
        "Arătați că un eveniment era deja încheiat la un reper din trecut.",
        "Mai-mult-ca-perfectul situează o acțiune înaintea altui moment trecut: "
        "Când am ajuns, trenul plecase. Reperul poate apărea în aceeași frază sau în context. "
        "Formele se învață împreună cu verbul: făcusem, văzusem, mersesem, fusesem. "
        "Nu adăugați auxiliarul am la aceste forme.",
        structure="eu plecasem, tu plecaseși, el/ea plecase; noi plecaserăm, voi plecaserăți, ei/ele plecaseră",
        rules=[
            "Comparați am terminat cu terminasem: a doua formă cere un reper trecut.",
            "Deja poate accentua anterioritatea, dar nu este obligatoriu.",
        ],
        examples=[
            GrammarExample("Nu aveam biletul la mine, fiindcă îl lăsasem acasă."),
            GrammarExample("Când ne-au sunat, noi aflaserăm deja vestea."),
        ],
        common_mistakes=[
            GrammarMistake("Eu am plecasem.", "Eu plecasem.", "Forma nu are auxiliarul am."),
        ],
        related=["ro-narrative-past-b1"],
    ),
    GrammarTopic(
        "ro-temporal-links-b1",
        "Când, în timp ce, după ce și până când",
        "B1",
        "Legături temporale",
        "Faceți clară ordinea sau suprapunerea evenimentelor.",
        "În timp ce pune în legătură acțiuni simultane. După ce introduce evenimentul anterior, "
        "iar până când fixează limita unei situații. Când are un sens temporal mai larg, "
        "precizat de timpuri și de context. În română, o propoziție temporală despre viitor "
        "poate avea indicativul: Când vei ajunge, sună-mă.",
        rules=[
            "Nu confundați după ce cu înainte să: ordinea evenimentelor se schimbă.",
            "Folosiți imperfectul când descrieți două activități în desfășurare în trecut.",
        ],
        examples=[
            GrammarExample("În timp ce eu găteam, el punea masa."),
            GrammarExample("După ce am citit contractul, l-am semnat."),
            GrammarExample("Rămân aici până când se termină ședința."),
        ],
        related=["ro-narrative-past-b1", "ro-subjunctive-selection-b1"],
    ),
    GrammarTopic(
        "ro-subjunctive-selection-b1",
        "Conjunctivul după dorință, încercare și cerere",
        "B1",
        "Moduri verbale",
        "Exprimați o acțiune dorită sau cerută, cu același subiect ori cu alt subiect.",
        "Conjunctivul prezent folosește să: Vreau să plec; Vreau să pleci. Româna îl folosește "
        "frecvent și când subiectul nu se schimbă. La persoana a treia, multe verbe au forme "
        "diferite de indicativ: merge — să meargă, face — să facă, vine — să vină. "
        "Formele verbului a fi sunt să fiu, să fii, să fie, să fim, să fiți, să fie.",
        rules=[
            "Verbul de după să se acordă cu propriul subiect, nu automat cu primul verb.",
            "Cu a putea sunt posibile pot veni și pot să vin; nu orice verb acceptă ambele tipare.",
            "Pentru o cerere adresată cuiva folosiți, de exemplu, Îți cer să verifici.",
        ],
        examples=[
            GrammarExample("Încerc să găsesc o soluție."),
            GrammarExample("Vreau ca vecinii să participe la discuție."),
            GrammarExample("Te rog să fii atent la adresă."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Vreau să el merge.",
                "Vreau ca el să meargă.",
                "Subiectul explicit poate sta între ca și să; verbul este la conjunctiv.",
            ),
        ],
        related=["ro-purpose-b1", "ro-conditional-b1"],
    ),
    GrammarTopic(
        "ro-purpose-b1",
        "Scopul: ca să și pentru a",
        "B1",
        "Relații între acțiuni",
        "Explicați rezultatul urmărit printr-o acțiune.",
        "Ca să introduce scopul și se construiește cu conjunctivul. Pentru a urmat de infinitiv "
        "este frecvent în instrucțiuni și în scris, de obicei cu același autor al acțiunii. "
        "Când scopul privește alt subiect, o propoziție cu ca… să îl poate preciza explicit.",
        structure="acțiune + ca să + verb / pentru a + infinitiv",
        rules=[
            "Scopul este urmărit, dar formularea nu garantează realizarea lui.",
            "Cu subiect explicit: Vorbesc rar pentru ca toți să înțeleagă.",
        ],
        examples=[
            GrammarExample("Am plecat devreme ca să prind autobuzul."),
            GrammarExample("Apăsați aici pentru a salva documentul."),
            GrammarExample("Am repetat adresa pentru ca șoferul să o audă."),
        ],
        related=["ro-subjunctive-selection-b1", "ro-argument-links-b1"],
    ),
    GrammarTopic(
        "ro-conditional-b1",
        "Condiționalul prezent: ipoteze și politețe",
        "B1",
        "Moduri verbale",
        "Propuneți o alternativă și formulați o cerere fără ton imperativ.",
        "Condiționalul prezent se formează cu aș, ai, ar, am, ați, ar și infinitivul fără a. "
        "Într-o ipoteză, condiția și rezultatul pot avea ambele condiționalul: "
        "Dacă aș avea timp, aș veni. Aceasta diferă de condiția deschisă Dacă am timp, vin. "
        "Aș dori și ați putea sunt frecvente în cereri politicoase.",
        rules=[
            "Nu adăugați să între auxiliarul condiționalului și infinitiv.",
            "După aș vrea poate urma conjunctivul: Aș vrea să discutăm.",
            "Forma nu stabilește singură dacă ipoteza este imposibilă; contextul contează.",
        ],
        examples=[
            GrammarExample("Dacă am începe mai devreme, am termina înainte de prânz."),
            GrammarExample("Mi-ați putea trimite programul?"),
        ],
        common_mistakes=[
            GrammarMistake("Eu aș să merg.", "Eu aș merge.", "Auxiliarul cere infinitivul fără a."),
        ],
        related=["ro-subjunctive-selection-b1", "ro-obligation-b1"],
    ),
    GrammarTopic(
        "ro-accusative-clitics-b1",
        "Pe cine? Reluarea prin clitice de acuzativ",
        "B1",
        "Pronume neaccentuate",
        "Identificați persoana sau lucrul asupra căruia se îndreaptă acțiunea.",
        "Cliticele mă, te, îl, o, ne, vă, îi, le înlocuiesc ori reiau un complement direct. "
        "Cu nume proprii de persoane și cu pronume accentuate, pe marchează complementul: "
        "O cunosc pe Irina; Pe tine te caut. Un obiect neînsuflețit obișnuit nu primește "
        "automat pe: Citesc raportul; Îl citesc.",
        rules=[
            "La perfect compus: l-am văzut, i-am văzut, le-am văzut, dar am văzut-o.",
            "Alegeți cliticul după referent: fetele — le; băieții — îi.",
            "Pe nu se adaugă tuturor complementelor directe.",
        ],
        examples=[
            GrammarExample("Pe Andrei îl aștept la intrare."),
            GrammarExample("Ai văzut-o pe Elena?"),
            GrammarExample("Am primit documentele și le citesc acum."),
        ],
        related=["ro-dative-clitics-b1", "ro-clitic-combinations-b1"],
    ),
    GrammarTopic(
        "ro-dative-clitics-b1",
        "Cui? Destinatarul și pronumele în dativ",
        "B1",
        "Pronume neaccentuate",
        "Distingeți persoana ajutată de persoana căreia îi transmiteți ceva.",
        "Dativul indică frecvent destinatarul: îi scriu Mariei, le explic elevilor. "
        "Seria de bază este îmi, îți, îi, ne, vă, le; în vecinătatea altor forme apar "
        "mi-, ți-, i-, v- sau li. Verbul stabilește construcția: îl ajut pe coleg, "
        "dar îi răspund colegului.",
        rules=[
            "Un dativ singular îi nu arată genul: îi scriu lui Dan / îi scriu Anei.",
            "La perfect compus folosiți i-am răspuns, nu îl am răspuns.",
            "Reluarea este firească în Le-am dat colegilor adresa.",
        ],
        examples=[
            GrammarExample("Îți trimit adresa după ședință."),
            GrammarExample("I-am explicat vecinei unde este contorul."),
            GrammarExample("Le răspund mâine tuturor."),
        ],
        related=["ro-accusative-clitics-b1", "ro-nominal-dative-b1"],
    ),
    GrammarTopic(
        "ro-clitic-combinations-b1",
        "Două clitice: mi-l, ți-o, i le",
        "B1",
        "Pronume neaccentuate",
        "Exprimați împreună destinatarul și obiectul fără repetări inutile.",
        "Când un verb are un destinatar și un obiect, cliticul de dativ precedă cliticul "
        "de acuzativ: îmi dai caietul — mi-l dai; îți dau cartea — ți-o dau. "
        "Formele trebuie învățate ca grupuri: i-l, i-o, i le, ni-l, vi-l, li-l. "
        "La perfect compus, femininul singular o rămâne după participiu.",
        rules=[
            "Comparați Mi-l trimite cu Mi l-a trimis.",
            "Comparați Mi-o trimite cu Mi-a trimis-o.",
            "Cu conjunctivul: să mi-l dai, să mi-o dai.",
        ],
        examples=[
            GrammarExample("Ai formularul? Mi-l dai, te rog?"),
            GrammarExample("Le-am cerut cheia și mi-au dat-o."),
            GrammarExample("Documentele sunt pentru Ana; i le trimit azi."),
        ],
        common_mistakes=[
            GrammarMistake("Îmi îl dai?", "Mi-l dai?", "Cele două clitice formează grupul mi-l."),
        ],
        related=["ro-accusative-clitics-b1", "ro-dative-clitics-b1"],
    ),
    GrammarTopic(
        "ro-relative-clauses-b1",
        "Care și pe care: informații despre un referent",
        "B1",
        "Propoziții relative",
        "Identificați un obiect sau o persoană prin rolul său într-o acțiune.",
        "Care poate fi subiect: colega care lucrează aici. Când este complement direct, "
        "forma standard este pe care, însoțită de reluarea prin clitic: cartea pe care o citesc. "
        "Prepoziția cerută de verb rămâne înaintea relativului: persoana cu care vorbesc.",
        rules=[
            "Distingeți cine face acțiunea de cine sau ce o primește.",
            "În cartea pe care am citit-o, o reia cartea, nu persoana care citește.",
            "Nu puneți pe înainte de care când acesta este subiect.",
        ],
        examples=[
            GrammarExample("Acesta este vecinul care ne-a ajutat."),
            GrammarExample("Apartamentul pe care l-am vizitat are balcon."),
            GrammarExample("Colega cu care lucrez locuiește în Brașov."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Cartea care am citit-o",
                "Cartea pe care am citit-o",
                "În exprimarea standard, complementul direct cere pe care.",
            ),
        ],
        related=["ro-accusative-clitics-b1", "ro-genitive-article-b1"],
    ),
    GrammarTopic(
        "ro-genitive-article-b1",
        "Posesia: al, a, ai, ale",
        "B1",
        "Grupul nominal",
        "Exprimați apartenența și acordați articolul cu obiectul posedat.",
        "Genitivul poate urma direct un substantiv articulat: contractul proprietarului. "
        "Într-un contract al proprietarului apare articolul genitival al. Formele al, a, ai, ale "
        "se acordă cu lucrul posedat, nu cu posesorul: o cheie a vecinului, două chei ale vecinului.",
        rules=[
            "Masculin singular: al; feminin singular: a; masculin plural: ai; feminin plural: ale.",
            "La neutru: un dosar al comisiei, două dosare ale comisiei.",
            "Pentru nume masculine: lui Radu; pentru multe nume feminine: Anei.",
        ],
        examples=[
            GrammarExample("Am găsit o factură a asociației."),
            GrammarExample("Acestea sunt două documente ale proprietarului."),
        ],
        common_mistakes=[
            GrammarMistake(
                "o cheie al vecinului",
                "o cheie a vecinului",
                "A se acordă cu substantivul feminin cheie.",
            ),
        ],
        related=["ro-nominal-dative-b1", "ro-relative-clauses-b1"],
    ),
    GrammarTopic(
        "ro-nominal-dative-b1",
        "Dativul substantivelor: vecinei, colegului, locatarilor",
        "B1",
        "Grupul nominal",
        "Numiți explicit destinatarul unei cereri, al unui răspuns sau al unui obiect.",
        "Substantivele în genitiv și dativ au frecvent aceeași formă, dar funcții diferite. "
        "În Îi scriu proprietarului, forma indică destinatarul; în adresa proprietarului, "
        "ea indică apartenența. Forme utile sunt unui coleg, unei colege, unor colegi; "
        "colegului, colegei, colegilor.",
        rules=[
            "Învățați femininul împreună cu forma sa: vecină — unei vecine — vecinei.",
            "Reluați destinatarul când construcția o cere: Îi mulțumesc vecinei.",
            "Cu nume proprii: Îi scriu lui Mihai; Îi scriu Mariei.",
        ],
        examples=[
            GrammarExample("Le-am trimis locatarilor anunțul."),
            GrammarExample("I-am dat unei colege copia contractului."),
        ],
        related=["ro-dative-clitics-b1", "ro-genitive-article-b1"],
    ),
    GrammarTopic(
        "ro-passive-se-b1",
        "Construcții cu se în anunțuri și instrucțiuni",
        "B1",
        "Prezentarea acțiunii",
        "Descrieți ce se face fără să numiți persoana care face acțiunea.",
        "În Aici se vând bilete, biletele sunt lucrurile vândute, iar autorul vânzării "
        "nu este precizat. Verbul se acordă cu subiectul: se vinde un bilet, se vând bilete. "
        "Nu orice se are sens pasiv: în Ana se spală, Ana face acțiunea asupra propriei persoane.",
        rules=[
            "Acordați verbul cu substantivul: se completează formularul / se completează formularele.",
            "Alegeți un exemplu cu forme distincte pentru a observa acordul: se cere / se cer.",
        ],
        examples=[
            GrammarExample("Cererile se depun la ghișeul doi."),
            GrammarExample("Pentru înscriere se cer două fotografii."),
            GrammarExample("Taxa se plătește înainte de consultație."),
        ],
        related=["ro-impersonal-b1", "ro-obligation-b1"],
    ),
    GrammarTopic(
        "ro-impersonal-b1",
        "Se poate, se lucrează, este necesar",
        "B1",
        "Prezentarea acțiunii",
        "Prezentați o situație generală sau o evaluare fără un autor individual.",
        "Construcții precum se lucrează sau se circulă nu au un subiect care să fie obiectul "
        "acțiunii. Verbul rămâne la persoana a treia singular. Este important și este necesar "
        "pot introduce o acțiune exprimată prin conjunctiv. Persoana care trebuie să acționeze "
        "se înțelege din context sau se precizează.",
        rules=[
            "În Pe aici se circulă greu nu căutați un substantiv cu care să faceți acordul.",
            "După este important puteți preciza persoana: Este important să ajungi la timp.",
        ],
        examples=[
            GrammarExample("În această sală se lucrează în liniște."),
            GrammarExample("Se poate plăti cu cardul?"),
            GrammarExample("Este necesar să aduceți un act de identitate."),
        ],
        related=["ro-passive-se-b1", "ro-obligation-b1"],
    ),
    GrammarTopic(
        "ro-obligation-b1",
        "Trebuie, ar trebui și nu este nevoie",
        "B1",
        "Obligație și recomandare",
        "Distingeți cerințele obligatorii de sfaturi și de acțiunile facultative.",
        "Trebuie să exprimă o necesitate, iar ar trebui să este frecvent o recomandare. "
        "La prezent, trebuie rămâne neschimbat, în timp ce verbul de după să se acordă: "
        "eu trebuie să vin, ei trebuie să vină. Nu trebuie să poate fi ambiguu în context; "
        "pentru lipsa obligației, nu este nevoie să este mai clar.",
        rules=[
            "Pentru interdicție explicită folosiți nu aveți voie să.",
            "Pentru o recomandare: Ar trebui să vă odihniți.",
            "Nu transformați automat o recomandare într-o obligație când transmiteți un mesaj.",
        ],
        examples=[
            GrammarExample("Trebuie să prezentați biletul la intrare."),
            GrammarExample("Nu este nevoie să imprimați confirmarea; o puteți arăta pe telefon."),
            GrammarExample("Nu aveți voie să parcați în fața intrării."),
        ],
        related=["ro-conditional-b1", "ro-impersonal-b1"],
    ),
    GrammarTopic(
        "ro-reported-speech-b1",
        "Vorbirea indirectă: spune că, cere să",
        "B1",
        "Transmiterea mesajelor",
        "Redați un mesaj fără să schimbați autorul, destinatarul sau momentul.",
        "O afirmație poate fi introdusă prin spune că, o cerere prin cere să. Pronumele și "
        "expresiile de timp se adaptează perspectivei celui care relatează. Româna nu cere "
        "o deplasare automată a tuturor timpurilor după un verb la trecut: "
        "Mi-a spus că lucrează aici poate descrie o situație încă valabilă.",
        rules=[
            "Clarificați la cine se referă eu, tu și aici în mesajul original.",
            "A doua zi poate înlocui mâine când relatarea are alt reper temporal.",
            "Păstrați diferența dintre afirmație și solicitare: spune că vine / cere să venim.",
        ],
        examples=[
            GrammarExample("Ana mi-a spus: «Lucrez acasă.» — Ana mi-a spus că lucrează acasă."),
            GrammarExample("Ieri Dan a spus: «Vin mâine.» — Ieri Dan a spus că vine astăzi."),
            GrammarExample("Recepționera ne-a cerut să așteptăm."),
        ],
        related=["ro-indirect-questions-b1", "ro-subjunctive-selection-b1"],
    ),
    GrammarTopic(
        "ro-indirect-questions-b1",
        "Întrebări indirecte: dacă, unde, când",
        "B1",
        "Transmiterea mesajelor",
        "Cereți informații și redați întrebările altcuiva.",
        "O întrebare cu răspuns da sau nu devine o propoziție introdusă prin dacă: "
        "Nu știu dacă este deschis. Întrebările cu unde, când, de ce sau cum păstrează "
        "cuvântul interogativ. Dacă are aici sens interogativ, nu introduce o condiție.",
        rules=[
            "Puteți atenua întrebarea: Îmi puteți spune când pleacă trenul?",
            "Punctuația depinde de enunțul întreg: Nu știu când pleacă trenul.",
            "Nu adăugați că înaintea lui dacă într-o întrebare indirectă obișnuită.",
        ],
        examples=[
            GrammarExample("M-a întrebat dacă am primit factura."),
            GrammarExample("Aș vrea să știu unde se depun actele."),
            GrammarExample("Nu am înțeles de ce s-a schimbat programul."),
        ],
        related=["ro-reported-speech-b1", "ro-conditional-b1"],
    ),
    GrammarTopic(
        "ro-concession-b1",
        "Deși, chiar dacă și totuși",
        "B1",
        "Legături logice",
        "Recunoașteți un obstacol și arătați că rezultatul nu corespunde așteptării.",
        "Deși introduce în mod obișnuit un fapt acceptat: Deși plouă, ieșim. "
        "Chiar dacă poate introduce o posibilitate: Chiar dacă va ploua, vom ieși. "
        "Totuși semnalează un rezultat contrar așteptării create anterior. "
        "Concesia nu neagă obstacolul, ci limitează efectul lui asupra concluziei.",
        rules=[
            "Nu transformați un fapt într-o simplă posibilitate când reformulați.",
            "După deși folosiți firesc indicativul: deși este scump.",
        ],
        examples=[
            GrammarExample("Deși sala este mică, încap toți participanții."),
            GrammarExample("Prețul a crescut. Totuși, serviciul rămâne accesibil."),
            GrammarExample("Chiar dacă nu găsim sponsori, vom organiza o întâlnire mai mică."),
        ],
        related=["ro-argument-links-b1", "ro-conditional-b1"],
    ),
    GrammarTopic(
        "ro-argument-links-b1",
        "Motive, consecințe și concluzii",
        "B1",
        "Legături logice",
        "Legați o opinie de motivele ei și păstrați direcția relației logice.",
        "Pentru că și fiindcă introduc un motiv. De aceea introduce o consecință sau "
        "o decizie bazată pe acel motiv. Deci marchează o concluzie. În primul rând și "
        "în plus organizează argumentele, dar nu dovedesc singure că ele sunt corecte.",
        rules=[
            "Nu inversați cauza și rezultatul: Am întârziat pentru că autobuzul s-a defectat.",
            "Folosiți de exemplu pentru o ilustrare, nu pentru a anunța automat concluzia.",
            "Un text scurt are nevoie de legături clare, nu de un conector la fiecare propoziție.",
        ],
        examples=[
            GrammarExample("Biblioteca este aproape; de aceea putem merge pe jos."),
            GrammarExample("Propun parcul fiindcă are umbră. În plus, intrarea este gratuită."),
            GrammarExample("Nu sunt suficiente scaune, deci trebuie să mai aducem câteva."),
        ],
        related=["ro-concession-b1", "ro-purpose-b1"],
    ),
]
