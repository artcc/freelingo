"""Czech B2 phrases for clear, tactful and practical interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "cs_clarification_b2",
        "B2",
        "Upřesnění významu",
        "💬",
        [
            PhrasebookEntry(
                "Měl jsem na mysli termín dodání, nikoli cenu.",
                "Opravujete konkrétní nedorozumění ohledně své námitky.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Když říkáte všichni, zahrnujete do toho i externí spolupracovníky?",
                "Ověřujete, koho přesně zahrnuje obecné tvrzení.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Z toho ještě nutně neplyne, že je celý návrh neproveditelný.",
                "Odmítáte příliš široký závěr, ale nepopíráte zmíněnou obtíž.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Rozumím tomu správně, že se mění pouze místo, ne čas?",
                "Před potvrzením účasti kontrolujete rozsah změny.",
                "neutral",
                "b2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_procedures_b2",
        "B2",
        "Jednání s úřadem a poskytovatelem služeb",
        "📋",
        [
            PhrasebookEntry(
                "Můžete mi prosím sdělit, z jakých podkladů rozhodnutí vychází?",
                "Žádáte věcné vysvětlení důvodů úředního nebo pracovního rozhodnutí.",
                "formal",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Ráda bych doplnila údaj, který v odůvodnění chybí.",
                "Upozorňujete na chybějící skutečnost bez obviňování pracovníka.",
                "formal",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Kdo má nyní vyřízení mé žádosti na starosti?",
                "V neosobním sdělení chybí odpovědná osoba a potřebujete další kontakt.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Prosím o potvrzení, že jste obdrželi i všechny přílohy.",
                "Kontrolujete úplnost zaslaného podání.",
                "formal",
                "b2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_sources_b2",
        "B2",
        "Předávání zpráv a ověřování zdrojů",
        "📰",
        [
            PhrasebookEntry(
                "Podle správce by oprava měla skončit v pátek; potvrzené to zatím není.",
                "Předáváte očekávání a zachováváte jeho nejistotu.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Máte tu informaci přímo od organizátorů, nebo zprostředkovaně?",
                "Ověřujete původ zprávy před dalším rozhodnutím.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Nechci mu vkládat do úst něco, co neřekl.",
                "Odmítáte nepřesné převyprávění cizího názoru.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "V zápisu bych rozlišila potvrzené údaje a předběžné odhady.",
                "Navrhujete přesnější shrnutí porady.",
                "neutral",
                "b2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_argumentation_b2",
        "B2",
        "Věcný nesouhlas",
        "⚖️",
        [
            PhrasebookEntry(
                "Vaší námitce rozumím, přesto v tomto řešení vidím větší přínos.",
                "Uznáváte relevantní protiargument a otevíráte vlastní zdůvodnění.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Cena je sice nižší, ale servis v ní zahrnutý není.",
                "Doplňujete omezení důležité pro porovnání nabídek.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Zkusme se na to podívat i z hlediska lidí, kteří dojíždějí.",
                "Rozšiřujete diskusi o potřeby opomenuté skupiny.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Čím déle rozhodnutí odkládáme, tím méně času zbývá na přípravu.",
                "Vysvětlujete praktický důsledek dalšího čekání.",
                "neutral",
                "b2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_agreements_b2",
        "B2",
        "Vyjednání podmínek",
        "🤝",
        [
            PhrasebookEntry(
                "S cenou souhlasíme za předpokladu, že zahrnuje i dopravu.",
                "Vážete přijetí nabídky na konkrétní podmínku.",
                "formal",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "V termínu vám můžeme vyjít vstříc, ve výši zálohy už ne.",
                "Nabízíte omezený ústupek a jasně vymezujete jeho hranici.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Než dohodu potvrdíme, potřebujeme změnu písemně.",
                "Žádáte doložení nové podmínky před konečným souhlasem.",
                "formal",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Můžeme si ujasnit, kdo zajistí podklady a kdo je odešle?",
                "Odstraňujete nejasnost v rozdělení pracovních úkolů.",
                "neutral",
                "b2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_relationships_b2",
        "B2",
        "Citlivé reakce a společenský tón",
        "🙂",
        [
            PhrasebookEntry(
                "To byla nadsázka, nechtěl jsem tě tím shodit.",
                "Vysvětlujete příteli nevydařený vtip a pojmenováváte svůj záměr.",
                "informal",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Nevím, jestli to myslíš vážně, nebo si děláš legraci.",
                "Ověřujete tón poznámky, než na ni zareagujete.",
                "informal",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Chápu, že spěcháte, ale dnes už to bohužel dokončit nemohu.",
                "Zdvořile odmítáte nereálný termín bez neurčitého příslibu.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Promiň, vyznělo to ostřeji, než jsem zamýšlela.",
                "Přebíráte odpovědnost za tón své předchozí reakce.",
                "informal",
                "b2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_mediation_b2",
        "B2",
        "Zprostředkování dohody",
        "🧩",
        [
            PhrasebookEntry(
                "Jestli tomu dobře rozumím, vám jde hlavně o klid a vám o dostupný prostor.",
                "Při společném jednání shrnujete rozdílné potřeby dvou stran.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Na tomhle bodě se shodneme; otevřená zůstává otázka času.",
                "Oddělujete dosaženou shodu od nevyřešené části dohody.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Co kdybychom to na měsíc vyzkoušeli a potom společně vyhodnotili?",
                "Navrhujete vratné praktické řešení při přetrvávajících obavách.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Nechci rozhodovat za vás, jen pomoci najít přijatelnou možnost.",
                "Vymezujete svou roli při rozhovoru mezi dvěma lidmi.",
                "neutral",
                "b2-unit-7",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_summary_b2",
        "B2",
        "Shrnutí a potvrzení výsledku",
        "✅",
        [
            PhrasebookEntry(
                "Shrnu, na čem jsme se dohodli, a prosím opravte mě, pokud něco vynechám.",
                "Na konci jednání ověřujete společné porozumění výsledku.",
                "neutral",
                "b2-unit-8",
            ),
            PhrasebookEntry(
                "Souhlas se týká pouze zkušebního provozu, nikoli trvalé změny.",
                "Při závěrečném potvrzení chráníte přesný rozsah dosažené dohody.",
                "formal",
                "b2-unit-8",
            ),
            PhrasebookEntry(
                "Přestože některé výhrady trvají, na tomto kroku se můžeme shodnout.",
                "Přijímáte dílčí řešení bez předstírání úplného souhlasu.",
                "neutral",
                "b2-unit-8",
            ),
            PhrasebookEntry(
                "Zápis vám pošlu dnes a případné připomínky zapracujeme do pátku.",
                "Stanovujete konkrétní další postup po společné diskusi.",
                "neutral",
                "b2-unit-8",
            ),
        ],
    ),
]
