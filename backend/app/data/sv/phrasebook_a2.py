"""Swedish A2 phrasebook for routine transactions and social plans."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "sv-travel_a2",
        "A2",
        "Resor och bokningar",
        "🚆",
        [
            PhrasebookEntry(
                "Jag har bokat ett rum för två nätter.",
                "Ange bokningen när du kommer till ett hotell.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Vilket spår går tåget från?", "Fråga var tåget avgår.", "neutral", "a2-unit-1"
            ),
            PhrasebookEntry(
                "Behöver jag byta tåg?", "Kontrollera om resan är direkt.", "neutral", "a2-unit-1"
            ),
            PhrasebookEntry(
                "Jag missade bussen eftersom tåget var sent.",
                "Förklara ett reseproblem.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "När är nästa avgång?",
                "Fråga efter nästa möjlighet att resa.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Jag skulle vilja avboka mitt rum.",
                "Be att få ta tillbaka en hotellbokning.",
                "neutral",
                "a2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-housing_a2",
        "A2",
        "Bostad och felanmälan",
        "🏠",
        [
            PhrasebookEntry(
                "Ingår el i hyran?",
                "Kontrollera vad bostadskostnaden omfattar.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Finns det en gemensam tvättstuga?",
                "Fråga om bostadens utrustning.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Den här lägenheten är ljusare än den förra.",
                "Jämför två bostäder.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Hissen har varit trasig sedan igår.",
                "Beskriv ett fel och när det började.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Vem ska jag kontakta om det läcker?",
                "Fråga vem som kan ta emot en felanmälan.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Kan vi boka en tid för att titta på lägenheten?",
                "Be om en visning.",
                "neutral",
                "a2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-health_a2",
        "A2",
        "Hos vården",
        "🩺",
        [
            PhrasebookEntry(
                "Jag skulle vilja boka en tid hos en läkare.",
                "Be om ett vårdbesök.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Jag har haft ont i magen sedan i måndags.",
                "Beskriv ett symtom och dess startpunkt.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Jag känner mig yr när jag reser mig.",
                "Beskriv när ett besvär uppstår.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Jag är allergisk mot nötter.",
                "Informera om en allergi; anpassa ämnet till din situation.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Kan du förklara hur medicinen ska tas?",
                "Be personalen förtydliga en ordination.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Jag behöver en tolk för att förstå allt.",
                "Be om språkligt stöd vid vårdkontakten.",
                "neutral",
                "a2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-work_a2",
        "A2",
        "I kursen och på jobbet",
        "📚",
        [
            PhrasebookEntry(
                "Vet du när mötet börjar?", "Be en kollega om information.", "neutral", "a2-unit-4"
            ),
            PhrasebookEntry(
                "Jag förstår inte vad vi ska göra.",
                "Be om en tydligare uppgift.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Kan du visa ett exempel?",
                "Be om konkret stöd i en förklaring.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Jag skickar filen efter lunch.",
                "Ange när du gör en uppgift.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Är det samma schema nästa vecka?",
                "Kontrollera om arbetstider eller lektioner ändras.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Jag kan inte komma idag eftersom jag är sjuk.",
                "Meddela frånvaro med en kort orsak.",
                "neutral",
                "a2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-shopping_a2",
        "A2",
        "Köp och returer",
        "🛍️",
        [
            PhrasebookEntry(
                "Jag köpte den här igår, men den fungerar inte.",
                "Beskriv ett problem med en vara.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Jag har kvittot här.",
                "Visa underlag vid ett ärende i butiken.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Kan jag byta till en mindre storlek?",
                "Fråga om ett byte, utan att förutsätta butikens villkor.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "När kan jag hämta paketet?",
                "Fråga när en leverans är tillgänglig.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Har ni något billigare alternativ?",
                "Be butikspersonalen visa en annan vara.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Skulle du kunna hjälpa mig att fylla i formuläret?",
                "Be om praktisk hjälp med ett dokument.",
                "neutral",
                "a2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-invitations_a2",
        "A2",
        "Inbjudningar och ändrade planer",
        "🎉",
        [
            PhrasebookEntry(
                "Vill du följa med på en utflykt i helgen?",
                "Bjud in till en gemensam aktivitet.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Tack för inbjudan, jag kommer gärna.", "Tacka ja tydligt.", "neutral", "a2-unit-6"
            ),
            PhrasebookEntry(
                "Tyvärr kan jag inte på lördag. Passar söndag?",
                "Avböj den föreslagna tiden och ge ett alternativ.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Om det regnar kan vi gå på museum istället.",
                "Föreslå en reservplan.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Ska jag ta med något att äta?",
                "Fråga om du kan bidra vid en träff.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Det var länge sedan vi sågs!",
                "Hälsa på en bekant efter lång tid.",
                "informal",
                "a2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "sv-confirming_a2",
        "A2",
        "Kontrollera tider och svar",
        "📅",
        [
            PhrasebookEntry(
                "Menar du den femte eller den femtonde?",
                "Kontrollera ett datum som kan ha hörts fel.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Jo, jag kommer, men lite senare.",
                "Motsäg frågan Kommer du inte? och precisera tiden.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Ja, det har jag redan gjort.",
                "Bekräfta att en tidigare nämnd uppgift är klar.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Nej, det kan jag tyvärr inte.",
                "Svara på en fråga om möjlighet att göra något.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Hur länge gäller biljetten?",
                "Kontrollera giltighetstiden.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Kan du skicka datumet i ett mejl?",
                "Be om en skriftlig bekräftelse.",
                "neutral",
                "a2-unit-7",
            ),
        ],
    ),
]
