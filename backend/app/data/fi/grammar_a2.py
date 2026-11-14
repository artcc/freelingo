"""Finnish A2 grammar: forms, narration and connected everyday speech."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "fi-gradation-a2",
        "Astevaihtelu tutuissa sanoissa",
        "A2",
        "Vartalot",
        "Tunnista vahva ja heikko konsonantti sanan taivutuksessa.",
        "Monissa sanoissa k, p ja t vaihtelevat taivutuksessa. Tavallisia pareja ovat "
        "kk–k, pp–p ja tt–t: pankki–pankin, kauppa–kaupan, matto–maton. "
        "Myös t–d, p–v ja k:n kato ovat tavallisia: katu–kadun, lupa–luvan, "
        "jalka–jalan. Konsonanttiyhtymissä tavataan esimerkiksi nk–ng, mp–mm ja nt–nn: "
        "Helsinki–Helsingin, kampa–kamman, ranta–rannan. Myös lt–ll ja rt–rr ovat "
        "tavallisia: silta–sillan, virta–virran. Verbeissä on esimerkiksi ottaa–otan–ottaa. "
        "Sääntö ei koske jokaista k:ta, p:tä tai t:tä. Suuntakaan ei ole aina sama: "
        "ottaa–otan sisältää heikkenemisen, mutta tavata–tapaan vahvistumisen. "
        "Opettele nominin perusmuoto ja genetiivi sekä verbin perusmuoto ja "
        "persoonamuodot yhdessä. Kauppa-sanan yksikön genetiivissä ja inessiivissä on "
        "heikko aste, illatiivissa vahva: kaupan, kaupassa, kauppaan. Älä siis käytä "
        "genetiivin heikkoa vartaloa kaikissa sijoissa. Ottaa-verbin minä-muodossa otan "
        "ja kieltomuodossa en ota on heikko aste, hän-muodossa ottaa vahva aste.\n\n"
        "Myös muu vartalo voi muuttua. Tavallisia sarjoja ovat huone–huoneen–huonetta, "
        "nainen–naisen–naista ja uusi–uuden–uutta. I-loppuiset sanat eivät kaikki taivu "
        "samoin: pankki–pankin, mutta ovi–oven. Nämä vartalonmuutokset eivät kaikki ole "
        "astevaihtelua. Muita tuttuja malleja ovat puhelin–puhelimen–puhelinta ja "
        "sairas–sairaan–sairasta. Tarkista uuden sanan taivutusmalli ennen päätteen lisäämistä.",
        rules=[
            "Älä muuta kaikkia konsonantteja saman mallin mukaan.",
            "Genetiivi auttaa löytämään monen nominin taivutusvartalon.",
        ],
        examples=[GrammarExample("Kaupan ovi on auki."), GrammarExample("Otan takin mukaan.")],
        common_mistakes=[
            GrammarMistake(
                "kauppan ovi", "kaupan ovi", "Kauppa-sanan genetiivissä pp muuttuu p:ksi."
            )
        ],
        related=["fi-genitive-a1", "fi-present-a1"],
    ),
    GrammarTopic(
        "fi-plural-nominative-a2",
        "Monikon perusmuoto ja genetiivi: talot ja talojen",
        "A2",
        "Nominit",
        "Nimeä useita asioita ja kerro, kenelle ne kuuluvat.",
        "Monikon nominatiivin tunnus on -t. Se liittyy tavallisesti samaan vartaloon kuin "
        "yksikön genetiivin -n: talon–talot, kadun–kadut, huoneen–huoneet. "
        "Tavallisen monikollisen subjektin kanssa verbi on yleiskielessä monikossa: "
        "Lapset leikkivät. Kaikki monikon tehtävät eivät käytä t-muotoa; epämääräinen "
        "määrä ilmaistaan usein monikon partitiivilla.\n\n"
        "Useaan omistajaan tai määritteeseen viitataan monikon genetiivillä: "
        "talojen ovet, lasten huone. Opettele tavalliset muodot sanoittain: "
        "talo–talojen, huone–huoneiden, nainen–naisten, lapsi–lasten. "
        "Monikon genetiivillä on useita päätteitä, joten pelkkä t:n vaihtaminen n:ksi ei riitä.",
        structure="talon → talot; huoneen → huoneet",
        rules=[
            "Käytä t-monikkoa esimerkiksi tutuista kokonaisista esineistä.",
            "Lukusanan jälkeen muoto on silti kaksi taloa, ei kaksi talot.",
        ],
        examples=[
            GrammarExample("Ikkunat ovat auki."),
            GrammarExample("Lapset leikkivät pihalla."),
            GrammarExample("Lasten huoneen ikkunat ovat auki."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Kaksi talot.", "Kaksi taloa.", "Perusmuotoinen kaksi vaatii yksikön partitiivin."
            )
        ],
        related=["fi-gradation-a2", "fi-numbers-a1"],
    ),
    GrammarTopic(
        "fi-adjective-agreement-a2",
        "Adjektiivi taipuu substantiivin mukana",
        "A2",
        "Nominit",
        "Taivuta substantiivin edellä oleva adjektiivi tutussa luvussa ja sijassa.",
        "Substantiivin edessä oleva adjektiivi on tavallisesti samassa luvussa ja sijassa "
        "kuin substantiivi: pieni talo, pienessä talossa, pienet talot. "
        "Molempien sanojen vartalo voi muuttua: uusi huone, uuden huoneen ovi, "
        "uudessa huoneessa, uudet huoneet. Tässä harjoitellaan substantiivin edellä "
        "olevaa määritettä yksikön tutuissa sijoissa ja monikon nominatiivissa. "
        "Olla-verbin jälkeiseen kuvaukseen tätä sääntöä ei sovelleta sellaisenaan; "
        "sen sijanvalintaa käsitellään monikon partitiivin yhteydessä.",
        rules=[
            "Taivuta myös edellä oleva kuvaileva sana.",
            "Opettele vartalot: pieni–pienen, uusi–uuden.",
        ],
        examples=[
            GrammarExample("Asun pienessä talossa."),
            GrammarExample("Uudet verhot ovat makuuhuoneessa."),
            GrammarExample("Pienen huoneen ikkuna on auki."),
        ],
        common_mistakes=[
            GrammarMistake(
                "pieni talossa", "pienessä talossa", "Molemmat sanat ovat tässä inessiivissä."
            )
        ],
        related=["fi-plural-nominative-a2", "fi-inner-local-a1"],
    ),
    GrammarTopic(
        "fi-plural-partitive-a2",
        "Monikon partitiivi: kirjoja ja kenkiä",
        "A2",
        "Nominit",
        "Puhu epämääräisestä määrästä ja kuvaile useita asioita.",
        "Monikon partitiivi ilmaisee usein rajaamatonta määrää: Ostan omenoita. "
        "Tavallisia muotoja ovat kirja–kirjoja, talo–taloja, kenkä–kenkiä, "
        "huone–huoneita ja nainen–naisia. Muoto riippuu sanatyypistä; yhtä päätettä "
        "ei voi lisätä kaikkiin sanoihin. Monikon tunnus i voi näkyä j:nä vokaalien "
        "välissä. Paljon ja monta käyttäytyvät eri tavoin: paljon kirjoja, monta kirjaa.\n\n"
        "Paikan sisältöä esittelevässä lauseessa käytetään usein yksiköllistä verbiä ja "
        "partitiivia: Pihalla on lapsia. Kun puhutaan jo tunnetuista lapsista, tavallinen "
        "rakenne on Lapset ovat pihalla. Kielteisessä esittelylauseessa sanotaan "
        "Pihalla ei ole lapsia. Valinta riippuu siis myös siitä, esitelläänkö uusi joukko "
        "vai kerrotaanko tunnetun joukon sijainti.\n\n"
        "Olla-verbin jälkeinen kuvaileva adjektiivi eli predikatiivi ei aina ole samassa "
        "sijassa kuin subjekti. Sija riippuu kuvattavasta asiasta: laskettavasta yksiköstä "
        "Talo on pieni, aineesta Vesi on kylmää ja monista erillisistä asioista "
        "Talot ovat pieniä. Vertaa substantiivin edellä olevaa määritettä ja "
        "predikatiivia: pienet talot – Talot ovat pieniä. Tavallisia adjektiivin "
        "monikon partitiiveja ovat pieni–pieniä, uusi–uusia ja kaunis–kauniita. "
        "Kun monikollinen sana tarkoittaa yhtä kokonaisuutta, predikatiivi on usein nominatiivissa: "
        "Housut ovat pitkät. Kaikki monikolliset kuvaukset eivät siis vaadi partitiivia.",
        rules=[
            "Opettele sanan monikon partitiivi osana taivutussarjaa.",
            "Adjektiivikin taipuu: uusia kenkiä.",
        ],
        examples=[
            GrammarExample("Kaupassa on tuoreita omenoita."),
            GrammarExample("Tarvitsen uusia kenkiä."),
            GrammarExample(
                "Talot ovat pieniä.",
                note="Vertaa substantiivin edellä olevaan määritteeseen: pienet talot.",
            ),
            GrammarExample(
                "Housut ovat pitkät.",
                note="Sana housut on monikollinen mutta tarkoittaa tässä yhtä vaatekappaletta.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                "paljon kirjat",
                "paljon kirjoja",
                "Epämääräinen suuri määrä saa monikon partitiivin.",
            )
        ],
        related=["fi-partitive-a1", "fi-adjective-agreement-a2"],
    ),
    GrammarTopic(
        "fi-demonstratives-a2",
        "Tämä, tuo ja se",
        "A2",
        "Pronominit",
        "Osoita asiaa ja viittaa jo mainittuun tietoon.",
        "Tämä viittaa usein lähellä olevaan asiaan, tuo kauempana osoitettavaan. "
        "Se viittaa usein keskustelussa jo tunnettuun asiaan. Monikot ovat nämä, nuo "
        "ja ne. Pronomini taipuu substantiivin mukana: tässä kaupassa, tuosta laukusta, "
        "näitä kenkiä. Puheessa se voi viitata myös ihmiseen; yleiskielisessä tekstissä "
        "ihmisestä käytetään tavallisesti hän-pronominia.",
        rules=[
            "Sovita osoittava pronomini nimen sijaan ja lukuun.",
            "Valitse viittaus keskustelutilanteen, älä vain etäisyyden mukaan.",
        ],
        examples=[
            GrammarExample("Nämä kengät ovat sopivat."),
            GrammarExample("Tässä kaupassa on paljon kirjoja."),
        ],
        common_mistakes=[
            GrammarMistake("tämä kaupassa", "tässä kaupassa", "Myös pronomini saa paikallissijan.")
        ],
        related=["fi-plural-partitive-a2", "fi-adjective-agreement-a2"],
    ),
    GrammarTopic(
        "fi-inner-local-a2",
        "Sisäpaikallissijojen vartalot",
        "A2",
        "Paikka",
        "Laajenna missä–mistä–mihin-sarjoja uusiin sanatyyppeihin.",
        "Inessiivi ja elatiivi käyttävät usein genetiivistä tuttua vartaloa: "
        "huoneen–huoneessa–huoneesta. Illatiivin tavallisia malleja ovat vokaalin "
        "pidennys ja n (taloon), -hVn (maahan) sekä -seen (huoneeseen). "
        "Monikossa tavallisia sarjoja ovat taloissa–taloista–taloihin ja "
        "kaupoissa–kaupoista–kauppoihin. Vartalo ja aste voivat muuttua muotojen välillä. "
        "Opettele kokonaiset käyttökelpoiset sarjat.",
        rules=[
            "Määränpää ei aina muodostu vain lisäämällä -n.",
            "Käytä monikkoa, kun tarkoitat useita paikkoja.",
        ],
        examples=[
            GrammarExample("Menen huoneeseen."),
            GrammarExample("Näissä kaupoissa on alennus."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Menen huoneen.",
                "Menen huoneeseen.",
                "Huoneen on genetiivi; määränpää on huoneeseen.",
            )
        ],
        related=["fi-inner-local-a1", "fi-gradation-a2", "fi-demonstratives-a2"],
    ),
    GrammarTopic(
        "fi-outer-local-a2",
        "Paikka, vastaanottaja ja väline",
        "A2",
        "Paikka",
        "Käytä -lla, -lta ja -lle myös muuhun kuin paikkaan.",
        "Ulkopaikallissijat ilmaisevat pintaa tai tavallista sijaintia: asemalla, "
        "asemalta, asemalle. Ne ilmaisevat myös vastaanottajaa ja lähdettä: annan "
        "ystävälle, saan ystävältä. Väline ilmaistaan usein -lla/-llä-päätteellä: "
        "kirjoitan kynällä, matkustan junalla. Monikon tuttuja muotoja ovat "
        "pöydillä, pöydiltä ja pöydille. Vastaanottaja ei siis ole sama asia kuin "
        "lauseen tekemisen kohde.",
        rules=[
            "Kysy vastaanottajaa: kenelle? Lähdettä: keneltä?",
            "Jalkaisin on tavallinen ilmaus kävelemisestä kulkutapana.",
        ],
        examples=[
            GrammarExample("Lähetän ystävälle viestin."),
            GrammarExample("Saan neuvoja opettajalta."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Annan sinä kirjan.",
                "Annan sinulle kirjan.",
                "Kun sinä saat kirjan, olet vastaanottaja: sinulle.",
            )
        ],
        related=["fi-outer-local-a1", "fi-plural-nominative-a2"],
    ),
    GrammarTopic(
        "fi-postpositions-a2",
        "Vieressä, takana ja edessä",
        "A2",
        "Paikka",
        "Kuvaile sijaintia suhteessa toiseen asiaan.",
        "Monet paikkasanat ovat postpositioita eli ne tulevat määritteensä jälkeen. "
        "Määrite on usein genetiivissä: talon edessä, aseman takana, kaupan vieressä. "
        "Suunta muuttaa myös postpositiota: edessä–edestä–eteen, "
        "takana–takaa–taakse, vieressä–vierestä–viereen. "
        "Kaikki paikkailmaukset eivät seuraa tätä rakennetta: lähellä asemaa käyttää "
        "partitiivia. Opettele sana ja sen täydennys yhdessä.",
        rules=[
            "Käytä genetiiviä tutuissa vieressä-, takana- ja edessä-rakenteissa.",
            "Erota paikassa oleminen ja sinne siirtyminen.",
        ],
        examples=[
            GrammarExample("Pysäkki on koulun edessä."),
            GrammarExample("Tule aseman viereen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "koulu edessä", "koulun edessä", "Edessä saa tässä genetiivimuotoisen määritteen."
            )
        ],
        related=["fi-genitive-a1", "fi-inner-local-a2"],
    ),
    GrammarTopic(
        "fi-object-a2",
        "Luen kirjaa vai luen kirjan?",
        "A2",
        "Lauseet",
        "Erota kielto, keskeneräisyys ja rajattu kokonaisuus.",
        "Partitiivi voi ilmaista keskeneräistä toimintaa: Luen kirjaa. "
        "Rajattu kokonaisuus saa usein yksikössä -n-muodon: Luen kirjan tänään "
        "tarkoittaa tässä koko kirjan lukemista. Kielto vaatii tavallisesti partitiivin: "
        "En lue kirjaa. Joidenkin verbien kohde on muutenkin partitiivissa, esimerkiksi "
        "odotan bussia. Kokonaisen kohteen muoto riippuu myös lauserakenteesta; "
        "käskyssä sanotaan Ota kirja. Tätä harjoitellaan käskyjen yhteydessä. "
        "Persoonapronominien kokonaiset kohdemuodot ovat minut, sinut, hänet, meidät, teidät, heidät. "
        "Totaaliobjekti ei siis tarkoita aina n-päätettä: monikossa sanotaan ostan liput, "
        "mutta kielteisessä lauseessa en osta lippuja.",
        rules=[
            "Valitse muoto merkityksen ja verbin perusteella.",
            "Tämän tason tavallinen aktiivinen lause: ostan lipun; en osta lippua.",
        ],
        examples=[
            GrammarExample("Kirjoitan viestiä.", note="Työ on kesken."),
            GrammarExample("Kirjoitan viestin loppuun.", note="Tavoitteena on valmis viesti."),
        ],
        common_mistakes=[
            GrammarMistake(
                "En osta lipun.", "En osta lippua.", "Kielteisen lauseen kohde on partitiivissa."
            )
        ],
        related=["fi-partitive-a1", "fi-genitive-a1"],
    ),
    GrammarTopic(
        "fi-imperfect-a2",
        "Imperfekti: eilen kävin",
        "A2",
        "Aika ja verbit",
        "Kerro tapahtumasta tai tilanteesta menneenä ajankohtana.",
        "Imperfekti kertoo menneestä: Eilen kävin kurssilla. Tunnus on usein i: "
        "puhun–puhuin, asun–asuin. Vartalo voi muuttua: menen–menin, "
        "otan–otin, syön–söin, tarvitsen–tarvitsin. Joissakin verbeissä tunnus on "
        "si: haluan–halusin, vastaan–vastasin. Olla taipuu olin, olit, oli, olimme, "
        "olitte, olivat. Opettele tavalliset minä- ja hän-muodot yhdessä: luin–luki. "
        "Imperfekti ei yksin tarkoita valmista tulosta: Luin kirjaa, mutta se jäi kesken.",
        rules=[
            "Käytä imperfektiä esimerkiksi eilen- ja viime viikolla -ilmauksissa.",
            "Persoonapääte tulee menneen ajan vartalon jälkeen.",
        ],
        examples=[
            GrammarExample("Eilen opiskelin kotona."),
            GrammarExample("Viime viikolla olimme Tampereella."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Eilen minä menimme kurssille.",
                "Eilen minä menin kurssille.",
                "Minä tarvitsee yksikön muodon menin; menimme on me-muoto.",
            )
        ],
        related=["fi-present-a1", "fi-gradation-a2", "fi-object-a2"],
    ),
    GrammarTopic(
        "fi-negative-past-a2",
        "En käynyt, emme käyneet",
        "A2",
        "Aika ja verbit",
        "Kerro, mikä jäi tapahtumatta menneenä aikana.",
        "Kielteinen imperfekti käyttää kieltoverbiä ja mennyttä partisiippia: "
        "en puhunut, et puhunut, hän ei puhunut; emme puhuneet, ette puhuneet, "
        "he eivät puhuneet. Partisiipin tavallisia muotoja ovat syönyt–syöneet, "
        "mennyt–menneet ja ollut–olleet. Osa muodoista vaatii oman mallin: "
        "tullut, opiskellut, pessyt. Imperfektin i-muotoa ei käytetä kieltoverbin jälkeen.",
        structure="en + puhunut; emme + puhuneet",
        rules=[
            "Yksikössä partisiippi päättyy usein -nut/-nyt, monikossa -neet.",
            "Olla-verbin mennyt kielto on en ollut, emme olleet.",
        ],
        examples=[
            GrammarExample("En käynyt eilen töissä."),
            GrammarExample("He eivät tulleet kokoukseen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "En menin.", "En mennyt.", "Kielteinen mennyt aika tarvitsee partisiipin."
            )
        ],
        related=["fi-imperfect-a2", "fi-negation-a1"],
    ),
    GrammarTopic(
        "fi-perfect-a2",
        "Perfekti: olen käynyt",
        "A2",
        "Aika ja verbit",
        "Yhdistä mennyt kokemus tai tapahtuma nykyhetkeen.",
        "Perfekti muodostuu olla-verbin preesensistä ja menneestä partisiipista: "
        "olen käynyt, hän on käynyt, olemme käyneet. Se kertoo usein kokemuksesta "
        "ilman tarkkaa mennyttä ajankohtaa tai asiasta, joka jatkuu nykyhetkeen: "
        "Olen asunut täällä kaksi vuotta. Imperfekti sijoittaa tapahtuman tavallisesti "
        "päättyneeseen ajankohtaan: Asuin siellä vuonna 2020. Aikamuodon valinta "
        "riippuu kertojan näkökulmasta, ei vain yhdestä aikasanasta. Yhtä henkilöä "
        "teititeltäessä apuverbi on monikossa mutta partisiippi yksikössä: "
        "Oletteko käynyt täällä aiemmin?",
        rules=[
            "Taivuta olla-verbi persoonassa.",
            "Useasta henkilöstä: olette käyneet; yhtä teititeltäessä: olette käynyt.",
        ],
        examples=[
            GrammarExample("Olen käynyt Oulussa."),
            GrammarExample("Olemme odottaneet tunnin.", note="Odotus liittyy nykyhetkeen."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Olen kävin.",
                "Olen käynyt.",
                "Perfekti tarvitsee partisiipin, ei imperfektimuotoa.",
            )
        ],
        related=["fi-negative-past-a2", "fi-olla-pronouns-a1"],
    ),
    GrammarTopic(
        "fi-negative-perfect-a2",
        "En ole vielä tehnyt",
        "A2",
        "Aika ja verbit",
        "Kerro kokemuksen puuttumisesta tai keskeneräisestä tilanteesta.",
        "Kielteinen perfekti muodostuu kieltoverbistä, ole-muodosta ja partisiipista: "
        "en ole käynyt, he eivät ole käyneet. Vielä kertoo, että asia voi tapahtua "
        "myöhemmin: En ole vielä syönyt. Koskaan liittyy usein kokemukseen: "
        "En ole koskaan käynyt Lapissa. Erota eilisen tapahtuman kielto "
        "(en käynyt eilen) ja nykyhetkeen liittyvä puuttuva kokemus (en ole käynyt).",
        rules=[
            "Ole pysyy samana kaikissa persoonissa tässä rakenteessa.",
            "Partisiippi mukautuu yksikköön tai monikkoon.",
        ],
        examples=[
            GrammarExample("En ole vielä varannut aikaa."),
            GrammarExample("Emme ole koskaan kokeilleet tätä ruokaa."),
        ],
        common_mistakes=[
            GrammarMistake(
                "En olen käynyt.", "En ole käynyt.", "Kieltoverbin jälkeen olla on muodossa ole."
            )
        ],
        related=["fi-perfect-a2", "fi-negation-a1"],
    ),
    GrammarTopic(
        "fi-comparison-a2",
        "Suurempi kuin ja kaikkein suurin",
        "A2",
        "Adjektiivit",
        "Vertaa kahta vaihtoehtoa ja tunnista ryhmän ääripää.",
        "Komparatiivin tunnus on -mpi: uusi–uudempi, pieni–pienempi. "
        "Kaksitavuisen a/ä-loppuisen adjektiivin vokaali muuttuu usein e:ksi: "
        "halpa–halvempi. Hyvä saa muodon parempi. Vertailukohta ilmaistaan usein "
        "kuin-sanalla: Tämä reitti on lyhyempi kuin toinen. Superlatiivi ilmaisee "
        "ryhmän ääripään: suurin, halvin, paras. Muodot taipuvat: halvemmassa "
        "hotellissa. Harjoittele ensin tavallisia vertailupareja.",
        rules=["Kuin aloittaa vertailukohdan.", "Hyvä–parempi–paras on epäsäännöllinen sarja."],
        examples=[
            GrammarExample("Juna on nopeampi kuin bussi."),
            GrammarExample("Tämä on retken helpoin reitti."),
        ],
        common_mistakes=[
            GrammarMistake(
                "hyvämpi vaihtoehto", "parempi vaihtoehto", "Hyvä-sanan komparatiivi on parempi."
            )
        ],
        related=["fi-adjective-agreement-a2"],
    ),
    GrammarTopic(
        "fi-imperative-a2",
        "Tule, tulkaa ja älä unohda",
        "A2",
        "Verbit",
        "Anna lyhyt ohje yhdelle tai usealle ihmiselle.",
        "Yhden henkilön tavallinen myönteinen käsky saadaan minä-muodosta ilman "
        "loppu-n: tulen–tule, otan–ota, luen–lue. Olla-verbin käsky on ole. "
        "Kielteinen käsky käyttää älä-sanaa: älä tule, älä ota. Kokonainen "
        "yksiköllinen esinekohde on käskyssä perusmuodossa: Ota takki. Kielteisessä "
        "käskyssä kohde on partitiivissa: Älä ota takkia. Suora käsky sopii ohjeisiin; "
        "pyynnön voi pehmentää kysymyksellä Voitko auttaa?\n\n"
        "Usealle ihmiselle tai yhtä teititeltäessä käytetään muotoja tulkaa, "
        "ottakaa, syökää ja olkaa. Vartalo voi erota sinä-käskystä: tule–tulkaa, "
        "ota–ottakaa. Kielto on älkää ja pääverbin -ko/-kö-muoto: älkää tulko, "
        "älkää ottako, älkää syökö. Myös tässä substantiivin totaaliobjekti on nominatiivissa: "
        "Ottakaa takki mukaan.",
        rules=[
            "Erota tule yhdelle ja tulkaa usealle tai yhtä teititeltäessä.",
            "Älä-muodon jälkeen ei käytetä persoonapäätettä.",
        ],
        examples=[
            GrammarExample("Sulje ovi, kiitos."),
            GrammarExample("Älä unohda avainta."),
            GrammarExample("Tulkaa sisään. Älkää jättäkö ovea auki."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Ota takin.",
                "Ota takki.",
                "Myönteisen käskyn kokonainen esinekohde on perusmuodossa.",
            )
        ],
        related=["fi-present-a1", "fi-object-a2"],
    ),
    GrammarTopic(
        "fi-modal-meanings-a2",
        "Osaan, saan ja voin",
        "A2",
        "Verbit",
        "Erota taito, lupa ja tilanteen mahdollisuus.",
        "Osata kertoo opitusta taidosta: Osaan uida. Saada kertoo tässä käytössä luvasta: "
        "Saat mennä. Voida kertoo mahdollisuudesta: Voin tulla huomenna. "
        "Tilanne voi tuoda merkitykset lähelle toisiaan, joten voinko on tavallinen myös "
        "lupaa pyydettäessä. Saada-verbi tarkoittaa toisissa rakenteissa vastaanottamista: "
        "Sain kirjeen. Modaalikäytössä verbiä seuraa perusmuoto.",
        rules=["Tarkista merkitys koko tilanteesta.", "Kielto: en osaa, en saa, en voi."],
        examples=[
            GrammarExample("Osaan ajaa, mutta en voi ajaa tänään."),
            GrammarExample("Saanko käyttää tätä tietokonetta?"),
        ],
        common_mistakes=[
            GrammarMistake("Osaan uin.", "Osaan uida.", "Osata-verbin täydennys on perusmuodossa.")
        ],
        related=["fi-modals-a1", "fi-imperfect-a2"],
    ),
    GrammarTopic(
        "fi-necessity-a2",
        "Minun täytyy ja minun ei tarvitse",
        "A2",
        "Lauseet",
        "Ilmaise velvollisuus ja tarpeen puuttuminen.",
        "Täytyä ja pitää ilmaisevat velvollisuutta rakenteessa minun täytyy lähteä, "
        "sinun pitää soittaa. Tekijä on genetiivissä ja verbi pysyy kolmannessa "
        "persoonassa: meidän täytyy. Tarpeen puuttuminen ilmaistaan tavallisesti "
        "rakenteella ei tarvitse: Sinun ei tarvitse tulla. Se ei ole kielto. "
        "Kielto ilmaistaan esimerkiksi et saa tulla. Tässä rakenteessa kokonainen "
        "esinekohde on perusmuodossa: Minun täytyy ostaa lippu.",
        rules=[
            "Tekijä: minun, sinun, hänen, meidän, teidän, heidän.",
            "Erota sinun ei tarvitse ja sinä et saa.",
        ],
        examples=[
            GrammarExample("Meidän täytyy lähteä ajoissa."),
            GrammarExample("Sinun ei tarvitse maksaa uudestaan."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Minä täytyy lähteä.",
                "Minun täytyy lähteä.",
                "Täytyä-rakenteen tekijä on genetiivissä.",
            )
        ],
        related=["fi-genitive-a1", "fi-modal-meanings-a2", "fi-object-a2"],
    ),
    GrammarTopic(
        "fi-infinitives-a2",
        "Menen syömään ja olen syömässä",
        "A2",
        "Verbit",
        "Liitä tekeminen liikkeeseen tai meneillään olevaan toimintaan.",
        "Kaikki verbit eivät saa perusmuotoista täydennystä. Mennä ja tulla voivat saada "
        "muodon -maan/-mään: menen uimaan, tulen syömään. Olla yhdistyy muotoon "
        "-massa/-mässä: olen syömässä. Toiminnasta palaamista ilmaisee "
        "-masta/-mästä: tulen uimasta. Vartalon löytää usein he-muodosta ilman "
        "-vat/-vät-päätettä: lukevat–lukemaan. Erota haluan syödä ja menen syömään.",
        rules=[
            "Valitse täydennyksen muoto ensimmäisen verbin ja merkityksen mukaan.",
            "Vokaalisointu näkyy muodoissa syömään ja lukemaan.",
        ],
        examples=[
            GrammarExample("Lähden opiskelemaan."),
            GrammarExample("Olen kirjastossa lukemassa."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Menen syödä.",
                "Menen syömään.",
                "Kun lähdet tekemään jotakin, käytä -maan/-mään-muotoa.",
            )
        ],
        related=["fi-modal-meanings-a2", "fi-inner-local-a2", "fi-present-a1"],
    ),
    GrammarTopic(
        "fi-subordination-a2",
        "Että, koska, kun ja jos",
        "A2",
        "Lauseet",
        "Kerro tiedon sisältö, syy, aika tai ehto.",
        "Että aloittaa esimerkiksi ajatuksen tai tiedon sisällön: Tiedän, että hän tulee. "
        "Koska ilmaisee syyn: Jään kotiin, koska olen sairas. Kun kertoo ajallisesta "
        "yhteydestä: Soitan, kun tulen kotiin. Jos ilmaisee ehdon: Jos sataa, jäämme "
        "sisälle. Sivulauseessa verbi taipuu tavallisesti persoonassa kuten muussakin "
        "lauseessa. Sivulause voi olla myös alussa; sen ja päälauseen väliin tulee "
        "tavallisesti pilkku.",
        rules=[
            "Erota varmana tai toteutuvana esitetty aika (kun) ja ehto (jos).",
            "Älä jätä taipunutta verbiä pois sivulauseesta.",
        ],
        examples=[
            GrammarExample("Tulen, jos ehdin."),
            GrammarExample("Kun kurssi päättyy, menemme kahville."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Tiedän, että hän tulla.",
                "Tiedän, että hän tulee.",
                "Että-lauseessa on taipunut verbi.",
            )
        ],
        related=["fi-coordination-a1", "fi-present-a1", "fi-necessity-a2"],
    ),
]
