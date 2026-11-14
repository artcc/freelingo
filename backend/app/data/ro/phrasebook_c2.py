"""Romanian C2 phrases for nuanced mediation and spontaneous repair."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "ro-delimiting-claims-c2",
        "C2",
        "Delimitarea unei afirmații",
        "🔬",
        [
            PhrasebookEntry(
                "Confirmăm că declarația există, nu că toate afirmațiile din ea au fost verificate.",
                "Comunici public statutul unei declarații fără să îi girezi conținutul.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Rezerva se referă la cauză sau și la faptul că incidentul a avut loc?",
                "Clarifici domeniul incertitudinii într-un raport cu mai multe surse.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Nu contest că ai plecat; contest felul în care a fost descrisă plecarea.",
                "Separi un fapt acceptat de eticheta nedreaptă care i-a fost atribuită.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Dacă eliminăm cuvântul «posibil», concluzia devine mai fermă decât permite raportul.",
                "Semnalezi o modificare de sens apărută în redactarea unui rezumat.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Când spuneți «doar», limitați persoanele autorizate sau operațiunile permise?",
                "Verifici domeniul unei restricții înainte de a explica regula altora.",
                "formal",
                "c2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-negotiating-exceptions-c2",
        "C2",
        "Excepții și angajamente precise",
        "🤝",
        [
            PhrasebookEntry(
                "Derogarea privește termenul; celelalte obligații rămân neschimbate.",
                "Explici oral o excepție fără să lași impresia unei scutiri generale.",
                "formal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Îmi asum să cer aprobarea astăzi, nu pot însă anticipa decizia directoarei.",
                "Promiți un demers aflat sub controlul tău și delimitezi decizia altei persoane.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Această condiție se aplică tuturor solicitanților sau numai celor care cer prelungirea?",
                "Clarifici o regulă cu domeniu neprecizat înainte de a depune un dosar.",
                "formal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Dacă am fi rezervat atunci, acum am avea locuri; ce variantă realistă ne mai rămâne?",
                "Într-o călătorie, recunoști alternativa ratată și readuci discuția la soluția actuală.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Acceptăm această excepție punctuală, fără să o transformăm într-o regulă pentru viitor.",
                "Închei un compromis și precizezi limita lui temporală.",
                "formal",
                "c2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-unpacking-dense-text-c2",
        "C2",
        "Un text dens explicat limpede",
        "📄",
        [
            PhrasebookEntry(
                "Înainte să simplific fraza, trebuie să știm al cui este proiectul.",
                "Refuzi să alegi arbitrar referentul unui posesiv într-un rezumat.",
                "neutral",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Asociațiile au depus cererile; textul nu spune cine a propus suspendarea evaluării.",
                "Desfaci un lanț nominal fără să atribui aceluiași grup toate acțiunile.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Putem împărți enunțul în două, păstrând condiția lângă permisiunea pe care o limitează.",
                "Colaborezi la rescrierea unui regulament pentru cititori nespecialiști.",
                "neutral",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Prefer să repet numele decât să las neclar cine trebuie să răspundă.",
                "Justifici o repetiție utilă într-un mesaj cu responsabilități importante.",
                "neutral",
                "c2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-discussing-narrative-c2",
        "C2",
        "O poveste, mai multe perspective",
        "📚",
        [
            PhrasebookEntry(
                "Aici aud mai degrabă îndoiala personajului decât verdictul naratorului.",
                "La un club de lectură, propui o interpretare a stilului indirect liber.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Ce anume din fragment susține lectura aceasta, dincolo de impresia noastră?",
                "Ceri un argument textual fără să respingi preferința celuilalt cititor.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Dacă povestesc scena la perfect compus, păstrez ordinea, dar se schimbă ritmul.",
                "Explici alegerea registrului într-o repovestire orală.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Pentru ea era deja o trădare; noi, ca cititori, încă nu știm ce se întâmplase.",
                "Distingi evaluarea personajului de informația confirmată de povestire.",
                "neutral",
                "c2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-responding-to-irony-c2",
        "C2",
        "Umor fără escaladare",
        "🎭",
        [
            PhrasebookEntry(
                "Am prins ironia; aș vrea totuși să lămurim problema din spatele ei.",
                "Recunoști gluma critică și readuci conversația la aspectul rezolvabil.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Fie el și expert, tot merită să-i cerem argumentele.",
                "Respingi într-o discuție informală autoritatea ca înlocuitor al justificării.",
                "informal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Pot să fac haz de încurcătură, dar nu vreau să pară că îți minimalizez efortul.",
                "Îți calibrezi umorul după un incident care l-a afectat pe interlocutor.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Când spui «mare reușită», mă lauzi sau îmi amintești de cele trei încercări ratate?",
                "Între apropiați, verifici dacă o evaluare este literală ori ironică.",
                "informal",
                "c2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-tactful-repair-c2",
        "C2",
        "Subînțelesuri și reparații delicate",
        "💬",
        [
            PhrasebookEntry(
                "Ca să nu iau acordul tău drept mai mult decât este: accepți ora sau și schimbarea locului?",
                "Clarifici un răspuns scurt dat după două propuneri diferite.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Când spuneți că formularea nu este tocmai potrivită, ce ar trebui schimbat concret?",
                "Transformi o critică atenuată într-o solicitare de îndrumare aplicabilă.",
                "formal",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Intenția mea era alta, dar asta nu schimbă faptul că te-a rănit replica.",
                "Recunoști efectul unei glume fără să te limitezi la apărarea intenției.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Îți las timp să te gândești; nu voi interpreta tăcerea ca pe un acord.",
                "Eviți presiunea asupra unei persoane care ezită în fața unei propuneri.",
                "neutral",
                "c2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-faithful-public-summary-c2",
        "C2",
        "O sinteză fidelă pentru alt public",
        "📝",
        [
            PhrasebookEntry(
                "Citez evaluarea din comunicat, fără să mi-o însușesc.",
                "Delimitezi vocea sursei de propria poziție într-o prezentare publică.",
                "formal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Putem spune lucrurile mai simplu, dar recomandarea trebuie să rămână recomandare.",
                "Corectezi o rescriere care ar transforma sfatul într-o obligație.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "În sinteză voi păstra obiecția voastră, chiar dacă majoritatea susține proiectul.",
                "Asiguri reprezentarea unei poziții minoritare după o consultare.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Avem o bază comună de lucru, nu încă un acord asupra tuturor consecințelor.",
                "Închei o mediere fără să prezinți progresul parțial drept consens deplin.",
                "formal",
                "c2-unit-7",
            ),
        ],
    ),
]
