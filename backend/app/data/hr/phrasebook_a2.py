"""Croatian A2 phrases for shopping, visits, travel and local services."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "hr-market-a2",
        "A2",
        "Na tržnici",
        "🥕",
        [
            PhrasebookEntry(
                "Molim pola kilograma ovog sira.",
                "Na štandu navodite proizvod i točnu količinu.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Ima li kruha bez soli?",
                "U pekarnici provjeravate postoji li proizvod bez određenog sastojka.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Koliko stoji kilogram ovih krušaka?",
                "Prije kupnje tražite cijenu voća koje pokazujete.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Trebam još šest jaja i bocu ulja.",
                "Dopunjujete narudžbu kod prodavača.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Jesu li ove rajčice zrele?",
                "Provjeravate je li povrće spremno za jelo.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Ne trebam vrećicu, hvala.",
                "Pri plaćanju pristojno odbijate dodatnu ambalažu.",
                "neutral",
                "a2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-visits-a2",
        "A2",
        "U gostima i sa susjedima",
        "🤝",
        [
            PhrasebookEntry(
                "Ivane, imaš li vremena za kavu?",
                "Poznatog prijatelja zovete na kratko druženje.",
                "informal",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Ovaj je poklon za vas.",
                "Predajete poklon domaćinu kojemu se obraćate uljudno.",
                "formal",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Hvala na pozivu i ugodnom društvu.",
                "Na kraju posjeta zahvaljujete domaćinima.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Dolazim s kolegicom s posla.",
                "Prije posjeta najavljujete tko dolazi s vama.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Gospodine, trebate li pomoć s torbom?",
                "Nudite pomoć nepoznatom muškarcu.",
                "formal",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Susjeda čuva moj ključ dok sam na poslu.",
                "Objašnjavate komu povjeravate ključ tijekom odsutnosti.",
                "neutral",
                "a2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-weekend-a2",
        "A2",
        "Razgovor o prošlom vikendu",
        "🎭",
        [
            PhrasebookEntry(
                "Kako je prošao izlet?",
                "Pitate poznanika o nedavnom kratkom putovanju.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Prošli vikend smo bili na koncertu.",
                "Započinjete kratko prepričavanje zajedničkog izlaska.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Predstava je trajala gotovo dva sata.",
                "Govorite koliko je dugo trajao kulturni događaj.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Jeste li već posjetili taj muzej?",
                "Pitate sugovornika kojemu govorite Vi o prošlom iskustvu.",
                "formal",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Nisam imao vremena za izložbu.",
                "Kao muški govornik objašnjavate zašto niste posjetili izložbu.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Bila sam umorna, ali zadovoljna.",
                "Kao govornica opisujete kako ste se osjećali nakon aktivnosti.",
                "neutral",
                "a2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-journeys-a2",
        "A2",
        "Na kolodvoru i u trajektnoj luci",
        "⛴️",
        [
            PhrasebookEntry(
                "S kojeg perona polazi autobus za Zadar?",
                "Na autobusnom kolodvoru tražite mjesto ukrcaja.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Vozi li ovaj trajekt do Supetra?",
                "Prije ukrcaja provjeravate odredište broda.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Trebam povratnu kartu za jednu osobu.",
                "Na blagajni kupujete putovanje u oba smjera.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Hoćemo li stići na sljedeći vlak?",
                "Zbog kašnjenja provjeravate vezu za nastavak putovanja.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Kartu ću kupiti putem interneta.",
                "Sugovorniku najavljujete kako ćete pripremiti put.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Od kolodvora do hotela ići ćemo pješice.",
                "Dogovarate posljednji dio puta nakon dolaska u grad.",
                "neutral",
                "a2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-care-a2",
        "A2",
        "Kod liječnika i u ljekarni",
        "🩺",
        [
            PhrasebookEntry(
                "Želim se naručiti na pregled.",
                "Telefonom tražite termin u liječničkoj ordinaciji.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Grlo me boli već tri dana.",
                "Liječniku opisujete tegobu i njezino trajanje.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Imam svoju zdravstvenu iskaznicu.",
                "Na prijamu potvrđujete da ste donijeli osobnu zdravstvenu ispravu.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Trebam li recept za ovaj lijek?",
                "U ljekarni provjeravate uvjete izdavanja konkretnog lijeka.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Molim vas, objasnite kako se uzima ovaj lijek.",
                "Od ljekarnika tražite jasnu uputu za propisani lijek.",
                "formal",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Danas se osjećam dobro.",
                "Pri ponovnom razgovoru s liječnikom opisujete svoje trenutačno stanje.",
                "neutral",
                "a2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-stay-a2",
        "A2",
        "Rezervacija i boravak u smještaju",
        "🏨",
        [
            PhrasebookEntry(
                "Htjela bih rezervirati dvokrevetnu sobu za dvije noći.",
                "Kao govornica ljubazno tražite određenu vrstu smještaja.",
                "formal",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Je li doručak uključen u cijenu?",
                "Prije potvrde rezervacije provjeravate što obuhvaća ponuda.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Imate li tišu sobu s pogledom na dvorište?",
                "Na recepciji tražite smještaj s manje buke.",
                "formal",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Koja je od ovih soba najpovoljnija?",
                "Uspoređujete cijene nekoliko ponuđenih soba.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Biste li mi donijeli još jednu deku?",
                "Ljubazno tražite dodatni pokrivač od osoblja.",
                "formal",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Do koliko sati moramo napustiti sobu?",
                "Provjeravate vrijeme odjave prije odlaska.",
                "neutral",
                "a2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-service-desk-a2",
        "A2",
        "Na šalteru i u servisu",
        "🛠️",
        [
            PhrasebookEntry(
                "Komu trebam predati ovaj obrazac?",
                "U uredu tražite osobu koja prima ispunjene dokumente.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Račun imam ovdje. Mogu vam ga pokazati.",
                "Pri reklamaciji nudite dokaz o kupnji.",
                "formal",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Ne mogu doći u petak jer radim.",
                "Objašnjavate zašto vam ponuđeni termin ne odgovara.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Možemo li dogovoriti novi termin?",
                "Nakon otkazivanja tražite drugi datum ili vrijeme usluge.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Smijem li paket ostaviti ovdje?",
                "Na šalteru provjeravate gdje je dopušteno odložiti pošiljku.",
                "formal",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Uređaj ne radi, zato tražim popravak.",
                "U servisu kratko povezujete problem sa svojim zahtjevom.",
                "neutral",
                "a2-unit-7",
            ),
        ],
    ),
]
