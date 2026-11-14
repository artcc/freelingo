"""Czech A1 vocabulary with Czech definitions and contextual examples."""

from app.data._types import VocabularyEntry, VocabularySet

A1_SETS: list[VocabularySet] = [
    VocabularySet(
        "cs_identity_a1",
        "A1",
        "Pozdravy, jméno a první rozhovor",
        "a1-unit-1",
        [
            VocabularyEntry(
                "dobrý den", "phrase", "Zdvořilý pozdrav během dne.", "Dobrý den, jsem Eva."
            ),
            VocabularyEntry(
                "ahoj", "phrase", "Pozdrav mezi kamarády při setkání i loučení.", "Ahoj, Petře!"
            ),
            VocabularyEntry(
                "na shledanou",
                "phrase",
                "Zdvořilý pozdrav při odchodu.",
                "Na shledanou a hezký den!",
            ),
            VocabularyEntry(
                "prosím",
                "phrase",
                "Zdvořilé slovo při žádosti nebo jako odpověď na poděkování.",
                "Jednu vodu, prosím.",
            ),
            VocabularyEntry(
                "děkuji", "phrase", "Slovo, kterým vyjadřujeme vděčnost.", "Děkuji za pomoc."
            ),
            VocabularyEntry("ano", "phrase", "Kladná odpověď na otázku.", "Ano, jsem student."),
            VocabularyEntry("ne", "phrase", "Záporná odpověď na otázku.", "Ne, nejsem učitel."),
            VocabularyEntry(
                "jméno", "noun", "Osobní označení, například Eva nebo Petr.", "Moje jméno je Jana."
            ),
            VocabularyEntry(
                "příjmení",
                "noun",
                "Rodinné jméno, například Novák nebo Nováková.",
                "Moje příjmení je Malá.",
            ),
            VocabularyEntry(
                "čeština", "noun", "Jazyk, kterým se mluví v Česku.", "Čeština je můj nový jazyk."
            ),
            VocabularyEntry(
                "jazyk",
                "noun",
                "Systém slov a pravidel pro dorozumění.",
                "Jaký jazyk se učíte?",
            ),
            VocabularyEntry(
                "písmeno", "noun", "Znak abecedy, například a nebo č.", "Ř je české písmeno."
            ),
            VocabularyEntry(
                "slovo",
                "noun",
                "Část řeči nebo textu, která má význam.",
                "Co znamená slovo ahoj?",
            ),
            VocabularyEntry(
                "otázka",
                "noun",
                "Věta, kterou žádáme o informaci.",
                "To je jednoduchá otázka.",
            ),
            VocabularyEntry(
                "odpověď",
                "noun",
                "Informace, kterou dáváme po otázce.",
                "Moje odpověď je ano.",
            ),
            VocabularyEntry(
                "student",
                "noun",
                "Muž nebo chlapec, který se vzdělává ve škole.",
                "Petr je student.",
            ),
            VocabularyEntry(
                "studentka",
                "noun",
                "Žena nebo dívka, která se vzdělává ve škole.",
                "Eva je studentka.",
            ),
            VocabularyEntry(
                "učitel",
                "noun",
                "Muž, který pomáhá žákům získávat znalosti.",
                "Náš učitel je pan Novák.",
            ),
            VocabularyEntry(
                "učitelka",
                "noun",
                "Žena, která pomáhá žákům získávat znalosti.",
                "Naše učitelka je paní Malá.",
            ),
            VocabularyEntry(
                "Česko",
                "noun",
                "Země ve střední Evropě, jejímž hlavním městem je Praha.",
                "Česko je můj domov.",
            ),
            VocabularyEntry(
                "být", "verb", "Existovat nebo mít určitý stav či vlastnost.", "Jsem doma."
            ),
            VocabularyEntry(
                "jmenovat se",
                "verb",
                "Mít určité osobní jméno.",
                "Jmenuji se Tomáš.",
            ),
            VocabularyEntry(
                "rozumět",
                "verb",
                "Vědět, co někdo říká nebo co něco znamená.",
                "Rozumím jen trochu.",
            ),
            VocabularyEntry("mluvit", "verb", "Vyjadřovat slova hlasem.", "Mluvím česky."),
            VocabularyEntry(
                "číst", "verb", "Poznávat napsaná slova a jejich význam.", "Čtu krátký text."
            ),
            VocabularyEntry(
                "psát",
                "verb",
                "Zaznamenávat písmena a slova na papír nebo do počítače.",
                "Píšu svoje jméno.",
            ),
            VocabularyEntry(
                "adresa",
                "noun",
                "Údaj o ulici, čísle domu a obci, kde někdo bydlí.",
                "Jaká je vaše adresa?",
            ),
            VocabularyEntry(
                "telefon",
                "noun",
                "Přístroj pro volání a posílání zpráv.",
                "To je můj telefon.",
            ),
        ],
    ),
    VocabularySet(
        "cs_family_home_a1",
        "A1",
        "Rodina, lidé a věci doma",
        "a1-unit-2",
        [
            VocabularyEntry(
                "rodina",
                "noun",
                "Blízcí příbuzní, například rodiče a děti.",
                "Moje rodina je malá.",
            ),
            VocabularyEntry(
                "matka", "noun", "Žena, která je rodičem dítěte.", "Moje matka je učitelka."
            ),
            VocabularyEntry("otec", "noun", "Muž, který je rodičem dítěte.", "Můj otec je doma."),
            VocabularyEntry(
                "sestra",
                "noun",
                "Dívka nebo žena, která má se mnou alespoň jednoho společného rodiče.",
                "Moje sestra se jmenuje Anna.",
            ),
            VocabularyEntry(
                "bratr",
                "noun",
                "Chlapec nebo muž, který má se mnou alespoň jednoho společného rodiče.",
                "Můj bratr je student.",
            ),
            VocabularyEntry(
                "dítě", "noun", "Člověk, který ještě není dospělý.", "To dítě je malé."
            ),
            VocabularyEntry(
                "rodiče",
                "noun",
                "Lidé, kteří jsou matkou nebo otcem dítěte.",
                "Rodiče jsou doma.",
            ),
            VocabularyEntry(
                "kamarád",
                "noun",
                "Blízký známý, se kterým trávíme volný čas.",
                "To je můj kamarád.",
            ),
            VocabularyEntry(
                "kamarádka",
                "noun",
                "Blízká známá, se kterou trávíme volný čas.",
                "Eva je moje kamarádka.",
            ),
            VocabularyEntry(
                "muž", "noun", "Dospělý člověk mužského pohlaví.", "Ten muž je můj otec."
            ),
            VocabularyEntry(
                "žena", "noun", "Dospělý člověk ženského pohlaví.", "Ta žena je naše učitelka."
            ),
            VocabularyEntry(
                "byt",
                "noun",
                "Prostor k bydlení s jednou nebo více místnostmi v domě.",
                "Náš byt je malý.",
            ),
            VocabularyEntry(
                "dům", "noun", "Budova, ve které mohou lidé bydlet.", "Ten dům je nový."
            ),
            VocabularyEntry(
                "pokoj", "noun", "Místnost v bytě nebo v hotelu.", "Můj pokoj je velký."
            ),
            VocabularyEntry(
                "kuchyně", "noun", "Místnost, kde připravujeme jídlo.", "Kuchyně je malá."
            ),
            VocabularyEntry(
                "koupelna",
                "noun",
                "Místnost s umyvadlem a obvykle se sprchou nebo vanou.",
                "Koupelna je tady.",
            ),
            VocabularyEntry(
                "stůl", "noun", "Nábytek s deskou, u kterého jíme nebo pracujeme.", "Stůl je nový."
            ),
            VocabularyEntry(
                "židle", "noun", "Nábytek pro sezení jedné osoby.", "To je moje židle."
            ),
            VocabularyEntry("postel", "noun", "Nábytek určený ke spaní.", "Postel je velká."),
            VocabularyEntry(
                "okno",
                "noun",
                "Skleněná část stěny, kterou do místnosti přichází světlo.",
                "Okno je malé.",
            ),
            VocabularyEntry(
                "dveře",
                "noun",
                "Pohyblivá část, která zavírá vstup do místnosti nebo domu.",
                "Dveře jsou bílé.",
            ),
            VocabularyEntry(
                "klíč", "noun", "Malý předmět pro zamykání a odemykání.", "To je můj klíč."
            ),
            VocabularyEntry(
                "taška",
                "noun",
                "Věc s uchy nebo popruhem pro přenášení předmětů.",
                "Taška je tady.",
            ),
            VocabularyEntry(
                "malý", "adjective", "Takový, který nemá velké rozměry.", "Náš stůl je malý."
            ),
            VocabularyEntry(
                "velký", "adjective", "Takový, který má značné rozměry.", "To je velký dům."
            ),
            VocabularyEntry(
                "nový",
                "adjective",
                "Nedávno vzniklý, získaný nebo dosud nepoužitý.",
                "To je nový byt.",
            ),
            VocabularyEntry(
                "starý", "adjective", "Takový, který existuje už dlouhou dobu.", "Ten dům je starý."
            ),
            VocabularyEntry(
                "můj", "pronoun", "Patřící mně nebo spojený se mnou.", "To je můj pokoj."
            ),
        ],
    ),
    VocabularySet(
        "cs_routines_a1",
        "A1",
        "Dny, čas a každodenní činnosti",
        "a1-unit-3",
        [
            VocabularyEntry(
                "den", "noun", "Časový úsek dlouhý dvacet čtyři hodin.", "Dnes je hezký den."
            ),
            VocabularyEntry(
                "týden",
                "noun",
                "Období sedmi dní; v kalendáři od pondělí do neděle.",
                "Týden má sedm dní.",
            ),
            VocabularyEntry("ráno", "adverb", "Na začátku dne po noci.", "Ráno vstávám v sedm."),
            VocabularyEntry(
                "dopoledne", "adverb", "V části dne mezi ránem a polednem.", "Dopoledne pracuji."
            ),
            VocabularyEntry(
                "poledne", "noun", "Doba kolem dvanácté hodiny během dne.", "Je poledne."
            ),
            VocabularyEntry(
                "odpoledne", "adverb", "V části dne po poledni a před večerem.", "Odpoledne čtu."
            ),
            VocabularyEntry("večer", "adverb", "Na konci dne před nocí.", "Večer jsem doma."),
            VocabularyEntry(
                "noc", "noun", "Tmavá část dne, kdy většina lidí spí.", "Noc je dlouhá."
            ),
            VocabularyEntry("dnes", "adverb", "V den, který právě probíhá.", "Dnes nepracuji."),
            VocabularyEntry(
                "zítra", "adverb", "V den, který následuje po dnešku.", "Zítra mám čas."
            ),
            VocabularyEntry(
                "včera", "adverb", "V den před dneškem.", "Včera: pondělí. Dnes: úterý."
            ),
            VocabularyEntry(
                "pondělí", "noun", "První den běžného kalendářního týdne.", "V pondělí pracuji."
            ),
            VocabularyEntry("úterý", "noun", "Den mezi pondělím a středou.", "V úterý mám školu."),
            VocabularyEntry("středa", "noun", "Den mezi úterým a čtvrtkem.", "Dnes je středa."),
            VocabularyEntry(
                "čtvrtek", "noun", "Den mezi středou a pátkem.", "Ve čtvrtek pracuji doma."
            ),
            VocabularyEntry("pátek", "noun", "Den před sobotou.", "V pátek mám čas."),
            VocabularyEntry("sobota", "noun", "Den mezi pátkem a nedělí.", "V sobotu nepracuji."),
            VocabularyEntry(
                "neděle",
                "noun",
                "Poslední den běžného kalendářního týdne.",
                "V neděli dlouho spím.",
            ),
            VocabularyEntry(
                "hodina",
                "noun",
                "Časový úsek dlouhý šedesát minut.",
                "Jedna hodina má šedesát minut.",
            ),
            VocabularyEntry(
                "minuta", "noun", "Časový úsek dlouhý šedesát sekund.", "Jedna minuta je krátká."
            ),
            VocabularyEntry(
                "práce",
                "noun",
                "Činnost, kterou člověk dělá například za peníze.",
                "Moje práce je zajímavá.",
            ),
            VocabularyEntry(
                "škola",
                "noun",
                "Místo, kde se žáci nebo studenti vzdělávají.",
                "Naše škola je velká.",
            ),
            VocabularyEntry("bydlet", "verb", "Mít někde svůj domov.", "Bydlím tady."),
            VocabularyEntry(
                "pracovat",
                "verb",
                "Vykonávat činnost, například za mzdu.",
                "Pracujeme doma.",
            ),
            VocabularyEntry("dělat", "verb", "Vykonávat nějakou činnost.", "Co děláš ráno?"),
            VocabularyEntry(
                "mít", "verb", "Vlastnit něco, například auto nebo telefon.", "Máme nový stůl."
            ),
            VocabularyEntry(
                "vstávat",
                "verb",
                "Přestávat ležet v posteli a začínat den.",
                "Vstávám v šest hodin.",
            ),
            VocabularyEntry(
                "spát", "verb", "Odpočívat ve stavu, kdy běžně nevnímáme okolí.", "Dítě spí."
            ),
        ],
    ),
    VocabularySet(
        "cs_numbers_a1",
        "A1",
        "Čísla a peníze",
        "a1-unit-3",
        [
            VocabularyEntry(
                "nula", "numeral", "Číslo 0; žádný kus.", "Telefonní číslo končí nulou."
            ),
            VocabularyEntry("jeden", "numeral", "Počet 1 v mužském rodě.", "Tady je jeden stůl."),
            VocabularyEntry("dva", "numeral", "Počet 2 v mužském rodě.", "To jsou dva telefony."),
            VocabularyEntry(
                "tři", "numeral", "Počet 3, o jeden více než dva.", "Tady jsou tři židle."
            ),
            VocabularyEntry(
                "čtyři", "numeral", "Počet 4, o jeden více než tři.", "Máme čtyři okna."
            ),
            VocabularyEntry(
                "pět", "numeral", "Počet 5, například počet prstů na jedné ruce.", "Je pět hodin."
            ),
            VocabularyEntry("šest", "numeral", "Počet 6, o jeden více než pět.", "Vstávám v šest."),
            VocabularyEntry(
                "sedm", "numeral", "Počet 7, například počet dní v týdnu.", "Je sedm hodin."
            ),
            VocabularyEntry(
                "osm", "numeral", "Počet 8, o jeden více než sedm.", "Pracuji od osmi hodin."
            ),
            VocabularyEntry(
                "devět", "numeral", "Počet 9, o jeden méně než deset.", "Je devět hodin."
            ),
            VocabularyEntry(
                "deset", "numeral", "Počet 10; dvě skupiny po pěti.", "Máme deset minut."
            ),
            VocabularyEntry(
                "jedenáct", "numeral", "Počet 11, o jeden více než deset.", "Je jedenáct hodin."
            ),
            VocabularyEntry(
                "dvanáct",
                "numeral",
                "Počet 12, například počet měsíců v roce.",
                "Je dvanáct hodin.",
            ),
            VocabularyEntry(
                "třináct", "numeral", "Počet 13, o jeden více než dvanáct.", "Máme třináct minut."
            ),
            VocabularyEntry(
                "čtrnáct", "numeral", "Počet 14, o dva více než dvanáct.", "Čekáme čtrnáct minut."
            ),
            VocabularyEntry("patnáct", "numeral", "Počet 15; deset a pět.", "Mám patnáct korun."),
            VocabularyEntry(
                "šestnáct", "numeral", "Počet 16; deset a šest.", "Vlak jede v šestnáct hodin."
            ),
            VocabularyEntry(
                "sedmnáct", "numeral", "Počet 17; deset a sedm.", "To stojí sedmnáct korun."
            ),
            VocabularyEntry("osmnáct", "numeral", "Počet 18; deset a osm.", "Máme osmnáct minut."),
            VocabularyEntry(
                "devatenáct",
                "numeral",
                "Počet 19, o jeden méně než dvacet.",
                "Vlak jede v devatenáct hodin.",
            ),
            VocabularyEntry("dvacet", "numeral", "Počet 20; dvě desítky.", "Mám dvacet korun."),
            VocabularyEntry(
                "třicet", "numeral", "Počet 30; tři desítky.", "Káva stojí třicet korun."
            ),
            VocabularyEntry(
                "čtyřicet", "numeral", "Počet 40; čtyři desítky.", "Čaj stojí čtyřicet korun."
            ),
            VocabularyEntry(
                "padesát", "numeral", "Počet 50; pět desítek.", "Čaj stojí padesát korun."
            ),
            VocabularyEntry(
                "šedesát", "numeral", "Počet 60; šest desítek.", "Hodina má šedesát minut."
            ),
            VocabularyEntry(
                "sedmdesát",
                "numeral",
                "Počet 70; sedm desítek.",
                "Jízdenka stojí sedmdesát korun.",
            ),
            VocabularyEntry(
                "osmdesát", "numeral", "Počet 80; osm desítek.", "Účet je osmdesát korun."
            ),
            VocabularyEntry(
                "devadesát",
                "numeral",
                "Počet 90; devět desítek.",
                "To stojí devadesát korun.",
            ),
            VocabularyEntry("sto", "numeral", "Počet 100; deset desítek.", "Mám sto korun."),
            VocabularyEntry(
                "tisíc", "numeral", "Počet 1000; deset stovek.", "To stojí tisíc korun."
            ),
            VocabularyEntry(
                "koruna",
                "noun",
                "Základní jednotka českých peněz, označovaná Kč.",
                "Jedna koruna je sto haléřů.",
            ),
            VocabularyEntry(
                "euro",
                "noun",
                "Peněžní jednotka používaná například na Slovensku a v Německu.",
                "To stojí jedno euro.",
            ),
        ],
    ),
    VocabularySet(
        "cs_food_a1",
        "A1",
        "Jídlo, pití a placení",
        "a1-unit-4",
        [
            VocabularyEntry(
                "voda",
                "noun",
                "Čirá tekutina, kterou pijeme a používáme k mytí.",
                "Prosím jednu vodu.",
            ),
            VocabularyEntry(
                "čaj",
                "noun",
                "Nápoj připravený z lístků nebo bylin a horké vody.",
                "Piju černý čaj.",
            ),
            VocabularyEntry(
                "káva", "noun", "Nápoj připravený z pražených kávových zrn.", "Mám malou kávu."
            ),
            VocabularyEntry(
                "mléko", "noun", "Bílý nápoj, který získáváme například od krav.", "Piju mléko."
            ),
            VocabularyEntry(
                "chléb", "noun", "Základní pečivo, které často krájíme na krajíce.", "Jím chléb."
            ),
            VocabularyEntry(
                "rohlík", "noun", "Menší podlouhlé české pečivo.", "Chci jeden rohlík."
            ),
            VocabularyEntry(
                "máslo", "noun", "Tuk z mléka, který často mažeme na pečivo.", "Máme máslo?"
            ),
            VocabularyEntry(
                "sýr",
                "noun",
                "Potravina vyrobená z mléka, často v plátcích nebo kusech.",
                "Kupuji sýr.",
            ),
            VocabularyEntry(
                "vejce",
                "noun",
                "Potravina od slepice s bílkem, žloutkem a skořápkou.",
                "Jím jedno vejce.",
            ),
            VocabularyEntry("maso", "noun", "Potravina z těla zvířete.", "Nejím maso."),
            VocabularyEntry(
                "ryba", "noun", "Živočich žijící ve vodě, také potravina z něj.", "Dnes máme rybu."
            ),
            VocabularyEntry(
                "polévka", "noun", "Tekuté jídlo, které obvykle jíme lžící.", "Chci teplou polévku."
            ),
            VocabularyEntry(
                "rýže", "noun", "Drobná zrna, která po uvaření jíme jako přílohu.", "Máte rýži?"
            ),
            VocabularyEntry(
                "brambora",
                "noun",
                "Jedlá hlíza, kterou vaříme, pečeme nebo smažíme.",
                "Ta brambora je velká.",
            ),
            VocabularyEntry(
                "jablko", "noun", "Kulatý plod jabloně s jadérky.", "Jím červené jablko."
            ),
            VocabularyEntry(
                "banán",
                "noun",
                "Podlouhlý plod, obvykle se žlutou slupkou a měkkou světlou dužinou.",
                "Mám jeden banán.",
            ),
            VocabularyEntry(
                "zelenina",
                "noun",
                "Jedlé části rostlin, například mrkev nebo salát.",
                "Kupuji zeleninu.",
            ),
            VocabularyEntry(
                "ovoce", "noun", "Jedlé plody, například jablka a hrušky.", "Jím ovoce každý den."
            ),
            VocabularyEntry(
                "sůl",
                "noun",
                "Bílá látka se slanou chutí, kterou přidáváme do jídla.",
                "Kde je sůl?",
            ),
            VocabularyEntry(
                "cukr",
                "noun",
                "Sladká látka, kterou přidáváme do nápojů a jídla.",
                "Cukr nechci, děkuji.",
            ),
            VocabularyEntry(
                "snídaně", "noun", "První jídlo dne, obvykle ráno.", "Snídaně je v sedm hodin."
            ),
            VocabularyEntry("oběd", "noun", "Hlavní jídlo kolem poledne.", "Oběd je ve dvanáct."),
            VocabularyEntry(
                "večeře", "noun", "Jídlo, které jíme na konci dne.", "Večeře je v šest."
            ),
            VocabularyEntry("jíst", "verb", "Přijímat potravu ústy.", "Jíme polévku."),
            VocabularyEntry("pít", "verb", "Přijímat tekutinu ústy.", "Piju vodu."),
            VocabularyEntry(
                "koupit", "verb", "Získat něco výměnou za peníze.", "Chci koupit chléb."
            ),
            VocabularyEntry(
                "účet", "noun", "Doklad s částkou, kterou je potřeba zaplatit.", "Účet, prosím."
            ),
            VocabularyEntry(
                "platit", "verb", "Dávat peníze za zboží nebo službu.", "Platím kartou."
            ),
        ],
    ),
    VocabularySet(
        "cs_city_a1",
        "A1",
        "Město, doprava a cesta",
        "a1-unit-5",
        [
            VocabularyEntry(
                "město", "noun", "Větší obec s ulicemi, domy a službami.", "Brno je velké město."
            ),
            VocabularyEntry(
                "vesnice", "noun", "Menší obec, často na venkově.", "Naše vesnice je malá."
            ),
            VocabularyEntry("ulice", "noun", "Cesta mezi domy v obci.", "Tato ulice je dlouhá."),
            VocabularyEntry(
                "náměstí", "noun", "Větší otevřené místo mezi domy ve městě.", "Jsme na náměstí."
            ),
            VocabularyEntry("obchod", "noun", "Místo, kde se prodává zboží.", "Jdu do obchodu."),
            VocabularyEntry(
                "supermarket",
                "noun",
                "Velký obchod hlavně s potravinami a potřebami pro domácnost.",
                "Supermarket je vpravo.",
            ),
            VocabularyEntry(
                "pekárna", "noun", "Místo, kde se peče nebo prodává pečivo.", "Jdu do pekárny."
            ),
            VocabularyEntry(
                "kavárna",
                "noun",
                "Podnik, kde si lidé objednávají kávu a jiné nápoje.",
                "Eva je v kavárně.",
            ),
            VocabularyEntry(
                "restaurace",
                "noun",
                "Podnik, kde si lidé objednávají hotové jídlo.",
                "Restaurace je vlevo.",
            ),
            VocabularyEntry(
                "pošta", "noun", "Místo, kde posíláme dopisy a balíky.", "Jdu na poštu."
            ),
            VocabularyEntry(
                "banka",
                "noun",
                "Instituce, která spravuje peníze a účty klientů.",
                "Banka je na náměstí.",
            ),
            VocabularyEntry(
                "lékárna", "noun", "Místo, kde dostaneme nebo koupíme léky.", "Lékárna je tady."
            ),
            VocabularyEntry(
                "nemocnice",
                "noun",
                "Zařízení, kde lékaři léčí nemocné a zraněné lidi.",
                "Jedu do nemocnice.",
            ),
            VocabularyEntry(
                "nádraží",
                "noun",
                "Místo, odkud odjíždějí vlaky nebo dálkové autobusy.",
                "Jsme na nádraží.",
            ),
            VocabularyEntry(
                "zastávka",
                "noun",
                "Místo, kde pravidelně zastavuje autobus nebo tramvaj.",
                "Zastávka je tam.",
            ),
            VocabularyEntry(
                "autobus",
                "noun",
                "Velké silniční vozidlo pro více cestujících.",
                "Autobus jede do centra.",
            ),
            VocabularyEntry(
                "tramvaj",
                "noun",
                "Městské vozidlo, které jezdí po kolejích v ulicích.",
                "Tramvaj číslo tři je tady.",
            ),
            VocabularyEntry(
                "vlak",
                "noun",
                "Dopravní prostředek z vozů, který jezdí po železnici.",
                "Vlak jede do Brna.",
            ),
            VocabularyEntry(
                "metro", "noun", "Městská dráha, která vede často pod zemí.", "V Praze je metro."
            ),
            VocabularyEntry(
                "jízdenka",
                "noun",
                "Doklad o zaplacení cesty veřejnou dopravou.",
                "Mám jízdenku do Prahy.",
            ),
            VocabularyEntry(
                "auto",
                "noun",
                "Menší silniční vozidlo obvykle pro několik lidí.",
                "Naše auto je staré.",
            ),
            VocabularyEntry("jít", "verb", "Pohybovat se pěšky určitým směrem.", "Jdu domů."),
            VocabularyEntry("jet", "verb", "Pohybovat se dopravním prostředkem.", "Jedu vlakem."),
            VocabularyEntry("vlevo", "adverb", "Na levé straně.", "Pošta je vlevo."),
            VocabularyEntry("vpravo", "adverb", "Na pravé straně.", "Obchod je vpravo."),
            VocabularyEntry("rovně", "adverb", "Přímo vpřed bez odbočení.", "Jděte rovně."),
            VocabularyEntry("tady", "adverb", "Na tomto místě blízko mluvčího.", "Bydlím tady."),
            VocabularyEntry(
                "tam", "adverb", "Na jiném, obvykle vzdálenějším místě.", "Nádraží je tam."
            ),
        ],
    ),
    VocabularySet(
        "cs_leisure_a1",
        "A1",
        "Volný čas a setkání",
        "a1-unit-6",
        [
            VocabularyEntry(
                "čas", "noun", "Doba, kterou máme pro činnost nebo setkání.", "Máš dnes čas?"
            ),
            VocabularyEntry(
                "víkend", "noun", "Sobota a neděle společně.", "O víkendu nepracujeme."
            ),
            VocabularyEntry(
                "park",
                "noun",
                "Veřejné místo se stromy a cestami pro odpočinek.",
                "Jdeme do parku.",
            ),
            VocabularyEntry(
                "kino",
                "noun",
                "Místo, kde diváci sledují filmy na velkém plátně.",
                "Chci jít do kina.",
            ),
            VocabularyEntry(
                "divadlo", "noun", "Místo, kde herci hrají před diváky.", "Divadlo je v centru."
            ),
            VocabularyEntry(
                "kniha",
                "noun",
                "Soubor spojených stránek s textem nebo obrázky.",
                "Čtu novou knihu.",
            ),
            VocabularyEntry(
                "film",
                "noun",
                "Příběh nebo záznam v pohyblivých obrazech.",
                "Ten film je zajímavý.",
            ),
            VocabularyEntry(
                "hudba",
                "noun",
                "Zvuky a tóny uspořádané do melodie nebo rytmu.",
                "Poslouchám hudbu.",
            ),
            VocabularyEntry(
                "písnička",
                "noun",
                "Krátká skladba se slovy, kterou zpíváme.",
                "To je hezká písnička.",
            ),
            VocabularyEntry(
                "sport",
                "noun",
                "Pohybová činnost pro zábavu, zdraví nebo soutěž.",
                "Fotbal je můj oblíbený sport.",
            ),
            VocabularyEntry(
                "fotbal",
                "noun",
                "Hra dvou týmů, které se snaží kopnout míč do branky.",
                "V sobotu hrajeme fotbal.",
            ),
            VocabularyEntry(
                "kolo", "noun", "Dopravní prostředek se dvěma koly a pedály.", "Mám nové kolo."
            ),
            VocabularyEntry(
                "procházka",
                "noun",
                "Chůze venku pro odpočinek nebo zábavu.",
                "Chci jít na procházku.",
            ),
            VocabularyEntry(
                "výlet",
                "noun",
                "Kratší cesta pro poznání a odpočinek.",
                "V sobotu jedeme na výlet.",
            ),
            VocabularyEntry(
                "fotografie",
                "noun",
                "Obraz zachycený fotoaparátem nebo telefonem.",
                "To je moje fotografie.",
            ),
            VocabularyEntry(
                "hrát",
                "verb",
                "Věnovat se hře, sportu nebo hudebnímu nástroji.",
                "Chceme hrát fotbal.",
            ),
            VocabularyEntry("plavat", "verb", "Pohybovat se ve vodě pomocí těla.", "Chci plavat."),
            VocabularyEntry(
                "běhat",
                "verb",
                "Pohybovat se opakovaně rychleji než při chůzi.",
                "Ráno chci běhat.",
            ),
            VocabularyEntry("tančit", "verb", "Pohybovat tělem podle hudby.", "Chceme tančit."),
            VocabularyEntry(
                "poslouchat",
                "verb",
                "Věnovat pozornost zvukům nebo řeči.",
                "Poslouchám českou písničku.",
            ),
            VocabularyEntry(
                "dívat se",
                "verb",
                "Zaměřovat zrak na něco nebo něco sledovat.",
                "Dívám se na film.",
            ),
            VocabularyEntry(
                "učit se",
                "verb",
                "Získávat nové znalosti nebo dovednosti.",
                "Každý den se učím česky.",
            ),
            VocabularyEntry("chtít", "verb", "Mít přání něco získat nebo udělat.", "Chci číst."),
            VocabularyEntry(
                "moci", "verb", "Mít možnost nebo dovolení něco udělat.", "Můžu přijít v šest."
            ),
            VocabularyEntry(
                "muset", "verb", "Mít povinnost nebo nutnost něco udělat.", "Musím pracovat."
            ),
            VocabularyEntry(
                "schůzka", "noun", "Předem domluvené setkání.", "Schůzka je v pět hodin."
            ),
            VocabularyEntry(
                "zajímavý",
                "adjective",
                "Takový, který přitahuje pozornost.",
                "Čtu zajímavou knihu.",
            ),
            VocabularyEntry("spolu", "adverb", "Společně s někým dalším.", "Jdeme spolu do kina."),
        ],
    ),
    VocabularySet(
        "cs_health_help_a1",
        "A1",
        "Zdraví, potíže a pomoc",
        "a1-unit-7",
        [
            VocabularyEntry(
                "pomoc",
                "noun",
                "Podpora člověka, který má problém nebo něco nezvládá sám.",
                "Potřebuji pomoc.",
            ),
            VocabularyEntry(
                "problém", "noun", "Potíž, kterou je třeba vyřešit.", "Mám malý problém."
            ),
            VocabularyEntry(
                "lékař", "noun", "Muž, který vyšetřuje a léčí nemocné lidi.", "Lékař je tady."
            ),
            VocabularyEntry(
                "lékařka",
                "noun",
                "Žena, která vyšetřuje a léčí nemocné lidi.",
                "Naše lékařka je milá.",
            ),
            VocabularyEntry(
                "lék",
                "noun",
                "Přípravek určený k léčbě nemoci nebo zmírnění potíží.",
                "Potřebuji lék na bolest.",
            ),
            VocabularyEntry(
                "hlava", "noun", "Horní část těla s očima, ušima a ústy.", "Bolí mě hlava."
            ),
            VocabularyEntry(
                "ruka", "noun", "Horní končetina, kterou bereme věci.", "Bolí mě pravá ruka."
            ),
            VocabularyEntry(
                "noha", "noun", "Dolní končetina, kterou používáme při chůzi.", "Bolí mě levá noha."
            ),
            VocabularyEntry("břicho", "noun", "Přední část těla pod hrudníkem.", "Bolí mě břicho."),
            VocabularyEntry(
                "zub", "noun", "Tvrdá část v ústech, kterou koušeme jídlo.", "Bolí mě zub."
            ),
            VocabularyEntry("oko", "noun", "Část těla, kterou vidíme.", "Pravé oko je červené."),
            VocabularyEntry("ucho", "noun", "Část těla, kterou slyšíme.", "Bolí mě ucho."),
            VocabularyEntry(
                "bolest",
                "noun",
                "Nepříjemný tělesný pocit, například při úrazu.",
                "Bolest je silná.",
            ),
            VocabularyEntry(
                "teplota",
                "noun",
                "Údaj o tom, jak je něco teplé; u těla pomáhá poznat nemoc.",
                "Moje teplota je třicet osm stupňů.",
            ),
            VocabularyEntry(
                "nemocný",
                "adjective",
                "Takový, který má zdravotní potíže nebo nemoc.",
                "Petr je nemocný.",
            ),
            VocabularyEntry(
                "unavený",
                "adjective",
                "Takový, který má málo energie a potřebuje odpočinek.",
                "Jsem unavený a chci spát.",
            ),
            VocabularyEntry("hlad", "noun", "Pocit, že potřebujeme jíst.", "Mám hlad."),
            VocabularyEntry("žízeň", "noun", "Pocit, že potřebujeme pít.", "Mám žízeň."),
            VocabularyEntry(
                "potřebovat", "verb", "Nemoci se bez něčeho dobře obejít.", "Potřebuji vodu."
            ),
            VocabularyEntry("bolet", "verb", "Působit nepříjemný tělesný pocit.", "Bolí mě hlava."),
            VocabularyEntry(
                "čekat",
                "verb",
                "Zůstávat do chvíle, kdy někdo přijde nebo se něco stane.",
                "Čekám tady.",
            ),
            VocabularyEntry(
                "volat",
                "verb",
                "Spojovat se s někým telefonem nebo ho oslovovat hlasem.",
                "Volám lékaře.",
            ),
            VocabularyEntry(
                "zpráva",
                "noun",
                "Krátké sdělení poslané nebo předané jiné osobě.",
                "Píšu krátkou zprávu.",
            ),
            VocabularyEntry(
                "doklad",
                "noun",
                "Dokument, který potvrzuje například totožnost.",
                "Mám doklad totožnosti.",
            ),
            VocabularyEntry(
                "pas",
                "noun",
                "Úřední doklad totožnosti používaný při cestách do zahraničí.",
                "Kde je můj pas?",
            ),
            VocabularyEntry(
                "peněženka",
                "noun",
                "Malé pouzdro na peníze a platební karty.",
                "Moje peněženka je doma.",
            ),
            VocabularyEntry(
                "otevřeno",
                "adverb",
                "Stav, kdy obchod nebo služba přijímá zákazníky.",
                "Lékárna má otevřeno.",
            ),
            VocabularyEntry(
                "zavřeno",
                "adverb",
                "Stav, kdy obchod nebo služba nepřijímá zákazníky.",
                "Dnes je zavřeno.",
            ),
        ],
    ),
]
