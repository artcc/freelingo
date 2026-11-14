"""Finnish B1 phrases for practical communication and repair."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "fi-experiences-b1",
        "B1",
        "Kokemuksesta kertominen",
        "💬",
        [
            PhrasebookEntry(
                "Olin jo lähtenyt kotoa, kun huomasin viestisi.",
                "Selität, miksi et voinut muuttaa suunnitelmaa heti.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Yritin korjata sitä itse, mutta en saanut sitä toimimaan.",
                "Erotat yrityksen onnistuneesta korjauksesta.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Aluksi kaikki sujui hyvin, mutta sitten juna pysähtyi.",
                "Aloitat kertomuksen matkalla syntyneestä ongelmasta.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "En ollut käynyt siellä aikaisemmin, joten eksyin hetkeksi.",
                "Annat taustatiedon, joka selittää tapahtuman.",
                "neutral",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Hetkinen, sitä ennen haimme vielä avaimet.",
                "Korjaat ystävän kertomuksen tapahtumajärjestystä.",
                "informal",
                "b1-unit-1",
            ),
            PhrasebookEntry(
                "Lopulta löysimme ratkaisun, ja nyt asia on kunnossa.",
                "Päätät kertomuksen ongelman selviämiseen.",
                "neutral",
                "b1-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-arrangements-b1",
        "B1",
        "Ajan ja ehtojen sopiminen",
        "📅",
        [
            PhrasebookEntry(
                "Voisimmeko siirtää tapaamisen puoli tuntia myöhemmäksi?",
                "Pyydät muutosta jo sovittuun aikaan.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Tiistai ei sovi minulle, mutta keskiviikkona olisin vapaa.",
                "Tarjoat vaihtoehdon pelkän kieltäytymisen sijaan.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Minun täytyy tarkistaa työvuoroni ennen kuin lupaan mitään.",
                "Selität, miksi et voi vielä sitoutua ehdotukseen.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Olisin ilmoittanut aiemmin, jos olisin tiennyt muutoksesta.",
                "Selität myöhäistä yhteydenottoa menneen tilanteen avulla.",
                "neutral",
                "b1-unit-2",
            ),
            PhrasebookEntry(
                "Tarvitseeko minun maksaa etukäteen, vai voinko maksaa paikan päällä?",
                "Tarkistat maksamisen ehdot ennen varausta.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Vahvistaisitteko uuden ajan vielä kirjallisesti?",
                "Pyydät palveluntarjoajalta yksiselitteistä vahvistusta.",
                "formal",
                "b1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-housing-b1",
        "B1",
        "Vikailmoitus ja yhteiset tilat",
        "🏠",
        [
            PhrasebookEntry(
                "Keittiön hanasta vuotaa vettä, vaikka se on suljettu.",
                "Kuvaat huoltoyhtiölle havaittavan vian.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Onko vesikatkosta jo ilmoitettu kaikille asukkaille?",
                "Varmistat, että yhteisestä häiriöstä on tiedotettu.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Hissiä ei korjattu eilen. Milloin korjaaja tulee uudestaan?",
                "Kysyt uuden käynnin aikaa toteutumattoman korjauksen jälkeen.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Saako pyörää säilyttää tässä, vai onko sille oma tila?",
                "Selvität yhteisten tilojen käyttösääntöjä.",
                "neutral",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Voisitteko ilmoittaa etukäteen, jos asuntoon täytyy tulla?",
                "Pyydät huollolta tietoa asuntoon pääsystä.",
                "formal",
                "b1-unit-3",
            ),
            PhrasebookEntry(
                "Kiitos, ovi toimii nyt. Vika on siis korjattu.",
                "Vahvistat huollolle, että korjaus onnistui.",
                "neutral",
                "b1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-learning-services-b1",
        "B1",
        "Oma osaaminen ja asioinnin tuki",
        "📝",
        [
            PhrasebookEntry(
                "Osaan hoitaa tavalliset tilanteet, mutta tarvitsen vielä apua puhelimessa.",
                "Kuvaat kielitaitoasi työpaikan ohjaajalle.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Haluaisin osallistua koulutukseen ja kehittää osaamistani.",
                "Ilmaiset halusi kehittää osaamistasi.",
                "neutral",
                "b1-unit-4",
            ),
            PhrasebookEntry(
                "Voisitko näyttää kerran, miten tämä tehdään?",
                "Pyydät työtoverilta käytännön mallia uuteen tehtävään.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Tässä on todistus, jota pyysitte hakemuksen liitteeksi.",
                "Toimitat puuttuvan asiakirjan virkailijalle.",
                "formal",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Haluaisin tietää, kuinka kauan käsittely yleensä kestää.",
                "Kysyt arviota odotusajasta vaatimatta varmaa määräpäivää.",
                "neutral",
                "b1-unit-5",
            ),
            PhrasebookEntry(
                "Tarvitsen lisäaikaa, jotta voin hankkia puuttuvan liitteen.",
                "Perustelet määräajan pidentämistä.",
                "neutral",
                "b1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-clarification-b1",
        "B1",
        "Viestin tarkentaminen",
        "🔎",
        [
            PhrasebookEntry(
                "Ymmärsinkö oikein, että tapaaminen alkaa vasta kymmeneltä?",
                "Tarkistat tulkintasi muuttuneesta aloitusajasta.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Tarkoitin ensi perjantaita, en huomista.",
                "Korjaat väärin ymmärretyn päivämäärän.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Aino pyysi kertomaan, että hän myöhästyy noin vartin.",
                "Välität poissa olevan henkilön viestin.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Voisitko sanoa viimeisen kohdan toisella tavalla?",
                "Pyydät uutta selitystä pelkän toistamisen sijaan.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Vaikka sain viestin, liite ei auennut puhelimessani.",
                "Erotat viestin vastaanottamisen sen sisällön lukemisesta.",
                "neutral",
                "b1-unit-6",
            ),
            PhrasebookEntry(
                "Sovitaan vielä, kuka ilmoittaa muutoksesta muille.",
                "Estät tiedonkulun katkeamisen keskustelun lopuksi.",
                "neutral",
                "b1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-choices-b1",
        "B1",
        "Valinnan perusteleminen",
        "⚖️",
        [
            PhrasebookEntry(
                "Tämä maksaa enemmän, mutta kestää todennäköisesti pidempään.",
                "Vertaat hankintahintaa ja tuotteen käyttöikää.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Minulle lyhyt työmatka on tärkeämpi kuin suuri asunto.",
                "Selität omat valintaperusteesi asuntoa etsiessäsi.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Olen samaa mieltä hinnasta, mutta laatu huolestuttaa minua.",
                "Hyväksyt yhden perusteen ja tuot esiin toisen näkökulman.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Minäkin valitsisin junan, jos aikataulu sopisi.",
                "Liität oman ehdollisen kantasi toisen mielipiteeseen.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "En halua päättää heti. Vertailen vielä muita vaihtoehtoja.",
                "Pyydät harkinta-aikaa ennen ostoa.",
                "neutral",
                "b1-unit-7",
            ),
            PhrasebookEntry(
                "Toimin ensin vapaaehtoisena ja kouluttauduin myöhemmin ohjaajaksi.",
                "Kuvaat oman roolisi muutosta.",
                "neutral",
                "b1-unit-7",
            ),
        ],
    ),
]
