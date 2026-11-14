"""Czech C1 placement questions on inference, register and practical argumentation."""

from app.data._types import AssessmentQuestion

C1_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "cs-g-c1-001",
        "grammar",
        "C1",
        "Redaktorka napsala: „Podle správce by oprava mohla skončit v pátek.“ "
        "Která věta vhodně navazuje, aniž by změnila status této informace?",
        [
            "Redakce tedy uvádí pátek jako vlastní odhad založený na kontrole stavby.",
            "Správce tím převzal závazek předat v pátek dokončenou opravu.",
            "Před oznámením pevného termínu je ještě třeba získat potvrzení.",
            "Páteční termín už lze zveřejnit jako schválený harmonogram správce.",
        ],
        "Před oznámením pevného termínu je ještě třeba získat potvrzení.",
        "cs-attribution-c1",
    ),
    AssessmentQuestion(
        "cs-g-c1-002",
        "grammar",
        "C1",
        "Výbor uvedl: „Nabídku přijmeme pouze tehdy, pokud obdržíme písemnou záruku.“ "
        "Dodavatel záruku poslal. Co lze z původního výroku vyvodit?",
        [
            "Jedna nutná podmínka je splněna; samotný výrok ještě přijetí nezaručuje.",
            "Výbor slíbil nabídku přijmout, jakmile bude záruka písemně doručena.",
            "Doručením záruky přešlo rozhodnutí o přijetí z výboru na dodavatele.",
            "Výbor se zavázal po doručení záruky upustit od posuzování ostatních podmínek.",
        ],
        "Jedna nutná podmínka je splněna; samotný výrok ještě přijetí nezaručuje.",
        "cs-necessary-conditions-c1",
    ),
    AssessmentQuestion(
        "cs-g-c1-003",
        "grammar",
        "C1",
        "V podkladu stojí: „O návrhu komise na odložení rekonstrukce se bude hlasovat "
        "příští týden.“ Které shrnutí zachovává rozdělení rolí i stav věci?",
        [
            "Komise příští týden zveřejní rozhodnutí, kterým rekonstrukci odložila.",
            "O odložení práce komise na rekonstrukci se rozhodne příští týden.",
            "Komise příští týden navrhne, aby se odložilo hlasování o rekonstrukci.",
            "Komise navrhla rekonstrukci odložit; o jejím návrhu se má hlasovat příští týden.",
        ],
        "Komise navrhla rekonstrukci odložit; o jejím návrhu se má hlasovat příští týden.",
        "cs-nominalisation-agents-c1",
    ),
    AssessmentQuestion(
        "cs-g-c1-004",
        "grammar",
        "C1",
        "Organizátorka píše: „Setkání proběhne venku, ledaže bude vydána výstraha před "
        "silným větrem.“ Jak máte podle zprávy plánovat, pokud výstraha vydána nebude?",
        [
            "Připravit venkovní setkání až poté, co organizátorka zvlášť potvrdí bezvětří.",
            "Počítat s venkovním setkáním podle oznámeného plánu.",
            "Vyčkat na nové rozhodnutí, protože zpráva určuje postup jen při výstraze.",
            "Přesunout setkání dovnitř, protože výjimka se vztahuje na nepřítomnost výstrahy.",
        ],
        "Počítat s venkovním setkáním podle oznámeného plánu.",
        "cs-exceptions-c1",
    ),
    AssessmentQuestion(
        "cs-g-c1-005",
        "grammar",
        "C1",
        "Recenzent píše: „Nejde ani tak o nedostatek údajů jako spíše o způsob jejich "
        "vyhodnocení.“ Která reakce nejlépe respektuje rozložení důrazu v této větě?",
        [
            "Přednostně upravíme analýzu a zároveň prověříme, zda některé údaje nechybějí.",
            "Nejprve doplníme údaje, protože způsob jejich vyhodnocení recenzent schvaluje.",
            "Rozdělíme práci rovnoměrně, protože recenzent označil oba problémy za stejně závažné.",
            "Zaměříme se jen na analýzu, protože recenzent výslovně potvrdil úplnost údajů.",
        ],
        "Přednostně upravíme analýzu a zároveň prověříme, zda některé údaje nechybějí.",
        "cs-corrective-contrast-c1",
    ),
    AssessmentQuestion(
        "cs-g-c1-006",
        "grammar",
        "C1",
        "V zápisu stojí: „Rada odložila projednání rozpočtu, což zkomplikovalo přípravu "
        "zakázky.“ Co zápis uvádí jako okolnost, která přípravu zkomplikovala?",
        [
            "Samotný návrh rozpočtu, jehož obsah rada označila za nevyhovující.",
            "Projednání rozpočtu, při němž rada změnila rozsah připravované zakázky.",
            "Přípravu zakázky, kterou rada přesunula na pozdější jednání.",
            "Skutečnost, že rada přesunula jednání o rozpočtu na později.",
        ],
        "Skutečnost, že rada přesunula jednání o rozpočtu na později.",
        "cs-propositional-reference-c1",
    ),
    AssessmentQuestion(
        "cs-g-c1-007",
        "grammar",
        "C1",
        "Vedoucí říká: „Byl bych rád, kdybyste mi návrh poslala do středy.“ "
        "Do středy můžete dodat osnovu, úplnou verzi až v pátek. Chcete vymezit "
        "reálný závazek a současně navrhnout řešení. Která odpověď tomu odpovídá?",
        [
            "Do středy návrh pošlu; případné chybějící části pak vysvětlím při předání.",
            "Do středy mohu dodat osnovu, úplný text v pátek. Vyhovovalo by vám to takto?",
            "Předpokládám tedy, že středa je nezávazná a termín si mohu zvolit sama.",
            "Beru středu na vědomí a pokusím se poslat návrh podle vašeho požadavku.",
        ],
        "Do středy mohu dodat osnovu, úplný text v pátek. Vyhovovalo by vám to takto?",
        "cs-tentative-requests-c1",
    ),
    AssessmentQuestion(
        "cs-g-c1-008",
        "grammar",
        "C1",
        "Jana řekla: „Zkusím se na ten návrh v pátek mrknout, ale podrobný rozbor "
        "neslíbím.“ Který zápis zachovává její sdělení v neutrálním písemném stylu?",
        [
            "Jana v pátek návrh posoudí; termín odevzdání podrobného rozboru upřesní později.",
            "Jana do pátku rozhodne, zda návrh v následujícím týdnu podrobně posoudí.",
            "Jana se pokusí návrh v pátek zběžně projít; k podrobnému rozboru se nezavazuje.",
            "Jana v pátek dokončí stručný posudek a podrobný rozbor předá podle svých možností.",
        ],
        "Jana se pokusí návrh v pátek zběžně projít; k podrobnému rozboru se nezavazuje.",
        "cs-register-reformulation-c1",
    ),
    AssessmentQuestion(
        "cs-v-c1-001",
        "vocabulary",
        "C1",
        "Dodavatel říká: „S cenou už níž jít nemůžeme, můžeme ale jednat o splatnosti.“ "
        "Který návrh navazuje přímo na nabídnutou možnost?",
        [
            "Ponechme dobu úhrady a zkusme dohodnout nižší cenu při stejném rozsahu.",
            "Ponechme cenu i úhradu a posuňme termín dokončení prací.",
            "Ponechme cenu a prodlužme dobu, po kterou lze uplatnit vady.",
            "Ponechme cenu a dohodněme delší lhůtu k zaplacení faktury.",
        ],
        "Ponechme cenu a dohodněme delší lhůtu k zaplacení faktury.",
    ),
    AssessmentQuestion(
        "cs-v-c1-002",
        "vocabulary",
        "C1",
        "V podkladu se píše: „Nové údaje původní vysvětlení zpochybnily, zatím je však "
        "nevyvrátily.“ Jak s vysvětlením zacházet při další diskusi?",
        [
            "Používat je jako potvrzené, protože nové údaje neprokázaly jeho nesprávnost.",
            "Znovu prověřit jeho oporu a zatím je neoznačovat za prokázaně neplatné.",
            "Vyřadit je z úvah, protože zpochybnění už znamená prokázání jeho neplatnosti.",
            "Ponechat je beze změny a doplnit pouze upozornění na odlišný názor autorů.",
        ],
        "Znovu prověřit jeho oporu a zatím je neoznačovat za prokázaně neplatné.",
    ),
    AssessmentQuestion(
        "cs-v-c1-003",
        "vocabulary",
        "C1",
        "Koordinátorka žádá: „Vypořádejte také připomínku, kterou nechcete přijmout.“ "
        "Co má zpracovatel udělat, aby požadavku vyhověl?",
        [
            "Zaznamenat posouzení připomínky a vysvětlit, proč se do návrhu nepromítne.",
            "Zapracovat připomínku do návrhu a výhrady zpracovatele uvést pod čarou.",
            "Přesunout připomínku do dalšího kola, aby nyní nebyla formálně odmítnuta.",
            "Vyřadit připomínku z přehledu a ponechat pouze podněty měnící výsledný návrh.",
        ],
        "Zaznamenat posouzení připomínky a vysvětlit, proč se do návrhu nepromítne.",
    ),
    AssessmentQuestion(
        "cs-v-c1-004",
        "vocabulary",
        "C1",
        "Po kritice jedné části projektu kolega řekne: „Rád bych to uvedl na pravou míru: "
        "moje výhrada se týkala termínu, ne práce vašeho týmu.“ Jakou funkci má "
        "ustálené spojení „uvést na pravou míru“?",
        [
            "Zmírnit předchozí kritiku týmu, aniž by měnil její původní předmět.",
            "Doplnit kritiku termínu o novou výhradu k rozdělení práce v týmu.",
            "Opravit vzniklý výklad tím, že přesně vymezí předmět své výhrady.",
            "Odvolat původní výhradu a uznat, že termín byl zvolen správně.",
        ],
        "Opravit vzniklý výklad tím, že přesně vymezí předmět své výhrady.",
    ),
    AssessmentQuestion(
        "cs-r-c1-001",
        "reading",
        "C1",
        "Knihovna zavedla večerní provoz na zkoušku. V prvních šesti týdnech přibylo "
        "návštěv, současně ale ve městě probíhal festival, jehož akce knihovna hostila. "
        "Ředitelka doporučuje pokračovat v měření i po skončení festivalu. "
        "Jaký problém má další měření především pomoci vyjasnit?",
        [
            "Zda festival způsobil růst nákladů, který by znemožnil dosavadní denní provoz.",
            "Nakolik vyšší návštěvnost přetrvá i bez mimořádného programu v knihovně.",
            "Zda návštěvníci festivalu podporují trvalé převedení knihovny na večerní provoz.",
            "Nakolik se šestitýdenní zvýšení návštěvnosti promítlo do růstu počtu členů.",
        ],
        "Nakolik vyšší návštěvnost přetrvá i bez mimořádného programu v knihovně.",
    ),
    AssessmentQuestion(
        "cs-r-c1-002",
        "reading",
        "C1",
        "Obyvatelé domu chtějí klid po desáté hodině. Majitel sousední kavárny upozorňuje, "
        "že většinu tržeb má večer. Na schůzce obě strany přijaly návrh měřit hluk po dobu "
        "měsíce; o otevírací době se bude jednat až nad výsledky. "
        "Který titulek nejvěrněji vystihuje výsledek schůzky?",
        [
            "Kavárna po dobu měření zkrátí provoz, obyvatelé posoudí účinek omezení",
            "Obyvatelé přijali večerní provoz, kavárna bude sledovat jeho dopady",
            "Výsledek měření rozhodne o již dohodnutém zkrácení otevírací doby",
            "Strany dohodly sběr podkladů, konečná úprava provozu zůstává otevřená",
        ],
        "Strany dohodly sběr podkladů, konečná úprava provozu zůstává otevřená",
    ),
    AssessmentQuestion(
        "cs-r-c1-003",
        "reading",
        "C1",
        "Eva na poradě řekla: „Mohu vám umožnit nahlédnout do podkladů, rozhodnutí komise "
        "ale předjímat nemohu.“ Petr pak do návrhu zápisu napsal: „Eva přislíbila souhlas "
        "komise po kontrole podkladů.“ Jaká oprava je nutná?",
        [
            "Doplnit, že komise už souhlasila, ale Eva teprve umožní kontrolu podkladů.",
            "Uvést, že Eva převezme rozhodování od komise, jakmile budou podklady prohlédnuty.",
            "Oddělit nabídnutý přístup k podkladům od výsledku, který Eva nepřislíbila.",
            "Upřesnit, že Eva musí nejprve získat souhlas komise se samotným nahlédnutím.",
        ],
        "Oddělit nabídnutý přístup k podkladům od výsledku, který Eva nepřislíbila.",
    ),
    AssessmentQuestion(
        "cs-r-c1-004",
        "reading",
        "C1",
        "Marek připojil k e-mailu prázdný soubor. Když na chybu přišel, napsal kolegyni: "
        "„Tak takhle vypadá moje důkladná kontrola příloh. Hned posílám správnou verzi.“ "
        "Jaký postoj Marek ve zprávě vyjadřuje?",
        [
            "S nadsázkou přiznává vlastní přehlédnutí a oznamuje bezprostřední nápravu.",
            "Omlouvá vlastní chybu nedostatkem času a žádá kolegyni o kontrolu nové přílohy.",
            "Zdůrazňuje vlastní pečlivost a připisuje chybu technickému problému při odesílání.",
            "Zlehčuje dopad chyby a navrhuje odložit opravu až po společné kontrole.",
        ],
        "S nadsázkou přiznává vlastní přehlédnutí a oznamuje bezprostřední nápravu.",
    ),
]
