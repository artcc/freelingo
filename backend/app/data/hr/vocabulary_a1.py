"""Croatian A1 vocabulary with contextual definitions and examples."""

from app.data._types import VocabularyEntry, VocabularySet

A1_SETS: list[VocabularySet] = [
    VocabularySet(
        "hr_first_contact_a1",
        "A1",
        "Prvi susret i osobni podatci",
        "a1-unit-1",
        [
            VocabularyEntry("ime", "noun", "Osobni naziv, primjerice Ana.", "Moje ime je Ana."),
            VocabularyEntry(
                "prezime", "noun", "Obiteljski naziv uz osobno ime.", "Moje prezime je Horvat."
            ),
            VocabularyEntry("osoba", "noun", "Jedan čovjek.", "Tko je ta osoba?"),
            VocabularyEntry(
                "muškarac", "noun", "Odrasla osoba muškog spola.", "Ovo je mlad muškarac."
            ),
            VocabularyEntry(
                "žena", "noun", "Odrasla osoba ženskog spola.", "Ta žena je učiteljica."
            ),
            VocabularyEntry(
                "prijatelj",
                "noun",
                "Muška osoba s kojom smo bliski i kojoj vjerujemo.",
                "Ivan je moj prijatelj.",
            ),
            VocabularyEntry(
                "prijateljica",
                "noun",
                "Ženska osoba s kojom smo bliski i kojoj vjerujemo.",
                "Ovo je moja prijateljica Maja.",
            ),
            VocabularyEntry("učenik", "noun", "Muška osoba koja uči u školi.", "Marko je učenik."),
            VocabularyEntry(
                "učenica", "noun", "Ženska osoba koja uči u školi.", "Petra je učenica."
            ),
            VocabularyEntry(
                "učitelj", "noun", "Muška osoba koja poučava učenike.", "Naš učitelj je Ivan."
            ),
            VocabularyEntry(
                "učiteljica", "noun", "Ženska osoba koja poučava učenike.", "Ana je učiteljica."
            ),
            VocabularyEntry(
                "jezik",
                "noun",
                "Sustav riječi kojim ljudi govore i pišu.",
                "Hrvatski je moj prvi jezik.",
            ),
            VocabularyEntry(
                "riječ", "noun", "Dio jezika koji ima značenje.", "Što znači ova riječ?"
            ),
            VocabularyEntry(
                "slovo", "noun", "Pisani znak u abecedi.", "Č je slovo hrvatske abecede."
            ),
            VocabularyEntry("glas", "noun", "Zvuk koji izgovaramo pri govoru.", "Ponovite glas š."),
            VocabularyEntry(
                "pitanje", "noun", "Ono što kažemo kada tražimo informaciju.", "Imam jedno pitanje."
            ),
            VocabularyEntry("odgovor", "noun", "Ono što kažemo na pitanje.", "Moj odgovor je da."),
            VocabularyEntry(
                "pozdrav",
                "noun",
                "Riječi pri susretu ili rastanku.",
                "Dobar dan je uljudan pozdrav.",
            ),
            VocabularyEntry(
                "hvala", "phrase", "Riječ kojom izražavamo zahvalnost.", "Hvala na pomoći."
            ),
            VocabularyEntry("molim", "phrase", "Riječ za uljudnu molbu.", "Ponovite, molim."),
            VocabularyEntry("da", "phrase", "Potvrdan odgovor.", "Da, ja sam Ana."),
            VocabularyEntry("ne", "phrase", "Niječan odgovor.", "Ne, nisam Ivan."),
            VocabularyEntry(
                "Hrvatska",
                "noun",
                "Država čiji je glavni grad Zagreb.",
                "Hrvatska je moja zemlja.",
            ),
            VocabularyEntry(
                "hrvatski",
                "adverb",
                "Na jeziku koji je službeni u Hrvatskoj.",
                "Govorim hrvatski.",
            ),
            VocabularyEntry(
                "adresa", "noun", "Podatak o ulici i kućnom broju.", "Moja adresa je Ilica 12."
            ),
            VocabularyEntry(
                "broj", "noun", "Oznaka količine ili redoslijeda.", "Koji je vaš telefonski broj?"
            ),
            VocabularyEntry("telefon", "noun", "Uređaj za pozive i poruke.", "Ovo je moj telefon."),
            VocabularyEntry(
                "dobro", "adverb", "Na zadovoljavajući način; ne loše.", "Dobro sam, hvala."
            ),
        ],
    ),
    VocabularySet(
        "hr_people_home_a1",
        "A1",
        "Obitelj, dom i osobne stvari",
        "a1-unit-2",
        [
            VocabularyEntry(
                "obitelj",
                "noun",
                "Roditelji, djeca i drugi bliski srodnici.",
                "Moja obitelj je mala.",
            ),
            VocabularyEntry("majka", "noun", "Ženski roditelj.", "Moja majka se zove Marija."),
            VocabularyEntry("otac", "noun", "Muški roditelj.", "Moj otac je liječnik."),
            VocabularyEntry(
                "brat",
                "noun",
                "Muška osoba s kojom imamo barem jednog zajedničkog roditelja.",
                "Moj brat je učenik.",
            ),
            VocabularyEntry(
                "sestra",
                "noun",
                "Ženska osoba s kojom imamo barem jednog zajedničkog roditelja.",
                "Moja sestra je kod kuće.",
            ),
            VocabularyEntry("dijete", "noun", "Vrlo mlada osoba.", "Dijete spava."),
            VocabularyEntry(
                "baka", "noun", "Majka naše majke ili našeg oca.", "Baka se zove Ruža."
            ),
            VocabularyEntry("djed", "noun", "Otac naše majke ili našeg oca.", "Moj djed čita."),
            VocabularyEntry("roditelji", "noun", "Majka i otac.", "Moji roditelji žive u Splitu."),
            VocabularyEntry("muž", "noun", "Muškarac s kojim je osoba u braku.", "Ovo je moj muž."),
            VocabularyEntry(
                "supruga", "noun", "Žena s kojom je osoba u braku.", "Moja supruga je učiteljica."
            ),
            VocabularyEntry(
                "dom", "noun", "Mjesto gdje živimo i osjećamo pripadnost.", "Ovdje je naš dom."
            ),
            VocabularyEntry("kuća", "noun", "Zgrada za stanovanje.", "Naša kuća ima mali vrt."),
            VocabularyEntry(
                "stan", "noun", "Prostor za stanovanje, često dio zgrade.", "Ovo je moj stan."
            ),
            VocabularyEntry("soba", "noun", "Prostorija u kući ili stanu.", "Moja soba je velika."),
            VocabularyEntry("kuhinja", "noun", "Prostorija za pripremu hrane.", "Kuhinja je mala."),
            VocabularyEntry(
                "kupaonica", "noun", "Prostorija za pranje i tuširanje.", "Gdje je kupaonica?"
            ),
            VocabularyEntry(
                "vrata", "noun", "Dio koji otvaramo pri ulasku u prostoriju.", "Vrata su otvorena."
            ),
            VocabularyEntry(
                "prozor", "noun", "Otvor sa staklom kroz koji ulazi svjetlo.", "Prozor je zatvoren."
            ),
            VocabularyEntry(
                "stol", "noun", "Komad namještaja na kojem jedemo ili radimo.", "Stol je velik."
            ),
            VocabularyEntry(
                "stolac", "noun", "Komad namještaja za sjedenje jedne osobe.", "Ovaj stolac je nov."
            ),
            VocabularyEntry(
                "krevet", "noun", "Komad namještaja za spavanje.", "Ovo je moj krevet."
            ),
            VocabularyEntry("ključ", "noun", "Predmet kojim otključavamo vrata.", "Imam ključ."),
            VocabularyEntry(
                "torba", "noun", "Predmet u kojem nosimo osobne stvari.", "To je moja torba."
            ),
            VocabularyEntry(
                "knjiga", "noun", "Povezane stranice s tekstom ili slikama.", "Knjiga je na stolu."
            ),
            VocabularyEntry(
                "velik", "adjective", "Koji zauzima mnogo prostora.", "Naš stan je velik."
            ),
            VocabularyEntry(
                "malen", "adjective", "Koji zauzima malo prostora.", "Ovaj stol je malen."
            ),
            VocabularyEntry(
                "nov", "adjective", "Koji još nije dugo u uporabi.", "Moj telefon je nov."
            ),
        ],
    ),
    VocabularySet(
        "hr_daily_life_a1",
        "A1",
        "Svakodnevne radnje i prvi brojevi",
        "a1-unit-3",
        [
            VocabularyEntry(
                "biti", "verb", "Postojati ili nalaziti se u nekom stanju.", "Danas sam kod kuće."
            ),
            VocabularyEntry("imati", "verb", "Posjedovati nešto.", "Imam novi telefon."),
            VocabularyEntry(
                "raditi", "verb", "Obavljati posao ili neku aktivnost.", "Radim u školi."
            ),
            VocabularyEntry("učiti", "verb", "Stjecati znanje ili vještinu.", "Učimo hrvatski."),
            VocabularyEntry(
                "čitati", "verb", "Razumijevati napisane riječi.", "Čitam kratku poruku."
            ),
            VocabularyEntry("pisati", "verb", "Bilježiti riječi slovima.", "Pišem svoje ime."),
            VocabularyEntry(
                "slušati", "verb", "Usmjeravati pozornost na zvuk ili govor.", "Slušam učiteljicu."
            ),
            VocabularyEntry(
                "govoriti", "verb", "Izražavati se riječima naglas.", "Govorite li hrvatski?"
            ),
            VocabularyEntry("razumjeti", "verb", "Znati što nešto znači.", "Razumijem pitanje."),
            VocabularyEntry("jesti", "verb", "Uzimati hranu.", "Ujutro jedem kruh."),
            VocabularyEntry("piti", "verb", "Uzimati tekućinu.", "Pijem vodu."),
            VocabularyEntry("spavati", "verb", "Odmarati se u snu.", "Noću spavam."),
            VocabularyEntry("jutro", "noun", "Početni dio dana nakon noći.", "Svako jutro učim."),
            VocabularyEntry("dan", "noun", "Razdoblje od 24 sata.", "Danas je lijep dan."),
            VocabularyEntry("večer", "noun", "Dio dana prije noći.", "Svaku večer čitam."),
            VocabularyEntry(
                "noć", "noun", "Tamni dio dana između večeri i jutra.", "Noć je mirna."
            ),
            VocabularyEntry("danas", "adverb", "Ovoga dana.", "Danas ne radim."),
            VocabularyEntry("sada", "adverb", "U ovom trenutku.", "Sada pišem poruku."),
            VocabularyEntry("nula", "numeral", "Broj 0.", "Telefonski broj počinje nulom."),
            VocabularyEntry("jedan", "numeral", "Broj 1.", "Imam jedan ključ."),
            VocabularyEntry("dva", "numeral", "Broj 2.", "Ovdje su dva stolca."),
            VocabularyEntry("tri", "numeral", "Broj 3.", "Imamo tri sobe."),
            VocabularyEntry("četiri", "numeral", "Broj 4.", "U sobi su četiri osobe."),
            VocabularyEntry("pet", "numeral", "Broj 5.", "Čitam pet minuta."),
            VocabularyEntry("šest", "numeral", "Broj 6.", "Sada je šest sati."),
            VocabularyEntry("sedam", "numeral", "Broj 7.", "Tjedan ima sedam dana."),
            VocabularyEntry("osam", "numeral", "Broj 8.", "Radim osam sati."),
            VocabularyEntry("devet", "numeral", "Broj 9.", "Autobus ima broj devet."),
        ],
    ),
    VocabularySet(
        "hr_food_shopping_a1",
        "A1",
        "Hrana, piće i kupnja",
        "a1-unit-4",
        [
            VocabularyEntry(
                "kruh", "noun", "Pečena hrana od brašna, vode i drugih sastojaka.", "Kupujem kruh."
            ),
            VocabularyEntry(
                "mlijeko", "noun", "Bijela tekućina, često od krave.", "Želim toplo mlijeko."
            ),
            VocabularyEntry("voda", "noun", "Prozirna tekućina potrebna za život.", "Molim vodu."),
            VocabularyEntry(
                "kava", "noun", "Napitak od prženih i mljevenih zrna.", "Pijem kavu bez šećera."
            ),
            VocabularyEntry(
                "čaj", "noun", "Topli napitak od listova, cvjetova ili plodova.", "Čaj je vruć."
            ),
            VocabularyEntry(
                "sok", "noun", "Napitak od voća ili povrća.", "Imate li sok od jabuke?"
            ),
            VocabularyEntry(
                "sir", "noun", "Čvrsta ili meka hrana od mlijeka.", "Kupujem kruh i sir."
            ),
            VocabularyEntry(
                "jaje", "noun", "Hrana s ljuskom, bjelanjkom i žumanjkom.", "Za doručak jedem jaje."
            ),
            VocabularyEntry(
                "meso", "noun", "Dio životinje koji se upotrebljava za hranu.", "Ne jedem meso."
            ),
            VocabularyEntry(
                "riba", "noun", "Životinja koja živi u vodi; također hrana.", "Za ručak imamo ribu."
            ),
            VocabularyEntry(
                "juha", "noun", "Tekuće jelo koje se jede žlicom.", "Ova juha je topla."
            ),
            VocabularyEntry(
                "salata", "noun", "Jelo od povrća, često bez kuhanja.", "Želim malu salatu."
            ),
            VocabularyEntry(
                "jabuka", "noun", "Okruglo voće crvene, zelene ili žute boje.", "Jedem jabuku."
            ),
            VocabularyEntry(
                "banana", "noun", "Duguljasto voće sa žutom korom.", "Ova banana je zrela."
            ),
            VocabularyEntry(
                "krumpir", "noun", "Povrće čiji jestivi dio raste pod zemljom.", "Kuham krumpir."
            ),
            VocabularyEntry(
                "rajčica",
                "noun",
                "Sočan, obično crven plod za salatu ili umak.",
                "Rajčica je svježa.",
            ),
            VocabularyEntry(
                "šećer", "noun", "Slatki sastojak koji dodajemo hrani i piću.", "Ne trebam šećer."
            ),
            VocabularyEntry("sol", "noun", "Bijeli slani začin.", "Molim malo soli."),
            VocabularyEntry("doručak", "noun", "Prvi obrok u danu.", "Doručak je u osam."),
            VocabularyEntry("ručak", "noun", "Glavni obrok oko sredine dana.", "Ručak je spreman."),
            VocabularyEntry("večera", "noun", "Obrok koji jedemo navečer.", "Večera je u sedam."),
            VocabularyEntry(
                "račun",
                "noun",
                "Zapis kupljenih stvari ili usluga i njihove cijene.",
                "Račun, molim.",
            ),
            VocabularyEntry(
                "cijena", "noun", "Iznos koji treba platiti.", "Koja je cijena ove kave?"
            ),
            VocabularyEntry(
                "euro",
                "noun",
                "Novčana jedinica koja se koristi u Hrvatskoj.",
                "To košta jedan euro.",
            ),
            VocabularyEntry(
                "novac", "noun", "Ono čime plaćamo robu i usluge.", "Imam novac za ručak."
            ),
            VocabularyEntry(
                "kartica",
                "noun",
                "Mali predmet kojim možemo elektronički platiti.",
                "Gdje je kartica?",
            ),
            VocabularyEntry("kupiti", "verb", "Dobiti nešto uz plaćanje.", "Želim kupiti jabuku."),
            VocabularyEntry("deset", "numeral", "Broj 10.", "Račun je deset eura."),
        ],
    ),
    VocabularySet(
        "hr_places_transport_a1",
        "A1",
        "Mjesta i prijevoz",
        "a1-unit-5",
        [
            VocabularyEntry(
                "grad", "noun", "Veće naselje s mnogo zgrada i ulica.", "Zagreb je velik grad."
            ),
            VocabularyEntry(
                "selo", "noun", "Manje naselje, često u prirodi.", "Moja baka živi u selu."
            ),
            VocabularyEntry("ulica", "noun", "Put između kuća u naselju.", "Ova ulica je mirna."),
            VocabularyEntry(
                "trg", "noun", "Otvoren javni prostor među zgradama.", "Vidimo se na trgu."
            ),
            VocabularyEntry(
                "park", "noun", "Zelena površina za odmor i šetnju.", "Djeca su u parku."
            ),
            VocabularyEntry("škola", "noun", "Mjesto gdje učenici uče.", "Idem u školu."),
            VocabularyEntry(
                "trgovina", "noun", "Mjesto gdje kupujemo proizvode.", "Trgovina je otvorena."
            ),
            VocabularyEntry(
                "tržnica",
                "noun",
                "Mjesto s više prodajnih mjesta, često za hranu.",
                "Idem na tržnicu.",
            ),
            VocabularyEntry(
                "banka",
                "noun",
                "Ustanova koja čuva novac i pruža novčane usluge.",
                "Ana je u banci.",
            ),
            VocabularyEntry("pošta", "noun", "Mjesto za slanje pisama i paketa.", "Gdje je pošta?"),
            VocabularyEntry(
                "hotel", "noun", "Zgrada u kojoj gosti plaćaju smještaj.", "Naš hotel je blizu."
            ),
            VocabularyEntry(
                "restoran",
                "noun",
                "Mjesto gdje naručujemo i jedemo pripremljena jela.",
                "Restoran radi.",
            ),
            VocabularyEntry(
                "kolodvor",
                "noun",
                "Mjesto polaska i dolaska vlakova ili autobusa.",
                "Idem na kolodvor.",
            ),
            VocabularyEntry(
                "stajalište",
                "noun",
                "Označeno mjesto gdje javno vozilo staje.",
                "Čekam na stajalištu.",
            ),
            VocabularyEntry(
                "autobus", "noun", "Cestovno vozilo za mnogo putnika.", "Autobus dolazi."
            ),
            VocabularyEntry(
                "tramvaj",
                "noun",
                "Gradsko vozilo koje vozi po tračnicama.",
                "Tramvaj broj šest staje.",
            ),
            VocabularyEntry(
                "vlak", "noun", "Vozilo s vagonima koje vozi željeznicom.", "Vlak ide u Split."
            ),
            VocabularyEntry(
                "automobil", "noun", "Cestovno vozilo za nekoliko osoba.", "Ovo je naš automobil."
            ),
            VocabularyEntry(
                "bicikl", "noun", "Vozilo s dva kotača koje pokrećemo nogama.", "Imam novi bicikl."
            ),
            VocabularyEntry(
                "karta", "noun", "Potvrda za putovanje ili ulazak.", "Trebam kartu za vlak."
            ),
            VocabularyEntry(
                "putovnica",
                "noun",
                "Osobna isprava za putovanje u druge države.",
                "Imam putovnicu.",
            ),
            VocabularyEntry("more", "noun", "Velika površina slane vode.", "More je danas mirno."),
            VocabularyEntry("plaža", "noun", "Dio obale za kupanje i odmor.", "Idemo na plažu."),
            VocabularyEntry(
                "lijevo",
                "adverb",
                "Na strani tijela na kojoj je obično srce ili prema toj strani.",
                "Skrenite lijevo.",
            ),
            VocabularyEntry(
                "desno",
                "adverb",
                "Na strani tijela suprotnoj od one na kojoj je obično srce "
                "ili prema toj strani.",
                "Banka je desno.",
            ),
            VocabularyEntry("ravno", "adverb", "Naprijed, bez skretanja.", "Idite ravno."),
            VocabularyEntry("blizu", "adverb", "Na maloj udaljenosti.", "Hotel je blizu."),
            VocabularyEntry("daleko", "adverb", "Na velikoj udaljenosti.", "Kolodvor nije daleko."),
        ],
    ),
    VocabularySet(
        "hr_time_leisure_a1",
        "A1",
        "Kalendar, vrijeme i slobodne aktivnosti",
        "a1-unit-6",
        [
            VocabularyEntry("ponedjeljak", "noun", "Dan nakon nedjelje.", "U ponedjeljak radim."),
            VocabularyEntry(
                "utorak", "noun", "Dan između ponedjeljka i srijede.", "Utorak je slobodan."
            ),
            VocabularyEntry(
                "srijeda", "noun", "Dan između utorka i četvrtka.", "Vidimo se u srijedu."
            ),
            VocabularyEntry("četvrtak", "noun", "Dan prije petka.", "U četvrtak imam tečaj."),
            VocabularyEntry("petak", "noun", "Dan nakon četvrtka.", "Danas je petak."),
            VocabularyEntry(
                "subota", "noun", "Dan između petka i nedjelje.", "U subotu idem na plažu."
            ),
            VocabularyEntry("nedjelja", "noun", "Dan nakon subote.", "Nedjelja je dan za odmor."),
            VocabularyEntry(
                "tjedan", "noun", "Razdoblje od sedam dana.", "Ovaj tjedan učim hrvatski."
            ),
            VocabularyEntry(
                "mjesec",
                "noun",
                "Jedno od dvanaest razdoblja u godini.",
                "Siječanj je prvi mjesec.",
            ),
            VocabularyEntry(
                "godina",
                "noun",
                "Razdoblje od dvanaest mjeseci.",
                "Nova godina počinje u siječnju.",
            ),
            VocabularyEntry(
                "sat",
                "noun",
                "Razdoblje od šezdeset minuta; uređaj za mjerenje vremena.",
                "Imam sat.",
            ),
            VocabularyEntry("minuta", "noun", "Šezdeseti dio sata.", "Čekam pet minuta."),
            VocabularyEntry("sutra", "adverb", "Sljedećeg dana.", "Sutra ne radim."),
            VocabularyEntry(
                "vikend", "noun", "Subota i nedjelja kao kraj tjedna.", "Za vikend se odmaram."
            ),
            VocabularyEntry(
                "vrijeme", "noun", "Trajanje ili slobodni dio dana.", "Imam vremena za šetnju."
            ),
            VocabularyEntry(
                "odmor", "noun", "Vrijeme bez rada radi povratka snage.", "Trebam kratak odmor."
            ),
            VocabularyEntry(
                "glazba", "noun", "Zvukovi povezani melodijom i ritmom.", "Slušam glazbu."
            ),
            VocabularyEntry("film", "noun", "Priča prikazana pokretnim slikama.", "Gledamo film."),
            VocabularyEntry(
                "sport", "noun", "Tjelesna aktivnost s pravilima.", "Nogomet je popularan sport."
            ),
            VocabularyEntry(
                "šetnja", "noun", "Lagano hodanje radi odmora ili uživanja.", "Idemo u šetnju."
            ),
            VocabularyEntry(
                "društvo", "noun", "Ljudi s kojima provodimo vrijeme.", "Volim tvoje društvo."
            ),
            VocabularyEntry(
                "sunce", "noun", "Zvijezda koja nam daje svjetlost i toplinu.", "Danas sja sunce."
            ),
            VocabularyEntry("kiša", "noun", "Voda koja pada iz oblaka u kapima.", "Pada kiša."),
            VocabularyEntry(
                "toplo", "adverb", "Uz ugodnu ili povišenu temperaturu.", "Danas je toplo."
            ),
            VocabularyEntry("hladno", "adverb", "Uz nisku temperaturu.", "Ujutro je hladno."),
            VocabularyEntry("igrati", "verb", "Sudjelovati u igri ili sportu.", "Igram nogomet."),
            VocabularyEntry("plesati", "verb", "Pomicati tijelo u ritmu glazbe.", "Volim plesati."),
            VocabularyEntry(
                "odmarati se", "verb", "Prekidati rad radi povratka snage.", "Nedjeljom se odmaram."
            ),
        ],
    ),
    VocabularySet(
        "hr_health_help_a1",
        "A1",
        "Zdravlje, potrebe i pomoć",
        "a1-unit-7",
        [
            VocabularyEntry(
                "pomoć", "noun", "Podrška osobi koja nešto ne može sama.", "Trebam pomoć."
            ),
            VocabularyEntry(
                "liječnik", "noun", "Muška osoba koja liječi bolesnike.", "Liječnik je ovdje."
            ),
            VocabularyEntry(
                "liječnica",
                "noun",
                "Ženska osoba koja liječi bolesnike.",
                "Moja liječnica radi danas.",
            ),
            VocabularyEntry(
                "ljekarna",
                "noun",
                "Mjesto gdje dobivamo ili kupujemo lijekove.",
                "Gdje je ljekarna?",
            ),
            VocabularyEntry(
                "bolnica", "noun", "Ustanova za liječenje i njegu bolesnika.", "Idemo u bolnicu."
            ),
            VocabularyEntry(
                "lijek", "noun", "Sredstvo za liječenje ili ublažavanje bolesti.", "Trebam lijek."
            ),
            VocabularyEntry("bol", "noun", "Neugodan osjećaj u tijelu.", "Osjećam bol u nozi."),
            VocabularyEntry(
                "glava", "noun", "Dio tijela s očima, ušima, nosom i ustima.", "Boli me glava."
            ),
            VocabularyEntry("zub", "noun", "Tvrdi dio u ustima za žvakanje.", "Boli me zub."),
            VocabularyEntry(
                "ruka", "noun", "Dio tijela od ramena do prstiju.", "Desna ruka me boli."
            ),
            VocabularyEntry(
                "noga", "noun", "Dio tijela kojim stojimo i hodamo.", "Lijeva noga me boli."
            ),
            VocabularyEntry(
                "leđa", "noun", "Stražnji dio trupa između vrata i zdjelice.", "Bole me leđa."
            ),
            VocabularyEntry(
                "trbuh", "noun", "Prednji dio tijela ispod prsnog koša.", "Boli me trbuh."
            ),
            VocabularyEntry(
                "temperatura",
                "noun",
                "Mjera topline tijela ili okoline.",
                "Imam visoku temperaturu.",
            ),
            VocabularyEntry(
                "bolest",
                "noun",
                "Zdravstveni problem zbog kojeg se loše osjećamo ili tijelo ne radi kako treba.",
                "Gripa je česta bolest.",
            ),
            VocabularyEntry("zdrav", "adjective", "Koji nije bolestan.", "Danas sam zdrav."),
            VocabularyEntry("bolestan", "adjective", "Koji ima bolest.", "Marko je bolestan."),
            VocabularyEntry(
                "umoran", "adjective", "Koji treba odmor.", "Umoran sam i želim spavati."
            ),
            VocabularyEntry(
                "gladan", "adjective", "Koji osjeća potrebu za hranom.", "Gladan sam; trebam ručak."
            ),
            VocabularyEntry(
                "žedan", "adjective", "Koji osjeća potrebu za pićem.", "Žedan sam; molim vodu."
            ),
            VocabularyEntry(
                "hitno", "adverb", "Bez čekanja, jer je vrlo važno.", "Hitno trebam liječnika."
            ),
            VocabularyEntry(
                "opasno", "adverb", "Uz mogućnost ozljede ili štete.", "Ovdje je opasno."
            ),
            VocabularyEntry(
                "čekati", "verb", "Ostati dok netko ili nešto ne dođe.", "Čekam liječnicu."
            ),
            VocabularyEntry("trebati", "verb", "Imati potrebu za nečim.", "Trebam vodu."),
            VocabularyEntry("moći", "verb", "Imati sposobnost ili mogućnost.", "Možete li pomoći?"),
            VocabularyEntry(
                "morati", "verb", "Imati obvezu ili nužnu potrebu.", "Moram se odmoriti."
            ),
            VocabularyEntry(
                "željeti",
                "verb",
                "Htjeti nešto imati ili učiniti.",
                "Želim razgovarati s liječnikom.",
            ),
            VocabularyEntry(
                "punjač", "noun", "Uređaj koji puni bateriju.", "Trebam punjač za telefon."
            ),
        ],
    ),
]
