#!/usr/bin/env python3
"""
TonyPi - Module Soins d'urgence pédagogique v1.0
AVERTISSEMENT : Ce module est UNIQUEMENT à des fins pédagogiques
pour les étudiants en soins infirmiers SOIN 430.
Il ne remplace PAS un professionnel de santé.
"""

import pyttsx3
import speech_recognition as sr

# ══════════════════════════════════════════════════════════════════════════════
#  VOIX
# ══════════════════════════════════════════════════════════════════════════════
moteur = pyttsx3.init()
moteur.setProperty("rate", 145)
moteur.setProperty("volume", 1.0)

AVERTISSEMENT = (
    "ATTENTION : Je suis un outil pédagogique pour étudiants en soins infirmiers. "
    "Je ne remplace pas un médecin ou une infirmière. "
    "En cas d'urgence réelle, appelez le 911."
)

def parler(texte):
    print(f"\n[TonyPi] {texte}")
    moteur.say(texte)
    moteur.runAndWait()

# ══════════════════════════════════════════════════════════════════════════════
#  BASE DE CONNAISSANCES CLINIQUES
# ══════════════════════════════════════════════════════════════════════════════
SOINS = {

    # ── TENSION ARTÉRIELLE ────────────────────────────────────────────────
    "hypertension": {
        "definition" : "Tension artérielle supérieure à 140/90 mmHg.",
        "normal"     : "Normale acceptable : systolique entre 100 et 139 mmHg, diastolique entre 60 et 90 mmHg. Au-dessus de ces valeurs = hypertension.",
        "signes"     : "Maux de tête, vision floue, bourdonnements, rougeur du visage, parfois sans symptômes.",
        "interventions": [
            "Installer le patient en position semi-assise ou assise.",
            "Prendre la tension artérielle des deux bras.",
            "Demander si le patient a pris ses médicaments antihypertenseurs.",
            "Réduire les stimuli : bruit, lumière, stress.",
            "Aviser l'infirmière responsable ou le médecin si TA supérieure à 180/110.",
            "Ne jamais donner de médicament sans ordonnance.",
            "Documenter au dossier : heure, valeur, interventions."
        ],
        "medicaments": "Aucun médicament sans ordonnance. Le médecin peut prescrire : Amlodipine, Ramipril, Métoprolol selon le cas.",
        "escalade"   : "Appeler le médecin si TA dépasse 180/110 mmHg ou si le patient présente des symptômes neurologiques.",
        "urgence"    : "TA supérieure à 180/120 avec symptômes = urgence hypertensive. Appeler le 911 ou aviser immédiatement."
    },

    "hypotension": {
        "definition" : "Tension artérielle inférieure à 100/60 mmHg.",
        "normal"     : "Normale acceptable : systolique entre 100 et 139 mmHg, diastolique entre 60 et 90 mmHg. En dessous de ces valeurs = hypotension.",
        "signes"     : "Étourdissements, faiblesse, pâleur, syncope, pouls faible et rapide.",
        "interventions": [
            "Installer le patient en décubitus dorsal, jambes surélevées à 30 degrés.",
            "Prendre les signes vitaux complets.",
            "S'assurer que le patient est hydraté, offrir de l'eau si conscient et capable d'avaler.",
            "Ne pas laisser le patient debout, risque de chute.",
            "Aviser l'infirmière responsable immédiatement.",
            "Vérifier si le patient a pris des médicaments pouvant causer une hypotension.",
            "Documenter au dossier."
        ],
        "medicaments": "Aucun médicament sans ordonnance. Hydratation orale si possible. IV si prescrit.",
        "escalade"   : "Aviser immédiatement si TA inférieure à 80/50 ou si le patient est inconscient.",
        "urgence"    : "Perte de conscience ou choc = appeler le 911 immédiatement."
    },

    # ── FRÉQUENCE CARDIAQUE ───────────────────────────────────────────────
    "tachycardie": {
        "definition" : "Fréquence cardiaque supérieure à 100 battements par minute au repos.",
        "normal"     : (
            "Le pouls s'évalue avec le FAR : "
            "F = Fréquence : valeur normale entre 60 et 100 battements par minute. "
            "A = Amplitude : faible, normal ou bondissant. "
            "R = Rythme : Régulier ou Irrégulier. "
            "Tachycardie = F supérieure à 100 battements par minute."
        ),
        "signes"     : "F supérieure à 100, A pouvant être faible ou bondissante, R Régulier ou Irrégulier, palpitations, essoufflement, douleur thoracique, étourdissements.",
        "interventions": [
            "Évaluer le pouls selon FAR : Fréquence, Amplitude, Rythme Régulier ou Irrégulier.",
            "Installer le patient en position assise ou semi-assise.",
            "Prendre la tension artérielle.",
            "Faire un électrocardiogramme si disponible et prescrit.",
            "Demander au patient de respirer lentement et profondément.",
            "Identifier la cause possible : fièvre, déshydratation, douleur, anxiété, médicaments.",
            "Aviser l'infirmière responsable.",
            "Documenter selon FAR : Fréquence, Amplitude, Rythme Régulier ou Irrégulier, heure, symptômes."
        ],
        "medicaments": "Aucun médicament sans ordonnance. Le médecin peut prescrire : Métoprolol, Diltiazem selon la cause.",
        "escalade"   : "Aviser immédiatement si F supérieure à 150, R Irrégulier, A filante ou douleur thoracique présente.",
        "urgence"    : "Tachycardie avec instabilité hémodynamique = urgence. Appeler le 911."
    },

    "bradycardie": {
        "definition" : "Fréquence cardiaque inférieure à 60 battements par minute au repos.",
        "normal"     : (
            "Le pouls s'évalue avec le FAR : "
            "F = Fréquence : valeur normale entre 60 et 100 battements par minute. "
            "A = Amplitude : faible, normal ou bondissant. "
            "R = Rythme : Régulier ou Irrégulier. "
            "Bradycardie = F inférieure à 60 battements par minute."
        ),
        "signes"     : "F inférieure à 60, A souvent faible ou filante, R pouvant être Irrégulier, fatigue, étourdissements, syncope, essoufflement, confusion.",
        "interventions": [
            "Évaluer le pouls selon FAR : Fréquence, Amplitude, Rythme Régulier ou Irrégulier.",
            "Évaluer l'état de conscience du patient.",
            "Prendre les signes vitaux complets.",
            "Installer le patient en décubitus dorsal si étourdi.",
            "Vérifier les médicaments du patient : bêtabloquants, digoxine peuvent causer la bradycardie.",
            "Aviser l'infirmière responsable immédiatement.",
            "Préparer le matériel de réanimation si disponible.",
            "Documenter selon FAR : Fréquence, Amplitude, Rythme Régulier ou Irrégulier, heure, symptômes."
        ],
        "medicaments": "Aucun médicament sans ordonnance. En urgence, le médecin peut prescrire de l'Atropine IV.",
        "escalade"   : "Aviser immédiatement si F inférieure à 40, A filante, R Irrégulier ou patient symptomatique.",
        "urgence"    : "Bradycardie avec perte de conscience = appeler le 911 immédiatement."
    },

    # ── TEMPÉRATURE ───────────────────────────────────────────────────────
    "hyperthermie": {
        "definition" : "Température corporelle supérieure à 38,5 degrés Celsius. Aussi appelée fièvre ou état fébrile. Peut s'accompagner de diaphorèse (transpiration excessive) et d'hyperhidrose.",
        "normal"     : "Normale : 36,5 à 37,5 degrés Celsius. Fébricule : 37,6 à 38,4. Fièvre : 38,5 et plus.",
        "signes"     : "Température élevée, diaphorèse (sudation excessive), hyperhidrose, peau chaude et rouge, frissons, tachycardie, tachypnée, maux de tête, confusion, lèvres sèches, linges mouillés.",
        "interventions": [
            "Prendre la température avec thermomètre approprié et noter la valeur.",
            "Découvrir le patient : retirer les couvertures excédentaires et les vêtements chauds.",
            "Changer les linges et jaquette mouillés par la diaphorèse pour assurer le confort.",
            "Hydrater le patient : offrir de l'eau fraîche à boire régulièrement si conscient et capable d'avaler.",
            "Appliquer un petit sac de glace enveloppé dans un linge sur le front ou les aisselles.",
            "Donner une douche tiède ou appliquer des compresses tièdes sur le front, le cou et les aisselles. Pas d'eau froide car risque de frissons.",
            "Connecter un ventilateur à basse intensité pour favoriser l'évaporation et le refroidissement.",
            "Aérer la chambre et réduire la température ambiante si possible.",
            "Aviser l'infirmière responsable.",
            "Administrer l'antipyrétique prescrit si ordonnance disponible.",
            "Réévaluer la température 30 à 60 minutes après les interventions.",
            "Documenter : température avant et après, heure, interventions effectuées, résultat."
        ],
        "medicaments": (
            "Acétaminophène (Tylenol) : 325 à 650 mg par voie orale toutes les 4 à 6 heures. "
            "Maximum 3000 mg par 24 heures chez l'adulte. "
            "Ne pas dépasser la dose prescrite. Ne pas utiliser si insuffisance hépatique. "
            "Ibuprofène si prescrit : 200 à 400 mg toutes les 6 à 8 heures avec nourriture. "
            "TOUJOURS vérifier les allergies et les contre-indications avant d'administrer."
        ),
        "escalade"   : "Aviser le médecin si température dépasse 39,5 malgré les interventions, si confusion présente ou si patient ne tolère pas les liquides.",
        "urgence"    : "Température supérieure à 41 degrés ou coup de chaleur avec confusion = urgence. Appeler le 911."
    },

    "hypothermie": {
        "definition" : "Température corporelle inférieure à 35 degrés Celsius. Le corps perd plus de chaleur qu'il n'en produit.",
        "normal"     : "Normale : 36,5 à 37,5 degrés Celsius. Hypothermie légère : 32 à 35 degrés. Hypothermie sévère : moins de 32 degrés.",
        "signes"     : "Frissons intenses (signe protecteur du corps), peau froide et pâle, pouls FAR lent et faible, respiration MARSF lente, confusion, somnolence, lèvres et ongles bleutés.",
        "interventions": [
            "Retirer les vêtements mouillés et froids immédiatement.",
            "Amener le patient dans un endroit chaud et sec.",
            "Couvrir le patient avec des couvertures chaudes en commençant par le tronc, pas les membres.",
            "Ne pas frictionner ni masser les membres : risque de choc circulatoire.",
            "Offrir des boissons chaudes non alcoolisées si le patient est conscient et peut avaler.",
            "Appliquer des sacs de chaleur enveloppés dans un linge sur les aisselles et l'aine.",
            "Prendre les signes vitaux avec précaution selon FAR et MARSF.",
            "Aviser l'infirmière responsable immédiatement.",
            "Documenter : température, heure, interventions effectuées, résultat."
        ],
        "medicaments": "Pas de médicaments en première ligne. Réchauffement progressif prioritaire. Soluté chaud intraveineux si prescrit.",
        "escalade"   : "Aviser immédiatement si température inférieure à 32 degrés, si patient confus ou inconscient.",
        "urgence"    : "Température inférieure à 30 degrés ou arrêt cardiaque = RCR et appeler le 911 immédiatement."
    },

    # ── FRÉQUENCE RESPIRATOIRE ────────────────────────────────────────────
    "tachypnee": {
        "definition" : "Fréquence respiratoire supérieure à 20 respirations par minute au repos.",
        "normal"     : (
            "La respiration s'évalue avec le MARSF : "
            "M = Mécanique : effort respiratoire, présence de tirage, utilisation des muscles accessoires. "
            "A = Amplitude : superficielle, normale ou profonde. "
            "R = Rythme : Régulier ou Irrégulier. "
            "S = Symétrie : les deux côtés du thorax se soulèvent-ils de façon égale. "
            "F = Fréquence : valeur normale entre 12 et 20 respirations par minute. "
            "Tachypnée = F supérieure à 20 par minute."
        ),
        "signes"     : "F élevée, A superficielle, R pouvant être irrégulier, asymétrie possible, tirage intercostal, anxiété, cyanose possible.",
        "interventions": [
            "Évaluer la respiration selon MARSF : Mécanique, Amplitude, Rythme Régulier ou Irrégulier, Symétrie, Fréquence.",
            "Installer le patient en position semi-assise ou assise pour faciliter la respiration.",
            "Desserrer les vêtements serrés.",
            "Administrer de l'oxygène si prescrit et si saturation inférieure à 94 pourcent.",
            "Demander au patient de respirer lentement et profondément par le nez.",
            "Identifier la cause : douleur, anxiété, fièvre, infection.",
            "Mesurer la saturation en oxygène avec le saturomètre.",
            "Aviser l'infirmière responsable.",
            "Documenter selon MARSF : préciser Mécanique, Amplitude, Rythme Régulier ou Irrégulier, Symétrie et Fréquence."
        ],
        "medicaments": "Aucun médicament sans ordonnance. Oxygène si prescrit. Bronchodilatateur si prescrit.",
        "escalade"   : "Aviser immédiatement si F supérieure à 30, A très superficielle, R très irrégulier ou saturation inférieure à 90 pourcent.",
        "urgence"    : "Détresse respiratoire sévère, asymétrie marquée ou cyanose = appeler le 911 immédiatement."
    },

    "bradypnee": {
        "definition" : "Fréquence respiratoire inférieure à 12 respirations par minute au repos.",
        "normal"     : (
            "La respiration s'évalue avec le MARSF : "
            "M = Mécanique : effort respiratoire, présence de tirage, utilisation des muscles accessoires. "
            "A = Amplitude : superficielle, normale ou profonde. "
            "R = Rythme : Régulier ou Irrégulier. "
            "S = Symétrie : les deux côtés du thorax se soulèvent-ils de façon égale. "
            "F = Fréquence : valeur normale entre 12 et 20 respirations par minute. "
            "Bradypnée = F inférieure à 12 par minute."
        ),
        "signes"     : "F basse, A souvent faible, R pouvant être irrégulier, somnolence excessive, confusion, cyanose possible.",
        "interventions": [
            "Évaluer la respiration selon MARSF : Mécanique, Amplitude, Rythme Régulier ou Irrégulier, Symétrie, Fréquence.",
            "Évaluer l'état de conscience du patient immédiatement.",
            "Stimuler le patient verbalement et physiquement.",
            "Installer le patient en position latérale de sécurité si inconscient.",
            "Administrer de l'oxygène si prescrit.",
            "Vérifier les médicaments : opioïdes et benzodiazépines peuvent causer la bradypnée.",
            "Aviser l'infirmière responsable immédiatement.",
            "Préparer le matériel de réanimation.",
            "Documenter selon MARSF : préciser Mécanique, Amplitude, Rythme Régulier ou Irrégulier, Symétrie et Fréquence."
        ],
        "medicaments": "Aucun médicament sans ordonnance. Naloxone si surdose d'opioïdes suspectée et prescrite.",
        "escalade"   : "Aviser immédiatement si F inférieure à 8, A très faible, R très irrégulier ou patient somnolent.",
        "urgence"    : "Apnée ou arrêt respiratoire = RCR et appeler le 911 immédiatement."
    },

    # ── DOULEUR ET ANALGÉSIQUES ───────────────────────────────────────────
    "douleur": {
        "definition" : "La douleur est le 5e signe vital. Elle doit être évaluée systématiquement.",
        "normal"     : "Échelle de douleur : 0 = aucune douleur. 10 = douleur insupportable.",
        "signes"     : "Grimaces, pleurs, agitation, position antalgique, tachycardie, hypertension.",
        "interventions": [
            "Évaluer la douleur avec l'échelle numérique de 0 à 10.",
            "Demander : localisation, type, intensité, durée, facteurs aggravants et soulageants.",
            "Installer le patient en position confortable.",
            "Appliquer de la chaleur ou du froid selon la cause et la prescription.",
            "Offrir des techniques non pharmacologiques : respiration, distraction, relaxation.",
            "Administrer l'analgésique prescrit selon l'ordonnance.",
            "Réévaluer la douleur 30 minutes après l'intervention.",
            "Documenter : intensité avant et après, interventions, résultat."
        ],
        "medicaments": (
            "Acétaminophène (Tylenol) : "
            "Adulte : 325 à 1000 mg par voie orale toutes les 4 à 6 heures. "
            "Maximum 3000 mg par 24 heures chez l'adulte en général, 4000 mg si prescrit par médecin. "
            "Ne pas utiliser si insuffisance hépatique. "
            "\n"
            "Aspirine (AAS) : "
            "Adulte : 325 à 650 mg par voie orale toutes les 4 à 6 heures. "
            "Prendre avec nourriture. "
            "Contre-indications : enfants de moins de 18 ans (risque de syndrome de Reye), "
            "allergie aux AINS, ulcère gastrique, trouble de coagulation, grossesse. "
            "\n"
            "Ibuprofène (Advil, Motrin) : "
            "Adulte : 200 à 400 mg toutes les 6 à 8 heures avec nourriture. "
            "Maximum 1200 mg par 24 heures sans ordonnance. "
            "\n"
            "IMPORTANT : Toujours vérifier les allergies, les contre-indications "
            "et l'ordonnance avant d'administrer tout médicament."
        ),
        "escalade"   : "Aviser le médecin si la douleur est supérieure à 7 sur 10 ou résiste aux analgésiques.",
        "urgence"    : "Douleur thoracique soudaine et intense, douleur abdominale sévère = appeler le 911."
    },

    # ── SATURATION EN OXYGÈNE ─────────────────────────────────────────────
    "saturation": {
        "definition" : "La saturation en oxygène (SpO2) mesure le pourcentage d'hémoglobine liée à l'oxygène.",
        "normal"     : "Normale : 95 à 100 pourcent. En dessous de 90 pourcent = hypoxémie.",
        "signes"     : "Cyanose des lèvres et des ongles, confusion, agitation, dyspnée.",
        "interventions": [
            "Mesurer la SpO2 avec le saturomètre au doigt.",
            "S'assurer que le saturomètre est bien positionné.",
            "Installer le patient en position semi-assise.",
            "Administrer de l'oxygène si prescrit.",
            "Aviser l'infirmière responsable si SpO2 inférieure à 94 pourcent.",
            "Documenter : valeur, heure, interventions."
        ],
        "medicaments": "Oxygène thérapeutique si prescrit. Débit selon ordonnance médicale.",
        "escalade"   : "Aviser immédiatement si SpO2 inférieure à 90 pourcent malgré l'oxygène.",
        "urgence"    : "SpO2 inférieure à 85 pourcent ou cyanose = urgence. Appeler le 911."
    },

    # ── GLYCÉMIE ──────────────────────────────────────────────────────────
    "glycemie": {
        "definition" : "La glycémie est le taux de sucre dans le sang.",
        "normal"     : "Normale à jeun : 4 à 7 mmol/L. Après repas : moins de 10 mmol/L.",
        "signes"     : (
            "Hypoglycémie (trop bas) : tremblements, sueurs, confusion, pâleur, palpitations. "
            "Hyperglycémie (trop élevé) : soif intense, urines fréquentes, fatigue, vision floue."
        ),
        "interventions": [
            "Mesurer la glycémie avec le glucomètre selon la procédure.",
            "Si hypoglycémie inférieure à 4 : donner 15g de glucides rapides si patient conscient.",
            "Exemples : 125 ml de jus, 3 à 4 comprimés de glucose, 3 sachets de sucre.",
            "Réévaluer la glycémie après 15 minutes.",
            "Si hyperglycémie supérieure à 15 : aviser l'infirmière responsable.",
            "Ne jamais laisser un patient hypoglycémique seul.",
            "Documenter : valeur, heure, interventions, résultat."
        ],
        "medicaments": "Glucides rapides si hypoglycémie. Insuline si prescrite pour hyperglycémie. Toujours selon ordonnance.",
        "escalade"   : "Aviser immédiatement si glycémie inférieure à 2,8 ou supérieure à 20 mmol/L.",
        "urgence"    : "Hypoglycémie avec perte de conscience = appeler le 911. Glucagon si disponible et prescrit."
    },

    # ── CONSCIENCE / NEUROLOGIE ───────────────────────────────────────────
    "conscience": {
        "definition" : "L'état de conscience s'évalue avec l'échelle de Glasgow (GCS) de 3 à 15.",
        "normal"     : "Glasgow normal : 15. Coma : moins de 8.",
        "signes"     : "Confusion, désorientation, agitation, somnolence, réponse inadéquate aux stimuli.",
        "interventions": [
            "Évaluer avec le AVPU : Alerte, Voix, Douleur, Inconscient.",
            "Appeler le patient par son nom, lui parler clairement.",
            "Prendre les signes vitaux complets.",
            "Vérifier la glycémie.",
            "Ne pas laisser le patient seul.",
            "Mettre les ridelles du lit en place.",
            "Aviser l'infirmière responsable immédiatement.",
            "Documenter : niveau de conscience, heure, interventions."
        ],
        "medicaments": "Aucun médicament sans ordonnance. Dextrose IV si hypoglycémie et prescrit.",
        "escalade"   : "Aviser immédiatement tout changement brusque de l'état de conscience.",
        "urgence"    : "Inconscience = position latérale de sécurité et appeler le 911 immédiatement."
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  5 PARAMÈTRES VITAUX — TABLEAU OFFICIEL SOIN 430 (Potter 5e édition)
# ══════════════════════════════════════════════════════════════════════════════
PARAMETRES_VITAUX = {
    "temperature": {
        "titre"   : "Température (T°)",
        "normale" : "Écart normal : 36,0 à 37,9 °C",
        "voies"   : (
            "Valeurs selon la voie de mesure : "
            "Buccale (B) : 37,1 °C. "
            "Rectale (R) : 37,5 °C — la plus précise. "
            "Axillaire (A) : 36,5 °C — la moins précise. "
            "Tympanique (Ty) : 37,0 °C."
        ),
        "anormal_bas"  : "< 35 °C = Hypothermie",
        "anormal_haut" : "> 38 °C = Hyperthermie. Fièvre si T° buccale ou rectale > 37,8 °C.",
        "geronto"      : "Fièvre gériatrique si T°B ou R > 37,8 °C — suggère une infection.",
        "facteurs"     : "Âge, exercice physique, variation hormonale (ménopause), rythme circadien, environnement, stress.",
    },
    "pouls": {
        "titre"   : "Pouls (P) — s'évalue avec le FAR",
        "normale" : "60 à 100 battements par minute.",
        "far"     : (
            "FAR : "
            "F = Fréquence : nombre de battements par minute, normale 60 à 100. "
            "A = Amplitude : bien frappé, absent, filant, bondissant, faible. "
            "R = Rythme : Régulier, Irrégulier ou Arythmie. "
            "Si arythmie : prendre le pouls apical."
        ),
        "anormal_bas"  : "< 60 batt/min = Bradycardie",
        "anormal_haut" : "> 100 batt/min = Tachycardie",
        "signes"       : "Palpitations, perte de conscience, étourdissements.",
        "facteurs"     : "Exercice, température, émotions, hémorragie, changement de position, troubles respiratoires, médicaments.",
    },
    "respiration": {
        "titre"   : "Respiration (R) — s'évalue avec le MARSF",
        "normale" : "12 à 20 respirations par minute.",
        "marsf"   : (
            "MARSF : "
            "M = Mécanique : effort respiratoire, tirage, muscles accessoires. "
            "A = Amplitude : normale, superficielle ou profonde. "
            "R = Rythme : Régulier ou Irrégulier. "
            "S = Symétrie : les deux côtés du thorax se soulèvent également. "
            "F = Fréquence : 12 à 20 respirations par minute. "
            "Mode : libre par le nez ou la bouche. "
            "Son : murmure vésiculaire, sibilances. "
            "Mouvement : thoracique ou abdominal."
        ),
        "anormal_bas"  : "< 12 R/min = Bradypnée",
        "anormal_haut" : "> 20 à 24 R/min = Tachypnée",
        "terminologie" : "Eupnée, apnée, dyspnée, orthopnée, Cheyne-Stokes, Kussmaul.",
        "facteurs"     : "Exercice, douleur aiguë, anxiété, tabagisme, médicaments, blessures neurologiques, fonction hématologique, MPOC.",
    },
    "pression_arterielle": {
        "titre"   : "Pression artérielle (PA)",
        "normale" : "Systolique (PAS) : 100 à 139 mmHg. Diastolique (PAD) : 60 à 90 mmHg.",
        "anormal_bas"  : "Hypotension : PAS < 100 mmHg ou PAD < 60 mmHg — rend symptomatique.",
        "anormal_haut" : "Hypertension : PAS > 139 mmHg ou PAD > 90 mmHg.",
        "signes_hypo"  : "Pâleur, étourdissements, FC élevée, moiteur, confusion.",
        "signes_hyper" : "Généralement asymptomatique. Signes : tumeur silencieux, risque AVC.",
        "geronto"      : "Personnes âgées : choisir un brassard de plus petite taille, changement de position en douceur, éviter HTO (hypotension orthostatique).",
        "facteurs"     : "Âge, stress et émotions, douleur, tabagisme, variation hormonale, diurèse, médicaments, exercice physique, origine ethnique, obésité.",
    },
    "saturometrie": {
        "titre"   : "Saturométrie (SpO2)",
        "normale" : "95 % à 100 %.",
        "anormal" : "< 95 % = anormal. MPOC ou BPCO : < 88 % = critique.",
        "interventions": (
            "Si SpO2 normale : 95 à 100 % — surveiller. "
            "Si MPOC/BPCO et SpO2 < 88 % : supplément d'oxygène à long terme, améliore la saturométrie et la condition. "
            "Administrer l'oxygène via lunette nasale ou petit débit si prescrit. "
            "Intervention infirmière : RESPIRATION selon MARSF."
        ),
        "signes"  : "Cyanose (lèvres, extrémités), peau froide, confusion.",
        "facteurs": "MPOC, BPCO, anémie, altitude, tabagisme.",
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  MALADIES INFECTIEUSES — SOIN 430
# ══════════════════════════════════════════════════════════════════════════════
MALADIES_INFECTIEUSES = {
    "sarm": {
        "nom_complet"  : "SARM = Staphylocoque aureus résistant à la méthicilline (Bactérie)",
        "reservoir"    : "Plaie",
        "porte_sortie" : "Écoulement de la plaie",
        "transmission" : "Contact direct et indirect",
        "porte_entree" : "Nez, bouche, plaie",
        "facteurs_risque": "Anti-inflammatoires, corticostéroïdes, diabète",
        "precautions"  : "Précautions de contact. Port de gants et blouse obligatoire. Hygiène des mains renforcée.",
    },
    "erv": {
        "nom_complet"  : "ERV = Entérocoque résistant à la vancomycine (Bactérie)",
        "reservoir"    : "Système urinaire ou digestif",
        "porte_sortie" : "Urine ou selles",
        "transmission" : "Contact direct et indirect",
        "porte_entree" : "Bouche, urètre, méat urinaire",
        "facteurs_risque": "Diabète, antibiothérapie prolongée",
        "precautions"  : "Précautions de contact. Chambre individuelle si possible. Gants et blouse obligatoires.",
    },
    "bgnmr": {
        "nom_complet"  : "BGNMR = Bacilles gram négatif multirésistant (Bactérie)",
        "reservoir"    : "Système digestif",
        "porte_sortie" : "Selles",
        "transmission" : "Contact direct et indirect, gouttelettes",
        "porte_entree" : "Bouche, anus",
        "facteurs_risque": "Hospitalisation dans les 12 derniers mois",
        "precautions"  : "Précautions de contact. Gants et blouse. Hygiène des mains stricte.",
    },
    "c_difficile": {
        "nom_complet"  : "C. difficile = Clostridium difficile (Bactérie)",
        "reservoir"    : "Système digestif",
        "porte_sortie" : "Selles, vomissements",
        "transmission" : "Contact direct et indirect, gouttelettes",
        "porte_entree" : "Bouche, anus",
        "facteurs_risque": "Antibiotiques (déstabilise la flore intestinale), hospitalisation",
        "precautions"  : "Précautions de contact. Lavage des mains au savon obligatoire — le gel hydroalcoolique ne détruit PAS les spores de C. difficile.",
    },
    "tuberculose": {
        "nom_complet"  : "Tuberculose (Bactérie)",
        "reservoir"    : "Système respiratoire",
        "porte_sortie" : "Expectorations, toux",
        "transmission" : "Aérien, indirect",
        "porte_entree" : "Nez, bouche",
        "facteurs_risque": "MPOC, immunosuppression",
        "precautions"  : "Précautions aériennes. Chambre à pression négative. Masque N95 obligatoire.",
    },
    "influenza": {
        "nom_complet"  : "Influenza H1N1 (Virus)",
        "reservoir"    : "Système respiratoire",
        "porte_sortie" : "Écoulement nasal, toux, expectoration",
        "transmission" : "Contact direct et indirect, gouttelettes",
        "porte_entree" : "Nez, bouche, anus",
        "facteurs_risque": "Stress, absence de vaccination",
        "precautions"  : "Précautions gouttelettes. Masque chirurgical. Hygiène des mains.",
    },
    "covid": {
        "nom_complet"  : "COVID-19 (Virus)",
        "reservoir"    : "Système respiratoire",
        "porte_sortie" : "Écoulement nasal, toux, expectoration",
        "transmission" : "Contact direct et indirect, gouttelettes, aérien (si intubation)",
        "porte_entree" : "Nez, bouche, nez-bouche",
        "facteurs_risque": "Antinéoplasique (médicament), immunosuppression, âge avancé",
        "precautions"  : "Précautions gouttelettes et contact. Masque N95 si aérosolisation. EPI complet.",
    },
    "gastro": {
        "nom_complet"  : "Gastro-Entérite (Bactérie/Virus)",
        "reservoir"    : "Système digestif",
        "porte_sortie" : "Selles, vomissements",
        "transmission" : "Contact direct et indirect, gouttelettes",
        "porte_entree" : "Bouche, anus",
        "facteurs_risque": "Enfants, milieux collectifs",
        "precautions"  : "Précautions de contact. Gants et blouse. Hygiène des mains stricte.",
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  FACTEURS DE RISQUE — SYSTÈME IMMUNITAIRE
# ══════════════════════════════════════════════════════════════════════════════
FACTEURS_RISQUE = {
    "age": {
        "nouveau_ne" : "Le système immunitaire du nouveau-né est immature.",
        "enfant"     : "Le système immunitaire gagne en maturité mais reste fragile. Susceptible aux infections sans vaccination (oreillons, varicelle).",
        "adulte"     : "Le système immunitaire est mature. Cette tranche d'âge est bien protégée.",
        "personne_agee": "Le déclin de la fonction immunitaire augmente la susceptibilité. Les lymphocytes sont en quantité moindre et leur réponse est plus courte. Affaiblissement des globules blancs.",
    },
    "etat_nutritionnel": "La réduction de l'apport protéique diminue les défenses de l'organisme contre les infections et ralentit la cicatrisation. Les globules blancs sont des soldats — il faut les augmenter par une bonne nutrition.",
    "traitements_medicaux": {
        "anti_inflammatoires": "Diminution de la réponse inflammatoire contre les bactéries et agents pathogènes.",
        "antineoplasiques"   : "Attaque les cellules cancéreuses mais entraîne des effets secondaires : la moelle osseuse devient incapable de produire suffisamment de lymphocytes ou de globules blancs.",
        "immunosuppresseurs" : "Diminution de la réponse du système immunitaire.",
        "antibiotiques"      : "Déstabilise la flore intestinale — risque de C. difficile.",
    },
    "maladies": {
        "lymphome_leucemie_vih": "Diminution ou destruction des globules blancs.",
        "diabete_sclerose"     : "Faiblesse généralisée et insuffisance nutritionnelle.",
        "mpoc"                 : "Nuit à l'action des cils vibratiles et épaissit le mucus.",
        "maladies_vasculaires" : "Réduisent l'afflux sanguin aux tissus lésés — diminution de l'apport nutritionnel.",
        "brulures_graves"      : "Altération des tissus cutanés.",
    },
    "stress": "L'organisme répond au stress physique et psychologique par le syndrome d'adaptation. Cela diminue la réponse inflammatoire par la libération de cortisone.",
}

# ══════════════════════════════════════════════════════════════════════════════
#  CHAÎNE DE TRANSMISSION (IMAGE 1)
# ══════════════════════════════════════════════════════════════════════════════
CHAINE_TRANSMISSION = {
    "definition": "La chaîne de transmission comporte 6 maillons : Agent infectieux → Réservoir → Porte de sortie → Mode de transmission → Porte d'entrée → Hôte susceptible.",
    "agent_infectieux": "Micro-organisme causant l'infection : bactérie, virus, champignon, parasite.",
    "reservoir"       : "Source de l'agent : humain, animal, environnement (eau, sol).",
    "porte_sortie"    : "Urine, selles, sang, salive, expectorations, sécrétions vaginales, pus, écoulement de plaie.",
    "transmission"    : "Contact direct, contact indirect, gouttelettes, aérien.",
    "porte_entree"    : "Nez, bouche, yeux, plaie, méat urinaire, anus.",
    "hote"            : "Contenant : l'eau, les animaux et l'humain. Spécifiquement un système : respiratoire, digestif.",
    "prevention"      : "Briser la chaîne : lavage des mains, EPI (gants, masque, lunettes, blouse), précautions de contact, aériennes ou gouttelettes.",
}

# ══════════════════════════════════════════════════════════════════════════════
#  MÉTHODES D'ÉVALUATION CLINIQUE
# ══════════════════════════════════════════════════════════════════════════════
EVALUATION_CLINIQUE = {
    "methodes": (
        "4 méthodes d'évaluation clinique : "
        "1. Inspection : observation visuelle du patient. "
        "2. Auscultation : écouter les sons produits par les organes internes du corps, "
        "tels que le cœur, les poumons ou l'abdomen, avec un stéthoscope. "
        "3. Percussion : tapoter sur une partie du corps doucement, "
        "exemple thorax et abdomen. "
        "4. Palpation : ressentir le battement du cœur, comme le pouls radial."
    ),
    "donnees": (
        "Données objectives : vérifiables, observables, mesurables. "
        "Données subjectives : ce que le patient ressent, son opinion personnelle, ce qu'il dit."
    ),
    "signes_vitaux": "Les 5 signes vitaux sont : Température, Pouls (FAR), Respiration (MARSF), Pression artérielle, Saturométrie (SpO2). Notés sur la feuille graphique.",
}

# ══════════════════════════════════════════════════════════════════════════════
#  MOTS-CLÉS DE DÉTECTION
# ══════════════════════════════════════════════════════════════════════════════
MOTS_CLES = {
    # Signes vitaux
    "hypertension" : ["hypertension", "tension élevée", "pression haute", "ta élevée", "tension trop haute"],
    "hypotension"  : ["hypotension", "tension basse", "pression basse", "ta basse", "tension trop basse"],
    "tachycardie"  : ["tachycardie", "pouls rapide", "cœur rapide", "palpitation", "fc élevée", "battements rapides"],
    "bradycardie"  : ["bradycardie", "pouls lent", "cœur lent", "fc basse", "battements lents"],
    "hyperthermie" : ["hyperthermie", "fièvre", "température élevée", "chaud", "brûlant", "chaleur", "fébrile", "diaphorèse"],
    "hypothermie"  : ["hypothermie", "température basse", "froid", "gelé", "frissons"],
    "tachypnee"    : ["tachypnée", "respiration rapide", "essoufflement", "dyspnée", "souffle court"],
    "bradypnee"    : ["bradypnée", "respiration lente", "apnée", "respire peu", "respiration faible"],
    "douleur"      : ["douleur", "mal", "souffre", "tylenol", "aspirine", "ibuprofène", "analgésique", "opioïde", "antidouleur"],
    "saturation"   : ["saturation", "spo2", "oxygène", "oxymètre", "cyanose", "bleu"],
    "glycemie"     : ["glycémie", "sucre", "glucose", "hypoglycémie", "hyperglycémie", "diabète", "insuline"],
    "conscience"   : ["conscience", "inconscient", "confusion", "glasgow", "coma", "répond pas", "somnolent"],
    # Maladies infectieuses
    "sarm"         : ["sarm", "staphylocoque", "méthicilline"],
    "erv"          : ["erv", "entérocoque", "vancomycine"],
    "bgnmr"        : ["bgnmr", "bacilles gram", "multirésistant"],
    "c_difficile"  : ["c difficile", "clostridium", "c.difficile"],
    "tuberculose"  : ["tuberculose", "tb", "bacille de koch"],
    "influenza"    : ["influenza", "h1n1", "grippe"],
    "covid"        : ["covid", "coronavirus", "covid-19"],
    "gastro"       : ["gastro", "gastro-entérite", "vomissements infectieux"],
    # Évaluation
    "parametres"   : ["paramètres vitaux", "5 paramètres", "signes vitaux", "tableau paramètres"],
    "far"          : ["far", "pouls far", "évaluer pouls", "comment évaluer pouls"],
    "marsf"        : ["marsf", "évaluer respiration", "comment évaluer respiration"],
    "transmission" : ["chaîne de transmission", "transmission infection", "comment se transmet"],
    "facteurs"     : ["facteurs de risque", "facteur immunitaire", "système immunitaire"],
    "evaluation"   : ["évaluation clinique", "méthodes évaluation", "inspection", "auscultation", "percussion", "palpation"],
}

# ══════════════════════════════════════════════════════════════════════════════
#  DÉTECTION ET RÉPONSE
# ══════════════════════════════════════════════════════════════════════════════
def detecter_condition(question):
    q = question.lower()
    for condition, mots in MOTS_CLES.items():
        for mot in mots:
            if mot in q:
                return condition
    return None

def demande_detail(question):
    mots = ["intervention", "que faire", "quoi faire", "médicament", "traitement",
            "urgence", "escalade", "appeler", "signes", "symptôme", "définition", "normal"]
    return any(m in question.lower() for m in mots)

def repondre_soin(question, nom="Étudiant"):
    condition = detecter_condition(question)

    if not condition:
        parler("Je n'ai pas reconnu la condition. Peux-tu reformuler? Par exemple : tachycardie, fièvre, SARM, FAR, MARSF, facteurs de risque.")
        return

    q = question.lower()

    # ── Maladies infectieuses ──────────────────────────────────────────────
    if condition in ["sarm","erv","bgnmr","c_difficile","tuberculose","influenza","covid","gastro"]:
        m = MALADIES_INFECTIEUSES[condition]
        parler(m["nom_complet"])
        parler(f"Réservoir : {m['reservoir']}. Porte de sortie : {m['porte_sortie']}.")
        parler(f"Transmission : {m['transmission']}. Porte d'entrée : {m['porte_entree']}.")
        parler(f"Facteurs de risque : {m['facteurs_risque']}.")
        parler(f"Précautions : {m['precautions']}")
        return

    # ── Paramètres vitaux ──────────────────────────────────────────────────
    if condition == "parametres":
        parler("Les 5 paramètres vitaux selon Potter 5e édition : Température, Pouls évalué avec le FAR, Respiration évaluée avec le MARSF, Pression artérielle, et Saturométrie SpO2.")
        return

    if condition == "far":
        p = PARAMETRES_VITAUX["pouls"]
        parler(p["far"])
        parler(f"Valeur normale : {p['normale']}")
        parler(f"Anormal bas : {p['anormal_bas']}. Anormal haut : {p['anormal_haut']}.")
        return

    if condition == "marsf":
        r = PARAMETRES_VITAUX["respiration"]
        parler(r["marsf"])
        parler(f"Valeur normale : {r['normale']}")
        parler(f"Terminologie : {r['terminologie']}")
        return

    # ── Chaîne de transmission ─────────────────────────────────────────────
    if condition == "transmission":
        parler(CHAINE_TRANSMISSION["definition"])
        parler(f"Porte de sortie : {CHAINE_TRANSMISSION['porte_sortie']}")
        parler(f"Prévention : {CHAINE_TRANSMISSION['prevention']}")
        return

    # ── Facteurs de risque ─────────────────────────────────────────────────
    if condition == "facteurs":
        parler("Les facteurs de risque du système immunitaire :")
        parler(f"Âge — Personnes âgées : {FACTEURS_RISQUE['age']['personne_agee']}")
        parler(f"État nutritionnel : {FACTEURS_RISQUE['etat_nutritionnel']}")
        parler(f"Stress : {FACTEURS_RISQUE['stress']}")
        parler("Traitements : anti-inflammatoires, antinéoplasiques, immunosuppresseurs et antibiotiques affaiblissent le système immunitaire.")
        return

    # ── Méthodes d'évaluation clinique ────────────────────────────────────
    if condition == "evaluation":
        parler(EVALUATION_CLINIQUE["methodes"])
        parler(EVALUATION_CLINIQUE["donnees"])
        return

    # ── Signes vitaux classiques ───────────────────────────────────────────
    info = SOINS[condition]

    if any(m in q for m in ["définition", "c'est quoi", "qu'est-ce"]):
        parler(info["definition"])
        parler(f"Valeur normale : {info['normal']}")

    elif any(m in q for m in ["signe", "symptôme", "reconnaître", "identifier"]):
        parler(f"Signes et symptômes : {info['signes']}")

    elif any(m in q for m in ["médicament", "tylenol", "aspirine", "ibuprofène", "analgésique", "opioïde", "donner"]):
        parler("Voici les informations sur les médicaments.")
        parler(info["medicaments"])
        parler("Rappel : toujours vérifier l'ordonnance, les allergies et les contre-indications avant d'administrer.")

    elif any(m in q for m in ["urgence", "911", "grave", "critique"]):
        parler(f"Situation d'urgence : {info['urgence']}")

    elif any(m in q for m in ["escalade", "aviser", "appeler médecin", "quand appeler"]):
        parler(f"Critères d'escalade : {info['escalade']}")

    elif any(m in q for m in ["intervention", "que faire", "quoi faire", "comment", "traitement"]):
        parler("Voici les interventions infirmières.")
        for i, intervention in enumerate(info["interventions"], 1):
            parler(f"Étape {i} : {intervention}")
        parler("N'oublie pas de documenter toutes tes interventions au dossier.")

    else:
        parler(info["definition"])
        parler(f"Valeur normale : {info['normal']}")
        parler(f"Premiers signes : {info['signes']}")
        parler("Veux-tu les interventions, les médicaments ou les critères d'urgence?")

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
    print("  TonyPi - Module Soins cliniques pédagogique v1.0")
    print("  SOIN 430 | Cégep St-Jérôme")
    print("  USAGE PÉDAGOGIQUE UNIQUEMENT")
    print("=" * 60)

    parler(AVERTISSEMENT)
    parler(
        "Bonjour! Je peux t'aider à apprendre les interventions infirmières pour : "
        "l'hypertension, l'hypotension, la tachycardie, la bradycardie, "
        "la fièvre, l'hypothermie, la tachypnée, la bradypnée, "
        "la douleur, la saturation, la glycémie et l'état de conscience. "
        "Pose-moi une question!"
    )

    while True:
        question = ecouter()

        if not question:
            parler("Je n'ai pas entendu. Tu peux répéter?")
            continue

        q_lower = question.lower()

        if any(m in q_lower for m in ["quitter", "stop", "au revoir", "bye"]):
            parler("Bonne chance pour ton stage! À bientôt!")
            break

        if any(m in q_lower for m in ["aide", "que peux-tu", "quoi dire", "liste"]):
            parler(
                "Je peux répondre sur : hypertension, hypotension, tachycardie, bradycardie, "
                "hyperthermie, hypothermie, tachypnée, bradypnée, douleur et analgésiques, "
                "saturation en oxygène, glycémie, et état de conscience."
            )
            continue

        repondre_soin(question)

# ══════════════════════════════════════════════════════════════════════════════
#  MODE TEXTE — test sans micro
# ══════════════════════════════════════════════════════════════════════════════
def mode_texte():
    print("=" * 60)
    print("  TonyPi Soins - Mode texte")
    print("  Exemples : 'que faire tachycardie', 'médicament fièvre'")
    print("  Tape 'quitter' pour sortir | 'liste' pour les sujets")
    print("=" * 60)

    while True:
        question = input("\nTa question: ").strip()
        if not question:
            continue
        if question.lower() in ["quitter", "exit", "quit"]:
            print("Au revoir!")
            break
        if question.lower() == "liste":
            print("\nSujets disponibles:")
            for k in SOINS.keys():
                print(f"  - {k}")
            continue
        repondre_soin(question)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "texte":
        mode_texte()
    else:
        main()
