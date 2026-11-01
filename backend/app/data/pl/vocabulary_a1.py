"""A1 vocabulary sets."""

from app.data._types import PartOfSpeech, VocabularyEntry, VocabularySet


def _entry(word: str, pos: PartOfSpeech, definition: str, example: str) -> VocabularyEntry:
    return VocabularyEntry(word=word, pos=pos, definition=definition, example=example)


A1_SETS: list[VocabularySet] = [
    VocabularySet(
        id="dane_osobowe_a1",
        level="A1",
        topic="Dane osobowe i przedstawianie się",
        unit_ref="a1-unit-1",
        words=[
            _entry(
                "imię",
                "noun",
                "Nazwa, której używa się, zwracając się do osoby.",
                "Mam na imię Marta.",
            ),
            _entry(
                "nazwisko",
                "noun",
                "Rodzinne określenie identyfikujące osobę.",
                "Moje nazwisko jest krótkie.",
            ),
            _entry(
                "mieszkać",
                "verb",
                "Przebywać na stałe w określonym miejscu.",
                "Mieszkam w Krakowie.",
            ),
            _entry(
                "student",
                "noun",
                "Osoba ucząca się na uczelni.",
                "Mój brat jest studentem.",
            ),
        ],
    ),
    VocabularySet(
        id="codziennosc_a1",
        level="A1",
        topic="Codzienne czynności",
        unit_ref="a1-unit-2",
        words=[
            _entry(
                "wstawać",
                "verb",
                "Podnosić się z łóżka po odpoczynku.",
                "Wstaję o siódmej rano.",
            ),
            _entry(
                "śniadanie",
                "noun",
                "Pierwszy posiłek jedzony zwykle rano.",
                "Jemy śniadanie w kuchni.",
            ),
            _entry(
                "pracować",
                "verb",
                "Wykonywać obowiązki zawodowe.",
                "Pracuję od poniedziałku do piątku.",
            ),
            _entry(
                "odpoczywać",
                "verb",
                "Odzyskiwać siły po wysiłku.",
                "Wieczorem odpoczywam przy książce.",
            ),
        ],
    ),
    VocabularySet(
        id="dom_i_miasto_a1",
        level="A1",
        topic="Dom i miasto",
        unit_ref="a1-unit-3",
        words=[
            _entry(
                "mieszkanie",
                "noun",
                "Lokal przeznaczony do zamieszkania.",
                "Nasze mieszkanie ma dwa pokoje.",
            ),
            _entry(
                "kuchnia",
                "noun",
                "Pomieszczenie służące do przygotowywania posiłków.",
                "W kuchni stoi duży stół.",
            ),
            _entry(
                "przystanek",
                "noun",
                "Miejsce, w którym zatrzymuje się autobus lub tramwaj.",
                "Przystanek jest obok biblioteki.",
            ),
            _entry(
                "ulica",
                "noun",
                "Droga w mieście z budynkami po obu stronach.",
                "Ta ulica prowadzi do centrum.",
            ),
        ],
    ),
    VocabularySet(
        id="liczby_czas_a1",
        level="A1",
        topic="Liczby, czas i kalendarz",
        unit_ref="a1-unit-4",
        words=[
            _entry(
                "dzisiaj",
                "adverb",
                "W dniu, w którym odbywa się rozmowa.",
                "Dzisiaj mam lekcję polskiego.",
            ),
            _entry(
                "jutro",
                "adverb",
                "W dniu następującym po dzisiejszym.",
                "Jutro pracuję od ósmej.",
            ),
            _entry(
                "poniedziałek",
                "noun",
                "Pierwszy dzień roboczy tygodnia.",
                "W poniedziałek zaczynam nowy kurs.",
            ),
            _entry(
                "godzina",
                "noun",
                "Jednostka czasu równa sześćdziesięciu minutom.",
                "Jest godzina dziewiąta.",
            ),
        ],
    ),
    VocabularySet(
        id="rodzina_a1",
        level="A1",
        topic="Rodzina i opisy osób",
        unit_ref="a1-unit-5",
        words=[
            _entry(
                "rodzeństwo",
                "noun",
                "Bracia i siostry danej osoby.",
                "Mam dwoje rodzeństwa.",
            ),
            _entry(
                "kuzyn",
                "noun",
                "Syn cioci lub wujka.",
                "Mój kuzyn mieszka w Łodzi.",
            ),
            _entry(
                "wysoki",
                "adjective",
                "Mający wzrost większy niż przeciętny.",
                "Moja siostra jest wysoka.",
            ),
            _entry(
                "życzliwy",
                "adjective",
                "Okazujący innym sympatię i pomoc.",
                "Nasz sąsiad jest bardzo życzliwy.",
            ),
        ],
    ),
    VocabularySet(
        id="jedzenie_a1",
        level="A1",
        topic="Jedzenie i zamawianie",
        unit_ref="a1-unit-6",
        words=[
            _entry(
                "śniadanie",
                "noun",
                "Posiłek jedzony zwykle na początku dnia.",
                "Na śniadanie jem owsiankę.",
            ),
            _entry(
                "warzywo",
                "noun",
                "Roślina lub jej część używana jako jedzenie.",
                "Do zupy dodaję świeże warzywa.",
            ),
            _entry(
                "zamawiać",
                "verb",
                "Prosić o przygotowanie lub podanie wybranej rzeczy.",
                "Zamawiam herbatę i kanapkę.",
            ),
            _entry(
                "smaczny",
                "adjective",
                "Mający przyjemny smak.",
                "Ta zupa jest bardzo smaczna.",
            ),
        ],
    ),
    VocabularySet(
        id="szkola_a1",
        level="A1",
        topic="Szkoła i nauka języka",
        unit_ref="a1-unit-7",
        words=[
            _entry(
                "zeszyt",
                "noun",
                "Zbiór kartek służący do pisania notatek.",
                "Zapisuję nowe słowa w zeszycie.",
            ),
            _entry(
                "pytanie",
                "noun",
                "Wypowiedź, która prosi o informację.",
                "Mam pytanie do nauczyciela.",
            ),
            _entry(
                "powtarzać",
                "verb",
                "Mówić lub robić coś ponownie, aby lepiej zapamiętać.",
                "Powtarzam trudne słowa.",
            ),
            _entry(
                "rozumieć",
                "verb",
                "Wiedzieć, co coś znaczy.",
                "Rozumiem krótkie zdania po polsku.",
            ),
        ],
    ),
    VocabularySet(
        id="powtorka_a1",
        level="A1",
        topic="Powtórka: podstawowe sytuacje",
        unit_ref="a1-unit-8",
        words=[
            _entry(
                "przedstawiać się",
                "verb",
                "Podawać komuś swoje imię lub podstawowe informacje.",
                "Przedstawiam się nowej koleżance.",
            ),
            _entry(
                "codziennie",
                "adverb",
                "Każdego dnia.",
                "Codziennie czytam kilka stron.",
            ),
            _entry(
                "blisko",
                "adverb",
                "W małej odległości od czegoś.",
                "Mieszkam blisko przystanku.",
            ),
            _entry(
                "ulubiony",
                "adjective",
                "Szczególnie lubiany spośród innych.",
                "Moim ulubionym napojem jest woda.",
            ),
        ],
    ),
    VocabularySet(
        id="ubrania_a1",
        level="A1",
        topic="Ubrania i kolory",
        unit_ref="a1-unit-5",
        words=[
            _entry(
                "koszula",
                "noun",
                "Ubranie noszone na górnej części ciała, zwykle zapinane z przodu.",
                "Na spotkanie zakładam białą koszulę.",
            ),
            _entry(
                "spodnie",
                "noun",
                "Ubranie zakrywające nogi, zwykle z dwiema nogawkami.",
                "Moje czarne spodnie są wygodne.",
            ),
            _entry("buty", "noun", "Obuwie noszone na stopach.", "Nowe buty stoją przy drzwiach."),
            _entry(
                "czerwony",
                "adjective",
                "Mający barwę krwi lub dojrzałego pomidora.",
                "Ona ma czerwony szalik.",
            ),
        ],
    ),
    VocabularySet(
        id="transport_a1",
        level="A1",
        topic="Transport i droga do pracy",
        unit_ref="a1-unit-3",
        words=[
            _entry(
                "autobus",
                "noun",
                "Duży pojazd przewożący pasażerów po drogach.",
                "Autobus zatrzymuje się przed szkołą.",
            ),
            _entry(
                "tramwaj",
                "noun",
                "Pojazd szynowy poruszający się po ulicach miasta.",
                "Jadę tramwajem do centrum.",
            ),
            _entry(
                "bilet",
                "noun",
                "Dokument uprawniający do przejazdu lub wejścia.",
                "Kupuję bilet w automacie.",
            ),
            _entry(
                "jechać",
                "verb",
                "Przemieszczać się pojazdem w określonym kierunku.",
                "Jedziemy pociągiem do Poznania.",
            ),
        ],
    ),
    VocabularySet(
        id="pogoda_a1",
        level="A1",
        topic="Pogoda i pory roku",
        unit_ref="a1-unit-7",
        words=[
            _entry(
                "słońce",
                "noun",
                "Gwiazda, której światło i ciepło docierają do Ziemi.",
                "Dzisiaj świeci słońce.",
            ),
            _entry(
                "deszcz",
                "noun",
                "Woda spadająca z chmur w postaci kropli.",
                "Po południu będzie deszcz.",
            ),
            _entry("zimny", "adjective", "Mający niską temperaturę.", "Rano jest zimno."),
            _entry(
                "zima",
                "noun",
                "Pora roku po jesieni i przed wiosną.",
                "Zimą często noszę ciepły płaszcz.",
            ),
        ],
    ),
    VocabularySet(
        id="kawiarnia_a1",
        level="A1",
        topic="W kawiarni",
        unit_ref="a1-unit-6",
        words=[
            _entry(
                "kawa",
                "noun",
                "Napój przygotowywany z prażonych ziaren kawowca.",
                "Poproszę kawę z mlekiem.",
            ),
            _entry(
                "herbata",
                "noun",
                "Napój przygotowywany z liści herbaty.",
                "Czy mają państwo zieloną herbatę?",
            ),
            _entry(
                "menu",
                "noun",
                "Lista potraw i napojów dostępnych w lokalu.",
                "Czy mogę prosić o menu?",
            ),
            _entry(
                "rachunek",
                "noun",
                "Dokument z kwotą do zapłaty za usługę lub zakup.",
                "Proszę o rachunek.",
            ),
        ],
    ),
    VocabularySet(
        id="przedmioty-szkolne_a1",
        level="A1",
        topic="Przedmioty szkolne",
        unit_ref="a1-unit-7",
        words=[
            _entry(
                "zeszyt",
                "noun",
                "Zbiór kartek służący do pisania lub robienia notatek.",
                "Zapisuję nowe słowa w zeszycie.",
            ),
            _entry("długopis", "noun", "Przyrząd do pisania z tuszem.", "Mam niebieski długopis."),
            _entry(
                "tablica",
                "noun",
                "Duża powierzchnia do pisania lub wyświetlania informacji.",
                "Nauczyciel pisze nowe zdanie na tablicy.",
            ),
            _entry(
                "pytanie",
                "noun",
                "Wypowiedź, która prosi o informację lub odpowiedź.",
                "Mam pytanie do nauczyciela.",
            ),
        ],
    ),
    VocabularySet(
        id="miejsca-w-miescie_a1",
        level="A1",
        topic="Miejsca w mieście",
        unit_ref="a1-unit-3",
        words=[
            _entry(
                "apteka",
                "noun",
                "Miejsce, w którym można kupić leki.",
                "Apteka jest obok przychodni.",
            ),
            _entry(
                "dworzec",
                "noun",
                "Budynek lub teren, z którego odjeżdżają pociągi albo autobusy.",
                "Spotykamy się przed dworcem.",
            ),
            _entry(
                "park",
                "noun",
                "Publiczny teren z zielenią, przeznaczony do odpoczynku i spacerów.",
                "W niedzielę spacerujemy po parku.",
            ),
            _entry(
                "skrzyżowanie",
                "noun",
                "Miejsce, w którym przecinają się drogi lub ulice.",
                "Skręć w prawo na następnym skrzyżowaniu.",
            ),
        ],
    ),
]
