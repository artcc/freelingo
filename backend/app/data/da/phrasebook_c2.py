"""Danish C2 phrases for exact commitments, tact and mediation."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "da-alternatives-dialogue-c2",
        "C2",
        "Tal om det, der kunne være sket",
        "🧭",
        [
            PhrasebookEntry(
                "Havde vi kendt omfanget dengang, ville vi stå med en anden plan i dag.",
                "Forbind et tænkt fortidigt grundlag med en tænkt nutidig situation.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Det kunne måske have begrænset skaden; det ved vi ikke med sikkerhed.",
                "Undgå at gøre en mulig alternativ følge til et sikkert udfald.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Mener du, at hun havde lovet at ringe, eller at nogen siger, hun faktisk ringede?",
                "Afklar to forskellige læsninger af hun skulle have ringet.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Vi skal vurdere beslutningen ud fra den viden, der var til rådighed på det tidspunkt.",
                "Skeln mellem en vurdering af beslutningen og viden om det senere udfald.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Jeg tager ansvar for, at vi reagerede sent, men ikke for forhold, vi ikke kendte.",
                "Afgræns dit ansvar konkret uden at bortforklare den erkendte fejl.",
                "formal",
                "c2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-premises-dialogue-c2",
        "C2",
        "Svar uden at acceptere en skjult præmis",
        "🔍",
        [
            PhrasebookEntry(
                "Før jeg svarer på hvorfor, må vi afklare, om det faktisk er sket.",
                "Stop en begrundelsesdiskussion, som bygger på et ubekræftet hændelsesforløb.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Jeg er uenig i betegnelsen besparelse; udgiften er flyttet til næste år.",
                "Ret en kategorisering uden at benægte den underliggende ændring.",
                "formal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Det er en mulig læsning, men den følger ikke af ordlyden alene.",
                "Skeln mellem modpartens fortolkning og det direkte sagte.",
                "formal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Jeg nævnte de to afdelinger som eksempler, ikke som en udtømmende liste.",
                "Ophæv en utilsigtet antydning af, at andre afdelinger er udelukket.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Når du kalder det endnu en fejl, hvilken tidligere fejl tænker du så på?",
                "Gør spørgsmålets forudsatte baggrund til genstand for afklaring.",
                "neutral",
                "c2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-terms-dialogue-c2",
        "C2",
        "Forhandl præcise rettigheder og tilsagn",
        "📑",
        [
            PhrasebookEntry(
                "Vi kan drøfte en dispensation, men det ændrer ikke den gældende regel.",
                "Åbn for en konkret undtagelse uden at love godkendelse.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Gælder undtagelsen kun fristen, eller også kravet om dokumentation?",
                "Afklar rækkevidden af en uklar bestemmelse.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Vi frafalder gebyret i denne sag uden dermed at ændre betalingsvilkårene fremover.",
                "Giv en afgrænset indrømmelse og gør dens rækkevidde tydelig.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "At bilaget ikke er påkrævet, betyder ikke, at det er forbudt at vedlægge det.",
                "Ret en praktisk misforståelse mellem fritagelse og forbud.",
                "neutral",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Jeg kan undersøge muligheden, men jeg har ikke mandat til at give tilsagn.",
                "Skeln mellem din undersøgende rolle og en beslutningsret, du ikke har.",
                "neutral",
                "c2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-perspectives-dialogue-c2",
        "C2",
        "Gengiv modargumentet loyalt",
        "⚖️",
        [
            PhrasebookEntry(
                "Det er nok en hurtig løsning, men den flytter en del af arbejdet over på jer.",
                "Anerkend en fordel og fremhæv et relevant modhensyn.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Jeg vedgår svagheden i beregningen; det gør ikke bekymringen for kapaciteten irrelevant.",
                "Indrøm et konkret problem uden at opgive et selvstændigt argument.",
                "formal",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Hvis jeg skal gengive dit synspunkt loyalt, er det så især fordelingen, du anfægter?",
                "Kontrollér din sammenfatning, før du argumenterer imod den.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Den vurdering ligger hos figuren; fortælleren bekræfter den ikke direkte.",
                "Adskil perspektiver i en litterær drøftelse.",
                "formal",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Vi er enige om målet, men vægter risikoen forskelligt. Det bør fremgå af referatet.",
                "Synliggør både fælles grund og en reel, tilbageværende uenighed.",
                "neutral",
                "c2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-rapport-dialogue-c2",
        "C2",
        "Red samtalen, når tonen rammer skævt",
        "💬",
        [
            PhrasebookEntry(
                "Det skulle have været selvironisk, men jeg kan høre, at det kom til at ramme dig.",
                "Skeln mellem din hensigt og den virkning, bemærkningen fik.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Den bemærkning var unødvendig. Undskyld; jeg holder mig til sagen.",
                "Tag ansvar for en personlig stikpille uden at forklare den væk.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Et hurtigt møde, sagde vi. Kaffen har da i hvert fald fået lov at trække.",
                "Brug mildt ironisk ekko med kolleger, der deler oplevelsen af et langt møde.",
                "informal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Må jeg rette én ting i min formulering, før du svarer?",
                "Bed kort om ordet for at forhindre, at modparten svarer på en fejl.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Jeg mente ikke, at du skulle trække dit forslag. Jeg bad om en præcisering af fristen.",
                "Afgræns den ønskede ændring efter en misforstået indvending.",
                "neutral",
                "c2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-mediation-dialogue-c2",
        "C2",
        "Gør det komplekse klart uden betydningsskred",
        "✍️",
        [
            PhrasebookEntry(
                "Hvis vi skriver 'hendes' her, kan læseren være i tvivl om, hvem der ejer materialet.",
                "Påpeg en konkret referencetvetydighed under fælles redigering.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Lad os gentage verbet; ellers ser det ud, som om begge parter har lovet det samme.",
                "Genskab en væsentlig forskel, som en forkortet formulering skjuler.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Undersøgelsen viser et sammenfald, men den fastslår ikke, hvad der er årsag til hvad.",
                "Formidl et resultat uden at opgradere forbindelsen til årsag.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Min anbefaling går et skridt videre end kildernes konklusion, og det vil jeg gøre tydeligt.",
                "Adskil din praktiske vurdering fra det dokumenterede grundlag.",
                "formal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Kort sagt kan vi afprøve løsningen, hvis begge parter accepterer en tidsbegrænset ordning.",
                "Afrund en længere drøftelse med en mulighed og dens afgørende betingelse.",
                "neutral",
                "c2-unit-7",
            ),
        ],
    ),
]
