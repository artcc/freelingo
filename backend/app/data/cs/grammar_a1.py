"""Czech A1 grammar, spelling and introductory pronunciation."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "cs-alphabet-a1",
        "Česká abeceda a diakritika",
        "A1",
        "Písmo a výslovnost",
        "Čti a piš česká písmena včetně háčků, čárek a kroužku.",
        "Čeština používá latinku. Háček najdeš například v písmenech č, š, ž, ř, ň, "
        "ť a ď. Čárka označuje dlouhou samohlásku: á, é, í, ó, ú, ý. Písmeno ů má "
        "kroužek a vyslovuje se stejně dlouze jako ú. Dvojice ch tvoří v české abecedě "
        "jedno písmeno a stojí za h. Písmeno ě čteme podle okolí: dě, tě, ně znějí "
        "měkce, bě a pě obsahují zvuk j; mě běžně vyslovujeme jako mně.\n\n"
        "Diakritiku při psaní zachovej. Jména osob a měst začínají velkým písmenem: "
        "Eva, Praha. Názvy jazyků a dnů mají malé písmeno: čeština, pondělí.",
        rules=[
            "Ú bývá na začátku slova, ů často uvnitř nebo na konci: účet, dům, domů.",
            "Písmena i a y se ve spisovné češtině vyslovují stejně; mohou však měnit "
            "výslovnost předchozího d, t nebo n.",
            "Při hláskování jména uveď také háčky a čárky.",
        ],
        examples=[
            GrammarExample("Jmenuji se Jiří.", note="Ve jméně je ř a dlouhé í."),
            GrammarExample("Učím se česky.", note="Česky píšeme s malým č."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Učím se Česky.", "Učím se česky.", "Příslovce česky není vlastní jméno."
            )
        ],
        related=["cs-sounds-a1"],
    ),
    GrammarTopic(
        "cs-sounds-a1",
        "Délka samohlásek, přízvuk a ř",
        "A1",
        "Písmo a výslovnost",
        "Dlouhá samohláska a přízvuk nejsou totéž.",
        "Slovní přízvuk je v češtině obvykle na první slabice. Samohláska ale může být "
        "dlouhá v kterékoli slabice: ve slově káva je dlouhá první, ve slově malá druhá. "
        "Délka může změnit význam: byt je místo k bydlení, být je sloveso. Čárka tedy "
        "neoznačuje přízvuk. Jednoslabičná původní předložka často nese přízvuk celé "
        "skupiny: na stole.\n\n"
        "Ř je samostatná česká hláska: jazyk se jemně chvěje jako u r a současně "
        "vzniká šum. Není to obyčejné r ani ž. Poslouchej krátká slova řeka, tři a "
        "dobře a opakuj je pomalu bez napětí. Výslovnost ř se podle okolních hlásek "
        "mění. Pro začátek je důležitá srozumitelnost, ne rychlost.",
        rules=[
            "Dlouhé samohlásky vyslovuj déle, ne automaticky silněji.",
            "Ú a ů označují stejnou dlouhou samohlásku.",
            "Srovnávej celé nahrané výrazy; nepřidávej mezi souhlásky další samohlásku.",
        ],
        examples=[
            GrammarExample("To je malá káva.", note="Malá a káva mají přízvuk na první slabice."),
            GrammarExample("Jiří má tři knihy.", note="Poslouchej ř ve jméně a ve slově tři."),
        ],
        related=["cs-alphabet-a1"],
    ),
    GrammarTopic(
        "cs-byt-a1",
        "Já jsem, ty jsi, vy jste",
        "A1",
        "Slovesa a osobní zájmena",
        "Představ se pomocí slovesa být a zvol vhodné oslovení.",
        "Osobní zájmena jsou já, ty, on, ona, ono, my, vy, oni, ony a ona. Sloveso být "
        "má v přítomném čase tvary jsem, jsi, je, jsme, jste, jsou. Zájmeno často "
        "vynecháváme, protože osobu ukazuje sloveso: Jsem Eva. Jsme doma.\n\n"
        "Jednomu kamarádovi obvykle tykáme: Ty jsi Petr? Neznámému dospělému běžně "
        "vykáme: Vy jste pan Novák? Vy a jste používáme také pro více lidí. "
        "Při vykání jedné osobě se přídavné jméno řídí touto osobou: Jste připravený, "
        "pane Nováku? Jste připravená, paní Nováková?",
        structure="já jsem · ty jsi · on/ona/ono je · my jsme · vy jste · oni/ony/ona jsou",
        rules=[
            "Ve větě Já jsem student sloveso jsem nevynechávej.",
            "Vykání je bezpečná volba při prvním rozhovoru s neznámým dospělým.",
            "Jmenuji se Eva se pro začátek nauč jako celý výraz pro představení.",
        ],
        examples=[
            GrammarExample("Jsem student. A ty?"),
            GrammarExample("Dobrý den, jste paní Malá?"),
            GrammarExample("My jsme doma."),
        ],
        common_mistakes=[
            GrammarMistake("Já je Pavel.", "Já jsem Pavel.", "K osobě já patří tvar jsem.")
        ],
        related=["cs-present-a1", "cs-negation-a1"],
    ),
    GrammarTopic(
        "cs-gender-a1",
        "Ten muž, ta žena, to dítě",
        "A1",
        "Podstatná jména",
        "U nového podstatného jména se uč také rod a mužskou životnost.",
        "Čeština má mužský, ženský a střední rod. Pomáhá spojení ten, ta, to: ten stůl, "
        "ta kniha, to okno. Čeština nemá členy; ten, ta a to jsou ukazovací zájmena, "
        "ne povinná součást každého podstatného jména.\n\n"
        "Mužská jména rozlišují životnost: muž a pes jsou životná, stůl a telefon "
        "neživotná. Tato vlastnost ovlivňuje koncovky. Rod nelze určit jen podle "
        "posledního písmene: táta je mužského rodu, noc ženského. Uč se celé spojení.",
        rules=[
            "Mužský rod často končí souhláskou, ženský na -a a střední na -o nebo -e.",
            "Koncovka je pomůcka, ne pravidlo bez výjimek: ten táta, ta tramvaj.",
            "Životnost v gramatice rozlišujeme u mužského rodu.",
        ],
        examples=[
            GrammarExample("To je ten nový stůl."),
            GrammarExample("Ta žena je Eva. To dítě je Adam."),
        ],
        common_mistakes=[
            GrammarMistake("ta táta", "ten táta", "Táta je podstatné jméno mužského rodu.")
        ],
        related=["cs-adjectives-a1", "cs-accusative-a1", "cs-plural-a1"],
    ),
    GrammarTopic(
        "cs-adjectives-a1",
        "Nový byt, nová kniha, nové auto",
        "A1",
        "Přídavná jména",
        "Přizpůsob základní tvar přídavného jména rodu podstatného jména.",
        "Přídavné jméno popisuje osobu nebo věc. V prvním pádě jednotného čísla mají "
        "tvrdá přídavná jména koncovky -ý, -á, -é: nový dům, nová škola, nové město. "
        "Stejná shoda platí po slovese být: Dům je nový. Měkká přídavná jména mají "
        "ve všech třech rodech -í: moderní byt, moderní škola, moderní auto. "
        "Další pády mohou koncovky změnit.",
        structure="nový + mužský rod · nová + ženský rod · nové + střední rod",
        rules=[
            "Tvar zvol podle popisovaného podstatného jména, ne podle mluvčího.",
            "U mužského rodu je v tomto pádě stejná koncovka: nový student, nový stůl.",
        ],
        examples=[
            GrammarExample("To je malá kuchyně."),
            GrammarExample("Okno je velké."),
            GrammarExample("Náš byt je moderní."),
        ],
        common_mistakes=[GrammarMistake("nový kniha", "nová kniha", "Kniha je ženského rodu.")],
        related=["cs-gender-a1", "cs-possessives-a1"],
    ),
    GrammarTopic(
        "cs-possessives-a1",
        "Můj, moje, náš a vaše",
        "A1",
        "Zájmena",
        "Řekni, komu patří věc nebo kdo je členem rodiny.",
        "Přivlastňovací zájmena spojují osobu s věcí nebo člověkem: můj bratr, moje "
        "sestra, moje dítě. V prvním pádě jednotného čísla používáme můj, tvůj, náš, "
        "váš pro mužský rod; moje, tvoje, naše, vaše pro ženský a střední. Také "
        "má kniha a mé auto jsou správné. Jeho a jejich se podle rodu nemění: "
        "jeho byt, jeho auto. Její má zde stejný tvar: její bratr, její sestra.",
        rules=[
            "Rod se řídí tím, co někomu patří: můj telefon, moje taška.",
            "Váš používáme při vykání i při oslovení více lidí.",
            "Tato část procvičuje první pád; v dalších pádech se některé tvary mění.",
        ],
        examples=[
            GrammarExample("To je moje sestra."),
            GrammarExample("Je to váš telefon?"),
            GrammarExample("Náš dům je malý."),
        ],
        common_mistakes=[GrammarMistake("můj auto", "moje auto", "Auto je středního rodu.")],
        related=["cs-gender-a1", "cs-adjectives-a1"],
    ),
    GrammarTopic(
        "cs-plural-a1",
        "Jedna věc a více věcí",
        "A1",
        "Podstatná jména",
        "Poznej běžná podstatná jména v množném čísle.",
        "Množné číslo nemá jednu společnou koncovku. Uč se dvojice: stůl–stoly, "
        "kniha–knihy, ulice–ulice, auto–auta, město–města. U mužských životných jmen "
        "jsou běžné tvary student–studenti a kamarád–kamarádi. Některé dvojice jsou "
        "nepravidelné: dítě–děti, člověk–lidé. Se slovesem být použij jsou: Děti jsou doma.",
        rules=[
            "Po dva, dvě, tři a čtyři v prvním pádě stojí množné číslo: dvě knihy.",
            "Po pět a vyšších základních číslovkách se používá jiný tvar; uč se "
            "celé časté výrazy, například pět korun.",
            "Příklady procvičují první pád, ne všechny pádové tvary.",
        ],
        examples=[
            GrammarExample("To jsou dvě auta."),
            GrammarExample("Studenti jsou tady."),
            GrammarExample("Děti jsou doma."),
        ],
        common_mistakes=[
            GrammarMistake("dvě dítě", "dvě děti", "Dítě má nepravidelné množné číslo děti.")
        ],
        related=["cs-gender-a1", "cs-numbers-time-a1"],
    ),
    GrammarTopic(
        "cs-present-a1",
        "Bydlím, pracuji a mám",
        "A1",
        "Slovesa",
        "Mluv o tom, co děláš teď a co děláš obvykle.",
        "Sloveso se mění podle osoby. U slovesa dělat jsou tvary dělám, děláš, dělá, "
        "děláme, děláte, dělají. Bydlet má bydlím, bydlíš, bydlí, bydlíme, bydlíte, "
        "bydlí. Pracovat má pracuji, pracuješ, pracuje, pracujeme, pracujete, pracují. "
        "Tvary pracuju a pracujou jsou běžné hovorové varianty; nejsou vhodné pro "
        "každý formální text.\n\n"
        "Častá slovesa se uč zvlášť: mít–mám, pít–piju nebo piji, jíst–jím, "
        "číst–čtu, psát–píšu nebo píši. Jedna koncovka neplatí pro všechna slovesa. "
        "Přítomný čas těchto sloves popisuje děj právě teď i pravidelný zvyk.",
        rules=[
            "K infinitivu si zapamatuj alespoň tvar pro já a ty.",
            "Osobní zájmeno nemusíš opakovat: Bydlím tady. Pracuji doma.",
        ],
        examples=[
            GrammarExample("Ráno piju čaj."),
            GrammarExample("Eva pracuje doma."),
            GrammarExample("Máme čas."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Já bydlet tady.", "Já bydlím tady.", "V osobní větě použij určitý tvar slovesa."
            )
        ],
        related=["cs-byt-a1", "cs-negation-a1", "cs-reflexive-a1"],
    ),
    GrammarTopic(
        "cs-questions-a1",
        "Kdo, co, kde a jak",
        "A1",
        "Otázky",
        "Zeptej se na osobu, věc, místo nebo způsob.",
        "Kdo se ptá na osobu, co na věc nebo činnost, kde na místo a jak na způsob "
        "nebo stav: Kdo je to? Co děláš? Kde bydlíte? Jak se máte? Kam se ptá na "
        "směr a kdy na čas. Kolik používáme pro počet nebo cenu.\n\n"
        "Otázka s odpovědí ano nebo ne nepotřebuje pomocné sloveso: Máte čas? "
        "Bydlíš tady? Slovosled je pružný, ale začátečník může používat krátké "
        "věty s tázacím výrazem na začátku.",
        rules=[
            "Rozlišuj kde bydlíš a kam jdeš.",
            "Za přímou otázkou napiš otazník a při poslechu sleduj také intonaci.",
        ],
        examples=[
            GrammarExample("Kde je škola?"),
            GrammarExample("Kolik stojí káva?"),
            GrammarExample("Máte telefon?"),
        ],
        related=["cs-present-a1", "cs-locative-a1", "cs-motion-a1"],
    ),
    GrammarTopic(
        "cs-negation-a1",
        "Nejsem, nemám a nerozumím",
        "A1",
        "Zápor",
        "Odpověz záporně a řekni, co neplatí.",
        "Zápor slovesa většinou tvoří ne- a slovesný tvar v jednom slově: mám–nemám, "
        "pracuji–nepracuji, rozumím–nerozumím. Sloveso být má tvary nejsem, nejsi, "
        "není, nejsme, nejste, nejsou. Tvar není se liší od ostatních.\n\n"
        "Ne může být samostatná odpověď: Máš čas? Ne, nemám. "
        "Ano a ne nejsou součástí slovesa; odděluj je od další věty čárkou.",
        rules=[
            "Předponu ne- piš se slovesem dohromady.",
            "Ve třetí osobě jednotného čísla použij není, nikoli neje.",
        ],
        examples=[
            GrammarExample("Nejsem učitel. Jsem student."),
            GrammarExample("Dnes nemáme čas."),
            GrammarExample("Promiňte, nerozumím."),
        ],
        common_mistakes=[
            GrammarMistake("Eva neje doma.", "Eva není doma.", "Záporný tvar od je je není.")
        ],
        related=["cs-byt-a1", "cs-present-a1"],
    ),
    GrammarTopic(
        "cs-numbers-time-a1",
        "Čísla, ceny a hodiny",
        "A1",
        "Číslovky a čas",
        "Přečti jednoduchou cenu a domluv se na čase.",
        "Základní čísla jsou nula, jedna, dva, tři, čtyři, pět, šest, sedm, osm, "
        "devět a deset. U podstatného jména se jeden mění podle rodu: jeden stůl, "
        "jedna kniha, jedno auto. Dva patří k mužskému rodu, dvě k ženskému "
        "a střednímu: dva stoly, dvě knihy, dvě auta.\n\n"
        "Čas můžeš říct pomocí celých hodin: v osm hodin. Pro 8.30 je srozumitelné "
        "v osm třicet. Běžné půl deváté znamená také 8.30, ne 9.30. "
        "Ceny se pro začátek uč v celých spojeních: jedna koruna, dvě koruny, pět korun.",
        rules=[
            "Telefonní číslo můžeš číst po jednotlivých číslicích.",
            "Na otázku Kdy? odpověz například v devět nebo v pondělí.",
            "Výraz půl deváté označuje polovinu hodiny před devátou.",
        ],
        examples=[
            GrammarExample("Káva stojí třicet korun."),
            GrammarExample("Schůzka je v osm třicet."),
            GrammarExample("Je jedna hodina."),
        ],
        common_mistakes=[GrammarMistake("dva knihy", "dvě knihy", "K ženskému rodu patří dvě.")],
        related=["cs-plural-a1", "cs-questions-a1"],
    ),
    GrammarTopic(
        "cs-accusative-a1",
        "Mám kávu: čtvrtý pád",
        "A1",
        "Pády",
        "Použij základní předmět po slovesech mít, chtít nebo vidět.",
        "Na přímý předmět se ptáme koho? co? a často používáme čtvrtý pád. "
        "Ženské jméno na -a mění koncovku na -u: káva–kávu, voda–vodu. "
        "Ženské jméno na -e ji často mění na -i: růže–růži. "
        "Mužská neživotná a střední jména v těchto jednoduchých příkladech "
        "zůstávají stejná: mám čaj, mám auto.\n\n"
        "Mužská životná jména mají jiný tvar: vidím studenta, kamaráda, muže, tátu. "
        "Nejde tedy jen o konec slova. Přídavné jméno se také mění: "
        "malá káva–malou kávu, nový student–nového studenta.",
        structure="mám / chci / vidím + koho? co?",
        rules=[
            "U mužských jmen rozlišuj životnost: vidím stůl, ale vidím studenta.",
            "Procvičuj celé spojení: jednu malou kávu, jeden čaj, jedno jablko.",
            "Tato pravidla jsou základní vzory, ne úplný přehled všech českých jmen.",
        ],
        examples=[
            GrammarExample("Mám vodu a čaj."),
            GrammarExample("Vidím kamaráda."),
            GrammarExample("Chci malou kávu."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Mám nová kniha.", "Mám novou knihu.", "Předmět po mám je zde ve čtvrtém pádě."
            )
        ],
        related=["cs-gender-a1", "cs-adjectives-a1", "cs-polite-a1"],
    ),
    GrammarTopic(
        "cs-polite-a1",
        "Prosím a zdvořilé žádosti",
        "A1",
        "Zdvořilost",
        "Požádej o něco jasně a zdvořile.",
        "V obchodě nebo kavárně stačí krátké Jednu kávu, prosím. Prosím používáme "
        "také jako odpověď na poděkování. Pro oslovení neznámého dospělého jsou "
        "užitečné celé výrazy Promiňte a Můžete to zopakovat, prosím?\n\n"
        "Objednávku můžeš změkčit spojením Chtěl bych čaj, prosím, když mluví muž, "
        "nebo Chtěla bych čaj, prosím, když mluví žena. Na této úrovni se spojení "
        "uč jako hotový zdvořilý výraz. Podrobné tvoření podmiňovacího způsobu "
        "není potřeba. Přímé Chci čaj je gramaticky správné, ale může znít stroze.\n\n"
        "Při přímém oslovení používáme pátý pád: Petr – Petře, Jana – Jano, "
        "pan – pane. Slovo paní se při oslovení nemění. Tyto běžné tvary se "
        "uč jako celá spojení.",
        rules=[
            "Při vykání použij můžete nebo promiňte; kamarádovi můžeš říct můžeš nebo promiň.",
            "Poděkuj slovem děkuji nebo neformálně díky.",
            "Vzor chtěl bych nebo chtěla bych se řídí mluvčím, ne objednávaným jídlem.",
            "Oslovení odděluj čárkou; uvnitř věty čárkami z obou stran.",
        ],
        examples=[
            GrammarExample("Jednu polévku, prosím."),
            GrammarExample("Chtěla bych vodu, prosím."),
            GrammarExample("Můžete to zopakovat, prosím?"),
            GrammarExample("Petře, máš čas?"),
            GrammarExample("Děkuji, Jano, za pomoc."),
            GrammarExample(
                "Dobrý den, pane Nováku.",
                note="Ženu oslovíme: Dobrý den, paní Nováková.",
            ),
        ],
        related=["cs-byt-a1", "cs-accusative-a1", "cs-modals-a1"],
    ),
    GrammarTopic(
        "cs-locative-a1",
        "Kde? V Praze a na nádraží",
        "A1",
        "Předložky a pády",
        "Řekni, kde se člověk nebo věc nachází.",
        "Na otázku kde často odpovídáme předložkou v nebo na a šestým pádem: "
        "v Praze, v Brně, v obchodě, ve škole, na nádraží, na poště. "
        "Koncovky nejsou stejné u všech slov, proto se uč celé spojení. "
        "Praha má v tomto tvaru změnu h na z: v Praze. "
        "V se pro snadnější výslovnost někdy mění na ve, například ve škole.\n\n"
        "Volbu v nebo na nelze vždy odvodit z významu. Pamatuj si běžné dvojice "
        "míst a předložek. Doma a tady jsou příslovce a další předložku nepotřebují.",
        rules=[
            "Při popisu místa použij například jsem ve škole nebo bydlím v Brně.",
            "Šestý pád stojí vždy s předložkou.",
            "Rozlišuj doma jako místo a domů jako směr.",
        ],
        examples=[
            GrammarExample("Petr je v obchodě."),
            GrammarExample("Jsme na nádraží."),
            GrammarExample("Eva bydlí v Praze."),
        ],
        common_mistakes=[
            GrammarMistake("Bydlím v Praha.", "Bydlím v Praze.", "Po v zde potřebujeme šestý pád.")
        ],
        related=["cs-questions-a1", "cs-motion-a1"],
    ),
    GrammarTopic(
        "cs-motion-a1",
        "Kam? Jdu do školy",
        "A1",
        "Pohyb a směr",
        "Rozlišuj místo a cíl cesty; vyber jít nebo jet.",
        "Kam se ptá na cíl pohybu: Jdu do školy. Jedu do Brna. Jdu na poštu. "
        "Do se pojí s druhým pádem: do školy, do obchodu, do Prahy. "
        "Na při vyjádření cíle používá čtvrtý pád: na poštu, na nádraží. "
        "Nauč se dvojice jsem ve škole–jdu do školy a jsem na poště–jdu na poštu.\n\n"
        "Jít označuje v základním významu pohyb pěšky: jdu, jdeš, jde, jdeme, "
        "jdete, jdou. Jet používáme při cestě dopravním prostředkem: jedu, jedeš, "
        "jede, jedeme, jedete, jedou. Výrazy vlakem a autobusem se nauč jako celé "
        "odpovědi na otázku Jak jedete?",
        rules=[
            "Domů označuje cíl bez předložky: Jdu domů.",
            "Nezaměňuj otázku kde jsi s otázkou kam jdeš.",
            "Jít a jet zde popisují konkrétní cestu, ne všechny opakované pohyby.",
        ],
        examples=[
            GrammarExample("Jdu do obchodu."),
            GrammarExample("Jedeme vlakem do Brna."),
            GrammarExample("Jdeš na nádraží?"),
        ],
        common_mistakes=[
            GrammarMistake("Jdu do škola.", "Jdu do školy.", "Předložka do vyžaduje druhý pád.")
        ],
        related=["cs-locative-a1", "cs-accusative-a1"],
    ),
    GrammarTopic(
        "cs-modals-a1",
        "Chci, můžu a musím",
        "A1",
        "Slovesa",
        "Vyjádři přání, možnost nebo nutnost pomocí infinitivu.",
        "Chci vyjadřuje přání, můžu možnost nebo dovolení a musím nutnost. "
        "Druhé sloveso zůstává v infinitivu: chci číst, můžu přijít, musím pracovat. "
        "Časté tvary jsou chci, chceš, chce, chceme, chcete, chtějí; můžu, můžeš, "
        "může, můžeme, můžete, můžou; musím, musíš, musí, musíme, musíte, musí. "
        "Mohu a mohou jsou také spisovné tvary slovesa moci.\n\n"
        "Nemusím znamená, že něco není nutné. Nemůžu znamená, že to není možné "
        "nebo dovolené. Tyto zápory nemají stejný význam.",
        structure="chci / můžu / musím + infinitiv",
        rules=[
            "Osobu vyjadřuje první sloveso: Chceme plavat.",
            "Záporné ne- patří k tomu slovesu, které popíráš: Dnes nemusím pracovat.",
        ],
        examples=[
            GrammarExample("Můžu platit kartou?"),
            GrammarExample("Chceme hrát fotbal."),
            GrammarExample("Dnes musím pracovat."),
        ],
        common_mistakes=[
            GrammarMistake("Chci čtu.", "Chci číst.", "Po chci zůstává druhé sloveso v infinitivu.")
        ],
        related=["cs-present-a1", "cs-polite-a1", "cs-negation-a1"],
    ),
    GrammarTopic(
        "cs-reflexive-a1",
        "Jmenuji se a učím se",
        "A1",
        "Slovesa a slovosled",
        "Uč se slovesa společně s jejich se nebo si.",
        "Některá slovesa používáme se se nebo si: jmenovat se, učit se, dívat se, "
        "hrát si. Tato krátká slova nelze libovolně měnit nebo vynechávat. "
        "Učit znamená například předávat znalosti druhým, učit se znamená "
        "získávat znalosti sám.\n\n"
        "Se a si v běžné oznamovací větě obvykle stojí za prvním větným členem, "
        "nikoli vždy za prvním napsaným slovem: Každý den se učím. "
        "Pokud je na začátku sloveso, stojí za ním: Učím se česky. "
        "Spojení se více krátkými slovy se uč postupně v celých větách.",
        rules=[
            "Do slovníčku napiš celý infinitiv: dívat se, nikoli jen dívat.",
            "První větný člen může mít více slov: Dnes večer se učím.",
            "Hraju fotbal a hraju si jsou různá spojení; si se nepřidává ke každému hrát.",
        ],
        examples=[
            GrammarExample("Jmenuji se Jana."),
            GrammarExample("Každý den se učím česky."),
            GrammarExample("Dítě si hraje."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Já jmenuji Eva.", "Já se jmenuji Eva.", "Sloveso pro uvedení jména je jmenovat se."
            )
        ],
        related=["cs-present-a1", "cs-questions-a1"],
    ),
    GrammarTopic(
        "cs-coordination-a1",
        "A, ale, nebo",
        "A1",
        "Spojování vět",
        "Spoj dvě jednoduché informace a nabídni volbu.",
        "A přidává další informaci: Mám čaj a vodu. Ale vyjadřuje rozdíl nebo "
        "protiklad: Chci jít ven, ale nemám čas. Nebo nabízí možnosti: Chceš čaj, "
        "nebo kávu? V krátkém výčtu bez zdůrazněného protikladu se před nebo "
        "čárka obvykle nepíše: Můžete přijít v pondělí nebo v úterý.\n\n"
        "Začni dvěma krátkými větami. Spojka nemění sama o sobě tvar slovesa "
        "ani nevyžaduje zvláštní slovosled.",
        rules=[
            "Před ale napiš čárku.",
            "Při prostém spojení dvou informací před a čárku obvykle nepiš.",
            "Vyber spojku podle významu: přidání, rozdíl, nebo volba.",
        ],
        examples=[
            GrammarExample("Jsem doma a čtu."),
            GrammarExample("Mám hlad, ale nechci polévku."),
            GrammarExample("Můžete zavolat dnes nebo zítra."),
        ],
        related=["cs-negation-a1", "cs-present-a1"],
    ),
]
