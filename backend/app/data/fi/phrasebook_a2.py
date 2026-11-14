"""Finnish A2 phrases for independent routine transactions."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "fi-housing-a2",
        "A2",
        "Asunnosta sopiminen",
        "🏠",
        [
            PhrasebookEntry(
                "Kuuluuko vesi vuokraan?",
                "Asumiskulujen selvittäminen ennen sopimusta.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Milloin asunto on vapaa?",
                "Mahdollisen muuttopäivän kysyminen.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Onko talossa hissiä?",
                "Rakennuksen kulkuyhteyksien varmistaminen.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Voinko tulla katsomaan asuntoa?",
                "Asuntonäytön pyytäminen valmiina asiointi-ilmauksena.",
                "neutral",
                "a2-unit-1",
            ),
            PhrasebookEntry(
                "Keittiön hana vuotaa.", "Vian ilmoittaminen huoltoon.", "neutral", "a2-unit-1"
            ),
            PhrasebookEntry(
                "Tarvitsen toisen avaimen.",
                "Lisäavaimen pyytäminen asunnon omistajalta.",
                "neutral",
                "a2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-shopping-a2",
        "A2",
        "Tuotteen valinta ja vaihtaminen",
        "🛍️",
        [
            PhrasebookEntry(
                "Onko tätä pienempää kokoa?",
                "Saman vaatteen toisen koon kysyminen.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Missä voin sovittaa näitä?",
                "Sovitustilan kysyminen usealle vaatteelle.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Nämä kengät ovat liian pienet.",
                "Sovituksen tuloksen kertominen myyjälle.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Onko tätä myös sinisenä?",
                "Tuotteen toisen värin kysyminen.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Voinko vaihtaa tämän tuotteen?",
                "Vaihtomahdollisuuden kysyminen myyjältä.",
                "neutral",
                "a2-unit-2",
            ),
            PhrasebookEntry(
                "Kuitti on tässä mukana.",
                "Ostotositteen näyttäminen palautustilanteessa.",
                "neutral",
                "a2-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-travel-a2",
        "A2",
        "Varaus ja matkan muutokset",
        "🧳",
        [
            PhrasebookEntry(
                "Minulla on varaus nimellä Laine.",
                "Ilmoittautuminen hotellin vastaanotossa.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Sisältyykö aamiainen hintaan?",
                "Majoituksen sisältämien palvelujen tarkistaminen.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Haluan perua varaukseni.",
                "Aiemmin sovitun majoituksen peruminen.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Pitääkö minun vaihtaa junaa?",
                "Vaihdon tarpeen kysyminen valmiina asiointi-ilmauksena.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Miltä laiturilta juna lähtee?",
                "Oikean lähtölaiturin selvittäminen.",
                "neutral",
                "a2-unit-3",
            ),
            PhrasebookEntry(
                "Voitko näyttää reitin kartalta?",
                "Reittiohjeen pyytäminen visuaalisesti.",
                "neutral",
                "a2-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-work-study-a2",
        "A2",
        "Työpäivä ja opintojen hoitaminen",
        "📚",
        [
            PhrasebookEntry(
                "Lähetin hakemuksen eilen.",
                "Hakemuksen lähetysajan vahvistaminen.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "En päässyt eilen tunnille.",
                "Menneen poissaolon kertominen opettajalle.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Mitä tehtäviä teimme viimeksi?",
                "Edellisen oppitunnin sisällön kysyminen.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Voinko palauttaa tehtävän huomenna?",
                "Lisäajan pyytäminen tehtävälle.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "Kokous alkoi jo kello yhdeksän.",
                "Menneen aloitusajan kertominen työkaverille.",
                "neutral",
                "a2-unit-4",
            ),
            PhrasebookEntry(
                "En saanut viestiäsi.",
                "Ilmoitus siitä, ettei aiempi viesti tullut perille.",
                "neutral",
                "a2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-health-a2",
        "A2",
        "Oireista ja hoidosta kertominen",
        "🩺",
        [
            PhrasebookEntry(
                "Olen yskinyt kolme päivää.",
                "Oireen ja sen keston kertominen hoitajalle.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Minulla on ollut kuumetta.",
                "Viimeaikaisen oireen kuvaaminen vastaanotolla.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "En ole vielä ottanut lääkettä.",
                "Lääkkeen käytön tilanteen kertominen ammattilaiselle.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Olen allerginen penisilliinille.",
                "Tunnetun lääkeallergian ilmoittaminen hoitohenkilökunnalle.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Kuinka usein tätä lääkettä otetaan?",
                "Annosteluohjeen kysyminen valmiina apteekki-ilmauksena.",
                "neutral",
                "a2-unit-5",
            ),
            PhrasebookEntry(
                "Olen varannut ajan hammaslääkärille.",
                "Hammashoidon järjestämisestä kertominen.",
                "neutral",
                "a2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-outdoors-a2",
        "A2",
        "Retkellä ja yhteisissä menoissa",
        "🌲",
        [
            PhrasebookEntry(
                "Tämä reitti on lyhyempi kuin toinen.",
                "Kahden reittivaihtoehdon vertaaminen.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Ota lämmin takki mukaan.",
                "Yhdelle retkikumppanille annettu pukeutumisohje.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Älä mene heikolle jäälle.",
                "Vaarallisesta paikasta varoittaminen.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Odota minua risteyksessä.",
                "Tapaamispaikan sopiminen yhdelle matkakumppanille.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Onko konserttiin vielä lippuja?",
                "Pääsylippujen saatavuuden kysyminen.",
                "neutral",
                "a2-unit-6",
            ),
            PhrasebookEntry(
                "Valitse sinä tällä kertaa.",
                "Valinnan jättäminen ystävän tehtäväksi.",
                "neutral",
                "a2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-arrangements-a2",
        "A2",
        "Lupa, esteet ja yhteiset päätökset",
        "💬",
        [
            PhrasebookEntry(
                "Saanko käyttää tätä tietokonetta?",
                "Luvan pyytäminen laitteen käyttöön.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Minun täytyy lähteä aikaisemmin.",
                "Oman aikataulurajoituksen kertominen.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Sinun ei tarvitse tuoda mitään.",
                "Vieraalle kertominen, ettei tuomisia odoteta.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Soitan, kun olen perillä.",
                "Yhteydenoton lupaaminen saapumisen jälkeen.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "Jos sataa, voimme tavata sisällä.",
                "Varasuunnitelman ehdottaminen sään varalle.",
                "neutral",
                "a2-unit-7",
            ),
            PhrasebookEntry(
                "En pääse mukaan, koska olen töissä.",
                "Kutsusta kieltäytyminen ja syyn kertominen.",
                "neutral",
                "a2-unit-7",
            ),
        ],
    ),
]
