"""
Listas de dominios para validación en memoria ultrarrápida (O(1)).
"""

FREE_PROVIDERS = {
    "gmail.com", "googlemail.com", "yahoo.com", "yahoo.es", "yahoo.com.ar",
    "hotmail.com", "hotmail.es", "outlook.com", "outlook.es", "live.com",
    "icloud.com", "me.com", "mac.com", "aol.com", "proton.me", "protonmail.com",
    "zoho.com", "gmx.com", "gmx.es", "mail.com", "yandex.com", "tutanota.com"
}

# Principales proveedores de correo temporal / desechable
DISPOSABLE_DOMAINS = {
    "10minutemail.com", "10minutemail.net", "10minutemail.org", "10minmail.com",
    "guerrillamail.com", "guerrillamail.net", "guerrillamail.org", "guerrillamail.biz",
    "guerrillamailblock.com", "sharklasers.com", "grr.la", "pokemail.net", "spam4.me",
    "mailinator.com", "mailinator.net", "mailinator2.com", "suremail.info", "spamherelots.com",
    "temp-mail.org", "temp-mail.io", "tempmail.com", "tempmail.net", "tempmail.ninja",
    "dispostable.com", "throwawaymail.com", "trashmail.com", "trashmail.net", "trashmail.me",
    "getairmail.com", "fakemailgenerator.com", "emailondeck.com", "yopmail.com", "yopmail.fr",
    "yopmail.net", "cool.fr.nf", "jetable.fr.nf", "courriel.fr.nf", "moncourrier.fr.nf",
    "monemail.fr.nf", "monmail.fr.nf", "hideemail.net", "mohmal.com", "burnerdelivery.com",
    "crazymailing.com", "nada.ltd", "nada.email", "inboxkitten.com", "mytemp.email",
    "generator.email", "discard.email", "discardmail.com", "spambog.com", "spambog.de",
    "tempinbox.com", "burnermail.io", "maildrop.cc", "harakirimail.com", "mailcatch.com",
    "getnada.com", "dropmail.me", "anonymbox.com", "luxusmail.org", "crazymailing.com",
    "boun.cr", "bouncr.com", "mailnesia.com", "nomail.xl.cx", "trashymail.com",
    "filzmail.com", "incognitomail.org", "deadaddress.com", "safetymail.info"
}
