"""Polish phrasebook — B2 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="spoleczenstwo_b2",
        level="B2",
        situation="Sprawy społeczne",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Jakie mogą być długofalowe skutki tej zmiany?",
                context="Pytanie o przewidywane konsekwencje.",
                register="neutral",
                unit_ref="b2-unit-1",
            ),
            PhrasebookEntry(
                text="Raport wskazuje na różnice między regionami.",
                context="Odwołanie do ustaleń raportu.",
                register="formal",
                unit_ref="b2-unit-1",
            ),
            PhrasebookEntry(
                text="Warto uwzględnić perspektywę osób, których to dotyczy.",
                context="Zachęta do poszerzenia analizy.",
                register="neutral",
                unit_ref="b2-unit-1",
            ),
            PhrasebookEntry(
                text="Ta propozycja wymaga bardziej szczegółowej oceny.",
                context="Zastrzeżenie do przedstawionego rozwiązania.",
                register="formal",
                unit_ref="b2-unit-1",
            ),
            PhrasebookEntry(
                text="Nie należy utożsamiać korelacji z przyczynowością.",
                context="Ważne rozróżnienie w analizie danych.",
                register="formal",
                unit_ref="b2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="media_b2",
        level="B2",
        situation="Media i interpretacja",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Czy można potwierdzić wiarygodność tego źródła?",
                context="Pytanie o rzetelność informacji.",
                register="formal",
                unit_ref="b2-unit-2",
            ),
            PhrasebookEntry(
                text="Autor przedstawia tę kwestię z innej perspektywy.",
                context="Opis sposobu ujęcia tematu.",
                register="neutral",
                unit_ref="b2-unit-2",
            ),
            PhrasebookEntry(
                text="Ten cytat należy odczytywać w szerszym kontekście.",
                context="Zastrzeżenie dotyczące interpretacji.",
                register="formal",
                unit_ref="b2-unit-2",
            ),
            PhrasebookEntry(
                text="W artykule nie podano danych potwierdzających tę tezę.",
                context="Wskazanie braku dowodów.",
                register="formal",
                unit_ref="b2-unit-2",
            ),
            PhrasebookEntry(
                text="Jak rozumie pani zakończenie tej powieści?",
                context="Pytanie o interpretację dzieła.",
                register="formal",
                unit_ref="b2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="prezentacja_b2",
        level="B2",
        situation="Prezentowanie i redagowanie",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Na początku przedstawię główne założenia analizy.",
                context="Rozpoczęcie prezentacji.",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="Przejdźmy teraz do najważniejszych wyników.",
                context="Przejście do kolejnej części wystąpienia.",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="Czy to sformułowanie można rozumieć na dwa sposoby?",
                context="Pytanie o możliwą dwuznaczność.",
                register="neutral",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="Pozwolę sobie doprecyzować zakres tego pojęcia.",
                context="Zapowiedź definicji lub uściślenia.",
                register="formal",
                unit_ref="b2-unit-3",
            ),
            PhrasebookEntry(
                text="Podsumowując, dostępne dane nie rozstrzygają tej kwestii.",
                context="Ostrożne podsumowanie.",
                register="formal",
                unit_ref="b2-unit-3",
            ),
        ],
    ),
]
