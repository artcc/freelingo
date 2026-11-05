"""Dutch A2: past events, comparisons and connected sentences."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="perfectum",
        title="Het perfectum met hebben en zijn",
        level="A2",
        category="Werkwoorden",
        summary="Vertel wat je hebt gedaan en wat er is gebeurd.",
        explanation="Het perfectum bestaat uit hebben of zijn met een voltooid deelwoord: Ik heb gewerkt; Zij is gekomen. Veel handelingen krijgen hebben. Zijn hoort onder meer bij een verandering van toestand en bij een verplaatsing met een bestemming: Hij is gevallen; We zijn naar huis gefietst. Bij fietsen als activiteit kan hebben: We hebben twee uur gefietst.\n\nLeer het hulpwerkwoord bij ieder werkwoord. Het perfectum komt vaak voor bij afgeronde gebeurtenissen, maar het kan ook een periode tot nu beschrijven: Ik heb hier altijd gewoond. Een tijdwoord als gisteren verplicht niet tot één bepaalde verleden tijd.",
        rules=[
            "Zet het hulpwerkwoord op de persoonsvormplaats en het deelwoord achteraan.",
            "Leer komen → is gekomen en doen → heeft gedaan.",
            "Let bij beweging op activiteit tegenover verandering van plaats.",
        ],
        examples=[
            GrammarExample("Gisteren heb ik gekookt."),
            GrammarExample("We zijn naar Groningen gereden."),
            GrammarExample("Ik heb de hele middag gewandeld."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik heb naar huis gegaan.",
                "Ik ben naar huis gegaan.",
                "Gaan vormt hier het perfectum met zijn.",
            )
        ],
        related=["voltooid-deelwoord", "verleden-tijd"],
    ),
    GrammarTopic(
        slug="voltooid-deelwoord",
        title="Gewerkt, gebeld en meegenomen",
        level="A2",
        category="Spelling",
        summary="Vorm regelmatige deelwoorden en herken onregelmatige vormen.",
        explanation="Een regelmatig deelwoord krijgt meestal ge- en -t of -d. Kijk voor die uitgang naar de laatste medeklinker van het werkwoord zonder -en: een stemloze medeklinker zoals in werken geeft gewerkt; bellen geeft gebeld. Bij reizen en leven kijk je naar z en v: gereisd, geleefd, ook al eindigt de geschreven stam op s of f.\n\nBij scheidbare werkwoorden komt ge tussen de delen: opbellen → opgebeld. Onbeklemtoonde voorvoegsels be-, ge-, her-, ont- en ver- krijgen doorgaans geen extra ge: betaald, verteld. Leer onregelmatige deelwoorden apart: gezien, genomen, geschreven.",
        rules=[
            "Werkte/gewerkt, belde/gebeld.",
            "Gebruik de onderliggende v of z bij leven en reizen.",
            "Opstaan → opgestaan; begrijpen → begrepen.",
        ],
        examples=[
            GrammarExample("Ik heb mijn moeder opgebeld."),
            GrammarExample("Zij heeft de rekening betaald."),
            GrammarExample("We hebben veel gereisd."),
        ],
        common_mistakes=[
            GrammarMistake("Ik heb gebetaald.", "Ik heb betaald.", "Betalen krijgt geen extra ge-.")
        ],
        related=["perfectum", "scheidbare-werkwoorden"],
    ),
    GrammarTopic(
        slug="verleden-tijd",
        title="De onvoltooid verleden tijd",
        level="A2",
        category="Werkwoorden",
        summary="Beschrijf vroegere situaties, gewoonten en gebeurtenissen.",
        explanation="Regelmatige werkwoorden krijgen -te(n) of -de(n): ik werkte, wij werkten, ik woonde, wij woonden. De keuze volgt dezelfde stemhebbende of stemloze medeklinker als bij het deelwoord. Leer sterke vormen met hun meervoud: ging/gingen, kwam/kwamen, zag/zagen. Zijn wordt was/waren; hebben wordt had/hadden.\n\nGebruik deze tijd vaak voor een vroegere toestand, gewoonte of een doorlopend verhaal: Vroeger woonde ik in Zwolle. Het perfectum kan een gebeurtenis introduceren: Ik heb een ongeluk gezien. Het verdere verhaal kan in de verleden tijd staan. Context bepaalt de keuze; beide tijden kunnen bij gisteren voorkomen.",
        rules=[
            "Enkelvoud: werkte; meervoud: werkten.",
            "Leer was/waren en had/hadden als basisvormen.",
            "Gebruik tijdscontext, niet alleen één signaalwoord.",
        ],
        examples=[
            GrammarExample("Als kind woonde ik in Breda."),
            GrammarExample("Gisteren was de winkel dicht."),
            GrammarExample("Ze gingen elke zomer kamperen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Wij was thuis.", "Wij waren thuis.", "Wij vraagt de meervoudsvorm waren."
            )
        ],
        related=["perfectum", "voltooid-deelwoord"],
    ),
    GrammarTopic(
        slug="omdat-dat",
        title="Bijzinnen met omdat en dat",
        level="A2",
        category="Zinsbouw",
        summary="Geef redenen en vertel wat je denkt of weet.",
        explanation="Omdat geeft een reden; dat leidt de inhoud van een gedachte of mededeling in. In zo'n bijzin staan de werkwoorden aan het einde: Ik blijf thuis omdat ik ziek ben; Ik denk dat ze morgen komt. Bij een scheidbaar werkwoord blijven de delen samen: omdat ik vroeg opsta.\n\nBij twee werkwoorden kunnen meerdere volgordes correct zijn: omdat ik heb gewerkt / omdat ik gewerkt heb. Leer eerst één natuurlijk model en herken de andere volgorde. Een bijzin vooraan neemt één zinsdeelplaats in: Omdat ik ziek ben, blijf ik thuis.",
        rules=[
            "Hoofdzin: ik ben ziek; bijzin: omdat ik ziek ben.",
            "Een bijzin vooraan geeft inversie in de hoofdzin.",
            "Dat als voegwoord verwijst niet naar het geslacht van een naamwoord.",
        ],
        examples=[
            GrammarExample("Ik weet dat hij in Arnhem woont."),
            GrammarExample("Omdat het regent, nemen we de bus."),
            GrammarExample("Ze zegt dat ze vroeg opstaat."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik blijf thuis omdat ik ben ziek.",
                "Ik blijf thuis omdat ik ziek ben.",
                "De persoonsvorm staat hier aan het einde van de bijzin.",
            )
        ],
        related=["en-maar-want", "als-wanneer"],
    ),
    GrammarTopic(
        slug="als-wanneer",
        title="Als, wanneer en toen",
        level="A2",
        category="Verbindingen",
        summary="Verbind een gebeurtenis met een tijd of voorwaarde.",
        explanation="Als kan een voorwaarde of herhaalde situatie aangeven: Als het regent, neem ik de bus. Wanneer kan naar een tijdstip vragen of een tijdsbijzin inleiden. Bij toekomstige situaties zijn als en wanneer vaak allebei mogelijk, met een verschil in nadruk.\n\nToen verwijst in een bijzin naar een bepaalde situatie of periode in het verleden: Toen ik klein was, woonde ik in Gouda. Gebruik als bij herhaling in het verleden: Als het regende, bleven we binnen. De werkwoorden staan in deze bijzinnen achteraan.",
        rules=[
            "Toen voor een bepaalde situatie in het verleden.",
            "Als voor een voorwaarde of herhaling.",
            "Een bijzin vooraan wordt gevolgd door de persoonsvorm van de hoofdzin.",
        ],
        examples=[
            GrammarExample("Als ik tijd heb, bel ik je."),
            GrammarExample("Toen ik thuiskwam, was het donker."),
            GrammarExample("Wanneer begint de les?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Als ik tijd heb, ik bel je.",
                "Als ik tijd heb, bel ik je.",
                "De hoofdzin begint na de bijzin met de persoonsvorm.",
            )
        ],
        related=["omdat-dat", "verleden-tijd"],
    ),
    GrammarTopic(
        slug="vergelijken",
        title="Groter dan en even groot als",
        level="A2",
        category="Bijvoeglijke naamwoorden",
        summary="Vergelijk prijzen, eigenschappen en mogelijkheden.",
        explanation="De vergrotende trap krijgt vaak -er: klein/kleiner, duur/duurder. De overtreffende trap krijgt -st: het kleinst, het duurst. Voor een naamwoord staat meestal -e: de goedkoopste fiets. Let op goed/beter/best, veel/meer/meest en graag/liever/liefst.\n\nIn verzorgd geschreven Nederlands gebruik je dan bij ongelijkheid: groter dan. Bij gelijkheid gebruik je even ... als of net zo ... als. Groter als komt in spreektaal en regionale variëteiten voor; presenteer het niet als betekenisloos, maar leer het geschreven standaardpatroon.",
        rules=[
            "Duurder dan; even duur als.",
            "Ik fiets liever dan dat ik autorijd; ik ga het liefst met de trein.",
            "Vergelijk dezelfde eigenschap en dezelfde eenheid.",
        ],
        examples=[
            GrammarExample("Deze jas is goedkoper dan die jas."),
            GrammarExample("De trein is even snel als de bus."),
            GrammarExample("Dit is de beste oplossing."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Deze fiets is goedder.",
                "Deze fiets is beter.",
                "Goed heeft de onregelmatige vergrotende trap beter.",
            )
        ],
        related=["bijvoeglijke-naamwoorden"],
    ),
    GrammarTopic(
        slug="te-infinitief",
        title="Te en om te",
        level="A2",
        category="Werkwoorden",
        summary="Druk een doel uit en gebruik proberen en hoeven.",
        explanation="Na sommige werkwoorden staat te: Ik probeer op tijd te komen. Om ... te geeft vaak een doel: Ik ga naar de winkel om brood te kopen. Bij een scheidbaar werkwoord komt te tussen de delen: om vroeg op te staan.\n\nHoeven komt meestal voor bij ontkenning of beperking: Je hoeft niet te komen; Je hoeft alleen te tekenen. Niet hoeven betekent geen noodzaak, niet mogen betekent geen toestemming. Na kunnen, willen, moeten en mogen staat in deze basisconstructies geen te: Ik wil komen.",
        rules=[
            "Proberen te; hoeven niet te; willen zonder te.",
            "Om te beschrijft een doel.",
            "Het verzwegen onderwerp van de doelzin moet duidelijk zijn.",
        ],
        examples=[
            GrammarExample("Ik bel om een afspraak te maken."),
            GrammarExample("Je hoeft niet te betalen."),
            GrammarExample("Ze probeert vroeg op te staan."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik probeer vroeg te opstaan.",
                "Ik probeer vroeg op te staan.",
                "Te komt tussen de delen van een scheidbaar werkwoord.",
            )
        ],
        related=["modale-werkwoorden", "scheidbare-werkwoorden"],
    ),
    GrammarTopic(
        slug="gebiedende-wijs",
        title="Instructies en beleefde verzoeken",
        level="A2",
        category="Interactie",
        summary="Geef begrijpelijke aanwijzingen zonder onnodig direct te zijn.",
        explanation="Een gewone gebiedende wijs gebruikt de stam zonder onderwerp: Kom binnen; Neem plaats; Bel morgen terug. Met zijn gebruik je wees: Wees voorzichtig. Voeg bij een scheidbaar werkwoord het eerste deel achteraan toe: Vul dit formulier in.\n\nEen instructie kan vriendelijker worden door alstublieft, even of een vraagvorm, maar toon en relatie blijven belangrijk. Kunt u mij helpen? en Zou u mij kunnen helpen? zijn verzoeken. Bij gevaar mag een korte instructie direct zijn: Stop! Gebruik geen vaste regel dat een gebiedende wijs altijd onbeleefd is.",
        rules=[
            "Gebruik de stam: wacht, loop, neem.",
            "Zijn heeft wees als gewone gebiedende wijs.",
            "Stem directheid af op situatie en relatie.",
        ],
        examples=[
            GrammarExample("Sla bij het plein linksaf."),
            GrammarExample("Vul uw naam hier in, alstublieft."),
            GrammarExample("Kun je even wachten?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Zijn voorzichtig!",
                "Wees voorzichtig!",
                "De gebiedende wijs van zijn is hier wees.",
            )
        ],
        related=["scheidbare-werkwoorden", "toekomst-plannen"],
    ),
    GrammarTopic(
        slug="toekomst-plannen",
        title="Morgen, gaan en zullen",
        level="A2",
        category="Tijd",
        summary="Maak plannen, afspraken en voorstellen.",
        explanation="Een tegenwoordige tijd met een tijdsbepaling kan naar de toekomst verwijzen: Morgen werk ik thuis. Gaan + infinitief drukt vaak een voornemen of ontwikkeling uit: Ik ga Nederlands leren. Zullen kan een voorspelling, belofte of voorstel geven: Het zal druk worden; Zal ik helpen?\n\nNiet elke toekomstige zin heeft zullen nodig. Kies de vorm die bij je bedoeling past. Met zou kun je een wens of beleefd verzoek formuleren: Ik zou graag een afspraak maken. Dat is niet automatisch verleden tijd in betekenis.",
        rules=[
            "Gebruik een tijdsbepaling om een afspraak duidelijk te maken.",
            "Gaan + infinitief zonder te.",
            "Zal ik ...? en Zullen we ...? zijn voorstellen.",
        ],
        examples=[
            GrammarExample("Volgende week begin ik."),
            GrammarExample("Zullen we om tien uur afspreken?"),
            GrammarExample("Ik zou graag een kamer reserveren."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik ga te werken.", "Ik ga werken.", "Gaan krijgt hier een infinitief zonder te."
            )
        ],
        related=["modale-werkwoorden", "tijd-getallen"],
    ),
    GrammarTopic(
        slug="wederkerende-werkwoorden",
        title="Me, je en zich",
        level="A2",
        category="Voornaamwoorden",
        summary="Beschrijf verzorging, gevoelens en dagelijkse handelingen.",
        explanation="Bij een wederkerend werkwoord verwijst het voornaamwoord terug naar het onderwerp: ik vergis me, jij vergist je, hij vergist zich, wij vergissen ons, jullie vergissen je, zij vergissen zich. Bij u zijn zowel u als zich mogelijk: U vergist u/zich.\n\nSommige werkwoorden zijn verplicht wederkerend in een bepaalde betekenis, zoals zich vergissen. Andere kunnen ook een ander object krijgen: Ik was me; Ik was de baby. Zelf geeft nadruk of contrast: Ik was mezelf. Gebruik zichzelf niet automatisch waar het gewone zich voldoende is.",
        rules=[
            "Ik/me; wij/ons; hij en zij/zich.",
            "Leer het voornaamwoord met het werkwoord.",
            "Zichzelf voegt vaak nadruk toe.",
        ],
        examples=[
            GrammarExample("Ik voel me beter."),
            GrammarExample("We melden ons aan."),
            GrammarExample("Zij vergist zich in de datum."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ik vergis zich.", "Ik vergis me.", "Het wederkerend voornaamwoord hoort bij ik."
            )
        ],
        related=["objectvormen", "scheidbare-werkwoorden"],
    ),
    GrammarTopic(
        slug="betrekkelijk-die-dat",
        title="De persoon die en het boek dat",
        level="A2",
        category="Zinsbouw",
        summary="Geef extra informatie bij een persoon of een ding.",
        explanation="Een betrekkelijke bijzin beschrijft een naamwoord. Gebruik die bij een enkelvoudig de-woord of een meervoud: de buurman die, de boeken die. Gebruik dat bij een enkelvoudig het-woord: het boek dat. Het werkwoord staat in de bijzin achteraan: het boek dat ik lees.\n\nDe verwijzing hangt af van het naamwoord, niet van het geslacht van een persoon. Daarom: het meisje dat hier woont. Begin met korte zinnen waarin het duidelijk is wie iets doet: de vrouw die ik bel tegenover de vrouw die mij belt.",
        rules=[
            "De en meervoud → die; enkelvoudig het → dat.",
            "Een betrekkelijke bijzin heeft bijzinvolgorde.",
            "Controleer wie onderwerp is binnen de bijzin.",
        ],
        examples=[
            GrammarExample("Dat is de fiets die ik wil kopen."),
            GrammarExample("Het huis dat we huren is klein."),
            GrammarExample("De mensen die hier werken zijn vriendelijk."),
        ],
        common_mistakes=[
            GrammarMistake(
                "het boek die ik lees", "het boek dat ik lees", "Boek is een enkelvoudig het-woord."
            )
        ],
        related=["lidwoorden-meervoud", "omdat-dat"],
    ),
    GrammarTopic(
        slug="verkleinwoorden-er-aantal",
        title="Een kopje en er twee",
        level="A2",
        category="Naamwoorden",
        summary="Gebruik verkleinwoorden en verwijs terug naar een hoeveelheid.",
        explanation="Verkleinwoorden kunnen kleinheid, vriendelijkheid of een gebruikelijke benaming uitdrukken: huisje, kopje, broodje. Leer de uitgangen met voorbeelden: tafel/tafeltje, boom/boompje, ring/ringetje. Een verkleinwoord is in het enkelvoud een het-woord; het meervoud eindigt meestal op -s.\n\nBij een getal zonder herhaald naamwoord gebruik je vaak er: Hoeveel broodjes wil je? Ik wil er twee. Het verwijst naar de eerder genoemde soort. Maak onderscheid tussen aantal en plaats: Ik heb er twee gaat over hoeveelheid; Ik woon er over plaats.",
        rules=[
            "Het kopje, de kopjes.",
            "Leer de spelling van verkleinwoorden per patroon.",
            "Gebruik er bij een terugverwijzend aantal: er drie, er veel.",
        ],
        examples=[
            GrammarExample("Mag ik een kopje thee?"),
            GrammarExample("Ik koop drie broodjes en eet er twee."),
            GrammarExample("We zitten aan een klein tafeltje."),
        ],
        common_mistakes=[
            GrammarMistake("de huisje", "het huisje", "Een enkelvoudig verkleinwoord krijgt het.")
        ],
        related=["er-plaats", "lidwoorden-meervoud"],
    ),
]
