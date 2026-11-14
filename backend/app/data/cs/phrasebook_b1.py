"""Czech B1 phrases for independent interaction and communication repair."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "cs_experiences_b1",
        "B1",
        "Vyprávění o zážitku",
        "💬",
        [
            PhrasebookEntry(
                "Zpočátku všechno probíhalo podle plánu, ale pak se změnilo počasí.",
                "Uveďte nečekaný obrat při vyprávění o výletu.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Když jsme hledali cestu, všimli jsme si turistické značky.",
                "Propojte probíhající činnost s událostí, která pomohla situaci vyřešit.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Opravoval jsem to celé odpoledne, ale ještě to není hotové.",
                "Vysvětlete, že dlouhá práce zatím nepřinesla konečný výsledek.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Něco podobného se mi už jednou přihodilo.",
                "Navažte na vyprávění druhého člověka vlastní zkušeností.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Nakonec jsme to zvládli a dnes už se tomu smějeme.",
                "Uzavřete příběh o obtížné situaci s dobrým koncem.",
                "informal",
                "b1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_travel_b1",
        "B1",
        "Změny během cesty",
        "🚆",
        [
            PhrasebookEntry(
                "Stihnu přípoj, když má náš vlak dvacet minut zpoždění?",
                "Ověřte u průvodčího, zda bude možné pokračovat plánovaným spojem.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Odkud odjíždí náhradní autobus do další stanice?",
                "Zjistěte místo odjezdu při výluce na železnici.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Projděte podchodem a pak pokračujte kolem pošty.",
                "Popište pěší trasu od nádraží.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Tudy jezdím pravidelně, ale dnes musím jet jinou cestou.",
                "Vysvětlete rozdíl mezi obvyklou trasou a dnešní změnou.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Platí tahle jízdenka i v náhradním autobusu?",
                "Ověřte platnost zakoupené jízdenky při změně dopravního prostředku.",
                "neutral",
                "b1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_housing_b1",
        "B1",
        "Bydlení a ohleduplnost",
        "🏠",
        [
            PhrasebookEntry(
                "Je v nájmu zahrnutá i záloha na vodu a teplo?",
                "Upřesněte celkové měsíční náklady při prohlídce bytu.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Hledáme byt, ve kterém chceme bydlet alespoň dva roky.",
                "Sdělte pronajímateli požadovanou délku bydlení.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Ten druhý pokoj je menší, ale dostanu se odtud rychleji do práce.",
                "Porovnejte nabídky bydlení podle prostoru i dopravy.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Po desáté je u nás hudba stále dost slyšet. Můžete ji prosím ztišit?",
                "Požádejte sousedy o klid bez osobního obviňování.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Na úklidu společné chodby se můžeme střídat.",
                "Navrhněte spravedlivé rozdělení péče o dům.",
                "neutral",
                "b1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_work_study_b1",
        "B1",
        "Práce a vzdělávání",
        "📚",
        [
            PhrasebookEntry(
                "Ráda bych se zeptala na možnost kratšího úvazku.",
                "Otevřete při pracovním rozhovoru téma rozsahu pracovní doby.",
                "formal",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Kdyby byl kurz večer, mohl bych se ho pravidelně účastnit.",
                "Vysvětlete, jaká změna rozvrhu by vám umožnila chodit na kurz.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Přihlásila jsem se, abych získala více praktických zkušeností.",
                "Popište svůj cíl při nástupu do vzdělávacího programu.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Mohl byste mi prosím popsat průběh pohovoru?",
                "Požádejte pracovníka náboru o informace před setkáním.",
                "formal",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Ve středu tě můžu zastoupit, pokud za mě vezmeš páteční směnu.",
                "Navrhněte kolegovi vzájemnou výměnu směn.",
                "informal",
                "b1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_services_b1",
        "B1",
        "Vyřizování žádosti",
        "📋",
        [
            PhrasebookEntry(
                "Potřebuji požádat o nový průkaz, protože můj současný brzy přestane platit.",
                "Vysvětlete na úřadě důvod své návštěvy.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Nerozumím této části formuláře. Co přesně mám uvést?",
                "Požádejte o vysvětlení nejasného pole v dokumentu.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Na koho se mám obrátit, pokud mi chybí jeden z dokladů?",
                "Zjistěte, kdo vám může poradit s neúplnou žádostí.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Do kdy musím dodat zbývající přílohy?",
                "Ověřte poslední možný termín pro doplnění podání.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Děkuji vám za vysvětlení. Mohu dostat potvrzení o podání žádosti?",
                "Uzavřete jednání a požádejte o doklad, že úřad žádost převzal.",
                "formal",
                "b1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_cooperation_b1",
        "B1",
        "Předávání informací a společné úkoly",
        "🤝",
        [
            PhrasebookEntry(
                "Petra vzkazuje, že přijde později a přinese potřebné podklady.",
                "Předejte skupině zprávu od nepřítomné účastnice.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Můžete mi říct, kdo má na starosti přípravu sálu?",
                "Zjistěte, na koho se obrátit při organizaci akce.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Už jsem mu to poslal, ale zatím mi neodpověděl.",
                "Informujte kolegu o předání zprávy a chybějící reakci.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Jestli tomu správně rozumím, každý připraví jednu část programu.",
                "Ověřte své porozumění rozdělení společné práce.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Ty připravíš pozvánku a já ji pak rozešlu ostatním. Platí?",
                "Potvrďte s kolegou konkrétní rozdělení dvou navazujících úkolů.",
                "informal",
                "b1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_choices_b1",
        "B1",
        "Nákup a řešení závad",
        "🛍️",
        [
            PhrasebookEntry(
                "I když je tenhle model dražší, má výrazně nižší spotřebu.",
                "Uveďte důvod, proč zvažujete výrobek s vyšší pořizovací cenou.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Přístroj se sám vypíná, proto bych ho chtěl reklamovat.",
                "Popište prodejci závadu a požadovaný další postup.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "O tomto poplatku mě při nákupu nikdo neinformoval.",
                "Upozorněte na náklad, o kterém jste předem nevěděli.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Rozumím vaší nabídce, přesto bych raději požádala o opravu.",
                "Zdvořile odmítněte jinou možnost řešení a vyjádřete svou preferenci.",
                "formal",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Můžete mi prosím písemně potvrdit, kdy bude reklamace vyřízená?",
                "Požádejte o jasný časový údaj při řešení vady.",
                "formal",
                "b1-unit-7",
            ),
        ],
    ),
    PhrasebookCategory(
        "cs_resolution_b1",
        "B1",
        "Hledání společného řešení",
        "🧩",
        [
            PhrasebookEntry(
                "Nejdřív vám popíšu, co se stalo, a pak navrhnu řešení.",
                "Uspořádejte delší vysvětlení praktického problému.",
                "neutral",
                "b1-unit-8",
            ),
            PhrasebookEntry(
                "Zřejmě došlo k nedorozumění. Měl jsem na mysli příští pátek.",
                "Opravte chybně pochopený termín bez obviňování druhé osoby.",
                "neutral",
                "b1-unit-8",
            ),
            PhrasebookEntry(
                "Kdyby vám tento termín nevyhovoval, mohli bychom se sejít v pondělí.",
                "Nabídněte konkrétní náhradní termín.",
                "neutral",
                "b1-unit-8",
            ),
            PhrasebookEntry(
                "Chápu, že je to složité, přesto potřebujeme najít řešení pro všechny.",
                "Uznejte obtížnost situace a vraťte jednání ke společnému cíli.",
                "neutral",
                "b1-unit-8",
            ),
            PhrasebookEntry(
                "Můžeme si na závěr potvrdit, na čem jsme se dohodli?",
                "Uzavřete jednání ověřením konkrétní dohody.",
                "neutral",
                "b1-unit-8",
            ),
        ],
    ),
]
