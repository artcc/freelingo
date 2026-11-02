"""Polish phrasebook — B2 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="argumentacja",
        level="B2",
        situation="Dyskusja i argumentacja",
        icon="\U0001f5e3\ufe0f",
        phrases=[
            PhrasebookEntry(
                text="Chciałbym przedstawić trzy argumenty na poparcie tej tezy.",
                context="Otwarcie własnego wystąpienia w dyskusji",
                register="formal",
            ),
            PhrasebookEntry(
                text="Rozumiem pani wątpliwości, ale pozwolę sobie mieć inne zdanie.",
                context="Kulturalne wyrażenie sprzeciwu wobec rozmówcy",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy mógłby pan rozwinąć ten wątek? Nie widzę, skąd płynie wniosek.",
                context="Prośba o uzasadnienie przedstawionego wniosku",
                register="formal",
            ),
            PhrasebookEntry(
                text="Zgadzam się z pierwszą częścią pańskiej wypowiedzi, natomiast druga "
                "budzi moje zastrzeżenia.",
                context="Częściowa zgoda połączona z zastrzeżeniem",
                register="formal",
            ),
            PhrasebookEntry(
                text="To, co pan mówi, jest prawdą, o ile przyjmiemy, że popyt jest stały.",
                context="Warunkowa zgoda z argumentem rozmówcy",
                register="formal",
            ),
            PhrasebookEntry(
                text="Muszę przyznać, że ten kontrargument jest przekonujący.",
                context="Uznanie trafności argumentu przeciwnika",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Podsumowując, uważam, że korzyści przeważają nad kosztami.",
                context="Zamknięcie wystąpienia wnioskiem",
                register="formal",
            ),
            PhrasebookEntry(
                text="Ten przykład mnie nie przekonuje, bo pomija kontekst historyczny.",
                context="Odrzucenie argumentu przez wskazanie luki",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Czy dobrze rozumiem, że proponuje pani zmianę terminu, a nie zakresu prac?",
                context="Sprawdzanie znaczenia propozycji przed zajęciem stanowiska",
                register="formal",
                unit_ref="b2-unit-1",
            ),
            PhrasebookEntry(
                text="Warto odróżnić to, co wiemy, od tego, czego się tylko domyślamy.",
                context="Porządkowanie faktów i przypuszczeń w dyskusji",
                register="neutral",
                unit_ref="b2-unit-1",
            ),
            PhrasebookEntry(
                text="Nie wykluczam takiej możliwości, ale potrzebuję więcej danych.",
                context="Ostrożna reakcja na niepotwierdzone wyjaśnienie",
                register="neutral",
                unit_ref="b2-unit-1",
            ),
            PhrasebookEntry(
                text="Jakie warunki musiałyby zostać spełnione, żeby zmienił pan zdanie?",
                context="Szukanie punktu wyjścia do porozumienia",
                register="formal",
                unit_ref="b2-unit-1",
            ),
            PhrasebookEntry(
                text="Zamiast rozstrzygać to teraz, proponuję porównać oba rozwiązania w praktyce.",
                context="Propozycja sprawdzenia spornych pomysłów",
                register="neutral",
                unit_ref="b2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="praca_gospodarka",
        level="B2",
        situation="Praca i gospodarka",
        icon="\U0001f4c8",
        phrases=[
            PhrasebookEntry(
                text="Chciałbym poznać zakres obowiązków na tym stanowisku.",
                context="Pytanie o zadania związane z oferowaną pracą",
                register="formal",
            ),
            PhrasebookEntry(
                text="Jakie są warunki zatrudnienia i wysokość wynagrodzenia?",
                context="Pytanie o warunki proponowanej pracy",
                register="formal",
            ),
            PhrasebookEntry(
                text="Do moich obowiązków należało prowadzenie dokumentacji projektowej.",
                context="Opis wcześniejszych zadań zawodowych",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy moglibyśmy omówić zakres współpracy na przyszły kwartał?",
                context="Propozycja ustalenia warunków współpracy",
                register="formal",
            ),
            PhrasebookEntry(
                text="W związku z rosnącą inflacją musimy zrewidować budżet.",
                context="Uzasadnienie zmiany planu finansowego",
                register="formal",
            ),
            PhrasebookEntry(
                text="Nasza firma odnotowała wzrost przychodów o osiem procent.",
                context="Przedstawienie wyniku finansowego firmy",
                register="formal",
            ),
            PhrasebookEntry(
                text="Rynek pracy zmienia się szybciej, niż przewidywały prognozy.",
                context="Komentarz do sytuacji na rynku zatrudnienia",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Podpisaliśmy umowę na czas nieokreślony.",
                context="Potwierdzenie zawarcia stałej umowy o pracę",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Proszę o doprecyzowanie, kto odpowiada za zatwierdzenie końcowej wersji.",
                context="Ustalanie odpowiedzialności w projekcie",
                register="formal",
                unit_ref="b2-unit-2",
            ),
            PhrasebookEntry(
                text="Przy obecnym obciążeniu zespołu nie możemy zagwarantować tego terminu.",
                context="Wyjaśnienie ograniczeń przy planowaniu pracy",
                register="formal",
                unit_ref="b2-unit-2",
            ),
            PhrasebookEntry(
                text="Czy podana kwota obejmuje podatek i wszystkie dodatkowe opłaty?",
                context="Weryfikacja całkowitego kosztu oferty",
                register="neutral",
                unit_ref="b2-unit-2",
            ),
            PhrasebookEntry(
                text="Proponuję rozłożyć płatność na dwie raty powiązane z etapami projektu.",
                context="Negocjowanie harmonogramu rozliczeń",
                register="formal",
                unit_ref="b2-unit-2",
            ),
            PhrasebookEntry(
                text="Po spotkaniu prześlę podsumowanie ustaleń do potwierdzenia.",
                context="Zapowiedź pisemnego utrwalenia uzgodnień",
                register="formal",
                unit_ref="b2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="nauka",
        level="B2",
        situation="Nauka i badania",
        icon="\U0001f52c",
        phrases=[
            PhrasebookEntry(
                text="Badania przeprowadzone w 2025 roku potwierdziły wstępną hipotezę.",
                context="Przywołanie wyniku opublikowanego badania",
                register="formal",
            ),
            PhrasebookEntry(
                text="Wyniki trzeba interpretować ostrożnie ze względu na małą próbę.",
                context="Zastrzeżenie metodologiczne do wyników",
                register="formal",
            ),
            PhrasebookEntry(
                text="Jakie metody zastosowano w tym eksperymencie?",
                context="Pytanie o metodologię badania",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy dane są dostępne w otwartym repozytorium?",
                context="Pytanie o dostęp do danych źródłowych",
                register="formal",
            ),
            PhrasebookEntry(
                text="Autor nie podaje źródła tej statystyki.",
                context="Wskazanie brakującego przypisu w tekście",
                register="neutral",
            ),
            PhrasebookEntry(
                text="To badanie nie zostało poddane recenzji.",
                context="Ocena wiarygodności publikacji",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Wniosek wykracza poza to, co pokazują wyniki.",
                context="Krytyka nadinterpretacji danych",
                register="formal",
            ),
            PhrasebookEntry(
                text="Chciałbym zgłosić uwagi do metodologii badania.",
                context="Zabranie głosu w dyskusji naukowej",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy możemy porównać te wyniki, skoro zastosowano różne metody pomiaru?",
                context="Sprawdzanie porównywalności dwóch badań",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="Proszę wyjaśnić, według jakich kryteriów wybrano uczestników.",
                context="Pytanie o sposób doboru próby",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="W prezentacji brakuje informacji o ograniczeniach tej metody.",
                context="Zwrócenie uwagi na niepełny opis badania",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="To możliwe wyjaśnienie, ale nie jedyne zgodne z uzyskanymi danymi.",
                context="Wskazanie alternatywnych interpretacji wyników",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="Czy mógłby pan przesłać pełny opis procedury, abyśmy mogli "
                "powtórzyć analizę?",
                context="Prośba o materiały potrzebne do sprawdzenia analizy",
                register="formal",
                unit_ref="b2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        id="podroze_miedzynarodowe",
        level="B2",
        situation="Podróże międzynarodowe",
        icon="\u2708\ufe0f",
        phrases=[
            PhrasebookEntry(
                text="Czy ten bilet obejmuje bagaż podręczny?",
                context="Pytanie o zakres biletu lotniczego",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Gdzie odbędzie się odprawa paszportowa?",
                context="Szukanie miejsca kontroli granicznej",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Mam przesiadkę w Monachium i półtorej godziny na zmianę samolotu.",
                context="Opis połączenia z przesiadką",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Czy mogę prosić o potwierdzenie rezerwacji na piśmie?",
                context="Prośba o dokument potwierdzający rezerwację",
                register="formal",
            ),
            PhrasebookEntry(
                text="Z powodu odwołania lotu utraciłem połączenie.",
                context="Zgłoszenie problemu po odwołanym locie",
                register="formal",
            ),
            PhrasebookEntry(
                text="Chciałbym zgłosić reklamację dotyczącą zagubionego bagażu.",
                context="Reklamacja w punkcie obsługi bagażu",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy w tym kraju honorowana jest europejska karta ubezpieczenia zdrowotnego?",
                context="Pytanie o dostęp do opieki medycznej za granicą",
                register="formal",
            ),
            PhrasebookEntry(
                text="Muszę przedłużyć wizę o kolejne trzydzieści dni.",
                context="Wniosek o przedłużenie pobytu w urzędzie",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy mogą Państwo zaproponować inne połączenie bez dodatkowych kosztów?",
                context="Szukanie rozwiązania po odwołaniu lotu",
                register="formal",
                unit_ref="b2-unit-6",
            ),
            PhrasebookEntry(
                text="Proszę o pisemne potwierdzenie przyczyny opóźnienia.",
                context="Uzyskiwanie dokumentu potrzebnego do reklamacji",
                register="formal",
                unit_ref="b2-unit-6",
            ),
            PhrasebookEntry(
                text="Zarezerwowany pokój miał być przystosowany do potrzeb osoby na wózku.",
                context="Zgłaszanie niezgodności warunków noclegu z rezerwacją",
                register="neutral",
                unit_ref="b2-unit-6",
            ),
            PhrasebookEntry(
                text="Jakie dokumenty należy dołączyć do wniosku o zwrot kosztów?",
                context="Ustalanie wymaganych załączników do reklamacji",
                register="formal",
                unit_ref="b2-unit-6",
            ),
            PhrasebookEntry(
                text="Nie chcę naruszyć miejscowych zwyczajów. Czy obowiązują tu zasady ubioru?",
                context="Pytanie przed wejściem do miejsca o znaczeniu religijnym lub kulturowym",
                register="neutral",
                unit_ref="b2-unit-6",
            ),
        ],
    ),
]
