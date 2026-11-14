"""Danish C1 phrases for qualified agreement and everyday public participation."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "da-evidence-dialogue-c1",
        "C1",
        "Vurdér grundlaget sammen",
        "🔎",
        [
            PhrasebookEntry(
                "Det taler for løsningen, men vi mangler stadig tal for vinterhalvåret.",
                "Fremlæg et positivt resultat med en konkret begrænsning.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Kan vi skelne mellem det, vi har målt, og det, vi regner med?",
                "Afklar grundlaget for en fælles vurdering på et møde.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Oplysningen stammer fra udlejeren; jeg har ikke selv efterprøvet den.",
                "Gengiv en relevant kilde uden at påtage dig en ubegrundet sikkerhed.",
                "formal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Så vidt jeg kan se, gælder beregningen kun de opvarmede rum.",
                "Afgræns en foreløbig læsning af et teknisk bilag.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Hvad skulle vi undersøge for at kunne sige noget mere sikkert?",
                "Flyt en uafklaret diskussion videre mod konkret viden.",
                "neutral",
                "c1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-agreement-dialogue-c1",
        "C1",
        "Forhandl en realistisk aftale",
        "🤝",
        [
            PhrasebookEntry(
                "Får vi materialet senest tirsdag, kan vi sende et udkast fredag.",
                "Knyt dit tilbud til en tydelig forudsætning.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Vi kan rykke datoen, hvis I til gengæld kan samle leveringen.",
                "Tilbyd en indrømmelse med en konkret modydelse.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Prisen kan vi godt acceptere; det er betalingsfristen, der er vanskelig.",
                "Afgræns uenigheden, så forhandlingen kan fortsætte.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Lad os skrive forbeholdet ind, så vi ikke husker aftalen forskelligt.",
                "Foreslå en fælles skriftlig præcisering uden at mistænkeliggøre modparten.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Jeg har en bagkant klokken tre. Kan vi nå at afklare de sidste vilkår inden da?",
                "Gør opmærksom på din tidsgrænse og foreslå en prioritering.",
                "informal",
                "c1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-association-dialogue-c1",
        "C1",
        "Deltag i foreningens beslutninger",
        "🏘️",
        [
            PhrasebookEntry(
                "Jeg vil gerne have min indsigelse ført til referat.",
                "Sikr, at din begrundede uenighed fremgår af mødeprotokollen.",
                "formal",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Jeg påtager mig at indhente tilbuddene, men valget skal træffes af bestyrelsen.",
                "Adskil din opgave fra den formelle beslutningskompetence.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Er det et forslag til afstemning eller blot en orientering?",
                "Afklar, hvad forsamlingen forventes at tage stilling til.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Hvem følger op, hvis vi ikke har fået svar inden fristen?",
                "Gør en vedtaget plan praktisk anvendelig.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Jeg er inhabil i den sag og deltager derfor ikke i behandlingen.",
                "Gør åbent opmærksom på en interessekonflikt.",
                "formal",
                "c1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-disagreement-dialogue-c1",
        "C1",
        "Afklar en uenighed uden at skærpe den",
        "🎯",
        [
            PhrasebookEntry(
                "Jeg hører dig sige, at omfanget er problemet. Er det rigtigt forstået?",
                "Afprøv din forståelse, før du svarer på modpartens kritik.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Når du siger alle, mener du så alle afdelinger eller alle medarbejdere?",
                "Afklar, hvilken gruppe et udsagn vedrører.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Det er ikke formålet, jeg anfægter, men den måde, vi vil nå det på.",
                "Fasthold en kritisk indvending og anerkend samtidig det fælles mål.",
                "formal",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Vi behøver ikke være enige om forklaringen for at aftale næste skridt.",
                "Skab mulighed for handling uden at fremstille uenigheden som løst.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Lad mig skille de to spørgsmål ad, før jeg svarer.",
                "Undgå et uklart samlet svar på spørgsmål med forskellige forudsætninger.",
                "neutral",
                "c1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-tact-dialogue-c1",
        "C1",
        "Vær venlig og tydelig på samme tid",
        "💬",
        [
            PhrasebookEntry(
                "Jeg ville høre, om der var mulighed for at få fristen forlænget.",
                "Fremsæt en høflig anmodning til en sagsbehandler eller samarbejdspartner.",
                "formal",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Det kan jeg desværre ikke påtage mig, men jeg kan hjælpe med overdragelsen.",
                "Afslå opgaven og tilbyd en afgrænset hjælp, du faktisk kan yde.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Jeg havde ellers forstået, at vi skulle vente på de sidste svar.",
                "Markér en forskel mellem den aktuelle plan og din hidtidige forståelse.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Det er vist mig, der har blandet datoerne sammen. Lad os lige se efter.",
                "Tag et foreløbigt ansvar og foreslå at kontrollere oplysningen sammen.",
                "informal",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Vi har jo ikke aftalt en pris endnu, så jeg kan ikke bekræfte bestillingen.",
                "Henvis til en fælles kendt mangel; undgå jo, hvis forholdet er omstridt.",
                "neutral",
                "c1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "da-tone-and-text-c1",
        "C1",
        "Fra den levende fortælling til den klare tekst",
        "✍️",
        [
            PhrasebookEntry(
                "Og så stod jeg dér med en paraply, der var vendt på vrangen.",
                "Giv en hverdagsfortælling et konkret og let humoristisk højdepunkt.",
                "informal",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Jeg er ikke helt med på, om du mener det alvorligt.",
                "Afklar mulig ironi uden at kræve, at modparten har været entydig.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Den joke landede vist ikke. Jeg prøver lige igen uden omsvøb.",
                "Registrér en manglende fælles forståelse og skift til direkte tale.",
                "informal",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Kan vi skrive navnet i stedet for 'det', så henvisningen bliver klar?",
                "Foreslå en konkret redigering af et uklart referat.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Jeg har gjort teksten kortere, men beholdt både betingelsen og forbeholdet.",
                "Forklar, hvordan du har redigeret en besked med bevaret indhold.",
                "neutral",
                "c1-unit-7",
            ),
        ],
    ),
]
