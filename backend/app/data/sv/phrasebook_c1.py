"""Swedish C1 phrases for nuanced and socially grounded communication."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "sv-evidence_c1",
        "C1",
        "Gradera en slutsats",
        "🔎",
        [
            PhrasebookEntry(
                "Såvitt jag kan bedöma talar underlaget för det, men urvalet är begränsat.",
                "Ge en underbyggd men avgränsad bedömning.",
                "formal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Uppgiften kommer från leverantören och är ännu inte oberoende bekräftad.",
                "Bevara källan och osäkerheten.",
                "formal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Det är en rimlig hypotes, inte en fastställd förklaring.",
                "Skilj möjlig tolkning från verifierad orsak.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Vad skulle få oss att ompröva den bedömningen?",
                "Undersök vilka belägg som kan ändra slutsatsen.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Jag vill reservera mig för att siffrorna kan behöva justeras.",
                "Ange en konkret begränsning i ett besked.",
                "formal",
                "c1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-focus_c1",
        "C1",
        "Precisera fokus och omfattning",
        "🎯",
        [
            PhrasebookEntry(
                "Just den delen har vi inte tagit ställning till ännu.",
                "Avgränsa vad som fortfarande är öppet.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Att inte alla svarade säger inte hur många som avstod.",
                "Motverka en obelagd kvantitativ slutsats.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Det förslaget kan jag stödja, men inte den utvidgade versionen.",
                "Knyt an till ett tidigare förslag och markera kontrast.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "När du säger enbart, gäller det kostnaden eller hela uppdraget?",
                "Kontrollera räckvidden hos ett fokusord.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Låt oss precisera vad vi faktiskt är oeniga om.",
                "Gör en bred konflikt hanterbar genom avgränsning.",
                "neutral",
                "c1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-responsibility_c1",
        "C1",
        "Klargöra ansvar och referens",
        "📋",
        [
            PhrasebookEntry(
                "Vem har mandat att fatta det beslutet?",
                "Skilj beredning från beslutanderätt.",
                "formal",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Jag lovade att fråga henne, inte att hon skulle tacka ja.",
                "Rätta en återgivning som gjort ditt åtagande för stort.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "För att undvika missförstånd skriver jag ut namnet istället för pronomenet.",
                "Förklara en precisering av ägare eller aktör.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Avser formuleringen en planerad eller redan genomförd granskning?",
                "Kontrollera tidsstatus i en informationstät text.",
                "formal",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Jag kan sammanställa underlaget, men själva godkännandet ligger hos styrelsen.",
                "Ange gränsen för ditt ansvar.",
                "formal",
                "c1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-deliberation_c1",
        "C1",
        "Villkorade ställningstaganden",
        "⚖️",
        [
            PhrasebookEntry(
                "Visserligen löser det ett problem, men vi behöver väga in följderna för andra.",
                "Medge en fördel och öppna en bredare avvägning.",
                "formal",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Jag tillstyrker förslaget under förutsättning att uppföljningen finansieras.",
                "Ge ett formellt stöd med ett uttryckligt villkor.",
                "formal",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Skulle tidsplanen ändras behöver vi ompröva bemanningen.",
                "Ange en följd av ett möjligt framtida villkor.",
                "formal",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Min invändning gäller proportionaliteten, inte syftet i sig.",
                "Avgränsa kritik mot en åtgärds omfattning.",
                "formal",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Kan vi enas om vilka kriterier som ska styra prövningen?",
                "Flytta diskussionen till gemensamma bedömningsgrunder.",
                "neutral",
                "c1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-mediation_c1",
        "C1",
        "Medla och avböja tydligt",
        "🤝",
        [
            PhrasebookEntry(
                "Ni tycks vara överens om målet men oense om hur snabbt förändringen bör ske.",
                "Pröva en sammanfattning av två perspektiv utan att slå fast den.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Jag uppskattar frågan, men behöver avstå från uppdraget.",
                "Ge ett vänligt och tydligt nej.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Jag kan inte lova leverans på fredag; tisdag är däremot realistiskt.",
                "Avgränsa ett åtagande och ge ett faktiskt alternativ.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Du menar väl inte att beslutet redan är fattat?",
                "Sök bekräftelse på en tolkning; tonfallet behöver vara öppet.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Låt mig återge bådas önskemål innan vi söker en lösning.",
                "Skapa utrymme för rättvis medling.",
                "neutral",
                "c1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-tone_c1",
        "C1",
        "Humor, betoning och missförstånd",
        "💬",
        [
            PhrasebookEntry(
                "Jag är osäker på om du skämtar eller menar det bokstavligt.",
                "Kontrollera ironi när signalerna är svaga.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Det var min egen miss jag skämtade om, inte din.",
                "Förtydliga självironi som uppfattats som kritik.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Jag sa att vi kunde prova, inte att vi hade bestämt oss.",
                "Korrigera modalitet med kontrastbetoning.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Det där lät hårdare än jag avsåg. Jag börjar om.",
                "Ta ansvar för tonen och reparera budskapet.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Ja, min planering var kanske inte dagens höjdpunkt.",
                "Använd mild självironi om ett eget misstag bland bekanta.",
                "informal",
                "c1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-expression_c1",
        "C1",
        "Anpassa en framställning",
        "✍️",
        [
            PhrasebookEntry(
                "Kan vi behålla reservationen men uttrycka den mer begripligt?",
                "Förenkla språket utan att ta bort viktig osäkerhet.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "I den här genren skulle jag välja en mer neutral formulering.",
                "Ge en registerbaserad rekommendation utan att kalla alternativet fel.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Det är en regional variant, inte nödvändigtvis ett språkfel.",
                "Påminn om giltig språklig variation.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Jag föreslår att inskottet blir en egen mening.",
                "Gör en tät text lättare att följa.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Vilken förkunskap kan vi rimligen förutsätta hos läsaren?",
                "Planera mottagaranpassning innan texten bearbetas.",
                "formal",
                "c1-unit-7",
            ),
        ],
    ),
]
