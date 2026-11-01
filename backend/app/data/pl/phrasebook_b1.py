"""Polish phrasebook — B1 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="opinia_b1",
        level="B1",
        situation="Wyrażanie opinii",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Moim zdaniem warto rozważyć tę propozycję.",
                context="Przedstawienie własnej opinii.",
                register="neutral",
                unit_ref="b1-unit-2",
            ),
            PhrasebookEntry(
                text="Zgadzam się z tym argumentem, ponieważ jest poparty danymi.",
                context="Uzasadniona zgoda.",
                register="neutral",
                unit_ref="b1-unit-2",
            ),
            PhrasebookEntry(
                text="Rozumiem ten punkt widzenia, ale mam pewne wątpliwości.",
                context="Uprzejme wyrażenie zastrzeżenia.",
                register="neutral",
                unit_ref="b1-unit-2",
            ),
            PhrasebookEntry(
                text="Czy mogę dodać jeszcze jeden argument?",
                context="Prośba o zabranie głosu.",
                register="formal",
                unit_ref="b1-unit-2",
            ),
            PhrasebookEntry(
                text="Warto odróżnić skutek od przyczyny.",
                context="Zwrócenie uwagi na ważne rozróżnienie.",
                register="neutral",
                unit_ref="b1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="praca_b1",
        level="B1",
        situation="Praca i nauka",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Jakie doświadczenie jest wymagane na tym stanowisku?",
                context="Pytanie podczas rozmowy o pracę.",
                register="formal",
                unit_ref="b1-unit-3",
            ),
            PhrasebookEntry(
                text="Chciałbym rozwijać swoje umiejętności analityczne.",
                context="Opis celu zawodowego.",
                register="formal",
                unit_ref="b1-unit-3",
            ),
            PhrasebookEntry(
                text="Czy moglibyśmy omówić zakres obowiązków?",
                context="Prośba o doprecyzowanie oferty.",
                register="formal",
                unit_ref="b1-unit-3",
            ),
            PhrasebookEntry(
                text="Zajmę się tym po zakończeniu spotkania.",
                context="Zobowiązanie do wykonania zadania.",
                register="neutral",
                unit_ref="b1-unit-3",
            ),
            PhrasebookEntry(
                text="Proszę przesłać dokument do końca tygodnia.",
                context="Uprzejme polecenie w pracy.",
                register="formal",
                unit_ref="b1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        id="debaty_b1",
        level="B1",
        situation="Dyskusja i debata",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="W jakim stopniu zgadza się pan z tym wnioskiem?",
                context="Pytanie o zakres zgody.",
                register="formal",
                unit_ref="b1-unit-2",
            ),
            PhrasebookEntry(
                text="Chciałbym odnieść się do poprzedniego argumentu.",
                context="Wprowadzenie odpowiedzi w dyskusji.",
                register="formal",
                unit_ref="b1-unit-2",
            ),
            PhrasebookEntry(
                text="Czy mogę prosić o konkretny przykład?",
                context="Prośba o poparcie tezy przykładem.",
                register="neutral",
                unit_ref="b1-unit-2",
            ),
            PhrasebookEntry(
                text="Przyjmijmy na chwilę inne założenie.",
                context="Propozycja zmiany punktu wyjścia.",
                register="neutral",
                unit_ref="b1-unit-2",
            ),
            PhrasebookEntry(
                text="Ten wniosek wymaga dodatkowego uzasadnienia.",
                context="Uprzejme zakwestionowanie wniosku.",
                register="neutral",
                unit_ref="b1-unit-2",
            ),
        ],
    ),
]
