"""Swedish B1 phrasebook for connected interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "sv-stories_b1",
        "B1",
        "Berätta om en erfarenhet",
        "💬",
        [
            PhrasebookEntry(
                "När jag kom fram hade de redan gått.",
                "Ange vad som hänt före din ankomst.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Förr brukade jag ta bilen, men nu cyklar jag.",
                "Beskriv en ändrad vana.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Det som överraskade mig mest var hur snabbt allt gick.",
                "Lyft fram en viktig del av en upplevelse.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Först blev jag orolig, men sedan ordnade det sig.",
                "Beskriv en förändrad känsla under ett förlopp.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Jag hade aldrig varit med om något liknande.",
                "Beskriv en ny erfarenhet från en dåtida utgångspunkt.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Till slut hittade vi en lösning tillsammans.",
                "Avsluta en berättelse om ett problem.",
                "neutral",
                "b1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-rules_b1",
        "B1",
        "Fråga om regler och ansvar",
        "📋",
        [
            PhrasebookEntry(
                "Vilka handlingar behöver jag skicka in?",
                "Fråga vad som krävs i ett ärende.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Måste blanketten skrivas under för hand?",
                "Kontrollera en formell instruktion.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Vem ansvarar för att lokalen låses?",
                "Gör ansvarsfördelningen tydlig.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Gäller samma regler även på helgerna?",
                "Kontrollera regelns räckvidd i tid.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Var kan jag läsa mer om villkoren?",
                "Be om den fullständiga informationen.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Jag vill gärna få beskedet skriftligt.",
                "Be om dokumentation av ett svar.",
                "neutral",
                "b1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-advice_b1",
        "B1",
        "Jämföra alternativ och ge råd",
        "⚖️",
        [
            PhrasebookEntry(
                "Om jag var du skulle jag fråga en gång till.",
                "Ge ett råd utan att uttrycka ett krav.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Fördelen är priset, men resan tar längre tid.",
                "Väg två sidor av ett alternativ.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Du behöver inte bestämma dig direkt.",
                "Förklara att ett omedelbart beslut inte krävs.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Jag skulle hellre välja det senare tåget.",
                "Uttryck en personlig preferens.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Hon sa att hon skulle återkomma på fredag.",
                "Återge ett besked utan att garantera att det genomförs.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Vilket alternativ passar dina behov bäst?",
                "Låt den andra personens behov styra jämförelsen.",
                "neutral",
                "b1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-opinions_b1",
        "B1",
        "Uttrycka och bemöta åsikter",
        "🗞️",
        [
            PhrasebookEntry(
                "Jag håller med om målet, men inte om metoden.",
                "Ange exakt var du instämmer och skiljer dig.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Vad bygger du den uppgiften på?",
                "Fråga efter källan utan att angripa personen.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Jag ser det på ett annat sätt.",
                "Inled en saklig invändning.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Vi ändrade tiden för att fler skulle kunna delta.",
                "Förklara avsikten med en förändring.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Trots att det kostar mer kan det vara bättre på lång sikt.",
                "Medge en nackdel och ange en möjlig fördel.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Kan du ge ett konkret exempel?",
                "Be om stöd för ett allmänt resonemang.",
                "neutral",
                "b1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-cooperation_b1",
        "B1",
        "Fördela arbete och hantera missförstånd",
        "🤝",
        [
            PhrasebookEntry(
                "Ska vi dela upp uppgifterna mellan oss?",
                "Föreslå en tydlig arbetsfördelning.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Jag tar hand om maten om du ordnar lokalen.",
                "Föreslå en konkret överenskommelse.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Vi verkar ha missförstått varandra.",
                "Öppna för gemensam reparation utan att lägga all skuld på någon.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Jag ber om ursäkt för att jag inte meddelade dig.",
                "Ta ansvar för en utebliven kontakt.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Båda behöver få möjlighet att förklara sig.",
                "Be om utrymme för två perspektiv.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Kan du ställa stolarna längs väggen?",
                "Be om hjälp med placeringen av möbler.",
                "neutral",
                "b1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-environment_b1",
        "B1",
        "Diskutera hållbara vardagsval",
        "🌿",
        [
            PhrasebookEntry(
                "Vi behöver färre förpackningar, inte bara större kärl.",
                "Skilj minskat antal från större kapacitet.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Jag försöker återanvända det som fortfarande fungerar.",
                "Beskriv en vardagsvana.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Var ska den här förpackningen sorteras?",
                "Fråga om en konkret sorteringsregel.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Det är både billigare och bättre för miljön i det här fallet.",
                "Ange två fördelar med tydlig avgränsning.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Jag har inte heller möjlighet att cykla varje dag.",
                "Lägg till ett liknande hinder utan att generalisera.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Vilka förändringar skulle fungera för dig?",
                "Fråga efter realistiska alternativ.",
                "neutral",
                "b1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-problems_b1",
        "B1",
        "Klargöra ett ärende",
        "🔎",
        [
            PhrasebookEntry(
                "Menar du att jag ska vänta tills ni hör av er?",
                "Kontrollera en instruktion och dess tidsgräns.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Det jag menar är att datumet inte stämmer.",
                "Förtydliga vilken del av ett besked som är fel.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Jag kan inte lämna besked förrän på torsdag.",
                "Ange tidigaste möjliga svarstid.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Kan tidsgränsen förlängas med två dagar?",
                "Be om ett avgränsat uppskov.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Vem kan hjälpa mig med återbetalningen?",
                "Hitta rätt kontakt för ett ärende.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Om jag har förstått rätt behöver ni bara den sista bilagan.",
                "Kontrollera att du uppfattat begäran korrekt.",
                "neutral",
                "b1-unit-7",
            ),
        ],
    ),
]
