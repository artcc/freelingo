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
    VocabularySet(
        id="strategie-retoryczne_c2",
        level="C2",
        topic="Strategie retoryczne",
        unit_ref="c2-unit-2",
        words=[
            _entry(
                "antyteza",
                "noun",
                "Zestawienie przeciwstawnych treści w jednej wypowiedzi.",
                "Antyteza porządkuje końcową część przemówienia.",
            ),
            _entry(
                "paralelizm",
                "noun",
                "Powtórzenie podobnej budowy składniowej w sąsiadujących członach.",
                "Paralelizm podkreśla kontrast między propozycjami.",
            ),
            _entry(
                "nacechowany",
                "adjective",
                "Niosący wyraźny odcień stylistyczny, emocjonalny lub społeczny.",
                "To słowo jest silnie nacechowane emocjonalnie.",
            ),
            _entry(
                "uwypuklać",
                "verb",
                "Sprawiać, że dana cecha lub informacja staje się bardziej widoczna.",
                "Powtórzenie uwypukla główną myśl tekstu.",
            ),
        ],
    ),
    VocabularySet(
        id="analiza-dyskursu_c2",
        level="C2",
        topic="Analiza dyskursu i perspektywy",
        unit_ref="c2-unit-3",
        words=[
            _entry(
                "ramowanie",
                "noun",
                "Sposób przedstawienia tematu, który wpływa na jego interpretację.",
                "Ramowanie problemu zmienia odbiór argumentu.",
            ),
            _entry(
                "perspektywa",
                "noun",
                "Punkt widzenia, z którego opisuje się lub ocenia zjawisko.",
                "Narracja przyjmuje perspektywę świadka.",
            ),
            _entry(
                "implikować",
                "verb",
                "Sugerować określony wniosek bez wyrażania go wprost.",
                "To sformułowanie może implikować zgodę autora.",
            ),
            _entry(
                "wieloznaczny",
                "adjective",
                "Dopuszczający kilka znaczeń lub interpretacji.",
                "Wieloznaczny finał pozostawia pole do interpretacji.",
            ),
        ],
    ),
    VocabularySet(
        id="aluzje-i-intertekstualnosc_c2",
        level="C2",
        topic="Aluzje i intertekstualność",
        unit_ref="c2-unit-4",
        words=[
            _entry(
                "aluzja",
                "noun",
                "Pośrednie nawiązanie do znanej osoby, dzieła lub zdarzenia.",
                "W ostatnim akapicie pojawia się aluzja literacka.",
            ),
            _entry(
                "intertekstualny",
                "adjective",
                "Odnoszący się do powiązań między różnymi tekstami.",
                "Powieść zawiera liczne intertekstualne odniesienia.",
            ),
            _entry(
                "parafrazować",
                "verb",
                "Przedstawić cudzą treść własnymi słowami, zachowując jej sens.",
                "Autorka parafrazuje stanowisko polemisty.",
            ),
            _entry(
                "nawiązywać",
                "verb",
                "Odsyłać do wcześniejszej treści lub znanego motywu.",
                "Tytuł nawiązuje do popularnego przysłowia.",
            ),
        ],
    ),
    VocabularySet(
        id="pragmatyka-wypowiedzi_c2",
        level="C2",
        topic="Pragmatyka i akty mowy",
        unit_ref="c2-unit-4",
        words=[
            _entry(
                "niedopowiedzenie",
                "noun",
                "Celowe pominięcie części informacji, którą odbiorca ma odtworzyć.",
                "Niedopowiedzenie wzmacnia ironiczny efekt.",
            ),
            _entry(
                "insynuować",
                "verb",
                "Sugerować coś pośrednio, często bez przedstawienia dowodów.",
                "Mówca insynuuje konflikt interesów.",
            ),
            _entry(
                "dosłowny",
                "adjective",
                "Zgodny z podstawowym, bezpośrednim znaczeniem słów.",
                "Dosłowna interpretacja nie uwzględnia ironii.",
            ),
            _entry(
                "intencja",
                "noun",
                "Cel, który ktoś chce osiągnąć przez określone działanie lub wypowiedź.",
                "Intencja mówiącego wynika z kontekstu.",
            ),
        ],
    ),
    VocabularySet(
        id="ocena-argumentow_c2",
        level="C2",
        topic="Ocena argumentów i błędów rozumowania",
        unit_ref="c2-unit-5",
        words=[
            _entry(
                "fałszywa alternatywa",
                "phrase",
                "Przedstawienie dwóch możliwości tak, jakby nie istniały inne.",
                "Autor tworzy fałszywą alternatywę między bezpieczeństwem a prywatnością.",
            ),
            _entry(
                "uogólnienie",
                "noun",
                "Wniosek obejmujący szerszą grupę niż zbadane przypadki.",
                "To uogólnienie nie wynika z trzech przykładów.",
            ),
            _entry(
                "podważać",
                "verb",
                "Osłabiać wiarygodność lub zasadność twierdzenia.",
                "Nowe dane podważają wcześniejsze założenie.",
            ),
            _entry(
                "trafny",
                "adjective",
                "Dobrze odpowiadający analizowanej kwestii.",
                "Recenzent przedstawił trafną uwagę.",
            ),
        ],
    ),
    VocabularySet(
        id="zmiana-jezyka_c2",
        level="C2",
        topic="Zmiana języka i warianty",
        unit_ref="c2-unit-6",
        words=[
            _entry(
                "archaizm",
                "noun",
                "Wyraz lub forma typowa dla dawniejszego etapu języka.",
                "Archaizm w dialogu buduje historyczny styl.",
            ),
            _entry(
                "neologizm",
                "noun",
                "Nowy wyraz lub nowe znaczenie utworzone w języku.",
                "Neologizm szybko przyjął się w mediach społecznościowych.",
            ),
            _entry(
                "zapożyczenie",
                "noun",
                "Wyraz lub element przejęty z innego języka.",
                "To zapożyczenie ma już polską pisownię.",
            ),
            _entry(
                "ewoluować",
                "verb",
                "Stopniowo zmieniać się w czasie.",
                "Znaczenie tego wyrażenia nadal ewoluuje.",
            ),
        ],
    ),
]
