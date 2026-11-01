"""C2 vocabulary sets."""

from app.data._types import PartOfSpeech, VocabularyEntry, VocabularySet


def _entry(word: str, pos: PartOfSpeech, definition: str, example: str) -> VocabularyEntry:
    return VocabularyEntry(word=word, pos=pos, definition=definition, example=example)


C2_SETS: list[VocabularySet] = [
    VocabularySet(
        id="frazeologia_c2",
        level="C2",
        topic="Frazeologia i idiomy",
        unit_ref="c2-unit-1",
        words=[
            _entry(
                "aluzja",
                "noun",
                "Pośrednie nawiązanie do znanej treści.",
                "W ostatnim zdaniu pojawia się aluzja literacka.",
            ),
            _entry(
                "konwencja",
                "noun",
                "Przyjęty zwyczaj lub sposób przedstawiania treści.",
                "Autor świadomie łamie konwencję gatunku.",
            ),
            _entry(
                "dosłowny",
                "adjective",
                "Zgodny z podstawowym znaczeniem użytych słów.",
                "Dosłowne odczytanie idiomu prowadzi do błędu.",
            ),
            _entry(
                "przenośnia",
                "noun",
                "Wyrażenie użyte w znaczeniu obrazowym.",
                "Ta przenośnia nadaje tekstowi lekko ironiczny ton.",
            ),
        ],
    ),
    VocabularySet(
        id="retoryka_c2",
        level="C2",
        topic="Retoryka i argumentacja",
        unit_ref="c2-unit-2",
        words=[
            _entry(
                "założenie",
                "noun",
                "Twierdzenie przyjęte jako punkt wyjścia rozumowania.",
                "Argument opiera się na nieuzasadnionym założeniu.",
            ),
            _entry(
                "kontrargument",
                "noun",
                "Argument podważający lub ograniczający inną tezę.",
                "Autorka odpowiada na najmocniejszy kontrargument.",
            ),
            _entry(
                "perswazja",
                "noun",
                "Oddziaływanie na odbiorcę w celu zmiany jego opinii.",
                "Perswazja nie zastępuje dowodów.",
            ),
            _entry(
                "wnikliwy",
                "adjective",
                "Dokładnie dostrzegający istotne szczegóły.",
                "To wnikliwy komentarz do debaty.",
            ),
        ],
    ),
    VocabularySet(
        id="synteza_c2",
        level="C2",
        topic="Synteza i interpretacja",
        unit_ref="c2-unit-3",
        words=[
            _entry(
                "rozbieżność",
                "noun",
                "Różnica między danymi, poglądami lub wynikami.",
                "Autor wyjaśnia rozbieżność między źródłami.",
            ),
            _entry(
                "zbieżny",
                "adjective",
                "Zgodny z innym elementem pod względem kierunku lub treści.",
                "Wnioski obu badań są zbieżne.",
            ),
            _entry(
                "konsekwencja",
                "noun",
                "Skutek lub logiczne następstwo działania.",
                "Warto uwzględnić długofalowe konsekwencje decyzji.",
            ),
            _entry(
                "syntetyzować",
                "verb",
                "Łączyć wiele informacji w spójną całość.",
                "Esej syntetyzuje wyniki kilku analiz.",
            ),
        ],
    ),
    VocabularySet(
        id="pragmatyka_c2",
        level="C2",
        topic="Pragmatyka, ironia i aluzje",
        unit_ref="c2-unit-4",
        words=[
            _entry(
                "niedopowiedzenie",
                "noun",
                "Celowe pozostawienie części treści bez wyraźnego wyrażenia.",
                "Niedopowiedzenie wzmacnia zakończenie opowiadania.",
            ),
            _entry(
                "ironia",
                "noun",
                "Sposób wyrażenia znaczenia odmiennego od dosłownego.",
                "Ironia autora jest czytelna dopiero w ostatnim zdaniu.",
            ),
            _entry(
                "aluzja",
                "noun",
                "Pośrednie nawiązanie do znanego tekstu lub wydarzenia.",
                "Czytelnik rozpoznaje aluzję do klasycznej powieści.",
            ),
            _entry(
                "sugerować",
                "verb",
                "Pośrednio wskazywać na możliwe znaczenie lub wniosek.",
                "Dobór słów może sugerować dystans mówiącego.",
            ),
        ],
    ),
    VocabularySet(
        id="perswazja_c2",
        level="C2",
        topic="Perswazja i krytyka argumentów",
        unit_ref="c2-unit-5",
        words=[
            _entry(
                "retoryczny",
                "adjective",
                "Służący przekonywaniu lub wywołaniu określonego efektu.",
                "Pytanie retoryczne porządkuje argumentację.",
            ),
            _entry(
                "manipulacja",
                "noun",
                "Wpływanie na czyjąś ocenę przez zniekształcenie informacji.",
                "Analiza ujawniła manipulację danymi.",
            ),
            _entry(
                "ustępstwo",
                "noun",
                "Przyznanie części racji drugiej stronie.",
                "Autor rozpoczyna odpowiedź od ustępstwa.",
            ),
            _entry(
                "podważać",
                "verb",
                "Osłabiać zasadność twierdzenia lub przekonania.",
                "Kontrprzykład podważa główną tezę.",
            ),
        ],
    ),
    VocabularySet(
        id="warianty_c2",
        level="C2",
        topic="Warianty języka i zmiana znaczeń",
        unit_ref="c2-unit-6",
        words=[
            _entry(
                "archaizm",
                "noun",
                "Dawna forma lub wyraz rzadko używany współcześnie.",
                "Archaizm wskazuje na historyczny charakter narracji.",
            ),
            _entry(
                "regionalizm",
                "noun",
                "Wyraz lub forma typowa dla określonego regionu.",
                "Regionalizm pojawia się w dialogach bohaterów.",
            ),
            _entry(
                "neologizm",
                "noun",
                "Nowy wyraz lub nowe znaczenie istniejącego słowa.",
                "Autor tworzy neologizm na potrzeby opowiadania.",
            ),
            _entry(
                "zapożyczenie",
                "noun",
                "Wyraz przejęty z innego języka.",
                "To zapożyczenie jest już powszechne w polszczyźnie.",
            ),
        ],
    ),
    VocabularySet(
        id="niuans_c2",
        level="C2",
        topic="Niuanse, styl i interpretacja",
        unit_ref="c2-unit-7",
        words=[
            _entry(
                "konotacja",
                "noun",
                "Dodatkowe skojarzenie związane z wyrazem.",
                "To słowo ma negatywną konotację.",
            ),
            _entry(
                "odcień",
                "noun",
                "Subtelna różnica w znaczeniu lub zabarwieniu wypowiedzi.",
                "Zmiana czasownika wprowadza inny odcień znaczeniowy.",
            ),
            _entry(
                "zwięzłość",
                "noun",
                "Przekazywanie treści w niewielu słowach.",
                "Zwięzłość nie może usuwać ważnych zastrzeżeń.",
            ),
            _entry(
                "niejednoznaczny",
                "adjective",
                "Pozostawiający więcej niż jedną możliwą interpretację.",
                "Zakończenie utworu pozostaje niejednoznaczne.",
            ),
        ],
    ),
    VocabularySet(
        id="powtorka_c2",
        level="C2",
        topic="Powtórka: styl i synteza",
        unit_ref="c2-unit-8",
        words=[
            _entry(
                "reinterpretacja",
                "noun",
                "Ponowne odczytanie znaczenia w nowym kontekście.",
                "Nowe źródła skłoniły badaczy do reinterpretacji tekstu.",
            ),
            _entry(
                "wielowarstwowy",
                "adjective",
                "Zawierający kilka poziomów znaczenia lub interpretacji.",
                "To wielowarstwowy esej o pamięci.",
            ),
            _entry(
                "niuansować",
                "verb",
                "Przedstawiać różnice i zastrzeżenia z dużą precyzją.",
                "Warto niuansować ocenę przedstawionych dowodów.",
            ),
            _entry(
                "wymowa",
                "noun",
                "Znaczenie lub skutek, jaki ma dana wypowiedź.",
                "Historyczna wymowa tego gestu zmienia interpretację.",
            ),
        ],
    ),
]
