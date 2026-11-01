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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
    ),
    GrammarTopic(
        slug="imieslowy-przyslowkowe",
        title="Imiesłowy przysłówkowe",
        level="B2",
        category="Gramatyka",
        summary="Imiesłów przysłówkowy łączy czynności wykonywane przez ten sam podmiot.",
        explanation="Imiesłów współczesny opisuje czynność równoczesną, a uprzedni — wcześniejszą. Podmiot obu czynności powinien być ten sam; konstrukcja imiesłowowa nie zastępuje poprawnego zdania z innym wykonawcą.",
        structure="czytając raport, notowała; przeczytawszy raport, wysłała go",
        rules=[
            "Używaj imiesłowu współczesnego dla czynności równoczesnej.",
            "Używaj imiesłowu uprzedniego dla wcześniejszej zakończonej czynności.",
            "Zachowuj tego samego wykonawcę w obu czynnościach.",
        ],
        examples=[
            GrammarExample(
                text="Wracając z pracy, słuchała podcastu.", note="Czynności równoczesne."
            ),
            GrammarExample(
                text="Przeczytawszy umowę, wysłał odpowiedź.", note="Czynność wcześniejsza."
            ),
        ],
    ),
    GrammarTopic(
        slug="strona-bierna-a-bierne-alternatywy",
        title="Strona bierna i konstrukcje bezosobowe",
        level="B2",
        category="Gramatyka",
        summary="Polszczyzna może przesunąć uwagę z wykonawcy na odbiorcę działania lub sam proces.",
        explanation="Stronę bierną tworzy się między innymi za pomocą być lub zostać i imiesłowu biernego. W wielu kontekstach naturalniejsza jest forma bezosobowa z się albo -no/-to; wybór zmienia akcent, niekoniecznie samą treść.",
        structure="raport został opublikowany; opublikowano raport; mówi się o raporcie",
        rules=[
            "Wybieraj stronę bierną, gdy ważny jest odbiorca działania.",
            "Używaj form bezosobowych, gdy wykonawca jest nieznany lub nieistotny.",
            "Nie mieszaj rodzaju orzeczenia z rodzajem rzeczownika.",
        ],
        examples=[
            GrammarExample(
                text="Wyniki zostały przedstawione na konferencji.", note="Strona bierna."
            ),
            GrammarExample(text="Na konferencji przedstawiono wyniki.", note="Forma bezosobowa."),
        ],
    ),
    GrammarTopic(
        slug="zdania-wtracone-i-przecinki",
        title="Zdania wtrącone i interpunkcja",
        level="B2",
        category="Gramatyka",
        summary="Przecinki wyznaczają granice zdań podrzędnych i wtrąceń.",
        explanation="Zdania podrzędne oraz wtrącone oddziela się przecinkami. Przy kilku zdaniach składowych interpunkcja powinna odzwierciedlać ich strukturę, a nie tylko pauzy w mowie.",
        structure="zdanie główne, które..., zdanie główne",
        rules=[
            "Oddzielaj przecinkiem zdanie podrzędne od nadrzędnego.",
            "Obejmuj zdanie wtrącone przecinkami z obu stron.",
            "Nie stawiaj przecinka między podmiotem a orzeczeniem bez uzasadnienia składniowego.",
        ],
        examples=[
            GrammarExample(
                text="Książka, którą mi poleciłaś, jest już dostępna.",
                note="Zdanie względne wtrącone.",
            ),
            GrammarExample(
                text="Wiem, że raport jest gotowy, ale jeszcze go nie wysłałem.",
                note="Granice zdań składowych.",
            ),
        ],
    ),
    GrammarTopic(
        slug="zdania-przyzwalajace",
        title="Zdania przyzwalające",
        level="B2",
        category="Gramatyka",
        summary="Zdania przyzwalające wskazują okoliczność, która nie zmienia oczekiwanego skutku.",
        explanation="Spójniki chociaż, mimo że i choć wprowadzają przeszkodę lub kontrast. Mimo że i chociaż łączą pełne zdania, a mimo może też występować z rzeczownikiem lub bezokolicznikiem.",
        structure="chociaż/mimo że + zdanie; mimo + dopełniacz",
        rules=[
            "Dobieraj konstrukcję do tego, czy po niej występuje zdanie, czy rzeczownik.",
            "Oddzielaj zdania składowe przecinkiem.",
            "Nie utożsamiaj przyzwolenia ze zwykłą przyczyną.",
        ],
        examples=[
            GrammarExample(
                text="Mimo że padało, mecz się odbył.", note="Pełne zdanie przyzwalające."
            ),
            GrammarExample(text="Mimo deszczu mecz się odbył.", note="Przyimek z dopełniaczem."),
        ],
    ),
    GrammarTopic(
        slug="mowa-zalezna-pytania",
        title="Pytania w mowie zależnej",
        level="B2",
        category="Gramatyka",
        summary="Pytanie zależne zachowuje szyk zdania oznajmującego i nie kończy się znakiem zapytania.",
        explanation="Pytania zależne rozpoczynają się od czy lub zaimka pytajnego. Wewnątrz zdania oznajmującego zachowują szyk właściwy zdaniu podrzędnemu i oddziela się je przecinkiem.",
        structure="zapytać, czy...; nie wiedzieć, kiedy...",
        rules=[
            "Używaj czy w pytaniu zależnym bez zaimka pytajnego.",
            "Zachowuj szyk zdania oznajmującego.",
            "Stawiaj znak zapytania tylko wtedy, gdy całe zdanie jest pytaniem.",
        ],
        examples=[
            GrammarExample(text="Zapytała, czy pociąg już odjechał.", note="Pytanie zależne."),
            GrammarExample(
                text="Nie wiem, kiedy zaczyna się spotkanie.",
                note="Zaimek pytajny w zdaniu zależnym.",
            ),
        ],
    ),
    GrammarTopic(
        slug="spojniki-wynikowe",
        title="Spójniki wynikowe i przeciwstawne",
        level="B2",
        category="Gramatyka",
        summary="Spójniki precyzują relację między argumentem, kontrastem i wnioskiem.",
        explanation="Zatem, dlatego, natomiast i jednak sygnalizują różne relacje logiczne. Ich pozycja wpływa na rytm wypowiedzi, ale nie zastępuje wyraźnego związku znaczeniowego między zdaniami.",
        structure="przesłanka, dlatego wniosek; teza, jednak kontrast",
        rules=[
            "Dobieraj spójnik do rzeczywistej relacji logicznej.",
            "Oddzielaj przecinkiem zdania składowe zgodnie z ich budową.",
            "Unikaj nagromadzenia spójników o tej samej funkcji.",
        ],
        examples=[
            GrammarExample(
                text="Próba była niewielka, dlatego wynik należy interpretować ostrożnie.",
                note="Relacja wynikowa.",
            ),
            GrammarExample(
                text="Projekt jest kosztowny, jednak może przynieść długofalowe korzyści.",
                note="Kontrast.",
            ),
        ],
    ),
    GrammarTopic(
        slug="tryb-warunkowy-wypowiedzi",
        title="Tryb warunkowy w wypowiedziach hipotetycznych",
        level="B2",
        category="Gramatyka",
        summary="Tryb warunkowy pozwala rozróżniać warunki realne, hipotetyczne i niespełnione.",
        explanation="Formy warunkowe mogą wyrażać przypuszczenie dotyczące teraźniejszości, przyszłości lub przeszłości. W zdaniach z gdyby cząstka by łączy się z odpowiednią formą, a czasownik zachowuje właściwy aspekt.",
        structure="gdyby + forma przeszła; zrobiłbym; byłbym zrobił",
        rules=[
            "Dopasuj formę do osoby i rodzaju.",
            "Rozróżniaj warunek możliwy od niespełnionego.",
            "Dobieraj aspekt do tego, czy istotny jest proces, czy rezultat.",
        ],
        examples=[
            GrammarExample(
                text="Gdybyśmy mieli więcej czasu, sprawdzilibyśmy dane ponownie.",
                note="Warunek hipotetyczny.",
            ),
            GrammarExample(
                text="Gdyby wcześniej wysłał dokument, zdążyłby na termin.",
                note="Niespełniony warunek przeszły.",
            ),
        ],
    ),
    GrammarTopic(
        slug="zdania-bezokolicznikowe",
        title="Konstrukcje bezokolicznikowe",
        level="B2",
        category="Gramatyka",
        summary="Bezokolicznik może uzupełniać czasownik modalny, fazowy lub wyrażenie celu.",
        explanation="Po wielu czasownikach, takich jak móc, zacząć i próbować, występuje bezokolicznik. Podmiot obu czynności jest zwykle ten sam; przy zmianie wykonawcy potrzebne jest zdanie podrzędne.",
        structure="mogę sprawdzić; zaczął pisać; żeby zespół sprawdził",
        rules=[
            "Używaj bezokolicznika po czasownikach, które go wymagają.",
            "Sprawdź, czy obie czynności mają tego samego wykonawcę.",
            "W zdaniu celu dobieraj żeby wraz z właściwą formą czasownika.",
        ],
        examples=[
            GrammarExample(text="Zespół może opublikować raport jutro.", note="Wspólny wykonawca."),
            GrammarExample(
                text="Poprosiła, żeby kolega sprawdził dane.",
                note="Inny wykonawca w zdaniu podrzędnym.",
            ),
        ],
    ),
    GrammarTopic(
        slug="imieslowy-w-stylu-pisemnym",
        title="Imiesłowy w stylu pisanym",
        level="B2",
        category="Gramatyka",
        summary="Imiesłowy pozwalają kondensować informację, ale wymagają jasnej relacji do rzeczownika.",
        explanation="Imiesłowy przymiotnikowe i przysłówkowe skracają zdania, lecz nadmierne ich użycie utrudnia odbiór. Konstrukcja musi jasno wskazywać, do którego rzeczownika lub wykonawcy się odnosi.",
        structure="dane zebrane w badaniu; analizując wyniki, autorzy...",
        rules=[
            "Upewnij się, że imiesłów ma jednoznaczne odniesienie.",
            "Zachowuj zgodność imiesłowu przymiotnikowego z rzeczownikiem.",
            "Zastąp konstrukcję zdaniem, jeśli skrót zaciemnia wykonawcę.",
        ],
        examples=[
            GrammarExample(
                text="Dane zebrane w marcu opublikowano w raporcie.", note="Imiesłów określa dane."
            ),
            GrammarExample(
                text="Analizując wyniki, autorka zauważyła rozbieżność.",
                note="Wykonawcą obu czynności jest autorka.",
            ),
        ],
    ),
    GrammarTopic(
        slug="przydawki-rzeczownikowe",
        title="Rozbudowane grupy rzeczownikowe",
        level="B2",
        category="Gramatyka",
        summary="Kilka określeń rzeczownika wymaga czytelnego szyku i zgodności przypadków.",
        explanation="Grupa rzeczownikowa może zawierać przymiotniki, dopełniacze i wyrażenia przyimkowe. Ich kolejność pomaga odróżnić określenia równorzędne od tych, które zależą od siebie.",
        structure="szczegółowa analiza wyników badania; raport dotyczący jakości danych",
        rules=[
            "Uzgadniaj przymiotniki z określanym rzeczownikiem.",
            "Umieszczaj dopełnienia blisko wyrazu, którego dotyczą.",
            "Przebuduj grupę, jeśli nie wiadomo, które określenie obejmuje rzeczownik.",
        ],
        examples=[
            GrammarExample(
                text="Zespół przedstawił szczegółową analizę nowych danych.",
                note="Zgodność określeń z rzeczownikiem.",
            ),
            GrammarExample(
                text="Raport dotyczący jakości próby wymaga uzupełnienia.",
                note="Wyrażenie przyimkowe określa raport.",
            ),
        ],
    ),
]
