"""Croatian A1 phrases for everyday encounters."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "hr-introductions-a1",
        "A1",
        "Pozdravljanje i upoznavanje",
        "👋",
        [
            PhrasebookEntry("Dobar dan!", "Pri susretu tijekom dana.", "neutral", "a1-unit-1"),
            PhrasebookEntry("Dobro jutro!", "Pri jutarnjem susretu.", "neutral", "a1-unit-1"),
            PhrasebookEntry(
                "Zovem se Ana.", "Pri predstavljanju vlastitim imenom.", "neutral", "a1-unit-1"
            ),
            PhrasebookEntry(
                "Kako se zovete?",
                "Kada uljudno pitamo novu odraslu osobu za ime.",
                "formal",
                "a1-unit-1",
            ),
            PhrasebookEntry("Drago mi je.", "Kao odgovor pri upoznavanju.", "neutral", "a1-unit-1"),
            PhrasebookEntry(
                "Kako si?", "Kada pitamo prijatelja kako se osjeća.", "informal", "a1-unit-1"
            ),
            PhrasebookEntry(
                "Doviđenja!", "Pri završetku susreta ili razgovora.", "neutral", "a1-unit-1"
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-home-a1",
        "A1",
        "U domu i s obitelji",
        "🏠",
        [
            PhrasebookEntry(
                "Ovo je moja obitelj.", "Pri predstavljanju obitelji.", "neutral", "a1-unit-2"
            ),
            PhrasebookEntry(
                "Dobro došli!",
                "Kada dočekujemo goste ili se uljudno obraćamo jednom gostu.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Ovo je vaša soba.", "Kada gostu pokazujemo sobu.", "formal", "a1-unit-2"
            ),
            PhrasebookEntry(
                "Gdje je kupaonica?", "Pri prvom posjetu domu.", "neutral", "a1-unit-2"
            ),
            PhrasebookEntry(
                "Čija je ovo torba?", "Kada ne znamo komu pripada torba.", "neutral", "a1-unit-2"
            ),
            PhrasebookEntry(
                "To je moj ključ.", "Kada prepoznamo svoj predmet.", "neutral", "a1-unit-2"
            ),
            PhrasebookEntry(
                "Vaš stan je lijep.", "Kada uljudno pohvalimo dom domaćina.", "formal", "a1-unit-2"
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-learning-a1",
        "A1",
        "Razgovor i učenje",
        "💬",
        [
            PhrasebookEntry(
                "Govorim malo hrvatskog.",
                "Kada opisujemo svoje početno znanje jezika.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry("Ne razumijem.", "Kada poruka nije jasna.", "neutral", "a1-unit-3"),
            PhrasebookEntry(
                "Što znači ova riječ?",
                "Kada tražimo značenje nepoznate riječi.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Kako se to piše?",
                "Kada trebamo zapisati nepoznatu riječ.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Možete li ponoviti?",
                "Kada uljudno tražimo da sugovornik kaže nešto još jednom.",
                "formal",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Govorite sporije, molim.",
                "Kada je govor sugovornika prebrz.",
                "formal",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Koji je vaš telefonski broj?",
                "Kada razmjenjujemo kontaktne podatke.",
                "formal",
                "a1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-orders-a1",
        "A1",
        "Narudžbe i plaćanje",
        "☕",
        [
            PhrasebookEntry(
                "Jednu kavu, molim.", "Pri naručivanju u kafiću.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Imate li čaj?", "Kada provjeravamo ponudu pića.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Bez šećera, molim.", "Kada ne želimo šećer u piću.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Koliko ovo košta?", "Kada pitamo za cijenu proizvoda.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Mogu li platiti karticom?",
                "Kada provjeravamo prihvaćeni način plaćanja.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Račun, molim.", "Na kraju posjeta kafiću ili restoranu.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry("To je sve, hvala.", "Kada završimo narudžbu.", "neutral", "a1-unit-4"),
        ],
    ),
    PhrasebookCategory(
        "hr-directions-a1",
        "A1",
        "Putovanje i snalaženje",
        "🚌",
        [
            PhrasebookEntry(
                "Oprostite, gdje je kolodvor?",
                "Kada uljudno pitamo prolaznika za mjesto polaska.",
                "formal",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Je li daleko?", "Nakon što saznamo gdje je odredište.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry(
                "Idite ravno pa lijevo.",
                "Kada dajemo kratku uputu za put.",
                "formal",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Jednu kartu za Split, molim.",
                "Pri kupnji karte na blagajni.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Ide li ovaj autobus u centar?",
                "Prije ulaska u autobus.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Gdje je naše stajalište?",
                "Kada sa suputnikom tražimo mjesto ukrcaja.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Trebam kartu za tramvaj.",
                "Kada tražimo odgovarajuću voznu kartu.",
                "neutral",
                "a1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-meetings-a1",
        "A1",
        "Dogovor i slobodno vrijeme",
        "📅",
        [
            PhrasebookEntry("Koliko je sati?", "Kada nemamo sat pri ruci.", "neutral", "a1-unit-6"),
            PhrasebookEntry(
                "Imaš li vremena sutra?",
                "Kada želimo dogovoriti susret s prijateljem.",
                "informal",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Idemo na kavu?", "Kao poziv prijatelju na druženje.", "informal", "a1-unit-6"
            ),
            PhrasebookEntry(
                "Vidimo se u pet.",
                "Kada potvrđujemo poznato vrijeme susreta.",
                "informal",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "U subotu sam slobodna.",
                "Kada govornica kaže koji dan ima vremena.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Danas se odmaram.", "Kada opisujemo plan za slobodan dan.", "neutral", "a1-unit-6"
            ),
            PhrasebookEntry(
                "Vidimo se sutra!",
                "Pri rastanku prije dogovorenog susreta.",
                "informal",
                "a1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-assistance-a1",
        "A1",
        "Pomoć i zdravlje",
        "🩺",
        [
            PhrasebookEntry(
                "Možete li mi pomoći?", "Kada uljudno tražimo pomoć.", "formal", "a1-unit-7"
            ),
            PhrasebookEntry(
                "Ne osjećam se dobro.",
                "Kada opisujemo loše zdravstveno stanje.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry("Boli me glava.", "Kada navodimo mjesto boli.", "neutral", "a1-unit-7"),
            PhrasebookEntry(
                "Trebam liječnika.", "Kada tražimo liječničku pomoć.", "neutral", "a1-unit-7"
            ),
            PhrasebookEntry(
                "Gdje je najbliža ljekarna?",
                "Kada trebamo lijek ili savjet ljekarnika.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Nazovite hitnu pomoć, molim.",
                "Kada je potrebna hitna medicinska pomoć.",
                "formal",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Moj telefon ne radi.",
                "Kada objašnjavamo zašto ne možemo sami nazvati.",
                "neutral",
                "a1-unit-7",
            ),
        ],
    ),
]
