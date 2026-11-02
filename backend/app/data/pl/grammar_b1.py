"""Polish grammar topics — B1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="aspekt-pary",
        title="Aspekt czasownika: pary aspektowe",
        level="B1",
        category="Czasownik",
        summary=(
            "Jak dobierać czasowniki niedokonane i dokonane, żeby oddać przebieg, "
            "nawyk i efekt czynności."
        ),
        explanation=(
            "Aspekt jest w polsku obowiązkowy: każda czynność wymaga wyboru między formą "
            "**niedokonaną** i **dokonaną**.\n\n"
            "**Niedokonany** (pisać, czytać, robić) opisuje:\n"
            "- przebieg i trwanie: *Pisałem list przez godzinę.*\n"
            "- nawyk i powtarzalność: *Codziennie czytam gazetę.*\n"
            "- czynność bez wskazania efektu: *Właśnie gotuję obiad.*\n\n"
            "**Dokonany** (napisać, przeczytać, zrobić) opisuje:\n"
            "- wynik i zakończenie: *Napisałem list.*\n"
            "- jednorazowe, zamknięte zdarzenie: *Przeczytałam tę książkę wczoraj.*\n\n"
            "Pary powstają przez dodanie przedrostka (pisać → napisać) albo przez zmianę "
            "tematu (brać → wziąć, mówić → powiedzieć)."
        ),
        structure=(
            "niedokonany: robić, pisać, mówić, czytać\n"
            "dokonany: zrobić, napisać, powiedzieć, przeczytać"
        ),
        rules=[
            "Czasowniki dokonane nie mają czasu teraźniejszego: forma piszę należy do "
            "czasownika pisać, a napiszę to czas przyszły.",
            "Po zaczynać, kończyć i przestawać stoi bezokolicznik niedokonany: "
            "zaczynam pisać, skończyłem czytać.",
            "Przeczenie dopuszcza oba aspekty: nie pisałem raportu opisuje brak czynności, "
            "a nie napisałem raportu — brak jej ukończenia.",
            "Aspekt wybiera mówiący, a nie czas gramatyczny: wczoraj czytałem i wczoraj "
            "przeczytałem są poprawne, ale znaczą co innego.",
        ],
        examples=[
            GrammarExample(
                text="Wczoraj pisałem raport przez trzy godziny.",
                translation=None,
                note="przebieg, czas trwania",
            ),
            GrammarExample(
                text="Wreszcie napisałem raport i wysłałem go szefowi.",
                translation=None,
                note="wynik, zakończenie",
            ),
            GrammarExample(
                text="Ona zawsze kupuje pieczywo w tej samej piekarni.",
                translation=None,
                note="nawyk",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wczoraj napisałem raport przez trzy godziny.",
                correct="Wczoraj pisałem raport przez trzy godziny.",
                note="Określenie czasu trwania (przez trzy godziny) wymaga czasownika "
                "niedokonanego.",
            ),
            GrammarMistake(
                wrong="Zaczynam napisać raport.",
                correct="Zaczynam pisać raport.",
                note="Po zaczynać stoi bezokolicznik niedokonany; napisać opisuje wynik, "
                "a nie sam proces.",
            ),
        ],
        related=["zdania-czasowe", "prefiksy-znaczenia", "strona-bierna"],
    ),
    GrammarTopic(
        slug="zdania-wzgledne",
        title="Zdania względne z który",
        level="B1",
        category="Składnia",
        summary="Łączenie zdań za pomocą który, która, które, których, z przyimkami i bez.",
        explanation=(
            "Zdanie względne opisuje rzeczownik ze zdania głównego i zaczyna się od "
            "**który**, odmienianego jak przymiotnik.\n\n"
            "Formy mianownika: *który, która, które; którzy, które*.\n\n"
            "- *To jest kolega, **który** pracuje w banku.*\n"
            "- *Kupiłam książkę, **która** ma piękne ilustracje.*\n"
            "- *Znam ludzi, **którzy** mieszkają w Gdańsku.*\n\n"
            "Zaimek przejmuje rodzaj i liczbę od rzeczownika, do którego się odnosi, a "
            "przypadek zależy od jego funkcji w zdaniu względnym: *Rozmawiałem z kobietą, "
            "**która** uczy polskiego* (mianownik, bo który jest podmiotem)."
        ),
        structure="rzeczownik + który/która/które + czasownik w formie zgodnej z rzeczownikiem",
        rules=[
            "Który odmienia się przez przypadki: którego, któremu, którym, z którym.",
            "Rodzaj i liczba zależą od wyrazu określanego, a nie od wyrazu stojącego " "najbliżej.",
            "Przyimek stoi przed zaimkiem: z którym, o której, do których.",
            "Mówione „co” zamiast którego jest potoczne: ten pan, co tu pracuje.",
        ],
        examples=[
            GrammarExample(
                text="Mam sąsiada, który codziennie biega w parku.",
                translation=None,
            ),
            GrammarExample(
                text="To jest projekt, nad którym pracowaliśmy od miesiąca.",
                translation=None,
                note="przyimek + narzędnik",
            ),
            GrammarExample(
                text="Nie znam nikogo, kto umiałby to naprawić.",
                translation=None,
                note="kto po zaimku nieokreślonym",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Rozmawiałem z kobietą, która uczą polskiego.",
                correct="Rozmawiałem z kobietą, która uczy polskiego.",
                note="Orzeczenie zgadza się z podmiotem która: trzecia osoba liczby pojedynczej uczy.",
            ),
            GrammarMistake(
                wrong="To jest kolega, z który pracuję.",
                correct="To jest kolega, z którym pracuję.",
                note="Po przyimku z wymagana jest forma narzędnika: którym.",
            ),
        ],
        related=["zaimki-wzgledne", "spojniki", "zdania-okolicznikowe"],
    ),
    GrammarTopic(
        slug="zaimki-wzgledne",
        title="Zaimki względne: kto, co, gdzie, kiedy",
        level="B1",
        category="Składnia",
        summary="Zdania względne wprowadzane zaimkami kto, co, gdzie, kiedy, jak.",
        explanation=(
            "Poza **który** zdania względne wprowadzają zaimki **kto**, **co**, **gdzie**, "
            "**kiedy** i **jak**.\n\n"
            "- *Kto pyta, nie błądzi.* (kto = osoba nieokreślona)\n"
            "- *To, **co** powiedziałeś, było ważne.* (co = treść wypowiedzi)\n"
            "- *Wracam do miasta, **gdzie** się urodziłem.*\n"
            "- *Pamiętam dzień, **kiedy** się poznaliśmy.*\n\n"
            "Ważna różnica: **co** odnosi się do rzeczy, zjawisk i całych zdań, a **kto** "
            "wyłącznie do osób. Po przyimku zaimek się odmienia: *z kim*, *o czym*, "
            "*do kogo*."
        ),
        structure="zaimek względny (kto, co, gdzie, kiedy) + zdanie podrzędne",
        rules=[
            "Kto odnosi się tylko do osób, co do rzeczy, zjawisk i treści wypowiedzi.",
            "Zaimek względny odmienia się przez przypadki: kogo, komu, kim; czego, czemu, " "czym.",
            "Gdzie i kiedy zastępują wyrażenia przyimkowe: w którym miejscu, w którym " "momencie.",
            "Zdanie z zaimkiem względnym może pełnić funkcję podmiotu: Kto rano wstaje, "
            "temu się wiedzie.",
        ],
        examples=[
            GrammarExample(
                text="To, co powiedziała, zabrzmiało jak ostrzeżenie.",
                translation=None,
            ),
            GrammarExample(
                text="Nie wiem, gdzie zostawiłem klucze.",
                translation=None,
            ),
            GrammarExample(
                text="Kto dużo czyta, ten pisze lepiej.",
                translation=None,
                note="zaimek kto w funkcji podmiotu",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="To, kto powiedziałeś, było ważne.",
                correct="To, co powiedziałeś, było ważne.",
                note="Do treści wypowiedzi odnosi się co, nie kto.",
            ),
            GrammarMistake(
                wrong="Miasto, gdzie w nim mieszkam, jest duże.",
                correct="Miasto, w którym mieszkam, jest duże.",
                note="Gdzie zawiera już znaczenie „w którym”, więc nie dodajemy zaimka w nim.",
            ),
        ],
        related=["zdania-wzgledne", "spojniki", "partykuly"],
    ),
    GrammarTopic(
        slug="strona-bierna",
        title="Strona bierna: budowa",
        level="B1",
        category="Czasownik",
        summary="Być lub zostać z imiesłowem biernym oraz sposoby wskazywania wykonawcy.",
        explanation=(
            "Stronę bierną tworzymy z **być** albo **zostać** i **imiesłowu biernego**, "
            "który zgadza się z podmiotem w rodzaju i liczbie.\n\n"
            "- *Raport **jest przygotowywany** przez zespół.* (czynność trwająca)\n"
            "- *Raport **został przygotowany** wczoraj.* (zakończona czynność, wynik)\n"
            "- *Drzwi **były zamknięte**.* (opis stanu)\n\n"
            "Wykonawcę wprowadza **przez** + biernik (*przez zespół*, *przez komisję*). "
            "Narzędzie lub środek wyraża **przy pomocy** + dopełniacz "
            "(*przy pomocy programu*).\n\n"
            "Strona bierna jest częstsza w tekstach urzędowych, prasowych i naukowych niż "
            "w codziennej rozmowie."
        ),
        structure="być/zostać (odmienione) + imiesłów bierny (‑ny, ‑ona, ‑one / ‑ty, ‑ta, ‑te)",
        rules=[
            "Zostać + imiesłów bierny opisuje zakończoną czynność: list został wysłany.",
            "Być + imiesłów bierny opisuje stan lub czynność trwającą: list jest wysyłany.",
            "Imiesłów bierny zgadza się z podmiotem: decyzja została podjęta, decyzje "
            "zostały podjęte.",
            "Wykonawcę wprowadza przyimek przez z biernikiem; bez wykonawcy strona bierna "
            "brzmi naturalniej.",
        ],
        examples=[
            GrammarExample(
                text="Nowy most został otwarty w zeszłym tygodniu.",
                translation=None,
            ),
            GrammarExample(
                text="Ten budynek jest codziennie sprzątany.",
                translation=None,
            ),
            GrammarExample(
                text="Umowa została podpisana przez obie strony.",
                translation=None,
                note="wykonawca z przez + biernik",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Raport został przygotowywany przez zespół wczoraj.",
                correct="Raport został przygotowany przez zespół wczoraj.",
                note="Po zostać używamy imiesłowu biernego od czasownika dokonanego, bo "
                "chodzi o wynik.",
            ),
            GrammarMistake(
                wrong="Decyzja został podjęta.",
                correct="Decyzja została podjęta.",
                note="Czasownik pomocniczy zgadza się z podmiotem: decyzja (rodzaj żeński) "
                "→ została.",
            ),
        ],
        related=["strona-bierna-czas", "imieslow-przymiotnikowy", "konstrukcje-bezosobowe"],
    ),
    GrammarTopic(
        slug="imieslow-przymiotnikowy",
        title="Imiesłów przymiotnikowy czynny i bierny",
        level="B1",
        category="Imiesłowy",
        summary="Uczący się student i napisany raport: dwa imiesłowy odmieniane jak przymiotniki.",
        explanation=(
            "**Imiesłów przymiotnikowy czynny** tworzymy od czasowników niedokonanych "
            "końcówką **‑ący** i opisujemy nim wykonawcę: *człowiek **czytający** gazetę*, "
            "*ucząca się młodzież*.\n\n"
            "**Imiesłów przymiotnikowy bierny** tworzymy od czasowników przechodnich "
            "końcówkami **‑ny**, **‑ty**, **‑ony** i opisujemy nim wynik lub stan: "
            "*napisany raport*, *zamknięte drzwi*, *czytana książka*.\n\n"
            "Oba imiesłowy odmieniają się przez przypadki jak przymiotniki: *czytającego "
            "studenta*, *o napisanym raporcie*.\n\n"
            "Od czasowników dokonanych nie tworzymy imiesłowu czynnego: forma *napiszący* "
            "nie istnieje, więc mówimy *student, który napisał raport*."
        ),
        structure=(
            "niedokonany + ‑ący (czytający)\n"
            "przechodni + ‑ny/‑ty/‑ony (napisany, zamknięty, czytany)"
        ),
        rules=[
            "Czynny tworzymy od czasowników niedokonanych: piszący, mówiący, idący.",
            "Bierny tworzymy od czasowników przechodnich: napisany, czytany, zamknięty.",
            "Imiesłowy odmieniają się jak przymiotniki: piszącego, napisanym, otwarte.",
            "Imiesłów bierny z być tworzy stronę bierną, a z rzeczownikiem — zwięzły opis: "
            "raport napisany przez eksperta.",
        ],
        examples=[
            GrammarExample(
                text="Na korytarzu stał student czytający ogłoszenia.",
                translation=None,
            ),
            GrammarExample(
                text="Dokumenty napisane przez prawnika były bardzo precyzyjne.",
                translation=None,
            ),
            GrammarExample(
                text="To zadanie, wykonane w pośpiechu, zawiera błędy.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Student napisający raport właśnie wyszedł.",
                correct="Student, który napisał raport, właśnie wyszedł.",
                note="Od czasowników dokonanych nie tworzymy imiesłowu czynnego; używamy "
                "zdania względnego.",
            ),
            GrammarMistake(
                wrong="Drzwi są zamknięty.",
                correct="Drzwi są zamknięte.",
                note="Imiesłów bierny zgadza się z podmiotem: drzwi (liczba mnoga, nie "
                "męskoosobowa) → zamknięte.",
            ),
        ],
        related=["strona-bierna", "imieslow-przyslowkowy", "rzeczowniki-odczasownikowe"],
    ),
    GrammarTopic(
        slug="mowa-zalezna",
        title="Mowa zależna",
        level="B1",
        category="Składnia",
        summary="Przekazywanie cudzych słów: że, czy, żeby i dopasowanie zaimków.",
        explanation=(
            "W mowie zależnej zdanie podrzędne łączymy spójnikiem **że** (twierdzenia), "
            "**czy** (pytania) lub **żeby** (prośby i polecenia).\n\n"
            "- *Powiedział, **że** szuka pracy.*\n"
            "- *Zapytała, **czy** mam czas.*\n"
            "- *Poprosił, **żebym** przyszedł wcześniej.*\n\n"
            "W polsku **nie ma obowiązku** cofania czasu: *„Jestem zmęczony”* → "
            "*Powiedział, że **jest** zmęczony.* Cofamy czas tylko wtedy, gdy sytuacja "
            "jest ujmowana z innego punktu odniesienia: *Powiedział, że **był** zmęczony* "
            "(np. poprzedniego dnia).\n\n"
            "Zmieniają się natomiast zaimki oraz określenia miejsca i czasu: *jutro → "
            "następnego dnia*, *tu → tam*, *teraz → wtedy*."
        ),
        structure="czasownik mówienia + że / czy / żeby + zdanie podrzędne",
        rules=[
            "Twierdzenia łączy spójnik że, pytania — czy, a prośby i polecenia — żeby.",
            "Przy różnych podmiotach po żeby stoi forma osobowa: żebym przyszedł, żebyś "
            "zadzwoniła.",
            "Czasu nie trzeba cofać, jeśli wypowiedź pozostaje aktualna.",
            "Zaimki i okoliczniki dostosowujemy do punktu widzenia osoby relacjonującej.",
        ],
        examples=[
            GrammarExample(
                text="Powiedział, że wróci około siódmej.",
                translation=None,
            ),
            GrammarExample(
                text="Zapytał, czy mogę mu pomóc.",
                translation=None,
            ),
            GrammarExample(
                text="Poprosiła, żebyśmy nie hałasowali.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Poprosił, żeby przyjdę wcześniej.",
                correct="Poprosił, żebym przyszedł wcześniej.",
                note="Po żeby używamy formy osobowej z ‑by, a nie czasu przyszłego.",
            ),
            GrammarMistake(
                wrong="Zapytała, że mam czas.",
                correct="Zapytała, czy mam czas.",
                note="Pytania zależne wprowadza czy, nie że.",
            ),
        ],
        related=["spojniki", "zdania-celowe", "tryb-warunkowy-zdania"],
    ),
    GrammarTopic(
        slug="tryb-warunkowy-zdania",
        title="Zdania warunkowe z gdyby",
        level="B1",
        category="Tryb warunkowy",
        summary="Gdyby, jeżeli i warunki realne: gdybym miał czas, chodziłbym na siłownię.",
        explanation=(
            "Warunek realny lub prawdopodobny wyrażamy przez **jeżeli/jeśli** z trybem "
            "oznajmującym albo **gdyby** z trybem przypuszczającym.\n\n"
            "- *Jeżeli będzie padać, zostaniemy w domu.* (warunek realny)\n"
            "- *Gdybym miał czas, chodziłbym na siłownię.* (hipoteza o teraźniejszości)\n"
            "- *Gdybyś zadzwonił, uprzedziłbym wszystkich.*\n\n"
            "**Gdyby** łączy się z formami osobowymi: *gdybym, gdybyś, gdyby, gdybyśmy, "
            "gdybyście, gdyby*. Nie powtarzamy **‑by** przy tym samym orzeczeniu: *gdybym "
            "**miał***, nigdy *gdybym miałbym*."
        ),
        structure=(
            "gdyby + forma osobowa (gdybym, gdybyś...) + forma przeszła\n"
            "jeżeli + czas teraźniejszy lub przyszły"
        ),
        rules=[
            "Jeżeli i jeśli często wprowadzają warunek realny z trybem oznajmującym; "
            "możliwy jest też hipotetyczny: jeśli miałbyś czas, zadzwoń.",
            "Gdyby wprowadza warunek hipotetyczny i wymaga formy osobowej z ‑by.",
            "Nie powtarzamy ‑by przy tym samym orzeczeniu: gdybym miał, nie gdybym miałbym.",
            "Warunek może poprzedzać zdanie główne lub stać po nim: Poszedłbym, gdybym "
            "miał czas.",
        ],
        examples=[
            GrammarExample(
                text="Gdybym miał więcej czasu, uczyłbym się hiszpańskiego.",
                translation=None,
            ),
            GrammarExample(
                text="Jeżeli zdasz egzamin, dostaniesz się na studia.",
                translation=None,
            ),
            GrammarExample(
                text="Gdybyśmy wyszli wcześniej, nie stalibyśmy w korku.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gdybym miał czas, poszedłbym bym na siłownię.",
                correct="Gdybym miał czas, poszedłbym na siłownię.",
                note="Nie dublujemy bym przy poszedłbym. Gdybym w osobnym członie jest poprawne.",
            ),
            GrammarMistake(
                wrong="Gdybym mam czas, pójdę na siłownię.",
                correct="Gdybym miał czas, poszedłbym na siłownię.",
                note="Po gdyby nie używamy czasu teraźniejszego ani przyszłego; potrzebny "
                "jest tryb przypuszczający w obu członach.",
            ),
        ],
        related=["tryb-warunkowy-przeszly", "spojniki", "zdania-czasowe"],
    ),
    GrammarTopic(
        slug="zdania-przyczynowe",
        title="Zdania przyczynowe",
        level="B1",
        category="Składnia",
        summary="Ponieważ, dlatego że, bo, z powodu — jak uzasadniać przyczynę.",
        explanation=(
            "Przyczynę wprowadzają **ponieważ**, **dlatego że**, **gdyż** (formalnie) i "
            "**bo** (potocznie) oraz wyrażenia przyimkowe **z powodu** + dopełniacz i "
            "**przez** + biernik przy przyczynie negatywnej.\n\n"
            "- *Nie przyszedłem, **ponieważ** zachorowałem.*\n"
            "- *Spóźnił się, **bo** autobus utknął w korku.*\n"
            "- *Z powodu remontu zamknięto ulicę.*\n"
            "- *Przez twoją nieuwagę straciliśmy czas.*\n\n"
            "Uwaga na różnicę: **dlatego** wprowadza skutek, a **dlatego że** — przyczynę. "
            "*Nie spał, **dlatego** był zmęczony.* ale *Był zmęczony, **dlatego że** nie "
            "spał.*"
        ),
        structure=(
            "zdanie główne + ponieważ / dlatego że / bo + zdanie podrzędne\n"
            "z powodu + dopełniacz"
        ),
        rules=[
            "Ponieważ, dlatego że i bo łączą zdania, a z powodu wymaga rzeczownika w "
            "dopełniaczu.",
            "Bo jest typowe dla mowy potocznej, ponieważ i gdyż — dla tekstów formalnych.",
            "Przez + biernik wskazuje przyczynę negatywną: przez pośpiech, przez chorobę.",
            "Nie mieszaj dlatego (skutek) z dlatego że (przyczyna).",
        ],
        examples=[
            GrammarExample(
                text="Zostałem w domu, ponieważ bolała mnie głowa.",
                translation=None,
            ),
            GrammarExample(
                text="Pociąg się spóźnił z powodu awarii.",
                translation=None,
            ),
            GrammarExample(
                text="Nie zdał egzaminu, dlatego że zbyt mało się uczył.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Z powodu choroba nie przyszedłem.",
                correct="Z powodu choroby nie przyszedłem.",
                note="Po z powodu stoi dopełniacz: choroby, nie choroba.",
            ),
            GrammarMistake(
                wrong="Z powodu że był chory, nie przyszedł.",
                correct="Ponieważ był chory, nie przyszedł.",
                note="Przed pełnym zdaniem przyczynowym używamy ponieważ; z powodu wymaga "
                "grupy rzeczownikowej: z powodu choroby.",
            ),
        ],
        related=["spojniki", "zdania-czasowe", "zdania-celowe"],
    ),
    GrammarTopic(
        slug="spojniki",
        title="Spójniki przeciwstawne i wynikowe",
        level="B1",
        category="Spójniki",
        summary="Jednak, natomiast, zatem, więc, mimo że — jak łączyć argumenty.",
        explanation=(
            "Spójniki porządkują relacje między zdaniami:\n\n"
            "- **przeciwstawne:** ale, jednak, natomiast, zaś, lecz\n"
            "- **wynikowe:** więc, zatem, dlatego, toteż\n"
            "- **ustępujące:** chociaż, choć, mimo że, wprawdzie\n\n"
            "*Był zmęczony, **jednak** dokończył pracę.*\n"
            "*Nie mam czasu, **natomiast** mogę pomóc w weekend.*\n"
            "*Pada deszcz, **więc** zostajemy w domu.*\n"
            "*Chociaż padał deszcz, wyszliśmy na spacer.*\n\n"
            "Po **mimo że** stoi czasownik w formie osobowej (*mimo że pada*), a po **mimo** "
            "— rzeczownik w dopełniaczu (*mimo deszczu*)."
        ),
        structure="zdanie + spójnik + zdanie",
        rules=[
            "Ale stoi przed drugim zdaniem; jednak i natomiast mogą też stać wewnątrz " "zdania.",
            "Mimo że łączy zdania, a mimo wymaga dopełniacza.",
            "Więc i zatem wprowadzają wniosek lub skutek.",
            "Chociaż i choć nie wymagają trybu przypuszczającego: chociaż pada, " "wychodzimy.",
        ],
        examples=[
            GrammarExample(
                text="Oglądałem ten film, jednak niezbyt mi się podobał.",
                translation=None,
            ),
            GrammarExample(
                text="Ona woli kawę, natomiast ja pijam tylko herbatę.",
                translation=None,
            ),
            GrammarExample(
                text="Mimo że było późno, zadzwoniłem do rodziców.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mimo że deszczu wyszliśmy na spacer.",
                correct="Mimo deszczu wyszliśmy na spacer.",
                note="Mimo wymaga dopełniacza; konstrukcja ze zdaniem wymaga mimo że.",
            ),
            GrammarMistake(
                wrong="Chociaż padał deszcz, więc wyszliśmy.",
                correct="Chociaż padał deszcz, wyszliśmy na spacer.",
                note="Nie łączymy spójnika ustępującego ze skutkowym w jednym zdaniu.",
            ),
        ],
        related=["zdania-przyczynowe", "zdania-wzgledne", "partykuly"],
    ),
    GrammarTopic(
        slug="imieslow-przyslowkowy",
        title="Imiesłów przysłówkowy współczesny i uprzedni",
        level="B1",
        category="Imiesłowy",
        summary="Czytając książkę, przeczytawszy recenzję — skracanie zdań podrzędnych.",
        explanation=(
            "**Imiesłów przysłówkowy współczesny** (‑ąc) opisuje czynność równoczesną z "
            "czynnością zdania głównego i tworzymy go od czasowników niedokonanych: "
            "*Czytając książkę, słuchał muzyki.*\n\n"
            "**Imiesłów przysłówkowy uprzedni** (‑wszy, ‑łszy) opisuje czynność wcześniejszą "
            "i tworzymy go od czasowników dokonanych: *Przeczytawszy recenzję, postanowił "
            "nie iść do kina.*\n\n"
            "Imiesłów się nie odmienia i zawsze odnosi się do podmiotu zdania głównego: "
            "*Wracając do domu, **zadzwoniłem** do matki* (ja wracałem i ja dzwoniłem).\n\n"
            "Formy uprzednie od czasowników niedokonanych, np. *jadłszy*, są dziś rzadkie "
            "i książkowe."
        ),
        structure=(
            "niedokonany + ‑ąc (czytając, idąc)\n"
            "dokonany + ‑wszy/‑łszy (przeczytawszy, wyszedłszy)"
        ),
        rules=[
            "Imiesłów współczesny tworzymy od czasowników niedokonanych, uprzedni od "
            "dokonanych.",
            "Imiesłów nie odmienia się i nie ma własnego podmiotu.",
            "Podmiot imiesłowu musi być podmiotem zdania głównego.",
            "Formy typu przeczytawszy są typowe dla stylu pisanego.",
        ],
        examples=[
            GrammarExample(
                text="Idąc do pracy, słucham podcastów.",
                translation=None,
            ),
            GrammarExample(
                text="Przeczytawszy umowę, podpisała ją bez wahania.",
                translation=None,
            ),
            GrammarExample(
                text="Nie znając odpowiedzi, milczał.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wracając do domu, zaczęło padać.",
                correct="Kiedy wracałem do domu, zaczęło padać.",
                note="Imiesłów musi odnosić się do wykonawcy czynności; zjawisko pogodowe "
                "nie może być podmiotem wracającym do domu.",
            ),
            GrammarMistake(
                wrong="Przeczytając recenzję, postanowił nie iść do kina.",
                correct="Przeczytawszy recenzję, postanowił nie iść do kina.",
                note="Czynność wcześniejsza wymaga imiesłowu uprzedniego od czasownika "
                "dokonanego.",
            ),
        ],
        related=["imieslow-przymiotnikowy", "zdania-czasowe", "zdania-okolicznikowe"],
    ),
    GrammarTopic(
        slug="konstrukcje-bezosobowe",
        title="Konstrukcje bezosobowe",
        level="B1",
        category="Składnia",
        summary="Mówi się, napisano, zbudowano — zdania bez wskazania wykonawcy.",
        explanation=(
            "Konstrukcje bezosobowe pozwalają opisać czynność bez podawania wykonawcy. "
            "Najczęstsze typy:\n\n"
            "- **się + czasownik w 3. os. l. poj.**: *Mówi się, że ceny wzrosną.* *Tu "
            "sprzedaje się bilety.*\n"
            "- **forma na ‑no/‑to**: *Napisano raport.* *Zbudowano nowy most.* *Zamknięto "
            "sklep.*\n"
            "- **3. os. l. mn. bez zaimka**: *Mówią, że będzie strajk.*\n\n"
            "Formy na ‑no/‑to są typowe dla komunikatów, prasy i tekstów urzędowych i nie "
            "odmieniają się przez osoby ani liczby."
        ),
        structure=(
            "się + 3. os. l. poj. (mówi się, sprzedaje się)\n"
            "temat + ‑no/‑to (napisano, zrobiono, otwarto)"
        ),
        rules=[
            "Formy na ‑no i ‑to tworzymy od czasowników dokonanych i niedokonanych: "
            "robiono, zrobiono.",
            "Konstrukcja z się nie ma wykonawcy, ale może mieć dopełnienie: Tu sprzedaje "
            "się bilety.",
            "Formy bezosobowe nie odmieniają się przez osoby ani liczby.",
            "W komunikacji oficjalnej wolimy napisano od ktoś napisał.",
        ],
        examples=[
            GrammarExample(
                text="Wczoraj ogłoszono wyniki konkursu.",
                translation=None,
            ),
            GrammarExample(
                text="W tym sklepie sprzedaje się bilety na koncerty.",
                translation=None,
            ),
            GrammarExample(
                text="Mówi się, że firma zmieni siedzibę.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wczoraj zostało ogłoszono wyniki konkursu.",
                correct="Wczoraj ogłoszono wyniki konkursu.",
                note="Formy bezosobowej na ‑no nie łączymy z czasownikiem zostać.",
            ),
            GrammarMistake(
                wrong="Tu się nie pali papierosy.",
                correct="Tu nie pali się papierosów.",
                note="Po zaprzeczonym czasowniku dopełnienie przechodzi do dopełniacza.",
            ),
        ],
        related=["strona-bierna", "rzeczowniki-odczasownikowe", "strona-bierna-czas"],
    ),
    GrammarTopic(
        slug="rzeczowniki-odczasownikowe",
        title="Rzeczowniki odczasownikowe z ‑nie i ‑cie",
        level="B1",
        category="Słowotwórstwo",
        summary="Czytanie, spotkanie, zamknięcie — nazywanie czynności rzeczownikiem.",
        explanation=(
            "Od czasowników tworzymy rzeczowniki zakończone na **‑nie** lub **‑cie**, które "
            "nazywają czynność albo jej wynik.\n\n"
            "- *czytać → **czytanie***, *mówić → **mówienie***\n"
            "- *spotkać → **spotkanie***, *jeść → **jedzenie***\n"
            "- *zamknąć → **zamknięcie***, *wyjść → **wyjście***\n"
            "- *pić → **picie***, *żyć → **życie***\n\n"
            "Są to rzeczowniki nijakie i odmieniają się regularnie: *czytanie, czytania, "
            "czytaniu*. W stylu urzędowym zastępują zdania podrzędne: *po zamknięciu sklepu* "
            "zamiast *po tym, jak zamknięto sklep*.\n\n"
            "Nie myl ich z imiesłowem biernym: *zamknięcie* to rzeczownik, a *zamknięty* — "
            "imiesłów opisujący stan."
        ),
        structure="bezokolicznik → temat + ‑nie lub ‑cie (czytanie, zamknięcie)",
        rules=[
            "Rzeczowniki odczasownikowe są rodzaju nijakiego i odmieniają się jak inne "
            "rzeczowniki na ‑e.",
            "‑nie występuje najczęściej po temacie zakończonym samogłoską lub ‑j "
            "(czytanie), a ‑cie w formach typu zamknięcie, wyjście, picie.",
            "Formy z ‑nie i ‑cie nazywają czynność, a nie wykonawcę.",
            "W tekstach urzędowych zastępują zdania podrzędne: po zamknięciu sklepu.",
        ],
        examples=[
            GrammarExample(
                text="Czytanie książek pomaga w nauce języka.",
                translation=None,
            ),
            GrammarExample(
                text="Zamknięcie mostu spowodowało ogromne korki.",
                translation=None,
            ),
            GrammarExample(
                text="Dziękuję za zaproszenie na spotkanie.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Dziękuję za zaproszeniu na spotkanie.",
                correct="Dziękuję za zaproszenie na spotkanie.",
                note="Po przyimku za w tym znaczeniu stoi biernik: za zaproszenie.",
            ),
            GrammarMistake(
                wrong="Zamknięty most potrwa do piątku.",
                correct="Zamknięcie mostu potrwa do piątku.",
                note="Czynność nazywa rzeczownik zamknięcie; zamknięty to imiesłów "
                "opisujący stan.",
            ),
        ],
        related=["imieslow-przymiotnikowy", "konstrukcje-bezosobowe", "przyimki-biernik"],
    ),
    GrammarTopic(
        slug="zdania-celowe",
        title="Zdania celowe z żeby i aby",
        level="B1",
        category="Składnia",
        summary="Po co? Żeby odpocząć, żebyś przyszedł, aby zdążyć.",
        explanation=(
            "Cel wyrażamy najczęściej przez **żeby** (neutralnie) lub **aby** (formalnie), a "
            "po nich stoi bezokolicznik albo forma osobowa.\n\n"
            "- **Ten sam podmiot → najczęściej bezokolicznik:** *Wychodzę, **żeby** odpocząć.*\n"
            "- **Różne podmioty → forma osobowa z ‑by:** *Chcę, **żebyś** przyszedł.*\n"
            "- **Styl formalny:** *Aby uzyskać zgodę, należy złożyć wniosek.*\n\n"
            "Formy osobowe: *żebym, żebyś, żeby, żebyśmy, żebyście, żeby*. Po spójnikach "
            "można też użyć krótkiego **by**: *Muszę wyjść, **by** zdążyć na pociąg.*"
        ),
        structure=(
            "zdanie główne + żeby/aby + bezokolicznik (ten sam podmiot)\n"
            "zdanie główne + żeby/aby + forma osobowa (różne podmioty)"
        ),
        rules=[
            "Przy tym samym podmiocie zwykle używamy bezokolicznika; forma osobowa "
            "również jest możliwa.",
            "Różne podmioty wymagają formy osobowej: żebyś, żebyśmy.",
            "Aby i by są bardziej formalne niż żeby.",
            "Po żeby nie stawiamy czasownika w czasie teraźniejszym: nie „żeby " "przychodzisz”.",
        ],
        examples=[
            GrammarExample(
                text="Wstaję wcześnie, żeby zdążyć na autobus.",
                translation=None,
            ),
            GrammarExample(
                text="Powiedziałem jej, żeby zadzwoniła wieczorem.",
                translation=None,
            ),
            GrammarExample(
                text="Aby zapisać się na kurs, trzeba wypełnić formularz.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Chcę, żeby przyjdziesz.",
                correct="Chcę, żebyś przyszedł.",
                note="Po żeby używamy formy na -ł; przyjdziesz to forma czasu przyszłego.",
            ),
            GrammarMistake(
                wrong="Wychodzę, żebym odpocząć.",
                correct="Wychodzę, żeby odpocząć.",
                note="Bezokolicznika nie łączymy z końcówką osobową spójnika: żeby odpocząć, "
                "nie żebym odpocząć.",
            ),
        ],
        related=["mowa-zalezna", "zdania-czasowe", "zdania-okolicznikowe"],
    ),
    GrammarTopic(
        slug="zdania-czasowe",
        title="Zdania czasowe: kiedy, gdy, zanim, po tym jak",
        level="B1",
        category="Składnia",
        summary="Kiedy, gdy, zanim, dopóki, po tym jak — relacje czasowe i aspekt.",
        explanation=(
            "Zdania czasowe określają, kiedy coś się dzieje:\n\n"
            "- **kiedy / gdy**: *Kiedy wróciłem, wszyscy już spali.*\n"
            "- **zanim**: *Zanim wyjdziesz, zamknij okno.*\n"
            "- **po tym jak**: *Po tym jak skończył pracę, poszedł biegać.*\n"
            "- **dopóki**: *Czekaj, dopóki nie wrócę.*\n"
            "- **gdy tylko**: *Gdy tylko zadzwonił, odebrałem.*\n\n"
            "W zdaniu czasowym o przyszłości aspekt zależy od znaczenia: "
            "*Kiedy **wrócę**, zadzwonię* wskazuje zakończenie powrotu, a "
            "*Kiedy **będę wracać**, zadzwonię* — czynność w toku. "
            "Nawyk opisuje np. *Kiedy wracam z pracy, zawsze piję kawę*."
        ),
        structure="zdanie główne + kiedy/gdy/zanim/po tym jak + zdanie podrzędne",
        rules=[
            "Zanim łączy się zwykle z czasownikiem dokonanym: zanim wyjdziesz, zanim " "skończysz.",
            "Dopóki nie z czasownikiem dokonanym wyznacza moment końcowy: "
            "czekaj, dopóki nie wrócę. Dopóki bez nie oznacza trwanie: "
            "dopóki pada, zostajemy w domu.",
            "Kiedy i gdy są wymienne; gdy jest bardziej książkowe.",
            "Po tym jak podkreśla następstwo dwóch czynności.",
        ],
        examples=[
            GrammarExample(
                text="Zanim zadzwonisz, sprawdź, czy nie jest za późno.",
                translation=None,
            ),
            GrammarExample(
                text="Kiedy skończę pracę, zadzwonię do ciebie.",
                translation=None,
            ),
            GrammarExample(
                text="Poczekam, dopóki nie wrócisz.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Poczekam, dopóki wrócisz.",
                correct="Poczekam, dopóki nie wrócisz.",
                note="Gdy dokonane wrócisz wyznacza koniec czekania, używamy dopóki nie. "
                "Bez nie dopóki może łączyć się z czynnością trwającą: dopóki tu jesteś.",
            ),
            GrammarMistake(
                wrong="Zanim wyszedłem z domu, zadzwonię do ciebie.",
                correct="Zanim wyjdę z domu, zadzwonię do ciebie.",
                note="Czasy w obu zdaniach muszą być zgodne; przyszłość wymaga formy "
                "przyszłej także po zanim.",
            ),
        ],
        related=["aspekt-pary", "zdania-celowe", "imieslow-przyslowkowy"],
    ),
    GrammarTopic(
        slug="przyimki-biernik",
        title="Przyimki z biernikiem",
        level="B1",
        category="Przyimki",
        summary="Przez, na, za, pod, nad — utarte wyrażenia z biernikiem.",
        explanation=(
            "Wiele przyimków łączy się z różnymi przypadkami w zależności od znaczenia. W "
            "utartych wyrażeniach z **biernikiem** występują:\n\n"
            "- **przez**: *przez cały dzień*, *przez ulicę*, *przez telefon*, *przez "
            "przypadek*\n"
            "- **na**: *na przyszłość*, *na koncert*, *na obiad* (kierunek lub cel)\n"
            "- **za**: *za tydzień*, *za chwilę*, *dziękuję za pomoc*\n"
            "- **pod, nad**: w konstrukcjach ruchu: *wjechać pod górę*, *wyjść nad jezioro*\n\n"
            "Uwaga na różnicę: *na koncert* (biernik, dokąd?) i *na koncercie* "
            "(miejscownik, gdzie?)."
        ),
        structure="przyimek (przez, na, za, pod, nad) + rzeczownik w bierniku",
        rules=[
            "Przez + biernik oznacza środek, czas trwania lub pokonanie przeszkody.",
            "Na + biernik wskazuje cel lub kierunek, a na + miejscownik — miejsce.",
            "Za + biernik określa czas przyszły liczony od teraz: za tydzień, za miesiąc.",
            "Po przyimkach ruchu (pod, nad, przed) biernik oznacza kierunek, a narzędnik — "
            "miejsce.",
        ],
        examples=[
            GrammarExample(
                text="Rozmawialiśmy przez telefon przez godzinę.",
                translation=None,
            ),
            GrammarExample(
                text="Za tydzień wyjeżdżam na konferencję.",
                translation=None,
            ),
            GrammarExample(
                text="Weszliśmy pod górę i odpoczęliśmy na szczycie.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Dziękuję za pomocą.",
                correct="Dziękuję za pomoc.",
                note="W podziękowaniu po za stoi biernik: za pomoc.",
            ),
            GrammarMistake(
                wrong="Spotkamy się za tygodniem.",
                correct="Spotkamy się za tydzień.",
                note="Odległość czasu w przyszłości wyrażamy biernikiem: za tydzień.",
            ),
        ],
        related=["zdania-czasowe", "rzeczowniki-odczasownikowe", "partykuly"],
    ),
    GrammarTopic(
        slug="strona-bierna-czas",
        title="Strona bierna w różnych czasach",
        level="B1",
        category="Czasownik",
        summary="Jest używany, był używany, będzie używany — odmiana konstrukcji biernej.",
        explanation=(
            "Imiesłów bierny nie zmienia się wraz z czasem, a przez czasy odmienia się "
            "czasownik pomocniczy **być**:\n\n"
            "- czas teraźniejszy: *Artykuł **jest** czytany.*\n"
            "- czas przeszły: *Artykuł **był** czytany.*\n"
            "- czas przyszły: *Artykuł **będzie** czytany.*\n"
            "- tryb przypuszczający: *Artykuł **byłby** czytany.*\n\n"
            "Z **zostać** tworzymy stronę bierną dokonaną w czasie przeszłym i przyszłym: "
            "*Artykuł **został** napisany*, *Artykuł **zostanie** napisany*.\n\n"
            "W czasie przeszłym czasownik pomocniczy i imiesłów przyjmują formę zgodną z "
            "podmiotem: *Książka była czytana*, *Książki były czytane*."
        ),
        structure="być w danym czasie + imiesłów bierny (forma zgodna z podmiotem)",
        rules=[
            "Odmienia się czasownik być lub zostać, a imiesłów dopasowuje się do podmiotu.",
            "Zostać nie tworzy strony biernej w czasie teraźniejszym.",
            "Imiesłów od czasownika niedokonanego (czytany) opisuje czynność trwającą, od "
            "dokonanego (przeczytany) — wynik.",
            "W czasie przyszłym używamy będzie + imiesłów: będzie sprawdzany.",
        ],
        examples=[
            GrammarExample(
                text="Ten program jest używany w wielu szkołach.",
                translation=None,
            ),
            GrammarExample(
                text="Raport był przygotowywany przez cały tydzień.",
                translation=None,
            ),
            GrammarExample(
                text="Decyzja zostanie ogłoszona w poniedziałek.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Raport były pisany przez cały tydzień.",
                correct="Raport był pisany przez cały tydzień.",
                note="Czasownik pomocniczy zgadza się z podmiotem raport: był, nie były.",
            ),
            GrammarMistake(
                wrong="Książki były czytany.",
                correct="Książki były czytane.",
                note="Imiesłów bierny zgadza się z podmiotem w liczbie i rodzaju: książki → "
                "czytane.",
            ),
        ],
        related=["strona-bierna", "imieslow-przymiotnikowy", "konstrukcje-bezosobowe"],
    ),
    GrammarTopic(
        slug="prefiksy-znaczenia",
        title="Przedrostki czasowników i ich znaczenia",
        level="B1",
        category="Słowotwórstwo",
        summary="Pisać, podpisać, wpisać, przepisać — jak przedrostek zmienia znaczenie.",
        explanation=(
            "Przedrostki tworzą nowe czasowniki dokonane i zmieniają znaczenie podstawy:\n\n"
            "- **pod‑**: podpisać (złożyć podpis), podnieść, podejść\n"
            "- **w‑**: wpisać (umieścić w czymś), wejść, wlać\n"
            "- **prze‑**: przepisać (skopiować), przejść, przeczytać\n"
            "- **za‑**: zapisać (utrwalić), zamknąć, zadzwonić\n"
            "- **od‑**: odpisać (udzielić odpowiedzi), oddać, odejść\n"
            "- **wy‑**: wypisać (usunąć z listy lub sporządzić), wyjść, wybrać\n\n"
            "Ten sam przedrostek może mieć różne znaczenia: *przepisać tekst* (skopiować) i "
            "*przepisać komuś leki* (wypisać receptę). Dlatego czasownika uczymy się razem z "
            "jego typowymi dopełnieniami."
        ),
        structure=(
            "przedrostek + czasownik niedokonany → czasownik dokonany\n"
            "(pisać → podpisać, wpisać, przepisać)"
        ),
        rules=[
            "Przedrostek zwykle zmienia czasownik niedokonany w dokonany.",
            "Znaczenie zależy od przedrostka i od dopełnienia: wpisać coś do zeszytu, "
            "podpisać dokument.",
            "Nie każdy przedrostek pasuje do każdego czasownika; formy są konwencjonalne.",
            "Wiele przedrostków ma znaczenie przestrzenne (w‑, wy‑, pod‑, nad‑) i przenośne.",
        ],
        examples=[
            GrammarExample(
                text="Proszę wpisać dane do formularza.",
                translation=None,
            ),
            GrammarExample(
                text="Sekretarka przepisała umowę na komputerze.",
                translation=None,
            ),
            GrammarExample(
                text="Odpisał na wiadomość dopiero po dwóch dniach.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Proszę wpisać dane do formularz.",
                correct="Proszę wpisać dane do formularza.",
                note="Kierunek „do środka” wymaga przyimka do z dopełniaczem.",
            ),
            GrammarMistake(
                wrong="Odpisałem na list od kolega.",
                correct="Odpisałem na list od kolegi.",
                note="Po od używamy dopełniacza: od kolegi.",
            ),
        ],
        related=["aspekt-pary", "strona-bierna", "rzeczowniki-odczasownikowe"],
    ),
    GrammarTopic(
        slug="stopniowanie-przyslowkow",
        title="Stopniowanie przysłówków",
        level="B1",
        category="Przysłówek",
        summary="Dobrze — lepiej — najlepiej: regularne i nieregularne stopnie przysłówków.",
        explanation=(
            "Przysłówki stopniują się podobnie jak przymiotniki.\n\n"
            "**Regularnie** (‑o → ‑iej lub ‑ej):\n"
            "- *szybko → szybciej → najszybciej*\n"
            "- *wolno → wolniej → najwolniej*\n"
            "- *głośno → głośniej → najgłośniej*\n\n"
            "**Nieregularnie:**\n"
            "- *dobrze → lepiej → najlepiej*\n"
            "- *źle → gorzej → najgorzej*\n"
            "- *dużo → więcej → najwięcej*\n"
            "- *mało → mniej → najmniej*\n"
            "- *daleko → dalej → najdalej*\n\n"
            "Stopień wyższy porównujemy za pomocą **niż** albo **od** z dopełniaczem: "
            "*Mówi szybciej **niż** ja.* *Mówi szybciej **ode mnie**.*"
        ),
        structure="szybciej niż ja · szybciej ode mnie\nnaj‑ + stopień wyższy",
        rules=[
            "Stopień wyższy tworzymy końcówką ‑iej lub ‑ej, najwyższy przez dodanie naj‑.",
            "Po od stoi dopełniacz; po niż przypadek wynika z funkcji członu porównania.",
            "Wiele przysłówków ma formy nieregularne, których trzeba się nauczyć.",
            "Stopień najwyższy z naj‑ służy do porównania w całej grupie.",
        ],
        examples=[
            GrammarExample(
                text="Ona mówi po polsku znacznie lepiej niż rok temu.",
                translation=None,
            ),
            GrammarExample(
                text="Pociąg jedzie szybciej od autobusu.",
                translation=None,
            ),
            GrammarExample(
                text="W weekendy wstaję najpóźniej.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mówi szybciej niż mnie.",
                correct="Mówi szybciej niż ja.",
                note="Tu porównujemy podmioty: niż ja. Alternatywnie używamy ode mnie.",
            ),
            GrammarMistake(
                wrong="Dziś czuję się bardziej dobrze.",
                correct="Dziś czuję się lepiej.",
                note="Przysłówek dobrze ma nieregularny stopień wyższy lepiej; formy "
                "bardziej dobrze nie tworzymy.",
            ),
        ],
        related=["partykuly", "zdania-okolicznikowe", "spojniki"],
    ),
    GrammarTopic(
        slug="tryb-warunkowy-przeszly",
        title="Warunek nierealny wobec przeszłości",
        level="B1",
        category="Tryb warunkowy",
        summary="Gdybym był wyszedł wcześniej, nie spóźniłbym się — nierzeczywista przeszłość.",
        explanation=(
            "Warunek nierealny wobec przeszłości wyrażamy konstrukcją **gdyby + forma "
            "przeszła** w obu członach zdania:\n\n"
            "- *Gdybym **był wyszedł** wcześniej, nie **spóźniłbym się**.*\n"
            "- *Gdybyś **przeczytała** umowę, **wiedziałabyś**, co podpisujesz.*\n"
            "- *Gdybyśmy **byli zarezerwowali** bilety, **mielibyśmy** miejsca.*\n\n"
            "Formy złożone typu *był wyszedł* są dziś rzadsze niż proste formy przeszłe "
            "(*wyszedł*), ale poprawne i typowe w stylu książkowym. W obu członach zdania "
            "musi wystąpić forma z ‑by.\n\n"
            "Warunek przeszły i teraźniejszy można łączyć: *Gdybym się wtedy uczył, dziś "
            "mówiłbym po polsku.*"
        ),
        structure="gdyby + forma przeszła (człon warunkowy) + forma z ‑by (człon główny)",
        rules=[
            "Oba człony zdania wymagają formy z ‑by: gdybym..., zrobiłbym...",
            "Książkowa konstrukcja był wyszedł łączy formę przeszłą być z formą na -ł "
            "czasownika wyjść; wyszedł nie jest imiesłowem przysłówkowym uprzednim "
            "wyszedłszy.",
            "W mowie częstsza jest forma prosta: gdybym wyszedł wcześniej.",
            "W członie warunkowym odnoszącym się do przeszłości nie używamy czasu "
            "teraźniejszego.",
        ],
        examples=[
            GrammarExample(
                text="Gdybym był wcześniej wyszedł, nie spóźniłbym się na pociąg.",
                translation=None,
            ),
            GrammarExample(
                text="Gdybyśmy zarezerwowali bilety, nie musielibyśmy stać w kolejce.",
                translation=None,
            ),
            GrammarExample(
                text="Gdybyś powiedział wcześniej, pomógłbym ci.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gdybym był wyszedł wcześniej, nie spóźniłem się.",
                correct="Gdybym był wyszedł wcześniej, nie spóźniłbym się.",
                note="W zdaniu głównym konieczna jest forma z ‑by: spóźniłbym się.",
            ),
            GrammarMistake(
                wrong="Gdybym był wcześniej wyszedł, mogłem nie spóźnić się.",
                correct="Gdybym był wcześniej wyszedł, mógłbym nie spóźnić się.",
                note="Po warunku nierealnym w zdaniu głównym wymagana jest forma z ‑by: "
                "mógłbym.",
            ),
        ],
        related=["tryb-warunkowy-zdania", "imieslow-przyslowkowy", "zdania-czasowe"],
    ),
    GrammarTopic(
        slug="zdania-okolicznikowe",
        title="Zdania okolicznikowe sposobu i celu",
        level="B1",
        category="Składnia",
        summary="Siedząc przy oknie, czytał; wyjechał, aby zwiedzić miasto — sposób i cel.",
        explanation=(
            "Zdania okolicznikowe sposobu odpowiadają na pytanie **jak?** i często skracamy "
            "je imiesłowem: *Siedząc przy oknie, obserwował ulicę.* *Mówił, gestykulując "
            "nerwowo.*\n\n"
            "Zdania okolicznikowe celu odpowiadają na pytanie **po co?** i wprowadzają je "
            "**żeby, aby, by**: *Wyjechał, **aby** zwiedzić miasto.*\n\n"
            "Zdania okolicznikowe stopnia i miary łączą się z **tak..., że...**: *Pracował "
            "tak ciężko, **że** zapomniał o obiedzie.*\n\n"
            "Skracając zdanie sposobowe imiesłowem, pamiętaj o wspólnym podmiocie: imiesłów "
            "odnosi się do tego samego wykonawcy co zdanie główne."
        ),
        structure="zdanie główne + imiesłów ‑ąc (sposób)\nzdanie główne + żeby/aby (cel)",
        rules=[
            "Okolicznik sposobu odpowiada na pytanie jak?, a celu — po co?.",
            "Imiesłów ‑ąc skraca zdanie sposobowe tylko przy wspólnym podmiocie.",
            "Cel wprowadzają żeby, aby i by, a nie ponieważ.",
            "Konstrukcja tak..., że... wyraża stopień lub skutek.",
        ],
        examples=[
            GrammarExample(
                text="Siedząc przy oknie, czytał gazetę.",
                translation=None,
            ),
            GrammarExample(
                text="Wyjechali nad morze, aby odpocząć od miasta.",
                translation=None,
            ),
            GrammarExample(
                text="Mówiła tak cicho, że nikt jej nie słyszał.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wyjechał nad morze, ponieważ odpocząć.",
                correct="Wyjechał nad morze, aby odpocząć.",
                note="Cel wyraża aby lub żeby, a nie ponieważ.",
            ),
            GrammarMistake(
                wrong="Siedząc przy oknie, gazeta była czytana.",
                correct="Siedząc przy oknie, czytał gazetę.",
                note="Imiesłów musi odnosić się do wykonawcy czynności, a nie do przedmiotu.",
            ),
        ],
        related=["imieslow-przyslowkowy", "zdania-celowe", "zdania-wzgledne"],
    ),
    GrammarTopic(
        slug="partykuly",
        title="Partykuły wzmacniające i ograniczające",
        level="B1",
        category="Partykuły",
        summary="Nawet, tylko, przecież, właśnie, chyba — niuanse nacisku i oceny mówiącego.",
        explanation=(
            "Partykuły nie pełnią funkcji składniowej, ale zmieniają nacisk i postawę "
            "mówiącego:\n\n"
            "- **wzmacniające:** nawet, przecież, wręcz, właśnie, zupełnie\n"
            "  *Nawet dziecko to rozumie.* *Przecież ci mówiłem!*\n"
            "- **ograniczające:** tylko, jedynie, wyłącznie, dopiero\n"
            "  *Mam tylko pięć minut.* *Dopiero wczoraj wrócił.*\n"
            "- **modalne:** chyba, pewnie, podobno, rzekomo, oczywiście\n"
            "  *Chyba będzie padać.* *Podobno zmienił pracę.*\n\n"
            "Partykuły są ruchome, ale ich pozycja zmienia sens: *Tylko ja to wiem* znaczy "
            "co innego niż *Ja tylko to wiem*."
        ),
        structure="partykuła + wyraz, do którego się odnosi (pozycja zmienia znaczenie)",
        rules=[
            "Partykuła tylko ogranicza ten wyraz, przed którym stoi.",
            "Nawet dodaje znaczenie „również, włącznie z najmniej oczekiwanym przypadkiem”.",
            "Przecież podkreśla, że mówiący uważa coś za oczywiste.",
            "Dopiero wskazuje na późne pojawienie się czegoś, a dopiero co — na niedawność.",
        ],
        examples=[
            GrammarExample(
                text="Nawet nie wiedziałem, że masz brata.",
                translation=None,
            ),
            GrammarExample(
                text="Dopiero wczoraj dowiedziałem się o zmianie planów.",
                translation=None,
            ),
            GrammarExample(
                text="Przecież mówiłem ci, żebyś wziął parasol.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Podobno, że zmienił pracę.",
                correct="Podobno zmienił pracę.",
                note="Podobno wprowadza zdanie bezpośrednio, bez spójnika że.",
            ),
            GrammarMistake(
                wrong="Dopiero wczoraj nie wiedziałem o tym.",
                correct="Jeszcze wczoraj nie wiedziałem o tym.",
                note="Dopiero wskazuje na późne pojawienie się czegoś; zaprzeczoną "
                "niedawność wyraża jeszcze.",
            ),
        ],
        related=["spojniki", "stopniowanie-przyslowkow", "zdania-wzgledne"],
    ),
]
