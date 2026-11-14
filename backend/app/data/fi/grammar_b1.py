"""Finnish B1 grammar for independent interaction."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "fi-object-result-b1",
        "Tekeminen vai valmis tulos?",
        "B1",
        "Objekti",
        "Objektin sija auttaa erottamaan prosessin rajatusta kokonaisuudesta.",
        "Partitiivi sopii keskeneräiseen tai rajaamattomaan tekemiseen: luin raporttia. "
        "Totaaliobjekti esittää kohteen kokonaisuutena ja tekemisen rajattuna: luin raportin. "
        "Myönteinenkään lause ei aina saa totaaliobjektia: odotan bussia kuvaa odottamista. "
        "Substantiivin monikollinen totaaliobjekti on nominatiivissa. Persoonapronomineilla on t-päätteinen "
        "akkusatiivi: näin hänet. Preesensissä rajattu toiminta voi viitata tulevaan.",
        structure="luen raporttia / luen raportin; luen raportit",
        rules=[
            "Tarkastele sekä verbin merkitystä että sitä, esitetäänkö toiminta rajattuna.",
            "Kesto ei yksin todista valmistumista: korjasin pyörää kaksi tuntia.",
        ],
        examples=[
            GrammarExample("Kirjoitin hakemusta illalla, mutta se jäi kesken."),
            GrammarExample("Kirjoitin hakemuksen valmiiksi ja lähetin sen."),
        ],
        related=["fi-object-negation-b1"],
    ),
    GrammarTopic(
        "fi-object-negation-b1",
        "Objekti kiellossa, käskyssä ja velvollisuudessa",
        "B1",
        "Objekti",
        "Lauseen rakenne vaikuttaa kokonaisenkin kohteen muotoon.",
        "Kielteisen lauseen objekti on tavallisesti partitiivissa: en ostanut lippua. "
        "Toisen persoonan myönteisen käskyn yksiköllinen substantiiviobjekti on kokonaisena "
        "nominatiivissa: osta lippu, ostakaa lippu. "
        "Sama koskee tavallista täytyy-rakennetta: minun täytyy ostaa lippu. "
        "Tavallisessa myönteisessä persoonalauseessa sanotaan ostan lipun. "
        "Persoonapronominin totaaliobjekti säilyttää t-muodon myös käskyssä: kutsu hänet.",
        rules=[
            "Kielto koskee myös pronominiobjektia: älä kutsu häntä.",
            "Totaaliobjektin muoto ja partitiivin valinta ovat eri kysymyksiä.",
        ],
        examples=[
            GrammarExample("En täyttänyt lomaketta, koska en ymmärtänyt kysymystä."),
            GrammarExample("Täytä lomake tänään. Minun täytyy lähettää se huomenna."),
        ],
        common_mistakes=[
            GrammarMistake(
                "En ostanut lipun.",
                "En ostanut lippua.",
                "Tässä tavallisessa kielteisessä lauseessa objekti on partitiivissa.",
            ),
        ],
        related=["fi-object-result-b1", "fi-necessity-b1"],
    ),
    GrammarTopic(
        "fi-pluperfect-b1",
        "Mitä oli tapahtunut aikaisemmin?",
        "B1",
        "Aikamuodot",
        "Pluskvamperfekti sijoittaa tapahtuman toisen menneen hetken edelle.",
        "Pluskvamperfekti muodostuu olla-verbin imperfektistä ja aktiivin "
        "NUT-partisiipista: olin lähtenyt, olimme lähteneet. Se antaa menneelle "
        "kertomukselle taustaa. Imperfekti vie usein tapahtumia eteenpäin. Kielteisessä "
        "muodossa käytetään en ollut tai emme olleet sekä pääverbin partisiippia. "
        "Partisiipin yksikkö tai monikko seuraa tekijää.",
        structure="olin tehnyt / olimme tehneet; en ollut tehnyt",
        rules=[
            "Tee mennyt vertailuhetki selväksi asiayhteydessä.",
            "Pluskvamperfekti ei yksin tarkoita, että tapahtumasta on hyvin pitkä aika.",
        ],
        examples=[
            GrammarExample("Kun saavuin asemalle, juna oli jo lähtenyt."),
            GrammarExample("Emme olleet varanneet pöytää, joten jouduimme odottamaan."),
        ],
        related=["fi-temporal-b1"],
    ),
    GrammarTopic(
        "fi-conditional-b1",
        "Kohtelias pyyntö ja kuviteltu tilanne",
        "B1",
        "Tapaluokat",
        "Konditionaalilla pyydät, ehdotat ja kuvittelet vaihtoehtoja.",
        "Konditionaalin tunnus on -isi-: tulisin, voisit, tekisimme. Kielteisessä "
        "muodossa persoonataivutus on kieltoverbissä: en tulisi, emme tulisi. "
        "Jos-lauseen konditionaali sopii kuviteltuun ehtoon. Todellista avointa "
        "ehtoa voi ilmaista indikatiivilla: jos bussi tulee, ehdin ajoissa. "
        "Konditionaali ei itsessään kerro menneestä ajasta.",
        structure="Jos minulla olisi aikaa, auttaisin. Voisitko auttaa?",
        rules=[
            "Kohteliaisuus riippuu myös tilanteesta ja äänensävystä.",
            "Älä lisää persoonapäätettä kielteisen pääverbin loppuun.",
        ],
        examples=[
            GrammarExample("Voisitteko siirtää ajan ensi viikolle?"),
            GrammarExample("Jos työpäivä päättyisi aiemmin, ehtisin kurssille."),
        ],
        common_mistakes=[
            GrammarMistake(
                "En tulisin tänään.", "En tulisi tänään.", "Persoona näkyy kieltoverbissä en."
            ),
        ],
        related=["fi-conditional-perfect-b1"],
    ),
    GrammarTopic(
        "fi-conditional-perfect-b1",
        "Mitä olisit tehnyt?",
        "B1",
        "Tapaluokat",
        "Konditionaalin perfekti auttaa puhumaan toteutumattomasta menneestä.",
        "Muodosta rakenne olla-verbin konditionaalista ja partisiipista: olisin tullut, "
        "olisimme tulleet. Menneeseen liittyvä ehto kertoo usein, miksi vaihtoehto ei "
        "toteutunut. Kielto on en olisi tullut. Rakenne voi myös kertoa aiemmasta "
        "toiveesta tai kohteliaasta tarkoituksesta; tulkinta ratkaistaan asiayhteydestä.",
        structure="Jos olisin tiennyt, olisin soittanut.",
        rules=[
            "Erota mennyt vaihtoehto nykyisestä: tulisin nyt / olisin tullut eilen.",
            "Säilytä partisiipin monikko: he olisivat auttaneet.",
        ],
        examples=[
            GrammarExample("Olisin ottanut sateenvarjon, jos olisin nähnyt ennusteen."),
            GrammarExample("Emme olisi ehtineet junaan ilman taksia."),
        ],
        related=["fi-conditional-b1", "fi-pluperfect-b1"],
    ),
    GrammarTopic(
        "fi-necessity-b1",
        "Täytyy, pitää ja ei tarvitse",
        "B1",
        "Velvollisuus",
        "Erotat velvollisuuden, tarpeettomuuden ja kiellon.",
        "Tavallisessa velvollisuusrakenteessa tekijä on genetiivissä ja verbi "
        "yksikön kolmannessa persoonassa: minun täytyy lähteä, meidän pitää ilmoittautua. "
        "Ei tarvitse poistaa velvollisuuden, mutta ei kiellä toimintaa. Ei saa "
        "ilmaisee kiellon. Rakenteessa minun ei tarvitse tehdä tekijä on genetiivissä. "
        "Tavallinen tarvita-verbi taipuu persoonassa: minä en tarvitse apua. "
        "Pitää-verbin muut merkitykset käyttävät muita rakenteita.",
        structure="minun täytyy tehdä; minun ei tarvitse tehdä; en saa tehdä",
        rules=[
            "Meidän täytyy, ei persoonan mukaan taivutettu täydymme.",
            "Substantiivin totaaliobjekti on tässä nominatiivissa: minun pitää ostaa lippu.",
        ],
        examples=[
            GrammarExample("Sinun ei tarvitse tulostaa lippua; puhelimen näyttö riittää."),
            GrammarExample("Täällä ei saa kuvata. Meidän täytyy jättää kamera laukkuun."),
        ],
        related=["fi-object-negation-b1"],
    ),
    GrammarTopic(
        "fi-passive-present-b1",
        "Mitä täällä tehdään?",
        "B1",
        "Passiivi",
        "Passiivi kertoo ihmisten toiminnasta nimeämättä tekijää.",
        "Suomen passiivi jättää tekijän avoimeksi: täällä korjataan pyöriä. "
        "Sillä voi kuvata tapaa, palvelua tai yhteistä ehdotusta. Se ei ole sama "
        "rakenne kuin esineen oma muuttuminen: ovi avataan, mutta ovi aukeaa. "
        "Kielto muodostetaan ei-sanalla ja lyhyemmällä muodolla: ei korjata, ei syödä. "
        "Substantiivin totaaliobjekti on nominatiivissa: ovi avataan. "
        "Persoonapronominilla säilyy akkusatiivi: minut kutsutaan.",
        structure="puhutaan / ei puhuta; tehdään / ei tehdä",
        rules=[
            "Passiivin taustalla on tavallisesti ihminen tai ihmisjoukko.",
            "Puhekielen me mennään vastaa yleiskielen muotoa me menemme.",
        ],
        examples=[
            GrammarExample("Kirjastossa lainataan myös liikuntavälineitä."),
            GrammarExample("Sovitaan uusi aika. Tätä asiaa ei ratkaista tänään."),
        ],
        related=["fi-passive-past-b1"],
    ),
    GrammarTopic(
        "fi-passive-past-b1",
        "Mitä tehtiin?",
        "B1",
        "Passiivi",
        "Passiivin imperfekti kuvaa mennyttä toimintaa ilman nimettyä tekijää.",
        "Myönteisen muodon lopussa on usein -ttiin tai -tiin: korjattiin, luettiin, "
        "syötiin. Kielteisessä muodossa käytetään ei ja passiivin TU-partisiippia: "
        "ei korjattu, ei luettu, ei syöty. Muoto ei kerro tekijöiden lukumäärää. "
        "Ajankohta tai kertomuksen kehys sitoo tapahtuman menneeseen.",
        structure="ovi avattiin / ovea ei avattu",
        rules=[
            "Kielteisessä imperfektissä ei käytetä muotoa ei avattiin.",
            "Myönteisen passiivin substantiiviobjekti on kokonaisena nominatiivissa.",
        ],
        examples=[
            GrammarExample("Piha siivottiin lauantaina."),
            GrammarExample("Hissiä ei korjattu eilen, koska varaosa puuttui."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Hissiä ei korjattiin.",
                "Hissiä ei korjattu.",
                "Kielteinen menneen ajan passiivi käyttää muotoa korjattu.",
            ),
        ],
        related=["fi-passive-present-b1", "fi-passive-perfect-b1"],
    ),
    GrammarTopic(
        "fi-passive-perfect-b1",
        "Mitä on jo tehty?",
        "B1",
        "Passiivi",
        "Passiivin perfekti yhdistää aiemman toiminnan nykyiseen tilanteeseen.",
        "Rakenne on on ja passiivin TU-partisiippi: on tarkistettu, on tehty. "
        "Kielto on ei ole tarkistettu. Apuverbi on yksikössä myös silloin, kun "
        "objekti on monikossa: ikkunat on pesty. Rakenne kertoo tekemisestä, "
        "kun taas ikkunat ovat puhtaat kuvaa suoraan niiden tilaa.",
        structure="on tehty / ei ole tehty",
        rules=[
            "Älä taivuta on-apuverbiä objektin lukumäärän mukaan.",
            "Jo ja vielä auttavat kertomaan työn etenemisestä.",
        ],
        examples=[
            GrammarExample("Vesikatkosta on ilmoitettu kaikille asukkaille."),
            GrammarExample("Avaimia ei ole vielä palautettu."),
        ],
        related=["fi-passive-past-b1"],
    ),
    GrammarTopic(
        "fi-verb-rection-b1",
        "Verbi ja sen vaatima sija",
        "B1",
        "Rektio",
        "Opit verbin yhdessä sen tavallisen täydennyksen kanssa.",
        "Verbi ohjaa usein sitä, missä sijassa täydennys on: osallistun koulutukseen, "
        "haen työpaikkaa, pidän työstä, luotan ohjaajaan. Sija ei aina ilmaise "
        "konkreettista paikkaa. Sama verbi voi eri merkityksessä saada erilaisen "
        "täydennyksen: pidän kirjasta mutta pidän kirjaa kädessäni.",
        rules=[
            "Opettele kokonaisuus: tottua johonkin, riippua jostakin, auttaa jotakuta.",
            "Kysy täydennyksen mukaan: mihin osallistut, mistä haaveilet?",
        ],
        examples=[
            GrammarExample("Osallistun koulutukseen ja tutustun uusiin työtovereihin."),
            GrammarExample("Aikataulu riippuu säästä, mutta luotan järjestäjiin."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Osallistun koulutuksesta.",
                "Osallistun koulutukseen.",
                "Osallistua-verbin täydennys on tässä illatiivissa.",
            ),
        ],
        related=["fi-ma-infinitive-b1", "fi-minen-b1"],
    ),
    GrammarTopic(
        "fi-ma-infinitive-b1",
        "Menen tekemään, olen tekemässä",
        "B1",
        "Infinitiivit",
        "MA-infinitiivi kertoo toimintaan siirtymisestä, siinä olemisesta ja siitä poistumisesta.",
        "Muodot tekemään, tekemässä ja tekemästä esiintyvät liikkeen ja sijainnin "
        "yhteydessä: menen uimaan, olen uimassa, tulen uimasta. Myös muut verbit "
        "vaativat näitä muotoja: opin käyttämään, pystyn auttamaan, lakkaan odottamasta. "
        "Valitse muoto hallitsevan verbin perusteella, älä vain toiminnan ajan mukaan.",
        structure="mennä tekemään; olla tekemässä; tulla tekemästä",
        rules=[
            "Kaikki verbit eivät saa MA-infinitiiviä: haluan oppia mutta opin tekemään.",
            "Pystyn-rakenteessa käytetään illatiivia: pystyn osallistumaan.",
        ],
        examples=[
            GrammarExample("Käyn harjoittelemassa suomea keskusteluryhmässä."),
            GrammarExample("En pysty tulemaan tänään, koska olen hoitamassa lasta."),
        ],
        related=["fi-verb-rection-b1"],
    ),
    GrammarTopic(
        "fi-minen-b1",
        "Tekemisestä puhuminen",
        "B1",
        "Verbistä substantiiviksi",
        "Minen-muoto nimeää toiminnan ja taipuu substantiivin tavoin.",
        "Lukeminen ja opiskeleminen voivat olla lauseen aiheita tai täydennyksiä. "
        "Vokaalivartalo on -mise-: lukemisen, lukemisesta. Yksikön partitiivissa "
        "käytetään konsonanttivartaloa -mis- ja päätettä -ta/-tä: lukemista. Verbistä "
        "tulee substantiivi, joten sen kohde voi olla genetiivissä: suomen opiskelu "
        "tai suomen opiskeleminen. Rakenne auttaa puhumaan tavoista ja tavoitteista "
        "yleisesti ilman tiettyä tekijää tai ajankohtaa.",
        structure="tekeminen → tekemisen → tekemistä → tekemisestä",
        rules=[
            "Hallitseva verbi määrää sijan: pidän lukemisesta.",
            "Toiminnan nimeäminen ei kerro, onko toiminta päättynyt.",
        ],
        examples=[
            GrammarExample("Uuden ammatin oppiminen vaatii aikaa."),
            GrammarExample("Harjoittelen hakemuksen kirjoittamista."),
        ],
        related=["fi-verb-rection-b1"],
    ),
    GrammarTopic(
        "fi-relative-b1",
        "Joka, jonka, jossa ja johon",
        "B1",
        "Relatiivilauseet",
        "Lisäät henkilöön tai asiaan tunnistamiseen tarvittavan tiedon.",
        "Joka-pronomini viittaa tavallisesti edeltävään substantiiviin. Sen sija "
        "ratkeaa relatiivilauseen tehtävästä: henkilö, jonka tapasin; koulutus, johon "
        "osallistun. Pronominin luku seuraa viittauskohdetta: ihmiset, jotka auttoivat. "
        "Koko edelliseen lauseeseen voidaan viitata mikä-pronominilla: aika vaihtui, "
        "mikä sopi minulle.",
        rules=[
            "Valitse sija relatiivilauseen, ei edeltävän lauseen verbin mukaan.",
            "Erota relatiivilause pilkuilla ympäröivästä lauseesta.",
        ],
        examples=[
            GrammarExample("Tässä on lomake, jonka täytin eilen."),
            GrammarExample("Etsin virkailijaa, jolle lähetin liitteet."),
        ],
        related=["fi-verb-rection-b1"],
    ),
    GrammarTopic(
        "fi-indirect-question-b1",
        "Tiedätkö, milloin palvelu avautuu?",
        "B1",
        "Kysymyslauseet",
        "Liität kysymyksen toiseen lauseeseen luontevasti.",
        "Epäsuora kysymys alkaa kysymyssanalla tai -ko/-kö-liitteisellä verbillä: "
        "kysyin, missä toimisto on; en tiedä, onko se auki. Kysymyssana säilyttää "
        "tehtävänsä ja sijansa. Koko virkkeen kysymysmerkki riippuu päälauseesta: "
        "Tiedätkö, milloin se avautuu? En tiedä, milloin se avautuu.",
        rules=[
            "Kyllä–ei-kysymys tarvitsee ko/kö-liitteen myös epäsuorana.",
            "Pidä kysymyksen sisältö erillään siitä, tiedetäänkö vastaus.",
        ],
        examples=[
            GrammarExample("Voisitko kertoa, tarvitseeko ajanvaraus vahvistaa?"),
            GrammarExample("Haluaisin tietää, kenelle hakemus lähetetään."),
        ],
        related=["fi-reported-speech-b1"],
    ),
    GrammarTopic(
        "fi-purpose-b1",
        "Jotta ja sitä varten",
        "B1",
        "Tarkoitus",
        "Selität tavoitteen erillään toiminnan syystä.",
        "Jotta-lause kertoo tarkoituksen: lähden ajoissa, jotta ehdin junaan. "
        "Koska-lause kertoo syyn: lähden, koska kokous alkaa pian. Jotta-lauseessa "
        "voi olla eri tekijä kuin päälauseessa. Konditionaali on mahdollinen, kun "
        "tavoite esitetään toivottuna tai ehdollisena; indikatiivi on myös tavallinen. "
        "Varten saa partitiivin: hakemusta varten.",
        rules=[
            "Tavoite ei takaa, että haluttu tulos toteutuu.",
            "Älä käsittele jotta-lauseen indikatiivia ja konditionaalia aina vastakohtina.",
        ],
        examples=[
            GrammarExample("Lähetän ohjeen, jotta voit valmistautua tapaamiseen."),
            GrammarExample("Tarvitsen todistuksen hakemusta varten."),
        ],
        related=["fi-conditional-b1"],
    ),
    GrammarTopic(
        "fi-temporal-b1",
        "Ennen kuin, sen jälkeen kun ja samalla kun",
        "B1",
        "Aikasuhteet",
        "Liität tapahtumat selkeään ajalliseen järjestykseen.",
        "Ennen kuin sijoittaa päälauseen tapahtuman toisen edelle. Sen jälkeen kun "
        "sijoittaa sen myöhemmäksi. Samalla kun kertoo samanaikaisuudesta. Kun voi "
        "viitata yksittäiseen tai toistuvaan tilanteeseen, eikä suomessa ole erillistä "
        "tulevaisuuden aikamuotoa: kun saan päätöksen, ilmoitan sinulle.",
        rules=[
            "Käytä pluskvamperfektiä, kun katsot menneestä hetkestä vielä taaksepäin.",
            "Kunnes ilmoittaa jatkumisen päätepisteen: odotan, kunnes saat vastauksen.",
        ],
        examples=[
            GrammarExample("Tarkistan osoitteen ennen kuin lähetän kirjeen."),
            GrammarExample("Kun olin lukenut viestin, soitin lähettäjälle."),
        ],
        related=["fi-pluperfect-b1"],
    ),
    GrammarTopic(
        "fi-concession-b1",
        "Vaikka, silti ja kuitenkin",
        "B1",
        "Vastakohta",
        "Ilmaiset, että odotettu seuraus ei toteudu.",
        "Vaikka esittelee seikan, joka ei estä päälauseen tapahtumaa: vaikka satoi, "
        "lähdimme ulos. Silti ja kuitenkin voivat yhdistää erillisiä lauseita "
        "samaan vastakohtaiseen ajatukseen. Vaikka voi myös aloittaa kuvitellun "
        "tilanteen: vaikka sataisi, lähtisimme. Tapaluokka, aikamuoto ja asiayhteys erottavat "
        "toteutuneen tilanteen kuvitellusta.",
        rules=[
            "Älä sekoita syytä ja vastakohtaa: koska ja vaikka muuttavat suhdetta.",
            "Silti ei vaadi samassa virkkeessä vaikka-sanaa.",
        ],
        examples=[
            GrammarExample("Vaikka ohje oli pitkä, luin sen kokonaan."),
            GrammarExample("Virkailija oli kiireinen. Hän auttoi minua silti."),
        ],
        related=["fi-conditional-b1"],
    ),
    GrammarTopic(
        "fi-reported-speech-b1",
        "Toisen viestin välittäminen",
        "B1",
        "Referointi",
        "Säilytät puhujan, ajankohdan ja viestin varmuuden.",
        "Että-lause välittää väitteen: Aino sanoi, että hän tulee huomenna. "
        "Pronominit ja ajanilmaukset sovitetaan kertojan näkökulmaan. Jos välität "
        "maanantain huomenna-sanan keskiviikkona, selkeä ilmaus voi olla tiistaina. "
        "Suomessa mennyt johtoverbi ei yksin pakota muuttamaan sivulauseen aikamuotoa. "
        "Kysymys välitetään kysyvällä sivulauseella, ei väittävällä että-lauseella.\n\n"
        "Myös omistajan on säilyttävä selvänä. Aino otti laukkunsa viittaa tavallisesti "
        "Ainon omaan laukkuun; Aino otti hänen laukkunsa viittaa toisen ihmisen laukkuun. "
        "Omistusliite tulee sijapäätteen jälkeen: laukussani, laukustasi. Kolmannessa "
        "persoonassa mahdollisia rinnakkaismuotoja ovat laukussaan ja harvinaisempi laukussansa. "
        "Jos omistaja jää epäselväksi, käytä nimeä: Aino otti Eeron laukun.",
        rules=[
            "Toista nimi, jos hän voisi viitata kahteen eri henkilöön.",
            "Älä muuta lupaa, toivetta tai arviota varmaksi lupaukseksi.",
        ],
        examples=[
            GrammarExample("Ohjaaja sanoi, että kurssi alkaa ensi viikolla."),
            GrammarExample("Mikko kysyi, voinko auttaa häntä muutossa."),
            GrammarExample(
                "Aino sanoi, että hän otti Eeron laukun.",
                note="Nimi kertoo yksiselitteisesti, että laukku kuuluu Eerolle eikä Ainolle.",
            ),
        ],
        related=["fi-indirect-question-b1", "fi-pluperfect-b1"],
    ),
    GrammarTopic(
        "fi-comparison-b1",
        "Vaihtoehtojen vertailu",
        "B1",
        "Vertailu",
        "Perustelet valinnan vertaamalla ominaisuuksia ja määriä.",
        "Komparatiivi vertailee: halvempi kuin, nopeampi kuin. Superlatiivi "
        "sijoittaa vaihtoehdon joukon kärkeen: halvin näistä. Muodot taipuvat "
        "pääsanan mukana: halvemmassa asunnossa, parhaaseen vaihtoehtoon. "
        "Yhtä ... kuin ilmaisee saman asteen. Määrän vertailussa käytetään "
        "enemmän ja vähemmän, ei aina adjektiivin komparatiivia.",
        rules=[
            "Epäsäännöllisiä muotoja ovat hyvä–parempi–paras ja pitkä–pidempi–pisin; myös pitempi on yleiskieltä.",
            "Tee vertailun peruste näkyväksi: halvempi vuokra mutta pidempi työmatka.",
        ],
        examples=[
            GrammarExample("Tämä reitti on yhtä nopea kuin toinen, mutta rauhallisempi."),
            GrammarExample("Valitsimme edullisemman asunnon läheltä asemaa."),
        ],
        related=["fi-essive-translative-b1"],
    ),
    GrammarTopic(
        "fi-essive-translative-b1",
        "Opettajana, valmiiksi ja ensi viikoksi",
        "B1",
        "Sijamuodot",
        "Erotat roolin tai tilan muutoksen tuloksesta.",
        "Essiivi -na/-nä kuvaa muun muassa roolia ja tilaa: työskentelen "
        "opettajana, olen sairaana. Translatiivi -ksi ilmaisee muutoksen tulosta: "
        "valmistuin opettajaksi, tulin iloiseksi. Translatiivi voi myös rajata aikaa "
        "tai ilmaista määräajan asiayhteydessä: muutan vuodeksi, teen työn perjantaiksi.",
        rules=[
            "Tilan ja muutoksen ero riippuu myös verbistä: olen valmiina / saan valmiiksi.",
            "Essiiviä käytetään ajanilmauksissa kuten maanantaina ja ensi vuonna.",
        ],
        examples=[
            GrammarExample("Toimin vapaaehtoisena, ja myöhemmin minut valittiin ohjaajaksi."),
            GrammarExample("Tarvitsen vastauksen torstaiksi."),
        ],
        related=["fi-object-result-b1"],
    ),
    GrammarTopic(
        "fi-particles-b1",
        "Myös, -kin ja -kaan/-kään",
        "B1",
        "Painotus",
        "Liität uuden asian aiempaan ja kerrot, mihin lisäys kohdistuu.",
        "Kin-liite voi vastata myös-sanaa: minäkin tulen tarkoittaa, että joku "
        "muukin tulee. Tavallisessa kielteisessä lisäyksessä käytetään -kaan/-kään: "
        "minäkään en tule. Liitteen paikka vaikuttaa painotukseen: minäkin luin kirjan "
        "lisää minut lukijoihin, minä luin kirjankin lisää kirjan muihin lukemiini asioihin. "
        "Liitteillä on myös muita, asiayhteydestä riippuvia merkityksiä, joten niitä ei voi "
        "vaihtaa mekaanisesti.",
        rules=[
            "Kiinnitä liite siihen sanaan, jota haluat korostaa.",
            "Vokaalisointu säilyy: minäkään, hänkään, Pekkaakaan.",
        ],
        examples=[
            GrammarExample("Sain ohjeen sähköpostilla. Siskonikin sai sen."),
            GrammarExample("En ymmärtänyt viimeistä kohtaa. Naapurinikaan ei ymmärtänyt sitä."),
        ],
        related=["fi-concession-b1"],
    ),
]
