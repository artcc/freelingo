"""Finnish C2 placement items on inference, voice and precise mediation."""

from app.data._types import AssessmentQuestion

C2_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "fi-g-c2-001",
        "grammar",
        "C2",
        "Selvityksessä todetaan: «On varmaa, että vika on saattanut vaikuttaa tulokseen, "
        "mutta vaikutuksen toteutumisesta ei ole näyttöä.» Mikä yhteenveto säilyttää rajauksen?",
        [
            "Vian vaikutus tulokseen on varmistettu, mutta sen suuruudesta tarvitaan lisänäyttöä.",
            "Vian olemassaolo on jäänyt epäselväksi, mutta sen vaikutus tulokseen on vahvistettu.",
            "Vaikutusmahdollisuus on vahvistettu, mutta tapahtunutta vaikutusta ei ole osoitettu.",
            "Vaikutus on osoitettu vähäiseksi, mutta sen tarkkaa mekanismia ei vielä tunneta.",
        ],
        "Vaikutusmahdollisuus on vahvistettu, mutta tapahtunutta vaikutusta ei ole osoitettu.",
        "fi-nested-modality-c2",
    ),
    AssessmentQuestion(
        "fi-g-c2-002",
        "grammar",
        "C2",
        "Haastattelija kysyy: «Miksi lykkäätte päätöstä taas?» Päätös on koko ajan ollut "
        "tarkoitus tehdä perjantaina, joka on huomenna. Haluat oikaista kysymyksen lähtökohdan "
        "ja kertoa etenemisestä. Mikä vastaus sopii?",
        [
            "Aikataulu ei ole muuttunut. Päätös tehdään suunnitellusti huomenna.",
            "Ymmärrän huolen toistuvasta viiveestä. Päätös tehdään huomenna.",
            "Tällä kertaa lisäaika on tarpeen. Päätös tehdään huomenna.",
            "Lykkäys jäi onneksi lyhyeksi. Päätös tehdään huomenna.",
        ],
        "Aikataulu ei ole muuttunut. Päätös tehdään suunnitellusti huomenna.",
        "fi-presuppositions-c2",
    ),
    AssessmentQuestion(
        "fi-g-c2-003",
        "grammar",
        "C2",
        "Lautakunta hyväksyi «esityksen tilapäisten rajoitusten jatkamisen edellytysten "
        "selvittämisestä». Mikä tiedote vastaa päätöksen sisältöä?",
        [
            "Lautakunta hyväksyi rajoitusten jatkamisen, ja selvityksessä määritellään jatkon kesto.",
            "Lautakunta hyväksyi nykyisten rajoitusten poistamisen selvityksen valmistumiseen asti.",
            "Lautakunta hyväksyi rajoitusten muuttamisen pysyviksi, jos selvitys tukee ratkaisua.",
            "Lautakunta hyväksyi selvityksen tekemisen siitä, millä ehdoilla rajoituksia voisi jatkaa.",
        ],
        "Lautakunta hyväksyi selvityksen tekemisen siitä, millä ehdoilla rajoituksia voisi jatkaa.",
        "fi-dense-noun-phrases-c2",
    ),
    AssessmentQuestion(
        "fi-g-c2-004",
        "grammar",
        "C2",
        "«Leena työnsi kirjeen laatikkoon. Taas yksi kohtuuton vaatimus. "
        "Miksi juuri hänen piti aina joustaa? Illalla hän kuitenkin avasi kirjeen uudelleen.» "
        "Mikä tulkinta suhtautuu tekstin näkökulmaan täsmällisimmin?",
        [
            "Kertoja vahvistaa vaatimuksen kohtuuttomaksi ennen kuin kuvaa Leenan myöhemmän toiminnan.",
            "Kohtuuttomuus välittyy Leenan kokemuksena, jonka lopullista oikeutusta katkelma ei ratkaise.",
            "Kirjeen lähettäjä pitää vaatimusta kohtuuttomana ja odottaa Leenan torjuvan sen illalla.",
            "Leena on jo muuttanut kantaansa vaatimukseen, ja kysymys kuvaa hänen aiempaa virhepäätelmäänsä.",
        ],
        "Kohtuuttomuus välittyy Leenan kokemuksena, jonka lopullista oikeutusta katkelma ei ratkaise.",
        "fi-free-indirect-viewpoint-c2",
    ),
    AssessmentQuestion(
        "fi-g-c2-005",
        "grammar",
        "C2",
        "Jälkiarvioinnissa sanotaan: «Olisimme voineet kiertää toista kautta, jos olisimme "
        "tienneet sillan sulkemisesta. Kiertotien ruuhkista ei kuitenkaan ollut tietoa.» "
        "Mitä arvio oikeuttaa päättelemään?",
        [
            "Ennakkotieto olisi avannut vaihtoehdon, mutta sen ajallisesta hyödystä ei ole varmuutta.",
            "Ennakkotieto olisi varmistanut saapumisen ajoissa, vaikka reitti olisi ollut pidempi.",
            "Kiertotien ruuhkat estivät reitin valinnan, vaikka sillan sulkeminen oli tiedossa.",
            "Reitti valittiin tietoisesti lyhyemmäksi, koska sillan avaamista pidettiin todennäköisenä.",
        ],
        "Ennakkotieto olisi avannut vaihtoehdon, mutta sen ajallisesta hyödystä ei ole varmuutta.",
        "fi-retrospective-conditions-c2",
    ),
    AssessmentQuestion(
        "fi-g-c2-006",
        "grammar",
        "C2",
        "Talouskeskustelussa sanotaan: «Se ei ole säästöä vaan laskun siirtämistä ensi vuoteen.» "
        "Mihin kielto tässä kohdistuu?",
        [
            "Siihen, että tämän vuoden maksettava summa olisi pienentynyt laskua siirtämällä.",
            "Siihen, että lasku olisi edelleen maksettava jonkin myöhemmän vuoden aikana.",
            "Siihen, että maksun siirtämisestä olisi voitu päättää tämän vuoden talouskeskustelussa.",
            "Siihen, että menon ajankohdan muutos olisi osuvaa esittää kokonaismenon vähenemisenä.",
        ],
        "Siihen, että menon ajankohdan muutos olisi osuvaa esittää kokonaismenon vähenemisenä.",
        "fi-metalinguistic-negation-c2",
    ),
    AssessmentQuestion(
        "fi-g-c2-007",
        "grammar",
        "C2",
        "Olet lukenut vain uutisen, jossa sanotaan: «Viraston mukaan tutkijat pitävät "
        "mahdollisena, että muutos vähentää ruuhkia.» Mikä kirjaus säilyttää tiedon alkuperän?",
        [
            "Tutkijoiden vahvistaman tiedon mukaan virasto vähentää ruuhkia muutoksella.",
            "Uutinen välittää viraston tiedon tutkijoiden arviosta, jossa hyöty on mahdollinen.",
            "Viraston uutisessa vahvistetaan tutkijoiden havainneen ruuhkien jo vähentyneen.",
            "Uutinen kuvaa viraston tavoitetta, jonka toteutumista tutkijat pitävät varmana.",
        ],
        "Uutinen välittää viraston tiedon tutkijoiden arviosta, jossa hyöty on mahdollinen.",
        "fi-source-chains-c2",
    ),
    AssessmentQuestion(
        "fi-g-c2-008",
        "grammar",
        "C2",
        "Tarjouksessa työ kestää «arviolta neljä päivää». Asiakas kirjoittaa vahvistukseen "
        "«enintään neljä päivää». Mikä vastaus käsittelee muutoksen täsmällisesti?",
        [
            "Sanamuoto säilyttää arvion, mutta työpäivien ja kalenteripäivien ero pitää vielä sopia.",
            "Sanamuoto madaltaa aiempaa vähimmäiskestoa, joten meidän on sovittava uusi aloitus.",
            "Sanamuoto muuttaa kestoarvion ylärajaksi, jota emme ole vielä luvanneet.",
            "Sanamuoto muuttaa tarkan toimituspäivän likimääräiseksi, joten tarvitsemme täsmennyksen.",
        ],
        "Sanamuoto muuttaa kestoarvion ylärajaksi, jota emme ole vielä luvanneet.",
        "fi-quantified-precision-c2",
    ),
    AssessmentQuestion(
        "fi-v-c2-001",
        "vocabulary",
        "C2",
        "Kaksi kyselyä raportoi odotusajan lyhentyneen. Toisessa aika mitataan yhteydenotosta "
        "tapaamiseen, toisessa hakemuksen hyväksymisestä tapaamiseen. Mikä huomautus osuu "
        "olennaisimpaan tulosten vertailussa?",
        [
            "Tulosten edustavuus on varmistettu, koska molemmissa odotusaika lyheni.",
            "Tulosten virhemarginaali on sama, koska molemmat mittaavat aikaa tapaamiseen.",
            "Tulosten syy-yhteys on epäselvä, koska toinen kysely tehtiin hakijoille.",
            "Tulosten vertailukelpoisuus on rajallinen, koska mittauksen alkupisteet eroavat.",
        ],
        "Tulosten vertailukelpoisuus on rajallinen, koska mittauksen alkupisteet eroavat.",
    ),
    AssessmentQuestion(
        "fi-v-c2-002",
        "vocabulary",
        "C2",
        "Ehdotat palvelulle kuukauden kokeilutaukoa arviointia varten. Vastapuoli vastaa: "
        "«Et siis halua, että tätä palvelua on enää olemassa.» Miten kuvaat hänen vastaustaan "
        "täsmällisimmin?",
        [
            "Se tuo esiin ehdotukseen sisältyvän rajausehdon ja pyytää tarkentamaan sen kestoa.",
            "Se rakentaa olkiukon muuttamalla määräaikaisen arviointitauon lopulliseksi lopettamiseksi.",
            "Se osoittaa arvoristiriidan hyväksymällä kokeilun mutta kiistämällä sen kustannukset.",
            "Se tekee myönnytyksen hyväksymällä tauon ja siirtää keskustelun palvelun tulevaisuuteen.",
        ],
        "Se rakentaa olkiukon muuttamalla määräaikaisen arviointitauon lopulliseksi lopettamiseksi.",
    ),
    AssessmentQuestion(
        "fi-v-c2-003",
        "vocabulary",
        "C2",
        "Puhuja tervehtii kavereitaan: «Kunnioitettu raati, pyydän lausuntoanne tästä "
        "pahasti kärähtäneestä paahtoleivästä.» Mikä kuvaa tyylin vaikutusta tässä?",
        [
            "Mahtipontinen muoto nostaa arkisen vahingon leikillisesti juhlavan arvioinnin kohteeksi.",
            "Lakoninen muoto häivyttää arvioinnin ja jättää kuulijoille vain vähäeleisen tosiasian.",
            "Alatyylinen muoto siirtää huomion vahingosta kuulijoihin kohdistuvaan loukkaukseen.",
            "Pidättyväinen muoto peittää puhujan suhteen tapahtumaan ja korostaa virallista vastuuta.",
        ],
        "Mahtipontinen muoto nostaa arkisen vahingon leikillisesti juhlavan arvioinnin kohteeksi.",
    ),
    AssessmentQuestion(
        "fi-v-c2-004",
        "vocabulary",
        "C2",
        "Sovittelussa molemmat hyväksyvät «joustavan työajan». Toinen tarkoittaa työntekijän "
        "oikeutta valita aloitusaika, toinen työnantajan oikeutta muuttaa vuoroja. "
        "Mitä yhteisen kirjauksen vaaraa tämä havainnollistaa?",
        [
            "Puolueettomuutta: kummankaan tulkinnalle ei vielä ole annettu etusijaa.",
            "Harkintavaltaa: kumpikin on jo saanut saman oikeuden päättää työajoista.",
            "Näennäisyhteisymmärrystä: sama ilmaus peittää erilaiset käsitykset päätösvallasta.",
            "Vastavuoroisuutta: molemmat ovat jo vaihtaneet oman oikeutensa yhteiseen etuun.",
        ],
        "Näennäisyhteisymmärrystä: sama ilmaus peittää erilaiset käsitykset päätösvallasta.",
    ),
    AssessmentQuestion(
        "fi-r-c2-001",
        "reading",
        "C2",
        "Kolumnisti kirjoittaa: «Palvelu on nyt kaikkien ulottuvilla, tiedote vakuuttaa. "
        "Kaikkien niiden siis, jotka ehtivät paikalle ennen neljää ja pääsevät kolme kerrosta "
        "portaita. Muut saavat iloita tilastollisesta edistyksestä.» Mihin tekstin ironia kohdistuu?",
        [
            "Käyttäjien tapaan vaatia palvelua myös sellaisina aikoina, jolloin sille ei ole kysyntää.",
            "Tilastojen kykyyn kuvata palvelun kustannuksia ilman tarkkaa tietoa rakennuksen iästä.",
            "Kattavuutta korostavan tiedotuksen ja käytännössä rajoitetun pääsyn väliseen ristiriitaan.",
            "Rakennuksen käyttäjien haluttomuuteen kokeilla palvelua ennen sen lopullista arviointia.",
        ],
        "Kattavuutta korostavan tiedotuksen ja käytännössä rajoitetun pääsyn väliseen ristiriitaan.",
    ),
    AssessmentQuestion(
        "fi-r-c2-002",
        "reading",
        "C2",
        "Muistelija kertoo odottaneensa anteeksipyyntöä. «Hän työnsi kupin eteeni ja kysyi, "
        "laitetaanko lisää kahvia. Vastasin, ettei tarvitse. Sitten puhuimme säästä. "
        "Vasta vuosia myöhemmin aloin ajatella, että ehkä siinä oli hänen tapansa lähestyä.» "
        "Mikä tulkinta kunnioittaa kertomuksen tiedollisia rajoja?",
        [
            "Muistelija tarjoaa myöhemmän mahdollisen tulkinnan eleelle vahvistamatta toisen aikomusta.",
            "Muistelija osoittaa toisen pyytäneen anteeksi tavalla, jonka hän jo tilanteessa ymmärsi.",
            "Muistelija peruu alkuperäisen muistonsa ja kertoo kahvitarjoilun olleen vasta myöhempi tapahtuma.",
            "Muistelija pitää kahvitarjoilua tietoisena keinona välttää sovintoa myös myöhemmässä arviossaan.",
        ],
        "Muistelija tarjoaa myöhemmän mahdollisen tulkinnan eleelle vahvistamatta toisen aikomusta.",
    ),
    AssessmentQuestion(
        "fi-r-c2-003",
        "reading",
        "C2",
        "Kokeiluraportti kertoo ruuhkien vähentyneen aamuisin. Yrittäjien lausunto kuvaa "
        "iltapäivän toimitusten vaikeutuneen. Kokouksessa raporttia käytetään perusteena "
        "lausunnon sivuuttamiselle. Mikä sovittelijan huomautus on aineistojen perusteella tarkin?",
        [
            "Yrittäjien kokemus kumoaa raportin, koska käytännön toimitukset ovat liikennemäärää tärkeämpiä.",
            "Havainnot voivat olla yhtä aikaa tosia, koska ne koskevat eri aikoja ja vaikutuksia.",
            "Raportti kumoaa lausunnon, koska aamuinen ruuhkien väheneminen parantaa myös iltapäivää.",
            "Havainnot osoittavat kokeilun kokonaisvaikutuksen neutraaliksi, koska yksi hyöty vastaa yhtä haittaa.",
        ],
        "Havainnot voivat olla yhtä aikaa tosia, koska ne koskevat eri aikoja ja vaikutuksia.",
    ),
    AssessmentQuestion(
        "fi-r-c2-004",
        "reading",
        "C2",
        "Neuvottelumuistiossa työntekijät hyväksyvät kokeilun sillä ehdolla, että työkuormaa "
        "seurataan viikoittain ja kokeilu voidaan keskeyttää yhteisesti sovitun rajan ylittyessä. "
        "Johto hyväksyy seurannan, mutta keskeytysrajasta keskustellaan ensi viikolla. "
        "Mikä otsikko sopii yhteiseen tiedotteeseen tässä vaiheessa?",
        [
            "Kokeilu hyväksytty: viikoittainen seuranta turvaa yhteisesti sovitun keskeytysrajan",
            "Kokeilusta luovuttu: työkuorman keskeytysraja esti yhteisen etenemisen",
            "Keskeytysraja ratkaistu: seurannan yksityiskohdista neuvotellaan ensi viikolla",
            "Kokeilun ehdot tarkentuvat: seurannasta sovittu, keskeytysraja vielä avoinna",
        ],
        "Kokeilun ehdot tarkentuvat: seurannasta sovittu, keskeytysraja vielä avoinna",
    ),
]
