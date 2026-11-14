"""Czech C2 placement items for nuanced interpretation and precise reformulation."""

from app.data._types import AssessmentQuestion

C2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "cs-g-c2-001",
        "grammar",
        "C2",
        "Vedoucí při jednání řekla: „Zkusím s účetní probrat, zda by šlo splátku "
        "odložit.“ Který zápis zachovává rozdělení rolí i sílu jejího příslibu?",
        [
            "Účetní prověří odklad splátky a vedoucí následně potvrdí nový termín.",
            "Vedoucí s účetní dohodne odklad splátky, bude-li změna administrativně možná.",
            "Vedoucí se pokusí projednat s účetní možnost odkladu splátky.",
            "Vedoucí přislíbila odklad splátky s výhradou následného vyjádření účetní.",
        ],
        "Vedoucí se pokusí projednat s účetní možnost odkladu splátky.",
        "cs-commitment-scope-c2",
    ),
    AssessmentQuestion(
        "cs-g-c2-002",
        "grammar",
        "C2",
        "Novinář se ptá: „Proč jste zase obešli obyvatele?“ Mluvčí chce nejprve "
        "zpochybnit předpoklad o minulosti, ne rovnou vysvětlovat dnešní postup. "
        "Která odpověď tento záměr naplňuje?",
        [
            "Nesouhlasíme s tím, že jsme obyvatele už dříve obešli. " "Z jakého případu vycházíte?",
            "Tentokrát jsme postupovali rychleji, "
            "protože jsme neměli čas na další veřejné setkání.",
            "Víme, že předchozí vynechání obyvatel vzbudilo odpor; "
            "dnešní okolnosti jsou však jiné.",
            "Příště obyvatele oslovíme dříve, "
            "abychom předešli podobnému hodnocení našeho postupu.",
        ],
        "Nesouhlasíme s tím, že jsme obyvatele už dříve obešli. " "Z jakého případu vycházíte?",
        "cs-presupposition-repair-c2",
    ),
    AssessmentQuestion(
        "cs-g-c2-003",
        "grammar",
        "C2",
        "Pravidlo zní: „Po 22. hodině se sál nepoužívá. Výjimku mají uzavřené akce, "
        "pokud je předem schválí správce. Povinnost uklidit platí i pro ně.“ "
        "Které shrnutí zachovává všechny podmínky?",
        [
            "Uzavřená akce může pokračovat po 22. hodině, "
            "pokud správce předem schválí způsob úklidu.",
            "Správce může povolit provoz po 22. hodině i veřejné akci, "
            "jestliže pořadatel zajistí úklid.",
            "Předem schválená uzavřená akce má po 22. hodině výjimku z provozního omezení i úklidu.",
            "Po 22. hodině smí pokračovat předem schválená uzavřená akce; uklidit se musí i po ní.",
        ],
        "Po 22. hodině smí pokračovat předem schválená uzavřená akce; uklidit se musí i po ní.",
        "cs-nested-conditions-c2",
    ),
    AssessmentQuestion(
        "cs-g-c2-004",
        "grammar",
        "C2",
        "Redaktorka chce v písemném pravidle omezit okruh osob oprávněných stáhnout "
        "návrh, nikoli rozsah Janiných ostatních oprávnění. Která formulace to "
        "vyjadřuje jednoznačně?",
        [
            "Jana může návrh jen stáhnout; k jeho úpravě oprávněna není.",
            "Jen Jana může návrh stáhnout; ostatní k tomu oprávnění nemají.",
            "Jana může stáhnout jen tento návrh; ostatní návrhy stáhnout nesmí.",
            "Jana může návrh stáhnout jen dnes; zítra už toto oprávnění nemá.",
        ],
        "Jen Jana může návrh stáhnout; ostatní k tomu oprávnění nemají.",
        "cs-focus-particles-c2",
    ),
    AssessmentQuestion(
        "cs-g-c2-005",
        "grammar",
        "C2",
        "V debatě zazní: „To nebyla úspora. Tu částku jen zaplatíme příští rok.“ "
        "Co mluvčí druhou větou objasňuje?",
        [
            "Odmítá pojmenování změny jako snížení nákladů, nikoli samotný posun platby.",
            "Odmítá posun platby do příštího roku, nikoli možnost snížit celkovou částku.",
            "Odmítá letošní úsporu, ale potvrzuje, že příští rok bude celková částka nižší.",
            "Odmítá zahrnout platbu do nákladů, protože její výši určí až příští rok.",
        ],
        "Odmítá pojmenování změny jako snížení nákladů, nikoli samotný posun platby.",
        "cs-metalinguistic-negation-c2",
    ),
    AssessmentQuestion(
        "cs-g-c2-006",
        "grammar",
        "C2",
        "Koordinátorka říká: „Někteří už odpověděli — možná dokonce všichni, ještě "
        "jsem to nespočítala.“ Jaký účinek má doplnění za pomlčkou?",
        [
            "Opravuje první část a potvrzuje, že odpověděli všichni oslovení.",
            "Zpochybňuje první část, protože připouští, že odpovědi zatím vůbec nepřišly.",
            "Ruší možný dojem neúplné skupiny, aniž potvrzuje odpověď všech oslovených.",
            "Rozšiřuje okruh oslovených o další lidi, jejichž odpovědi nebyly očekávány.",
        ],
        "Ruší možný dojem neúplné skupiny, aniž potvrzuje odpověď všech oslovených.",
        "cs-cancellable-implicature-c2",
    ),
    AssessmentQuestion(
        "cs-g-c2-007",
        "grammar",
        "C2",
        "V zápisu stojí: „Po zamítnutí žádosti komisí se spolek odvolal.“ Která "
        "slovesná verze zachovává původce obou dějů a jejich pořadí?",
        [
            "Když spolek zamítl žádost komise, komise se proti tomu odvolala.",
            "Komise zamítla žádost a spolek se poté proti zamítnutí odvolal.",
            "Spolek se odvolal proti žádosti a komise poté jeho odvolání zamítla.",
            "Komise zamítla odvolání spolku, který předtím žádost stáhl.",
        ],
        "Komise zamítla žádost a spolek se poté proti zamítnutí odvolal.",
        "cs-nominal-compression-c2",
    ),
    AssessmentQuestion(
        "cs-g-c2-008",
        "grammar",
        "C2",
        "Dodavatel říká: „Zítra vám pošlu výsledek — přesněji, zítra vám potvrdím, "
        "kdy bude hotový.“ Co lze po této opravě zaznamenat jako jeho příslib?",
        [
            "Zítra pošle výsledek a současně potvrdí, kdy práce skončily.",
            "Zítra výsledek dokončí, datum odeslání však ještě nechává otevřené.",
            "Pokusí se zítra zjistit termín, ale jeho sdělení zatím neslibuje.",
            "Zítra oznámí termín dokončení; doručení výsledku na zítřek neslibuje.",
        ],
        "Zítra oznámí termín dokončení; doručení výsledku na zítřek neslibuje.",
        "cs-ellipsis-and-repair-c2",
    ),
    AssessmentQuestion(
        "cs-v-c2-001",
        "vocabulary",
        "C2",
        "Zástupkyně týmu říká: „Mám mandát projednat cenu, podpis smlouvy si ale "
        "vyhradilo vedení.“ Co tím vymezuje?",
        [
            "Může schválit cenu a smlouva je tím závazná, vedení už doplní jen podpis.",
            "Smí o ceně jednat za tým, ale smlouvu podle tohoto pověření podepsat nesmí.",
            "Smí smlouvu podepsat, pokud při cenovém jednání nepřekročí původní nabídku.",
            "Může pouze předat cenovou nabídku, protože vyjednávání si ponechalo vedení.",
        ],
        "Smí o ceně jednat za tým, ale smlouvu podle tohoto pověření podepsat nesmí.",
    ),
    AssessmentQuestion(
        "cs-v-c2-002",
        "vocabulary",
        "C2",
        "Po schůzce někdo shrne: „Tereza nechce spolupracovat.“ Tereza přitom "
        "odmítla pouze navržený termín. Která reakce přesně pojmenovává problém?",
        [
            "Tereza svou výhradu zlehčila, protože termín označila za jediný problém.",
            "Tereza předjímá výsledek jednání, když žádá o jiný termín spolupráce.",
            "Shrnutí zestručňuje její odmítnutí, ale zachovává rozsah jejího postoje.",
            "Shrnutí jí podsouvá širší odmítnutí, než jaké skutečně vyjádřila.",
        ],
        "Shrnutí jí podsouvá širší odmítnutí, než jaké skutečně vyjádřila.",
    ),
    AssessmentQuestion(
        "cs-v-c2-003",
        "vocabulary",
        "C2",
        "Kolega vám po nepovedeném žertu řekne: „Tím ses trefil do citlivého místa.“ "
        "Chcete uznat účinek poznámky a napravit vztah, ne obhajovat humor. "
        "Která odpověď tomu odpovídá?",
        [
            "Mrzí mě, že jsem se tě dotkl. Mířil jsem na tu situaci, ne na tebe; "
            "příště si na to dám pozor.",
            "Mrzí mě, že vtip nevyšel. Zkusím ho říct jinak, "
            "aby bylo zřejmé, proč mi připadal vtipný.",
            "Mrzí mě, že jsme se nepochopili. Než budeme pokračovat, "
            "vysvětlím ti, jak se podobné vtipy myslí.",
            "Mrzí mě to nedorozumění. Počkáme, až opadne napětí, "
            "a pak se k tomu stejnému vtipu vrátíme.",
        ],
        "Mrzí mě, že jsem se tě dotkl. Mířil jsem na tu situaci, ne na tebe; "
        "příště si na to dám pozor.",
    ),
    AssessmentQuestion(
        "cs-v-c2-004",
        "vocabulary",
        "C2",
        "Redaktorka chce „civilní poděkování bez okázalých formulí“, přitom chce "
        "zachovat zdvořilost a uvést konkrétní přínos. Která verze nejlépe odpovídá?",
        [
            "Dovolte nám vyjádřit nejhlubší uznání za vaše mimořádně obětavé dodání podkladů.",
            "Tímto se zaznamenává, že včasné předání podkladů z vaší strany splnilo svůj účel.",
            "Děkujeme, že jste podklady dodali včas. Díky tomu jsme mohli dodržet termín.",
            "No vida, podklady tentokrát přišly včas, takže se ten termín nakonec stihl.",
        ],
        "Děkujeme, že jste podklady dodali včas. Díky tomu jsme mohli dodržet termín.",
    ),
    AssessmentQuestion(
        "cs-r-c2-001",
        "reading",
        "C2",
        "Přečtěte si úryvek: „Eva otevřela nabídku a porovnala částku s rozpočtem. "
        "Tak tohle měla být ta velkorysá pomoc? Za to sotva zaplatí dopravu. "
        "Dopis složila a odložila.“ Které shrnutí zachovává perspektivu úryvku?",
        [
            "Vypravěč uvádí, že dárce chtěl Evu nízkou částkou urazit, a Eva jeho úmysl rozpoznává.",
            "Eva přijímá nabídku jako velkorysou, ale vypravěč upozorňuje na nepokryté náklady.",
            "Eva se obává vysoké ceny dopravy, hodnotu nabídky však úryvek nechává bez hodnocení.",
            "Úryvek přibližuje Evinu nespokojenost s nabídkou, aniž dokládá dárcův úmysl.",
        ],
        "Úryvek přibližuje Evinu nespokojenost s nabídkou, aniž dokládá dárcův úmysl.",
        "cs-represented-voice-c2",
    ),
    AssessmentQuestion(
        "cs-r-c2-002",
        "reading",
        "C2",
        "Přečtěte si výměnu: „Naše nová linka vše vyřídí bez čekání,“ slíbil "
        "dodavatel. Po třetím přepojení a čtyřiceti minutách kolegyně poznamenala: "
        "„Tak tomu říkám bez čekání.“ Co její poznámka v tomto kontextu nejspíše dělá?",
        [
            "Oceňuje, že přepojování na nové lince probíhá rychleji než dřívější čekání.",
            "Vrací dodavateli jeho slib jako ironický komentář k rozporu se zkušeností.",
            "Žádá kolegu, aby dobu přepojování nepočítal do celkové délky čekání.",
            "Připouští, že slib platil pro vyřízení požadavku, nikoli pro spojení s obsluhou.",
        ],
        "Vrací dodavateli jeho slib jako ironický komentář k rozporu se zkušeností.",
        "cs-ironic-echo-c2",
    ),
    AssessmentQuestion(
        "cs-r-c2-003",
        "reading",
        "C2",
        "Zápis uvádí: „Jana řekla Petře, že Petr její žádost do pátku doplní.“ "
        "Jiné údaje nejsou k dispozici. Redaktor chce ve shrnutí výslovně uvést "
        "vlastnici žádosti. Který postup je věcně obhajitelný?",
        [
            "Uvést Petru jako žadatelku; zájmeno vyložit podle osoby, které Jana zprávu sděluje.",
            "Uvést Janu jako žadatelku; Petrovi ponechat pouze roli osoby doplňující podklady.",
            "Vyžádat si upřesnění; věta sama neumožňuje bezpečně zvolit vlastnici žádosti.",
            "Zapsat, že žádost podala Petra za Janu, a její doplnění ponechat Petrovi.",
        ],
        "Vyžádat si upřesnění; věta sama neumožňuje bezpečně zvolit vlastnici žádosti.",
        "cs-reference-resolution-c2",
    ),
    AssessmentQuestion(
        "cs-r-c2-004",
        "reading",
        "C2",
        "Posudek uvádí: „Návrh není bez předností. Jeho provozní náklady však zatím "
        "neznáme, a proto jej v této podobě nedoporučujeme přijmout. Upravenou verzi "
        "rádi znovu posoudíme.“ Která zpráva pro členy spolku je věrná posudku?",
        [
            "Posudek uznává určité přednosti, nynější přijetí nedoporučuje "
            "a připouští nové posouzení úprav.",
            "Posudek přednosti zatím nepotvrzuje; návrh doporučí "
            "po pouhém doplnění údaje o nákladech.",
            "Posudek doporučuje návrh přijmout pod podmínkou, "
            "že se později prověří provozní náklady.",
            "Posudek uznává přednosti a předběžně schvaluje upravenou verzi, "
            "pokud se náklady nezvýší.",
        ],
        "Posudek uznává určité přednosti, nynější přijetí nedoporučuje "
        "a připouští nové posouzení úprav.",
        "cs-understatement-c2",
    ),
]
