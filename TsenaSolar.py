import streamlit as st
import pandas as pd
import numpy as np
import json
import base64
from datetime import datetime, timedelta
from io import BytesIO

# Configuration de la page
st.set_page_config(
    page_title="Tsena Solaire Malagasy",
    page_icon="☀️",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
    :root {
        --vert-malgache: #00843D;
        --rouge-malgache: #FC3D32;
        --jaune-soleil: #FFD700;
    }
    
    .main-title {
        background: linear-gradient(90deg, var(--vert-malgache), var(--rouge-malgache));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 10px;
    }
    
    .section-title {
        background-color: var(--vert-malgache);
        color: white;
        padding: 12px 20px;
        border-radius: 10px 10px 0 0;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 30px;
    }
    
    .product-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 2px solid var(--vert-malgache);
        box-shadow: 0 4px 15px rgba(0, 132, 61, 0.1);
    }
    
    .price-tag {
        background: linear-gradient(135deg, var(--rouge-malgache), #FF6B6B);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 5px 0;
    }
    
    .whatsapp-btn {
        background: linear-gradient(135deg, #25D366, #128C7E) !important;
        color: white !important;
        border: none !important;
        padding: 12px 20px !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        width: 100% !important;
        margin: 10px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des données
if 'materiels' not in st.session_state:
    st.session_state.materiels = []
if 'selected_config' not in st.session_state:
    st.session_state.selected_config = {}
if 'devis' not in st.session_state:
    st.session_state.devis = {}

# Base de données simplifiée
PRODUCTS_DB = {
    "panneaux": [
        {"id": "P110", "nom": "Panneau 110W", "puissance": 110, "prix": 130000},
        {"id": "P210", "nom": "Panneau 210W", "puissance": 210, "prix": 180000},
        {"id": "P550", "nom": "Panneau 550W", "puissance": 550, "prix": 500000},
        {"id": "P580", "nom": "Panneau 580W", "puissance": 580, "prix": 600000},
    ],
    "batteries": [
        {"id": 7, "nom": "Lithium 25.6V/100Ah", "energie": 2.56, "prix": 2600000},
        {"id": 8, "nom": "Lithium 51.2V/100Ah", "energie": 5.12, "prix": 5000000},
        {"id": 9, "nom": "Lithium 51.2V/200Ah", "energie": 10.24, "prix": 9000000},
    ],
    "convertisseurs": [
        {"id": 1, "nom": "Onduleur 24V/3KW", "puissance": 3000, "prix": 1400000},
        {"id": 2, "nom": "Onduleur 48V/5KW", "puissance": 5000, "prix": 2400000},
        {"id": 3, "nom": "Onduleur 48V/10KW", "puissance": 10000, "prix": 6000000},
    ]
}

# Fonctions utilitaires
def format_prix(prix):
    return f"{prix:,.0f} Ar".replace(",", " ")

def calculate_config(energie_totale, puissance_max):
    """Calcule la configuration optimale"""
    # Paramètres par défaut
    rendement = 0.85
    autonomie = 2
    profondeur_decharge = 0.8
    heures_soleil = 5.5
    marge_securite = 1.25
    
    # Calculs
    energie_necessaire = energie_totale / rendement
    
    # Sélection panneau (choisir le plus efficace)
    panneau = max(PRODUCTS_DB['panneaux'], key=lambda x: x['puissance'])
    energie_panneau_jour = panneau['puissance'] * heures_soleil
    n_panneaux = max(1, int(np.ceil(energie_necessaire / energie_panneau_jour)))
    
    # Sélection batterie
    capacite_necessaire_wh = (energie_totale * autonomie) / profondeur_decharge
    batterie = None
    for b in PRODUCTS_DB['batteries']:
        capacite_wh = b['energie'] * 1000
        if capacite_wh >= capacite_necessaire_wh * 0.8:
            batterie = b
            break
    if not batterie:
        batterie = max(PRODUCTS_DB['batteries'], key=lambda x: x['energie'])
    
    n_batteries = max(1, int(np.ceil(capacite_necessaire_wh / (batterie['energie'] * 1000))))
    
    # Sélection convertisseur
    puissance_convertisseur = puissance_max * marge_securite
    convertisseur = None
    for c in PRODUCTS_DB['convertisseurs']:
        if c['puissance'] >= puissance_convertisseur:
            convertisseur = c
            break
    if not convertisseur:
        convertisseur = max(PRODUCTS_DB['convertisseurs'], key=lambda x: x['puissance'])
    
    return {
        'panneau': panneau,
        'n_panneaux': n_panneaux,
        'batterie': batterie,
        'n_batteries': n_batteries,
        'convertisseur': convertisseur,
        'energie_totale': energie_totale,
        'capacite_necessaire_wh': capacite_necessaire_wh
    }

# Interface principale
st.markdown('<h1 class="main-title">☀️ TSENA SOLAIRE MALAGASY</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #00843D;">Énergie verte accessible à tous les Malagasy</p>', unsafe_allow_html=True)

# Bouton WhatsApp
st.markdown("""
<div style="text-align: center; margin: 20px 0;">
    <a href="https://wa.me/261388103083?text=Bonjour%2C%20je%20souhaite%20un%20devis%20solaire" target="_blank">
        <button class="whatsapp-btn">
            💬 Discuter avec expert WhatsApp
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

# Onglets
tabs = st.tabs(["📊 Calcul Conso", "🛒 Produits", "⚡ Configuration", "💰 Devis"])

# Tab 1: Calcul de consommation
with tabs[0]:
    st.markdown('<div class="section-title">Calcul de votre consommation</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("ajout_form"):
            nom = st.text_input("Équipement", placeholder="Ex: Réfrigérateur")
            puissance = st.number_input("Puissance (W)", min_value=1, value=100)
            quantite = st.number_input("Quantité", min_value=1, value=1)
            heures = st.number_input("Heures/jour", min_value=0.0, value=8.0)
            
            if st.form_submit_button("➕ Ajouter l'équipement"):
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
    
    with col2:
        st.markdown("**💡 Équipements courants**")
        if st.button("➕ Ampoule LED 10W (5h/jour)"):
            st.session_state.materiels.append({
                "Équipement": "Ampoule LED 10W",
                "Puissance (W)": 10,
                "Quantité": 1,
                "Heures/jour": 5,
                "Énergie (Wh/jour)": 50
            })
            st.rerun()
        
        if st.button("➕ Réfrigérateur 150W (24h/jour)"):
            st.session_state.materiels.append({
                "Équipement": "Réfrigérateur 150W",
                "Puissance (W)": 150,
                "Quantité": 1,
                "Heures/jour": 24,
                "Énergie (Wh/jour)": 3600
            })
            st.rerun()
        
        if st.button("➕ TV LED 50W (4h/jour)"):
            st.session_state.materiels.append({
                "Équipement": "TV LED 50W",
                "Puissance (W)": 50,
                "Quantité": 1,
                "Heures/jour": 4,
                "Énergie (Wh/jour)": 200
            })
            st.rerun()
    
    # Affichage des équipements
    if st.session_state.materiels:
        st.markdown("### 📋 Votre consommation")
        
        df = pd.DataFrame(st.session_state.materiels)
        total_energie = df["Énergie (Wh/jour)"].sum()
        total_puissance = (df["Puissance (W)"] * df["Quantité"]).sum()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Énergie quotidienne", f"{total_energie:,.0f} Wh")
        with col2:
            st.metric("Puissance totale", f"{total_puissance:,.0f} W")
        with col3:
            st.metric("Nombre d'équipements", len(df))
        
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ Réinitialiser"):
            st.session_state.materiels = []
            st.rerun()
    else:
        st.info("Commencez par ajouter vos équipements")

# Tab 2: Produits
with tabs[1]:
    st.markdown('<div class="section-title">Nos produits</div>', unsafe_allow_html=True)
    
    categorie = st.selectbox("Catégorie", ["Panneaux solaires", "Batteries", "Convertisseurs"])
    
    if categorie == "Panneaux solaires":
        for produit in PRODUCTS_DB['panneaux']:
            st.markdown(f"""
            <div class="product-card">
                <h4>{produit['nom']}</h4>
                <div class="price-tag">{format_prix(produit['prix'])}</div>
                <p>Puissance: {produit['puissance']}W</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif categorie == "Batteries":
        for produit in PRODUCTS_DB['batteries']:
            st.markdown(f"""
            <div class="product-card">
                <h4>{produit['nom']}</h4>
                <div class="price-tag">{format_prix(produit['prix'])}</div>
                <p>Énergie: {produit['energie']} kWh</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif categorie == "Convertisseurs":
        for produit in PRODUCTS_DB['convertisseurs']:
            st.markdown(f"""
            <div class="product-card">
                <h4>{produit['nom']}</h4>
                <div class="price-tag">{format_prix(produit['prix'])}</div>
                <p>Puissance: {produit['puissance']:,}W</p>
            </div>
            """, unsafe_allow_html=True)

# Tab 3: Configuration
with tabs[2]:
    st.markdown('<div class="section-title">Configuration automatique</div>', unsafe_allow_html=True)
    
    if not st.session_state.materiels:
        st.warning("Calculez d'abord votre consommation")
    else:
        df = pd.DataFrame(st.session_state.materiels)
        energie_totale = df["Énergie (Wh/jour)"].sum()
        puissance_max = (df["Puissance (W)"] * df["Quantité"]).max()
        
        if st.button("🔍 Calculer configuration optimale", use_container_width=True):
            config = calculate_config(energie_totale, puissance_max)
            st.session_state.selected_config = config
            st.success("Configuration calculée!")
        
        if st.session_state.selected_config:
            config = st.session_state.selected_config
            
            st.markdown("### 🎯 Configuration recommandée")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Panneaux", config['n_panneaux'])
            with col2:
                st.metric("Batteries", config['n_batteries'])
            with col3:
                st.metric("Convertisseur", f"{config['convertisseur']['puissance']:,}W")
            with col4:
                prix_total = (
                    config['panneau']['prix'] * config['n_panneaux'] +
                    config['batterie']['prix'] * config['n_batteries'] +
                    config['convertisseur']['prix']
                )
                st.metric("Budget estimé", format_prix(prix_total))
            
            # Détails
            st.markdown("#### Détails des composants")
            
            st.markdown(f"**{config['panneau']['nom']}**")
            st.markdown(f"- Quantité: {config['n_panneaux']}")
            st.markdown(f"- Prix unitaire: {format_prix(config['panneau']['prix'])}")
            st.markdown(f"- Total: {format_prix(config['panneau']['prix'] * config['n_panneaux'])}")
            
            st.markdown(f"**{config['batterie']['nom']}**")
            st.markdown(f"- Quantité: {config['n_batteries']}")
            st.markdown(f"- Prix unitaire: {format_prix(config['batterie']['prix'])}")
            st.markdown(f"- Total: {format_prix(config['batterie']['prix'] * config['n_batteries'])}")
            
            st.markdown(f"**{config['convertisseur']['nom']}**")
            st.markdown(f"- Prix: {format_prix(config['convertisseur']['prix'])}")

# Tab 4: Devis
with tabs[3]:
    st.markdown('<div class="section-title">Votre devis</div>', unsafe_allow_html=True)
    
    if not st.session_state.selected_config:
        st.info("Configurez d'abord votre système")
    else:
        config = st.session_state.selected_config
        
        # Calcul du devis
        cout_panneaux = config['panneau']['prix'] * config['n_panneaux']
        cout_batteries = config['batterie']['prix'] * config['n_batteries']
        cout_convertisseur = config['convertisseur']['prix']
        cout_installation = (cout_panneaux + cout_batteries + cout_convertisseur) * 0.15
        cout_accessoires = 250000
        cout_transport = 150000
        
        sous_total = cout_panneaux + cout_batteries + cout_convertisseur + cout_installation + cout_accessoires + cout_transport
        tva = sous_total * 0.20
        total_ttc = sous_total + tva
        
        # Affichage
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Détail du devis")
            
            data = {
                "Composant": ["Panneaux", "Batteries", "Convertisseur", "Installation", "Accessoires", "Transport"],
                "Montant (Ar)": [
                    format_prix(cout_panneaux),
                    format_prix(cout_batteries),
                    format_prix(cout_convertisseur),
                    format_prix(cout_installation),
                    format_prix(cout_accessoires),
                    format_prix(cout_transport)
                ]
            }
            
            df_devis = pd.DataFrame(data)
            st.dataframe(df_devis, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown(f"**Sous-total:** {format_prix(sous_total)}")
            st.markdown(f"**TVA (20%):** {format_prix(tva)}")
            st.markdown(f"### **Total TTC:** {format_prix(total_ttc)}")
        
        with col2:
            st.markdown("### 🧾 Résumé")
            
            # Sauvegarder le devis
            devis_data = {
                'reference': f"TS-{datetime.now().strftime('%Y%m%d')}",
                'date': datetime.now().strftime('%d/%m/%Y'),
                'total_ttc': total_ttc,
                'details': {
                    'panneaux': cout_panneaux,
                    'batteries': cout_batteries,
                    'convertisseur': cout_convertisseur,
                    'installation': cout_installation,
                    'accessoires': cout_accessoires,
                    'transport': cout_transport,
                    'tva': tva
                }
            }
            
            st.session_state.devis = devis_data
            
            # Bouton WhatsApp avec devis
            whatsapp_msg = f"""
Bonjour, je souhaite discuter du devis solaire suivant:

Référence: {devis_data['reference']}
Date: {devis_data['date']}
Total estimé: {format_prix(total_ttc)}

Détails:
- Panneaux: {format_prix(cout_panneaux)}
- Batteries: {format_prix(cout_batteries)}
- Convertisseur: {format_prix(cout_convertisseur)}
- Total TTC: {format_prix(total_ttc)}

Pouvez-vous m'en dire plus?
            """.replace("\n", "%0A")
            
            whatsapp_url = f"https://wa.me/261388103083?text={whatsapp_msg}"
            
            st.markdown(f"""
            <a href="{whatsapp_url}" target="_blank">
                <button class="whatsapp-btn">
                    💬 Demander devis détaillé
                </button>
            </a>
            """, unsafe_allow_html=True)
            
            # Export JSON
            if st.button("💾 Sauvegarder le devis"):
                json_data = json.dumps(devis_data, indent=2)
                b64 = base64.b64encode(json_data.encode()).decode()
                href = f'<a href="data:application/json;base64,{b64}" download="devis_tsena_{devis_data["reference"]}.json">📥 Télécharger le devis (JSON)</a>'
                st.markdown(href, unsafe_allow_html=True)
            
            # Économies
            st.markdown("---")
            st.markdown("#### 💡 Économies estimées")
            
            economie_mensuelle = (config['energie_totale'] / 1000) * 350 * 30
            st.metric("Économie mensuelle", f"{economie_mensuelle:,.0f} Ar")
            st.metric("Retour sur investissement", "3-4 ans")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #00843D; padding: 20px;">
    <h3>☀️ Tsena Solaire Malagasy</h3>
    <p>Énergie verte pour chaque famille malgache</p>
    <p>📞 +261 38 81 030 83 | 📍 Antananarivo, Madagascar</p>
    <p>💚 Ensemble pour un Madagascar plus vert !</p>
</div>
""", unsafe_allow_html=True)
