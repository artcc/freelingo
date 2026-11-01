"""Polish phrasebook — C2 categories."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="frazeologia_c2",
        level="C2",
        situation="Idiomy i aluzje",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="To sformułowanie ma wydźwięk ironiczny.",
                context="Opis tonu wypowiedzi.",
                register="formal",
                unit_ref="c2-unit-1",
            ),
            PhrasebookEntry(
                text="Czy ta aluzja jest czytelna bez znajomości kontekstu?",
                context="Pytanie o zrozumiałość odniesienia.",
                register="neutral",
                unit_ref="c2-unit-1",
            ),
            PhrasebookEntry(
                text="Autor świadomie odwraca utrwalone znaczenie tego zwrotu.",
                context="Opis gry frazeologicznej.",
                register="formal",
                unit_ref="c2-unit-1",
            ),
            PhrasebookEntry(
                text="W tym rejestrze ten idiom brzmiałby zbyt potocznie.",
                context="Uwaga o dopasowaniu stylu.",
                register="formal",
                unit_ref="c2-unit-1",
            ),
            PhrasebookEntry(
                text="Dosłowne tłumaczenie nie oddaje sensu tej wypowiedzi.",
                context="Wyjaśnienie problemu przekładu.",
                register="neutral",
                unit_ref="c2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        id="retoryka_c2",
        level="C2",
        situation="Argumentacja i perswazja",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Jakie założenie pozostaje tu niewypowiedziane?",
                context="Pytanie o ukrytą przesłankę.",
                register="formal",
                unit_ref="c2-unit-2",
            ),
            PhrasebookEntry(
                text="Ten argument jest przekonujący, ale nie rozstrzygający.",
                context="Zniuansowana ocena argumentu.",
                register="formal",
                unit_ref="c2-unit-2",
            ),
            PhrasebookEntry(
                text="Czy autor odpowiada na najmocniejszy kontrargument?",
                context="Pytanie o kompletność rozumowania.",
                register="formal",
                unit_ref="c2-unit-2",
            ),
            PhrasebookEntry(
                text="Proszę oddzielić ocenę skutków od oceny intencji.",
                context="Prośba o precyzję analizy.",
                register="formal",
                unit_ref="c2-unit-2",
            ),
            PhrasebookEntry(
                text="Wniosek należy ograniczyć do zakresu przedstawionych przesłanek.",
                context="Zastrzeżenie logiczne.",
                register="formal",
                unit_ref="c2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="synteza_c2",
        level="C2",
        situation="Synteza i podsumowanie",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                text="Oba teksty są zbieżne w ocenie długofalowych skutków.",
                context="Porównanie stanowisk.",
                register="formal",
                unit_ref="c2-unit-3",
            ),
            PhrasebookEntry(
                text="Źródła różnią się co do przyczyn tego zjawiska.",
                context="Wskazanie rozbieżności.",
                register="formal",
                unit_ref="c2-unit-3",
            ),
            PhrasebookEntry(
                text="Podsumowując, można wyróżnić trzy wzajemnie powiązane wątki.",
                context="Wprowadzenie syntezy.",
                register="formal",
                unit_ref="c2-unit-3",
            ),
            PhrasebookEntry(
                text="Ten wniosek pozostaje zgodny z wcześniejszymi ustaleniami.",
                context="Powiązanie konkluzji z analizą.",
                register="formal",
                unit_ref="c2-unit-3",
            ),
            PhrasebookEntry(
                text="Warto zaznaczyć, że dostępne dane nie pozwalają na mocniejsze twierdzenie.",
                context="Zastrzeżenie dotyczące pewności.",
                register="formal",
                unit_ref="c2-unit-3",
            ),
        ],
    ),
]
