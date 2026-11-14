"""Czech C1 grammar, discourse and pragmatic control."""

from app.data._types import GrammarExample, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "cs-attribution-c1",
        "Podle, prý a údajně: komu tvrzení patří",
        "C1",
        "Zdroj informace",
        "Oddělte převzatou zprávu od vlastního potvrzení její pravdivosti.",
        "Spojení podle mluvčího pojmenovává zdroj. Částice prý označuje převzatou informaci, "
        "aniž by sama určovala, zda je pravdivá. Údajně často navíc vyjadřuje odstup od "
        "neověřeného tvrzení. V odborném nebo úředním shrnutí bývá přesnější zdroj výslovně "
        "uvést než pouze napsat prý. Při převyprávění zachovejte i nejistotu obsaženou ve zdroji.",
        structure="Podle + 2. pád; zdroj uvádí, že…; prý / údajně + tvrzení",
        rules=[
            "Podle nevyjadřuje samo o sobě souhlas autora se zdrojem.",
            "Tvrzení dodavatele není automaticky nezávisle ověřené zjištění.",
            "Prý může v rozhovoru vyjadřovat i překvapení či pochybnost; rozhoduje kontext.",
        ],
        examples=[
            GrammarExample(
                "Podle dodavatele by oprava mohla skončit v pátek.",
                note="Zdroj i podmíněná možnost zůstávají výslovně uvedeny.",
            ),
            GrammarExample(
                "Oprava je údajně hotová, ale předávací protokol zatím nemáme.",
                note="Mluvčí zprávu nepředkládá jako vlastní ověřené zjištění.",
            ),
        ],
        related=["cs-inference-c1", "cs-evidence-limits-c1"],
    ),
    GrammarTopic(
        "cs-inference-c1",
        "Musí jít o chybu: úsudek, nikoli povinnost",
        "C1",
        "Míra jistoty",
        "Rozlišujte silný úsudek, pravděpodobnost a pouhou možnost.",
        "Modální sloveso muset může vyjadřovat závěr z okolností, nejen povinnost. "
        "Ve větě To musí být omyl mluvčí hodnotí vysvětlení jako velmi pravděpodobné. "
        "Může to být omyl ponechává otevřené jiné možnosti. Výrazy zřejmě a patrně obvykle "
        "signalizují úsudek, nikoli přímý důkaz; jejich sílu pomáhá určit celý kontext.",
        rules=[
            "Úsudkové musí nelze bez změny jistoty nahradit výrazem možná.",
            "Záporné nemusí znamená také, že závěr není nutný: vyšší cena nemusí znamenat kvalitu.",
            "Při shrnutí nezaměňujte pravděpodobný závěr za prokázanou příčinu.",
        ],
        examples=[
            GrammarExample(
                "Součty se liší přesně o částku na jedné faktuře; "
                "zřejmě jsme ji započítali dvakrát."
            ),
            GrammarExample(
                "To musí být omyl: v potvrzení je jiný termín, než jsme si domluvili.",
                note="Musí vyjadřuje silný úsudek mluvčího, nikoli příkaz udělat chybu.",
            ),
            GrammarExample(
                "Ticho v sále nemusí znamenat souhlas; účastníci možná čekají na vysvětlení."
            ),
        ],
        related=["cs-attribution-c1"],
    ),
    GrammarTopic(
        "cs-evidence-limits-c1",
        "Pokud lze soudit a nakolik víme",
        "C1",
        "Vymezení platnosti",
        "Uveďte, na jakých podkladech a v jakém rozsahu závěr platí.",
        "Výrazy pokud lze soudit z dostupných údajů, nakolik víme a podle dosavadních "
        "výsledků omezují poznávací základ tvrzení. Nejde o libovolnou zdvořilostní ozdobu: "
        "čtenář potřebuje vědět, co bylo zkoumáno a co zůstává otevřené. Závěr o části "
        "souboru nepřenášejte bez dalšího na celek.",
        rules=[
            "Výhradu umístěte k tvrzení, které omezuje.",
            "Rozlišujte chybějící důkaz problému od důkazu, že problém neexistuje.",
        ],
        examples=[
            GrammarExample(
                "Pokud lze soudit z prvních dvou měsíců, opatření snížilo počet stížností."
            ),
            GrammarExample(
                "Z dosavadních odpovědí nevyplývá, že by lidé změnu odmítali; "
                "názor většiny obyvatel však zatím neznáme."
            ),
        ],
        related=["cs-argument-scope-c1"],
    ),
    GrammarTopic(
        "cs-reason-result-c1",
        "Totiž, proto a z toho vyplývá",
        "C1",
        "Výstavba argumentu",
        "Uspořádejte důvod, tvrzení a závěr bez obrácení jejich vztahu.",
        "Totiž uvádí dodatečné vysvětlení předchozího sdělení: Jednání odložíme. "
        "Chybí totiž rozpočet. Proto naopak připojuje důsledek: Chybí rozpočet, proto "
        "jednání odložíme. Z toho vyplývá označuje závěr argumentace, ale samotný spojovací "
        "výraz nezaručuje, že podklady tak silný závěr skutečně umožňují.",
        rules=[
            "Totiž obvykle nestojí na úplném začátku vysvětlující věty.",
            "Při změně pořadí vět upravte spojovací výraz, nikoli věcný vztah.",
            "Rozlišujte příčinu události od důvodu, proč určitému tvrzení věříte.",
        ],
        examples=[
            GrammarExample("Návrh nelze zatím ocenit. Neobsahuje totiž rozsah prací."),
            GrammarExample(
                "V zápisu chybí výsledek hlasování; z toho však nevyplývá, že se nehlasovalo."
            ),
        ],
        related=["cs-discourse-links-c1", "cs-evidence-limits-c1"],
    ),
    GrammarTopic(
        "cs-argument-scope-c1",
        "Pokud jde o a do té míry, do jaké",
        "C1",
        "Rozsah argumentu",
        "Vymezte téma nebo míru platnosti hodnocení.",
        "Pokud jde o zavádí oblast, k níž se výrok vztahuje; nejde zde o běžnou podmínku. "
        "Spojení do té míry, do jaké váže platnost jednoho tvrzení na rozsah druhého. "
        "Umožňuje podmíněné hodnocení místo neomezeného souhlasu. Když shrnujete argument, "
        "zachovejte jak zvolenou oblast, tak případné omezení míry.",
        rules=[
            "Pokud jde o cenu neříká nic samo o sobě o kvalitě nebo termínu.",
            "Míru vyjádřenou do té míry nelze bez dalšího změnit na úplnou platnost.",
        ],
        examples=[
            GrammarExample(
                "Pokud jde o dostupnost, návrh vyhovuje; jeho náklady musíme ještě posoudit."
            ),
            GrammarExample(
                "Průzkum je vypovídající do té míry, do jaké vzorek odpovídá celé populaci."
            ),
        ],
        related=["cs-evidence-limits-c1", "cs-corrective-contrast-c1"],
    ),
    GrammarTopic(
        "cs-corrective-contrast-c1",
        "Nikoli příčina, nýbrž souvislost",
        "C1",
        "Zpřesňování argumentu",
        "Opravte nesprávné zařazení bez popření celého sdělení.",
        "Konstrukce nikoli X, nýbrž Y nahrazuje jednu charakteristiku jinou. V běžném "
        "rozhovoru často stačí ne X, ale Y. Spojení ani ne tak X jako spíše Y naproti tomu "
        "může pouze měnit důraz, nikoli X zcela vylučovat. Při opravě výkladu je nutné "
        "rozlišit úplné odmítnutí označení od odstupňování jeho významu.",
        rules=[
            "Části kontrastu by měly mít srovnatelnou syntaktickou stavbu.",
            "Nýbrž je spisovné a působí knižněji než ale; ale není nesprávné.",
            "Spíše nelze vypustit, pokud původní výrok ponechává první možnost částečně platnou.",
        ],
        examples=[
            GrammarExample("Studie dokládá nikoli příčinu, nýbrž souvislost mezi oběma jevy."),
            GrammarExample(
                "Nejde ani tak o nedostatek peněz jako spíše o jejich nerovnoměrné rozdělení."
            ),
        ],
        related=["cs-argument-scope-c1", "cs-interaction-repair-c1"],
    ),
    GrammarTopic(
        "cs-necessary-conditions-c1",
        "Jen pokud: nutná podmínka není záruka",
        "C1",
        "Podmínky dohody",
        "Rozlišujte podmínku přijetí od příslibu, že k přijetí dojde.",
        "Věta Nabídku přijmeme jen tehdy, pokud se vejde do rozpočtu stanoví nutnou "
        "podmínku. Sama ještě neslibuje přijetí každé nabídky splňující rozpočet. "
        "Věta Pokud se nabídka vejde do rozpočtu, přijmeme ji naopak v daném sdělení "
        "představuje splnění rozpočtu jako dostačující podmínku přijetí.",
        rules=[
            "Při převyprávění zachovejte omezující jen nebo pouze.",
            "Výraz můžeme přijmout vyjadřuje možnost, ne stejný závazek jako přijmeme.",
        ],
        examples=[
            GrammarExample("Termín můžeme potvrdit pouze tehdy, pokud dostaneme všechny podklady."),
            GrammarExample("Pokud cenu snížíte na dohodnutou částku, objednávku dnes potvrdíme."),
            GrammarExample(
                "Na společnou dovolenou pojedu jen tehdy, pokud si náklady rozdělíme předem. "
                "Ještě si ale musím ověřit, zda dostanu volno.",
                note="Dohoda o nákladech je nutná, sama však účast nezaručuje.",
            ),
        ],
        related=["cs-exceptions-c1", "cs-hypothetical-concession-c1"],
    ),
    GrammarTopic(
        "cs-exceptions-c1",
        "Ledaže, leda by a s výjimkou",
        "C1",
        "Výjimky",
        "Vymezte okolnost, která mění jinak platný postup.",
        "Ledaže uvádí výjimku: Termín zůstává, ledaže dodavatel požádá o změnu. "
        "Konstrukce leda by s příčestím vyjadřuje uvažovanou výjimku: leda by dodavatel "
        "požádal o změnu. Po s výjimkou následuje druhý pád. Výjimka vyjímá případ z "
        "obecného tvrzení; nemusí sama určovat všechny další kroky v tomto případě.",
        rules=[
            "Nepřidávejte zápor automaticky: ledaže požádá a ledaže nepožádá mají jiný význam.",
            "Při převodu jmenné výjimky na větu zachovejte její rozsah.",
        ],
        examples=[
            GrammarExample("Zasedání se uskuteční v pondělí, ledaže předsedkyně oznámí změnu."),
            GrammarExample(
                "Návrh dnes neuzavřeme, leda bychom ještě dostali chybějící stanovisko."
            ),
        ],
        related=["cs-necessary-conditions-c1"],
    ),
    GrammarTopic(
        "cs-hypothetical-concession-c1",
        "Přestože a i kdyby: skutečnost nebo hypotéza",
        "C1",
        "Přípustka v argumentaci",
        "Uznávejte překážky, aniž byste z hypotézy udělali doložený fakt.",
        "Přestože představuje okolnost jako platnou. I kdyby s podmiňovacím způsobem "
        "pracuje s hypotézou a říká, že ani její splnění by závěr nezměnilo. Věta "
        "I kdyby se náklady snížily, návrh bych nepodpořil netvrdí, že ke snížení došlo. "
        "Při vyjednávání tak lze oddělit cenovou otázku od jiné rozhodující námitky.",
        rules=[
            "Zachovejte rozdíl mezi uznanou skutečností a uvažovaným případem.",
            "Přípustka vyjadřuje rozpor s očekáváním, nikoli automaticky příčinu rozhodnutí.",
        ],
        examples=[
            GrammarExample(
                "Přestože se náklady snížily, návrh stále nesplňuje bezpečnostní požadavky."
            ),
            GrammarExample(
                "I kdyby dodávka přišla zítra, otevření bychom nestihli; chybí nám povolení."
            ),
        ],
        related=["cs-necessary-conditions-c1", "cs-argument-scope-c1"],
    ),
    GrammarTopic(
        "cs-propositional-reference-c1",
        "Což: komentář k celé předchozí výpovědi",
        "C1",
        "Větné odkazování",
        "Odlište hodnocení události od vlastnosti konkrétního předmětu.",
        "Vztažné což může odkazovat na obsah celé předchozí věty: Rada jednání odložila, "
        "což nás překvapilo. Zájmeno který se naproti tomu obvykle vztahuje ke konkrétnímu "
        "jménu: Rada odložila návrh, který jsme připravili. Tvar čehož nebo čímž se řídí "
        "vazbou následujícího výrazu. Není-li rozsah odkazu jasný, použijte samostatnou větu.",
        rules=[
            "Před připojenou vztažnou větou píšeme čárku.",
            "Vyjádření čímž může připisovat události důsledek; tento vztah musí být doložen.",
        ],
        examples=[
            GrammarExample("Dodavatel posunul termín, čehož si účetní všimla při kontrole."),
            GrammarExample(
                "Výbor zveřejnil úplný zápis, čímž umožnil obyvatelům ověřit průběh hlasování."
            ),
        ],
        related=["cs-cohesive-reference-c1", "cs-reason-result-c1"],
    ),
    GrammarTopic(
        "cs-nominalisation-agents-c1",
        "Od slovesného podstatného jména k jasné větě",
        "C1",
        "Role účastníků",
        "Rozbalte úřední formulaci bez změny aktéra nebo stavu rozhodnutí.",
        "Slovesná podstatná jména jako schválení, předání a posouzení zhušťují děj, ale "
        "mohou zastřít jeho účastníky. Spojení posouzení návrhu komisí označuje návrh jako "
        "předmět posouzení a komisi jako posuzovatele. Samo podstatné jméno neurčuje, zda "
        "je děj dokončený; čas a stav vyplývají z okolí. Návrh na odložení není totéž co odložení.",
        rules=[
            "Nevymýšlejte aktéra, kterého původní text neuvádí.",
            "Zachovejte rozdíl mezi plánovaným posouzením a schváleným výsledkem.",
        ],
        examples=[
            GrammarExample(
                "Posouzení žádosti komisí proběhne v úterý. Komise tedy žádost posoudí v úterý."
            ),
            GrammarExample(
                "O návrhu výboru na odložení opravy se bude hlasovat. "
                "Výbor odložení navrhl; zatím nebylo schváleno."
            ),
        ],
        related=["cs-infinitive-agents-c1", "cs-register-reformulation-c1"],
    ),
    GrammarTopic(
        "cs-infinitive-agents-c1",
        "Slíbit, požádat a umožnit: kdo má jednat",
        "C1",
        "Infinitivní vazby",
        "Určete nevyjádřeného vykonavatele děje podle řídícího slovesa.",
        "Ve větě Eva slíbila Petrovi zavolat má zavolat Eva. Ve větě Eva požádala Petra, "
        "aby zavolal má zavolat Petr. Vazba Eva umožnila Petrovi nahlédnout do spisu "
        "dává Petrovi možnost; nepotvrzuje, že ji využil. Infinitivní vazby nelze převádět "
        "mechanicky: sloveso určuje role, závazek i vztah k uskutečnění děje.",
        rules=[
            "Po slíbit označuje podmět zpravidla i vykonavatele slíbené činnosti.",
            "Požádat někoho, aby něco udělal neznamená, že žádosti vyhověl.",
            "Při nejasnosti použijte vedlejší větu s výslovně uvedeným podmětem.",
        ],
        examples=[
            GrammarExample("Lenka slíbila kolegovi ověřit čísla; kontrolu tedy přislíbila Lenka."),
            GrammarExample(
                "Vedoucí umožnila Janovi pracovat z domova, ale Jan zatím zůstává v kanceláři."
            ),
        ],
        related=["cs-nominalisation-agents-c1", "cs-register-reformulation-c1"],
    ),
    GrammarTopic(
        "cs-cohesive-reference-c1",
        "Tento postup, uvedené zjištění a nejasné to",
        "C1",
        "Soudržnost textu",
        "Zpřesněte návaznost tak, aby čtenář věděl, k čemu se vracíte.",
        "Zájmena to, ten a jejich tvary mohou odkazovat k více částem předchozího textu. "
        "Shrnující pojmenování tento postup, uvedená výhrada nebo toto zjištění objasňuje "
        "odkaz, zároveň však obsah zařazuje. Návrh proto nepřejmenovávejte na rozhodnutí "
        "a podezření na zjištění. Shoda rodu sama o sobě nezaručuje jednoznačnost.",
        rules=[
            "Po více možných předchůdcích zopakujte klíčové podstatné jméno.",
            "Shrnující jméno musí odpovídat skutečnému statusu sdělení.",
        ],
        examples=[
            GrammarExample(
                "Komise doporučila změnit trasu. Toto doporučení rada projedná v pondělí."
            ),
            GrammarExample(
                "Petra poslala Janě upravenou smlouvu. Jana pak smlouvu předala právníkovi.",
                note="Zopakování jména odstraňuje nejasnost, kterou by mohlo vytvořit zájmeno ona.",
            ),
        ],
        related=["cs-propositional-reference-c1", "cs-discourse-links-c1"],
    ),
    GrammarTopic(
        "cs-recoverable-ellipsis-c1",
        "Výpustka bez ztráty významu",
        "C1",
        "Zhušťování textu",
        "Vynechte opakování jen tehdy, když lze bezpečně doplnit obsah i vazbu.",
        "V souřadných větách lze vypustit opakovaný přísudek: Jana ověřila ceny, Petr "
        "termíny. Čtenář doplní ověřil se shodou podle nového podmětu. Nelze však automaticky "
        "sdílet jeden předmět mezi slovesy s různými vazbami. Místo zabýváme se a hodnotíme "
        "návrh je vhodné zabýváme se návrhem a hodnotíme ho.",
        rules=[
            "Výpustka musí umožňovat jednoznačné doplnění děje a jeho účastníků.",
            "U rozdílných pádových vazeb zopakujte jméno nebo použijte správný tvar zájmena.",
        ],
        examples=[
            GrammarExample("Jana zkontrolovala rozpočet, Petr harmonogram a Eva přílohy."),
            GrammarExample("O návrhu jsme diskutovali a nakonec jsme ho podpořili."),
        ],
        related=["cs-cohesive-reference-c1", "cs-nominalisation-agents-c1"],
    ),
    GrammarTopic(
        "cs-discourse-links-c1",
        "Nicméně, ostatně a naopak",
        "C1",
        "Návaznost argumentů",
        "Volte spojovací výrazy podle vztahu mezi myšlenkami.",
        "Nicméně přináší omezení nebo protiklad k očekávání vyvolanému předchozí větou. "
        "Ostatně připojuje další podpůrnou okolnost, často jako doplňující argument. "
        "Naopak označuje obrácený vztah či protiklad, nikoli jakékoli jiné téma. "
        "Přehledný odstavec má rozpoznatelnou hlavní myšlenku i bez množství spojovacích výrazů.",
        rules=[
            "Nicméně může stát na začátku věty; nenahrazuje však vysvětlení námitky.",
            "Naopak používejte tehdy, když lze určit, vůči čemu je tvrzení opačné.",
        ],
        examples=[
            GrammarExample(
                "Návrh přinese úspory. Nicméně počáteční investice zatíží letošní rozpočet."
            ),
            GrammarExample(
                "Změnu je vhodné nejprve vyzkoušet. Ostatně stejný postup doporučili i uživatelé."
            ),
        ],
        related=["cs-reason-result-c1", "cs-corrective-contrast-c1"],
    ),
    GrammarTopic(
        "cs-shared-knowledge-particles-c1",
        "Vždyť a přece: připomenutí i nátlak",
        "C1",
        "Postoj v rozhovoru",
        "Rozpoznejte, kdy mluvčí předkládá informaci jako společně známou.",
        "Vždyť často uvádí připomenutí či důvod: Vždyť jsme to probírali. Přece může "
        "předkládat tvrzení jako zřejmé a očekávat souhlas. Podle intonace a situace mohou "
        "oba výrazy působit vstřícně, překvapeně nebo vyčítavě. Jejich použití nedokazuje, "
        "že adresát opravdu souhlasil nebo že danou věc ví.",
        rules=[
            "Při zprostředkování nepřebírejte údajný společný souhlas bez ověření.",
            "Význam částice posuzujte společně s intonací a předchozími replikami.",
        ],
        examples=[
            GrammarExample(
                "Vždyť na to nejsi sám, pomůžeme ti.",
                note="V podpůrném kontextu jde o uklidňující připomenutí.",
            ),
            GrammarExample(
                "My jsme se přece dohodli. — Na termínu ano, na ceně zatím ne.",
                note="Odpověď omezuje rozsah předpokládané shody.",
            ),
        ],
        related=["cs-interaction-repair-c1", "cs-mediating-voices-c1"],
    ),
    GrammarTopic(
        "cs-tentative-requests-c1",
        "Nešlo by a byl bych rád, kdyby",
        "C1",
        "Zdvořilost a vyjednávání",
        "Změkčete žádost, aniž byste zastřeli její obsah nebo reálné možnosti.",
        "Otázka Nešlo by posunout termín? obvykle zkoumá možnost změny a zároveň o ni "
        "zdvořile žádá. Nejde jen o neutrální dotaz na schopnost. Byl bych rád, kdybyste "
        "vyjadřuje přání; v nadřízeném postavení však může znít jako nepřímý pokyn. "
        "Zdvořilý tvar proto neruší vliv rolí a situace.",
        rules=[
            "Kdybyste je jeden spisovný tvar; podoba kdyby jste do spisovného textu nepatří.",
            "Při odmítnutí pojmenujte omezení a případně nabídněte splnitelnou alternativu.",
            "Změkčení neznamená neurčitost: uveďte, co a do kdy potřebujete.",
        ],
        examples=[
            GrammarExample("Nešlo by poslat podklady do středy, abychom je stihli projít?"),
            GrammarExample(
                "Do středy úplný rozbor nezvládnu. Mohl bych vám ale poslat předběžné závěry."
            ),
        ],
        related=["cs-necessary-conditions-c1", "cs-register-reformulation-c1"],
    ),
    GrammarTopic(
        "cs-interaction-repair-c1",
        "Vlastně, přesněji řečeno a rozumím tomu správně",
        "C1",
        "Oprava nedorozumění",
        "Zpřesněte vlastní sdělení a ověřte výklad druhé strany.",
        "Přesněji řečeno opravuje nebo zužuje předchozí formulaci. Vlastně může uvádět "
        "opravu, dodatečné uvědomění nebo návrat k jádru věci; funkci určuje situace. "
        "Otázka Rozumím tomu správně, že… předkládá výklad k potvrzení, nikoli hotovou "
        "dohodu. V zápisu zaznamenejte opravenou verzi, pokud ji mluvčí skutečně potvrdil.",
        rules=[
            "Při opravě odlište změnu informace od pouhé změny formulace.",
            "Ověřovací otázku nepřepisujte jako souhlas dotazovaného.",
        ],
        examples=[
            GrammarExample(
                "Zprávu pošlu v pátek, přesněji řečeno její pracovní verzi; přílohy dodám v pondělí."
            ),
            GrammarExample(
                "Rozumím tomu správně, že chcete nejdřív ověřit cenu a až potom vybrat dodavatele?"
            ),
        ],
        related=["cs-corrective-contrast-c1", "cs-cohesive-reference-c1"],
    ),
    GrammarTopic(
        "cs-mediating-voices-c1",
        "Jedna strana uvádí…, druhá namítá…",
        "C1",
        "Zprostředkování stanovisek",
        "Udržte odlišné hlasy a nezaměňte rozdílné postoje za společný závěr.",
        "Při zprostředkování určujte, komu tvrzení náleží. Slovesa uvádí, upozorňuje, "
        "připouští a namítá mají různý význam: připouští může uznávat možnost, nikoli "
        "potvrzovat fakt. Zatímco umožňuje souběžně porovnat postoje. Shodu lze shrnout "
        "samostatně, ale jen v bodech, v nichž se strany skutečně shodly.",
        rules=[
            "Nezaměňujte názor účastníka za hodnocení zprostředkovatele.",
            "Pojmenujte nevyřešený bod a zachovejte podmínky případného souhlasu.",
        ],
        examples=[
            GrammarExample(
                "Obyvatelé žádají klidnější večery, zatímco provozovatel upozorňuje "
                "na příjmy z večerních akcí."
            ),
            GrammarExample(
                "Obě strany souhlasí s měřením hluku; na zkrácení provozu se zatím neshodly."
            ),
        ],
        related=["cs-attribution-c1", "cs-shared-knowledge-particles-c1"],
    ),
    GrammarTopic(
        "cs-register-reformulation-c1",
        "Od rozhovoru k formálnímu shrnutí",
        "C1",
        "Styl a zachování významu",
        "Přizpůsobte formulaci adresátovi bez posílení závazku nebo jistoty.",
        "Změna stylu může nahradit hovorové výrazy neutrálními a zkrátit opakování. "
        "Nesmí však proměnit zkusím v zajistím, mohl bych v provedu nebo předběžně "
        "v definitivně. Přímý citát a shrnutí plní jinou funkci: shrnutí nemusí zachovat "
        "každé slovo, musí však zachovat účastníky, čas, rozsah a míru závazku.",
        rules=[
            "Spisovná úprava není důvodem k vypuštění věcné výhrady.",
            "Hovorový výraz není automaticky gramatická chyba; volba závisí na situaci.",
        ],
        examples=[
            GrammarExample(
                "Jana: „Zkusím se na ten návrh zítra jen zběžně mrknout.“ — "
                "Jana se pokusí návrh zítra zběžně projít.",
                note="Při shrnutí ve stejný den zůstává zítra. Pokus ani výslovně zběžná "
                "kontrola se nemění v závazek návrh dokončit.",
            ),
            GrammarExample(
                "Petr: „S cenou problém nemám, ale termín neslíbím.“ — "
                "Petr nemá k ceně výhrady, termín však nepřislibuje."
            ),
        ],
        related=["cs-infinitive-agents-c1", "cs-tentative-requests-c1"],
    ),
    GrammarTopic(
        "cs-contextual-irony-c1",
        "To se nám povedlo: doslovný a ironický význam",
        "C1",
        "Pragmatika",
        "Vyvozujte záměr z okolností a při nejistotě se doptávejte.",
        "Kladně znějící věta může při zjevném nezdaru fungovat ironicky. Není to vlastnost "
        "samotných slov: To se nám povedlo může být upřímná pochvala i sebekritická nadsázka. "
        "Intonace, vztahy a situace pomáhají výklad určit. V pracovním shrnutí raději popište "
        "věcný problém, pokud ironická formulace není pro účel textu důležitá.",
        rules=[
            "Ironie nemusí být osobní útok; může mířit na situaci nebo na samotného mluvčího.",
            "Bez dostatečného kontextu nepřisuzujte mluvčímu ironii s jistotou.",
        ],
        examples=[
            GrammarExample(
                "Zase jsem si nechal deštník doma. To jsem ale připravený!",
                note="Mluvčí sám sobě vytýká nepřipravenost formou zdánlivé pochvaly.",
            ),
            GrammarExample(
                "Myslíš to jako pochvalu, nebo narážíš na tu chybu v rozpočtu?",
                note="Ověření záměru je vhodnější než automatická obranná reakce.",
            ),
        ],
        related=["cs-interaction-repair-c1", "cs-register-reformulation-c1"],
    ),
]
