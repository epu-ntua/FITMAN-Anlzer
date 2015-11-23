# This is a set of ***language dependent*** methods for ***english*** text processing. It includes functions for the following:
# - find swear words

swear_words = ["ahole", "anus", "ash0le", "ash0les", "asholes", "ass", "assmonkey", "assface", "assh0le", "assh0lez",
               "asshole", "assholes", "assholz", "asswipe", "azzhole", "bassterds", "bastard", "bastards", "bastardz",
               "basterds", "basterdz", "biatch", "bitch", "bitches", "blowjob", "boffing", "butthole", "buttwipe",
               "c0ck", "c0cks", "c0k", "carpetmuncher", "cawk", "cawks", "clit", "cnts", "cntz", "cock", "cockhead",
               "cock-head", "cocks", "cocksucker", "cock-sucker", "crap", "cum", "cunt", "cunts", "cuntz", "dick",
               "dild0", "dild0s", "dildo", "dildos", "dilld0", "dilld0s", "dominatricks", "dominatrics", "dominatrix",
               "dyke", "enema", "fag", "fag1t", "faget", "fagg1t", "faggit", "faggot", "fagit", "fags", "fagz", "faig",
               "faigs", "fart", "flippingthebird", "fudgepacker", "fukah", "Fuken", "fuker", "fukk", "g00k", "gayboy",
               "gaygirl", "god-damned", "h00r", "h0ar", "h0re", "hells", "hoar", "hoor", "hoore", "jackoff", "jap",
               "japs", "jerk-off", "jisim", "jiss", "jizm", "jizz", "knob", "knobs", "knobz", "kunt", "kunts", "kuntz",
               "lipshits", "lipshitz", "massterbait", "masstrbait", "masstrbate", "masterbaiter", "masterbate",
               "masterbates", "mothafucker", "mothafuker", "mothafukkah", "mothafukker", "motherfucker", "motherfukah",
               "motherfuker", "motherfukkah", "motherfukker", "mother-fucker", "muthafucker", "muthafukah",
               "muthafuker", "muthafukkah", "muthafukker", "n1gr", "nastt", "nigger;", "nigur;", "niiger;", "niigr;",
               "orafis", "orgasim;", "orgasm", "orgasum", "oriface", "orifice", "orifiss", "packi", "packie", "packy",
               "paki", "pakie", "paky", "pecker", "peeenus", "peeenusss", "peenus", "peinus", "pen1s", "penas", "penis",
               "penis-breath", "penus", "penuus", "phuc", "phuck", "phuk", "phuker", "phukker", "polac", "polack",
               "polak", "poonani", "pr1c", "pr1ck", "pr1k", "pusse", "pussee", "pussy", "puuke", "puuker", "queer",
               "queers", "queerz", "qweers", "qweerz", "qweir", "recktum", "rectum", "retard", "sadist", "scank",
               "schlong", "screwing", "semen", "shyt", "shyte", "shytty", "shyty", "skanck", "skank", "skankee",
               "skankey", "skanks", "skanky", "slut", "sluts", "slutty", "slutz", "son-of-a-bitch", "tit", "turd",
               "va1jina", "vag1na", "vagiina", "vagina", "vaj1na", "vajina", "vullva", "vulva", "w0p", "wh00r", "wh0re",
               "whore", "xrated", "b!+ch", "bitch", "blowjob", "clit", "arschloch", "shit", "ass", "asshole", "b!tch",
               "b17ch", "b1tch", "bastard", "bi+ch", "boiolas", "buceta", "c0ck", "cawk", "chink", "cipa", "clits",
               "cock", "cum", "cunt", "dildo", "dirsa", "ejakulate", "fatass", "fux0r", "hoer", "hore", "jism", "kawk",
               "l3itch", "l3i+ch", "masturbate", "masterbat*", "masterbat3", "motherfucker", "s.o.b.", "mofo", "nazi",
               "nigga", "nigger", "nutsack", "phuck", "pimpis", "pusse", "pussy", "scrotum", "slut", "smut", "teets",
               "tits", "boobs", "b00bs", "teez", "testical", "testicle", "titt", "w00se", "jackoff", "wank", "whoar",
               "whore", "*damn", "*dyke", "@$$", "amcik", "andskota", "arse*", "assrammer", "ayir", "bi7ch", "bitch*",
               "bollock*", "breasts", "butt-pirate", "cabron", "cazzo", "chraa", "chuj", "Cock*", "cunt*", "d4mn",
               "daygo", "dego", "dick*", "dike*", "dupa", "dziwka", "ejackulate", "ekrem*", "ekto", "enculer", "faen",
               "fag*", "fanculo", "feces", "feg", "felcher", "ficken", "fitt*", "fotze", "futkretzn", "gay", "gook",
               "guiena", "h0r", "h4x0r", "hell", "helvete", "hoer*", "honkey", "huevon", "hui", "injun", "jizz",
               "kanker*", "kike", "klootzak", "kraut", "knulle", "kuk", "kuksuger", "Kurac", "kurwa", "kusi*", "kyrpa*",
               "lesbo", "mamhoon", "masturbat*", "merd*", "mibun", "monkleigh", "mouliewop", "muie", "mulkku", "muschi",
               "nazis", "nepesaurio", "nigger*", "orospu", "paska*", "perse", "picka", "pierdol*", "pillu*", "pimmel",
               "piss*", "pizda", "poontsee", "poop", "porn", "p0rn", "pr0n", "pula", "pule", "puta", "puto", "qahbeh",
               "queef*", "rautenberg", "schaffer", "scheiss*", "schlampe", "schmuck", "screw", "sharmuta", "sharmute",
               "shipal", "shiz", "skribz", "skurwysyn", "sphencter", "spic", "spierdalaj", "splooge", "suka", "b00b*",
               "testicle*", "titt*", "twat", "vittu", "wank*", "wetback*", "wichser", "wop*", "yed", "zabourah", "porn"]


def is_swearing_en(text):
    swear = False
    for w in swear_words:
        if w in text:
            swear = True
            break
    return swear

def process_en(text):
    return text
