"""Swedish A2 vocabulary for independent everyday tasks."""

from app.data._types import VocabularyEntry, VocabularySet

A2_SETS: list[VocabularySet] = [
    VocabularySet(
        "sv_travel_a2",
        "A2",
        "Resor och erfarenheter",
        "a2-unit-1",
        [
            VocabularyEntry(
                "en resa",
                "noun",
                "En förflyttning till en annan plats, ofta längre bort.",
                "Resan till Kiruna tog många timmar.",
            ),
            VocabularyEntry(
                "en semester",
                "noun",
                "Ledig tid från arbetet för vila och andra aktiviteter.",
                "Jag hade semester i juli.",
            ),
            VocabularyEntry(
                "ett flygplan",
                "noun",
                "Ett fordon med vingar som färdas i luften.",
                "Flygplanet landade i tid.",
            ),
            VocabularyEntry(
                "en flygplats",
                "noun",
                "En plats där flygplan startar och landar.",
                "Vi tog tåget till flygplatsen.",
            ),
            VocabularyEntry(
                "en avgång",
                "noun",
                "Tidpunkten eller tillfället då ett fordon lämnar en plats.",
                "Nästa avgång är klockan tolv.",
            ),
            VocabularyEntry(
                "en ankomst",
                "noun",
                "Tillfället då någon eller något kommer fram.",
                "Vid ankomsten hämtade vi våra väskor.",
            ),
            VocabularyEntry(
                "en hållplats",
                "noun",
                "En bestämd plats där buss eller spårvagn stannar.",
                "Jag gick av vid fel hållplats.",
            ),
            VocabularyEntry(
                "ett byte",
                "noun",
                "En övergång från ett färdmedel eller alternativ till ett annat.",
                "Resan har ett byte i Stockholm.",
            ),
            VocabularyEntry(
                "ett spår",
                "noun",
                "Räls som ett tåg går på; också numret för tågets plats på stationen.",
                "Tåget går från spår fyra.",
            ),
            VocabularyEntry(
                "en försening",
                "noun",
                "Att något sker senare än planerat.",
                "Det blev en försening på tjugo minuter.",
            ),
            VocabularyEntry(
                "bagage",
                "noun",
                "Väskor och saker som man tar med på en resa.",
                "Mitt bagage kom inte fram.",
            ),
            VocabularyEntry(
                "ett pass",
                "noun",
                "En officiell handling som visar vem man är och vilket medborgarskap man har.",
                "Jag tog med mitt pass.",
            ),
            VocabularyEntry(
                "boka", "verb", "Beställa en plats eller tid i förväg.", "Vi har bokat ett rum."
            ),
            VocabularyEntry(
                "avboka", "verb", "Ta tillbaka en tidigare bokning.", "Jag måste avboka resan."
            ),
            VocabularyEntry(
                "resa", "verb", "Åka till en annan plats.", "Vi reste till Öland förra sommaren."
            ),
            VocabularyEntry(
                "hinna", "verb", "Ha tillräckligt med tid för något.", "Vi hann med tåget."
            ),
            VocabularyEntry(
                "missa",
                "verb",
                "Inte hinna till eller få något som man tänkt.",
                "Jag missade bussen.",
            ),
            VocabularyEntry(
                "ett hotell",
                "noun",
                "En byggnad där gäster betalar för att bo tillfälligt.",
                "Hotellet låg nära stationen.",
            ),
            VocabularyEntry(
                "en reception",
                "noun",
                "En plats där besökare får hjälp och anmäler sin ankomst.",
                "Fråga i receptionen.",
            ),
            VocabularyEntry(
                "en nattbuss", "noun", "En buss som går på natten.", "Vi tog nattbussen hem."
            ),
            VocabularyEntry(
                "en karta",
                "noun",
                "En bild som visar platser och vägar.",
                "Kan du visa hotellet på kartan?",
            ),
            VocabularyEntry(
                "en väg", "noun", "En sträcka där man kan gå eller köra.", "Vilken väg är kortast?"
            ),
            VocabularyEntry(
                "tillbaka",
                "adverb",
                "Åter till en tidigare plats eller situation.",
                "Vi kom tillbaka igår.",
            ),
            VocabularyEntry(
                "utomlands",
                "adverb",
                "I ett annat land än det man utgår från.",
                "Hon har arbetat utomlands.",
            ),
            VocabularyEntry(
                "förra",
                "adjective",
                "Den närmast föregående i en följd.",
                "Förra veckan var jag i Gävle.",
            ),
            VocabularyEntry(
                "redan",
                "adverb",
                "Tidigare än nu eller tidigare än väntat.",
                "Jag har redan köpt biljetten.",
            ),
        ],
    ),
    VocabularySet(
        "sv_housing_a2",
        "A2",
        "Bostad och jämförelser",
        "a2-unit-2",
        [
            VocabularyEntry(
                "en bostad", "noun", "En plats där någon bor.", "Vi söker en större bostad."
            ),
            VocabularyEntry(
                "en hyra",
                "noun",
                "Pengar som betalas för att använda till exempel en bostad.",
                "Hyran betalas varje månad.",
            ),
            VocabularyEntry(
                "en granne",
                "noun",
                "En person som bor nära en.",
                "Vår granne hjälpte oss att flytta.",
            ),
            VocabularyEntry(
                "ett sovrum", "noun", "Ett rum där man sover.", "Sovrummet är litet men tyst."
            ),
            VocabularyEntry(
                "ett vardagsrum",
                "noun",
                "Ett rum för umgänge och vila.",
                "Soffan står i vardagsrummet.",
            ),
            VocabularyEntry(
                "en balkong",
                "noun",
                "En plattform utanför en lägenhet ovanför marken.",
                "Vi åt frukost på balkongen.",
            ),
            VocabularyEntry(
                "en tvättstuga",
                "noun",
                "Ett rum med maskiner för att tvätta kläder.",
                "Jag har bokat tvättstugan.",
            ),
            VocabularyEntry(
                "en hiss",
                "noun",
                "En anordning som transporterar människor mellan våningar.",
                "Hissen är trasig.",
            ),
            VocabularyEntry(
                "en våning", "noun", "Ett plan i en byggnad.", "Vi bor på tredje våningen."
            ),
            VocabularyEntry(
                "ett golv", "noun", "Den yta man går på inne i ett rum.", "Golvet behöver tvättas."
            ),
            VocabularyEntry(
                "en vägg",
                "noun",
                "En lodrät del som skiljer rum åt eller omger ett hus.",
                "Vi målade väggen vit.",
            ),
            VocabularyEntry(
                "ett tak", "noun", "Den övre delen av ett rum eller hus.", "Det droppar från taket."
            ),
            VocabularyEntry(
                "en soffa",
                "noun",
                "En mjuk sittmöbel för flera personer.",
                "Den nya soffan är bekväm.",
            ),
            VocabularyEntry(
                "en hylla",
                "noun",
                "En skiva eller möbel där saker kan stå.",
                "Böckerna står på hyllan.",
            ),
            VocabularyEntry(
                "ett kylskåp",
                "noun",
                "Ett skåp som håller maten kall.",
                "Mjölken står i kylskåpet.",
            ),
            VocabularyEntry(
                "en spis",
                "noun",
                "En apparat som man värmer mat på.",
                "Glöm inte att stänga av spisen.",
            ),
            VocabularyEntry(
                "flytta",
                "verb",
                "Byta bostad eller föra något till en annan plats.",
                "Vi flyttade hit i april.",
            ),
            VocabularyEntry(
                "städa", "verb", "Göra rent och ordna saker.", "Jag städar köket på söndagar."
            ),
            VocabularyEntry(
                "tvätta",
                "verb",
                "Göra rent med vatten och ofta tvål eller tvättmedel.",
                "Hon tvättar sina kläder.",
            ),
            VocabularyEntry(
                "laga", "verb", "Reparera något trasigt; också göra mat.", "Kan någon laga hissen?"
            ),
            VocabularyEntry(
                "trasig", "adjective", "Som är skadad eller inte fungerar.", "Lampan är trasig."
            ),
            VocabularyEntry("ren", "adjective", "Utan smuts.", "Nu är lägenheten ren."),
            VocabularyEntry("smutsig", "adjective", "Som har smuts på sig.", "Skorna är smutsiga."),
            VocabularyEntry(
                "ljus",
                "adjective",
                "Med mycket ljus eller en färg nära vitt.",
                "Rummet är ljust på morgonen.",
            ),
            VocabularyEntry(
                "mörk", "adjective", "Med lite ljus eller en färg nära svart.", "Hallen är mörk."
            ),
            VocabularyEntry(
                "bekväm",
                "adjective",
                "Som känns skön och lätt att använda.",
                "Stolen är bekväm att sitta på.",
            ),
        ],
    ),
    VocabularySet(
        "sv_health_a2",
        "A2",
        "Hälsa och vårdkontakt",
        "a2-unit-3",
        [
            VocabularyEntry(
                "en vårdcentral",
                "noun",
                "En mottagning för vanlig sjukvård nära där man bor.",
                "Jag ringde vårdcentralen.",
            ),
            VocabularyEntry(
                "en sjuksköterska",
                "noun",
                "En utbildad person som ger omvårdnad och medicinsk hjälp.",
                "Sjuksköterskan frågade hur jag mådde.",
            ),
            VocabularyEntry(
                "en tandläkare",
                "noun",
                "En person som undersöker och behandlar tänder.",
                "Jag har tid hos tandläkaren.",
            ),
            VocabularyEntry(
                "en tid",
                "noun",
                "En bestämd tidpunkt, till exempel för ett besök.",
                "Finns det en ledig tid imorgon?",
            ),
            VocabularyEntry(
                "ett besök",
                "noun",
                "Ett tillfälle då man går till någon eller någonstans.",
                "Besöket tog en halvtimme.",
            ),
            VocabularyEntry(
                "en undersökning",
                "noun",
                "En kontroll för att ta reda på hur något är.",
                "Läkaren gjorde en undersökning.",
            ),
            VocabularyEntry(
                "feber",
                "noun",
                "Högre kroppstemperatur än normalt vid till exempel sjukdom.",
                "Barnet har feber.",
            ),
            VocabularyEntry(
                "en hosta",
                "noun",
                "Upprepade kraftiga utandningar när halsen eller luftvägarna är irriterade.",
                "Hostan håller mig vaken.",
            ),
            VocabularyEntry(
                "en förkylning",
                "noun",
                "En vanlig infektion med till exempel snuva och hosta.",
                "Jag har fått en förkylning.",
            ),
            VocabularyEntry(
                "en allergi",
                "noun",
                "En reaktion i kroppen mot ett ämne som många andra tål.",
                "Jag har allergi mot pollen.",
            ),
            VocabularyEntry(
                "en medicin",
                "noun",
                "Ett ämne som används för att förebygga eller behandla sjukdom.",
                "Jag frågade hur medicinen ska tas.",
            ),
            VocabularyEntry(
                "ett recept",
                "noun",
                "En ordination som ger rätt att hämta ett visst läkemedel.",
                "Läkaren skrev ett recept.",
            ),
            VocabularyEntry(
                "en tablett",
                "noun",
                "En liten fast bit av ett läkemedel.",
                "Apoteket förklarade hur tabletten ska tas.",
            ),
            VocabularyEntry(
                "en mage",
                "noun",
                "Den del av kroppen där bland annat magsäcken finns.",
                "Jag har ont i magen.",
            ),
            VocabularyEntry(
                "en rygg",
                "noun",
                "Kroppens baksida från nacken ned till höfterna.",
                "Min rygg gör ont.",
            ),
            VocabularyEntry(
                "en fot", "noun", "Kroppsdelen längst ned på benet.", "Jag skadade foten igår."
            ),
            VocabularyEntry(
                "en tand",
                "noun",
                "En hård del i munnen som används när man tuggar.",
                "En tand gör ont.",
            ),
            VocabularyEntry(
                "må", "verb", "Känna sig på ett visst sätt i kropp eller sinne.", "Hur mår du idag?"
            ),
            VocabularyEntry(
                "vila",
                "verb",
                "Ta en paus så att kroppen eller tankarna får återhämta sig.",
                "Jag behöver vila en stund.",
            ),
            VocabularyEntry(
                "andas",
                "verb",
                "Ta in och släppa ut luft genom lungorna.",
                "Hon bad mig andas lugnt.",
            ),
            VocabularyEntry(
                "göra ont", "phrase", "Ge en känsla av smärta.", "Det gör ont när jag går."
            ),
            VocabularyEntry(
                "frisk", "adjective", "Som inte är sjuk.", "Nu känner jag mig frisk igen."
            ),
            VocabularyEntry(
                "orolig",
                "adjective",
                "Som känner att något kan vara fel eller gå dåligt.",
                "Jag är orolig för min vän.",
            ),
            VocabularyEntry(
                "yr",
                "adjective",
                "Som känner att kroppen eller omgivningen snurrar.",
                "Jag blev yr när jag reste mig.",
            ),
            VocabularyEntry(
                "akut", "adjective", "Som behöver hjälp eller åtgärd direkt.", "Ärendet är akut."
            ),
            VocabularyEntry(
                "ett symtom",
                "noun",
                "Ett tecken på en sjukdom eller ett kroppsligt tillstånd.",
                "Vilka symtom har du?",
            ),
        ],
    ),
    VocabularySet(
        "sv_study_work_a2",
        "A2",
        "Studier och arbetsdagar",
        "a2-unit-4",
        [
            VocabularyEntry(
                "ett arbete",
                "noun",
                "Uppgifter man gör, ofta mot betalning.",
                "Jag söker ett nytt arbete.",
            ),
            VocabularyEntry(
                "ett jobb",
                "noun",
                "Ett vardagligt ord för en anställning eller arbetsuppgift.",
                "Hon har fått ett jobb på ett café.",
            ),
            VocabularyEntry(
                "en kollega",
                "noun",
                "En person som man arbetar tillsammans med.",
                "Min kollega börjar senare idag.",
            ),
            VocabularyEntry(
                "en chef",
                "noun",
                "En person som leder arbetet för andra.",
                "Jag frågade min chef om ledighet.",
            ),
            VocabularyEntry(
                "ett möte",
                "noun",
                "Ett planerat tillfälle då människor träffas för att prata om något.",
                "Mötet börjar om tio minuter.",
            ),
            VocabularyEntry(
                "en lön", "noun", "Pengar som man får för sitt arbete.", "Lönen kommer varje månad."
            ),
            VocabularyEntry(
                "ett schema",
                "noun",
                "En plan som visar tider för olika aktiviteter.",
                "Mitt schema ändras nästa vecka.",
            ),
            VocabularyEntry(
                "en uppgift",
                "noun",
                "Något som man ska göra eller lösa.",
                "Vi arbetar med samma uppgift.",
            ),
            VocabularyEntry(
                "en kurs", "noun", "En serie lektioner om ett ämne.", "Jag går en kurs i svenska."
            ),
            VocabularyEntry(
                "en lektion",
                "noun",
                "En bestämd tid för undervisning.",
                "Lektionen varar i en timme.",
            ),
            VocabularyEntry(
                "ett prov",
                "noun",
                "Uppgifter som används för att se vad någon kan.",
                "Vi har prov på fredag.",
            ),
            VocabularyEntry(
                "en läxa", "noun", "Skolarbete som görs mellan lektionerna.", "Jag har gjort läxan."
            ),
            VocabularyEntry(
                "ett betyg",
                "noun",
                "En bedömning av vad en elev har lärt sig.",
                "Hon fick sitt betyg igår.",
            ),
            VocabularyEntry(
                "ett bibliotek",
                "noun",
                "En plats där man kan låna böcker och hitta information.",
                "Jag lånar böcker på biblioteket.",
            ),
            VocabularyEntry(
                "en dator",
                "noun",
                "En apparat som behandlar information och kör program.",
                "Min dator är långsam.",
            ),
            VocabularyEntry(
                "ett mejl",
                "noun",
                "Ett meddelande som skickas elektroniskt till en adress.",
                "Jag skickade ett mejl till läraren.",
            ),
            VocabularyEntry(
                "en fil",
                "noun",
                "Sparad digital information, till exempel en text eller bild.",
                "Kan du öppna filen?",
            ),
            VocabularyEntry(
                "söka", "verb", "Försöka hitta eller få något.", "Jag söker jobb i Malmö."
            ),
            VocabularyEntry(
                "lära sig", "phrase", "Få ny kunskap eller förmåga.", "Hon lär sig att köra bil."
            ),
            VocabularyEntry(
                "öva", "verb", "Göra något flera gånger för att bli bättre.", "Vi övar på uttalet."
            ),
            VocabularyEntry(
                "förklara", "verb", "Göra något lättare att förstå.", "Kan du förklara uppgiften?"
            ),
            VocabularyEntry(
                "skicka",
                "verb",
                "Sända något till en annan person eller plats.",
                "Jag skickar svaret imorgon.",
            ),
            VocabularyEntry(
                "svara",
                "verb",
                "Ge ett svar på en fråga eller ett meddelande.",
                "Hon svarade på mitt mejl.",
            ),
            VocabularyEntry(
                "svår",
                "adjective",
                "Som kräver mycket arbete eller kunskap.",
                "Texten var svår att förstå.",
            ),
            VocabularyEntry(
                "lätt",
                "adjective",
                "Som inte kräver mycket arbete eller kunskap.",
                "Första frågan var lätt.",
            ),
            VocabularyEntry(
                "viktig", "adjective", "Som har stor betydelse.", "Det är viktigt att komma i tid."
            ),
        ],
    ),
    VocabularySet(
        "sv_services_a2",
        "A2",
        "Inköp och service",
        "a2-unit-5",
        [
            VocabularyEntry(
                "ett kvitto",
                "noun",
                "Ett bevis på vad man har köpt och betalat.",
                "Spara kvittot om du vill byta varan.",
            ),
            VocabularyEntry(
                "en vara", "noun", "En sak som säljs i en butik.", "Den här varan är slut."
            ),
            VocabularyEntry(
                "en kund",
                "noun",
                "En person som köper en vara eller tjänst.",
                "Kunden väntar på hjälp.",
            ),
            VocabularyEntry(
                "en kassa", "noun", "En plats där man betalar i en butik.", "Det är kö till kassan."
            ),
            VocabularyEntry(
                "en kö",
                "noun",
                "Människor som väntar på sin tur i en ordning.",
                "Jag stod i kö i tio minuter.",
            ),
            VocabularyEntry(
                "ett erbjudande",
                "noun",
                "Ett förslag att få eller köpa något på vissa villkor.",
                "Erbjudandet gäller till söndag.",
            ),
            VocabularyEntry(
                "en rabatt",
                "noun",
                "En sänkning av det vanliga priset.",
                "Vi fick tio procent rabatt.",
            ),
            VocabularyEntry(
                "en storleksguide",
                "noun",
                "Information som hjälper en att välja rätt mått på kläder.",
                "Jag läste storleksguiden före köpet.",
            ),
            VocabularyEntry(
                "ett paket",
                "noun",
                "Något som är inslaget eller packat för transport.",
                "Mitt paket har kommit.",
            ),
            VocabularyEntry(
                "en leverans",
                "noun",
                "Att en beställd vara kommer till mottagaren.",
                "Leveransen tar tre dagar.",
            ),
            VocabularyEntry(
                "ett postombud",
                "noun",
                "En plats där man kan hämta eller lämna post och paket.",
                "Jag hämtade paketet hos ett postombud.",
            ),
            VocabularyEntry(
                "ett bankkort",
                "noun",
                "Ett kort som används för att betala från ett konto.",
                "Mitt bankkort fungerar inte.",
            ),
            VocabularyEntry(
                "kontanter", "noun", "Pengar i form av sedlar och mynt.", "Tar ni emot kontanter?"
            ),
            VocabularyEntry(
                "en räkning",
                "noun",
                "Ett meddelande om hur mycket man ska betala och när.",
                "Räkningen ska betalas på fredag.",
            ),
            VocabularyEntry(
                "ett konto",
                "noun",
                "En registrerad plats för pengar eller tillgång till en digital tjänst.",
                "Jag behöver logga in på mitt konto.",
            ),
            VocabularyEntry(
                "beställa",
                "verb",
                "Be att få köpa eller få något levererat.",
                "Vi beställde maten på nätet.",
            ),
            VocabularyEntry(
                "byta",
                "verb",
                "Lämna något och få eller ta något annat.",
                "Kan jag byta till en mindre storlek?",
            ),
            VocabularyEntry(
                "lämna tillbaka",
                "phrase",
                "Ge tillbaka något man köpt eller lånat.",
                "Jag vill lämna tillbaka jackan.",
            ),
            VocabularyEntry(
                "prova", "verb", "Testa hur något fungerar eller passar.", "Får jag prova skorna?"
            ),
            VocabularyEntry(
                "passa", "verb", "Ha rätt storlek eller vara lämplig.", "Jackan passar mig bra."
            ),
            VocabularyEntry(
                "spara", "verb", "Behålla något för senare användning.", "Jag sparar kvittot."
            ),
            VocabularyEntry(
                "hämta",
                "verb",
                "Gå till en plats och ta med någon eller något.",
                "Du kan hämta paketet imorgon.",
            ),
            VocabularyEntry(
                "lämna",
                "verb",
                "Ge något till någon eller låta det vara kvar.",
                "Lämna nyckeln i receptionen.",
            ),
            VocabularyEntry(
                "slut",
                "adjective",
                "Som inte längre finns kvar att använda eller köpa.",
                "Mjölken är slut.",
            ),
            VocabularyEntry(
                "öppen",
                "adjective",
                "Som inte är stängd eller som tar emot besökare.",
                "Butiken är öppen till åtta.",
            ),
            VocabularyEntry(
                "stängd",
                "adjective",
                "Som inte är öppen eller inte tar emot besökare.",
                "Receptionen är stängd på natten.",
            ),
        ],
    ),
    VocabularySet(
        "sv_social_a2",
        "A2",
        "Relationer och gemensamma planer",
        "a2-unit-6",
        [
            VocabularyEntry(
                "en inbjudan",
                "noun",
                "Ett meddelande som ber någon komma till en aktivitet.",
                "Tack för inbjudan till festen.",
            ),
            VocabularyEntry(
                "en fest",
                "noun",
                "En träff för att fira eller ha roligt tillsammans.",
                "Vi ordnar en fest på lördag.",
            ),
            VocabularyEntry(
                "en födelsedag", "noun", "Årsdagen av när någon föddes.", "Min födelsedag är i maj."
            ),
            VocabularyEntry(
                "en present",
                "noun",
                "Något man ger till någon utan betalning.",
                "Jag köpte en present till min vän.",
            ),
            VocabularyEntry(
                "en gäst",
                "noun",
                "En person som besöker någon eller deltar efter en inbjudan.",
                "Gästerna kommer klockan sex.",
            ),
            VocabularyEntry(
                "en värd", "noun", "En person som tar emot gäster.", "Vår värd visade oss runt."
            ),
            VocabularyEntry(
                "en släkting",
                "noun",
                "En person som hör till ens släkt.",
                "Vi besökte släktingar i helgen.",
            ),
            VocabularyEntry(
                "en kusin",
                "noun",
                "Ett barn till en av ens föräldrars syskon.",
                "Min kusin bor i Västerås.",
            ),
            VocabularyEntry(
                "en partner",
                "noun",
                "En person som man har en nära kärleksrelation med.",
                "Min partner följer med.",
            ),
            VocabularyEntry(
                "en sambo",
                "noun",
                "En partner som man bor tillsammans med utan att vara gift.",
                "Jag och min sambo lagar mat tillsammans.",
            ),
            VocabularyEntry(
                "en hobby",
                "noun",
                "Något man gör på fritiden för att det är roligt.",
                "Min hobby är att fotografera.",
            ),
            VocabularyEntry(
                "en förening",
                "noun",
                "En grupp som organiserar sig kring ett gemensamt intresse.",
                "Hon är med i en idrottsförening.",
            ),
            VocabularyEntry(
                "ett lag",
                "noun",
                "En grupp som spelar eller tävlar tillsammans.",
                "Vårt lag tränar på onsdagar.",
            ),
            VocabularyEntry(
                "en utflykt",
                "noun",
                "En kortare resa för att se eller göra något.",
                "Vi gjorde en utflykt till havet.",
            ),
            VocabularyEntry(
                "ett museum",
                "noun",
                "En plats där föremål och berättelser visas för besökare.",
                "Museet är stängt på måndagar.",
            ),
            VocabularyEntry(
                "en konsert",
                "noun",
                "Ett tillfälle då musik framförs för en publik.",
                "Vi gick på konsert igår.",
            ),
            VocabularyEntry(
                "bjuda",
                "verb",
                "Erbjuda något eller be någon komma.",
                "Jag vill bjuda dig på middag.",
            ),
            VocabularyEntry(
                "fira",
                "verb",
                "Uppmärksamma något positivt med en särskild aktivitet.",
                "Vi firar hennes födelsedag.",
            ),
            VocabularyEntry(
                "följa med",
                "phrase",
                "Gå eller åka tillsammans med någon.",
                "Vill du följa med till museet?",
            ),
            VocabularyEntry("träffas", "verb", "Möta varandra.", "Vi träffas utanför stationen."),
            VocabularyEntry(
                "bestämma",
                "verb",
                "Välja hur något ska vara eller göras.",
                "Vi bestämde en tid för mötet.",
            ),
            VocabularyEntry(
                "lova", "verb", "Säga att man säkert ska göra något.", "Jag lovade att ringa."
            ),
            VocabularyEntry(
                "glömma", "verb", "Inte komma ihåg något.", "Jag glömde hennes adress."
            ),
            VocabularyEntry(
                "komma ihåg", "phrase", "Ha kvar något i minnet.", "Kommer du ihåg tiden?"
            ),
            VocabularyEntry(
                "gärna", "adverb", "Med vilja och positiv inställning.", "Jag följer gärna med."
            ),
            VocabularyEntry(
                "tyvärr",
                "adverb",
                "Ett ord som visar att något är tråkigt eller beklagligt.",
                "Tyvärr kan jag inte komma.",
            ),
        ],
    ),
    VocabularySet(
        "sv_planning_a2",
        "A2",
        "Tid, årstider och praktiska villkor",
        "a2-unit-7",
        [
            VocabularyEntry("januari", "noun", "Årets första månad.", "Kursen börjar i januari."),
            VocabularyEntry("februari", "noun", "Årets andra månad.", "Vi flyttade i februari."),
            VocabularyEntry("mars", "noun", "Årets tredje månad.", "Mötet är den tredje mars."),
            VocabularyEntry("april", "noun", "Årets fjärde månad.", "Hon kommer i april."),
            VocabularyEntry("maj", "noun", "Årets femte månad.", "Jag fyller år i maj."),
            VocabularyEntry("juni", "noun", "Årets sjätte månad.", "Skolan slutar i juni."),
            VocabularyEntry("juli", "noun", "Årets sjunde månad.", "Vi har semester i juli."),
            VocabularyEntry("augusti", "noun", "Årets åttonde månad.", "Arbetet börjar i augusti."),
            VocabularyEntry("september", "noun", "Årets nionde månad.", "Vi ses i september."),
            VocabularyEntry("oktober", "noun", "Årets tionde månad.", "Hon flyttar i oktober."),
            VocabularyEntry(
                "november", "noun", "Årets elfte månad.", "Det blir ofta mörkt tidigt i november."
            ),
            VocabularyEntry(
                "december",
                "noun",
                "Årets tolfte månad.",
                "Biblioteket har ändrade tider i december.",
            ),
            VocabularyEntry(
                "en vår",
                "noun",
                "Årstiden mellan vinter och sommar.",
                "På våren blir dagarna längre.",
            ),
            VocabularyEntry(
                "en höst",
                "noun",
                "Årstiden mellan sommar och vinter.",
                "På hösten börjar många kurser.",
            ),
            VocabularyEntry(
                "ett datum",
                "noun",
                "En bestämd dag uttryckt med dag, månad och ibland år.",
                "Vilket datum passar dig?",
            ),
            VocabularyEntry(
                "en helg",
                "noun",
                "Dagar som ofta är lediga, särskilt lördag och söndag.",
                "Vad gjorde du i helgen?",
            ),
            VocabularyEntry(
                "en vardag",
                "noun",
                "En vanlig arbetsdag, till skillnad från helgdag.",
                "Bussen går oftare på vardagar.",
            ),
            VocabularyEntry(
                "en eftermiddag",
                "noun",
                "Tiden efter lunch och före kväll.",
                "Jag kan komma på eftermiddagen.",
            ),
            VocabularyEntry(
                "en förmiddag",
                "noun",
                "Tiden mellan morgon och mitt på dagen.",
                "Vi arbetar hela förmiddagen.",
            ),
            VocabularyEntry(
                "en stund", "noun", "En kortare tid utan exakt längd.", "Kan du vänta en stund?"
            ),
            VocabularyEntry(
                "ofta",
                "adverb",
                "Många gånger eller med kort tid mellan tillfällena.",
                "Vi går ofta till biblioteket.",
            ),
            VocabularyEntry("sällan", "adverb", "Inte många gånger.", "Jag åker sällan taxi."),
            VocabularyEntry(
                "aldrig", "adverb", "Inte vid något tillfälle.", "Jag har aldrig varit där."
            ),
            VocabularyEntry(
                "alltid", "adverb", "Vid varje relevant tillfälle.", "Hon kommer alltid i tid."
            ),
            VocabularyEntry(
                "tidig",
                "adjective",
                "Som sker före den vanliga eller väntade tiden.",
                "Vi tog ett tidigt tåg.",
            ),
            VocabularyEntry(
                "sen",
                "adjective",
                "Som sker efter den väntade eller planerade tiden.",
                "Jag blev sen eftersom bussen inte kom.",
            ),
        ],
    ),
]
