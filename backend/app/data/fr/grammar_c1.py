"""French grammar topics — C1."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="subjonctif-concessif",
        title="Le subjonctif concessif",
        level="C1",
        category="Verbes",
        summary="Maîtrise des nuances concessives : quoi que, où que, qui que, quel que.",
        explanation="Les structures concessives avec subjonctif expriment une opposition nuancée :\n\n- **Quoi que + subjonctif** (peu importe ce que) : *Quoi qu'il **dise**, je ne le crois pas.*\n- **Où que + subjonctif** (peu importe où) : *Où que tu **ailles**, je te retrouverai.*\n- **Qui que + subjonctif** (peu importe qui) : *Qui que vous **soyez**, vous êtes le bienvenu.*\n- **Quel(le)(s) que + subjonctif** (quel que soit) : *Quelles que **soient** vos raisons, cela reste inacceptable.*\n\nNe pas confondre **quoi que** (concession) et **quoique** (bien que).",
        structure="quoi que/où que/qui que/quel que + subjonctif",
        rules=[
            "Quoi que = peu importe ce que (en deux mots).",
            "Quoique = bien que (en un seul mot).",
            "Quel que s'accorde avec le sujet.",
            "Toujours le subjonctif après ces locutions.",
        ],
        examples=[
            GrammarExample(text="Quoi qu'il arrive, je resterai à tes côtés.", translation=None),
            GrammarExample(text="Où que tu ailles, je penserai à toi.", translation=None),
            GrammarExample(
                text="Quelles que soient les difficultés, nous réussirons.",
                translation=None,
                note="accord de 'quelles'",
            ),
            GrammarExample(text="Qui que vous soyez, veuillez vous identifier.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quoique tu dises, je ne te crois pas.",
                correct="Quoi que tu dises, je ne te crois pas.",
                note="'Quoi que' = concession. 'Quoique' = bien que.",
            ),
        ],
        related=["subjonctif-conjonctions", "subjonctif-final", "subjonctif-relatives"],
    ),
    GrammarTopic(
        slug="subjonctif-final",
        title="Le subjonctif de but",
        level="C1",
        category="Verbes",
        summary="Le subjonctif pour exprimer la finalité : pour que, afin que, de peur que, de crainte que.",
        explanation="Les conjonctions de **but** exigent le subjonctif quand il y a changement de sujet :\n\n- **Pour que / Afin que + subjonctif** : *Je te l'explique pour que tu **comprennes**.*\n- **De peur que / De crainte que + subjonctif** (but négatif) : *Il chuchote de peur qu'on ne l'**entende**.*\n\n**Ne explétif** : après 'de peur que', 'de crainte que', 'avant que', on ajoute parfois un 'ne' explétif (sans valeur négative).\n- *Dépêche-toi avant qu'il ne **parte**.* (ne = explétif, pas de sens négatif)\n\nSans changement de sujet → **pour / afin de + infinitif**.",
        structure="pour que/afin que + subjonctif · de peur que + ne + subjonctif",
        rules=[
            "Changement de sujet → subjonctif.",
            "Même sujet → pour/afin de + infinitif.",
            "Le 'ne' explétif après avant que, de peur que (soutenu).",
        ],
        examples=[
            GrammarExample(
                text="J'explique lentement pour que tout le monde suive.",
                translation=None,
            ),
            GrammarExample(
                text="Il est sorti discrètement de peur qu'on ne le remarque.",
                translation=None,
                note="ne explétif",
            ),
            GrammarExample(text="Rentre avant qu'il ne fasse nuit.", translation=None),
            GrammarExample(
                text="Je te prête ce livre afin que tu puisses préparer l'examen.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Je t'explique pour que tu comprends.",
                correct="Je t'explique pour que tu comprennes.",
                note="'Pour que' est suivi du subjonctif.",
            ),
        ],
        related=[
            "subjonctif-conjonctions",
            "subjonctif-concessif",
            "subjonctif-present",
        ],
    ),
    GrammarTopic(
        slug="subjonctif-relatives",
        title="Le subjonctif dans les relatives",
        level="C1",
        category="Verbes",
        summary="Subjonctif dans les propositions relatives restrictives, après un superlatif, ou avec un antécédent indéfini.",
        explanation="Le subjonctif s'utilise dans la proposition relative dans ces cas :\n\n**Antécédent indéfini ou nié** :\n- *Je cherche quelqu'un qui **parle** chinois.* (je ne sais pas si cette personne existe)\n- *Je ne connais personne qui **puisse** t'aider.*\n\n**Après un superlatif** :\n- *C'est le meilleur livre que j'**aie** jamais lu.*\n\n**Après le seul, l'unique, le premier** :\n- *C'est la seule personne qui **ait** répondu.*\n\n**Opposition** : si l'antécédent est défini → indicatif (*Je connais quelqu'un qui parle chinois*).",
        structure="nom indéfini/nié + qui/que + subjonctif",
        rules=[
            "Antécédent dont l'existence n'est pas certaine → subjonctif.",
            "Antécédent défini → indicatif.",
            "Après un superlatif, le subjonctif souligne l'appréciation; l'indicatif peut présenter un constat factuel.",
            "Après le seul, l'unique ou le premier, le mode dépend du sens et de la perspective du locuteur.",
        ],
        examples=[
            GrammarExample(
                text="Je cherche un appartement qui ait un balcon.",
                translation=None,
                note="indéfini → subjonctif",
            ),
            GrammarExample(
                text="Je connais un appartement qui a un balcon.",
                translation=None,
                note="défini → indicatif",
            ),
            GrammarExample(
                text="C'est le plus beau spectacle que j'aie jamais vu.",
                translation=None,
            ),
            GrammarExample(
                text="Il n'y a personne ici qui sache parler japonais.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Je cherche une maison qui aie un jardin.",
                correct="Je cherche une maison qui ait un jardin.",
                note="Au subjonctif, la troisième personne est ait, pas aie. L'indicatif a reste possible pour une maison présentée comme existante.",
            ),
        ],
        related=["subjonctif-present", "subjonctif-concessif", "dont"],
    ),
    GrammarTopic(
        slug="nominalisation",
        title="La nominalisation",
        level="C1",
        category="Expression",
        summary="Transformer des phrases verbales en structures nominales pour le style académique.",
        explanation="La **nominalisation** consiste à transformer un verbe ou un adjectif en nom. C'est une technique clé du style académique.\n\n**Verbe → Nom** :\n- *augmenter → l'augmentation*\n- *développer → le développement*\n- *disparaître → la disparition*\n\n**Adjectif → Nom** :\n- *efficace → l'efficacité*\n- *lent → la lenteur*\n\n**Phrase verbale → Phrase nominale** :\n- *Le chômage augmente → L'augmentation du chômage*\n- *Les technologies se développent → Le développement des technologies*",
        structure="déterminant + nom + complément du nom",
        rules=[
            "La nominalisation allège le style et le rend plus formel.",
            "Le verbe ou l'adjectif devient le noyau nominal.",
            "Bien choisir le suffixe : -tion, -ment, -té, -eur, -age, -ance.",
        ],
        examples=[
            GrammarExample(
                text="L'augmentation du trafic aérien inquiète les écologistes.",
                translation=None,
                note="augmenter → augmentation",
            ),
            GrammarExample(
                text="La disparition des abeilles menace la biodiversité.",
                translation=None,
                note="disparaître → disparition",
            ),
            GrammarExample(
                text="La lenteur du processus a été critiquée.",
                translation=None,
                note="lent → lenteur",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Le augmentement du chômage.",
                correct="L'augmentation du chômage.",
                note="'Augmenter' → 'augmentation', pas 'augmentement'.",
            ),
        ],
        related=["impersonalite", "registre-formel", "orthotypographie"],
    ),
    GrammarTopic(
        slug="impersonalite",
        title="L'impersonnalité",
        level="C1",
        category="Expression",
        summary="Tournures impersonnelles pour le style académique et objectif.",
        explanation="L'**impersonnalité** est essentielle dans l'écriture académique pour donner un ton objectif.\n\n**Structures impersonnelles** :\n- *Il convient de + infinitif*\n- *Il est à noter que...*\n- *Il s'avère que...*\n- *Force est de constater que...*\n- *Il ressort de cette étude que...*\n- *On ne saurait trop insister sur...*\n\n**Éviter 'je'** : le remplacer par 'nous' de modestie ou par des structures passives/impersonnelles.",
        structure="il + verbe impersonnel + de/que",
        rules=[
            "Préférer les structures impersonnelles au 'je'.",
            "Il convient de, il importe de, il s'agit de.",
            "Éviter 'on' en contexte très formel.",
        ],
        examples=[
            GrammarExample(
                text="Il convient de souligner l'importance de ces résultats.",
                translation=None,
            ),
            GrammarExample(
                text="Force est de constater que les progrès sont insuffisants.",
                translation=None,
            ),
            GrammarExample(
                text="Il ressort de l'enquête que la majorité des sondés approuvent la mesure.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Je pense que c'est une bonne idée.",
                correct="Il apparaît que cette proposition présente des avantages.",
                note="Remplacer 'je pense' par une tournure impersonnelle en contexte académique.",
            ),
        ],
        related=["nominalisation", "registre-formel", "orthotypographie"],
    ),
    GrammarTopic(
        slug="orthotypographie",
        title="L'orthotypographie française",
        level="C1",
        category="Expression",
        summary="Règles typographiques du français : guillemets, espaces, majuscules, tirets.",
        explanation="L'**orthotypographie** est l'ensemble des règles typographiques propres à une langue. En français :\n\n**Guillemets** : « ... » (espace insécable entre guillemet et texte).\n\n**Espaces insécables** (devant certains signes) :\n- point-virgule (;), deux-points (:), point d'exclamation (!), point d'interrogation (?), guillemets, pourcentages (%).\n\n**Majuscules accentuées** : É, È, Ç, À, etc. (souvent oubliées).\n\n**Tirets** : tiret cadratin (—) pour les incises, tiret demi-cadratin (–) pour les intervalles.\n\n**Abréviations** : M. (Monsieur), Mme (Madame), etc.",
        structure="« texte » · texte ; texte : · État (pas Etat)",
        rules=[
            "Espace insécable avant : ; ! ? %",
            "Espace insécable à l'intérieur des guillemets « ... ».",
            "Les majuscules prennent les accents en français.",
            "Pas de point après les titres centrés.",
        ],
        examples=[
            GrammarExample(
                text="« Cette découverte est majeure », a déclaré le chercheur.",
                translation=None,
            ),
            GrammarExample(
                text="Trois options s'offrent à nous : négocier, résister ou céder.",
                translation=None,
            ),
            GrammarExample(
                text="L'État français a annoncé une nouvelle réforme.",
                translation=None,
                note="majuscule accentuée",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="'Cette découverte est majeure', a déclaré le chercheur.",
                correct="« Cette découverte est majeure », a déclaré le chercheur.",
                note="En français, les guillemets sont « ... », pas ' ... '.",
            ),
        ],
        related=["registre-formel", "nominalisation", "impersonalite"],
    ),
    GrammarTopic(
        slug="derivation",
        title="La dérivation lexicale",
        level="C1",
        category="Lexique",
        summary="Suffixes et préfixes productifs du français.",
        explanation="Maîtriser la **dérivation** permet d'enrichir son vocabulaire de façon systématique.\n\n**Suffixes de noms** :\n- -tion/-ation (action) : *créer → création*\n- -ment (action) : *développer → développement*\n- -age (action) : *bricoler → bricolage*\n- -té/-ité (qualité) : *égal → égalité*\n- -eur/-euse (agent) : *travailler → travailleur/travailleuse*\n- -isme (doctrine) : *capital → capitalisme*\n\n**Préfixes** :\n- dé-/dés- (contraire) : *faire → défaire*\n- re-/ré- (répétition) : *faire → refaire*\n- sur- (au-dessus, excès) : *voler → survoler*\n- sous- (au-dessous) : *estimer → sous-estimer*",
        structure="préfixe + radical + suffixe",
        rules=[
            "La dérivation permet de créer des familles de mots.",
            "Connaître les suffixes permet de deviner le sens des mots inconnus.",
            "Attention aux faux amis de dérivation.",
        ],
        examples=[
            GrammarExample(
                text="créer → création, créateur, créatif, créativité, recréer",
                translation=None,
            ),
            GrammarExample(
                text="égal → égalité, inégal, inégalité, égaliser, égalitaire",
                translation=None,
            ),
            GrammarExample(
                text="faire → défaire, refaire, surfaire, parfaire, contrefaire",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="La créativité → La créativité",
                correct="La créativité.",
                note="'Créativité' est correct. Ne pas inventer de formes qui n'existent pas.",
            ),
        ],
        related=["champs-semantiques", "precision-lexicale"],
    ),
    GrammarTopic(
        slug="champs-semantiques",
        title="Les champs sémantiques",
        level="C1",
        category="Lexique",
        summary="Les réseaux de sens : synonymes, antonymes, hyperonymes, hyponymes, collocations.",
        explanation="Un **champ sémantique** est un ensemble de mots liés par le sens.\n\n**Synonymes partiels** : *maison, demeure, habitation, résidence, logement* (registres différents).\n**Hyperonymes** (général) / **Hyponymes** (spécifique) : *véhicule → voiture, camion, moto.*\n**Collocations** (mots qui vont naturellement ensemble) : *commettre une erreur, prendre une décision, dresser la table, griller un feu rouge.*\n\nMaîtriser les collocations est essentiel pour parler un français naturel.",
        structure="hyperonyme > hyponyme · mot + collocatif",
        rules=[
            "Les collocations sont des associations figées de mots.",
            "On ne peut pas traduire une collocation mot à mot.",
            "Apprendre le vocabulaire par champs sémantiques, pas par listes isolées.",
        ],
        examples=[
            GrammarExample(text="commettre une erreur (pas *faire une erreur)", translation=None),
            GrammarExample(text="prendre une décision (pas *faire une décision)", translation=None),
            GrammarExample(text="dresser la table / mettre la table", translation=None),
            GrammarExample(text="Il pleut à verse. (pas *Il pleut fortement)", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="faire une décision",
                correct="prendre une décision",
                note="La collocation correcte est 'prendre une décision'.",
            ),
            GrammarMistake(
                wrong="commettre un crime → faire un crime",
                correct="commettre un crime",
                note="C'est une collocation figée.",
            ),
        ],
        related=["derivation", "precision-lexicale"],
    ),
    GrammarTopic(
        slug="precision-lexicale",
        title="La précision lexicale",
        level="C1",
        category="Lexique",
        summary="Choisir le mot juste : éviter les approximations et les verbes 'passe-partout'.",
        explanation="En français avancé, on remplace les verbes 'passe-partout' par des verbes **précis**.\n\n| À éviter | Préférer |\n|----------|----------|\n| faire | effectuer, réaliser, accomplir, procéder à |\n| dire | affirmer, déclarer, indiquer, souligner, prétendre |\n| avoir | disposer de, bénéficier de, posséder |\n| être | se trouver, résider, consister en |\n| mettre | placer, déposer, installer, appliquer |\n| donner | fournir, accorder, octroyer, offrir |\n\nLe mot juste dépend du contexte et du registre.",
        structure="verbe précis au lieu de verbe générique",
        rules=[
            "Éviter les verbes trop génériques (faire, dire, avoir, être).",
            "Choisir le verbe qui exprime exactement l'action ou l'état.",
            "Le registre formel exige une précision lexicale élevée.",
        ],
        examples=[
            GrammarExample(
                text="Le gouvernement a procédé à une réforme.",
                translation=None,
                note="vs a fait une réforme",
            ),
            GrammarExample(
                text="L'étude révèle des inégalités persistantes.",
                translation=None,
                note="vs l'étude dit",
            ),
            GrammarExample(
                text="La solution réside dans le dialogue.",
                translation=None,
                note="vs la solution est",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Le président a fait un discours.",
                correct="Le président a prononcé un discours.",
                note="On 'prononce' un discours, on ne le 'fait' pas.",
            ),
        ],
        related=["champs-semantiques", "derivation", "registre-formel"],
    ),
    GrammarTopic(
        slug="ironie",
        title="L'ironie",
        level="C1",
        category="Expression",
        summary="Mécanismes de l'ironie en français : antiphrase, hyperbole, litote.",
        explanation="L'**ironie** consiste à dire le contraire de ce qu'on pense, tout en le laissant entendre.\n\n**Antiphrase** (dire le contraire) : *Quel temps magnifique !* (sous la pluie).\n**Hyperbole ironique** : *C'est génial, j'ai perdu mes clés !*\n**Litote** (dire moins pour faire entendre plus) : *Ce n'est pas faux.* (= c'est vrai)\n**Naïveté feinte** : *Ah bon ? Je ne savais pas que la Terre était ronde...*\n\nL'ironie repose sur le contexte et l'intonation. Elle peut être bienveillante ou mordante (sarcasme).",
        structure="dire A pour faire comprendre non-A",
        rules=[
            "L'ironie dépend du contexte et de l'intonation.",
            "Antiphrase = figure la plus courante de l'ironie.",
            "La litote atténue pour renforcer.",
            "Attention au sarcasme qui peut blesser.",
        ],
        examples=[
            GrammarExample(
                text="Bravo, tu as encore oublié ton rendez-vous !",
                translation=None,
                note="antiphrase",
            ),
            GrammarExample(text="Ce n'est pas la mer à boire. (litote)", translation=None),
            GrammarExample(text="Ah, tu t'es réveillé ? Il est midi ! (ironie)", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ironie mal comprise car l'intonation n'était pas marquée.",
                correct="À l'oral, l'ironie se marque par une intonation appuyée. À l'écrit, le contexte doit être clair.",
                note="L'ironie à l'écrit est risquée sans indicateurs contextuels.",
            ),
        ],
        related=["humour", "double-sens", "figures-rhetoriques"],
    ),
    GrammarTopic(
        slug="humour",
        title="L'humour en français",
        level="C1",
        category="Expression",
        summary="Ressorts de l'humour : jeux de mots, calembours, contrepèteries, autodérision.",
        explanation="L'**humour français** a un goût prononcé pour :\n\n**Jeux de mots** : *C'est l'histoire d'un pingouin qui respire par les fesses. Un jour, il s'assied et il meurt.*\n**Calembours** (homophonie) : *Le capitaine a bon pied, bon œil... et bon Porto ! (bon port)*\n**Contrepèteries** : inverser des sons (*femme folle à la messe →...*)\n**Autodérision** : se moquer de soi-même.\n**Absurde** : humour nonsensique (Devinette : Qu'est-ce qui est jaune et qui attend ? Jonathan).",
        structure="double sens, jeux sur les sons, décalage",
        rules=[
            "L'humour français valorise le jeu sur les mots.",
            "Le second degré est culturellement important.",
            "L'autodérision est appréciée socialement.",
        ],
        examples=[
            GrammarExample(
                text="Pourquoi le plombier n'a-t-il jamais faim ? Parce qu'il a toujours un tuyau.",
                translation=None,
                note="jeu de mots",
            ),
            GrammarExample(
                text="Je suis ponctuel : j'arrive toujours à l'heure... à laquelle je ne devrais pas.",
                translation=None,
                note="autodérision",
            ),
        ],
        common_mistakes=[],
        related=["ironie", "double-sens", "figures-rhetoriques"],
    ),
    GrammarTopic(
        slug="double-sens",
        title="Le double sens",
        level="C1",
        category="Expression",
        summary="Comprendre et produire des énoncés à double sens : sous-entendus, allusions, implicites.",
        explanation="Le **double sens** exploite la polysémie des mots pour créer une ambiguïté, humoristique ou rhétorique.\n\n**Sous-entendu** : sens implicite qui n'est pas dit ouvertement.\n- *Ce restaurant est... intéressant.* (= ce n'est pas bon)\n\n**Allusion** : référence indirecte.\n- *Après ce match, on a tous été un peu 'Zidane' !* (allusion au coup de tête de 2006)\n\n**Euphémisme** : atténuation.\n- *Il nous a quittés.* (= il est mort)",
        structure="mot/expression polysémique · sens littéral + sens implicite",
        rules=[
            "Le double sens repose sur la polysémie.",
            "Le contexte et l'intonation guident l'interprétation.",
            "Les sous-entendus sont très présents dans la communication française.",
        ],
        examples=[
            GrammarExample(
                text="Ce politicien a de l'avenir... derrière lui. (double sens)",
                translation=None,
            ),
            GrammarExample(
                text="Il est parti. (selon le contexte : il a quitté la pièce ou il est décédé)",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["ironie", "humour", "nuance"],
    ),
    GrammarTopic(
        slug="figures-rhetoriques",
        title="Les figures de rhétorique",
        level="C1",
        category="Expression",
        summary="Principales figures de style pour le discours persuasif.",
        explanation="Les **figures de rhétorique** structurent le discours persuasif :\n\n**Anaphore** : répéter un mot en début de phrase pour marteler.\n- *J'accuse... J'accuse... J'accuse...* (Zola)\n\n**Gradation** : progression dans l'intensité.\n- *Je suis déçu, consterné, révolté.*\n\n**Antithèse** : opposition de deux idées.\n- *C'est un petit pas pour l'homme, un bond de géant pour l'humanité.*\n\n**Question rhétorique** : fausse question.\n- *Peut-on rester indifférent face à une telle injustice ?*\n\n**Parallélisme** : structure syntaxique identique.\n- *Plus je regarde, moins je comprends.*",
        structure="figure de style + effet recherché",
        rules=[
            "L'anaphore martèle une idée.",
            "La question rhétorique engage l'auditoire.",
            "L'antithèse crée un contraste frappant.",
            "La gradation dramatise le propos.",
        ],
        examples=[
            GrammarExample(
                text="Moi, président, je serai exemplaire. Moi, président, je respecterai la parole donnée.",
                translation=None,
                note="anaphore",
            ),
            GrammarExample(
                text="Peut-on vraiment fermer les yeux sur cette situation ?",
                translation=None,
                note="question rhétorique",
            ),
            GrammarExample(
                text="Ils sont venus, ils ont vu, ils ont vaincu. (gradation et parallélisme)",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["persuasion", "art-oratoire", "structure-argumentative"],
    ),
    GrammarTopic(
        slug="persuasion",
        title="Les techniques de persuasion",
        level="C1",
        category="Expression",
        summary="Stratégies rhétoriques pour convaincre : logos, pathos, ethos.",
        explanation="La **persuasion** repose sur trois piliers aristotéliciens :\n\n**Logos** (logique) : arguments rationnels, faits, statistiques.\n- *Selon une étude de l'INSEE, 15% des Français...*\n\n**Pathos** (émotion) : faire appel aux sentiments.\n- *Pensez aux générations futures...*\n\n**Ethos** (crédibilité) : établir son autorité, montrer son expertise.\n- *Fort de vingt ans d'expérience dans ce domaine...*\n\nUn discours équilibré combine les trois.",
        structure="logos (raison) + pathos (émotion) + ethos (crédibilité)",
        rules=[
            "Logos = arguments factuels, preuves, logique.",
            "Pathos = appel à l'émotion, images fortes.",
            "Ethos = montrer sa légitimité à parler du sujet.",
        ],
        examples=[
            GrammarExample(
                text="D'après l'OMS, la pollution cause 7 millions de décès par an. Il est temps d'agir.",
                translation=None,
                note="logos",
            ),
            GrammarExample(
                text="Imaginez vos enfants grandir dans un monde sans forêts.",
                translation=None,
                note="pathos",
            ),
            GrammarExample(
                text="En tant que médecin urgentiste depuis quinze ans, je peux vous assurer que...",
                translation=None,
                note="ethos",
            ),
        ],
        common_mistakes=[],
        related=["figures-rhetoriques", "art-oratoire", "structure-argumentative"],
    ),
    GrammarTopic(
        slug="art-oratoire",
        title="L'art oratoire",
        level="C1",
        category="Expression",
        summary="Techniques pour structurer et délivrer un discours oral persuasif.",
        explanation="Un bon **discours oral** suit une structure claire :\n\n**1. Captatio benevolentiae** (accroche) : *Mesdames, Messieurs, je vous remercie de votre présence...*\n\n**2. Annonce du plan** : *J'aborderai trois points : d'abord..., ensuite..., enfin...*\n\n**3. Développement** : une idée par partie, transitions fluides.\n\n**4. Péroraison** (conclusion) : *Pour conclure, je dirais que... / En définitive...*\n\nUtiliser des pauses, varier le rythme, et regarder l'auditoire.",
        structure="accroche + annonce + développement + conclusion",
        rules=[
            "Toujours annoncer le plan.",
            "Une idée principale par partie.",
            "Soigner les transitions.",
            "Terminer par une phrase forte.",
        ],
        examples=[
            GrammarExample(
                text="Chers collègues, la question qui nous réunit aujourd'hui est cruciale.",
                translation=None,
                note="accroche",
            ),
            GrammarExample(
                text="Permettez-moi d'illustrer ce propos par un exemple concret.",
                translation=None,
                note="transition",
            ),
            GrammarExample(
                text="En définitive, c'est notre responsabilité collective qui est en jeu.",
                translation=None,
                note="péroraison",
            ),
        ],
        common_mistakes=[],
        related=["figures-rhetoriques", "persuasion", "structure-argumentative"],
    ),
    GrammarTopic(
        slug="francophonie",
        title="La francophonie",
        level="C1",
        category="Expression",
        summary="Introduction aux variétés du français dans le monde.",
        explanation="Le français est parlé sur tous les continents avec des **variétés** régionales riches.\n\n**Québec** : *magasiner* (faire du shopping), *char* (voiture), *achalant* (énervant), *blonde* (copine).\n\n**Belgique** : *septante, nonante* (70, 90), *une fois* (ponctuation orale), *dracher* (pleuvoir fort).\n\n**Suisse** : *septante, huitante, nonante*, *natel* (téléphone portable), *panosse* (serpillière).\n\n**Afrique subsaharienne** : *un maquis* (restaurant populaire en Côte d'Ivoire), *essencerie* (station-service).",
        structure="variété régionale = lexique + expressions + parfois syntaxe",
        rules=[
            "Toutes les variétés du français sont légitimes.",
            "Le lexique est la différence la plus visible.",
            "Certaines variétés ont des différences syntaxiques.",
            "Comprendre la diversité évite les malentendus.",
        ],
        examples=[
            GrammarExample(
                text="Au Québec : Je vais magasiner avec ma blonde.",
                translation=None,
                note="magasiner = faire du shopping",
            ),
            GrammarExample(
                text="En Belgique : Il drache ! On va goûter une fois.",
                translation=None,
            ),
            GrammarExample(text="En Suisse : Mon natel n'a plus de batterie.", translation=None),
            GrammarExample(
                text="Au Sénégal : On va à l'essencerie avant de partir.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["varietes-francais", "differences-regionales"],
    ),
    GrammarTopic(
        slug="varietes-francais",
        title="Les variétés du français",
        level="C1",
        category="Expression",
        summary="Approfondissement des différences entre le français hexagonal et les français du monde.",
        explanation="Au-delà du lexique, les variétés du français diffèrent par :\n\n**Prononciation** :\n- Québec : diphtongaison (*fête* → *faête*), affrication (*tu* → *tsu*).\n- Belgique : *w* prononcé /w/ (pas /v/).\n- Midi de la France : *e* caduc prononcé, voyelles nasales moins nasales.\n- Afrique : rythme syllabique marqué, influence des langues locales.\n\n**Syntaxe** :\n- Québec : *Tu veux-tu ?* (question), *ça fait du sens* (calque de 'makes sense').\n- Afrique : usage élargi de l'aspect progressif (*être en train de*).",
        structure="différences phonologiques, syntaxiques et lexicales",
        rules=[
            "Chaque variété a sa cohérence interne.",
            "La norme n'est pas unique.",
            "Comprendre la variation enrichit la compétence linguistique.",
        ],
        examples=[
            GrammarExample(
                text="Québec : Tu veux-tu aller au cinéma ?",
                translation=None,
                note="particule interrogative -tu",
            ),
            GrammarExample(
                text="Marseille : Eh bé ! Il fait chaud aujourd'hui, con !",
                translation=None,
            ),
            GrammarExample(
                text="Côte d'Ivoire : Il y a un maquis juste là, on y va ?",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["francophonie", "differences-regionales"],
    ),
    GrammarTopic(
        slug="differences-regionales",
        title="Différences régionales en France",
        level="C1",
        category="Expression",
        summary="Variétés régionales au sein de la France hexagonale.",
        explanation="Même au sein de la France hexagonale, il existe des **variations régionales** :\n\n**Nord** : *dracher* (pleuvoir), *biloute* (ami), *wassingue* (serpillière).\n**Est** : *schluck* (gorgée), *schatz* (chéri, alsacien).\n**Bretagne** : *kenavo* (au revoir, breton).\n**Sud** : *chocolatine* (pain au chocolat), *poche* (sac plastique), *tchatche* (parler).\n**Normandie** : *boujou* (bonjour/au revoir), *itou* (aussi).\n\nCes mots font partie du patrimoine linguistique et sont généralement compris dans le contexte.",
        structure="variation régionale = géographie + culture",
        rules=[
            "Le français standard est compris partout.",
            "Les régionalismes enrichissent la langue.",
            "La plupart sont du lexique (pas de différence syntaxique majeure).",
        ],
        examples=[
            GrammarExample(text="À Lille : Tiens, biloute, ça drache dehors !", translation=None),
            GrammarExample(
                text="À Toulouse : Tu veux une chocolatine ?",
                translation=None,
                note="pain au chocolat",
            ),
            GrammarExample(
                text="À Marseille : T'as vu cette tchatche, il est fort lui !",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["francophonie", "varietes-francais"],
    ),
    GrammarTopic(
        slug="synthese-textuelle",
        title="La synthèse textuelle",
        level="C1",
        category="Expression",
        summary="Techniques pour synthétiser plusieurs sources en un texte cohérent.",
        explanation="La **synthèse** est un exercice académique majeur en français (concours, examens).\n\n**Méthode** :\n1. **Lire et analyser** les documents sources.\n2. **Repérer** la problématique commune.\n3. **Confronter** les points de vue, sans les juxtaposer.\n4. **Reformuler** sans plagier.\n5. **Organiser** selon un plan thématique.\n\n**Ne pas** : donner son avis personnel, résumer document par document.\n\n**Marqueurs utiles** :\n- *Selon X..., Pour X..., D'après Y...*\n- *X affirme que..., Y contredit cette vision en soulignant que...*",
        structure="introduction problématisée + plan thématique + conclusion de synthèse",
        rules=[
            "Ne pas donner son avis personnel.",
            "Confronter les sources, ne pas les juxtaposer.",
            "Référencer chaque idée à son auteur.",
            "Plan thématique, pas plan par document.",
        ],
        examples=[
            GrammarExample(
                text="Si pour Durand la mondialisation est une opportunité, Martin y voit au contraire une menace pour les cultures locales.",
                translation=None,
            ),
            GrammarExample(
                text="Ces trois auteurs convergent sur un point : la nécessité de réguler les échanges.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["critique-constructive", "reformulation"],
    ),
    GrammarTopic(
        slug="critique-constructive",
        title="La critique constructive",
        level="C1",
        category="Expression",
        summary="Comment formuler une critique de façon constructive et argumentée.",
        explanation="Une **critique constructive** respecte une structure :\n\n**1. Points positifs** :\n- *Le point fort de cette approche est... / On peut saluer...*\n\n**2. Limites avec nuance** :\n- *Cependant, on peut regretter que... / Il est dommage que...*\n\n**3. Suggestions** :\n- *Il serait souhaitable de... / Une piste d'amélioration serait...*\n\n**4. Conclusion équilibrée** :\n- *En dépit de ces réserves, ce travail apporte... / Malgré ces limites...*\n\nUtiliser des **modalisateurs** : *peut-être, sans doute, il semble que, à mon sens...*",
        structure="positif + limites nuancées + suggestions + conclusion",
        rules=[
            "Toujours commencer par les points positifs.",
            "Nuancer la critique avec des modalisateurs.",
            "Proposer des alternatives, pas seulement pointer les problèmes.",
            "Terminer par une appréciation globale.",
        ],
        examples=[
            GrammarExample(
                text="L'analyse est rigoureuse. Toutefois, il aurait été intéressant d'élargir le corpus.",
                translation=None,
            ),
            GrammarExample(
                text="On peut saluer la clarté de l'exposé, même si certains aspects mériteraient d'être approfondis.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["synthese-textuelle", "reformulation", "structure-argumentative"],
    ),
    GrammarTopic(
        slug="reformulation",
        title="La reformulation",
        level="C1",
        category="Expression",
        summary="Techniques de paraphrase et de reformulation pour clarifier ou synthétiser.",
        explanation="**Reformuler**, c'est redire avec d'autres mots, sans changer le sens.\n\n**Pourquoi reformuler ?**\n- Vérifier la compréhension : *Si je comprends bien, vous voulez dire que...*\n- Clarifier : *Autrement dit..., En d'autres termes..., C'est-à-dire...*\n- Synthétiser : *En résumé..., Pour faire court..., Bref...*\n- Adapter le niveau de langue : expliquer un terme technique au grand public.\n\n**Technique** : repérer l'idée principale, trouver des synonymes, changer la structure syntaxique.",
        structure="idée source → connecteur de reformulation → idée reformulée",
        rules=[
            "Garder le sens exact, ne pas interpréter.",
            "Utiliser des connecteurs de reformulation.",
            "Changer la structure syntaxique.",
        ],
        examples=[
            GrammarExample(
                text="Si je vous ai bien compris, vous estimez que la réforme est prématurée.",
                translation=None,
            ),
            GrammarExample(
                text="La croissance démographique ralentit. En d'autres termes, la population augmente moins vite qu'avant.",
                translation=None,
            ),
            GrammarExample(
                text="Il souffre d'anosmie, c'est-à-dire qu'il a perdu l'odorat.",
                translation=None,
            ),
        ],
        common_mistakes=[],
        related=["synthese-textuelle", "critique-constructive"],
    ),
]
