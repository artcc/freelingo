"""B2 curriculum units — Polish (pl-PL)."""

from __future__ import annotations

from app.data._types import CurriculumUnit

B2_UNITS: list[CurriculumUnit] = [
    CurriculumUnit(
        id="b2-unit-1",
        level="B2",
        unit_number=1,
        title="Argumentacja i opinie",
        grammar_points=[
            "tryb-warunkowy-hipotetyczny",
            "zdania-przeciwstawne",
            "partykuly-modalne",
        ],
        vocabulary_set_ids=["argumentacja_b2", "opinie_b2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Formułuje hipotezy i scenariusze nierealne: gdyby polityka się zmieniła, "
            "sytuacja wyglądałaby inaczej",
            "Buduje zdania przeciwstawne i ustępstwowe: wprawdzie..., ale; " "mimo że..., jednak",
            "Używa partykuł modalnych do stopniowania pewności: zapewne, chyba, "
            "rzekomo, podobno",
            "Broni własnej opinii w dyskusji, odpierając kontrargumenty",
        ],
        default_weeks=2,
        prerequisite_unit=None,
    ),
    CurriculumUnit(
        id="b2-unit-2",
        level="B2",
        unit_number=2,
        title="Praca i gospodarka",
        grammar_points=[
            "nominalizacja",
            "strona-bierna-zaawansowana",
            "konstrukcje-bezosobowe-zaawansowane",
        ],
        vocabulary_set_ids=["praca_b2", "gospodarka_b2", "finanse_b2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Przekształca zdania w konstrukcje nominalne: wzrost zatrudnienia, "
            "obniżenie kosztów, podjęcie decyzji",
            "Stosuje stronę bierną z modalnymi i w czasach złożonych: musi zostać "
            "zatwierdzony, został już wysłany",
            "Używa konstrukcji bezosobowych w tekstach formalnych: należy zauważyć, "
            "wymaga się, zaleca się",
            "Pisze służbowe pismo lub raport z zachowaniem formalnego rejestru",
        ],
        default_weeks=2,
        prerequisite_unit="b2-unit-1",
    ),
    CurriculumUnit(
        id="b2-unit-3",
        level="B2",
        unit_number=3,
        title="Nauka i technologia",
        grammar_points=[
            "imieslowy-zaawansowane",
            "zdania-wielokrotne",
            "mowa-zalezna-zaawansowana",
        ],
        vocabulary_set_ids=["nauka_b2", "technologia_b2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Buduje złożone konstrukcje imiesłowowe w tekstach naukowych: "
            "badania przeprowadzone w 2024 roku wykazały..., analizując dane...",
            "Łączy kilka zdań podrzędnych w spójną wypowiedź bez utraty czytelności",
            "Przekazuje wypowiedź z zachowaniem czasu, trybu i modalności: "
            "twierdził, że badanie zostało zakończone",
            "Streszcza artykuł popularnonaukowy, oddzielając tezę od dowodów",
        ],
        default_weeks=2,
        prerequisite_unit="b2-unit-2",
    ),
    CurriculumUnit(
        id="b2-unit-4",
        level="B2",
        unit_number=4,
        title="Kultura i literatura",
        grammar_points=["szyk-wyrazow", "inwersja", "elipsa"],
        vocabulary_set_ids=["literatura_b2", "kultura_b2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Świadomie zmienia szyk wyrazów dla emfazy: to właśnie wtedy "
            "zrozumiałem..., nigdy nie zapomnę...",
            "Stosuje inwersję i konstrukcje emfatyczne w wypowiedzi pisemnej",
            "Rozpoznaje elipsę w dialogu i uzupełnia pominięte elementy: "
            "Ja do kina, a ty do domu",
            "Interpretuje fragment literacki, uzasadniając odczytania cytatami",
        ],
        default_weeks=2,
        prerequisite_unit="b2-unit-3",
    ),
    CurriculumUnit(
        id="b2-unit-5",
        level="B2",
        unit_number=5,
        title="Społeczeństwo i polityka",
        grammar_points=[
            "spojniki-zaawansowane",
            "zdania-ustepstwowe",
            "przyimki-zaawansowane",
        ],
        vocabulary_set_ids=["polityka_b2", "spoleczenstwo_b2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Używa zaawansowanych spójników: o ile, podczas gdy, tymczasem, " "w związku z tym",
            "Buduje zdania ustępstwowe: chociaż, mimo że, pomimo że, nawet gdyby",
            "Stosuje przyimki w konstrukcjach abstrakcyjnych: wbrew oczekiwaniom, "
            "wobec braku danych, ze względu na sytuację",
            "Analizuje problem społeczny, przedstawiając stanowiska i ich konsekwencje",
        ],
        default_weeks=2,
        prerequisite_unit="b2-unit-4",
    ),
    CurriculumUnit(
        id="b2-unit-6",
        level="B2",
        unit_number=6,
        title="Podróże i wielokulturowość",
        grammar_points=["aspekt-niuans", "prefiksy-ruchu", "przyslowki-zaawansowane"],
        vocabulary_set_ids=["podroze_b2", "wielokulturowosc_b2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Rozróżnia niuanse aspektu w opisie czynności powtarzalnych i jednorazowych",
            "Używa czasowników ruchu z przedrostkami w narracji podróżniczej: "
            "dolecieć, objechać, przewędrować",
            "Tworzy i stopniuje przysłówki złożone: coraz częściej, najbardziej "
            "charakterystycznie",
            "Opisuje spotkanie międzykulturowe, unikając stereotypów i uproszczeń",
        ],
        default_weeks=2,
        prerequisite_unit="b2-unit-5",
    ),
    CurriculumUnit(
        id="b2-unit-7",
        level="B2",
        unit_number=7,
        title="Zdrowie i psychologia",
        grammar_points=[
            "partykuly-zaawansowane",
            "wyrazenia-przyimkowe",
            "skladnia-zlozona",
        ],
        vocabulary_set_ids=["zdrowie_b2", "psychologia_b2", "emocje_b2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Stosuje partykuły w funkcji pragmatycznej: przecież, bynajmniej, " "wręcz, niejako",
            "Używa utartych wyrażeń przyimkowych: pod wpływem stresu, w obliczu "
            "trudności, na skutek zaniedbania",
            "Buduje złożone zdania podrzędne bez błędów w zgodzie czasów",
            "Omawia zagadnienia zdrowia psychicznego z zachowaniem precyzji " "i wrażliwości",
        ],
        default_weeks=2,
        prerequisite_unit="b2-unit-6",
    ),
    CurriculumUnit(
        id="b2-unit-8",
        level="B2",
        unit_number=8,
        title="Powtórka B2",
        grammar_points=[
            "tryb-warunkowy-hipotetyczny",
            "nominalizacja",
            "strona-bierna-zaawansowana",
            "spojniki-zaawansowane",
            "zdania-ustepstwowe",
            "aspekt-niuans",
            "szyk-wyrazow",
        ],
        vocabulary_set_ids=["powtorka_b2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Tworzy spójną wypowiedź argumentacyjną z tezą, argumentami " "i kontrargumentami",
            "Stosuje konstrukcje nominalne i bierne odpowiednio do rejestru tekstu",
            "Dobiera aspekt i szyk wyrazów do zamierzonego efektu znaczeniowego",
            "Czyta tekst specjalistyczny i ocenia wiarygodność przedstawionych danych",
        ],
        default_weeks=1,
        prerequisite_unit="b2-unit-7",
    ),
]
