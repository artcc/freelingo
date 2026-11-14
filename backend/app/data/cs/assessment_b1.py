"""Czech B1 placement questions with balanced answer positions within each skill."""

from app.data._types import AssessmentQuestion

B1_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "cs-g-b1-001",
        "grammar",
        "B1",
        "Pavel říká: Dopis jsem psal celé dopoledne, ale ještě ho musím dokončit. "
        "Co z jeho slov vyplývá?",
        [
            "Pavel dopis dokončil a čeká na odpověď.",
            "Pavel se psaním strávil čas, ale dopis není hotový.",
            "Pavel chce s psaním začít až odpoledne.",
            "Pavel dopis dokončil během několika minut.",
        ],
        "Pavel se psaním strávil čas, ale dopis není hotový.",
        "cs-narrative-aspect-b1",
    ),
    AssessmentQuestion(
        "cs-g-b1-002",
        "grammar",
        "B1",
        "Doplňte popis dnešní konkrétní cesty: Obvykle do práce jezdím tramvají, "
        "ale právě teď ___ pěšky přes park.",
        ["jezdím", "pojedu", "odjel jsem", "jdu"],
        "jdu",
        "cs-motion-direction-b1",
    ),
    AssessmentQuestion(
        "cs-g-b1-003",
        "grammar",
        "B1",
        "Doplňte: To je kolegyně, ___ jsem včera pomohl s formulářem.",
        ["které", "kterou", "která", "kterých"],
        "které",
        "cs-relative-clauses-b1",
    ),
    AssessmentQuestion(
        "cs-g-b1-004",
        "grammar",
        "B1",
        "Mluvčí je žena a popisuje, co by sama dělala v představované situaci. Doplňte: "
        "Kdybych měla volné večery, ___ na kurz.",
        ["chodil bych", "chodila by", "chodila bych", "chodila bys"],
        "chodila bych",
        "cs-kdyby-b1",
    ),
    AssessmentQuestion(
        "cs-g-b1-005",
        "grammar",
        "B1",
        "Doplňte správný tvar: Zajímám se o ___, který začíná v září.",
        ["novém kurzu", "nový kurz", "novému kurzu", "novým kurzem"],
        "nový kurz",
        "cs-prepositional-government-b1",
    ),
    AssessmentQuestion(
        "cs-g-b1-006",
        "grammar",
        "B1",
        "V pondělí Eva řekla: Přijdu zítra. Ve středu předáváte pouze obsah jejího "
        "pondělního sdělení. Která věta zachovává zamýšlený den příchodu?",
        [
            "Eva v pondělí řekla, že přijde v úterý.",
            "Eva v pondělí řekla, že přijde ve středu.",
            "Eva v pondělí řekla, že přijde ve čtvrtek.",
            "Eva v pondělí řekla, že přijde v pátek.",
        ],
        "Eva v pondělí řekla, že přijde v úterý.",
        "cs-reported-speech-b1",
    ),
    AssessmentQuestion(
        "cs-g-b1-007",
        "grammar",
        "B1",
        "Která věta zachovává význam sdělení: I když pršelo, vyrazili jsme na výlet?",
        [
            "Pršelo, proto jsme na výlet nevyrazili.",
            "Nepršelo, a tak jsme vyrazili na výlet.",
            "Vyrazili jsme na výlet, protože pršelo.",
            "Pršelo, přesto jsme vyrazili na výlet.",
        ],
        "Pršelo, přesto jsme vyrazili na výlet.",
        "cs-concession-b1",
    ),
    AssessmentQuestion(
        "cs-g-b1-008",
        "grammar",
        "B1",
        "Chcete říct, že vám s žádostí nepomohla ani jedna osoba. Která věta to vyjadřuje?",
        [
            "Ne všichni mi s žádostí pomohli.",
            "Někdo mi s žádostí nepomohl.",
            "Nikdo mi s žádostí nepomohl.",
            "Každý mi s žádostí pomohl.",
        ],
        "Nikdo mi s žádostí nepomohl.",
        "cs-negative-concord-b1",
    ),
    AssessmentQuestion(
        "cs-v-b1-001",
        "vocabulary",
        "B1",
        "Trať se opravuje a mezi dvěma stanicemi musíte místo vlaku jet autobusem. "
        "Které označení budete hledat na směrovkách?",
        ["Zpáteční jízdenky", "Povinné rezervace", "Náhradní doprava", "Úschova zavazadel"],
        "Náhradní doprava",
    ),
    AssessmentQuestion(
        "cs-v-b1-002",
        "vocabulary",
        "B1",
        "Před převzetím bytu posíláte vratnou částku pro případ škody nebo nezaplaceného "
        "nájmu. Jak se tato částka běžně nazývá?",
        ["Kauce", "Provize", "Přeplatek", "Sleva"],
        "Kauce",
    ),
    AssessmentQuestion(
        "cs-v-b1-003",
        "vocabulary",
        "B1",
        "Zaměstnavatel chce dokument, ve kterém najde vaše předchozí zaměstnání, "
        "vzdělání a dovednosti. Co pošlete?",
        ["Účtenku", "Domovní řád", "Jízdní řád", "Životopis"],
        "Životopis",
    ),
    AssessmentQuestion(
        "cs-v-b1-004",
        "vocabulary",
        "B1",
        "Úřednice říká: Chybějící doklad musíte dodat do deseti dnů. "
        "Které slovo označuje tuto stanovenou dobu?",
        ["Směna", "Lhůta", "Výluka", "Záloha"],
        "Lhůta",
    ),
    AssessmentQuestion(
        "cs-v-b1-005",
        "vocabulary",
        "B1",
        "Kolegyně napsala jen: Sejdeme se odpoledne. Potřebujete znát přesnou hodinu. "
        "Která žádost nejlépe odpovídá vašemu cíli?",
        [
            "Můžeš prosím zrušit naši schůzku?",
            "Můžeš prosím předat moji omluvu?",
            "Můžeš prosím upřesnit čas schůzky?",
            "Můžeš prosím rozdělit naše úkoly?",
        ],
        "Můžeš prosím upřesnit čas schůzky?",
    ),
    AssessmentQuestion(
        "cs-v-b1-006",
        "vocabulary",
        "B1",
        "Nově koupená konvice netopí. Chcete u prodejce uplatnit požadavek "
        "na řešení této vady. Co chcete podat?",
        ["Přihlášku", "Objednávku", "Pozvánku", "Reklamaci"],
        "Reklamaci",
    ),
    AssessmentQuestion(
        "cs-v-b1-007",
        "vocabulary",
        "B1",
        "Za tuto lednici zaplatíte méně při nákupu, ale každý měsíc bude potřebovat "
        "více elektřiny. Která vlastnost může zvýšit vaše pozdější výdaje?",
        ["Nižší kauce", "Vyšší spotřeba", "Kratší objížďka", "Větší sleva"],
        "Vyšší spotřeba",
    ),
    AssessmentQuestion(
        "cs-v-b1-008",
        "vocabulary",
        "B1",
        "Na sousedské slavnosti pomáháte připravit sál. Nikdo vám to nenařídil "
        "a za pomoc nedostáváte zaplaceno. V jaké roli se účastníte?",
        ["Jako dobrovolník", "Jako pronajímatel", "Jako uchazeč o práci", "Jako průvodčí"],
        "Jako dobrovolník",
    ),
    AssessmentQuestion(
        "cs-r-b1-001",
        "reading",
        "B1",
        "Na nádraží čtete: Kvůli opravě tratě je mezi Turnovem a Železným Brodem "
        "zavedena náhradní autobusová doprava. Autobusy odjíždějí od hlavního vchodu, "
        "nikoli z nástupiště. Jízdenky na vlak zůstávají v platnosti. "
        "Co má udělat cestující s platnou vlakovou jízdenkou, který jede tímto úsekem?",
        [
            "Počkat na svém nástupišti na příjezd náhradního autobusu.",
            "Koupit novou autobusovou jízdenku a zůstat na nástupišti.",
            "Vrátit vlakovou jízdenku a cestu odložit do konce opravy.",
            "Přejít k hlavnímu vchodu a použít původní jízdenku v autobusu.",
        ],
        "Přejít k hlavnímu vchodu a použít původní jízdenku v autobusu.",
    ),
    AssessmentQuestion(
        "cs-r-b1-002",
        "reading",
        "B1",
        "Inzerát uvádí: Nájem 14 000 Kč měsíčně, zálohy na služby 3 000 Kč. "
        "Elektřinu si nájemník platí zvlášť dodavateli. Kauce činí 28 000 Kč. "
        "Co víte o pravidelných měsíčních výdajích?",
        [
            "Částka 14 000 Kč zahrnuje služby i veškerou elektřinu.",
            "K částce 17 000 Kč je nutné připočítat platbu za elektřinu.",
            "Částka 28 000 Kč se připočítává ke každému měsíčnímu nájmu.",
            "Služby se zaplatí pouze při nastěhování a další měsíce už ne.",
        ],
        "K částce 17 000 Kč je nutné připočítat platbu za elektřinu.",
    ),
    AssessmentQuestion(
        "cs-r-b1-003",
        "reading",
        "B1",
        "Organizátor kurzu píše: Děkujeme za vyplnění přihlášky. Místo vám rezervujeme "
        "po přijetí platby. Pokud peníze nedorazí do pátku, nabídneme místo dalšímu "
        "zájemci. Co má zájemce udělat, aby měl místo rezervované?",
        [
            "Poslat v pátek další přihlášku se stejnými údaji.",
            "Přijít na první hodinu a zaplatit až po jejím skončení.",
            "Zařídit, aby organizátor dostal platbu nejpozději v pátek.",
            "Počkat, zda se po pátku přihlásí ještě další zájemci.",
        ],
        "Zařídit, aby organizátor dostal platbu nejpozději v pátek.",
    ),
    AssessmentQuestion(
        "cs-r-b1-004",
        "reading",
        "B1",
        "Úřad informuje: Vaši žádost jsme přijali. Chybí však potvrzení o studiu. "
        "Doplňte ho do deseti dnů; teprve potom budeme moci žádost posoudit. "
        "V jakém stavu je žádost?",
        [
            "Je podaná, ale k jejímu posouzení je potřeba další dokument.",
            "Je schválená, potvrzení je nutné jen pro převzetí výsledku.",
            "Je zamítnutá a zájemce musí podat zcela novou žádost.",
            "Je úplná a úřad právě rozhoduje o jejím konečném výsledku.",
        ],
        "Je podaná, ale k jejímu posouzení je potřeba další dokument.",
    ),
    AssessmentQuestion(
        "cs-r-b1-005",
        "reading",
        "B1",
        "Lenka píše kolegovi: Sobotní ranní směnu za tebe můžu vzít, pokud mě zastoupíš "
        "v pondělí odpoledne. Dej mi vědět do zítřka, ať to můžeme potvrdit vedoucí. "
        "Co Lenka navrhuje?",
        [
            "Vezme obě směny, pokud jí vedoucí potvrdí volné úterý.",
            "Vymění si s kolegou směny, jestliže souhlasí s pondělním zastoupením.",
            "Zastoupí kolegu v sobotu bez jakékoli podmínky.",
            "Pondělní směnu zruší, pokud kolega do zítřka neodpoví.",
        ],
        "Vymění si s kolegou směny, jestliže souhlasí s pondělním zastoupením.",
    ),
    AssessmentQuestion(
        "cs-r-b1-006",
        "reading",
        "B1",
        "Sousedé dostali zprávu: Původně jsme chtěli uklízet dvůr ráno. Protože má "
        "dopoledne pršet, začneme až ve dvě. Kdo nemůže zůstat celé odpoledne, "
        "může přijít alespoň na chvíli. Jaké zapojení zpráva umožňuje?",
        [
            "Přijít ráno a dokončit celý úklid ještě před deštěm.",
            "Přijít jen v případě, že člověk může zůstat až do večera.",
            "Přesunout vlastní část úklidu na libovolné jiné dopoledne.",
            "Přijít od dvou hodin a pomoci i po kratší dobu.",
        ],
        "Přijít od dvou hodin a pomoci i po kratší dobu.",
    ),
    AssessmentQuestion(
        "cs-r-b1-007",
        "reading",
        "B1",
        "Zákaznice píše: Levnější pračka měla kratší dodací dobu, ale její roční "
        "spotřeba byla výrazně vyšší. Nakonec jsme si připlatili za úspornější model, "
        "i když jsme na něj museli týden čekat. Proč se rozhodli pro druhý model?",
        [
            "Dali přednost nižší spotřebě před nižší cenou a rychlejším dodáním.",
            "Chtěli nejrychlejší dodání, i když druhý model spotřebuje více.",
            "Potřebovali ušetřit při nákupu a neřešili další náklady.",
            "Vybrali model, který byl levnější a zároveň ihned k odběru.",
        ],
        "Dali přednost nižší spotřebě před nižší cenou a rychlejším dodáním.",
    ),
    AssessmentQuestion(
        "cs-r-b1-008",
        "reading",
        "B1",
        "Petr píše: Omlouvám se, podklady jsem vám včera poslal na starou adresu. "
        "Teď je přeposílám sem. Jestli se příloha neotevře, zavolejte mi a najdeme "
        "jiný způsob předání. Která reakce odpovídá Petrově zprávě, pokud soubor nefunguje?",
        [
            "Požádáte ho, aby další zprávy posílal jen na starou adresu.",
            "Počkáte do příštího týdne, až automaticky pošle tištěnou kopii.",
            "Zavoláte mu a domluvíte se na jiném způsobu doručení podkladů.",
            "Přijdete bez ohlášení, protože osobní převzetí už bylo dohodnuto.",
        ],
        "Zavoláte mu a domluvíte se na jiném způsobu doručení podkladů.",
    ),
]
