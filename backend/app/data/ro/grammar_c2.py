"""Romanian C2 grammar for scope, interpretation and register."""

from app.data._types import GrammarExample, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "ro-layered-evidence-c2",
        "Surse suprapuse și domeniul rezervei",
        "C2",
        "Precizia afirmației",
        "Păstrează lanțul atribuirilor fără să transferi unei surse concluzia alteia.",
        "În «Redacția spune că, potrivit expertului, avaria ar fi fost provocată de "
        "îngheț», redacția transmite o atribuire, iar cauza rămâne neconfirmată. "
        "Mutarea lui «probabil» sau eliminarea condiționalului poate schimba ceea ce "
        "își asumă fiecare voce. Delimitează separat faptul observat, explicația propusă "
        "și autorul evaluării. «Nu s-a demonstrat că» nu echivalează cu demonstrarea contrariului.",
        rules=[
            "Păstrează rezerva lângă afirmația asupra căreia se aplică.",
            "Nu trata confirmarea existenței unei declarații drept confirmarea conținutului ei.",
        ],
        examples=[
            GrammarExample(
                "Primăria confirmă că a primit raportul; nu confirmă încă explicația din raport.",
                note="Confirmarea privește primirea documentului, nu cauza descrisă.",
            ),
            GrammarExample(
                "Potrivit medicului, simptomele ar putea avea legătură cu tratamentul.",
                note="Sursa este identificată, iar legătura rămâne posibilă, nu stabilită.",
            ),
        ],
        related=["ro-quotation-polyphony-c2", "ro-obligation-scope-c2"],
    ),
    GrammarTopic(
        "ro-metalinguistic-negation-c2",
        "Negarea descrierii, nu a evenimentului",
        "C2",
        "Precizia afirmației",
        "Identifică dacă se contestă faptul, intensitatea sau cuvântul ales pentru a-l descrie.",
        "În «Nu a plecat pe furiș; a anunțat că pleacă», vorbitorul nu neagă plecarea, "
        "ci caracterizarea ei. «Nu e bun, e excelent» poate respinge o evaluare prea slabă, "
        "nu calitatea obiectului. Interpretarea cere continuarea și accentul. Într-un "
        "rezumat, nu păstra numai segmentul negativ: ai putea inversa poziția vorbitorului.",
        rules=[
            "Verifică ce element este corectat de continuare.",
            "Păstrează faptele acceptate chiar dacă eticheta folosită inițial este respinsă.",
        ],
        examples=[
            GrammarExample(
                "Nu a abandonat proiectul; și-a încheiat partea prevăzută în contract.",
                note="Se contestă caracterizarea încetării implicării drept abandon.",
            ),
            GrammarExample(
                "Nu e util, e indispensabil pentru accesul în clădire.",
                note="Se respinge cuvântul util ca prea slab, nu utilitatea obiectului.",
            ),
        ],
        related=["ro-scalar-focus-c2", "ro-ironic-echo-c2"],
    ),
    GrammarTopic(
        "ro-scalar-focus-c2",
        "Domeniul lui doar, nici măcar și abia",
        "C2",
        "Precizia afirmației",
        "Controlează ce se exclude și ce așteptare este evocată prin focalizare.",
        "«Doar Ana poate aproba» restrânge persoanele autorizate; «Ana poate doar verifica» "
        "restrânge acțiunile. «Nici măcar» situează un caz sub așteptarea minimă evocată "
        "în context. «Abia» poate indica un moment considerat târziu sau o cantitate "
        "insuficientă, dar nu înlocuiește automat «numai». Într-un text normativ, "
        "clarifică domeniul printr-o a doua propoziție dacă accentul oral ar fi decisiv.",
        rules=[
            "Așază restricția lângă elementul vizat și verifică interpretarea întregului enunț.",
            "Nu transforma o așteptare sugerată într-o obligație explicită.",
        ],
        examples=[
            GrammarExample(
                "Doar Ana poate aproba plata; Vlad poate verifica documentele.",
                note="Restricția privește autoritatea de aprobare.",
            ),
            GrammarExample(
                "Răspunsul a venit abia vineri, deși îl așteptam marți.",
                note="«Abia» raportează momentul la așteptarea unei date mai timpurii.",
            ),
        ],
        related=["ro-metalinguistic-negation-c2", "ro-nested-exceptions-c2"],
    ),
    GrammarTopic(
        "ro-nested-exceptions-c2",
        "Excepții condiționate și reguli rămase în vigoare",
        "C2",
        "Negociere și angajament",
        "Desfă o regulă cu excepții fără să extinzi permisiunea la alte persoane sau situații.",
        "O excepție de la termen nu anulează automat cerințele documentare. Într-un "
        "enunț cu «cu excepția», «numai în măsura în care» și «cu condiția să», "
        "urmărește separat grupul eligibil, avantajul acordat și condiția acestuia. "
        "În conversație, prezintă întâi regula generală, apoi excepția și limitele ei.",
        rules=[
            "Asociază fiecare condiție cu permisiunea exactă pe care o limitează.",
            "Nu generaliza o derogare acordată unei categorii la întregul grup.",
        ],
        examples=[
            GrammarExample(
                "Cererile se depun vineri; cei plecați în delegație le pot depune luni, "
                "dacă anunță joi. Dovada plății rămâne obligatorie.",
                note="Excepția privește termenul, nu documentele și nici toți solicitanții.",
            ),
            GrammarExample(
                "Sala se închide la zece, cu excepția serilor aprobate în scris, când se poate sta până la unsprezece.",
                note="Prelungirea are un plafon și cere o aprobare distinctă.",
            ),
        ],
        related=["ro-obligation-scope-c2", "ro-scalar-focus-c2"],
    ),
    GrammarTopic(
        "ro-obligation-scope-c2",
        "Obligația de a încerca și promisiunea rezultatului",
        "C2",
        "Negociere și angajament",
        "Identifică exact acțiunea asupra căreia se aplică angajamentul.",
        "«Mă angajez să solicit aprobarea» privește solicitarea, nu obținerea aprobării. "
        "«Voi încerca să obțin» anunță un efort, pe când «garantez că obțin» asumă un "
        "rezultat mai puternic. O formulă politicoasă nu slăbește automat obligația, "
        "iar un verb la viitor nu este întotdeauna o promisiune contractuală. "
        "La consemnare, păstrează verbul modal, obiectul lui și persoana competentă să decidă.",
        rules=[
            "Nu atribui celui care intermediază puterea de decizie a altei persoane.",
            "Separă obligația de transmitere de obligația de a obține un răspuns favorabil.",
        ],
        examples=[
            GrammarExample(
                "Mă oblig să transmit cererea astăzi; aprobarea îi revine directoarei.",
                note="Angajamentul are un executant și un obiect precis delimitate.",
            ),
            GrammarExample(
                "Voi încerca să vă obțin o programare mai devreme, dar nu pot garanta un loc.",
                note="Vorbitorul promite demersul, nu disponibilitatea.",
            ),
        ],
        related=["ro-nested-exceptions-c2", "ro-register-recasting-c2"],
    ),
    GrammarTopic(
        "ro-counterfactual-alignment-c2",
        "Ipoteze contrafactuale cu efecte în alt moment",
        "C2",
        "Negociere și angajament",
        "Urmărește separat momentul condiției și momentul rezultatului imaginat.",
        "O condiție trecută poate avea un rezultat imaginat în prezent: «Dacă am fi "
        "rezervat atunci, acum am avea locuri». Condiționalul perfect din condiție "
        "și condiționalul prezent din rezultat nu constituie o inconsecvență. "
        "În schimb, «am fi avut» poate muta rezultatul în trecut. La reformulare, "
        "păstrează reperele și nu adăuga o cauzalitate exclusivă care nu este afirmată.",
        rules=[
            "Verifică timpul fiecărei situații, nu uniformiza mecanic formele verbale.",
            "Un scenariu alternativ nu demonstrează singur toate cauzele rezultatului real.",
        ],
        examples=[
            GrammarExample(
                "Dacă aș fi acceptat postul la Iași, acum aș locui mai aproape de părinți.",
                note="Decizia ipotetică aparține trecutului; locuirea imaginată, prezentului.",
            ),
            GrammarExample(
                "Dacă am fi verificat sala ieri, am fi observat atunci problema.",
                note="Atât condiția, cât și rezultatul imaginat sunt situate în trecut.",
            ),
        ],
        related=["ro-obligation-scope-c2", "ro-layered-evidence-c2"],
    ),
    GrammarTopic(
        "ro-reference-resolution-c2",
        "Posesive ambigue și referință verificată",
        "C2",
        "Claritate și condensare",
        "Rezolvă o referință numai când contextul permite identificarea sigură a persoanei.",
        "În «Irina i-a spus Marei că proiectul său a fost selectat», posesivul "
        "«său» nu identifică fără echivoc persoana căreia îi este atribuit proiectul. "
        "Nici proximitatea numelui, nici intuiția despre cine ar fi mai important nu sunt suficiente. "
        "Repetarea numelui poate fi preferabilă eleganței aparente a pronumelui. "
        "Într-o reformulare, confirmă mai întâi posesorul și păstrează sursa informației.",
        rules=[
            "Nu aplica românei o regulă absolută potrivit căreia «său» ar desemna mereu subiectul.",
            "În texte cu consecințe practice, repetă numele după clarificare.",
        ],
        examples=[
            GrammarExample(
                "Când spui «proiectul său», te referi la proiectul Irinei sau la cel al Marei?",
                note="Întrebarea nu alege arbitrar una dintre interpretări.",
            ),
            GrammarExample(
                "Irina i-a spus Marei că proiectul Marei a fost selectat.",
                note="Repetarea este justificată dacă legătura proiectului cu Mara a fost confirmată.",
            ),
        ],
        related=["ro-dense-nominals-c2", "ro-elliptical-recovery-c2"],
    ),
    GrammarTopic(
        "ro-dense-nominals-c2",
        "Lanțuri nominale și statutul unei proceduri",
        "C2",
        "Claritate și condensare",
        "Desfă un grup nominal dens fără să transformi o propunere în fapt împlinit.",
        "În «propunerea de suspendare a evaluării cererilor depuse de asociații», "
        "asociațiile depun cereri, nu neapărat propunerea. Existența propunerii nu "
        "dovedește suspendarea evaluării. Reconstruiește fiecare relație înainte de "
        "a împărți fraza: cine propune, ce activitate ar fi suspendată și ce cereri "
        "sunt vizate. Păstrează necunoscut ceea ce textul nu precizează.",
        rules=[
            "Nu atribui tuturor nominalizărilor același agent.",
            "Păstrează stadiul procedural: analiză, recomandare, aprobare sau executare.",
        ],
        examples=[
            GrammarExample(
                "Comisia analizează propunerea de suspendare a evaluării cererilor depuse de asociații.",
                note="Comisia analizează; asociațiile au depus cererile; autorul propunerii nu este numit.",
            ),
            GrammarExample(
                "A fost aprobată prelungirea perioadei de consultare, nu modificarea regulamentului.",
                note="Decizia privește timpul pentru observații, nu conținutul regulilor.",
            ),
        ],
        related=["ro-reference-resolution-c2", "ro-register-recasting-c2"],
    ),
    GrammarTopic(
        "ro-free-indirect-voice-c2",
        "Stilul indirect liber și evaluarea personajului",
        "C2",
        "Voce și perspectivă",
        "Recunoaște o perspectivă interioară fără să o confunzi cu un fapt garantat de narator.",
        "Stilul indirect liber poate păstra persoana a treia a narațiunii, dar prelua "
        "întrebări, exclamații și repere ale personajului. «Mâine» se poate raporta "
        "la prezentul trăit de personaj. Nu orice întrebare dintr-o povestire este "
        "automat gândul lui; lectura trebuie susținută de context. În repovestirea "
        "neutră, atribuie explicit judecata dacă altfel s-ar pierde perspectiva.",
        rules=[
            "Distinge ceea ce personajul crede de ceea ce narațiunea confirmă.",
            "Păstrează centrul temporal al gândului atunci când îl transformi în relatare.",
        ],
        examples=[
            GrammarExample(
                "Mara strânse scrisoarea. Chiar o credeau atât de ușor de convins? Aveau să vadă!",
                note="Întrebarea și replica sfidătoare se citesc ca reacția Marei.",
            ),
            GrammarExample(
                "Radu se uită la ușa închisă. Îl uitaseră iar. Cel puțin așa i se părea.",
                note="Ultima propoziție limitează acuzația la interpretarea lui Radu.",
            ),
        ],
        related=["ro-literary-time-register-c2", "ro-quotation-polyphony-c2"],
    ),
    GrammarTopic(
        "ro-literary-time-register-c2",
        "Alternanța timpurilor și distanța narativă",
        "C2",
        "Voce și perspectivă",
        "Recunoaște perfectul simplu și interpretează alternanța lui cu timpurile deja cunoscute.",
        "Perfectul simplu poate susține succesiunea evenimentelor într-o narațiune "
        "literară; în unele varietăți regionale, inclusiv în Oltenia, are și utilizare "
        "orală vie. Recunoaște formele de persoana a treia singular din exemple: "
        "«deschise» corespunde lui «a deschis», «citi» lui «a citit», «se așeză» lui "
        "«s-a așezat», iar «strânse» lui «a strâns». Nu este în sine o greșeală sau "
        "un semn de limbă exclusiv veche. "
        "Alternanța cu imperfectul, mai-mult-ca-perfectul și prezentul narativ "
        "modifică perspectiva și ritmul. Obiectivul este interpretarea și adaptarea "
        "registrului, nu înlocuirea sistematică a perfectului compus în conversație.",
        rules=[
            "Nu deduce registrul numai dintr-o formă izolată; verifică genul textului și contextul.",
            "La repovestire, păstrează succesiunea, durata și raporturile de anterioritate.",
        ],
        examples=[
            GrammarExample(
                "Deschise plicul, citi primele rânduri și se așeză. Afară ningea.",
                note="Evenimentele succesive se disting de fundalul durativ.",
            ),
            GrammarExample(
                "Ieri intru în librărie și pe cine văd? Pe fostul meu profesor!",
                note="Prezentul narativ apropie o întâmplare trecută și susține surpriza orală.",
            ),
        ],
        related=["ro-free-indirect-voice-c2", "ro-register-recasting-c2"],
    ),
    GrammarTopic(
        "ro-marked-concession-c2",
        "Concesii emfatice și alegerea registrului",
        "C2",
        "Atitudine și umor",
        "Interpretează concesia în formulări marcate fără să o confunzi cu acceptarea condiției.",
        "«Fie și numai pentru o zi» admite un caz minimal relevant; «Oricât ar insista» "
        "menține concluzia indiferent de intensitatea insistenței. Construcții precum "
        "«Fie el și director, regula rămâne aceeași» sunt emfatice și pot suna "
        "polemice. Într-o negociere sensibilă, o formulare neutră cu «chiar dacă» "
        "poate păstra sensul fără aceeași provocare.",
        rules=[
            "Păstrează generalizarea sau limita scalară a concesiei la reformulare.",
            "Nu deduce că situația ipotetic admisă s-a produs deja.",
        ],
        examples=[
            GrammarExample(
                "Fie el și director, tot trebuie să respecte procedura.",
                note="Statutul înalt nu este acceptat ca motiv de exceptare.",
            ),
            GrammarExample(
                "Merită să deschidem biblioteca, fie și numai pentru o zi.",
                note="Chiar durata minimă este prezentată ca suficientă pentru utilitate.",
            ),
        ],
        related=["ro-nested-exceptions-c2", "ro-pragmatic-attenuation-c2"],
    ),
    GrammarTopic(
        "ro-ironic-echo-c2",
        "Ecoul ironic și intenția verificată",
        "C2",
        "Atitudine și umor",
        "Leagă o evaluare aparent pozitivă de promisiunea sau situația pe care o reia.",
        "După promisiunea unei proceduri simple, «Ce simplu a fost!» poate exprima "
        "ironie dacă procedura a durat ore întregi. Intenția rezultă din contrast, "
        "intonare și contextul comun; ghilimelele sau cuvântul «grozav» nu dovedesc "
        "singure ironia. Când relația este sensibilă, verifică ținta glumei înainte "
        "de a răspunde printr-un reproș.",
        rules=[
            "Separă sensul literal de atitudinea sugerată și de persoana vizată.",
            "Nu prezenta o interpretare ironică drept certă când lipsesc indiciile necesare.",
        ],
        examples=[
            GrammarExample(
                "«Doar două minute», ai spus. După o oră de coadă, chiar au fost două minute lungi!",
                note="Estimarea anterioară este reluată critic, prin contrast cu durata reală.",
            ),
            GrammarExample(
                "Când spui că ne-am descurcat grozav, te referi la rezultat sau la încurcătura de la început?",
                note="Replica verifică intenția fără să atribuie automat dispreț.",
            ),
        ],
        related=["ro-metalinguistic-negation-c2", "ro-pragmatic-attenuation-c2"],
    ),
    GrammarTopic(
        "ro-elliptical-recovery-c2",
        "Elipsă, întreruperi și reluarea firului",
        "C2",
        "Gestionarea conversației",
        "Recuperează conținutul omis numai dacă replica are un antecedent clar.",
        "«Eu nu» sau «Se poate, dar nu vineri» preiau conținut din discuția anterioară. "
        "După o întrerupere ori două propuneri concurente, cel mai apropiat enunț nu "
        "este neapărat antecedentul corect. Într-un acord scris, reintroduce verbul, "
        "participanții și obiectul acceptării după verificare. Nu transforma un "
        "răspuns scurt într-o aprobare generală a tuturor opțiunilor.",
        rules=[
            "Clarifică la care întrebare se răspunde înainte de a consemna decizia.",
            "Păstrează limitele temporale și modale ale replicii eliptice.",
        ],
        examples=[
            GrammarExample(
                "Ana poate veni luni, iar Vlad, marți.",
                note="Se recuperează «poate veni», nu o obligație de a veni.",
            ),
            GrammarExample(
                "«Mutăm masa sau scurtăm plimbarea?» — «De acord.» — "
                "«Cu mutarea mesei sau cu scurtarea plimbării?»",
                note="Acceptarea nu identifică singură opțiunea aleasă.",
            ),
        ],
        related=["ro-reference-resolution-c2", "ro-pragmatic-attenuation-c2"],
    ),
    GrammarTopic(
        "ro-pragmatic-attenuation-c2",
        "Atenuare, litotă și consecințe practice",
        "C2",
        "Gestionarea conversației",
        "Interpretează o evaluare discretă și transform-o într-o clarificare utilă.",
        "«Nu e tocmai fericită formularea» poate introduce o critică importantă, "
        "nu o obiecție minoră. «Nu e rău» poate exprima o laudă rezervată sau una "
        "puternică, în funcție de context. Atenuarea protejează relația, dar poate "
        "ascunde amploarea problemei. Cere detalii concrete în loc să echivalezi "
        "automat blândețea expresiei cu lipsa urgenței.",
        rules=[
            "Nu atribui unei litote un grad fix de apreciere în toate situațiile.",
            "Când repari o glumă, separă intenția proprie de efectul asupra interlocutorului.",
        ],
        examples=[
            GrammarExample(
                "Când spuneți că termenul nu este tocmai realist, de câte zile în plus aveți nevoie?",
                note="Răspunsul clarifică problema fără să respingă critica.",
            ),
            GrammarExample(
                "Am vrut să glumesc, dar înțeleg că a sunat ca un reproș. Îmi pare rău.",
                note="Explicarea intenției nu anulează recunoașterea efectului.",
            ),
        ],
        related=["ro-ironic-echo-c2", "ro-marked-concession-c2"],
    ),
    GrammarTopic(
        "ro-quotation-polyphony-c2",
        "Citat, distanțare și mai multe voci",
        "C2",
        "Sinteză și registru",
        "Atribuie exact o evaluare și deosebește citarea de adeziune.",
        "Un citat poate fi reprodus pentru documentare, critică sau acord. Ghilimelele "
        "nu stabilesc singure atitudinea autorului. Formule precum «în termenii "
        "vorbitorului», «după cum susține» și «fără a prelua această caracterizare» "
        "delimitează vocile. Într-o sinteză, păstrează diferența dintre poziția "
        "individuală, reacția altuia și concluzia efectiv acceptată de grup.",
        rules=[
            "Nu atribui autorului rezumatului fiecare evaluare pe care o citează.",
            "Când elimini ghilimelele, păstrează sursa și eventuala distanțare.",
        ],
        examples=[
            GrammarExample(
                "Directorul a numit măsura «inevitabilă»; reprezentanții locatarilor contestă această apreciere.",
                note="Două evaluări sunt atribuite unor participanți diferiți.",
            ),
            GrammarExample(
                "Redau expresia «succes deplin» din comunicat, fără să îmi însușesc evaluarea.",
                note="Citarea documentează o formulare, nu o aprobă.",
            ),
        ],
        related=["ro-layered-evidence-c2", "ro-free-indirect-voice-c2"],
    ),
    GrammarTopic(
        "ro-register-recasting-c2",
        "Schimbarea registrului fără schimbarea angajamentului",
        "C2",
        "Sinteză și registru",
        "Adaptează densitatea și tonul mesajului păstrând forța și limitele lui.",
        "Trecerea de la limbaj administrativ la conversație presupune adesea verbe "
        "mai directe, fraze mai scurte și altă adresare. Nu justifică transformarea "
        "unei recomandări în condiție obligatorie sau a unei obligații în sugestie. "
        "Termeni juridici ori tehnici se explică prin consecințele lor în context; "
        "nu se înlocuiesc cu aproximări care ar extinde regula.",
        rules=[
            "Inventariază agentul, acțiunea, termenul, condiția și modalitatea înainte de rescriere.",
            "Păstrează o rezervă relevantă chiar dacă eliminarea ei ar face fraza mai scurtă.",
        ],
        examples=[
            GrammarExample(
                "Transmiterea dovezii până vineri este obligatorie. — Vă rugăm să trimiteți dovada până vineri; este necesară.",
                note="Tonul devine accesibil, iar obligația și termenul rămân explicite.",
            ),
            GrammarExample(
                "Se recomandă programarea prealabilă. — Ar fi bine să vă programați înainte.",
                note="Recomandarea nu este transformată într-o condiție de acces.",
            ),
        ],
        related=["ro-dense-nominals-c2", "ro-obligation-scope-c2"],
    ),
]
