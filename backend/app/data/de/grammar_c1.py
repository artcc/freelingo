"""German grammar topics — C1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="modalverben-subjektiv",
        title="Subjektive Modalverben",
        level="C1",
        category="Verben",
        summary="Subjektive Modalverben auf fortgeschrittenem Niveau – Hörensagen, Wahrscheinlichkeit und epistemische Modalität.",
        explanation="""Auf C1-Niveau werden subjektive Modalverben in ihrer ganzen Tiefe behandelt. Gewissheitsgrade: müssen ≈95%, dürfte ≈75%, können ≈50%, mögen ≈30%. sollen zitiert Quellen neutral, wollen mit Skepsis.
Vergangenheit: Er muss krank gewesen sein. Sie will ihn gesehen haben.
sollen: unpersönliches Gerücht (Der Politiker soll zurücktreten). wollen: Behauptung des Subjekts selbst, oft zweifelhaft (Er will nichts gewusst haben).""",
        structure="Modalverb (subjektiv) + Infinitiv (Gegenwart) / Partizip II + haben/sein (Vergangenheit)",
        rules=[
            "Subjektive Modalverben drücken unterschiedliche Gewissheitsgrade aus.",
            "Müssen subjektiv = höchster Gewissheitsgrad.",
            "Dürfte = moderate Wahrscheinlichkeit.",
            "Sollen zitiert fremde Quelle neutral, wollen mit Skepsis.",
            "Vergangenheit: Modalverb + Partizip II + haben/sein.",
        ],
        examples=[
            GrammarExample(
                text="Der Chef muss Bescheid wissen.",
                translation=None,
                note="sichere Vermutung",
            ),
            GrammarExample(
                text="Der Angeklagte soll das Geld gestohlen haben.",
                translation=None,
                note="Gerücht",
            ),
            GrammarExample(
                text="Sie will bereits dreimal in Japan gewesen sein.",
                translation=None,
                note="zweifelhafte Behauptung",
            ),
            GrammarExample(
                text="Das dürfte die Lösung unseres Problems sein.",
                translation=None,
                note="vorsichtige Vermutung",
            ),
            GrammarExample(
                text="Das mag ja alles stimmen, aber was hilft uns das?",
                translation=None,
                note="einräumend",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Er will krank sein. = Er soll krank sein. (gleichgesetzt)",
                correct="wollen = Behauptung des Subjekts, sollen = Behauptung Dritter",
                note="Subjektive Modalverben haben unterschiedliche Quellenbezüge.",
            ),
        ],
        related=[
            "subjektive-modalverben",
            "konjunktiv-i",
            "indirekte-rede",
            "modalverben",
        ],
    ),
    GrammarTopic(
        slug="gehobene-sprache",
        title="Gehobene Sprache",
        level="C1",
        category="Stil",
        summary="Gehobenes Register – Konjunktiv I in formellen Texten, Nominalstil, anspruchsvolle Syntax.",
        explanation="""Die gehobene Sprache zeichnet sich aus durch: Konjunktiv I für indirekte Rede, Nominalstil und Funktionsverbgefüge, Genitiv-Präpositionen (bezüglich, hinsichtlich, angesichts), unpersönliche Konstruktionen (Es ist davon auszugehen, dass...), komplexe Hypotaxe.
Registerwechsel (Code-Switching): Im Freundeskreis: Hast du Bock auf Kino? Im Büro: Hätten Sie Interesse an einem Kinobesuch? In einer Rede: Es wäre mir eine Freude, Sie einladen zu dürfen.""",
        structure="Konjunktiv I · Nominalstil · Genitiv-Präpositionen · unpersönliche Passiv-Konstruktionen · komplexe Hypotaxe",
        rules=[
            "Gehobenes Register verwendet Konjunktiv I für indirekte Rede.",
            "Nominalstil und Funktionsverbgefüge sind typisch für formelle Texte.",
            "Genitiv-Präpositionen ersetzen einfachere Dativ-Konstruktionen.",
            "Unpersönliche Konstruktionen erhöhen Formalität.",
            "Die Wahl des Registers hängt von Situation, Medium und Beziehung ab.",
        ],
        examples=[
            GrammarExample(
                text="Es ist darauf hinzuweisen, dass die Frist morgen endet.",
                translation=None,
            ),
            GrammarExample(
                text="Bezüglich Ihrer Anfrage teilen wir Ihnen mit, dass...",
                translation=None,
                note="Genitiv + formell",
            ),
            GrammarExample(
                text="Der Minister äußerte, er sei zuversichtlich.",
                translation=None,
                note="Konjunktiv I",
            ),
            GrammarExample(
                text="Angesichts der Umstände bleibt uns keine andere Wahl.",
                translation=None,
                note="Genitiv-Präposition",
            ),
            GrammarExample(
                text="Es gilt, die richtigen Schlüsse zu ziehen.",
                translation=None,
                note="unpersönlich",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gemischte Register: Bezüglich deiner Anfrage sag ich mal so: Nee.",
                correct="Konsistent formell ODER informell schreiben.",
                note="Einheitliches Register durchhalten.",
            ),
        ],
        related=[
            "konjunktiv-i",
            "indirekte-rede",
            "nominalstil",
            "funktionsverbgefuege",
            "textkonnektoren",
        ],
    ),
    GrammarTopic(
        slug="nominalstil",
        title="Nominalstil",
        level="C1",
        category="Stil",
        summary="Nominalstil – komplexe Nominalphrasen und Funktionsverbgefüge.",
        explanation="""Der Nominalstil verdichtet Informationen in komplexen Nominalphrasen. Von verbal zu nominal: Weil die Preise steigen → Aufgrund der steigenden Preise. Nachdem das Gesetz verabschiedet wurde → Nach der Verabschiedung des Gesetzes.
Bausteine: Nominalisierung (steigen → der Anstieg), Komposita (Preisanstieg), Funktionsverbgefüge (zur Durchführung bringen), präpositionale Genitivkonstruktionen (unter Berücksichtigung), Partizipialattribute (das zu lösende Problem).
Vorteil: Informationsdichte. Nachteil: Schwerfälligkeit bei Übergebrauch.""",
        structure="Verb/Adjektiv → Nomen · Satz → Nominalphrase · Funktionsverbgefüge · Genitivkette · Partizipialattribut",
        rules=[
            "Verben und Adjektive werden durch Suffixe zu Nomen.",
            "Zeitliche/kausale Zusammenhänge durch Präpositionen ausgedrückt.",
            "Funktionsverbgefüge ersetzen einfache Verben.",
            "Lange Genitivketten sind typisch (aber schwer verständlich).",
        ],
        examples=[
            GrammarExample(
                text="Die zunehmende Digitalisierung der Arbeitswelt",
                translation=None,
            ),
            GrammarExample(
                text="trotz der schwierigen wirtschaftlichen Rahmenbedingungen",
                translation=None,
            ),
            GrammarExample(
                text="nach Abschluss der seit Monaten andauernden Verhandlungen",
                translation=None,
            ),
            GrammarExample(
                text="Die Durchführung des Projekts erfolgte planmäßig.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Übermäßige Nominalisierung (Substantivitis).",
                correct="Stilistisch ausgewogene Mischung: Kernaussagen nominal, Beispiele verbal.",
                note="Zu viel Nominalstil macht Texte unlesbar.",
            ),
        ],
        related=[
            "nominalisierung",
            "verbalisierung",
            "funktionsverbgefuege",
            "genitiv",
            "wissenschaftssprache",
        ],
    ),
    GrammarTopic(
        slug="funktionsverbgefuege",
        title="Funktionsverbgefüge",
        level="C1",
        category="Stil",
        summary="Funktionsverbgefüge – erweiterte Liste mit stilistischen Feinheiten.",
        explanation="""Funktionsverbgefüge (FVGs): feste Verbindungen aus Nomen + bedeutungsarmem Verb.
Mit bringen: zur Anwendung bringen (anwenden), zur Sprache bringen (ansprechen), zum Ausdruck bringen (ausdrücken), in Erfahrung bringen (erfahren), in Gefahr bringen (gefährden).
Mit ziehen: in Betracht ziehen (betrachten), in Erwägung ziehen (erwägen), in Zweifel ziehen (bezweifeln), zur Rechenschaft ziehen (belangen).
Mit stehen: zur Verfügung stehen (verfügbar sein), zur Debatte stehen (diskutiert werden), außer Frage stehen (sicher sein).
Mit treffen: eine Entscheidung treffen (entscheiden), eine Vereinbarung treffen (vereinbaren), Maßnahmen treffen (handeln).
FVGs machen Sprache formeller, präziser und distanzierter.""",
        structure="Nomen + Funktionsverb (bringen, ziehen, stehen, treffen, nehmen...) = formellere Variante eines einfachen Verbs",
        rules=[
            "FVGs bestehen aus bedeutungsarmem Verb + bedeutungstragendem Nomen.",
            "Das Nomen kann oft durch ein einfaches Verb ersetzt werden.",
            "FVGs erhöhen Formalität.",
            "Die Wahl des Funktionsverbs ist idiomatisch festgelegt.",
        ],
        examples=[
            GrammarExample(
                text="Wir müssen diese Möglichkeit in Betracht ziehen.",
                translation=None,
            ),
            GrammarExample(
                text="Das neue Verfahren wurde zur Anwendung gebracht.",
                translation=None,
            ),
            GrammarExample(
                text="Diese Behauptung muss ich in Zweifel ziehen.",
                translation=None,
            ),
            GrammarExample(
                text="Stehen Ihnen die Unterlagen zur Verfügung?",
                translation=None,
            ),
            GrammarExample(
                text="Das Komitee traf eine einstimmige Entscheidung.",
                translation=None,
            ),
            GrammarExample(
                text="Er wurde für den Schaden zur Rechenschaft gezogen.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="in Betracht nehmen / zur Verfügung bringen",
                correct="in Betracht ziehen / zur Verfügung stellen",
                note="Die Verben in FVGs sind fest und dürfen nicht ausgetauscht werden.",
            ),
        ],
        related=[
            "nomen-verb-verbindungen",
            "nominalisierung",
            "nominalstil",
            "wissenschaftssprache",
        ],
    ),
    GrammarTopic(
        slug="wortbildung",
        title="Wortbildung",
        level="C1",
        category="Wortbildung",
        summary="Wortbildung – Präfixe, Suffixe und Komposita als System.",
        explanation="""Die deutsche Wortbildung umfasst: Komposition (Haustürschlüssel = Haus+Tür+Schlüssel — Grundwort rechts bestimmt Genus), Derivation (Präfixe: be-, er-, ver-, zer-, ent-, miss-; Suffixe: -ung, -heit, -keit, -bar, -lich, -los), Konversion (laufen → das Laufen, blau → das Blau), Kurzwortbildung (LKW, Uni, Kripo).
Fugenelemente: -s-, -en-, -es- zwischen Kompositionsteilen: Arbeit**s**platz, Hunde**h**ütte.""",
        structure="Komposition: Bestimmungswort + (Fuge) + Grundwort / Derivation: Präfix + Stamm + Suffix / Konversion: Wortartwechsel ohne Formänderung",
        rules=[
            "In Komposita bestimmt das letzte Element Genus und Kernbedeutung.",
            "Fugenelemente können zwischen Teilen eines Kompositums stehen.",
            "Präfixe verändern die Bedeutung des Basisworts.",
            "Suffixe bestimmen die Wortart: -ung → Nomen, -bar → Adjektiv, -ieren → Verb.",
        ],
        examples=[
            GrammarExample(
                text="die Haustür = das Haus + die Tür",
                translation=None,
                note="Komposition",
            ),
            GrammarExample(
                text="die Kindheit = das Kind + -heit",
                translation=None,
                note="Derivation",
            ),
            GrammarExample(
                text="das Essen (vom Verb essen)",
                translation=None,
                note="Konversion",
            ),
            GrammarExample(text="unmöglich = un- + möglich", translation=None, note="Präfix"),
            GrammarExample(
                text="das Autobahnkreuz = Auto + Bahn + Kreuz",
                translation=None,
                note="dreiteilig",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Der Wortbildung (falsches Genus)",
                correct="Die Wortbildung",
                note="Das Grundwort bestimmt das Genus.",
            ),
        ],
        related=["praefixe", "nominalisierung", "genus"],
    ),
    GrammarTopic(
        slug="praefixe",
        title="Verbpräfixe und ihre Bedeutungen",
        level="C1",
        category="Wortbildung",
        summary="Verbpräfixe – be-, er-, ver-, zer-, ent-, miss- und ihre systematischen Bedeutungen.",
        explanation="""Untrennbare Verbpräfixe mit systematischen Bedeutungen:
be-: macht transitiv, zielgerichtet (antworten → beantworten, treten → betreten)
er-: Resultat, Erkennung, Beginn (kennen → erkennen, öffnen → eröffnen)
ver-: falsch machen (verlaufen), verbrauchen (verbrennen), verschwinden (vergehen), weggeben (verkaufen)
zer-: Zerstörung (brechen → zerbrechen, stören → zerstören)
ent-: Entfernung, Gegenteil, Beginn (kommen → entkommen, decken → entdecken)
miss-: falsch, schlecht (verstehen → missverstehen, trauen → misstrauen)""",
        structure="Präfix + Basisverb = neues Verb mit modifizierter Bedeutung",
        rules=[
            '"Be-" macht intransitive Verben transitiv.',
            '"Er-" drückt Resultat oder Beginn aus.',
            '"Ver-" ist vielseitig: falsch machen, verbrauchen, verschwinden.',
            '"Zer-" bedeutet Zerstörung.',
            '"Ent-" bedeutet Entfernung oder Gegenteil.',
            '"Miss-" drückt Negatives oder Falsches aus.',
        ],
        examples=[
            GrammarExample(
                text="Er beantwortete die Frage.",
                translation=None,
                note="be-: transitiv",
            ),
            GrammarExample(
                text="Ich habe mich im Wald verlaufen.",
                translation=None,
                note="ver-: falsch laufen",
            ),
            GrammarExample(
                text="Das Glas zerbrach in tausend Stücke.",
                translation=None,
                note="zer-: Zerstörung",
            ),
            GrammarExample(
                text="Kolumbus entdeckte Amerika.",
                translation=None,
                note="ent-: die Decke wegnehmen",
            ),
            GrammarExample(
                text="Du hast mich missverstanden.",
                translation=None,
                note="miss-: falsch verstehen",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich antworte die Frage.",
                correct="Ich beantworte die Frage.",
                note='Intransitives "antworten auf" → transitives "beantworten".',
            ),
        ],
        related=["wortbildung", "trennbare-verben", "partizip-ii"],
    ),
    GrammarTopic(
        slug="ironie",
        title="Ironie im Deutschen",
        level="C1",
        category="Stil",
        summary="Ironie im Deutschen – sprachliche Marker, rhetorische Mittel und kulturelle Konventionen.",
        explanation="""Ironie als Stilmittel: Modalpartikeln (Das hast du ja toll gemacht!), Übertreibung (Das hat nur drei Stunden gedauert!), Untertreibung/Litotes (Das war nicht schlecht = sehr gut), Konjunktiv II (Das könnte ja vielleicht etwas schneller gehen!).
Berliner Schnauze (direkt, sarkastisch), Wiener Schmäh (charmant-subtil), Rheinischer Humor (lebensbejahend).
Gefahr: Ironie kann von Nicht-Muttersprachlern leicht missverstanden werden. Besonders in formellen Kontexten ist Vorsicht geboten.""",
        structure="Ironische Signale: Modalpartikeln + Übertreibung/Untertreibung + Konjunktiv II + spezifische Intonation",
        rules=[
            "Modalpartikeln (ja, wohl, vielleicht) können Ironie markieren.",
            'Untertreibung ("nicht schlecht" = sehr gut) ist ein typisch deutsches Ironiesignal.',
            "Konjunktiv II in Aufforderungen kann ironisch-passiv-aggressiv sein.",
            "Schriftliche Ironie ohne Kontext wird oft missverstanden.",
        ],
        examples=[
            GrammarExample(
                text="Das hast du ja mal wieder super hingekriegt!",
                translation=None,
                note="ja + Übertreibung",
            ),
            GrammarExample(
                text="Der Vortrag war nicht ganz langweilig.",
                translation=None,
                note="Litotes",
            ),
            GrammarExample(
                text="Du könntest vielleicht beim nächsten Mal etwas pünktlicher sein.",
                translation=None,
            ),
            GrammarExample(
                text="Ach, wirklich? Das hätte ich ja nie gedacht!",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ironie in formellen E-Mails ohne Emojis.",
                correct="In formellen Kontexten Ironie vermeiden.",
                note="Schriftliche Ironie ohne nonverbale Signale ist riskant.",
            ),
        ],
        related=["konnotationen", "rhetorische-mittel", "konjunktiv-ii-hoeflichkeit"],
    ),
    GrammarTopic(
        slug="konnotationen",
        title="Konnotationen und Nuancen",
        level="C1",
        category="Wortschatz",
        summary="Konnotationen und Nuancen – feine Unterschiede zwischen bedeutungsähnlichen Wörtern verstehen.",
        explanation="""Konnotationen sind emotionale Nebenbedeutungen: dünn (negativ) vs schlank (positiv), billig (schlechte Qualität) vs preiswert (gutes Preis-Leistungs-Verhältnis), Gesicht (neutral) vs Antlitz (poetisch) vs Visage (abwertend).
Register-Ebenen: vulgär (kotzen) → umgangssprachlich (sich übergeben) → standard (erbrechen) → gehoben (sich übergeben) → fachsprachlich (vomieren).
C1-Sprecher wählen Wörter nach Konnotation und Register — und erkennen die stilistische Wirkung von Wortwahl bei anderen.""",
        structure="Synonym erkennen + Konnotation (positiv/negativ/neutral) + Register (vulgär-gehoben-fachsprachlich) bestimmen",
        rules=[
            "Fast jedes Wort hat neben der Grundbedeutung emotionale Assoziationen.",
            "Synonyme unterscheiden sich meist in Konnotation oder Register.",
            "Register reichen von vulgär bis fachsprachlich.",
            "Die Kenntnis von Konnotationen ist entscheidend für idiomatisches Deutsch.",
        ],
        examples=[
            GrammarExample(
                text="Sie hat eine schlanke Figur.",
                translation=None,
                note="positiv",
            ),
            GrammarExample(
                text="Das ist ein sehr preiswertes Hotel.",
                translation=None,
                note="positiv",
            ),
            GrammarExample(
                text="Er äußerte Bedenken gegen den Plan.",
                translation=None,
                note="formell, neutral",
            ),
            GrammarExample(
                text="Sie behauptete, ihn zu kennen.",
                translation=None,
                note="behaupten = Zweifel impliziert",
            ),
            GrammarExample(
                text="Diese Ansicht ist obsolet.",
                translation=None,
                note="fachsprachlich",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Meine Chefin ist ein dünnes Weib.",
                correct="Meine Chefin ist eine schlanke Frau.",
                note="Dünn und Weib können abwertend klingen.",
            ),
        ],
        related=["gehobene-sprache", "ironie", "rhetorische-mittel"],
    ),
    GrammarTopic(
        slug="rhetorische-mittel",
        title="Rhetorische Mittel",
        level="C1",
        category="Stil",
        summary="Rhetorische Mittel – Metapher, Alliteration, rhetorische Frage, Chiasmus.",
        explanation="""Wichtige Stilfiguren:
Wiederholung: Anapher (gleicher Satzanfang), Alliteration (Milch macht müde Männer munter)
Gegensatz: Antithese (Der Worte sind genug gewechselt...), Chiasmus (Die Kunst ist lang, und kurz ist das Leben), Oxymoron (beredtes Schweigen)
Bildlichkeit: Metapher (Sturm der Gefühle), Personifikation (Die Sonne lacht), Vergleich (stark wie ein Bär)
Hervorhebung: Rhetorische Frage (Wer will schon ewig leben?), Hyperbel (tausendmal gesagt), Litotes (nicht schlecht = sehr gut)""",
        structure="Stilfiguren: Wiederholung · Gegensatz · Bildlichkeit · Hervorhebung",
        rules=[
            "Rhetorische Mittel steigern die Wirkung von Texten.",
            "Stilfiguren müssen zur Textsorte passen.",
            "Häufung von Stilfiguren kann manieriert wirken.",
            "Rhetorische Fragen und Litotes sind im Alltagsdeutsch besonders häufig.",
        ],
        examples=[
            GrammarExample(
                text="Das ist der Anfang vom Ende.",
                translation=None,
                note="Paradoxon",
            ),
            GrammarExample(
                text="Reden ist Silber, Schweigen ist Gold.",
                translation=None,
                note="Antithese",
            ),
            GrammarExample(
                text="Wer ist schon perfekt?",
                translation=None,
                note="rhetorische Frage",
            ),
            GrammarExample(
                text="Das habe ich dir schon hundertmal gesagt!",
                translation=None,
                note="Hyperbel",
            ),
            GrammarExample(text="Der Himmel weinte.", translation=None, note="Personifikation"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Stilmittel um ihrer selbst willen einsetzen.",
                correct="Jedes Stilmittel sollte eine bewusste Funktion haben.",
                note="Ornament ohne Funktion wirkt hohl.",
            ),
        ],
        related=["ironie", "konnotationen", "textanalyse", "gehobene-sprache"],
    ),
    GrammarTopic(
        slug="argumentation",
        title="Argumentationsstruktur",
        level="C1",
        category="Stil",
        summary="Argumentationsstruktur – logische Argumente mit Konnektoren, These-Antithese-Synthese.",
        explanation="""Klassischer Dreischritt: These → Antithese → Synthese. Aufbau eines Arguments: Behauptung → Begründung (weil, denn, da) → Beispiel (zum Beispiel, etwa) → Folgerung (deshalb, daher, also).
Sprachliche Mittel: hinzufügen (außerdem, darüber hinaus), gewichten (vor allem, insbesondere), einschränken (allerdings, jedoch, dennoch), schlussfolgern (daher, folglich, somit).
Typische Phrasen: Es stellt sich die Frage, ob... / Man muss jedoch bedenken, dass... / Zusammenfassend lässt sich sagen...""",
        structure="These → Begründung → Beispiel → Folgerung",
        rules=[
            "Jedes Argument braucht Begründung und wenn möglich ein Beispiel.",
            "Konnektoren wie daher, deshalb, folglich strukturieren den Gedankengang.",
            "Eine gute Argumentation berücksichtigt auch Gegenargumente.",
            "Die deutsche Argumentationskultur ist direkt und sachorientiert.",
        ],
        examples=[
            GrammarExample(
                text="Einerseits bietet die Digitalisierung viele Chancen. Andererseits birgt sie Risiken.",
                translation=None,
            ),
            GrammarExample(
                text="Es stimmt zwar, dass die Mieten steigen. Allerdings muss man auch die Einkommensentwicklung berücksichtigen.",
                translation=None,
            ),
            GrammarExample(
                text="Daraus folgt, dass wir unser Verhalten ändern müssen.",
                translation=None,
            ),
            GrammarExample(
                text="Zusammenfassend lässt sich feststellen, dass beide Ansätze ihre Berechtigung haben.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Behauptung ohne Begründung.",
                correct="Immer Begründung liefern: weil oder denn.",
                note="Im Deutschen wird Unbegründetes schnell als unüberzeugend abgetan.",
            ),
        ],
        related=[
            "textkonnektoren",
            "zweiteilige-konnektoren",
            "synthese",
            "wissenschaftssprache",
        ],
    ),
    GrammarTopic(
        slug="oesterreich-schweiz",
        title="Varietäten: Österreich, Schweiz",
        level="C1",
        category="Varietäten",
        summary="Österreichisches und Schweizer Standarddeutsch – wichtiger Wortschatz, grammatische Unterschiede.",
        explanation="""Plurizentrische Sprache mit drei Standardvarietäten.
Österreich: Jänner (Januar), Paradeiser (Tomaten), Topfen (Quark), Semmel (Brötchen), Sackerl (Tüte), Bankomat (Geldautomat). Grammatik: Perfekt statt Präteritum auch schriftlich. Ich bin gesessen (statt habe gesessen). Diminutiv -erl/-el.
Schweiz: Velo (Fahrrad), Trottoir (Bürgersteig), Natel (Handy), Rahm (Sahne). Orthographie: Kein ß, immer ss (Strasse, gross). Relativsätze mit welcher/welche/welches sind häufiger.""",
        structure="Deutschland-Österreich-Schweiz: Wortschatz, Grammatik, Orthographie",
        rules=[
            "Alle drei Varietäten sind standardsprachlich korrekt.",
            "Austriazismen/Helvetismen sind im jeweiligen Land Standard.",
            "In der Schweiz wird generell kein ß geschrieben.",
            "Österreich bevorzugt Perfekt auch in schriftlichen Texten.",
        ],
        examples=[
            GrammarExample(
                text="Ich kaufe eine Semmel und ein Sackerl.",
                translation=None,
                note="Österreich",
            ),
            GrammarExample(
                text="Er fährt mit dem Velo auf dem Trottoir.",
                translation=None,
                note="Schweiz",
            ),
            GrammarExample(
                text="Das ist eine grosse Strasse.",
                translation=None,
                note="Schweizer Orthographie: kein ß",
            ),
            GrammarExample(
                text="Ich bin am Sofa gesessen.",
                translation=None,
                note="Österreich: sein + gesessen",
            ),
            GrammarExample(
                text="Das ist der Mann, welcher das gesagt hat.",
                translation=None,
                note="Schweiz: welcher als Relativpronomen",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Schweizer schreiben falsch, weil sie kein ß verwenden.",
                correct="Schweizer Standarddeutsch verwendet kein ß — das ist korrekt.",
                note="Das Fehlen des ß ist ein orthographisches Merkmal, kein Fehler.",
            ),
        ],
        related=["regionale-unterschiede", "gehobene-sprache", "konnotationen"],
    ),
    GrammarTopic(
        slug="regionale-unterschiede",
        title="Regionale Unterschiede im Deutschen",
        level="C1",
        category="Varietäten",
        summary="Regionale Unterschiede – lexikalische Nord-Süd-Teilungen und dialektaler Einfluss.",
        explanation="""Nord-Süd-Gefälle: Brötchen (Nord) / Semmel (Süd), Sonnabend / Samstag, Sahne / Rahm, Junge / Bub, Hallo / Grüß Gott.
Grammatik: Norden mehr Präteritum, Süden fast ausschließlich Perfekt (oberdeutscher Präteritumschwund). Süden: Genitiv bleibt länger erhalten als possessiver Dativ (dem Peter sein Haus).
Phonetik: Norden ich [ɪç], Süden i(ch) [iː]. In Norddeutschland ist Standardsprache näher an der Umgangssprache, im Süden sind Dialekte im Alltag präsenter.""",
        structure="Norddeutsch vs. süddeutsch vs. ost-/westdeutsch: Wortschatz, Grammatik, Aussprache",
        rules=[
            "Regionale Varianten des Standarddeutschen sind korrekt.",
            "Im Süden ist Perfekt die dominante Vergangenheitsform.",
            "Im Norden ist Präteritum in der gesprochenen Sprache häufiger.",
            "Dialekt beeinflusst das Standarddeutsch stärker im Süden.",
        ],
        examples=[
            GrammarExample(
                text="Ich möchte ein Brötchen / eine Semmel.",
                translation=None,
                note="Nord / Süd",
            ),
            GrammarExample(
                text="Grüß Gott! (Süd) / Moin! (Nord) / Tach! (West)",
                translation=None,
                note="regionale Begrüßung",
            ),
            GrammarExample(text="Samstag / Sonnabend", translation=None, note="Süd / Nord"),
            GrammarExample(
                text="ein Viertel vor acht (allg.) / drei Viertel acht (Ost)",
                translation=None,
                note="Uhrzeit regional",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Semmel ist ein Fehler für Brötchen.",
                correct="Semmel ist in Süddeutschland und Österreich korrekt.",
                note="Regionale Varianten sind keine Fehler.",
            ),
        ],
        related=["oesterreich-schweiz", "perfekt-vs-praeteritum", "konnotationen"],
    ),
    GrammarTopic(
        slug="textanalyse",
        title="Textanalyse",
        level="C1",
        category="Stil",
        summary="Textanalyse – systematischer Ansatz zur Analyse deutscher Texte.",
        explanation="""Textanalyse auf C1-Niveau umfasst: Textsorte und Kontext → Inhalt/Thema → Struktur/Aufbau → Sprachliche Analyse (Wortwahl, Satzbau, rhetorische Mittel, grammatische Besonderheiten) → Argumentationsstruktur → Wirkung und Intention.
Typische Formulierungen: Der Autor bedient sich einer bildhaften Sprache... / Der Text ist geprägt von... / Die Argumentation erfolgt auf mehreren Ebenen... / Auffällig ist die Verwendung von...
Wichtig: Analyse ist objektiv, eigene Meinung gehört nicht hinein. Belege aus dem Text (Zitate) sind Pflicht.""",
        structure="Textsorte → Inhalt → Aufbau → Sprache → Argumentation → Wirkung",
        rules=[
            "Immer mit Textsorte und Kontext beginnen.",
            "Inhaltliche und sprachliche Analyse klar trennen.",
            "Belege aus dem Text sind Pflicht.",
            "Die Analyse ist objektiv, keine eigene Meinung.",
        ],
        examples=[
            GrammarExample(
                text="Der Artikel ist im Stil eines Kommentars verfasst.",
                translation=None,
            ),
            GrammarExample(
                text="Der Autor argumentiert auf zwei Ebenen: emotional und sachlich.",
                translation=None,
            ),
            GrammarExample(
                text="Die sprachliche Gestaltung ist durch den Nominalstil geprägt.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Eigene Meinung in die Analyse einfließen lassen.",
                correct="Analyse ist objektiv. Eigene Bewertung gehört in einen Kommentar.",
                note="Textanalyse ≠ Textkritik.",
            ),
        ],
        related=["rhetorische-mittel", "argumentation", "synthese", "reformulierung"],
    ),
    GrammarTopic(
        slug="synthese",
        title="Synthese und Paraphrase",
        level="C1",
        category="Stil",
        summary="Synthese und Paraphrase – Quellen kombinieren und in eigenen Worten wiedergeben.",
        explanation="""Paraphrase: Fremden Text in eigenen Worten wiedergeben. Techniken: Synonyme, Satzbau ändern, Perspektive wechseln.
Synthese: Mehrere Quellen zu neuer, eigenständiger Aussage verarbeiten. Kernaussagen identifizieren, Gemeinsamkeiten/Unterschiede finden, in kohärente Argumentation einbetten.
Formulierungen: Sowohl Müller als auch Schmidt argumentieren... / Im Gegensatz zu X vertritt Y... / Die Studien kommen übereinstimmend zu dem Ergebnis... / Während A den Fokus auf ... legt, betont B...""",
        structure="Paraphrase: Synonym + Umstrukturierung + Perspektivwechsel / Synthese: Quelle A + Quelle B → integrierte Aussage",
        rules=[
            "Paraphrasen müssen den Sinn exakt wiedergeben.",
            "Synthesen integrieren mehrere Quellen in neue Argumentation.",
            "Bei Paraphrasen muss die Quelle angegeben werden.",
            "Aktiv-Passiv-Wechsel und Nominalisierung sind mächtige Paraphrasenwerkzeuge.",
        ],
        examples=[
            GrammarExample(
                text="Laut Müller stellt der Klimawandel die größte Herausforderung dar.",
                translation=None,
                note="Paraphrase",
            ),
            GrammarExample(
                text="Während Autor A die Vorteile betont, hebt Autor B die Kosten hervor.",
                translation=None,
                note="Synthese",
            ),
            GrammarExample(
                text="Die Ergebnisse beider Studien deuten übereinstimmend darauf hin, dass...",
                translation=None,
                note="Synthese",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Paraphrase mit denselben Satzstrukturen.",
                correct="Echte Paraphrasen verändern Wortwahl und Satzbau grundlegend.",
                note="Zu viel vom Original = kein Paraphrase.",
            ),
        ],
        related=["indirekte-rede", "konjunktiv-i", "reformulierung", "textanalyse"],
    ),
    GrammarTopic(
        slug="reformulierung",
        title="Reformulierungstechniken",
        level="C1",
        category="Stil",
        summary="Reformulierungstechniken – umformulieren, erklären, komplexe Ideen vereinfachen.",
        explanation="""Reformulierung ist die Fähigkeit, einen Gedanken auf verschiedene Weise auszudrücken. Techniken: Synonyme, Aktiv↔Passiv, Nominalisierung↔Verbalisierung, Perspektivwechsel (Ich gebe dir → Du bekommst von mir), Konkretisierung vs Abstraktion.
Markierungen: Das heißt, ... / Anders gesagt, ... / Mit anderen Worten: ... / Um es einfacher auszudrücken: ... / Oder andersherum: ...
Eine gute Reformulierung bewahrt die Kernaussage, variiert aber die sprachliche Form.""",
        structure="Reformulierung = Synonym + Grammatik-Transformation + Paraphrase + Perspektivwechsel",
        rules=[
            "Reformulierung bedeutet, das Gleiche anders zu sagen.",
            "Techniken: Synonym, Aktiv/Passiv, Nominal-/Verbalstil, Perspektivwechsel.",
            "Reformulierungsmarker machen die Reformulierung transparent.",
            "Vereinfachung ist wichtig für Kommunikation mit unterschiedlichen Niveaus.",
        ],
        examples=[
            GrammarExample(
                text="Die Inflation steigt rapide an. Das heißt, das Geld verliert schnell an Wert.",
                translation=None,
                note="Vereinfachung",
            ),
            GrammarExample(
                text="Man könnte auch sagen, dass diese Maßnahme kontraproduktiv ist.",
                translation=None,
            ),
            GrammarExample(
                text="Anders formuliert: Wir brauchen eine grundlegende Neuausrichtung.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Reformulierung die Bedeutung verändert.",
                correct="Reformulierung muss den Inhalt exakt bewahren.",
                note="Sonst ist es eine Fehlinterpretation.",
            ),
        ],
        related=["synthese", "nominalisierung", "verbalisierung", "passiv-werden"],
    ),
    GrammarTopic(
        slug="wissenschaftssprache",
        title="Wissenschaftssprache",
        level="C1",
        category="Stil",
        summary="Wissenschaftssprache – Konventionen wissenschaftlichen Schreibens: unpersönlich, hedgend, fachspezifisch.",
        explanation="""Wissenschaftssprache: Passiv (Die Proben wurden untersucht), unpersönliche Konstruktionen (Es ist festzustellen, dass...), Nominalstil (Die Durchführung der Untersuchung), Konjunktiv I (Der Autor stellt fest, dies sei...).
Hedging: Dies dürfte zutreffen. / Die Ergebnisse deuten darauf hin... / Die Daten legen nahe... / Es scheint, dass...
Wissenschaftliche Phrasen: Die vorliegende Arbeit untersucht... / Zusammenfassend lässt sich festhalten... / Diesen Ergebnissen zufolge...
Vermeiden: Ich/Wir (außer in manchen Fachkulturen), Umgangssprache, Übertreibungen ohne Beleg, direkte Aufforderungen.""",
        structure="Passiv + Nominalstil + Konjunktiv I + Hedging + Fachvokabular",
        rules=[
            "Passiv und unpersönliche Konstruktionen sind Standard.",
            "Hedging ist zentral: Daten deuten hin, nicht Daten beweisen.",
            "Konjunktiv I für fremde Positionen.",
            "Ich und subjektive Wertungen werden vermieden.",
        ],
        examples=[
            GrammarExample(
                text="Es konnte gezeigt werden, dass die Hypothese zutrifft.",
                translation=None,
            ),
            GrammarExample(
                text="Die Ergebnisse legen nahe, dass ein Zusammenhang besteht.",
                translation=None,
                note="Hedging",
            ),
            GrammarExample(
                text="Zusammenfassend lässt sich festhalten, dass die These bestätigt wurde.",
                translation=None,
            ),
            GrammarExample(
                text="Dem ist entgegenzuhalten, dass die Stichprobe klein war.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Absolute Behauptungen: Die Ergebnisse beweisen eindeutig...",
                correct="Hedging: Die Ergebnisse weisen darauf hin...",
                note="In der Wissenschaft wird kaum etwas 'bewiesen'.",
            ),
        ],
        related=[
            "nominalstil",
            "passiv-werden",
            "konjunktiv-i",
            "funktionsverbgefuege",
            "indirekte-rede",
        ],
    ),
    GrammarTopic(
        slug="redewendungen",
        title="Fortgeschrittene Redewendungen",
        level="C1",
        category="Wortschatz",
        summary="Fortgeschrittene Redewendungen – idiomatische, bildhafte und kulturspezifische deutsche Ausdrücke.",
        explanation="""Redewendungen auf C1-Niveau: sich ins Zeug legen (to put in effort), Nägel mit Köpfen machen (to do things properly), den Nagel auf den Kopf treffen (to hit the nail on the head), vom Regen in die Traufe kommen (from bad to worse), die Flinte ins Korn werfen (to throw in the towel).
Kommunikation: etwas durch die Blume sagen (indirectly), kein Blatt vor den Mund nehmen (to speak one's mind), mit der Tür ins Haus fallen (to be too blunt).
Emotionen: die Nase voll haben (fed up), auf Wolke sieben schweben (on cloud nine), sich wie gerädert fühlen (completely exhausted).
Redensart vs Sprichwort: Redensart ist satzintegriert, Sprichwort ist vollständiger Satz (Wer zuerst kommt, mahlt zuerst.).""",
        structure="Feste Wendung mit idiomatischer (nicht wörtlicher) Bedeutung",
        rules=[
            "Redewendungen sind idiomatisch.",
            "Viele stammen aus Handwerk oder Landwirtschaft.",
            "Sie machen Sprache lebendig und muttersprachlich.",
            "In formellen Kontexten sparsam einsetzen.",
        ],
        examples=[
            GrammarExample(
                text="Du hast den Nagel auf den Kopf getroffen!",
                translation=None,
            ),
            GrammarExample(
                text="Ich habe die Nase voll von dieser Diskussion.",
                translation=None,
            ),
            GrammarExample(text="Er nimmt kein Blatt vor den Mund.", translation=None),
            GrammarExample(
                text="Wir müssen Nägel mit Köpfen machen.",
                translation=None,
            ),
            GrammarExample(
                text="Nach der Wanderung fühle ich mich wie gerädert.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Du hast den Hammer auf den Nagel getroffen.",
                correct="Du hast den Nagel auf den Kopf getroffen.",
                note="Redewendung ist fest — Wörter können nicht ausgetauscht werden.",
            ),
        ],
        related=["konnotationen", "nomen-verb-verbindungen", "funktionsverbgefuege"],
    ),
    GrammarTopic(
        slug="orthotypographie",
        title="Deutsche Orthotypographie",
        level="C1",
        category="Orthographie",
        summary="Deutsche Orthotypographie – Anführungszeichen, ß/ss-Regeln, Kommaregeln.",
        explanation="""Anführungszeichen: Deutsch „..." (99 unten, 66 oben), Schweiz «...» (Guillemets nach innen). Falsch: Englische "...".
ß vs ss: ß nach langem Vokal/Diphthong (Straße, heißen), ss nach kurzem Vokal (Kuss, Fluss, muss).
Kommaregeln: Immer vor Nebensätzen, vor Infinitivgruppen mit zu, bei Aufzählungen, vor aber/sondern/jedoch/doch.
Kein Apostroph bei Genitiv: Peters Auto (nicht: Peter's Auto). Apostroph nur bei Auslassungen: Wie geht's?""",
        structure='„..." (Doppel) · ß nach langem Vokal/Diphthong, ss nach kurzem · Komma vor Nebensätzen, Infinitivgruppen mit zu, Aufzählungen',
        rules=[
            'Anführungszeichen: „..." (deutsch), «...» (Schweiz).',
            "ß nach langem Vokal, ss nach kurzem.",
            "Kein Apostroph beim Genitiv.",
            "Infinitivgruppen mit zu werden mit Komma abgetrennt.",
        ],
        examples=[
            GrammarExample(
                text='Er sagte: „Ich komme morgen."',
                translation=None,
                note="korrekte Anführungszeichen",
            ),
            GrammarExample(
                text="Die Straße ist lang. — Der Fluss ist kurz.",
                translation=None,
                note="ß vs ss",
            ),
            GrammarExample(
                text="Peters Auto, nicht: Peter's Auto",
                translation=None,
                note="kein Apostroph bei Genitiv",
            ),
            GrammarExample(
                text="Wie geht's dir?",
                translation=None,
                note="Apostroph nur bei Auslassung",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong='Englische Anführungszeichen: "Das ist falsch."',
                correct='„So ist es richtig."',
                note="Deutsche Anführungszeichen: 99 unten, 66 oben.",
            ),
        ],
        related=["wissenschaftssprache", "gehobene-sprache"],
    ),
    GrammarTopic(
        slug="fachsprache",
        title="Fachsprache und Terminologie",
        level="C1",
        category="Wortschatz",
        summary="Fachsprache und Terminologie – fachspezifisches Vokabular, akademischer Jargon und domänenspezifische Ausdrücke verstehen und anwenden.",
        explanation="""Fachsprachen sind Varietäten der Standardsprache, die in bestimmten Fachgebieten verwendet werden. Sie zeichnen sich aus durch: präzise Terminologie (jeder Begriff hat eine festgelegte Definition), Nominalstil, hohe Informationsdichte und oft international verständliche Latinismen/Gräzismen.
Horizontale Gliederung: Fachsprache der Medizin (Diagnose, Anamnese, Prognose), der Jura (Kläger, Revision, Nichtigkeit), der Technik (Drehmoment, Frequenz, Kalibrierung), der Wirtschaft (Liquidität, Bilanz, Abschreibung).
Vertikale Gliederung: Theoriensprache (hoch abstrakt), fachliche Umgangssprache (vereinfacht), Verteilersprache (populärwissenschaftlich).
Wichtig: Die Grenze zwischen Fachwort und Allgemeinwort ist fließend (z.B. Stress, Trauma, Energie).""",
        structure="Fachsprache = spezifische Lexik + spezifische Syntax (Nominalstil, Passiv) + definierte Terminologie",
        rules=[
            "Jede Fachsprache hat einen definierten, präzisen Wortschatz.",
            "Fachsprache ist meist schriftlich und zeichnet sich durch Nominalstil und Passiv aus.",
            "Latinismen und Gräzismen sind in vielen Fachsprachen verbreitet.",
            "Die vertikale Schichtung reicht von hochabstrakt bis populärwissenschaftlich.",
        ],
        examples=[
            GrammarExample(
                text="Die Anamnese ergab keine relevanten Vorerkrankungen.",
                translation=None,
                note="medizinische Fachsprache",
            ),
            GrammarExample(
                text="Der Beklagte legte Revision gegen das Urteil ein.",
                translation=None,
                note="juristische Fachsprache",
            ),
            GrammarExample(
                text="Die Liquiditätskennzahlen weisen auf eine stabile Finanzlage hin.",
                translation=None,
                note="wirtschaftliche Fachsprache",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Fachwörter ungeprüft in Alltagstexten verwenden.",
                correct="Fachsprache nur verwenden, wenn das Gegenüber sie versteht.",
                note="Fachjargon wirkt sonst unverständlich oder angeberisch.",
            ),
        ],
        related=[
            "wissenschaftssprache",
            "nominalstil",
            "konnotationen",
            "gehobene-sprache",
        ],
    ),
    GrammarTopic(
        slug="sprachkritik",
        title="Sprachkritik und Stilistik",
        level="C1",
        category="Stil",
        summary="Sprachkritik und Stilistik – Analyse von politischer Sprache, Framing und medialer Diskurse auf Deutsch.",
        explanation="""Sprachkritik untersucht den Gebrauch von Sprache in öffentlichen Diskursen kritisch. Zentrale Konzepte:
Framing: Durch Wortwahl wird ein Deutungsrahmen gesetzt (Steuererleichterung vs Steuergeschenk, Flüchtlingswelle vs Flüchtlingsstrom). Politische Sprache analysieren: Wer spricht? Mit welcher Wortwahl? Welches Framing wird transportiert? Was wird verschwiegen?
Euphemismen: freisetzen (entlassen), preisgünstig (billig), entschlafen (sterben). Dysphemismen: absichtlich abwertende Ausdrücke.
Sprachkritik fragt: Welches Weltbild vermittelt diese Sprachverwendung? Wer profitiert davon? Welche Alternativen gäbe es?
Wichtige Quellen: Victor Klemperer (LTI – Lingua Tertii Imperii), Uwe Pörksen (Plastikwörter), die Aktion Unwort des Jahres.""",
        structure="Sprachgebrauch → Framing identifizieren → Funktion analysieren → kritisch bewerten",
        rules=[
            "Framing bedeutet, dass Wortwahl Denkrahmen setzt.",
            "Sprachkritik hinterfragt, welche Interessen hinter bestimmten Formulierungen stehen.",
            "Euphemismen verschleiern, Dysphemismen werten ab.",
            "Die Analyse politischer Sprache braucht sprachliches und politisches Wissen.",
        ],
        examples=[
            GrammarExample(
                text='"Steuererleichterung" vs "Steuergeschenk" — zwei Frames für dieselbe Maßnahme.',
                translation=None,
                note="Framing",
            ),
            GrammarExample(
                text='"Personalabbau" vs "Freisetzung von Arbeitskräften" — Euphemismus für Entlassungen.',
                translation=None,
                note="Euphemismus",
            ),
            GrammarExample(
                text='"Klimahysterie" vs "Klimaschutz" — dysphemistisches vs neutrales Framing.',
                translation=None,
                note="Dysphemismus",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Sprachkritik mit Sprachpurismus oder Korrektur gleichsetzen.",
                correct="Sprachkritik analysiert, Sprachpurismus lehnt ab. Sprachkritik bewertet nicht einen Ausdruck als ‚falsch', sondern fragt nach dessen Funktion.",
                note="Sprachkritik ist deskriptiv-analytisch, nicht präskriptiv.",
            ),
        ],
        related=["argumentation", "konnotationen", "rhetorische-mittel", "textanalyse"],
    ),
    GrammarTopic(
        slug="verhandlungssprache",
        title="Verhandlungssprache und Diplomatie",
        level="C1",
        category="Stil",
        summary="Verhandlungssprache und Diplomatie – diplomatische Ausdrücke, Hedging und konsensorientierte Kommunikation auf Deutsch.",
        explanation="""Diplomatische Sprache zielt auf Deeskalation, Gesichtswahrung und Konsensbildung. Typische Strategien:
Hedging (Abschwächung): Es könnte sein, dass... / Unter Umständen... / Es wäre zu überlegen, ob... / Möglicherweise ließe sich...
Unverbindlichkeit: Wir werden dies prüfen. (bedeutet oft: Nein) / Das ist ein interessanter Vorschlag. (bedeutet: Ich bin nicht überzeugt).
Diplomatisches Nein: Ich verstehe Ihren Standpunkt, jedoch... / Das ist eine Überlegung wert, allerdings...
Konsensformeln: Lassen Sie uns gemeinsam überlegen... / Wir sind uns ja einig, dass... / Gibt es einen Mittelweg?
Status-Markierungen: Sehr geehrter Herr Kollege... / Ich darf Sie bitten... / Wären Sie so freundlich...?""",
        structure="Hedging + Unverbindlichkeit + Gesichtswahrung + Konsensformeln",
        rules=[
            "Diplomatische Sprache wahrt das Gesicht aller Beteiligten.",
            "Hedging und Unverbindlichkeit sind zentrale Strategien.",
            "Ein direktes Nein ist in diplomatischen Kontexten selten.",
            "Konsensformeln signalisieren Kooperationsbereitschaft.",
        ],
        examples=[
            GrammarExample(
                text="Wir werden Ihren Vorschlag sorgfältig prüfen.",
                translation=None,
                note="diplomatisch unverbindlich",
            ),
            GrammarExample(
                text="Ihre Position ist nachvollziehbar, allerdings müssen wir die finanziellen Rahmenbedingungen berücksichtigen.",
                translation=None,
                note="diplomatisches Nein",
            ),
            GrammarExample(
                text="Wären Sie bereit, über eine alternative Lösung nachzudenken?",
                translation=None,
                note="Konsensformel",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="In diplomatischen Kontexten direkt Nein sagen: Das ist völlig inakzeptabel.",
                correct="Diplomatisch: Da sehe ich noch erheblichen Gesprächsbedarf.",
                note="Direktheit kann als unhöflich oder konfrontativ wahrgenommen werden.",
            ),
        ],
        related=[
            "gehobene-sprache",
            "konjunktiv-ii-hoeflichkeit",
            "argumentation",
            "reformulierung",
        ],
    ),
    GrammarTopic(
        slug="kulturelle-referenzen",
        title="Kulturelle Referenzen und Zitate",
        level="C1",
        category="Wortschatz",
        summary="Kulturelle Referenzen und Zitate – literarische Anspielungen, Intertextualität und kulturelles Wissen im deutschen Sprachraum.",
        explanation="""Kulturelle Referenzen erfordern geteiltes Wissen zwischen Sprecher und Hörer. Wichtige Quellen:
Klassiker-Zitate: Faust (Goethe): Das also war des Pudels Kern. / Wer immer strebend sich bemüht, den können wir erlösen. Schiller (Wilhelm Tell): Der brave Mann denkt an sich selbst zuletzt. / Durch diese hohle Gasse muss er kommen.
Brecht: Erst kommt das Fressen, dann kommt die Moral. / Und der Haifisch, der hat Zähne.
Literarische Anspielungen: kafkaesk (nach Kafka, absurde Bürokratie), faustisch (nach Faust, maßloses Streben), Stunde Null (Neuanfang nach 1945).
Sprichwörter und geflügelte Worte: Wer zuerst kommt, mahlt zuerst. / Aller Anfang ist schwer. / Die Axt im Hause erspart den Zimmermann.
Intertextualität: Das Zitieren und Anspielen auf bekannte Texte ist ein typisches Merkmal gehobener deutscher Alltags- und Medienkommunikation.""",
        structure="Referenz (Literatur, Sprichwort, Geschichte) → Anspielung → geteiltes kulturelles Wissen",
        rules=[
            "Kulturelle Referenzen setzen geteiltes Wissen voraus.",
            "Goethe, Schiller und Brecht sind die meistzitierten Autoren.",
            "Geflügelte Worte und Sprichwörter sind feste Bestandteile der Alltagssprache.",
            "Das Erkennen und Verwenden kultureller Referenzen signalisiert Bildung und Zugehörigkeit.",
        ],
        examples=[
            GrammarExample(
                text="Damit sind wir am Ende der Fahnenstange angelangt.",
                translation=None,
                note="geflügeltes Wort",
            ),
            GrammarExample(
                text="Nun ist das also des Pudels Kern!",
                translation=None,
                note="Faust-Zitat",
            ),
            GrammarExample(
                text="Die Bearbeitung meines Antrags war geradezu kafkaesk.",
                translation=None,
                note="literarische Anspielung",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Referenzen ohne Verständnis des Kontextes benutzen.",
                correct="Nur Referenzen verwenden, die man wirklich versteht.",
                note="Falsche Verwendung wirkt peinlich und ungebildet.",
            ),
        ],
        related=["redewendungen", "ironie", "rhetorische-mittel", "gehobene-sprache"],
    ),
]
