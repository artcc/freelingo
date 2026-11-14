"""Czech B2 placement: grammatical scope, interaction and contextual inference."""

from app.data._types import AssessmentQuestion

B2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "cs-g-b2-001",
        "grammar",
        "B2",
        "Doplňte spisovnou větu vyjadřující podmíněnou možnost: "
        "Po dnešním jednání ___ ještě mohl rozmyslet.",
        [
            "by jsem si to",
            "bych se to",
            "bych si to",
            "bych si se to",
        ],
        "bych si to",
        "cs-clitic-order-b2",
    ),
    AssessmentQuestion(
        "cs-g-b2-002",
        "grammar",
        "B2",
        "Zápis z desetičlenné komise uvádí: Ne všichni členové návrh podpořili. "
        "Který závěr vyplývá pouze z této věty?",
        [
            "Alespoň jeden člen návrh nepodpořil.",
            "Většina členů hlasovala proti návrhu.",
            "Návrh získal podporu přesně pěti členů.",
            "Každý člen se zdržel hlasování.",
        ],
        "Alespoň jeden člen návrh nepodpořil.",
        "cs-negation-scope-b2",
    ),
    AssessmentQuestion(
        "cs-g-b2-003",
        "grammar",
        "B2",
        "Převeďte větu do činného rodu bez změny účastníků, času a dokončenosti děje: "
        "Návrh byl po diskusi schválen zastupitelstvem.",
        [
            "Zastupitelstvo po diskusi návrh schvalovalo.",
            "Zastupitelstvo návrh schválí po diskusi.",
            "Komise po diskusi návrh schválila.",
            "Zastupitelstvo po diskusi návrh schválilo.",
        ],
        "Zastupitelstvo po diskusi návrh schválilo.",
        "cs-periphrastic-passive-b2",
    ),
    AssessmentQuestion(
        "cs-g-b2-004",
        "grammar",
        "B2",
        "V pondělí Klára vašemu týmu řekla: „Pošlu vám podklady zítra.“ "
        "Ve čtvrtek její výrok předáváte kolegovi. Které znění zachovává "
        "původní závazek, ale netvrdí, že už byl splněn?",
        [
            "Klára v pondělí řekla, že nám podklady pošle v pátek.",
            "Klára v pondělí řekla, že nám podklady pošle v úterý.",
            "Klára v pondělí potvrdila, že nám podklady poslala v neděli.",
            "Klára v pondělí řekla, že nám podklady možná někdy pošle.",
        ],
        "Klára v pondělí řekla, že nám podklady pošle v úterý.",
        "cs-reported-speech-b2",
    ),
    AssessmentQuestion(
        "cs-g-b2-005",
        "grammar",
        "B2",
        "Dům má vyšší nájem, ale nižší celkové měsíční náklady díky úspornému vytápění. "
        "Která věta zachovává obě informace a vztah mezi nimi?",
        [
            "Dům má nižší celkové náklady, protože jeho nájem je vyšší.",
            "Přestože je nájem vyšší, celkové měsíční náklady jsou nižší.",
            "Dům bude mít nižší celkové náklady, jen pokud se zvýší nájem.",
            "Čím vyšší je nájem tohoto domu, tím nižší jsou náklady na vytápění.",
        ],
        "Přestože je nájem vyšší, celkové měsíční náklady jsou nižší.",
        "cs-concession-b2",
    ),
    AssessmentQuestion(
        "cs-g-b2-006",
        "grammar",
        "B2",
        "Jana slíbila Petrovi zavolat dodavateli. Petr doporučil Janě počkat do pondělí. "
        "Kdo podle první věty přijal závazek telefonovat?",
        [
            "Petr přijal závazek zavolat dodavateli.",
            "Dodavatel přijal závazek zavolat Janě.",
            "Jana i Petr přijali závazek zavolat společně.",
            "Jana přijala závazek zavolat dodavateli.",
        ],
        "Jana přijala závazek zavolat dodavateli.",
        "cs-infinitive-control-b2",
    ),
    AssessmentQuestion(
        "cs-g-b2-007",
        "grammar",
        "B2",
        "Pravidla uvádějí: O příspěvek lze žádat jen tehdy, pokud má spolek sídlo v obci. "
        "Co tato podmínka znamená?",
        [
            "Sídlo v obci je nutné k žádosti, nikoli zárukou příspěvku.",
            "Sídlo v obci zaručuje přidělení příspěvku, pokud spolek podá žádost.",
            "Sídlo mimo obec umožňuje žádat, ale pouze o nižší částku.",
            "Sídlo v obci se vyžaduje až po schválení žádosti o příspěvek.",
        ],
        "Sídlo v obci je nutné k žádosti, nikoli zárukou příspěvku.",
        "cs-conditional-limits-b2",
    ),
    AssessmentQuestion(
        "cs-g-b2-008",
        "grammar",
        "B2",
        "Kolegyně v neformálním rozhovoru řekla: „To je dobrej návrh, ale nový auta "
        "teď kupovat nebudeme.“ Který zápis zachovává význam a užívá neutrální spisovné tvary?",
        [
            "Je to dobrý návrh, ale nová auta už jsme koupili.",
            "Je to dobrej návrh, ale nová auta teď kupovat nebudeme.",
            "Je to dobrý návrh, ale nová auta teď kupovat nebudeme.",
            "Je to dobrý návrh, ale nové auto teď koupíme.",
        ],
        "Je to dobrý návrh, ale nová auta teď kupovat nebudeme.",
        "cs-standard-spoken-b2",
    ),
    AssessmentQuestion(
        "cs-v-b2-001",
        "vocabulary",
        "B2",
        "Dodavatel už nesníží cenu, ale nabídne delší dobu na zaplacení. "
        "Chcete stručně pojmenovat právě tuto změnu. Co nabídl?",
        [
            "Prodloužení splatnosti.",
            "Snížení zálohy.",
            "Zvýšení rozpočtu.",
            "Zkrácení dodací lhůty.",
        ],
        "Prodloužení splatnosti.",
    ),
    AssessmentQuestion(
        "cs-v-b2-002",
        "vocabulary",
        "B2",
        "Sousedé se obávají hluku z klubovny. Organizátoři posunou konec programu na dřívější "
        "hodinu, sousedé na oplátku přijmou dvě akce měsíčně. Jak nejpřesněji popíšete výsledek?",
        [
            "Organizátoři odstoupili od pořádání akcí.",
            "Sousedé vzali svou námitku v plném rozsahu zpět.",
            "Obě strany dosáhly kompromisu.",
            "Organizátoři na sousedy přenesli odpovědnost.",
        ],
        "Obě strany dosáhly kompromisu.",
    ),
    AssessmentQuestion(
        "cs-v-b2-003",
        "vocabulary",
        "B2",
        "Rozvrh se tento týden měnil potřetí. Kolega při pohledu na další večerní směnu "
        "s povzdechem řekl: „Ještě jedna změna a budu tady bydlet.“ "
        "Jak jeho poznámku v této situaci nejspíše chápat?",
        [
            "Žádá o ubytování, aby mohl přijmout další směny.",
            "S nadsázkou si stěžuje, kolik času tráví v práci.",
            "Nabízí, že se ujme plánování večerních směn.",
            "Oznamuje, že si kvůli práci hledá byt v okolí.",
        ],
        "S nadsázkou si stěžuje, kolik času tráví v práci.",
    ),
    AssessmentQuestion(
        "cs-v-b2-004",
        "vocabulary",
        "B2",
        "V rozhovoru zaznělo: „Pokud získáme povolení, otevřeme v červnu.“ "
        "Titulek následně oznámil jisté červnové otevření. Co titulek udělal s původním sdělením?",
        [
            "Doložil ho nezávislým důkazem.",
            "Upřesnil, kdy bylo vydáno povolení.",
            "Vyvrátil plán červnového otevření.",
            "Zkreslil ho vynecháním podmínky.",
        ],
        "Zkreslil ho vynecháním podmínky.",
    ),
    AssessmentQuestion(
        "cs-r-b2-001",
        "reading",
        "B2",
        "Přečtěte si zprávu: „Zkušební sobotní provoz knihovny přilákal více čtenářů, "
        "než jsme čekali. Na pravidelné sobotní služby však nyní nemáme dost pracovníků. "
        "Do konce roku proto otevřeme ještě dvě vybrané soboty a poté situaci vyhodnotíme.“ "
        "Který závěr nejlépe vystihuje rozhodnutí knihovny?",
        [
            "Slabá návštěvnost vede k ukončení zkoušky po dvou dalších sobotách.",
            "Úspěšná zkouška umožní pravidelný sobotní provoz už od ledna.",
            "Další soboty se otevřou až po přijetí nových pracovníků.",
            "Zájem je slibný, ale počet pracovníků zatím omezuje pokračování.",
        ],
        "Zájem je slibný, ale počet pracovníků zatím omezuje pokračování.",
    ),
    AssessmentQuestion(
        "cs-r-b2-002",
        "reading",
        "B2",
        "E-mail klienta uvádí: „Děkujeme za upravenou nabídku. Rozsah služeb už odpovídá "
        "našim potřebám. Před potvrzením objednávky však potřebujeme stanovisko našeho "
        "právního oddělení k odpovědnosti za škodu. Ozveme se nejpozději ve středu.“ "
        "Co má dodavatel z této zprávy vyvodit?",
        [
            "Klient objednávku potvrdil a právní oddělení už jen připraví podpis.",
            "Obsah služeb klientovi vyhovuje, ale objednávka ještě není potvrzena.",
            "Klient odmítl odpovědnost za škodu a žádá zúžení rozsahu služeb.",
            "Ve středu začne poskytování služeb bez ohledu na právní stanovisko.",
        ],
        "Obsah služeb klientovi vyhovuje, ale objednávka ještě není potvrzena.",
    ),
    AssessmentQuestion(
        "cs-r-b2-003",
        "reading",
        "B2",
        "Zápis ze schůze obyvatel domu říká: „Pavel navrhl kameru u vchodu. Alena podpořila "
        "lepší zabezpečení, ale upozornila na ochranu soukromí. Na tom, že nejprve "
        "opraví zámek, se nakonec shodli všichni. O kameře rozhodnou až po získání "
        "dalších informací.“ "
        "Které shrnutí zachovává rozsah dosažené shody?",
        [
            "Obyvatelé schválili kameru, pokud se při její instalaci opraví zámek.",
            "Alena odmítla lepší zabezpečení a ostatní podpořili její stanovisko.",
            "Obyvatelé přijali první praktický krok, ale otázku kamery zatím neuzavřeli.",
            "Pavel vzal návrh kamery zpět výměnou za okamžitou opravu zámku.",
        ],
        "Obyvatelé přijali první praktický krok, ale otázku kamery zatím neuzavřeli.",
    ),
    AssessmentQuestion(
        "cs-r-b2-004",
        "reading",
        "B2",
        "Přečtěte si výměnu zpráv. Eva: „Prezentaci zvládnu do pátku, pokud mi dnes "
        "pošlete konečná čísla.“ Tomáš: „Dnes ještě hotová nebudou. Mám vedení slíbit "
        "pátek?“ Chcete zabránit tomu, aby Tomáš slíbil termín, který Eva za nových "
        "okolností nepotvrdila. Která odpověď je nejvhodnější?",
        [
            "Nejdřív s Evou ověř nový termín podle toho, kdy dostane čísla.",
            "Potvrď pátek, protože Eva už uvedla, že prezentaci do té doby zvládne.",
            "Posuň slíbený termín o den, stejně jako se posune dodání čísel.",
            "Pošli Evě předběžná čísla a vedení potvrď původní páteční termín.",
        ],
        "Nejdřív s Evou ověř nový termín podle toho, kdy dostane čísla.",
    ),
]
