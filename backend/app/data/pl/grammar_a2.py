"""Polish grammar topics — A2."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="czas-przeszly-rodzaj",
        title="Czas przeszły: rodzaj i osoba",
        level="A2",
        category="Czasowniki",
        summary="Zgodność form czasu przeszłego z rodzajem podmiotu w dłuższych wypowiedziach.",
        explanation=(
            "Czas przeszły zgadza się z **rodzajem podmiotu**, a nie z płcią osoby, która mówi. "
            "Dlatego o tej samej czynności powiemy *Piotr czytał*, *Anna czytała*, *dziecko "
            "czytało*, a w liczbie mnogiej *chłopcy czytali*, *dziewczynki czytały*.\n\n"
            "**Liczba mnoga:** grupa z przynajmniej jednym mężczyzną wymaga form męskoosobowych "
            "(*byliśmy, czytaliście, przyszli*), a pozostałe grupy — form niemęskoosobowych "
            "(*byłyśmy, czytałyście, przyszły*).\n\n"
            "**Nieregularne tematy czasu przeszłego:** iść → szedł, szła, szli; jeść → jadł, "
            "jadła, jedli; wziąć → wziąłem, wzięła, wzięli; móc → mogłem, mogła, mogli; "
            "pić → piłem, piła, pili.\n\n"
            "W opowiadaniu warto trzymać się jednego punktu odniesienia: jeśli narratorem jest "
            "kobieta, o sobie w liczbie pojedynczej mówi w rodzaju żeńskim "
            "(*wstałam, zrobiłam, poszłam*), nawet gdy "
            "opowiada o pracy w typowo męskim środowisku."
        ),
        structure="-łem / -łam · -łeś / -łaś · -ł / -ła / -ło\nlm.: -liśmy / -łyśmy · -li / -ły",
        rules=[
            "Forma czasu przeszłego zależy od rodzaju podmiotu, nie od płci mówiącego.",
            "Grupa mieszana i grupa samych mężczyzn wymagają form męskoosobowych: byliśmy, poszli.",
            "Grupy kobiet, dzieci i rzeczy przyjmują formy niemęskoosobowe: byłyśmy, poszły.",
            "Niektóre czasowniki mają nieregularny temat przeszły: szedł, jadł, wziął, mógł.",
        ],
        examples=[
            GrammarExample(text="Kiedy byłem mały, jeździłem z dziadkiem nad jezioro."),
            GrammarExample(text="Ania i Kasia wróciły z wakacji w niedzielę."),
            GrammarExample(text="Wczoraj poszliśmy z bratem na mecz.", note="grupa mieszana"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ania i Piotr były zmęczone.",
                correct="Ania i Piotr byli zmęczeni.",
                note="W grupie mieszanej obowiązuje forma męskoosobowa.",
            ),
            GrammarMistake(
                wrong="Ja wzięła parasol.",
                correct="Ja wzięłam parasol.",
                note="Kobieta mówi wzięłam; forma wzięła to trzecia osoba.",
            ),
        ],
        related=["aspekt-wprowadzenie", "czas-przyszly-niedokonany", "tryb-warunkowy"],
    ),
    GrammarTopic(
        slug="aspekt-wprowadzenie",
        title="Aspekt czasownika",
        level="A2",
        category="Czasowniki",
        summary="Para aspektowa: czynność w toku i czynność zakończona z rezultatem.",
        explanation=(
            "Polskie czasowniki występują w **parach aspektowych**. Niedokonany opisuje proces, "
            "trwanie i powtarzalność, dokonany — zakończenie i wynik: *czytać — przeczytać*, "
            "*pisać — napisać*, *robić — zrobić*.\n\n"
            "**Niedokonany:** *Czytałem gazetę przez godzinę.* *Czytuję gazety.* (proces, nawyk)\n"
            "**Dokonany:** *Przeczytałem gazetę.* (czynność skończona, jest efekt)\n\n"
            "Czasowniki dokonane **nie mają czasu teraźniejszego**. Ich formy z końcówkami "
            "teraźniejszymi oznaczają przyszłość: *przeczytam, napiszę, przyjdą*.\n\n"
            "Niektóre pary różnią się przedrostkiem (*pisać — napisać*), inne przyrostkiem "
            "(*kupować — kupić*), a jeszcze inne mają zupełnie inny temat (*brać — wziąć*)."
        ),
        structure="niedokonany: proces i nawyk · dokonany: wynik\npary: czytać — przeczytać, "
        "pisać — napisać",
        rules=[
            "Czasownik niedokonany tworzy czas teraźniejszy, przyszły złożony i przeszły.",
            "Czasownik dokonany nie ma czasu teraźniejszego; jego formy dotyczą przyszłości.",
            "Proces opisujemy zwykle przez + biernik (pisałem przez godzinę), "
            "a czas potrzebny na wynik przez w + biernik (napisałem w godzinę).",
            "Nawyki zwykle opisujemy aspektem niedokonanym. Zawsze może też łączyć się "
            "z dokonanym, np. gdy wyrażamy obietnicę: Zawsze ci pomogę.",
        ],
        examples=[
            GrammarExample(text="Wczoraj pisałem raport przez cały wieczór.", note="proces"),
            GrammarExample(text="Wczoraj napisałem raport i wysłałem go szefowi.", note="wynik"),
            GrammarExample(text="Codziennie kupuję świeże pieczywo.", note="nawyk"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wczoraj przeczytałem książkę przez trzy godziny.",
                correct="Wczoraj czytałem książkę przez trzy godziny.",
                note="Określenie czasu trwania wymaga czasownika niedokonanego.",
            ),
            GrammarMistake(
                wrong="Codziennie będę kupić mleko w tym sklepie.",
                correct="Codziennie będę kupować mleko w tym sklepie.",
                note="Przyszłość złożona wymaga bezokolicznika niedokonanego.",
            ),
        ],
        related=["czas-przeszly-rodzaj", "czas-przyszly-niedokonany", "czasowniki-prefiksalne"],
    ),
    GrammarTopic(
        slug="dopelniacz",
        title="Dopełniacz: formy i użycie",
        level="A2",
        category="Przypadki",
        summary="Końcówki dopełniacza oraz jego użycie po przyimkach i przy wyrażaniu posiadania.",
        explanation=(
            "Dopełniacz odpowiada na pytania **kogo? czego?** i jest przypadkiem najczęściej "
            "wymaganym przez przyimki.\n\n"
            "**Końcówki liczby pojedynczej:**\n"
            "- rzeczowniki męskie zakończone na spółgłoskę: **-a** przy osobach i zwierzętach "
            "(*studenta, psa*); przy rzeczach wybór **-a / -u** zależy od wyrazu "
            "(*noża, chleba*, ale *cukru, sklepu*). Pojęcia abstrakcyjne często mają **-u** "
            "(*czasu*), lecz nie zawsze (*pecha*)\n"
            "- rzeczowniki żeńskie oraz męskie zakończone na **-a**: **-y / -i** — "
            "*wody, pracy, ziemi, ręki, drogi; kierowca → kierowcy, kolega → kolegi*. "
            "Dobór końcówki zależy od tematu; po k i g piszemy **-i**, nie -y\n"
            "- rodzaj nijaki: **-a** (*okna, morza, imienia*)\n\n"
            "**Liczba mnoga:** w rodzaju męskim często **-ów** (*studentów, sklepów*), "
            "ale też **-i / -y** (*nauczycieli, lekarzy*). Rzeczowniki żeńskie i nijakie "
            "często mają formę bez końcówki (*kobiet, ulic, okien, jabłek*); "
            "spotykamy też **-i / -y** (*kości, nocy*).\n\n"
            "Z dopełniaczem łączą się przyimki **do, z, od, bez, dla, u, obok, koło, podczas, "
            "oprócz**: *do sklepu, z pracy, bez cukru, dla dzieci*."
        ),
        structure="kogo? czego? → -a / -u (m. na spółgłoskę) · -y / -i (ż. i m. na -a) · "
        "-a (n.) · -ów / -y / -i / brak końcówki (lm.)",
        rules=[
            "Męskie nazwy osób i zwierząt zakończone na spółgłoskę mają -a: studenta, psa. "
            "Męskie na -a odmieniają się inaczej: kolegi, kierowcy.",
            "Przy męskich nazwach rzeczy i pojęć wybór -a / -u trzeba poznawać z wyrazem: "
            "chleba, cukru, czasu, pecha.",
            "Do, od, bez, dla, u oraz z w znaczeniu pochodzenia wymagają dopełniacza; "
            "z w znaczeniu towarzystwa łączy się z narzędnikiem.",
            "W liczbie mnogiej rodzaj męski ma zwykle końcówkę -ów.",
        ],
        examples=[
            GrammarExample(text="Wracam z pracy około siódmej."),
            GrammarExample(text="Kupiliśmy bukiet dla mamy."),
            GrammarExample(text="Obok naszego domu jest mały park."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Idę do sklep.",
                correct="Idę do sklepu.",
                note="Po przyimku do używamy dopełniacza.",
            ),
            GrammarMistake(
                wrong="Kawa bez cukier.",
                correct="Kawa bez cukru.",
                note="Po przyimku bez stoi dopełniacz z końcówką -u.",
            ),
        ],
        related=["dopelniacz-liczebniki", "zaimki-dopelniacz", "celownik"],
    ),
    GrammarTopic(
        slug="dopelniacz-liczebniki",
        title="Dopełniacz po liczebnikach",
        level="A2",
        category="Liczebniki",
        summary="Liczebniki proste i złożone oraz ich wpływ na formę rzeczownika.",
        explanation=(
            "W mianowniku i bierniku liczebniki **dwa, trzy, cztery** łączą się z formami "
            "liczby mnogiej rzeczowników niemęskoosobowych: *dwa bilety, trzy książki, "
            "cztery okna*. Przy rzeczownikach męskoosobowych rozróżniamy konstrukcje "
            "*dwaj studenci przyszli* i *dwóch studentów przyszło*. W bierniku używamy "
            "formy *widzę dwóch studentów*.\n\n"
            "Liczebniki **5–21** wymagają w tych konstrukcjach dopełniacza liczby mnogiej: "
            "*pięć jabłek, dziesięć minut, dwadzieścia jeden złotych*.\n\n"
            "Wyrażenia ilościowe również łączą się z dopełniaczem: *kilka osób, wiele pracy, dużo "
            "czasu, mało pieniędzy*.\n\n"
            "W liczebnikach złożonych zakończonych na **dwa, trzy, cztery** wracamy do form "
            "typu *dwadzieścia dwa bilety, trzydzieści cztery książki*. Nie dotyczy to "
            "liczb zakończonych na **12, 13, 14**: *dwanaście biletów, sto dwanaście biletów*. "
            "Pozostałe liczebniki większe od jednego wymagają tu dopełniacza: "
            "*dwadzieścia pięć biletów, dwadzieścia jeden złotych*. W przypadkach zależnych "
            "odmieniamy całą grupę, np. *z pięcioma studentami*."
        ),
        structure=(
            "mianownik/biernik, niemęskoosobowe: 2–4, 22–24, 32–34... + bilety; "
            "5–21, 25–31... + biletów\n"
            "męskoosobowe: dwaj studenci przyszli / dwóch studentów przyszło"
        ),
        rules=[
            "W mianowniku i bierniku liczebniki 5–21 łączą się z dopełniaczem liczby mnogiej.",
            "Dwa, trzy, cztery i liczebniki złożone zakończone tymi wyrazami łączą się "
            "z formami typu bilety; liczby zakończone na 12–14 wymagają formy biletów.",
            "Kilka, wiele, dużo, mało łączą się z dopełniaczem.",
            "Przy rzeczownikach męskoosobowych odróżniamy dwaj studenci od dwóch studentów.",
        ],
        examples=[
            GrammarExample(text="Kup pięć jabłek i dwie bułki."),
            GrammarExample(text="W klasie było dwadzieścia osiem osób."),
            GrammarExample(text="Potrzebuję jeszcze trzech minut."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Kup pięć jabłka.",
                correct="Kup pięć jabłek.",
                note="Po liczebniku pięć rzeczownik przyjmuje dopełniacz liczby mnogiej.",
            ),
            GrammarMistake(
                wrong="Na kursie było trzy studentów.",
                correct="Na kursie było trzech studentów.",
                note="Przy orzeczeniu było używamy trzech studentów; alternatywnie: "
                "Na kursie byli trzej studenci.",
            ),
        ],
        related=["dopelniacz", "liczebniki-porzadkowe", "zaimki-dopelniacz"],
    ),
    GrammarTopic(
        slug="zaimki-dopelniacz",
        title="Zaimki osobowe w dopełniaczu",
        level="A2",
        category="Zaimki",
        summary="Formy mnie, ciebie, jego, jej, ich oraz ich warianty po przyimkach.",
        explanation=(
            "W dopełniaczu zaimki osobowe mają formy: **mnie, ciebie (cię), jego (go), jej, nas, "
            "was, ich (nich)**.\n\n"
            "**Bez przyimka** częstsze są formy krótkie, nieakcentowane: *Nie ma go. Nie widzę "
            "cię. Nie znam jej.*\n\n"
            "**Po przyimku** używamy form pełnych, a zaimki trzeciej osoby zaczynają się od *n-*: "
            "*do mnie, u ciebie, do niego, u niej, do nich*. Formy *niego, niej, nich* występują "
            "wyłącznie po przyimkach.\n\n"
            "Formy pełne *mnie* i *ciebie* stoją też na początku zdania oraz wtedy, gdy chcemy "
            "coś podkreślić: *Ciebie szukam, nie jego.*"
        ),
        structure="mnie · ciebie / cię · jego / go · jej · nas · was · ich / nich\npo przyimku: "
        "do niego, u niej, do nich",
        rules=[
            "Po przyimkach zaimki trzeciej osoby przyjmują formy niego, niej, nich.",
            "Formy krótkie go, cię są nieakcentowane i nie występują po przyimku.",
            "Formy pełne mnie i ciebie stosujemy na początku zdania i przy podkreśleniu.",
            "Zaimek w dopełniaczu pojawia się też po przeczeniu: nie znam jej.",
        ],
        examples=[
            GrammarExample(text="Nie widziałem jej od poniedziałku."),
            GrammarExample(text="Bez ciebie nie dam rady."),
            GrammarExample(text="Idę do niego na kolację.", note="po przyimku"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Nie znam ją.",
                correct="Nie znam jej.",
                note="Po przeczeniu biernik zamienia się w dopełniacz.",
            ),
            GrammarMistake(
                wrong="Byłem u jego wczoraj.",
                correct="Byłem u niego wczoraj.",
                note="Po przyimku forma jego zmienia się w niego.",
            ),
        ],
        related=["dopelniacz", "celownik", "dopelniacz-liczebniki"],
    ),
    GrammarTopic(
        slug="liczebniki-porzadkowe",
        title="Liczebniki porządkowe",
        level="A2",
        category="Liczebniki",
        summary="Pierwszy, drugi, trzeci — odmiana w datach, adresach i numeracji.",
        explanation=(
            "Liczebniki porządkowe odpowiadają na pytanie **który?** i odmieniają się jak "
            "przymiotniki: *pierwszy, pierwszego, pierwszemu, pierwszym*.\n\n"
            "**Podstawowe formy:** pierwszy, drugi, trzeci, czwarty, piąty, szósty, siódmy, "
            "ósmy, dziewiąty, dziesiąty.\n\n"
            "**Złożone:** jedenasty, dwunasty, dwudziesty, trzydziesty. Gdy liczba składa się z "
            "dwóch wyrazów, zapisujemy je rozdzielnie: *dwudziesty pierwszy*.\n\n"
            "Na pytanie **kiedy?** odpowiadamy dopełniaczem: *pierwszego maja, trzeciego "
            "czerwca*. Na pytanie **który dziś jest?** odpowiadamy mianownikiem dnia: "
            "*Dzisiaj jest pierwszy maja*. Nazwa miesiąca pozostaje w dopełniaczu.\n\n"
            "**Adresy i piętra:** *mieszkam na trzecim piętrze*, *mieszkanie numer dwunasty*, "
            "*jestem w drugiej klasie*."
        ),
        structure="dziś jest pierwszy maja · spotkamy się pierwszego maja",
        rules=[
            "Liczebniki porządkowe odmieniają się przez przypadki i rodzaje jak przymiotniki.",
            "Kiedy? — pierwszego maja; który dziś jest? — pierwszy maja.",
            "Liczebniki złożone zapisujemy rozdzielnie: dwudziesty pierwszy.",
            "Po przyimku na z nazwą piętra występuje miejscownik: na drugim piętrze.",
        ],
        examples=[
            GrammarExample(text="Urodziłem się trzeciego marca."),
            GrammarExample(text="Mieszkam na czwartym piętrze."),
            GrammarExample(text="To już moja druga wizyta w Krakowie."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Urodziłem się pierwszy maja.",
                correct="Urodziłem się pierwszego maja.",
                note="Data odpowiadająca na pytanie kiedy wymaga tu dopełniacza.",
            ),
            GrammarMistake(
                wrong="Mieszkam na trzecie piętrze.",
                correct="Mieszkam na trzecim piętrze.",
                note="Po przyimku na z nazwą piętra używamy miejscownika.",
            ),
        ],
        related=["dopelniacz-liczebniki", "miejscownik-przyimki", "przyimki-czasu"],
    ),
    GrammarTopic(
        slug="celownik",
        title="Celownik",
        level="A2",
        category="Przypadki",
        summary="Komu? czemu? — odbiorca czynności i konstrukcje z zaimkiem w celowniku.",
        explanation=(
            "Celownik odpowiada na pytania **komu? czemu?** i wskazuje odbiorcę czynności.\n\n"
            "**Końcówki liczby pojedynczej:**\n"
            "- rzeczowniki męskie zakończone na spółgłoskę: **-owi** (*studentowi, sąsiadowi*) "
            "oraz **-u** w niewielkiej grupie "
            "wyrazów (*ojcu, bratu, psu*)\n"
            "- rzeczowniki żeńskie oraz męskie zakończone na **-a**: **-e**, często ze zmianą "
            "spółgłoski (*siostra → siostrze, mama → mamie, kolega → koledze*), lub **-y / -i** "
            "(*praca → pracy, noc → nocy, ziemia → ziemi, kierowca → kierowcy*). "
            "Dobór końcówki zależy od tematu; formy te są takie jak w miejscowniku\n"
            "- rodzaj nijaki: **-u** (*dziecko → dziecku, okno → oknu*)\n\n"
            "**Liczba mnoga:** zawsze **-om** (*studentom, dzieciom, kobietom*).\n\n"
            "Celownika wymagają czasowniki **pomagać, dziękować, mówić, dawać, kupować, "
            "życzyć**: *Pomagam mamie. Dziękuję ci.* Występuje też w konstrukcjach z zaimkiem: "
            "*jest mi zimno, podoba mi się, trudno mu uwierzyć*."
        ),
        structure="komu? czemu? → -owi / -u (m. na spółgłoskę) · "
        "-e / -y / -i (ż. i m. na -a) · -u (n.) · -om (lm.)",
        rules=[
            "Czasowniki pomagać, dziękować, mówić i dawać wymagają celownika.",
            "Celownik liczby mnogiej ma zawsze końcówkę -om.",
            "W konstrukcjach typu jest mi zimno zaimek stoi w celowniku.",
            "Rzeczowniki żeńskie i męskie na -a mają -e, -y lub -i; temat nie zawsze się "
            "zmienia: siostra → siostrze, ale praca → pracy i ziemia → ziemi.",
        ],
        examples=[
            GrammarExample(text="Pomagam mamie w kuchni."),
            GrammarExample(text="Dziękuję ci za pomoc."),
            GrammarExample(text="Kolega pomaga kierowcy, a ja przyglądam się jego pracy."),
            GrammarExample(text="Jest mi zimno, zamknij okno.", note="zaimek w celowniku"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Pomagam mamę w kuchni.",
                correct="Pomagam mamie w kuchni.",
                note="Czasownik pomagać łączy się z celownikiem, nie z biernikiem.",
            ),
            GrammarMistake(
                wrong="Dziękuję ciebie za prezent.",
                correct="Dziękuję ci za prezent.",
                note="Dziękować wymaga celownika: dziękuję tobie, dziękuję ci.",
            ),
        ],
        related=["boli-mnie", "dopelniacz", "tryb-rozka"],
    ),
    GrammarTopic(
        slug="boli-mnie",
        title="Boli mnie — dolegliwości",
        level="A2",
        category="Składnia",
        summary="Opisywanie bólu i złego samopoczucia za pomocą biernika i celownika.",
        explanation=(
            "O dolegliwościach mówimy w konstrukcji **boli mnie + część ciała** lub **bolą mnie + "
            "część ciała w liczbie mnogiej**.\n\n"
            "Podmiotem zdania jest narząd, a osoba odczuwająca ból występuje w **bierniku**: "
            "*Boli mnie głowa. Bolą mnie plecy. Boli go ząb.*\n\n"
            "Podobnie działają konstrukcje z **celownikiem**: *Jest mi zimno. Jest mi niedobrze. "
            "Kręci mi się w głowie.* Natomiast *Mdli mnie* wymaga biernika.\n\n"
            "Przyczynę bólu wyrażamy przyimkiem **od** z dopełniaczem: *Boli mnie głowa od "
            "hałasu.* Czas trwania też wymaga dopełniacza: *Boli mnie gardło od trzech dni.*"
        ),
        structure="boli mnie + narząd (l. poj.) · bolą mnie + narządy (l. mn.)\njest mi zimno / "
        "niedobrze / słabo",
        rules=[
            "Przy jednym narządzie używamy boli, przy kilku — bolą.",
            "Osoba odczuwająca ból stoi w bierniku: mnie, cię, go, ją, nas, was, ich.",
            "W konstrukcjach typu jest mi zimno zaimek występuje w celowniku.",
            "Przyczynę bólu wyraża od + dopełniacz: od hałasu, od wysiłku.",
        ],
        examples=[
            GrammarExample(text="Boli mnie gardło od wczoraj."),
            GrammarExample(text="Bolą mnie oczy po całym dniu przy komputerze."),
            GrammarExample(text="Jest mi słabo, muszę usiąść."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Boli mnie plecy.",
                correct="Bolą mnie plecy.",
                note="Plecy to rzeczownik w liczbie mnogiej, więc czasownik też jest w liczbie "
                "mnogiej.",
            ),
            GrammarMistake(
                wrong="Jestem zimno.",
                correct="Jest mi zimno.",
                note="Stan odczuwany przez osobę wyrażamy celownikiem: jest mi.",
            ),
        ],
        related=["celownik", "tryb-rozka"],
    ),
    GrammarTopic(
        slug="tryb-rozka",
        title="Tryb rozkazujący",
        level="A2",
        category="Czasowniki",
        summary="Polecenia, prośby i instrukcje w drugiej osobie oraz w formach grzecznościowych.",
        explanation=(
            "Tryb rozkazujący drugiej osoby liczby pojedynczej tworzymy od tematu trzeciej osoby "
            "liczby mnogiej: *czytają → czytaj*, *mówią → mów*, *robią → rób*, *idą → idź*.\n\n"
            "**Liczba mnoga:** dodajemy **-my** i **-cie**: *czytajmy, czytajcie; mówmy, "
            "mówcie; chodźmy, chodźcie*.\n\n"
            "**Formy grzecznościowe:** *niech pan / niech pani + trzecia osoba*: *Niech pan "
            "usiądzie. Niech pani wejdzie.* Równoważne jest *proszę + bezokolicznik*: *Proszę "
            "usiąść.*\n\n"
            "**Ważniejsze formy nieregularne:** być → bądź, mieć → miej, dać → daj, iść → idź, "
            "jeść → jedz, wziąć → weź, powiedzieć → powiedz."
        ),
        structure="2. os. sg.: czytaj · mów · rób\n1. os. pl.: -my · 2. os. pl.: -cie\ngrzecz.: "
        "niech pan / pani + 3. os.",
        rules=[
            "Formy pierwszej i drugiej osoby liczby mnogiej tworzymy przez dodanie -my i -cie.",
            "Do osoby, do której zwracamy się per pan lub pani, używamy niech + trzecia osoba.",
            "Po proszę stoi bezokolicznik, a nie forma osobowa.",
            "Przeczenie tworzymy słowem nie: nie czytaj, nie mów, proszę nie palić.",
        ],
        examples=[
            GrammarExample(text="Zamknij okno, proszę."),
            GrammarExample(text="Niech pani usiądzie w poczekalni.", note="forma grzecznościowa"),
            GrammarExample(text="Przeczytajcie instrukcję przed użyciem."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Idz do domu.",
                correct="Idź do domu.",
                note="Temat miękki wymaga znaku diakrytycznego: idź.",
            ),
            GrammarMistake(
                wrong="Proszę pani, usiądź.",
                correct="Proszę pani, niech pani usiądzie.",
                note="Z formą pani nie łączymy drugiej osoby; używamy niech pani + trzecia osoba.",
            ),
        ],
        related=["musiec-powinien", "konstrukcje-bezokolicznikowe"],
    ),
    GrammarTopic(
        slug="narzednik",
        title="Narzędnik",
        level="A2",
        category="Przypadki",
        summary="Kim? czym? — narzędzie, środek transportu i przedmiot zainteresowania.",
        explanation=(
            "Narzędnik odpowiada na pytania **kim? czym?** i służy do wyrażania narzędzia, środka "
            "transportu, sposobu oraz przedmiotu zainteresowania.\n\n"
            "**Końcówki liczby pojedynczej:**\n"
            "- większość rzeczowników męskich oraz rzeczowniki nijakie: **-em**, niekiedy "
            "ze zmianą tematu (*kot → kotem, chłopiec → chłopcem, okno → oknem*); "
            "po k i g piszemy **-iem** (*Polakiem, pedagogiem*)\n"
            "- rzeczowniki żeńskie i męskie zakończone na **-a**: **-ą** "
            "(*praca → pracą, ziemia → ziemią, kolega → kolegą, kierowca → kierowcą*)\n\n"
            "**Liczba mnoga:** zwykle **-ami** (*pociągami, kobietami*), a w nielicznej grupie "
            "**-mi** (*dziećmi, ludźmi, końmi, braćmi*).\n\n"
            "Narzędnika wymagają czasowniki **interesować się** i **zajmować się**. Środek "
            "transportu także wyrażamy narzędnikiem, po czasownikach **jechać, lecieć, płynąć**: "
            "*Interesuję się historią. Jadę tramwajem.* Narzędnik występuje też po przyimkach "
            "*z, nad, pod, przed, za, między*."
        ),
        structure="kim? czym? → zwykle -em (m./n.) · -ą (ż. i m. na -a) · -ami / -mi (lm.)",
        rules=[
            "Rzeczowniki żeńskie i męskie na -a mają w narzędniku liczby pojedynczej -ą: "
            "z kolegą, z kierowcą.",
            "Narzędnik liczby mnogiej ma zwykle końcówkę -ami, a nieliczne wyrazy -mi.",
            "Środek transportu wyrażamy narzędnikiem bez przyimka: jadę pociągiem.",
            "Po czasownikach interesować się i zajmować się używamy narzędnika.",
        ],
        examples=[
            GrammarExample(text="Jadę do pracy tramwajem."),
            GrammarExample(text="Interesuję się polską historią."),
            GrammarExample(text="Rozmawialiśmy z nauczycielem o egzaminie."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Jadę pociąg.",
                correct="Jadę pociągiem.",
                note="Środek transportu wymaga narzędnika.",
            ),
            GrammarMistake(
                wrong="Interesuję się muzyka.",
                correct="Interesuję się muzyką.",
                note="Po interesować się używamy narzędnika z końcówką -ą w rodzaju żeńskim.",
            ),
        ],
        related=["przyimki-narzednik", "miejscownik-przyimki", "celownik"],
    ),
    GrammarTopic(
        slug="przyimki-narzednik",
        title="Przyimki z narzędnikiem",
        level="A2",
        category="Przyimki",
        summary="Z, nad, pod, przed, za, między — położenie i towarzystwo w narzędniku.",
        explanation=(
            "Przyimki **z, nad, pod, przed, za, między** łączą się z narzędnikiem, gdy opisują "
            "**stałe położenie**: *z przyjacielem, nad jeziorem, pod stołem, przed domem, za "
            "rogiem, między nami*.\n\n"
            "Gdy wskazujemy **kierunek ruchu**, przyimki nad, pod, przed i za wymagają biernika: "
            "*Idę nad jezioro. Wchodzę pod stół. Wychodzę przed dom.*\n\n"
            "Przyimek **z** ma dwa znaczenia: towarzystwo (*z bratem* — narzędnik) i pochodzenie "
            "(*z Warszawy* — dopełniacz).\n\n"
            "Przyimek **za** z narzędnikiem znaczy „z tyłu, poza czymś” (*za miastem*), a z "
            "biernikiem — „w zamian za” (*za bilet*) lub kierunek (*za róg*)."
        ),
        structure="z + N. (towarzystwo) · nad / pod / przed / za + N. (położenie)\nruch: nad / "
        "pod / przed / za + B.",
        rules=[
            "Przyimki nad, pod, przed, za z narzędnikiem oznaczają miejsce, nie kierunek.",
            "Przyimek z w znaczeniu towarzystwa wymaga narzędnika.",
            "Przyimek z w znaczeniu pochodzenia łączy się z dopełniaczem.",
            "Między występuje z narzędnikiem: między nami, między drzewami.",
        ],
        examples=[
            GrammarExample(text="Mieszkam za miastem, niedaleko lasu."),
            GrammarExample(text="Stań przed lustrem i powtórz zdanie."),
            GrammarExample(text="Rozmawiam z koleżanką o pracy."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Idę z kolega do kina.",
                correct="Idę z kolegą do kina.",
                note="Po przyimku z w znaczeniu towarzystwa używamy narzędnika.",
            ),
            GrammarMistake(
                wrong="Wracam z Polska.",
                correct="Wracam z Polski.",
                note="Przyimek z w znaczeniu pochodzenia łączy się z dopełniaczem.",
            ),
        ],
        related=["narzednik", "miejscownik-przyimki", "dopelniacz"],
    ),
    GrammarTopic(
        slug="czasowniki-prefiksalne",
        title="Czasowniki z przedrostkami",
        level="A2",
        category="Czasowniki",
        summary="Przy-, wy-, do-, prze-, w-, od-, po- i ich znaczenie kierunkowe.",
        explanation=(
            "Przedrostki zmieniają znaczenie czasownika i najczęściej tworzą **aspekt dokonany**: "
            "*jechać → przyjechać, wyjechać, dojechać, przejechać*.\n\n"
            "**Najważniejsze przedrostki ruchu:**\n"
            "- *przy-* dotarcie: *przyjechać, przyjść*\n"
            "- *wy-* wyjście na zewnątrz: *wyjechać, wyjść*\n"
            "- *do-* osiągnięcie celu: *dojechać, dojść*\n"
            "- *prze-* przejście na drugą stronę: *przejechać, przejść*\n"
            "- *w-* wejście do środka: *wjechać, wejść*\n"
            "- *od-* oddalenie: *odjechać, odejść*\n"
            "- *po-* krótki ruch lub początek: *pojechać, pójść*\n\n"
            "Ten sam przedrostek zmienia też znaczenie czasowników nieruchu: *pisać → podpisać, "
            "przepisać, dopisać*. Czasowniki z przedrostkiem mają zwykle niedokonane pary: "
            "*przyjeżdżać, wychodzić, dochodzić*."
        ),
        structure="przedrostek + czasownik podstawowy\nprzy- · wy- · do- · prze- · w- · od- · po-",
        rules=[
            "Przedrostki ruchu precyzują kierunek: przyjechać do kogoś, wyjechać z domu.",
            "Czasowniki z przedrostkiem są zwykle dokonane, ale wiele ma pary niedokonane.",
            "Przedrostek prze- oznacza przejście przez coś lub na drugą stronę.",
            "Przedrostek po- tworzy formę dokonaną czasowników ruchu: iść → pójść.",
        ],
        examples=[
            GrammarExample(text="Przyjechałem do Krakowa wczoraj wieczorem."),
            GrammarExample(text="Wyszedł z domu bez parasola."),
            GrammarExample(text="Musimy przesiąść się na drugi autobus."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wczoraj przyjechałem w Krakowa.",
                correct="Wczoraj przyjechałem do Krakowa.",
                note="Cel podróży do miasta wyrażamy przez do + dopełniacz: do Krakowa.",
            ),
            GrammarMistake(
                wrong="Wsiadłem z pociągu.",
                correct="Wysiadłem z pociągu.",
                note="Wsiadać znaczy wchodzić do środka; wysiadać — opuszczać pojazd.",
            ),
        ],
        related=["aspekt-wprowadzenie", "przyimki-narzednik", "czas-przyszly-niedokonany"],
    ),
    GrammarTopic(
        slug="musiec-powinien",
        title="Musieć, powinien, wolno",
        level="A2",
        category="Czasowniki",
        summary="Obowiązek, powinność i zakaz wyrażane czasownikami modalnymi.",
        explanation=(
            "**Musieć** wyraża silny obowiązek i odmienia się jak czasownik teraźniejszy: "
            "*muszę, musisz, musi, musimy, musicie, muszą*: *Muszę iść do pracy.*\n\n"
            "**Powinien** wyraża powinność lub radę i odmienia się przez rodzaj: *powinienem, "
            "powinieneś, powinien; powinnam, powinnaś, powinna; powinniśmy, powinniście, "
            "powinni / powinnyśmy, powinnyście, powinny*.\n\n"
            "**Wolno** i **nie wolno** wyrażają pozwolenie i zakaz: *Czy wolno tu palić? Nie "
            "wolno.*\n\n"
            "**Nie trzeba** znaczy brak konieczności, a nie zakaz: *Nie trzeba czekać, pociąg "
            "odjeżdża od razu.*"
        ),
        structure="muszę + bezokolicznik\npowinienem / powinnam + bezokolicznik\nwolno / nie wolno "
        "+ bezokolicznik",
        rules=[
            "Po musieć stoi bezokolicznik, nigdy forma osobowa drugiego czasownika.",
            "Powinien ma formy rodzajowe: powinienem, powinnam, powinniśmy, powinnyśmy.",
            "Nie wolno wyraża zakaz, a nie trzeba — brak konieczności.",
            "Musieć oznacza silny przymus, powinien — radę lub oczekiwanie.",
        ],
        examples=[
            GrammarExample(text="Muszę skończyć raport do piątku."),
            GrammarExample(text="Powinieneś odpocząć, wyglądasz na zmęczonego."),
            GrammarExample(text="Nie wolno palić w tym budynku."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Muszę idę do pracy.",
                correct="Muszę iść do pracy.",
                note="Po musieć używamy bezokolicznika, nie formy osobowej.",
            ),
            GrammarMistake(
                wrong="Ona powinien odpocząć.",
                correct="Ona powinna odpocząć.",
                note="Powinien odmienia się przez rodzaj: powinna dla rodzaju żeńskiego.",
            ),
        ],
        related=["konstrukcje-bezokolicznikowe", "tryb-rozka", "przyimki-czasu"],
    ),
    GrammarTopic(
        slug="konstrukcje-bezokolicznikowe",
        title="Konstrukcje z bezokolicznikiem",
        level="A2",
        category="Składnia",
        summary="Warto spróbować, trudno powiedzieć, można wejść — zdania bez podmiotu.",
        explanation=(
            "Bezokolicznik łączy się z czasownikami modalnymi i fazowymi (*muszę, mogę, chcę, "
            "lubię, zaczynam, przestaję*) oraz z wyrażeniami oceniającymi.\n\n"
            "**Konstrukcje bezosobowe:** *łatwo zapomnieć, trudno powiedzieć, warto spróbować, "
            "można wejść, trzeba poczekać, szkoda tracić czas*.\n\n"
            "W takich zdaniach nie ma podmiotu w mianowniku, a wyrażenie oceniające ma stałą "
            "formę: *Można tu usiąść. Trzeba się spieszyć. Nie wolno palić.*\n\n"
            "Neutralnie wyrażenie oceniające poprzedza bezokolicznik: *trudno uwierzyć*. "
            "Szyk może się zmieniać dla podkreślenia: *Uwierzyć trudno*, *Zapomnieć o tym łatwo*."
        ),
        structure="łatwo / trudno / warto / można / trzeba + bezokolicznik",
        rules=[
            "Po czasownikach chcieć, móc, musieć i lubić stoi bezokolicznik.",
            "Zdania z można, trzeba i warto nie mają podmiotu i są nieosobowe.",
            "Wyrażenie oceniające zwykle poprzedza bezokolicznik, lecz szyk jest elastyczny.",
            "Bezokolicznik nie odmienia się, więc nie przyjmuje końcówek osoby ani rodzaju.",
        ],
        examples=[
            GrammarExample(text="Warto zarezerwować bilet wcześniej."),
            GrammarExample(text="Trudno powiedzieć, czy zdążymy."),
            GrammarExample(text="Można płacić kartą przy wejściu."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Warto rezerwujemy bilet wcześniej.",
                correct="Warto zarezerwować bilet wcześniej.",
                note="Po warto używamy bezokolicznika, nie formy osobowej.",
            ),
            GrammarMistake(
                wrong="Trzeba idziemy teraz.",
                correct="Trzeba iść teraz.",
                note="Trzeba łączy się z bezokolicznikiem.",
            ),
        ],
        related=["musiec-powinien", "tryb-rozka", "przyslowki"],
    ),
    GrammarTopic(
        slug="przyimki-czasu",
        title="Przyimki czasu",
        level="A2",
        category="Przyimki",
        summary="Przed, po, od, do, w, o, za — przypadki i znaczenie w wyrażeniach czasu.",
        explanation=(
            "Przyimki czasu wymagają różnych przypadków.\n\n"
            "**przed + narzędnik:** *przed pracą, przed obiadem*\n"
            "**po + miejscownik:** *po pracy, po spotkaniu*\n"
            "**od + dopełniacz:** *od poniedziałku, od rana*\n"
            "**do + dopełniacz:** *do piątku, do wieczora*\n"
            "**w + miejscownik (miesiące, lata) lub biernik (dni tygodnia):** *w styczniu, w 2026 "
            "roku, w poniedziałek*\n"
            "**o + miejscownik (godziny):** *o siódmej, o wpół do ósmej*\n"
            "**za + biernik (przyszłość):** *za godzinę, za tydzień*\n\n"
            "*Przed* i *po* określają kolejność zdarzeń, *za* — odstęp czasu liczony od teraz."
        ),
        structure="przed + N. · po + Ms. · od / do + D. · o + Ms. · za + B.",
        rules=[
            "Przed łączy się z narzędnikiem, a po z miejscownikiem.",
            "Od i do wymagają dopełniacza: od rana, do wieczora.",
            "Godzinę wyrażamy przyimkiem o i miejscownikiem: o ósmej.",
            "Za z biernikiem wskazuje czas przyszły liczony od teraz: za dwa dni.",
        ],
        examples=[
            GrammarExample(text="Spotkajmy się przed wejściem o szóstej."),
            GrammarExample(text="Po obiedzie idziemy na spacer."),
            GrammarExample(text="Wracam do domu za tydzień."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Spotkajmy się po obiad.",
                correct="Spotkajmy się po obiedzie.",
                note="Po wymaga miejscownika.",
            ),
            GrammarMistake(
                wrong="Pracuję tu od poniedziałek.",
                correct="Pracuję tu od poniedziałku.",
                note="Od łączy się z dopełniaczem.",
            ),
        ],
        related=["przyimki-narzednik", "miejscownik-przyimki", "czas-przyszly-niedokonany"],
    ),
    GrammarTopic(
        slug="czas-przyszly-niedokonany",
        title="Czas przyszły niedokonany",
        level="A2",
        category="Czasowniki",
        summary="Będę czytać, będę czytał — przyszłość procesów i nawyków.",
        explanation=(
            "Czas przyszły niedokonany tworzymy dwoma sposobami:\n"
            "- **będę + bezokolicznik:** *będę czytać, będziesz pracować*\n"
            "- **będę + forma przeszła:** *będę czytał, będę czytała* — z odmianą przez rodzaj\n\n"
            "Odmiana czasownika **być** w czasie przyszłym: **będę, będziesz, będzie, będziemy, "
            "będziecie, będą.**\n\n"
            "Czasowniki dokonane tworzą przyszłość prostą, bez czasownika być: *przeczytam, "
            "napiszę, przyjdą*.\n\n"
            "Konstrukcja z bezokolicznikiem jest neutralna, a forma przeszła podkreśla rodzaj "
            "wykonawcy: *Będę pracować w domu* i *Będę pracowała w domu* znaczą to samo, ale "
            "druga forma wskazuje kobietę."
        ),
        structure="będę / będziesz / będzie + bezokolicznik\nbędę / będziesz / będzie + forma "
        "przeszła (czytał / czytała)",
        rules=[
            "Czas przyszły niedokonany wymaga formy być: będę, będziesz, będzie.",
            "Po będzie stoi bezokolicznik albo forma przeszła z końcówką rodzajową.",
            "Czasowniki dokonane nie łączą się z być w czasie przyszłym.",
            "Przyszłość niedokonana opisuje proces i powtarzanie: będę codziennie biegać.",
        ],
        examples=[
            GrammarExample(text="Jutro będę pracować od rana."),
            GrammarExample(text="W weekend będziemy odpoczywać nad jeziorem."),
            GrammarExample(text="Będziesz się uczyć czy oglądać film?"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Jutro będę przeczytać książkę.",
                correct="Jutro przeczytam książkę.",
                note="Czasownik dokonany tworzy przyszłość prostą bez czasownika być.",
            ),
            GrammarMistake(
                wrong="Ja będę pracuję jutro.",
                correct="Będę pracować jutro.",
                note="Po będę stoi bezokolicznik lub forma przeszła, nie forma teraźniejsza.",
            ),
        ],
        related=["aspekt-wprowadzenie", "czasowniki-prefiksalne", "tryb-warunkowy"],
    ),
    GrammarTopic(
        slug="tryb-warunkowy",
        title="Tryb warunkowy",
        level="A2",
        category="Czasowniki",
        summary="Chciałbym, moglibyśmy, gdybym miał czas — warunek i uprzejma prośba.",
        explanation=(
            "Tryb warunkowy tworzymy z **formy czasu przeszłego i cząstki by**, która odmienia "
            "się przez osoby: *bym, byś, by, byśmy, byście, by*.\n\n"
            "**Chciałbym / chciałabym** to uprzejme życzenie, a **moglibyśmy** — propozycja: "
            "*Chciałbym zamówić kawę. Moglibyśmy spotkać się w piątek?*\n\n"
            "**Zdanie warunkowe:** warunek możliwy wyrażamy czasem przyszłym (*Jeśli będę miał "
            "czas, przyjdę*), a warunek nierzeczywisty — trybem warunkowym w obu członach: "
            "*Gdybym miał czas, poszedłbym do kina.*\n\n"
            "Cząstkę by piszemy łącznie z formą czasownika: *chciałbym, poszlibyśmy*. Po zaimku "
            "lub spójniku stoi osobno: *ja bym chciał*."
        ),
        structure="forma przeszła + bym / byś / by / byśmy / byście / by\ngdyby + forma przeszła, "
        "... + tryb warunkowy",
        rules=[
            "Cząstka by odmienia się przez osoby: bym, byś, by, byśmy, byście, by.",
            "Cząstkę by piszemy łącznie z czasownikiem: chciałbym, poszlibyśmy.",
            "W warunku nierzeczywistym tryb warunkowy występuje w obu członach zdania.",
            "Po jeśli możliwy jest czas przyszły: jeśli będę miał czas, przyjdę.",
        ],
        examples=[
            GrammarExample(text="Chciałbym zamówić kawę."),
            GrammarExample(text="Gdybym miał więcej czasu, uczyłbym się hiszpańskiego."),
            GrammarExample(text="Moglibyśmy spotkać się w piątek?"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gdybym miał czas, pójdę do kina.",
                correct="Gdybym miał czas, poszedłbym do kina.",
                note="W warunku nierzeczywistym oba człony wymagają trybu warunkowego.",
            ),
            GrammarMistake(
                wrong="Ja bym chciałbym kawę.",
                correct="Ja bym chciał kawę. / Chciałbym kawę.",
                note="Nie powtarzamy by przy tym samym orzeczeniu: ja bym chciał albo chciałbym.",
            ),
        ],
        related=["zdania-z-ze", "musiec-powinien", "czas-przyszly-niedokonany"],
    ),
    GrammarTopic(
        slug="zdania-z-ze",
        title="Zdania ze spójnikiem że",
        level="A2",
        category="Składnia",
        summary="Myślę, że...; nie wiem, czy...; chcę, żeby... — mowa zależna i życzenia.",
        explanation=(
            "Spójnik **że** wprowadza zdanie podrzędne twierdzące: *Myślę, że masz rację. Wiem, "
            "że spóźnię się.*\n\n"
            "**Czy** wprowadza zdanie zależne pytajne: *Nie wiem, czy przyjdzie. Zapytaj, czy "
            "mają bilety.*\n\n"
            "**Żeby** wyraża życzenie, prośbę lub cel, zwłaszcza gdy podmioty są różne: *Chcę, "
            "żebyś przyszedł. Mówię głośno, żeby wszyscy słyszeli.*\n\n"
            "Po że i czy następuje zwykle tryb oznajmujący, a po żeby — forma na -ł "
            "lub bezokolicznik: żeby przyszedł, żeby odpocząć. Nie dodajemy drugiego by. Przed "
            "spójnikiem stawiamy przecinek: *Myślę, że to dobry pomysł.*"
        ),
        structure="myślę / wiem / sądzę, że + zdanie oznajmujące\nnie wiem, czy + zdanie pytajne\n"
        "chcę, żeby + forma na -ł (żebyś przyszedł)",
        rules=[
            "Po czasownikach myśleć, wiedzieć i sądzić używamy że.",
            "Zdanie zależne pytajne wprowadza czy.",
            "Żeby stosujemy przy życzeniu lub celu, szczególnie gdy podmioty są różne.",
            "Przed że, czy i żeby stawiamy przecinek.",
        ],
        examples=[
            GrammarExample(text="Myślę, że ten film warto zobaczyć."),
            GrammarExample(text="Nie wiem, czy zdążę na pociąg."),
            GrammarExample(text="Chcę, żebyś mi pomógł w przeprowadzce."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Myślę, żeby to dobry pomysł.",
                correct="Myślę, że to dobry pomysł.",
                note="Po myślę z twierdzeniem używamy że, nie żeby.",
            ),
            GrammarMistake(
                wrong="Nie wiem, czy on przyjdziesz jutro.",
                correct="Nie wiem, czy on przyjdzie jutro.",
                note="Orzeczenie pytania zależnego zgadza się z podmiotem: on przyjdzie.",
            ),
        ],
        related=["tryb-warunkowy", "konstrukcje-bezokolicznikowe"],
    ),
    GrammarTopic(
        slug="miejscownik-przyimki",
        title="Miejscownik z przyimkami",
        level="A2",
        category="Przypadki",
        summary="W Krakowie, na stole, przy oknie, o pracy — miejsce i temat rozmowy.",
        explanation=(
            "Miejscownik występuje **wyłącznie z przyimkami**: *w, na, przy, o, po*.\n\n"
            "**Końcówki liczby pojedynczej:**\n"
            "- rzeczowniki męskie zakończone na spółgłoskę i rzeczowniki nijakie: **-e** "
            "ze zmianą tematu (*Kraków → Krakowie, stół → stole, miasto → mieście*) albo "
            "**-u**. Końcówkę **-u** mają m.in. tematy na k, g, ch (*roku, pociągu, "
            "dachu*) oraz miękkie i stwardniałe (*nauczycielu, mieszkaniu, morzu*). "
            "Są też formy wymagające zapamiętania, np. *dom → domu*\n"
            "- rzeczowniki żeńskie i męskie zakończone na **-a**: **-e**, często ze zmianą "
            "spółgłoski (*woda → wodzie, siostra → siostrze, kolega → koledze*), "
            "lub **-y / -i**, np. po spółgłoskach stwardniałych **-y** "
            "(*praca → pracy, ulica → ulicy*), a po miękkich **-i** (*ziemia → ziemi*). "
            "Formy te są takie jak w celowniku\n\n"
            "**Liczba mnoga:** **-ach** (*miastach, pracach, domach*).\n\n"
            "**Znaczenia przyimków:** *w* — wnętrze i większe obszary (*w Polsce, w kinie*), "
            "*na* — powierzchnie i otwarte przestrzenie (*na stole, na rynku*), *przy* — bliskość "
            "(*przy oknie*), *o* — temat rozmowy (*rozmawiamy o pracy*)."
        ),
        structure="w / na / przy / o / po + miejscownik\n-e / -u (m. na spółgłoskę i n.) · "
        "-e / -y / -i (ż. i m. na -a) · -ach (lm.)",
        rules=[
            "Miejscownik nie występuje bez przyimka.",
            "Tematy męskie zakończone na k, g i ch przyjmują w miejscowniku końcówkę -u.",
            "Końcówka -u występuje też w formach nauczycielu, mieszkaniu, morzu; "
            "nie jest ograniczona do tematów na k, g i ch.",
            "Po przyimku w z nazwą miasta używamy miejscownika: w Warszawie.",
            "Temat rozmowy wyrażamy przyimkiem o i miejscownikiem: o filmie, o pracy.",
        ],
        examples=[
            GrammarExample(text="Mieszkam w Krakowie od pięciu lat."),
            GrammarExample(text="Rozmawialiśmy o nowej pracy."),
            GrammarExample(text="Spotkajmy się przy stacji metra."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mieszkam w Kraków.",
                correct="Mieszkam w Krakowie.",
                note="Po przyimku w nazwa miasta stoi w miejscowniku.",
            ),
            GrammarMistake(
                wrong="Rozmawialiśmy o nową pracę.",
                correct="Rozmawialiśmy o nowej pracy.",
                note="Po przyimku o używamy miejscownika, także w formie przymiotnika.",
            ),
        ],
        related=["przyimki-narzednik", "przyimki-czasu", "stopniowanie-przymiotnikow"],
    ),
    GrammarTopic(
        slug="stopniowanie-przymiotnikow",
        title="Stopniowanie przymiotników",
        level="A2",
        category="Przymiotniki",
        summary="Tańszy, najtańszy, lepszy — stopień wyższy i najwyższy oraz porównania.",
        explanation=(
            "**Stopień wyższy** tworzymy najczęściej przez dodanie **-szy** lub **-iejszy** do "
            "tematu: *tani → tańszy, ładny → ładniejszy, ciekawy → ciekawszy*.\n\n"
            "**Stopień najwyższy** powstaje przez dodanie przedrostka **naj-** do formy wyższej: "
            "*najtańszy, najładniejszy, najciekawszy*.\n\n"
            "**Formy nieregularne:** dobry → lepszy → najlepszy, zły → gorszy → najgorszy, duży → "
            "większy → największy, mały → mniejszy → najmniejszy, wysoki → wyższy → najwyższy.\n\n"
            "Porównanie tworzymy na dwa sposoby: **od + dopełniacz** (*większy od brata*) albo "
            "**niż**, po którym przypadek zależy od funkcji porównywanego członu "
            "(*większy niż brat*, ale *lubię ją bardziej niż jego*). Równość wyraża *tak ... jak*: *tak wysoki "
            "jak ja*."
        ),
        structure="-szy / -iejszy → stopień wyższy\nnaj- + stopień wyższy\nwiększy od + D. · "
        "większy niż + M.",
        rules=[
            "Stopień najwyższy tworzymy regularnie przez dodanie naj- do stopnia wyższego.",
            "Po od używamy dopełniacza. Niż nie narzuca przypadku: wyższy niż ja, "
            "ale pomagam jej częściej niż jemu.",
            "Formy nieregularne trzeba zapamiętać: lepszy, gorszy, większy, mniejszy.",
            "Równość wyrażamy konstrukcją tak ... jak lub taki sam jak.",
        ],
        examples=[
            GrammarExample(text="Ten pokój jest większy od mojego."),
            GrammarExample(text="To najciekawsza książka, jaką czytałem."),
            GrammarExample(text="Ona jest tak samo wysoka jak ja."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mój brat jest wyższy niż mnie.",
                correct="Mój brat jest wyższy niż ja. / wyższy ode mnie.",
                note="Tu porównujemy podmioty, więc niż ja; po ode używamy dopełniacza mnie.",
            ),
            GrammarMistake(
                wrong="To najbardziej lepszy wybór.",
                correct="To najlepszy wybór.",
                note="Lepszy jest już stopniem wyższym; naj- dodajemy do formy wyższej.",
            ),
        ],
        related=["przyslowki", "miejscownik-przyimki"],
    ),
    GrammarTopic(
        slug="przyslowki",
        title="Przysłówki i ich stopniowanie",
        level="A2",
        category="Przysłówki",
        summary="Szybko, szybciej, najszybciej — jak opisujemy sposób wykonywania czynności.",
        explanation=(
            "Przysłówki tworzymy od przymiotników przez dodanie **-o** lub **-e**: *szybki → "
            "szybko, ładny → ładnie, ciepły → ciepło*.\n\n"
            "**Stopniowanie regularne:** stopień wyższy ma końcówkę **-ej**, a najwyższy dodaje "
            "**naj-**: *szybko → szybciej → najszybciej, cicho → ciszej → najciszej*.\n\n"
            "**Formy nieregularne:** dobrze → lepiej → najlepiej, źle → gorzej → najgorzej, dużo "
            "→ więcej → najwięcej, mało → mniej → najmniej, daleko → dalej → najdalej.\n\n"
            "Przysłówek opisuje **jak** wykonywana jest czynność, przymiotnik — **jaki** jest "
            "rzeczownik: *mówi głośno* / *głośny głos*."
        ),
        structure="przymiotnik + -o / -e → przysłówek\nstopień wyższy: -ej · najwyższy: naj-",
        rules=[
            "Przysłówki tworzymy od przymiotników końcówkami -o lub -e; formy warto sprawdzać.",
            "Stopień wyższy przysłówka tworzymy zwykle końcówką -ej.",
            "Formy nieregularne: dobrze — lepiej, źle — gorzej, dużo — więcej.",
            "Przysłówek opisuje czynność, przymiotnik — rzeczownik.",
        ],
        examples=[
            GrammarExample(text="Mów wolniej, proszę."),
            GrammarExample(text="Wszyscy pracowaliśmy szybciej niż wczoraj."),
            GrammarExample(text="Ona śpiewa najlepiej w całej klasie."),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mówisz bardzo szybki.",
                correct="Mówisz bardzo szybko.",
                note="Sposób wykonywania czynności opisuje przysłówek, nie przymiotnik.",
            ),
            GrammarMistake(
                wrong="Dziś czuję się bardziej dobrze.",
                correct="Dziś czuję się lepiej.",
                note="Dobrze ma nieregularny stopień wyższy: lepiej.",
            ),
        ],
        related=["stopniowanie-przymiotnikow", "konstrukcje-bezokolicznikowe"],
    ),
]
