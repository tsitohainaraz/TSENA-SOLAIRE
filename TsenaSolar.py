import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="Tsena Solaire Malagasy - Devis Automatique",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration CSS avancée
st.markdown("""
<style>
    :root {
        --primary: #FF6B00;
        --secondary: #2E86C1;
        --accent: #28B463;
        --light: #F8F9F9;
        --dark: #2C3E50;
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        text-align: center;
        font-size: 2.8em;
        font-weight: 800;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .section-header {
        background-color: var(--light);
        color: var(--dark);
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid var(--primary);
        margin: 20px 0;
        font-size: 1.6em;
        font-weight: 700;
    }
    
    .product-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        border-color: var(--primary);
    }
    
    .price-tag {
        background: linear-gradient(135deg, var(--accent) 0%, #1D8348 100%);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2em;
        display: inline-block;
        margin: 5px 0;
    }
    
    .config-box {
        background: linear-gradient(135deg, #E8F4FD 0%, #F0F7FF 100%);
        border-radius: 10px;
        padding: 20px;
        border: 2px solid var(--secondary);
        margin: 15px 0;
    }
    
    .result-card {
        background: linear-gradient(135deg, #fff8e1 0%, #fff3e0 100%);
        border-radius: 15px;
        padding: 25px;
        border: 3px solid var(--primary);
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(255,107,0,0.15);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, #E65B00 100%);
        color: white;
        font-weight: bold;
        padding: 12px 28px;
        border-radius: 8px;
        border: none;
        font-size: 1.1em;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 5px 15px rgba(255,107,0,0.3);
    }
    
    .metric-box {
        background: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 2px solid var(--secondary);
        margin: 10px 0;
    }
    
    .metric-value {
        font-size: 1.8em;
        font-weight: bold;
        color: var(--primary);
        margin: 5px 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        color: var(--dark);
        opacity: 0.8;
    }
    
    .tab-container {
        background: var(--light);
        border-radius: 10px;
        padding: 5px;
        margin: 15px 0;
    }
    
    .footer {
        text-align: center;
        color: var(--dark);
        padding: 20px;
        margin-top: 40px;
        border-top: 3px solid var(--primary);
        font-size: 0.9em;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des données de session
if 'materiels' not in st.session_state:
    st.session_state.materiels = []
if 'selected_components' not in st.session_state:
    st.session_state.selected_components = {}
if 'devis_data' not in st.session_state:
    st.session_state.devis_data = {}

# Base de données des produits
PRODUCT_DATABASE = {
    "convertisseurs": [
        {
            "id": 1,
            "nom": "24V / 3KW Inverter",
            "puissance": 3000,
            "tension": 24,
            "prix": 1400000,
            "description": "Puissance 3000W · Sortie 230Vac monophasé · Batterie 24Vdc · MPPT 30-90Vdc 40A · 1 MPPT · Usage intérieur IP20",
            "marque": "SRNE",
            "type": "Hybride"
        },
        {
            "id": 2,
            "nom": "48V / 5KW Inverter",
            "puissance": 5000,
            "tension": 48,
            "prix": 2400000,
            "description": "Puissance 5000W · Sortie 230Vac mono/tri en parallèle · Batterie 48Vdc · MPPT 120-450Vdc 22A · Jusqu'à 6 unités en parallèle · IP20",
            "marque": "HAISIC",
            "type": "Hybride"
        },
        {
            "id": 3,
            "nom": "48V / 10KW Inverter",
            "puissance": 10000,
            "tension": 48,
            "prix": 6000000,
            "description": "Puissance 10 000W · Sortie 230Vac mono/tri · Batterie 48Vdc · 2 MPPT (22A+22A) · Parallèle jusqu'à 6 unités · IP20",
            "marque": "HAISIC",
            "type": "Hybride"
        },
        {
            "id": 4,
            "nom": "48V / 12KW Inverter H3",
            "puissance": 12000,
            "tension": 48,
            "prix": 6600000,
            "description": "Puissance 12 000W · Sortie 230Vac mono/tri · Batterie 48Vdc · 2 MPPT · Entrée PV max 9kW+9kW · IP20",
            "marque": "SRNE",
            "type": "Hybride"
        },
        {
            "id": 5,
            "nom": "48V / 6KW Inverter IP65",
            "puissance": 6000,
            "tension": 48,
            "prix": 3500000,
            "description": "Puissance 6000W · Sortie 230Vac mono/tri · Batterie 48Vdc · MPPT 120-450Vdc · Parallèle jusqu'à 6 unités · IP65",
            "marque": "HONG FENG",
            "type": "Hybride"
        },
        {
            "id": 6,
            "nom": "48V / 12KW Inverter IP65",
            "puissance": 12000,
            "tension": 48,
            "prix": 8700000,
            "description": "Puissance 12 000W · Sortie 230Vac mono/tri · Batterie 48Vdc · 2 MPPT · Entrée PV 5.5kW+5.5kW · IP65",
            "marque": "SRNE",
            "type": "Hybride"
        }
    ],
    
    "batteries": [
        {
            "id": 7,
            "nom": "Batterie Lithium 25.6V / 100Ah",
            "tension": 25.6,
            "capacite": 100,
            "energie": 2.56,
            "prix": 2600000,
            "description": "Tension 25.6V · Capacité 100Ah · Énergie 2.56kWh · Courant charge max 100A · Durée de vie 6000 cycles",
            "marque": "HAISIC",
            "type": "Lithium LFP"
        },
        {
            "id": 8,
            "nom": "Batterie Lithium 51.2V / 100Ah",
            "tension": 51.2,
            "capacite": 100,
            "energie": 5.12,
            "prix": 5000000,
            "description": "Tension 51.2V · Capacité 100Ah · Énergie 5.12kWh · Courant charge max 100A · 6000 cycles",
            "marque": "SRNE",
            "type": "Lithium LFP"
        },
        {
            "id": 9,
            "nom": "Batterie Lithium 51.2V / 200Ah",
            "tension": 51.2,
            "capacite": 200,
            "energie": 10.24,
            "prix": 9000000,
            "description": "Tension 51.2V · Capacité 200Ah · Énergie 10.24kWh · Courant charge max 200A · 6000 cycles",
            "marque": "HAISIC",
            "type": "Lithium LFP"
        },
        {
            "id": 10,
            "nom": "Batterie Lithium 51.2V / 316Ah",
            "tension": 51.2,
            "capacite": 316,
            "energie": 16.49,
            "prix": 11500000,
            "description": "Tension 51.2V · Capacité 316Ah · Énergie 16.49kWh · Courant charge max 300A · 6000 cycles",
            "marque": "CHINA ESS",
            "type": "Lithium LFP"
        }
    ],
    
    "panneaux": [
        {
            "id": "P110",
            "puissance": 110,
            "prix": 130000,
            "description": "Panneau solaire monocristallin 110W",
            "marque": "Jinko Solar"
        },
        {
            "id": "P210",
            "puissance": 210,
            "prix": 180000,
            "description": "Panneau solaire monocristallin 210W",
            "marque": "Jinko Solar"
        },
        {
            "id": "P550",
            "puissance": 550,
            "prix": 500000,
            "description": "Panneau solaire monocristallin 550W",
            "marque": "Canadian Solar"
        },
        {
            "id": "P580",
            "puissance": 580,
            "prix": 600000,
            "description": "Panneau solaire monocristallin 580W",
            "marque": "Canadian Solar"
        },
        {
            "id": "P60",
            "puissance": 60,
            "prix": 80000,
            "description": "Panneau solaire polycristallin 60W",
            "marque": "Trina Solar"
        },
        {
            "id": "P80",
            "puissance": 80,
            "prix": 100000,
            "description": "Panneau solaire polycristallin 80W",
            "marque": "Trina Solar"
        }
    ],
    
    "pompes": [
        {"id": 13, "nom": "3DSP4/95-D18/750W", "puissance": 750, "prix": 720000, "type": "DC"},
        {"id": 14, "nom": "3DSP4/165-D110/1500", "puissance": 1500, "prix": 870000, "type": "DC"},
        {"id": 15, "nom": "3DSP4/125-D110/1100W", "puissance": 1100, "prix": 830000, "type": "DC"},
        {"id": 16, "nom": "4DSP6/95-D110/1100W", "puissance": 1100, "prix": 840000, "type": "DC"},
        {"id": 17, "nom": "4DSP6/135-D110/1500W", "puissance": 1500, "prix": 850000, "type": "DC"},
        {"id": 18, "nom": "3DSP4/95-A220/D110V-750W", "puissance": 750, "prix": 980000, "type": "AC/DC"},
        {"id": 19, "nom": "3DSP4/125-A220/D110V-1100W", "puissance": 1100, "prix": 1030000, "type": "AC/DC"},
        {"id": 20, "nom": "3DSP5-140-A220/D200-1500", "puissance": 1500, "prix": 1050000, "type": "AC/DC"},
        {"id": 21, "nom": "4DSP6/175-A220/D300-2200W", "puissance": 2200, "prix": 1140000, "type": "AC"},
        {"id": 22, "nom": "4SPM318-1.1", "puissance": 1100, "prix": 520000, "type": "AC Surface"},
        {"id": 23, "nom": "PM60-400Z", "puissance": 400, "prix": 260000, "type": "AC"},
        {"id": 24, "nom": "PM70-600Z", "puissance": 600, "prix": 330000, "type": "AC"},
        {"id": 25, "nom": "PM80-800Z", "puissance": 800, "prix": 340000, "type": "AC"},
        {"id": 26, "nom": "PM90-1500Z", "puissance": 1500, "prix": 420000, "type": "AC"}
    ],
    
    "regulateurs": [
        {"id": 27, "nom": "PWM 12/24V -- 20A", "courant": 20, "prix": 80000, "type": "PWM"},
        {"id": 28, "nom": "PWM 12/24V -- 60A", "courant": 60, "prix": 190000, "type": "PWM"},
        {"id": 29, "nom": "MPPT 12/24V -- 20A", "courant": 20, "prix": 240000, "type": "MPPT"},
        {"id": 30, "nom": "MPPT 12/24/48V -- 60A", "courant": 60, "prix": 650000, "type": "MPPT"}
    ],
    
    "eclairage": [
        {"id": 11, "nom": "BL-3000 Solar Street Light", "prix": 200000, "description": "Lampadaire solaire autonome · Panneau intégré · Usage extérieur"},
        {"id": 12, "nom": "YL-30P Solar Street Light", "prix": 270000, "description": "Lampadaire solaire 250W · Panneau solaire inclus"}
    ]
}

# Fonctions utilitaires
def format_prix(prix):
    return f"{prix:,.0f} Ar".replace(",", " ")

def calculate_system_configuration(consommation_jour, consommation_nuit, params):
    """Calcule la configuration du système solaire"""
    # Calculs de base
    energie_totale = consommation_jour + consommation_nuit
    energie_avec_rendement = energie_totale / params['rendement']
    
    # Calcul nombre de panneaux
    energie_panneau_jour = params['puissance_panneau'] * params['heures_ensoleillement']
    n_panneaux = max(1, np.ceil(energie_avec_rendement / energie_panneau_jour))
    
    # Calcul capacité batterie nécessaire
    capacite_necessaire_wh = (consommation_nuit * params['autonomie']) / params['profondeur_decharge']
    
    # Sélection de la batterie
    batterie_selectionnee = None
    for batterie in PRODUCT_DATABASE['batteries']:
        capacite_wh = batterie['energie'] * 1000  # Convertir kWh en Wh
        if capacite_wh >= capacite_necessaire_wh:
            batterie_selectionnee = batterie
            break
    
    # Si aucune batterie n'est suffisante, prendre la plus grande
    if not batterie_selectionnee:
        batterie_selectionnee = max(PRODUCT_DATABASE['batteries'], key=lambda x: x['energie'])
    
    # Calcul nombre de batteries
    n_batteries = max(1, np.ceil(capacite_necessaire_wh / (batterie_selectionnee['energie'] * 1000)))
    
    # Sélection du convertisseur
    puissance_maximale = params['puissance_max'] * params['marge_securite']
    convertisseur_selectionne = None
    
    for conv in sorted(PRODUCT_DATABASE['convertisseurs'], key=lambda x: x['puissance']):
        if conv['puissance'] >= puissance_maximale:
            convertisseur_selectionne = conv
            break
    
    if not convertisseur_selectionne:
        convertisseur_selectionne = max(PRODUCT_DATABASE['convertisseurs'], key=lambda x: x['puissance'])
    
    return {
        'n_panneaux': int(n_panneaux),
        'batterie': batterie_selectionnee,
        'n_batteries': int(n_batteries),
        'convertisseur': convertisseur_selectionne,
        'energie_totale': energie_totale,
        'energie_avec_rendement': energie_avec_rendement,
        'capacite_necessaire_wh': capacite_necessaire_wh
    }

# Interface principale
st.markdown('<div class="main-header">☀️ TSENA SOLAIRE MALAGASY ☀️</div>', unsafe_allow_html=True)
st.markdown("### Plateforme de Devis Automatique - Ingénieur d'Étude Énergie Solaire")

# Sidebar pour la navigation
with st.sidebar:
    st.markdown("### 🔧 Navigation")
    menu = st.radio("", [
        "📝 Saisie Consommation", 
        "⚙️ Configuration Système", 
        "💰 Génération Devis",
        "📊 Visualisation Complète"
    ])
    
    st.markdown("---")
    st.markdown("### ⚡ Paramètres Techniques")
    
    # Paramètres avancés dans la sidebar
    with st.expander("Paramètres de calcul"):
        rendement = st.slider("Rendement système (%)", 70, 95, 85)
        autonomie = st.slider("Autonomie (jours)", 1, 5, 2)
        profondeur_decharge = st.selectbox("Profondeur de décharge", 
                                          [("Lithium LFP", 0.8), 
                                           ("Gel", 0.7), 
                                           ("Acide", 0.5)], 
                                          format_func=lambda x: f"{x[0]} - {int(x[1]*100)}%")[1]
        heures_ensoleillement = st.slider("Heures d'ensoleillement", 3.0, 8.0, 5.5, 0.5)
        marge_securite = st.slider("Marge de sécurité", 1.0, 2.0, 1.25, 0.05)
    
    st.markdown("---")
    if st.button("🔄 Réinitialiser tout", type="secondary"):
        st.session_state.materiels = []
        st.session_state.selected_components = {}
        st.session_state.devis_data = {}
        st.success("Toutes les données ont été réinitialisées!")
        st.rerun()

# Section 1: Saisie de consommation
if menu == "📝 Saisie Consommation":
    st.markdown('<div class="section-header">1. Saisie de votre consommation électrique</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### 📋 Ajouter un équipement")
        with st.form("ajout_equipement", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                nom = st.text_input("Nom de l'équipement*", placeholder="Ex: Réfrigérateur")
            with c2:
                puissance = st.number_input("Puissance (W)*", min_value=1, step=1, value=100)
            with c3:
                quantite = st.number_input("Quantité*", min_value=1, step=1, value=1)
            
            c4, c5 = st.columns(2)
            with c4:
                heures_jour = st.number_input("Heures/jour*", min_value=0.0, max_value=24.0, step=0.5, value=8.0)
            with c5:
                heures_nuit = st.number_input("Heures/nuit*", min_value=0.0, max_value=24.0, step=0.5, value=8.0)
            
            if st.form_submit_button("➕ Ajouter l'équipement", use_container_width=True):
                if nom:
                    puissance_totale = puissance * quantite
                    energie_jour = puissance_totale * heures_jour
                    energie_nuit = puissance_totale * heures_nuit
                    
                    st.session_state.materiels.append({
                        "Nom": nom,
                        "Puissance (W)": puissance,
                        "Quantité": quantite,
                        "Puissance totale (W)": puissance_totale,
                        "Heures/jour": heures_jour,
                        "Energie jour (Wh)": energie_jour,
                        "Heures/nuit": heures_nuit,
                        "Energie nuit (Wh)": energie_nuit
                    })
                    st.success(f"✅ {nom} ajouté avec succès!")
                else:
                    st.error("Veuillez saisir un nom pour l'équipement")
    
    with col2:
        st.markdown("#### 📊 Consommation rapide")
        
        with st.expander("💡 Exemples typiques"):
            exemples = {
                "Ampoule LED 10W": {"puissance": 10, "heures": 5},
                "Réfrigérateur 150W": {"puissance": 150, "heures": 24},
                "TV LED 50W": {"puissance": 50, "heures": 4},
                "Ordinateur 100W": {"puissance": 100, "heures": 6},
                "Ventilateur 50W": {"puissance": 50, "heures": 8}
            }
            
            for nom_ex, details in exemples.items():
                if st.button(f"➕ {nom_ex}", key=f"ex_{nom_ex}"):
                    st.session_state.materiels.append({
                        "Nom": nom_ex,
                        "Puissance (W)": details["puissance"],
                        "Quantité": 1,
                        "Puissance totale (W)": details["puissance"],
                        "Heures/jour": details["heures"],
                        "Energie jour (Wh)": details["puissance"] * details["heures"],
                        "Heures/nuit": 0,
                        "Energie nuit (Wh)": 0
                    })
                    st.rerun()
    
    # Affichage des équipements
    if st.session_state.materiels:
        st.markdown("#### 📈 Synthèse de votre consommation")
        
        df_materiels = pd.DataFrame(st.session_state.materiels)
        
        # Calculs totaux
        total_puissance = df_materiels["Puissance totale (W)"].sum()
        total_energie_jour = df_materiels["Energie jour (Wh)"].sum()
        total_energie_nuit = df_materiels["Energie nuit (Wh)"].sum()
        puissance_max = df_materiels["Puissance totale (W)"].max()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Puissance totale", f"{total_puissance:,} W")
        with col2:
            st.metric("Énergie jour", f"{total_energie_jour:,} Wh")
        with col3:
            st.metric("Énergie nuit", f"{total_energie_nuit:,} Wh")
        with col4:
            st.metric("Puissance max", f"{puissance_max:,} W")
        
        # Tableau détaillé
        st.markdown("##### Détail des équipements")
        st.dataframe(df_materiels, use_container_width=True, hide_index=True)
        
        # Bouton de suppression
        if st.button("🗑️ Supprimer tous les équipements", type="secondary"):
            st.session_state.materiels = []
            st.rerun()
    else:
        st.info("👋 Commencez par ajouter vos équipements électriques ci-dessus")

# Section 2: Configuration du système
elif menu == "⚙️ Configuration Système":
    st.markdown('<div class="section-header">2. Configuration de votre système solaire</div>', unsafe_allow_html=True)
    
    if not st.session_state.materiels:
        st.warning("⚠️ Veuillez d'abord saisir votre consommation dans l'onglet 'Saisie Consommation'")
    else:
        # Calcul de la consommation
        df_materiels = pd.DataFrame(st.session_state.materiels)
        consommation_jour = df_materiels["Energie jour (Wh)"].sum()
        consommation_nuit = df_materiels["Energie nuit (Wh)"].sum()
        puissance_max = df_materiels["Puissance totale (W)"].max()
        
        # Paramètres de calcul
        params = {
            'rendement': rendement / 100,
            'autonomie': autonomie,
            'profondeur_decharge': profondeur_decharge,
            'heures_ensoleillement': heures_ensoleillement,
            'marge_securite': marge_securite,
            'puissance_max': puissance_max
        }
        
        # Onglets pour les différents composants
        tab1, tab2, tab3, tab4 = st.tabs(["☀️ Panneaux Solaires", "🔋 Batteries", "🔌 Convertisseurs", "⚙️ Autres Équipements"])
        
        with tab1:
            st.markdown("#### Sélectionnez vos panneaux solaires")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                # Sélection automatique ou manuelle
                mode_selection = st.radio("Mode de sélection", ["Automatique (recommandé)", "Manuelle"])
                
                if mode_selection == "Automatique (recommandé)":
                    # Calcul automatique
                    puissance_panneau_auto = st.selectbox(
                        "Puissance des panneaux disponibles",
                        [60, 80, 110, 210, 550, 580],
                        format_func=lambda x: f"{x}W"
                    )
                    params['puissance_panneau'] = puissance_panneau_auto
                    
                    # Calcul de la configuration
                    config = calculate_system_configuration(consommation_jour, consommation_nuit, params)
                    
                    st.markdown(f"**Configuration recommandée:**")
                    st.markdown(f"- {config['n_panneaux']} × {puissance_panneau_auto}W")
                    
                    # Trouver le prix du panneau sélectionné
                    for panneau in PRODUCT_DATABASE['panneaux']:
                        if panneau['puissance'] == puissance_panneau_auto:
                            prix_panneau = panneau['prix']
                            st.markdown(f"- Prix unitaire: {format_prix(prix_panneau)}")
                            st.markdown(f"- Total panneaux: {format_prix(prix_panneau * config['n_panneaux'])}")
                            break
                    
                    # Stocker la sélection
                    st.session_state.selected_components['panneaux'] = {
                        'type': f"Panneau {puissance_panneau_auto}W",
                        'quantite': config['n_panneaux'],
                        'prix_unitaire': prix_panneau,
                        'config': config
                    }
                
                else:
                    # Sélection manuelle
                    panneaux_options = {f"{p['puissance']}W - {format_prix(p['prix'])}": p for p in PRODUCT_DATABASE['panneaux']}
                    panneau_selection = st.selectbox("Choisir un panneau", list(panneaux_options.keys()))
                    panneau_data = panneaux_options[panneau_selection]
                    
                    quantite_panneaux = st.number_input("Nombre de panneaux", min_value=1, value=4, step=1)
                    
                    st.session_state.selected_components['panneaux'] = {
                        'type': f"Panneau {panneau_data['puissance']}W",
                        'quantite': quantite_panneaux,
                        'prix_unitaire': panneau_data['prix'],
                        'description': panneau_data['description']
                    }
            
            with col2:
                st.markdown("#### 📋 Liste des panneaux disponibles")
                for panneau in PRODUCT_DATABASE['panneaux']:
                    with st.container():
                        st.markdown(f"**{panneau['puissance']}W**")
                        st.markdown(f"<span class='price-tag'>{format_prix(panneau['prix'])}</span>", unsafe_allow_html=True)
                        st.caption(f"{panneau['description']}")
                        st.markdown("---")
        
        with tab2:
            st.markdown("#### Sélectionnez vos batteries")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                if 'config' in st.session_state.selected_components.get('panneaux', {}):
                    config = st.session_state.selected_components['panneaux']['config']
                    
                    st.markdown("**Batterie recommandée:**")
                    batterie = config['batterie']
                    
                    st.markdown(f"**{batterie['nom']}**")
                    st.markdown(f"- Énergie: {batterie['energie']} kWh")
                    st.markdown(f"- Tension: {batterie['tension']}V")
                    st.markdown(f"- Capacité: {batterie['capacite']}Ah")
                    st.markdown(f"- Quantité recommandée: {config['n_batteries']}")
                    st.markdown(f"- Prix unitaire: {format_prix(batterie['prix'])}")
                    
                    quantite_batteries = st.number_input(
                        "Nombre de batteries", 
                        min_value=1, 
                        value=config['n_batteries'],
                        step=1,
                        key="batteries_qty"
                    )
                    
                    st.session_state.selected_components['batteries'] = {
                        'type': batterie['nom'],
                        'quantite': quantite_batteries,
                        'prix_unitaire': batterie['prix'],
                        'description': batterie['description'],
                        'energie': batterie['energie']
                    }
                else:
                    st.warning("Veuillez d'abord configurer les panneaux solaires")
            
            with col2:
                st.markdown("#### 🔋 Batteries disponibles")
                for batterie in PRODUCT_DATABASE['batteries']:
                    with st.container():
                        st.markdown(f"**{batterie['nom']}**")
                        st.markdown(f"<span class='price-tag'>{format_prix(batterie['prix'])}</span>", unsafe_allow_html=True)
                        st.caption(f"{batterie['energie']} kWh · {batterie['capacite']}Ah")
                        st.markdown("---")
        
        with tab3:
            st.markdown("#### Sélectionnez votre convertisseur hybride")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                if 'config' in st.session_state.selected_components.get('panneaux', {}):
                    config = st.session_state.selected_components['panneaux']['config']
                    
                    st.markdown("**Convertisseur recommandé:**")
                    convertisseur = config['convertisseur']
                    
                    st.markdown(f"**{convertisseur['nom']}**")
                    st.markdown(f"- Puissance: {convertisseur['puissance']:,}W")
                    st.markdown(f"- Tension: {convertisseur['tension']}V")
                    st.markdown(f"- Prix: {format_prix(convertisseur['prix'])}")
                    st.markdown(f"- Marque: {convertisseur['marque']}")
                    
                    st.markdown("**Description technique:**")
                    st.info(convertisseur['description'])
                    
                    st.session_state.selected_components['convertisseur'] = {
                        'type': convertisseur['nom'],
                        'prix': convertisseur['prix'],
                        'description': convertisseur['description'],
                        'puissance': convertisseur['puissance'],
                        'marque': convertisseur['marque']
                    }
                else:
                    st.warning("Veuillez d'abord configurer les panneaux solaires")
            
            with col2:
                st.markdown("#### 🔌 Convertisseurs disponibles")
                for conv in PRODUCT_DATABASE['convertisseurs']:
                    with st.container():
                        st.markdown(f"**{conv['nom']}**")
                        st.markdown(f"<span class='price-tag'>{format_prix(conv['prix'])}</span>", unsafe_allow_html=True)
                        st.caption(f"{conv['puissance']:,}W · {conv['marque']}")
                        st.markdown("---")
        
        with tab4:
            st.markdown("#### Autres équipements optionnels")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Pompes solaires")
                pompe_selection = st.selectbox(
                    "Sélectionnez une pompe",
                    [""] + [p['nom'] for p in PRODUCT_DATABASE['pompes']],
                    format_func=lambda x: x if x else "Aucune pompe"
                )
                
                if pompe_selection:
                    pompe_data = next(p for p in PRODUCT_DATABASE['pompes'] if p['nom'] == pompe_selection)
                    st.markdown(f"**Prix:** {format_prix(pompe_data['prix'])}")
                    st.markdown(f"**Puissance:** {pompe_data['puissance']}W")
                    
                    if st.button("➕ Ajouter cette pompe"):
                        st.session_state.selected_components['pompe'] = {
                            'type': pompe_data['nom'],
                            'prix': pompe_data['prix'],
                            'puissance': pompe_data['puissance']
                        }
                        st.success("Pompe ajoutée!")
            
            with col2:
                st.markdown("##### Régulateurs de charge")
                regulateur_selection = st.selectbox(
                    "Sélectionnez un régulateur",
                    [""] + [r['nom'] for r in PRODUCT_DATABASE['regulateurs']],
                    format_func=lambda x: x if x else "Aucun régulateur"
                )
                
                if regulateur_selection:
                    regulateur_data = next(r for r in PRODUCT_DATABASE['regulateurs'] if r['nom'] == regulateur_selection)
                    st.markdown(f"**Prix:** {format_prix(regulateur_data['prix'])}")
                    st.markdown(f"**Type:** {regulateur_data['type']}")
                    
                    if st.button("➕ Ajouter ce régulateur"):
                        st.session_state.selected_components['regulateur'] = {
                            'type': regulateur_data['nom'],
                            'prix': regulateur_data['prix']
                        }
                        st.success("Régulateur ajouté!")

# Section 3: Génération du devis
elif menu == "💰 Génération Devis":
    st.markdown('<div class="section-header">3. Génération du devis détaillé</div>', unsafe_allow_html=True)
    
    if not st.session_state.selected_components:
        st.warning("⚠️ Veuillez d'abord configurer votre système dans l'onglet 'Configuration Système'")
    else:
        # Calcul des totaux
        cout_total = 0
        details_couts = []
        
        # Récupération de la configuration
        if 'panneaux' in st.session_state.selected_components:
            panneaux = st.session_state.selected_components['panneaux']
            cout_panneaux = panneaux['quantite'] * panneaux['prix_unitaire']
            cout_total += cout_panneaux
            details_couts.append(("☀️ Panneaux solaires", panneaux['quantite'], format_prix(panneaux['prix_unitaire']), format_prix(cout_panneaux)))
        
        if 'batteries' in st.session_state.selected_components:
            batteries = st.session_state.selected_components['batteries']
            cout_batteries = batteries['quantite'] * batteries['prix_unitaire']
            cout_total += cout_batteries
            details_couts.append(("🔋 Batteries", batteries['quantite'], format_prix(batteries['prix_unitaire']), format_prix(cout_batteries)))
        
        if 'convertisseur' in st.session_state.selected_components:
            convertisseur = st.session_state.selected_components['convertisseur']
            cout_total += convertisseur['prix']
            details_couts.append(("🔌 Convertisseur hybride", 1, format_prix(convertisseur['prix']), format_prix(convertisseur['prix'])))
        
        # Autres équipements
        autres_couts = 0
        autres_details = []
        
        if 'pompe' in st.session_state.selected_components:
            pompe = st.session_state.selected_components['pompe']
            cout_total += pompe['prix']
            autres_couts += pompe['prix']
            autres_details.append(f"Pompe solaire: {format_prix(pompe['prix'])}")
        
        if 'regulateur' in st.session_state.selected_components:
            regulateur = st.session_state.selected_components['regulateur']
            cout_total += regulateur['prix']
            autres_couts += regulateur['prix']
            autres_details.append(f"Régulateur: {format_prix(regulateur['prix'])}")
        
        # Coûts d'installation et accessoires
        cout_installation = cout_total * 0.15  # 15% pour installation
        cout_accessoires = 300000  # Câbles, protections, etc.
        
        cout_total += cout_installation + cout_accessoires
        
        # TVA
        tva = cout_total * 0.20
        total_ttc = cout_total + tva
        
        # Affichage du devis
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("### 📋 DEVIS DÉTAILLÉ")
            st.markdown(f"**Date:** {datetime.now().strftime('%d/%m/%Y')}")
            st.markdown(f"**Référence:** TS-{datetime.now().strftime('%Y%m%d')}-001")
            st.markdown("---")
            
            st.markdown("#### Composants principaux")
            for nom, qte, prix_unitaire, total in details_couts:
                st.markdown(f"**{nom}**")
                st.markdown(f"- Quantité: {qte}")
                st.markdown(f"- Prix unitaire: {prix_unitaire}")
                st.markdown(f"- Sous-total: **{total}**")
                st.markdown("")
            
            if autres_details:
                st.markdown("#### Autres équipements")
                for detail in autres_details:
                    st.markdown(f"- {detail}")
            
            st.markdown("#### Frais supplémentaires")
            st.markdown(f"- Installation: {format_prix(cout_installation)}")
            st.markdown(f"- Accessoires (câbles, protections): {format_prix(cout_accessoires)}")
            st.markdown("---")
            
            st.markdown("#### RÉCAPITULATIF FINANCIER")
            st.markdown(f"**Total HT:** {format_prix(cout_total - tva)}")
            st.markdown(f"**TVA (20%):** {format_prix(tva)}")
            st.markdown(f"### **TOTAL TTC:** {format_prix(total_ttc)}")
            
            st.markdown("---")
            st.markdown(f"**Validité du devis:** {(datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')}")
            st.markdown("**Conditions de paiement:** 50% à la commande, 50% à la livraison")
            st.markdown("**Délai de livraison:** 15 jours ouvrables")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📊 Synthèse technique")
            
            if 'panneaux' in st.session_state.selected_components:
                config = st.session_state.selected_components['panneaux'].get('config', {})
                if config:
                    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                    st.markdown('<div class="metric-label">Énergie quotidienne</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{config.get("energie_totale", 0):,.0f} Wh</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                    st.markdown('<div class="metric-label">Nombre de panneaux</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{config.get("n_panneaux", 0)}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                    st.markdown('<div class="metric-label">Nombre de batteries</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{config.get("n_batteries", 0)}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    if 'convertisseur' in st.session_state.selected_components:
                        conv = st.session_state.selected_components['convertisseur']
                        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                        st.markdown('<div class="metric-label">Puissance convertisseur</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="metric-value">{conv["puissance"]:,} W</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            
            # Bouton de génération
            if st.button("📄 Générer le PDF du devis", use_container_width=True):
                # Préparer les données pour l'export
                devis_complet = {
                    "date": datetime.now().strftime('%d/%m/%Y'),
                    "reference": f"TS-{datetime.now().strftime('%Y%m%d')}-001",
                    "composants": details_couts,
                    "autres_equipements": autres_details,
                    "frais": {
                        "installation": format_prix(cout_installation),
                        "accessoires": format_prix(cout_accessoires)
                    },
                    "totaux": {
                        "ht": format_prix(cout_total - tva),
                        "tva": format_prix(tva),
                        "ttc": format_prix(total_ttc)
                    }
                }
                
                # Convertir en JSON pour l'export
                devis_json = json.dumps(devis_complet, indent=2, ensure_ascii=False)
                
                st.download_button(
                    label="⬇️ Télécharger le devis (JSON)",
                    data=devis_json,
                    file_name=f"devis_tsena_solaire_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                st.success("✅ Devis généré avec succès! Vous pouvez le télécharger ci-dessus.")

# Section 4: Visualisation complète
elif menu == "📊 Visualisation Complète":
    st.markdown('<div class="section-header">4. Visualisation complète du projet</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### 📈 Vue d'ensemble du système")
        
        if not st.session_state.materiels and not st.session_state.selected_components:
            st.info("ℹ️ Aucune donnée à afficher. Commencez par configurer votre système.")
        else:
            # Affichage de la consommation
            if st.session_state.materiels:
                st.markdown("##### Consommation électrique")
                df_materiels = pd.DataFrame(st.session_state.materiels)
                
                # Graphique de consommation
                import plotly.express as px
                
                fig = px.bar(df_materiels, 
                           x='Nom', 
                           y=['Energie jour (Wh)', 'Energie nuit (Wh)'],
                           title='Consommation par équipement',
                           barmode='group',
                           labels={'value': 'Énergie (Wh)', 'variable': 'Période'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Affichage de la configuration
            if st.session_state.selected_components:
                st.markdown("##### Configuration du système")
                
                config_data = []
                if 'panneaux' in st.session_state.selected_components:
                    p = st.session_state.selected_components['panneaux']
                    config_data.append({"Composant": "Panneaux", "Détail": f"{p['quantite']} × {p['type']}"})
                
                if 'batteries' in st.session_state.selected_components:
                    b = st.session_state.selected_components['batteries']
                    config_data.append({"Composant": "Batteries", "Détail": f"{b['quantite']} × {b['type']}"})
                
                if 'convertisseur' in st.session_state.selected_components:
                    c = st.session_state.selected_components['convertisseur']
                    config_data.append({"Composant": "Convertisseur", "Détail": c['type']})
                
                if config_data:
                    df_config = pd.DataFrame(config_data)
                    st.dataframe(df_config, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 📋 Résumé technique")
        
        if st.session_state.selected_components:
            # Calcul des indicateurs techniques
            indicateurs = []
            
            if 'panneaux' in st.session_state.selected_components:
                p = st.session_state.selected_components['panneaux']
                if 'config' in p:
                    config = p['config']
                    indicateurs.append(("☀️ Production estimée", f"{config.get('energie_avec_rendement', 0):,.0f} Wh/jour"))
                    indicateurs.append(("🔋 Autonomie", f"{autonomie} jours"))
                    indicateurs.append(("⚡ Rendement système", f"{rendement}%"))
            
            if 'batteries' in st.session_state.selected_components:
                b = st.session_state.selected_components['batteries']
                if 'energie' in b:
                    energie_totale_batteries = b['quantite'] * b['energie']
                    indicateurs.append(("🔋 Capacité totale", f"{energie_totale_batteries:,.1f} kWh"))
            
            for label, valeur in indicateurs:
                st.markdown(f"**{label}:** {valeur}")
            
            # Avantages du système
            st.markdown("##### ✅ Avantages du système")
            avantages = [
                "✓ Énergie renouvelable et gratuite",
                "✓ Indépendance énergétique",
                "✓ Réduction des factures d'électricité",
                "✓ Faible entretien",
                "✓ Durée de vie longue",
                "✓ Respect de l'environnement"
            ]
            
            for avantage in avantages:
                st.markdown(f"<div style='color: var(--accent);'>{avantage}</div>", unsafe_allow_html=True)
        
        # Bouton pour tout réinitialiser
        st.markdown("---")
        if st.button("🔄 Nouveau projet", use_container_width=True, type="secondary"):
            st.session_state.materiels = []
            st.session_state.selected_components = {}
            st.session_state.devis_data = {}
            st.success("Nouveau projet créé! Vous pouvez recommencer la configuration.")
            st.rerun()

# Pied de page
st.markdown("""
<div class="footer">
    <p><strong>☀️ TSENA SOLAIRE MALAGASY</strong> · Votre expert en énergie solaire à Madagascar</p>
    <p>📞 Contact: +261 34 00 000 00 | ✉️ contact@tsenasolaire.mg | 🌐 www.tsenasolaire.mg</p>
    <p>📍 Antananarivo, Madagascar · Développé par l'équipe IT Tsena Solaire</p>
    <p style="font-size: 0.8em; margin-top: 10px;">© 2024 Tsena Solaire Malagasy · Tous droits réservés</p>
</div>
""", unsafe_allow_html=True)
