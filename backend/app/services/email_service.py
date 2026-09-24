"""Email service — wraps fastapi-mail for transactional emails.

Reads configuration from settings. If EMAIL_ENABLED=false, all send_*
functions are no-ops so the app works without SMTP configured.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.app_logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)

_TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "email"


class _SafeHtml(str):
    """Trusted HTML controlled by the application, never by user input."""


def _safe_html(value: str) -> _SafeHtml:
    return _SafeHtml(value)


def _get_mail_config() -> ConnectionConfig:
    return ConnectionConfig(
        MAIL_USERNAME=settings.SMTP_USER,
        MAIL_PASSWORD=settings.SMTP_PASSWORD,
        MAIL_FROM=settings.SMTP_FROM,
        MAIL_PORT=settings.SMTP_PORT,
        MAIL_SERVER=settings.SMTP_HOST,
        MAIL_STARTTLS=settings.SMTP_TLS,
        MAIL_SSL_TLS=settings.SMTP_SSL,
        USE_CREDENTIALS=bool(settings.SMTP_USER),
        VALIDATE_CERTS=True,
    )


_VERIFY_I18N: dict[str, dict[str, str]] = {
    "en": {
        "greeting": "Hi {name},",
        "subject": "Verify your FreeLingo account",
        "body": "Thank you for creating your FreeLingo account.<br />Please verify your email address by clicking the button below. This link is valid for <strong>24 hours</strong>.",
        "button": "Verify my account",
        "link_fallback": "If the button doesn't work, copy and paste this link into your browser:",
        "footer": "If you didn't create this account, you can ignore this email.",
    },
    "es": {
        "greeting": "Hola {name},",
        "subject": "Verifica tu cuenta de FreeLingo",
        "body": "Gracias por crear tu cuenta de FreeLingo.<br />Por favor, verifica tu direcci\u00f3n de correo haciendo clic en el bot\u00f3n. Este enlace es v\u00e1lido durante <strong>24 horas</strong>.",
        "button": "Verificar mi cuenta",
        "link_fallback": "Si el bot\u00f3n no funciona, copia y pega este enlace en tu navegador:",
        "footer": "Si no creaste esta cuenta, puedes ignorar este correo.",
    },
    "fr": {
        "greeting": "Bonjour {name},",
        "subject": "V\u00e9rifiez votre compte FreeLingo",
        "body": "Merci de cr\u00e9er votre compte FreeLingo.<br />Veuillez v\u00e9rifier votre adresse e-mail en cliquant sur le bouton ci-dessous. Ce lien est valable <strong>24 heures</strong>.",
        "button": "V\u00e9rifier mon compte",
        "link_fallback": "Si le bouton ne fonctionne pas, copiez et collez ce lien dans votre navigateur\u00a0:",
        "footer": "Si vous n'avez pas cr\u00e9\u00e9 ce compte, vous pouvez ignorer cet e-mail.",
    },
    "de": {
        "greeting": "Hallo {name},",
        "subject": "Verifiziere deinen FreeLingo-Account",
        "body": "Danke f\u00fcr die Erstellung deines FreeLingo-Accounts.<br />Bitte verifiziere deine E-Mail-Adresse \u00fcber den Button. Dieser Link ist <strong>24 Stunden</strong> g\u00fcltig.",
        "button": "Meinen Account verifizieren",
        "link_fallback": "Falls der Button nicht funktioniert, kopiere diesen Link in deinen Browser:",
        "footer": "Falls du diesen Account nicht erstellt hast, kannst du diese E-Mail ignorieren.",
    },
    "pt": {
        "greeting": "Ol\u00e1 {name},",
        "subject": "Verifique a sua conta FreeLingo",
        "body": "Obrigado por criar a sua conta FreeLingo.<br />Por favor, verifique o seu endere\u00e7o de e-mail clicando no bot\u00e3o. Este link \u00e9 v\u00e1lido por <strong>24 horas</strong>.",
        "button": "Verificar a minha conta",
        "link_fallback": "Se o bot\u00e3o n\u00e3o funcionar, copie e cole este link no seu navegador:",
        "footer": "Se n\u00e3o criou esta conta, pode ignorar este e-mail.",
    },
    "it": {
        "greeting": "Ciao {name},",
        "subject": "Verifica il tuo account FreeLingo",
        "body": "Grazie per aver creato il tuo account FreeLingo.<br />Verifica il tuo indirizzo e-mail cliccando sul pulsante. Questo link \u00e8 valido per <strong>24 ore</strong>.",
        "button": "Verifica il mio account",
        "link_fallback": "Se il pulsante non funziona, copia e incolla questo link nel browser:",
        "footer": "Se non hai creato questo account, puoi ignorare questa e-mail.",
    },
    "nl": {
        "greeting": "Hallo {name},",
        "subject": "Verifieer je FreeLingo-account",
        "body": "Bedankt voor het aanmaken van je FreeLingo-account.<br />Verifieer je e-mailadres door op de knop te klikken. Deze link is <strong>24 uur</strong> geldig.",
        "button": "Mijn account verifi\u00ebren",
        "link_fallback": "Als de knop niet werkt, kopieer en plak dan deze link in je browser:",
        "footer": "Als je dit account niet hebt aangemaakt, kun je deze e-mail negeren.",
    },
    "pl": {
        "greeting": "Cze\u015b\u0107 {name},",
        "subject": "Zweryfikuj swoje konto FreeLingo",
        "body": "Dzi\u0119kujemy za za\u0142o\u017cenie konta FreeLingo.<br />Zweryfikuj sw\u00f3j adres e-mail klikaj\u0105c przycisk poni\u017cej. Ten link jest wa\u017cny przez <strong>24 godziny</strong>.",
        "button": "Zweryfikuj moje konto",
        "link_fallback": "Je\u015bli przycisk nie dzia\u0142a, skopiuj i wklej ten link do przegl\u0105darki:",
        "footer": "Je\u015bli nie zak\u0142ada\u0142e\u015b tego konta, mo\u017cesz zignorowa\u0107 ten e-mail.",
    },
    "ro": {
        "greeting": "Bun\u0103 {name},",
        "subject": "Verific\u0103-\u021bi contul FreeLingo",
        "body": "Mul\u021bumim c\u0103 \u021bi-ai creat contul FreeLingo.<br />Te rug\u0103m s\u0103-\u021bi verifici adresa de e-mail f\u0103c\u00e2nd clic pe buton. Acest link este valabil <strong>24 de ore</strong>.",
        "button": "Verific\u0103-mi contul",
        "link_fallback": "Dac\u0103 butonul nu func\u021bioneaz\u0103, copiaz\u0103 \u0219i lipi\u015fte acest link \u00een browser:",
        "footer": "Dac\u0103 nu ai creat acest cont, po\u021bi ignora acest e-mail.",
    },
    "ru": {
        "greeting": "\u041f\u0440\u0438\u0432\u0435\u0442, {name},",
        "subject": "\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u0435 \u0430\u043a\u043a\u0430\u0443\u043d\u0442 FreeLingo",
        "body": "\u0421\u043f\u0430\u0441\u0438\u0431\u043e \u0437\u0430 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044e \u0432 FreeLingo.<br />\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u0435 \u0430\u0434\u0440\u0435\u0441 \u044d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u043e\u0439 \u043f\u043e\u0447\u0442\u044b, \u043d\u0430\u0436\u0430\u0432 \u043d\u0430 \u043a\u043d\u043e\u043f\u043a\u0443. \u0421\u0441\u044b\u043b\u043a\u0430 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u0430 <strong>24 \u0447\u0430\u0441\u0430</strong>.",
        "button": "\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u044c \u0430\u043a\u043a\u0430\u0443\u043d\u0442",
        "link_fallback": "\u0415\u0441\u043b\u0438 \u043a\u043d\u043e\u043f\u043a\u0430 \u043d\u0435 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442, \u0441\u043a\u043e\u043f\u0438\u0440\u0443\u0439\u0442\u0435 \u0438 \u0432\u0441\u0442\u0430\u0432\u044c\u0442\u0435 \u044d\u0442\u0443 \u0441\u0441\u044b\u043b\u043a\u0443 \u0432 \u0431\u0440\u0430\u0443\u0437\u0435\u0440:",
        "footer": "\u0415\u0441\u043b\u0438 \u0432\u044b \u043d\u0435 \u0441\u043e\u0437\u0434\u0430\u0432\u0430\u043b\u0438 \u044d\u0442\u043e\u0442 \u0430\u043a\u043a\u0430\u0443\u043d\u0442, \u043f\u0440\u043e\u0441\u0442\u043e \u0438\u0433\u043d\u043e\u0440\u0438\u0440\u0443\u0439\u0442\u0435 \u044d\u0442\u043e \u043f\u0438\u0441\u044c\u043c\u043e.",
    },
    "tr": {
        "greeting": "Merhaba {name},",
        "subject": "FreeLingo hesab\u0131n\u0131z\u0131 do\u011frulay\u0131n",
        "body": "FreeLingo hesab\u0131n\u0131z\u0131 olu\u015fturdu\u011funuz i\u00e7in te\u015fekk\u00fcr ederiz.<br />L\u00fctfen a\u015fa\u011f\u0131daki d\u00fc\u011fmeye t\u0131klayarak e-posta adresinizi do\u011frulay\u0131n. Bu ba\u011flant\u0131 <strong>24 saat</strong> ge\u00e7erlidir.",
        "button": "Hesab\u0131m\u0131 do\u011frula",
        "link_fallback": "D\u00fc\u011fme \u00e7al\u0131\u015fmazsa bu ba\u011flant\u0131y\u0131 kopyalay\u0131p taray\u0131c\u0131n\u0131za yap\u0131\u015ft\u0131r\u0131n:",
        "footer": "Bu hesab\u0131 siz olu\u015fturmad\u0131ysan\u0131z bu e-postay\u0131 yok sayabilirsiniz.",
    },
    "sv": {
        "greeting": "Hej {name},",
        "subject": "Bekräfta ditt FreeLingo-konto",
        "body": "Tack för att du skapade ett FreeLingo-konto.<br />Bekräfta din e-postadress genom att klicka på knappen nedan. Länken är giltig i <strong>24 timmar</strong>.",
        "button": "Bekräfta mitt konto",
        "link_fallback": "Om knappen inte fungerar kan du kopiera länken och klistra in den i din webbläsare:",
        "footer": "Om du inte har skapat kontot kan du ignorera det här e-postmeddelandet.",
    },
    "da": {
        "greeting": "Hej {name},",
        "subject": "Bekræft din FreeLingo-konto",
        "body": "Tak, fordi du oprettede en FreeLingo-konto.<br />Bekræft din e-mailadresse ved at klikke på knappen nedenfor. Linket er gyldigt i <strong>24 timer</strong>.",
        "button": "Bekræft min konto",
        "link_fallback": "Hvis knappen ikke virker, kan du kopiere linket og indsætte det i din browser:",
        "footer": "Hvis du ikke har oprettet kontoen, kan du ignorere denne e-mail.",
    },
    "fi": {
        "greeting": "Hei {name},",
        "subject": "Vahvista FreeLingo-tilisi",
        "body": "Kiitos, että loit FreeLingo-tilin.<br />Vahvista sähköpostiosoitteesi napsauttamalla alla olevaa painiketta. Linkki on voimassa <strong>24 tuntia</strong>.",
        "button": "Vahvista tilini",
        "link_fallback": "Jos painike ei toimi, kopioi tämä linkki ja liitä se selaimeesi:",
        "footer": "Jos et luonut tätä tiliä, voit jättää tämän viestin huomiotta.",
    },
}

_RESET_I18N: dict[str, dict[str, str]] = {
    "en": {
        "greeting": "Hi {name},",
        "subject": "Reset your FreeLingo password",
        "body": "We received a request to reset the password for your FreeLingo account.<br />Click the button below to create a new password. This link is valid for <strong>1 hour</strong>.",
        "button": "Reset my password",
        "link_fallback": "If the button doesn't work, copy and paste this link into your browser:",
        "footer": "If you didn't request a password reset, you can safely ignore this email.",
    },
    "es": {
        "greeting": "Hola {name},",
        "subject": "Restablece tu contrase\u00f1a de FreeLingo",
        "body": "Hemos recibido una solicitud para restablecer la contrase\u00f1a de tu cuenta FreeLingo.<br />Haz clic en el bot\u00f3n para crear una nueva. Este enlace es v\u00e1lido durante <strong>1 hora</strong>.",
        "button": "Restablecer contrase\u00f1a",
        "link_fallback": "Si el bot\u00f3n no funciona, copia y pega este enlace en tu navegador:",
        "footer": "Si no solicitaste restablecer tu contrase\u00f1a, puedes ignorar este correo.",
    },
    "fr": {
        "greeting": "Bonjour {name},",
        "subject": "R\u00e9initialisez votre mot de passe FreeLingo",
        "body": "Nous avons re\u00e7u une demande de r\u00e9initialisation du mot de passe de votre compte FreeLingo.<br />Cliquez sur le bouton pour cr\u00e9er un nouveau mot de passe. Ce lien est valable <strong>1 heure</strong>.",
        "button": "R\u00e9initialiser mon mot de passe",
        "link_fallback": "Si le bouton ne fonctionne pas, copiez et collez ce lien dans votre navigateur\u00a0:",
        "footer": "Si vous n'avez pas demand\u00e9 cette r\u00e9initialisation, vous pouvez ignorer cet e-mail.",
    },
    "de": {
        "greeting": "Hallo {name},",
        "subject": "Setze dein FreeLingo-Passwort zur\u00fcck",
        "body": "Wir haben eine Anfrage zum Zur\u00fccksetzen deines FreeLingo-Passworts erhalten.<br />Klicke auf den Button, um ein neues Passwort zu erstellen. Dieser Link ist <strong>1 Stunde</strong> g\u00fcltig.",
        "button": "Passwort zur\u00fccksetzen",
        "link_fallback": "Falls der Button nicht funktioniert, kopiere diesen Link in deinen Browser:",
        "footer": "Falls du keine Zur\u00fccksetzung beantragt hast, kannst du diese E-Mail ignorieren.",
    },
    "pt": {
        "greeting": "Ol\u00e1 {name},",
        "subject": "Redefina a sua senha do FreeLingo",
        "body": "Recebemos um pedido para redefinir a senha da sua conta FreeLingo.<br />Clique no bot\u00e3o para criar uma nova senha. Este link \u00e9 v\u00e1lido por <strong>1 hora</strong>.",
        "button": "Redefinir senha",
        "link_fallback": "Se o bot\u00e3o n\u00e3o funcionar, copie e cole este link no seu navegador:",
        "footer": "Se n\u00e3o solicitou esta redefini\u00e7\u00e3o, pode ignorar este e-mail.",
    },
    "it": {
        "greeting": "Ciao {name},",
        "subject": "Reimposta la tua password FreeLingo",
        "body": "Abbiamo ricevuto una richiesta di reimpostazione della password del tuo account FreeLingo.<br />Clicca sul pulsante per creare una nuova password. Questo link \u00e8 valido per <strong>1 ora</strong>.",
        "button": "Reimposta password",
        "link_fallback": "Se il pulsante non funziona, copia e incolla questo link nel browser:",
        "footer": "Se non hai richiesto la reimpostazione, puoi ignorare questa e-mail.",
    },
    "nl": {
        "greeting": "Hallo {name},",
        "subject": "Stel je FreeLingo-wachtwoord opnieuw in",
        "body": "We hebben een verzoek ontvangen om het wachtwoord van je FreeLingo-account opnieuw in te stellen.<br />Klik op de knop om een nieuw wachtwoord aan te maken. Deze link is <strong>1 uur</strong> geldig.",
        "button": "Wachtwoord opnieuw instellen",
        "link_fallback": "Als de knop niet werkt, kopieer en plak dan deze link in je browser:",
        "footer": "Als je dit niet hebt aangevraagd, kun je deze e-mail negeren.",
    },
    "pl": {
        "greeting": "Cze\u015b\u0107 {name},",
        "subject": "Zresetuj swoje has\u0142o do FreeLingo",
        "body": "Otrzymali\u015bmy pro\u015bb\u0119 o zresetowanie has\u0142a do konta FreeLingo.<br />Kliknij przycisk, aby utworzy\u0107 nowe has\u0142o. Ten link jest wa\u017cny przez <strong>1 godzin\u0119</strong>.",
        "button": "Zresetuj has\u0142o",
        "link_fallback": "Je\u015bli przycisk nie dzia\u0142a, skopiuj i wklej ten link do przegl\u0105darki:",
        "footer": "Je\u015bli nie prosi\u0142e\u015b o reset, mo\u017cesz zignorowa\u0107 ten e-mail.",
    },
    "ro": {
        "greeting": "Bun\u0103 {name},",
        "subject": "Resetez\u0103-\u021bi parola FreeLingo",
        "body": "Am primit o cerere de resetare a parolei contului t\u0103u FreeLingo.<br />F\u0103 clic pe buton pentru a crea o parol\u0103 nou\u0103. Acest link este valabil <strong>1 or\u0103</strong>.",
        "button": "Resetez\u0103 parola",
        "link_fallback": "Dac\u0103 butonul nu func\u021bioneaz\u0103, copiaz\u0103 \u0219i lipi\u015fte acest link \u00een browser:",
        "footer": "Dac\u0103 nu ai solicitat resetarea, po\u021bi ignora acest e-mail.",
    },
    "ru": {
        "greeting": "\u041f\u0440\u0438\u0432\u0435\u0442, {name},",
        "subject": "\u0421\u0431\u0440\u043e\u0441 \u043f\u0430\u0440\u043e\u043b\u044f FreeLingo",
        "body": "\u041c\u044b \u043f\u043e\u043b\u0443\u0447\u0438\u043b\u0438 \u0437\u0430\u043f\u0440\u043e\u0441 \u043d\u0430 \u0441\u0431\u0440\u043e\u0441 \u043f\u0430\u0440\u043e\u043b\u044f \u0432\u0430\u0448\u0435\u0433\u043e \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430 FreeLingo.<br />\u041d\u0430\u0436\u043c\u0438\u0442\u0435 \u043a\u043d\u043e\u043f\u043a\u0443, \u0447\u0442\u043e\u0431\u044b \u0441\u043e\u0437\u0434\u0430\u0442\u044c \u043d\u043e\u0432\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c. \u0421\u0441\u044b\u043b\u043a\u0430 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u0430 <strong>1 \u0447\u0430\u0441</strong>.",
        "button": "\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u043f\u0430\u0440\u043e\u043b\u044c",
        "link_fallback": "\u0415\u0441\u043b\u0438 \u043a\u043d\u043e\u043f\u043a\u0430 \u043d\u0435 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442, \u0441\u043a\u043e\u043f\u0438\u0440\u0443\u0439\u0442\u0435 \u0438 \u0432\u0441\u0442\u0430\u0432\u044c\u0442\u0435 \u044d\u0442\u0443 \u0441\u0441\u044b\u043b\u043a\u0443 \u0432 \u0431\u0440\u0430\u0443\u0437\u0435\u0440:",
        "footer": "\u0415\u0441\u043b\u0438 \u0432\u044b \u043d\u0435 \u0437\u0430\u043f\u0440\u0430\u0448\u0438\u0432\u0430\u043b\u0438 \u0441\u0431\u0440\u043e\u0441, \u043f\u0440\u043e\u0441\u0442\u043e \u0438\u0433\u043d\u043e\u0440\u0438\u0440\u0443\u0439\u0442\u0435 \u044d\u0442\u043e \u043f\u0438\u0441\u044c\u043c\u043e.",
    },
    "tr": {
        "greeting": "Merhaba {name},",
        "subject": "FreeLingo parolan\u0131z\u0131 s\u0131f\u0131rlay\u0131n",
        "body": "FreeLingo hesab\u0131n\u0131z\u0131n parolas\u0131n\u0131 s\u0131f\u0131rlama iste\u011fi ald\u0131k.<br />Yeni bir parola olu\u015fturmak i\u00e7in a\u015fa\u011f\u0131daki d\u00fc\u011fmeye t\u0131klay\u0131n. Bu ba\u011flant\u0131 <strong>1 saat</strong> ge\u00e7erlidir.",
        "button": "Parolam\u0131 s\u0131f\u0131rla",
        "link_fallback": "D\u00fc\u011fme \u00e7al\u0131\u015fmazsa bu ba\u011flant\u0131y\u0131 kopyalay\u0131p taray\u0131c\u0131n\u0131za yap\u0131\u015ft\u0131r\u0131n:",
        "footer": "Parola s\u0131f\u0131rlama iste\u011finde bulunmad\u0131ysan\u0131z bu e-postay\u0131 g\u00fcvenle yok sayabilirsiniz.",
    },
    "sv": {
        "greeting": "Hej {name},",
        "subject": "Återställ ditt FreeLingo-lösenord",
        "body": "Vi har fått en begäran om att återställa lösenordet för ditt FreeLingo-konto.<br />Klicka på knappen nedan för att skapa ett nytt lösenord. Länken är giltig i <strong>1 timme</strong>.",
        "button": "Återställ mitt lösenord",
        "link_fallback": "Om knappen inte fungerar kan du kopiera länken och klistra in den i din webbläsare:",
        "footer": "Om du inte har begärt en lösenordsåterställning kan du ignorera det här e-postmeddelandet.",
    },
    "da": {
        "greeting": "Hej {name},",
        "subject": "Nulstil din FreeLingo-adgangskode",
        "body": "Vi har modtaget en anmodning om at nulstille adgangskoden til din FreeLingo-konto.<br />Klik på knappen nedenfor for at oprette en ny adgangskode. Linket er gyldigt i <strong>1 time</strong>.",
        "button": "Nulstil min adgangskode",
        "link_fallback": "Hvis knappen ikke virker, kan du kopiere linket og indsætte det i din browser:",
        "footer": "Hvis du ikke har bedt om at få nulstillet adgangskoden, kan du ignorere denne e-mail.",
    },
    "fi": {
        "greeting": "Hei {name},",
        "subject": "Palauta FreeLingo-salasanasi",
        "body": "Saimme pyynnön palauttaa FreeLingo-tilisi salasana.<br />Luo uusi salasana napsauttamalla alla olevaa painiketta. Linkki on voimassa <strong>1 tunnin</strong>.",
        "button": "Palauta salasanani",
        "link_fallback": "Jos painike ei toimi, kopioi tämä linkki ja liitä se selaimeesi:",
        "footer": "Jos et pyytänyt salasanan palautusta, voit jättää tämän viestin huomiotta.",
    },
}

_WELCOME_I18N: dict[str, dict[str, str]] = {
    "en": {
        "subject": "Welcome to FreeLingo!",
        "greeting": "Hi {name},",
        "body": "Your account is ready. Here is how to get started:",
        "step1": "Take the <strong>Assessment</strong> — it detects your current level (A1–C2) and your strengths and weak points.",
        "step2": "Generate your <strong>Study Plan</strong> — a week-by-week schedule tailored to your level and goals.",
        "step3": "Complete your first daily lesson and start building your streak.",
        "button": "Go to my dashboard",
        "footer": "Happy learning!",
    },
    "es": {
        "subject": "\u00a1Bienvenido a FreeLingo!",
        "greeting": "Hola {name},",
        "body": "Tu cuenta est\u00e1 lista. As\u00ed puedes empezar:",
        "step1": "Haz la <strong>Evaluaci\u00f3n</strong> \u2014 detecta tu nivel actual (A1\u2013C2) y tus puntos fuertes y d\u00e9biles.",
        "step2": "Genera tu <strong>Plan de estudio</strong> \u2014 un calendario semanal adaptado a tu nivel y objetivos.",
        "step3": "Completa tu primera lecci\u00f3n diaria y empieza a construir tu racha.",
        "button": "Ir a mi panel",
        "footer": "\u00a1Buena suerte con el aprendizaje!",
    },
    "fr": {
        "subject": "Bienvenue sur FreeLingo\u00a0!",
        "greeting": "Bonjour {name},",
        "body": "Votre compte est pr\u00eat. Voici comment commencer\u00a0:",
        "step1": "Passez l\u2019<strong>\u00e9valuation</strong> \u2014 elle d\u00e9tecte votre niveau actuel (A1\u2013C2) et vos points forts et faibles.",
        "step2": "G\u00e9n\u00e9rez votre <strong>plan d\u2019\u00e9tude</strong> \u2014 un planning semaine par semaine adapt\u00e9 \u00e0 votre niveau et vos objectifs.",
        "step3": "Terminez votre premi\u00e8re le\u00e7on quotidienne et commencez \u00e0 construire votre s\u00e9rie.",
        "button": "Aller \u00e0 mon tableau de bord",
        "footer": "Bon apprentissage\u00a0!",
    },
    "de": {
        "subject": "Willkommen bei FreeLingo!",
        "greeting": "Hallo {name},",
        "body": "Dein Konto ist bereit. So geht es los:",
        "step1": "Mache das <strong>Assessment</strong> \u2014 es erkennt dein aktuelles Niveau (A1\u2013C2) sowie deine St\u00e4rken und Schw\u00e4chen.",
        "step2": "Erstelle deinen <strong>Lernplan</strong> \u2014 einen wochenweisen Zeitplan, der auf dein Niveau und deine Ziele abgestimmt ist.",
        "step3": "Schlie\u00dfe deine erste t\u00e4gliche Lektion ab und baue deine Serie auf.",
        "button": "Zu meinem Dashboard",
        "footer": "Viel Spa\u00df beim Lernen!",
    },
    "pt": {
        "subject": "Bem-vindo ao FreeLingo!",
        "greeting": "Ol\u00e1 {name},",
        "body": "A sua conta est\u00e1 pronta. Veja como come\u00e7ar:",
        "step1": "Fa\u00e7a a <strong>Avalia\u00e7\u00e3o</strong> \u2014 ela deteta o seu n\u00edvel atual (A1\u2013C2) e os seus pontos fortes e fracos.",
        "step2": "Gere o seu <strong>Plano de estudo</strong> \u2014 um calend\u00e1rio semanal adaptado ao seu n\u00edvel e objetivos.",
        "step3": "Complete a sua primeira li\u00e7\u00e3o di\u00e1ria e comece a construir a sua sequ\u00eancia.",
        "button": "Ir para o meu painel",
        "footer": "Bons estudos!",
    },
    "it": {
        "subject": "Benvenuto su FreeLingo!",
        "greeting": "Ciao {name},",
        "body": "Il tuo account \u00e8 pronto. Ecco come iniziare:",
        "step1": "Fai la <strong>Valutazione</strong> \u2014 rileva il tuo livello attuale (A1\u2013C2) e i tuoi punti di forza e debolezza.",
        "step2": "Genera il tuo <strong>Piano di studio</strong> \u2014 un programma settimanale adattato al tuo livello e ai tuoi obiettivi.",
        "step3": "Completa la tua prima lezione quotidiana e inizia a costruire la tua serie.",
        "button": "Vai alla mia dashboard",
        "footer": "Buono studio!",
    },
    "nl": {
        "subject": "Welkom bij FreeLingo!",
        "greeting": "Hallo {name},",
        "body": "Je account is klaar. Zo ga je aan de slag:",
        "step1": "Doe de <strong>Assessment</strong> \u2014 het detecteert je huidige niveau (A1\u2013C2) en je sterke en zwakke punten.",
        "step2": "Genereer je <strong>Studieplan</strong> \u2014 een week-voor-week schema afgestemd op je niveau en doelen.",
        "step3": "Voltooi je eerste dagelijkse les en begin met het opbouwen van je reeks.",
        "button": "Naar mijn dashboard",
        "footer": "Veel leerplezier!",
    },
    "pl": {
        "subject": "Witamy w FreeLingo!",
        "greeting": "Cze\u015b\u0107 {name},",
        "body": "Twoje konto jest gotowe. Oto jak zacz\u0105\u0107:",
        "step1": "Wykonaj <strong>Assessment</strong> \u2014 wykryje Tw\u00f3j obecny poziom (A1\u2013C2) oraz mocne i s\u0142abe strony.",
        "step2": "Wygeneruj sw\u00f3j <strong>Plan nauki</strong> \u2014 tygodniowy harmonogram dostosowany do Twojego poziomu i cel\u00f3w.",
        "step3": "Uko\u0144cz pierwsz\u0105 codzienn\u0105 lekcj\u0119 i zacznij budowa\u0107 swoj\u0105 seri\u0119.",
        "button": "Przejd\u017a do mojego panelu",
        "footer": "Mi\u0142ej nauki!",
    },
    "ro": {
        "subject": "Bun venit la FreeLingo!",
        "greeting": "Bun\u0103 {name},",
        "body": "Contul t\u0103u este gata. Iat\u0103 cum po\u021bi \u00eencepe:",
        "step1": "F\u0103 <strong>Evaluarea</strong> \u2014 detecteaz\u0103 nivelul t\u0103u actual (A1\u2013C2) \u0219i punctele forte \u0219i slabe.",
        "step2": "Genereaz\u0103 <strong>Planul de studiu</strong> \u2014 un program s\u0103pt\u0103m\u00e2nal adaptat nivelului \u0219i obiectivelor tale.",
        "step3": "Finalizeaz\u0103 prima lec\u021bie zilnic\u0103 \u0219i \u00eencepe s\u0103 \u00ee\u021bi construie\u0219ti seria.",
        "button": "Mergi la tabloul meu de bord",
        "footer": "Mult succes la \u00eenv\u0103\u021bat!",
    },
    "ru": {
        "subject": "\u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c \u0432 FreeLingo!",
        "greeting": "\u041f\u0440\u0438\u0432\u0435\u0442, {name},",
        "body": "\u0412\u0430\u0448 \u0430\u043a\u043a\u0430\u0443\u043d\u0442 \u0433\u043e\u0442\u043e\u0432. \u0412\u043e\u0442 \u043a\u0430\u043a \u043d\u0430\u0447\u0430\u0442\u044c:",
        "step1": "\u041f\u0440\u043e\u0439\u0434\u0438\u0442\u0435 <strong>\u0422\u0435\u0441\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435</strong> \u2014 \u043e\u043d\u043e \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0438\u0442 \u0432\u0430\u0448 \u0442\u0435\u043a\u0443\u0449\u0438\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c (A1\u2013C2), \u0441\u0438\u043b\u044c\u043d\u044b\u0435 \u0438 \u0441\u043b\u0430\u0431\u044b\u0435 \u0441\u0442\u043e\u0440\u043e\u043d\u044b.",
        "step2": "\u0421\u043e\u0437\u0434\u0430\u0439\u0442\u0435 <strong>\u041f\u043b\u0430\u043d \u043e\u0431\u0443\u0447\u0435\u043d\u0438\u044f</strong> \u2014 \u043f\u043e\u043d\u0435\u0434\u0435\u043b\u044c\u043d\u043e\u0435 \u0440\u0430\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u0435, \u0430\u0434\u0430\u043f\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u043e\u0435 \u043f\u043e\u0434 \u0432\u0430\u0448 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0438 \u0446\u0435\u043b\u0438.",
        "step3": "\u0417\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u0435 \u043f\u0435\u0440\u0432\u044b\u0439 \u0435\u0436\u0435\u0434\u043d\u0435\u0432\u043d\u044b\u0439 \u0443\u0440\u043e\u043a \u0438 \u043d\u0430\u0447\u043d\u0438\u0442\u0435 \u043d\u0430\u043a\u0430\u043f\u043b\u0438\u0432\u0430\u0442\u044c \u0441\u0435\u0440\u0438\u044e.",
        "button": "\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u043d\u0430 \u043f\u0430\u043d\u0435\u043b\u044c \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u044f",
        "footer": "\u0423\u0441\u043f\u0435\u0445\u043e\u0432 \u0432 \u043e\u0431\u0443\u0447\u0435\u043d\u0438\u0438!",
    },
    "tr": {
        "subject": "FreeLingo'ya ho\u015f geldiniz!",
        "greeting": "Merhaba {name},",
        "body": "Hesab\u0131n\u0131z haz\u0131r. Ba\u015flamak i\u00e7in \u015funlar\u0131 yapabilirsiniz:",
        "step1": "<strong>Seviye Tespitine</strong> girin \u2014 mevcut seviyenizi (A1\u2013C2), g\u00fc\u00e7l\u00fc ve zay\u0131f y\u00f6nlerinizi belirler.",
        "step2": "<strong>\u00c7al\u0131\u015fma Plan\u0131n\u0131z\u0131</strong> olu\u015fturun \u2014 seviyenize ve hedeflerinize g\u00f6re haz\u0131rlanm\u0131\u015f haftal\u0131k bir program.",
        "step3": "\u0130lk g\u00fcnl\u00fck dersinizi tamamlay\u0131n ve serinizi olu\u015fturmaya ba\u015flay\u0131n.",
        "button": "Panoma git",
        "footer": "\u0130yi \u00e7al\u0131\u015fmalar!",
    },
    "sv": {
        "subject": "Välkommen till FreeLingo!",
        "greeting": "Hej {name},",
        "body": "Ditt konto är redo. Så här kommer du igång:",
        "step1": "Gör <strong>nivåbedömningen</strong> – den visar din nuvarande nivå (A1–C2) samt dina styrkor och svagheter.",
        "step2": "Skapa din <strong>studieplan</strong> – en plan vecka för vecka anpassad till din nivå och dina mål.",
        "step3": "Slutför din första dagliga lektion och börja bygga din svit.",
        "button": "Gå till min översikt",
        "footer": "Lycka till med studierna!",
    },
    "da": {
        "subject": "Velkommen til FreeLingo!",
        "greeting": "Hej {name},",
        "body": "Din konto er klar. Sådan kommer du i gang:",
        "step1": "Tag <strong>niveauvurderingen</strong> – den viser dit aktuelle niveau (A1–C2) samt dine styrker og svagheder.",
        "step2": "Opret din <strong>læringsplan</strong> – en ugeplan tilpasset dit niveau og dine mål.",
        "step3": "Gennemfør din første daglige lektion, og begynd at opbygge din stime.",
        "button": "Gå til min oversigt",
        "footer": "God fornøjelse med læringen!",
    },
    "fi": {
        "subject": "Tervetuloa FreeLingoon!",
        "greeting": "Hei {name},",
        "body": "Tilisi on valmis. Näin pääset alkuun:",
        "step1": "Tee <strong>tasoarvio</strong> – se selvittää nykyisen tasosi (A1–C2) sekä vahvuutesi ja kehittämiskohteesi.",
        "step2": "Luo <strong>opintosuunnitelmasi</strong> – tasosi ja tavoitteidesi mukainen viikkosuunnitelma.",
        "step3": "Suorita ensimmäinen päivittäinen oppituntisi ja aloita putkesi.",
        "button": "Siirry koontinäyttöön",
        "footer": "Iloisia opiskeluhetkiä!",
    },
}


_DELETION_I18N: dict[str, dict[str, str]] = {
    "en": {
        "subject": "Your FreeLingo account has been deleted",
        "greeting": "Hi {name},",
        "body": "Your FreeLingo account has been successfully deleted. All your data has been permanently removed from our servers.",
        "footer": "If you did not request this deletion, please contact us immediately.",
    },
    "es": {
        "subject": "Tu cuenta de FreeLingo ha sido eliminada",
        "greeting": "Hola {name},",
        "body": "Tu cuenta de FreeLingo ha sido eliminada correctamente. Todos tus datos han sido borrados permanentemente de nuestros servidores.",
        "footer": "Si no solicitaste esta eliminaci\u00f3n, cont\u00e1ctanos de inmediato.",
    },
    "fr": {
        "subject": "Votre compte FreeLingo a \u00e9t\u00e9 supprim\u00e9",
        "greeting": "Bonjour {name},",
        "body": "Votre compte FreeLingo a \u00e9t\u00e9 supprim\u00e9 avec succ\u00e8s. Toutes vos donn\u00e9es ont \u00e9t\u00e9 d\u00e9finitivement effac\u00e9es de nos serveurs.",
        "footer": "Si vous n\u2019avez pas demand\u00e9 cette suppression, contactez-nous imm\u00e9diatement.",
    },
    "de": {
        "subject": "Dein FreeLingo-Konto wurde gel\u00f6scht",
        "greeting": "Hallo {name},",
        "body": "Dein FreeLingo-Konto wurde erfolgreich gel\u00f6scht. Alle deine Daten wurden dauerhaft von unseren Servern entfernt.",
        "footer": "Falls du diese L\u00f6schung nicht beantragt hast, kontaktiere uns bitte sofort.",
    },
    "pt": {
        "subject": "A sua conta FreeLingo foi eliminada",
        "greeting": "Ol\u00e1 {name},",
        "body": "A sua conta FreeLingo foi eliminada com sucesso. Todos os seus dados foram removidos permanentemente dos nossos servidores.",
        "footer": "Se n\u00e3o solicitou esta elimina\u00e7\u00e3o, contacte-nos imediatamente.",
    },
    "it": {
        "subject": "Il tuo account FreeLingo \u00e8 stato eliminato",
        "greeting": "Ciao {name},",
        "body": "Il tuo account FreeLingo \u00e8 stato eliminato con successo. Tutti i tuoi dati sono stati rimossi definitivamente dai nostri server.",
        "footer": "Se non hai richiesto questa eliminazione, contattaci immediatamente.",
    },
    "nl": {
        "subject": "Je FreeLingo-account is verwijderd",
        "greeting": "Hallo {name},",
        "body": "Je FreeLingo-account is succesvol verwijderd. Al je gegevens zijn permanent van onze servers verwijderd.",
        "footer": "Als je deze verwijdering niet hebt aangevraagd, neem dan onmiddellijk contact met ons op.",
    },
    "pl": {
        "subject": "Twoje konto FreeLingo zosta\u0142o usuni\u0119te",
        "greeting": "Cze\u015b\u0107 {name},",
        "body": "Twoje konto FreeLingo zosta\u0142o pomy\u015blnie usuni\u0119te. Wszystkie Twoje dane zosta\u0142y trwale usuni\u0119te z naszych serwerk\u00f3w.",
        "footer": "Je\u015bli nie prosi\u0142e\u015b o usuni\u0119cie konta, skontaktuj si\u0119 z nami natychmiast.",
    },
    "ro": {
        "subject": "Contul t\u0103u FreeLingo a fost \u0219ters",
        "greeting": "Bun\u0103 {name},",
        "body": "Contul t\u0103u FreeLingo a fost \u0219ters cu succes. Toate datele tale au fost eliminate definitiv de pe serverele noastre.",
        "footer": "Dac\u0103 nu ai solicitat aceast\u0103 \u015ftergere, contacteaz\u0103-ne imediat.",
    },
    "ru": {
        "subject": "\u0412\u0430\u0448 \u0430\u043a\u043a\u0430\u0443\u043d\u0442 FreeLingo \u0443\u0434\u0430\u043b\u0451\u043d",
        "greeting": "\u041f\u0440\u0438\u0432\u0435\u0442, {name},",
        "body": "\u0412\u0430\u0448 \u0430\u043a\u043a\u0430\u0443\u043d\u0442 FreeLingo \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u0443\u0434\u0430\u043b\u0451\u043d. \u0412\u0441\u0435 \u0432\u0430\u0448\u0438 \u0434\u0430\u043d\u043d\u044b\u0435 \u0431\u044b\u043b\u0438 \u043d\u0430\u0432\u0441\u0435\u0433\u0434\u0430 \u0443\u0434\u0430\u043b\u0435\u043d\u044b \u0441 \u043d\u0430\u0448\u0438\u0445 \u0441\u0435\u0440\u0432\u0435\u0440\u043e\u0432.",
        "footer": "\u0415\u0441\u043b\u0438 \u0432\u044b \u043d\u0435 \u0437\u0430\u043f\u0440\u0430\u0448\u0438\u0432\u0430\u043b\u0438 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u0435, \u043d\u0435\u043c\u0435\u0434\u043b\u0435\u043d\u043d\u043e \u0441\u0432\u044f\u0436\u0438\u0442\u0435\u0441\u044c \u0441 \u043d\u0430\u043c\u0438.",
    },
    "tr": {
        "subject": "FreeLingo hesab\u0131n\u0131z silindi",
        "greeting": "Merhaba {name},",
        "body": "FreeLingo hesab\u0131n\u0131z ba\u015far\u0131yla silindi. T\u00fcm verileriniz sunucular\u0131m\u0131zdan kal\u0131c\u0131 olarak kald\u0131r\u0131ld\u0131.",
        "footer": "Bu silme i\u015flemini siz istemediyseniz l\u00fctfen hemen bizimle ileti\u015fime ge\u00e7in.",
    },
    "sv": {
        "subject": "Ditt FreeLingo-konto har raderats",
        "greeting": "Hej {name},",
        "body": "Ditt FreeLingo-konto har raderats. Alla dina uppgifter har tagits bort permanent från våra servrar.",
        "footer": "Om du inte har begärt att kontot ska raderas ska du kontakta oss omedelbart.",
    },
    "da": {
        "subject": "Din FreeLingo-konto er blevet slettet",
        "greeting": "Hej {name},",
        "body": "Din FreeLingo-konto er blevet slettet. Alle dine oplysninger er fjernet permanent fra vores servere.",
        "footer": "Hvis du ikke har bedt om sletningen, skal du kontakte os med det samme.",
    },
    "fi": {
        "subject": "FreeLingo-tilisi on poistettu",
        "greeting": "Hei {name},",
        "body": "FreeLingo-tilisi on poistettu. Kaikki tietosi on poistettu pysyvästi palvelimiltamme.",
        "footer": "Jos et pyytänyt tilin poistamista, ota meihin välittömästi yhteyttä.",
    },
}

_CONTACT_I18N: dict[str, dict[str, str]] = {
    "en": {
        "email_title": "Contact form message",
        "subject_prefix": "[FreeLingo Contact]",
        "logo": "FreeLingo: Contact Form",
        "from_label": "From",
        "subject_label": "Subject",
        "message_label": "Message",
        "footer": "Sent via FreeLingo contact form",
    },
    "es": {
        "email_title": "Mensaje del formulario de contacto",
        "subject_prefix": "[Contacto FreeLingo]",
        "logo": "FreeLingo: Formulario de contacto",
        "from_label": "De",
        "subject_label": "Asunto",
        "message_label": "Mensaje",
        "footer": "Enviado desde el formulario de contacto de FreeLingo",
    },
    "fr": {
        "email_title": "Message du formulaire de contact",
        "subject_prefix": "[Contact FreeLingo]",
        "logo": "FreeLingo : Formulaire de contact",
        "from_label": "De",
        "subject_label": "Sujet",
        "message_label": "Message",
        "footer": "Envoyé via le formulaire de contact FreeLingo",
    },
    "de": {
        "email_title": "Nachricht aus dem Kontaktformular",
        "subject_prefix": "[FreeLingo Kontakt]",
        "logo": "FreeLingo: Kontaktformular",
        "from_label": "Von",
        "subject_label": "Betreff",
        "message_label": "Nachricht",
        "footer": "Gesendet über das FreeLingo-Kontaktformular",
    },
    "pt": {
        "email_title": "Mensagem do formulário de contacto",
        "subject_prefix": "[Contacto FreeLingo]",
        "logo": "FreeLingo: Formulário de contacto",
        "from_label": "De",
        "subject_label": "Assunto",
        "message_label": "Mensagem",
        "footer": "Enviado pelo formulário de contacto do FreeLingo",
    },
    "it": {
        "email_title": "Messaggio dal modulo di contatto",
        "subject_prefix": "[Contatto FreeLingo]",
        "logo": "FreeLingo: Modulo di contatto",
        "from_label": "Da",
        "subject_label": "Oggetto",
        "message_label": "Messaggio",
        "footer": "Inviato tramite il modulo di contatto FreeLingo",
    },
    "nl": {
        "email_title": "Bericht van het contactformulier",
        "subject_prefix": "[FreeLingo Contact]",
        "logo": "FreeLingo: Contactformulier",
        "from_label": "Van",
        "subject_label": "Onderwerp",
        "message_label": "Bericht",
        "footer": "Verzonden via het FreeLingo-contactformulier",
    },
    "pl": {
        "email_title": "Wiadomość z formularza kontaktowego",
        "subject_prefix": "[Kontakt FreeLingo]",
        "logo": "FreeLingo: Formularz kontaktowy",
        "from_label": "Od",
        "subject_label": "Temat",
        "message_label": "Wiadomość",
        "footer": "Wysłano przez formularz kontaktowy FreeLingo",
    },
    "ro": {
        "email_title": "Mesaj din formularul de contact",
        "subject_prefix": "[Contact FreeLingo]",
        "logo": "FreeLingo: Formular de contact",
        "from_label": "De la",
        "subject_label": "Subiect",
        "message_label": "Mesaj",
        "footer": "Trimis prin formularul de contact FreeLingo",
    },
    "ru": {
        "email_title": "Сообщение из контактной формы",
        "subject_prefix": "[Контакт FreeLingo]",
        "logo": "FreeLingo: Контактная форма",
        "from_label": "От",
        "subject_label": "Тема",
        "message_label": "Сообщение",
        "footer": "Отправлено через контактную форму FreeLingo",
    },
    "tr": {
        "email_title": "İletişim formu mesajı",
        "subject_prefix": "[FreeLingo İletişim]",
        "logo": "FreeLingo: İletişim Formu",
        "from_label": "Gönderen",
        "subject_label": "Konu",
        "message_label": "Mesaj",
        "footer": "FreeLingo iletişim formu aracılığıyla gönderildi",
    },
    "sv": {
        "email_title": "Meddelande från kontaktformuläret",
        "subject_prefix": "[FreeLingo Kontakt]",
        "logo": "FreeLingo: Kontaktformulär",
        "from_label": "Från",
        "subject_label": "Ämne",
        "message_label": "Meddelande",
        "footer": "Skickat via FreeLingos kontaktformulär",
    },
    "da": {
        "email_title": "Besked fra kontaktformularen",
        "subject_prefix": "[FreeLingo Kontakt]",
        "logo": "FreeLingo: Kontaktformular",
        "from_label": "Fra",
        "subject_label": "Emne",
        "message_label": "Besked",
        "footer": "Sendt via FreeLingos kontaktformular",
    },
    "fi": {
        "email_title": "Yhteydenottolomakkeen viesti",
        "subject_prefix": "[FreeLingo Yhteydenotto]",
        "logo": "FreeLingo: Yhteydenottolomake",
        "from_label": "Lähettäjä",
        "subject_label": "Aihe",
        "message_label": "Viesti",
        "footer": "Lähetetty FreeLingon yhteydenottolomakkeella",
    },
}

_FEEDBACK_I18N: dict[str, dict[str, str]] = {
    "en": {
        "email_title": "New feedback submitted",
        "logo": "FreeLingo: New Feedback",
        "feature_label": "Feature request",
        "bug_label": "Bug report",
        "feature_subject_prefix": "[Feature Request]",
        "bug_subject_prefix": "[Bug Report]",
        "author_label": "Submitted by",
        "title_label": "Title",
        "description_label": "Description",
        "cta": "View in admin panel",
        "footer": "FreeLingo feedback board",
    },
    "es": {
        "email_title": "Nuevo feedback recibido",
        "logo": "FreeLingo: Nuevo feedback",
        "feature_label": "Solicitud de funcionalidad",
        "bug_label": "Reporte de error",
        "feature_subject_prefix": "[Solicitud de funcionalidad]",
        "bug_subject_prefix": "[Reporte de error]",
        "author_label": "Enviado por",
        "title_label": "Título",
        "description_label": "Descripción",
        "cta": "Ver en el panel de admin",
        "footer": "Panel de feedback de FreeLingo",
    },
    "fr": {
        "email_title": "Nouveau retour reçu",
        "logo": "FreeLingo : Nouveau retour",
        "feature_label": "Demande de fonctionnalité",
        "bug_label": "Rapport de bug",
        "feature_subject_prefix": "[Demande de fonctionnalité]",
        "bug_subject_prefix": "[Rapport de bug]",
        "author_label": "Envoyé par",
        "title_label": "Titre",
        "description_label": "Description",
        "cta": "Voir dans le panneau admin",
        "footer": "Tableau de feedback FreeLingo",
    },
    "de": {
        "email_title": "Neues Feedback eingereicht",
        "logo": "FreeLingo: Neues Feedback",
        "feature_label": "Funktionswunsch",
        "bug_label": "Fehlerbericht",
        "feature_subject_prefix": "[Funktionswunsch]",
        "bug_subject_prefix": "[Fehlerbericht]",
        "author_label": "Eingereicht von",
        "title_label": "Titel",
        "description_label": "Beschreibung",
        "cta": "Im Adminbereich ansehen",
        "footer": "FreeLingo-Feedbackboard",
    },
    "pt": {
        "email_title": "Novo feedback recebido",
        "logo": "FreeLingo: Novo feedback",
        "feature_label": "Pedido de funcionalidade",
        "bug_label": "Relatório de erro",
        "feature_subject_prefix": "[Pedido de funcionalidade]",
        "bug_subject_prefix": "[Relatório de erro]",
        "author_label": "Enviado por",
        "title_label": "Título",
        "description_label": "Descrição",
        "cta": "Ver no painel de admin",
        "footer": "Quadro de feedback FreeLingo",
    },
    "it": {
        "email_title": "Nuovo feedback ricevuto",
        "logo": "FreeLingo: Nuovo feedback",
        "feature_label": "Richiesta di funzionalità",
        "bug_label": "Segnalazione bug",
        "feature_subject_prefix": "[Richiesta di funzionalità]",
        "bug_subject_prefix": "[Segnalazione bug]",
        "author_label": "Inviato da",
        "title_label": "Titolo",
        "description_label": "Descrizione",
        "cta": "Vedi nel pannello admin",
        "footer": "Bacheca feedback FreeLingo",
    },
    "nl": {
        "email_title": "Nieuwe feedback ingediend",
        "logo": "FreeLingo: Nieuwe feedback",
        "feature_label": "Functieverzoek",
        "bug_label": "Bugrapport",
        "feature_subject_prefix": "[Functieverzoek]",
        "bug_subject_prefix": "[Bugrapport]",
        "author_label": "Ingediend door",
        "title_label": "Titel",
        "description_label": "Beschrijving",
        "cta": "Bekijk in adminpaneel",
        "footer": "FreeLingo-feedbackbord",
    },
    "pl": {
        "email_title": "Dodano nową opinię",
        "logo": "FreeLingo: Nowa opinia",
        "feature_label": "Prośba o funkcję",
        "bug_label": "Zgłoszenie błędu",
        "feature_subject_prefix": "[Prośba o funkcję]",
        "bug_subject_prefix": "[Zgłoszenie błędu]",
        "author_label": "Przesłane przez",
        "title_label": "Tytuł",
        "description_label": "Opis",
        "cta": "Zobacz w panelu admina",
        "footer": "Tablica opinii FreeLingo",
    },
    "ro": {
        "email_title": "Feedback nou trimis",
        "logo": "FreeLingo: Feedback nou",
        "feature_label": "Solicitare funcționalitate",
        "bug_label": "Raport de eroare",
        "feature_subject_prefix": "[Solicitare funcționalitate]",
        "bug_subject_prefix": "[Raport de eroare]",
        "author_label": "Trimis de",
        "title_label": "Titlu",
        "description_label": "Descriere",
        "cta": "Vezi în panoul admin",
        "footer": "Panoul de feedback FreeLingo",
    },
    "ru": {
        "email_title": "Новый отзыв отправлен",
        "logo": "FreeLingo: Новый отзыв",
        "feature_label": "Запрос функции",
        "bug_label": "Отчет об ошибке",
        "feature_subject_prefix": "[Запрос функции]",
        "bug_subject_prefix": "[Отчет об ошибке]",
        "author_label": "Отправил",
        "title_label": "Заголовок",
        "description_label": "Описание",
        "cta": "Открыть в панели администратора",
        "footer": "Доска отзывов FreeLingo",
    },
    "tr": {
        "email_title": "Yeni geri bildirim gönderildi",
        "logo": "FreeLingo: Yeni Geri Bildirim",
        "feature_label": "Özellik isteği",
        "bug_label": "Hata bildirimi",
        "feature_subject_prefix": "[Özellik İsteği]",
        "bug_subject_prefix": "[Hata Bildirimi]",
        "author_label": "Gönderen",
        "title_label": "Başlık",
        "description_label": "Açıklama",
        "cta": "Yönetim panelinde görüntüle",
        "footer": "FreeLingo geri bildirim panosu",
    },
    "sv": {
        "email_title": "Ny feedback har skickats in",
        "logo": "FreeLingo: Ny feedback",
        "feature_label": "Funktionsförslag",
        "bug_label": "Felrapport",
        "feature_subject_prefix": "[Funktionsförslag]",
        "bug_subject_prefix": "[Felrapport]",
        "author_label": "Skickat av",
        "title_label": "Titel",
        "description_label": "Beskrivning",
        "cta": "Visa i administrationspanelen",
        "footer": "FreeLingos feedbacktavla",
    },
    "da": {
        "email_title": "Ny feedback er indsendt",
        "logo": "FreeLingo: Ny feedback",
        "feature_label": "Funktionsforslag",
        "bug_label": "Fejlrapport",
        "feature_subject_prefix": "[Funktionsforslag]",
        "bug_subject_prefix": "[Fejlrapport]",
        "author_label": "Indsendt af",
        "title_label": "Titel",
        "description_label": "Beskrivelse",
        "cta": "Se i administrationspanelet",
        "footer": "FreeLingos feedbacktavle",
    },
    "fi": {
        "email_title": "Uusi palaute lähetetty",
        "logo": "FreeLingo: Uusi palaute",
        "feature_label": "Ominaisuusehdotus",
        "bug_label": "Virheraportti",
        "feature_subject_prefix": "[Ominaisuusehdotus]",
        "bug_subject_prefix": "[Virheraportti]",
        "author_label": "Lähettäjä",
        "title_label": "Otsikko",
        "description_label": "Kuvaus",
        "cta": "Näytä ylläpidossa",
        "footer": "FreeLingon palautetaulu",
    },
}

_REVIEW_I18N: dict[str, dict[str, str]] = {
    "en": {
        "email_title": "New review submitted",
        "subject_prefix": "[New Review]",
        "logo": "FreeLingo: New Review",
        "author_label": "Submitted by",
        "rating_label": "Rating",
        "language_label": "Learning language",
        "comment_label": "Comment",
        "empty_comment": "No comment provided.",
        "cta": "View in admin panel",
        "footer": "FreeLingo review moderation",
    },
    "es": {
        "email_title": "Nueva reseña recibida",
        "subject_prefix": "[Nueva reseña]",
        "logo": "FreeLingo: Nueva reseña",
        "author_label": "Enviada por",
        "rating_label": "Valoración",
        "language_label": "Idioma de aprendizaje",
        "comment_label": "Comentario",
        "empty_comment": "No se incluyó ningún comentario.",
        "cta": "Ver en el panel de admin",
        "footer": "Moderación de reseñas de FreeLingo",
    },
    "fr": {
        "email_title": "Nouvel avis reçu",
        "subject_prefix": "[Nouvel avis]",
        "logo": "FreeLingo : Nouvel avis",
        "author_label": "Envoyé par",
        "rating_label": "Note",
        "language_label": "Langue d'apprentissage",
        "comment_label": "Commentaire",
        "empty_comment": "Aucun commentaire fourni.",
        "cta": "Voir dans le panneau admin",
        "footer": "Modération des avis FreeLingo",
    },
    "de": {
        "email_title": "Neue Bewertung eingereicht",
        "subject_prefix": "[Neue Bewertung]",
        "logo": "FreeLingo: Neue Bewertung",
        "author_label": "Eingereicht von",
        "rating_label": "Bewertung",
        "language_label": "Lernsprache",
        "comment_label": "Kommentar",
        "empty_comment": "Kein Kommentar angegeben.",
        "cta": "Im Adminbereich ansehen",
        "footer": "FreeLingo-Bewertungsmoderation",
    },
    "pt": {
        "email_title": "Nova avaliação recebida",
        "subject_prefix": "[Nova avaliação]",
        "logo": "FreeLingo: Nova avaliação",
        "author_label": "Enviada por",
        "rating_label": "Avaliação",
        "language_label": "Idioma de aprendizagem",
        "comment_label": "Comentário",
        "empty_comment": "Nenhum comentário fornecido.",
        "cta": "Ver no painel de admin",
        "footer": "Moderação de avaliações FreeLingo",
    },
    "it": {
        "email_title": "Nuova recensione ricevuta",
        "subject_prefix": "[Nuova recensione]",
        "logo": "FreeLingo: Nuova recensione",
        "author_label": "Inviata da",
        "rating_label": "Valutazione",
        "language_label": "Lingua di apprendimento",
        "comment_label": "Commento",
        "empty_comment": "Nessun commento fornito.",
        "cta": "Vedi nel pannello admin",
        "footer": "Moderazione recensioni FreeLingo",
    },
    "nl": {
        "email_title": "Nieuwe review ingediend",
        "subject_prefix": "[Nieuwe review]",
        "logo": "FreeLingo: Nieuwe review",
        "author_label": "Ingediend door",
        "rating_label": "Beoordeling",
        "language_label": "Leertaal",
        "comment_label": "Opmerking",
        "empty_comment": "Geen opmerking toegevoegd.",
        "cta": "Bekijk in adminpaneel",
        "footer": "FreeLingo-reviewmoderatie",
    },
    "pl": {
        "email_title": "Dodano nową recenzję",
        "subject_prefix": "[Nowa recenzja]",
        "logo": "FreeLingo: Nowa recenzja",
        "author_label": "Przesłana przez",
        "rating_label": "Ocena",
        "language_label": "Język nauki",
        "comment_label": "Komentarz",
        "empty_comment": "Nie podano komentarza.",
        "cta": "Zobacz w panelu admina",
        "footer": "Moderacja recenzji FreeLingo",
    },
    "ro": {
        "email_title": "Recenzie nouă trimisă",
        "subject_prefix": "[Recenzie nouă]",
        "logo": "FreeLingo: Recenzie nouă",
        "author_label": "Trimisă de",
        "rating_label": "Evaluare",
        "language_label": "Limba de învățare",
        "comment_label": "Comentariu",
        "empty_comment": "Nu a fost furnizat niciun comentariu.",
        "cta": "Vezi în panoul admin",
        "footer": "Moderare recenzii FreeLingo",
    },
    "ru": {
        "email_title": "Новый отзыв отправлен",
        "subject_prefix": "[Новый отзыв]",
        "logo": "FreeLingo: Новый отзыв",
        "author_label": "Отправил",
        "rating_label": "Оценка",
        "language_label": "Изучаемый язык",
        "comment_label": "Комментарий",
        "empty_comment": "Комментарий не указан.",
        "cta": "Открыть в панели администратора",
        "footer": "Модерация отзывов FreeLingo",
    },
    "tr": {
        "email_title": "Yeni yorum gönderildi",
        "subject_prefix": "[Yeni Yorum]",
        "logo": "FreeLingo: Yeni Yorum",
        "author_label": "Gönderen",
        "rating_label": "Puan",
        "language_label": "Öğrenilen dil",
        "comment_label": "Yorum",
        "empty_comment": "Yorum yazılmadı.",
        "cta": "Yönetim panelinde görüntüle",
        "footer": "FreeLingo yorum moderasyonu",
    },
    "sv": {
        "email_title": "Nytt omdöme har skickats in",
        "subject_prefix": "[Nytt omdöme]",
        "logo": "FreeLingo: Nytt omdöme",
        "author_label": "Skickat av",
        "rating_label": "Betyg",
        "language_label": "Språk som lärs in",
        "comment_label": "Kommentar",
        "empty_comment": "Ingen kommentar lämnades.",
        "cta": "Visa i administrationspanelen",
        "footer": "Moderering av FreeLingo-omdömen",
    },
    "da": {
        "email_title": "Ny anmeldelse er indsendt",
        "subject_prefix": "[Ny anmeldelse]",
        "logo": "FreeLingo: Ny anmeldelse",
        "author_label": "Indsendt af",
        "rating_label": "Bedømmelse",
        "language_label": "Sprog, der læres",
        "comment_label": "Kommentar",
        "empty_comment": "Ingen kommentar tilføjet.",
        "cta": "Se i administrationspanelet",
        "footer": "Moderering af FreeLingo-anmeldelser",
    },
    "fi": {
        "email_title": "Uusi arvostelu lähetetty",
        "subject_prefix": "[Uusi arvostelu]",
        "logo": "FreeLingo: Uusi arvostelu",
        "author_label": "Lähettäjä",
        "rating_label": "Arvosana",
        "language_label": "Opiskeltava kieli",
        "comment_label": "Kommentti",
        "empty_comment": "Kommenttia ei annettu.",
        "cta": "Näytä ylläpidossa",
        "footer": "FreeLingon arvostelujen moderointi",
    },
}


def _render_template(name: str, context: dict) -> str:
    """Render a plain HTML template, escaping interpolated values by default."""
    path = _TEMPLATES_DIR / name
    html = path.read_text(encoding="utf-8")
    for key, value in context.items():
        rendered = str(value) if isinstance(value, _SafeHtml) else escape(str(value), quote=True)
        html = html.replace(f"{{{{{key}}}}}", rendered)
    return html


async def _dispatch(subject: str, recipients: list[str], html: str) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=html,
        subtype=MessageType.html,
    )
    try:
        fm = FastMail(_get_mail_config())
        await fm.send_message(message)
    except Exception:
        logger.exception("Failed to send email to %s", recipients)


async def send_verification_email(
    to: str, display_name: str, token: str, locale: str = "en"
) -> None:
    """Send email verification link in the user's native language."""
    if not settings.EMAIL_ENABLED:
        return
    strings = _VERIFY_I18N.get(locale, _VERIFY_I18N["en"])
    url = f"{settings.APP_BASE_URL}/verify-email?token={token}"
    html = _render_template(
        "verify_email.html",
        {
            "greeting": strings["greeting"].format(name=display_name),
            "body": _safe_html(strings["body"]),
            "button": strings["button"],
            "link_fallback": strings["link_fallback"],
            "footer": strings["footer"],
            "url": url,
            "base_url": settings.APP_BASE_URL,
        },
    )
    await _dispatch(strings["subject"], [to], html)


async def send_reset_password_email(
    to: str, display_name: str, token: str, locale: str = "en"
) -> None:
    """Send password reset link in the user's native language."""
    if not settings.EMAIL_ENABLED:
        return
    strings = _RESET_I18N.get(locale, _RESET_I18N["en"])
    url = f"{settings.APP_BASE_URL}/reset-password?token={token}"
    html = _render_template(
        "reset_password.html",
        {
            "greeting": strings["greeting"].format(name=display_name),
            "body": _safe_html(strings["body"]),
            "button": strings["button"],
            "link_fallback": strings["link_fallback"],
            "footer": strings["footer"],
            "url": url,
            "base_url": settings.APP_BASE_URL,
        },
    )
    await _dispatch(strings["subject"], [to], html)


async def send_welcome_email(to: str, display_name: str, locale: str = "en") -> None:
    """Send a welcome email with onboarding steps in the user's native language."""
    if not settings.EMAIL_ENABLED:
        return
    strings = _WELCOME_I18N.get(locale, _WELCOME_I18N["en"])
    url = f"{settings.APP_BASE_URL}/dashboard"
    html = _render_template(
        "welcome.html",
        {
            "greeting": strings["greeting"].format(name=display_name),
            "body": _safe_html(strings["body"]),
            "step1": _safe_html(strings["step1"]),
            "step2": _safe_html(strings["step2"]),
            "step3": strings["step3"],
            "button": strings["button"],
            "footer": strings["footer"],
            "url": url,
            "base_url": settings.APP_BASE_URL,
        },
    )
    await _dispatch(strings["subject"], [to], html)


async def send_contact_email(
    sender_email: str, subject: str, description: str, locale: str = "en"
) -> None:
    """Forward a contact-form submission to the configured CONTACT_EMAIL address."""
    if not settings.EMAIL_ENABLED:
        return
    if not settings.CONTACT_EMAIL:
        logger.warning("CONTACT_EMAIL is not configured — contact form submission dropped")
        return
    strings = _CONTACT_I18N.get(locale, _CONTACT_I18N["en"])
    html = _render_template(
        "contact.html",
        {
            "email_title": strings["email_title"],
            "logo": strings["logo"],
            "from_label": strings["from_label"],
            "subject_label": strings["subject_label"],
            "message_label": strings["message_label"],
            "sender_email": sender_email,
            "subject": subject,
            "description": description,
            "footer": strings["footer"],
            "base_url": settings.APP_BASE_URL,
        },
    )
    message = MessageSchema(
        subject=f"{strings['subject_prefix']} {subject}",
        recipients=[settings.CONTACT_EMAIL],
        reply_to=[sender_email],
        body=html,
        subtype=MessageType.html,
    )
    try:
        fm = FastMail(_get_mail_config())
        await fm.send_message(message)
    except Exception:
        logger.exception("Failed to send contact email from %s", sender_email)
        raise


async def send_account_deleted_email(to: str, display_name: str, locale: str = "en") -> None:
    """Send account deletion confirmation in the user's native language."""
    if not settings.EMAIL_ENABLED:
        return
    strings = _DELETION_I18N.get(locale, _DELETION_I18N["en"])
    html = _render_template(
        "account_deleted.html",
        {
            "greeting": strings["greeting"].format(name=display_name),
            "body": _safe_html(strings["body"]),
            "footer": strings["footer"],
            "base_url": settings.APP_BASE_URL,
        },
    )
    await _dispatch(strings["subject"], [to], html)


async def send_feedback_notification(
    entry_type: str,
    title: str,
    description: str,
    author_username: str,
    entry_id: int,
    locale: str = "en",
) -> None:
    """Notify CONTACT_EMAIL when a new feature request or bug report is submitted.

    Sent in the first admin user's native language, with English fallback.
    Silently skipped when EMAIL_ENABLED=false or CONTACT_EMAIL is not set.
    Never raises — the feedback entry is already persisted before this is called.
    """
    if not settings.EMAIL_ENABLED:
        return
    if not settings.CONTACT_EMAIL:
        logger.warning("CONTACT_EMAIL is not configured — feedback notification dropped")
        return
    strings = _FEEDBACK_I18N.get(locale, _FEEDBACK_I18N["en"])
    type_label = strings["feature_label"] if entry_type == "feature" else strings["bug_label"]
    admin_url = f"{settings.APP_BASE_URL}/admin/feedback"
    html = _render_template(
        "feedback_submitted.html",
        {
            "email_title": strings["email_title"],
            "logo": strings["logo"],
            "type": entry_type,
            "type_label": type_label,
            "author_label": strings["author_label"],
            "author_username": author_username,
            "title_label": strings["title_label"],
            "title": title,
            "description_label": strings["description_label"],
            "description": description,
            "cta": strings["cta"],
            "footer": strings["footer"],
            "admin_url": admin_url,
            "base_url": settings.APP_BASE_URL,
        },
    )
    subject_prefix = (
        strings["feature_subject_prefix"]
        if entry_type == "feature"
        else strings["bug_subject_prefix"]
    )
    await _dispatch(f"{subject_prefix} {title}", [settings.CONTACT_EMAIL], html)


async def send_review_notification(
    user_display_name: str,
    rating: int,
    comment: str | None,
    target_language: str,
    review_id: int,
    locale: str = "en",
) -> None:
    """Notify CONTACT_EMAIL when a new user review is submitted.

    Sent in the first admin user's native language, with English fallback.
    Silently skipped when EMAIL_ENABLED=false or CONTACT_EMAIL is not set.
    Never raises — the review is already persisted before this is called.
    """
    if not settings.EMAIL_ENABLED:
        return
    if not settings.CONTACT_EMAIL:
        logger.warning("CONTACT_EMAIL is not configured — review notification dropped")
        return
    strings = _REVIEW_I18N.get(locale, _REVIEW_I18N["en"])
    admin_url = f"{settings.APP_BASE_URL}/admin/reviews"
    html = _render_template(
        "review_submitted.html",
        {
            "email_title": strings["email_title"],
            "logo": strings["logo"],
            "author_label": strings["author_label"],
            "user_display_name": user_display_name,
            "rating_label": strings["rating_label"],
            "rating": f"{rating}/5",
            "language_label": strings["language_label"],
            "target_language": target_language,
            "comment_label": strings["comment_label"],
            "comment": comment or strings["empty_comment"],
            "cta": strings["cta"],
            "admin_url": admin_url,
            "footer": strings["footer"],
            "base_url": settings.APP_BASE_URL,
        },
    )
    await _dispatch(
        f"{strings['subject_prefix']} {rating}/5 — {user_display_name}",
        [settings.CONTACT_EMAIL],
        html,
    )
