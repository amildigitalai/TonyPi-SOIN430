#!/bin/bash
# ═══════════════════════════════════════════════════════
#  TonyPi - Lancement automatique
#  Double-clic pour démarrer
# ═══════════════════════════════════════════════════════

# Dossier du script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

clear
echo "╔══════════════════════════════════════════════╗"
echo "║         TonyPi - SOIN 430                   ║"
echo "║         Cégep St-Jérôme                     ║"
echo "║         Démarrage en cours...               ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ ERREUR : Python3 introuvable!"
    read -p "Appuie sur ENTER pour fermer..."
    exit 1
fi

# Vérifier que le modèle Vosk est présent
if [ ! -d "/home/pi/vosk-model-fr" ]; then
    echo "⚠️  Modèle Vosk introuvable!"
    echo "Installation automatique en cours..."
    echo ""
    cd /home/pi
    wget -q --show-progress https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip
    unzip -q vosk-model-small-fr-0.22.zip
    mv vosk-model-small-fr-0.22 vosk-model-fr
    cd "$DIR"
    echo "✅ Modèle Vosk installé!"
    echo ""
fi

# Vérifier les dépendances Python
echo "🔍 Vérification des dépendances..."
python3 -c "import vosk" 2>/dev/null || {
    echo "📦 Installation de Vosk..."
    pip install vosk --break-system-packages -q
}
python3 -c "import pyaudio" 2>/dev/null || {
    echo "📦 Installation de PyAudio..."
    pip install pyaudio --break-system-packages -q
}
python3 -c "import face_recognition" 2>/dev/null || {
    echo "📦 Installation de face_recognition..."
    pip install face_recognition --break-system-packages -q
}
python3 -c "import cv2" 2>/dev/null || {
    echo "📦 Installation de OpenCV..."
    pip install opencv-python --break-system-packages -q
}
python3 -c "import pyttsx3" 2>/dev/null || {
    echo "📦 Installation de pyttsx3..."
    pip install pyttsx3 --break-system-packages -q
}

echo ""
echo "✅ Tout est prêt!"
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  🤖 TonyPi démarre...                       ║"
echo "║  Appuie sur Q pour arrêter                  ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Lancer TonyPi
python3 "$DIR/tonypi_vosk.py"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  TonyPi arrêté. À bientôt!                  ║"
echo "╚══════════════════════════════════════════════╝"
read -p "Appuie sur ENTER pour fermer..."
