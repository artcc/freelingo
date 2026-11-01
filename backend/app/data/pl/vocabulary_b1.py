"""B1 vocabulary sets."""

from app.data._types import PartOfSpeech, VocabularyEntry, VocabularySet


def _entry(word: str, pos: PartOfSpeech, definition: str, example: str) -> VocabularyEntry:
    return VocabularyEntry(word=word, pos=pos, definition=definition, example=example)


B1_SETS: list[VocabularySet] = [
    VocabularySet(
        id="opowiesci_b1",
        level="B1",
        topic="Opowiadanie i narracja",
        unit_ref="b1-unit-1",
        words=[
            _entry(
                "przypadkiem",
                "adverb",
                "Nieplanowanie i bez zamiaru.",
                "Przypadkiem spotkałem dawną nauczycielkę.",
            ),
            _entry(
                "wspominać",
                "verb",
                "Przywoływać coś w pamięci lub w rozmowie.",
                "Często wspomina wakacje nad morzem.",
            ),
            _entry(
                "zakończyć",
                "verb",
                "Doprowadzić działanie do końca.",
                "Zakończyliśmy projekt przed terminem.",
            ),
            _entry(
                "nagle",
                "adverb",
                "Szybko i niespodziewanie.",
                "Nagle zgasło światło.",
            ),
        ],
    ),
    VocabularySet(
        id="opinie_b1",
        level="B1",
        topic="Opinie i argumenty",
        unit_ref="b1-unit-2",
        words=[
            _entry(
                "stanowisko",
                "noun",
                "Pogląd lub sposób podejścia do sprawy.",
                "Przedstawiła swoje stanowisko na spotkaniu.",
            ),
            _entry(
                "uzasadniać",
                "verb",
                "Podawać powody popierające opinię.",
                "Autor uzasadnia wniosek przykładami.",
            ),
            _entry(
                "z kolei",
                "phrase",
                "Wyrażenie wprowadzające kontrast lub kolejny punkt.",
                "Marta lubi góry, z kolei Adam woli morze.",
            ),
            _entry(
                "wniosek",
                "noun",
                "Myśl wynikająca z rozważenia informacji.",
                "Z tych danych wynika prosty wniosek.",
            ),
        ],
    ),
    VocabularySet(
        id="praca_i_nauka_b1",
        level="B1",
        topic="Praca i edukacja",
        unit_ref="b1-unit-3",
        words=[
            _entry(
                "doświadczenie",
                "noun",
                "Wiedza i umiejętności zdobyte w praktyce.",
                "Mam doświadczenie w pracy z klientami.",
            ),
            _entry(
                "umiejętność",
                "noun",
                "Zdolność do wykonywania określonej czynności.",
                "Komunikacja to ważna umiejętność.",
            ),
            _entry(
                "staż",
                "noun",
                "Czasowa praktyka zawodowa służąca zdobyciu doświadczenia.",
                "Latem odbywała staż w redakcji.",
            ),
            _entry(
                "rekrutacja",
                "noun",
                "Proces wyboru osoby do pracy lub innej roli.",
                "Rekrutacja zakończy się w przyszłym tygodniu.",
            ),
        ],
    ),
    VocabularySet(
        id="podroze_b1",
        level="B1",
        topic="Podróże i doświadczenia",
        unit_ref="b1-unit-4",
        words=[
            _entry(
                "opóźnienie",
                "noun",
                "Sytuacja, w której coś odbywa się później niż planowano.",
                "Z powodu opóźnienia przegapiłem autobus.",
            ),
            _entry(
                "zakwaterowanie",
                "noun",
                "Miejsce zapewniające nocleg podczas pobytu.",
                "Zakwaterowanie było blisko centrum.",
            ),
            _entry(
                "zwiedzać",
                "verb",
                "Oglądać interesujące miejsca lub zabytki.",
                "Podczas urlopu zwiedzaliśmy stare miasto.",
            ),
            _entry(
                "wrażenie",
                "noun",
                "Odczucie lub opinia powstałe po kontakcie z czymś.",
                "Największe wrażenie zrobiły na mnie góry.",
            ),
        ],
    ),
    VocabularySet(
        id="relacje_b1",
        level="B1",
        topic="Relacje i komunikacja",
        unit_ref="b1-unit-5",
        words=[
            _entry(
                "nieporozumienie",
                "noun",
                "Błędne zrozumienie czyichś słów lub zamiarów.",
                "Wyjaśniliśmy nieporozumienie podczas rozmowy.",
            ),
            _entry(
                "zaufanie",
                "noun",
                "Przekonanie, że można na kimś polegać.",
                "Współpraca opiera się na zaufaniu.",
            ),
            _entry(
                "uzgadniać",
                "verb",
                "Wspólnie ustalać szczegóły lub wspólne stanowisko.",
                "Musimy uzgodnić termin spotkania.",
            ),
            _entry(
                "wspierać",
                "verb",
                "Pomagać komuś w trudnej sytuacji lub działaniu.",
                "Przyjaciele wspierali ją podczas studiów.",
            ),
        ],
    ),
    VocabularySet(
        id="spoleczenstwo_b1",
        level="B1",
        topic="Społeczność i życie publiczne",
        unit_ref="b1-unit-6",
        words=[
            _entry(
                "mieszkaniec",
                "noun",
                "Osoba mieszkająca w danej miejscowości lub regionie.",
                "Mieszkańcy rozmawiali o nowej drodze.",
            ),
            _entry(
                "wolontariat",
                "noun",
                "Dobrowolna praca na rzecz innych osób lub wspólnoty.",
                "W czasie studiów angażowała się w wolontariat.",
            ),
            _entry(
                "wniosek",
                "noun",
                "Formalna prośba skierowana do instytucji.",
                "Złożyłem wniosek o stypendium.",
            ),
            _entry(
                "uczestniczyć",
                "verb",
                "Brać udział w wydarzeniu lub działaniu.",
                "Uczestniczymy w zebraniu mieszkańców.",
            ),
        ],
    ),
    VocabularySet(
        id="kultura_b1",
        level="B1",
        topic="Kultura, edukacja i media",
        unit_ref="b1-unit-7",
        words=[
            _entry(
                "recenzja",
                "noun",
                "Tekst oceniający książkę, film lub inne dzieło.",
                "Przeczytałam recenzję nowego filmu.",
            ),
            _entry(
                "bohater",
                "noun",
                "Główna postać opowieści lub filmu.",
                "Bohater powieści podejmuje trudną decyzję.",
            ),
            _entry(
                "wydarzenie",
                "noun",
                "Zaplanowana lub ważna sytuacja, która się odbywa.",
                "W muzeum organizują wydarzenie dla rodzin.",
            ),
            _entry(
                "opisywać",
                "verb",
                "Przedstawiać słowami cechy lub przebieg czegoś.",
                "Autorka opisuje życie w małym mieście.",
            ),
        ],
    ),
    VocabularySet(
        id="powtorka_b1",
        level="B1",
        topic="Powtórka: samodzielna komunikacja",
        unit_ref="b1-unit-8",
        words=[
            _entry(
                "przebieg",
                "noun",
                "Sposób, w jaki coś rozwija się w czasie.",
                "Opisał przebieg całego spotkania.",
            ),
            _entry(
                "stanowisko",
                "noun",
                "Opinia lub sposób podejścia do danej sprawy.",
                "Przedstawiła swoje stanowisko spokojnie.",
            ),
            _entry(
                "zależnie",
                "adverb",
                "W sposób różniący się w zależności od warunków.",
                "Wybierz trasę zależnie od pogody.",
            ),
            _entry(
                "uzasadnienie",
                "noun",
                "Powód lub argument wyjaśniający decyzję.",
                "Proszę podać uzasadnienie swojej odpowiedzi.",
            ),
        ],
    ),
    VocabularySet(
        id="obowiazki-zawodowe_b1",
        level="B1",
        topic="Obowiązki i współpraca w pracy",
        unit_ref="b1-unit-3",
        words=[
            _entry(
                "obowiązek",
                "noun",
                "Zadanie lub działanie, które należy wykonać.",
                "Do moich obowiązków należy przygotowanie raportu.",
            ),
            _entry(
                "współpracować",
                "verb",
                "Pracować razem z innymi przy wspólnym zadaniu.",
                "Współpracujemy z zespołem z Krakowa.",
            ),
            _entry(
                "termin",
                "noun",
                "Ustalony czas wykonania zadania lub odbycia wydarzenia.",
                "Musimy dotrzymać terminu projektu.",
            ),
            _entry(
                "odpowiedzialny",
                "adjective",
                "Zobowiązany do wykonania zadania lub ponoszenia jego skutków.",
                "Kasia jest odpowiedzialna za kontakt z klientem.",
            ),
        ],
    ),
    VocabularySet(
        id="dyskusja-i-argumenty_b1",
        level="B1",
        topic="Dyskusja i uzasadnianie opinii",
        unit_ref="b1-unit-2",
        words=[
            _entry(
                "stanowisko",
                "noun",
                "Opinia lub sposób podejścia do określonej sprawy.",
                "Przedstawił swoje stanowisko podczas spotkania.",
            ),
            _entry(
                "uzasadniać",
                "verb",
                "Podawać powody potwierdzające opinię lub decyzję.",
                "Autorka uzasadnia swoją tezę przykładami.",
            ),
            _entry(
                "zgadzać się",
                "verb",
                "Podzielać czyjąś opinię lub przyjmować propozycję.",
                "Zgadzam się z tym argumentem.",
            ),
            _entry(
                "wątpliwość",
                "noun",
                "Brak pewności co do prawdziwości lub słuszności czegoś.",
                "Mam wątpliwości dotyczące tego wniosku.",
            ),
        ],
    ),
    VocabularySet(
        id="zdrowie-i-nawyki_b1",
        level="B1",
        topic="Zdrowie i codzienne nawyki",
        unit_ref="b1-unit-5",
        words=[
            _entry(
                "nawyk",
                "noun",
                "Czynność wykonywana regularnie, często bez zastanowienia.",
                "Codzienny spacer stał się moim dobrym nawykiem.",
            ),
            _entry(
                "zapobiegać",
                "verb",
                "Podejmować działania, aby nie dopuścić do czegoś.",
                "Regularny ruch może zapobiegać problemom zdrowotnym.",
            ),
            _entry(
                "objaw",
                "noun",
                "Zauważalny znak choroby lub innego stanu.",
                "Kaszel jest jednym z objawów przeziębienia.",
            ),
            _entry(
                "zalecenie",
                "noun",
                "Rada lub wskazówka dotycząca właściwego działania.",
                "Lekarz wyjaśnił najważniejsze zalecenia.",
            ),
        ],
    ),
    VocabularySet(
        id="podroze-i-zakwaterowanie_b1",
        level="B1",
        topic="Podróże i zakwaterowanie",
        unit_ref="b1-unit-4",
        words=[
            _entry(
                "zakwaterowanie",
                "noun",
                "Miejsce zapewniające nocleg podczas pobytu.",
                "Zakwaterowanie mamy blisko centrum.",
            ),
            _entry(
                "rezerwować",
                "verb",
                "Zamawiać lub zabezpieczać miejsce na określony termin.",
                "Rezerwujemy pokój na trzy noce.",
            ),
            _entry(
                "odwołany",
                "adjective",
                "Taki, który nie odbędzie się zgodnie z planem.",
                "Nasz lot został odwołany.",
            ),
            _entry(
                "przesiadać się",
                "verb",
                "Zmieniać pojazd lub połączenie w czasie podróży.",
                "W Warszawie przesiadamy się do autobusu.",
            ),
        ],
    ),
    VocabularySet(
        id="zycie-publiczne_b1",
        level="B1",
        topic="Społeczność i życie publiczne",
        unit_ref="b1-unit-6",
        words=[
            _entry(
                "mieszkaniec",
                "noun",
                "Osoba mieszkająca w określonym miejscu.",
                "Mieszkańcy miasta zebrali się na rynku.",
            ),
            _entry(
                "władze",
                "noun",
                "Osoby lub instytucje zarządzające państwem albo miejscem.",
                "Władze dzielnicy przedstawiły nowy plan.",
            ),
            _entry(
                "zgłaszać",
                "verb",
                "Przekazywać informację o sprawie lub problemie.",
                "Mieszkańcy mogą zgłaszać usterki przez internet.",
            ),
            _entry(
                "wydarzenie",
                "noun",
                "Sytuacja lub zorganizowana aktywność, która się odbywa.",
                "W bibliotece odbędzie się wydarzenie dla rodzin.",
            ),
        ],
    ),
    VocabularySet(
        id="media-i-informacja_b1",
        level="B1",
        topic="Media i weryfikowanie informacji",
        unit_ref="b1-unit-7",
        words=[
            _entry(
                "źródło",
                "noun",
                "Miejsce lub osoba, od której pochodzi informacja.",
                "Artykuł podaje źródło wykorzystanych danych.",
            ),
            _entry(
                "nagłówek",
                "noun",
                "Tytuł artykułu lub innego materiału prasowego.",
                "Nagłówek nie oddaje całej treści tekstu.",
            ),
            _entry(
                "sprawdzać",
                "verb",
                "Ustalać, czy coś jest poprawne lub prawdziwe.",
                "Przed udostępnieniem warto sprawdzać informacje.",
            ),
            _entry(
                "wiarygodny",
                "adjective",
                "Zasługujący na zaufanie ze względu na rzetelność.",
                "To wiarygodne źródło informacji.",
            ),
        ],
    ),
]
