"""Finnish B1 placement questions with balanced answer positions per skill."""

from app.data._types import AssessmentQuestion

B1_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "fi-g-b1-001",
        "grammar",
        "B1",
        "Sari sanoo: Korjasin pyörää koko illan, mutta jarrut eivät vieläkään toimi. "
        "Mikä kuvaa Sarin kertomaa?",
        [
            "Sari korjasi pyörän ja testaa nyt valmiita jarruja.",
            "Sari teki korjaustyötä, mutta vika ei poistunut.",
            "Sari aikoo aloittaa korjaamisen tänä iltana.",
            "Sari jätti korjauksen tekemättä ja tilasi uudet jarrut.",
        ],
        "Sari teki korjaustyötä, mutta vika ei poistunut.",
        "fi-object-result-b1",
    ),
    AssessmentQuestion(
        "fi-g-b1-002",
        "grammar",
        "B1",
        "Kun tulin toimistoon, Aino oli jo lähettänyt hakemuksen. "
        "Mikä tapahtumajärjestys vastaa lausetta?",
        [
            "Saavuin ensin, ja sitten Aino alkoi kirjoittaa hakemusta.",
            "Aino lähetti hakemuksen samalla hetkellä, kun saavuin.",
            "Aino odotti saapumistani ennen hakemuksen lähettämistä.",
            "Aino lähetti hakemuksen ennen kuin saavuin toimistoon.",
        ],
        "Aino lähetti hakemuksen ennen kuin saavuin toimistoon.",
        "fi-pluperfect-b1",
    ),
    AssessmentQuestion(
        "fi-g-b1-003",
        "grammar",
        "B1",
        "Puhut eilisestä tilaisuudesta, johon et saanut kutsua ajoissa. Täydennä: "
        "Jos olisin tiennyt tilaisuudesta, ___ mukaan.",
        ["olisin tullut", "tulen", "olen tulossa", "tulisin huomenna"],
        "olisin tullut",
        "fi-conditional-perfect-b1",
    ),
    AssessmentQuestion(
        "fi-g-b1-004",
        "grammar",
        "B1",
        "Täydennä yleiskielen passiivin perfektillä: Taloyhtiön kaikki ikkunat ___.",
        ["ovat pesty", "on pesseet", "on pesty", "ovat pestään"],
        "on pesty",
        "fi-passive-perfect-b1",
    ),
    AssessmentQuestion(
        "fi-g-b1-005",
        "grammar",
        "B1",
        "Täydennä: Osallistun ensi kuussa ___.",
        ["uuden koulutuksen", "uudesta koulutuksesta", "uutta koulutusta", "uuteen koulutukseen"],
        "uuteen koulutukseen",
        "fi-verb-rection-b1",
    ),
    AssessmentQuestion(
        "fi-g-b1-006",
        "grammar",
        "B1",
        "Täydennä: Tässä on virkailija, ___ lähetin puuttuvan liitteen.",
        ["joka", "jolle", "jonka", "josta"],
        "jolle",
        "fi-relative-b1",
    ),
    AssessmentQuestion(
        "fi-g-b1-007",
        "grammar",
        "B1",
        "Ohjeessa lukee: Sinun ei tarvitse tulostaa lippua, jos näytät sen puhelimesta. "
        "Mitä ohje tarkoittaa?",
        [
            "Paperilippu on kielletty, vaikka puhelin olisi rikki.",
            "Lippu on tulostettava myös puhelimesta näyttämisen lisäksi.",
            "Puhelimesta näyttäminen riittää ilman paperilippua.",
            "Puhelimesta voi näyttää lipun vain tulostuksen jälkeen.",
        ],
        "Puhelimesta näyttäminen riittää ilman paperilippua.",
        "fi-necessity-b1",
    ),
    AssessmentQuestion(
        "fi-g-b1-008",
        "grammar",
        "B1",
        "Mikko sanoi maanantaina: Lähetän laskun huomenna. Kerrot keskiviikkona, mitä "
        "Mikko lupasi. Et tiedä, lähettikö hän laskun. Mikä säilyttää tiedon oikein?",
        [
            "Mikko lupasi maanantaina lähettää laskun tiistaina.",
            "Mikko lähetti laskun varmasti tiistaina.",
            "Mikko lupasi lähettää laskun torstaina.",
            "Mikko oli lähettänyt laskun jo ennen maanantaita.",
        ],
        "Mikko lupasi maanantaina lähettää laskun tiistaina.",
        "fi-reported-speech-b1",
    ),
    AssessmentQuestion(
        "fi-v-b1-001",
        "vocabulary",
        "B1",
        "Hakemuksesi on saapunut, mutta virkailija pyytää lähettämään vielä "
        "opiskelutodistuksen sen mukana käsiteltäväksi. Mitä hän pyytää?",
        [
            "Uutta ajanvarausta.",
            "Hakemuksen perumista.",
            "Puuttuvaa liitettä.",
            "Maksun palautusta.",
        ],
        "Puuttuvaa liitettä.",
    ),
    AssessmentQuestion(
        "fi-v-b1-002",
        "vocabulary",
        "B1",
        "Työpaikka antaa uudelle työntekijälle kaksi päivää aikaa tutustua laitteisiin "
        "ja käytäntöihin kokeneen työntekijän kanssa. Mistä on kyse?",
        ["Perehdytyksestä.", "Lomautuksesta.", "Irtisanoutumisesta.", "Vuosilomasta."],
        "Perehdytyksestä.",
    ),
    AssessmentQuestion(
        "fi-v-b1-003",
        "vocabulary",
        "B1",
        "Huolto kertoo: Hissiä ei saada vielä kuntoon, koska odotamme rikkoutuneen "
        "kytkimen tilalle uutta. Mitä huolto odottaa?",
        ["Vuokralaista.", "Vesikatkoa.", "Suostumusta.", "Varaosaa."],
        "Varaosaa.",
    ),
    AssessmentQuestion(
        "fi-v-b1-004",
        "vocabulary",
        "B1",
        "Et pääse lääkärille sovittuna päivänä, mutta tarvitset edelleen vastaanottoajan. "
        "Mikä pyyntö ilmaisee tavoitteesi?",
        [
            "Haluaisin perua kaikki tulevat käynnit.",
            "Haluaisin siirtää ajan toiselle päivälle.",
            "Haluaisin vahvistaa alkuperäisen käyntiajan.",
            "Haluaisin lyhentää vastaanoton kestoa.",
        ],
        "Haluaisin siirtää ajan toiselle päivälle.",
    ),
    AssessmentQuestion(
        "fi-v-b1-005",
        "vocabulary",
        "B1",
        "Lähetä vastaus viimeistään perjantaina. Mikä vastaa ohjetta?",
        [
            "Vastauksen saa lähettää jo aiemmin tai perjantaina.",
            "Vastaus pitää lähettää perjantain jälkeen.",
            "Vastauksen voi lähettää aikaisintaan perjantaina.",
            "Vastauksen pitää saapua ennen perjantain alkamista.",
        ],
        "Vastauksen saa lähettää jo aiemmin tai perjantaina.",
    ),
    AssessmentQuestion(
        "fi-v-b1-006",
        "vocabulary",
        "B1",
        "Yksi osallistuja odotti kirjastossa ja toinen kahvilassa. Molemmat luulivat "
        "olevansa sovitussa paikassa. Mikä selittää tilanteen parhaiten?",
        ["Yhteinen valinta.", "Tarkka aikataulu.", "Väärinkäsitys.", "Vapaaehtoinen tehtävä."],
        "Väärinkäsitys.",
    ),
    AssessmentQuestion(
        "fi-v-b1-007",
        "vocabulary",
        "B1",
        "Ohjaaja kysyy, miksi valitsit juuri tämän kurssin. Haluat perustella valintasi. "
        "Mikä vastaus tekee sen?",
        [
            "Ilmoittauduin kurssille viime viikon torstaina.",
            "Kurssin ilta-aika sopii työvuoroihini.",
            "Kurssi alkaa ensi kuun ensimmäisellä viikolla.",
            "Ilmoittautumissivulla on myös ohjaajan yhteystiedot.",
        ],
        "Kurssin ilta-aika sopii työvuoroihini.",
    ),
    AssessmentQuestion(
        "fi-v-b1-008",
        "vocabulary",
        "B1",
        "Sopimus ei ole vielä valmis. Haluat miettiä ehtoja ennen vastausta. "
        "Mikä ilmaus kertoo tämän?",
        [
            "Vahvistan sopimuksen näillä ehdoilla.",
            "Kieltäydyn tarjouksesta lopullisesti.",
            "Perun jo tekemäni tilauksen.",
            "Harkitsen tarjousta vielä huomiseen.",
        ],
        "Harkitsen tarjousta vielä huomiseen.",
    ),
    AssessmentQuestion(
        "fi-r-b1-001",
        "reading",
        "B1",
        "Taloyhtiön tiedote: Pihan portti vaihdetaan torstaina. Työ alkaa kello kahdeksan, "
        "ja pääportti on suljettu iltapäivään asti. Jalankulkijat voivat käyttää "
        "sivuporttia. Jos tarvitset autoasi torstaiaamuna, siirrä se kadun varteen jo "
        "keskiviikkoiltana. Työn tarkka päättymisaika riippuu toimituksesta. "
        "Leena lähtee autolla töihin torstaina kello yhdeksän. Miten hänen kannattaa toimia?",
        [
            "Ajaa torstaiaamuna sivuportin kautta.",
            "Odottaa, että pääportti avataan ennen yhdeksää.",
            "Pyytää jalankulkijoita avaamaan pääportin.",
            "Pysäköidä auto kadulle edellisenä iltana.",
        ],
        "Pysäköidä auto kadulle edellisenä iltana.",
    ),
    AssessmentQuestion(
        "fi-r-b1-002",
        "reading",
        "B1",
        "Hei! Kurssin ensimmäinen tapaaminen siirtyy verkkoon, koska luokassa on vesivahinko. "
        "Lähetän osallistumislinkin samana aamuna. Jos et saa linkkiä kello kymmeneen "
        "mennessä, soita toimistoon. Tapaaminen alkaa tavalliseen aikaan kello 12. "
        "Seuraavien viikkojen paikoista ilmoitetaan myöhemmin. "
        "Mitä opiskelija voi päätellä viestistä?",
        [
            "Kaikki loputkin tapaamiset pidetään verkossa.",
            "Ensimmäisen kerran paikka muuttuu, mutta aloitusaika säilyy.",
            "Osallistumislinkki pitää hakea toimistolta henkilökohtaisesti.",
            "Ensimmäinen tapaaminen alkaa kaksi tuntia aikaisemmin.",
        ],
        "Ensimmäisen kerran paikka muuttuu, mutta aloitusaika säilyy.",
    ),
    AssessmentQuestion(
        "fi-r-b1-003",
        "reading",
        "B1",
        "Etsin asuntoa läheltä keskustaa, mutta vuokrat olivat liian korkeita. Löysin "
        "lopulta pienemmän asunnon kauempaa. Työmatka kestää nyt kymmenen minuuttia "
        "pidempään, mutta asema on lähellä ja vuokrissa säästyvä raha riittää kuukausilippuun "
        "ja sitä jää vielä säästöönkin. En tarvitse enää omaa autoa. "
        "Mikä oli kirjoittajan ratkaisun tärkeä etu?",
        [
            "Asumisen säästö kattaa matkalipun ja jättää rahaa yli.",
            "Uusi asunto on entistä suurempi ja lähempänä keskustaa.",
            "Työmatka lyheni, koska kirjoittaja hankki auton.",
            "Kuukausilippu sisältyy uuden asunnon vuokraan.",
        ],
        "Asumisen säästö kattaa matkalipun ja jättää rahaa yli.",
    ),
    AssessmentQuestion(
        "fi-r-b1-004",
        "reading",
        "B1",
        "Hei Omar! Lupasin auttaa muutossa lauantaina. Työvuoroni kuitenkin vaihtui, "
        "joten pääsen paikalle vasta kahdelta. Siskoni voi tuoda pakettiauton jo "
        "kymmeneltä, jos joku hakee avaimet häneltä perjantaina. Hän ei voi jäädä "
        "kantamaan tavaroita. Kerro, sopiiko tämä järjestely. "
        "Mitä Omarin pitää järjestää, jos hän haluaa auton käyttöön aamuksi?",
        [
            "Pyytää viestin kirjoittajaa tulemaan ennen työvuoroa.",
            "Sopia, että sisko jää auttamaan kantamisessa.",
            "Sopia avainten hakemisesta edellisenä päivänä.",
            "Siirtää koko muutto sunnuntaiaamuun.",
        ],
        "Sopia avainten hakemisesta edellisenä päivänä.",
    ),
]
