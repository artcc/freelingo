"""Croatian B1 grammar for narration, negotiation and connected discourse."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

B1_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "hr-narrative-aspect-b1",
        "Glagolski vid u pripovijedanju",
        "B1",
        "Glagolski vid",
        "Razlikujte radnju u tijeku od događaja prikazanog kao cjelina.",
        "Nesvršeni glagol često opisuje pozadinu događaja ili ponavljanje. Svršeni glagol "
        "prikazuje radnju kao zaokruženu cjelinu i često pomiče priču naprijed. Oba vida "
        "imaju perfekt: pisao sam i napisao sam. Sam perfekt ne jamči dovršenost radnje.",
        rules=[
            "Nesvršeni vid može označavati tijek, naviku ili iskustvo bez naglašavanja rezultata.",
            "Svršeni vid ne znači nužno kratku radnju: izgradili smo kuću može obuhvatiti godine.",
            "Parove poput čitati – pročitati učimo s njihovim značenjem, a ne samo prema prefiksu.",
        ],
        examples=[
            GrammarExample(
                "Dok sam kuhala ručak, zazvonio je telefon.",
                note="Kuhanje je pozadina, a zvonjava novi događaj.",
            ),
            GrammarExample(
                "Otvorio sam poruku, pročitao je i nazvao kolegicu.",
                note="Tri svršene radnje tvore slijed događaja.",
            ),
            GrammarExample(
                "Svake smo večeri razgovarali na balkonu.",
                note="Nesvršeni glagol opisuje ponavljanu aktivnost.",
            ),
        ],
        related=["hr-duration-result-b1", "hr-narrative-sequence-b1"],
    ),
    GrammarTopic(
        "hr-duration-result-b1",
        "Trajanje i postignuti rezultat",
        "B1",
        "Glagolski vid",
        "Recite koliko je aktivnost trajala i je li dovršena.",
        "Izrazi dva sata i cijelo jutro mogu opisati trajanje aktivnosti. Uz svršeni glagol "
        "izraz za dva sata može označavati vrijeme potrebno za dovršetak. U budućem "
        "kontekstu isti izraz može označavati trenutak koji tek dolazi: Vratit ću se za dva sata.",
        rules=[
            "Pisao sam izvještaj dva sata ne govori sam po sebi da je izvještaj gotov.",
            "Napisao sam izvještaj za dva sata potvrđuje dovršenje.",
            "Za precizan opis provjerite vid glagola i vremenski kontekst zajedno.",
        ],
        examples=[
            GrammarExample(
                "Popravljao sam bicikl cijelo jutro, ali kočnice još ne rade.",
                note="Trajanje aktivnosti nije isto što i uspješan rezultat.",
            ),
            GrammarExample(
                "Majstor je popravio bicikl za pola sata.",
                note="Navodi se vrijeme potrebno za dovršenu radnju.",
            ),
        ],
        related=["hr-narrative-aspect-b1"],
    ),
    GrammarTopic(
        "hr-narrative-sequence-b1",
        "Redoslijed i istodobnost događaja",
        "B1",
        "Vremenski odnosi",
        "Povežite događaje izrazima najprije, zatim, dok i nakon što.",
        "Najprije, zatim i naposljetku uređuju priču. Dok često povezuje istodobne radnje, "
        "a nakon što pokazuje da jedna radnja prethodi drugoj. Prije nego što označava "
        "radnju koja slijedi nakon radnje iz glavne rečenice.",
        rules=[
            "U pripovijedanju o prošlosti nakon što može stajati uz perfekt.",
            "Iza zavisne rečenice koja prethodi glavnoj pišemo zarez.",
            "Kod istodobnih aktivnosti čest je nesvršeni vid u obje rečenice.",
        ],
        examples=[
            GrammarExample(
                "Nakon što smo kupili karte, otišli smo na peron.",
                note="Kupnja karata prethodi odlasku na peron.",
            ),
            GrammarExample(
                "Dok je Ana pakirala torbu, Luka je provjeravao vozni red.",
                note="Dvije su aktivnosti trajale istodobno.",
            ),
            GrammarExample(
                "Prije nego što smo krenuli, zatvorili smo sve prozore.",
                note="Prozori su zatvoreni prije polaska.",
            ),
        ],
        related=["hr-narrative-aspect-b1"],
    ),
    GrammarTopic(
        "hr-motion-verbs-b1",
        "Kretanje, dolazak i odlazak",
        "B1",
        "Glagoli kretanja",
        "Odaberite glagol prema načinu kretanja i cilju puta.",
        "Ići je širok glagol kretanja: idem na posao može značiti pješice ili prijevozom. "
        "Hodati naglašava kretanje nogama, voziti upravljanje vozilom, a voziti se putovanje "
        "vozilom. Dolaziti – doći i odlaziti – otići razlikuju tijek ili ponavljanje od "
        "zaokruženog dolaska ili odlaska.",
        rules=[
            "Način putovanja možemo dodati: ići pješice, autobusom ili vlakom.",
            "Ići se može odnositi i na naviku: Svaki dan idem na posao autobusom.",
            "Doći označava dolazak do odredišta; otići odlazak s polazišta.",
        ],
        examples=[
            GrammarExample(
                "Svaki dan idem na posao tramvajem, a danas idem pješice.",
                note="Isti glagol prirodno opisuje naviku i današnju pojedinačnu radnju.",
            ),
            GrammarExample(
                "Vozili smo se dva sata i napokon došli u Zadar.",
                note="Voziti se opisuje putovanje, a doći ostvareni dolazak.",
            ),
            GrammarExample(
                "Ana vozi, a mi se vozimo s njom.",
                note="Ana upravlja vozilom, ostali su putnici.",
            ),
        ],
        related=["hr-narrative-aspect-b1", "hr-route-prepositions-b1"],
    ),
    GrammarTopic(
        "hr-route-prepositions-b1",
        "Opis puta prijedložnim izrazima",
        "B1",
        "Prijedlozi i padeži",
        "Opišite prolazak, smjer i odredište.",
        "Za opis puta korisni su kroz s akuzativom, preko s genitivom te prema s dativom. "
        "Do s genitivom označava granicu puta ili odredište. Izbor prijedloga mijenja "
        "prostorni odnos: kroz park znači unutar parka, a pokraj parka uz njegov rub.",
        rules=[
            "Kroz traži akuzativ: kroz tunel, kroz šumu.",
            "Preko, pokraj i do traže genitiv: preko mosta, pokraj pošte, do stanice.",
            "Prema s dativom označava smjer, ali samo po sebi ne potvrđuje dolazak.",
        ],
        examples=[
            GrammarExample(
                "Prođite kroz pothodnik pa skrenite prema kolodvoru.",
                note="Kroz opisuje prolazak, a prema daljnji smjer.",
            ),
            GrammarExample(
                "Prešli smo preko mosta i nastavili do tržnice.",
                note="Most je dio puta, a tržnica njegovo odredište.",
            ),
        ],
        related=["hr-motion-verbs-b1"],
    ),
    GrammarTopic(
        "hr-clitic-order-b1",
        "Zanaglasnice u kratkoj poruci",
        "B1",
        "Red riječi",
        "Povežite kratke oblike poput sam, mu, ga i se.",
        "Zanaglasnice, odnosno enklitike, kratki su nenaglašeni oblici poput sam, mu i ga. "
        "Ne stoje samostalno na početku izjavne rečenice. Često dolaze nakon "
        "prve naglašene riječi ili prve smislene cjeline. U čestoj skupini pomoćni glagol "
        "poput sam stoji prije zamjenica, a dativna zamjenica prije akuzativne. Oblik je "
        "ima posebno mjesto iza zamjenica: Ana mu ga je dala.",
        rules=[
            "U skupini sam mu ga oblici označavaju vrijeme, primatelja i predmet.",
            "Oblik je slijedi zamjeničke nenaglasnice: Poslao mi ga je.",
            "Uz povratno se u perfektu trećeg lica jednine je se uobičajeno izostavlja: Vratio se.",
        ],
        examples=[
            GrammarExample(
                "Kartu sam mu poslala jutros.",
                note="Zanaglasnice sam i mu slijede prvu istaknutu riječ.",
            ),
            GrammarExample(
                "Luka mi ga je pokazao na karti.",
                note="Mi prethodi ga, a pomoćno je dolazi iza njih.",
            ),
            GrammarExample(
                "Ana se vratila ranije.",
                note="Uz se ovdje nema dodatnog oblika je.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                "Sam mu poslala kartu.",
                "Poslala sam mu kartu.",
                "Nenaglašeni oblik sam ne započinje ovu samostalnu izjavnu rečenicu.",
            ),
        ],
        related=["hr-word-order-focus-b1"],
    ),
    GrammarTopic(
        "hr-conditional-first-b1",
        "Kondicional prvi: želje i uljudne molbe",
        "B1",
        "Glagolski načini",
        "Izrazite želju, prijedlog ili molbu manje izravno.",
        "Kondicional prvi tvori se oblicima bih, bi, bi, bismo, biste, bi i glagolskim "
        "pridjevom radnim. Pridjev se slaže sa subjektom u rodu i broju. Kondicional "
        "često ublažava molbu ili predstavlja mogući plan, umjesto da ga prikaže kao odluku.",
        structure="bih / bi / bi / bismo / biste / bi + glagolski pridjev radni",
        rules=[
            "Za prvo lice jednine standardni je oblik bih: Ja bih predložila drugi termin.",
            "U standardnom jeziku za mi i vi koristimo bismo i biste, a ne bi.",
            "U pitanju možemo reći Biste li ponovili? ili Možete li ponoviti?; oba su uljudna.",
        ],
        examples=[
            GrammarExample(
                "Htjela bih razgovarati o rasporedu.",
                note="Govornica izražava želju uljudnim oblikom.",
            ),
            GrammarExample(
                "Bismo li mogli početi pola sata kasnije?",
                note="Skupina predlaže promjenu, ali je još ne smatra dogovorenom.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                "Mi bi prihvatili ponudu.",
                "Mi bismo prihvatili ponudu.",
                "U standardnom jeziku prvo lice množine ima oblik bismo.",
            ),
        ],
        related=["hr-clitic-order-b1", "hr-hypothetical-conditions-b1", "hr-purpose-b1"],
    ),
    GrammarTopic(
        "hr-hypothetical-conditions-b1",
        "Zamišljeni uvjet s kad bi",
        "B1",
        "Uvjetne rečenice",
        "Razgovarajte o mogućnosti koju zamišljate.",
        "Kad bih imao više vremena, učio bih svaki dan predstavlja zamišljeni uvjet i "
        "njegovu posljedicu. U takvoj se rečenici kondicional pojavljuje u oba dijela. "
        "To nije isto što i otvoreni uvjet Ako imam vremena, doći ću, koji ostavlja "
        "stvarnu mogućnost dolaska.",
        structure="Kad + kondicional prvi, kondicional prvi.",
        rules=[
            "Oblik bih, bi, bismo ili biste određujemo zasebno prema subjektu svake rečenice.",
            "Kad bi ovdje ne govori o prošlosti; situacija može biti sadašnja ili buduća.",
            "Zamišljeni uvjet na početku odvajamo zarezom od njegove posljedice.",
        ],
        examples=[
            GrammarExample(
                "Kad bismo dobili popust, uzeli bismo dvije karte.",
                note="Govornici razmatraju kupnju pod zamišljenim uvjetom.",
            ),
            GrammarExample(
                "Kad bi ti preuzeo jutarnju smjenu, ja bih radila navečer.",
                note="Uvjet i posljedica imaju različite subjekte i oblike kondicionala.",
            ),
        ],
        related=["hr-conditional-first-b1"],
    ),
    GrammarTopic(
        "hr-purpose-b1",
        "Svrha s da i kako bi",
        "B1",
        "Namjerne rečenice",
        "Objasnite radi čega nešto poduzimate.",
        "Namjerna rečenica odgovara na pitanje S kojom svrhom? Česti su da s prezentom "
        "i kako s kondicionalom. Svrha opisuje željeni rezultat, ali ne potvrđuje da je "
        "on ostvaren. Oblik uz kako usklađuje se sa subjektom namjerne rečenice.",
        rules=[
            "Da + prezent: Došao sam ranije da razgovaramo.",
            "Kako + kondicional: Poslala sam podatke kako biste pripremili ugovor.",
            "U uobičajenoj namjernoj rečenici iza glavne ne pišemo zarez ispred da ili kako.",
        ],
        examples=[
            GrammarExample(
                "Zapisujem dogovor da nešto ne zaboravim.",
                note="Zapisivanje ima svrhu spriječiti zaboravljanje.",
            ),
            GrammarExample(
                "Promijenili smo raspored kako bismo svi mogli sudjelovati.",
                note="Bismo se odnosi na skupinu koja želi sudjelovati.",
            ),
        ],
        related=["hr-conditional-first-b1"],
    ),
    GrammarTopic(
        "hr-relative-clauses-b1",
        "Odnosne rečenice s koji",
        "B1",
        "Odnosne rečenice",
        "Precizirajte osobu ili stvar bez ponavljanja cijele imenice.",
        "Odnosna zamjenica koji slaže se s imenicom na koju se odnosi u rodu i broju, "
        "ali njezin padež ovisi o ulozi u odnosnoj rečenici. U izrazu susjeda kojoj sam pomogao "
        "oblik kojoj je dativ jer pomažemo komu. Rečenicu koja određuje o kojoj osobi "
        "ili stvari govorimo obično ne odvajamo zarezom.",
        rules=[
            "Padež zamjenice ne mora biti jednak padežu imenice ispred nje.",
            "Prijedlog ide ispred odnosne zamjenice: stan u kojem živim.",
            "Dodatnu obavijest o već određenoj osobi ili stvari odvajamo zarezima.",
        ],
        examples=[
            GrammarExample(
                "To je susjeda kojoj sam posudio ljestve.",
                note="Kojoj je dativ jer je susjeda primateljica ljestava.",
            ),
            GrammarExample(
                "Tražimo stan u kojem ima dovoljno svjetla.",
                note="U kojem označava mjesto i odnosi se na imenicu stan.",
            ),
            GrammarExample(
                "Moja sestra Ana, koja živi u Puli, dolazi sutra.",
                note="Odnosna rečenica dodaje podatak o već imenovanoj osobi.",
            ),
        ],
        related=["hr-basic-passive-b1"],
    ),
    GrammarTopic(
        "hr-passive-participles-b1",
        "Glagolski pridjev trpni u opisima",
        "B1",
        "Glagolski pridjevi",
        "Razumijte oblike poput zatvoren, popravljen i opran.",
        "Glagolski pridjev trpni opisuje predmet ili osobu na koju je radnja usmjerena. "
        "Česti su nastavci -n, -en, -jen i -t, uz promjene osnove: napisati – napisan, "
        "popraviti – popravljen, oprati – opran, otvoriti – otvoren. Oblici se uče "
        "uz glagol i slažu se s imenicom.",
        rules=[
            "Pridjev se mijenja prema rodu, broju i padežu: zatvoren prozor, zatvorena vrata.",
            "Ne postoji jedan nastavak koji se može mehanički dodati svakom glagolu.",
            "Takav opis često ističe rezultat ili stanje, bez navođenja izvršitelja.",
        ],
        examples=[
            GrammarExample(
                "U kuhinji je popravljen hladnjak.",
                note="Popravljen se slaže s imenicom hladnjak u muškom rodu jednine.",
            ),
            GrammarExample(
                "Provjerite jesu li sva vrata zatvorena.",
                note="Vrata su množinska imenica srednjeg roda pa stoji zatvorena.",
            ),
        ],
        related=["hr-basic-passive-b1"],
    ),
    GrammarTopic(
        "hr-basic-passive-b1",
        "Pasiv u obavijestima",
        "B1",
        "Pasiv",
        "Usmjerite pozornost na obavljeni posao umjesto na izvršitelja.",
        "U obavijestima se često pojavljuje biti s glagolskim pridjevom trpnim: Dizalo je "
        "popravljeno. Predmet radnje postaje subjekt rečenice. Aktiv Majstor je popravio "
        "dizalo navodi izvršitelja, dok pasiv omogućuje da ga izostavimo ako nije važan.",
        rules=[
            "Pridjev trpni slaže se s novim subjektom: Računi su plaćeni.",
            "Vrijeme izražavamo oblikom glagola biti: je popravljeno, bit će popravljeno.",
            "U svakodnevnom razgovoru aktiv je često izravniji ako je izvršitelj važan.",
        ],
        examples=[
            GrammarExample(
                "Prozori su zamijenjeni prošli tjedan.",
                note="Obavijest ističe završeni posao, a ne osobu koja ga je obavila.",
            ),
            GrammarExample(
                "Kvar će biti uklonjen do petka.",
                note="Futur najavljuje rok završetka popravka.",
            ),
        ],
        related=["hr-passive-participles-b1", "hr-relative-clauses-b1"],
    ),
    GrammarTopic(
        "hr-future-second-b1",
        "Tvorba futura drugog",
        "B1",
        "Buduća vremena",
        "Prepoznajte buduću radnju povezanu s drugom budućom radnjom.",
        "Futur drugi tvori se od budem, budeš, bude, budemo, budete, budu i glagolskog "
        "pridjeva radnog. Upotrebljava se uglavnom u zavisnim rečenicama, primjerice "
        "uz ako, kad ili dok. Ne služi kao uobičajena samostalna najava budućnosti.",
        structure="budem / budeš / bude / budemo / budete / budu + glagolski pridjev radni",
        rules=[
            "Radni pridjev slaže se sa subjektom: budeš čekala, budemo čekali.",
            "U glavnoj rečenici za običnu najavu koristimo futur prvi: Sutra ću raditi.",
            "Futur drugi sam po sebi ne znači da je radnja dovršena prije druge radnje.",
        ],
        examples=[
            GrammarExample(
                "Ako budete trebali pomoć, nazovite nas.",
                note="Budete trebali označava moguću buduću potrebu.",
            ),
            GrammarExample(
                "Dok budem čekala odgovor, pripremit ću ostale dokumente.",
                note="Budem čekala prikazuje radnju koja će trajati usporedno s pripremom.",
            ),
        ],
        related=["hr-future-time-clauses-b1"],
    ),
    GrammarTopic(
        "hr-future-time-clauses-b1",
        "Buduće radnje uz kad, čim i dok",
        "B1",
        "Vremenske rečenice",
        "Uskladite budući događaj s radnjom koja o njemu ovisi.",
        "Uz kad i čim buduću završenu radnju često izražavamo svršenim prezentom: Kad "
        "dobijem potvrdu, javit ću se. Moguć je i futur drugi: Kad budem dobio potvrdu. "
        "Dok s nesvršenim glagolom može označavati istodobno trajanje. Izbor vremena "
        "ovisi o odnosu radnji, a ne samo o vezniku.",
        rules=[
            "Svršeni prezent može imati buduće značenje u vremenskoj zavisnoj rečenici.",
            "Čim naglašava da druga radnja slijedi odmah nakon prve.",
            "Futur prvi nije uobičajen izbor u vremenskoj rečenici tipa Kad dobijem potvrdu.",
        ],
        examples=[
            GrammarExample(
                "Čim stigne rješenje, poslat ću vam presliku.",
                note="Slanje slijedi odmah nakon primitka rješenja.",
            ),
            GrammarExample(
                "Dok budete ispunjavali obrazac, provjerit ću vaše podatke.",
                note="Futur drugi s nesvršenim glagolom prikazuje istodobnu aktivnost.",
            ),
        ],
        related=["hr-future-second-b1", "hr-narrative-sequence-b1"],
    ),
    GrammarTopic(
        "hr-indirect-questions-b1",
        "Neizravna pitanja",
        "B1",
        "Zavisne rečenice",
        "Zatražite informaciju unutar uljudne molbe ili druge rečenice.",
        "Izravno pitanje Gdje je ured? možemo uključiti u molbu Recite mi gdje je ured. "
        "Pitanja bez upitne riječi često uvodimo s je li ili drugim glagolskim oblikom "
        "uz li: Zanima me radi li ured subotom. Upitnik ovisi o cijeloj rečenici.",
        rules=[
            "Zadržavamo upitnu riječ: gdje, kada, kako, koliko ili zašto.",
            "Je li pišemo odvojeno; u primjeru Zanima me je li potvrda gotova "
            "oblik je pripada glagolu biti.",
            "Izjavna rečenica Ne znam kada ured radi završava točkom.",
        ],
        examples=[
            GrammarExample(
                "Možete li mi reći kada mogu preuzeti potvrdu?",
                note="Cijela je rečenica uljudno pitanje pa završava upitnikom.",
            ),
            GrammarExample(
                "Zanima me treba li priložiti izvornik.",
                note="Li uvodi neizravno pitanje na koje je moguć odgovor da ili ne.",
            ),
        ],
        related=["hr-reported-speech-b1"],
    ),
    GrammarTopic(
        "hr-reported-speech-b1",
        "Prenošenje tuđih riječi",
        "B1",
        "Neupravni govor",
        "Prenesite poruku bez promjene njezina značenja.",
        "Izjave često prenosimo uz reći da, a pitanja uz pitati i odgovarajuću upitnu riječ "
        "ili li. Zamjenice i vremenske izraze prilagođavamo novom govorniku i trenutku. "
        "U hrvatskom nema obveznog pomicanja svih glagolskih vremena u prošlost nakon rekao je.",
        rules=[
            "Ana je rekla: Umorna sam. postaje Ana je rekla da je umorna.",
            "Sutra zamjenjujemo izrazom sljedeći dan ili imenom dana ako se promijenio trenutak.",
            "Čuvamo tko govori, kome se obraća i odnosi li se poruka na plan ili već gotovu radnju.",
        ],
        examples=[
            GrammarExample(
                "Petar je rekao da će poslati dokumente u petak.",
                note="Futur ostaje futur jer prenesena izjava najavljuje slanje.",
            ),
            GrammarExample(
                "U ponedjeljak je rekla da dolazi sljedeći dan, dakle u utorak.",
                note="Sljedeći dan čuva smisao izvornog sutra pri kasnijem prepričavanju.",
            ),
            GrammarExample(
                "Pitala me jesam li primio njezinu poruku.",
                note="Pitanje je preneseno bez navodnika i bez završnog upitnika.",
            ),
        ],
        related=["hr-indirect-questions-b1", "hr-word-order-focus-b1"],
    ),
    GrammarTopic(
        "hr-negative-concord-b1",
        "Niječne riječi u istoj rečenici",
        "B1",
        "Nijekanje",
        "Jasno izrazite odsutnost osobe, stvari ili događaja.",
        "Riječi nitko, ništa, nikad i nigdje u uobičajenoj niječnoj rečenici dolaze uz "
        "niječni glagol. Više niječnih riječi pritom ne pretvara rečenicu u potvrdnu. "
        "Uz prijedlog se zamjenice razdvajaju: ni s kim, ni o čemu, ni od koga.",
        rules=[
            "Nitko nije došao znači da nije došla nijedna osoba.",
            "Ništa nisam čuo nije isto što i Nisam sve čuo.",
            "U prijedložnom izrazu ni stoji ispred prijedloga: Nisam razgovarao ni s kim.",
        ],
        examples=[
            GrammarExample(
                "Nitko mi nije ništa javio.",
                note="Obje niječne zamjenice slažu se s niječnim glagolom.",
            ),
            GrammarExample(
                "O tome nisam razgovarala ni s kim.",
                note="Izraz ni s kim uključuje prijedlog s i instrumental kim.",
            ),
        ],
        common_mistakes=[
            GrammarMistake(
                "Nitko je poslao odgovor.",
                "Nitko nije poslao odgovor.",
                "Zamjenica nitko u ovoj rečenici zahtijeva niječni glagol.",
            ),
        ],
        related=["hr-clitic-order-b1"],
    ),
    GrammarTopic(
        "hr-word-order-focus-b1",
        "Red riječi i ispravljanje nesporazuma",
        "B1",
        "Red riječi",
        "Istaknite važan podatak bez promjene sudionika radnje.",
        "Hrvatski dopušta različit red punih rečeničnih članova. Padeži pomažu prepoznati "
        "njihove uloge. Poznatu temu često stavljamo na početak, a novu informaciju prema "
        "kraju. Za jasan kontrast koristimo pune naglašene oblike: meni, tebi, njega. "
        "Zanaglasnice poput sam, mi i ga i dalje slijede svoja pravila.",
        rules=[
            "Položaj riječi i govorni naglasak zajedno određuju što je istaknuto.",
            "Kratko mi samo po sebi ne nosi kontrast kao meni u izrazu meni, a ne njemu.",
            "Pri preoblikovanju zadržite padež i razlikujte pošiljatelja od primatelja.",
        ],
        examples=[
            GrammarExample(
                "Meni je poslala poziv, a ne Marku.",
                note="Puni dativ meni ispravlja nesporazum o primatelju.",
            ),
            GrammarExample(
                "Poziv je poslala Ana, a ne Ivana.",
                note="Kontrast se odnosi na osobu koja je poslala poziv.",
            ),
        ],
        related=["hr-clitic-order-b1", "hr-reported-speech-b1"],
    ),
    GrammarTopic(
        "hr-cause-result-b1",
        "Uzrok i posljedica",
        "B1",
        "Povezivanje rečenica",
        "Razlikujte razlog odluke od onoga što je iz nje proizašlo.",
        "Jer i zato što uvode razlog. Zato i stoga upućuju na posljedicu već navedenog "
        "razloga. Uzročni izraz može biti i zbog s genitivom. Redoslijed dviju obavijesti "
        "ne smije promijeniti njihov odnos.",
        rules=[
            "Zbog traži genitiv: zbog kiše, zbog radova.",
            "Jer uvodi uzrok, a zato uvodi posljedicu.",
            "U običnoj uzročnoj rečenici iza glavne ne pišemo zarez ispred jer.",
        ],
        examples=[
            GrammarExample(
                "Odabrali smo dvoranu jer se ondje može doći autobusom.",
                note="Dostupnost autobusom razlog je odabira.",
            ),
            GrammarExample(
                "Počela je jaka kiša, zato smo odgodili čišćenje parka.",
                note="Odgoda je posljedica kiše, a ne njezin uzrok.",
            ),
        ],
        related=["hr-purpose-b1", "hr-concession-b1"],
    ),
    GrammarTopic(
        "hr-concession-b1",
        "Dopuštanje s iako i unatoč",
        "B1",
        "Dopusni odnosi",
        "Priznajte prepreku i navedite što ipak vrijedi.",
        "Iako uvodi činjenicu zbog koje bismo mogli očekivati drukčiji ishod. Glavna "
        "rečenica donosi stvarni ishod ili odluku. Unatoč ima slično značenje, ali iza "
        "njega dolazi imenski izraz u dativu. Ipak dodatno naglašava suprotnost očekivanju.",
        rules=[
            "Iako uvodi rečenicu: iako pada kiša.",
            "Unatoč traži dativ: unatoč kiši, unatoč problemima.",
            "Dopusni odnos razlikuje se od uzroka: prepreka nije razlog zbog kojeg nešto činimo.",
        ],
        examples=[
            GrammarExample(
                "Iako je dvorana mala, u njoj ima mjesta za cijelu skupinu.",
                note="Veličina je moguća prepreka koja ipak ne sprječava okupljanje.",
            ),
            GrammarExample(
                "Unatoč višoj cijeni, izabrali smo prostor s pristupom za invalidska kolica.",
                note="Viša cijena priznata je kao nedostatak, ali nije presudila odluci.",
            ),
        ],
        related=["hr-cause-result-b1", "hr-argument-connectors-b1"],
    ),
    GrammarTopic(
        "hr-argument-connectors-b1",
        "Povezivanje razloga i zaključka",
        "B1",
        "Povezivanje teksta",
        "Uredite kratko obrazloženje i sažmite dogovor.",
        "Prvo i drugo raspoređuju razloge. Osim toga dodaje novi razlog, s druge strane "
        "uvodi drukčiji pogled, a dakle označava zaključak izveden iz prethodnih podataka. "
        "Poveznica treba odgovarati stvarnom odnosu među idejama.",
        rules=[
            "Osim toga dodaje informaciju; ne označava automatski suprotnost.",
            "S jedne strane i s druge strane pomažu usporediti prednosti i nedostatke.",
            "Dakle ne dokazuje tvrdnju samo po sebi: zaključak mora slijediti iz navedenog.",
        ],
        examples=[
            GrammarExample(
                "Dvorana je blizu stanice. Osim toga, ima pristup za invalidska kolica.",
                note="Druga rečenica dodaje još jednu prednost.",
            ),
            GrammarExample(
                "Svi možemo doći u subotu. Dakle, sastanak ćemo održati tada.",
                note="Zaključak o terminu proizlazi iz zajedničke dostupnosti.",
            ),
            GrammarExample(
                "Prostor je povoljan. S druge strane, premalen je za sve sudionike.",
                note="Druga rečenica uvodi praktičan nedostatak.",
            ),
        ],
        related=["hr-cause-result-b1", "hr-concession-b1"],
    ),
]
