"""Romanian B2 phrases for precise requests, negotiation and mediation."""

from app.data._types import PhrasebookCategory, PhrasebookEntry

B2_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        "ro-decisions-b2",
        "B2",
        "Reanalizarea unei decizii",
        "🔎",
        [
            PhrasebookEntry(
                "Dacă am fi avut aceste date, am fi ales altă variantă.",
                "Explici rolul informațiilor lipsă într-o decizie trecută.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "E posibil să fi înțeles greșit termenul; aș vrea să verificăm.",
                "Admiți o posibilă eroare de interpretare și ceri verificarea.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Nu mai putem schimba decizia de atunci, dar putem limita consecințele.",
                "Îndrepți discuția despre o greșeală către soluții actuale.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Dacă am fi început mai devreme, acum am avea timp pentru verificări.",
                "Legi un început întârziat de situația prezentă.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Îmi asum partea mea de răspundere pentru această întârziere.",
                "Recunoști propria contribuție la o problemă comună.",
                "neutral",
                "b2-unit-1",
            ),
            PhrasebookEntry(
                "Privind retrospectiv, ar fi fost mai prudent să cerem un deviz detaliat.",
                "Evaluezi o decizie trecută și formulezi o lecție practică.",
                "neutral",
                "b2-unit-1",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-procedures-b2",
        "B2",
        "Responsabilități și stadiul unei lucrări",
        "📋",
        [
            PhrasebookEntry(
                "Cui îi revine verificarea finală și până când trebuie făcută?",
                "Clarifici persoana responsabilă și termenul unei sarcini.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Vă rog să mi le trimiteți numai după ce le semnează titularul.",
                "Precizezi condiția trimiterii unor documente deja identificate.",
                "formal",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Mă refer la instituția ale cărei date apar în contract.",
                "Identifici exact organizația despre care vorbești.",
                "neutral",
                "b2-unit-2",
            ),
            PhrasebookEntry(
                "Cererea a fost înregistrată, dar încă nu a fost aprobată.",
                "Separi două etape pe care interlocutorul le-ar putea confunda.",
                "formal",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Mai avem de verificat devizul înainte de a confirma lucrarea.",
                "Precizezi ce sarcină împiedică momentan acordul final.",
                "neutral",
                "b2-unit-3",
            ),
            PhrasebookEntry(
                "Lucrările au fost reluate, însă data finalizării rămâne de confirmat.",
                "Comunici progresul fără să promiți un termen neverificat.",
                "formal",
                "b2-unit-4",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-negotiation-b2",
        "B2",
        "Negocierea condițiilor",
        "🤝",
        [
            PhrasebookEntry(
                "Putem accepta termenul cu condiția să păstrați prețul convenit.",
                "Accepți o modificare legând-o de o cerință explicită.",
                "formal",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Chiar dacă am mări bugetul, tot ar trebui să reducem volumul lucrării.",
                "Arăți că o concesie financiară nu rezolvă întreaga problemă.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Care dintre aceste condiții sunt negociabile?",
                "Identifici spațiul real de negociere înainte de o contrapropunere.",
                "formal",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Cu cât prelungim discuția, cu atât ne rămâne mai puțin timp pentru execuție.",
                "Explici costul unei negocieri care se prelungește.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Aș putea ceda în privința datei, dar nu și a garanției.",
                "Delimitezi o concesie și o condiție pe care vrei să o păstrezi.",
                "neutral",
                "b2-unit-5",
            ),
            PhrasebookEntry(
                "Să consemnăm în scris această condiție, ca să avem aceeași interpretare.",
                "Ceri fixarea acordului după negociere.",
                "neutral",
                "b2-unit-5",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-evidence-b2",
        "B2",
        "Surse și informații neconfirmate",
        "📰",
        [
            PhrasebookEntry(
                "Potrivit raportului, costurile au crescut; cauza nu este însă precizată.",
                "Rezumi o sursă fără să adaugi o explicație absentă.",
                "formal",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Avem o confirmare independentă sau doar declarația furnizorului?",
                "Verifici pe ce se bazează o afirmație.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Este o explicație plauzibilă, dar datele nu o dovedesc încă.",
                "Recunoști valoarea unei ipoteze fără să o prezinți ca fapt.",
                "neutral",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "O fi uitat să răspundă; mai bine îl sunăm înainte să tragem concluzii.",
                "Sugerezi informal o explicație posibilă și propui verificarea.",
                "informal",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Din informațiile disponibile nu rezultă că toate cererile au fost respinse.",
                "Limitezi o generalizare care depășește dovezile.",
                "formal",
                "b2-unit-6",
            ),
            PhrasebookEntry(
                "Aș prefera să prezentăm cifra drept estimare, nu drept rezultat definitiv.",
                "Ceri un grad de certitudine potrivit datelor.",
                "formal",
                "b2-unit-6",
            ),
        ],
    ),
    PhrasebookCategory(
        "ro-mediation-b2",
        "B2",
        "Dezacord, reformulare și mediere",
        "💬",
        [
            PhrasebookEntry(
                "Obiecția mea nu privește scopul, ci modul de aplicare.",
                "Corectezi impresia că respingi întreaga propunere.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "În principiu suntem de acord; ne despart încă detaliile privind costurile.",
                "Identifici acordul general și problema rămasă.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Dacă reformulez corect, vă preocupă accesul, nu programul în sine.",
                "Verifici interpretarea unei obiecții înainte să răspunzi.",
                "formal",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Să separăm ceea ce am convenit de ceea ce mai trebuie negociat.",
                "Organizezi o discuție în care acordurile și propunerile se amestecă.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Înțeleg gluma, dar aș vrea să revenim la problema concretă.",
                "Răspunzi calm la umor și readuci discuția la subiect.",
                "neutral",
                "b2-unit-7",
            ),
            PhrasebookEntry(
                "Putem nota această rezervă în rezumat, fără să blocăm punctele deja agreate.",
                "Propui consemnarea unui dezacord limitat la finalul consultării.",
                "formal",
                "b2-unit-8",
            ),
        ],
    ),
]
