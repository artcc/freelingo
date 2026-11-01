"""B2 vocabulary sets."""

from app.data._types import PartOfSpeech, VocabularyEntry, VocabularySet


def _entry(word: str, pos: PartOfSpeech, definition: str, example: str) -> VocabularyEntry:
    return VocabularyEntry(word=word, pos=pos, definition=definition, example=example)


B2_SETS: list[VocabularySet] = [
    VocabularySet(
        id="spoleczenstwo_b2",
        level="B2",
        topic="Społeczeństwo i zmiany",
        unit_ref="b2-unit-1",
        words=[
            _entry(
                "nierówność",
                "noun",
                "Różnica w dostępie do praw, zasobów lub możliwości.",
                "Raport opisuje nierówność dochodową.",
            ),
            _entry(
                "dobrobyt",
                "noun",
                "Stan zaspokojenia potrzeb materialnych i społecznych.",
                "Wzrost gospodarczy nie zawsze zwiększa dobrobyt.",
            ),
            _entry(
                "wdrożenie",
                "noun",
                "Wprowadzenie rozwiązania do praktycznego użycia.",
                "Wdrożenie nowych zasad wymaga czasu.",
            ),
            _entry(
                "zrównoważony",
                "adjective",
                "Uwzględniający potrzeby obecne i przyszłe.",
                "Miasto szuka zrównoważonego rozwoju.",
            ),
        ],
    ),
    VocabularySet(
        id="media_i_kultura_b2",
        level="B2",
        topic="Media i kultura",
        unit_ref="b2-unit-2",
        words=[
            _entry(
                "wiarygodność",
                "noun",
                "Cecha informacji, której można zaufać.",
                "Redakcja sprawdza wiarygodność źródeł.",
            ),
            _entry(
                "odbiorca",
                "noun",
                "Osoba, do której skierowano komunikat lub dzieło.",
                "Autor dostosował tekst do odbiorcy.",
            ),
            _entry(
                "interpretować",
                "verb",
                "Wyjaśniać znaczenie na podstawie kontekstu.",
                "Czytelnicy różnie interpretują zakończenie.",
            ),
            _entry(
                "przekaz",
                "noun",
                "Treść lub myśl przekazywana odbiorcy.",
                "Film ma mocny przekaz społeczny.",
            ),
        ],
    ),
    VocabularySet(
        id="precyzja_b2",
        level="B2",
        topic="Precyzyjne wypowiedzi",
        unit_ref="b2-unit-3",
        words=[
            _entry(
                "jednoznaczny",
                "adjective",
                "Mający tylko jedno możliwe znaczenie.",
                "Umowa powinna zawierać jednoznaczne warunki.",
            ),
            _entry(
                "zastrzeżenie",
                "noun",
                "Ograniczenie lub uwaga dotycząca twierdzenia.",
                "Przedstawił ważne zastrzeżenie do propozycji.",
            ),
            _entry(
                "spójność",
                "noun",
                "Logiczne i stylistyczne powiązanie elementów.",
                "Spójność argumentacji ułatwia lekturę.",
            ),
            _entry(
                "doprecyzować",
                "verb",
                "Uściślić treść lub znaczenie.",
                "Musimy doprecyzować zakres projektu.",
            ),
        ],
    ),
    VocabularySet(
        id="praca_b2",
        level="B2",
        topic="Praca, gospodarka i organizacje",
        unit_ref="b2-unit-4",
        words=[
            _entry(
                "wynagrodzenie",
                "noun",
                "Pieniądze otrzymywane za wykonaną pracę.",
                "Wynagrodzenie zależy od doświadczenia.",
            ),
            _entry(
                "przedsiębiorstwo",
                "noun",
                "Organizacja prowadząca działalność gospodarczą.",
                "Przedsiębiorstwo zatrudnia kilkaset osób.",
            ),
            _entry(
                "wdrażać",
                "verb",
                "Wprowadzać nowe rozwiązanie do praktycznego użycia.",
                "Firma wdraża nowy system obsługi.",
            ),
            _entry(
                "wydajność",
                "noun",
                "Ilość lub jakość pracy wykonanej w określonym czasie.",
                "Nowe narzędzie zwiększyło wydajność zespołu.",
            ),
        ],
    ),
    VocabularySet(
        id="debata_b2",
        level="B2",
        topic="Media, debata i wiarygodność",
        unit_ref="b2-unit-5",
        words=[
            _entry(
                "nagłówek",
                "noun",
                "Tytuł umieszczony nad artykułem lub wiadomością.",
                "Nagłówek nie oddaje treści całego raportu.",
            ),
            _entry(
                "źródło",
                "noun",
                "Miejsce lub osoba, od której pochodzi informacja.",
                "Dziennikarz sprawdził źródło tej wiadomości.",
            ),
            _entry(
                "sprostowanie",
                "noun",
                "Publiczna poprawka błędnej lub nieścisłej informacji.",
                "Redakcja opublikowała sprostowanie.",
            ),
            _entry(
                "kwestionować",
                "verb",
                "Podawać w wątpliwość prawdziwość lub zasadność czegoś.",
                "Eksperci kwestionują metodę badania.",
            ),
        ],
    ),
    VocabularySet(
        id="srodowisko_b2",
        level="B2",
        topic="Środowisko i rozwój nauki",
        unit_ref="b2-unit-6",
        words=[
            _entry(
                "bioróżnorodność",
                "noun",
                "Różnorodność organizmów żyjących na danym obszarze.",
                "Ochrona bioróżnorodności wymaga współpracy.",
            ),
            _entry(
                "emisja",
                "noun",
                "Uwalnianie substancji lub energii do otoczenia.",
                "Miasto chce ograniczyć emisję spalin.",
            ),
            _entry(
                "odnawialny",
                "adjective",
                "Możliwy do naturalnego odtworzenia w krótkim czasie.",
                "Energia słoneczna jest źródłem odnawialnym.",
            ),
            _entry(
                "badanie",
                "noun",
                "Działanie służące zdobyciu lub sprawdzeniu wiedzy.",
                "Badanie porównuje dwa sposoby uprawy.",
            ),
        ],
    ),
    VocabularySet(
        id="styl_b2",
        level="B2",
        topic="Precyzyjny styl i argumentacja",
        unit_ref="b2-unit-7",
        words=[
            _entry(
                "spójny",
                "adjective",
                "Logicznie powiązany i uporządkowany.",
                "Raport zawiera spójny zestaw argumentów.",
            ),
            _entry(
                "dwuznaczny",
                "adjective",
                "Dopuszczający więcej niż jedną interpretację.",
                "To zdanie jest dwuznaczne bez kontekstu.",
            ),
            _entry(
                "doprecyzowanie",
                "noun",
                "Dodanie szczegółu, który wyjaśnia znaczenie.",
                "Definicja wymaga krótkiego doprecyzowania.",
            ),
            _entry(
                "redagować",
                "verb",
                "Poprawiać i porządkować tekst przed publikacją.",
                "Zespół redaguje końcową wersję raportu.",
            ),
        ],
    ),
    VocabularySet(
        id="powtorka_b2",
        level="B2",
        topic="Powtórka: analiza i argumentacja",
        unit_ref="b2-unit-8",
        words=[
            _entry(
                "przesłanka",
                "noun",
                "Twierdzenie, na którym opiera się wniosek.",
                "Każda przesłanka powinna mieć uzasadnienie.",
            ),
            _entry(
                "wiarygodny",
                "adjective",
                "Zasługujący na zaufanie dzięki dobrym podstawom.",
                "Autor korzysta z wiarygodnych źródeł.",
            ),
            _entry(
                "konsekwencja",
                "noun",
                "Skutek lub logiczne następstwo działania.",
                "Raport omawia konsekwencje tej decyzji.",
            ),
            _entry(
                "zestawiać",
                "verb",
                "Umieszczać obok siebie, aby porównać elementy.",
                "W artykule zestawiono dane z dwóch lat.",
            ),
        ],
    ),
    VocabularySet(
        id="polityka-publiczna_b2",
        level="B2",
        topic="Polityka publiczna i regulacje",
        unit_ref="b2-unit-1",
        words=[
            _entry(
                "przepis",
                "noun",
                "Ustanowiona zasada określająca sposób postępowania.",
                "Nowy przepis zacznie obowiązywać w lipcu.",
            ),
            _entry(
                "wdrażać",
                "verb",
                "Wprowadzać plan, rozwiązanie lub regulację w życie.",
                "Samorząd wdraża program pilotażowy.",
            ),
            _entry(
                "wyjątek",
                "noun",
                "Przypadek, którego nie obejmuje ogólna reguła.",
                "Regulamin przewiduje jeden wyjątek.",
            ),
            _entry(
                "obowiązujący",
                "adjective",
                "Mający moc prawną lub stosowany w danym czasie.",
                "Przed złożeniem wniosku sprawdź obowiązujące przepisy.",
            ),
        ],
    ),
    VocabularySet(
        id="analiza-mediow_b2",
        level="B2",
        topic="Analiza mediów i przekazu",
        unit_ref="b2-unit-2",
        words=[
            _entry(
                "przekaz",
                "noun",
                "Treść lub komunikat przekazywany odbiorcom.",
                "Przekaz kampanii zmieniał się w kolejnych tygodniach.",
            ),
            _entry(
                "przedstawiać",
                "verb",
                "Ukazywać lub opisywać kogoś albo coś w określony sposób.",
                "Artykuł przedstawia problem z kilku perspektyw.",
            ),
            _entry(
                "stronniczy",
                "adjective",
                "Nieprzedstawiający różnych stron sprawy w równy sposób.",
                "Komentarz był wyraźnie stronniczy.",
            ),
            _entry(
                "odbiorca",
                "noun",
                "Osoba, do której skierowana jest informacja lub usługa.",
                "Odbiorca może odczytać ten komunikat inaczej.",
            ),
        ],
    ),
    VocabularySet(
        id="rynek-pracy_b2",
        level="B2",
        topic="Rynek pracy i zatrudnienie",
        unit_ref="b2-unit-4",
        words=[
            _entry(
                "zatrudnienie",
                "noun",
                "Praca wykonywana na określonych warunkach.",
                "Po szkoleniu wzrosło zatrudnienie w regionie.",
            ),
            _entry(
                "wynagrodzenie",
                "noun",
                "Pieniądze wypłacane za wykonaną pracę.",
                "Warunki obejmują stałe wynagrodzenie.",
            ),
            _entry(
                "rekrutować",
                "verb",
                "Prowadzić proces poszukiwania i wyboru pracowników.",
                "Firma rekrutuje specjalistów do nowego zespołu.",
            ),
            _entry(
                "kwalifikacja",
                "noun",
                "Umiejętność lub formalne przygotowanie do określonego zadania.",
                "To stanowisko wymaga dodatkowych kwalifikacji.",
            ),
        ],
    ),
    VocabularySet(
        id="ocena-dowodow_b2",
        level="B2",
        topic="Dowody i ocena wiarygodności",
        unit_ref="b2-unit-5",
        words=[
            _entry(
                "przesłanka",
                "noun",
                "Informacja, na której opiera się wniosek lub rozumowanie.",
                "Wniosek wynika z kilku niezależnych przesłanek.",
            ),
            _entry(
                "potwierdzać",
                "verb",
                "Dostarczać dowodów na prawdziwość czegoś.",
                "Nowe dane potwierdzają wcześniejszą obserwację.",
            ),
            _entry(
                "ograniczenie",
                "noun",
                "Czynnik zmniejszający zakres lub siłę działania albo wniosku.",
                "Autorzy opisują ograniczenia badania.",
            ),
            _entry(
                "niejednoznaczny",
                "adjective",
                "Dopuszczający więcej niż jedną interpretację.",
                "Wynik pozostaje niejednoznaczny.",
            ),
        ],
    ),
    VocabularySet(
        id="klimat-i-energia_b2",
        level="B2",
        topic="Klimat i transformacja energetyczna",
        unit_ref="b2-unit-6",
        words=[
            _entry(
                "emisja",
                "noun",
                "Uwalnianie substancji lub energii do otoczenia.",
                "Transport odpowiada za część emisji w mieście.",
            ),
            _entry(
                "odnawialny",
                "adjective",
                "Taki, którego zasoby mogą być naturalnie uzupełniane.",
                "Region inwestuje w odnawialne źródła energii.",
            ),
            _entry(
                "ograniczać",
                "verb",
                "Zmniejszać zakres, liczbę lub intensywność czegoś.",
                "Nowe rozwiązanie ma ograniczać zużycie energii.",
            ),
            _entry(
                "zasób",
                "noun",
                "Dostępna ilość materiału, energii lub innego dobra.",
                "Woda jest cennym zasobem.",
            ),
        ],
    ),
    VocabularySet(
        id="redakcja-argumentacji_b2",
        level="B2",
        topic="Redagowanie i struktura argumentu",
        unit_ref="b2-unit-7",
        words=[
            _entry(
                "teza",
                "noun",
                "Główne twierdzenie, którego autor stara się dowieść.",
                "Teza artykułu pojawia się w pierwszym akapicie.",
            ),
            _entry(
                "kontrargument",
                "noun",
                "Argument przedstawiający racje przeciwne do tezy.",
                "Autorka omawia również kontrargument.",
            ),
            _entry(
                "wnioskować",
                "verb",
                "Wyprowadzać sąd na podstawie dostępnych informacji.",
                "Nie można wnioskować o przyczynie z samej korelacji.",
            ),
            _entry(
                "spójny",
                "adjective",
                "Logicznie powiązany i uporządkowany.",
                "Tekst zawiera spójny argument.",
            ),
        ],
    ),
]
