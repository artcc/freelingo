"""Polish grammar topics — C2."""

from app.data._types import GrammarExample, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="frazeologia",
        title="Frazeologizmy",
        level="C2",
        category="Gramatyka",
        summary="Frazeologizmy mają znaczenie, którego nie da się odczytać wyłącznie ze składników.",
        explanation="Związki frazeologiczne różnią się stopniem utrwalenia i formalności. Ich znaczenie zależy od kontekstu, a niektóre dopuszczają ograniczone warianty. Dosłowne tłumaczenie często prowadzi do nienaturalnej polszczyzny.",
        structure="rzucić nowe światło; wyciągnąć wnioski; mieć coś na uwadze",
        rules=[
            "Ustal znaczenie związku z kontekstu.",
            "Sprawdź, czy frazeologizm pasuje do rejestru.",
            "Nie zmieniaj utrwalonych składników bez wyraźnego efektu stylistycznego.",
        ],
        examples=[
            GrammarExample(
                text="Nowe dane rzuciły światło na przyczynę awarii.",
                translation=None,
                note="Znaczenie przenośne.",
            ),
            GrammarExample(
                text="Warto mieć na uwadze ograniczenia badania.",
                translation=None,
                note="Utrwalone połączenie.",
            ),
        ],
        common_mistakes=[],
    ),
    GrammarTopic(
        slug="rejestry",
        title="Rejestry językowe",
        level="C2",
        category="Gramatyka",
        summary="Rejestr językowy zależy od odbiorcy, celu i sytuacji komunikacyjnej.",
        explanation="Wypowiedź może być potoczna, neutralna, oficjalna, specjalistyczna lub artystyczna. Mieszanie rejestrów bywa celowym środkiem stylistycznym, lecz bez uzasadnienia osłabia spójność. Wybór formy grzecznościowej niesie znaczenie społeczne.",
        structure="ty; pan/pani; formy urzędowe i specjalistyczne",
        rules=[
            "Ustal odbiorcę i cel przed doborem rejestru.",
            "Zachowuj spójność rejestru w obrębie tekstu.",
            "Traktuj zmianę rejestru jako świadomy zabieg.",
        ],
        examples=[
            GrammarExample(
                text="Uprzejmie proszę o potwierdzenie terminu.",
                translation=None,
                note="Rejestr formalny.",
            ),
            GrammarExample(
                text="Daj znać, kiedy będziesz.",
                translation=None,
                note="Rejestr nieformalny.",
            ),
        ],
        common_mistakes=[],
    ),
    GrammarTopic(
        slug="retoryka",
        title="Środki retoryczne",
        level="C2",
        category="Gramatyka",
        summary="Środki retoryczne organizują argumentację i wpływają na odbiór tekstu.",
        explanation="Kontrast, powtórzenie, pytanie retoryczne i analogia mogą porządkować tok rozumowania lub wzmacniać perswazję. Analizując tekst, oddzielaj efekt retoryczny od wartości dowodowej argumentu.",
        structure="teza, przesłanki, zastrzeżenie, wniosek",
        rules=[
            "Oceniaj, czy przesłanki wspierają tezę.",
            "Rozpoznawaj założenia niewypowiedziane wprost.",
            "Nie utożsamiaj przekonującej formy z prawdziwością twierdzenia.",
        ],
        examples=[
            GrammarExample(
                text="Czy możemy pozwolić sobie na dalsze odkładanie tej decyzji?",
                translation=None,
                note="Pytanie retoryczne.",
            ),
            GrammarExample(
                text="Z jednej strony koszty rosną, z drugiej — opóźnienie zwiększa ryzyko.",
                translation=None,
                note="Równoważenie argumentów.",
            ),
        ],
        common_mistakes=[],
    ),
    GrammarTopic(
        slug="ironia-i-pragmatyka",
        title="Ironia i znaczenie pragmatyczne",
        level="C2",
        category="Gramatyka",
        summary="Znaczenie wypowiedzi zależy od kontekstu, intencji i wspólnej wiedzy rozmówców.",
        explanation="Ironia, aluzja, niedopowiedzenie i implikatura mogą przekazywać treść inną niż dosłowna. Ich interpretacja wymaga uwzględnienia relacji między rozmówcami, sytuacji oraz sygnałów językowych; nie należy przypisywać intencji bez wystarczających przesłanek.",
        structure="dosłownie; w przenośni; aluzja; niedopowiedzenie",
        rules=[
            "Oddzielaj sens dosłowny od możliwego sensu implikowanego.",
            "Uzasadniaj interpretację sygnałami z kontekstu.",
            "Uwzględniaj, że ironia może być nieczytelna poza daną sytuacją.",
        ],
        examples=[
            GrammarExample(
                text="Świetnie, kolejna godzina w korku.",
                translation=None,
                note="Kontekst może wskazywać na ironię.",
            ),
            GrammarExample(
                text="Nie powiedział tego wprost, ale aluzja była czytelna.",
                translation=None,
                note="Znaczenie przekazane pośrednio.",
            ),
        ],
        common_mistakes=[],
    ),
    GrammarTopic(
        slug="warianty-i-norma",
        title="Warianty, norma i zmiana języka",
        level="C2",
        category="Gramatyka",
        summary="Polszczyzna zmienia się w czasie i różnicuje zależnie od regionu oraz sytuacji.",
        explanation="Norma wzorcowa i użytkowa opisują różne poziomy akceptacji form. Regionalizmy, archaizmy, zapożyczenia i neologizmy mogą pełnić funkcję stylistyczną. Ocenę formy należy oddzielić od opisu jej społecznego użycia.",
        structure="norma; regionalizm; archaizm; neologizm",
        rules=[
            "Rozpoznawaj, czy forma jest regionalna, historyczna, środowiskowa czy ogólnopolska.",
            "Oceniaj poprawność w odniesieniu do rejestru i celu wypowiedzi.",
            "Nie utożsamiaj częstego użycia z neutralnym stylem.",
        ],
        examples=[
            GrammarExample(
                text="W dialogu autor zachował regionalizmy bohaterów.",
                translation=None,
                note="Wariant języka buduje charakterystykę postaci.",
            ),
            GrammarExample(
                text="To zapożyczenie jest już powszechne, ale nadal ma potoczny odcień.",
                translation=None,
                note="Częstość i rejestr to odrębne cechy.",
            ),
        ],
        common_mistakes=[],
    ),
    GrammarTopic(
        slug="szyk-a-akcent",
        title="Szyk zdania a akcent informacyjny",
        level="C2",
        category="Gramatyka",
        summary="Szyk pozwala subtelnie zaznaczyć kontrast, korektę lub punkt wyjścia wypowiedzi.",
        explanation="Odmiana daje polszczyźnie dużą swobodę szyku, ale przesunięcie elementu zmienia jego status informacyjny. Kontekst i intonacja rozstrzygają, czy dana kolejność jest neutralna, czy kontrastowa.",
        structure="znane → nowe; element kontrastowany w pozycji akcentowanej",
        rules=[
            "Zachowuj neutralny szyk, jeśli nie ma potrzeby wyróżnienia informacji.",
            "Używaj przestawienia dla czytelnego kontrastu lub korekty.",
            "Oceń szyk w kontekście całego akapitu, nie pojedynczego zdania.",
        ],
        examples=[
            GrammarExample(
                text="To rozwiązanie zaproponował zespół, nie zarząd.", note="Kontrast wykonawcy."
            ),
            GrammarExample(
                text="Zespół zaproponował to rozwiązanie wczoraj.", note="Neutralny szyk."
            ),
        ],
    ),
    GrammarTopic(
        slug="zakres-negacji",
        title="Zakres negacji",
        level="C2",
        category="Gramatyka",
        summary="Pozycja negacji i wyrazów ograniczających decyduje o zakresie zaprzeczenia.",
        explanation="Nie może zaprzeczać całemu zdaniu lub jego składnikowi, a wyrażenia takie jak tylko i nawet dodatkowo zawężają zakres. Odczytanie zależy od szyku, akcentu i kontekstu.",
        structure="nie wszyscy; nie tylko A, lecz także B",
        rules=[
            "Ustal, który składnik obejmuje negacja.",
            "Używaj przecinka i spójników zgodnie z konstrukcją przeciwstawną.",
            "Przepisz zdanie, jeśli zakres zaprzeczenia pozostaje niejasny.",
        ],
        examples=[
            GrammarExample(
                text="Nie wszyscy uczestnicy poparli wniosek.",
                note="Negacja obejmuje kwantyfikator.",
            ),
            GrammarExample(
                text="Nie tylko zebrano dane, lecz także sprawdzono ich jakość.",
                note="Konstrukcja rozszerzająca.",
            ),
        ],
    ),
    GrammarTopic(
        slug="elipsa-i-powtorzenia",
        title="Elipsa i powtórzenia składniowe",
        level="C2",
        category="Gramatyka",
        summary="Pominięcie powtarzalnego elementu może usprawnić tekst, jeśli jego odniesienie jest jasne.",
        explanation="Elipsa usuwa element możliwy do odtworzenia z kontekstu. Zbyt dalekie pominięcie utrudnia interpretację, a powtórzenie może być celowe dla kontrastu lub rytmu.",
        structure="pierwszy człon + pominięty element wspólny + drugi człon",
        rules=[
            "Pomijaj tylko element łatwy do odtworzenia.",
            "Zachowuj równoległą składnię w zestawionych członach.",
            "Powtarzaj wyraz, gdy jego brak tworzyłby dwuznaczność.",
        ],
        examples=[
            GrammarExample(
                text="Pierwszy zespół zebrał dane, drugi — przeprowadził analizę.",
                note="Elipsa czasownika w drugim członie.",
            ),
            GrammarExample(
                text="Autorka ocenia zarówno metodę, jak i wnioski z badania.",
                note="Równoległa składnia.",
            ),
        ],
    ),
    GrammarTopic(
        slug="inwersja-i-podmiot-domyslny",
        title="Inwersja i podmiot domyślny",
        level="C2",
        category="Gramatyka",
        summary="Zmiana szyku i pominięcie podmiotu mogą kształtować perspektywę tekstu.",
        explanation="Końcówki czasownika często pozwalają pominąć zaimek, ale jego obecność może zaznaczyć kontrast. Inwersja bywa neutralna w określonym kontekście, lecz nadmierna może brzmieć sztucznie.",
        structure="podmiot domyślny; zaimek dla kontrastu",
        rules=[
            "Pomiń podmiot, gdy jest jasny i nie wymaga kontrastu.",
            "Dodaj zaimek, gdy rozróżnia osoby lub akcentuje stanowisko.",
            "Oceniaj inwersję względem informacji poprzedzającej.",
        ],
        examples=[
            GrammarExample(
                text="Przeanalizowaliśmy wyniki i przygotowaliśmy rekomendacje.",
                note="Podmiot domyślny.",
            ),
            GrammarExample(
                text="My przygotowaliśmy rekomendacje, a oni odpowiadają za wdrożenie.",
                note="Podmiot wyrażony dla kontrastu.",
            ),
        ],
    ),
    GrammarTopic(
        slug="paralelizm-skladniowy",
        title="Paralelizm składniowy",
        level="C2",
        category="Gramatyka",
        summary="Równoległa budowa członów ułatwia porównanie i wzmacnia przejrzystość argumentu.",
        explanation="Paralelizm polega na powtarzaniu podobnej struktury składniowej. Nierównoległe elementy po spójnikach zestawnych mogą tworzyć niezamierzoną dwuznaczność.",
        structure="zarówno + forma A, jak i + forma A",
        rules=[
            "Utrzymuj tę samą kategorię gramatyczną w zestawionych członach.",
            "Sprawdzaj równoległość po zarówno...jak i oraz nie tylko...lecz także.",
            "Łam paralelizm świadomie, a nie przypadkowo.",
        ],
        examples=[
            GrammarExample(
                text="Projekt wymaga zarówno analizy danych, jak i oceny ryzyka.",
                note="Równoległe rzeczowniki.",
            ),
            GrammarExample(
                text="Zespół nie tylko zebrał materiał, lecz także go zweryfikował.",
                note="Równoległe formy czasownikowe.",
            ),
        ],
    ),
    GrammarTopic(
        slug="konstrukcje-korelacyjne",
        title="Konstrukcje korelacyjne",
        level="C2",
        category="Gramatyka",
        summary="Zestawy spójników wiążą dwa człony i wskazują ich wzajemną relację.",
        explanation="Konstrukcje zarówno...jak i, albo...albo, ani...ani oraz im...tym wymagają zgodnego połączenia członów. Ich elementy powinny obejmować składniki o podobnej funkcji.",
        structure="im + stopień wyższy, tym + stopień wyższy",
        rules=[
            "Zachowuj oba elementy pary korelacyjnej.",
            "Łącz składniki o równoległej funkcji składniowej.",
            "Dopasuj negację do ani...ani.",
        ],
        examples=[
            GrammarExample(
                text="Im dokładniej opisano metodę, tym łatwiej ocenić wynik.",
                note="Korelacja stopnia.",
            ),
            GrammarExample(
                text="Ani autor, ani recenzenci nie zakwestionowali danych.",
                note="Konstrukcja złożona z ani.",
            ),
        ],
    ),
    GrammarTopic(
        slug="odniesienia-zaimkowe",
        title="Jednoznaczność odniesień zaimkowych",
        level="C2",
        category="Gramatyka",
        summary="Zaimek powinien jednoznacznie wskazywać rzeczownik lub treść, do której się odnosi.",
        explanation="W zdaniach z kilkoma rzeczownikami zaimek może mieć więcej niż jednego możliwego poprzednika. Powtórzenie rzeczownika lub przebudowa zdania często usuwa niejasność.",
        structure="zaimek → jednoznaczny poprzednik",
        rules=[
            "Sprawdzaj możliwe poprzedniki każdego zaimka.",
            "Powtarzaj rzeczownik, jeśli dwa odniesienia są równie prawdopodobne.",
            "Nie używaj zaimka to, gdy jego zakres jest niejasny.",
        ],
        examples=[
            GrammarExample(
                text="Komisja omówiła raport zespołu i zatwierdziła jego wnioski.",
                note="Odniesienie zaimka jest czytelne.",
            ),
            GrammarExample(
                text="Po rozmowie z autorką redaktor zmienił jej tytuł.",
                note="Właściciel tytułu może wymagać doprecyzowania.",
            ),
        ],
    ),
    GrammarTopic(
        slug="przeksztalcenia-imieslowowe",
        title="Przekształcenia imiesłowowe",
        level="C2",
        category="Gramatyka",
        summary="Konstrukcje imiesłowowe kondensują zdanie, ale wymagają wspólnego i czytelnego wykonawcy.",
        explanation="Imiesłów przysłówkowy odnosi się do podmiotu zdania nadrzędnego. Błędne przypisanie wykonawcy tworzy konstrukcję wiszącą; w takim wypadku należy przywrócić zdanie podrzędne.",
        structure="analizując dane, badacz zauważył... (nie: analizując dane, wynik...)",
        rules=[
            "Upewnij się, że wykonawca imiesłowu jest podmiotem zdania nadrzędnego.",
            "Zachowuj właściwą relację czasową między czynnościami.",
            "Zastąp konstrukcję zdaniem, jeśli wykonawcy są różni.",
        ],
        examples=[
            GrammarExample(
                text="Analizując dane, badacz zauważył nieoczekiwany wzorzec.",
                note="Wspólny wykonawca.",
            ),
            GrammarExample(
                text="Gdy badacz analizował dane, pojawił się nowy problem.",
                note="Zdanie podrzędne usuwa zmianę wykonawcy.",
            ),
        ],
    ),
    GrammarTopic(
        slug="operatorzy-i-kwantyfikatory",
        title="Operatory i kwantyfikatory",
        level="C2",
        category="Gramatyka",
        summary="Kwantyfikatory określają zakres odniesienia i mogą zmieniać interpretację zdania.",
        explanation="Wszystkie, niektóre, żaden, każdy i większość nie są wymienne. Ich zakres może obejmować różne składniki zdania, a forma orzeczenia zależy od budowy grupy podmiotu.",
        structure="każdy uczestnik; większość uczestników; żaden z wniosków",
        rules=[
            "Dobieraj kwantyfikator do zamierzonego zakresu.",
            "Uzgadniaj przypadek rzeczownika z konstrukcją kwantyfikującą.",
            "Sprawdzaj zgodę orzeczenia przy większość, część i każdy.",
        ],
        examples=[
            GrammarExample(
                text="Każdy z wniosków wymaga osobnego uzasadnienia.",
                note="Każdy z + dopełniacz, orzeczenie w liczbie pojedynczej.",
            ),
            GrammarExample(
                text="Część uczestników zgłosiła poprawki.", note="Orzeczenie uzgodnione z część."
            ),
        ],
    ),
    GrammarTopic(
        slug="rejestr-a-skladnia",
        title="Rejestr a wybór składni",
        level="C2",
        category="Gramatyka",
        summary="Rejestr wpływa na wybór konstrukcji, lecz nie znosi wymagań składniowych.",
        explanation="Tekst urzędowy, akademicki i potoczny różnią się długością zdań, nominalizacją i stopniem bezpośredniości. Formalność nie uzasadnia niejasnych konstrukcji ani niepotrzebnego rozbudowywania zdań.",
        structure="dobór konstrukcji do odbiorcy i celu",
        rules=[
            "Dostosuj składnię do gatunku i odbiorcy.",
            "Zachowuj jasne relacje między podmiotem, czynnością i skutkiem.",
            "Odróżniaj konwencję stylistyczną od poprawności gramatycznej.",
        ],
        examples=[
            GrammarExample(
                text="Prosimy przesłać formularz do piątku.", note="Zwięzła forma formalna."
            ),
            GrammarExample(
                text="Będziemy wdzięczni za przesłanie formularza do piątku.",
                note="Uprzejma forma korespondencyjna.",
            ),
        ],
    ),
]
