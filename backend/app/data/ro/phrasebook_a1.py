"""Romanian A1 phrasebook: forty-nine phrases for everyday first exchanges."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "ro-first-contact-a1",
        "A1",
        "Saluturi și prezentări",
        "👋",
        [
            PhrasebookEntry(
                "Bună ziua!", "Salut politicos în timpul zilei.", "formal", "a1-unit-1"
            ),
            PhrasebookEntry(
                "Bună! Eu sunt Ana.",
                "Prezentare într-o întâlnire între colegi.",
                "informal",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Sunt din România.", "Precizarea țării de origine.", "neutral", "a1-unit-1"
            ),
            PhrasebookEntry(
                "Încântat de cunoștință!",
                "Formulă spusă de un bărbat când cunoaște pe cineva.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Încântată de cunoștință!",
                "Formulă spusă de o femeie când cunoaște pe cineva.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Mulțumesc!", "Aprecierea unui ajutor sau a unei atenții.", "neutral", "a1-unit-1"
            ),
            PhrasebookEntry(
                "La revedere!", "Încheierea politicoasă a unei întâlniri.", "neutral", "a1-unit-1"
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-home-a1",
        "A1",
        "Familie și casă",
        "🏠",
        [
            PhrasebookEntry(
                "Aici sunt doi copii.",
                "Identificarea persoanelor dintr-o fotografie.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Mama este acasă.",
                "Precizarea locului unde se află un membru al familiei.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Tata este aici.",
                "Indicarea prezenței unui membru al familiei.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Bine ați venit!",
                "Primirea politicoasă a unui oaspete; formulă fixă.",
                "formal",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Baia este aici.", "Indicarea unei încăperi din locuință.", "neutral", "a1-unit-2"
            ),
            PhrasebookEntry(
                "Aici sunt două scaune.",
                "Arătarea unor locuri pentru oaspeți.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Suntem acasă.", "Confirmarea prezenței în locuință.", "neutral", "a1-unit-2"
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-daily-life-a1",
        "A1",
        "Activități și învățare",
        "💬",
        [
            PhrasebookEntry(
                "Ce faci?",
                "Întrebare familiară despre activitatea de acum.",
                "informal",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Unde lucrezi?",
                "Întrebare între persoane care se adresează cu tu.",
                "informal",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Lucrez de acasă.", "Precizarea locului obișnuit de muncă.", "neutral", "a1-unit-3"
            ),
            PhrasebookEntry(
                "Învăț limba română.", "Explicarea activității de învățare.", "neutral", "a1-unit-3"
            ),
            PhrasebookEntry(
                "Nu înțeleg cuvântul.",
                "Semnalarea unei dificultăți de vocabular.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Cum se scrie?",
                "Cererea formei scrise; întrebare uzuală învățată ca întreg.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Ce înseamnă «acasă»?", "Cererea sensului unui cuvânt.", "neutral", "a1-unit-3"
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-cafe-market-a1",
        "A1",
        "La cafenea și la piață",
        "☕",
        [
            PhrasebookEntry(
                "O cafea, vă rog.", "Comandă simplă la cafenea.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Fără zahăr, vă rog.",
                "Precizarea unei preferințe pentru băutură.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Două mere și trei pere, vă rog.",
                "Cererea unei cantități la piață.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Cât costă pâinea?", "Întrebare despre prețul unui produs.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Aveți apă rece?",
                "Verificarea disponibilității unei băuturi.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Nota, vă rog.",
                "Cererea notei de plată la sfârșitul mesei.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Pâinea este proaspătă?",
                "Întrebare despre un produs înainte de cumpărare.",
                "neutral",
                "a1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-directions-a1",
        "A1",
        "Orientare și transport",
        "🚌",
        [
            PhrasebookEntry(
                "Unde este gara?", "Cererea unui reper pentru călătorie.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry(
                "Acest autobuz merge în centru?",
                "Confirmarea destinației înainte de urcare.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Un bilet până la Brașov, vă rog.",
                "Cumpărarea unui bilet cu destinația precizată.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Farmacia este aproape?",
                "Verificarea distanței până la un loc.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Merg pe jos.", "Precizarea modului de deplasare.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry(
                "Intrarea este la dreapta.",
                "Indicarea accesului într-o clădire.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Acea stradă duce la muzeu?",
                "Confirmarea unui traseu prin arătarea străzii.",
                "neutral",
                "a1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-meeting-time-a1",
        "A1",
        "Ora și întâlnirile",
        "🕒",
        [
            PhrasebookEntry(
                "Cât este ceasul?", "Întrebare despre ora actuală.", "neutral", "a1-unit-6"
            ),
            PhrasebookEntry(
                "La ce oră începe filmul?",
                "Verificarea orei unei activități.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Sunt liber sâmbătă.",
                "Disponibilitate exprimată de un bărbat.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Sunt liberă duminică.",
                "Disponibilitate exprimată de o femeie.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Ne vedem la ora șase.",
                "Stabilirea unei întâlniri; formulă uzuală.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Acesta este numărul meu de telefon.",
                "Oferirea unui mijloc de contact.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Pe mâine!",
                "Despărțire când este prevăzută o întâlnire a doua zi.",
                "informal",
                "a1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-asking-help-a1",
        "A1",
        "Ajutor și nevoi imediate",
        "🩺",
        [
            PhrasebookEntry(
                "Am nevoie de ajutor.", "Anunțarea unei nevoi de sprijin.", "neutral", "a1-unit-7"
            ),
            PhrasebookEntry(
                "Vreau să vorbesc cu un medic.",
                "Cererea unui contact medical.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Am o durere de cap.",
                "Descrierea simplă a unei probleme de sănătate.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Puteți să repetați, vă rog?",
                "Cerere politicoasă când informația nu a fost înțeleasă.",
                "formal",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Vă rog să vorbiți mai încet.",
                "Cererea unui ritm mai ușor de urmărit.",
                "formal",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Pot să stau aici?",
                "Cererea permisiunii de a ocupa un loc.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Vreau să vin, dar nu pot astăzi.",
                "Refuz simplu care păstrează interesul pentru întâlnire.",
                "neutral",
                "a1-unit-7",
            ),
        ],
    ),
]
