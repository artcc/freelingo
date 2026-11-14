"""Finnish A1 grammar with standard Finnish explanations."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "fi-sounds-a1",
        "Lyhyet ja pitkät äänteet",
        "A1",
        "Äänteet ja kirjoitus",
        "Äänteen pituus voi muuttaa sanan merkityksen.",
        "Suomen kirjoitus näyttää yleensä äänteiden pituuden. Yksi kirjain merkitsee lyhyttä "
        "äännettä, kaksi samaa kirjainta pitkää: tuli ja tuuli, kuka ja kukka. "
        "Pitkä konsonantti kestää kauemmin; älä lisää sen väliin vokaalia. Sanan pääpaino on "
        "ensimmäisellä tavulla myös silloin, kun pitkä äänne on myöhemmin. Ä ja ö ovat omia "
        "kirjaimiaan, eivät a:n ja o:n koristeita.",
        rules=[
            "Kuuntele sekä vokaalin että konsonantin kestoa.",
            "Kirjoita pitkä äänne kahdella samalla kirjaimella.",
        ],
        examples=[
            GrammarExample("Tuli on kuuma.", note="Tuli: lyhyt u."),
            GrammarExample("Tuuli on kylmä.", note="Tuuli: pitkä uu."),
            GrammarExample("Kuka hän on?"),
            GrammarExample("Tämä on kukka."),
        ],
        related=["fi-vowel-harmony-a1"],
    ),
    GrammarTopic(
        "fi-vowel-harmony-a1",
        "Vokaalisointu",
        "A1",
        "Äänteet ja kirjoitus",
        "Valitse tavalliseen päätteeseen a tai ä sanan vokaalien mukaan.",
        "Vokaalit a, o ja u ovat takavokaaleja; ä, ö ja y ovat etuvokaaleja. "
        "Tavallisessa yksinkertaisessa sanassa ne eivät yleensä esiinny yhdessä. "
        "E ja i voivat esiintyä kummankin ryhmän kanssa. Pääte mukautuu sanaan: "
        "talo–talossa, kylä–kylässä. Jos sanassa on vain e ja i, pääte on tavallisesti "
        "etuvokaalinen: nimi–nimessä. Yhdyssanan pääte seuraa viimeistä osaa: "
        "kirjahyllyssä. Joissakin lainasanoissa on poikkeavia yhdistelmiä.",
        structure="a, o, u → -ssa; ä, ö, y → -ssä",
        rules=[
            "E ja i eivät yksin vaadi takavokaalista päätettä.",
            "Opettele uudet päätteet pareina: -ko/-kö, -ssa/-ssä.",
        ],
        examples=[
            GrammarExample("talossa – kylässä", note="Paikan muodot opitaan myöhemmin."),
            GrammarExample("Onko hän täällä?", note="On saa liitteen -ko: sanassa on o."),
        ],
        common_mistakes=[GrammarMistake("kylassa", "kylässä", "Kylä saa etuvokaalisen päätteen.")],
        related=["fi-sounds-a1"],
    ),
    GrammarTopic(
        "fi-olla-pronouns-a1",
        "Minä olen, sinä olet",
        "A1",
        "Verbit ja pronominit",
        "Esittele ihminen tai asia olla-verbillä.",
        "Persoonapronominit ovat minä, sinä, hän, me, te ja he. Hän viittaa ihmiseen "
        "sukupuolesta riippumatta. Olla-verbin preesens on olen, olet, on, olemme, olette, "
        "ovat. Käytä yleiskielessä he ovat. Puheessa kuulet myös muita muotoja. "
        "Minä ja sinä voivat jäädä pois, kun verbin pääte kertoo henkilön: Olen Aino. "
        "Sinuttelu on Suomessa tavallista; te voi tarkoittaa useita ihmisiä tai kohteliasta "
        "puhuttelua yhdelle ihmiselle.",
        structure="minä olen / sinä olet / hän on / me olemme / te olette / he ovat",
        rules=[
            "Suomessa ei ole erillisiä hän-pronomineja miehelle ja naiselle.",
            "Valitse verbimuoto tekijän mukaan.",
        ],
        examples=[GrammarExample("Minä olen opiskelija."), GrammarExample("He ovat täällä.")],
        common_mistakes=[
            GrammarMistake("Minä on Aino.", "Minä olen Aino.", "Minä tarvitsee muodon olen.")
        ],
        related=["fi-sounds-a1"],
    ),
    GrammarTopic(
        "fi-nominative-a1",
        "Sanan perusmuoto ja yksinkertainen kuvaus",
        "A1",
        "Nominit",
        "Nimeä yksi asia ja kuvaile sitä.",
        "Nominatiivi on sanakirjan perusmuoto: talo, kirja, ystävä. Suomen sanoilla ei ole "
        "kieliopillista sukua eikä artikkeleita. Yhden laskettavan asian tavallisessa "
        "kuvauksessa käytetään muotoa Kirja on uusi. Adjektiivi voi olla myös ennen nimeä: "
        "uusi kirja. Tämä esittelee lähellä olevan asian. Tässä vaiheessa harjoitellaan "
        "yksikköä; aineita ja monikkoa kuvataan myöhemmin myös muilla muodoilla.",
        rules=["Älä lisää artikkelia substantiivin eteen.", "Erota uusi kirja ja Kirja on uusi."],
        examples=[GrammarExample("Tämä on pieni talo."), GrammarExample("Talo on vanha.")],
        common_mistakes=[
            GrammarMistake(
                "Tämä ovat pieni talo.",
                "Tämä on pieni talo.",
                "Yhtä taloa esiteltäessä tämä saa verbimuodon on.",
            )
        ],
        related=["fi-olla-pronouns-a1"],
    ),
    GrammarTopic(
        "fi-genitive-a1",
        "Kenen? Genetiivin alku",
        "A1",
        "Nominit",
        "Liitä omistaja tai muu määrite asian nimeen.",
        "Yksikön genetiivin pääte on -n: Aino–Ainon, talo–talon. Se vastaa usein kysymykseen "
        "kenen: Ainon kirja. Genetiivi voi ilmaista myös muuta yhteyttä: talon ovi. "
        "Pääte liittyy vartaloon, joka voi poiketa perusmuodosta: käsi–käden. "
        "Opettele tavalliset muodot pareina. Minä-pronominin genetiivi on minun. "
        "Huolitellussa yleiskielessä omistus ilmaistaan myös omistusliitteellä: minun nimeni. "
        "Harjoittele aluksi valmiita ilmauksia nimeni ja sinun nimesi.\n\n"
        "Omistusliitteet ovat -ni, -si, -nsa/-nsä, -mme ja -nne: minun kirjani, "
        "sinun kirjasi, hänen kirjansa, meidän kirjamme, teidän kirjanne, heidän kirjansa. "
        "Hänen kirjansa ja heidän kirjansa käyttävät samaa liitettä. Puheessa kuulet myös ilmauksia kuten "
        "mun kirja; ne ovat puhekieltä. Nimen jälkeen liitettä ei yleensä tarvita: Ainon kirja.",
        structure="Ainon + kirja; minun nimeni; sinun nimesi",
        rules=["Omistaja tulee ennen omistettavaa asiaa.", "Genetiivin -n ei ole monikon tunnus."],
        examples=[GrammarExample("Tämä on Ainon koti."), GrammarExample("Minun nimeni on Eero.")],
        common_mistakes=[
            GrammarMistake(
                "Aino kirja", "Ainon kirja", "Kun Aino omistaa kirjan, nimi saa genetiivin."
            )
        ],
        related=["fi-nominative-a1"],
    ),
    GrammarTopic(
        "fi-present-a1",
        "Preesens: puhun ja asun",
        "A1",
        "Verbit",
        "Kerro nykyhetkestä ja tavallisista tekemisistä.",
        "Preesens kertoo nykyhetkestä tai tavasta. Puhua taipuu: puhun, puhut, puhuu, "
        "puhumme, puhutte, puhuvat. Vartalon jälkeen tulevat persoonapäätteet. "
        "Kolmannen persoonan yksikössä vokaali usein pitenee. Kaikki verbit eivät taivu "
        "samalla tavalla: syödä–syön–syö, mennä–menen–menee, opiskella–opiskelen–opiskelee. "
        "Oppimista auttaa perusmuodon ja minä-muodon pari. Preesens voi viitata myös tulevaan, "
        "kun ajankohta on selvä.",
        structure="puhu-n, puhu-t, puhu-u, puhu-mme, puhu-tte, puhu-vat",
        rules=[
            "Opettele verbin vartalo minä-muodon avulla.",
            "Yleiskielessä he puhuvat, eivät he puhu.",
        ],
        examples=[
            GrammarExample("Puhun suomea."),
            GrammarExample("Me asumme Suomessa."),
            GrammarExample("Hän opiskelee tänään."),
        ],
        common_mistakes=[GrammarMistake("Minä puhuu.", "Minä puhun.", "Minä-muodon pääte on -n.")],
        related=["fi-olla-pronouns-a1", "fi-vowel-harmony-a1"],
    ),
    GrammarTopic(
        "fi-negation-a1",
        "En puhu, ei ole",
        "A1",
        "Verbit",
        "Kielteisen lauseen persoonapääte on kieltoverbissä.",
        "Kieltoverbin muodot ovat en, et, ei, emme, ette ja eivät. Preesensissä pääverbi "
        "on kieltomuodossa ilman persoonapäätettä: en puhu, hän ei puhu. Kieltomuodon saa "
        "monissa tutuissa verbeissä poistamalla minä-muodon lopun -n: asun–asu, menen–mene. "
        "Olla-verbin kieltomuoto on ole: emme ole.",
        structure="en / et / ei / emme / ette / eivät + puhu",
        rules=["Taivuta kieltoverbi tekijän mukaan.", "Älä säilytä pääverbin persoonapäätettä."],
        examples=[GrammarExample("En asu Turussa."), GrammarExample("He eivät ole täällä.")],
        common_mistakes=[
            GrammarMistake(
                "Minä en puhun.", "Minä en puhu.", "Kieltoverbi kantaa persoonapäätteen."
            )
        ],
        related=["fi-present-a1", "fi-olla-pronouns-a1"],
    ),
    GrammarTopic(
        "fi-questions-a1",
        "Kysymyssanat ja -ko/-kö",
        "A1",
        "Lauseet",
        "Pyydä tietoa tai kysy, pitääkö asia paikkansa.",
        "Kysymyssanat kuka, mikä, missä, mistä, mihin ja milloin pyytävät tietoa. "
        "Tavallisessa kyllä–ei-kysymyksessä taipunut verbi on alussa ja saa liitteen "
        "-ko tai -kö: Asutko täällä? Oletko opiskelija? Vastauksessa voi toistaa verbin: "
        "Asun. En asu. Kielteisessä kysymyksessä liite on kieltoverbissä: Etkö asu täällä? "
        "Kielteinen kysymys voi ilmaista myös yllättyneisyyttä.",
        rules=[
            "Valitse -ko/-kö vokaalisoinnun mukaan.",
            "Kysymyssanan kanssa ei yleensä tarvita -ko/-kö-liitettä.",
        ],
        examples=[
            GrammarExample("Kuka hän on?"),
            GrammarExample("Puhutko suomea?"),
            GrammarExample("Missä sinä asut?"),
        ],
        common_mistakes=[
            GrammarMistake(
                "Missä asutko?", "Missä asut?", "Tavallinen missä-kysymys ei saa kysymysliitettä."
            )
        ],
        related=["fi-present-a1", "fi-negation-a1", "fi-vowel-harmony-a1"],
    ),
    GrammarTopic(
        "fi-numbers-a1",
        "Lukumäärät ja hinnat",
        "A1",
        "Luvut",
        "Tunnista perusluvut ja ilmoita yksinkertainen määrä.",
        "Perusluvut ovat nolla, yksi, kaksi, kolme, neljä, viisi, kuusi, seitsemän, kahdeksan "
        "ja yhdeksän. Kymmenen on 10, yksitoista 11, kaksikymmentä 20 ja sata 100. "
        "Yksi liittyy tavallisesti yksikön perusmuotoon: yksi euro. Perusmuotoisen "
        "lukusanan kaksi tai sitä suuremman luvun jälkeen asia on yksikön partitiivissa: "
        "kaksi euroa. Partitiivin muodot harjoitellaan seuraavaksi. Puhelinnumeron voi "
        "sanoa numero kerrallaan.",
        structure="yksi euro; kaksi euroa; kaksikymmentäviisi euroa",
        rules=[
            "Lukumäärän jälkeen ei käytetä automaattisesti monikkoa.",
            "Desimaalipilkku erottaa eurot ja senttien osuuden hinnassa.",
        ],
        examples=[GrammarExample("Hinta on yksi euro."), GrammarExample("Hinta on kolme euroa.")],
        common_mistakes=[
            GrammarMistake("kaksi euro", "kaksi euroa", "Kaksi vaatii tässä yksikön partitiivin.")
        ],
        related=["fi-nominative-a1"],
    ),
    GrammarTopic(
        "fi-partitive-a1",
        "Partitiivi: kahvia ja kaksi omenaa",
        "A1",
        "Nominit",
        "Ilmaise ainetta, määrää ja kielteisen lauseen kohdetta.",
        "Yksikön partitiivin tavallisia päätteitä ovat -a/-ä ja -ta/-tä: kahvi–kahvia, "
        "tee–teetä. Joidenkin sanojen vartalo muuttuu: vesi–vettä. Partitiivia käytetään "
        "aineesta ilman rajattua määrää: Juon vettä. Sitä käytetään myös lukusanan kaksi "
        "tai suuremman luvun jälkeen: kolme omenaa. Kielteisen lauseen kohde on tavallisesti "
        "partitiivissa: En osta leipää. Kaikki myönteisen lauseen kohteet eivät ole "
        "partitiivissa; kokonaisen kohteen muodot opitaan myöhemmin.",
        rules=[
            "Opettele tavalliset ruokasanat myös partitiivissa.",
            "Kielteinen lause: En juo kahvia.",
        ],
        examples=[GrammarExample("Juon teetä."), GrammarExample("Minulla on kaksi omenaa.")],
        common_mistakes=[
            GrammarMistake(
                "En juo kahvi.", "En juo kahvia.", "Kielteisen lauseen kohde on partitiivissa."
            )
        ],
        related=["fi-numbers-a1", "fi-negation-a1"],
    ),
    GrammarTopic(
        "fi-possession-a1",
        "Minulla on ja minulla ei ole",
        "A1",
        "Lauseet",
        "Kerro, mitä joku omistaa tai mitä hänellä on mukanaan.",
        "Omistusta ilmaistaan rakenteella minulla on. Muodot ovat minulla, sinulla, hänellä, "
        "meillä, teillä ja heillä. Olla-verbi on tässä yleensä muodossa on, myös monikon "
        "omistajan kanssa: Meillä on auto. Tavallisessa kielteisessä omistuslauseessa "
        "omistettava asia on partitiivissa: Minulla ei ole autoa. Sama rakenne ilmaisee "
        "myös olotilan: Minulla on nälkä.",
        structure="omistaja -lla/-llä + on + asia; omistaja + ei ole + partitiivi",
        rules=["Älä taivuta on-muotoa omistajan persoonan mukaan.", "Kysymys: Onko sinulla rahaa?"],
        examples=[GrammarExample("Hänellä on koira."), GrammarExample("Meillä ei ole autoa.")],
        common_mistakes=[
            GrammarMistake(
                "Minä on koira.", "Minulla on koira.", "Omistaja ilmaistaan tässä -lla-muodolla."
            )
        ],
        related=["fi-olla-pronouns-a1", "fi-partitive-a1"],
    ),
    GrammarTopic(
        "fi-inner-local-a1",
        "Talossa, talosta, taloon",
        "A1",
        "Paikka",
        "Erota sisällä oleminen, lähteminen ja sisään meneminen.",
        "Kysymykseen missä vastaa usein -ssa/-ssä: talossa. Kysymykseen mistä vastaa "
        "-sta/-stä: talosta. Kysymykseen mihin vastaa illatiivi: taloon, kauppaan. "
        "Illatiivilla on useita muodostustapoja; opettele ensin tutut paikat kokonaisina "
        "sarjoina. Paikkamuotoja käytetään myös kaupunkien kanssa: Helsingissä, "
        "Helsingistä, Helsinkiin. Kaikki paikat eivät käytä samaa sarjaa.",
        structure="missä: talossa; mistä: talosta; mihin: taloon",
        rules=[
            "Valitse muoto liikkeen suunnan mukaan.",
            "Opettele erikseen kotona, kotoa ja kotiin.",
        ],
        examples=[
            GrammarExample("Olen kaupassa."),
            GrammarExample("Tulen kaupasta."),
            GrammarExample("Menen kauppaan."),
        ],
        common_mistakes=[
            GrammarMistake("Menen talo.", "Menen taloon.", "Kun talo on määränpää, käytä taloon.")
        ],
        related=["fi-vowel-harmony-a1", "fi-questions-a1"],
    ),
    GrammarTopic(
        "fi-outer-local-a1",
        "Pöydällä, pöydältä, pöydälle",
        "A1",
        "Paikka",
        "Käytä ulkopaikallissijoja pinnasta ja tutuista paikoista.",
        "Pinnalla oleminen ilmaistaan usein -lla/-llä-päätteellä: pöydällä. Pinnalta "
        "lähteminen ilmaistaan -lta/-ltä-päätteellä ja pinnalle tuleminen -lle-päätteellä. "
        "Samaa sarjaa käytetään esimerkiksi sanoissa tori ja asema: torilla, torilta, "
        "torille; asemalla, asemalta, asemalle. Valinta ei riipu vain siitä, onko paikassa "
        "katto. Opettele paikan tavallinen käyttötapa. -lla/-llä voi ilmaista myös "
        "kulkuvälineen: bussilla.",
        structure="missä: pöydällä; mistä: pöydältä; mihin: pöydälle",
        rules=["Erota torilla ja torille.", "Paikan pääte opitaan sanan käytön mukana."],
        examples=[
            GrammarExample("Kirja on pöydällä."),
            GrammarExample("Menen asemalle."),
            GrammarExample("Tulen bussilla."),
        ],
        common_mistakes=[
            GrammarMistake("Olen torille.", "Olen torilla.", "Sijainti, ei määränpää: torilla.")
        ],
        related=["fi-inner-local-a1", "fi-possession-a1"],
    ),
    GrammarTopic(
        "fi-time-a1",
        "Viikonpäivät ja kellonajat",
        "A1",
        "Aika",
        "Sovi, milloin jokin tapahtuu.",
        "Viikonpäivän ajankohta saa usein -na/-nä-päätteen: maanantaina, perjantaina. "
        "Päivän osia ovat aamulla, päivällä, illalla ja yöllä. Kellonaika ilmaistaan "
        "sanalla kello: kello kahdeksan. Puoli yhdeksän on 8.30, siis puoli tuntia ennen "
        "yhdeksää. Varttia yli kahdeksan on 8.15; varttia vaille yhdeksän on 8.45. "
        "Kirjallisessa aikataulussa käytetään usein 24 tunnin kelloa.",
        rules=[
            "Kysy ajankohtaa: Milloin? Mihin aikaan?",
            "Erota puoli kahdeksan (7.30) ja puoli yhdeksän (8.30).",
        ],
        examples=[
            GrammarExample("Tapaamme tiistaina kello kuusi."),
            GrammarExample("Kurssi alkaa aamulla kello yhdeksän."),
        ],
        common_mistakes=[
            GrammarMistake(
                "Tapaamme maanantai.",
                "Tapaamme maanantaina.",
                "Tapaamisen ajankohta tarvitsee tässä -na-päätteen.",
            )
        ],
        related=["fi-numbers-a1", "fi-present-a1"],
    ),
    GrammarTopic(
        "fi-modals-a1",
        "Voin ja haluan tehdä",
        "A1",
        "Verbit",
        "Ilmaise mahdollisuus tai oma toive.",
        "Voida ja haluta saavat usein seurakseen verbin perusmuodon: voin tulla, haluan "
        "levätä. Ensimmäinen verbi taipuu persoonassa, toinen ei: hän voi tulla, me "
        "haluamme tulla. Kielto koskee ensimmäistä verbiä: en voi tulla. Voitko auttaa? "
        "on tavallinen avunpyyntö. Se ei edellytä muodollista puhuttelua. Taito, lupa ja "
        "velvollisuus erotetaan tarkemmin seuraavalla tasolla.",
        structure="voin / haluan + verbin perusmuoto",
        rules=["Taivuta vain ensimmäinen verbi.", "Kielteinen muoto: en halua, en voi."],
        examples=[GrammarExample("Voitko auttaa?"), GrammarExample("Haluan levätä kotona.")],
        common_mistakes=[
            GrammarMistake("Voin tulen.", "Voin tulla.", "Voida-verbin jälkeen tulee perusmuoto.")
        ],
        related=["fi-present-a1", "fi-negation-a1", "fi-questions-a1"],
    ),
    GrammarTopic(
        "fi-coordination-a1",
        "Ja, mutta, tai ja vai",
        "A1",
        "Lauseet",
        "Yhdistä asioita ja esitä vaihtoehtoja.",
        "Ja yhdistää: teetä ja kahvia. Mutta ilmaisee vastakohdan: Haluan tulla, mutta en "
        "voi. Tai esittää vaihtoehdon: Voimme tavata tänään tai huomenna. Vai kuuluu "
        "tavallisesti vaihtoehtokysymykseen, jossa valitaan vaihtoehdoista: Otatko teetä "
        "vai kahvia? Tai voi esiintyä myös kysymyksessä, jos kysytään, löytyykö jompaakumpaa: "
        "Onko sinulla kynää tai paperia?",
        rules=[
            "Valintakysymyksessä käytä tavallisesti vai-sanaa.",
            "Kaksi itsenäistä lausetta erotetaan yleensä pilkulla ennen mutta-sanaa.",
        ],
        examples=[
            GrammarExample("Olen väsynyt, mutta voin auttaa."),
            GrammarExample("Tuletko tänään vai huomenna?"),
        ],
        related=["fi-modals-a1", "fi-questions-a1"],
    ),
]
