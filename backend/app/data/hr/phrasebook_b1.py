"""Croatian B1 phrases for practical interaction and communication repair."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "hr-experiences-b1",
        "B1",
        "Prepričavanje iskustva",
        "💬",
        [
            PhrasebookEntry(
                "Isprva je sve išlo prema planu, a onda se vrijeme promijenilo.",
                "Uvodite neočekivanu promjenu u priči o izletu.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Dok smo čekali pomoć, pokušavali smo pronaći drugi put.",
                "Povezujete dvije aktivnosti koje su trajale istodobno.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Tražio sam ključeve cijelo jutro, ali ih nisam našao.",
                "Razlikujete dug trud od rezultata koji nije ostvaren.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Tek sam kasnije shvatila što se zapravo dogodilo.",
                "Objašnjavate da ste događaj razumjeli s odmakom.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Čekaj, prije toga smo još otišli po karte.",
                "Prijatelju ispravljate redoslijed događaja u zajedničkoj priči.",
                "informal",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Naposljetku smo se snašli i sada se tome smijemo.",
                "Završavate priču o poteškoći koja je dobro završila.",
                "informal",
                "b1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-travel-b1",
        "B1",
        "Promjena puta",
        "🚆",
        [
            PhrasebookEntry(
                "Hoću li stići na sljedeći vlak ako ovaj kasni dvadeset minuta?",
                "Kod konduktera provjeravate mogućnost planiranog presjedanja.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Gdje staje zamjenski autobus za sljedeću postaju?",
                "Tražite mjesto polaska tijekom prekida željezničkog prometa.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Prođite kroz pothodnik pa nastavite prema izlazu.",
                "Putniku dajete upute za izlazak s kolodvora.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Pokazala sam mu kartu, ali rekao je da vrijedi za drugi polazak.",
                "Suputniku objašnjavate problem s kartom.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Oprostite, mislila sam na autobusni, a ne na željeznički kolodvor.",
                "Ispravljate nesporazum o traženom odredištu.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Postoji li druga veza do odredišta? Molim vas, provjerite.",
                "Na informacijama tražite pomoć nakon propuštenog polaska.",
                "formal",
                "b1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-negotiation-b1",
        "B1",
        "Dogovaranje uvjeta",
        "🤝",
        [
            PhrasebookEntry(
                "Biste li mogli ponuditi neki drugi termin?",
                "Uljudno tražite promjenu ponuđenog termina.",
                "formal",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Kad bismo počeli ranije, imali bismo više vremena za pitanja.",
                "Predlažete promjenu i navodite njezinu moguću korist.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Mogla bih preuzeti petak ako ti odgovara subota.",
                "Kolegici nudite zamjenu smjene uz provjeru njezine dostupnosti.",
                "informal",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Ta bi nam cijena odgovarala uz malo dulji rok plaćanja.",
                "Pregovarate o uvjetima ponude umjesto da je odmah odbijete.",
                "formal",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Zapišimo dogovor kako bismo izbjegli nesporazume.",
                "Predlažete pisanu potvrdu i objašnjavate njezinu svrhu.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Razumijem vaš prijedlog, ali taj mi uvjet ne odgovara.",
                "Pristojno odbijate dio ponude i ostavljate prostor za daljnji razgovor.",
                "formal",
                "b1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-housing-b1",
        "B1",
        "Kvarovi i odnosi u zgradi",
        "🏠",
        [
            PhrasebookEntry(
                "Pišem vam zbog prozora koji se ne može dobro zatvoriti.",
                "Najmodavcu jasno navodite predmet i razlog poruke.",
                "formal",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Slavina je popravljena, ali ispod sudopera još curi voda.",
                "Razlikujete završeni popravak od preostalog problema.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Je li u najamninu uključeno parkirno mjesto?",
                "Prije najma provjeravate što obuhvaća ponuđena cijena.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Možemo li dogovoriti dolazak majstora dok sam kod kuće?",
                "Usklađujete pristup stanu s vlastitom dostupnošću.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "To je susjed kojem sam već prijavila buku.",
                "Precizirate o kojoj osobi govorite pri rješavanju problema.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Bili bismo vam zahvalni kad biste navečer malo stišali glazbu.",
                "Susjedima uljudno iznosite konkretnu molbu.",
                "formal",
                "b1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-services-b1",
        "B1",
        "Dokumenti i rokovi",
        "📄",
        [
            PhrasebookEntry(
                "Možete li mi reći koje priloge trebam dostaviti?",
                "Na šalteru provjeravate popis potrebnih dokumenata.",
                "formal",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Zanima me treba li donijeti izvornik ili je dovoljna preslika.",
                "Prije dolaska provjeravate oblik prihvatljivog dokumenta.",
                "formal",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Čim dobijem potvrdu, poslat ću vam je.",
                "Obvezujete se proslijediti dokument odmah nakon primitka.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Ako budete trebali dodatne podatke, javite mi se.",
                "Ostavljate mogućnost dopune zahtjeva tijekom postupka.",
                "formal",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Dok budem čekala rješenje, mogu li dopuniti zahtjev?",
                "Provjeravate dopušteni sljedeći korak dok postupak traje.",
                "formal",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Samo da provjerim: rok vrijedi za predaju, a ne za preuzimanje?",
                "Razjašnjavate na koju se fazu postupka odnosi navedeni datum.",
                "neutral",
                "b1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-communication-b1",
        "B1",
        "Prenošenje poruka i razjašnjavanje",
        "📨",
        [
            PhrasebookEntry(
                "Rekla je da će potvrditi termin do četvrtka.",
                "Prenosite najavu druge osobe bez tvrdnje da je termin već potvrdila.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Ako sam vas dobro razumio, sastanak još nije otkazan.",
                "Provjeravate točnost vlastitog razumijevanja.",
                "formal",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Nitko mi nije javio da se mjesto sastanka promijenilo.",
                "Objašnjavate zašto ste došli na staru adresu.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Meni je poslala nacrt, a konačnu verziju trebate tražiti od nje.",
                "Razlikujete dokument koji posjedujete od dokumenta koji sugovornik treba.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Oprosti, nisam mislio na ovaj petak, nego na sljedeći.",
                "Prijatelju ispravljate dvosmislen vremenski podatak.",
                "informal",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Drugim riječima, trebamo pričekati njezinu potvrdu prije rezervacije.",
                "Preoblikujete dogovor kako biste provjerili da ga svi jednako razumiju.",
                "neutral",
                "b1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "hr-community-b1",
        "B1",
        "Zajednička odluka",
        "🌳",
        [
            PhrasebookEntry(
                "Predlažem ovaj prostor jer je blizu autobusne stanice.",
                "Povezujete prijedlog mjesta s praktičnim razlogom.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Iako je ponuda povoljna, prostor nije dovoljno velik.",
                "Priznajete prednost ponude i upozoravate na važan nedostatak.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Osim toga, trebamo provjeriti pristup za invalidska kolica.",
                "U raspravu dodajete uvjet važan za sudjelovanje svih članova.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Razumijem vašu primjedbu; možemo li smanjiti trošak prijevoza?",
                "Uvažavate zabrinutost i usmjeravate razgovor na moguću prilagodbu.",
                "formal",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Unatoč lošem vremenu, radionicu možemo održati u dvorani.",
                "Nudite izvedivu mogućnost uz postojeću prepreku.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Dakle, ja ću rezervirati prostor, a vi ćete obavijestiti sudionike.",
                "Sažimate dogovor i jasno raspoređujete sljedeće zadatke.",
                "neutral",
                "b1-unit-7",
            ),
        ],
    ),
]
