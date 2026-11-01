"""Polish grammar topics — A1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="byc",
        title="Czasownik być",
        level="A1",
        category="Czasowniki",
        summary="Najważniejszy czasownik polski: opisuje stan, tożsamość i położenie.",
        explanation=(
            "Czasownik **być** łączy podmiot z informacją o tym, kim jesteśmy, gdzie jesteśmy "
            "i w jakim stanie się znajdujemy. Jest nieregularny, więc jego formy trzeba opanować "
            "na pamięć.\n\n"
            "Odmiana w czasie teraźniejszym:\n"
            "- **ja** jestem\n"
            "- **ty** jesteś\n"
            "- **on / ona / ono** jest\n"
            "- **my** jesteśmy\n"
            "- **wy** jesteście\n"
            "- **oni / one** są\n\n"
            "Zaimków osobowych zwykle nie używamy, bo końcówka czasownika wskazuje osobę. "
            "Mówimy *Jestem studentem*, a nie *Ja jestem studentem*, chyba że chcemy coś "
            "podkreślić lub przeciwstawić.\n\n"
            "Gdy określamy zawód albo narodowość, po **być** występuje narzędnik: "
            "*Jestem lekarką*, *Jestem Polakiem*. Przeczenie **nie** piszemy oddzielnie: "
            "*nie jestem*, *nie jesteśmy*."
        ),
        structure="jestem · jesteś · jest · jesteśmy · jesteście · są",
        rules=[
            "Odmiana jest nieregularna: jestem, jesteś, jest, jesteśmy, jesteście, są.",
            "Zawód i narodowość po czasowniku być występują w narzędniku.",
            "Przeczenie nie piszemy rozdzielnie: nie jestem, nie jest.",
            "Zaimka osobowego nie powtarzamy, jeśli nie ma kontrastu.",
        ],
        examples=[
            GrammarExample(text="Jestem z Hiszpanii, ale mieszkam w Polsce.", translation=None),
            GrammarExample(text="Czy ty jesteś nauczycielem?", translation=None, note="pytanie"),
            GrammarExample(text="Moje dzieci nie są jeszcze w szkole.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Jestem student.",
                correct="Jestem studentem.",
                note="Po czasowniku być zawód występuje w narzędniku.",
            ),
            GrammarMistake(
                wrong="Nie jestem zmęczonym.",
                correct="Nie jestem zmęczony.",
                note="Orzecznik przymiotnikowy po być stoi w mianowniku.",
            ),
        ],
        related=["zaimki-osobowe", "przeczenie-nie", "narzednik-narodowosc"],
    ),
    GrammarTopic(
        slug="zaimki-osobowe",
        title="Zaimki osobowe",
        level="A1",
        category="Zaimki",
        summary="Ja, ty, on, ona, ono, my, wy, oni, one — często zbędne w zdaniu.",
        explanation=(
            "Zaimki osobowe w mianowniku to: **ja**, **ty**, **on**, **ona**, **ono**, **my**, "
            "**wy**, **oni**, **one**.\n\n"
            "W języku polskim końcówka czasownika wystarcza do rozpoznania osoby, dlatego zaimka "
            "zwykle nie ma w zdaniu: *Mieszkam w Krakowie*. Zaimek pojawia się wtedy, gdy chcemy "
            "podkreślić osobę lub ją przeciwstawić: *Ja mieszkam w Krakowie, a ty w Gdańsku*.\n\n"
            "Rodzaj odgrywa rolę w trzeciej osobie liczby mnogiej. Formy **oni** używamy, gdy "
            "w grupie jest przynajmniej jeden mężczyzna, a **one** — gdy grupa składa się "
            "wyłącznie z kobiet lub rzeczy: *Oni są studentami*, *One są studentkami*.\n\n"
            "W kontaktach oficjalnych zamiast *ty* używamy form **pan** i **pani** z czasownikiem "
            "w trzeciej osobie liczby pojedynczej: *Czy pan jest z Polski?*"
        ),
        structure="ja · ty · on / ona / ono · my · wy · oni / one",
        rules=[
            "Zaimka osobowego używamy tylko dla podkreślenia lub kontrastu.",
            "Oni obejmuje grupy mieszane, one wyłącznie kobiety i rzeczy.",
            "Pan i pani łączą się z trzecią osobą liczby pojedynczej.",
            "Zaimek nie zmienia formy czasownika, bo osobę wskazuje już końcówka.",
        ],
        examples=[
            GrammarExample(text="Ona mówi po polsku, a on po angielsku.", translation=None),
            GrammarExample(text="Oni są z Warszawy, a one z Krakowa.", translation=None),
            GrammarExample(text="Czy pan jest z Polski?", translation=None, note="forma oficjalna"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="One są studentami.",
                correct="Oni są studentami.",
                note="Grupa mieszana wymaga formy oni; dla samych kobiet: One są studentkami.",
            ),
            GrammarMistake(
                wrong="Pani jesteś z Polski?",
                correct="Pani jest z Polski?",
                note="Pan i pani łączą się z trzecią osobą liczby pojedynczej.",
            ),
        ],
        related=["byc", "zaimki-dzierzawcze", "czas-terazniejszy"],
    ),
    GrammarTopic(
        slug="rodzaj-rzeczownika",
        title="Rodzaj rzeczownika",
        level="A1",
        category="Rzeczowniki",
        summary="Trzy rodzaje gramatyczne, rozpoznawane po końcówce rzeczownika.",
        explanation=(
            "Każdy polski rzeczownik ma jeden z trzech rodzajów: **męski**, **żeński** albo "
            "**nijaki**. Rodzaj decyduje o formie przymiotnika, zaimka i czasownika w czasie "
            "przeszłym.\n\n"
            "Najprostsza wskazówka to końcówka:\n"
            "- rodzaj męski: spółgłoska na końcu — *dom*, *stół*, *kot*, *student*\n"
            "- rodzaj żeński: **-a** — *kobieta*, *kawa*, *ulica*\n"
            "- rodzaj nijaki: **-o**, **-e**, **-ę**, **-um** — *okno*, *morze*, *imię*, "
            "*muzeum*\n\n"
            "W rodzaju męskim rozróżniamy rzeczowniki **żywotne** (*kot*, *student*) i "
            "**nieżywotne** (*stół*, *chleb*). Ma to znaczenie w bierniku, gdzie formy żywotne "
            "zachowują się jak dopełniacz.\n\n"
            "Istnieją wyjątki. *Mężczyzna*, *tata* i *kolega* kończą się na **-a**, ale są rodzaju "
            "męskiego: *Ten mężczyzna jest zmęczony*. Nazwy cech z przyrostkiem **-ość** są "
            "żeńskie: *radość*, *miłość*. Sama końcówka **-ść** nie wystarcza: *gość* jest męski."
        ),
        structure="męski: spółgłoska · żeński: -a · nijaki: -o, -e, -ę, -um",
        rules=[
            "Rodzaj rzeczownika określa formę przymiotnika i czasownika w czasie przeszłym.",
            "Rzeczowniki na -a są zwykle żeńskie, ale mężczyzna, tata i kolega są męskie.",
            "Nazwy cech z przyrostkiem -ość są żeńskie; gość jest rodzaju męskiego.",
            "W rodzaju męskim wyróżniamy rzeczowniki żywotne i nieżywotne.",
        ],
        examples=[
            GrammarExample(text="Ten duży stół stoi w kuchni.", translation=None),
            GrammarExample(text="Ta nowa kawa jest gorąca.", translation=None),
            GrammarExample(text="To małe dziecko śpi spokojnie.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="To jest dobry kawa.",
                correct="To jest dobra kawa.",
                note="Kawa jest rodzaju żeńskiego, więc przymiotnik ma końcówkę -a.",
            ),
            GrammarMistake(
                wrong="Ten mężczyzna jest zmęczona.",
                correct="Ten mężczyzna jest zmęczony.",
                note="Mężczyzna jest rodzaju męskiego mimo końcówki -a.",
            ),
        ],
        related=["przymiotniki-rodzaj", "mianownik-liczba-mnoga", "biernik"],
    ),
    GrammarTopic(
        slug="narzednik-narodowosc",
        title="Narzędnik: narodowość i zawód",
        level="A1",
        category="Przypadki",
        summary="Kim jestem? Narzędnik po być i dopełniacz po przyimku z.",
        explanation=(
            "Narzędnik odpowiada na pytania **kim? czym?** i pojawia się po czasowniku **być**, "
            "gdy mówimy o narodowości lub zawodzie: *Jestem Polakiem*, *Jestem lekarką*.\n\n"
            "Końcówki narzędnika:\n"
            "- rodzaj męski i nijaki: **-em** — *Polak → Polakiem*, *nauczyciel → nauczycielem*, "
            "*dziecko → dzieckiem*\n"
            "- rodzaj żeński: **-ą** — *Polka → Polką*, *studentka → studentką*\n\n"
            "Przy dodawaniu końcówki zachodzą wymiany spółgłosek: **k → kiem** (*Polak → "
            "Polakiem*), **g → giem** (*pedagog → pedagogiem*), **rz → rzem** (*lekarz → "
            "lekarzem*).\n\n"
            "Pochodzenie wyrażamy inaczej: przyimkiem **z** i dopełniaczem. Mówimy *Jestem z "
            "Polski*, *Jestem z Hiszpanii*, *Jestem z Niemiec*. Narzędnik opisuje, kim jesteśmy, "
            "a konstrukcja z przyimkiem — skąd pochodzimy."
        ),
        structure="męski / nijaki: -em · żeński: -ą · pochodzenie: z + dopełniacz",
        rules=[
            "Narzędnik odpowiada na pytania kim? czym?",
            "Rzeczowniki męskie i nijakie przyjmują końcówkę -em, żeńskie -ą.",
            "Nazwy narodowości i zawodów po być stoją w narzędniku.",
            "Pochodzenie wyrażamy przyimkiem z i dopełniaczem, nie narzędnikiem.",
        ],
        examples=[
            GrammarExample(text="Jestem Polakiem, a moja żona jest Hiszpanką.", translation=None),
            GrammarExample(text="Marek jest inżynierem w dużej firmie.", translation=None),
            GrammarExample(text="Jestem z Polski, ale mieszkam w Niemczech.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Jestem Polka.",
                correct="Jestem Polką.",
                note="Narodowość po być wymaga narzędnika, tu z końcówką -ą.",
            ),
            GrammarMistake(
                wrong="Jestem z Polska.",
                correct="Jestem z Polski.",
                note="Po przyimku z używamy dopełniacza, nie mianownika.",
            ),
        ],
        related=["zawod-rodzaj", "byc", "mianownik-liczba-mnoga"],
    ),
    GrammarTopic(
        slug="mianownik-liczba-mnoga",
        title="Mianownik liczby mnogiej",
        level="A1",
        category="Rzeczowniki",
        summary="Studenci, koty, kobiety, okna — jak tworzyć liczbę mnogą.",
        explanation=(
            "Mianownik liczby mnogiej zależy od rodzaju i od zakończenia rzeczownika. Najwięcej "
            "uwagi wymaga rodzaj męskoosobowy, czyli nazwy mężczyzn.\n\n"
            "**Rodzaj męskoosobowy:**\n"
            "- **-i** lub **-y** z wymianą: *student → studenci*, *Polak → Polacy*\n"
            "- **-owie**: *pan → panowie*, *syn → synowie*\n"
            "- **-e**: *lekarz → lekarze*, *nauczyciel → nauczyciele*\n\n"
            "**Rodzaj męski nieosobowy, żeński i nijaki:**\n"
            "- męski nieosobowy: *kot → koty*, *stół → stoły*, *hotel → hotele*\n"
            "- żeński: *kobieta → kobiety*, *ulica → ulice*, *noc → noce*\n"
            "- nijaki: *okno → okna*, *morze → morza*\n\n"
            "Kilka form trzeba zapamiętać osobno: *brat → bracia*, *dziecko → dzieci*, "
            "*imię → imiona*. W liczbie mnogiej czasownik i przymiotnik też zmieniają formę: "
            "*Studenci są zmęczeni*, *Kobiety są zmęczone*."
        ),
        structure="męskoosobowy: -i / -y / -owie / -e · pozostałe: -y / -i / -e / -a",
        rules=[
            "Mianownik liczby mnogiej zależy od rodzaju i zakończenia rzeczownika.",
            "Rzeczowniki męskoosobowe mają -i, -y, -owie lub -e: studenci, Polacy, "
            "panowie, lekarze.",
            "Rzeczowniki żeńskie i męskie nieosobowe przyjmują -y, -i lub -e.",
            "Rzeczowniki nijakie przyjmują najczęściej końcówkę -a: okna, morza.",
        ],
        examples=[
            GrammarExample(text="Studenci uczą się w bibliotece.", translation=None),
            GrammarExample(text="W parku rosną wysokie drzewa.", translation=None),
            GrammarExample(text="Kobiety i dzieci czekają na przystanku.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Studenty uczą się w bibliotece.",
                correct="Studenci uczą się w bibliotece.",
                note="Rzeczowniki męskoosobowe mają formę studenci.",
            ),
            GrammarMistake(
                wrong="To są moje braty.",
                correct="To są moi bracia.",
                note="Brat ma nieregularną liczbę mnogą bracia.",
            ),
        ],
        related=["rodzaj-rzeczownika", "liczebniki", "biernik"],
    ),
    GrammarTopic(
        slug="zawod-rodzaj",
        title="Zawody i rodzaj żeński",
        level="A1",
        category="Rzeczowniki",
        summary="Nauczyciel i nauczycielka — jak nazywać zawody kobiet i mężczyzn.",
        explanation=(
            "Nazwy zawodów mają formę męską i żeńską. Forma męska jest podstawą, a żeńska "
            "najczęściej powstaje przez dodanie końcówki **-ka**: *nauczyciel → nauczycielka*, "
            "*student → studentka*, *kelner → kelnerka*, *kucharz → kucharka*.\n\n"
            "Inne typowe końcówki żeńskie:\n"
            "- **-yni** i **-czyni**: *sprzedawca → sprzedawczyni*, *doradca → doradczyni*\n"
            "- **-arka**: *dziennikarz → dziennikarka*, *bibliotekarz → bibliotekarka*\n\n"
            "Niektóre nazwy są takie same dla obu płci, na przykład *kierowca*. Wtedy rodzaj "
            "widać dopiero w zdaniu: *Piotr jest kierowcą*, *Anna jest kierowcą*.\n\n"
            "W zdaniu z **być** nazwa zawodu stoi w narzędniku: *Jestem nauczycielem*, "
            "*Ona jest lekarką*. Możliwa jest też nazwa męska odnosząca się do kobiety: "
            "*Ona jest lekarzem*. Wybór zależy od nazwy i kontekstu."
        ),
        structure="męski: temat · żeński: -ka / -yni / -czyni / -arka",
        rules=[
            "Nazwa zawodu po być występuje w narzędniku.",
            "Forma żeńska najczęściej powstaje przez dodanie końcówki -ka.",
            "Rzeczowniki na -ca tworzą formę żeńską na -czyni: sprzedawca — sprzedawczyni.",
            "Niektóre nazwy są wspólne dla obu płci, np. kierowca.",
        ],
        examples=[
            GrammarExample(text="Mój ojciec jest nauczycielem, a matka lekarką.", translation=None),
            GrammarExample(text="Anna pracuje jako kelnerka w kawiarni.", translation=None),
            GrammarExample(text="Piotr jest kierowcą autobusu.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ona jest lekarka.",
                correct="Ona jest lekarką.",
                note="Nazwa lekarka po jest wymaga narzędnika: lekarką.",
            ),
            GrammarMistake(
                wrong="Jestem nauczycielka.",
                correct="Jestem nauczycielką.",
                note="Brak końcówki -ą to błąd: zawód po być wymaga narzędnika.",
            ),
        ],
        related=["narzednik-narodowosc", "rodzaj-rzeczownika"],
    ),
    GrammarTopic(
        slug="przymiotniki-rodzaj",
        title="Przymiotnik a rodzaj rzeczownika",
        level="A1",
        category="Przymiotniki",
        summary="Wysoki, wysoka, wysokie — przymiotnik zgadza się z rzeczownikiem.",
        explanation=(
            "Przymiotnik dostosowuje się do rodzaju, liczby i przypadku rzeczownika, który "
            "określa. W liczbie pojedynczej końcówki są trzy: **-y** lub **-i** dla rodzaju "
            "męskiego, **-a** dla żeńskiego i **-e** dla nijakiego.\n\n"
            "Przykład: *wysoki mężczyzna*, *wysoka kobieta*, *wysokie drzewo*. Podobnie: "
            "*dobry chleb*, *dobra zupa*, *dobre wino*.\n\n"
            "W liczbie mnogiej rodzaj męskoosobowy ma końcówkę **-i** lub **-y**, a pozostałe "
            "rodzaje **-e**: *wysocy mężczyźni*, *wysokie kobiety*, *wysokie drzewa*. Przy "
            "tematach twardych zachodzi wymiana: *wysoki → wysocy*, *dobry → dobrzy*.\n\n"
            "Przymiotnik stoi zwykle przed rzeczownikiem i przyjmuje jego formę: *Mam "
            "wysokiego brata* (biernik), *Mieszkam w wysokim domu* (miejscownik)."
        ),
        structure="męski -y / -i · żeński -a · nijaki -e · mnogi męskoosobowy -i / -y",
        rules=[
            "Przymiotnik zgadza się z rzeczownikiem w rodzaju, liczbie i przypadku.",
            "W liczbie pojedynczej: -y lub -i (męski), -a (żeński), -e (nijaki).",
            "W liczbie mnogiej rodzaj męskoosobowy ma -i lub -y, pozostałe rodzaje -e.",
            "Twardy temat zmienia się w rodzaju męskoosobowym: wysoki — wysocy.",
        ],
        examples=[
            GrammarExample(text="To jest wysoki mężczyzna.", translation=None),
            GrammarExample(text="Ta zupa jest bardzo dobra.", translation=None),
            GrammarExample(text="Te dzieci są małe i wesołe.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="To jest dobra chleb.",
                correct="To jest dobry chleb.",
                note="Chleb jest rodzaju męskiego, więc przymiotnik ma końcówkę -y.",
            ),
            GrammarMistake(
                wrong="Ci studenci są wysokie.",
                correct="Ci studenci są wysocy.",
                note="Rodzaj męskoosobowy wymaga formy wysocy.",
            ),
        ],
        related=["rodzaj-rzeczownika", "zaimki-dzierzawcze", "mianownik-liczba-mnoga"],
    ),
    GrammarTopic(
        slug="zaimki-dzierzawcze",
        title="Zaimki dzierżawcze",
        level="A1",
        category="Zaimki",
        summary="Mój, moja, moje — zaimek zgadza się z rzeczą, nie z właścicielem.",
        explanation=(
            "Zaimki dzierżawcze to **mój**, **twój**, **jego**, **jej**, **nasz**, **wasz**, "
            "**ich**. Odpowiadają na pytanie **czyj?** i określają, do kogo należy rzecz.\n\n"
            "Zaimek przyjmuje rodzaj rzeczownika, który określa, a nie rodzaj właściciela:\n"
            "- *mój brat*, *moja siostra*, *moje dziecko*\n"
            "- *moi rodzice*, *moje dzieci*\n\n"
            "Formy **jego**, **jej** i **ich** są nieodmienne: *jego samochód*, *jej mieszkanie*, "
            "*ich dzieci*. Nie mówimy *jegowa siostra*.\n\n"
            "Zaimek **swój** odnosi się do podmiotu zdania: *Anna kocha swoją rodzinę*. Na "
            "poziomie A1 wystarczy rozpoznawać tę formę, a w prostych zdaniach używać **mój**, "
            "**twój** i **nasz**."
        ),
        structure="mój / moja / moje / moi · twój / twoja / twoje / twoi",
        rules=[
            "Zaimek dzierżawczy zgadza się z rzeczownikiem, który określa.",
            "Formy mój, twój, nasz i wasz odmieniają się przez rodzaje: moja, moje, moi.",
            "Jego, jej i ich są nieodmienne.",
            "Moi łączymy z rodzajem męskoosobowym, moje z pozostałymi: moi rodzice, moje dzieci.",
        ],
        examples=[
            GrammarExample(text="To jest mój brat, a to moja siostra.", translation=None),
            GrammarExample(text="Gdzie są twoi rodzice?", translation=None),
            GrammarExample(text="Jej mieszkanie jest na trzecim piętrze.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="To jest moja brat.",
                correct="To jest mój brat.",
                note="Brat jest rodzaju męskiego, więc używamy mój.",
            ),
            GrammarMistake(
                wrong="To są moje rodzice.",
                correct="To są moi rodzice.",
                note="Rodzice to rzeczownik męskoosobowy, więc zaimek ma formę moi.",
            ),
        ],
        related=["przymiotniki-rodzaj", "zaimki-osobowe"],
    ),
    GrammarTopic(
        slug="przeczenie-nie",
        title="Przeczenie nie",
        level="A1",
        category="Składnia",
        summary="Nie piszemy rozdzielnie, a w zdaniach z nikt i nic przeczenie jest podwójne.",
        explanation=(
            "Przeczenie **nie** stawiamy przed czasownikiem i piszemy osobno: *nie mieszkam*, "
            "*nie mam*, *nie wiem*. Nie łączymy go z czasownikiem w jeden wyraz.\n\n"
            "Polski wymaga przeczenia podwójnego. Jeśli w zdaniu jest **nikt**, **nic**, "
            "**nigdy** albo **nigdzie**, czasownik też musi mieć **nie**: *Nikt nie przyszedł*, "
            "*Nic nie wiem*, *Nigdy nie piję kawy*.\n\n"
            "Zdanie *Nie ma* oznacza brak czegoś i łączy się z dopełniaczem: *Nie ma mleka*, "
            "*Nie ma czasu*. Przeczenie przy być nie zmienia przypadku orzecznika: "
            "*To nie jest mój brat*, ale *On nie jest lekarzem*.\n\n"
            "Z przymiotnikami **nie** może tworzyć nowy wyraz i wtedy piszemy je razem: "
            "*niedobry*, *niewysoki*. Z czasownikami zawsze rozdzielnie."
        ),
        structure="nie + czasownik · nikt nie · nic nie · nigdy nie · nie ma + dopełniacz",
        rules=[
            "Przeczenie nie piszemy rozdzielnie przed czasownikiem.",
            "Przy nikt, nic, nigdy i nigdzie czasownik również ma przeczenie.",
            "Konstrukcja nie ma wymaga dopełniacza: nie ma mleka.",
            "Nie z przymiotnikiem może tworzyć nowy wyraz pisany razem: niedobry.",
        ],
        examples=[
            GrammarExample(text="Nie mieszkam w Warszawie.", translation=None),
            GrammarExample(text="Ona nie ma rodzeństwa.", translation=None),
            GrammarExample(text="Nikt nie zna odpowiedzi.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Nikt przyszedł na spotkanie.",
                correct="Nikt nie przyszedł na spotkanie.",
                note="Przy zaimku nikt czasownik musi mieć przeczenie.",
            ),
            GrammarMistake(
                wrong="Nie mam mleko.",
                correct="Nie mam mleka.",
                note="Po przeczeniu biernik zmienia się w dopełniacz.",
            ),
        ],
        related=["byc", "dopelniacz-przeczenie", "czas-terazniejszy"],
    ),
    GrammarTopic(
        slug="czas-terazniejszy",
        title="Czas teraźniejszy",
        level="A1",
        category="Czasowniki",
        summary="Podstawowe wzorce odmiany i najczęstsze czasowniki nieregularne.",
        explanation=(
            "Wzorzec odmiany poznajemy po formach pierwszej i drugiej osoby, nie tylko po "
            "bezokoliczniku. Wiele czasowników na **-ać** ma **-am, -asz**: "
            "*mieszkać — mieszkam, mieszkasz, mieszka, mieszkamy, mieszkacie, mieszkają*. "
            "Inne mają **-ę, -esz**, np. *pisać — piszę, piszesz*.\n\n"
            "Czasowniki zakończone na **-eć** odmieniają się różnie: *siedzieć — siedzę, "
            "siedzisz*, *umieć — umiem, umiesz*. Dlatego nową formę warto sprawdzić w "
            "słowniku.\n\n"
            "Kolejny częsty wzorzec to **-ę, -isz / -ysz**. Czasowniki takie jak mówić mają "
            "końcówkę **-ę**: *mówić — mówię, mówisz, mówi, mówimy, mówicie, mówią*. Podobnie "
            "odmieniają się *robić* i *lubić*.\n\n"
            "Osobna grupa to czasowniki na **-ować**, które w odmianie mają cząstkę **-uj-**: "
            "*pracować — pracuję, pracujesz, pracuje, pracujemy, pracujecie, pracują*.\n\n"
            "Kilka czasowników jest nieregularnych i trzeba je zapamiętać: *być*, *mieć* (*mam, "
            "masz, ma, mamy, macie, mają*), *iść* (*idę, idziesz, idzie, idziemy, idziecie, idą*) "
            "oraz *jeść* (*jem, jesz, je, jemy, jecie, jedzą*)."
        ),
        structure="mieszkam / mieszkasz · mówię / mówisz · piszę / piszesz · umiem / umiesz",
        rules=[
            "Końcówki osobowe wskazują wykonawcę, dlatego zaimków zwykle nie używamy.",
            "Czasowniki na -ować mają w odmianie cząstkę -uj-: pracować — pracuję.",
            "Ucz się obu form: mówię — mówisz, piszę — piszesz, umiem — umiesz.",
            "Być, mieć, iść i jeść odmieniają się nieregularnie.",
        ],
        examples=[
            GrammarExample(text="Mieszkam w Krakowie i pracuję w biurze.", translation=None),
            GrammarExample(text="Co robisz w weekend?", translation=None, note="pytanie"),
            GrammarExample(text="Ona mówi po polsku i po angielsku.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ona mieszkają w Krakowie.",
                correct="Ona mieszka w Krakowie.",
                note="Trzecia osoba liczby pojedynczej ma końcówkę -a.",
            ),
            GrammarMistake(
                wrong="On mówię po polsku.",
                correct="On mówi po polsku.",
                note="Końcówka -ę należy do pierwszej osoby, nie do trzeciej.",
            ),
        ],
        related=["byc", "czasowniki-zwrotne", "czasowniki-modalne"],
    ),
    GrammarTopic(
        slug="czasowniki-zwrotne",
        title="Czasowniki zwrotne",
        level="A1",
        category="Czasowniki",
        summary="Myć się, uczyć się, nazywać się — czasowniki z zaimkiem się.",
        explanation=(
            "Czasowniki zwrotne mają przy sobie cząstkę **się**, która jest taka sama dla "
            "wszystkich osób: *myć się*, *ubierać się*, *uczyć się*, *nazywać się*, "
            "*kłaść się*.\n\n"
            "Odmienia się tylko czasownik, a **się** zostaje bez zmian:\n"
            "- *myję się*, *myjesz się*, *myje się*\n"
            "- *myjemy się*, *myjecie się*, *myją się*\n\n"
            "**Się** stoi zwykle po czasowniku i nigdy nie rozpoczyna zdania. Mówimy *Uczę się "
            "polskiego*, a nie *Się uczę polskiego*. W konstrukcjach z bezokolicznikiem cząstka "
            "może stać po czasowniku osobowym: *Chcę się uczyć*.\n\n"
            "Niektóre czasowniki wymagają **się**, np. *bać się*. Inne zmieniają znaczenie: "
            "*uczyć* oznacza nauczanie kogoś, a *uczyć się* — zdobywanie wiedzy. "
            "Podobnie *nazywać kogoś przyjacielem* różni się od *nazywać się Anna*."
        ),
        structure="myć się: myję się · myjesz się · myje się · myjemy się · myjecie się · myją się",
        rules=[
            "Zaimek się stoi zazwyczaj po czasowniku.",
            "Się nie rozpoczyna zdania.",
            "Forma się jest taka sama dla wszystkich osób.",
            "Bać się wymaga się; uczyć i nazywać mogą występować bez się w innym znaczeniu.",
        ],
        examples=[
            GrammarExample(text="Nazywam się Marta i uczę się polskiego.", translation=None),
            GrammarExample(text="On myje się rano i wieczorem.", translation=None),
            GrammarExample(text="Dzieci bawią się w ogrodzie.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Nazywam Anna.",
                correct="Nazywam się Anna.",
                note="Gdy podajemy własne imię, używamy nazywać się.",
            ),
            GrammarMistake(
                wrong="Się uczę polskiego.",
                correct="Uczę się polskiego.",
                note="Się nie może stać na początku zdania.",
            ),
        ],
        related=["czas-terazniejszy", "zaimki-osobowe"],
    ),
    GrammarTopic(
        slug="godziny-dni",
        title="Godziny i dni tygodnia",
        level="A1",
        category="Czas i daty",
        summary="Jest siódma, o wpół do ósmej, w poniedziałek, we wtorek.",
        explanation=(
            "Godzinę podajemy w liczbie pojedynczej rodzaju żeńskiego, ponieważ domyślnym "
            "rzeczownikiem jest *godzina*: *Jest pierwsza*, *Jest siódma*, *Jest dwunasta*.\n\n"
            "Inne sposoby określania czasu:\n"
            "- *Jest wpół do ósmej* — o 7:30\n"
            "- *Jest kwadrans po trzeciej* — o 15:15\n"
            "- *Jest za dziesięć siódma* — o 6:50\n\n"
            "Na pytanie **O której?** odpowiadamy przyimkiem **o** i miejscownikiem: *o ósmej*, "
            "*o wpół do szóstej*, *o drugiej po południu*.\n\n"
            "Dni tygodnia łączymy z przyimkiem **w**: *w poniedziałek*, *w środę*, *w piątek*. "
            "Przed **wtorkiem** używamy formy **we**: *we wtorek*. Mówimy też *w weekend*, a "
            "datę tworzymy dopełniaczem: *piątego maja*."
        ),
        structure="Jest siódma · o siódmej · wpół do ósmej · w poniedziałek · we wtorek",
        rules=[
            "Godzina ma rodzaj żeński: jest siódma, jest dwunasta.",
            "Na pytanie o której odpowiadamy przyimkiem o i miejscownikiem: o ósmej.",
            "Dni tygodnia występują z przyimkiem w, a przed wtorkiem z formą we.",
            "Wpół do oznacza trzydzieści minut przed pełną godziną.",
        ],
        examples=[
            GrammarExample(text="Jest siódma rano, muszę iść do pracy.", translation=None),
            GrammarExample(text="Spotkamy się o wpół do szóstej.", translation=None),
            GrammarExample(text="W sobotę i w niedzielę nie pracuję.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Jest siódmy.",
                correct="Jest siódma.",
                note="Godzina jest rodzaju żeńskiego: siódma godzina.",
            ),
            GrammarMistake(
                wrong="Spotkamy się w wtorek.",
                correct="Spotkamy się we wtorek.",
                note="Przed wtorkiem używamy formy we, nie w.",
            ),
        ],
        related=["liczebniki", "czas-terazniejszy"],
    ),
    GrammarTopic(
        slug="biernik",
        title="Biernik",
        level="A1",
        category="Przypadki",
        summary="Kogo? Co? Kupuję kawę i chleb.",
        explanation=(
            "Biernik odpowiada na pytania **kogo? co?** i jest przypadkiem dopełnienia "
            "bliskiego. Używamy go po czasownikach takich jak *mieć*, *jeść*, *pić*, *kupować*, "
            "*lubić*, *czytać*, *widzieć* i *zamawiać*.\n\n"
            "Końcówki biernika zależą od rodzaju:\n"
            "- żeński: **-ę** — *kawa → kawę*, *herbata → herbatę*, *książka → książkę*\n"
            "- męski nieżywotny: forma jak w mianowniku — *chleb → chleb*, *stół → stół*\n"
            "- męski żywotny: forma jak w dopełniaczu — *kot → kota*, *student → studenta*\n"
            "- nijaki: forma jak w mianowniku — *okno → okno*, *mleko → mleko*\n\n"
            "Biernik występuje też po przyimkach **na** i **w**, gdy opisują ruch lub cel: "
            "*Idę na pocztę*, *Jadę w góry*, oraz po przyimku **przez**: *Rozmawiam przez "
            "telefon*. Dla położenia te same przyimki wymagają miejscownika: *Jestem na "
            "poczcie*."
        ),
        structure=(
            "żeński -ę · męski nieżywotny = mianownik · męski żywotny = dopełniacz "
            "· nijaki = mianownik"
        ),
        rules=[
            "Biernik odpowiada na pytania kogo? co?",
            "Rzeczowniki żeńskie na -a mają w bierniku końcówkę -ę.",
            "Rzeczowniki męskie żywotne mają formę równą dopełniaczowi: kot — kota.",
            "Rzeczowniki męskie nieżywotne i nijakie mają formę równą mianownikowi.",
        ],
        examples=[
            GrammarExample(text="Kupuję kawę i chleb.", translation=None),
            GrammarExample(text="Widzę swojego kota w ogrodzie.", translation=None),
            GrammarExample(text="Lubię herbatę z mlekiem.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Kupuję kawa.",
                correct="Kupuję kawę.",
                note="Kawa jest żeńska, więc w bierniku ma końcówkę -ę.",
            ),
            GrammarMistake(
                wrong="Widzę kot.",
                correct="Widzę kota.",
                note="Rzeczowniki męskie żywotne przyjmują w bierniku formę dopełniacza.",
            ),
        ],
        related=["dopelniacz-przeczenie", "liczebniki", "miejscownik"],
    ),
    GrammarTopic(
        slug="liczebniki",
        title="Liczebniki",
        level="A1",
        category="Liczebniki",
        summary="Dwa jabłka, pięć jabłek — liczebnik zmienia formę rzeczownika.",
        explanation=(
            "Liczebniki od jednego do dziesięciu to: **jeden**, **dwa**, **trzy**, **cztery**, "
            "**pięć**, **sześć**, **siedem**, **osiem**, **dziewięć**, **dziesięć**.\n\n"
            "**Jeden** zachowuje się jak przymiotnik i zgadza się z rodzajem: *jeden brat*, "
            "*jedna siostra*, *jedno dziecko*. Formy **dwa** używamy z rzeczownikami męskimi i "
            "nijakimi, a **dwie** z żeńskimi: *dwa jabłka*, *dwie kawy*.\n\n"
            "W podstawowych konstrukcjach z rzeczownikami niemęskoosobowymi liczby **2–4** "
            "łączą się z formami *dwa bilety*, *trzy kawy*, *cztery stoły*. Liczby **5–21** "
            "wymagają tu dopełniacza liczby mnogiej: *pięć jabłek*, *dziesięć minut*. "
            "Dalej wracają formy *dwadzieścia dwa bilety*, ale *dwadzieścia pięć biletów*; "
            "liczby zakończone na 12–14 mają dopełniacz: *sto dwanaście biletów*.\n\n"
            "Przy mężczyznach liczebnik też się zmienia: *dwóch braci*, *trzech studentów*, "
            "*pięciu kolegów*. W sklepie usłyszysz *pięć złotych* i *dwa złote* — forma "
            "rzeczownika zależy od liczebnika."
        ),
        structure="jeden bilet · dwa bilety · pięć biletów · dwadzieścia dwa bilety",
        rules=[
            "Liczebnik jeden zgadza się z rzeczownikiem w rodzaju.",
            "W mianowniku i bierniku: dwa jabłka, trzy kawy, dwadzieścia dwa bilety.",
            "Liczby 5–21 wymagają tu dopełniacza liczby mnogiej: pięć jabłek.",
            "Dwie łączymy z rzeczownikami żeńskimi: dwie siostry, dwie kawy.",
        ],
        examples=[
            GrammarExample(text="Mam dwóch braci i jedną siostrę.", translation=None),
            GrammarExample(text="Kup dwa bilety i trzy kawy.", translation=None),
            GrammarExample(text="To kosztuje pięć złotych.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mam dwa braty.",
                correct="Mam dwóch braci.",
                note="Przy rzeczownikach męskoosobowych używamy formy dwóch i dopełniacza.",
            ),
            GrammarMistake(
                wrong="Pięć jabłka.",
                correct="Pięć jabłek.",
                note="Po pięć rzeczownik stoi tu w dopełniaczu liczby mnogiej.",
            ),
        ],
        related=["biernik", "mianownik-liczba-mnoga", "dopelniacz-przeczenie"],
    ),
    GrammarTopic(
        slug="czasowniki-modalne",
        title="Czasowniki modalne",
        level="A1",
        category="Czasowniki",
        summary="Móc, musieć, chcieć, umieć — zawsze z bezokolicznikiem.",
        explanation=(
            "Najważniejsze czasowniki modalne to **móc**, **musieć**, **chcieć** i **umieć**. "
            "Po każdym z nich występuje bezokolicznik: *muszę iść*, *chcę kupić*, *mogę "
            "zapłacić*, *umiem pływać*.\n\n"
            "Odmiana w czasie teraźniejszym:\n"
            "- **móc**: mogę, możesz, może, możemy, możecie, mogą\n"
            "- **musieć**: muszę, musisz, musi, musimy, musicie, muszą\n"
            "- **chcieć**: chcę, chcesz, chce, chcemy, chcecie, chcą\n"
            "- **umieć**: umiem, umiesz, umie, umiemy, umiecie, umieją\n\n"
            "Ważna różnica: *nie musieć* znaczy 'nie mieć obowiązku', a zakaz wyrażamy przez "
            "**nie wolno**: *Nie musisz przychodzić* (możesz nie przychodzić), ale *Nie wolno "
            "tu palić* (zakaz).\n\n"
            "Czasowniki modalne odmieniają się jak zwykłe czasowniki. W czasie przeszłym "
            "przyjmują końcówki rodzajowe: *musiałem*, *musiałam*, *chciał*, *chciała*."
        ),
        structure="móc / musieć / chcieć / umieć + bezokolicznik",
        rules=[
            "Po czasowniku modalnym występuje bezokolicznik: muszę iść.",
            "Musieć i móc są nieregularne: muszę, możesz.",
            "Nie musieć znaczy 'nie mieć obowiązku', a nie 'nie wolno'.",
            "Chcieć ma pierwszą osobę chcę, a przeczenie tworzymy jako nie chcę.",
        ],
        examples=[
            GrammarExample(text="Muszę iść do lekarza.", translation=None),
            GrammarExample(text="Czy mogę zapłacić kartą?", translation=None, note="pytanie"),
            GrammarExample(text="Chcę się uczyć polskiego.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Muszę idę do lekarza.",
                correct="Muszę iść do lekarza.",
                note="Po czasowniku modalnym używamy bezokolicznika.",
            ),
            GrammarMistake(
                wrong="Tu nie musisz palić.",
                correct="Tu nie wolno palić.",
                note="Jeśli chodzi o zakaz, używamy nie wolno. Nie musisz oznacza brak obowiązku.",
            ),
        ],
        related=["czas-terazniejszy", "czas-przyszly"],
    ),
    GrammarTopic(
        slug="miejscownik",
        title="Miejscownik",
        level="A1",
        category="Przypadki",
        summary="W Polsce, na stole, o pracy — przypadek z przyimkiem.",
        explanation=(
            "Miejscownik odpowiada na pytania **o kim? o czym?** i **gdzie?** Występuje wyłącznie "
            "z przyimkami **w**, **na**, **o**, **przy** i **po**: *w kuchni*, *na stole*, "
            "*o pracy*, *przy oknie*, *po obiedzie*.\n\n"
            "Końcówki zależą od tematu:\n"
            "- rzeczowniki żeńskie na **-a**: **-e** z wymianą — *szkoła → w szkole*, "
            "*Warszawa → w Warszawie*\n"
            "- po spółgłoskach **c, cz, sz, ż, rz** oraz po miękkich: **-y** lub **-i** — "
            "*ulica → na ulicy*, *kuchnia → w kuchni*\n"
            "- rodzaj męski i nijaki z twardym tematem: **-e** — *stół → na stole*, "
            "*miasto → w mieście*\n"
            "- po **k, g, ch** i po miękkich: **-u** — *biurko → na biurku*, *pociąg → w pociągu*, "
            "*pokój → w pokoju*\n\n"
            "Nazwy krajów też są w miejscowniku: *w Polsce*, *w Niemczech*, *we Włoszech*. "
            "Uwaga na przyimek: *w Polsce*, ale *na Węgrzech* i *na Ukrainie*."
        ),
        structure="w / na / o / przy / po + miejscownik · -e, -u, -i / -y",
        rules=[
            "Miejscownik występuje wyłącznie z przyimkami w, na, o, przy i po.",
            "Rzeczowniki żeńskie na -a mają końcówkę -e z wymianą: szkoła — w szkole.",
            "Po k, g, ch oraz po spółgłoskach miękkich często występuje -u.",
            "Nazwy krajów: w Polsce, w Niemczech, we Włoszech.",
        ],
        examples=[
            GrammarExample(text="Mieszkam w Polsce, w małym mieście.", translation=None),
            GrammarExample(text="Książka leży na stole.", translation=None),
            GrammarExample(text="Rozmawiamy o pracy i o rodzinie.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Mieszkam w Polska.",
                correct="Mieszkam w Polsce.",
                note="Po przyimku w używamy miejscownika.",
            ),
            GrammarMistake(
                wrong="Książka leży na stół.",
                correct="Książka leży na stole.",
                note="Położenie wyrażamy miejscownikiem, nie biernikiem.",
            ),
        ],
        related=["przyimki-miejsca", "biernik", "czasowniki-ruchu"],
    ),
    GrammarTopic(
        slug="przyimki-miejsca",
        title="Przyimki miejsca",
        level="A1",
        category="Przyimki",
        summary="Na, pod, nad, obok, między — każdy przyimek ma swój przypadek.",
        explanation=(
            "Przyimki miejsca opisują położenie przedmiotów. Każdy z nich wymaga konkretnego "
            "przypadku, więc trzeba uczyć się ich razem z formami rzeczowników.\n\n"
            "- **w** i **na** + miejscownik: *w kuchni*, *na stole*\n"
            "- **pod**, **nad**, **przed**, **za** i **między** + narzędnik: *pod stołem*, "
            "*nad łóżkiem*, *przed domem*, *za szafą*, *między szafą a drzwiami*\n"
            "- **obok** i **koło** + dopełniacz: *obok okna*, *koło sklepu*\n"
            "- **przy** + miejscownik: *przy stole*, *przy oknie*\n\n"
            "Te same przyimki mogą opisywać ruch. Wtedy **na**, **pod** i **za** łączą się z "
            "biernikiem: *Kładę książkę na stół*, *Wchodzę pod drzewo*, *Idę za dom*. "
            "Położenie wymaga miejscownika lub narzędnika, a kierunek — biernika."
        ),
        structure="w / na / przy + miejscownik · pod / nad / przed / za / między + narzędnik "
        "· obok / koło + dopełniacz",
        rules=[
            "W i na łączą się z miejscownikiem, gdy opisują położenie.",
            "Pod, nad, przed, za i między w opisie położenia wymagają narzędnika.",
            "Obok i koło łączą się z dopełniaczem.",
            "Przy występuje z miejscownikiem: przy stole.",
        ],
        examples=[
            GrammarExample(text="Kot śpi pod stołem.", translation=None),
            GrammarExample(text="Lampa wisi nad łóżkiem.", translation=None),
            GrammarExample(text="Sklep jest obok apteki.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Kot śpi pod stół.",
                correct="Kot śpi pod stołem.",
                note="Pod z narzędnikiem opisuje miejsce, z biernikiem kierunek.",
            ),
            GrammarMistake(
                wrong="Sklep jest obok apteka.",
                correct="Sklep jest obok apteki.",
                note="Obok wymaga dopełniacza.",
            ),
        ],
        related=["miejscownik", "narzednik-narodowosc", "czasowniki-ruchu"],
    ),
    GrammarTopic(
        slug="czasowniki-ruchu",
        title="Czasowniki ruchu",
        level="A1",
        category="Czasowniki",
        summary="Iść czy chodzić? Jechać czy jeździć? Ruch jednorazowy i powtarzalny.",
        explanation=(
            "Polski rozróżnia ruch jednorazowy i ruch powtarzalny. **Iść** i **jechać** opisują "
            "konkretną czynność wykonywaną teraz: *Idę do sklepu*, *Jadę do Krakowa*.\n\n"
            "**Chodzić** i **jeździć** opisują czynność powtarzaną lub ogólną: *Codziennie "
            "chodzę na spacer*, *Często jeżdżę pociągiem*. Drugie rozróżnienie dotyczy środka "
            "transportu: **iść** i **chodzić** to ruch pieszo, a **jechać** i **jeździć** — "
            "samochodem, pociągiem, autobusem lub rowerem.\n\n"
            "Odmiana:\n"
            "- **iść**: idę, idziesz, idzie, idziemy, idziecie, idą\n"
            "- **chodzić**: chodzę, chodzisz, chodzi, chodzimy, chodzicie, chodzą\n"
            "- **jechać**: jadę, jedziesz, jedzie, jedziemy, jedziecie, jadą\n"
            "- **jeździć**: jeżdżę, jeździsz, jeździ, jeździmy, jeździcie, jeżdżą\n\n"
            "Gdy mówimy o drodze do celu, po tych czasownikach często pojawia się **do** z "
            "dopełniaczem: *Idę do pracy*, *Jadę do domu*."
        ),
        structure="iść / jechać (teraz) · chodzić / jeździć (regularnie) · do + dopełniacz",
        rules=[
            "Iść i jechać opisują jedną, konkretną czynność w danym momencie.",
            "Chodzić i jeździć opisują czynność powtarzaną lub ogólną.",
            "Iść i chodzić dotyczą ruchu pieszego, jechać i jeździć — transportu.",
            "Cel ruchu wyrażamy przyimkiem do i dopełniaczem: do pracy, do domu.",
        ],
        examples=[
            GrammarExample(text="Idę teraz do sklepu.", translation=None),
            GrammarExample(text="Codziennie chodzę na spacer.", translation=None),
            GrammarExample(text="Jadę do Krakowa pociągiem.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Codziennie chodzię na spacer.",
                correct="Codziennie chodzę na spacer.",
                note="Pierwsza osoba czasownika chodzić to chodzę.",
            ),
            GrammarMistake(
                wrong="Jadę do Krakowa pieszo.",
                correct="Idę do Krakowa pieszo.",
                note="Jechać dotyczy transportu, pieszo chodzimy i idziemy.",
            ),
        ],
        related=["przyimki-miejsca", "czas-terazniejszy", "czas-przyszly"],
    ),
    GrammarTopic(
        slug="czas-przyszly",
        title="Czas przyszły",
        level="A1",
        category="Czasowniki",
        summary="Będę czytać, napiszę, pojedziemy — przyszłość złożona i prosta.",
        explanation=(
            "Czas przyszły złożony tworzymy z form czasownika **być** i bezokolicznika: "
            "*będę czytać*, *będziesz pracować*, *będziemy mieszkać*. Odmiana być w czasie "
            "przyszłym to: **będę**, **będziesz**, **będzie**, **będziemy**, **będziecie**, "
            "**będą**.\n\n"
            "Zamiast bezokolicznika można użyć formy przeszłej z rodzajem: *będę czytał*, "
            "*będę czytała*. Oba warianty są poprawne: *Będę czytać* i *Będę czytał*.\n\n"
            "Czasowniki **dokonane** tworzą czas przyszły prosty, bez czasownika być: "
            "*napisać → napiszę*, *zrobić → zrobię*, *pojechać → pojedziemy*. Taka forma "
            "podkreśla, że czynność zostanie zakończona.\n\n"
            "Porównaj: *Będę pisać list* (proces) i *Napiszę list* (skutek). Na poziomie A1 "
            "wystarczy umieć obie konstrukcje w prostych zdaniach o planach."
        ),
        structure="będę + bezokolicznik · będę + forma przeszła · czasowniki dokonane: napiszę",
        rules=[
            "Czas przyszły złożony tworzymy z będę i bezokolicznika: będę czytać.",
            "Można też użyć formy przeszłej: będę czytał, będę czytała.",
            "Czasowniki dokonane tworzą czas przyszły prosty: napiszę, zrobię.",
            "Po będę nie występuje forma osobowa drugiego czasownika.",
        ],
        examples=[
            GrammarExample(text="Jutro będę pracować w domu.", translation=None),
            GrammarExample(text="W przyszłym roku pojedziemy do Polski.", translation=None),
            GrammarExample(text="Napiszę do ciebie wieczorem.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Jutro będę pracuję w domu.",
                correct="Jutro będę pracować w domu.",
                note="Po będę występuje bezokolicznik, nie forma osobowa.",
            ),
            GrammarMistake(
                wrong="Będę czytać książka.",
                correct="Będę czytać książkę.",
                note="Czasownik czytać wymaga biernika: książkę.",
            ),
        ],
        related=["czas-przeszly", "czasowniki-modalne", "czas-terazniejszy"],
    ),
    GrammarTopic(
        slug="czas-przeszly",
        title="Czas przeszły",
        level="A1",
        category="Czasowniki",
        summary="Byłem, byłam, byliśmy — końcówki rodzajowe w czasie przeszłym.",
        explanation=(
            "Czas przeszły tworzymy od tematu bezokolicznika, dodając końcówki rodzajowe i "
            "osobowe. Rodzaj męski liczby pojedynczej ma końcówkę **-ł**: *czytać → czytał*, "
            "*być → był*. Rodzaj żeński ma **-ła**: *czytała*, *była*. Rodzaj nijaki ma **-ło**: "
            "*dziecko czytało*.\n\n"
            "Pełna odmiana czasownika **być**:\n"
            "- *byłem / byłam*, *byłeś / byłaś*, *był / była / było*\n"
            "- *byliśmy / byłyśmy*, *byliście / byłyście*, *byli / były*\n\n"
            "W liczbie mnogiej rozróżniamy grupę męskoosobową (**-liśmy**, **-li**) i pozostałe "
            "osoby (**-łyśmy**, **-ły**): *Byliśmy w kinie*, *Dziewczynki były w kinie*.\n\n"
            "Czas przeszły zgadza się z rodzajem podmiotu, nie z rodzajem mówiącego: *Anna "
            "powiedziała*, *Piotr powiedział*. Końcówki **-em** i **-eś** piszemy razem z "
            "formą czasownika: *byłem*, *byłeś*."
        ),
        structure="-łem / -łam · -łeś / -łaś · -ł / -ła / -ło · -liśmy / -łyśmy · -li / -ły",
        rules=[
            "Czas przeszły tworzymy od tematu bezokolicznika z końcówkami rodzajowymi.",
            "Rodzaj męski liczby pojedynczej ma końcówkę -ł: czytał.",
            "W liczbie mnogiej występują formy męskoosobowe -liśmy, -li oraz "
            "niemęskoosobowe -łyśmy, -ły.",
            "Końcówki -em i -eś piszemy łącznie z czasownikiem: byłem, byłeś.",
        ],
        examples=[
            GrammarExample(text="Wczoraj byłem w kinie.", translation=None),
            GrammarExample(text="Ona czytała książkę przez cały wieczór.", translation=None),
            GrammarExample(text="Byliśmy w Krakowie w zeszłym tygodniu.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ona był w domu.",
                correct="Ona była w domu.",
                note="Czas przeszły zgadza się z rodzajem podmiotu: ona była.",
            ),
            GrammarMistake(
                wrong="My byli w Krakowie.",
                correct="Byliśmy w Krakowie.",
                note="Pierwsza osoba liczby mnogiej ma końcówkę -liśmy.",
            ),
        ],
        related=["czas-przyszly", "byc", "dopelniacz-przeczenie"],
    ),
    GrammarTopic(
        slug="dopelniacz-przeczenie",
        title="Dopełniacz po przeczeniu",
        level="A1",
        category="Przypadki",
        summary="Nie mam czasu, nie ma mleka — biernik zmienia się w dopełniacz.",
        explanation=(
            "Dopełniacz odpowiada na pytania **kogo? czego?** i pojawia się po przeczeniu "
            "czasowników, które normalnie wymagają biernika: *Mam czas → Nie mam czasu*, "
            "*Widzę samochód → Nie widzę samochodu*.\n\n"
            "Końcówki dopełniacza:\n"
            "- rodzaj męski nieżywotny: **-u** lub **-a** — *czas → czasu*, *chleb → chleba*\n"
            "- rodzaj żeński: **-y** lub **-i** — *kawa → kawy*, *herbata → herbaty*\n"
            "- rodzaj nijaki: **-a** — *mleko → mleka*, *jajko → jajka*\n\n"
            "Konstrukcja **nie ma** zawsze wymaga dopełniacza, bo opisuje brak czegoś: *Nie ma "
            "mleka w lodówce*, *Nie ma czasu*. Nie mówimy *Nie ma mleko*.\n\n"
            "Dopełniacz występuje też po wyrażeniach ilościowych **dużo**, **mało**, **trochę** "
            "oraz w konstrukcjach z liczebnikami takimi jak pięć: *dużo owoców*, *mało czasu*, *trochę wody*, "
            "*pięć jabłek*."
        ),
        structure="nie mam + dopełniacz · nie ma + dopełniacz · dużo / mało / trochę + dopełniacz",
        rules=[
            "Po przeczeniu czasownika mieć biernik zmienia się w dopełniacz.",
            "Konstrukcja nie ma zawsze wymaga dopełniacza.",
            "Dopełniacz odpowiada na pytania kogo? czego?",
            "Po dużo, mało i trochę używamy dopełniacza; podobnie w konstrukcji pięć jabłek.",
        ],
        examples=[
            GrammarExample(text="Nie mam czasu na kawę.", translation=None),
            GrammarExample(text="W lodówce nie ma mleka.", translation=None),
            GrammarExample(text="Kupuję dużo owoców.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Nie mam czas.",
                correct="Nie mam czasu.",
                note="Po przeczeniu używamy dopełniacza.",
            ),
            GrammarMistake(
                wrong="Nie ma mleko w lodówce.",
                correct="Nie ma mleka w lodówce.",
                note="Nie ma łączy się z dopełniaczem.",
            ),
        ],
        related=["przeczenie-nie", "biernik", "liczebniki"],
    ),
]
