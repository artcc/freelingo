"""Finnish B2 grammar connecting concise texts with practical interaction."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "fi-active-participle-b2",
        "Saapuva vieras ja saapunut vieras",
        "B2",
        "Partisiipit",
        "Aktiivin partisiippi kuvaa henkilöä tai asiaa toiminnan kautta.",
        "VA-partisiippi vastaa usein joka tekee -lausetta: saapuva vieras on vieras, "
        "joka saapuu. NUT-partisiippi kuvaa aiempaa toimintaa: saapunut vieras on jo "
        "saapunut. Ajallinen suhde ratkaistaan muun lauseen ja tilanteen perusteella, "
        "ei vain puhehetkestä. Määrite taipuu pääsanan mukana: saapuville vieraille, "
        "saapuneiden vieraiden. Sama NUT-muoto tunnetaan perfektistä.",
        structure="saapuva / saapunut; saapuvat / saapuneet",
        rules=[
            "Säilytä partisiipin ja pääsanan sijan sekä luvun yhteys.",
            "Käytä joka-lausetta, jos pitkä määrite vaikeuttaa ymmärtämistä.",
        ],
        examples=[
            GrammarExample("Lähetämme saapuville vieraille kulkuohjeet."),
            GrammarExample("Eilen saapuneet vieraat ovat jo tutustuneet alueeseen."),
        ],
        related=["fi-pluperfect-b1", "fi-relative-b1", "fi-passive-participle-b2"],
    ),
    GrammarTopic(
        "fi-passive-participle-b2",
        "Tehtävä työ ja tehty työ",
        "B2",
        "Partisiipit",
        "Passiivin partisiippi kuvaa toiminnan kohdetta.",
        "TAVA-partisiippi voi kuvata suunniteltua tai vaadittua toimintaa: huomenna "
        "käsiteltävä asia. TU-partisiippi ilmaisee aiempaa toimintaa: eilen käsitelty "
        "asia. Määrite taipuu pääsanan mukana: korjattavassa laitteessa, korjatuista "
        "laitteista. Rakenne ei yleensä nimeä tekijää. On tehtävä -velvollisuusrakenne "
        "on erotettava pelkästä substantiivin määritteestä.",
        structure="käsiteltävä asia / käsitelty asia",
        rules=[
            "Partisiipin merkitys tarkentuu ajanmääritteen ja asiayhteyden avulla.",
            "TU-partisiippi ei yksin kerro, onko lopputulos edelleen voimassa.",
        ],
        examples=[
            GrammarExample("Huomenna esiteltävä suunnitelma on nähtävillä verkossa."),
            GrammarExample("Viime viikolla hyväksytyssä suunnitelmassa on kolme vaihetta."),
        ],
        related=["fi-passive-perfect-b1", "fi-agent-participle-b2"],
    ),
    GrammarTopic(
        "fi-agent-participle-b2",
        "Asukkaan tekemä ehdotus",
        "B2",
        "Partisiipit",
        "Agenttipartisiippi nimeää tekijän tiiviissä määritteessä.",
        "MA-partisiippi liittää tekijän toiminnan kohteeseen: asukkaan tekemä ehdotus "
        "on ehdotus, jonka asukas teki. Tekijä on genetiivissä. Kun tekijänä on "
        "persoonapronomini, yleiskielessä käytetään omistusliitettä: minun tekemäni, "
        "hänen tekemänsä. Partisiippi taipuu pääsanan mukaan: asukkaan tekemästä "
        "ehdotuksesta. Rakenteen kohde on tekemisen kohde, ei tekijä.",
        structure="tekijän + tekemä + kohde; tekemäni ehdotus",
        rules=[
            "Erota tekijä ja kohde: johtajan lähettämä viesti on johtajalta.",
            "Älä käytä agenttipartisiippia verbistä, jolla ei ole sopivaa objektia.",
        ],
        examples=[
            GrammarExample("Käsittelemme asukkaiden esittämät toiveet kokouksessa."),
            GrammarExample("Löysitkö lähettämäni aikataulun?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Yleiskielinen tiedote: minun laatima suunnitelma",
                "Yleiskielinen tiedote: minun laatimani suunnitelma",
                "Puheessa omistusliite voi jäädä pois; tässä harjoitellaan yleiskieltä.",
            ),
        ],
        related=["fi-passive-participle-b2", "fi-relative-b1"],
    ),
    GrammarTopic(
        "fi-negative-participle-b2",
        "Ratkaisematon kysymys",
        "B2",
        "Partisiipit",
        "Kielteinen partisiippi ilmaisee puuttuvaa toimintaa tai ominaisuutta.",
        "MATON-partisiippi muodostaa kielteisiä määritteitä: käsittelemätön hakemus "
        "on hakemus, jota ei ole käsitelty. Merkitys voi olla aktiivinen tai "
        "passiivinen: puhumaton lapsi ei puhu; avaamaton kirje on kirje, jota ei ole avattu. "
        "Taivutusvartalo muuttuu: käsittelemättömän, käsittelemättömiä. Sanan merkitys "
        "ja asiayhteys ratkaisevat, onko kyse tilapäisestä tilanteesta vai ominaisuudesta.",
        rules=[
            "Älä päättele tekijää tai aikamuotoa yksin MATON-päätteestä.",
            "Erota tekemätön työ ja mahdoton työ: tekemättä jääminen ei tarkoita mahdottomuutta.",
        ],
        examples=[
            GrammarExample("Listalla on vielä kaksi ratkaisemattomaa kysymystä."),
            GrammarExample("Avaamattoman pakkauksen voi palauttaa näiden ehtojen mukaisesti."),
        ],
        related=["fi-passive-participle-b2"],
    ),
    GrammarTopic(
        "fi-referative-present-b2",
        "Hän kertoo tarvitsevansa apua",
        "B2",
        "Referatiivirakenne",
        "VA-muoto tiivistää tiedon, havainnon tai ajatuksen sisältävän että-lauseen.",
        "Kertoo tarvitsevansa vastaa lausetta kertoo, että hän tarvitsee. Kun "
        "tekijä on sama kuin päälauseessa, käytetään omistusliitettä. Eri tekijä "
        "ilmaistaan genetiivillä: huomaan asiakkaan odottavan. VA-muoto ilmaisee "
        "tavallisesti samanaikaisuutta tai myöhempää tapahtumaa suhteessa päälauseeseen. "
        "Kielteinen sisältö on usein selkeintä ilmaista että-lauseella.",
        structure="kertoo tarvitsevansa; huomaan asiakkaan odottavan",
        rules=[
            "Tarkista, kenen toiminnasta omistusliite kertoo.",
            "Johtoverbi voi olla menneessä: hän kertoi tarvitsevansa apua.",
        ],
        examples=[
            GrammarExample("Huomasin puhelimen soivan kesken kokouksen."),
            GrammarExample("Sari sanoo palaavansa huomenna."),
        ],
        related=["fi-active-participle-b2", "fi-reported-speech-b1"],
    ),
    GrammarTopic(
        "fi-referative-past-b2",
        "Hän kertoo lähettäneensä hakemuksen",
        "B2",
        "Referatiivirakenne",
        "NUT-muoto sijoittaa referoidun tapahtuman päälauseen tapahtumaa aikaisemmaksi.",
        "Kertoo lähettäneensä tarkoittaa, että lähettäminen edeltää kertomista. "
        "Muoto perustuu NUT-partisiipin genetiivivartaloon: tehnyt → tehneen → "
        "tehneensä. Sama tekijä näkyy omistusliitteessä, eri tekijä genetiivissä: "
        "tiedän Annan lähteneen. Rakenne välittää väitteen; johtoverbin merkitys "
        "vaikuttaa siihen, esittääkö kertoja sisällön tietona vai pelkkänä väitteenä.",
        structure="sanoo tehneensä; sanoo Annan tehneen",
        rules=[
            "Erota kertoo lähtevänsä ja kertoo lähteneensä.",
            "Säilytä lähteen epävarmuus: väittää ei tarkoita samaa kuin osoittaa.",
        ],
        examples=[
            GrammarExample("Asiakas kertoo maksaneensa laskun jo maanantaina."),
            GrammarExample("Luulin kokouksen päättyneen, mutta keskustelu jatkui."),
        ],
        related=["fi-referative-present-b2", "fi-active-participle-b2"],
    ),
    GrammarTopic(
        "fi-temporal-simultaneous-b2",
        "Kokouksen alkaessa",
        "B2",
        "Temporaalirakenne",
        "ESSA-muoto tiivistää samanaikaisuutta ilmaisevan kun-lauseen.",
        "Kokouksen alkaessa vastaa lausetta kun kokous alkaa tai alkoi. Aikamuoto "
        "tulkitaan päälauseesta. Eri tekijä ilmaistaan genetiivillä; sama tekijä "
        "yleiskielessä omistusliitteellä: kirjoittaessani tarkoittaa kun kirjoitan "
        "tai kirjoitin. Rakenne voi kuvata myös toistuvaa tilannetta. Sitä ei "
        "yleensä eroteta pilkulla päälauseesta.",
        structure="kokouksen alkaessa; kirjoittaessani",
        rules=[
            "Varmista, että omistusliitteen tekijä vastaa tarkoitettua henkilöä.",
            "Älä korvaa syytä ilmaisevaa koska-lausetta automaattisesti tällä rakenteella.",
        ],
        examples=[
            GrammarExample("Kokouksen alkaessa kaksi osallistujaa oli vielä matkalla."),
            GrammarExample("Lukiessani ohjetta huomasin ristiriidan."),
        ],
        related=["fi-temporal-b1", "fi-temporal-prior-b2"],
    ),
    GrammarTopic(
        "fi-temporal-prior-b2",
        "Saatuani päätöksen",
        "B2",
        "Temporaalirakenne",
        "TUA-muoto ilmaisee ennen päälauseen tapahtumaa päättyneen toiminnan.",
        "Saatuani päätöksen tarkoittaa sen jälkeen kun olin tai olen saanut "
        "päätöksen. Rakenne muodostetaan passiivin partisiipin partitiivista ja "
        "tarvittaessa omistusliitteestä: tehnyt ei ole lähtömuoto, vaan tehty → "
        "tehtyä → tehtyäni. Muodon passiivinen alkuperä ei tee tekijästä "
        "epämääräistä. Eri tekijä on genetiivissä: kokouksen päätyttyä.",
        structure="tehtyäni; saatuamme; kokouksen päätyttyä",
        rules=[
            "Erota tehdessäni eli samaan aikaan ja tehtyäni eli sen jälkeen.",
            "Pidä tekijä selvänä myös pitkässä virkkeessä.",
        ],
        examples=[
            GrammarExample("Saatuani vahvistuksen varasin junaliput."),
            GrammarExample("Tilaisuuden päätyttyä palautimme avaimet vahtimestarille."),
        ],
        related=["fi-temporal-simultaneous-b2", "fi-passive-participle-b2"],
    ),
    GrammarTopic(
        "fi-final-construction-b2",
        "Saadakseni lisätietoa",
        "B2",
        "Finaalirakenne",
        "KSE-muoto ilmaisee saman tekijän tavoitteen tiiviisti.",
        "Soitin saadakseni lisätietoa vastaa lausetta soitin, jotta saisin "
        "lisätietoa. Lyhyeen infinitiiviin liittyy -kse- ja omistusliite: saada → "
        "saadakseni, saadaksemme. Tavoitteen tekijä on normaalisti sama kuin "
        "päälauseen tekijä. Jos tekijät eroavat, jotta-lause on selkeämpi: "
        "lähetin ohjeen, jotta kollega voisi valmistautua.",
        rules=[
            "Tarkoitus ei todista tavoitteen toteutuneen.",
            "Valitse omistusliite tekijän mukaan: minä saadakseni, me saadaksemme.",
        ],
        examples=[
            GrammarExample("Pyysin tapaamista selvittääkseni laskutuksen virheen."),
            GrammarExample("Harjoittelemme yhdessä valmistautuaksemme esitykseen."),
        ],
        related=["fi-purpose-b1", "fi-temporal-simultaneous-b2"],
    ),
    GrammarTopic(
        "fi-manner-infinitive-b2",
        "Kokeilemalla ja keskeyttämättä",
        "B2",
        "Infinitiivit",
        "Kuvaat keinoa ja tekemättä jäävää rinnakkaistoimintaa.",
        "MALLA-muoto ilmaisee usein keinon: opin kokeilemalla. MATTA-muoto "
        "kertoo, että toiminta puuttuu: poistuin sanomatta mitään. Se ei yksin "
        "vastaa kaikkia kielteisiä sivulauseita. Eri tekijä on tarvittaessa "
        "ilmaistava selvästi, esimerkiksi ilman että -lauseella. MATTA ei "
        "ole sama kuin substantiivia määrittävä MATON.",
        structure="tekemällä / tekemättä",
        rules=[
            "Keino vastaa kysymykseen miten: tarkistan tiedon soittamalla.",
            "Erota lukematta lähteminen ja lukematon viesti.",
        ],
        examples=[
            GrammarExample("Säästämme aikaa yhdistämällä kaksi tapaamista."),
            GrammarExample("Kuuntelin palautteen keskeyttämättä puhujaa."),
        ],
        related=["fi-ma-infinitive-b1", "fi-negative-participle-b2"],
    ),
    GrammarTopic(
        "fi-modal-obligation-b2",
        "On tehtävä, kannattaa ja saa tehdä",
        "B2",
        "Modaalisuus",
        "Tulkitset vaatimuksen, suosituksen ja luvan eri vahvuisiksi.",
        "Minun on tehtävä ilmaisee velvollisuutta ja on tavallinen ohjeissa. "
        "Kannattaa suosittelee hyödyllistä toimintaa, mutta ei yksin määrää. "
        "Saa tehdä antaa luvan; voi tehdä voi ilmaista mahdollisuutta tai lupaa "
        "tilanteen mukaan. Tarpeettomuus ei ole kielto: ei tarvitse toimittaa "
        "ei tarkoita ei saa toimittaa. Virallisen ohjeen sanamuoto kannattaa "
        "varmistaa, jos velvollisuuden laajuus jää epäselväksi.",
        rules=[
            "On tehtävä -rakenteessa tekijä on genetiivissä: hakijan on ilmoitettava.",
            "Substantiivin totaaliobjekti on tässä nominatiivissa: hakijan on toimitettava todistus.",
            "Persoonapronominilla käytetään akkusatiivia: minun on tavattava hänet.",
        ],
        examples=[
            GrammarExample("Hakijan on toimitettava liite määräajassa."),
            GrammarExample("Sinun kannattaa säilyttää kuitti, vaikka sitä ei tarvitse liittää."),
        ],
        related=["fi-necessity-b1", "fi-passive-participle-b2"],
    ),
    GrammarTopic(
        "fi-potential-b2",
        "Lienee ja saapunee: arvion tunnistaminen",
        "B2",
        "Tapaluokat",
        "Tunnistat potentiaalin todennäköisyyttä ilmaisevaksi muodoksi.",
        "Potentiaali ilmaisee arviota: valmistunee tarkoittaa suunnilleen "
        "valmistuu luultavasti. Tunnus on usein -ne-, mutta vartalo voi muuttua: "
        "tulla → tullee, mennä → mennee. Olla-verbin muoto on lienee. "
        "Mennyt arvio voidaan ilmaista lienee saapunut. Muotoja esiintyy "
        "etenkin kirjoitetussa kielessä; aktiivisen käytön sijaan keskeistä on "
        "tunnistaminen ja luonteva selittäminen tavallisilla sanoilla.",
        rules=[
            "Potentiaali ei ole varma lupaus eikä velvollisuus.",
            "Arkipuheessa luultavasti ja varmaan ovat tavallisia vaihtoehtoja.",
        ],
        examples=[
            GrammarExample("Korjaus valmistunee perjantaina, jos varaosa saapuu ajoissa."),
            GrammarExample("Hakemus lienee jo käsitelty, mutta tarkistan asian."),
        ],
        related=["fi-modal-obligation-b2", "fi-hedging-b2"],
    ),
    GrammarTopic(
        "fi-conditional-passive-b2",
        "Voitaisiinko sopia toisin?",
        "B2",
        "Passiivi ja ehdotus",
        "Neuvottelet yhteisestä toiminnasta nimeämättä yhtä tekijää.",
        "Passiivin konditionaali sisältää muodot tehtäisiin ja ei tehtäisi. "
        "Sillä ehdotetaan, kuvitellaan tai arvioidaan yhteistä menettelyä. "
        "Kysymys voitaisiinko siirtää jättää neuvotteluvaraa, mutta ei vielä "
        "merkitse päätöstä. Konditionaalin perfekti on olisi tehty tai ei olisi "
        "tehty, kun tarkastellaan aiempaa vaihtoehtoa.",
        structure="tehtäisiin / ei tehtäisi; olisi tehty",
        rules=[
            "Älä sekoita ehdotusta tehdään ja varovaisempaa ehdotusta tehtäisiinkö.",
            "Passiivissa substantiivin totaaliobjekti on nominatiivissa: aikataulu muutettaisiin.",
            "Persoonapronominin totaaliobjekti on akkusatiivissa: hänet kutsuttaisiin.",
        ],
        examples=[
            GrammarExample("Voitaisiinko määräaikaa pidentää kahdella päivällä?"),
            GrammarExample("Jos tila olisi pienempi, osallistujamäärää rajoitettaisiin."),
        ],
        related=["fi-conditional-b1", "fi-passive-present-b1"],
    ),
    GrammarTopic(
        "fi-passive-pluperfect-b2",
        "Mitä oli jo sovittu?",
        "B2",
        "Passiivi ja aikajärjestys",
        "Erotat aiemmat toimenpiteet myöhemmästä tapahtumasta.",
        "Passiivin pluskvamperfekti on oli tehty, kielteisenä ei ollut tehty. "
        "Se kuvaa ennen mennyttä vertailuhetkeä tapahtunutta toimintaa. "
        "Apuverbi pysyy yksikössä: ehdot oli hyväksytty. Rakenne ei kerro "
        "automaattisesti, kuka teki päätöksen. Jos vastuu on olennainen, nimeä "
        "tekijä aktiivisessa lauseessa tai selitä lähde erikseen.",
        structure="oli sovittu / ei ollut sovittu",
        rules=[
            "Vertailuhetki voi tulla edellisestä virkkeestä.",
            "Älä päättele passiivista, että kaikki osapuolet hyväksyivät asian.",
        ],
        examples=[
            GrammarExample("Kun muutos tuli, liput oli jo varattu."),
            GrammarExample("Kustannuksista ei ollut sovittu ennen työn aloittamista."),
        ],
        related=["fi-pluperfect-b1", "fi-passive-perfect-b1"],
    ),
    GrammarTopic(
        "fi-counterfactual-b2",
        "Jälkiviisaus ja toteutumaton vaihtoehto",
        "B2",
        "Ehdollisuus",
        "Arvioit mennyttä ratkaisua muuttamatta vaihtoehtoa tosiasiaksi.",
        "Jos olisimme tarkistaneet ehdot, olisimme huomanneet rajan kuvaa "
        "menneeseen liittyvää toteutumatonta vaihtoehtoa. Se ei yksin kerro, "
        "kuka oli vastuussa tarkistamisesta. Ehto voi johtaa myös nykyiseen "
        "seuraukseen: jos olisimme säästäneet, meillä olisi nyt vararahasto. "
        "Jälkiarvioinnissa kannattaa erottaa tosiasiat, vaihtoehtoinen kulku "
        "ja tulevaa koskeva parannusehdotus.",
        rules=[
            "Säilytä aikaviite: olisi ollut silloin eroaa muodosta olisi nyt.",
            "Voisi olla tai olisi voinut olla ei takaa vaihtoehdon onnistumista.",
        ],
        examples=[
            GrammarExample("Jos aikataulu olisi tarkistettu, päällekkäisyys olisi huomattu."),
            GrammarExample(
                "Olisimme voineet kysyä ensin; jatkossa varmistamme asian kirjallisesti."
            ),
        ],
        related=["fi-conditional-perfect-b1", "fi-conditional-passive-b2"],
    ),
    GrammarTopic(
        "fi-information-structure-b2",
        "Mikä on tuttua, mikä uutta?",
        "B2",
        "Sanajärjestys ja painotus",
        "Kohdistat huomion olennaiseen tietoon ja korjaat väärän oletuksen.",
        "Suomen sanajärjestys on joustava mutta ei merkityksetön. Virkkeen alku "
        "liittyy usein tuttuun puheenaiheeseen, loppu tuo uutta tietoa. Puheen "
        "painotus voi muuttaa tulkintaa. Juuri, vain ja myös rajaavat huomion "
        "kohdetta: vain Liisa allekirjoitti ei tarkoita samaa kuin Liisa vain "
        "allekirjoitti. Selkeä korjaus nimeää sekä väärän että oikean tiedon.",
        rules=[
            "Älä esitä yhtä sanajärjestystä ainoaksi kieliopilliseksi vaihtoehdoksi.",
            "Sijoita rajaava sana lähelle sitä, mitä rajaat.",
        ],
        examples=[
            GrammarExample("Raportin laati Aino, ei hänen esihenkilönsä."),
            GrammarExample("Vain liite puuttuu; itse hakemus on saapunut."),
        ],
        related=["fi-particles-b1", "fi-quantifier-scope-b2"],
    ),
    GrammarTopic(
        "fi-register-b2",
        "Yleiskieli, puhekieli ja tilanteeseen sopiva viesti",
        "B2",
        "Rekisteri",
        "Mukautat ilmaisun tilanteeseen säilyttäen asiasisällön.",
        "Yleiskielen me menemme ja monen puhekielen me mennään ilmaisevat "
        "saman toiminnan eri rekistereissä. Puhekieli ei ole yksi yhtenäinen "
        "järjestelmä, eikä tuttu muoto sovi jokaiseen kirjalliseen tekstiin. "
        "Viranomaisviestissä selkeä yleiskieli helpottaa tulkintaa; ystävälle "
        "lyhyempi ilmaus voi olla luonteva. Sinuttelu voi olla kohteliasta, "
        "eikä teitittely yksin takaa ystävällistä sävyä.",
        rules=[
            "Arvioi suhdetta, kanavaa ja viestin tavoitetta, älä vain muodollisuutta.",
            "Älä lisää tai poista ehtoja vaihtaessasi rekisteriä.",
        ],
        examples=[
            GrammarExample("Ystävälle: Voitko laittaa sen viestin uudestaan?"),
            GrammarExample("Palveluun: Voisitteko lähettää vahvistuksen uudelleen?"),
        ],
        related=["fi-conditional-b1", "fi-hedging-b2"],
    ),
    GrammarTopic(
        "fi-hedging-b2",
        "Väitteen varmuuden rajaaminen",
        "B2",
        "Modaalisuus ja vuorovaikutus",
        "Ilmaiset, mihin arviosi perustuu ja kuinka varma olet.",
        "Näyttää siltä, käsittääkseni ja tietojeni mukaan rajaavat väitteen "
        "puhujan havaintoon tai tietoon. Ehkä jättää mahdollisuuden avoimeksi; "
        "todennäköisesti ilmaisee vahvempaa arviota. Ilmaisut eivät muodosta "
        "tarkkaa prosenttiasteikkoa. Eriävässä mielipiteessä voit tunnustaa "
        "toisen perusteen ja kertoa oman rajauksesi ilman näennäistä myöntymistä.",
        rules=[
            "Vahvista tarkistettu asia suoraan; älä peitä olennaista ehtoa epämääräisyyteen.",
            "Erota oma epävarmuutesi lähteen epävarmuudesta.",
        ],
        examples=[
            GrammarExample("Käsittääkseni tarjous koskee vain nykyisiä asiakkaita."),
            GrammarExample(
                "Ymmärrän perustelun, mutta näillä tiedoilla en vielä kannata muutosta."
            ),
        ],
        related=["fi-potential-b2", "fi-referative-past-b2"],
    ),
    GrammarTopic(
        "fi-argument-links-b2",
        "Toisaalta, silti ja näin ollen",
        "B2",
        "Perustelu",
        "Rakennat perusteluketjun ja punnitset eri tavoitteita.",
        "Toisaalta tuo rinnalle toisen näkökulman. Silti ilmaisee odotuksenvastaisen "
        "jatkon, kun taas näin ollen esittää päätelmän. Sen sijaan vaihtaa "
        "vaihtoehtoa tai vertailun kohdetta. Sidossana ei tee päätelmästä pätevää: "
        "lukijan on nähtävä, miten peruste liittyy johtopäätökseen. Myönnytys "
        "voi tunnustaa todellisen haitan muuttamatta lopullista kantaa.",
        rules=[
            "Valitse sidossana ajatusten todellisen suhteen mukaan.",
            "Erota oma johtopäätös lähteestä lainatusta tiedosta.",
        ],
        examples=[
            GrammarExample("Reitti lyhenee, mutta toisaalta vaihto vaikeutuu."),
            GrammarExample("Tila ei ole esteetön. Näin ollen tarvitsemme toisen kokouspaikan."),
        ],
        related=["fi-concession-b1", "fi-hedging-b2"],
    ),
    GrammarTopic(
        "fi-quantifier-scope-b2",
        "Kaikki eivät ja kukaan ei",
        "B2",
        "Kiellon vaikutusala",
        "Erotat osittaisen kiellon koko joukkoa koskevasta kiellosta.",
        "Kaikki eivät hyväksyneet ehdotusta kertoo, ettei hyväksyntä ollut "
        "yksimielinen; lause ei yksin anna hyväksyjien määrää. Kukaan ei "
        "hyväksynyt kertoo, että hyväksyjiä oli nolla. Ei aina sallii tilanteita, "
        "joissa asia toteutuu, eikä tarkoita samaa kuin ei koskaan. Monitulkintainen "
        "määräilmaus kannattaa avata lukumääriksi, jos päätös riippuu siitä.",
        rules=[
            "Älä päättele sanasta kaikki eivät, että enemmistö vastusti.",
            "Tarkenna tarvittaessa: kolme kannatti, kaksi vastusti ja yksi pidättyi.",
        ],
        examples=[
            GrammarExample("Kaikki eivät vastanneet kyselyyn, joten tulos ei kata koko ryhmää."),
            GrammarExample("Kukaan ei vastustanut, mutta kaksi ei ottanut kantaa."),
        ],
        related=["fi-information-structure-b2"],
    ),
    GrammarTopic(
        "fi-repair-b2",
        "Tarkoitatko siis...? – Tulkinnan korjaaminen",
        "B2",
        "Vuorovaikutus",
        "Selvität merkityksen ja säilytät keskusteluyhteyden.",
        "Tarkoitatko, että esittää tulkinnan tarkistettavaksi eikä vielä "
        "vahvista sitä todeksi. Toisin sanoen voi tiivistää, mutta tiivistelmässä "
        "on säilytettävä ehdot ja varmuus. Huumori tai ironia voi kääntää "
        "kirjaimellisen merkityksen; jos tarkoitus on epäselvä, pyydä tarkennusta "
        "ilman syytöstä. Korjaa ensin merkitys ja jatka sitten yhteistä tehtävää.",
        rules=[
            "Erottele en ymmärtänyt ja olen eri mieltä.",
            "Älä poista sanoja ehkä, vain tai jos toisen viestiä tiivistäessäsi.",
        ],
        examples=[
            GrammarExample("Tarkoitatko, että voimme aloittaa, jos saamme luvan tänään?"),
            GrammarExample("Taisit sanoa sen leikillä. Palataan silti hetkeksi aikatauluun."),
        ],
        related=["fi-indirect-question-b1", "fi-hedging-b2", "fi-register-b2"],
    ),
]
