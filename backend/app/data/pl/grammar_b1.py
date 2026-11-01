"""Polish grammar topics — B1."""

from app.data._types import GrammarExample, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="aspekt-czasownika",
        title="Aspekt czasownika",
        level="B1",
        category="Gramatyka",
        summary="Aspekt pokazuje, czy czynność jest przedstawiona jako proces, czy jako osiągnięty rezultat.",
        explanation="Czasowniki niedokonane ujmują czynność jako trwającą, powtarzaną lub bez wskazanego końca. Czasowniki dokonane przedstawiają ją jako całość lub rezultat. Aspekt nie jest tym samym co czas gramatyczny.",
        structure="czytać — przeczytać; robić — zrobić",
        rules=[
            "Wybieraj niedokonany dla procesu lub powtarzalności.",
            "Wybieraj dokonany dla pojedynczego rezultatu.",
            "Nie używaj form dokonanych jako czasu teraźniejszego.",
        ],
        examples=[
            GrammarExample(
                text="Czytałam raport, gdy zadzwonił telefon.",
                translation=None,
                note="Proces w tle.",
            ),
            GrammarExample(
                text="Przeczytałam raport przed spotkaniem.",
                translation=None,
                note="Zakończony rezultat.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="zdania-wzgledne",
        title="Zdania względne",
        level="B1",
        category="Gramatyka",
        summary="Zdanie względne doprecyzowuje rzeczownik i łączy informacje.",
        explanation="Zdanie względne najczęściej rozpoczyna się od który, która, które albo jaki. Zaimek uzgadnia rodzaj i liczbę z określanym rzeczownikiem, a jego przypadek zależy od funkcji wewnątrz zdania podrzędnego.",
        structure="rzeczownik + który/która/które + zdanie",
        rules=[
            "Uzgadniaj rodzaj i liczbę zaimka z określanym rzeczownikiem.",
            "Dobieraj przypadek zaimka do jego funkcji w zdaniu podrzędnym.",
            "Oddzielaj zdanie względne przecinkami.",
        ],
        examples=[
            GrammarExample(
                text="To jest książka, którą poleciła mi Marta.",
                translation=None,
                note="Biernik wynika z czasownika polecić.",
            ),
            GrammarExample(
                text="Spotkałem autora, o którym rozmawialiśmy.",
                translation=None,
                note="Przypadek po przyimku o.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="spojniki",
        title="Spójniki i relacje logiczne",
        level="B1",
        category="Gramatyka",
        summary="Spójniki łączą zdania i pokazują relacje między ich treścią.",
        explanation="Spójniki takie jak ponieważ, chociaż, dlatego że i mimo że wprowadzają określone relacje znaczeniowe. Szyk w zdaniu podrzędnym pozostaje naturalny dla polszczyzny, a granicę zdań zaznacza przecinek.",
        structure="teza, ponieważ uzasadnienie; chociaż przeszkoda, skutek",
        rules=[
            "Stawiaj przecinek przed zdaniem podrzędnym.",
            "Dobieraj spójnik do relacji przyczynowej, przeciwstawnej lub warunkowej.",
            "Unikaj łączenia kilku spójników o tej samej funkcji.",
        ],
        examples=[
            GrammarExample(
                text="Zostałem w domu, ponieważ źle się czułem.",
                translation=None,
                note="Przyczyna.",
            ),
            GrammarExample(
                text="Chociaż padało, poszliśmy na spacer.",
                translation=None,
                note="Ustępstwo.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="tryb-warunkowy",
        title="Tryb warunkowy",
        level="B1",
        category="Gramatyka",
        summary="Tryb warunkowy wyraża przypuszczenie, życzenie, możliwość lub uprzejmą prośbę.",
        explanation="Formę tworzy się zwykle z przeszłej formy czasownika i ruchomej cząstki by. Cząstka może łączyć się z osobowymi końcówkami albo wystąpić po zaimku. W zdaniu podrzędnym często pojawia się gdyby.",
        structure="zrobiłbym, zrobiłabyś; gdybym wiedział, zadzwoniłbym",
        rules=[
            "Uzgadniaj formę z osobą i rodzajem.",
            "Używaj gdyby do hipotetycznego warunku.",
            "Stosuj tryb warunkowy do uprzejmych próśb.",
        ],
        examples=[
            GrammarExample(
                text="Czy mogłaby pani powtórzyć?",
                translation=None,
                note="Uprzejma prośba.",
            ),
            GrammarExample(
                text="Gdybym miał więcej czasu, nauczyłbym się tego.",
                translation=None,
                note="Warunek hipotetyczny.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="rekcja-czasownikow",
        title="Rekcja czasowników",
        level="B1",
        category="Gramatyka",
        summary="Rekcja określa przypadek lub przyimek wymagany przez czasownik.",
        explanation="Wiele polskich czasowników łączy się z ustalonym przypadkiem albo przyimkiem. Warto zapamiętywać czasownik razem z jego typowym dopełnieniem. Zmiana przypadku może zmienić znaczenie całej wypowiedzi.",
        structure="szukać + dopełniacz; pomagać + celownik; interesować się + narzędnik",
        rules=[
            "Ucz się czasownika razem z wymaganym przypadkiem.",
            "Nie przenoś rekcji z innego języka.",
            "Sprawdzaj, czy wybrany przyimek nie zmienia znaczenia.",
        ],
        examples=[
            GrammarExample(
                text="Szukam spokojnego miejsca do pracy.",
                translation=None,
                note="Dopełniacz po szukać.",
            ),
            GrammarExample(
                text="Pomagam nowemu koledze.",
                translation=None,
                note="Celownik po pomagać.",
            ),
        ],
        common_mistakes=[
        ],
    ),
]
