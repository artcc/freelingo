"""Polish phrasebook — C1 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="dyskurs",
        level="C1",
        situation="Wystąpienia publiczne",
        icon="\U0001f3a4",
        phrases=[
            PhrasebookEntry(
                text="Szanowni Państwo, dziękuję za zaproszenie.",
                context="Otwarcie wystąpienia przed publicznością",
                register="formal",
            ),
            PhrasebookEntry(
                text="Chciałbym zwrócić Państwa uwagę na trzy kwestie.",
                context="Zapowiedź struktury wystąpienia",
                register="formal",
            ),
            PhrasebookEntry(
                text="Zacznę od danych, które pozwolą nakreślić skalę zjawiska.",
                context="Przejście do argumentacji opartej na danych",
                register="formal",
            ),
            PhrasebookEntry(
                text="Jak Państwo zapewne wiedzą, problem narasta od kilku lat.",
                context="Przywołanie wiedzy wspólnej odbiorców",
                register="formal",
            ),
            PhrasebookEntry(
                text="Pozwolę sobie na krótką dygresję.",
                context="Zapowiedź odejścia od głównego wątku",
                register="formal",
            ),
            PhrasebookEntry(
                text="Nie sposób pominąć faktu, że koszty ponoszą najsłabsi.",
                context="Podkreślenie konsekwencji społecznych",
                register="formal",
            ),
            PhrasebookEntry(
                text="Podsumowując, proponujemy trzy konkretne rozwiązania.",
                context="Zamknięcie wywodu wnioskami",
                register="formal",
            ),
            PhrasebookEntry(
                text="Dziękuję za uwagę; chętnie odpowiem na Państwa pytania.",
                context="Zakończenie wystąpienia i zaproszenie do pytań",
                register="formal",
            ),
            PhrasebookEntry(
                text="Doprecyzuję to stwierdzenie, ponieważ w obecnej formie może być mylące.",
                context="Korygowanie własnego sformułowania podczas wystąpienia",
                register="formal",
                unit_ref="c1-unit-1",
            ),
            PhrasebookEntry(
                text="To ważne pytanie, ale wykracza poza zakres danych, którymi dysponujemy.",
                context="Odpowiedź na pytanie bez nieuzasadnionego rozszerzania wniosków",
                register="formal",
                unit_ref="c1-unit-1",
            ),
            PhrasebookEntry(
                text="Pozwolę sobie dokończyć tę myśl, a następnie odniosę się do pani uwagi.",
                context="Uprzejme odzyskanie głosu po przerwaniu wypowiedzi",
                register="formal",
                unit_ref="c1-unit-1",
            ),
            PhrasebookEntry(
                text="Przywołuję ten przykład jako ilustrację problemu, nie jako dowód jego skali.",
                context="Określenie roli przykładu w argumentacji publicznej",
                register="formal",
                unit_ref="c1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="negocjacje",
        level="C1",
        situation="Negocjacje i współpraca",
        icon="\U0001f91d",
        phrases=[
            PhrasebookEntry(
                text="Proponuję, abyśmy ustalili porządek rozmowy.",
                context="Otwarcie negocjacji i uporządkowanie dyskusji",
                register="formal",
            ),
            PhrasebookEntry(
                text="Rozumiem Państwa stanowisko, ale chciałbym przedstawić nasze zastrzeżenia.",
                context="Wyrażenie zrozumienia i przejście do kontrargumentu",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy byliby Państwo skłonni rozważyć termin przesunięty o dwa tygodnie?",
                context="Zaproponowanie ustępstwa w kwestii terminu",
                register="formal",
            ),
            PhrasebookEntry(
                text="Nasza zgoda na budżet jest warunkowa: oczekujemy skrócenia harmonogramu.",
                context="Przedstawienie warunku brzegowego",
                register="formal",
            ),
            PhrasebookEntry(
                text="Proponuję kompromis: obniżymy cenę, jeśli zwiększycie wolumen zamówień.",
                context="Zaproponowanie wymiany ustępstw",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Pozwólcie Państwo, że wrócimy do punktu drugiego.",
                context="Powrót do nierozstrzygniętej kwestii",
                register="formal",
            ),
            PhrasebookEntry(
                text="Chciałbym upewnić się, że dobrze rozumiem Państwa intencje.",
                context="Weryfikacja stanowiska drugiej strony",
                register="formal",
            ),
            PhrasebookEntry(
                text="Jeśli nie dojdziemy do porozumienia, pozostaje nam mediacja.",
                context="Wskazanie alternatywy wobec impasu",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Możemy zaakceptować tę zmianę pod warunkiem zachowania pozostałych ustaleń.",
                context="Wyrażenie ograniczonej zgody na zmianę warunków współpracy",
                register="formal",
                unit_ref="c1-unit-6",
            ),
            PhrasebookEntry(
                text="Oddzielmy kwestie już uzgodnione od tych, które nadal wymagają "
                "rozstrzygnięcia.",
                context="Porządkowanie negocjacji w sytuacji impasu",
                register="formal",
                unit_ref="c1-unit-6",
            ),
            PhrasebookEntry(
                text="Czy ten zapis ma charakter wiążący, czy wyraża jedynie intencję stron?",
                context="Ustalanie znaczenia postanowienia przed podpisaniem porozumienia",
                register="formal",
                unit_ref="c1-unit-6",
            ),
            PhrasebookEntry(
                text="Proponuję krótką przerwę, aby każda ze stron mogła ocenić skutki "
                "tej propozycji.",
                context="Ograniczanie presji podczas trudnych negocjacji",
                register="formal",
                unit_ref="c1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        id="etyka",
        level="C1",
        situation="Dylematy etyczne",
        icon="\u2696\ufe0f",
        phrases=[
            PhrasebookEntry(
                text="Czy cel uświęca środki, jeśli koszt ponoszą osoby trzecie?",
                context="Postawienie dylematu etycznego",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Trzeba rozdzielić opis sytuacji od jej oceny moralnej.",
                context="Porządkowanie argumentacji etycznej",
                register="formal",
            ),
            PhrasebookEntry(
                text="Mam poważne wątpliwości, czy ta decyzja jest sprawiedliwa.",
                context="Wyrażenie wątpliwości natury moralnej",
                register="formal",
            ),
            PhrasebookEntry(
                text="Nie chcę naruszać czyjejś prywatności, nawet w imię skuteczności.",
                context="Zaznaczenie granicy etycznej",
                register="formal",
            ),
            PhrasebookEntry(
                text="Uważam, że mamy obowiązek poinformować o tym opinię publiczną.",
                context="Uzasadnienie obowiązku ujawnienia informacji",
                register="formal",
            ),
            PhrasebookEntry(
                text="Czy potrafimy uzasadnić ten wybór komuś, kto poniesie jego skutki?",
                context="Test uniwersalizacji decyzji",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Zgadzam się co do zasady, ale nie co do sposobu jej realizacji.",
                context="Rozdzielenie zgody na wartość i na metodę",
                register="formal",
            ),
            PhrasebookEntry(
                text="Musimy ważyć dobro jednostki i interes wspólnoty.",
                context="Wskazanie napięcia między wartościami",
                register="formal",
            ),
            PhrasebookEntry(
                text="Ze względu na możliwy konflikt interesów wyłączę się z oceny tego wniosku.",
                context="Ujawnienie okoliczności mogącej podważyć bezstronność oceny",
                register="formal",
                unit_ref="c1-unit-5",
            ),
            PhrasebookEntry(
                text="Zgoda udzielona pod presją nie rozwiązuje naszych wątpliwości etycznych.",
                context="Kwestionowanie dobrowolności zgody w dyskusji o procedurze",
                register="formal",
                unit_ref="c1-unit-5",
            ),
            PhrasebookEntry(
                text="Zanim ujawnimy te informacje, ustalmy, czy można osiągnąć cel "
                "mniej inwazyjnie.",
                context="Poszukiwanie rozwiązania lepiej chroniącego prywatność",
                register="formal",
                unit_ref="c1-unit-5",
            ),
            PhrasebookEntry(
                text="Same przeprosiny nie wystarczą, jeśli nie towarzyszy im naprawienie szkody.",
                context="Rozmowa o odpowiedzialności za skutki podjętej decyzji",
                register="neutral",
                unit_ref="c1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        id="tozsamosc",
        level="C1",
        situation="Kultura i tożsamość",
        icon="\U0001f30d",
        phrases=[
            PhrasebookEntry(
                text="Tożsamość kształtuje się w napięciu między tradycją a zmianą.",
                context="Ogólna teza o tożsamości kulturowej",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Moje korzenie są tu, choć od lat mieszkam za granicą.",
                context="Opisanie własnej tożsamości wielomiejscowej",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Nie należy mylić dziedzictwa z bezkrytycznym powtarzaniem tradycji.",
                context="Rozróżnienie dziedzictwa i tradycjonalizmu",
                register="formal",
            ),
            PhrasebookEntry(
                text="Język jest nośnikiem pamięci zbiorowej.",
                context="Znaczenie języka dla tożsamości",
                register="formal",
            ),
            PhrasebookEntry(
                text="Stereotypy upraszczają obraz innych kultur i utrudniają dialog.",
                context="Krytyka stereotypów kulturowych",
                register="formal",
            ),
            PhrasebookEntry(
                text="Migracja nie musi oznaczać utraty tożsamości.",
                context="Odpowiedź na obawę o asymilację",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Warto pytać, kto opowiada historię i czyim głosem.",
                context="Refleksja nad narracją kulturową",
                register="neutral",
            ),
            PhrasebookEntry(
                text="Wielokulturowość jest praktyką, nie tylko deklaracją.",
                context="Krytyka deklaratywnej wielokulturowości",
                register="formal",
            ),
            PhrasebookEntry(
                text="Mogę opowiedzieć o własnym doświadczeniu, ale nie reprezentuję "
                "całej społeczności.",
                context="Zaznaczenie granic własnej perspektywy podczas rozmowy o kulturze",
                register="neutral",
                unit_ref="c1-unit-7",
            ),
            PhrasebookEntry(
                text="Czy mogłaby pani wyjaśnić, jakie znaczenie ma ten zwyczaj "
                "dla jego uczestników?",
                context="Prośba o wyjaśnienie praktyki kulturowej bez pochopnej oceny",
                register="formal",
                unit_ref="c1-unit-7",
            ),
            PhrasebookEntry(
                text="Wolałbym, żebyśmy nie sprowadzali tej różnicy wyłącznie do narodowości.",
                context="Reakcja na nadmierne uogólnienie w rozmowie międzykulturowej",
                register="neutral",
                unit_ref="c1-unit-7",
            ),
            PhrasebookEntry(
                text="Czuję się związana z obiema kulturami, choć w każdej funkcjonuję "
                "trochę inaczej.",
                context="Opis wielokulturowej tożsamości w rozmowie osobistej",
                register="neutral",
                unit_ref="c1-unit-7",
            ),
        ],
    ),
]
