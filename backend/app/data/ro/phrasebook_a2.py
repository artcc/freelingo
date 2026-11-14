"""Romanian A2 phrasebook: forty-two practical exchanges."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "ro-travel-stay-a2",
        "A2",
        "Călătorie și cazare",
        "🧳",
        [
            PhrasebookEntry(
                "Am făcut o rezervare pe numele Popescu.",
                "Identificarea rezervării la recepție.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Am rezervat o cameră pentru două nopți.",
                "Confirmarea duratei șederii.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "La ce oră a plecat trenul?",
                "Cererea unei informații despre o plecare trecută.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Nu am primit prosopul.",
                "Semnalarea unui obiect lipsă din cameră.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Am ajuns ieri și plecăm vineri.",
                "Precizarea datelor unei șederi.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Micul dejun este inclus în preț?",
                "Verificarea serviciilor oferite de cazare.",
                "neutral",
                "a2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-routine-memory-a2",
        "A2",
        "Rutine și experiențe personale",
        "🌅",
        [
            PhrasebookEntry(
                "M-am trezit mai devreme astăzi.",
                "Relatarea unei schimbări față de rutina obișnuită.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Ne-am întâlnit la gară.",
                "Precizarea locului unei întâlniri trecute.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "În copilărie locuiam la țară.",
                "Introducerea unei amintiri personale.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Mergeam des la bunici.",
                "Descrierea unui obicei din trecut.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Nu m-am odihnit bine azi-noapte.",
                "Explicarea unei stări de oboseală.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Te-ai pregătit pentru plecare?",
                "Verificare familiară înaintea unei călătorii.",
                "informal",
                "a2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-neighbours-a2",
        "A2",
        "Locuință și relații cu vecinii",
        "🔑",
        [
            PhrasebookEntry(
                "Robinetul din baie nu funcționează.",
                "Semnalarea unei probleme proprietarului.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Îi trimit proprietarului o fotografie.",
                "Explicarea modului de a arăta o defecțiune.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Aceasta este cheia apartamentului.",
                "Identificarea cheii la predare.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Îți împrumut eu o scară.",
                "Oferirea unui obiect unui vecin cunoscut.",
                "informal",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Îmi place cartierul, dar chiria este mare.",
                "Exprimarea unei preferințe și a unei dificultăți.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Cui îi dau cheia?",
                "Identificarea persoanei care primește obiectul.",
                "neutral",
                "a2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-counter-clinic-a2",
        "A2",
        "La ghișeu și la medic",
        "📋",
        [
            PhrasebookEntry(
                "Formularul l-am completat deja.",
                "Confirmarea pregătirii unui document.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Cererea am depus-o ieri.",
                "Precizarea momentului depunerii unui document.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Am o programare la ora zece.",
                "Anunțarea sosirii la cabinet.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Îl caut pe domnul doctor Popescu.",
                "Precizarea persoanei căutate la recepție.",
                "formal",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Rețeta am lăsat-o acasă.",
                "Explicarea lipsei unui document medical.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Am o alergie la acest medicament.",
                "Comunicarea unei informații relevante pentru consultație.",
                "neutral",
                "a2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-shopping-choices-a2",
        "A2",
        "Compararea produselor și plata",
        "🛍️",
        [
            PhrasebookEntry(
                "Aveți o mărime mai mare?",
                "Cererea altei mărimi după probarea unei haine.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Această geacă este mai ieftină decât cealaltă?",
                "Compararea prețurilor a două produse.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Nu am găsit nimic potrivit.",
                "Explicarea deciziei de a nu cumpăra.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "O jumătate de kilogram de brânză, vă rog.",
                "Cererea unei cantități la tejghea.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Pot să plătesc cu cardul?",
                "Verificarea unei modalități de plată.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Am păstrat bonul.",
                "Confirmarea existenței dovezii de cumpărare.",
                "neutral",
                "a2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-plans-invitations-a2",
        "A2",
        "Planuri, cereri și invitații",
        "📅",
        [
            PhrasebookEntry(
                "Aș dori să mă înscriu la curs.",
                "Cerere politicoasă de participare la un curs.",
                "formal",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Ați putea să mutați programarea pentru luni?",
                "Solicitarea politicoasă a unei alte zile.",
                "formal",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "O să ajung cu zece minute mai târziu.",
                "Anunțarea unei întârzieri previzibile.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Vrei să vii la petrecere sâmbătă?",
                "Invitație adresată unui prieten.",
                "informal",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Mulțumesc pentru invitație, dar o să fiu plecat.",
                "Refuz politicos exprimat de un bărbat, cu un motiv.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Aș prefera să ne întâlnim după serviciu.",
                "Propunerea unui moment mai convenabil.",
                "neutral",
                "a2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-instructions-a2",
        "A2",
        "Instrucțiuni și explicații",
        "🗺️",
        [
            PhrasebookEntry(
                "Urmați indicatoarele până la ieșire.",
                "Îndrumare politicoasă într-un spațiu public.",
                "formal",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Nu traversa pe roșu!", "Avertizare familiară la semafor.", "informal", "a2-unit-7"
            ),
            PhrasebookEntry(
                "Ia umbrela, pentru că o să plouă.",
                "Recomandare motivată înaintea unei ieșiri.",
                "informal",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Acesta este autobuzul care merge la muzeu.",
                "Identificarea mijlocului de transport potrivit.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Sunați-mă când ajungeți.", "Cererea unui apel după sosire.", "formal", "a2-unit-7"
            ),
            PhrasebookEntry(
                "Mai întâi cumpărăm biletele, apoi intrăm.",
                "Explicarea ordinii activităților.",
                "neutral",
                "a2-unit-7",
            ),
        ],
    ),
]
