"""Dutch B1 vocabulary for narration, relationships and civic life."""

from app.data._types import VocabularyEntry, VocabularySet

B1_SETS: list[VocabularySet] = [
    VocabularySet(
        id="ervaringen_b1",
        level="B1",
        topic="Gebeurtenissen en reacties",
        unit_ref="b1-unit-1",
        words=[
            VocabularyEntry(
                "de gebeurtenis",
                "noun",
                "Iets wat op een bepaald moment plaatsvindt.",
                "Die gebeurtenis maakte veel indruk.",
            ),
            VocabularyEntry(
                "het ongeluk",
                "noun",
                "Een onverwachte gebeurtenis waarbij schade of letsel ontstaat.",
                "Gelukkig raakte niemand gewond bij het ongeluk.",
            ),
            VocabularyEntry(
                "de omstandigheid",
                "noun",
                "Een situatie die invloed heeft op wat er gebeurt.",
                "De omstandigheden waren moeilijk.",
            ),
            VocabularyEntry(
                "de afloop",
                "noun",
                "De manier waarop een gebeurtenis eindigt.",
                "Het verhaal had een goede afloop.",
            ),
            VocabularyEntry(
                "plotseling",
                "adverb",
                "Zonder dat je het verwacht.",
                "Plotseling ging het licht uit.",
            ),
            VocabularyEntry(
                "uiteindelijk",
                "adverb",
                "Na alles wat daarvoor is gebeurd.",
                "Uiteindelijk kwamen we veilig thuis.",
            ),
            VocabularyEntry(
                "schrikken",
                "verb",
                "Plotseling bang of onrustig worden.",
                "Ik schrok van het harde geluid.",
            ),
            VocabularyEntry(
                "opmerken",
                "verb",
                "Iets zien of horen dat je aandacht trekt.",
                "Ik merkte dat de deur openstond.",
            ),
            VocabularyEntry(
                "meemaken",
                "verb",
                "Zelf bij een gebeurtenis betrokken zijn.",
                "Ik heb zoiets eerder meegemaakt.",
            ),
            VocabularyEntry(
                "opgelucht",
                "adjective",
                "Blij omdat zorgen of spanning voorbij zijn.",
                "We waren opgelucht toen iedereen veilig was.",
            ),
        ],
    ),
    VocabularySet(
        id="informatie_b1",
        level="B1",
        topic="Informatie uitwisselen",
        unit_ref="b1-unit-2",
        words=[
            VocabularyEntry(
                "de toelichting",
                "noun",
                "Extra uitleg die iets duidelijker maakt.",
                "Kunt u een toelichting geven?",
            ),
            VocabularyEntry(
                "de mededeling",
                "noun",
                "Informatie die aan anderen wordt verteld.",
                "De mededeling kwam via e-mail.",
            ),
            VocabularyEntry(
                "het misverstand",
                "noun",
                "Een situatie waarin mensen elkaar verkeerd begrijpen.",
                "We hebben het misverstand opgelost.",
            ),
            VocabularyEntry(
                "de samenvatting",
                "noun",
                "Een korte weergave van de belangrijkste informatie.",
                "Ik stuur een samenvatting van het gesprek.",
            ),
            VocabularyEntry(
                "de voorwaarde",
                "noun",
                "Iets waaraan moet worden voldaan voordat iets anders kan.",
                "De voorwaarden staan in de brief.",
            ),
            VocabularyEntry(
                "navragen",
                "verb",
                "Bij iemand controleren hoe iets zit.",
                "Ik zal de openingstijden navragen.",
            ),
            VocabularyEntry(
                "doorgeven",
                "verb",
                "Informatie naar iemand anders overbrengen.",
                "Wil je mijn boodschap doorgeven?",
            ),
            VocabularyEntry(
                "bedoelen",
                "verb",
                "Een bepaalde betekenis of bedoeling hebben.",
                "Wat bedoelt u precies?",
            ),
            VocabularyEntry(
                "duidelijk",
                "adjective",
                "Goed te begrijpen of waar te nemen.",
                "De uitleg was duidelijk.",
            ),
            VocabularyEntry(
                "waarschijnlijk",
                "adverb",
                "Met een grote kans dat het zo is.",
                "Hij komt waarschijnlijk morgen.",
            ),
        ],
    ),
    VocabularySet(
        id="relaties_b1",
        level="B1",
        topic="Omgaan met elkaar",
        unit_ref="b1-unit-3",
        words=[
            VocabularyEntry(
                "het vertrouwen",
                "noun",
                "Het gevoel dat iemand betrouwbaar is of iets goed zal gaan.",
                "Ik heb vertrouwen in onze samenwerking.",
            ),
            VocabularyEntry(
                "de verwachting",
                "noun",
                "Wat je denkt of hoopt dat zal gebeuren.",
                "We bespreken onze verwachtingen.",
            ),
            VocabularyEntry(
                "het meningsverschil",
                "noun",
                "Een situatie waarin mensen ergens anders over denken.",
                "We hebben een meningsverschil over de planning.",
            ),
            VocabularyEntry(
                "de grens",
                "noun",
                "Een punt waar iets ophoudt of niet meer aanvaardbaar is.",
                "Het is belangrijk om je grenzen aan te geven.",
            ),
            VocabularyEntry(
                "de steun", "noun", "Hulp waardoor iemand verder kan.", "Bedankt voor je steun."
            ),
            VocabularyEntry(
                "rekening houden met",
                "phrase",
                "Iets meenemen bij wat je beslist of doet.",
                "We houden rekening met jouw werktijden.",
            ),
            VocabularyEntry(
                "samenwerken",
                "verb",
                "Met anderen aan hetzelfde doel werken.",
                "Ik werk graag met haar samen.",
            ),
            VocabularyEntry(
                "vertrouwen",
                "verb",
                "Geloven dat iemand eerlijk of betrouwbaar is.",
                "Je kunt op hem vertrouwen.",
            ),
            VocabularyEntry(
                "respecteren",
                "verb",
                "Iemands grenzen, rechten of keuzes serieus nemen.",
                "We respecteren elkaars mening.",
            ),
            VocabularyEntry(
                "teleurgesteld",
                "adjective",
                "Verdrietig omdat iets niet aan een verwachting voldoet.",
                "Ze was teleurgesteld over de afzegging.",
            ),
        ],
    ),
    VocabularySet(
        id="regelen_b1",
        level="B1",
        topic="Aanvragen en administratie",
        unit_ref="b1-unit-4",
        words=[
            VocabularyEntry(
                "de aanvraag",
                "noun",
                "Een verzoek om een dienst, toestemming of voorziening.",
                "Mijn aanvraag wordt deze week behandeld.",
            ),
            VocabularyEntry(
                "de gemeente",
                "noun",
                "Een lokaal bestuursgebied en de organisatie die het bestuurt.",
                "Ik meld mijn verhuizing bij de gemeente.",
            ),
            VocabularyEntry(
                "de vergunning",
                "noun",
                "Officiële toestemming om iets te doen.",
                "Voor deze verbouwing is een vergunning nodig.",
            ),
            VocabularyEntry(
                "het bewijs",
                "noun",
                "Informatie of een document waarmee je iets kunt aantonen.",
                "Neem een bewijs van inschrijving mee.",
            ),
            VocabularyEntry(
                "de termijn",
                "noun",
                "De beschikbare of afgesproken periode voor een handeling.",
                "U krijgt binnen de genoemde termijn antwoord.",
            ),
            VocabularyEntry(
                "de verzekering",
                "noun",
                "Een overeenkomst die bepaalde risico's tegen betaling dekt.",
                "Lees wat uw verzekering vergoedt.",
            ),
            VocabularyEntry(
                "indienen",
                "verb",
                "Een document officieel aan een organisatie geven.",
                "Ik dien de aanvraag online in.",
            ),
            VocabularyEntry(
                "ondertekenen",
                "verb",
                "Je handtekening op een document zetten.",
                "U moet het formulier ondertekenen.",
            ),
            VocabularyEntry(
                "behandelen",
                "verb",
                "Een zaak bekijken en er actie op ondernemen.",
                "De afdeling behandelt mijn verzoek.",
            ),
            VocabularyEntry(
                "ontbreken",
                "verb",
                "Niet aanwezig zijn terwijl iets nodig of verwacht is.",
                "Er ontbreekt een bijlage.",
            ),
        ],
    ),
    VocabularySet(
        id="keuzes_b1",
        level="B1",
        topic="Voor- en nadelen",
        unit_ref="b1-unit-5",
        words=[
            VocabularyEntry(
                "het voordeel",
                "noun",
                "Een gunstige kant van iets.",
                "Een voordeel is de korte reistijd.",
            ),
            VocabularyEntry(
                "het nadeel",
                "noun",
                "Een ongunstige kant van iets.",
                "Het grootste nadeel is de prijs.",
            ),
            VocabularyEntry(
                "de mogelijkheid",
                "noun",
                "Iets wat kan gebeuren of gedaan kan worden.",
                "We onderzoeken beide mogelijkheden.",
            ),
            VocabularyEntry(
                "de keuze",
                "noun",
                "Een beslissing tussen verschillende opties.",
                "Dit is een moeilijke keuze.",
            ),
            VocabularyEntry(
                "het risico",
                "noun",
                "De kans op een ongunstige gebeurtenis of uitkomst.",
                "We willen het risico beperken.",
            ),
            VocabularyEntry(
                "beslissen", "verb", "Bepalen wat je gaat doen.", "We beslissen morgen."
            ),
            VocabularyEntry(
                "aanraden",
                "verb",
                "Zeggen dat je een bepaalde keuze goed vindt.",
                "Ik raad je aan eerst informatie te vragen.",
            ),
            VocabularyEntry(
                "twijfelen",
                "verb",
                "Niet zeker weten wat juist of verstandig is.",
                "Ik twijfel tussen twee opleidingen.",
            ),
            VocabularyEntry(
                "haalbaar",
                "adjective",
                "Mogelijk met de beschikbare tijd en middelen.",
                "Is dit plan haalbaar?",
            ),
            VocabularyEntry(
                "liever",
                "adverb",
                "Met een grotere voorkeur dan voor iets anders.",
                "Ik zou liever dichter bij mijn werk wonen.",
            ),
        ],
    ),
    VocabularySet(
        id="omgeving_b1",
        level="B1",
        topic="Buurt en milieu",
        unit_ref="b1-unit-6",
        words=[
            VocabularyEntry(
                "de buurt",
                "noun",
                "Het gebied dicht bij een woonplek.",
                "In onze buurt komt een nieuw park.",
            ),
            VocabularyEntry(
                "de bewoner",
                "noun",
                "Iemand die in een bepaalde woning of plaats woont.",
                "Bewoners geven hun mening over het plan.",
            ),
            VocabularyEntry(
                "het afval",
                "noun",
                "Materialen en spullen die worden weggegooid.",
                "We scheiden ons afval.",
            ),
            VocabularyEntry(
                "de overlast",
                "noun",
                "Hinder die mensen van iets of iemand ervaren.",
                "De werkzaamheden veroorzaken geluidsoverlast.",
            ),
            VocabularyEntry(
                "het verkeer",
                "noun",
                "Voertuigen en mensen die zich over wegen verplaatsen.",
                "Er is veel verkeer in de straat.",
            ),
            VocabularyEntry(
                "de maatregel",
                "noun",
                "Een handeling of regel om een doel te bereiken.",
                "Deze maatregel moet de straat veiliger maken.",
            ),
            VocabularyEntry(
                "besparen",
                "verb",
                "Minder van iets gebruiken of uitgeven.",
                "We besparen energie door beter te isoleren.",
            ),
            VocabularyEntry(
                "vervuilen",
                "verb",
                "Vuil of schadelijke stoffen in de omgeving brengen.",
                "Afval kan het water vervuilen.",
            ),
            VocabularyEntry(
                "duurzaam",
                "adjective",
                "Gericht op langdurig verantwoord gebruik van middelen.",
                "We zoeken een duurzame oplossing.",
            ),
            VocabularyEntry(
                "veilig", "adjective", "Met weinig gevaar of risico.", "Deze fietsroute is veilig."
            ),
        ],
    ),
    VocabularySet(
        id="ontwikkeling_b1",
        level="B1",
        topic="Leren en gewoonten",
        unit_ref="b1-unit-7",
        words=[
            VocabularyEntry(
                "de vooruitgang",
                "noun",
                "Een verbetering ten opzichte van eerder.",
                "Ik merk vooruitgang in mijn uitspraak.",
            ),
            VocabularyEntry(
                "het doel", "noun", "Wat je wilt bereiken.", "Mijn doel is zelfstandiger spreken."
            ),
            VocabularyEntry(
                "de inspanning",
                "noun",
                "De energie of moeite die je voor iets gebruikt.",
                "Een nieuwe gewoonte vraagt inspanning.",
            ),
            VocabularyEntry(
                "de vaardigheid",
                "noun",
                "Iets wat je door kennis en oefening kunt doen.",
                "Luisteren is een belangrijke vaardigheid.",
            ),
            VocabularyEntry(
                "het resultaat",
                "noun",
                "Wat een handeling of proces oplevert.",
                "Het resultaat is beter dan verwacht.",
            ),
            VocabularyEntry(
                "volhouden",
                "verb",
                "Doorgaan ondanks moeite.",
                "Ik probeer mijn dagelijkse oefening vol te houden.",
            ),
            VocabularyEntry(
                "verbeteren",
                "verb",
                "Beter maken of beter worden.",
                "Mijn Nederlands is verbeterd.",
            ),
            VocabularyEntry(
                "wennen",
                "verb",
                "Geleidelijk vertrouwd raken met iets nieuws.",
                "Ik moet aan het nieuwe rooster wennen.",
            ),
            VocabularyEntry(
                "regelmatig", "adverb", "Vaak en met enige herhaling.", "Ik oefen regelmatig."
            ),
            VocabularyEntry(
                "zelfstandig",
                "adjective",
                "Zonder voortdurend hulp van anderen nodig te hebben.",
                "Ik kan deze taak zelfstandig uitvoeren.",
            ),
        ],
    ),
    VocabularySet(
        id="overleg_b1",
        level="B1",
        topic="Overleggen en afspraken vastleggen",
        unit_ref="b1-unit-8",
        words=[
            VocabularyEntry(
                "het overleg",
                "noun",
                "Een gesprek om informatie of besluiten af te stemmen.",
                "Na het overleg sturen we een verslag.",
            ),
            VocabularyEntry(
                "het voorstel",
                "noun",
                "Een idee dat anderen kunnen bespreken en beoordelen.",
                "Ik heb een voorstel voor de planning.",
            ),
            VocabularyEntry(
                "het verslag",
                "noun",
                "Een geschreven weergave van wat is gebeurd of besproken.",
                "De afspraken staan in het verslag.",
            ),
            VocabularyEntry(
                "de taak",
                "noun",
                "Werk dat iemand moet uitvoeren.",
                "Iedereen krijgt een duidelijke taak.",
            ),
            VocabularyEntry(
                "de oplossing",
                "noun",
                "Een manier om een probleem weg te nemen.",
                "We zoeken samen een oplossing.",
            ),
            VocabularyEntry(
                "akkoord gaan",
                "phrase",
                "Instemmen met een voorstel of afspraak.",
                "Ik ga akkoord met de nieuwe datum.",
            ),
            VocabularyEntry(
                "samenvatten",
                "verb",
                "De belangrijkste informatie kort weergeven.",
                "Kun je de afspraken samenvatten?",
            ),
            VocabularyEntry(
                "toelichten",
                "verb",
                "Met extra uitleg duidelijk maken.",
                "Wil je je voorstel toelichten?",
            ),
            VocabularyEntry(
                "afstemmen",
                "verb",
                "Zorgen dat plannen of handelingen bij elkaar passen.",
                "We stemmen onze taken op elkaar af.",
            ),
            VocabularyEntry(
                "voorlopig",
                "adverb",
                "Voor nu, terwijl later nog iets kan veranderen.",
                "Voorlopig houden we deze planning aan.",
            ),
        ],
    ),
]
