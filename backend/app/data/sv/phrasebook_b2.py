"""Swedish B2 phrases for accountable discussion and practical negotiation."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "sv-consequences_b2",
        "B2",
        "Förklara ett förlopp",
        "⏳",
        [
            PhrasebookEntry(
                "Om vi hade fått besked tidigare skulle vi ha hunnit anpassa oss.",
                "Beskriv ett annat tänkbart förflutet.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Det var planerat så, men jag vet inte om det genomfördes.",
                "Skilj avsikt från faktisk handling.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Åtgärden löste det akuta problemet men fick andra följder.",
                "Nyansera en beskrivning av ett resultat.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Kan vi gå igenom vad som hände före avbrottet?",
                "Be om en gemensam tidslinje.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Jag vill förstå orsaken innan vi bestämmer nästa steg.",
                "Motivera att beslutet behöver mer underlag.",
                "neutral",
                "b2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-focus_b2",
        "B2",
        "Avgränsa det du menar",
        "🎯",
        [
            PhrasebookEntry(
                "Det är tidsplanen jag invänder mot, inte målet.",
                "Precisera vilken del kritiken gäller.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Inte alla omfattas av ändringen; vi behöver se vilka som gör det.",
                "Undvik att göra en delvis förändring allmän.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "När du säger de, vilka syftar du på?",
                "Klargör en oklar hänvisning.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Jag vill bara kontrollera en sak innan vi går vidare.",
                "Begränsa ett avbrott till en konkret kontroll.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Kan du skilja mellan det som ingår och det som tillkommer?",
                "Be om en tydlig avgränsning av ett erbjudande.",
                "neutral",
                "b2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-sources_b2",
        "B2",
        "Bedöma en uppgift",
        "📰",
        [
            PhrasebookEntry(
                "Enligt rapporten har väntetiden minskat, men underlaget gäller bara en månad.",
                "Återge ett resultat med källa och avgränsning.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Det kan vara en förklaring, men vi har inte bekräftat den.",
                "Håll en möjlighet öppen utan att göra den till faktum.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Vilka belägg finns för den slutsatsen?",
                "Be om relevant stöd för ett påstående.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Jag uppfattar det som en uppskattning snarare än ett löfte.",
                "Markera din tolkning av ett beskeds säkerhetsgrad.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Vi bör kontrollera originalkällan innan vi delar uppgiften.",
                "Föreslå källkontroll före vidare spridning.",
                "neutral",
                "b2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-conditions_b2",
        "B2",
        "Villkor och undantag",
        "📄",
        [
            PhrasebookEntry(
                "Gäller erbjudandet även om leveransen blir försenad?",
                "Kontrollera ett särskilt fall innan du accepterar.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Är det ett krav eller bara en rekommendation?",
                "Skilj skyldighet från råd.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Jag accepterar priset under förutsättning att frakten ingår.",
                "Ge ett uttryckligen villkorat godkännande.",
                "formal",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Kan ni bekräfta vilka undantag som finns?",
                "Be organisationen precisera regelns gränser.",
                "formal",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Ett kvitto är alltså nödvändigt, men finns det fler krav?",
                "Kontrollera att ett nödvändigt villkor inte misstas för det enda.",
                "neutral",
                "b2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-argument_b2",
        "B2",
        "Bemöta argument",
        "⚖️",
        [
            PhrasebookEntry(
                "Jag ser fördelen, men den behöver vägas mot kostnaden.",
                "Medge en poäng och tillför en relevant avvägning.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Det visar ett samband, men inte nödvändigtvis en orsak.",
                "Avgränsa vad underlaget faktiskt stöder.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Vilken invändning tycker du väger tyngst?",
                "Fokusera diskussionen på det viktigaste motargumentet.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Däremot ser jag inget stöd för att alla skulle påverkas lika.",
                "Invänd mot en för bred slutsats.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Kan vi pröva förslaget i mindre skala först?",
                "Föreslå ett praktiskt sätt att hantera osäkerhet.",
                "neutral",
                "b2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-workplace_b2",
        "B2",
        "Förhandla om arbete och tid",
        "🤝",
        [
            PhrasebookEntry(
                "Jag kan ta över uppgiften, men behöver underlaget senast onsdag.",
                "Ange ansvar och villkor i samma besked.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Vad behöver prioriteras om tiden inte räcker?",
                "Be om ett konkret val vid hög arbetsbelastning.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Jag vill ta upp en risk innan vi fastställer tidsplanen.",
                "Inled en relevant invändning före beslut.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Det här är ett utkast och jag vill gärna ha synpunkter.",
                "Markera att en text ännu inte är slutlig.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Låt oss skriva ned vem som gör vad och till när.",
                "Säkra en gemensam förståelse av överenskommelsen.",
                "neutral",
                "b2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-society_b2",
        "B2",
        "Samtal om samhälle och kultur",
        "🌍",
        [
            PhrasebookEntry(
                "Min erfarenhet är en annan, men den gäller bara den förening jag känner.",
                "Dela en erfarenhet utan att generalisera.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Vilka olika perspektiv saknas i den här beskrivningen?",
                "Öppna för fler röster i ett kultursamtal.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Jag vill gärna delta, men inte få mitt namn publicerat.",
                "Ange en tydlig gräns för deltagande och integritet.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Vet du vilka regler som gäller just i det här naturreservatet?",
                "Fråga om lokala begränsningar i naturen.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Hur kan vi göra aktiviteten tillgänglig för fler?",
                "Föreslå ett inkluderande praktiskt samtal.",
                "neutral",
                "b2-unit-7",
            ),
        ],
    ),
]
