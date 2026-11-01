"""A2 vocabulary sets."""

from app.data._types import PartOfSpeech, VocabularyEntry, VocabularySet


def _entry(word: str, pos: PartOfSpeech, definition: str, example: str) -> VocabularyEntry:
    return VocabularyEntry(word=word, pos=pos, definition=definition, example=example)


A2_SETS: list[VocabularySet] = [
    VocabularySet(
        id="doswiadczenia_a2",
        level="A2",
        topic="Wydarzenia i doświadczenia",
        unit_ref="a2-unit-1",
        words=[
            _entry(
                "wspomnienie",
                "noun",
                "Obraz lub myśl o czymś, co wydarzyło się wcześniej.",
                "To miłe wspomnienie z dzieciństwa.",
            ),
            _entry(
                "odwiedzić",
                "verb",
                "Przyjść do kogoś lub jakiegoś miejsca z wizytą.",
                "W sobotę odwiedziłam babcię.",
            ),
            _entry(
                "podróżować",
                "verb",
                "Przemieszczać się między miejscami.",
                "Latem lubimy podróżować pociągiem.",
            ),
            _entry(
                "wydarzenie",
                "noun",
                "Coś, co się stało lub jest zaplanowane.",
                "Koncert był ważnym wydarzeniem.",
            ),
        ],
    ),
    VocabularySet(
        id="zakupy_a2",
        level="A2",
        topic="Zakupy i usługi",
        unit_ref="a2-unit-2",
        words=[
            _entry(
                "paragon",
                "noun",
                "Dokument potwierdzający zakup.",
                "Proszę zachować paragon.",
            ),
            _entry(
                "zwrot",
                "noun",
                "Oddanie kupionego produktu i odzyskanie pieniędzy.",
                "Sklep przyjmuje zwroty przez czternaście dni.",
            ),
            _entry(
                "opakowanie",
                "noun",
                "Osłona, w której sprzedaje się lub przechowuje produkt.",
                "Czy mogę prosić o papierowe opakowanie?",
            ),
            _entry(
                "kosztować",
                "verb",
                "Mieć określoną cenę.",
                "Ile kosztuje ten plecak?",
            ),
        ],
    ),
    VocabularySet(
        id="podroze_a2",
        level="A2",
        topic="Podróże i noclegi",
        unit_ref="a2-unit-3",
        words=[
            _entry(
                "odjazd",
                "noun",
                "Rozpoczęcie podróży przez pojazd.",
                "Odjazd pociągu zaplanowano na dziewiątą.",
            ),
            _entry(
                "przesiadka",
                "noun",
                "Zmiana pojazdu podczas podróży.",
                "Na tej trasie potrzebna jest jedna przesiadka.",
            ),
            _entry(
                "rezerwować",
                "verb",
                "Zamawiać miejsce lub usługę z wyprzedzeniem.",
                "Chcemy zarezerwować pokój na trzy noce.",
            ),
            _entry(
                "bagaż",
                "noun",
                "Rzeczy zabierane ze sobą w podróż.",
                "Mój bagaż jest już w przechowalni.",
            ),
        ],
    ),
    VocabularySet(
        id="zdrowie_a2",
        level="A2",
        topic="Zdrowie i samopoczucie",
        unit_ref="a2-unit-4",
        words=[
            _entry(
                "ból",
                "noun",
                "Nieprzyjemne odczucie w ciele.",
                "Od rana czuję ból gardła.",
            ),
            _entry(
                "apteka",
                "noun",
                "Miejsce, w którym kupuje się leki.",
                "Najbliższa apteka jest przy rynku.",
            ),
            _entry(
                "odpoczywać",
                "verb",
                "Odzyskiwać siły po wysiłku lub chorobie.",
                "Lekarz zalecił mi odpoczywać.",
            ),
            _entry(
                "zdrowie",
                "noun",
                "Stan organizmu i jego prawidłowe funkcjonowanie.",
                "Regularny sen jest ważny dla zdrowia.",
            ),
        ],
    ),
    VocabularySet(
        id="mieszkanie_a2",
        level="A2",
        topic="Mieszkanie i codzienne usługi",
        unit_ref="a2-unit-5",
        words=[
            _entry(
                "czynsz",
                "noun",
                "Regularna opłata za wynajmowane mieszkanie.",
                "Czynsz płacę do dziesiątego dnia miesiąca.",
            ),
            _entry(
                "właściciel",
                "noun",
                "Osoba, do której należy dana rzecz lub lokal.",
                "Właściciel naprawił zepsuty kran.",
            ),
            _entry(
                "umawiać się",
                "verb",
                "Ustalać wspólnie termin spotkania lub usługi.",
                "Umawiam się z hydraulikiem na piątek.",
            ),
            _entry(
                "naprawa",
                "noun",
                "Usunięcie usterki lub przywrócenie sprawności.",
                "Naprawa pralki potrwa jeden dzień.",
            ),
        ],
    ),
    VocabularySet(
        id="czas_wolny_a2",
        level="A2",
        topic="Czas wolny i zainteresowania",
        unit_ref="a2-unit-6",
        words=[
            _entry(
                "zainteresowanie",
                "noun",
                "Czynność lub temat, który kogoś ciekawi.",
                "Moim zainteresowaniem jest fotografia.",
            ),
            _entry(
                "wystawa",
                "noun",
                "Publiczna prezentacja dzieł lub przedmiotów.",
                "W sobotę odwiedzamy wystawę malarstwa.",
            ),
            _entry(
                "spotykać się",
                "verb",
                "Spędzać czas z inną osobą lub grupą.",
                "W weekend spotykam się ze znajomymi.",
            ),
            _entry(
                "wypożyczać",
                "verb",
                "Brać coś na pewien czas z obowiązkiem zwrotu.",
                "W bibliotece wypożyczam książki.",
            ),
        ],
    ),
    VocabularySet(
        id="plany_a2",
        level="A2",
        topic="Plany, pogoda i pory roku",
        unit_ref="a2-unit-7",
        words=[
            _entry(
                "prognoza",
                "noun",
                "Przewidywanie, jaka będzie pogoda lub inne zjawisko.",
                "Prognoza zapowiada deszcz.",
            ),
            _entry(
                "wiosna",
                "noun",
                "Pora roku między zimą a latem.",
                "Wiosną dni stają się dłuższe.",
            ),
            _entry(
                "planować",
                "verb",
                "Zastanawiać się, co chce się zrobić w przyszłości.",
                "Planujemy wycieczkę w góry.",
            ),
            _entry(
                "zachmurzenie",
                "noun",
                "Stopień pokrycia nieba chmurami.",
                "Po południu zachmurzenie będzie duże.",
            ),
        ],
    ),
    VocabularySet(
        id="powtorka_a2",
        level="A2",
        topic="Powtórka: codzienne sprawy",
        unit_ref="a2-unit-8",
        words=[
            _entry(
                "doświadczenie",
                "noun",
                "Wiedza zdobyta dzięki temu, co się przeżyło lub zrobiło.",
                "To było ciekawe doświadczenie.",
            ),
            _entry(
                "dostępny",
                "adjective",
                "Możliwy do użycia, kupienia lub uzyskania.",
                "Pokój jest dostępny od soboty.",
            ),
            _entry(
                "zwykle",
                "adverb",
                "W sposób typowy lub powtarzający się.",
                "Zwykle dojeżdżam do pracy autobusem.",
            ),
            _entry(
                "wygodny",
                "adjective",
                "Zapewniający komfort lub łatwy w użyciu.",
                "Ten pociąg ma wygodne siedzenia.",
            ),
        ],
    ),
]
