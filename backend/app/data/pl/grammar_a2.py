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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
    ),
    GrammarTopic(
        slug="celownik",
        title="Celownik",
        level="A2",
        category="Gramatyka",
        summary="Celownik wskazuje odbiorcę, adresata lub osobę, której dotyczy czynność.",
        explanation="Celownik odpowiada często na pytania komu? czemu? i występuje po czasownikach takich jak pomagać, dziękować czy przyglądać się. Końcówki rzeczowników zależą od rodzaju i liczby.",
        structure="pomagać + celownik; dziękować + celownik",
        rules=[
            "Zapamiętuj czasownik razem z wymaganym celownikiem.",
            "Uzgadniaj zaimek i przymiotnik z rzeczownikiem.",
            "Nie zastępuj celownika biernikiem po pomagać.",
        ],
        examples=[
            GrammarExample(text="Pomagam nowemu sąsiadowi.", note="Celownik rodzaju męskiego."),
            GrammarExample(
                text="Dziękuję pani za wiadomość.", note="Celownik zaimka grzecznościowego."
            ),
        ],
    ),
    GrammarTopic(
        slug="zaimki-w-przypadkach",
        title="Zaimki osobowe w przypadkach",
        level="A2",
        category="Gramatyka",
        summary="Zaimki osobowe zmieniają formę zależnie od swojej funkcji w zdaniu.",
        explanation="Formy mnie, mi, ciebie, ci, jego, jej, nas i wam zastępują rzeczowniki w odpowiednim przypadku. Krótsze formy zwykle stoją blisko czasownika, a formy akcentowane służą między innymi kontrastowi.",
        structure="widzę ją; daję mu książkę; rozmawiam z nimi",
        rules=[
            "Dobieraj przypadek zaimka do czasownika lub przyimka.",
            "Używaj form akcentowanych dla kontrastu lub nacisku.",
            "Pamiętaj o formach po przyimkach: ze mną, do niego.",
        ],
        examples=[
            GrammarExample(text="Czy możesz mi pomóc?", note="Celownik w krótkiej formie."),
            GrammarExample(text="Ten list jest dla niej.", note="Forma po przyimku dla."),
        ],
    ),
    GrammarTopic(
        slug="liczebniki-i-przypadek",
        title="Liczebniki i przypadek rzeczownika",
        level="A2",
        category="Gramatyka",
        summary="Liczebnik wpływa na formę rzeczownika i czasownika w zdaniu.",
        explanation="Po dwa, trzy i cztery rzeczownik ma zwykle formę mnogą, a po liczebnikach pięć i wyższych często występuje dopełniacz liczby mnogiej. Zgodność czasownika zależy między innymi od tego, czy grupa jest podmiotem.",
        structure="dwa bilety; pięć biletów",
        rules=[
            "Ucz się połączenia liczebnika z właściwą formą rzeczownika.",
            "Po liczebnikach pięć i wyższych stosuj zwykle dopełniacz liczby mnogiej.",
            "Zwracaj uwagę na zgodność orzeczenia z całym podmiotem.",
        ],
        examples=[
            GrammarExample(text="Mam trzy wolne dni.", note="Rzeczownik w liczbie mnogiej."),
            GrammarExample(text="Na stole leży pięć listów.", note="Dopełniacz liczby mnogiej."),
        ],
    ),
    GrammarTopic(
        slug="czas-przeszly-rodzaj",
        title="Rodzaj w czasie przeszłym",
        level="A2",
        category="Gramatyka",
        summary="Forma czasu przeszłego zależy od rodzaju i liczby podmiotu.",
        explanation="W liczbie pojedynczej czas przeszły rozróżnia rodzaj męski, żeński i nijaki. W liczbie mnogiej formy zależą między innymi od tego, czy grupa jest męskoosobowa.",
        structure="czytałem; czytałam; czytało; czytali; czytały",
        rules=[
            "Dopasuj końcówkę czasu przeszłego do rodzaju podmiotu.",
            "W liczbie mnogiej rozróżniaj grupy męskoosobowe i pozostałe.",
            "Nie pomijaj informacji o osobie, jeśli forma może być niejasna.",
        ],
        examples=[
            GrammarExample(text="Dziecko zasnęło przed północą.", note="Rodzaj nijaki."),
            GrammarExample(
                text="Studentki wróciły po zajęciach.", note="Liczba mnoga niemęskoosobowa."
            ),
        ],
    ),
    GrammarTopic(
        slug="czasowniki-ruchu",
        title="Czasowniki ruchu",
        level="A2",
        category="Gramatyka",
        summary="Polskie czasowniki ruchu rozróżniają kierunek, powtarzalność i sposób przemieszczania się.",
        explanation="Iść i jechać opisują ruch w jednym kierunku, a chodzić i jeździć zwykle ruch powtarzany lub odbywający się w różnych kierunkach. Dobór czasownika zależy także od tego, czy podróż odbywa się pieszo, czy środkiem transportu.",
        structure="iść/chodzić — pieszo; jechać/jeździć — transportem",
        rules=[
            "Wybieraj iść lub jechać dla ruchu w określonym kierunku.",
            "Wybieraj chodzić lub jeździć dla zwyczaju lub powtarzalności.",
            "Łącz czasownik z odpowiednim przyimkiem i przypadkiem.",
        ],
        examples=[
            GrammarExample(
                text="Teraz jadę do pracy tramwajem.", note="Jedna podróż środkiem transportu."
            ),
            GrammarExample(
                text="Codziennie chodzę do biura pieszo.", note="Powtarzalny ruch pieszo."
            ),
        ],
    ),
    GrammarTopic(
        slug="przyslowki-i-stopniowanie",
        title="Przysłówki i stopniowanie",
        level="A2",
        category="Gramatyka",
        summary="Przysłówki opisują sposób, czas lub częstotliwość czynności i mogą podlegać stopniowaniu.",
        explanation="Wiele przysłówków tworzy się od przymiotników przez zmianę końcówki, a ich stopień wyższy i najwyższy może mieć formę regularną lub nieregularną. Przysłówek nie uzgadnia się z rzeczownikiem.",
        structure="szybki → szybko → szybciej → najszybciej",
        rules=[
            "Używaj przysłówka do opisu czasownika.",
            "Odróżniaj przysłówek od przymiotnika.",
            "Zapamiętuj nieregularne formy, takie jak dobrze — lepiej.",
        ],
        examples=[
            GrammarExample(
                text="Pociąg jedzie szybciej niż autobus.", note="Stopień wyższy przysłówka."
            ),
            GrammarExample(text="Marta najlepiej mówi po polsku.", note="Stopień najwyższy."),
        ],
    ),
    GrammarTopic(
        slug="zdania-czasowe",
        title="Zdania czasowe",
        level="A2",
        category="Gramatyka",
        summary="Zdania czasowe określają, kiedy jedna czynność odbywa się względem drugiej.",
        explanation="Spójniki kiedy, zanim, gdy i po tym jak łączą zdarzenia w czasie. W zdaniach o przyszłości polszczyzna często używa czasu teraźniejszego po kiedy, jeśli czynność ma się dopiero wydarzyć.",
        structure="Zadzwonię, kiedy wrócę.",
        rules=[
            "Oddzielaj zdanie podrzędne przecinkiem.",
            "Używaj czasu teraźniejszego po kiedy w odniesieniu do przyszłości.",
            "Wybieraj zanim lub po tym jak zgodnie z kolejnością zdarzeń.",
        ],
        examples=[
            GrammarExample(
                text="Zadzwonię, kiedy dojadę do domu.",
                note="Przyszłość wyrażona czasem teraźniejszym.",
            ),
            GrammarExample(text="Zamknij okno, zanim wyjdziesz.", note="Czynność wcześniejsza."),
        ],
    ),
]
