#!/usr/bin/env python3
"""
TonyPi - Module Évaluation clinique SOIN 430 v1.0
Morse, Glasgow, Plaies, Douleur, 5P, FFE
USAGE PÉDAGOGIQUE UNIQUEMENT
"""

import pyttsx3
import speech_recognition as sr

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
#  BASE DE CONNAISSANCES
# ══════════════════════════════════════════════════════════════════════════════
EVALUATION = {

    # ── ÉCHELLE DE MORSE ──────────────────────────────────────────────────
    "morse": {
        "definition": (
            "L'échelle de Morse évalue le risque de chute d'un patient. "
            "Elle comporte 6 critères. "
            "Score total de 0 à 125. "
            "Plus le score est élevé, plus le risque de chute est grand."
        ),
        "interpretation": {
            "0-24"  : "Risque faible — Mesures de prévention de base.",
            "25-44" : "Risque modéré — Mettre en place les interventions standard de prévention des chutes.",
            "45 et plus" : "Risque élevé — Protocole intensif de prévention des chutes obligatoire.",
        },
        "criteres": {
            "1": {
                "titre" : "1. Antécédents de chutes — 0 ou 25 points",
                "detail": "Non = 0 point. Oui, chute dans les 3 derniers mois = 25 points."
            },
            "2": {
                "titre" : "2. Diagnostic secondaire — 0 ou 15 points",
                "detail": "Non = 0 point. Oui, plus d'un diagnostic médical = 15 points."
            },
            "3": {
                "titre" : "3. Aide à la marche — 0, 15 ou 30 points",
                "detail": (
                    "Aucune aide ou alitement ou fauteuil roulant = 0 point. "
                    "Béquilles, canne ou marchette = 15 points. "
                    "S'appuie sur les meubles pour marcher = 30 points."
                )
            },
            "4": {
                "titre" : "4. Perfusion intraveineuse ou héparine — 0 ou 20 points",
                "detail": "Non = 0 point. Oui, patient sous perfusion IV ou héparine = 20 points."
            },
            "5": {
                "titre" : "5. Démarche et transfert — 0, 10 ou 20 points",
                "detail": (
                    "Normale ou alitement ou immobile = 0 point. "
                    "Faible : légèrement voûtée mais capable de se lever seul = 10 points. "
                    "Altérée : grandes difficultés à se lever, courtes enjambées = 20 points."
                )
            },
            "6": {
                "titre" : "6. État mental — 0 ou 15 points",
                "detail": (
                    "Orienté selon ses capacités = 0 point. "
                    "Surestime ses capacités ou oublie ses limites = 15 points."
                )
            },
        },
        "interventions": [
            "Afficher le bracelet de risque de chute selon le protocole de l'établissement.",
            "Mettre les ridelles en place selon l'état du patient.",
            "Placer la sonnette d'appel à portée de main.",
            "Assurer un éclairage adéquat, surtout la nuit.",
            "Garder l'environnement dégagé : pas d'obstacles au sol.",
            "Chaussures antidérapantes ou bas antidérapants.",
            "Accompagner le patient lors des déplacements si score élevé.",
            "Éduquer le patient et la famille sur le risque de chute.",
            "Revoir les médicaments pouvant causer des étourdissements.",
            "Documenter le score et les interventions au dossier.",
        ],
        "court": (
            "L'échelle de Morse évalue le risque de chute sur 6 critères : "
            "antécédents de chutes, diagnostic secondaire, aide à la marche, "
            "perfusion IV, démarche et état mental. "
            "Score 0-24 = faible, 25-44 = modéré, 45 et plus = élevé."
        )
    },

    # ── ÉCHELLE DE GLASGOW ────────────────────────────────────────────────
    "glasgow": {
        "definition": (
            "L'échelle de Glasgow ou GCS évalue l'état de conscience d'un patient. "
            "Elle comporte 3 composantes : ouverture des yeux, réponse verbale et réponse motrice. "
            "Score total de 3 à 15. "
            "15 = conscient normal. Moins de 8 = coma."
        ),
        "composantes": {
            "yeux": {
                "titre" : "Ouverture des yeux — Y — score 1 à 4",
                "detail": (
                    "Y4 : Spontanée — ouvre les yeux spontanément. "
                    "Y3 : Au bruit — ouvre les yeux à la voix ou à l'appel. "
                    "Y2 : À la douleur — ouvre les yeux seulement à la stimulation douloureuse. "
                    "Y1 : Aucune — n'ouvre pas les yeux même à la douleur."
                )
            },
            "verbale": {
                "titre" : "Réponse verbale — V — score 1 à 5",
                "detail": (
                    "V5 : Orientée — répond correctement aux questions sur nom, lieu, date. "
                    "V4 : Confuse — répond mais est désorientée dans le temps ou l'espace. "
                    "V3 : Inappropriée — utilise des mots isolés, pas de phrase cohérente. "
                    "V2 : Incompréhensible — émet des sons mais pas de mots reconnaissables. "
                    "V1 : Aucune — aucune réponse verbale même à la douleur."
                )
            },
            "motrice": {
                "titre" : "Réponse motrice — M — score 1 à 6",
                "detail": (
                    "M6 : Obéit aux ordres — exécute les commandes simples. "
                    "M5 : Localise la douleur — tente de retirer le stimulus douloureux. "
                    "M4 : Retrait — retire le membre à la douleur de façon réflexe. "
                    "M3 : Flexion anormale — décortication, flexion des bras sur la poitrine. "
                    "M2 : Extension anormale — décérébration, extension rigide des membres. "
                    "M1 : Aucune — aucune réponse motrice même à la douleur."
                )
            },
        },
        "interpretation": {
            "15"    : "Conscience normale.",
            "13-14" : "Trouble léger de la conscience.",
            "9-12"  : "Trouble modéré de la conscience.",
            "8 et moins" : "Coma — protéger les voies aériennes. Aviser immédiatement.",
            "3"     : "Score minimal — coma profond ou mort cérébrale.",
        },
        "interventions": [
            "Évaluer le GCS à l'admission et selon la fréquence prescrite.",
            "Noter le score total ET les scores individuels Y, V, M.",
            "Comparer avec les évaluations précédentes : toute diminution de 2 points = aviser.",
            "Position latérale de sécurité si GCS inférieur à 8 et patient sans protection des voies.",
            "Aviser l'infirmière responsable de tout changement du score.",
            "Documenter : score Y, V, M, total, heure, comportement observé.",
        ],
        "court": (
            "Glasgow évalue la conscience sur 3 critères : "
            "Yeux Y de 1 à 4, Verbale V de 1 à 5, Motrice M de 1 à 6. "
            "Score total de 3 à 15. "
            "15 = normal, inférieur à 8 = coma, aviser immédiatement."
        )
    },

    # ── TYPES DE PLAIES ET SOINS ──────────────────────────────────────────
    "plaies": {
        "definition": (
            "Une plaie est une lésion de la peau ou des tissus sous-jacents. "
            "L'infirmière évalue la plaie, assure les soins selon l'ordonnance "
            "et documente l'évolution."
        ),
        "types": {
            "Aiguë": {
                "def"    : "Plaie récente qui guérit normalement selon les étapes prévues.",
                "exemples": "Incision chirurgicale, lacération, abrasion, brûlure.",
                "soins"  : "Nettoyage, protection stérile, surveiller les signes d'infection."
            },
            "Chronique": {
                "def"    : "Plaie qui ne guérit pas dans les délais normaux, souvent plus de 4 semaines.",
                "exemples": "Ulcère de jambe, plaie de pression, pied diabétique.",
                "soins"  : "Débridement si nécessaire, pansement spécialisé, traitement cause sous-jacente."
            },
            "Pression": {
                "def"    : "Lésion cutanée causée par une pression prolongée sur une zone osseuse.",
                "stades" : [
                    "Stade 1 : Rougeur non blanchissante sur peau intacte.",
                    "Stade 2 : Perte partielle de l'épiderme, plaie superficielle.",
                    "Stade 3 : Perte complète de l'épiderme, graisse visible.",
                    "Stade 4 : Os, tendon ou muscle visible.",
                ],
                "soins"  : "Décharger la pression, nettoyer, pansement adapté selon le stade."
            },
        },
        "evaluation_plaie": {
            "T": "Tissu : granulation rouge vif, fibrine jaune, nécrose noire ou escarrotique.",
            "A": "Aspect des bords : nets, irréguliers, décollés, hyperkératose.",
            "I": "Infection ou inflammation : rougeur, chaleur, oedème, douleur, odeur, exsudat purulent.",
            "M": "Macération : peau périplaie blanche et ramollie par l'humidité.",
        },
        "signes_infection": [
            "Rougeur et chaleur autour de la plaie.",
            "Gonflement ou oedème.",
            "Douleur augmentée.",
            "Exsudat purulent, jaunâtre ou verdâtre.",
            "Odeur nauséabonde.",
            "Fièvre et frissons.",
            "Bords de la plaie qui s'élargissent malgré les soins.",
        ],
        "technique_soin": [
            "Vérifier l'ordonnance de soin de plaie.",
            "Rassembler le matériel stérile nécessaire.",
            "Se laver les mains selon les 4 moments.",
            "Mettre les gants propres pour retirer l'ancien pansement.",
            "Évaluer la plaie : taille, profondeur, tissu, exsudat, odeur, bords, peau périplaie.",
            "Nettoyer la plaie avec sérum physiologique ou solution prescrite, du centre vers l'extérieur.",
            "Changer de gants stériles pour appliquer le nouveau pansement.",
            "Appliquer le pansement selon l'ordonnance.",
            "Documenter : évaluation complète, soins effectués, pansement appliqué, tolérance du patient.",
        ],
        "court": (
            "Les plaies se divisent en plaies aiguës et chroniques. "
            "L'évaluation utilise le TAIM : Tissu, Aspect des bords, Infection et Macération. "
            "Les signes d'infection incluent rougeur, chaleur, oedème, exsudat purulent et odeur."
        )
    },

    # ── ÉCHELLES DE DOULEUR ───────────────────────────────────────────────
    "douleur_echelle": {
        "definition": (
            "La douleur est le 5e signe vital. "
            "Plusieurs échelles permettent d'évaluer la douleur selon l'âge "
            "et l'état cognitif du patient."
        ),
        "echelles": {
            "Numérique": {
                "pour"   : "Adultes capables de communiquer.",
                "comment": "Demander au patient de donner un chiffre de 0 à 10. 0 = aucune douleur. 10 = pire douleur imaginable.",
                "interpretation": "1-3 = légère, 4-6 = modérée, 7-10 = sévère."
            },
            "EVA": {
                "pour"   : "Adultes capables de comprendre une échelle visuelle.",
                "comment": "Réglette avec une ligne de 0 à 10 cm. Le patient déplace le curseur selon son niveau de douleur.",
                "interpretation": "0-3 = légère, 4-6 = modérée, 7-10 = sévère."
            },
            "Wong-Baker": {
                "pour"   : "Enfants de 3 ans et plus, personnes âgées, difficultés cognitives.",
                "comment": "6 visages allant du sourire au pleurs. Le patient pointe le visage qui correspond à sa douleur.",
                "interpretation": "Visage 0 = pas de douleur. Visage 10 = pire douleur possible."
            },
            "CPOT": {
                "pour"   : "Patients intubés ou non communicants en soins critiques.",
                "comment": "Évalue 4 indicateurs : expression faciale, mouvements corporels, tension musculaire, compliance au ventilateur ou vocalisation.",
                "interpretation": "Score de 0 à 8. Score de 2 et plus indique une douleur significative."
            },
            "FLACC": {
                "pour"   : "Enfants de 2 mois à 7 ans ou patients non verbaux.",
                "comment": "Évalue Face, Jambes, Activité, Cris et Consolabilité. Chaque critère de 0 à 2.",
                "interpretation": "Score de 0 à 10. 0 = détendu et confortable. 10 = douleur sévère."
            },
        },
        "principes": [
            "Toujours croire le patient sur sa douleur : la douleur est subjective.",
            "Réévaluer la douleur après chaque intervention, idéalement après 30 minutes.",
            "Utiliser la même échelle pour le même patient pour suivre l'évolution.",
            "Documenter le score avant et après les interventions.",
            "Une réduction de 2 points sur 10 est considérée cliniquement significative.",
            "Si le patient ne peut pas communiquer, utiliser une échelle comportementale.",
        ],
        "court": (
            "Les principales échelles de douleur sont : "
            "numérique de 0 à 10 pour les adultes, "
            "EVA visuelle pour les adultes, "
            "Wong-Baker avec les visages pour les enfants et personnes âgées, "
            "CPOT pour les patients intubés, "
            "FLACC pour les enfants non verbaux."
        )
    },

    # ── SIGNES NEUROVASCULAIRES 5P ────────────────────────────────────────
    "cinq_p": {
        "definition": (
            "Les signes neurovasculaires ou 5P évaluent la circulation et l'innervation "
            "d'un membre, particulièrement après un traumatisme, une chirurgie orthopédique "
            "ou la pose d'un plâtre ou d'une attelle."
        ),
        "signes": {
            "P1": {
                "titre" : "P1 — Pouls",
                "detail": (
                    "Évaluer le pouls distal du membre affecté. "
                    "Comparer avec le membre controlatéral. "
                    "Normal : pouls présent, fort et régulier. "
                    "Anormal : pouls faible, filant ou absent. Aviser immédiatement."
                )
            },
            "P2": {
                "titre" : "P2 — Pâleur",
                "detail": (
                    "Observer la couleur de la peau et du lit unguéal. "
                    "Évaluer le temps de remplissage capillaire : appuyer 5 secondes sur l'ongle, la couleur doit revenir en moins de 2 secondes. "
                    "Normal : peau rosée, TRC inférieur à 2 secondes. "
                    "Anormal : pâleur, cyanose, marbrures, TRC supérieur à 2 secondes."
                )
            },
            "P3": {
                "titre" : "P3 — Paresthésie",
                "detail": (
                    "Évaluer la sensibilité du membre : picotements, engourdissements, sensation de brûlure. "
                    "Demander au patient : Avez-vous des picotements, des engourdissements? "
                    "Normal : aucune paresthésie, sensibilité intacte. "
                    "Anormal : présence de picotements, engourdissement ou absence de sensation."
                )
            },
            "P4": {
                "titre" : "P4 — Paralysie",
                "detail": (
                    "Évaluer la motricité du membre : capacité de mobiliser les doigts ou les orteils. "
                    "Demander au patient de bouger les doigts ou les orteils selon le membre affecté. "
                    "Normal : mobilisation active possible, force musculaire conservée. "
                    "Anormal : faiblesse, diminution de la force ou impossibilité de bouger."
                )
            },
            "P5": {
                "titre" : "P5 — Douleur",
                "detail": (
                    "Évaluer la douleur au niveau du membre et à la mobilisation passive. "
                    "Une douleur intense et disproportionnée à la mobilisation passive est un signe d'alarme majeur. "
                    "Normal : douleur légère et proportionnelle à la blessure. "
                    "Anormal : douleur intense, augmentée, résistante aux analgésiques. Aviser immédiatement."
                )
            },
        },
        "frequence": [
            "Après une fracture ou traumatisme : toutes les 15 à 30 minutes pendant les 2 premières heures.",
            "Après pose d'un plâtre ou attelle : toutes les 30 minutes pendant 2 heures, puis toutes les heures.",
            "Après chirurgie orthopédique : selon l'ordonnance, généralement toutes les heures.",
            "Si anomalie détectée : aviser immédiatement et augmenter la fréquence.",
        ],
        "signes_alarme": [
            "Douleur intense et disproportionnée non soulagée par les analgésiques.",
            "Pâleur ou cyanose du membre.",
            "Absence de pouls distal.",
            "Engourdissement ou paralysie soudaine.",
            "Temps de remplissage capillaire supérieur à 3 secondes.",
            "Ces signes peuvent indiquer un syndrome des loges : urgence chirurgicale.",
        ],
        "court": (
            "Les 5P évaluent la circulation et l'innervation d'un membre : "
            "P1 Pouls, P2 Pâleur et TRC, P3 Paresthésie, P4 Paralysie, P5 douleur ou Pain. "
            "Toute anomalie doit être signalée immédiatement. "
            "Douleur intense disproportionnée = syndrome des loges possible, urgence."
        )
    },

    # ── FFE — FEUILLE DE FLOT D'ÉVALUATION ───────────────────────────────
    "ffe": {
        "definition": (
            "La Feuille de Flot d'Évaluation ou FFE est un outil de documentation systématique "
            "qui permet de consigner les évaluations infirmières de façon organisée et complète. "
            "Elle assure la continuité des soins entre les quarts de travail."
        ),
        "composantes": {
            "Identification": [
                "Nom, prénom et date de naissance du patient.",
                "Numéro de chambre et de lit.",
                "Médecin traitant.",
                "Date et heure de l'évaluation.",
                "Nom de l'infirmière.",
            ],
            "Signes_vitaux": [
                "Tension artérielle selon FAR : Fréquence, Amplitude, Rythme Régulier ou Irrégulier.",
                "Fréquence cardiaque selon FAR.",
                "Respiration selon MARSF : Mécanique, Amplitude, Rythme, Symétrie, Fréquence.",
                "Température en degrés Celsius.",
                "Saturation en oxygène SpO2 en pourcent.",
                "Douleur selon l'échelle appropriée de 0 à 10.",
                "Glycémie capillaire si applicable.",
            ],
            "Evaluation_systemes": [
                "Neurologique : Glasgow, orientation, état de conscience.",
                "Cardiovasculaire : pouls, couleur de la peau, TRC, oedème.",
                "Respiratoire : MARSF, auscultation pulmonaire, oxygène.",
                "Digestif : appétit, nausées, vomissements, bruits intestinaux, élimination.",
                "Urinaire : diurèse, couleur, caractéristiques de l'urine.",
                "Tégumentaire : intégrité de la peau, plaies, rougeurs, Braden.",
                "Musculosquelettique : mobilité, force, 5P si applicable.",
                "Douleur : PQRSTU complet.",
            ],
            "Risques": [
                "Score de Morse : risque de chute.",
                "Score de Braden : risque de plaie de pression.",
                "Risque de délirium si applicable.",
            ],
            "Plan_soins": [
                "Problèmes infirmiers identifiés.",
                "Objectifs de soins.",
                "Interventions planifiées.",
                "Résultats attendus.",
                "Évaluation des résultats.",
            ],
        },
        "conseils": [
            "Compléter la FFE au début du quart de travail puis à chaque changement de condition.",
            "Être factuel et objectif : décrire ce qu'on observe, pas ce qu'on interprète.",
            "Utiliser les abréviations reconnues du milieu.",
            "Signer chaque entrée avec nom, prénom et titre professionnel.",
            "Ne jamais laisser d'espaces vides, mettre N-A si non applicable.",
            "La FFE doit être lisible, complète et refléter fidèlement l'état du patient.",
            "En cas d'erreur : un trait, la mention erreur, initiales. Ne jamais effacer ni utiliser du correcteur.",
        ],
        "court": (
            "La FFE documente systématiquement l'évaluation infirmière complète. "
            "Elle inclut les signes vitaux selon FAR et MARSF, "
            "l'évaluation de chaque système, les scores de Morse et Braden, "
            "et le plan de soins. Elle assure la continuité entre les quarts."
        )
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  MOTS-CLÉS
# ══════════════════════════════════════════════════════════════════════════════
MOTS_CLES = {
    "morse"         : ["morse", "chute", "risque de chute", "tomber", "prévention chute", "bracelet chute"],
    "glasgow"       : ["glasgow", "gcs", "état de conscience", "coma", "conscience", "yeux verbale motrice"],
    "plaies"        : ["plaie", "plaies", "escarre", "ulcère", "pansement", "soin de plaie", "infection plaie", "taim", "granulation"],
    "douleur_echelle":["échelle de douleur", "wong baker", "wong-baker", "eva", "cpot", "flacc", "évaluer douleur", "5e signe vital"],
    "cinq_p"        : ["5p", "cinq p", "neurovasculaire", "signes neurovasculaires", "pouls pâleur", "paresthésie", "paralysie", "syndrome des loges", "plâtre", "fracture"],
    "ffe"           : ["ffe", "feuille de flot", "feuille flot", "documentation", "dossier infirmier", "noter", "documenter", "feuille évaluation"],
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

def repondre_evaluation(question):
    sujet = detecter_sujet(question)
    if not sujet:
        parler("Je n'ai pas reconnu le sujet. Tu peux demander : Morse, Glasgow, plaies, échelle de douleur, 5P neurovasculaires ou FFE.")
        return

    info = EVALUATION[sujet]
    q    = question.lower()

    # ── MORSE ──
    if sujet == "morse":
        if any(m in q for m in ["critère", "comment évaluer", "composante", "sous-échelle"]):
            parler(info["definition"])
            for num, data in info["criteres"].items():
                parler(f"{data['titre']} : {data['detail']}")
        elif any(m in q for m in ["score", "interprét", "risque", "valeur"]):
            parler("Interprétation du score de Morse :")
            for score, signif in info["interpretation"].items():
                parler(f"Score {score} : {signif}")
        elif any(m in q for m in ["intervention", "que faire", "prévenir"]):
            parler_liste("Interventions de prévention des chutes :", info["interventions"])
        else:
            parler(info["court"])
            parler("Veux-tu les critères d'évaluation, les scores ou les interventions de prévention?")

    # ── GLASGOW ──
    elif sujet == "glasgow":
        if any(m in q for m in ["oeil", "yeux", "ouverture"]):
            parler(info["composantes"]["yeux"]["detail"])
        elif any(m in q for m in ["verbal", "parole", "voix"]):
            parler(info["composantes"]["verbale"]["detail"])
        elif any(m in q for m in ["motrice", "mouvement", "bouger"]):
            parler(info["composantes"]["motrice"]["detail"])
        elif any(m in q for m in ["score", "interprét", "coma", "valeur"]):
            parler("Interprétation du score de Glasgow :")
            for score, signif in info["interpretation"].items():
                parler(f"Score {score} : {signif}")
        elif any(m in q for m in ["intervention", "que faire"]):
            parler_liste("Interventions selon le score de Glasgow :", info["interventions"])
        else:
            parler(info["court"])
            parler("Veux-tu les détails des yeux, de la réponse verbale, de la réponse motrice ou l'interprétation des scores?")

    # ── PLAIES ──
    elif sujet == "plaies":
        if any(m in q for m in ["type", "chronique", "aiguë"]):
            parler("Il y a deux types principaux de plaies.")
            for t, data in info["types"].items():
                parler(f"Plaie {t} : {data['def']} Exemples : {data['exemples']}")
        elif any(m in q for m in ["infection", "infectée", "signe"]):
            parler_liste("Signes d'infection d'une plaie :", info["signes_infection"])
        elif any(m in q for m in ["taim", "évaluer", "évaluation"]):
            parler("L'évaluation d'une plaie utilise le TAIM :")
            for lettre, detail in info["evaluation_plaie"].items():
                parler(f"{lettre} : {detail}")
        elif any(m in q for m in ["soin", "technique", "pansement", "comment faire"]):
            parler_liste("Technique de soin de plaie :", info["technique_soin"])
        elif any(m in q for m in ["stade", "pression"]):
            parler_liste("Stades des plaies de pression :", info["types"]["Pression"]["stades"])
        else:
            parler(info["court"])
            parler("Veux-tu les types de plaies, l'évaluation TAIM, les signes d'infection ou la technique de soin?")

    # ── DOULEUR ÉCHELLES ──
    elif sujet == "douleur_echelle":
        if any(m in q for m in ["numérique", "adulte", "0 à 10"]):
            e = info["echelles"]["Numérique"]
            parler(f"Échelle numérique : {e['pour']} Comment : {e['comment']} Interprétation : {e['interpretation']}")
        elif any(m in q for m in ["eva", "réglette", "visuelle"]):
            e = info["echelles"]["EVA"]
            parler(f"Échelle EVA : {e['pour']} Comment : {e['comment']}")
        elif any(m in q for m in ["wong", "baker", "visage", "enfant"]):
            e = info["echelles"]["Wong-Baker"]
            parler(f"Échelle Wong-Baker : {e['pour']} Comment : {e['comment']}")
        elif any(m in q for m in ["cpot", "intubé", "soins critiques"]):
            e = info["echelles"]["CPOT"]
            parler(f"Échelle CPOT : {e['pour']} Comment : {e['comment']} {e['interpretation']}")
        elif any(m in q for m in ["flacc", "bébé", "2 mois"]):
            e = info["echelles"]["FLACC"]
            parler(f"Échelle FLACC : {e['pour']} Comment : {e['comment']} {e['interpretation']}")
        elif any(m in q for m in ["principe", "règle", "important"]):
            parler_liste("Principes d'évaluation de la douleur :", info["principes"])
        else:
            parler(info["court"])
            parler("Veux-tu les détails sur une échelle en particulier? Numérique, EVA, Wong-Baker, CPOT ou FLACC?")

    # ── 5P ──
    elif sujet == "cinq_p":
        if any(m in q for m in ["pouls", "p1"]):
            parler(info["signes"]["P1"]["detail"])
        elif any(m in q for m in ["pâleur", "couleur", "trc", "p2"]):
            parler(info["signes"]["P2"]["detail"])
        elif any(m in q for m in ["paresthésie", "engourdissement", "picotement", "p3"]):
            parler(info["signes"]["P3"]["detail"])
        elif any(m in q for m in ["paralysie", "bouger", "motricité", "p4"]):
            parler(info["signes"]["P4"]["detail"])
        elif any(m in q for m in ["douleur", "pain", "p5"]):
            parler(info["signes"]["P5"]["detail"])
        elif any(m in q for m in ["alarme", "urgence", "danger", "syndrome"]):
            parler_liste("Signes d'alarme neurovasculaires :", info["signes_alarme"])
        elif any(m in q for m in ["fréquence", "quand", "combien de fois"]):
            parler_liste("Fréquence d'évaluation des 5P :", info["frequence"])
        else:
            parler(info["court"])
            parler("Veux-tu que j'explique chaque P en détail, les signes d'alarme ou la fréquence d'évaluation?")

    # ── FFE ──
    elif sujet == "ffe":
        if any(m in q for m in ["signe vital", "signes vitaux"]):
            parler_liste("Signes vitaux à documenter dans la FFE :", info["composantes"]["Signes_vitaux"])
        elif any(m in q for m in ["système", "évaluation", "composante"]):
            parler_liste("Systèmes à évaluer dans la FFE :", info["composantes"]["Evaluation_systemes"])
        elif any(m in q for m in ["conseil", "règle", "comment documenter", "erreur"]):
            parler_liste("Conseils pour bien remplir la FFE :", info["conseils"])
        elif any(m in q for m in ["risque", "morse", "braden"]):
            parler_liste("Évaluation des risques dans la FFE :", info["composantes"]["Risques"])
        else:
            parler(info["court"])
            parler("Veux-tu les signes vitaux, l'évaluation des systèmes, les risques ou les conseils de documentation?")

# ══════════════════════════════════════════════════════════════════════════════
#  ÉCOUTE ET BOUCLE PRINCIPALE
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

def main():
    print("=" * 60)
    print("  TonyPi - Module Évaluation SOIN 430 v1.0")
    print("  Morse | Glasgow | Plaies | Douleur | 5P | FFE")
    print("=" * 60)

    parler(
        "Bonjour! Je peux t'aider avec : "
        "l'échelle de Morse pour les chutes, "
        "l'échelle de Glasgow pour la conscience, "
        "les types de plaies et soins, "
        "les échelles de douleur Wong-Baker, EVA et numérique, "
        "les signes neurovasculaires 5P "
        "et la feuille de flot d'évaluation FFE. "
        "Pose-moi une question!"
    )

    while True:
        question = ecouter()
        if not question:
            parler("Je n'ai pas entendu. Tu peux répéter?")
            continue
        q = question.lower()
        if any(m in q for m in ["quitter", "stop", "au revoir"]):
            parler("Bonne chance! À bientôt!")
            break
        if any(m in q for m in ["aide", "liste", "que peux-tu"]):
            parler("Je couvre : Morse, Glasgow, plaies et soins, échelles de douleur, signes neurovasculaires 5P et FFE.")
            continue
        repondre_evaluation(question)

def mode_texte():
    print("=" * 60)
    print("  TonyPi Évaluation - Mode texte")
    print("  Exemples : 'Glasgow', 'échelle Morse', '5P', 'FFE'")
    print("  Tape 'quitter' pour sortir")
    print("=" * 60)
    while True:
        question = input("\nTa question: ").strip()
        if not question:
            continue
        if question.lower() in ["quitter", "exit"]:
            print("Au revoir!")
            break
        repondre_evaluation(question)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "texte":
        mode_texte()
    else:
        main()
