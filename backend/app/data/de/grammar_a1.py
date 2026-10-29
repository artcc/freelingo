"""German grammar topics — A1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="verb-sein",
        title='Das Verb "sein"',
        level="A1",
        category="Verben",
        summary='Das Verb "sein" – Konjugation und Grundverwendung für Identität, Herkunft und Eigenschaften.',
        explanation="""Das Verb **sein** ist das wichtigste Verb im Deutschen. Es bedeutet *to be* und wird für Identität, Herkunft, Eigenschaften und Zustände verwendet.

**Konjugation:**

| Person | Form |
|--------|------|
| ich | bin |
| du | bist |
| er/sie/es | ist |
| wir | sind |
| ihr | seid |
| sie/Sie | sind |

**Verwendung:**

- **Identität**: *Ich bin Anna.*
- **Nationalität / Herkunft**: *Er ist Deutscher. / Ich bin aus Spanien.*
- **Beruf**: *Sie ist Ärztin.*
- **Eigenschaften**: *Das Haus ist groß. / Mein Bruder ist nett.*
- **Befinden**: *Mir ist kalt. / Wie geht es dir? — Mir geht es gut.*

In vollständigen Aussagesätzen steht normalerweise ein Subjekt: *Ich bin müde.* Ein Subjektpronomen wird nicht allein deshalb weggelassen, weil die Verbform die Person erkennen lässt.""",
        structure="ich bin · du bist · er/sie/es ist · wir sind · ihr seid · sie/Sie sind",
        rules=[
            "In vollständigen Aussagesätzen braucht man normalerweise ein Subjekt, zum Beispiel ein Nomen oder ein Personalpronomen.",
            '"Sein" drückt Identität, Herkunft, Beruf, Alter, Eigenschaften und vorübergehende Zustände aus.',
            'Die Höflichkeitsform "Sie" wird immer großgeschrieben und gilt für Singular und Plural.',
            'In der Frage steht das Verb an erster Position: "Bist du müde?"',
            'Nationalitäten werden ohne Artikel verwendet: "Ich bin Spanier."',
        ],
        examples=[
            GrammarExample(text="Ich bin Student.", translation=None),
            GrammarExample(text="Bist du aus Berlin?", translation=None),
            GrammarExample(text="Wir sind müde.", translation=None, note="Zustand"),
            GrammarExample(text="Sie ist Lehrerin.", translation=None, note="Beruf"),
            GrammarExample(text="Seid ihr fertig?", translation=None),
            GrammarExample(text="Das Wetter ist schön.", translation=None, note="Eigenschaft"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich bin heiße Tom.",
                correct="Ich heiße Tom.",
                note='Für den Namen verwendet man entweder "Ich heiße Tom" oder "Ich bin Tom", nicht beide Verben zusammen.',
            ),
            GrammarMistake(
                wrong="Sind müde.",
                correct="Wir sind müde.",
                note="Im Deutschen darf das Subjektpronomen nicht fehlen.",
            ),
        ],
        related=["verb-haben", "personalpronomen", "verneinung"],
    ),
    GrammarTopic(
        slug="verb-haben",
        title='Das Verb "haben"',
        level="A1",
        category="Verben",
        summary='Das Verb "haben" – Konjugation und Verwendung für Besitz, Beziehungen und feste Ausdrücke.',
        explanation="""Das Verb **haben** ist nach *sein* das zweitwichtigste Verb im Deutschen.

**Konjugation:**

| Person | Form |
|--------|------|
| ich | habe |
| du | hast |
| er/sie/es | hat |
| wir | haben |
| ihr | habt |
| sie/Sie | haben |

**Verwendung:**

- **Besitz**: *Ich habe ein Auto.*
- **Familie**: *Ich habe zwei Kinder.*
- **Gefühle / körperliche Zustände**: *Ich habe Hunger. / Ich habe Kopfschmerzen.*
- **Termine / Verpflichtungen**: *Ich habe heute einen Termin.*
- **Ausdrücke mit Akkusativ**: *Ich habe Zeit / Glück / Pech / Lust / Angst.*

Für das Alter verwendet man **sein**, nicht *haben*: *Ich bin 25 Jahre alt.*

**Wichtig**: *Haben* verlangt den **Akkusativ**: *Ich habe einen Hund.*""",
        structure="ich habe · du hast · er/sie/es hat · wir haben · ihr habt · sie/Sie haben",
        rules=[
            "Haben ist ein unregelmäßiges Verb. Die Formen hast und hat weichen vom Stamm ab.",
            "Haben + Akkusativ: Das direkte Objekt steht immer im Akkusativ.",
            'Für das Alter verwendet man "sein", nicht "haben": "Ich bin 30 Jahre alt."',
            'Viele feste Ausdrücke verwenden "haben": "Hunger haben, Durst haben, Zeit haben, Recht haben".',
            'In der gesprochenen Sprache wird "haben" oft als Hilfsverb für das Perfekt verwendet.',
        ],
        examples=[
            GrammarExample(text="Ich habe einen Bruder.", translation=None),
            GrammarExample(text="Hast du Zeit?", translation=None),
            GrammarExample(text="Er hat Hunger.", translation=None, note="Ausdruck"),
            GrammarExample(text="Wir haben kein Geld.", translation=None),
            GrammarExample(text="Habt ihr Kinder?", translation=None),
            GrammarExample(
                text="Sie hat Geburtstag.",
                translation=None,
                note="feststehender Ausdruck",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich habe 25 Jahre.",
                correct="Ich bin 25 Jahre alt.",
                note='Im Deutschen verwendet man "sein" für das Alter, nicht "haben".',
            ),
            GrammarMistake(
                wrong="Ich habe kalt.",
                correct="Mir ist kalt. / Ich friere.",
                note='Kalt haben gibt es nicht. "Mir ist kalt" oder "Ich friere" sind korrekt.',
            ),
        ],
        related=["verb-sein", "akkusativ", "personalpronomen"],
    ),
    GrammarTopic(
        slug="personalpronomen",
        title="Personalpronomen",
        level="A1",
        category="Pronomen",
        summary="Personalpronomen im Nominativ (ich, du, er, sie, es, wir, ihr, sie, Sie).",
        explanation="""Die **Personalpronomen im Nominativ** ersetzen das Subjekt im Satz.

| Person | Singular | Plural |
|--------|----------|--------|
| 1. Person | ich | wir |
| 2. Person (informell) | du | ihr |
| 2. Person (formell) | Sie | Sie |
| 3. Person maskulin | er | sie |
| 3. Person feminin | sie | sie |
| 3. Person neutral | es | sie |

**Wichtige Regeln:**

1. Das Pronomen richtet sich im **Geschlecht** nach dem Nomen, das es ersetzt: *Der Tisch → er. Die Lampe → sie. Das Buch → es.*
2. **Sie** (formell) wird **immer großgeschrieben**, Singular und Plural sind gleich.
3. **du** und **ihr** sind informell und werden für Freunde, Familie und Kinder verwendet.
4. **ihr** ist das informelle Plural-Pronomen der 2. Person.
5. Im Deutschen **muss** das Personalpronomen im Satz stehen — es kann nicht weggelassen werden.""",
        structure="ich · du · er/sie/es · wir · ihr · sie/Sie",
        rules=[
            "Das Personalpronomen muss immer stehen, anders als im Spanischen oder Italienischen.",
            'Das Genus entscheidet über das Pronomen in der 3. Person: "der → er, die → sie, das → es".',
            '"Sie" (Höflichkeitsform) wird immer großgeschrieben.',
            '"ihr" ist die informelle 2. Person Plural (Freunde, Familie).',
            'Im Plural gibt es nur ein Pronomen für alle drei Genera: "sie".',
        ],
        examples=[
            GrammarExample(text="Ich komme aus Spanien.", translation=None),
            GrammarExample(text="Wo wohnst du?", translation=None),
            GrammarExample(text="Er ist mein Freund.", translation=None),
            GrammarExample(text="Wir gehen ins Kino.", translation=None),
            GrammarExample(text="Kommt ihr mit?", translation=None, note="informell"),
            GrammarExample(text="Woher kommen Sie?", translation=None, note="formell"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Wo wohnen?",
                correct="Wo wohnst du?",
                note="Im Deutschen muss das Personalpronomen immer stehen.",
            ),
            GrammarMistake(
                wrong="Der Tisch ist alt. Sie ist kaputt.",
                correct="Der Tisch ist alt. Er ist kaputt.",
                note='Der Tisch = maskulin → Pronomen "er", nicht "sie".',
            ),
        ],
        related=["verb-sein", "verb-haben", "bestimmte-artikel"],
    ),
    GrammarTopic(
        slug="bestimmte-artikel",
        title="Bestimmte Artikel",
        level="A1",
        category="Artikel",
        summary="Bestimmte Artikel der, die, das – Genus und Artikelkongruenz im Nominativ.",
        explanation="""Im Deutschen hat jedes Nomen ein **Genus** (Geschlecht): maskulin, feminin oder neutral. Der **bestimmte Artikel** (definite article) zeigt dieses Genus an.

| Genus | Singular | Plural |
|-------|----------|--------|
| maskulin | **der** | die |
| feminin | **die** | die |
| neutral | **das** | die |

**Achtung**: Im Plural gibt es nur **einen** Artikel: **die** für alle drei Genera.

**Verwendung:**

- Der bestimmte Artikel wird verwendet, wenn das Nomen **bekannt** oder **eindeutig** ist.
- *Der Mann dort ist mein Vater.*
- *Die Sonne scheint.* (es gibt nur eine)
- *Das Buch auf dem Tisch gehört mir.*

**Merksatz**: *Im Plural alles die!*""",
        structure="der (m) · die (f) · das (n) · die (Pl.)",
        rules=[
            "Jedes deutsche Nomen hat ein Genus: maskulin (der), feminin (die) oder neutral (das).",
            "Das Genus muss für jedes neue Nomen mitgelernt werden.",
            'Im Plural verwenden alle Nomina den Artikel "die".',
            'Es gibt einige Regeln für Genus: z.B. "-chen" und "-lein" sind immer neutral (das Mädchen).',
            "Der bestimmte Artikel zeigt an, dass etwas Bekanntes oder Bestimmtes gemeint ist.",
        ],
        examples=[
            GrammarExample(text="Der Hund ist braun.", translation=None),
            GrammarExample(text="Die Katze schläft.", translation=None),
            GrammarExample(text="Das Kind spielt.", translation=None),
            GrammarExample(text="Die Bücher sind neu.", translation=None, note="Plural"),
            GrammarExample(text="Der Tisch ist aus Holz.", translation=None),
            GrammarExample(text="Die Stadt ist schön.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Die Auto ist schnell.",
                correct="Das Auto ist schnell.",
                note="Auto ist neutral (das), nicht feminin.",
            ),
            GrammarMistake(
                wrong="Der Kinder spielen.",
                correct="Die Kinder spielen.",
                note='Im Plural steht immer "die".',
            ),
        ],
        related=["genus", "unbestimmte-artikel", "personalpronomen"],
    ),
    GrammarTopic(
        slug="genus",
        title="Das Genus der Substantive",
        level="A1",
        category="Nomen",
        summary="Das grammatische Genus im Deutschen – hilfreiche Muster und Regeln für der, die, das.",
        explanation="""Das Genus (Geschlecht) eines Nomens zu wissen ist essentiell, denn es bestimmt den Artikel und die Adjektivdeklination. Hier sind die wichtigsten **Regeln und Signale**:

### Typische Endungen für **der** (maskulin):
- **-er**: der Lehrer, der Computer
- **-ich**: der Teppich
- **-ling**: der Schmetterling, der Frühling
- **-ismus**: der Tourismus
- **Tageszeiten, Wochentage, Monate, Jahreszeiten**: der Morgen, der Montag, der Januar, der Sommer
- **Himmelsrichtungen**: der Norden, der Süden

### Typische Endungen für **die** (feminin):
- **-ung**: die Wohnung, die Zeitung
- **-heit/-keit**: die Freiheit, die Möglichkeit
- **-schaft**: die Freundschaft
- **-tion**: die Information
- **-tät**: die Universität
- **-e**: die Lampe, die Tasche (sehr viele, aber nicht alle!)

### Typische Endungen für **das** (neutral):
- **-chen/-lein** (Verkleinerungsform): das Mädchen, das Tischlein
- **-ment**: das Instrument
- **-um**: das Museum
- **-ma**: das Thema
- **Substantivierte Infinitive**: das Essen, das Trinken

⚠️ Lerne jedes Nomen immer mit Artikel (der Tisch, die Lampe, das Buch). Substantive werden im Deutschen **immer großgeschrieben**.""",
        structure="Genus-Signale: Endungen und Bedeutungsgruppen",
        rules=[
            'Substantive auf "-ung", "-heit", "-keit", "-schaft", "-tion", "-tät" sind immer feminin (die).',
            'Substantive auf "-chen" und "-lein" sind immer neutral (das).',
            'Substantive auf "-er", "-ling", "-ismus" und männliche Personen sind meist maskulin (der).',
            "Substantivierte Verben (das Essen, das Lesen) sind immer neutral.",
            "Lerne jedes Nomen immer mit Artikel (der Tisch, die Lampe, das Buch).",
            "Substantive werden im Deutschen **immer großgeschrieben**.",
        ],
        examples=[
            GrammarExample(
                text="der Lehrer → die Lehrerin",
                translation=None,
                note="Beruf mit -er = maskulin",
            ),
            GrammarExample(text="die Freiheit", translation=None, note="Endung -heit = feminin"),
            GrammarExample(
                text="das Mädchen",
                translation=None,
                note="Verkleinerungsform -chen = neutral",
            ),
            GrammarExample(text="der Montag", translation=None, note="Wochentage = maskulin"),
            GrammarExample(text="die Universität", translation=None, note="Endung -tät = feminin"),
            GrammarExample(text="das Instrument", translation=None, note="Endung -ment = neutral"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="der Information",
                correct="die Information",
                note='Wörter auf "-tion" sind immer feminin.',
            ),
            GrammarMistake(
                wrong="die Mädchen",
                correct="das Mädchen",
                note="Mädchen ist trotz der weiblichen Bedeutung neutral (Verkleinerungsform -chen).",
            ),
        ],
        related=["bestimmte-artikel", "unbestimmte-artikel"],
    ),
    GrammarTopic(
        slug="unbestimmte-artikel",
        title="Unbestimmte Artikel",
        level="A1",
        category="Artikel",
        summary="Unbestimmte Artikel ein, eine – wann und wie man sie im Nominativ verwendet.",
        explanation="""Der **unbestimmte Artikel** (indefinite article) wird verwendet, wenn das Nomen **unbekannt**, **nicht spezifisch** oder **zum ersten Mal erwähnt** wird.

| Genus | Singular |
|-------|----------|
| maskulin | **ein** |
| feminin | **eine** |
| neutral | **ein** |

⚠️ Im Plural gibt es **keinen** unbestimmten Artikel: *Da sind Bücher.* (Es gibt nur den Nullartikel oder Mengenangaben wie *viele*, *einige*.)

**Vergleich:**
- *Der Hund bellt.* = Der bestimmte Hund (du weißt welcher)
- *Ein Hund bellt.* = Irgendein Hund (unbekannt)

**Verwendung:**
- **Erste Erwähnung**: *Ich habe ein neues Auto.*
- **Unbekanntes Objekt**: *Da steht ein Mann.*
- **Kategorie / Definition**: *Ein Löwe ist ein Tier.*
- **Nach 'es gibt'**: *Es gibt ein Problem.*""",
        structure="ein (m/n) · eine (f) · — (Pl.)",
        rules=[
            'Maskulin und neutral teilen sich die gleiche Form "ein" im Nominativ.',
            'Feminin verwendet "eine" im Nominativ.',
            "Im Plural gibt es keinen unbestimmten Artikel.",
            'Nach "es gibt" steht immer der unbestimmte Artikel (oder Nullartikel im Plural).',
            'Bei Berufen und Nationalitäten steht kein Artikel: "Ich bin Lehrer." (nicht: ein Lehrer)',
        ],
        examples=[
            GrammarExample(text="Das ist ein Tisch.", translation=None, note="maskulin"),
            GrammarExample(text="Ich habe eine Frage.", translation=None, note="feminin"),
            GrammarExample(text="Das ist ein Buch.", translation=None, note="neutral"),
            GrammarExample(text="Es gibt ein Problem.", translation=None),
            GrammarExample(
                text="Hier sind Stühle.",
                translation=None,
                note="Plural, kein Artikel",
            ),
            GrammarExample(text="Ein Hund ist ein Haustier.", translation=None, note="Kategorie"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich bin ein Lehrer.",
                correct="Ich bin Lehrer.",
                note="Bei Berufen, Nationalitäten und Religionen steht kein unbestimmter Artikel.",
            ),
            GrammarMistake(
                wrong="Da ist eine Männer.",
                correct="Da sind Männer.",
                note="Im Plural gibt es keinen unbestimmten Artikel. Stattdessen Nullartikel.",
            ),
        ],
        related=["bestimmte-artikel", "genus", "akkusativ", "es-gibt"],
    ),
    GrammarTopic(
        slug="possessivartikel",
        title="Possessivartikel",
        level="A1",
        category="Artikel",
        summary="Possessivartikel mein, dein, sein, ihr, unser, euer, Ihr – Nominativformen.",
        explanation="""**Possessivartikel** zeigen Besitz oder Zugehörigkeit an. Sie stehen vor dem Nomen und richten sich nach dem **Besitzer**.

| Besitzer | maskulin/neutral | feminin/Plural |
|----------|-------------------|----------------|
| ich | **mein** | **meine** |
| du | **dein** | **deine** |
| er/es | **sein** | **seine** |
| sie | **ihr** | **ihre** |
| wir | **unser** | **unsere** |
| ihr | **euer** | **eure** |
| sie/Sie | **ihr/Ihr** | **ihre/Ihre** |

**Wichtig:**
- **sein** = von ihm (er) oder von ihm (es): *Das ist sein Buch.*
- **ihr** = von ihr (sie Singular): *Das ist ihr Auto.*
- **Ihr** (groß) = von Ihnen (Sie, Höflichkeitsform): *Ist das Ihr Pass?*

Im **Nominativ** gilt: Maskulin & neutral Singular: **mein/dein/sein/unser/euer/ihr** / Feminin Singular & alle Plural: **meine/deine/seine/unsere/eure/ihre**""",
        structure="mein/dein/sein + Nomen (m/n) · meine/deine/seine + Nomen (f/Pl.)",
        rules=[
            "Der Possessivartikel richtet sich nach dem Besitzer, nicht nach dem besessenen Objekt.",
            "Im Nominativ: maskulin und neutral ohne -e, feminin und Plural mit -e.",
            '"sein" = gehört zu er/es; "ihr" = gehört zu sie (Sg.) oder sie (Pl.).',
            'Die Höflichkeitsform "Ihr/Ihre" wird immer großgeschrieben.',
            '"euer" verliert das mittlere -e- vor -e: "eure" (nicht: euere).',
        ],
        examples=[
            GrammarExample(text="Das ist mein Buch.", translation=None, note="neutral"),
            GrammarExample(text="Das ist meine Tasche.", translation=None, note="feminin"),
            GrammarExample(text="Sein Auto ist neu.", translation=None),
            GrammarExample(
                text="Unsere Kinder sind klein.",
                translation=None,
                note="Plural",
            ),
            GrammarExample(text="Ist das euer Hund?", translation=None, note="informell Plural"),
            GrammarExample(text="Wo ist Ihr Pass?", translation=None, note="formell"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Das ist sein Freundin.",
                correct="Das ist seine Freundin.",
                note='Freundin ist feminin → seine (mit -e). "Sein" ohne -e nur für maskulin/neutral.',
            ),
            GrammarMistake(
                wrong="Das ist euere Katze.",
                correct="Das ist eure Katze.",
                note='"Euer" verliert das -e- vor der Endung: eure, euren, eurem.',
            ),
        ],
        related=["personalpronomen", "bestimmte-artikel", "genus"],
    ),
    GrammarTopic(
        slug="adjektive",
        title="Adjektive",
        level="A1",
        category="Adjektive",
        summary="Grundlegende Adjektive im Deutschen – Stellung, häufige Adjektive und prädikativer Gebrauch.",
        explanation="""Adjektive beschreiben Eigenschaften von Personen oder Dingen.

**Prädikative Verwendung (nach sein):** Nach den Verben **sein**, **werden** und **bleiben** steht das Adjektiv **unverändert** (ohne Endung):
- *Das Haus ist **groß**.*
- *Der Kaffee ist **kalt**.*
- *Ich bin **müde**.*

**Häufige Adjektive A1:**

| Deutsch | Englisch |
|---------|----------|
| groß / klein | big / small |
| alt / neu / jung | old / new / young |
| gut / schlecht | good / bad |
| schön / hässlich | beautiful / ugly |
| teuer / billig | expensive / cheap |
| schnell / langsam | fast / slow |
| warm / kalt | warm / cold |
| lang / kurz | long / short |
| interessant / langweilig | interesting / boring |
| leicht / schwer | easy / heavy/difficult |

**Gegensatzpaare** sind eine gute Lernstrategie.""",
        structure="Subjekt + sein/werden/bleiben + Adjektiv (ohne Endung)",
        rules=[
            'Nach "sein", "werden" und "bleiben" bleibt das Adjektiv ohne Endung.',
            "Adjektive werden im Deutschen kleingeschrieben (anders als Substantive).",
            "Lerne Adjektive in Gegensatzpaaren: groß ↔ klein, alt ↔ neu.",
            "Vor dem Nomen bekommen Adjektive eine Endung (→ Adjektivdeklination, A2).",
        ],
        examples=[
            GrammarExample(text="Der Film ist interessant.", translation=None),
            GrammarExample(text="Mein Zimmer ist klein.", translation=None),
            GrammarExample(text="Die Suppe ist zu heiß.", translation=None),
            GrammarExample(text="Bist du müde?", translation=None),
            GrammarExample(text="Das ist zu teuer.", translation=None),
            GrammarExample(text="Deutsch ist nicht schwer.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Der Film ist interessante.",
                correct="Der Film ist interessant.",
                note="Nach 'sein' bleibt das Adjektiv ohne Endung.",
            ),
            GrammarMistake(
                wrong="Das ist ein groß Haus.",
                correct="Das ist ein großes Haus.",
                note="Vor dem Nomen braucht das Adjektiv eine Endung. Das ist die Adjektivdeklination (→ A2).",
            ),
        ],
        related=["verb-sein", "genus"],
    ),
    GrammarTopic(
        slug="regelmaessige-verben",
        title="Regelmäßige Verben im Präsens",
        level="A1",
        category="Verben",
        summary="Regelmäßige Verben im Präsens – das Grundmuster für die meisten deutschen Verben.",
        explanation="""Die meisten deutschen Verben sind **regelmäßig** (schwach). Sie folgen einem festen Konjugationsmuster im Präsens:

**Stamm finden:** Infinitiv ohne **-en** (oder **-n**). Beispiel: **wohnen** → Stamm: **wohn-**

| Person | Endung | Beispiel (wohnen) |
|--------|--------|-------------------|
| ich | -e | ich wohne |
| du | -st | du wohnst |
| er/sie/es | -t | er wohnt |
| wir | -en | wir wohnen |
| ihr | -t | ihr wohnt |
| sie/Sie | -en | sie wohnen |

**Besonderheiten:**
- Endet der Stamm auf **-d, -t** oder **Konsonant + m/n**: Extra **-e-** vor -st und -t: *du arbeit**e**st, er arbeit**e**t*.
- Endet der Stamm auf **-s, -ß, -z**: Kein extra -s- bei du: *du tanzt* (nicht: du tanzst).
- Verben auf **-eln** verlieren das -e-: *ich sammle* (nicht: ich sammele).""",
        structure="Stamm + -e · -st · -t · -en · -t · -en",
        rules=[
            "Die meisten deutschen Verben sind regelmäßig und folgen diesem Muster.",
            "Endet der Stamm auf -d/-t oder Konsonant+m/n, füge -e- vor -st und -t ein.",
            'Endet der Stamm auf -s/-ß/-z, fällt bei "du" das -s- weg: "du tanzt".',
            '"wir" und "sie/Sie" verwenden immer den Infinitiv (Stamm + -en).',
            'Bei trennbaren Verben wird das Präfix ans Ende gestellt: "ich stehe auf".',
        ],
        examples=[
            GrammarExample(text="Ich wohne in Berlin.", translation=None),
            GrammarExample(text="Du lernst Deutsch.", translation=None),
            GrammarExample(
                text="Er arbeitet bei Siemens.",
                translation=None,
                note="-d → extra -e-",
            ),
            GrammarExample(text="Wir kaufen ein Auto.", translation=None),
            GrammarExample(text="Tanzt du gern?", translation=None, note="-z → kein -s-"),
            GrammarExample(text="Sie spielen Fußball.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Du arbeitst.",
                correct="Du arbeitest.",
                note='"Arbeiten" hat den Stamm "arbeit-". Bei -t am Ende muss ein -e- vor -st.',
            ),
            GrammarMistake(
                wrong="Er wohne in Berlin.",
                correct="Er wohnt in Berlin.",
                note='Die 3. Person Singular endet auf -t. "-e" ist 1. Person.',
            ),
        ],
        related=["verb-sein", "verb-haben", "trennbare-verben", "personalpronomen"],
    ),
    GrammarTopic(
        slug="trennbare-verben",
        title="Trennbare Verben",
        level="A1",
        category="Verben",
        summary="Trennbare Verben – wie Präfixe sich ablösen und ans Satzende wandern.",
        explanation="""**Trennbare Verben** bestehen aus einem **Präfix** (Vorsilbe) und einem Basisverb. Im Präsens wird das Präfix **abgetrennt** und ans **Satzende** gestellt.

**Beispiele:**

| Infinitiv | Satz |
|-----------|------|
| **auf**stehen | Ich stehe um 7 Uhr **auf**. |
| **an**rufen | Rufst du mich **an**? |
| **ein**kaufen | Wir kaufen im Supermarkt **ein**. |
| **fern**sehen | Sie sieht gern **fern**. |
| **mit**kommen | Kommst du **mit**? |

**Trennbare Präfixe (die häufigsten):** ab-, an-, auf-, aus-, bei-, ein-, fern-, fort-, mit-, nach-, vor-, weg-, zu-, zurück-, zusammen-

**Wichtig:**
- Nur diese Präfixe sind trennbar. Präfixe wie **be-, er-, ver-, zer-, ent-, miss-, emp-** sind **untrennbar**.
- Bei Modalverben bleibt das trennbare Verb im Infinitiv am Satzende: *Ich muss um 7 Uhr **aufstehen**.*""",
        structure="Präfix + Verb (Infinitiv) → Verb + ... + Präfix (im Satz)",
        rules=[
            "Trennbare Präfixe stehen im Hauptsatz immer am Satzende.",
            "Das Präfix trägt die Betonung: AUFstehen, ANrufen (nicht: aufSTEHEN).",
            "Bei Modalverben bleibt das trennbare Verb im Infinitiv beisammen: Ich muss aufstehen.",
            'Im Nebensatz wird das trennbare Verb nicht getrennt: "..., weil ich um 7 Uhr aufstehe."',
            "Nicht verwechseln: bekommen (untrennbar) vs mitkommen (trennbar).",
        ],
        examples=[
            GrammarExample(text="Ich stehe jeden Tag um 7 Uhr auf.", translation=None),
            GrammarExample(text="Rufst du mich morgen an?", translation=None),
            GrammarExample(text="Wir kaufen am Samstag ein.", translation=None),
            GrammarExample(text="Sie sieht abends fern.", translation=None),
            GrammarExample(text="Wann fängt der Film an?", translation=None),
            GrammarExample(text="Kommst du mit ins Kino?", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich aufstehe um 7 Uhr.",
                correct="Ich stehe um 7 Uhr auf.",
                note="Das Präfix wird abgetrennt und ans Satzende gestellt.",
            ),
            GrammarMistake(
                wrong="Kannst du mich morgen anrufst?",
                correct="Kannst du mich morgen anrufen?",
                note="Nach Modalverb steht der Infinitiv (anrufen), nicht die konjugierte Form.",
            ),
        ],
        related=["regelmaessige-verben", "modalverben"],
    ),
    GrammarTopic(
        slug="uhrzeit",
        title="Die Uhrzeit",
        level="A1",
        category="Syntax",
        summary="Die Uhrzeit im Deutschen – offizielle und umgangssprachliche Formen, Stunden und Minuten.",
        explanation="""Es gibt im Deutschen zwei Arten, die Uhrzeit auszudrücken:

### 1. Offizielle Zeit (24-Stunden-Format)
Wird bei Terminen, Fahrplänen und im formellen Kontext verwendet:
- *Der Zug kommt um **vierzehn Uhr dreißig**.* (14:30)
- *Die Sitzung beginnt um **neunzehn Uhr fünfzehn**.* (19:15)

### 2. Umgangssprachliche Zeit (12-Stunden-Format)
Wird im Alltag mit Freunden und Familie verwendet:
- **Volle Stunde**: *Es ist **drei**.* (3:00)
- **Viertel**: *Es ist **Viertel nach** drei.* (3:15) / *Es ist **Viertel vor** vier.* (3:45)
- **Halb**: *Es ist **halb** vier.* (3:30) ⚠️ **Halb vier = halb vor vier = 3:30!**
- **Minuten mit nach/vor**: *Es ist **zehn nach** drei.* (3:10) / *Es ist **zwanzig vor** vier.* (3:40)

**Wichtige Wörter:**
- **um** = at (Um wie viel Uhr? — Um 8 Uhr.)
- **von ... bis** = from ... to (von 9 bis 17 Uhr)""",
        structure="Es ist + [Zahl] + Uhr (offiziell) · Es ist + [Minuten] + nach/vor + [Stunde] (umgangssprachlich)",
        rules=[
            'Offizielle Zeit verwendet 24-Stunden-Format: "15:30" = "fünfzehn Uhr dreißig".',
            '"Halb" bezieht sich auf die nächste Stunde: "halb vier" = 3:30 Uhr.',
            '"Um" wird für Zeitpunkte verwendet: "um 8 Uhr", "um halb drei".',
            '"Von ... bis" gibt einen Zeitraum an: "von 9 bis 12 Uhr".',
            "Bei der umgangssprachlichen Zeit wird meist eine 12-Stunden-Zählung verwendet.",
        ],
        examples=[
            GrammarExample(
                text="Wie spät ist es? — Es ist halb zehn.",
                translation=None,
                note="Achtung: halb zehn = 9:30",
            ),
            GrammarExample(text="Der Bus kommt um Viertel nach acht.", translation=None),
            GrammarExample(
                text="Der Film beginnt um zwanzig Uhr.",
                translation=None,
                note="offiziell",
            ),
            GrammarExample(text="Ich arbeite von neun bis fünf.", translation=None),
            GrammarExample(text="Es ist fünf vor zwölf.", translation=None, note="11:55"),
            GrammarExample(
                text="Um wie viel Uhr frühstückst du?",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Es ist halb drei = 3:30",
                correct="Es ist halb vier = 3:30",
                note='"Halb" zeigt auf die nächste volle Stunde. "Halb vier" = 3:30.',
            ),
            GrammarMistake(
                wrong="Um halb drei Uhr",
                correct="Um halb drei",
                note='Nach "halb" sagt man nicht "Uhr". Nur bei vollen Stunden: "um drei Uhr".',
            ),
        ],
        related=["wochentage", "regelmaessige-verben"],
    ),
    GrammarTopic(
        slug="moegen-gern",
        title="Vorlieben ausdrücken",
        level="A1",
        category="Verben",
        summary="Vorlieben ausdrücken mit mögen, gern, lieber und am liebsten.",
        explanation="""Im Deutschen gibt es mehrere Möglichkeiten, Vorlieben auszudrücken:

### 1. **mögen** (to like)

| Person | Form |
|--------|------|
| ich | mag |
| du | magst |
| er/sie/es | mag |
| wir | mögen |
| ihr | mögt |
| sie/Sie | mögen |

*Ich **mag** Pizza. / **Magst** du Kaffee?*

### 2. **gern / gerne** (with pleasure)
Wird mit einem Verb kombiniert:
- *Ich spiele **gern** Fußball.*
- *Er liest **gern** Bücher.*

### 3. **Steigerung: lieber / am liebsten**
- **gern** = I like to
- **lieber** = I prefer to
- **am liebsten** = I like ... most / my favourite is

*Ich trinke **gern** Kaffee, aber ich trinke **lieber** Tee. **Am liebsten** trinke ich Wasser.*

**mögen vs möchten:**
- *Ich mag Pizza.* = I like pizza (allgemein)
- *Ich möchte eine Pizza.* = I would like a pizza (jetzt / Bestellung)""",
        structure="mögen + Nomen (Akk.) · Verb + gern/lieber/am liebsten",
        rules=[
            "Mögen ist ein unregelmäßiges Verb: ich mag, du magst, er mag.",
            'Mögen + Nomen (Akkusativ): "Ich mag Hunde."',
            'Gern steht nach dem Verb: "Ich tanze gern."',
            "Die Steigerung: gern → lieber → am liebsten.",
            'Möchten ist der Konjunktiv II von "mögen" und drückt einen Wunsch aus: "Ich möchte ein Eis."',
        ],
        examples=[
            GrammarExample(text="Ich mag Schokolade.", translation=None),
            GrammarExample(text="Magst du klassische Musik?", translation=None),
            GrammarExample(text="Ich spiele gern Tennis.", translation=None),
            GrammarExample(
                text="Ich trinke lieber Tee als Kaffee.",
                translation=None,
                note="Vergleich",
            ),
            GrammarExample(
                text="Am liebsten esse ich Pizza.",
                translation=None,
                note="am liebsten",
            ),
            GrammarExample(text="Möchtest du etwas trinken?", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich mag Tennis spielen.",
                correct="Ich spiele gern Tennis.",
                note='Mögen steht normalerweise mit einem Nomen, nicht mit einem zweiten Verb. Für Aktivitäten: "gern" + Verb.',
            ),
            GrammarMistake(
                wrong="Ich mag mehr Kaffee.",
                correct="Ich mag Kaffee lieber. / Ich trinke lieber Kaffee.",
                note='Mehr mögen ist Deutsch-Englisch. Verwende "lieber".',
            ),
        ],
        related=["akkusativ", "verb-haben", "regelmaessige-verben"],
    ),
    GrammarTopic(
        slug="akkusativ",
        title="Der Akkusativ",
        level="A1",
        category="Kasus",
        summary="Der Akkusativ – direkte Objekte, Artikel im Akkusativ und Akkusativpräpositionen.",
        explanation="""Der **Akkusativ** ist der Fall für das **direkte Objekt** (Wen? Was?). Er wird auch nach bestimmten Präpositionen verwendet.

### Artikel im Akkusativ

| Genus | Nominativ | Akkusativ |
|-------|-----------|-----------|
| maskulin | der / ein / kein | **den** / **einen** / **keinen** |
| feminin | die / eine / keine | die / eine / keine |
| neutral | das / ein / kein | das / ein / kein |
| Plural | die / — / keine | die / — / keine |

**Nur der maskuline Artikel ändert sich im Akkusativ!** Feminin, neutral und Plural bleiben gleich.

### Akkusativ-Präpositionen (immer Akkusativ):
**durch, für, gegen, ohne, um, bis, entlang**

Merkwort: **DOGFUB** (Durch, Ohne, Gegen, Für, Um, Bis)""",
        structure="Nominativ → Akkusativ: nur maskulin ändert sich (der → den, ein → einen, kein → keinen)",
        rules=[
            "Nur der maskuline Artikel ändert sich im Akkusativ: der → den, ein → einen, kein → keinen.",
            "Feminine, neutrale und Plural Artikel bleiben im Akkusativ unverändert.",
            'Das direkte Objekt eines Verbs steht im Akkusativ: "Ich sehe den Mann." (Wen sehe ich?)',
            'Nach "durch, für, gegen, ohne, um, bis" steht immer Akkusativ.',
            "Personalpronomen im Akkusativ: mich, dich, ihn, sie, es, uns, euch, sie, Sie.",
        ],
        examples=[
            GrammarExample(text="Ich sehe den Mann.", translation=None, note="maskulin Akkusativ"),
            GrammarExample(
                text="Er kauft einen Computer.",
                translation=None,
                note="ein → einen",
            ),
            GrammarExample(
                text="Das Geschenk ist für die Mutter.",
                translation=None,
                note="feminin, kein Wechsel",
            ),
            GrammarExample(text="Wir gehen durch den Park.", translation=None),
            GrammarExample(text="Ich habe keinen Hunger.", translation=None, note="kein → keinen"),
            GrammarExample(
                text="Ohne dich macht es keinen Spaß.",
                translation=None,
                note="Personalpronomen",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich sehe der Mann.",
                correct="Ich sehe den Mann.",
                note='Nach transitiven Verben mit direktem Objekt steht Akkusativ: "der" → "den".',
            ),
            GrammarMistake(
                wrong="Das ist für der Vater.",
                correct="Das ist für den Vater.",
                note='"Für" ist eine Akkusativ-Präposition. Der Artikel muss zu "den" werden.',
            ),
        ],
        related=["bestimmte-artikel", "unbestimmte-artikel", "verneinung"],
    ),
    GrammarTopic(
        slug="verneinung",
        title="Verneinung",
        level="A1",
        category="Syntax",
        summary="Verneinung mit nicht und kein – wie man Verben, Adjektive und Nomen korrekt verneint.",
        explanation="""Es gibt zwei Arten der Verneinung im Deutschen:

### 1. **nicht** — verneint Verben, Adjektive, Adverbien, Ortsangaben
- **Am Satzende** (wenn es den ganzen Satz verneint): *Ich verstehe das **nicht**.*
- **Vor dem Element, das verneint wird**:
  - Vor Adjektiv: *Das ist **nicht gut**.*
  - Vor Ortsangabe: *Ich wohne **nicht in Berlin**.*
  - Vor Präposition: *Ich gehe **nicht ins Kino**.*

### 2. **kein** — verneint Nomen (ohne Artikel oder mit unbestimmtem Artikel)

| Genus | Nominativ | Akkusativ |
|-------|-----------|-----------|
| maskulin | kein | keinen |
| feminin | keine | keine |
| neutral | kein | kein |
| Plural | keine | keine |

*Ich habe **kein** Geld. / Das ist **keine** gute Idee. / Er hat **keinen** Hund.*

**Faustregel:** **nicht** = verneint Verben, Adjektive, Sätze / **kein** = verneint Nomen (übersetzt: not a / no)""",
        structure="nicht (verneint Verben/Adjektive) · kein/keine/keinen (verneint Nomen)",
        rules=[
            '"Nicht" steht meist am Satzende, wenn es den ganzen Satz verneint.',
            '"Nicht" steht vor dem verneinten Element (Adjektiv, Ortsangabe, Präposition).',
            '"Kein" ersetzt den unbestimmten Artikel oder den Nullartikel und wird dekliniert.',
            '"Kein" kann nicht mit dem bestimmten Artikel kombiniert werden.',
            'Im Plural ohne Artikel: "Ich habe keine Kinder." (nicht: Ich habe nicht Kinder.)',
        ],
        examples=[
            GrammarExample(text="Ich verstehe das nicht.", translation=None),
            GrammarExample(text="Das ist nicht teuer.", translation=None),
            GrammarExample(text="Ich habe kein Auto.", translation=None),
            GrammarExample(
                text="Er trinkt keinen Kaffee.",
                translation=None,
                note="Akkusativ",
            ),
            GrammarExample(text="Das ist keine gute Idee.", translation=None),
            GrammarExample(text="Ich habe keine Zeit.", translation=None, note="Plural/feminin"),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich habe nicht ein Auto.",
                correct="Ich habe kein Auto.",
                note="Ein Nomen ohne Artikel oder mit unbestimmtem Artikel wird mit 'kein' verneint.",
            ),
            GrammarMistake(
                wrong="Der Film ist kein gut.",
                correct="Der Film ist nicht gut.",
                note='Adjektive werden mit "nicht" verneint, nicht mit "kein".',
            ),
        ],
        related=["akkusativ", "unbestimmte-artikel", "ja-nein-doch"],
    ),
    GrammarTopic(
        slug="es-gibt",
        title='"Es gibt"',
        level="A1",
        category="Syntax",
        summary='Verwendung von "es gibt" – Existenzaussagen mit dem Akkusativ.',
        explanation="""**Es gibt** bedeutet *there is / there are* und wird verwendet, um die **Existenz** von etwas zu beschreiben.

**Grammatik:**
- **Es gibt** ist immer Singular.
- Das Nomen nach *es gibt* steht **immer im Akkusativ**.

| Deutsch | Englisch |
|---------|----------|
| Es gibt **einen** Supermarkt. | There is a supermarket. |
| Es gibt **ein** Problem. | There is a problem. |
| Es gibt **eine** Lösung. | There is a solution. |
| Es gibt **keine** Stadt in der Nähe. | There is no city nearby. |
| Es gibt **viele** Restaurants. | There are many restaurants. |

**Es gibt vs Es ist**: *Es gibt* beschreibt Existenz, *es ist* beschreibt eine Eigenschaft:
- *Es gibt ein Restaurant in der Straße.* (Existenz)
- *Das Restaurant ist gut.* (Eigenschaft)""",
        structure="Es gibt + Akkusativ (immer Singular Verbform: gibt)",
        rules=[
            '"Es gibt" bleibt immer im Singular, auch bei mehreren Dingen.',
            'Das Nomen nach "es gibt" steht immer im Akkusativ.',
            '"Es gibt" beschreibt Existenz, nicht Eigenschaften oder Zustände.',
            '"Es gibt" + kein für Verneinung: "Es gibt kein Problem."',
            'Im Plural ohne Artikel: "Es gibt Restaurants." / "Es gibt keine Restaurants."',
        ],
        examples=[
            GrammarExample(
                text="Es gibt einen Supermarkt in der Nähe.",
                translation=None,
            ),
            GrammarExample(text="Gibt es hier ein Krankenhaus?", translation=None),
            GrammarExample(text="Es gibt keine Probleme.", translation=None),
            GrammarExample(
                text="In Berlin gibt es viele Museen.",
                translation=None,
            ),
            GrammarExample(text="Es gibt heute Abend eine Party.", translation=None),
            GrammarExample(text="Gibt es noch Kaffee?", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Es geben viele Leute.",
                correct="Es gibt viele Leute.",
                note='"Es gibt" bleibt immer in der 3. Person Singular, egal ob Singular oder Plural folgt.',
            ),
            GrammarMistake(
                wrong="Es gibt der Supermarkt.",
                correct="Es gibt einen Supermarkt.",
                note='Nach "es gibt" steht der Akkusativ, nicht der Nominativ.',
            ),
        ],
        related=["akkusativ", "verneinung", "unbestimmte-artikel"],
    ),
    GrammarTopic(
        slug="lokalpraepositionen",
        title="Lokalpräpositionen",
        level="A1",
        category="Präpositionen",
        summary="Lokale Präpositionen in, an, auf, neben, vor, hinter, unter, über, zwischen mit Dativ.",
        explanation="""**Lokalpräpositionen** beschreiben den **Ort** oder die **Position** von Personen und Dingen. Auf A1-Niveau werden sie meist mit dem **Dativ** verwendet, um einen festen Ort anzugeben (Wo?).

| Präposition | Bedeutung | Beispiel |
|-------------|-----------|----------|
| **in** | in (inside) | in der Tasche |
| **an** | at, on (vertical surface) | an der Wand |
| **auf** | on (horizontal surface) | auf dem Tisch |
| **neben** | next to | neben dem Bett |
| **vor** | in front of | vor dem Haus |
| **hinter** | behind | hinter dem Sofa |
| **unter** | under | unter dem Bett |
| **über** | above, over | über dem Sofa |
| **zwischen** | between | zwischen den Stühlen |

**Fragewort für Ort:** **Wo?** (Where?) — *Wo ist das Buch? — Auf dem Tisch.*

**Merksatz für kontrahierte Formen:**
- in + dem → **im**: *im Kino, im Büro*
- an + dem → **am**: *am Bahnhof, am Tisch*""",
        structure="Präposition + Dativ (Wo?)",
        rules=[
            'Auf die Frage "Wo?" antwortet man mit Dativ (fester Ort).',
            "Diese Präpositionen stehen auf A1-Niveau immer mit Dativ.",
            "Kontrahierte Formen: in + dem = im, an + dem = am.",
            "Nach der Präposition muss der Artikel im Dativ stehen.",
            "Die Präposition bestimmt den Fall, nicht das Verb.",
        ],
        examples=[
            GrammarExample(text="Das Buch liegt auf dem Tisch.", translation=None),
            GrammarExample(text="Die Katze ist unter dem Bett.", translation=None),
            GrammarExample(
                text="Das Kino ist neben dem Bahnhof.",
                translation=None,
            ),
            GrammarExample(
                text="Wir warten vor dem Kino.",
                translation=None,
            ),
            GrammarExample(text="Der Spiegel hängt an der Wand.", translation=None),
            GrammarExample(text="Mein Handy ist in der Tasche.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Das Buch ist auf der Tisch.",
                correct="Das Buch ist auf dem Tisch.",
                note='Nach "auf" mit Dativ: der Tisch → dem Tisch.',
            ),
            GrammarMistake(
                wrong="Ich bin in das Kino.",
                correct="Ich bin im Kino.",
                note="Wenn es um den Ort geht (Wo?): in + dem = im. Mit Dativ.",
            ),
        ],
        related=["dativ-basic", "akkusativ"],
    ),
    GrammarTopic(
        slug="dativ-basic",
        title="Dativ Grundlagen",
        level="A1",
        category="Kasus",
        summary="Dativ-Grundlagen – Artikel, Dativpräpositionen (nach, mit, zu, bei, von, aus, seit) und indirekte Objekte.",
        explanation="""Der **Dativ** ist der dritte Fall im Deutschen. Er antwortet auf die Frage **Wem?** (to whom? / for whom?).

### Artikel im Dativ

| Genus | Nominativ | Dativ |
|-------|-----------|-------|
| maskulin | der / ein | **dem** / **einem** |
| feminin | die / eine | **der** / **einer** |
| neutral | das / ein | **dem** / **einem** |
| Plural | die / — | **den** (Nomen + **-n**) |

⚠️ Im Dativ Plural bekommt das Nomen ein **-n** (wenn es nicht schon auf -n oder -s endet): *die Kinder → den Kinder**n***.

### Dativ-Präpositionen (immer Dativ):
| Präposition | Bedeutung | Beispiel |
|-------------|-----------|----------|
| **mit** | with | mit dem Bus |
| **nach** | after, to | nach der Arbeit |
| **zu** | to | zu dem → **zum** Arzt |
| **bei** | at (a person/company) | bei mir, bei Siemens |
| **von** | from, of | von dem → **vom** Bahnhof |
| **aus** | from (inside) | aus der Schweiz |
| **seit** | since, for | seit einem Jahr |

Merkwort: **Mit, Nach, Zu, Bei, Von, Aus, Seit** — diese 7 immer mit Dativ.""",
        structure="Dativ: dem/einem (m/n) · der/einer (f) · den/— (Pl. + -n)",
        rules=[
            'Im Dativ ändern sich alle Artikel. Nur feminin bleibt "der" (aber das ist Dativ, nicht Nominativ!).',
            'Dativ Plural: Artikel "den" + Nomen mit -n: "den Kindern, den Frauen".',
            'Nach "mit, nach, zu, bei, von, aus, seit" steht immer Dativ.',
            "Kontraktionen: zu + dem = zum, zu + der = zur, von + dem = vom, bei + dem = beim.",
            'Das indirekte Objekt steht im Dativ: "Ich gebe dem Mann das Buch."',
        ],
        examples=[
            GrammarExample(text="Ich fahre mit dem Bus.", translation=None),
            GrammarExample(
                text="Er geht zum Arzt.",
                translation=None,
                note="zu + dem = zum",
            ),
            GrammarExample(text="Ich wohne bei meinen Eltern.", translation=None),
            GrammarExample(
                text="Nach der Arbeit gehe ich ins Fitnessstudio.",
                translation=None,
            ),
            GrammarExample(
                text="Das Geschenk ist von meiner Freundin.",
                translation=None,
            ),
            GrammarExample(text="Ich komme aus der Türkei.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich fahre mit der Bus.",
                correct="Ich fahre mit dem Bus.",
                note='Nach "mit" steht Dativ. "Der Bus" → Dativ: "dem Bus".',
            ),
            GrammarMistake(
                wrong="Ich gehe zu der Arbeit.",
                correct="Ich gehe zur Arbeit.",
                note="Zu + der = zur. Die Kontraktion ist idiomatisch und üblich.",
            ),
        ],
        related=["akkusativ", "lokalpraepositionen"],
    ),
    GrammarTopic(
        slug="werden-futur",
        title='Futur I mit "werden"',
        level="A1",
        category="Verben",
        summary='Futur mit "werden" – wie man über zukünftige Ereignisse spricht.',
        explanation="""Das Futur I wird mit dem Hilfsverb **werden** + Infinitiv gebildet.

**Konjugation von werden:**

| Person | Form |
|--------|------|
| ich | werde |
| du | wirst |
| er/sie/es | wird |
| wir | werden |
| ihr | werdet |
| sie/Sie | werden |

**Satzbau:** *Ich **werde** morgen nach Berlin **fahren**.*
- Das konjugierte *werden* steht auf Position 2.
- Der Infinitiv steht am **Satzende**.

**Verwendung:**
- **Zukünftige Ereignisse**: *Morgen werde ich ins Kino gehen.*
- **Vorhersagen**: *Es wird morgen regnen.*
- **Versprechen / Absichten**: *Ich werde dir helfen.*

⚠️ Im gesprochenen Deutsch wird die Zukunft oft mit dem **Präsens + Zeitangabe** ausgedrückt:
*Ich fahre morgen nach Berlin.* (statt: Ich werde morgen nach Berlin fahren.)

Das Präsens für Zukunft ist völlig korrekt und sogar häufiger als das Futur I.""",
        structure="werden (konjugiert) + ... + Infinitiv (am Satzende)",
        rules=[
            '"Werden" + Infinitiv bildet das Futur I.',
            'Der Infinitiv steht am Satzende: "Ich werde morgen kommen."',
            "In der Umgangssprache wird das Futur oft durch Präsens + Zeitangabe ersetzt.",
            "Werden ist unregelmäßig: ich werde, du wirst, er wird.",
            'Futur I kann auch Vermutungen über die Gegenwart ausdrücken: "Er wird jetzt zu Hause sein."',
        ],
        examples=[
            GrammarExample(
                text="Ich werde morgen nach München fahren.",
                translation=None,
            ),
            GrammarExample(text="Es wird am Wochenende regnen.", translation=None),
            GrammarExample(text="Wirst du zur Party kommen?", translation=None),
            GrammarExample(text="Wir werden dich besuchen.", translation=None),
            GrammarExample(text="Er wird nächste Woche umziehen.", translation=None),
            GrammarExample(
                text="Morgen gehe ich ins Kino.",
                translation=None,
                note="Präsens statt Futur I",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich werde morgen nach Berlin fahre.",
                correct="Ich werde morgen nach Berlin fahren.",
                note='Nach "werden" steht immer der Infinitiv (fahren), nicht die konjugierte Form.',
            ),
            GrammarMistake(
                wrong="Morgen ich werde gehen.",
                correct="Morgen werde ich gehen.",
                note="Das konjugierte Verb (werde) muss an Position 2 stehen. Die Zeitangabe nimmt Position 1 ein.",
            ),
        ],
        related=["regelmaessige-verben", "trennbare-verben", "modalverben"],
    ),
    GrammarTopic(
        slug="modalverben",
        title="Modalverben",
        level="A1",
        category="Verben",
        summary="Modalverben können, wollen, müssen, dürfen, sollen, möchten – Bedeutung, Konjugation und Satzbau.",
        explanation="""**Modalverben** modifizieren die Bedeutung des Hauptverbs. Sie stehen immer mit einem zweiten Verb im **Infinitiv** am Satzende.

### Die 6 Modalverben:

| Modalverb | Bedeutung | Beispiel |
|-----------|-----------|----------|
| **können** | can, to be able to | Ich kann schwimmen. |
| **wollen** | to want | Ich will nach Hause gehen. |
| **müssen** | must, to have to | Ich muss arbeiten. |
| **dürfen** | may, to be allowed to | Hier darf man nicht rauchen. |
| **sollen** | should, to be supposed to | Du sollst zum Arzt gehen. |
| **möchten** | would like | Ich möchte einen Kaffee. |

**Konjugation (Präsens):**

| | können | wollen | müssen | dürfen | sollen | möchten |
|--------|--------|--------|--------|--------|--------|---------|
| ich | kann | will | muss | darf | soll | möchte |
| du | kannst | willst | musst | darfst | sollst | möchtest |
| er/sie/es | kann | will | muss | darf | soll | möchte |
| wir | können | wollen | müssen | dürfen | sollen | möchten |
| ihr | könnt | wollt | müsst | dürft | sollt | möchtet |
| sie/Sie | können | wollen | müssen | dürfen | sollen | möchten |

**Satzbau:** *Ich **muss** heute lange **arbeiten**.*
→ Das Modalverb steht auf Position 2, der Infinitiv am Satzende.""",
        structure="Modalverb (konjugiert, Position 2) + ... + Infinitiv (am Satzende)",
        rules=[
            'Modalverben stehen immer mit einem Infinitiv ohne "zu".',
            "Modalverben haben in der 1. und 3. Person Singular die gleiche Form (ich/er kann).",
            'Der Infinitiv steht am Satzende: "Ich will nach Hause gehen."',
            'Möchten ist der Konjunktiv II von "mögen" und bedeutet "would like".',
            'Bei trennbaren Verben: "Ich muss um 7 Uhr aufstehen." (nicht getrennt!).',
        ],
        examples=[
            GrammarExample(text="Ich kann gut schwimmen.", translation=None),
            GrammarExample(text="Willst du mitkommen?", translation=None),
            GrammarExample(
                text="Er muss morgen früh aufstehen.",
                translation=None,
            ),
            GrammarExample(text="Hier darf man nicht parken.", translation=None),
            GrammarExample(
                text="Du solltest mehr schlafen.",
                translation=None,
                note="sollen im Konjunktiv = Ratschlag",
            ),
            GrammarExample(text="Ich möchte eine Cola, bitte.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ich muss zu arbeiten.",
                correct="Ich muss arbeiten.",
                note='Nach Modalverben steht der Infinitiv ohne "zu".',
            ),
            GrammarMistake(
                wrong="Er kannt gut kochen.",
                correct="Er kann gut kochen.",
                note='Die 3. Person Singular von "können" ist "kann" (ohne -t).',
            ),
        ],
        related=[
            "regelmaessige-verben",
            "trennbare-verben",
            "werden-futur",
            "moegen-gern",
        ],
    ),
    GrammarTopic(
        slug="wochentage",
        title="Wochentage und Zeitangaben",
        level="A1",
        category="Syntax",
        summary="Wochentage, Monate, Jahreszeiten und Zeitausdrücke mit den Präpositionen am, im, um.",
        explanation="""### Wochentage (alle maskulin: **der**)

| Deutsch | Englisch |
|---------|----------|
| der Montag | Monday |
| der Dienstag | Tuesday |
| der Mittwoch | Wednesday |
| der Donnerstag | Thursday |
| der Freitag | Friday |
| der Samstag / Sonnabend | Saturday |
| der Sonntag | Sunday |

### Monate (alle maskulin: **der**)
Januar, Februar, März, April, Mai, Juni, Juli, August, September, Oktober, November, Dezember

### Jahreszeiten (alle maskulin: **der**)
der Frühling, der Sommer, der Herbst, der Winter

### Präpositionen mit Zeitangaben:

| Präposition | Verwendung |
|-------------|------------|
| **am** | Wochentage, Tageszeiten (am Morgen), Datum |
| **im** | Monate, Jahreszeiten |
| **um** | Uhrzeit |
| **von ... bis** | Zeitraum |""",
        structure="am + Wochentag · im + Monat/Jahreszeit · um + Uhrzeit",
        rules=[
            "Alle Wochentage und Monate sind maskulin (der Montag, der Januar).",
            '"Am" verwendet man für Tage und Tageszeiten: am Montag, am Morgen.',
            '"Im" verwendet man für Monate und Jahreszeiten: im August, im Winter.',
            '"Um" verwendet man für Uhrzeiten: um 14 Uhr.',
            '"Von ... bis" drückt einen Zeitraum aus: von Montag bis Freitag.',
        ],
        examples=[
            GrammarExample(text="Am Montag habe ich frei.", translation=None),
            GrammarExample(text="Im Sommer fahren wir ans Meer.", translation=None),
            GrammarExample(text="Der Kurs beginnt um 9 Uhr.", translation=None),
            GrammarExample(
                text="Ich arbeite von Dienstag bis Freitag.",
                translation=None,
            ),
            GrammarExample(text="Am Wochenende schlafe ich lange.", translation=None),
            GrammarExample(text="Im Januar ist es kalt.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="In Montag arbeite ich.",
                correct="Am Montag arbeite ich.",
                note='Wochentage verwenden "am", nicht "in" oder "im".',
            ),
            GrammarMistake(
                wrong="Am Sommer ist es heiß.",
                correct="Im Sommer ist es heiß.",
                note='Jahreszeiten und Monate verwenden "im", nicht "am".',
            ),
        ],
        related=["uhrzeit", "lokalpraepositionen", "dativ-basic"],
    ),
    GrammarTopic(
        slug="imperativ",
        title="Der Imperativ",
        level="A1",
        category="Verben",
        summary="Der Imperativ – Befehle, Anweisungen und Bitten im Deutschen.",
        explanation="""Der **Imperativ** wird für Befehle, Aufforderungen und Bitten verwendet.

### Formen:

| Person | Bildung | Beispiel (kommen) |
|--------|---------|-------------------|
| **du** | Stamm (ohne -st) | Komm! |
| **ihr** | Stamm + -t | Kommt! |
| **Sie** | Infinitiv + Sie | Kommen Sie! |

**Genauer:**

1. **du-Form**: Verbstamm + optional **-e**: *Komm(e)! Geh(e)! Sag(e)!*
   - In der Umgangssprache oft ohne -e.
   - Bei Stamm auf -d/-t oder Konsonant+m/n: **-e** obligatorisch: *Arbeite! Warte!*
   - Umlaut fällt weg: *du fährst → Fahr(e)!* (nicht: Fähr!)

2. **ihr-Form**: Wie das konjugierte Verb ohne Pronomen: *Kommt! Geht! Arbeitet!*

3. **Sie-Form**: Infinitiv + Sie: *Kommen Sie! Gehen Sie!*

**Bitte hinzufügen macht es höflich:** *Komm bitte! / Kommen Sie bitte!*""",
        structure="du: Stamm (+ -e) · ihr: Stamm + -t · Sie: Infinitiv + Sie",
        rules=[
            "Du-Imperativ: Verbstamm ohne Endung. Umgangssprachlich oft ohne -e.",
            'Umlaute fallen bei der du-Form weg: "Fahr!" (nicht: Fähr).',
            'Vokalwechsel (e→i) bleibt: "Iss!" (von essen), "Gib!" (von geben).',
            'Ihr-Imperativ: identisch mit der konjugierten ihr-Form, aber ohne "ihr".',
            'Sie-Imperativ für formelle Ansprache: Infinitiv + "Sie".',
        ],
        examples=[
            GrammarExample(text="Komm bitte hierher!", translation=None, note="du"),
            GrammarExample(text="Warte einen Moment!", translation=None, note="-e obligatorisch"),
            GrammarExample(text="Esst langsam!", translation=None, note="ihr"),
            GrammarExample(text="Nehmen Sie Platz!", translation=None, note="Sie, formell"),
            GrammarExample(text="Sei ruhig!", translation=None, note="unregelmäßig: sein"),
            GrammarExample(
                text="Lies den Text!", translation=None, note="Vokalwechsel e→ie bleibt"
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Du komm hier!",
                correct="Komm hierher!",
                note='Im Imperativ wird "du" weggelassen. Nur das Verb bleibt.',
            ),
            GrammarMistake(
                wrong="Fähr nach Hause!",
                correct="Fahr nach Hause!",
                note='Bei der du-Form des Imperativs fällt der Umlaut weg: "du fährst" → "Fahr!".',
            ),
        ],
        related=["personalpronomen", "regelmaessige-verben", "modalverben"],
    ),
    GrammarTopic(
        slug="ja-nein-doch",
        title="Ja/Nein/Doch",
        level="A1",
        category="Syntax",
        summary="Fragen richtig beantworten – das dreigliedrige System ja, nein und doch.",
        explanation="""Im Deutschen gibt es **drei** Antwortwörter für Ja/Nein-Fragen: **ja**, **nein** und **doch**.

### Die Regel:

| Frage | Positive Antwort | Negative Antwort |
|-------|-----------------|------------------|
| Positive Frage (ohne Verneinung) | **Ja** | **Nein** |
| Negative Frage (mit Verneinung) | **Doch** | **Nein** |

### Beispiele:

1. **Positive Frage:**
   - *Kommst du mit?* — **Ja**, ich komme mit. / **Nein**, ich komme nicht mit.

2. **Negative Frage:**
   - *Kommst du **nicht** mit?* — **Doch**, ich komme mit. / **Nein**, ich komme nicht mit.

**Doch** korrigiert eine negative Annahme und bestätigt das Positive!

- *Hast du keinen Hunger?* — **Doch**, ich habe Hunger.
- *Bist du nicht müde?* — **Doch**, sehr müde.
- *Magst du keinen Kaffee?* — **Doch**, ich mag Kaffee.

Dieses System (ja/nein/doch) gibt es im Englischen nicht — dort gibt es nur yes und no. *Doch* ist eine der wichtigsten Besonderheiten des Deutschen.""",
        structure="Positive Frage → Ja/Nein · Negative Frage → Doch/Nein",
        rules=[
            '"Ja" bestätigt eine positive Frage.',
            '"Nein" verneint sowohl eine positive als auch eine negative Frage.',
            '"Doch" widerspricht einer negativen Frage und bestätigt das Gegenteil.',
            "Bei negativen Fragen ohne Verneinungswort (rhetorisch) kann ja verwendet werden.",
            '"Doch" kann auch als Modalpartikel verwendet werden (Betonung): "Das ist doch klar!"',
        ],
        examples=[
            GrammarExample(
                text="Kommst du mit? — Ja, gern.",
                translation=None,
                note="positive Frage → ja",
            ),
            GrammarExample(
                text="Kommst du mit? — Nein, ich habe keine Zeit.",
                translation=None,
            ),
            GrammarExample(
                text="Kommst du nicht mit? — Doch, ich komme mit.",
                translation=None,
                note="negative Frage → doch",
            ),
            GrammarExample(
                text="Hast du keinen Hunger? — Doch, ich habe Hunger.",
                translation=None,
            ),
            GrammarExample(
                text="Magst du keinen Kaffee? — Nein, ich trinke keinen Kaffee.",
                translation=None,
            ),
            GrammarExample(
                text="Bist du nicht müde? — Doch, sehr!",
                translation=None,
                note="kurze Antwort mit doch",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Hast du keinen Hunger? — Ja, ich habe Hunger.",
                correct="Hast du keinen Hunger? — Doch, ich habe Hunger.",
                note='Auf eine negative Frage antwortet man nicht mit "ja", sondern mit "doch".',
            ),
            GrammarMistake(
                wrong="Kommst du nicht? — Ja.",
                correct="Kommst du nicht? — Doch.",
                note='"Ja" auf eine negative Frage ist falsch. Es muss "doch" heißen.',
            ),
        ],
        related=["verneinung"],
    ),
]
