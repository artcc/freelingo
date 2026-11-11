"""Polish grammar topics — C2."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="rejestr-jezykowy",
        title="Rejestr językowy i jego odmiany",
        level="C2",
        category="Stylistyka",
        summary="Świadome przełączanie rejestru zależnie od gatunku, odbiorcy i celu wypowiedzi.",
        explanation=(
            "**Rejestr** to konfiguracja środków językowych zależna od sytuacji, relacji "
            "między rozmówcami i celu wypowiedzi. Ten sam komunikat można przekazać na kilka "
            "sposobów; ich **stosowność** zależy od gatunku i relacji z odbiorcą.\n"
            "- **Oficjalny**: formuły, nominalizacje, brak ekspresji („Niniejszym informuję...”).\n"
            "- **Neutralny**: jasność i rzeczowość bez patyny urzędowej.\n"
            "- **Potoczny**: elipsa, partykuły, ekspresja („Daj znać, czy ogarniamy temat”).\n"
            "Rejestr nie jest tym samym co **styl**: rejestr opisuje sytuację użycia, styl — "
            "indywidualny lub gatunkowy sposób kształtowania tekstu.\n"
            "*Mieszanie rejestrów bywa zabiegiem*: w felietonie kontrast formuły urzędowej "
            "z mową potoczną buduje ironię. W podaniu ten sam kontrast będzie błędem."
        ),
        structure=(
            "[formuła otwarcia] + [treść] + [formuła zamykająca] — dobór zależny od gatunku "
            "i odbiorcy"
        ),
        rules=[
            "Rejestr wynika z sytuacji, nie z ambicji stylistycznych autora.",
            "Formy adresatywne (Pan, Państwo, ty) muszą być konsekwentne w całym tekście.",
            "Mieszanie rejestrów jest dopuszczalne tylko jako środek celowy i rozpoznawalny.",
            "Błąd rejestru psuje wrażenie kompetencji nawet przy poprawnej gramatyce.",
        ],
        examples=[
            GrammarExample(
                text="Niniejszym informuję, że wniosek został rozpatrzony pozytywnie.",
                translation=None,
                note="rejestr oficjalny: formuła performatywna i strona bierna",
            ),
            GrammarExample(
                text="Szanowni Państwo, uprzejmie proszę o potwierdzenie terminu spotkania.",
                translation=None,
                note="formuła adresatywna i grzecznościowa",
            ),
            GrammarExample(
                text="Daj znać, czy ogarniamy ten temat do piątku.",
                translation=None,
                note="rejestr potoczny: elipsa i leksyka środowiskowa",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Szanowny Panie Prezesie! Ogarniemy temat i damy znać.",
                correct=(
                    "Szanowny Panie Prezesie, zajmiemy się tą sprawą i przekażemy informację "
                    "o jej realizacji."
                ),
                note="Mieszanie rejestru oficjalnego z potocznym narusza decorum.",
            ),
            GrammarMistake(
                wrong="W dniu dzisiejszym mam urwanie głowy, więc nie przyjdę.",
                correct="Dziś nie mogę przyjść z powodu nadmiaru obowiązków.",
                note="Formuła urzędowa z idiomem potocznym daje efekt komiczny.",
            ),
        ],
        related=["dobor-slow", "styl-formalny", "jezyk-potoczny"],
    ),
    GrammarTopic(
        slug="dobor-slow",
        title="Dobór słownictwa i nacechowanie",
        level="C2",
        category="Leksyka",
        summary="Wybieranie wyrazów według znaczenia, konotacji, łączliwości i rejestru.",
        explanation=(
            "**Dobór słowa** to decyzja o znaczeniu, nacechowaniu i łączliwości, nie tylko "
            "o poprawności słownikowej.\n"
            "- **Denotacja** wyznacza zakres przedmiotowy, **konotacja** — zabarwienie "
            "emocjonalne i oceniające.\n"
            "- Synonimy rzadko są wymienne: *zmarł*, *odszedł* i *kopnął w kalendarz* odnoszą "
            "się do tego samego zdarzenia, ale sytuują mówiącego inaczej.\n"
            "- **Kolokacje** wiążą wyraz z konkretnymi partnerami: *poważny* błąd, ale "
            "*ciężkie* przestępstwo.\n"
            "Na poziomie C2 istotna jest **gospodarka słowem**: mniej rzeczowników "
            "odczasownikowych, mniej pustych wzmocnień, każdy wyraz na swoim miejscu."
        ),
        structure="wyraz neutralny → wariant książkowy / potoczny / nacechowany",
        rules=[
            "Sprawdzać konotację, nie tylko definicję słownikową.",
            "Nie zastępować synonimu, jeśli ma inną łączliwość.",
            "Unikać łańcuchów rzeczowników odczasownikowych, gdy wystarczy czasownik.",
            "Eufemizm jest wyborem etycznym, nie tylko stylistycznym.",
        ],
        examples=[
            GrammarExample(
                text="Zmarł wczoraj w nocy, otoczony rodziną.",
                translation=None,
                note="neutralne i godne",
            ),
            GrammarExample(
                text="Odszedł wczoraj w nocy.",
                translation=None,
                note="eufemizm o zabarwieniu emocjonalnym",
            ),
            GrammarExample(
                text="Firma zredukowała zatrudnienie o sto osób.",
                translation=None,
                note="eufemizm korporacyjny wobec „zwolniła”",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Podjął decyzję o tym, że pójdzie na studia.",
                correct="Zdecydował się pójść na studia.",
                note="Wariant zwięźlejszy stylistycznie; zdanie wyjściowe jest gramatycznie poprawne.",
            ),
            GrammarMistake(
                wrong="Odniósł zwycięstwo w postaci wygranej.",
                correct="Zwyciężył.",
                note="Pleonazm: „zwycięstwo w postaci wygranej” mówi to samo dwa razy.",
            ),
        ],
        related=["rejestr-jezykowy", "kolokacje", "frazeologia"],
    ),
    GrammarTopic(
        slug="skladnia-emfatyczna",
        title="Szyk emfatyczny i zdania wyodrębnione",
        level="C2",
        category="Składnia",
        summary="Wykorzystywanie szyku, kleftu i akcentu zdaniowego do sterowania uwagą odbiorcy.",
        explanation=(
            "Polski ma **szyk swobodny, lecz nie dowolny**: kolejność składników wyznacza "
            "strukturę tematyczno-rematyczną, a więc to, co znane (temat), i to, co nowe "
            "(remat).\n"
            "- **Wyodrębnienie na początku** sygnalizuje temat: *Raport napisał Jan* "
            "(nie kto inny).\n"
            "- **Konstrukcja kleftowa** *To Jan napisał raport* przenosi akcent kontrastowy "
            "na *Jan*.\n"
            "- **Remat na końcu** nosi najsilniejszy akcent zdaniowy: *Dopiero po godzinie "
            "zorientował się, że zgubił klucze*.\n"
            "Emfazę można zaznaczyć intonacją lub szykiem. Sama emfaza nie uzasadnia "
            "przecinka: piszemy *To Jan napisał raport*, bez przecinka po Jan.\n"
            "*Nadmiarem emfazy* mówca traci wiarygodność: każdy kontrast przestaje być "
            "kontrastem."
        ),
        structure="To + [wyodrębniony składnik] + reszta zdania; [składnik] to + orzeczenie",
        rules=[
            "Człon kontrastowany przenosi się na pozycję przed orzeczeniem lub po nim.",
            "W konstrukcji To Jan napisał raport to pozostaje nieodmienne; "
            "wyróżniany składnik zachowuje swój przypadek: To Jana widziałem.",
            "Akcent zdaniowy zaznacza się w piśmie szykiem, nie wykrzyknikiem.",
            "Emfaza działa, dopóki jest rzadka.",
        ],
        examples=[
            GrammarExample(
                text="To Anna podpisała umowę, nie Piotr.",
                translation=None,
                note="kleft z kontrastem",
            ),
            GrammarExample(
                text="Dopiero po godzinie zorientował się, że zgubił klucze.",
                translation=None,
                note="dopiero ogranicza czas; akcent na godzinie wymaga odpowiedniej intonacji",
            ),
            GrammarExample(
                text="Nigdy więcej nie wrócę w to miejsce.",
                translation=None,
                note="okolicznik i przeczenie na początku wzmacniają stanowczość",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Myślę że to, co powiedział nie jest prawdą.",
                correct="Myślę, że to, co powiedział, nie jest prawdą.",
                note="Zdanie podrzędne i wtrącenie wymagają przecinków; ich brak zmienia "
                "intonację.",
            ),
            GrammarMistake(
                wrong="To Annę podpisała umowę, nie Piotr.",
                correct="To Anna podpisała umowę, nie Piotr.",
                note="Wyróżniony podmiot pozostaje w mianowniku: Anna, nie Annę.",
            ),
        ],
        related=["szyk-wyrazow", "skladnia-retoryczna", "partykuly-niuans"],
    ),
    GrammarTopic(
        slug="frazeologia",
        title="Frazeologia: łączliwość i wariantywność",
        level="C2",
        category="Frazeologia",
        summary="Rozpoznawanie typów związków frazeologicznych i ich utrwalonej łączliwości.",
        explanation=(
            "**Frazeologizm** to utrwalony związek wyrazów o znaczeniu całościowym, "
            "odtwarzany z pamięci, a nie tworzony doraźnie.\n"
            "- **Związki stałe** (idiomy): *wyjść z siebie*, *mieć muchy w nosie* — znaczenie "
            "nie wynika ze składników.\n"
            "- **Związki łączliwe**: *poważna choroba*, *ciężkie przestępstwo* — "
            "dopuszczają ograniczoną wymianę składników.\n"
            "- **Związki luźne** graniczą ze zwykłą kolokacją.\n"
            "Frazeologizm ma **utrwaloną łączliwość**: *rzucać grochem o ścianę*, "
            "nie *w ścianę*. Warianty sprawdzamy w słowniku: obok *kruszyć kopie* "
            "notowane jest także *kruszyć kopię*.\n"
            "*Odtwarzalność* odróżnia idiom od metafory autorskiej: metaforę tworzymy, "
            "frazeologizm przywołujemy."
        ),
        structure=(
            "czasownik + stały rzeczownik w ustalonym przypadku " "(np. rzucać grochem o ścianę)"
        ),
        rules=[
            "Odtwarzalność i całościowe znaczenie to dwa kryteria idiomu.",
            "Nie wolno wymieniać składnika, jeśli związek jest stały.",
            "Wariantywność dotyczy tylko związków, które ją utrwaliły.",
            "Kontaminacja dwóch frazeologizmów to błąd, nie innowacja.",
        ],
        examples=[
            GrammarExample(
                text="Rzucał grochem o ścianę, tłumacząc mu to po raz trzeci.",
                translation=None,
                note="utrwalona łączliwość: o ścianę, nie w ścianę",
            ),
            GrammarExample(
                text="Kruszyć kopie o taką błahostkę to strata czasu.",
                translation=None,
                note="utrwalona postać z liczbą mnogą; słowniki notują też kruszyć kopię",
            ),
            GrammarExample(
                text="Wyciągnął do nas pomocną dłoń w najgorszym momencie.",
                translation=None,
                note="Utrwalony wariant: wyciągnąć do kogoś pomocną rękę.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Rzucał grochem w ścianę, tłumacząc mu to kolejny raz.",
                correct="Rzucał grochem o ścianę, tłumacząc mu to kolejny raz.",
                note="Frazeologizm utrwalił przyimek „o”, nie „w”.",
            ),
            GrammarMistake(
                wrong="Drużyna odniosła porażkę w finale.",
                correct="Drużyna poniosła porażkę w finale.",
                note="Kontaminacja związków „odnieść zwycięstwo” i „ponieść porażkę”.",
            ),
        ],
        related=["zwroty-idiomatyczne", "kolokacje", "przyslowia"],
    ),
    GrammarTopic(
        slug="przyslowia",
        title="Przysłowia i ich funkcja pragmatyczna",
        level="C2",
        category="Frazeologia",
        summary="Stosowanie paremii jako argumentu, komentarza i środka stylizacji.",
        explanation=(
            "**Przysłowie** należy do paremii — krótkich utworów o ustalonej postaci, "
            "przekazujących sąd ogólny. Jego siła argumentacyjna opiera się na **autorytecie "
            "tradycji**, nie na dowodzie.\n"
            "- Funkcja **perswazyjna**: przysłowie zamyka spór, zanim zostaną przedstawione "
            "racje.\n"
            "- Funkcja **rytualna**: w rozmowie nieoficjalnej buduje wspólnotę doświadczenia.\n"
            "- Funkcja **stylizacyjna**: w literaturze sygnalizuje wiejskość, dawność lub "
            "naiwność mówiącego.\n"
            "Przysłowie bywa **modyfikowane** dla efektu: *Nie ma dymu bez ognia, ale w tej "
            "sprawie dymu jest więcej niż ognia*. Taka gra wymaga, by odbiorca rozpoznał "
            "pierwowzór.\n"
            "W tekstach specjalistycznych przysłowie rzadko zastępuje analizę — pełni wtedy "
            "funkcję ozdobnika lub wymówki."
        ),
        structure="przysłowie + zdanie komentujące odniesienie do sytuacji",
        rules=[
            "Przysłowie jest sądem ogólnym, nie danymi o konkretnym przypadku.",
            "Modyfikacja działa tylko wtedy, gdy odbiorca zna pierwowzór.",
            "Paremii nie przypisuje się autorstwa.",
            "W tekstach formalnych przysłowie wymaga komentarza uzasadniającego.",
        ],
        examples=[
            GrammarExample(
                text="Gdzie kucharek sześć, tam nie ma co jeść — im więcej decydentów, "
                "tym gorszy efekt.",
                translation=None,
                note="przysłowie jako argument z tradycji",
            ),
            GrammarExample(
                text="Jak sobie pościelesz, tak się wyśpisz, więc nie dziw się, "
                "że projekt się rozsypał.",
                translation=None,
                note="funkcja oceniająca, lekko ironiczna",
            ),
            GrammarExample(
                text="Nie ma dymu bez ognia, ale w tej sprawie dymu jest więcej niż ognia.",
                translation=None,
                note="modyfikacja przysłowia jako komentarz",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Jak powiedział Mickiewicz: „Gdzie kucharek sześć, tam nie ma co jeść”.",
                correct="Jak mówi przysłowie: „Gdzie kucharek sześć, tam nie ma co jeść”.",
                note="Przysłowie nie ma autora; przypisanie go poecie to błąd atrybucji.",
            ),
            GrammarMistake(
                wrong=(
                    "W raporcie: „No cóż, jak sobie pościelesz, tak się wyśpisz, "
                    "więc dział IT jest sam sobie winien”."
                ),
                correct=(
                    "W raporcie: „Dział IT ponosi odpowiedzialność za skutki własnych działań”."
                ),
                note="Neutralna parafraza oceny; jej prawdziwość nadal wymaga uzasadnienia "
                "w raporcie. Redakcja nie pozwala dopisywać niepodanych przyczyn.",
            ),
        ],
        related=["frazeologia", "wyrazenia-utarte", "retoryka"],
    ),
    GrammarTopic(
        slug="wyrazenia-utarte",
        title="Wyrażenia utarte i formuły",
        level="C2",
        category="Stylistyka",
        summary="Sprawne posługiwanie się formułami grzecznościowymi, urzędowymi i medialnymi.",
        explanation=(
            "**Wyrażenia utarte** to formuły o wysokim stopniu skonwencjonalizowania: "
            "otwierają pismo, sygnalizują gatunek, regulują relację nadawcy i odbiorcy.\n"
            "- **Formuły grzecznościowe**: *Szanowni Państwo*, *Uprzejmie proszę*, "
            "*Z poważaniem*.\n"
            "- **Formuły urzędowe**: *W odpowiedzi na Państwa pismo*, *W związku z powyższym*, "
            "*W załączeniu przesyłam*.\n"
            "- **Formuły medialne**: *Jak wynika z danych*, *Warto podkreślić, że*.\n"
            "Formuła jest użyteczna, dopóki **coś znaczy**. *W związku z powyższym* wymaga, "
            "by wcześniej rzeczywiście coś wynikało; inaczej staje się pustym łącznikiem.\n"
            "*Szablon nie jest błędem* — błędem jest szablon zamiast treści."
        ),
        structure="W związku z + N (instr.) ... uprzejmie informuję, że ...",
        rules=[
            "Formuła otwarcia musi odpowiadać gatunkowi i relacji służbowej.",
            "Nie łączyć dwóch formuł o tej samej funkcji w jednym zdaniu.",
            "Unikać nadmiaru „niniejszy”, „przedmiotowy”, „w zakresie”.",
            "Formuła nie zwalnia z obowiązku podania konkretnej treści.",
        ],
        examples=[
            GrammarExample(
                text="W odpowiedzi na Państwa pismo z 3 marca uprzejmie informuję, "
                "że sprawa jest w toku.",
                translation=None,
                note="formuła otwarcia korespondencji urzędowej",
            ),
            GrammarExample(
                text="W załączeniu przesyłam podpisaną umowę.",
                translation=None,
                note="formuła załącznika bez pleonazmu",
            ),
            GrammarExample(
                text="Jak wynika z danych, sprzedaż wzrosła w trzecim kwartale.",
                translation=None,
                note="formuła wprowadzająca dane",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Niniejszym załączam załącznik do niniejszego pisma.",
                correct="W załączeniu przesyłam dokument.",
                note="Pleonazm „załączam załącznik” i nadmiar „niniejszy”.",
            ),
            GrammarMistake(
                wrong="Jak powszechnie wiadomo, wszyscy wiemy, że budżet jest napięty.",
                correct="Jak wiadomo, budżet jest napięty.",
                note="„Jak powszechnie wiadomo” i „wszyscy wiemy” mówią to samo.",
            ),
        ],
        related=["jezyk-prawny", "styl-formalny", "rejestr-jezykowy"],
    ),
    GrammarTopic(
        slug="aspekt-mistrzostwo",
        title="Aspekt czasownika w narracji",
        level="C2",
        category="Gramatyka",
        summary="Sterowanie aspektem w złożonej narracji, opisie nawyków i zdaniach zależnych.",
        explanation=(
            "**Aspekt** organizuje polską narrację: niedokonany przedstawia proces, nawyk "
            "i tło, dokonany — zdarzenie zamknięte i jego efekt.\n"
            "- **Tło i pierwszy plan**: *Kiedy czytałem raport, zadzwonił telefon*.\n"
            "- **Nawyk i jednostkowość**: *Codziennie pił kawę o siódmej* / *Wypił kawę "
            "i wyszedł*.\n"
            "- **Skutek i próba**: *przeczytać* (do końca) wobec *czytać* (w trakcie).\n"
            "Aspekt wchodzi w relacje z innymi kategoriami: czasowniki fazowe łączą się "
            "z niedokonanym (*zaczynać czytać*). Zakaz zwykle ma aspekt niedokonany "
            "(*Nie rób tego!*), a ostrzeżenie może mieć dokonany "
            "(*Nie zrób sobie krzywdy!*).\n"
            "*Kontrola aspektu* to nie dobór „ładniejszej” formy, lecz decyzja o tym, "
            "co odbiorca ma zobaczyć: **proces czy rezultat**."
        ),
        structure="niedokonany = tło, nawyk, proces; dokonany = zdarzenie punktowe, efekt",
        rules=[
            "Tło narracji buduje się czasownikami niedokonanymi.",
            "Nawyk zwykle ma aspekt niedokonany; aspekt dokonany może podkreślać "
            "kolejne rezultaty w serii zdarzeń.",
            "Czasowniki fazowe (zacząć, przestać) łączą się z bezokolicznikiem niedokonanym.",
            "Zakaz zwykle ma formę niedokonaną, lecz ostrzeżenie dopuszcza dokonaną.",
        ],
        examples=[
            GrammarExample(
                text="Kiedy czytałem raport, zadzwonił telefon.",
                translation=None,
                note="tło niedokonane i zdarzenie dokonane",
            ),
            GrammarExample(
                text="Codziennie pił kawę o siódmej, a tamtego dnia wypił ją w biegu.",
                translation=None,
                note="nawyk wobec jednostkowego faktu",
            ),
            GrammarExample(
                text="Nie zamykaj drzwi, ktoś jeszcze przyjdzie.",
                translation=None,
                note="zakaz wyrażony czasownikiem niedokonanym",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Zacząłem przeczytać gazetę przy śniadaniu.",
                correct="Zacząłem czytać gazetę przy śniadaniu.",
                note="Czasownik fazowy zacząć wymaga bezokolicznika niedokonanego.",
            ),
            GrammarMistake(
                wrong="Będę napiszę raport po konsultacji.",
                correct="Napiszę raport po konsultacji.",
                note="Forma dokonana napiszę tworzy przyszłość prostą bez będę.",
            ),
        ],
        related=["aspekt-pary", "aspekt-niuans", "czas-przeszly"],
    ),
    GrammarTopic(
        slug="tryby-mowione",
        title="Tryby w mowie: modalność i dystans",
        level="C2",
        category="Gramatyka",
        summary=(
            "Wykorzystywanie trybu rozkazującego, warunkowego i życzącego " "w funkcjach modalnych."
        ),
        explanation=(
            "Tryby w polszczyźnie pełnią funkcje **modalne**, nie tylko gramatyczne.\n"
            "- **Rozkaźnik** służy też grzeczności i namowie: *Niech Pan siada*, "
            "*Powiedzmy, że...*, *Niech mi Pan wybaczy*.\n"
            "- **Tryb warunkowy** tworzy dystans i przypuszczenie: *Byłoby wskazane, abyśmy "
            "przełożyli decyzję*, *Chciałbym zapytać*.\n"
            "- **Partykuła -by** wchodzi w skład spójników i form życzących: *żeby*, *gdyby*, "
            "*jakby*, *oby*.\n"
            "- **Tryb życzący** wyrażają konstrukcje z *oby* i *niech*: *Oby tylko zdążyli "
            "na pociąg*.\n"
            "Formy z *-bym*, *-byś* są **ruchome**: *Gdybym miał czas* / *Gdybym ja miał czas*. "
            "Nie wolno ich dublować: formy *gdybym bym* są błędem."
        ),
        structure="Niech + 3. os.; aby + bezokolicznik lub forma przeszła; -bym/-byś jako dystans",
        rules=[
            "Rozkaźnik z „niech” łagodzi polecenie i wyraża namowę.",
            "Tryb warunkowy służy do dystansowania się od twierdzenia.",
            "Formy z -by są ruchome, ale niedublowane.",
            "Oby łączy się z formą na -ł, np. oby zdążyli, obym zdążył, "
            "ale występuje też z bezokolicznikiem: Oby zdążyć na pociąg.",
        ],
        examples=[
            GrammarExample(
                text="Niech mi Pan wybaczy, ale muszę wrócić do tej kwestii.",
                translation=None,
                note="rozkaźnik w funkcji grzecznościowej",
            ),
            GrammarExample(
                text="Byłoby wskazane, abyśmy przełożyli decyzję o tydzień.",
                translation=None,
                note="tryb warunkowy jako dystans",
            ),
            GrammarExample(
                text="Oby tylko zdążyli na pociąg.",
                translation=None,
                note="tryb życzący z partykułą oby",
            ),
            GrammarExample(
                text="Oby zdążyć na pociąg.",
                translation=None,
                note="życzenie z bezokolicznikiem; forma osobowa: obym zdążył lub obym zdążyła",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gdybym bym miał czas, przyszedłbym na spotkanie.",
                correct="Gdybym miał czas, przyszedłbym na spotkanie.",
                note="Forma „gdybym” zawiera już partykułę -by.",
            ),
        ],
        related=["tryb-warunkowy", "tryb-rozka", "partykuly-modalne"],
    ),
    GrammarTopic(
        slug="formy-archaiczne",
        title="Formy archaiczne i książkowe",
        level="C2",
        category="Stylistyka",
        summary=(
            "Rozpoznawanie i świadome używanie archaizmów leksykalnych, fleksyjnych "
            "i składniowych."
        ),
        explanation=(
            "**Archaizmy** to elementy starszej warstwy języka, dziś odczuwane jako książkowe, "
            "ceremonialne lub komiczne.\n"
            "- **Leksykalne**: *przeto*, *wszelako*, *zaiste*, *jeno*.\n"
            "- **Fleksyjne**: dawne formy przypadków i końcówki osobowe (*iżeś*, *był-ci*).\n"
            "- **Składniowe**: *jako iż*, dawny szyk *rzekł Bóg*.\n"
            "Archaizm bywa **środkiem stylizacji**: w powieści historycznej buduje patynę "
            "epoki, w modlitwie jest naturalny, w mailu służbowym brzmi pretensjonalnie.\n"
            "*Warunek skuteczności*: konsekwencja. Jeden archaizm w zdaniu współczesnym "
            "wygląda jak błąd, cała warstwa — jak decyzja stylistyczna."
        ),
        structure="ów + N; przeto / wszelako / zaiste + zdanie",
        rules=[
            "Archaizm musi być rozpoznany jako archaizm, nie jako zwykły wyraz.",
            "Stylizacja wymaga konsekwencji w całym tekście.",
            "Nie używać archaizmów w tekstach użytkowych bez wyraźnej funkcji.",
            "Nie mylić archaizmu z błędem fleksyjnym.",
        ],
        examples=[
            GrammarExample(
                text="Przeto nie godzi się sądzić pochopnie.",
                translation=None,
                note="przeto = dlatego; rejestr książkowy",
            ),
            GrammarExample(
                text="Wszelako racje obu stron zasługują na uwagę.",
                translation=None,
                note="wszelako = jednak",
            ),
            GrammarExample(
                text="Zaiste, trudno o lepszy przykład.",
                translation=None,
                note="zaiste wyłącznie w stylizacji",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wszelako jednak nie zgadzam się z tą oceną.",
                correct="Wszelako nie zgadzam się z tą oceną.",
                note="„Wszelako” znaczy „jednak”; połączenie obu jest tautologią.",
            ),
            GrammarMistake(
                wrong="Ów mężczyzna, o którym mówiłem, ów był moim szefem.",
                correct="Ów mężczyzna, o którym mówiłem, był moim szefem.",
                note="„Ów” nie pełni funkcji zaimka anaforycznego w podmiocie.",
            ),
        ],
        related=["jezyk-prawny", "styl-formalny", "srodki-stylistyczne"],
    ),
    GrammarTopic(
        slug="jezyk-prawny",
        title="Język prawny i prawniczy",
        level="C2",
        category="Język specjalistyczny",
        summary="Czytanie i redagowanie tekstów normatywnych z zachowaniem precyzji zakresu.",
        explanation=(
            "**Język prawny** to język tekstów normatywnych; **język prawniczy** to metajęzyk "
            "ich opisu. Pierwszy stanowi prawo, drugi o prawie mówi.\n"
            "- **Performatywność**: *niniejszym oświadczam*, *zobowiązuję się* — wypowiedzenie "
            "tworzy skutek.\n"
            "- **Modalność normatywna**: *ma obowiązek*, *może*, *nie może*, *jest obowiązany*.\n"
            "- **Definicje legalne**: *W rozumieniu niniejszej ustawy...* wiążą w całym akcie.\n"
            "- **Odesłania i domniemania**: *Z zastrzeżeniem ust. 2*, *uważa się za zachowany*.\n"
            "Precyzja wymaga **stałości terminologicznej**: jeśli termin zdefiniowano raz, "
            "nie wolno używać go później w innym znaczeniu. Zasada ta koliduje z postulatem "
            "zrozumiałości — dlatego teksty prawne bywają długie i powtarzalne."
        ),
        structure="kto + [czyn] + podlega + [sankcja]",
        rules=[
            "Termin zdefiniowany raz zachowuje znaczenie w całym akcie.",
            "Modalność wyraża się zwrotami „jest obowiązany”, „może”, „nie może”.",
            "Zakres normy wyznaczają warunki i odesłania, nie domysł odbiorcy.",
            "Zakaz wykładni synonimicznej: różne terminy mają różne znaczenia.",
        ],
        examples=[
            GrammarExample(
                text="Kto bez uprawnienia wchodzi na teren objęty zakazem, podlega karze "
                "grzywny.",
                translation=None,
                note="norma z sankcją, teraźniejszość normatywna",
            ),
            GrammarExample(
                text="W rozumieniu niniejszej umowy „dzień roboczy” oznacza dzień "
                "od poniedziałku do piątku.",
                translation=None,
                note="definicja legalna",
            ),
            GrammarExample(
                text="Z zastrzeżeniem ust. 2, termin uważa się za zachowany, jeżeli "
                "przesyłkę nadano przed jego upływem.",
                translation=None,
                note="odesłanie i domniemanie",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Klient jest obowiązany do zapłata w terminie 14 dni, chyba że strony "
                "postanowią inaczej.",
                correct="Klient jest obowiązany do zapłaty w terminie 14 dni, chyba że strony "
                "postanowią inaczej.",
                note="Do wymaga dopełniacza zapłaty. Korekta językowa zachowuje termin "
                "i wyjątek przewidziany w zdaniu wyjściowym.",
            ),
            GrammarMistake(
                wrong="Za szkodę odpowiadają pracodawca oraz pracownik który wyrządził szkodę.",
                correct="Za szkodę odpowiadają pracodawca oraz pracownik, który wyrządził szkodę.",
                note="Przecinek wydziela zdanie względne. To przykład redakcji, nie opis "
                "obowiązującego prawa; nie zmieniamy podmiotów ani zakresu odpowiedzialności.",
            ),
        ],
        related=["terminologia", "definicje-precyzja", "wyrazenia-utarte"],
    ),
    GrammarTopic(
        slug="jezyk-naukowy",
        title="Język naukowy",
        level="C2",
        category="Język specjalistyczny",
        summary="Redagowanie tekstu badawczego z zachowaniem hedgingu, cytowania i struktury.",
        explanation=(
            "**Język naukowy** dąży do intersubiektywnej sprawdzalności: czytelnik musi móc "
            "odtworzyć tok rozumowania i ocenić jego podstawy.\n"
            "- **Nominalizacje i konstrukcje bezosobowe** przenoszą uwagę z badacza na "
            "przedmiot: *przeprowadzono analizę*, *w literaturze przyjmuje się*.\n"
            "- **Hedging** ogranicza siłę twierdzeń do zakresu danych: *dane sugerują*, "
            "*można przypuszczać*, *wyniki wskazują*.\n"
            "- **Cytowanie i przypisy** lokują twierdzenie w dyskursie i oddzielają cudze "
            "wyniki od własnych.\n"
            "- **Struktura IMRaD** porządkuje artykuł: wstęp, metody, wyniki, dyskusja.\n"
            "*Granica*: ostrożność nie może zastąpić uzasadnienia. Wniosek może być "
            "ostrożny, ale trzeba wskazać dane, na których się opiera, oraz jego ograniczenia."
        ),
        structure="dane sugerują, że + zdanie; w literaturze przyjmuje się, że + zdanie",
        rules=[
            "Ograniczać twierdzenia do zakresu zbadanej próby.",
            "Oddzielać wynik własny od wyniku cytowanego.",
            "Dobierać osobę gramatyczną do konwencji dyscypliny i czasopisma; "
            "pierwsza osoba nie jest ogólnie zakazana.",
            "Zastrzeżenia formułować wprost, nie w domyśle.",
        ],
        examples=[
            GrammarExample(
                text="Uzyskane dane sugerują, że zależność ma charakter nieliniowy.",
                translation=None,
                note="hedging: sugerują, nie dowodzą",
            ),
            GrammarExample(
                text="W literaturze przedmiotu dominuje stanowisko, zgodnie z którym "
                "efekt wynika z doboru próby.",
                translation=None,
                note="wprowadzenie cudzego stanowiska",
            ),
            GrammarExample(
                text="Niniejsze badanie ma charakter pilotażowy; jego wyniki wymagają "
                "replikacji.",
                translation=None,
                note="zastrzeżenie zakresu wniosków",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Uważam, że wszyscy wiedzą, że to rozwiązanie działa.",
                correct="Uważam, że to rozwiązanie działa.",
                note="Usunięto nieuzasadnione wszyscy wiedzą. To nadal opinia wymagająca "
                "dowodów; nie wolno zastępować jej twierdzeniem o danych, których nie podano.",
            ),
            GrammarMistake(
                wrong="Badania zostały przeprowadzone przez badaczy, którzy przebadali "
                "200 osób.",
                correct="Badacze przebadali 200 osób.",
                note="Uproszczenie stylistyczne usuwa powtórzenie bez dopisywania dat "
                "ani innych informacji.",
            ),
        ],
        related=[
            "nominalizacja-zaawansowana",
            "konstrukcje-bezosobowe-zaawansowane",
            "definicje-precyzja",
        ],
    ),
    GrammarTopic(
        slug="definicje-precyzja",
        title="Definicje i precyzja pojęciowa",
        level="C2",
        category="Semantyka",
        summary=(
            "Budowanie definicji poprawnych logicznie i wystarczających "
            "do rozstrzygania przypadków."
        ),
        explanation=(
            "**Definicja** ustala znaczenie terminu na użytek tekstu. Definicja **nominalna** "
            "wprowadza termin (*Przez „klienta” rozumie się...*), **realna** opisuje przedmiot.\n"
            "Klasyczna struktura: *definiendum* + łącznik + *genus proximum* + *differentia "
            "specifica*, czyli termin, klasa nadrzędna i cecha odróżniająca.\n"
            "- *Klient to osoba fizyczna, która zawarła umowę za pośrednictwem serwisu.*\n"
            "Błędy: **circulus in definiendo** (*innowacja to coś innowacyjnego*), definicja "
            "**za szeroka** lub **za wąska**, **ignotum per ignotum**, definicja przez przykład.\n"
            "**Precyzja** wymaga też kwantyfikacji i wskazania warunków: *wszyscy*, "
            "*niektórzy*, *co najmniej*, *wyłącznie*. Bez nich definicja nie pozwala "
            "rozstrzygać przypadków granicznych."
        ),
        structure="X to [genus proximum], który [differentia specifica]",
        rules=[
            "Definicja nie może zawierać terminu definiowanego.",
            "Zakres definicji musi pokrywać się z zakresem terminu — ani szerzej, ani wężej.",
            "Terminy obce w definicji wymagają wcześniejszego objaśnienia.",
            "Przykład ilustruje definicję, ale jej nie zastępuje.",
        ],
        examples=[
            GrammarExample(
                text="Klient to osoba fizyczna, która zawarła umowę za pośrednictwem serwisu.",
                translation=None,
                note="genus proximum + differentia specifica",
            ),
            GrammarExample(
                text="Przez „dane osobowe” rozumie się informacje o zidentyfikowanej lub "
                "możliwej do zidentyfikowania osobie fizycznej.",
                translation=None,
                note="definicja nominalna",
            ),
            GrammarExample(
                text="Lęk to stan emocjonalny charakteryzujący się przewlekłym napięciem, "
                "którego źródło nie jest jednoznacznie określone.",
                translation=None,
                note="definicja realna",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Sprawiedliwość to wtedy, gdy każdy dostaje to, na co zasługuje.",
                correct=(
                    "Sprawiedliwość to zasada rozdzielania dóbr i obowiązków "
                    "proporcjonalnie do zasług."
                ),
                note="Definicja przez okoliczność nie podaje genus proximum.",
            ),
            GrammarMistake(
                wrong="Innowacja to nowatorskie rozwiązanie, czyli coś innowacyjnego.",
                correct=(
                    "Innowacja to wdrożone rozwiązanie nowe w danej organizacji, "
                    "przynoszące wymierną zmianę."
                ),
                note="Circulus in definiendo: termin wyjaśniany własnym derywatem.",
            ),
        ],
        related=["definiowanie", "jezyk-naukowy", "jezyk-prawny"],
    ),
    GrammarTopic(
        slug="retoryka",
        title="Retoryka: kompozycja i figury",
        level="C2",
        category="Retoryka",
        summary="Budowanie mowy według części retorycznych i stosowanie figur z umiarem.",
        explanation=(
            "**Retoryka** to sztuka wypowiedzi skutecznej i stosownej. Klasyczny podział "
            "wyróżnia **inventio** (znalezienie treści), **dispositio** (układ), "
            "**elocutio** (kształt językowy), **memoria** i **actio**.\n"
            "Kompozycja mowy: **exordium** (zjednanie odbiorcy), **narratio** (przedstawienie "
            "stanu rzeczy), **argumentatio** (dowody i odparcie), **peroratio** (puenta i apel).\n"
            "- **Figury** działają przez powtórzenie i kontrast: anafora, antyteza, triada, "
            "gradacja, pytanie retoryczne.\n"
            "- **Apostrofa** to bezpośredni, często uroczysty zwrot do osoby, zbiorowości, "
            "przedmiotu lub pojęcia, np. *Wolności, nie pozwól nam o sobie zapomnieć!*. "
            "Adresat nie musi być obecny; taki zwrot może wzmacniać emocjonalny ton apelu.\n"
            "- **Decorum** nakazuje dobór środków do tematu, odbiorcy i okoliczności.\n"
            "*Skuteczność* nie jest tym samym co ozdobność: jedna dobrze umieszczona anafora "
            "waży więcej niż dziesięć figur w akapicie."
        ),
        structure="exordium → narratio → argumentatio → peroratio",
        rules=[
            "Każda część mowy ma inne zadanie i inny rytm.",
            "Figura musi wzmacniać argument, nie zastępować go.",
            "Apostrofa ustanawia bezpośredniego adresata wypowiedzi, także gdy jest nim "
            "osoba nieobecna lub pojęcie abstrakcyjne.",
            "Etos mówcy buduje się na początku, nie w puencie.",
            "Peroracja zamyka myśl, ale nie dodaje nowych argumentów.",
        ],
        examples=[
            GrammarExample(
                text="Nie chodzi o to, kto ma rację. Chodzi o to, kto ma odwagę przyznać "
                "się do błędu.",
                translation=None,
                note="paralelizm i antyteza",
            ),
            GrammarExample(
                text="Przeanalizowaliśmy dane, wysłuchaliśmy ekspertów, przygotowaliśmy plan.",
                translation=None,
                note="triada z gradacją",
            ),
            GrammarExample(
                text="Czy naprawdę chcemy, żeby nasze dzieci dorastały w świecie, w którym "
                "nikt nie odpowiada za słowa?",
                translation=None,
                note="pytanie retoryczne w peroracji",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Im więcej figur retorycznych w akapicie, tym mowa skuteczniejsza.",
                correct="Skuteczna mowa używa figur oszczędnie, w miejscach kluczowych "
                "dla argumentu.",
                note="Nadmiar środków narusza decorum i rozprasza odbiorcę.",
            ),
            GrammarMistake(
                wrong="Exordium najlepiej zacząć od wyznania: „Nie mam pojęcia, o czym mówić”.",
                correct="Exordium powinno budować zaufanie: wskazywać kompetencję "
                "i wspólny cel.",
                note="Błąd kompozycji: osłabienie etosu mówcy w otwarciu.",
            ),
        ],
        related=["skladnia-retoryczna", "srodki-stylistyczne", "argumentacja-zaawansowana"],
    ),
    GrammarTopic(
        slug="argumentacja-zaawansowana",
        title="Argumentacja: struktura i siła",
        level="C2",
        category="Retoryka",
        summary="Ocenianie i budowanie argumentów w modelu Toulmina, z odparciem i koncesją.",
        explanation=(
            "**Argumentacja** to jawne powiązanie tezy z przesłankami. Model Toulmina rozbija "
            "je na **tezę**, **dane**, **uzasadnienie** (warrant), **poparcie**, "
            "**kwalifikator** i **odparcie**.\n"
            "- **Kontrargument** atakuje przesłankę lub uzasadnienie, nie osobę.\n"
            "- **Koncesja** uznaje część racji przeciwnika i zwiększa wiarygodność: *Owszem, "
            "koszty rosną, ale...*\n"
            "- **Ciężar dowodu** spoczywa na tym, kto formułuje twierdzenie: *Proszę wskazać, "
            "które procedury znosimy*.\n"
            "Typowe błędy: **słomiana kukła**, **fałszywa dychotomia**, **petitio principii**, "
            "**argument z autorytetu bez źródła**, **post hoc**.\n"
            "*Siła argumentu* zależy od jakości przesłanek i od tego, czy wniosek nie wykracza "
            "poza to, co z nich wynika."
        ),
        structure="teza + dane + uzasadnienie + zastrzeżenie + odparcie",
        rules=[
            "Każda teza wymaga wskazania przesłanek, na których się opiera.",
            "Koncesja nie osłabia stanowiska, jeśli jest ograniczona i szczera.",
            "Kwalifikator („z reguły”, „w większości przypadków”) chroni przed uogólnieniem.",
            "Odpierając zarzut, trzeba odtworzyć jego najmocniejszą wersję.",
        ],
        examples=[
            GrammarExample(
                text="Owszem, koszty rosną, ale w wartościach bezwzględnych pozostają niższe "
                "niż straty z tytułu przestojów.",
                translation=None,
                note="koncesja i kontrargument",
            ),
            GrammarExample(
                text="Argument z analogii jest tu słaby: oba rynki różnią się skalą "
                "i regulacjami.",
                translation=None,
                note="ocena uzasadnienia",
            ),
            GrammarExample(
                text="Kto twierdzi, że ograniczenie biurokracji rozwiąże problem, musi "
                "wskazać, które procedury znosi.",
                translation=None,
                note="ciężar dowodu po stronie twierdzącej",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Skoro mój rozmówca jest prawnikiem, jego zdanie o gospodarce jest "
                "niewiarygodne.",
                correct="Argument należy oceniać ze względu na przesłanki i wnioskowanie, "
                "nie na cechy osoby.",
                note="Ad hominem: atak na osobę zamiast na argument.",
            ),
            GrammarMistake(
                wrong="Albo przyjmujemy cały pakiet, albo rezygnujemy z reformy.",
                correct="Pakiet można przyjąć częściowo; warto rozważyć warianty pośrednie.",
                note="Fałszywa dychotomia: pominięcie opcji trzeciej.",
            ),
        ],
        related=["retoryka", "manipulacja-jezykowa", "spojniki-zaawansowane"],
    ),
    GrammarTopic(
        slug="manipulacja-jezykowa",
        title="Manipulacja językowa",
        level="C2",
        category="Pragmatyka",
        summary=(
            "Rozpoznawanie presupozycji, ramowania i ukrywania sprawcy "
            "w wypowiedziach publicznych."
        ),
        explanation=(
            "**Manipulacja językowa** nie kłamie wprost — narzuca odbiorcy założenia i ramy "
            "oceny.\n"
            "- **Presupozycja**: *Czy nadal zamierza Pan wprowadzać w błąd?* — pytanie "
            "zakłada fakt, którego nie udowodniono.\n"
            "- **Nominalizacja i strona bierna bez sprawcy**: *Dokonano optymalizacji "
            "zatrudnienia* — znika ten, kto decydował.\n"
            "- **Ramowanie**: *ulga dla przedsiębiorców* zamiast *obniżka podatku* ustawia "
            "ocenę z góry.\n"
            "- **Eufemizm**: *redukcja zatrudnienia*, *elastyczne formy pracy*.\n"
            "- **Autorytet bez źródła**: *eksperci twierdzą*, *jak powszechnie wiadomo*.\n"
            "Obrona nie polega na podejrzliwości wobec każdego zdania, lecz na "
            "**rekonstrukcji założeń**: co ta wypowiedź każe mi przyjąć, zanim cokolwiek "
            "sprawdzę?"
        ),
        structure="presupozycja + ramowanie + nominalizacja bez sprawcy",
        rules=[
            "Oddzielać treść zdania od założeń, które ono narzuca.",
            "Pytanie może być twierdzeniem w przebraniu — sprawdzać presupozycje.",
            "Forma gramatyczna sama w sobie nie jest manipulacją; liczy się funkcja.",
            "Nazwanie mechanizmu jest skuteczniejszą obroną niż ogólna nieufność.",
        ],
        examples=[
            GrammarExample(
                text="Dokonano optymalizacji zatrudnienia.",
                translation=None,
                note="nominalizacja i eufemizm ukrywają sprawcę",
            ),
            GrammarExample(
                text="Czy nadal zamierza Pan wprowadzać w błąd opinię publiczną?",
                translation=None,
                note="pytanie z presupozycją",
            ),
            GrammarExample(
                text="Oczywiście każdy rozsądny człowiek to popiera.",
                translation=None,
                note="presupozycja wspólnoty i wykluczenie sprzeciwu",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wystarczy słowo „eksperci”, by uznać argument za rozstrzygający.",
                correct="Argument z autorytetu wymaga wskazania źródła, kompetencji "
                "i zgodności opinii w dziedzinie.",
                note="Autorytet bez źródła to chwyt erystyczny, nie dowód.",
            ),
            GrammarMistake(
                wrong="Każde zdanie w stronie biernej jest manipulacją.",
                correct="Strona bierna bywa neutralna; manipulacją staje się wtedy, gdy "
                "celowo ukrywa sprawcę.",
                note="Nadinterpretacja: forma gramatyczna nie jest chwytem sama w sobie.",
            ),
        ],
        related=["retoryka", "argumentacja-zaawansowana", "strona-bierna-styl"],
    ),
    GrammarTopic(
        slug="trudnosci-przekladu",
        title="Trudności przekładu",
        level="C2",
        category="Przekład",
        summary="Rozpoznawanie luk leksykalnych, kolokacyjnych i kulturowych oraz dobór strategii.",
        explanation=(
            "**Trudność przekładowa** pojawia się tam, gdzie systemy językowe nie pokrywają "
            "się: w leksyce, składni, konotacjach i realiach.\n"
            "- **Luka leksykalna**: *załatwić sprawę* zależy od kontekstu — *sort something "
            "out*, *pull strings*, *get it done*.\n"
            "- **Odmienny podział pola semantycznego**: polskie *kombinować* obejmuje sensy, "
            "których angielskie *combine* nie ma.\n"
            "- **Konotacje i rejestr**: *spuścić z tonu* ma odcień ustępstwa, *back off* — "
            "także wycofania się.\n"
            "- **Gra słów, rym, rytm**: często nieprzenośne bez kompensacji.\n"
            "Strategie: **ekwiwalent funkcjonalny**, **opis**, **zapożyczenie** z "
            "objaśnieniem, **kompensacja** w innym miejscu tekstu.\n"
            "*Kalka* jest rozwiązaniem najsłabszym: zachowuje formę obcą, gubiąc funkcję "
            "rodzimą."
        ),
        structure="oryginał → ekwiwalent funkcjonalny (+ przypis, jeśli realia)",
        rules=[
            "Ustalić funkcję fragmentu, zanim wybierze się ekwiwalent.",
            "Nie tłumaczyć idiomu dosłownie, jeśli istnieje utrwalony odpowiednik.",
            "Realia objaśniać przypisem lub opisem, nie cudzysłowem.",
            "Straty w jednym miejscu kompensować w innym, nie wszędzie naraz.",
        ],
        examples=[
            GrammarExample(
                text="PL: załatwić sprawę — EN: to sort something out / to pull strings.",
                translation=None,
                note="ekwiwalent zależny od kontekstu",
            ),
            GrammarExample(
                text="PL: spuścić z tonu — EN: to climb down.",
                translation=None,
                note="ekwiwalent funkcjonalny, nie dosłowny",
            ),
            GrammarExample(
                text="PL: Tłusty czwartek — EN: Fat Thursday (nazwa wymaga objaśnienia).",
                translation=None,
                note="realia kulturowe",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Angielskie „It's raining cats and dogs” → „Pada kotami i psami”.",
                correct="„Leje jak z cebra”.",
                note="Dosłowny przekład gubi funkcję idiomatyczną.",
            ),
            GrammarMistake(
                wrong="„Zrobić sens” jako odpowiednik „to make sense”.",
                correct="„Mieć sens”.",
                note="Kalka składniowa; poprawny związek to „mieć sens”.",
            ),
        ],
        related=["kalki-jezykowe", "ekwiwalencja", "frazeologia"],
    ),
    GrammarTopic(
        slug="kalki-jezykowe",
        title="Kalki językowe",
        level="C2",
        category="Przekład",
        summary=(
            "Wykrywanie dosłownych odwzorowań obcych struktur i zastępowanie ich "
            "formami rodzimymi."
        ),
        explanation=(
            "**Kalka** to dosłowne odwzorowanie obcej formy: leksykalne (*dedykowany zespół*), "
            "składniowe (*adresować problem*) lub semantyczne (rozszerzenie znaczenia pod "
            "wpływem obcego wyrazu).\n"
            "Kalki bywają **pożyteczne**, gdy wypełniają realną lukę i przyjmują się w uzusie; "
            "bywają **szkodliwe**, gdy wypierają istniejący, precyzyjniejszy środek rodzimy.\n"
            "- *dedykowany* → *przeznaczony*, *specjalnie powołany*\n"
            "- *adresować problem* → *odnosić się do problemu*, *rozwiązywać problem*\n"
            "- *robić różnicę* → *mieć znaczenie*\n"
            "Rozstrzyga **łączliwość i rejestr**: jeśli kalka wymaga niepolskich związków "
            "(*dokonać decyzji*), jest błędem, a nie innowacją."
        ),
        structure="kalka: [obcy wzór] → [poprawna forma rodzima]",
        rules=[
            "Sprawdzać, czy wyraz ma polską łączliwość, zanim uzna się go za poprawny.",
            "Kalka utrwalona w uzusie nie jest błędem, ale wymaga świadomej oceny.",
            "Nie zastępować precyzyjnego terminu rodzimego modnym odpowiednikiem obcym.",
            "Kalki składniowe ujawniają się w przypadkach i przyimkach.",
        ],
        examples=[
            GrammarExample(
                text="Adresujemy problemy zgłoszone przez klientów.",
                translation=None,
                note="kalka „address the issue”",
            ),
            GrammarExample(
                text="Dla klientów kluczowych powstał dedykowany zespół wsparcia.",
                translation=None,
                note="kalka „dedicated team”; lepiej: zespół przeznaczony dla...",
            ),
            GrammarExample(
                text="To robi różnicę.",
                translation=None,
                note="kalka „make a difference”; lepiej: to ma znaczenie",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Dokonano decyzji o zmianie harmonogramu.",
                correct="Podjęto decyzję o zmianie harmonogramu.",
                note="Poprawna kolokacja to „podjąć decyzję”; „dokonać” łączy się m.in. "
                "z „analizy”, „wpisu”.",
            ),
            GrammarMistake(
                wrong="Zespół fokusuje się na wynikach kwartalnych.",
                correct="Zespół skupia się na wynikach kwartalnych.",
                note="Kalka „to focus on”; „fokusować się” jest potoczne i nadużywane.",
            ),
        ],
        related=["trudnosci-przekladu", "ekwiwalencja", "dobor-slow"],
    ),
    GrammarTopic(
        slug="ekwiwalencja",
        title="Ekwiwalencja w przekładzie",
        level="C2",
        category="Przekład",
        summary="Ocenianie przekładu na poziomie znaczenia, funkcji, stylu i pragmatyki.",
        explanation=(
            "**Ekwiwalencja** to zgodność przekładu z oryginałem na poziomie **znaczenia, "
            "funkcji, stylu i pragmatyki**. Ekwiwalencja formalna naśladuje strukturę, "
            "dynamiczna — wywołuje u odbiorcy analogiczną reakcję.\n"
            "- **Leksykalna**: *dąb* — *oak*.\n"
            "- **Gramatyczna**: polskiego aspektu nie da się oddać jednym angielskim czasem; "
            "różnicę przejmuje kontekst.\n"
            "- **Pragmatyczna**: *Dzień dobry* o osiemnastej to *Good evening*, nie *Good day*.\n"
            "- **Stylistyczna**: rejestr oryginału musi zostać zachowany, nawet jeśli środki "
            "są inne.\n"
            "Dylemat **egzotyzacji i udomowienia**: *Jan* pozostaje *Janem* albo staje się "
            "*Johnem* — decyzja zależy od funkcji tekstu, nie od wierności słowu."
        ),
        structure="funkcja tekstu → środek języka docelowego (nie: słowo → słowo)",
        rules=[
            "Ekwiwalencja dotyczy całości tekstu, nie pojedynczych wyrazów.",
            "Zachowanie funkcji ma pierwszeństwo przed zachowaniem formy.",
            "Decyzje translatorskie trzeba umieć uzasadnić wobec odbiorcy.",
            "Spójność terminologiczna obowiązuje w całym przekładzie.",
        ],
        examples=[
            GrammarExample(
                text="PL: Przeczytałem tę książkę wczoraj. — EN: I read this book yesterday.",
                translation=None,
                note="aspekt dokonany oddany przez kontekst",
            ),
            GrammarExample(
                text="PL: Dzień dobry (o 18:00) — EN: Good evening.",
                translation=None,
                note="ekwiwalencja pragmatyczna",
            ),
            GrammarExample(
                text="PL: Jan — EN: John (udomowienie) lub Jan (egzotyzacja).",
                translation=None,
                note="decyzja translatorska",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wierny przekład to przekład dosłowny.",
                correct="Wierność dotyczy sensu i funkcji tekstu, nie liczby zachowanych słów.",
                note="Dosłowność często niszczy ekwiwalencję pragmatyczną.",
            ),
            GrammarMistake(
                wrong="Ekwiwalent musi mieć ten sam rodzaj gramatyczny i liczbę co oryginał.",
                correct="Ekwiwalent dobiera się ze względu na funkcję w tekście, a nie cechy "
                "formalne.",
                note="Formalizm prowadzi do nienaturalnych rozwiązań.",
            ),
        ],
        related=["trudnosci-przekladu", "kalki-jezykowe", "metafora-jezykowa"],
    ),
    GrammarTopic(
        slug="regionalizmy",
        title="Regionalizmy i odmiany terytorialne",
        level="C2",
        category="Socjolingwistyka",
        summary="Odróżnianie regionalizmów od form ogólnopolskich, gwar i błędów językowych.",
        explanation=(
            "**Regionalizm** to cecha językowa właściwa danemu terytorium, poprawna w obrębie "
            "jego normy użytkowej. Nie jest tym samym co **gwara** (mowa ludności wiejskiej) "
            "ani **dialekt** (odmiana o własnym systemie).\n"
            "- **Leksykalne**: *tytka* (torebka) w Wielkopolsce, *kartofle* (ziemniaki), "
            "*szneka z glancem* (drożdżówka).\n"
            "- **Fonetyczne**: regionalne różnice w wymowie połączeń między wyrazami.\n"
            "- **Składniowe**: *na polu* w znaczeniu *na dworze*, m.in. w Małopolsce.\n"
            "Norma wzorcowa nie unieważnia regionalizmów, ale ogranicza ich użycie poza "
            "regionem. W tekście literackim regionalizm bywa **stylizacją**, w dokumentacji "
            "technicznej — źródłem nieporozumień."
        ),
        structure="forma ogólnopolska ↔ regionalizm (zasięg terytorialny)",
        rules=[
            "Regionalizm nie staje się błędem poza regionem; jego stosowność zależy "
            "od rejestru i zrozumiałości dla odbiorcy.",
            "Gwara, dialekt i regionalizm to trzy różne pojęcia.",
            "Odstępstwo od normy wzorcowej nie zawsze jest regionalizmem.",
            "W tekstach użytkowych regionalizm wymaga uzasadnienia funkcją.",
        ],
        examples=[
            GrammarExample(
                text="Kup mi dwie tytki, bo torba mi się rozdarła.",
                translation=None,
                note="Poznań: tytka = torebka",
            ),
            GrammarExample(
                text="Na polu jest zimno, weź kurtkę.",
                translation=None,
                note="m.in. Małopolska: na polu = na dworze",
            ),
            GrammarExample(
                text="Kupiłem sznekę z glancem do kawy.",
                translation=None,
                note="Wielkopolska: szneka z glancem = drożdżówka z lukrem",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Regionalizmy to błędy językowe.",
                correct="Regionalizmy to cechy odmiany terytorialnej; ich stosowność "
                "zależy od sytuacji i odbiorcy.",
                note="Wartościowanie odmian nie jest oceną językoznawczą.",
            ),
            GrammarMistake(
                wrong="„Włanczać” to regionalizm.",
                correct="„Włanczać” to błąd wymawianiowy; poprawna forma to „włączać”.",
                note="Odstępstwo od normy wzorcowej nie jest regionalizmem.",
            ),
        ],
        related=["jezyk-potoczny", "intonacja-znaczenie", "rejestr-jezykowy"],
    ),
    GrammarTopic(
        slug="jezyk-potoczny",
        title="Język potoczny",
        level="C2",
        category="Socjolingwistyka",
        summary="Świadome posługiwanie się elipsą, partykułami i ekspresją mowy codziennej.",
        explanation=(
            "**Język potoczny** to podstawowa odmiana mowy codziennej: nieoficjalna, "
            "bezpośrednia, nastawiona na kontakt.\n"
            "- **Elipsa**: *Idziesz?* zamiast *Czy idziesz na spotkanie?*\n"
            "- **Partykuły**: *no*, *chyba*, *przecież*, *normalnie* — regulują stosunek "
            "mówiącego do treści.\n"
            "- **Ekspresja słowotwórcza**: *pośpiewaliśmy*, *nakupował*, *kawusia*.\n"
            "- **Funkcja fatyczna**: *No i co tam?* podtrzymuje kontakt, nie przekazuje "
            "informacji.\n"
            "Potoczność nie jest błędem — jest **rejestrem**. Błędem staje się w gatunkach, "
            "które wymagają dystansu: w podaniu, umowie, artykule naukowym.\n"
            "*Wartość C2*: umiejętność przełączania między rejestrami bez utraty precyzji."
        ),
        structure="partykuła + elipsa + prefiks ekspresywny (np. po- + bezokolicznik)",
        rules=[
            "Potoczność jest dopuszczalna tylko w sytuacjach nieoficjalnych.",
            "Partykuły modalne niosą postawę mówiącego, nie treść.",
            "Elipsa nie może prowadzić do niejednoznaczności.",
            "Formy ekspresywne z prefiksami są poprawne i rejestrowane w słownikach.",
        ],
        examples=[
            GrammarExample(
                text="No i co, ogarnąłeś ten projekt? Bo wiesz, ja mam urwanie głowy.",
                translation=None,
                note="partykuły, elipsa, leksyka potoczna",
            ),
            GrammarExample(
                text="Normalnie masakra, nie spodziewałem się, że tak wyjdzie.",
                translation=None,
                note="wzmocnienie i ekspresja",
            ),
            GrammarExample(
                text="Poszliśmy na miasto, pośpiewaliśmy, pośmialiśmy się — fajnie było.",
                translation=None,
                note="prefiks po- jako wykładnik ekspresji",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong=(
                    "W podaniu: „No więc piszę, żebyście mi dali urlop, " "bo mam urwanie głowy”."
                ),
                correct="Proszę o udzielenie mi urlopu z powodu nadmiaru obowiązków.",
                note="Zmiana rejestru zachowuje podaną prośbę i uzasadnienie. Termin "
                "oraz rodzaj urlopu trzeba ustalić, nie dopisywać w parafrazie.",
            ),
            GrammarMistake(
                wrong="Formy „pośmiać się”, „pogadać” są niepoprawne.",
                correct="Prefiks „po-” wnosi znaczenie „trochę, przez chwilę” i jest "
                "w pełni poprawny.",
                note="Ekspresywne formacje prefiksalne należą do normy.",
            ),
        ],
        related=["partykuly-niuans", "rejestr-jezykowy", "regionalizmy"],
    ),
    GrammarTopic(
        slug="intonacja-znaczenie",
        title="Intonacja i akcent zdaniowy",
        level="C2",
        category="Fonetyka",
        summary="Wykorzystywanie akcentu i konturu intonacyjnego jako nośników znaczenia.",
        explanation=(
            "**Akcent wyrazowy** w polszczyźnie pada zwykle na przedostatnią sylabę "
            "(*RA-port*, *ko-BIE-ta*). Wyjątki obejmują formy czasu przeszłego z *-śmy*, "
            "*-ście* (*zro-BI-liś-my*), zapożyczenia typu *re-TO-ry-ka* oraz nazwy typu "
            "*Rzecz-po-SPO-li-ta*.\n"
            "**Akcent zdaniowy** wyznacza człon kontrastowany i zmienia implikaturę:\n"
            "- *TO była jego decyzja.* — wyróżnienie tej właśnie decyzji.\n"
            "- *To była JEGO decyzja.* — podkreślenie właściciela.\n"
            "**Kontur intonacyjny**: opadający dla oznajmień, rosnący dla pytań ogólnych, "
            "rosnąco-opadający dla rezerwy i niedowierzania.\n"
            "*Przecinek bywa nośnikiem intonacji*: *Nie, dziękuję* (odmowa) różni się od "
            "*Nie dziękuję* układem pauz i akcentów."
        ),
        structure="opadający = oznajmienie; rosnący = pytanie; akcent na członie kontrastowanym",
        rules=[
            "Akcent wyrazowy pada na przedostatnią sylabę, z nielicznymi wyjątkami.",
            "Akcent zdaniowy przenosi się na człon kontrastowany.",
            "Pytania ogólne mają kontur rosnący, pytania szczegółowe — opadający.",
            "Pauza i przecinek zmieniają znaczenie wypowiedzi.",
        ],
        examples=[
            GrammarExample(
                text="To była jego decyzja, nie moja.",
                translation=None,
                note="akcent zdaniowy na „jego”",
            ),
            GrammarExample(
                text="Przyszedłeś?",
                translation=None,
                note="pytanie ogólne z intonacją rosnącą",
            ),
            GrammarExample(
                text="Nie, dziękuję.",
                translation=None,
                note="przecinek i kontur opadający sygnalizują odmowę",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Akcent w języku polskim pada zawsze na ostatnią sylabę wyrazu.",
                correct="Akcent pada zwykle na przedostatnią sylabę; wyjątki to m.in. formy "
                "z -śmy, -ście i nieliczne zapożyczenia.",
                note="Mylenie polszczyzny z językami o akcencie końcowym.",
            ),
            GrammarMistake(
                wrong="Intonacja nie wpływa na znaczenie, bo liczy się tylko treść słów.",
                correct="Ten sam ciąg słów z innym akcentem zdaniowym niesie inną " "implikaturę.",
                note="Prozodia jest nośnikiem znaczenia pragmatycznego.",
            ),
        ],
        related=["partykuly-modalne", "skladnia-emfatyczna", "jezyk-potoczny"],
    ),
]
