"""Dutch C1 precise and context-sensitive interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="bronstatus_c1",
        level="C1",
        situation="Bronstatus en reikwijdte",
        icon="📊",
        phrases=[
            PhrasebookEntry(
                "Voor zover ik kan nagaan, is dit bericht nog niet onafhankelijk bevestigd.",
                "De verificatiestatus afbakenen.",
                "formal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Is dat een waarneming of uw interpretatie ervan?",
                "Feit en gevolgtrekking uit elkaar houden.",
                "formal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Die conclusie lijkt mij sterker dan de gegevens rechtvaardigen.",
                "Een te stellige gevolgtrekking betwisten.",
                "formal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Niet alle gevallen vallen binnen de reikwijdte van dit onderzoek.",
                "Generalisatie beperken.",
                "formal",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Bedoelt u hoogstens tien of precies tien?",
                "Een kwantitatieve grens controleren.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Die mogelijkheid is niet uitgesloten, maar ook niet aangetoond.",
                "Twee verschillende bewijsposities onderscheiden.",
                "formal",
                "c1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="redactie_project_c1",
        level="C1",
        situation="Tekst en verantwoordelijkheid verduidelijken",
        icon="✍️",
        phrases=[
            PhrasebookEntry(
                "Kunnen we dit beknopter formuleren zonder de beperking weg te laten?",
                "Betekenisbehoud bij redactie bewaken.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Het tweede deel lijkt een ander onderwerp te hebben.",
                "Een onduidelijke samentrekking bespreken.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Deze opsomming is inhoudelijk helder, maar grammaticaal niet parallel.",
                "Gerichte redactionele feedback geven.",
                "formal",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Wie heeft de controle uitgevoerd voordat het rapport werd gepubliceerd?",
                "Een verzwegen uitvoerder expliciteren.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Laten we de verantwoordelijkheden scherper afbakenen.",
                "Een risico in de taakverdeling bespreken.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Onder deze randvoorwaarden kan ik de voortgang niet waarborgen.",
                "Een professionele beperking aangeven.",
                "formal",
                "c1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        id="toon_register_c1",
        level="C1",
        situation="Toon en relatie bewaken",
        icon="💬",
        phrases=[
            PhrasebookEntry(
                "Ik merk enige aarzeling. Welk bezwaar houdt u nog tegen?",
                "Een impliciete reactie bespreekbaar maken.",
                "formal",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Bedoel je dat als voorstel of als een besluit?",
                "De bedoeling van een uiting controleren.",
                "informal",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Ik wil je niet onder druk zetten; neem gerust tijd om na te denken.",
                "Onbedoelde druk wegnemen.",
                "informal",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Deze formulering klinkt verplichtender dan bedoeld.",
                "Een registerwijziging inhoudelijk beoordelen.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "We kunnen de brief toegankelijker maken zonder minder precies te worden.",
                "Een redactioneel doel afspreken.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Dat is een huisstijlkeuze, geen algemene grammaticaregel.",
                "Een normoordeel afbakenen.",
                "neutral",
                "c1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        id="betoog_rapport_c1",
        level="C1",
        situation="Argumenteren en rapporteren",
        icon="🗂️",
        phrases=[
            PhrasebookEntry(
                "Die tegenwerping is terecht, maar tast niet de volledige redenering aan.",
                "Een kritiekpunt gedeeltelijk erkennen.",
                "formal",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Op welke premisse berust die gevolgtrekking?",
                "Het uitgangspunt van een argument onderzoeken.",
                "formal",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Het voorbeeld illustreert het probleem, maar bewijst niet hoe vaak het voorkomt.",
                "Illustratie en bewijs uit elkaar houden.",
                "formal",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Ik plaats hierbij de kanttekening dat de gegevens voorlopig zijn.",
                "Een beperking zichtbaar houden.",
                "formal",
                "c1-unit-8",
            ),
            PhrasebookEntry(
                "Met deze ontwikkeling bedoel ik de stijging van het aantal aanvragen.",
                "Een verwijzing eenduidig maken.",
                "neutral",
                "c1-unit-8",
            ),
            PhrasebookEntry(
                "Ik zal de conclusie herzien als die aanvullende gegevens worden bevestigd.",
                "Bereidheid tot inhoudelijke correctie uitspreken.",
                "formal",
                "c1-unit-8",
            ),
        ],
    ),
]
