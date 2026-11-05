"""Swedish C2 phrasebook balancing analytical precision and real interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "sv-inference_c2",
        "C2",
        "Pröva förutsättningar och antydningar",
        "🔎",
        [
            PhrasebookEntry(
                "Jag delar inte förutsättningen som frågan bygger på.",
                "Avvisa en omstridd premiss utan att svara inom dess ram.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Det är en möjlig läsning, men den följer inte nödvändigtvis av orden.",
                "Skilj rimlig inferens från uttryckligt innehåll.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Kan vi skilja det som är belagt från det som bara antyds?",
                "Säkra en korrekt sammanfattning av ett underlag.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Invändningen gäller ordvalet, inte den positiva bedömningen.",
                "Förklara en metalingvistisk korrigering.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Vilket ytterligare antagande behövs för att nå den slutsatsen?",
                "Synliggör ett dolt steg i ett resonemang.",
                "formal",
                "c2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-perspectives_c2",
        "C2",
        "Röster och tidslager",
        "📖",
        [
            PhrasebookEntry(
                "Här tycks värderingen tillhöra personen snarare än berättaren.",
                "Ge en försiktig tolkning av fri indirekt framställning.",
                "formal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Att hon kunde ha ingripit innebär inte att hon faktiskt gjorde det.",
                "Håll möjlighet och genomförande isär.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Jag skulle vilja behålla den äldre formen i citatet men förklara den efteråt.",
                "Skilj citerad originaltext från språklig förklaring.",
                "formal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Från vems tidpunkt ska ordet imorgon förstås här?",
                "Klargör deiktiskt perspektiv i en berättelse.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Texten lämnar öppet om minnet är tillförlitligt.",
                "Bevara en avsiktlig osäkerhet i litterär tolkning.",
                "formal",
                "c2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-precision_c2",
        "C2",
        "Avgränsa rättigheter och villkor",
        "📄",
        [
            PhrasebookEntry(
                "Gäller undantaget enbart tidsfristen eller även själva skyldigheten?",
                "Kontrollera räckvidden i en tät regeltext.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Jag ser två rimliga tolkningar och vill inte välja en utan förtydligande.",
                "Markera en verklig tvetydighet.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Omskrivningen gör en möjlighet till en rättighet och behöver därför justeras.",
                "Påpeka en betydelseförskjutning i redigering.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Låt oss formulera huvudregeln och undantaget var för sig.",
                "Föreslå en tydligare struktur utan att ändra innehållet.",
                "neutral",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Jag kan godta preciseringen, förutsatt att den inte utvidgar vårt åtagande.",
                "Acceptera en ändring med en uttrycklig gräns.",
                "formal",
                "c2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-rhetoric_c2",
        "C2",
        "Retorik och varsam kritik",
        "🎭",
        [
            PhrasebookEntry(
                "Jämförelsen är belysande, men den bär inte hela slutsatsen.",
                "Erkänn en analogis värde utan att godta den som bevis.",
                "formal",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Den retoriska frågan får oenigheten att framstå som mindre än den är.",
                "Synliggör en påtryckande framställning.",
                "formal",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Om jag uttrycker det utan underdrift behöver den delen göras om.",
                "Gör mild kritik tydlig när handling krävs.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Jag vill bemöta ditt faktiska förslag, inte en förenklad version av det.",
                "Undvik att diskutera en halmgubbe.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Vilken del av bilden är avsedd att motsvara vår situation?",
                "Pröva en metafor eller analogi sakligt.",
                "neutral",
                "c2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-negotiation_c2",
        "C2",
        "Säkra ett korrekt åtagande",
        "🤝",
        [
            PhrasebookEntry(
                "Vi är öppna för att pröva idén, men har inte förbundit oss att genomföra den.",
                "Skilj sondering från ett bindande löfte.",
                "formal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Får jag stanna vid tidsfristen innan vi går vidare till kostnaden?",
                "Avbryt med ett tydligt och avgränsat syfte.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Jag vill kontrollera en detalj, sedan lämnar jag tillbaka ordet.",
                "Ta en kort tur utan att ta över hela samtalet.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Kan protokollet skilja överenskomna åtgärder från frågor som återstår?",
                "Undvik att dokumentationen skapar ett falskt samförstånd.",
                "formal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Det är en eftergift i fråga om tid, inte ett godkännande av den högre kostnaden.",
                "Avgränsa vad en kompromiss faktiskt innebär.",
                "formal",
                "c2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-repair_c2",
        "C2",
        "Reparera ton och relation",
        "💬",
        [
            PhrasebookEntry(
                "Avsikten var att skämta om mig själv, men jag förstår att det träffade dig.",
                "Erkänn skillnaden mellan humoristisk avsikt och faktisk effekt.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Jag vill inte släta över det med ett skämt; låt oss reda ut vad som blev fel.",
                "Ta ett relationsproblem på allvar.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Det där blev klumpigt. Jag ber om ursäkt och försöker formulera mig bättre.",
                "Ta ansvar för ett misslyckat yttrande.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Jag hör att kommentaren landade annorlunda än jag tänkte.",
                "Öppna för den andres upplevelse utan att förneka den.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Kan vi återgå till sakfrågan utan att tappa det du just tog upp?",
                "Återför samtalet varsamt och bevara den känsliga punkten.",
                "neutral",
                "c2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-synthesis_c2",
        "C2",
        "Förmedla komplexa slutsatser",
        "🧭",
        [
            PhrasebookEntry(
                "Sammantaget stöder materialet ett begränsat försök, inte ett fullständigt införande.",
                "Anpassa rekommendationens omfattning till beläggen.",
                "formal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Vi kan förenkla termerna, men reservationen måste finnas kvar.",
                "Gör fackinnehåll tillgängligt utan betydelseförlust.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Genomsnittet säger inget säkert om hur just den här personen påverkas.",
                "Håll gruppnivå och individnivå isär.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Källorna pekar åt samma håll i den delen, men skiljer sig åt beträffande orsaken.",
                "Sammanväg både gemensamt resultat och kvarstående oenighet.",
                "formal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Min rekommendation är ett praktiskt val under osäkerhet, inte ett påstående om säker effekt.",
                "Skilj handlingsförslag från faktasäkerhet.",
                "formal",
                "c2-unit-7",
            ),
        ],
    ),
]
