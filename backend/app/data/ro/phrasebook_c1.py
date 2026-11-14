"""Romanian C1 phrases for precise and considerate interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "ro-checking-information-c1",
        "C1",
        "Verificarea unei informații",
        "🔎",
        [
            PhrasebookEntry(
                "Pe ce vă bazați când spuneți că întârzierea se va prelungi?",
                "Ceri temeiul unei estimări fără să pui la îndoială buna-credință a persoanei.",
                "formal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Asta mi s-a spus; eu nu am verificat încă la fața locului.",
                "Transmiți familiei o veste despre starea casei și precizezi limita informației.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Nu exclud explicația, dar deocamdată nu avem suficiente indicii.",
                "Răspunzi unei ipoteze fără să o respingi și fără să o confirmi prematur.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Când spuneți că trebuie să fie așa, este o concluzie sau o cerință?",
                "Clarifici sensul modal al unei formulări ambigue într-o discuție tehnică.",
                "formal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Hai să separăm ce am văzut de ce am auzit de la alții.",
                "Într-o conversație între prieteni, relatările directe și zvonurile s-au amestecat.",
                "informal",
                "c1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-negotiating-limits-c1",
        "C1",
        "Condiții realiste pentru un acord",
        "🤝",
        [
            PhrasebookEntry(
                "Putem accepta data propusă, cu condiția să primim materialele până luni.",
                "Delimitezi angajamentul echipei înainte de confirmarea unui atelier.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Înțeleg urgența, dar nu pot promite o variantă finală până mâine.",
                "Refuzi un termen nerealist recunoscând nevoia interlocutorului.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Dacă vă ajunge o schiță în această etapă, o pot trimite joi.",
                "Oferi o alternativă realizabilă fără să o prezinți drept lucrare terminată.",
                "formal",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Prețul este acceptabil; asupra condițiilor de anulare aș vrea să revenim.",
                "Negociezi o rezervare și limitezi dezacordul la clauza încă deschisă.",
                "formal",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Ai fi putut să mă anunți; data viitoare, trimite-mi măcar un mesaj.",
                "Exprimi un reproș pentru așteptarea inutilă și formulezi o cerere pentru viitor.",
                "informal",
                "c1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-assigning-responsibility-c1",
        "C1",
        "Clarificarea responsabilității",
        "📋",
        [
            PhrasebookEntry(
                "Cine are împuternicirea de a semna și cine pregătește documentele?",
                "Separi autoritatea de semnare de sarcina administrativă.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Vă referiți la bunurile asociației sau la cele lăsate temporar în custodie?",
                "Verifici proprietatea înainte de a modifica un inventar.",
                "formal",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Ea este colega căreia i-am încredințat dosarul; o includ în discuție.",
                "Identifici persoana care cunoaște situația și facilitezi continuarea conversației.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Îți duc eu valiza, dar spune-mi unde trebuie lăsată.",
                "Oferi ajutor într-o călătorie și verifici limita sarcinii asumate.",
                "informal",
                "c1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-recounting-an-incident-c1",
        "C1",
        "Relatarea unui incident",
        "🧭",
        [
            PhrasebookEntry(
                "Ca să se înțeleagă de ce am reacționat așa, trebuie să mă întorc puțin în timp.",
                "Introduci o explicație anterioară fără să pierzi firul poveștii.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Abia după aceea am aflat că mesajul fusese trimis cu o seară înainte.",
                "Distingi momentul în care ai aflat informația de momentul evenimentului.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Cine citea mesajul în acel moment: tu sau colega ta?",
                "Verifici autorul acțiunii într-o relatare orală prea condensată.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Revin la momentul în care am ajuns la cabană: atunci a început ploaia.",
                "Închei o digresiune și restabilești reperul temporal al întâmplării.",
                "neutral",
                "c1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-weighing-arguments-c1",
        "C1",
        "Un dezacord bine delimitat",
        "⚖️",
        [
            PhrasebookEntry(
                "Obiecția mea privește modul de aplicare, nu obiectivul propunerii.",
                "Previi interpretarea unei critici punctuale drept respingere a întregului proiect.",
                "formal",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Faptul că nu avem confirmarea nu înseamnă că avem dovada contrariului.",
                "Corectezi un salt nejustificat de la incertitudine la negare.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Este greu de verificat în forma aceasta; putem vedea documentul original?",
                "Legi dificultatea de o acțiune concretă care ar putea-o reduce.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Nu toți au respins ideea; ar fi util să aflăm ce variante ar accepta.",
                "Redeschizi negocierea fără să pretinzi că există deja o majoritate favorabilă.",
                "neutral",
                "c1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-repairing-the-tone-c1",
        "C1",
        "Repararea tonului și a neînțelegerilor",
        "💬",
        [
            PhrasebookEntry(
                "Cred că m-am exprimat prea abrupt. Încerc să spun că avem nevoie de mai mult timp.",
                "Îți corectezi tonul fără să retragi cererea de fond.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Glumești pe seama situației sau e ceva ce ai vrea să-mi reproșezi?",
                "Între prieteni, verifici intenția unei replici care te-a pus pe gânduri.",
                "informal",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Mă refeream la schiță, nu la varianta pe care ai trimis-o clientului.",
                "Corectezi obiectul unei observații fără să acuzi interlocutorul că nu a ascultat.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Să nu-mi răcești pe drum; dă-mi un semn când ajungi.",
                "Îți exprimi grija față de o persoană apropiată într-un registru afectuos.",
                "informal",
                "c1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-recording-an-agreement-c1",
        "C1",
        "Încheierea unei discuții",
        "📝",
        [
            PhrasebookEntry(
                "Ca să nu consemnez greșit: aceasta este o propunere sau o decizie acceptată?",
                "Verifici statutul unei idei înainte de redactarea procesului-verbal.",
                "formal",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Ana i-a cerut lui Vlad să trimită datele; confirmăm că Vlad își asumă termenul?",
                "Separi cererea unei persoane de acceptarea efectivă a sarcinii de către alta.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Avem acordul asupra locului; data rămâne deschisă până răspund și ceilalți.",
                "Rezumă un acord parțial fără să îl extinzi la întreaga organizare.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Vă trimit sinteza și vă rog să semnalați orice rezervă pe care am omis-o.",
                "Închei o mediere lăsând participanților posibilitatea de a corecta rezumatul.",
                "formal",
                "c1-unit-7",
            ),
        ],
    ),
]
