"""Polish phrasebook — A2 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="codzienne_rozmowy_a2",
        level="A2",
        situation="Codzienne rozmowy",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Co robiłeś w weekend?",
                context="Pytanie o przeszłe czynności do znajomego.",
                register="informal",
                unit_ref="a2-unit-1",
            ),
            PhrasebookEntry(
                text="W zeszłym roku byliśmy nad morzem.",
                context="Opowieść o minionym wyjeździe.",
                register="neutral",
                unit_ref="a2-unit-1",
            ),
            PhrasebookEntry(
                text="Czy mogłaby pani powtórzyć?",
                context="Uprzejma prośba o powtórzenie informacji.",
                register="formal",
                unit_ref="a2-unit-1",
            ),
            PhrasebookEntry(
                text="Planuję odwiedzić rodzinę w sobotę.",
                context="Informacja o przyszłym planie.",
                register="neutral",
                unit_ref="a2-unit-1",
            ),
            PhrasebookEntry(
                text="To było naprawdę ciekawe doświadczenie.",
                context="Ocena minionego wydarzenia.",
                register="neutral",
                unit_ref="a2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="uslugi_a2",
        level="A2",
        situation="Zakupy i usługi",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Ile kosztuje ta torba?",
                context="Pytanie o cenę produktu.",
                register="neutral",
                unit_ref="a2-unit-2",
            ),
            PhrasebookEntry(
                text="Czy mogę zapłacić kartą?",
                context="Pytanie o akceptowaną formę płatności.",
                register="neutral",
                unit_ref="a2-unit-2",
            ),
            PhrasebookEntry(
                text="Chciałbym zwrócić ten produkt.",
                context="Prośba o przyjęcie zwrotu.",
                register="formal",
                unit_ref="a2-unit-2",
            ),
            PhrasebookEntry(
                text="Poproszę paragon.",
                context="Prośba o potwierdzenie zakupu.",
                register="neutral",
                unit_ref="a2-unit-2",
            ),
            PhrasebookEntry(
                text="Czy ten produkt jest dostępny w innym rozmiarze?",
                context="Pytanie o inną wersję produktu.",
                register="formal",
                unit_ref="a2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="podroz_a2",
        level="A2",
        situation="W podróży",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="O której odjeżdża następny pociąg?",
                context="Pytanie o godzinę odjazdu.",
                register="neutral",
                unit_ref="a2-unit-3",
            ),
            PhrasebookEntry(
                text="Gdzie muszę się przesiąść?",
                context="Pytanie o miejsce zmiany pociągu lub autobusu.",
                register="neutral",
                unit_ref="a2-unit-3",
            ),
            PhrasebookEntry(
                text="Mam rezerwację na nazwisko Kowalska.",
                context="Zameldowanie w hotelu.",
                register="formal",
                unit_ref="a2-unit-3",
            ),
            PhrasebookEntry(
                text="Czy w pobliżu jest apteka?",
                context="Pytanie o lokalną usługę.",
                register="neutral",
                unit_ref="a2-unit-3",
            ),
            PhrasebookEntry(
                text="Zgubiłem bagaż na dworcu.",
                context="Zgłoszenie zagubionego bagażu.",
                register="neutral",
                unit_ref="a2-unit-3",
            ),
        ],
    ),
]
