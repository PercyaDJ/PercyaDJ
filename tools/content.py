"""Every text of the profile README, as (English, French) pairs.

Edit a sentence here, then run `python3 tools/build.py` to regenerate the images and both README files.
"""

OWNER = "PercyaDJ"
CONTACT = "jolan@norkenix.com"
LINKEDIN = "https://www.linkedin.com/in/jolandemottie"

TITLE = ("Security, local AI and automation. A day with my tools.",
         "Sécurité, IA locale et automatisation. Une journée avec mes outils.")
BUTTON_MAIL = ("Send an email", "Écrire un mail")
NOW_PREFIX = ("Right now in France: ", "En ce moment en France : ")

# the "now" frame moves at each of these French times (0 = midnight, frame stays on Aurion)
NOWTXT = {
    8: ("the sun is rising, Lowsper is taking notes in the first meeting.",
        "le jour se lève, Lowsper prend les notes de la première réunion."),
    10: ("mid-morning, Lysbor is reviewing code on its way to production.",
         "la matinée avance, Lysbor relit le code qui part en production."),
    14: ("it's the afternoon, PatchBoard is sorting this week's reports.",
         "c'est l'après-midi, PatchBoard trie les rapports de la semaine."),
    18: ("the sun is setting, time for the photo lab.",
         "le soleil se couche, place à l'atelier photo."),
    22: ("it's night, Aurion is watching the sky.",
         "il fait nuit, Aurion surveille le ciel."),
    0: ("deep night, Aurion keeps watch until morning.",
        "c'est la nuit noire, Aurion veille jusqu'au matin."),
}

HOURS = [
    {"key": "lowsper", "label": "08:00", "what": ("The meeting", "La réunion"), "proj": ("Lowsper", "Lowsper"),
     "colors": ["#f3a76f", "#f7c99b", "#fde6c8"]},
    {"key": "lysbor", "label": "10:00", "what": ("Code ships", "Le code part"), "proj": ("Lysbor", "Lysbor"),
     "colors": ["#5ea9dd", "#9fd0ef", "#e1f2fb"]},
    {"key": "patchboard", "label": "14:00", "what": ("The reports", "Les rapports"), "proj": ("PatchBoard", "PatchBoard"),
     "colors": ["#3f8fd0", "#86c3ea", "#d8eef9"]},
    {"key": "labo", "label": "18:00", "what": ("The photo lab", "L'atelier photo"), "proj": ("Photo lab", "Labo photo"),
     "colors": ["#3b3f78", "#c4637a", "#f6a96b"]},
    {"key": "aurion", "label": "22:00", "what": ("Northern skies", "Le ciel du Nord"), "proj": ("Aurion", "Aurion"),
     "colors": ["#0b1633", "#2fe0a8", "#8b6cf0"]},
]

SIGNS_HINT = ("↑ click the signs to read ↑", "↑ cliquez sur les panneaux pour lire ↑")
SIGNS = [
    {"title": ("30 seconds", "30 secondes"), "sub": ("you hire, you decide", "vous recrutez, vous décidez"),
     "text": ("Cybersecurity and compliance consultant, certified ISO 27001 Lead Implementer. I bring companies into "
              "compliance (NIS2, GDPR, CRA) and build the tools that automate the work, powered by local AI.",
              "Consultant en cybersécurité et conformité, certifié ISO 27001 Lead Implementer. Je mets les entreprises "
              "en conformité (NIS2, RGPD, CRA) et je construis les outils qui automatisent ce travail grâce à l'IA locale.")},
    {"title": ("The tech side", "Côté tech"), "sub": ("you code, you audit", "vous codez, vous auditez"),
     "text": ("TypeScript, Python, Rust, PHP · local AI (Ollama, LM Studio, Mistral, Qwen, Codestral) and MCP servers · "
              "Semgrep, Trivy, Syft. AI writes a good share of the code. I own the architecture, the review, the "
              "testing and the hardening.",
              "TypeScript, Python, Rust, PHP · IA locale (Ollama, LM Studio, Mistral, Qwen, Codestral) et serveurs MCP · "
              "Semgrep, Trivy, Syft. L'IA écrit une bonne partie du code. Je porte l'architecture, la relecture, les "
              "tests et le durcissement.")},
    {"title": ("The human side", "Côté humain"), "sub": ("you're curious", "vous êtes curieux"),
     "text": ("Aurora photographer, curious about everything. A new topic? I'm in.",
              "Photographe d'aurores boréales et curieux de tout. Un nouveau sujet ? Je m'y mets.")},
]

HEADINGS = {
    "tech": ("Technical details", "Détails techniques"),
    "reserve": ("After midnight · The vault", "Après minuit · La réserve"),
}

PROJECTS = {
    "lowsper": {
        "title": ("Lowsper", "Lowsper"),
        "tag": ("Open source · runs in the browser", "Code ouvert · dans le navigateur"),
        "text": ("During a meeting, Lowsper writes down everything that is said and tells the speakers apart. I walk "
                 "out with what I need to write the minutes in two minutes. Nothing goes online: everything stays "
                 "on the computer.",
                 "Pendant une réunion, Lowsper écrit tout ce qui se dit et sépare qui parle. J'en ressors avec de "
                 "quoi faire le compte rendu en deux minutes. Rien ne part sur internet : tout reste sur l'ordinateur."),
        "tech": ("Whisper in the browser · a single HTML file, no install and no admin rights · speaker separation · "
                 "domain glossary · audio file import · Markdown export to Obsidian · JavaScript · MIT license.",
                 "Whisper dans le navigateur · un seul fichier HTML, sans installation ni droits administrateur · "
                 "séparation des intervenants · glossaire métier · import de fichiers audio · export Markdown vers "
                 "Obsidian · JavaScript · licence MIT."),
        "link": ("View the project", "Voir le projet"),
        "href": "https://github.com/PercyaDJ/Lowsper",
    },
    "lysbor": {
        "title": ("Lysbor", "Lysbor"),
        "tag": ("SaaS · open demo", "Logiciel en ligne · démo ouverte"),
        "text": ("When a team writes software, security flaws slip in. Lysbor reviews every new version, finds the "
                 "flaws and says who must fix what, and by when. It also warns you when European law requires a "
                 "problem to be reported.",
                 "Quand une équipe écrit un logiciel, des failles s'y glissent. Lysbor relit chaque nouvelle version, "
                 "trouve les failles et dit qui doit corriger quoi, avant quand. Il prévient aussi quand la loi "
                 "européenne impose de déclarer un problème."),
        "tech": ("CI/CD agent · static code analysis (SAST, Semgrep) · dependency and image scanning (SCA, Trivy) · "
                 "SBOM generation (Syft) · secret detection · action plans with owners · CRA reporting alerts · "
                 "SaaS, closed source.",
                 "Agent CI/CD · analyse statique du code (SAST, Semgrep) · analyse des dépendances et des images "
                 "(SCA, Trivy) · génération de SBOM (Syft) · détection de secrets · plans d'action avec responsables · "
                 "alertes de déclaration CRA · SaaS, code fermé."),
        "link": ("Try the demo", "Essayer la démo"),
        "href": "https://lysbor.com/",
    },
    "patchboard": {
        "title": ("PatchBoard", "PatchBoard"),
        "tag": ("Open source · a single file", "Code ouvert · un seul fichier"),
        "text": ("Every week, security teams receive dozens of files listing which computers are out of date. "
                 "PatchBoard takes them all in at once, shows the machines to fix and drafts the emails to warn the "
                 "right people.",
                 "Chaque semaine, les équipes sécurité reçoivent des dizaines de fichiers pour savoir quels "
                 "ordinateurs ne sont pas à jour. PatchBoard les avale d'un coup, montre les postes à corriger et "
                 "prépare les mails pour prévenir les bonnes personnes."),
        "tech": ("A single HTML file, zero dependencies, works offline · consolidates EPO (antivirus) and WSUS "
                 "(Windows updates) CSV exports · automatic file type and site detection · one-click email drafts · "
                 "MIT license.",
                 "Un seul fichier HTML, zéro dépendance, fonctionne hors ligne · consolidation des exports CSV EPO "
                 "(antivirus) et WSUS (mises à jour Windows) · détection automatique du type de fichier et du site · "
                 "brouillons de mail en un clic · licence MIT."),
        "link": ("View the project", "Voir le projet"),
        "href": "https://github.com/PercyaDJ/PatchBoard",
    },
    "labo": {
        "title": ("Photo lab", "Labo photo"),
        "tag": ("Private project · demo on request", "Projet privé · démo sur demande"),
        "text": ("I rebuilt my own photo lab so I no longer depend on Adobe. It sorts photos, edits them and cuts "
                 "videos. An AI can drive it through an MCP server to handle the repetitive work for me. Everything "
                 "runs locally.",
                 "J'ai reconstruit mon propre atelier photo pour ne plus dépendre d'Adobe. Il trie les photos, les "
                 "retouche et monte les vidéos. Une IA peut le piloter via un serveur MCP pour faire le travail "
                 "répétitif à ma place. Tout tourne en local."),
        "tech": ("In-house editing engine · interface built on ArtCraft (LightCraft, PhotoCraft…) · video playback "
                 "and editing with FFmpeg · MCP server to plug in a local or external AI · automatic sorting and "
                 "tagging · open source micro-models (4 to 279 MB): people detection · power line and cable "
                 "detection · image area reconstruction · 100% local.",
                 "Moteur de retouche maison · interface basée sur ArtCraft (LightCraft, PhotoCraft…) · lecture et "
                 "montage vidéo via FFmpeg · serveur MCP pour brancher une IA locale ou externe · tri et étiquetage "
                 "automatiques · micro-modèles open source (de 4 à 279 Mo) : détection de personnes · détection de "
                 "câbles et fils électriques · reconstruction de zones d'image · 100 % local."),
        "link": ("Request a demo", "Demander une démo"),
        "href": "mailto:jolan@norkenix.com?subject=Demo%20photo%20lab",
    },
    "aurion": {
        "title": ("Aurion", "Aurion"),
        "tag": ("Open source · Raspberry Pi", "Code ouvert · Raspberry Pi"),
        "text": ("A small computer and a camera you leave outside at night. It watches the sky on its own, "
                 "photographs the northern lights and ranks them for the morning. You set it up from your phone, "
                 "even without internet.",
                 "Un petit ordinateur et une caméra qu'on pose dehors la nuit. Il surveille le ciel tout seul, "
                 "photographie les aurores boréales et me les classe pour le matin. On le règle depuis son "
                 "téléphone, même sans internet."),
        "tech": ("Rust · Raspberry Pi 4 or 5 · HQ camera (IMX477 sensor) · built-in Wi-Fi access point · automatic "
                 "exposure · multi-night expedition mode · RAW photos · updates from the phone with rollback.",
                 "Rust · Raspberry Pi 4 ou 5 · caméra HQ (capteur IMX477) · point d'accès Wi-Fi intégré · exposition "
                 "automatique · mode expédition sur plusieurs nuits · photos RAW · mise à jour depuis le téléphone "
                 "avec retour arrière."),
        "link": ("View the project", "Voir le projet"),
        "href": "https://github.com/PercyaDJ/Aurion",
    },
}

RESERVE = {
    "badge": ("ON REQUEST", "SUR DEMANDE"),
    "alt": ("The vault, a locked fisherman's cabin at night. Tools shown on request: ",
            "La réserve, un rorbu fermé à clé la nuit. Outils montrés sur demande : "),
    "tags": [("GDPR and DPIA analysis", "Analyse RGPD et AIPD"),
             ("Business impact analysis", "Analyse d'impact (BIA)"),
             ("Security assurance plans", "Plans d'assurance sécurité"),
             ("SBOM scripts", "Scripts SBOM"),
             ("Proxmox hardening", "Durcissement Proxmox")],
    "text": ("Tools built for real engagements. The code stays closed, but I'm happy to demo them on request.",
             "Des outils construits pour de vraies missions. Le code reste fermé, mais je les montre volontiers sur "
             "demande."),
    "tech": ("GDPR and DPIA analysis (WP248 criteria) · business impact analysis (BIA) · security assurance plan "
             "generator · SBOM scripts · Proxmox VE hardening · runs locally, no data sent out.",
             "Analyse RGPD et AIPD (critères G29 WP248) · analyse d'impact sur l'activité (BIA) · générateur de plans "
             "d'assurance sécurité · scripts SBOM · durcissement de Proxmox VE · fonctionnement local, sans envoi de "
             "données."),
}

TALK = ("Want to talk? Local AI in compliance, automating NIS2 and CRA deliverables, vulnerability management, "
        "security architecture. Contact links are at the top.",
        "Envie d'en parler ? IA locale dans la conformité, automatisation des livrables NIS2 et CRA, gestion des "
        "vulnérabilités, architecture de sécurité. Les contacts sont tout en haut.")

# texts drawn inside the animations
TEXTS = {
    "lys_in": ("CODE GOES IN", "LE CODE ENTRE"),
    "lys_out": ("AN ACTION PLAN COMES OUT", "UN PLAN D'ACTION SORT"),
    "lys_rows": [(("Vulnerable library", "Web team · by Friday"), ("Faille dans une librairie", "Équipe web · avant vendredi")),
                 (("Password left in the code", "Infra team · today"), ("Mot de passe oublié dans le code", "Équipe infra · aujourd'hui")),
                 (("Must be reported (CRA)", "Security lead · within 24 h"), ("À déclarer (loi CRA)", "Responsable sécurité · sous 24 h"))],
    "lys_alt": ("Lysbor: code is reviewed and three issues come out as an action plan with owners and deadlines",
                "Lysbor : le code est relu et trois problèmes sortent en plan d'action avec responsables et délais"),
    "pb_in": ("30 MESSY FILES", "30 FICHIERS EN VRAC"),
    "pb_out": ("ONE CLEAR DASHBOARD", "UN SEUL TABLEAU CLAIR"),
    "pb_computers": ("computers", "ordinateurs"),
    "pb_update": ("to update", "à mettre à jour"),
    "pb_bars": [("Antivirus", "Antivirus"), ("Updates", "Mises à jour"), ("Both", "Les deux")],
    "pb_alt": ("PatchBoard: messy files become one dashboard, then an email goes out",
               "PatchBoard : des fichiers en vrac deviennent un tableau, puis un mail part"),
    "lw_in": ("PEOPLE TALK", "ON PARLE"),
    "lw_out": ("IT'S WRITTEN DOWN, ON THE COMPUTER", "C'EST ÉCRIT, SUR L'ORDINATEUR"),
    "lw_people": [("You", "Vous"), ("Participants", "Participants")],
    "lw_lines": [("09:02", ("You", "Vous"), ("Shall we lock the schedule?", "On valide le planning ?")),
                 ("09:02", ("Speaker 1", "Intervenant 1"), ("Yes, delivery on Friday.", "Oui, livraison vendredi.")),
                 ("09:03", ("Speaker 2", "Intervenant 2"), ("I'll draft the minutes.", "Je prépare le compte rendu.")),
                 ("09:03", ("You", "Vous"), ("Perfect, thanks everyone.", "Parfait, merci à tous."))],
    "lw_local": ("nothing leaves the computer", "rien ne quitte l'ordinateur"),
    "lw_alt": ("Lowsper: two people talk and the transcript writes itself, offline",
               "Lowsper : deux personnes parlent et le texte s'écrit tout seul, hors ligne"),
    "lb_in": ("THE RAW PHOTO", "LA PHOTO BRUTE"),
    "lb_out": ("AI SORTS, THE ENGINE EDITS", "L'IA TRIE, LE MOTEUR RETOUCHE"),
    "lb_tags": [("northern lights", "aurore boréale"), ("sharpness 94%", "netteté 94 %"),
                ("keep · 5 stars", "à garder · 5 étoiles"), ("video: timelapse ready", "vidéo : timelapse prêt")],
    "lb_mcp": ("MCP server", "serveur MCP"),
    "lb_mcp2": ("local or external AI plugged in", "IA locale ou externe branchée dessus"),
    "lb_alt": ("Photo lab: the photo is sorted by an AI, then edited, before and after",
               "Labo photo : la photo est triée par une IA puis retouchée, avant et après"),
    "au_detect": ("aurora detected", "aurore détectée"),
    "au_ranks": [("strongest", "la plus forte"), ("good", "belle"), ("faint", "faible")],
    "au_alt": ("Aurion: a Raspberry Pi camera on a tripod photographs the northern lights and ranks the shots",
               "Aurion : une caméra Raspberry Pi sur trépied photographie les aurores et classe les photos"),
}
