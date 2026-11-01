"""Polish grammar topics — B2."""

from app.data._types import GrammarExample, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="strona-bierna",
        title="Strona bierna",
        level="B2",
        category="Gramatyka",
        summary="Strona bierna eksponuje obiekt działania zamiast jego wykonawcy.",
        explanation="Stronę bierną tworzy się z imiesłowu biernego i odpowiedniej formy być lub zostać. Imiesłów uzgadnia się z podmiotem. Strona bierna bywa przydatna w tekstach formalnych, lecz nie powinna zastępować naturalnych konstrukcji czynnych.",
        structure="został opublikowany; jest przygotowywana; zostały omówione",
        rules=[
            "Dobierz rodzaj i liczbę imiesłowu do podmiotu.",
            "Używaj być dla stanu lub procesu, a zostać dla zdarzenia.",
            "Wskazuj wykonawcę przez przez tylko wtedy, gdy jest istotny.",
        ],
        examples=[
            GrammarExample(
                text="Raport został opublikowany w poniedziałek.",
                translation=None,
                note="Zakończone zdarzenie.",
            ),
            GrammarExample(
                text="Nowa ustawa jest właśnie omawiana.",
                translation=None,
                note="Trwający proces.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="imieslowy",
        title="Imiesłowy",
        level="B2",
        category="Gramatyka",
        summary="Imiesłowy skracają zdania i opisują czynność lub cechę.",
        explanation="Imiesłów przysłówkowy współczesny opisuje czynność równoczesną, a uprzedni — wcześniejszą. Podmiot obu czynności powinien być ten sam. Imiesłów przymiotnikowy uzgadnia się z określanym rzeczownikiem.",
        structure="czytając, przeczytawszy; czytający, przeczytany",
        rules=[
            "Używaj imiesłowu współczesnego dla czynności równoczesnych.",
            "Nie zmieniaj podmiotu między imiesłowem a orzeczeniem.",
            "Oddzielaj imiesłowowy równoważnik zdania przecinkiem.",
        ],
        examples=[
            GrammarExample(
                text="Wracając z pracy, spotkałam sąsiada.",
                translation=None,
                note="Ta sama osoba wraca i spotyka.",
            ),
            GrammarExample(
                text="Przeczytawszy umowę, podpisał ją.",
                translation=None,
                note="Czynność wcześniejsza.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="mowa-zalezna",
        title="Mowa zależna",
        level="B2",
        category="Gramatyka",
        summary="Mowa zależna przekazuje cudzą wypowiedź bez cytowania jej dosłownie.",
        explanation="Wypowiedź można wprowadzić czasownikami mówić, twierdzić, zapytać lub oznajmić. Dobór spójnika zależy od rodzaju treści: że dla stwierdzenia, czy dla pytania rozstrzygającego, a zaimek pytajny dla pytania szczegółowego.",
        structure="powiedział, że…; zapytała, czy…; chciał wiedzieć, kiedy…",
        rules=[
            "Zachowuj sens i stopień pewności oryginalnej wypowiedzi.",
            "Dopasuj zaimek i określenie czasu do nowej perspektywy.",
            "Nie stawiaj znaku zapytania po pośrednim pytaniu.",
        ],
        examples=[
            GrammarExample(
                text="Marta powiedziała, że wróci po południu.",
                translation=None,
                note="Relacja stwierdzenia.",
            ),
            GrammarExample(
                text="Zapytał, czy mamy już wyniki.",
                translation=None,
                note="Relacja pytania rozstrzygającego.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="skladnia-zlozona",
        title="Składnia zdań złożonych",
        level="B2",
        category="Gramatyka",
        summary="Zdania złożone porządkują kilka relacji w jednej wypowiedzi.",
        explanation="Wypowiedzenie może łączyć zdania współrzędne lub podrzędne. Spójnik i szyk powinny ujawniać hierarchię informacji. Przecinki oddzielają zdania składowe zgodnie z ich funkcją.",
        structure="zdanie nadrzędne, ponieważ zdanie podrzędne",
        rules=[
            "Rozpoznaj zdanie nadrzędne i podrzędne.",
            "Stosuj przecinek między zdaniami składowymi.",
            "Nie przeciążaj jednego zdania wieloma poziomami zależności.",
        ],
        examples=[
            GrammarExample(
                text="Choć projekt był trudny, zespół ukończył go przed terminem.",
                translation=None,
                note="Zdanie przyzwalające.",
            ),
            GrammarExample(
                text="Wiem, że raport, który otrzymaliśmy, wymaga poprawek.",
                translation=None,
                note="Zdanie podrzędne wtrącone.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="styl-formalny",
        title="Styl formalny",
        level="B2",
        category="Gramatyka",
        summary="Styl formalny dopasowuje słownictwo i formę do sytuacji zawodowej lub urzędowej.",
        explanation="Formalność budują precyzyjne sformułowania, pełne formy grzecznościowe i uporządkowana struktura. Sama długość zdania nie nadaje mu formalnego charakteru. Należy unikać potocznych skrótów i nieuzasadnionej pompatyczności.",
        structure="Szanowna Pani; uprzejmie proszę; z poważaniem",
        rules=[
            "Dopasuj formę grzecznościową do odbiorcy.",
            "Stosuj precyzyjne słownictwo zamiast potocznych ogólników.",
            "Zachowuj rzeczowy ton.",
        ],
        examples=[
            GrammarExample(
                text="Zwracam się z uprzejmą prośbą o przesłanie dokumentu.",
                translation=None,
                note="Neutralna prośba formalna.",
            ),
            GrammarExample(
                text="W załączeniu przekazuję wymagane zestawienie.",
                translation=None,
                note="Styl korespondencji zawodowej.",
            ),
        ],
        common_mistakes=[
        ],
    ),
]
