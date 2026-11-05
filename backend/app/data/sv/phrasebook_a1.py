"""Swedish A1 phrasebook with short, reusable exchanges."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "sv-introductions_a1",
        "A1",
        "Hälsa och förstå varandra",
        "👋",
        [
            PhrasebookEntry(
                "Hej! Jag heter Sara.",
                "Presentera dig; byt ut namnet mot ditt eget.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry("Vad heter du?", "Fråga en person om namnet.", "neutral", "a1-unit-1"),
            PhrasebookEntry(
                "Trevligt att träffas.",
                "Säg något vänligt efter en presentation.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Jag lär mig svenska.",
                "Förklara kort att du studerar språket.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Kan du säga det igen?",
                "Be om upprepning när du inte hör eller förstår.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Kan du tala lite långsammare?", "Be om ett lägre taltempo.", "neutral", "a1-unit-1"
            ),
            PhrasebookEntry(
                "Hur stavar du ditt namn?",
                "Be personen säga bokstäverna i namnet.",
                "neutral",
                "a1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-people_a1",
        "A1",
        "Människor och tillhörigheter",
        "👥",
        [
            PhrasebookEntry(
                "Det här är min vän Ali.",
                "Presentera en vän för någon annan.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Jag har två syskon.",
                "Berätta kort om familjen; anpassa antalet.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Min syster bor i Malmö.",
                "Berätta var en familjemedlem bor.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Är det din väska?", "Kontrollera vem en sak tillhör.", "neutral", "a1-unit-2"
            ),
            PhrasebookEntry(
                "Nej, den är inte min.",
                "Säg att en nämnd väska inte tillhör dig.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Vilken fin hund!", "Säg något vänligt om någons hund.", "neutral", "a1-unit-2"
            ),
            PhrasebookEntry(
                "Hur gammalt är barnet?",
                "Fråga om ett barns ålder när det passar samtalet.",
                "neutral",
                "a1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-time_a1",
        "A1",
        "Tider och vardag",
        "🕒",
        [
            PhrasebookEntry(
                "Vad är klockan?", "Fråga vilken tid det är nu.", "neutral", "a1-unit-3"
            ),
            PhrasebookEntry(
                "Klockan är halv åtta.",
                "Ange 7.30; halv räknas mot nästa timme.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "När börjar lektionen?", "Fråga om starttiden.", "neutral", "a1-unit-3"
            ),
            PhrasebookEntry(
                "Jag arbetar på måndag.",
                "Berätta om en kommande arbetsdag.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Jag kan inte idag.",
                "Säg att dagens föreslagna tid inte passar.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Vi ses klockan nio.", "Bekräfta en gemensam tid.", "neutral", "a1-unit-3"
            ),
            PhrasebookEntry(
                "Menar du nio på morgonen?",
                "Kontrollera vilken del av dygnet som avses.",
                "neutral",
                "a1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-food_a1",
        "A1",
        "På café och i matbutiken",
        "☕",
        [
            PhrasebookEntry(
                "En kopp kaffe, tack.", "Beställ en dryck vid disken.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry("Kan jag få ett glas vatten?", "Be om vatten.", "neutral", "a1-unit-4"),
            PhrasebookEntry("Vad kostar det?", "Fråga om priset.", "neutral", "a1-unit-4"),
            PhrasebookEntry(
                "Jag vill ha två äpplen.",
                "Ange vad och hur många du vill köpa.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Finns det mjölk i den här?",
                "Fråga om en ingrediens i en utpekad produkt.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Kan jag betala med kort?", "Kontrollera betalningssätt.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Nej tack, det är bra.",
                "Avböj något extra på ett vänligt sätt.",
                "neutral",
                "a1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-directions_a1",
        "A1",
        "Hemma och på väg",
        "🚌",
        [
            PhrasebookEntry(
                "Ursäkta, var ligger stationen?", "Be en person visa vägen.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry(
                "Går den här bussen till centrum?",
                "Kontrollera bussens destination.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "En biljett till Uppsala, tack.",
                "Köp en biljett; byt ut orten efter behov.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Finns det ett apotek här?",
                "Fråga efter en serviceplats i närheten.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Jag bor nära skolan.", "Beskriv var ditt hem ligger.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry(
                "Nyckeln ligger på bordet.", "Berätta var en sak finns.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry("Var är toaletten?", "Fråga efter toaletten.", "neutral", "a1-unit-5"),
        ],
    ),
    PhrasebookCategory(
        "sv-leisure_a1",
        "A1",
        "Fritid tillsammans",
        "🌤️",
        [
            PhrasebookEntry(
                "Vill du ta en promenad?", "Föreslå en enkel aktivitet.", "neutral", "a1-unit-6"
            ),
            PhrasebookEntry("Ja, gärna!", "Tacka ja till ett förslag.", "neutral", "a1-unit-6"),
            PhrasebookEntry(
                "Jag vill gärna, men jag arbetar.",
                "Avböj med en kort förklaring.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Ska vi ses på lördag?", "Föreslå en dag för en träff.", "neutral", "a1-unit-6"
            ),
            PhrasebookEntry(
                "Jag tycker om att läsa.", "Berätta om ett fritidsintresse.", "neutral", "a1-unit-6"
            ),
            PhrasebookEntry(
                "Kom in!", "Bjud in någon som står vid dörren.", "neutral", "a1-unit-6"
            ),
            PhrasebookEntry(
                "Vi hörs!",
                "Avsluta ett vardagligt samtal med tanke på fortsatt kontakt.",
                "informal",
                "a1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-help_a1",
        "A1",
        "Be om hjälp",
        "💬",
        [
            PhrasebookEntry(
                "Kan du hjälpa mig?", "Be om hjälp med ett konkret problem.", "neutral", "a1-unit-7"
            ),
            PhrasebookEntry(
                "Jag behöver en läkare.", "Säg att du behöver vårdkontakt.", "neutral", "a1-unit-7"
            ),
            PhrasebookEntry(
                "Jag har ont i huvudet.", "Beskriv var det gör ont.", "neutral", "a1-unit-7"
            ),
            PhrasebookEntry(
                "Igår var jag sjuk.", "Berätta kort om gårdagen.", "neutral", "a1-unit-7"
            ),
            PhrasebookEntry(
                "Har ni den här i en annan storlek?",
                "Fråga butikspersonalen om ett plagg; ni syftar här på butiken.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Kan du skriva numret?",
                "Be om skriftligt stöd för ett nummer.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Jag förstår inte det här ordet.",
                "Ange exakt vad som är svårt att förstå.",
                "neutral",
                "a1-unit-7",
            ),
        ],
    ),
]
