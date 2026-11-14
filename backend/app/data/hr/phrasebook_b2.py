"""Croatian B2 phrases for argument, negotiation and practical mediation."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "hr-public-debate-b2",
        "B2",
        "Sudjelovanje u javnoj raspravi",
        "🏘️",
        [
            PhrasebookEntry(
                "Razumijem zabrinutost zbog troškova, no odgoda bi mogla biti još skuplja.",
                "Priznajete prigovor i iznosite razlog za nastavak projekta.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Na kojim se podacima temelji procjena broja korisnika?",
                "Na javnom sastanku tražite provjerljivu osnovu iznesene procjene.",
                "formal",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Prednost je bolja povezanost, a nedostatak veći trošak održavanja.",
                "Uspoređujete korist i ograničenje prometnog prijedloga.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Unatoč tim poteškoćama, smatram da vrijedi pokušati s manjim opsegom.",
                "Predlažete ograničeno isprobavanje ideje nakon iznesenih prigovora.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Možemo li prije glasanja čuti i stanare koji se još nisu javili?",
                "Pomažete da u raspravi sudjeluju i manje glasni članovi skupine.",
                "neutral",
                "b2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-news-evidence-b2",
        "B2",
        "Provjera i prenošenje vijesti",
        "📰",
        [
            PhrasebookEntry(
                "To sam čula od kolege, ali još nemam službenu potvrdu.",
                "Prenosite informaciju i jasno označujete ograničenje svojeg znanja.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Je li to objavljena odluka ili zasad samo prijedlog?",
                "Provjeravate status vijesti prije nego što promijenite vlastite planove.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "U priopćenju piše da se promjena razmatra, ne da je već prihvaćena.",
                "Ispravljate previše sigurno prepričavanje službenog teksta.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Kad je rekla „sutra”, mislila je na utorak jer smo razgovarale u ponedjeljak.",
                "Pojašnjavate na koji se dan odnosila sugovorničina izjava.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Pričekajmo provjeru izvora prije nego što to pošaljemo u grupu.",
                "Predlažete prijateljima da ne šire neprovjerenu vijest.",
                "informal",
                "b2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-procedures-accountability-b2",
        "B2",
        "Razjašnjavanje službenog postupka",
        "📋",
        [
            PhrasebookEntry(
                "Molim vas za potvrdu da je dopuna zaprimljena i pridružena mojem zahtjevu.",
                "Nakon slanja dokumenta provjeravate je li evidentiran u odgovarajućem predmetu.",
                "formal",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "U obavijesti nije navedeno tko je nadležan za sljedeći korak.",
                "Tražite razjašnjenje odgovornosti u neosobno sastavljenoj uputi.",
                "formal",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Znači li zaprimanje zahtjeva da je postupak pokrenut "
                "ili samo da su dokumenti stigli?",
                "Razlikujete primitak dokumenata od pravnog ili organizacijskog učinka.",
                "formal",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Možete li mi ovu uputu objasniti kroz korake koje trebam poduzeti?",
                "Tražite pristupačno objašnjenje složenog službenog izraza.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Željela bih da se moja primjedba unese u zapisnik.",
                "Na sastanku tražite službeni zapis važnog neslaganja.",
                "formal",
                "b2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-negotiation-risk-b2",
        "B2",
        "Pregovaranje o uvjetima",
        "🤝",
        [
            PhrasebookEntry(
                "Prihvatili bismo ponudu pod uvjetom da u cijenu uključite dostavu.",
                "Izričete uvjet pod kojim biste pristali na poslovnu ponudu.",
                "formal",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Kad bismo smanjili broj sudionika, bi li sadašnji prostor bio dovoljan?",
                "Ispitujete zamišljenu promjenu prije donošenja konačne odluke.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Da smo ranije znali za dodatni trošak, drukčije bismo rasporedili sredstva.",
                "Objašnjavate propuštenu mogućnost u prošlom planiranju.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Je li potpuna dokumentacija jedini uvjet ili postoje još neka ograničenja?",
                "Provjeravate je li navedeni nužni uvjet ujedno dovoljan.",
                "formal",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Dogovorimo unaprijed tko snosi troškove ako dođe do otkazivanja.",
                "Prije potvrde događaja razjašnjavate posljedice nepovoljnog ishoda.",
                "neutral",
                "b2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-meaning-precision-b2",
        "B2",
        "Ispravljanje nesporazuma",
        "💬",
        [
            PhrasebookEntry(
                "Nisam rekla da nitko ne dolazi, nego da ne dolaze svi.",
                "Ispravljate zamjenu djelomične negacije potpunom.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Odnosi li se riječ „samo” na cijenu ili na cijelu ponudu?",
                "Provjeravate koji je dio ponude ograničen prethodnim iskazom.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Tebi sam poslao radnu verziju; konačna je otišla voditeljici.",
                "Naglašenom zamjenicom i izričitim nazivima razjašnjavate različite primatelje.",
                "informal",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "To što nemamo primjedbi ne znači nužno da možemo odmah početi.",
                "Odbacujete preširok zaključak izveden iz odsutnosti prigovora.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Da preciziram: problem je vrijeme isporuke, a ne kvaliteta proizvoda.",
                "Sužavate raniju primjedbu kako je sugovornik ne bi shvatio kao opću kritiku.",
                "neutral",
                "b2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-workplace-cooperation-b2",
        "B2",
        "Jasne i obzirne poslovne poruke",
        "📨",
        [
            PhrasebookEntry(
                "Biste li mogli označiti dijelove nacrta koje trebamo dodatno razraditi?",
                "Tražite konkretnu povratnu informaciju umjesto opće ocjene rada.",
                "formal",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Molim vas da do srijede potvrdite tko preuzima provjeru podataka.",
                "U poslovnoj poruci jasno navodite potreban odgovor i rok.",
                "formal",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Taj rok, nažalost, ne možemo prihvatiti; možemo ponuditi petak poslijepodne.",
                "Uljudno odbijate neizvediv zahtjev i nudite konkretan drugi termin.",
                "formal",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Kad kažete da će ona poslati privitak, mislite li na Ivu ili na Lanu?",
                "Razjašnjavate zamjenicu prije nego što dodijelite zadatak.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "U privitku je nacrt za komentiranje, "
                "pa vas molim da ga još ne prosljeđujete klijentima.",
                "Označujete radni status dokumenta i granicu njegove uporabe.",
                "formal",
                "b2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-mediation-solutions-b2",
        "B2",
        "Posredovanje u razgovoru",
        "🗣️",
        [
            PhrasebookEntry(
                "Čini mi se da se slažete oko cilja, ali ne i oko načina provedbe.",
                "Izdvajate zajedničku točku i stvarno područje neslaganja.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Drugim riječima, treba vam ranija potvrda, a ne ranija dostava?",
                "Provjeravate jeste li točno saželi tuđi praktični zahtjev.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Što ranije razjasnimo zaduženja, to ćemo lakše izbjeći preklapanja.",
                "Objašnjavate korist pravodobnog dogovora o podjeli rada.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Kad kažeš da ćeš ovdje dočekati mirovinu, " "šališ se ili stvarno želiš odustati?",
                "U razgovoru s prijateljem provjeravate značenje pretjerivanja o dugom čekanju.",
                "informal",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Predlažem da najprije zapišemo ono oko čega smo se složili, "
                "a zatim otvorena pitanja.",
                "Usmjeravate napet razgovor prema jasnom zajedničkom sažetku.",
                "neutral",
                "b2-unit-7",
            ),
        ],
    ),
]
