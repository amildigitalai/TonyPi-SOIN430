#!/usr/bin/env python3
"""
TonyPi - Système complet v2.0 VOSK OFFLINE
- Reconnaissance vocale Vosk (sans internet)
- Reconnaissance faciale + mémoire persistante
- Réponses OIIQ code de déontologie
- Compatible ReSpeaker 2-Mic HAT
"""

import face_recognition
import cv2
import json
import os
import pyttsx3
import numpy as np
from datetime import datetime

# Vosk offline
import vosk
import pyaudio
import queue

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
MEMOIRE_FILE = "memoire_etudiants.json"
VISAGES_DIR  = "visages/"
MODELE_VOSK  = "/home/pi/vosk-model-fr"
RATE         = 16000
CHUNK        = 8000

os.makedirs(VISAGES_DIR, exist_ok=True)

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
#  VOSK — RECONNAISSANCE VOCALE OFFLINE
# ══════════════════════════════════════════════════════════════════════════════
class VoskEcoute:
    def __init__(self):
        print("[Vosk] Chargement du modèle français...")
        self.modele     = vosk.Model(MODELE_VOSK)
        self.recognizer = vosk.KaldiRecognizer(self.modele, RATE)
        self.audio      = pyaudio.PyAudio()
        self.q          = queue.Queue()
        print("[Vosk] Prêt ✓")

    def _callback(self, in_data, frame_count, time_info, status):
        self.q.put(bytes(in_data))
        return (None, pyaudio.paContinue)

    def ecouter(self, timeout=8):
        """Écoute et retourne le texte reconnu ou None"""
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=self._callback
        )
        stream.start_stream()
        print("[Écoute] Parle maintenant...")

        import time
        texte_final = None
        debut = time.time()

        try:
            while time.time() - debut < timeout:
                try:
                    data = self.q.get(timeout=0.5)
                except queue.Empty:
                    continue
                if self.recognizer.AcceptWaveform(data):
                    res = json.loads(self.recognizer.Result())
                    texte = res.get("text", "").strip()
                    if texte:
                        print(f"[Étudiant] {texte}")
                        texte_final = texte
                        break
        finally:
            stream.stop_stream()
            stream.close()
            while not self.q.empty():
                self.q.get()

        return texte_final

    def fermer(self):
        self.audio.terminate()

# ══════════════════════════════════════════════════════════════════════════════
#  MÉMOIRE PERSISTANTE
# ══════════════════════════════════════════════════════════════════════════════
def charger_memoire():
    if os.path.exists(MEMOIRE_FILE):
        with open(MEMOIRE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def sauvegarder_memoire(memoire):
    with open(MEMOIRE_FILE, "w", encoding="utf-8") as f:
        json.dump(memoire, f, ensure_ascii=False, indent=2)

def mettre_a_jour_visite(memoire, nom):
    if nom in memoire:
        memoire[nom]["derniere_visite"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        memoire[nom]["nb_visites"] = memoire[nom].get("nb_visites", 0) + 1
        sauvegarder_memoire(memoire)

# ══════════════════════════════════════════════════════════════════════════════
#  RECONNAISSANCE FACIALE
# ══════════════════════════════════════════════════════════════════════════════
def encoder_visages_connus(memoire):
    noms, encodages = [], []
    for nom in memoire:
        chemin = os.path.join(VISAGES_DIR, f"{nom}.jpg")
        if os.path.exists(chemin):
            image = face_recognition.load_image_file(chemin)
            enc   = face_recognition.face_encodings(image)
            if enc:
                encodages.append(enc[0])
                noms.append(nom)
    return noms, encodages

def capturer_visage(nom, camera):
    parler(f"Regarde la caméra {nom}.")
    import time; time.sleep(1)
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(os.path.join(VISAGES_DIR, f"{nom}.jpg"), frame)
        return True
    return False

def identifier_visage(frame, noms_connus, encodages_connus):
    petit = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb   = cv2.cvtColor(petit, cv2.COLOR_BGR2RGB)
    positions = face_recognition.face_locations(rgb)
    encodages = face_recognition.face_encodings(rgb, positions)
    for enc in encodages:
        if not encodages_connus:
            return "inconnu"
        distances = face_recognition.face_distance(encodages_connus, enc)
        idx = np.argmin(distances)
        if distances[idx] < 0.5:
            return noms_connus[idx]
    return "inconnu" if positions else None

# ══════════════════════════════════════════════════════════════════════════════
#  ACCUEIL
# ══════════════════════════════════════════════════════════════════════════════
def accueillir_etudiant(nom, memoire):
    data    = memoire.get(nom, {})
    nb      = data.get("nb_visites", 1)
    erreurs = data.get("erreurs", [])
    if nb == 1:
        parler(f"Bonjour {nom}! Première visite. Je suis TonyPi ton assistant SOIN 430.")
    elif nb <= 3:
        parler(f"Bonjour {nom}! Content de te revoir. C'est ta {nb}ème visite.")
    else:
        parler(f"Bonjour {nom}! {nb} visites, tu es un habitué!")
    if erreurs:
        if len(erreurs) == 1:
            parler(f"La dernière fois tu avais de la difficulté avec {erreurs[0]}. On reprend?")
        else:
            liste = ", ".join(erreurs[:-1]) + f" et {erreurs[-1]}"
            parler(f"Tes points à retravailler : {liste}.")
    parler("Pose-moi une question!")

def accueillir_inconnu(memoire, camera, vosk_ecoute):
    parler("Bonjour! Je ne te connais pas encore. Comment tu t'appelles?")
    nom = vosk_ecoute.ecouter(timeout=6)
    if nom:
        nom = nom.strip().capitalize()
        parler(f"Enchanté {nom}!")
        memoire[nom] = {
            "nb_visites"     : 1,
            "erreurs"        : [],
            "derniere_visite": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "programme"      : "SOIN 430"
        }
        if capturer_visage(nom, camera):
            parler(f"Je vais me souvenir de toi {nom}.")
        sauvegarder_memoire(memoire)
        return nom
    parler("Je n'ai pas entendu. Je t'appelle Étudiant pour l'instant.")
    return "Étudiant"

# ══════════════════════════════════════════════════════════════════════════════
#  BASE OIIQ — CODE DE DÉONTOLOGIE
# ══════════════════════════════════════════════════════════════════════════════
OIIQ = {
    "secours"       : { "court": "L'infirmière doit porter secours à toute personne dont la vie est en péril, personnellement ou en obtenant de l'aide. Elle ne peut refuser sauf si cela représente un risque pour elle-même ou pour autrui.", "articles": ["1"] },
    "discrimination": { "court": "L'infirmière ne peut refuser de soigner quelqu'un en raison de sa race, couleur, sexe, religion, orientation sexuelle, langue, handicap ou condition sociale.", "articles": ["2"] },
    "dignite"       : { "court": "L'infirmière doit prendre tous les moyens nécessaires pour assurer le respect de la dignité, de la liberté et de l'intégrité du client en tout temps.", "articles": ["3.1", "29"] },
    "incident"      : { "court": "L'infirmière doit dénoncer tout incident ou accident résultant de son intervention. Elle ne doit pas tenter de le dissimuler.", "articles": ["12"] },
    "dossier"       : { "court": "L'infirmière ne peut falsifier, fabriquer ni inscrire de fausses informations dans un dossier client.", "articles": ["14"] },
    "competence"    : { "court": "L'infirmière doit agir avec compétence, tenir compte des limites de ses habiletés et assurer la mise à jour de ses compétences.", "articles": ["17", "18", "19"] },
    "alcool"        : { "court": "L'infirmière doit s'abstenir d'exercer lorsqu'elle est sous l'influence d'alcool, stupéfiants ou toute substance altérant ses facultés.", "articles": ["16"] },
    "conflit"       : { "court": "L'infirmière doit éviter toute situation de conflit d'intérêts. En cas de conflit, elle doit s'assurer que les soins soient prodigués par une autre personne.", "articles": ["23", "24"] },
    "secret"        : { "court": "L'infirmière doit préserver le secret professionnel de toutes les informations confidentielles obtenues dans l'exercice de sa profession.", "articles": ["31", "32", "33"] },
    "consentement"  : { "court": "L'infirmière doit obtenir le consentement libre et éclairé du client avant de prodiguer des soins. Le client peut retirer son consentement en tout temps.", "articles": ["40", "41"] },
    "violence"      : { "court": "L'infirmière ne doit jamais faire preuve de violence physique, verbale ou psychologique envers le client.", "articles": ["37", "48"] },
    "negligence"    : { "court": "L'infirmière ne doit pas faire preuve de négligence. Elle doit évaluer, intervenir promptement, surveiller et assurer la continuité des soins.", "articles": ["44"] },
    "honoraires"    : { "court": "L'infirmière doit demander des honoraires justes et raisonnables, proportionnés aux services rendus.", "articles": ["52", "53"] },
    "ordre"         : { "court": "L'infirmière doit collaborer avec l'OIIQ lors d'enquêtes ou d'inspections professionnelles.", "articles": ["49", "50"] },
}

MOTS_OIIQ = {
    "secours"       : ["secours", "urgence", "péril", "danger"],
    "discrimination": ["discrimination", "refuser", "race", "religion", "handicap"],
    "dignite"       : ["dignité", "liberté", "intégrité", "respect"],
    "incident"      : ["incident", "accident", "erreur", "dissimuler"],
    "dossier"       : ["dossier", "falsifier", "fausses informations", "notes"],
    "competence"    : ["compétence", "habiletés", "formation", "mise à jour"],
    "alcool"        : ["alcool", "drogue", "stupéfiant", "ivresse"],
    "conflit"       : ["conflit", "intérêt personnel", "ristourne"],
    "secret"        : ["secret", "confidentialité", "confidentiel", "divulguer"],
    "consentement"  : ["consentement", "éclairé", "libre"],
    "violence"      : ["violence", "abus", "maltraitance"],
    "negligence"    : ["négligence", "surveillance", "sécurité"],
    "honoraires"    : ["honoraires", "facturation", "frais"],
    "ordre"         : ["ordre", "oiiq", "syndic", "inspection"],
}

# ══════════════════════════════════════════════════════════════════════════════
#  BASE SOINS CLINIQUES
# ══════════════════════════════════════════════════════════════════════════════
SOINS_COURT = {
    "hypertension" : "Tension artérielle supérieure à 139 sur 90. Installer en position semi-assise, prendre la TA des deux bras, réduire les stimuli, aviser si supérieure à 180 sur 110.",
    "hypotension"  : "Tension artérielle inférieure à 100 sur 60. Installer en décubitus dorsal jambes surélevées, hydrater si conscient, ne pas laisser debout, aviser immédiatement.",
    "tachycardie"  : "Fréquence cardiaque supérieure à 100. Évaluer selon FAR : Fréquence, Amplitude, Rythme Régulier ou Irrégulier. Position assise, respiration lente, aviser si supérieure à 150.",
    "bradycardie"  : "Fréquence cardiaque inférieure à 60. Évaluer selon FAR. Décubitus dorsal, vérifier les médicaments, aviser immédiatement si inférieure à 40.",
    "hyperthermie" : "Température supérieure à 38,5 degrés. Découvrir, hydrater eau fraîche, sac de glace sur le front, changer les linges mouillés, ventilateur, douche tiède, Tylenol si prescrit.",
    "hypothermie"  : "Température inférieure à 35 degrés. Retirer vêtements mouillés, couvrir par le tronc, boissons chaudes si conscient, ne pas frictionner les membres.",
    "tachypnee"    : "Respiration supérieure à 20. Évaluer selon MARSF. Position semi-assise, respiration lente par le nez, oxygène si prescrit, aviser si supérieure à 30.",
    "bradypnee"    : "Respiration inférieure à 12. Évaluer selon MARSF. Stimuler le patient, position latérale si inconscient, oxygène si prescrit, aviser immédiatement.",
    "douleur"      : "5e signe vital. Évaluer selon PQRSTU, échelle 0 à 10. Position confortable, Tylenol 325 à 650mg si prescrit, réévaluer après 30 minutes.",
    "marsf"        : "MARSF évalue la respiration : M Mécanique, A Amplitude, R Rythme Régulier ou Irrégulier, S Symétrie, F Fréquence normale 12 à 20 par minute.",
    "far"          : "FAR évalue le pouls : F Fréquence normale 60 à 100, A Amplitude faible normal ou bondissant, R Rythme Régulier ou Irrégulier.",
}

MOTS_SOINS = {
    "hypertension" : ["hypertension", "tension élevée", "pression haute"],
    "hypotension"  : ["hypotension", "tension basse", "pression basse"],
    "tachycardie"  : ["tachycardie", "pouls rapide", "cœur rapide", "palpitation"],
    "bradycardie"  : ["bradycardie", "pouls lent", "cœur lent"],
    "hyperthermie" : ["hyperthermie", "fièvre", "température élevée", "chaud", "diaphorèse"],
    "hypothermie"  : ["hypothermie", "température basse", "froid", "gelé"],
    "tachypnee"    : ["tachypnée", "respiration rapide", "essoufflement"],
    "bradypnee"    : ["bradypnée", "respiration lente", "apnée"],
    "douleur"      : ["douleur", "mal", "souffre", "tylenol", "analgésique"],
    "marsf"        : ["marsf", "respiration marsf", "évaluer respiration"],
    "far"          : ["far", "pouls far", "évaluer pouls"],
}

# ══════════════════════════════════════════════════════════════════════════════
#  BASE CLINIQUE
# ══════════════════════════════════════════════════════════════════════════════
CLINIQUE_COURT = {
    "pci1"        : "PCI 1 sont les précautions de base pour tous les patients : hygiène des mains, EPI, gestion des piquants, décontamination de l'environnement.",
    "pci2"        : "PCI 2 sont les précautions additionnelles : Contact pour plaies infectées, Gouttelettes pour grippe, Voie aérienne pour tuberculose avec masque N95.",
    "mains"       : "4 moments : 1 avant contact patient, 2 avant acte aseptique, 3 après risque liquides biologiques, 4 après contact patient ou environnement.",
    "pqrstu"      : "PQRSTU évalue un symptôme : P Provoquer Pallier, Q Qualité Quantité, R Région Irradiation, S Symptômes associés, T Temps durée, U compréhension du patient.",
    "ample"       : "AMPLE recueille l'histoire de santé : A Allergies, M Médicaments, P Passé médical, L Last meal dernier repas, E Événement déclencheur.",
    "auscultation": "Auscultation pulmonaire : écouter avec stéthoscope de façon symétrique apex vers bases. Normal : vésiculaire. Anormal : crépitants, sibilances, ronchi, stridor.",
    "inspection"  : "Inspection : évaluation visuelle de la tête aux pieds. Thorax : symétrie, tirage, muscles accessoires, couleur de la peau, rythme selon MARSF.",
    "palpation"   : "Palpation : évaluer par le toucher. Thorax : trachée centrée, expansion symétrique, vibrations vocales. Comparer toujours les deux côtés.",
    "percussion"  : "Percussion : tapoter le thorax. Sonorité normale = poumons aérés. Matité = liquide ou consolidation. Tympanisme = air. Percuter de façon symétrique.",
    "braden"      : "Braden évalue le risque de plaie de pression : 6 critères, score 6 à 23. Inférieur à 18 = risque présent. Plus bas = plus de risque.",
    "morse"       : "Morse évalue le risque de chute : 6 critères, score 0 à 125. 25 à 44 = modéré, 45 et plus = élevé. Ridelles, sonnette, chaussures antidérapantes.",
    "glasgow"     : "Glasgow évalue la conscience : Yeux 1 à 4, Verbal 1 à 5, Motrice 1 à 6. Total 3 à 15. Inférieur à 8 = coma, aviser immédiatement.",
    "cinq_p"      : "5P évaluent la circulation d'un membre : P1 Pouls, P2 Pâleur TRC, P3 Paresthésie, P4 Paralysie, P5 douleur. Toute anomalie = aviser immédiatement.",
    "ffe"         : "FFE documente l'évaluation infirmière complète : signes vitaux FAR et MARSF, évaluation des systèmes, scores Morse et Braden, plan de soins.",
}

MOTS_CLINIQUE = {
    "pci1"        : ["pci 1", "pci1", "précautions de base"],
    "pci2"        : ["pci 2", "pci2", "précautions additionnelles", "isolement", "n95"],
    "mains"       : ["laver les mains", "hygiène des mains", "4 moments", "quatre moments"],
    "pqrstu"      : ["pqrstu", "évaluer douleur", "provoquer pallier"],
    "ample"       : ["ample", "histoire de santé", "antécédents"],
    "auscultation": ["auscultation", "ausculter", "stéthoscope", "bruits pulmonaires"],
    "inspection"  : ["inspection", "inspecter", "observer thorax"],
    "palpation"   : ["palpation", "palper", "expansion thoracique"],
    "percussion"  : ["percussion", "percuter", "sonorité", "matité"],
    "braden"      : ["braden", "plaie de pression", "escarre", "risque escarre"],
    "morse"       : ["morse", "chute", "risque de chute"],
    "glasgow"     : ["glasgow", "gcs", "coma", "état de conscience"],
    "cinq_p"      : ["5p", "cinq p", "neurovasculaire", "paresthésie", "paralysie"],
    "ffe"         : ["ffe", "feuille de flot", "documentation", "dossier infirmier"],
}

# ══════════════════════════════════════════════════════════════════════════════
#  DÉTECTION ET RÉPONSE
# ══════════════════════════════════════════════════════════════════════════════
def detecter_et_repondre(question):
    q = question.lower()

    # Chercher dans OIIQ
    for sujet, mots in MOTS_OIIQ.items():
        for mot in mots:
            if mot in q:
                info = OIIQ[sujet]
                parler(info["court"])
                arts = ", ".join(info["articles"])
                parler(f"Référence : article{'s' if len(info['articles']) > 1 else ''} {arts} du code de déontologie OIIQ.")
                return

    # Chercher dans Soins
    for sujet, mots in MOTS_SOINS.items():
        for mot in mots:
            if mot in q:
                parler(SOINS_COURT[sujet])
                return

    # Chercher dans Clinique
    for sujet, mots in MOTS_CLINIQUE.items():
        for mot in mots:
            if mot in q:
                parler(CLINIQUE_COURT[sujet])
                return

    # Rien trouvé
    parler("Je n'ai pas trouvé de réponse sur ce sujet. Reformule ta question ou demande-moi de l'aide.")

# ══════════════════════════════════════════════════════════════════════════════
#  BOUCLE PRINCIPALE
# ══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("  TonyPi - Système complet v2.0 VOSK OFFLINE")
    print("  SOIN 430 | Cégep St-Jérôme")
    print("=" * 60)

    # Initialiser Vosk
    try:
        vosk_ecoute = VoskEcoute()
    except Exception as e:
        print(f"[ERREUR Vosk] {e}")
        print("Installe le modèle : voir vosk_recognition.py pour les instructions")
        return

    # Mémoire et caméra
    memoire = charger_memoire()
    print(f"[Mémoire] {len(memoire)} étudiant(s) connu(s)")

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not camera.isOpened():
        print("[ERREUR] Caméra introuvable!")
        return

    parler("TonyPi est prêt. Je surveille l'entrée.")

    noms_connus, encodages_connus = encoder_visages_connus(memoire)
    print(f"[Visages] {len(noms_connus)} visage(s) chargé(s)")

    nom_actuel         = None
    derniere_detection = None
    compteur           = 0

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                break

            compteur += 1

            # Reconnaissance faciale (1 frame sur 10)
            if compteur % 10 == 0:
                detecte = identifier_visage(frame, noms_connus, encodages_connus)
                if detecte and detecte != derniere_detection:
                    derniere_detection = detecte
                    if detecte == "inconnu":
                        nom_actuel = accueillir_inconnu(memoire, camera, vosk_ecoute)
                        if nom_actuel:
                            noms_connus, encodages_connus = encoder_visages_connus(memoire)
                    else:
                        nom_actuel = detecte
                        mettre_a_jour_visite(memoire, nom_actuel)
                        accueillir_etudiant(nom_actuel, memoire)

            # Écoute des questions (1 frame sur 30)
            if nom_actuel and compteur % 30 == 0:
                question = vosk_ecoute.ecouter(timeout=4)
                if question:
                    q = question.lower()
                    if any(m in q for m in ["quitter", "stop", "au revoir", "bye"]):
                        parler(f"À bientôt {nom_actuel}!")
                        nom_actuel         = None
                        derniere_detection = None
                    elif any(m in q for m in ["aide", "que peux-tu", "liste"]):
                        parler("Je peux répondre sur le code OIIQ, les signes vitaux, PCI, PQRSTU, AMPLE, Braden, Morse, Glasgow et plus encore!")
                    else:
                        detecter_et_repondre(question)

            cv2.imshow("TonyPi", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\n[TonyPi] Arrêt...")
    finally:
        vosk_ecoute.fermer()
        camera.release()
        cv2.destroyAllWindows()
        parler("À bientôt!")

# ══════════════════════════════════════════════════════════════════════════════
#  MODE TEXTE — test sans caméra ni micro
# ══════════════════════════════════════════════════════════════════════════════
def mode_texte():
    print("=" * 60)
    print("  TonyPi v2.0 - Mode texte")
    print("  Tape 'quitter' pour sortir")
    print("=" * 60)
    while True:
        question = input("\nTa question: ").strip()
        if not question:
            continue
        if question.lower() in ["quitter", "exit"]:
            parler("À bientôt!")
            break
        detecter_et_repondre(question)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "texte":
        mode_texte()
    else:
        main()
