"""Czech A2 grammar: productive cases, narration and practical interaction."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "cs-genitive-a2",
        "Druhý pád: odkud, od koho a bez čeho",
        "A2",
        "Pády a předložky",
        "Vyjádříme původ, výchozí místo a nepřítomnost věci.",
        "Po předložkách z, do, od, u a bez používáme druhý pád. U ženských jmen na -a "
        "bývá koncovka -y: škola – ze školy. U jmen na -e se tvar často nemění: "
        "ulice – z ulice. Střední jména na -o mají často -a: město – z města. Mužská jména "
        "mají různé koncovky: hotel – z hotelu, obchod – z obchodu, park – z parku, "
        "bratr – od bratra. Učíme se vždy celé spojení, ne jednu koncovku pro všechna jména.\n\n"
        "Přídavné jméno mění tvar také: z nového hotelu, do nové školy. Tvary ze "
        "a ode mají stejný význam jako z a od; usnadňují výslovnost, například ze školy.",
        structure="z / do / od / u / bez + 2. pád",
        rules=[
            "Otázka odkud vede například k odpovědi z Prahy nebo z nádraží.",
            "Po do říkáme cíl cesty: do Brna, do hotelu.",
            "Po bez označujeme chybějící věc: bez jízdenky, bez telefonu.",
        ],
        examples=[
            GrammarExample("Autobus jede z Brna do Prahy."),
            GrammarExample("Jdu do nového obchodu."),
            GrammarExample("Jsem u sestry a piju čaj bez cukru."),
        ],
        common_mistakes=[
            GrammarMistake("Jedu z Praha.", "Jedu z Prahy.", "Po z potřebujeme druhý pád: Prahy.")
        ],
        related=["cs-direction-a2", "cs-quantities-a2"],
    ),
    GrammarTopic(
        "cs-locative-a2",
        "Šestý pád: na nádraží a o cestě",
        "A2",
        "Pády a předložky",
        "Rozšíříme popis místa a řekneme, o čem mluvíme.",
        "Šestý pád používáme vždy s předložkou. V a na často označují místo, o téma "
        "rozhovoru a po například pohyb po určitém prostoru. Běžné tvary jsou ve "
        "městě, v hotelu, na nádraží, o cestě, po ulici. Koncovky nejsou u všech "
        "slov stejné: Praha – v Praze, škola – ve škole, park – v parku, tramvaj – "
        "v tramvaji. U některých slov se mění i souhláska.\n\n"
        "Tvary přídavných jmen jsou například v novém hotelu a v nové škole. "
        "Předložku se učíme se slovem: v obchodě, ale na poště. Nevybíráme ji "
        "jen podle toho, zda je místo uvnitř budovy.",
        structure="v / na / o / po + 6. pád",
        rules=[
            "Kde? V Praze. O čem? O Praze.",
            "V a ve jsou podoby stejné předložky: v parku, ve škole.",
            "Na tomto místě procvičujeme hlavně jednotné číslo a běžná místní jména.",
        ],
        examples=[
            GrammarExample("Čekám na hlavním nádraží."),
            GrammarExample("Mluvíme o nové cestě."),
            GrammarExample("Turisté chodí po městě."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Bydlím v nový hotel.",
                "Bydlím v novém hotelu.",
                "Místo po v vyžaduje šestý pád u jména i přídavného jména.",
            )
        ],
        related=["cs-direction-a2"],
    ),
    GrammarTopic(
        "cs-direction-a2",
        "Kde, kam a odkud",
        "A2",
        "Pády a předložky",
        "Rozlišíme místo, cíl a výchozí bod cesty.",
        "Na otázku kde odpovídáme například v práci nebo na poště. Na otázku kam "
        "říkáme do práce nebo na poštu. Do má druhý pád; na při vyjádření cíle "
        "čtvrtý pád. Na otázku odkud říkáme z práce nebo z pošty. Cílové spojení "
        "nepoužívá automaticky stejnou předložku jako popis místa.\n\n"
        "Učíme se trojice: v obchodě – do obchodu – z obchodu; na nádraží – na "
        "nádraží – z nádraží. U nádraží vypadá čtvrtý a šestý pád stejně, proto "
        "význam poznáme ze slovesa a situace. Doma označuje místo, domů cíl.",
        rules=[
            "Místo: jsem ve škole. Cíl: jdu do školy.",
            "Na poště je šestý pád; na poštu je čtvrtý pád.",
            "Směr domů vyjadřujeme bez předložky.",
        ],
        examples=[
            GrammarExample("Teď jsem na poště a potom jdu do knihovny."),
            GrammarExample("Ráno jedu do práce, večer jedu z práce domů."),
        ],
        common_mistakes=[
            GrammarMistake("Jdu do doma.", "Jdu domů.", "Domů už samo vyjadřuje cíl cesty.")
        ],
        related=["cs-genitive-a2", "cs-locative-a2", "cs-motion-a2"],
    ),
    GrammarTopic(
        "cs-dative-a2",
        "Třetí pád: komu a ke komu",
        "A2",
        "Pády a předložky",
        "Pojmenujeme příjemce, člověka, kterému pomáháme, a cíl po k.",
        "Třetí pád odpovídá na otázky komu a čemu. Používáme ho například po "
        "slovesech dát, pomáhat a telefonovat a po předložce k. Běžná spojení "
        "jsou pomáhám sestře, telefonuji mamince, jdu k lékaři. U mužských osob "
        "se setkáme s koncovkami -ovi a -i: sousedovi, příteli, lékaři i lékařovi. "
        "Obě poslední podoby jsou správné.\n\n"
        "U ženských jmen může změnu koncovky doprovázet změna souhlásky: "
        "maminka – mamince, kolegyně – kolegyni. Přídavné jméno má například "
        "tvar novému nebo nové: k novému sousedovi, k nové sousedce.",
        structure="pomáhat / telefonovat / dát něco + 3. pád; k + 3. pád",
        rules=[
            "Po k a ke je třetí pád: k domu, ke škole.",
            "Příjemce a věc mají různé pády: dávám sestře klíč.",
            "U osob se učíme běžné tvary jako celé dvojice: lékař – k lékaři.",
        ],
        examples=[
            GrammarExample("Pomáhám nové sousedce."),
            GrammarExample("Dávám bratrovi klíč od bytu."),
            GrammarExample("Cesta vede ke škole."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Pomáhám sestru.",
                "Pomáhám sestře.",
                "Pomáhat se pojí se třetím pádem, ne se čtvrtým.",
            )
        ],
        related=["cs-personal-pronouns-a2", "cs-direction-a2"],
    ),
    GrammarTopic(
        "cs-instrumental-a2",
        "Sedmý pád: s kým a čím",
        "A2",
        "Pády a předložky",
        "Vyjádříme společnost, dopravní prostředek a nástroj.",
        "S a se se pojí se sedmým pádem: s bratrem, se sestrou, s kolegyní. "
        "Bez předložky používáme sedmý pád například pro dopravní prostředek "
        "nebo nástroj: jedu vlakem, píšu tužkou. Neříkáme s vlakem, když pouze "
        "cestujeme vlakem.\n\n"
        "Běžné koncovky v jednotném čísle jsou -em u mnoha mužských a středních "
        "jmen, -ou u ženských jmen na -a a -í například u kolegyně: domem, "
        "městem, tramvají, kolegyní. Přídavná jména mají tvary s novým "
        "sousedem a s novou sousedkou. V místních spojeních se setkáme také "
        "s před domem a za školou.",
        rules=[
            "S někým označuje společnost: bydlím s bratrem.",
            "Dopravní prostředek vyjádříme bez s: autobusem, metrem, autem.",
            "U pěší cesty používáme pěšky, ne název dopravního prostředku.",
        ],
        examples=[
            GrammarExample("Jedu tramvají s novou kolegyní."),
            GrammarExample("Píšu adresu tužkou."),
            GrammarExample("Před domem je zahrada."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Bydlím s sestra.",
                "Bydlím se sestrou.",
                "Po s potřebujeme sedmý pád; zde je běžná podoba se.",
            )
        ],
        related=["cs-dative-a2", "cs-personal-pronouns-a2"],
    ),
    GrammarTopic(
        "cs-personal-pronouns-a2",
        "Osobní zájmena po slovesech a předložkách",
        "A2",
        "Zájmena",
        "Místo opakování jména použijeme mi, ti, ho, ji nebo delší tvar.",
        "Krátké tvary zájmen používáme bez předložky a bez důrazu: pomáhá mi, "
        "dám ti klíč, vidím ho, znám ji. Často stojí za prvním větným celkem: "
        "Dnes ti pomáhám. Delší tvary používáme po předložkách nebo při "
        "zdůraznění: pro mě, ke mně, k tobě, se mnou, s tebou.\n\n"
        "U třetí osoby začíná tvar po předložce často na n: bez něho, k němu, "
        "s ním; bez ní, k ní, s ní. Učíme se tvary podle pádu, ne jen podle "
        "rodu. Ve větě Dávám jí klíč je jí třetí pád; ve větě Vidím ji je ji "
        "čtvrtý pád a má krátké i.",
        rules=[
            "Krátké mi a ti nestojí hned po předložce.",
            "Třetí pád: mi, ti, mu, jí, nám, vám, jim.",
            "Čtvrtý pád v běžných spojeních: vidí mě, tě, ho, ji, nás, vás, je.",
        ],
        examples=[
            GrammarExample("To je Eva. Znám ji a často jí telefonuji."),
            GrammarExample("Petr bydlí blízko. Dnes jdu k němu."),
            GrammarExample("Eva bydlí se mnou."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Jdu k mi.",
                "Jdu ke mně.",
                "Po předložce potřebujeme delší tvar zájmena: ke mně.",
            )
        ],
        related=["cs-dative-a2", "cs-instrumental-a2"],
    ),
    GrammarTopic(
        "cs-past-forms-a2",
        "Minulý čas: pracoval jsem a byla jsi",
        "A2",
        "Slovesa a čas",
        "Řekneme, co se dělo před dneškem.",
        "Minulý čas tvoříme pomocí tvaru na -l a u první a druhé osoby také "
        "pomocí jsem, jsi, jsme, jste: pracoval jsem, pracovala jsi, pracovali jsme. "
        "Ve třetí osobě pomocné být nepřidáváme: Petr pracoval, Eva pracovala. "
        "Tvar na -l se mění podle rodu a čísla, podrobněji ho procvičíme v "
        "následujícím tématu.\n\n"
        "Pomocné sloveso obvykle stojí za prvním větným celkem: Včera jsem "
        "pracoval doma. Zápor přidáváme k tvaru na -l: nepracoval jsem. "
        "Některá slovesa mají zvláštní základ: být – byl, jít – šel, mít – měl.",
        structure="tvar na -l + jsem / jsi / jsme / jste; ve 3. osobě bez pomocného slovesa",
        rules=[
            "Já: byl jsem nebo byla jsem podle mluvčího.",
            "On byl a ona byla, ne on je byl a ona je byla.",
            "Pomocné sloveso není záporné: neměl jsem čas.",
        ],
        examples=[
            GrammarExample("Včera jsem pracovala do pěti.", note="Mluví žena."),
            GrammarExample("Petr šel večer domů."),
            GrammarExample("Neměl jsem telefon.", note="Mluví muž."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Eva je byla doma.",
                "Eva byla doma.",
                "Ve třetí osobě minulého času nepřidáváme je.",
            )
        ],
        related=["cs-past-agreement-a2", "cs-time-expressions-a2"],
    ),
    GrammarTopic(
        "cs-past-agreement-a2",
        "Shoda v minulém čase",
        "A2",
        "Slovesa a shoda",
        "Přizpůsobíme minulý čas osobě, o které mluvíme.",
        "V jednotném čísle používáme mužské -l, ženské -la a střední -lo: Petr "
        "četl, Eva četla, dítě četlo. V množném čísle píšeme u mužského životného "
        "rodu -li, u ženského a mužského neživotného -ly a u středního -la: "
        "muži čekali, ženy čekaly, vlaky čekaly, auta čekala.\n\n"
        "Skupina Petr a Eva má v běžné shodě čekali, protože obsahuje mužskou "
        "životnou osobu. Děti mají zvláštní shodu: děti byly. Při vykání jedné "
        "osobě používáme jste, ale tvar podle rodu této osoby: Pane Nováku, "
        "byl jste doma? Paní Nováková, byla jste doma?",
        rules=[
            "Pomocné jsme vyjadřuje osobu; koncovka -li nebo -ly vyjadřuje složení skupiny.",
            "Dvě ženy řeknou: Byly jsme v kině.",
            "Při vykání jedné ženě říkáme byla jste, nikoli byly jste.",
        ],
        examples=[
            GrammarExample("Jana a Lenka pracovaly v knihovně."),
            GrammarExample("Petr a Jana cestovali vlakem."),
            GrammarExample("Děti byly doma a auta stála před domem."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Eva pracoval doma.",
                "Eva pracovala doma.",
                "Ženský podmět v jednotném čísle vyžaduje koncovku -la.",
            )
        ],
        related=["cs-past-forms-a2"],
    ),
    GrammarTopic(
        "cs-time-expressions-a2",
        "Kdy, jak dlouho a před jakou dobou",
        "A2",
        "Časové výrazy",
        "Umístíme událost v čase a vyjádříme její délku.",
        "Kdy označuje okamžik: v pondělí, v osm hodin, minulý týden. Jak dlouho "
        "označuje trvání: hodinu, dva dny, celý večer. Před se sedmým pádem "
        "udává vzdálenost do minulosti: před hodinou, před týdnem. Za se čtvrtým "
        "pádem může označit vzdálenost do budoucnosti: za hodinu, za týden.\n\n"
        "Od a do mají druhý pád a označují hranice: od rána do večera, od "
        "pondělí do pátku. Pro pořadí událostí používáme nejdřív, potom a nakonec. "
        "Samotné dvě hodiny vyjadřují délku, ve dvě hodiny konkrétní čas.",
        rules=[
            "Délka: Čekal jsem hodinu. Minulý okamžik: Volal před hodinou.",
            "Den v týdnu: v úterý, ve středu, v pátek.",
            "Výrazy včera a loni nepotřebují předložku.",
        ],
        examples=[
            GrammarExample("Včera jsem čekala na autobus dvacet minut."),
            GrammarExample("Kurz začal před týdnem."),
            GrammarExample("Pracujeme od rána do večera."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Volal před hodinu.",
                "Volal před hodinou.",
                "Časové před vyžaduje sedmý pád.",
            )
        ],
        related=["cs-past-forms-a2", "cs-future-a2"],
    ),
    GrammarTopic(
        "cs-aspect-a2",
        "Slovesný vid: dělat a udělat",
        "A2",
        "Slovesa a vid",
        "Rozlišíme činnost a dosažený výsledek.",
        "Nedokonavé sloveso popisuje průběh, opakování nebo činnost bez důrazu na "
        "výsledek: psal jsem dopis, každý den jsem kupoval chléb. Dokonavé sloveso "
        "ukazuje událost jako celek s hranicí nebo výsledkem: napsal jsem dopis, "
        "koupil jsem chléb. Psát dopis neznamená, že dopis určitě zůstal "
        "nedokončený; věta pouze dokončení nepotvrzuje.\n\n"
        "Běžné dvojice jsou dělat – udělat, psát – napsat, číst – přečíst, "
        "kupovat – koupit. Předpona někdy vytváří dokonavé sloveso, ale může "
        "také změnit význam. Proto se učíme dvojice, ne obecné pravidlo "
        "„přidej libovolnou předponu“. Krátká činnost nemusí být dokonavá a "
        "dlouhá činnost může mít dokonavý výsledek.",
        rules=[
            "Co jsi dělal? Četl jsem. Co jsi dokončil? Přečetl jsem knihu.",
            "Pro pravidelnou činnost běžně volíme nedokonavé sloveso.",
            "Tvar přečtu nepopisuje právě probíhající čtení; má budoucí význam.",
        ],
        examples=[
            GrammarExample("Celý večer jsem psala zprávu."),
            GrammarExample("Nakonec jsem zprávu napsala a teď je hotová."),
            GrammarExample("Každou sobotu jsme kupovali zeleninu na trhu."),
        ],
        related=["cs-past-forms-a2", "cs-future-a2"],
    ),
    GrammarTopic(
        "cs-future-a2",
        "Budoucí čas: budu číst a přečtu",
        "A2",
        "Slovesa a čas",
        "Vyjádříme budoucí činnost i plánovaný výsledek.",
        "U nedokonavých sloves tvoříme budoucí čas pomocí budu, budeš, bude, "
        "budeme, budete, budou a infinitivu: budu pracovat. Dokonavá slovesa "
        "mají budoucí význam v tvarech jako udělám, napíšu, koupím; budu k nim "
        "nepřidáváme. Budu číst popisuje činnost, přečtu knihu celý výsledek.\n\n"
        "Sloveso být má budoucí tvary budu, budeš a další bez infinitivu být: "
        "Zítra budu doma. U pohybu používáme mimo jiné půjdu a pojedu. "
        "Zápor tvoříme nebudu pracovat, nenapíšu, nepůjdu.",
        rules=[
            "Nedokonavé sloveso: budu vařit, budeme čekat.",
            "Dokonavé sloveso: uvařím, počkáme.",
            "Budoucí tvar ani slovesný vid samy nezaručují splnění plánu.",
        ],
        examples=[
            GrammarExample("Zítra budu pracovat doma."),
            GrammarExample("Večer napíšu zprávu a přečtu ten krátký článek."),
            GrammarExample("V sobotu nebudeme ve městě."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Budu napsat dopis.",
                "Napíšu dopis.",
                "Napsat je dokonavé; pro budoucí výsledek použijeme napíšu.",
            )
        ],
        related=["cs-aspect-a2", "cs-motion-a2"],
    ),
    GrammarTopic(
        "cs-motion-a2",
        "Jít, chodit, jet a jezdit",
        "A2",
        "Slovesa pohybu",
        "Rozlišíme pěší cestu, jízdu a pravidelný pohyb.",
        "Jít a jet používáme pro pohyb jedním směrem v určité situaci: právě "
        "jdu domů, jedu do Brna. Chodit a jezdit běžně označují opakování: "
        "chodím do práce pěšky, jezdím do práce tramvají. Mohou také popisovat "
        "pohyb různými směry: chodím po pokoji. Jít a chodit obvykle označují "
        "chůzi, jet a jezdit dopravu.\n\n"
        "Minulé tvary jsou šel, šla, šli; chodil; jel; jezdil. Pro jednu "
        "budoucí cestu používáme půjdu nebo pojedu. Pro budoucí pravidelnost "
        "můžeme říct budu chodit nebo budu jezdit. Tyto dvojice nejsou běžné "
        "dvojice dokonavého a nedokonavého vidu; všechna čtyři základní slovesa "
        "jsou nedokonavá.",
        rules=[
            "Jedna cesta právě teď: jedu vlakem. Pravidelně: jezdím vlakem.",
            "Budoucí cesta pěšky: půjdu. Dopravou: pojedu.",
            "Předložky místa a směru zůstávají stejné: do školy, na poštu.",
        ],
        examples=[
            GrammarExample("Každý den chodím do školy pěšky, ale dnes jedu autobusem."),
            GrammarExample("Příští týden pojedeme do Olomouce."),
            GrammarExample("V létě budu jezdit do práce na kole."),
        ],
        related=["cs-direction-a2", "cs-future-a2"],
    ),
    GrammarTopic(
        "cs-reflexives-a2",
        "Zvratná slovesa se se a si",
        "A2",
        "Slovesa a zájmena",
        "Použijeme běžná zvratná spojení a správné místo se nebo si.",
        "Některá slovesa se učíme vždy se se nebo si: smát se, těšit se, "
        "stěžovat si. V jiných spojeních se vztahuje děj k člověku, který ho "
        "dělá: myju se. Si může vyjadřovat, že dělám něco pro sebe: kupuji si "
        "čaj. U tělesné péče porovnáme myju se a myju si ruce; ve druhé větě "
        "jsou přímým předmětem ruce.\n\n"
        "Se a si obvykle stojí za prvním větným celkem: Ráno se sprchuji. "
        "S pomocným slovesem je běžné pořadí jsem se a jsem si: Včera jsem se "
        "sprchoval. Ve druhé osobě minulého času se jsi se a jsi si ve "
        "spisovné češtině spojují do ses a sis: Kdy ses vrátil? Co sis koupila?",
        rules=[
            "Se a si nejsou libovolně zaměnitelné; učíme se celé slovesné spojení.",
            "Ve větě Dnes se cítím dobře stojí se za prvním celkem dnes.",
            "Záporná část patří ke slovesu: necítím se dobře.",
        ],
        examples=[
            GrammarExample("Ráno si myju ruce a potom se oblékám."),
            GrammarExample("Včera jsem se necítila dobře."),
            GrammarExample("Kdy ses vrátil od lékaře?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Já se jsem sprchoval.",
                "Já jsem se sprchoval.",
                "V této skupině krátkých slov stojí jsem před se.",
            )
        ],
        related=["cs-personal-pronouns-a2", "cs-past-forms-a2"],
    ),
    GrammarTopic(
        "cs-reflexive-possessive-a2",
        "Svůj, moje a jeho",
        "A2",
        "Zájmena",
        "Ukážeme, komu patří věc ve větě.",
        "Svůj označuje vlastnictví osoby, která je podmětem stejné věty: Jana "
        "hledá svůj telefon znamená telefon Jany. Jana hledá její telefon "
        "běžně odkazuje na jinou ženu známou ze situace. Svůj používáme u "
        "různých osob: hledám svůj telefon, hledáš svůj telefon, hledáme svůj "
        "telefon.\n\n"
        "Tvar zájmena odpovídá vlastněné věci a jejímu pádu, ne rodu vlastníka: "
        "svůj pas, svou tašku, své jméno, se svým lékařem. Tvary svoje a své "
        "mohou být v některých pozicích obě správné. Moje nebo naše nejsou "
        "vždy chybné, například při zdůraznění rozdílu; zde procvičujeme "
        "neutrální věty s jasným podmětem.",
        rules=[
            "Petr hledá svůj pas: pas patří Petrovi.",
            "Petr hledá jeho pas: pas v běžném kontextu patří jinému muži.",
            "Svůj nemůže být podmětem běžné věty o vlastníkovi: Můj lékař přijde zítra.",
        ],
        examples=[
            GrammarExample("Eva mluví se svým lékařem."),
            GrammarExample("Petr má svůj průkaz a Jana má svůj průkaz."),
            GrammarExample("Beru si svou tašku."),
        ],
        related=["cs-reflexives-a2", "cs-personal-pronouns-a2"],
    ),
    GrammarTopic(
        "cs-imperative-a2",
        "Pokyny a výzvy",
        "A2",
        "Slovesné způsoby",
        "Porozumíme radě, pokynu a jednoduchému zákazu.",
        "Rozkazovací způsob používáme při pokynech i přátelských výzvách. "
        "Běžné tvary jsou čekej, poslouchej, napiš, pojď, vezmi a buď. Pro "
        "vykání nebo více lidí přidáváme -te: čekejte, napište, pojďte, vezměte, "
        "buďte. Některé tvary mění základ, proto je učíme spolu s infinitivem.\n\n"
        "Zápor tvoříme pomocí ne-: nečekejte, nekuřte. Pro zákaz činnosti "
        "obvykle používáme nedokonavé sloveso: Neotvírejte okno. Dokonavý zápor "
        "se objevuje například ve varování: Nezapomeňte na léky. Prosím "
        "a vhodný tón zmírňují přímý pokyn.",
        rules=[
            "Jednomu známému: Počkej tady. Při vykání: Počkejte tady, prosím.",
            "Společný návrh může mít -me: Pojďme domů.",
            "Se a si zachováváme: posaďte se, vezměte si průkaz.",
        ],
        examples=[
            GrammarExample("Otevřete ústa, prosím."),
            GrammarExample("Vezměte si kartičku pojištěnce."),
            GrammarExample("Nekuřte v čekárně."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Prosím, vezmite si průkaz.",
                "Prosím, vezměte si průkaz.",
                "Spisovný tvar pro vykání je vezměte.",
            )
        ],
        related=["cs-aspect-a2", "cs-reflexives-a2", "cs-polite-requests-a2"],
    ),
    GrammarTopic(
        "cs-quantities-a2",
        "Množství: dva rohlíky, pět rohlíků",
        "A2",
        "Číslovky a pády",
        "Objednáme běžné množství a použijeme časté tvary druhého pádu.",
        "V základních spojeních se dvěma až čtyřmi věcmi používáme tvary jako "
        "dva rohlíky, tři banány, čtyři jablka. Od pěti je druhý pád množného "
        "čísla: pět rohlíků, šest banánů, deset jablek. Stejný pád bývá po "
        "hodně a málo: hodně lidí, málo peněz. U ženského a středního rodu "
        "je tvar dvě: dvě tašky, dvě jablka.\n\n"
        "Druhý pád množného čísla nemá jednu univerzální koncovku: rohlíků, "
        "žen, jablek, vajec, lidí. Učíme se ho s často používaným množstvím. "
        "Po názvu obalu nebo míry následuje druhý pád: láhev vody, kilo "
        "sýra, kilo brambor. Věta s pěti a více má v základním vyjádření "
        "počtu tvar je: Na stole je pět jablek.",
        rules=[
            "Jeden rohlík, dva rohlíky, pět rohlíků.",
            "Jedna taška, dvě tašky, pět tašek.",
            "Látku často vyjadřujeme jednotným číslem: litr mléka.",
        ],
        examples=[
            GrammarExample("Prosím pět rohlíků a dvě jablka."),
            GrammarExample("Koupila jsem láhev vody a kilo brambor."),
            GrammarExample("V peněžence mám málo peněz."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Chci pět rohlíky.",
                "Chci pět rohlíků.",
                "Po pět je v tomto spojení druhý pád množného čísla.",
            )
        ],
        related=["cs-genitive-a2"],
    ),
    GrammarTopic(
        "cs-comparison-a2",
        "Porovnávání: levnější, lepší a nejbližší",
        "A2",
        "Přídavná jména a příslovce",
        "Porovnáme vlastnosti a vybereme vhodnou možnost.",
        "Druhý stupeň přídavného jména tvoříme různými koncovkami: levný – "
        "levnější, nový – novější, drahý – dražší. Některé tvary jsou "
        "nepravidelné: dobrý – lepší, špatný – horší, velký – větší, malý – "
        "menší. Pro rozdíl používáme než: Tento pokoj je větší než náš.\n\n"
        "Třetí stupeň přidává nej-: nejlevnější, nejlepší, největší. "
        "Stejnou míru vyjadřujeme tak ... jako: Tento pokoj je tak velký "
        "jako náš. Rozlišujeme vlastnost věci "
        "a způsob činnosti: levnější výrobek, ale nakoupím levněji.",
        rules=[
            "Druhý stupeň: lepší než, dražší než.",
            "Nej- spojujeme s druhým stupněm: blízký – bližší – nejbližší.",
            "Srovnáváme stejnou vlastnost ve stejných podmínkách.",
        ],
        examples=[
            GrammarExample("Tato bunda je levnější než ten kabát."),
            GrammarExample("Která lékárna je nejbližší?"),
            GrammarExample("Na trhu nakoupím levněji než tady."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ten obchod je nejlevný.",
                "Ten obchod je nejlevnější.",
                "Nej- přidáváme k druhému stupni levnější.",
            )
        ],
        related=["cs-polite-requests-a2"],
    ),
    GrammarTopic(
        "cs-polite-requests-a2",
        "Zdvořile: chtěl bych a mohla byste",
        "A2",
        "Slovesné způsoby",
        "Požádáme o pomoc nebo vyjádříme přání zdvořilým způsobem.",
        "Pro běžné žádosti se učíme spojení chtěl bych, chtěla bych a mohl "
        "byste, mohla byste. Základem je tvar na -l a bych, bys, by, bychom, "
        "byste nebo by. Tvar na -l se shoduje s osobou: muž řekne chtěl bych, "
        "žena chtěla bych. Při vykání jednomu člověku je mohl byste nebo "
        "mohla byste podle oslovené osoby.\n\n"
        "Po mohl bych nebo chtěl bych může následovat infinitiv: Chtěl bych "
        "vyměnit košili. Prosím je možné přidat, není ale součástí gramatického "
        "tvaru. Na této úrovni používáme podmiňovací způsob hlavně v žádostech "
        "a přáních; složité nereálné podmínky zatím nepotřebujeme.",
        rules=[
            "První osoba množného čísla je bychom: Chtěli bychom dva lístky.",
            "Při vykání používáme byste, ne by jste.",
            "Krátké bych bývá za prvním celkem: Já bych chtěla menší velikost.",
        ],
        examples=[
            GrammarExample("Chtěla bych vrátit tuto sukni."),
            GrammarExample("Mohl byste mi ukázat levnější model?"),
            GrammarExample("Mohla bych platit kartou?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Mohl by jste mi pomoci?",
                "Mohl byste mi pomoci?",
                "Tvar byste píšeme dohromady; nejde o pomocné jste v minulém čase.",
            )
        ],
        related=["cs-past-agreement-a2", "cs-imperative-a2"],
    ),
    GrammarTopic(
        "cs-connectors-a2",
        "Důvod, výsledek a podmínka",
        "A2",
        "Spojování vět",
        "Spojíme jednoduché informace pomocí protože, proto, když a jestli.",
        "Protože uvádí důvod: Zůstanu doma, protože jsem nemocný. Proto "
        "uvádí výsledek: Jsem nemocný, proto zůstanu doma. Ale označuje "
        "rozdíl nebo překážku: Chci přijít, ale nemám čas.\n\n"
        "Když často vyjadřuje čas nebo opakovanou situaci: Když mám volno, "
        "chodím na procházku. Jestli může vyjádřit otevřenou podmínku: "
        "Jestli bude pršet, zůstaneme doma. Budoucí tvary ve větě po jestli "
        "jsou v češtině běžné. V krátkých zprávách stačí dvě jasně propojené "
        "věty; neztrácíme informaci o tom, kdo co dělá.",
        rules=[
            "Protože odpovídá na proč; proto navazuje následkem.",
            "Před protože a ale obvykle píšeme čárku.",
            "Po úvodní větě s když nebo jestli píšeme čárku před hlavní větou.",
        ],
        examples=[
            GrammarExample("Nemám hotovost, proto zaplatím kartou."),
            GrammarExample("Volám, protože potřebuji jiný termín."),
            GrammarExample("Jestli bude úřad zavřený, přijdu zítra."),
        ],
        related=["cs-future-a2", "cs-modal-verbs-a2"],
    ),
    GrammarTopic(
        "cs-modal-verbs-a2",
        "Musím, můžu, nesmím a nemusím",
        "A2",
        "Způsobová slovesa",
        "Rozlišíme povinnost, možnost, zákaz a nepovinnou činnost.",
        "Po muset, moci a smět stojí infinitiv bez předložky: musím čekat, "
        "můžu přijít, smím vstoupit. Musím označuje povinnost; můžu schopnost, "
        "možnost nebo dovolení podle situace. Tvary můžu i mohu jsou spisovné, "
        "mohu bývá formálnější.\n\n"
        "Nesmím znamená zákaz. Nemusím znamená, že povinnost neexistuje, "
        "nikoli zákaz: Nemusíte přijít osobně, můžete napsat e-mail. "
        "Nemůžu může označovat praktickou nemožnost nebo zákaz podle kontextu. "
        "V minulosti říkáme musel jsem čekat; v budoucnosti budu muset čekat.",
        rules=[
            "Povinnost: Musíte mít průkaz. Zákaz: Nesmíte zde kouřit.",
            "Bez povinnosti: Nemusíte tisknout formulář.",
            "Infinitiv se nemění podle osoby: můžu pracovat, můžeme pracovat.",
        ],
        examples=[
            GrammarExample("Na přepážce musíte ukázat průkaz."),
            GrammarExample("Nemusíte čekat venku, můžete se posadit."),
            GrammarExample("Zítra budu muset zavolat na úřad."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Musím čekám.",
                "Musím čekat.",
                "Po musím potřebujeme infinitiv, ne další určitý slovesný tvar.",
            )
        ],
        related=["cs-future-a2", "cs-connectors-a2"],
    ),
    GrammarTopic(
        "cs-relative-clauses-a2",
        "Který, která a které jako podmět",
        "A2",
        "Spojování vět",
        "Upřesníme známou osobu nebo věc jednoduchou vedlejší větou.",
        "Který může připojit další informaci ke jménu: To je kolega, který "
        "pracuje na recepci. V tomto tématu je který podmětem vedlejší věty, "
        "proto má první pád. Rod a číslo volíme podle jména: obchod, který "
        "otevírá brzy; lékárna, která má otevřeno; okno, které nejde zavřít.\n\n"
        "V množném čísle jsou například kolegové, kteří pomáhají, a "
        "kolegyně, které pomáhají. Podoba zájmena může v jiných větách "
        "záviset také na pádu, ale zde procvičujeme pouze jasné věty, kde "
        "zájmeno samo vykonává činnost. Vedlejší větu oddělujeme čárkou.",
        rules=[
            "Jednotné číslo podmětu: který, která, které.",
            "Mužské životné množné číslo: kteří; ženské množné číslo: které.",
            "Když věta pokračuje za vloženou vedlejší větou, uzavřeme ji další čárkou.",
        ],
        examples=[
            GrammarExample("Hledám obchod, který prodává baterie."),
            GrammarExample("To je pracovnice, která mi pomohla."),
            GrammarExample("Lékárna, která je u nádraží, má dnes otevřeno."),
        ],
        common_mistakes=[
            GrammarMistake(
                "To je lékárna, který má otevřeno.",
                "To je lékárna, která má otevřeno.",
                "Lékárna je ženského rodu; podmět vedlejší věty má tvar která.",
            )
        ],
        related=["cs-connectors-a2", "cs-past-agreement-a2"],
    ),
]
