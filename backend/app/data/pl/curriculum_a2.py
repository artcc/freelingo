"""A2 curriculum units — Polish (pl-PL)."""

from __future__ import annotations

from app.data._types import CurriculumUnit

A2_UNITS: list[CurriculumUnit] = [
    CurriculumUnit(
        id="a2-unit-1",
        level="A2",
        unit_number=1,
        title="Wspomnienia i dzieciństwo",
        grammar_points=["czas-przeszly-rodzaj", "aspekt-wprowadzenie", "dopelniacz"],
        vocabulary_set_ids=["wspomnienia_a2", "dziecinstwo_a2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Opowiada o przeszłości z poprawną końcówką rodzajową i osobową: "
            "byłem, byłam, byliśmy, uczyły się",
            "Rozróżnia czasowniki niedokonane i dokonane w prostych parach: "
            "czytać — przeczytać, pisać — napisać",
            "Używa dopełniacza po rzeczownikach i przyimkach: koniec wakacji, "
            "wracam z pracy, uczyłem się języka",
            "Pisze krótkie wspomnienie z dzieciństwa, łącząc czas przeszły " "z wyrażeniami czasu",
        ],
        default_weeks=2,
        prerequisite_unit=None,
    ),
    CurriculumUnit(
        id="a2-unit-2",
        level="A2",
        unit_number=2,
        title="Zakupy i ilości",
        grammar_points=[
            "dopelniacz-liczebniki",
            "zaimki-dopelniacz",
            "liczebniki-porzadkowe",
        ],
        vocabulary_set_ids=["zakupy_a2", "pieniadze_a2", "ubrania_a2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Łączy liczebniki z dopełniaczem: pięć jabłek, dwadzieścia złotych, " "kilka minut",
            "Stosuje zaimki osobowe w dopełniaczu: nie mam go, potrzebuję jej, " "szukam ich",
            "Tworzy liczebniki porządkowe i używa ich w datach oraz adresach: "
            "pierwszy maja, trzecie piętro",
            "Prowadzi rozmowę w sklepie: pyta o rozmiar, cenę i dostępność towaru",
        ],
        default_weeks=2,
        prerequisite_unit="a2-unit-1",
    ),
    CurriculumUnit(
        id="a2-unit-3",
        level="A2",
        unit_number=3,
        title="Zdrowie i samopoczucie",
        grammar_points=["celownik", "boli-mnie", "tryb-rozka"],
        vocabulary_set_ids=["zdrowie_a2", "cialo_a2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Używa celownika w typowych konstrukcjach: pomagam mamie, "
            "źle mi się robi, dziękuję lekarzowi",
            "Mówi o dolegliwościach: boli mnie głowa, bolą mnie plecy, " "jest mi zimno",
            "Tworzy tryb rozkazujący i rozumie polecenia lekarza oraz farmaceuty: "
            "proszę wziąć, niech pan odpocznie",
            "Relacjonuje wizytę u lekarza i opisuje objawy w krótkiej rozmowie",
        ],
        default_weeks=2,
        prerequisite_unit="a2-unit-2",
    ),
    CurriculumUnit(
        id="a2-unit-4",
        level="A2",
        unit_number=4,
        title="Podróże i komunikacja",
        grammar_points=["narzednik", "przyimki-narzednik", "czasowniki-prefiksalne"],
        vocabulary_set_ids=["podroze_a2", "transport_a2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Używa narzędnika z przyimkami z i nad oraz w konstrukcjach typu "
            "jechać pociągiem, interesować się sportem",
            "Rozumie i stosuje podstawowe czasowniki z przedrostkami ruchu: "
            "przyjechać, wyjechać, dojechać, przejechać",
            "Kupuje bilet i pyta o połączenie: o której odjeżdża pociąg, "
            "czy trzeba się przesiadać",
            "Opisuje podróż i rozwiązuje proste sytuacje na dworcu oraz na lotnisku",
        ],
        default_weeks=2,
        prerequisite_unit="a2-unit-3",
    ),
    CurriculumUnit(
        id="a2-unit-5",
        level="A2",
        unit_number=5,
        title="Praca i obowiązki",
        grammar_points=[
            "musiec-powinien",
            "konstrukcje-bezokolicznikowe",
            "przyimki-czasu",
        ],
        vocabulary_set_ids=["praca_a2", "obowiazki_a2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Wyraża obowiązek i powinność: muszę skończyć, powinieneś odpocząć, " "nie wolno palić",
            "Używa konstrukcji z bezokolicznikiem: łatwo zapomnieć, trudno powiedzieć, "
            "warto spróbować",
            "Stosuje przyimki czasu: przed pracą, po spotkaniu, od poniedziałku, " "do piątku",
            "Opisuje swoje obowiązki zawodowe i uzgadnia prosty termin spotkania",
        ],
        default_weeks=2,
        prerequisite_unit="a2-unit-4",
    ),
    CurriculumUnit(
        id="a2-unit-6",
        level="A2",
        unit_number=6,
        title="Rozrywka i technologia",
        grammar_points=[
            "czas-przyszly-niedokonany",
            "tryb-warunkowy",
            "zdania-z-ze",
        ],
        vocabulary_set_ids=["rozrywka_a2", "technologia_a2", "sport_a2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Tworzy czas przyszły niedokonany: będę oglądać, będziecie pracować",
            "Buduje tryb warunkowy z by: chciałbym, moglibyśmy, gdybyś miał czas",
            "Łączy zdania spójnikiem że i przekazuje proste komunikaty: "
            "myślę, że to dobry pomysł",
            "Dyskutuje o filmach, muzyce i technologii, wyrażając preferencje " "i propozycje",
        ],
        default_weeks=2,
        prerequisite_unit="a2-unit-5",
    ),
    CurriculumUnit(
        id="a2-unit-7",
        level="A2",
        unit_number=7,
        title="Mieszkanie i okolica",
        grammar_points=[
            "miejscownik-przyimki",
            "stopniowanie-przymiotnikow",
            "przyslowki",
        ],
        vocabulary_set_ids=["mieszkanie_a2", "okolica_a2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Używa miejscownika z przyimkami w, na, przy, o: mieszkam w Krakowie, "
            "rozmawiamy o mieszkaniu",
            "Stopniuje przymiotniki regularnie i nieregularnie: większy, największy, "
            "lepszy, najlepszy",
            "Tworzy przysłówki odprzymiotnikowe i stopniuje je: szybko — szybciej — " "najszybciej",
            "Opisuje mieszkanie i sąsiedztwo oraz porównuje dwa miejsca zamieszkania",
        ],
        default_weeks=2,
        prerequisite_unit="a2-unit-6",
    ),
    CurriculumUnit(
        id="a2-unit-8",
        level="A2",
        unit_number=8,
        title="Powtórka A2",
        grammar_points=[
            "czas-przeszly-rodzaj",
            "aspekt-wprowadzenie",
            "dopelniacz",
            "celownik",
            "narzednik",
            "tryb-warunkowy",
            "stopniowanie-przymiotnikow",
        ],
        vocabulary_set_ids=["powtorka_a2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Opowiada o doświadczeniach i planach, płynnie przechodząc między "
            "czasem przeszłym, teraźniejszym i przyszłym",
            "Dobiera przypadek do funkcji zdania w rozmowie o zdrowiu, pracy " "i podróżach",
            "Formułuje prośby, propozycje i warunki w uprzejmym rejestrze",
            "Czyta krótki tekst użytkowy i wyciąga z niego najważniejsze informacje "
            "oraz intencję autora",
        ],
        default_weeks=1,
        prerequisite_unit="a2-unit-7",
    ),
]
