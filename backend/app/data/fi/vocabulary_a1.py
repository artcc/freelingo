"""Finnish A1 vocabulary: seven practical sets of twenty-eight entries."""

from app.data._types import VocabularyEntry, VocabularySet

A1_SETS: list[VocabularySet] = [
    VocabularySet(
        "fi_first_contact_a1",
        "A1",
        "Ensimmäinen tapaaminen ja omat tiedot",
        "a1-unit-1",
        [
            VocabularyEntry(
                "nimi", "noun", "Sana, jolla ihminen tai asia tunnetaan.", "Minun nimeni on Aino."
            ),
            VocabularyEntry(
                "etunimi", "noun", "Henkilön oma nimi ennen sukunimeä.", "Eero on etunimi."
            ),
            VocabularyEntry(
                "sukunimi",
                "noun",
                "Nimi, joka on usein sama perheenjäsenillä.",
                "Minun sukunimeni on Laine.",
            ),
            VocabularyEntry(
                "ihminen",
                "noun",
                "Henkilö, esimerkiksi lapsi tai aikuinen.",
                "Hän on ystävällinen ihminen.",
            ),
            VocabularyEntry(
                "nainen", "noun", "Aikuinen naispuolinen ihminen.", "Tuo nainen on opettaja."
            ),
            VocabularyEntry(
                "mies", "noun", "Aikuinen miespuolinen ihminen.", "Tuo mies on opiskelija."
            ),
            VocabularyEntry(
                "lapsi", "noun", "Nuori ihminen, joka ei ole vielä aikuinen.", "Lapsi on täällä."
            ),
            VocabularyEntry(
                "ystävä",
                "noun",
                "Läheinen ihminen, jonka kanssa on hyvä olla.",
                "Aino on minun ystäväni.",
            ),
            VocabularyEntry(
                "opettaja",
                "noun",
                "Ihminen, jonka työ on auttaa muita oppimaan.",
                "Hän on suomen opettaja.",
            ),
            VocabularyEntry(
                "opiskelija",
                "noun",
                "Ihminen, joka oppii esimerkiksi oppilaitoksessa.",
                "Olen uusi opiskelija.",
            ),
            VocabularyEntry(
                "kieli",
                "noun",
                "Sanojen ja sääntöjen järjestelmä, jolla ihmiset viestivät.",
                "Suomi on uusi kieli minulle.",
            ),
            VocabularyEntry("sana", "noun", "Kielen osa, jolla on merkitys.", "Hei on lyhyt sana."),
            VocabularyEntry(
                "kirjain", "noun", "Kirjoituksen merkki, esimerkiksi a tai ä.", "Ä on kirjain."
            ),
            VocabularyEntry("ääni", "noun", "Se, minkä voi kuulla.", "Opettajan ääni on selvä."),
            VocabularyEntry(
                "kotimaa",
                "noun",
                "Maa, josta ihminen on kotoisin tai jonka hän kokee omakseen.",
                "Minun kotimaani on Suomi.",
            ),
            VocabularyEntry(
                "suomalainen",
                "adjective",
                "Suomeen tai sen ihmisiin kuuluva.",
                "Tämä on suomalainen nimi.",
            ),
            VocabularyEntry(
                "suomi",
                "noun",
                "Suomessa puhuttu kieli, jossa on esimerkiksi sanat hei ja kiitos.",
                "Suomi on minun äidinkieleni.",
            ),
            VocabularyEntry(
                "maa", "noun", "Alue, jolla on oma valtio ja rajat.", "Suomi on yksi maa."
            ),
            VocabularyEntry(
                "kaupunki",
                "noun",
                "Suuri asuttu paikka, jossa on katuja ja palveluja.",
                "Turku on vanha kaupunki.",
            ),
            VocabularyEntry(
                "osoite",
                "noun",
                "Tieto siitä, missä ihminen asuu tai paikka sijaitsee.",
                "Osoite on Koivukatu 2.",
            ),
            VocabularyEntry(
                "puhelinnumero",
                "noun",
                "Numerosarja, jonka avulla voi soittaa ihmiselle.",
                "Tämä on minun puhelinnumeroni.",
            ),
            VocabularyEntry(
                "sähköposti",
                "noun",
                "Verkon kautta lähetettävä kirjallinen viesti tai viestipalvelu.",
                "Tämä sähköposti on opettajalta.",
            ),
            VocabularyEntry(
                "minä", "pronoun", "Sana, jolla puhuja viittaa itseensä.", "Minä olen Eero."
            ),
            VocabularyEntry(
                "sinä", "pronoun", "Sana yhdelle ihmiselle, jolle puhutaan.", "Sinä olet Aino."
            ),
            VocabularyEntry(
                "hän", "pronoun", "Sana yhdestä ihmisestä, josta puhutaan.", "Hän on opettaja."
            ),
            VocabularyEntry(
                "me", "pronoun", "Puhuja ja vähintään yksi muu ihminen.", "Me olemme täällä."
            ),
            VocabularyEntry(
                "te",
                "pronoun",
                "Useat kuulijat tai kohteliaasti puhuteltu yksi kuulija.",
                "Te olette täällä.",
            ),
            VocabularyEntry(
                "he", "pronoun", "Useat ihmiset, joista puhutaan.", "He ovat Suomessa."
            ),
        ],
    ),
    VocabularySet(
        "fi_people_home_a1",
        "A1",
        "Perhe ja kodin tavarat",
        "a1-unit-2",
        [
            VocabularyEntry(
                "perhe",
                "noun",
                "Läheisten ihmisten ryhmä, esimerkiksi vanhemmat ja lapset.",
                "Tämä on Ainon perhe.",
            ),
            VocabularyEntry("äiti", "noun", "Lapsen naispuolinen vanhempi.", "Äiti on kotona."),
            VocabularyEntry("isä", "noun", "Lapsen miespuolinen vanhempi.", "Isä on opettaja."),
            VocabularyEntry(
                "sisko",
                "noun",
                "Tyttö tai nainen, jolla on kanssasi yhteinen vanhempi.",
                "Minun siskoni on opiskelija.",
            ),
            VocabularyEntry(
                "veli",
                "noun",
                "Poika tai mies, jolla on kanssasi yhteinen vanhempi.",
                "Eero on Ainon veli.",
            ),
            VocabularyEntry("vauva", "noun", "Hyvin pieni lapsi.", "Vauva on pieni."),
            VocabularyEntry(
                "koti",
                "noun",
                "Paikka, jossa ihminen asuu ja elää arkeaan.",
                "Tämä on minun kotini.",
            ),
            VocabularyEntry(
                "talo", "noun", "Rakennus, jossa voi esimerkiksi asua.", "Talo on suuri."
            ),
            VocabularyEntry(
                "asunto",
                "noun",
                "Yhden ihmisen tai perheen asumiseen tarkoitettu tila.",
                "Asunto on uusi.",
            ),
            VocabularyEntry(
                "huone", "noun", "Seinien erottama osa rakennuksen sisällä.", "Tämä huone on pieni."
            ),
            VocabularyEntry(
                "keittiö",
                "noun",
                "Huone tai tila, jossa valmistetaan ruokaa.",
                "Keittiö on valoisa.",
            ),
            VocabularyEntry(
                "ovi", "noun", "Avattava osa, jonka kautta kuljetaan huoneeseen.", "Ovi on auki."
            ),
            VocabularyEntry(
                "ikkuna",
                "noun",
                "Seinässä oleva lasinen osa, josta näkee ulos.",
                "Ikkuna on suuri.",
            ),
            VocabularyEntry(
                "pöytä",
                "noun",
                "Huonekalu, jonka tasolla voi syödä tai kirjoittaa.",
                "Tämä on keittiön pöytä.",
            ),
            VocabularyEntry(
                "tuoli",
                "noun",
                "Tavallisesti yhdelle ihmiselle tarkoitettu istuin.",
                "Tuoli on vanha.",
            ),
            VocabularyEntry("sänky", "noun", "Huonekalu, jossa nukutaan.", "Sänky on pehmeä."),
            VocabularyEntry("lamppu", "noun", "Esine, joka antaa valoa.", "Lamppu on uusi."),
            VocabularyEntry(
                "kirja", "noun", "Sivuista koottu teos, jota luetaan.", "Tämä on suomen kirja."
            ),
            VocabularyEntry(
                "kynä", "noun", "Väline, jolla kirjoitetaan tai piirretään.", "Tämä on Eeron kynä."
            ),
            VocabularyEntry(
                "avain", "noun", "Väline, jolla lukon saa auki.", "Tämä on kodin avain."
            ),
            VocabularyEntry(
                "laukku", "noun", "Esine, jossa kannetaan tavaroita.", "Ainon laukku on suuri."
            ),
            VocabularyEntry(
                "puhelin",
                "noun",
                "Laite, jolla voi soittaa ja lähettää viestejä.",
                "Puhelin on uusi.",
            ),
            VocabularyEntry(
                "koira",
                "noun",
                "Haukkuva eläin, jota pidetään usein lemmikkinä.",
                "Koira on pieni.",
            ),
            VocabularyEntry(
                "kissa", "noun", "Naukuva eläin, jota pidetään usein lemmikkinä.", "Kissa on musta."
            ),
            VocabularyEntry(
                "pieni",
                "adjective",
                "Kooltaan vähäinen; suuren vastakohta.",
                "Tämä on pieni huone.",
            ),
            VocabularyEntry(
                "suuri",
                "adjective",
                "Kooltaan huomattava; pienen vastakohta.",
                "Tämä talo on suuri.",
            ),
            VocabularyEntry(
                "uusi",
                "adjective",
                "Vasta tehty, hankittu tai käyttöön tullut.",
                "Tämä on uusi pöytä.",
            ),
            VocabularyEntry(
                "vanha", "adjective", "Kauan elänyt tai olemassa ollut.", "Talo on vanha."
            ),
        ],
    ),
    VocabularySet(
        "fi_daily_life_a1",
        "A1",
        "Päivän tekemiset",
        "a1-unit-3",
        [
            VocabularyEntry(
                "olla",
                "verb",
                "Ilmaista esimerkiksi olemassaoloa, tilaa tai sijaintia.",
                "Olen kotona.",
            ),
            VocabularyEntry("asua", "verb", "Pitää kotia jossakin paikassa.", "Asun Turussa."),
            VocabularyEntry(
                "puhua", "verb", "Ilmaista ajatuksia sanoilla ääneen.", "Puhun vähän suomea."
            ),
            VocabularyEntry(
                "opiskella",
                "verb",
                "Hankkia tietoa tai taitoa harjoittelemalla.",
                "Opiskelen joka päivä.",
            ),
            VocabularyEntry(
                "lukea",
                "verb",
                "Katsoa kirjoitusta ja ymmärtää sen sisältöä.",
                "Luen suomen kirjaa.",
            ),
            VocabularyEntry(
                "kirjoittaa", "verb", "Tuottaa tekstiä käsin tai laitteella.", "Kirjoitan viestiä."
            ),
            VocabularyEntry("kuunnella", "verb", "Seurata ääntä tarkasti.", "Kuuntelen opettajaa."),
            VocabularyEntry(
                "katsoa", "verb", "Suunnata silmät johonkin ja seurata sitä.", "Katson kuvaa."
            ),
            VocabularyEntry("mennä", "verb", "Liikkua kohti toista paikkaa.", "Menen kotiin."),
            VocabularyEntry(
                "tulla", "verb", "Liikkua kohti puhujan tai tilanteen paikkaa.", "Tuletko tänne?"
            ),
            VocabularyEntry("syödä", "verb", "Ottaa ruokaa suuhun ja niellä se.", "Syön leipää."),
            VocabularyEntry("juoda", "verb", "Ottaa nestettä suuhun ja niellä se.", "Juon vettä."),
            VocabularyEntry("nukkua", "verb", "Levätä unessa.", "Lapsi nukkuu."),
            VocabularyEntry(
                "herätä", "verb", "Lopettaa nukkuminen ja tulla valveille.", "Herään aikaisin."
            ),
            VocabularyEntry(
                "tehdä",
                "verb",
                "Suorittaa jokin toiminta tai valmistaa jotakin.",
                "Mitä sinä teet?",
            ),
            VocabularyEntry(
                "kävellä", "verb", "Liikkua jaloilla askel kerrallaan.", "Kävelen kotiin."
            ),
            VocabularyEntry(
                "istua", "verb", "Olla esimerkiksi tuolilla vartalo pystyssä.", "Istun tässä."
            ),
            VocabularyEntry(
                "seisoa", "verb", "Olla pystyssä jalkojen varassa.", "Seison oven vieressä."
            ),
            VocabularyEntry(
                "ymmärtää",
                "verb",
                "Saada selville asian tai viestin merkitys.",
                "En ymmärrä tätä sanaa.",
            ),
            VocabularyEntry("kysyä", "verb", "Pyytää toiselta tietoa.", "Kysyn opettajalta."),
            VocabularyEntry(
                "vastata", "verb", "Antaa tieto tai reaktio kysymykseen.", "Opettaja vastaa."
            ),
            VocabularyEntry("alkaa", "verb", "Tulla käyntiin tai saada alku.", "Kurssi alkaa nyt."),
            VocabularyEntry(
                "loppua", "verb", "Päättyä tai tulla käytetyksi kokonaan.", "Työ loppuu pian."
            ),
            VocabularyEntry(
                "työ",
                "noun",
                "Tehtävä tai toiminta, jota tehdään usein palkkaa vastaan.",
                "Työ alkaa aamulla.",
            ),
            VocabularyEntry(
                "koulu", "noun", "Paikka tai yhteisö, jossa oppilaat oppivat.", "Koulu on lähellä."
            ),
            VocabularyEntry(
                "kurssi", "noun", "Tietyn aiheen opetuskokonaisuus.", "Suomen kurssi alkaa tänään."
            ),
            VocabularyEntry(
                "aina", "adverb", "Joka kerta tai kaikkina aikoina.", "Juon aina aamulla vettä."
            ),
            VocabularyEntry(
                "usein", "adverb", "Monta kertaa; ei vain harvoin.", "Kävelen usein kouluun."
            ),
        ],
    ),
    VocabularySet(
        "fi_food_shopping_a1",
        "A1",
        "Ruoka, raha ja määrät",
        "a1-unit-4",
        [
            VocabularyEntry(
                "vesi", "noun", "Väritön neste, jota ihminen tarvitsee juotavaksi.", "Juon vettä."
            ),
            VocabularyEntry(
                "kahvi",
                "noun",
                "Paahdetuista pavuista valmistettu tumma juoma.",
                "Kahvi on kuumaa.",
            ),
            VocabularyEntry(
                "tee",
                "noun",
                "Juoma, joka valmistetaan yleensä kasvin lehdistä ja kuumasta vedestä.",
                "Haluan teetä.",
            ),
            VocabularyEntry(
                "maito",
                "noun",
                "Vaalea juoma, jota saadaan esimerkiksi lehmästä.",
                "Kahvissa on maitoa.",
            ),
            VocabularyEntry(
                "leipä",
                "noun",
                "Jauhoista ja nesteestä valmistettu paistettu ruoka.",
                "Syön leipää aamulla.",
            ),
            VocabularyEntry(
                "voi", "noun", "Maidon rasvasta valmistettu levite.", "Leivällä on voita."
            ),
            VocabularyEntry(
                "juusto", "noun", "Maidosta valmistettu usein kiinteä ruoka.", "Ostan juustoa."
            ),
            VocabularyEntry(
                "omena", "noun", "Pyöreä hedelmä, joka kasvaa puussa.", "Minulla on kaksi omenaa."
            ),
            VocabularyEntry(
                "banaani",
                "noun",
                "Pitkä hedelmä, jonka kuori on kypsänä yleensä keltainen.",
                "Banaani on makea.",
            ),
            VocabularyEntry(
                "peruna",
                "noun",
                "Maan alla kasvava mukula, jota syödään kypsennettynä.",
                "Keitän kolme perunaa.",
            ),
            VocabularyEntry(
                "kala", "noun", "Vedessä elävä eläin tai siitä tehty ruoka.", "Syön kalaa."
            ),
            VocabularyEntry(
                "liha", "noun", "Eläimestä saatava ruoka, esimerkiksi naudanliha.", "En syö lihaa."
            ),
            VocabularyEntry(
                "riisi",
                "noun",
                "Pienijyväinen vilja, joka keitetään ruoaksi.",
                "Ruoassa on riisiä.",
            ),
            VocabularyEntry(
                "ruoka", "noun", "Se, mitä ihminen syö saadakseen energiaa.", "Ruoka on valmista."
            ),
            VocabularyEntry(
                "kauppa", "noun", "Paikka, jossa myydään tavaroita tai ruokaa.", "Kauppa on auki."
            ),
            VocabularyEntry(
                "kahvila",
                "noun",
                "Paikka, josta voi ostaa juomia ja pientä syötävää.",
                "Tämä kahvila on pieni.",
            ),
            VocabularyEntry(
                "raha",
                "noun",
                "Maksamiseen käytettävä arvo, esimerkiksi kolikot ja setelit.",
                "Minulla ei ole rahaa mukana.",
            ),
            VocabularyEntry(
                "euro",
                "noun",
                "Suomessa käytettävän valuutan yksikkö.",
                "Leipä maksaa kaksi euroa.",
            ),
            VocabularyEntry(
                "hinta",
                "noun",
                "Rahamäärä, joka tuotteesta tai palvelusta maksetaan.",
                "Mikä tämän hinta on?",
            ),
            VocabularyEntry(
                "kuitti", "noun", "Todistus maksetusta ostoksesta.", "Tässä on kuitti."
            ),
            VocabularyEntry("yksi", "numeral", "Luku 1; vain yksi kappale.", "Yksi kahvi, kiitos."),
            VocabularyEntry("kaksi", "numeral", "Luku 2; yksi ja yksi.", "Ostan kaksi omenaa."),
            VocabularyEntry("kolme", "numeral", "Luku 3; kaksi ja yksi.", "Tässä on kolme euroa."),
            VocabularyEntry("neljä", "numeral", "Luku 4; kaksi ja kaksi.", "Meitä on neljä."),
            VocabularyEntry("viisi", "numeral", "Luku 5; neljä ja yksi.", "Hinta on viisi euroa."),
            VocabularyEntry(
                "kuusi", "numeral", "Luku 6; viisi ja yksi.", "Pussissa on kuusi perunaa."
            ),
            VocabularyEntry(
                "kymmenen",
                "numeral",
                "Luku 10; kahden käden sormien määrä tavallisesti.",
                "Minulla on kymmenen euroa.",
            ),
            VocabularyEntry(
                "sata", "numeral", "Luku 100; kymmenen kertaa kymmenen.", "Tämä maksaa sata euroa."
            ),
        ],
    ),
    VocabularySet(
        "fi_places_transport_a1",
        "A1",
        "Paikat ja liikkuminen",
        "a1-unit-5",
        [
            VocabularyEntry(
                "katu",
                "noun",
                "Kaupungin kulkuväylä, jonka varrella on usein rakennuksia.",
                "Asun tällä kadulla.",
            ),
            VocabularyEntry(
                "tie",
                "noun",
                "Reitti, jota pitkin ihmiset ja ajoneuvot kulkevat.",
                "Tie menee kylään.",
            ),
            VocabularyEntry(
                "tori",
                "noun",
                "Avoin paikka, jossa voi olla myyjiä ja tapahtumia.",
                "Olen torilla.",
            ),
            VocabularyEntry(
                "asema", "noun", "Paikka, josta esimerkiksi junat lähtevät.", "Menen asemalle."
            ),
            VocabularyEntry(
                "pysäkki",
                "noun",
                "Paikka, jossa bussi tai raitiovaunu ottaa matkustajia.",
                "Odotan pysäkillä.",
            ),
            VocabularyEntry(
                "bussi", "noun", "Suuri auto, jossa kulkee monta matkustajaa.", "Tulen bussilla."
            ),
            VocabularyEntry(
                "juna",
                "noun",
                "Raiteilla kulkeva kulkuväline, jossa on vaunuja.",
                "Juna tulee asemalle.",
            ),
            VocabularyEntry(
                "raitiovaunu",
                "noun",
                "Kaupungin kiskoilla kulkeva joukkoliikenneväline.",
                "Menen raitiovaunulla keskustaan.",
            ),
            VocabularyEntry(
                "metro",
                "noun",
                "Kaupungin raideliikenneväline, joka kulkee usein maan alla.",
                "Metro on nopea.",
            ),
            VocabularyEntry(
                "auto",
                "noun",
                "Moottorilla kulkeva ajoneuvo muutamalle ihmiselle.",
                "Auto on kadulla.",
            ),
            VocabularyEntry(
                "polkupyörä",
                "noun",
                "Kaksipyöräinen kulkuväline, jota liikutetaan polkemalla.",
                "Tulen polkupyörällä.",
            ),
            VocabularyEntry(
                "lippu",
                "noun",
                "Todiste oikeudesta matkustaa tai päästä tilaisuuteen.",
                "Ostan lipun Turkuun.",
            ),
            VocabularyEntry(
                "kartta", "noun", "Kuva, joka näyttää alueen paikat ja reitit.", "Katson karttaa."
            ),
            VocabularyEntry(
                "kirjasto",
                "noun",
                "Paikka, josta voi lainata kirjoja ja muuta aineistoa.",
                "Opiskelen kirjastossa.",
            ),
            VocabularyEntry(
                "apteekki", "noun", "Liike, jossa myydään lääkkeitä.", "Apteekki on lähellä."
            ),
            VocabularyEntry(
                "sairaala",
                "noun",
                "Paikka, jossa hoidetaan sairaita ihmisiä.",
                "Hän on sairaalassa.",
            ),
            VocabularyEntry(
                "hotelli",
                "noun",
                "Paikka, josta voi maksua vastaan saada huoneen yöksi.",
                "Asun nyt hotellissa.",
            ),
            VocabularyEntry(
                "ravintola",
                "noun",
                "Paikka, jossa asiakas tilaa ja syö valmistettua ruokaa.",
                "Syömme ravintolassa.",
            ),
            VocabularyEntry(
                "puisto",
                "noun",
                "Yhteinen viheralue, jossa on esimerkiksi puita ja penkkejä.",
                "Kävelen puistossa.",
            ),
            VocabularyEntry("ranta", "noun", "Maan ja veden kohtaamispaikka.", "Menen rannalle."),
            VocabularyEntry(
                "silta",
                "noun",
                "Rakenne, jonka yli pääsee esimerkiksi joen toiselle puolelle.",
                "Bussi kulkee sillalla.",
            ),
            VocabularyEntry(
                "vasen",
                "adjective",
                "Oikean vastakkainen puoli.",
                "Kauppa on kadun vasemmalla puolella.",
            ),
            VocabularyEntry(
                "oikea",
                "adjective",
                "Vasemman vastakkainen puoli.",
                "Pysäkki on oikealla puolella.",
            ),
            VocabularyEntry(
                "suoraan", "adverb", "Eteenpäin ilman kääntymistä.", "Kävelen suoraan asemalle."
            ),
            VocabularyEntry(
                "lähellä", "adverb", "Vain lyhyen matkan päässä.", "Kirjasto on lähellä."
            ),
            VocabularyEntry("kaukana", "adverb", "Pitkän matkan päässä.", "Asema on kaukana."),
            VocabularyEntry(
                "täällä",
                "adverb",
                "Tässä paikassa tai tällä alueella, missä puhuja on.",
                "Olen täällä.",
            ),
            VocabularyEntry(
                "siellä",
                "adverb",
                "Toisessa paikassa, johon puhuja viittaa.",
                "Ystävä asuu siellä.",
            ),
        ],
    ),
    VocabularySet(
        "fi_time_leisure_a1",
        "A1",
        "Ajankohdat ja vapaa-aika",
        "a1-unit-6",
        [
            VocabularyEntry(
                "päivä",
                "noun",
                "Vuorokauden valoisa osa tai yksi kalenterin ajanjakso.",
                "Tänään on hyvä päivä.",
            ),
            VocabularyEntry(
                "viikko", "noun", "Seitsemän päivän ajanjakso.", "Kurssi alkaa ensi viikolla."
            ),
            VocabularyEntry(
                "kuukausi",
                "noun",
                "Vuoden kahdestoista osa, esimerkiksi tammikuu.",
                "Tämä kuukausi on marraskuu.",
            ),
            VocabularyEntry(
                "vuosi",
                "noun",
                "Kahdentoista kuukauden ajanjakso.",
                "Vuodessa on kaksitoista kuukautta.",
            ),
            VocabularyEntry(
                "maanantai",
                "noun",
                "Viikon ensimmäinen päivä suomalaisessa kalenterissa.",
                "Maanantaina olen töissä.",
            ),
            VocabularyEntry(
                "tiistai",
                "noun",
                "Maanantain jälkeinen viikonpäivä.",
                "Tiistaina on suomen kurssi.",
            ),
            VocabularyEntry(
                "keskiviikko",
                "noun",
                "Tiistain ja torstain välinen päivä.",
                "Keskiviikkona opiskelen kotona.",
            ),
            VocabularyEntry(
                "torstai",
                "noun",
                "Keskiviikon jälkeinen viikonpäivä.",
                "Torstaina menen kirjastoon.",
            ),
            VocabularyEntry(
                "perjantai",
                "noun",
                "Torstain ja lauantain välinen päivä.",
                "Perjantaina tapaan ystävän.",
            ),
            VocabularyEntry(
                "lauantai",
                "noun",
                "Perjantain jälkeinen viikonpäivä, osa viikonloppua.",
                "Lauantaina käyn torilla.",
            ),
            VocabularyEntry(
                "sunnuntai",
                "noun",
                "Lauantain jälkeinen viikonpäivä ennen maanantaita.",
                "Sunnuntaina nukun pitkään.",
            ),
            VocabularyEntry("aamu", "noun", "Päivän alku yön jälkeen.", "Aamulla juon kahvia."),
            VocabularyEntry("ilta", "noun", "Päivän loppu ennen yötä.", "Illalla luen kirjaa."),
            VocabularyEntry("yö", "noun", "Aika illan ja aamun välillä.", "Yöllä nukun."),
            VocabularyEntry(
                "tunti", "noun", "Kuudenkymmenen minuutin ajanjakso.", "Matka kestää tunnin."
            ),
            VocabularyEntry(
                "minuutti",
                "noun",
                "Kuudenkymmenen sekunnin ajanjakso.",
                "Bussi tulee viiden minuutin päästä.",
            ),
            VocabularyEntry("tänään", "adverb", "Tänä päivänä.", "Tänään on tiistai."),
            VocabularyEntry(
                "huomenna", "adverb", "Tätä päivää seuraavana päivänä.", "Tapaamme huomenna."
            ),
            VocabularyEntry(
                "eilen", "adverb", "Tätä päivää edeltävänä päivänä.", "Eilen oli maanantai."
            ),
            VocabularyEntry("nyt", "adverb", "Tällä hetkellä.", "Lähden nyt."),
            VocabularyEntry(
                "myöhemmin",
                "adverb",
                "Jonkin ajan kuluttua tai toisen ajankohdan jälkeen.",
                "Nähdään myöhemmin.",
            ),
            VocabularyEntry(
                "viikonloppu",
                "noun",
                "Viikon lopun päivät, tavallisesti lauantai ja sunnuntai.",
                "Viikonloppuna olen kotona.",
            ),
            VocabularyEntry(
                "vapaa-aika",
                "noun",
                "Aika, jolloin ei tarvitse tehdä työtä tai opiskella.",
                "Vapaa-ajalla kuuntelen musiikkia.",
            ),
            VocabularyEntry(
                "musiikki",
                "noun",
                "Sävelistä ja rytmistä muodostuva kuunneltava taide.",
                "Kuuntelen suomalaista musiikkia.",
            ),
            VocabularyEntry(
                "elokuva",
                "noun",
                "Liikkuvilla kuvilla kerrottu tarina tai muu teos.",
                "Elokuva alkaa kello kuusi.",
            ),
            VocabularyEntry(
                "peli",
                "noun",
                "Sääntöihin perustuva tekeminen, usein huvin vuoksi.",
                "Tämä peli on hauska.",
            ),
            VocabularyEntry(
                "harrastus",
                "noun",
                "Mieluinen toiminta, jota tekee vapaa-ajalla toistuvasti.",
                "Lukeminen on minun harrastukseni.",
            ),
            VocabularyEntry(
                "tavata",
                "verb",
                "Olla toisen ihmisen kanssa sovitusti tai sattumalta.",
                "Tapaan ystävän kahvilassa.",
            ),
        ],
    ),
    VocabularySet(
        "fi_health_help_a1",
        "A1",
        "Vointi ja avun pyytäminen",
        "a1-unit-7",
        [
            VocabularyEntry(
                "apu", "noun", "Toiminta, joka helpottaa toisen tilannetta.", "Tarvitsen apua."
            ),
            VocabularyEntry(
                "auttaa",
                "verb",
                "Tehdä jotakin toisen tilanteen helpottamiseksi.",
                "Voitko auttaa minua?",
            ),
            VocabularyEntry(
                "tarvita",
                "verb",
                "Olla jonkin tarpeessa tai pitää jotakin välttämättömänä.",
                "Tarvitsen vettä.",
            ),
            VocabularyEntry(
                "haluta",
                "verb",
                "Toivoa jotakin itselleen tai toivoa tekevänsä jotakin.",
                "Haluan mennä kotiin.",
            ),
            VocabularyEntry(
                "voida", "verb", "Olla mahdollista tehdä jotakin.", "Voin tulla huomenna."
            ),
            VocabularyEntry(
                "pää",
                "noun",
                "Kehon ylin osa, jossa ovat esimerkiksi aivot ja silmät.",
                "Minun pääni on kipeä.",
            ),
            VocabularyEntry(
                "käsi", "noun", "Kehon osa, jolla voi tarttua esineeseen.", "Nostan käden."
            ),
            VocabularyEntry(
                "jalka",
                "noun",
                "Kehon osa, jonka varassa seisotaan ja kävellään.",
                "Jalka on kipeä.",
            ),
            VocabularyEntry("silmä", "noun", "Elin, jolla näkee.", "Silmä on punainen."),
            VocabularyEntry("korva", "noun", "Kehon osa, jolla kuulee.", "Korva on kipeä."),
            VocabularyEntry(
                "suu", "noun", "Kasvojen osa, jolla syödään ja puhutaan.", "Suu on kuiva."
            ),
            VocabularyEntry(
                "hammas", "noun", "Kova osa suussa, jolla purraan ruokaa.", "Hammas on kipeä."
            ),
            VocabularyEntry(
                "vatsa",
                "noun",
                "Kehon keskiosan alue, jossa on ruoansulatuselimiä.",
                "Minun vatsani on kipeä.",
            ),
            VocabularyEntry(
                "selkä", "noun", "Vartalon takapuoli niskasta lantioon.", "Selkä on kipeä."
            ),
            VocabularyEntry(
                "kipu", "noun", "Ikävä tunne kehossa, esimerkiksi vamman vuoksi.", "Kipu on kova."
            ),
            VocabularyEntry(
                "kipeä", "adjective", "Sellainen, jossa tuntuu kipua.", "Käsi on kipeä."
            ),
            VocabularyEntry(
                "sairas",
                "adjective",
                "Sellainen, jonka terveys ei ole kunnossa.",
                "Olen tänään sairas.",
            ),
            VocabularyEntry(
                "terve", "adjective", "Sellainen, jolla ei ole sairautta.", "Lapsi on terve."
            ),
            VocabularyEntry(
                "väsynyt",
                "adjective",
                "Sellainen, joka tarvitsee lepoa tai unta.",
                "Olen illalla väsynyt.",
            ),
            VocabularyEntry(
                "lääkäri",
                "noun",
                "Ammattilainen, joka tutkii ja hoitaa sairauksia.",
                "Haluan puhua lääkärin kanssa.",
            ),
            VocabularyEntry(
                "hoitaja",
                "noun",
                "Ammattilainen, joka huolehtii potilaiden hoidosta.",
                "Hoitaja auttaa minua.",
            ),
            VocabularyEntry(
                "lääke",
                "noun",
                "Aine tai valmiste, jolla hoidetaan tai ehkäistään sairautta.",
                "Tarvitsen lääkettä.",
            ),
            VocabularyEntry(
                "levätä", "verb", "Pitää taukoa ja antaa kehon palautua.", "Haluan levätä."
            ),
            VocabularyEntry(
                "soittaa",
                "verb",
                "Ottaa puhelimella yhteyttä toiseen.",
                "Voitko soittaa lääkärille?",
            ),
            VocabularyEntry(
                "odottaa",
                "verb",
                "Olla paikalla tai antaa ajan kulua ennen jotakin.",
                "Odotan hoitajaa.",
            ),
            VocabularyEntry(
                "hätä", "noun", "Vakava tilanne, jossa tarvitaan nopeasti apua.", "Minulla on hätä."
            ),
            VocabularyEntry("nälkä", "noun", "Tunne, että tarvitsee ruokaa.", "Minulla on nälkä."),
            VocabularyEntry("jano", "noun", "Tunne, että tarvitsee juotavaa.", "Minulla on jano."),
        ],
    ),
]
