"""Polish grammar topics — B2."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="tryb-warunkowy-hipotetyczny",
        title="Tryb warunkowy hipotetyczny",
        level="B2",
        category="Tryb warunkowy",
        summary="Zdania warunkowe o sytuacjach nierealnych w teraźniejszości i przeszłości.",
        explanation=(
            "**Tryb warunkowy hipotetyczny** opisuje sytuacje, które nie zachodzą "
            "lub nie zaszły.\n"
            "- Teraźniejszość i przyszłość: *Gdybym miał więcej czasu, uczyłbym się "
            "gry na pianinie.*\n"
            "- Przeszłość: *Gdyby wtedy powiedział prawdę, uniknęlibyśmy kryzysu.*\n\n"
            "Warunek wprowadza **gdyby** z końcówką osobową (gdybym, gdybyś, gdyby, "
            "gdybyśmy, gdybyście, gdyby), a skutek — forma przeszła z cząstką **by**: "
            "*uczyłbym się*, *uniknęlibyśmy*. Czas przeszły w obu członach jest zwykle "
            "taki sam; o tym, czy "
            "sytuacja dotyczy teraźniejszości, czy przeszłości, decyduje kontekst."
        ),
        structure="gdyby + forma przeszła, forma przeszła + by (z końcówką osobową)",
        rules=[
            "Gdyby wprowadza hipotezę; możliwe są też jeśli lub jeżeli z trybem "
            "przypuszczającym: jeśli miałbyś czas, moglibyśmy porozmawiać.",
            "Nie dublujemy by przy jednym orzeczeniu: gdybym miał, poszedłbym.",
            "Skutek wyraża forma przeszła z cząstką by: przyszłabym, przyszlibyśmy.",
            "O przeszłości decyduje kontekst: wtedy, rok temu, wówczas.",
        ],
        examples=[
            GrammarExample(
                text="Gdybym miał więcej czasu, uczyłbym się gry na pianinie.",
                translation=None,
            ),
            GrammarExample(
                text="Gdyby wtedy powiedział prawdę, uniknęlibyśmy kryzysu.",
                translation=None,
            ),
            GrammarExample(
                text="Gdybyśmy wynajęli większe biuro, zespół pracowałby wygodniej.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gdybym bym miał więcej czasu, przeczytałbym tę książkę.",
                correct="Gdybym miał więcej czasu, przeczytałbym tę książkę.",
                note="Cząstka by jest już zawarta w formie gdybym; podwójne by jest błędem.",
            ),
            GrammarMistake(
                wrong="Gdybym miał wtedy czas, przychodzę na spotkanie.",
                correct="Gdybym miał wtedy czas, przyszedłbym na spotkanie.",
                note="W zdaniu nadrzędnym potrzebna jest forma przeszła z by, a nie "
                "czas teraźniejszy.",
            ),
        ],
        related=[
            "tryb-warunkowy-przeszly",
            "zdania-warunkowe-mieszane",
            "tryb-warunkowy-zdania",
        ],
    ),
    GrammarTopic(
        slug="zdania-przeciwstawne",
        title="Zdania przeciwstawne",
        level="B2",
        category="Składnia",
        summary="Zestawianie treści różniących się lub ograniczających się wzajemnie.",
        explanation=(
            "**Zdania przeciwstawne** łączą dwie treści, które się różnią albo wzajemnie "
            "ograniczają.\n"
            "- *Wprawdzie pada, ale idziemy na spacer.*\n"
            "- *Ona woli góry, natomiast on wybiera morze.*\n"
            "- *Ja pracuję w biurze, podczas gdy ty pracujesz zdalnie.*\n\n"
            "**Wprawdzie** otwiera człon ustępujący i wymaga w drugiej części **ale** lub "
            "**jednak**. **Natomiast** i **zaś** zestawiają odrębne podmioty albo stany. "
            "**Podczas gdy** wprowadza zdanie podrzędne i nie łączy się z dodatkowym **a**."
        ),
        structure="wprawdzie A, ale B | A, natomiast B | A, podczas gdy B",
        rules=[
            "Wprawdzie wymaga w drugim członie spójnika ale lub jednak.",
            "Natomiast i zaś zestawiają różne podmioty, stany lub oceny.",
            "Podczas gdy wprowadza zdanie podrzędne i nie wymaga spójnika a.",
            "Przeciwieństwo w obrębie jednego podmiotu wyraża raczej ale lub jednak.",
        ],
        examples=[
            GrammarExample(
                text="Wprawdzie ceny wzrosły, ale popyt się nie zmienił.",
                translation=None,
            ),
            GrammarExample(
                text="Kandydat mówił spokojnie, natomiast jego rozmówca podnosił głos.",
                translation=None,
            ),
            GrammarExample(
                text="Ja wolę pracę w zespole, podczas gdy ona pracuje najlepiej w ciszy.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Jest zmęczony, natomiast idzie do pracy.",
                correct="Jest zmęczony, ale idzie do pracy.",
                note="Natomiast zestawia różne podmioty lub stany; przy jednym podmiocie "
                "naturalne jest ale albo jednak.",
            ),
            GrammarMistake(
                wrong="Podczas gdy ona czyta, a ja gotuję.",
                correct="Podczas gdy ona czyta, ja gotuję.",
                note="Podczas gdy jest spójnikiem podrzędnym i nie wymaga dodatkowego a.",
            ),
        ],
        related=["zdania-ustepstwowe", "spojniki-zaawansowane", "skladnia-zlozona"],
    ),
    GrammarTopic(
        slug="partykuly-modalne",
        title="Partykuły modalne",
        level="B2",
        category="Partykuły",
        summary="Stopniowanie pewności i oznaczanie źródła informacji za pomocą partykuł.",
        explanation=(
            "**Partykuły modalne** wyrażają stosunek mówiącego do treści zdania.\n"
            "- Wysoka pewność: *niewątpliwie*, *z pewnością*, *zapewne*\n"
            "- Przypuszczenie: *prawdopodobnie*, *chyba*, *pewnie*\n"
            "- Informacja cudza: *podobno* (neutralnie), *rzekomo* (z dystansem)\n\n"
            "Partykuła nie jest częścią zdania i nie oddziela się przecinkiem: *Podobno "
            "wyjechał na rok.* **Rzekomo** sugeruje, że mówiący nie bierze odpowiedzialności "
            "za prawdziwość informacji, a nawet w nią wątpi."
        ),
        structure="partykuła modalna + zdanie oznajmujące",
        rules=[
            "Zapewne i niewątpliwie wyrażają wysoką pewność mówiącego.",
            "Chyba i pewnie sygnalizują przypuszczenie, często z nutą wahania.",
            "Podobno przekazuje informację zasłyszaną bez potwierdzenia.",
            "Rzekomo dystansuje się od treści i podsuwa wątpliwość.",
        ],
        examples=[
            GrammarExample(
                text="Zapewne spotkanie potrwa dłużej, niż planowano.",
                translation=None,
            ),
            GrammarExample(text="Chyba nie zdążyliśmy na ostatni autobus.", translation=None),
            GrammarExample(text="Rzekomo umowa została już podpisana.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Podobno, że wyjechał na rok.",
                correct="Podobno wyjechał na rok.",
                note="Podobno nie wprowadza zdania podrzędnego, więc nie stawia się po nim "
                "przecinka ani spójnika że.",
            ),
            GrammarMistake(
                wrong="Zapewne, że przyjdzie przed obiadem.",
                correct="Zapewne przyjdzie przed obiadem.",
                note="Zapewne jest partykułą i łączy się bezpośrednio z orzeczeniem.",
            ),
        ],
        related=["partykuly-zaawansowane", "partykuly"],
    ),
    GrammarTopic(
        slug="nominalizacja",
        title="Nominalizacja",
        level="B2",
        category="Słowotwórstwo",
        summary="Zamiana czasowników i przymiotników w rzeczowniki w tekstach formalnych.",
        explanation=(
            "**Nominalizacja** zamienia czasownik lub przymiotnik w rzeczownik.\n"
            "- *przeanalizować → analiza*, *przeprowadzić analizę*\n"
            "- *wzrosnąć → wzrost*\n"
            "- *zatrudnić → zatrudnienie*\n"
            "- *dostępny → dostępność*\n\n"
            "Konstrukcje nominalne są typowe dla raportów i pism urzędowych: *W wyniku audytu "
            "stwierdzono konieczność obniżenia kosztów.* Nominalizacja może zmieniać przypadek "
            "dopełnienia: *obniżyć koszty* (biernik) → *obniżenie kosztów* (dopełniacz). "
            "Inne zależności mogą pozostać: *pomagać dzieciom → pomaganie dzieciom*."
        ),
        structure="czasownik → rzeczownik na -nie, -cie, -acja, -ość + dopełniacz",
        rules=[
            "Dopełnienie biernikowe często staje się dopełniaczem: obniżyć koszty → "
            "obniżenie kosztów.",
            "Formy na -nie i -cie tworzy się od tematu czasownika: zatrudnić → zatrudnienie.",
            "Nominalizacja zagęszcza tekst, ale jej nadmiar utrudnia czytanie.",
            "W tekście formalnym wybieraj nominalizację, gdy ważniejszy jest sam fakt "
            "niż wykonawca.",
        ],
        examples=[
            GrammarExample(
                text="Wzrost zatrudnienia w sektorze usług utrzymał się przez cały rok.",
                translation=None,
            ),
            GrammarExample(
                text="Po przeprowadzeniu analizy danych zespół przedstawił rekomendacje.",
                translation=None,
            ),
            GrammarExample(
                text="Podjęcie decyzji o inwestycji wymaga zgody zarządu.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="obniżenie koszty produkcji",
                correct="obniżenie kosztów produkcji",
                note="Po obniżenie używamy dopełniacza kosztów, choć obniżyć wymaga biernika koszty.",
            ),
            GrammarMistake(
                wrong="Nastąpiło zwiększenie się liczby wniosków o dwadzieścia procent.",
                correct="Liczba wniosków wzrosła o dwadzieścia procent.",
                note="Uproszczenie stylistyczne, nie błąd gramatyczny: czasownik przekazuje "
                "tę samą informację zwięźlej.",
            ),
        ],
        related=["nominalizacja-zaawansowana", "konstrukcje-imienne", "rzeczowniki-odczasownikowe"],
    ),
    GrammarTopic(
        slug="strona-bierna-zaawansowana",
        title="Strona bierna zaawansowana",
        level="B2",
        category="Strona bierna",
        summary="Strona bierna z czasownikami modalnymi, w czasach złożonych i z wykonawcą.",
        explanation=(
            "**Strona bierna** z **być** opisuje stan, a z **zostać** — zakończoną "
            "czynność.\n"
            "- *Raport jest przechowywany w archiwum.* (stan)\n"
            "- *Raport został wysłany wczoraj.* (czynność zakończona)\n\n"
            "Z czasownikami modalnymi: *Dokument musi zostać zatwierdzony przez kierownika.* "
            "W czasie przyszłym: *Wniosek będzie rozpatrzony w ciągu miesiąca.*\n\n"
            "Wykonawcę wprowadza **przez** z biernikiem, a narzędzie — **przy pomocy** "
            "z dopełniaczem: *Drzwi otwarto przy pomocy wytrycha.*"
        ),
        structure="być / zostać + imiesłów bierny (+ przez + biernik)",
        rules=[
            "Być z imiesłowem biernym opisuje stan lub czynność trwającą.",
            "Zostać z imiesłowem biernym podkreśla zakończony rezultat.",
            "Imiesłów zgadza się z podmiotem w rodzaju i liczbie.",
            "Wykonawcę wyraża konstrukcja przez + biernik.",
        ],
        examples=[
            GrammarExample(
                text="Decyzja musi zostać zatwierdzona przez komisję.",
                translation=None,
            ),
            GrammarExample(
                text="Dokumenty są przechowywane w archiwum zakładowym.",
                translation=None,
            ),
            GrammarExample(
                text="Wniosek będzie rozpatrzony na najbliższym posiedzeniu.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Decyzja musi zostać zatwierdzona przez komisji.",
                correct="Decyzja musi zostać zatwierdzona przez komisję.",
                note="Przyimek przez łączy się z biernikiem, nie z dopełniaczem.",
            ),
            GrammarMistake(
                wrong="Raport został wysłany przez dyrektor.",
                correct="Raport został wysłany przez dyrektora.",
                note="Biernik rzeczownika męskiego żywotnego ma końcówkę -a.",
            ),
        ],
        related=["strona-bierna", "strona-bierna-czas", "strona-bierna-styl"],
    ),
    GrammarTopic(
        slug="konstrukcje-bezosobowe-zaawansowane",
        title="Konstrukcje bezosobowe zaawansowane",
        level="B2",
        category="Konstrukcje bezosobowe",
        summary="Formy bez wskazania wykonawcy w regulaminach, instrukcjach i tekstach naukowych.",
        explanation=(
            "**Konstrukcje bezosobowe** pozwalają mówić o czynności bez wskazywania "
            "wykonawcy.\n"
            "- *Należy zauważyć, że...* (obowiązek)\n"
            "- *Wymaga się złożenia dokumentów.* (wymóg formalny)\n"
            "- *Zaleca się wcześniejsze zgłoszenie.* (rekomendacja)\n"
            "- *Można przypuszczać, że...* (możliwość)\n\n"
            "Są typowe dla instrukcji, regulaminów i tekstów naukowych. W mowie "
            "potocznej brzmią sztywno, dlatego w rozmowie lepiej użyć form osobowych."
        ),
        structure=(
            "należy / trzeba / można / wymaga się / zaleca się + bezokolicznik " "lub dopełniacz"
        ),
        rules=[
            "Wymaga się i zakazuje się łączą się z dopełniaczem.",
            "Należy, można i trzeba stoją przed bezokolicznikiem.",
            "Konstrukcje z się nie mają podmiotu i nie odmieniają się przez osoby.",
            "Rejestr formalny wymaga tych form w procedurach i regulaminach.",
        ],
        examples=[
            GrammarExample(
                text="Należy zauważyć, że dane pochodzą z różnych źródeł.",
                translation=None,
            ),
            GrammarExample(
                text="Wymaga się złożenia wniosku do końca miesiąca.",
                translation=None,
            ),
            GrammarExample(
                text="Zaleca się, aby dokumenty dostarczyć osobiście.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wymaga się złożenie dokumentów.",
                correct="Wymaga się złożenia dokumentów.",
                note="Czasownik wymagać, także w formie wymaga się, rządzi dopełniaczem.",
            ),
            GrammarMistake(
                wrong="Można się zauważyć, że wyniki są zaniżone.",
                correct="Można zauważyć, że wyniki są zaniżone.",
                note="Możliwość wyraża sama forma można; dodawanie się jest zbędne.",
            ),
        ],
        related=[
            "konstrukcje-bezosobowe",
            "strona-bierna-zaawansowana",
            "styl-formalny",
        ],
    ),
    GrammarTopic(
        slug="imieslowy-zaawansowane",
        title="Imiesłowy zaawansowane",
        level="B2",
        category="Imiesłowy",
        summary="Imiesłowy przysłówkowe i przymiotnikowe w zdaniach skróconych i naukowych.",
        explanation=(
            "**Imiesłowy przysłówkowe** skracają zdania podrzędne, gdy oba zdania mają "
            "ten sam podmiot.\n"
            "- współczesny na **-ąc**: *Czytając raport, robił notatki.*\n"
            "- uprzedni na **-wszy / -łszy**: *Przeczytawszy raport, napisał recenzję.*\n\n"
            "**Imiesłów przymiotnikowy bierny** (-ny, -ty, -ony) tworzy stronę bierną i "
            "przydawki: *badanie przeprowadzone w 2024 roku*. Imiesłów czynny (-ący, -ąca) "
            "opisuje wykonawcę czynności, także chwilowej: *uczący się student*."
        ),
        structure="temat czasownika + -ąc (współczesny) / -wszy, -łszy (uprzedni)",
        rules=[
            "Imiesłów przysłówkowy wymaga tego samego podmiotu w obu zdaniach.",
            "Forma na -ąc opisuje czynność równoczesną wobec nadrzędnej.",
            "Forma na -wszy lub -łszy opisuje czynność wcześniejszą.",
            "Imiesłów przymiotnikowy bierny zgadza się z rzeczownikiem w rodzaju i liczbie.",
        ],
        examples=[
            GrammarExample(
                text="Analizując dane, zespół dostrzegł wyraźny trend.",
                translation=None,
            ),
            GrammarExample(
                text="Przeczytawszy recenzję, autor poprawił dwa rozdziały.",
                translation=None,
            ),
            GrammarExample(
                text="Badania przeprowadzone w 2024 roku potwierdziły hipotezę.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Idąc do domu, zaczęło padać.",
                correct="Kiedy szedłem do domu, zaczęło padać.",
                note="Imiesłów przysłówkowy wymaga wspólnego podmiotu; tutaj podmioty " "są różne.",
            ),
            GrammarMistake(
                wrong="Przeczytając książkę, napisałem recenzję.",
                correct="Przeczytawszy książkę, napisałem recenzję.",
                note="Od dokonanego przeczytać tworzymy przeczytawszy, nie przeczytając. "
                "Forma uprzednia wskazuje, że lektura poprzedziła napisanie recenzji.",
            ),
        ],
        related=[
            "imieslow-przymiotnikowy",
            "imieslow-przyslowkowy",
            "strona-bierna-zaawansowana",
        ],
    ),
    GrammarTopic(
        slug="zdania-wielokrotne",
        title="Zdania wielokrotnie złożone",
        level="B2",
        category="Składnia",
        summary="Łączenie kilku zdań podrzędnych w spójną wypowiedź z poprawną składnią.",
        explanation=(
            "**Zdania wielokrotnie złożone** zawierają trzy lub więcej zdań składowych.\n"
            "- *Sądzę, że projekt, który przedstawiono wczoraj, zostanie przyjęty, o ile nie "
            "zabraknie środków.*\n\n"
            "Kolejne zdania podrzędne oddziela się przecinkami. Przed spójnikiem **i**, który "
            "łączy równorzędne zdania podrzędne, przecinka nie stawiamy: *Wiem, że "
            "przyszedł i że przeprosił.* Zdania tego samego stopnia powinny mieć "
            "równoległą budowę."
        ),
        structure="zdanie nadrzędne + kolejne zdania podrzędne różnych stopni",
        rules=[
            "Każde zdanie podrzędne oddziela się przecinkiem od nadrzędnego.",
            "Przed spójnikiem i, który łączy równorzędne zdania podrzędne, przecinka "
            "nie stawiamy.",
            "Zdania podrzędne tego samego stopnia powinny mieć równoległą budowę.",
            "Zbyt długie zdanie warto rozbić, zachowując relacje logiczne.",
        ],
        examples=[
            GrammarExample(
                text="Sądzę, że projekt, który przedstawiono wczoraj, zostanie przyjęty.",
                translation=None,
            ),
            GrammarExample(text="Wiem, że przyszedł i że przeprosił.", translation=None),
            GrammarExample(
                text="Kiedy komisja zakończyła obrady, okazało się, że brakuje " "jednego głosu.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wiem że przyszedł, i że przeprosił.",
                correct="Wiem, że przyszedł i że przeprosił.",
                note="Przecinek stawiamy po zdaniu nadrzędnym, a nie przed i łączącym "
                "równorzędne zdania podrzędne.",
            ),
            GrammarMistake(
                wrong="Sądzę, że projekt który przedstawiono wczoraj zostanie przyjęty.",
                correct="Sądzę, że projekt, który przedstawiono wczoraj, zostanie przyjęty.",
                note="Zdanie podrzędne względne trzeba wydzielić przecinkami z obu stron.",
            ),
        ],
        related=["skladnia-zlozona", "zdania-okolicznikowe", "zdania-z-ze"],
    ),
    GrammarTopic(
        slug="mowa-zalezna-zaawansowana",
        title="Mowa zależna zaawansowana",
        level="B2",
        category="Mowa zależna",
        summary="Przekazywanie twierdzeń, pytań i poleceń z dostosowaniem zaimków i czasu.",
        explanation=(
            "**Mowa zależna** przekazuje cudzą wypowiedź bez cytowania.\n"
            "- Twierdzenie: *Powiedział, że projekt jest gotowy.*\n"
            "- Pytanie: *Zapytała, czy zdążymy na spotkanie.*\n"
            "- Prośba i rozkaz: *Poprosił, żebyśmy przyszli wcześniej.*\n\n"
            "W polszczyźnie nie ma sztywnej zgodności czasów: *Powiedział, że jest "
            "zmęczony* i *Powiedział, że był zmęczony* różnią się perspektywą, nie "
            "poprawnością. Trzeba natomiast przestawić zaimki i okoliczniki czasu: "
            "*jutro → następnego dnia*."
        ),
        structure="czasownik mówienia + że / czy / żeby + zdanie podrzędne",
        rules=[
            "Twierdzenia wprowadza że lub iż po czasowniku mówienia.",
            "Pytania zależne wprowadza czy, bez znaku zapytania na końcu.",
            "Prośby i rozkazy oddaje konstrukcja żeby + forma przeszła.",
            "Zaimki i okoliczniki czasu trzeba dostosować do sytuacji mówienia.",
        ],
        examples=[
            GrammarExample(text="Twierdził, że badanie zostało zakończone.", translation=None),
            GrammarExample(text="Zapytała, czy dane są już dostępne.", translation=None),
            GrammarExample(
                text="Poprosił, żebyśmy nie rozgłaszali tej informacji.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Zapytał, że czy przyjdzie.",
                correct="Zapytał, czy przyjdzie.",
                note="Pytanie zależne wprowadza samo czy, bez że i bez znaku zapytania.",
            ),
            GrammarMistake(
                wrong="Poprosił, aby przyszedłby wcześniej.",
                correct="Poprosił, aby przyszedł wcześniej.",
                note="Po aby nie powtarza się cząstki by w orzeczeniu zdania podrzędnego.",
            ),
        ],
        related=["mowa-zalezna", "mowa-zalezna-styl", "zdania-z-ze"],
    ),
    GrammarTopic(
        slug="szyk-wyrazow",
        title="Szyk wyrazów",
        level="B2",
        category="Szyk zdania",
        summary="Świadome sterowanie kolejnością składniową dla tematu, rematu i emfazy.",
        explanation=(
            "**Szyk wyrazów** w polszczyźnie jest swobodny, ale nie dowolny: zmiana kolejności "
            "zmienia nacisk i temat zdania.\n"
            "- Neutralnie: *Anna czyta raport.*\n"
            "- Emfatycznie: *Raport czyta Anna.* (właśnie Anna, nie kto inny)\n"
            "- Temat na początku: *Ten raport Anna czyta od tygodnia.*\n\n"
            "Krótkie nieakcentowane formy zaimków, np. mi, ci, go, oraz **się** "
            "nie stoją na początku neutralnego zdania: "
            "*Spóźniłem się*, nie *Się spóźniłem*."
        ),
        structure="temat (znane) + remat (nowe), enklityki przy czasowniku",
        rules=[
            "Na końcu zdania stoi zwykle nowa, najważniejsza informacja.",
            "Enklityki mi, ci, go, się nie rozpoczynają zdania.",
            "Przeczenie nie stoi bezpośrednio przed tym, co neguje.",
            "Przydawka jakościowa zwykle poprzedza rzeczownik, a klasyfikująca może stać "
            "po nim: ciekawy wykład, język polski.",
        ],
        examples=[
            GrammarExample(text="Raport czyta Anna, nie Piotr.", translation=None),
            GrammarExample(text="Spóźniłem się na wykład.", translation=None),
            GrammarExample(text="To właśnie ten argument przekonał komisję.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Się spóźniłem na wykład.",
                correct="Spóźniłem się na wykład.",
                note="Się jest enklityką i nie może rozpoczynać zdania.",
            ),
            GrammarMistake(
                wrong="Mi przekazano dokumenty, nie tobie.",
                correct="Mnie przekazano dokumenty, nie tobie.",
                note="Na początku zdania i w kontraście używamy akcentowanej formy mnie.",
            ),
        ],
        related=["inwersja", "elipsa", "skladnia-retoryczna"],
    ),
    GrammarTopic(
        slug="inwersja",
        title="Inwersja",
        level="B2",
        category="Szyk zdania",
        summary="Przestawnia szyku dla emfazy w narracji, wystąpieniach i tekstach literackich.",
        explanation=(
            "**Inwersja** to przestawnia szyku, która służy emfazie i budowaniu napięcia.\n"
            "- *Nigdy nie zapomnę tamtego wieczoru.*\n"
            "- *Zaledwie wszedł, sala zamilkła.*\n"
            "- *Nie tylko o pieniądze tu chodzi.*\n\n"
            "Inaczej niż w angielszczyźnie, w polszczyźnie inwersja nie jest obowiązkowa po "
            "przeczeniu. Wysunięcie elementu na początek zmienia rozkład tematu i rematu, "
            "a jego naturalność zależy od kontekstu i intonacji."
        ),
        structure="element emfatyczny + orzeczenie + reszta zdania",
        rules=[
            "Element wysunięty na początek zyskuje nacisk i staje się tematem.",
            "Nigdy nie wymusza inwersji: Nigdy Anna tego nie powiedziała jest poprawne.",
            "Nie tylko... ale także wymaga równoległej budowy obu członów.",
            "Przestawienie szyku może służyć kontrastowi także w codziennej rozmowie.",
        ],
        examples=[
            GrammarExample(text="Nigdy nie zapomnę pierwszego dnia w pracy.", translation=None),
            GrammarExample(
                text="Zaledwie zamknął drzwi, rozległ się telefon.",
                translation=None,
            ),
            GrammarExample(
                text="O wyniku decydują nie tylko szybkość, ale i precyzja.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Nigdy zapomnę tamtego wieczoru.",
                correct="Nigdy nie zapomnę tamtego wieczoru.",
                note="Wysunięte nigdy nie zastępuje przeczenia nie przy orzeczeniu.",
            ),
            GrammarMistake(
                wrong="Ten argumentów przekonał komisję.",
                correct="Ten argument przekonał komisję.",
                note="Wysunięcie elementu nie zmienia jego przypadku: podmiot pozostaje "
                "w mianowniku, ten argument.",
            ),
        ],
        related=["szyk-wyrazow", "skladnia-retoryczna", "retoryka"],
    ),
    GrammarTopic(
        slug="elipsa",
        title="Elipsa",
        level="B2",
        category="Składnia",
        summary="Pomijanie elementów odtwarzalnych z kontekstu w dialogu i nagłówkach.",
        explanation=(
            "**Elipsa** to pominięcie elementu, który odbiorca odtworzy z kontekstu.\n"
            "- *Ja do kina, a ty do domu.* (pominięte idę)\n"
            "- *Kawa? – Poproszę.* (pominięte chcę kawę)\n"
            "- *Kto przyszedł? – Anna.* (pominięte przyszła)\n\n"
            "Elipsa jest naturalna w dialogu, nagłówkach i notatkach. W tekstach formalnych "
            "bywa ryzykowna, bo zatarta informacja może zmienić sens zobowiązania."
        ),
        structure="zdanie niepełne, uzupełniane z kontekstu",
        rules=[
            "Pomijaj tylko to, co odbiorca jednoznacznie odtworzy.",
            "W dialogu elipsa orzeczenia jest normą.",
            "W tekście urzędowym unikaj elipsy, która zaciera warunki lub obowiązki.",
            "Zdania eliptyczne zachowują interpunkcję pełnego zdania.",
        ],
        examples=[
            GrammarExample(text="Ja do kina, a ty do domu.", translation=None),
            GrammarExample(text="Kawa czy herbata? – Herbata.", translation=None),
            GrammarExample(text="Spotkanie o ósmej? – Tak, o ósmej.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Z powodu opóźnienia odwołano, a pasażerowie czekali.",
                correct="Z powodu opóźnienia odwołano lot, a pasażerowie czekali.",
                note="Pominięcie dopełnienia zaciera sens; elipsa musi być odtwarzalna "
                "z kontekstu.",
            ),
            GrammarMistake(
                wrong="Spotkanie odbędzie o ósmej.",
                correct="Spotkanie odbędzie się o ósmej.",
                note="Nie pomijaj się w czasownikach zwrotnych; odbędzie bez się jest błędem.",
            ),
        ],
        related=["szyk-wyrazow", "skladnia-zlozona"],
    ),
    GrammarTopic(
        slug="spojniki-zaawansowane",
        title="Spójniki zaawansowane",
        level="B2",
        category="Spójniki",
        summary="Precyzyjne oznaczanie warunku, przyczyny, skutku i przeciwstawienia.",
        explanation=(
            "**Spójniki zaawansowane** nazywają relację logiczną między zdaniami.\n"
            "- warunek z ograniczeniem: *o ile*, *pod warunkiem że*\n"
            "- przeciwstawienie: *podczas gdy*, *tymczasem*, *zaś*\n"
            "- przyczyna: *bowiem*, *albowiem*\n"
            "- skutek: *zatem*, *w związku z tym*, *dlatego*\n\n"
            "**Bowiem** stoi po pierwszym składniku zdania: *Nie przyszedł, był bowiem chory.* "
            "Nie otwiera wypowiedzi, w odróżnieniu od *ponieważ* i *dlatego że*."
        ),
        structure="zdanie + spójnik + zdanie (ze stałą pozycją spójnika)",
        rules=[
            "O ile i pod warunkiem że wprowadzają warunek konieczny.",
            "Bowiem zwykle stoi wewnątrz członu przyczynowego; albowiem może go "
            "otwierać: Nie przyszedł, albowiem był chory.",
            "Zatem i w związku z tym sygnalizują wniosek lub skutek.",
            "Zaś i tymczasem zestawiają treści, nie wyrażając przyczyny.",
        ],
        examples=[
            GrammarExample(text="Przyjdę, o ile zdążę skończyć raport.", translation=None),
            GrammarExample(text="Odwołano spotkanie, nie było bowiem kworum.", translation=None),
            GrammarExample(
                text="W związku z tym, że brakuje danych, wniosek odłożono.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Bowiem nie było kworum, odwołano spotkanie.",
                correct="Odwołano spotkanie, nie było bowiem kworum.",
                note="Bowiem nie otwiera zdania; stoi po pierwszym składniku.",
            ),
            GrammarMistake(
                wrong="Zostajemy w domu ponieważ pada.",
                correct="Zostajemy w domu, ponieważ pada.",
                note="Zdanie podrzędne przyczynowe oddzielamy przecinkiem od nadrzędnego.",
            ),
        ],
        related=["zdania-przeciwstawne", "zdania-przyczynowe", "zdania-ustepstwowe"],
    ),
    GrammarTopic(
        slug="zdania-ustepstwowe",
        title="Zdania ustępstwowe",
        level="B2",
        category="Zdania podrzędne",
        summary="Przyznawanie faktów, które nie podważają głównej tezy wypowiedzi.",
        explanation=(
            "**Zdania ustępstwowe** przyznają fakt, który nie zmienia głównego twierdzenia.\n"
            "- *Chociaż pada, idziemy na spacer.*\n"
            "- *Mimo że był zmęczony, dokończył raport.*\n"
            "- *Nawet gdyby zaproponowano mi awans, nie przyjąłbym go.*\n\n"
            "Uwaga na rekcję: **mimo** i **pomimo** łączą się z dopełniaczem (*mimo "
            "deszczu*), a **mimo że** i **pomimo że** — ze zdaniem. Po członie "
            "ustępowym nie powtarza się spójnika **ale**."
        ),
        structure="chociaż / mimo że / pomimo że + zdanie, zdanie nadrzędne",
        rules=[
            "Chociaż, choć i aczkolwiek wprowadzają zdanie podrzędne ustępujące.",
            "Mimo że i pomimo że wymagają zdania, a mimo i pomimo dopełniacza.",
            "W zdaniu z ustępstwem nie powtarza się spójnika ale.",
            "Nawet gdyby wyraża ustępstwo hipotetyczne.",
        ],
        examples=[
            GrammarExample(
                text="Chociaż zabrakło czasu, zespół dowiózł projekt.",
                translation=None,
            ),
            GrammarExample(text="Mimo zmęczenia pracowała do późna.", translation=None),
            GrammarExample(
                text="Nawet gdyby zaproponowano mi awans, nie przyjąłbym go.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mimo że deszczu wyszliśmy na spacer.",
                correct="Mimo deszczu wyszliśmy na spacer.",
                note="Mimo łączy się z dopełniaczem; wersja ze zdaniem wymaga formy mimo że.",
            ),
            GrammarMistake(
                wrong="Chociaż był zmęczony, ale dokończył raport.",
                correct="Chociaż był zmęczony, dokończył raport.",
                note="Po zdaniu ustępowym nie powtarza się spójnika ale.",
            ),
        ],
        related=[
            "zdania-przeciwstawne",
            "spojniki-zaawansowane",
            "tryb-warunkowy-hipotetyczny",
        ],
    ),
    GrammarTopic(
        slug="przyimki-zaawansowane",
        title="Przyimki zaawansowane",
        level="B2",
        category="Przyimki",
        summary="Abstrakcyjne konstrukcje przyimkowe i ich stała rekcja przypadkowa.",
        explanation=(
            "**Przyimki zaawansowane** tworzą utarte konstrukcje o znaczeniu abstrakcyjnym.\n"
            "- **wbrew** + celownik: *wbrew zaleceniom*\n"
            "- **wobec** + dopełniacz: *wobec braku danych*\n"
            "- **ze względu na** + biernik: *ze względu na pogodę*\n"
            "- **w obliczu** + dopełniacz: *w obliczu trudności*\n"
            "- **pod wpływem** + dopełniacz: *pod wpływem stresu*\n"
            "- **w związku z** + narzędnik: *w związku z decyzją*"
        ),
        structure="przyimek + rzeczownik w stałym przypadku",
        rules=[
            "Wbrew i dzięki łączą się z celownikiem.",
            "Wobec, w obliczu i na skutek wymagają dopełniacza.",
            "Ze względu na łączy się z biernikiem.",
            "W związku z występuje z narzędnikiem.",
        ],
        examples=[
            GrammarExample(text="Wbrew prognozom pogoda się poprawiła.", translation=None),
            GrammarExample(text="Wobec braku danych nie podjęto decyzji.", translation=None),
            GrammarExample(
                text="Ze względu na remont zamknięto główną ulicę.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wbrew oczekiwania komisja przyjęła wniosek.",
                correct="Wbrew oczekiwaniom komisja przyjęła wniosek.",
                note="Wbrew wymaga celownika liczby mnogiej: oczekiwaniom.",
            ),
            GrammarMistake(
                wrong="Ze względu na sytuacji kryzysowej odwołano rozmowy.",
                correct="Ze względu na sytuację kryzysową odwołano rozmowy.",
                note="Ze względu na łączy się z biernikiem, nie z dopełniaczem.",
            ),
        ],
        related=["wyrazenia-przyimkowe", "przyimki-specjalistyczne", "celownik"],
    ),
    GrammarTopic(
        slug="aspekt-niuans",
        title="Aspekt — niuanse",
        level="B2",
        category="Aspekt",
        summary="Wybór aspektu w nawykach, narracji, przeczeniu i czasownikach iteratywnych.",
        explanation=(
            "**Niuanse aspektu** wykraczają poza prosty podział dokonany–niedokonany.\n"
            "- Nawyk: *Czytywał gazetę przy śniadaniu.* (forma iteratywna)\n"
            "- Jednorazowo: *Przeczytał gazetę i wyszedł.*\n"
            "- Przeczenie: *Nie przeczytałem raportu* (brak skutku) wobec *Nie czytałem "
            "raportu* (brak czynności)\n"
            "- Tło narracji: *Wchodził do sali, gdy zadzwonił telefon* wobec *Wszedł do sali i "
            "rozejrzał się*.\n\n"
            "Aspekt niedokonany opisuje przebieg i tło, dokonany — zamknięcie i skutek."
        ),
        structure="czasownik niedokonany (przebieg) / dokonany (skutek) / iteratywny (nawyk)",
        rules=[
            "Niedokonany opisuje przebieg, nawyk i tło zdarzeń.",
            "Dokonany podkreśla zakończenie i osiągnięty skutek.",
            "Formy iteratywne (czytywać, jadać, mawiać) wyrażają regularną powtarzalność.",
            "W przeczeniu wybór aspektu zmienia znaczenie: brak czynności a brak skutku.",
        ],
        examples=[
            GrammarExample(text="Codziennie czytywał gazetę przy śniadaniu.", translation=None),
            GrammarExample(text="Wchodził do sali, gdy zadzwonił telefon.", translation=None),
            GrammarExample(
                text="Nie przeczytałem jeszcze raportu, ale już go przejrzałem.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Zaczynałem przeczytać gazetę przy śniadaniu.",
                correct="Zaczynałem czytać gazetę przy śniadaniu.",
                note="Po czasowniku fazowym zaczynać używamy bezokolicznika niedokonanego.",
            ),
            GrammarMistake(
                wrong="Jutro będę przeczytać całą książkę.",
                correct="Jutro przeczytam całą książkę.",
                note="Dokonane przeczytać tworzy przyszłość prostą, bez będę.",
            ),
        ],
        related=["aspekt-pary", "aspekt-mistrzostwo", "prefiksy-znaczenia"],
    ),
    GrammarTopic(
        slug="prefiksy-ruchu",
        title="Prefiksy ruchu",
        level="B2",
        category="Czasowniki ruchu",
        summary="Kierunek i aspekt czasowników ruchu tworzone przedrostkami.",
        explanation=(
            "**Prefiksy ruchu** zmieniają kierunek i aspekt czasowników jechać, iść, lecieć, "
            "płynąć.\n"
            "- **do-** dotarcie do celu: *dojechać do Krakowa*\n"
            "- **przy-** przybycie: *przylecieć z Lizbony*\n"
            "- **wy-** opuszczenie miejsca: *wyjechać z domu*\n"
            "- **od-** oddalenie: *odjechać od peronu*\n"
            "- **prze-** przejście przez coś: *przejechać przez tunel*\n"
            "- **ob-** ruch wokół: *objechać jezioro*\n\n"
            "Każdy prefiks tworzy formę dokonaną; niedokonana powstaje przez wymianę tematu: "
            "*dojechać → dojeżdżać*."
        ),
        structure="prefiks (do-, przy-, wy-, od-, prze-, ob-, w-, za-) + czasownik ruchu",
        rules=[
            "Prefiks nadaje kierunek i tworzy formę dokonaną.",
            "Do- i przy- wskazują dotarcie lub przybycie.",
            "Wy- i od- oznaczają opuszczenie miejsca.",
            "Ob- oznacza ruch wokół obiektu i łączy się z biernikiem bez dookoła.",
        ],
        examples=[
            GrammarExample(text="Dojechaliśmy do Zakopanego przed zmrokiem.", translation=None),
            GrammarExample(text="Przyleciała z Lizbony wczoraj wieczorem.", translation=None),
            GrammarExample(text="Objechaliśmy całe jezioro w dwie godziny.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Objechaliśmy dookoła całe jezioro.",
                correct="Objechaliśmy całe jezioro.",
                note="Objechać zawiera znaczenie wokół i łączy się z biernikiem; "
                "dookoła jest zbędne.",
            ),
            GrammarMistake(
                wrong="Codziennie wyjechał z domu o siódmej.",
                correct="Codziennie wyjeżdżał z domu o siódmej.",
                note="Dla opisu zwyczaju w przeszłości naturalne jest wyjeżdżał. "
                "Dokonane wyjechał może podkreślać realizację każdego zdarzenia "
                "w określonym okresie; sam wyraz codziennie nie wyklucza aspektu dokonanego.",
            ),
        ],
        related=["prefiksy-znaczenia", "aspekt-niuans", "czas-przeszly"],
    ),
    GrammarTopic(
        slug="przyslowki-zaawansowane",
        title="Przysłówki zaawansowane",
        level="B2",
        category="Przysłówki",
        summary="Tworzenie, stopniowanie i użycie przysłówków złożonych.",
        explanation=(
            "**Przysłówki** określają czasownik, przymiotnik lub inny przysłówek.\n"
            "- Od przymiotników: *szybki → szybko*, *dobry → dobrze*\n"
            "- Stopniowanie: *często → częściej → najczęściej*\n"
            "- Stopniowanie opisowe: *charakterystycznie → bardziej charakterystycznie → "
            "najbardziej charakterystycznie*\n"
            "- Wyrażenia: *coraz częściej*, *na ogół*, *w dużej mierze*\n\n"
            "Przysłówek **coraz** z formą wyższą wyraża narastanie cechy: *coraz szybciej*, "
            "*coraz rzadziej*."
        ),
        structure="temat przymiotnika + -o / -e; bardziej / najbardziej + przysłówek",
        rules=[
            "Przysłówki na -o tworzy się od przymiotników zakończonych na -y.",
            "Stopień wyższy i najwyższy mają formy nieregularne: dobrze, lepiej, najlepiej.",
            "Coraz z formą wyższą wyraża narastanie cechy.",
            "Bardziej i najbardziej stopniują przysłówki o długiej formie.",
        ],
        examples=[
            GrammarExample(text="Coraz częściej pracujemy zdalnie.", translation=None),
            GrammarExample(
                text="Mówi po polsku znacznie płynniej niż rok temu.",
                translation=None,
            ),
            GrammarExample(
                text="Ta cecha ujawnia się najbardziej charakterystycznie w jego wczesnych "
                "wierszach.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Coraz bardziej częściej spotykamy się online.",
                correct="Coraz częściej spotykamy się online.",
                note="Przy formie wyższej przysłówka nie dodaje się bardziej.",
            ),
            GrammarMistake(
                wrong="Mówię dobrze polsku.",
                correct="Mówię dobrze po polsku.",
                note="Po polsku to utrwalone wyrażenie przysłówkowe; polsku nie jest "
                "współczesną formą miejscownika (ta ma postać polskim).",
            ),
        ],
        related=["przyslowki", "stopniowanie-przyslowkow", "stopniowanie-przymiotnikow"],
    ),
    GrammarTopic(
        slug="partykuly-zaawansowane",
        title="Partykuły zaawansowane",
        level="B2",
        category="Partykuły",
        summary="Partykuły pragmatyczne: przecież, bynajmniej, wręcz, niejako, właśnie.",
        explanation=(
            "**Partykuły zaawansowane** modyfikują sens całej wypowiedzi i sygnalizują "
            "postawę mówiącego.\n"
            "- **przecież** przypomina o czymś oczywistym: *Przecież mówiłem ci o tym.*\n"
            "- **bynajmniej** wzmacnia przeczenie: *Bynajmniej nie żartuję.*\n"
            "- **wręcz** stopniuje: *To wręcz niemożliwe.*\n"
            "- **niejako** osłabia twierdzenie: *Jest niejako naszym przewodnikiem.*\n"
            "- **właśnie** wskazuje dokładnie ten element: *Właśnie o to mi chodziło.*"
        ),
        structure="partykuła + człon zdania, który modyfikuje",
        rules=[
            "Bynajmniej wzmacnia przeczenie; może też samodzielnie znaczyć wcale nie.",
            "Wręcz wzmacnia ocenę i łączy człony o rosnącej sile.",
            "Niejako sygnalizuje dystans i ostrożność w ocenie.",
            "Przecież odwołuje się do wiedzy wspólnej rozmówców.",
        ],
        examples=[
            GrammarExample(
                text="Przecież uprzedzałem, że dokumenty trzeba złożyć osobiście.",
                translation=None,
            ),
            GrammarExample(text="Bynajmniej nie chciałem cię urazić.", translation=None),
            GrammarExample(
                text="To wręcz nieprawdopodobne, ile udało się zrobić w tydzień.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Bynajmniej mi to przeszkadza.",
                correct="Bynajmniej mi to nie przeszkadza.",
                note="Bynajmniej wzmacnia przeczenie, więc orzeczenie musi być zaprzeczone.",
            ),
            GrammarMistake(
                wrong="Ale przecież jednak wiesz, że mam rację.",
                correct="Przecież wiesz, że mam rację.",
                note="Uproszczenie stylistyczne dla neutralnego kontekstu. Oryginał może "
                "być poprawny, gdy ale i jednak odnoszą się do wcześniejszych argumentów.",
            ),
        ],
        related=["partykuly", "partykuly-modalne", "rejestr-jezykowy"],
    ),
    GrammarTopic(
        slug="wyrazenia-przyimkowe",
        title="Wyrażenia przyimkowe",
        level="B2",
        category="Wyrażenia przyimkowe",
        summary="Utarte połączenia przyimka z rzeczownikiem w tekstach formalnych.",
        explanation=(
            "**Wyrażenia przyimkowe** to stałe połączenia przyimka z rzeczownikiem, "
            "których nie należy przestawiać ani odmieniać.\n"
            "- *pod wpływem stresu*\n"
            "- *w obliczu trudności*\n"
            "- *na skutek zaniedbania*\n"
            "- *w trosce o zdrowie*\n"
            "- *na rzecz społeczności*\n"
            "- *w drodze wyjątku*\n\n"
            "Zastępują rozwinięte zdania podrzędne i zagęszczają tekst: *Ponieważ zabrakło "
            "danych → wobec braku danych*."
        ),
        structure="przyimek + rzeczownik w stałym przypadku",
        rules=[
            "Pod wpływem, w obliczu i na skutek łączą się z dopełniaczem.",
            "W trosce o wymaga biernika, a na rzecz — dopełniacza.",
            "Zachowuj rekcję wyrażenia; dodatki bywają poprawne: pod silnym wpływem stresu.",
            "W tekstach formalnych wyrażenia przyimkowe zastępują zdania podrzędne.",
        ],
        examples=[
            GrammarExample(
                text="Pod wpływem stresu podejmował pochopne decyzje.",
                translation=None,
            ),
            GrammarExample(
                text="W trosce o zdrowie pracowników wprowadzono przerwy.",
                translation=None,
            ),
            GrammarExample(
                text="W drodze wyjątku zgodzono się na zmianę terminu.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="w obliczu trudnościami",
                correct="w obliczu trudności",
                note="W obliczu wymaga dopełniacza.",
            ),
            GrammarMistake(
                wrong="w trosce o zdrowia pracowników",
                correct="w trosce o zdrowie pracowników",
                note="Przyimek o łączy się z biernikiem: o zdrowie.",
            ),
        ],
        related=["przyimki-zaawansowane", "przyimki-specjalistyczne", "frazeologia"],
    ),
    GrammarTopic(
        slug="skladnia-zlozona",
        title="Składnia złożona",
        level="B2",
        category="Składnia",
        summary="Wielopoziomowa podrzędność, zgodność składniowa i interpunkcja tekstu.",
        explanation=(
            "**Składnia złożona** obejmuje zdania z wieloma poziomami podrzędności i wymaga "
            "kontroli składni, interpunkcji oraz zgodności.\n"
            "- dopełnieniowe: *Sądzę, że...*\n"
            "- względne: *raport, który...*\n"
            "- okolicznikowe: *gdy, ponieważ, chociaż, o ile*\n\n"
            "W zdaniu względnym nie powtarza się zaimka: *Książka, którą kupiłem* — nie "
            "*Książka, którą kupiłem ją*. Każdy poziom podrzędności musi mieć jasne "
            "zdanie nadrzędne."
        ),
        structure="zdanie nadrzędne + zdania podrzędne różnych typów",
        rules=[
            "Każdy poziom podrzędności musi mieć jasne zdanie nadrzędne i własny spójnik.",
            "W zdaniu względnym zaimek który zastępuje rzeczownik i nie powtarza go.",
            "Zdania okolicznikowe oddziela się przecinkiem od nadrzędnego.",
            "Zbyt długie zdanie rozbijaj na krótsze, zachowując relacje logiczne.",
        ],
        examples=[
            GrammarExample(
                text="Książka, którą kupiłem wczoraj, leży na stole.",
                translation=None,
            ),
            GrammarExample(
                text="Twierdzę, że raport, który przedstawiono komisji, zawiera błędy.",
                translation=None,
            ),
            GrammarExample(
                text="Ponieważ brakowało danych, zdecydowano, że badanie powtórzymy.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Książka, którą kupiłem ją wczoraj, leży na stole.",
                correct="Książka, którą kupiłem wczoraj, leży na stole.",
                note="Zaimek którą zastępuje rzeczownik, więc ją jest zbędne.",
            ),
            GrammarMistake(
                wrong="Twierdzę że komisja która oceniała projekt nie miała pełnych danych.",
                correct="Twierdzę, że komisja, która oceniała projekt, nie miała "
                "pełnych danych.",
                note="Zdania podrzędne wydziela się przecinkami.",
            ),
        ],
        related=["zdania-wielokrotne", "skladnia-retoryczna", "zdania-okolicznikowe"],
    ),
]
