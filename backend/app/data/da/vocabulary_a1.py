"""Danish A1 vocabulary with concrete definitions and everyday examples."""

from app.data._types import VocabularyEntry, VocabularySet

A1_SETS: list[VocabularySet] = [
    VocabularySet(
        "da_identity_a1",
        "A1",
        "Navn, sprog og kontakt",
        "a1-unit-1",
        [
            VocabularyEntry(
                "hej",
                "phrase",
                "En almindelig hilsen, når man møder nogen.",
                "Hej, jeg hedder Noor.",
            ),
            VocabularyEntry(
                "farvel", "phrase", "En hilsen, når man går fra nogen.", "Farvel, og tak for i dag."
            ),
            VocabularyEntry(
                "tak",
                "phrase",
                "Et ord, der viser, at man er glad for noget, man får.",
                "Tak for hjælpen.",
            ),
            VocabularyEntry(
                "undskyld",
                "phrase",
                "Et ord, man bruger for at beklage eller få kontakt.",
                "Undskyld, hvad hedder du?",
            ),
            VocabularyEntry(
                "ja", "adverb", "Et svar, der bekræfter det, der spørges om.", "Ja, jeg bor her."
            ),
            VocabularyEntry(
                "nej",
                "adverb",
                "Et negativt svar eller et ord, man bruger til at sige fra.",
                "Nej, jeg er ikke lærer.",
            ),
            VocabularyEntry(
                "et navn", "noun", "Det ord, en person eller ting kaldes.", "Mit navn er Emil."
            ),
            VocabularyEntry("hedde", "verb", "Have et bestemt navn.", "Hvad hedder din ven?"),
            VocabularyEntry(
                "være",
                "verb",
                "Have en bestemt egenskab, rolle eller tilstand.",
                "Jeg er studerende.",
            ),
            VocabularyEntry("bo", "verb", "Have sit hjem et bestemt sted.", "Vi bor i Aalborg."),
            VocabularyEntry(
                "komme", "verb", "Bevæge sig til et sted eller ankomme.", "Hun kommer klokken ni."
            ),
            VocabularyEntry(
                "et land",
                "noun",
                "Et område med egne grænser og en stat.",
                "Danmark er et lille land.",
            ),
            VocabularyEntry(
                "en by",
                "noun",
                "Et sted med mange huse, gader og mennesker.",
                "Odense er en by på Fyn.",
            ),
            VocabularyEntry(
                "et sprog",
                "noun",
                "Ord og regler, som mennesker bruger til at tale sammen.",
                "Hvilke sprog taler du?",
            ),
            VocabularyEntry(
                "dansk", "noun", "Sproget, der blandt andet tales i Danmark.", "Jeg lærer dansk."
            ),
            VocabularyEntry(
                "tale", "verb", "Bruge stemmen til at sige ord.", "Vi taler dansk på kurset."
            ),
            VocabularyEntry(
                "forstå", "verb", "Vide, hvad noget betyder.", "Jeg forstår dit spørgsmål."
            ),
            VocabularyEntry(
                "lytte",
                "verb",
                "Prøve at høre og følge en lyd eller en samtale.",
                "Lyt til navnet.",
            ),
            VocabularyEntry(
                "læse", "verb", "Se skrevne ord og forstå dem.", "Jeg læser en kort tekst."
            ),
            VocabularyEntry(
                "skrive",
                "verb",
                "Lave bogstaver og ord på papir eller en skærm.",
                "Skriv dit navn her.",
            ),
            VocabularyEntry(
                "en adresse",
                "noun",
                "Oplysninger om, hvor nogen bor eller noget ligger.",
                "Hvad er din adresse?",
            ),
            VocabularyEntry(
                "et telefonnummer",
                "noun",
                "Tal, man bruger for at ringe til en telefon.",
                "Kan du skrive dit telefonnummer?",
            ),
            VocabularyEntry("et bogstav", "noun", "Et tegn i alfabetet.", "Ø er et dansk bogstav."),
            VocabularyEntry(
                "et spørgsmål",
                "noun",
                "Noget, man siger for at få noget at vide.",
                "Jeg har et spørgsmål.",
            ),
            VocabularyEntry(
                "et svar",
                "noun",
                "Det, man siger eller skriver til et spørgsmål.",
                "Tak for dit svar.",
            ),
            VocabularyEntry(
                "lære",
                "verb",
                "Få ny viden eller blive i stand til at gøre noget.",
                "Vi lærer nye ord.",
            ),
            VocabularyEntry(
                "gentage", "verb", "Sige eller gøre det samme igen.", "Kan du gentage dit navn?"
            ),
            VocabularyEntry("langsomt", "adverb", "Uden høj fart.", "Tal langsomt, tak."),
        ],
    ),
    VocabularySet(
        "da_people_a1",
        "A1",
        "Mennesker og ting derhjemme",
        "a1-unit-2",
        [
            VocabularyEntry(
                "en familie",
                "noun",
                "Mennesker, der er knyttet sammen som børn, forældre eller andre nære slægtninge.",
                "Min familie bor i Aarhus.",
            ),
            VocabularyEntry(
                "en mor", "noun", "En kvinde, der er forælder.", "Min mor hedder Anne."
            ),
            VocabularyEntry("en far", "noun", "En mand, der er forælder.", "Min far arbejder her."),
            VocabularyEntry(
                "en søster",
                "noun",
                "En pige eller kvinde, man har en eller flere forældre fælles med.",
                "Min søster bor i Ribe.",
            ),
            VocabularyEntry(
                "en bror",
                "noun",
                "En dreng eller mand, man har en eller flere forældre fælles med.",
                "Jeg har en bror.",
            ),
            VocabularyEntry(
                "et barn",
                "noun",
                "Et ungt menneske, der endnu ikke er voksent.",
                "Barnet læser en bog.",
            ),
            VocabularyEntry(
                "en forælder",
                "noun",
                "En person, der har et barn.",
                "En forælder kommer med til mødet.",
            ),
            VocabularyEntry(
                "en ven",
                "noun",
                "En person, man holder af og gerne er sammen med.",
                "Det er min ven Ali.",
            ),
            VocabularyEntry(
                "en nabo", "noun", "En person, der bor tæt på ens hjem.", "Vores nabo hedder Lise."
            ),
            VocabularyEntry(
                "en kollega",
                "noun",
                "En person, man arbejder sammen med.",
                "Min kollega taler dansk.",
            ),
            VocabularyEntry(
                "en person", "noun", "Et enkelt menneske.", "Der er fire personer i rummet."
            ),
            VocabularyEntry(
                "en kvinde",
                "noun",
                "Et voksent menneske af hunkøn.",
                "Kvinden ved døren er min lærer.",
            ),
            VocabularyEntry(
                "en mand", "noun", "Et voksent menneske af hankøn.", "Manden hedder Peter."
            ),
            VocabularyEntry(
                "et hjem",
                "noun",
                "Det sted, hvor man bor og har sin hverdag.",
                "Vi har et lille hjem.",
            ),
            VocabularyEntry(
                "et hus", "noun", "En bygning, man kan bo eller arbejde i.", "Huset er gult."
            ),
            VocabularyEntry(
                "et værelse",
                "noun",
                "Et rum i en bolig, for eksempel til at sove i.",
                "Mit værelse er lyst.",
            ),
            VocabularyEntry(
                "et bord",
                "noun",
                "Et møbel med en flade, man kan spise eller arbejde ved.",
                "Bogen ligger på bordet.",
            ),
            VocabularyEntry(
                "en stol",
                "noun",
                "Et møbel, som én person kan sidde på.",
                "Her er en stol til dig.",
            ),
            VocabularyEntry("en seng", "noun", "Et møbel, man sover i.", "Sengen er stor."),
            VocabularyEntry(
                "en dør", "noun", "En del af en væg, man kan åbne og gå igennem.", "Døren er åben."
            ),
            VocabularyEntry(
                "et vindue",
                "noun",
                "En åbning med glas, der giver lys i et rum.",
                "Der er to vinduer.",
            ),
            VocabularyEntry(
                "en nøgle", "noun", "En lille ting, der kan åbne en lås.", "Hvor er min nøgle?"
            ),
            VocabularyEntry(
                "en taske", "noun", "Noget, man kan bære sine ting i.", "Min taske er sort."
            ),
            VocabularyEntry(
                "en bog",
                "noun",
                "Skrevne eller trykte sider, der er samlet.",
                "Jeg læser en god bog.",
            ),
            VocabularyEntry("stor", "adjective", "Som fylder meget.", "Vi har et stort bord."),
            VocabularyEntry("lille", "adjective", "Som fylder lidt.", "Det er et lille værelse."),
            VocabularyEntry(
                "ny",
                "adjective",
                "Som kun har eksisteret eller været brugt i kort tid.",
                "Jeg har en ny taske.",
            ),
            VocabularyEntry(
                "gammel", "adjective", "Som har eksisteret i lang tid.", "Min stol er gammel."
            ),
        ],
    ),
    VocabularySet(
        "da_routines_a1",
        "A1",
        "Dage, tider og rutiner",
        "a1-unit-3",
        [
            VocabularyEntry(
                "en dag",
                "noun",
                "En periode på et døgn eller den lyse del af døgnet.",
                "Jeg arbejder fem dage om ugen.",
            ),
            VocabularyEntry(
                "en morgen",
                "noun",
                "Den første del af dagen, når man normalt står op.",
                "Jeg læser om morgenen.",
            ),
            VocabularyEntry(
                "en formiddag",
                "noun",
                "Tiden mellem morgen og middag.",
                "Vi har dansk om formiddagen.",
            ),
            VocabularyEntry(
                "middag",
                "noun",
                "Tiden omkring klokken tolv om dagen; også et hovedmåltid.",
                "Vi mødes ved middagstid.",
            ),
            VocabularyEntry(
                "en eftermiddag",
                "noun",
                "Tiden mellem middag og aften.",
                "Jeg arbejder om eftermiddagen.",
            ),
            VocabularyEntry(
                "en aften", "noun", "Den sidste del af dagen før natten.", "Vi ses i aften."
            ),
            VocabularyEntry(
                "en nat",
                "noun",
                "Den mørke del af døgnet, hvor mange sover.",
                "Jeg sover om natten.",
            ),
            VocabularyEntry(
                "en uge", "noun", "En periode på syv dage.", "Kurset starter næste uge."
            ),
            VocabularyEntry(
                "mandag", "noun", "Ugedagen efter søndag og før tirsdag.", "Jeg arbejder mandag."
            ),
            VocabularyEntry(
                "tirsdag", "noun", "Ugedagen mellem mandag og onsdag.", "Vi har dansk tirsdag."
            ),
            VocabularyEntry(
                "onsdag", "noun", "Ugedagen mellem tirsdag og torsdag.", "Hun kommer onsdag."
            ),
            VocabularyEntry(
                "torsdag", "noun", "Ugedagen mellem onsdag og fredag.", "Jeg er hjemme torsdag."
            ),
            VocabularyEntry(
                "fredag", "noun", "Ugedagen mellem torsdag og lørdag.", "Vi mødes fredag."
            ),
            VocabularyEntry(
                "lørdag",
                "noun",
                "Ugedagen mellem fredag og søndag.",
                "Butikken åbner klokken ti lørdag.",
            ),
            VocabularyEntry(
                "søndag", "noun", "Ugedagen mellem lørdag og mandag.", "Jeg sover længe søndag."
            ),
            VocabularyEntry(
                "en weekend",
                "noun",
                "Lørdag og søndag, ofte med fredag aften.",
                "Hvad laver du i weekenden?",
            ),
            VocabularyEntry(
                "et ur", "noun", "En ting, der viser, hvad klokken er.", "Mit ur viser halv otte."
            ),
            VocabularyEntry(
                "en time", "noun", "En periode på tres minutter.", "Turen tager en time."
            ),
            VocabularyEntry(
                "et minut", "noun", "En periode på tres sekunder.", "Turen tager kun et minut."
            ),
            VocabularyEntry(
                "i dag", "adverb", "På den dag, der er nu.", "I dag arbejder jeg hjemme."
            ),
            VocabularyEntry("i morgen", "adverb", "På dagen efter i dag.", "Vi ses i morgen."),
            VocabularyEntry("i går", "adverb", "På dagen før i dag.", "Taler du om i går?"),
            VocabularyEntry(
                "arbejde",
                "verb",
                "Udføre opgaver, ofte som et job.",
                "Hun arbejder på et hospital.",
            ),
            VocabularyEntry(
                "stå op", "phrase", "Forlade sengen efter søvn.", "Jeg står op klokken syv."
            ),
            VocabularyEntry(
                "spise", "verb", "Tage mad ind i munden og synke den.", "Vi spiser klokken seks."
            ),
            VocabularyEntry("drikke", "verb", "Tage væske ind gennem munden.", "Jeg drikker vand."),
            VocabularyEntry(
                "sove", "verb", "Hvile med lukkede øjne uden at være vågen.", "Barnet sover nu."
            ),
            VocabularyEntry(
                "begynde",
                "verb",
                "Gå i gang eller have sit første tidspunkt.",
                "Lektionen begynder klokken ni.",
            ),
        ],
    ),
    VocabularySet(
        "da_food_a1",
        "A1",
        "Mad, drikke og priser",
        "a1-unit-4",
        [
            VocabularyEntry(
                "et brød",
                "noun",
                "Mad bagt af dej, ofte skåret i skiver.",
                "Jeg køber et brød hos bageren.",
            ),
            VocabularyEntry(
                "rugbrød",
                "noun",
                "Mørkt brød med rugmel, ofte med kerner.",
                "Jeg spiser rugbrød til frokost.",
            ),
            VocabularyEntry(
                "en bolle", "noun", "Et lille rundt stykke brød.", "En bolle med ost, tak."
            ),
            VocabularyEntry(
                "smør",
                "noun",
                "Fedt fra mælk, som man blandt andet smører på brød.",
                "Vil du have smør på brødet?",
            ),
            VocabularyEntry(
                "ost",
                "noun",
                "En fast eller blød madvare lavet af mælk.",
                "Jeg vil gerne have lidt ost.",
            ),
            VocabularyEntry(
                "mælk", "noun", "En hvid drik, blandt andet fra køer.", "Der er mælk i køleskabet."
            ),
            VocabularyEntry(
                "vand", "noun", "Den klare væske, man blandt andet drikker.", "Et glas vand, tak."
            ),
            VocabularyEntry(
                "kaffe",
                "noun",
                "En drik lavet af ristede bønner og vand.",
                "Jeg drikker kaffe om morgenen.",
            ),
            VocabularyEntry(
                "te", "noun", "En drik lavet af blade og varmt vand.", "Vil du have en kop te?"
            ),
            VocabularyEntry(
                "et æg",
                "noun",
                "En madvare med skal, hvide og blomme, ofte fra en høne.",
                "Vi skal bruge to æg.",
            ),
            VocabularyEntry(
                "en fisk",
                "noun",
                "Et dyr, der lever i vand og har gæller.",
                "Vi spiser fisk i aften.",
            ),
            VocabularyEntry(
                "kød", "noun", "De dele af et dyr, som man spiser.", "Jeg spiser ikke kød."
            ),
            VocabularyEntry(
                "en kylling",
                "noun",
                "En ung høne eller hane, også brugt som mad.",
                "Vi køber en kylling til aftensmad.",
            ),
            VocabularyEntry(
                "en kartoffel",
                "noun",
                "En spiselig knold, der vokser i jorden.",
                "Kartoflerne er varme.",
            ),
            VocabularyEntry(
                "en gulerod",
                "noun",
                "En lang, ofte orange rod, man kan spise.",
                "Jeg skærer en gulerod.",
            ),
            VocabularyEntry(
                "et æble", "noun", "En rund frugt med kerner i midten.", "Æblet er rødt."
            ),
            VocabularyEntry(
                "en banan",
                "noun",
                "En lang frugt med en skal, der ofte er gul.",
                "Barnet spiser en banan.",
            ),
            VocabularyEntry(
                "salt",
                "noun",
                "Små krystaller, som findes i havvand og bruges til at give mad smag.",
                "Der er for meget salt i suppen.",
            ),
            VocabularyEntry(
                "sukker",
                "noun",
                "Et sødt stof, som bruges i mad og drikke.",
                "Jeg vil ikke have sukker i kaffen.",
            ),
            VocabularyEntry("mad", "noun", "Det, mennesker og dyr spiser.", "Maden er klar."),
            VocabularyEntry(
                "morgenmad", "noun", "Dagens første måltid.", "Jeg spiser morgenmad klokken syv."
            ),
            VocabularyEntry(
                "frokost", "noun", "Et måltid midt på dagen.", "Vi holder frokost klokken tolv."
            ),
            VocabularyEntry(
                "aftensmad", "noun", "Et måltid sidst på dagen.", "Hvad skal vi have til aftensmad?"
            ),
            VocabularyEntry(
                "en butik",
                "noun",
                "Et sted, hvor man kan købe varer.",
                "Butikken lukker klokken otte.",
            ),
            VocabularyEntry(
                "en bager",
                "noun",
                "En person, der bager og ofte sælger brød og kager.",
                "Jeg køber boller hos bageren.",
            ),
            VocabularyEntry(
                "en pris",
                "noun",
                "Det beløb, man skal betale for noget.",
                "Hvad er prisen på brødet?",
            ),
            VocabularyEntry(
                "en krone",
                "noun",
                "Den danske pengeenhed; én svarer til hundrede øre.",
                "Bollen koster tolv kroner.",
            ),
            VocabularyEntry(
                "købe", "verb", "Få noget ved at betale for det.", "Jeg køber æbler og mælk."
            ),
        ],
    ),
    VocabularySet(
        "da_neighbourhood_a1",
        "A1",
        "Hjemmet, byen og transport",
        "a1-unit-5",
        [
            VocabularyEntry(
                "en lejlighed",
                "noun",
                "En bolig med egne rum i en større bygning.",
                "Vi bor i en lejlighed.",
            ),
            VocabularyEntry(
                "et køkken", "noun", "Et rum, hvor man laver mad.", "Der er et bord i køkkenet."
            ),
            VocabularyEntry(
                "et badeværelse",
                "noun",
                "Et rum, hvor man kan vaske sig.",
                "Badeværelset ligger ved siden af køkkenet.",
            ),
            VocabularyEntry(
                "en stue",
                "noun",
                "Et rum i hjemmet, hvor man ofte slapper af.",
                "Vi sidder i stuen.",
            ),
            VocabularyEntry(
                "et toilet",
                "noun",
                "En kumme, man bruger til at tisse eller have afføring i; også rummet med kummen.",
                "Hvor er toilettet?",
            ),
            VocabularyEntry(
                "en gade", "noun", "En vej mellem huse i en by.", "Jeg bor i en stille gade."
            ),
            VocabularyEntry(
                "en vej",
                "noun",
                "Et sted, hvor man kan gå eller køre fra et sted til et andet.",
                "Denne vej går til havnen.",
            ),
            VocabularyEntry(
                "en plads",
                "noun",
                "Et åbent område, ofte mellem bygninger i byen.",
                "Vi mødes på pladsen foran biblioteket.",
            ),
            VocabularyEntry(
                "en station",
                "noun",
                "Et sted, hvor tog standser for passagerer.",
                "Stationen ligger tæt på.",
            ),
            VocabularyEntry(
                "et stoppested",
                "noun",
                "Et sted, hvor man stiger på eller af en bus.",
                "Vi venter ved stoppestedet.",
            ),
            VocabularyEntry(
                "en bus",
                "noun",
                "Et stort køretøj med plads til mange passagerer.",
                "Bussen kommer om fem minutter.",
            ),
            VocabularyEntry(
                "et tog",
                "noun",
                "Et køretøj med vogne, der kører på skinner.",
                "Toget kører til Vejle.",
            ),
            VocabularyEntry(
                "en cykel", "noun", "Et køretøj med to hjul og pedaler.", "Min cykel står udenfor."
            ),
            VocabularyEntry(
                "en billet",
                "noun",
                "Et bevis på, at man må rejse eller komme ind et sted.",
                "Jeg har en billet til toget.",
            ),
            VocabularyEntry(
                "et kort",
                "noun",
                "En tegning af et område med steder og veje.",
                "Kan du vise mig stationen på kortet?",
            ),
            VocabularyEntry(
                "en park",
                "noun",
                "Et grønt område, hvor man kan gå og opholde sig.",
                "Vi går en tur i parken.",
            ),
            VocabularyEntry(
                "et bibliotek",
                "noun",
                "Et sted, hvor man blandt andet kan låne bøger.",
                "Biblioteket åbner klokken ti.",
            ),
            VocabularyEntry(
                "et apotek",
                "noun",
                "Et sted, hvor man kan købe medicin.",
                "Der er et apotek ved torvet.",
            ),
            VocabularyEntry(
                "et hospital",
                "noun",
                "Et sted, hvor syge og tilskadekomne får behandling.",
                "Hospitalet ligger uden for byen.",
            ),
            VocabularyEntry(
                "en skole",
                "noun",
                "Et sted, hvor elever får undervisning.",
                "Skolen ligger bag parken.",
            ),
            VocabularyEntry(
                "højre",
                "adverb",
                "Retningen mod den ene side, modsat venstre.",
                "Drej til højre ved lyskrydset.",
            ),
            VocabularyEntry(
                "venstre",
                "adverb",
                "Retningen mod den anden side, modsat højre.",
                "Apoteket ligger til venstre.",
            ),
            VocabularyEntry(
                "ligeud", "adverb", "Fremad uden at dreje.", "Gå ligeud til stationen."
            ),
            VocabularyEntry(
                "nær", "preposition", "Med kort afstand til noget.", "Vi bor nær havet."
            ),
            VocabularyEntry("langt", "adverb", "Med stor afstand.", "Er der langt til skolen?"),
            VocabularyEntry("gå", "verb", "Bevæge sig på fødderne.", "Jeg går til stationen."),
            VocabularyEntry(
                "køre", "verb", "Bevæge sig med et køretøj.", "Bussen kører gennem byen."
            ),
            VocabularyEntry(
                "ligge",
                "verb",
                "Have en vandret stilling eller befinde sig et bestemt sted.",
                "Hvor ligger biblioteket?",
            ),
        ],
    ),
    VocabularySet(
        "da_leisure_a1",
        "A1",
        "Fritid, vejr og samvær",
        "a1-unit-6",
        [
            VocabularyEntry(
                "fritid",
                "noun",
                "Tid, hvor man ikke arbejder eller går i skole.",
                "Jeg læser i min fritid.",
            ),
            VocabularyEntry(
                "en tur",
                "noun",
                "En kortere rejse eller bevægelse ud og ofte hjem igen.",
                "Skal vi gå en tur?",
            ),
            VocabularyEntry(
                "en strand",
                "noun",
                "Et område med sand eller sten ved vandet.",
                "Vi går ned til stranden.",
            ),
            VocabularyEntry(
                "en skov", "noun", "Et større område med mange træer.", "Vi cykler i skoven."
            ),
            VocabularyEntry(
                "et hav", "noun", "Et stort område med saltvand.", "Havet er koldt i dag."
            ),
            VocabularyEntry(
                "en film",
                "noun",
                "En fortælling med levende billeder og ofte lyd.",
                "Vi ser en film i aften.",
            ),
            VocabularyEntry(
                "musik", "noun", "Lyde med rytme eller melodi.", "Jeg lytter til musik."
            ),
            VocabularyEntry(
                "en sang", "noun", "Ord med en melodi, som man synger.", "Vi synger en dansk sang."
            ),
            VocabularyEntry(
                "et spil",
                "noun",
                "En aktivitet med regler, ofte for flere deltagere.",
                "Vil du være med i et spil?",
            ),
            VocabularyEntry(
                "sport",
                "noun",
                "Fysiske aktiviteter med træning eller konkurrence.",
                "Jeg dyrker sport to gange om ugen.",
            ),
            VocabularyEntry(
                "en bold",
                "noun",
                "En rund ting, som bruges i mange spil.",
                "Børnene spiller med en bold.",
            ),
            VocabularyEntry(
                "svømme", "verb", "Bevæge sig gennem vand med kroppen.", "Jeg kan svømme."
            ),
            VocabularyEntry(
                "løbe", "verb", "Bevæge sig hurtigt på fødderne.", "Vi løber i parken."
            ),
            VocabularyEntry(
                "danse", "verb", "Bevæge kroppen til musik.", "Hun kan godt lide at danse."
            ),
            VocabularyEntry("synge", "verb", "Lave en melodi med stemmen.", "Vi synger sammen."),
            VocabularyEntry(
                "spille",
                "verb",
                "Deltage i et spil eller bruge et musikinstrument.",
                "Jeg spiller guitar.",
            ),
            VocabularyEntry("se", "verb", "Bruge øjnene til at opfatte noget.", "Vi ser en film."),
            VocabularyEntry(
                "mødes", "verb", "Komme til samme sted for at være sammen.", "Vi mødes ved caféen."
            ),
            VocabularyEntry(
                "besøge",
                "verb",
                "Tage hen til en person eller et sted i en periode.",
                "Jeg besøger min ven på søndag.",
            ),
            VocabularyEntry(
                "invitere",
                "verb",
                "Bede nogen om at komme eller deltage.",
                "Vi inviterer vores nabo til kaffe.",
            ),
            VocabularyEntry("gerne", "adverb", "Med lyst eller villighed.", "Jeg vil gerne med."),
            VocabularyEntry(
                "sammen", "adverb", "Med en eller flere andre.", "Vi laver mad sammen."
            ),
            VocabularyEntry(
                "sjov",
                "adjective",
                "Som giver glæde eller får en til at le.",
                "Det er et sjovt spil.",
            ),
            VocabularyEntry(
                "god",
                "adjective",
                "Som man synes positivt om, eller som fungerer godt.",
                "Det er en god film.",
            ),
            VocabularyEntry("varm", "adjective", "Med en høj temperatur.", "Det er en varm dag."),
            VocabularyEntry("kold", "adjective", "Med en lav temperatur.", "Vandet er koldt."),
            VocabularyEntry(
                "en sol",
                "noun",
                "Den stjerne, der giver Jorden lys og varme.",
                "Solen skinner i dag.",
            ),
            VocabularyEntry(
                "regn",
                "noun",
                "Vanddråber, der falder fra skyer.",
                "Der kommer regn i eftermiddag.",
            ),
        ],
    ),
    VocabularySet(
        "da_help_a1",
        "A1",
        "Hjælp, helbred og små ærinder",
        "a1-unit-7",
        [
            VocabularyEntry(
                "hjælp",
                "noun",
                "Noget, en anden gør for at gøre en opgave eller situation lettere.",
                "Jeg har brug for hjælp.",
            ),
            VocabularyEntry(
                "en læge",
                "noun",
                "En person, der undersøger og behandler sygdom.",
                "Jeg skal til lægen.",
            ),
            VocabularyEntry(
                "en tandlæge",
                "noun",
                "En person, der undersøger og behandler tænder.",
                "Tandlægen har åbent i dag.",
            ),
            VocabularyEntry(
                "en krop",
                "noun",
                "Alle de fysiske dele af et menneske eller dyr.",
                "Min krop er træt.",
            ),
            VocabularyEntry(
                "et hoved",
                "noun",
                "Den del af kroppen, hvor øjne, mund og hjerne er.",
                "Jeg har ondt i hovedet.",
            ),
            VocabularyEntry(
                "en hånd",
                "noun",
                "Den del for enden af armen, som har fingre.",
                "Jeg skriver med højre hånd.",
            ),
            VocabularyEntry(
                "en fod",
                "noun",
                "Den nederste del af benet, som man står på.",
                "Jeg har ondt i venstre fod.",
            ),
            VocabularyEntry(
                "en mave",
                "noun",
                "Den del af kroppen foran mellem bryst og hofter.",
                "Hun har ondt i maven.",
            ),
            VocabularyEntry(
                "ondt",
                "adverb",
                "Med smerte, især i forbindelsen have ondt.",
                "Det gør ondt, når jeg går.",
            ),
            VocabularyEntry("syg", "adjective", "Som ikke er rask.", "Jeg er syg i dag."),
            VocabularyEntry(
                "træt",
                "adjective",
                "Som har brug for hvile eller søvn.",
                "Jeg var meget træt i går.",
            ),
            VocabularyEntry(
                "sulten",
                "adjective",
                "Som har lyst til eller brug for mad.",
                "Jeg er sulten efter turen.",
            ),
            VocabularyEntry(
                "tørstig", "adjective", "Som har brug for noget at drikke.", "Er du tørstig?"
            ),
            VocabularyEntry(
                "åben", "adjective", "Som man kan komme ind i eller igennem.", "Butikken er åben."
            ),
            VocabularyEntry(
                "lukket",
                "adjective",
                "Som man ikke kan komme ind i eller igennem.",
                "Apoteket er lukket nu.",
            ),
            VocabularyEntry(
                "finde",
                "verb",
                "Opdage, hvor noget eller nogen er.",
                "Jeg kan ikke finde min taske.",
            ),
            VocabularyEntry(
                "miste",
                "verb",
                "Ikke længere have noget, man havde før.",
                "Jeg vil ikke miste min nøgle.",
            ),
            VocabularyEntry(
                "vente",
                "verb",
                "Blive et sted eller lade tiden gå før noget sker.",
                "Vent her et øjeblik.",
            ),
            VocabularyEntry(
                "ringe", "verb", "Kontakte nogen med en telefon.", "Jeg ringer til lægen."
            ),
            VocabularyEntry("koste", "verb", "Have en bestemt pris.", "Hvad koster denne taske?"),
            VocabularyEntry("betale", "verb", "Give penge for noget.", "Kan jeg betale her?"),
            VocabularyEntry(
                "penge",
                "noun",
                "Mønter, sedler eller beløb, man kan betale med.",
                "Jeg har ikke penge med.",
            ),
            VocabularyEntry(
                "kortbetaling",
                "noun",
                "Det, at man betaler med et bankkort frem for sedler eller mønter.",
                "Er kortbetaling mulig her?",
            ),
            VocabularyEntry(
                "en kvittering",
                "noun",
                "Et bevis på, hvad man har købt og betalt.",
                "Må jeg få en kvittering?",
            ),
            VocabularyEntry(
                "en pose",
                "noun",
                "En beholder af papir eller plastik, som kan bruges til varer.",
                "Vil du have en pose?",
            ),
            VocabularyEntry(
                "en størrelse",
                "noun",
                "Et mål for, hvor stort noget er, for eksempel tøj.",
                "Har I den i en anden størrelse?",
            ),
            VocabularyEntry(
                "et nummer",
                "noun",
                "Et tal, der bruges til at kende noget fra andet.",
                "Tag et nummer og vent.",
            ),
            VocabularyEntry(
                "en besked",
                "noun",
                "En kort oplysning, som nogen siger eller skriver.",
                "Jeg skriver en besked til min ven.",
            ),
        ],
    ),
]
