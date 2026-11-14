"""Czech B1 grammar: connected narration and independent interaction."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "cs-narrative-aspect-b1",
        "Vid při vyprávění",
        "B1",
        "Slovesný vid",
        "Rozlišujte probíhající pozadí a jednotlivé dokončené události.",
        "Nedokonavé sloveso často popisuje, co právě probíhalo: Četl jsem zprávu. "
        "Dokonavé sloveso představuje událost jako celek nebo posouvá příběh dál: "
        "Přečetl jsem zprávu a zavolal jsem kolegovi. Samotný minulý čas neříká, "
        "zda činnost dosáhla výsledku. Volba vidu závisí na tom, co chceme sdělit.",
        structure="Když jsem + nedokonavý minulý čas, + dokonavý minulý čas.",
        rules=[
            "Nedokonavý vid může vyjadřovat průběh, opakování i samotnou zkušenost.",
            "Dokonavý vid představuje ohraničenou událost; neznamená vždy krátké trvání.",
            "Otázka Četl jsi tu knihu? se může ptát na zkušenost, ne pouze na průběh.",
        ],
        examples=[
            GrammarExample("Když jsem vařila večeři, zazvonil telefon."),
            GrammarExample("Otevřel jsem okno, podíval jsem se ven a uviděl jsem souseda."),
            GrammarExample("Celý večer jsem psala dopis, ale nedopsala jsem ho."),
        ],
        related=["cs-duration-result-b1", "cs-temporal-clauses-b1"],
    ),
    GrammarTopic(
        "cs-duration-result-b1",
        "Dvě hodiny, nebo za dvě hodiny?",
        "B1",
        "Slovesný vid",
        "Vyjádřete dobu činnosti i dobu potřebnou k dosažení výsledku.",
        "Spojení bez předložky, například dvě hodiny, běžně udává trvání činnosti: "
        "Opravoval jsem kolo dvě hodiny. Spojení za dvě hodiny může s dokonavým "
        "slovesem označit dobu potřebnou k dokončení: Opravil jsem ho za dvě hodiny. "
        "V budoucím kontextu může za dvě hodiny také znamenat okamžik o dvě hodiny později.",
        rules=[
            "Opravoval jsem kolo dvě hodiny samo o sobě nepotvrzuje úspěšnou opravu.",
            "Opravil jsem kolo za dvě hodiny vyjadřuje dosažený výsledek.",
            "Přijdu za hodinu určuje budoucí příchod, nikoli délku chůze.",
        ],
        examples=[
            GrammarExample("Zprávu jsem psal celé dopoledne, ale ještě není hotová."),
            GrammarExample("Krátkou odpověď jsem napsal za pět minut."),
            GrammarExample("Za půl hodiny se vrátím a pak vám pomůžu."),
        ],
        related=["cs-narrative-aspect-b1"],
    ),
    GrammarTopic(
        "cs-temporal-clauses-b1",
        "Když, zatímco, než a až",
        "B1",
        "Časové věty",
        "Spojte souběžné děje a události, které následují po sobě.",
        "Když uvádí časovou situaci v minulosti i opakovaný děj. Zatímco zdůrazňuje "
        "souběh dvou dějů a může také vyjadřovat protiklad. Než označuje hranici, "
        "před kterou se něco děje. Až často uvádí očekávanou budoucí událost. "
        "Dokonavý tvar po až má budoucí význam: Až přijdu, zavolám.",
        rules=[
            "Časovou vedlejší větu oddělujeme čárkou.",
            "Budoucí význam dokonavého slovesa netvoříme pomocí budu.",
            "Než odejdu znamená před mým odchodem; až odejdu odkazuje na dobu po odchodu.",
        ],
        examples=[
            GrammarExample("Zatímco jsem hledal klíče, sestra objednávala taxi."),
            GrammarExample("Než odejdeš, zavři prosím okno."),
            GrammarExample("Až dokončím kurz, začnu hledat novou práci."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Až budu přijít, zavolám ti.",
                "Až přijdu, zavolám ti.",
                "Dokonavé přijdu už má budoucí význam.",
            ),
        ],
        related=["cs-narrative-aspect-b1"],
    ),
    GrammarTopic(
        "cs-motion-direction-b1",
        "Jít a chodit, jet a jezdit",
        "B1",
        "Slovesa pohybu",
        "Rozlišujte jednu cestu určitým směrem a opakovaný nebo neurčený pohyb.",
        "Jít a jet obvykle popisují pohyb jedním směrem v konkrétní situaci. "
        "Chodit a jezdit se používají při opakování, pohybu různými směry nebo "
        "popisu schopnosti či zvyku. Obě dvojice jsou v základním významu nedokonavé; "
        "rozdíl není totéž co rozdíl mezi dokonavým a nedokonavým videm.",
        rules=[
            "Jít a chodit běžně označují pohyb pěšky, jet a jezdit dopravním prostředkem.",
            "Pro běžný budoucí pohyb používáme půjdu a pojedu.",
            "Budoucí opakování lze vyjádřit budu chodit nebo budu jezdit.",
        ],
        examples=[
            GrammarExample("Každý den jezdím do práce tramvají, ale dnes jedu na kole."),
            GrammarExample("Když jsem šel domů, potkal jsem kolegyni."),
            GrammarExample("Od září budu chodit na večerní kurz."),
        ],
        related=["cs-motion-prefixes-b1"],
    ),
    GrammarTopic(
        "cs-motion-prefixes-b1",
        "Přijít, odejít a projít",
        "B1",
        "Slovesa pohybu",
        "Popište cíl, začátek a průběh cesty pomocí předpon.",
        "Předpona mění význam pohybového slovesa: přijít označuje dosažení místa, "
        "odejít opuštění místa a projít pohyb skrz prostor nebo kolem bodu na trase. "
        "Podobně rozlišujeme přijet, odjet a projet. Tato slovesa jsou dokonavá; "
        "pro průběh či opakování používáme například přicházet, odcházet, procházet "
        "nebo přijíždět, odjíždět, projíždět.",
        rules=[
            "Tvar přišel je minulý čas od přijít; přijdu vyjadřuje budoucnost.",
            "Předpony se učíme s konkrétním významem, ne pouze jako značku vidu.",
            "Pro pravidelné odjezdy je vhodné odjíždět: Vlak odjíždí v osm.",
        ],
        examples=[
            GrammarExample("Prošli jsme parkem a přišli jsme až k řece."),
            GrammarExample("Autobus odjel před pěti minutami."),
            GrammarExample("Tímto tunelem projíždíme každý týden."),
        ],
        related=["cs-motion-direction-b1", "cs-route-prepositions-b1"],
    ),
    GrammarTopic(
        "cs-route-prepositions-b1",
        "Přes náměstí, kolem školy a parkem",
        "B1",
        "Pády a pohyb",
        "Vyjádřete trasu, nejen výchozí bod a cíl.",
        "Přes se pojí se čtvrtým pádem a označuje cestu napříč nebo přes určité místo. "
        "Kolem má druhý pád a popisuje pohyb poblíž nebo okolo něčeho. Samotný sedmý "
        "pád může vyjadřovat prostor, kterým cesta vede: parkem, lesem, podchodem. "
        "Předložka k se třetím pádem směřuje k cíli, ale sama neznamená vstup dovnitř.",
        rules=[
            "Rozlišujte jít ke škole a jít do školy podle zamýšleného cíle.",
            "Přes most obsahuje čtvrtý pád; kolem mostu obsahuje druhý pád.",
            "Instrumentál trasy nepotřebuje předložku: Projděte podchodem.",
        ],
        examples=[
            GrammarExample("Jděte přes náměstí a potom kolem knihovny."),
            GrammarExample("Do centra jsme šli parkem."),
            GrammarExample("Dojděte k nádraží a počkejte před vchodem."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Jděte kolem školu.",
                "Jděte kolem školy.",
                "Po předložce kolem následuje druhý pád.",
            ),
        ],
        related=["cs-motion-prefixes-b1"],
    ),
    GrammarTopic(
        "cs-relative-clauses-b1",
        "Byt, který hledáme",
        "B1",
        "Vztažné věty",
        "Upřesněte osobu nebo věc pomocí zájmena který.",
        "Zájmeno který se shoduje v rodě a čísle se jménem, které rozvíjí. Jeho pád "
        "ale určuje funkce ve vedlejší větě: žena, kterou znám; žena, které pomáhám. "
        "Předložku potřebnou ve vedlejší větě zachováme: dům, ve kterém bydlím. "
        "Vztažnou větu oddělujeme čárkami.",
        rules=[
            "Pád nepřebíráme automaticky od podstatného jména v hlavní větě.",
            "Předložka stojí před zájmenem: soused, se kterým mluvím.",
            "Vložená vztažná věta má čárku na začátku i na konci.",
        ],
        examples=[
            GrammarExample("Byt, který si chceme pronajmout, má balkon."),
            GrammarExample("Sousedka, které jsem včera pomohl, bydlí ve třetím patře."),
            GrammarExample("To je dům, ve kterém jsme dříve bydleli."),
        ],
        common_mistakes=[
            GrammarMistake(
                "To je žena, který bydlí vedle nás.",
                "To je žena, která bydlí vedle nás.",
                "Žena je ženského rodu; zájmeno je zde podmětem vedlejší věty.",
            ),
        ],
    ),
    GrammarTopic(
        "cs-adjective-comparison-b1",
        "Levnější než a stejně velký jako",
        "B1",
        "Srovnávání",
        "Porovnávejte vlastnosti a vyjádřete velikost rozdílu.",
        "Druhý stupeň přídavného jména vyjadřuje rozdíl: levnější, větší, lepší. "
        "Po srovnání používáme než. Shodu vlastností vyjadřujeme stejně + přídavné "
        "jméno + jako. Rozdíl lze upřesnit spojením o něco, mnohem nebo údajem "
        "s předložkou o a čtvrtým pádem: o tisíc korun dražší.",
        rules=[
            "Třetí stupeň tvoříme pomocí nej-: nejlevnější, nejlepší.",
            "I druhý stupeň se skloňuje: v levnějším bytě, s lepší nabídkou.",
            "Při výběru z více možností určíme skupinu: nejmenší ze tří bytů.",
        ],
        examples=[
            GrammarExample("Tenhle byt je o dva tisíce korun levnější než náš současný byt."),
            GrammarExample("Kuchyň je stejně velká jako v předchozím bytě."),
            GrammarExample("Ze všech nabídek se nám nejvíc líbí byt s větším balkonem."),
        ],
        related=["cs-adverb-comparison-b1"],
    ),
    GrammarTopic(
        "cs-adverb-comparison-b1",
        "Lépe, rychleji a méně často",
        "B1",
        "Srovnávání",
        "Porovnávejte způsob, míru a četnost děje.",
        "Příslovce rozvíjí sloveso: dobře spím, rychle cestuji. Ve srovnání používáme "
        "lépe, rychleji, častěji nebo více a méně s dalším příslovcem. Přídavné jméno "
        "naopak popisuje vlastnost osoby či věci: lepší byt. Podoby lépe a líp jsou "
        "obě běžné; líp je hovorové.",
        rules=[
            "Rozlišujte lepší spojení a cestovat lépe.",
            "Méně často znamená nižší četnost, ne kratší trvání jednotlivého děje.",
            "Nejvyšší míru vyjadřujeme například nejlépe, nejrychleji nebo nejméně často.",
        ],
        examples=[
            GrammarExample("V novém bytě se nám spí lépe než ve starém."),
            GrammarExample("Do práce se teď dostanu rychleji."),
            GrammarExample("Sousedé už pořádají večírky méně často."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Po opravě topení se nám bydlí lepší.",
                "Po opravě topení se nám bydlí lépe.",
                "Způsob bydlení popisuje příslovce, nikoli přídavné jméno.",
            ),
        ],
        related=["cs-adjective-comparison-b1"],
    ),
    GrammarTopic(
        "cs-conditional-b1",
        "Udělal bych to jinak",
        "B1",
        "Podmiňovací způsob",
        "Vyjádřete návrh, zdvořilou žádost nebo představovanou možnost.",
        "Přítomný podmiňovací způsob tvoří příčestí na -l a tvary bych, bys, by, "
        "bychom, byste, by. Příčestí vyjadřuje rod a číslo: mohl bych, mohla bych, "
        "mohli bychom. Tvar bych stojí v neutrální větě mezi krátkými nepřízvučnými "
        "výrazy za prvním větným úsekem: Příští týden bych mohl přijít.",
        rules=[
            "Spisovný tvar první osoby množného čísla je bychom.",
            "Při vykání jedné osobě používáme byste, ale příčestí je v jednotném čísle.",
            "Podmiňovací způsob sám o sobě neoznačuje minulou událost.",
        ],
        examples=[
            GrammarExample("Ráda bych se přihlásila do večerního kurzu."),
            GrammarExample("Pane Nováku, mohl byste mi poslat pracovní smlouvu?"),
            GrammarExample("Navrhl bych kratší schůzku."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Já by chtěl jiný termín.",
                "Já bych chtěl jiný termín.",
                "K první osobě jednotného čísla patří bych.",
            ),
        ],
        related=["cs-kdyby-b1", "cs-purpose-aby-b1", "cs-clitic-clusters-b1"],
    ),
    GrammarTopic(
        "cs-kdyby-b1",
        "Kdybych měl více času",
        "B1",
        "Podmínkové věty",
        "Rozlišujte otevřenou podmínku a představovanou situaci.",
        "Pokud nebo jestli s oznamovacím způsobem často uvádí otevřenou podmínku: "
        "Pokud budu mít čas, přijdu. Kdyby uvádí představovanou podmínku; tvary "
        "kdybych, kdybys, kdyby, kdybychom, kdybyste, kdyby už obsahují osobu. "
        "V hlavní větě obvykle následuje podmiňovací způsob. Stejné tvary "
        "mohou s jasným časovým údajem označit i neuskutečněnou minulou možnost: "
        "Kdybych měl včera čas, přišel bych. Zda jde o minulost, přítomnost "
        "nebo budoucnost, proto určujeme z celého sdělení.",
        structure="Kdybych + příčestí na -l, + příčestí na -l + bych.",
        rules=[
            "Nezdvojujte osobní tvar: kdybych měl, nikoli kdybych bych měl.",
            "Rod vyjadřuje příčestí: Kdybych měla čas, přišla bych.",
            "Představovaná situace může být málo pravděpodobná, nemusí být zcela nemožná.",
        ],
        examples=[
            GrammarExample("Kdybych měl kratší pracovní dobu, chodil bych na kurz češtiny."),
            GrammarExample("Kdybychom bydleli blíž, nemuseli bychom tak brzy vstávat."),
            GrammarExample("Pokud zítra skončím včas, přijdu na schůzku."),
            GrammarExample(
                "Kdybych včera nezmeškal autobus, dorazil bych včas.",
                note="Mluvčí vysvětluje minulou situaci: autobus zmeškal a včas nedorazil.",
            ),
        ],
        related=["cs-conditional-b1"],
    ),
    GrammarTopic(
        "cs-purpose-aby-b1",
        "Učím se, abych se domluvil",
        "B1",
        "Účelové věty",
        "Vysvětlete, čeho chce někdo svou činností dosáhnout.",
        "Účelovou větu uvádíme tvary abych, abys, aby, abychom, abyste, aby "
        "a příčestím na -l. Tento tvar zde neznamená minulost: Učím se, abych "
        "rozuměl kolegům. Podmět účelové věty může být jiný než v hlavní větě. "
        "Účel je zamýšlený cíl, ne potvrzení, že se ho podařilo dosáhnout.",
        rules=[
            "Osoba se vyjadřuje ve tvaru abych nebo abyste, nepřidáváme další bych.",
            "Příčestí se shoduje s podmětem účelové věty.",
            "Rozlišujte důvod s protože a zamýšlený cíl s aby.",
        ],
        examples=[
            GrammarExample("Přihlásila jsem se na kurz, abych získala novou kvalifikaci."),
            GrammarExample("Pošlu vám mapu, abyste nás snadno našli."),
            GrammarExample("Mluvíme pomaleji, aby nám nový kolega rozuměl."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Učím se, abych budu rozumět.",
                "Učím se, abych rozuměl.",
                "Po abych používáme příčestí na -l; zde mluví muž.",
            ),
        ],
        related=["cs-conditional-b1", "cs-cause-result-b1"],
    ),
    GrammarTopic(
        "cs-dative-government-b1",
        "Komu pomáhám a čemu rozumím",
        "B1",
        "Slovesné vazby",
        "Používejte třetí pád po běžných slovesech bez předložky.",
        "Slovesa pomáhat, děkovat, věřit a rozumět se pojí se třetím pádem: "
        "pomáhám sousedovi, děkuji úřednici, věřím kolegům, rozumím otázce. "
        "Třetí pád může označovat osobu i věc. U mužských osobních jmen se "
        "objevují koncovky -ovi a -u; například panu Novákovi.",
        rules=[
            "Vazbu se učíme spolu se slovesem: rozumět někomu nebo něčemu.",
            "Bez důrazu užíváme mi, ti, mu, jí, nám, vám, jim. Při důrazu volíme "
            "mně, tobě, jemu; tvary jí, nám, vám a jim se nemění.",
            "Děkovat komu za co spojuje třetí pád s předložkou za a čtvrtým pádem.",
        ],
        examples=[
            GrammarExample("Nerozumím poslední otázce ve formuláři."),
            GrammarExample("Děkuji vám za rychlou odpověď."),
            GrammarExample("Pomohla jsem novému kolegovi s žádostí."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Rozumím ten pokyn.",
                "Rozumím tomu pokynu.",
                "Sloveso rozumět vyžaduje třetí pád.",
            ),
        ],
        related=["cs-prepositional-government-b1"],
    ),
    GrammarTopic(
        "cs-genitive-government-b1",
        "Ptát se, účastnit se a bát se",
        "B1",
        "Slovesné vazby",
        "Rozlišujte osobu, které se ptáte, a věc, na kterou se ptáte.",
        "Slovesa bát se a účastnit se vyžadují druhý pád: bojím se chyby, účastním "
        "se schůzky. U ptát se stojí dotazovaná osoba ve druhém pádě; téma otázky "
        "běžně vyjadřuje na se čtvrtým pádem: Ptám se úřednice na termín. "
        "Zvratné se je součástí "
        "těchto slovesných spojení a nelze ho libovolně vypustit.\n\n"
        "Ve druhém pádě množného čísla rozlišujeme například kolegů, schůzek, "
        "otázek, možností a měst. Přídavná jména mají -ých nebo -ích: "
        "nových kolegů, pracovních schůzek. Stejný pád použijeme také "
        "po bez nebo od: bez potřebných dokladů, od nových kolegů.",
        rules=[
            "Ptát se koho není stejná vazba jako odpovídat komu.",
            "Zápor běžně nemění předmět na druhý pád: Nemám doklad.",
            "Zájmena ve druhém pádě mají například tvary tě, ho, jí, nás, vás, jich.",
        ],
        examples=[
            GrammarExample("Zeptám se kolegyně na číslo kanceláře."),
            GrammarExample("Zítra se účastníme informační schůzky."),
            GrammarExample("Nebojte se drobných chyb."),
            GrammarExample(
                "Účastním se pravidelných schůzek a ptám se kolegů na jejich zkušenosti."
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                "Účastním se schůzku.",
                "Účastním se schůzky.",
                "Po účastnit se potřebujeme druhý pád.",
            ),
        ],
        related=["cs-prepositional-government-b1"],
    ),
    GrammarTopic(
        "cs-prepositional-government-b1",
        "Žádat o něco a obrátit se na někoho",
        "B1",
        "Slovesné vazby",
        "Spojujte sloveso se správnou předložkou a pádem.",
        "Předložkové vazby se učíme jako celek: žádat o něco, čekat na někoho, "
        "obrátit se na někoho, zajímat se o něco, mluvit o něčem a souhlasit s někým. "
        "Stejná předložka nemusí mít ve všech vazbách stejný pád: zajímat se "
        "o nový kurz má čtvrtý pád, mluvit o novém kurzu má šestý pád.",
        rules=[
            "Žádat o a obrátit se na vyžadují čtvrtý pád.",
            "Mluvit o vyžaduje šestý pád; souhlasit s vyžaduje sedmý pád.",
            "Po předložce se u osobních zájmen užívají tvary jako na něj, o ní, s nimi.",
        ],
        examples=[
            GrammarExample("Chtěla bych požádat o nový průkaz."),
            GrammarExample("S tímto problémem se obraťte na vedoucího."),
            GrammarExample("Mluvili jsme o změně termínu, ale nesouhlasím s navrženým datem."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Souhlasím s váš návrh.",
                "Souhlasím s vaším návrhem.",
                "Předložka s ve vazbě souhlasit s vyžaduje sedmý pád.",
            ),
        ],
        related=["cs-dative-government-b1", "cs-genitive-government-b1"],
    ),
    GrammarTopic(
        "cs-reported-speech-b1",
        "Předávání zpráv",
        "B1",
        "Nepřímá řeč",
        "Předejte cizí sdělení se správnými osobami a časovými údaji.",
        "Oznamovací sdělení často předáváme větou se že: Eva říká, že přijde později. "
        "V češtině se po minulém čase automaticky neposouvá slovesný čas. Měníme "
        "ale zájmena a výrazy jako dnes, zítra nebo tady, pokud by z nového pohledu "
        "znamenaly jiný den či místo. Důležitý je původní význam zprávy.",
        rules=[
            "Uveďte, kdo zprávu řekl, zvlášť když se účastní více osob.",
            "Věta Řekl, že přijde může vyjadřovat budoucnost vzhledem k jeho sdělení.",
            "Časový údaj změňte jen tehdy, když se změnil časový pohled.",
        ],
        examples=[
            GrammarExample("Eva mi ráno řekla, že dnes zůstane doma."),
            GrammarExample(
                "V pondělí Petr řekl, že přijde následující den.",
                note="Původně v pondělí řekl: Přijdu zítra.",
            ),
            GrammarExample("Kolegyně říká, že nám pošle podklady."),
        ],
        related=["cs-indirect-questions-b1"],
    ),
    GrammarTopic(
        "cs-indirect-questions-b1",
        "Nevíte, jestli je volno?",
        "B1",
        "Nepřímé otázky",
        "Zeptejte se zdvořile nebo předejte otázku jiné osoby.",
        "U otázky s odpovědí ano nebo ne používáme v nepřímé větě jestli nebo zda: "
        "Nevíte, jestli je kancelář otevřená? U doplňovací otázky zachováme tázací "
        "slovo: Ptá se, kdy začínáme. Zda je běžné zejména v písemné a formálnější "
        "komunikaci. Pořadí slov se řídí českým slovosledem, nikoli zvláštní inverzí.",
        rules=[
            "Nepřímou otázku oddělujeme čárkou.",
            "Za celým souvětím píšeme otazník, pokud samo funguje jako otázka.",
            "Výpověď Nevím, kdy přijde. není přímá otázka a končí tečkou.",
        ],
        examples=[
            GrammarExample("Můžete mi říct, kde se máme sejít?"),
            GrammarExample("Chtěla bych vědět, zda je v ceně také oběd."),
            GrammarExample("Kolega se ptá, jestli může přijít o hodinu později."),
        ],
        related=["cs-reported-speech-b1", "cs-conditional-b1"],
    ),
    GrammarTopic(
        "cs-clitic-clusters-b1",
        "Už jsem mu to poslal",
        "B1",
        "Slovosled",
        "Řaďte krátká zájmena a pomocná slova v běžných sděleních.",
        "Krátká nepřízvučná slova obvykle stojí za prvním větným úsekem, ne nutně "
        "za prvním napsaným slovem. V běžných skupinách stojí pomocné slovo před "
        "se nebo si, potom následuje krátký třetí pád a čtvrtý pád: Včera jsem mu ho "
        "poslal. Podobně říkáme Rád bych si to přečetl. Dlouhé důrazové tvary "
        "zájmen mohou stát jinde.",
        rules=[
            "První úsek může mít více slov: Minulý týden jsem mu to vysvětlil.",
            "Krátké mi stojí před ho: Dej mi ho, prosím.",
            "Ve druhé osobě jednotného čísla minulého času používáme ses a sis: "
            "Kdy ses vrátil? Co sis objednal?",
        ],
        examples=[
            GrammarExample("Po dnešní schůzce jsem mu to ještě jednou vysvětlila."),
            GrammarExample("Rád bych si to nejdřív promyslel."),
            GrammarExample("Kdy ses o té změně dozvěděl?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Dej ho mi, prosím.",
                "Dej mi ho, prosím.",
                "V této neutrální skupině krátký třetí pád předchází čtvrtému pádu.",
            ),
        ],
        related=["cs-conditional-b1", "cs-dative-government-b1"],
    ),
    GrammarTopic(
        "cs-cause-result-b1",
        "Protože, proto a kvůli",
        "B1",
        "Příčina a důsledek",
        "Vysvětlete důvod rozhodnutí a jeho následek.",
        "Protože uvádí větu s příčinou: Zůstali jsme doma, protože pršelo. Proto "
        "spojuje příčinu s následkem: Pršelo, proto jsme zůstali doma. Kvůli se "
        "pojí se třetím pádem a v tomto použití uvádí příčinu pomocí jména: kvůli "
        "dešti. Díky se třetím pádem běžně ukazuje příznivou příčinu.",
        rules=[
            "Po protože následuje věta, po kvůli podstatné jméno nebo zájmeno.",
            "Při převodu zachovejte směr vztahu mezi příčinou a následkem.",
            "Díky se může objevit i ironicky; v neutrálním vysvětlení zdůrazňuje přínos.",
        ],
        examples=[
            GrammarExample("Kvůli poruše jsme museli změnit trasu."),
            GrammarExample("Oprava by byla příliš drahá, proto jsme koupili nový spotřebič."),
            GrammarExample("Díky pomoci sousedů jsme všechno zvládli včas."),
        ],
        related=["cs-purpose-aby-b1", "cs-concession-b1"],
    ),
    GrammarTopic(
        "cs-concession-b1",
        "I když a přesto",
        "B1",
        "Přípustka",
        "Vyjádřete výsledek, který neodpovídá běžnému očekávání.",
        "I když a ačkoli uvádějí okolnost, která by mohla bránit výsledku, ale "
        "v dané situaci mu nebrání: I když pršelo, šli jsme ven. Ačkoli je běžnější "
        "v psaném projevu. Přesto vyjadřuje podobný vztah v navazující větě: "
        "Pršelo, přesto jsme šli ven. Při přeformulování zachováme obě skutečnosti.",
        rules=[
            "I když není totéž co kdyby: v uvedených větách mluvíme o skutečné okolnosti.",
            "Po i když následuje věta se slovesem.",
            "Přesto nevyjadřuje příčinu; upozorňuje na překvapivý protiklad.",
        ],
        examples=[
            GrammarExample("I když je ten výrobek dražší, vydrží podle recenzí déle."),
            GrammarExample("Návrh má několik výhod, přesto s ním zatím nesouhlasím."),
            GrammarExample("Ačkoli jsme měli málo času, stihli jsme všechno připravit."),
        ],
        related=["cs-cause-result-b1"],
    ),
    GrammarTopic(
        "cs-negative-concord-b1",
        "Nikdo mi nic neřekl",
        "B1",
        "Zápor",
        "Spojujte záporná zájmena a příslovce se záporným slovesem.",
        "Nikdo, nic, nikde, nikdy a žádný se v běžné záporné větě spojují se "
        "záporným slovesem: Nikdo nepřišel. Více záporných výrazů zde neruší "
        "zápor: Nikdo mi nic neřekl. Zájmena se skloňují podle větné funkce "
        "a předložky: nikoho, nikomu, s nikým, o ničem.",
        rules=[
            "Nikdo vyjadřuje nepřítomnost osoby; nic nepřítomnost věci nebo obsahu.",
            "Ne všichni přišli neznamená Nikdo nepřišel; část lidí mohla přijít.",
            "Po předložce zachovejte potřebný pád: s nikým, bez ničeho.",
        ],
        examples=[
            GrammarExample("Nikomu jsem nic nesliboval."),
            GrammarExample("O změně ceny jsme nikde nenašli žádnou informaci."),
            GrammarExample("S nikým jsem se na jiném řešení nedomluvila."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Nikdo mi pomohl.",
                "Nikdo mi nepomohl.",
                "Záporné nikdo vyžaduje v této větě také záporné sloveso.",
            ),
        ],
        related=["cs-dative-government-b1", "cs-prepositional-government-b1"],
    ),
]
