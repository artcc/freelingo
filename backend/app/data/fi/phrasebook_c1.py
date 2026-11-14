"""Finnish C1 phrases for collaborative, precise everyday interaction."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "fi-checking-evidence-c1",
        "C1",
        "Tiedon tarkistaminen yhdessä",
        "🔎",
        [
            PhrasebookEntry(
                "Mihin havaintoon tämä arvio perustuu?",
                "Pyydät kokouksessa perustetta epäilemättä suoraan puhujan rehellisyyttä.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Tämä on huoltajan kertoma tieto; en ole itse käynyt paikalla.",
                "Välität tietoa rakennuksen kunnosta ja kerrot samalla tiedon rajat.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Luvut viittaavat kasvuun, mutta kesäkuun tiedot puuttuvat vielä.",
                "Esittelet alustavaa tulosta peittämättä aineiston puutetta.",
                "formal",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "Voisimmeko erottaa sen, mitä tiedämme, siitä, mitä vasta oletamme?",
                "Keskustelussa havainnot ja arviot ovat alkaneet sekoittua.",
                "neutral",
                "c1-unit-1",
            ),
            PhrasebookEntry(
                "En sulje sitä pois, mutta en vielä pitäisi sitä todennäköisimpänä selityksenä.",
                "Vastaat ehdotettuun selitykseen hyväksymättä sitä liian vahvasti.",
                "neutral",
                "c1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-negotiating-terms-c1",
        "C1",
        "Realistisen sopimuksen neuvotteleminen",
        "🤝",
        [
            PhrasebookEntry(
                "Voimme joustaa toimituspäivässä, kunhan kokonaiskustannus ei nouse.",
                "Tarjoat myönnytyksen ja liität siihen selkeän ehdon.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Hinta sopii meille; maksuaikataulusta haluaisimme vielä keskustella.",
                "Rajaat erimielisyyden, jotta koko tarjous ei vaikuta hylätyltä.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Ymmärrän kiireen, mutta en voi luvata valmista työtä perjantaiksi.",
                "Kieltäydyt mahdottomasta aikarajasta tunnustaen toisen tarpeen.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Jos luonnos riittää tässä vaiheessa, voin toimittaa sen torstaina.",
                "Tarjoat toteuttamiskelpoisen vaihtoehdon lopullisen työn sijaan.",
                "neutral",
                "c1-unit-2",
            ),
            PhrasebookEntry(
                "Kirjataanko tämä ehdolliseksi tarjoukseksi vai jo sovituksi tehtäväksi?",
                "Tarkistat sitoumuksen aseman ennen neuvottelun päättämistä.",
                "formal",
                "c1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-clarifying-responsibility-c1",
        "C1",
        "Vastuun ja päätöksen täsmentäminen",
        "📋",
        [
            PhrasebookEntry(
                "Kuka vastaa yhteydenotosta, ja milloin saamme siitä tiedon?",
                "Tehtävä on mainittu passiivissa mutta vastuuhenkilö puuttuu.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Voin valmistella vaihtoehdot, mutta päätös ei kuulu minun toimivaltaani.",
                "Erotat oman valmistelutehtäväsi lopullisesta päätösvallasta.",
                "formal",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Ymmärsinkö oikein, että hyväksyimme selvityksen tilaamisen, emme vielä remonttia?",
                "Korjaat pöytäkirjaan mahdollisesti tulevan liian vahvan tulkinnan.",
                "neutral",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Pyydän, että tämä rajaus merkitään pöytäkirjaan.",
                "Varmistat, että päätöksen olennainen ehto säilyy kirjallisessa muistissa.",
                "formal",
                "c1-unit-3",
            ),
            PhrasebookEntry(
                "Tarjous on pyydetty, mutta tilausta ei ole vielä tehty.",
                "Selvennät työn vaihetta henkilölle, joka luuli sen jo alkavan.",
                "neutral",
                "c1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-telling-experience-c1",
        "C1",
        "Kokemuksen kertominen ja tarkentaminen",
        "📖",
        [
            PhrasebookEntry(
                "Ennen kuin jatkan, minun on kerrottava, mitä oli tapahtunut edellisenä iltana.",
                "Johdat kuulijan takaumaan menettämättä pääjuonta.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Siinä minä sitten seisoin väärällä laiturilla, lippu kädessä ja juna jo menossa.",
                "Kuvaat ystävälle matkalla sattunutta harmillista mutta huvittavaa tilannetta.",
                "informal",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Tässä kohtaa tarkoitan kuljettajaa, en sitä toista matkustajaa.",
                "Täsmennät henkilön, johon kertomuksesi pronomini viittasi.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Vasta myöhemmin ymmärsin, miksi hän oli kysynyt juuri sitä.",
                "Erotat tapahtumahetken kokemuksen jälkikäteen syntyneestä tulkinnasta.",
                "neutral",
                "c1-unit-4",
            ),
            PhrasebookEntry(
                "Mutta palataan siihen aamuun: olin siis juuri päässyt asemalle.",
                "Palaat sivupolulta kertomuksen pääasialliseen tapahtumaketjuun.",
                "neutral",
                "c1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-weighing-proposals-c1",
        "C1",
        "Ehdotusten punnitseminen",
        "⚖️",
        [
            PhrasebookEntry(
                "Ehdotus ratkaisee yhden ongelman, mutta synnyttää toisen iltavuorolaisille.",
                "Tuot keskusteluun seurauksen, jota esityksessä ei ole huomioitu.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Pidän tavoitetta hyvänä, vaikka en kannata tätä toteutustapaa.",
                "Erotat yhteisen tavoitteen kiistanalaisesta keinosta.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Mitä vertailussa muuttuu, jos kuljetuksetkin lasketaan mukaan?",
                "Pyydät arvioimaan vaihtoehtoja samoilla kustannusperusteilla.",
                "neutral",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Se, että asiat tapahtuivat samaan aikaan, ei vielä osoita niiden syy-yhteyttä.",
                "Rajoitat liian pitkälle menevää päätelmää yhteisessä arvioinnissa.",
                "formal",
                "c1-unit-5",
            ),
            PhrasebookEntry(
                "Voisimmeko kokeilla tätä kuukauden ja arvioida sitten vaikutukset?",
                "Ehdotat kokeilua tilanteessa, jossa lopullisesta ratkaisusta ei ole yhteisymmärrystä.",
                "neutral",
                "c1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-repairing-tone-c1",
        "C1",
        "Sävyn tulkitseminen ja väärinkäsityksen korjaaminen",
        "💬",
        [
            PhrasebookEntry(
                "Taisin sanoa epäselvästi. Tarkoitin vain tämän viikon vuoroja.",
                "Korjaat oman ilmauksesi syyttämättä kuulijaa väärin ymmärtämisestä.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Kun sanoit, että asia on sovittu, tarkoititko hintaa vai myös toimituspäivää?",
                "Tarkistat, kuinka laajasta yhteisymmärryksestä toinen puhui.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Tämä ei tainnut olla ihan minun tähtihetkeni.",
                "Suhtaudut omaan pieneen erehdykseesi itseironisesti tuttujen kesken.",
                "informal",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "Sellaista sattuu. Katsotaan yhdessä, miten tästä päästään eteenpäin.",
                "Vastaat toisen itseironiaan tukevasti tekemättä hänestä vitsin kohdetta.",
                "neutral",
                "c1-unit-6",
            ),
            PhrasebookEntry(
                "En ole varma, oliko tuo vitsi vai toive muuttaa suunnitelmaa.",
                "Pyydät selvennystä, kun sanat ja äänenpaino eivät anna varmaa tulkintaa.",
                "neutral",
                "c1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-mediating-interests-c1",
        "C1",
        "Erilaisten tarpeiden välittäminen",
        "🌉",
        [
            PhrasebookEntry(
                "Teille tärkeintä on ennakoitava aikataulu, teille taas mahdollisuus vaihtaa vuoroja.",
                "Nimeät kahden osapuolen tarpeet arvottamatta niitä.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Olemmeko samaa mieltä tavoitteesta, vaikka keinot ovat vielä avoinna?",
                "Etsit yhteistä lähtökohtaa ennen yksityiskohdista neuvottelemista.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Tämä on oma yhteenvetoni; korjatkaa, jos jokin painotus ei vastaa tarkoitustanne.",
                "Annat osapuolille mahdollisuuden tarkistaa, miten olet esittänyt heidän kantansa.",
                "formal",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Kirjataan sovitut asiat erikseen ja palataan jäljelle jääneeseen kysymykseen huomenna.",
                "Estät avoimen erimielisyyden peittämästä jo saavutettua edistystä.",
                "neutral",
                "c1-unit-7",
            ),
            PhrasebookEntry(
                "Voisiko yhteinen kokeilu vastata molempien huoliin ilman pysyvää sitoumusta?",
                "Ehdotat sovittelussa rajattua toimintatapaa, jonka vaikutuksia voidaan arvioida.",
                "neutral",
                "c1-unit-7",
            ),
        ],
    ),
]
