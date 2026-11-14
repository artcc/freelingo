"""Danish A1 grammar and introductory sound awareness."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "da-alphabet-a1",
        "Alfabetet: æ, ø og å",
        "A1",
        "Skrift og udtale",
        "Læs og stav navne og almindelige danske ord.",
        "Det danske alfabet har 29 bogstaver. Æ, ø og å står efter z og er selvstændige "
        "bogstaver. Bevar dem, når du skriver: læge, ø og år. Nogle navne skrives med aa, "
        "for eksempel Aalborg; brug den stavemåde, navnet har. Sprog, ugedage og måneder "
        "skrives normalt med lille begyndelsesbogstav.",
        rules=[
            "Øv bogstavernes navne, når du staver et navn.",
            "Skriv dansk og mandag med lille bogstav, men Danmark med stort.",
        ],
        examples=[GrammarExample("Jeg hedder Søren."), GrammarExample("Jeg lærer dansk.")],
        common_mistakes=[
            GrammarMistake(
                "Jeg taler Dansk.", "Jeg taler dansk.", "Et sprognavn er ikke et egennavn."
            )
        ],
        related=["da-sounds-a1"],
    ),
    GrammarTopic(
        "da-sounds-a1",
        "Vokaler, tryk og stød",
        "A1",
        "Skrift og udtale",
        "Lyt til hele ord; skriften viser ikke alle lydforskelle.",
        "Dansk har flere vokallyde end vokalbogstaver. Vokalens længde og lyd kan skelne ord, "
        "og æ, ø og å har ikke kun én udtale hver. Et d kan være blødt, som i mad, og et "
        "ubetonet e kan være svagt eller falde sammen med en nabolyd i almindelig tale.\n\n"
        "Stød er en særlig stemmekvalitet, ofte en kort indsnævring i stemmen, som kan "
        "skelne ord, for eksempel hun og hund i mange udtaler. Det er ikke et ekstra "
        "bogstav eller en pause mellem ord. Stød varierer med dialekt og sammenhæng; "
        "ikke alle danskere bruger det på samme måde. Lyt og efterlign korte optagelser "
        "frem for at presse stemmen eller gætte ud fra stavningen.",
        rules=[
            "Lær et nyt ord med både skrift, betydning og lyd.",
            "Øv trykket i en hel sætning; småord er ofte svagere end indholdsord.",
        ],
        examples=[
            GrammarExample("Hun har en hund.", note="Lyt til forskellen i en konkret optagelse."),
            GrammarExample("Vi spiser mad.", note="D'et i mad udtales normalt blødt."),
        ],
        related=["da-alphabet-a1"],
    ),
    GrammarTopic(
        "da-present-a1",
        "Jeg hedder, du bor, vi er",
        "A1",
        "Verber og pronomener",
        "Præsenter dig og fortæl om nuet med nutid.",
        "Personlige pronomener som subjekt er jeg, du, han, hun, den, det, vi, I og de. "
        "I skrives med stort, når det betyder flere personer, man taler til. Du er den "
        "almindelige tiltale til én person. Nutid har samme form uanset personen: jeg bor, "
        "vi bor. Mange verber får -r: tale–taler, lære–lærer. Vigtige former er være–er, "
        "have–har og gøre–gør. En almindelig dansk sætning har normalt et subjekt.",
        rules=[
            "Lær navneform og nutid sammen: hedde–hedder, bo–bor.",
            "Nutid bruges både om det, der sker nu, og om vaner.",
        ],
        examples=[
            GrammarExample("Jeg hedder Amina."),
            GrammarExample("Vi bor i Odense."),
            GrammarExample("Taler I dansk?"),
        ],
        common_mistakes=[
            GrammarMistake("Jeg være lærer.", "Jeg er lærer.", "Brug nutidsformen er.")
        ],
        related=["da-v2-a1", "da-questions-a1"],
    ),
    GrammarTopic(
        "da-gender-a1",
        "En cykel og et hus",
        "A1",
        "Navneord",
        "Lær et navneord sammen med en eller et.",
        "Danske navneord har fælleskøn eller intetkøn. Fælleskøn bruger en, og intetkøn "
        "bruger et: en cykel, et hus. Man kan ikke altid gætte kønnet. Den ubestemte artikel "
        "bruges ofte, når en enkelt ting introduceres. Ved et erhverv uden nærmere "
        "beskrivelse udelades artiklen ofte: Hun er læge.",
        rules=["Gem en eller et sammen med ordet.", "En og et kan også angive antallet én."],
        examples=[GrammarExample("Jeg har en cykel."), GrammarExample("Det er et hus.")],
        common_mistakes=[GrammarMistake("et cykel", "en cykel", "Cykel er fælleskøn.")],
        related=["da-definite-a1", "da-plural-a1"],
    ),
    GrammarTopic(
        "da-definite-a1",
        "Cyklen og huset",
        "A1",
        "Navneord",
        "Tal om en ting, som den anden kan identificere.",
        "Uden et tillægsord foran navneordet sættes den bestemte artikel normalt på som "
        "endelse: en cykel–cyklen, en bil–bilen, et hus–huset, et æble–æblet. "
        "Bestemt form bruges, når det er klart, hvilken ting man mener. Brug ikke en "
        "ekstra artikel foran i denne enkle konstruktion. Udtryk med tillægsord som "
        "den røde cykel har et andet mønster, som behandles senere.",
        rules=[
            "Lær hele parret: en nøgle–nøglen.",
            "Bestemt form afhænger af sammenhængen, ikke kun af en tidligere omtale.",
        ],
        examples=[
            GrammarExample("Jeg har en cykel. Cyklen er blå."),
            GrammarExample("Luk døren, tak."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Det huset er stort.",
                "Huset er stort.",
                "Et almindeligt navneord uden tillægsord får her kun endelsen.",
            )
        ],
        related=["da-gender-a1", "da-definite-adjectives-a2"],
    ),
    GrammarTopic(
        "da-plural-a1",
        "Flere ting: stole, cykler og huse",
        "A1",
        "Navneord",
        "Genkend almindelige former i flertal.",
        "Flertal dannes på flere måder: en stol–stole, en cykel–cykler, et hus–huse "
        "og en sko–sko. Nogle ord skifter vokal: en bog–bøger, et barn–børn. "
        "Bestemt flertal ender ofte på -ne eller -ene: stolene, cyklerne, husene, "
        "skoene, bøgerne og børnene. Lær formerne sammen; kønnet alene bestemmer "
        "ikke flertalsformen.",
        rules=[
            "Brug flertal efter to, tre og andre antal over én.",
            "Lær en bog, bogen, bøger, bøgerne.",
        ],
        examples=[GrammarExample("Vi har tre stole."), GrammarExample("Børnene er hjemme.")],
        common_mistakes=[GrammarMistake("to barn", "to børn", "Barn har uregelmæssigt flertal.")],
        related=["da-gender-a1", "da-definite-a1"],
    ),
    GrammarTopic(
        "da-possessives-a1",
        "Min, mit og mine",
        "A1",
        "Pronomener",
        "Fortæl, hvem noget tilhører.",
        "Min, din og vores kan vise ejerskab eller tilknytning. Min og din bøjes efter "
        "det, der ejes: min cykel, mit hus, mine bøger; din cykel, dit hus, dine bøger. "
        "Hans, hendes, vores og jeres har samme form foran en-ord, et-ord og flertal. "
        "Efter disse ord står navneordet i ubestemt form.",
        rules=[
            "Det ejede navneords køn bestemmer min eller mit.",
            "Brug mine og dine ved flertal, uanset navneordets køn.",
        ],
        examples=[GrammarExample("Hvor er mine nøgler?"), GrammarExample("Det er vores køkken.")],
        common_mistakes=[
            GrammarMistake("min cyklen", "min cykel", "Brug ubestemt navneord efter min.")
        ],
        related=["da-gender-a1", "da-reflexive-possessive-a2"],
    ),
    GrammarTopic(
        "da-adjectives-a1",
        "En stor taske og et stort bord",
        "A1",
        "Tillægsord",
        "Beskriv enkle egenskaber og tilpas formen.",
        "Mange tillægsord har en grundform til en-ord, en t-form til et-ord og en e-form "
        "til flertal: stor, stort, store. Det gælder både foran navneordet og efter er: "
        "et stort bord; bordet er stort. Nogle ord har særlige former: en god dag, "
        "et godt svar, gode venner. Andre ændres ikke, for eksempel moderne.",
        rules=[
            "Lær almindelige former sammen: ny–nyt–nye.",
            "Flertalsformen afhænger ikke af, om navneordet er fælleskøn eller intetkøn.",
        ],
        examples=[GrammarExample("Huset er stort."), GrammarExample("Vi har to nye stole.")],
        common_mistakes=[
            GrammarMistake(
                "et stor bord", "et stort bord", "Bord er et-ord og kræver her t-formen."
            )
        ],
        related=["da-gender-a1", "da-definite-adjectives-a2"],
    ),
    GrammarTopic(
        "da-v2-a1",
        "Verbet som andet led",
        "A1",
        "Ordstilling",
        "Begynd et udsagn med en person, en tid eller et sted.",
        "I en almindelig fremsættende hovedsætning står det bøjede verbum som andet led. "
        "Det første led kan bestå af flere ord: Om morgenen drikker jeg te. "
        "Når tiden eller stedet kommer først, står subjektet efter verbet. "
        "Andet led betyder ikke andet skrevet ord.",
        rules=[
            "Jeg arbejder i dag. I dag arbejder jeg.",
            "Ved to verber er det kun det bøjede verbum, der står som andet led.",
        ],
        examples=[
            GrammarExample("Om aftenen læser vi."),
            GrammarExample("Her bor min søster."),
        ],
        common_mistakes=[
            GrammarMistake(
                "I dag jeg arbejder.",
                "I dag arbejder jeg.",
                "Tidsleddet står først, så arbejder kommer før jeg.",
            )
        ],
        related=["da-present-a1", "da-negation-a1"],
    ),
    GrammarTopic(
        "da-questions-a1",
        "Hvad, hvor, hvem og hvornår",
        "A1",
        "Ordstilling",
        "Stil korte spørgsmål om hverdagen.",
        "Et ja-nej-spørgsmål begynder normalt med verbet: Bor du her? Et spørgeled "
        "kommer foran verbet: Hvor bor du? Hvad spørger om en ting eller handling, "
        "hvem om en person, hvor om et sted, hvornår om tid og hvordan om en måde. "
        "Når hvem selv er subjekt, indsættes ikke et ekstra subjekt: Hvem kommer?",
        rules=[
            "Hvor gammel er du? spørger om alder.",
            "Hvor meget koster det? spørger om en pris.",
        ],
        examples=[
            GrammarExample("Hvornår åbner butikken?"),
            GrammarExample("Har du en billet?"),
            GrammarExample("Hvem bor her?"),
        ],
        related=["da-v2-a1"],
    ),
    GrammarTopic(
        "da-negation-a1",
        "Ikke i hovedsætninger",
        "A1",
        "Ordstilling",
        "Sig, at noget ikke gælder.",
        "I en enkel hovedsætning med subjektet først står ikke efter det bøjede verbum: "
        "Jeg drikker ikke kaffe. Med et hjælpeverbum kommer ikke mellem de to verber: "
        "Jeg kan ikke komme. Når et tidsled står først, står ikke normalt efter subjektet: "
        "I dag arbejder jeg ikke. Ledsætninger har et andet grundmønster.",
        rules=[
            "Brug jeg er ikke, jeg har ikke og jeg kan ikke som korte mønstre.",
            "Et negativt svar kan udbygges: Nej, jeg bor ikke her.",
        ],
        examples=[GrammarExample("Hun er ikke hjemme."), GrammarExample("Vi spiser ikke kød.")],
        common_mistakes=[
            GrammarMistake(
                "Jeg ikke drikker kaffe.",
                "Jeg drikker ikke kaffe.",
                "I denne hovedsætning står ikke efter det bøjede verbum.",
            )
        ],
        related=["da-v2-a1", "da-modals-a1"],
    ),
    GrammarTopic(
        "da-numbers-time-a1",
        "Tal, priser og klokken",
        "A1",
        "Tal og tid",
        "Forstå danske tal og almindelige klokkeslæt.",
        "Grundtallene er nul, en/et, to, tre, fire, fem, seks, syv, otte, ni og ti. "
        "Derefter kommer elleve, tolv, tretten, fjorten, femten, seksten, sytten, atten, "
        "nitten og tyve. Lær derefter tierne: tredive, fyrre, halvtreds, tres, halvfjerds, "
        "firs og halvfems. Fra 21 nævnes eneren før tieren: enogtyve, toogtredive, "
        "syvoghalvtreds. Lær de høje tiere som hele ord; halvtreds betyder 50, "
        "ikke 30. Hundrede betyder 100.\n\nKlokken halv otte er 7.30. Kvart over "
        "syv er 7.15, og kvart i otte er 7.45. Digitale tider kan læses direkte: "
        "sytten tredive er 17.30. Sig om morgenen eller om aftenen, når det er nødvendigt.",
        rules=[
            "Skriv sammensatte tal som ét ord: femogtyve.",
            "Spørg Hvad er klokken? om tiden nu og Hvornår? om en aftale.",
        ],
        examples=[
            GrammarExample("Det koster nioghalvtreds kroner."),
            GrammarExample("Vi mødes klokken halv otte om aftenen."),
        ],
        related=["da-questions-a1"],
    ),
    GrammarTopic(
        "da-modals-a1",
        "Kan, vil, skal og må",
        "A1",
        "Verber",
        "Udtryk mulighed, ønske, plan og tilladelse.",
        "Efter kan, vil, skal og må bruges navneform uden at. Kan udtrykker blandt andet "
        "evne og mulighed. Vil gerne bruges om et ønske, og skal bruges blandt andet "
        "om en plan eller en forpligtelse. Må kan handle om tilladelse: Må jeg sidde her? "
        "Må ikke betyder i denne brug, at noget er forbudt, mens behøver ikke betyder, "
        "at noget ikke er nødvendigt. Betydningen afhænger altid af sammenhængen.",
        rules=[
            "Brug vil gerne have, når du bestiller noget.",
            "Sæt ikke at mellem modalverbet og navneformen.",
        ],
        examples=[
            GrammarExample("Jeg vil gerne have en bolle."),
            GrammarExample("Kan du hjælpe mig?"),
            GrammarExample("Vi skal mødes klokken ti."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Jeg kan at svømme.", "Jeg kan svømme.", "Kan følges af navneform uden at."
            )
        ],
        related=["da-objects-a1", "da-negation-a1"],
    ),
    GrammarTopic(
        "da-quantity-a1",
        "Meget, mange, lidt og få",
        "A1",
        "Mængde og antal",
        "Tal om en mængde eller et antal.",
        "Mange og få bruges med tællelige navneord i flertal: mange æbler, få kunder. "
        "Meget og lidt bruges med en mængde, der ikke tælles direkte: meget vand, lidt "
        "mælk. En kop, et glas og et kilo gør mængden målbar: to kopper kaffe, et kilo "
        "kartofler. Nogle navneord kan både tælles og betegne en mængde i forskellige situationer.",
        rules=["Spørg Hvor mange æbler? men Hvor meget vand?", "Brug antal foran måleenheden."],
        examples=[GrammarExample("Jeg køber lidt ost."), GrammarExample("Vi har mange æg.")],
        common_mistakes=[
            GrammarMistake("mange vand", "meget vand", "Vand beskrives her som en mængde.")
        ],
        related=["da-plural-a1", "da-numbers-time-a1"],
    ),
    GrammarTopic(
        "da-objects-a1",
        "Mig, dig, ham og hende",
        "A1",
        "Pronomener",
        "Brug personlige pronomener som objekt.",
        "Subjektsformerne jeg, du, han, hun, vi, I og de har objektformerne mig, dig, "
        "ham, hende, os, jer og dem. Objektformen bruges blandt andet efter et verbum, "
        "når personen modtager handlingen, og efter forholdsord: Hun hjælper mig; "
        "en gave til dig. Den og det har samme form som subjekt og objekt.",
        rules=[
            "Skeln mellem Jeg hjælper og Hun hjælper mig.",
            "Efter til og med bruges objektform: til os, med dem.",
        ],
        examples=[GrammarExample("Kan du hjælpe os?"), GrammarExample("Kaffen er til hende.")],
        common_mistakes=[
            GrammarMistake(
                "Han hjælper jeg.", "Han hjælper mig.", "Personen er objekt, ikke subjekt."
            )
        ],
        related=["da-present-a1", "da-modals-a1"],
    ),
    GrammarTopic(
        "da-place-a1",
        "Hvor er du, og hvor går du hen?",
        "A1",
        "Sted og retning",
        "Beskriv en placering og en bevægelse.",
        "I, på, under, over, foran og bagved forbinder en ting med et sted. Lær faste "
        "forbindelser i sammenhæng: i køkkenet, på stationen, på arbejde. Hjemme, inde "
        "og ude angiver ophold; hjem, ind og ud angiver ofte retning. Her og der bruges "
        "om steder, og hen kan gøre en retning tydelig: Hvor går du hen?",
        rules=[
            "Jeg er hjemme beskriver ophold; jeg går hjem beskriver bevægelse.",
            "Brug ikke én oversat regel til alle forbindelser med i og på.",
        ],
        examples=[
            GrammarExample("Nøglen ligger på bordet."),
            GrammarExample("Vi går ind. Nu er vi inde."),
        ],
        related=["da-questions-a1", "da-existential-a1"],
    ),
    GrammarTopic(
        "da-existential-a1",
        "Der er og det er",
        "A1",
        "Sætningsmønstre",
        "Fortæl, at noget findes, eller identificer det.",
        "Der er introducerer ofte noget på et sted: Der er et apotek ved stationen. "
        "Det er identificerer eller beskriver noget i situationen: Hvad er det? Det er "
        "et apotek. I spørgsmålet Er der en bus? spørger man, om en bus findes eller "
        "er til rådighed. Er det bussen? spørger til noget bestemt, man kan se eller omtaler.",
        rules=[
            "Brug der er med både ental og flertal.",
            "Når et sted står først: Ved stationen er der et apotek.",
        ],
        examples=[
            GrammarExample("Der er to stole i køkkenet."),
            GrammarExample("Er der et toilet her?"),
        ],
        related=["da-v2-a1", "da-place-a1"],
    ),
    GrammarTopic(
        "da-coordination-a1",
        "Og, men, eller og for",
        "A1",
        "Sammenbinding",
        "Forbind korte udsagn og giv en enkel begrundelse.",
        "Og føjer noget til, men viser en modsætning, og eller giver et valg. For kan "
        "indføre en begrundelse i en ny hovedsætning: Jeg bliver hjemme, for jeg er træt. "
        "Efter for bevares hovedsætningens ordstilling, også med ikke. To udsagn kan "
        "have samme subjekt: Jeg læser og skriver.",
        rules=[
            "Vælg forbindelsen efter betydningen, ikke kun efter sætningslængden.",
            "Efter for: Jeg kommer ikke, for jeg har ikke tid.",
        ],
        examples=[
            GrammarExample("Vil du have te eller kaffe?"),
            GrammarExample("Jeg vil gerne med, men jeg skal arbejde."),
        ],
        related=["da-negation-a1", "da-subordinate-a2"],
    ),
    GrammarTopic(
        "da-imperative-a1",
        "Vent, kom og læs",
        "A1",
        "Verber",
        "Forstå korte instruktioner og gør en anmodning venlig.",
        "Bydeform bruges i instruktioner og opfordringer. Formen er ofte verbets stamme: "
        "vente–vent, komme–kom, læse–læs. Verber som gå og se beholder formen. Subjektet "
        "du står normalt ikke med. En bydeform kan lyde direkte; tone, tak og "
        "en spørgende formulering gør en forskel i situationen.",
        rules=[
            "En negativ instruktion kan begynde med Lad være med at: Lad være med at løbe.",
            "Kan du vente lidt? er en almindelig venlig anmodning.",
        ],
        examples=[
            GrammarExample("Vent her, tak."),
            GrammarExample("Læs beskeden og skriv dit navn."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Venter her, tak.",
                "Vent her, tak.",
                "En direkte instruktion bruger bydeform, ikke nutid.",
            )
        ],
        related=["da-modals-a1"],
    ),
    GrammarTopic(
        "da-past-a1",
        "I går var jeg hjemme",
        "A1",
        "Verber",
        "Fortæl kort om en afsluttet dag.",
        "Datid bruges til at fortælle om noget på et afsluttet tidspunkt. Begynd med "
        "hyppige former: er–var, har–havde, går–gik, gør–gjorde og køber–købte. "
        "Formen er den samme for alle personer. Et indledende tidsled ændrer ikke "
        "reglen om verbet som andet led: I går købte jeg brød.",
        rules=[
            "Lær formen sammen med et kort udsagn om i går.",
            "Når en fortidig ramme er tydelig, behøver hver sætning ikke et nyt tidsord.",
        ],
        examples=[
            GrammarExample("I går var jeg på arbejde."),
            GrammarExample("Vi gik hjem klokken fem."),
            GrammarExample("Hun havde ikke tid."),
        ],
        related=["da-v2-a1", "da-past-a2"],
    ),
]
