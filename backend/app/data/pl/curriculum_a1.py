"""A1 curriculum units — Polish (pl-PL)."""

from __future__ import annotations

from app.data._types import CurriculumUnit

A1_UNITS: list[CurriculumUnit] = [
    CurriculumUnit(
        id="a1-unit-1",
        level="A1",
        unit_number=1,
        title="Powitania i przedstawianie się",
        grammar_points=["byc", "zaimki-osobowe", "rodzaj-rzeczownika"],
        vocabulary_set_ids=["alfabet_a1", "liczby_a1", "powitania_a1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Wita się i żegna, dobierając rejestr do sytuacji: cześć, dzień dobry, "
            "dobry wieczór, do widzenia, na razie",
            "Przedstawia się i podaje podstawowe informacje: nazywam się Anna, "
            "jestem z Polski, mam dwadzieścia lat",
            "Odmienia czasownik być w liczbie pojedynczej i mnogiej i łączy go "
            "z właściwym zaimkiem osobowym",
            "Rozpoznaje rodzaj gramatyczny rzeczownika po końcówce i dobiera do niego "
            "poprawną formę czasownika oraz przymiotnika",
        ],
        default_weeks=2,
        prerequisite_unit=None,
    ),
    CurriculumUnit(
        id="a1-unit-2",
        level="A1",
        unit_number=2,
        title="Narodowości i zawody",
        grammar_points=["narzednik-narodowosc", "mianownik-liczba-mnoga", "zawod-rodzaj"],
        vocabulary_set_ids=["przedstawianie_sie_a1", "narodowosci_a1", "zawody_a1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Mówi o narodowości i pochodzeniu, używając narzędnika po być oraz "
            "dopełniacza po przyimku z: "
            "jestem Polakiem, jestem z Hiszpanii",
            "Tworzy mianownik liczby mnogiej rzeczowników osobowych i nieosobowych: "
            "student — studenci, kot — koty, okno — okna",
            "Nazywa zawody i odróżnia formy męskie od żeńskich: nauczyciel — nauczycielka, "
            "lekarz — lekarka",
            "Prowadzi krótką rozmowę zapoznawczą, pytając o kraj, zawód i miejsce zamieszkania",
        ],
        default_weeks=2,
        prerequisite_unit="a1-unit-1",
    ),
    CurriculumUnit(
        id="a1-unit-3",
        level="A1",
        unit_number=3,
        title="Rodzina i opisy",
        grammar_points=["przymiotniki-rodzaj", "zaimki-dzierzawcze", "przeczenie-nie"],
        vocabulary_set_ids=["rodzina_a1", "wyglad_a1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Nazywa członków rodziny i mówi o relacjach: moja siostra, mój brat, "
            "nasi dziadkowie",
            "Dostosowuje przymiotnik do rodzaju i liczby rzeczownika: wysoki ojciec, "
            "wysoka matka, wysokie dzieci",
            "Używa zaimków dzierżawczych w mianowniku i rozpoznaje ich formy zależne "
            "w prostych zdaniach",
            "Tworzy przeczenia z nie i odróżnia je od przeczenia czasownika: to nie jest mój brat",
        ],
        default_weeks=2,
        prerequisite_unit="a1-unit-2",
    ),
    CurriculumUnit(
        id="a1-unit-4",
        level="A1",
        unit_number=4,
        title="Codzienna rutyna",
        grammar_points=["czas-terazniejszy", "czasowniki-zwrotne", "godziny-dni"],
        vocabulary_set_ids=["czas_a1", "dni_tygodnia_a1", "czynnosci_a1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Odmienia częste czasowniki według podstawowych wzorców czasu teraźniejszego: "
            "mieszkać — mieszkam, mówić — mówię",
            "Używa czasowników zwrotnych z właściwą formą się: myć się, ubierać się, "
            "kłaść się spać",
            "Podaje godzinę i datę: jest siódma, o wpół do ósmej, w poniedziałek, " "piątego maja",
            "Opisuje swoją rutynę w spójnym tekście z wyrażeniami czasu: rano, po południu, "
            "wieczorem, codziennie",
        ],
        default_weeks=2,
        prerequisite_unit="a1-unit-3",
    ),
    CurriculumUnit(
        id="a1-unit-5",
        level="A1",
        unit_number=5,
        title="Jedzenie i zakupy",
        grammar_points=["biernik", "liczebniki", "czasowniki-modalne"],
        vocabulary_set_ids=["jedzenie_a1", "zakupy_a1", "napoje_a1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Używa biernika rzeczowników żeńskich i męskich nieżywotnych: kupuję kawę, "
            "jem chleb",
            "Łączy liczebniki z rzeczownikami w typowych połączeniach: dwa jabłka, "
            "pięć złotych, trzy kawy",
            "Stosuje czasowniki modalne z bezokolicznikiem: chcę kupić, muszę iść, "
            "mogę zapłacić kartą",
            "Zamawia posiłek i robi proste zakupy w sklepie oraz w restauracji",
        ],
        default_weeks=2,
        prerequisite_unit="a1-unit-4",
    ),
    CurriculumUnit(
        id="a1-unit-6",
        level="A1",
        unit_number=6,
        title="Dom i okolica",
        grammar_points=["miejscownik", "przyimki-miejsca", "czasowniki-ruchu"],
        vocabulary_set_ids=["dom_a1", "meble_a1", "miasto_a1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Tworzy miejscownik z przyimkami w i na: w kuchni, na balkonie, w Polsce",
            "Opisuje położenie przedmiotów i miejsc: na stole, pod łóżkiem, obok okna, "
            "między szafą a drzwiami",
            "Rozróżnia iść i chodzić oraz jechać i jeździć w prostych kontekstach " "ruchowych",
            "Opisuje swoje mieszkanie i okolicę oraz pyta o drogę w znanym otoczeniu",
        ],
        default_weeks=2,
        prerequisite_unit="a1-unit-5",
    ),
    CurriculumUnit(
        id="a1-unit-7",
        level="A1",
        unit_number=7,
        title="Podróże i pogoda",
        grammar_points=["czas-przyszly", "czas-przeszly", "dopelniacz-przeczenie"],
        vocabulary_set_ids=["podroze_a1", "pogoda_a1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Tworzy czas przyszły złożony: będę czytać, będziemy mieszkać, "
            "oraz prosty czas przyszły czasowników dokonanych: napiszę, pojedziemy",
            "Tworzy czas przeszły z właściwą końcówką rodzajową: byłem, byłam, " "byliśmy, czytała",
            "Używa dopełniacza po przeczeniu: nie mam czasu, nie ma mleka",
            "Opowiada o podróży i pogodzie, łącząc czas przeszły, przyszły i słownictwo "
            "tematyczne",
        ],
        default_weeks=2,
        prerequisite_unit="a1-unit-6",
    ),
    CurriculumUnit(
        id="a1-unit-8",
        level="A1",
        unit_number=8,
        title="Powtórka A1",
        grammar_points=[
            "byc",
            "czas-terazniejszy",
            "biernik",
            "miejscownik",
            "czas-przeszly",
            "czas-przyszly",
            "liczebniki",
            "przeczenie-nie",
        ],
        vocabulary_set_ids=["powtorka_a1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Prowadzi krótką rozmowę o sobie, rodzinie i codzienności bez dłuższych "
            "przerw w wypowiedzi",
            "Stosuje przypadki A1 w utartych zwrotach bez błędów systemowych: biernik, "
            "miejscownik i dopełniacz po przeczeniu",
            "Opowiada w czasie przeszłym i przyszłym o prostym wydarzeniu z życia",
            "Czyta krótki tekst o tematyce codziennej i odpowiada na pytania "
            "o najważniejsze informacje",
        ],
        default_weeks=1,
        prerequisite_unit="a1-unit-7",
    ),
]
