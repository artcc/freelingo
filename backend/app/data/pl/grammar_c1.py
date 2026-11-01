"""Polish grammar topics — C1."""

from app.data._types import GrammarExample, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="nominalizacja",
        title="Nominalizacja",
        level="C1",
        category="Gramatyka",
        summary="Nominalizacja przedstawia czynność lub cechę jako rzeczownik.",
        explanation="Nominalizacje są częste w tekstach akademickich i urzędowych. Pozwalają kondensować informacje, ale nadmierne ich użycie zaciemnia relacje między wykonawcą, czynnością i skutkiem. Czasownik bywa czytelniejszym wyborem.",
        structure="analizować → analiza; wdrożyć → wdrożenie",
        rules=[
            "Używaj nominalizacji, gdy pomaga ona nazwać proces lub pojęcie.",
            "Wskazuj wykonawcę działania, gdy jest ważny.",
            "Zastępuj ciężką konstrukcję rzeczownikową czasownikiem, gdy poprawia to jasność.",
        ],
        examples=[
            GrammarExample(
                text="Analiza danych potwierdziła hipotezę.",
                translation=None,
                note="Proces jako nazwa pojęcia.",
            ),
            GrammarExample(
                text="Zespół wdrożył nowe rozwiązanie.",
                translation=None,
                note="Czasownik wyraźniej wskazuje wykonawcę.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="modalnosc",
        title="Modalność i stopień pewności",
        level="C1",
        category="Gramatyka",
        summary="Modalność wyraża stosunek mówiącego do pewności, obowiązku lub możliwości.",
        explanation="Modalność można wyrazić czasownikami, przysłówkami, trybem warunkowym i konstrukcją zdania. Wypowiedź może przedstawiać treść jako fakt, przypuszczenie, ocenę lub zalecenie. Dobór środka wpływa na siłę twierdzenia.",
        structure="możliwe, że; prawdopodobnie; należy; musiałby",
        rules=[
            "Odróżniaj pewność od prawdopodobieństwa.",
            "Nie wzmacniaj wniosku ponad dostępne przesłanki.",
            "Zaznaczaj, czy wypowiedź jest oceną, czy opisem.",
        ],
        examples=[
            GrammarExample(
                text="Wynik może wskazywać na zmianę trendu.",
                translation=None,
                note="Ostrożny wniosek.",
            ),
            GrammarExample(
                text="Zgodnie z regulaminem należy złożyć wniosek.",
                translation=None,
                note="Obowiązek.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="konstrukcje-bezosobowe",
        title="Konstrukcje bezosobowe",
        level="C1",
        category="Gramatyka",
        summary="Konstrukcje bezosobowe pozwalają opisać działanie bez wskazania wykonawcy.",
        explanation="Polszczyzna wykorzystuje formy zakończone na -no i -to, konstrukcje z się oraz bezosobowe formy modalne. Wybór zależy od aspektu, czasu i tego, czy wykonawca jest znany lub istotny.",
        structure="ustalono wyniki; mówi się o zmianach; należy uwzględnić",
        rules=[
            "Dobieraj aspekt formy -no/-to do zakończonego działania.",
            "Używaj się do ogólnych obserwacji, a nie do ukrywania ważnego wykonawcy.",
            "Wskaż wykonawcę, jeśli jest istotny dla odpowiedzialności lub interpretacji.",
        ],
        examples=[
            GrammarExample(
                text="W raporcie przedstawiono wyniki ankiety.",
                translation=None,
                note="Forma bezosobowa z -no.",
            ),
            GrammarExample(
                text="Należy uwzględnić ograniczenia metody.",
                translation=None,
                note="Bezosobowa forma modalna.",
            ),
        ],
        common_mistakes=[
        ],
    ),
]
