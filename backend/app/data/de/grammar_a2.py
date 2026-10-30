"""German grammar topics — A2."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="perfekt-mit-haben",
        title='Perfekt mit "haben"',
        level="A2",
        category="Zeitformen",
        summary='Das Perfekt mit "haben" – Bildung und Verwendung für die meisten Verben.',
        explanation="""Das **Perfekt** ist die wichtigste Vergangenheitsform im gesprochenen Deutsch. Es wird mit einem Hilfsverb (**haben** oder **sein**) + **Partizip II** gebildet. Die meisten Verben bilden das Perfekt mit **haben**:

**Bildung:** **haben** (konjugiert) + **Partizip II** (am Satzende)
ich habe gemacht · du hast gemacht · er/es/sie hat gemacht · wir haben gemacht · ihr habt gemacht · sie/Sie haben gemacht

**Welche Verben verwenden haben?** Transitive Verben, reflexive Verben, Modalverben, unpersönliche Verben und die meisten intransitiven Verben ohne Ortswechsel.

**Satzklammer:** Das Hilfsverb steht auf Position 2, das Partizip II am Satzende: *Ich **habe** gestern einen Film **gesehen**.*""",
        structure="haben (konjugiert, Position 2) + ... + Partizip II (Satzende)",
        rules=[
            "Die meisten deutschen Verben bilden das Perfekt mit 'haben'.",
            'Das Hilfsverb "haben" wird konjugiert und steht auf Position 2.',
            "Das Partizip II steht immer am Satzende.",
            'Transitive Verben, reflexive Verben und Modalverben verwenden immer "haben".',
            "Im Perfekt tritt eine Satzklammer auf: Hilfsverb ... Partizip II.",
        ],
        examples=[
            GrammarExample(
                text="Ich habe gestern Fußball gespielt.",
                translation=None,
            ),
            GrammarExample(text="Hast du den Film gesehen?", translation=None),
            GrammarExample(text="Er hat lange geschlafen.", translation=None),
            GrammarExample(text="Wir haben im Restaurant gegessen.", translation=None),
            GrammarExample(text="Sie hat mir nicht geantwortet.", translation=None),
            GrammarExample(text="Habt ihr die Hausaufgaben gemacht?", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich habe gegangen.",
                correct="Ich bin gegangen.",
                note='Verben der Bewegung (gehen) verwenden "sein", nicht "haben".',
            ),
            GrammarMistake(
                wrong="Ich habe gestern Fußball gespielen.",
                correct="Ich habe gestern Fußball gespielt.",
                note='Das Partizip II von "spielen" ist "gespielt" (regelmäßig: ge + Stamm + t).',
            ),
        ],
        related=[
            "perfekt-mit-sein",
            "partizip-ii",
            "perfekt-vs-praeteritum",
            "verb-haben",
        ],
    ),
    GrammarTopic(
        slug="perfekt-mit-sein",
        title='Perfekt mit "sein"',
        level="A2",
        category="Zeitformen",
        summary='Das Perfekt mit "sein" – für Verben der Bewegung, Zustandsänderung und besondere Verben.',
        explanation="""Eine kleinere Gruppe von Verben bildet das Perfekt mit dem Hilfsverb **sein**:
**sein** (konjugiert) + **Partizip II** (am Satzende)
ich bin gegangen · du bist gegangen · er ist gegangen · wir sind gegangen · ihr seid gegangen · sie sind gegangen

**Welche Verben verwenden sein?**
1. Bewegungsverben mit Ortswechsel: gehen, fahren, laufen, fliegen, schwimmen, reisen, kommen, wandern
2. Zustandsänderung: aufwachen, einschlafen, sterben, werden, wachsen, fallen
3. Spezialverben: sein, werden, bleiben, passieren, geschehen""",
        structure="sein (konjugiert, Position 2) + ... + Partizip II (am Satzende)",
        rules=[
            'Verben mit Ortswechsel (A→B) bilden das Perfekt mit "sein".',
            'Verben der Zustandsänderung (aufwachen, sterben, werden) verwenden "sein".',
            '"Sein", "werden", "bleiben", "passieren" sind die Spezialverben mit "sein".',
            'Das Hilfsverb "sein" wird konjugiert und steht auf Position 2.',
            'Reflexive Verben verwenden immer "haben", auch bei Bewegung: "Ich habe mich bewegt."',
        ],
        examples=[
            GrammarExample(
                text="Ich bin gestern nach Hamburg gefahren.",
                translation=None,
            ),
            GrammarExample(text="Bist du mit dem Zug gekommen?", translation=None),
            GrammarExample(text="Er ist um 6 Uhr aufgewacht.", translation=None),
            GrammarExample(text="Wir sind zu Hause geblieben.", translation=None),
            GrammarExample(text="Was ist passiert?", translation=None),
            GrammarExample(
                text="Sie sind schnell gewachsen.",
                translation=None,
                note="Zustandsänderung",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich habe nach Hause gegangen.",
                correct="Ich bin nach Hause gegangen.",
                note='"Gehen" ist ein Bewegungsverb und verwendet "sein".',
            ),
            GrammarMistake(
                wrong="Er hat Arzt geworden.",
                correct="Er ist Arzt geworden.",
                note='"Werden" bildet das Perfekt mit "sein".',
            ),
        ],
        related=[
            "perfekt-mit-haben",
            "partizip-ii",
            "perfekt-vs-praeteritum",
            "verb-sein",
        ],
    ),
    GrammarTopic(
        slug="partizip-ii",
        title="Partizip II",
        level="A2",
        category="Zeitformen",
        summary="Bildung des Partizips II – regelmäßige, unregelmäßige und gemischte Muster.",
        explanation="""Das **Partizip II** wird für Perfekt, Plusquamperfekt und Passiv benötigt.

1. Regelmäßige (schwache) Verben: **ge + Stamm + t** — machen → gemacht, spielen → gespielt, wohnen → gewohnt, arbeiten → gearbeitet

2. Unregelmäßige (starke) Verben: **ge + Stamm (Vokalwechsel) + en** — sehen → gesehen, essen → gegessen, trinken → getrunken, schreiben → geschrieben

3. Gemischte Verben: **ge + Stamm (Vokalwechsel) + t** — bringen → gebracht, denken → gedacht, kennen → gekannt, wissen → gewusst

4. Verben ohne ge-: untrennbare Präfixe (be-, er-, ver-, zer-, ent-, miss-, emp-) oder auf -ieren — besuchen → besucht, erklären → erklärt, studieren → studiert

5. Trennbare Verben: ge- steht zwischen Präfix und Stamm — aufgestanden, eingekauft""",
        structure="Regelmäßig: ge + Stamm + t · Unregelmäßig: ge + Stamm (Wechsel) + en · Ohne ge-: untrennbare Präfixe und -ieren Verben",
        rules=[
            "Regelmäßige Verben: ge- + Verbstamm + -t (gemacht, gespielt).",
            "Unregelmäßige Verben: ge- + veränderter Stamm + -en (gesehen, getrunken).",
            "Verben auf -ieren und mit untrennbarem Präfix bekommen kein ge- (studiert, besucht).",
            "Trennbare Verben: Präfix + ge + Stamm + t/en (aufgestanden, eingekauft).",
            "Die wichtigsten unregelmäßigen Partizipien sollte man auswendig lernen.",
        ],
        examples=[
            GrammarExample(text="machen → gemacht", translation=None, note="regelmäßig"),
            GrammarExample(text="sehen → gesehen", translation=None, note="unregelmäßig"),
            GrammarExample(
                text="aufstehen → aufgestanden",
                translation=None,
                note="trennbar",
            ),
            GrammarExample(
                text="besuchen → besucht",
                translation=None,
                note="untrennbar, kein ge-",
            ),
            GrammarExample(
                text="studieren → studiert",
                translation=None,
                note="-ieren, kein ge-",
            ),
            GrammarExample(text="bringen → gebracht", translation=None, note="gemischt"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich habe gestudiert.",
                correct="Ich habe studiert.",
                note='Verben auf "-ieren" bilden das Partizip II ohne "ge-".',
            ),
            GrammarMistake(
                wrong="aufgemacht → Ich habe die Tür aufgegemacht.",
                correct="aufgemacht → Ich habe die Tür aufgemacht.",
                note="Trennbare Verben: das Präfix steht VOR dem ge-. auf + ge + macht = aufgemacht.",
            ),
        ],
        related=["perfekt-mit-haben", "perfekt-mit-sein", "praeteritum-sein-haben"],
    ),
    GrammarTopic(
        slug="praeteritum-sein-haben",
        title="Präteritum von sein und haben",
        level="A2",
        category="Zeitformen",
        summary="Das Präteritum von sein und haben – die Grundlage für das narrative Präteritum.",
        explanation="""Im gesprochenen Deutsch wird häufig das **Perfekt** verwendet. Bei **sein** und **haben** ist auch das **Präteritum** sehr gebräuchlich. Die Wahl hängt unter anderem von Region und Kontext ab.

Präteritum von **sein**: ich war, du warst, er/es/sie war, wir waren, ihr wart, sie/Sie waren
Präteritum von **haben**: ich hatte, du hattest, er/es/sie hatte, wir hatten, ihr hattet, sie/Sie hatten

*Gestern **war** ich im Kino.* Auch korrekt: *Gestern bin ich im Kino gewesen.*
*Ich **hatte** keine Zeit.* Auch korrekt: *Ich habe keine Zeit gehabt.*

In schriftlichen Erzählungen und Berichten ist das Präteritum häufig die Grundzeit. Im Gespräch sind besonders sein, haben und Modalverben im Präteritum üblich; andere Verben sind je nach Region und Kontext ebenfalls möglich.""",
        structure="ich war/hatte · du warst/hattest · er/es/sie war/hatte · wir waren/hatten · ihr wart/hattet · sie waren/hatten",
        rules=[
            'Im gesprochenen Deutsch sind "war" und "hatte" sehr gebräuchlich; die Perfektformen sind ebenfalls korrekt.',
            "In schriftlichen Erzählungen ist das Präteritum häufig die Grundzeit.",
            'Die 1. und 3. Person Singular sind gleich: "war" und "hatte".',
            "Die Modalverben werden im gesprochenen Deutsch auch meist im Präteritum verwendet.",
            "Das Präteritum ist eine einteilige Vergangenheitsform (kein Hilfsverb nötig).",
        ],
        examples=[
            GrammarExample(text="Gestern war ich im Kino.", translation=None),
            GrammarExample(text="Warst du schon in Berlin?", translation=None),
            GrammarExample(text="Ich hatte einen anstrengenden Tag.", translation=None),
            GrammarExample(
                text="Wir waren letzte Woche im Urlaub.",
                translation=None,
            ),
            GrammarExample(text="Er hatte kein Geld dabei.", translation=None),
            GrammarExample(text="Wart ihr schon essen?", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gestern ich war im Kino.",
                correct="Gestern war ich im Kino.",
                note='Nach dem vorangestellten Zeitadverb steht das konjugierte Verb an zweiter Position: "Gestern war ich ...".',
            ),
            GrammarMistake(
                wrong="Ich war keine Zeit.",
                correct="Ich hatte keine Zeit.",
                note='"Keine Zeit haben" verwendet "haben", nicht "sein".',
            ),
        ],
        related=[
            "perfekt-mit-haben",
            "perfekt-mit-sein",
            "praeteritum-modalverben",
            "perfekt-vs-praeteritum",
        ],
    ),
    GrammarTopic(
        slug="praeteritum-modalverben",
        title="Präteritum der Modalverben",
        level="A2",
        category="Zeitformen",
        summary="Präteritum der Modalverben – wie man vergangene Fähigkeit, Verpflichtung und Erlaubnis ausdrückt.",
        explanation="""Für vergangene Situationen stehen Modalverben im gesprochenen Deutsch häufig im **Präteritum**. Auch das Perfekt ist korrekt.

können → konnte / müssen → musste / dürfen → durfte / wollen → wollte / sollen → sollte / mögen → mochte

**Achtung:** Im Präteritum verlieren Modalverben den **Umlaut**! *Ich **konnte** nicht kommen.* (nicht: könnte — das ist Konjunktiv II!)

*Ich **konnte** gestern nicht kommen, weil ich krank war.*
*Als Kind **durfte** ich nicht so lange fernsehen.*
*Er **wollte** uns helfen, aber er hatte keine Zeit.*

Das Perfekt der Modalverben (*Ich habe kommen können*) ist ebenfalls möglich. Welche Form üblich ist, hängt auch von Region und Kontext ab.""",
        structure="Modalverb im Präteritum (Position 2) + ... + Infinitiv (Satzende)",
        rules=[
            "Modalverben werden im gesprochenen Deutsch meist im Präteritum verwendet.",
            "Im Präteritum verlieren Modalverben den Umlaut: können → konnte (nicht: könnte).",
            '"Mögen" im Präteritum: mochte (bedeutet "liked"). Möchten (would like) gibt es nur im Konjunktiv II.',
            "Die Präteritum-Formen haben -te, teilweise mit verändertem Stamm: konnte, musste, durfte, wollte, sollte, mochte.",
            'Das Präteritum der Modalverben wird ohne "haben" verwendet (einteilig).',
        ],
        examples=[
            GrammarExample(
                text="Ich konnte gestern nicht zur Party kommen.",
                translation=None,
            ),
            GrammarExample(
                text="Als Kind durfte ich nicht so lange aufbleiben.",
                translation=None,
            ),
            GrammarExample(
                text="Er musste am Wochenende arbeiten.",
                translation=None,
            ),
            GrammarExample(
                text="Wir wollten eigentlich wandern gehen.",
                translation=None,
            ),
            GrammarExample(
                text="Als Kind sollte ich jeden Abend um acht im Bett sein.",
                translation=None,
                note="sollen im Präteritum: damalige Anweisung; ein heutiger Ratschlag mit sollte wäre Konjunktiv II",
            ),
            GrammarExample(
                text="Ich mochte die Schule nicht.",
                translation=None,
                note="mögen im Präteritum",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich könnte gestern nicht kommen.",
                correct="Ich konnte gestern nicht kommen.",
                note='Könnte ist Konjunktiv II. Das Präteritum von können ist "konnte" (ohne Umlaut).',
            ),
            GrammarMistake(
                wrong="Wir mussten gestern gearbeitet.",
                correct="Wir mussten gestern arbeiten.",
                note="Nach dem Modalverb im Präteritum steht der Infinitiv, nicht das Partizip II.",
            ),
        ],
        related=["modalverben", "praeteritum-sein-haben", "perfekt-vs-praeteritum"],
    ),
    GrammarTopic(
        slug="perfekt-vs-praeteritum",
        title="Perfekt vs Präteritum",
        level="A2",
        category="Zeitformen",
        summary="Wann Perfekt, wann Präteritum – gesprochen vs. geschrieben, Norden vs. Süden.",
        explanation="""Deutsch hat zwei Haupt-Vergangenheitsformen.

**Perfekt** (habe gemacht / bin gegangen): Gesprochene Sprache, informelle Texte, E-Mails, WhatsApp. In Süddeutschland, Österreich und Schweiz sogar noch häufiger.

**Präteritum** (machte / ging): Häufig in Erzählungen, Berichten und Literatur. Im gesprochenen Deutsch besonders bei sein, haben und Modalverben, regional und je nach Kontext auch bei anderen Verben.

| Situation | Empfehlung |
|-----------|------------|
| Sprechen (Alltag) | Häufig Perfekt; auch war, hatte, konnte usw. |
| Schriftliche Erzählungen / Berichte | Häufig Präteritum |
| E-Mails / WhatsApp | Meist Perfekt |
| Geschichten erzählen | Schriftlich häufig Präteritum, mündlich auch Perfekt |""",
        structure="Alltagsgespräch: häufig Perfekt, auch Präteritum · Schriftliche Erzählung: häufig Präteritum",
        rules=[
            "Im Alltagsgespräch ist das Perfekt häufig; die Wahl hängt auch von Verb, Region und Kontext ab.",
            "In schriftlichen Erzählungen und Berichten dominiert das Präteritum.",
            "Sein, haben und Modalverben sind im Präteritum auch im Gespräch gebräuchlich; ihre Perfektformen bleiben korrekt.",
            "Im Norden Deutschlands wird das Präteritum tendenziell etwas häufiger verwendet.",
            "Bei zweiteiligen Sätzen im Perfekt entsteht die Satzklammer: habe ... gesehen.",
        ],
        examples=[
            GrammarExample(
                text="Gestern habe ich einen Film gesehen.",
                translation=None,
                note="gesprochen: Perfekt",
            ),
            GrammarExample(
                text="Gestern sah ich einen Film.",
                translation=None,
                note="geschrieben: Präteritum",
            ),
            GrammarExample(
                text="Ich war müde.",
                translation=None,
                note="auch gesprochen häufig: Präteritum von sein",
            ),
            GrammarExample(
                text="Sie hatte keine Zeit.",
                translation=None,
                note="gesprochen: Präteritum von haben",
            ),
            GrammarExample(
                text="Er konnte nicht kommen.",
                translation=None,
                note="gesprochen: Präteritum Modalverb",
            ),
            GrammarExample(
                text="Letzten Sommer fuhren wir nach Italien.",
                translation=None,
                note="geschrieben: Präteritum",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gestern bin ich ein Film gesehen.",
                correct="Gestern habe ich einen Film gesehen.",
                note='"Einen Film sehen" ist transitiv (Akkusativobjekt) und verwendet "haben", nicht "sein".',
            ),
            GrammarMistake(
                wrong="Er machte die Tür auf und geht rein.",
                correct="Er machte die Tür auf und ging hinein.",
                note="Ohne beabsichtigten Perspektivwechsel bleiben diese aufeinanderfolgenden vergangenen Handlungen in derselben Erzählzeit.",
            ),
        ],
        related=[
            "perfekt-mit-haben",
            "perfekt-mit-sein",
            "praeteritum-sein-haben",
            "praeteritum-modalverben",
        ],
    ),
    GrammarTopic(
        slug="dativ-objekt",
        title="Dativobjekt",
        level="A2",
        category="Kasus",
        summary="Das Dativobjekt – indirekte Objekte, Dativverben und Dativ-Personalpronomen.",
        explanation="""Das **Dativobjekt** ist das indirekte Objekt im Satz (Wem?). Es steht vor dem Akkusativobjekt, wenn beide Nomen sind. Ist das Akkusativobjekt ein Pronomen, steht es vor dem Dativobjekt.

Verben mit Dativ: helfen (+Dat), danken (+Dat), antworten (+Dat), gefallen (+Dat), gehören (+Dat), schmecken (+Dat), passen (+Dat), glauben (+Dat)

Personalpronomen im Dativ: mir, dir, ihm, ihr, ihm, uns, euch, ihnen/Ihnen""",
        structure="Subjekt + Verb + Dativobjekt (Wem?) + Akkusativobjekt (Was?)",
        rules=[
            'Das Dativobjekt antwortet auf die Frage "Wem?".',
            "Bei zwei Nomen: Dativ vor Akkusativ.",
            "Es gibt Verben, die ein Dativobjekt verlangen (helfen, danken, gefallen, gehören...).",
            "Die Personalpronomen im Dativ: mir, dir, ihm, ihr, ihm, uns, euch, ihnen.",
            "Nach Dativ-Präpositionen (mit, nach, zu, bei, von, aus, seit) steht ebenfalls Dativ.",
        ],
        examples=[
            GrammarExample(text="Ich gebe dem Mann das Buch.", translation=None),
            GrammarExample(text="Kannst du mir helfen?", translation=None),
            GrammarExample(
                text="Das Kleid gefällt ihr.",
                translation=None,
                note="gefallen + Dativ",
            ),
            GrammarExample(text="Ich danke dir für das Geschenk.", translation=None),
            GrammarExample(text="Gehört das Auto ihm?", translation=None),
            GrammarExample(
                text="Die Musik ist zu laut. Sie stört mich.",
                translation=None,
                note="stören braucht Akkusativ",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich helfe dich.",
                correct="Ich helfe dir.",
                note='"Helfen" verlangt immer Dativ (helfen + wem?).',
            ),
            GrammarMistake(
                wrong="Sie gibt den Mann das Buch.",
                correct="Sie gibt dem Mann das Buch.",
                note='Das indirekte Objekt muss im Dativ stehen. "Der Mann" → "dem Mann".',
            ),
        ],
        related=["dativ-basic", "personalpronomen-akk-dat", "akkusativ"],
    ),
    GrammarTopic(
        slug="wechselpraepositionen",
        title="Wechselpräpositionen",
        level="A2",
        category="Präpositionen",
        summary="Wechselpräpositionen – Dativ für Ort (Wo?), Akkusativ für Richtung (Wohin?).",
        explanation="""Die **Wechselpräpositionen** können sowohl mit Dativ als auch mit Akkusativ stehen — je nach Bedeutung.

Die 9 Wechselpräpositionen: **in, an, auf, hinter, neben, vor, unter, über, zwischen**

| Frage | Fall | Bedeutung |
|-------|------|-----------|
| **Wo?** (Wo befindet sich etwas?) | **Dativ** | Position / fester Ort |
| **Wohin?** (Wohin bewegt sich etwas?) | **Akkusativ** | Richtung / Bewegung zu einem Ziel |

Kontraktionen: in + das = ins (Wohin?), in + dem = im (Wo?), an + das = ans (Wohin?), an + dem = am (Wo?)

**Verben der Position** (sein, stehen, liegen, sitzen, hängen) → Dativ.
**Verben der Bewegung** (gehen, legen, stellen, setzen, hängen) → Akkusativ.""",
        structure="Wo? → Dativ | Wohin? → Akkusativ",
        rules=[
            'Bei Ortsangabe (Wo?) steht Dativ: "Ich bin im Kino."',
            'Bei Richtungsangabe (Wohin?) steht Akkusativ: "Ich gehe ins Kino."',
            "Kontraktionen: ins (in das), im (in dem), ans (an das), am (an dem).",
            "Die gleiche Präposition kann beide Fälle regieren — die Bedeutung entscheidet.",
            "Verben der Position → Dativ. Verben der Bewegung → Akkusativ.",
        ],
        examples=[
            GrammarExample(text="Ich bin im Garten.", translation=None, note="Wo? → Dativ"),
            GrammarExample(
                text="Ich gehe in den Garten.",
                translation=None,
                note="Wohin? → Akkusativ",
            ),
            GrammarExample(
                text="Das Bild hängt an der Wand.",
                translation=None,
                note="Position → Dativ",
            ),
            GrammarExample(
                text="Ich hänge das Bild an die Wand.",
                translation=None,
                note="Bewegung → Akkusativ",
            ),
            GrammarExample(
                text="Die Katze springt auf den Tisch.",
                translation=None,
                note="Wohin? → Akkusativ",
            ),
            GrammarExample(
                text="Die Katze sitzt auf dem Tisch.",
                translation=None,
                note="Wo? → Dativ",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich gehe in dem Supermarkt.",
                correct="Ich gehe in den Supermarkt.",
                note='Bewegung mit "gehen" = Richtung (Wohin?) → Akkusativ.',
            ),
            GrammarMistake(
                wrong="Das Buch liegt auf den Tisch.",
                correct="Das Buch liegt auf dem Tisch.",
                note='"Liegen" ist ein Positionsverb (Wo?) → Dativ.',
            ),
        ],
        related=["lokalpraepositionen", "akkusativ", "dativ-basic", "dativ-objekt"],
    ),
    GrammarTopic(
        slug="personalpronomen-akk-dat",
        title="Personalpronomen im Akkusativ und Dativ",
        level="A2",
        category="Pronomen",
        summary="Personalpronomen im Akkusativ und Dativ – mich/dich, mir/dir und die vollständige Tabelle.",
        explanation="""Personalpronomen ändern sich je nach Fall:

| Nominativ | Akkusativ | Dativ |
|-----------|-----------|-------|
| ich | mich | mir |
| du | dich | dir |
| er | ihn | ihm |
| sie | sie | ihr |
| es | es | ihm |
| wir | uns | uns |
| ihr | euch | euch |
| sie (Pl.) | sie | ihnen |
| Sie (formell) | Sie | Ihnen |

Akkusativ: direktes Objekt (Wen? Was?), nach Akkusativ-Präpositionen — *Ich sehe **dich**.*
Dativ: indirektes Objekt (Wem?), nach Dativ-Präpositionen — *Ich helfe **dir**.*""",
        structure="Akk: mich · dich · ihn · sie · es · uns · euch · sie · Sie / Dat: mir · dir · ihm · ihr · ihm · uns · euch · ihnen · Ihnen",
        rules=[
            '"Mich" und "dich" sind Akkusativ; "mir" und "dir" sind Dativ.',
            '"Ihn" ist Akkusativ maskulin, "ihm" ist Dativ maskulin/neutral.',
            '"Ihr" kann Nominativ (2. Person Plural), Dativ feminin oder Possessivartikel sein.',
            '"Ihnen" (großgeschrieben) ist die Dativ-Höflichkeitsform.',
            'Nach "für" und "ohne" steht immer Akkusativ, nach "mit" und "zu" immer Dativ.',
        ],
        examples=[
            GrammarExample(text="Ich sehe dich.", translation=None, note="Akkusativ"),
            GrammarExample(text="Kannst du mir helfen?", translation=None, note="Dativ"),
            GrammarExample(
                text="Das Geschenk ist für ihn.",
                translation=None,
                note="Akkusativ nach für",
            ),
            GrammarExample(
                text="Ich fahre mit ihr nach Berlin.",
                translation=None,
                note="Dativ nach mit",
            ),
            GrammarExample(
                text="Wir warten auf euch.",
                translation=None,
                note="Akkusativ nach auf",
            ),
            GrammarExample(
                text="Ich möchte Ihnen danken.",
                translation=None,
                note="formell, Dativ",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich helfe dich.",
                correct="Ich helfe dir.",
                note='"Helfen" verlangt Dativ: "dir", nicht "dich".',
            ),
            GrammarMistake(
                wrong="Das ist für dir.",
                correct="Das ist für dich.",
                note='"Für" ist eine Akkusativ-Präposition: "dich".',
            ),
        ],
        related=["akkusativ", "dativ-basic", "dativ-objekt", "personalpronomen"],
    ),
    GrammarTopic(
        slug="komparativ",
        title="Komparativ",
        level="A2",
        category="Adjektive",
        summary="Der Komparativ – wie man zwei Dinge mit -er und als vergleicht.",
        explanation="""Der **Komparativ** wird verwendet, um zwei Dinge zu vergleichen: **Adjektiv + -er** + **als**

schnell → schneller, groß → größer, klein → kleiner, schön → schöner

**Umlaut im Komparativ:** Viele einsilbige Adjektive mit a, o, u bekommen Umlaut: alt → älter, groß → größer, jung → jünger, kurz → kürzer, warm → wärmer, stark → stärker

⚠️ Vergleich mit **als**, nicht *wie*: *Peter ist größer **als** Paul.*

**Unregelmäßige Formen:** gut → besser, gern → lieber, viel → mehr, hoch → höher""",
        structure="Adjektiv + -er + als + Vergleichsobjekt",
        rules=[
            'Der Komparativ wird mit "-er" gebildet: schnell → schneller.',
            "Viele einsilbige Adjektive mit a/o/u bekommen Umlaut: groß → größer.",
            'Der Vergleich erfolgt mit "als": "größer als", nicht "größer wie".',
            "Einige Adjektive sind unregelmäßig: gut → besser, viel → mehr, gern → lieber.",
            "Attributiv verwendete Komparative brauchen Adjektivdeklination: ein schnelleres Auto.",
        ],
        examples=[
            GrammarExample(
                text="Mein Auto ist schneller als deins.",
                translation=None,
            ),
            GrammarExample(text="Berlin ist größer als München.", translation=None),
            GrammarExample(
                text="Meine Schwester ist jünger als ich.",
                translation=None,
            ),
            GrammarExample(
                text="Dieses Buch ist besser als das andere.",
                translation=None,
            ),
            GrammarExample(
                text="Der Sommer ist wärmer als der Frühling.",
                translation=None,
                note="Umlaut",
            ),
            GrammarExample(
                text="Sie spricht schneller Deutsch als ich.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Berlin ist größer wie München.",
                correct="Berlin ist größer als München.",
                note='Im Deutschen verwendet man "als" für Komparativ-Vergleiche, nicht "wie".',
            ),
            GrammarMistake(
                wrong="Mein Auto ist mehr schnell als deins.",
                correct="Mein Auto ist schneller als deins.",
                note='Kein "mehr" mit Adjektiven — immer die Endung -er.',
            ),
        ],
        related=["superlativ", "vergleich-als-wie", "adjektive"],
    ),
    GrammarTopic(
        slug="superlativ",
        title="Superlativ",
        level="A2",
        category="Adjektive",
        summary="Der Superlativ – den höchsten Grad ausdrücken mit am ...sten und der/die/das ...ste.",
        explanation="""Der **Superlativ** drückt den höchsten Grad aus.

**Zwei Formen:**
1. **am + Adjektiv + -sten** (prädikativ): *Dieses Auto ist **am schnellsten**.*
2. **der/die/das + Adjektiv + -ste** (attributiv): *Das ist **der schnellste** Wagen.*

**Umlaut** (wie beim Komparativ): groß → am größten, jung → am jüngsten, alt → am ältesten

**-esten:** Adjektive auf -d, -t, -s, -ß, -z, -sch bekommen -esten: kurz → am kürzesten, süß → am süßesten

**Unregelmäßig:** gut → am besten, gern → am liebsten, viel → am meisten, hoch → am höchsten""",
        structure="am + Adjektiv + -(e)sten (prädikativ) · der/die/das + Adjektiv + -ste (attributiv)",
        rules=[
            "Prädikativ: am + Adjektiv + -sten: am schnellsten.",
            "Attributiv vor Nomen: der/die/das + Adjektiv + -ste: der schnellste Wagen.",
            "Umlaut bei a/o/u: groß → am größten, jung → am jüngsten.",
            "Nach -d/-t/-s/-ß/-z/-sch: -esten statt -sten: am kürzesten.",
            "Unregelmäßig: gut → am besten, gern → am liebsten, viel → am meisten.",
        ],
        examples=[
            GrammarExample(
                text="Usain Bolt ist der schnellste Läufer der Welt.",
                translation=None,
            ),
            GrammarExample(text="Dieses Restaurant ist am besten.", translation=None),
            GrammarExample(
                text="Der Mount Everest ist der höchste Berg.",
                translation=None,
            ),
            GrammarExample(
                text="Am liebsten trinke ich Wasser.",
                translation=None,
                note="unregelmäßig",
            ),
            GrammarExample(
                text="Das ist das teuerste Hotel der Stadt.",
                translation=None,
            ),
            GrammarExample(
                text="Er spricht am schnellsten von allen.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Er ist der am schnellsten Läufer.",
                correct="Er ist der schnellste Läufer.",
                note='Attributiv: "der schnellste", nicht "der am schnellsten".',
            ),
            GrammarMistake(
                wrong="Das ist das am beste Restaurant.",
                correct="Das ist das beste Restaurant.",
                note='"Am besten" ist prädikativ, "das beste" ist attributiv.',
            ),
        ],
        related=[
            "komparativ",
            "vergleich-als-wie",
            "adjektive",
            "adjektivdeklination-best",
        ],
    ),
    GrammarTopic(
        slug="vergleich-als-wie",
        title="Vergleich mit als und wie",
        level="A2",
        category="Syntax",
        summary="Vergleich mit als und wie – Gleichheit (so ... wie) vs. Unterschied (Komparativ + als).",
        explanation="""Für Vergleiche im Deutschen verwendet man zwei verschiedene Strukturen:

**Gleichheit: so + Adjektiv + wie** — *Peter ist **so groß wie** Paul.* / *Deutsch ist **so schwer wie** Französisch.*

**Ungleichheit: Komparativ + als** — *Peter ist **größer als** Paul.* / *Deutsch ist **schwerer als** Englisch.*

**Spezialfall: je ... desto/umso** — *Je mehr ich lerne, **desto** besser verstehe ich.*

⚠️ In manchen deutschen Dialekten wird *wie* auch für Komparative verwendet (*besser wie*), das gilt standardsprachlich als falsch.""",
        structure="Gleichheit: so + Adjektiv + wie · Ungleichheit: Adjektiv-er + als",
        rules=[
            'Gleichheit: "so + Adjektiv/Grundform + wie".',
            'Verschiedenheit: "Komparativ (-er) + als".',
            "Je ... desto/umso drückt eine proportionale Beziehung aus.",
            'Im Standarddeutschen niemals "besser wie" — es muss "besser als" heißen.',
            '"Nicht so ... wie" verneint die Gleichheit.',
        ],
        examples=[
            GrammarExample(
                text="Sie ist so intelligent wie ihr Bruder.",
                translation=None,
                note="Gleichheit",
            ),
            GrammarExample(
                text="Deutsch ist nicht so schwer wie Chinesisch.",
                translation=None,
                note="negative Gleichheit",
            ),
            GrammarExample(
                text="Dieses Auto ist teurer als jenes.",
                translation=None,
                note="Ungleichheit",
            ),
            GrammarExample(
                text="Je mehr du übst, desto besser wirst du.",
                translation=None,
            ),
            GrammarExample(text="Ich bin so müde wie gestern.", translation=None),
            GrammarExample(text="Er läuft schneller als ich.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Sie ist so intelligent als ihr Bruder.",
                correct="Sie ist so intelligent wie ihr Bruder.",
                note='Gleichheit verwendet "wie", nicht "als".',
            ),
            GrammarMistake(
                wrong="Er ist besser wie ich.",
                correct="Er ist besser als ich.",
                note='Komparativ + "als", nicht "wie". Dialektal verbreitet, aber standardsprachlich falsch.',
            ),
        ],
        related=["komparativ", "superlativ", "adjektive"],
    ),
    GrammarTopic(
        slug="adjektivdeklination-best",
        title="Adjektivdeklination nach bestimmtem Artikel",
        level="A2",
        category="Adjektive",
        summary="Adjektivdeklination nach der/die/das – die schwache Deklination mit -e oder -en.",
        explanation="""Nach dem **bestimmten Artikel** (der/die/das) folgt die **schwache Deklination**:

| Fall | maskulin | feminin | neutral | Plural |
|------|----------|---------|---------|--------|
| Nom. | der gute Wein | die gute Suppe | das gute Brot | die guten Weine |
| Akk. | den guten Wein | die gute Suppe | das gute Brot | die guten Weine |
| Dat. | dem guten Wein | der guten Suppe | dem guten Brot | den guten Weinen |

**Faustregel:** Nach der/die/das ist die Endung entweder **-e** oder **-en**.
- **-e**: Nominativ Singular (alle Genera) + Akkusativ feminin + Akkusativ neutral
- **-en**: Alle anderen Fälle und immer im Plural""",
        structure="der/die/das + Adjektiv + -e/-en + Nomen",
        rules=[
            "Nach dem bestimmten Artikel endet das Adjektiv meist auf -e oder -en.",
            "Nominativ Singular (alle Genera) und Akkusativ feminin/neutral: Endung -e.",
            "Akkusativ maskulin, Dativ (alle) und Plural (alle): Endung -en.",
            "Die schwache Deklination ist einfacher als die starke und gemischte.",
            "Die Artikel geben Genus und Fall bereits an, deshalb reichen -e/-en.",
        ],
        examples=[
            GrammarExample(text="der große Hund", translation=None, note="Nom. maskulin: -e"),
            GrammarExample(
                text="Ich kaufe den roten Pullover.",
                translation=None,
                note="Akk. maskulin: -en",
            ),
            GrammarExample(text="die nette Kellnerin", translation=None, note="Nom. feminin: -e"),
            GrammarExample(text="mit dem alten Auto", translation=None, note="Dat. neutral: -en"),
            GrammarExample(text="die kleinen Kinder", translation=None, note="Nom. Plural: -en"),
            GrammarExample(text="in der großen Stadt", translation=None, note="Dat. feminin: -en"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="der großer Hund",
                correct="der große Hund",
                note='Nach "der" im Nominativ maskulin: Adjektivendung ist -e, nicht -er.',
            ),
            GrammarMistake(
                wrong="Ich sehe der große Hund.",
                correct="Ich sehe den großen Hund.",
                note='Das direkte Objekt (Akkusativ) verlangt "den": Artikel und Adjektivendung ändern sich.',
            ),
        ],
        related=[
            "adjektivdeklination-unbest",
            "adjektivdeklination-null",
            "bestimmte-artikel",
            "adjektive",
            "akkusativ",
        ],
    ),
    GrammarTopic(
        slug="adjektivdeklination-unbest",
        title="Adjektivdeklination nach unbestimmtem Artikel",
        level="A2",
        category="Adjektive",
        summary="Adjektivdeklination nach ein/eine – die gemischte Deklination.",
        explanation="""Nach **ein, eine, kein, keine** und den **Possessivartikeln** (mein, dein, sein...) folgt die **gemischte Deklination**:

| Fall | maskulin | feminin | neutral | Plural (keine) |
|------|----------|---------|---------|----------------|
| Nom. | ein guter Wein | eine gute Suppe | ein gutes Brot | keine guten Weine |
| Akk. | einen guten Wein | eine gute Suppe | ein gutes Brot | keine guten Weine |
| Dat. | einem guten Wein | einer guten Suppe | einem guten Brot | keinen guten Weinen |

**Prinzip:** Wenn der Artikel keine eindeutige Genus-Endung hat (z.B. *ein* maskulin/neutral), übernimmt das Adjektiv die starke Endung (-er, -es). Wenn der Artikel eine klare Endung hat (z.B. *eine* feminin), bleibt das Adjektiv schwach (-e, -en).""",
        structure="ein/eine/kein/mein + Adjektiv + passende Endung + Nomen",
        rules=[
            'Nach "ein" (maskulin Nom.) steht das Adjektiv mit -er: ein guter Wein.',
            'Nach "ein" (neutral Nom./Akk.) steht das Adjektiv mit -es: ein schönes Haus.',
            'Nach "eine" (feminin Nom./Akk.) bleibt es bei -e: eine nette Frau.',
            'Akkusativ maskulin ("einen") und alle Dativ-Formen verwenden -en.',
            "Die gleichen Regeln gelten für keinen und alle Possessivartikel.",
        ],
        examples=[
            GrammarExample(
                text="Das ist ein interessantes Buch.",
                translation=None,
                note="neutral Nom.: -es",
            ),
            GrammarExample(
                text="Ich habe einen neuen Computer.",
                translation=None,
                note="maskulin Akk.: -en",
            ),
            GrammarExample(
                text="Sie wohnt in einer kleinen Wohnung.",
                translation=None,
                note="feminin Dat.: -en",
            ),
            GrammarExample(
                text="Mein alter Freund wohnt in Berlin.",
                translation=None,
                note="Possessivartikel: -er",
            ),
            GrammarExample(
                text="Kein gutes Restaurant hat heute geöffnet.",
                translation=None,
                note="kein neutral: -es",
            ),
            GrammarExample(
                text="Er fährt mit seinem neuen Auto.",
                translation=None,
                note="Dat. neutral: -en",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Das ist ein interessantes Buch. (korrekt) / Das ist ein interessante Buch. (falsch)",
                correct="Das ist ein interessantes Buch.",
                note='"Buch" ist neutral. Nach "ein" im Nominativ neutral: Adjektivendung -es.',
            ),
            GrammarMistake(
                wrong="Ich habe ein neuer Computer.",
                correct="Ich habe einen neuen Computer.",
                note='Akkusativ maskulin: "einen" + Adjektiv auf -en.',
            ),
        ],
        related=[
            "adjektivdeklination-best",
            "adjektivdeklination-null",
            "akkusativ",
            "possessivartikel",
            "unbestimmte-artikel",
        ],
    ),
    GrammarTopic(
        slug="adjektivdeklination-null",
        title="Adjektivdeklination ohne Artikel",
        level="A2",
        category="Adjektive",
        summary="Adjektivdeklination ohne Artikel – die starke Deklination.",
        explanation="""Wenn das Adjektiv **ohne Artikel** vor einem Nomen steht, übernimmt es die **starke Deklination**. Die starken Endungen sind fast identisch mit den bestimmten Artikeln:

| Fall | maskulin | feminin | neutral | Plural |
|------|----------|---------|---------|--------|
| Nom. | guter Wein | gute Suppe | gutes Brot | gute Weine |
| Akk. | guten Wein | gute Suppe | gutes Brot | gute Weine |
| Dat. | gutem Wein | guter Suppe | gutem Brot | guten Weinen |

**Wann ohne Artikel?** Plural ohne Artikel (*Gute Bücher sind teuer.*), unzählbare Nomen (*Kaltes Wasser.*), nach Mengenangaben (*viel frisches Obst*), nach Zahlen (*drei kleine Kinder*).

Nach **viel, wenig, etwas, nichts** nominalisiert und **großgeschrieben**: *etwas Neues, nichts Besonderes*.""",
        structure="Kein Artikel + Adjektiv (starke Endung) + Nomen",
        rules=[
            "Ohne Artikel übernimmt das Adjektiv die Rolle des Artikels und zeigt Genus und Fall an.",
            "Die starken Endungen entsprechen weitgehend den bestimmten Artikeln (der → -er, die → -e, das → -es).",
            'Nach "viel", "wenig", "etwas", "nichts" wird das Adjektiv nominalisiert und großgeschrieben.',
            'Nach Zahlen steht das Adjektiv ohne Artikel: "drei kleine Kinder".',
            'Bei unzählbaren Nomen im Singular ohne Artikel: "kaltes Wasser, guter Kaffee".',
        ],
        examples=[
            GrammarExample(
                text="Guter Wein ist teuer.",
                translation=None,
                note="maskulin Nominativ: -er",
            ),
            GrammarExample(
                text="Ich trinke gern kaltes Bier.",
                translation=None,
                note="neutral Akkusativ: -es",
            ),
            GrammarExample(
                text="Sie hat große blaue Augen.",
                translation=None,
                note="Plural Akkusativ: -e",
            ),
            GrammarExample(
                text="Mit großem Interesse habe ich den Vortrag gehört.",
                translation=None,
                note="Dativ neutral: -em",
            ),
            GrammarExample(
                text="Viele junge Leute wohnen in dieser Gegend.",
                translation=None,
                note="nach viele, Plural: -e",
            ),
            GrammarExample(
                text="Hast du etwas Neues gehört?",
                translation=None,
                note="Nominalisierung: großgeschrieben",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Gut Wein ist teuer.",
                correct="Guter Wein ist teuer.",
                note="Ohne Artikel muss das Adjektiv die starke Endung bekommen: guter Wein.",
            ),
            GrammarMistake(
                wrong="Ich habe etwas altes gefunden.",
                correct="Ich habe etwas Altes gefunden.",
                note='Nach "etwas" wird das Adjektiv nominalisiert und großgeschrieben.',
            ),
        ],
        related=[
            "adjektivdeklination-best",
            "adjektivdeklination-unbest",
            "adjektive",
            "genus",
        ],
    ),
    GrammarTopic(
        slug="nebensatz-dass",
        title='Nebensätze mit "dass"',
        level="A2",
        category="Syntax",
        summary='Nebensätze mit "dass" – Wortstellung und Zeichensetzung.',
        explanation="""Nebensätze mit **dass** (that) sind die häufigste Art von Nebensätzen. Im **dass-Satz** steht das konjugierte Verb **am Ende**: *Ich weiß, **dass** er heute kommt.*

⚠️ Vor dem **dass** steht immer ein **Komma**!

Typische Verben mit dass-Satz: wissen, sagen, glauben, denken, finden, meinen, hoffen, verstehen, hören, sehen.

**dass vs das:**
- **dass** (Konjunktion, mit ß) = that
- **das** (Artikel/Pronomen, mit einem s) = the / which
*Ich weiß, **dass** das Auto kaputt ist.*""",
        structure="Hauptsatz, dass + Subjekt + ... + Verb (am Ende)",
        rules=[
            "Im dass-Satz steht das konjugierte Verb am Ende.",
            'Vor "dass" steht immer ein Komma.',
            '"Dass" leitet einen Nebensatz ein und bedeutet "that".',
            '"Dass" (mit ß) ist die Konjunktion; "das" ist Artikel oder Relativpronomen.',
            "Der dass-Satz kann das Subjekt oder Objekt des Hauptsatzes sein.",
        ],
        examples=[
            GrammarExample(text="Ich weiß, dass du recht hast.", translation=None),
            GrammarExample(
                text="Sie sagt, dass sie keine Zeit hat.",
                translation=None,
            ),
            GrammarExample(
                text="Ich hoffe, dass es morgen schönes Wetter gibt.",
                translation=None,
            ),
            GrammarExample(
                text="Es ist wichtig, dass du genug schläfst.",
                translation=None,
            ),
            GrammarExample(
                text="Er glaubt, dass der Test einfach ist.",
                translation=None,
            ),
            GrammarExample(
                text="Ich finde, dass dieser Film sehr interessant ist.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich weiß, dass er kommt heute.",
                correct="Ich weiß, dass er heute kommt.",
                note="Im dass-Satz muss das konjugierte Verb am Ende stehen.",
            ),
            GrammarMistake(
                wrong="Ich weiß, das du recht hast.",
                correct="Ich weiß, dass du recht hast.",
                note='Die Konjunktion wird mit "ss/ß" geschrieben: "dass". "Das" ist der Artikel.',
            ),
        ],
        related=["nebensatz-weil", "wortstellung-nebensatz", "nebensatz-wenn"],
    ),
    GrammarTopic(
        slug="nebensatz-weil",
        title='Nebensätze mit "weil"',
        level="A2",
        category="Syntax",
        summary='Nebensätze mit "weil" – Grund/Ursache ausdrücken.',
        explanation="""Nebensätze mit **weil** drücken einen Grund oder eine Ursache aus. Im **weil-Satz** steht das konjugierte Verb **am Ende**: *Ich bleibe zu Hause, **weil** ich krank **bin**.*

**Typische Fragen:** Warum? Wieso?
*Warum lernst du Deutsch? — Weil ich in Berlin arbeiten möchte.*

⚠️ Umgangssprachlich hört man manchmal Hauptsatz-Wortstellung nach *weil* (*weil ich habe geschlafen*). In formellen Kontexten und Prüfungen muss das Verb am Ende stehen!

**weil vs denn:** *denn* leitet einen Hauptsatz ein (Verb an Position 2): *Ich bleibe zu Hause, denn ich bin krank.*""",
        structure="Hauptsatz, weil + Subjekt + ... + Verb (am Ende)",
        rules=[
            "Im weil-Satz steht das konjugierte Verb am Ende.",
            'Weil antwortet auf die Frage "Warum?" / "Wieso?".',
            'In formellem und schriftlichem Deutsch steht das Verb nach "weil" immer am Ende.',
            'Umgangssprachlich hört man manchmal Hauptsatz-Wortstellung nach "weil" — vermeide das in Prüfungen.',
            '"Denn" ist eine Alternative mit Hauptsatz-Wortstellung: "Ich bleibe zu Hause, denn ich bin krank."',
        ],
        examples=[
            GrammarExample(
                text="Ich lerne Deutsch, weil ich in Berlin studieren möchte.",
                translation=None,
            ),
            GrammarExample(
                text="Er kommt zu spät, weil sein Bus Verspätung hat.",
                translation=None,
            ),
            GrammarExample(
                text="Wir können nicht kommen, weil wir arbeiten müssen.",
                translation=None,
            ),
            GrammarExample(
                text="Sie ist glücklich, weil sie die Prüfung bestanden hat.",
                translation=None,
            ),
            GrammarExample(
                text="Ich bleibe im Bett, weil ich krank bin.",
                translation=None,
            ),
            GrammarExample(
                text="Warum trinkst du keinen Kaffee? — Weil ich lieber Tee mag.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich bleibe zu Hause, weil ich bin krank.",
                correct="Ich bleibe zu Hause, weil ich krank bin.",
                note='Nach "weil" steht das Verb am Satzende.',
            ),
            GrammarMistake(
                wrong="Ich bleibe zu Hause, weil krank.",
                correct="Ich bleibe zu Hause, weil ich krank bin.",
                note="Der weil-Satz braucht ein Subjekt und ein Verb, genau wie ein vollständiger Satz.",
            ),
        ],
        related=["nebensatz-dass", "wortstellung-nebensatz", "nebensatz-wenn"],
    ),
    GrammarTopic(
        slug="nebensatz-wenn",
        title='Nebensätze mit "wenn"',
        level="A2",
        category="Syntax",
        summary='Nebensätze mit "wenn" – Bedingung (falls) und Zeit (immer wenn).',
        explanation="""**Wenn** kann zwei verschiedene Bedeutungen haben:

1. Konditional (if): *Wenn es morgen regnet, bleiben wir zu Hause.*
2. Temporal — wiederholt (whenever): *(Immer) wenn ich Zeit habe, lese ich ein Buch.*

Im **wenn-Satz** steht das konjugierte Verb **am Ende**. Steht der wenn-Satz vorne, beginnt der Hauptsatz mit dem konjugierten Verb: *Wenn ich Zeit habe, **lese** ich ein Buch.*

**wenn vs als:** als = einmaliges Ereignis in der Vergangenheit (*Als ich ein Kind war...*), wenn = wiederholtes Ereignis oder Zukunft (*Wenn ich in Berlin bin...*)

**wenn vs ob:** ob = indirekte Frage (whether) — *Ich weiß nicht, ob er kommt.*""",
        structure="Wenn + Subjekt + ... + Verb (am Ende), Hauptsatz",
        rules=[
            "Im wenn-Satz steht das konjugierte Verb am Ende.",
            '"Wenn" kann "if" (konditional) oder "whenever" (temporal wiederholt) bedeuten.',
            "Steht der wenn-Satz vorne, beginnt der Hauptsatz mit dem konjugierten Verb.",
            '"Wenn" ≠ "als": "als" für einmalige Vergangenheit, "wenn" für Wiederholung/Zukunft.',
            'Ob ≠ wenn: "ob" leitet indirekte Fragen ein, "wenn" leitet Bedingungen oder Zeitsätze ein.',
        ],
        examples=[
            GrammarExample(
                text="Wenn es regnet, bleibe ich zu Hause.",
                translation=None,
                note="konditional",
            ),
            GrammarExample(
                text="Immer wenn ich Kaffee trinke, werde ich wach.",
                translation=None,
                note="temporal",
            ),
            GrammarExample(
                text="Ich freue mich, wenn du kommst.",
                translation=None,
            ),
            GrammarExample(
                text="Wenn du Hilfe brauchst, ruf mich an.",
                translation=None,
            ),
            GrammarExample(
                text="Weißt du, ob er heute kommt?",
                translation=None,
                note="ob, nicht wenn",
            ),
            GrammarExample(
                text="Als ich klein war, wohnte ich auf dem Land.",
                translation=None,
                note="als, nicht wenn — einmalige Vergangenheit",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wenn ich habe Zeit, lese ich.",
                correct="Wenn ich Zeit habe, lese ich.",
                note='Das Verb im Nebensatz steht am Ende: "Zeit habe".',
            ),
            GrammarMistake(
                wrong="Als ich nach Hause komme, koche ich.",
                correct="Wenn ich nach Hause komme, koche ich.",
                note='"Als" nur für Vergangenheit. Für Gegenwart/Gewohnheit: "wenn".',
            ),
        ],
        related=["nebensatz-dass", "nebensatz-weil", "wortstellung-nebensatz"],
    ),
    GrammarTopic(
        slug="nebensatz-obwohl",
        title='Nebensätze mit "obwohl"',
        level="A2",
        category="Syntax",
        summary='Nebensätze mit "obwohl" – Einräumung/Konzession ausdrücken.',
        explanation="""Nebensätze mit **obwohl** drücken einen **Gegensatz** oder eine **Einschränkung** aus (although, even though). Im **obwohl-Satz** steht das konjugierte Verb **am Ende**: *Er kommt, **obwohl** er krank **ist**.*

Steht der obwohl-Satz vorne, beginnt der Hauptsatz mit dem Verb: *Obwohl es regnet, **gehe** ich spazieren.*

**obwohl vs trotzdem:**
- obwohl + Nebensatz (Verb am Ende): *Obwohl es regnet, gehe ich raus.*
- trotzdem + Hauptsatz (Verb an Position 2): *Es regnet. Trotzdem gehe ich raus.*""",
        structure="Obwohl + Subjekt + ... + Verb (am Ende), Hauptsatz (Verb an Position 1)",
        rules=[
            "Im obwohl-Satz steht das konjugierte Verb am Ende.",
            '"Obwohl" leitet einen Konzessivsatz ein und bedeutet "although".',
            'Vor "obwohl" steht immer ein Komma.',
            "Ist der Nebensatz vorne, fängt der Hauptsatz mit dem Verb an.",
            '"Obwohl" und "trotzdem" haben ähnliche Bedeutung, aber andere Satzstellung.',
        ],
        examples=[
            GrammarExample(
                text="Er geht zur Arbeit, obwohl er krank ist.",
                translation=None,
            ),
            GrammarExample(
                text="Obwohl es regnet, gehen wir spazieren.",
                translation=None,
            ),
            GrammarExample(
                text="Sie hat die Prüfung bestanden, obwohl sie wenig gelernt hat.",
                translation=None,
            ),
            GrammarExample(
                text="Obwohl das Restaurant teuer ist, ist es immer voll.",
                translation=None,
            ),
            GrammarExample(
                text="Ich mag ihn, obwohl er manchmal nervig ist.",
                translation=None,
            ),
            GrammarExample(
                text="Obwohl ich müde bin, kann ich nicht schlafen.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Obwohl es regnet, ich bleibe zu Hause.",
                correct="Obwohl es regnet, bleibe ich zu Hause.",
                note="Wenn der Nebensatz vorne steht, beginnt der Hauptsatz mit dem Verb: bleibe ich.",
            ),
            GrammarMistake(
                wrong="Obwohl er ist krank, geht er arbeiten.",
                correct="Obwohl er krank ist, geht er arbeiten.",
                note='Im obwohl-Satz steht das Verb am Ende: "krank ist".',
            ),
        ],
        related=[
            "nebensatz-weil",
            "nebensatz-dass",
            "wortstellung-nebensatz",
            "nebensatz-wenn",
        ],
    ),
    GrammarTopic(
        slug="wortstellung-nebensatz",
        title="Wortstellung im Nebensatz",
        level="A2",
        category="Syntax",
        summary="Wortstellung im Nebensatz – Verb am Ende, die Klammerstruktur.",
        explanation="""Die **Wortstellung im Nebensatz** ist eine der wichtigsten Regeln im Deutschen: **Das konjugierte Verb steht am Ende.**

Nebensatz-Einleiter: dass, weil, wenn, obwohl, als, bevor, nachdem, während, seitdem, bis, damit, ob, sodass, falls, da

Perfekt im Nebensatz: Partizip II + Hilfsverb am Schluss — *Ich weiß, dass er gestern ins Kino **gegangen ist**.*

Trennbare Verben im Nebensatz: werden **nicht getrennt** — *Ich weiß, dass er um 7 Uhr **aufsteht**.*

Hauptsatz nach Nebensatz: Verb an Position 1 — *Weil ich krank bin, **bleibe** ich zu Hause.*""",
        structure="Subjunktion + Subjekt + ... + Verb (am Ende) / Perfekt: ... Partizip II + Hilfsverb (am Ende)",
        rules=[
            "Im Nebensatz steht das konjugierte Verb immer am Ende.",
            "Im Nebensatz mit Perfekt: Partizip II + Hilfsverb am Schluss.",
            'Trennbare Verben werden im Nebensatz nicht getrennt: "aufsteht", nicht "steht auf".',
            "Wenn der Nebensatz vorne steht, beginnt der Hauptsatz mit dem Verb.",
            "Zwei Verben am Ende: Modalverb/Hilfsverb steht hinter dem Infinitiv/Partizip.",
        ],
        examples=[
            GrammarExample(
                text="Ich bleibe zu Hause, weil ich krank bin.",
                translation=None,
            ),
            GrammarExample(
                text="Ich weiß, dass er gestern ins Kino gegangen ist.",
                translation=None,
                note="Perfekt: gegangen ist",
            ),
            GrammarExample(
                text="Sie sagt, dass sie um 7 Uhr aufsteht.",
                translation=None,
                note="trennbares Verb: aufsteht (nicht getrennt)",
            ),
            GrammarExample(
                text="Weil ich krank bin, bleibe ich zu Hause.",
                translation=None,
                note="Nebensatz vorne, Hauptsatz Verb vor Subjekt",
            ),
            GrammarExample(
                text="Ich hoffe, dass du morgen kommen kannst.",
                translation=None,
                note="Modalverb: kommen kannst",
            ),
            GrammarExample(
                text="Er fragt, ob wir mitkommen wollen.",
                translation=None,
                note="ob + Verb am Ende",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich weiß, dass er ist krank.",
                correct="Ich weiß, dass er krank ist.",
                note="Im Nebensatz steht das konjugierte Verb (ist) am Ende.",
            ),
            GrammarMistake(
                wrong="Ich weiß, dass er steht um 7 Uhr auf.",
                correct="Ich weiß, dass er um 7 Uhr aufsteht.",
                note="Trennbare Verben werden im Nebensatz nicht getrennt.",
            ),
        ],
        related=[
            "nebensatz-dass",
            "nebensatz-weil",
            "nebensatz-wenn",
            "nebensatz-obwohl",
            "trennbare-verben",
        ],
    ),
    GrammarTopic(
        slug="relativsaetze",
        title="Relativsätze",
        level="A2",
        category="Syntax",
        summary="Relativsätze im Nominativ und Akkusativ – der, die, das als Relativpronomen.",
        explanation="""**Relativsätze** geben zusätzliche Informationen über ein Nomen. Sie werden mit **Relativpronomen** (der, die, das) eingeleitet.

| Genus | Nominativ | Akkusativ |
|-------|-----------|-----------|
| maskulin | der | den |
| feminin | die | die |
| neutral | das | das |
| Plural | die | die |

Das Verb steht im Relativsatz am Ende: *Der Mann, der Deutsch **lernt**, ist nett.*

**Genus und Numerus** kommen vom Bezugswort. **Kasus** kommt aus der Funktion im Relativsatz: *Der Mann, **der** (Nom.) hier wohnt...* vs *Der Mann, **den** (Akk.) ich sehe...*

Vor dem Relativpronomen steht immer ein Komma.""",
        structure="Bezugswort, Relativpronomen (der/die/das) + ... + Verb (am Ende)",
        rules=[
            "Das Relativpronomen richtet sich in Genus und Numerus nach dem Bezugswort.",
            "Der Kasus des Relativpronomens hängt von seiner Funktion im Relativsatz ab.",
            "Das Verb steht im Relativsatz am Ende.",
            "Vor dem Relativpronomen steht immer ein Komma.",
            'Akkusativ maskulin: "den" (Der Film, den ich gesehen habe).',
        ],
        examples=[
            GrammarExample(
                text="Der Mann, der dort steht, ist mein Onkel.",
                translation=None,
                note="Nominativ maskulin",
            ),
            GrammarExample(
                text="Der Film, den wir gestern gesehen haben, war super.",
                translation=None,
                note="Akkusativ maskulin",
            ),
            GrammarExample(
                text="Die Frau, die hier wohnt, ist sehr nett.",
                translation=None,
                note="Nominativ feminin",
            ),
            GrammarExample(
                text="Das Buch, das auf dem Tisch liegt, gehört mir.",
                translation=None,
                note="Nominativ neutral",
            ),
            GrammarExample(
                text="Die Kinder, die im Garten spielen, sind meine Neffen.",
                translation=None,
                note="Nominativ Plural",
            ),
            GrammarExample(
                text="Kennst du den Mann, den Petra geheiratet hat?",
                translation=None,
                note="Akkusativ maskulin",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Der Film, der wir gesehen haben, ist gut.",
                correct="Der Film, den wir gesehen haben, ist gut.",
                note="Der Film ist das direkte Objekt des Relativsatzes → Akkusativ: den.",
            ),
            GrammarMistake(
                wrong="Das Buch, das ich lese es, ist spannend.",
                correct="Das Buch, das ich lese, ist spannend.",
                note="Im Relativsatz wird das Bezugswort nicht durch ein Pronomen wiederholt.",
            ),
        ],
        related=["wortstellung-nebensatz", "akkusativ", "bestimmte-artikel"],
    ),
    GrammarTopic(
        slug="indirekte-fragen",
        title="Indirekte Fragesätze",
        level="A2",
        category="Syntax",
        summary="Indirekte Fragen – ob (bei Ja/Nein-Fragen) und Fragewörter im Nebensatz.",
        explanation="""**Indirekte Fragesätze** geben eine Frage wieder, ohne das Fragezeichen und die direkte Satzstellung.

**Direkte vs indirekte Frage:**
- Direkt: *Wo wohnt er?* → Indirekt: *Ich weiß nicht, **wo er wohnt**.*
- Direkt: *Kommt er?* → Indirekt: *Ich weiß nicht, **ob er kommt**.*

Ja/Nein-Fragen → **ob** / W-Fragen → **Fragewort** (wo, wie, wann, was, wer...)

Das konjugierte Verb steht am Ende: *Kannst du mir sagen, **wo die Bank ist**?*""",
        structure="Einleitung + ob/Fragewort + Subjekt + ... + Verb (am Ende)",
        rules=[
            'Ja/Nein-Fragen werden indirekt mit "ob" eingeleitet.',
            "W-Fragen werden indirekt mit dem Fragewort eingeleitet.",
            "Das konjugierte Verb steht im indirekten Fragesatz am Ende.",
            '"Ob" bedeutet "whether/if" und steht ohne dass.',
            "Vor dem indirekten Fragesatz steht immer ein Komma.",
        ],
        examples=[
            GrammarExample(text="Ich weiß nicht, wo er wohnt.", translation=None),
            GrammarExample(
                text="Weißt du, ob der Supermarkt noch geöffnet ist?",
                translation=None,
            ),
            GrammarExample(
                text="Kannst du mir sagen, wie spät es ist?",
                translation=None,
            ),
            GrammarExample(
                text="Ich frage mich, warum er nicht geantwortet hat.",
                translation=None,
            ),
            GrammarExample(
                text="Sie möchte wissen, wann der nächste Zug fährt.",
                translation=None,
            ),
            GrammarExample(
                text="Hast du eine Ahnung, ob das Konzert morgen stattfindet?",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich weiß nicht, wo wohnt er.",
                correct="Ich weiß nicht, wo er wohnt.",
                note="In der indirekten Frage steht das Verb am Ende (Nebensatz-Wortstellung).",
            ),
            GrammarMistake(
                wrong="Ich weiß nicht, ob dass er kommt.",
                correct="Ich weiß nicht, ob er kommt.",
                note='"Ob" oder "dass", nicht beides gleichzeitig. "Ob" = indirekte Frage, "dass" = Fakt.',
            ),
        ],
        related=["nebensatz-dass", "wortstellung-nebensatz", "relativsaetze"],
    ),
]
