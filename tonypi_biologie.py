#!/usr/bin/env python3
"""
TonyPi - Module Biologie SOIN 430
Sessions 1 et 2 - 14 themes complets - 48 objectifs
USAGE PEDAGOGIQUE UNIQUEMENT
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

BIOLOGIE = {
    "organisation": {
        "titre": "Theme 1 - Organisation du corps humain",
        "court": "Le corps humain est organise en 5 niveaux : cellule, tissu, organe, systeme et organisme. Les systemes nerveux, cardiovasculaire et endocrinien contribuent aux fonctions digestives.",
        "detail": [
            "Cellule : unite de base de la vie.",
            "Tissu : groupe de cellules semblables ayant la meme fonction. 4 types : epithelial, conjonctif, musculaire, nerveux.",
            "Organe : structure composee de plusieurs tissus. Ex : estomac.",
            "Systeme : ensemble d'organes travaillant ensemble. Ex : systeme digestif.",
            "Organisme : l'individu complet.",
            "Les systemes nerveux, cardiovasculaire et endocrinien contribuent aux fonctions du systeme digestif.",
        ]
    },
    "homeostasie": {
        "titre": "Theme 2 - L'homeostasie",
        "court": "L'homeostasie maintient un environnement interne stable. 7 conditions a maintenir. La boucle de retroaction comprend un recepteur, un centre de regulation et un effecteur.",
        "detail": [
            "Definition : maintien d'un environnement interne stable malgre les changements externes.",
            "7 conditions : 1. Concentration des nutriments. 2. O2 et CO2. 3. Dechets. 4. pH. 5. Volume et pression des liquides. 6. Temperature. 7. Volume et pression sanguine.",
            "Boucle de retroaction : Recepteur detecte → Centre de regulation analyse → Effecteur agit.",
            "Retro-inhibition : la reponse reduit le stimulus. Ex : glycemie elevee → insuline → baisse glycemie.",
            "Retroactivation : la reponse amplifie le stimulus. Ex : accouchement, coagulation sanguine.",
            "Metabolisme : ensemble des reactions chimiques du corps pour produire de l'energie.",
        ]
    },
    "nerveux": {
        "titre": "Theme 3 - Le systeme nerveux autonome",
        "court": "Le SNS controle les muscles squelettiques. Le SNA controle les organes internes. Le sympathique active le combat ou fuite. Le parasympathique active le repos et la digestion.",
        "detail": [
            "SNS - Systeme nerveux somatique : controle volontaire des muscles squelettiques.",
            "SNA - Systeme nerveux autonome : controle involontaire des organes internes.",
            "Effecteurs du SNS : muscles squelettiques.",
            "Effecteurs du SNA : muscle cardiaque, muscles lisses, glandes.",
            "Sympathique : combat ou fuite. Accelere le coeur, dilate les bronches, ralentit la digestion. Noradrenaline.",
            "Parasympathique : repos et digestion. Ralentit le coeur, contracte les bronches, active la digestion. Acetylcholine.",
            "Les deux divisions ont des effets opposes sur les memes organes.",
        ]
    },
    "molecules": {
        "titre": "Theme 5 - Les molecules du vivant",
        "court": "Les 4 familles organiques sont glucides, lipides, proteines et acides nucleiques. Le pH normal du sang est 7,35 a 7,45. La denaturation des proteines detruit leur forme 3D.",
        "detail": [
            "Electrolytes : se dissocient en ions dans l'eau. Ex : NaCl donne Na+ et Cl-.",
            "Acides : liberent H+, pH inferieur a 7. Bases : acceptent H+, pH superieur a 7.",
            "Tampons : maintiennent le pH stable. pH sanguin normal : 7,35 a 7,45.",
            "Glucides simples : glucose, fructose, galactose. Complexes : amidon, glycogene, cellulose.",
            "Lipides : triglycerides, phospholipides, steroides. Energie longue duree, membranes, hormones.",
            "Proteines : formees d'acides amines. Roles : enzymes, transport, anticorps, structure.",
            "Denaturation : perte de la forme 3D par chaleur ou pH extreme. Ex : albumine cuite. Perte de fonction.",
            "Acides nucleiques : ADN et ARN. Portent l'information genetique.",
        ]
    },
    "cellule": {
        "titre": "Theme 6 - La cellule et les tissus",
        "court": "La membrane plasmique controle les echanges. Les transports sont passifs sans ATP ou actifs avec ATP. La synthese des proteines se fait en 2 etapes : transcription ADN vers ARNm, puis traduction ARNm vers proteine.",
        "detail": [
            "Membrane plasmique : bicouche de phospholipides avec proteines. Roles : protection, echanges, communication.",
            "Composantes : phospholipides, proteines integrees, proteines peripheriques, cholesterol, glucides.",
            "Transports passifs sans ATP : diffusion simple, diffusion facilitee, osmose.",
            "Transports actifs avec ATP : pompe Na+/K+, endocytose, exocytose.",
            "Mitochondrie : produit ATP par respiration cellulaire. Centrale energetique.",
            "Ribosome : synthese des proteines. Lieu de la traduction.",
            "Noyau : contient ADN. Centre de controle de la cellule.",
            "ADN : code genetique contenant les instructions pour fabriquer toutes les proteines.",
            "Etape 1 Transcription : dans le noyau, ADN → ARNm.",
            "Etape 2 Traduction : au ribosome, ARNm → proteine.",
        ]
    },
    "respiration": {
        "titre": "Theme 7 - La respiration cellulaire",
        "court": "Formule : glucose plus O2 donne CO2 plus eau plus 36 a 38 ATP. Sans oxygene, respiration anaerobie produit acide lactique et seulement 2 ATP. Autres combustibles : acides gras et acides amines.",
        "detail": [
            "ATP : adenosine triphosphate. Monnaie energetique de la cellule.",
            "Formule generale : C6H12O6 + 6O2 → 6CO2 + 6H2O + 36 a 38 ATP.",
            "Lieu : mitochondrie principalement.",
            "3 etapes : glycolyse dans cytoplasme, cycle de Krebs, chaine de transport electrons.",
            "Manque O2 → respiration anaerobie → acide lactique + seulement 2 ATP → fatigue musculaire.",
            "Manque glucose → le corps utilise d'abord les lipides puis les proteines.",
            "Autres combustibles que le glucose : acides gras des lipides et acides amines des proteines.",
        ]
    },
    "digestif": {
        "titre": "Theme 8 - L'anatomie du systeme digestif",
        "court": "Ordre du tube digestif : bouche, pharynx, oesophage, estomac, intestin grele, gros intestin, rectum, anus. Les 4 couches sont muqueuse, sous-muqueuse, musculeuse et sereuse.",
        "detail": [
            "Tube digestif dans l'ordre : bouche, pharynx, oesophage, estomac, intestin grele, gros intestin, rectum, anus.",
            "Organes accessoires : foie, vesicule biliaire, pancreas, glandes salivaires.",
            "4 tissus de l'organisme : epithelial, conjonctif, musculaire, nerveux.",
            "4 couches de l'interieur vers l'exterieur :",
            "Couche 1 Muqueuse : epithelium en contact avec les aliments. Absorption.",
            "Couche 2 Sous-muqueuse : tissu conjonctif, vaisseaux sanguins, nerfs.",
            "Couche 3 Musculeuse : muscles lisses circulaires et longitudinaux. Peristaltisme.",
            "Couche 4 Sereuse : membrane protectrice externe.",
            "Memo : Mon Sous-vetement Muscle Seche = Muqueuse, Sous-muqueuse, Musculeuse, Sereuse.",
        ]
    },
    "digestion": {
        "titre": "Theme 9 - La digestion mecanique et chimique",
        "court": "La salive digere l'amidon. Le suc gastrique digere les proteines. La bile emulsionne les lipides. Le suc pancreatique contient des enzymes pour tous les nutriments dans l'intestin grele.",
        "detail": [
            "Roles de la salive : humidifie, amylase salivaire digere l'amidon, protege les dents, lubrifie.",
            "Composantes du suc gastrique : HCl acide chlorhydrique, pepsine, mucus, facteur intrinseque.",
            "Roles suc gastrique : decompose chimiquement, active pepsine, tue les bacteries.",
            "Nutriments digeres dans l'estomac : proteines partiellement. Tres peu de glucides et lipides.",
            "Nutriments digeres dans intestin grele : glucides, proteines et lipides completement.",
            "Composantes de la bile : sels biliaires, bilirubine, cholesterol, eau.",
            "Role de la bile : emulsionner les lipides en petites gouttelettes pour la lipase.",
            "Hepatocytes et bilirubine : degradent l'hemoglobine en bilirubine excretee dans la bile.",
            "Composantes suc pancreatique : amylase, lipase, proteases, bicarbonate.",
            "Role suc pancreatique : digerer glucides, lipides et proteines. Bicarbonate neutralise l'acidite.",
            "Enzymes inactives du pancreas : secretees sous forme inactive pour eviter l'autodigestion.",
            "Circulation bile : foie → vesicule biliaire → canal choledoque → duodenum.",
            "Roles du colon : absorption eau et electrolytes, formation et elimination des feces.",
            "Composition des feces : eau 75%, bacteries, fibres non digerees, cellules mortes, bilirubine.",
        ]
    },
    "absorption": {
        "titre": "Theme 10 - L'absorption des nutriments",
        "court": "Glucides et acides amines vont dans le sang. Lipides vont dans la lymphe sous forme de chylomicrons. La veine porte hepatique amene les nutriments directement au foie.",
        "detail": [
            "Absorption dans intestin grele : glucides, acides amines, lipides, vitamines, mineraux, eau.",
            "Vers la circulation sanguine : glucose, fructose, acides amines, vitamines hydrosolubles B et C.",
            "Vers la circulation lymphatique : lipides sous forme de chylomicrons, vitamines liposolubles A, D, E, K.",
            "Veine porte hepatique : transporte nutriments absorbes de l'intestin directement au foie.",
            "Foie : traite, stocke et distribue les nutriments. Produit proteines plasmatiques.",
            "Micelles : sels biliaires + lipides → facilitent absorption dans la cellule intestinale.",
            "Chylomicrons : lipides emballes dans la cellule intestinale, transportes dans la lymphe.",
            "VLDL : tres faible densite. Transporte lipides du foie vers les tissus.",
            "LDL : mauvais cholesterol. Apporte cholesterol aux cellules.",
            "HDL : bon cholesterol. Ramene cholesterol des cellules vers le foie.",
        ]
    },
    "regulation_dig": {
        "titre": "Theme 11 - La regulation de la digestion",
        "court": "2 mecanismes de controle : nerveux et hormonal. Le parasympathique active la digestion. Le sympathique l'inhibe. Les hormones gastrine, secretine et cholecystokinine regulen les secretions.",
        "detail": [
            "2 types de mecanismes : nerveux et hormonal.",
            "Parasympathique : active la digestion. Augmente secretions et motilite.",
            "Sympathique : inhibe la digestion. Reduit secretions et motilite.",
            "Gastrine : stimule la secretion de HCl par l'estomac.",
            "Secretine : stimule le pancreas a secreter du bicarbonate.",
            "Cholecystokinine CCK : stimule la vesicule biliaire et le pancreas.",
        ]
    },
    "cancer": {
        "titre": "Theme 12 - La division cellulaire et le cancer",
        "court": "La mitose produit 2 cellules filles identiques pour la croissance et la reparation. Les cellules cancereuses se divisent de facon incontrolee, envahissent les tissus et peuvent former des metastases.",
        "detail": [
            "Mitose : division cellulaire produisant 2 cellules filles identiques a la cellule mere.",
            "Utilite dans le corps : croissance, reparation et remplacement des cellules usees.",
            "Cellules cancereuses : se divisent de facon incontrolee et anarchique.",
            "Proliferation incontrolee : ne s'arretent pas de se diviser.",
            "Dedifferentiation : perdent leurs fonctions specialisees.",
            "Invasivite : envahissent les tissus voisins.",
            "Metastases : migrent vers d'autres organes via le sang ou la lymphe.",
            "Tumeur benigne : croissance lente, encapsulee, ne metastase pas.",
            "Tumeur maligne : croissance rapide, invasive, peut metastaser.",
        ]
    },
    "metabolisme": {
        "titre": "Theme 13 - Le metabolisme des glucides, lipides et proteines",
        "court": "Le glucose est stocke en glycogene. L'exces est converti en lipides. Les lipides fournissent 2 fois plus d'energie par gramme que les glucides. Les proteines peuvent servir d'energie en dernier recours.",
        "detail": [
            "Glycogenese : formation de glycogene a partir du glucose en exces.",
            "Glycogenolyse : degradation du glycogene en glucose lors d'une hypoglycemie.",
            "Neoglucogenese : fabrication de glucose a partir d'acides amines ou glycerol.",
            "Metabolisme lipides : triglycerides → acides gras → beta-oxydation → ATP.",
            "Les lipides fournissent 9 kcal/g contre 4 kcal/g pour les glucides.",
            "Exces de glucides ou proteines : converti en lipides stockes dans le tissu adipeux.",
            "Metabolisme proteines : acides amines → synthese proteique ou energie.",
            "Desamination : retrait du groupe amine → ammoniac → uree → eliminee par les reins.",
            "Corps cetoniques : produits lors de degradation excessive des lipides. Signe d'alarme en diabete.",
        ]
    },
    "diabete": {
        "titre": "Theme 14 - Le diabete",
        "court": "Le diabete est une hyperglycemie chronique. Type 1 : manque d'insuline. Type 2 : resistance a l'insuline. L'insuline fait entrer le glucose dans les cellules et abaisse la glycemie.",
        "detail": [
            "Diabete : glycemie chroniquement superieure a 7 mmol/L a jeun.",
            "Insuline : hormone du pancreas. Fait entrer glucose dans les cellules. Abaisse la glycemie.",
            "Glucagon : hormone du pancreas. Libere glucose du foie. Augmente la glycemie.",
            "Diabete type 1 : destruction cellules beta du pancreas. Manque total insuline. Insulinodependant.",
            "Diabete type 2 : resistance des cellules a l'insuline. Lie a l'obesite et la sedentarite.",
            "Diabete gestationnel : pendant la grossesse. Resistance temporaire a l'insuline.",
            "Hyperglycemie : glycemie trop elevee. Symptomes : polyurie, polydipsie, polyphagie.",
            "Hypoglycemie : glycemie trop basse. Symptomes : tremblements, sueurs, confusion.",
            "Complications : retinopathie, nephropathie, neuropathie, maladies cardiovasculaires.",
            "Traitement type 1 : insuline obligatoire.",
            "Traitement type 2 : alimentation, exercice, metformine, insuline si necessaire.",
            "HbA1c : mesure glycemie moyenne des 3 derniers mois. Normal : inferieur a 6,5 pourcent.",
        ]
    },
}

MOTS_CLES = {
    "organisation"  : ["organisation", "niveaux", "cellule tissu organe"],
    "homeostasie"   : ["homeostasie", "retroaction", "retro-inhibition", "retroactivation", "7 conditions", "metabolisme"],
    "nerveux"       : ["nerveux autonome", "sympathique", "parasympathique", "sna", "sns", "effecteurs"],
    "molecules"     : ["molecules", "electrolytes", "ions", "acides", "bases", "tampons", "ph", "glucides", "lipides", "proteines", "denaturation"],
    "cellule"       : ["cellule", "membrane plasmique", "mitochondrie", "ribosome", "noyau", "adn", "transcription", "traduction", "synthese proteines"],
    "respiration"   : ["respiration cellulaire", "atp", "anaerobie", "combustible", "formule respiration"],
    "digestif"      : ["systeme digestif", "tube digestif", "4 couches", "muqueuse", "sereuse"],
    "digestion"     : ["digestion", "salive", "suc gastrique", "bile", "pancreas", "suc pancreatique", "colon", "feces", "bilirubine"],
    "absorption"    : ["absorption", "nutriments absorbes", "veine porte", "chylomicrons", "ldl", "hdl", "vldl", "micelles"],
    "regulation_dig": ["regulation digestion", "gastrine", "secretine", "cholecystokinine"],
    "cancer"        : ["cancer", "mitose", "division cellulaire", "tumeur", "metastase"],
    "metabolisme"   : ["metabolisme", "glycogene", "glycogenese", "glycogenolyse", "neoglucogenese", "corps cetoniques"],
    "diabete"       : ["diabete", "insuline", "glucagon", "hyperglycemie", "hypoglycemie", "type 1", "type 2", "hba1c", "glycemie"],
}

def detecter_theme(question):
    q = question.lower()
    for theme, mots in MOTS_CLES.items():
        for mot in mots:
            if mot in q:
                return theme
    return None

def demande_detail(question):
    return any(m in question.lower() for m in ["detail", "expliquer", "tout", "complet", "liste", "enumerer", "objectif"])

def repondre_biologie(question):
    theme = detecter_theme(question)
    if not theme:
        parler("Je n'ai pas reconnu le theme. Tu peux demander : homeostasie, cellule, respiration cellulaire, digestion, absorption, cancer, metabolisme, diabete et plus!")
        return
    info = BIOLOGIE[theme]
    parler(info["titre"])
    if demande_detail(question):
        for item in info["detail"]:
            parler(item)
    else:
        parler(info["court"])
        parler("Veux-tu que je t'explique en detail?")

def ecouter(timeout=8):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Ecoute] Pose ta question...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
            texte = recognizer.recognize_google(audio, language="fr-CA")
            print(f"[Etudiant] {texte}")
            return texte
        except:
            return None

def main():
    print("=" * 60)
    print("  TonyPi - Module Biologie SOIN 430")
    print("  Sessions 1 et 2 - 14 themes - 48 objectifs")
    print("=" * 60)
    parler("Bonjour! Je peux t'aider avec les 14 themes de biologie SOIN 430 sessions 1 et 2. Pose-moi une question!")
    while True:
        question = ecouter()
        if not question:
            parler("Je n'ai pas entendu. Tu peux repeter?")
            continue
        if any(m in question.lower() for m in ["quitter", "stop", "au revoir"]):
            parler("Bonne chance pour ton examen!")
            break
        if any(m in question.lower() for m in ["aide", "liste", "themes"]):
            parler("14 themes disponibles : organisation, homeostasie, nerveux autonome, molecules, cellule, respiration cellulaire, digestif, digestion, absorption, regulation, cancer, metabolisme, diabete.")
            continue
        repondre_biologie(question)

def mode_texte():
    print("=" * 60)
    print("  TonyPi Biologie - Mode texte")
    print("  Exemples : 'homeostasie', 'digestion detail', 'diabete'")
    print("  Tape 'liste' pour les themes | 'quitter' pour sortir")
    print("=" * 60)
    while True:
        question = input("\nTa question: ").strip()
        if not question:
            continue
        if question.lower() in ["quitter", "exit"]:
            break
        if question.lower() == "liste":
            for k, v in BIOLOGIE.items():
                print(f"  - {v['titre']}")
            continue
        repondre_biologie(question)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "texte":
        mode_texte()
    else:
        main()
