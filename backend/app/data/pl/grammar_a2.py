"""Polish grammar topics — A2."""

from app.data._types import GrammarExample, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="czas-przeszly",
        title="Czas przeszły",
        level="A2",
        category="Gramatyka",
        summary="Czas przeszły opisuje zdarzenia wcześniejsze i uzgadnia formę z rodzajem.",
        explanation="Polski czas przeszły odmienia się przez osoby oraz rodzaje w liczbie pojedynczej i mnogiej. W pierwszej i drugiej osobie końcówki osobowe mogą występować po czasowniku lub zaimku, zależnie od szyku.",
        structure="czytałem/czytałam, czytałeś/czytałaś, czytał/czytała; czytaliśmy/czytałyśmy",
        rules=[
            "Dobierz rodzaj do mówiącego lub podmiotu.",
            "Stosuj końcówki osobowe odpowiednie dla osoby.",
            "Używaj określeń czasu, gdy kolejność zdarzeń nie jest oczywista.",
        ],
        examples=[
            GrammarExample(
                text="Wczoraj napisałam długi e-mail.",
                translation=None,
                note="Rodzaj żeński i zakończone zdarzenie.",
            ),
            GrammarExample(
                text="Dzieci wróciły przed zmrokiem.",
                translation=None,
                note="Liczba mnoga niemęskoosobowa.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="czas-przyszly",
        title="Czas przyszły",
        level="A2",
        category="Gramatyka",
        summary="Przyszłość wyraża się formą dokonaną albo złożoną formą niedokonaną.",
        explanation="Czasownik dokonany w czasie teraźniejszym ma znaczenie przyszłe. Czasownik niedokonany tworzy przyszłość z formą będę i bezokolicznikiem albo formą osobową, na przykład będę czytać lub będę czytał.",
        structure="napiszę; będę czytać / będę czytał",
        rules=[
            "Rozróżniaj planowany przebieg od zakończonego rezultatu.",
            "Uzgadniaj formę osobową z podmiotem.",
            "Nie łącz będę z czasownikiem dokonanym.",
        ],
        examples=[
            GrammarExample(
                text="Jutro będziemy zwiedzać muzeum.",
                translation=None,
                note="Przyszła czynność niedokonana.",
            ),
            GrammarExample(
                text="Wieczorem przeczytam raport.",
                translation=None,
                note="Przyszły rezultat dokonany.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="dopelniacz",
        title="Dopełniacz",
        level="A2",
        category="Gramatyka",
        summary="Dopełniacz wyraża między innymi brak, przynależność, ilość i cel ruchu.",
        explanation="Dopełniacz odpowiada na pytania kogo? czego?. Występuje po przeczeniu wielu czasowników, po wyrażeniach ilości oraz po wybranych przyimkach. Końcówka zależy od rodzaju, liczby i wzoru odmiany.",
        structure="nie mam kogo? czego?; dużo czasu; do sklepu",
        rules=[
            "Po przeczeniu mam użyj formy dopełniacza.",
            "Po przyimku do stosuj dopełniacz.",
            "Kontroluj końcówki przymiotnika i rzeczownika.",
        ],
        examples=[
            GrammarExample(
                text="Nie mam dzisiaj czasu.",
                translation=None,
                note="Dopełniacz po przeczeniu.",
            ),
            GrammarExample(
                text="Idziemy do nowego teatru.",
                translation=None,
                note="Dopełniacz po do.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="narzednik",
        title="Narzędnik",
        level="A2",
        category="Gramatyka",
        summary="Narzędnik opisuje narzędzie, sposób oraz role po wybranych czasownikach.",
        explanation="Narzędnik odpowiada na pytania kim? czym? Pojawia się z przyimkiem z, a także w orzeczniku po być, zostać i interesować się. Końcówka zależy od rodzaju i liczby.",
        structure="kim? czym?; jestem lekarzem; jadę pociągiem",
        rules=[
            "Po być przy nazwie zawodu używaj narzędnika.",
            "Po z w znaczeniu towarzyszenia używaj narzędnika.",
            "Uzgadniaj przymiotnik z rzeczownikiem.",
        ],
        examples=[
            GrammarExample(
                text="Rozmawiam z nową sąsiadką.",
                translation=None,
                note="Towarzyszenie.",
            ),
            GrammarExample(
                text="Mój brat jest architektem.",
                translation=None,
                note="Nazwa zawodu w narzędniku.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="miejscownik",
        title="Miejscownik",
        level="A2",
        category="Gramatyka",
        summary="Miejscownik wskazuje miejsce lub temat po określonych przyimkach.",
        explanation="Miejscownik występuje zawsze z przyimkiem. Typowe połączenia to w, na, o i po. Końcówki rzeczownika często zmieniają temat, dlatego formę warto uczyć razem z przyimkiem.",
        structure="w kim? w czym?; na poczcie; o czym?",
        rules=[
            "Używaj miejscownika po w, na i o w znaczeniu miejsca lub tematu.",
            "Zapamiętuj przyimek razem z rzeczownikiem.",
            "Zmieniaj końcówkę przymiotnika zgodnie z rzeczownikiem.",
        ],
        examples=[
            GrammarExample(
                text="Pracuję w dużym biurze.",
                translation=None,
                note="Miejsce po w.",
            ),
            GrammarExample(
                text="Myślimy o wakacjach.",
                translation=None,
                note="Temat po o.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="przyimki",
        title="Przyimki miejsca i ruchu",
        level="A2",
        category="Gramatyka",
        summary="Przyimki wskazują położenie, kierunek oraz relacje między miejscami.",
        explanation="Przyimek wpływa na przypadek następującego po nim rzeczownika. Ten sam przyimek może łączyć się z różnymi przypadkami zależnie od tego, czy opisuje położenie, czy ruch do celu.",
        structure="w domu, do domu, na rynek, z rynku",
        rules=[
            "Odróżniaj miejsce od kierunku ruchu.",
            "Sprawdzaj przypadek wymagany przez przyimek.",
            "Dobieraj przyimek do znaczenia czasownika ruchu.",
        ],
        examples=[
            GrammarExample(
                text="Jesteśmy w centrum miasta.",
                translation=None,
                note="Położenie.",
            ),
            GrammarExample(
                text="Jedziemy na dworzec.",
                translation=None,
                note="Kierunek ruchu.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="tryb-rozkazujacy",
        title="Tryb rozkazujący i prośby",
        level="A2",
        category="Gramatyka",
        summary="Tryb rozkazujący wyraża polecenie, zachętę lub prośbę.",
        explanation="Formy rozkazujące zależą od osoby i wzoru czasownika. Uprzejme prośby często używają proszę oraz bezokolicznika albo formy niech pan/pani. Przeczenie tworzy się przez nie przed formą czasownika.",
        structure="czytaj; proszę poczekać; niech pani usiądzie",
        rules=[
            "Dopasuj formę rozkazującą do adresata.",
            "Łagodź polecenia przez proszę lub konstrukcję warunkową.",
            "W uprzejmym zwrocie pan/pani łącz z czasownikiem w trzeciej osobie.",
        ],
        examples=[
            GrammarExample(
                text="Proszę powtórzyć adres.",
                translation=None,
                note="Uprzejma prośba z bezokolicznikiem.",
            ),
            GrammarExample(
                text="Niech państwo wejdą.",
                translation=None,
                note="Uprzejma forma liczby mnogiej.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="stopniowanie-przymiotnikow",
        title="Stopniowanie przymiotników",
        level="A2",
        category="Gramatyka",
        summary="Stopień wyższy i najwyższy porównują cechy osób i rzeczy.",
        explanation="Większość przymiotników tworzy stopień wyższy przez zmianę tematu i dodanie końcówki, a najwyższy przez dodanie naj-. Niektóre formy są nieregularne. Porównanie często zawiera niż lub od.",
        structure="wysoki — wyższy — najwyższy; dobry — lepszy — najlepszy",
        rules=[
            "Ucz się nieregularnych stopni razem z przymiotnikiem.",
            "Używaj niż lub od do wskazania porównania.",
            "Uzgadniaj przymiotnik z opisywanym rzeczownikiem.",
        ],
        examples=[
            GrammarExample(
                text="Ten pociąg jest szybszy niż autobus.",
                translation=None,
                note="Stopień wyższy i porównanie.",
            ),
            GrammarExample(
                text="To najciekawsza książka w bibliotece.",
                translation=None,
                note="Stopień najwyższy uzgodniony z rzeczownikiem.",
            ),
        ],
        common_mistakes=[
        ],
    ),
]
