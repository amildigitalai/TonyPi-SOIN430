#!/usr/bin/env python3
"""
TonyPi - Module Clinique SOIN 430 v1.0
PCI 1 et 2, Hygiène des mains, PQRSTU, AMPLE,
Auscultation pulmonaire, Inspection, Palpation, Percussion
USAGE PÉDAGOGIQUE UNIQUEMENT
"""

import pyttsx3
import speech_recognition as sr

# ══════════════════════════════════════════════════════════════════════════════
#  VOIX
# ══════════════════════════════════════════════════════════════════════════════
moteur = pyttsx3.init()
moteur.setProperty("rate", 145)
moteur.setProperty("volume", 1.0)

def parler(texte):
    print(f"\n[TonyPi] {texte}")
    moteur.say(texte)
    moteur.runAndWait()

def parler_liste(titre, items):
    parler(titre)
    for i, item in enumerate(items, 1):
        parler(f"{i}. {item}")

# ══════════════════════════════════════════════════════════════════════════════
#  BASE DE CONNAISSANCES CLINIQUES
# ══════════════════════════════════════════════════════════════════════════════
CLINIQUE = {

    # ── PCI 1 ─────────────────────────────────────────────────────────────
    "pci1": {
        "definition": (
            "PCI 1 — Précautions de base. "
            "S'appliquent à TOUS les patients, en TOUT temps, peu importe le diagnostic. "
            "Elles protègent le soignant et le patient contre la transmission de microorganismes."
        ),
        "elements": [
            "Hygiène des mains : avant et après tout contact avec le patient ou son environnement.",
            "Équipement de protection individuelle ou EPI : gants, masque, lunettes, blouse selon le risque d'éclaboussure.",
            "Hygiène respiratoire : couvrir la bouche et le nez en toussant ou éternuant.",
            "Manipulation sécuritaire des objets piquants et tranchants : ne jamais recapuchonner une aiguille.",
            "Décontamination de l'environnement : nettoyer et désinfecter le matériel réutilisable.",
            "Gestion sécuritaire des déchets : sacs jaunes pour déchets biomédicaux, contenants rigides pour piquants.",
            "Linge propre et linge souillé séparés : ne jamais secouer le linge souillé.",
            "Pratiques sécuritaires pour les injections : une seringue, une aiguille, un patient.",
        ],
        "court": (
            "PCI 1 sont les précautions de base qui s'appliquent à tous les patients en tout temps. "
            "Elles incluent l'hygiène des mains, le port d'EPI, la gestion sécuritaire des objets piquants "
            "et la décontamination de l'environnement."
        )
    },

    # ── PCI 2 ─────────────────────────────────────────────────────────────
    "pci2": {
        "definition": (
            "PCI 2 — Précautions additionnelles. "
            "S'ajoutent aux PCI 1 pour des patients porteurs de microorganismes transmissibles "
            "par contact, gouttelettes ou voie aérienne."
        ),
        "types": {
            "Contact": {
                "quand"   : "Patients avec infections cutanées, plaies infectées, diarrhée à C. difficile, SARM, ERV.",
                "mesures" : [
                    "Chambre individuelle ou regroupement de patients avec même infection.",
                    "Gants ET blouse à manches longues pour tout contact avec le patient ou son environnement.",
                    "Matériel dédié au patient : stéthoscope, tensiomètre, thermomètre.",
                    "Hygiène des mains obligatoire à la sortie de la chambre.",
                    "Affiche PCI contact sur la porte de la chambre.",
                ]
            },
            "Gouttelettes": {
                "quand"   : "Patients avec grippe, coqueluche, méningite, COVID-19, oreillons.",
                "mesures" : [
                    "Chambre individuelle ou distance minimale de 1 mètre entre les patients.",
                    "Masque chirurgical porté en entrant dans la chambre.",
                    "Le patient porte un masque chirurgical lors de transferts.",
                    "Limiter les déplacements du patient hors de la chambre.",
                    "Affiche PCI gouttelettes sur la porte.",
                ]
            },
            "Voie aérienne": {
                "quand"   : "Patients avec tuberculose active, rougeole, varicelle, zona disséminé.",
                "mesures" : [
                    "Chambre à pression négative obligatoire.",
                    "Masque N95 ou respirateur certifié pour tous les entrants.",
                    "Tester l'ajustement du masque N95 avant utilisation.",
                    "Porte de la chambre fermée en permanence.",
                    "Affiche PCI voie aérienne sur la porte.",
                ]
            }
        },
        "court": (
            "PCI 2 sont des précautions additionnelles aux PCI 1. "
            "Il y en a 3 types : Contact, Gouttelettes et Voie aérienne. "
            "Chaque type a ses propres mesures et s'applique selon le mode de transmission du microorganisme."
        )
    },

    # ── 4 MOMENTS HYGIÈNE DES MAINS ───────────────────────────────────────
    "mains": {
        "definition": (
            "L'OMS a identifié 4 moments clés pour l'hygiène des mains en milieu de soins. "
            "On utilise soit le lavage à l'eau et au savon, soit la friction avec solution hydroalcoolique."
        ),
        "moments": [
            "Moment 1 — AVANT le contact avec le patient : avant de toucher le patient, son lit ou ses effets personnels.",
            "Moment 2 — AVANT un acte aseptique : avant une injection, un soin de plaie, la pose d'un cathéter.",
            "Moment 3 — APRÈS un risque d'exposition aux liquides biologiques : après contact avec sang, urine, selles, sécrétions.",
            "Moment 4 — APRÈS le contact avec le patient ou son environnement : après avoir touché le patient, son lit, sa chambre.",
        ],
        "technique_SHA": [
            "Appliquer une dose de solution hydroalcoolique dans le creux de la main.",
            "Frotter paume contre paume.",
            "Frotter le dos de chaque main avec la paume de l'autre.",
            "Frotter les espaces interdigitaux paume contre paume doigts entrelacés.",
            "Frotter le dos des doigts contre la paume opposée.",
            "Frotter chaque pouce en rotation dans la paume opposée.",
            "Frotter les bouts des doigts en rotation dans la paume opposée.",
            "Durée minimale : 20 à 30 secondes jusqu'à séchage complet.",
        ],
        "technique_eau": [
            "Mouiller les mains à l'eau courante.",
            "Appliquer du savon et frotter pendant 40 à 60 secondes.",
            "Frotter toutes les surfaces : paumes, dos des mains, espaces interdigitaux, pouces, bouts des doigts.",
            "Rincer abondamment à l'eau courante.",
            "Sécher avec un essuie-mains à usage unique.",
            "Fermer le robinet avec l'essuie-mains usagé.",
        ],
        "quand_eau": "Utiliser eau et savon si mains visiblement souillées, après contact avec C. difficile, avant de manger.",
        "court": (
            "Il y a 4 moments pour l'hygiène des mains : "
            "1. Avant le contact patient. "
            "2. Avant un acte aseptique. "
            "3. Après risque d'exposition aux liquides biologiques. "
            "4. Après contact avec le patient ou son environnement."
        )
    },

    # ── PQRSTU ────────────────────────────────────────────────────────────
    "pqrstu": {
        "definition": (
            "PQRSTU est un outil mnémotechnique utilisé pour évaluer la douleur "
            "ou tout symptôme de façon systématique et complète."
        ),
        "elements": {
            "P": {
                "titre"  : "P — Provoquer / Pallier",
                "detail" : "Qu'est-ce qui provoque ou aggrave le symptôme? Qu'est-ce qui le soulage ou le pallie?"
            },
            "Q": {
                "titre"  : "Q — Qualité / Quantité",
                "detail" : "Comment décrivez-vous votre douleur? Brûlure, élancement, pression, crampe, coup de couteau? Quelle est son intensité de 0 à 10?"
            },
            "R": {
                "titre"  : "R — Région / Radiation / Irradiation",
                "detail" : "Où est localisée la douleur? Est-ce qu'elle irradie ou se propage ailleurs? Montrez-moi avec un doigt."
            },
            "S": {
                "titre"  : "S — Symptômes et signes associés",
                "detail" : "Y a-t-il d'autres symptômes associés? Nausées, vomissements, fièvre, essoufflement, diaphorèse?"
            },
            "T": {
                "titre"  : "T — Temps / Durée",
                "detail" : "Quand la douleur a-t-elle commencé? Est-elle continue ou intermittente? Depuis combien de temps?"
            },
            "U": {
                "titre"  : "U — Understand / Compréhension du patient",
                "detail" : "Qu'est-ce que vous pensez qui cause votre douleur? Qu'est-ce que cela signifie pour vous? Quelle est votre préoccupation principale?"
            },
        },
        "court": (
            "PQRSTU évalue un symptôme de façon complète : "
            "P comme Provoquer et Pallier, "
            "Q comme Qualité et Quantité, "
            "R comme Région et Irradiation, "
            "S comme Symptômes associés, "
            "T comme Temps et durée, "
            "U comme compréhension du patient."
        )
    },

    # ── AMPLE ─────────────────────────────────────────────────────────────
    "ample": {
        "definition": (
            "AMPLE est un outil mnémotechnique utilisé pour recueillir "
            "l'histoire de santé complète d'un patient rapidement, "
            "particulièrement en situation d'urgence."
        ),
        "elements": {
            "A": {
                "titre"  : "A — Allergies",
                "detail" : "Le patient a-t-il des allergies médicamenteuses ou alimentaires? Quelle est la réaction allergique?"
            },
            "M": {
                "titre"  : "M — Médicaments",
                "detail" : "Quels médicaments prend-il actuellement? Incluant les médicaments sans ordonnance, les suppléments et les produits naturels."
            },
            "P": {
                "titre"  : "P — Passé médical / Antécédents",
                "detail" : "Quels sont ses antécédents médicaux et chirurgicaux? Hospitalisations passées? Maladies chroniques?"
            },
            "L": {
                "titre"  : "L — Last meal / Dernier repas",
                "detail" : "Quand a-t-il mangé et bu pour la dernière fois? Quoi? Important avant une chirurgie ou anesthésie."
            },
            "E": {
                "titre"  : "E — Événement / Environnement",
                "detail" : "Qu'est-ce qui s'est passé? Quel est le contexte? Comment le problème actuel a-t-il commencé?"
            },
        },
        "court": (
            "AMPLE recueille l'histoire de santé complète : "
            "A comme Allergies, "
            "M comme Médicaments actuels, "
            "P comme Passé médical et antécédents, "
            "L comme Last meal ou dernier repas, "
            "E comme Événement déclencheur."
        )
    },

    # ── AUSCULTATION PULMONAIRE ───────────────────────────────────────────
    "auscultation": {
        "definition": (
            "L'auscultation pulmonaire consiste à écouter les bruits respiratoires "
            "avec un stéthoscope pour évaluer la ventilation et détecter des anomalies."
        ),
        "preparation": [
            "Expliquer la procédure au patient.",
            "Installer le patient en position assise si possible.",
            "Demander au patient de respirer profondément par la bouche.",
            "Réchauffer la membrane du stéthoscope avant de l'appliquer.",
            "Utiliser la membrane du stéthoscope pour les bruits pulmonaires.",
        ],
        "zones": [
            "Ausculter de façon symétrique : comparer le côté droit et le côté gauche.",
            "Commencer par les apex : au-dessus des clavicules, à l'avant.",
            "Descendre vers les bases pulmonaires : dans le dos, au niveau des omoplates.",
            "Ausculter au moins 4 à 6 zones de chaque côté.",
            "Au moins une inspiration et une expiration complètes par zone.",
        ],
        "bruits_normaux": [
            "Bruits vésiculaires : doux, à basse fréquence, entendus dans la majorité des champs pulmonaires.",
            "Bruits bronchiques : plus forts et aigus, entendus au niveau de la trachée et des grosses bronches.",
            "Bruits bronchovésiculaires : intermédiaires, entendus entre les omoplates.",
        ],
        "bruits_anormaux": [
            "Crépitants ou crackles : bruit de papier froissé, discontinu. Signe d'accumulation de liquide. Ex : pneumonie, oedème pulmonaire.",
            "Sibilances ou wheezing : sifflement aigu à l'expiration. Signe de bronchospasme. Ex : asthme, MPOC.",
            "Ronchi : bruit grave comme un ronflement. Signe de sécrétions dans les grosses voies aériennes.",
            "Stridor : sifflement aigu à l'inspiration. Signe d'obstruction des voies aériennes supérieures. Urgence.",
            "Frottement pleural : bruit de cuir qui frotte. Signe d'inflammation de la plèvre.",
            "Abolition des bruits : absence de bruits dans une zone. Signe d'atélectasie, épanchement ou pneumothorax.",
        ],
        "documentation": "Documenter : zones auscultées, bruits entendus, présence de bruits anormaux, symétrie, heure.",
        "court": (
            "L'auscultation pulmonaire s'effectue avec le stéthoscope de façon symétrique, "
            "des apex vers les bases. Les bruits normaux sont les bruits vésiculaires. "
            "Les bruits anormaux incluent les crépitants, les sibilances, les ronchi et le stridor."
        )
    },

    # ── INSPECTION ────────────────────────────────────────────────────────
    "inspection": {
        "definition": (
            "L'inspection est l'évaluation visuelle systématique du patient. "
            "C'est la première étape de l'examen physique. "
            "Elle s'effectue de façon ordonnée, de la tête aux pieds."
        ),
        "thorax": [
            "Observer la forme du thorax : cylindrique, en entonnoir, en carène.",
            "Observer la symétrie du soulèvement thoracique à chaque respiration.",
            "Observer la présence de tirage : intercostal, sous-costal, sus-sternal.",
            "Observer l'utilisation des muscles respiratoires accessoires : cou, épaules.",
            "Observer la fréquence et le rythme respiratoire selon MARSF.",
            "Observer la couleur de la peau : rosée, pâle, cyanosée, jaunâtre.",
            "Observer la présence de cicatrices, lésions ou déformations.",
        ],
        "general": [
            "Observer l'état général : alerte, orienté, confortable ou souffrant.",
            "Observer la posture et la position adoptée.",
            "Observer la couleur et l'humidité de la peau.",
            "Observer les muqueuses : lèvres, bouche, intérieur des joues.",
            "Observer les ongles : couleur, forme, temps de remplissage capillaire.",
            "Observer la présence d'oedème.",
            "Observer le faciès : grimaces, anxiété, douleur.",
        ],
        "court": (
            "L'inspection est l'évaluation visuelle du patient de la tête aux pieds. "
            "Pour le thorax, on observe la symétrie, le tirage, l'utilisation des muscles accessoires, "
            "la couleur de la peau et le rythme respiratoire selon MARSF."
        )
    },

    # ── PALPATION ─────────────────────────────────────────────────────────
    "palpation": {
        "definition": (
            "La palpation consiste à utiliser les mains pour évaluer les structures anatomiques. "
            "Elle permet d'évaluer la texture, la température, la sensibilité, la masse et les vibrations."
        ),
        "thorax": [
            "Palper les ganglions lymphatiques : cou, aisselles.",
            "Palper la trachée : doit être centrée, ligne médiane.",
            "Palper les côtes et le sternum : rechercher douleur ou crépitation.",
            "Évaluer l'expansion thoracique : placer les mains à plat dans le dos, pouces vers la colonne. Observer la symétrie lors de l'inspiration profonde.",
            "Évaluer les vibrations vocales ou frémissement vocal : placer la main à plat, demander au patient de dire trente-trois. Comparer les deux côtés.",
        ],
        "technique": [
            "Se laver les mains avant et après.",
            "Réchauffer les mains avant la palpation.",
            "Commencer par une palpation légère, puis profonde si nécessaire.",
            "Observer le visage du patient pour détecter une douleur.",
            "Palper les zones douloureuses en dernier.",
            "Documenter : localisation, consistance, taille, douleur, symétrie.",
        ],
        "court": (
            "La palpation évalue les structures par le toucher. "
            "Pour le thorax, on palpe la trachée, les côtes, l'expansion thoracique "
            "et les vibrations vocales en comparant toujours les deux côtés de façon symétrique."
        )
    },

    # ── PERCUSSION ────────────────────────────────────────────────────────
    "percussion": {
        "definition": (
            "La percussion consiste à tapoter la paroi thoracique pour produire des sons "
            "qui renseignent sur le contenu des structures sous-jacentes."
        ),
        "technique": [
            "Placer le majeur de la main non dominante à plat sur la peau, entre les côtes.",
            "Frapper avec le bout du majeur de la main dominante sur la première phalange du doigt posé.",
            "Le mouvement vient du poignet, pas du bras.",
            "Frapper 2 à 3 fois rapidement puis écouter le son produit.",
            "Percuter de façon symétrique : comparer droite et gauche.",
            "Percuter de haut en bas des apex vers les bases.",
        ],
        "sons": [
            "Sonorité normale : son creux et résonnant. Présent sur les poumons normalement aérés.",
            "Matité : son sourd comme sur un muscle. Présent sur le foie, le coeur ou un épanchement pleural ou une consolidation.",
            "Tympanisme : son très résonnant comme un tambour. Présent sur un estomac plein d'air ou un pneumothorax.",
            "Hypersonorité : son plus résonnant que normal. Présent dans l'emphysème ou le pneumothorax.",
        ],
        "zones": [
            "Percuter les apex pulmonaires au-dessus des clavicules.",
            "Percuter les champs pulmonaires antérieurs de chaque côté du sternum.",
            "Percuter les champs pulmonaires postérieurs dans le dos.",
            "Identifier les limites du foie : transition matité-sonorité.",
            "Identifier les bases pulmonaires : transition sonorité-matité.",
        ],
        "court": (
            "La percussion produit des sons selon le contenu des structures. "
            "La sonorité normale indique des poumons bien aérés. "
            "La matité indique un liquide ou une consolidation. "
            "Le tympanisme indique la présence d'air. "
            "On percute toujours de façon symétrique."
        )
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  MOTS-CLÉS
# ══════════════════════════════════════════════════════════════════════════════
MOTS_CLES = {
    "pci1"        : ["pci 1", "pci1", "précautions de base", "précaution standard", "protection de base"],
    "pci2"        : ["pci 2", "pci2", "précautions additionnelles", "isolement", "contact", "gouttelettes", "voie aérienne", "n95"],
    "mains"       : ["laver les mains", "hygiène des mains", "4 moments", "quatre moments", "solution hydroalcoolique", "savon", "sha"],
    "pqrstu"      : ["pqrstu", "évaluer douleur", "évaluation douleur", "provoquer", "pallier", "qualité douleur"],
    "ample"       : ["ample", "histoire de santé", "antécédents", "allergies médicaments", "dernier repas"],
    "auscultation": ["auscultation", "ausculter", "stéthoscope", "bruits pulmonaires", "crépitants", "sibilances", "wheezing", "poumons"],
    "inspection"  : ["inspection", "inspecter", "observer", "regarder thorax", "tirage", "symétrie thorax"],
    "palpation"   : ["palpation", "palper", "expansion thoracique", "vibrations vocales", "frémissement", "trachée"],
    "percussion"  : ["percussion", "percuter", "sonorité", "matité", "tympanisme", "tapoter thorax"],
}

# ══════════════════════════════════════════════════════════════════════════════
#  DÉTECTION ET RÉPONSE
# ══════════════════════════════════════════════════════════════════════════════
def detecter_sujet(question):
    q = question.lower()
    for sujet, mots in MOTS_CLES.items():
        for mot in mots:
            if mot in q:
                return sujet
    return None

def repondre_clinique(question):
    sujet = detecter_sujet(question)

    if not sujet:
        parler("Je n'ai pas reconnu le sujet. Tu peux demander : PCI 1, PCI 2, lavage des mains, PQRSTU, AMPLE, auscultation, inspection, palpation ou percussion.")
        return

    info = CLINIQUE[sujet]
    q    = question.lower()

    if sujet == "pci1":
        if any(m in q for m in ["détail", "élément", "liste", "quoi", "expliquer"]):
            parler(info["definition"])
            parler_liste("Les éléments des précautions de base PCI 1 sont :", info["elements"])
        else:
            parler(info["court"])
            parler("Veux-tu que je te détaille tous les éléments des PCI 1?")

    elif sujet == "pci2":
        if any(m in q for m in ["contact"]):
            t = info["types"]["Contact"]
            parler(f"PCI 2 Contact. Quand : {t['quand']}")
            parler_liste("Mesures à appliquer :", t["mesures"])
        elif any(m in q for m in ["gouttelette"]):
            t = info["types"]["Gouttelettes"]
            parler(f"PCI 2 Gouttelettes. Quand : {t['quand']}")
            parler_liste("Mesures à appliquer :", t["mesures"])
        elif any(m in q for m in ["aérien", "aérienne", "n95", "tuberculose"]):
            t = info["types"]["Voie aérienne"]
            parler(f"PCI 2 Voie aérienne. Quand : {t['quand']}")
            parler_liste("Mesures à appliquer :", t["mesures"])
        else:
            parler(info["court"])
            parler("Il y a 3 types : Contact, Gouttelettes et Voie aérienne. Lequel veux-tu que j'explique?")

    elif sujet == "mains":
        if any(m in q for m in ["moment", "quand"]):
            parler_liste("Les 4 moments pour l'hygiène des mains sont :", info["moments"])
        elif any(m in q for m in ["technique", "comment", "sha", "solution"]):
            parler_liste("Technique de friction avec solution hydroalcoolique :", info["technique_SHA"])
        elif any(m in q for m in ["savon", "eau", "lavage"]):
            parler_liste("Technique de lavage à l'eau et au savon :", info["technique_eau"])
            parler(f"Quand utiliser eau et savon : {info['quand_eau']}")
        else:
            parler(info["court"])
            parler("Veux-tu les 4 moments, la technique SHA ou la technique eau et savon?")

    elif sujet == "pqrstu":
        if any(m in q for m in ["détail", "expliquer", "complet", "tout"]):
            parler(info["definition"])
            for lettre, data in info["elements"].items():
                parler(f"{data['titre']} : {data['detail']}")
        else:
            parler(info["court"])
            parler("Veux-tu que je t'explique chaque lettre en détail?")

    elif sujet == "ample":
        if any(m in q for m in ["détail", "expliquer", "complet", "tout"]):
            parler(info["definition"])
            for lettre, data in info["elements"].items():
                parler(f"{data['titre']} : {data['detail']}")
        else:
            parler(info["court"])
            parler("Veux-tu que je t'explique chaque lettre en détail?")

    elif sujet == "auscultation":
        if any(m in q for m in ["bruit anormal", "crépitant", "sibilance", "wheezing", "ronchi", "stridor"]):
            parler_liste("Les bruits anormaux à l'auscultation pulmonaire sont :", info["bruits_anormaux"])
        elif any(m in q for m in ["bruit normal", "vésiculaire", "bronchique"]):
            parler_liste("Les bruits normaux à l'auscultation sont :", info["bruits_normaux"])
        elif any(m in q for m in ["comment", "technique", "zone", "où"]):
            parler_liste("Préparation :", info["preparation"])
            parler_liste("Zones à ausculter :", info["zones"])
        else:
            parler(info["court"])
            parler("Veux-tu que j'explique les bruits normaux, les bruits anormaux ou la technique?")

    elif sujet == "inspection":
        if any(m in q for m in ["thorax", "thoracique", "poitrine", "respiration"]):
            parler_liste("Inspection du thorax :", info["thorax"])
        elif any(m in q for m in ["général", "générale", "tête aux pieds"]):
            parler_liste("Inspection générale :", info["general"])
        else:
            parler(info["court"])
            parler("Veux-tu l'inspection du thorax ou l'inspection générale?")

    elif sujet == "palpation":
        if any(m in q for m in ["comment", "technique"]):
            parler_liste("Technique de palpation :", info["technique"])
        else:
            parler(info["court"])
            parler_liste("Palpation du thorax :", info["thorax"])

    elif sujet == "percussion":
        if any(m in q for m in ["son", "matité", "sonorité", "tympanisme"]):
            parler_liste("Les sons de la percussion sont :", info["sons"])
        elif any(m in q for m in ["comment", "technique"]):
            parler_liste("Technique de percussion :", info["technique"])
        else:
            parler(info["court"])
            parler("Veux-tu la technique de percussion ou les sons produits?")

# ══════════════════════════════════════════════════════════════════════════════
#  ÉCOUTE
# ══════════════════════════════════════════════════════════════════════════════
def ecouter(timeout=8, limite=15):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Écoute] Pose ta question...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=limite)
            texte = recognizer.recognize_google(audio, language="fr-CA")
            print(f"[Étudiant] {texte}")
            return texte
        except:
            return None

# ══════════════════════════════════════════════════════════════════════════════
#  BOUCLE PRINCIPALE
# ══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("  TonyPi - Module Clinique SOIN 430 v1.0")
    print("  PCI | Hygiène mains | PQRSTU | AMPLE")
    print("  Auscultation | Inspection | Palpation | Percussion")
    print("=" * 60)

    parler(
        "Bonjour! Je peux t'aider avec : "
        "PCI 1, PCI 2, les 4 moments du lavage des mains, "
        "le PQRSTU, le AMPLE, "
        "l'auscultation pulmonaire, l'inspection, la palpation et la percussion. "
        "Pose-moi une question!"
    )

    while True:
        question = ecouter()
        if not question:
            parler("Je n'ai pas entendu. Tu peux répéter?")
            continue

        q_lower = question.lower()
        if any(m in q_lower for m in ["quitter", "stop", "au revoir", "bye"]):
            parler("Bonne chance pour ton examen! À bientôt!")
            break

        if any(m in q_lower for m in ["aide", "liste", "que peux-tu"]):
            parler("Je couvre : PCI 1 et 2, les 4 moments hygiène des mains, PQRSTU, AMPLE, auscultation pulmonaire, inspection, palpation et percussion.")
            continue

        repondre_clinique(question)

# ══════════════════════════════════════════════════════════════════════════════
#  MODE TEXTE
# ══════════════════════════════════════════════════════════════════════════════
def mode_texte():
    print("=" * 60)
    print("  TonyPi Clinique - Mode texte")
    print("  Exemples : 'PCI 1', 'les 4 moments', 'PQRSTU', 'auscultation'")
    print("  Tape 'quitter' pour sortir")
    print("=" * 60)

    while True:
        question = input("\nTa question: ").strip()
        if not question:
            continue
        if question.lower() in ["quitter", "exit", "quit"]:
            print("Au revoir!")
            break
        repondre_clinique(question)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "texte":
        mode_texte()
    else:
        main()

# ══════════════════════════════════════════════════════════════════════════════
#  ÉCHELLE DE BRADEN — ajout au dictionnaire CLINIQUE
# ══════════════════════════════════════════════════════════════════════════════
CLINIQUE["braden"] = {
    "definition": (
        "L'échelle de Braden évalue le risque de développer des plaies de pression "
        "ou escarres. Elle comporte 6 sous-échelles. "
        "Le score total varie de 6 à 23. "
        "Plus le score est bas, plus le risque est élevé."
    ),
    "interpretation": {
        "19-23": "Pas de risque — Aucune intervention spéciale requise.",
        "15-18": "Risque léger — Surveillance accrue et mesures préventives de base.",
        "13-14": "Risque modéré — Protocole de prévention des plaies de pression.",
        "10-12": "Risque élevé — Protocole intensif, matelas spécialisé recommandé.",
        "6-9"  : "Risque très élevé — Protocole maximal, matelas thérapeutique obligatoire.",
    },
    "sous_echelles": {
        "1_perception": {
            "titre"  : "1. Perception sensorielle — score 1 à 4",
            "detail" : (
                "Évalue la capacité du patient à ressentir et exprimer l'inconfort lié à la pression. "
                "Score 1 : Complètement limitée — inconscient ou insensible à la douleur sur tout le corps. "
                "Score 2 : Très limitée — répond seulement à la douleur, déficit sensoriel sur la moitié du corps. "
                "Score 3 : Légèrement limitée — répond aux ordres verbaux, déficit sensoriel sur 1 ou 2 membres. "
                "Score 4 : Aucune limitation — répond aux ordres verbaux, pas de déficit sensoriel."
            )
        },
        "2_humidite": {
            "titre"  : "2. Humidité — score 1 à 4",
            "detail" : (
                "Évalue le degré d'humidité de la peau. "
                "Score 1 : Constamment humide — peau toujours mouillée par transpiration, urine. Linge changé à chaque retournement. "
                "Score 2 : Souvent humide — peau souvent mais pas toujours humide. Linge changé au moins une fois par quart. "
                "Score 3 : Parfois humide — peau parfois humide. Linge changé environ une fois par jour. "
                "Score 4 : Rarement humide — peau habituellement sèche. Linge changé selon les intervalles habituels."
            )
        },
        "3_activite": {
            "titre"  : "3. Activité — score 1 à 4",
            "detail" : (
                "Évalue le niveau d'activité physique du patient. "
                "Score 1 : Alité — confiné au lit en tout temps. "
                "Score 2 : En fauteuil — capacité de marche très limitée ou nulle, ne peut supporter son poids. "
                "Score 3 : Marche à l'occasion — marche de courtes distances avec ou sans aide, passe la majorité du temps au lit. "
                "Score 4 : Marche fréquemment — marche hors de la chambre au moins 2 fois par jour."
            )
        },
        "4_mobilite": {
            "titre"  : "4. Mobilité — score 1 à 4",
            "detail" : (
                "Évalue la capacité à changer et contrôler la position du corps. "
                "Score 1 : Complètement immobile — ne fait aucun mouvement même léger sans aide. "
                "Score 2 : Très limitée — fait parfois de légers changements de position, ne peut faire de changements fréquents seul. "
                "Score 3 : Légèrement limitée — fait de fréquents légers changements de position de façon autonome. "
                "Score 4 : Aucune limitation — fait de fréquents et importants changements de position sans aide."
            )
        },
        "5_nutrition": {
            "titre"  : "5. Nutrition — score 1 à 4",
            "detail" : (
                "Évalue le profil alimentaire habituel du patient. "
                "Score 1 : Très pauvre — ne mange jamais un repas complet, mange rarement plus du tiers des aliments offerts, peu de protéines. "
                "Score 2 : Probablement inadéquate — mange rarement un repas complet, généralement la moitié des aliments. "
                "Score 3 : Adéquate — mange plus de la moitié des repas, 4 portions de protéines par jour. "
                "Score 4 : Excellente — mange la totalité de chaque repas, 4 portions ou plus de protéines, ne refuse jamais un repas."
            )
        },
        "6_friction": {
            "titre"  : "6. Friction et cisaillement — score 1 à 3",
            "detail" : (
                "Évalue les problèmes liés au glissement et au frottement. "
                "Score 1 : Problème — nécessite une aide modérée à totale pour être mobilisé, glisse souvent dans le lit. "
                "Score 2 : Problème potentiel — se déplace avec difficulté, glisse parfois. "
                "Score 3 : Pas de problème apparent — se déplace seul dans le lit, a suffisamment de force musculaire."
            )
        },
    },
    "interventions": {
        "prevention": [
            "Retournement toutes les 2 heures chez le patient alité.",
            "Utiliser un matelas à réduction de pression selon le score.",
            "Garder la peau propre et sèche : hygiène et change rapide après incontinence.",
            "Appliquer une crème barrière protectrice sur les zones à risque.",
            "Hydrater la peau avec une lotion non parfumée.",
            "Installer des protecteurs de talons si score bas.",
            "Assurer un apport nutritionnel adéquat en protéines et calories.",
            "Éduquer le patient et la famille sur la prévention.",
        ],
        "zones_risque": [
            "Sacrum et coccyx : zone numéro 1 chez le patient alité.",
            "Talons : zone numéro 2, très vulnérables.",
            "Trochanters : en décubitus latéral.",
            "Ischions : chez le patient en fauteuil.",
            "Omoplates, coudes, oreilles, nuque.",
            "Toute zone osseuse en contact prolongé avec une surface.",
        ],
        "stades": [
            "Stade 1 : Rougeur qui ne blanchit pas à la pression. Peau intacte.",
            "Stade 2 : Perte partielle de l'épiderme. Plaie superficielle rose ou rouge.",
            "Stade 3 : Perte complète de l'épiderme et du derme. Graisse sous-cutanée visible.",
            "Stade 4 : Perte tissulaire totale. Os, tendon ou muscle visible.",
        ],
    },
    "court": (
        "L'échelle de Braden évalue le risque de plaies de pression sur 6 critères : "
        "perception sensorielle, humidité, activité, mobilité, nutrition et friction-cisaillement. "
        "Score total de 6 à 23. Score inférieur à 18 = risque présent. "
        "Plus le score est bas, plus le risque est élevé."
    )
}

# Ajouter les mots-clés Braden
MOTS_CLES["braden"] = [
    "braden", "échelle de braden", "plaie de pression", "escarre",
    "risque escarre", "ulcère de pression", "prévention plaie",
    "stade plaie", "zones de pression", "matelas", "retournement"
]

# ── Nouvelle fonction de réponse Braden ──────────────────────────────────────
_repondre_clinique_original = repondre_clinique

def repondre_clinique(question):
    sujet = detecter_sujet(question)

    if sujet == "braden":
        info = CLINIQUE["braden"]
        q    = question.lower()

        if any(m in q for m in ["score", "interprét", "risque", "chiffre", "valeur"]):
            parler("Interprétation du score de Braden :")
            for score, signif in info["interpretation"].items():
                parler(f"Score {score} : {signif}")

        elif any(m in q for m in ["critère", "sous-échelle", "évalué", "comment évaluer", "composante"]):
            parler("Les 6 sous-échelles de l'échelle de Braden sont :")
            for key, data in info["sous_echelles"].items():
                parler(data["titre"])

        elif any(m in q for m in ["perception", "sensoriel"]):
            parler(info["sous_echelles"]["1_perception"]["detail"])

        elif any(m in q for m in ["humidité", "humide", "peau mouillée"]):
            parler(info["sous_echelles"]["2_humidite"]["detail"])

        elif any(m in q for m in ["activité", "alité", "fauteuil", "marche"]):
            parler(info["sous_echelles"]["3_activite"]["detail"])

        elif any(m in q for m in ["mobilité", "mobile", "position", "bouger"]):
            parler(info["sous_echelles"]["4_mobilite"]["detail"])

        elif any(m in q for m in ["nutrition", "manger", "repas", "alimentation"]):
            parler(info["sous_echelles"]["5_nutrition"]["detail"])

        elif any(m in q for m in ["friction", "cisaillement", "glissement"]):
            parler(info["sous_echelles"]["6_friction"]["detail"])

        elif any(m in q for m in ["stade", "stades", "degré"]):
            parler_liste("Les stades des plaies de pression sont :", info["interventions"]["stades"])

        elif any(m in q for m in ["zone", "où", "localisation", "endroit"]):
            parler_liste("Les zones à risque de plaies de pression sont :", info["interventions"]["zones_risque"])

        elif any(m in q for m in ["intervention", "prévention", "que faire", "comment prévenir"]):
            parler_liste("Interventions de prévention des plaies de pression :", info["interventions"]["prevention"])

        else:
            parler(info["court"])
            parler(
                "Veux-tu que j'explique les scores et leur interprétation, "
                "les 6 critères d'évaluation, les stades des plaies, "
                "les zones à risque ou les interventions de prévention?"
            )
    else:
        _repondre_clinique_original(question)
