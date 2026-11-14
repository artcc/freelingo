"""Czech C1 phrases for qualified judgement and constructive interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "cs_evidence_dialogue_c1",
        "C1",
        "Posouzení podkladů",
        "🔎",
        [
            PhrasebookEntry(
                "Z čeho přesně tento závěr vyvozujeme a co zatím zůstává jen odhadem?",
                "Na pracovní poradě oddělujete zjištěné údaje od předpokladů.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Podle dostupných údajů se situace zlepšuje, na celkové hodnocení je ale brzy.",
                "Představujete průběžné výsledky bez předčasného zobecnění.",
                "formal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Tohle mám zatím jen z doslechu; než se podle toho zařídíme, radši to ověřím.",
                "V neformálním rozhovoru upozorňujete na neověřený původ zprávy.",
                "informal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Můžeme tento údaj vztáhnout i na menší obce, nebo se týká jen krajských měst?",
                "Při čtení průzkumu ověřujete rozsah platnosti jeho výsledků.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Absence stížností sama o sobě ještě nemusí znamenat spokojenost.",
                "Upozorňujete na jiné možné vysvětlení zdánlivě příznivého výsledku.",
                "formal",
                "c1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_argument_dialogue_c1",
        "C1",
        "Věcná argumentace",
        "💬",
        [
            PhrasebookEntry(
                "S východiskem souhlasím, ale tento závěr z něj podle mě nevyplývá.",
                "Oddělujete přijatelný předpoklad od sporného kroku v argumentaci.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Nezpochybňuji účel opatření, nýbrž způsob jeho provedení.",
                "Na veřejné diskusi upřesňujete, kterou část návrhu kritizujete.",
                "formal",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Pokud jde o pořizovací cenu, máme jasno; zbývá posoudit provozní náklady.",
                "Rozdělujete složitou debatu na již vyřešenou otázku a další krok.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Jak by váš návrh fungoval v případě, že by se počet zájemců zdvojnásobil?",
                "Prověřujete použitelnost argumentu v jiné realistické situaci.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Ten příklad je přesvědčivý, jen bych z něj zatím nedělal obecné pravidlo.",
                "V rozhovoru uznáváte zkušenost druhého a zároveň bráníte ukvapenému zobecnění.",
                "informal",
                "c1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_negotiation_dialogue_c1",
        "C1",
        "Vyjednávání přijatelné dohody",
        "🤝",
        [
            PhrasebookEntry(
                "Na delší dobu trvání smlouvy můžeme přistoupit, pokud ji půjde předčasně ukončit.",
                "Nabízíte ústupek a současně formulujete konkrétní ochrannou podmínku.",
                "formal",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "V termínu vám vyjdeme vstříc; potřebujeme ale zachovat dohodnutý rozsah.",
                "Oddělujete oblast možného ústupku od požadavku, který chcete ponechat.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "I kdyby cena klesla, bez záruky dostupnosti služby bychom nabídku nepřijali.",
                "Vysvětlujete, proč samotná sleva neřeší rozhodující překážku.",
                "formal",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Pojďme si zapsat, za jakých okolností se k dohodě znovu vrátíme.",
                "Před uzavřením jednání navrhujete výslovně zachytit podmínky nové diskuse.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "To už je mimo můj mandát; mohu ale navrhnout variantu k dalšímu schválení.",
                "Otevřeně sdělujete hranici svého oprávnění a nabízíte další postup.",
                "formal",
                "c1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_accountability_dialogue_c1",
        "C1",
        "Jasný zápis a rozdělení úkolů",
        "📋",
        [
            PhrasebookEntry(
                "Rozumím správně, že byl schválen pouze záměr, nikoli konečný rozpočet?",
                "Před zveřejněním zápisu ověřujete rozsah přijatého rozhodnutí.",
                "formal",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Kdo se ujme doplnění podkladů a do kdy je může předat?",
                "Měníte obecný požadavek v konkrétní úkol s odpovědnou osobou a termínem.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Prosím, zaznamenejme i důvod, proč tato připomínka nebyla přijata.",
                "Žádáte dohledatelné vypořádání připomínky, nejen údaj o výsledku.",
                "formal",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Já jsem slíbil zjistit možnosti, ne zajistit schválení.",
                "Opravujete příliš široký výklad vlastního závazku.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "V zápisu se mluví o předání, ale není uvedeno, kdo komu dokument předá.",
                "Upozorňujete na chybějící účastníky děje v příliš zhuštěné formulaci.",
                "neutral",
                "c1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_cohesion_dialogue_c1",
        "C1",
        "Přehledné vysvětlování",
        "🧩",
        [
            PhrasebookEntry(
                "Než přejdu k doporučení, shrnu dvě omezení této analýzy.",
                "V prezentaci připravujete posluchače na závěr s jasně uvedenými výhradami.",
                "formal",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Když říkáte tento postup, myslíte tím výběr dodavatele, nebo kontrolu výsledku?",
                "Odstraňujete nejasný odkaz na jednu ze dvou předchozích činností.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "To souvisí s předchozím bodem, liší se ale způsob financování.",
                "Propojujete témata a zároveň pojmenováváte důležitý rozdíl.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Vrátím se k hlavní otázce: co z těchto zjištění plyne pro příští rok?",
                "Po užitečné odbočce vracíte výklad k rozhodnutí, které je potřeba učinit.",
                "formal",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Zkusím to říct stručněji, ale tu výhradu k termínu bych nerad vypustil.",
                "Při společném psaní zkracujete text bez ztráty podstatného omezení.",
                "informal",
                "c1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_interaction_dialogue_c1",
        "C1",
        "Nesouhlas a náprava nedorozumění",
        "🗣️",
        [
            PhrasebookEntry(
                "Proti tomuto výkladu se musím ohradit; mou připomínku jste vztáhl na celý tým.",
                "Věcně odmítáte nepřesnou interpretaci svého výroku.",
                "formal",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Vyjádřil jsem se nepřesně: nejde o odmítnutí, ale o žádost o doplnění.",
                "Opravujete vlastní sdělení dříve, než se nedorozumění prohloubí.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Nešlo by nejdřív vyslechnout i kolegy, kteří se zatím nedostali ke slovu?",
                "Zdvořile žádáte rovnoměrnější zapojení účastníků do diskuse.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Chápu, že je to naléhavé. Dnes mohu nabídnout konzultaci, nikoli hotové řešení.",
                "Uznáváte potřebu druhé strany a zároveň vymezujete splnitelnou pomoc.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Počkej, na tom jsme se ještě neshodli; já jsem jen navrhl, ať to prověříme.",
                "V neformální debatě opravujete předpoklad již dosaženého souhlasu.",
                "informal",
                "c1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_mediation_dialogue_c1",
        "C1",
        "Zprostředkování rozdílných pohledů",
        "🌉",
        [
            PhrasebookEntry(
                "Obě strany chtějí předvídatelný provoz, rozcházejí se však v navržené otevírací době.",
                "Při jednání obyvatel s provozovatelem oddělujete společný zájem od sporu.",
                "formal",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Zkusím vaše stanovisko shrnout a prosím vás o opravu, pokud něco vyložím nepřesně.",
                "Před zprostředkováním názoru nabízíte jeho nositeli možnost upřesnění.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Souhlas s měřením ještě neznamená souhlas s navrženým omezením.",
                "Bráníte tomu, aby dílčí dohoda byla prezentována jako přijetí celého řešení.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Do zprávy bych uvedl, že se o kontrolu pokusíte, ne že je její dokončení zaručeno.",
                "Při úpravě formálního shrnutí zachováváte původní míru závazku.",
                "formal",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Teď si nejsem jistý, jestli si děláš legraci, nebo ti na tom opravdu něco vadí.",
                "V osobním rozhovoru ověřujete podtext namísto automatické obranné reakce.",
                "informal",
                "c1-unit-7",
            ),
        ],
    ),
]
