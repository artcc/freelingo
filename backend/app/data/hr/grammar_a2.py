"""Croatian A2 grammar: cases, the perfect, aspect and everyday requests."""

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic

A2_GRAMMAR_TOPICS: list[GrammarTopic] = [
    GrammarTopic(
        "hr-genitive-a2",
        "Genitiv: od koga i bez čega",
        "A2",
        "Padeži",
        "Genitivom označujemo izvor, pripadnost i ono što izostavljamo.",
        "Prijedlozi od, iz, do, kod i bez traže genitiv. U jednini mnoge muške i srednje "
        "imenice dobivaju -a: sir – sira, selo – sela. Ženske imenice na -a obično imaju "
        "-e: trgovina – trgovine. Nisu svi oblici jednaki: sol – soli.\n\n"
        "Pridjev se slaže s imenicom: bez bijelog šećera, iz male trgovine. Učimo cijela "
        "spajanja, osobito kad se mijenja osnova: otac – od oca.",
        structure="od / iz / do / kod / bez + genitiv",
        rules=[
            "Od označuje izvor ili osobu od koje nešto dolazi: poklon od prijatelja.",
            "Kod + genitiv označuje mjesto uz osobu: kod susjede.",
            "Bez označuje izostavljeni sastojak ili predmet: bez mlijeka.",
        ],
        examples=[
            GrammarExample("Kupujem sir od susjede.", note="Susjeda u genitivu glasi susjede."),
            GrammarExample(
                "Želim kavu bez bijelog šećera.",
                note="I pridjev i imenica stoje u genitivu.",
            ),
        ],
        common_mistakes=[
            GrammarMistake("Čaj bez mlijeko.", "Čaj bez mlijeka.", "Bez traži genitiv.")
        ],
        related=["hr-quantities-a2", "hr-absence-a2"],
    ),
    GrammarTopic(
        "hr-quantities-a2",
        "Količine: malo sira, pet jabuka",
        "A2",
        "Količina",
        "Naručujemo mjerljive količine i brojimo namirnice.",
        "Uz riječi malo, puno i kilogram često dolazi genitiv: malo sira, puno vode, "
        "kilogram brašna. Kod tvari koje ne brojimo koristimo genitiv jednine; kod "
        "više zasebnih predmeta genitiv množine: puno jabuka.\n\n"
        "Nakon pet i većih jednostavnih brojeva u ovim izrazima dolazi genitiv množine: "
        "pet limuna, šest jaja. Uz dva, tri i četiri učimo drukčije oblike: dva limuna, "
        "dvije jabuke, tri jaja. Imenica jaje u nominativu množine glasi jaja.\n\n"
        "Genitiv množine često ima -a, ali osnova se može promijeniti: limun — limuna, "
        "jabuka — jabuka, kruška — krušaka. Neke imenice imaju -i: stvar — stvari. "
        "Uči i česte posebne oblike: puno ljudi, puno djece. Pridjev u genitivu "
        "množine često završava na -ih: pet zrelih jabuka.",
        structure="mjera / malo / puno + genitiv; pet + genitiv množine",
        rules=[
            "Čaša vode i boca ulja sadrže genitiv jednine.",
            "Dvije jabuke i pet jabuka nisu isti padežni oblik.",
            "Ne prenosimo jedan množinski nastavak na sve imenice: jaja, jabuka, limuna.",
        ],
        examples=[
            GrammarExample("Trebam pola kilograma sira.", note="Sir je tvar; sira je genitiv."),
            GrammarExample(
                "Kupujem dvije kruške i pet jabuka.",
                note="Brojevi dvije i pet traže različite oblike ženskih imenica.",
            ),
        ],
        related=["hr-genitive-a2"],
    ),
    GrammarTopic(
        "hr-absence-a2",
        "Ima i nema: dostupnost i nedostatak",
        "A2",
        "Postojanje",
        "Provjeravamo ima li nečega i navodimo što nedostaje.",
        "U izrazima ima vode i nema kruha ne navodimo osobu koja posjeduje stvar. "
        "Ima i nema ostaju u trećem licu jednine, a imenica je u genitivu. "
        "Za više predmeta kažemo ima jabuka ili nema jaja.\n\n"
        "To razlikujemo od osobnog glagola imati: imam torbu, nemam torbu. "
        "U takvoj rečenici predmet može ostati u akuzativu; nije pravilo da svaka "
        "niječna rečenica traži genitiv.",
        structure="ima / nema + genitiv; Ima li + genitiv?",
        rules=[
            "Pitanje o ponudi glasi: Ima li svježeg kruha?",
            "Za odsutnu osobu kažemo: Nema Marka.",
            "U ovom bezličnom obrascu množina imenice ne mijenja glagol: nema jaja.",
        ],
        examples=[
            GrammarExample("Danas nema svježeg kruha.", note="Nema govori o dostupnosti."),
            GrammarExample(
                "Ima li jaja? Ima, ali nema mlijeka.",
                note="Jaja je ovdje genitiv množine, a mlijeka genitiv jednine.",
            ),
        ],
        related=["hr-genitive-a2", "hr-quantities-a2"],
    ),
    GrammarTopic(
        "hr-dative-a2",
        "Dativ: komu dajemo i pomažemo",
        "A2",
        "Padeži",
        "Dativom imenujemo primatelja ili osobu kojoj pomažemo.",
        "Na pitanje komu? odgovaramo dativom: prijatelju, sestri, djetetu. Muške i "
        "srednje imenice često imaju -u, a ženske na -a imaju -i. U nekim ženskim "
        "imenicama mijenja se suglasnik: majka – majci, ruka – ruci.\n\n"
        "Dativ koristimo uz dati, pisati, pomoći i pripadati. Pridjev također mijenja "
        "oblik: dobrom prijatelju, dobroj prijateljici. Primatelj nije isto što i "
        "predmet: dajem sestri knjigu.\n\n"
        "U množini su česti nastavci -ima i -ama: prijateljima, roditeljima, "
        "sestrama, kolegama. Pridjev ima -im: pomažem starim susjedima, pišem "
        "novim kolegicama. Oblike učimo uz imenicu, ne samo prema spolu osobe.",
        structure="komu? prijatelju / sestri / djetetu",
        rules=[
            "U rečenici Pišem bratu riječ bratu označuje primatelja.",
            "Uz pomagati osoba je u dativu: pomažem susjedi.",
            "Oblike s promjenom suglasnika učimo uz imenicu: majci, ruci.",
        ],
        examples=[
            GrammarExample("Dajem poklon majci.", note="Majci odgovara na pitanje komu."),
            GrammarExample(
                "Pomažemo starom susjedu.",
                note="Dativ imaju i pridjev starom i imenica susjedu.",
            ),
            GrammarExample(
                "Šaljem pozive dobrim prijateljima.",
                note="Dobrim prijateljima označuje više primatelja u dativu množine.",
            ),
        ],
        related=["hr-object-clitics-a2"],
    ),
    GrammarTopic(
        "hr-instrumental-a2",
        "Instrumental: društvo i sredstvo",
        "A2",
        "Padeži",
        "Kažemo s kim nešto radimo i čime putujemo.",
        "Za društvo koristimo s ili sa i instrumental: s bratom, s prijateljicom. "
        "Za sredstvo obično nema prijedloga: putujem vlakom, pišem olovkom. "
        "Muške i srednje imenice često imaju -om, a nakon nekih suglasnika -em: "
        "prijateljem, morem. Ženske imenice na -a imaju -om: sestrom.\n\n"
        "Sa olakšava izgovor, osobito ispred s, š, z i ž: sa sestrom, sa ženom. "
        "Uobičajen je i izraz sa mnom. Pridjevi imaju oblike poput dobrim prijateljem "
        "i dobrom prijateljicom.\n\n"
        "U množini se dativ, lokativ i instrumental podudaraju u obliku: prijateljima, "
        "kolegicama. Usporedi: pomažem prijateljima, govorim o prijateljima, putujem "
        "s prijateljima. O s lokativom ovdje označuje temu razgovora. "
        "Prijedlog i značenje pokazuju ulogu. Za mjesta kažemo "
        "u gradovima i u školama; za društvo s dobrim prijateljima i s novim kolegicama.",
        structure="s(a) + instrumental društva; instrumental sredstva bez s(a)",
        rules=[
            "S prijateljem označuje društvo, a biciklom sredstvo prijevoza.",
            "Ne dodajemo s u neutralni izraz putujem vlakom.",
            "Učimo oblike imenice i pridjeva zajedno: s novim kolegom.",
        ],
        examples=[
            GrammarExample(
                "Putujem vlakom s prijateljicom.",
                note="Vlakom je sredstvo, s prijateljicom društvo.",
            ),
            GrammarExample("Razgovaram sa sestrom.", note="Sa olakšava izgovor ispred s."),
        ],
        related=["hr-dative-a2", "hr-route-a2"],
    ),
    GrammarTopic(
        "hr-vocative-a2",
        "Vokativ: izravno obraćanje",
        "A2",
        "Padeži",
        "Dozivamo osobu i obraćamo joj se imenom ili titulom.",
        "Vokativ koristimo kad nekome izravno govorimo: Ivane, gospodine, prijatelju. "
        "Oblik nije uvijek jednak nominativu. Neka imena ostaju ista: Marko. "
        "Kod ženskih imena postoje različiti obrasci: Ana – Ana, Maja – Majo.\n\n"
        "Ne stvaramo vokativ samo prema posljednjem slovu. Učimo uobičajen oblik "
        "imena osobe. U pisanju ga odvajamo zarezom, a u govoru kratkom stankom.",
        structure="Ivane, ... / ..., gospodine.",
        rules=[
            "Izravno obraćanje razlikuje se od spominjanja: Ivan je ovdje. Ivane, gdje si?",
            "Titula gospodin u obraćanju glasi gospodine.",
            "Vokativ nije sam po sebi neformalan; registar ovisi o imenu, tituli i situaciji.",
        ],
        examples=[
            GrammarExample("Ivane, imaš li vremena?", note="Govornik se obraća Ivanu."),
            GrammarExample(
                "Gospodine, ovo je vaša torba.",
                note="Titula i zamjenica vaša odgovaraju uljudnom obraćanju.",
            ),
        ],
        related=["hr-imperative-a2"],
    ),
    GrammarTopic(
        "hr-perfect-a2",
        "Perfekt: pričamo o prošlosti",
        "A2",
        "Glagolska vremena",
        "Spajamo sadašnji oblik glagola biti i glagolski pridjev radni.",
        "Perfekt označuje prošlu radnju. Tvori se od pomoćnog glagola biti i "
        "glagolskog pridjeva radnog: radio sam, radila si, radili smo. Pomoćni oblici "
        "su sam, si, je, smo, ste, su. U trećem licu također zadržavamo pomoćni "
        "glagol u običnoj potvrdnoj rečenici: Ivan je radio.\n\n"
        "Mnogi oblici nastaju prema infinitivu: raditi – radio/radila, gledati – "
        "gledao/gledala. Neki su posebni: biti – bio/bila, ići – išao/išla. "
        "Najprije vježbamo ove česte parove, a ne jedno pravilo za sve glagole.",
        structure="sam / si / je / smo / ste / su + glagolski pridjev radni",
        rules=[
            "Osobu pokazuje pomoćni glagol: radio sam, radio si.",
            "Zamjenicu često izostavljamo: Jučer sam radio.",
            "U neutralnoj punoj rečenici kažemo Ona je čitala. "
            "Krnji perfekt bez pomoćnog glagola susreće se u posebnim pripovjednim "
            "ili razgovornim kontekstima.",
        ],
        examples=[
            GrammarExample("Jučer sam bio u Zadru.", note="Govornik koristi muški oblik bio."),
            GrammarExample(
                "Ana je gledala film.",
                note="Je je pomoćni glagol; gledala je ženski oblik.",
            ),
        ],
        related=["hr-perfect-agreement-a2", "hr-perfect-questions-a2"],
    ),
    GrammarTopic(
        "hr-perfect-agreement-a2",
        "Perfekt: rod i broj",
        "A2",
        "Slaganje",
        "Biramo prošli oblik prema subjektu rečenice.",
        "Glagolski pridjev radni slaže se sa subjektom u rodu i broju: Ivan je radio, "
        "Ana je radila, dijete je radilo. U množini razlikujemo radili, radile i radila: "
        "muškarci su radili, žene su radile, sela su bila mirna.\n\n"
        "Za skupinu muškaraca i žena koristimo muški rod množine: Ana i Ivan su "
        "putovali. Kad žena govori o sebi, kaže radila sam; muškarac kaže radio sam. "
        "Pri uljudnom obraćanju jednoj osobi s Vi uobičajen je oblik muškog roda "
        "množine: Gospođo, jeste li putovali?",
        structure="radio / radila / radilo; radili / radile / radila",
        rules=[
            "Pomoćni glagol prati osobu i broj, a radni pridjev rod i broj.",
            "Dvije žene: Ana i Iva su putovale.",
            "Mješovita skupina: Ana i Ivan su putovali.",
        ],
        examples=[
            GrammarExample(
                "Maja i Petra su gledale predstavu.",
                note="Dvije žene traže ženski rod množine gledale.",
            ),
            GrammarExample(
                "Djeca su bila umorna.",
                note="Uz zbirnu imenicu djeca ovdje dolaze oblici bila i umorna.",
            ),
        ],
        related=["hr-perfect-a2", "hr-perfect-questions-a2"],
    ),
    GrammarTopic(
        "hr-perfect-questions-a2",
        "Perfekt: pitanja, negacija i red riječi",
        "A2",
        "Glagolska vremena",
        "Pitam o prošlom događaju i kažem što se nije dogodilo.",
        "Pitanja često počinju oblicima Jesam li, Jesi li, Je li, Jesmo li, Jeste li, "
        "Jesu li: Jesi li gledao film? Uz upitnu riječ kažemo Gdje si bio? "
        "Niječemo oblicima nisam, nisi, nije, nismo, niste, nisu.\n\n"
        "Kratki potvrdni oblici sam, si i je ne stoje samostalno na početku obične "
        "izjavne rečenice. Dolaze iza prve naglašene riječi ili cjeline: Jučer sam "
        "radio. Prošli vikend sam radio. Niječni oblik može početi rečenicu: Nisam radio.",
        structure="Jesi li radio? / Gdje si radio? / Nisam radio.",
        rules=[
            "U standardnom pitanju s li kažemo Je li Ana došla?; li pišemo odvojeno.",
            "Negaciju pišemo spojeno: nisam, nije, nisu.",
            "Pomoćni oblik ne stavljamo mehanički na kraj: Jučer sam gledala film.",
        ],
        examples=[
            GrammarExample("Gdje ste bili jučer?", note="Ste slijedi upitnu riječ gdje."),
            GrammarExample(
                "Nisam bio kod kuće.",
                note="Nisam može stajati na početku niječne rečenice.",
            ),
        ],
        related=["hr-perfect-a2", "hr-perfect-agreement-a2"],
    ),
    GrammarTopic(
        "hr-aspect-a2",
        "Glagolski vid: čitati i pročitati",
        "A2",
        "Glagolski vid",
        "Razlikujemo radnju u tijeku od zaokružene cjeline.",
        "Nesvršeni glagoli, primjerice čitati i kupovati, prikazuju trajanje ili "
        "ponavljanje. Svršeni glagoli, primjerice pročitati i kupiti, prikazuju "
        "radnju kao cjelinu s granicom ili rezultatom. Vid nije isto što i vrijeme: "
        "jučer sam čitao i jučer sam pročitao obje su prošle radnje.\n\n"
        "Čitao sam knjigu ne potvrđuje da je knjiga dovršena. Pročitao sam knjigu "
        "potvrđuje čitanje cjeline. Parove učimo kao rječničke veze; dodavanje "
        "prefiksa ne daje uvijek jednostavan par istog značenja.",
        structure="čitati – pročitati; kupovati – kupiti; pisati – napisati",
        rules=[
            "Za tijek radnje sada koristimo nesvršeni prezent: Sada pišem poruku.",
            "Za ponavljanje prirodan je nesvršeni oblik: Svaki dan kupujem kruh.",
            "U perfektu svršenost često ističe rezultat: Napisao sam poruku.",
        ],
        examples=[
            GrammarExample(
                "Jučer sam čitala knjigu dva sata.",
                note="Trajanje je važno; završetak cijele knjige nije potvrđen.",
            ),
            GrammarExample(
                "Jučer sam pročitala cijelu knjigu.",
                note="Pročitala prikazuje završenu cjelinu.",
            ),
        ],
        related=["hr-perfect-a2", "hr-future-a2"],
    ),
    GrammarTopic(
        "hr-future-a2",
        "Futur prvi: što ćemo raditi",
        "A2",
        "Glagolska vremena",
        "Najavljujemo buduću radnju s oba glagolska vida.",
        "Futur prvi tvori se od infinitiva i kratkih oblika glagola htjeti: ću, ćeš, "
        "će, ćemo, ćete, će. Kažemo Sutra ću putovati ili Putovat ću sutra. "
        "Kad infinitiv na -ti stoji ispred kratkog pomoćnog glagola, završno i "
        "izostavljamo: kupit ću. Infinitiv na -ći ostaje cijeli: ići ću, doći ću.\n\n"
        "Oba vida tvore futur prvi: čitat ću opisuje čitanje, pročitat ću najavljuje "
        "cjelinu. Svršeni prezent nije opća zamjena za ovaj futur. Niječemo oblicima "
        "neću, nećeš, neće, nećemo, nećete, neće.",
        structure="Sutra ću putovati. / Putovat ću. / Ići ću. / Neću putovati.",
        rules=[
            "Pomoćni oblik i infinitiv pišemo odvojeno: vidjet ću, doći ću.",
            "Kad pomoćni oblik prethodi infinitivu, infinitiv je pun: Sutra ću vidjeti Anu.",
            "Pitanje može glasiti Hoćeš li putovati? ili Kad ćeš putovati?",
        ],
        examples=[
            GrammarExample(
                "Sutra ću kupiti kartu.",
                note="Svršeni infinitiv kupiti najavljuje rezultat.",
            ),
            GrammarExample(
                "Kupit ćemo kartu, a putovat ćemo vlakom.",
                note="Infinitivi na -ti gube završno i ispred ćemo.",
            ),
        ],
        related=["hr-aspect-a2", "hr-perfect-a2"],
    ),
    GrammarTopic(
        "hr-route-a2",
        "Kamo, gdje i odakle",
        "A2",
        "Padeži i kretanje",
        "Razlikujemo odredište, mjesto boravka i polazište.",
        "Za odredište u i na dolaze s akuzativom: idem u Rijeku, na otok. "
        "Za mjesto dolaze s lokativom: u Rijeci, na otoku. Polazište često izražavamo "
        "s iz ili s i genitivom: iz Rijeke, s otoka. Prijedlog do također traži "
        "genitiv i označuje granicu puta: do kolodvora.\n\n"
        "Učimo povezane izraze: u Split – u Splitu – iz Splita; na otok – na otoku – "
        "s otoka. Kod osobe opisuje boravak: kod prijatelja. Kao jasan cilj posjeta "
        "možemo reći idem k prijatelju.",
        structure="u/na + akuzativ; u/na + lokativ; iz/s/do + genitiv",
        rules=[
            "Smjer i mjesto razlikujemo prema značenju glagola i padežu.",
            "Ne biramo prijedlog samo prema tome je li mjesto zatvoreno.",
            "S otoka ima genitiv; s prijateljem ima instrumental i označuje društvo.",
        ],
        examples=[
            GrammarExample(
                "Idemo na Hvar, a prijatelji su već na Hvaru.",
                note="Na Hvar je odredište, na Hvaru mjesto.",
            ),
            GrammarExample(
                "Putujemo iz Zadra do Zagreba.",
                note="Iz Zadra označuje polazište, do Zagreba granicu putovanja.",
            ),
        ],
        related=["hr-genitive-a2", "hr-instrumental-a2"],
    ),
    GrammarTopic(
        "hr-reflexive-a2",
        "Glagoli sa se i si",
        "A2",
        "Povratni glagoli",
        "Opisujemo osobnu njegu i svakodnevne radnje.",
        "Neki glagoli redovito dolaze sa se: odmarati se, osjećati se, brinuti se. "
        "Kod drugih se pokazuje da osoba djeluje na sebe: perem se. Ako je izravan "
        "predmet imenovan, si može značiti sebi: perem si ruke.\n\n"
        "Kratke riječi se i si ne stavljamo na početak obične izjavne rečenice: "
        "Danas se odmaram. U perfektu trećeg lica jednine uz se obično izostaje je: "
        "Ana se odmarala. U prvom licu ostaje sam: Odmarao sam se.",
        structure="odmaram se; perem si ruke; Ana se odmarala",
        rules=[
            "Glagol i njegovu povratnu riječ učimo zajedno: osjećati se.",
            "Se i si nisu slobodno zamjenjivi: perem se, ali perem si ruke.",
            "U kratkom skupu pomoćni sam dolazi prije se: Danas sam se odmarao.",
        ],
        examples=[
            GrammarExample(
                "Osjećam se slabo i danas se odmaram.",
                note="Se pripada glagolima osjećati se i odmarati se.",
            ),
            GrammarExample(
                "Ivan si pere ruke prije jela.",
                note="Ruke su predmet, a si označuje da ih pere sebi.",
            ),
        ],
        related=["hr-perfect-a2", "hr-svoj-a2"],
    ),
    GrammarTopic(
        "hr-svoj-a2",
        "Svoj: pripadnost subjektu",
        "A2",
        "Zamjenice",
        "Jasno razlikujemo vlasništvo osobe koja vrši radnju.",
        "Svoj upućuje na subjekt iste rečenice. U rečenici Ana traži svoju iskaznicu "
        "iskaznica pripada Ani. Ana traži njezinu iskaznicu obično upućuje na drugu "
        "ženu. Oblik svoj ne ovisi o spolu vlasnika, nego se slaže s posjedovanom "
        "imenicom u rodu, broju i padežu.\n\n"
        "Kažemo svoj lijek, svoju torbu, svoje dijete; u drugim padežima svom liječniku, "
        "sa svojom sestrom. I uz ja i ti koristimo svoj kad vlasnik odgovara subjektu: "
        "Nosim svoju iskaznicu.",
        structure="subjekt + glagol + svoj/svoja/svoje + posjedovana stvar",
        rules=[
            "Svoj može upućivati na bilo koje lice: ja, ti, on, mi.",
            "U izrazu svoju torbu ženski oblik dolazi od imenice torba.",
            "Njegov i njezin mogu označiti drugog vlasnika; kontekst razjašnjava koga.",
        ],
        examples=[
            GrammarExample(
                "Marko nosi svoju zdravstvenu iskaznicu.",
                note="Iskaznica pripada Marku, subjektu rečenice.",
            ),
            GrammarExample(
                "Razgovaram sa svojim liječnikom.",
                note="Svojim se slaže s liječnikom u instrumentalu.",
            ),
        ],
        related=["hr-instrumental-a2", "hr-reflexive-a2"],
    ),
    GrammarTopic(
        "hr-imperative-a2",
        "Imperativ: upute i savjeti",
        "A2",
        "Način",
        "Razumijemo i dajemo kratke upute.",
        "Imperativ koristimo za upute, molbe i poticaje. Uobičajeni su oblici pij – "
        "pijte, čekaj – čekajte, uzmi – uzmite, dođi – dođite. Nastavak -te označuje "
        "više osoba ili uljudno obraćanje jednoj osobi. Za zajedničku radnju kažemo "
        "idemo ili upotrijebimo imperativ poput krenimo.\n\n"
        "Zabranu često izražavamo s nemoj/nemojte i infinitivom: Nemojte pušiti. "
        "Molim vas ublažava izravnu uputu. Nije svaka zapovjedna rečenica nepristojna; "
        "u ordinaciji kratka jasna uputa može biti očekivana.",
        structure="pij / pijte; uzmi / uzmite; nemoj(te) + infinitiv",
        rules=[
            "Za osobu kojoj govorimo Vi biramo oblik na -te.",
            "Česte nepravilne oblike učimo zasebno: biti – budi/budite.",
            "Razlikujemo ponavljanu radnju i jednu cjelinu: Pijte vodu. Popijte ovu čašu.",
        ],
        examples=[
            GrammarExample(
                "Otvorite usta, molim vas.",
                note="Uputa liječnika jednoj osobi kojoj se obraća s Vi.",
            ),
            GrammarExample(
                "Nemoj uzimati lijek bez savjeta liječnika.",
                note="Nemoj s infinitivom izražava zabranu ili upozorenje.",
            ),
        ],
        related=["hr-aspect-a2", "hr-vocative-a2"],
    ),
    GrammarTopic(
        "hr-comparative-a2",
        "Komparativ: veći, jeftiniji, bolji",
        "A2",
        "Usporedba",
        "Uspoređujemo dvije osobe, stvari ili ponude.",
        "Komparativ označuje viši stupanj svojstva: jeftin – jeftiniji, star – stariji, "
        "mlad – mlađi. Česti nepravilni oblici su dobar – bolji, loš – gori, velik – "
        "veći, malen – manji. Komparativ se slaže s imenicom: veća soba, veći balkon.\n\n"
        "Usporedbu gradimo s od i genitivom: soba je jeftinija od apartmana. "
        "Moguća je i usporedba s nego: soba je jeftinija nego apartman. Za niži "
        "stupanj kažemo manje udoban, a ne izmišljamo poseban nastavak.",
        structure="komparativ + od + genitiv; komparativ + nego",
        rules=[
            "Kratak pridjev ne dobiva uvijek -iji: skup – skuplji, tih – tiši.",
            "Nastavak prati rod: hotel je bolji, soba je bolja.",
            "Od traži genitiv, dok iza nego možemo usporediti dvije imenice u nominativu.",
        ],
        examples=[
            GrammarExample(
                "Ova je soba veća od naše sobe.",
                note="Veća se slaže sa soba, a od naše sobe je genitiv.",
            ),
            GrammarExample(
                "Hotel je skuplji nego kamp.",
                note="Nego povezuje dvije uspoređene mogućnosti.",
            ),
        ],
        related=["hr-genitive-a2", "hr-superlative-a2"],
    ),
    GrammarTopic(
        "hr-superlative-a2",
        "Superlativ: najpovoljniji izbor",
        "A2",
        "Usporedba",
        "Izdvajamo jednu mogućnost iz skupine.",
        "Superlativ tvorimo dodavanjem naj- komparativu: jeftiniji – najjeftiniji, "
        "bolji – najbolji, bliži – najbliži. Pišemo ga kao jednu riječ. U obliku "
        "najjeftiniji zadržavamo oba j jer jedno pripada naj-, a drugo komparativu.\n\n"
        "Navodimo skupinu kad je važna: najjeftinija soba u ovom hotelu. To ne znači "
        "da je najjeftinija u cijelom gradu. Oblik pridjeva prati imenicu: najbliži "
        "hotel, najbliža plaža, najbliže selo.",
        structure="naj- + komparativ",
        rules=[
            "Najbolji je superlativ od dobar preko komparativa bolji.",
            "Naj- pišemo spojeno s pridjevom.",
            "Usporednu skupinu možemo odrediti izrazima u gradu ili od svih ponuđenih soba.",
        ],
        examples=[
            GrammarExample(
                "Od ove tri sobe zelena je najjeftinija.",
                note="Tvrdnja se odnosi samo na tri navedene sobe.",
            ),
            GrammarExample(
                "Ovo je najbliži hotel kolodvoru.",
                note="Najbliži označuje najmanju udaljenost u relevantnoj skupini.",
            ),
        ],
        related=["hr-comparative-a2"],
    ),
    GrammarTopic(
        "hr-polite-conditional-a2",
        "Ljubazne molbe: htio bih i biste li",
        "A2",
        "Uljudno izražavanje",
        "Koristimo česte gotove izraze za želju i molbu.",
        "Za ljubazno izražavanje želje učimo izraze Htio bih rezervirati sobu i "
        "Htjela bih rezervirati sobu. Bih je oblik za ja, a htio ili htjela "
        "prati rod govornika. Za molbu osobi kojoj govorimo Vi koristimo Biste li "
        "ponovili? ili Možete li ponoviti?\n\n"
        "Ovdje uvježbavamo uobičajene izraze, a ne sve vrste pogodbenih rečenica. "
        "Želio bih/Željela bih i Molio bih/Molila bih također uvode ljubaznu želju "
        "ili zahtjev. U standardnom jeziku prvo lice jednine glasi bih, iako se "
        "u razgovoru čuje i bi.",
        structure="Htio/Htjela bih + infinitiv; Biste li + radni pridjev?",
        rules=[
            "Muški govornik kaže htio bih, a ženska govornica htjela bih.",
            "Biste li otvorili prozor? prikladno je u uljudnom obraćanju.",
            "Molim vas možemo dodati molbi, ali ljubaznost ovisi i o tonu.",
        ],
        examples=[
            GrammarExample(
                "Htjela bih rezervirati dvokrevetnu sobu.",
                note="Govornica ljubazno izražava želju ustaljenim izrazom.",
            ),
            GrammarExample(
                "Biste li nam pokazali sobu?",
                note="Biste li uvodi molbu osobi kojoj govorimo Vi.",
            ),
        ],
        related=["hr-perfect-agreement-a2", "hr-imperative-a2"],
    ),
    GrammarTopic(
        "hr-object-clitics-a2",
        "Kratke zamjenice: mi, mu, ga, je",
        "A2",
        "Zamjenice i red riječi",
        "Zamjenjujemo već poznatog primatelja ili predmet.",
        "Za poznatog primatelja koristimo kratki dativ: mi, ti, mu, joj, nam, vam, im. "
        "Za poznati predmet česti su kratki akuzativi me, te, ga, je, nas, vas, ih. "
        "Predajem račun službeniku postaje Predajem mu račun; čitam poruku postaje "
        "Čitam je. Referent mora biti jasan iz konteksta. Za ženski rod postoji i "
        "akuzativ ju. Ispred pomoćnog je upotrebljavamo ju: Ana ju je pročitala, "
        "pri čemu ju zamjenjuje poruku, a je tvori perfekt.\n\n"
        "Iza prijedloga i pod naglaskom ovdje vježbamo duge oblike: za mene, s njim. "
        "Kad su dvije kratke zamjenice zajedno, "
        "dativ prethodi akuzativu: Dajem mu ga. Uz pomoćni glagol u perfektu: "
        "Jučer sam mu dao račun. Za naglašavanje koristimo duge oblike: Dajem njemu.",
        structure="dajem mu račun → dajem mu ga; čitam poruku → čitam je",
        rules=[
            "Mu označuje muškog ili srednjeg primatelja, joj ženskog primatelja.",
            "Ga može zamijeniti račun, a je poruku.",
            "U spoju mu ga dativ dolazi prije akuzativa; ne obrćemo njihov red.",
        ],
        examples=[
            GrammarExample(
                "Ana treba potvrdu. Šaljem joj je danas.",
                note="Joj zamjenjuje Anu, a je potvrdu.",
            ),
            GrammarExample(
                "Imam račun i dajem ga službeniku.",
                note="Ga zamjenjuje već spomenuti račun.",
            ),
        ],
        related=["hr-dative-a2", "hr-perfect-questions-a2"],
    ),
    GrammarTopic(
        "hr-modals-a2",
        "Morati, moći i smjeti",
        "A2",
        "Modalni glagoli",
        "Razlikujemo obvezu, mogućnost i dopuštenje.",
        "Morati s infinitivom izražava obvezu: Moram platiti račun. Moći izražava "
        "mogućnost ili sposobnost: Mogu doći sutra. Smjeti govori o dopuštenju: "
        "Smijete ući. U prezentu učimo česte oblike mogu, možeš, može te smijem, "
        "smiješ, smije.\n\n"
        "Ne moram znači da nema obveze; ne smijem znači da postoji zabrana. "
        "Ne mogu često znači da nemam mogućnost, primjerice zbog zatvorenog ureda. "
        "Biramo izraz prema stvarnoj poruci, a ne samo prema negaciji.",
        structure="moram / mogu / smijem + infinitiv",
        rules=[
            "Ne morate čekati dopušta odlazak; ne zabranjuje čekanje.",
            "Ne smijete parkirati označuje zabranu.",
            "Poslije modalnog glagola u ovim obrascima dolazi infinitiv.",
        ],
        examples=[
            GrammarExample(
                "Račun moram platiti do petka.",
                note="Moram označuje obvezu s rokom.",
            ),
            GrammarExample(
                "Ovdje ne smijete pušiti, ali smijete čekati.",
                note="Prvi dio zabranjuje radnju, a drugi je dopušta.",
            ),
        ],
        related=["hr-imperative-a2", "hr-future-a2"],
    ),
    GrammarTopic(
        "hr-connectors-a2",
        "Povezujemo poruke: jer, zato, ali i kad",
        "A2",
        "Povezivanje rečenica",
        "Objašnjavamo razlog, posljedicu, suprotnost i vrijeme.",
        "Jer uvodi razlog: Ne dolazim jer sam bolestan. Zato uvodi posljedicu: "
        "Bolestan sam. Zato ne dolazim. Ali suprotstavlja dvije informacije: "
        "Ured je otvoren, ali službenik nije ovdje.\n\n"
        "Kad povezuje radnju s vremenom druge radnje. Ovdje vježbamo navike i prošle "
        "događaje: Kad imam vremena, čitam. Kad sam došao kući, nazvao sam prijatelja. "
        "Kad rečenica s kad stoji prva, odvajamo je zarezom.",
        structure="razlog: jer; posljedica: zato; suprotnost: ali; vrijeme: kad",
        rules=[
            "Jer i zato ne zamjenjujemo bez promjene redoslijeda razloga i posljedice.",
            "Prije ali u ovim povezanim rečenicama pišemo zarez.",
            "Kad u ovim primjerima označuje vrijeme, a ne uzrok.",
        ],
        examples=[
            GrammarExample(
                "Kasnim jer autobus ne vozi. Zato trebam novi termin.",
                note="Jer objašnjava kašnjenje, a zato povezuje kašnjenje s novim zahtjevom.",
            ),
            GrammarExample(
                "Kad sam dobila poruku, nazvala sam ured.",
                note="Prvo je stigla poruka, a zatim je uslijedio poziv.",
            ),
        ],
        related=["hr-perfect-a2", "hr-modals-a2"],
    ),
]
