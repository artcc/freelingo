"""Polish assessment bank — placement questions."""

from app.data._types import AssessmentQuestion

ASSESSMENT_BANK: list[AssessmentQuestion] = [
    # ============================================================
    # A1 GRAMMAR (10 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-g-a1-001",
        skill="grammar",
        difficulty="A1",
        question="Uzupełnij: Ona ___ z Polski.",
        options=["jestem", "jest", "jesteś", "są"],
        correct="jest",
        grammar_slug="byc",
    ),
    AssessmentQuestion(
        id="pl-g-a1-002",
        skill="grammar",
        difficulty="A1",
        question="Który zaimek pasuje? ___ jesteśmy studentami.",
        options=["Ja", "Wy", "My", "Oni"],
        correct="My",
        grammar_slug="zaimki-osobowe",
    ),
    AssessmentQuestion(
        id="pl-g-a1-003",
        skill="grammar",
        difficulty="A1",
        question="Który rzeczownik jest rodzaju żeńskiego?",
        options=["stół", "okno", "samochód", "książka"],
        correct="książka",
        grammar_slug="rodzaj-rzeczownika",
    ),
    AssessmentQuestion(
        id="pl-g-a1-004",
        skill="grammar",
        difficulty="A1",
        question="Uzupełnij: Jestem ___.",
        options=["Hiszpaninem", "Hiszpan", "Hiszpana", "Hiszpanie"],
        correct="Hiszpaninem",
        grammar_slug="narzednik-narodowosc",
    ),
    AssessmentQuestion(
        id="pl-g-a1-005",
        skill="grammar",
        difficulty="A1",
        question="Jaka jest liczba mnoga rzeczownika „student” w mianowniku?",
        options=["studenty", "studenci", "studentowie", "studencie"],
        correct="studenci",
        grammar_slug="mianownik-liczba-mnoga",
    ),
    AssessmentQuestion(
        id="pl-g-a1-006",
        skill="grammar",
        difficulty="A1",
        question="Która forma żeńska rzeczownika „lekarz” jest poprawna?",
        options=["lekarzka", "lekarzowa", "lekarka", "lekarska"],
        correct="lekarka",
        grammar_slug="zawod-rodzaj",
    ),
    AssessmentQuestion(
        id="pl-g-a1-007",
        skill="grammar",
        difficulty="A1",
        question="Uzupełnij: ___ kobieta.",
        options=["Wysoki", "Wysokie", "Wysokiego", "Wysoka"],
        correct="Wysoka",
        grammar_slug="przymiotniki-rodzaj",
    ),
    AssessmentQuestion(
        id="pl-g-a1-008",
        skill="grammar",
        difficulty="A1",
        question="Uzupełnij: To jest ___ brat.",
        options=["mój", "moja", "moje", "mojego"],
        correct="mój",
        grammar_slug="zaimki-dzierzawcze",
    ),
    AssessmentQuestion(
        id="pl-g-a1-009",
        skill="grammar",
        difficulty="A1",
        question="Które zdanie przeczy zdaniu „To jest mój brat” przez negację czasownika jest?",
        options=[
            "To jest nie mój brat.",
            "To nie jest mój brat.",
            "To niebrat jest mój.",
            "To nie moja brat jest.",
        ],
        correct="To nie jest mój brat.",
        grammar_slug="przeczenie-nie",
    ),
    AssessmentQuestion(
        id="pl-g-a1-010",
        skill="grammar",
        difficulty="A1",
        question="Uzupełnij: Ona ___ po polsku.",
        options=["mówi", "mówię", "mówisz", "mówimy"],
        correct="mówi",
        grammar_slug="czas-terazniejszy",
    ),
    # ============================================================
    # A1 VOCABULARY (6 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-v-a1-001",
        skill="vocabulary",
        difficulty="A1",
        question="Które słowo należy do grupy „owoce”?",
        options=["marchew", "jabłko", "chleb", "mleko"],
        correct="jabłko",
    ),
    AssessmentQuestion(
        id="pl-v-a1-002",
        skill="vocabulary",
        difficulty="A1",
        question="Które słowo jest przeciwieństwem słowa „drogi”?",
        options=["tani", "duży", "nowy", "szybki"],
        correct="tani",
    ),
    AssessmentQuestion(
        id="pl-v-a1-003",
        skill="vocabulary",
        difficulty="A1",
        question="Który wyraz jest nazwą dnia tygodnia?",
        options=["styczeń", "lato", "wtorek", "godzina"],
        correct="wtorek",
    ),
    AssessmentQuestion(
        id="pl-v-a1-004",
        skill="vocabulary",
        difficulty="A1",
        question="Jak nazywa się osoba, która leczy chorych?",
        options=["nauczyciel", "kierowca", "sprzedawca", "lekarz"],
        correct="lekarz",
    ),
    AssessmentQuestion(
        id="pl-v-a1-005",
        skill="vocabulary",
        difficulty="A1",
        question="Który wyraz jest nazwą pomieszczenia w domu?",
        options=["stół", "kuchnia", "okno", "dywan"],
        correct="kuchnia",
    ),
    AssessmentQuestion(
        id="pl-v-a1-006",
        skill="vocabulary",
        difficulty="A1",
        question="Które słowo oznacza osobę uczącą się w szkole?",
        options=["uczeń", "nauczyciel", "dyrektor", "lekarz"],
        correct="uczeń",
    ),
    # ============================================================
    # A1 READING (5 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-r-a1-001",
        skill="reading",
        difficulty="A1",
        question=(
            "Tekst: Anna mieszka w Krakowie. Codziennie rano pije kawę i czyta gazetę. "
            "Gdzie mieszka Anna?"
        ),
        options=["w Warszawie", "w Gdańsku", "w Krakowie", "w Poznaniu"],
        correct="w Krakowie",
    ),
    AssessmentQuestion(
        id="pl-r-a1-002",
        skill="reading",
        difficulty="A1",
        question="Tekst: Piotr ma dwa koty i jednego psa. Ile kotów ma Piotr?",
        options=["dwa", "trzy", "jednego", "cztery"],
        correct="dwa",
    ),
    AssessmentQuestion(
        id="pl-r-a1-003",
        skill="reading",
        difficulty="A1",
        question=("Tekst: W sobotę Marek idzie do kina z siostrą. " "Z kim idzie Marek do kina?"),
        options=["z bratem", "z siostrą", "z mamą", "z kolegą"],
        correct="z siostrą",
    ),
    AssessmentQuestion(
        id="pl-r-a1-004",
        skill="reading",
        difficulty="A1",
        question=(
            "Tekst: Sklep jest otwarty od poniedziałku do piątku. "
            "W niedzielę jest zamknięty. Kiedy sklep jest zamknięty?"
        ),
        options=["w poniedziałek", "we wtorek", "w piątek", "w niedzielę"],
        correct="w niedzielę",
    ),
    AssessmentQuestion(
        id="pl-r-a1-005",
        skill="reading",
        difficulty="A1",
        question=(
            "Tekst: Ewa jest nauczycielką. Pracuje w małej szkole i uczy dzieci. "
            "Jaki jest zawód Ewy?"
        ),
        options=["nauczycielka", "lekarka", "studentka", "sprzedawczyni"],
        correct="nauczycielka",
    ),
    # ============================================================
    # A2 GRAMMAR (10 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-g-a2-001",
        skill="grammar",
        difficulty="A2",
        question="Uzupełnij: Wczoraj Anna ___ do kina.",
        options=["poszedł", "poszło", "poszli", "poszła"],
        correct="poszła",
        grammar_slug="czas-przeszly-rodzaj",
    ),
    AssessmentQuestion(
        id="pl-g-a2-002",
        skill="grammar",
        difficulty="A2",
        question="Który czasownik jest dokonany?",
        options=["czytać", "pisać", "przeczytać", "malować"],
        correct="przeczytać",
        grammar_slug="aspekt-wprowadzenie",
    ),
    AssessmentQuestion(
        id="pl-g-a2-003",
        skill="grammar",
        difficulty="A2",
        question="Uzupełnij: Nie mam ___ na kawę.",
        options=["czas", "czasu", "czasem", "czasie"],
        correct="czasu",
        grammar_slug="dopelniacz",
    ),
    AssessmentQuestion(
        id="pl-g-a2-004",
        skill="grammar",
        difficulty="A2",
        question="Uzupełnij: Mam pięć ___.",
        options=["jabłek", "jabłka", "jabłko", "jabłkami"],
        correct="jabłek",
        grammar_slug="dopelniacz-liczebniki",
    ),
    AssessmentQuestion(
        id="pl-g-a2-005",
        skill="grammar",
        difficulty="A2",
        question="Uzupełnij: Nie mam tej książki. Nie mam ___.",
        options=["ją", "ona", "nią", "jej"],
        correct="jej",
        grammar_slug="zaimki-dopelniacz",
    ),
    AssessmentQuestion(
        id="pl-g-a2-006",
        skill="grammar",
        difficulty="A2",
        question="Uzupełnij: Dzisiaj jest ___ maja.",
        options=["pierwszego", "pierwszym", "pierwszy", "pierwsza"],
        correct="pierwszy",
        grammar_slug="liczebniki-porzadkowe",
    ),
    AssessmentQuestion(
        id="pl-g-a2-007",
        skill="grammar",
        difficulty="A2",
        question="Uzupełnij: Daję prezent ___.",
        options=["mama", "mamie", "mamę", "mamą"],
        correct="mamie",
        grammar_slug="celownik",
    ),
    AssessmentQuestion(
        id="pl-g-a2-008",
        skill="grammar",
        difficulty="A2",
        question="Uzupełnij w czasie teraźniejszym: ___ mnie głowa.",
        options=["Boli", "Bolą", "Boleje", "Bolała"],
        correct="Boli",
        grammar_slug="boli-mnie",
    ),
    AssessmentQuestion(
        id="pl-g-a2-009",
        skill="grammar",
        difficulty="A2",
        question="Utwórz tryb rozkazujący: ___ do sklepu!",
        options=["idziesz", "iść", "idź", "szedł"],
        correct="idź",
        grammar_slug="tryb-rozka",
    ),
    AssessmentQuestion(
        id="pl-g-a2-010",
        skill="grammar",
        difficulty="A2",
        question="Uzupełnij: Interesuję się ___.",
        options=["muzyka", "muzykę", "muzyce", "muzyką"],
        correct="muzyką",
        grammar_slug="narzednik",
    ),
    # ============================================================
    # A2 VOCABULARY (6 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-v-a2-001",
        skill="vocabulary",
        difficulty="A2",
        question="Które słowo oznacza miejsce, gdzie kupujemy lekarstwa?",
        options=["piekarnia", "apteka", "księgarnia", "poczta"],
        correct="apteka",
    ),
    AssessmentQuestion(
        id="pl-v-a2-002",
        skill="vocabulary",
        difficulty="A2",
        question="Który wyraz nie pasuje do pozostałych: spodnie, koszula, sukienka, ...?",
        options=["spodnie", "koszula", "sukienka", "parasol"],
        correct="parasol",
    ),
    AssessmentQuestion(
        id="pl-v-a2-003",
        skill="vocabulary",
        difficulty="A2",
        question="Które słowo oznacza dokument potrzebny do podróży pociągiem?",
        options=["bilet", "paragon", "rachunek", "recepta"],
        correct="bilet",
    ),
    AssessmentQuestion(
        id="pl-v-a2-004",
        skill="vocabulary",
        difficulty="A2",
        question="Które słowo jest przeciwieństwem słowa „chory”?",
        options=["zmęczony", "głodny", "zdrowy", "smutny"],
        correct="zdrowy",
    ),
    AssessmentQuestion(
        id="pl-v-a2-005",
        skill="vocabulary",
        difficulty="A2",
        question="Uzupełnij: Płacę kartą, a w sklepie dostaję ___.",
        options=["receptę", "paragon", "bilet", "przepis"],
        correct="paragon",
    ),
    AssessmentQuestion(
        id="pl-v-a2-006",
        skill="vocabulary",
        difficulty="A2",
        question="Który wyraz oznacza ubranie noszone zimą na dłoniach?",
        options=["rękawiczki", "skarpetki", "szalik", "czapka"],
        correct="rękawiczki",
    ),
    # ============================================================
    # A2 READING (5 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-r-a2-001",
        skill="reading",
        difficulty="A2",
        question=(
            "Tekst: Wczoraj Kasia była w restauracji. Zamówiła zupę pomidorową i pierogi, "
            "a potem wypiła kawę. Co zamówiła Kasia?"
        ),
        options=[
            "tylko kawę",
            "sałatkę i herbatę",
            "pierogi i sok",
            "zupę pomidorową i pierogi",
        ],
        correct="zupę pomidorową i pierogi",
    ),
    AssessmentQuestion(
        id="pl-r-a2-002",
        skill="reading",
        difficulty="A2",
        question=(
            "Tekst: Piotr wstał o szóstej, bo o ósmej miał pociąg do Gdańska. "
            "Musiał jeszcze kupić bilet. O której Piotr wstał?"
        ),
        options=["o ósmej", "o szóstej", "o siódmej", "o dziesiątej"],
        correct="o szóstej",
    ),
    AssessmentQuestion(
        id="pl-r-a2-003",
        skill="reading",
        difficulty="A2",
        question=(
            "Tekst: Od poniedziałku Marta pracuje w nowej firmie. Biuro znajduje się blisko "
            "dworca, więc jeździ tam tramwajem. Jak Marta dojeżdża do pracy?"
        ),
        options=["tramwajem", "samochodem", "pociągiem", "rowerem"],
        correct="tramwajem",
    ),
    AssessmentQuestion(
        id="pl-r-a2-004",
        skill="reading",
        difficulty="A2",
        question=(
            "Tekst: W sobotę padał deszcz, dlatego zostaliśmy w domu i oglądaliśmy film. "
            "Dopiero wieczorem wyszliśmy na krótki spacer. Dlaczego zostaliście w domu?"
        ),
        options=[
            "bo byliśmy chorzy",
            "bo nie mieliśmy czasu",
            "bo padał deszcz",
            "bo zabrakło prądu",
        ],
        correct="bo padał deszcz",
    ),
    AssessmentQuestion(
        id="pl-r-a2-005",
        skill="reading",
        difficulty="A2",
        question=(
            "Tekst: Na targu kupiłem kilogram jabłek, pół kilo pomidorów i bukiet kwiatów "
            "dla mamy. Za wszystko zapłaciłem czterdzieści złotych. Ile zapłaciłem?"
        ),
        options=[
            "czterdzieści złotych",
            "czternaście złotych",
            "czterysta złotych",
            "cztery złote",
        ],
        correct="czterdzieści złotych",
    ),
    # ============================================================
    # B1 GRAMMAR (10 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-g-b1-001",
        skill="grammar",
        difficulty="B1",
        question="Uzupełnij tak, aby podkreślić zakończenie czynności: Wczoraj ___ całą książkę.",
        options=["przeczytałem", "czytałem", "czytam", "przeczytam"],
        correct="przeczytałem",
        grammar_slug="aspekt-pary",
    ),
    AssessmentQuestion(
        id="pl-g-b1-002",
        skill="grammar",
        difficulty="B1",
        question="Uzupełnij: To jest kolega, ___ poznałem na kursie.",
        options=["który", "któremu", "którego", "którym"],
        correct="którego",
        grammar_slug="zdania-wzgledne",
    ),
    AssessmentQuestion(
        id="pl-g-b1-003",
        skill="grammar",
        difficulty="B1",
        question="Uzupełnij: Ten film, ___ widziałem wczoraj, był świetny.",
        options=["którego", "którym", "któremu", "który"],
        correct="który",
        grammar_slug="zaimki-wzgledne",
    ),
    AssessmentQuestion(
        id="pl-g-b1-004",
        skill="grammar",
        difficulty="B1",
        question="Uzupełnij: List ___ wczoraj przez sekretarkę.",
        options=["napisał", "został napisany", "był napisał", "został napisać"],
        correct="został napisany",
        grammar_slug="strona-bierna",
    ),
    AssessmentQuestion(
        id="pl-g-b1-005",
        skill="grammar",
        difficulty="B1",
        question="Która forma jest poprawnym imiesłowem przymiotnikowym biernym od „zamknąć”?",
        options=["zamykany", "zamkniony", "zamknięty", "zamkający"],
        correct="zamknięty",
        grammar_slug="imieslow-przymiotnikowy",
    ),
    AssessmentQuestion(
        id="pl-g-b1-006",
        skill="grammar",
        difficulty="B1",
        question=(
            "Kolega zapytał mnie: „Gdzie mieszkasz?”. Relacjonuję jego pytanie o moje "
            "miejsce zamieszkania: Zapytał, gdzie ___."
        ),
        options=["mieszkam", "mieszkasz", "mieszka", "mieszkamy"],
        correct="mieszkam",
        grammar_slug="mowa-zalezna",
    ),
    AssessmentQuestion(
        id="pl-g-b1-007",
        skill="grammar",
        difficulty="B1",
        question="Uzupełnij w pierwszej osobie obu członów: Gdybym miał czas, ___ do kina.",
        options=["poszedłem", "pójdę", "poszedłbyś", "poszedłbym"],
        correct="poszedłbym",
        grammar_slug="tryb-warunkowy-zdania",
    ),
    AssessmentQuestion(
        id="pl-g-b1-008",
        skill="grammar",
        difficulty="B1",
        question="Wskaż przyczynę mojego spóźnienia: Spóźniłem się, ___ autobus się spóźnił.",
        options=["dlatego", "ponieważ", "więc", "mimo że"],
        correct="ponieważ",
        grammar_slug="zdania-przyczynowe",
    ),
    AssessmentQuestion(
        id="pl-g-b1-009",
        skill="grammar",
        difficulty="B1",
        question="Który spójnik wyraża przeciwieństwo?",
        options=["oraz", "więc", "ponieważ", "ale"],
        correct="ale",
        grammar_slug="spojniki",
    ),
    AssessmentQuestion(
        id="pl-g-b1-010",
        skill="grammar",
        difficulty="B1",
        question="Uzupełnij, wskazując, że zakupy zakończyły się przed powrotem: "
        "___ zakupy, wróciłem do domu.",
        options=["Robiąc", "Zrobić", "Zrobiwszy", "Zrobiony"],
        correct="Zrobiwszy",
        grammar_slug="imieslow-przyslowkowy",
    ),
    # ============================================================
    # B1 VOCABULARY (6 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-v-b1-001",
        skill="vocabulary",
        difficulty="B1",
        question="Które słowo oznacza osobę, która kieruje zespołem w firmie?",
        options=["pracownik", "klient", "kierownik", "stażysta"],
        correct="kierownik",
    ),
    AssessmentQuestion(
        id="pl-v-b1-002",
        skill="vocabulary",
        difficulty="B1",
        question="Który wyraz opisuje bardzo silny wiatr?",
        options=["mgła", "mróz", "upał", "wichura"],
        correct="wichura",
    ),
    AssessmentQuestion(
        id="pl-v-b1-003",
        skill="vocabulary",
        difficulty="B1",
        question="Które wyjaśnienie odpowiada słowu „wypadek”?",
        options=[
            "nagłe zdarzenie, w którym ktoś ucierpiał",
            "planowany urlop",
            "spotkanie rodzinne",
            "zakup biletu",
        ],
        correct="nagłe zdarzenie, w którym ktoś ucierpiał",
    ),
    AssessmentQuestion(
        id="pl-v-b1-004",
        skill="vocabulary",
        difficulty="B1",
        question="Które słowo jest przeciwieństwem słowa „spokojny”?",
        options=["cichy", "zdenerwowany", "uprzejmy", "zmęczony"],
        correct="zdenerwowany",
    ),
    AssessmentQuestion(
        id="pl-v-b1-005",
        skill="vocabulary",
        difficulty="B1",
        question="Uzupełnij: Muszę naładować ___.",
        options=["okno", "krzesło", "parasol", "telefon"],
        correct="telefon",
    ),
    AssessmentQuestion(
        id="pl-v-b1-006",
        skill="vocabulary",
        difficulty="B1",
        question="Który wyraz oznacza miejsce, gdzie można wysłać list?",
        options=["apteka", "piekarnia", "poczta", "biblioteka"],
        correct="poczta",
    ),
    # ============================================================
    # B1 READING (5 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-r-b1-001",
        skill="reading",
        difficulty="B1",
        question=(
            "Tekst: Odkąd Anna przeprowadziła się do Gdańska, dojeżdża do pracy pociągiem. "
            "Podróż zajmuje jej czterdzieści minut, ale woli ją od stania w korkach. "
            "Dlaczego Anna wybrała pociąg?"
        ),
        options=[
            "bo jest taniej",
            "bo nie lubi korków",
            "bo nie ma samochodu",
            "bo pociąg jest szybszy od samolotu",
        ],
        correct="bo nie lubi korków",
    ),
    AssessmentQuestion(
        id="pl-r-b1-002",
        skill="reading",
        difficulty="B1",
        question=(
            "Tekst: Firma wprowadziła pracę zdalną dwa dni w tygodniu. Pracownicy mogą "
            "zostać w domu w poniedziałki i piątki, ale muszą być dostępni online. "
            "Co firma pozwoliła pracownikom robić?"
        ),
        options=[
            "pracować krócej",
            "brać dodatkowe urlopy",
            "pracować wyłącznie w biurze",
            "pracować z domu w poniedziałki i piątki",
        ],
        correct="pracować z domu w poniedziałki i piątki",
    ),
    AssessmentQuestion(
        id="pl-r-b1-003",
        skill="reading",
        difficulty="B1",
        question=(
            "Tekst: Marek zapisał się na kurs gotowania, ponieważ chciał nauczyć się "
            "przyrządzać zdrowe posiłki. Zajęcia odbywają się raz w tygodniu, w czwartki. "
            "Po co Marek poszedł na kurs?"
        ),
        options=[
            "żeby poznać nowych ludzi",
            "żeby schudnąć przed wakacjami",
            "żeby nauczyć się gotować zdrowe posiłki",
            "żeby otworzyć restaurację",
        ],
        correct="żeby nauczyć się gotować zdrowe posiłki",
    ),
    AssessmentQuestion(
        id="pl-r-b1-004",
        skill="reading",
        difficulty="B1",
        question=(
            "Tekst: W Muzeum Narodowym do końca miesiąca można zobaczyć wystawę poświęconą "
            "polskiemu malarstwu XIX wieku. Wstęp w niedziele jest bezpłatny. "
            "Co można zobaczyć w muzeum?"
        ),
        options=[
            "wystawę polskiego malarstwa XIX wieku",
            "kolekcję starych samochodów",
            "wystawę fotografii współczesnej",
            "zbiór instrumentów muzycznych",
        ],
        correct="wystawę polskiego malarstwa XIX wieku",
    ),
    AssessmentQuestion(
        id="pl-r-b1-005",
        skill="reading",
        difficulty="B1",
        question=(
            "Tekst: Kasia zamówiła nową szafę przez internet. Sklep obiecał dostawę w ciągu "
            "pięciu dni roboczych, ale mebel dotarł dopiero po dwóch tygodniach. "
            "Jak długo Kasia czekała na szafę?"
        ),
        options=["pięć dni", "dwa tygodnie", "tydzień", "miesiąc"],
        correct="dwa tygodnie",
    ),
    # ============================================================
    # B2 GRAMMAR (10 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-g-b2-001",
        skill="grammar",
        difficulty="B2",
        question="Uzupełnij formą dokonaną opisującą jednorazowy skutek: "
        "Gdybyśmy byli wcześniej wyszli, ___ pociąg.",
        options=[
            "zdążymy na",
            "zdążyliśmy na",
            "zdążylibyśmy na",
            "zdążalibyśmy na",
        ],
        correct="zdążylibyśmy na",
        grammar_slug="tryb-warunkowy-hipotetyczny",
    ),
    AssessmentQuestion(
        id="pl-g-b2-002",
        skill="grammar",
        difficulty="B2",
        question="Uzupełnij spójnikiem wyrażającym przeciwstawienie: "
        "Nie lubi kawy, ___ herbatę pije codziennie.",
        options=["natomiast", "ponieważ", "dlatego", "więc"],
        correct="natomiast",
        grammar_slug="zdania-przeciwstawne",
    ),
    AssessmentQuestion(
        id="pl-g-b2-003",
        skill="grammar",
        difficulty="B2",
        question="Która partykuła wyraża przypuszczenie?",
        options=["nie", "chyba", "się", "że"],
        correct="chyba",
        grammar_slug="partykuly-modalne",
    ),
    AssessmentQuestion(
        id="pl-g-b2-004",
        skill="grammar",
        difficulty="B2",
        question=("Wybierz poprawną nominalizację zdania: „Rząd postanowił zwiększyć podatki”."),
        options=[
            "rząd decyduje o podatkach",
            "podatki zostały zwiększone przez rząd",
            "zwiększanie podatków przez decyzję",
            "decyzja rządu o zwiększeniu podatków",
        ],
        correct="decyzja rządu o zwiększeniu podatków",
        grammar_slug="nominalizacja",
    ),
    AssessmentQuestion(
        id="pl-g-b2-005",
        skill="grammar",
        difficulty="B2",
        question="Które zdanie jest poprawną konstrukcją bierną od „Naukowcy przebadali próbki”?",
        options=[
            "Próbki przebadały naukowców.",
            "Próbki były przebadać przez naukowców.",
            "Próbki zostały przebadane przez naukowców.",
            "Naukowcy zostały przebadane przez próbki.",
        ],
        correct="Próbki zostały przebadane przez naukowców.",
        grammar_slug="strona-bierna-zaawansowana",
    ),
    AssessmentQuestion(
        id="pl-g-b2-006",
        skill="grammar",
        difficulty="B2",
        question="Uzupełnij konstrukcją bezosobową: ___ tu palić.",
        options=["Zabrania", "Zabrania się", "Zabronione", "Zabrania się jest"],
        correct="Zabrania się",
        grammar_slug="konstrukcje-bezosobowe-zaawansowane",
    ),
    AssessmentQuestion(
        id="pl-g-b2-007",
        skill="grammar",
        difficulty="B2",
        question="Uzupełnij, wyrażając równoczesność realizacji i napotykania trudności: "
        "___ nowy projekt, zespół napotkał wiele trudności.",
        options=["Realizując", "Zrealizowawszy", "Realizowany", "Realizować"],
        correct="Realizując",
        grammar_slug="imieslowy-zaawansowane",
    ),
    AssessmentQuestion(
        id="pl-g-b2-008",
        skill="grammar",
        difficulty="B2",
        question="Wybierz poprawnie zbudowane zdanie z dwoma zdaniami podrzędnymi.",
        options=[
            "Wiem, że przyjdziesz, kiedy skończysz, pracę.",
            "Wiem że, przyjdziesz gdy, skończysz pracę.",
            "Wiem, przyjdziesz, że gdy skończysz pracę.",
            "Wiem, że przyjdziesz, gdy skończysz pracę.",
        ],
        correct="Wiem, że przyjdziesz, gdy skończysz pracę.",
        grammar_slug="zdania-wielokrotne",
    ),
    AssessmentQuestion(
        id="pl-g-b2-009",
        skill="grammar",
        difficulty="B2",
        question=(
            "Nauczyciel zapytał nas: „Czy odrobiliście zadanie?”. "
            "Relacjonuję pytanie o zadanie naszej grupy w pierwszej osobie liczby mnogiej: "
            "Nauczyciel zapytał, czy ___ zadanie."
        ),
        options=["odrobiliście", "odrobimy", "odrobiliśmy", "odrabialiście"],
        correct="odrobiliśmy",
        grammar_slug="mowa-zalezna-zaawansowana",
    ),
    AssessmentQuestion(
        id="pl-g-b2-010",
        skill="grammar",
        difficulty="B2",
        question="Które zdanie zawiera elipsę czasownika?",
        options=[
            "Anna poszła do kina, a Piotr do teatru.",
            "Anna i Piotr poszli do kina.",
            "Anna poszła do kina, a Piotr poszedł do teatru.",
            "Anna poszła do kina, ponieważ Piotr chciał iść do teatru.",
        ],
        correct="Anna poszła do kina, a Piotr do teatru.",
        grammar_slug="elipsa",
    ),
    # ============================================================
    # B2 VOCABULARY (6 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-v-b2-001",
        skill="vocabulary",
        difficulty="B2",
        question="Które słowo oznacza wzrost cen i spadek wartości pieniądza?",
        options=["deflacja", "recesja", "dotacja", "inflacja"],
        correct="inflacja",
    ),
    AssessmentQuestion(
        id="pl-v-b2-002",
        skill="vocabulary",
        difficulty="B2",
        question="Który wyraz jest synonimem słowa „niezbędny”?",
        options=["zbędny", "konieczny", "dodatkowy", "wątpliwy"],
        correct="konieczny",
    ),
    AssessmentQuestion(
        id="pl-v-b2-003",
        skill="vocabulary",
        difficulty="B2",
        question="Co oznacza wyrażenie „wziąć coś pod uwagę”?",
        options=["odrzucić coś", "zapomnieć o czymś", "uwzględnić coś", "ukryć coś"],
        correct="uwzględnić coś",
    ),
    AssessmentQuestion(
        id="pl-v-b2-004",
        skill="vocabulary",
        difficulty="B2",
        question="Które słowo jest przeciwieństwem słowa „obniżyć”?",
        options=["podwyższyć", "zmniejszyć", "ograniczyć", "zlikwidować"],
        correct="podwyższyć",
    ),
    AssessmentQuestion(
        id="pl-v-b2-005",
        skill="vocabulary",
        difficulty="B2",
        question="Które słowo oznacza oficjalną prośbę skierowaną do instytucji?",
        options=["wyrok", "umowa", "rachunek", "wniosek"],
        correct="wniosek",
    ),
    AssessmentQuestion(
        id="pl-v-b2-006",
        skill="vocabulary",
        difficulty="B2",
        question="Który wyraz jest przeciwieństwem słowa „korzyść”?",
        options=["zaleta", "strata", "zysk", "wartość"],
        correct="strata",
    ),
    # ============================================================
    # B2 READING (5 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-r-b2-001",
        skill="reading",
        difficulty="B2",
        question=(
            "Tekst: Z badania przeprowadzonego wśród pracowników biurowych wynika, że ponad "
            "połowa z nich chętniej pracowałaby zdalnie przez trzy dni w tygodniu. "
            "Najczęściej wymienianym powodem jest czas zaoszczędzony na dojazdach, a nie "
            "sama efektywność pracy. Czego dotyczy najczęściej podawany powód?"
        ),
        options=[
            "wyższej efektywności",
            "lepszych relacji z zespołem",
            "wyższego wynagrodzenia",
            "czasu zaoszczędzonego na dojazdach",
        ],
        correct="czasu zaoszczędzonego na dojazdach",
    ),
    AssessmentQuestion(
        id="pl-r-b2-002",
        skill="reading",
        difficulty="B2",
        question=(
            "Tekst: Nowa ustawa nakłada na producentów obowiązek oznaczania opakowań "
            "informacją o możliwości recyklingu. Przepisy wejdą w życie dopiero za rok, "
            "aby firmy zdążyły dostosować linie produkcyjne. "
            "Dlaczego wprowadzono roczne opóźnienie?"
        ),
        options=[
            "bo ustawa została odrzucona",
            "bo zabrakło funduszy",
            "aby firmy zdążyły dostosować produkcję",
            "aby obniżyć ceny opakowań",
        ],
        correct="aby firmy zdążyły dostosować produkcję",
    ),
    AssessmentQuestion(
        id="pl-r-b2-003",
        skill="reading",
        difficulty="B2",
        question=(
            "Tekst: Autor artykułu przekonuje, że dostęp do darmowej edukacji online nie "
            "wyrównuje szans automatycznie. Jego zdaniem kluczowe pozostaje wsparcie "
            "nauczyciela, którego nie zastąpią nagrania wideo. Jaki jest główny argument autora?"
        ),
        options=[
            "nauczyciel jest nie do zastąpienia",
            "nagrania wideo są zbyt drogie",
            "edukacja online jest nieskuteczna",
            "darmowe kursy psują rynek",
        ],
        correct="nauczyciel jest nie do zastąpienia",
    ),
    AssessmentQuestion(
        id="pl-r-b2-004",
        skill="reading",
        difficulty="B2",
        question=(
            "Tekst: Podczas gdy starsi mieszkańcy osiedla domagali się budowy parkingu, "
            "młodsi proponowali plac zabaw. Ostatecznie rada miasta zdecydowała się "
            "przeznaczyć działkę na zieleniec z ławkami, co spotkało się z krytyką obu grup. "
            "Jaka decyzja zapadła?"
        ),
        options=[
            "budowa parkingu",
            "urządzenie zieleńca",
            "budowa placu zabaw",
            "sprzedaż działki",
        ],
        correct="urządzenie zieleńca",
    ),
    AssessmentQuestion(
        id="pl-r-b2-005",
        skill="reading",
        difficulty="B2",
        question=(
            "Tekst: W raporcie zwrócono uwagę, że rosnące ceny mieszkań wynikają nie tylko "
            "z drożejących materiałów, lecz także z ograniczonej podaży gruntów w centrach "
            "miast. Analitycy zalecają więc inwestycje w transport publiczny na obrzeżach. "
            "Co analitycy zalecają?"
        ),
        options=[
            "zamrożenie cen mieszkań",
            "dotacje dla deweloperów",
            "inwestycje w transport na obrzeżach",
            "sprzedaż gruntów miejskich",
        ],
        correct="inwestycje w transport na obrzeżach",
    ),
    # ============================================================
    # C1 GRAMMAR (10 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-g-c1-001",
        skill="grammar",
        difficulty="C1",
        question="Która forma jest najbardziej odpowiednia w oficjalnym piśmie do urzędu?",
        options=[
            "Chcę, żebyście to załatwili.",
            "Uprzejmie proszę o rozpatrzenie wniosku.",
            "Dajcie znać, co z tym.",
            "No to jak będzie?",
        ],
        correct="Uprzejmie proszę o rozpatrzenie wniosku.",
        grammar_slug="styl-formalny",
    ),
    AssessmentQuestion(
        id="pl-g-c1-002",
        skill="grammar",
        difficulty="C1",
        question=(
            "Która wersja najlepiej przekształca zdanie „Po tym, jak komisja przeanalizowała "
            "dokumenty, podjęto decyzję” w styl nominalny?"
        ),
        options=[
            "Po przeanalizowaniu dokumentów przez komisję podjęto decyzję.",
            "Komisja przeanalizowała dokumenty i podjęła decyzję.",
            "Dokumenty przeanalizowano, potem decyzja.",
            "Komisja, analizując dokumenty, decyduje.",
        ],
        correct="Po przeanalizowaniu dokumentów przez komisję podjęto decyzję.",
        grammar_slug="nominalizacja-zaawansowana",
    ),
    AssessmentQuestion(
        id="pl-g-c1-003",
        skill="grammar",
        difficulty="C1",
        question="Który środek stylistyczny występuje w zdaniu „Miasto spało, a ulice milczały”?",
        options=["hiperbola", "porównanie", "personifikacja", "apostrofa"],
        correct="personifikacja",
        grammar_slug="srodki-stylistyczne",
    ),
    AssessmentQuestion(
        id="pl-g-c1-004",
        skill="grammar",
        difficulty="C1",
        question=(
            "Który zabieg składniowy polega na celowym pominięciu spójników "
            "między współrzędnymi członami?"
        ),
        options=["elipsa", "inwersja", "parenteza", "asyndeton"],
        correct="asyndeton",
        grammar_slug="skladnia-retoryczna",
    ),
    AssessmentQuestion(
        id="pl-g-c1-005",
        skill="grammar",
        difficulty="C1",
        question="Który termin oznacza zjawisko zmniejszania się liczby ludności?",
        options=["emigracja", "depopulacja", "urbanizacja", "migracja"],
        correct="depopulacja",
        grammar_slug="terminologia",
    ),
    AssessmentQuestion(
        id="pl-g-c1-006",
        skill="grammar",
        difficulty="C1",
        question="Które zdanie ma formę definicji, a nie opisu?",
        options=[
            "Termometr wisi na ścianie w kuchni.",
            "Termometr, który kupiłem, jest czerwony.",
            "Termometr to przyrząd służący do pomiaru temperatury.",
            "Termometr służy, bo mierzy ciepło.",
        ],
        correct="Termometr to przyrząd służący do pomiaru temperatury.",
        grammar_slug="definiowanie",
    ),
    AssessmentQuestion(
        id="pl-g-c1-007",
        skill="grammar",
        difficulty="C1",
        question="Który przyimek jest poprawny w konstrukcji urzędowej „wystąpić ___ wnioskiem”?",
        options=["z", "na", "po", "o"],
        correct="z",
        grammar_slug="przyimki-specjalistyczne",
    ),
    AssessmentQuestion(
        id="pl-g-c1-008",
        skill="grammar",
        difficulty="C1",
        question=(
            "Redaktor porównuje odpowiedzi „Nie przeczytałem raportu” i „Nie czytałem "
            "raportu”, odnoszące się do tego samego okresu. Która interpretacja zachowuje "
            "różnicę aspektu, nie dopisując informacji o przebiegu lektury?"
        ),
        options=[
            "Pierwsza odpowiedź potwierdza rozpoczęcie lektury, druga temu zaprzecza.",
            "Obie odpowiedzi zaprzeczają wyłącznie ukończeniu lektury.",
            "Pierwsza odpowiedź zaprzecza zamiarowi lektury, druga jej ukończeniu.",
            "Pierwsza zaprzecza ukończeniu lektury, druga samej czynności czytania.",
        ],
        correct="Pierwsza zaprzecza ukończeniu lektury, druga samej czynności czytania.",
        grammar_slug="aspekt-niuanse",
    ),
    AssessmentQuestion(
        id="pl-g-c1-009",
        skill="grammar",
        difficulty="C1",
        question="Co znaczy związek frazeologiczny „mieć węża w kieszeni”?",
        options=["być bogatym", "być skąpym", "być odważnym", "być zmęczonym"],
        correct="być skąpym",
        grammar_slug="zwroty-idiomatyczne",
    ),
    AssessmentQuestion(
        id="pl-g-c1-010",
        skill="grammar",
        difficulty="C1",
        question=(
            "W komunikacie „Zarząd odrzucił wniosek po konsultacjach” redaktor zastąpił "
            "zdanie wersją „Wniosek został odrzucony po konsultacjach”. Jak zmienia się "
            "sposób przedstawienia tej samej decyzji?"
        ),
        options=[
            "Wniosek staje się tematem zdania, a wykonawca decyzji nie zostaje nazwany.",
            "Decyzja staje się mniej ostateczna, a konsultacje nadal mogą zmienić jej wynik.",
            "Konsultacje zostają przedstawione jako przyczyna decyzji, a nie jej tło czasowe.",
            "Odpowiedzialność za decyzję zostaje przypisana uczestnikom konsultacji.",
        ],
        correct="Wniosek staje się tematem zdania, a wykonawca decyzji nie zostaje nazwany.",
        grammar_slug="strona-bierna-styl",
    ),
    # ============================================================
    # C1 VOCABULARY (6 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-v-c1-001",
        skill="vocabulary",
        difficulty="C1",
        question="Które słowo jest synonimem słowa „nieuchronny”?",
        options=["zbędny", "odwracalny", "nieunikniony", "niepewny"],
        correct="nieunikniony",
    ),
    AssessmentQuestion(
        id="pl-v-c1-002",
        skill="vocabulary",
        difficulty="C1",
        question="Co oznacza słowo „bezstronny”?",
        options=[
            "oceniający bez uprzedzeń",
            "bardzo surowy",
            "pozbawiony celu",
            "mało dokładny",
        ],
        correct="oceniający bez uprzedzeń",
    ),
    AssessmentQuestion(
        id="pl-v-c1-003",
        skill="vocabulary",
        difficulty="C1",
        question="Które słowo jest przeciwieństwem słowa „zaniechać”?",
        options=["porzucić", "odłożyć", "przerwać", "podjąć"],
        correct="podjąć",
    ),
    AssessmentQuestion(
        id="pl-v-c1-004",
        skill="vocabulary",
        difficulty="C1",
        question="Który wyraz oznacza krótkie podsumowanie na końcu tekstu?",
        options=["wstęp", "konkluzja", "przypis", "tytuł"],
        correct="konkluzja",
    ),
    AssessmentQuestion(
        id="pl-v-c1-005",
        skill="vocabulary",
        difficulty="C1",
        question=(
            "Autor stawia otwarte pytania, by skłonić odbiorcę do samodzielnego namysłu. "
            "Uzupełnij zgodnie z tą intencją: Autor ___ czytelnika do refleksji."
        ),
        options=["odradza", "zniechęca", "zachęca", "zabrania"],
        correct="zachęca",
    ),
    AssessmentQuestion(
        id="pl-v-c1-006",
        skill="vocabulary",
        difficulty="C1",
        question="Który wyraz jest neutralnym stylistycznie odpowiednikiem słowa „facet”?",
        options=["mężczyzna", "typek", "koleś", "gość"],
        correct="mężczyzna",
    ),
    # ============================================================
    # C1 READING (4 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-r-c1-001",
        skill="reading",
        difficulty="C1",
        question=(
            "Tekst: Uczelnia zastąpiła egzaminy ustne testami automatycznymi. Władze "
            "przedstawiają skrócenie czasu oceniania jako dowód powodzenia reformy. "
            "Autor komentarza przyznaje, że wyniki są teraz dostępne szybciej, a wszyscy "
            "zdający podlegają tym samym kryteriom. Zauważa jednak, że w programie kursu "
            "nadal figuruje obrona własnego stanowiska, podczas gdy student wybiera tylko "
            "gotowe odpowiedzi. Nie domaga się przywrócenia dawnej formy za wszelką cenę; "
            "pyta, co właściwie ma potwierdzać ocena. Które założenie władz podważa?"
        ),
        options=[
            "Jednakowe kryteria oceniania mogą ograniczać uznaniowość egzaminatorów.",
            "Sprawniejsza organizacja egzaminu wystarcza, by uznać go za trafną ocenę umiejętności.",
            "Obronę własnego stanowiska można oceniać inaczej niż podczas egzaminu ustnego.",
            "Szybsze udostępnianie wyników jest korzyścią z punktu widzenia studentów.",
        ],
        correct="Sprawniejsza organizacja egzaminu wystarcza, by uznać go za trafną ocenę umiejętności.",
    ),
    AssessmentQuestion(
        id="pl-r-c1-002",
        skill="reading",
        difficulty="C1",
        question=(
            "Tekst: Łatwo powiedzieć, że o wpływie platform społecznościowych decyduje "
            "wyłącznie rozsądek użytkownika. Owszem, można wyłączyć powiadomienia, lecz "
            "ustawienia domyślne zachęcają do ciągłego powracania, a dotarcie do opcji "
            "ograniczających ten mechanizm wymaga wysiłku. Nie wynika z tego, że odbiorca "
            "jest bezwolny ani że każda platforma działa tak samo. Trudno jednak uznać "
            "wybór za całkowicie niezależny od warunków, w których jest dokonywany. "
            "Jaką funkcję pełni przyznanie, że można wyłączyć powiadomienia?"
        ),
        options=[
            "Uznaje część racji przeciwnego stanowiska przed ograniczeniem jego zasięgu.",
            "Przenosi całą odpowiedzialność z projektantów platform na ich użytkowników.",
            "Podważa znaczenie ustawień domyślnych dla sposobu korzystania z platform.",
            "Uzasadnia podział użytkowników na rozsądnych i niezdolnych do samodzielnego wyboru.",
        ],
        correct="Uznaje część racji przeciwnego stanowiska przed ograniczeniem jego zasięgu.",
    ),
    AssessmentQuestion(
        id="pl-r-c1-003",
        skill="reading",
        difficulty="C1",
        question=(
            "Tekst: Po cyfryzacji urzędu wnioski są rejestrowane szybciej, ale liczba "
            "załączników wzrosła. Urzędnicy przedstawiają ten wzrost jako nieunikniony "
            "skutek dostosowania procedur do wymogów unijnych, choć sami przyznają, że "
            "kilka formularzy powiela te same dane i można je połączyć bez naruszenia "
            "przepisów. Autor nie kwestionuje potrzeby dostosowania procedur; zauważa "
            "jedynie, że przeniesienie dokumentów na ekran nie rozstrzyga, ile powinno "
            "ich być. Jaką rolę odgrywa zdanie wprowadzone przez „choć”?"
        ),
        options=[
            "Podważa informację, że cyfryzacja przyspieszyła rejestrowanie wniosków.",
            "Wskazuje, że ograniczenie liczby formularzy wymaga zmiany prawa unijnego.",
            "Osłabia tezę, że wzrost liczby załączników był w całości nieunikniony.",
            "Uzasadnia konieczność powielania danych w celu zachowania zgodności z prawem.",
        ],
        correct="Osłabia tezę, że wzrost liczby załączników był w całości nieunikniony.",
    ),
    AssessmentQuestion(
        id="pl-r-c1-004",
        skill="reading",
        difficulty="C1",
        question=(
            "Tekst: Obaj uczestnicy debaty domagają się lepszych dowodów. Pierwszy "
            "wskazuje, jakie wyniki skłoniłyby go do zmiany zdania. Drugi po każdej "
            "odpowiedzi ustanawia nowy warunek, którego wcześniej nie wymieniał. "
            "Autor nie twierdzi, że pierwsze dostępne badanie musi kończyć dyskusję: "
            "nowe zastrzeżenie może być zasadne. Ostrzega jednak przed stanowiskiem, "
            "którego żadna możliwa obserwacja nie mogłaby podważyć, choć jego zwolennik "
            "nazywa je sceptycyzmem. Jakie kryterium rozróżnienia wynika z tekstu?"
        ),
        options=[
            "Sceptycyzm wymaga zaakceptowania pierwszego badania spełniającego normy naukowe.",
            "O zasadności stanowiska decyduje liczba zgłoszonych zastrzeżeń metodologicznych.",
            "Każde nowe zastrzeżenie po otrzymaniu odpowiedzi świadczy o odrzucaniu dowodów.",
            "Sceptycyzm dopuszcza zmianę stanowiska pod wpływem dowodów, a nie tylko ich żąda.",
        ],
        correct="Sceptycyzm dopuszcza zmianę stanowiska pod wpływem dowodów, a nie tylko ich żąda.",
    ),
    # ============================================================
    # C2 GRAMMAR (10 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-g-c2-001",
        skill="grammar",
        difficulty="C2",
        question="Która konstrukcja z „to” wyróżnia Annę jako autorkę listu, a nie inną osobę?",
        options=[
            "Anna napisała to ten list.",
            "To ten list Anna napisała to.",
            "To Anna napisała ten list.",
            "To ten list napisała Anna, nie tamten.",
        ],
        correct="To Anna napisała ten list.",
        grammar_slug="skladnia-emfatyczna",
    ),
    AssessmentQuestion(
        id="pl-g-c2-002",
        skill="grammar",
        difficulty="C2",
        question="Co znaczy archaizm „jeno”?",
        options=["już", "bardzo", "zaraz", "tylko"],
        correct="tylko",
        grammar_slug="formy-archaiczne",
    ),
    AssessmentQuestion(
        id="pl-g-c2-003",
        skill="grammar",
        difficulty="C2",
        question="Uzupełnij: Umowa wchodzi w życie z dniem ___.",
        options=["podpisania", "podpisać", "podpisany", "podpisanie"],
        correct="podpisania",
        grammar_slug="jezyk-prawny",
    ),
    AssessmentQuestion(
        id="pl-g-c2-004",
        skill="grammar",
        difficulty="C2",
        question=(
            "W pilotażu obejmującym ochotników z jednej placówki zaobserwowano poprawę "
            "po wprowadzeniu programu, ale nie zastosowano grupy kontrolnej. Który wniosek "
            "zachowuje wynik obserwacji i ogranicza siłę twierdzenia do zakresu danych?"
        ),
        options=[
            "Wyniki potwierdzają skuteczność programu, choć wielkość efektu wymaga dalszych badań.",
            "Odnotowano poprawę w badanej grupie, lecz nie można przypisać jej samemu programowi.",
            "Brak grupy kontrolnej oznacza, że nie można stwierdzić nawet zaobserwowanej poprawy.",
            "Poprawa pozwala uogólnić wynik na inne placówki, o ile ich uczestnicy są ochotnikami.",
        ],
        correct="Odnotowano poprawę w badanej grupie, lecz nie można przypisać jej samemu programowi.",
        grammar_slug="jezyk-naukowy",
    ),
    AssessmentQuestion(
        id="pl-g-c2-005",
        skill="grammar",
        difficulty="C2",
        question=(
            "Podczas posiedzenia przewodnicząca mówi: „Nie przesądzałabym jeszcze, że "
            "projekt jest niewykonalny”. Która parafraza zachowuje funkcję trybu warunkowego "
            "oraz zakres zastrzeżenia, nie wzmacniając stanowiska mówiącej?"
        ),
        options=[
            "Przewodnicząca uznaje projekt za wykonalny, lecz odkłada ogłoszenie tej oceny.",
            "Przewodnicząca uznaje projekt za niewykonalny, lecz łagodzi sposób przekazania oceny.",
            "Przewodnicząca łagodzi sprzeciw wobec przedwczesnego uznania projektu za niewykonalny.",
            "Przewodnicząca uzależnia sprzeciw wobec oceny projektu od spełnienia warunku.",
        ],
        correct=(
            "Przewodnicząca łagodzi sprzeciw wobec przedwczesnego uznania projektu za niewykonalny."
        ),
        grammar_slug="tryby-mowione",
    ),
    AssessmentQuestion(
        id="pl-g-c2-006",
        skill="grammar",
        difficulty="C2",
        question=(
            "Porównaj „Nie zamykaj tych drzwi — czekamy na gości” z „Tylko nie zamknij "
            "tych drzwi przez nieuwagę — klucz został w środku”. Które wyjaśnienie "
            "najtrafniej wiąże aspekt z funkcją wypowiedzi w podanych kontekstach?"
        ),
        options=[
            "Niedokonany służy zakazowi, a dokonany ostrzega przed niepożądanym rezultatem.",
            "Niedokonany służy uprzejmej prośbie, a dokonany zawsze nadaje wypowiedzi ton rozkazu.",
            "Niedokonany wskazuje na wielokrotne zamykanie, a dokonany na jednorazową czynność.",
            "Niedokonany zaprzecza zamiarowi zamknięcia, a dokonany zaprzecza jego wykonaniu.",
        ],
        correct="Niedokonany służy zakazowi, a dokonany ostrzega przed niepożądanym rezultatem.",
        grammar_slug="aspekt-mistrzostwo",
    ),
    AssessmentQuestion(
        id="pl-g-c2-007",
        skill="grammar",
        difficulty="C2",
        question=(
            "Które sformułowanie jest kalką z języka angielskiego krytykowaną "
            "w starannej polszczyźnie?"
        ),
        options=["rozwiązać problem", "poruszyć problem", "opisać problem", "adresować problem"],
        correct="adresować problem",
        grammar_slug="kalki-jezykowe",
    ),
    AssessmentQuestion(
        id="pl-g-c2-008",
        skill="grammar",
        difficulty="C2",
        question=(
            "Które pojęcie oznacza brak pełnego odpowiednika leksykalnego " "w języku docelowym?"
        ),
        options=["kalka", "luka leksykalna", "transliteracja", "ekwiwalent"],
        correct="luka leksykalna",
        grammar_slug="ekwiwalencja",
    ),
    AssessmentQuestion(
        id="pl-g-c2-009",
        skill="grammar",
        difficulty="C2",
        question=(
            "Który zabieg retoryczny polega na zwróceniu się do osoby nieobecnej "
            "lub do przedmiotu?"
        ),
        options=["anafora", "elipsa", "peryfraza", "apostrofa"],
        correct="apostrofa",
        grammar_slug="retoryka",
    ),
    AssessmentQuestion(
        id="pl-g-c2-010",
        skill="grammar",
        difficulty="C2",
        question=(
            "Po pytaniu kolegi „Nie zaczekasz na Martę?” rozmówca odpowiada: "
            "„No przecież na nią czekam”. Co wnosi połączenie „no przecież” "
            "w tej wymianie, poza samą informacją o czekaniu?"
        ),
        options=[
            "Przedstawia czekanie jako ustępstwo, na które rozmówca zgadza się dopiero teraz.",
            "Sygnalizuje niepewność, czy oczekiwana osoba rzeczywiście ma na imię Marta.",
            "Koryguje sugestię pytającego, przedstawiając czekanie jako fakt, który powinien znać.",
            "Ogranicza deklarację czekania warunkiem, że Marta przyjdzie wkrótce.",
        ],
        correct=(
            "Koryguje sugestię pytającego, przedstawiając czekanie jako fakt, który powinien znać."
        ),
        grammar_slug="jezyk-potoczny",
    ),
    # ============================================================
    # C2 VOCABULARY (6 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-v-c2-001",
        skill="vocabulary",
        difficulty="C2",
        question="Które słowo jest synonimem słowa „uboczny”?",
        options=["poboczny", "główny", "zasadniczy", "konieczny"],
        correct="poboczny",
    ),
    AssessmentQuestion(
        id="pl-v-c2-002",
        skill="vocabulary",
        difficulty="C2",
        question="Co oznacza słowo „próżność”?",
        options=[
            "skromność",
            "pracowitość",
            "nadmierna duma z siebie",
            "nieśmiałość",
        ],
        correct="nadmierna duma z siebie",
    ),
    AssessmentQuestion(
        id="pl-v-c2-003",
        skill="vocabulary",
        difficulty="C2",
        question="Które słowo jest przeciwieństwem słowa „skrupulatny”?",
        options=["dokładny", "niedbały", "sumienny", "staranny"],
        correct="niedbały",
    ),
    AssessmentQuestion(
        id="pl-v-c2-004",
        skill="vocabulary",
        difficulty="C2",
        question="Co oznacza słowo „zgryźliwy”?",
        options=["pogodny", "nieśmiały", "obojętny", "ironiczny i uszczypliwy"],
        correct="ironiczny i uszczypliwy",
    ),
    AssessmentQuestion(
        id="pl-v-c2-005",
        skill="vocabulary",
        difficulty="C2",
        question="Które słowo należy do najwyższego rejestru i jest najbardziej książkowe?",
        options=["iść", "gnać", "podążać", "lecieć"],
        correct="podążać",
    ),
    AssessmentQuestion(
        id="pl-v-c2-006",
        skill="vocabulary",
        difficulty="C2",
        question="Co oznacza słowo „niecny”?",
        options=[
            "podły i nikczemny",
            "odważny i śmiały",
            "bogaty i wpływowy",
            "uczciwy i prawy",
        ],
        correct="podły i nikczemny",
    ),
    # ============================================================
    # C2 READING (4 questions)
    # ============================================================
    AssessmentQuestion(
        id="pl-r-c2-001",
        skill="reading",
        difficulty="C2",
        question=(
            "Tekst: Trudno odmówić autorowi erudycji: przypisy prowadzą czytelnika przez "
            "archiwa, do których mało kto zagląda. Kłopot zaczyna się nie tam, gdzie "
            "materiału brakuje, lecz tam, gdzie przestaje on stawiać opór opowieści. "
            "Świadectwa niezgodne z tezą trafiają do przypisów jako osobliwości epoki, "
            "zgodne zaś przemawiają w imieniu całego pokolenia. Być może teza dałaby się "
            "obronić; przedstawiona argumentacja nie pozwala jednak odróżnić jej "
            "od założenia, według którego dobrano wagę świadectw. Jaką funkcję pełni "
            "pochwała erudycji w toku tej recenzji?"
        ),
        options=[
            "Uzasadnia zaufanie do tezy mimo wskazanych uchybień w sposobie cytowania.",
            "Pozornie chwali autora, by ostatecznie zakwestionować autentyczność jego źródeł.",
            "Oddziela rozległość wiedzy od sposobu argumentowania, którego dotyczy krytyka.",
            "Przygotowuje odrzucenie tezy jako fałszywej na podstawie liczby pominiętych źródeł.",
        ],
        correct="Oddziela rozległość wiedzy od sposobu argumentowania, którego dotyczy krytyka.",
    ),
    AssessmentQuestion(
        id="pl-r-c2-002",
        skill="reading",
        difficulty="C2",
        question=(
            "Tekst: Raport opisuje związek między dostępnością bibliotek a wynikami "
            "szkolnymi w jednym województwie. Autorzy zastrzegają, że nie oddzielili "
            "wpływu bibliotek od zamożności gmin. Komentator uznaje tę ostrożność za "
            "dowód, że raport niczego nie wnosi. Tymczasem brak podstaw do rozstrzygnięcia "
            "o przyczynie nie unieważnia zaobserwowanej współzmienności; wyznacza jedynie "
            "granicę wniosku, jaki wolno z niej wyprowadzić. Kto z tej granicy czyni "
            "zarzut wobec samych danych, żąda od opisu odpowiedzi na inne pytanie. "
            "Na czym polega błąd komentatora wskazany w tekście?"
        ),
        options=[
            "Traktuje zamożność gmin jako wykluczoną przyczynę różnic w wynikach szkolnych.",
            "Uogólnia zaobserwowaną zależność na województwa, których raport nie obejmuje.",
            "Uznaje samą współzmienność za wystarczający dowód skuteczności bibliotek.",
            "Utożsamia ograniczenie wnioskowania przyczynowego z brakiem wartości opisu zależności.",
        ],
        correct=(
            "Utożsamia ograniczenie wnioskowania przyczynowego z brakiem wartości opisu zależności."
        ),
    ),
    AssessmentQuestion(
        id="pl-r-c2-003",
        skill="reading",
        difficulty="C2",
        question=(
            "Tekst: W mieście burmistrza wszystko odbywało się z godną podziwu zgodą. "
            "Mieszkańcom oszczędzano trudnych wyborów, ogłaszając wyniki konsultacji, "
            "zanim zdążyli zgłosić uwagi. Ci, którzy mimo to pisali listy, otrzymywali "
            "podziękowania za poparcie. Kronikarz skrupulatnie odnotowywał tę harmonię, "
            "a puste miejsce po rubryce z głosami sprzeciwu uznawał za największe "
            "osiągnięcie drukarni. Doprawdy, niewiele miast mogło się poszczycić tak "
            "staranną troską o to, by nikt nie musiał kłopotać się własnym zdaniem. "
            "Jak należy odczytać pochwalne słownictwo tego fragmentu?"
        ),
        options=[
            "Jako aprobatę sprawnego zarządzania, równoważoną zastrzeżeniem do pracy drukarni.",
            "Jako ironię: pozorna pochwała harmonii ujawnia mechanizm wyciszania sprzeciwu.",
            "Jako wyraz tęsknoty za wspólnotą, w której obywatele dobrowolnie rezygnują ze sporów.",
            "Jako neutralne przytoczenie kroniki, bez sygnałów dystansu wobec jej ocen.",
        ],
        correct="Jako ironię: pozorna pochwała harmonii ujawnia mechanizm wyciszania sprzeciwu.",
    ),
    AssessmentQuestion(
        id="pl-r-c2-004",
        skill="reading",
        difficulty="C2",
        question=(
            "Tekst: Gdy proponuję uzależnić wysokość opłaty od faktycznego zużycia wody, "
            "słyszę, że bez opłat sieć nie będzie miała z czego się utrzymać. Zgoda — "
            "tyle że nie o istnieniu opłaty rozmawiamy. Można odrzucić mój pomysł, "
            "wykazując, że nie pokryje kosztów stałych; nie można go obalić, przypisując "
            "mi zamiar likwidacji finansowania. Obrona obecnego systemu zacznie się "
            "dopiero wtedy, gdy ktoś wyjaśni, dlaczego jego sposób rozłożenia kosztów "
            "jest lepszy od proponowanego. Jaki zakres ma słowo „Zgoda” w tym wywodzie?"
        ),
        options=[
            "Akceptuje potrzebę finansowania sieci, ale nie uznaje jej za obronę obecnej metody opłat.",
            "Akceptuje zarzut, że proponowana metoda nie pokryje kosztów stałych utrzymania sieci.",
            "Przyznaje, że porównanie metod naliczania opłat jest zbędne wobec konieczności ich poboru.",
            "Wycofuje postulat zmiany metody opłat, zachowując jedynie krytykę sposobu prowadzenia sporu.",
        ],
        correct=(
            "Akceptuje potrzebę finansowania sieci, ale nie uznaje jej za obronę obecnej metody opłat."
        ),
    ),
]
