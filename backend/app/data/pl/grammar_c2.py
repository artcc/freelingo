"""Polish grammar topics — C2."""

from app.data._types import GrammarExample, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="frazeologia",
        title="Frazeologizmy",
        level="C2",
        category="Gramatyka",
        summary="Frazeologizmy mają znaczenie, którego nie da się odczytać wyłącznie ze składników.",
        explanation="Związki frazeologiczne różnią się stopniem utrwalenia i formalności. Ich znaczenie zależy od kontekstu, a niektóre dopuszczają ograniczone warianty. Dosłowne tłumaczenie często prowadzi do nienaturalnej polszczyzny.",
        structure="rzucić nowe światło; wyciągnąć wnioski; mieć coś na uwadze",
        rules=[
            "Ustal znaczenie związku z kontekstu.",
            "Sprawdź, czy frazeologizm pasuje do rejestru.",
            "Nie zmieniaj utrwalonych składników bez wyraźnego efektu stylistycznego.",
        ],
        examples=[
            GrammarExample(
                text="Nowe dane rzuciły światło na przyczynę awarii.",
                translation=None,
                note="Znaczenie przenośne.",
            ),
            GrammarExample(
                text="Warto mieć na uwadze ograniczenia badania.",
                translation=None,
                note="Utrwalone połączenie.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="rejestry",
        title="Rejestry językowe",
        level="C2",
        category="Gramatyka",
        summary="Rejestr językowy zależy od odbiorcy, celu i sytuacji komunikacyjnej.",
        explanation="Wypowiedź może być potoczna, neutralna, oficjalna, specjalistyczna lub artystyczna. Mieszanie rejestrów bywa celowym środkiem stylistycznym, lecz bez uzasadnienia osłabia spójność. Wybór formy grzecznościowej niesie znaczenie społeczne.",
        structure="ty; pan/pani; formy urzędowe i specjalistyczne",
        rules=[
            "Ustal odbiorcę i cel przed doborem rejestru.",
            "Zachowuj spójność rejestru w obrębie tekstu.",
            "Traktuj zmianę rejestru jako świadomy zabieg.",
        ],
        examples=[
            GrammarExample(
                text="Uprzejmie proszę o potwierdzenie terminu.",
                translation=None,
                note="Rejestr formalny.",
            ),
            GrammarExample(
                text="Daj znać, kiedy będziesz.",
                translation=None,
                note="Rejestr nieformalny.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="retoryka",
        title="Środki retoryczne",
        level="C2",
        category="Gramatyka",
        summary="Środki retoryczne organizują argumentację i wpływają na odbiór tekstu.",
        explanation="Kontrast, powtórzenie, pytanie retoryczne i analogia mogą porządkować tok rozumowania lub wzmacniać perswazję. Analizując tekst, oddzielaj efekt retoryczny od wartości dowodowej argumentu.",
        structure="teza, przesłanki, zastrzeżenie, wniosek",
        rules=[
            "Oceniaj, czy przesłanki wspierają tezę.",
            "Rozpoznawaj założenia niewypowiedziane wprost.",
            "Nie utożsamiaj przekonującej formy z prawdziwością twierdzenia.",
        ],
        examples=[
            GrammarExample(
                text="Czy możemy pozwolić sobie na dalsze odkładanie tej decyzji?",
                translation=None,
                note="Pytanie retoryczne.",
            ),
            GrammarExample(
                text="Z jednej strony koszty rosną, z drugiej — opóźnienie zwiększa ryzyko.",
                translation=None,
                note="Równoważenie argumentów.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="ironia-i-pragmatyka",
        title="Ironia i znaczenie pragmatyczne",
        level="C2",
        category="Gramatyka",
        summary="Znaczenie wypowiedzi zależy od kontekstu, intencji i wspólnej wiedzy rozmówców.",
        explanation="Ironia, aluzja, niedopowiedzenie i implikatura mogą przekazywać treść inną niż dosłowna. Ich interpretacja wymaga uwzględnienia relacji między rozmówcami, sytuacji oraz sygnałów językowych; nie należy przypisywać intencji bez wystarczających przesłanek.",
        structure="dosłownie; w przenośni; aluzja; niedopowiedzenie",
        rules=[
            "Oddzielaj sens dosłowny od możliwego sensu implikowanego.",
            "Uzasadniaj interpretację sygnałami z kontekstu.",
            "Uwzględniaj, że ironia może być nieczytelna poza daną sytuacją.",
        ],
        examples=[
            GrammarExample(
                text="Świetnie, kolejna godzina w korku.",
                translation=None,
                note="Kontekst może wskazywać na ironię.",
            ),
            GrammarExample(
                text="Nie powiedział tego wprost, ale aluzja była czytelna.",
                translation=None,
                note="Znaczenie przekazane pośrednio.",
            ),
        ],
        common_mistakes=[
        ],
    ),
    GrammarTopic(
        slug="warianty-i-norma",
        title="Warianty, norma i zmiana języka",
        level="C2",
        category="Gramatyka",
        summary="Polszczyzna zmienia się w czasie i różnicuje zależnie od regionu oraz sytuacji.",
        explanation="Norma wzorcowa i użytkowa opisują różne poziomy akceptacji form. Regionalizmy, archaizmy, zapożyczenia i neologizmy mogą pełnić funkcję stylistyczną. Ocenę formy należy oddzielić od opisu jej społecznego użycia.",
        structure="norma; regionalizm; archaizm; neologizm",
        rules=[
            "Rozpoznawaj, czy forma jest regionalna, historyczna, środowiskowa czy ogólnopolska.",
            "Oceniaj poprawność w odniesieniu do rejestru i celu wypowiedzi.",
            "Nie utożsamiaj częstego użycia z neutralnym stylem.",
        ],
        examples=[
            GrammarExample(
                text="W dialogu autor zachował regionalizmy bohaterów.",
                translation=None,
                note="Wariant języka buduje charakterystykę postaci.",
            ),
            GrammarExample(
                text="To zapożyczenie jest już powszechne, ale nadal ma potoczny odcień.",
                translation=None,
                note="Częstość i rejestr to odrębne cechy.",
            ),
        ],
        common_mistakes=[
        ],
    ),
]
