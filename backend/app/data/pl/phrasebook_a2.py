"""Polish phrasebook — A2 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="zdrowie",
        level="A2",
        situation="U lekarza",
        icon="\U0001fa7a",
        phrases=[
            PhrasebookEntry(
                text="Chciałbym zapisać się na wizytę.",
                context="Umawianie wizyty w przychodni",
                register="formal",
            ),
            PhrasebookEntry(
                text="Od trzech dni boli mnie gardło.",
                context="Opisywanie objawów lekarzowi",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Mam gorączkę i mokry kaszel.",
                context="Podawanie kolejnych objawów",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Czy to coś poważnego?",
                context="Pytanie o wagę choroby",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Czy mogę dostać zwolnienie lekarskie?",
                context="Prośba o zwolnienie z pracy",
                register="formal",
            ),
            PhrasebookEntry(
                text="Proszę przyjmować ten lek dwa razy dziennie.",
                context="Polecenie lekarza dotyczące leczenia",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy ten lek jest dostępny bez recepty?",
                context="Pytanie w aptece o dostępność leku",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Muszę iść do dentysty, bo boli mnie ząb.",
                context="Zgłaszanie bólu zęba",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="podroze",
        level="A2",
        situation="Podróże i bilety",
        icon="\U0001f686",
        phrases=[
            PhrasebookEntry(
                text="Poproszę dwa bilety w obie strony.",
                context="Kupowanie biletów w kasie",
                register="neutral",
            ),
            PhrasebookEntry(
                text="O której odjeżdża pociąg do Gdańska?",
                context="Pytanie o godzinę odjazdu",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Czy trzeba się przesiadać?",
                context="Pytanie o połączenie bezpośrednie",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Z którego peronu odjeżdża pociąg?",
                context="Szukanie właściwego peronu",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Czy mogę zarezerwować miejsce przy oknie?",
                context="Rezerwacja konkretnego miejsca",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy jest jakieś tańsze połączenie?",
                context="Pytanie o tańsze połączenie",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Zgubiłem walizkę. Gdzie mogę to zgłosić?",
                context="Zgłaszanie zagubionego bagażu",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Ile kosztuje bilet ulgowy?",
                context="Pytanie o cenę biletu zniżkowego",
                register="neutral",
            ),
        ],
    ),
    PhrasebookCategory(
        id="praca",
        level="A2",
        situation="Praca i rozmowa kwalifikacyjna",
        icon="\U0001f4bc",
        phrases=[
            PhrasebookEntry(
                text="Chciałbym ubiegać się o to stanowisko.",
                context="Otwarcie rozmowy kwalifikacyjnej",
                register="formal",
            ),
            PhrasebookEntry(
                text="Mam trzy lata doświadczenia w obsłudze klienta.",
                context="Przedstawianie doświadczenia zawodowego",
                register="formal",
            ),
            PhrasebookEntry(
                text="Jakie będą moje obowiązki?",
                context="Pytanie o zakres zadań",
                register="formal",
            ),
            PhrasebookEntry(
                text="Kiedy mogę liczyć na odpowiedź?",
                context="Pytanie o termin informacji zwrotnej",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy oferujecie szkolenia dla nowych pracowników?",
                context="Pytanie o rozwój w firmie",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy mogę pracować zdalnie dwa dni w tygodniu?",
                context="Negocjowanie trybu pracy",
                register="formal",
            ),
            PhrasebookEntry(
                text="Mój kolega jest dziś na zwolnieniu.",
                context="Informowanie zespołu o nieobecności",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Czy możemy przesunąć spotkanie na czwartek?",
                context="Zmiana terminu narady",
                register="formal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="rozrywka",
        level="A2",
        situation="Rozrywka i zaproszenia",
        icon="\U0001f3ac",
        phrases=[
            PhrasebookEntry(
                text="Masz ochotę pójść jutro do kina?",
                context="Zaproszenie znajomego",
                register="informal",
            ),
            PhrasebookEntry(
                text="Chętnie, o której się spotykamy?",
                context="Przyjęcie zaproszenia",
                register="informal",
            ),
            PhrasebookEntry(
                text="Niestety nie mogę, mam już plany.",
                context="Odmowa zaproszenia",
                register="informal",
            ),
            PhrasebookEntry(
                text="Kupiłem bilety na koncert w sobotę.",
                context="Informowanie o kupionych biletach",
                register="informal",
            ),
            PhrasebookEntry(
                text="Może zamówimy pizzę i obejrzymy film?",
                context="Propozycja wspólnego wieczoru",
                register="informal",
            ),
            PhrasebookEntry(
                text="Ten film podobno jest naprawdę dobry.",
                context="Polecanie filmu",
                register="informal",
            ),
            PhrasebookEntry(
                text="Zapraszam cię na kolację w piątek.",
                context="Zaproszenie na kolację",
                register="informal",
            ),
            PhrasebookEntry(
                text="Daj znać, czy będziesz mógł przyjść.",
                context="Prośba o potwierdzenie obecności",
                register="informal",
            ),
        ],
    ),
    PhrasebookCategory(
        id="mieszkanie",
        level="A2",
        situation="Mieszkanie i sąsiedztwo",
        icon="\U0001f3e0",
        phrases=[
            PhrasebookEntry(
                text="Szukam mieszkania do wynajęcia.",
                context="Rozmowa z pośrednikiem nieruchomości",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Czy czynsz obejmuje opłaty za media?",
                context="Pytanie o wysokość opłat",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Od kiedy mogę się wprowadzić?",
                context="Ustalanie terminu przeprowadzki",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Czy w budynku jest winda?",
                context="Pytanie o wyposażenie budynku",
                register="neutral",
            ),
            PhrasebookEntry(
                text="W okolicy jest dużo sklepów, a przystanek jest tuż za rogiem.",
                context="Opisywanie sąsiedztwa",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Przepraszam, czy może pan ściszyć muzykę?",
                context="Uprzejma prośba do sąsiada",
                register="formal",
            ),
            PhrasebookEntry(
                text="Sąsiad z góry hałasuje po nocach.",
                context="Skarga na uciążliwego sąsiada",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Chciałbym podpisać umowę najmu.",
                context="Finalizowanie wynajmu",
                register="formal",
            ),
        ],
    ),
]
