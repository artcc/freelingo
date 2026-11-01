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
        common_mistakes=[],
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
        common_mistakes=[],
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
        common_mistakes=[],
    ),
    GrammarTopic(
        slug="spojnosc-tekstu",
        title="Spójność i nawiązania w tekście",
        level="C1",
        category="Gramatyka",
        summary="Zaimek i powtórzenie leksykalne pomagają zachować czytelne odniesienia między zdaniami.",
        explanation="Spójność tekstu zależy od jasnych nawiązań, powtórzeń i relacji logicznych. Zaimek powinien mieć jednoznaczny poprzednik, a zbyt wiele synonimów może utrudnić rozpoznanie, czy nadal mowa o tym samym obiekcie.",
        structure="rzeczownik wprowadzający → jednoznaczne nawiązanie",
        rules=[
            "Sprawdź, czy każdy zaimek ma jasny poprzednik.",
            "Powtarzaj kluczowy termin, gdy synonim mógłby zmienić znaczenie.",
            "Używaj spójników tylko wtedy, gdy odpowiadają relacji między zdaniami.",
        ],
        examples=[
            GrammarExample(
                text="Zespół opublikował raport. Dokument zawiera trzy rekomendacje.",
                note="Jednoznaczne nawiązanie.",
            ),
            GrammarExample(
                text="Badanie wskazuje korelację, ale nie dowodzi związku przyczynowego.",
                note="Spójnik sygnalizuje ograniczenie wniosku.",
            ),
        ],
    ),
    GrammarTopic(
        slug="nominalizacja-a-czasownik",
        title="Nominalizacja a konstrukcja czasownikowa",
        level="C1",
        category="Gramatyka",
        summary="Wybór między rzeczownikiem odczasownikowym a czasownikiem wpływa na zwięzłość i jasność.",
        explanation="Nominalizacja kondensuje proces, lecz może ukryć wykonawcę i zależności między działaniami. Konstrukcja czasownikowa zwykle wyraźniej wskazuje, kto co zrobił i z jakim skutkiem.",
        structure="przeprowadzić analizę → przeanalizować",
        rules=[
            "Wybieraj nominalizację dla nazwanego procesu lub pojęcia.",
            "Preferuj czasownik, gdy ważne są wykonawca i kolejność działania.",
            "Unikaj kilku abstrakcyjnych rzeczowników w jednym ciągu.",
        ],
        examples=[
            GrammarExample(text="Komisja oceniła wniosek.", note="Jasny wykonawca i działanie."),
            GrammarExample(
                text="Ocena wniosku przez komisję zakończyła się w piątek.",
                note="Nominalizacja eksponuje proces.",
            ),
        ],
    ),
    GrammarTopic(
        slug="modalnosc-w-wnioskowaniu",
        title="Modalność wnioskowania",
        level="C1",
        category="Gramatyka",
        summary="Środki modalne wyrażają siłę wniosku i stopień pewności mówiącego.",
        explanation="Czasowniki modalne, przysłówki i tryb warunkowy różnicują pewność, możliwość oraz obowiązek. W tekstach argumentacyjnych ich dobór powinien odzwierciedlać siłę dostępnych dowodów.",
        structure="może wskazywać; prawdopodobnie wynika; należy sprawdzić",
        rules=[
            "Odróżniaj hipotezę od ustalonego faktu.",
            "Nie łącz osłabiających i kategorycznych określeń bez powodu.",
            "Wskazuj, czy modalność dotyczy możliwości, obowiązku czy oceny.",
        ],
        examples=[
            GrammarExample(
                text="Różnica może wynikać z odmiennej metody pomiaru.", note="Ostrożna hipoteza."
            ),
            GrammarExample(
                text="Dane nie pozwalają jednoznacznie rozstrzygnąć tej kwestii.",
                note="Ograniczenie wniosku.",
            ),
        ],
    ),
    GrammarTopic(
        slug="zdania-zlozone-wielokrotnie",
        title="Zdania wielokrotnie złożone",
        level="C1",
        category="Gramatyka",
        summary="Rozbudowane zdanie wymaga czytelnej hierarchii zdań składowych.",
        explanation="W zdaniu wielokrotnie złożonym zdania podrzędne mogą zależeć od różnych elementów. Przecinki wyznaczają ich granice; przy nadmiernym rozbudowaniu warto rozdzielić treść na kilka zdań.",
        structure="zdanie główne + podrzędne + wtrącenie",
        rules=[
            "Ustal, od którego wyrazu zależy każde zdanie podrzędne.",
            "Stawiaj przecinki zgodnie z granicami składniowymi.",
            "Rozbij zdanie, gdy kilka poziomów zależności utrudnia odczyt.",
        ],
        examples=[
            GrammarExample(
                text="Autor zaznaczył, że dane, które zebrano wiosną, wymagają weryfikacji.",
                note="Zdanie względne wewnątrz podrzędnego.",
            ),
            GrammarExample(
                text="Choć próba była niewielka, wynik, który uzyskano, uzasadnia dalsze badania.",
                note="Czytelnie oddzielone zdania składowe.",
            ),
        ],
    ),
    GrammarTopic(
        slug="struktury-tematyczno-rematyczne",
        title="Temat i remat w zdaniu",
        level="C1",
        category="Gramatyka",
        summary="Szyk wyrazów może odróżniać znany temat wypowiedzi od nowej informacji.",
        explanation="Temat wskazuje punkt wyjścia, a remat wnosi informację istotną w danym kontekście. Polski szyk pozwala przesuwać elementy dla kontrastu, lecz nie należy mylić swobody szyku z dowolnością.",
        structure="znany temat → nowa informacja lub kontrast",
        rules=[
            "Umieszczaj informację znaną przed nową, jeśli wspiera to płynność.",
            "Używaj szyku przestawnego dla wyraźnego kontrastu.",
            "Dbaj, by zaimek nie wyprzedzał niejasno swojego odniesienia.",
        ],
        examples=[
            GrammarExample(
                text="Raport omówiła komisja, a nie zespół badawczy.",
                note="Kontrast na końcu zdania.",
            ),
            GrammarExample(
                text="Komisja omówiła raport podczas posiedzenia.", note="Neutralny punkt wyjścia."
            ),
        ],
    ),
    GrammarTopic(
        slug="partykuły-wypowiedzi",
        title="Partykuły i odcień wypowiedzi",
        level="C1",
        category="Gramatyka",
        summary="Partykuły modyfikują zakres, nacisk lub stosunek mówiącego do treści.",
        explanation="Wyrazy takie jak właśnie, nawet, tylko, chyba i przecież wpływają na interpretację całego zdania albo jego fragmentu. Ich zakres zależy od pozycji i kontekstu.",
        structure="właśnie ten wynik; wynik chyba się zmienił",
        rules=[
            "Ustaw partykułę blisko elementu, który modyfikuje.",
            "Sprawdź, czy zakres partykuły nie pozostawia dwuznaczności.",
            "Odróżniaj ostrożne przypuszczenie od pewnego twierdzenia.",
        ],
        examples=[
            GrammarExample(
                text="Tylko komisja zatwierdziła poprawioną wersję.",
                note="Tylko ogranicza wykonawcę.",
            ),
            GrammarExample(
                text="Komisja zatwierdziła tylko poprawioną wersję.",
                note="Tylko ogranicza przedmiot.",
            ),
        ],
    ),
    GrammarTopic(
        slug="strona-i-perspektywa",
        title="Strona gramatyczna a perspektywa",
        level="C1",
        category="Gramatyka",
        summary="Wybór strony czynnej, biernej lub bezosobowej zmienia perspektywę opisu.",
        explanation="Strona czynna eksponuje wykonawcę, bierna — odbiorcę działania, a konstrukcja bezosobowa może pomijać wykonawcę. Każda forma ma konsekwencje dla odpowiedzialności i struktury informacji.",
        structure="zespół opublikował; raport został opublikowany; opublikowano raport",
        rules=[
            "Wybieraj stronę czynną, gdy istotny jest wykonawca.",
            "Używaj strony biernej, gdy ważniejszy jest odbiorca działania.",
            "Nie ukrywaj wykonawcy formą bezosobową, jeśli ma znaczenie dla sensu.",
        ],
        examples=[
            GrammarExample(text="Zespół opublikował wyniki w maju.", note="Wskazany wykonawca."),
            GrammarExample(
                text="Wyniki opublikowano w maju.", note="Wykonawca nie jest eksponowany."
            ),
        ],
    ),
    GrammarTopic(
        slug="zdania-warunkowe-mieszane",
        title="Warunki i skutki w różnych ramach czasowych",
        level="C1",
        category="Gramatyka",
        summary="Zdanie warunkowe może łączyć warunek z przeszłości ze skutkiem obecnym.",
        explanation="Cząstka by i formy czasu przeszłego tworzą różne interpretacje warunku. Kontekst pozwala odróżnić warunek otwarty, hipotetyczny oraz niespełniony, a czasem zestawić wcześniejszą przyczynę z aktualnym skutkiem.",
        structure="gdyby + forma przeszła; skutek w trybie warunkowym",
        rules=[
            "Ustal, czy warunek jest możliwy, hipotetyczny czy niespełniony.",
            "Dobieraj aspekt do zakończonego rezultatu lub trwającej sytuacji.",
            "Zachowuj zgodność osoby i rodzaju w obu częściach zdania.",
        ],
        examples=[
            GrammarExample(
                text="Gdyby wniosek złożono wcześniej, decyzja byłaby już znana.",
                note="Przeszły warunek i obecny skutek.",
            ),
            GrammarExample(
                text="Gdyby znała szczegóły, nie wyciągałaby takiego wniosku.",
                note="Warunek hipotetyczny.",
            ),
        ],
    ),
    GrammarTopic(
        slug="mowa-niezalezna-i-zalezna",
        title="Mowa niezależna i zależna",
        level="C1",
        category="Gramatyka",
        summary="Przytaczanie wypowiedzi wymaga zachowania jej treści i relacji czasowych.",
        explanation="Mowa niezależna cytuje słowa, a zależna włącza je do zdania narratora. Przy zmianie konstrukcji zaimki i określenia czasu muszą odpowiadać nowemu punktowi widzenia.",
        structure="Powiedziała: „Wrócę jutro” → Powiedziała, że wróci następnego dnia.",
        rules=[
            "Zachowuj znaczenie i stopień pewności wypowiedzi źródłowej.",
            "Dostosuj zaimki i określenia czasu do perspektywy narratora.",
            "Nie przedstawiaj wniosku jako bezpośredniego cytatu.",
        ],
        examples=[
            GrammarExample(text="Powiedział: „Wyślę raport jutro”.", note="Mowa niezależna."),
            GrammarExample(
                text="Powiedział, że wyśle raport następnego dnia.", note="Mowa zależna."
            ),
        ],
    ),
    GrammarTopic(
        slug="przyimki-przenosne",
        title="Przyimki w znaczeniach przenośnych",
        level="C1",
        category="Gramatyka",
        summary="Przyimki tworzą utrwalone połączenia abstrakcyjne i przestrzenne.",
        explanation="W polszczyźnie przyimki występują w licznych połączeniach o znaczeniu przenośnym. Przypadek rzeczownika zależy od konkretnej konstrukcji, dlatego należy zapamiętywać całe wyrażenia.",
        structure="w związku z + narzędnik; w odniesieniu do + dopełniacz",
        rules=[
            "Ucz się przyimka wraz z wymaganym przypadkiem.",
            "Odróżniaj znaczenie dosłowne od utrwalonego połączenia.",
            "Unikaj kalkowania przyimków z innych języków.",
        ],
        examples=[
            GrammarExample(
                text="W związku z opóźnieniem zmieniono harmonogram.", note="Narzędnik po z."
            ),
            GrammarExample(
                text="W odniesieniu do tej kwestii nie podjęto decyzji.", note="Dopełniacz po do."
            ),
        ],
    ),
    GrammarTopic(
        slug="uzgodnienie-wyrazen-liczebnikowych",
        title="Uzgodnienie w rozbudowanych grupach liczebnikowych",
        level="C1",
        category="Gramatyka",
        summary="Liczebniki i określenia ilościowe wpływają na przypadek i zgodę w zdaniu.",
        explanation="Grupy z liczebnikami, ułamkami i określeniami ilościowymi mogą wymagać dopełniacza oraz różnej formy orzeczenia. Wybór zależy od konstrukcji i tego, który składnik pełni funkcję podmiotu.",
        structure="większość uczestników; dwie trzecie zespołu",
        rules=[
            "Ustal, który rzeczownik jest głową grupy.",
            "Dobieraj przypadek do konstrukcji ilościowej.",
            "Sprawdzaj zgodność orzeczenia z całym podmiotem.",
        ],
        examples=[
            GrammarExample(
                text="Większość uczestników przyjęła rekomendację.",
                note="Orzeczenie uzgodnione z większością.",
            ),
            GrammarExample(
                text="Dwie trzecie odpowiedzi było poprawnych.", note="Konstrukcja ułamkowa."
            ),
        ],
    ),
    GrammarTopic(
        slug="nastepstwo-czasow-w-mowie-zaleznej",
        title="Następstwo czasów w mowie zależnej",
        level="C1",
        category="Gramatyka",
        summary="Perspektywa narratora wpływa na formę czasu i określenia czasu w przytoczonej wypowiedzi.",
        explanation="W polszczyźnie forma czasu w mowie zależnej zależy od relacji czasowej i punktu widzenia, a nie od mechanicznego przesunięcia czasu. Określenia takie jak dziś i jutro mogą wymagać zmiany, jeśli zmienił się moment odniesienia.",
        structure="Powiedziała: „Wrócę jutro” → Powiedziała, że wróci następnego dnia.",
        rules=[
            "Zachowuj relację między momentem wypowiedzi a opisywanym zdarzeniem.",
            "Zmieniaj określenia czasu tylko wtedy, gdy zmienia się punkt odniesienia.",
            "Nie stosuj mechanicznego przesunięcia czasu z innych języków.",
        ],
        examples=[
            GrammarExample(
                text="Wczoraj zapowiedział, że dziś prześle poprawioną wersję.",
                note="Relacja czasowa wynika z kontekstu.",
            ),
            GrammarExample(
                text="Autorka napisała, że wyniki są niejednoznaczne.",
                note="Treść nadal aktualna w chwili relacji.",
            ),
        ],
    ),
]
