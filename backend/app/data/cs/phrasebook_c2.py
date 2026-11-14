"""Czech C2 phrases for nuanced, spontaneous and accountable interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "cs_style_dialogue_c2",
        "C2",
        "Zvolit přirozený tón a zachovat obsah",
        "📝",
        [
            PhrasebookEntry(
                "Řeknu to méně úředně: potřebujeme váš souhlas, jinak nemůžeme pokračovat.",
                "Zpřístupnění formálního sdělení bez oslabení podmínky.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Můžeme ubrat na formálnosti, ale ta podmínka musí zůstat výslovná.",
                "Společná redakce dopisu, jehož přátelský tón nesmí změnit obsah dohody.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Ta věta vyznívá jako pokyn; zamýšlíme ji ale pouze jako doporučení.",
                "Upozornění na nechtěnou závaznost připravovaného textu.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Zkusím to rozdělit: nejdřív ověříme údaje, teprve potom potvrdíme termín.",
                "Zpřehlednění hutného vysvětlení během hovoru se zákazníkem.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Zní to trochu strojeně. Co kdybychom poděkovali prostě za konkrétní pomoc?",
                "Návrh civilnějšího poděkování při přípravě společného projevu.",
                "neutral",
                "c2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_humour_dialogue_c2",
        "C2",
        "Zachytit narážku a napravit nepovedený vtip",
        "💬",
        [
            PhrasebookEntry(
                "Myslíš to vážně, nebo narážíš na to, jak to dopadlo minule?",
                "Ověření ironie mezi známými, když samotný tón nestačí.",
                "informal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Ten vtip vyzněl na tvůj účet. To jsem nechtěl a mrzí mě to.",
                "Přijetí odpovědnosti za zraňující účinek žertu bez zpochybnění reakce druhého.",
                "informal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Dobře, to rýpnutí beru. A teď vážně: jak to opravíme?",
                "Přijetí přátelského škádlení a návrat k řešení společného problému.",
                "informal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Když říkám, že mám nabitý den, neznamená to, že se nechci sejít.",
                "Zrušení nechtěného náznaku odmítnutí při domlouvání setkání.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "S tou mou slavnou organizací bych měl nejdřív najít vlastní poznámky.",
                "Sebeironie při drobném zmatku, která nepřenáší vinu na ostatní.",
                "informal",
                "c2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_premises_dialogue_c2",
        "C2",
        "Opravit předpoklad a vést věcný spor",
        "🔎",
        [
            PhrasebookEntry(
                "Než vysvětlím důvod, upřesním jednu věc: o opakovanou změnu nešlo.",
                "Odpověď na otázku, která neoprávněně předpokládá opakování události.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Nezpochybňuji, že se platba posunula; nesouhlasím s označením sleva.",
                "Oddělení uznaného faktu od sporného ekonomického pojmenování.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Kterou moji větu vykládáte jako souhlas s cenou?",
                "Výzva k doložení závazku, který vám druhá strana připisuje.",
                "neutral",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "To označení nechme na chvíli stranou. Shodneme se aspoň na tom, co se stalo?",
                "Návrat od sporu o hodnotící nálepku ke společně ověřitelným skutečnostem.",
                "neutral",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Neříkám, že to nejde; říkám, že to za těchto podmínek nemohu slíbit.",
                "Oprava příliš silného výkladu vlastního stanoviska během jednání.",
                "neutral",
                "c2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_ambiguity_dialogue_c2",
        "C2",
        "Vyjasnit dvojí čtení a rozdělení rolí",
        "🧭",
        [
            PhrasebookEntry(
                "Mluvíte o Petřině návrhu, nebo o návrhu, který Petra pouze předala?",
                "Vyjasnění rozdílu mezi vlastníkem návrhu a osobou, která jej doručila.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Ta věta připouští dvě čtení. Koho přesně se má omezení týkat?",
                "Redakce nejasného pravidla před jeho rozesláním.",
                "formal",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Doplňme sem raději jméno, ať není sporné, kdo má odpovědět.",
                "Úprava zápisu, v němž zájmeno může odkazovat k více účastníkům.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "To je pravděpodobný výklad, ale z té jediné věty nevyplývá jednoznačně.",
                "Zastavení nepodloženého závěru při společném čtení smlouvy.",
                "formal",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Když to rozepíšu takto, zůstává podle vás zachované, kdo co udělal?",
                "Kontrola věrnosti srozumitelnější verze se znalcem původní události.",
                "neutral",
                "c2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_commitments_dialogue_c2",
        "C2",
        "Vyjednat přesný rozsah příslibu",
        "🤝",
        [
            PhrasebookEntry(
                "Mohu slíbit, že žádost předložím, nikoli že jí rada vyhoví.",
                "Vymezení vlastního závazku a pravomoci při žádosti o výjimku.",
                "formal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Platí ta výjimka jen pro lhůtu, nebo také pro povinnost dodat potvrzení?",
                "Ověření dosahu výjimky, než se na ni žadatel spolehne.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "S cenou souhlasíme za předpokladu, že zahrnuje i uvedení do provozu.",
                "Podmíněný souhlas, který brání dodatečnému účtování podstatné části služby.",
                "formal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Berme to zatím jako možnost k prověření, ne jako potvrzený termín.",
                "Oprava příliš optimistického shrnutí přímo během telefonického jednání.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "V termínu ustoupit můžeme; na písemném souhlasu ale trváme.",
                "Oddělení vyjednatelného bodu od nepřekročitelné podmínky.",
                "formal",
                "c2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_perspective_dialogue_c2",
        "C2",
        "Vyprávět s odstupem a citlivě reagovat",
        "🎭",
        [
            PhrasebookEntry(
                "Tehdy mi to připadalo jako katastrofa; dnes to vidím spíš jako drahou lekci.",
                "Vyprávění osobní zkušenosti s rozlišením tehdejšího a dnešního pohledu.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "To hodnocení patří postavě; nebral bych ho automaticky jako stanovisko vypravěče.",
                "Diskuse o pasáži, v níž se vyprávění přibližuje perspektivě postavy.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Říct, že to nebylo ideální, je v tuhle chvíli dost mírné hodnocení.",
                "Upozornění na zdrženlivé pojmenování závažného praktického problému.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Nechci tu zkušenost zlehčovat; jen vysvětluji, proč jsem tehdy reagoval jinak.",
                "Zachování respektu k druhému při porovnávání odlišných reakcí.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Na vlastní účet se tomu zasměju, ale z vašeho zklamání si legraci dělat nechci.",
                "Vymezení přijatelné sebeironie při citlivém společném hodnocení neúspěchu.",
                "neutral",
                "c2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_repair_dialogue_c2",
        "C2",
        "Pohotově se opravit a věrně shrnout dohodu",
        "🔄",
        [
            PhrasebookEntry(
                "To jsem řekl příliš silně. Přesněji: zavazuji se to prověřit, ne schválit.",
                "Okamžitá oprava neúmyslného příslibu během živé debaty.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Dopovím jen tu podmínku a hned vám předám slovo.",
                "Zdvořilé udržení slova, aby přerušení nezkreslilo rozsah závazku.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Do zápisu patří i to, že Jana účast zatím nepotvrdila.",
                "Zachování otevřeného bodu při zkracování záznamu z porady.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Shrnu to pro zákazníka jednodušeji, ale doporučení zůstane doporučením.",
                "Převod odborného závěru do srozumitelné zprávy bez přidání povinnosti.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Ověřme si závěr: domluvili jsme další jednání, nikoli konečnou cenu.",
                "Závěrečná kontrola shody, když během vyjednávání zaznělo několik návrhů.",
                "formal",
                "c2-unit-8",
            ),
        ],
    ),
]
