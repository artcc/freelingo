"""Croatian C1 phrases for nuanced public and personal interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "hr_source_discussion_c1",
        "C1",
        "Provjera vijesti i tumačenje nalaza",
        "🔎",
        [
            PhrasebookEntry(
                "Imamo li neovisnu potvrdu ili se svi izvještaji pozivaju na isti izvor?",
                "Na uredničkom sastanku provjeravate jesu li različite objave doista različiti dokazi.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Prema dostupnim nalazima to je moguće, ali zasad ne bih tvrdila da je dokazano.",
                "Predstavljate stručnu procjenu i čuvate razliku između mogućnosti i potvrde.",
                "formal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "To što nije potvrđeno ne znači samo po sebi da je opovrgnuto.",
                "U raspravi ispravljate zaključak da je neprovjerena vijest nužno netočna.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Čula sam to iz druge ruke; provjerit ću prije nego što prenesem dalje.",
                "Prijateljima prenosite glasinu bez predstavljanja sebe kao neposredne svjedokinje.",
                "informal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Možemo li taj zaključak primijeniti i izvan razdoblja koje je istraživanje obuhvatilo?",
                "Na predstavljanju rezultata provjeravate granice njihova vremenskog dosega.",
                "formal",
                "c1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_conditional_agreement_c1",
        "C1",
        "Dogovor uz uvjete i rezerve",
        "🤝",
        [
            PhrasebookEntry(
                "Načelno smo spremni prihvatiti ponudu, uz prethodnu provjeru troškovnika.",
                "U pregovorima pokazujete spremnost, ali još ne dajete konačan pristanak.",
                "formal",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Čak i kad bismo povećali proračun, ostalo bi pitanje raspoloživih ljudi.",
                "Objašnjavate zašto zamišljeni novčani ustupak ne uklanja sve zapreke.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Ako preuzmete prijevoz, mi ćemo osigurati prostor; odgovara li vam takva podjela?",
                "Nudite konkretnu uzajamnu obvezu i tražite izričit odgovor druge strane.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "To je nužan uvjet, ali još moramo usuglasiti rokove.",
                "Sprečavate da ispunjenje jednog zahtjeva bude shvaćeno kao prihvaćanje cijele ponude.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Mogli bismo se naći na pola puta, samo da ne obećamo više nego što možemo izvesti.",
                "S bliskim suradnikom tražite kompromis bez neostvarivih obećanja.",
                "informal",
                "c1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_clear_minutes_c1",
        "C1",
        "Precizan zapisnik i podjela odgovornosti",
        "📋",
        [
            PhrasebookEntry(
                "Da ne ostane nejasno, tko preuzima provedbu, a tko samo daje suglasnost?",
                "Na sastanku razlikujete izvršitelja posla od osobe koja ga odobrava.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Molim da se u zapisniku razdvoje prihvaćeni zaključci od prijedloga za razmatranje.",
                "Prije potvrde službenog zapisnika sprečavate pripisivanje nepostojećih odluka.",
                "formal",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Odluka je donesena, ali to još nije potvrda da su radovi započeli.",
                "Tumačite obavijest koja govori o odobrenju, a ne o stvarnom početku radova.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Možemo li navesti nositelja zadatka i rok, umjesto da ostane samo 'riješit će se'?",
                "Zatražili ste da neodređena obveza dobije jasno odgovornu osobu.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Nisam preuzela nabavu opreme, nego prikupljanje ponuda za nju.",
                "Ispravljate zapis koji vam pripisuje širu obvezu nego što ste prihvatili.",
                "neutral",
                "c1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_shared_experiences_c1",
        "C1",
        "Pripovijedanje i razjašnjavanje iskustva",
        "⛵",
        [
            PhrasebookEntry(
                "Tek sam poslije shvatila da je njegova šutnja značila nelagodu, a ne nezainteresiranost.",
                "Prepričavate susret i odvajate tadašnji dojam od naknadnog razumijevanja.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Da se vratim korak unatrag: prije nego što smo stigli, vodič je već promijenio rutu.",
                "U priči naknadno objašnjavate raniju okolnost nužnu za razumijevanje događaja.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Kad kažeš da joj je vratio torbu, misliš na Martu ili na vodičicu?",
                "Slušate priču s više žena i provjeravate na koga se odnosi zamjenica.",
                "informal",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Zamisli prizor: mi na pogrešnom peronu, a vlak već kreće s drugoga.",
                "Prijateljima živopisno prepričavate putnu nezgodu.",
                "informal",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Iz ove perspektive zvuči smiješno, ali tada nam stvarno nije bilo do šale.",
                "U razgovoru povezujete današnji humor s ozbiljnošću tadašnjeg iskustva.",
                "informal",
                "c1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_public_arguments_c1",
        "C1",
        "Uvažavanje i osporavanje u javnoj raspravi",
        "🏛️",
        [
            PhrasebookEntry(
                "Svrhu mjere ne dovodim u pitanje; moj se prigovor odnosi na način provedbe.",
                "Na javnom savjetovanju precizno određujete što podržavate, a čemu se protivite.",
                "formal",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Premda je taj podatak važan, sam po sebi ne objašnjava uzrok promjene.",
                "U raspravi priznajete relevantnost nalaza, ali odbijate neopravdan uzročni zaključak.",
                "formal",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Nije toliko sporan cilj koliko su sporne posljedice "
                "za ljude koji ovdje žive cijele godine.",
                "Pomicanjem težišta vraćate raspravu na potrebe stalnih stanovnika.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Koju bismo okolnost morali promijeniti da bi vam prijedlog postao prihvatljiv?",
                "Umjesto ponavljanja argumenata tražite konkretan uvjet za prevladavanje prigovora.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Taj je primjer uvjerljiv, ali provjerimo vrijedi li isto i za manje sredine.",
                "U razgovoru ograničavate generalizaciju iz iskustva jednoga grada.",
                "neutral",
                "c1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_spontaneous_replies_c1",
        "C1",
        "Taktičan odgovor, šala i popravak nesporazuma",
        "💬",
        [
            PhrasebookEntry(
                "Rado bih pomogla, ali danas ne mogu preuzeti cijeli posao; mogu pregledati nacrt.",
                "Odbijate prevelik zahtjev uz jasnu, ostvarivu ponudu pomoći.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Nespretno sam se izrazio: nisam osporavao vaš trud, nego procjenu potrebnog vremena.",
                "Nakon napete reakcije ispravljate vlastitu formulaciju i precizirate predmet kritike.",
                "formal",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Kad kažeš 'sjajno smo prošli', šališ se ili sam propustio neku dobru vijest?",
                "Zbog nesklada između riječi i situacije provjeravate je li poruka ironična.",
                "informal",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Dobro, barem smo dokazali da se i stručnjaci znaju izgubiti.",
                "Nakon bezazlene zajedničke pogreške šalite se na račun cijele skupine, uključujući sebe.",
                "informal",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Hajdemo spustiti loptu; čini mi se da odgovaramo na dva različita pitanja.",
                "U zahuktaloj raspravi smirujete ton i predlažete razjašnjenje predmeta neslaganja.",
                "informal",
                "c1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr_mediating_positions_c1",
        "C1",
        "Prenošenje stavova bez prisilnog slaganja",
        "🔗",
        [
            PhrasebookEntry(
                "Ako vas dobro razumijem, podržavate obnovu, ali ne i predloženi raspored radova.",
                "Kao posrednik provjeravate sažetak tuđeg stava prije nego što ga prenesete drugima.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Obje strane traže predvidljivost; razlikuju se u tome tko bi trebao snositi rizik.",
                "Na zajedničkom sastanku odvajate zajednički interes od stvarne točke razilaženja.",
                "formal",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Izrazili su spremnost za razgovor, ali nisu još prihvatili uvjete.",
                "Prenosite poruku odsutne skupine bez pretvaranja otvorenosti u pristanak.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Za obavijest stanarima predlažem jednostavniji tekst, uz iste rokove i obveze.",
                "Prilagođavate službenu formulaciju široj publici bez promjene sadržaja dogovora.",
                "formal",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Zabilježimo oko čega smo se složili, a pitanje troškova ostavimo izričito otvorenim.",
                "Završavate sastanak djelomičnim dogovorom bez prikrivanja preostalog neslaganja.",
                "neutral",
                "c1-unit-7",
            ),
        ],
    ),
]
