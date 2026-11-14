"""Finnish C1 grammar in evidence, negotiation, narration and mediation."""

from app.data._types import GrammarExample, GrammarTopic

C1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "fi-source-marking-c1",
        "Mukaan, kuulemma ja muka",
        "C1",
        "Tiedon lähde",
        "Ilmaise, keneltä tieto on peräisin ja miten itse suhtaudut siihen.",
        "Mukaan liittää tiedon nimettyyn lähteeseen. Kuulemma esittää tiedon muualta kuultuna "
        "nimeämättä välttämättä lähdettä. Muka voi etäännyttää puhujan väitteestä ja ilmaista "
        "epäilyä; se ei ole kuulemma-sanan neutraali vastine. Sävy ratkaistaan asiayhteydestä.",
        rules=[
            "Älä muuta lähteen väitettä omaksi havainnoksesi tiivistäessäsi.",
            "Nimeä lähde, jos vastaanottajan on voitava arvioida tiedon luotettavuutta.",
        ],
        examples=[
            GrammarExample("Huoltajan mukaan ovikoodi vaihtuu huomenna."),
            GrammarExample("Ovikoodi on kuulemma jo vaihdettu; en ole vielä kokeillut sitä."),
            GrammarExample("Koodi muka toimii, vaikka kukaan meistä ei pääse sisään."),
        ],
        related=["fi-inference-c1"],
    ),
    GrammarTopic(
        "fi-inference-c1",
        "Taitaa, lienee ja näyttää siltä",
        "C1",
        "Päätelmät",
        "Erota päätelmä varmennetusta tiedosta.",
        "Taitaa ilmaisee usein puhujan arviota: juna taitaa olla myöhässä. Lienee on olla-verbin "
        "potentiaalimuoto ja tavallinen etenkin harkitussa kirjoitetussa arviossa. Näyttää siltä, "
        "että sitoo arvion havaittuihin merkkeihin. Näillä ilmauksilla ei ole kiinteitä "
        "todennäköisyysprosentteja, eikä niitä voi järjestää joka tilanteessa samalle asteikolle.",
        rules=[
            "Ilmoita tarvittaessa havainto, johon päätelmä perustuu.",
            "Taitaa voi toisessa rakenteessa merkitä osaamista: hän taitaa monta kieltä.",
        ],
        examples=[
            GrammarExample("Valot ovat sammuneet, joten kokous taitaa olla ohi."),
            GrammarExample("Arvio lienee liian optimistinen, sillä talven kuluja ei ole laskettu."),
        ],
        related=["fi-source-marking-c1"],
    ),
    GrammarTopic(
        "fi-negation-scope-c1",
        "Kaikki eivät, ei välttämättä ja tuskin",
        "C1",
        "Kiellon vaikutusala",
        "Säilytä kielteisen väitteen tarkka ulottuvuus.",
        "Kaikki eivät vastanneet sulkee pois kaikkien vastaamisen mutta ei kerro vastaajien "
        "määrää. Kukaan ei vastannut sulkee pois jokaisen vastaajan. Ei välttämättä kiistää "
        "seurauksen varmuuden, ei sen mahdollisuutta. Tuskin esittää asian epätodennäköisenä "
        "ja voi muussa yhteydessä tarkoittaa myös niukasti: tuskin kuultava ääni.",
        rules=[
            "Älä päättele enemmistön kantaa ilmauksesta kaikki eivät.",
            "Täsmennä kiellon kohde, jos sanajärjestys tai painotus sallii useita tulkintoja.",
        ],
        examples=[
            GrammarExample("Halvempi vuokra ei välttämättä pienennä kokonaiskuluja."),
            GrammarExample("Kaikki eivät vastustaneet esitystä; osa ei ottanut kantaa."),
        ],
    ),
    GrammarTopic(
        "fi-condition-boundaries-c1",
        "Kunhan, ellei ja vain jos",
        "C1",
        "Ehdot",
        "Muotoile sopimuksen edellytys ja poikkeus.",
        "Kunhan voi ilmaista riittävänä pidetyn ehdon: voimme aloittaa, kunhan lupa saadaan. "
        "Se voi myös viitata odotettuun tulevaan hetkeen, joten tilanne on huomioitava. "
        "Ellei sisältää kiellon ja esittää poikkeuksen. Vain jos nimeää välttämättömän ehdon "
        "mutta ei yksin takaa, että sen täyttyminen riittää.",
        rules=[
            "Ellei lupa tule vastaa tässä ilmausta jos lupaa ei tule.",
            "Erota sopimuksessa välttämätön edellytys lupauksesta toteuttaa työ.",
        ],
        examples=[
            GrammarExample("Pidämme tilaisuuden ulkona, ellei sääennuste muutu."),
            GrammarExample("Voin hyväksyä hinnan vain, jos kuljetus sisältyy siihen."),
        ],
    ),
    GrammarTopic(
        "fi-concession-c1",
        "Vaikka, vaikka … -kin ja siitä huolimatta",
        "C1",
        "Myönnytys",
        "Hyväksy vastanäkökohta muuttamatta omaa johtopäätöstäsi.",
        "Vaikka-lause voi esittää myönnetyn tosiasian tai kuvitellun tilanteen. Vaikka hinta on "
        "korkea esittää hinnan korkeana; vaikka hinta nousisi jättää nousun oletukseksi. "
        "Vaikka tarjous onkin halpa korostaa myönnytystä. Muoto ei yksin ratkaise kaikkea, "
        "vaan aikamuoto, modus ja asiayhteys ohjaavat tulkintaa.",
        rules=[
            "Myönnä vain se väite, jonka todella hyväksyt.",
            "Säilytä reformulaatiossa ero toteutuneen ja kuvitellun tilanteen välillä.",
        ],
        examples=[
            GrammarExample("Vaikka ehdotus onkin edullinen, sen aikataulu ei sovi meille."),
            GrammarExample("Vaikka saisimme lisärahaa, emme ehtisi avata tilaa toukokuussa."),
        ],
    ),
    GrammarTopic(
        "fi-conditional-commitment-c1",
        "Voisin, suostuisin ja lupaan",
        "C1",
        "Sitoumus ja kohteliaisuus",
        "Erota tunnusteleva tarjous sovitusta tehtävästä.",
        "Konditionaali voi ilmaista kohteliaisuutta, ehdollisuutta tai alustavaa valmiutta. "
        "Voisin selvittää asian on tilanteesta riippuen tarjous, ei pelkkä kuvitteellinen kyky. "
        "Se ei silti automaattisesti vastaa yksiselitteistä lupausta selvitän asian. "
        "Neuvottelussa lopullinen sitoumus varmistetaan yhteisellä tarkennuksella.",
        rules=[
            "Kysy, saako tarjouksen kirjata sovituksi tehtäväksi.",
            "Liitä tarjoukseen todelliset aikarajat sen sijaan, että peittäisit ne kohteliaisuuteen.",
        ],
        examples=[
            GrammarExample("Voisin ottaa iltavuoron, jos joku vaihtaisi kanssani perjantain."),
            GrammarExample("Sovitaan näin: hoidan iltavuoron ja sinä hoidat perjantain."),
        ],
        related=["fi-condition-boundaries-c1"],
    ),
    GrammarTopic(
        "fi-nominalisation-c1",
        "Tekeminen, esitys ja päätös",
        "C1",
        "Tiiviin tekstin avaaminen",
        "Muuta substantiivirakenne toiminnaksi säilyttäen sen asema.",
        "Ilmaus hallituksen esitys maksun alentamisesta sisältää ehdotuksen, ei toteutunutta "
        "alennusta. Hallitus esittää, että maksua alennetaan säilyttää tämän eron. "
        "Tekemistä ilmaiseva substantiivi voi jättää tekijän tai ajankohdan avoimeksi; niitä "
        "ei saa keksiä, kun rakennetta avataan.",
        rules=[
            "Tarkista erikseen ehdottaja, päättäjä ja toteuttaja.",
            "Älä muuta suunniteltua toimenpidettä suoritetuksi teoksi.",
        ],
        examples=[
            GrammarExample(
                "Päätös tilan sulkemisesta siirrettiin: tilaa ei siis vielä päätetty sulkea."
            ),
            GrammarExample("Hakemuksen käsittely odottaa liitettä; hakemusta ei ole hylätty."),
        ],
    ),
    GrammarTopic(
        "fi-participle-agents-c1",
        "Hyväksynyt, hyväksytty ja hyväksymä",
        "C1",
        "Osallistujat",
        "Tunnista tiiviin määritteen tekijä ja kohde.",
        "Hakemuksen hyväksynyt virkailija nimeää hyväksyjän. Virkailijan hyväksymä hakemus "
        "nimeää kohteen ja kertoo hyväksyjän genetiivillä. Hyväksytty hakemus jättää tekijän "
        "nimeämättä. Rakenne avataan relatiivilauseeksi sen mukaan, kumpi osallistuja on "
        "pääsanana; pelkkä tuttujen sanojen säilyttäminen ei riitä.",
        rules=[
            "Erota hakemus, jonka virkailija hyväksyi, virkailijasta, joka hyväksyi hakemuksen.",
            "Säilytä mahdolliset rajaukset kuten alustavasti ja ehdollisesti.",
        ],
        examples=[
            GrammarExample("Asukkaiden ehdottama ratkaisu odottaa vielä teknistä arviota."),
            GrammarExample("Ratkaisua ehdottaneet asukkaat kutsuttiin keskusteluun."),
        ],
    ),
    GrammarTopic(
        "fi-impersonal-agency-c1",
        "Nollapersoona, passiivi ja näkyvä vastuu",
        "C1",
        "Toimijuus",
        "Valitse yleistävä tai toimijan nimeävä esitys tilanteen mukaan.",
        "Jos saapuu myöhässä, joutuu odottamaan kuvaa avointa kokijan paikkaa ilman ilmipantua "
        "subjektia. Hakemukset käsitellään huomenna nostaa käsittelyn esiin mutta ei nimeä "
        "käsittelijöitä. Kumpikaan ei ole sinänsä epätarkka: ongelma syntyy, jos kuulijan "
        "pitää tietää, kuka vastaa työstä. Puheessa me käsitellään on yleinen rakenne; "
        "muodollisessa yleiskielessä käytetään tavallisesti me käsittelemme.",
        rules=[
            "Nimeä vastuuhenkilö tehtävänjaossa, jos hän on tiedossa.",
            "Älä tulkitse yleistävää nollapersoonaa automaattisesti puhujan omaksi kokemukseksi.",
        ],
        examples=[
            GrammarExample("Tässä työssä joutuu välillä tekemään päätöksiä puutteellisin tiedoin."),
            GrammarExample("Tarjoukset pyydetään huomenna. Sari vastaa yhteydenotoista."),
        ],
    ),
    GrammarTopic(
        "fi-narrative-time-c1",
        "Takauma ja kerronnan preesens",
        "C1",
        "Kertominen",
        "Pidä aikajana seurattavana näkökulman vaihtuessa.",
        "Imperfekti kantaa usein menneen tapahtuman kertomusta. Pluskvamperfekti sijoittaa "
        "tapahtuman menneeseen viitehetkeen nähden aiemmaksi. Kerronnan preesens voi tuoda "
        "kohtauksen lähelle: ja sitten ovi aukeaa. Vaihdos on kerronnallinen keino, ei "
        "automaattinen aikamuotovirhe, mutta kuulijan on tunnistettava sen tehtävä.",
        rules=[
            "Merkitse paluu pääjuoneen tarvittaessa ajanilmauksella.",
            "Säilytä tapahtumien järjestys, kun kerrot kokemuksen uudelleen.",
        ],
        examples=[
            GrammarExample("Saavuin asemalle myöhässä. Olin lähtenyt vahingossa väärään suuntaan."),
            GrammarExample("Seisoin ovella. Sitten ovi aukeaa ja vanha ystäväni astuu ulos!"),
        ],
    ),
    GrammarTopic(
        "fi-information-order-c1",
        "Teeman vaihtaminen ja vastakohtapainotus",
        "C1",
        "Informaatiorakenne",
        "Ohjaa huomio siihen, mikä keskustelussa todella muuttuu.",
        "Suomen sanajärjestys sallii monenlaisia painotuksia, mutta järjestykset eivät ole "
        "keskenään merkityksettömiä. Tämän asian Liisa selvittää nostaa asian puheenaiheeksi; "
        "Liisa tämän asian selvittää voi korostaa tekijää etenkin vastakohtaisessa tilanteessa. "
        "Sijat säilyttävät osallistujien tehtävät, ja puheessa myös painotus ohjaa tulkintaa.",
        rules=[
            "Tee kirjoituksessa tarvittaessa vastakohta näkyväksi ilmauksella ei vaan.",
            "Älä selitä jokaista poikkeavaa järjestystä yhdellä jäykällä sääntömallilla.",
        ],
        examples=[
            GrammarExample("Aikataulua haluan muuttaa, en työn sisältöä."),
            GrammarExample("Liisa kutsui Pekan, ei Pekka Liisaa."),
        ],
    ),
    GrammarTopic(
        "fi-relative-reference-c1",
        "Joka, mikä ja viittauksen kohde",
        "C1",
        "Tekstin sidokset",
        "Erota nimettyyn asiaan viittaaminen koko väitteen kommentoinnista.",
        "Joka viittaa tavallisesti edeltävään substantiivilausekkeeseen. Mikä voi viitata "
        "kokonaiseen edeltävään lauseeseen: juna peruttiin, mikä muutti suunnitelmamme. "
        "Mikä-pronominilla on myös muita käyttöjä, kuten kaikki, mikä auttaa. Jos mahdollisia "
        "viittauskohteita on useita, toista asian nimi.",
        rules=[
            "Koko tapahtumaa kommentoiva relatiivilause ei kuvaile vain lähintä substantiivia.",
            "Älä muuta ehdotusta päätökseksi nimeämällä viittauskohde väärin.",
        ],
        examples=[
            GrammarExample("Saimme ehdotuksen, joka koski pihan valaistusta."),
            GrammarExample("Ehdotus vedettiin pois, mikä yllätti kokouksen osallistujat."),
        ],
    ),
    GrammarTopic(
        "fi-additive-focus-c1",
        "-kin, -kaan ja myös",
        "C1",
        "Fokusointi",
        "Näytä, mihin lisäys tai odotuksen vastaisuus kohdistuu.",
        "Liite -kin voi merkitä lisäystä: Laurakin tuli. Se voi myös osoittaa odotuksen "
        "täyttymistä tai muuttumista: hän tulikin jo. Kielteisessä lisäyksessä käytetään "
        "usein -kaan/-kään-liitettä: Laurakaan ei tullut. Liitteen paikka, lauseen kielteisyys "
        "ja asiayhteys vaikuttavat merkitykseen; kyse ei ole mekaanisesta sananvaihdosta.",
        rules=[
            "Erota henkilöön kohdistuva lisäys koko tapahtumaa kommentoivasta liitteestä.",
            "Tarvittaessa avaa sävy kokonaiseksi lauseeksi.",
        ],
        examples=[
            GrammarExample("Tämäkin laskelma sisältää kuljetuksen; myös aiemmassa se oli mukana."),
            GrammarExample("Hän ei tullutkaan: olimme odottaneet häntä paikalle."),
        ],
    ),
    GrammarTopic(
        "fi-causal-inference-c1",
        "Koska, kun kerran ja päätelmän peruste",
        "C1",
        "Perustelut",
        "Erota tapahtuman aiheuttaja tiedon perusteesta.",
        "Koska voi perustella tapahtumaa tai puhujan päätelmää. Piha kastui, koska satoi "
        "esittää sateen syyksi. Ulkona taitaa sataa, koska tulijoiden takit ovat märkiä "
        "antaa päätelmälle todisteen, ei sateelle syytä. Kun kerran voi vedota asiayhteydessä "
        "hyväksyttynä pidettyyn lähtökohtaan, jota toinen ei välttämättä hyväksy.",
        rules=[
            "Kysy, selittääkö sivulause tapahtuman vai oikeuttaako se puhujan arvion.",
            "Tarkista yhteiseksi esitetty lähtökohta ennen siihen perustuvaa päätöstä.",
        ],
        examples=[
            GrammarExample("Koska varausvahvistus puuttuu, en vielä uskalla luvata tilaa."),
            GrammarExample(
                "Kun kerran tarvitsemme lisätietoa, siirretään päätös seuraavaan kokoukseen."
            ),
        ],
    ),
    GrammarTopic(
        "fi-discourse-contrast-c1",
        "Silti, sen sijaan ja toisaalta",
        "C1",
        "Argumentin kulku",
        "Rakenna vastakohta, korvaava vaihtoehto tai uusi näkökulma.",
        "Silti yhdistää päätelmän sitä vastaan puhuvaan seikkaan. Sen sijaan esittää "
        "vastakkaisen tai korvaavan vaihtoehdon. Toisaalta tuo rinnalle toisen näkökulman "
        "ilman, että ensimmäinen välttämättä hylätään. Näiden vaihtaminen voi muuttaa "
        "lukijan käsityksen koko perustelusta.",
        rules=[
            "Nimeä vaihtoehdot, jos sen sijaan jää ilman selvää vertailukohtaa.",
            "Kerro lopuksi oma johtopäätöksesi, jos punnitset useita näkökulmia.",
        ],
        examples=[
            GrammarExample("Tilaan pääsee portaita. Silti se ei ole kaikkien saavutettavissa."),
            GrammarExample("Emme osta laitetta. Sen sijaan vuokraamme sen kuukaudeksi."),
        ],
    ),
    GrammarTopic(
        "fi-han-shared-ground-c1",
        "-han ja yhteiseksi esitetty tieto",
        "C1",
        "Vuorovaikutus",
        "Tunnista muistuttamisen, selittämisen ja painostamisen sävyjä.",
        "Liite -han/-hän voi esittää tiedon tunnettuna tai muistuttaa siitä: mehän sovimme näin. "
        "Se voi myös pehmentää selitystä tai ilmaista oivalluksen. Yhteiseksi esitetty tieto "
        "ei silti ole välttämättä oikeasti yhteistä. Sävy syntyy liitteen lisäksi tilanteesta, "
        "painotuksesta ja osallistujien suhteesta.",
        rules=[
            "Älä käsittele liitettä aina ystävällisenä tai aina moittivana.",
            "Kiistä tarvittaessa oletettu yhteisymmärrys täsmällisesti.",
        ],
        examples=[
            GrammarExample("Sinähän tunnet reitin; osaisitko neuvoa meitä?"),
            GrammarExample("Mehän hyväksyimme hinnan. — Hyväksyimme vasta hinta-arvion."),
        ],
    ),
    GrammarTopic(
        "fi-pa-reactions-c1",
        "-pa, -pä ja reaktion tulkinta",
        "C1",
        "Sävy ja huumori",
        "Tulkitse reaktiota suhteessa tilanteeseen ja äänenpainoon.",
        "Onpa hiljaista voi olla vilpitön havainto, yllätys tai ironinen kommentti meluun. "
        "Liite -pa/-pä vahvistaa tai sävyttää reaktiota, mutta ei yksin tee siitä ironista. "
        "Käskymuodossa katsopa liite voi ohjata huomiota; sen kohteliaisuus riippuu tilanteesta. "
        "Itseen kohdistuva leikillinen arvio voi tarjota toiselle mahdollisuuden lievittää harmia.",
        rules=[
            "Etsi ironiselle tulkinnalle tukea tilanteesta, älä vain liitteestä.",
            "Tarkista tarkoitus, jos myönteiset sanat ja tilanne ovat ristiriidassa.",
        ],
        examples=[
            GrammarExample("Unohdin sateenvarjon juuri tänään. Olenpa minä kaukonäköinen."),
            GrammarExample("Katsopa tätä kohtaa: tässä laskussa on sama maksu kahdesti."),
        ],
    ),
    GrammarTopic(
        "fi-conversation-repair-c1",
        "Siis, tai oikeastaan ja tarkoitatko",
        "C1",
        "Keskustelun korjaaminen",
        "Korjaa ilmaus ja varmista tulkinta keskeyttämättä yhteistyötä.",
        "Siis voi ilmaista johtopäätöksen tai aloittaa täsmennyksen. Tai oikeastaan "
        "korjaa puhujan omaa sanavalintaa. Tarkoitatko, että tarjoaa toiselle tarkistettavan "
        "tulkinnan, ei valmista kuvausta hänen kannastaan. Korjauksessa on hyödyllistä nimetä, "
        "mikä aiemmasta ilmauksesta korvautuu ja mikä jää voimaan.",
        rules=[
            "Pidä toisen kannasta tekemäsi tulkinta kysymyksenä, kun et ole varma.",
            "Erota sanan korjaaminen koko ehdotuksen peruuttamisesta.",
        ],
        examples=[
            GrammarExample("Tarvitsen vastauksen huomenna, tai oikeastaan alustava arvio riittää."),
            GrammarExample("Tarkoitatko, että voimme varata tilan mutta emme vielä maksaa sitä?"),
        ],
    ),
    GrammarTopic(
        "fi-reported-commitments-c1",
        "Lupasi, ehdotti ja sanoi voivansa",
        "C1",
        "Referointi",
        "Välitä puheenvuoron sitovuus täsmällisesti.",
        "Lupasi tehdä esittää sitoumuksen. Ehdotti, että tehtäisiin esittää harkittavan "
        "toimintatavan. Sanoi voivansa tehdä voi välittää kykyä tai tarjousta, jonka "
        "lopullinen asema selviää asiayhteydestä. Suomen epäsuora esitys ei vaadi "
        "mekaanista aikamuotojen siirtoa; ajallinen suhde on säilytettävä merkityksen avulla.",
        rules=[
            "Säilytä alkuperäinen ehto myös lyhyessä muistiossa.",
            "Älä muuta valmiutta tehtävän vastaanottamiseksi ilman perustetta.",
        ],
        examples=[
            GrammarExample("Eeva sanoi voivansa tulla, jos työvuoro vaihtuisi."),
            GrammarExample("Eeva lupasi ilmoittaa päätöksensä huomenna, ei vielä osallistua."),
        ],
        related=["fi-source-marking-c1", "fi-conditional-commitment-c1"],
    ),
    GrammarTopic(
        "fi-register-recasting-c1",
        "Puheenvuorosta asiatekstiksi",
        "C1",
        "Rekisteri",
        "Vaihda esitystapaa säilyttäen asenne ja rajaukset.",
        "Puheen toistot, katkokset ja pronominit palvelevat vuorovaikutusta. Asiatekstissä "
        "niitä voi tiivistää, mutta ehkä, kai tai vain voivat rajata itse väitettä. "
        "Puhekielen muodot vaihtelevat alueittain ja tilanteittain; yksi puhetapa ei "
        "edusta kaikkea Suomessa puhuttua suomea. Yleiskielistäminen ei oikeuta lisäämään varmuutta.",
        rules=[
            "Erottele esitystavan tiivistäminen sisällöllisestä muutoksesta.",
            "Säilytä puhujan epävarmuus silloinkin, kun poistat epäröinnin toistoa.",
        ],
        examples=[
            GrammarExample(
                "Voisin ehkä vilkaista sitä. → Puhuja tarjoutui alustavasti katsomaan asiaa."
            ),
            GrammarExample("Se hinta, siitä pitää vielä puhua. → Hinnasta pitää vielä puhua."),
        ],
        related=["fi-nominalisation-c1"],
    ),
    GrammarTopic(
        "fi-summary-cohesion-c1",
        "Tämä ehdotus, kyseinen arvio ja avoin kysymys",
        "C1",
        "Yhteenveto",
        "Nimeä edeltävä sisältö muuttamatta sen asemaa.",
        "Tämä voi viitata kokonaiseen ajatukseen, mutta usean ehdotuksen jälkeen viittaus voi "
        "jäädä epäselväksi. Tarkempi ilmaus kuten tämä aikatauluehdotus auttaa lukijaa. "
        "Nimeäminen myös tulkitsee: huoli, vastalause ja päätös eivät ole sama asia. "
        "Hyvä yhteenveto erottaa yhteisesti sovitun, yhden osapuolen esittämän ja avoimeksi jääneen.",
        rules=[
            "Toista tarpeellinen nimi, vaikka tekstiin tulisi hieman toistoa.",
            "Käytä päätös-sanaa vasta asiasta, josta todella on päätetty.",
        ],
        examples=[
            GrammarExample("Asukkaat pyysivät lisäaikaa. Tämä pyyntö käsitellään torstaina."),
            GrammarExample("Hinnasta sovittiin. Toimituspäivä jäi sen sijaan avoimeksi."),
        ],
        related=["fi-relative-reference-c1", "fi-reported-commitments-c1"],
    ),
]
