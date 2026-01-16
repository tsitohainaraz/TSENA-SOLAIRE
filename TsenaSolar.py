import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import base64
from io import BytesIO
import pdfkit
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Tsena Solaire Malagasy",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour mobile et design malgache
st.markdown("""
<style>
    /* Style général avec couleurs de Madagascar */
    :root {
        --vert-malgache: #00843D;
        --rouge-malgache: #FC3D32;
        --blanc-malgache: #FFFFFF;
        --jaune-soleil: #FFD700;
        --terre-malgache: #8B4513;
        --ciel-malgache: #87CEEB;
    }
    
    /* Design responsive pour mobile */
    @media only screen and (max-width: 768px) {
        .main-title { font-size: 1.8rem !important; }
        .section-title { font-size: 1.3rem !important; }
        .metric-card { padding: 10px !important; margin: 5px 0 !important; }
        .stButton > button { font-size: 0.9rem !important; padding: 8px 15px !important; }
        .product-grid { grid-template-columns: repeat(1, 1fr) !important; }
    }
    
    /* Style principal */
    .main-title {
        background: linear-gradient(90deg, var(--vert-malgache), var(--rouge-malgache));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 10px;
        font-family: 'Arial', sans-serif;
    }
    
    .sub-title {
        color: var(--terre-malgache);
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 30px;
        font-style: italic;
    }
    
    /* Sections */
    .section-title {
        background-color: var(--vert-malgache);
        color: white;
        padding: 12px 20px;
        border-radius: 10px 10px 0 0;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 30px;
        position: relative;
    }
    
    .section-title:after {
        content: "🌍";
        position: absolute;
        right: 20px;
    }
    
    /* Cartes de produits */
    .product-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 2px solid var(--vert-malgache);
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 132, 61, 0.1);
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 132, 61, 0.2);
        border-color: var(--rouge-malgache);
    }
    
    .price-tag {
        background: linear-gradient(135deg, var(--rouge-malgache), #FF6B6B);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 5px 0;
        font-size: 1.1em;
    }
    
    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, var(--vert-malgache), #00A86B);
        color: white;
        font-weight: bold;
        padding: 12px 25px;
        border-radius: 25px;
        border: none;
        font-size: 1em;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 132, 61, 0.3);
    }
    
    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 20px rgba(0, 132, 61, 0.4);
        background: linear-gradient(135deg, #00A86B, var(--vert-malgache));
    }
    
    /* Bouton WhatsApp spécifique */
    .whatsapp-btn {
        background: linear-gradient(135deg, #25D366, #128C7E) !important;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* Cartes métriques */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 2px solid var(--ciel-malgache);
        margin: 10px;
        box-shadow: 0 4px 12px rgba(135, 206, 235, 0.2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--vert-malgache);
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--terre-malgache);
        opacity: 0.8;
    }
    
    /* Grille de produits */
    .product-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        background: linear-gradient(90deg, var(--vert-malgache), var(--rouge-malgache));
        color: white;
        padding: 20px;
        margin-top: 40px;
        border-radius: 15px 15px 0 0;
    }
    
    /* Badges */
    .eco-badge {
        background-color: var(--vert-malgache);
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        display: inline-block;
        margin: 5px 5px 5px 0;
    }
    
    /* Responsive */
    .mobile-hidden {
        display: block;
    }
    
    @media only screen and (max-width: 768px) {
        .mobile-hidden {
            display: none;
        }
    }
    
    /* Images décoratives */
    .deco-leaf {
        color: var(--vert-malgache);
        font-size: 1.2em;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des données de session
if 'materiels' not in st.session_state:
    st.session_state.materiels = []
if 'selected_config' not in st.session_state:
    st.session_state.selected_config = {}
if 'devis' not in st.session_state:
    st.session_state.devis = {}

# Base de données complète des produits
PRODUCTS_DB = {
    "convertisseurs": [
        {"id": 1, "nom": "Onduleur 24V/3KW", "puissance": 3000, "tension": 24, "prix": 1400000, "marque": "SRNE", "type": "Hybride", "mppt": "1x40A", "efficiency": "93%"},
        {"id": 2, "nom": "Onduleur 48V/5KW", "puissance": 5000, "tension": 48, "prix": 2400000, "marque": "HAISIC", "type": "Hybride", "mppt": "1x22A", "efficiency": "95%"},
        {"id": 3, "nom": "Onduleur 48V/10KW", "puissance": 10000, "tension": 48, "prix": 6000000, "marque": "HAISIC", "type": "Hybride", "mppt": "2x22A", "efficiency": "96%"},
        {"id": 4, "nom": "Onduleur 48V/12KW H3", "puissance": 12000, "tension": 48, "prix": 6600000, "marque": "SRNE", "type": "Hybride", "mppt": "2xMPPT", "efficiency": "96%"},
        {"id": 5, "nom": "Onduleur 48V/6KW IP65", "puissance": 6000, "tension": 48, "prix": 3500000, "marque": "HONG FENG", "type": "Hybride", "mppt": "1xMPPT", "efficiency": "94%"},
        {"id": 6, "nom": "Onduleur 48V/12KW IP65", "puissance": 12000, "tension": 48, "prix": 8700000, "marque": "SRNE", "type": "Hybride", "mppt": "2xMPPT", "efficiency": "96%"}
    ],
    
    "batteries": [
        {"id": 7, "nom": "Batterie Lithium 25.6V/100Ah", "tension": 25.6, "capacite": 100, "energie": 2.56, "prix": 2600000, "marque": "HAISIC", "cycles": 6000, "poids": "25kg"},
        {"id": 8, "nom": "Batterie Lithium 51.2V/100Ah", "tension": 51.2, "capacite": 100, "energie": 5.12, "prix": 5000000, "marque": "SRNE", "cycles": 6000, "poids": "45kg"},
        {"id": 9, "nom": "Batterie Lithium 51.2V/200Ah", "tension": 51.2, "capacite": 200, "energie": 10.24, "prix": 9000000, "marque": "HAISIC", "cycles": 6000, "poids": "85kg"},
        {"id": 10, "nom": "Batterie Lithium 51.2V/316Ah", "tension": 51.2, "capacite": 316, "energie": 16.49, "prix": 11500000, "marque": "CHINA ESS", "cycles": 6000, "poids": "120kg"}
    ],
    
    "panneaux": [
        {"id": "P110", "puissance": 110, "prix": 130000, "type": "Monocristallin", "efficiency": "21%", "dimensions": "1480×670×35mm"},
        {"id": "P210", "puissance": 210, "prix": 180000, "type": "Monocristallin", "efficiency": "21.5%", "dimensions": "1650×992×35mm"},
        {"id": "P550", "puissance": 550, "prix": 500000, "type": "Monocristallin", "efficiency": "22.1%", "dimensions": "2278×1134×35mm"},
        {"id": "P580", "puissance": 580, "prix": 600000, "type": "Monocristallin", "efficiency": "22.3%", "dimensions": "2278×1134×35mm"},
        {"id": "P60", "puissance": 60, "prix": 80000, "type": "Polycristallin", "efficiency": "18%", "dimensions": "670×540×30mm"},
        {"id": "P80", "puissance": 80, "prix": 100000, "type": "Polycristallin", "efficiency": "18.5%", "dimensions": "810×540×30mm"}
    ],
    
    "pompes": [
        {"id": 13, "nom": "Pompe DC 750W", "puissance": 750, "prix": 720000, "type": "DC", "debit": "95m³/h", "hauteur": "18m"},
        {"id": 14, "nom": "Pompe DC 1500W", "puissance": 1500, "prix": 870000, "type": "DC", "debit": "165m³/h", "hauteur": "110m"},
        {"id": 15, "nom": "Pompe DC 1100W", "puissance": 1100, "prix": 830000, "type": "DC", "debit": "125m³/h", "hauteur": "110m"},
        {"id": 16, "nom": "Pompe DC 1100W 4DSP6", "puissance": 1100, "prix": 840000, "type": "DC", "debit": "95m³/h", "hauteur": "110m"},
        {"id": 17, "nom": "Pompe DC 1500W 4DSP6", "puissance": 1500, "prix": 850000, "type": "DC", "debit": "135m³/h", "hauteur": "110m"}
    ],
    
    "eclairage": [
        {"id": 11, "nom": "Lampadaire Solaire BL-3000", "prix": 200000, "puissance": "30W LED", "autonomie": "12h", "detection": "Mouvement"},
        {"id": 12, "nom": "Lampadaire Solaire YL-30P", "prix": 270000, "puissance": "250W LED", "autonomie": "10h", "detection": "Mouvement"}
    ],
    
    "regulateurs": [
        {"id": 27, "nom": "Régulateur PWM 20A", "courant": 20, "prix": 80000, "type": "PWM", "tension": "12/24V"},
        {"id": 28, "nom": "Régulateur PWM 60A", "courant": 60, "prix": 190000, "type": "PWM", "tension": "12/24V"},
        {"id": 29, "nom": "Régulateur MPPT 20A", "courant": 20, "prix": 240000, "type": "MPPT", "tension": "12/24V"},
        {"id": 30, "nom": "Régulateur MPPT 60A", "courant": 60, "prix": 650000, "type": "MPPT", "tension": "12/24/48V"}
    ]
}

# Fonctions utilitaires
def format_prix(prix):
    return f"{prix:,.0f} Ar".replace(",", " ")

def calculate_optimal_config(energie_totale, puissance_max, params):
    """Calcule la configuration optimale automatique"""
    # Calcul énergie nécessaire avec pertes
    energie_necessaire = energie_totale / params['rendement']
    
    # Sélection optimale des panneaux
    panneau_selection = None
    n_panneaux_optimal = float('inf')
    
    for panneau in PRODUCTS_DB['panneaux']:
        energie_panneau_jour = panneau['puissance'] * params['heures_soleil']
        n_panneaux = max(1, np.ceil(energie_necessaire / energie_panneau_jour))
        
        if n_panneaux < n_panneaux_optimal:
            n_panneaux_optimal = n_panneaux
            panneau_selection = panneau
    
    # Sélection de la batterie
    capacite_necessaire_wh = (energie_totale * params['autonomie']) / params['profondeur_decharge']
    batterie_selection = None
    
    for batterie in PRODUCTS_DB['batteries']:
        capacite_wh = batterie['energie'] * 1000
        if capacite_wh >= capacite_necessaire_wh * 0.8:  # 80% de la capacité nécessaire
            batterie_selection = batterie
            break
    
    if not batterie_selection:
        batterie_selection = max(PRODUCTS_DB['batteries'], key=lambda x: x['energie'])
    
    n_batteries = max(1, np.ceil(capacite_necessaire_wh / (batterie_selection['energie'] * 1000)))
    
    # Sélection du convertisseur
    puissance_convertisseur = puissance_max * params['marge_securite']
    convertisseur_selection = None
    
    for conv in sorted(PRODUCTS_DB['convertisseurs'], key=lambda x: x['puissance']):
        if conv['puissance'] >= puissance_convertisseur:
            convertisseur_selection = conv
            break
    
    if not convertisseur_selection:
        convertisseur_selection = max(PRODUCTS_DB['convertisseurs'], key=lambda x: x['puissance'])
    
    return {
        'panneaux': panneau_selection,
        'n_panneaux': int(n_panneaux_optimal),
        'batterie': batterie_selection,
        'n_batteries': int(n_batteries),
        'convertisseur': convertisseur_selection,
        'energie_totale': energie_totale,
        'energie_necessaire': energie_necessaire,
        'capacite_batterie_wh': capacite_necessaire_wh
    }

def generate_pdf_devis(devis_data):
    """Génère un PDF du devis"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ text-align: center; color: #00843D; border-bottom: 3px solid #FC3D32; padding-bottom: 20px; }}
            .title {{ font-size: 28px; font-weight: bold; }}
            .subtitle {{ color: #666; }}
            .section {{ margin-top: 30px; }}
            .section-title {{ background-color: #00843D; color: white; padding: 10px; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .total {{ font-size: 20px; font-weight: bold; color: #00843D; }}
            .footer {{ margin-top: 50px; text-align: center; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">☀️ TSENA SOLAIRE MALAGASY</div>
            <div class="subtitle">Devis N° {devis_data.get('reference', 'TS-2024-001')}</div>
            <div>Date: {datetime.now().strftime('%d/%m/%Y')}</div>
        </div>
        
        <div class="section">
            <div class="section-title">Configuration du système</div>
            <table>
                <tr>
                    <th>Composant</th>
                    <th>Description</th>
                    <th>Quantité</th>
                    <th>Prix unitaire</th>
                    <th>Total</th>
                </tr>
    """
    
    total = 0
    for item in devis_data.get('items', []):
        html_content += f"""
                <tr>
                    <td>{item['type']}</td>
                    <td>{item.get('description', '')}</td>
                    <td>{item['quantite']}</td>
                    <td>{format_prix(item['prix_unitaire'])}</td>
                    <td>{format_prix(item['total'])}</td>
                </tr>
        """
        total += item['total']
    
    html_content += f"""
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">Récapitulatif financier</div>
            <p>Sous-total: {format_prix(total)}</p>
            <p>Installation: {format_prix(devis_data.get('installation', 0))}</p>
            <p>Accessoires: {format_prix(devis_data.get('accessoires', 0))}</p>
            <p>TVA (20%): {format_prix(devis_data.get('tva', 0))}</p>
            <p class="total">TOTAL TTC: {format_prix(devis_data.get('total_ttc', 0))}</p>
        </div>
        
        <div class="footer">
            <p>Tsena Solaire Malagasy - L'énergie verte pour tous</p>
            <p>Contact: +261 38 81 030 83 | Email: info@tsenasolaire.mg</p>
            <p>Valable 30 jours à partir de la date d'émission</p>
        </div>
    </body>
    </html>
    """
    
    try:
        # Utiliser pdfkit si disponible, sinon retourner HTML
        import pdfkit
        pdf = pdfkit.from_string(html_content, False)
        return pdf
    except:
        # Retourner le HTML si pdfkit n'est pas disponible
        return html_content.encode()

# Interface principale
st.markdown('<h1 class="main-title">☀️ TSENA SOLAIRE MALAGASY</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Énergie verte pour chaque famille malgache - Miara-miroborobo amin\'ny angovo maitso</p>', unsafe_allow_html=True)

# Bouton WhatsApp flottant
st.markdown("""
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
    <a href="https://wa.me/261388103083?text=Bonjour,%20je%20souhaite%20discuter%20de%20mon%20devis%20solaire" target="_blank">
        <button style="background: #25D366; color: white; border: none; padding: 15px 20px; border-radius: 50px; font-weight: bold; box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4); display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.5em;">💬</span> Discuter avec expert
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

# Onglets principaux
tabs = st.tabs(["🏠 Accueil", "📊 Calcul Conso", "🛒 Produits", "⚡ Configuration", "💰 Devis"])

# Tab 1: Accueil
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🌿 Bienvenue à Tsena Solaire Malagasy
        
        **L'énergie solaire accessible à tous les Malagasy**, où que vous soyez !
        
        ### 💚 Pourquoi choisir l'énergie solaire ?
        
        ✓ **Indépendance énergétique** - Plus de coupures d'électricité  
        ✓ **Économies durables** - Réduction de vos factures  
        ✓ **Respect de l'environnement** - Énergie 100% renouvelable  
        ✓ **Installation rapide** - Fonctionnel en quelques jours  
        ✓ **Maintenance simple** - Durabilité garantie  
        
        ### 📱 Comment ça marche ?
        
        1. **Calculez** votre consommation  
        2. **Visualisez** nos produits  
        3. **Configurez** votre système  
        4. **Recevez** votre devis instantané  
        5. **Discutez** avec nos experts  
        
        """)
        
        # Statistiques
        st.markdown("### 📈 Notre impact")
        cols_stats = st.columns(4)
        with cols_stats[0]:
            st.metric("👥 Familles équipées", "500+")
        with cols_stats[1]:
            st.metric("☀️ Panneaux installés", "2,500+")
        with cols_stats[2]:
            st.metric("💡 kWh économisés", "1.2M+")
        with cols_stats[3]:
            st.metric("🌿 CO₂ évité (tonnes)", "850+")
    
    with col2:
        # Image/Illustration
        st.markdown("### 🌍 Couverture nationale")
        regions = {
            "Analamanga": 35,
            "Atsinanana": 22,
            "Vakinankaratra": 18,
            "Sava": 15,
            "Boeny": 10
        }
        
        fig = px.pie(
            values=list(regions.values()),
            names=list(regions.keys()),
            title="Installations par région",
            color_discrete_sequence=['#00843D', '#00A86B', '#FC3D32', '#FF6B6B', '#FFD700']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Témoignage
        st.markdown("""
        <div style="background: #f0f8f0; padding: 15px; border-radius: 10px; border-left: 5px solid #00843D; margin-top: 20px;">
        <i>"Avec Tsena Solaire, ma famille a enfin de l'électricité fiable. Les enfants peuvent étudier le soir et nous regardons la télévision ensemble."</i>
        <br><br>
        <b>- Rakoto Jean, Ankazobe</b>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Calcul de consommation
with tabs[1]:
    st.markdown('<div class="section-title">📊 Calcul de votre consommation</div>', unsafe_allow_html=True)
    
    # Interface de saisie simplifiée
    with st.expander("➕ Ajouter un équipement", expanded=True):
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            nom = st.text_input("Équipement", placeholder="Ex: Réfrigérateur, TV, Lampe...")
        with col2:
            puissance = st.number_input("Puissance (W)", min_value=1, value=100)
        with col3:
            quantite = st.number_input("Qté", min_value=1, value=1)
        with col4:
            heures = st.number_input("Heures/jour", min_value=0.0, max_value=24.0, value=8.0)
        
        if st.button("Ajouter cet équipement", type="primary"):
            if nom:
                energie = puissance * quantite * heures
                st.session_state.materiels.append({
                    "Équipement": nom,
                    "Puissance (W)": puissance,
                    "Quantité": quantite,
                    "Heures/jour": heures,
                    "Énergie (Wh/jour)": energie
                })
                st.success(f"✅ {nom} ajouté!")
                st.rerun()
    
    # Équipements prédéfinis
    st.markdown("### 💡 Équipements courants")
    equipements_predefinis = {
        "Ampoule LED 10W": {"puissance": 10, "heures": 5},
        "Réfrigérateur 150W": {"puissance": 150, "heures": 24},
        "TV LED 50W": {"puissance": 50, "heures": 4},
        "Ordinateur 100W": {"puissance": 100, "heures": 6},
        "Ventilateur 60W": {"puissance": 60, "heures": 8},
        "Radio 20W": {"puissance": 20, "heures": 3},
        "Chargeur téléphone 5W": {"puissance": 5, "heures": 2}
    }
    
    cols = st.columns(4)
    for idx, (nom_eq, details) in enumerate(equipements_predefinis.items()):
        with cols[idx % 4]:
            if st.button(f"➕ {nom_eq}", key=f"eq_{idx}"):
                energie = details["puissance"] * 1 * details["heures"]
                st.session_state.materiels.append({
                    "Équipement": nom_eq,
                    "Puissance (W)": details["puissance"],
                    "Quantité": 1,
                    "Heures/jour": details["heures"],
                    "Énergie (Wh/jour)": energie
                })
                st.rerun()
    
    # Affichage des équipements
    if st.session_state.materiels:
        st.markdown("### 📋 Votre consommation")
        
        df_conso = pd.DataFrame(st.session_state.materiels)
        total_energie = df_conso["Énergie (Wh/jour)"].sum()
        total_puissance = (df_conso["Puissance (W)"] * df_conso["Quantité"]).sum()
        
        # Graphique
        fig = px.bar(
            df_conso,
            x="Équipement",
            y="Énergie (Wh/jour)",
            color="Équipement",
            title=f"Consommation totale: {total_energie:,.0f} Wh/jour",
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Métriques
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⚡ Énergie quotidienne", f"{total_energie:,.0f} Wh")
        with col2:
            st.metric("🔌 Puissance totale", f"{total_puissance:,.0f} W")
        with col3:
            st.metric("📊 Nombre d'équipements", len(st.session_state.materiels))
        
        if st.button("🗑️ Réinitialiser la liste", type="secondary"):
            st.session_state.materiels = []
            st.rerun()
    else:
        st.info("👈 Commencez par ajouter vos équipements ci-dessus")

# Tab 3: Visualisation des produits
with tabs[2]:
    st.markdown('<div class="section-title">🛒 Notre catalogue de produits</div>', unsafe_allow_html=True)
    
    # Filtres
    col_filtre1, col_filtre2 = st.columns(2)
    with col_filtre1:
        categorie = st.selectbox(
            "Catégorie",
            ["Tous", "Panneaux solaires", "Batteries", "Convertisseurs", "Pompes", "Éclairage", "Régulateurs"]
        )
    with col_filtre2:
        prix_max = st.slider("Prix maximum (Ar)", 50000, 15000000, 5000000, 50000)
    
    # Affichage des produits
    categories_map = {
        "Panneaux solaires": "panneaux",
        "Batteries": "batteries",
        "Convertisseurs": "convertisseurs",
        "Pompes": "pompes",
        "Éclairage": "eclairage",
        "Régulateurs": "regulateurs"
    }
    
    if categorie == "Tous":
        products_to_show = []
        for cat in categories_map.values():
            products_to_show.extend(PRODUCTS_DB[cat])
    else:
        products_to_show = PRODUCTS_DB[categories_map[categorie]]
    
    # Filtrer par prix
    products_to_show = [p for p in products_to_show if p['prix'] <= prix_max]
    
    # Affichage en grille
    st.markdown(f"### 📦 {len(products_to_show)} produits disponibles")
    
    cols = st.columns(2)
    for idx, produit in enumerate(products_to_show):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <h4>{produit['nom']}</h4>
                    <div class="price-tag">{format_prix(produit['prix'])}</div>
                    <hr>
                """, unsafe_allow_html=True)
                
                # Informations spécifiques par catégorie
                if 'puissance' in produit:
                    st.markdown(f"**Puissance:** {produit['puissance']}W")
                if 'capacite' in produit:
                    st.markdown(f"**Capacité:** {produit['capacite']}Ah")
                if 'energie' in produit:
                    st.markdown(f"**Énergie:** {produit['energie']}kWh")
                if 'marque' in produit:
                    st.markdown(f"**Marque:** {produit['marque']}")
                if 'type' in produit:
                    st.markdown(f"**Type:** {produit['type']}")
                if 'efficiency' in produit:
                    st.markdown(f"**Efficacité:** {produit['efficiency']}")
                
                # Bouton d'ajout rapide
                if st.button(f"➕ Ajouter au devis", key=f"add_{idx}"):
                    if 'panneaux' in produit.values():
                        st.session_state.selected_config['panneaux'] = produit
                    elif 'batterie' in produit.values():
                        st.session_state.selected_config['batterie'] = produit
                    elif 'convertisseur' in produit.values():
                        st.session_state.selected_config['convertisseur'] = produit
                    st.success(f"{produit['nom']} ajouté à la configuration!")
                
                st.markdown("</div>", unsafe_allow_html=True)

# Tab 4: Configuration
with tabs[3]:
    st.markdown('<div class="section-title">⚡ Configuration automatique</div>', unsafe_allow_html=True)
    
    if not st.session_state.materiels:
        st.warning("Veuillez d'abord calculer votre consommation dans l'onglet 'Calcul Conso'")
    else:
        # Calcul des totaux
        df_conso = pd.DataFrame(st.session_state.materiels)
        energie_totale = df_conso["Énergie (Wh/jour)"].sum()
        puissance_max = (df_conso["Puissance (W)"] * df_conso["Quantité"]).max()
        
        # Paramètres
        with st.expander("⚙️ Paramètres techniques", expanded=True):
            col_param1, col_param2 = st.columns(2)
            with col_param1:
                autonomie = st.slider("Autonomie souhaitée (jours)", 1, 5, 2)
                profondeur_decharge = st.select_slider(
                    "Profondeur de décharge",
                    options=[0.5, 0.6, 0.7, 0.8, 0.9],
                    value=0.8,
                    format_func=lambda x: f"{int(x*100)}%"
                )
            with col_param2:
                heures_soleil = st.slider("Heures d'ensoleillement/jour", 3.0, 8.0, 5.5, 0.5)
                rendement = st.slider("Rendement système", 70, 95, 85)
        
        # Bouton de calcul
        if st.button("🔍 Calculer la configuration optimale", type="primary", use_container_width=True):
            params = {
                'rendement': rendement / 100,
                'autonomie': autonomie,
                'profondeur_decharge': profondeur_decharge,
                'heures_soleil': heures_soleil,
                'marge_securite': 1.25
            }
            
            config = calculate_optimal_config(energie_totale, puissance_max, params)
            st.session_state.selected_config = config
            
            st.success("✅ Configuration optimale calculée!")
        
        # Affichage de la configuration
        if st.session_state.selected_config:
            config = st.session_state.selected_config
            
            st.markdown("### 🎯 Configuration recommandée")
            
            # Métriques principales
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("☀️ Panneaux", f"{config.get('n_panneaux', 0)} unités")
            with col2:
                st.metric("🔋 Batteries", f"{config.get('n_batteries', 0)} unités")
            with col3:
                if 'convertisseur' in config:
                    st.metric("🔌 Convertisseur", f"{config['convertisseur']['puissance']:,}W")
            with col4:
                st.metric("💰 Budget estimé", format_prix(
                    config.get('panneaux', {}).get('prix', 0) * config.get('n_panneaux', 0) +
                    config.get('batterie', {}).get('prix', 0) * config.get('n_batteries', 0) +
                    config.get('convertisseur', {}).get('prix', 0)
                ))
            
            # Détails des composants
            st.markdown("#### 📋 Détail des composants")
            
            if 'panneaux' in config:
                panneau = config['panneaux']
                col_p1, col_p2, col_p3 = st.columns([2, 1, 1])
                with col_p1:
                    st.markdown(f"**{panneau['puissance']}W {panneau['type']}**")
                with col_p2:
                    st.markdown(f"**Quantité:** {config['n_panneaux']}")
                with col_p3:
                    st.markdown(f"**Prix:** {format_prix(panneau['prix'])}")
            
            if 'batterie' in config:
                batterie = config['batterie']
                col_b1, col_b2, col_b3 = st.columns([2, 1, 1])
                with col_b1:
                    st.markdown(f"**{batterie['nom']}**")
                with col_b2:
                    st.markdown(f"**Quantité:** {config['n_batteries']}")
                with col_b3:
                    st.markdown(f"**Prix:** {format_prix(batterie['prix'])}")
            
            if 'convertisseur' in config:
                convertisseur = config['convertisseur']
                col_c1, col_c2 = st.columns([2, 1])
                with col_c1:
                    st.markdown(f"**{convertisseur['nom']}**")
                with col_c2:
                    st.markdown(f"**Prix:** {format_prix(convertisseur['prix'])}")
            
            # Graphique de répartition
            st.markdown("#### 📊 Répartition du coût")
            
            if all(k in config for k in ['panneaux', 'batterie', 'convertisseur']):
                cout_panneaux = config['panneaux']['prix'] * config['n_panneaux']
                cout_batteries = config['batterie']['prix'] * config['n_batteries']
                cout_convertisseur = config['convertisseur']['prix']
                
                fig = go.Figure(data=[go.Pie(
                    labels=['Panneaux', 'Batteries', 'Convertisseur'],
                    values=[cout_panneaux, cout_batteries, cout_convertisseur],
                    hole=.3,
                    marker_colors=['#00843D', '#FC3D32', '#FFD700']
                )])
                fig.update_layout(title="Répartition des coûts")
                st.plotly_chart(fig, use_container_width=True)

# Tab 5: Devis
with tabs[4]:
    st.markdown('<div class="section-title">💰 Votre devis détaillé</div>', unsafe_allow_html=True)
    
    if not st.session_state.selected_config:
        st.info("Veuillez d'abord configurer votre système dans l'onglet 'Configuration'")
    else:
        config = st.session_state.selected_config
        
        # Calcul du devis
        if all(k in config for k in ['panneaux', 'batterie', 'convertisseur']):
            # Coûts directs
            cout_panneaux = config['panneaux']['prix'] * config['n_panneaux']
            cout_batteries = config['batterie']['prix'] * config['n_batteries']
            cout_convertisseur = config['convertisseur']['prix']
            
            # Frais additionnels
            cout_installation = (cout_panneaux + cout_batteries + cout_convertisseur) * 0.15
            cout_accessoires = 250000
            cout_transport = 150000
            
            sous_total = cout_panneaux + cout_batteries + cout_convertisseur + cout_installation + cout_accessoires + cout_transport
            tva = sous_total * 0.20
            total_ttc = sous_total + tva
            
            # Stocker le devis
            devis_data = {
                'reference': f"TS-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.materiels)}",
                'date': datetime.now().strftime('%d/%m/%Y'),
                'items': [
                    {
                        'type': 'Panneaux solaires',
                        'description': f"{config['panneaux']['puissance']}W {config['panneaux']['type']}",
                        'quantite': config['n_panneaux'],
                        'prix_unitaire': config['panneaux']['prix'],
                        'total': cout_panneaux
                    },
                    {
                        'type': 'Batteries',
                        'description': config['batterie']['nom'],
                        'quantite': config['n_batteries'],
                        'prix_unitaire': config['batterie']['prix'],
                        'total': cout_batteries
                    },
                    {
                        'type': 'Convertisseur',
                        'description': config['convertisseur']['nom'],
                        'quantite': 1,
                        'prix_unitaire': config['convertisseur']['prix'],
                        'total': cout_convertisseur
                    }
                ],
                'installation': cout_installation,
                'accessoires': cout_accessoires,
                'transport': cout_transport,
                'sous_total': sous_total,
                'tva': tva,
                'total_ttc': total_ttc
            }
            
            st.session_state.devis = devis_data
            
            # Affichage du devis
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 📄 Devis détaillé")
                
                # Table des composants
                st.markdown("#### Composants du système")
                df_items = pd.DataFrame(devis_data['items'])
                df_items['Prix unitaire'] = df_items['prix_unitaire'].apply(format_prix)
                df_items['Total'] = df_items['total'].apply(format_prix)
                st.dataframe(df_items[['type', 'description', 'quantite', 'Prix unitaire', 'Total']], 
                           use_container_width=True, hide_index=True)
                
                # Frais additionnels
                st.markdown("#### Frais additionnels")
                col_f1, col_f2, col_f3 = st.columns(3)
                with col_f1:
                    st.metric("Installation", format_prix(cout_installation))
                with col_f2:
                    st.metric("Accessoires", format_prix(cout_accessoires))
                with col_f3:
                    st.metric("Transport", format_prix(cout_transport))
                
                # Récapitulatif financier
                st.markdown("#### 💰 Récapitulatif")
                
                fig = go.Figure(go.Waterfall(
                    name="Devis",
                    orientation="v",
                    measure=["relative", "relative", "relative", "relative", "relative", "relative", "total"],
                    x=["Panneaux", "Batteries", "Convertisseur", "Installation", "Accessoires", "Transport", "Total HT"],
                    textposition="outside",
                    text=[format_prix(cout_panneaux), format_prix(cout_batteries), 
                          format_prix(cout_convertisseur), format_prix(cout_installation),
                          format_prix(cout_accessoires), format_prix(cout_transport), ""],
                    y=[cout_panneaux, cout_batteries, cout_convertisseur, 
                       cout_installation, cout_accessoires, cout_transport, total_ttc],
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                ))
                
                fig.update_layout(
                    title="Évolution du coût total",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🧾 Résumé")
                
                # Cartes de synthèse
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Total HT</div>
                    <div class="metric-value">{}</div>
                </div>
                """.format(format_prix(sous_total)), unsafe_allow_html=True)
                
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">TVA (20%)</div>
                    <div class="metric-value">{}</div>
                </div>
                """.format(format_prix(tva)), unsafe_allow_html=True)
                
                st.markdown("""
                <div class="metric-card" style="border-color: #00843D;">
                    <div class="metric-label" style="color: #00843D;">Total TTC</div>
                    <div class="metric-value" style="color: #00843D;">{}</div>
                </div>
                """.format(format_prix(total_ttc)), unsafe_allow_html=True)
                
                # Boutons d'action
                st.markdown("---")
                
                # WhatsApp
                whatsapp_msg = f"Bonjour, je souhaite discuter du devis {devis_data['reference']} pour un système solaire."
                whatsapp_url = f"https://wa.me/261388103083?text={whatsapp_msg}"
                
                st.markdown(f"""
                <a href="{whatsapp_url}" target="_blank">
                    <button class="whatsapp-btn" style="width: 100%; margin-bottom: 10px;">
                        💬 Discuter avec expert
                    </button>
                </a>
                """, unsafe_allow_html=True)
                
                # Export PDF
                if st.button("📄 Exporter le devis (PDF)", use_container_width=True):
                    pdf_content = generate_pdf_devis(devis_data)
                    
                    if isinstance(pdf_content, bytes):
                        b64 = base64.b64encode(pdf_content).decode()
                        href = f'<a href="data:application/pdf;base64,{b64}" download="devis_tsena_solaire_{devis_data["reference"]}.pdf">📥 Télécharger le PDF</a>'
                    else:
                        href = f'<a href="data:text/html;base64,{base64.b64encode(pdf_content).decode()}" download="devis_tsena_solaire_{devis_data["reference"]}.html">📥 Télécharger le HTML</a>'
                    
                    st.markdown(href, unsafe_allow_html=True)
                    st.success("Devis généré avec succès!")
                
                # Statistiques d'économie
                st.markdown("---")
                st.markdown("#### 💡 Économies estimées")
                
                economie_mensuelle = (config.get('energie_totale', 0) / 1000) * 350 * 30  # Estimation 350Ar/kWh
                st.metric("Économie mensuelle", f"{economie_mensuelle:,.0f} Ar")
                st.metric("Retour sur investissement", "3-4 ans")
                st.metric("Garantie système", "5 ans")

# Footer
st.markdown("""
<div class="footer">
    <h3>☀️ Tsena Solaire Malagasy</h3>
    <p>L'énergie verte pour chaque famille, partout à Madagascar</p>
    <p>📞 +261 38 81 030 83 | 📍 Antananarivo, Madagascar</p>
    <p>🌐 www.tsenasolaire.mg | ✉️ contact@tsenasolaire.mg</p>
    <p style="font-size: 0.8em; margin-top: 15px;">
        <span class="eco-badge">♻️ Énergie propre</span>
        <span class="eco-badge">🇲🇬 Made for Madagascar</span>
        <span class="eco-badge">💚 Développement durable</span>
    </p>
</div>
""", unsafe_allow_html=True)

# Message pour mobile
st.markdown("""
<script>
    // Détection mobile
    if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        // Application optimisée pour mobile
    }
</script>
""", unsafe_allow_html=True)
