"""Finnish B2 placement questions with balanced answer positions per skill."""

from app.data._types import AssessmentQuestion

B2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "fi-g-b2-001",
        "grammar",
        "B2",
        "Tiedotteessa lukee: Asukkaiden laatima ehdotus lähetettiin hallitukselle. "
        "Mikä säilyttää tekijän ja vastaanottajan oikein?",
        [
            "Hallitus laati ehdotuksen ja lähetti sen asukkaille.",
            "Asukkaat saivat hallituksen laatiman ehdotuksen.",
            "Asukkaat laativat ehdotuksen, joka lähetettiin hallitukselle.",
            "Hallitus ja asukkaat laativat ehdotuksen yhdessä.",
        ],
        "Asukkaat laativat ehdotuksen, joka lähetettiin hallitukselle.",
        "fi-agent-participle-b2",
    ),
    AssessmentQuestion(
        "fi-g-b2-002",
        "grammar",
        "B2",
        "Tiina kertoo palauttaneensa avaimet. Mitä lause ilmaisee ilman lisätietoja?",
        [
            "Tiinan mukaan hän palautti avaimet ennen kertomista.",
            "Kertoja näki itse, kun Tiina palautti avaimet.",
            "Tiina kertoo jonkun toisen palauttavan avaimet.",
            "Tiina lupaa palauttaa avaimet kertomisen jälkeen.",
        ],
        "Tiinan mukaan hän palautti avaimet ennen kertomista.",
        "fi-referative-past-b2",
    ),
    AssessmentQuestion(
        "fi-g-b2-003",
        "grammar",
        "B2",
        "Saatuaan hyväksynnän yhdistys tilasi laitteet. Mikä tulkinta säilyttää aikajärjestyksen?",
        [
            "Yhdistys tilasi laitteet ja odottaa vielä hyväksyntää.",
            "Hyväksyntää haettiin vasta laitteiden saapumisen jälkeen.",
            "Laitteet tilattiin riippumatta siitä, tuleeko hyväksyntää.",
            "Hyväksyntä saatiin ennen laitteiden tilaamista.",
        ],
        "Hyväksyntä saatiin ennen laitteiden tilaamista.",
        "fi-temporal-prior-b2",
    ),
    AssessmentQuestion(
        "fi-g-b2-004",
        "grammar",
        "B2",
        "Rakennuttaja kirjoittaa: Työ valmistunee toukokuussa. "
        "Miten kerrot saman asian arkisesti muuttamatta varmuutta?",
        [
            "Työn on valmistuttava toukokuussa.",
            "Työ valmistuu luultavasti toukokuussa.",
            "Työn luvataan valmistuvan toukokuussa.",
            "Työ oli valmistunut jo toukokuussa.",
        ],
        "Työ valmistuu luultavasti toukokuussa.",
        "fi-potential-b2",
    ),
    AssessmentQuestion(
        "fi-g-b2-005",
        "grammar",
        "B2",
        "Sopimuksessa lukee: Vuokralaisen on ilmoitettava viasta viipymättä. "
        "Mikä tulkinta vastaa velvoitteen vahvuutta?",
        [
            "Vuokralaisen täytyy ilmoittaa viasta ilman tarpeetonta viivettä.",
            "Vuokralainen saa ilmoittaa viasta, jos pitää sitä hyödyllisenä.",
            "Vuokralaisen täytyy ilmoittaa viasta seuraavan määräaikaistarkastuksen yhteydessä.",
            "Vuokralaisen kannattaa ilmoittaa viasta, mutta hän voi itse päättää ajankohdan.",
        ],
        "Vuokralaisen täytyy ilmoittaa viasta ilman tarpeetonta viivettä.",
        "fi-modal-obligation-b2",
    ),
    AssessmentQuestion(
        "fi-g-b2-006",
        "grammar",
        "B2",
        "Varaus tehtiin aikataulua tarkistamatta, ja päällekkäisyys huomattiin vasta myöhemmin. "
        "Kollega toteaa: Jos aikataulu olisi tarkistettu, päällekkäisyys olisi huomattu ennen varausta. "
        "Miten puhuja käsittelee tapahtumaa?",
        [
            "Hän pitää tarkistusta tarpeettomana, koska päällekkäisyys huomattiin lopulta.",
            "Hän kertoo toteutuneesta tarkistuksesta, jossa päällekkäisyys jäi havaitsematta.",
            "Hän kuvaa tarkistusta, jonka avulla jo tehty varaus voidaan vielä perua.",
            "Hän kuvaa mennyttä vaihtoehtoa, joka ei toteutunut.",
        ],
        "Hän kuvaa mennyttä vaihtoehtoa, joka ei toteutunut.",
        "fi-counterfactual-b2",
    ),
    AssessmentQuestion(
        "fi-g-b2-007",
        "grammar",
        "B2",
        "Kaikki osallistujat eivät hyväksyneet ehdotusta. Mitä tästä voidaan varmasti päätellä?",
        [
            "Yksikään osallistuja ei hyväksynyt ehdotusta.",
            "Ainakin yksi osallistuja jätti ehdotuksen hyväksymättä.",
            "Yli puolet osallistujista vastusti ehdotusta.",
            "Täsmälleen puolet osallistujista hyväksyi ehdotuksen.",
        ],
        "Ainakin yksi osallistuja jätti ehdotuksen hyväksymättä.",
        "fi-quantifier-scope-b2",
    ),
    AssessmentQuestion(
        "fi-g-b2-008",
        "grammar",
        "B2",
        "Kollega sanoo: Voisin ottaa tehtävän, jos saisin kaksi päivää lisäaikaa. "
        "Haluat tarkistaa hänen kantansa muuttamatta ehtoa lupaukseksi. Mitä sanot?",
        [
            "Eli otat tehtävän vastaan, ja sovimme lisäajasta myöhemmin?",
            "Eli kaksi lisäpäivää ei muuttaisi kantaasi tehtävän vastaanottamiseen?",
            "Eli kahden päivän jousto aikataulussa voisi tehdä tehtävästä sinulle mahdollisen?",
            "Eli tarvitset kaksi lisäpäivää päättääksesi, otatko tehtävän vastaan?",
        ],
        "Eli kahden päivän jousto aikataulussa voisi tehdä tehtävästä sinulle mahdollisen?",
        "fi-repair-b2",
    ),
    AssessmentQuestion(
        "fi-v-b2-001",
        "vocabulary",
        "B2",
        "Toimittaja alentaa hintaa, ja asiakas hyväksyy pidemmän toimitusajan. "
        "Molemmat muuttavat alkuperäistä vaatimustaan. Mikä kuvaa lopputulosta?",
        [
            "Yksipuolinen määräys.",
            "Yhteinen kompromissi.",
            "Alkuperäinen tarjous.",
            "Ratkaisematon umpikuja.",
        ],
        "Yhteinen kompromissi.",
    ),
    AssessmentQuestion(
        "fi-v-b2-002",
        "vocabulary",
        "B2",
        "Raportin mukaan uusi työtapa nopeutti palvelua huomattavasti, mutta vertailuryhmä puuttuu. "
        "Haluat kyseenalaistaa johtopäätöksen asiallisesti. Mikä vastaus toteuttaa tavoitteen?",
        [
            "Kuinka nopeasti uusi työtapa voidaan ottaa käyttöön muissakin toimipisteissä?",
            "Miten voimme esittää todetun syy-yhteyden raportissa nykyistä selkeämmin?",
            "Miten työtavan jo osoitettu hyöty vaikuttaa seuraavan vuoden resursointiin?",
            "Miten erotamme työtavan vaikutuksen muista mahdollisista syistä?",
        ],
        "Miten erotamme työtavan vaikutuksen muista mahdollisista syistä?",
    ),
    AssessmentQuestion(
        "fi-v-b2-003",
        "vocabulary",
        "B2",
        "Asiakas saa hinta-arvion ja kysyy, voiko summa vielä muuttua. "
        "Myyjä vastaa: Tämä on vasta alustava arvio. Mitä vastaus tarkoittaa?",
        [
            "Luku voi tarkentua ennen lopullista tarjousta.",
            "Luku velvoittaa myyjää jo sopimuksen tavoin.",
            "Luku on asiakkaan tähän mennessä maksama summa.",
            "Luku sisältää jo kaikki tulevat hinnankorotukset.",
        ],
        "Luku voi tarkentua ennen lopullista tarjousta.",
    ),
    AssessmentQuestion(
        "fi-v-b2-004",
        "vocabulary",
        "B2",
        "Työtoveri kertoo olevansa ylikuormittunut eikä halua puhua asiasta ryhmän edessä. "
        "Mikä vastaus osoittaa hienotunteisuutta ja vie asiaa eteenpäin?",
        [
            "Otetaan tämä heti koko ryhmän käsittelyyn, niin kaikki kuulevat.",
            "Jätetään työmäärä käsittelemättä, koska siitä on vaikea puhua.",
            "Sovitaanko rauhallinen hetki kahden kesken ja mietitään vaihtoehtoja?",
            "Kerron tilanteestasi muille ensin, jotta sinun ei tarvitse selittää.",
        ],
        "Sovitaanko rauhallinen hetki kahden kesken ja mietitään vaihtoehtoja?",
    ),
    AssessmentQuestion(
        "fi-r-b2-001",
        "reading",
        "B2",
        "Kunta kokeili kirjaston pidempiä omatoimiaikoja yhdessä toimipisteessä. "
        "Kävijämäärä kasvoi kokeilun aikana, mutta samaan aikaan lähikirjasto oli "
        "remontin vuoksi suljettu. Kyselyyn vastanneet pitivät uusia aikoja hyödyllisinä. "
        "Kysely oli saatavilla vain kirjaston sisällä, eikä vastaajien suhdetta kaikkiin "
        "kävijöihin selvitetty. Lautakunta päätti jatkaa kokeilua syksyyn ja kerätä "
        "vertailutietoa remontin päätyttyä. Vakituista laajennusta ei vielä hyväksytty. "
        "Mikä johtopäätös ottaa tiedon rajat parhaiten huomioon?",
        [
            "Kävijämäärän kasvu voidaan erottaa remontin vaikutuksesta myönteisen kyselyn avulla.",
            "Laajennus voidaan jo vakinaistaa, koska kysely vahvistaa uusien aikojen tarpeellisuuden.",
            "Kasvu on kiinnostava havainto, mutta sen syy ja pysyvyys vaativat lisäselvitystä.",
            "Remontin päätyttyä riittää kyselyn uusiminen, sillä kasvun syy on jo tiedossa.",
        ],
        "Kasvu on kiinnostava havainto, mutta sen syy ja pysyvyys vaativat lisäselvitystä.",
    ),
    AssessmentQuestion(
        "fi-r-b2-002",
        "reading",
        "B2",
        "Hei, kiitos ehdotuksesta. Voimme hyväksyä uuden hinnan, mikäli sovittu "
        "huoltopalvelu sisältyy siihen myös toisena vuonna. Toimituksen siirtyminen "
        "viikolla ei aiheuta meille ongelmaa. Emme kuitenkaan voi vahvistaa tilausta "
        "ennen kuin saamme huollon sisällöstä kirjallisen kuvauksen. Alustava "
        "keskustelumme koski laajempaa huoltoa kuin viimeisimmässä liitteessä mainitaan. "
        "Ehdotan lyhyttä puhelua huomiseksi, jotta voimme ratkaista tämän kohdan. "
        "Mikä vastaus edistäisi tilauksen vahvistamista viestin mukaisesti?",
        [
            "Täsmennämme huollon kirjallisesti; sovittu huolto sisältyy hintaan myös toisena vuonna.",
            "Vahvistamme tilauksen heti, sillä uusi hinta ja myöhäisempi toimitus on hyväksytty.",
            "Palautamme alkuperäisen toimituspäivän ja poistamme huollon toisen vuoden tarjouksesta.",
            "Lähetämme saman liitteen uudelleen ja pidämme huoltoa jo sovittuna.",
        ],
        "Täsmennämme huollon kirjallisesti; sovittu huolto sisältyy hintaan myös toisena vuonna.",
    ),
    AssessmentQuestion(
        "fi-r-b2-003",
        "reading",
        "B2",
        "Työryhmässä ehdotettiin kaikkien kokousten siirtämistä verkkoon. Leena kannatti "
        "matkustamisen vähentämistä, mutta muistutti uusien työntekijöiden tarvitsevan "
        "myös kasvokkaista tutustumista. Omar huomautti, että viikoittainen läsnäolopakko "
        "kuormittaisi kaukana asuvia. Molemmat pitivät säännöllistä yhteydenpitoa tärkeänä. "
        "Puheenjohtaja ehdotti määräaikaista kokeilua: tavalliset kokoukset verkossa ja "
        "harvemmat, etukäteen sovitut yhteiset päivät toimistolla. Etäosallistuminen "
        "olisi näinäkin päivinä mahdollista perustellusta syystä. "
        "Miten puheenjohtajan ehdotus suhteutuu esitettyihin näkemyksiin?",
        [
            "Se toteuttaa Leenan toiveen velvoittamalla kaikki viikoittain toimistolle.",
            "Se poistaa Omarin huolen lopettamalla kasvokkaiset tapaamiset kokonaan.",
            "Se siirtää päätöksen tekemättä yhteydenpidolle mitään käytännön muutosta.",
            "Se yhdistää matkojen vähentämisen ja rajatut mahdollisuudet tavata kasvokkain.",
        ],
        "Se yhdistää matkojen vähentämisen ja rajatut mahdollisuudet tavata kasvokkain.",
    ),
    AssessmentQuestion(
        "fi-r-b2-004",
        "reading",
        "B2",
        "Kun kokous venyi kolmannen kerran, Aino sanoi hymyillen: Tällä vauhdilla "
        "saamme ensi vuodenkin asiat käsiteltyä tänään. Hetken kuluttua hän lisäsi: "
        "Vakavasti puhuen, tarvitsen päätöksen ainakin hankinnasta ennen neljää. "
        "Muut asiat voivat mielestäni odottaa ensi viikkoon. Kollega vastasi: "
        "Sovitaanko siis, että keskitymme hankintaan ja siirrämme loput? Aino nyökkäsi. "
        "Mikä tulkinta sopii koko tilanteeseen parhaiten?",
        [
            "Aino halusi lisätä kokoukseen seuraavan vuoden suunnittelun.",
            "Aino kommentoi venymistä leikillisesti ja ehdotti sitten asioiden priorisointia.",
            "Aino vaati kaikkien asioiden ratkaisemista ennen neljää.",
            "Aino hyväksyi hankintapäätöksen siirtämisen seuraavalle viikolle.",
        ],
        "Aino kommentoi venymistä leikillisesti ja ehdotti sitten asioiden priorisointia.",
    ),
]
