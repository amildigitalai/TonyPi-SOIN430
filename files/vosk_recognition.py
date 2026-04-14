#!/usr/bin/env python3
"""
TonyPi - Module reconnaissance vocale Vosk offline
Remplace Google Speech Recognition
Fonctionne sans internet sur Raspberry Pi 4
"""

import vosk
import pyaudio
import json
import queue
import threading

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIGURATION VOSK
# ══════════════════════════════════════════════════════════════════════════════
# Chemin du modèle français — à ajuster selon ton installation
MODELE_VOSK = "/home/pi/vosk-model-fr"  # ou /home/pi/model

# Paramètres audio
RATE        = 16000   # Fréquence d'échantillonnage
CHUNK       = 8000    # Taille des blocs audio
CHANNELS    = 1       # Mono

class ReconnaissanceVocale:
    """
    Classe de reconnaissance vocale Vosk offline
    Compatible avec le ReSpeaker 2-Mic HAT
    """

    def __init__(self, modele_path=MODELE_VOSK):
        print("[Vosk] Chargement du modèle français...")
        try:
            self.modele    = vosk.Model(modele_path)
            self.recognizer = vosk.KaldiRecognizer(self.modele, RATE)
            self.audio     = pyaudio.PyAudio()
            self.q         = queue.Queue()
            print("[Vosk] Modèle chargé ✓")
        except Exception as e:
            print(f"[Vosk] ERREUR : {e}")
            print("[Vosk] Vérifie que le modèle est dans : " + modele_path)
            raise

    def _callback(self, in_data, frame_count, time_info, status):
        """Callback PyAudio — reçoit les données audio en continu"""
        self.q.put(bytes(in_data))
        return (None, pyaudio.paContinue)

    def ecouter(self, timeout=8):
        """
        Écoute le microphone et retourne le texte reconnu.
        timeout = durée maximale d'écoute en secondes
        Retourne None si rien de reconnu.
        """
        stream = self.audio.open(
            format            = pyaudio.paInt16,
            channels          = CHANNELS,
            rate              = RATE,
            input             = True,
            frames_per_buffer = CHUNK,
            stream_callback   = self._callback
        )

        stream.start_stream()
        print("[Écoute] Parle maintenant...")

        texte_final = None
        import time
        debut = time.time()

        try:
            while time.time() - debut < timeout:
                try:
                    data = self.q.get(timeout=0.5)
                except queue.Empty:
                    continue

                if self.recognizer.AcceptWaveform(data):
                    resultat = json.loads(self.recognizer.Result())
                    texte = resultat.get("text", "").strip()
                    if texte:
                        print(f"[Étudiant] {texte}")
                        texte_final = texte
                        break
                else:
                    # Résultat partiel — afficher en temps réel
                    partiel = json.loads(self.recognizer.PartialResult())
                    texte_partiel = partiel.get("partial", "")
                    if texte_partiel:
                        print(f"[...] {texte_partiel}", end="\r")

        finally:
            stream.stop_stream()
            stream.close()
            # Vider la queue
            while not self.q.empty():
                self.q.get()

        return texte_final

    def ecouter_continu(self, callback):
        """
        Mode écoute continue — appelle callback(texte) à chaque phrase reconnue.
        Utile pour la boucle principale de TonyPi.
        Usage: reco.ecouter_continu(lambda texte: repondre(texte))
        """
        stream = self.audio.open(
            format            = pyaudio.paInt16,
            channels          = CHANNELS,
            rate              = RATE,
            input             = True,
            frames_per_buffer = CHUNK,
            stream_callback   = self._callback
        )

        stream.start_stream()
        print("[Vosk] Mode écoute continue activé. Ctrl+C pour arrêter.")

        try:
            while True:
                try:
                    data = self.q.get(timeout=1)
                except queue.Empty:
                    continue

                if self.recognizer.AcceptWaveform(data):
                    resultat = json.loads(self.recognizer.Result())
                    texte = resultat.get("text", "").strip()
                    if texte:
                        print(f"\n[Étudiant] {texte}")
                        callback(texte)

        except KeyboardInterrupt:
            print("\n[Vosk] Arrêt écoute continue.")
        finally:
            stream.stop_stream()
            stream.close()

    def fermer(self):
        """Libère les ressources audio"""
        self.audio.terminate()


# ══════════════════════════════════════════════════════════════════════════════
#  INSTALLATION VOSK — instructions complètes
# ══════════════════════════════════════════════════════════════════════════════
INSTRUCTIONS_INSTALLATION = """
╔══════════════════════════════════════════════════════════════╗
║         INSTALLATION VOSK SUR RASPBERRY PI 4               ║
╚══════════════════════════════════════════════════════════════╝

1. INSTALLER VOSK ET PYAUDIO :
   pip install vosk pyaudio --break-system-packages

2. TÉLÉCHARGER LE MODÈLE FRANÇAIS :
   cd /home/pi
   wget https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip
   unzip vosk-model-small-fr-0.22.zip
   mv vosk-model-small-fr-0.22 vosk-model-fr

3. VÉRIFIER LE RESPEAKER 2-MIC HAT :
   # Le ReSpeaker doit être installé en premier
   arecord -l  # doit voir le ReSpeaker comme carte son

4. TESTER LA RECONNAISSANCE :
   python vosk_recognition.py test

5. METTRE À JOUR LE CHEMIN SI NÉCESSAIRE :
   Modifier MODELE_VOSK dans ce fichier si ton modèle
   est dans un autre dossier.

MODÈLES DISPONIBLES (du plus petit au plus précis) :
- vosk-model-small-fr-0.22 : 41 MB — rapide, bon pour RPi 4
- vosk-model-fr-0.6-linto  : 1.4 GB — plus précis mais lent

RECOMMANDATION : vosk-model-small-fr-0.22 pour TonyPi ✓
"""


# ══════════════════════════════════════════════════════════════════════════════
#  TEST RAPIDE
# ══════════════════════════════════════════════════════════════════════════════
def test_vosk():
    """Test rapide de la reconnaissance vocale"""
    print("=" * 60)
    print("  Test Vosk — Reconnaissance vocale offline")
    print("  Parle clairement en français")
    print("  Ctrl+C pour arrêter")
    print("=" * 60)

    try:
        reco = ReconnaissanceVocale()
    except Exception:
        print("\n" + INSTRUCTIONS_INSTALLATION)
        return

    import pyttsx3
    voix = pyttsx3.init()
    voix.setProperty("rate", 145)

    def repondre(texte):
        voix.say(f"J'ai entendu : {texte}")
        voix.runAndWait()

    print("\nDis quelque chose — TonyPi va répéter ce qu'il entend.\n")

    try:
        while True:
            texte = reco.ecouter(timeout=10)
            if texte:
                repondre(texte)
            else:
                print("[Vosk] Rien entendu, réessaie...")
    except KeyboardInterrupt:
        print("\n[Test] Terminé.")
    finally:
        reco.fermer()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_vosk()
    else:
        print(INSTRUCTIONS_INSTALLATION)
