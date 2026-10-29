"""French grammar topics — B2."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        slug="subjonctif-passe",
        title="Le subjonctif passé",
        level="B2",
        category="Verbes",
        summary="Le subjonctif passé pour exprimer l'antériorité dans le subjonctif.",
        explanation="Le **subjonctif passé** exprime une action antérieure dans un contexte qui exige le subjonctif.\n\n**Formation** : être/avoir au subjonctif présent + participe passé.\n\n- *Je suis content que tu **sois venu**.*\n- *Je doute qu'il **ait fini** à temps.*\n- *C'est dommage qu'elle **soit partie** sans dire au revoir.*\n\n**Quand l'utiliser ?**\n- Action passée par rapport au verbe principal.\n- Avec un verbe principal au présent : *Je regrette qu'il **ait menti**.*\n- Avec un verbe principal au passé (registre courant) : *Je regrettais qu'il **ait menti**.*",
        structure="être/avoir (subjonctif présent) + participe passé",
        rules=[
            "Action antérieure dans un contexte subjonctif.",
            "Mêmes règles d'accord que le passé composé.",
            "Le subjonctif passé remplace le passé composé au subjonctif.",
            "Registre courant : on garde le subjonctif présent même après un verbe au passé.",
        ],
        examples=[
            GrammarExample(text="Je suis content que tu sois venu.", translation=None),
            GrammarExample(text="Je doute qu'il ait compris la question.", translation=None),
            GrammarExample(
                text="C'est le meilleur film que j'aie jamais vu.",
                translation=None,
                note="superlatif + subjonctif",
            ),
            GrammarExample(text="Il est possible qu'elle se soit trompée.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Je suis content que tu es venu.",
                correct="Je suis content que tu sois venu.",
                note="Après 'content que', on utilise le subjonctif.",
            ),
            GrammarMistake(
                wrong="Je regrette qu'il a menti.",
                correct="Je regrette qu'il ait menti.",
                note="Regretter que appelle le subjonctif; le passé exprime l'antériorité.",
            ),
        ],
        related=[
            "subjonctif-conjonctions",
            "concordance-subjonctif",
            "subjonctif-present",
        ],
    ),
    GrammarTopic(
        slug="concordance-subjonctif",
        title="La concordance des temps au subjonctif",
        level="B2",
        category="Verbes",
        summary="Règles de concordance au subjonctif : présent, passé, imparfait, plus-que-parfait.",
        explanation="La **concordance des temps au subjonctif** dépend du temps du verbe principal :\n\n**Verbe principal au PRÉSENT / FUTUR** :\n- Antériorité → subjonctif passé : *Je veux que tu **aies fini** avant midi.*\n- Simultanéité → subjonctif présent : *Je veux que tu **viennes**.*\n\n**Verbe principal au PASSÉ (registre soutenu/littéraire)** :\n- Simultanéité → subjonctif imparfait : *Je voulais qu'il **vînt**.* (rare)\n- Antériorité → subjonctif plus-que-parfait : *Je doutais qu'il **fût venu**.* (très rare)\n\n**Registre courant** : on utilise le subjonctif présent/passé même après un verbe au passé.",
        structure="verbe principal + que + subjonctif (présent/passé en registre courant)",
        rules=[
            "Registre courant : subjonctif présent et passé suffisent.",
            "Subjonctif imparfait et plus-que-parfait = registre très soutenu/littéraire.",
            "Le subjonctif imparfait est quasi absent de l'oral contemporain.",
        ],
        examples=[
            GrammarExample(text="Il fallait que tu viennes. (courant)", translation=None),
            GrammarExample(text="Il fallait que tu vinsses. (littéraire, rare)", translation=None),
            GrammarExample(
                text="Je voulais qu'il ait terminé avant ce soir.",
                translation=None,
                note="subj. passé",
            ),
            GrammarExample(
                text="Je ne pensais pas qu'elle puisse le faire. (courant)",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Il fallait que tu viens.",
                correct="Il fallait que tu viennes.",
                note="Même après un verbe au passé, on utilise le subjonctif (présent en registre courant).",
            ),
        ],
        related=["subjonctif-present", "subjonctif-passe", "subjonctif-conjonctions"],
    ),
    GrammarTopic(
        slug="subjonctif-conjonctions",
        title="Le subjonctif après les conjonctions",
        level="B2",
        category="Verbes",
        summary="Les conjonctions qui exigent le subjonctif : bien que, pour que, avant que, etc.",
        explanation="Certaines **conjonctions de subordination** exigent le subjonctif :\n\n**Concession** : *bien que, quoique, encore que*\n- *Bien qu'il **pleuve**, je sors.*\n\n**But** : *pour que, afin que, de sorte que, de peur que*\n- *Je t'explique pour que tu **comprennes**.*\n\n**Temps** : *avant que, jusqu'à ce que, en attendant que*\n- *Attends avant qu'il ne **parte**.*\n\n**Condition** : *à condition que, pourvu que, à moins que*\n- *Tu peux sortir à condition que tu **aies** fini tes devoirs.*\n\n**Conjonctions + indicatif** (pièges) : *après que, parce que, puisque, alors que, pendant que, étant donné que.*",
        structure="conjonction + subjonctif",
        rules=[
            "Bien que, quoique → subjonctif (concession).",
            "Pour que, afin que → subjonctif (but).",
            "Avant que, jusqu'à ce que → subjonctif (temps).",
            "À condition que, à moins que → subjonctif (condition).",
            "Après que → indicatif (piège classique).",
        ],
        examples=[
            GrammarExample(text="Bien qu'il soit tard, je vais t'appeler.", translation=None),
            GrammarExample(text="Je répète pour que tout le monde comprenne.", translation=None),
            GrammarExample(text="Attends ici jusqu'à ce que je revienne.", translation=None),
            GrammarExample(
                text="Tu peux venir à condition que tu sois à l'heure.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Après qu'il soit parti.",
                correct="Après qu'il est parti.",
                note="'Après que' est suivi de l'indicatif, pas du subjonctif.",
            ),
            GrammarMistake(
                wrong="Bien que il est tard.",
                correct="Bien qu'il soit tard.",
                note="'Bien que' exige le subjonctif.",
            ),
        ],
        related=["subjonctif-present", "subjonctif-passe", "connecteurs-avances"],
    ),
    GrammarTopic(
        slug="gerondif",
        title="Le gérondif",
        level="B2",
        category="Verbes",
        summary="Le gérondif : en + participe présent pour exprimer la simultanéité, la manière, la cause.",
        explanation="Le **gérondif** se forme avec **en + participe présent** (radical de la 1re personne du pluriel + -ant).\n\n**Usages** :\n- **Simultanéité** : *Il travaille **en écoutant** de la musique.*\n- **Manière** : *Il est arrivé **en courant**.*\n- **Cause** : ***En prenant** le train, on arrive plus vite.*\n- **Condition** : *Tu réussiras **en travaillant** davantage.*\n\n**Tout + gérondif** = insistance sur la simultanéité : *Tout en conduisant, il téléphonait.*",
        structure="en + radical (nous au présent) + -ant",
        rules=[
            "Formation sur le radical de 'nous' au présent.",
            "Exprime la simultanéité, la manière, la cause ou la condition.",
            "Le sujet du gérondif doit être le même que celui du verbe principal.",
            "Tout en + gérondif pour marquer la simultanéité de deux actions contradictoires.",
        ],
        examples=[
            GrammarExample(text="J'écoute de la musique en travaillant.", translation=None),
            GrammarExample(
                text="Il est sorti en claquant la porte.",
                translation=None,
                note="manière",
            ),
            GrammarExample(
                text="En faisant du sport, on reste en forme.",
                translation=None,
                note="condition générale",
            ),
            GrammarExample(text="Tout en étant d'accord, je reste prudent.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Il est tombé en courrant.",
                correct="Il est tombé en courant.",
                note="'Courir' → participe présent : courant (un seul r).",
            ),
            GrammarMistake(
                wrong="En je travaillant.",
                correct="En travaillant.",
                note="Pas de pronom entre 'en' et le participe présent.",
            ),
        ],
        related=["participe-present", "participes-composes"],
    ),
    GrammarTopic(
        slug="participe-present",
        title="Le participe présent",
        level="B2",
        category="Verbes",
        summary="Le participe présent : forme en -ant utilisée comme adjectif ou proposition participiale.",
        explanation="Le **participe présent** se forme sur le radical de la 1re personne du pluriel + **-ant**.\n\n**Usages** :\n- **Adjectif verbal** (s'accorde) : *Une histoire **intéressante**, une journée **fatigante**.*\n- **Proposition participiale** (invariable, registre soutenu) : *Les enfants **ayant** moins de 12 ans ne paient pas.* / *Ne **sachant** pas quoi faire, il est parti.*\n\n**Différence** : l'adjectif verbal s'accorde, le participe présent non.\n- participe présent : *Les films **intéressant** les jeunes...* (invariable)\n- adjectif verbal : *des films **intéressants*** (s'accorde)",
        structure="radical (nous au présent) + -ant",
        rules=[
            "Invariable en tant que participe présent.",
            "S'accorde en tant qu'adjectif verbal.",
            "Registre soutenu en proposition participiale.",
            "Ne pas confondre avec le gérondif (en + participe présent).",
        ],
        examples=[
            GrammarExample(
                text="Les personnes ayant un billet peuvent entrer.",
                translation=None,
                note="participe présent, registre soutenu",
            ),
            GrammarExample(
                text="Ne sachant pas la réponse, j'ai gardé le silence.",
                translation=None,
            ),
            GrammarExample(
                text="C'est une histoire passionnante.",
                translation=None,
                note="adjectif verbal → accord",
            ),
            GrammarExample(
                text="Les employés travaillant de nuit ont une prime.", translation=None
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Une histoire passionante.",
                correct="Une histoire passionnante.",
                note="L'adjectif verbal de 'passionner' a deux n : passionnant.",
            ),
            GrammarMistake(
                wrong="Les personnes ayant un billet... → Les personnes ayantes...",
                correct="Les personnes ayant un billet...",
                note="Le participe présent est invariable.",
            ),
        ],
        related=["gerondif", "participes-composes"],
    ),
    GrammarTopic(
        slug="participes-composes",
        title="Les participes composés",
        level="B2",
        category="Verbes",
        summary="Les participes composés : ayant fait, étant arrivé... pour exprimer l'antériorité.",
        explanation="Le **participe passé composé** (ou participe composé) exprime une action accomplie antérieure à une autre action.\n\n**Formation** :\n- Participe présent de être/avoir + participe passé.\n- **Ayant** + participe passé (verbes avec avoir)\n- **Étant** + participe passé (verbes avec être)\n\n- ***Ayant fini** son travail, il est rentré chez lui.*\n- ***Étant arrivée** en retard, elle s'est excusée.*\n- ***S'étant réveillé** tôt, il a fait du sport.*\n\nCette structure est propre au registre soutenu et à l'écrit.",
        structure="ayant/étant + participe passé",
        rules=[
            "Exprime une action accomplie antérieure.",
            "Ayant pour les verbes avec avoir.",
            "Étant pour les verbes avec être, s'étant pour les pronominaux.",
            "Registre soutenu / écrit surtout.",
        ],
        examples=[
            GrammarExample(text="Ayant terminé son rapport, il est parti.", translation=None),
            GrammarExample(text="Étant arrivés en avance, nous avons attendu.", translation=None),
            GrammarExample(
                text="S'étant entraînée tous les jours, elle a gagné.", translation=None
            ),
            GrammarExample(text="N'ayant pas reçu de réponse, j'ai relancé.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Ayant fini son travail, il est parti. → Avoir fini..., il est parti.",
                correct="Ayant fini son travail, il est parti.",
                note="'Avoir fini' n'est pas une proposition participiale correcte.",
            ),
            GrammarMistake(
                wrong="Étant arrivé, elle s'est excusée. (sujet fém.)",
                correct="Étant arrivée, elle s'est excusée.",
                note="Avec 'étant', le participe passé s'accorde avec le sujet.",
            ),
        ],
        related=[
            "gerondif",
            "participe-present",
            "passe-compose-avoir",
            "passe-compose-etre",
        ],
    ),
    GrammarTopic(
        slug="connecteurs-avances",
        title="Les connecteurs avancés",
        level="B2",
        category="Expression",
        summary="Connecteurs sophistiqués pour l'écrit formel et l'argumentation.",
        explanation="**Pour l'écrit formel** :\n\n**Cause** : *en raison de, du fait de, étant donné que, sous prétexte que*\n- *Le vol a été annulé **en raison du** mauvais temps.*\n\n**Conséquence** : *si bien que, de sorte que, au point que, d'où*\n- *Il a beaucoup plu, **si bien que** la rivière a débordé.*\n\n**Opposition** : *en revanche, au contraire, à l'inverse*\n- *Le train est cher ; **en revanche**, il est rapide.*\n\n**Concession** : *certes... mais, il n'en reste pas moins que, toujours est-il que*\n- ***Certes**, il a raison, **mais** sa méthode est discutable.*",
        structure="connecteur + phrase / nom",
        rules=[
            "En raison de + nom, en raison du fait que + indicatif.",
            "Au point que + indicatif.",
            "Il n'en reste pas moins que = néanmoins (formel).",
            "Certes... mais = concession élégante.",
        ],
        examples=[
            GrammarExample(text="En raison des travaux, la route est fermée.", translation=None),
            GrammarExample(
                text="Il a tellement crié, au point que tout le monde s'est retourné.",
                translation=None,
            ),
            GrammarExample(
                text="Certes, le projet est ambitieux, mais il est réalisable.",
                translation=None,
            ),
            GrammarExample(
                text="Il n'en reste pas moins que des efforts restent à faire.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="En raison du mauvais temps, donc le vol est annulé.",
                correct="En raison du mauvais temps, le vol est annulé.",
                note="'En raison de' exprime déjà la cause, pas besoin de 'donc'.",
            ),
        ],
        related=["connecteurs-logiques", "structure-argumentative", "registre-formel"],
    ),
    GrammarTopic(
        slug="cohesion-textuelle",
        title="La cohésion textuelle",
        level="B2",
        category="Expression",
        summary="Techniques pour maintenir la cohésion d'un texte : anaphores, reprises, ellipses.",
        explanation="Pour qu'un texte soit **cohérent**, il faut éviter les répétitions en utilisant :\n\n**Reprises pronominales** :\n- *Marie est arrivée. **Elle** semblait fatiguée.*\n\n**Reprises nominales** (synonymes, hyperonymes) :\n- *Le **président** a parlé. Le **chef de l'État** a abordé plusieurs sujets.*\n\n**Ellipse** :\n- *Pierre a pris le train, Marie **∅** l'avion.* (a pris est sous-entendu)\n\n**Connecteurs** pour marquer les enchaînements : *d'une part... d'autre part, non seulement... mais aussi...*",
        structure="reprise pronominale, nominale, ellipse, connecteurs",
        rules=[
            "Éviter de répéter le même mot dans la même phrase.",
            "Alterner pronom, synonyme et ellipse.",
            "Les connecteurs guident le lecteur entre les idées.",
        ],
        examples=[
            GrammarExample(
                text="Le musée du Louvre est immense. Ce monument attire des millions de visiteurs chaque année.",
                translation=None,
                note="reprise nominale",
            ),
            GrammarExample(
                text="Paul aime le tennis ; Marie, le basket.",
                translation=None,
                note="ellipse",
            ),
            GrammarExample(
                text="Non seulement il est compétent, mais il est aussi très sympathique.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Le président a parlé. Le président a annoncé que le président allait...",
                correct="Le président a parlé. Il a annoncé que le chef de l'État allait...",
                note="Répéter 'le président' trois fois est lourd. Utiliser des reprises.",
            ),
        ],
        related=[
            "connecteurs-avances",
            "connecteurs-logiques",
            "structure-argumentative",
        ],
    ),
    GrammarTopic(
        slug="registre-formel",
        title="Le registre formel",
        level="B2",
        category="Expression",
        summary="Caractéristiques du registre formel à l'écrit : nominalisation, impersonnalité, vocabulaire soutenu.",
        explanation="Le **registre formel** (ou soutenu) s'utilise dans les écrits académiques, professionnels et administratifs.\n\n**Caractéristiques** :\n- **Nominalisation** : *Le développement des technologies...* (au lieu de 'les technologies se développent')\n- **Impersonnalité** : *Il convient de noter que... / On observera que...*\n- **Vocabulaire soutenu** : *effectuer* au lieu de *faire*, *solliciter* au lieu de *demander*\n- **Éviter** : le langage familier, les abréviations, le 'je' excessif.\n- **Négation complète** : *Je ne sais pas* (pas *Je sais pas*).",
        structure="nominalisations, tournures impersonnelles, vocabulaire soutenu",
        rules=[
            "Préférer les structures nominales aux verbales.",
            "Éviter le 'je' dans les écrits académiques.",
            "Utiliser le 'nous' de modestie ou des tournures impersonnelles.",
            "Proscrire le langage familier et les abréviations.",
        ],
        examples=[
            GrammarExample(
                text="L'augmentation du chômage a entraîné une baisse de la consommation.",
                translation=None,
                note="nominalisation",
            ),
            GrammarExample(
                text="Il convient de souligner l'importance de ce phénomène.",
                translation=None,
                note="impersonnel",
            ),
            GrammarExample(
                text="Les résultats de cette étude seront présentés ci-après.",
                translation=None,
            ),
            GrammarExample(
                text="Nous avons procédé à l'analyse des données recueillies.",
                translation=None,
                note="nous de modestie",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Y a plein de problèmes.",
                correct="Il existe de nombreux problèmes.",
                note="À l'écrit formel, on évite 'y a' et 'plein de'.",
            ),
        ],
        related=[
            "connecteurs-avances",
            "nominalisation",
            "impersonalite",
            "orthotypographie",
        ],
    ),
    GrammarTopic(
        slug="structure-argumentative",
        title="La structure argumentative",
        level="B2",
        category="Expression",
        summary="Comment structurer un texte argumentatif : thèse, arguments, exemples, concession, conclusion.",
        explanation="Un **texte argumentatif** bien structuré suit un plan précis :\n\n**1. Introduction** : présenter le sujet et annoncer la thèse.\n- *De nos jours, la question de... fait débat. Nous verrons que...*\n\n**2. Développement** :\n- Arguments pour : *Tout d'abord..., En premier lieu..., Par ailleurs...*\n- Exemples : *À titre d'exemple..., Ainsi..., C'est le cas de...*\n- Concession : *Certes..., mais... / Bien que... / Il est vrai que..., cependant...*\n\n**3. Conclusion** :\n- *En définitive..., Pour conclure..., Au terme de cette analyse...*",
        structure="introduction + arguments + exemples + concession + conclusion",
        rules=[
            "Annoncer le plan dans l'introduction.",
            "Chaque paragraphe = une idée.",
            "Utiliser des connecteurs variés.",
            "Toujours inclure une concession pour montrer la nuance.",
        ],
        examples=[
            GrammarExample(
                text="Tout d'abord, il faut reconnaître que cette mesure présente des avantages.",
                translation=None,
                note="argument",
            ),
            GrammarExample(
                text="Certes, cette solution est coûteuse. Cependant, elle reste la plus efficace.",
                translation=None,
                note="concession",
            ),
            GrammarExample(
                text="En définitive, il apparaît que la réforme est nécessaire.",
                translation=None,
                note="conclusion",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Je pense que c'est bien. Je pense aussi que c'est utile. Je pense donc que...",
                correct="Cette mesure est bénéfique. De plus, elle s'avère utile. Par conséquent...",
                note="Éviter les répétitions et utiliser des connecteurs variés.",
            ),
        ],
        related=["connecteurs-avances", "concession", "nuance", "registre-formel"],
    ),
    GrammarTopic(
        slug="concession",
        title="La concession",
        level="B2",
        category="Expression",
        summary="Structures pour exprimer la concession : bien que, quoique, encore que, quand bien même.",
        explanation="La **concession** permet de reconnaître un argument opposé avant de le dépasser.\n\n**Structures** :\n- **Bien que / Quoique + subjonctif** : *Bien qu'il pleuve, je sors.*\n- **Même si + indicatif** : *Même s'il pleut, je sortirai.*\n- **Encore que + subjonctif** (restriction) : *C'est bien, encore que ce soit un peu cher.*\n- **Quand bien même + conditionnel** (hypothèse extrême) : *Quand bien même il me supplierait, je refuserais.*\n- **Avoir beau + infinitif** : *Il a beau être intelligent, il manque de méthode.*",
        structure="connecteur de concession + subjonctif/indicatif/conditionnel",
        rules=[
            "Bien que + subjonctif.",
            "Même si + indicatif.",
            "Encore que + subjonctif (restriction).",
            "Quand bien même + conditionnel (concession hypothétique).",
            "Avoir beau + infinitif (concession avec insistance).",
        ],
        examples=[
            GrammarExample(
                text="Bien qu'il soit tard, je vais continuer à travailler.",
                translation=None,
            ),
            GrammarExample(text="Même s'il fait froid, je prendrai mon vélo.", translation=None),
            GrammarExample(
                text="Il a beau avoir de l'expérience, il commet encore des erreurs.",
                translation=None,
            ),
            GrammarExample(
                text="Quand bien même tu aurais raison, je ne changerais pas d'avis.",
                translation=None,
                note="extrême",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Bien qu'il est fatigué, il continue.",
                correct="Bien qu'il soit fatigué, il continue.",
                note="'Bien que' est toujours suivi du subjonctif.",
            ),
        ],
        related=["structure-argumentative", "subjonctif-conjonctions", "nuance"],
    ),
    GrammarTopic(
        slug="nuance",
        title="L'expression de la nuance",
        level="B2",
        category="Expression",
        summary="Modalisateurs et expressions pour nuancer son discours.",
        explanation="Pour nuancer son discours et éviter les affirmations trop catégoriques :\n\n**Probabilité / Incertitude** :\n- *Il se peut que / Il se pourrait que + subjonctif*\n- *Il semblerait que + subjonctif*\n- *Apparemment... / Visiblement...*\n\n**Atténuation** :\n- *Pour ainsi dire / en quelque sorte / si l'on peut dire*\n- *Je dirais que... / On pourrait penser que...*\n- *Dans une certaine mesure...*\n\n**Prudence académique** :\n- *Il semblerait que... / Il apparaît que... / Tout porte à croire que...*",
        structure="modalisateur + subjonctif/indicatif",
        rules=[
            "Nuancer = exprimer le degré de certitude.",
            "Conditionnel journalistique pour l'information non confirmée.",
            "Verbes modaux : devoir, pouvoir + infinitif pour la probabilité.",
        ],
        examples=[
            GrammarExample(text="Il se pourrait que nous ayons tort.", translation=None),
            GrammarExample(text="Cette solution est, pour ainsi dire, idéale.", translation=None),
            GrammarExample(
                text="Le président aurait démissionné. (conditionnel journalistique)",
                translation=None,
            ),
            GrammarExample(text="Il semblerait que la situation s'améliore.", translation=None),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Il se peut que c'est vrai.",
                correct="Il se peut que ce soit vrai.",
                note="'Il se peut que' est suivi du subjonctif.",
            ),
        ],
        related=["structure-argumentative", "concession", "subjonctif-doute"],
    ),
    GrammarTopic(
        slug="temps-narratifs",
        title="Les temps narratifs",
        level="B2",
        category="Expression",
        summary="Maîtrise des temps dans le récit littéraire : passé simple, imparfait, plus-que-parfait.",
        explanation="Dans le **récit littéraire** (écrit, soutenu), les temps s'organisent ainsi :\n\n**Premier plan (actions)** : **passé simple** (écrit) ou **passé composé** (oral).\n- *Il **entra**, **salua** l'assemblée et **prit** la parole.* (littéraire)\n\n**Arrière-plan (descriptions)** : **imparfait**.\n- *La salle **était** silencieuse. Il **faisait** sombre.*\n\n**Antériorité** : **plus-que-parfait**.\n- *Il **avait longtemps réfléchi** avant de prendre sa décision.*\n\nLe passé simple n'est utilisé qu'à l'écrit littéraire. À l'oral, on le remplace par le passé composé.",
        structure="passé simple (1er plan) · imparfait (arrière-plan) · plus-que-parfait (antériorité)",
        rules=[
            "Passé simple = équivalent écrit/littéraire du passé composé.",
            "On ne mélange pas passé simple et passé composé dans un même récit.",
            "Imparfait pour tout ce qui est description et contexte.",
            "Plus-que-parfait pour l'antériorité.",
        ],
        examples=[
            GrammarExample(
                text="Il ouvrit la porte, traversa le couloir et disparut dans la nuit.",
                translation=None,
                note="passé simple littéraire",
            ),
            GrammarExample(
                text="La lune éclairait faiblement le jardin.",
                translation=None,
                note="imparfait, description",
            ),
            GrammarExample(
                text="Il sortit. Il avait attendu ce moment toute sa vie.",
                translation=None,
                note="plus-que-parfait",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Il ouvrit la porte et il a disparu.",
                correct="Il ouvrit la porte et disparut.",
                note="Dans un même récit, on ne mélange pas passé simple et passé composé.",
            ),
        ],
        related=["imparfait", "passe-compose-vs-imparfait", "description-litteraire"],
    ),
    GrammarTopic(
        slug="description-litteraire",
        title="La description littéraire",
        level="B2",
        category="Expression",
        summary="Techniques pour écrire une description littéraire riche : adjectifs, métaphores, rythme.",
        explanation="Une bonne **description littéraire** enrichit le récit en créant une atmosphère.\n\n**Techniques** :\n- **Adjectifs précis et évocateurs** : *Une lumière **blafarde, crépusculaire, tamisée**...*\n- **Métaphores et comparaisons** : *Le ciel était comme un océan d'encre.*\n- **Rythme** : phrases longues pour le calme, courtes pour la tension.\n- **Sensations** (5 sens) : *L'odeur du pain chaud flottait dans la rue.*\n\nÉviter les adjectifs vagues : 'beau', 'bien', 'intéressant'.",
        structure="description = adjectifs précis + métaphores + sensations",
        rules=[
            "Utiliser des adjectifs précis et variés.",
            "Faire appel aux cinq sens.",
            "Varier le rythme des phrases.",
            "Créer des images (comparaisons, métaphores).",
        ],
        examples=[
            GrammarExample(
                text="Le soleil couchant embrasait les toits de cuivre et d'or.",
                translation=None,
            ),
            GrammarExample(
                text="Un vent glacial sifflait entre les branches dénudées.",
                translation=None,
            ),
            GrammarExample(
                text="L'air était lourd, chargé de l'odeur sucrée des jasmins.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="C'était un beau jardin avec de belles fleurs.",
                correct="Le jardin regorgeait de roses pourpres et de glycines parfumées.",
                note="Remplacer 'beau' par des adjectifs plus évocateurs.",
            ),
        ],
        related=["temps-narratifs", "imparfait"],
    ),
    GrammarTopic(
        slug="langage-journalistique",
        title="Le langage journalistique",
        level="B2",
        category="Expression",
        summary="Caractéristiques du style journalistique : phrases nominales, titres, discours rapporté.",
        explanation="Le **style journalistique** a des caractéristiques propres :\n\n**Titres** :\n- Économie de mots, ellipse du verbe : *Gouvernement : démission surprise du ministre.*\n- Présent de narration : *Un séisme frappe la région.* (pour un événement passé)\n- Infinitif à valeur d'annonce : *Réforme des retraites : le projet adopté.*\n\n**Corps de l'article** :\n- Phrases nominales : *Une décision qui a surpris tout le monde.*\n- Voix passive : *Le suspect a été arrêté hier.*\n- Discours rapporté : *Selon le ministre..., D'après les sources...*",
        structure="titres concis · présent de narration · discours rapporté · voix passive",
        rules=[
            "Titres : concision maximale, ellipse fréquente.",
            "Le présent peut exprimer le passé proche dans les titres.",
            "Utiliser la voix passive et les tournures impersonnelles.",
            "Attribuer les informations : 'selon X', 'd'après Y'.",
        ],
        examples=[
            GrammarExample(
                text="Le conseil des ministres a adopté hier la réforme.",
                translation=None,
            ),
            GrammarExample(
                text="Selon des sources proches du dossier, un accord aurait été trouvé.",
                translation=None,
                note="conditionnel journalistique",
            ),
            GrammarExample(
                text="Le suspect, arrêté mardi, a été placé en garde à vue.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Le ministre a dit que c'est bien.",
                correct="Le ministre a déclaré que la mesure était bénéfique.",
                note="Utiliser des verbes d'attribution précis : déclarer, affirmer, souligner.",
            ),
        ],
        related=["discours-rapporte", "concordance-temps", "passif"],
    ),
    GrammarTopic(
        slug="discours-rapporte",
        title="Le discours rapporté avancé",
        level="B2",
        category="Expression",
        summary="Maîtrise du discours rapporté : verbes introducteurs variés, concordance, conditionnel journalistique.",
        explanation="Pour rapporter un discours de façon élégante, il faut varier les **verbes introducteurs** et maîtriser les nuances.\n\n**Verbes neutres** : dire, déclarer, annoncer, indiquer, préciser.\n**Verbes interprétatifs** : affirmer, soutenir, prétendre (mise à distance), reconnaître, avouer, admettre, concéder.\n**Verbes de question** : demander, s'interroger sur, s'enquérir de.\n**Verbes d'ordre/conseil** : ordonner, exiger, recommander, conseiller, suggérer.\n\nLe choix du verbe introducteur colore l'information (neutre, sceptique, approbateur).",
        structure="sujet + verbe introducteur + que/si/de + discours rapporté",
        rules=[
            "Varier les verbes introducteurs pour éviter 'il a dit'.",
            "Le verbe introducteur peut exprimer un jugement implicite.",
            "Concordance des temps avec un verbe introducteur au passé.",
            "Conditionnel pour l'information non confirmée.",
        ],
        examples=[
            GrammarExample(
                text="Le porte-parole a indiqué que la situation était sous contrôle.",
                translation=None,
                note="neutre",
            ),
            GrammarExample(
                text="L'opposition prétend que la réforme est insuffisante.",
                translation=None,
                note="mise à distance",
            ),
            GrammarExample(
                text="Le directeur a reconnu que des erreurs avaient été commises.",
                translation=None,
            ),
            GrammarExample(
                text="Des témoins affirment que le bruit était assourdissant.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Il a dit qu'il a faim.",
                correct="Il a dit qu'il avait faim.",
                note="Concordance des temps : le présent devient imparfait.",
            ),
        ],
        related=[
            "concordance-temps",
            "langage-journalistique",
            "discours-indirect-passe",
        ],
    ),
    GrammarTopic(
        slug="expressions-idiomatiques",
        title="Les expressions idiomatiques françaises",
        level="B2",
        category="Lexique",
        summary="Comprendre et utiliser les expressions idiomatiques et le langage figuré en français.",
        explanation="Les **expressions idiomatiques** sont des locutions figées dont le sens n'est pas littéral. Elles sont très fréquentes en français quotidien.\n\n**Exemples courants** :\n- *Poser un lapin* = ne pas venir à un rendez-vous.\n- *Avoir le cafard* = être triste, déprimé.\n- *Donner sa langue au chat* = abandonner une devinette.\n- *Mettre son grain de sel* = intervenir sans être invité.\n- *Tomber dans les pommes* = s'évanouir.\n- *Avoir un chat dans la gorge* = être enroué.\n- *Ce n'est pas la mer à boire* = ce n'est pas si difficile.\n- *Être à cheval sur* = être très strict concernant.\n\n**Conseil** : ne pas traduire littéralement. Apprendre le sens global de chaque expression.",
        structure="expression figée → sens global, non littéral",
        rules=[
            "Ne pas traduire mot à mot les expressions idiomatiques.",
            "Elles sont figées : on ne peut pas changer les mots.",
            "Le registre est souvent familier ou courant.",
            "Très utiles pour comprendre les francophones natifs.",
        ],
        examples=[
            GrammarExample(
                text="Il m'a posé un lapin hier soir.",
                translation=None,
                note="pas venu au rendez-vous",
            ),
            GrammarExample(
                text="J'ai le cafard depuis son départ.",
                translation=None,
                note="je suis triste",
            ),
            GrammarExample(text="Allez, donne ta langue au chat !", translation=None),
            GrammarExample(
                text="Elle est à cheval sur la ponctuation.",
                translation=None,
                note="très stricte",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Donner sa langue au chien.",
                correct="Donner sa langue au chat.",
                note="Les expressions idiomatiques sont figées, on ne peut pas changer les mots.",
            ),
            GrammarMistake(
                wrong="Il m'a donné un lapin. (sens littéral)",
                correct="Il m'a posé un lapin. (sens idiomatique)",
                note="Le verbe est 'poser' dans cette expression.",
            ),
        ],
        related=["registre-formel"],
    ),
    GrammarTopic(
        slug="conditionnel-passe-avance",
        title="Le conditionnel passé — approfondissement",
        level="B2",
        category="Verbes",
        summary="Le conditionnel passé pour exprimer le regret, le reproche, l'hypothèse non réalisée et l'irréel du passé.",
        explanation="Le **conditionnel passé** exprime une action qui aurait pu se produire dans le passé mais qui ne s'est pas réalisée.\n\n**Formation** : être/avoir au conditionnel présent + participe passé.\n\n**Usages** :\n- **Regret** : *J'**aurais dû** étudier davantage.* / *Tu **aurais pu** me prévenir !*\n- **Reproche** : *Il **aurait fallu** que tu m'en parles plus tôt.*\n- **Hypothèse non réalisée** (irréel du passé) : *Si j'avais su, je **serais venu**.*\n- **Information non confirmée** (conditionnel journalistique au passé) : *L'accident **aurait fait** trois victimes.*\n\n**Avec 'si'** : si + plus-que-parfait → conditionnel passé.\n- *Si tu **avais écouté**, tu **aurais compris**.*",
        structure="être/avoir (conditionnel présent) + participe passé",
        rules=[
            "Action non réalisée dans le passé, souvent avec un sentiment de regret ou de reproche.",
            "Si + plus-que-parfait → conditionnel passé pour l'irréel du passé.",
            "Conditionnel journalistique au passé pour une information non confirmée.",
            "Avec les modaux : j'aurais dû, j'aurais pu, il aurait fallu.",
        ],
        examples=[
            GrammarExample(text="J'aurais voulu être un artiste.", translation=None),
            GrammarExample(
                text="Si j'avais eu plus de temps, j'aurais visité le musée.",
                translation=None,
                note="irréel du passé",
            ),
            GrammarExample(
                text="Tu aurais pu me le dire plus tôt !",
                translation=None,
                note="reproche",
            ),
            GrammarExample(
                text="Le ministre aurait démissionné hier soir.",
                translation=None,
                note="conditionnel journalistique au passé",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Si j'aurais su, je serais venu.",
                correct="Si j'avais su, je serais venu.",
                note="Après 'si', on n'utilise jamais le conditionnel. Si + plus-que-parfait.",
            ),
            GrammarMistake(
                wrong="J'aurais aimé que tu viens.",
                correct="J'aurais aimé que tu viennes.",
                note="Après 'j'aurais aimé que', on utilise le subjonctif.",
            ),
        ],
        related=[
            "conditionnel-present",
            "passe-compose-avoir",
            "passe-compose-etre",
            "nuance",
        ],
    ),
    GrammarTopic(
        slug="futur-anterieur",
        title="Le futur antérieur",
        level="B2",
        category="Verbes",
        summary="Le futur antérieur pour exprimer l'antériorité future et l'hypothèse sur un fait passé.",
        explanation="Le **futur antérieur** est un temps composé du futur qui exprime une action future accomplie avant une autre action future.\n\n**Formation** : être/avoir au futur simple + participe passé.\n\n**Usages** :\n- **Antériorité future** : *Quand tu **auras fini** tes devoirs, tu pourras sortir.*\n- **Fait accompli dans le futur** : *Dans deux ans, j'**aurai obtenu** mon diplôme.*\n- **Hypothèse sur un fait passé** : *Il n'est pas encore arrivé ; il **aura oublié** le rendez-vous.* (probabilité)\n- **Bilan prospectif** : *À la fin du mois, nous **aurons dépensé** tout le budget.*\n\n**Avec 'quand', 'lorsque', 'dès que', 'une fois que'** → futur antérieur dans la subordonnée.",
        structure="être/avoir (futur simple) + participe passé",
        rules=[
            "Action qui sera accomplie avant un moment futur.",
            "Dans une subordonnée de temps avec 'quand', 'lorsque', 'dès que' → futur antérieur.",
            "Peut exprimer une supposition sur un événement passé (valeur modale).",
            "Ne pas confondre avec le conditionnel passé pour l'hypothèse.",
        ],
        examples=[
            GrammarExample(
                text="Quand tu auras terminé ton assiette, tu pourras avoir du dessert.",
                translation=None,
                note="antériorité future",
            ),
            GrammarExample(
                text="Elle n'est pas encore là ; elle aura eu un empêchement.",
                translation=None,
                note="supposition",
            ),
            GrammarExample(
                text="Dès que nous serons arrivés, nous vous appellerons.",
                translation=None,
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Quand tu finiras, tu pourras sortir.",
                correct="Quand tu auras fini, tu pourras sortir.",
                note="Pour marquer l'antériorité, on utilise le futur antérieur, pas le futur simple.",
            ),
            GrammarMistake(
                wrong="Il aura oublié son rendez-vous ; donc il aurait dû venir.",
                correct="Il aura oublié son rendez-vous ; c'est pourquoi il n'est pas venu.",
                note="Ne pas confondre futur antérieur de supposition avec le conditionnel passé de reproche.",
            ),
        ],
        related=["futur-simple", "conditionnel-passe", "temps-narratifs"],
    ),
    GrammarTopic(
        slug="pronoms-doubles",
        title="Les pronoms doubles",
        level="B2",
        category="Pronoms",
        summary="L'ordre des pronoms compléments quand ils sont combinés et leur placement à l'impératif.",
        explanation="Quand deux **pronoms compléments** sont utilisés ensemble, leur ordre suit une règle fixe.\n\n**Ordre avant le verbe (déclaratif)** :\nme/te/se/nous/vous → le/la/les → lui/leur → y → en\n\n- *Il **me le** donne.* — *Elle **le lui** a expliqué.*\n- *Je **vous y** emmène.* — *Elle **lui en** a parlé.* — *Nous **y en** avons acheté.* (rare)\n\n**Ordre à l'impératif affirmatif** :\nle/la/les → moi/toi/nous/vous → lui/leur → y → en\n\n- *Donne-**le-moi** !* — *Apporte-**les-lui** !* — *Va-**t'en** !*\n- *Parle-**m'en** !* — *Emmène-**nous-y** !*\n\n**Impératif négatif** : retour à l'ordre déclaratif.\n- *Ne **me le** donne pas !* — *Ne **le lui** apporte pas !*",
        structure="déclaratif: me/te/se/nous/vous → le/la/les → lui/leur → y → en  |  impératif: le/la/les → moi/toi/nous/vous → lui/leur → y → en",
        rules=[
            "Avant le verbe, l'ordre est : sujet réfléchi/COI → COD → autre COI → y → en.",
            "À l'impératif affirmatif, le COD passe en première position.",
            "Moi/toi remplacent me/te à l'impératif affirmatif (sauf devant y/en → m'en, t'en).",
            "À l'impératif négatif, on reprend l'ordre déclaratif.",
        ],
        examples=[
            GrammarExample(text="Il me l'a offert pour mon anniversaire.", translation=None),
            GrammarExample(
                text="Donne-la-moi immédiatement !",
                translation=None,
                note="impératif affirmatif",
            ),
            GrammarExample(
                text="Elle lui en a parlé hier soir.",
                translation=None,
                note="lui + en",
            ),
            GrammarExample(
                text="Ne le leur dis pas encore.",
                translation=None,
                note="impératif négatif",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Donne-moi-le !",
                correct="Donne-le-moi !",
                note="À l'impératif, le COD (le) précède le COI (moi).",
            ),
            GrammarMistake(
                wrong="Il me lui présente.",
                correct="Il me le présente. / Il le lui présente.",
                note="On ne peut pas avoir deux pronoms COI de la même colonne (me et lui).",
            ),
        ],
        related=["pronoms-cod", "pronoms-coi", "pronoms-y-en", "ordre-pronoms"],
    ),
    GrammarTopic(
        slug="ne-expletif",
        title="Le ne explétif et les nuances de la négation",
        level="B2",
        category="Négation",
        summary="Le ne explétif (non négatif) et les nuances de la négation : ne...guère, ne...que, sans que.",
        explanation="Le **ne explétif** est un 'ne' facultatif qui n'exprime pas la négation. Il apparaît dans des contextes formels et n'est pas obligatoire, mais son usage témoigne d'une maîtrise avancée.\n\n**Contextes du 'ne' explétif** :\n- Après **avant que** : *Dépêche-toi avant qu'il ne **pleuve**.*\n- Après **à moins que** : *À moins que tu ne **veuilles** m'aider...*\n- Après **sans que** : *Il est parti sans qu'on ne **s'en aperçoive**.*\n- Comparaison d'inégalité : *C'est plus difficile qu'il ne **semble**.*\n- Verbes de crainte (craindre que, avoir peur que) : *Je crains qu'il ne **soit** trop tard.*\n\n**Nuances de la négation** :\n- **ne...guère** = peu, presque pas (soutenu) : *Il n'est guère bavard.*\n- **ne...que** = seulement : *Je n'ai que dix euros.*\n- **sans que + (ne) + subjonctif** : concession nuancée.",
        structure="ne explétif devant verbe au subjonctif (facultatif)  |  ne...guère / ne...que / sans que",
        rules=[
            "Le 'ne' explétif est facultatif et ne nie pas.",
            "Il apparaît après avant que, à moins que, sans que, et avec les verbes de crainte.",
            "Ne...guère exprime une quantité ou intensité faible (= pas beaucoup).",
            "Ne...que exprime la restriction (= seulement).",
        ],
        examples=[
            GrammarExample(
                text="Dépêchons-nous avant qu'il ne soit trop tard.",
                translation=None,
                note="ne explétif",
            ),
            GrammarExample(
                text="Il a réussi sans que personne ne l'aide.",
                translation=None,
                note="ne explétif après 'sans que'",
            ),
            GrammarExample(
                text="Ce n'est guère étonnant vu les circonstances.",
                translation=None,
                note="ne...guère",
            ),
            GrammarExample(
                text="Elle n'a que vingt ans et déjà tant d'expérience.",
                translation=None,
                note="ne...que = seulement",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="Avant qu'il part, appelle-moi.",
                correct="Avant qu'il parte, appelle-moi. / Avant qu'il ne parte, appelle-moi.",
                note="'Avant que' exige le subjonctif. Le 'ne' explétif est facultatif.",
            ),
            GrammarMistake(
                wrong="Il n'a guère d'argent donc il en a beaucoup.",
                correct="Il n'a guère d'argent donc il en a très peu.",
                note="'Ne...guère' signifie 'presque pas', pas 'beaucoup'.",
            ),
        ],
        related=["subjonctif-conjonctions", "registre-formel"],
    ),
    GrammarTopic(
        slug="relatifs-composes",
        title="Les pronoms relatifs composés",
        level="B2",
        category="Pronoms",
        summary="Les pronoms relatifs composés : lequel, laquelle, lesquels, lesquelles, auquel, duquel et leur distinction avec qui/que/dont/où.",
        explanation="Les **pronoms relatifs composés** sont formés de l'article défini + -quel. Ils remplacent les relatifs simples dans certains contextes pour lever une ambiguïté ou après une préposition.\n\n**Formes** :\n- Masculin singulier : **lequel** / **auquel** (à + lequel) / **duquel** (de + lequel)\n- Féminin singulier : **laquelle** / **à laquelle** / **de laquelle**\n- Masculin pluriel : **lesquels** / **auxquels** / **desquels**\n- Féminin pluriel : **lesquelles** / **auxquelles** / **desquelles**\n\n**Quand les utiliser ?**\n- **Après une préposition** : *La table sur **laquelle** j'ai posé mon livre.*\n- **Avec une préposition locative** : *La ville dans **laquelle** j'habite.*\n- **Pour lever l'ambiguïté sur l'antécédent** : *Le fils de ma voisine, **lequel** habite à Lyon...*\n- **Parmi + lesquels** : *Trois candidats, parmi **lesquels** figure...*\n\n**Distinction** :\n- *Qui* = sujet / *Que* = COD / *Dont* = de + antécédent / *Où* = lieu/temps\n- Composés = après préposition (surtout composée), antécédent ambigu, registre soutenu.",
        structure="préposition + lequel/laquelle/lesquels/lesquelles (avec contractions : auquel, duquel, etc.)",
        rules=[
            "Après une préposition (sur, dans, avec, à, de, etc.) on utilise les relatifs composés.",
            "Auquel = à + lequel ; duquel = de + lequel.",
            "Parmi + lesquels/lesquelles pour sélectionner dans un ensemble.",
            "Peut remplacer 'qui' quand l'antécédent est ambigu.",
        ],
        examples=[
            GrammarExample(
                text="C'est une question à laquelle je n'ai pas de réponse.",
                translation=None,
                note="à + laquelle",
            ),
            GrammarExample(
                text="Les documents sur lesquels nous travaillons sont confidentiels.",
                translation=None,
                note="sur + lesquels",
            ),
            GrammarExample(
                text="L'ami de mon frère, lequel est médecin, nous a conseillés.",
                translation=None,
                note="levée d'ambiguïté",
            ),
            GrammarExample(
                text="Plusieurs raisons, parmi lesquelles le coût, expliquent ce choix.",
                translation=None,
                note="parmi lesquelles",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                wrong="C'est le problème à qui je pense.",
                correct="C'est le problème auquel je pense.",
                note="Après 'à', on utilise 'auquel/à laquelle', pas 'à qui' pour un inanimé.",
            ),
            GrammarMistake(
                wrong="La réunion dans qui j'étais.",
                correct="La réunion dans laquelle j'étais.",
                note="Après une préposition, 'qui' est réservé aux personnes dans le registre courant.",
            ),
        ],
        related=["registre-formel", "cohesion-textuelle"],
    ),
]
