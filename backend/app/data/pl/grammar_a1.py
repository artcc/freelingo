"""Polish grammar topics — A1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="zaimki-osobowe",
        title="Zaimki osobowe",
        level="A1",
        category="Gramatyka",
        summary="Zaimki wskazują wykonawcę czynności, a ich forma zależy od osoby i liczby.",
        explanation="W języku polskim zaimek osobowy często można pominąć, ponieważ końcówka czasownika wskazuje osobę. Zaimki pojawiają się dla podkreślenia, kontrastu lub uniknięcia niejasności. Formy pan i pani wyrażają grzeczność i łączą się z czasownikiem w trzeciej osobie.",
        structure="ja, ty, on/ona/ono; my, wy, oni/one; pan, pani, państwo",
        rules=[
            "Pomijaj zaimek, gdy osoba jest jasna z formy czasownika.",
            "Używaj pan/pani w uprzejmych kontaktach.",
            "Dobieraj oni do grup mieszanych lub męskoosobowych, a one do pozostałych.",
        ],
        examples=[
            GrammarExample(
                text="Jestem studentką.",
                translation=None,
                note="Podmiot wynika z końcówki czasownika.",
            ),
            GrammarExample(
                text="Czy pani mieszka tutaj?",
                translation=None,
                note="Uprzejma forma z czasownikiem w trzeciej osobie.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ty jest studentem.",
                correct="Ty jesteś studentem.",
                note="W drugiej osobie liczby pojedynczej czasownik mieć formę jesteś.",
            ),
        ],
    ),
    GrammarTopic(
        slug="byc",
        title="Czasownik być",
        level="A1",
        category="Gramatyka",
        summary="Być łączy osobę z jej cechą, rolą lub miejscem.",
        explanation="Czasownik być odmienia się nieregularnie. W czasie teraźniejszym służy do opisu osób, zawodów, cech oraz lokalizacji. W zdaniu z orzecznikiem rzeczownik i przymiotnik dopasowują się do rodzaju podmiotu.",
        structure="jestem, jesteś, jest; jesteśmy, jesteście, są",
        rules=[
            "Używaj jestem, jesteś i jest w liczbie pojedynczej.",
            "Po przeczeniu dodaj nie przed odmienioną formą.",
            "W czasie teraźniejszym nie pomijaj czasownika być.",
        ],
        examples=[
            GrammarExample(
                text="Jestem z Gdańska.",
                translation=None,
                note="Pochodzenie.",
            ),
            GrammarExample(
                text="Oni są bardzo mili.",
                translation=None,
                note="Zgodność orzecznika z grupą.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ja studentem.",
                correct="Jestem studentem.",
                note="W zdaniu teraźniejszym potrzebny jest czasownik być.",
            ),
        ],
    ),
    GrammarTopic(
        slug="czas-terazniejszy",
        title="Czas teraźniejszy",
        level="A1",
        category="Gramatyka",
        summary="Czas teraźniejszy opisuje czynności obecne i regularne.",
        explanation="Czasowniki odmieniają się przez osoby. Bezokoliczniki najczęściej kończą się na -ć lub -c, a wzory odmiany zależą od grupy koniugacyjnej. Wypowiedź o zwyczaju często zawiera określenie częstotliwości.",
        structure="czytam, czytasz, czyta; czytamy, czytacie, czytają",
        rules=[
            "Dopasuj końcówkę czasownika do osoby.",
            "Stosuj czas teraźniejszy do rutyny i faktów.",
            "Nie dodawaj zaimka, jeśli końcówka wystarcza.",
        ],
        examples=[
            GrammarExample(
                text="Codziennie zaczynam pracę o ósmej.",
                translation=None,
                note="Czynność regularna.",
            ),
            GrammarExample(
                text="Czytamy polskie wiadomości.",
                translation=None,
                note="Pierwsza osoba liczby mnogiej.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ona czytam książkę.",
                correct="Ona czyta książkę.",
                note="Końcówka czasownika musi odpowiadać osobie.",
            ),
        ],
    ),
    GrammarTopic(
        slug="pytania-i-przeczenia",
        title="Pytania i przeczenia",
        level="A1",
        category="Gramatyka",
        summary="Pytania i przeczenia tworzy się bez dodatkowego czasownika posiłkowego.",
        explanation="Pytanie ogólne ma zwykle szyk twierdzący i intonację pytającą; można je rozpocząć od czy. Pytanie szczegółowe zawiera zaimek lub przysłówek pytajny. Przeczenie tworzy się przez nie przed czasownikiem.",
        structure="Czy + podmiot + czasownik?; nie + czasownik",
        rules=[
            "Używaj czy w pytaniach wymagających odpowiedzi tak lub nie.",
            "Umieszczaj wyraz pytajny na początku pytania.",
            "Pisz nie osobno od czasownika.",
        ],
        examples=[
            GrammarExample(
                text="Czy mieszkasz w Warszawie?",
                translation=None,
                note="Pytanie ogólne.",
            ),
            GrammarExample(
                text="Dlaczego nie pracujesz dzisiaj?",
                translation=None,
                note="Pytanie szczegółowe i przeczenie.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="mianownik",
        title="Mianownik",
        level="A1",
        category="Gramatyka",
        summary="Mianownik nazywa wykonawcę czynności i odpowiada na pytania kto? oraz co?.",
        explanation="Mianownik jest podstawową formą rzeczownika, używaną między innymi jako podmiot zdania. Przymiotnik i zaimek wskazujący uzgadniają z rzeczownikiem rodzaj i liczbę.",
        structure="kto? co?; nowy dom, nowa ulica, nowe miasto",
        rules=[
            "Używaj mianownika dla podmiotu.",
            "Uzgadniaj przymiotnik z rodzajem i liczbą rzeczownika.",
            "Rozpoznawaj rodzaj rzeczownika na podstawie jego formy i kontekstu.",
        ],
        examples=[
            GrammarExample(
                text="Nowy sąsiad pracuje w szkole.",
                translation=None,
                note="Rzeczownik jest podmiotem.",
            ),
            GrammarExample(
                text="Te książki są ciekawe.",
                translation=None,
                note="Zgodność liczby i rodzaju.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="biernik",
        title="Biernik",
        level="A1",
        category="Gramatyka",
        summary="Biernik najczęściej wskazuje bezpośredni obiekt czynności.",
        explanation="Biernik odpowiada na pytania kogo? oraz co? po czasownikach przechodnich. W liczbie pojedynczej rodzaj męski często odróżnia biernik od mianownika, a rzeczowniki żeńskie i nijakie mają inne charakterystyczne końcówki.",
        structure="widzę kogo? co?; mam nową książkę, kupuję bilet",
        rules=[
            "Stosuj biernik po czasownikach takich jak mieć, widzieć i kupować.",
            "Uwzględniaj rodzaj rzeczownika przy wyborze końcówki.",
            "Po przeczeniu czasownika przechodniego często pojawia się dopełniacz.",
        ],
        examples=[
            GrammarExample(
                text="Czytam interesującą powieść.",
                translation=None,
                note="Bezpośredni obiekt.",
            ),
            GrammarExample(
                text="Kupuję świeże pieczywo.",
                translation=None,
                note="Biernik rodzaju nijakiego.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="liczebniki-i-data",
        title="Liczebniki, godziny i daty",
        level="A1",
        category="Gramatyka",
        summary="Liczebniki pozwalają podać ilość, godzinę i datę.",
        explanation="Liczebniki główne łączą się z rzeczownikami według reguł rodzaju i przypadka. Godzinę podaje się konstrukcją jest godzina lub są godziny, a datę najczęściej przez liczebnik porządkowy i nazwę miesiąca w dopełniaczu.",
        structure="dwa bilety; jest godzina ósma; 3 maja",
        rules=[
            "Uzgadniaj liczebnik dwa z rodzajem rzeczownika.",
            "Przy pełnej dacie używaj nazwy miesiąca w dopełniaczu.",
            "Odróżniaj godzinę od liczby minut.",
        ],
        examples=[
            GrammarExample(
                text="Spotkanie jest 12 czerwca.",
                translation=None,
                note="Nazwa miesiąca w dopełniaczu.",
            ),
            GrammarExample(
                text="Pociąg odjeżdża o ósmej.",
                translation=None,
                note="Godzina po przyimku o.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="przymiotniki-i-zgodnosc",
        title="Przymiotniki i zgodność",
        level="A1",
        category="Gramatyka",
        summary="Przymiotnik dopasowuje formę do rodzaju, liczby i przypadka rzeczownika.",
        explanation="Przymiotniki w rodzaju męskim, żeńskim i nijakim mają różne końcówki w mianowniku. W zdaniu przymiotnik uzgadnia się z rzeczownikiem także w liczbie mnogiej i przypadkach, które uczeń poznaje stopniowo.",
        structure="nowy dom; nowa książka; nowe okno; nowi sąsiedzi",
        rules=[
            "Rozpoznaj rodzaj i liczbę rzeczownika.",
            "Uzgodnij końcówkę przymiotnika z określanym rzeczownikiem.",
            "Nie zakładaj, że wszystkie rzeczowniki zakończone na spółgłoskę są rodzaju męskiego.",
        ],
        examples=[
            GrammarExample(
                text="Mam nową torbę.",
                translation=None,
                note="Przymiotnik i rzeczownik są rodzaju żeńskiego.",
            ),
            GrammarExample(
                text="To są dobrzy nauczyciele.",
                translation=None,
                note="Forma męskoosobowa w liczbie mnogiej.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="nowy książka",
                correct="nowa książka",
                note="Przymiotnik uzgadnia się z żeńskim rzeczownikiem.",
            ),
        ],
    ),
    GrammarTopic(
        slug="liczba-mnoga",
        title="Liczba mnoga rzeczowników",
        level="A1",
        category="Gramatyka",
        summary="Liczba mnoga rzeczowników zależy od rodzaju i wzoru odmiany.",
        explanation="Polskie rzeczowniki tworzą liczbę mnogą na różne sposoby. W mianowniku rozróżnia się między innymi formy męskoosobowe i niemęskoosobowe, co wpływa również na zgodność przymiotników i czasowników.",
        structure="student — studenci; książka — książki; okno — okna",
        rules=[
            "Ucz się liczby mnogiej razem z rzeczownikiem.",
            "Stosuj formy męskoosobowe dla grup ludzi zgodnie z normą.",
            "Uzgadniaj orzeczenie z rodzajem grupy.",
        ],
        examples=[
            GrammarExample(
                text="Studenci są gotowi.",
                translation=None,
                note="Grupa męskoosobowa.",
            ),
            GrammarExample(
                text="Książki leżą na stole.",
                translation=None,
                note="Rzeczownik niemęskoosobowy.",
            ),
        ],
        common_mistakes=[
        ],
    ),
]
