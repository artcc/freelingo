"""Danish B2 phrases for nuanced collaboration and disagreement."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "da-clarification-b2",
        "B2",
        "Ret en misforståelse præcist",
        "💬",
        [
            PhrasebookEntry(
                "Det var tidsplanen, jeg satte spørgsmålstegn ved, ikke selve idéen.",
                "Afgræns din kritik, når den er blevet opfattet for bredt.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Når du siger alle, mener du så også de midlertidigt ansatte?",
                "Kontrollér, hvem en generel formulering omfatter.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Jeg læser formuleringen anderledes; må jeg forklare hvorfor?",
                "Åbn en saglig samtale om to mulige læsninger.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Det følger ikke nødvendigvis af tallene, at ordningen skal afskaffes.",
                "Udfordr en konklusion uden at afvise selve tallene.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Lad os få skilt de to spørgsmål ad, før vi går videre.",
                "Undgå, at forskellige problemer bliver behandlet som ét.",
                "neutral",
                "b2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-negotiation-b2",
        "B2",
        "Forhandl klare vilkår",
        "🤝",
        [
            PhrasebookEntry(
                "Vi kan acceptere prisen, på betingelse af at leveringen er inkluderet.",
                "Knyt din accept til et konkret vilkår.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Hvor meget råderum har vi med hensyn til datoen?",
                "Undersøg, om et punkt stadig er åbent for forhandling.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Havde vi kendt betingelserne, ville vi have bedt om et andet tilbud.",
                "Forklar et alternativ til en tidligere beslutning.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Vi kan komme jer i møde med prisen, men ikke med betalingsfristen.",
                "Tilbyd en begrænset indrømmelse.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Jeg vil gerne have ændringen bekræftet skriftligt, før vi går videre.",
                "Sikr en fælles forståelse af de ændrede vilkår.",
                "formal",
                "b2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-administration-b2",
        "B2",
        "Spørg til en afgørelse og dens grundlag",
        "📋",
        [
            PhrasebookEntry(
                "Hvilke oplysninger er der lagt vægt på i afgørelsen?",
                "Bed om indsigt i det konkrete beslutningsgrundlag.",
                "formal",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Jeg vil gerne gøre opmærksom på en oplysning, der mangler i sagen.",
                "Supplér sagens materiale uden at antage, at fejlen er bevidst.",
                "formal",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Er arbejdet allerede udført, eller er det kun bestilt?",
                "Skeln mellem en beslutning og dens gennemførelse.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Det fremgår ikke af brevet, hvem der skal følge op.",
                "Påpeg en uklar ansvarsfordeling.",
                "formal",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Kan I oplyse, hvordan jeg gør indsigelse, og hvilken frist der gælder?",
                "Bed om proceduren, før du reagerer på en afgørelse.",
                "formal",
                "b2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-debate-b2",
        "B2",
        "Anerkend og afvej argumenter",
        "⚖️",
        [
            PhrasebookEntry(
                "Det er ganske vist billigere nu, men hvad koster vedligeholdelsen?",
                "Anerkend en besparelse og udvid vurderingen til længere sigt.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Jeg kan følge argumentet, men jeg er ikke enig i konklusionen.",
                "Skeln mellem forståelse af en begrundelse og tilslutning til resultatet.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Jo længere vi udsætter beslutningen, desto sværere bliver planlægningen.",
                "Forklar, hvorfor tidspunktet har betydning for næste skridt.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Selv hvis antallet falder lidt, er der stadig behov for tilbuddet.",
                "Forklar, hvorfor et muligt modargument ikke ændrer din vurdering.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Hvilke hensyn mener du bør veje tungest i den afvejning?",
                "Bed den anden om at gøre sine prioriteringer tydelige.",
                "neutral",
                "b2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-information-b2",
        "B2",
        "Gengiv oplysninger med passende forbehold",
        "🔎",
        [
            PhrasebookEntry(
                "Så vidt jeg kan se, bygger vurderingen på en ret lille stikprøve.",
                "Påpeg en mulig begrænsning uden at erklære resultatet ugyldigt.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Det skulle være afklaret, men jeg har ikke selv set bekræftelsen.",
                "Videregiv en andenhåndsoplysning med tydelig kildeafstand.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Du har vel ikke hørt noget mere om, hvornår de åbner?",
                "Spørg en bekendt, om der er kommet nyt om en fælles sag.",
                "informal",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Det er da lovende, men lad os vente på de endelige tal.",
                "Reagér positivt og bevar samtidig et forbehold.",
                "neutral",
                "b2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-professional-b2",
        "B2",
        "Få en arbejdsaftale helt på plads",
        "📝",
        [
            PhrasebookEntry(
                "Den del tager jeg mig af; hvem følger op på resten?",
                "Afgræns dit eget ansvar og få fordelt de øvrige opgaver.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Skal jeg forstå det sådan, at du beder mig kontakte leverandøren?",
                "Kontrollér, hvem der forventes at handle.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Lad mig sammenfatte, hvad vi har besluttet, og hvad der stadig er åbent.",
                "Afslut et møde med en præcis opsummering.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Skriv gerne konkrete rettelser i referatet inden torsdag klokken tolv.",
                "Bed om en afgrænset tilbagemelding med en tydelig frist.",
                "neutral",
                "b2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-mediation-b2",
        "B2",
        "Bevar samarbejdet under uenighed",
        "🗣️",
        [
            PhrasebookEntry(
                "Jeg tror, vi taler lidt forbi hinanden; lad os begynde med målet.",
                "Flyt en fastlåst samtale tilbage til et fælles udgangspunkt.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Det kan jeg godt forstå, uden at jeg dermed er enig i løsningen.",
                "Anerkend en bekymring uden at acceptere det foreslåede indgreb.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Kunne vi tage den del på tomandshånd efter mødet?",
                "Foreslå en mere diskret ramme for en følsom uenighed.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Hvad ville være et rimeligt første skridt for jer begge?",
                "Hjælp to parter med at finde en konkret fælles handling.",
                "neutral",
                "b2-unit-7",
            ),
        ],
    ),
]
