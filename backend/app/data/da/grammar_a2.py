"""Danish A2 grammar for narration, descriptions and practical messages."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "da-past-a2",
        "Datid i en fortælling",
        "A2",
        "Verber",
        "Fortæl om flere hændelser i en afsluttet situation.",
        "Regelmæssige verber har blandt andet datid på -ede eller -te: arbejde–arbejdede, "
        "vente–ventede, købe–købte, høre–hørte. Andre skifter vokal eller har særlige "
        "former: skrive–skrev, tage–tog, være–var. Lær de hyppige former med navneformen. "
        "Datid angiver et fortidigt perspektiv; det er ikke i sig selv en kort handling.",
        rules=[
            "Brug en tydelig ramme som sidste sommer eller i går.",
            "Først, så og bagefter hjælper læseren med rækkefølgen.",
        ],
        examples=[
            GrammarExample("Først tog vi toget til Roskilde. Bagefter besøgte vi museet."),
            GrammarExample("Vi ventede på bussen i tyve minutter."),
        ],
        related=["da-past-a1", "da-perfect-a2"],
    ),
    GrammarTopic(
        "da-perfect-a2",
        "Førnutid med har og er",
        "A2",
        "Verber",
        "Forbind en tidligere hændelse med situationen nu.",
        "Førnutid dannes med har eller er og kort tillægsform: har købt, har spist, "
        "er kommet, er blevet. Har bruges ved mange handlinger og tilstande. Er bruges "
        "blandt andet ved flere verber om overgang eller bevægelse til en ny tilstand "
        "eller et nyt sted: Hun er gået hjem. Valget afhænger af verbets brug, ikke kun "
        "af om noget bevæger sig: Hun har gået fem kilometer beskriver aktiviteten.\n\n"
        "Jeg har boet her i to år betyder normalt, at jeg stadig bor her. Jeg boede "
        "der i 2022 placerer opholdet i en afsluttet fortidig ramme.",
        rules=[
            "Lær hjælpeverbum og kort tillægsform som en forbindelse.",
            "Brug ikke datidsformen efter har: har skrevet, ikke har skrev.",
        ],
        examples=[
            GrammarExample("Har du været på Bornholm?"),
            GrammarExample("Toget er lige ankommet."),
            GrammarExample("Jeg har allerede købt billetter."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Jeg har spiste.", "Jeg har spist.", "Efter har bruges kort tillægsform."
            )
        ],
        related=["da-past-a2"],
    ),
    GrammarTopic(
        "da-future-a2",
        "Planer og forventninger",
        "A2",
        "Verber",
        "Tal om det, der skal eller forventes at ske.",
        "Nutid med en tidsangivelse kan beskrive fremtid: Færgen sejler i morgen. "
        "Skal bruges ofte om en plan, aftale eller forpligtelse. Vil kan udtrykke "
        "vilje eller en forventning. Kommer til at bruges blandt andet om en forventet "
        "udvikling: Det kommer til at tage en time. Formerne kan overlappe, så en "
        "bestemt fremtidsform er ikke altid den eneste mulige.",
        rules=[
            "Efter skal og vil står navneform uden at.",
            "Efter kommer til står at foran navneformen.",
        ],
        examples=[
            GrammarExample("Vi skal besøge min bror på søndag."),
            GrammarExample("Jeg tager bussen i morgen."),
            GrammarExample("Det kommer til at regne i aften."),
        ],
        related=["da-modals-a1"],
    ),
    GrammarTopic(
        "da-definite-adjectives-a2",
        "Den røde cykel og det nye køkken",
        "A2",
        "Tillægsord og bestemthed",
        "Beskriv noget bestemt uden dobbelt bestemthed.",
        "Når et tillægsord står foran et bestemt navneord, bruges normalt den, det "
        "eller de, tillægsordets e-form og navneordets ubestemte form: den røde cykel, "
        "det nye køkken, de store vinduer. Dansk bruger altså ikke samtidig en bestemt "
        "endelse på navneordet i denne konstruktion. Efter et ejestedord bruges også "
        "e-form og ubestemt navneord: min røde cykel.",
        rules=[
            "Uden tillægsord: cyklen. Med tillægsord: den røde cykel.",
            "Lille har særlige former: den lille taske, de små tasker.",
        ],
        examples=[
            GrammarExample("Det gamle køleskab larmer."),
            GrammarExample("Vores nye nabo er venlig."),
        ],
        common_mistakes=[
            GrammarMistake(
                "den røde cyklen",
                "den røde cykel",
                "Den står foran tillægsordet; navneordet får ikke bestemt endelse her.",
            )
        ],
        related=["da-definite-a1", "da-adjectives-a1", "da-possessives-a1"],
    ),
    GrammarTopic(
        "da-comparison-a2",
        "Billigere end og lige så stor som",
        "A2",
        "Tillægsord",
        "Sammenlign to muligheder.",
        "Mange tillægsord får -ere i højere grad: billig–billigere, hurtig–hurtigere. "
        "Andre har uregelmæssige former: god–bedre, stor–større, lille–mindre. "
        "Længere tillægsord bruger ofte mere: mere praktisk. End bruges ved forskel, "
        "og lige så ... som ved samme grad.",
        rules=[
            "Sammenlign samme egenskab i en tydelig sammenhæng.",
            "Brug ikke både mere og -ere i en almindelig sammenligning.",
        ],
        examples=[
            GrammarExample("Denne lejlighed er billigere end den anden."),
            GrammarExample("Køkkenet er lige så stort som vores."),
        ],
        common_mistakes=[
            GrammarMistake(
                "mere billigere", "billigere", "Endelsen -ere udtrykker allerede højere grad."
            )
        ],
        related=["da-superlative-a2", "da-adjectives-a1"],
    ),
    GrammarTopic(
        "da-superlative-a2",
        "Den billigste og det bedste",
        "A2",
        "Tillægsord",
        "Udpeg en mulighed inden for en gruppe.",
        "Højeste grad dannes ofte med -st eller -est: billigst, hurtigst. Andre former "
        "er bedst, størst og mindst, eller forbindelser med mest: mest praktisk. "
        "Foran et bestemt navneord får mange former -e: den billigste bolig, det "
        "største rum. Gruppen skal være klar, for eksempel tre boliger, man sammenligner.",
        rules=[
            "Billigere sammenligner; billigst udpeger den laveste pris i gruppen.",
            "Efter er uden navneord: Denne bolig er billigst.",
        ],
        examples=[
            GrammarExample("Det er det bedste tilbud af de tre."),
            GrammarExample("Hvilket værelse er størst?"),
        ],
        related=["da-comparison-a2", "da-definite-adjectives-a2"],
    ),
    GrammarTopic(
        "da-genitive-a2",
        "Naboens nøgle og Mads' cykel",
        "A2",
        "Navneord",
        "Vis tilhørsforhold med genitiv.",
        "Genitiv dannes normalt med -s: naboens nøgle, Annas cykel. Efter en genitiv "
        "står navneordet i ubestemt form. Navne, der allerede ender på s, x eller z, "
        "får normalt kun en apostrof: Mads' cykel. Brug ikke apostrof foran det "
        "almindelige danske genitiv-s.",
        rules=[
            "Skriv Annas, ikke Anna's.",
            "Et tillægsord efter genitiv står normalt i e-form: naboens nye bil.",
        ],
        examples=[
            GrammarExample("Udlejerens nummer står i kontrakten."),
            GrammarExample("Mads' værelse er mindre end Annas."),
        ],
        related=["da-possessives-a1", "da-definite-adjectives-a2"],
    ),
    GrammarTopic(
        "da-subordinate-a2",
        "At, fordi og når",
        "A2",
        "Ordstilling",
        "Giv en forklaring i en ledsætning.",
        "En ledsætning kan begynde med at, fordi eller når. I det almindelige "
        "ledsætningsmønster kommer subjektet før et sætningsadverbial som ikke og "
        "derefter det bøjede verbum: fordi jeg ikke kan komme. Sammenlign "
        "hovedsætningen Jeg kan ikke komme. At kan indføre en oplysning; fordi en "
        "årsag; når et tidspunkt eller en gentagen situation.",
        structure="Indleder + subjekt + ikke + bøjet verbum",
        rules=[
            "At foran en hel ledsætning er ikke det samme som at foran en navneform.",
            "Brug her det neutrale ledsætningsmønster; talesprog kan have andre mønstre.",
        ],
        examples=[
            GrammarExample("Jeg ringer, fordi jeg ikke kan komme."),
            GrammarExample("Hun siger, at hun har feber."),
        ],
        common_mistakes=[
            GrammarMistake(
                "fordi jeg ikke komme kan",
                "fordi jeg ikke kan komme",
                "Efter ikke kommer det bøjede modalverbum kan før navneformen komme.",
            )
        ],
        related=["da-negation-a1", "da-initial-clause-a2"],
    ),
    GrammarTopic(
        "da-initial-clause-a2",
        "Når ledsætningen står først",
        "A2",
        "Ordstilling",
        "Begynd med en tid eller en årsag.",
        "En hel ledsætning kan stå som første led i en hovedsætning. Derefter kommer "
        "hovedsætningens bøjede verbum før subjektet: Når jeg kommer hjem, laver jeg mad. "
        "Ledsætningen beholder sin egen ordstilling. Man tæller hele ledsætningen som "
        "ét led, uanset hvor mange ord den indeholder.",
        rules=[
            "Efter en indledende ledsætning: bøjet verbum + subjekt.",
            "Bevar ikke før verbet inde i den neutrale ledsætning.",
        ],
        examples=[
            GrammarExample("Når jeg ikke har det godt, bliver jeg hjemme."),
            GrammarExample("Fordi bussen er forsinket, kommer jeg lidt senere."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Når jeg kommer hjem, jeg laver mad.",
                "Når jeg kommer hjem, laver jeg mad.",
                "Hele når-ledsætningen står på hovedsætningens første plads.",
            )
        ],
        related=["da-subordinate-a2", "da-v2-a1"],
    ),
    GrammarTopic(
        "da-reflexive-a2",
        "Jeg skynder mig, hun skynder sig",
        "A2",
        "Pronomener og verber",
        "Brug almindelige refleksive forbindelser.",
        "Nogle verber bruges med et pronomen, der peger tilbage på subjektet: "
        "skynde sig, sætte sig, glæde sig. Formen følger personen: jeg skynder mig, "
        "du skynder dig, hun skynder sig, vi skynder os, I skynder jer, de skynder sig. "
        "Lær hele forbindelsen, da betydningen ikke altid kan udledes af verbet alene.",
        rules=[
            "Sig bruges ved tredje person, både ental og flertal.",
            "Han vasker sig og Han vasker ham har forskellige deltagere.",
        ],
        examples=[
            GrammarExample("Jeg føler mig træt."),
            GrammarExample("Sæt dig her, tak."),
            GrammarExample("De glæder sig til ferien."),
        ],
        related=["da-objects-a1", "da-reflexive-possessive-a2"],
    ),
    GrammarTopic(
        "da-reflexive-possessive-a2",
        "Sin, sit og sine",
        "A2",
        "Pronomener",
        "Skeln mellem subjektets egne ting og en andens.",
        "Sin, sit og sine viser normalt tilbage til subjektet i samme sætning, når "
        "subjektet er tredje person ental: Sara ringer til sin læge. Hans og hendes "
        "viser her til en anden person: Sara ringer til hendes læge betyder i denne "
        "sammenhæng en anden kvindes læge. Formen bestemmes af det ejede: sin taske, "
        "sit kort, sine nøgler. Ved flertal som subjekt bruges deres: Børnene tager "
        "deres tasker. Min, din og vores skifter ikke til sin.",
        rules=[
            "Brug ikke sin inde i selve subjektet: Hendes læge ringer, ikke Sin læge ringer.",
            "Find subjektet og den, der ejer tingen, før du vælger form.",
        ],
        examples=[
            GrammarExample("Jonas tager sit sundhedskort med."),
            GrammarExample("Jonas og Lea tager deres sundhedskort med."),
        ],
        related=["da-possessives-a1", "da-reflexive-a2"],
    ),
    GrammarTopic(
        "da-relative-a2",
        "En kollega som hjælper",
        "A2",
        "Ledsætninger",
        "Tilføj en kort beskrivelse af en person eller ting.",
        "En relativsætning kan knytte en beskrivelse til et navneord: en kollega, som "
        "arbejder om aftenen. Som kan være subjekt eller objekt. Der bruges også som "
        "relativt subjekt: en kollega, der arbejder om aftenen. Når personen eller "
        "tingen er objekt, bruges ikke der alene: bogen, som jeg læser. Som kan "
        "udelades i denne sidste konstruktion: bogen, jeg læser.",
        rules=[
            "Når som eller der er subjekt, tilføjes ikke et ekstra han eller den.",
            "Brug ledsætningsordstilling: en opgave, som jeg ikke forstår.",
        ],
        examples=[
            GrammarExample("Jeg kender en lærer, der taler arabisk."),
            GrammarExample("Her er den opgave, som vi skal lave."),
        ],
        related=["da-subordinate-a2"],
    ),
    GrammarTopic(
        "da-indirect-question-a2",
        "Ved du, hvornår mødet begynder?",
        "A2",
        "Spørgsmål og ledsætninger",
        "Indbyg et spørgsmål i en anden sætning.",
        "Et indirekte spørgsmål har ledsætningsordstilling: Hvornår begynder mødet? "
        "bliver til Ved du, hvornår mødet begynder? Et ja-nej-spørgsmål indledes med om: "
        "Ved du, om mødet er aflyst? Når hvem er subjekt, bruges normalt der: "
        "Ved du, hvem der kommer? Hele sætningen kan være et spørgsmål eller et udsagn.",
        rules=[
            "Byt ikke om på subjekt og verbum inde i det indirekte spørgsmål.",
            "Brug om, når det oprindelige spørgsmål ikke har et spørgeord.",
        ],
        examples=[
            GrammarExample("Kan du fortælle mig, hvor lokalet ligger?"),
            GrammarExample("Jeg ved ikke, om kurset starter i dag."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ved du, hvornår starter kurset?",
                "Ved du, hvornår kurset starter?",
                "Det indbyggede spørgsmål har subjektet før verbet.",
            )
        ],
        related=["da-questions-a1", "da-subordinate-a2"],
    ),
    GrammarTopic(
        "da-infinitive-a2",
        "At lære og for at forstå",
        "A2",
        "Verber",
        "Forbind to handlinger og forklar et formål.",
        "Mange verber forbindes med at og navneform: prøve at skrive, begynde at "
        "arbejde, huske at ringe. Modalverber følger et andet mønster: kan skrive, "
        "skal ringe. For at kan forklare formålet med en handling, når den samme "
        "person typisk udfører begge handlinger: Jeg spørger for at forstå opgaven.",
        rules=[
            "Lær forbindelsen sammen med verbet; at bruges ikke efter alle verber.",
            "Efter at som navneformsmærke står en ubøjet form, ikke nutid.",
        ],
        examples=[
            GrammarExample("Jeg prøver at finde filen."),
            GrammarExample("Vi mødes for at planlægge næste uge."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Jeg prøver at skriver.", "Jeg prøver at skrive.", "Efter at bruges navneform."
            )
        ],
        related=["da-modals-a1"],
    ),
    GrammarTopic(
        "da-time-prepositions-a2",
        "I to dage, om to dage og for to dage siden",
        "A2",
        "Tid",
        "Skeln mellem varighed, fremtid og fortidig afstand.",
        "I to dage beskriver en varighed. Om to dage peger frem fra nu. For to dage "
        "siden peger tilbage fra nu. Siden kan angive et startpunkt: Jeg har boet her "
        "siden marts. På to timer kan angive den tid, en afsluttet opgave kræver. "
        "Valget afhænger af, om man beskriver et forløb, et tidspunkt eller et resultat.",
        rules=[
            "Sammenlign Jeg ventede i en time og Jeg er tilbage om en time.",
            "Brug for ... siden som en samlet forbindelse.",
        ],
        examples=[
            GrammarExample("Jeg købte jakken for tre dage siden."),
            GrammarExample("Pakken kommer om to dage."),
            GrammarExample("Hun samlede reolen på en time."),
        ],
        related=["da-perfect-a2", "da-past-a2"],
    ),
    GrammarTopic(
        "da-indefinite-a2",
        "Nogen, noget, nogle og ingen",
        "A2",
        "Pronomener og mængde",
        "Tal om ubestemte personer, ting og antal.",
        "Nogle bruges ofte om et ubestemt antal i positive udsagn: Jeg har nogle "
        "spørgsmål. Nogen bruges ofte i spørgsmål og nægtelser: Har du nogen "
        "spørgsmål? Jeg har ikke nogen spørgsmål. Noget bruges blandt andet om en "
        "ubestemt ting eller mængde: noget mad. Ingen og intet udtrykker fravær: "
        "ingen beskeder, intet svar. Nogen alene kan betyde en ubestemt person.",
        rules=[
            "Har du nogle spørgsmål? kan også være muligt, især når man forventer nogle.",
            "Undgå at gøre nogen og nogle til en regel uden hensyn til betydningen.",
        ],
        examples=[
            GrammarExample("Er der nogen hjemme?"),
            GrammarExample("Jeg har købt nogle kopper."),
            GrammarExample("Der er ikke noget papir."),
        ],
        related=["da-quantity-a1", "da-negation-a1"],
    ),
    GrammarTopic(
        "da-adverbs-a2",
        "Tydelig og tydeligt",
        "A2",
        "Tillægsord og biord",
        "Beskriv, hvordan en handling udføres.",
        "Et tillægsord beskriver et navneord: en tydelig besked. Et biord kan beskrive "
        "en handling: Hun taler tydeligt. Mange mådesbiord dannes med -t, men ikke "
        "alle biord dannes af tillægsord: gerne og ofte læres som selvstændige ord. "
        "God har formen godt som mådesbiord: Hun synger godt. Den samme t-form kan "
        "være et tillægsord ved et-ord eller et biord.",
        rules=[
            "Find ud af, om ordet beskriver en ting eller selve handlingen.",
            "Lær hyppige forbindelser: lytte godt, tale langsomt, svare venligt.",
        ],
        examples=[
            GrammarExample("Han skriver tydeligt på tavlen."),
            GrammarExample("Det er et tydeligt svar."),
        ],
        related=["da-adjectives-a1"],
    ),
    GrammarTopic(
        "da-reciprocal-a2",
        "Vi hjælper hinanden og ses på fredag",
        "A2",
        "Verber og pronomener",
        "Beskriv gensidig kontakt.",
        "Hinanden viser, at flere personer gør noget gensidigt: De hjælper hinanden. "
        "Nogle almindelige verber har en s-form med gensidig betydning: mødes, ses, "
        "skændes. Vi ses på fredag er en fast måde at aftale eller bekræfte et møde på. "
        "En s-form er derfor ikke altid passiv; lær verbets betydning i sammenhæng.",
        rules=[
            "Vi kender hinanden beskriver et gensidigt forhold.",
            "Tilføj et tidspunkt eller sted, når mødes bruges til en aftale.",
        ],
        examples=[
            GrammarExample("Vi mødes foran biblioteket."),
            GrammarExample("Deltagerne hjælper hinanden med opgaven."),
        ],
        related=["da-objects-a1", "da-passive-a2"],
    ),
    GrammarTopic(
        "da-passive-a2",
        "Døren lukkes, og pakken bliver sendt",
        "A2",
        "Verber",
        "Genkend passiv i almindelige beskeder.",
        "Passiv sætter en handling og det, handlingen rammer, i centrum frem for den, "
        "der udfører den. På skilte og i regler møder man ofte s-passiv: Døren lukkes "
        "klokken 18. Blive-passiv består af bliver og kort tillægsform: Pakken bliver "
        "sendt i morgen. Den handlende kan tilføjes med af, hvis det er relevant. "
        "Begynd med at forstå de hyppige formuleringer; de to passive former kan overlappe.",
        rules=[
            "Efter kan bruges ofte s-passiv: Billetten kan købes her.",
            "Ses og mødes kan være gensidige verber, så et slut-s er ikke nok til at kende passiv.",
        ],
        examples=[
            GrammarExample("Affaldet bliver hentet på tirsdag."),
            GrammarExample("Døren skal holdes lukket."),
        ],
        related=["da-reciprocal-a2", "da-perfect-a2"],
    ),
    GrammarTopic(
        "da-condition-a2",
        "Hvis det ikke virker",
        "A2",
        "Ledsætninger",
        "Aftal, hvad der sker under en bestemt betingelse.",
        "Hvis indleder en betingelse: Hvis kortet ikke virker, ringer jeg til banken. "
        "I hvis-ledsætningen står ikke normalt før det bøjede verbum. Står betingelsen "
        "først, kommer hovedsætningens verbum før subjektet. Ved en mulig fremtidig "
        "situation er nutid ofte nok; man behøver ikke sætte vil ind i begge dele.",
        rules=[
            "Hvis udtrykker en betingelse; når bruges, når situationen fremstilles som forventet.",
            "Man kan også slutte med betingelsen: Vi går en tur, hvis det holder tørt.",
        ],
        examples=[
            GrammarExample("Hvis bussen er aflyst, tager vi toget."),
            GrammarExample("Jeg sender en besked, hvis jeg bliver forsinket."),
        ],
        related=["da-subordinate-a2", "da-initial-clause-a2"],
    ),
]
