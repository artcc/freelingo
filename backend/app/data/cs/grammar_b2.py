"""Czech B2 grammar for information structure, register and practical discourse."""

from app.data._types import GrammarExample, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "cs-information-structure-b2",
        "Známá informace a jádro sdělení",
        "B2",
        "Slovosled a význam",
        "Uspořádejte větu podle toho, na co odpovídáte a co chcete zdůraznit.",
        "V neutrálním sdělení často postupujeme od známého k novému. Věta "
        "Smlouvu připravila Jana odpovídá přirozeně na otázku, kdo ji připravil. "
        "Jana připravila smlouvu může odpovídat na otázku, co Jana udělala. "
        "Slovosled však není mechanická šablona: v řeči význam dotváří přízvuk "
        "a kontext. Při opravě nedorozumění lze kontrastní člen zdůraznit i na začátku.",
        rules=[
            "Před přeformulováním určete, která informace je pro posluchače nová.",
            "Změnou slovosledu neměňte role účastníků; ty pomáhají vyjadřovat pády.",
        ],
        examples=[
            GrammarExample(
                "Podklady poslala účetní.",
                note="Odpověď na otázku: Kdo poslal podklady?",
            ),
            GrammarExample(
                "Termín jsem kritizoval, ne cenu.",
                note="Mluvčí opravuje, čeho se jeho kritika týkala.",
            ),
        ],
        related=["cs-clitic-order-b2", "cs-focus-particles-b2"],
    ),
    GrammarTopic(
        "cs-clitic-order-b2",
        "Příklonky za prvním větným úsekem",
        "B2",
        "Slovosled",
        "Spojujte nepřízvučné tvary do přirozené skupiny.",
        "Příklonky jako jsem, bych, se, si, mi nebo ho se v neutrální větě "
        "řadí za první přízvučný větný úsek, nikoli nutně za první slovo. "
        "V běžných skupinách stojí pomocný nebo podmiňovací tvar před se či si "
        "a nepřízvučný třetí pád před čtvrtým: Včera jsem mu ho poslal. "
        "Vlastní vedlejší věta má své uspořádání: Vím, že se mu to nelíbí.",
        rules=[
            "Delší úvodní člen nerozdělujte jen proto, abyste příklonku dali za první slovo.",
            "Po předložce nebo při důrazu užijte plný tvar: pro mě, právě jemu.",
            "Ve spisovném vyjádření užívejte například chtěl by sis a mohl by ses.",
        ],
        examples=[
            GrammarExample("Po dnešní poradě jsem mu to vysvětlila."),
            GrammarExample("Chtěl by sis tu nabídku ještě promyslet?"),
            GrammarExample("Řekla, že se mu ozve zítra."),
        ],
        related=["cs-information-structure-b2"],
    ),
    GrammarTopic(
        "cs-negation-scope-b2",
        "Ne všichni, nikdo a ne nutně",
        "B2",
        "Zápor a význam",
        "Rozlišujte popření celku, části a nutného závěru.",
        "Ne všichni souhlasili popírá souhlas celé skupiny, ale samo neurčuje počet "
        "nesouhlasících. Nikdo nesouhlasil popírá souhlas u každého jejího člena. "
        "Česká záporná zájmena se běžně pojí se záporným slovesem: Nikdo nic "
        "nenamítal. Spojení ne nutně nebo nemusí vyjadřuje, že závěr není nezbytný; "
        "neznamená automaticky jeho opak.",
        rules=[
            "Pro jednoznačnost nahraďte nejasné Všichni nepřišli výrazem "
            "Ne všichni přišli nebo Nikdo nepřišel.",
            "Odlišujte Nemusíte přijít, tedy není to povinné, "
            "od Nesmíte přijít, tedy je to zakázané.",
        ],
        examples=[
            GrammarExample("Ne všichni odpověděli; na tři odpovědi ještě čekáme."),
            GrammarExample("Vyšší cena nemusí znamenat lepší kvalitu."),
            GrammarExample("Nikdo proti návrhu nic nenamítal."),
        ],
        related=["cs-focus-particles-b2", "cs-conditional-limits-b2"],
    ),
    GrammarTopic(
        "cs-periphrastic-passive-b2",
        "Opisné trpné tvary a původce děje",
        "B2",
        "Slovesný rod",
        "Popište děj z pohledu osoby nebo věci, které se týká.",
        "Opisný trpný rod tvoří sloveso být a trpné příčestí: Žádost byla schválena. "
        "Příčestí se shoduje s podmětem: dokument byl podepsán, smlouvy byly "
        "podepsány. Původce může být vyjádřen sedmým pádem, ale často chybí. "
        "Při převodu do činného rodu ho doplňte pouze tehdy, pokud ho znáte. "
        "Vid pomáhá odlišit průběh a dokončení: byl projednáván oproti byl projednán.",
        rules=[
            "Předmět činné věty se při běžném převodu stává podmětem trpné věty.",
            "Nevyvozujte z nevyjádřeného původce, že je neznámý nebo že není důležitý.",
        ],
        examples=[
            GrammarExample("Návrh byl schválen zastupitelstvem."),
            GrammarExample("Přihlášky budou posouzeny do konce měsíce."),
            GrammarExample("Smlouva byla projednávána celé dopoledne."),
        ],
        related=["cs-reflexive-passive-b2", "cs-result-state-b2"],
    ),
    GrammarTopic(
        "cs-reflexive-passive-b2",
        "Zvratné pasivum a neosobní vyjádření",
        "B2",
        "Slovesný rod",
        "Vyjadřujte běžné postupy, aniž musíte jmenovat jejich vykonavatele.",
        "Věty Žádosti se podávají elektronicky a Vstupenky se prodávají u vchodu "
        "staví do popředí postup. Sloveso se shoduje s podmětem: žádost se podává, "
        "žádosti se podávají. Ne každé se však označuje pasivum: Jana se myje "
        "může znamenat, že myje sama sebe. Neosobní V kanceláři se nekouří "
        "nemá pojmenovaný podmět a sloveso zůstává ve třetí osobě jednotného čísla.",
        rules=[
            "Zvratné pasivum je běžné v návodech a obecných pravidlech.",
            "Při potřebě určit odpovědnost raději jmenujte původce v činné větě.",
        ],
        examples=[
            GrammarExample("Reklamace se vyřizují do třiceti dnů."),
            GrammarExample("O víkendu se v této budově nepracuje."),
            GrammarExample("Přihláška se podává prostřednictvím formuláře."),
        ],
        related=["cs-periphrastic-passive-b2", "cs-clitic-order-b2"],
    ),
    GrammarTopic(
        "cs-result-state-b2",
        "Děj, stav a hotový výsledek",
        "B2",
        "Sloveso a přídavné jméno",
        "Odlište zprávu o události od popisu současného výsledku.",
        "Krátké příčestí často zdůrazňuje děj: Dveře byly v osm hodin zamčeny. "
        "Dlouhý přídavný tvar často popisuje stav: Dveře jsou zamčené. "
        "Hranice není vždy ostrá; Dveře jsou zavřeny může také označovat stav, "
        "zvlášť ve formálním oznámení. Konstrukce mít hotovo nebo mít něco "
        "připravené zdůrazňuje dosažený výsledek, nefunguje jako obecný minulý čas.",
        rules=[
            "Význam určujte také podle časového údaje a situace, ne jen podle koncovky.",
            "Ve spojení mít něco připravené se přídavné jméno shoduje s předmětem.",
        ],
        examples=[
            GrammarExample("Zpráva byla odeslána v poledne."),
            GrammarExample("Mám připravené všechny podklady, můžeme začít."),
            GrammarExample("Kancelář je zavřená, ale nevíme, kdy ji zavřeli."),
        ],
        related=["cs-periphrastic-passive-b2"],
    ),
    GrammarTopic(
        "cs-reported-speech-b2",
        "Nepřímá řeč a časová perspektiva",
        "B2",
        "Předávání informací",
        "Předávejte cizí výpověď bez změny účastníků a časových vztahů.",
        "Oznamovací výpověď obvykle uvádíme pomocí že. Čeština nevyžaduje "
        "automatický posun slovesného času po minulém slovese: Jana řekla, "
        "že přijde. Zájmena a výrazy dnes, zítra nebo tady přizpůsobujeme tomu, "
        "kdy, kde a komu výrok předáváme. Změna musí zachovat původní časový "
        "vztah, nikoli jen mechanicky nahradit jednotlivá slova.",
        rules=[
            "U časově vzdálené zprávy použijte konkrétní datum nebo například následující den.",
            "Rozlišujte slíbil, předpokládal a potvrdil; tato slovesa nevyjadřují stejný závazek.",
        ],
        examples=[
            GrammarExample(
                "V pondělí Jana řekla, že přijde v úterý.",
                note="Původní pondělní výrok: Přijdu zítra.",
            ),
            GrammarExample("Petr mi řekl, že si s sebou vezme vlastní notebook."),
        ],
        related=["cs-reported-questions-b2", "cs-evidentiality-b2"],
    ),
    GrammarTopic(
        "cs-reported-questions-b2",
        "Nepřímé otázky a předané žádosti",
        "B2",
        "Předávání informací",
        "Převádějte otázky a pokyny tak, aby zůstalo jasné, kdo má jednat.",
        "Zjišťovací otázku předáme pomocí zda nebo jestli: Ptala se, zda přijdu. "
        "U doplňovací otázky zachováme tázací slovo: Ptala se, kdy přijdu. "
        "Předaná otázka nemá povinný zvláštní slovosled. Žádost lze vyjádřit "
        "větou s aby: Požádala mě, abych počkal. Tvary abych, abys, abychom "
        "a abyste vyjadřují osobu, která má zamýšlený děj vykonat.",
        rules=[
            "Zda i jestli jsou spisovné; zda bývá častější ve formálním textu.",
            "Za oznamovací hlavní větou s nepřímou otázkou pište tečku: Nevím, kdy přijde.",
        ],
        examples=[
            GrammarExample("Vedoucí se zeptala, jestli máme všechny přílohy."),
            GrammarExample("Klient nás požádal, abychom mu zaslali podrobný rozpočet."),
            GrammarExample("Zajímalo ji, kdo bude mít projekt na starosti."),
        ],
        related=["cs-reported-speech-b2", "cs-infinitive-control-b2"],
    ),
    GrammarTopic(
        "cs-evidentiality-b2",
        "Prý, údajně, zřejmě a podle někoho",
        "B2",
        "Zdroj a jistota",
        "Oddělujte převzatou informaci od vlastního úsudku.",
        "Prý a údajně představují informaci jako převzatou; samy nedokazují, "
        "že je pravdivá ani nepravdivá. Podle vedení výslovně označuje zdroj. "
        "Zřejmě nebo patrně často vyjadřuje úsudek mluvčího na základě dostupných "
        "znaků. Jejich síla závisí na kontextu. Při shrnutí zprávy zachovejte "
        "také její nejistotu a neproměňujte odhad v potvrzený fakt.",
        rules=[
            "Je-li zdroj známý a podstatný, pojmenujte ho místo neurčitého prý.",
            "Slovo údajně může vyjadřovat odstup; nemusí znamenat obvinění ze lži.",
        ],
        examples=[
            GrammarExample("Podle správce bude výtah opraven ve čtvrtek."),
            GrammarExample("V kanceláři se nesvítí; kolegové už zřejmě odešli."),
            GrammarExample("Soused prý prodává byt, ale přímo jsem se ho neptala."),
        ],
        related=["cs-reported-speech-b2", "cs-particles-b2"],
    ),
    GrammarTopic(
        "cs-concession-b2",
        "Přestože, i když a navzdory",
        "B2",
        "Vztahy mezi větami",
        "Uznávejte překážku, která nezabránila výsledku.",
        "Přípustka spojuje skutečnost s výsledkem, který by se na jejím základě "
        "nemusel očekávat: Přestože pršelo, vyrazili jsme. Ačkoli má podobný "
        "význam a bývá knižnější. I když může označovat skutečnou okolnost "
        "i hypotetickou možnost, podle kontextu. Navzdory se pojí se třetím "
        "pádem: navzdory potížím. Ani jedna konstrukce sama nepředstavuje příčinu.",
        rules=[
            "Po spojce přestože následuje věta; po předložce navzdory jmenný výraz.",
            "Při námitce uznejte konkrétní skutečnost a potom vysvětlete své stanovisko.",
        ],
        examples=[
            GrammarExample("Přestože je nabídka dražší, zahrnuje i pravidelný servis."),
            GrammarExample("Navzdory opakovaným žádostem jsme odpověď nedostali."),
            GrammarExample("I když bude pršet, koncert se uskuteční v sále."),
        ],
        related=["cs-contrast-b2"],
    ),
    GrammarTopic(
        "cs-contrast-b2",
        "Zatímco, kdežto a sice, ale",
        "B2",
        "Vztahy mezi větami",
        "Porovnávejte odlišné možnosti a vyvažujte hodnocení.",
        "Zatímco může vyjadřovat současnost nebo kontrast: Zatímco Jana vařila, "
        "Petr uklízel; Jedna nabídka je levná, zatímco druhá zahrnuje servis. "
        "Kdežto zdůrazňuje kontrast. Dvojice sice, ale uznává jednu stránku "
        "a přidává omezení: Byt je sice malý, ale má nízké náklady. "
        "Porovnávané informace mají být věcně srovnatelné.",
        rules=[
            "Rozhodněte podle kontextu, zda zatímco popisuje čas, nebo rozdíl.",
            "Po sice obvykle doplňte protiklad, například ale, avšak nebo zato.",
        ],
        examples=[
            GrammarExample("První návrh šetří čas, kdežto druhý snižuje náklady."),
            GrammarExample("Termín je sice napjatý, ale ještě ho můžeme dodržet."),
        ],
        related=["cs-concession-b2", "cs-correlative-b2"],
    ),
    GrammarTopic(
        "cs-correlative-b2",
        "Nejen, ale i; čím, tím",
        "B2",
        "Souvztažná spojení",
        "Spojujte rovnocenné informace a popisujte závislost změn.",
        "Nejen, ale i přidává další významnou informaci: Návrh nejen šetří čas, "
        "ale i snižuje náklady. Spojujte stejnorodé větné členy nebo celé věty. "
        "Konstrukce čím, tím s druhým stupněm vyjadřuje závislost: Čím dřív "
        "začneme, tím lépe. Samotná tato konstrukce ještě nedokazuje, že je "
        "popsaná souvislost ve skutečnosti příčinná.",
        rules=[
            "Před ale v dvojici nejen, ale i pište čárku.",
            "U konstrukce čím, tím vyjádřete srozumitelně oba srovnávané jevy.",
        ],
        examples=[
            GrammarExample("Kurz je určen nejen zaměstnancům, ale i dobrovolníkům."),
            GrammarExample("Čím déle budeme čekat, tím méně možností nám zbude."),
        ],
        related=["cs-contrast-b2"],
    ),
    GrammarTopic(
        "cs-nominalisation-b2",
        "Jmenné vyjádření a srozumitelnost",
        "B2",
        "Pracovní a úřední text",
        "Zkracujte text, ale zachovávejte jasné účastníky a děje.",
        "Podstatná jména slovesná, například schválení nebo předání, umožňují "
        "hutné vyjádření: po schválení žádosti. Řetězce druhých pádů však "
        "mohou zamlžit, kdo jedná. Spojení kontrola dodavatele může podle "
        "kontextu označovat kontrolu prováděnou dodavatelem i kontrolu dodavatele "
        "jinou osobou. Při přeformulování do věty doplňujte pouze známé účastníky.",
        rules=[
            "Pro pokyny bývá jasnější určité sloveso: "
            "Pošlete potvrzení místo Proveďte zaslání potvrzení.",
            "Při převodu zachovejte časový vztah: po schválení není před schválením.",
        ],
        examples=[
            GrammarExample(
                "Po schválení žádosti vám zašleme rozhodnutí.",
                note="Stejný časový vztah: Až bude žádost schválena, zašleme vám rozhodnutí.",
            ),
            GrammarExample("Dodavatel zkontroluje zařízení a pošle nám zprávu."),
        ],
        related=["cs-periphrastic-passive-b2", "cs-reference-cohesion-b2"],
    ),
    GrammarTopic(
        "cs-infinitive-control-b2",
        "Kdo má vykonat děj infinitivu?",
        "B2",
        "Slovesné vazby",
        "Odlišujte vlastní závazek od úkolu předaného někomu jinému.",
        "Ve větě Jana slíbila Petrovi zavolat je vykonavatelkou telefonátu Jana. "
        "Ve větě Jana dovolila Petrovi odejít má odejít Petr. O vztahu rozhoduje "
        "význam řídícího slovesa, ne pouze blízkost jména k infinitivu. "
        "Pokud by delší text byl nejasný, použijte vedlejší větu s výslovně "
        "určeným podmětem nebo jednoznačným tvarem slovesa.",
        rules=[
            "U sloves slíbit a rozhodnout se obvykle jedná podmět hlavní věty.",
            "U dovolit nebo doporučit může být vykonavatelem osoba ve třetím pádě.",
        ],
        examples=[
            GrammarExample("Vedoucí slíbila kolegovi poslat upravenou smlouvu."),
            GrammarExample("Lékař doporučil pacientovi omezit pracovní zátěž."),
            GrammarExample("Vedoucí požádala kolegu, aby upravenou smlouvu poslal on."),
        ],
        related=["cs-reported-questions-b2"],
    ),
    GrammarTopic(
        "cs-conditional-limits-b2",
        "Jen pokud, pokud ne a za předpokladu, že",
        "B2",
        "Podmínky a dohody",
        "Vymezujte požadavky a výjimky bez nechtěných příslibů.",
        "Jen pokud označuje nezbytnou podmínku, ale nemusí zaručovat výsledek: "
        "O podporu lze žádat jen tehdy, pokud máte trvalý pobyt v obci. Mohou platit "
        "i další požadavky. Pokud nepřijde námitka, návrh odešleme vymezuje "
        "okolnost, za které zamýšlený postup proběhne. Za předpokladu, že "
        "je formálnější způsob uvedení podmínky.",
        rules=[
            "Nezaměňujte nezbytnou podmínku s příslibem automatického schválení.",
            "U záporné podmínky ověřte, co přesně brání uskutečnění děje.",
        ],
        examples=[
            GrammarExample("Slevu poskytneme jen tehdy, pokud objednáte alespoň deset kusů."),
            GrammarExample("Pokud do pátku nevznesete námitku, odešleme konečnou verzi."),
            GrammarExample("Termín dodržíme za předpokladu, že podklady dostaneme dnes."),
        ],
        related=["cs-negation-scope-b2", "cs-polite-softening-b2"],
    ),
    GrammarTopic(
        "cs-standard-spoken-b2",
        "Spisovné, hovorové a obecněčeské podoby",
        "B2",
        "Jazykový rejstřík",
        "Rozpoznávejte běžnou mluvu a volte podobu vhodnou pro danou situaci.",
        "Mluvený projev není automaticky nespisovný. Tvary můžu nebo taky "
        "patří k běžným spisovným prostředkům, zatímco obecněčeské dobrej "
        "a nový auta se do neutrálního formálního textu nehodí. V něm zvolíme "
        "dobrý a nová auta. Obecná čeština je rozšířená hlavně v Čechách; "
        "běžná mluva na Moravě a ve Slezsku má i jiné podoby. Rozpoznání "
        "nespisovné varianty není požadavek používat ji v každém rozhovoru.",
        rules=[
            "Nevydávejte běžný neformální tvar za chybu bez určení požadovaného rejstříku.",
            "Ve formální žádosti volte neutrální spisovné tvary a přehlednou stavbu vět.",
        ],
        examples=[
            GrammarExample("Můžu se na něco zeptat?", note="Běžná spisovná mluvená podoba."),
            GrammarExample(
                "To je dobrej nápad.",
                note="Běžná obecněčeská podoba; neutrálně spisovně: To je dobrý nápad.",
            ),
            GrammarExample("Děkujeme za nové podklady a žádáme o upřesnění termínu."),
        ],
        related=["cs-polite-softening-b2", "cs-particles-b2"],
    ),
    GrammarTopic(
        "cs-polite-softening-b2",
        "Zdvořilá žádost, výhrada a odmítnutí",
        "B2",
        "Zdvořilost",
        "Upravujte sílu sdělení, aniž ztratíte jeho jasný účel.",
        "Podmiňovací způsob může zmírnit žádost: Mohl byste mi poslat podklady? "
        "Záporná otázka Nemohl byste mi pomoci? bývá rovněž žádostí, ne "
        "zjišťováním neschopnosti. Při odmítnutí lze nejprve uznat potřebu "
        "druhé strany a potom jasně vymezit hranici. Hromadění slov možná, "
        "trochu a případně může naopak zastřít, co skutečně potřebujete.",
        rules=[
            "Rozlišujte prosbu, doporučení a závazný požadavek.",
            "Při vykání jedné osobě zachovejte rod: mohl byste, mohla byste.",
        ],
        examples=[
            GrammarExample("Mohla byste prosím potvrdit termín do středy?"),
            GrammarExample("Rozumím, že spěcháte, ale bez podkladů nemohu žádost dokončit."),
            GrammarExample("Navrhoval bych nejdřív ověřit náklady a teprve potom rozhodnout."),
        ],
        related=["cs-standard-spoken-b2", "cs-conditional-limits-b2"],
    ),
    GrammarTopic(
        "cs-particles-b2",
        "Vždyť, přece a snad v rozhovoru",
        "B2",
        "Postoj mluvčího",
        "Rozpoznávejte očekávání, připomenutí a možné podráždění.",
        "Vždyť a přece často připomínají skutečnost, kterou mluvčí pokládá "
        "za známou: Vždyť jsme se domluvili. Podle tónu mohou uklidňovat "
        "nebo vyčítat. Snad může vyjadřovat naději či nejistotu: Snad to "
        "stihneme. V otázce Ty jsi na to snad zapomněl? může signalizovat "
        "překvapení nebo výtku. Význam proto určujeme i podle vztahu a intonace.",
        rules=[
            "Částice nejsou důkazem, že adresát sdílí mluvčího předpoklad.",
            "Při nejistotě ohledně tónu si ověřte záměr místo okamžitého protiútoku.",
        ],
        examples=[
            GrammarExample("Nemusíš spěchat, vždyť máme ještě hodinu."),
            GrammarExample("To jsme si přece už vysvětlili.", note="Může znít netrpělivě."),
            GrammarExample("Snad se nám podaří najít termín, který bude vyhovovat oběma."),
        ],
        related=["cs-evidentiality-b2", "cs-polite-softening-b2"],
    ),
    GrammarTopic(
        "cs-reference-cohesion-b2",
        "Zájmena a jednoznačné odkazy v textu",
        "B2",
        "Soudržnost textu",
        "Udržujte přehled o účastnících a o tom, na co navazujete.",
        "Zájmena tento, ten, on nebo to mohou odkazovat k předchozímu textu. "
        "Shoda v rodě a čísle pomáhá, ale při více možných předchůdcích nestačí. "
        "Věta „Jana řekla Evě, že její návrh podpoří“ sama neurčuje jednoznačně, "
        "o čí návrh jde. V důležité dohodě zopakujte jméno. Zájmeno to může "
        "odkazovat také na celý děj: Schůzku odložili. To nám zkomplikovalo plán.",
        rules=[
            "Nespoléhejte pouze na pravidlo nejbližšího jména; rozhoduje také kontext.",
            "Opakování podstatného jména je vhodné, pokud zabrání věcné nejasnosti.",
        ],
        examples=[
            GrammarExample("Jana řekla Evě, že podpoří Evin návrh."),
            GrammarExample("Dodavatel změnil termín. Tato změna ovlivní i školení."),
            GrammarExample("Oba týmy souhlasily s odkladem. To však nevyřešilo nedostatek lidí."),
        ],
        related=["cs-reported-speech-b2", "cs-discourse-markers-b2"],
    ),
    GrammarTopic(
        "cs-discourse-markers-b2",
        "Jinými slovy, nicméně a z toho plyne",
        "B2",
        "Stavba argumentace",
        "Ukažte, zda vysvětlujete, namítáte, nebo vyvozujete závěr.",
        "Jinými slovy uvádí přeformulování a nemá bez upozornění měnit obsah. "
        "Nicméně signalizuje omezení nebo protiklad. Proto a z toho plyne "
        "uvádějí důsledek či závěr, který musí mít oporu v předchozí informaci. "
        "Výraz mimochodem naopak otevírá vedlejší téma. V delším rozhovoru "
        "pomáhá nejprve stručně shrnout shodu a potom pojmenovat otevřený bod.",
        rules=[
            "Zvolte spojovací výraz podle skutečného vztahu mezi sděleními.",
            "Při shrnutí nerozšiřujte souhlas jedné strany na body, o nichž nemluvila.",
        ],
        examples=[
            GrammarExample("Cena zahrnuje dopravu. Jinými slovy, za doručení už nic nepřiplatíte."),
            GrammarExample("Na termínu se shodujeme. Nicméně způsob úhrady zůstává otevřený."),
            GrammarExample("Obě nabídky překračují rozpočet, proto požádáme o jejich úpravu."),
        ],
        related=["cs-reference-cohesion-b2", "cs-concession-b2"],
    ),
    GrammarTopic(
        "cs-focus-particles-b2",
        "Jen, pouze, i a právě",
        "B2",
        "Rozsah a důraz",
        "Určete, kterou informaci omezujete nebo přidáváte.",
        "Jen a pouze omezují platnost na určitý člen. Jen Jana podepsala smlouvu "
        "omezuje skupinu podepisujících; Jana podepsala jen smlouvu omezuje "
        "to, co podepsala. I může přidávat dalšího účastníka nebo neočekávaný "
        "případ. Právě může zdůraznit konkrétní člen, ale také označovat čas: "
        "Právě odcházím. Rozsah částice pomáhá určit umístění, přízvuk a kontext.",
        rules=[
            "V písemné dohodě umístěte omezující výraz co nejblíže k tomu, co omezuje.",
            "Při přeformulování zachovejte, zda se omezení týká osoby, věci, nebo času.",
        ],
        examples=[
            GrammarExample("Slevu nabízíme pouze členům spolku."),
            GrammarExample(
                "I Jana s návrhem souhlasila.",
                note="Jana se přidala k dalším souhlasícím.",
            ),
            GrammarExample("Právě termín dodání nám nevyhovuje, cenu přijímáme."),
        ],
        related=["cs-information-structure-b2", "cs-negation-scope-b2"],
    ),
]
