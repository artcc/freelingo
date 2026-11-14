"""Czech C2 grammar and pragmatics for interpretation and flexible production."""

from app.data._types import GrammarExample, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "cs-register-shifts-c2",
        "Změna stylu bez změny sdělení",
        "C2",
        "Styl a komunikační situace",
        "Volte přirozený způsob vyjádření podle adresáta a zachovejte věcný obsah.",
        "Úřední věta „Žádáme vás o doplnění podkladů“ může v hovoru znít „Prosím, "
        "doplňte ještě podklady“. Změna stylu sama o sobě nemění žádost v doporučení. "
        "Obecněčeské nebo regionální podoby nejsou automaticky chybné; jejich vhodnost "
        "závisí na situaci. Při přechodu k formálnímu projevu upravujeme také oslovení, "
        "stavbu vět a míru přímosti, ne jen jednotlivé koncovky.",
        rules=[
            "Před úpravou určete, kdo žádá, kdo má jednat a zda jde o prosbu, pokyn či návrh.",
            "Nehodnoťte neformální podobu jako obecně nesprávnou jen kvůli jejímu registru.",
            "Zdvořilejší formulací nepřidávejte možnost odmítnout, pokud ji původní pokyn nedává.",
        ],
        examples=[
            GrammarExample(
                "O výsledku vás vyrozumíme písemně. — Výsledek vám pošleme písemně.",
                note="Druhá verze je méně úřední, ale zachovává odesílatele i způsob oznámení.",
            ),
            GrammarExample(
                "Hele, tohle bych zatím neposílal. — Doporučuji s odesláním zatím počkat.",
                note="Neformální a formálnější podoba stejného doporučení, nikoli zákazu.",
            ),
        ],
        related=["cs-cross-genre-reformulation-c2"],
    ),
    GrammarTopic(
        "cs-sentence-rhythm-c2",
        "Rytmus věty a informační důraz",
        "C2",
        "Slovosled a členění",
        "Řiďte tempo sdělení, aniž by zanikly vztahy mezi jeho částmi.",
        "Krátká věta může zvýraznit důsledek; souvětí může naopak držet podmínku "
        "těsně u závěru. V češtině bývá nové nebo kontrastní sdělení často na konci, "
        "ale mluvený důraz může toto rozložení změnit. Rozdělením souvětí nesmí "
        "z podmíněného závěru vzniknout nepodmíněné tvrzení. Vložky a pomlčky "
        "používejte tak, aby adresát udržel hlavní linii.",
        rules=[
            "Po rozdělení souvětí ponechte podmínku výslovně spojenou s jejím důsledkem.",
            "Pro neutrální psaný text nespoléhejte na důraz, který je slyšet pouze v řeči.",
        ],
        examples=[
            GrammarExample(
                "Začneme v pondělí, jen pokud dorazí souhlas. Bez něj nezačneme.",
                note="Krátké dovysvětlení zvýrazňuje podmínku, nikoli nový termín.",
            ),
            GrammarExample(
                "Podklady dodá Jana. Jana dodá podklady.",
                note="Bez zvláštní intonace první věta zvýrazňuje osobu, druhá předmět dodání.",
            ),
        ],
        related=["cs-focus-particles-c2"],
    ),
    GrammarTopic(
        "cs-nominal-compression-c2",
        "Rozvíjení zhuštěných jmenných formulací",
        "C2",
        "Jmenné a slovesné vyjadřování",
        "Zpřehledněte řetězce podstatných jmen bez domýšlení chybějícího původce.",
        "Výrazy jako „odmítnutí návrhu vedením“ zhušťují děj, předmět a původce. "
        "Instrumentál určuje původce; v minulém kontextu můžeme spojení rozvést "
        "jako „vedení odmítlo návrh“. Samotné "
        "„odmítnutí vedení“ však může znamenat, že vedení něco odmítlo, nebo že někdo "
        "odmítl vedení. Při převodu na slovesnou větu musí původce vyplývat z textu; "
        "není-li známý, zachovejte neosobní či pasivní vyjádření.",
        rules=[
            "Rozlišujte vlastníka, původce a předmět děje, i když mají stejný pádový tvar.",
            "Jmenná formulace sama neurčuje čas děje; převezměte jej z kontextu.",
        ],
        examples=[
            GrammarExample(
                "Po zamítnutí žádosti komisí se žadatel odvolal.",
                note="Komise žádost zamítla; žadatel podal odvolání.",
            ),
            GrammarExample(
                "Došlo ke zrušení schůzky. — Schůzka byla zrušena.",
                note="Ani jedna verze neurčuje, kdo schůzku zrušil.",
            ),
        ],
        related=["cs-attachment-ambiguity-c2", "cs-reference-resolution-c2"],
    ),
    GrammarTopic(
        "cs-ironic-echo-c2",
        "Ironická ozvěna a odstup",
        "C2",
        "Pragmatika a intonace",
        "Rozpoznejte, kdy mluvčí opakuje cizí hodnocení, aby se od něj distancoval.",
        "Po třetím výpadku může věta „Tak to je opravdu spolehlivá služba“ obracet "
        "kladné hodnocení proti předchozímu slibu. Ironii podporuje rozpor se situací, "
        "intonace nebo známé očekávání; slovo „opravdu“ ji samo nekóduje. Uvozovky "
        "mohou vyjadřovat odstup, citaci i označení pojmu. Pokud záměr není jasný, "
        "ověřte jej místo automatického připsání výsměchu.",
        rules=[
            "Oddělte doslovné znění od hodnocení, které v dané situaci naznačuje.",
            "Při opravě nepovedené ironie uznejte účinek výroku a vysvětlete jeho cíl.",
        ],
        examples=[
            GrammarExample(
                "„Bez čekání,“ říkali. Už tu sedíme hodinu.",
                note="Opakovaný slib je konfrontován se zkušeností.",
            ),
            GrammarExample(
                "To byla narážka na ten systém, ne na tebe. Mrzí mě, že to vyznělo osobně.",
                note="Oprava určuje terč poznámky a nezpochybňuje reakci adresáta.",
            ),
        ],
        related=["cs-understatement-c2", "cs-ellipsis-and-repair-c2"],
    ),
    GrammarTopic(
        "cs-cancellable-implicature-c2",
        "Náznak, který lze odvolat",
        "C2",
        "Význam v rozhovoru",
        "Nezaměňujte pravděpodobný závěr posluchače za výslovný obsah.",
        "Věta „Někteří už odpověděli“ často naznačuje, že neodpověděli všichni. "
        "Pokračování „možná už všichni, ještě jsem to nespočítal“ však tuto hranici "
        "ruší bez nutného rozporu. Také zmínka o pracovním vytížení může v reakci "
        "na pozvání naznačit odmítnutí, ale následující replika může výklad změnit. "
        "Takový kontextový náznak označujeme jako konverzační implikaturu. "
        "Nejde o logický důsledek, který by byl nutně pravdivý spolu s původní větou. "
        "Při výkladu se opírejte o celé vyjádření.",
        rules=[
            "Zkuste, zda lze náznak zrušit dodatkem bez popření původního tvrzení.",
            "Při zápisu jednání neproměňujte nepřímý signál v potvrzené rozhodnutí.",
        ],
        examples=[
            GrammarExample(
                "Někteří už návrh četli, možná dokonce všichni; seznam zatím nemám.",
                note="Mluvčí nepotvrzuje úplnost skupiny, ale ani ji nevylučuje.",
            ),
            GrammarExample(
                "Zítra mám dost práce, ale na oběd s tebou si čas udělám.",
                note="Druhá část blokuje očekávané odmítnutí pozvání.",
            ),
        ],
        related=["cs-ironic-echo-c2", "cs-commitment-scope-c2"],
    ),
    GrammarTopic(
        "cs-presupposition-repair-c2",
        "Jak odpovědět bez přijetí skrytého předpokladu",
        "C2",
        "Předpoklady otázek",
        "Otevřete k diskusi i to, co otázka předkládá jako již známé.",
        "Otázka „Proč jste zase změnili podmínky?“ představuje změnu jako opakovanou. "
        "Pouhé vysvětlení důvodu může vyznít jako přijetí této historie. Jestliže "
        "je sporná, nejprve určete, kterou změnu uznáváte a kterou ne. Výrazy "
        "„zase“, „ještě“ nebo „přestat“ mají různé funkce; jejich předpoklady vždy "
        "posuzujte v konkrétní větě, ne mechanicky.",
        rules=[
            "Odlište spor o událost od sporu o její příčinu nebo opakování.",
            "Po opravě předpokladu nabídněte odpověď na věcně upravenou otázku.",
        ],
        examples=[
            GrammarExample(
                "Nejde o další změnu; předchozí text byl návrh. "
                "Vysvětlím, co obsahuje schválená verze.",
            ),
            GrammarExample(
                "Když říkáte, že jsme přestali odpovídat, o které nevyřízené zprávy jde?",
            ),
        ],
        related=["cs-metalinguistic-negation-c2"],
    ),
    GrammarTopic(
        "cs-metalinguistic-negation-c2",
        "Ne popření faktu, ale oprava označení",
        "C2",
        "Zápor a hodnocení",
        "Rozlišujte, zda zápor odmítá událost, pojmenování, nebo příliš slabé hodnocení.",
        "Věta „To není sleva, ale odklad platby“ nepopírá změnu platebních podmínek; "
        "odmítá její zařazení mezi slevy. Věta „Nebyl dobrý, byl výborný“ může "
        "odmítat nedostatečně silné hodnocení, ne kvalitu výkonu. Rozhodující je "
        "opravující pokračování a v řeči také důraz. Samostatné „nebyl dobrý“ "
        "má bez takového kontextu jiný běžný výklad.",
        rules=[
            "Před interpretací záporu přečtěte i následující opravu.",
            "Uveďte náhradní pojmenování, chcete-li předejít dojmu, že odmítáte celý popis.",
        ],
        examples=[
            GrammarExample(
                "Neodmítám spolupráci; odmítám, aby se její náklady přenesly jen na nás."
            ),
            GrammarExample("To nebylo drobné zdržení, ale celodenní výpadek."),
        ],
        related=["cs-presupposition-repair-c2", "cs-understatement-c2"],
    ),
    GrammarTopic(
        "cs-attachment-ambiguity-c2",
        "Dvojí vazba a více možných čtení",
        "C2",
        "Větné vztahy",
        "Zjistěte, ke které části věty se může vztahovat sporné určení.",
        "Ve větě „Pozoroval souseda s dalekohledem“ může dalekohled patřit "
        "k popisu souseda nebo k vybavení pozorovatele při činnosti. Pravděpodobnost "
        "výkladu závisí na situaci, ale sama nenahrazuje jasnou formulaci. Také "
        "rozsah přívlastku u několika souřadných jmen může být nejasný. Při úpravě "
        "opakujte přívlastek nebo rozdělte větu, pokud by jeho dosah zůstal sporný.",
        rules=[
            "Před redakcí vypište možné vztahy mezi členy; nevolte jeden jen podle blízkosti.",
            "Upřesnění musí odpovídat doloženému záměru, ne pouze pravděpodobnému scénáři.",
        ],
        examples=[
            GrammarExample(
                "Pozoroval souseda, který měl u sebe dalekohled.",
                note="Tato verze odpovídá výkladu, že dalekohled měl soused. "
                "Bez kontextu nelze z původní věty vybrat právě tento výklad.",
            ),
            GrammarExample(
                "Dalekohledem pozoroval souseda.",
                note="Tato verze výslovně označuje dalekohled za nástroj pozorování.",
            ),
            GrammarExample(
                "Hledáme zkušené překladatele a zkušené redaktory.",
                note="Opakování výslovně vztahuje požadavek zkušenosti k oběma skupinám.",
            ),
        ],
        related=["cs-nominal-compression-c2", "cs-reference-resolution-c2"],
    ),
    GrammarTopic(
        "cs-reference-resolution-c2",
        "Zájmena, vlastnictví a odpovědnost",
        "C2",
        "Odkazování v textu",
        "Odstraňte nejasné odkazy bez záměny účastníků.",
        "Zvratné „svůj“ se v běžné větě s určitým slovesným tvarem vztahuje k podmětu: "
        "„Petra předala Janě svůj návrh“ označuje Petřin návrh. „Její návrh“ "
        "vyžaduje kontext a nemusí odkazovat právě k nejbližšímu ženskému jménu. "
        "V souvětích a infinitivních konstrukcích může být určení perspektivy "
        "náročnější. V dokumentu, kde záleží na vlastnictví nebo odpovědnosti, "
        "je opakování jména často vhodnější než elegantní, ale nejasné zájmeno.",
        rules=[
            "Při nahrazení zájmena jménem zachovejte roli vlastníka i původce děje.",
            "Není-li odkaz doložený, označte nejasnost a vyžádejte si upřesnění.",
        ],
        examples=[
            GrammarExample(
                "Petra předala Janě svůj návrh. — Petra předala Janě Petřin návrh.",
                note="Výslovné jméno zachovává přivlastnění; samo neupřesňuje vznik návrhu.",
            ),
            GrammarExample(
                "Jana řekla Petře, že Petr její žádost doplní. Čí žádost má Petr doplnit?",
                note="Samotná věta neřeší jednoznačně odkaz přivlastňovacího zájmena.",
            ),
        ],
        related=["cs-attachment-ambiguity-c2", "cs-cross-genre-reformulation-c2"],
    ),
    GrammarTopic(
        "cs-nested-conditions-c2",
        "Podmíněná výjimka z pravidla",
        "C2",
        "Podmínkové vztahy",
        "Udržte hlavní pravidlo, výjimku i podmínku výjimky oddělené.",
        "V ustanovení „Po desáté je provoz zakázán; výjimku mají uzavřené akce, "
        "pokud je předem schválí správce“ nestačí, že jde o uzavřenou akci. "
        "Je nutné i předchozí schválení. Výrazy „ledaže“, „pokud ovšem“ a "
        "„s výjimkou“ mohou měnit dosah pravidla; nesmějí při zjednodušování "
        "zmizet. Výjimka z časového omezení sama neruší jiné povinnosti.",
        rules=[
            "Ověřte, které podmínky platí současně a které jsou alternativní.",
            "Výjimku vztahujte jen k tomu požadavku, z něhož byla udělena.",
        ],
        examples=[
            GrammarExample(
                "Registrace je nutná i pro členy; poplatek však neplatí, "
                "pokud mají uhrazené příspěvky.",
            ),
            GrammarExample(
                "Lhůtu lze prodloužit jen se souhlasem správce, a to nejvýše o týden.",
                note="Souhlas neumožňuje překročit uvedenou horní hranici.",
            ),
        ],
        related=["cs-commitment-scope-c2", "cs-focus-particles-c2"],
    ),
    GrammarTopic(
        "cs-commitment-scope-c2",
        "Příslib jednání není příslib výsledku",
        "C2",
        "Modalita a závaznost",
        "Přesně určete, k jakému kroku se mluvčí zavazuje.",
        "„Prověříme, zda můžeme termín posunout“ slibuje prověření, nikoli posun. "
        "„Posuneme termín, pokud získáme souhlas“ naopak vyslovuje podmíněný závazek. "
        "Také „mohu slíbit, že se pokusím“ omezuje příslib na pokus. V rychlém "
        "jednání zopakujte rozsah dohody, protože zdvořilá ochota může být mylně "
        "přijata jako souhlas s požadovaným výsledkem.",
        rules=[
            "Najděte sloveso, jehož děj je skutečně přislíben, a zachovejte jeho doplnění.",
            "Při shrnutí nerozšiřujte závazek jedné osoby na celý tým nebo instituci.",
        ],
        examples=[
            GrammarExample("Zavazuji se návrh předložit, ne zajistit jeho schválení."),
            GrammarExample(
                "Slevu mohu doporučit. Potvrdit ji ale musí vedoucí.",
                note="Mluvčí odděluje své oprávnění od rozhodovací pravomoci jiné osoby.",
            ),
        ],
        related=["cs-nested-conditions-c2", "cs-cross-genre-reformulation-c2"],
    ),
    GrammarTopic(
        "cs-focus-particles-c2",
        "Jen, i a právě: co je omezeno nebo zdůrazněno",
        "C2",
        "Částice a dosah",
        "Vymezte, k čemu se vztahuje omezení nebo kontrast.",
        "„Jen Jana může návrh stáhnout“ omezuje okruh oprávněných osob. "
        "„Jana může návrh jen stáhnout“ v odpovídajícím kontextu omezuje dostupné "
        "úkony. Intonace může dosah částice ovlivnit, proto v písemné dohodě "
        "použijte výslovné dovysvětlení. Výraz „i“ přidává prvek k předpokládaným "
        "alternativám; „právě“ může zdůraznit přesnou totožnost i aktuální čas.",
        rules=[
            "Umístěte částici k zamýšlenému členu a v citlivém textu její dosah ověřte parafrází.",
            "Přesunutí částice nepovažujte za čistě stylistickou úpravu.",
        ],
        examples=[
            GrammarExample("Jen Jana může návrh stáhnout; ostatní k tomu oprávnění nemají."),
            GrammarExample("Jana může návrh jen stáhnout; měnit ho už nesmí."),
        ],
        related=["cs-sentence-rhythm-c2", "cs-commitment-scope-c2"],
    ),
    GrammarTopic(
        "cs-represented-voice-c2",
        "Kdo hodnotí v polopřímé řeči",
        "C2",
        "Perspektiva a vyprávění",
        "Rozpoznejte přechod k perspektivě postavy i bez uvozovací věty.",
        "Vyprávění ve třetí osobě může převzít otázky, slovník a hodnocení postavy "
        "bez přímé citace: „Eva otevřela dopis. Tak tohle měla být ta velkorysá "
        "nabídka?“ Otázka v kontextu zpřístupňuje Evinu reakci; není automaticky "
        "ověřeným soudem vypravěče. Polopřímou řeč je užitečné rozpoznávat "
        "v próze i publicistickém vyprávění. Při věcném shrnutí perspektivu "
        "označte, místo abyste její hodnocení vydávali za vlastní závěr.",
        rules=[
            "Přiřaďte hodnocení podle okolního děje a slovníku, ne jen podle třetí osoby.",
            "V neutrálním shrnutí oddělte popsanou událost od reakce postavy.",
        ],
        examples=[
            GrammarExample(
                "Pavel se podíval na účet. A za tohle měl ještě děkovat?",
                note="Otázka v daném vyprávění zachycuje Pavlovo rozhořčení.",
            ),
            GrammarExample(
                "Eva pochybovala o velkorysosti nabídky.",
                note="Parafráze otázky z výkladu zachovává nositelku pochybnosti. "
                "Nepřidává konkrétní důvod, proč nabídku zpochybnila.",
            ),
        ],
        related=["cs-ironic-echo-c2", "cs-cross-genre-reformulation-c2"],
    ),
    GrammarTopic(
        "cs-understatement-c2",
        "Zdrženlivé hodnocení a litotes",
        "C2",
        "Styl a hodnotící výrazy",
        "Odhadněte sílu hodnocení bez mechanického převracení záporu.",
        "„Není to bez rizika“ upozorňuje na přítomnost rizika, neurčuje však jeho "
        "velikost. „To nebylo zrovna šťastné“ může podle situace tlumit výraznou "
        "kritiku. Litotes využívá například zápor protikladného výrazu; konkrétní "
        "účinek závisí na kontextu a intonaci. Zdrženlivost může vyjadřovat takt, "
        "ironii i skutečně mírný soud. Nepřepisujte ji automaticky jako nadšení "
        "nebo jednoznačné odsouzení.",
        rules=[
            "Rozlišujte výslovně vyjádřené minimum od silnějšího kontextového náznaku.",
            "Při převodu do věcné zprávy zachovejte neurčenou míru hodnocení.",
        ],
        examples=[
            GrammarExample(
                "Návrh není bez předností, ale k přijetí má zatím daleko.",
                note="Uznání předností není doporučením návrh přijmout.",
            ),
            GrammarExample(
                "Po dvou hodinách v dešti jsme nebyli zrovna nadšení.",
                note="Kontext podporuje silnější nespokojenost, než naznačuje mírná formulace.",
            ),
            GrammarExample(
                "Když jsem zjistila, že jsem čekala u jiného vchodu, nebyla jsem na sebe "
                "zrovna pyšná. Teď už se tomu směju.",
                note="Osobní vyprávění spojuje tlumenou sebekritiku s pozdějším odstupem.",
            ),
        ],
        related=["cs-metalinguistic-negation-c2", "cs-ironic-echo-c2"],
    ),
    GrammarTopic(
        "cs-ellipsis-and-repair-c2",
        "Výpustka a průběžná oprava repliky",
        "C2",
        "Stavba rozhovoru",
        "Doplňujte nevyřčené členy a opravujte se bez změny dohodnutého obsahu.",
        "V replice „Já připravím zápis, ty podklady“ se druhé sloveso doplňuje "
        "z první části. Výpustka je přirozená, pokud vztahy zůstávají jasné. "
        "Opravné výrazy „vlastně“, „přesněji“ nebo „tedy“ mohou nahradit jeden "
        "člen, ale také změnit celý závazek. Posluchač musí poznat, co z původní "
        "verze zůstává v platnosti. U citlivé dohody je vhodné opravu zopakovat celou.",
        rules=[
            "Při doplnění výpustky zachovejte osobu, modalitu i čas z příslušné části.",
            "Opravu formulujte jako vlastní upřesnění, ne jako výtku posluchači.",
        ],
        examples=[
            GrammarExample(
                "Já mohu zkontrolovat rozpočet a Jana zase harmonogram.",
                note="Druhá část vyjadřuje Janinu možnost kontroly, sama nepotvrzuje její souhlas.",
            ),
            GrammarExample(
                "Pošlu vám výsledek zítra — přesněji, zítra vám potvrdím, kdy bude hotový.",
                note="Oprava zužuje původní příslib; je třeba ji při shrnutí zachovat.",
            ),
        ],
        related=["cs-commitment-scope-c2", "cs-reference-resolution-c2"],
    ),
    GrammarTopic(
        "cs-cross-genre-reformulation-c2",
        "Věrná přeformulace mezi žánry",
        "C2",
        "Redakce a zprostředkování",
        "Měňte formu sdělení, nikoli účastníky, podmínky nebo sílu závazku.",
        "Při převodu rozhovoru do zápisu obvykle vypustíme váhání a opakování. "
        "Výhrada, podmínka nebo omezení pravomoci však není pouhá slovní vata. "
        "„Zkusím to s účetní probrat“ nelze zapsat jako „účetní věc vyřeší“. "
        "Před převodem si určete původce, zamýšlený krok, míru závazku a čas. "
        "Ve zprávě pro veřejnost můžete nahradit odborné výrazy vysvětlením, "
        "ale nevyřešené otázky musí zůstat otevřené.",
        rules=[
            "Každý závazek připisujte pouze osobě nebo instituci, která jej skutečně přijala.",
            "Ponechte rozdíl mezi návrhem, pokusem, rozhodnutím a uskutečněným krokem.",
            "Při zkrácení zachovejte výhrady ovlivňující praktický důsledek.",
        ],
        examples=[
            GrammarExample(
                "Vedoucí Jan: „Proberu to s účetní.“ — Jan přislíbil konzultaci s účetní.",
                note="Zápis nepřipisuje účetní souhlas ani povinnost věc vyřešit.",
            ),
            GrammarExample(
                "Zkušební provoz se doporučuje, není však podmínkou schválení. "
                "— Vyzkoušet si provoz je vhodné, ale ke schválení to není nutné.",
                note="Srozumitelnější verze zachovává rozdíl mezi doporučením a požadavkem.",
            ),
        ],
        related=["cs-register-shifts-c2", "cs-commitment-scope-c2", "cs-ellipsis-and-repair-c2"],
    ),
]
