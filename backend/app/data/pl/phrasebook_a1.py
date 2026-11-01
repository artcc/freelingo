"""Polish phrasebook — A1 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="powitania",
        level="A1",
        situation="Powitania i przedstawianie się",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Dzień dobry.",
                context="Uprzejme powitanie w ciągu dnia.",
                register="formal",
                unit_ref="a1-unit-1",
            ),
            PhrasebookEntry(
                text="Cześć!",
                context="Powitanie znajomej osoby.",
                register="informal",
                unit_ref="a1-unit-1",
            ),
            PhrasebookEntry(
                text="Mam na imię Anna.",
                context="Podanie swojego imienia.",
                register="neutral",
                unit_ref="a1-unit-1",
            ),
            PhrasebookEntry(
                text="Miło mi pana poznać.",
                context="Uprzejma reakcja przy poznaniu mężczyzny.",
                register="formal",
                unit_ref="a1-unit-1",
            ),
            PhrasebookEntry(
                text="Do zobaczenia jutro.",
                context="Pożegnanie z zapowiedzią kolejnego spotkania.",
                register="neutral",
                unit_ref="a1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="prosby_a1",
        level="A1",
        situation="Prośby i podstawowe informacje",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Czy może mi pan pomóc?",
                context="Uprzejma prośba o pomoc.",
                register="formal",
                unit_ref="a1-unit-1",
            ),
            PhrasebookEntry(
                text="Proszę mówić wolniej.",
                context="Prośba o wolniejsze tempo rozmowy.",
                register="formal",
                unit_ref="a1-unit-1",
            ),
            PhrasebookEntry(
                text="Nie rozumiem tego słowa.",
                context="Informacja o niezrozumiałym wyrazie.",
                register="neutral",
                unit_ref="a1-unit-1",
            ),
            PhrasebookEntry(
                text="Gdzie jest najbliższy przystanek?",
                context="Pytanie o położenie przystanku.",
                register="neutral",
                unit_ref="a1-unit-1",
            ),
            PhrasebookEntry(
                text="Dziękuję za pomoc.",
                context="Podziękowanie po otrzymaniu pomocy.",
                register="neutral",
                unit_ref="a1-unit-1",
            ),
        ],
    ),
]
