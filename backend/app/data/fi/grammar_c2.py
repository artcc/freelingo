"""Finnish C2 discourse grammar with explicit limits on interpretation."""

from app.data._types import GrammarExample, GrammarTopic

C2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "fi-nested-modality-c2",
        "Epävarmuus väitteen eri tasoilla",
        "C2",
        "Modaliteetti",
        "Tunnista, koskeeko varaus tapahtumaa, sen syytä vai lähteen arviota.",
        "Voi olla, että keskeytys johtui viasta jättää syyselityksen avoimeksi. "
        "Vika saattoi estää käynnistyksen esittää mahdollisen vaikutussuhteen. "
        "On varmaa, että keskeytys saattoi johtua viasta esittää vikasyyn mahdollisuuden "
        "varmana mutta ei vahvista vikaa todelliseksi syyksi. Sisäkkäiset ilmaukset on "
        "purettava väite kerrallaan.",
        rules=[
            "Älä anna ulomman varmuusilmauksen vahvistaa kaikkea sisäkkäistä sisältöä tosiasiaksi.",
            "Tee tarvittaessa kaksi virkettä, jotta varauksen kohde näkyy.",
        ],
        examples=[
            GrammarExample("Tutkija pitää mahdollisena, että mittari näytti liian vähän."),
            GrammarExample("Varmistimme vain, ettei laitevikaa voida vielä sulkea pois."),
        ],
        related=["fi-inference-c1"],
    ),
    GrammarTopic(
        "fi-potential-register-c2",
        "Lienee tehnyt, ei liene ja lienee tehtävä",
        "C2",
        "Arvion rekisteri",
        "Tulkitse potentiaalia myös menneen ja velvoitteen yhteydessä.",
        "Lienee tehnyt arvioi aiempaa toimintaa; ei liene tehnyt esittää tekemättä "
        "jäämisen todennäköisenä. Asiasta lienee päätettävä pian arvioi velvoitteen tai tarpeen "
        "todennäköiseksi, ei kerro päätöksen syntyneen. Potentiaali on monissa "
        "yleiskielisissä teksteissä luonteva, mutta sen yleisyys vaihtelee ilmauksittain ja "
        "puhetavoittain. Tavoitteena on täsmällinen tulkinta, ei jokaisen verbin harvinainen muoto.",
        rules=[
            "Valitse arkisessa reformulaatiossa esimerkiksi taitaa tai todennäköisesti.",
            "Erota päättänyt, päätetty ja päätettävä myös epävarmassa arviossa.",
        ],
        examples=[
            GrammarExample("Viesti lienee päätynyt vanhaan osoitteeseen."),
            GrammarExample("Lisäselvitystä lienee pyydettävä ennen äänestystä."),
        ],
        related=["fi-nested-modality-c2"],
    ),
    GrammarTopic(
        "fi-retrospective-conditions-c2",
        "Olisi voinut ja olisi pitänyt",
        "C2",
        "Menneen arviointi",
        "Erota käyttämättä jäänyt mahdollisuus jälkikäteisestä vaatimuksesta.",
        "Olisi voinut kysyä kuvaa usein toteutumatonta mahdollisuutta. Olisi pitänyt kysyä "
        "arvioi kysymisen tarpeelliseksi tai velvoittavaksi. Muodot voivat myös liittyä "
        "menneeseen epävarmuuteen tai kuviteltuun tapahtumaketjuun; tulkinta varmistetaan "
        "kontekstista. Jälkiviisas arvio ei osoita, että toimijalla oli silloin tarvittava tieto.",
        rules=[
            "Nimeä, mitä päätöksentekijä tiesi tapahtumahetkellä.",
            "Älä muuta mahdollista vaihtoehtoa varmaksi onnistumiseksi.",
        ],
        examples=[
            GrammarExample(
                "Olisimme voineet hakea lisäaikaa, mutta emme tienneet mahdollisuudesta."
            ),
            GrammarExample(
                "Olisi pitänyt tarkistaa osoite; siitä ei seuraa, että lähetys olisi ehtinyt."
            ),
        ],
    ),
    GrammarTopic(
        "fi-presuppositions-c2",
        "Yhä, taas ja kysymykseen piilotettu oletus",
        "C2",
        "Taustaoletukset",
        "Vastaa kysymyksen sisältöön hyväksymättä perusteetonta lähtökohtaa.",
        "Miksi viivyttelette taas? esittää sekä nykyisen viivyttelyn että sen toistumisen "
        "kysymyksen taustana. Pelkkä syyn antaminen voi jättää molemmat oletukset voimaan "
        "keskustelussa. Yhä puolestaan esittää tilanteen jatkuvana. Oletuksen voi nostaa "
        "arvioitavaksi ennen varsinaiseen kysymykseen vastaamista.",
        rules=[
            "Erota kysytty asia siitä, mitä kysymys käsittelee valmiiksi annettuna.",
            "Kiistä vain perusteeton oletus ja vastaa jäljelle jäävään asialliseen kysymykseen.",
        ],
        examples=[
            GrammarExample(
                "Emme ole ylittäneet määräaikaa. Jos kysyt etenemisestä, luonnos on valmis."
            ),
            GrammarExample(
                "Yhäkö vastustat ehdotusta? — En vastustanut sitä, vaan pyysin laskelman."
            ),
        ],
    ),
    GrammarTopic(
        "fi-scalar-alternatives-c2",
        "Vaikka, edes ja saati",
        "C2",
        "Vaihtoehdot ja asteikot",
        "Tunnista ehdotus, vähimmäisodotus ja vahvempi vaihtoehto.",
        "Tavataan vaikka torstaina tarjoaa torstain yhtenä mahdollisuutena. Tavataan edes "
        "torstaina voi esittää torstain vähimmäisratkaisuna tilanteessa, jossa parempi ei "
        "onnistu. Ei ehdi lukea viestiä, saati vastata siihen asettaa vastaamisen tässä "
        "vaativammaksi vaihtoehdoksi. Asteikko syntyy asiayhteydestä, ei asioiden pysyvästä arvosta.",
        rules=[
            "Vaikka ei aina aloita myönnytyslausesuhdetta.",
            "Edes voi kielteisessä lauseessa osoittaa, ettei vähäinenkään odotus toteudu.",
        ],
        examples=[
            GrammarExample(
                "Voimme kokeilla vaikka kahta iltaa viikossa; muutkin ehdotukset käyvät."
            ),
            GrammarExample("Emme saaneet edes vastaanottokuittausta, saati perusteltua vastausta."),
        ],
    ),
    GrammarTopic(
        "fi-metalinguistic-negation-c2",
        "En sanoisi sitä säästöksi vaan siirroksi",
        "C2",
        "Sanavalinnan oikaisu",
        "Erota tapahtuman kieltäminen sen kuvauksen vastustamisesta.",
        "Se ei ollut keskustelu vaan kuulustelu voi hyväksyä puhetilanteen tapahtuneen "
        "mutta torjua neutraalin nimityksen. Tällainen kielto kohdistuu kuvaukseen tai "
        "sen vaikutelmaan, ei välttämättä ulkoiseen tapahtumaan. Oikaisussa kannattaa "
        "selittää, mikä piirre tekee ensimmäisestä sanasta harhaanjohtavan.",
        rules=[
            "Säilytä yhteiset tosiasiat, vaikka kiistäisit niiden nimityksen.",
            "Vahvempi sana tarvitsee perustelun, jos keskustelua halutaan jatkaa rakentavasti.",
        ],
        examples=[
            GrammarExample(
                "Meno ei poistunut. Kyse ei siis ole säästöstä vaan maksun lykkäämisestä."
            ),
            GrammarExample(
                "En kutsuisi sitä vapaaehtoiseksi, jos kieltäytymisestä seurasi rangaistus."
            ),
        ],
    ),
    GrammarTopic(
        "fi-compressed-agency-c2",
        "Kuka sanoo kenen tehneen?",
        "C2",
        "Sisäkkäiset rakenteet",
        "Pura referatiivirakenne muuttamatta tekijää tai tiedon lähdettä.",
        "Johtaja kertoi tarkastajan hyväksyneen urakoitsijan tekemät korjaukset sisältää "
        "kolme toimijaa. Johtaja välittää tiedon, tarkastaja hyväksyy ja urakoitsija tekee. "
        "Rakenteen tiiviys ei tee hyväksymisestä kertojan varmentamaa tosiasiaa. "
        "Omistusliitteellinen kertoi hyväksyneensä puolestaan kytkee hyväksyjän tavallisesti "
        "kertovan lauseen subjektiin.",
        rules=[
            "Pura rakenne tarvittaessa että-lauseeksi ennen tiivistämistä.",
            "Säilytä nimeämättä jätetty toimija nimeämättä myös selkokielisemmässä esityksessä.",
        ],
        examples=[
            GrammarExample(
                "Liisa sanoi tarkastajan hyväksyneen muutoksen; hyväksyjäksi nimetään siis tarkastaja."
            ),
            GrammarExample("Liisa sanoi hyväksyneensä muutoksen vasta lisäselvityksen jälkeen."),
        ],
        related=["fi-participle-agents-c1", "fi-reported-commitments-c1"],
    ),
    GrammarTopic(
        "fi-dense-noun-phrases-c2",
        "Rajaukset pitkissä lausekkeissa",
        "C2",
        "Sopimusten lukeminen",
        "Erota päätöksen kohde sen ehdoista ja valmistelusta.",
        "Esitys määräaikaisten käyttörajoitusten jatkamisen edellytysten selvittämisestä "
        "ehdottaa selvitystä. Se ei vielä ehdota suoraan jatkamista eikä kerro, että jatkosta "
        "olisi päätetty. Pitkää määriteketjua avattaessa ydinsana etsitään ensin, minkä jälkeen "
        "toimintojen väliset suhteet ja rajaukset ilmaistaan erillisinä lauseina.",
        rules=[
            "Pidä määräaikaisuus, kohderyhmä ja poikkeukset kiinni oikeassa toiminnossa.",
            "Älä vahvista selvitystehtävää toimeenpanovaltuudeksi.",
        ],
        examples=[
            GrammarExample("Ehdotamme, että selvitetään, millä ehdoilla rajoituksia voisi jatkaa."),
            GrammarExample("Tilapäisen käytön lupa ei ole lupa muuttaa tilaa pysyvästi."),
        ],
        related=["fi-nominalisation-c1"],
    ),
    GrammarTopic(
        "fi-free-indirect-viewpoint-c2",
        "Vapaa epäsuora esitys ja näkökulman liukuminen",
        "C2",
        "Kertomuksen äänet",
        "Tunnista henkilön ajatus ilman johtolausetta.",
        "Kertojan mennyt aikamuoto ja kolmas persoona voivat yhdistyä henkilön omaan "
        "arvioon: Aino vilkaisi kelloa. Pitikö hänen taas odottaa? Jälkimmäinen kysymys "
        "voi välittää Ainon ajatuksen ilman ilmausta Aino ajatteli. Tulkinta perustuu "
        "ympäröivään tekstiin; jokainen kysymys kertomuksessa ei ole henkilön sisäistä puhetta.",
        rules=[
            "Perustele näkökulma sanavalinnoilla ja lähikontekstilla.",
            "Älä esitä henkilön arviota kertojan vahvistamana totuutena.",
        ],
        examples=[
            GrammarExample(
                "Olli avasi kirjeen. Taas uusi selvityspyyntö! Eikö tämä koskaan loppuisi?"
            ),
            GrammarExample(
                "Ollista pyyntö tuntui kohtuuttomalta; teksti ei vielä osoita sen olleen sitä."
            ),
        ],
        related=["fi-narrative-time-c1"],
    ),
    GrammarTopic(
        "fi-narrative-ellipsis-c2",
        "Pois jätetty yhteys ja lukijan päätelmä",
        "C2",
        "Kerronnan rytmi",
        "Rakenna ja tulkitse aukkoja sekoittamatta vihjettä todisteeseen.",
        "Hän luki viestin. Seuraavana aamuna työpöytä oli tyhjä antaa lukijan yhdistää "
        "tapahtumat, mutta ei nimeä poistumisen syytä. Ellipsi voi myös jättää toistuvan "
        "lauseenjäsenen pois: minä otin kahvin, hän teen. Kerronnallinen aukko ei aina ole "
        "kieliopillinen ellipsi. Molemmissa vastaanottajalle jätetään pääteltävää.",
        rules=[
            "Erota tekstin väite siitä rakentamastasi mahdollisesta tapahtumaketjusta.",
            "Lisää selitys, jos käytännön ohjeessa aukko voisi johtaa väärään toimintaan.",
        ],
        examples=[
            GrammarExample("Minä jäin laiturille, hän junaan. Yhteinen matkamme päättyi siihen."),
            GrammarExample(
                "Puhelin soi. Kertoja lopetti pakkaamisen. Puhelun sisältö jäi kertomatta."
            ),
        ],
    ),
    GrammarTopic(
        "fi-dialogical-concession-c2",
        "Kyllä minä ymmärrän, mutta",
        "C2",
        "Vastaväitteen käsittely",
        "Tunnista myönnytyksen ja varsinaisen kannan välinen painotus.",
        "Kyllä hyväksyy tai vahvistaa jotakin, mutta kyllä … mutta -rakenteessa jälkiosa "
        "usein rajoittaa myönnytyksen merkitystä johtopäätökselle. Kyllä minä ymmärrän "
        "huolesi ei yksin merkitse ehdotuksen hyväksymistä. Toisto, painotus ja jatko "
        "voivat tehdä myönnytyksestä aidon, varautuneen tai torjuvan.",
        rules=[
            "Sano konkreettisesti, minkä perustelun hyväksyt.",
            "Älä päättele koko kantaa pelkästä kyllä-sanasta.",
        ],
        examples=[
            GrammarExample("Kyllä reitti lyhenisi, mutta esteetön sisäänkäynti jäisi liian kauas."),
            GrammarExample(
                "Ymmärrän kiireen. Ehdotan silti päivän lisäaikaa, jotta kaikki ehtivät vastata."
            ),
        ],
    ),
    GrammarTopic(
        "fi-echo-and-distance-c2",
        "Muka, niin sanottu ja toisen sanojen kaiuttaminen",
        "C2",
        "Moniääninen keskustelu",
        "Erota lainaus epäilevästä tai arvottavasta toistosta.",
        "Ai tämäkö on se joustava ratkaisu? voi kaiuttaa aiempaa lupausta ja haastaa sen "
        "sopivuuden nykytilanteeseen. Muka merkitsee usein etäisyyttä väitteeseen. "
        "Niin sanottu voi esitellä termin tai vihjata, ettei nimitys ole osuva; "
        "se ei aina ole pilkallinen. Kirjoituksessa lainausmerkitkin voivat joko lainata "
        "tai etäännyttää, joten niiden tehtävä kannattaa tehdä selväksi.",
        rules=[
            "Nimeä epäilyn kohde, jos kaiuttaminen muuten kuulostaa henkilökohtaiselta hyökkäykseltä.",
            "Erota puhujan toistama väite hänen omasta kannastaan.",
        ],
        examples=[
            GrammarExample("Tämäkö muka säästää aikaa, kun jokainen tieto pitää syöttää kahdesti?"),
            GrammarExample(
                "Käytän tässä termiä joustava työaika sen sopimuksessa määritellyssä merkityksessä."
            ),
        ],
        related=["fi-source-marking-c1", "fi-metalinguistic-negation-c2"],
    ),
    GrammarTopic(
        "fi-register-voices-c2",
        "Tyylinvaihdos ja puhujan rooli",
        "C2",
        "Rekisterin hallinta",
        "Mukauta ääni yleisölle muuttamatta viestin sisältöä.",
        "Juhlava ilmoitus arkisesta asiasta voi olla leikillinen: täten julistan kahvitauon "
        "alkaneeksi. Sama muoto virallisessa päätöksessä rakentaa institutionaalista roolia. "
        "Puheen alueelliset ja sosiaaliset piirteet eivät itsessään osoita osaamattomuutta "
        "tai tuttavallisuuden lupaa. Tyylin sopivuus arvioidaan suhteessa yleisöön ja tarkoitukseen.",
        rules=[
            "Muuta sävyä mutta säilytä vastuut, ehdot ja aikarajat.",
            "Älä rakenna huumoria oletukselle, että tietty puhetapa olisi muita huonompi.",
        ],
        examples=[
            GrammarExample("Arvoisa seurue, päivän tärkein päätös: kahvia vai teetä?"),
            GrammarExample(
                "Virallisessa kutsussa sama kysymys on: ilmoittakaa, haluatteko kahvia vai teetä."
            ),
        ],
    ),
    GrammarTopic(
        "fi-irony-boundaries-c2",
        "Vähättely, itseironia ja tulkinnan varmistaminen",
        "C2",
        "Huumorin pragmatiikka",
        "Tunnista epäsuora arvio ja vastaa sen vaikutukseen.",
        "Ei mennyt aivan putkeen voi vähätellä suurta epäonnistumista. Ironinen tulkinta "
        "syntyy sanamuodon ja tilanteen suhteesta, ei kiinteästä sanalistasta. "
        "Itseironia voi kutsua yhteiseen nauruun, mutta se voi myös peittää huolta. "
        "Hyvä vastaus huomioi sen, miten puhe vaikuttaa, eikä vetoa vain puhujan aikomukseen.",
        rules=[
            "Kysy tarvittaessa, haluaako toinen myötätuntoa, apua vai leikillisen vastauksen.",
            "Selitä oma huumorisi ja ota vastuu sanavalinnasta, jos se loukkasi.",
        ],
        examples=[
            GrammarExample("Koko esitys katosi koneelta. Pieni tekninen haaste, sanoisin."),
            GrammarExample(
                "Tarkoitukseni oli vitsailla itsestäni, mutta ymmärrän, miksi se kuulosti sinusta toiselta."
            ),
        ],
        related=["fi-pa-reactions-c1", "fi-echo-and-distance-c2"],
    ),
    GrammarTopic(
        "fi-source-chains-c2",
        "Lähdeketju ja eriävät tulkinnat",
        "C2",
        "Synteesi",
        "Näytä, kuka tietää, kuka kertoo ja kuka päättelee.",
        "Lehden mukaan virasto arvioi, että kustannukset saattavat nousta sisältää "
        "julkaisulähteen, arvion tekijän ja mahdollisuuden. Tiivistelmä kustannukset nousevat "
        "poistaa kaikki kolme rajausta. Lähteiden yhdistäminen ei tarkoita ristiriitojen "
        "häivyttämistä: eri laskentatavat tai ajankohdat voivat selittää eron.",
        rules=[
            "Säilytä olennainen lähdeketju silloin, kun et ole tarkistanut alkuperäistä aineistoa.",
            "Erota lähteiden yhteinen havainto omasta sovittavasta tulkinnastasi.",
        ],
        examples=[
            GrammarExample(
                "Tiedotteen mukaan tutkija pitää vaikutusta mahdollisena, ei vielä osoitettuna."
            ),
            GrammarExample(
                "Molemmat raportit kuvaavat kasvua, mutta vain toinen käsittelee talvikautta."
            ),
        ],
        related=["fi-source-marking-c1", "fi-nested-modality-c2"],
    ),
    GrammarTopic(
        "fi-quantified-precision-c2",
        "Vähintään, enintään, lähes ja arviolta",
        "C2",
        "Rajauksen tarkkuus",
        "Säilytä määrän raja, vertailujoukko ja arvion asema.",
        "Vähintään kymmenen antaa alarajan ja enintään kymmenen ylärajan. Lähes kymmenen "
        "esittää määrän kymmentä pienempänä mutta lähellä sitä; arviolta kymmenen ilmaisee "
        "epätarkkaa arviota, ei kumpaakaan rajaa. Joka kolmas vastaaja koskee vastanneita, "
        "ei ilman lisätietoa kaikkia kutsuttuja. Käytännön sopimuksessa rajan ja arvion ero on olennainen.",
        rules=[
            "Nimeä prosenttiluvun tai osuuden vertailujoukko.",
            "Älä muuta alustavaa arviota enimmäislupaukseksi.",
        ],
        examples=[
            GrammarExample(
                "Työ kestää arviolta kolme päivää; kolmea päivää ei luvattu enimmäisajaksi."
            ),
            GrammarExample(
                "Vähintään puolet vastanneista kannatti ehdotusta, mutta kaikki eivät vastanneet."
            ),
        ],
    ),
]
