"""Danish B1 phrases for practical independent interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "da-settling-b1",
        "B1",
        "Fortæl om at flytte og falde til",
        "🏡",
        [
            PhrasebookEntry(
                "Vi havde kun boet her i en uge, da vi mødte vores naboer.",
                "Giv baggrund for et første møde.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Jeg plejer at cykle, men dengang tog jeg bussen hver dag.",
                "Sammenlign din nuværende hverdag med en tidligere vane.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Det tog lidt tid, før jeg følte mig hjemme.",
                "Beskriv, hvordan du faldt til et nyt sted.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Mens vi pakkede ud, kom naboen forbi med kaffe.",
                "Forbind to samtidige hændelser i en fortælling.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Jeg savner havnen, men jeg er glad for at bo tættere på mit arbejde.",
                "Fortæl om både et savn og en fordel ved din flytning.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Til sidst fandt vi ud af, hvor alle kasserne skulle stå.",
                "Afslut en fortælling om at indrette en bolig.",
                "neutral",
                "b1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-neighbours-b1",
        "B1",
        "Tal med naboerne om fælles hensyn",
        "🏘️",
        [
            PhrasebookEntry(
                "Jeg skriver, fordi jeg ikke kan få døren til kælderen op.",
                "Forklar viceværten, hvorfor du henvender dig.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Er det dig, der har reserveret vaskemaskinen?",
                "Find ud af, hvem der bruger en fælles facilitet.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Vil du sige til, hvis musikken bliver for høj?",
                "Vis hensyn, når du holder en mindre sammenkomst.",
                "informal",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Vi kan vaske trappen på skift, så ingen står med det hele.",
                "Foreslå en rimelig fordeling af en praktisk opgave.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "De kasser, jeg lånte af dig, er klar til at blive hentet.",
                "Giv besked om, at lånte ting kan afleveres tilbage.",
                "informal",
                "b1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-citizen-b1",
        "B1",
        "Få afklaret et brev eller en ansøgning",
        "📄",
        [
            PhrasebookEntry(
                "Jeg vil gerne vide, hvilke bilag der mangler.",
                "Bed om en konkret liste over manglende dokumenter.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Skal jeg møde op personligt, eller kan det klares digitalt?",
                "Undersøg, hvordan en henvendelse skal håndteres.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Kan jeg få en kvittering for, at I har modtaget ansøgningen?",
                "Bed om bekræftelse på modtagelsen.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Jeg beder om en kort forklaring på, hvad jeg skal gøre nu.",
                "Skriv, når et formelt brev ikke giver dig et tydeligt næste skridt.",
                "formal",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Betyder det, at jeg ikke behøver at sende originalen?",
                "Kontrollér, om en kopi er tilstrækkelig.",
                "neutral",
                "b1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-work-study-b1",
        "B1",
        "Afklar opgaver på arbejde og kursus",
        "📚",
        [
            PhrasebookEntry(
                "Ved du, hvornår vi får den nye vagtplan?",
                "Stil et indirekte spørgsmål til en kollega.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Kan du uddybe, hvad vi skal aflevere?",
                "Bed underviseren om mere præcise krav til en opgave.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Hun sagde, at vi skulle vente på en bekræftelse.",
                "Gengiv en kollegas besked om næste skridt.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Jeg tager noter, så jeg kan forklare det til resten af holdet.",
                "Fortæl, hvorfor du skriver under et møde.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Jeg er ikke helt med; kan du tage det sidste en gang til?",
                "Sig åbent, at du har brug for en gentagelse.",
                "informal",
                "b1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-planning-b1",
        "B1",
        "Lav en plan med et alternativ",
        "🗓️",
        [
            PhrasebookEntry(
                "Hvis vi tog et tidligere tog, ville vi have mere tid derovre.",
                "Foreslå en anden rejseplan og dens fordel.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Jeg regner med at komme, men jeg kan først svare endeligt i morgen.",
                "Giv et foreløbigt svar uden at love for meget.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Vi har ikke råd til begge dele, så vi må vælge.",
                "Forklar en økonomisk begrænsning i fælles planlægning.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Hvad gør vi, hvis vejret bliver dårligt?",
                "Åbn for at aftale en reserveplan.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Skal vi lige sove på det og tale sammen i morgen?",
                "Foreslå en tænkepause, før I beslutter jer.",
                "informal",
                "b1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-participation-b1",
        "B1",
        "Vær med i en forening",
        "🤝",
        [
            PhrasebookEntry(
                "Jeg er ny her; hvem skal jeg tale med om at blive medlem?",
                "Find den rette kontaktperson i en forening.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Jeg kan godt stå for kaffen, hvis en anden køber ind.",
                "Tilbyd en konkret opgave med en tydelig betingelse.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Vi kan jo hjælpe hinanden med at stille op.",
                "Foreslå en fælles indsats, som virker oplagt i situationen.",
                "informal",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Der kommer nok flere, når de har fri fra arbejde.",
                "Giv et forsigtigt bud på, hvorfor ikke alle er mødt endnu.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Tak for i dag, det var hyggeligt at være med.",
                "Tag afsked efter en fælles aktivitet.",
                "informal",
                "b1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-consumption-b1",
        "B1",
        "Tal om køb, fejl og mindre spild",
        "♻️",
        [
            PhrasebookEntry(
                "Kan den repareres, eller skal hele delen skiftes?",
                "Undersøg mulighederne, før du køber nyt.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Selv om den var på tilbud, forventer jeg, at den virker.",
                "Fremsæt en saglig reklamation over en defekt vare.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Jeg kan undvære den indtil fredag, men derefter skal jeg bruge den.",
                "Aftal en tidsgrænse med et værksted.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Vi kunne købe færre ting og bruge lidt mere på kvalitet.",
                "Foreslå et ændret forbrugsmønster.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Lad os bruge resterne først, så vi ikke smider mad ud.",
                "Foreslå en praktisk måde at mindske madspild på.",
                "informal",
                "b1-unit-7",
            ),
        ],
    ),
]
