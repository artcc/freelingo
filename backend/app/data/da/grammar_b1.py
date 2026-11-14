"""Danish B1 grammar for connected everyday communication."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "da-pluperfect-b1",
        "Noget var sket før noget andet",
        "B1",
        "Tid og fortælling",
        "Placér en hændelse før et andet tidspunkt i fortiden.",
        "Førdatid dannes med havde eller var og kort tillægsform. Den viser tilbage fra "
        "et tidspunkt i fortiden. Hjælpeverbet følger normalt samme mønster som i førnutid: "
        "har pakket bliver til havde pakket, og er flyttet bliver til var flyttet. "
        "Datid fører ofte fortællingen videre, mens førdatid giver baggrunden.",
        structure="Da + grundled + datid, havde/var + grundled + kort tillægsform.",
        rules=[
            "Brug en tydelig fortidig ramme, når rækkefølgen ellers kan misforstås.",
            "Vælg hjælpeverbum efter verbets betydning og brug.",
        ],
        examples=[
            GrammarExample("Da flyttebilen kom, havde vi pakket alle kasserne."),
            GrammarExample("Hun var allerede flyttet, da jeg ringede."),
        ],
        related=["da-temporal-clauses-b1"],
    ),
    GrammarTopic(
        "da-temporal-clauses-b1",
        "Da, når og mens",
        "B1",
        "Tid og fortælling",
        "Skeln mellem en bestemt fortidig situation, gentagelse og samtidighed.",
        "Da bruges om en bestemt situation i fortiden: Da jeg flyttede til Odense, kendte "
        "jeg ingen. Når bruges blandt andet om gentagelser og fremtidige tidspunkter. "
        "Mens forbinder samtidige forløb. En tidsledsætning først i helsætningen fylder "
        "første plads, så det bøjede verbum i hovedsætningen kommer før grundleddet.",
        rules=[
            "Når jeg kom hjem fra skole, lavede jeg te beskriver en gentagen fortidig vane.",
            "En fremtidig tidsledsætning kan stå i nutid: Når jeg kommer, ringer jeg.",
        ],
        examples=[
            GrammarExample("Mens vi bar møbler op, holdt naboen døren."),
            GrammarExample("Når jeg har fri, går jeg tit ned til havnen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Da vi kom frem, vi hentede nøglen.",
                "Da vi kom frem, hentede vi nøglen.",
                "Efter den indledende ledsætning kommer hovedsætningens bøjede verbum.",
            ),
        ],
    ),
    GrammarTopic(
        "da-habits-b1",
        "Plejer at og plejede at",
        "B1",
        "Vaner",
        "Beskriv det sædvanlige uden at gøre det til en fast regel.",
        "Plejer at efterfølges af navneform og beskriver en vane eller et sædvanligt "
        "forløb. Plejede at placerer vanen i fortiden, ofte med en forskel til nu. "
        "Udtrykket betyder ikke nødvendigvis hver gang. En enkelt afsluttet handling "
        "udtrykkes normalt med almindelig datid.",
        structure="Grundled + plejer/plejede + at + navneform.",
        rules=[
            "Behold at: Vi plejer at spise sammen.",
            "Brug ikke plejer alene som markør for noget, der sker lige nu.",
        ],
        examples=[
            GrammarExample("Jeg plejer at tage cyklen, men i dag tager jeg bussen."),
            GrammarExample("Vi plejede at spise sammen hver søndag."),
        ],
    ),
    GrammarTopic(
        "da-subordinate-negation-b1",
        "Ikke i ledsætninger",
        "B1",
        "Ordstilling",
        "Brug neutral ledsætningsordstilling med ikke og andre sætningsadverbier.",
        "I almindelige ledsætninger står ikke før det bøjede verbum: fordi hun ikke kan "
        "komme. I en fremsættende hovedsætning står det normalt efter: Hun kan ikke komme. "
        "Allerede, ofte og sikkert kan stå på samme centrale adverbialplads. "
        "Talesprog kan have hovedsætningsordstilling i visse at- og fordi-sætninger, "
        "også i formelle samtaler. Det er ikke et mønster, man frit kan overføre til "
        "alle ledsætninger.",
        structure="fordi/hvis/at + grundled + ikke + bøjet verbum",
        rules=[
            "Med to verber står ikke før hjælpeverbet i den neutrale ledsætning.",
            "En indledende ledsætning ændrer ikke sin egen indre ordstilling.",
        ],
        examples=[
            GrammarExample("Jeg skriver, fordi jeg ikke har fået en nøgle."),
            GrammarExample("Hvis du ikke kan komme, tager jeg din vagt."),
        ],
        related=["da-indirect-questions-b1"],
    ),
    GrammarTopic(
        "da-relative-som-der-b1",
        "Naboen som hjælper, og naboen jeg hjælper",
        "B1",
        "Relativsætninger",
        "Beskriv personer og ting med som, der eller en udeladt forbindelse.",
        "Som og der kan begge indlede en relativsætning, når de står for dens grundled: "
        "naboen som hjælper, naboen der hjælper. Når det relative led er genstandsled, "
        "bruges som eller ingen relativmarkør: naboen som jeg hjælper, naboen jeg hjælper. "
        "Der bruges ikke som genstandsled i denne konstruktion.",
        rules=[
            "En relativmarkør, der selv fungerer som grundled, kan ikke blot udelades.",
            "Skeln mellem relativmarkørens funktion og navneordets funktion i hovedsætningen.",
        ],
        examples=[
            GrammarExample("Det er den nabo, der passer vores kat."),
            GrammarExample("De kasser, jeg lånte, står i kælderen."),
        ],
        related=["da-subordinate-negation-b1"],
    ),
    GrammarTopic(
        "da-reflexive-possession-b1",
        "Sin, sit, sine eller hans og hendes",
        "B1",
        "Ejeforhold",
        "Vis, om ejeren er sætningens eget grundled.",
        "Sin, sit og sine viser normalt tilbage til et grundled i tredje person ental "
        "i samme sætning. Formen passer til det ejede: sin cykel, sit skur, sine nøgler. "
        "Hans og hendes peger normalt på en anden person. Med et flertalsgrundled bruges "
        "deres også om grundleddets egne ting. I konstruktioner med navneform kan "
        "henvisningen være mere kompleks; brug et navn, hvis ejeren ellers er uklar.",
        rules=[
            "Det er den enkelte sætnings grundled, der er udgangspunktet.",
            "Ejeren bestemmer ikke valget mellem sin, sit og sine; det gør det ejede.",
        ],
        examples=[
            GrammarExample("Maja låner sin cykel ud.", note="Cyklen tilhører Maja."),
            GrammarExample("Maja låner hendes cykel.", note="Cyklen tilhører en anden kvinde."),
            GrammarExample("Naboerne maler deres skur."),
        ],
    ),
    GrammarTopic(
        "da-s-passive-b1",
        "Blanketten udfyldes",
        "B1",
        "Passiv",
        "Forstå og formulér upersonlige instruktioner.",
        "S-passiv bruges blandt andet i vejledninger, regler og beskrivelser af sædvanlige "
        "forløb: Affaldet sorteres. I nutid har mange verber samme s-form som navneformen "
        "i passiv: udfyldes. Efter et modalverbum står passiv navneform: skal udfyldes. "
        "S-passiv fortæller ikke i sig selv, hvem der gør arbejdet.",
        rules=[
            "Skal udfyldes udtrykker et krav; udfyldes kan beskrive en procedure.",
            "Ikke alle verber på s er passive: synes og findes har også andre funktioner.",
        ],
        examples=[
            GrammarExample("Skemaet udfyldes digitalt."),
            GrammarExample("Bilag skal vedhæftes ansøgningen."),
        ],
        related=["da-blive-passive-b1"],
    ),
    GrammarTopic(
        "da-blive-passive-b1",
        "Ansøgningen bliver behandlet",
        "B1",
        "Passiv",
        "Flyt fokus fra den handlende til det, handlingen angår.",
        "Blive og kort tillægsform danner passiv: bliver behandlet, blev behandlet, "
        "er blevet behandlet. Formen er almindelig om konkrete hændelser og forløb. "
        "Den handlende kan tilføjes med af. Valget mellem s-passiv og blive-passiv "
        "afhænger også af teksttype; forskellen er ikke blot rigtig eller forkert.",
        rules=[
            "Bevar tid og aktør: Kommunen sendte brevet → Brevet blev sendt af kommunen.",
            "Af angiver den handlende: af kommunen.",
        ],
        examples=[
            GrammarExample("Mit pas blev sendt til den gamle adresse."),
            GrammarExample("Ansøgningen bliver behandlet af en sagsbehandler."),
        ],
        related=["da-s-passive-b1"],
    ),
    GrammarTopic(
        "da-modal-obligation-b1",
        "Skal, må ikke og behøver ikke",
        "B1",
        "Modalverber",
        "Skeln mellem pligt, forbud, råd og valgfrihed.",
        "Skal kan udtrykke et krav. Må udtrykker blandt andet tilladelse, så må ikke "
        "kan angive et forbud. Behøver ikke betyder, at noget ikke er nødvendigt, "
        "ikke at det er forbudt. Bør giver et råd eller en anbefaling. Skal ikke "
        "kan have forskellig styrke efter sammenhæng og tone; læs hele beskeden.",
        rules=[
            "Efter skal, må og bør står navneform uden at.",
            "Med behøver er både behøver komme og behøver at komme mulige.",
        ],
        examples=[
            GrammarExample("Du skal vise billedlegitimation."),
            GrammarExample("Du behøver ikke bestille tid."),
            GrammarExample("Du må ikke sende dit kodeord til andre."),
        ],
    ),
    GrammarTopic(
        "da-indirect-questions-b1",
        "Ved du, hvornår kurset begynder?",
        "B1",
        "Spørgsmål",
        "Indlejr et spørgsmål i en anden sætning.",
        "Et indirekte spørgsmål beholder sit spørgeord, men får ledsætningsordstilling: "
        "Hvornår begynder kurset? bliver til Ved du, hvornår kurset begynder? "
        "Et ja-nej-spørgsmål indledes med om. Når hvem selv spørger til grundleddet, "
        "bruges normalt der i den indirekte konstruktion: Jeg ved ikke, hvem der kommer.",
        rules=[
            "Brug ikke direkte spørgeordstilling efter om.",
            "Sætningsadverbier står normalt før det bøjede verbum i det indirekte spørgsmål.",
        ],
        examples=[
            GrammarExample("Kan du sige mig, om vi skal aflevere i dag?"),
            GrammarExample("Jeg vil gerne vide, hvorfor hun ikke har svaret."),
        ],
        related=["da-subordinate-negation-b1"],
    ),
    GrammarTopic(
        "da-reported-speech-b1",
        "Hun sagde, at hun kom senere",
        "B1",
        "Gengivelse",
        "Gengiv en besked fra dit eget tidspunkt og perspektiv.",
        "Ved indirekte tale skal stedord og tidsudtryk passe til den, der gengiver "
        "beskeden. Efter sagde står der ofte datid, men nutid kan bevares, når indholdet "
        "stadig gælder. Skulle kan vise en plan, som lå senere end det fortidige "
        "udsagn. Det er ikke nødvendigt at flytte alle tider mekanisk.",
        rules=[
            "Skeln mellem et ordret citat og din egen gengivelse.",
            "I morgen kan blive til dagen efter, når fortællingens tidspunkt ændres.",
        ],
        examples=[
            GrammarExample("I mandags sagde Ali, at han skulle på kursus dagen efter."),
            GrammarExample("Læreren sagde, at biblioteket har åbent om søndagen."),
        ],
        related=["da-subordinate-negation-b1"],
    ),
    GrammarTopic(
        "da-purpose-b1",
        "For at og så",
        "B1",
        "Formål",
        "Forklar, hvad en handling skal gøre muligt.",
        "For at efterfølges af navneform og udtrykker formål. Den tænkte handlende "
        "er ofte den samme som i hovedsætningen: Jeg øver mig for at blive bedre. "
        "Når formålet har sit eget grundled, er så med en sætning en almindelig løsning. "
        "Så kan også angive en faktisk følge; modalverber og sammenhæng hjælper med tolkningen.",
        rules=[
            "Brug en hel sætning, når det skal fremgå, hvem der får en mulighed.",
            "Et formål er et ønsket resultat, ikke nødvendigvis noget, der lykkes.",
        ],
        examples=[
            GrammarExample("Jeg tager et aftenkursus for at lære at skrive bedre."),
            GrammarExample("Jeg sender noterne, så du kan følge med."),
        ],
    ),
    GrammarTopic(
        "da-hypothetical-b1",
        "Hvis jeg havde mere tid",
        "B1",
        "Betingelser",
        "Tal om en tænkt mulighed i nutiden.",
        "Datid i en hvis-sætning kan markere afstand til virkeligheden snarere end "
        "fortidig tid: Hvis jeg havde mere tid, ville jeg lære at sejle. Følgen "
        "kan stå med ville eller kunne og navneform. En åben, realistisk betingelse "
        "står ofte i nutid: Hvis jeg får fri, tager jeg med.",
        rules=[
            "Tolk tiden ud fra hele situationen, ikke ud fra havde alene.",
            "Hovedsætningen har omvendt ordstilling efter en indledende hvis-sætning.",
        ],
        examples=[
            GrammarExample("Hvis turen var billigere, ville vi tage med."),
            GrammarExample("Jeg kunne hente dig, hvis jeg havde en bil."),
        ],
    ),
    GrammarTopic(
        "da-future-b1",
        "Planer, forventninger og fremtid",
        "B1",
        "Tid og modalitet",
        "Vælg en naturlig måde at tale om det kommende på.",
        "Dansk kan udtrykke fremtid med nutid og et tidsudtryk: Vi mødes på fredag. "
        "Skal bruges ofte om en plan eller aftale, mens vil blandt andet kan udtrykke "
        "vilje eller en forudsigelse. Kommer til at peger på et forventet forløb eller "
        "resultat. Formerne overlapper, men giver ikke altid samme perspektiv.",
        rules=[
            "Brug ikke automatisk vil i enhver sætning om fremtiden.",
            "Skal kan være både en plan og et krav; sammenhængen afgør betydningen.",
        ],
        examples=[
            GrammarExample("Vi skal besøge min søster i weekenden."),
            GrammarExample("Det kommer til at tage længere tid end planlagt."),
        ],
    ),
    GrammarTopic(
        "da-cause-result-b1",
        "Fordi, for og derfor",
        "B1",
        "Sammenhæng",
        "Forbind en begrundelse med dens følge.",
        "Fordi indleder en ledsætning med en årsag. For forbinder hovedsætninger "
        "og giver en begrundelse. Derfor peger tilbage på årsagen og står i en "
        "sætning, der beskriver følgen. Først i sætningen medfører derfor, at det "
        "bøjede verbum kommer før grundleddet.",
        rules=[
            "Fordi hun ikke kan komme, flytter vi mødet har ledsætningsordstilling.",
            "Vi flytter mødet, for hun kan ikke komme har hovedsætningsordstilling efter for.",
        ],
        examples=[
            GrammarExample("Bussen kører ikke i dag. Derfor tager vi toget."),
            GrammarExample("Jeg bliver hjemme, fordi jeg ikke er rask endnu."),
        ],
        related=["da-subordinate-negation-b1"],
    ),
    GrammarTopic(
        "da-particles-jo-nok-b1",
        "Det ved du jo, og det går nok",
        "B1",
        "Småord i samtalen",
        "Skeln mellem fælles viden og en forventning.",
        "Jo præsenterer ofte noget som kendt eller indlysende for samtalens deltagere. "
        "Nok kan som sætningsadverbium udtrykke en sandsynlig vurdering eller en "
        "beroligende forventning. Det er en anden brug end nok i mad nok, som handler "
        "om tilstrækkelig mængde. Tonefald og situation påvirker begge småord.",
        rules=[
            "Jo kan lyde belærende, hvis modtageren ikke deler den påståede viden.",
            "Nok er ikke et løfte om, at noget med sikkerhed sker.",
        ],
        examples=[
            GrammarExample("Vi kan jo låne borde i fælleshuset."),
            GrammarExample("Der kommer nok flere efter arbejde."),
            GrammarExample("Bare rolig, vi når det nok."),
        ],
    ),
    GrammarTopic(
        "da-reciprocal-reflexive-b1",
        "Sig og hinanden",
        "B1",
        "Stedord og relationer",
        "Gør det klart, om handlingen går tilbage på én selv eller mellem flere.",
        "Sig viser tilbage til et grundled i tredje person: Hun skynder sig. "
        "Med jeg, du og vi bruges mig, dig og os. Hinanden beskriver en gensidig "
        "relation mellem flere deltagere. Nogle verber har et fast refleksivt led, "
        "som ikke kan oversættes ord for ord: glæde sig, melde sig og skynde sig.",
        rules=[
            "De hjælper sig selv og de hjælper hinanden har forskellig betydning.",
            "Lær faste forbindelser med deres forholdsord: glæde sig til noget.",
        ],
        examples=[
            GrammarExample("Vi hjælper hinanden med oprydningen."),
            GrammarExample("Hun har meldt sig til fællesspisningen."),
            GrammarExample("Jeg glæder mig til at møde de andre."),
        ],
        related=["da-reflexive-possession-b1", "da-particle-verbs-b1"],
    ),
    GrammarTopic(
        "da-particle-verbs-b1",
        "Møde op, finde på og give op",
        "B1",
        "Faste verbforbindelser",
        "Lær verbet og det lille ord som en samlet betydning.",
        "Et lille ord kan ændre verbets betydning: møde nogen er ikke det samme "
        "som møde op. Finde på en aktivitet betyder at få en idé til den; finde "
        "en aktivitet kan blot betyde at opdage den. Placeringen af et genstandsled "
        "afhænger af forbindelsen, så lær et helt eksempel sammen med udtrykket.",
        rules=[
            "Møde op kan stå uden genstandsled: til mødet, på kontoret eller i fælleshuset.",
            "Giv ikke alle småord samme funktion: nogle indgår i faste forholdsordsforbindelser.",
        ],
        examples=[
            GrammarExample("Kan du finde på noget, børnene kan lave?"),
            GrammarExample("Hun mødte op til arbejdsdagen klokken ni."),
            GrammarExample("Vi giver ikke op, selv om det tager tid."),
        ],
    ),
    GrammarTopic(
        "da-concession-b1",
        "Selv om og alligevel",
        "B1",
        "Indrømmelse og kontrast",
        "Vis, at et forhold ikke forhindrer et andet.",
        "Selv om indleder en ledsætning og kan beskrive både en faktisk og en tænkt "
        "hindring. Alligevel fremhæver, at følgen går imod en forventning. Trods "
        "efterfølges af et navneordsudtryk, mens selv om efterfølges af en sætning. "
        "Sammenhængen viser, om hindringen allerede er kendt.",
        rules=[
            "Skriv trods regnen eller selv om det regner.",
            "Alligevel først i en hovedsætning efterfølges af det bøjede verbum.",
        ],
        examples=[
            GrammarExample("Selv om jakken var på tilbud, var den for dyr."),
            GrammarExample("Det regnede. Alligevel cyklede vi hjem."),
        ],
        related=["da-subordinate-negation-b1"],
    ),
    GrammarTopic(
        "da-quantity-b1",
        "Flere, færre, mere og mindre",
        "B1",
        "Mængde og sammenligning",
        "Skeln mellem antal og mængde i en sammenligning.",
        "Flere og færre bruges som udgangspunkt om noget, der tælles: flere "
        "cykler, færre poser. Mere og mindre bruges om mængde: mere vand, mindre "
        "affald. Et ord kan skifte perspektiv: flere kaffe kan i en bestilling "
        "betyde flere kopper, mens mere kaffe handler om mængden.",
        rules=[
            "Se på betydningen i sammenhængen, ikke kun på navneordet isoleret.",
            "Få og lidt bliver til færre og mindre i sammenligninger.",
        ],
        examples=[
            GrammarExample("Vi køber færre engangsposer og bruger mindre plastik."),
            GrammarExample("Der er flere gæster, så vi skal bruge mere kaffe."),
        ],
    ),
    GrammarTopic(
        "da-time-limits-b1",
        "Inden, indtil og først",
        "B1",
        "Tidsgrænser",
        "Forstå forskellen mellem en frist, en varighed og et sent starttidspunkt.",
        "Inden angiver, at noget skal ske før en grænse: inden fredag. Indtil "
        "angiver, hvor længe noget fortsætter: Vi venter indtil fredag. Først "
        "markerer et tidspunkt som det tidligste eller som senere end ventet: "
        "Pengene kommer først fredag. Ikke før kan udtrykke den samme nedre grænse.",
        rules=[
            "Spørg om dato og klokkeslæt, hvis en praktisk frist kan forstås forskelligt.",
            "Indtil fortæller ikke, at handlingen først begynder ved slutpunktet.",
        ],
        examples=[
            GrammarExample("Du kan bruge lånecyklen indtil mandag."),
            GrammarExample("Vi får først svar i næste uge."),
            GrammarExample("Send kvitteringen inden klokken tolv."),
        ],
    ),
]
