"""Swedish A1 vocabulary: concrete meanings and usable example sentences."""

from app.data._types import VocabularyEntry, VocabularySet

A1_SETS: list[VocabularySet] = [
    VocabularySet(
        "sv_identity_a1",
        "A1",
        "Namn, kontakt och språk",
        "a1-unit-1",
        [
            VocabularyEntry("hej", "phrase", "En vanlig hälsning.", "Hej, jag heter Sara."),
            VocabularyEntry(
                "hej då", "phrase", "Ord när man lämnar någon.", "Hej då, vi ses imorgon!"
            ),
            VocabularyEntry(
                "tack",
                "phrase",
                "Ett ord som visar att man är glad för hjälpen.",
                "Tack för hjälpen!",
            ),
            VocabularyEntry(
                "ursäkta",
                "phrase",
                "Ett ord för att be om förlåtelse eller få kontakt.",
                "Ursäkta, vad heter du?",
            ),
            VocabularyEntry("ja", "adverb", "Ett positivt svar på en fråga.", "Ja, jag bor här."),
            VocabularyEntry(
                "nej", "adverb", "Ett negativt svar på en fråga.", "Nej, jag är inte lärare."
            ),
            VocabularyEntry(
                "ett namn", "noun", "Det som en person eller sak kallas.", "Mitt namn är Ali."
            ),
            VocabularyEntry("heta", "verb", "Ha ett visst namn.", "Vad heter du?"),
            VocabularyEntry(
                "vara", "verb", "Ett verb som bland annat säger vem någon är.", "Jag är student."
            ),
            VocabularyEntry("bo", "verb", "Ha sitt hem på en plats.", "Vi bor i Lund."),
            VocabularyEntry(
                "komma",
                "verb",
                "Förflytta sig hit eller till en nämnd plats.",
                "Hon kommer imorgon.",
            ),
            VocabularyEntry(
                "ett land",
                "noun",
                "Ett område med en egen stat, till exempel Sverige.",
                "Vilket land kommer du från?",
            ),
            VocabularyEntry(
                "en stad",
                "noun",
                "En större plats med många hus och människor.",
                "Göteborg är en stad.",
            ),
            VocabularyEntry(
                "ett språk",
                "noun",
                "Ord och regler som människor använder för att förstå varandra.",
                "Vilka språk talar du?",
            ),
            VocabularyEntry(
                "svenska",
                "noun",
                "Ett språk som talas bland annat i Sverige och Finland.",
                "Jag lär mig svenska.",
            ),
            VocabularyEntry(
                "tala", "verb", "Använda rösten för att säga ord.", "Talar du svenska?"
            ),
            VocabularyEntry("förstå", "verb", "Veta vad något betyder.", "Jag förstår frågan."),
            VocabularyEntry(
                "lyssna",
                "verb",
                "Försöka höra vad någon säger eller vad som låter.",
                "Vi lyssnar på läraren.",
            ),
            VocabularyEntry("läsa", "verb", "Se skrivna ord och förstå dem.", "Jag läser en bok."),
            VocabularyEntry(
                "skriva",
                "verb",
                "Göra bokstäver och ord på papper eller skärm.",
                "Skriv ditt namn här.",
            ),
            VocabularyEntry(
                "en bokstav", "noun", "Ett tecken i alfabetet.", "Å är en svensk bokstav."
            ),
            VocabularyEntry(
                "ett ord",
                "noun",
                "En del av språket med en betydelse.",
                "Vad betyder det här ordet?",
            ),
            VocabularyEntry(
                "en fråga", "noun", "Något man säger för att få ett svar.", "Jag har en fråga."
            ),
            VocabularyEntry(
                "ett svar", "noun", "Något man säger efter en fråga.", "Tack för ditt svar."
            ),
            VocabularyEntry(
                "en adress", "noun", "Uppgift om var någon bor eller finns.", "Vad är din adress?"
            ),
            VocabularyEntry(
                "ett telefonnummer",
                "noun",
                "Siffror som man använder för att ringa någon.",
                "Kan jag få ditt telefonnummer?",
            ),
            VocabularyEntry(
                "en lärare",
                "noun",
                "En person som hjälper andra att lära sig något.",
                "Vår lärare heter Eva.",
            ),
            VocabularyEntry(
                "en elev",
                "noun",
                "En person som går i skolan eller får undervisning.",
                "Det finns tio elever i rummet.",
            ),
        ],
    ),
    VocabularySet(
        "sv_people_a1",
        "A1",
        "Människor, familj och egenskaper",
        "a1-unit-2",
        [
            VocabularyEntry(
                "en familj",
                "noun",
                "Människor som hör ihop som till exempel föräldrar och barn.",
                "Min familj bor här.",
            ),
            VocabularyEntry("en mamma", "noun", "En kvinnlig förälder.", "Min mamma heter Anna."),
            VocabularyEntry("en pappa", "noun", "En manlig förälder.", "Min pappa arbetar idag."),
            VocabularyEntry(
                "ett barn",
                "noun",
                "En ung människa; också någons son eller dotter.",
                "Hon har två barn.",
            ),
            VocabularyEntry(
                "en syster",
                "noun",
                "En flicka eller kvinna som har en förälder gemensam med en annan person.",
                "Min syster är tio år.",
            ),
            VocabularyEntry(
                "en bror",
                "noun",
                "En pojke eller man som har en förälder gemensam med en annan person.",
                "Min bror bor i Uppsala.",
            ),
            VocabularyEntry(
                "en vän",
                "noun",
                "En person som man tycker om och gärna träffar.",
                "Sara är min vän.",
            ),
            VocabularyEntry("en person", "noun", "En människa.", "Tre personer väntar här."),
            VocabularyEntry(
                "en kvinna", "noun", "En vuxen människa av kvinnligt kön.", "Kvinnan heter Lina."
            ),
            VocabularyEntry(
                "en man", "noun", "En vuxen människa av manligt kön.", "Mannen är lärare."
            ),
            VocabularyEntry("en flicka", "noun", "Ett barn som är tjej.", "Flickan läser en bok."),
            VocabularyEntry("en pojke", "noun", "Ett barn som är kille.", "Pojken spelar fotboll."),
            VocabularyEntry(
                "en hund", "noun", "Ett vanligt husdjur som kan skälla.", "Vår hund är liten."
            ),
            VocabularyEntry(
                "en katt", "noun", "Ett vanligt husdjur som kan jama.", "Katten sover."
            ),
            VocabularyEntry(
                "stor",
                "adjective",
                "Med mycket utrymme eller storlek; motsatsen till liten.",
                "Vi har ett stort bord.",
            ),
            VocabularyEntry(
                "liten",
                "adjective",
                "Med lite utrymme eller storlek; motsatsen till stor.",
                "Hon har en liten väska.",
            ),
            VocabularyEntry(
                "gammal", "adjective", "Som har levt eller funnits länge.", "Huset är gammalt."
            ),
            VocabularyEntry("ung", "adjective", "Som inte har levt så länge.", "Läraren är ung."),
            VocabularyEntry(
                "glad", "adjective", "Som känner att något är bra eller roligt.", "Barnen är glada."
            ),
            VocabularyEntry(
                "trött", "adjective", "Som behöver vila eller sova.", "Jag är trött ikväll."
            ),
            VocabularyEntry(
                "snäll", "adjective", "Som är vänlig och vill andra väl.", "Min granne är snäll."
            ),
            VocabularyEntry(
                "lång",
                "adjective",
                "Med stort avstånd från ena änden till den andra.",
                "Min bror är lång.",
            ),
            VocabularyEntry(
                "kort",
                "adjective",
                "Med litet avstånd från ena änden till den andra.",
                "Hon har kort hår.",
            ),
            VocabularyEntry(
                "ett hår",
                "noun",
                "En tunn tråd som växer på kroppen; hår på huvudet används som mängdord.",
                "Han har brunt hår.",
            ),
            VocabularyEntry(
                "ett öga", "noun", "En kroppsdel som man ser med.", "Hon har blå ögon."
            ),
            VocabularyEntry(
                "en hand",
                "noun",
                "Kroppsdelen längst ut på armen med fingrar.",
                "Min hand är kall.",
            ),
            VocabularyEntry(
                "ha",
                "verb",
                "Äga något eller vara tillsammans med något som hör till en.",
                "Jag har en syster.",
            ),
            VocabularyEntry(
                "tycka om",
                "phrase",
                "Känna att någon eller något är bra.",
                "Jag tycker om min katt.",
            ),
        ],
    ),
    VocabularySet(
        "sv_day_a1",
        "A1",
        "Dagen, veckan och klockan",
        "a1-unit-3",
        [
            VocabularyEntry(
                "en dag",
                "noun",
                "Tiden från en midnatt till nästa; också den ljusa delen av dygnet.",
                "Idag är en bra dag.",
            ),
            VocabularyEntry(
                "en morgon", "noun", "Den första delen av dagen.", "Jag läser på morgonen."
            ),
            VocabularyEntry(
                "en kväll", "noun", "Tiden efter eftermiddagen och före natten.", "Vi ses ikväll."
            ),
            VocabularyEntry(
                "en natt",
                "noun",
                "Den del av dygnet då det normalt är mörkt.",
                "Jag sover på natten.",
            ),
            VocabularyEntry(
                "en vecka", "noun", "Sju dagar tillsammans.", "Jag arbetar fem dagar i veckan."
            ),
            VocabularyEntry(
                "en månad",
                "noun",
                "En av årets tolv delar, till exempel januari.",
                "Juni är en månad.",
            ),
            VocabularyEntry("ett år", "noun", "Tolv månader tillsammans.", "Barnet är tre år."),
            VocabularyEntry(
                "måndag", "noun", "Veckodagen efter söndag.", "Kursen börjar på måndag."
            ),
            VocabularyEntry("tisdag", "noun", "Veckodagen efter måndag.", "På tisdag arbetar jag."),
            VocabularyEntry(
                "onsdag", "noun", "Veckodagen mellan tisdag och torsdag.", "Vi ses på onsdag."
            ),
            VocabularyEntry(
                "torsdag", "noun", "Veckodagen efter onsdag.", "Hon kommer på torsdag."
            ),
            VocabularyEntry("fredag", "noun", "Veckodagen före lördag.", "På fredag är jag ledig."),
            VocabularyEntry(
                "lördag", "noun", "Veckodagen mellan fredag och söndag.", "Vi spelar på lördag."
            ),
            VocabularyEntry(
                "söndag", "noun", "Veckodagen före måndag.", "Butiken är stängd på söndag."
            ),
            VocabularyEntry("idag", "adverb", "Den dag som är nu.", "Idag är jag hemma."),
            VocabularyEntry("imorgon", "adverb", "Dagen efter idag.", "Imorgon kommer min vän."),
            VocabularyEntry("igår", "adverb", "Dagen före idag.", "Igår var jag i skolan."),
            VocabularyEntry("nu", "adverb", "Vid den här tidpunkten.", "Jag kommer nu."),
            VocabularyEntry("en timme", "noun", "Sextio minuter.", "Lektionen tar en timme."),
            VocabularyEntry("en minut", "noun", "Sextio sekunder.", "Vänta en minut."),
            VocabularyEntry("en klocka", "noun", "Något som visar tiden.", "Min klocka är ny."),
            VocabularyEntry(
                "halv",
                "adjective",
                "En av två lika stora delar; används också om tid före nästa hel timme.",
                "Vi ses klockan halv nio.",
            ),
            VocabularyEntry(
                "arbeta",
                "verb",
                "Göra uppgifter i ett jobb eller annan verksamhet.",
                "Jag arbetar på en skola.",
            ),
            VocabularyEntry("sova", "verb", "Vila utan att vara vaken.", "Barnet sover nu."),
            VocabularyEntry("vakna", "verb", "Sluta sova.", "Jag vaknar klockan sju."),
            VocabularyEntry(
                "börja", "verb", "Göra den första delen av något.", "Vi börjar klockan åtta."
            ),
            VocabularyEntry(
                "sluta", "verb", "Inte fortsätta med något.", "Jag slutar arbeta klockan fem."
            ),
            VocabularyEntry(
                "en rast",
                "noun",
                "En kort paus från arbete eller lektion.",
                "Vi har rast klockan tio.",
            ),
            VocabularyEntry(
                "noll",
                "numeral",
                "Talet som anger att inget finns att räkna.",
                "Det är noll grader ute.",
            ),
            VocabularyEntry(
                "ett",
                "numeral",
                "Det första positiva heltalet; en används med en-ord.",
                "Jag har ett barn och en hund.",
            ),
            VocabularyEntry(
                "två", "numeral", "Antalet efter ett och före tre.", "Jag vill ha två biljetter."
            ),
            VocabularyEntry(
                "tre", "numeral", "Antalet efter två och före fyra.", "Vi är tre personer."
            ),
            VocabularyEntry(
                "fyra", "numeral", "Antalet efter tre och före fem.", "Det finns fyra stolar."
            ),
            VocabularyEntry(
                "fem",
                "numeral",
                "Antalet efter fyra och före sex.",
                "Jag arbetar fem dagar i veckan.",
            ),
            VocabularyEntry("sex", "numeral", "Antalet efter fem och före sju.", "Klockan är sex."),
            VocabularyEntry(
                "sju", "numeral", "Antalet efter sex och före åtta.", "En vecka har sju dagar."
            ),
            VocabularyEntry(
                "åtta", "numeral", "Antalet efter sju och före nio.", "Vi börjar klockan åtta."
            ),
            VocabularyEntry(
                "nio", "numeral", "Antalet efter åtta och före tio.", "Bussen går klockan nio."
            ),
            VocabularyEntry(
                "tio", "numeral", "Antalet efter nio och före elva.", "Det kostar tio kronor."
            ),
            VocabularyEntry("elva", "numeral", "Tio plus ett.", "Det finns elva elever här."),
            VocabularyEntry("tolv", "numeral", "Tio plus två.", "Ett år har tolv månader."),
            VocabularyEntry("tretton", "numeral", "Tio plus tre.", "Barnet är tretton år."),
            VocabularyEntry("fjorton", "numeral", "Tio plus fyra.", "Vi har fjorton böcker."),
            VocabularyEntry("femton", "numeral", "Tio plus fem.", "En kvart är femton minuter."),
            VocabularyEntry("sexton", "numeral", "Tio plus sex.", "Mötet börjar klockan sexton."),
            VocabularyEntry("sjutton", "numeral", "Tio plus sju.", "Det kostar sjutton kronor."),
            VocabularyEntry("arton", "numeral", "Tio plus åtta.", "Hon är arton år."),
            VocabularyEntry("nitton", "numeral", "Tio plus nio.", "Vi ses klockan nitton."),
            VocabularyEntry("tjugo", "numeral", "Två gånger tio.", "Det kostar tjugo kronor."),
            VocabularyEntry(
                "trettio", "numeral", "Tre gånger tio.", "En halvtimme är trettio minuter."
            ),
            VocabularyEntry("fyrtio", "numeral", "Fyra gånger tio.", "Resan tar fyrtio minuter."),
            VocabularyEntry(
                "femtio", "numeral", "Fem gånger tio.", "Biljetten kostar femtio kronor."
            ),
            VocabularyEntry("sextio", "numeral", "Sex gånger tio.", "En timme är sextio minuter."),
            VocabularyEntry(
                "sjuttio", "numeral", "Sju gånger tio.", "Boken kostar sjuttio kronor."
            ),
            VocabularyEntry(
                "åttio", "numeral", "Åtta gånger tio.", "Biljetten kostar åttio kronor."
            ),
            VocabularyEntry(
                "nittio", "numeral", "Nio gånger tio.", "Filmen är nittio minuter lång."
            ),
            VocabularyEntry("hundra", "numeral", "Tio gånger tio.", "Jag betalar hundra kronor."),
            VocabularyEntry(
                "tusen", "numeral", "Tio gånger hundra.", "Cykeln kostar tusen kronor."
            ),
        ],
    ),
    VocabularySet(
        "sv_food_a1",
        "A1",
        "Mat, dryck och inköp",
        "a1-unit-4",
        [
            VocabularyEntry("mat", "noun", "Det som man äter för att få energi.", "Maten är god."),
            VocabularyEntry(
                "vatten",
                "noun",
                "En klar vätska som människor behöver dricka.",
                "Jag vill ha vatten.",
            ),
            VocabularyEntry(
                "kaffe", "noun", "En mörk dryck av rostade bönor.", "Dricker du kaffe?"
            ),
            VocabularyEntry(
                "te",
                "noun",
                "En dryck som ofta görs av blad och varmt vatten.",
                "Jag dricker te på kvällen.",
            ),
            VocabularyEntry(
                "mjölk", "noun", "En vit dryck, till exempel från kor.", "Det finns mjölk i kylen."
            ),
            VocabularyEntry(
                "bröd", "noun", "Mat som bakas av bland annat mjöl och vatten.", "Jag köper bröd."
            ),
            VocabularyEntry(
                "ost",
                "noun",
                "Mat som görs av mjölk och ofta läggs på bröd.",
                "Vill du ha ost på smörgåsen?",
            ),
            VocabularyEntry(
                "ett ägg", "noun", "Rund mat med skal, ofta från en höna.", "Jag äter ett ägg."
            ),
            VocabularyEntry(
                "en fisk",
                "noun",
                "Ett djur som lever i vatten; också mat från sådana djur.",
                "Vi äter fisk idag.",
            ),
            VocabularyEntry(
                "ris",
                "noun",
                "Små korn som ofta kokas och äts till annan mat.",
                "Jag vill ha ris till maten.",
            ),
            VocabularyEntry(
                "en potatis",
                "noun",
                "En knöl som växer i jorden och används som mat.",
                "Jag kokar potatis.",
            ),
            VocabularyEntry(
                "ett äpple",
                "noun",
                "En rund frukt som kan vara röd, grön eller gul.",
                "Äpplet är grönt.",
            ),
            VocabularyEntry(
                "en banan",
                "noun",
                "En lång frukt med skal som ofta är gult.",
                "Barnet äter en banan.",
            ),
            VocabularyEntry(
                "en tomat",
                "noun",
                "En saftig frukt som ofta används som grönsak i sallad.",
                "Jag vill ha två tomater.",
            ),
            VocabularyEntry(
                "en frukost", "noun", "Dagens första måltid.", "Jag äter frukost klockan sju."
            ),
            VocabularyEntry(
                "en lunch", "noun", "En måltid mitt på dagen.", "Vi äter lunch tillsammans."
            ),
            VocabularyEntry(
                "en middag",
                "noun",
                "Dagens större måltid, ofta på eftermiddagen eller kvällen.",
                "Middagen är klar.",
            ),
            VocabularyEntry("äta", "verb", "Ta mat i munnen och svälja den.", "Vad vill du äta?"),
            VocabularyEntry("dricka", "verb", "Ta in vätska genom munnen.", "Jag dricker vatten."),
            VocabularyEntry("köpa", "verb", "Få något genom att betala.", "Vi köper mjölk."),
            VocabularyEntry("betala", "verb", "Ge pengar för något.", "Kan jag betala med kort?"),
            VocabularyEntry("kosta", "verb", "Ha ett visst pris.", "Vad kostar brödet?"),
            VocabularyEntry(
                "en krona", "noun", "Enheten för svenska pengar.", "Det kostar tjugo kronor."
            ),
            VocabularyEntry(
                "hungrig", "adjective", "Som behöver eller vill äta.", "Jag är hungrig."
            ),
            VocabularyEntry(
                "törstig", "adjective", "Som behöver eller vill dricka.", "Vi är törstiga."
            ),
            VocabularyEntry(
                "god", "adjective", "Som smakar bra, när ordet beskriver mat.", "Soppan är god."
            ),
            VocabularyEntry(
                "en kopp",
                "noun",
                "Ett litet kärl för till exempel kaffe eller te.",
                "Jag vill ha en kopp te.",
            ),
            VocabularyEntry(
                "ett glas", "noun", "Ett kärl som man kan dricka ur.", "Kan jag få ett glas vatten?"
            ),
        ],
    ),
    VocabularySet(
        "sv_home_a1",
        "A1",
        "Hemma och i närområdet",
        "a1-unit-5",
        [
            VocabularyEntry(
                "ett hus", "noun", "En byggnad där människor kan bo eller arbeta.", "Huset är gult."
            ),
            VocabularyEntry(
                "en lägenhet",
                "noun",
                "En bostad som är en del av ett större hus.",
                "Vi bor i en liten lägenhet.",
            ),
            VocabularyEntry(
                "ett rum", "noun", "En del av en byggnad med väggar runt.", "Mitt rum är ljust."
            ),
            VocabularyEntry(
                "ett kök", "noun", "Ett rum där man lagar mat.", "Bordet står i köket."
            ),
            VocabularyEntry(
                "ett badrum",
                "noun",
                "Ett rum där man kan tvätta sig och ofta duscha.",
                "Var är badrummet?",
            ),
            VocabularyEntry(
                "en dörr",
                "noun",
                "En del som öppnas för att gå in eller ut.",
                "Öppna dörren, tack.",
            ),
            VocabularyEntry(
                "ett fönster",
                "noun",
                "En öppning med glas som släpper in ljus.",
                "Fönstret är öppet.",
            ),
            VocabularyEntry(
                "ett bord",
                "noun",
                "En möbel med en skiva som man kan äta eller arbeta vid.",
                "Boken ligger på bordet.",
            ),
            VocabularyEntry(
                "en stol", "noun", "En möbel för en person att sitta på.", "Det finns fyra stolar."
            ),
            VocabularyEntry(
                "en säng", "noun", "En möbel som man sover i.", "Barnet ligger i sängen."
            ),
            VocabularyEntry("en lampa", "noun", "Något som ger ljus.", "Lampan står på bordet."),
            VocabularyEntry(
                "en nyckel",
                "noun",
                "Ett föremål som används för att öppna ett lås.",
                "Var är min nyckel?",
            ),
            VocabularyEntry(
                "en gata", "noun", "En väg mellan hus i en stad eller ort.", "Vi bor på samma gata."
            ),
            VocabularyEntry(
                "en butik", "noun", "En plats där man köper saker.", "Butiken öppnar klockan nio."
            ),
            VocabularyEntry(
                "ett apotek",
                "noun",
                "En plats där man köper läkemedel.",
                "Finns det ett apotek här?",
            ),
            VocabularyEntry(
                "en skola",
                "noun",
                "En plats där elever får undervisning.",
                "Skolan ligger nära huset.",
            ),
            VocabularyEntry(
                "en buss",
                "noun",
                "Ett stort fordon som tar flera passagerare på väg.",
                "Jag tar bussen till skolan.",
            ),
            VocabularyEntry(
                "ett tåg", "noun", "Ett fordon som går på räls.", "Tåget går klockan tio."
            ),
            VocabularyEntry(
                "en cykel", "noun", "Ett fordon med två hjul som man trampar.", "Min cykel är röd."
            ),
            VocabularyEntry(
                "en biljett",
                "noun",
                "Ett bevis på att man får resa eller gå in någonstans.",
                "Jag köper en biljett.",
            ),
            VocabularyEntry(
                "en station",
                "noun",
                "En plats där till exempel tåg stannar.",
                "Vi ses vid stationen.",
            ),
            VocabularyEntry("nära", "adverb", "På kort avstånd.", "Jag bor nära skolan."),
            VocabularyEntry("här", "adverb", "På den här platsen.", "Sitt här!"),
            VocabularyEntry("där", "adverb", "På den platsen.", "Bussen stannar där."),
            VocabularyEntry("hemma", "adverb", "I den bostad där man bor.", "Jag är hemma idag."),
            VocabularyEntry("gå", "verb", "Förflytta sig med steg.", "Vi går till butiken."),
            VocabularyEntry("åka", "verb", "Förflytta sig med ett fordon.", "Jag åker tåg."),
            VocabularyEntry(
                "öppna",
                "verb",
                "Göra så att något inte längre är stängt.",
                "Kan du öppna fönstret?",
            ),
        ],
    ),
    VocabularySet(
        "sv_leisure_a1",
        "A1",
        "Fritid, väder och planer",
        "a1-unit-6",
        [
            VocabularyEntry(
                "en bok",
                "noun",
                "Sidor med text eller bilder som hör ihop.",
                "Jag läser en bra bok.",
            ),
            VocabularyEntry(
                "en film", "noun", "Rörliga bilder som berättar något.", "Vi ser en film ikväll."
            ),
            VocabularyEntry(
                "musik",
                "noun",
                "Ljud och toner som bildar till exempel en melodi.",
                "Jag lyssnar på musik.",
            ),
            VocabularyEntry(
                "en sång", "noun", "Musik med ord som man sjunger.", "Barnen sjunger en sång."
            ),
            VocabularyEntry(
                "en park",
                "noun",
                "Ett grönt område där man kan promenera och vila.",
                "Vi går i parken.",
            ),
            VocabularyEntry(
                "en promenad",
                "noun",
                "En tur till fots, ofta för nöjes skull.",
                "Vi tar en promenad.",
            ),
            VocabularyEntry(
                "fotboll",
                "noun",
                "En sport där två lag försöker sparka en boll i mål.",
                "Hon spelar fotboll.",
            ),
            VocabularyEntry(
                "simma", "verb", "Förflytta sig i vatten med kroppen.", "Kan du simma?"
            ),
            VocabularyEntry(
                "spela",
                "verb",
                "Delta i ett spel eller använda ett musikinstrument.",
                "Han spelar piano.",
            ),
            VocabularyEntry("sjunga", "verb", "Göra musik med rösten.", "Vi sjunger tillsammans."),
            VocabularyEntry("dansa", "verb", "Röra kroppen till musik.", "Vill du dansa?"),
            VocabularyEntry("träffa", "verb", "Möta en person.", "Jag träffar min vän på fredag."),
            VocabularyEntry(
                "vilja", "verb", "Ha en önskan att göra eller få något.", "Jag vill spela idag."
            ),
            VocabularyEntry(
                "kunna", "verb", "Ha förmåga eller möjlighet att göra något.", "Hon kan simma."
            ),
            VocabularyEntry(
                "ledig",
                "adjective",
                "Som inte behöver arbeta eller gå i skolan just då.",
                "Jag är ledig imorgon.",
            ),
            VocabularyEntry(
                "rolig",
                "adjective",
                "Som ger glädje eller får någon att skratta.",
                "Filmen är rolig.",
            ),
            VocabularyEntry(
                "bra", "adjective", "Som har god kvalitet eller fungerar väl.", "Det är en bra bok."
            ),
            VocabularyEntry(
                "dålig",
                "adjective",
                "Som inte har god kvalitet eller inte fungerar väl.",
                "Bilden är dålig.",
            ),
            VocabularyEntry("varm", "adjective", "Med ganska hög temperatur.", "Soppan är varm."),
            VocabularyEntry("kall", "adjective", "Med låg temperatur.", "Vattnet är kallt."),
            VocabularyEntry(
                "en sol", "noun", "Stjärnan som ger jorden ljus och värme.", "Solen skiner idag."
            ),
            VocabularyEntry(
                "regn", "noun", "Vatten som faller från moln.", "Det kommer regn ikväll."
            ),
            VocabularyEntry(
                "snö",
                "noun",
                "Vita iskristaller som faller från himlen.",
                "Det ligger snö på marken.",
            ),
            VocabularyEntry(
                "väder",
                "noun",
                "Hur luften och himlen är, till exempel soligt eller regnigt.",
                "Vilket fint väder!",
            ),
            VocabularyEntry(
                "en sommar", "noun", "Årstiden mellan vår och höst.", "På sommaren badar vi."
            ),
            VocabularyEntry(
                "en vinter",
                "noun",
                "Årstiden mellan höst och vår.",
                "På vintern är det ofta kallt.",
            ),
            VocabularyEntry(
                "tillsammans", "adverb", "Med varandra, inte ensam.", "Vi lagar mat tillsammans."
            ),
            VocabularyEntry(
                "vänta",
                "verb",
                "Stanna tills något händer eller någon kommer.",
                "Jag väntar på bussen.",
            ),
        ],
    ),
    VocabularySet(
        "sv_errands_a1",
        "A1",
        "Kläder, hjälp och enkla ärenden",
        "a1-unit-7",
        [
            VocabularyEntry(
                "en jacka", "noun", "Ett ytterplagg för överkroppen.", "Min jacka är blå."
            ),
            VocabularyEntry(
                "en tröja",
                "noun",
                "Ett plagg för överkroppen, ofta med ärmar.",
                "Jag har en varm tröja.",
            ),
            VocabularyEntry(
                "en sko", "noun", "Något man har på foten utomhus.", "Var är mina skor?"
            ),
            VocabularyEntry(
                "ett par", "noun", "Två saker som hör ihop.", "Jag köper ett par skor."
            ),
            VocabularyEntry(
                "en väska", "noun", "Något som man bär saker i.", "Nyckeln ligger i väskan."
            ),
            VocabularyEntry(
                "röd", "adjective", "Med färg som en mogen tomat.", "Jag vill ha den röda jackan."
            ),
            VocabularyEntry("blå", "adjective", "Med färg som en klar himmel.", "Bilen är blå."),
            VocabularyEntry("grön", "adjective", "Med färg som gräs.", "Äpplet är grönt."),
            VocabularyEntry("svart", "adjective", "Med den mörkaste färgen.", "Skorna är svarta."),
            VocabularyEntry("vit", "adjective", "Med färg som snö.", "Huset är vitt."),
            VocabularyEntry(
                "en storlek",
                "noun",
                "Ett mått som visar hur stort något är.",
                "Har ni en större storlek?",
            ),
            VocabularyEntry(
                "ett pris", "noun", "Hur mycket pengar något kostar.", "Vad är priset?"
            ),
            VocabularyEntry(
                "billig", "adjective", "Som kostar lite pengar.", "Den här väskan är billig."
            ),
            VocabularyEntry("dyr", "adjective", "Som kostar mycket pengar.", "Jackan är dyr."),
            VocabularyEntry(
                "ny",
                "adjective",
                "Som inte har funnits eller använts länge.",
                "Jag har en ny telefon.",
            ),
            VocabularyEntry(
                "hjälpa",
                "verb",
                "Göra något så att det blir lättare för en annan person.",
                "Kan du hjälpa mig?",
            ),
            VocabularyEntry(
                "behöva",
                "verb",
                "Inte kunna vara utan något i en viss situation.",
                "Jag behöver en penna.",
            ),
            VocabularyEntry(
                "en toalett",
                "noun",
                "En plats där man kan kissa eller bajsa.",
                "Var finns toaletten?",
            ),
            VocabularyEntry(
                "sjuk",
                "adjective",
                "Som inte mår bra i kroppen eller på annat sätt.",
                "Jag är sjuk idag.",
            ),
            VocabularyEntry(
                "ont", "adverb", "Ett ord i uttryck som beskriver smärta.", "Jag har ont i huvudet."
            ),
            VocabularyEntry(
                "ett huvud",
                "noun",
                "Kroppsdelen där ögon, öron och mun finns.",
                "Mitt huvud gör ont.",
            ),
            VocabularyEntry(
                "en läkare",
                "noun",
                "En person som undersöker och behandlar sjukdomar.",
                "Jag behöver träffa en läkare.",
            ),
            VocabularyEntry(
                "en telefon",
                "noun",
                "En apparat som man kan ringa med.",
                "Min telefon ligger hemma.",
            ),
            VocabularyEntry(
                "ringa", "verb", "Kontakta någon med telefon.", "Jag ringer min syster."
            ),
            VocabularyEntry(
                "en penna", "noun", "Ett redskap som man skriver med.", "Har du en penna?"
            ),
            VocabularyEntry(
                "ett papper",
                "noun",
                "Ett tunt material som man kan skriva på.",
                "Skriv numret på ett papper.",
            ),
        ],
    ),
]
