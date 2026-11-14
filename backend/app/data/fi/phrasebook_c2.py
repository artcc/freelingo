"""Finnish C2 phrases for difficult conversations and accountable synthesis."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

C2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "fi-weighing-uncertainty-c2",
        "C2",
        "Epävarmuuden arvioiminen ilman jälkiviisautta",
        "🔎",
        [
            PhrasebookEntry(
                "Näillä tiedoilla pitäisin tätä mahdollisena selityksenä, en vielä todennäköisimpänä.",
                "Rajoitat liian varmaa tulkintaa keskeneräisessä selvityksessä.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Mitä vaihtoehtoja meillä oli silloin käytettävissä, ennen kuin tämä tieto saatiin?",
                "Palautat jälkikäteisen arvioinnin tapahtumahetken todellisiin mahdollisuuksiin.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Se olisi voinut auttaa, mutta emme voi tietää, olisiko lopputulos muuttunut.",
                "Tunnustat käyttämättä jääneen mahdollisuuden lupaamatta vaihtoehtoista onnistumista.",
                "neutral",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Arvion epävarmuus ei tarkoita, ettei päätöstä voisi tehdä; se pitää vain huomioida.",
                "Ehdotat etenemistä tilanteessa, jossa täydellistä tietoa ei ole saatavilla.",
                "formal",
                "c2-unit-1",
            ),
            PhrasebookEntry(
                "Sovitaanko samalla, mikä uusi havainto saisi meidät arvioimaan ratkaisua uudelleen?",
                "Liität epävarmaan päätökseen etukäteen sovitun tarkistuskohdan.",
                "neutral",
                "c2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-questioning-assumptions-c2",
        "C2",
        "Kiistanalaisen oletuksen nostaminen esiin",
        "🧩",
        [
            PhrasebookEntry(
                "Kysymys olettaa, että olemme jo hylänneet ehdotuksen. Siitä ei ole vielä päätetty.",
                "Vastaat painostavaan kysymykseen hyväksymättä sen virheellistä lähtökohtaa.",
                "formal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "En kiistä tapahtunutta, vaan sen, että sitä olisi täsmällistä kutsua suostumukseksi.",
                "Erotat tapahtumien myöntämisen niistä käytetyn nimityksen hyväksymisestä.",
                "formal",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Mitä tässä yhteydessä tarkoitat kohtuullisella ajalla?",
                "Pyydät avaamaan sanan, jonka merkityksestä osapuolet voivat olla eri mieltä.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Voimmeko tarjota edes väliaikaisen ratkaisun, jos pysyvä ei vielä onnistu?",
                "Asetat neuvottelulle vaatimattomamman mutta hyödyllisen välitavoitteen.",
                "neutral",
                "c2-unit-2",
            ),
            PhrasebookEntry(
                "Jos jätämme tuon oletuksen hetkeksi sivuun, mitä itse aineisto osoittaa?",
                "Ohjaat keskustelun arvottavasta lähtökohdasta yhteisesti tarkasteltavaan tietoon.",
                "neutral",
                "c2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-unpacking-contracts-c2",
        "C2",
        "Vaativan asiakirjan selventäminen",
        "📄",
        [
            PhrasebookEntry(
                "Pyydän yksilöimään, mihin tilanteisiin tämä poikkeusperuste soveltuu.",
                "Haet virallisessa yhteydenotossa tarkkaa tietoa säännön soveltamisalasta.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Onko velvoite selvittää vaihtoehdot vai toteuttaa niistä jokin?",
                "Purat tiivistä tehtävänantoa ennen työn aloittamista.",
                "neutral",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Jos muotoilemme tämän lyhyemmin, myös määräaikaisuuden on jäätävä näkyviin.",
                "Ohjaat sopimuksen tiivistämistä niin, ettei olennainen rajaus katoa.",
                "formal",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Tässä puhutaan tarkastajan hyväksymästä muutoksesta, ei tarkastajan ehdottamasta.",
                "Korjaat osapuolten roolit sekoittavan selostuksen.",
                "neutral",
                "c2-unit-3",
            ),
            PhrasebookEntry(
                "Voimmeko kokeilla sanamuotoa yhdellä rajatapauksella ennen kuin hyväksymme sen?",
                "Testaat käytännössä, onko yhdessä laadittu ehto riittävän yksiselitteinen.",
                "neutral",
                "c2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-narrative-perspectives-c2",
        "C2",
        "Kokemuksen ja tulkinnan erottaminen",
        "📚",
        [
            PhrasebookEntry(
                "Silloin tulkitsin hiljaisuuden torjunnaksi; nyt näen muitakin mahdollisuuksia.",
                "Kerrot vanhasta ristiriidasta tekemättä omasta kokemuksestasi ainoaa selitystä.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Kerron tämän omasta näkökulmastani, joten hänen tarkoituksensa jää minulle osin avoimeksi.",
                "Rajaat oman kertomuksesi tiedollista ulottuvuutta.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Tuossa kohdassa kuulen enemmän henkilön pettymyksen kuin kertojan lopullisen arvion.",
                "Perustelet lukupiirissä, kenen ääni tekstin sanavalinnassa kuuluu.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Teksti yhdistää tapahtumat ajallisesti, mutta syyn me lukijat lisäämme itse.",
                "Erotat tekstin antamat tiedot sen herättämästä tulkinnasta.",
                "neutral",
                "c2-unit-4",
            ),
            PhrasebookEntry(
                "Lyhyesti kerrottuna kyse oli eksymisestä; pidempi tarina onkin sitten toinen juttu.",
                "Säätelet tutussa seurassa kertomuksen pituutta ja herätät kiinnostusta jatkoon.",
                "informal",
                "c2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-reframing-disagreement-c2",
        "C2",
        "Kärjistyneen erimielisyyden purkaminen",
        "⚖️",
        [
            PhrasebookEntry(
                "Tunnistan tuon riskin, mutta siitä ei vielä seuraa, että ehdotus pitäisi hylätä.",
                "Hyväksyt vastaväitteen olennaisen osan rajaamatta keskustelua sen johtopäätökseen.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Emme taida kiistellä samasta asiasta: minä puhun oikeudesta, sinä käytännön toteutuksesta.",
                "Nimeät keskustelun eri tasot, jotta osapuolet lakkaisivat puhumasta toistensa ohi.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Tuosta muotoilusta en tunnista omaa kantaani. Saanko täsmentää sen?",
                "Korjaat oman näkemyksesi kärjistyksen hyökkäämättä keskustelukumppania vastaan.",
                "neutral",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Yhteinen sanavalinta ei vielä takaa yhteistä käsitystä; avataan, mitä kumpikin tarkoittaa.",
                "Puratte näennäistä yksimielisyyttä ennen sopimuksen tekemistä.",
                "formal",
                "c2-unit-5",
            ),
            PhrasebookEntry(
                "Mistä osasta voisimme sopia nyt ilman, että kumpikaan luopuu keskeisestä periaatteestaan?",
                "Etsit ulospääsyä periaatteellisen kiistan pysäyttämästä neuvottelusta.",
                "neutral",
                "c2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-adjusting-humour-c2",
        "C2",
        "Huumorin ja rekisterin hienosäätö",
        "🎭",
        [
            PhrasebookEntry(
                "Arvoisa yleisö, tekniikka on päättänyt pitää oman puheenvuoronsa.",
                "Kevennät tuttavallisessa tilaisuudessa pientä teknistä häiriötä juhlavalla tyylillä.",
                "informal",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Tuo kuulosti korvissani vähättelevältä, vaikka et ehkä tarkoittanut sitä niin.",
                "Kerrot vitsin vaikutuksesta väittämättä tietäväsi varmasti toisen tarkoitusta.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Yritin keventää tunnelmaa, mutta ajoitus oli huono. Sanon asian uudelleen.",
                "Otat vastuun epäonnistuneesta vitsistä ja palaat varsinaiseen viestiin.",
                "neutral",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Itselleni tässä nauroin, en sinun tavallesi hoitaa asiaa.",
                "Selvennät itseironian kohteen, kun toinen on kokenut huomautuksen arvosteluksi.",
                "informal",
                "c2-unit-6",
            ),
            PhrasebookEntry(
                "Pidetään kirjallinen versio neutraalina; se voi päätyä myös ihmisille, jotka eivät tunne meitä.",
                "Mukautat sisäpiirin viestin laajemmalle yleisölle.",
                "neutral",
                "c2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-synthesising-sources-c2",
        "C2",
        "Lähteistä yhteiseen ratkaisuun",
        "🌉",
        [
            PhrasebookEntry(
                "Lähteet tukevat samaa suuntaa, mutta eivät sellaisinaan samaa suuruusluokkaa.",
                "Esittelet kahden aineiston yhteisen havainnon peittämättä niiden eroja.",
                "formal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Tämä arvio koskee vastanneita, eikä sitä voi suoraan yleistää kaikkiin käyttäjiin.",
                "Rajaat kyselytuloksen tulkintaa päätöstä valmisteltaessa.",
                "formal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Erotetaan tiedotteessa lähteen havainto meidän siitä tekemästämme johtopäätöksestä.",
                "Laadit yhteistä tekstiä, jossa tiedon alkuperän pitää näkyä.",
                "formal",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Kirjataan kolme päivää arvioksi ja sovitaan erikseen sitova viimeinen toimituspäivä.",
                "Estät alustavaa kestoarviota muuttumasta huomaamatta sopimuslupaukseksi.",
                "neutral",
                "c2-unit-7",
            ),
            PhrasebookEntry(
                "Yhteenveto voi olla yhteinen, vaikka siihen kirjataan myös tämä perusteltu erimielisyys.",
                "Rakennat hyväksyttävää loppumuistiota vaatimatta näennäistä yksimielisyyttä.",
                "neutral",
                "c2-unit-7",
            ),
        ],
    ),
]
