"""Dutch C2 interpretive and editorial exchanges."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="interpretatie_toon_c2",
        level="C2",
        situation="Interpretatie en ondertoon bespreken",
        icon="🔍",
        phrases=[
            PhrasebookEntry(
                "Uw vraag veronderstelt iets wat nog niet is vastgesteld.",
                "Een verborgen aanname betwisten.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Die beperking wordt gesuggereerd, maar volgt niet noodzakelijk uit de formulering.",
                "Implicatuur van letterlijke betekenis onderscheiden.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Welke contextuele aanwijzing ondersteunt die lezing?",
                "Een interpretatie laten onderbouwen.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Letterlijk klinkt het positief; binnen deze context lees ik het als ironie.",
                "Een niet-letterlijke interpretatie motiveren.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Zonder intonatie blijft een oprechte lezing eveneens mogelijk.",
                "Interpretatieve onzekerheid erkennen.",
                "formal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Dat is wel heel zacht uitgedrukt.",
                "Informeel reageren op een understatement.",
                "informal",
                "c2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        id="retoriek_perspectief_c2",
        level="C2",
        situation="Retoriek en vertelstem analyseren",
        icon="📖",
        phrases=[
            PhrasebookEntry(
                "De retorische vraag maakt het standpunt vanzelfsprekend zonder het te onderbouwen.",
                "Een overtuigingsmiddel kritisch analyseren.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Is hier werkelijk sprake van een tegenstelling, of wordt die alleen opgeroepen?",
                "Een mogelijk valse keuze onderzoeken.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "De herhaling versterkt het effect, niet noodzakelijk het argument.",
                "Stijl en bewijs onderscheiden.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Dit oordeel lijkt bij het personage te horen, niet bij de verteller.",
                "Een perspectiefwisseling bespreken.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "De vrije indirecte rede laat beide stemmen door elkaar klinken.",
                "Een verteltechniek benoemen.",
                "formal",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Ik zou die uitspraak niet zonder meer aan de auteur toeschrijven.",
                "Een te directe auteursinterpretatie begrenzen.",
                "formal",
                "c2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        id="precisie_formeel_c2",
        level="C2",
        situation="Precisie in formele teksten",
        icon="⚖️",
        phrases=[
            PhrasebookEntry(
                "Deze herschrijving lost de dubbelzinnigheid op, maar kiest wel één specifieke lezing.",
                "Het effect van redactie expliciteren.",
                "formal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Welke interpretatie wordt door de oorspronkelijke context gerechtvaardigd?",
                "Voorkomen dat redactie feiten verzint.",
                "formal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "De parafrase verandert het bereik van de ontkenning.",
                "Een betekenisverschuiving signaleren.",
                "formal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "De instemming geldt slechts onder het genoemde voorbehoud.",
                "Een formele beperking behouden.",
                "formal",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Kunt u preciseren op welke gevallen deze bepaling van toepassing is?",
                "De reikwijdte van een regel navragen.",
                "formal",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Het voorstel is verdedigbaar, zij het met de nodige kanttekeningen.",
                "Een genuanceerd formeel oordeel geven.",
                "formal",
                "c2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        id="norm_synthese_c2",
        level="C2",
        situation="Normen en syntheses beoordelen",
        icon="🧭",
        phrases=[
            PhrasebookEntry(
                "Voor welke regio en welk register geldt dat normoordeel?",
                "Een taalkundig oordeel contextualiseren.",
                "formal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Beide vormen zijn standaardtaal; consistentie is hier een redactionele keuze.",
                "Variatie van huisstijl onderscheiden.",
                "formal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Laten we de variant beschrijven zonder de sprekers ervan te stigmatiseren.",
                "Een respectvolle bespreking van variatie bevorderen.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Deze bronnen zijn eensluidend, maar mogelijk niet onafhankelijk.",
                "De bewijskracht van meerdere bronnen afwegen.",
                "formal",
                "c2-unit-8",
            ),
            PhrasebookEntry(
                "De extrapolatie gaat verder dan het waargenomen bereik.",
                "Een te brede generalisatie signaleren.",
                "formal",
                "c2-unit-8",
            ),
            PhrasebookEntry(
                "Mijn synthese behoudt de discrepantie omdat de beschikbare gegevens haar niet oplossen.",
                "Onzekerheid verantwoord zichtbaar laten.",
                "formal",
                "c2-unit-8",
            ),
        ],
    ),
]
