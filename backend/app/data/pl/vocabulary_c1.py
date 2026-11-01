"""C1 vocabulary sets."""

from app.data._types import PartOfSpeech, VocabularyEntry, VocabularySet


def _entry(word: str, pos: PartOfSpeech, definition: str, example: str) -> VocabularyEntry:
    return VocabularyEntry(word=word, pos=pos, definition=definition, example=example)


C1_SETS: list[VocabularySet] = [
    VocabularySet(
        id="akademicki_c1",
        level="C1",
        topic="Język akademicki",
        unit_ref="c1-unit-1",
        words=[
            _entry(
                "przesłanka",
                "noun",
                "Twierdzenie, na którym opiera się wniosek.",
                "Każda przesłanka wymaga uzasadnienia.",
            ),
            _entry(
                "zależność",
                "noun",
                "Relacja między elementami lub zjawiskami.",
                "Badanie wykazało zależność między zmiennymi.",
            ),
            _entry(
                "zakres",
                "noun",
                "Granice tematu, działania lub zbioru.",
                "Autor jasno określa zakres analizy.",
            ),
            _entry(
                "wykazywać",
                "verb",
                "Przedstawiać dowody potwierdzające twierdzenie.",
                "Wyniki wykazują istotną różnicę.",
            ),
        ],
    ),
    VocabularySet(
        id="interpretacja_c1",
        level="C1",
        topic="Interpretacja i perspektywa",
        unit_ref="c1-unit-2",
        words=[
            _entry(
                "przypuszczenie",
                "noun",
                "Sąd przyjęty bez pełnej pewności.",
                "To przypuszczenie wymaga dalszej weryfikacji.",
            ),
            _entry(
                "perspektywa",
                "noun",
                "Punkt widzenia, z którego rozpatruje się sprawę.",
                "Tekst przedstawia perspektywę mieszkańców.",
            ),
            _entry(
                "zatem",
                "adverb",
                "Słowo wprowadzające logiczny wniosek.",
                "Dane są niepełne, zatem wniosek pozostaje wstępny.",
            ),
            _entry(
                "niuans",
                "noun",
                "Drobna, lecz znacząca różnica znaczenia.",
                "Tłumaczenie nie oddaje tego niuansu.",
            ),
        ],
    ),
    VocabularySet(
        id="redakcja_c1",
        level="C1",
        topic="Redakcja i styl",
        unit_ref="c1-unit-3",
        words=[
            _entry(
                "dwuznaczność",
                "noun",
                "Możliwość rozumienia wypowiedzi na więcej niż jeden sposób.",
                "Redaktor usunął dwuznaczność z instrukcji.",
            ),
            _entry(
                "zwięzłość",
                "noun",
                "Przekazywanie treści w niewielu słowach.",
                "Zwięzłość nie powinna ograniczać precyzji.",
            ),
            _entry(
                "powtórzenie",
                "noun",
                "Ponowne użycie tego samego słowa lub treści.",
                "Powtórzenie jest uzasadnione, gdy porządkuje wywód.",
            ),
            _entry(
                "redagować",
                "verb",
                "Opracowywać tekst pod względem treści i formy.",
                "Zespół redaguje raport przed publikacją.",
            ),
        ],
    ),
    VocabularySet(
        id="badania_c1",
        level="C1",
        topic="Badania i argumentacja akademicka",
        unit_ref="c1-unit-4",
        words=[
            _entry(
                "metodologia",
                "noun",
                "Zasady i metody stosowane w badaniu.",
                "Metodologia badania została szczegółowo opisana.",
            ),
            _entry(
                "próba",
                "noun",
                "Część populacji wybrana do analizy.",
                "Próba obejmowała osoby z trzech regionów.",
            ),
            _entry(
                "zestawienie",
                "noun",
                "Uporządkowany zbiór informacji lub porównanie danych.",
                "Zestawienie pokazuje różnice między grupami.",
            ),
            _entry(
                "zweryfikować",
                "verb",
                "Sprawdzić, czy informacja lub hipoteza jest prawdziwa.",
                "Należy zweryfikować te wyniki w kolejnych badaniach.",
            ),
        ],
    ),
    VocabularySet(
        id="dyskurs_c1",
        level="C1",
        topic="Dyskurs publiczny i instytucje",
        unit_ref="c1-unit-5",
        words=[
            _entry(
                "rozporządzenie",
                "noun",
                "Akt prawny wydany przez uprawniony organ.",
                "Rozporządzenie określa nowe zasady finansowania.",
            ),
            _entry(
                "interesariusz",
                "noun",
                "Osoba lub grupa, na którą wpływa dane działanie.",
                "Interesariusze przedstawili swoje uwagi.",
            ),
            _entry(
                "wykluczenie",
                "noun",
                "Ograniczenie komuś udziału lub dostępu do czegoś.",
                "Projekt ma przeciwdziałać wykluczeniu cyfrowemu.",
            ),
            _entry(
                "argumentować",
                "verb",
                "Uzasadniać swoje stanowisko za pomocą argumentów.",
                "Autorka argumentuje na rzecz zmiany przepisów.",
            ),
        ],
    ),
    VocabularySet(
        id="literatura_c1",
        level="C1",
        topic="Literatura i interpretacja",
        unit_ref="c1-unit-6",
        words=[
            _entry(
                "narrator",
                "noun",
                "Głos opowiadający wydarzenia w utworze.",
                "Narrator opisuje wydarzenia z perspektywy dziecka.",
            ),
            _entry(
                "motyw",
                "noun",
                "Powracający temat lub element utworu.",
                "Podróż jest ważnym motywem tej powieści.",
            ),
            _entry(
                "konwencja",
                "noun",
                "Utrwalony sposób tworzenia lub odbierania dzieła.",
                "Film świadomie nawiązuje do konwencji kryminału.",
            ),
            _entry(
                "odczytywać",
                "verb",
                "Interpretować znaczenie tekstu lub zachowania.",
                "Ten fragment można odczytywać na kilka sposobów.",
            ),
        ],
    ),
    VocabularySet(
        id="komunikacja_zawodowa_c1",
        level="C1",
        topic="Redakcja i komunikacja zawodowa",
        unit_ref="c1-unit-7",
        words=[
            _entry(
                "korekta",
                "noun",
                "Poprawianie błędów językowych i typograficznych.",
                "Tekst wymaga jeszcze korekty.",
            ),
            _entry(
                "spójność",
                "noun",
                "Logiczne powiązanie elementów wypowiedzi.",
                "Redaktor sprawdził spójność całego dokumentu.",
            ),
            _entry(
                "sformułowanie",
                "noun",
                "Sposób ujęcia myśli w słowach.",
                "To sformułowanie jest zbyt kategoryczne.",
            ),
            _entry(
                "przeredagować",
                "verb",
                "Napisać fragment ponownie, aby był jaśniejszy lub lepszy.",
                "Musimy przeredagować wstęp do raportu.",
            ),
        ],
    ),
    VocabularySet(
        id="powtorka_c1",
        level="C1",
        topic="Powtórka: synteza i precyzja",
        unit_ref="c1-unit-8",
        words=[
            _entry(
                "ograniczenie",
                "noun",
                "Czynnik zmniejszający zakres lub siłę działania.",
                "Autorzy wskazali ograniczenia badania.",
            ),
            _entry(
                "rozstrzygający",
                "adjective",
                "Pozwalający zakończyć spór lub podjąć decyzję.",
                "Dostępne dane nie są rozstrzygające.",
            ),
            _entry(
                "wieloznaczność",
                "noun",
                "Możliwość różnych interpretacji wyrażenia.",
                "Kontekst usuwa wieloznaczność tego terminu.",
            ),
            _entry(
                "syntetyczny",
                "adjective",
                "Zwięźle łączący najważniejsze informacje.",
                "Na końcu zamieszczono syntetyczne podsumowanie.",
            ),
        ],
    ),
    VocabularySet(
        id="metodologia-badan_c1",
        level="C1",
        topic="Metodologia badań",
        unit_ref="c1-unit-4",
        words=[
            _entry(
                "próba",
                "noun",
                "Część populacji wybrana do udziału w badaniu.",
                "Próba obejmowała mieszkańców trzech regionów.",
            ),
            _entry(
                "dobór",
                "noun",
                "Sposób wyboru elementów do określonego zbioru.",
                "Autorzy opisali dobór respondentów.",
            ),
            _entry(
                "zmienna",
                "noun",
                "Właściwość, której wartość może się zmieniać w badaniu.",
                "Wiek był jedną ze zmiennych uwzględnionych w analizie.",
            ),
            _entry(
                "replikować",
                "verb",
                "Powtórzyć badanie lub procedurę w celu sprawdzenia wyniku.",
                "Inny zespół próbował replikować eksperyment.",
            ),
        ],
    ),
    VocabularySet(
        id="retoryka-i-perswazja_c1",
        level="C1",
        topic="Retoryka i perswazja",
        unit_ref="c1-unit-2",
        words=[
            _entry(
                "zabieg",
                "noun",
                "Celowe działanie lub środek użyty w określonym celu.",
                "Powtórzenie jest tu świadomym zabiegiem retorycznym.",
            ),
            _entry(
                "perswazyjny",
                "adjective",
                "Mający skłonić odbiorcę do przyjęcia opinii lub działania.",
                "Autor posługuje się perswazyjnym językiem.",
            ),
            _entry(
                "apelować",
                "verb",
                "Zwracać się do odbiorcy z prośbą lub wezwaniem.",
                "Mówczyni apeluje o rzetelną debatę.",
            ),
            _entry(
                "odbiór",
                "noun",
                "Sposób, w jaki treść jest rozumiana przez odbiorców.",
                "Kontekst wpływa na odbiór wypowiedzi.",
            ),
        ],
    ),
    VocabularySet(
        id="redakcja-tekstu_c1",
        level="C1",
        topic="Redakcja tekstu i precyzja",
        unit_ref="c1-unit-3",
        words=[
            _entry(
                "dwuznaczność",
                "noun",
                "Możliwość rozumienia wypowiedzi na więcej niż jeden sposób.",
                "Redakcja usunęła dwuznaczność z instrukcji.",
            ),
            _entry(
                "doprecyzować",
                "verb",
                "Dodać szczegóły, które ograniczają niejasność.",
                "Proszę doprecyzować zakres analizy.",
            ),
            _entry(
                "zwięzły",
                "adjective",
                "Wyrażający treść krótko, bez zbędnych elementów.",
                "Zwięzłe podsumowanie ułatwia lekturę.",
            ),
            _entry(
                "nawiązanie",
                "noun",
                "Element tekstu odsyłający do wcześniej wspomnianej treści.",
                "To nawiązanie nie ma jednoznacznego poprzednika.",
            ),
        ],
    ),
    VocabularySet(
        id="interpretacja-danych_c1",
        level="C1",
        topic="Interpretacja danych i niepewność",
        unit_ref="c1-unit-4",
        words=[
            _entry(
                "współwystępowanie",
                "noun",
                "Pojawianie się dwóch zjawisk w tym samym czasie lub zbiorze obserwacji.",
                "Współwystępowanie zjawisk nie dowodzi związku przyczynowego.",
            ),
            _entry(
                "wniosek",
                "noun",
                "Sąd wyprowadzony z przesłanek lub analizy.",
                "Wniosek powinien uwzględniać ograniczenia próby.",
            ),
            _entry(
                "zależność",
                "noun",
                "Relacja, w której zmiana jednego elementu wiąże się z innym.",
                "Badanie wykazało zależność między zmiennymi.",
            ),
            _entry(
                "ostrożny",
                "adjective",
                "Wyrażający sąd bez nadmiernej pewności.",
                "Autor formułuje ostrożny wniosek.",
            ),
        ],
    ),
    VocabularySet(
        id="instytucje-publiczne_c1",
        level="C1",
        topic="Instytucje i procedury publiczne",
        unit_ref="c1-unit-5",
        words=[
            _entry(
                "rozporządzenie",
                "noun",
                "Akt prawny wydany przez uprawniony organ.",
                "Rozporządzenie określa szczegółowy tryb postępowania.",
            ),
            _entry(
                "kompetencja",
                "noun",
                "Zakres uprawnień lub umiejętności przypisanych osobie albo instytucji.",
                "Kompetencje urzędu opisano w ustawie.",
            ),
            _entry(
                "wnioskować",
                "verb",
                "Składać formalny wniosek lub wyprowadzać konkluzję z danych.",
                "Organ może wnioskować o uzupełnienie dokumentów.",
            ),
            _entry(
                "bezstronny",
                "adjective",
                "Niekierujący się osobistym interesem ani uprzedzeniem.",
                "Postępowanie powinno być bezstronne.",
            ),
        ],
    ),
    VocabularySet(
        id="komunikacja-instytucjonalna_c1",
        level="C1",
        topic="Komunikacja zawodowa i instytucjonalna",
        unit_ref="c1-unit-7",
        words=[
            _entry(
                "uzgodnienie",
                "noun",
                "Wspólne ustalenie treści lub sposobu działania.",
                "Projekt wymaga uzgodnienia z partnerami.",
            ),
            _entry(
                "przedłożyć",
                "verb",
                "Formalnie przedstawić dokument lub propozycję do rozpatrzenia.",
                "Zarząd przedłożył projekt do konsultacji.",
            ),
            _entry(
                "zobowiązanie",
                "noun",
                "Obietnica lub obowiązek podjęcia określonego działania.",
                "Umowa zawiera zobowiązanie do zachowania poufności.",
            ),
            _entry(
                "wiążący",
                "adjective",
                "Wymagający zastosowania lub wykonania.",
                "Uchwała jest wiążąca dla wszystkich oddziałów.",
            ),
        ],
    ),
]
