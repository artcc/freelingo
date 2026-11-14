"""Finnish A2 vocabulary: seven sets of twenty-six distinct entries."""

from app.data._types import VocabularyEntry, VocabularySet

A2_SETS: list[VocabularySet] = [
    VocabularySet(
        "fi_housing_a2",
        "A2",
        "Asuminen ja muuttaminen",
        "a2-unit-1",
        [
            VocabularyEntry(
                "vuokra",
                "noun",
                "Maksu toisen omistaman asunnon tai tavaran käytöstä.",
                "Asunnon vuokra on 700 euroa kuukaudessa.",
            ),
            VocabularyEntry(
                "vuokralainen",
                "noun",
                "Henkilö, joka maksaa toisen omaisuuden käytöstä.",
                "Uusi vuokralainen muuttaa huomenna.",
            ),
            VocabularyEntry(
                "vuokranantaja",
                "noun",
                "Henkilö tai yritys, joka antaa omaisuuttaan käyttöön maksua vastaan.",
                "Vuokranantaja asuu toisessa kaupungissa.",
            ),
            VocabularyEntry(
                "sopimus",
                "noun",
                "Osapuolten yhteinen päätös oikeuksista ja velvollisuuksista.",
                "Vuokrasopimus on kirjallinen sopimus.",
            ),
            VocabularyEntry(
                "muutto",
                "noun",
                "Kodin ja tavaroiden siirtäminen uuteen paikkaan.",
                "Muutto on lauantaina.",
            ),
            VocabularyEntry(
                "kerrostalo",
                "noun",
                "Usean kerroksen rakennus, jossa on tavallisesti monta asuntoa.",
                "Asun kerrostalossa.",
            ),
            VocabularyEntry(
                "omakotitalo",
                "noun",
                "Yleensä yhden perheen käyttöön tarkoitettu erillinen asuintalo.",
                "Tämä omakotitalo on puinen.",
            ),
            VocabularyEntry(
                "parveke",
                "noun",
                "Asunnosta ulos rakennettu pieni avoin tai lasitettu tila.",
                "Parvekkeella on kaksi tuolia.",
            ),
            VocabularyEntry(
                "piha", "noun", "Rakennuksen ympärillä oleva ulkoalue.", "Lapset leikkivät pihalla."
            ),
            VocabularyEntry(
                "kerros",
                "noun",
                "Rakennuksen samalla korkeudella oleva huoneiden taso.",
                "Asun kolmannessa kerroksessa.",
            ),
            VocabularyEntry(
                "hissi",
                "noun",
                "Laite, joka kuljettaa ihmisiä tai tavaroita kerrosten välillä.",
                "Talossa ei ole hissiä.",
            ),
            VocabularyEntry(
                "portaat",
                "noun",
                "Askelmista muodostuva kulkureitti tasolta toiselle.",
                "Portaat ovat kapeat.",
            ),
            VocabularyEntry(
                "eteinen",
                "noun",
                "Sisäänkäynnin yhteydessä oleva tila vaatteille ja kengille.",
                "Kengät ovat eteisessä.",
            ),
            VocabularyEntry(
                "makuuhuone",
                "noun",
                "Huone, joka on tarkoitettu nukkumiseen.",
                "Makuuhuoneen ikkuna on pihalle päin.",
            ),
            VocabularyEntry(
                "olohuone",
                "noun",
                "Kodin huone yhdessä olemista ja rentoutumista varten.",
                "Olohuoneessa on sohva.",
            ),
            VocabularyEntry(
                "kylpyhuone", "noun", "Huone peseytymistä varten.", "Kylpyhuoneessa on suihku."
            ),
            VocabularyEntry(
                "sauna",
                "noun",
                "Lämmitettävä tila, jossa kylvetään kuumassa ilmassa ja löylyssä.",
                "Talossa on yhteinen sauna.",
            ),
            VocabularyEntry(
                "lattia", "noun", "Huoneen alin pinta, jonka päällä kävellään.", "Lattia on puhdas."
            ),
            VocabularyEntry(
                "seinä",
                "noun",
                "Pystysuora rakenne, joka rajaa huonetta tai rakennusta.",
                "Seinällä on kuva.",
            ),
            VocabularyEntry(
                "katto",
                "noun",
                "Rakennuksen ylin suojaava osa tai huoneen yläpinta.",
                "Huoneen katto on valkoinen.",
            ),
            VocabularyEntry(
                "verho",
                "noun",
                "Kangas, joka peittää esimerkiksi ikkunan.",
                "Uudet verhot ovat siniset.",
            ),
            VocabularyEntry(
                "hylly",
                "noun",
                "Vaakasuora taso, jolla säilytetään tavaroita.",
                "Kirjat ovat hyllyllä.",
            ),
            VocabularyEntry(
                "jääkaappi", "noun", "Kylmä säilytyslaite ruoalle.", "Maito on jääkaapissa."
            ),
            VocabularyEntry(
                "pesukone",
                "noun",
                "Laite, joka pesee esimerkiksi pyykkiä.",
                "Pesukone on kylpyhuoneessa.",
            ),
            VocabularyEntry(
                "siivota", "verb", "Puhdistaa ja järjestää tila.", "Siivoan keittiön tänään."
            ),
            VocabularyEntry(
                "muuttaa",
                "verb",
                "Siirtää oma koti toiseen asuntoon tai paikkaan.",
                "Muutan ensi viikolla Espooseen.",
            ),
        ],
    ),
    VocabularySet(
        "fi_shopping_services_a2",
        "A2",
        "Vaatteet ja asiakaspalvelu",
        "a2-unit-2",
        [
            VocabularyEntry(
                "asiakas",
                "noun",
                "Henkilö, joka ostaa tai käyttää palvelua.",
                "Asiakas kysyy neuvoa.",
            ),
            VocabularyEntry(
                "myyjä", "noun", "Henkilö, jonka työ on myydä tuotteita.", "Myyjä näyttää takkeja."
            ),
            VocabularyEntry(
                "palvelu",
                "noun",
                "Toisen hyväksi tehtävä työ tai tarjottu apu.",
                "Tässä kaupassa on ystävällinen palvelu.",
            ),
            VocabularyEntry(
                "tuote", "noun", "Valmistettu tavara tai muu myytävä asia.", "Tämä tuote on loppu."
            ),
            VocabularyEntry(
                "koko", "noun", "Esineen tai vaatteen suuruus.", "Mikä tämän paidan koko on?"
            ),
            VocabularyEntry(
                "väri",
                "noun",
                "Näköominaisuus, esimerkiksi sininen tai punainen.",
                "Pidän tästä väristä.",
            ),
            VocabularyEntry(
                "vaate",
                "noun",
                "Kehon suojaksi tai peitteeksi puettava esine.",
                "Tarvitsen lämpimiä vaatteita.",
            ),
            VocabularyEntry(
                "takki", "noun", "Ylävartalon päälle puettava ulkovaate.", "Sovitan tätä takkia."
            ),
            VocabularyEntry(
                "paita",
                "noun",
                "Ylävartalon vaate, jossa on yleensä hihat.",
                "Tässä paidassa on pitkät hihat.",
            ),
            VocabularyEntry(
                "housut",
                "noun",
                "Vyötäröltä jalkoihin ulottuva vaate, jossa on kaksi lahjetta.",
                "Nämä housut ovat liian pitkät.",
            ),
            VocabularyEntry(
                "kenkä",
                "noun",
                "Jalkaterää suojaava jalkine, jossa on tavallisesti pohja.",
                "Etsin uusia kenkiä.",
            ),
            VocabularyEntry(
                "sukka",
                "noun",
                "Pehmeä vaate, joka peittää jalan kengän sisällä.",
                "Ostan lämpimiä sukkia.",
            ),
            VocabularyEntry(
                "hame",
                "noun",
                "Vyötäröltä alaspäin riippuva vaate ilman lahkeita.",
                "Hame on polvipituinen.",
            ),
            VocabularyEntry(
                "mekko",
                "noun",
                "Yhtenäinen vaate, jossa on yläosa ja hameosa.",
                "Tämä mekko on sopiva.",
            ),
            VocabularyEntry(
                "sovituskoppi",
                "noun",
                "Pieni tila, jossa voi kokeilla vaatetta päälleen.",
                "Sovituskoppi on tuolla.",
            ),
            VocabularyEntry(
                "alennus",
                "noun",
                "Tavallista hintaa pienentävä määrä.",
                "Näistä kengistä saa alennuksen.",
            ),
            VocabularyEntry(
                "tarjous",
                "noun",
                "Rajattu mahdollisuus ostaa tuote erityiseen hintaan.",
                "Tämä tarjous on voimassa tänään.",
            ),
            VocabularyEntry(
                "kassajono",
                "noun",
                "Maksuvuoroa odottavien asiakkaiden rivi.",
                "Kassajono on pitkä.",
            ),
            VocabularyEntry(
                "maksukortti",
                "noun",
                "Kortti, jolla ostos maksetaan tililtä tai luotolla.",
                "Maksan maksukortilla.",
            ),
            VocabularyEntry(
                "käteinen",
                "noun",
                "Fyysinen raha eli setelit ja kolikot.",
                "Onko sinulla käteistä?",
            ),
            VocabularyEntry(
                "palautus",
                "noun",
                "Ostoksen vieminen takaisin myyjälle sovittujen ehtojen mukaan.",
                "Palautus onnistuu kuitin kanssa.",
            ),
            VocabularyEntry(
                "vaihtaa",
                "verb",
                "Ottaa tai antaa toinen asia ensimmäisen tilalle.",
                "Haluan vaihtaa tämän pienempään kokoon.",
            ),
            VocabularyEntry(
                "sovittaa",
                "verb",
                "Kokeilla vaatetta päälle koon ja ulkonäön tarkistamiseksi.",
                "Voinko sovittaa näitä kenkiä?",
            ),
            VocabularyEntry(
                "maksaa",
                "verb",
                "Antaa rahaa ostoksesta tai palvelusta.",
                "Maksan ostokset kassalla.",
            ),
            VocabularyEntry(
                "kallis",
                "adjective",
                "Sellainen, jonka hinta on suuri.",
                "Tuo takki on minulle liian kallis.",
            ),
            VocabularyEntry(
                "halpa", "adjective", "Sellainen, jonka hinta on pieni.", "Tämä paita on halpa."
            ),
        ],
    ),
    VocabularySet(
        "fi_travel_a2",
        "A2",
        "Matkustaminen ja reitin löytäminen",
        "a2-unit-3",
        [
            VocabularyEntry(
                "matka",
                "noun",
                "Kulkeminen paikasta toiseen tai näiden paikkojen välimatka.",
                "Matka kestää kaksi tuntia.",
            ),
            VocabularyEntry(
                "lähtö",
                "noun",
                "Hetki tai tapahtuma, jolloin lähdetään matkalle.",
                "Junan lähtö on kello yhdeksän.",
            ),
            VocabularyEntry(
                "saapuminen",
                "noun",
                "Tuleminen matkan päätepisteeseen.",
                "Saapuminen Turkuun on kello yksitoista.",
            ),
            VocabularyEntry(
                "aikataulu",
                "noun",
                "Luettelo tapahtumien tai kulkuvälineiden ajoista.",
                "Tarkistan bussin aikataulun.",
            ),
            VocabularyEntry(
                "reitti",
                "noun",
                "Kulkuväylä tai kuljettava tie lähtöpaikasta määränpäähän.",
                "Tämä reitti kulkee puiston kautta.",
            ),
            VocabularyEntry(
                "vaihto",
                "noun",
                "Siirtyminen yhdestä kulkuvälineestä toiseen matkan aikana.",
                "Tampereella on vaihto toiseen junaan.",
            ),
            VocabularyEntry(
                "laituri",
                "noun",
                "Asemalla oleva taso junaan nousemista varten.",
                "Juna lähtee laiturilta kolme.",
            ),
            VocabularyEntry(
                "lentokenttä",
                "noun",
                "Alue, josta lentokoneet lähtevät ja jonne ne laskeutuvat.",
                "Menen lentokentälle junalla.",
            ),
            VocabularyEntry(
                "lento", "noun", "Matka ilmassa lentokoneella.", "Lento lähtee aamulla."
            ),
            VocabularyEntry(
                "passi",
                "noun",
                "Viranomaisen antama henkilöllisyys- ja matkustusasiakirja.",
                "Passi on laukussa.",
            ),
            VocabularyEntry(
                "matkalaukku",
                "noun",
                "Suuri suljettava laukku matkalla tarvittaville tavaroille.",
                "Matkalaukku on painava.",
            ),
            VocabularyEntry(
                "varaus",
                "noun",
                "Etukäteen tehty sopimus paikan tai palvelun käytöstä.",
                "Minulla on huonevaraus.",
            ),
            VocabularyEntry(
                "majoitus",
                "noun",
                "Matkustajan yöpyminen ja siihen tarjottu tila.",
                "Majoitus sisältyy hintaan.",
            ),
            VocabularyEntry(
                "vastaanotto",
                "noun",
                "Hotellin palvelupiste, jossa asiakkaat ilmoittautuvat.",
                "Kysyn vastaanotosta karttaa.",
            ),
            VocabularyEntry(
                "retki",
                "noun",
                "Tavallisesti lyhyt matka virkistymistä tai tutustumista varten.",
                "Teemme retken saareen.",
            ),
            VocabularyEntry(
                "nähtävyys",
                "noun",
                "Paikka tai kohde, jota matkailijat käyvät katsomassa.",
                "Vanha linna on suosittu nähtävyys.",
            ),
            VocabularyEntry(
                "keskusta",
                "noun",
                "Kaupungin keskeinen alue, jossa on usein paljon palveluja.",
                "Hotelli on keskustassa.",
            ),
            VocabularyEntry(
                "risteys",
                "noun",
                "Paikka, jossa tiet tai kadut kohtaavat.",
                "Käänny seuraavasta risteyksestä.",
            ),
            VocabularyEntry(
                "liikennevalo",
                "noun",
                "Valomerkki, joka ohjaa liikenteen kulkua.",
                "Odotan liikennevalon vaihtumista.",
            ),
            VocabularyEntry(
                "suojatie",
                "noun",
                "Merkitty kohta, jossa jalankulkija ylittää tien.",
                "Ylitän kadun suojatietä pitkin.",
            ),
            VocabularyEntry(
                "myöhästyä",
                "verb",
                "Saapua liian myöhään sovittuun aikaan nähden.",
                "En halua myöhästyä junasta.",
            ),
            VocabularyEntry(
                "ehtiä",
                "verb",
                "Saada jotakin tehtyä tai saapua ennen määräaikaa.",
                "Ehdin vielä bussiin.",
            ),
            VocabularyEntry(
                "matkustaa",
                "verb",
                "Kulkea matkustajana paikasta toiseen.",
                "Matkustan Ouluun junalla.",
            ),
            VocabularyEntry(
                "varata",
                "verb",
                "Sopia etukäteen paikan tai ajan käyttämisestä.",
                "Varaan huoneen kahdeksi yöksi.",
            ),
            VocabularyEntry(
                "perua",
                "verb",
                "Ilmoittaa, ettei aiemmin sovittu asia toteudu.",
                "Haluan perua varauksen.",
            ),
            VocabularyEntry(
                "opastaa",
                "verb",
                "Näyttää reitti tai neuvoa, miten toimitaan.",
                "Voitko opastaa minut asemalle?",
            ),
        ],
    ),
    VocabularySet(
        "fi_work_study_a2",
        "A2",
        "Työ ja opiskelu",
        "a2-unit-4",
        [
            VocabularyEntry(
                "ammatti",
                "noun",
                "Työala tai tehtävä, johon ihmisellä on osaamista.",
                "Mikä sinun ammattisi on?",
            ),
            VocabularyEntry(
                "työpaikka",
                "noun",
                "Paikka tai organisaatio, jossa ihminen tekee työtään.",
                "Työpaikkani on lähellä kotia.",
            ),
            VocabularyEntry(
                "työntekijä",
                "noun",
                "Henkilö, joka tekee työtä työnantajalle.",
                "Uusi työntekijä aloitti eilen.",
            ),
            VocabularyEntry(
                "työnantaja",
                "noun",
                "Henkilö tai organisaatio, joka palkkaa työntekijöitä.",
                "Työnantaja järjesti koulutuksen.",
            ),
            VocabularyEntry(
                "työkaveri",
                "noun",
                "Henkilö, jonka kanssa tekee työtä samassa paikassa.",
                "Työkaveri auttoi minua.",
            ),
            VocabularyEntry(
                "kokous",
                "noun",
                "Sovittu tapaaminen yhteisten asioiden käsittelyyn.",
                "Kokous alkoi yhdeksältä.",
            ),
            VocabularyEntry(
                "työvuoro",
                "noun",
                "Aika, jolloin tietyn työntekijän kuuluu olla töissä.",
                "Työvuoroni päättyi illalla.",
            ),
            VocabularyEntry(
                "tauko",
                "noun",
                "Lyhyt keskeytys työn tai muun toiminnan aikana.",
                "Pidimme tauon kello kymmenen.",
            ),
            VocabularyEntry(
                "palkka",
                "noun",
                "Työstä maksettava rahallinen korvaus.",
                "Palkka tulee tilille perjantaina.",
            ),
            VocabularyEntry(
                "hakemus",
                "noun",
                "Kirjallinen pyyntö saada esimerkiksi työ tai opiskelupaikka.",
                "Lähetin hakemuksen eilen.",
            ),
            VocabularyEntry(
                "haastattelu",
                "noun",
                "Keskustelu, jossa kysymyksillä hankitaan tietoa henkilöstä tai aiheesta.",
                "Työhaastattelu meni hyvin.",
            ),
            VocabularyEntry(
                "tehtävä", "noun", "Asia, joka pitää tehdä tai ratkaista.", "Tein vaikean tehtävän."
            ),
            VocabularyEntry(
                "koe",
                "noun",
                "Tilanne, jossa osaamista mitataan kysymyksillä tai tehtävillä.",
                "Suomen koe oli maanantaina.",
            ),
            VocabularyEntry(
                "arvosana",
                "noun",
                "Numero tai muu arvio, joka kuvaa suorituksen tasoa.",
                "Sain kokeesta hyvän arvosanan.",
            ),
            VocabularyEntry(
                "todistus",
                "noun",
                "Asiakirja, joka vahvistaa esimerkiksi opintojen suorittamisen.",
                "Sain kurssilta todistuksen.",
            ),
            VocabularyEntry(
                "tutkinto",
                "noun",
                "Oppilaitoksessa suoritettu virallinen opintokokonaisuus.",
                "Hän suoritti tutkinnon Suomessa.",
            ),
            VocabularyEntry(
                "harjoitus",
                "noun",
                "Tehtävä tai toistuva toiminta, jolla kehitetään taitoa.",
                "Teimme ääntämisharjoituksen.",
            ),
            VocabularyEntry(
                "oppikirja",
                "noun",
                "Opiskelua varten kirjoitettu kirja.",
                "Luin oppikirjan ensimmäisen luvun.",
            ),
            VocabularyEntry(
                "muistiinpano",
                "noun",
                "Lyhyt kirjoitettu tieto muistamisen tueksi.",
                "Kirjoitin muistiinpanoja tunnilla.",
            ),
            VocabularyEntry(
                "kirjautua",
                "verb",
                "Avata oma käyttöyhteys palveluun tunnusten avulla.",
                "Kirjauduin kurssin sivulle.",
            ),
            VocabularyEntry(
                "lähettää",
                "verb",
                "Toimittaa viesti tai esine vastaanottajalle.",
                "Lähetin opettajalle sähköpostia.",
            ),
            VocabularyEntry(
                "palauttaa",
                "verb",
                "Antaa tehty työ arvioitavaksi tai viedä asia takaisin.",
                "Palautin tehtävän ajoissa.",
            ),
            VocabularyEntry(
                "hakea",
                "verb",
                "Pyrkiä saamaan paikka tai etuus hakemuksen avulla.",
                "Hain uutta työpaikkaa.",
            ),
            VocabularyEntry(
                "oppia", "verb", "Saada uusi tieto tai taito.", "Opin eilen uuden sanan."
            ),
            VocabularyEntry(
                "onnistua", "verb", "Saada aikaan toivottu tulos.", "Onnistuin tehtävässä."
            ),
            VocabularyEntry(
                "valmistua",
                "verb",
                "Saada opinnot päätökseen ja tutkinto suoritetuksi.",
                "Valmistuin viime vuonna.",
            ),
        ],
    ),
    VocabularySet(
        "fi_wellbeing_a2",
        "A2",
        "Terveys ja omat kokemukset",
        "a2-unit-5",
        [
            VocabularyEntry(
                "oire",
                "noun",
                "Kehon tai mielen merkki mahdollisesta sairaudesta.",
                "Oireet ovat jatkuneet kaksi päivää.",
            ),
            VocabularyEntry(
                "kuume",
                "noun",
                "Tavallista korkeampi kehon lämpötila sairauden aikana.",
                "Minulla on ollut kuumetta.",
            ),
            VocabularyEntry(
                "yskä",
                "noun",
                "Toistuva ilman voimakas puhaltuminen ulos hengitysteiden ärsytyksen vuoksi.",
                "Yskä on jatkunut viikon.",
            ),
            VocabularyEntry(
                "nuha", "noun", "Tila, jossa nenä vuotaa tai on tukossa.", "Minulla on nuha."
            ),
            VocabularyEntry(
                "kurkku",
                "noun",
                "Kaulan sisäinen alue, jonka kautta ilma ja ruoka kulkevat.",
                "Kurkku on ollut kipeä.",
            ),
            VocabularyEntry(
                "päänsärky", "noun", "Pään alueella tuntuva kipu.", "Päänsärky on helpottanut."
            ),
            VocabularyEntry(
                "allergia",
                "noun",
                "Elimistön haitallinen reaktio tavallisesti vaarattomaan aineeseen.",
                "Minulla on siitepölyallergia.",
            ),
            VocabularyEntry(
                "resepti",
                "noun",
                "Lääkärin määräys tietyn lääkkeen saamiseksi apteekista.",
                "Lääkäri on kirjoittanut reseptin.",
            ),
            VocabularyEntry(
                "annos",
                "noun",
                "Kerralla otettava tai tarjottava määrä.",
                "Lääkkeen annos lukee ohjeessa.",
            ),
            VocabularyEntry(
                "ajanvaraus",
                "noun",
                "Sopiminen tietystä palveluajasta etukäteen.",
                "Ajanvaraus onnistuu puhelimella.",
            ),
            VocabularyEntry(
                "terveyskeskus",
                "noun",
                "Paikka, jossa annetaan tavallisia terveydenhuollon palveluja.",
                "Olen soittanut terveyskeskukseen.",
            ),
            VocabularyEntry(
                "hammaslääkäri",
                "noun",
                "Ammattilainen, joka tutkii ja hoitaa suun ja hampaiden sairauksia.",
                "Olen varannut ajan hammaslääkärille.",
            ),
            VocabularyEntry(
                "potilas",
                "noun",
                "Henkilö, jota tutkitaan tai hoidetaan terveydenhuollossa.",
                "Potilas odottaa hoitajaa.",
            ),
            VocabularyEntry(
                "tutkimus",
                "noun",
                "Tarkastus tai selvitys, jolla hankitaan tietoa esimerkiksi terveydestä.",
                "Lääkäri on tehnyt tutkimuksen.",
            ),
            VocabularyEntry(
                "verikoe",
                "noun",
                "Tutkimus, jossa verinäytteestä selvitetään terveystietoa.",
                "Olen käynyt verikokeessa.",
            ),
            VocabularyEntry(
                "rokotus",
                "noun",
                "Rokotteen antaminen suojaksi tiettyä tautia vastaan.",
                "Olen saanut rokotuksen.",
            ),
            VocabularyEntry(
                "tapaturma",
                "noun",
                "Äkillinen vahinko, jossa ihminen loukkaantuu.",
                "Tapaturma sattui kotona.",
            ),
            VocabularyEntry(
                "haava",
                "noun",
                "Ihon tai muun kudoksen rikkoutunut kohta.",
                "Kädessä on pieni haava.",
            ),
            VocabularyEntry(
                "liikunta",
                "noun",
                "Kehon liikuttaminen terveyden tai kunnon vuoksi.",
                "Kevyt liikunta tekee minulle hyvää.",
            ),
            VocabularyEntry(
                "uni",
                "noun",
                "Nukkumisen tila, jossa keho ja mieli lepäävät.",
                "Olen saanut liian vähän unta.",
            ),
            VocabularyEntry(
                "ruokavalio",
                "noun",
                "Tapa, jolla ihminen valitsee ja syö ruokansa.",
                "Olen muuttanut ruokavaliotani.",
            ),
            VocabularyEntry(
                "toipua",
                "verb",
                "Saada voimia ja terveyttä takaisin sairauden jälkeen.",
                "Olen toipunut hitaasti.",
            ),
            VocabularyEntry("sairastua", "verb", "Tulla sairaaksi.", "Lapsi on sairastunut."),
            VocabularyEntry(
                "yskiä",
                "verb",
                "Puhaltaa ilmaa äkillisesti ulos hengitysteiden ärsytyksen vuoksi.",
                "Olen yskinyt koko yön.",
            ),
            VocabularyEntry(
                "mitata",
                "verb",
                "Selvittää jonkin asian määrä, koko tai arvo välineen avulla.",
                "Olen mitannut kuumeen.",
            ),
            VocabularyEntry(
                "parantua", "verb", "Tulla terveeksi tai parempaan kuntoon.", "Haava on parantunut."
            ),
        ],
    ),
    VocabularySet(
        "fi_leisure_nature_a2",
        "A2",
        "Luonto ja yhteinen vapaa-aika",
        "a2-unit-6",
        [
            VocabularyEntry(
                "metsä", "noun", "Laaja alue, jolla kasvaa paljon puita.", "Kävelemme metsässä."
            ),
            VocabularyEntry(
                "järvi", "noun", "Maan ympäröimä suuri vesialue.", "Järvi on tänään tyyni."
            ),
            VocabularyEntry("meri", "noun", "Laaja suolainen vesialue.", "Meren rannalla tuulee."),
            VocabularyEntry(
                "joki",
                "noun",
                "Luonnollinen uoma, jossa vesi virtaa.",
                "Joki kulkee kaupungin läpi.",
            ),
            VocabularyEntry(
                "saari",
                "noun",
                "Maa-alue, jota vesi ympäröi joka puolelta.",
                "Menemme saareen veneellä.",
            ),
            VocabularyEntry("polku", "noun", "Kapea kulkureitti maastossa.", "Seuraa tätä polkua."),
            VocabularyEntry(
                "mäki",
                "noun",
                "Ympäristöään korkeampi maaston kohta.",
                "Tämä mäki on jyrkempi kuin edellinen.",
            ),
            VocabularyEntry(
                "sää",
                "noun",
                "Ilman tila tietyssä paikassa ja tiettynä aikana.",
                "Huomenna sää on lämpimämpi.",
            ),
            VocabularyEntry(
                "sade", "noun", "Pilvistä maahan putoava vesi tai lumi.", "Sade loppuu illalla."
            ),
            VocabularyEntry(
                "lumi",
                "noun",
                "Valkoiset jääkiteet, joita sataa kylmällä ilmalla.",
                "Maassa on paljon lunta.",
            ),
            VocabularyEntry(
                "jää",
                "noun",
                "Vesi kiinteässä muodossa kylmyyden vuoksi.",
                "Älä mene heikolle jäälle.",
            ),
            VocabularyEntry(
                "pakkanen",
                "noun",
                "Nollaa astetta kylmempi ulkoilman lämpötila.",
                "Ulkona on kova pakkanen.",
            ),
            VocabularyEntry("tuuli", "noun", "Ulkoilman liike.", "Tuuli on voimakas."),
            VocabularyEntry(
                "aurinko",
                "noun",
                "Tähti, joka antaa maapallolle valoa ja lämpöä.",
                "Aurinko paistaa.",
            ),
            VocabularyEntry(
                "pilvi",
                "noun",
                "Ilmassa näkyvä vesipisaroiden tai jääkiteiden muodostuma.",
                "Taivaalla on tummia pilviä.",
            ),
            VocabularyEntry("vene", "noun", "Pieni vedessä kulkeva alus.", "Vene on rannassa."),
            VocabularyEntry(
                "teltta",
                "noun",
                "Kankaasta tehty siirrettävä suoja yöpymiseen.",
                "Pystytä teltta tähän.",
            ),
            VocabularyEntry(
                "eväät",
                "noun",
                "Mukaan otettu ruoka esimerkiksi matkalle tai retkelle.",
                "Ota eväät mukaan.",
            ),
            VocabularyEntry(
                "uimahalli",
                "noun",
                "Sisärakennus, jossa on altaita uimista varten.",
                "Uimahallin vesi on lämpimämpää kuin järven vesi.",
            ),
            VocabularyEntry(
                "konsertti",
                "noun",
                "Tilaisuus, jossa esitetään musiikkia yleisölle.",
                "Konsertti alkaa seitsemältä.",
            ),
            VocabularyEntry(
                "näyttely",
                "noun",
                "Yleisölle järjestetty kokoelma katsottavia teoksia tai esineitä.",
                "Museossa on uusi näyttely.",
            ),
            VocabularyEntry(
                "lippukassa",
                "noun",
                "Palvelupiste, josta ostetaan pääsylippuja.",
                "Lippukassa on sisäänkäynnin vieressä.",
            ),
            VocabularyEntry("uida", "verb", "Liikkua vedessä kehon avulla.", "Ui rannan lähellä."),
            VocabularyEntry(
                "hiihtää", "verb", "Liikkua lumella suksilla.", "Talvella hiihdän metsässä."
            ),
            VocabularyEntry(
                "luistella", "verb", "Liikkua jäällä luistimilla.", "Luistelemme kaukalossa."
            ),
            VocabularyEntry(
                "rentoutua",
                "verb",
                "Vapautua jännityksestä ja saada levollinen olo.",
                "Rentoudun luonnossa.",
            ),
        ],
    ),
    VocabularySet(
        "fi_communication_a2",
        "A2",
        "Viestit, sopiminen ja perustelut",
        "a2-unit-7",
        [
            VocabularyEntry(
                "viesti",
                "noun",
                "Toiselle välitetty lyhyt tieto tai teksti.",
                "Lähetän viestin, jos myöhästyn.",
            ),
            VocabularyEntry(
                "puhelu", "noun", "Puhelimella käytävä keskustelu.", "Puhelu kestää vain hetken."
            ),
            VocabularyEntry(
                "tapaaminen",
                "noun",
                "Sovittu hetki, jolloin ihmiset ovat yhdessä.",
                "Minun täytyy siirtää tapaamista.",
            ),
            VocabularyEntry(
                "kutsu",
                "noun",
                "Pyyntö tulla mukaan tilaisuuteen tai tapaamiseen.",
                "Kiitos kutsusta.",
            ),
            VocabularyEntry(
                "ehdotus", "noun", "Ajatus siitä, miten voisi toimia.", "Minulla on toinen ehdotus."
            ),
            VocabularyEntry(
                "päätös",
                "noun",
                "Valinta, jonka jälkeen tiedetään, miten toimitaan.",
                "Teemme päätöksen huomenna.",
            ),
            VocabularyEntry(
                "syy",
                "noun",
                "Asia, joka selittää tapahtuman tai toiminnan.",
                "Mikä on perumisen syy?",
            ),
            VocabularyEntry(
                "lupa",
                "noun",
                "Hyväksyntä sille, että jokin toiminta on sallittua.",
                "Tarvitsen luvan kuvan käyttöön.",
            ),
            VocabularyEntry(
                "ohje",
                "noun",
                "Tieto siitä, miten jokin asia tehdään.",
                "Luen ohjeen ennen aloittamista.",
            ),
            VocabularyEntry(
                "neuvo", "noun", "Ehdotus, joka auttaa toista toimimaan.", "Voitko antaa neuvon?"
            ),
            VocabularyEntry(
                "ongelma", "noun", "Vaikeus, johon tarvitaan ratkaisu.", "Kerron, mikä ongelma on."
            ),
            VocabularyEntry(
                "ratkaisu",
                "noun",
                "Keino, jolla vaikeus selvitetään.",
                "Tämä on meille hyvä ratkaisu.",
            ),
            VocabularyEntry(
                "mielipide",
                "noun",
                "Oma käsitys tai arvio asiasta.",
                "Haluan kuulla sinun mielipiteesi.",
            ),
            VocabularyEntry(
                "sopia",
                "verb",
                "Päättää yhdessä, mitä tehdään tai millä ehdoilla.",
                "Sovitaan, että tapaamme huomenna.",
            ),
            VocabularyEntry(
                "ehdottaa",
                "verb",
                "Esittää muille mahdollinen toimintatapa.",
                "Ehdotan, että menemme kirjastoon.",
            ),
            VocabularyEntry(
                "luvata",
                "verb",
                "Sanoa sitoutuvansa tekemään jotakin.",
                "Lupaan soittaa, kun pääsen kotiin.",
            ),
            VocabularyEntry(
                "selittää",
                "verb",
                "Tehdä asian merkitys tai syy ymmärrettäväksi.",
                "Voitko selittää tämän ohjeen?",
            ),
            VocabularyEntry(
                "muistaa",
                "verb",
                "Pitää tieto mielessä tai palauttaa se mieleen.",
                "Muistan, että kurssi alkaa tänään.",
            ),
            VocabularyEntry(
                "unohtaa",
                "verb",
                "Menettää tieto hetkeksi mielestä tai jättää asia muistamatta.",
                "Älä unohda tapaamista.",
            ),
            VocabularyEntry(
                "osata", "verb", "Hallita opittu taito.", "Osaan käyttää tätä ohjelmaa."
            ),
            VocabularyEntry(
                "saada",
                "verb",
                "Olla luvallista tehdä jotakin tässä käyttötavassa.",
                "Saat käyttää minun kynääni.",
            ),
            VocabularyEntry(
                "täytyä", "verb", "Olla välttämätöntä tai pakollista.", "Minun täytyy lähteä nyt."
            ),
            VocabularyEntry(
                "koska",
                "conjunction",
                "Sana, joka aloittaa syyn kertovan lauseen.",
                "Jään kotiin, koska olen sairas.",
            ),
            VocabularyEntry(
                "jos", "conjunction", "Sana, joka aloittaa ehdon.", "Tulen, jos ehdin."
            ),
            VocabularyEntry(
                "kun",
                "conjunction",
                "Sana, joka yhdistää tapahtuman toisen tapahtuman aikaan.",
                "Soitan, kun olen kotona.",
            ),
            VocabularyEntry(
                "että",
                "conjunction",
                "Sana, joka aloittaa esimerkiksi tiedon tai ajatuksen sisällön.",
                "Tiedän, että hän tulee.",
            ),
        ],
    ),
]
