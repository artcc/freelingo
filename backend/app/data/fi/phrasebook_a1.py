"""Finnish A1 phrases for first encounters and everyday needs."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

A1_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "fi-greetings-a1",
        "A1",
        "Tervehtiminen ja esittäytyminen",
        "👋",
        [
            PhrasebookEntry(
                "Hei!", "Tavallinen tervehdys kohtaamisen alussa.", "neutral", "a1-unit-1"
            ),
            PhrasebookEntry("Hyvää huomenta!", "Tervehdys aamulla.", "neutral", "a1-unit-1"),
            PhrasebookEntry(
                "Hyvää päivää!", "Kohtelias tervehdys päiväsaikaan.", "formal", "a1-unit-1"
            ),
            PhrasebookEntry(
                "Minun nimeni on Aino.",
                "Oman nimen kertominen ensimmäisessä tapaamisessa.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Hauska tutustua.",
                "Ystävällinen vastaus uuden ihmisen esittelyyn.",
                "neutral",
                "a1-unit-1",
            ),
            PhrasebookEntry(
                "Näkemiin!", "Kohtelias hyvästely tapaamisen lopussa.", "neutral", "a1-unit-1"
            ),
            PhrasebookEntry(
                "Kiitos!", "Kiittäminen saadusta avusta tai palvelusta.", "neutral", "a1-unit-1"
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-home-a1",
        "A1",
        "Kotona ja kylässä",
        "🏠",
        [
            PhrasebookEntry(
                "Tervetuloa!", "Vieraan vastaanottaminen kotiin.", "neutral", "a1-unit-2"
            ),
            PhrasebookEntry(
                "Tämä on minun perheeni.",
                "Perheen esitteleminen vieraalle.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Tässä on sinun huoneesi.",
                "Vieraalle varatun huoneen näyttäminen.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Kenen laukku tämä on?", "Laukun omistajan selvittäminen.", "neutral", "a1-unit-2"
            ),
            PhrasebookEntry(
                "Tämä on ystäväni Eero.",
                "Ystävän esitteleminen toiselle ihmiselle.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Kylpyhuone on tuolla.",
                "Peseytymistilan osoittaminen vieraalle.",
                "neutral",
                "a1-unit-2",
            ),
            PhrasebookEntry(
                "Onpa kaunis koti!",
                "Vierailijan ystävällinen huomio asunnosta.",
                "neutral",
                "a1-unit-2",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-learning-a1",
        "A1",
        "Kielen oppiminen ja ymmärtäminen",
        "💬",
        [
            PhrasebookEntry(
                "Opiskelen suomea.",
                "Oman opiskelun kertominen keskustelukumppanille.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "En ymmärrä.",
                "Ilmoitus siitä, että viesti jäi epäselväksi.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Hitaammin, kiitos.", "Lyhyt pyyntö vähentää puhenopeutta.", "neutral", "a1-unit-3"
            ),
            PhrasebookEntry(
                "Sanotko sen uudestaan?",
                "Pyyntö toistaa juuri sanottu asia.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Mitä tämä sana tarkoittaa?",
                "Tuntemattoman sanan merkityksen kysyminen.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "En puhu vielä hyvin suomea.",
                "Oman kielitaidon kuvaaminen keskustelun alussa.",
                "neutral",
                "a1-unit-3",
            ),
            PhrasebookEntry(
                "Puhutko englantia?",
                "Yhteisen apukielen kysyminen tarvittaessa.",
                "neutral",
                "a1-unit-3",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-cafe-a1",
        "A1",
        "Kahvilassa ja kassalla",
        "☕",
        [
            PhrasebookEntry(
                "Yksi kahvi, kiitos.",
                "Yksinkertainen juomatilaus kahvilassa.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Kaksi teetä, kiitos.",
                "Kahden juoman tilaaminen samalla kertaa.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Paljonko tämä maksaa?", "Tuotteen hinnan kysyminen.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Voinko maksaa kortilla?",
                "Maksutavan varmistaminen kassalla.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Kuitti, kiitos.",
                "Maksutositteen pyytäminen ostoksen jälkeen.",
                "neutral",
                "a1-unit-4",
            ),
            PhrasebookEntry(
                "Ilman maitoa, kiitos.", "Juoman tilaaminen ilman maitoa.", "neutral", "a1-unit-4"
            ),
            PhrasebookEntry(
                "Onko teillä vettä?",
                "Juoman saatavuuden kysyminen palvelutilanteessa.",
                "neutral",
                "a1-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-directions-a1",
        "A1",
        "Kaupungissa liikkuminen",
        "🚌",
        [
            PhrasebookEntry(
                "Missä asema on?", "Rautatieaseman sijainnin kysyminen.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry(
                "Meneekö tämä bussi keskustaan?",
                "Bussin määränpään varmistaminen ennen nousua.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Yksi lippu Turkuun, kiitos.", "Yhden matkalipun ostaminen.", "neutral", "a1-unit-5"
            ),
            PhrasebookEntry(
                "Onko kirjasto lähellä?",
                "Kävelymatkan pituuden selvittäminen.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Olen nyt asemalla.",
                "Oman sijainnin kertominen odottavalle ystävälle.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Mistä tämä juna lähtee?",
                "Junan lähtöpaikan kysyminen asemalla.",
                "neutral",
                "a1-unit-5",
            ),
            PhrasebookEntry(
                "Anteeksi, onko tämä paikka vapaa?",
                "Istumapaikan kysyminen toiselta matkustajalta.",
                "neutral",
                "a1-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-meeting-a1",
        "A1",
        "Tapaamisen sopiminen",
        "🕒",
        [
            PhrasebookEntry(
                "Mitä kello on?", "Nykyisen kellonajan kysyminen.", "neutral", "a1-unit-6"
            ),
            PhrasebookEntry(
                "Mihin aikaan kurssi alkaa?",
                "Opetuksen alkamisajan kysyminen.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Sopiiko huomenna?",
                "Seuraavan päivän ehdottaminen tapaamiseen.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Tavataanko kello kuusi?",
                "Kellonajan ehdottaminen valmiina kysymysilmauksena.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Nähdään perjantaina!",
                "Sovitun tapaamispäivän vahvistaminen hyvästelyssä.",
                "neutral",
                "a1-unit-6",
            ),
            PhrasebookEntry(
                "Olen vapaa illalla.", "Omasta vapaasta ajasta kertominen.", "neutral", "a1-unit-6"
            ),
            PhrasebookEntry(
                "Tulen vähän myöhemmin.",
                "Ilmoitus pienestä muutoksesta saapumisaikaan.",
                "neutral",
                "a1-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "fi-help-a1",
        "A1",
        "Avun pyytäminen ja vointi",
        "🩺",
        [
            PhrasebookEntry(
                "Voitko auttaa minua?",
                "Yleinen avunpyyntö toiselle ihmiselle.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Tarvitsen lääkärin apua.", "Hoidon tarpeesta kertominen.", "neutral", "a1-unit-7"
            ),
            PhrasebookEntry(
                "Minun vatsani on kipeä.",
                "Kivun paikan kuvaaminen hoitajalle.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Minulla on jano.", "Juoman tarpeen kertominen.", "neutral", "a1-unit-7"
            ),
            PhrasebookEntry(
                "Haluan levätä hetken.",
                "Lyhyen levon tarpeen ilmaiseminen.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "Voitko soittaa numeroon 112?",
                "Toisen pyytäminen soittamaan hätänumeroon kiireellisessä hätätilanteessa.",
                "neutral",
                "a1-unit-7",
            ),
            PhrasebookEntry(
                "En voi tulla tänään, mutta voin tulla huomenna.",
                "Esteen kertominen ja uuden ajankohdan ehdottaminen.",
                "neutral",
                "a1-unit-7",
            ),
        ],
    ),
]
