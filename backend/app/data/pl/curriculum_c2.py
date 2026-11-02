"""C2 curriculum units — Polish (pl-PL)."""

from __future__ import annotations

from app.data._types import CurriculumUnit

C2_UNITS: list[CurriculumUnit] = [
    CurriculumUnit(
        id="c2-unit-1",
        level="C2",
        unit_number=1,
        title="Mistrzostwo stylu",
        grammar_points=["rejestr-jezykowy", "dobor-slow", "skladnia-emfatyczna"],
        vocabulary_set_ids=["styl_c2", "rejestr_c2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Dostosowuje rejestr wypowiedzi do gatunku, odbiorcy i kontekstu "
            "bez niezamierzonych efektów",
            "Dobiera słownictwo o właściwym nacechowaniu: książkowe, neutralne, "
            "potoczne, ironiczne",
            "Buduje zdania emfatyczne i okresy retoryczne o kontrolowanym rytmie",
            "Redaguje tekst o wysokich wymaganiach stylistycznych i uzasadnia " "dokonane wybory",
        ],
        default_weeks=2,
        prerequisite_unit=None,
    ),
    CurriculumUnit(
        id="c2-unit-2",
        level="C2",
        unit_number=2,
        title="Idiomy i frazeologia",
        grammar_points=["frazeologia", "przyslowia", "wyrazenia-utarte"],
        vocabulary_set_ids=["frazeologia_c2", "przyslowia_c2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Używa frazeologizmów z poprawną łączliwością i bez kalk z innych języków",
            "Rozpoznaje przysłowia i ich znaczenie pragmatyczne w kontekście",
            "Stosuje utarte wyrażenia właściwe dla sytuacji oficjalnych i medialnych",
            "Wyjaśnia znaczenie idiomu i jego ograniczenia użycia",
        ],
        default_weeks=2,
        prerequisite_unit="c2-unit-1",
    ),
    CurriculumUnit(
        id="c2-unit-3",
        level="C2",
        unit_number=3,
        title="Niuanse gramatyczne",
        grammar_points=["aspekt-mistrzostwo", "tryby-mowione", "formy-archaiczne"],
        vocabulary_set_ids=["gramatyka_c2", "archaizmy_c2", "niuanse_c2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Kontroluje aspekt w narracji o dużej gęstości zdarzeń i nawyków",
            "Rozpoznaje i stosuje formy trybu warunkowego oraz rozkazującego "
            "w funkcjach modalnych",
            "Identyfikuje formy archaiczne i książkowe oraz ocenia ich użyteczność " "współcześnie",
            "Koryguje subtelne błędy gramatyczne w cudzym tekście i uzasadnia poprawki",
        ],
        default_weeks=2,
        prerequisite_unit="c2-unit-2",
    ),
    CurriculumUnit(
        id="c2-unit-4",
        level="C2",
        unit_number=4,
        title="Tekst specjalistyczny",
        grammar_points=["jezyk-prawny", "jezyk-naukowy", "definicje-precyzja"],
        vocabulary_set_ids=["prawo_c2", "nauka_c2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Czyta i streszcza tekst prawny, zachowując warunki i zakresy obowiązywania",
            "Stosuje konwencje języka naukowego: hedging, cytowanie, przypisy",
            "Formułuje definicje precyzyjne i odróżnia je od opisu oraz przykładu",
            "Redaguje ekspertyzę z zachowaniem struktury i zastrzeżeń",
        ],
        default_weeks=2,
        prerequisite_unit="c2-unit-3",
    ),
    CurriculumUnit(
        id="c2-unit-5",
        level="C2",
        unit_number=5,
        title="Perswazja i retoryka",
        grammar_points=["retoryka", "argumentacja-zaawansowana", "manipulacja-jezykowa"],
        vocabulary_set_ids=["retoryka_c2", "perswazja_c2", "media_c2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Buduje wystąpienie perswazyjne z wyraźną tezą, argumentacją i puentą",
            "Ocenia siłę argumentów i rozpoznaje błędy logiczne",
            "Identyfikuje chwyty manipulacyjne w tekście i mowie, nazywając mechanizm",
            "Debatuje, odpierając zarzuty i zachowując spójność stanowiska",
        ],
        default_weeks=2,
        prerequisite_unit="c2-unit-4",
    ),
    CurriculumUnit(
        id="c2-unit-6",
        level="C2",
        unit_number=6,
        title="Kultura i przekład",
        grammar_points=[
            "trudnosci-przekladu",
            "kalki-jezykowe",
            "ekwiwalencja",
        ],
        vocabulary_set_ids=["przeklad_c2", "kultura_c2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Rozpoznaje trudności przekładowe: grę słów, rejestr, konotacje "
            "i elementy kulturowe",
            "Wykrywa kalki językowe i proponuje naturalne odpowiedniki",
            "Ocenia ekwiwalencję przekładu na poziomie znaczenia, stylu i funkcji",
            "Tłumaczy krótki tekst, uzasadniając wybory translatorskie",
        ],
        default_weeks=2,
        prerequisite_unit="c2-unit-5",
    ),
    CurriculumUnit(
        id="c2-unit-7",
        level="C2",
        unit_number=7,
        title="Język mówiony i regionalizmy",
        grammar_points=["regionalizmy", "jezyk-potoczny", "intonacja-znaczenie"],
        vocabulary_set_ids=["regionalizmy_c2", "mowa-potoczna_c2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Rozpoznaje regionalizmy i odróżnia je od form ogólnopolskich",
            "Stosuje cechy języka potocznego w odpowiednim kontekście i rejestrze",
            "Interpretuje intonację i akcent zdaniowy jako nośniki znaczenia "
            "oraz postawy mówiącego",
            "Analizuje nagranie mowy naturalnej i opisuje użyte środki językowe",
        ],
        default_weeks=2,
        prerequisite_unit="c2-unit-6",
    ),
    CurriculumUnit(
        id="c2-unit-8",
        level="C2",
        unit_number=8,
        title="Powtórka C2",
        grammar_points=[
            "rejestr-jezykowy",
            "frazeologia",
            "aspekt-mistrzostwo",
            "jezyk-prawny",
            "retoryka",
            "trudnosci-przekladu",
            "regionalizmy",
        ],
        vocabulary_set_ids=["powtorka_c2"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Produkuje teksty i wystąpienia o wysokiej precyzji, spójności i trafności "
            "stylistycznej",
            "Stosuje frazeologię i niuanse gramatyczne świadomie i adekwatnie",
            "Referuje, ocenia i przekłada teksty o złożonej strukturze",
            "Identyfikuje i koryguje subtelne błędy językowe, uzasadniając decyzje",
        ],
        default_weeks=1,
        prerequisite_unit="c2-unit-7",
    ),
]
