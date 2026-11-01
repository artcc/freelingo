"""Polish phrasebook — C2 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="styl",
        level="C2",
        situation="Rejestr i styl",
        icon="\U0001f58b\ufe0f",
        phrases=[
            PhrasebookEntry(
                text="Niniejszym potwierdzam przyjęcie warunków przedstawionych w ofercie.",
                context="Odpowiedź na ofertę w korespondencji służbowej",
                register="formal",
                unit_ref="c2-unit-1",
            ),
            PhrasebookEntry(
                text="Uprzejmie proszę o ustosunkowanie się do uwag zawartych w recenzji.",
                context="Zwrot do autora lub wykonawcy w trybie oficjalnym",
                register="formal",
                unit_ref="c2-unit-1",
            ),
            PhrasebookEntry(
                text="Pozwalam sobie zauważyć, że proponowane rozwiązanie budzi zastrzeżenia "
                "natury prawnej.",
                context="Komentarz krytyczny w tonie ceremonialnym",
                register="formal",
                unit_ref="c2-unit-1",
            ),
            PhrasebookEntry(
                text="Nie chciałbym, żeby to zabrzmiało jak zarzut, ale ta wersja wymaga "
                "jeszcze pracy.",
                context="Łagodzenie krytyki w rozmowie zawodowej",
                register="neutral",
                unit_ref="c2-unit-1",
            ),
            PhrasebookEntry(
                text="Mówiąc wprost: to nie zadziała i wszyscy o tym wiemy.",
                context="Stawianie sprawy jasno w zespole",
                register="neutral",
                unit_ref="c2-unit-1",
            ),
            PhrasebookEntry(
                text="Mam wrażenie, że mówimy o dwóch różnych rzeczach i warto to nazwać.",
                context="Sygnalizowanie nieporozumienia w dyskusji",
                register="neutral",
                unit_ref="c2-unit-1",
            ),
            PhrasebookEntry(
                text="Daj znać, czy ogarniamy temat do piątku, bo muszę coś wpisać w grafik.",
                context="Ustalenie terminu w nieoficjalnej wiadomości",
                register="informal",
                unit_ref="c2-unit-1",
            ),
            PhrasebookEntry(
                text="No dobra, skoro tak stawiasz sprawę, to nie mam więcej pytań.",
                context="Zamknięcie dyskusji w swobodnej rozmowie",
                register="informal",
                unit_ref="c2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="frazeologia",
        level="C2",
        situation="Frazeologia i przysłowia",
        icon="\U0001f4d6",
        phrases=[
            PhrasebookEntry(
                text="Rzucasz grochem o ścianę — on i tak zrobi po swojemu.",
                context="Bezskuteczne przekonywanie kogoś",
                register="informal",
                unit_ref="c2-unit-2",
            ),
            PhrasebookEntry(
                text="Nie ma dymu bez ognia, ale w tej sprawie dymu jest więcej niż ognia.",
                context="Ostrożne komentowanie plotki",
                register="neutral",
                unit_ref="c2-unit-2",
            ),
            PhrasebookEntry(
                text="Jak sobie pościelesz, tak się wyśpisz — nikt tego nie odrobi za ciebie.",
                context="Przypomnienie o konsekwencjach własnych decyzji",
                register="neutral",
                unit_ref="c2-unit-2",
            ),
            PhrasebookEntry(
                text="Gdzie kucharek sześć, tam nie ma co jeść, więc wyznaczmy jedną osobę "
                "odpowiedzialną.",
                context="Wskazywanie skutków rozproszonej odpowiedzialności",
                register="neutral",
                unit_ref="c2-unit-2",
            ),
            PhrasebookEntry(
                text="Muszę przyznać, że wyciągnął do nas pomocną dłoń w najgorszym momencie.",
                context="Docenienie czyjejś pomocy",
                register="neutral",
                unit_ref="c2-unit-2",
            ),
            PhrasebookEntry(
                text="Nie krusz kopii o drobiazg, zachowaj siły na sprawy, które naprawdę ważą.",
                context="Odradzanie jałowego sporu",
                register="neutral",
                unit_ref="c2-unit-2",
            ),
            PhrasebookEntry(
                text="W końcu wyszedł z siebie i powiedział, co myśli.",
                context="Reakcja po długim tłumieniu irytacji",
                register="neutral",
                unit_ref="c2-unit-2",
            ),
            PhrasebookEntry(
                text="Mieć muchy w nosie to u niego stan permanentny, więc nie bierz tego "
                "do siebie.",
                context="Usprawiedliwienie czyjegoś złego humoru",
                register="informal",
                unit_ref="c2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="prawo_nauka",
        level="C2",
        situation="Prawo i nauka",
        icon="\U0001f4dc",
        phrases=[
            PhrasebookEntry(
                text="Zgodnie z § 4 ust. 2 umowy wypowiedzenie wymaga formy pisemnej "
                "pod rygorem nieważności.",
                context="Przywołanie postanowienia umowy",
                register="formal",
                unit_ref="c2-unit-4",
            ),
            PhrasebookEntry(
                text="W rozumieniu niniejszej umowy „dzień roboczy” oznacza dzień "
                "od poniedziałku do piątku.",
                context="Definiowanie pojęcia w tekście umowy",
                register="formal",
                unit_ref="c2-unit-4",
            ),
            PhrasebookEntry(
                text="Z zastrzeżeniem ust. 3, termin uważa się za zachowany, jeżeli przesyłkę "
                "nadano przed jego upływem.",
                context="Warunek i domniemanie w klauzuli umownej",
                register="formal",
                unit_ref="c2-unit-4",
            ),
            PhrasebookEntry(
                text="Wnoszę o udzielenie mi urlopu wypoczynkowego w dniach 12–16 maja.",
                context="Wniosek urlopowy w formie pisemnej",
                register="formal",
                unit_ref="c2-unit-4",
            ),
            PhrasebookEntry(
                text="Uzyskane dane sugerują zależność nieliniową, lecz jej nie dowodzą.",
                context="Ostrożny wniosek z wyników badania",
                register="formal",
                unit_ref="c2-unit-4",
            ),
            PhrasebookEntry(
                text="Niniejsze badanie ma charakter pilotażowy; jego wyniki wymagają "
                "replikacji.",
                context="Zastrzeżenie w abstrakcie artykułu",
                register="formal",
                unit_ref="c2-unit-4",
            ),
            PhrasebookEntry(
                text="W literaturze przedmiotu dominuje stanowisko, zgodnie z którym efekt "
                "wynika z doboru próby.",
                context="Wprowadzenie przeglądu literatury",
                register="formal",
                unit_ref="c2-unit-4",
            ),
            PhrasebookEntry(
                text="Próba liczyła 412 respondentów dobranych losowo, co pozwala ograniczyć "
                "błąd doboru.",
                context="Opis metodologii badania",
                register="formal",
                unit_ref="c2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        id="debata",
        level="C2",
        situation="Debata i perswazja",
        icon="\U0001f3db\ufe0f",
        phrases=[
            PhrasebookEntry(
                text="Zanim przejdę do wniosków, chciałbym ustalić, co dokładnie jest "
                "przedmiotem sporu.",
                context="Otwarcie debaty i porządkowanie tezy",
                register="formal",
                unit_ref="c2-unit-5",
            ),
            PhrasebookEntry(
                text="Przyjmuję ten zarzut w części dotyczącej kosztów, ale nie w części "
                "dotyczącej terminu.",
                context="Koncesja i częściowe odparcie zarzutu",
                register="formal",
                unit_ref="c2-unit-5",
            ),
            PhrasebookEntry(
                text="Teza przeciwnika opiera się na założeniu, którego nikt tu nie uzasadnił.",
                context="Wskazanie nieuzasadnionej przesłanki",
                register="formal",
                unit_ref="c2-unit-5",
            ),
            PhrasebookEntry(
                text="To, że coś jest droższe, nie znaczy jeszcze, że jest gorsze.",
                context="Odpieranie argumentu z kosztu",
                register="formal",
                unit_ref="c2-unit-5",
            ),
            PhrasebookEntry(
                text="Czy naprawdę chcemy rozstrzygać tę sprawę w pośpiechu, bez danych?",
                context="Pytanie retoryczne wobec presji czasu",
                register="formal",
                unit_ref="c2-unit-5",
            ),
            PhrasebookEntry(
                text="Proszę wskazać, które procedury znosimy i jakie ryzyko przejmujemy "
                "w zamian.",
                context="Żądanie doprecyzowania wniosku",
                register="formal",
                unit_ref="c2-unit-5",
            ),
            PhrasebookEntry(
                text="Rozumiem emocje, ale wróćmy do liczb, bo na nich opiera się decyzja.",
                context="Chłodzenie sporu i powrót do danych",
                register="neutral",
                unit_ref="c2-unit-5",
            ),
            PhrasebookEntry(
                text="Nie przekonałeś mnie, ale przyznaję, że postawiłeś problem w nowym "
                "świetle.",
                context="Zamknięcie wymiany z uznaniem argumentu",
                register="neutral",
                unit_ref="c2-unit-5",
            ),
        ],
    ),
]
