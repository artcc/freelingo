"""Finnish B2 phrases for mediation, precise requests and register control."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "fi-projects-b2",
        "B2",
        "Työn eteneminen ja tiedon alkuperä",
        "📋",
        [
            PhrasebookEntry(
                "Viimeksi hyväksytty suunnitelma ei sisällä tätä muutosta.",
                "Erotat voimassa olevan suunnitelman uudesta ehdotuksesta.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Voimmeko ensin käydä läpi asiakkaan esittämät toiveet?",
                "Palautat suunnittelukeskustelun toimeksiannon tarpeisiin.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Toimittaja kertoo lähettäneensä osat, mutta emme ole saaneet seurantatietoa.",
                "Erotat toimittajan ilmoituksen omasta varmennetusta tiedosta.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Tässä on vielä kaksi ratkaisemattomaksi jäänyttä kysymystä.",
                "Nostat esiin keskeneräiset asiat ennen päätöstä.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Saatuani lopulliset luvut päivitän kustannusarvion.",
                "Kerrot, mikä vaihe edeltää oman työsi valmistumista.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Pyydän kirjallista vahvistusta välttääkseni väärinkäsitykset.",
                "Perustelet virallisen vahvistuksen tarvetta.",
                "formal",
                "b2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-obligations-b2",
        "B2",
        "Ehtojen ja arvioiden tarkistaminen",
        "🔎",
        [
            PhrasebookEntry(
                "Onko kyse sitovasta vaatimuksesta vai suosituksesta?",
                "Selvität ohjeen velvoittavuuden ennen toimintaa.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Mihin tietoihin tämä arvio perustuu?",
                "Pyydät ennusteen perustaa arvostelematta puhujaa.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Tarkoittaako tämä, ettei liitettä tarvitse toimittaa lainkaan?",
                "Tarkistat poikkeuksen laajuuden hakemusmenettelyssä.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Voin antaa alustavan arvion, mutta en vielä luvata päivämäärää.",
                "Rajaat vastauksesi varmuuden aikataulua kysyttäessä.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Varmistetaan asia soittamalla, jotta emme toimi vanhan ohjeen mukaan.",
                "Ehdotat konkreettista tapaa poistaa epävarmuus.",
                "neutral",
                "b2-unit-4",
            ),
            PhrasebookEntry(
                "Pyytäisin täsmentämään, koskeeko velvoite myös nykyisiä asiakkaita.",
                "Pyydät palveluntarjoajalta ehtojen soveltamisalan tarkennusta.",
                "formal",
                "b2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-negotiation-b2",
        "B2",
        "Neuvottelu ja jälkikäsittely",
        "🤝",
        [
            PhrasebookEntry(
                "Voitaisiinko sopia välivaiheesta lopullisen määräajan siirtämisen sijaan?",
                "Tarjoat ratkaisun, joka huomioi molempien aikataulupaineet.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Hyväksymme hinnan, jos toimitus sisältyy siihen.",
                "Esität hyväksynnän ehdollisena, et avoimena lupauksena.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Tästä osuudesta voimme joustaa, mutta turvallisuusvaatimuksista emme.",
                "Erotat neuvoteltavat ehdot ehdottomista rajoista.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Kun ongelma huomattiin, työ oli jo tilattu.",
                "Selität tapahtumajärjestyksen jälkikäsittelyssä.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Olisimme voineet toimia toisin, mutta sovitaan nyt, miten etenemme.",
                "Tunnustat vaihtoehdon ja suuntaat keskustelun korjaavaan toimintaan.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Kirjataan sovitut ehdot, jotta meille jää sama käsitys päätöksestä.",
                "Varmistat neuvottelun lopputuloksen ennen lopettamista.",
                "neutral",
                "b2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-tone-b2",
        "B2",
        "Vaikean asian ottaminen puheeksi",
        "💬",
        [
            PhrasebookEntry(
                "Voisimmeko puhua työmäärästä kahden kesken?",
                "Aloitat arkaluonteisen keskustelun esihenkilön kanssa.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Ymmärrän kiireen, mutta en pysty lupaamaan tätä huomiseksi.",
                "Tunnustat toisen tarpeen ja kerrot oman rajasi.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Hei, taisin ilmaista itseäni turhan jyrkästi. Yritän uudestaan.",
                "Korjaat ystävälle tai tutulle työtoverille viestisi sävyä.",
                "informal",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Pahoittelen viestini epäselvyyttä. Tarkoitukseni oli pyytää lisätietoja.",
                "Selvennät virallisen viestin tavoitetta väärinkäsityksen jälkeen.",
                "formal",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Käsittääkseni päätöstä ei ole vielä tehty. Korjaa, jos olen väärässä.",
                "Esität oman tietosi rajattuna ja jätät tilaa korjaukselle.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "En arvostele sinua, vaan ehdotan toista tapaa tehdä tämä.",
                "Erotat työtapaa koskevan palautteen henkilöön kohdistuvasta arvostelusta.",
                "neutral",
                "b2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-discussion-b2",
        "B2",
        "Eriävät näkemykset ja keskustelun korjaaminen",
        "⚖️",
        [
            PhrasebookEntry(
                "Toisaalta säästämme rahaa, mutta samalla palvelun käyttö vaikeutuu osalle käyttäjistä.",
                "Tuot kustannuskeskusteluun saavutettavuuden näkökulman.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Kaikki eivät vastustaneet ehdotusta; osa pyysi vain lisäselvitystä.",
                "Korjaat liian laajan tulkinnan ryhmän kannasta.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Jos ymmärsin oikein, hyväksyt tavoitteen mutta et tätä toteutustapaa.",
                "Tarkistat toisen kannan säilyttäen sen rajauksen.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Taisit sanoa sen leikillä, mutta haluan varmistaa, mitä oikeasti ehdotat.",
                "Selvität epäselvän huumorin merkityksen loukkaamatta puhujaa.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Voisimmeko erottaa toisistaan tämän päivän ratkaisun ja pitkän aikavälin tavoitteen?",
                "Jäsennät keskustelua, jossa eri aikajänteet sekoittuvat.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Olemme eri mieltä keinosta, mutta näyttää siltä, että tavoite on yhteinen.",
                "Tunnistat yhteisen lähtökohdan sovittelun jatkamiseksi.",
                "neutral",
                "b2-unit-7",
            ),
        ],
    ),
]
