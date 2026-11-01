"""Polish phrasebook — C1 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="akademicki_c1",
        level="C1",
        situation="Rozmowa akademicka",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Jakie przesłanki uzasadniają tę interpretację?",
                context="Pytanie o podstawę wniosku.",
                register="formal",
                unit_ref="c1-unit-1",
            ),
            PhrasebookEntry(
                text="Wyniki należy interpretować z uwzględnieniem ograniczeń badania.",
                context="Zastrzeżenie metodologiczne.",
                register="formal",
                unit_ref="c1-unit-1",
            ),
            PhrasebookEntry(
                text="Czy autorzy rozróżniają korelację i zależność przyczynową?",
                context="Pytanie o metodę analizy.",
                register="formal",
                unit_ref="c1-unit-1",
            ),
            PhrasebookEntry(
                text="Pozwolę sobie zakwestionować to założenie.",
                context="Uprzejme podważenie punktu wyjścia.",
                register="formal",
                unit_ref="c1-unit-1",
            ),
            PhrasebookEntry(
                text="Ten wniosek wykracza poza przedstawione dane.",
                context="Ocena zakresu wnioskowania.",
                register="formal",
                unit_ref="c1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="redakcja_c1",
        level="C1",
        situation="Redakcja i precyzja",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Proponuję zastąpić to wyrażenie bardziej precyzyjnym terminem.",
                context="Sugestia redakcyjna.",
                register="formal",
                unit_ref="c1-unit-3",
            ),
            PhrasebookEntry(
                text="W tym akapicie warto wyraźniej wskazać podmiot działania.",
                context="Uwagi dotyczące jasności tekstu.",
                register="formal",
                unit_ref="c1-unit-3",
            ),
            PhrasebookEntry(
                text="Czy można skrócić to zdanie bez utraty istotnej treści?",
                context="Pytanie o zwięzłość.",
                register="neutral",
                unit_ref="c1-unit-3",
            ),
            PhrasebookEntry(
                text="Należy zachować rozróżnienie między opisem a oceną.",
                context="Przypomnienie o obiektywności.",
                register="formal",
                unit_ref="c1-unit-3",
            ),
            PhrasebookEntry(
                text="To sformułowanie jest poprawne, lecz nie pasuje do rejestru.",
                context="Uwaga dotycząca stylu.",
                register="formal",
                unit_ref="c1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        id="kultura_c1",
        level="C1",
        situation="Kultura i interpretacja",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Jaką funkcję pełni ten motyw w całym utworze?",
                context="Pytanie o rolę powracającego elementu.",
                register="formal",
                unit_ref="c1-unit-2",
            ),
            PhrasebookEntry(
                text="Interpretacja zależy tu od kontekstu historycznego.",
                context="Zastrzeżenie kontekstowe.",
                register="neutral",
                unit_ref="c1-unit-2",
            ),
            PhrasebookEntry(
                text="Ten zabieg tworzy wyraźny kontrast między bohaterami.",
                context="Opis środka artystycznego.",
                register="formal",
                unit_ref="c1-unit-2",
            ),
            PhrasebookEntry(
                text="Warto odróżnić intencję autora od reakcji odbiorcy.",
                context="Wskazanie dwóch poziomów interpretacji.",
                register="neutral",
                unit_ref="c1-unit-2",
            ),
            PhrasebookEntry(
                text="Czy ta aluzja była czytelna dla ówczesnych odbiorców?",
                context="Pytanie o odbiór historyczny.",
                register="formal",
                unit_ref="c1-unit-2",
            ),
        ],
    ),
]
