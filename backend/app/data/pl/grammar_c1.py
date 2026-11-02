"""Polish grammar topics — C1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="styl-formalny",
        title="Styl formalny",
        level="C1",
        category="Stylistyka",
        summary="Polszczyzna oficjalna: nominalizacja, bezosobowość, słownictwo abstrakcyjne "
        "i spójność terminologiczna.",
        explanation=(
            "Styl formalny to odmiana polszczyzny pisanej i mówionej, której celem jest "
            "precyzja, bezosobowość i trwałość tekstu.\n\n"
            "- **Nominalizacja** zastępuje czasowniki rzeczownikami odczasownikowymi: "
            "*przeprowadzić analizę* → *przeprowadzenie analizy*.\n"
            "- **Bezosobowość** usuwa sprawcę z pierwszego planu: *ustalono*, *zdecydowano*, "
            "*należy przyjąć*.\n"
            "- **Słownictwo abstrakcyjne** porządkuje treść: *zakres*, *kryterium*, "
            "*w odniesieniu do*.\n\n"
            "Rejestr formalny nie oznacza rozwlekłości: nadmiar rzeczowników odczasownikowych "
            "i łańcuchów dopełniaczowych utrudnia lekturę."
        ),
        structure="rzeczownik odczasownikowy + dopełniacz · konstrukcja bezosobowa · "
        "słownictwo abstrakcyjne · spójniki formalne",
        rules=[
            "Zastępuj czasowniki rzeczownikami odczasownikowymi: *przeprowadzić analizę* → "
            "*przeprowadzenie analizy*.",
            "Unikaj form osobowych, gdy nadawca nie jest istotny: *ustalono*, *zdecydowano*.",
            "Stosuj pełne, nieeliptyczne konstrukcje i konsekwentny szyk zdania.",
            "Zachowaj spójność terminologiczną; synonimia w stylu formalnym jest źródłem "
            "nieprecyzji.",
        ],
        examples=[
            GrammarExample(
                text="W związku z otrzymanymi zastrzeżeniami Komisja postanowiła odroczyć "
                "rozpatrzenie wniosku do dnia 15 maja.",
                translation=None,
            ),
            GrammarExample(
                text="Przeprowadzona analiza wykazała, że przyjęte rozwiązania nie odpowiadają "
                "obowiązującym standardom.",
                translation=None,
            ),
            GrammarExample(
                text="Należy podkreślić, iż zakres odpowiedzialności został określony "
                "w odrębnym dokumencie.",
                translation=None,
                note="spójnik *iż* podnosi rejestr wypowiedzi",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Komisja zdecydowała, że odracza rozpatrzenie, bo dostali zastrzeżenia.",
                correct="Komisja zdecydowała, że odracza rozpatrzenie, ponieważ otrzymała "
                "zastrzeżenia.",
                note="Komisja wymaga liczby pojedynczej: otrzymała. Nominalizacja przyczyny "
                "nie jest obowiązkowa w stylu formalnym.",
            ),
            GrammarMistake(
                wrong="Ja myślę, że to nie jest dobre rozwiązanie.",
                correct="Zdaniem autora proponowane rozwiązanie budzi zastrzeżenia.",
                note="Wariant bezosobowy przydatny w niektórych gatunkach formalnych. "
                "Pierwsza osoba sama w sobie nie jest błędem.",
            ),
        ],
        related=[
            "nominalizacja-zaawansowana",
            "konstrukcje-imienne",
            "jezyk-grzecznosci",
        ],
    ),
    GrammarTopic(
        slug="nominalizacja-zaawansowana",
        title="Nominalizacja zaawansowana",
        level="C1",
        category="Składnia",
        summary="Przekształcanie zdań w grupy nominalne dla zwięzłości, bezosobowości i hierarchii "
        "informacji.",
        explanation=(
            "Nominalizacja to zabieg składniowy polegający na przekształceniu orzeczenia "
            "w rzeczownik, dzięki czemu treść zdania zostaje upakowana w grupie imiennej.\n\n"
            "- **Odczasownikowe** rzeczowniki na *-nie* i *-cie*: *wdrożyć* → *wdrożenie*, "
            "*przyjąć* → *przyjęcie*.\n"
            "- **Odprzymiotnikowe** rzeczowniki na *-ość*, *-stwo*, *-izm*: *odporny* → "
            "*odporność*.\n"
            "- **Łańcuch dopełniaczowy** porządkuje zależności, ale po dwóch dopełniaczach "
            "traci czytelność.\n\n"
            "Nominalizacja jest naturalna w nagłówkach, tytułach i tekstach urzędowych. "
            "W zdaniu głównym, gdzie ważny jest sprawca, lepszy bywa czasownik."
        ),
        structure="czasownik → rzeczownik odczasownikowy (-nie/-cie) · przymiotnik → "
        "rzeczownik (-ość/-stwo) · grupa nominalna z dopełniaczem",
        rules=[
            "Twórz rzeczowniki odczasownikowe zakończone na *-nie* lub *-cie*: *wdrożyć* → "
            "*wdrożenie*, *przyjąć* → *przyjęcie*.",
            "Nie piętrz więcej niż dwóch dopełniaczy w jednej grupie: *analiza wyników badania "
            "skuteczności* jest na granicy czytelności.",
            "Zachowaj informację o sprawcy, gdy jest istotna: *nadzór dyrektora nad projektem*.",
            "W nagłówkach nominalizacja jest dopuszczalna; w zdaniu głównym często lepszy jest "
            "czasownik.",
        ],
        examples=[
            GrammarExample(
                text="Wdrożenie nowych procedur wymagało przeprowadzenia konsultacji ze "
                "wszystkimi zainteresowanymi stronami.",
                translation=None,
            ),
            GrammarExample(
                text="Skuteczność oddziaływania kampanii zależy od trafności doboru odbiorców.",
                translation=None,
                note="trzy dopełniacze w jednym zdaniu — granica czytelności",
            ),
            GrammarExample(
                text="Po zakończeniu negocjacji podpisano porozumienie o współpracy.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Dokonanie analizy wyników badań zostało przeprowadzone przez zespół.",
                correct="Zespół przeprowadził analizę wyników badań.",
                note="Nadmiar nominalizacji i czasowników analitycznych zaciemnia sprawcę.",
            ),
            GrammarMistake(
                wrong="Wzrost poziomu zadowolenia klientów firmy sprzedającej odzież.",
                correct="Wzrost zadowolenia klientów firmy odzieżowej.",
                note="Łańcuch dopełniaczy i imiesłowów jest nieczytelny; użyj przymiotnika.",
            ),
        ],
        related=[
            "styl-formalny",
            "konstrukcje-imienne",
            "rzeczowniki-odczasownikowe",
        ],
    ),
    GrammarTopic(
        slug="konstrukcje-imienne",
        title="Konstrukcje imienne",
        level="C1",
        category="Składnia",
        summary="Rozbudowane grupy nominalne z imiesłowami, przydawkami i wyrażeniami przyimkowymi "
        "zamiast zdań podrzędnych.",
        explanation=(
            "Konstrukcja imienna zastępuje zdanie podrzędne grupą nominalną, co zagęszcza "
            "informację i nadaje tekstowi charakter analityczny.\n\n"
            "- **Imiesłów czynny** na *-ący*: *student przygotowujący referat* (= student, "
            "który przygotowuje referat).\n"
            "- **Imiesłów bierny** na *-ny*, *-ony*, *-ty*: *dokument przygotowany przez radcę*.\n"
            "- **Przydawka przyimkowa**: *decyzja o wszczęciu postępowania*, *wpływ na wynik*.\n\n"
            "Imiesłów przymiotnikowy zgadza się z określanym rzeczownikiem, który nie musi "
            "być podmiotem: *Widzę studenta przygotowującego referat*. Wymóg wspólnego "
            "podmiotu dotyczy imiesłowów przysłówkowych."
        ),
        structure="rzeczownik + imiesłów przymiotnikowy + grupa przyimkowa",
        rules=[
            "Imiesłów przymiotnikowy czynny tworzymy końcówką *-ący/-ąca/-ące*: *student "
            "przygotowujący referat*.",
            "Imiesłów przymiotnikowy bierny tworzymy końcówką *-ny/-ony/-ty*: *dokument "
            "przygotowany przez radcę*.",
            "Imiesłów przymiotnikowy zgadza się z określanym rzeczownikiem w przypadku, "
            "liczbie i rodzaju.",
            "Przydawka może stać między podmiotem a orzeczeniem, lecz jej nadmierna długość "
            "utrudnia lekturę.",
        ],
        examples=[
            GrammarExample(
                text="Uczestnicy zakwalifikowani do drugiego etapu zostaną poinformowani "
                "o terminie spotkania.",
                translation=None,
            ),
            GrammarExample(
                text="Raport opisujący przyczyny opóźnienia trafił do zarządu w poniedziałek.",
                translation=None,
            ),
            GrammarExample(
                text="Projekt realizowany wspólnie z partnerem zagranicznym obejmuje trzy moduły "
                "szkoleniowe.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Dokument podpisany przez dyrektora leżał na biurku, który dotyczył umowy.",
                correct="Dokument podpisany przez dyrektora, dotyczący umowy, leżał na biurku.",
                note="Zaimek względny musi odnosić się jednoznacznie do rzeczownika.",
            ),
            GrammarMistake(
                wrong="Wnioski kandydatów nie spełniających wymagań zostaną odrzucone.",
                correct="Wnioski kandydatów niespełniających wymagań zostaną odrzucone.",
                note="Nie z imiesłowami przymiotnikowymi piszemy łącznie: niespełniających. "
                "Z przysłówkowymi — rozdzielnie: nie spełniając.",
            ),
        ],
        related=[
            "imieslow-przymiotnikowy",
            "nominalizacja-zaawansowana",
            "zdania-wzgledne",
        ],
    ),
    GrammarTopic(
        slug="srodki-stylistyczne",
        title="Środki stylistyczne",
        level="C1",
        category="Stylistyka",
        summary="Metafora, metonimia, hiperbola, anafora i litota oraz ich funkcja w tekstach "
        "literackich i użytkowych.",
        explanation=(
            "Środki stylistyczne to świadome operacje na języku, które wzmacniają sens "
            "i oddziałują na odbiorcę.\n\n"
            "- **Metafora** przenosi znaczenie na podstawie podobieństwa: *morze światła*.\n"
            "- **Metonimia** opiera się na styczności: *czytać Mickiewicza* (= jego twórczość).\n"
            "- **Hiperbola** przesadza, **litota** łagodzi przez zaprzeczenie przeciwieństwa: "
            "*nie można powiedzieć, żeby...*.\n"
            "- **Anafora** i **paralelizm** budują rytm i podkreślają ciąg argumentów.\n\n"
            "Figura retoryczna ma sens tylko wtedy, gdy służy celowi komunikacyjnemu; użyta "
            "bez powodu staje się ozdobnikiem."
        ),
        structure="figura retoryczna + funkcja w tekście",
        rules=[
            "Metafora przenosi znaczenie na podstawie podobieństwa: *morze światła*.",
            "Metonimia opiera się na styczności: *czytać Mickiewicza* (= jego twórczość).",
            "Hiperbola i litota służą wartościowaniu; anafora i paralelizm budują rytm.",
            "Środek stylistyczny musi służyć celowi komunikacyjnemu, nie ozdobie.",
        ],
        examples=[
            GrammarExample(
                text="Miasto tonęło w ciszy, a jedynym dźwiękiem był szelest kartek.",
                translation=None,
                note="metafora i kontrast",
            ),
            GrammarExample(
                text="Godziny pracy, godziny nauki, godziny bezsennych nocy — wszystko to "
                "złożyło się na ten wynik.",
                translation=None,
                note="anafora i wyliczenie",
            ),
            GrammarExample(
                text="Nie można powiedzieć, żeby ta propozycja była szczególnie nowatorska.",
                translation=None,
                note="litota",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="To była prawdziwa burza oklasków, dosłownie.",
                correct="To była prawdziwa burza oklasków.",
                note="Wzmocnienie *dosłownie* niweczy metaforę.",
            ),
            GrammarMistake(
                wrong="Powtórzenie *i* na początku trzech zdań to hiperbola.",
                correct="Powtórzenie *i* na początku trzech zdań to anafora.",
                note="Hiperbola to przesadnia, nie powtórzenie.",
            ),
        ],
        related=[
            "skladnia-retoryczna",
            "metafora-jezykowa",
            "styl-formalny",
        ],
    ),
    GrammarTopic(
        slug="skladnia-retoryczna",
        title="Składnia retoryczna",
        level="C1",
        category="Stylistyka",
        summary="Paralelizm, wyliczenie, pytanie retoryczne i inwersja jako narzędzia "
        "argumentacji.",
        explanation=(
            "Składnia retoryczna porządkuje argumenty i nadaje wypowiedzi rytm, który ułatwia "
            "ich zapamiętanie.\n\n"
            "- **Paralelizm** powtarza strukturę gramatyczną: *rządy prawa, rządy przejrzystości, "
            "rządy odpowiedzialności*.\n"
            "- **Wyliczenie** gromadzi człony jednorodne składniowo, zwykle rosnące pod względem "
            "ciężaru.\n"
            "- **Pytanie retoryczne** sugeruje odpowiedź i angażuje odbiorcę.\n"
            "- **Inwersja** przenosi remat na początek lub koniec zdania.\n\n"
            "Składnia retoryczna zawodzi, gdy rytm zastępuje treść: wyliczenie musi być "
            "merytorycznie uzasadnione."
        ),
        structure="paralelizm · wyliczenie · pytanie retoryczne · inwersja · elipsa",
        rules=[
            "Paralelizm wymaga identycznej struktury gramatycznej członów: *rządy prawa, rządy "
            "przejrzystości, rządy odpowiedzialności*.",
            "Wyliczenie powinno być jednorodne składniowo i rosnące pod względem ciężaru.",
            "Pytanie retoryczne zadajemy, gdy odpowiedź jest oczywista lub gdy chcemy ją "
            "zasugerować.",
            "Inwersja nie może zaciemniać relacji między podmiotem a orzeczeniem.",
        ],
        examples=[
            GrammarExample(
                text="Czy można dłużej udawać, że problem nie istnieje?",
                translation=None,
                note="pytanie retoryczne",
            ),
            GrammarExample(
                text="Potrzebujemy odwagi, by spojrzeć w oczy faktom, i pokory, by przyznać się "
                "do błędów.",
                translation=None,
                note="paralelizm",
            ),
            GrammarExample(
                text="Nie o budżet tu chodzi, lecz o zaufanie.",
                translation=None,
                note="inwersja i przeciwstawienie",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Nie chodzi o pieniądze, ale o tym, czy mamy zaufanie.",
                correct="Nie chodzi o pieniądze, ale o to, czy mamy zaufanie.",
                note="Chodzić o wymaga biernika: o to, nie o tym. Zachowujemy pytanie "
                "o istnienie zaufania.",
            ),
            GrammarMistake(
                wrong="Potrzebujemy czasu, pieniędzy i żeby ludzie zrozumieli.",
                correct="Potrzebujemy czasu, pieniędzy i zrozumienia.",
                note="Wyliczenie łączy człony równorzędne; zdanie podrzędne psuje rytm.",
            ),
        ],
        related=[
            "retoryka",
            "srodki-stylistyczne",
            "skladnia-emfatyczna",
        ],
    ),
    GrammarTopic(
        slug="metafora-jezykowa",
        title="Metafora językowa",
        level="C1",
        category="Semantyka",
        summary="Metafora konceptualna w codziennym języku i jej wpływ na sposób mówienia "
        "o abstrakcji.",
        explanation=(
            "Metafora językowa to utrwalony wzorzec przenoszenia znaczeń z domeny konkretnej na "
            "abstrakcyjną. Nie jest ozdobą, lecz sposobem myślenia.\n\n"
            "- **Domena źródłowa** dostarcza obrazu, **domena docelowa** — treści: *spór to "
            "wojna* → *bronić stanowiska*, *atakować argument*.\n"
            "- **Metafora utarta** jest skonwencjonalizowana i przezroczysta: *fala imigracji*, "
            "*kryzys uderzył w firmy*.\n"
            "- **Metafora świeża** zaskakuje i wymaga kontekstu, który ją uzasadnia.\n\n"
            "Wybór metafory jest wyborem oceny: *fala* wartościuje inaczej niż *napływ*."
        ),
        structure="domena źródłowa → domena docelowa (metafora konceptualna)",
        rules=[
            "Metafora utarta jest skonwencjonalizowana: *bronić stanowiska*, *atakować argument*.",
            "Świeża metafora zaskakuje i wymaga kontekstu, który ją uzasadnia.",
            "Nie mieszaj metafor z różnych domen w jednym zdaniu.",
            "Metafora kształtuje ocenę: *fala imigracji* wartościuje inaczej niż *napływ "
            "ludności*.",
        ],
        examples=[
            GrammarExample(
                text="Debata zamieniła się w wymianę ciosów, choć obie strony deklarowały chęć "
                "porozumienia.",
                translation=None,
                note="spór to wojna",
            ),
            GrammarExample(
                text="Kryzys uderzył w najmniejsze firmy, zanim rząd zdążył zareagować.",
                translation=None,
                note="kryzys to siła fizyczna",
            ),
            GrammarExample(
                text="Argumenty oponenta osłabły, gdy zabrakło mu danych.",
                translation=None,
                note="argument to obiekt o sile",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Musimy wbić klin w ten mur i wypłynąć na szerokie wody.",
                correct="Musimy przerwać ten impas i wypracować nowe rozwiązanie.",
                note="Dwie metafory z różnych domen tworzą niespójny obraz.",
            ),
            GrammarMistake(
                wrong="Ceny poszybowały w dół.",
                correct="Ceny gwałtownie spadły.",
                note="Metafora lotu w górę kłóci się z kierunkiem spadku.",
            ),
        ],
        related=[
            "srodki-stylistyczne",
            "frazeologia",
            "kolokacje",
        ],
    ),
    GrammarTopic(
        slug="terminologia",
        title="Terminologia",
        level="C1",
        category="Leksyka",
        summary="Systemowość terminów, ich jednoznaczność i relacje znaczeniowe w tekście "
        "specjalistycznym.",
        explanation=(
            "Termin to wyraz lub połączenie wyrazów o znaczeniu ustalonym w obrębie danej "
            "dziedziny. Jego wartość polega na powtarzalności i jednoznaczności.\n\n"
            "- **Systemowość**: terminy tworzą hierarchie, np. *ssak* jako termin nadrzędny "
            "wobec *gryzonia* i *naczelnego*.\n"
            "- **Jednoznaczność w tekście**: jeden termin — jedno znaczenie, bez synonimii "
            "stylistycznej.\n"
            "- **Definicyjność**: znaczenie terminu ustala definicja, nie potoczne skojarzenia.\n\n"
            "Termin różni się od profesjonalizmu: profesjonalizm funkcjonuje w komunikacji "
            "wewnątrzgrupowej i nie musi być zdefiniowany."
        ),
        structure="termin nadrzędny → terminy podrzędne · definicja · ekwiwalent",
        rules=[
            "Termin w obrębie jednego tekstu ma jedno znaczenie; nie stosuj synonimów "
            "terminologicznych.",
            "Definicja terminu podaje rodzaj nadrzędny i cechę różnicującą.",
            "Zapożyczenia utrwalone w danej dziedzinie zachowują przyjętą pisownię i odmianę.",
            "Odróżniaj termin od profesjonalizmu; ten drugi funkcjonuje w komunikacji "
            "wewnątrzgrupowej.",
        ],
        examples=[
            GrammarExample(
                text="W artykule terminu *bezrobocie strukturalne* używa się wyłącznie "
                "w znaczeniu przyjętym w statystyce publicznej.",
                translation=None,
            ),
            GrammarExample(
                text="Nadciśnienie tętnicze definiuje się jako wartości ciśnienia przekraczające "
                "ustalony próg.",
                translation=None,
            ),
            GrammarExample(
                text="Decyzja administracyjna różni się od postanowienia zakresem "
                "rozstrzygnięcia.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="W pracy raz piszę *pacjent*, raz *klient*, a raz *użytkownik*.",
                correct="W całej pracy konsekwentnie używam terminu *pacjent*.",
                note="Synonimia w terminologii wprowadza niejednoznaczność.",
            ),
            GrammarMistake(
                wrong="Definicja: recesja to wtedy, gdy gospodarka się kurczy.",
                correct="Recesja to okres spadku aktywności gospodarczej.",
                note="Definicja wskazuje kategorię okresu i jego cechę. Kryterium dwóch "
                "kwartałów dotyczy recesji technicznej i wymaga osobnego doprecyzowania.",
            ),
        ],
        related=[
            "definiowanie",
            "jezyk-naukowy",
            "przyimki-specjalistyczne",
        ],
    ),
    GrammarTopic(
        slug="definiowanie",
        title="Definiowanie pojęć",
        level="C1",
        category="Leksyka",
        summary="Struktura definicji klasycznej, warunki konieczne i wystarczające oraz typowe "
        "błędy definiowania.",
        explanation=(
            "Definicja porządkuje znaczenie pojęcia i umożliwia jego sprawdzalne stosowanie.\n\n"
            "- **Definicja klasyczna**: *X to Y, który Z*, gdzie Y jest rodzajem nadrzędnym "
            "(genus proximum), a Z cechą różnicującą.\n"
            "- **Definicja operacyjna** wskazuje procedurę rozpoznania lub pomiaru: *bezdomność "
            "to brak stałego miejsca zamieszkania w okresie trzydziestu dni*.\n"
            "- **Definicja kontrastywna** odróżnia pojęcie od sąsiedniego: *kara to nie to samo "
            "co środek wychowawczy*.\n\n"
            "Typowe błędy to definicja za szeroka, za wąska, błędne koło oraz definiowanie przez "
            "wyraz niejaśniejszy od definiowanego."
        ),
        structure="definiendum = definiens (rodzaj nadrzędny + cecha różnicująca)",
        rules=[
            "Definicja klasyczna: *X to Y, który Z*, gdzie Y jest rodzajem nadrzędnym.",
            "Nie definiuj terminu przez niego samego ani przez wyrazy bliskoznaczne.",
            "Definicja musi być ani za szeroka, ani za wąska: sprawdź przypadki graniczne.",
            "Definicja operacyjna wskazuje procedurę pomiaru lub rozpoznania.",
        ],
        examples=[
            GrammarExample(
                text="Klient to osoba lub podmiot, który nabywa towar lub usługę od "
                "przedsiębiorcy.",
                translation=None,
            ),
            GrammarExample(
                text="Przez mobbing rozumiemy powtarzające się działania polegające na "
                "uporczywym nękaniu pracownika.",
                translation=None,
            ),
            GrammarExample(
                text="Bezdomność definiuje się operacyjnie jako brak stałego miejsca zamieszkania "
                "w okresie ostatnich trzydziestu dni.",
                translation=None,
                note="definicja operacyjna",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Tolerancja to postawa tolerancyjna wobec innych.",
                correct="Tolerancja to postawa akceptacji odmiennych poglądów i zachowań, o ile "
                "nie naruszają prawa.",
                note="Definicja przez wyraz pokrewny niczego nie wyjaśnia (błędne koło).",
            ),
            GrammarMistake(
                wrong="Pies to zwierzę, które szczeka.",
                correct="Pies to udomowiony ssak z rodziny psowatych.",
                note="Definicja przez jedną cechę jest za wąska.",
            ),
        ],
        related=[
            "terminologia",
            "jezyk-naukowy",
            "definicje-precyzja",
        ],
    ),
    GrammarTopic(
        slug="przyimki-specjalistyczne",
        title="Przyimki w języku specjalistycznym",
        level="C1",
        category="Składnia",
        summary="Utarte połączenia przyimkowe w nauce, prawie i administracji: w zakresie, "
        "w odniesieniu do, na podstawie.",
        explanation=(
            "W tekstach specjalistycznych przyimek nie jest swobodny: tworzy utrwalone "
            "połączenie z określonym przypadkiem i rzeczownikiem.\n\n"
            "- **w zakresie** + dopełniacz: *w zakresie ochrony danych*.\n"
            "- **w odniesieniu do** + dopełniacz: *w odniesieniu do zgłoszonych uwag*.\n"
            "- **na podstawie** + dopełniacz: *na podstawie badań*.\n"
            "- **pod względem** + dopełniacz: *pod względem jakości*.\n\n"
            "Dobór konstrukcji zależy od sensu i rejestru. *W oparciu o* i *na podstawie* "
            "są używane w polszczyźnie; nie każda różnica stylistyczna jest błędem rekcji."
        ),
        structure="przyimek + dopełniacz / biernik / miejscownik (rekcja ustalona)",
        rules=[
            "Ustalona rekcja: *w zakresie* + dopełniacz, *w odniesieniu do* + dopełniacz, "
            "*na podstawie* + dopełniacz.",
            "Rozróżniaj rekcję: w oparciu o + biernik, na podstawie + dopełniacz.",
            "Przyimek *wobec* wyraża stosunek, a *w stosunku do* bywa nadużywany.",
            "Nie rozdzielaj przyimka od rzeczownika rozbudowaną przydawką.",
        ],
        examples=[
            GrammarExample(
                text="W zakresie ochrony danych osobowych obowiązują przepisy rozporządzenia.",
                translation=None,
            ),
            GrammarExample(
                text="W odniesieniu do zgłoszonych uwag przedstawiamy stanowisko w załączniku.",
                translation=None,
            ),
            GrammarExample(
                text="Na podstawie przeprowadzonych badań sformułowano trzy wnioski.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="W oparciu o danych przedstawiono wnioski.",
                correct="W oparciu o dane przedstawiono wnioski.",
                note="W oparciu o wymaga biernika: dane, nie danych.",
            ),
            GrammarMistake(
                wrong="Na podstawie o przeprowadzonych badaniach sformułowano wnioski.",
                correct="Na podstawie przeprowadzonych badań sformułowano wnioski.",
                note="*Na podstawie* łączy się z dopełniaczem, nie z konstrukcją przyimkową.",
            ),
        ],
        related=[
            "przyimki-zaawansowane",
            "jezyk-naukowy",
            "terminologia",
        ],
    ),
    GrammarTopic(
        slug="aspekt-niuanse",
        title="Niuanse aspektu",
        level="C1",
        category="Morfologia",
        summary="Aspekt dokonany i niedokonany w niuansach: próba, nawyk, skutek, powtarzalność "
        "i grzeczność.",
        explanation=(
            "Aspekt w polszczyźnie nie ogranicza się do opozycji *skończone / nieskończone*. "
            "Wyznacza sposób patrzenia na czynność.\n\n"
            "- **Niedokonany** przedstawia proces, nawyk lub czynność powtarzaną: *czytałem "
            "raport*, *co dzień pisał listy*.\n"
            "- **Dokonany** wskazuje skutek lub jednorazowe zamknięcie: *przeczytałem raport*, "
            "*napisał list*.\n"
            "- W **negacji** powrót do niedokonanego zmienia presupozycję: *nie przeczytałem* "
            "(nie doszedłem do końca) wobec *nie czytałem* (w ogóle nie było czynności).\n\n"
            "W rozkaźniku aspekt nie wyznacza samodzielnie grzeczności: *Siadaj* może być "
            "zaproszeniem, a *Pisz wreszcie!* — ponagleniem. Znaczenie zależy też od "
            "intonacji, kontekstu i wyrazów takich jak *proszę*."
        ),
        structure="niedokonany (proces/nawyk) ↔ dokonany (skutek/jednorazowość)",
        rules=[
            "Czas przyszły złożony z bezokolicznikiem niedokonanym: *będę czytać*; z dokonanym: "
            "*przeczytam*.",
            "W negacji aspekt zmienia presupozycję: *nie przeczytałem* ≠ *nie czytałem*.",
            "Nawyk zwykle wyraża niedokonany: co dzień pisał listy. Dokonany może "
            "opisywać powtarzane rezultaty: co dzień napisze list i wychodzi.",
            "Grzeczność rozkaźnika zależy od kontekstu i intonacji, nie tylko od aspektu.",
        ],
        examples=[
            GrammarExample(
                text="Wczoraj czytałem raport, ale go nie przeczytałem.",
                translation=None,
                note="proces bez skutku",
            ),
            GrammarExample(
                text="Codziennie otwierałem okno o siódmej.",
                translation=None,
                note="nawyk",
            ),
            GrammarExample(
                text="Proszę pisać do mnie raz w tygodniu.",
                translation=None,
                note="powtarzalna prośba w formie łagodnej",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Przestałem przeczytać gazetę.",
                correct="Przestałem czytać gazetę.",
                note="Przestać wymaga bezokolicznika niedokonanego.",
            ),
            GrammarMistake(
                wrong="Będę przeczytać tę książkę.",
                correct="Przeczytam tę książkę.",
                note="Czasownik dokonany nie tworzy czasu przyszłego złożonego z "
                "bezokolicznikiem.",
            ),
        ],
        related=[
            "aspekt-pary",
            "aspekt-mistrzostwo",
            "czas-przyszly-niedokonany",
        ],
    ),
    GrammarTopic(
        slug="partykuly-niuans",
        title="Partykuły i niuanse modalne",
        level="C1",
        category="Pragmatyka",
        summary="Partykuły wzmacniające, osłabiające i wartościujące: przecież, właśnie, bodaj, "
        "niejako, wręcz.",
        explanation=(
            "Partykuła nie należy do zdania pod względem składniowym, ale zmienia jego wartość "
            "modalną i pragmatyczną.\n\n"
            "- **przecież** przywołuje wiedzę wspólną i może brzmieć pouczająco: *Przecież "
            "mówiłem*.\n"
            "- **wręcz** wzmacnia ocenę: *To wręcz skandal*.\n"
            "- **niejako** dystansuje nadawcę i osłabia odpowiedzialność za twierdzenie.\n"
            "- **bodaj**, **chyba**, **ponoć** różnią się źródłem niepewności: przypuszczenie, "
            "wątpliwość, cudza relacja.\n\n"
            "Pozycja partykuły wyznacza zakres twierdzenia: *Tylko on to wiedział* ≠ *On tylko "
            "to wiedział*."
        ),
        structure="partykuła + zdanie · pozycja w zdaniu zmienia zakres twierdzenia",
        rules=[
            "Partykuła *przecież* przywołuje wiedzę wspólną i może brzmieć pouczająco.",
            "*Wręcz* wzmacnia, *niejako* dystansuje i osłabia odpowiedzialność za twierdzenie.",
            "*Bodaj*, *chyba*, *ponoć* różnią się źródłem niepewności: przypuszczenie, "
            "wątpliwość, cudza relacja.",
            "Przesuń partykułę i sprawdź, czy nie zmienia się zakres twierdzenia.",
        ],
        examples=[
            GrammarExample(
                text="Przecież mówiłem, że ten termin jest nierealny.",
                translation=None,
                note="przypomnienie wiedzy wspólnej",
            ),
            GrammarExample(
                text="To wręcz skandal, że nikt nie zareagował.",
                translation=None,
                note="wzmocnienie oceny",
            ),
            GrammarExample(
                text="Ponoć umowa została już podpisana, choć oficjalnie tego nie potwierdzono.",
                translation=None,
                note="cudza relacja",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Podobno, że przyjdzie.",
                correct="Podobno przyjdzie.",
                note="Podobno nie wymaga że. Połączenie Podobno na pewno przyjdzie może "
                "natomiast przekazywać cudze zapewnienie o przyjściu.",
            ),
            GrammarMistake(
                wrong="Niejako to był błąd.",
                correct="To był niejako błąd.",
                note="Wariant stylistyczny z niejako przy ocenianym członie. Szyk początkowy "
                "nie jest automatycznie błędem; jego naturalność zależy od kontekstu.",
            ),
        ],
        related=[
            "partykuly-modalne",
            "partykuly-zaawansowane",
            "konstrukcje-modalne",
        ],
    ),
    GrammarTopic(
        slug="zaimki-nieokreslone",
        title="Zaimki nieokreślone i przeczące",
        level="C1",
        category="Morfologia",
        summary="Ktoś, ktokolwiek, byle kto, nikt z nas: zakres znaczeniowy, odmiana i negacja "
        "wielokrotna.",
        explanation=(
            "Zaimki nieokreślone tworzą serie od zaimków pytajnych i różnią się stopniem "
            "określoności oraz nastawieniem nadawcy.\n\n"
            "- **-ś** wskazuje osobę lub rzecz nieznaną mówiącemu: *ktoś, coś, gdzieś*.\n"
            "- **-kolwiek** wyraża dowolność bez ograniczeń: *ktokolwiek, cokolwiek*.\n"
            "- **byle-** wyraża obojętność wyboru: *byle kto*, *byle jaki*.\n"
            "- **ni-** tworzy wyrazy przeczące: *nikt, nic, nigdzie*.\n\n"
            "Polszczyzna wymaga negacji wielokrotnej: *Nikt nigdy nic nie powiedział*."
        ),
        structure="ktoś / ktokolwiek / byle kto / nikt (serie zaimków nieokreślonych)",
        rules=[
            "Zaimki z *-ś* wskazują osobę lub rzecz nieznaną mówiącemu: *ktoś, coś, gdzieś*.",
            "Zaimki z *-kolwiek* i *byle-* wyrażają dowolność; *byle* sugeruje obojętność.",
            "Polszczyzna wymaga negacji wielokrotnej: *nikt nigdy nic nie powiedział*.",
            "Zaimki nieokreślone odmieniają się jak zaimki pytajne, od których powstały.",
        ],
        examples=[
            GrammarExample(
                text="Ktokolwiek podejmie decyzję, musi liczyć się z konsekwencjami.",
                translation=None,
            ),
            GrammarExample(
                text="Nie powiedział nikomu niczego, co mogłoby go obciążyć.",
                translation=None,
                note="negacja wielokrotna",
            ),
            GrammarExample(
                text="Weź byle jaki długopis, byle pisał.",
                translation=None,
                note="obojętność wyboru",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Nikt powiedział o tym głośno.",
                correct="Nikt nie powiedział o tym głośno.",
                note="Zaimek *nikt* wymaga *nie* przy orzeczeniu.",
            ),
            GrammarMistake(
                wrong="Nikt z nas nigdy słyszał o tej sprawie.",
                correct="Nikt z nas nigdy nie słyszał o tej sprawie.",
                note="Przy zaimkach przeczących orzeczenie wymaga partykuły *nie*.",
            ),
        ],
        related=[
            "zaimki-wzgledne",
            "przeczenie-nie",
            "zaimki-osobowe",
        ],
    ),
    GrammarTopic(
        slug="zdania-warunkowe-mieszane",
        title="Mieszane zdania warunkowe",
        level="C1",
        category="Składnia",
        summary="Kombinacje warunku przeszłego ze skutkiem teraźniejszym i warunku "
        "teraźniejszego ze skutkiem przeszłym.",
        explanation=(
            "Zdanie warunkowe mieszane łączy dwa punkty odniesienia w czasie: warunek dotyczy "
            "jednej epoki, a skutek drugiej.\n\n"
            "- **Warunek przeszły → skutek teraźniejszy**: *Gdybyśmy wtedy zainwestowali, dziś "
            "bylibyśmy niezależni*.\n"
            "- **Warunek teraźniejszy → skutek przeszły**: *Gdyby znał przepisy, nie popełniłby "
            "tamtego błędu*.\n"
            "- **Warunek przeszły → skutek przeszły**: *Gdyby nie awaria, pociąg przyjechałby "
            "punktualnie*.\n\n"
            "Cząstka *by* jest ruchoma: *zrobiłbym* lub *ja bym zrobił*. W *gdybym* "
            "i *gdybyśmy* końcówka osobowa łączy się ze spójnikiem *gdyby*."
        ),
        structure="gdyby + czas przeszły → tryb warunkowy w członie nadrzędnym",
        rules=[
            "Warunek przeszły i skutek teraźniejszy: *Gdybyśmy wtedy zainwestowali, dziś "
            "bylibyśmy niezależni*.",
            "Warunek teraźniejszy i skutek przeszły: *Gdyby znał przepisy, nie popełniłby tego "
            "błędu*.",
            "Gdybym i gdybyśmy zawierają końcówkę osobową; nie dodajemy jej ponownie "
            "do czasownika w tym członie.",
            "Nie mieszaj czasów w jednym członie: *gdybym wiedział*, nie: *gdybym wiem*.",
        ],
        examples=[
            GrammarExample(
                text="Gdybyśmy wtedy nie podpisali tej umowy, dziś nie mielibyśmy problemów z jej "
                "realizacją.",
                translation=None,
                note="warunek przeszły, skutek teraźniejszy",
            ),
            GrammarExample(
                text="Gdyby dyrektor znał realia, nie podjąłby tamtej decyzji.",
                translation=None,
                note="warunek teraźniejszy, skutek przeszły",
            ),
            GrammarExample(
                text="Gdybym teraz zrezygnował, cała praca poszłaby na marne.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gdybym wiem, że przyjdziesz, przygotowałbym kolację.",
                correct="Gdybym wiedział, że przyjdziesz, przygotowałbym kolację.",
                note="Po *gdyby* wymagana jest forma czasu przeszłego.",
            ),
            GrammarMistake(
                wrong="Gdybym miał czas, przeczytam tę książkę.",
                correct="Gdybym miał czas, przeczytałbym tę książkę.",
                note="Warunek nierzeczywisty wymaga trybu warunkowego w obu członach.",
            ),
        ],
        related=[
            "tryb-warunkowy-przeszly",
            "tryb-warunkowy-hipotetyczny",
            "zdania-ustepstwowe",
        ],
    ),
    GrammarTopic(
        slug="mowa-zalezna-styl",
        title="Mowa zależna w tekście",
        level="C1",
        category="Składnia",
        summary="Referowanie cudzych wypowiedzi z zachowaniem sensu: czasowniki wprowadzające, "
        "spójniki i punkt odniesienia.",
        explanation=(
            "Mowa zależna polega na wtórnym przytoczeniu cudzej wypowiedzi w sposób, który "
            "zachowuje jej treść, ale nie formę.\n\n"
            "- Po czasowniku twierdzenia występuje *że*: *Minister oświadczył, że...*.\n"
            "- Po pytaniu występuje *czy*: *Zapytał, czy...*.\n"
            "- Po żądaniu występuje *żeby*: *Zażądali, żeby...*.\n"
            "- Zaimki i okoliczniki czasu zmieniają się według punktu odniesienia: *tu* → *tam*, "
            "*dziś* → *tego dnia*.\n\n"
            "W polszczyźnie nie ma obowiązku przesuwania czasu, jeśli treść pozostaje aktualna."
        ),
        structure="verbum dicendi + że / czy / żeby + zdanie podrzędne",
        rules=[
            "Po czasowniku twierdzenia: *że*; po pytaniu: *czy*; po żądaniu: *żeby*.",
            "W polszczyźnie nie ma obowiązku przesuwania czasu; zachowaj czas oryginału, jeśli "
            "jest nadal aktualny.",
            "Zaimki i wyrażenia czasu zmieniają się zgodnie z punktem odniesienia: *tu* → *tam*, "
            "*dziś* → *tego dnia*.",
            "Nie łącz mowy zależnej z dosłownym cytatem bez wyraźnego oznaczenia.",
        ],
        examples=[
            GrammarExample(
                text="Minister oświadczył, że decyzja zapadnie do końca miesiąca.",
                translation=None,
            ),
            GrammarExample(
                text="Dziennikarz zapytał, czy rząd zamierza zmienić przepisy.",
                translation=None,
                note="pytanie zależne",
            ),
            GrammarExample(
                text="Związkowcy zażądali, żeby negocjacje wznowiono natychmiast.",
                translation=None,
                note="żądanie",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Prezes powiedział, żeby inwestycja jest opłacalna.",
                correct="Prezes powiedział, że inwestycja jest opłacalna.",
                note="*Żeby* wprowadza żądanie, nie twierdzenie.",
            ),
            GrammarMistake(
                wrong="Zapytał, że przyjdziemy.",
                correct="Zapytał, czy przyjdziemy.",
                note="Pytania zależne wprowadza *czy*.",
            ),
        ],
        related=[
            "mowa-zalezna-zaawansowana",
            "mowa-zalezna",
            "zdania-z-ze",
        ],
    ),
    GrammarTopic(
        slug="strona-bierna-styl",
        title="Strona bierna w stylu",
        level="C1",
        category="Składnia",
        summary="Funkcje strony biernej: ukrycie sprawcy, eksponowanie tematu i bezosobowość "
        "tekstu naukowego.",
        explanation=(
            "Strona bierna zmienia układ informacji: sprawca schodzi na dalszy plan, a temat "
            "wysuwa się na pierwsze miejsce.\n\n"
            "- **zostać + imiesłów bierny** podkreśla rezultat: *projekt został przyjęty*.\n"
            "- **być + imiesłów bierny** opisuje stan: *decyzja jest uzasadniona*.\n"
            "- **Formy -no, -to** są bezosobowe i neutralne: *ustalono*, *podpisano*.\n\n"
            "Ukrycie sprawcy bywa zabiegiem perswazyjnym: pozwala uniknąć odpowiedzialności. "
            "Dlatego w tekstach opiniotwórczych warto je rozpoznawać."
        ),
        structure="być/zostać + imiesłów przymiotnikowy bierny · formy -no/-to",
        rules=[
            "Strona bierna z *zostać* podkreśla rezultat: *został przyjęty*; z *być* — stan: "
            "*jest przyjęty*.",
            "Bezosobowe formy *-no, -to* są neutralne i nie wskazują sprawcy: *ustalono, "
            "podpisano*.",
            "Ukrywanie sprawcy jest zabiegiem perswazyjnym; stosuj je świadomie.",
            "Nie piętrz imiesłowów biernych w jednym zdaniu.",
        ],
        examples=[
            GrammarExample(
                text="Projekt został przyjęty większością głosów.",
                translation=None,
            ),
            GrammarExample(
                text="W raporcie stwierdzono, że dane zostały zaniżone.",
                translation=None,
                note="forma bezosobowa i strona bierna w jednym zdaniu",
            ),
            GrammarExample(
                text="Decyzja jest uzasadniona względami bezpieczeństwa.",
                translation=None,
                note="stan, nie czynność",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Raport został napisany przez autora, który jest załączony.",
                correct="Raport napisany przez autora znajduje się w załączniku.",
                note="Imiesłów i zaimek względny muszą mieć jednoznaczne odniesienie.",
            ),
            GrammarMistake(
                wrong="Dokumenty są sprawdzane przez nas codziennie rano.",
                correct="Dokumenty sprawdzamy codziennie rano.",
                note="Gdy sprawca jest znany i istotny, strona czynna jest prostsza.",
            ),
        ],
        related=[
            "strona-bierna-zaawansowana",
            "strona-bierna-czas",
            "konstrukcje-bezosobowe",
        ],
    ),
    GrammarTopic(
        slug="jezyk-grzecznosci",
        title="Język grzeczności",
        level="C1",
        category="Pragmatyka",
        summary="Formy adresatywne, modalność uprzejmości i strategie osłabiania próśb w relacjach "
        "służbowych.",
        explanation=(
            "Grzeczność w polszczyźnie opiera się na dystansie i na stopniowaniu siły aktu "
            "mowy.\n\n"
            "- **Adresatywy**: *pan / pani* z czasownikiem w trzeciej osobie, *państwo* z formą "
            "trzeciej osoby liczby mnogiej.\n"
            "- **Osłabianie prośby**: tryb warunkowy i pytanie: *Czy mógłby pan...?*, *Byłbym "
            "wdzięczny za...*.\n"
            "- **Wzmocnienie podziękowania** przez konkretyzację: *dziękuję za szybką reakcję*.\n\n"
            "Mieszanie *ty* i *pan* w jednej wypowiedzi jest odbierane jako brak taktu."
        ),
        structure="proszę + bezokolicznik · czy mógłby pan/pani + bezokolicznik · byłbym wdzięczny "
        "za + biernik",
        rules=[
            "Do nieznajomych i w relacjach służbowych używaj *pan/pani* z czasownikiem w trzeciej "
            "osobie.",
            "Prośbę osłabiaj trybem warunkowym i pytaniem: *Czy mógłby pan...?*",
            "Podziękowanie i przeprosiny wzmacniaj konkretyzacją: *dziękuję za szybką reakcję*.",
            "Nie mieszaj form *ty* i *pan* w jednej wypowiedzi.",
        ],
        examples=[
            GrammarExample(
                text="Czy mógłby pan przesłać dokument do piątku?",
                translation=None,
            ),
            GrammarExample(
                text="Byłbym wdzięczny za potwierdzenie terminu spotkania.",
                translation=None,
                note="prośba w formie warunkowej",
            ),
            GrammarExample(
                text="Przepraszam za opóźnienie, postaram się nadrobić stracony czas.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Czy ty możesz mi to wysłać, panie prezesie?",
                correct="Czy mógłby pan mi to wysłać, panie prezesie?",
                note="Forma *pan* wymaga trzeciej osoby, nie *ty*.",
            ),
            GrammarMistake(
                wrong="Chcę, żeby pan natychmiast to zrobił.",
                correct="Byłbym wdzięczny, gdyby pan mógł to zrobić natychmiast.",
                note="Wariant łagodzący prośbę z zachowaniem pilności. Oryginał jest "
                "gramatyczny i wyraża stanowcze żądanie, choć nie ma formy rozkaźnika.",
            ),
        ],
        related=[
            "tryb-rozka-zaawansowany",
            "konstrukcje-modalne",
            "styl-formalny",
        ],
    ),
    GrammarTopic(
        slug="tryb-rozka-zaawansowany",
        title="Tryb rozkazujący zaawansowany",
        level="C1",
        category="Morfologia",
        summary="Rozkaźnik w funkcji perswazyjnej, dyplomatycznej i retorycznej; formy "
        "nieregularne i partykuły.",
        explanation=(
            "Tryb rozkazujący nie służy wyłącznie wydawaniu poleceń. W tekstach dorosłych "
            "użytkowników języka występuje jako narzędzie perswazji i uprzejmej zachęty.\n\n"
            "- **Formy podstawowe**: *idź*, *weź*, *daj*, *bądź*; w liczbie mnogiej *idźcie*, "
            "*weźcie*.\n"
            "- **Niech pan/pani** + trzecia osoba łagodzi polecenie: *Niech pan usiądzie*.\n"
            "- **Partykuły -że, no** dodają nacisku lub poufałości: *chodźże*, *siadaj no*.\n"
            "- **Zakaz** zwykle tworzymy z *nie* i aspektu niedokonanego: *nie rób*. "
            "Ostrzeżenie może mieć aspekt dokonany: *Nie zrób sobie krzywdy*.\n\n"
            "W negocjacjach rozkaźnik zastępuje się konstrukcjami modalnymi, aby nie naruszyć "
            "twarzy rozmówcy."
        ),
        structure="temat czasu teraźniejszego + -∅ / -cie / -my · niech + 3. os.",
        rules=[
            "Poprawna druga osoba liczby pojedynczej: *idź*, *weź*, *daj*, *bądź*; liczby "
            "mnogiej: *idźcie*, *weźcie*.",
            "*Niech pan* + trzecia osoba łagodzi polecenie: *Niech pan usiądzie*.",
            "Partykułę -że piszemy łącznie (chodźże), a no oddzielnie (siadaj no).",
            "Zakaz zwykle ma aspekt niedokonany; dokonany jest poprawny w ostrzeżeniach: "
            "Nie zrób sobie krzywdy.",
        ],
        examples=[
            GrammarExample(
                text="Proszę rozważyć naszą propozycję przed podjęciem decyzji.",
                translation=None,
            ),
            GrammarExample(
                text="Niech państwo zechcą zająć miejsca.",
                translation=None,
                note="polecenie złagodzone formą niech",
            ),
            GrammarExample(
                text="Weźcie pod uwagę, że termin został już przesunięty.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Nie zróbij sobie krzywdy.",
                correct="Nie zrób sobie krzywdy.",
                note="Poprawna forma rozkazująca zrobić to zrób; dokonany aspekt "
                "jest tu naturalny w ostrzeżeniu.",
            ),
            GrammarMistake(
                wrong="Proszę państwo usiąść.",
                correct="Proszę państwa o zajęcie miejsc.",
                note="W proszę państwa o zajęcie miejsc państwa jest biernikiem "
                "(proszę kogo?), równym w formie dopełniaczowi.",
            ),
        ],
        related=[
            "tryb-rozka",
            "jezyk-grzecznosci",
            "konstrukcje-modalne",
        ],
    ),
    GrammarTopic(
        slug="konstrukcje-modalne",
        title="Konstrukcje modalne",
        level="C1",
        category="Składnia",
        summary="Stopniowanie zobowiązania i możliwości: należy, wypada, należałoby, jesteśmy "
        "zobowiązani, wolno.",
        explanation=(
            "Konstrukcje modalne pozwalają precyzyjnie określić siłę i źródło zobowiązania.\n\n"
            "- **należy** wyraża normę: *należy dochować terminu*.\n"
            "- **wypada** odwołuje się do obyczaju: *wypada podziękować*.\n"
            "- **należałoby**, **wypadałoby** łagodzą postulat: *należałoby to sprawdzić*.\n"
            "- **jesteśmy zobowiązani** wskazuje źródło w umowie lub prawie.\n"
            "- **wolno** dotyczy pozwolenia, **można** — możliwości lub pozwolenia, "
            "zależnie od kontekstu.\n\n"
            "Skala siły: *można* < *warto* < *należy* < *musi*."
        ),
        structure="bezosobowe: należy/wypada/należałoby + bezokolicznik · osobowe: jestem "
        "zobowiązany + bezokolicznik",
        rules=[
            "*Należy* wyraża normę, *wypada* — obyczaj, *należałoby* — postulat złagodzony.",
            "*Jesteśmy zobowiązani* wskazuje źródło zobowiązania w umowie lub prawie.",
            "*Wolno* dotyczy pozwolenia; *można* może wyrażać możliwość lub pozwolenie.",
            "Stopniuj siłę: *można* < *warto* < *należy* < *musi*.",
        ],
        examples=[
            GrammarExample(
                text="Należy dochować terminu wskazanego w umowie.",
                translation=None,
            ),
            GrammarExample(
                text="Wypadałoby poinformować partnerów o zmianie harmonogramu.",
                translation=None,
                note="postulat złagodzony",
            ),
            GrammarExample(
                text="Nie wolno nam ignorować sygnałów ostrzegawczych.",
                translation=None,
                note="brak pozwolenia",
            ),
            GrammarExample(
                text="Czy można tu zaparkować?",
                translation=None,
                note="pytanie o pozwolenie",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wypada, że trzeba to zrobić.",
                correct="Wypada to zrobić.",
                note="*Wypada* łączy się bezpośrednio z bezokolicznikiem.",
            ),
            GrammarMistake(
                wrong="Jesteśmy zobowiązani, że dostarczymy towar.",
                correct="Jesteśmy zobowiązani dostarczyć towar.",
                note="Konstrukcja modalna wymaga bezokolicznika, nie zdania z *że*.",
            ),
        ],
        related=[
            "musiec-powinien",
            "czasowniki-modalne",
            "jezyk-grzecznosci",
        ],
    ),
    GrammarTopic(
        slug="zwroty-idiomatyczne",
        title="Związki frazeologiczne",
        level="C1",
        category="Frazeologia",
        summary="Idiomy w użyciu: obrazowość, rejestr i ograniczenia kontekstowe.",
        explanation=(
            "Związek frazeologiczny to utrwalone połączenie wyrazów, którego znaczenie nie wynika "
            "z sumy znaczeń składników.\n\n"
            "- **Idiom właściwy** jest niepodzielny znaczeniowo: *wziąć nogi za pas* = uciec.\n"
            "- **Zestawienie** zachowuje znaczenia składników, ale ma utrwaloną formę: *pod "
            "karą*.\n"
            "- **Rejestr** bywa decydujący: *dać nogę* jest potoczne, *oddalić się* — "
            "neutralne.\n\n"
            "Modyfikacja idiomu w tekstach perswazyjnych jest możliwa, ale wymaga czytelnego "
            "sygnału, inaczej odbiorca odczyta ją jako błąd."
        ),
        structure="idiom + kontekst + rejestr",
        rules=[
            "Idiom jest niepodzielny znaczeniowo: *wziąć nogi za pas* nie znaczy dosłownie.",
            "Zachowaj formę utrwaloną: *mieć muchy w nosie*, nie: *mieć owady w nosie*.",
            "Sprawdź rejestr: *dać nogę* jest potoczne, *oddalić się* — neutralne.",
            "Modyfikacja idiomu jest dopuszczalna, ale wymaga czytelnego sygnału.",
        ],
        examples=[
            GrammarExample(
                text="Negocjacje utknęły w martwym punkcie, gdy obie strony zaczęły grać na "
                "zwłokę.",
                translation=None,
                note="dwa idiomy w jednym zdaniu, oba w tym samym rejestrze",
            ),
            GrammarExample(
                text="Nie owijajmy w bawełnę: projekt jest opóźniony.",
                translation=None,
            ),
            GrammarExample(
                text="Zrobił z igły widły, choć problem dotyczył jednego podpisu.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Musimy wziąć byka za rogi i przeciąć węzeł gordyjski.",
                correct="Musimy wziąć byka za rogi.",
                note="Dwa idiomy o podobnej funkcji tworzą pleonazm.",
            ),
            GrammarMistake(
                wrong="On zawsze ma muchy w nosie, czyli jest bardzo spokojny.",
                correct="On zawsze ma muchy w nosie, czyli jest obrażony.",
                note="Znaczenie idiomu jest utrwalone i nie podlega dowolnej zmianie.",
            ),
        ],
        related=[
            "frazeologia",
            "wyrazenia-utarte",
            "kolokacje",
        ],
    ),
    GrammarTopic(
        slug="kolokacje",
        title="Kolokacje",
        level="C1",
        category="Leksyka",
        summary="Naturalne połączenia wyrazowe: podejmować decyzję, odgrywać rolę, ponosić "
        "odpowiedzialność.",
        explanation=(
            "Kolokacja to utrwalone połączenie wyrazów, które jest poprawne i naturalne dla "
            "rodzimego użytkownika, choć nie wynika z reguły gramatycznej.\n\n"
            "- **Czasownik + rzeczownik**: *podejmować decyzję*, *odgrywać rolę*, *ponosić "
            "odpowiedzialność*.\n"
            "- **Przymiotnik + rzeczownik**: *istotną rolę*, *pełną odpowiedzialność*.\n"
            "- **Rzeczownik + dopełniacz**: *wzrost zatrudnienia*, *spadek popytu*.\n\n"
            "Bliskoznaczne czasowniki nie są wymienne: *podejmować decyzję*, ale *podejmować "
            "działania* i *podejmować próbę* mają własne zakresy."
        ),
        structure="czasownik + biernik · czasownik + dopełniacz · przymiotnik + rzeczownik",
        rules=[
            "Ucz się kolokacji w całości; bliskoznaczne czasowniki nie są wymienne.",
            "Rozróżniaj: *podejmować decyzję*, *podejmować działania*, *podejmować próbę*.",
            "Mów podejmować decyzję, nie robić decyzję. Brać odpowiedzialność jest "
            "poprawne i oznacza jej przyjmowanie.",
            "Kolokacja z rzeczownikiem abstrakcyjnym często wymaga dopełniacza: *wzrost "
            "zatrudnienia*.",
        ],
        examples=[
            GrammarExample(
                text="Rząd podjął decyzję o wydłużeniu terminu konsultacji.",
                translation=None,
            ),
            GrammarExample(
                text="Media odgrywają istotną rolę w kształtowaniu opinii publicznej.",
                translation=None,
            ),
            GrammarExample(
                text="Firma ponosi pełną odpowiedzialność za jakość świadczonych usług.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Musimy zrobić decyzję do piątku.",
                correct="Musimy podjąć decyzję do piątku.",
                note="*Decyzję* łączy się z *podejmować*, nie z *robić*.",
            ),
            GrammarMistake(
                wrong="Należy wziąć odpowiedzialność o błąd.",
                correct="Należy wziąć odpowiedzialność za błąd.",
                note="Wziąć odpowiedzialność jest poprawną kolokacją i łączy się z za + "
                "biernik. Ponieść odpowiedzialność akcentuje konsekwencje, nie samo "
                "przyjęcie odpowiedzialności.",
            ),
        ],
        related=[
            "frazeologia",
            "zwroty-idiomatyczne",
            "dobor-slow",
        ],
    ),
    GrammarTopic(
        slug="slowotworstwo",
        title="Słowotwórstwo",
        level="C1",
        category="Morfologia",
        summary="Derywacja, kompozycja i konwersja; funkcje formantów i ich odcienie znaczeniowe.",
        explanation=(
            "Słowotwórstwo opisuje, jak z istniejących tematów powstają nowe wyrazy i jakie "
            "znaczenie wnosi formant.\n\n"
            "- **Derywacja sufiksalna**: *-ość* tworzy nazwy cech (*odporny* → *odporność*), "
            "*-izm* — nazwy doktryn (*liberalizm*).\n"
            "- **Derywacja prefiksalna**: *nad-* oznacza nadmiar, *pod-* częściowość, *prze-* "
            "przekroczenie.\n"
            "- **Kompozycja** łączy dwa tematy: *współautorstwo*, *samokontrola*.\n"
            "- **Konwersja** zmienia kategorię bez zmiany formy: *chory* (przymiotnik) → *chory* "
            "(rzeczownik).\n\n"
            "Formanty niosą ocenę: zdrobnienia i zgrubienia w tekstach formalnych wymagają "
            "świadomej decyzji."
        ),
        structure="temat + formant · prefiks + temat · temat + temat",
        rules=[
            "Sufiks *-ość* tworzy nazwy cech od przymiotników: *odporny* → *odporność*.",
            "Sufiks *-izm* tworzy nazwy doktryn i postaw: *liberalizm*, *aktywizm*.",
            "Prefiksy modyfikują znaczenie: *nad-* (nadmiar), *pod-* (częściowość), *prze-* "
            "(przekroczenie).",
            "Zdrobnienia i zgrubienia niosą ocenę; w tekstach formalnych używaj ich świadomie.",
        ],
        examples=[
            GrammarExample(
                text="Odporność systemu zależy od jakości danych wejściowych.",
                translation=None,
            ),
            GrammarExample(
                text="Nadinterpretacja wyników prowadzi do błędnych wniosków.",
                translation=None,
                note="prefiks *nad-* = nadmiar",
            ),
            GrammarExample(
                text="Współautorstwo tekstu wymaga uzgodnienia zakresu odpowiedzialności.",
                translation=None,
                note="kompozycja",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Odporność systemu zależą od jakości danych.",
                correct="Odporność systemu zależy od jakości danych.",
                note="Rzeczownik odprzymiotnikowy odporność jest w liczbie pojedynczej "
                "i wymaga orzeczenia zależy.",
            ),
            GrammarMistake(
                wrong="Musimy podjąć przeddecyzję.",
                correct="Musimy podjąć decyzję wstępną.",
                note="Prefiks *przed-* nie tworzy swobodnie rzeczowników od rzeczowników "
                "odczasownikowych.",
            ),
        ],
        related=[
            "prefiksy-znaczenia",
            "rzeczowniki-odczasownikowe",
            "formy-archaiczne",
        ],
    ),
]
