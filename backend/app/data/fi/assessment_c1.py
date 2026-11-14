"""Finnish C1 placement items with balanced answer positions by skill."""

from app.data._types import AssessmentQuestion

C1_QUESTIONS: list[AssessmentQuestion] = [
    AssessmentQuestion(
        "fi-g-c1-001",
        "grammar",
        "C1",
        "Sari lukee taloyhtiön viestiketjua ja sanoo: "
        "«Hissi on kuulemma käytössä jo iltapäivällä.» Mitä hänen ilmauksestaan voi päätellä?",
        [
            "Sari välittää muualta saamansa tiedon siitä, milloin hissi on käytössä.",
            "Sari ilmaisee epäilevänsä väitettä hissin iltapäiväisestä käyttöönotosta.",
            "Sari kertoo omasta havainnostaan hissin onnistuneen koekäytön aikana.",
            "Sari ottaa vastuun siitä, että hissi saadaan iltapäiväksi toimintakuntoon.",
        ],
        "Sari välittää muualta saamansa tiedon siitä, milloin hissi on käytössä.",
        "fi-source-marking-c1",
    ),
    AssessmentQuestion(
        "fi-g-c1-002",
        "grammar",
        "C1",
        "Viestissä lukee: «Tilaisuus voidaan järjestää tässä salissa vain, jos poistumisreitti "
        "saadaan esteettömäksi.» Reitti on nyt esteetön. Mikä seuraava toteamus on perusteltu?",
        [
            "Salin käyttö on nyt vahvistettu, joten muut järjestelyt voidaan päättää.",
            "Salin käytön muut ehdot on jo tarkistettu, koska viesti mainitsi vain poistumisreitin.",
            "Salin käytöstä voidaan sopia, sillä poistumisreitti oli viestin mukaan ainoa ehto.",
            "Mainittu este on poistettu, mutta viesti ei vahvista kaikkien ehtojen täyttymistä.",
        ],
        "Mainittu este on poistettu, mutta viesti ei vahvista kaikkien ehtojen täyttymistä.",
        "fi-condition-boundaries-c1",
    ),
    AssessmentQuestion(
        "fi-g-c1-003",
        "grammar",
        "C1",
        "Työlistalla lukee: «Asukkaiden ehdottaman kulkureitin tarkastanut suunnittelija "
        "lähettää lausunnon huomenna.» Kenen puoleen käännyt, kun haluat kysyä lausunnon aikataulusta?",
        [
            "Asukkaiden puoleen, koska he tarkastivat suunnittelijan ehdottaman reitin.",
            "Suunnittelijan puoleen, koska hän ehdotti asukkaiden jo hyväksymää reittiä.",
            "Suunnittelijan puoleen, koska hän tarkasti asukkaiden esittämän reitin.",
            "Asukkaiden puoleen, koska he hyväksyivät suunnittelijan valmiin lausunnon.",
        ],
        "Suunnittelijan puoleen, koska hän tarkasti asukkaiden esittämän reitin.",
        "fi-participle-agents-c1",
    ),
    AssessmentQuestion(
        "fi-g-c1-004",
        "grammar",
        "C1",
        "Muistiossa todetaan: «Lisärahoitus ei välttämättä nopeuta valmistumista.» "
        "Mikä kommentti säilyttää muistion väitteen vahvuuden?",
        [
            "Lisärahoituksen vaikutusta pidetään niin vähäisenä, ettei sitä kannata selvittää.",
            "Aikatauluhyöty on mahdollinen, mutta sitä ei voi pitää lisärahoituksen varmana seurauksena.",
            "Lisärahoituksen arvioidaan hidastavan työtä, vaikka kustannukset samalla kasvavat.",
            "Aikatauluhyötyä odotetaan, mutta lisärahoituksen myöntämisestä ei ole vielä varmuutta.",
        ],
        "Aikatauluhyöty on mahdollinen, mutta sitä ei voi pitää lisärahoituksen varmana seurauksena.",
        "fi-negation-scope-c1",
    ),
    AssessmentQuestion(
        "fi-g-c1-005",
        "grammar",
        "C1",
        "Aino odottaa tapaamista ja saa viestin: «Mikko ei tulekaan tänään.» "
        "Mikä tulkinta sopii liitteen tehtävään tässä viestissä?",
        [
            "Viestissä täsmennetään, että Mikko saapuu myöhemmin samana päivänä.",
            "Viestissä lisätään Mikko muiden ennalta tiedettyjen poissaolijoiden joukkoon.",
            "Viestissä korostetaan, että Mikko on jättänyt tulematta myös aiemmin.",
            "Viestissä korjataan aiempi odotus siitä, että Mikko olisi tulossa.",
        ],
        "Viestissä korjataan aiempi odotus siitä, että Mikko olisi tulossa.",
        "fi-additive-focus-c1",
    ),
    AssessmentQuestion(
        "fi-g-c1-006",
        "grammar",
        "C1",
        "Kollega sanoo: «Mehän päätimme jo sulkea oven kuudelta.» Viime kokouksessa "
        "sovittiin vasta käyttäjäkyselystä. Haluat oikaista tilanteen ja jatkaa valmistelua. Mitä vastaat?",
        [
            "Päätimme vasta selvittää käyttäjien tarpeet. Palataan sulkemisaikaan tulosten jälkeen.",
            "Pidetään kuusi lähtökohtana. Käyttäjiltä voidaan kysyä myöhemmin, sopiko muutos heille.",
            "Tiedotetaan sulkemisesta ensin. Käyttäjäkysely auttaa sitten arvioimaan päätöksen vaikutusta.",
            "Kuusi sopii minulle edelleen. Päätetään seuraavaksi, minä päivänä uusi käytäntö alkaa.",
        ],
        "Päätimme vasta selvittää käyttäjien tarpeet. Palataan sulkemisaikaan tulosten jälkeen.",
        "fi-han-shared-ground-c1",
    ),
    AssessmentQuestion(
        "fi-g-c1-007",
        "grammar",
        "C1",
        "Eeva sanoo: «Voisin tarkistaa luvut ensi viikolla, jos saan alkuperäisen aineiston.» "
        "Mikä merkintä sopii alustavaan muistioon?",
        [
            "Eeva tarkistaa aineiston tällä viikolla ja lähettää korjatut luvut ensi viikolla.",
            "Eeva lupasi vahvistaa luvut ensi viikolla ja pyysi lisäksi alkuperäistä aineistoa.",
            "Eeva tarjoutui tarkistamaan luvut ensi viikolla sillä ehdolla, että saa aineiston.",
            "Eeva pyysi tarkistamaan luvut ensi viikolla ennen alkuperäisen aineiston lähettämistä.",
        ],
        "Eeva tarjoutui tarkistamaan luvut ensi viikolla sillä ehdolla, että saa aineiston.",
        "fi-conditional-commitment-c1",
    ),
    AssessmentQuestion(
        "fi-g-c1-008",
        "grammar",
        "C1",
        "Raportissa lukee: «Työryhmä luopui viikonloppua koskevasta ehdotuksesta, mikä "
        "rauhoitti keskustelua.» Mikä asia esitetään keskustelua rauhoittaneena?",
        [
            "Viikonloppua koskevan ehdotuksen sisältö ennen työryhmän uutta ratkaisua.",
            "Työryhmän ratkaisu jättää viikonloppua koskeva ehdotus pois.",
            "Työryhmän kokoonpanon muuttuminen viikonlopun keskustelun jälkeen.",
            "Viikonlopulle sovittu keskustelu työryhmän ehdotuksen yksityiskohdista.",
        ],
        "Työryhmän ratkaisu jättää viikonloppua koskeva ehdotus pois.",
        "fi-relative-reference-c1",
    ),
    AssessmentQuestion(
        "fi-v-c1-001",
        "vocabulary",
        "C1",
        "Toimittaja sanoo: «Hinnassa ei ole liikkumavaraa, mutta eräpäivästä voimme sopia.» "
        "Mikä ehdotus jatkaa neuvottelua hänen mainitsemallaan tavalla?",
        [
            "Pidetään eräpäivä ja vähennetään laskun kokonaissummaa viisi prosenttia.",
            "Pidetään molemmat ehdot ja lisätään toimitukseen uusia tuotteita samaan hintaan.",
            "Pidetään kokonaishinta ja siirretään maksua seuraavan kuukauden alkuun.",
            "Pidetään maksuaikataulu ja jätetään kuljetuksen hinta pois loppulaskusta.",
        ],
        "Pidetään kokonaishinta ja siirretään maksua seuraavan kuukauden alkuun.",
    ),
    AssessmentQuestion(
        "fi-v-c1-002",
        "vocabulary",
        "C1",
        "Sihteeri kirjoittaa: «Toimeksiantoni koskee vaihtoehtojen valmistelua.» "
        "Mikä pyyntö pysyy tämän rajauksen sisällä?",
        [
            "Kokoaisitko vertailun hinnoista ja toimitusajoista seuraavaa kokousta varten?",
            "Allekirjoittaisitko vertailussa edullisimmaksi osoittautuvan sopimuksen puolestamme?",
            "Ilmoittaisitko tarjoajille, mikä vaihtoehto on lopullisesti valittu kokouksessa?",
            "Vahvistaisitko toimittajalle, että tilaus voidaan aloittaa heti vertailun valmistuttua?",
        ],
        "Kokoaisitko vertailun hinnoista ja toimitusajoista seuraavaa kokousta varten?",
    ),
    AssessmentQuestion(
        "fi-v-c1-003",
        "vocabulary",
        "C1",
        "Ystävä unohtaa retkikartan kotiin ja sanoo hymyillen: «Suunnistamisen mestari "
        "taas vauhdissa.» Haluat vastata itseironiaan ystävällisesti ja ratkaista tilanteen. Mitä sanot?",
        [
            "Hyvä, että tunnet maaston niin hyvin. Jätetään varareitin tarkistaminen myöhemmäksi.",
            "Et taida suhtautua reittiin kovin vakavasti. Ehkä jonkun muun pitäisi suunnitella se.",
            "Karttaa ei siis ollut tarkoituskaan ottaa mukaan. Mennään sinun alkuperäisen suunnitelmasi mukaan.",
            "Mestarin tukijoukot auttavat. Minulla on reitti puhelimessa, katsotaan sitä yhdessä.",
        ],
        "Mestarin tukijoukot auttavat. Minulla on reitti puhelimessa, katsotaan sitä yhdessä.",
    ),
    AssessmentQuestion(
        "fi-v-c1-004",
        "vocabulary",
        "C1",
        "Kokouksessa vertaillaan kahta ehdotusta iltavuorojen jakamiseksi. Vetäjä toteaa: "
        "«Etsitään ensin ehdotusten yhteinen nimittäjä.» Mikä vastaus vie vertailua tähän suuntaan?",
        [
            "Kummankin ehdotuksen hinta on erilainen, joten valitaan ensin laskutapa.",
            "Molemmissa halutaan turvata iltakäyttö; erimielisyys koskee vuorojen jakamista.",
            "Ensimmäinen ehdotus on lyhyempi, joten käytetään sen rakennetta tiedotteessa.",
            "Toisen ehdotuksen vuorot sopivat minulle paremmin, joten kannatan sitä sellaisenaan.",
        ],
        "Molemmissa halutaan turvata iltakäyttö; erimielisyys koskee vuorojen jakamista.",
    ),
    AssessmentQuestion(
        "fi-r-c1-001",
        "reading",
        "C1",
        "Kirjasto kokeili myöhäisempää sulkemista tiistaisin. Kävijöitä tuli vähän, mutta "
        "haastatellut iltatyöläiset pitivät kokeilua tärkeänä. Osa heistä kuuli uusista ajoista "
        "vasta jakson lopussa. Raportti suosittelee toista "
        "kokeilujaksoa paremman tiedotuksen jälkeen. Mihin suositus ensisijaisesti perustuu?",
        [
            "Ensimmäinen jakso vahvisti kysynnän riittäväksi; nyt etsitään sopivaa pysyvää sulkemisaikaa.",
            "Tarvetta on vaikea arvioida, kun osa mahdollisista käyttäjistä ei tiennyt kokeilusta ajoissa.",
            "Haastattelut ennustavat kävijämäärän kasvun; uusi jakso selvittää lähinnä kasvun suuruutta.",
            "Vähäinen käyttö osoitti ilta-ajan tarpeettomaksi; toisella jaksolla verrataan päiväaikoja.",
        ],
        "Tarvetta on vaikea arvioida, kun osa mahdollisista käyttäjistä ei tiennyt kokeilusta ajoissa.",
    ),
    AssessmentQuestion(
        "fi-r-c1-002",
        "reading",
        "C1",
        "Asukas kirjoittaa: «En vastusta pihajuhlia. Viime vuonna ilmoitus tuli vasta samana "
        "iltana, enkä ehtinyt järjestää yövuoroa edeltävää lepoa muualla. Jos päivämäärän "
        "tietäisi ajoissa, tilanne olisi toinen.» Mikä ehdotus vastaa parhaiten hänen huoleensa?",
        [
            "Pidetään juhla entiseen tapaan ja kerätään sen jälkeen palaute kaikilta asukkailta.",
            "Vähennetään juhlan tarjoilua, jotta yhteiset kustannukset pysyvät kohtuullisina.",
            "Siirretään juhla sisälle ja ilmoitetaan muutoksesta asukkaille tapahtumapäivänä.",
            "Sovitaan päivä hyvissä ajoin ja ilmoitetaan se myös niille, jotka eivät osallistu.",
        ],
        "Sovitaan päivä hyvissä ajoin ja ilmoitetaan se myös niille, jotka eivät osallistu.",
    ),
    AssessmentQuestion(
        "fi-r-c1-003",
        "reading",
        "C1",
        "«Kun lähdin korjaamolle, kuvittelin saavani laitteen heti mukaani. Olin saanut viestin, jossa "
        "kerrottiin osan saapuneen. Vasta tiskillä selvisi, että asennusaika piti varata erikseen.» "
        "Mistä kertojan väärinkäsitys syntyi?",
        [
            "Hän oletti varaosan saapumisen merkitsevän, että laitteen voisi jo noutaa.",
            "Hän tulkitsi asennusajan vahvistuksen merkiksi varaosan tilauksen peruuntumisesta.",
            "Hän oletti korjaamon viestin koskevan toista laitetta kuin sitä, jonka oli jättänyt sinne.",
            "Hän oletti varaosan puuttuvan, vaikka korjaamo oli ilmoittanut asennuksen alkaneen.",
        ],
        "Hän oletti varaosan saapumisen merkitsevän, että laitteen voisi jo noutaa.",
    ),
    AssessmentQuestion(
        "fi-r-c1-004",
        "reading",
        "C1",
        "Työryhmä haluaa yhteistilan pysyvän avoinna pidempään. Huoltoyhtiö suostuu "
        "selvittämään kustannukset, jos käyttäjämääristä saadaan viikon seuranta. "
        "Seurannan tekijää ei vielä sovittu. Mikä seuraava toimi vie asiaa eteenpäin "
        "ylittämättä annettuja sitoumuksia?",
        [
            "Ilmoitetaan pidennetyt aukioloajat ja pyydetään huoltoyhtiöltä lasku jälkikäteen.",
            "Pyydetään huoltoyhtiötä vahvistamaan seuranta, jonka se jo lupasi toteuttaa.",
            "Sovitaan seurannan vastuuhenkilö ja toimitetaan tulokset kustannusten selvittämistä varten.",
            "Tilataan huoltoyhtiöltä lisätunnit, joiden kustannukset työryhmä on hyväksynyt.",
        ],
        "Sovitaan seurannan vastuuhenkilö ja toimitetaan tulokset kustannusten selvittämistä varten.",
    ),
]
