"""B1 curriculum units — Polish (pl-PL)."""

from __future__ import annotations

from app.data._types import CurriculumUnit

B1_UNITS: list[CurriculumUnit] = [
    CurriculumUnit(
        id="b1-unit-1",
        level="B1",
        unit_number=1,
        title="Relacje i emocje",
        grammar_points=["aspekt-pary", "zdania-wzgledne", "zaimki-wzgledne"],
        vocabulary_set_ids=["emocje_b1", "relacje_b1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Dobiera aspekt czasownika do znaczenia wypowiedzi: pisać list "
            "i napisać list, uczyć się i nauczyć się",
            "Tworzy zdania względne z który, która, które i zaimkami względnymi " "kto, co, gdzie",
            "Opisuje relacje i emocje, precyzując intensywność i przyczynę stanu: "
            "jestem zmęczony, bo..., cieszę się, że...",
            "Pisze wiadomość do bliskiej osoby, dobierając ton i formę do relacji",
        ],
        default_weeks=2,
        prerequisite_unit=None,
    ),
    CurriculumUnit(
        id="b1-unit-2",
        level="B1",
        unit_number=2,
        title="Edukacja i kariera",
        grammar_points=[
            "strona-bierna",
            "imieslow-przymiotnikowy",
            "mowa-zalezna",
        ],
        vocabulary_set_ids=["edukacja_b1", "praca_b1", "kariera_b1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Buduje stronę bierną z być i imiesłowem biernym: projekt został "
            "przygotowany, dokumenty są przechowywane",
            "Używa imiesłowu przymiotnikowego czynnego i biernego w opisach: "
            "uczący się student, napisany raport",
            "Przekazuje cudzą wypowiedź, dopasowując zaimki i formy czasu: "
            "powiedział, że szuka pracy",
            "Opisuje ścieżkę edukacyjną i zawodową oraz uzasadnia wybory",
        ],
        default_weeks=2,
        prerequisite_unit="b1-unit-1",
    ),
    CurriculumUnit(
        id="b1-unit-3",
        level="B1",
        unit_number=3,
        title="Zdrowie i styl życia",
        grammar_points=[
            "tryb-warunkowy-zdania",
            "zdania-przyczynowe",
            "spojniki",
        ],
        vocabulary_set_ids=["zdrowie_b1", "styl_zycia_b1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Buduje zdania warunkowe z gdyby i jeżeli w realnych scenariuszach: "
            "gdybym miał czas, chodziłbym na siłownię",
            "Łączy zdania spójnikami przyczyny i skutku: ponieważ, dlatego że, więc",
            "Stosuje spójniki przeciwstawne i wynikowe: jednak, natomiast, zatem",
            "Uzasadnia decyzje dotyczące zdrowia i stylu życia w dłuższej wypowiedzi",
        ],
        default_weeks=2,
        prerequisite_unit="b1-unit-2",
    ),
    CurriculumUnit(
        id="b1-unit-4",
        level="B1",
        unit_number=4,
        title="Kultura i sztuka",
        grammar_points=[
            "imieslow-przyslowkowy",
            "konstrukcje-bezosobowe",
            "rzeczowniki-odczasownikowe",
        ],
        vocabulary_set_ids=["kultura_b1", "sztuka_b1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Używa imiesłowu przysłówkowego współczesnego i uprzedniego: "
            "czytając książkę, przeczytawszy recenzję",
            "Tworzy konstrukcje bezosobowe: mówi się, napisano, zbudowano",
            "Tworzy rzeczowniki odczasownikowe z -nie i -cie: czytanie, spotkanie",
            "Recenzuje wydarzenie kulturalne, łącząc opis, ocenę i uzasadnienie",
        ],
        default_weeks=2,
        prerequisite_unit="b1-unit-3",
    ),
    CurriculumUnit(
        id="b1-unit-5",
        level="B1",
        unit_number=5,
        title="Środowisko i społeczeństwo",
        grammar_points=["zdania-celowe", "zdania-czasowe", "przyimki-biernik"],
        vocabulary_set_ids=["srodowisko_b1", "spoleczenstwo_b1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Buduje zdania celowe z żeby i aby, dopasowując podmiot: "
            "wychodzę, żeby odpocząć; chcę, żebyś przyszedł",
            "Tworzy zdania czasowe z kiedy, gdy, zanim, po tym jak",
            "Stosuje przyimki z biernikiem w utartych wyrażeniach: "
            "przez cały dzień, na przyszłość, za tydzień",
            "Wyraża opinię o problemach społecznych i środowiskowych, podając "
            "argumenty i przykłady",
        ],
        default_weeks=2,
        prerequisite_unit="b1-unit-4",
    ),
    CurriculumUnit(
        id="b1-unit-6",
        level="B1",
        unit_number=6,
        title="Technologia i media",
        grammar_points=[
            "strona-bierna-czas",
            "prefiksy-znaczenia",
            "stopniowanie-przyslowkow",
        ],
        vocabulary_set_ids=["technologia_b1", "media_b1", "internet_b1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Używa strony biernej w różnych czasach: jest używany, był używany, " "będzie używany",
            "Rozróżnia znaczenia czasowników z przedrostkami: pisać, podpisać, "
            "wpisać, przepisać",
            "Stopniuje przysłówki nieregularne: dobrze — lepiej — najlepiej, "
            "dużo — więcej — najwięcej",
            "Omawia zalety i wady technologii, odwołując się do źródeł i przykładów",
        ],
        default_weeks=2,
        prerequisite_unit="b1-unit-5",
    ),
    CurriculumUnit(
        id="b1-unit-7",
        level="B1",
        unit_number=7,
        title="Podróże i doświadczenia",
        grammar_points=[
            "tryb-warunkowy-przeszly",
            "zdania-okolicznikowe",
            "partykuly",
        ],
        vocabulary_set_ids=["podroze_b1", "doswiadczenia_b1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Buduje nierealne zdania warunkowe o przeszłości: gdybym był wcześniej "
            "wyszedł, nie spóźniłbym się",
            "Tworzy zdania okolicznikowe sposobu i celu: siedząc przy oknie, "
            "wyjechał, aby zwiedzić miasto",
            "Używa partykuł wzmacniających i ograniczających: nawet, tylko, " "przecież, właśnie",
            "Opowiada o podróży i wyciąga wnioski z doświadczeń, używając "
            "zróżnicowanych konstrukcji",
        ],
        default_weeks=2,
        prerequisite_unit="b1-unit-6",
    ),
    CurriculumUnit(
        id="b1-unit-8",
        level="B1",
        unit_number=8,
        title="Powtórka B1",
        grammar_points=[
            "aspekt-pary",
            "strona-bierna",
            "mowa-zalezna",
            "tryb-warunkowy-zdania",
            "zdania-celowe",
            "imieslow-przyslowkowy",
            "spojniki",
        ],
        vocabulary_set_ids=["powtorka_b1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Relacjonuje wydarzenie, łącząc mowę zależną, stronę bierną "
            "i konstrukcje bezosobowe",
            "Buduje dłuższą wypowiedź argumentacyjną z poprawnymi spójnikami "
            "i zróżnicowanym słownictwem",
            "Stosuje aspekt czasownika świadomie w narracji i opisie nawyków",
            "Czyta tekst publicystyczny i odróżnia fakty od opinii autora",
        ],
        default_weeks=1,
        prerequisite_unit="b1-unit-7",
    ),
]
