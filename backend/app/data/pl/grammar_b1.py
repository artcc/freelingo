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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
    ),
    GrammarTopic(
        slug="rekcja-przymiotnikow",
        title="Rekcja przymiotników",
        level="B1",
        category="Gramatyka",
        summary="Niektóre przymiotniki wymagają określonego przypadku lub przyimka.",
        explanation="Przymiotnik może łączyć się z rzeczownikiem w dopełniaczu, celowniku, narzędniku albo z ustalonym przyimkiem. Tę zależność najlepiej zapamiętywać jako część całego wyrażenia.",
        structure="pewny + dopełniacz; podobny do + dopełniacz; zainteresowany + narzędnik",
        rules=[
            "Sprawdzaj przypadek wymagany przez przymiotnik.",
            "Zapamiętuj przyimek razem z określanym wyrazem.",
            "Nie przenoś połączeń z innego języka.",
        ],
        examples=[
            GrammarExample(text="Jestem pewna tej decyzji.", note="Dopełniacz po pewna."),
            GrammarExample(
                text="Ten projekt jest podobny do poprzedniego.", note="Przyimek do z dopełniaczem."
            ),
        ],
    ),
    GrammarTopic(
        slug="sie-konstrukcje",
        title="Konstrukcje z się",
        level="B1",
        category="Gramatyka",
        summary="Cząstka się tworzy czasowniki zwrotne i różne konstrukcje bezosobowe.",
        explanation="Cząstka się może być częścią czasownika, wskazywać wzajemność albo tworzyć zdanie o ogólnym wykonawcy. Jej pozycja jest zwykle bliska odmienionemu czasownikowi, lecz zależy od szyku i akcentu.",
        structure="uczyć się; spotykać się; tutaj dobrze się mieszka",
        rules=[
            "Ucz się czasownika razem z cząstką, jeśli jest wymagana.",
            "Rozróżniaj znaczenie zwrotne, wzajemne i bezosobowe.",
            "Nie pomijaj się w czasowniku, który go wymaga.",
        ],
        examples=[
            GrammarExample(text="Uczę się polskiego od roku.", note="Czasownik zwrotny."),
            GrammarExample(
                text="W tym mieście dobrze się mieszka.", note="Konstrukcja bezosobowa."
            ),
        ],
    ),
    GrammarTopic(
        slug="strona-zwrotna",
        title="Strona zwrotna i wzajemność",
        level="B1",
        category="Gramatyka",
        summary="Konstrukcje zwrotne opisują działanie skierowane na wykonawcę lub wykonywane wzajemnie.",
        explanation="Cząstka się może oznaczać, że podmiot wykonuje czynność na sobie albo że kilka osób wykonuje ją wzajemnie. Znaczenie wynika z czasownika i kontekstu, dlatego nie każda forma z się jest dosłownie zwrotna.",
        structure="ubierać się; przyjaciele spotykają się",
        rules=[
            "Rozpoznawaj, czy podmiot jest odbiorcą własnego działania.",
            "Przy liczbie mnogiej sprawdź, czy czynność jest wzajemna.",
            "Uwzględniaj utrwalone znaczenie czasownika.",
        ],
        examples=[
            GrammarExample(text="Dziecko samo się ubiera.", note="Czynność skierowana na podmiot."),
            GrammarExample(
                text="Po latach przyjaciele spotkali się ponownie.", note="Znaczenie wzajemne."
            ),
        ],
    ),
    GrammarTopic(
        slug="imieslow-przymiotnikowy-czynny",
        title="Imiesłów przymiotnikowy czynny",
        level="B1",
        category="Gramatyka",
        summary="Imiesłów czynny opisuje wykonawcę czynności jako cechę osoby lub rzeczy.",
        explanation="Imiesłów przymiotnikowy czynny tworzy się od czasowników niedokonanych i uzgadnia z rzeczownikiem pod względem rodzaju, liczby i przypadku. Zastępuje zdanie względne, gdy podmiot wykonuje opisywaną czynność.",
        structure="czytać → czytający; pracować → pracujący",
        rules=[
            "Twórz imiesłów czynny od czasownika niedokonanego.",
            "Uzgadniaj jego formę z określanym rzeczownikiem.",
            "Nie używaj go, gdy opisywana osoba nie wykonuje czynności.",
        ],
        examples=[
            GrammarExample(
                text="Student czytający raport siedzi przy oknie.",
                note="Imiesłów określa wykonawcę.",
            ),
            GrammarExample(
                text="Rozmawiam z osobą pracującą w bibliotece.", note="Zgodność w narzędniku."
            ),
        ],
    ),
    GrammarTopic(
        slug="imieslow-przymiotnikowy-bierny",
        title="Imiesłów przymiotnikowy bierny",
        level="B1",
        category="Gramatyka",
        summary="Imiesłów bierny opisuje rzecz lub osobę jako odbiorcę zakończonej czynności.",
        explanation="Imiesłów przymiotnikowy bierny tworzy się od wielu czasowników przechodnich i uzgadnia z opisywanym rzeczownikiem. Może występować samodzielnie lub w stronie biernej z czasownikiem być albo zostać.",
        structure="napisać → napisany; przygotować → przygotowany",
        rules=[
            "Sprawdź, czy czasownik może tworzyć stronę bierną.",
            "Uzgadniaj imiesłów z rzeczownikiem.",
            "Wybieraj być lub zostać zgodnie z sensem i czasem wypowiedzi.",
        ],
        examples=[
            GrammarExample(
                text="Dokument przygotowany przez zespół jest gotowy.",
                note="Imiesłów określa rzeczownik.",
            ),
            GrammarExample(
                text="Raport został opublikowany wczoraj.", note="Strona bierna w czasie przeszłym."
            ),
        ],
    ),
    GrammarTopic(
        slug="zgoda-podmiotu-z-orzeczeniem",
        title="Zgoda podmiotu z orzeczeniem",
        level="B1",
        category="Gramatyka",
        summary="Forma orzeczenia zależy od liczby, osoby i rodzaju gramatycznego podmiotu.",
        explanation="W czasie przeszłym orzeczenie uzgadnia się z rodzajem podmiotu, a w liczbie mnogiej także z kategorią męskoosobowości. Przy podmiotach złożonych forma zależy od ich składu i szyku zdania.",
        structure="uczennica przyszła; uczniowie przyszli; dzieci przyszły",
        rules=[
            "Ustal rodzaj i liczbę całego podmiotu.",
            "W liczbie mnogiej odróżniaj formy męskoosobowe.",
            "Sprawdzaj zgodę przy podmiotach połączonych spójnikiem i.",
        ],
        examples=[
            GrammarExample(
                text="Nauczycielka i uczniowie rozpoczęli spotkanie.",
                note="Podmiot obejmuje mężczyznę lub grupę męskoosobową.",
            ),
            GrammarExample(
                text="Książki i zeszyty leżały na biurku.", note="Zgoda niemęskoosobowa."
            ),
        ],
    ),
    GrammarTopic(
        slug="szyk-zdania-i-temat",
        title="Szyk zdania i temat wypowiedzi",
        level="B1",
        category="Gramatyka",
        summary="Szyk wyrazów pomaga wskazać temat, kontrast i nową informację.",
        explanation="Polski szyk jest elastyczny dzięki odmianie, ale kolejność wyrazów wpływa na akcent informacyjny. Znana informacja często pojawia się wcześniej, a nowa lub kontrastowana może zostać przesunięta na koniec.",
        structure="temat + komentarz; kontrastowana informacja na końcu",
        rules=[
            "Zachowuj naturalny szyk, gdy nie chcesz podkreślać elementu.",
            "Przesuwaj wyraz dla kontrastu tylko wtedy, gdy kontekst to uzasadnia.",
            "Nie kopiuj mechanicznie szyku z języka obcego.",
        ],
        examples=[
            GrammarExample(text="Marta kupiła wczoraj nowy rower.", note="Neutralny szyk."),
            GrammarExample(
                text="Nowy rower kupiła wczoraj Marta.",
                note="Podmiot jest nową lub kontrastowaną informacją.",
            ),
        ],
    ),
    GrammarTopic(
        slug="aspekt-w-opowiadaniu",
        title="Aspekt w opowiadaniu",
        level="B1",
        category="Gramatyka",
        summary="Dobór aspektu porządkuje zdarzenia i tło w narracji.",
        explanation="Czasowniki niedokonane przedstawiają tło, trwanie lub powtarzalność. Dokonane ujmują kolejne zdarzenia jako całości. W jednym opowiadaniu oba aspekty mogą się przeplatać zgodnie z rolą informacji.",
        structure="tło: padał deszcz; zdarzenie: pociąg odjechał",
        rules=[
            "Używaj aspektu niedokonanego do opisu tła i trwania.",
            "Używaj aspektu dokonanego do kolejnych zdarzeń i rezultatów.",
            "Nie wybieraj aspektu wyłącznie na podstawie angielskiego czasu.",
        ],
        examples=[
            GrammarExample(
                text="Kiedy wracałam do domu, spotkałam dawną znajomą.",
                note="Tło niedokonane i zdarzenie dokonane.",
            ),
            GrammarExample(
                text="Otworzył drzwi, wszedł do pokoju i usiadł.",
                note="Sekwencja zakończonych zdarzeń.",
            ),
        ],
    ),
    GrammarTopic(
        slug="okoliczniki-i-przypadki",
        title="Okoliczniki miejsca i czasu",
        level="B1",
        category="Gramatyka",
        summary="Przypadek po przyimku często zależy od tego, czy opisujemy miejsce, czy kierunek.",
        explanation="Niektóre przyimki łączą się z różnymi przypadkami zależnie od znaczenia. Miejscownik opisuje położenie po w, na i przy, a biernik może wskazywać kierunek ruchu po w lub na.",
        structure="w mieście — do miasta; na stole — na stół",
        rules=[
            "Rozróżniaj pytanie gdzie? od dokąd?.",
            "Ustal przypadek wymagany przez przyimek w danym znaczeniu.",
            "Zapamiętuj typowe pary miejsca i kierunku.",
        ],
        examples=[
            GrammarExample(text="Książka leży na stole.", note="Miejsce i miejscownik."),
            GrammarExample(text="Położyłam książkę na stół.", note="Kierunek/rezultat i biernik."),
        ],
    ),
    GrammarTopic(
        slug="przypadek-po-przeczeniu",
        title="Przypadek dopełnienia po przeczeniu",
        level="B1",
        category="Gramatyka",
        summary="Przeczenie może zmienić przypadek dopełnienia czasownika.",
        explanation="W wielu zdaniach dopełnienie biernikowe przy przeczeniu przyjmuje dopełniacz. Zmiana jest szczególnie widoczna przy rzeczownikach niepoliczalnych i w połączeniach z czasownikami posiadania lub zauważania.",
        structure="mam czas → nie mam czasu; widzę błąd → nie widzę błędu",
        rules=[
            "Sprawdź, czy przeczenie wymaga dopełniacza zamiast biernika.",
            "Uzgodnij przymiotnik z rzeczownikiem w zmienionym przypadku.",
            "Nie zmieniaj przypadku, gdy czasownik lub konstrukcja wymaga innego.",
        ],
        examples=[
            GrammarExample(
                text="Nie przeczytałam jeszcze tej książki.", note="Dopełniacz w zdaniu przeczącym."
            ),
            GrammarExample(
                text="Nie widzę żadnego problemu.", note="Przymiotnik i rzeczownik w dopełniaczu."
            ),
        ],
    ),
]
