"""Czech A2 phrases for practical situations in Czechia."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "cs_travel_a2",
        "A2",
        "Na cestě a při přestupu",
        "🚆",
        [
            PhrasebookEntry(
                "Ze kterého nástupiště jede vlak do Brna?",
                "Na nádraží zjišťujete místo odjezdu.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Musím cestou přestupovat?",
                "Před nákupem jízdenky ověřujete, zda je spoj přímý.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Platí tato jízdenka také v tramvaji?",
                "Ověřujete možnost použít stejný doklad v jiné dopravě.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Kolik minut má vlak zpoždění?",
                "Potřebujete odhadnout další čekání na vlak.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Jede tento autobus na hlavní nádraží?",
                "Před nástupem kontrolujete směr autobusu.",
                "neutral",
                "a2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_housing_a2",
        "A2",
        "V bytě a se sousedy",
        "🏠",
        [
            PhrasebookEntry(
                "Je v nájmu také voda a topení?",
                "Při hledání bytu zjišťujete, co zahrnuje pravidelná platba.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "V koupelně neteče teplá voda.",
                "Oznamujete majiteli konkrétní problém v bytě.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Komu mám zavolat kvůli opravě?",
                "Hledáte člověka, který řeší závadu v domě.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Mám pro vás náhradní klíč.",
                "Předáváte klíč sousedovi, se kterým si vykáte.",
                "formal",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Můžeš mi pomoct s tou skříní?",
                "Žádáte známého o pomoc při přesouvání nábytku.",
                "informal",
                "a2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_experiences_a2",
        "A2",
        "Vyprávění o víkendu",
        "🎭",
        [
            PhrasebookEntry(
                "O víkendu jsme byli na výletě.",
                "Začínáte krátké vyprávění o společném volnu.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Jak dlouho trvala cesta?",
                "Ptáte se na délku již skončeného cestování.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Nejdřív jsme navštívili hrad a potom jsme šli na oběd.",
                "Popisujete dvě události ve správném pořadí.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Na koncertě byla výborná hudba.",
                "Doplňujete vyprávění o atmosféru na koncertě.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Nakonec jsme jeli domů posledním vlakem.",
                "Uzavíráte příběh informací o cestě domů.",
                "neutral",
                "a2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_plans_a2",
        "A2",
        "Rezervace a budoucí plány",
        "🗓️",
        [
            PhrasebookEntry(
                "Máte volný dvoulůžkový pokoj na dvě noci?",
                "Ověřujete dostupnost ubytování pro dvě osoby.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Přijedeme v pátek kolem šesté večer.",
                "Informujete recepci o plánovaném příjezdu.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Je snídaně v ceně pokoje?",
                "Před rezervací zjišťujete rozsah služby.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Zítra budu pracovat, ale v sobotu mám volno.",
                "Vysvětlujete, kdy máte čas na společnou aktivitu.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Napíšu ti večer a domluvíme přesný čas.",
                "Slibujete známému zprávu s upřesněním setkání.",
                "informal",
                "a2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_health_a2",
        "A2",
        "U lékaře a v lékárně",
        "🩺",
        [
            PhrasebookEntry(
                "Chci se objednat na vyšetření.",
                "Telefonujete do ordinace a žádáte termín.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Od včerejška mě bolí v krku.",
                "Popisujete zdravotníkovi potíže a jejich začátek.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Mám alergii na penicilin.",
                "Informujete zdravotníka o své známé alergii.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Jak často mám tento lék užívat?",
                "Ověřujete pokyny k předepsanému léku.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Prosím, napište mi ty pokyny.",
                "Žádáte písemné informace, abyste je měli později k dispozici.",
                "formal",
                "a2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_shopping_a2",
        "A2",
        "V obchodě a při reklamaci",
        "🛍️",
        [
            PhrasebookEntry(
                "Prosím pět rohlíků a půl kila jablek.",
                "Objednáváte pečivo a ovoce s konkrétním množstvím.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Máte tuto košili v menší velikosti?",
                "Zjišťujete dostupnost vhodnějšího oblečení.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Mohla bych si ty boty vyzkoušet?",
                "Zákaznice zdvořile žádá o možnost vyzkoušení.",
                "formal",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Chtěl bych reklamovat toto nefunkční zboží.",
                "Zákazník oznamuje vadu a žádá její řešení.",
                "formal",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Mohl byste mi vrátit peníze na kartu?",
                "Při vracení zboží žádáte o vrácení peněz na kartu; oslovujete muže.",
                "formal",
                "a2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_services_a2",
        "A2",
        "Na úřadě, na poště a v práci",
        "📮",
        [
            PhrasebookEntry(
                "Který formulář mám vyplnit?",
                "Na úřadě vybíráte správný dokument pro svou žádost.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Musím přijít osobně, nebo můžu žádost poslat?",
                "Ověřujete povinnost osobní návštěvy.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Jdu si vyzvednout balík.",
                "Na poště sdělujete důvod své návštěvy.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "V příloze posílám vyplněný formulář.",
                "V e-mailu upozorňujete příjemce na přiložený dokument.",
                "formal",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Můžeme schůzku přesunout na zítřek?",
                "Navrhujete jiný termín pracovního setkání.",
                "neutral",
                "a2-unit-7",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_review_a2",
        "A2",
        "Domluva a řešení běžných problémů",
        "💬",
        [
            PhrasebookEntry(
                "Promiňte, rozumím správně, že mám přijít až zítra?",
                "Ověřujete důležitý údaj v rozhovoru.",
                "formal",
                "a2-unit-8",
            ),
            PhrasebookEntry(
                "Vlak měl zpoždění, proto přijdu o půl hodiny později.",
                "Vysvětlujete příčinu pozdního příchodu a uvádíte odhad.",
                "neutral",
                "a2-unit-8",
            ),
            PhrasebookEntry(
                "Jestli budete mít volný termín v pátek, ráda přijdu.",
                "Žena nabízí konkrétní možnost náhradního termínu.",
                "formal",
                "a2-unit-8",
            ),
            PhrasebookEntry(
                "Tento pokoj je menší, ale je levnější a blíž nádraží.",
                "Porovnáváte ubytování a vysvětlujete jeho výhody.",
                "neutral",
                "a2-unit-8",
            ),
            PhrasebookEntry(
                "Včera jsem se necítil dobře, dnes už můžu pracovat.",
                "Muž vysvětluje změnu zdravotního stavu a svou dostupnost.",
                "neutral",
                "a2-unit-8",
            ),
        ],
    ),
]
