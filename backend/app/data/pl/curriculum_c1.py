"""C1 curriculum units — Polish (pl-PL)."""

from __future__ import annotations

from app.data._types import CurriculumUnit

C1_UNITS: list[CurriculumUnit] = [
    CurriculumUnit(
        id="c1-unit-1",
        level="C1",
        unit_number=1,
        title="Dyskurs publiczny",
        grammar_points=[
            "styl-formalny",
            "nominalizacja-zaawansowana",
            "konstrukcje-imienne",
        ],
        vocabulary_set_ids=["dyskurs_c1", "media_c1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Dostosowuje rejestr wypowiedzi publicznej do odbiorcy i celu: "
            "przemówienie, artykuł, komentarz",
            "Przekształca rozbudowane zdania w konstrukcje imienne bez utraty "
            "znaczenia i precyzji",
            "Stosuje konstrukcje imienne właściwe dla języka administracji " "i publicystyki",
            "Analizuje tekst publicystyczny, wskazując środki perswazji i ich funkcję",
        ],
        default_weeks=2,
        prerequisite_unit=None,
    ),
    CurriculumUnit(
        id="c1-unit-2",
        level="C1",
        unit_number=2,
        title="Literatura i styl",
        grammar_points=[
            "srodki-stylistyczne",
            "skladnia-retoryczna",
            "metafora-jezykowa",
        ],
        vocabulary_set_ids=["literatura_c1", "styl_c1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Rozpoznaje i nazywa środki stylistyczne: metaforę, metonimię, " "hiperbolę, anaforę",
            "Buduje zdania o spójności retorycznej: paralelizm, wyliczenie, " "pytanie retoryczne",
            "Odróżnia metaforę utartą od świeżej i ocenia jej skuteczność",
            "Pisze interpretację tekstu literackiego z jasną tezą i cytatami",
        ],
        default_weeks=2,
        prerequisite_unit="c1-unit-1",
    ),
    CurriculumUnit(
        id="c1-unit-3",
        level="C1",
        unit_number=3,
        title="Nauka i specjalizacja",
        grammar_points=[
            "terminologia",
            "definiowanie",
            "przyimki-specjalistyczne",
        ],
        vocabulary_set_ids=["nauka_c1", "specjalizacja_c1", "terminologia_c1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Definiuje pojęcia specjalistyczne, podając zakres i kryteria",
            "Stosuje precyzyjne przyimki w języku nauki: w zakresie, "
            "w odniesieniu do, na podstawie",
            "Odróżnia terminy bliskoznaczne i uzasadnia wybór w kontekście",
            "Streszcza artykuł naukowy, zachowując hierarchię twierdzeń i zastrzeżeń",
        ],
        default_weeks=2,
        prerequisite_unit="c1-unit-2",
    ),
    CurriculumUnit(
        id="c1-unit-4",
        level="C1",
        unit_number=4,
        title="Emocje i niuanse",
        grammar_points=["aspekt-niuanse", "partykuly-niuans", "zaimki-nieokreslone"],
        vocabulary_set_ids=["emocje_c1", "niuanse_c1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Wykorzystuje niuanse aspektu do różnicowania intencji i przebiegu " "czynności",
            "Używa partykuł i wykładników modalności do precyzyjnego stopniowania " "twierdzeń",
            "Stosuje zaimki nieokreślone i przeczące: cokolwiek, byle kto, " "nikt z nas",
            "Wyraża stany emocjonalne z odcieniami intensywności i rejestru",
        ],
        default_weeks=2,
        prerequisite_unit="c1-unit-3",
    ),
    CurriculumUnit(
        id="c1-unit-5",
        level="C1",
        unit_number=5,
        title="Społeczeństwo i etyka",
        grammar_points=[
            "zdania-warunkowe-mieszane",
            "mowa-zalezna-styl",
            "strona-bierna-styl",
        ],
        vocabulary_set_ids=["etyka_c1", "spoleczenstwo_c1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Buduje mieszane zdania warunkowe w rozważaniach etycznych: "
            "gdybyśmy wtedy zdecydowali inaczej, dziś...",
            "Wykorzystuje mowę zależną do referowania stanowisk bez zniekształceń",
            "Stosuje stronę bierną świadomie, aby ukryć lub wyeksponować sprawcę",
            "Argumentuje w dylemacie etycznym, rozróżniając opis, ocenę i normę",
        ],
        default_weeks=2,
        prerequisite_unit="c1-unit-4",
    ),
    CurriculumUnit(
        id="c1-unit-6",
        level="C1",
        unit_number=6,
        title="Praca i negocjacje",
        grammar_points=[
            "jezyk-grzecznosci",
            "tryb-rozka-zaawansowany",
            "konstrukcje-modalne",
        ],
        vocabulary_set_ids=["negocjacje_c1", "praca_c1", "grzecznosc_c1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Stosuje formy grzecznościowe właściwe dla relacji służbowych " "i negocjacji",
            "Używa trybu rozkazującego w funkcji perswazyjnej i dyplomatycznej: "
            "proszę rozważyć, niech pan zauważy",
            "Buduje konstrukcje modalne o różnej sile zobowiązania: wypada, "
            "należałoby, jesteśmy zobowiązani",
            "Prowadzi negocjacje, formułując ustępstwa i warunki bez utraty " "precyzji",
        ],
        default_weeks=2,
        prerequisite_unit="c1-unit-5",
    ),
    CurriculumUnit(
        id="c1-unit-7",
        level="C1",
        unit_number=7,
        title="Kultura i tożsamość",
        grammar_points=["zwroty-idiomatyczne", "kolokacje", "slowotworstwo"],
        vocabulary_set_ids=["tozsamosc_c1", "kultura_c1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Używa związków frazeologicznych adekwatnie do kontekstu i rejestru",
            "Dobiera naturalne kolokacje rzeczownikowo-czasownikowe: "
            "podejmować decyzję, odgrywać rolę",
            "Tworzy wyrazy pochodne z typowymi formantami i rozumie ich odcienie",
            "Omawia zagadnienia tożsamości kulturowej, unikając uproszczeń",
        ],
        default_weeks=2,
        prerequisite_unit="c1-unit-6",
    ),
    CurriculumUnit(
        id="c1-unit-8",
        level="C1",
        unit_number=8,
        title="Powtórka C1",
        grammar_points=[
            "styl-formalny",
            "srodki-stylistyczne",
            "terminologia",
            "aspekt-niuanse",
            "zdania-warunkowe-mieszane",
            "jezyk-grzecznosci",
            "zwroty-idiomatyczne",
        ],
        vocabulary_set_ids=["powtorka_c1"],
        lesson_types=["grammar", "vocabulary", "listening", "reading", "writing", "review"],
        competency_checklist=[
            "Tworzy tekst użytkowy o wysokim stopniu formalności, spójny " "i precyzyjny",
            "Dobiera środki stylistyczne i leksykę do celu komunikacyjnego",
            "Referuje i ocenia cudze stanowiska, zachowując ich pierwotny sens",
            "Czyta tekst o złożonej strukturze i rekonstruuje jego argumentację",
        ],
        default_weeks=1,
        prerequisite_unit="c1-unit-7",
    ),
]
